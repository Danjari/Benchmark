"""
Script 03: Model Evaluation
Input:  data/utterances.jsonl
Output: data/responses.jsonl

Runs each (C, U) pair through 3 models with a Socratic tutor system prompt.
Models: GPT-4o, Claude Sonnet 4.6, Gemini 1.5 Pro

Cross-judge protocol (Zheng et al., 2024):
  - Claude judges GPT-4o outputs (in metric scripts)
  - GPT-4o judges Claude outputs (in metric scripts)
  - GPT-4o judges Gemini outputs
"""

import os
import json
import asyncio
from pathlib import Path
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
import google.generativeai as genai
from dotenv import load_dotenv
from tqdm.asyncio import tqdm

load_dotenv()

openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
anthropic_client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

INPUT_FILE = Path("data/utterances.jsonl")
OUTPUT_FILE = Path("data/responses.jsonl")

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

MODELS = {
    "gpt-4o": "openai",
    "claude-sonnet-4-6": "anthropic",
    "gemini-1.5-pro": "gemini",
}


async def call_openai(chunk_text: str, utterance: str, semaphore: asyncio.Semaphore) -> str:
    async with semaphore:
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


async def call_anthropic(chunk_text: str, utterance: str, semaphore: asyncio.Semaphore) -> str:
    async with semaphore:
        response = await anthropic_client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=300,
            system=SOCRATIC_SYSTEM_PROMPT.format(chunk_text=chunk_text),
            messages=[{"role": "user", "content": USER_TURN.format(utterance=utterance)}],
        )
        return response.content[0].text.strip()


async def call_gemini(chunk_text: str, utterance: str, semaphore: asyncio.Semaphore) -> str:
    async with semaphore:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            system_instruction=SOCRATIC_SYSTEM_PROMPT.format(chunk_text=chunk_text),
        )
        response = await asyncio.to_thread(
            model.generate_content,
            USER_TURN.format(utterance=utterance),
        )
        return response.text.strip()


async def evaluate_utterance(u: dict, semaphore: asyncio.Semaphore) -> list[dict]:
    rows = []
    calls = {
        "gpt-4o": call_openai(u["chunk_text"], u["utterance"], semaphore),
        "claude-sonnet-4-6": call_anthropic(u["chunk_text"], u["utterance"], semaphore),
        "gemini-1.5-pro": call_gemini(u["chunk_text"], u["utterance"], semaphore),
    }
    results = await asyncio.gather(*calls.values(), return_exceptions=True)
    for model, result in zip(calls.keys(), results):
        if isinstance(result, Exception):
            print(f"Error [{model}] {u['utterance_id']}: {result}")
            continue
        rows.append({
            "response_id": f"{u['utterance_id']}_{model.replace('-', '_')}",
            "utterance_id": u["utterance_id"],
            "chunk_id": u["chunk_id"],
            "chunk_text": u["chunk_text"],
            "course": u["course"],
            "state": u["state"],
            "utterance": u["utterance"],
            "target_concept": u["target_concept"],
            "model": model,
            "response": result,
        })
    return rows


async def main():
    utterances = []
    with open(INPUT_FILE) as f:
        for line in f:
            utterances.append(json.loads(line))

    print(f"Running {len(utterances)} utterances x 3 models = {len(utterances) * 3} API calls...")

    semaphore = asyncio.Semaphore(3)
    tasks = [evaluate_utterance(u, semaphore) for u in utterances]
    results = await tqdm.gather(*tasks, desc="Model eval")

    all_responses = [row for batch in results for row in batch]

    with open(OUTPUT_FILE, "w") as f:
        for row in all_responses:
            f.write(json.dumps(row) + "\n")

    print(f"\nSaved {len(all_responses)} responses to {OUTPUT_FILE}")
    by_model = {}
    for r in all_responses:
        by_model[r["model"]] = by_model.get(r["model"], 0) + 1
    for model, count in by_model.items():
        print(f"  {model}: {count} responses")


if __name__ == "__main__":
    asyncio.run(main())
