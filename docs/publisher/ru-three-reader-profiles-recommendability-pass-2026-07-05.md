# RU three reader profiles recommendability pass

Date: 2026-07-05.

Status: completed and synced to the current Google Doc.

Google Doc:

- <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI/edit>

Final known Google Doc revision:

- `ALtnJHyZy1LMv4XzR_qTR0FPFlSJ4unAgE-dDg43jHDi7XQoDGg0pXZh6Yx8pPMYboRV2KnwARZezcDLxlbWlO8ccbxfz1FKybyFJZ2Zu7k`

## Goal

Make the Russian manuscript more recommendable by giving three primary reader
profiles a clear reason to keep reading, apply the material and send specific
chapters to colleagues.

## Implemented changes

1. Added a technical lead / architect route to the introduction.
2. Added an engineering manager / CTO route to the introduction.
3. Added a practicing developer route to the introduction.
4. Added a short team-handoff block explaining how to use chapters in
   architecture, leadership and engineering discussions.
5. Added seven part-level profile outcome blocks: architect, manager and
   developer outcomes for each major part.
6. Added 23 chapter forwarding hooks after the existing chapter takeaways.
7. Restored the short book-structure section after moving profile blocks to the
   real part headings.
8. Added the missing Part V Heading 1 in the raw DOCX proof before Chapter 13.
9. Recorded 100 controlled editorial micro-iterations in
   `docs/publisher/ru-editorial-100-three-reader-profiles-iterations-2026-07-05.md`.

## Proof metrics

Raw Google Doc DOCX:

- `docs/publisher/artifacts/agent-arch-ru-google-doc-dedup-source-sync-2026-07-05.docx`
- rendered pages: 516
- blank-like pages: 0
- paragraphs: 8457
- non-empty paragraphs: 6355
- builder approximate words: 104217
- structural word-token count: 105370
- embedded images: 12

Template2000n derivative:

- `docs/publisher/artifacts/agent-arch-ru-template2000n-dedup-source-sync-2026-07-05.docx`
- rendered pages: 375
- blank-like pages: 0
- raw/styled paragraph text equality: preserved
- body paragraphs mapped to `Body Text`: 5144
- SHA-256: `86dd873f42f29066a94fd07c5004fe7d05295cf1dc5f7bf79b6d7e35eebadbe1`

Machine-readable QA:

- `docs/publisher/ru-google-doc-dedup-source-sync-2026-07-05.render-qa.json`
- `docs/publisher/ru-template2000n-dedup-source-sync-2026-07-05.render-qa.json`
- `docs/publisher/ru-template2000n-dedup-source-sync-2026-07-05.metrics.json`

## Verification summary

- Google Doc readback found the architect route phrase.
- Google Doc readback found the manager / CTO route phrase.
- Google Doc readback found the developer route phrase.
- Local Markdown has chapters 1-23 in order.
- Local Markdown has seven short-structure parts and seven main part headings.
- Raw DOCX and Template2000n DOCX have seven Heading 1 part headings.
- Raw DOCX and Template2000n DOCX have 1 three-profile route block, 1 team
  handoff block, 7 part profile blocks and 23 chapter forwarding hooks.
- Raw/styled paragraph text equality is preserved.
- Exact duplicate paragraph groups with 35+ words: 0.
- Paragraphs with 250+ words: 0.
- Render QA found 0 blank-like pages in both current proof files.

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
as the current publisher-style proof candidate after this three-reader-profiles
recommendability pass.
