# SocraticRAG — Strategic Thoughts, May 22 2026

## The Honest Situation

**What we have:** A detailed, well-argued proposal. All citations verified (sources.md). All methodology decisions resolved (decisions.md v1.1). The gap argument is airtight.

**What we don't have:** A paper. Specifically: no dataset, no experiment results, no results table, no abstract, no LaTeX file, no human validation numbers.

**What EMNLP will desk-reject:** A methodology paper with zero empirical results. Even a "Resources and Evaluation" track paper needs to show the benchmark exists and produces meaningful signal across models.

---

## The Gap: Proposal vs. Paper

The thesis doc flagged this as unresolved on May 11: "Confirm with professors — is May 25 the target for a workshop paper, a findings paper, or the full main track paper?" Never answered. Most important open question.

| Target | What's needed | Realistic without AI? | With AI tools? |
|---|---|---|---|
| Long paper (8 pages, main track) | 400-800 annotated items, 5+ models, Phase 4 validation | No | Tight but possible |
| Short paper (4 pages, main track) | 30-50 pilot items, 2-3 models, correlation check | Tight | Yes |
| EMNLP Findings | Same bar as short/long | Same | Yes |
| Workshop | Proposal + small pilot | Yes | Yes |

---

## The Critical Path

Everything blocks on the pilot experiment. Nothing else matters until there are numbers.

The emnlp-readiness.md already specifies the minimum: 10 document chunks, GPT-4o in Socratic mode, Metric 2 flags >30% of outputs introducing concepts not in C. If that lands, the core claim is empirically confirmed and the paper has a spine.

### Three parallel workstreams

**1. Pilot experiment (the empirical backbone)**
- 10-20 MIT OCW or LibreTexts chunks (downloadable tonight)
- GPT-4 generates student utterances: 4 states x 15 chunks = ~60 items
- 2-3 models: GPT-4o, Claude Sonnet, Qwen2.5-7B-SocraticLM
- Metric 1: GPT-4 judge with EULER rubric (just a prompt)
- Metric 2: GPT-4 extracts presuppositions, LLM entailment check against C
- Metric 3: GPT-4 POE judge from Discerning Minds rubric
- RAGAS on same outputs as "Add 1" (cheap, gives RAGAS-fails-to-discriminate comparison)

**2. Paper writing (starts Day 2 in parallel)**
The proposal is ~80% of the paper in informal style. Conversion work:
- Write abstract (what it is, what was built, what was found)
- Restructure proposal into ACL format
- Add results section once pilot numbers land
- EMNLP LaTeX template + formatting

**3. Professor loop**
- Send draft on Day 3 (May 24)
- Get read on: pilot scale defensibility, 2-annotator design argument

---

## The One Thing That Could Sink It

The joint degradation result. If Metric 2 flags less than 10% of outputs, the core claim isn't visible in the numbers. The whole argument collapses. This is why the pilot experiment is the first action, not paper writing.

If the numbers are weak: revisit the hypothesis before investing in the full paper.
If the numbers are strong: the paper writes itself from the proposal.

---

## What AI Tools Actually Change

With AI assistance, timelines compress roughly 5-7x on everything except human judgment:
- Corpus chunking: hours, not days
- Student utterance generation: hours (batch API)
- Model evaluation across all three metrics: hours (batch API)
- Paper writing: 1 day, not 3 (proposal is the skeleton)

Human bottleneck that cannot be skipped: professor review of gold standard samples and paper draft. Budget 3-4 focused hours of professor time across Days 3-4.

---

*Written: 2026-05-22. Revisit after pilot experiment results land.*
