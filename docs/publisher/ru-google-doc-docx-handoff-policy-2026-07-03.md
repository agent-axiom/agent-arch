# Google Doc and DOCX handoff policy

Date: 2026-07-03.

Status: active policy for the current editorial cycle.

## Source roles

Repository:

- semantic source of truth;
- stores Markdown manuscript sources, publisher maps, source records, QA reports
  and reproducible handoff state;
- receives backports for every semantic change accepted in Google Docs.

Google Doc:

- working editorial manuscript;
- used for editor comments, author review and Google Docs DOCX export;
- may contain front matter placeholders until author-owned facts are filled.

Raw DOCX export:

- dated export artifact from the current Google Doc;
- used as the text baseline for proof generation and integrity comparison;
- not edited manually as the semantic source.

Template2000n DOCX derivative:

- dated publisher-style proof candidate;
- generated from the raw DOCX export and style package;
- used for style/layout acceptance and editorial proof review;
- regenerated after author-owned fields or accepted semantic edits change the
  Google Doc.

## Change flow

1. Semantic content change starts in repository Markdown or is explicitly
   captured from Google Doc comments.
2. Accepted semantic change is reflected in Google Doc.
3. Repository control files record the change and status.
4. Raw DOCX is exported from Google Doc.
5. Template2000n derivative is rebuilt.
6. Render QA and text-integrity checks are run.
7. The new artifact pair becomes the current proof candidate only after the
   report is committed.

## What not to do

- Do not treat a manually edited DOCX as the source of truth.
- Do not call a Google Doc export final if author-owned facts are still blank.
- Do not run or require legacy template macros unless the publisher explicitly
  asks for that route.
- Do not accept style-only proof artifacts as semantic changes without
  backporting the accepted text.
- Do not send the clean editor packet as final publisher submission while the
  author fill packet remains open.

## Current artifact pair

- Raw DOCX:
  `docs/publisher/artifacts/agent-arch-ru-publisher-style-raw-2026-07-03.docx`
- Template2000n DOCX:
  `docs/publisher/artifacts/agent-arch-ru-template2000n-official-style-pass-2026-07-03.docx`
- QA report:
  `docs/publisher/ru-google-doc-template2000n-official-style-pass-2026-07-03.md`

Current page counts:

- raw: 489 pages;
- Template2000n official-style: 357 pages;
- blank-like pages: 0 in both render checks.
