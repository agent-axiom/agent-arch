# RU Reader Delight Polish Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the Russian manuscript more enjoyable, memorable and recommendable without adding another visible recurring rubric or inflating the book mechanically.

**Architecture:** Keep `docs/publisher/ru-manuscript-full.md` as the repository source record, update the current raw Google Docs DOCX and regenerate the Template2000n proof. Add short natural prose only at high-leverage locations: the introduction, selected part openings and selected chapter pivots. Verify that existing 1/7/23 editorial layers remain stable and that the new prose does not duplicate existing blocks.

**Tech Stack:** Markdown source, `python-docx`, Google Drive connector, Template2000n derivative builder, `render_docx.py`, `render_qa_metrics.py`, git.

---

### Task 1: Audit Reader Fatigue And High-Leverage Polish Points

**Files:**
- Read: `docs/publisher/ru-manuscript-full.md`
- Create: `docs/publisher/ru-reader-delight-audit-2026-07-06.md`

- [x] **Step 1: Inspect current recurring layers and opening rhythm**

Confirm where the manuscript already has reader routes, scenes, case episodes,
chapter theses, skeptic responses, mindset shifts, action blocks and narrative
bridges. Identify places where a small natural paragraph can improve delight
without creating another repeated box.

### Task 2: Add Aha Moments Without A New Rubric

**Files:**
- Modify: `docs/publisher/ru-manuscript-full.md`
- Modify: `docs/publisher/artifacts/agent-arch-ru-google-doc-dedup-source-sync-2026-07-05.docx`

- [x] **Step 1: Add targeted natural prose**

Add a small set of memorable prose paragraphs in high-leverage positions:
the introduction, part openings and selected chapter pivots. Do not add a new
heading, repeated label or visible recurring block.

### Task 3: Sharpen Conflicts And Retellability

**Files:**
- Modify: `docs/publisher/ru-manuscript-full.md`
- Modify: `docs/publisher/artifacts/agent-arch-ru-google-doc-dedup-source-sync-2026-07-05.docx`

- [x] **Step 1: Strengthen the book's central conflicts**

Make the main conflicts easier to remember and retell: demo vs product,
autonomy vs responsibility, speed vs control, convenience vs audit, and
launch vs accountability.

### Task 4: Check Duplicates, Rhythm And Terminology

**Files:**
- Read: `docs/publisher/ru-manuscript-full.md`
- Read: `docs/publisher/artifacts/agent-arch-ru-google-doc-dedup-source-sync-2026-07-05.docx`

- [x] **Step 1: Run structural and editorial checks**

Verify that no existing 1/7/23 recurring label counts regress, no exact
duplicate paragraph groups with 35+ words appear, no raw DOCX paragraphs over
250 words appear, visible Cyrillic+Latin suffix forms stay absent, and the new
paragraphs do not closely restate existing rubrics.

### Task 5: Rebuild, Sync, Verify, Report And Push

**Files:**
- Modify: `docs/publisher/artifacts/agent-arch-ru-template2000n-dedup-source-sync-2026-07-05.docx`
- Modify: current render QA and Template2000n metrics JSON files
- Create: `docs/publisher/ru-reader-delight-polish-pass-2026-07-06.md`
- Create: `docs/publisher/ru-editorial-100-reader-delight-polish-iterations-2026-07-06.md`
- Modify: `docs/publisher/ru-google-doc-dedup-source-sync-pass-2026-07-05.md`
- Modify: `docs/publisher/ru-google-doc-workflow.md`
- Modify: `docs/publisher/ru-manuscript-evolution.md`
- Modify: `docs/publisher/ru-editor-handoff-packet-dedup-integrity-2026-07-05.md`

- [x] **Step 1: Rebuild and sync**

Rebuild Template2000n, upload the updated raw DOCX to the existing Google Doc,
and verify connector readback for representative new prose.

- [x] **Step 2: Render and QA**

Render raw and Template2000n DOCX, run render QA, inspect contact sheets, and
run structural checks.

- [x] **Step 3: Record 100 editorial iterations**

Create a 100-item controlled editorial ledger for this pass, including reader
fatigue, aha moments, conflict sharpness, retellability, author-owned fields
and publisher handoff checks.

- [x] **Step 4: Final verification, commit and push**

Run `git diff --check`, `uv run --group docs mkdocs build --strict`, stage only
the files for this pass, commit and push the current branch.
