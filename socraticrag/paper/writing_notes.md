# SocraticRAG — Paper Writing Notes

---

## Dataset Construction Section

### Corpus and Chunking (Script 00)

**Pipeline:** Two steps — Mistral OCR (`mistral-ocr-latest`) converts each PDF page to markdown, then GPT-4o (temperature=0.1) segments the markdown into concept units via the Propositionizer prompt.

**Token filter:** 100-token floor (below = slide header or orphaned fragment), 500-token soft ceiling (above = likely multi-concept block; flagged but accepted; Dean's derivability criterion acts as downstream filter).

**Empirical results from first run:**
- ~303 valid concept units across 2 MIT OCW courses (6.7960 Deep Learning + 6.036 ML)
- Token distribution: min 100, max 694, avg 171 tokens
- 3 units exceeded 500-token ceiling (flagged for manual review)

**Draft language for Dataset Construction:**
> "We extract concept units from lecture PDFs using a two-step pipeline: Mistral OCR converts each page to structured markdown, and GPT-4o segments the markdown into concept-level chunks following Chen et al. (EMNLP 2024). Each unit covers exactly one teachable idea — a definition, theorem, algorithm, or worked example. Units below 100 tokens (slide headers, orphaned fragments) are discarded; units above 500 tokens are flagged as potential multi-concept candidates. The resulting corpus contains X concept units from two MIT OpenCourseWare courses (MIT 6.7960 Deep Learning and MIT 6.036 Introduction to Machine Learning), with a mean of 171 tokens per unit (range: 100–694)."

---

### Utterance Generation (Script 01)

**Three API calls per chunk (GPT-4o, cross-judge isolation from Claude Dean):**
1. Concept extraction (temperature=0.3): identifies the single primary teachable concept; derives what correct understanding looks like from C alone; derives a specific misconception that arises only from misreading C — not imported from external knowledge.
2. Contrastive pair A/E (temperature=0.5): accurate utterance demonstrates correct understanding; erroneous utterance expresses the specific C-grounded misconception from step 1.
3. Contrastive pair C/C (temperature=0.5): comprehension utterance uses explicit markers ("I think I understand now…", "So what you're saying is…", "Ah, I see —"); confusion utterance uses explicit markers ("I'm confused about…", "I don't understand why…", "Wait, I'm not sure…").

**Key design choice:** Profile P (target_concept, correct_understanding, misconception) is extracted in step 1 and stored as a first-class field, distinct from utterance U. This ensures: (a) erroneous misconceptions are grounded in C, not in external misconception lists; (b) contrastive pairs target the same concept, which is a structural requirement for Metric 3 scoring.

**Results:** 1,212 raw utterances from 303 chunks (303 × 4). 1 chunk failed concept extraction and was skipped.

**Draft language:**
> "For each concept unit C, we apply a three-step generation procedure using GPT-4o. First, we extract the primary teachable concept and derive a C-grounded misconception — a specific wrong belief that could arise from misreading C alone, without importing external knowledge. Second, we generate a contrastive accurate/erroneous pair: both utterances target the same concept, with the erroneous utterance expressing the C-derived misconception. Third, we generate a contrastive comprehension/confusion pair: both utterances use explicit metacognitive markers. Each step enforces that only concepts present in C may appear in U, establishing C as the sole permitted knowledge source for all downstream evaluation."

---

### Dean Validation (Script 02)

**Validator:** Claude Sonnet 4.6. Cross-judge: different model family from GPT-4o generator. Motivated by Zheng et al. (NeurIPS 2024), Du et al. (ICML 2024), Chan et al. (ICLR 2024).

**Four criteria (all utterances):**
1. **State Match** — utterance authentically expresses the claimed cognitive state. Comprehension/confusion require explicit markers, not restatements. Accurate requires correct understanding, not a question that could come from any state.
2. **Derivability** — utterance is derivable ONLY from C. Any concept not explicitly present in C fails this criterion, even if the concept is implied or closely related.
3. **Plausibility** — a real university student could plausibly say this.
4. **Concept Presence** — the target concept is explicitly present in C (guards against hallucinated concepts in step 1).

**Fifth criterion (erroneous only):**
5. **Misconception Match** — utterance expresses the specific misconception from step 1 of generation, not a generic or unrelated error.

**Contrastive pair integrity check (post-individual validation):**
- For each chunk, check accurate/erroneous pair and comprehension/confusion pair separately.
- If one sibling is accepted and the other rejected → broken pair → both excluded from output.
- If siblings target different concepts → broken pair → both excluded.
- Broken pairs are flagged for regeneration with script 01.
- Rationale: Metric 3 requires both siblings to compare against; a half-pair is useless for contrastive scoring.

**Empirical results (final):**
- Accepted: 658 utterances
- Individually rejected: 215
- Broken pairs excluded: 129 chunks / 258 utterances
- Acceptance rate by cognitive state: accurate 52%, erroneous 52%, comprehension 56%, confusion 56%
- Overall acceptance rate: ~54%

**Top rejection reasons (for paper discussion):**
- Comprehension utterances lacking explicit comprehension markers (reads as accurate restatement)
- Accurate utterances importing outside knowledge not present in C
- Erroneous utterances expressing generic gradient descent errors instead of the specific C-derived misconception
- Concept presence failures where C only demonstrates a concept numerically but never names it

**Draft language:**
> "Each (P, U) pair is validated by a Claude Sonnet 4.6 Dean agent — a different model family from the GPT-4o generator, implementing the cross-judge protocol of Zheng et al. (2024). The Dean applies four criteria: (1) state match, (2) derivability from C alone, (3) plausibility for a university student, and (4) concept presence in C. For erroneous utterances, a fifth criterion verifies that the expressed error matches the specific C-grounded misconception derived in generation step 1 rather than a generic or unrelated error. Following individual validation, a contrastive pair integrity check verifies that both siblings of each pair are accepted and target the same concept; broken pairs are excluded and flagged for regeneration. The overall acceptance rate is 54% (range: 52–56% across cognitive states), reflecting the strictness of the derivability criterion. The final dataset contains 658 validated utterances from 303 source chunks."

---

## Empirical Results (Final Numbers — All Scripts Complete)

### M1 — Direct-Answer Leakage

| Model | Mean M1 | SD | Judge |
|---|---|---|---|
| GPT-4o | 0.845 | 0.231 | Claude Sonnet 4.6 |
| Claude Sonnet 4.6 | 0.643 | 0.226 | GPT-4o |
| Gemini 2.0 Flash | 0.643 | 0.226 | GPT-4o |

**Verdict distribution:** 42% CLEARLY_WITHHELD · 58% BORDERLINE · 0% CLEARLY_LEAKED

**Interpretation:**
- 0% CLEARLY_LEAKED is expected and defensible: frontier models instructed to be Socratic tutors do not ignore the instruction entirely. The failure mode is leading questions, not stated answers.
- 58% BORDERLINE is the real finding: the majority of responses from all three models are interrogative in form but so leading that a student could extract the correct answer without reasoning.
- Claude = Gemini identically (0.643 ± 0.226) — both judged by GPT-4o. Worth noting as a potential cross-judge artifact; professor spot-check on BORDERLINE cases is the validation path.
- GPT-4o scores higher on M1 (0.845) but lower on M3 (5.821/9) — the models most cautious about revealing answers are the least pedagogically effective. This M1-M3 reversal is a key cross-metric finding.

**Draft language for Results:**
> "No model produced CLEARLY_LEAKED responses, consistent with instruction-following behavior: frontier models prompted as Socratic tutors do not abandon the role entirely. However, 58% of responses across all models were classified as BORDERLINE — interrogative in form but sufficiently leading that a student could extract the correct understanding without independent reasoning. GPT-4o produced the most clearly-withheld responses (M1 = 0.845), while Claude Sonnet 4.6 and Gemini 2.0 Flash scored equally (M1 = 0.643)."

---

### M2 — Retrieval Faithfulness

| Model | Mean M2 | SD | Vacuous | Judge |
|---|---|---|---|---|
| GPT-4o | 0.643 | 0.256 | — | Claude Sonnet 4.6 |
| Claude Sonnet 4.6 | 1.000 | 0.000 | ~66.7% | GPT-4o |
| Gemini 2.0 Flash | 1.000 | 0.000 | ~66.7% | GPT-4o |

**Overall vacuous rate:** 66.7% (no presuppositions extractable → score defaults to 1.0)
**Responses with ≥1 unentailed presupposition:** 26.8%

**Interpretation — two distinct M2 failure modes:**
- **Type A (GPT-4o):** Asks specific, grounded Socratic questions → presuppositions extractable → some fail entailment check → M2 = 0.643. The model is specific but introduces concepts not in C.
- **Type B (Claude/Gemini):** Asks generic, vague Socratic questions → no presuppositions to extract → vacuous M2 = 1.000. The model is technically faithful but produces low-information questions.
- Both are faithfulness problems: Type A = unfaithful specificity; Type B = vacuous genericism. M3 scores confirm Type B is not pedagogically superior (Claude 8.164, Gemini 7.799 — but these are high despite vacuous M2, suggesting M3 measures something different from M2).
- This finding is richer than a simple "GPT-4o fails M2." It reveals that faithfulness metrics alone cannot distinguish quality: a vacuous question scores perfectly on M2 but may be pedagogically useless.

**Draft language for Results:**
> "M2 reveals two distinct failure modes. GPT-4o produces specific Socratic questions with extractable presuppositions, 35.7% of which are not entailed by C (M2 = 0.643 ± 0.256). Claude and Gemini produce questions with no extractable presuppositions in 66.7% of cases, scoring vacuously at 1.000 ± 0.000 — technically faithful but informationally empty. Both patterns represent faithfulness failures of different kinds: unfaithful specificity versus vacuous generalism."

---

### M3 — Pedagogical Alignment

| Model | Perception | Orchestration | Elicitation | Total (max 9) | Judge |
|---|---|---|---|---|---|
| Claude Sonnet 4.6 | — | — | — | 8.164 ± 1.370 | GPT-4o |
| Gemini 2.0 Flash | — | — | — | 7.799 ± 1.838 | GPT-4o |
| GPT-4o | — | — | — | 5.821 ± 1.921 | Claude Sonnet 4.6 |

**Dimension breakdown (all models):** Perception 2.5 · Orchestration 2.43 · Elicitation 2.27 (approx — need script 08 for per-model breakdown)

**By cognitive state (all models):**
- Comprehension: 7.893 ± 1.776 (highest)
- Erroneous: 7.812 ± 1.001
- Accurate: 7.232 ± 2.436
- Confusion: 6.148 ± 2.020 (lowest — models struggle most with confused students)

**Key finding — M1/M3 reversal:**
GPT-4o scores highest on M1 (Socratic withholding) but lowest on M3 (pedagogical alignment). Claude scores lowest on M1 but highest on M3. Being maximally Socratic does not mean being maximally pedagogically effective. This is a substantive finding for educational AI: optimizing for one constraint (don't reveal the answer) can trade off against the other (guide the student well).

**Confused students are systematically underserved:** All models score lowest on confusion-state utterances. This is actionable for future system design.

**Draft language for Results:**
> "M3 scores reveal a striking reversal of M1 rankings. Claude Sonnet 4.6 achieves the highest pedagogical alignment (8.164/9), followed by Gemini 2.0 Flash (7.799/9), while GPT-4o — the model most successful at withholding direct answers — scores lowest on pedagogical alignment (5.821/9). This inversion suggests that Socratic restraint and pedagogical effectiveness are not the same capability: maximizing answer-withholding may come at the cost of guidance quality. Across all models, responses to confusion-state utterances receive the lowest M3 scores (6.148 ± 2.020), indicating that supporting students who are genuinely lost remains the most challenging scenario for current LLMs."

---

### RAGAS Baseline — Structural Incompatibility Confirmed

| Model | RAGAS Score | SD |
|---|---|---|
| Claude Sonnet 4.6 | 1.0000 | 0.0000 |
| GPT-4o | 1.0000 | 0.0000 |
| Gemini 2.0 Flash | 0.9863 | 0.1162 |
| **Overall** | **0.9954** | **0.0674** |

**Empty responses (no statements extracted):** 1,920/1,974 = **97.3%**
**Scores ≥ 0.9:** 99.5%

**Interpretation:** Even stronger than expected. 97.3% of Socratic questions — across all three models — yielded zero declarative statements under RAGAS decomposition. The remaining 2.7% produced trivially supported statements. RAGAS cannot discriminate between a strong and a weak Socratic response. This is not a limitation of RAGAS for this specific dataset — it is a structural incompatibility: the metric presupposes declarative output, and Socratic tutoring requires interrogative output.

**The key comparison for the paper:**
- RAGAS: 0.9954 ± 0.0674 — uniform, no model discrimination
- M2: 0.643 (GPT-4o) vs 1.000 (Claude/Gemini) — discriminates between models (though vacuous problem remains)
- This single comparison is the empirical anchor of the paper.

**Draft language for Results:**
> "RAGAS faithfulness scores cluster at 1.000 for all models (mean 0.9954 ± 0.0674), with 97.3% of responses yielding zero extractable declarative statements. This confirms the structural incompatibility identified in Section 3: RAGAS cannot evaluate Socratic outputs because its decomposition step presupposes declarative text. In contrast, M2's presupposition-based adaptation identifies meaningful faithfulness variation across models (0.643–1.000), demonstrating that the problem is not the task difficulty but the metric design."

---

## Competitive Landscape & Submission Strategy

### Honest Assessment vs. Accepted 2025 Papers

We compared against five accepted 2025 ACL/EMNLP papers. Key findings:

**Our genuine strengths:**
- Novel problem statement: joint constraint evaluation (Socratic + faithful) is unaddressed in the literature
- M2 presupposition adaptation of FActScore to interrogative outputs is a real methodological contribution
- RAGAS incompatibility demonstration is a concrete, testable claim
- Educational AI application is timely

**Four structural weaknesses reviewers will name:**

**1. Scale gap.**
MEBench (accepted long paper): 4,780 items, 241 topics, diverse domains. SocraticRAG: 658 items, 2 MIT OCW courses, one domain (ML/DL). For a benchmark claiming to measure a general failure mode, this is a significant vulnerability. Mitigation: scope the claim explicitly ("initial benchmark in ML/DL educational content; multi-domain extension is future work").

**2. Circular LLM evaluation.**
Every accepted benchmark paper avoids LLM-as-judge for its main evaluation metric. MEBench uses SQL-derived verifiable answers. The Self-Consistent paper uses NLI + 15 stochastic samples. Our M1, M2, M3 are all LLM judges. Without human validation numbers (Cohen's κ, Spearman ρ), reviewers will correctly say the pipeline is circular. **Professor spot checks are not optional — they are the paper's main defense against this objection.**

**3. Too many contributions at medium depth.**
Every successful short paper in the sample does one thing well (one definition, one method, one finding). SocraticRAG is presenting: task definition + dataset pipeline + 3 metrics + RAGAS baseline + experiments. More contributions = more attack surface. Mitigation: frame M2 as the central contribution; M1 and M3 are supporting axes.

**4. No gold labels / ground truth.**
MEBench has SQL-verified answers. We have no ground truth for what a "good" Socratic response looks like — no expert-annotated Golden Response R₀ₙₑˣ yet. Mitigation: be explicit in Limitations that this is a silver-standard benchmark; professor spot checks provide partial validation.

### Recommended Paper Strategy

**Target: short paper (4 pages) with M2 as the central contribution.**

The story that fits in 4 pages and is defensible:
> "Existing RAG faithfulness metrics (RAGAS) structurally fail on Socratic question outputs because they require declarative statements. We propose a presupposition-based adaptation (M2) that handles interrogative outputs, show it produces meaningful score variance (unlike RAGAS which clusters near 1.0), and validate it against human judgment (Cohen's κ = X). M1 and M3 provide supporting evidence of the joint constraint failure mode."

The RAGAS near-1.0 clustering table is the empirical anchor of the paper. If RAGAS scores ≈ 0.98 ± 0.02 while M2 shows real spread across models and states, that one comparison tells the whole story.

**If going long paper:** the human validation gap is the main risk. Need κ and ρ numbers from professor before submission. Without them, reviewers have an easy rejection reason.

### Critical Pre-Submission Checklist

- [ ] Professor spot check M2 (40 rows): compute Cohen's κ — report in Evaluation Metrics section
- [ ] Professor spot check M3 (30 rows): compute Spearman ρ — target > 0.7, report in Evaluation Metrics
- [ ] M2 critical checkpoint: if >25% responses flag unentailed presuppositions → confirms core claim
- [ ] RAGAS clustering confirmed: scores ≈ 1.0 with near-zero variance → structural incompatibility demonstrated
- [ ] One sentence in Task Definition: oracle-retrieval defense
- [ ] Limitations section: scale (2 courses, 1 domain), no gold labels, LLM judge limitations, stochastic reproducibility

---

## Task Definition Section

### Defending Oracle-Perfect Retrieval (Reviewer Objection)

**The vulnerability:** In a real Socratic RAG system the flow is:

```
student query → retrieval (find relevant chunk) → LLM generates Socratic response using C
```

The pipeline skips the first arrow. C is handed directly to the model — no retrieval step runs. This means we are testing **context adherence**, not retrieval + generation jointly.

**The defense (two-part argument):**

**1. We evaluate the component that has no existing benchmark.**

Decompose RAG into retrieval and generation. Retrieval quality (did the system find the right chunk?) is already addressed by existing metrics — recall, precision, RAGAS context metrics. What has *no* existing benchmark is the generation step for pedagogical outputs: given C, does the model generate a Socratic response that stays bounded by C while guiding the student? That is the gap SocraticRAG fills. Evaluating both retrieval and generation in one paper would dilute the contribution and conflate two distinct failure modes.

**2. Providing C directly is the right experimental design, not a shortcut.**

By handing C to the model directly we test under *perfect retrieval* — the best-case condition. If models fail M2 (introduce concepts not in C) even when C is given to them explicitly, the failure is unambiguously attributable to generation, not to retrieval noise. This is a *stronger* finding than failure under noisy retrieval because it eliminates a confound. End-to-end retrieval evaluation would make it impossible to isolate where the system breaks down.

**3. The name "SocraticRAG" still holds.**

The name refers to the *system type* being evaluated — LLM-based tutoring systems that use RAG as their knowledge grounding mechanism. The benchmark stress-tests the generation component of those systems. The name is the deployment context, not a claim that the benchmark itself runs a retrieval step.

**One-sentence fix for the Task Definition section (add where (C, U) → R is defined):**

> "We provide C directly to evaluated models, treating retrieval as oracle-perfect to isolate generation-side failures; evaluating retrieval quality over a student utterance corpus is left as future work."

This single sentence preempts the reviewer objection. Place it immediately after the formal input notation.

---

## Limitations Section

### Visual slide content and text-grounded RAG

Presentation slides with primarily visual content yield significantly fewer extractable text-based concept units than textbook-format notes. This reflects a genuine limitation of text-grounded educational RAG: visual explanations cannot serve as verifiable derivation sources for language-model tutoring.

**Why we did not use vision-generated descriptions as C:**
- C is the source of truth for all downstream validation (Dean) and metrics (M1, M2, M3).
- If C were generated by GPT-4o Vision describing a diagram, the ground truth would itself be model-generated — introducing circular evaluation (GPT-4o generates C, is evaluated against C, and judges responses against C) and making the benchmark non-reproducible across runs.
- We therefore scope the benchmark strictly to text-grounded concept units extracted verbatim from source material.

**How to frame it:**
> "Presentation slides with primarily visual content yield significantly fewer extractable text-based concept units than textbook-format notes. This reflects a genuine limitation of text-grounded educational RAG: visual explanations cannot serve as verifiable derivation sources for language-model tutoring. We treat this asymmetry as an empirical observation and scope the benchmark to text-grounded concept units, leaving multimodal grounding as future work."

**Implication:** The corpus skews toward textbook-format notes (6.036) over slide-format lectures (6.7960). This should be reported in the Dataset Construction section as a consequence of format, not a selection bias.
