# Google Doc Template2000n official style pass

Date: 2026-07-03.

Status: completed. This pass applies the attached `Template2000n.dot` style
package to a fresh DOCX export of the existing Google Doc manuscript and
verifies the result through raw and styled render QA. It is a publisher-style
proof pass, not a final publisher-ready submission.

Google Doc:

- <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>
- connector modified time at export: `2026-07-02T22:46:03.373Z`

## Implemented plan

1. Inspected the attached `Template2000n.dot` file. It is a legacy Word 2000
   binary template (`Composite Document File V2`, code page 1251, 107008 bytes).
2. Exported a fresh raw DOCX from the current Google Doc.
3. Converted the `.dot` to `/tmp/Template2000n.docx` with headless LibreOffice
   as a style source. No VBA/macros were executed.
4. Built a conservative Template2000n derivative:
   - copied `styles.xml`, `theme1.xml` and `fontTable.xml` from the converted
     template;
   - preserved raw Google Docs `numbering.xml` to keep existing list structure;
   - removed legacy `numPr` from `Heading1`-`Heading5` style definitions;
   - mapped `4953` no-style body paragraphs to `BodyText`.
5. Verified raw/styled text equality, DOCX archive integrity and render QA.
6. Updated the editorial packet state and created the next 100 style/finalization
   goals.

## Artifacts

Raw working proof:

- `docs/publisher/artifacts/agent-arch-ru-publisher-style-raw-2026-07-03.docx`
- bytes: `687813`
- SHA-256: `b47d5bddd773891c02649659cb1c5df0ca92f25eaeab3d76329eafec8ce54e7c`
- paragraphs: `8179`
- non-empty paragraphs: `6105`
- approximate words: `99587`

Template2000n official-style derivative:

- `docs/publisher/artifacts/agent-arch-ru-template2000n-official-style-pass-2026-07-03.docx`
- bytes: `693413`
- SHA-256: `a3dfea607a7c6be19d8cc215033fe421e77a4ebf774fc624b178f97b006b216b`
- paragraphs: `8179`
- non-empty paragraphs: `6105`
- approximate words: `99587`

Report metadata:

- `docs/publisher/ru-google-doc-template2000n-official-style-pass-2026-07-03.render-qa.json`
- `docs/publisher/ru-editorial-100-template2000n-official-style-iterations-2026-07-03.md`

## Style metrics

Raw proof:

- `Heading1`: `26`
- `Heading2`: `567`
- `Heading3`: `508`
- `Heading4`: `51`
- `Normal`: `4953`
- `BodyText`: `0`

Template2000n official-style derivative:

- `Heading1`: `26`
- `Heading2`: `567`
- `Heading3`: `508`
- `Heading4`: `51`
- `Normal`: `0`
- `BodyText`: `4953`
- missing style refs: `0`

Text integrity:

- Raw non-empty paragraph count equals Template2000n non-empty paragraph count.
- Raw paragraph text equals Template2000n paragraph text.
- Raw and styled word counts are unchanged: `99587`.

## Render QA

Raw proof:

- PDF:
  `/tmp/agent-arch-ru-publisher-style-raw-render-2026-07-03/agent-arch-ru-publisher-style-raw-2026-07-03.pdf`
- pages: `489`
- PNG pages: `489`
- blank-like pages: `0`
- lowest-density pages checked: `62`, `125`, `296`, `302`, `41`, `326`,
  `297`, `327`, `300`, `325`
- final page: `489`

Template2000n official-style derivative:

- PDF:
  `/tmp/agent-arch-ru-template2000n-official-style-render-2026-07-03/agent-arch-ru-template2000n-official-style-pass-2026-07-03.pdf`
- pages: `357`
- PNG pages: `357`
- blank-like pages: `0`
- lowest-density pages checked: `238`, `240`, `219`, `215`, `208`, `41`,
  `230`, `239`, `241`, `31`
- final page: `357`

Targeted visual checks:

- raw contact sheet:
  `/tmp/agent-arch-ru-publisher-style-raw-contact-2026-07-03.png`
- Template2000n contact sheet:
  `/tmp/agent-arch-ru-template2000n-official-style-contact-2026-07-03.png`

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

The attached Template2000n style package has now been applied to a fresh Google
Doc export in a conservative, macro-free way. The resulting styled DOCX is the
current publisher-style proof candidate for editorial review. Final publisher
submission remains blocked until author-owned fields, full human proofread,
publisher/editor acceptance of this style route and final export QA are closed.
