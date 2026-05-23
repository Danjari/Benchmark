# SocraticRAG — EMNLP 2026 Execution Plan

**Deadline:** May 25, 2026
**Corpus:** 6.7960 Deep Learning (Fall 2024) + 6.036 Intro to ML
**Models evaluated:** GPT-4o, Claude Sonnet 4.6, Gemini 2.0 Flash

Status legend: `[ ]` todo · `[~]` in progress · `[x]` done

---

## Day 1 — May 22 (tonight) + May 23

### Tonight — Project Setup (2–3 hours)

- [x] Create Python project structure: `socraticrag/` with subfolders `data/`, `scripts/`, `outputs/`, `paper/`
- [x] Set up `.env` with OpenAI, Anthropic, Gemini API keys
- [x] Install dependencies: `mistralai`, `openai`, `anthropic`, `google-generativeai`, `ragas`, `pandas`, `scipy`, `tiktoken`, `tqdm`
- [x] Write `scripts/00_chunk_corpus.py` — automated two-step corpus chunker (added; replaces manual chunk selection)
  - Step 1: Mistral OCR — PDF → per-page markdown, preserving equations and layout
  - Step 2: GPT-4o Propositionizer — markdown → concept units (one teachable concept per unit, 100–500 tokens)
  - Grounded in Chen et al. (EMNLP 2024) Dense X Retrieval, adapted to concept-level units
  - Output schema: `chunk_id`, `source`, `course`, `page`, `concept`, `text`, `token_count`
- [ ] Download lecture note PDFs from MIT OCW — 6.036 target weeks: Perceptrons (W2), Regression (W5), Neural Networks I & II (W6–7), CNNs (W8)
- [ ] Download lecture note PDFs from MIT OCW — 6.7960: Optimization, Transformers/Attention, Regularization, Generative Models
- [ ] Run `00_chunk_corpus.py` and manually curate output to **~20 chunks** (10 per course)

### May 23 Morning — Dataset Generation

- [x] Write `scripts/01_generate_utterances.py`
  - Two-step contrastive generation per chunk C (upgraded from single-step 4-utterance generation)
  - Step 1: concept extraction — identify primary concept, derive correct understanding and C-grounded misconception
  - Step 2a: contrastive pair — accurate / erroneous (both targeting same concept)
  - Step 2b: contrastive pair — comprehension / confusion (both targeting same concept)
  - Profile P (`cognitive_state`, `target_concept`, `correct_understanding`, `misconception`) stored as first-class field
  - Output: `data/utterances_raw.jsonl`
- [x] Write `scripts/02_dean_validation.py`
  - Cross-judge protocol: GPT-4o generates, Claude Sonnet 4.6 validates (prevents self-enhancement bias)
  - 4 criteria for all states + 5th criterion (misconception match) for erroneous utterances
  - Contrastive pair integrity check: excludes both siblings if one is rejected or if they target different concepts
  - Outputs: `data/utterances.jsonl` (accepted) + `data/utterances_rejected.jsonl` (for acceptance-rate reporting)
- [ ] Run scripts 00 → 01 → 02
- [ ] Verify output: `data/utterances.jsonl` — 80 validated (chunk, utterance, state) triples

### May 23 Afternoon — Model Evaluation

- [x] Write `scripts/03_model_eval.py`
  - Async batch calls to GPT-4o, Claude Sonnet 4.6, Gemini 2.0 Flash
  - System prompt: EULER Socratic tutor prompt (guide without revealing answer)
  - Models receive only (C, U) — Profile P withheld for ecological validity
  - Cross-judge protocol baked in: Claude judges GPT-4o, GPT-4o judges Claude and Gemini (in metric scripts)
  - Output: `data/responses.jsonl`
- [ ] Run script (let it run in background while writing starts)
- [ ] Verify output: `data/responses.jsonl` — ~240 rows (chunk × utterance × model)

---

## Day 2 — May 24

### Morning — Score Everything (6 hours)

- Write `scripts/04_metric1.py` — Direct-Answer Leakage (Socratic Adherence)
  - GPT-4o judge with EULER rubric (question presence, on-topic, helpful, reveal-answer)
  - Binary output per response: 0 = leaked answer, 1 = withheld
- Write `scripts/05_metric2.py` — Retrieval Faithfulness
  - Step 1: GPT-4o extracts declarative presuppositions embedded in the Socratic question
  - Step 2: LLM entailment check of each presupposition against C (ENTAILED / NEUTRAL / CONTRADICTED)
  - Score = % of presuppositions entailed by C
- Write `scripts/06_metric3.py` — Pedagogical Alignment
  - GPT-4o POE judge from Discerning Minds rubric
  - Scores: Perception (0–3), Orchestration (0–3), Elicitation/Bloom's level (0–3)
- Write `scripts/07_ragas_baseline.py`
  - Run RAGAS faithfulness on the same 240 responses
  - Document that it returns undefined/trivial scores on interrogative outputs
- Run all four scripts
- Merge into `outputs/results.csv`

### Afternoon — Analysis + Paper Writing (6–8 hours)

- Write `scripts/08_analysis.py`
  - Results table: M1 / M2 / M3 per model (mean ± SD)
  - Spearman correlation between M1 and M2 scores (orthogonality check)
  - RAGAS comparison column showing it fails to discriminate
- Build joint degradation figure: models ranked by M1, M2 overlaid — shows they don't track
- **Send results table + paper draft to professors for review** (end of Day 2)

---

## Day 3 — May 25 (Submission Day)

### Morning — Final Paper (6–8 hours)

- Incorporate professor feedback
- Write abstract (after results are in hand — do this last)
- Final check: all citations match sources.md exactly, BibTeX formatted
- Confirm EMNLP 2026 LaTeX template is applied correctly
- Final read-through for consistency between methodology and results sections

### Afternoon — Submit

- Upload to EMNLP 2026 submission system
- Submit before deadline

---

## Paper Writing Track (starts May 23 afternoon, parallel to experiments)


| Section              | Source                                                  | Owner | Status |
| -------------------- | ------------------------------------------------------- | ----- | ------ |
| Introduction         | Section 1 of proposal, tighten to 1 page                |       | `[ ]`  |
| Related Work         | Sections 1.1–1.3, restructure into paragraphs           |       | `[ ]`  |
| Task Definition      | Phase 1 task formulation + formal notation              |       | `[ ]`  |
| Dataset Construction | Sections 2.1 + Phase 1, add real chunk/utterance counts |       | `[ ]`  |
| Evaluation Metrics   | Sections 2.2 + Phase 2 (already detailed)               |       | `[ ]`  |
| Experiments          | Phase 3 setup, add actual model/API identifiers         |       | `[ ]`  |
| Results & Analysis   | Write after numbers land (Day 2 evening)                |       | `[ ]`  |
| Conclusion           | 1 paragraph                                             |       | `[ ]`  |
| Abstract             | Write last, after results confirmed                     |       | `[ ]`  |
| References (BibTeX)  | Convert from sources.md                                 |       | `[ ]`  |


---

## Critical Checkpoint

**End of May 23, before stopping work:**

Look at raw M2 scores. If Metric 2 flags more than 25–30% of responses as introducing concepts not present in C, the core claim is confirmed and the paper has a spine. If under 10%, revisit the Socratic tutor system prompt before running full scoring.

---

## Open Items (need resolution before or during Day 1)

- Confirm which specific lecture note PDFs are available on MIT OCW for 6.7960 Fall 2024
- Confirm HuggingFace Inference API not needed (Gemini replaces Qwen2.5-7B-SocraticLM)
- Confirm professors are available for review end of Day 2 (May 24)
- Decide: long paper (8 pages) or short paper (4 pages)?

---

*Created: 2026-05-22. Update status markers as tasks complete.*