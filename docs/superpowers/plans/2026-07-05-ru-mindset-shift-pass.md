# RU Mindset Shift Pass Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a reader-mindset layer that makes the Russian manuscript more compelling, easier to discuss, and more likely to be recommended after reading.

**Architecture:** Keep the existing Google Doc as the live editorial manuscript, `docs/publisher/ru-manuscript-full.md` as the repository source record, and the current raw/Template2000n DOCX pair as proof artifacts. Add one introduction block, seven part-level before/after blocks, and twenty-three chapter-level mindset-shift blocks, then verify that the new layer does not duplicate the existing takeaway, quote, skeptic-response, forwarding-hook, and action layers.

**Tech Stack:** Markdown source, `python-docx`, Google Drive connector, Template2000n derivative builder, `render_docx.py`, `render_qa_metrics.py`, git.

---

### Task 1: Add The Intro Mindset Promise

**Files:**
- Modify: `docs/publisher/ru-manuscript-full.md`
- Modify: `docs/publisher/artifacts/agent-arch-ru-google-doc-dedup-source-sync-2026-07-05.docx`

- [x] **Step 1: Insert `Как изменится ваше мышление после книги`**

Add a concise introduction section after `С кем спорит эта книга`. The section
must explain the reader transformation without promising a universal recipe.

### Task 2: Add Part-Level Before/After Blocks

**Files:**
- Modify: `docs/publisher/ru-manuscript-full.md`
- Modify: `docs/publisher/artifacts/agent-arch-ru-google-doc-dedup-source-sync-2026-07-05.docx`

- [x] **Step 1: Insert seven `До этой части / После этой части` blocks**

After each part-level `Типичное возражение` block, add one before/after block
that names the reader's expected shift in judgment.

### Task 3: Add Chapter-Level Mindset Shifts

**Files:**
- Modify: `docs/publisher/ru-manuscript-full.md`
- Modify: `docs/publisher/artifacts/agent-arch-ru-google-doc-dedup-source-sync-2026-07-05.docx`

- [x] **Step 1: Insert 23 `Смена мышления` lines**

Inside each chapter takeaway block, add exactly one concise `Смена мышления`
line after `Что ответить скептику` and before `Почему главу стоит переслать`.

### Task 4: Check Duplication And Editorial Fit

**Files:**
- Modify: `docs/publisher/ru-manuscript-full.md`
- Modify: `docs/publisher/artifacts/agent-arch-ru-google-doc-dedup-source-sync-2026-07-05.docx`

- [x] **Step 1: Run structural and duplicate checks**

Verify the new labels appear exactly once/seven/twenty-three times in Markdown,
raw DOCX and Template2000n DOCX. Check that no new exact duplicate paragraph
groups with 35+ words appear and that the mindset lines do not restate the
existing `Что унести из главы`, `Фраза для пересказа`, `Что ответить скептику`,
`Почему главу стоит переслать`, or `Что сделать после чтения` lines.

### Task 5: Rebuild, Sync, Verify, Report And Push

**Files:**
- Modify: `docs/publisher/artifacts/agent-arch-ru-template2000n-dedup-source-sync-2026-07-05.docx`
- Modify: current render QA and Template2000n metrics JSON files
- Create: `docs/publisher/ru-mindset-shift-pass-2026-07-05.md`
- Create: `docs/publisher/ru-editorial-100-mindset-shift-iterations-2026-07-05.md`
- Modify: `docs/publisher/ru-google-doc-dedup-source-sync-pass-2026-07-05.md`
- Modify: `docs/publisher/ru-google-doc-workflow.md`
- Modify: `docs/publisher/ru-manuscript-evolution.md`
- Modify: `docs/publisher/ru-editor-handoff-packet-dedup-integrity-2026-07-05.md`

- [x] **Step 1: Rebuild and sync**

Rebuild Template2000n, upload the raw DOCX to the existing Google Doc, and
verify connector readback for the new labels.

- [x] **Step 2: Render and QA**

Render raw and Template2000n DOCX, run render QA, inspect contact sheets, and
run structural checks.

- [x] **Step 3: Record 100 editorial iterations**

Create a 100-item controlled editorial ledger for this pass, including
recommendability, pacing, duplication, author-owned fields and publisher
handoff checks.

- [x] **Step 4: Final verification, commit and push**

Run `git diff --check`, `uv run --group docs mkdocs build --strict`, stage only
the files for this pass, commit and push the current branch.
