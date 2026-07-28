# RU Case Thesis Pass Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a recurring production support-agent case and quotable chapter theses to make the Russian manuscript more memorable and easier to recommend.

**Architecture:** Keep the current Google Doc as the live manuscript and `docs/publisher/ru-manuscript-full.md` as the source record. Patch the current raw DOCX with the same semantic additions, rebuild the Template2000n derivative, upload the raw DOCX back to the existing Google Doc, then verify text, structure and render quality.

**Tech Stack:** Markdown source, `python-docx`, Google Drive connector, Template2000n derivative builder, `render_docx.py`, `render_qa_metrics.py`, git.

---

### Task 1: Source And DOCX Editorial Insertions

**Files:**
- Modify: `docs/publisher/ru-manuscript-full.md`
- Modify: `docs/publisher/artifacts/agent-arch-ru-google-doc-dedup-source-sync-2026-07-05.docx`

- [x] **Step 1: Add the explicit through-case**

Insert `Сквозной производственный кейс` in the introduction near the existing
support scenario and through-line blocks. The block must explain that the
support agent is the main recurring case and that every part changes one
production constraint.

- [x] **Step 2: Add seven part-level case episodes**

After each main part's workshop block, insert one `Эпизод сквозного кейса`
paragraph that shows the support-agent system evolving through that part.

- [x] **Step 3: Add 23 quotable chapter theses**

Inside each `Что унести из главы` block, add exactly one `Фраза для пересказа`
line before `Почему главу стоит переслать`.

### Task 2: Proof Rebuild And Google Doc Sync

**Files:**
- Modify: `docs/publisher/artifacts/agent-arch-ru-template2000n-dedup-source-sync-2026-07-05.docx`
- Modify: `docs/publisher/ru-template2000n-dedup-source-sync-2026-07-05.metrics.json`
- Modify: current render QA JSON files.

- [x] **Step 1: Rebuild Template2000n**

Run `docs/publisher/tools/build_template2000n_derivative.py` with the current
raw DOCX and `/tmp/Template2000n.docx`. Expected: `text_equality: true`.

- [x] **Step 2: Upload the raw DOCX to the existing Google Doc**

Use Drive `files.update` through the Google Drive connector for document ID
`1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI`.

- [x] **Step 3: Verify Google Doc readback**

Read back exact phrases:

- `Сквозной производственный кейс`
- `Эпизод сквозного кейса`
- `Фраза для пересказа`

### Task 3: QA, Reports, Commit And Push

**Files:**
- Create: `docs/publisher/ru-case-thesis-pass-2026-07-05.md`
- Create: `docs/publisher/ru-editorial-100-case-thesis-iterations-2026-07-05.md`
- Modify: `docs/publisher/ru-manuscript-evolution.md`
- Modify: `docs/publisher/ru-google-doc-workflow.md`
- Modify: `docs/publisher/ru-google-doc-dedup-source-sync-pass-2026-07-05.md`
- Modify: `docs/publisher/ru-editor-handoff-packet-dedup-integrity-2026-07-05.md`

- [x] **Step 1: Render both DOCX files**

Render raw and Template2000n DOCX with `render_docx.py --emit_pdf`, then run
`render_qa_metrics.py` and update the current QA JSON files.

- [x] **Step 2: Run structural QA**

Verify counts: 1 through-case, 7 case episodes, 23 quotable theses, 7 parts,
23 chapters, raw/template text equality, 0 duplicate groups with 35+ words,
0 paragraphs with 250+ words, 0 blank-like pages.

- [x] **Step 3: Update reports**

Record the pass report, 100 controlled micro-iterations, current Google Doc
revision, render pages and remaining author-owned fields.

- [x] **Step 4: Final checks and git**

Run `git diff --check`, `uv run --group docs mkdocs build --strict`,
stage only relevant files, run `git diff --cached --check`, commit and push.
