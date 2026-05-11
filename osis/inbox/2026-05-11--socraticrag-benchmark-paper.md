---
type: imported-signal
status: unconfirmed
source: existing-doc
path: benchmark paper.md
summary: Full EMNLP research proposal for SocraticRAG — a benchmark evaluating joint Pedagogical Faithfulness and Socratic Adherence in retrieval-augmented educational LLMs.
---

## Claims
- No existing benchmark evaluates RAG faithfulness and Socratic dialogue quality jointly in a constrained educational setting
- RAGAS is structurally incompatible with Socratic (non-declarative) outputs — the claim-decomposition mechanism breaks when the output is a question rather than a statement
- LLMs exhibit a joint failure mode (answer leakage + context drift + misconception miss) that is invisible to either benchmark family in isolation
- MathTutorBench is the closest prior work but is math-only and entirely retrieval-free; Discerning Minds is open-domain with no retrieval constraint
- NLI-based faithfulness checking can be adapted from declarative QA to non-declarative pedagogical outputs (novel contribution)
- Corpus backbone leverages existing SynapsEd OCR/chunking pipeline on Andrew Ng course materials
- Expert annotation (Golden Socratic Responses with highlighted supporting sentences) is necessary, not optional, per MathTutorBench findings
- Target: Spearman ρ > 0.7 between automated metrics and human judgment to make the benchmark fully reusable

## Tensions
- The proposal references SynapsEd's corpus pipeline as the backbone, suggesting SocraticRAG is built around a specific production system — but no SynapsEd code or data lives in this repo; the coupling is asserted but not operationalized
- Expert annotation is called "necessary" but the annotation pipeline, annotator recruitment, and cost model are unspecified
- EULER (the judge rubric) was validated on Socratic quality in open-domain settings — its validity under retrieval-constrained conditions is assumed, not demonstrated
- Ilkou et al. 2024 is cited as calling for RAG+Socratic hybrid benchmarks, but a note in the verified sources section clarifies they use a Knowledge Graph proxy, not RAG — the citation framing may need adjustment
- The four cognitive states (accurate, erroneous, comprehension, confusion) are borrowed from Discerning Minds, but the proposal does not address whether these states behave differently under retrieval constraints vs. open-domain
- CoT prompting motivation (Hu et al. 2025) comes from multimodal reasoning — the transfer assumption to text-based educational RAG is untested and acknowledged as speculative

## Questions
- Is SynapsEd an existing deployed product the builder owns, or a research reference? If it's a live product, SocraticRAG is likely an eval layer on top of it — that changes the scope significantly
- What is the timeline for EMNLP submission? Has a call for papers been confirmed?
- Is the corpus (Andrew Ng materials) cleared for research use / redistribution under the benchmark license?
- Who are the expert annotators? What field (NLP, education, both)? What's the target annotation volume beyond the 500-sample human validation?
- Is the LLM-as-a-Judge (automated three-axis) intended to run as a public leaderboard, a static dataset release, or a private evaluation tool?
- Does the builder want to position SocraticRAG as a dataset contribution, a metric contribution, or both?
