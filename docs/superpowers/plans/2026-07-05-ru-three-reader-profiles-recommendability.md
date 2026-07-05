# RU Three Reader Profiles Recommendability Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Strengthen the Russian manuscript so tech leads, engineering managers, CTOs, and practicing developers each find a clear reason to keep reading, apply the book, and recommend it.

**Architecture:** Keep `docs/publisher/ru-manuscript-full.md` as the local source record, patch the current raw DOCX proof with the same editorial additions, rebuild the Template2000n derivative, then replace the existing Google Doc content while preserving its document id. The pass is bounded to three reader-profile layers: architect, executive/manager, and developer.

**Tech Stack:** Markdown source, `python-docx`, Google Drive connector, Template2000n derivative builder, `render_docx.py`, `render_qa_metrics.py`, git.

---

### Task 1: Tech Lead / Architect Reader Layer

**Files:**
- Modify: `docs/publisher/ru-manuscript-full.md`
- Modify: `docs/publisher/artifacts/agent-arch-ru-google-doc-dedup-source-sync-2026-07-05.docx`

- [ ] **Step 1: Add the architect route to the introduction**

Insert a compact route explaining how a tech lead should use the book: as a decision framework for boundaries, capabilities, traces, evaluations, rollout, and ownership.

- [ ] **Step 2: Add part-level architect outcomes**

After each part heading, add one line that tells the architect what decision the part helps make.

- [ ] **Step 3: Add recommendation hooks to chapter takeaways**

Extend every chapter takeaway with a short "why this chapter is worth forwarding" line.

### Task 2: Engineering Manager / CTO Reader Layer

**Files:**
- Modify: `docs/publisher/ru-manuscript-full.md`
- Modify: `docs/publisher/artifacts/agent-arch-ru-google-doc-dedup-source-sync-2026-07-05.docx`

- [ ] **Step 1: Add the executive route to the introduction**

Insert a compact route explaining how EM/CTO readers should use the book: as a risk, ownership, rollout, and operating-model map.

- [ ] **Step 2: Add part-level management outcomes**

After each part heading, add one line that tells the manager what organizational decision or risk conversation the part enables.

- [ ] **Step 3: Add a management handoff block**

Add a concise "how to discuss this with leadership" block near the end of the introduction.

### Task 3: Practicing Developer Reader Layer, 100 Iterations, QA, Google Doc, Push

**Files:**
- Modify: `docs/publisher/ru-manuscript-full.md`
- Modify: `docs/publisher/artifacts/agent-arch-ru-google-doc-dedup-source-sync-2026-07-05.docx`
- Modify: `docs/publisher/artifacts/agent-arch-ru-template2000n-dedup-source-sync-2026-07-05.docx`
- Create: `docs/publisher/ru-three-reader-profiles-recommendability-pass-2026-07-05.md`
- Create: `docs/publisher/ru-editorial-100-three-reader-profiles-iterations-2026-07-05.md`
- Modify: `docs/publisher/ru-manuscript-evolution.md`
- Modify: `docs/publisher/ru-google-doc-workflow.md`
- Modify: `docs/publisher/ru-google-doc-dedup-source-sync-pass-2026-07-05.md`
- Modify: `docs/publisher/ru-editor-handoff-packet-dedup-integrity-2026-07-05.md`
- Modify: current render QA JSON and Template2000n metrics files.

- [ ] **Step 1: Add the developer route to the introduction**

Insert a compact route explaining how a developer should use the book: as a sequence of runnable checks, contracts, and operational habits.

- [ ] **Step 2: Add part-level developer outcomes**

After each part heading, add one line that tells the developer what concrete artifact or check the part helps produce.

- [ ] **Step 3: Record 100 editorial micro-iterations**

Create a ledger with 100 iterations grouped by the three reader profiles and final proofing.

- [ ] **Step 4: Rebuild proof artifacts**

Rebuild the Template2000n derivative from the patched raw DOCX and update the current metrics JSON.

- [ ] **Step 5: Sync Google Doc and verify readback**

Replace the existing Google Doc file content with the updated raw DOCX while preserving the document id. Verify readback for one architect, one management, and one developer phrase.

- [ ] **Step 6: Render QA**

Render raw and Template2000n DOCX proofs, generate render QA JSON, and inspect first/last page contact sheets.

- [ ] **Step 7: Commit and push**

Run `git diff --check`, `mkdocs build --strict`, stage only this pass, commit, and push the current branch.
