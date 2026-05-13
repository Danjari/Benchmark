# Session Handoff — SynapsEd Capstone 2 Paper
**Date:** 2026-05-12  
**Project:** SynapsEd capstone paper, library submission (end-of-year)  
**Working directory:** `/Users/mahamadoumoudjahidmahamadounouroudini/Code/Benchmark/capstone_paper_Dec2025/`

---

## What This Session Did

### 1. Osis Skill Updated
Osis upgraded from v1.5.1 → v1.9.4. No structural migration needed (protocol shape stayed at 1.0).

### 2. Understood the Full Context
- **capstone1.tex** — the Semester 1 completion report. Fully read. This is the base document.
- **main.tex** — an earlier proposal version (has a Budget section, different advisor: Nancy Gleason). Ignore for capstone2.
- **refs.bib** — existing bibliography with ~12 citations already in capstone1.

### 3. Created capstone2.tex
A copy of capstone1.tex lives at `capstone_paper_Dec2025/capstone2.tex`. It is currently identical to capstone1. The next agent writes into this file.

### 4. Created sources.md
`capstone_paper_Dec2025/sources.md` — 8 new candidate papers with DOI links and roles. Wollny (2021) is marked "No existent" (link dead). All others are verified accessible.

### 5. Created citation-notes.md
`capstone_paper_Dec2025/citation-notes.md` — **THE MOST IMPORTANT FILE.** Contains exact quotes with page numbers, BibTeX keys, and where each quote goes in capstone2.tex. 6 papers fully documented. Do not re-read the PDFs — everything needed is in this file.

### 6. Paper Review — STOPPED
The user decided to stop reviewing new papers. We have enough: ~12 from capstone1 + 6-7 new ones = ~20 total. Additional RAG/NLP/benchmark citations can be borrowed from:
- `Benchmark/sources.md` — the SocraticRAG benchmark paper's full source list (rich: RAGAS, SocraticLM, MathTutorBench, FActScore, etc.)
- capstone1's existing refs.bib (already has Lewis RAG, Herrmann-Werner, Ausubel, ColPali, TutorLLM, etc.)

---

## File Map — Everything That Exists

```
capstone_paper_Dec2025/
  capstone1.tex          ← Original S1 paper. READ ONLY. Source of truth for S1 content.
  capstone2.tex          ← WORKING FILE. Currently = capstone1 copy. Write here.
  refs.bib               ← Existing citations. Add new BibTeX entries here.
  sources.md             ← 8 new paper candidates with links and roles.
  citation-notes.md      ← Exact quotes + BibTeX entries for 6 papers. USE THIS.
  main.tex               ← Ignore. Old proposal version.
  abstract.tex           ← Ignore. Older draft.
  newSources/            ← PDFs of new papers.
    instructional Videos2021-42922-001.pdf    → Mayer (2021)
    s10648-015-9348-9.pdf                     → Fiorella & Mayer (2016)
    s10648-016-9365-3.pdf                     → Rau (2017)
    s40593-018-0168-1.pdf                     → Walkington & Bernacki (2019)
    bloom-1984-the-2-sigma-problem-...pdf     → Bloom (1984)
    s10648-007-9047-2.pdf                     → Moreno & Mayer (2007)
    Nine Ways to Reduce Cognitive Load...pdf  → Mayer & Moreno (2003) — OPTIONAL, superseded
    Dual Coding theory and education.pdf      → Clark & Paivio (1991) — DROP, superseded
  figures/               ← All existing figures for capstone1 (system diagrams, UI screenshots)
  stylefiles/            ← LaTeX style. Do not touch.

Benchmark/
  sources.md             ← SocraticRAG benchmark paper sources. Use for RAG/NLP citations if needed.
  benchmark paper.md     ← The benchmark paper itself.
```

---

## What capstone2.tex Must Become

### Metadata Changes (top of file)
```latex
\capstoneyear{2026}
\capstonedocument{Project 2}      % was: Seminar
\capstonesemester{Spring}
% Advisors stay the same:
\advisors{Hanan Salam, Djellel Difallah}
```

### Structure (professor's required format)
The professor explicitly gave this structure. Follow it exactly:

1. **Abstract** — rewrite to cover both semesters + 3 new features + 2 planned EMNLP papers
2. **Introduction** — keep but tighten (same motivation, shorter)
3. **Related Work** — keep capstone1 structure, add one paragraph on multimodal learning (voice/drawing) citing Mayer 2021 + Fiorella & Mayer 2016 + Rau 2017
4. **Summary of Work Across Both Semesters** — NEW SECTION. Two sub-sections: S1 (core system built) and S2 (3 new features added)
5. **Technical Description** — keep ALL existing TikZ diagrams and component descriptions from capstone1. Add 3 new subsections (one per S2 feature) with their own diagrams if available.
6. **Results, Evaluation, or Outcomes** — frame as: (a) S1 expert consultation = result; (b) S2 feature implementation = outcome; (c) 2 EMNLP papers in progress = future evaluation
7. **Limitations and Future Directions** — evaluation not yet conducted; features still under development; longitudinal study planned for summer
8. **References**

### Keep the Diagrams
User explicitly said: **keep all TikZ flowcharts and figures**. Do not compress or remove any diagrams. The paper can be longer than 10 pages.

### What to Trim
Only trim verbose prose (long paragraphs that repeat what diagrams already show). The diagrams stay. The paper structure content stays. Just tighten the text around diagrams.

---

## The Three Semester 2 Features to Write

### Feature 1: Voice-Based Learning
- **What it does:** Student speaks to the AI tutor; AI speaks back. Bidirectional voice interaction.
- **Tech:** Text-to-speech + speech-to-text. Implemented in SynapsEd.
- **Citations to use** (all in citation-notes.md):
  - Mayer (2021) `mayer2021instructional` — modality principle, d=1.90 effect size
  - Moreno & Mayer (2007) `moreno2007interactive` — dialoguing interactivity, bidirectional voice
  - Fiorella & Mayer (2016) `fiorella2016generative` — generative learning framework
- **Key quote to anchor section:** "the presentation of verbal materials in the auditory modality and non-verbal materials in the visual modality" prevents cognitive overload (Moreno & Mayer, 2007, p. 310)

### Feature 2: Drawing-Based Visual Explanation
- **What it does:** AI generates Excalidraw diagrams to explain concepts. Triggered by: (a) student's onboarding survey indicated visual preference, OR (b) concept is spatial/geometric by nature.
- **CRITICAL FRAMING:** Do NOT write "visual learner." Write "students who expressed a preference for visual explanations in the onboarding survey." This avoids the discredited learning-styles matching hypothesis.
- **Tool:** Excalidraw (cite as software: `https://github.com/excalidraw/excalidraw`)
- **Citations to use** (all in citation-notes.md):
  - Rau (2017) `rau2017visual` — visual reps in STEM; "make abstract concepts accessible"; effective for low-prior-knowledge students
  - Fiorella & Mayer (2016) `fiorella2016generative` — drawing effect d=0.81; spatial content benefits most from drawing
  - Walkington & Bernacki (2019) `walkington2019personalizing` — ITS personalization to student profile justification
- **Key quote:** "visual representations can help students learn because they make abstract concepts accessible" (Rau, 2017, p. 718)

### Feature 3: Mastery-Gated Quizzes
- **What it does:** Students complete 2-3 in-chat quizzes (already existed in S1 as "in-chat assessments"). If they score highly, the formal quiz section for that node unlocks. The goal: accountability + confirmation of learning before advancing.
- **Status:** Still under development; not yet empirically validated in SynapsEd.
- **Connected to S1:** The DKT (Deep Knowledge Tracing) component from S1 tracks performance. The mastery gate is built on top of this.
- **Citations to use:**
  - Bloom (1984) `bloom1984sigma` — THE mastery learning citation; 1 SD gain; 70% of mastery students reach top-20% threshold
  - VanLehn (2011) `vanlehn2011relative` — ITS effectiveness meta-analysis (**PDF still needed**)
  - Kulik & Fletcher (2016) `kulik2016effectiveness` — ITS meta-analysis (**PDF still needed**)
  - Shute (2008) `shute2008focus` — formative feedback design (**PDF still needed**)
- **Key quote:** "the average mastery learning student was above 84% of the students in the control class" (Bloom, 1984, p. 4)

---

## BibTeX Entries Ready to Add to refs.bib

Copy these directly into `refs.bib`:

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

@misc{excalidraw2024,
  author    = {{Excalidraw Contributors}},
  title     = {Excalidraw: Virtual whiteboard for sketching hand-drawn like diagrams},
  year      = {2024},
  howpublished = {GitHub},
  url       = {https://github.com/excalidraw/excalidraw}
}
```

---

## Citations Still Needed (PDFs Not Yet Provided)

Three papers from the mastery section have no PDFs. The next agent can either:
- Ask the user to provide the PDFs, then read and add to citation-notes.md before writing that section
- OR proceed without them and add the Bloom (1984) quote alone, which is sufficient

| BibTeX key | Full citation | Where to find |
|---|---|---|
| `vanlehn2011relative` | VanLehn, K. (2011). The relative effectiveness of human tutoring, intelligent tutoring systems, and other tutoring systems. *Educational Psychologist*, 46(4), 197–221. | DOI: 10.1080/00461520.2011.611369 |
| `kulik2016effectiveness` | Kulik, J. A., & Fletcher, J. D. (2016). Effectiveness of intelligent tutoring systems: A meta-analytic review. *Review of Educational Research*, 86(1), 42–78. | DOI: 10.3102/0034654315581420 |
| `shute2008focus` | Shute, V. J. (2008). Focus on formative feedback. *Review of Educational Research*, 78(1), 153–189. | DOI: 10.3102/0034654307313795 |

**Also:** Wollny (2021) chatbot review link is dead. Check `https://doi.org/10.1016/j.caeai.2021.100033` (Okonkwo & Ade-Ibijola, 2021) as a replacement if a voice/chatbot-in-education systematic review is still needed.

---

## Framing Decisions (Do Not Contradict These)

1. **"Results" section** — no user study was conducted due to timing and external circumstances (war situation). Frame: S1 expert consultation (8 instructors, 6 students) = empirical result. S2 features = deliverable outcomes. Future evaluation = 2 EMNLP papers (benchmark + longitudinal study).

2. **Two EMNLP papers** being prepared:
   - **SocraticRAG benchmark** — evaluates the technology (NLP, RAG, Socratic question quality). Full details in `Benchmark/sources.md` and `Benchmark/benchmark paper.md`.
   - **Longitudinal study** — evaluates system effectiveness with real students/instructors over summer.

3. **"Visual learner" framing is banned.** Write: "students who expressed a preference for visual explanations in the onboarding survey." Reason: the learning styles matching hypothesis (Pashler et al., 2008) is heavily contested in the literature.

4. **All modalities available to all students.** Profile data prioritizes which is surfaced first, not which is withheld.

5. **Mastery gate is still under development.** Write this honestly in the paper. Don't claim it works — frame it as a design hypothesis being implemented and tested in the upcoming longitudinal study.

---

## Next Steps — In Order

1. **Add the 6 BibTeX entries** above to `refs.bib`.
2. **Update capstone2.tex metadata** (year, document type) — see Metadata Changes section above.
3. **Rewrite the Abstract** for both semesters + S2 features + 2 EMNLP papers.
4. **Keep Introduction and Related Work** from capstone1, trim only verbose prose. Add one paragraph to Related Work on multimodal learning (cite Mayer 2021, Fiorella & Mayer 2016).
5. **Keep all 4 existing system components** and their TikZ diagrams verbatim.
6. **Write 3 new subsections** for S2 features using quotes from citation-notes.md. One subsection per feature.
7. **Rewrite the Evaluation section** to: S1 consultation results (existing), S2 feature implementation, future evaluation plan (two EMNLP papers).
8. **Write Limitations** — honest: no user study yet, mastery threshold not empirically validated, features under development.
9. **Update the Timeline section** — S1 is complete, S2 produced the 3 features (not the planned user study).
10. **Compile and check** the LaTeX compiles without errors.

---

## About the User

- Name: Moudjahid Nouroudini Moussa, mm12515@nyu.edu
- Institution: Computer Science, NYUAD
- Advisors: Hanan Salam, Djellel Difallah
- Working on two simultaneous tracks: (1) this capstone library submission, (2) SocraticRAG benchmark paper for EMNLP 2026 (deadline: May 25, 2026)
- Communication style: direct, prefers concrete action over discussion, pushes back on old references and unnecessary verbosity

---

*Handoff written: 2026-05-12. Next agent: read this file first, then citation-notes.md, then open capstone2.tex and start writing.*
