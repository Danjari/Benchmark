# SocraticRAG — EMNLP 2026 Execution Plan

**Deadline:** May 25, 2026
**Corpus:** 6.7960 Deep Learning (Fall 2024) + 6.036 Intro to ML
**Models evaluated:** GPT-4o, Claude Sonnet 4.6, Gemini

Status legend: `[ ]` todo · `[~]` in progress · `[x]` done

---

## Day 1 — May 22 (tonight) + May 23

### Tonight — Project Setup (2–3 hours)

- Create Python project structure: `socraticrag/` with subfolders `data/`, `scripts/`, `outputs/`, `paper/`
- Set up `.env` with OpenAI, Anthropic, Gemini API keys
- Install dependencies: `pymupdf`, `openai`, `anthropic`, `google-generativeai`, `ragas`, `pandas`, `scipy`, `tiktoken`
- Download lecture note PDFs from MIT OCW — 6.036 target weeks: Perceptrons (W2), Regression (W5), Neural Networks I & II (W6–7), CNNs (W8)
- Download lecture note PDFs from MIT OCW — 6.7960: Optimization, Transformers/Attention, Regularization, Generative Models
- Manually select **10 chunks per course = 20 chunks total** (200–500 tokens, one concept per chunk)
- Write selected chunks to `data/chunks.jsonl`

### May 23 Morning — Dataset Generation

- Write `scripts/01_generate_utterances.py`
  - For each chunk C, prompt GPT-4o to generate 4 student utterances (one per cognitive state)
  - Seed erroneous + confusion states with known DL/ML misconceptions, not arbitrary LLM inventions
  - Output format: `{ chunk_id, chunk_text, state, utterance, target_concept }`
- Write `scripts/02_dean_validation.py`
  - Second GPT-4o call per utterance: plausible? derivable from C only? state correctly expressed?
  - Auto-regenerate rejects until all 80 pass
- Run both scripts
- Verify output: `data/utterances.jsonl` — 80 validated (chunk, utterance, state) triples

### May 23 Afternoon — Model Evaluation

- Write `scripts/03_model_eval.py`
  - Async batch calls to GPT-4o, Claude Sonnet 4.6, Gemini
  - System prompt: EULER Socratic tutor prompt (guide without revealing answer)
  - Each model receives: system prompt + chunk C + student utterance
- Run script (let it run in background while writing starts)
- Verify output: `data/responses.jsonl` — 240 rows (chunk × utterance × model)

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