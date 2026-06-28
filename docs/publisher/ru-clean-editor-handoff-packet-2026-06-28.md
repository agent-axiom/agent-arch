# Clean editor handoff packet: русская рукопись

Date: 2026-06-28.

Status: clean editorial handoff for the current full manuscript. This is the
best current working package for an editor, but not the final publisher
submission until author-owned facts and external proofread are closed.

## Main manuscript

- Google Doc:
  <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>
- Title: `Архитектура безопасных ИИ-агентов - полная рукопись`
- Current revision after author/front-matter pass:
  `ALtnJHxghK0ux39XZSQMkGfFh_TqFc9QasJFxuerN_vYLBxxWKS036rEaQmQRW9mCVrBIR2uNFtXgg1EbDTdIopzLmiVbROaOd-e0Vj1GTQ`

## Current proof artifacts

Raw Google Docs export:

- `docs/publisher/artifacts/agent-arch-ru-editorial-ready-2026-06-28.docx`
- Render QA: 499 pages, 0 blank-like pages.

Template2000n proof candidate:

- `docs/publisher/artifacts/agent-arch-ru-template2000n-editorial-ready-2026-06-28.docx`
- Render QA: 315 pages, 0 blank-like pages.

Machine-readable render report:

- `docs/publisher/ru-publisher-style-pass-2026-06-28.render-qa.json`

Human-readable proof reports:

- `docs/publisher/ru-author-frontmatter-pass-2026-06-28.md`
- `docs/publisher/ru-final-editorial-proof-pass-2026-06-28.md`
- `docs/publisher/ru-publisher-style-pass-2026-06-28.md`
- `docs/publisher/ru-author-query-packet-2026-06-28.md`
- `docs/publisher/ru-editor-facing-brief-2026-06-28.md`
- `docs/publisher/ru-companion-readiness-pass-2026-06-28.md`
- `docs/publisher/ru-companion-example-artifacts-plan-2026-06-28.md`
- `docs/publisher/ru-final-fact-check-backlog-2026-06-28.md`
- `docs/publisher/ru-source-verification-packet-2026-06-28.md`
- `docs/publisher/ru-post-author-final-export-workflow-2026-06-28.md`

## What is now stable

- The manuscript is the full Google Doc, not the old compressed 71-72 page
  snapshot.
- The structure is 7 parts, 23 chapters, front matter, glossary, practical
  cases and appendices.
- The H2/H3 body-style debt is closed for the current proof.
- The current raw export and Template2000n derivative have the same paragraph
  text sequence.
- The author/front-matter section now clearly separates author-owned fields
  from missing book content.
- Internal iteration reports are not part of the clean external packet unless
  the editor explicitly asks for process evidence.

## What the editor should review first

1. The reader arc: demo-agent failure -> platform responsibility -> safety and
   control -> memory/retrieval -> execution/runtime -> evidence/evals ->
   organization/ADLC -> launch.
2. The late-book density: chapters 20-23 must remain readable as lifecycle and
   launch guidance, not as a reference manual.
3. The repeated chapter rhythms: repeated checklists should feel intentional
   and useful, not mechanical.
4. The book/companion boundary: print keeps the architectural argument and
   minimum working artifacts; companion keeps long YAML/CLI/runtime/reference
   material.
5. The author voice: reduce places where the text reads like assembled
   documentation instead of a coherent IT book.

## Not final until the author fills

The author still owns these facts before final publisher submission:

- short and long author bio;
- role/title and public positioning;
- verified experience and public projects;
- GitHub/site/blog/profile links;
- final title, subtitle and cover copy;
- public companion URL, release version, changelog and errata route;
- legal/compliance disclaimer;
- AI tooling disclosure;
- decision on real vs composite cases;
- acknowledgements;
- final publisher metadata.

## Recommended external packet

For first serious editor review, send:

1. Google Doc link.
2. Template2000n DOCX proof candidate.
3. Raw Google Docs export as fallback.
4. This handoff packet.
5. Author open-fields report.
6. Author query packet.
7. Editor-facing brief.
8. Publisher-style pass report.
9. Companion readiness pass.
10. Final fact-check backlog.
11. Source verification packet.

Do not send internal 100-iteration logs unless the editor asks for the
preparation trail.

## Repository control files

- Roadmap: `docs/publisher/ru-editorial-roadmap.md`
- Workflow: `docs/publisher/ru-google-doc-workflow.md`
- Evolution ledger: `docs/publisher/ru-manuscript-evolution.md`
- Manuscript map: `docs/publisher/ru-manuscript-map.md`
- Submission checklist: `docs/publisher/ru-submission-checklist.md`
- Author open fields: `docs/publisher/ru-author-open-fields-2026-06-28.md`
- Author query packet: `docs/publisher/ru-author-query-packet-2026-06-28.md`
- Editor-facing brief: `docs/publisher/ru-editor-facing-brief-2026-06-28.md`
- Companion readiness pass:
  `docs/publisher/ru-companion-readiness-pass-2026-06-28.md`
- Companion example artifacts plan:
  `docs/publisher/ru-companion-example-artifacts-plan-2026-06-28.md`
- Fact-check backlog:
  `docs/publisher/ru-final-fact-check-backlog-2026-06-28.md`
- Source verification packet:
  `docs/publisher/ru-source-verification-packet-2026-06-28.md`
- Editor comment intake workflow:
  `docs/publisher/ru-editor-comment-intake-workflow-2026-06-28.md`
- Final placeholder/link scan workflow:
  `docs/publisher/ru-final-placeholder-link-scan-workflow-2026-06-28.md`
- Post-author export workflow:
  `docs/publisher/ru-post-author-final-export-workflow-2026-06-28.md`
- Next 100 goals:
  `docs/publisher/ru-editorial-100-final-scan-iterations-2026-06-28.md`
