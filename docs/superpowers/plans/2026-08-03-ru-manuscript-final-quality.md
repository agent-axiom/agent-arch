# Russian Manuscript Final Quality Implementation Plan

**Goal:** Make the Russian publisher manuscript technically reproducible, pedagogically complete, editorially consistent, and safely synchronized to the existing Google Doc.

**Source of truth:** Repository sources, companion runtime, tests, and the generated editorial manuscript. The Google Doc is the publisher-facing projection and must be updated only after local verification.

## 1. Lock Regressions Before Fixing Them

- Extend `tests/test_companion_evidence_manifest.py` with a failing laboratory 8 case.
- Extend `tests/test_ru_lab_commands.py` with the documented export/replay workflow.
- Add manuscript assertions for the unsafe listing patterns and decision vocabulary.
- Run the focused tests and retain the failing evidence.

## 2. Repair Executable Practice

- Extend `docs/companion/examples/build_lab_evidence_manifest.py` through laboratory 8.
- Add a tested companion mutation utility so laboratories 2 and 6 use short commands instead of embedded shell programs.
- Add a deterministic capstone reference runner and committed artifact contract.
- Correct the replay command so it supplies the original input when the export redacts it.
- Verify every laboratory command in a clean temporary directory.

## 3. Repair Technical Listings

- Make approval-required decisions pause before tool dispatch.
- Apply risk policy before selecting MCP or sandbox transport.
- Bind approval expiry to the signed action and explain atomic nonce consumption.
- Show lease/CAS and step idempotency in durable resume pseudocode.
- Materialize external-effect evidence and emergency decision ownership in their examples.
- Synchronize affected online-book source chapters and all localizations where the same defect exists.

## 4. Strengthen Learning Architecture

- Add a compact walking-skeleton tour before the second laboratory.
- Add explicit verification status to the 28-chapter learning-outcome map, preserving the pending local chapter 11 and chapter 28 refinements.
- Add assessable transfer checkpoints and symmetrical part conclusions.
- Normalize release decisions to `hold`, `limited_wave`, and `expand`; reserve `freeze` and `rollback` for controls.

## 5. Perform Editorial and Navigation Pass

- Normalize memory, execution, policy-gateway, reference-package, and single-agent terminology.
- Consolidate duplicate reader guidance and repeated chapter prose.
- Flatten stray level-five headings and replace positional references with named references.
- Rewrite figure and table introductions to explain what the reader should inspect.
- Classify snippets, output, pseudocode, and executable listings consistently.

## 6. Verify Publisher Artifacts

- Regenerate the manuscript through `revise_ru_manuscript.py` and require byte-for-byte reproducibility.
- Run focused tests, the full test suite, linting, document audits, and clean-room laboratory smoke tests.
- Build DOCX/PDF artifacts with the publisher template and inspect page count, fonts, figures, tables, headings, links, and overflow.

## 7. Publish the Verified Revision

- Commit the executable code and manuscript revision, then pin the companion-code commit honestly in the manuscript.
- Update the existing Google Doc in bounded, structure-preserving operations and verify images/tables afterward.
- Commit the release metadata, push the branch, open and merge a pull request, deploy the online editions, and report the remaining author-owned placeholders.
