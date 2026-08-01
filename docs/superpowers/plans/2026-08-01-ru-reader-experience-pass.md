# Russian Manuscript Reader Experience Pass Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Improve entry, reading rhythm, practical learning, and repeat-use value of the Russian publisher manuscript without adding mechanical scaffolding or weakening technical rigor.

**Architecture:** Add one final deterministic reader-experience transformation after the existing August editorial pass. Concentrate navigation in the introduction and Appendix 2, replace selected dense chapter meta openings with concrete case decisions, retain the existing laboratory and visual contracts, then rebuild and synchronize every publisher surface.

**Tech Stack:** Python 3.12, pytest, Markdown, python-docx/OOXML, bundled Documents runtime, Google Docs API through the Google Drive connector, LibreOffice/Poppler render QA.

---

### Task 1: Lock Reader-Experience Invariants

**Files:**
- Modify: `tests/test_ru_manuscript_revision.py`

- [x] Add a failing test for one task-oriented introduction navigator covering all eight parts.
- [x] Add a failing test for the symptom navigator and reusable-pattern catalog in Appendix 2.
- [x] Add a failing test requiring concrete openings in chapters 5, 11, and 26 while keeping chapter counts and learning contracts unchanged.
- [x] Add a failing test for the single predict-run-compare-explain-save laboratory protocol and unchanged eight-lab structure.
- [x] Run the focused tests and confirm that only the new expectations fail.

### Task 2: Implement The Deterministic Editorial Delta

**Files:**
- Modify: `docs/publisher/tools/revise_ru_manuscript.py`
- Regenerate: `docs/publisher/ru-manuscript-editorial-2026-07-13.md`
- Regenerate: `docs/publisher/ru-manuscript-editorial-2026-07-13.manifest.json`

- [x] Add `apply_reader_experience_pass_2026_08_01()` after the existing August pass.
- [x] Insert the task-oriented route after `Как читать книгу`.
- [x] Insert the one-time laboratory learning loop near `Как устроены код и практика`.
- [x] Rewrite the selected chapter openings with exact, idempotent anchors.
- [x] Add the symptom navigator and reusable-pattern catalog to Appendix 2.
- [x] Regenerate the manuscript and prove byte-for-byte reproducibility.
- [x] Run the focused manuscript tests until they pass.

### Task 3: Editorial And Visual Consistency Review

**Files:**
- Modify if required: `docs/publisher/tools/revise_ru_manuscript.py`
- Regenerate if required: `docs/publisher/ru-manuscript-editorial-2026-07-13.md`

- [x] Review all chapter openings for duplicated hooks and meta narration.
- [x] Review all 25 numbered figures and 29 inline diagrams for a nearby explanatory takeaway.
- [x] Scan prose outside code and sources for residual avoidable anglicisms, bureaucratic constructions, exact duplicate paragraphs, and repetitive transitions.
- [x] Apply only verified targeted fixes and re-run the focused tests.

### Task 4: Rebuild Editorial Packets And Publisher Artifacts

**Files:**
- Regenerate: `docs/publisher/ru-index-terms-2026-07-27.md`
- Regenerate: `docs/publisher/ru-learning-outcome-map-2026-07-27.md`
- Regenerate: `docs/publisher/ru-human-review-packet-2026-07-27.md`
- Create: `docs/publisher/artifacts/agent-arch-ru-google-doc-reader-experience-2026-08-01.docx`
- Create: `docs/publisher/artifacts/agent-arch-ru-google-doc-reader-experience-2026-08-01.pdf`
- Create: `docs/publisher/artifacts/agent-arch-ru-template2000n-reader-experience-2026-08-01.docx`
- Create: `docs/publisher/artifacts/agent-arch-ru-template2000n-reader-experience-2026-08-01.pdf`

- [x] Rebuild editorial packets from the regenerated manuscript.
- [x] Build the Google-oriented DOCX from the latest verified publisher base.
- [x] Build the Template2000n derivative and verify text/media equality.
- [x] Render both DOCX files to PDF and page images.
- [x] Run accessibility, style, font, geometry, blank-page, overflow, link, bookmark, table, and image audits.
- [x] Visually inspect the introduction, changed chapters, Appendix 2, all figure placement sheets, and final pages.

### Task 5: Synchronize The Existing Google Doc

**Files:**
- Create: `docs/publisher/ru-reader-experience-pass-2026-08-01.md`
- Modify: `docs/publisher/ru-manuscript-evolution.md`
- Modify: `docs/publisher/ru-google-doc-workflow.md`

- [x] Perform a trusted full read of document `1LyY2Psy2yaobn7VLmOwLTWm4QVrhp2I-ylE2B7V4pp4`, confirm tab `t.0`, controls, and current revision.
- [x] Generate and inspect a paragraph-level synchronization plan against the latest Google-oriented DOCX.
- [x] Apply guarded native updates in descending index order without replacing the document.
- [x] Re-read changed anchors and verify tab topology, headings, links, 56 inline objects, and 11 tables.
- [x] Export the updated Google Doc to DOCX and confirm semantic equality with the canonical manuscript.

### Task 6: Final Review And Repository Handoff

**Files:**
- Create: `docs/publisher/ru-reader-experience-pass-2026-08-01.md`

- [x] Run the full pytest suite, ruff checks, strict MkDocs builds for all three locales, and `git diff --check`.
- [x] Obtain independent narrative, pedagogy, and navigation reviews; resolve all P0/P1 findings.
- [x] Record final word count, page counts, structure counts, Google revision, artifact hashes, QA results, and author-owned fields.
- [x] Stage and commit only the files belonging to this pass; leave unrelated `.tmp/` content untouched.
