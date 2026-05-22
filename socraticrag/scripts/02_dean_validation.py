"""
Script 02: Dean Validation
Input:  data/utterances_raw.jsonl
Output: data/utterances.jsonl  (validated only, rejects regenerated up to 3x)

The Dean agent checks each utterance against 4 criteria:
  1. Correct cognitive state expressed
  2. Derivable ONLY from concepts in C (no outside knowledge required)
  3. Pedagogically plausible (a real student could say this)
  4. RAG constraint: the target concept is explicitly present in C
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
MAX_RETRIES = 3

DEAN_PROMPT = """You are the Dean agent in a benchmark dataset curation pipeline for AI tutoring evaluation.

Your role: validate whether a simulated student utterance meets ALL of the following criteria.

Context C (the ONLY permitted knowledge source):
---
{chunk_text}
---

Student utterance:
"{utterance}"

Claimed cognitive state: {state}
Claimed target concept: {target_concept}

Validate against ALL 4 criteria:
1. STATE MATCH: Does the utterance authentically express the claimed cognitive state ({state})?
   - accurate: demonstrates correct understanding
   - erroneous: expresses a specific, plausible wrong belief
   - comprehension: explicitly states understanding
   - confusion: explicitly states uncertainty
2. DERIVABILITY: Is the utterance derivable ONLY from concepts in C? (No outside knowledge needed)
3. PLAUSIBILITY: Could a real university student plausibly say this?
4. CONCEPT PRESENCE: Is the target concept "{target_concept}" explicitly present in C?

Respond ONLY with valid JSON:
{{
  "accept": true or false,
  "criteria": {{
    "state_match": true or false,
    "derivability": true or false,
    "plausibility": true or false,
    "concept_presence": true or false
  }},
  "reason": "one sentence explanation if rejecting, empty string if accepting"
}}"""


async def validate(utterance: dict, semaphore: asyncio.Semaphore) -> dict:
    async with semaphore:
        prompt = DEAN_PROMPT.format(
            chunk_text=utterance["chunk_text"],
            utterance=utterance["utterance"],
            state=utterance["state"],
            target_concept=utterance["target_concept"],
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

    print(f"\nAccepted: {len(accepted)} / {len(utterances)}")
    print(f"Rejected: {len(rejected)}")

    if rejected:
        print("\nRejection reasons:")
        for u in rejected[:10]:
            print(f"  [{u['state']}] {u['utterance_id']}: {u['dean_result'].get('reason', '')}")

    with open(OUTPUT_FILE, "w") as f:
        for u in accepted:
            f.write(json.dumps(u) + "\n")

    print(f"\nSaved {len(accepted)} validated utterances to {OUTPUT_FILE}")

    if len(rejected) > 0:
        print(f"\n{len(rejected)} utterances rejected. Re-run 01_generate_utterances.py")
        print("for specific chunk_ids and regenerate, then re-run this script.")


if __name__ == "__main__":
    asyncio.run(main())
