# Google Doc dedup/source sync pass

Date: 2026-07-05.

Status: completed for the current working manuscript. This is not the final
publisher submission because author-owned fields, public companion metadata,
external proofread and publisher style acceptance remain open.

Google Doc:

- <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>

Final known Google Doc revision for this pass:

- `ALtnJHyYapbkiUC6iu1GxFan0C6cwyoMIHWVI320Wi1XqXC0-S6pZYCU543zoWAUmarcQdnT2TyRrpBWXhpeyd74AxV5wI19jHeRRlqYp9U`

## Implemented changes

1. Added a Chapter 15 block on control evaluations and automated adversarial
   testing as checks of the governance loop, not only final-answer quality.
2. Added a Chapter 20 block on agentic goal misalignment and insider-style risk
   inside the assurance loop.
3. Cleaned the local full Markdown assembly by removing large structural
   duplicates: reference package repeats, policy/catalog repeats, incident
   template repeats and repeated policy/checklist resets.
4. Updated `docs/publisher/ru-source-map.md` so Chapter 15 now cites
   `docs/book/part-viii/chapter-25.md` and Chapter 20 cites
   `docs/book/part-viii/chapter-24.md`.
5. Replaced the Drive file content with a cleaned raw DOCX while preserving the
   same Google Doc URL. During upload the file became a native Google Docs
   document.
6. Rebuilt the Template2000n proof from the cleaned raw DOCX and preserved text
   equality.
7. Removed 15 trailing empty DOCX paragraphs that caused a blank trailing page
   in the first Template2000n render.
8. Completed an integrity follow-up: corrected stale cross-references to the
   renumbered chapters and removed visible mixed suffix forms such as
   `шлюз выпускаs`, `шлюз оценкиs`, `регрессионный шлюзs`,
   `человеческой проверкиer`, `волна поэтапного выпускаs` and
   `production-контроля` from the current DOCX/Google Doc proof.
9. Completed a reader-recommendability follow-up: strengthened the opening
   promise, added production scenes, continuity bridges, maturity bridges and
   chapter takeaway blocks, then uploaded the updated raw DOCX back to the
   same Google Doc.
10. Completed a three-reader-profiles follow-up: added explicit routes and
   part-level outcomes for technical leads/architects, engineering
   managers/CTOs and practicing developers, then added 23 chapter forwarding
   hooks.
11. Completed a page-turner/workshop follow-up: added a through-line block,
   seven part-level team workshop blocks and 23 concrete next actions after
   the chapter forwarding hooks.
12. Completed a case/thesis follow-up: made the support-agent story the
   explicit recurring production case, added seven part-level case episodes
   and added 23 quotable chapter theses.

## Duplicate checks

Local Markdown assembly:

- before this pass: 92 exact duplicate paragraph groups with 35+ words;
- after this pass: 0 exact duplicate paragraph groups with 35+ words;
- current word count: 114574.

Drive/raw DOCX working manuscript:

- exact duplicate paragraph groups with 35+ words: 0;
- paragraphs with 250+ words: 0.

## Artifacts

Raw Google Doc DOCX uploaded to Drive:

- `docs/publisher/artifacts/agent-arch-ru-google-doc-dedup-source-sync-2026-07-05.docx`
- paragraphs: 8558
- non-empty paragraphs: 6456
- approximate words: 105808

Template2000n derivative:

- `docs/publisher/artifacts/agent-arch-ru-template2000n-dedup-source-sync-2026-07-05.docx`
- paragraphs: 8558
- non-empty paragraphs: 6456
- approximate words: 105808
- raw/styled paragraph text equality: preserved
- body paragraphs mapped to `Body Text`: 5243

Machine-readable QA:

- `docs/publisher/ru-google-doc-dedup-source-sync-2026-07-05.render-qa.json`
- `docs/publisher/ru-template2000n-dedup-source-sync-2026-07-05.render-qa.json`
- `docs/publisher/ru-template2000n-dedup-source-sync-2026-07-05.metrics.json`

## Render QA

Raw Google Doc DOCX:

- pages: 522;
- blank-like pages: 0;
- contact sheet:
  `/tmp/agent_arch_ru_google_doc_case_thesis_2026_07_05_render/contact-sheet.png`.

Template2000n derivative:

- pages: 379;
- blank-like pages: 0;
- contact sheet:
  `/tmp/agent_arch_ru_template2000n_case_thesis_2026_07_05_render/contact-sheet.png`.

DOCX archive integrity:

- raw DOCX: `unzip -t` passed;
- Template2000n DOCX: `unzip -t` passed.

## Remaining author-owned fields

The author still needs to fill or explicitly omit:

- public author name/byline;
- short and long author bio;
- role/public positioning;
- verified experience claims;
- public project links;
- public companion URL/version;
- acknowledgements;
- legal/compliance disclaimer;
- AI-use disclosure if required by the publisher;
- final publisher metadata and cover copy.
