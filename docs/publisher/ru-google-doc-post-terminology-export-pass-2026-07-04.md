# Google Doc post-terminology export pass

Date: 2026-07-04.

Status: completed as a publisher proof checkpoint. This is still not the final
publisher submission because author-owned fields and independent external
proofread remain open.

Google Doc:

- <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>

## Implemented plan

1. Cleaned the active Google Doc manuscript after the quality-sync pass.
2. Saved a fresh authenticated raw DOCX export from the updated Google Doc.
3. Rebuilt the Template2000n derivative from that fresh raw DOCX baseline.
4. Rendered raw and Template2000n DOCX proofs to PDF/PNG and checked page
   counts, blank-like pages and low-density pages.
5. Updated repository reports, checkpoint notes and the next 100 editorial
   goals.
6. Prepared the repository for commit and push.

## Google Doc update

Revision before this post-terminology cleanup:

- `ALtnJHxkd-6hTZn1wEzTpTSAHUAVcPv-Bg7jAh8pAZiEQjlPdEXA0lZRmqtSoIxtrcWwY01MRjL5tLyIFq724WFnRxgx9vh92uvk7tQgB58`

Final revision after this pass:

- `ALtnJHzZWz2-IJ7JpxskwAFAeTHIK5wTRmKA_MrDjFTgOlPIbOMvFgV7Go8Trlwx1WPtElObAQ1OmEI0Tbg7i8I4NJ5RyfZdmR8apePtOyc`

Applied direct guarded replacements in Google Doc: `116` total:

- `32` occurrences of `rollout wave` -> `волна поэтапного выпуска`;
- `5` broken `вызов инструментаing` forms fixed;
- `18` major `Online companion` / `Companion route` forms normalized;
- `33` grammatical and падежные corrections around online-support and
  companion-material wording;
- `12` remaining appendix-level `companion` placeholders normalized or marked
  as author-owned public URL placeholders;
- `15` broader `companion` prose leftovers normalized while keeping
  `docs/companion/...` paths intact;
- `1` mixed-language retirement paragraph rewritten in Russian.

Checked exact bad markers after export; all were absent in the saved raw DOCX:

- `вызов инструментаing`;
- `Online companion`;
- `Companion route`;
- `Companion должен`;
- `Структура репозитория companion`;
- `Чеклист готовности companion`;
- `Как устроен онлайн-сопровождение`;
- `Зачем нужен онлайн-сопровождение`;
- `Адрес онлайн-сопровождение`;
- `материаловs`;
- `Product docs and`;
- `migration and communication`;
- `Публичная версия онлайн-сопровождения: онлайн-сопровождение.`

Accepted technical English terms, identifiers, paths and artifact names were
left intact where they are part of the engineering vocabulary or code surface.

## DOCX artifacts

Fresh raw Google Docs export:

- `docs/publisher/artifacts/agent-arch-ru-post-terminology-raw-2026-07-04.docx`
- bytes: `689758`
- SHA-256:
  `089e419c83a79685f8be99da04e3edf4638ec0d3b0edde592ba94bfadeb1310a`
- paragraphs: `8187`
- non-empty paragraphs: `6109`
- approximate words: `99884`

Template2000n derivative from that raw export:

- `docs/publisher/artifacts/agent-arch-ru-template2000n-post-terminology-2026-07-04.docx`
- bytes: `697015`
- SHA-256:
  `2db2a5e3eafb1ca9afdef9d5f89ef21b8c71f0df4e2aeb42dc4a77fa33e93e00`
- paragraphs: `8187`
- non-empty paragraphs: `6109`
- approximate words: `99884`
- no-style body paragraphs mapped to `Body Text`: `4957`
- raw/styled paragraph text equality: preserved

The attached `Template2000n.dot` was converted with headless LibreOffice using
an isolated temporary user profile. No Template2000n macros were executed.

## Render QA

Raw Google Docs export:

- pages: `493`
- blank-like pages: `0`
- contact sheet:
  `/tmp/agent-arch-ru-post-terminology-final3-raw-contact-2026-07-04.png`
- lowest-density page spot-check: page `359`, confirmed as a short paragraph
  tail, not a blank page.

Template2000n derivative:

- pages: `359`
- blank-like pages: `0`
- contact sheet:
  `/tmp/agent-arch-ru-template2000n-post-terminology-final3-contact-2026-07-04.png`
- lowest-density page spot-checks: pages `238` and `240`, confirmed as short
  headed sections, not blank pages.

Machine-readable QA:

- `docs/publisher/ru-google-doc-post-terminology-export-pass-2026-07-04.render-qa.json`
- `docs/publisher/ru-template2000n-post-terminology-2026-07-04.metrics.json`

## Repository updates

Updated:

- `docs/publisher/ru-manuscript-full.md`;
- `docs/publisher/ru-manuscript-evolution.md`;
- `docs/publisher/ru-google-doc-workflow.md`;
- `docs/publisher/ru-submission-checklist.md`.

Added:

- `docs/publisher/artifacts/agent-arch-ru-post-terminology-raw-2026-07-04.docx`;
- `docs/publisher/artifacts/agent-arch-ru-template2000n-post-terminology-2026-07-04.docx`;
- `docs/publisher/ru-google-doc-post-terminology-export-pass-2026-07-04.md`;
- `docs/publisher/ru-google-doc-post-terminology-export-pass-2026-07-04.render-qa.json`;
- `docs/publisher/ru-template2000n-post-terminology-2026-07-04.metrics.json`;
- `docs/publisher/ru-editorial-100-post-terminology-export-iterations-2026-07-04.md`.

## Remaining author-owned fields

The author still needs to fill or explicitly omit:

- public author name/byline;
- short and long author bio;
- role/public positioning;
- verified experience claims;
- public project links;
- public online-support URL, versioning, changelog and errata route;
- acknowledgements;
- legal/compliance disclaimer wording if publisher requires it;
- AI-use disclosure wording if publisher requires it;
- final title, subtitle, cover copy and imprint metadata.

## Decision

The earlier quality-sync limitation is closed: the repository now contains a
fresh raw DOCX export from the updated Google Doc and a matching Template2000n
proof with render QA. The best current publisher-facing proof artifact is the
Template2000n post-terminology DOCX on `359` rendered pages. Final submission
still waits for author-owned fields, external proofread and any publisher style
requirements received after this checkpoint.
