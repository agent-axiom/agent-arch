# RU case thesis pass

Date: 2026-07-05.

Status: completed and synced to the current Google Doc.

Google Doc:

- <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI/edit>

Final known Google Doc revision:

- `ALtnJHyYapbkiUC6iu1GxFan0C6cwyoMIHWVI320Wi1XqXC0-S6pZYCU543zoWAUmarcQdnT2TyRrpBWXhpeyd74AxV5wI19jHeRRlqYp9U`

## Goal

Make the Russian manuscript more memorable and recommendable by adding an
explicit recurring production case and short chapter theses that readers can
quote or send to colleagues.

## Implemented changes

1. Added `Сквозной производственный кейс` to the introduction. The support
   agent is now named as the main recurring case that carries the book from
   demo to governed launch.
2. Added seven `Эпизод сквозного кейса` blocks, one per main part. Each episode
   shows how the same support-agent system changes after the part's engineering
   layer is added.
3. Added 23 `Фраза для пересказа` lines inside chapter takeaway blocks. These
   lines are deliberately short, quotable and technically aligned with the
   chapter.
4. Rebuilt the Template2000n derivative from the updated raw DOCX and preserved
   raw/styled paragraph text equality.
5. Uploaded the updated raw DOCX back to the same Google Doc ID.
6. Recorded 100 controlled editorial micro-iterations in
   `docs/publisher/ru-editorial-100-case-thesis-iterations-2026-07-05.md`.

## Proof metrics

Raw Google Doc DOCX:

- `docs/publisher/artifacts/agent-arch-ru-google-doc-dedup-source-sync-2026-07-05.docx`
- rendered pages: 522
- blank-like pages: 0
- paragraphs: 8558
- non-empty paragraphs: 6456
- approximate words: 105808

Template2000n derivative:

- `docs/publisher/artifacts/agent-arch-ru-template2000n-dedup-source-sync-2026-07-05.docx`
- rendered pages: 379
- blank-like pages: 0
- raw/styled paragraph text equality: preserved
- body paragraphs mapped to `Body Text`: 5243
- SHA-256: `0b92d75dad3188c36d217008affe3268f4951463479939d3dd627238cd117bbe`

Local Markdown source record:

- current word-token count: 114574
- chapters 1-23 in order
- seven main part headings and seven short-structure part entries

## Verification summary

- Google Doc readback found `Сквозной производственный кейс`.
- Google Doc readback found `Эпизод сквозного кейса`.
- Google Doc readback found `Фраза для пересказа:`.
- Local Markdown, raw DOCX and Template2000n DOCX have 1 through-case block,
  7 case episodes and 23 quotable chapter theses.
- Exact duplicate paragraph groups with 35+ words: 0 in raw and Template2000n
  DOCX.
- Paragraphs with 250+ words: 0 in raw and Template2000n DOCX.
- Visible mixed Cyrillic + `s` suffix hits in Markdown: 0.
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
as the current publisher-style proof candidate after this case/thesis pass.
