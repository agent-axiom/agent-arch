# Russian Technical Book Polish Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Apply the remaining high-value prose, cognitive-load, code-explanation, terminology, and release-governance improvements to the Russian publisher manuscript without duplicating the Online Companion or weakening normative safety contracts.

**Architecture:** Add one final idempotent transformation to `revise_ru_manuscript.py`, guarded by focused manuscript tests. Regenerate the canonical Markdown and publisher packets, rebuild both DOCX/PDF variants, synchronize the existing Google Doc with revision control, and verify every surface against the same semantic source.

**Tech Stack:** Python 3.12, pytest, Markdown, python-docx/OOXML, bundled Documents runtime, LibreOffice/Poppler, Google Docs connector, git.

---

### Task 1: Lock Editorial Invariants

**Files:**
- Modify: `tests/test_ru_manuscript_revision.py`

- [x] Add focused assertions for the revised chapter 4 sentence and Russian-first journal terminology.
- [x] Add assertions for varied narrative phrasing in chapters 5, 11, 15, 24, 26, and 28 while retaining explicit normative contracts.
- [x] Add assertions that chapter 27 explains the expected result, failure signal, and architectural reason around its substantial code examples.
- [x] Run the focused tests and confirm the new assertions fail against the current generated manuscript.

### Task 2: Implement The Deterministic Editorial Pass

**Files:**
- Modify: `docs/publisher/tools/revise_ru_manuscript.py`
- Regenerate: `docs/publisher/ru-manuscript-editorial-2026-07-13.md`
- Regenerate: `docs/publisher/ru-manuscript-editorial-2026-07-13.manifest.json`

- [x] Add `apply_technical_book_polish_2026_08_17()` after the publication-readiness pass.
- [x] Replace only verified narrative occurrences of repetitive modal and transition language; preserve policy, acceptance, checklist, and protocol requirements.
- [x] Simplify the single long sentence in chapter 4 and replace the remaining avoidable use of `логирование`.
- [x] Tighten transitions in chapters 5, 11, 15, and 24 without adding headings or repeated summaries.
- [x] Strengthen chapter 27 explanations around substantial code examples without expanding the code itself.
- [x] Regenerate twice and prove byte-for-byte reproducibility.

### Task 3: Validate Editorial Quality

**Files:**
- Modify if a verified defect remains: `docs/publisher/tools/revise_ru_manuscript.py`
- Regenerate if required: `docs/publisher/ru-manuscript-editorial-2026-07-13.md`

- [x] Recompute chapter length, list share, repeated phrase, duplicate paragraph, long sentence, and avoidable-anglicism metrics.
- [x] Inspect chapters 5, 11, 15, 24, 26, 27, and 28 as continuous reading sequences.
- [x] Confirm that no Online Companion implementation catalogue was copied into the print manuscript.
- [x] Run focused manuscript, documentation-surface, and practice tests.

### Task 4: Record Online/Print Update Governance

**Files:**
- Create: `docs/publisher/ru-technical-book-polish-pass-2026-08-17.md`
- Modify: `docs/publisher/ru-google-doc-workflow.md`
- Modify: `docs/publisher/ru-manuscript-evolution.md`

- [x] Record the synchronized baseline commit `9c05a1d37d91b07ca38836d254945f8f720887b5`.
- [x] Define the three-way classification for future changes: stable invariant, dated technology snapshot, or Online Companion-only executable detail.
- [x] Record acceptance evidence, artifact inventory, page counts, Google revision, and author-owned fields.

### Task 5: Rebuild Publisher Artifacts

**Files:**
- Regenerate: `docs/publisher/ru-index-terms-2026-07-27.md`
- Regenerate: `docs/publisher/ru-learning-outcome-map-2026-07-27.md`
- Regenerate: `docs/publisher/ru-human-review-packet-2026-07-27.md`
- Create: `docs/publisher/artifacts/agent-arch-ru-google-doc-technical-book-polish-2026-08-17.docx`
- Create: `docs/publisher/artifacts/agent-arch-ru-google-doc-technical-book-polish-2026-08-17.pdf`
- Create: `docs/publisher/artifacts/agent-arch-ru-template2000n-technical-book-polish-2026-08-17.docx`
- Create: `docs/publisher/artifacts/agent-arch-ru-template2000n-technical-book-polish-2026-08-17.pdf`

- [x] Rebuild editorial packets from the canonical manuscript.
- [x] Build the Google-oriented DOCX and the Template2000n derivative.
- [x] Prove paragraph-text and media equality between the two DOCX files.
- [x] Render both variants and run accessibility, font, geometry, blank-page, overflow, link, bookmark, table, and image checks.
- [x] Inspect contact sheets plus every page affected by the editorial delta.

### Task 6: Synchronize The Existing Google Doc

**Target:** `1LyY2Psy2yaobn7VLmOwLTWm4QVrhp2I-ylE2B7V4pp4`, tab `t.0`

- [x] Perform the required trusted full read and confirm revision, tab topology, controls, tables, and inline objects.
- [x] Generate a paragraph-level synchronization plan against the rebuilt Google-oriented DOCX.
- [x] Apply guarded native updates in descending index order with `requiredRevisionId`.
- [x] Re-read every changed anchor and confirm all target paragraphs, tables, links, figures, and alternative descriptions remain present.
- [x] Export the Google Doc and verify semantic equality with the canonical manuscript.

### Task 7: Complete Verification And Handoff

**Files:**
- Finalize: `docs/publisher/ru-technical-book-polish-pass-2026-08-17.md`

- [x] Run the complete pytest suite, Ruff, strict MkDocs builds for Russian, English, and Chinese, and `git diff --check`.
- [x] Compare the final diff with this plan and confirm that every requirement has evidence.
- [x] Commit only the files belonging to this pass and preserve the isolated worktree for review.
