# Brief — Proposal Finalization

## The Bet

Deliver a professor-ready research proposal by May 25, 2026 (EMNLP 2026 submission deadline). The proposal proves the benchmark design is sound, the citations are correct, and the methodology is defensible — so professors can co-sign the submission direction and the build phase can begin immediately after.

## What Changes

1. **Three remaining paper fixes** (based on professor session, April 30):
   - Phase 4: update annotator count from "three" to "two professors with adjudication"
   - Context C: add explicit boundary definition (200-500 tokens, sole knowledge source)
   - Section 4: remove remaining SynapsEd corpus backbone reference

2. **Three missing citations to add** to the proposal:
   - FActScore (Min et al., 2023, EMNLP) — anchor for Metric 2 NLI mechanism
   - MT-Bench / Zheng et al. (2024) — validates LLM-as-judge + documents self-enhancement bias
   - TutorChat / Chevalier et al. (2024) — establishes LibreTexts as prior-work corpus precedent

3. **Specific MIT OCW courses**: name 3-4 courses across 3-4 domains to ground the corpus claim.

4. **Professor sign-off items** from session (still open):
   - Himanshi's annotator minimum research (hl3937@nyu.edu) — is 2 enough for EMNLP?
   - "Are the 4 profiles sufficient?" — needs a brief written defense in the proposal

## What Doesn't Change

- The three-metric design (Metrics 1, 2, 3 are final)
- The silver-to-gold annotation pipeline
- The model list (Qwen2.5-7B-SocraticLM, LearnLM, GPT-4o, Claude, Llama)
- The EMNLP 2026 target

## Open Questions (Block the Build Phase)

- Himanshi's annotator count research — gate for Phase 4 design
- Whether 4 cognitive states are sufficient or a custom taxonomy is needed
- Specific MIT OCW course selection (Moudjahid to provide)

---

## Sessions

- 2026-05-11 — Iteration 1 brief created: proposal finalization, 14-day window to EMNLP deadline, 3 paper fixes + 3 missing citations · `claude -r 127ec0b2-7994-4530-bcae-3fbf88969adc`
