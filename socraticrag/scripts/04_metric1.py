"""
Script 04: Metric 1 — Direct-Answer Leakage
Input:  data/responses.jsonl
Output: data/scores_m1.jsonl

Judges whether each model response withholds the answer (Socratic)
or reveals it directly. Adapted from EULER's reveal_answer criterion
(Bonino et al., 2024; Pearson r = 0.78 against human judgment).

Cross-judge protocol:
  gpt-4o responses         → Claude Sonnet 4.6 judges
  claude-sonnet-4-6        → GPT-4o judges
  gemini-2.0-flash         → GPT-4o judges

Verdict → score mapping:
  CLEARLY_WITHHELD → 1.0
  BORDERLINE       → 0.5
  CLEARLY_LEAKED   → 0.0

Human spot-check (REQUIRED before reporting):
  After running, filter scores_m1.jsonl for m1_verdict == "BORDERLINE".
  Have a professor rate each borderline case independently.
  Report agreement rate in the paper to validate M1 calibration.

Failure handling:
  All API errors are retried up to 6 times with exponential backoff.
  Rows where the judge fails all retries are written with judge_failed=True
  and excluded from statistics. Run --reprocess-failed to reset them.
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
from anthropic import AsyncAnthropic
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
anthropic_client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

INPUT_FILE = Path("data/responses.jsonl")
OUTPUT_FILE = Path("data/scores_m1.jsonl")
CHECKPOINT_FILE = Path("data/.scores_m1_checkpoint.json")
TEMP_FILE = Path("data/.scores_m1_temp.jsonl")

ABORT_AFTER_CONSECUTIVE = 3  # consecutive all-failed batches before aborting

VERDICT_TO_SCORE = {
    "CLEARLY_WITHHELD": 1.0,
    "BORDERLINE": 0.5,
    "CLEARLY_LEAKED": 0.0,
}

JUDGE_SYSTEM = (
    "You are a strict dataset quality evaluator for an AI tutoring benchmark. "
    "Respond ONLY with valid JSON. No preamble, no markdown."
)

JUDGE_PROMPT = """You are evaluating whether a Socratic tutor response reveals the correct answer or withholds it.

Context C (the tutor's only permitted knowledge source):
---
{chunk_text}
---

Student utterance: "{utterance}"

Tutor response: "{response}"

The tutor's role is to guide the student to discover the answer themselves through a question — never to state the correct understanding directly.

Classify the response as one of three verdicts:

CLEARLY_WITHHELD: the response is a pure guiding question. It gives the student nothing they could treat as an answer. The student must still reason independently.

BORDERLINE: the response asks a question but is so leading, or contains so strong a hint, that a student could extract the correct understanding without reasoning. Includes: rhetorical questions that imply their answer, responses that confirm or deny the student's claim before asking a follow-up, questions that restate the correct understanding as a premise.

CLEARLY_LEAKED: the response directly states the correct understanding of the concept, explains why the student is right or wrong, or summarises what C says about the concept in a way that resolves the student's question.

Respond ONLY with valid JSON:
{{"verdict": "CLEARLY_WITHHELD" or "BORDERLINE" or "CLEARLY_LEAKED", "reason": "one sentence"}}"""


def get_judge_model(evaluated_model: str) -> str:
    return "claude-sonnet-4-6" if evaluated_model == "gpt-4o" else "gpt-4o"


async def call_openai_judge(prompt: str, semaphore: asyncio.Semaphore) -> dict | None:
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
                )
                return json.loads(resp.choices[0].message.content)
            except Exception as e:
                err = str(e)
                if "429" in err:
                    match = re.search(r"try again in (\d+(?:\.\d+)?)s", err)
                    wait = float(match.group(1)) + 1.0 if match else 2 ** attempt
                else:
                    wait = 2 ** attempt
                print(f"\n  [openai judge] attempt {attempt + 1}/6: {type(e).__name__}: {e}")
                if attempt < 5:
                    await asyncio.sleep(wait)
        print("\n  [openai judge] all 6 attempts failed.")
        return None


async def call_anthropic_judge(prompt: str, semaphore: asyncio.Semaphore) -> dict | None:
    async with semaphore:
        for attempt in range(6):
            try:
                resp = await anthropic_client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=256,
                    system=JUDGE_SYSTEM,
                    messages=[{"role": "user", "content": prompt}],
                )
                raw = resp.content[0].text.strip()
                if raw.startswith("```"):
                    raw = raw[raw.index("{"):raw.rindex("}") + 1]
                return json.loads(raw)
            except Exception as e:
                err = str(e)
                wait = 2 ** attempt
                if "429" in err or "rate_limit" in err or "overloaded" in err:
                    match = re.search(r"try again in (\d+(?:\.\d+)?)s", err)
                    if match:
                        wait = float(match.group(1)) + 1.0
                print(f"\n  [anthropic judge] attempt {attempt + 1}/6: {type(e).__name__}: {e}")
                if attempt < 5:
                    await asyncio.sleep(wait)
        print("\n  [anthropic judge] all 6 attempts failed.")
        return None


async def call_judge(prompt: str, judge_model: str, semaphore: asyncio.Semaphore) -> dict | None:
    if judge_model == "gpt-4o":
        return await call_openai_judge(prompt, semaphore)
    return await call_anthropic_judge(prompt, semaphore)


async def score_response(row: dict, semaphore: asyncio.Semaphore) -> dict:
    judge_model = get_judge_model(row["model"])
    prompt = JUDGE_PROMPT.format(
        chunk_text=row["chunk_text"],
        utterance=row["utterance"],
        response=row["response"],
    )
    result = await call_judge(prompt, judge_model, semaphore)

    if result is None:
        return {
            "response_id": row["response_id"],
            "utterance_id": row["utterance_id"],
            "chunk_id": row["chunk_id"],
            "model": row["model"],
            "cognitive_state": row["profile"]["cognitive_state"],
            "judge_model": judge_model,
            "m1_verdict": "JUDGE_ERROR",
            "m1_score": None,
            "m1_reason": "judge error — all retries failed",
            "judge_failed": True,
        }

    verdict = result.get("verdict", "BORDERLINE")
    if verdict not in VERDICT_TO_SCORE:
        verdict = "BORDERLINE"

    return {
        "response_id": row["response_id"],
        "utterance_id": row["utterance_id"],
        "chunk_id": row["chunk_id"],
        "model": row["model"],
        "cognitive_state": row["profile"]["cognitive_state"],
        "judge_model": judge_model,
        "m1_verdict": verdict,
        "m1_score": VERDICT_TO_SCORE[verdict],
        "m1_reason": result.get("reason", ""),
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
    print("Run: python3 scripts/04_metric1.py")


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
    print(f"{len(responses)} responses. {len(remaining)} remaining. 1 API call each.")

    semaphore = asyncio.Semaphore(5)
    batch_size = 4
    total_failed = 0
    consecutive_all_failed = 0

    for i in tqdm(range(0, len(remaining), batch_size), desc="M1 scoring"):
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
            print("   Run: python3 scripts/04_metric1.py --reprocess-failed after fixing.")
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

    print(f"\nSaved {len(all_scores)} M1 scores to {OUTPUT_FILE}")
    if failed_rows:
        print(f"⚠  {len(failed_rows)} rows have judge_failed=True — excluded from statistics.")
        print("   Run: python3 scripts/04_metric1.py --reprocess-failed to reset them.")

    by_model: dict[str, list] = {}
    by_verdict: dict[str, int] = {}
    for s in valid:
        by_model.setdefault(s["model"], []).append(s["m1_score"])
        by_verdict[s["m1_verdict"]] = by_verdict.get(s["m1_verdict"], 0) + 1

    print("\nM1 mean score by model (valid rows only):")
    for m, scores in sorted(by_model.items()):
        mean = sum(scores) / len(scores)
        sd = statistics.stdev(scores) if len(scores) > 1 else 0.0
        print(f"  {m}: {mean:.3f} ± {sd:.3f}")

    print("\nVerdict distribution:")
    for v in ["CLEARLY_WITHHELD", "BORDERLINE", "CLEARLY_LEAKED"]:
        count = by_verdict.get(v, 0)
        pct = 100 * count / len(valid) if valid else 0.0
        print(f"  {v}: {count} ({pct:.1f}%)")

    borderline = [s for s in valid if s["m1_verdict"] == "BORDERLINE"]
    print(f"\n⚠  {len(borderline)} BORDERLINE responses flagged for human review.")
    print("   Filter scores_m1.jsonl for m1_verdict=BORDERLINE and send to professor.")
    print("\nTo start fresh: delete data/scores_m1.jsonl, data/.scores_m1_temp.jsonl, data/.scores_m1_checkpoint.json")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--reprocess-failed", action="store_true",
                        help="Reset checkpoint for judge-failed rows so they are re-scored on next run")
    args = parser.parse_args()

    if args.reprocess_failed:
        reprocess_failed()
    else:
        asyncio.run(main())
