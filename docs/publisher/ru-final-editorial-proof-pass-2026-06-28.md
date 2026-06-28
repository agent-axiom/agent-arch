# Final editorial proof pass

Date: 2026-06-28

Google Doc: <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>

Goal: check the current post-H3, post-author-front-matter manuscript as an
editor-ready book proof before the publisher-style/export pass.

## Current proof artifact

- Raw DOCX export:
  `docs/publisher/artifacts/agent-arch-ru-editorial-ready-2026-06-28.docx`
- Source Google Doc revision:
  `ALtnJHxghK0ux39XZSQMkGfFh_TqFc9QasJFxuerN_vYLBxxWKS036rEaQmQRW9mCVrBIR2uNFtXgg1EbDTdIopzLmiVbROaOd-e0Vj1GTQ`

## Structural result

The current proof is structurally stable after the author/front matter pass:

- paragraphs: 8040;
- non-empty paragraphs: 6028;
- rough words: 97703;
- style inventory unchanged from the H3-normalized proof:
  - `normal`: 5567;
  - `Heading 1`: 27;
  - `Heading 2`: 1758;
  - `Heading 3`: 637;
  - `Heading 4`: 51;
- non-empty heading counts:
  - `Heading 1`: 26;
  - `Heading 2`: 764;
  - `Heading 3`: 513;
  - `Heading 4`: 51;
- long non-empty `Heading 2` over 220 chars: 0;
- long non-empty `Heading 3` over 220 chars: 0.

Paragraph count is unchanged versus the previous H3-normalized proof. The only
content-level delta is the expanded author-owned/front-matter checklist under
`Об авторе`.

## Editorial checks

Automated editorial scan:

- `[заполнить` markers: 5, all in the intentionally author-owned front matter;
- bracketed placeholder-like spans: 114, mostly technical notation and
  intentional template language, with author-owned fields tracked separately;
- `TODO`: 0;
- `FIXME`: 0;
- `Что делать дальше`: 9;
- `Что проверить`: 7;
- `online companion`: 27.

The repeated `Что делать дальше` and `Что проверить` blocks are not formatting
defects, but they remain the main line-edit risk for the external editor: in
some chapters they work as practical closing rhythm; in others they may read as
documentation residue.

## Editor-facing verdict

The manuscript is ready for controlled external editorial review as a working
book manuscript:

- the full book volume is present;
- the 7-part / 23-chapter structure is stable;
- H1/H2/H3 body-style pollution is closed for the current proof;
- front matter clearly marks the author-owned fields;
- companion boundary is explicit;
- raw DOCX and Template2000n proof routes exist.

It is not yet a final publisher submission. Remaining blockers:

- author-owned factual fields;
- final author/publisher decisions on title, subtitle and cover copy;
- public companion URL and release version;
- legal/compliance and AI tooling disclosure wording;
- final publisher style application and render QA;
- external proofread after the export shape is stable.

## Recommended editorial route

1. Start with front matter, chapter 1 and chapter 23 to validate the book
   promise and final payoff.
2. Then review chapters 20-21 as the highest late-book density risk.
3. Review one technical evidence chapter, preferably chapter 13 or 15.
4. Review repeated chapter endings and decide which ones should be tightened.
5. Verify glossary and companion references after the author-owned fields are
   filled.

## Next work

Proceed to publisher-style pass: build a fresh Template2000n derivative from
the updated raw proof, render raw and Template2000n outputs, and record the new
page counts.
