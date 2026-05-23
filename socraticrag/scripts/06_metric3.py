"""
Script 06: Metric 3 — Pedagogical Alignment
Input:  data/responses.jsonl
Output: data/scores_m3.jsonl

Three-phase GuideEval rubric from Discerning Minds (Liu et al. 2025):
  Perception  (0–3): did the tutor correctly infer the student's cognitive state?
  Orchestration (0–3): did the tutor select an appropriate pedagogical strategy?
  Elicitation (0–3): did the question target the right Bloom's taxonomy level?

Receives (C, U, P, R) — P is the ground-truth profile annotation metadata
withheld from evaluated models during generation (script 03).

Cross-judge protocol: same as M1/M2.

Human spot-check (REQUIRED before reporting M3):
  Sample 20–30 responses across models and cognitive states.
  Have a professor score each on the GuideEval rubric independently.
  Compute Spearman ρ between professor scores and automated M3 scores.
  Target: ρ > 0.7. Report in paper.
  Export helper: python3 scripts/06_metric3.py --spot-check 30
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
OUTPUT_FILE = Path("data/scores_m3.jsonl")
CHECKPOINT_FILE = Path("data/.scores_m3_checkpoint.json")
TEMP_FILE = Path("data/.scores_m3_temp.jsonl")
SPOT_CHECK_FILE = Path("data/m3_spot_check.jsonl")

JUDGE_SYSTEM = (
    "You are a strict dataset quality evaluator for an AI tutoring benchmark. "
    "Respond ONLY with valid JSON. No preamble, no markdown."
)

JUDGE_PROMPT = """You are evaluating a Socratic tutor response using the GuideEval rubric (Discerning Minds framework).

=== CONTEXT C (the tutor's only permitted knowledge source) ===
{chunk_text}

=== GROUND-TRUTH STUDENT PROFILE P (annotation metadata — NOT given to the tutor) ===
Cognitive state: {cognitive_state}
Target concept: {target_concept}
Correct understanding: {correct_understanding}
Misconception (if any): {misconception}

=== STUDENT UTTERANCE U ===
{utterance}

=== TUTOR RESPONSE R (what you are evaluating) ===
{response}

=== SCORING RUBRIC ===

Score each phase from 0 to 3 using the anchors below.

--- PERCEPTION: Did the tutor correctly infer the student's cognitive state? ---
3 — The response clearly targets the student's specific cognitive state (accurate / erroneous / comprehension / confusion) and reflects the precise misconception or gap described in P.
2 — The response broadly matches the cognitive state but misses the specific misconception or targets a related but different concept.
1 — The response partially addresses the student's state; it could apply to multiple states and shows limited tailoring.
0 — The response is generic: it would fit any student regardless of state, or it misdiagnoses the student's state entirely.

--- ORCHESTRATION: Did the tutor select an appropriate pedagogical strategy for this state? ---
State-specific expectations:
  accurate → strategy should deepen or challenge (e.g., ask about edge cases, connections to other concepts, or higher-order implications)
  erroneous → strategy should surface and gently destabilise the misconception without stating the correction directly
  comprehension → strategy should probe depth of understanding (e.g., ask the student to apply or derive, not just recall)
  confusion → strategy should scaffold back to a simpler, grounded premise in C before advancing

3 — The question enacts the ideal strategy for this state: it would materially help this student, given their cognitive state, move toward understanding.
2 — The strategy is appropriate in direction but either too aggressive (jumps ahead of the student's state) or too conservative (stays at a lower level than needed).
1 — The strategy is marginally appropriate but generic; a different strategy would serve this student better.
0 — The strategy is mismatched: it would confuse a confused student further, confirm a misconception, or be irrelevant to an accurate student.

--- ELICITATION: Does the question target the correct Bloom's taxonomy level for this state? ---
Bloom's levels — L1 Remember, L2 Understand, L3 Apply, L4 Analyze, L5 Evaluate, L6 Create

State-specific expected levels:
  accurate       → L4–L6 (Analyze / Evaluate / Create): student has accurate knowledge; push beyond recall
  erroneous      → L1–L2 (Remember / Understand): bring student back to what C actually says before building up
  comprehension  → L3–L4 (Apply / Analyze): student understands; check whether they can use the knowledge
  confusion      → L1–L2 (Remember / Understand): scaffold — re-anchor to the simplest correct claim in C

3 — The question targets exactly the right Bloom's level for the student's state; the cognitive demand matches what this student needs next.
2 — One level off from ideal (e.g., L3 when L4 is ideal, or L2 when L1 is ideal); still reasonable but not optimal.
1 — Two or more levels off, but the question is still coherent and Socratic in form.
0 — The Bloom's level is completely mismatched (e.g., L6 creation task for a confused student, or pure recall for an accurate student who needs challenge).

=== OUTPUT ===
Respond ONLY with valid JSON (integers 0–3 for each score):
{{
  "perception": <0-3>,
  "orchestration": <0-3>,
  "elicitation": <0-3>,
  "reasoning": "<one sentence explaining the most important strength or weakness across all three dimensions>"
}}"""


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
                    max_tokens=256,
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


def clamp_score(v, key: str) -> int:
    try:
        return max(0, min(3, int(v)))
    except (TypeError, ValueError):
        return 0


async def score_response(row: dict, semaphore: asyncio.Semaphore) -> dict:
    judge_model = get_judge_model(row["model"])
    profile = row["profile"]

    prompt = JUDGE_PROMPT.format(
        chunk_text=row["chunk_text"],
        cognitive_state=profile.get("cognitive_state", ""),
        target_concept=profile.get("target_concept", ""),
        correct_understanding=profile.get("correct_understanding", ""),
        misconception=profile.get("misconception", "none"),
        utterance=row["utterance"],
        response=row["response"],
    )

    result = await call_judge(prompt, judge_model, semaphore)

    if result:
        perception = clamp_score(result.get("perception"), "perception")
        orchestration = clamp_score(result.get("orchestration"), "orchestration")
        elicitation = clamp_score(result.get("elicitation"), "elicitation")
        reasoning = result.get("reasoning", "")
    else:
        perception = orchestration = elicitation = 0
        reasoning = "judge error"

    return {
        "response_id": row["response_id"],
        "utterance_id": row["utterance_id"],
        "chunk_id": row["chunk_id"],
        "model": row["model"],
        "cognitive_state": profile.get("cognitive_state", ""),
        "judge_model": judge_model,
        "m3_perception": perception,
        "m3_orchestration": orchestration,
        "m3_elicitation": elicitation,
        "m3_total": perception + orchestration + elicitation,
        "m3_reasoning": reasoning,
    }


def export_spot_check(n: int = 30):
    """Export a stratified sample for professor spot-check."""
    if not OUTPUT_FILE.exists():
        print("Run the full scoring first, then export spot-check.")
        return

    scores = []
    with open(OUTPUT_FILE) as f:
        for line in f:
            scores.append(json.loads(line))

    # Load full response rows to include (C, U, P, R) for professor review
    responses: dict[str, dict] = {}
    if Path(INPUT_FILE).exists():
        with open(INPUT_FILE) as f:
            for line in f:
                r = json.loads(line)
                responses[r["response_id"]] = r

    from collections import defaultdict
    buckets: dict = defaultdict(list)
    for s in scores:
        key = (s["model"], s["cognitive_state"])
        buckets[key].append(s)

    sample = []
    per_bucket = max(1, n // len(buckets))
    for key, rows in buckets.items():
        sample.extend(random.sample(rows, min(per_bucket, len(rows))))

    with open(SPOT_CHECK_FILE, "w") as f:
        for row in sample[:n]:
            # Enrich with full response context so professor can see everything
            full = responses.get(row["response_id"], {})
            enriched = {**row}
            if full:
                enriched["chunk_text"] = full.get("chunk_text", "")
                enriched["utterance"] = full.get("utterance", "")
                enriched["response"] = full.get("response", "")
                enriched["profile"] = full.get("profile", {})
            f.write(json.dumps(enriched) + "\n")

    print(f"Exported {min(len(sample), n)} rows to {SPOT_CHECK_FILE}")
    print("For each row, professor should independently score Perception, Orchestration, Elicitation (0–3).")
    print("Compute Spearman ρ between professor scores and m3_* fields. Target: ρ > 0.7.")


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

    for row in tqdm(remaining, desc="M3 scoring"):
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

    print(f"\nSaved {len(all_scores)} M3 scores to {OUTPUT_FILE}")

    import statistics

    # Per-model totals
    by_model: dict[str, list] = {}
    for s in all_scores:
        by_model.setdefault(s["model"], []).append(s["m3_total"])

    print("\nM3 total score by model (max 9):")
    for m, totals in sorted(by_model.items()):
        mean = sum(totals) / len(totals)
        sd = statistics.stdev(totals) if len(totals) > 1 else 0.0
        print(f"  {m}: {mean:.3f} ± {sd:.3f}")

    # Per-dimension breakdown
    print("\nDimension breakdown (all models combined):")
    for dim in ("m3_perception", "m3_orchestration", "m3_elicitation"):
        vals = [s[dim] for s in all_scores]
        mean = sum(vals) / len(vals)
        sd = statistics.stdev(vals) if len(vals) > 1 else 0.0
        print(f"  {dim}: {mean:.3f} ± {sd:.3f}")

    # Per-cognitive-state breakdown
    print("\nM3 total by cognitive state (all models):")
    by_state: dict[str, list] = {}
    for s in all_scores:
        by_state.setdefault(s["cognitive_state"], []).append(s["m3_total"])
    for state, vals in sorted(by_state.items()):
        mean = sum(vals) / len(vals)
        sd = statistics.stdev(vals) if len(vals) > 1 else 0.0
        print(f"  {state}: {mean:.3f} ± {sd:.3f}")

    print("\n⚠  Human spot-check required before reporting M3.")
    print("   Run: python3 scripts/06_metric3.py --spot-check 30")
    print("   Send data/m3_spot_check.jsonl to professor for independent scoring.")
    print("   Compute Spearman ρ between professor scores and automated scores. Target: ρ > 0.7.")
    print("\nTo start fresh: delete data/scores_m3.jsonl, data/.scores_m3_temp.jsonl, data/.scores_m3_checkpoint.json")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--spot-check", type=int, metavar="N", help="Export N rows for human spot-check")
    args = parser.parse_args()

    if args.spot_check:
        export_spot_check(args.spot_check)
    else:
        asyncio.run(main())
