"""
Script 00: Corpus Chunker
Input:  PDF files in data/pdfs/{course}/
Output: data/chunks.jsonl

Uses Mistral OCR for text extraction (preserves slide structure, headers, visual content)
then RecursiveCharacterTextSplitter with markdown-aware splitting — ported from SynapsEd.
"""

import os
import json
import hashlib
import base64
import tiktoken
from pathlib import Path
from mistralai import Mistral
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from dotenv import load_dotenv

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
TOKENIZER = tiktoken.get_encoding("cl100k_base")

# chunk_size is in characters (~250 tokens at 4 chars/token); paper target is 200–500 tokens
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
MIN_CHUNK_TOKENS = 150  # filter slide headers and orphaned fragments
PDF_DIR = Path("data/pdfs")
OUTPUT_FILE = Path("data/chunks.jsonl")


def count_tokens(text: str) -> int:
    return len(TOKENIZER.encode(text))


def get_ocr_markdown(pdf_path: Path) -> list[dict]:
    """Extract per-page markdown from a PDF using Mistral OCR."""
    with open(pdf_path, "rb") as f:
        b64 = base64.standard_b64encode(f.read()).decode()

    response = client.ocr.process(
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


def chunk_markdown_by_page(
    pages: list[dict],
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> list[dict]:
    """Chunk per-page markdown using markdown-aware recursive splitting."""
    splitter = RecursiveCharacterTextSplitter.from_language(
        Language.MARKDOWN,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    all_chunks = []
    for page in pages:
        docs = splitter.create_documents([page["markdown"]])
        for doc in docs:
            lines = doc.metadata.get("loc", {}).get("lines", {"from": 0, "to": 0})
            all_chunks.append({
                "text": doc.page_content,
                "metadata": {
                    "page": page["page"],
                    "lines": lines,
                },
            })

    return all_chunks


def process_pdf(pdf_path: Path, course: str) -> list[dict]:
    print(f"  OCR: {pdf_path.name}...")
    pages = get_ocr_markdown(pdf_path)
    print(f"  Chunking {len(pages)} pages...")
    raw_chunks = chunk_markdown_by_page(pages)

    results = []
    skipped = 0
    for i, chunk in enumerate(raw_chunks):
        text = chunk["text"].strip()
        if not text:
            continue
        tokens = count_tokens(text)
        if tokens < MIN_CHUNK_TOKENS:
            skipped += 1
            continue
        chunk_id = hashlib.md5(f"{pdf_path.name}_{i}".encode()).hexdigest()[:8]
        results.append({
            "chunk_id": chunk_id,
            "source": pdf_path.name,
            "course": course,
            "chunk_index": i,
            "page": chunk["metadata"]["page"],
            "lines": chunk["metadata"]["lines"],
            "text": text,
            "token_count": count_tokens(text),
        })

    if skipped:
        print(f"  Filtered {skipped} sub-threshold chunks (< {MIN_CHUNK_TOKENS} tokens)")
    return results


def main():
    if not PDF_DIR.exists():
        print(f"Create {PDF_DIR} with course subfolders:")
        print("  data/pdfs/6.7960/  — Deep Learning lecture notes")
        print("  data/pdfs/6.036/   — Intro to ML lecture notes")
        return

    all_chunks = []
    for course_dir in sorted(PDF_DIR.iterdir()):
        if not course_dir.is_dir():
            continue
        course = course_dir.name
        pdfs = sorted(course_dir.glob("*.pdf"))
        if not pdfs:
            print(f"No PDFs found in {course_dir}")
            continue
        for pdf_file in pdfs:
            print(f"\nProcessing {pdf_file.name} ({course})")
            chunks = process_pdf(pdf_file, course)
            all_chunks.extend(chunks)
            print(f"  -> {len(chunks)} chunks")

    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        for chunk in all_chunks:
            f.write(json.dumps(chunk) + "\n")

    print(f"\nTotal chunks: {len(all_chunks)}")
    print(f"Saved to {OUTPUT_FILE}")

    tokens = [c["token_count"] for c in all_chunks]
    if tokens:
        print(f"Token distribution — min: {min(tokens)}  max: {max(tokens)}  avg: {sum(tokens)//len(tokens)}")


if __name__ == "__main__":
    main()
