# EMNLP 2026 — Readiness Assessment & What We Need to Strengthen

* To revisit before we finalize the submission.*

---

## Bottom Line

If we implement the plan exactly as designed — dataset built, experiments run, human validation done — we have a legitimate shot at EMNLP 2026. Not a guaranteed acceptance, but a competitive one. My estimate is roughly 40–50% acceptance probability as a long paper, which is around EMNLP's historical rate. That means we compete on merit, not on a technicality.

The goal of this document is to be honest about what's genuinely strong, what's soft and could cause rejection from the similar papers I read that have been accepted, and what three specific additions would meaningfully improve our odds.

---

## What's Working in Our Favor

**The gap argument is solid and hard to refute.** RAGAS structurally breaks on interrogative text — this is a technical fact, not an opinion. No reviewer can say "have you tried RAGAS?" because we've already explained why it produces a vacuous score on Socratic questions. The gap is evidenced from multiple directions: MathTutorBench evaluates its own Socratic task with BLEU while calling BLEU unreliable (internal contradiction), TutorChat gives models a context chunk but never checks whether they use it, Lefton shows the same absence in a completely different domain. That accumulation is hard to dismiss.

**The FActScore adaptation is a real technical contribution.** Extending atomic decomposition and entailment checking from declarative text to interrogative text is novel. The step where we extract presuppositions embedded in a Socratic question before running NLI is not something that has been done for pedagogical evaluation. Reviewers will see this.

**The three-axis orthogonal design in diagnostic benchmarks.** A model can fail any one axis while passing the other two, and each failure points to a different deficiency. MathTutorBench got an oral at EMNLP 2025 partly for the same reason — diagnostic clarity. Our design has the same structure, applied to a harder joint problem.

**We have human validation built in.** A lot of benchmark papers skip meta-evaluation. We plan Cohen's Kappa and Spearman ρ with a target threshold in Phase 4. That directly answers the reviewer who asks "how do we know the automated metrics mean anything?"

---

## Where we might need to strengthen the paper

### 1. Scale: 400–800 items is on the small side

MathTutorBench has 9,125 items. We are much smaller. This is defensible — our annotation is harder (three dimensions, expert educators, supported-sentence highlights) and we are measuring a more constrained phenomenon — but we need to make that argument explicitly in the paper. We cannot just say "quality over quantity" without showing the benchmark has enough statistical power to support the core claim. **We need to compute this before submission.**

### 2. The "joint degradation" claim must land clearly in the results

This is the riskiest part of the whole paper. Our core finding is that performance degrades when both constraints (Socratic adherence + retrieval faithfulness) are applied together. If the results table doesn't show this clearly — if the numbers are noisy, the effect is small, or models perform similarly across conditions — the entire argument weakens. (Professor even asked to try this on a small scale to even see if it's relevant at all.)

We need a model that scores well on open-domain Socratic benchmarks and visibly fails on SocraticRAG, specifically on Metric 2. If GPT-4o scores 85% on Metric 1 but 40% on Metric 2, that's a story. If it scores 72% and 68% and the differences across models are small, reviewers will say the benchmark doesn't reveal a failure mode that didn't already exist.

**We cannot know this until we run the experiments. It is the single biggest unknown in the plan.**

### 3. Metric 2 needs independent validation

The NLI presupposition extraction step is our most novel technical claim. Reviewers will ask: how reliable is the LLM presupposition extraction itself? If the LLM misidentifies what's embedded in the question, Metric 2 is measuring noise, not faithfulness.

Phase 4 human validation partially addresses this for the full pipeline, but a focused study specifically on Metric 2 would be stronger. See the "What to Add" section below.

### 4. Two annotators for Phase 4 is statistically fragile

Cohen's Kappa with two annotators is computable but weak. If agreement falls below 0.6 on either dimension, reviewers will say the benchmark measures something subjective. The adjudication protocol helps but does not fully mitigate this. Three annotators would change the story significantly.

**Question for the team: is there a third person — a grad student with an education background, or a colleague of one of the professors — who could join Phase 4?**

### 5. Corpus diversity needs explicit defense

5–10 courses, 3–4 domains sounds diverse. But if the domains are all STEM-adjacent, a reviewer will ask whether the findings generalize. but we can also just stick to few courses in one field.However if we want to diversify, We need to make the domain selection deliberate and justify it in the paper. One humanities or social science course would strengthen this significantly.

---

## Three Things That Would potentially Push Acceptance

### Add 1 — Cross-benchmark comparison showing RAGAS fails to discriminate

Run RAGAS on the same model outputs we evaluate with SocraticRAG. Show that RAGAS scores for GPT-4o and Llama-3.1 are indistinguishable or undefined, while our three-axis metrics separate them clearly. This is the sharpest possible argument that SocraticRAG is necessary. It turns a theoretical claim ("RAGAS breaks") into an empirical one ("RAGAS cannot tell these models apart; ours can"). RAGAS is public and this experiment is relatively cheap to run.

### Add 2 — A focused Metric 2 reliability study

50 items: the LLM extracts presuppositions from model outputs, a professor rates whether each extracted claim is actually in C (yes/no), we compute agreement. Even 80% agreement is enough to say the extraction is reliable. This directly validates our most novel technical contribution without waiting for Phase 4. It's one afternoon of annotation for one professor.

### Add 3 — Frame for the EMNLP 2026 Theme Track ("New Missions for NLP Research")

The theme track explicitly asks for papers that rethink evaluation and are "grounded in clear claims, strong evidence, and actionable insights." Our argument is that educational RAG systems are now being deployed, and we have no evaluation infrastructure to know whether they are safe to use pedagogically. That is a new mission for NLP evaluation research.

Submitting to the theme track doesn't lower the bar — it puts the paper in front of reviewers who are specifically looking for this kind of argument, rather than reviewers comparing us against MathTutorBench by item count. Worth discussing with the professors whether this framing fits the paper they want to write.

---

## The One Thing That Could Sink It Regardless of Everything Else

The joint degradation result. If the empirical finding is weak or unclear, the paper's argument collapses regardless of how well-designed the methodology is. We need to run pilot experiments as early as possible — before we invest in the full annotation pipeline — to confirm the failure mode is real and measurable.

**Recommended early experiment:** Take 10 document chunks. Prompt GPT-4o with zero-shot Socratic tutor instructions. Run EULER's reveal_answer judge (Metric 1) and a basic NLI check (Metric 2) on the outputs. If Metric 2 flags more than 30% of outputs as introducing concepts not in C, the failure mode is confirmed and we have empirical motivation to proceed with the full benchmark. If the rate is under 10%, we need to revisit the hypothesis.

---

## Open Questions for the Professor Meeting

1. Can we recruit a third annotator for Phase 4 to strengthen the inter-rater reliability claim?
2. Which specific MIT OCW courses are we targeting? We need at least one non-STEM course.
3. Are we submitting to the standard "Resources and Evaluation" track or the Theme Track? The framing is different and the choice affects how we write the introduction.

---

*Last updated: 2026-05-11. Revisit after pilot experiment results are in.*
