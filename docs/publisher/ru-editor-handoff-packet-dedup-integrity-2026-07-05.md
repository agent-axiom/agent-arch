# RU editor handoff packet: dedup/source sync + integrity follow-up

Date: 2026-07-05.

Status: working editor handoff proof. This is not the final publisher
submission; author-owned fields, public companion metadata, external proofread
and publisher style acceptance remain open.

Google Doc:

- <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI/edit>

Final known Google Doc revision:

- `ALtnJHyYapbkiUC6iu1GxFan0C6cwyoMIHWVI320Wi1XqXC0-S6pZYCU543zoWAUmarcQdnT2TyRrpBWXhpeyd74AxV5wI19jHeRRlqYp9U`

## Current proof files

Raw Google Doc DOCX uploaded to Drive:

- `docs/publisher/artifacts/agent-arch-ru-google-doc-dedup-source-sync-2026-07-05.docx`
- 522 rendered pages
- 0 blank-like pages
- 8558 paragraphs
- 6456 non-empty paragraphs
- approximately 105808 words

Template2000n derivative:

- `docs/publisher/artifacts/agent-arch-ru-template2000n-dedup-source-sync-2026-07-05.docx`
- 379 rendered pages
- 0 blank-like pages
- raw/styled paragraph text equality preserved
- 8558 paragraphs
- 6456 non-empty paragraphs
- approximately 105808 words
- 5243 body paragraphs mapped to `Body Text`

Machine-readable QA:

- `docs/publisher/ru-google-doc-dedup-source-sync-2026-07-05.render-qa.json`
- `docs/publisher/ru-template2000n-dedup-source-sync-2026-07-05.render-qa.json`
- `docs/publisher/ru-template2000n-dedup-source-sync-2026-07-05.metrics.json`

## Source and integrity status

- Repository source additions from `docs/book/part-viii/chapter-24.md` and
  `docs/book/part-viii/chapter-25.md` are represented in the working
  manuscript through Chapter 20 and Chapter 15 additions.
- `docs/publisher/ru-source-map.md` records the source contribution for those
  chapters.
- `docs/publisher/ru-manuscript-full.md` has chapters 1-23 in order.
- Exact duplicate paragraph groups with 35+ words in the local full Markdown
  assembly: 0.
- Exact duplicate paragraph groups with 35+ words in the raw DOCX proof: 0.
- Raw DOCX paragraphs with 250+ words: 0.
- Embedded visual assets in the DOCX proof: 12 PNG files.
- Visible mixed suffix forms checked and removed from the current proof:
  `шлюз выпускаs`, `шлюз оценкиs`, `регрессионный шлюзs`,
  `человеческой проверкиer`, `волна поэтапного выпускаs`,
  `шлюз подтвержденияs`, `production-контроля`.
- Current chapter cross-references were checked for the known stale numbering
  patterns from the compressed assembly and corrected in the local source.
- Reader-recommendability follow-up added six production scenes, continuity
  bridges, maturity bridges, final assembly framing and 23 chapter takeaway
  blocks to the current proof.
- Three-reader-profiles follow-up added explicit routes for architects,
  engineering managers/CTOs and developers, seven part-level profile outcome
  blocks and 23 chapter forwarding hooks to the current proof.
- Page-turner/workshop follow-up added one through-line block, seven
  part-level team workshop blocks and 23 concrete next actions after chapter
  forwarding hooks.
- Case/thesis follow-up made the support-agent storyline the explicit
  recurring production case, added seven part-level case episodes and 23
  quotable chapter theses.

## Editor review focus

1. Verify that the compressed Google Doc proof keeps a coherent reading line
   despite being shorter than the full Markdown source assembly.
2. Review the new Chapter 15 control-evaluation/adversarial-testing block as a
   governance-loop section, not only as final-answer evaluation content.
3. Review the new Chapter 20 agentic goal-misalignment / insider-risk block as
   part of the assurance loop.
4. Decide whether the 12 visualization assets should stay in their current
   proof locations or move closer to the first chapter references.
5. Check remaining English technical terms. Terms such as `trace`,
   `observability`, `eval`, `SLO`, `prompt injection`, `red team` and `ADLC`
   are intentionally retained where they function as industry terms, but the
   editor may choose stronger Russian phrasing in narrative prose.
6. Review the seven new team workshop blocks as possible recurring boxed
   material or part-closing exercises.
7. Review the 23 `Фраза для пересказа` lines for tone: each should be sharp
   enough to quote but not more absolute than the chapter evidence supports.
8. Re-run export/render QA after author fields and editor changes are applied.

## Author-owned fields still required

The author should fill or explicitly omit:

- public author name and byline;
- short author bio for the book;
- longer author bio for publisher metadata;
- role, public positioning and professional affiliation wording;
- verified experience claims that can be printed;
- public project links;
- public companion URL and versioning policy;
- acknowledgements;
- legal/compliance disclaimer wording;
- AI-use disclosure if required by the publisher;
- final publisher metadata and cover copy.

## Handoff decision

Use
`docs/publisher/artifacts/agent-arch-ru-template2000n-dedup-source-sync-2026-07-05.docx`
as the current publisher-facing proof for layout/style review, and use the
Google Doc as the living manuscript workspace.
