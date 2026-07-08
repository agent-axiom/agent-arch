# RU Case-Driven Reader Pass Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the Russian manuscript more interesting and recommendable by strengthening the story arc, reader actions, quotable language, and final adoption path.

**Architecture:** Keep the manuscript technically serious and avoid another repeated chapter rubric. Add a small number of high-leverage reader-facing blocks in the Markdown source, mirror the important blocks into the live Google Doc, record 100 controlled editorial iterations, verify docs/tests, then commit and push.

**Tech Stack:** Markdown manuscript, Google Docs connector batchUpdate/readback, MkDocs, pytest, git.

---

### Task 1: Add Story And Application Blocks

**Files:**
- Modify: `docs/publisher/ru-manuscript-full.md`
- Create: `docs/publisher/ru-editorial-100-case-driven-reader-iterations-2026-07-08.md`
- Create: `docs/publisher/ru-case-driven-reader-pass-2026-07-08.md`

- [x] **Step 1: Add the cross-case mini-series**

Add a compact block after the first cross-case episode that turns the support-triage case into a seven-part story.

- [x] **Step 2: Add two key chapter scenes**

Add short reader-facing scenes to Chapter 12 and Chapter 16, where the story benefits most from concrete tension: duplicate side effects and release evidence.

- [x] **Step 3: Add the final adoption path**

Before appendices, add a section with the seven-day, thirty-day, and architecture-review paths.

- [x] **Step 4: Add quotable lines**

Inside the same final section, add a compact set of reusable phrases readers can bring to team conversations.

- [x] **Step 5: Record the 100 editorial iterations**

Create a dated report with 100 controlled iteration goals and decisions. Count no-churn passes as valid editorial iterations only when they explicitly protect the manuscript from repetition.

### Task 2: Sync To Google Doc

**Files:**
- Live Google Doc: `https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI/edit`

- [x] **Step 1: Confirm target document identity**

Use connector readback to confirm document id, title, revision id and tab id.

- [x] **Step 2: Insert key reader-facing blocks**

Use `batchUpdate` with current revision control to insert the cross-case mini-series and final application section in the same logical locations as the Markdown source.

- [x] **Step 3: Verify readback**

Read back the inserted headings and representative paragraphs from the exact Google Doc.

### Task 3: Verify, Commit, Push

**Files:**
- Verify all modified Markdown and docs surface.

- [x] **Step 1: Run checks**

Run:

```bash
git diff --check
uv run pytest tests/test_docs_surface.py tests/test_agent_runtime_ref.py
uv run --group docs mkdocs build --strict
```

- [x] **Step 2: Commit**

Stage only intentional files and commit:

```bash
git add docs/publisher/ru-manuscript-full.md docs/publisher/ru-editorial-100-case-driven-reader-iterations-2026-07-08.md docs/publisher/ru-case-driven-reader-pass-2026-07-08.md docs/superpowers/plans/2026-07-08-ru-case-driven-reader-pass.md
git commit -m "docs: add case-driven reader pass"
```

- [x] **Step 3: Push**

Push the current branch and report the result.
