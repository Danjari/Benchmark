# Thesis — SocraticRAG v1

## The Bet

SocraticRAG introduces Pedagogical Faithfulness as a measurable NLP construct: the ability of an LLM to generate Socratic guidance that simultaneously avoids giving the answer away AND stays strictly bounded by a retrieved educational document. We bet that this joint failure mode is real, measurable, and currently invisible to every existing benchmark.

The v1 bet is to produce the first benchmark that exposes this failure mode, validate its automated metrics against human judgment (Spearman ρ > 0.7), and submit to EMNLP 2026.

## Why Now

Two research lines are converging without meeting: RAG faithfulness evaluation (RAGAS, FActScore) and Socratic dialogue quality evaluation (EULER, SocraticLM, MathTutorBench, Discerning Minds). Neither line evaluates the joint constraint. Educational RAG systems are being deployed into classrooms now (SynapsEd, Khanmigo) with no principled way to verify that their Socratic outputs stay grounded in the materials they retrieved.

MathTutorBench (EMNLP 2025 Oral) is the closest prior work and explicitly acknowledges the gap. Its internal contradiction — evaluating Socratic Questioning with BLEU-4 while arguing BLEU is "noisy and unreliable" — demonstrates the field does not yet have purpose-built metrics for this task.

## The Hypothesis

Current LLMs fail Pedagogical Faithfulness in one of three ways:
1. They reveal the answer (Metric 1 failure: Direct-Answer Leakage)
2. They introduce concepts absent from the retrieved chunk (Metric 2 failure: Retrieval Faithfulness)
3. They ask a generically valid question that misses the student's actual misconception (Metric 3 failure: Pedagogical Alignment)

These failures are orthogonal: a model can pass two while failing one. This orthogonality is what makes SocraticRAG diagnostically useful rather than just another benchmark score.

## Constraint: EMNLP 2026 Deadline

**Submission deadline: May 25, 2026 (14 days from project start).**

The current phase covers proposal finalization and professor sign-off only. The full paper (with evaluation results) follows once the proposal is approved and the annotation pipeline is operational. If the May 25 deadline is for the full paper, the timeline is extremely tight and requires immediate parallel execution of corpus acquisition, annotation, and evaluation.

Confirm with professors: is May 25 the target for a workshop paper, a findings paper, or the full main track paper?

## What Must Be True for This to Work

1. The three metrics are empirically orthogonal (models can fail one independently).
2. LLM-as-judge achieves ρ > 0.7 correlation with human judgment on all three metrics.
3. The silver-to-gold annotation pipeline produces high-quality gold standards that professors validate as pedagogically sound.
4. At least 3-4 subject domains are covered in the corpus to demonstrate generalizability beyond math.
5. At least one specialized tutoring model (Qwen2.5-7B-SocraticLM, LearnLM) performs meaningfully differently from general LLMs, validating the benchmark's discriminative power.

## Open Design Questions

- **Are 4 cognitive states sufficient?** (Professor Hanan Salam, April 30). SocraticLM uses 6 states. Discerning Minds uses 4. Himanshi suggested possibly creating a custom taxonomy. Resolution needed before annotation begins.
- **Minimum annotator count for EMNLP?** Himanshi (hl3937@nyu.edu) was tasked with researching this. Two professors are confirmed. The question is whether two annotators with adjudication meets the EMNLP bar for inter-rater reliability claims.
- **Specific MIT OCW courses**: Multi-domain coverage requires naming courses. To be provided by Moudjahid.

---

## Sessions

- 2026-05-11 — Initial thesis created: EMNLP 2026 deadline, three-metric hypothesis, open design questions · `claude -r 127ec0b2-7994-4530-bcae-3fbf88969adc`
