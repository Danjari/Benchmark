---
type: feedback
date: 2026-05-11
source: professor session (Hanan Salam, April 30 2026 + Moudjahid responses May 1)
summary: Professor raised 4 concerns about the proposal — DTS/4-state combination clarity, annotator count, human verification framing, and Context C definition.
---

## Raw Signal

**Hanan Salam, 8:04 PM Apr 30:**
"is this based on the 4 profiles?"

**Moudjahid, 9:55 AM May 1:**
"no this is based on the Dean Teacher Student (DTS) pipeline.

we basically have two things:
a pipeline for generating responses and misconceptions (DTS)
and a pipeline for detecting where the student is in their understanding (Accurate, Erroneous, Comprehension, Confusion).

these two came from different papers but I thought we could combine...

Himanshi suggested maybe creating our own?"

**Hanan Salam, 8:05 PM Apr 30:**
"how many?"

**Moudjahid, 9:56 AM May 1:**
"Himanshi was going to do some research on how many people could be the minimum for such a conference. @hl3937@nyu.edu"

**Hanan Salam, 8:05 PM Apr 30:**
"I wonder if these are sufficient. can you double check whether these are sufficient."

**Hanan Salam, 8:06 PM Apr 30:**
"so no human verification?"

**Moudjahid, 9:58 AM May 1:**
"the human here will check only a few responses and see if they are aligned. but yes it is LLM first."

**Hanan Salam, 8:07 PM Apr 30:**
"how do we define the Context C?"

**Moudjahid, 10:00 AM May 1:**
"C is the content from documents that are accessible through RAG.

for example: in the document there is a definition for a topic and few examples.
does the LLM mention them in a conversation about said topic with the student? if so to what extent?"

## Interpretation

- **DTS + 4-state combination**: professor did not understand the two systems were orthogonal. Needs a paragraph in the proposal.
- **"How many?"**: likely about annotators. Himanshi researching minimum for EMNLP. Still open.
- **"Are these sufficient?"**: likely about the 4 cognitive states (accurate/erroneous/comprehension/confusion). Whether 4 states cover the space adequately vs. SocraticLM's 6. Possibly also about the 3 evaluation metrics. Open design question.
- **"No human verification?"**: misread the pipeline as fully automated. Clarification: Phase 1 = professors review every gold response. Phase 4 = professors validate automated metrics against human scores. Two separate human checkpoints.
- **Context C**: needs a concrete definition with bounds (200-500 tokens, specific concept unit, sole permitted knowledge source).

---

## Sessions

- 2026-05-11 — Professor session signal logged: 4 concerns from Hanan Salam (April 30) with Moudjahid responses (May 1) · `claude -r 127ec0b2-7994-4530-bcae-3fbf88969adc`
