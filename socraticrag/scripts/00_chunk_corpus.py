"""
Script 00: Corpus Chunker
Input:  PDF files in data/pdfs/
Output: data/chunks.jsonl

Each chunk is a semantically coherent unit (200-500 tokens) representing
one concept from the course material. This is context C in the benchmark.
"""

import os
import json
import hashlib
import fitz  # pymupdf
import tiktoken
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

TOKENIZER = tiktoken.get_encoding("cl100k_base")
MIN_TOKENS = 150
MAX_TOKENS = 500
PDF_DIR = Path("data/pdfs")
OUTPUT_FILE = Path("data/chunks.jsonl")


def count_tokens(text: str) -> int:
    return len(TOKENIZER.encode(text))


def chunk_text(text: str, source: str, course: str) -> list[dict]:
    """Split text into semantic chunks within token bounds."""
    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
    chunks = []
    current = []
    current_tokens = 0

    for sentence in sentences:
        s_tokens = count_tokens(sentence)
        if current_tokens + s_tokens > MAX_TOKENS and current:
            chunk_text = ". ".join(current) + "."
            if count_tokens(chunk_text) >= MIN_TOKENS:
                chunks.append(chunk_text)
            current = [sentence]
            current_tokens = s_tokens
        else:
            current.append(sentence)
            current_tokens += s_tokens

    if current:
        chunk_text = ". ".join(current) + "."
        if count_tokens(chunk_text) >= MIN_TOKENS:
            chunks.append(chunk_text)

    results = []
    for i, text in enumerate(chunks):
        chunk_id = hashlib.md5(f"{source}_{i}".encode()).hexdigest()[:8]
        results.append({
            "chunk_id": chunk_id,
            "source": source,
            "course": course,
            "chunk_index": i,
            "text": text,
            "token_count": count_tokens(text),
        })
    return results


def extract_pdf(pdf_path: Path, course: str) -> list[dict]:
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    doc.close()
    return chunk_text(full_text, pdf_path.name, course)


def main():
    if not PDF_DIR.exists():
        print(f"Create {PDF_DIR} and place course PDFs inside subfolders named by course.")
        print("  data/pdfs/6.7960/  — Deep Learning lecture notes")
        print("  data/pdfs/6.036/   — Intro to ML lecture notes")
        return

    all_chunks = []
    for course_dir in sorted(PDF_DIR.iterdir()):
        if not course_dir.is_dir():
            continue
        course = course_dir.name
        for pdf_file in sorted(course_dir.glob("*.pdf")):
            print(f"Processing {pdf_file.name} ({course})...")
            chunks = extract_pdf(pdf_file, course)
            all_chunks.extend(chunks)
            print(f"  -> {len(chunks)} chunks")

    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        for chunk in all_chunks:
            f.write(json.dumps(chunk) + "\n")

    print(f"\nTotal chunks: {len(all_chunks)}")
    print(f"Saved to {OUTPUT_FILE}")
    print("\nToken distribution:")
    tokens = [c["token_count"] for c in all_chunks]
    print(f"  Min: {min(tokens)}  Max: {max(tokens)}  Avg: {sum(tokens)//len(tokens)}")


if __name__ == "__main__":
    main()
