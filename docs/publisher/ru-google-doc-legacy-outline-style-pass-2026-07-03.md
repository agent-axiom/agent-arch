# Google Doc legacy outline/style pass

Date: 2026-07-03.

Status: completed. This pass was applied directly to the existing Google Doc
manuscript and then verified through fresh raw and Template2000n DOCX proofs.
It is a style-only proof pass, not a final publisher-ready submission.

Google Doc:

- <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>
- tab: `t.0`
- final checked revision after style-only Google Doc updates:
  `ALtnJHwG2y0y6xdziVEBWf1jHm7r6i_bkXLaj0f_p_1raU2fzYu7XbniNYm86oBYvk_aFiwhUgAkAa8LnjW7E-hl6iMi5fJR-77zzvllovI`

## Implemented plan

1. Audited legacy long `Heading2`/`Heading3` body-style debt in the previous
   layout/style proof.
2. Applied safe `updateParagraphStyle` cleanup ranges in the existing Google
   Doc. The cleanup targeted memory review cards, trace fields, SLO/eval
   checklists, ownership/readiness checklists, launch checklist and appendix
   template fields.
3. Exported a fresh raw DOCX proof from the updated Google Doc.
4. Built a fresh Template2000n/publisher-style derivative from the current raw
   proof using the checked derivative route, not by running the legacy `.dot`
   macros.
5. Rendered raw and Template2000n proofs to PDF/PNG and ran blank-like page
   checks plus targeted visual checks.
6. Updated the editorial packet state and created the next 100 editorial goals.

## Artifacts

Raw working proof:

- `docs/publisher/artifacts/agent-arch-ru-legacy-outline-style-pass-2026-07-03.docx`
- bytes: `687813`
- SHA-256: `2a293f065a4b28bc8f3ac7c42d39744122e1591ce20fae9c5efe2a95e5146302`
- paragraphs: `8179`
- non-empty paragraphs: `6105`
- approximate words: `99587`

Template2000n derivative:

- `docs/publisher/artifacts/agent-arch-ru-template2000n-legacy-outline-style-pass-2026-07-03.docx`
- bytes: `690067`
- SHA-256: `3cfa021aebc3d2c237c8147096d65c2fcb272b8181a0fa8d4c95653ae7be199d`
- paragraphs: `8179`
- non-empty paragraphs: `6105`
- approximate words: `99587`

Report metadata:

- `docs/publisher/ru-google-doc-legacy-outline-style-pass-2026-07-03.render-qa.json`
- `docs/publisher/ru-editorial-100-legacy-outline-style-iterations-2026-07-03.md`

## Style metrics

Previous layout/style proof:

- heading paragraphs: `1352`
- `Heading1`: `26`
- `Heading2`: `762`
- `Heading3`: `513`
- `Heading4`: `51`

Current raw proof:

- heading paragraphs: `1152`
- `Heading1`: `26`
- `Heading2`: `567`
- `Heading3`: `508`
- `Heading4`: `51`
- `Normal`: `4953`

Template2000n derivative:

- `Heading1`: `26`
- `Heading2`: `567`
- `Heading3`: `508`
- `Heading4`: `51`
- `BodyText`: `4953`

Result: `200` legacy body-like paragraphs were removed from the automatic
heading structure while preserving the manuscript text volume.

Text integrity:

- Raw non-empty paragraph count equals Template2000n non-empty paragraph count.
- Raw paragraph text equals Template2000n paragraph text.
- Raw word count is unchanged from the previous layout/style proof: `99587`.

## Render QA

Raw proof:

- PDF:
  `/tmp/agent-arch-ru-legacy-outline-raw-render-2026-07-03/agent-arch-ru-legacy-outline-style-pass-2026-07-03.pdf`
- pages: `489`
- PNG pages: `489`
- blank-like pages: `0`
- lowest-density pages checked: `62`, `125`, `296`, `302`, `41`, `326`,
  `297`, `327`
- final page: `489`

Template2000n derivative:

- PDF:
  `/tmp/agent-arch-ru-legacy-outline-template2000n-render-2026-07-03/agent-arch-ru-template2000n-legacy-outline-style-pass-2026-07-03.pdf`
- pages: `351`
- PNG pages: `351`
- blank-like pages: `0`
- lowest-density pages checked: `232`, `234`, `213`, `209`, `41`, `224`,
  `233`, `235`
- final page: `351`

Targeted visual checks:

- raw contact sheet:
  `/tmp/agent-arch-ru-legacy-outline-raw-contact-2026-07-03.png`
- Template2000n contact sheet:
  `/tmp/agent-arch-ru-legacy-outline-template-contact-2026-07-03.png`

The targeted pages were visually checked through contact sheets. This pass is
automated render QA plus targeted visual review, not a full human proofread of
every page.

## Remaining author-owned fields

The author still needs to fill or explicitly omit:

- public author name/byline;
- short and long author bio;
- role/public positioning;
- verified experience claims that can appear in the book;
- public project links;
- companion URL and versioning/changelog/errata route;
- acknowledgements;
- legal/compliance disclaimer wording if publisher requires it;
- AI-use disclosure wording if publisher requires it;
- final title/subtitle/cover-copy/imprint metadata.

## Decision

The current Google Doc and the two 2026-07-03 DOCX proofs are the best working
outline/style proof artifacts for editorial review. The pass materially reduces
false outline noise without shrinking the manuscript text. Final publisher
submission remains blocked until author-owned fields, external proofread,
publisher-approved style requirements and final export QA are closed.
