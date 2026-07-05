# RU Skeptic Response Pass Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a constructive "answers to skeptics" layer so readers can use the Russian manuscript in real engineering and leadership discussions.

**Architecture:** Keep the current Google Doc as the live manuscript, `docs/publisher/ru-manuscript-full.md` as the local source record, and the current raw/Template2000n DOCX pair as proof artifacts. Add one introduction block, seven part-level objection blocks and twenty-three chapter-level skeptic responses, then rebuild, sync, render and verify.

**Tech Stack:** Markdown source, `python-docx`, Google Drive connector, Template2000n derivative builder, `render_docx.py`, `render_qa_metrics.py`, git.

---

### Task 1: Add The Intro Framing

**Files:**
- Modify: `docs/publisher/ru-manuscript-full.md`
- Modify: `docs/publisher/artifacts/agent-arch-ru-google-doc-dedup-source-sync-2026-07-05.docx`

- [x] **Step 1: Insert `С кем спорит эта книга`**

Add a short introduction section after the current recurring-case block. The
section must explain that the book argues against common shortcuts without
caricaturing skeptical readers.

### Task 2: Add Part-Level Objections

**Files:**
- Modify: `docs/publisher/ru-manuscript-full.md`
- Modify: `docs/publisher/artifacts/agent-arch-ru-google-doc-dedup-source-sync-2026-07-05.docx`

- [x] **Step 1: Insert seven `Типичное возражение` blocks**

After each main part's recurring-case episode, add one objection block with a
skeptical claim and a calm engineering response.

### Task 3: Add Chapter-Level Skeptic Responses And Finish

**Files:**
- Modify: `docs/publisher/ru-manuscript-full.md`
- Modify: `docs/publisher/artifacts/agent-arch-ru-google-doc-dedup-source-sync-2026-07-05.docx`
- Modify: `docs/publisher/artifacts/agent-arch-ru-template2000n-dedup-source-sync-2026-07-05.docx`
- Create: `docs/publisher/ru-skeptic-response-pass-2026-07-05.md`
- Create: `docs/publisher/ru-editorial-100-skeptic-response-iterations-2026-07-05.md`
- Modify: current QA, metrics, workflow, evolution and handoff reports.

- [x] **Step 1: Insert 23 `Что ответить скептику` lines**

Inside each chapter takeaway block, add exactly one concise response after
`Фраза для пересказа` and before `Почему главу стоит переслать`.

- [x] **Step 2: Rebuild, sync and verify**

Rebuild Template2000n, upload the raw DOCX to the existing Google Doc, verify
readback for all new labels, render both DOCX files, run structural QA,
`git diff --check`, `uv run --group docs mkdocs build --strict`, commit and
push.
