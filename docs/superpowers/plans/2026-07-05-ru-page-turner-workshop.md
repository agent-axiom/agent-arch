# RU Page-Turner Workshop Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the Russian manuscript more interesting and recommendable by adding a stronger through-line, part-level team workshops, and chapter-level next actions.

**Architecture:** Keep the existing Google Doc as the live manuscript, `docs/publisher/ru-manuscript-full.md` as the source record, and the current raw/Template2000n DOCX pair as reproducible proof artifacts. Apply a bounded editorial pass: add the story arc in the introduction, add seven part workshops, and add one practical next action after each chapter takeaway.

**Tech Stack:** Markdown source, `python-docx`, Google Drive connector, Template2000n derivative builder, `render_docx.py`, `render_qa_metrics.py`, git.

---

### Task 1: Through-Line And Reading Tension

**Files:**
- Modify: `docs/publisher/ru-manuscript-full.md`
- Modify: `docs/publisher/artifacts/agent-arch-ru-google-doc-dedup-source-sync-2026-07-05.docx`

- [x] **Step 1: Add a through-line section to the introduction**

Add a compact "Сквозная дуга книги" section that frames the book as one story:
demo agent, unsafe action, memory/context risk, tool execution, trace/eval,
organizational ownership, runtime and launch gate.

- [x] **Step 2: Keep the section short**

The section must give reading momentum without repeating all chapter summaries.

### Task 2: Part-Level Team Workshops

**Files:**
- Modify: `docs/publisher/ru-manuscript-full.md`
- Modify: `docs/publisher/artifacts/agent-arch-ru-google-doc-dedup-source-sync-2026-07-05.docx`

- [x] **Step 1: Add seven workshop blocks**

After each main `# Часть ...` heading profile block, add a "Командная сессия"
block with duration, discussion focus, artifact, success signal and red flag.

- [x] **Step 2: Keep workshops operational**

Each block must tell a team what to do after reading the part, not just restate
the part's topic.

### Task 3: Chapter-Level Next Actions, 100 Iterations, QA, Google Doc, Push

**Files:**
- Modify: `docs/publisher/ru-manuscript-full.md`
- Modify: `docs/publisher/artifacts/agent-arch-ru-google-doc-dedup-source-sync-2026-07-05.docx`
- Modify: `docs/publisher/artifacts/agent-arch-ru-template2000n-dedup-source-sync-2026-07-05.docx`
- Create: `docs/publisher/ru-page-turner-workshop-pass-2026-07-05.md`
- Create: `docs/publisher/ru-editorial-100-page-turner-workshop-iterations-2026-07-05.md`
- Modify: `docs/publisher/ru-manuscript-evolution.md`
- Modify: `docs/publisher/ru-google-doc-workflow.md`
- Modify: `docs/publisher/ru-google-doc-dedup-source-sync-pass-2026-07-05.md`
- Modify: `docs/publisher/ru-editor-handoff-packet-dedup-integrity-2026-07-05.md`
- Modify: current render QA JSON and Template2000n metrics files.

- [x] **Step 1: Add one next-action line to every chapter takeaway**

Each chapter's existing `Что унести из главы` block must get a compact
`Что сделать после чтения` line.

- [x] **Step 2: Record 100 editorial iterations**

Create a ledger with 100 controlled iterations grouped by story arc, workshops,
chapter actions and proofing.

- [x] **Step 3: Rebuild and verify proof artifacts**

Rebuild Template2000n, upload raw DOCX to the existing Google Doc, verify
readback, render both proof files, update QA JSON, run structural checks,
`git diff --check`, `mkdocs build --strict`, commit and push.
