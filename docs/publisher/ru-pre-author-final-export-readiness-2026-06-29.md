# Pre-author final export readiness

Date: 2026-06-29.

Status: ready for pre-author review, not ready for final publisher export.

## Current state

- Full Google Doc manuscript is the authoritative working manuscript:
  <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>
- Latest Google Doc revision after 2026-07-01 pre-author finalization sync:
  `ALtnJHwQSbMVcXf5UUw3QyuuxPZVGdtR-7yOKUdJM8DtE76ktgR6WhHDA0zngCtIQFMNxPaYHMglaPHowPxYQS8TpcL8wryth-RYjYpT_iQ`
- Latest proof pair remains the 2026-06-28 pair:
  raw Google Docs export at 499 rendered pages and Template2000n derivative at
  315 rendered pages, both with 0 blank-like pages.

## Why final export is deferred

The final export would be misleading while author-owned fields remain open.
Running it now would create another proof candidate, but not a final publisher
artifact.

## Final export trigger

Run the final export only after:

1. author bio, role, links, companion metadata and disclosure/legal text are
   filled or explicitly omitted;
2. OpenReview remains demoted out of primary evidence unless metadata is
   verified and the records are deliberately promoted again;
3. Google Doc access is checked for the target editor/publisher account.

## 2026-07-01 gate update

The pre-author finalization pass is recorded in
`docs/publisher/ru-pre-author-finalization-pass-2026-07-01.md`. The export
decision remains unchanged: final raw DOCX, Template2000n final derivative and
final render QA are deferred until author-owned fields are closed.

## Next export steps after author input

1. Export raw Google Docs DOCX.
2. Apply Template2000n flow or publisher-approved styles.
3. Render both DOCX files to page images.
4. Record page counts and blank-like page checks.
5. Inspect title/front matter, dense technical pages, appendices and back
   matter manually.
6. Update clean handoff packet, cover note and submission checklist.
