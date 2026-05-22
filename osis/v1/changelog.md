# Changelog

## 2026-05-23

**Build phase begins. Scripts 00–03 implemented and pipeline-ready.**

- Rewrote script 00: replaced character-based RecursiveCharacterTextSplitter with a two-step Propositionizer pipeline (Mistral OCR → GPT-4o concept-unit extraction), following Chen et al. (EMNLP 2024). Removed LangChain dependency.
- Rewrote script 01: two-step contrastive generation (concept extraction → pair generation); P as first-class artifact with `common_misconception` grounded in C as ground truth, not the generator's self-report.
- Rewrote script 02: switched Dean from GPT-4o to Claude (cross-judge protocol at dataset construction); extended contrastive pair check to comprehension/confusion siblings; added rejection log (`utterances_rejected.jsonl`) with per-state acceptance rates.
- Updated script 03: fixed broken field access (`u["state"]` → `u["profile"]["cognitive_state"]`); added `profile` to output rows; updated Gemini model from `gemini-1.5-pro` to `gemini-2.0-flash`; documented ecological validity rationale for (C, U) model input.
- Cross-script audit logged in decisions.md v1.3: 16 issues identified; 6 resolved same session (I1, I2, I5, I6, I7, I14); 10 remain open.
- Benchmark paper updated: Propositionizer chunking description + Chen et al. citation; cross-judge at construction time + Du et al. / Chan et al. citations; formal task P clarification; "up to 80" scenarios; Gemini 2.0 Flash; 4 new sources added.
- Literature confirmed: Dense X Retrieval (Chen et al., EMNLP 2024), Multiagent Debate (Du et al., ICML 2024), ChatEval (Chan et al., ICLR 2024), Self-Refine (Madaan et al., NeurIPS 2023).

## 2026-05-11

- Added thesis.md — version hypothesis, EMNLP 2026 deadline (May 25), open design questions
- Added core/product.md — product definition, C definition, DTS + 4-state combination explanation
- Added iteration-1--proposal-finalization/brief.md — current iteration bet, 14-day window
- Added professor session signal (April 30) — 4 concerns: DTS clarity, annotator count, human verification, C definition
- Updated twin.md — 15 stale items corrected (corpus, models, CoT, notation, pipeline)
- Resolved all 16 open decisions (decisions.md v1.1)
- All primary papers fully verified from PDFs
