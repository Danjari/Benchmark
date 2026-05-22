**SocraticRAG**

*A Benchmark for Evaluating Pedagogically Safe and Retrieval-Faithful Socratic Dialogue in RAG-based LLMs*

Literature Review & Research Proposal, EMNLP Submission

# 

# **1\. The Argument & The Gap in the Literature**

To motivate SocraticRAG to EMNLP reviewers, we argue that current benchmarks evaluate RAG faithfulness and Socratic dialogue quality in isolation, but never together, and that this is exactly where LLMs fail in real educational deployments.

Note: By definition, Socratic dialogue is *a structured collaborative interaction requiring participants to engage in critical, independent reasoning regarding the dialectical and epistemological foundations of a given topic*.

## **1.1  The RAG Evaluation Gap**

Standard RAG evaluation frameworks were built for one thing: direct Question Answering. RAGAS (Es et al., 2024), the dominant evaluation framework, works by breaking the model's answer into atomic factual statements and checking whether each statement is supported by the retrieved context. The framework was designed and validated exclusively on WikiEval, a dataset of factual questions with declarative answers like "Who directed Oppenheimer?" and "When was the clock tower completed?"

**The Problem:** In education, giving a direct answer is a pedagogical failure (Bonino et al., 2024; Liu et al., 2024; Macina et al., 2025). The LLM must instead synthesize the retrieved context into a hint or a guiding question. So when the output is a Socratic question like *"What do you think happens when the variable increases?"*, RAGAS has nothing to decompose, there are no factual statements to verify. The statement extraction step yields nothing meaningful, making the faithfulness score undefined or trivially zero. A RAG system that generates a well-supported Socratic hint and one that hallucinates an unsupported concept would be completely indistinguishable under this framework.

Researchers are already beginning to combine RAG with Socratic dialogue (Lefton et al., 2025; Ilkou et al., 2024), but none of these systems include any evaluation of whether the Socratic outputs actually stay faithful to the retrieved material. Ilkou et al. (2024) acknowledge this gap directly, noting that while RAG could be applied to Socratic tutoring, it "will require an extension of the current benchmarking techniques," and that existing RAG implementations "do not include evaluation metrics about the quality of the retrieved documents nor human aspects."

## **1.2  The Socratic Evaluation Gap**

In parallel, a growing body of NLP research has begun evaluating the Socratic abilities of LLMs. EULER (Bonino et al., 2024\) fine-tunes LLMs using Direct Preference Optimization to steer them away from direct answers and toward guiding questions. SocraticLM (Liu et al., 2024\) constructs a dataset of 35,000 Socratic-style dialogues and trains models across five pedagogical dimensions, explicitly arguing that "current LLM-based application in personalized teaching predominantly follows a 'Question-Answering' paradigm, where students are passively provided with answers and explanations." MathTutorBench (Macina et al., 2025), an EMNLP 2025 oral, provides the most comprehensive evaluation to date, covering Socratic questioning, mistake identification, and scaffolding generation across multiple models, finding that "subject expertise does not immediately translate to good teaching" and that "tutoring appears to become more challenging in longer dialogs, where simpler questioning strategies begin to fail."

**The Problem:** None of these approaches test whether the model's Socratic outputs stay faithful to a specific retrieved educational document. The evaluation is always open-domain, the model can ask whatever it wants, constrained by nothing. Even TutorEval (Chevalier et al., 2024), which grounds benchmark questions in LibreTexts textbook chapters and was published at ICML 2024, includes no evaluation of whether model responses remain faithful to the provided chapter. And this has measurable consequences. Bonino et al. (2024) empirically show that even fine-tuned Socratic LLMs drift from the original topic across multi-turn interactions, generating responses that diverge from the original educational subject. MathTutorBench itself acknowledges this limitation, noting that the benchmark "does not contain all possible dimensions for educational evaluation" and is entirely retrieval-free. Strikingly, MathTutorBench evaluates its Socratic Questioning task using BLEU-4 while simultaneously arguing that BLEU is “noisy and unreliable” for open-ended pedagogical evaluation—an internal contradiction that demonstrates the field’s lack of purpose-built evaluation metrics for this task. None of these failure analyses even ask whether the model's outputs are constrained by any retrieved instructional context. The question of pedagogical faithfulness is left unaddressed.

## **1.3  Conclusion: The Gap**

The NLP community lacks a benchmark to evaluate what we call **Pedagogical Faithfulness**, the ability of an LLM to generate Socratic guidance that avoids giving the answer away AND stays strictly bounded by a retrieved educational document. RAG benchmarks assume declarative outputs and cannot evaluate guiding questions. Socratic benchmarks operate in open-domain settings with no retrieval constraints. MathTutorBench is the closest existing work, but it is math-only and entirely retrieval-free. **SocraticRAG fills this gap, and it is the first benchmark to evaluate both dimensions jointly in an educational RAG setting.**

## **1.4  Contributions**

We make the following contributions:

1. **Task formulation.** We formally define Pedagogical Faithfulness as an NLP construct: the joint ability of an LLM to generate Socratic guidance that withholds the answer AND stays strictly bounded by a retrieved educational document. No existing benchmark defines or operationalizes this joint constraint. We provide a formal task specification: given (C, P, U), generate R such that R is a question, R ⊢ C, and R ⊬ sol.

2. **A novel evaluation mechanism (Metric 2).** We adapt FActScore's (Min et al., 2023) atomic decomposition and entailment checking from declarative to interrogative text. Rather than decomposing statements into atomic facts, we extract the declarative presuppositions embedded in a Socratic question and verify each against the retrieved context C via NLI. This is the first adaptation of this mechanism to non-declarative pedagogical outputs, and the only automated faithfulness metric that does not break when the model output is a question.

3. **A three-axis evaluation framework.** We propose three orthogonal metrics that jointly capture what no existing benchmark measures: Direct-Answer Leakage (Metric 1, adapted from EULER), Retrieval Faithfulness (Metric 2, novel), and Pedagogical Alignment (Metric 3, adapted from Discerning Minds). Each metric independently exposes a distinct failure mode. A model can fail any one while passing the other two, making SocraticRAG diagnostically useful rather than producing a single aggregate score.

4. **A pilot benchmark dataset (Edu-QA-Socratic).** We construct and release 80 retrieval-constrained educational scenarios drawn from MIT OpenCourseWare (6.7960 Deep Learning, 6.036 Introduction to Machine Learning), covering four cognitive student states per document chunk, with gold Socratic responses validated by expert educators. Each scenario includes the source chunk C, a simulated student utterance U encoding a specific cognitive state, and the highlighted supporting sentences in C that anchor the gold response.

5. **Empirical baseline results.** We evaluate GPT-4o, Claude Sonnet 4.6, and Gemini on Edu-QA-Socratic across all three metrics, demonstrating that joint-constraint performance degrades significantly compared to open-domain Socratic evaluation, and that RAGAS scores are undefined or trivially uninformative on the same model outputs.

# 

# **2\. How to Build the Benchmark (The Methodology)**

To create SocraticRAG for EMNLP, we construct a dataset of retrieval-constrained educational interactions and define three evaluation metrics that jointly capture what no existing benchmark measures.

## **2.1  The Dataset Construction (Edu-QA-Socratic)**

* **Corpus Collection.** Collect a corpus of real university course materials, instructor slide PDFs sourced from MIT OpenCourseWare (CC BY-NC-SA 4.0) and LibreTexts (a repository of 1,685 CC-licensed textbooks spanning all academic domains, previously used as the primary training corpus for TutorChat, Chevalier et al., 2024), syllabi, and reading excerpts, and chunk them using our own OCR and semantic chunking pipeline. This distinguishes SocraticRAG from all existing Socratic benchmarks, which draw from open-domain math problems (MathTutorBench, Macina et al., 2025\) or single-platform dialogues (Discerning Minds, Liu et al., 2025).

* **Student Profile Construction.** Using literature backed concept we will construct students profiles that emulates real world scenarios. And encoding them with four cognitive states, accurate, erroneous, comprehension, and confusion, following the taxonomy from Discerning Minds (Liu et al., 2025), which demonstrates these are the most diagnostically useful states for exposing model weaknesses.

* **Seed Generation (LLM-Assisted).** Prompt a strong teacher LLM to generate candidate student misconceptions and corresponding utterances for each chunk, following the "Dean-Teacher-Student" multi-agent pipeline introduced in SocraticLM (Liu et al., 2024). The Dean agent serves an oversight role, rejecting candidate utterances that are pedagogically implausible or that cannot be derived from the retrieved chunk.

* **Expert Annotation (Gold Standard).** We first generate candidate Socratic responses using a strong teacher LLM, then have expert educators review each scenario and select or lightly revise the best candidate as the Golden Socratic Response (*R*₀ₙₑˣ), with supporting sentences in C explicitly highlighted. This silver-to-gold pipeline follows MathTutorBench's validated practice of expert revision of LLM-generated candidates as the standard for capturing genuine pedagogical quality (Macina et al., 2025).

## **2.2  The Evaluation Axes (What the Benchmark Measures)**

We run state-of-the-art models, GPT-4.5, Claude 4.6 Sonnet, Llama-3.1 (8B and 70B), LearnLM, and EULER (Bonino et al., 2024), through this dataset and score them automatically using an LLM-as-a-Judge framework across three orthogonal dimensions.

### ***Metric 1: Direct-Answer Leakage (Socratic Adherence)***

**What it measures.** Did the LLM act like a vending machine and just give the answer, violating the Socratic constraint?

**Measurement.** We adapt the "reveal\_answer" rubric from EULER's validated GPT-4o judge (Bonino et al., 2024), which evaluates four dimensions of Socratic quality, question presence, on-topic relevance, helpfulness, and answer revelation, and was validated against human annotators with a Pearson r = 0.78 (reported as p = 0.78 in the original paper, non-standard notation). We use the "reveal\_answer" criterion as a binary classifier: a response scores 0 if it states the answer directly and 1 if it successfully withholds it. MathTutorBench (Macina et al., 2025\) operationalizes the same failure mode as a revealing-answer criterion within its Scaffolding Score reward model, confirming it as a central and measurable dimension of tutoring quality.

**Why it matters.** SocraticLM (Liu et al., 2024\) demonstrates that current LLMs, including GPT-4, regularly fail this criterion, directly providing solutions when instructed to teach Socratically. Bonino et al. (2024) confirm the same failure in their qualitative analysis: GPT-4 gives the answer directly in their sample output, which they note "contradicts the demands of Socratic teaching."

### ***Metric 2: Retrieval Faithfulness***

**What it measures.** Are the premises embedded in the LLM's Socratic question factually supported by the retrieved Context C? Does the model introduce concepts absent from C?

**Measurement.** We use Natural Language Inference (NLI) to verify whether each premise implicit in the model's question is entailed by C. Following FActScore (Min et al., 2023), which decomposes generated text into atomic facts and verifies each fact against a knowledge source, we adapt this mechanism to the interrogative setting: we first extract the declarative presuppositions embedded in the Socratic question — for example, the question "What do you think happens when pressure increases in this system?" embeds the assumption that the system involves pressure — then verify whether each assumption is supported by C. If the model embeds a concept not present in C, it receives a penalty for Unverifiable Specificity. Our novel contribution is the adaptation itself: unlike FActScore, which operates on declarative outputs, SocraticRAG's Metric 2 extends the atomic decomposition and entailment mechanism to non-declarative pedagogical text.

**Why this is necessary.** Ilkou et al. (2024) explicitly state that RAG implementations for Socratic tutoring "do not include evaluation metrics about the quality of the retrieved documents nor human aspects," and call for an extension of benchmarking techniques. Lefton et al. (2025) demonstrate that Socratic RAG systems in information retrieval contexts (academic knowledge organization system disambiguation) also include no faithfulness evaluation, confirming the systemic absence of this component. This metric directly fills the gap both papers identify. Furthermore, this measurement is structurally impossible under RAGAS (Es et al., 2024), whose faithfulness score presupposes declarative outputs and breaks when applied to interrogative forms.

### ***Metric 3: Pedagogical Alignment (Student State Targeting)***

**What it measures.** Did the question directly address the student's specific misconception, or did it ask something generically valid but contextually irrelevant?

**Measurement.** We evaluate whether the model correctly perceives the student's cognitive state and adapts its questioning strategy accordingly. Following the three-phase behavioral framework from Discerning Minds (Liu et al., 2025), Perception (inferring learner state), Orchestration (adapting strategy), and Elicitation (posing appropriate questions), we score each response on whether it: (1) correctly identifies the student's state, (2) selects an appropriate instructional strategy, and (3) poses a question at the correct cognitive depth per Bloom's taxonomy, as operationalized in the GuideEval scoring rubric. A response that asks a generically valid question but misses the student's specific misconception scores low on this axis, even if it passes Metrics 1 and 2\.

**Why existing benchmarks miss this.** Discerning Minds (Liu et al., 2025\) evaluates pedagogical alignment without retrieval constraints, the model can draw on any knowledge. SocraticRAG adds the requirement that the aligned question must simultaneously stay within the bounds of C. This is the joint evaluation that no existing benchmark performs.

### ***The Three Axes are Orthogonal***

A model can fail any single axis while passing the other two. For example: a model can ask a Socratic question that stays within C but completely misses the student's misconception (passes Metrics 1 and 2, fails Metric 3); or it can ask a perfectly targeted question that introduces a concept not in C (passes Metrics 1 and 3, fails Metric 2); or it can give a direct answer that is well-supported by C (passes Metric 2, fails Metrics 1 and 3). This orthogonality is what makes SocraticRAG diagnostically useful, each failure mode points to a different architectural or training deficiency.

## **2.3  The Empirical Contribution**

The paper concludes by showing that while modern LLMs perform reasonably on either Socratic questioning in open domains or faithfulness in direct QA, their performance severely degrades when asked to do both simultaneously in a constrained educational context. This is the core empirical claim: the joint constraint creates a failure mode that neither Socratic benchmarks nor RAG benchmarks can detect in isolation.

# 

# **3\. Detailed Methodology, The Four Phases**

## **Phase 1: Task Definition & Dataset Construction**

### ***The Task***

Given a pedagogical Context (C) — a semantically coherent text unit (typically 200–500 tokens) extracted from a specific course document, representing a single concept such as a definition, worked example, or explanation, and serving as the model's sole permitted knowledge source — a simulated Student Profile (P) encoding a specific cognitive state and misconception, and a Student Utterance (U) expressing that state, the model must generate a Response (R) that acts as a Socratic guiding question derived strictly from C, without revealing the answer and without introducing concepts absent from C.

*Input:  (C, P, U)   ⟶   Output:  R  such that  (1) R is a question,  (2) R ⊢ C,  (3) R ⊬ sol*

This task formulation is distinct from all existing Socratic benchmarks in one critical way: the model's output is simultaneously constrained by pedagogical form (it must be a question, not an answer) and by retrieval faithfulness (it must stay within C). No existing benchmark evaluates both constraints jointly.

### ***Data Curation: The Silver-to-Gold Pipeline***

* **Corpus Collection.** We extract text chunks from real university course materials, lecture slide PDFs sourced from MIT OpenCourseWare (CC BY-NC-SA 4.0) and LibreTexts (Chevalier et al., 2024), syllabi, and reading excerpts, using our own OCR and semantic chunking pipeline. LibreTexts hosts 1,685 CC-licensed textbooks across all academic domains and was used as the primary training corpus for TutorChat (Chevalier et al., 2024), confirming its suitability as a multi-domain educational source. This situates SocraticRAG in authentic instructor-uploaded content, directly distinguishing it from MathTutorBench (Macina et al., 2025), which sources all problems from GSM8K, and from Discerning Minds (Liu et al., 2025), which draws from a single middle-school science tutoring platform. Our multi-domain, multi-format corpus reflects the real-world deployment conditions of RAG-based educational systems.

* **Student Profile Construction.** We simulate four cognitive states per document chunk, following the taxonomy established in Discerning Minds (Liu et al., 2025): accurate (correct understanding), erroneous (incorrect answer), comprehension (explicit understanding), and confusion (expressed uncertainty). Liu et al. (2025) demonstrate empirically that current LLMs handle positive states effectively but systematically fail under negative states, particularly when misconceptions must be inferred rather than explicitly stated, making these four states the most diagnostically useful categories for exposing model weaknesses. The four-state taxonomy and the Dean-Teacher-Student pipeline operate on orthogonal dimensions: the DTS pipeline governs the generation process (how candidate misconceptions and Socratic responses are produced and filtered), while the four-state taxonomy governs the student profile space (what kind of understanding a student is expressing in a given utterance). Combining them produces a dataset where every scenario is both pedagogically plausible (Dean-validated) and diagnostically targeted (state-specific), covering the full range of student comprehension states that an educational RAG system will encounter. For each chunk, we generate at least one Student Utterance per state, producing contrastive pairs (e.g., erroneous vs. accurate under identical context) that enable controlled evaluation of model sensitivity.

* **Seed Generation (LLM-Assisted).** We prompt a strong teacher LLM to generate candidate student misconceptions and corresponding utterances for each chunk, following the "Dean-Teacher-Student" multi-agent pipeline introduced in SocraticLM (Liu et al., 2024). The Dean agent serves an oversight role, rejecting candidate utterances that are pedagogically implausible or that cannot be derived from C.

* **Expert Annotation (Gold Standard).** Expert educators review LLM-generated candidate responses for each scenario and select or lightly revise the best as the Golden Socratic Response (R₀ₙₑˣ): a response that successfully guides the student toward the correct understanding using only content present in C. Annotators explicitly highlight the supporting sentences in C that justify the pedagogical intervention, creating a mapping that anchors the faithfulness evaluation in Phase 2\. This follows MathTutorBench's finding that teacher-created data is essential for capturing high-quality tutoring and must be prioritized in the final data mix (Macina et al., 2025). Standard automatic metrics based on word overlap are unreliable for open-ended pedagogical evaluation (Macina et al., 2025), making expert-annotated ground truth a necessary rather than optional component.

## **Phase 2: Evaluation Metrics, Three Orthogonal Axes**

Standard metrics like BLEU and ROUGE are inadequate for open-ended conversational RAG (Macina et al., 2025). RAGAS (Es et al., 2024), the dominant RAG faithfulness framework, is structurally incompatible with Socratic outputs: its faithfulness score works by decomposing the generated answer into atomic statements and verifying entailment against the retrieved context, a mechanism that presupposes a declarative output. When the output is a Socratic question, there are no factual claims to decompose, and the metric either breaks or returns a vacuous score. We therefore propose a three-axis LLM-as-a-Judge framework, where each axis captures a distinct and orthogonal failure mode. To mitigate self-enhancement bias — the documented tendency for LLMs to inflate scores when judging outputs from their own model family (Zheng et al., 2024) — we apply a cross-judge protocol: Claude evaluates GPT-4o outputs, and GPT-4o evaluates Claude outputs.

### ***Metric 1: Direct-Answer Leakage (Socratic Adherence)***

**What it measures.** Did the model give the answer directly instead of guiding the student to discover it?

**Measurement.** We prompt an evaluator LLM with a strict rubric to flag responses that reveal the answer or solution directly rather than posing a guiding question. The rubric is adapted from EULER's GPT-4o judge (Bonino et al., 2024), which evaluates four dimensions of Socratic quality, question presence, on-topic relevance, helpfulness, and answer revelation, and was validated against human annotators with a Pearson r = 0.78 (reported as p = 0.78 in the original paper, non-standard notation). We use the "reveal\_answer" criterion as a binary classifier: a response scores 0 if it states the answer directly and 1 if it successfully withholds it. MathTutorBench (Macina et al., 2025\) operationalizes the same failure mode as a revealing-answer criterion within its Scaffolding Score reward model, confirming it as a central and measurable dimension of tutoring quality.

**Why it matters.** SocraticLM (Liu et al., 2024\) demonstrates that current LLMs, including GPT-4, regularly fail this criterion, directly providing solutions when instructed to teach Socratically. Bonino et al. (2024) confirm the same failure in their qualitative analysis: GPT-4 gives the answer directly in their sample output, which they note "contradicts the demands of Socratic teaching."

### ***Metric 2: Retrieval Faithfulness***

**What it measures.** Are the premises embedded in the model's Socratic question factually supported by Context C? Does the model introduce concepts absent from C?

**Measurement.** We use Natural Language Inference (NLI) to verify whether each premise implicit in the model's question is entailed by C. Following FActScore (Min et al., 2023), which decomposes generated text into atomic facts and verifies each fact against a knowledge source, we adapt this mechanism to the interrogative setting: we first extract the declarative presuppositions embedded in the Socratic question — for example, the question "What do you think happens when pressure increases in this system?" embeds the assumption that the system involves pressure — then verify whether each assumption is supported by C. If the model embeds a concept not present in C, it receives a penalty for Unverifiable Specificity. Our novel contribution is the adaptation itself: unlike FActScore, which operates on declarative outputs, SocraticRAG's Metric 2 extends the atomic decomposition and entailment mechanism to non-declarative pedagogical text.

**Why this is necessary.** Ilkou et al. (2024) explicitly state that RAG implementations for Socratic tutoring "do not include evaluation metrics about the quality of the retrieved documents nor human aspects," and call for an extension of benchmarking techniques. Lefton et al. (2025) demonstrate that Socratic RAG systems in information retrieval contexts (academic knowledge organization system disambiguation) also include no faithfulness evaluation, confirming the systemic absence of this component. This metric directly fills the gap both papers identify.

### ***Metric 3: Pedagogical Alignment (Student State Targeting)***

**What it measures.** Does the Socratic question actually address the student's specific misconception, or does it ask a generically valid but contextually irrelevant question?

**Measurement.** We evaluate whether the model correctly perceives the student's cognitive state and adapts its questioning strategy accordingly. Following the three-phase behavioral framework from Discerning Minds (Liu et al., 2025), Perception (inferring learner state), Orchestration (adapting strategy), and Elicitation (posing appropriate questions), we score each response on whether it: (1) correctly identifies the student's state, (2) selects an appropriate instructional strategy, and (3) poses a question at the correct cognitive depth per Bloom's taxonomy, as operationalized in the GuideEval scoring rubric. A response that asks a generically valid question but misses the student's specific misconception scores low on this axis, even if it passes Metrics 1 and 2\.

**Why existing benchmarks miss this.** Discerning Minds (Liu et al., 2025\) evaluates pedagogical alignment without retrieval constraints, the model can draw on any knowledge. SocraticRAG adds the requirement that the aligned question must simultaneously stay within C. This is the joint evaluation no existing benchmark performs.

## **Phase 3: Experimental Setup & Baselines**

### ***Models Evaluated***

We evaluate across three model categories, following MathTutorBench's experimental design (Macina et al., 2025):

* **General LLMs:** GPT-4o, Claude 4.6 Sonnet, Llama-3.1 (8B and 70B)

* **Specialized tutoring models:** LearnLM (available as learnlm-1.5-pro-experimental via Google AI API), Qwen2.5-7B-SocraticLM (Liu et al., 2024; CogBase-USTC/SocraticLM on HuggingFace), a fine-tuned Socratic model with publicly available weights

* **Math-specialized models:** included as a baseline to test whether subject expertise compensates for pedagogical and faithfulness deficits, following MathTutorBench's finding that "subject expertise does not immediately translate to good teaching" (Macina et al., 2025\)

### ***Prompting Paradigms***

* **Zero-Shot:** A standard Socratic tutor system prompt, following EULER's inference prompt (Bonino et al., 2024\) which instructs the model to ask thought-provoking questions without revealing the answer.

* **Few-Shot (In-Context Learning):** 3–5 examples of retrieval-constrained Socratic turns drawn from the gold dataset, where each example shows the context C, student utterance U, and R₀ₙₑˣ alongside the highlighted supporting sentences.

* **Chain-of-Thought (CoT):** The model outputs an explicit rationale, Identify misconception → Locate supporting sentences in C → Draft question, before producing R. Wei et al. (2022) establish that Chain-of-Thought prompting reliably elicits reasoning across arithmetic, commonsense, and symbolic tasks; we test whether the same approach improves retrieval-grounded Socratic generation in our educational RAG setting.

**The goal of Phase 3** is to determine whether SocraticRAG is solvable through prompt engineering alone, or whether it exposes architectural limitations that require retrieval-aware training, a question that existing Socratic benchmarks, operating in open-domain settings, cannot answer.

## **Phase 4: Human Validation (Meta-Evaluation)**

An NLP benchmark is only credible if its automated metrics correlate reliably with human judgment (Macina et al., 2025; Bonino et al., 2024).

**Method.** We sample 500 generated interactions from the baseline models. Two expert educators (the co-authoring professors), blind to which model produced each response, rate each on two dimensions: Faithfulness (is the question derived from C?) and Socratic Adherence (does the question guide without revealing?) using a Likert scale (1–5). Disagreements are resolved through a structured adjudication protocol where both annotators re-examine contested cases jointly.

**Statistical Validation.** We calculate Cohen's Kappa (κ) for inter-rater reliability between the two human annotators. Discerning Minds (Liu et al., 2025\) reports agreement ratios of 89–97% between LLM-based and human scoring across their pedagogical metrics, suggesting that well-designed LLM judges can serve as reliable proxies. We then calculate Spearman's ρ between human scores and our automated three-axis pipeline. Following EULER's validation methodology (Bonino et al., 2024), which achieved Pearson r = 0.78 (reported as p = 0.78, non-standard notation) between GPT-4o and human judgments on Socratic quality, we set a target of ρ \> 0.7 as the threshold for confirming that SocraticRAG's automated metrics can reliably substitute for expensive human evaluation in future work.

**Success Criteria.** If the correlation is strong, SocraticRAG becomes a reusable, fully automated benchmark that future researchers can run without human annotation, directly addressing the scalability limitation identified by Macina et al. (2025), who note that human pedagogical evaluation "is expensive" and "can only create a snapshot of current performance."

# **4\. Why This is a Strong EMNLP Paper**

* **It contributes a reusable resource.** NLP researchers value datasets. SocraticRAG would become the standard benchmark used when researchers want to prove their new fine-tuned educational LLM handles retrieval-constrained Socratic tutoring better than GPT-4o. MathTutorBench (Macina et al., 2025\) already demonstrates that EMNLP accepts and values holistic pedagogical benchmarks as oral papers, SocraticRAG fills the retrieval-faithful gap that MathTutorBench explicitly acknowledges it does not cover.

* **It is highly topical.** Hallucination mitigation in RAG and LLM alignment for education are two of the most heavily funded research areas in NLP right now. Ilkou et al. (2024) call directly for hybrid benchmarks combining RAG and pedagogical evaluation. Lefton et al. (2025) build a Socratic RAG system for information retrieval contexts without evaluating faithfulness. SocraticRAG is the evaluation infrastructure both lines of work are missing.

* **It leverages existing work.** Our own OCR and semantic chunking pipeline provides the corpus backbone. The Socratic prompting strategies already developed provide the zero-shot baseline. The student misconception simulation follows a validated pipeline from SocraticLM (Liu et al., 2024). The evaluation rubric is adapted from EULER (Bonino et al., 2024\) and Discerning Minds (Liu et al., 2025). Nothing is built from scratch, everything is a principled extension of verified prior work.

# 

# 

# 

# 

# 

# 

# 

# **5\. Verified Sources**

All citations below have been verified through full-text access. No source is cited on the basis of abstracts or secondary descriptions alone.

**1\. Es et al. (2024), RAGAS** | EACL 2024

Defines the dominant RAG faithfulness framework. Its claim-decomposition mechanism, which breaks answers into atomic statements for entailment checking, structurally breaks for non-declarative Socratic outputs. Validated on WikiEval, a purely declarative QA dataset.

→ [https://aclanthology.org/2024.eacl-demo.16](https://aclanthology.org/2024.eacl-demo.16)

**2\. Bonino, G., Sanmartino, G., Pinheiro, G.G., Papotti, P., Troncy, R., & Michiardi, P. (2024), EULER** | AIxEDU @ AIxIA 2024

Fine-tunes LLMs for Socratic interactions using DPO. Provides the validated LLM-as-a-judge rubric for Socratic quality, including the "reveal\_answer" binary criterion, confirmed at Pearson r = 0.78 (reported as p = 0.78 in the original paper, non-standard notation) against human judgment. Empirically shows topic drift in multi-turn Socratic dialogues.

→[https://scholar.google.com/scholar?hl=en\&as\_sdt=0%2C5\&q=EULER%3A+Fine+Tuning+a+Large+Language+Model+for+Socratic+Interactions\&btnG=](https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=EULER%3A+Fine+Tuning+a+Large+Language+Model+for+Socratic+Interactions&btnG=) 

**3\. Liu, J. et al. (2024), SocraticLM** | NeurIPS 2024

Constructs 35,000 Socratic-style dialogues via a Dean-Teacher-Student multi-agent pipeline and fine-tunes LLMs across five pedagogical dimensions. Demonstrates that current LLMs, including GPT-4, predominantly follow a Question-Answering paradigm and fail at Socratic teaching even when explicitly instructed to guide students.

→ [https://proceedings.neurips.cc/paper\_files/paper/2024/hash/9bae399d1f34b8650351c1bd3692aeae-Abstract-Conference.html](https://proceedings.neurips.cc/paper_files/paper/2024/hash/9bae399d1f34b8650351c1bd3692aeae-Abstract-Conference.html)

**4\. Macina, J. et al. (2025), MathTutorBench** | EMNLP 2025 (Oral)

The most comprehensive holistic tutoring benchmark to date. Establishes that subject expertise does not translate to good teaching, that tutoring degrades in longer dialogues, and that teacher-created ground truth is essential. Explicitly limited to math and entirely retrieval-free, the gap SocraticRAG addresses.

→ [https://arxiv.org/abs/2502.18940](https://arxiv.org/abs/2502.18940)

**5\. Ilkou, E., Linzbach, S., & Wallat, J. (2024), Hybrid Evaluation of Socratic Dialogue for Teaching** | ISWC 2024

Explicitly calls for hybrid benchmarks combining RAG and Socratic evaluation, noting that existing RAG implementations "do not include evaluation metrics about the quality of the retrieved documents nor human aspects." States directly that applying RAG to Socratic tutoring "will require an extension of the current benchmarking techniques."

This paper does not use RAG but rather introduces a proxy LLM format with Knowledge engineering and create a knowledge graph through which information is retrieved. Check page 3 of paper for more details

→ [https://ceur-ws.org/Vol-3953/363.pdf](https://ceur-ws.org/Vol-3953/363.pdf)

**6\. Lefton, L. et al. (2025), A Socratic RAG Approach** | AAAI 2025

Demonstrates a Socratic RAG system for academic knowledge organization system (KOS) disambiguation—a library taxonomy information retrieval task, not educational tutoring. Includes zero evaluation of whether the Socratic outputs stay faithful to the retrieved material, confirming the systemic absence of faithfulness evaluation even outside educational settings.

→ [https://arxiv.org/abs/2502.15005](https://arxiv.org/abs/2502.15005)

**7\. Liu, Y. et al. (2025), Discerning Minds or Generic Tutors?** | arXiv 2025

Proposes GuideEval, a benchmark evaluating Socratic LLMs through a three-phase framework of Perception, Orchestration, and Elicitation, and the four-state cognitive taxonomy (accurate, erroneous, comprehension, confusion). Shows LLMs systematically fail under negative student states. Operates entirely in open-domain settings with no retrieval constraints, the closest existing work to SocraticRAG, and the clearest demonstration that the retrieval-faithfulness dimension remains unevaluated.

→ [https://arxiv.org/abs/2508.06583](https://arxiv.org/abs/2508.06583)

**8\. Wei, J. et al. (2022), Chain-of-Thought Prompting Elicits Reasoning in Large Language Models** | NeurIPS 2022

Establishes Chain-of-Thought prompting as a reliable technique for eliciting reasoning across arithmetic, commonsense, and symbolic tasks. Provides the canonical motivation for the CoT prompting paradigm tested in Phase 3.

→ [https://arxiv.org/abs/2201.11903](https://arxiv.org/abs/2201.11903)

**9\. Zheng, L. et al. (2024), Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena** | NeurIPS 2024

Introduces MT-Bench (80 multi-turn questions across 8 categories) and documents three systematic LLM-as-judge biases: position bias, verbosity bias, and self-enhancement bias (LLMs significantly inflate scores when evaluating outputs from their own model family). GPT-4 as judge achieves >80% agreement with human evaluators, establishing the validation bar for LLM-as-judge methods. Self-enhancement bias directly motivates SocraticRAG's cross-judge protocol.

→ [https://arxiv.org/abs/2306.05685](https://arxiv.org/abs/2306.05685)

**10\. Min, S. et al. (2023), FActScore: Fine-Grained Atomic Evaluation of Factual Precision in Long Form Text Generation** | EMNLP 2023

Proposes decomposing generated text into atomic facts and verifying each fact independently against a knowledge source via entailment. Automated pipeline achieves <2% error rate versus human annotation, establishing atomic decomposition and entailment checking as a reliable faithfulness evaluation mechanism. Direct methodological ancestor of SocraticRAG's Metric 2, which adapts the same two-step mechanism from declarative to interrogative text.

→ [https://arxiv.org/abs/2305.14251](https://arxiv.org/abs/2305.14251)

**11\. Chevalier, A. et al. (2024), Language Models as Science Tutors** | ICML 2024

Introduces TutorEval (834 expert-annotated questions across 5 domains, grounded in LibreTexts textbook chapters) and TutorChat (78,000 synthetic tutoring dialogues from 1,685 LibreTexts textbooks). Confirms LibreTexts as a viable multi-domain CC-licensed educational corpus. Critically, TutorChat provides context C to the model but includes zero evaluation of whether responses stay faithful to that context — confirming the faithfulness gap SocraticRAG addresses is present even in LibreTexts-grounded educational systems.

→ [https://arxiv.org/abs/2402.11111](https://arxiv.org/abs/2402.11111)

*SocraticRAG Research Proposal, For Internal Review*  
