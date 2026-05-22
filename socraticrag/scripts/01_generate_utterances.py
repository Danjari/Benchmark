"""
Script 01: Student Utterance Generator
Input:  data/chunks.jsonl (manually curated — run 00 then hand-pick 20 chunks)
Output: data/utterances_raw.jsonl

Two-step contrastive generation per chunk C:
  Step 1 — Concept extraction: identify the primary teachable concept in C,
            derive what correct vs. incorrect understanding looks like from C alone.
  Step 2a — Contrastive pair (accurate/erroneous): both target the same concept.
  Step 2b — Contrastive pair (comprehension/confusion): both target the same concept.

Each output row includes Profile P = {cognitive_state, target_concept,
correct_understanding, misconception (erroneous only)} as a first-class field,
distinct from utterance U. This guarantees:
  - Erroneous misconceptions are grounded in C, not imported from external lists.
  - Contrastive pairs target the same concept (structural requirement for Metric 3).
"""

import os
import json
import asyncio
from pathlib import Path
from openai import AsyncOpenAI
from dotenv import load_dotenv
from tqdm.asyncio import tqdm

load_dotenv()

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

CHUNKS_FILE = Path("data/chunks.jsonl")
OUTPUT_FILE = Path("data/utterances_raw.jsonl")

# ── Prompts ────────────────────────────────────────────────────────────────────

CONCEPT_EXTRACTION_PROMPT = """You are preparing a benchmark dataset for evaluating AI tutoring systems.

Given this educational chunk C from {course}:

---
{chunk_text}
---

Identify the ONE primary teachable concept in this chunk. Then characterize:
1. What a correct understanding of this concept looks like (from C only).
2. A specific, plausible misconception about this concept — derived ONLY from what is stated or implied in C. Do NOT import misconceptions from outside C.

Respond ONLY with valid JSON:
{{
  "target_concept": "the specific concept name (e.g., 'gradient descent convergence')",
  "correct_understanding": "1-2 sentences describing what correct understanding looks like",
  "common_misconception": "1-2 sentences describing a specific wrong belief that could arise from misreading C"
}}"""

CONTRASTIVE_AE_PROMPT = """You are generating benchmark data for an AI tutoring evaluation system.

Context C ({course}):
---
{chunk_text}
---

Target concept: {target_concept}
Correct understanding of this concept (from C): {correct_understanding}
Specific misconception about this concept (derived from C): {common_misconception}

Generate two student utterances forming a CONTRASTIVE PAIR. Both must target "{target_concept}" as described in C.

1. ACCURATE: Student correctly understands the concept and asks a natural follow-up or makes a correct observation. Shows genuine understanding.
2. ERRONEOUS: Student expresses the specific misconception above. The error must be clearly about "{target_concept}" as described in C. Do NOT introduce concepts absent from C.

Respond ONLY with valid JSON:
{{
  "accurate": {{
    "utterance": "...",
    "demonstrates": "what correct understanding this utterance shows"
  }},
  "erroneous": {{
    "utterance": "...",
    "misconception_expressed": "the specific wrong belief the student is expressing"
  }}
}}"""

CONTRASTIVE_CC_PROMPT = """You are generating benchmark data for an AI tutoring evaluation system.

Context C ({course}):
---
{chunk_text}
---

Target concept: {target_concept}

Generate two student utterances forming a CONTRASTIVE PAIR. Both must target "{target_concept}" as described in C.

1. COMPREHENSION: Student explicitly states they understood something specific about "{target_concept}". Must use explicit comprehension markers ("I think I understand now that...", "So what you're saying is...", "Ah, I see —").
2. CONFUSION: Student explicitly expresses uncertainty about something specific about "{target_concept}". Must use explicit confusion markers ("I'm confused about...", "I don't understand why...", "Wait, I'm not sure...").

Both utterances must reference ONLY concepts present in C.

Respond ONLY with valid JSON:
{{
  "comprehension": {{
    "utterance": "...",
    "what_they_understood": "the specific aspect they claim to understand"
  }},
  "confusion": {{
    "utterance": "...",
    "source_of_confusion": "what specifically in C is causing the confusion"
  }}
}}"""

# ── API helpers ────────────────────────────────────────────────────────────────

async def gpt4o(prompt: str, semaphore: asyncio.Semaphore, temperature: float = 0.5) -> dict | None:
    async with semaphore:
        try:
            response = await client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=temperature,
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"  API error: {e}")
            return None


# ── Core generation ────────────────────────────────────────────────────────────

async def generate_for_chunk(chunk: dict, semaphore: asyncio.Semaphore) -> list[dict] | None:
    chunk_id = chunk["chunk_id"]
    chunk_text = chunk["text"]
    course = chunk["course"]

    # Step 1: extract the primary concept from C
    concept = await gpt4o(
        CONCEPT_EXTRACTION_PROMPT.format(chunk_text=chunk_text, course=course),
        semaphore,
        temperature=0.3,
    )
    if not concept or "target_concept" not in concept:
        print(f"  [SKIP] concept extraction failed for {chunk_id}")
        return None

    target_concept = concept["target_concept"]
    correct_understanding = concept["correct_understanding"]
    common_misconception = concept["common_misconception"]

    # Step 2a: contrastive pair — accurate / erroneous (same concept)
    ae = await gpt4o(
        CONTRASTIVE_AE_PROMPT.format(
            chunk_text=chunk_text,
            course=course,
            target_concept=target_concept,
            correct_understanding=correct_understanding,
            common_misconception=common_misconception,
        ),
        semaphore,
    )

    # Step 2b: contrastive pair — comprehension / confusion (same concept)
    cc = await gpt4o(
        CONTRASTIVE_CC_PROMPT.format(
            chunk_text=chunk_text,
            course=course,
            target_concept=target_concept,
        ),
        semaphore,
    )

    if not ae or not cc:
        print(f"  [SKIP] pair generation failed for {chunk_id}")
        return None

    rows = []

    if "accurate" in ae:
        rows.append({
            "utterance_id": f"{chunk_id}_accurate",
            "chunk_id": chunk_id,
            "chunk_text": chunk_text,
            "course": course,
            "source": chunk["source"],
            "profile": {
                "cognitive_state": "accurate",
                "target_concept": target_concept,
                "correct_understanding": correct_understanding,
                "demonstrates": ae["accurate"].get("demonstrates", ""),
            },
            "utterance": ae["accurate"]["utterance"],
            "dean_validated": False,
        })

    if "erroneous" in ae:
        rows.append({
            "utterance_id": f"{chunk_id}_erroneous",
            "chunk_id": chunk_id,
            "chunk_text": chunk_text,
            "course": course,
            "source": chunk["source"],
            "profile": {
                "cognitive_state": "erroneous",
                "target_concept": target_concept,
                "correct_understanding": correct_understanding,
                "misconception": ae["erroneous"].get("misconception_expressed", common_misconception),
            },
            "utterance": ae["erroneous"]["utterance"],
            "dean_validated": False,
        })

    if "comprehension" in cc:
        rows.append({
            "utterance_id": f"{chunk_id}_comprehension",
            "chunk_id": chunk_id,
            "chunk_text": chunk_text,
            "course": course,
            "source": chunk["source"],
            "profile": {
                "cognitive_state": "comprehension",
                "target_concept": target_concept,
                "correct_understanding": correct_understanding,
                "what_they_understood": cc["comprehension"].get("what_they_understood", ""),
            },
            "utterance": cc["comprehension"]["utterance"],
            "dean_validated": False,
        })

    if "confusion" in cc:
        rows.append({
            "utterance_id": f"{chunk_id}_confusion",
            "chunk_id": chunk_id,
            "chunk_text": chunk_text,
            "course": course,
            "source": chunk["source"],
            "profile": {
                "cognitive_state": "confusion",
                "target_concept": target_concept,
                "correct_understanding": correct_understanding,
                "source_of_confusion": cc["confusion"].get("source_of_confusion", ""),
            },
            "utterance": cc["confusion"]["utterance"],
            "dean_validated": False,
        })

    return rows if len(rows) == 4 else None


# ── Main ───────────────────────────────────────────────────────────────────────

async def main():
    chunks = []
    with open(CHUNKS_FILE) as f:
        for line in f:
            chunks.append(json.loads(line))

    print(f"Loaded {len(chunks)} chunks. Generating utterances (2-step contrastive)...")

    semaphore = asyncio.Semaphore(3)  # 3 concurrent chunks × 3 calls each = 9 max concurrent
    tasks = [generate_for_chunk(chunk, semaphore) for chunk in chunks]
    results = await tqdm.gather(*tasks, desc="Generating")

    all_utterances = []
    failed = 0
    for result in results:
        if result:
            all_utterances.extend(result)
        else:
            failed += 1

    with open(OUTPUT_FILE, "w") as f:
        for u in all_utterances:
            f.write(json.dumps(u) + "\n")

    print(f"\nGenerated {len(all_utterances)} utterances from {len(chunks) - failed}/{len(chunks)} chunks")
    print(f"Expected: {len(chunks) * 4}  |  Got: {len(all_utterances)}  |  Failed chunks: {failed}")
    print(f"Contrastive pairs: {len(all_utterances) // 2} (accurate/erroneous + comprehension/confusion per chunk)")
    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    asyncio.run(main())
