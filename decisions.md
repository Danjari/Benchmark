# SocraticRAG — Open Decisions & Issues Log

Each version entry documents what was surfaced on that date: issues flagged, decisions pending, and items that need professor approval or further research before the plan is finalized.

---

## Version 1.0 — 2026-05-11

### STATUS: In review. Nothing is built. This is the plan-stage stress test.

---

### A. Citation Issues (Need Professor Sign-Off)

**A1. EULER and Ilkou et al. are workshop papers**
Both of the primary sources used to establish the evaluation gap are workshop papers, not peer-reviewed conference papers.
- EULER (Bonino et al., 2024) is a 7-page paper from the AIxEDU workshop at AIxIA 2024.
- Ilkou et al. (2024) is a 5-page kick-starter / position paper from an ISWC 2024 special session workshop.
*Decision needed:* These citations are accurate and the quotes are real. But their authority is limited. Should the proposal downgrade them to "prior work calling for this research" rather than treating them as empirical findings? Recommended: yes. The paper should rely on MathTutorBench and SocraticLM (both top-tier venues) as the primary evidence, and treat EULER and Ilkou as supporting voices.

**A2. Lefton et al. (2025) is a 6-page AAAI workshop paper about library taxonomy, not educational tutoring**
The paper is cited as demonstrating a "Socratic RAG system" for education that lacks faithfulness evaluation. In reality, it's about mapping natural language queries to academic Knowledge Organization Systems for research topic disambiguation. It is not an educational tutoring paper.
*Decision needed:* The citation can stay if reframed correctly: "Socratic RAG systems in adjacent domains also lack faithfulness evaluation." But it cannot be presented as educational precedent without misleading reviewers.

**A3. Discerning Minds (Liu et al., 2025) is an August 2025 arXiv preprint**
ArXiv ID 2508.06583 = posted August 2025. If EMNLP submission deadline is before August 2025, this paper technically does not exist yet at submission time and cannot be cited.
*Decision needed:* What is the actual EMNLP submission deadline? If it's after August 2025, fine. If not, the four cognitive states taxonomy needs a different primary source (SocraticLM has six cognitive types; another source may exist).

**A4. Hu et al. (2025) CoT motivation does not transfer**
The 31.2% hallucination reduction cited to motivate Chain-of-Thought prompting in Phase 3 comes from a paper about multimodal visual reasoning on images (fine-grained physical activities), not text-based educational RAG.
*Decision needed:* Replace with Wei et al. (2022) "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" (NeurIPS 2022), which is the canonical CoT paper validated across text tasks. Hu et al. can be retained as a brief contextual note, not a motivation.

**A5. "Pearson p = 0.78" notation**
EULER literally writes "Pearson correlation (p=0.78)" but uses "p" to mean Pearson's r (correlation coefficient), not a p-value. This is the source paper's own non-standard notation.
*Decision needed:* When citing this in SocraticRAG, clarify: "Pearson's r = 0.78 (reported as p=0.78 in the original paper)." This prevents readers from misreading it as a p-value (which would mean "barely significant at p<0.05 would be a stronger threshold").

---

### B. Methodology Issues (Need Resolution Before Writing)

**B1. Gold standard: who writes the gold Socratic responses?**
The proposal says "expert educators draft the Golden Socratic Response (R₀ₙₑˣ)." This implies professors WRITE the gold responses. The working plan is that LLMs generate candidate responses and professors review a subset to validate them.
These are methodologically different:
- Option A (as written): professors author all gold responses. Strong gold standard. Expensive and slow.
- Option B (working plan): LLMs generate responses, professors validate a subset. Faster. But: is this a "gold standard" or a "silver standard with spot-checking"?
- Option C (hybrid): LLMs generate candidates, professors select and lightly edit the best one per scenario. Middle ground.
*Decision needed:* Which option? The answer changes how Phase 1 is written and how credibility is claimed for the gold standard. Option B or C is more honest and realistic. The paper's current framing (Option A) is not what will actually happen.

**B2. Metric 2 NLI step is underspecified**
The proposal says "use NLI to verify whether each premise implicit in the model's question is entailed by C." NLI models are trained on declarative sentence pairs; they cannot directly process interrogative forms.
The actual mechanism needs two steps:
1. Use an LLM to extract the declarative presuppositions embedded in the Socratic question (e.g., "What happens when pressure increases?" → "The system involves pressure as a variable").
2. Check each presupposition against C using an NLI model or LLM entailment check.
This adapts the FActScore methodology (Min et al., 2023, EMNLP) to interrogative text, which is the novel contribution.
*Decision needed:* Confirm this two-step approach is the intended design. Then rewrite Metric 2 to state it explicitly. Add FActScore as the methodological ancestor.

**B3. Self-enhancement bias: GPT-4o as both evaluated model and judge**
The benchmark evaluates GPT-4o as one of the models AND uses LLM-as-judge for all three metrics (where GPT-4o is the natural choice as judge given EULER's validation). MT-Bench (Zheng et al., 2024) documents that LLMs favor their own outputs when used as judges (self-enhancement bias).
*Decision needed:* Propose a bias-mitigation strategy. Options:
- Use Claude as judge when evaluating GPT-4o outputs, and GPT-4o when evaluating Claude outputs.
- Use a single judge (e.g., GPT-4o) consistently and acknowledge the limitation.
- Use two judges and report agreement.
This needs to be stated in the experimental design section.

**B4. Dataset size is not specified anywhere in the proposal**
EMNLP reviewers will ask in round one. No number is given for: number of document chunks, number of scenarios, number of interactions.
*Decision needed:* Commit to a number. Preliminary recommendation: 50-100 chunks across 5-10 courses and 3-4 subject domains, 4 cognitive states per chunk = 200-400 annotated scenarios, 1-2 utterances per scenario = 400-800 total benchmark items.

**B5. "Accurate" and "Comprehension" cognitive states overlap**
The proposal defines: accurate = "correct understanding" and comprehension = "explicit understanding." These are nearly identical. No operational distinction is given.
*Decision needed:* Either sharpen the distinction (e.g., accurate = student answers correctly without prompting; comprehension = student explicitly restates the concept correctly after being taught) or collapse them into one state. Verify that Discerning Minds (Liu et al., 2025) defines them distinctly in their paper — if they do, cite their definition directly.

**B6. Formal task notation has an error**
The paper writes the constraint as: R ∩ ¬sol ≠ ∅
This says "R shares content with the non-solution," which is trivially true for almost any response and does not capture "R does not reveal the answer."
The correct formal expression of the constraint is: R ⊬ sol (R does not entail the solution).
*Decision needed:* Fix the notation before sharing the proposal with professors.

**B7. The Dean agent role is unspecified for non-math domains**
SocraticLM's Dean-Teacher-Student pipeline was designed for math problems where it's clear whether a student utterance is "derivable from the problem." For lecture slide PDFs on topics like neural networks or supply chain economics, "pedagogically plausible" is harder to define.
*Decision needed:* How will the Dean agent's rejection criterion be defined for multi-domain content? This needs a brief paragraph in the methodology.

---

### C. Corpus Issues (Need Resolution)

**C1. Andrew Ng's Coursera materials may not be usable**
Coursera's Terms of Service prohibit bulk extraction of course materials for use in third-party research datasets. The materials are copyrighted by the instructors and Coursera.
*Decision needed:* Replace with MIT OpenCourseWare (CC BY-NC-SA 4.0, confirmed free for non-commercial research use) and/or LibreTexts (used by the TutorChat dataset, also CC-licensed). MIT OCW includes AI/ML, math, biology, physics, and economics courses — sufficient for multi-domain coverage.

**C2. SynapsEd appears three times in the proposal without a citation**
The proposal references "the SynapsEd ingestion pipeline" as the corpus backbone. SynapsEd is your capstone project (NYUAD 2025). It has no published paper.
*Decision needed:* Either (a) describe the pipeline as "our own OCR + semantic chunking pipeline, inspired by prior RAG work" without naming SynapsEd (avoids reviewers asking for a citation), or (b) cite the capstone document as an unpublished technical report if EMNLP allows that. Professors should weigh in on which is appropriate.

---

### D. Model Availability Issues

**D1. LearnLM public access**
LearnLM is Google's educational LLM. It is not publicly available for unrestricted research use.
*Decision needed:* Either confirm API or model access has been arranged, or remove LearnLM from the evaluated models list and add a different open-weight educational model.

**D2. EULER model public availability**
The proposal cites EULER as "the only fine-tuned Socratic model with a publicly available pipeline and evaluation rubric." The code is on GitHub (confirmed: https://github.com/GiovanniGatti/socratic-llm). Whether the fine-tuned weights are released needs verification.
*Decision needed:* Check the EULER GitHub repo to confirm the fine-tuned Phi-3 model weights are released, not just the training code.

---

### E. Validation Design Issues

**E1. Phase 4 human validation: 3 expert educators vs. "one or two professors"**
The proposal requires three expert educators for Phase 4 human validation (500 generated interactions, rated by three annotators blind to model identity). The current team is one or two professors.
*Decision needed:* Confirm whether three annotators can be recruited. If not, two annotators with an adjudication process for disagreements is a defensible alternative. Cohen's Kappa works with two raters.

**E2. Target correlation threshold (Spearman ρ > 0.7)**
The proposal sets ρ > 0.7 as the threshold for validating the automated metrics. This is borrowed from EULER's Pearson r = 0.78. If SocraticRAG's automated metrics achieve ρ < 0.7, the benchmark's credibility as an automated evaluation tool is undermined.
*Decision needed:* Have a plan for what to report if the threshold is not met. (It would still be a finding — it would mean the task requires human evaluation — but it needs to be framed as a discovery, not a failure.)

---

### F. EMNLP-Specific Issues

**F1. Submission deadline and timeline**
The proposal targets EMNLP. The 10-day window to finalize the plan is clear. But the full paper writing, dataset construction, model evaluation, and human validation cannot all happen in 10 days.
*Decision needed:* Is this targeting EMNLP 2025 (submission likely May-June 2025) or EMNLP 2026? The answer changes everything about the timeline and what "ready" means. If EMNLP 2025, the 10 days covers only the research proposal and literature review, not the actual benchmark. That is fine and should be stated clearly to professors.

**F2. Author list and affiliation**
Not yet specified in the proposal.
*Decision needed:* Confirm author list (student + professors as co-authors or advisors?) and NYUAD affiliation. EMNLP requires this at submission.

---

---

## Version 1.1 — 2026-05-11

### STATUS: All decisions resolved. Changes applied to benchmark paper.md, sources.md, and decisions.md.

---

### A. Citation Issues — RESOLVED

**A1. EULER and Ilkou et al. are workshop papers → RESOLVED**
EULER and Ilkou are downgraded to supporting voices. MathTutorBench (EMNLP 2025 Oral) and SocraticLM (NeurIPS 2024) are the primary empirical authorities. EULER is still cited for its validated LLM-as-judge rubric and the topic-drift finding. Ilkou is still cited for its explicit gap statement ("do not include evaluation metrics about the quality of the retrieved documents nor human aspects").

**A2. Lefton et al. (2025) is about library taxonomy, not educational tutoring → RESOLVED**
Reframed throughout the paper as "Socratic RAG in information retrieval contexts (academic knowledge organization system disambiguation)." The paper itself labels itself "work in progress." It is cited as confirming the systemic absence of faithfulness evaluation beyond educational settings, not as educational precedent.

**A3. Discerning Minds (Liu et al., 2025) is an August 2025 arXiv preprint → RESOLVED**
The paper is arXiv v2, dated September 29, 2025. Safe to cite for EMNLP 2026. The v2 date post-dates the v1 deposit of August 2025 — this is a revised and updated version, not just the initial preprint.

**A4. Hu et al. (2025) CoT motivation does not transfer → RESOLVED**
Hu et al. removed as CoT motivation throughout. Replaced with Wei et al. (2022) "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" (NeurIPS 2022, arXiv:2201.11903) as the canonical CoT citation. The paper now cites Wei et al. for CoT rationale in Phase 3. Note: the 31.2% figure from SocraticLM refers to a fine-tuning ablation (accuracy drop when removing problem-solving data), not a hallucination reduction claim — this figure does not appear in the paper at all now.

**A5. "Pearson p = 0.78" notation → RESOLVED**
Fixed throughout the paper to: "Pearson r = 0.78 (reported as p = 0.78 in the original paper, non-standard notation)." All four occurrences updated.

---

### B. Methodology Issues — RESOLVED

**B1. Gold standard: who writes the gold Socratic responses? → RESOLVED: Option C (hybrid)**
Expert educators review LLM-generated candidates and select or lightly revise the best response per scenario. This is the silver-to-gold pipeline. It is now the stated methodology in both Section 2.1 and Phase 1. This approach is validated by both MathTutorBench (Bridge dataset = expert revision of LLM-generated novice teacher responses) and Discerning Minds (LLM responses + human annotation/revision). Frame it as the principled industry standard, not a compromise.

**B2. Metric 2 NLI step is underspecified → RESOLVED**
The paper now explicitly describes the two-step mechanism: (1) LLM extracts declarative presuppositions embedded in the Socratic question, (2) NLI/entailment check verifies each presupposition against C. FActScore (Min et al., 2023, EMNLP) is the methodological ancestor — the same atomic decomposition + entailment mechanism, adapted from declarative to interrogative outputs.

**B3. Self-enhancement bias: GPT-4o as both evaluated model and judge → RESOLVED**
Strategy: cross-judge protocol. When evaluating GPT-4o outputs, use Claude as judge. When evaluating Claude outputs, use GPT-4o as judge. When evaluating open-weight models, use either. This is stated in the experimental design. MT-Bench (Zheng et al., 2024) is cited as the paper that identifies and quantifies self-enhancement bias.

**B4. Dataset size not specified → RESOLVED**
Committed to: 50–100 document chunks across 5–10 courses and 3–4 subject domains, 4 cognitive states per chunk = 200–400 annotated scenarios, 1–2 utterances per scenario = 400–800 total benchmark items. This is publishable and well-precedented (MathTutorBench = 9,125 items across 7 tasks; Discerning Minds = 180 scenarios; EULER = 100 test samples).

**B5. "Accurate" and "Comprehension" cognitive states overlap → RESOLVED**
These are two orthogonal axes confirmed from Discerning Minds (v2, Table 1):
- Answer-correctness axis: accurate (correct answer) vs. erroneous (wrong answer)
- Metacognitive-expression axis: comprehension (expresses understanding) vs. confusion (expresses uncertainty)
A student can be accurate but confused (correct answer, uncertain why) — these are distinct states. All four are operationally distinct. Keep all four, cite Discerning Minds Table 1 for the definitions.

**B6. Formal task notation has an error → RESOLVED**
Fixed: `R ∩ ¬sol ≠ ∅` → `R ⊬ sol` (R does not entail the solution). The corrected notation appears in the Phase 1 task formulation.

**B7. The Dean agent role is unspecified for non-math domains → RESOLVED**
SocraticLM's three Dean criteria are domain-agnostic: (1) Socratic questioning style, (2) pointing out student errors, (3) teacher-like language. SocraticRAG adds criterion (4): the question draws only on concepts present in retrieved chunk C. This fourth criterion makes the Dean the retrieval-faithfulness gatekeeper, which is the novel contribution. No domain-specific logic needed.

---

### C. Corpus Issues — RESOLVED

**C1. Andrew Ng's Coursera materials may not be usable → RESOLVED**
Replaced throughout with MIT OpenCourseWare (CC BY-NC-SA 4.0) and LibreTexts. MIT OCW includes AI/ML (6.034, 6.036), math, biology, physics, economics — sufficient for multi-domain coverage. LibreTexts is the source used by TutorChat (Chevalier et al., 2024), confirming it as accepted practice in the field.

**C2. SynapsEd appears three times without a citation → RESOLVED**
All three occurrences replaced. The pipeline is now described as "our own OCR and semantic chunking pipeline" (Phase 1 and Section 2.1) or removed entirely (corpus rationale sentence). No unpublished project is cited by name.

---

### D. Model Availability Issues — RESOLVED

**D1. LearnLM public access → RESOLVED**
LearnLM is available as **learnlm-1.5-pro-experimental** via Google AI API. It is evaluated in MathTutorBench (confirmed from full PDF). Include it in the model list with this specific API identifier noted.

**D2. EULER model public availability → RESOLVED**
EULER fine-tuned weights status is uncertain. Replaced in the models evaluated list with **Qwen2.5-7B-SocraticLM** (CogBase-USTC/SocraticLM on HuggingFace) — publicly available fine-tuned weights, evaluated in both MathTutorBench and Discerning Minds as a baseline, making it well-known in the field.

---

### E. Validation Design Issues — RESOLVED

**E1. Phase 4 human validation: 3 experts vs. "one or two professors" → RESOLVED**
Two professors are confirmed as collaborators. Two-annotator design with adjudication protocol for disagreements is a defensible alternative. Cohen's Kappa (κ) works with two raters. Phase 4 text updated to reflect two annotators + adjudication.

**E2. Target correlation threshold (Spearman ρ > 0.7) → RESOLVED**
Keep ρ > 0.7 as the target. If not met, frame it as a discovery (the task genuinely requires human evaluation at scale) rather than a failure. The paper already includes this framing in Phase 4 Success Criteria.

---

### F. EMNLP-Specific Issues — RESOLVED

**F1. Submission deadline and timeline → RESOLVED**
Targeting EMNLP 2026. The current 10-day window covers the research proposal and literature review only, not the full benchmark. This is explicitly acknowledged. The proposal is a plan-stage document for professor review before full execution begins.

**F2. Author list and affiliation → RESOLVED**
Two professors confirmed as collaborators/co-authors. NYUAD affiliation. Author list to be finalized with professors before submission.

---

*Version 1.1 closes all open decisions from Version 1.0. Changes applied 2026-05-11 to benchmark paper.md, sources.md, and this document.*
