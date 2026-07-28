# RU Shareable Manuscript Pass Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the Russian manuscript more memorable, practical, and easy to recommend by adding a case dossier, stronger part openings, wrong/right contrasts, repository practice routes, and reusable team artifacts.

**Architecture:** Keep `docs/publisher/ru-manuscript-full.md` as the source of truth and mirror only the high-signal reader-facing additions into the live Google Doc. Add a dated editorial iteration report and a dated implementation report so the publisher-facing history remains auditable.

**Tech Stack:** Markdown manuscript, Google Docs connector batchUpdate/readback, MkDocs, pytest, git.

---

### Task 1: Add The Case Dossier

**Files:**
- Modify: `docs/publisher/ru-manuscript-full.md`

- [x] **Step 1: Insert a compact dossier after the cross-case section**

Add `### Досье сквозного кейса` after `### Сквозной производственный кейс`.

- [x] **Step 2: Keep the dossier role-based and reusable**

Cover product goal, actors, capabilities, risk, proof, and reader question in short paragraphs.

### Task 2: Add Cold Opens For Parts

**Files:**
- Modify: `docs/publisher/ru-manuscript-full.md`

- [x] **Step 1: Add a scene opener to Part I**

Place `**Сцена, с которой начинается часть**` after the Part I heading and before `Три оптики этой части`.

- [x] **Step 2: Add scene openers to Parts II-VII**

Repeat the same marker for Parts II-VII, each with a different production tension.

### Task 3: Add Wrong/Right Contrasts

**Files:**
- Modify: `docs/publisher/ru-manuscript-full.md`

- [x] **Step 1: Add a final wrong/right section**

Add `**Неправильно / промышленно**` inside `### Как применить книгу после чтения`.

- [x] **Step 2: Cover key decisions**

Cover agent choice, memory, tool calls, confirmation, traces, evals, launch, and ownership.

### Task 4: Add Repository Practice Route

**Files:**
- Modify: `docs/publisher/ru-manuscript-full.md`

- [x] **Step 1: Add a repository route near the introductory practice section**

Add a route that names the concrete companion files under `docs/companion`.

- [x] **Step 2: Add a final practice route near the adoption path**

Add a short "open, change, run, discuss" route that ties the manuscript to tests and companion artifacts.

### Task 5: Add Team-Shareable Artifacts And Reports

**Files:**
- Modify: `docs/publisher/ru-manuscript-full.md`
- Create: `docs/publisher/ru-editorial-100-shareable-manuscript-iterations-2026-07-09.md`
- Create: `docs/publisher/ru-shareable-manuscript-pass-2026-07-09.md`

- [x] **Step 1: Add the team artifacts section**

Add `**Пять артефактов, которые удобно переслать команде**` inside the final adoption section.

- [x] **Step 2: Record 100 editorial iterations**

Create a dated report with 100 iteration goals and decisions.

- [x] **Step 3: Record implementation status and author-owned fields**

Create a dated pass report with Google Doc status, verification commands, commit/push status, and fields the author must fill manually.

### Task 6: Sync, Verify, Commit, Push

**Files:**
- Live Google Doc: `https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI/edit`

- [x] **Step 1: Sync key additions to Google Doc**

Use current-revision controlled `batchUpdate` requests and verify markers with connector readback.

- [x] **Step 2: Run local checks**

Run:

```bash
git diff --check
uv run pytest tests/test_docs_surface.py tests/test_agent_runtime_ref.py
uv run --group docs mkdocs build --strict
```

- [x] **Step 3: Commit and push**

Stage only intentional files, commit with `docs: add shareable manuscript pass`, and push the current branch.
