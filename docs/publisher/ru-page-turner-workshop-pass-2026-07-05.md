# RU page-turner workshop pass

Date: 2026-07-05.

Status: completed and synced to the current Google Doc.

Google Doc:

- <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI/edit>

Final known Google Doc revision:

- `ALtnJHzDDo0-WoZ_Tzj_JPnk4GkxKpxtZZ6XGYVPp1qNx9jNzOmJzeQxUxlLtAi29eTJYnQ1MHIyHouDx9ufBBlUXzBnOZ-DY3bgnQXPlXc`

## Goal

Make the Russian manuscript easier to keep reading, discuss with a team and
recommend to colleagues by adding a stronger story arc and more explicit
chapter-to-action handoff.

## Implemented changes

1. Added the introduction block `Сквозная дуга книги`: the manuscript now reads
   as one engineering story from a useful demo to an organization-ready system
   of governed actions.
2. Added seven part-level `Командная сессия части` blocks, one after each main
   part profile. Each block defines the workshop format, expected artifact,
   success signal and red flag.
3. Added 23 `Что сделать после чтения` actions after the chapter forwarding
   hooks, so every chapter ends with a concrete team or architecture step.
4. Rebuilt the Template2000n derivative from the updated raw DOCX and preserved
   raw/styled paragraph text equality.
5. Uploaded the updated raw DOCX back to the same Google Doc ID.
6. Recorded 100 controlled editorial micro-iterations in
   `docs/publisher/ru-editorial-100-page-turner-workshop-iterations-2026-07-05.md`.

## Proof metrics

Raw Google Doc DOCX:

- `docs/publisher/artifacts/agent-arch-ru-google-doc-dedup-source-sync-2026-07-05.docx`
- rendered pages: 519
- blank-like pages: 0
- paragraphs: 8518
- non-empty paragraphs: 6416
- approximate words: 105103

Template2000n derivative:

- `docs/publisher/artifacts/agent-arch-ru-template2000n-dedup-source-sync-2026-07-05.docx`
- rendered pages: 377
- blank-like pages: 0
- raw/styled paragraph text equality: preserved
- body paragraphs mapped to `Body Text`: 5204
- SHA-256: `2344d84dc605c9f632f3b3bd447468b8746fd4fab5f86cc000d043fa530639a0`

Local Markdown source record:

- current word-token count: 113868
- chapters 1-23 in order
- seven main part headings and seven short-structure part entries

## Verification summary

- Google Doc readback found `Сквозная дуга книги`.
- Google Doc readback found `Командная сессия части`.
- Google Doc readback found `Что сделать после чтения:`.
- Local Markdown, raw DOCX and Template2000n DOCX have 1 through-line block,
  7 part workshop blocks and 23 chapter next-action blocks.
- Exact duplicate paragraph groups with 35+ words: 0 in raw and Template2000n
  DOCX.
- Paragraphs with 250+ words: 0 in raw and Template2000n DOCX.
- Visible mixed Cyrillic + `s` suffix hits in Markdown: 0.
- Render QA found 0 blank-like pages in both current proof files.
- `uv run --group docs mkdocs build --strict` passed.

## Author-owned fields still required

The author still needs to fill or explicitly omit:

- public author name and byline;
- short author bio;
- long author bio for publisher metadata;
- public role, affiliation and positioning wording;
- verified experience claims;
- public project links;
- public companion URL and versioning policy;
- acknowledgements;
- legal/compliance disclaimer wording;
- AI-use disclosure if required by the publisher;
- final publisher metadata and cover copy.

## Current decision

Use the current Google Doc as the living manuscript and
`docs/publisher/artifacts/agent-arch-ru-template2000n-dedup-source-sync-2026-07-05.docx`
as the current publisher-style proof candidate after this page-turner/workshop
pass.
