# SocraticRAG — Sources & Research Log

Organized by role in the paper. Each entry includes: citation, link, verification status, and a paragraph explaining its exact relevance and how it should be used.

---

## 1. Core Gap Papers (Motivating the Benchmark)

### 1.1 RAGAS — Es et al. (2024)
**Full citation:** Es, S., James, J., Anke, L. E., & Schockaert, S. (2024). RAGAS: Automated evaluation of retrieval augmented generation. *EACL 2024 (Demo Track)*.
**Link:** https://aclanthology.org/2024.eacl-demo.16
**Verification:** FULLY VERIFIED (complete PDF read).
**Role in paper:** Establishes the dominant RAG faithfulness framework. Faithfulness score F = |V|/|S| where S = set of atomic statements extracted from the generated answer, V = subset supported by retrieved context. The mechanism structurally breaks when the output is an interrogative (Socratic question): the statement extraction step yields no atomic declarative claims to verify, making F undefined or trivially zero. Validated exclusively on WikiEval — 50 Wikipedia pages with factual declarative Q&A (e.g., "Who directed Oppenheimer?"). No interrogative output format is addressed anywhere in the paper. This confirms SocraticRAG's Metric 2 cannot use RAGAS and must propose a presupposition-extraction adaptation.
**Watch out:** Confirmed from full text — WikiEval is purely declarative QA, 50 Wikipedia pages. The RAGAS mechanism produces a vacuous score for any question-form output. No competing faithfulness framework for interrogative outputs exists in the literature.

---

### 1.2 EULER — Bonino et al. (2024)
**Full citation:** Bonino, G., Sanmartino, G., Gatti Pinheiro, G., Papotti, P., Troncy, R., & Michiardi, P. (2024). EULER: Fine tuning a large language model for Socratic interactions. *Workshop on AI for Education (AIxEDU) @ AIxIA 2024*.
**Link:** https://ceur-ws.org/Vol-3879/AIxEDU2024_paper_26.pdf
**Verification:** FULLY VERIFIED (complete PDF read).
**Role in paper:**
- Provides the validated LLM-as-judge rubric for Socratic quality: four criteria (question presence, on_topic 1-5, helpful 1-5, reveal_answer boolean).
- The "reveal_answer" criterion is the direct basis for SocraticRAG's Metric 1 (Socratic Adherence).
- Validated against 2 human annotators on 100 samples, Pearson r = 0.78 (paper writes "p=0.78" — this is their notation for Pearson's r, not a p-value. Cite it exactly as they write it but note the non-standard notation in your methods section).
- CRITICAL: EULER's judge contains NO retrieval faithfulness criterion. It only checks whether the question reveals the answer, is on-topic, and is helpful. There is no check whether the question's premises are grounded in any retrieved document. This is the gap SocraticRAG fills.
- EULER explicitly identifies topic drift as its main limitation (Section 7): "interactions can start on a specific subject and move into a different topic loosely connected from the initial one after a few iterations." This is empirical evidence that Socratic LLMs drift even when fine-tuned, motivating the need for a faithfulness constraint.
- NOTE: This is a workshop paper (7 pages). Do not over-weight its authority. It is best used as "prior work providing the validated rubric we adapt" rather than as a major empirical study.
- Validated on 100 test samples per dataset. Training sets: 500-650 examples.

---

### 1.3 SocraticLM — Liu, J. et al. (2024)
**Full citation:** Liu, J. et al. (2024). SocraticLM: Exploring socratic personalized teaching with large language models. *NeurIPS 2024*.
**Link:** https://proceedings.neurips.cc/paper_files/paper/2024/hash/9bae399d1f34b8650351c1bd3692aeae-Abstract-Conference.html
**Verification:** FULLY VERIFIED (complete PDF read).
**Role in paper:**
- Provides the Dean-Teacher-Student multi-agent pipeline for generating Socratic dialogues, which SocraticRAG adapts for its seed generation step.
- Demonstrates that GPT-4 fails at Socratic teaching even when explicitly instructed, directly providing solutions rather than guiding questions.
- Contains SocraTeach: 35,000 multi-round dialogues (208K single-round exchanges) on math problems (GSM8K and MAWPS datasets).
- The Dean agent's three rejection criteria are **domain-agnostic**: (1) Socratic questioning style (avoids giving answers directly), (2) points out student errors, (3) uses teacher-like language. SocraticRAG adds a fourth criterion specific to RAG: (4) the question draws only on concepts present in chunk C.
- CRITICAL: The "31.2% hallucination reduction" figure does NOT come from this paper. The 31.2% in SocraticLM is a fine-tuning ablation: removing problem-solving data from training causes a 31.2%/9.7% accuracy drop on GSM8K/MAWPS. It measures accuracy loss in fine-tuning, not hallucination reduction in inference. Do not cite this as a CoT/hallucination result. Use Wei et al. (2022) for CoT motivation instead.
- The silver-to-gold gold standard methodology in SocraticLM: human professors authored responses via revision of LLM-generated candidates — direct precedent for SocraticRAG's Option C hybrid approach.
- NOTE: The dataset is math-only. SocraticRAG's corpus spans multiple domains, which is a key differentiator.
- NOTE: SocraticLM uses six student cognitive states. SocraticRAG uses four from Discerning Minds because those four (accurate/erroneous/comprehension/confusion) form two clean orthogonal axes (answer-correctness vs. metacognitive-expression), making controlled evaluation cleaner. The paper should state this justification explicitly.

---

### 1.4 MathTutorBench — Macina et al. (2025)
**Full citation:** Macina, J. et al. (2025). MathTutorBench: A benchmark for measuring open-ended pedagogical capabilities of LLM tutors. *EMNLP 2025 (Oral)*.
**Link:** https://arxiv.org/abs/2502.18940
**Verification:** FULLY VERIFIED (complete PDF read, EMNLP 2025 Oral).
**Role in paper:**
- The strongest precedent: EMNLP accepts holistic pedagogical benchmarks as oral papers.
- Exact benchmark size: **9,125 items across 7 tasks** (Socratic Questioning, Mistake Identification, Providing Feedback, Scaffolding, Error Correction, Subgoal Decomposition, Guided Discovery).
- Key confirmed quote: "subject expertise does not immediately translate to good teaching."
- Key confirmed quote: "tutoring appears to become more challenging in longer dialogs."
- Explicitly limited to math (GSM8K problems) and entirely retrieval-free — the gap SocraticRAG fills.
- Confirms that teacher-created ground truth is essential: the Bridge dataset is created by expert revision of novice teacher LLM-generated responses — direct precedent for SocraticRAG's silver-to-gold methodology.
- Confirms BLEU/ROUGE are "noisy and unreliable" for open-ended tutoring evaluation.
- **NEW GAP ARGUMENT**: MathTutorBench evaluates its Socratic Questioning task using BLEU-4 despite arguing BLEU is unreliable. This internal contradiction motivates SocraticRAG's purpose-built three-axis metric design.
- **CORRECTION on "Leaked Solution (%)"**: This exact phrase does NOT appear as a named metric in MathTutorBench. The analogous concept appears as a criterion inside the Scaffolding Score reward model (does the response reveal the solution?). Cite it as "a revealing-answer criterion within the Scaffolding Score" not as "Leaked Solution (%)."
- LearnLM confirmed evaluated in MathTutorBench: available as **learnlm-1.5-pro-experimental** via Google AI API.

---

### 1.5 Ilkou et al. (2024) — Hybrid Evaluation of Socratic Dialogue
**Full citation:** Ilkou, E., Linzbach, S., & Wallat, J. (2024). Hybrid evaluation of Socratic dialogue for teaching. *ISWC 2024 Special Session on Harmonising Generative AI and Semantic Web Technologies*.
**Link:** https://ceur-ws.org/Vol-3953/363.pdf
**Verification:** FULLY VERIFIED (complete PDF read).
**Role in paper:** The key quote is real and confirmed: "Although RAG models rely on the quality of the retrieved documents for question-answering, the implementations do not include evaluation metrics about the quality of the retrieved documents nor human aspects." This directly motivates SocraticRAG's Metric 2.
**CRITICAL CORRECTION NEEDED:** This is a 5-page kick-starter/position paper from a workshop special session. It does NOT implement RAG for Socratic tutoring. It proposes a KG-based (Knowledge Graph) hybrid system with a proxy LLM, not RAG. The paper calls for future work; it is not an empirical study. Using it as primary gap evidence overstates its authority. Recommended framing: "Ilkou et al. (2024) identify this gap in a position paper calling for hybrid evaluation approaches, noting that existing RAG implementations 'do not include evaluation metrics about the quality of the retrieved documents nor human aspects'."

---

### 1.6 Lefton et al. (2025) — A Socratic RAG Approach
**Full citation:** Lefton, L. et al. (2025). A Socratic RAG approach to research topic disambiguation. *AAAI 2025 Workshop on Knowledge Axiomatization*.
**Link:** https://arxiv.org/abs/2502.15005
**Verification:** FULLY VERIFIED (complete PDF read). 6-page work-in-progress paper.
**Role in paper:** Demonstrates that Socratic RAG systems in information retrieval contexts also lack faithfulness evaluation, confirming the systemic absence of this component beyond educational settings.
**CORRECTION APPLIED:** This paper is about academic Knowledge Organization System (KOS) disambiguation — mapping natural language queries to library taxonomy categories to help researchers find research topics. It is NOT about educational tutoring. The paper explicitly labels itself "work in progress." The Socratic dialogue helps researchers disambiguate research topics, not teach students. Framing in the paper has been updated: cited as "information retrieval contexts (academic knowledge organization system disambiguation)" rather than as educational precedent.
**Why still useful:** It confirms that the gap in faithfulness evaluation is systemic, not limited to the educational domain. Any Socratic RAG system, regardless of domain, currently ships without faithfulness evaluation.

---

### 1.7 Discerning Minds — Liu, Y. et al. (2025)
**Full citation:** Liu, Y. et al. (2025). Discerning minds or generic tutors? Evaluating LLMs as adaptive instructional agents. *arXiv preprint arXiv:2508.06583*.
**Link:** https://arxiv.org/abs/2508.06583
**Verification:** FULLY VERIFIED (complete PDF read, v2 dated September 29, 2025).
**Role in paper:** Provides the GuideEval framework (Perception-Orchestration-Elicitation) and the four cognitive state taxonomy that SocraticRAG adopts. Shows LLMs fail under negative student states (confusion, requiring redirection).
**Four cognitive states CONFIRMED with operational definitions:**
- **Accurate**: student gives a correct answer (answer-correctness axis = positive)
- **Erroneous**: student gives an incorrect answer (answer-correctness axis = negative)
- **Comprehension**: student explicitly expresses understanding (metacognitive-expression axis = positive)
- **Confusion**: student explicitly expresses uncertainty or misunderstanding (metacognitive-expression axis = negative)
- The two axes are **orthogonal**: a student can be accurate (correct answer) but confused (uncertain why), or erroneous (wrong answer) but show comprehension (knows what they got wrong). All four states are operationally distinct.
**89-97% agreement CONFIRMED from Table 3:** GPT-4o judge achieves 89-97% agreement with human scoring across all three POE phases (Perception, Orchestration, Elicitation). This directly supports SocraticRAG's LLM-as-judge validation design.
**Bloom's taxonomy operationalized:** Elicitation scoring uses E-Level 1 (recall), E-Level 2 (application), E-Level 3 (higher-order synthesis). This is the direct NLP operationalization needed for SocraticRAG Metric 3 — cite GuideEval's Elicitation rubric from Table 1.
**Dataset:** 180 scenarios, 4 cognitive states per scenario, evaluated on GPT-4o, Claude 3.5 Sonnet, and Qwen2.5-7B-SocraticLM (the model SocraticRAG uses in its model list).
**EMNLP 2026 safety:** v2 is dated September 29, 2025. Safe to cite for EMNLP 2026 submission.

---

### 1.8 Hu et al. (2025) — Socratic Questioning for Multimodal Reasoning
**Full citation:** Hu, W. et al. (2025). Socratic questioning: Learn to self-guide multimodal reasoning in the wild. *arXiv preprint arXiv:2501.02964*.
**Link:** https://arxiv.org/abs/2501.02964
**Verification:** Verified (abstract fetched).
**Role in paper (AS PROPOSED):** Used to motivate CoT prompting in Phase 3.
**CORRECTION NEEDED:** The 31.2% hallucination reduction is from a multimodal LLM paper about visual reasoning on fine-grained activity images (custom CapQA dataset, 1,000 images). This is a completely different setting from text-based educational RAG. The transfer is not justified. RECOMMENDATION: Drop this citation as CoT motivation. Instead cite Wei et al. (2022) "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" (arXiv:2201.11903) for CoT, and include a disclaimer that CoT is tested as a prompting paradigm in our setting, with results compared empirically rather than assumed from prior work.

---

## 2. Papers to Add (Not Yet in the Proposal)

### 2.1 Wei et al. (2022) — Chain-of-Thought Prompting
**Full citation:** Wei, J. et al. (2022). Chain-of-thought prompting elicits reasoning in large language models. *NeurIPS 2022*.
**Link:** https://arxiv.org/abs/2201.11903
**Verification:** Verified (abstract fetched). Key finding: intermediate reasoning steps improve complex reasoning across arithmetic, commonsense, symbolic tasks.
**Why to add:** Replace Hu et al. as the citation motivating CoT in Phase 3. Wei et al. is the canonical CoT paper, broadly validated across text tasks. It establishes CoT as a prompting paradigm without making domain-specific hallucination reduction claims that don't transfer.

---

### 2.2 Zheng et al. (2024) — MT-Bench and LLM-as-Judge
**Full citation:** Zheng, L. et al. (2024). Judging LLM-as-a-judge with MT-bench and chatbot arena. *NeurIPS 2024*.
**Link:** https://arxiv.org/abs/2306.05685
**Verification:** Verified (abstract fetched). Full PDF added to cited_papers_full/ but requires poppler-utils to render (not installed). Summary from prior abstract verification below.
**Key confirmed findings:**
- MT-Bench: 80 multi-turn conversation questions across 8 categories (writing, roleplay, extraction, reasoning, math, coding, knowledge I, knowledge II)
- GPT-4 as judge achieves >80% agreement with human evaluations on single-answer grading
- Documents three systematic LLM-as-judge biases: position bias (favors first response), verbosity bias (favors longer responses), self-enhancement bias (LLMs favor their own outputs when used as judges — GPT-4 prefers GPT-4-generated answers)
- Chatbot Arena: 30K+ crowd-sourced human preference votes confirming rankings
**Role in paper:**
- Primary validation for using LLM-as-judge across Metrics 1, 2, and 3 (>80% human agreement is the bar SocraticRAG targets)
- Self-enhancement bias finding **directly motivates** the cross-judge protocol in SocraticRAG: Claude judges GPT-4o outputs, GPT-4o judges Claude outputs. Without this protocol, a GPT-4o judge evaluating GPT-4o responses would systematically inflate GPT-4o scores.
- Cite in the experimental design section when introducing the cross-judge strategy.

---

### 2.3 FActScore — Min et al. (2023)
**Full citation:** Min, S. et al. (2023). FActScore: Fine-grained atomic evaluation of factual precision in long form text generation. *EMNLP 2023*.
**Link:** https://arxiv.org/abs/2305.14251
**Verification:** Verified (abstract fetched + full PDF added to cited_papers_full/). PDF requires poppler-utils to render interactively; summary based on prior abstract verification and published EMNLP findings.
**Key confirmed findings:**
- Proposes a two-step factual precision framework: (1) decompose long-form generated text into a list of atomic facts (minimal, indivisible claims), (2) verify each atomic fact independently against a knowledge source via retrieval + entailment.
- Evaluated on biography generation (Wikipedia as knowledge source). Automated pipeline achieves <2% error rate compared to human annotation — establishing that LLM-based decomposition + NLI entailment is a reliable automatic faithfulness evaluation mechanism.
- Key insight: standard sentence-level or passage-level metrics conflate supported and unsupported claims. Atomic decomposition makes each fact independently verifiable, enabling fine-grained precision scoring.
- Published at EMNLP 2023 (main conference, not workshop).
**Role in paper:**
- **Direct methodological ancestor of Metric 2** (Retrieval Faithfulness). SocraticRAG's two-step NLI process is an adaptation: instead of decomposing declarative sentences into atomic facts, we decompose an interrogative Socratic question into its embedded declarative presuppositions (what the question implicitly asserts), then apply entailment checking against context C.
- The key adaptation — and the novel contribution — is that FActScore was designed for declarative text only. Socratic questions are interrogative: they do not state facts, they presuppose them. SocraticRAG's Metric 2 is the first adaptation of FActScore's atomic decomposition mechanism to interrogative pedagogical outputs.
- Cite in Metric 2 methodology section: "Following FActScore (Min et al., 2023), we apply atomic decomposition and entailment checking. However, unlike FActScore's declarative setting, we first extract the declarative presuppositions embedded in the Socratic question before applying entailment."
**Watch out:** FActScore requires a knowledge source for retrieval during verification. In SocraticRAG, context C is fixed (the retrieved chunk given to the model) — this simplifies the pipeline: no retrieval step needed, just entailment against the known C. Mention this as a simplification advantage over FActScore's general setup.

---

### 2.4 MathDial — Macina et al. (2023)
**Full citation:** Macina, J., Daheim, N., Chowdhury, S. P., Sinha, T., Kapur, M., Gurevych, I., & Sachan, M. (2023). MathDial: A dialogue tutoring dataset with rich pedagogical properties grounded in math reasoning problems. *arXiv preprint arXiv:2305.14536*.
**Link:** https://arxiv.org/abs/2305.14536
**Verification:** Confirmed via EULER paper (cited as [11]). 3,000 one-shot teacher-student interactions. Teacher questions written by humans, student solutions LLM-generated.
**Why to add:** A related prior dataset with teacher-student math tutoring interactions. Useful for baseline comparison and for contextualizing SocraticRAG's dataset size. MathDial is math-only and not RAG-grounded — two dimensions SocraticRAG improves on.

---

### 2.5 TutorEval / TutorChat — Chevalier et al. (2024)
**Full citation:** Chevalier, A. et al. (2024). Language models as science tutors. *ICML 2024*.
**Link:** https://arxiv.org/abs/2402.11111
**Verification:** FULLY VERIFIED (complete PDF read, all 26 pages, ICML 2024 published paper — not arXiv preprint as previously noted).
**Key confirmed findings:**
- **TutorEval**: 834 questions across 5 subject domains, created by 17 expert STEM annotators (Ph.D. students and researchers). Questions are grounded in LibreTexts textbook chapters. Evaluation measures whether models can answer complex, multi-step science questions — not Socratic quality.
- **TutorChat**: 78,000 synthetic multi-turn tutoring dialogues from 1,685 LibreTexts textbooks (78K chapters). GPT-4 generated. The teacher role gives direct explanations and answers — this is **NOT Socratic teaching**; the teacher explains, not guides.
- **LibreTexts corpus**: 1,685 textbooks spanning all academic domains (STEM + humanities). CC-licensed. Used as the raw source for both the benchmark questions and the synthetic dialogues.
- **No retrieval faithfulness evaluation anywhere in the paper.** The system prompts include the textbook chapter as context, but there is no metric for whether the model's response stays grounded in that chapter. This is the exact gap SocraticRAG fills.
- **Evaluation metrics**: correctness of the answer (judged by GPT-4), not pedagogical quality (no Socratic adherence, no faithfulness check, no cognitive state targeting).
**Role in paper:**
- Confirms LibreTexts as a viable multi-domain CC-licensed corpus source — 1,685 textbooks across all academic domains. This directly supports SocraticRAG's corpus decision to use LibreTexts.
- Demonstrates the persistent gap: even when context C is provided to the model (as TutorChat does), no existing work evaluates whether the model stays faithful to it. SocraticRAG is the first to close this.
- Useful for comparison: TutorChat trains on teacher-gives-answers dialogues; SocraticRAG evaluates question-guided Socratic responses. The contrast sharpens the contribution.
- Cite when justifying the LibreTexts corpus and when listing prior educational NLP benchmarks that do not address faithfulness.
**Correction from prior entry:** Previously cited as "arXiv preprint" — it is ICML 2024 (published proceedings). Update any in-text citations accordingly.

---

### 2.6 Kumar & Lan (2024) — Improving Socratic Question Generation
**Full citation:** Kumar, N. A., & Lan, A. (2024). Improving socratic question generation using data augmentation and preference optimization. *arXiv preprint arXiv:2403.00199*.
**Link:** https://arxiv.org/abs/2403.00199
**Verification:** Confirmed via EULER paper (cited as [9]). Directly relevant — the Debugging dataset used by EULER comes from this paper.
**Why to add:** Demonstrates data augmentation + DPO for Socratic question generation. Provides the "rejected answer" taxonomy (irrelevant, direct, premature, repeated) that could inform SocraticRAG's annotation guidelines for what constitutes a failure on Metric 1.

---

### 2.7 MIT OpenCourseWare (Corpus Alternative)
**Link:** https://ocw.mit.edu
**License:** Creative Commons CC BY-NC-SA 4.0 — confirmed.
**Why to add:** Safe, open-licensed alternative to Andrew Ng's Coursera materials for the benchmark corpus. MIT OCW includes AI, ML, computer science, math, biology, and physics courses with lecture notes and slides available for download. Thousands of MIT courses. Non-commercial research use is explicitly permitted.
**Recommendation:** Replace or supplement Andrew Ng's Coursera materials with MIT OCW courses. The corpus can include AI/ML courses (6.034 Artificial Intelligence, 6.036 Introduction to Machine Learning) alongside courses from other domains (biology, physics, economics) to ensure multi-domain coverage. Cite MIT OpenCourseWare as the corpus source with the CC license noted.

---

## 3. Papers Still Needed (To Find)

### 3.1 A paper on question presupposition extraction or NLI applied to interrogative forms
**What we need:** A paper that either (a) extracts the declarative presuppositions/premises embedded in questions, or (b) applies NLI-style entailment checking to non-declarative text. This is the methodological foundation for Metric 2 that is currently missing.
**Where to look:** ACL Anthology, search "presupposition extraction NLP" or "question-grounded NLI" or "implicit claim detection questions"
**Why critical:** Metric 2 currently proposes NLI on question premises without citing any paper that does this. Without a precedent, reviewers will ask why this approach is valid. The FActScore approach (add as 2.3 above) partially covers this by providing the two-step methodology (LLM decompose → NLI check).

### 3.2 A study on LLM self-enhancement bias (GPT-4 judging GPT-4 outputs)
**What we need:** A paper quantifying how much GPT-4 favors its own outputs when used as a judge evaluating competing models.
**Why needed:** GPT-4o is both an evaluated model and the intended judge in this benchmark. MT-Bench (2.2 above) names this bias; we need a paper that quantifies it, so we can propose a bias-mitigation strategy (e.g., using Claude as judge when evaluating GPT-4, and GPT-4 when evaluating Claude).

### 3.3 A Bloom's taxonomy paper with NLP operationalization
**STATUS: RESOLVED.** Discerning Minds (Liu et al., 2025) explicitly operationalizes Bloom's taxonomy for Elicitation scoring via E-Level 1 (recall/remember), E-Level 2 (application/apply), E-Level 3 (higher-order synthesis/analyze-evaluate) in Table 1. This is the direct NLP operationalization needed for Metric 3 — cite GuideEval's Elicitation rubric from Table 1 as the scoring methodology for cognitive depth. No additional paper is needed.

### 3.4 Open educational resources for multi-domain corpus
**What we need:** Confirm that LibreTexts (used by TutorChat) and MIT OCW are appropriate corpus sources with confirmed licensing, and find at least one more source for non-STEM courses (e.g., social science, history) to ensure domain diversity.

---

## 4. Papers to Remove or Reframe

### 4.1 Hu et al. (2025) as CoT motivation
**Action:** Remove as primary CoT citation. Replace with Wei et al. (2022). Hu et al. can be retained as a brief note: "Socratic self-questioning has also reduced hallucinations in multimodal visual reasoning (Hu et al., 2025), though we cannot assume this transfers directly to text-based RAG settings" — framing it as contextual rather than motivating.

---

## 5. Corpus Decision

**Current proposal:** Andrew Ng's course materials (Coursera/deeplearning.ai).
**Problem:** Coursera Terms of Service prohibit bulk extraction of course materials for third-party research datasets. Copyright is held by the instructors and Coursera.
**Recommended alternative:** MIT OpenCourseWare (CC BY-NC-SA) + LibreTexts (various CC licenses, used by TutorChat). Multi-domain coverage: AI/ML, mathematics, biology, chemistry, physics, economics.
**Action needed:** Confirm the MIT OCW and LibreTexts licenses permit research benchmark publication, and select specific courses to form the corpus (aim for 5-10 courses across 3-4 domains).

---

## 6. Dataset Scale Decision

**Reference points from comparable EMNLP benchmarks:**
- MathTutorBench: **9,125 items across 7 tasks** (verified from full PDF)
- MathDial: 3,000 one-shot interactions
- SocraticLM / SocraTeach: 35,000 generated dialogues (208K single-round)
- EULER: 100 test samples, 500-650 training samples (very small)
- Discerning Minds / GuideEval: **180 scenarios, 4 cognitive states** (verified from full PDF)

**Recommended scale for SocraticRAG:**
- Corpus: 50-100 document chunks across 5-10 courses and 3-4 domains
- Student profiles: 4 cognitive states per chunk = 200-400 scenario-profiles
- Student utterances: 1-2 per scenario-profile = 400-800 total utterances
- Gold annotations: all (human educators annotate all scenarios; this is the benchmark)
- Phase 4 human validation: 500 generated interactions as proposed (retain)

**Rationale:** Quality over quantity. SocraticRAG's value is in multi-dimensional grading, not data volume. A well-annotated 500-item benchmark is more credible for EMNLP than a large synthetic one.

---

*Last updated: 2026-05-11. Research ongoing.*
