"""
Script 01: Student Utterance Generator
Input:  data/chunks.jsonl (manually curated — run 00 then hand-pick 20 chunks)
Output: data/utterances_raw.jsonl

For each chunk C, generates 4 student utterances (one per cognitive state):
  - accurate:      student makes a correct statement or follow-up
  - erroneous:     student expresses a specific misconception about C
  - comprehension: student explicitly says they understood something in C
  - confusion:     student explicitly says they don't understand something in C

Misconceptions for erroneous/confusion are seeded from known DL/ML errors,
not invented arbitrarily. The Dean validates in script 02.
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

COGNITIVE_STATES = ["accurate", "erroneous", "comprehension", "confusion"]

# Known DL/ML misconceptions to seed erroneous/confusion states
DL_MISCONCEPTIONS = """
Known misconceptions students have in machine learning and deep learning:
- Deeper networks always generalize better regardless of data size
- Dropout eliminates overfitting completely
- A high training accuracy means the model will perform well on test data
- Gradient descent always finds the global minimum
- Batch normalization removes the need for careful weight initialization
- ReLU cannot suffer from vanishing gradients under any circumstances
- More data always helps, regardless of data quality
- The learning rate only affects training speed, not final performance
- Convolutional layers require the same number of filters at every layer
- Attention mechanisms in transformers operate on tokens sequentially
- Backpropagation computes gradients by running the forward pass in reverse
- Regularization always hurts training accuracy
"""

GENERATION_PROMPT = """You are generating a benchmark dataset for evaluating AI tutoring systems.

Given this educational text chunk C from a university course:

---
{chunk_text}
---
(Course: {course})

Generate exactly 4 student utterances, one for each cognitive state below.
Each utterance must be derived ONLY from concepts explicitly present in C.
Do NOT introduce concepts from outside C.

Cognitive states:
1. ACCURATE: Student correctly understands a concept from C and asks a natural follow-up or makes a correct observation. Shows genuine understanding.
2. ERRONEOUS: Student has a specific, plausible misconception about a concept in C. Draw from these known misconceptions where relevant: {misconceptions}. The error must be derivable from C (the student misunderstood something IN C, not something unrelated).
3. COMPREHENSION: Student explicitly expresses that they understood something specific in C. ("I think I understand now that...", "So what you're saying is...")
4. CONFUSION: Student explicitly expresses uncertainty about something specific in C. ("I'm confused about...", "I don't understand why..."). The confusion must be about a concept present in C.

Respond ONLY with valid JSON in this exact format:
{{
  "accurate": {{
    "utterance": "...",
    "target_concept": "the specific concept from C this utterance is about",
    "correct_understanding": "what a correct understanding looks like"
  }},
  "erroneous": {{
    "utterance": "...",
    "target_concept": "the specific concept from C this utterance is about",
    "misconception": "the specific wrong belief the student holds",
    "correct_understanding": "what the correct understanding is"
  }},
  "comprehension": {{
    "utterance": "...",
    "target_concept": "the specific concept from C this utterance is about"
  }},
  "confusion": {{
    "utterance": "...",
    "target_concept": "the specific concept from C this utterance is about",
    "source_of_confusion": "what specifically in C is causing the confusion"
  }}
}}"""


async def generate_utterances(chunk: dict, semaphore: asyncio.Semaphore) -> dict | None:
    async with semaphore:
        prompt = GENERATION_PROMPT.format(
            chunk_text=chunk["text"],
            course=chunk["course"],
            misconceptions=DL_MISCONCEPTIONS,
        )
        try:
            response = await client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.7,
            )
            states = json.loads(response.choices[0].message.content)
            results = []
            for state in COGNITIVE_STATES:
                if state not in states:
                    continue
                results.append({
                    "utterance_id": f"{chunk['chunk_id']}_{state}",
                    "chunk_id": chunk["chunk_id"],
                    "chunk_text": chunk["text"],
                    "course": chunk["course"],
                    "source": chunk["source"],
                    "state": state,
                    "utterance": states[state]["utterance"],
                    "target_concept": states[state].get("target_concept", ""),
                    "metadata": {k: v for k, v in states[state].items()
                                 if k not in ("utterance", "target_concept")},
                    "dean_validated": False,
                })
            return results
        except Exception as e:
            print(f"Error on chunk {chunk['chunk_id']}: {e}")
            return None


async def main():
    chunks = []
    with open(CHUNKS_FILE) as f:
        for line in f:
            chunks.append(json.loads(line))

    print(f"Loaded {len(chunks)} chunks. Generating utterances...")

    semaphore = asyncio.Semaphore(5)  # max 5 concurrent API calls
    tasks = [generate_utterances(chunk, semaphore) for chunk in chunks]
    results = await tqdm.gather(*tasks, desc="Generating")

    all_utterances = []
    for result in results:
        if result:
            all_utterances.extend(result)

    with open(OUTPUT_FILE, "w") as f:
        for u in all_utterances:
            f.write(json.dumps(u) + "\n")

    print(f"\nGenerated {len(all_utterances)} utterances from {len(chunks)} chunks")
    print(f"Expected: {len(chunks) * 4}  |  Got: {len(all_utterances)}")
    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    asyncio.run(main())
