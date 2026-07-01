# Pre-author export gate

Date: 2026-07-01.

Status: final export gate is prepared; final export is intentionally deferred.

## Decision

Do not create a new final publisher DOCX until author-owned fields are closed.
A fresh export before that point would be a new working proof, not a final
publisher artifact, and would need to be regenerated after author metadata is
filled.

## Current accepted proof baseline

- Raw Google Docs export:
  `docs/publisher/artifacts/agent-arch-ru-editorial-ready-2026-06-28.docx`
  - 499 rendered pages
  - 0 blank-like pages
- Template2000n derivative:
  `docs/publisher/artifacts/agent-arch-ru-template2000n-editorial-ready-2026-06-28.docx`
  - 315 rendered pages
  - 0 blank-like pages

## Trigger to run the final export workflow

Run the final export workflow when all of the following are true:

1. The author input closure packet is filled or explicitly marks omissions.
2. Google Doc author/front-matter fields are synchronized.
3. Companion URL/version/changelog/errata are final.
4. Fast-moving platform/API/security source claims have a fresh semantic pass.
5. The selected final Google Doc revision is recorded.

## Workflow after trigger

1. Export raw Google Docs DOCX from the final Google Doc state.
2. Apply Template2000n or the publisher-approved style flow.
3. Render both DOCX files.
4. Count pages and blank-like pages.
5. Spot-check title/front matter, dense tables, code blocks, source appendix
   and glossary.
6. Update the clean handoff packet, final external packet outline and
   submission checklist with final proof paths and page counts.
