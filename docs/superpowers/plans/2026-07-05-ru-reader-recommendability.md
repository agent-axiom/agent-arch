# RU Reader Recommendability Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Improve the Russian manuscript so it reads less like a static technical manual and more like a memorable, recommendable engineering book.

**Architecture:** Keep Google Doc as the live manuscript workspace, keep `docs/publisher/ru-manuscript-full.md` as the local source record, and keep DOCX proofs as reproducible artifacts. Apply a bounded narrative/readability pass rather than an uncontrolled rewrite: add story spine, production failure scenes, part-level continuity, chapter takeaways, and a 100-iteration editorial ledger.

**Tech Stack:** Markdown source, `python-docx`, Google Drive connector, Template2000n derivative builder, `render_docx.py`, `render_qa_metrics.py`, git.

---

### Task 1: Planning and Scope Control

**Files:**
- Create: `docs/superpowers/plans/2026-07-05-ru-reader-recommendability.md`
- Modify: `docs/publisher/ru-manuscript-evolution.md`
- Create: `docs/publisher/ru-reader-recommendability-pass-2026-07-05.md`
- Create: `docs/publisher/ru-editorial-100-reader-recommendability-iterations-2026-07-05.md`

- [ ] **Step 1: Confirm current manuscript state**

Run:

```bash
git status --short
rg -n "^## Глава|^# Часть|^## Введение" docs/publisher/ru-manuscript-full.md
```

Expected: only known unrelated untracked files before edits; chapters 1-23 present.

- [ ] **Step 2: Fix scope**

Implement exactly five content passes:

1. sharpen the book opening and promise;
2. strengthen chapters 1-6 with recognizable production failures;
3. strengthen chapters 7-16 with the memory/tools/traces/eval/release arc;
4. strengthen chapters 17-23 with the final platform maturity arc;
5. add chapter-level takeaways and reader action prompts.

- [ ] **Step 3: Record 100 editorial micro-iterations**

Create a ledger with 100 completed iterations grouped by the five passes. Each row must include goal, implementation result, and verification signal.

### Task 2: Opening Hook and Story Spine

**Files:**
- Modify: `docs/publisher/ru-manuscript-full.md`
- Modify: `docs/publisher/artifacts/agent-arch-ru-google-doc-dedup-source-sync-2026-07-05.docx`

- [ ] **Step 1: Add a stronger reader promise**

Insert a short section after the introduction promise that names the core transformation: from demo agent to accountable production system.

- [ ] **Step 2: Add a reusable story spine**

Add a compact "сквозная история" block that follows one support agent through safety boundary, memory, tools, observability, evals, rollout, incident response, registry, and decommissioning.

- [ ] **Step 3: Add part-level continuity notes**

After each `# Часть` heading, add a 2-4 sentence "Где мы в истории" note that tells the reader what changed in the system and why the next part matters.

### Task 3: Chapters 1-6 Production Failure Scenes

**Files:**
- Modify: `docs/publisher/ru-manuscript-full.md`
- Modify: `docs/publisher/artifacts/agent-arch-ru-google-doc-dedup-source-sync-2026-07-05.docx`

- [ ] **Step 1: Add one compact failure scene to each chapter 1-6**

Each scene must show a plausible production failure, the false confidence that allowed it, and the architectural control that prevents recurrence.

- [ ] **Step 2: Keep scenes short**

Each scene should be 120-180 words in Markdown and should not introduce new external claims.

### Task 4: Chapters 7-23 Narrative Continuity

**Files:**
- Modify: `docs/publisher/ru-manuscript-full.md`
- Modify: `docs/publisher/artifacts/agent-arch-ru-google-doc-dedup-source-sync-2026-07-05.docx`

- [ ] **Step 1: Add arc bridges to chapters 7-16**

Each bridge must show how the previous technical layer becomes the next operational risk or proof obligation.

- [ ] **Step 2: Add maturity bridges to chapters 17-23**

Each bridge must show how organizational model, ADLC, assurance loop, runtime, policy catalog, and launch checklist combine into one platform.

### Task 5: Chapter Takeaways, Proofs, QA, Google Doc Update, Commit

**Files:**
- Modify: `docs/publisher/ru-manuscript-full.md`
- Modify: `docs/publisher/artifacts/agent-arch-ru-google-doc-dedup-source-sync-2026-07-05.docx`
- Modify: `docs/publisher/artifacts/agent-arch-ru-template2000n-dedup-source-sync-2026-07-05.docx`
- Modify: render QA JSON and metrics files for the current proof pair.
- Modify: `docs/publisher/ru-google-doc-workflow.md`
- Modify: `docs/publisher/ru-manuscript-evolution.md`

- [ ] **Step 1: Add a compact reader takeaway block to every chapter**

Each chapter must get:

- `Главная мысль главы`
- `Что проверить у себя`
- `Что рассказать команде`

- [ ] **Step 2: Update raw DOCX and Google Doc**

Patch the current raw DOCX with the same new content and replace the Drive file content while preserving the existing Google Doc id.

- [ ] **Step 3: Rebuild Template2000n derivative**

Run:

```bash
python docs/publisher/tools/build_template2000n_derivative.py \
  --raw-docx docs/publisher/artifacts/agent-arch-ru-google-doc-dedup-source-sync-2026-07-05.docx \
  --template-docx /tmp/Template2000n.docx \
  --output-docx docs/publisher/artifacts/agent-arch-ru-template2000n-dedup-source-sync-2026-07-05.docx \
  --metrics-json docs/publisher/ru-template2000n-dedup-source-sync-2026-07-05.metrics.json
```

Expected: `text_equality: true`.

- [ ] **Step 4: Render both DOCX files**

Run `render_docx.py` for raw and Template2000n DOCX. Generate render QA JSON with `docs/publisher/tools/render_qa_metrics.py`.

Expected: no blank-like pages and no obvious first/last-page visual defects.

- [ ] **Step 5: Verification**

Run:

```bash
git diff --check
python - <<'PY'
from pathlib import Path
import re
text = Path('docs/publisher/ru-manuscript-full.md').read_text()
chapters = [int(m.group(1)) for m in re.finditer(r'^## Глава (\d+)\.', text, re.M)]
print(chapters == list(range(1, 24)))
print(len(re.findall(r'\b[А-Яа-яЁё]+s\b', text)))
PY
```

Expected: `True` and `0`.

- [ ] **Step 6: Commit and push**

Commit all task files and push the current branch.
