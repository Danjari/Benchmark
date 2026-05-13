# SynapsEd Capstone 2 — Citation Notes

For each paper: exact quotes, page numbers, proposed BibTeX key, and where it lands in capstone2.tex.
Do NOT re-read these PDFs. Everything needed is captured here.

---

## PAPER 1 — Mayer (2021)

**Full citation:** Mayer, R. E. (2021). Evidence-based principles for how to design effective instructional videos. *Journal of Applied Research in Memory and Cognition*, 10(2), 229–240.
**DOI:** https://doi.org/10.1016/j.jarmac.2021.03.007
**Proposed BibTeX key:** `mayer2021instructional`
**PDF file:** `instructional Videos2021-42922-001.pdf`
**Status:** FULLY READ

**Where it goes in capstone2.tex:** Section on Voice Feature (Semester 2 additions). Justifies spoken narration as superior to on-screen text.

**Exact quotes to use:**

1. The modality principle (p. 229, abstract table):
   > "modality (present words as spoken text)"
   Use: When introducing the voice feature design rationale — the system delivers AI responses as spoken audio because modality principle research shows spoken narration outperforms text on screen.

2. The voice principle (p. 229, abstract table):
   > "voice (use appealing human voice)"
   Use: Alongside the modality quote — cite both as design constraints SynapsEd's voice feature operationalizes.

3. Multimedia + narration effect size (p. 232):
   > "students performed better on a transfer posttest after receiving a narrated animation than after receiving narration alone, yielding a median effect size of d = 1.90"
   Use: Quantitative backing. Strongest number in the paper for why multimodal (voice + visual) delivery improves learning.

4. Core multimedia principle (p. 232):
   > "people learn better from words and graphics than from words alone"
   Use: Opening sentence when introducing the theoretical basis for multimodal delivery.

5. Dual channels basis (p. 230, Table 1):
   > "People have separate channels for processing visual and verbal information"
   Use: When explaining WHY voice + drawing together (two modalities) is more effective than text alone.

**BibTeX entry to add to refs.bib:**
```bibtex
@article{mayer2021instructional,
  author    = {Mayer, Richard E.},
  title     = {Evidence-based principles for how to design effective instructional videos},
  journal   = {Journal of Applied Research in Memory and Cognition},
  volume    = {10},
  number    = {2},
  pages     = {229--240},
  year      = {2021},
  doi       = {10.1016/j.jarmac.2021.03.007}
}
```

---

## PAPER 2 — Fiorella & Mayer (2016)

**Full citation:** Fiorella, L., & Mayer, R. E. (2016). Eight ways to promote generative learning. *Educational Psychology Review*, 28(4), 717–741.
**DOI:** https://doi.org/10.1007/s10648-015-9348-9
**Proposed BibTeX key:** `fiorella2016generative`
**PDF file:** `s10648-015-9348-9.pdf`
**Status:** FULLY READ

**Where it goes in capstone2.tex:** Two places — (1) Voice Feature section, for generative processing theory. (2) Drawing Feature section, for the "learning by drawing" generative effect.

**Exact quotes to use:**

1. Core generative learning definition (p. 717, abstract):
   > "Generative learning involves actively making sense of to-be-learned information by mentally reorganizing and integrating it with one's prior knowledge, thereby enabling learners to apply what they have learned to new situations."
   Use: When framing why both voice and drawing are not cosmetic features but generative learning mechanisms.

2. The eight strategies — drawing is one of them (p. 717):
   > "eight learning strategies intended to promote generative learning: summarizing, mapping, drawing, imagining, self-testing, self-explaining, teaching, and enacting"
   Use: To establish that BOTH voice (activates imagining/self-explaining) AND drawing are research-validated generative strategies — not ad hoc features.

3. Why drawing works — the mechanism (p. 724):
   > "the act of translating from text to a pictorial representation prompts the learner to select the relevant information from the text, show its organization spatially in a drawing, and use prior knowledge to clarify the meaning of the text and its relation to the drawing"
   Use: In the Drawing Feature section — this is the exact mechanism the AI-generated Excalidraw diagrams trigger in the student.

4. Drawing effect size (p. 724):
   > "the drawing group outperformed the control group, yielding a large effect size (d=0.81)"
   Use: Quantitative backing for the drawing feature alongside the Rau (2017) review evidence.

5. Generative drawing effect (p. 724):
   > "people learn better from a scientific text when they are provided with support in how to create a drawing that depicts the material in the text"
   Use: When explaining why SynapsEd provides AI-generated drawings rather than just text explanations — it reduces the mechanical burden of drawing while preserving the generative benefit.

6. Spatial concept boundary condition (p. 724, near boundary conditions):
   > "When the material is highly spatial, such as in physics or chemistry, other generative learning strategies are likely more appropriate (e.g., imagining, mapping, drawing, or enacting)"
   Use: To justify the AI's adaptive logic — drawing is triggered for spatially complex concepts (e.g., Pythagorean theorem geometry), not for all content indiscriminately.

**BibTeX entry to add to refs.bib:**
```bibtex
@article{fiorella2016generative,
  author    = {Fiorella, Logan and Mayer, Richard E.},
  title     = {Eight ways to promote generative learning},
  journal   = {Educational Psychology Review},
  volume    = {28},
  number    = {4},
  pages     = {717--741},
  year      = {2016},
  doi       = {10.1007/s10648-015-9348-9}
}
```

---

## PAPER 3 — Walkington & Bernacki (2019)

**Full citation:** Walkington, C., & Bernacki, M. L. (2019). Personalizing algebra to students' individual interests in an intelligent tutoring system: Moderators of impact. *International Journal of Artificial Intelligence in Education*, 29(1), 58–88.
**DOI:** https://doi.org/10.1007/s40593-018-0168-1
**Proposed BibTeX key:** `walkington2019personalizing`
**PDF file:** `s40593-018-0168-1.pdf`
**Status:** FULLY READ

**Where it goes in capstone2.tex:** Drawing Feature section (adaptive modality selection based on student profile). Also usable in Introduction when discussing personalization in ITS broadly.

**IMPORTANT framing note:** This paper is about connecting math problems to student interests (sports, games), NOT about visual/verbal modality selection. The connection to SynapsEd is through the broader principle: personalizing ITS content delivery to student-expressed preferences improves learning. Do NOT overstate — cite it as evidence that ITS personalization to student profile yields learning benefits, which motivates our adaptive modality selection (student survey → drawing triggered for visual preference students).

**Exact quotes to use:**

1. Core finding on personalization in ITS (p. 58, abstract):
   > "connecting to students' individual interests can be used to personalize learning using an Intelligent Tutoring System (ITS)"
   Use: When establishing the scientific basis for SynapsEd's profile-driven feature selection.

2. AI in education and personalization as priority (p. 59):
   > "Accounting for the different experiences, goals, and backgrounds of students through personalization and individualized pathways is cited as an important focus for those interested in artificial intelligence in education"
   Use: In Related Work or Introduction — frames personalization as a recognized AI-in-education research direction, not an engineering novelty.

3. Depth of personalization matters (p. 58, abstract):
   > "benefits may only be realized when students' degree of quantitative engagement with their out-of-school interests matches the depth at which the personalized problems are written"
   Use: Carefully — this supports the idea that shallow personalization (just changing the topic label) is not enough. SynapsEd's profile-driven modality selection aims for deeper alignment (student expressed preference → actual change in delivery format). Shows we're aware of the nuance.

4. Engagement reduction when personalized (p. 58, abstract):
   > "connecting math instruction to students' out-of-school interests can be beneficial for learning in an ITS and reduces gaming the system"
   Use: In the gated quiz section — connect personalization to reduced gaming behavior (students who feel the system is adapted to them are less likely to click through answers).

**BibTeX entry to add to refs.bib:**
```bibtex
@article{walkington2019personalizing,
  author    = {Walkington, Candace and Bernacki, Matthew L.},
  title     = {Personalizing algebra to students' individual interests in an intelligent tutoring system: {M}oderators of impact},
  journal   = {International Journal of Artificial Intelligence in Education},
  volume    = {29},
  number    = {1},
  pages     = {58--88},
  year      = {2019},
  doi       = {10.1007/s40593-018-0168-1}
}
```

---

## PAPER 4 — Bloom (1984)

**Full citation:** Bloom, B. S. (1984). The 2 sigma problem: The search for methods of group instruction as effective as one-to-one tutoring. *Educational Researcher*, 13(6), 4–16.
**DOI:** https://doi.org/10.3102/0013189X013006004
**Proposed BibTeX key:** `bloom1984sigma`
**PDF file:** `bloom-1984-the-2-sigma-problem-the-search-for-methods-of-group-instruction-as-effective-as-one-to-one-tutoring.pdf`
**Status:** FULLY READ

**Where it goes in capstone2.tex:** Mastery-Based Assessment Gating section. The anchor citation.

**Exact quotes to use:**

1. The 2-sigma result — tutoring (p. 4):
   > "the average student under tutoring was about two standard deviations above the average of the control class (the average tutored student was above 98% of the students in the control class)"
   Use: As the motivating benchmark — SynapsEd's intelligent tutoring agent aims toward this ideal of individualized one-on-one tutoring at scale.

2. The mastery learning result (p. 4):
   > "The average student under mastery learning was about one standard deviation above the average of the control class (the average mastery learning student was above 84% of the students in the control class)"
   Use: When introducing the gated quiz design — mastery learning alone (without full tutoring) still produces 1 SD gain. The gated quiz operationalizes mastery learning at scale.

3. The high achiever comparison (p. 4):
   > "about 90% of the tutored students and 70% of the mastery learning students attained the level of summative achievement reached by only the highest 20% of the students under conventional instructional conditions"
   Use: Strongest framing for why mastery gating matters — it democratizes outcomes that were previously only achievable by the top 20%.

4. Time on task change (p. 4):
   > "There were corresponding changes in students' time on task in the classroom (65% under conventional instruction, 75% under Mastery Learning, and 90+% under tutoring)"
   Use: Optional — supports the claim that mastery-based approaches increase student engagement time, not just achievement.

**BibTeX entry to add to refs.bib:**
```bibtex
@article{bloom1984sigma,
  author    = {Bloom, Benjamin S.},
  title     = {The 2 sigma problem: {T}he search for methods of group instruction as effective as one-to-one tutoring},
  journal   = {Educational Researcher},
  volume    = {13},
  number    = {6},
  pages     = {4--16},
  year      = {1984},
  doi       = {10.3102/0013189X013006004}
}
```

---

## PAPER 5 — Rau (2017)

**Full citation:** Rau, M. A. (2017). Conditions for the effectiveness of multiple visual representations in enhancing STEM learning. *Educational Psychology Review*, 29(4), 717–761.
**DOI:** https://doi.org/10.1007/s10648-016-9365-3
**Proposed BibTeX key:** `rau2017visual`
**PDF file:** `s10648-016-9365-3.pdf`
**Status:** FULLY READ

**Where it goes in capstone2.tex:** Drawing Feature section. Establishes WHEN visual representations help (the conditions), justifying the AI's adaptive decision to draw.

**Exact quotes to use:**

1. Core finding on visual representations in STEM (p. 717, abstract):
   > "Visual representations play a critical role in enhancing science, technology, engineering, and mathematics (STEM) learning. Educational psychology research shows that adding visual representations to text can enhance students' learning of content knowledge, compared to text-only."
   Use: Opening claim for the drawing feature section — cites a 2017 review as primary evidence.

2. Why visual representations help — abstraction (p. 718):
   > "visual representations can help students learn because they make abstract concepts accessible"
   Use: Justification for AI generating a diagram for an abstract concept (e.g., a Pythagorean theorem proof becomes accessible through geometry visualization).

3. Multiple visual representations and mental model (p. 718):
   > "students can construct deeper understanding by integrating them into a coherent mental model of the content"
   Use: When explaining why SynapsEd combines both text explanation AND visual diagram — not redundant but complementary, enabling the student to integrate both into a stronger mental model.

4. The representation dilemma — why support matters (p. 719):
   > "how can students learn new content from visual representations they do not yet fully understand, and—at the same time—learn how visual representations show content they have not yet learned?"
   Use: Justifies why SynapsEd generates the diagram FOR the student rather than asking students to draw themselves — reduces cognitive overhead of the representation dilemma.

5. Conditions for effectiveness — prior knowledge (p. 718):
   > "visual representations are particularly effective if students have low prior knowledge (expertise reversal effect)"
   Use: Connects to SynapsEd's profile data: the system triggers visual explanations especially for students who indicated lower prior knowledge on the onboarding survey.

**BibTeX entry to add to refs.bib:**
```bibtex
@article{rau2017visual,
  author    = {Rau, Martina A.},
  title     = {Conditions for the effectiveness of multiple visual representations in enhancing {STEM} learning},
  journal   = {Educational Psychology Review},
  volume    = {29},
  number    = {4},
  pages     = {717--761},
  year      = {2017},
  doi       = {10.1007/s10648-016-9365-3}
}
```

---

## PAPERS STILL NEEDING PDFs

The following 3 papers from the sources.md new list have no PDFs yet.
Ask the user to locate and share these before writing those sections.

| Paper | BibTeX key | Needed for |
|---|---|---|
| VanLehn (2011) — ITS Effectiveness | `vanlehn2011relative` | Mastery/gated quiz section |
| Kulik & Fletcher (2016) — ITS Meta-Analysis | `kulik2016effectiveness` | Mastery/gated quiz section |
| Shute (2008) — Formative Feedback | `shute2008focus` | Mastery/gated quiz section |

---

## PAPER 1.1 REPLACEMENT NEEDED

Wollny et al. (2021) is marked "No existent" in sources.md — the DOI does not resolve.
Suggested replacement (to verify):
- Okonkwo, C. W., & Ade-Ibijola, A. (2021). Chatbots applications in education: A systematic review. *Computers and Education: Artificial Intelligence*, 2, 100033.
  Candidate link: https://doi.org/10.1016/j.caeai.2021.100033

---

## PAPER 6 — Moreno & Mayer (2007)

**Full citation:** Moreno, R., & Mayer, R. E. (2007). Interactive multimodal learning environments. *Educational Psychology Review*, 19(3), 309–326.
**DOI:** https://doi.org/10.1007/s10648-007-9047-2
**Proposed BibTeX key:** `moreno2007interactive`
**PDF file:** `s10648-007-9047-2.pdf`
**Status:** FULLY READ

**Where it goes in capstone2.tex:** Voice Feature section specifically — this paper covers the bidirectional, conversational dimension of voice interaction (student speaks → AI speaks back). Mayer (2021) covers one-way narration; this paper covers dialogue.

**Exact quotes to use:**

1. Definition of interactive multimodal environment (p. 310):
   > "An interactive multimodal learning environment is one in which what happens depends on the actions of the learner."
   Use: When describing the voice feature — SynapsEd's voice mode is an interactive multimodal learning environment by this definition: student speech triggers AI speech response.

2. Dialoguing as the key interactivity type (p. 311):
   > "In interactivity by dialoguing, the learner can ask a question and receive an answer, or can give an answer and receive feedback."
   Use: The voice feature is precisely this type of interactivity — student speaks a question, AI speaks back. Cite this to ground the design in a recognized framework.

3. Why mixed modality prevents overload (p. 310):
   > "the presentation of verbal and non-verbal materials in the visual modality alone is more likely to overload students' cognitive capacity during learning as compared to the presentation of verbal materials in the auditory modality and non-verbal materials in the visual modality"
   Use: Justifies delivering AI explanations as voice (auditory channel) while visual content is shown on screen — prevents overloading a single channel.

4. Mixed-modality principle (p. 310):
   > "the most effective learning environments are those that combine verbal and non-verbal representations of the knowledge using mixed-modality presentations"
   Use: Pair with Mayer (2021) multimedia principle — two sources, same principle, spanning 14 years.

**BibTeX entry to add to refs.bib:**
```bibtex
@article{moreno2007interactive,
  author    = {Moreno, Roxana and Mayer, Richard E.},
  title     = {Interactive multimodal learning environments},
  journal   = {Educational Psychology Review},
  volume    = {19},
  number    = {3},
  pages     = {309--326},
  year      = {2007},
  doi       = {10.1007/s10648-007-9047-2}
}
```

---

## OLD PAPERS IN FOLDER (not in new 8 list)

The folder also contains three older papers. Notes on whether to keep or drop:

| File | Paper | Decision |
|---|---|---|
| `Nine Ways to Reduce Cognitive Load in Multimedia Learning.pdf` | Mayer & Moreno (2003) | OPTIONAL — superseded by Mayer (2021) for our purposes. Only cite if a reviewer expects the classic 2003 formulation. |
| `s10648-007-9047-2.pdf` | Moreno & Mayer (2007) | KEEP — covers interactive bidirectional voice, which Mayer (2021) does not. Still needed for the voice feature. Read this next. |
| `Dual Coding theory and education.pdf` | Clark & Paivio (1991) | DROP — superseded by Fiorella & Mayer (2016) which covers generative learning more recently. Only add back if a reviewer pushes for the dual coding framing explicitly. |

---

*Updated: 2026-05-12. 6 papers fully documented. 3 PDFs still needed (VanLehn 2011, Kulik & Fletcher 2016, Shute 2008). Wollny 2021 link dead — replacement needed.*
