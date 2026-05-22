---
type: observation
date: 2026-05-22
source: manual
summary: Methodology sentence for corpus ingestion pipeline (OCR + chunking) to use in paper Section 2.1.
---

Methodology framing for the ingestion pipeline (to place in Section 2.1, Corpus Collection):

> "We use Mistral OCR to extract text from slide PDFs, preserving structural boundaries, followed by semantic markdown chunking that respects section headers and logical divisions."

Context: the pipeline mirrors SynapsEd's production ingestion stack (Mistral OCR + multi-layered markdown chunking). This is not a standalone contribution — it supports Contribution 4 (Edu-QA-Socratic dataset) by ensuring chunk C is semantically coherent and faithful to the original lecture material. Naive sentence-splitting on `.` would corrupt slide content (bullets, headers, equations) and silently degrade every downstream metric.

Implementation: rewriting `socraticrag/scripts/00_chunk_corpus.py` to use the Mistral OCR API + semantic markdown chunking ported from SynapsEd's `lib/chunking/chunkMarkdown.ts`.
