# SocraticRAG — Sources & Research Log

Organized by role in the paper. Each entry includes: citation, link, verification status, and a paragraph explaining its exact relevance and how it should be used.

---

## 1. Core Gap Papers (Motivating the Benchmark)

### 1.1 RAGAS — Es et al. (2024)
**Full citation:** Es, S., James, J., Anke, L. E., & Schockaert, S. (2024). RAGAS: Automated evaluation of retrieval augmented generation. *EACL 2024 (Demo Track)*.
**Link:** https://aclanthology.org/2024.eacl-demo.16
**Verification:** Partially verified (abstract fetched). Full mechanism requires PDF.
**Role in paper:** Establishes the dominant RAG faithfulness framework. Its claim-decomposition mechanism — breaking answers into atomic declarative statements and checking entailment against retrieved context — structurally breaks when the output is an interrogative (Socratic question). No declarative claims exist to decompose, so the faithfulness score is undefined or vacuous. This is the primary reason SocraticRAG cannot use RAGAS and must propose Metric 2.
**Watch out:** The paper confirms reference-free evaluation and was validated on WikiEval (declarative QA dataset). Confirm from full text that WikiEval is factual Q&A only and that no interrogative output format is addressed.

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
**Verification:** Partially verified (abstract page fetched). Fetch says "six student cognitive types" in the dataset; the proposal adopts four from Discerning Minds instead.
**Role in paper:**
- Provides the Dean-Teacher-Student multi-agent pipeline for generating Socratic dialogues, which SocraticRAG adapts for its seed generation step.
- Demonstrates that GPT-4 fails at Socratic teaching even when explicitly instructed.
- Contains SocraTeach: 35,000 multi-round dialogues (208K single-round exchanges) on math problems.
- NOTE: The dataset is math-only (like MathTutorBench). SocraticRAG's corpus spans multiple domains (lecture slides, PDFs), which is explicitly stated as a differentiator.
- NOTE: SocraticLM uses "six student cognitive types" while Discerning Minds uses four. The proposal uses four (from Discerning Minds). You must explicitly state why you chose Discerning Minds' taxonomy over SocraticLM's in the methodology section.

---

### 1.4 MathTutorBench — Macina et al. (2025)
**Full citation:** Macina, J. et al. (2025). MathTutorBench: A benchmark for measuring open-ended pedagogical capabilities of LLM tutors. *EMNLP 2025 (Oral)*.
**Link:** https://arxiv.org/abs/2502.18940
**Verification:** Partially verified (abstract fetched). Key findings confirmed.
**Role in paper:**
- The strongest precedent: EMNLP accepts holistic pedagogical benchmarks as oral papers.
- Key confirmed finding: "subject expertise does not immediately translate to good teaching."
- Key confirmed finding: "tutoring becomes more challenging in longer dialogs."
- Explicitly limited to math (GSM8K problems) and entirely retrieval-free — the gap SocraticRAG fills.
- Confirms that teacher-created ground truth is essential and that standard metrics (BLEU, ROUGE) are inadequate for open-ended tutoring evaluation.
- Confirms "Leaked Solution (%)" as a central measurable dimension (equivalent to SocraticRAG's Metric 1).
- NOTE: Need to verify from full paper: exact number of benchmark items, specific models evaluated, and exact wording of the statement about retrieval-free limitation.

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
**Verification:** Verified (abstract fetched). Full paper: 6-page workshop paper.
**Role in paper:** Demonstrates a system that combines RAG with Socratic dialogue but includes zero evaluation of whether the Socratic outputs stay faithful to retrieved material.
**CRITICAL CORRECTION NEEDED:** This paper is about research topic disambiguation (mapping natural language queries to academic Knowledge Organization Systems like library taxonomies). It is NOT about educational tutoring. Its Socratic dialogue is about helping researchers find research topics, not about teaching students. The framing in the proposal ("Lefton et al. propose a Socratic RAG system but include no faithfulness evaluation") is accurate but the context implies educational setting. Recommend reframing to: "Beyond educational settings, Lefton et al. (2025) demonstrate that Socratic RAG approaches lack faithfulness evaluation even in information retrieval contexts, confirming the systemic absence of this evaluation component."

---

### 1.7 Discerning Minds — Liu, Y. et al. (2025)
**Full citation:** Liu, Y. et al. (2025). Discerning minds or generic tutors? Evaluating LLMs as adaptive instructional agents. *arXiv preprint arXiv:2508.06583*.
**Link:** https://arxiv.org/abs/2508.06583
**Verification:** Partially verified (abstract fetched). Full paper not read.
**Role in paper:** Provides the GuideEval framework (Perception-Orchestration-Elicitation) and the four cognitive state taxonomy that SocraticRAG adopts. Shows LLMs fail under negative student states (confusion, requiring redirection).
**NOTE:** This is an August 2025 arXiv preprint (ID: 2508.06583). Verify whether it has been accepted anywhere. If submitting to EMNLP 2025, citing an August 2025 preprint may raise questions about timeline. Check submission deadline.
**NOTE:** Fetch confirmed the POE framework but did NOT explicitly confirm all four cognitive states (accurate, erroneous, comprehension, confusion). Must verify from full paper that these exact four states are named.
**NOTE:** The paper says "89-97% agreement between LLM-based and human scoring" for their pedagogical metrics — must verify this claim from full paper, as the proposal relies on it for Phase 4 validation design.

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
**Verification:** Verified (abstract fetched). 80%+ agreement with human evaluations. Identifies position bias, verbosity bias, self-enhancement bias.
**Why to add:** Provides strong validation for the LLM-as-judge methodology used across all three metrics. Also surfaces the self-enhancement bias issue: GPT-4o is both an evaluated model AND a potential judge in this benchmark. This must be addressed in the paper (use a different judge, or report bias-correction). Already cited by EULER [ref 5].

---

### 2.3 FActScore — Min et al. (2023)
**Full citation:** Min, S. et al. (2023). FActScore: Fine-grained atomic evaluation of factual precision in long form text generation. *EMNLP 2023*.
**Link:** https://arxiv.org/abs/2305.14251
**Verification:** Verified (abstract fetched). Breaks text into atomic facts; verified finding that automated model achieves <2% error rate vs. human.
**Why to add:** Direct methodological ancestor of Metric 2. FActScore shows that breaking declarative text into atomic claims and checking entailment is a valid faithfulness evaluation approach. SocraticRAG extends this to interrogative text by first converting the question's embedded premises into declarative claims (via LLM decomposition), then applying entailment checking. Cite as the methodology being adapted.

---

### 2.4 MathDial — Macina et al. (2023)
**Full citation:** Macina, J., Daheim, N., Chowdhury, S. P., Sinha, T., Kapur, M., Gurevych, I., & Sachan, M. (2023). MathDial: A dialogue tutoring dataset with rich pedagogical properties grounded in math reasoning problems. *arXiv preprint arXiv:2305.14536*.
**Link:** https://arxiv.org/abs/2305.14536
**Verification:** Confirmed via EULER paper (cited as [11]). 3,000 one-shot teacher-student interactions. Teacher questions written by humans, student solutions LLM-generated.
**Why to add:** A related prior dataset with teacher-student math tutoring interactions. Useful for baseline comparison and for contextualizing SocraticRAG's dataset size. MathDial is math-only and not RAG-grounded — two dimensions SocraticRAG improves on.

---

### 2.5 TutorEval / TutorChat — Chevalier et al. (2024)
**Full citation:** Chevalier, A. et al. (2024). Language models as science tutors. *arXiv preprint arXiv:2402.11111*.
**Link:** https://arxiv.org/abs/2402.11111
**Verification:** Confirmed via EULER paper (cited as [10]). TutorChat: 80,000 synthetic dialogues from LibreTexts science textbooks. TutorEval: benchmark of science questions created with human expert assistance.
**Why to add:** TutorChat is the closest prior work to SocraticRAG in terms of domain diversity (science textbooks) and using instructor-curated content. However, TutorChat is synthetic (GPT-generated) and has no retrieval faithfulness evaluation. Contextualizes SocraticRAG's contribution of real annotator gold responses and explicit faithfulness grounding. LibreTexts is CC-licensed — could supplement or replace Andrew Ng materials for the corpus.

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
**What we need:** A paper that operationalizes Bloom's taxonomy levels (remember, understand, apply, analyze, evaluate, create) in an NLP or LLM evaluation context.
**Why needed:** Metric 3 references Bloom's taxonomy for "cognitive depth" scoring, but the current paper cites no NLP paper that does this operationally. The SynapsEd paper cites Herrmann-Werner et al. (2024) on GPT-4 + Bloom's for medical exams — this could work.

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
- MathTutorBench: not yet verified exact count (need to check)
- MathDial: 3,000 one-shot interactions
- SocraticLM / SocraTeach: 35,000 generated dialogues
- EULER: 100 test samples, 500-650 training samples (very small)
- Discerning Minds / GuideEval: not yet verified

**Recommended scale for SocraticRAG:**
- Corpus: 50-100 document chunks across 5-10 courses and 3-4 domains
- Student profiles: 4 cognitive states per chunk = 200-400 scenario-profiles
- Student utterances: 1-2 per scenario-profile = 400-800 total utterances
- Gold annotations: all (human educators annotate all scenarios; this is the benchmark)
- Phase 4 human validation: 500 generated interactions as proposed (retain)

**Rationale:** Quality over quantity. SocraticRAG's value is in multi-dimensional grading, not data volume. A well-annotated 500-item benchmark is more credible for EMNLP than a large synthetic one.

---

*Last updated: 2026-05-11. Research ongoing.*
