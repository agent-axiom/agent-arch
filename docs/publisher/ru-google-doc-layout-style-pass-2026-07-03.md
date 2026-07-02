# Google Doc layout/style proof pass

Date: 2026-07-03.

Status: completed working-proof cleanup for the full Russian Google Doc
manuscript. This is not a final publisher-ready submission.

Google Doc:

- <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>
- tab: `t.0`
- final checked revision after style-only Google Doc updates:
  `ALtnJHwIVs8gJyJyrGPDctcgdF7ErhiFjFyvH-7E7UDpz7uFhzRhtfVmGsJgSN1xJRlyDTnkL9l8xz6mXFF5DhkyL_Tlw4vPeghlejfY9yc`

## Implemented plan

1. Fixed the known page-338/layout debt from the previous practice-polish
   proof. The `15. Eval readiness checklist перед rollout` block no longer has
   the old one-line `Hard blockers` carryover on a mostly empty page.
2. Checked page breaks around all new practice blocks. One orphan-prone SLO
   practice heading was moved to a clean page start.
3. Checked H1/H2/H3 outline after edits. Five practice body ranges were
   demoted from heading styles to normal text, and three late practice headings
   were promoted to navigable `Heading 2`.
4. Exported/refreshed the raw DOCX working proof and preserved non-empty text
   equality with the previous practice-polish proof.
5. Built a fresh Template2000n/publisher-style derivative from the current raw
   proof using the checked derivative route, not by running the legacy `.dot`
   macros.
6. Rendered raw and Template2000n proofs to PDF/PNG and ran blank-like page
   checks plus targeted visual checks.
7. Updated the editorial packet state and added the next 100 editorial goals.

## Artifacts

Raw working proof:

- `docs/publisher/artifacts/agent-arch-ru-layout-style-pass-2026-07-02.docx`
- bytes: `688755`
- SHA-256:
  `c5d19d5de61d74f5a25f50f759c7e2b68153455ee3056a4e450d4a8cc3200040`
- paragraphs: `8179`
- non-empty paragraphs: `6105`
- approximate words: `99924`

Template2000n derivative:

- `docs/publisher/artifacts/agent-arch-ru-template2000n-layout-style-pass-2026-07-02.docx`
- bytes: `691476`
- SHA-256:
  `7aa67b19c47eb762ed9706aa4e888167ddb78362c9a20d8b60503e1eafc68ff5`
- paragraphs: `8179`
- non-empty paragraphs: `6105`
- approximate words: `99924`

Report metadata:

- `docs/publisher/ru-google-doc-layout-style-pass-2026-07-03.render-qa.json`
- `docs/publisher/ru-editorial-100-layout-style-proof-iterations-2026-07-03.md`

## Style metrics

Raw proof:

- `Heading1`: `26`
- `Heading2`: `762`
- `Heading3`: `513`
- `Heading4`: `51`
- `Normal`: `4753`
- practice headings: `14`

Template2000n derivative:

- `Heading1`: `26`
- `Heading2`: `762`
- `Heading3`: `513`
- `Heading4`: `51`
- `BodyText`: `4753`
- practice headings: `14`

Text integrity:

- Raw non-empty text equals previous practice-polish proof non-empty text.
- Raw text equals Template2000n derivative paragraph text.
- Raw and Template2000n paragraph counts match.

## Render QA

Raw proof:

- PDF:
  `/tmp/agent-arch-ru-layout-style-raw-render-2026-07-03-clean/agent-arch-ru-layout-style-pass-2026-07-02.pdf`
- pages: `507`
- PNG pages: `507`
- blank-like pages: `0`
- lowest-density page: `62`, nonwhite ratio `0.007205141335716643`
- final page: `507`

Template2000n derivative:

- PDF:
  `/tmp/agent-arch-ru-layout-style-template2000n-render-2026-07-03-clean/agent-arch-ru-template2000n-layout-style-pass-2026-07-02.pdf`
- pages: `371`
- PNG pages: `371`
- blank-like pages: `0`
- lowest-density page: `343`, nonwhite ratio `0.004608190774965177`
- final page: `371`

Targeted checks:

- raw pages `286`, `310`, `334`, `335`, `349`, `368`, `412`, `428`, `431`;
- Template2000n pages `202`, `221`, `242`, `243`, `252`, `267`, `298`,
  `310`, `312`;
- title, low-density and final pages in both proof sets.

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

The current Google Doc and the two 2026-07-02 DOCX proofs are the best working
layout/style proof artifacts for editorial review. Final publisher submission
remains blocked until author-owned fields, final proofread, publisher-approved
style requirements and final export QA are closed.
