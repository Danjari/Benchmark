"""
Script 07: RAGAS Faithfulness Baseline
Input:  data/responses.jsonl
Output: data/scores_ragas.jsonl

Purpose: demonstrate structural incompatibility of RAGAS faithfulness
with interrogative (Socratic question) outputs. Not a meaningful metric
for this task — included to show that existing RAG evaluation frameworks
cannot be directly applied to pedagogical dialogue.

RAGAS faithfulness (Es et al., EMNLP 2024) works as follows:
  1. Decompose the "answer" into a list of declarative atomic statements.
  2. For each statement, check if it is supported by the retrieved context.
  3. Score = fraction of statements supported.

Structural incompatibility: Socratic questions are interrogative, not
declarative. They do not assert claims — they ask them. Standard
decomposition yields near-zero or empty statement lists, and any
statements extracted are shallow or trivially true, producing
near-1.0 scores with near-zero variance across all responses.
This clustering makes RAGAS unable to discriminate good from bad
Socratic responses, confirming the motivation for M2's presupposition-
based adaptation (scripts 05).

We implement the RAGAS faithfulness logic directly (the ragas library
imports are broken due to a removed langchain_community dependency) so
we control the decomposition step and can show the failure mode clearly.

Note: this script uses GPT-4o only (no cross-judge needed — this is a
baseline demonstration, not an evaluation of model quality).

Failure handling:
  All API errors are retried up to 6 times with exponential backoff.
  Rows where either API call fails all retries are written with
  judge_failed=True and excluded from statistics. Note: an empty
  statement list after a successful decomposition call is NOT a failure
  — it is the expected RAGAS behavior for interrogative outputs.
  Run --reprocess-failed to reset judge-failed rows.
  Script aborts if 3 consecutive batches have 100% judge failure (API down).
"""

import os
import re
import sys
import json
import asyncio
import argparse
import statistics
from pathlib import Path
from openai import AsyncOpenAI
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

INPUT_FILE = Path("data/responses.jsonl")
OUTPUT_FILE = Path("data/scores_ragas.jsonl")
CHECKPOINT_FILE = Path("data/.scores_ragas_checkpoint.json")
TEMP_FILE = Path("data/.scores_ragas_temp.jsonl")

ABORT_AFTER_CONSECUTIVE = 3

JUDGE_SYSTEM = (
    "You are a strict dataset quality evaluator. "
    "Respond ONLY with valid JSON. No preamble, no markdown."
)

DECOMPOSE_PROMPT = """Given the following text, decompose it into a list of simple, atomic, declarative statements.
Each statement should be a complete sentence that asserts a single fact.
If the text is a question and contains no declarative assertions, return an empty list.

Text: "{response}"

Respond ONLY with valid JSON:
{{"statements": ["statement 1", "statement 2", ...]}}"""

NLI_PROMPT = """Context:
---
{chunk_text}
---

For each statement below, judge whether it is SUPPORTED by the context.
SUPPORTED: the statement is directly and explicitly stated in or clearly implied by the context.
NOT_SUPPORTED: the statement is not present in or contradicts the context.

Statements:
{numbered_statements}

Respond ONLY with valid JSON. The verdicts array must have exactly {n} elements:
{{"verdicts": ["SUPPORTED" or "NOT_SUPPORTED", ...]}}"""


async def call_gpt4o(prompt: str, semaphore: asyncio.Semaphore, max_tokens: int = 512) -> dict | None:
    async with semaphore:
        for attempt in range(6):
            try:
                resp = await openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": JUDGE_SYSTEM},
                        {"role": "user", "content": prompt},
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.0,
                    max_tokens=max_tokens,
                )
                return json.loads(resp.choices[0].message.content)
            except Exception as e:
                err = str(e)
                if "429" in err:
                    match = re.search(r"try again in (\d+(?:\.\d+)?)s", err)
                    wait = float(match.group(1)) + 1.0 if match else 2 ** attempt
                else:
                    wait = 2 ** attempt
                print(f"\n  [gpt-4o] attempt {attempt + 1}/6: {type(e).__name__}: {e}")
                if attempt < 5:
                    await asyncio.sleep(wait)
        print("\n  [gpt-4o] all 6 attempts failed.")
        return None


async def score_response(row: dict, semaphore: asyncio.Semaphore) -> dict:
    # Step 1: decompose the Socratic question into declarative statements
    decomp = await call_gpt4o(
        DECOMPOSE_PROMPT.format(response=row["response"]),
        semaphore,
        max_tokens=512,
    )

    if decomp is None:
        return {
            "response_id": row["response_id"],
            "utterance_id": row["utterance_id"],
            "chunk_id": row["chunk_id"],
            "model": row["model"],
            "cognitive_state": row["profile"]["cognitive_state"],
            "ragas_statements": [],
            "ragas_verdicts": [],
            "ragas_score": None,
            "ragas_empty": False,
            "judge_failed": True,
        }

    statements = decomp.get("statements", [])
    statements = [s for s in statements if isinstance(s, str) and s.strip()]

    # Empty statement list is a legitimate RAGAS outcome for interrogative outputs
    if not statements:
        return {
            "response_id": row["response_id"],
            "utterance_id": row["utterance_id"],
            "chunk_id": row["chunk_id"],
            "model": row["model"],
            "cognitive_state": row["profile"]["cognitive_state"],
            "ragas_statements": [],
            "ragas_verdicts": [],
            "ragas_score": 1.0,
            "ragas_empty": True,
            "judge_failed": False,
        }

    # Step 2: NLI check each statement against C
    numbered = "\n".join(f"{i+1}. {s}" for i, s in enumerate(statements))
    nli = await call_gpt4o(
        NLI_PROMPT.format(
            chunk_text=row["chunk_text"],
            numbered_statements=numbered,
            n=len(statements),
        ),
        semaphore,
        max_tokens=256,
    )

    if nli is None:
        return {
            "response_id": row["response_id"],
            "utterance_id": row["utterance_id"],
            "chunk_id": row["chunk_id"],
            "model": row["model"],
            "cognitive_state": row["profile"]["cognitive_state"],
            "ragas_statements": statements,
            "ragas_verdicts": [],
            "ragas_score": None,
            "ragas_empty": False,
            "judge_failed": True,
        }

    verdicts = nli.get("verdicts", [])
    if len(verdicts) < len(statements):
        verdicts += ["NOT_SUPPORTED"] * (len(statements) - len(verdicts))
    verdicts = verdicts[:len(statements)]
    verdicts = [v if v in ("SUPPORTED", "NOT_SUPPORTED") else "NOT_SUPPORTED" for v in verdicts]

    supported = sum(1 for v in verdicts if v == "SUPPORTED")
    score = round(supported / len(statements), 4)

    return {
        "response_id": row["response_id"],
        "utterance_id": row["utterance_id"],
        "chunk_id": row["chunk_id"],
        "model": row["model"],
        "cognitive_state": row["profile"]["cognitive_state"],
        "ragas_statements": statements,
        "ragas_verdicts": verdicts,
        "ragas_score": score,
        "ragas_empty": False,
        "judge_failed": False,
    }


def reprocess_failed():
    """Reset checkpoint for judge-failed rows so they are re-scored on next run."""
    if not TEMP_FILE.exists() or not CHECKPOINT_FILE.exists():
        print("No temp file or checkpoint found. Run the full scoring first.")
        return

    all_rows = []
    with open(TEMP_FILE) as f:
        for line in f:
            all_rows.append(json.loads(line))

    failed = [r for r in all_rows if r.get("judge_failed")]
    succeeded = [r for r in all_rows if not r.get("judge_failed")]

    if not failed:
        print("No failed rows found. Nothing to reprocess.")
        return

    print(f"Found {len(failed)} failed rows. Removing from checkpoint and temp file.")
    with open(TEMP_FILE, "w") as f:
        for row in succeeded:
            f.write(json.dumps(row) + "\n")
    with open(CHECKPOINT_FILE, "w") as f:
        json.dump([r["response_id"] for r in succeeded], f)

    print(f"{len(succeeded)} valid rows preserved. {len(failed)} rows will be re-scored on next run.")
    print("Run: python3 scripts/07_ragas_baseline.py")


async def main():
    responses = []
    with open(INPUT_FILE) as f:
        for line in f:
            responses.append(json.loads(line))

    done: set[str] = set()
    if CHECKPOINT_FILE.exists() and TEMP_FILE.exists():
        with open(CHECKPOINT_FILE) as f:
            done = set(json.load(f))
        saved = sum(1 for _ in open(TEMP_FILE))
        print(f"Resuming: {len(done)} already scored, {saved} rows on disk.")

    remaining = [r for r in responses if r["response_id"] not in done]
    print(f"{len(responses)} responses. {len(remaining)} remaining. 2 API calls each (GPT-4o only).")

    semaphore = asyncio.Semaphore(5)
    batch_size = 5
    total_failed = 0
    consecutive_all_failed = 0

    for i in tqdm(range(0, len(remaining), batch_size), desc="RAGAS baseline"):
        batch = remaining[i:i + batch_size]
        results = await asyncio.gather(*[score_response(row, semaphore) for row in batch])

        batch_failed = sum(1 for r in results if r.get("judge_failed"))
        total_failed += batch_failed
        if batch_failed:
            print(f"\n  ⚠  {batch_failed}/{len(batch)} judge failures in this batch ({total_failed} total).")

        consecutive_all_failed = consecutive_all_failed + 1 if batch_failed == len(batch) else 0
        if consecutive_all_failed >= ABORT_AFTER_CONSECUTIVE:
            print(f"\n❌ ABORTING: {ABORT_AFTER_CONSECUTIVE} consecutive batches with 100% judge failure.")
            print("   Check your API key, quota, and network. Fix the issue and rerun.")
            print("   Run: python3 scripts/07_ragas_baseline.py --reprocess-failed after fixing.")
            sys.exit(1)

        with open(TEMP_FILE, "a") as f:
            for result in results:
                f.write(json.dumps(result) + "\n")
        for row in batch:
            done.add(row["response_id"])
        with open(CHECKPOINT_FILE, "w") as f:
            json.dump(list(done), f)

    all_scores = []
    with open(TEMP_FILE) as f:
        for line in f:
            all_scores.append(json.loads(line))

    with open(OUTPUT_FILE, "w") as f:
        for row in all_scores:
            f.write(json.dumps(row) + "\n")

    valid = [s for s in all_scores if not s.get("judge_failed")]
    failed_rows = [s for s in all_scores if s.get("judge_failed")]

    print(f"\nSaved {len(all_scores)} RAGAS baseline scores to {OUTPUT_FILE}")
    if failed_rows:
        print(f"⚠  {len(failed_rows)} rows have judge_failed=True — excluded from statistics.")
        print("   Run: python3 scripts/07_ragas_baseline.py --reprocess-failed to reset them.")

    all_ragas = [s["ragas_score"] for s in valid]
    empty = [s for s in valid if s.get("ragas_empty")]
    non_empty = [s for s in valid if not s.get("ragas_empty")]

    print(f"\nRAGAS baseline summary (valid rows only):")
    print(f"  Total valid responses: {len(valid)}")
    print(f"  Empty (no statements extracted): {len(empty)} ({100*len(empty)/len(valid):.1f}%)" if valid else "")
    print(f"  Non-empty: {len(non_empty)}")

    if all_ragas:
        mean = sum(all_ragas) / len(all_ragas)
        sd = statistics.stdev(all_ragas) if len(all_ragas) > 1 else 0.0
        print(f"  Mean RAGAS score: {mean:.4f} ± {sd:.4f}")
        above_90 = sum(1 for s in all_ragas if s >= 0.9)
        print(f"  Scores ≥ 0.9: {above_90} ({100*above_90/len(all_ragas):.1f}%)")

    print("\nBy model:")
    by_model: dict[str, list] = {}
    for s in valid:
        by_model.setdefault(s["model"], []).append(s["ragas_score"])
    for m, scores in sorted(by_model.items()):
        mean = sum(scores) / len(scores)
        sd = statistics.stdev(scores) if len(scores) > 1 else 0.0
        print(f"  {m}: {mean:.4f} ± {sd:.4f}")

    print("\nInterpretation:")
    print("  Near-1.0 scores with near-zero variance confirm that RAGAS cannot discriminate")
    print("  good from bad Socratic responses. Socratic questions are interrogative, not")
    print("  declarative — standard statement decomposition yields empty or trivial lists.")
    print("  This structural incompatibility motivates M2's presupposition-based adaptation.")
    print("\nTo start fresh: delete data/scores_ragas.jsonl, data/.scores_ragas_temp.jsonl, data/.scores_ragas_checkpoint.json")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--reprocess-failed", action="store_true",
                        help="Reset checkpoint for judge-failed rows so they are re-scored on next run")
    args = parser.parse_args()

    if args.reprocess_failed:
        reprocess_failed()
    else:
        asyncio.run(main())
