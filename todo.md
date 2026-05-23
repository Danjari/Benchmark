# SocraticRAG — EMNLP 2026 Execution Plan

**Deadline:** May 25, 2026
**Corpus:** 6.7960 Deep Learning (Fall 2024) + 6.036 Intro to ML
**Models evaluated:** GPT-4o, Claude Sonnet 4.6, Gemini 2.0 Flash

Status legend: `[ ]` todo · `[~]` in progress · `[x]` done

---

## ✅ COMPLETED — Pipeline (May 22–24)

- [x] Project structure, `.env`, dependencies
- [x] `scripts/00_chunk_corpus.py` — Mistral OCR + GPT-4o Propositionizer
  - **Result:** 303 concept units across MIT 6.7960 + 6.036, avg 171 tokens (range 100–694)
- [x] Download + ingest all MIT OCW PDFs for both courses (lec1–lec24 for DL, full notes for ML)
- [x] `scripts/01_generate_utterances.py` — two-step contrastive generation (GPT-4o)
  - **Result:** 1,212 raw utterances (303 chunks × 4 states), 1 chunk failed
- [x] `scripts/02_dean_validation.py` — Claude Sonnet 4.6 cross-judge Dean
  - **Result:** 658 accepted utterances; 54% acceptance rate (52% accurate/erroneous, 56% comprehension/confusion); 129 broken pairs excluded
- [x] `scripts/03_model_eval.py` — GPT-4o, Claude Sonnet 4.6, Gemini 2.0 Flash
  - **Result:** 1,974 responses (658 × 3), 0 failures, 26 min runtime

---

## 🔴 TODAY — May 24 (Remaining)

### Metric Scripts (Critical Path)

- [x] Write `scripts/04_metric1.py` — Direct-Answer Leakage
  - Cross-judge (Claude judges GPT-4o; GPT-4o judges Claude/Gemini)
  - EULER rubric: CLEARLY_WITHHELD (1.0) / BORDERLINE (0.5) / CLEARLY_LEAKED (0.0)
  - Input: `data/responses.jsonl` → Output: `data/scores_m1.jsonl`

- [x] Write `scripts/05_metric2.py` — Retrieval Faithfulness
  - Two-step: presupposition extraction → entailment check vs C
  - Vacuous handling (m2_vacuous flag); spot-check export CLI
  - Input: `data/responses.jsonl` → Output: `data/scores_m2.jsonl`

- [x] Write `scripts/06_metric3.py` — Pedagogical Alignment
  - GuideEval POE rubric: Perception (0–3), Orchestration (0–3), Elicitation/Bloom's (0–3)
  - Per-cognitive-state Bloom's anchors; spot-check export CLI
  - Input: `data/responses.jsonl` → Output: `data/scores_m3.jsonl`

- [x] Write `scripts/07_ragas_baseline.py`
  - Manual RAGAS faithfulness (library broken); demonstrates near-1.0 clustering
  - Input: `data/responses.jsonl` → Output: `data/scores_ragas.jsonl`

- [x] Write `scripts/08_analysis.py` — merge scores into `outputs/results.csv`
  - Results table: M1 / M2 / M3 / RAGAS per model (mean ± SD)
  - Spearman correlation M1 vs M2, M1 vs M3, M2 vs M3 (orthogonality check)
  - Per-cognitive-state breakdown for M3; M2 critical checkpoint (>25% flag rate)
  - Output: `outputs/results.csv`, `outputs/results_by_state.csv`, `outputs/correlation_matrix.csv`

- [ ] Run scripts 04 → 05 → 06 → 07 → 08
- [ ] **Send results table to professors** for review

---

## 🔴 TOMORROW — May 25 (Submission Day)

### Paper Writing (All sections)

| Section | Notes | Status |
|---|---|---|
| Introduction | Tighten proposal Section 1 to 1 page; lead with the joint constraint gap | `[ ]` |
| Related Work | Restructure proposal 1.1–1.3 into paragraphs; MathTutorBench BLEU argument | `[ ]` |
| Task Definition | Formal (C, U) → R notation; clarify P is annotation metadata, not model input | `[ ]` |
| Dataset Construction | Use writing_notes.md draft language; fill in final numbers from pipeline | `[ ]` |
| Evaluation Metrics | M1, M2, M3 descriptions; M2 two-step NLI as novel contribution | `[ ]` |
| Experiments | 3 models, zero-shot only (CoT/few-shot = future work given timeline) | `[ ]` |
| Results & Analysis | Write after scores land; orthogonality table; per-state breakdown for M3 | `[ ]` |
| Conclusion | 1 paragraph; restate contribution, limitations, future work | `[ ]` |
| Abstract | Write last, after results confirmed | `[ ]` |
| References (BibTeX) | Convert from sources.md; verify all cited in text | `[ ]` |

### Final Checks

- [ ] Incorporate professor feedback
- [ ] All citations match sources.md exactly
- [ ] EMNLP 2026 LaTeX template applied
- [ ] Final consistency check: methodology ↔ results ↔ abstract
- [ ] Upload + submit

---

## Critical Checkpoint (run immediately after script 05)

Look at raw M2 scores. If Metric 2 flags >25% of responses as introducing concepts not present in C, the core claim is confirmed. If <10%, the Socratic system prompt may be too constraining and models are playing it too safe — still a finding, but a different story.

---

## Open Decisions (still need resolution)

- **I3 — Multi-domain corpus:** currently ML/DL only. Either add a LibreTexts source or revise the paper's multi-domain claim. Recommend: revise claim for this submission, extend corpus in v2.
- **I4 — Model coverage:** Llama, LearnLM, SocraticLM not in script 03. Recommend: acknowledge as future work, frame GPT-4o / Claude / Gemini as the general LLM comparison.
- **I8 — Formal task notation:** paper says (C, P, U) → R; implementation uses (C, U) → R. Fix in Task Definition section with one sentence.
- **I11 — Temperature documentation:** add to paper appendix or implementation details.
- **I12 — Stochastic reproducibility:** add standard disclaimer sentence to Dataset Construction.
- **I15 — RAGAS intent:** add comment in requirements.txt.
- **I16 — README:** write after paper is done; needed for artifact submission.
- **Paper length:** long (8 pages) or short (4 pages)? Decide before writing.

---

*Last updated: 2026-05-24. Pipeline complete through script 03.*
