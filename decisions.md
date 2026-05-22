# SocraticRAG — Open Decisions & Issues Log

Each version entry documents what was surfaced on that date: issues flagged, decisions pending, and items that need professor approval or further research before the plan is finalized.

---

## Version 1.3 — 2026-05-23

### STATUS: Open. Cross-script audit surfaced 16 issues. Issues I1–I4 are critical; I5–I10 require revision; I11–I16 are documentation and release gaps.

---

### I. Cross-Script Audit Issues

---

#### CRITICAL — Would trigger reviewer rejection

**I1. Self-judge at dataset construction (scripts 01 + 02) — OPEN**

GPT-4o generates utterances (script 01) and validates them as the Dean (script 02). The paper explicitly cites Zheng et al. (2024) for self-enhancement bias and applies a cross-judge protocol at model evaluation time — but not at dataset construction. A reviewer familiar with Zheng et al. will ask immediately: why does the cross-judge logic apply to model outputs but not to the ground truth being constructed? If GPT-4o's Dean inflates acceptance of its own generations, the benchmark is contaminated before any model runs on it.

*Decision needed:* Apply the cross-judge protocol to the Dean: if GPT-4o generates utterances, use Claude as the Dean validator (and vice versa). This directly extends the paper's existing cross-judge rationale from model evaluation to dataset construction.

*Supporting literature (confirmed 2026-05-23):*
- **Du et al. (ICML 2024)** "Improving Factuality and Reasoning in Language Models through Multiagent Debate" (arXiv:2305.14325): Multiple LLM instances debating each other's outputs significantly improve factuality and reduce hallucination compared to any single model — motivating a cross-model generate-then-validate pipeline.
- **Chan et al. (ICLR 2024)** "ChatEval: Towards Better LLM-based Evaluators through Multi-Agent Debate" (arXiv:2308.07201): A multi-agent referee team with different LLMs delivers better accuracy and closer correlation with human judgment than single-agent evaluation — directly supports using a different-family model as Dean.
- **Madaan et al. (NeurIPS 2023)** "Self-Refine: Iterative Refinement with Self-Feedback" (arXiv:2303.17651): Self-refinement with the *same* model is structurally blind to that model's systematic biases. Cross-model validation (different families, different training) catches errors that self-refinement cannot — because different models have different failure modes.
- **Zheng et al. (NeurIPS 2024)** [already cited]: Self-enhancement bias is documented quantitatively; the paper already applies the cross-judge fix at model evaluation time. Extending it to dataset construction is the consistent application of the same principle.

*Proposed implementation:* In script 01, generate utterances with GPT-4o (or Claude). In script 02, switch the Dean's `client` to the opposite family: use `anthropic.AsyncAnthropic` + `claude-sonnet-4-6` as Dean when the generator is GPT-4o. No other structural changes needed.

**I2. Comprehension/confusion pair integrity not checked (script 02, `check_contrastive_pairs`) — RESOLVED 2026-05-23**

`check_contrastive_pairs()` only checks `accurate`/`erroneous` siblings. It does not check whether the comprehension and confusion utterances for the same chunk target the same concept. The paper's structural guarantee — "all four states anchor to the same target concept" — is only enforced for half the contrastive pairs.

*Decision needed:* Extend `check_contrastive_pairs` to also validate comprehension/confusion siblings, exactly as it does for accurate/erroneous. A broken comprehension/confusion pair should also trigger exclusion and regeneration.

**I3. "Multi-domain corpus" claim not implemented — OPEN**

The paper (Phase 1, Contribution 4, Phase 3) claims a corpus from MIT OCW AND LibreTexts spanning multiple subject domains. Script 00 only handles two MIT OCW ML courses (6.7960, 6.036). Currently the corpus is single-domain (deep learning / intro ML). "Multi-domain" is a load-bearing claim used to distinguish SocraticRAG from MathTutorBench (math-only). Without a second domain, that distinction weakens significantly.

*Decision needed:* Either (a) add LibreTexts sources from at least one non-ML domain, or (b) revise the paper's corpus claims to accurately describe a focused ML/CS corpus and remove the multi-domain distinction argument.

**I4. Script 03 implements 3 of ~7 models promised in the paper — OPEN**

Paper (Phase 3) lists: GPT-4o, Claude 4.6 Sonnet, Llama-3.1 (8B + 70B), LearnLM, Qwen2.5-7B-SocraticLM, and math-specialized models. Script 03 currently implements: GPT-4o, Claude Sonnet, Gemini 2.0 Flash. Llama, LearnLM, and the fine-tuned SocraticLM model are absent. The comparison between a fine-tuned Socratic model (Qwen2.5-SocraticLM) and a general LLM (GPT-4o) under the joint constraint is one of the paper's central empirical contributions.

*Decision needed:* Add Llama-3.1 (via API: Together AI or Groq), LearnLM (Google AI API: `learnlm-1.5-pro-experimental`), and Qwen2.5-7B-SocraticLM (HuggingFace local or Together AI) to script 03. Or narrow the paper's claims to the three implemented models and acknowledge the others as future work.

---

#### SIGNIFICANT — Requires revision or rebuttal response

**I5. Misconception validation is circular (scripts 01 + 02) — RESOLVED 2026-05-23**

For erroneous utterances, script 01 stores `"misconception": ae["erroneous"].get("misconception_expressed", common_misconception)`. When the model fills `misconception_expressed`, that value ends up in P. Script 02's Dean criterion 5 then checks "does U express specifically the misconception *from P*?" — but P's misconception was written by the same model that wrote U, in the same API call. The Dean is verifying U against U's own self-declared misconception. That is trivially true and adds no independent validation power.

*Decision needed:* Dean criterion 5 should always validate against `common_misconception` (extracted from C in Step 1, independent of the generation step). The profile field `misconception` should always store the Step 1 value (`common_misconception`), not the Step 2 self-report. **This is a code fix, not just a documentation issue.** See fix applied in script 01 when this is resolved.

**I6. Chunk size is character-based but paper says "200–500 tokens"; no minimum token filter — RESOLVED 2026-05-23**

`RecursiveCharacterTextSplitter(chunk_size=1000)` splits on 1000 *characters* (~250 tokens). The paper states "200–500 tokens." These roughly overlap, but: (a) it's not documented that the splitter uses characters; (b) there is no minimum token threshold — a 3-token slide header passes through as a valid C. Feeding a 3-token context to GPT-4o produces essentially hallucinated utterances.

*Decision needed:* (a) Switch to token-aware splitting (LangChain's `from_tiktoken_encoder`), or document clearly that chunk_size=1000 characters ≈ 250 tokens; (b) add a hard minimum token threshold (e.g., `min_chunk_tokens=150`) and filter chunks below it. This is a code fix in script 00.

**I7. Chunking mechanism needs redesign — OPEN (research in progress)**

The current character-based, page-by-page splitter is not principled for educational content. The paper claims C represents "a single concept such as a definition, worked example, or explanation." Character splitting does not enforce this — a chunk may contain fragments of two concepts or none. Additionally, page-by-page processing prevents cross-page semantic coherence for textbook content.

*Recommendation (confirmed 2026-05-23):* Switch to **proposition-level chunking**, the approach with the strongest research backing for educational RAG contexts.

**Why proposition-level:**
Chen et al. (EMNLP 2024) "Dense X Retrieval: What Retrieval Granularity Should We Use?" (arXiv:2312.06648) demonstrates that proposition-level chunks — where each chunk is one atomic, self-contained factual statement — outperform passage-level chunks in dense retrieval. This directly matches SocraticRAG's requirement that C represents "a single concept such as a definition, worked example, or explanation." Proposition-level chunks make the "one concept per C" claim structurally enforced, not just asserted.

**Why NOT semantic chunking (LangChain SemanticChunker):**
Qu et al. (arXiv:2410.13070, Oct 2024) "Is Semantic Chunking Worth the Computational Cost?" finds that embedding-based semantic chunking is not consistently superior to simpler methods in downstream RAG performance, and has significant computational overhead. No peer-reviewed paper has validated LangChain's SemanticChunker specifically. Avoid this path.

**Proposed implementation:**
Replace the `chunk_markdown_by_page` step with a two-phase approach:
1. Keep Mistral OCR for PDF → markdown (this is good and defensible)
2. Add a "Propositionizer" step: prompt GPT-4o or Claude to decompose each page's markdown into atomic propositions, one per line. Each proposition becomes a chunk candidate.
3. Filter by token count (MIN_CHUNK_TOKENS = 150; MAX ≈ 400 tokens) — propositions that are too short (titles, headers) or too long (multi-sentence paragraphs) are filtered or split further.
4. Apply a minimum coherence check: a proposition must contain a verb and a subject (simple heuristic) to be retained.

*Supporting literature:*
- **Chen et al. (EMNLP 2024)** "Dense X Retrieval" (arXiv:2312.06648, ACL Anthology: 2024.emnlp-main.845): Proposition-level > passage-level for RAG; Propositionizer trained on GPT-4 seed data.
- **Qu et al. (arXiv:2410.13070, 2024)** "Is Semantic Chunking Worth the Computational Cost?": Semantic chunking (embedding-based) is not consistently better and more expensive — motivation to choose proposition-level over SemanticChunker.

*Decision status:* RESOLVED 2026-05-23. Script 00 fully rewritten with Propositionizer. LangChain dependency removed. Paper's Methodology section still needs updating to describe concept-level chunking (Chen et al. 2024 citation to add).

**I8. Formal task says `(C, P, U) → R` but models receive `(C, U)` — OPEN**

Paper's formal task: models receive `(C, P, U)`. Script 03 passes only `(C, U)`. The design decision (confirmed correct for ecological validity — a deployed tutor doesn't have a labelled ground-truth profile) is good, but the paper hasn't been updated to reflect it. Reviewers will see a direct contradiction between the formal task specification and the implementation.

*Decision needed:* Add one sentence to Phase 1 and/or Phase 2: "Student Profile P is annotation metadata used as Metric 3 ground truth at evaluation time; evaluated models receive only (C, U), as they would in deployment." The formal task notation may also need adjustment.

**I9. "80 scenarios" is a hard claim that will likely be wrong — OPEN**

Contribution 4: "80 retrieval-constrained educational scenarios." The actual count after Dean validation and broken-pair exclusion is always ≤ 80. The paper should not commit to an exact number before the pipeline runs.

*Decision needed:* Change to "up to 80 scenarios" or "N validated scenarios across 20 chunks, where N depends on Dean acceptance rate." Update after the pipeline runs with the actual number.

**I10. Gold annotation pipeline and supporting sentences field don't exist — OPEN**

The paper describes a silver-to-gold pipeline where expert educators select/revise candidate Socratic responses and "explicitly highlight the supporting sentences in C." No script implements any of this. Scripts 04–08 are entirely unwritten. No `supporting_sentences` field exists in any output schema.

*Decision needed:* Build (a) a gold response generation script (LLM generates candidates, formatted for human review), (b) an annotation interface or structured format for expert selection, and (c) add `supporting_sentences: list[str]` to the data schema. This is a substantial implementation gap and is required for the Metric 3 ground truth claim.

---

#### DESIGN QUESTIONS — Defensible but need documentation

**I11. Temperature choices are undocumented — OPEN**

Script 01 uses `temperature=0.3` (concept extraction) and `0.5` (pair generation). Script 02 uses `0.0` (Dean). Script 03 uses `0.7` (model evaluation). None appear in the paper. Benchmark papers routinely report these.

*Decision needed:* Add a "Implementation Details" section or appendix documenting all temperature and generation hyperparameters with brief justifications.

**I12. Dataset construction is stochastic with no fixed seed — OPEN**

API-based models cannot be seeded. Running script 01 twice on the same 20 chunks produces different utterances. Reproducibility must be addressed.

*Decision needed:* Add explicit statement to the paper: "The benchmark artifact is the released `utterances.jsonl`; the generation script is provided for transparency and for future corpus extension, not for exact reproduction of the released dataset." Standard practice (MathTutorBench does this), but must be stated.

**I13. Page-by-page chunking prevents cross-page semantic coherence — OPEN**

`chunk_markdown_by_page` processes each page independently and never produces cross-page chunks. For lecture slides this is correct (one slide = one concept). For textbook PDFs (LibreTexts), concepts frequently span pages. If the corpus ever includes textbooks, the current chunker produces incoherent C at page boundaries.

*Decision needed:* Either (a) document that the chunker is designed for slide-format PDFs only, or (b) extend it to support cross-page merging for textbook formats. Linked to I3 and I7.

**I14. Rejected utterances not saved; acceptance rates can't be reported — RESOLVED 2026-05-23**

Script 02 only saves accepted utterances. Rejected ones are printed to console and lost. The paper will need to report acceptance rates by cognitive state — a quality metric that validates the Dean's discriminative power.

*Decision needed:* Add `OUTPUT_REJECTED_FILE = Path("data/utterances_rejected.jsonl")` and save all Dean-rejected utterances alongside the reason. This is a small code fix with high scientific value.

**I15. `ragas` in requirements.txt without documentation of intent — OPEN**

The paper argues RAGAS is structurally incompatible with Socratic outputs. `ragas` is in requirements.txt, presumably for the "RAGAS baseline" demonstration (Contribution 5). Without documentation, a reviewer examining the repo may think the RAGAS score is used as an actual metric.

*Decision needed:* Add a comment in requirements.txt or a README note: "ragas is included to demonstrate its incompatibility with Socratic outputs (Contribution 5), not as an evaluation metric."

**I16. No README — pipeline is undocumented — OPEN**

No `README.md` exists in `socraticrag/`. EMNLP now requires artifact submission. Reviewers running the released code need clear instructions.

*Decision needed:* Write a README covering: environment setup, API keys, pipeline execution order (00 → 01 → 02 → 03), expected inputs/outputs per script, and how to reproduce the benchmark.

---

## Version 1.2 — 2026-05-23

### STATUS: Resolved 2026-05-23. All four issues fixed in benchmark paper.md and script 01.

---

### G. Dataset Construction Issues (Surfaced During Implementation)

**G1. Contrastive pair guarantee is claimed in the paper but not operationally specified or enforced**

The paper (Phase 1, Section 3) states: "producing contrastive pairs (e.g., erroneous vs. accurate under identical context) that enable controlled evaluation of model sensitivity." Discerning Minds (Section 2.3) makes contrastive pairs a structural requirement: erroneous utterances are "generated from validated accurate answers" and comprehension/confusion pairs are "produced by producing counterpart utterances with the same context."

The current implementation generates all 4 states in a single GPT-4o call with no constraint forcing accurate.target_concept == erroneous.target_concept. The model may assign each state to a different concept within C, producing 4 valid utterances that are not contrastive pairs in any meaningful sense.

*Decision needed:* Either (a) generate the contrastive pairs explicitly — first generate the accurate utterance and its target_concept, then generate the erroneous utterance constrained to the same concept; same for comprehension/confusion — or (b) add an explicit post-generation check that enforces concept alignment. The paper must also specify how pairing is enforced, since it is cited as a methodological feature of the benchmark.

**G2. Student Profile P is underspecified as a distinct artifact**

The formal task in the paper is (C, P, U) → R. P is listed in Contribution 4 and in Phase 1's task formulation as "a simulated Student Profile encoding a specific cognitive state and misconception." Section 2.1 goes further, saying "Using literature backed concept we will construct student profiles that emulate real world scenarios."

The current implementation has no P as a distinct field. The state label (accurate/erroneous/etc.) is embedded in the utterance row. When script 03 runs model evaluation, it feeds (chunk_text, utterance) to the models — P is absent. This creates two problems: (1) the formal task specification in the paper is not implemented, and (2) Metric 3 (Pedagogical Alignment — did the model correctly perceive the student's state?) has no ground-truth P to compare against during scoring.

*Decision needed:* Define exactly what P contains. At minimum: {cognitive_state, target_concept, misconception (if erroneous)}. Add P as a first-class field in utterances.jsonl. Update script 03 to pass P as part of the model input. Decide whether P is passed explicitly to the evaluated models (as a separate student profile block) or is implicit in U — this is a significant methodological choice that changes what the benchmark measures.

**G3. The Dean's role in this paper diverges from SocraticLM but the paper implies full DTS fidelity**

The paper cites the Dean-Teacher-Student pipeline from SocraticLM (Liu et al., 2024) and says "The Dean agent serves an oversight role, rejecting candidate utterances that are pedagogically implausible or that cannot be derived from C." Script 02 implements exactly this: accept/reject with no revision.

But SocraticLM's Dean is a reviser, not a binary gatekeeper. From Section 3.2: "The Dean judges and revises... T2 ← D(T2). The revised response is then sent to the Student." The Dean corrects the Teacher's output before it reaches the Student — it does not simply discard failures.

The current design is simpler and defensible for SocraticRAG's purposes (we are generating utterances, not full dialogues), but the paper's framing implies more fidelity to DTS than exists. A reviewer familiar with SocraticLM will notice this immediately.

*Decision needed:* Add one sentence to the methodology explicitly noting that SocraticRAG's Dean operates as a validation gate (accept/reject) rather than a revision agent, and state why this is appropriate for single-turn utterance generation. This is a small change but closes a gap a reviewer will flag.

**G4. Erroneous state generated by static list-matching — risks RAG constraint violation at construction time**

The current script passes a hardcoded list of 12 generic ML/DL misconceptions to GPT-4o and asks it to "draw from these where relevant." This is the most dangerous issue because it can silently corrupt the benchmark at its foundation.

The core RAG constraint is that every utterance must be derivable ONLY from concepts explicitly present in C. If GPT-4o anchors the erroneous state to "Attention mechanisms in transformers operate on tokens sequentially" for a chunk about regularization, the misconception is not derivable from C — but it may sound plausible enough that the Dean's accept/reject check passes it anyway. Discerning Minds explicitly flags erroneous states as the hardest and most diagnostically valuable (Section 3.2): "models respond effectively to explicit expressions of understanding or confusion but struggle with implicit cues that require deeper inference such as inferring underlying misconceptions from erroneous responses." If the erroneous utterances in the dataset are not genuinely grounded in C, the benchmark's diagnostic power for Metric 3 is undermined.

The paper's Contribution 4 claims "gold Socratic responses validated by expert educators" — but the utterances themselves (not just the gold responses) need to be grounded. A contaminated erroneous utterance is not fixed by having a good gold response.

*Decision needed:* Remove the static misconception list. Replace with a two-step generation: (1) LLM identifies the key concept in C and what a correct vs. incorrect understanding of that specific concept looks like, derived only from C; (2) LLM generates the erroneous utterance based on the C-derived misunderstanding. This ensures the misconception is derivable from C, not imported from a generic list.

---

## Version 1.2 (Addendum) — 2026-05-23

### H. Design Rationale: Stateless Per-Chunk Profiles (Deliberate Choice, Not an Issue)

**H1. Why SocraticRAG uses per-chunk profiles instead of persistent student archetypes**

During implementation, the question arose whether Student Profile P should be a persistent student archetype (a single student with defined prior knowledge, demographics, and consistent misconception patterns across all chunks) rather than a freshly constructed profile per chunk. This was considered and explicitly rejected. The rationale is documented here for professor review and paper defense.

**The case for persistent profiles (why it seems appealing):**
Real students have consistent cognitive patterns across topics. A student with weak mathematical foundations will likely struggle with gradient descent AND backpropagation AND regularization in correlated ways. Persistent profiles grounded in student typology literature (VanLehn, 2011; Corbett & Anderson, 1994) would make the benchmark more ecologically valid.

**Why per-chunk profiles are the correct design for SocraticRAG:**

1. *SocraticRAG evaluates a single interaction, not a learning trajectory.* The benchmark measures whether a model generates a retrieval-faithful Socratic question in one turn given (C, P, U). Metrics 1 and 2 are entirely chunk-dependent and do not change based on who the student is. Metric 3 checks whether the model perceives and adapts to the student's state in this interaction — it does not measure cross-chunk consistency. Persistent profiles measure a different research question: cross-topic model consistency over a learning session. That is a valid question for a different benchmark.

2. *Persistent profiles would import misconceptions that violate the RAG constraint.* A student archetype defined by "weak mathematical foundations" will naturally express misconceptions drawn from their general profile, not exclusively from chunk C. This breaks the central constraint of SocraticRAG — that every element of the scenario must be derivable from C. A persistent profile and a per-chunk RAG faithfulness constraint are structurally in tension.

3. *The ITS literature supports per-interaction knowledge component modeling.* VanLehn (2011) establishes that the most effective ITS student models track knowledge at the knowledge-component level — per concept, per interaction — rather than via global student archetypes. Corbett & Anderson's (1994) Knowledge Tracing model, the field's dominant approach, updates per skill per interaction. SocraticRAG's profile construction aligns with this: P = {state, target_concept, misconception} is a knowledge-component-level snapshot, not a global student model.

4. *Documented misconception taxonomies support concept-level seeding.* Research on ML/CS student misconceptions (Doğan et al., WiPSCE 2024) identifies misconceptions at the concept level (e.g., "Continuous Learning," "Programmed Behavior") — not at the student archetype level. Seeding erroneous states from concept-level misconception research is epistemically consistent with the per-chunk design.

**What persistent profiles would contribute (future work):**
Cross-chunk consistency evaluation — testing whether a model treats "Student A" coherently across five different chunks — is a meaningful contribution for a future benchmark focused on longitudinal tutoring. It is explicitly out of scope for SocraticRAG v1, which targets the single-interaction RAG faithfulness problem.

**Decision: stateless per-chunk profiles are the correct design. No change needed.**

*Supporting literature:*
- VanLehn, K. (2011). The relative effectiveness of human tutoring, intelligent tutoring systems, and other tutoring systems. *Educational Psychologist*, 46(4), 197–221. DOI: 10.1080/00461520.2011.611369
- Corbett, A. T., & Anderson, J. R. (1994). Knowledge tracing: Modeling the acquisition of procedural knowledge. *User Modeling and User-Adapted Interaction*, 4(4), 253–278.
- Doğan, M. et al. (2024). Identifying secondary school students' misconceptions about machine learning: An interview study. *WiPSCE 2024*. DOI: 10.1145/3677619.3678114

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

## Version 1.0 — 2026-05-03

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
The proposal cites EULER as "the only fine-tuned Socratic model with a publicly available pipeline and evaluation rubric." The code is on GitHub (confirmed: [https://github.com/GiovanniGatti/socratic-llm](https://github.com/GiovanniGatti/socratic-llm)). Whether the fine-tuned weights are released needs verification.
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

