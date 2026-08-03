# Russian Manuscript Reader Experience Design

## Goal

Make the Russian publisher manuscript easier to enter, easier to read in long
sessions, and more valuable as a book readers return to during design reviews,
incidents, and release decisions.

## Current State

The manuscript already has a mature teaching structure: 28 chapter learning
contracts, eight part routes, eight laboratories, a cumulative evidence
artifact, a recurring support-agent case, 37 listings, 25 numbered figures,
29 inline diagrams, checklists, glossary routes, and a capstone. Earlier passes
also removed most editorial-assembly residue and reduced list density.

The remaining opportunity is therefore not another visible recurring rubric.
It is a targeted reader-experience delta:

1. provide a task- and symptom-oriented route back into the book;
2. replace abstract reading instructions in selected dense chapters with a
   concrete decision or failure;
3. make the laboratory method explicit once, before the practical route;
4. make the book's reusable engineering patterns easy to retrieve;
5. preserve technical precision, reproducibility, source traceability, and the
   established publisher layout.

## Chosen Approach

Use a hybrid book structure: narrative entry, rigorous explanation, worked
artifact, negative path, and reference-quality close. The recurring
`support-triage-ref` case remains the main narrative line. Reader navigation is
concentrated in the introduction and appendices instead of repeated in every
chapter.

## Content Changes

### Entry And Return Routes

Add a compact "start from your situation" navigator after the existing reading
routes. It maps eight common engineering needs to chapters, laboratories, and
the artifact the reader should produce. Add a symptom-oriented navigator and a
short reusable-pattern catalog at the start of Appendix 2.

### Dense Chapter Openings

Revise the meta openings of chapters 5, 11, and 26 into concrete moments from
the support-agent case. Tighten the entry to chapters 15 and 24 only where it
repeats surrounding explanation. Chapters 1 and 28 already have strong direct
openings and should serve as controls rather than receive gratuitous changes.

### Practical Learning Loop

Add one laboratory protocol before the first practical route: predict, run,
compare, explain, and save the evidence. Keep the existing lab-specific steps,
observations, negative checks, diagnostics, and cumulative manifest. Do not add
a new repeated label to all eight labs.

### Visual Reading

Keep the existing 56-image set unless an audit finds a factual or logical gap.
Numbered figure captions remain concise labels; the following prose must state
the decision or invariant the figure teaches. Generic or redundant nearby
explanations may be tightened, but image order, dimensions, and alt text must
remain stable.

### Voice And Density

Prefer concrete subjects and verbs, Russian-first terminology, and direct
questions at genuine decision points. Remove meta narration that tells the
reader that a chapter is useful without showing why. Do not add jokes,
fictional author experience, motivational filler, or decorative stories.

## Deterministic Source And Outputs

The semantic change belongs in
`docs/publisher/tools/revise_ru_manuscript.py`, after
`apply_editorial_pass_2026_08_01()`. The generated canonical manuscript remains
`docs/publisher/ru-manuscript-editorial-2026-07-13.md`. Tests must prove
byte-for-byte regeneration from the source snapshot.

The pass also regenerates the editorial index and learning packets, the
Google-oriented DOCX/PDF, the Template2000n DOCX/PDF, and the existing Google
Doc. Existing comments, inline objects, tables, links, and tab topology must be
preserved during native synchronization.

## Acceptance Criteria

1. The introduction contains one task-oriented route with all eight parts and
   no new per-chapter rubric.
2. Appendix 2 provides direct routes for at least eight recognizable symptoms
   and names the book's reusable engineering patterns.
3. Chapters 5, 11, and 26 open on a concrete decision or failure before their
   first abstract explanation.
4. The practical route states the predict-run-compare-explain-save protocol
   once; all eight laboratories retain their existing contracts.
5. Counts stay at 28 chapters, eight parts, eight labs, 37 listings, 25 numbered
   figures, 29 inline diagrams, 56 total images, and 11 tables unless a verified
   correction requires otherwise.
6. Full manuscript, runtime, DOCX, accessibility, geometry, font, and strict
   three-locale documentation checks pass.
7. The Google Doc readback contains every new anchor and preserves all native
   images, tables, links, and tab structure.
