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

## Build Phase Status (as of 2026-05-24)

Scripts 00–02 have completed their first full run. Pipeline is producing clean data.

**Confirmed results:**
- Corpus: ~303 concept units from MIT 6.7960 (Deep Learning) + MIT 6.036 (ML), avg 171 tokens
- Raw utterances: 1,212 (303 chunks × 4 cognitive states)
- Dean validation acceptance rate: ~45% overall (symmetric across states: 44–48%)
- Final validated dataset: 556 accepted utterances = 139 complete 4-utterance scenarios
- 102 broken contrastive pairs excluded (Metric 3 integrity preserved)
- Script 02 re-running on 211 credit-interrupted utterances; expected final: ~600–650 utterances

**Open implementation gaps (tracked in decisions.md v1.3):**
- **I3** — Multi-domain corpus: LibreTexts not yet integrated; currently MIT OCW only (2 courses)
- **I4** — Model coverage in script 03: Llama, LearnLM, Qwen2.5-SocraticLM not yet implemented
- **I10** — Gold annotation pipeline (scripts 04–08) not yet written
- **I16** — No README in `socraticrag/`

Paper fixes applied today: Propositionizer chunking description, cross-judge at construction, formal task (C,U) clarification, "up to 80" scenarios, Gemini 2.0 Flash, 4 new citations.

## Open Questions (Still Blocking)

- Himanshi's annotator count research — gate for Phase 4 design
- Specific MIT OCW course selection beyond 6.7960 and 6.036 (needed for multi-domain claim)
- PDFs not yet downloaded — need to be placed in `data/pdfs/6.7960/` and `data/pdfs/6.036/`

---

## Sessions

- 2026-05-23 — Build phase begins: scripts 00–03 implemented; Propositionizer, cross-judge Dean, rejection log, pair integrity check; 6 of 16 audit issues resolved; paper and all osis docs updated · `claude -r 242d2edc-a547-4cdb-a480-4616a9850466`
- 2026-05-11 — Iteration 1 brief created: proposal finalization, 14-day window to EMNLP deadline, 3 paper fixes + 3 missing citations · `claude -r 127ec0b2-7994-4530-bcae-3fbf88969adc`
