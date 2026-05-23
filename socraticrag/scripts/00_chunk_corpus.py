"""
Script 00: Corpus Chunker
Input:  PDF files in data/pdfs/{course}/
Output: data/chunks.jsonl

Two-step pipeline:
  Step 1 — Mistral OCR: PDF → per-page markdown
            Preserves slide structure, equations, tables, and visual layout markers.

  Step 2 — Propositionizer: per-page markdown → concept units via GPT-4o
            Each concept unit covers exactly ONE teachable concept from the source,
            with original wording preserved. Enforces the paper's claim that
            C = "a single concept such as a definition, worked example, or explanation."

Methodology: concept-level chunking following Chen et al. (EMNLP 2024) "Dense X Retrieval:
What Retrieval Granularity Should We Use?" (arXiv:2312.06648), adapted from atomic
propositions to concept-level units appropriate for multi-sentence educational RAG context.

Output schema per chunk:
  chunk_id     — 8-char MD5 hash of (source_filename, chunk_index)
  source       — PDF filename
  course       — full course name from COURSE_NAMES mapping (e.g. "MIT 6.7960 Deep Learning (Fall 2024)")
  chunk_index  — sequential index within the document
  page         — source page number
  concept      — short concept label extracted by the Propositionizer (metadata only)
  text         — concept unit text, preserving original wording
  token_count  — cl100k_base token count
"""

import os
import re
import json
import hashlib
import base64
import asyncio
import tiktoken
from pathlib import Path
from mistralai import Mistral
from openai import AsyncOpenAI
from dotenv import load_dotenv
from tqdm.asyncio import tqdm

load_dotenv()

mistral_client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
TOKENIZER = tiktoken.get_encoding("cl100k_base")

MIN_CHUNK_TOKENS = 100   # below this a unit lacks enough content for tutoring
MAX_CHUNK_TOKENS = 500   # above this a unit spans multiple concepts; paper target: 200–500
PDF_DIR = Path("data/pdfs")
OUTPUT_FILE = Path("data/chunks.jsonl")
CHECKPOINT_FILE = Path("data/.chunks_checkpoint.json")

COURSE_NAMES = {
    "deeplearning":    "MIT 6.7960 Deep Learning (Fall 2024)",
    "machinelearning": "MIT 6.036 Introduction to Machine Learning",
}

# ── Propositionizer prompt ─────────────────────────────────────────────────────

PROPOSITIONIZER_PROMPT = """You are preparing a benchmark dataset for AI tutoring evaluation.

Given this educational content from a {course} lecture (page {page}):

---
{markdown}
---

Extract CONCEPT UNITS. A concept unit is a self-contained block of text covering exactly ONE teachable idea — a definition, theorem, algorithm, property, or worked example — that a student and tutor could discuss in a single interaction.

Requirements for each unit:
1. ONE concept only — do not bundle multiple distinct ideas into one unit
2. Self-contained — the text must be intelligible without surrounding context
3. Preserve original wording — copy text as it appears; do not paraphrase or summarize
4. Substantive — must contain at minimum one claim plus its explanation or implication

Skip entirely:
- Slide titles, section headers, and lecture labels used only for navigation
- Enumerations that name topics without explaining them (e.g., "Topics: 1. X 2. Y 3. Z")
- Image captions and figure references without substantive explanation
- Administrative text (office hours, grading policies, course logistics)

Output rules:
- If the page has one coherent concept, return one unit
- If it has multiple distinct concepts, split them into separate units
- If the page has no extractable concept units (title slide, agenda, image-only), return an empty list

Respond ONLY with valid JSON:
{{
  "units": [
    {{
      "concept": "concise concept label, 5 words max (e.g. 'vanishing gradient problem')",
      "text": "exact text from the page, preserving original wording"
    }}
  ]
}}"""


# ── OCR ────────────────────────────────────────────────────────────────────────

def count_tokens(text: str) -> int:
    return len(TOKENIZER.encode(text))


def get_ocr_markdown(pdf_path: Path) -> list[dict]:
    """Extract per-page markdown from a PDF using Mistral OCR."""
    with open(pdf_path, "rb") as f:
        b64 = base64.standard_b64encode(f.read()).decode()

    response = mistral_client.ocr.process(
        model="mistral-ocr-latest",
        document={
            "type": "document_url",
            "document_url": f"data:application/pdf;base64,{b64}",
        },
    )

    return [
        {"page": (page.index if page.index is not None else i) + 1, "markdown": page.markdown}
        for i, page in enumerate(response.pages)
    ]


# ── Propositionizer ────────────────────────────────────────────────────────────

async def extract_concept_units(
    page: dict,
    course: str,
    semaphore: asyncio.Semaphore,
) -> list[dict]:
    """Decompose one page's markdown into concept units via GPT-4o with retry on rate limits."""
    async with semaphore:
        units = []
        for attempt in range(5):
            try:
                response = await openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{
                        "role": "user",
                        "content": PROPOSITIONIZER_PROMPT.format(
                            course=course,
                            page=page["page"],
                            markdown=page["markdown"],
                        ),
                    }],
                    response_format={"type": "json_object"},
                    temperature=0.1,
                )
                result = json.loads(response.choices[0].message.content)
                units = result.get("units", [])
                break
            except Exception as e:
                err = str(e)
                if "429" in err:
                    match = re.search(r"try again in (\d+(?:\.\d+)?)s", err)
                    wait = float(match.group(1)) + 1.0 if match else 2 ** attempt
                    await asyncio.sleep(wait)
                else:
                    print(f"  [WARN] Page {page['page']} attempt {attempt + 1}: {e}")
                    break

    valid = []
    for u in units:
        text = u.get("text", "").strip()
        if not text:
            continue
        tokens = count_tokens(text)
        if tokens < MIN_CHUNK_TOKENS:
            continue  # too short: slide header or orphaned fragment
        if tokens > MAX_CHUNK_TOKENS:
            # Unit spans too many tokens — likely a multi-concept block the model didn't split.
            # Accept it but flag: the Dean in script 02 will reject utterances
            # that can't be derived from C alone, which acts as a downstream safety net.
            pass
        valid.append({
            "text": text,
            "concept": u.get("concept", "").strip(),
            "page": page["page"],
            "token_count": tokens,
        })

    return valid


# ── PDF processing ─────────────────────────────────────────────────────────────

async def process_pdf(
    pdf_path: Path,
    course: str,
    semaphore: asyncio.Semaphore,
) -> list[dict]:
    print(f"  OCR: {pdf_path.name}...")
    pages = await asyncio.to_thread(get_ocr_markdown, pdf_path)
    print(f"  Propositionizing {len(pages)} pages...")

    tasks = [extract_concept_units(page, course, semaphore) for page in pages]
    page_results = await tqdm.gather(*tasks, desc=f"  {pdf_path.stem}", leave=False)

    all_units = [unit for page_units in page_results for unit in page_units]

    chunks = []
    for i, unit in enumerate(all_units):
        chunk_id = hashlib.md5(f"{pdf_path.name}_{i}".encode()).hexdigest()[:8]
        chunks.append({
            "chunk_id": chunk_id,
            "source": pdf_path.name,
            "course": course,
            "chunk_index": i,
            "page": unit["page"],
            "concept": unit["concept"],
            "text": unit["text"],
            "token_count": unit["token_count"],
        })

    return chunks


# ── Main ───────────────────────────────────────────────────────────────────────

async def main():
    if not PDF_DIR.exists():
        print(f"Create {PDF_DIR} with course subfolders:")
        print("  data/pdfs/deeplearning/    — Deep Learning lecture notes")
        print("  data/pdfs/machinelearning/ — Intro to ML notes")
        return

    OUTPUT_FILE.parent.mkdir(exist_ok=True)

    # Resume support: load already-processed PDFs from checkpoint
    processed: set[str] = set()
    if CHECKPOINT_FILE.exists() and OUTPUT_FILE.exists():
        with open(CHECKPOINT_FILE) as f:
            processed = set(json.load(f))
        saved = sum(1 for _ in open(OUTPUT_FILE))
        print(f"Resuming: {len(processed)} PDF(s) already done, {saved} chunks on disk.\n")
    elif OUTPUT_FILE.exists():
        OUTPUT_FILE.unlink()  # output exists but no checkpoint — start fresh

    semaphore = asyncio.Semaphore(2)  # 2 concurrent Propositionizer calls — stays within 30k TPM
    new_chunks = 0

    for course_dir in sorted(PDF_DIR.iterdir()):
        if not course_dir.is_dir():
            continue
        course = COURSE_NAMES.get(course_dir.name, course_dir.name)
        pdfs = sorted(course_dir.glob("*.pdf"))
        if not pdfs:
            print(f"No PDFs found in {course_dir}")
            continue
        for pdf_file in pdfs:
            pdf_key = str(pdf_file)
            if pdf_key in processed:
                print(f"  Skipping {pdf_file.name} (already processed)")
                continue

            print(f"\nProcessing {pdf_file.name} ({course})")
            chunks = await process_pdf(pdf_file, course, semaphore)

            # Save this PDF's chunks immediately
            with open(OUTPUT_FILE, "a") as f:
                for chunk in chunks:
                    f.write(json.dumps(chunk) + "\n")

            processed.add(pdf_key)
            with open(CHECKPOINT_FILE, "w") as f:
                json.dump(list(processed), f)

            print(f"  → {len(chunks)} concept units (saved)")
            new_chunks += len(chunks)

    # Final summary across all chunks on disk
    all_chunks = []
    with open(OUTPUT_FILE) as f:
        all_chunks = [json.loads(line) for line in f]

    print(f"\nDone. {new_chunks} new chunks this run, {len(all_chunks)} total in {OUTPUT_FILE}")
    if all_chunks:
        tokens = [c["token_count"] for c in all_chunks]
        over = sum(1 for t in tokens if t > MAX_CHUNK_TOKENS)
        print(f"Token distribution — min: {min(tokens)}  max: {max(tokens)}  avg: {sum(tokens)//len(tokens)}")
        if over:
            print(f"  Note: {over} units exceed {MAX_CHUNK_TOKENS} tokens (multi-concept candidates — review manually)")
    print("\nTo start fresh: delete data/chunks.jsonl and data/.chunks_checkpoint.json")


if __name__ == "__main__":
    asyncio.run(main())
