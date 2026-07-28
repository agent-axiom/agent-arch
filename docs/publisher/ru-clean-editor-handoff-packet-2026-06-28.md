# Clean editor handoff packet: русская рукопись

Date: 2026-06-28.

Status: clean editorial handoff for the current full manuscript. This is the
best current working package for an editor, but not the final publisher
submission until author-owned facts and external proofread are closed.

## Main manuscript

- Google Doc:
  <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>
- Title: `Архитектура безопасных ИИ-агентов - полная рукопись`
- Current revision after companion/source-status sync:
  `ALtnJHwQSbMVcXf5UUw3QyuuxPZVGdtR-7yOKUdJM8DtE76ktgR6WhHDA0zngCtIQFMNxPaYHMglaPHowPxYQS8TpcL8wryth-RYjYpT_iQ`

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
- `docs/publisher/ru-live-source-verification-actions-2026-06-29.md`
- `docs/publisher/ru-live-source-verification-pass-2026-06-29.md`
- `docs/publisher/ru-full-source-verification-pass-2026-06-29.md`
- `docs/publisher/ru-source-url-live-check-2026-06-29.tsv`
- `docs/publisher/ru-source-follow-up-pass-2026-06-30.md`
- `docs/publisher/ru-source-follow-up-live-check-2026-06-30.tsv`
- `docs/publisher/ru-google-doc-companion-source-sync-pass-2026-06-29.md`
- `docs/publisher/ru-mechanical-scan-report-2026-06-29.md`
- `docs/publisher/ru-final-external-packet-outline-2026-06-29.md`
- `docs/publisher/ru-author-owned-final-inputs-2026-06-29.md`
- `docs/publisher/ru-author-intake-ready-pass-2026-06-29.md`
- `docs/publisher/ru-author-input-closure-packet-2026-06-30.md`
- `docs/publisher/ru-pre-author-finalization-pass-2026-07-01.md`
- `docs/publisher/ru-final-placeholder-source-readiness-pass-2026-07-01.md`
- `docs/publisher/ru-pre-author-export-gate-2026-07-01.md`
- `docs/publisher/ru-pre-author-final-export-readiness-2026-06-29.md`
- `docs/publisher/ru-final-export-readiness-after-source-pass-2026-06-29.md`
- `docs/publisher/ru-pre-final-export-readiness-after-follow-up-2026-06-30.md`
- `docs/publisher/ru-sendable-editor-packet-state-2026-06-29.md`
- `docs/publisher/ru-final-editor-packet-skeleton-2026-06-30.md`
- `docs/publisher/ru-external-packet-readiness-pass-2026-06-29.md`
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
- Print-facing reference pages now link to companion examples and trace/eval
  artifacts for the support-ticket case.
- Mechanical placeholder/link scan, live source verification actions and final
  external packet outline are documented.
- Google Doc companion/source-status wording is synchronized and recorded.
- Representative P0 live source pass is complete.
- Full source catalog URL availability pass is complete, and the targeted
  2026-06-30 follow-up resolved the actionable blocked URL cleanup. OpenReview
  records are demoted to non-primary research leads and are not part of the
  primary evidence set for the final editor packet.
- Internal iteration reports are not part of the clean external packet unless
  the editor explicitly asks for process evidence.
- The 2026-07-01 pre-author finalization gate is recorded: final DOCX export,
  Template2000n final derivative and final render QA are intentionally deferred
  until author-owned fields are filled or explicitly omitted.

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
12. P0 live source verification pass.
13. Mechanical scan report.
14. Final external packet outline.

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
- Live source verification actions:
  `docs/publisher/ru-live-source-verification-actions-2026-06-29.md`
- P0 live source verification pass:
  `docs/publisher/ru-live-source-verification-pass-2026-06-29.md`
- Full source URL availability pass:
  `docs/publisher/ru-full-source-verification-pass-2026-06-29.md`
- Source URL availability evidence TSV:
  `docs/publisher/ru-source-url-live-check-2026-06-29.tsv`
- Google Doc companion/source-status sync:
  `docs/publisher/ru-google-doc-companion-source-sync-pass-2026-06-29.md`
- Mechanical scan report:
  `docs/publisher/ru-mechanical-scan-report-2026-06-29.md`
- Final external packet outline:
  `docs/publisher/ru-final-external-packet-outline-2026-06-29.md`
- Author-owned final inputs:
  `docs/publisher/ru-author-owned-final-inputs-2026-06-29.md`
- Author intake ready pass:
  `docs/publisher/ru-author-intake-ready-pass-2026-06-29.md`
- Pre-author final export readiness:
  `docs/publisher/ru-pre-author-final-export-readiness-2026-06-29.md`
- Final export readiness after source pass:
  `docs/publisher/ru-final-export-readiness-after-source-pass-2026-06-29.md`
- Sendable editor packet state:
  `docs/publisher/ru-sendable-editor-packet-state-2026-06-29.md`
- External packet readiness pass:
  `docs/publisher/ru-external-packet-readiness-pass-2026-06-29.md`
- Editor comment intake workflow:
  `docs/publisher/ru-editor-comment-intake-workflow-2026-06-28.md`
- Final placeholder/link scan workflow:
  `docs/publisher/ru-final-placeholder-link-scan-workflow-2026-06-28.md`
- Post-author export workflow:
  `docs/publisher/ru-post-author-final-export-workflow-2026-06-28.md`
- Next 100 goals:
  `docs/publisher/ru-editorial-100-external-packet-iterations-2026-06-29.md`
- Next 100 source/author/finalization goals:
  `docs/publisher/ru-editorial-100-source-author-finalization-iterations-2026-06-29.md`
- Next 100 final editorial goals:
  `docs/publisher/ru-editorial-100-final-editorial-iterations-2026-06-29.md`
- Next 100 author/source/export goals:
  `docs/publisher/ru-editorial-100-author-source-export-iterations-2026-06-30.md`
- Next 100 final packet goals:
  `docs/publisher/ru-editorial-100-final-packet-iterations-2026-06-30.md`
