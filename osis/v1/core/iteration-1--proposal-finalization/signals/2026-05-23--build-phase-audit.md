---
name: 2026-05-23-build-phase-audit
description: Cross-script audit of scripts 00–03; 16 issues identified and logged; 6 resolved; Propositionizer chunking redesign; cross-judge Dean; new citations confirmed
metadata:
  type: project
---

## Signal — Build Phase Start & Cross-Script Audit

**Date:** 2026-05-23  
**Session:** `claude -r 242d2edc-a547-4cdb-a480-4616a9850466`

### What happened

The first working session after the methodology-lock session (2026-05-11). This session transitioned from plan to build:

1. **Implemented scripts 00–03** (full pipeline from PDF → model responses)
2. **Ran a cross-script audit** — compared every script against the paper, each other, and the research literature. Surfaced 16 issues, categorized by severity.
3. **Resolved 6 critical/significant issues** in-session:
   - **I1** Cross-judge at dataset construction: Dean switched from GPT-4o to Claude
   - **I2** Comprehension/confusion pair integrity: `check_contrastive_pairs` extended to both pair types
   - **I5** Circular misconception validation: erroneous profile now always stores `common_misconception` from Step 1, not the generator's self-report
   - **I6** Token filter: `MIN_CHUNK_TOKENS = 150` enforced in script 00
   - **I7** Chunking redesign: replaced RecursiveCharacterTextSplitter with Propositionizer pipeline (Mistral OCR + GPT-4o concept-unit extraction, following Chen et al. EMNLP 2024)
   - **I14** Rejection log: `utterances_rejected.jsonl` now saved with per-state acceptance rates

4. **Literature confirmed for two new design choices:**
   - Proposition-level chunking: Chen et al. (EMNLP 2024) "Dense X Retrieval" — arXiv:2312.06648
   - Cross-model validation superiority over self-validation: Du et al. (ICML 2024) arXiv:2305.14325, Chan et al. (ICLR 2024) arXiv:2308.07201, contrasted with Madaan et al. (NeurIPS 2023) Self-Refine arXiv:2303.17651

5. **Paper updated** with all methodology changes; 4 new citations added to Sources section.

### Open issues (tracked in decisions.md v1.3)

| ID | Issue | Status |
|---|---|---|
| I3 | Multi-domain corpus — LibreTexts not integrated | Open |
| I4 | Script 03 missing ~4 models from paper | Open |
| I8 | Paper formal task (C,P,U) vs (C,U) — partial fix applied | Open |
| I9 | "80 scenarios" hard claim — fixed to "up to 80" | Open |
| I10 | Gold annotation pipeline and supporting sentences | Open |
| I11 | Temperature choices undocumented | Open |
| I12 | Stochastic generation reproducibility note | Open |
| I13 | Cross-page chunking for textbooks | Open |
| I15 | ragas in requirements.txt undocumented | Open |
| I16 | No README | Open |

### Next priorities

1. Download PDFs and run pipeline end-to-end (validate all scripts work together)
2. Build scripts 04–06 (Metric 1, Metric 2, Metric 3)
3. Add multi-domain corpus (LibreTexts, one non-ML domain)
4. Write README
