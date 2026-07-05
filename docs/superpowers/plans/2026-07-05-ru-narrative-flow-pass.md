# RU Narrative Flow Pass Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Improve the Russian manuscript's reading momentum so chapters feel less like isolated reference units and more like a continuous engineering narrative.

**Architecture:** Keep the existing Google Doc as the live editorial manuscript, `docs/publisher/ru-manuscript-full.md` as the repository source record, and the current raw/Template2000n DOCX pair as proof artifacts. Do not introduce another visible recurring rubric; instead, add short natural prose hooks after chapter headings and short closing bridge paragraphs after chapter action blocks.

**Tech Stack:** Markdown source, `python-docx`, Google Drive connector, Template2000n derivative builder, `render_docx.py`, `render_qa_metrics.py`, git.

---

### Task 1: Audit Chapter Starts And Ends

**Files:**
- Read: `docs/publisher/ru-manuscript-full.md`
- Create: `docs/publisher/ru-narrative-flow-audit-2026-07-05.md`

- [x] **Step 1: Inspect all 23 chapter openings and endings**

Record whether each chapter begins with a strong reader tension and whether it
ends with a natural bridge after the service blocks.

### Task 2: Add Chapter Opening Hooks

**Files:**
- Modify: `docs/publisher/ru-manuscript-full.md`
- Modify: `docs/publisher/artifacts/agent-arch-ru-google-doc-dedup-source-sync-2026-07-05.docx`

- [x] **Step 1: Insert 23 natural opening hooks**

After each chapter heading, insert one short prose paragraph that names the
chapter's practical tension. Do not use a repeated label such as `Вопрос главы`
or `Hook`.

### Task 3: Add Chapter Closing Bridges

**Files:**
- Modify: `docs/publisher/ru-manuscript-full.md`
- Modify: `docs/publisher/artifacts/agent-arch-ru-google-doc-dedup-source-sync-2026-07-05.docx`

- [x] **Step 1: Insert 23 natural closing bridges**

After each `Что сделать после чтения` block, insert one short prose paragraph
that carries the reader into the next chapter, part, or final launch frame.
Do not use a repeated label.

### Task 4: Check Duplication And Editorial Fit

**Files:**
- Read: `docs/publisher/ru-manuscript-full.md`
- Read: `docs/publisher/artifacts/agent-arch-ru-google-doc-dedup-source-sync-2026-07-05.docx`

- [x] **Step 1: Run structural and similarity checks**

Verify 23 opening hooks and 23 closing bridges are present in Markdown and raw
DOCX, no existing 1/7/23 recurring label counts regress, no exact duplicate
paragraph groups with 35+ words appear, and the new hooks/bridges do not
closely restate `Смена мышления`, `Фраза для пересказа`,
`Что ответить скептику`, or `Что сделать после чтения`.

### Task 5: Rebuild, Sync, Verify, Report And Push

**Files:**
- Modify: `docs/publisher/artifacts/agent-arch-ru-template2000n-dedup-source-sync-2026-07-05.docx`
- Modify: current render QA and Template2000n metrics JSON files
- Create: `docs/publisher/ru-narrative-flow-pass-2026-07-05.md`
- Create: `docs/publisher/ru-editorial-100-narrative-flow-iterations-2026-07-05.md`
- Modify: `docs/publisher/ru-google-doc-dedup-source-sync-pass-2026-07-05.md`
- Modify: `docs/publisher/ru-google-doc-workflow.md`
- Modify: `docs/publisher/ru-manuscript-evolution.md`
- Modify: `docs/publisher/ru-editor-handoff-packet-dedup-integrity-2026-07-05.md`

- [x] **Step 1: Rebuild and sync**

Rebuild Template2000n, upload the raw DOCX to the existing Google Doc, and
verify connector readback for sample new opening and closing bridge text.

- [x] **Step 2: Render and QA**

Render raw and Template2000n DOCX, run render QA, inspect contact sheets, and
run structural checks.

- [x] **Step 3: Record 100 editorial iterations**

Create a 100-item controlled editorial ledger for this pass, including pacing,
continuity, duplication, author-owned fields and publisher handoff checks.

- [x] **Step 4: Final verification, commit and push**

Run `git diff --check`, `uv run --group docs mkdocs build --strict`, stage only
the files for this pass, commit and push the current branch.
