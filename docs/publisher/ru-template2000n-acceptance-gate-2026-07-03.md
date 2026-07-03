# Template2000n acceptance gate

Date: 2026-07-03.

Status: ready for publisher/editor acceptance. This gate records what was
actually done with the attached `Template2000n.dot` and what must be confirmed
before the manuscript is called final publisher submission.

## Current proof candidate

Canonical working manuscript:

- Google Doc:
  <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>

Current proof artifacts:

- raw Google Docs DOCX export:
  `docs/publisher/artifacts/agent-arch-ru-publisher-style-raw-2026-07-03.docx`;
- Template2000n official-style derivative:
  `docs/publisher/artifacts/agent-arch-ru-template2000n-official-style-pass-2026-07-03.docx`;
- pass report:
  `docs/publisher/ru-google-doc-template2000n-official-style-pass-2026-07-03.md`;
- render QA metadata:
  `docs/publisher/ru-google-doc-template2000n-official-style-pass-2026-07-03.render-qa.json`.

## Applied style route

`Template2000n.dot` is a legacy Word 2000 binary template. The current pass uses
a conservative, macro-free route:

1. Convert the `.dot` file to a temporary DOCX style source.
2. Copy `styles.xml`, `theme1.xml` and `fontTable.xml` from the converted
   template.
3. Preserve the Google Docs export `numbering.xml` to avoid legacy list
   remapping.
4. Remove legacy heading numbering properties from `Heading1`-`Heading5`.
5. Map Google Docs body paragraphs from `Normal` to `BodyText`.
6. Do not execute VBA/macros.

## Evidence

Measured result:

- raw render: 489 pages, 0 blank-like pages;
- Template2000n official-style render: 357 pages, 0 blank-like pages;
- paragraph count: 8179 in both raw and styled proofs;
- non-empty paragraphs: 6105 in both raw and styled proofs;
- approximate words: 99587 in both raw and styled proofs;
- raw/styled paragraph text equality: preserved;
- DOCX archive integrity: passed for both files.

## Acceptance questions for publisher/editor

The publisher or editor should answer these before final delivery:

1. Is the macro-free conversion route acceptable for a legacy `.dot` template?
2. Should final delivery be a styled DOCX derivative or a Google Docs export
   plus style instructions?
3. Must template macros be run by the publisher inside their own Word
   environment, or should they remain unused?
4. Are heading styles, body text style and list preservation acceptable for
   copyediting?
5. Are page count and line density acceptable for the next editorial cycle?
6. Does the publisher require any additional style names, front matter blocks,
   metadata fields or proof marks before copyedit?

## Decision state

Current decision:

- the Template2000n styled DOCX is the current publisher-style proof candidate;
- it is suitable for editorial style acceptance review;
- it is not final publisher submission until author-owned fields, human
  proofread, publisher/editor acceptance and a final post-author export pass are
  closed.
