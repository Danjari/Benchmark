"""
Script 05: Metric 2 — Retrieval Faithfulness
Input:  data/responses.jsonl
Output: data/scores_m2.jsonl

Two-step pipeline — novel adaptation of FActScore (Min et al., EMNLP 2023)
to interrogative (non-declarative) outputs:

  Step 1: LLM extracts declarative presuppositions from the Socratic question.
           A presupposition is a factual claim the question assumes to be true.
  Step 2: Each presupposition is checked for entailment against C.
  Score:  fraction of presuppositions entailed by C.
           Vacuous responses (no presuppositions) score 1.0 and are flagged.

Cross-judge protocol: same as M1.

Human spot-check (CRITICAL — required before reporting M2):
  After running, sample 40 rows stratified by model and cognitive_state.
  For each sampled row, print m2_presuppositions and m2_verdicts.
  Have a professor verify whether the presuppositions are correct and
  whether the entailment verdicts match their judgment.
  Compute Cohen's κ and report in the paper.
  Export helper: python3 scripts/05_metric2.py --spot-check 40
"""

import os
import re
import json
import asyncio
import argparse
import random
from pathlib import Path
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
anthropic_client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

INPUT_FILE = Path("data/responses.jsonl")
OUTPUT_FILE = Path("data/scores_m2.jsonl")
CHECKPOINT_FILE = Path("data/.scores_m2_checkpoint.json")
TEMP_FILE = Path("data/.scores_m2_temp.jsonl")
SPOT_CHECK_FILE = Path("data/m2_spot_check.jsonl")

JUDGE_SYSTEM = (
    "You are a strict dataset quality evaluator for an AI tutoring benchmark. "
    "Respond ONLY with valid JSON. No preamble, no markdown."
)

EXTRACTION_PROMPT = """A Socratic tutor responded to a student with this question:
"{response}"

Extract every factual claim this question presupposes as a list of declarative sentences.
A presupposition is a specific, falsifiable factual claim that must be true for the question to make sense.

Good presuppositions (specific and falsifiable):
  Q: "What does it mean when m and n are different?" → ["m and n can take different values", "the relationship between m and n affects the result"]
  Q: "What happens to the gradient when the learning rate exceeds a threshold?" → ["gradients change based on learning rate", "there exists a threshold for the learning rate"]

NOT presuppositions (too vague or trivially true):
  Q: "What do you think?" → [] (no specific claim)
  Q: "Can you explain that?" → [] (no content)
  "There is a concept being discussed" → too trivially true to count

Rules:
- Only extract specific, content-bearing presuppositions tied to the subject matter
- Do NOT include the question itself restated as a declarative sentence
- Return an empty list if the question is too generic to extract meaningful presuppositions

Respond ONLY with valid JSON:
{{"presuppositions": ["claim 1", "claim 2", ...]}}"""

ENTAILMENT_PROMPT = """Context C (the tutor's only permitted knowledge source):
---
{chunk_text}
---

For each presupposition below, judge whether it is ENTAILED by C.
ENTAILED: the claim is directly and explicitly supported by what C states.
NOT_ENTAILED: the claim introduces knowledge not present in C, goes beyond what C says, or contradicts C.

Be strict: if C implies a claim only loosely or through inference, mark it NOT_ENTAILED.

Presuppositions:
{numbered_presuppositions}

Respond ONLY with valid JSON. The verdicts array must have exactly {n} elements:
{{"verdicts": ["ENTAILED" or "NOT_ENTAILED", ...]}}"""


def get_judge_model(evaluated_model: str) -> str:
    return "claude-sonnet-4-6" if evaluated_model == "gpt-4o" else "gpt-4o"


async def call_openai_judge(prompt: str, semaphore: asyncio.Semaphore, max_tokens: int = 512) -> dict | None:
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
                    await asyncio.sleep(wait)
                else:
                    print(f"  [openai judge] {e}")
                    return None
    return None


async def call_anthropic_judge(prompt: str, semaphore: asyncio.Semaphore, max_tokens: int = 512) -> dict | None:
    async with semaphore:
        for attempt in range(6):
            try:
                resp = await anthropic_client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=max_tokens,
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


async def call_judge(prompt: str, judge_model: str, semaphore: asyncio.Semaphore, max_tokens: int = 512) -> dict | None:
    if judge_model == "gpt-4o":
        return await call_openai_judge(prompt, semaphore, max_tokens)
    return await call_anthropic_judge(prompt, semaphore, max_tokens)


async def score_response(row: dict, semaphore: asyncio.Semaphore) -> dict:
    judge_model = get_judge_model(row["model"])

    # Step 1: extract presuppositions
    extraction = await call_judge(
        EXTRACTION_PROMPT.format(response=row["response"]),
        judge_model,
        semaphore,
        max_tokens=512,
    )
    presuppositions = extraction.get("presuppositions", []) if extraction else []
    presuppositions = [p for p in presuppositions if isinstance(p, str) and p.strip()]

    if not presuppositions:
        return {
            "response_id": row["response_id"],
            "utterance_id": row["utterance_id"],
            "chunk_id": row["chunk_id"],
            "model": row["model"],
            "cognitive_state": row["profile"]["cognitive_state"],
            "judge_model": judge_model,
            "m2_presuppositions": [],
            "m2_verdicts": [],
            "m2_score": 1.0,
            "m2_vacuous": True,
        }

    # Step 2: entailment check
    numbered = "\n".join(f"{i+1}. {p}" for i, p in enumerate(presuppositions))
    entailment = await call_judge(
        ENTAILMENT_PROMPT.format(
            chunk_text=row["chunk_text"],
            numbered_presuppositions=numbered,
            n=len(presuppositions),
        ),
        judge_model,
        semaphore,
        max_tokens=256,
    )
    verdicts = entailment.get("verdicts", []) if entailment else []

    # Align lengths if LLM returned wrong count
    if len(verdicts) < len(presuppositions):
        verdicts += ["NOT_ENTAILED"] * (len(presuppositions) - len(verdicts))
    verdicts = verdicts[:len(presuppositions)]
    verdicts = [v if v in ("ENTAILED", "NOT_ENTAILED") else "NOT_ENTAILED" for v in verdicts]

    entailed = sum(1 for v in verdicts if v == "ENTAILED")
    score = round(entailed / len(presuppositions), 4)

    return {
        "response_id": row["response_id"],
        "utterance_id": row["utterance_id"],
        "chunk_id": row["chunk_id"],
        "model": row["model"],
        "cognitive_state": row["profile"]["cognitive_state"],
        "judge_model": judge_model,
        "m2_presuppositions": presuppositions,
        "m2_verdicts": verdicts,
        "m2_score": score,
        "m2_vacuous": False,
    }


def export_spot_check(n: int = 40):
    """Export a stratified sample for professor spot-check."""
    if not OUTPUT_FILE.exists():
        print("Run the full scoring first, then export spot-check.")
        return

    scores = []
    with open(OUTPUT_FILE) as f:
        for line in f:
            scores.append(json.loads(line))

    # Stratify by model and cognitive_state
    from collections import defaultdict
    buckets: dict = defaultdict(list)
    for s in scores:
        key = (s["model"], s["cognitive_state"])
        buckets[key].append(s)

    sample = []
    per_bucket = max(1, n // len(buckets))
    for key, rows in buckets.items():
        non_vacuous = [r for r in rows if not r.get("m2_vacuous")]
        pool = non_vacuous if non_vacuous else rows
        sample.extend(random.sample(pool, min(per_bucket, len(pool))))

    with open(SPOT_CHECK_FILE, "w") as f:
        for row in sample[:n]:
            f.write(json.dumps(row) + "\n")

    print(f"Exported {min(len(sample), n)} rows to {SPOT_CHECK_FILE}")
    print("Send this file to professor for verification of presuppositions and verdicts.")
    print("For each row, professor should judge: are the presuppositions correct? Are the verdicts correct?")


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
    print(f"{len(responses)} responses. {len(remaining)} remaining. 2 API calls each.")

    semaphore = asyncio.Semaphore(5)
    batch_size = 5

    for i in tqdm(range(0, len(remaining), batch_size), desc="M2 scoring"):
        batch = remaining[i:i + batch_size]
        results = await asyncio.gather(*[score_response(row, semaphore) for row in batch])
        with open(TEMP_FILE, "a") as f:
            for result in results:
                f.write(json.dumps(result) + "\n")
        for row, result in zip(batch, results):
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

    print(f"\nSaved {len(all_scores)} M2 scores to {OUTPUT_FILE}")

    import statistics
    by_model: dict[str, list] = {}
    vacuous = [s for s in all_scores if s.get("m2_vacuous")]
    for s in all_scores:
        by_model.setdefault(s["model"], []).append(s["m2_score"])

    print("\nM2 mean score by model:")
    for m, scores in sorted(by_model.items()):
        mean = sum(scores) / len(scores)
        sd = statistics.stdev(scores) if len(scores) > 1 else 0.0
        print(f"  {m}: {mean:.3f} ± {sd:.3f}")

    print(f"\nVacuous responses (no presuppositions, score=1.0): {len(vacuous)} ({100*len(vacuous)/len(all_scores):.1f}%)")

    not_entailed = [s for s in all_scores if not s.get("m2_vacuous") and s["m2_score"] < 1.0]
    print(f"Responses with ≥1 unentailed presupposition: {len(not_entailed)} ({100*len(not_entailed)/len(all_scores):.1f}%)")

    print("\n⚠  Human spot-check required before reporting M2.")
    print("   Run: python3 scripts/05_metric2.py --spot-check 40")
    print("   Send data/m2_spot_check.jsonl to professor for verification.")
    print("\nTo start fresh: delete data/scores_m2.jsonl, data/.scores_m2_temp.jsonl, data/.scores_m2_checkpoint.json")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--spot-check", type=int, metavar="N", help="Export N rows for human spot-check")
    args = parser.parse_args()

    if args.spot_check:
        export_spot_check(args.spot_check)
    else:
        asyncio.run(main())
