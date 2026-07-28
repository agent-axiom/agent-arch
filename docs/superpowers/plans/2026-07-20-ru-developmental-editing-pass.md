# Russian Manuscript Developmental Editing Pass Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove the remaining editorial-assembly feel from the Russian manuscript while preserving its technical contracts, reproducible examples, source apparatus, and existing Google Doc.

**Architecture:** Keep `docs/publisher/tools/revise_ru_manuscript.py` as the deterministic semantic source of the generated manuscript. Add one final, idempotent developmental-editing pass, test its observable manuscript invariants, then add live internal references in the DOCX renderer. Rebuild and visually verify both the Google-oriented and `Template2000n` derivatives before applying targeted native edits to the existing Google Doc.

**Tech Stack:** Python 3.12, pytest, Markdown, python-docx/OOXML, LibreOffice/Poppler render QA, Google Docs API through the Google Drive connector.

---

### Task 1: Consolidate Chapter Architecture

**Files:**
- Modify: `tests/test_ru_manuscript_revision.py`
- Modify: `docs/publisher/tools/revise_ru_manuscript.py`
- Regenerate: `docs/publisher/ru-manuscript-editorial-2026-07-13.md`

- [x] Add a failing test asserting that chapter 1 contains one conclusion, no editorial labels such as `Доказательства: кратко`, and leaves the detailed execution-form matrix to chapter 2.
- [x] Add a failing test asserting that chapters 5, 11, 20, 24, and 26 contain four to seven top-level instructional acts while preserving `Ключевые выводы` and `Источники главы`.
- [x] Run the two tests and confirm they fail against the current generated manuscript.
- [x] Implement `apply_developmental_editing_pass_2026_07_20()` as the final semantic transformation before table captions.
- [x] Re-run the focused tests and the reproducibility test.

### Task 2: Improve Narrative Rhythm Without Losing Checklists

**Files:**
- Modify: `tests/test_ru_manuscript_revision.py`
- Modify: `docs/publisher/tools/revise_ru_manuscript.py`
- Regenerate: `docs/publisher/ru-manuscript-editorial-2026-07-13.md`

- [x] Add a failing test that removes the seven-line blank seam in chapter 24 and caps ordinary list blocks in the selected dense chapters.
- [x] Convert causal and explanatory lists in chapters 5, 20, and 24 into short prose sequences; retain lists used for procedures, acceptance criteria, and source entries.
- [x] Integrate the chapter 1 evidence/alternative-view labels into ordinary authorial prose.
- [x] Normalize chapter openings to hook, learning outcomes, and artifact; keep optional reading guidance only where the chapter has multiple routes.
- [x] Normalize chapter endings to key takeaways, one practical next step, and sources.

### Task 3: Turn Labs Into Discrete Learning Steps

**Files:**
- Modify: `tests/test_ru_manuscript_revision.py`
- Modify: `docs/publisher/tools/revise_ru_manuscript.py`
- Regenerate: `docs/publisher/ru-manuscript-editorial-2026-07-13.md`

- [x] Add a failing test requiring every laboratory to contain named steps, an expected observation for executable steps, and a closing statement explaining what the result proves.
- [x] Preserve the existing prerequisites, timing, negative check, diagnosis, extension, and cumulative artifact in all eight labs.
- [x] Split grouped command sequences in labs 2, 4, 5, 6, 7, and 8 into named steps without changing executable command text.
- [x] Add explicit design/inspection steps to labs 1 and 3 so the same lab contract applies without pretending that every exercise is code-driven.
- [x] Re-run all laboratory and runtime contract tests.

### Task 4: Add Stable DOCX Cross-References

**Files:**
- Modify: `tests/test_publisher_docx.py`
- Modify: `docs/publisher/tools/build_ru_editorial_docx.py`

- [x] Add failing OOXML tests requiring bookmarks for numbered chapters, figures, tables, and listings.
- [x] Add failing tests requiring internal hyperlinks for prose references such as `глава 16`, `рисунок 3`, `таблица 4`, and `листинг 12`.
- [x] Implement deterministic bookmark names and internal `w:hyperlink` anchors while preserving external hyperlinks and inline formatting.
- [x] Ensure captions do not link to themselves and bookmark identifiers are unique.
- [x] Run publisher DOCX tests and inspect generated `word/document.xml`.

### Task 5: Rebuild and Verify Publisher Artifacts

**Files:**
- Create: `docs/publisher/ru-developmental-editing-pass-2026-07-20.md`
- Create: `docs/publisher/artifacts/agent-arch-ru-google-doc-developmental-edit-2026-07-20.docx`
- Create: `docs/publisher/artifacts/agent-arch-ru-google-doc-developmental-edit-2026-07-20.pdf`
- Create: `docs/publisher/artifacts/agent-arch-ru-template2000n-developmental-edit-2026-07-20.docx`
- Create: `docs/publisher/artifacts/agent-arch-ru-template2000n-developmental-edit-2026-07-20.pdf`

- [x] Regenerate the canonical manuscript from `ru-manuscript-google-doc-final-2026-07-11.md` and prove byte-for-byte reproducibility.
- [x] Build the Google-oriented DOCX and the `Template2000n` derivative.
- [x] Render both DOCX files to PDF and page PNGs using the bundled document runtime.
- [x] Inspect representative front matter, dense chapters, all laboratories, figures/tables/listings, and final pages; run automated blank-page, overflow, font, image, and bookmark audits.
- [x] Record word count, page count, headings, lists, figures, tables, listings, cross-references, and test results in the dated report.

### Task 6: Synchronize the Existing Google Doc

**Files:**
- Modify: `docs/publisher/ru-manuscript-evolution.md`
- Modify: `docs/publisher/ru-source-map.md`
- Modify: `docs/publisher/ru-google-doc-workflow.md`

- [x] Perform the required trusted read of the existing Google Doc and confirm the target revision and tab topology.
- [x] Apply only the text and heading changes produced by this pass to the existing document; do not replace the file or discard editor comments.
- [x] Re-read all changed anchors and verify chapter order, heading roles, laboratory steps, figures, tables, links, and author placeholders.
- [x] Export the updated Google Doc as DOCX, render it, and compare its text and media inventory with the canonical manuscript.
- [x] Record the final Google revision, exported page count, and remaining author-owned fields.

### Task 7: Final Verification and Review

**Files:**
- Test: `tests/test_ru_manuscript_revision.py`
- Test: `tests/test_publisher_docx.py`
- Test: `tests/test_review_remediations.py`

- [x] Run the focused manuscript and publisher tests.
- [x] Run the full repository test suite and `ruff` for changed Python files.
- [x] Run a specification review against this plan.
- [x] Run an independent editorial/quality review of the final generated manuscript and rendered artifacts.
- [x] Leave the working tree uncommitted unless the user explicitly requests a commit and push.
