"""
Script 02: Dean Validation
Input:  data/utterances_raw.jsonl
Output: data/utterances.jsonl  (validated only)

The Dean validates each (P, U) pair against 4 criteria:
  1. STATE MATCH:      utterance authentically expresses the claimed cognitive state
  2. DERIVABILITY:     utterance is derivable ONLY from concepts in C
  3. PLAUSIBILITY:     a real university student could plausibly say this
  4. CONCEPT PRESENCE: the target concept is explicitly present in C

For erroneous utterances, the Dean also checks a 5th criterion:
  5. MISCONCEPTION MATCH: the utterance expresses the specific misconception
                          stated in P, not a generic or unrelated error

After individual validation, a contrastive pair check verifies that the
accurate and erroneous utterances for each chunk target the same concept.
Pairs where one sibling was rejected are flagged so both can be regenerated.
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

INPUT_FILE = Path("data/utterances_raw.jsonl")
OUTPUT_FILE = Path("data/utterances.jsonl")
REJECTED_FILE = Path("data/utterances_rejected.jsonl")  # saved for acceptance-rate reporting in paper

# ── Dean prompts ───────────────────────────────────────────────────────────────

DEAN_PROMPT_BASE = """You are the Dean agent in a benchmark dataset curation pipeline for AI tutoring evaluation.

Validate whether this simulated student utterance meets ALL required criteria.

Context C (the ONLY permitted knowledge source):
---
{chunk_text}
---

Student Profile P:
  Cognitive state:       {cognitive_state}
  Target concept:        {target_concept}
  Correct understanding: {correct_understanding}

Student utterance U:
"{utterance}"

Validate against ALL 4 criteria:
1. STATE MATCH: Does U authentically express the claimed cognitive state ({cognitive_state})?
   - accurate:      demonstrates correct understanding of {target_concept}
   - comprehension: explicitly states understanding ("I think I understand now...", "So what you're saying is...")
   - confusion:     explicitly states uncertainty ("I'm confused about...", "I don't understand why...")
2. DERIVABILITY: Is U derivable ONLY from concepts in C? No outside knowledge required.
3. PLAUSIBILITY: Could a real university student plausibly say this?
4. CONCEPT PRESENCE: Is "{target_concept}" explicitly present in C?

Respond ONLY with valid JSON:
{{
  "accept": true or false,
  "criteria": {{
    "state_match": true or false,
    "derivability": true or false,
    "plausibility": true or false,
    "concept_presence": true or false
  }},
  "reason": "one sentence if rejecting, empty string if accepting"
}}"""

DEAN_PROMPT_ERRONEOUS = """You are the Dean agent in a benchmark dataset curation pipeline for AI tutoring evaluation.

Validate whether this simulated erroneous student utterance meets ALL required criteria.

Context C (the ONLY permitted knowledge source):
---
{chunk_text}
---

Student Profile P:
  Cognitive state:       erroneous
  Target concept:        {target_concept}
  Correct understanding: {correct_understanding}
  Expected misconception (derived from C): {misconception}

Student utterance U:
"{utterance}"

Validate against ALL 5 criteria:
1. STATE MATCH: Does U express a specific, plausible wrong belief (not confusion or correct understanding)?
2. DERIVABILITY: Is U derivable ONLY from concepts in C? The misconception must arise from misreading C, not from outside knowledge.
3. PLAUSIBILITY: Could a real university student plausibly say this?
4. CONCEPT PRESENCE: Is "{target_concept}" explicitly present in C?
5. MISCONCEPTION MATCH: Does U express specifically the misconception "{misconception}"? A generic or unrelated error fails this criterion.

Respond ONLY with valid JSON:
{{
  "accept": true or false,
  "criteria": {{
    "state_match": true or false,
    "derivability": true or false,
    "plausibility": true or false,
    "concept_presence": true or false,
    "misconception_match": true or false
  }},
  "reason": "one sentence if rejecting, empty string if accepting"
}}"""


# ── Validation ─────────────────────────────────────────────────────────────────

async def validate(utterance: dict, semaphore: asyncio.Semaphore) -> dict:
    async with semaphore:
        profile = utterance.get("profile", {})
        cognitive_state = profile.get("cognitive_state", "")
        target_concept = profile.get("target_concept", "")
        correct_understanding = profile.get("correct_understanding", "")
        misconception = profile.get("misconception", "")

        if cognitive_state == "erroneous":
            prompt = DEAN_PROMPT_ERRONEOUS.format(
                chunk_text=utterance["chunk_text"],
                utterance=utterance["utterance"],
                target_concept=target_concept,
                correct_understanding=correct_understanding,
                misconception=misconception,
            )
        else:
            prompt = DEAN_PROMPT_BASE.format(
                chunk_text=utterance["chunk_text"],
                utterance=utterance["utterance"],
                cognitive_state=cognitive_state,
                target_concept=target_concept,
                correct_understanding=correct_understanding,
            )

        try:
            response = await client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.0,
            )
            result = json.loads(response.choices[0].message.content)
            utterance["dean_validated"] = result.get("accept", False)
            utterance["dean_result"] = result
            return utterance
        except Exception as e:
            print(f"Dean error on {utterance['utterance_id']}: {e}")
            utterance["dean_validated"] = False
            utterance["dean_result"] = {"accept": False, "reason": str(e)}
            return utterance


def check_contrastive_pairs(utterances: list[dict]) -> set[str]:
    """
    Flag chunk_ids where contrastive pair integrity is broken.
    Checks both pair types:
      - accurate/erroneous: one sibling rejected, or targeting different concepts
      - comprehension/confusion: one sibling rejected, or targeting different concepts
    Returns a set of chunk_ids with broken pairs.
    """
    by_chunk: dict[str, dict] = {}
    for u in utterances:
        chunk_id = u["chunk_id"]
        state = u["profile"]["cognitive_state"]
        if chunk_id not in by_chunk:
            by_chunk[chunk_id] = {}
        by_chunk[chunk_id][state] = u

    broken = set()
    for chunk_id, states in by_chunk.items():
        for a_state, b_state in [("accurate", "erroneous"), ("comprehension", "confusion")]:
            a = states.get(a_state)
            b = states.get(b_state)
            if not a or not b:
                continue
            # broken if one sibling accepted and the other rejected
            if a["dean_validated"] != b["dean_validated"]:
                broken.add(chunk_id)
            # broken if siblings target different concepts
            if a["profile"]["target_concept"] != b["profile"]["target_concept"]:
                broken.add(chunk_id)
    return broken


# ── Main ───────────────────────────────────────────────────────────────────────

async def main():
    utterances = []
    with open(INPUT_FILE) as f:
        for line in f:
            utterances.append(json.loads(line))

    print(f"Validating {len(utterances)} utterances with Dean agent...")

    semaphore = asyncio.Semaphore(5)
    tasks = [validate(u, semaphore) for u in utterances]
    results = await tqdm.gather(*tasks, desc="Dean validation")

    accepted = [u for u in results if u["dean_validated"]]
    rejected = [u for u in results if not u["dean_validated"]]

    # Contrastive pair integrity check
    broken_pairs = check_contrastive_pairs(results)
    if broken_pairs:
        print(f"\nBroken contrastive pairs (accurate/erroneous mismatch): {len(broken_pairs)} chunk(s)")
        for chunk_id in broken_pairs:
            print(f"  chunk_id: {chunk_id}")
        # Exclude both siblings of broken pairs from output
        accepted = [u for u in accepted if u["chunk_id"] not in broken_pairs]
        print(f"  Excluded from output — regenerate these chunk_ids with script 01.")

    print(f"\nAccepted: {len(accepted)} / {len(utterances)}")
    print(f"Rejected (individual): {len(rejected)}")
    if broken_pairs:
        print(f"Excluded (broken pairs): {len(broken_pairs) * 2} utterances across {len(broken_pairs)} chunks")

    if rejected:
        print("\nRejection reasons (first 10):")
        for u in rejected[:10]:
            state = u["profile"]["cognitive_state"]
            print(f"  [{state}] {u['utterance_id']}: {u['dean_result'].get('reason', '')}")

    with open(OUTPUT_FILE, "w") as f:
        for u in accepted:
            f.write(json.dumps(u) + "\n")

    # Save all rejected utterances for acceptance-rate analysis in the paper
    all_rejected = rejected + [
        u for u in results
        if u["dean_validated"] and u["chunk_id"] in broken_pairs
    ]
    with open(REJECTED_FILE, "w") as f:
        for u in all_rejected:
            f.write(json.dumps(u) + "\n")

    print(f"\nSaved {len(accepted)} validated utterances to {OUTPUT_FILE}")
    print(f"Saved {len(all_rejected)} rejected utterances to {REJECTED_FILE}")

    if rejected or broken_pairs:
        print("\nTo regenerate failed chunks, re-run script 01 targeting the failed chunk_ids.")

    # Acceptance rate by cognitive state (needed for paper reporting)
    from collections import Counter
    state_total: Counter = Counter()
    state_accepted: Counter = Counter()
    for u in results:
        s = u["profile"]["cognitive_state"]
        state_total[s] += 1
        if u["dean_validated"] and u["chunk_id"] not in broken_pairs:
            state_accepted[s] += 1
    print("\nAcceptance rate by cognitive state:")
    for s in ("accurate", "erroneous", "comprehension", "confusion"):
        total = state_total[s]
        acc = state_accepted[s]
        pct = f"{100 * acc / total:.0f}%" if total else "n/a"
        print(f"  {s:15s}: {acc}/{total} ({pct})")


if __name__ == "__main__":
    asyncio.run(main())
