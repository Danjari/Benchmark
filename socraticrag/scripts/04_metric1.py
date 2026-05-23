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
"""

import os
import re
import json
import asyncio
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
                    await asyncio.sleep(wait)
                else:
                    print(f"  [openai judge] {e}")
                    return None
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
                if "429" in err or "rate_limit" in err or "overloaded" in err:
                    wait = 2 ** attempt
                    match = re.search(r"try again in (\d+(?:\.\d+)?)s", err)
                    if match:
                        wait = float(match.group(1)) + 1.0
                    await asyncio.sleep(wait)
                else:
                    print(f"  [anthropic judge] {e}")
                    return None
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

    verdict = result.get("verdict", "BORDERLINE") if result else "BORDERLINE"
    if verdict not in VERDICT_TO_SCORE:
        verdict = "BORDERLINE"
    reason = result.get("reason", "") if result else "judge error"

    return {
        "response_id": row["response_id"],
        "utterance_id": row["utterance_id"],
        "chunk_id": row["chunk_id"],
        "model": row["model"],
        "cognitive_state": row["profile"]["cognitive_state"],
        "judge_model": judge_model,
        "m1_verdict": verdict,
        "m1_score": VERDICT_TO_SCORE[verdict],
        "m1_reason": reason,
    }


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

    for row in tqdm(remaining, desc="M1 scoring"):
        result = await score_response(row, semaphore)
        with open(TEMP_FILE, "a") as f:
            f.write(json.dumps(result) + "\n")
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

    print(f"\nSaved {len(all_scores)} M1 scores to {OUTPUT_FILE}")

    by_model: dict[str, list] = {}
    by_verdict: dict[str, int] = {}
    for s in all_scores:
        by_model.setdefault(s["model"], []).append(s["m1_score"])
        by_verdict[s["m1_verdict"]] = by_verdict.get(s["m1_verdict"], 0) + 1

    print("\nM1 mean score by model:")
    for m, scores in sorted(by_model.items()):
        import statistics
        mean = sum(scores) / len(scores)
        sd = statistics.stdev(scores) if len(scores) > 1 else 0.0
        print(f"  {m}: {mean:.3f} ± {sd:.3f}")

    print("\nVerdict distribution:")
    for v in ["CLEARLY_WITHHELD", "BORDERLINE", "CLEARLY_LEAKED"]:
        count = by_verdict.get(v, 0)
        pct = 100 * count / len(all_scores)
        print(f"  {v}: {count} ({pct:.1f}%)")

    borderline = [s for s in all_scores if s["m1_verdict"] == "BORDERLINE"]
    print(f"\n⚠  {len(borderline)} BORDERLINE responses flagged for human review.")
    print("   Filter scores_m1.jsonl for m1_verdict=BORDERLINE and send to professor.")
    print("\nTo start fresh: delete data/scores_m1.jsonl, data/.scores_m1_temp.jsonl, data/.scores_m1_checkpoint.json")


if __name__ == "__main__":
    asyncio.run(main())
