# RU Manuscript World-Class Revision Implementation Plan

> **For agentic workers:** execute the checklist in order and verify the repository source, the live Google Doc, and the publisher export after every structural batch.

**Goal:** turn the full Russian manuscript into a coherent, reproducible, visually supported engineering book whose claims are backed by the companion repository.

**Architecture:** `docs/book/**`, `docs/appendix/**`, and the publisher assembly remain the durable source. The existing Google Doc is the publisher-facing manuscript and receives guarded, revision-controlled updates. Structural edits land before prose, practice, visuals, and final proofing so chapter references are changed only once.

**Toolchain:** Markdown, MkDocs, `agent_runtime_ref`, pytest, Google Docs batchUpdate, DOCX/PDF export, Template2000n style derivative, render QA.

---

## 1. Structural recomposition

- [x] Split the current megachapter 20 into chapters 20-24.
- [x] Renumber the current implementation and launch chapters as 25-27.
- [x] Rebuild the reader map and all internal chapter references.
- [x] Reorder chapter 2 to follow its decision question.
- [x] Expand the conclusion and return to the opening incident.

## 2. Editorial cleanup

- [x] Remove web-navigation and assembly labels from reader-facing prose.
- [x] Reduce every chapter to one conclusion and one forward bridge.
- [x] Remove empty and repeated headings.
- [x] Normalize reader address to polite plural Russian.
- [x] Apply the terminology policy without damaging identifiers.

## 3. Practical learning path

- [x] Turn seven one-paragraph exercises into reproducible labs.
- [x] Add one cumulative capstone based on the support-ticket scenario.
- [x] Label snippets as runnable code, configuration, pseudocode, or output.
- [x] Add repository checks for every claimed executable command.
- [x] Expand the policy and capability implementation chapter.

## 4. Narrative and visual system

- [x] Carry support triage, knowledge assistant, and incident coordination through the relevant parts.
- [x] Insert all existing publisher diagrams at their canonical anchors.
- [x] Add missing diagrams for decision, lifecycle, incident, and capstone flows.
- [x] Add compact decision and evidence tables where prose currently simulates a matrix.
- [x] Renumber every figure and repair every cross-reference.

## 5. Verification and delivery

- [x] Run duplicate, residue, heading, terminology, figure, and link scans.
- [x] Run the complete Python test suite and strict MkDocs build.
- [x] Read back the final Google Docs revision and verify structure and counts.
- [x] Export DOCX/PDF, apply Template2000n styles, render, and inspect changed pages.
- [x] Commit and push the source, artifacts, and final report.

## Definition of done

- No chapter exceeds 8,000 words and no chapter is visibly underdeveloped.
- No reader-visible assembly labels, stale numbering, or empty headings remain.
- The manuscript uses one reader address and one terminology policy.
- Seven labs plus one capstone have commands, expected artifacts, and acceptance criteria.
- Every runnable command is verified against the recorded repository revision.
- The visual system contains at least 25 meaningful figures/tables with valid numbering.
- Repository sources, Google Doc, and publisher export describe the same book structure.

## Completion evidence

- Live Google Doc: 27 sequential chapters, 25 sequential figures, two native
  tables, seven labs, one capstone, and five appendices.
- Control export: approximately 99,000 words and 450 PDF pages.
- Repository verification: 948 pytest tests, strict MkDocs build, scoped Ruff,
  scoped ty, and executable lab commands passed on 2026-07-11.
- Visual verification: all 450 pages of the raw Google PDF were reviewed; no
  clipping, overlaps, or missing figures were found. The Template2000n
  derivative passed text-sequence and OOXML integrity checks. Its independent
  render is deferred because LibreOffice is unavailable and the Pages export
  did not complete.
