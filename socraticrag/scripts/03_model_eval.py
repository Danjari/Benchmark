"""
Script 03: Model Evaluation
Input:  data/utterances.jsonl
Output: data/responses.jsonl

Runs each (C, U) pair through 3 models with a Socratic tutor system prompt.
Models: GPT-4o, Claude Sonnet 4.6, Gemini 2.0 Flash

Ecological validity note: models receive only (C, U) — not P. Student Profile P
is annotation metadata serving as Metric 3 ground truth. A deployed tutoring
system would not have access to a labelled ground-truth profile; passing P would
give an unrealistic advantage and conflate annotation with model capability.

Cross-judge protocol (Zheng et al., 2024):
  - Claude judges GPT-4o outputs (in metric scripts)
  - GPT-4o judges Claude outputs (in metric scripts)
  - GPT-4o judges Gemini outputs
"""

import os
import re
import json
import asyncio
from pathlib import Path
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
import google.generativeai as genai
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
anthropic_client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

INPUT_FILE = Path("data/utterances.jsonl")
OUTPUT_FILE = Path("data/responses.jsonl")
CHECKPOINT_FILE = Path("data/.responses_checkpoint.json")
RESULTS_TEMP_FILE = Path("data/.responses_temp.jsonl")

# Socratic tutor system prompt adapted from EULER (Bonino et al., 2024)
SOCRATIC_SYSTEM_PROMPT = """You are a Socratic tutor. Your role is to guide students to discover answers themselves through thoughtful questions.

Rules you must follow:
1. NEVER reveal the answer or solution directly.
2. Ask ONE guiding question that helps the student think through the problem.
3. Your question must be grounded ONLY in the provided context. Do not introduce concepts not present in the context.
4. Adapt your question to the student's apparent level of understanding.
5. Your entire response must be a single guiding question, not a statement or explanation.

Context (your sole knowledge source):
{chunk_text}"""

USER_TURN = """Student says: "{utterance}"

Respond with a single Socratic guiding question."""


async def call_openai(chunk_text: str, utterance: str, semaphore: asyncio.Semaphore) -> str | None:
    async with semaphore:
        for attempt in range(6):
            try:
                response = await openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": SOCRATIC_SYSTEM_PROMPT.format(chunk_text=chunk_text)},
                        {"role": "user", "content": USER_TURN.format(utterance=utterance)},
                    ],
                    temperature=0.7,
                    max_tokens=300,
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                err = str(e)
                if "429" in err:
                    match = re.search(r"try again in (\d+(?:\.\d+)?)s", err)
                    wait = float(match.group(1)) + 1.0 if match else 2 ** attempt
                    await asyncio.sleep(wait)
                else:
                    print(f"  [gpt-4o] error: {e}")
                    return None
        return None


async def call_anthropic(chunk_text: str, utterance: str, semaphore: asyncio.Semaphore) -> str | None:
    async with semaphore:
        for attempt in range(6):
            try:
                response = await anthropic_client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=300,
                    system=SOCRATIC_SYSTEM_PROMPT.format(chunk_text=chunk_text),
                    messages=[{"role": "user", "content": USER_TURN.format(utterance=utterance)}],
                )
                return response.content[0].text.strip()
            except Exception as e:
                err = str(e)
                if "429" in err or "rate_limit" in err or "overloaded" in err:
                    wait = 2 ** attempt
                    match = re.search(r"try again in (\d+(?:\.\d+)?)s", err)
                    if match:
                        wait = float(match.group(1)) + 1.0
                    await asyncio.sleep(wait)
                else:
                    print(f"  [claude] error: {e}")
                    return None
        return None


async def call_gemini(chunk_text: str, utterance: str, semaphore: asyncio.Semaphore) -> str | None:
    async with semaphore:
        for attempt in range(6):
            try:
                model = genai.GenerativeModel(
                    model_name="gemini-2.0-flash",
                    system_instruction=SOCRATIC_SYSTEM_PROMPT.format(chunk_text=chunk_text),
                )
                response = await asyncio.to_thread(
                    model.generate_content,
                    USER_TURN.format(utterance=utterance),
                )
                return response.text.strip()
            except Exception as e:
                err = str(e)
                if "429" in err or "quota" in err.lower() or "resource_exhausted" in err.lower():
                    await asyncio.sleep(2 ** attempt)
                else:
                    print(f"  [gemini] error: {e}")
                    return None
        return None


async def evaluate_utterance(u: dict, semaphore: asyncio.Semaphore) -> list[dict]:
    model_calls = {
        "gpt-4o": call_openai(u["chunk_text"], u["utterance"], semaphore),
        "claude-sonnet-4-6": call_anthropic(u["chunk_text"], u["utterance"], semaphore),
        "gemini-2.0-flash": call_gemini(u["chunk_text"], u["utterance"], semaphore),
    }
    results = await asyncio.gather(*model_calls.values())
    rows = []
    for model, result in zip(model_calls.keys(), results):
        if result is None:
            print(f"  [SKIP] {u['utterance_id']} / {model}")
            continue
        rows.append({
            "response_id": f"{u['utterance_id']}_{model.replace('-', '_')}",
            "utterance_id": u["utterance_id"],
            "chunk_id": u["chunk_id"],
            "chunk_text": u["chunk_text"],
            "course": u["course"],
            "profile": u["profile"],
            "utterance": u["utterance"],
            "model": model,
            "response": result,
        })
    return rows


async def main():
    utterances = []
    with open(INPUT_FILE) as f:
        for line in f:
            utterances.append(json.loads(line))

    # Resume support: load already-processed utterance_ids from checkpoint
    done: set[str] = set()
    if CHECKPOINT_FILE.exists() and RESULTS_TEMP_FILE.exists():
        with open(CHECKPOINT_FILE) as f:
            done = set(json.load(f))
        saved = sum(1 for _ in open(RESULTS_TEMP_FILE))
        print(f"Resuming: {len(done)} utterances already done, {saved} responses on disk.")

    remaining = [u for u in utterances if u["utterance_id"] not in done]
    print(f"{len(utterances)} utterances total. {len(remaining)} remaining. Running 3 models each...")

    semaphore = asyncio.Semaphore(3)  # 3 concurrent calls — one per model per utterance

    for u in tqdm(remaining, desc="Model eval"):
        rows = await evaluate_utterance(u, semaphore)
        if rows:
            with open(RESULTS_TEMP_FILE, "a") as f:
                for row in rows:
                    f.write(json.dumps(row) + "\n")
        done.add(u["utterance_id"])
        with open(CHECKPOINT_FILE, "w") as f:
            json.dump(list(done), f)

    # Compile final output
    all_responses = []
    with open(RESULTS_TEMP_FILE) as f:
        for line in f:
            all_responses.append(json.loads(line))

    with open(OUTPUT_FILE, "w") as f:
        for row in all_responses:
            f.write(json.dumps(row) + "\n")

    print(f"\nSaved {len(all_responses)} responses to {OUTPUT_FILE}")
    by_model: dict[str, int] = {}
    for r in all_responses:
        by_model[r["model"]] = by_model.get(r["model"], 0) + 1
    for model, count in sorted(by_model.items()):
        print(f"  {model}: {count} responses")
    print(f"\nTo start fresh: delete data/responses.jsonl, data/.responses_temp.jsonl, data/.responses_checkpoint.json")


if __name__ == "__main__":
    asyncio.run(main())
