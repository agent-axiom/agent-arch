# RU mindset shift pass

Date: 2026-07-05.

Status: synced to the existing working Google Doc and recorded as the current
reader-facing proof pair. This is still not the final publisher submission:
author-owned fields, public companion metadata, external proofread and final
publisher acceptance remain open.

Google Doc:

- <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI/edit>

Final known Google Doc revision:

- `ALtnJHxrm9Lz5_KVTxgVu1rd4I8eRo4ogBBZeZ86-vzl9YMxYGtRZQOjb-_hrGWKrSYh9_GWLhF8aE1LeXRTHMipWROizAGGFNOdCD7XaqE`

## Implemented changes

1. Added `Как изменится ваше мышление после книги` after the skeptic framing
   block in the introduction.
2. Added seven `До этой части / После этой части` blocks, one per main part.
   Each block names the reader's expected shift before entering the part's
   chapters.
3. Added 23 `Смена мышления` lines inside chapter takeaway blocks, after
   `Что ответить скептику` and before `Почему главу стоит переслать`.
4. Checked the new layer against existing takeaway, quote, skeptic-response,
   forwarding-hook and next-action layers. No high-similarity repeats were
   found by the local heuristic check.
5. Rebuilt the Template2000n derivative and uploaded the updated raw DOCX back
   to the same Google Doc.
6. Verified Google Doc readback for the new labels:
   `Как изменится ваше мышление после книги`,
   `До этой части / После этой части` and `Смена мышления:`.

## Structural QA

Required marker counts in Markdown, raw DOCX and Template2000n DOCX:

- `Как изменится ваше мышление после книги`: 1;
- `До этой части / После этой части`: 7;
- `Смена мышления:`: 23;
- `С кем спорит эта книга`: 1;
- `Типичное возражение`: 7;
- `Что ответить скептику:`: 23;
- `Сквозной производственный кейс`: 1;
- `Эпизод сквозного кейса`: 7;
- `Фраза для пересказа:`: 23;
- `Сквозная дуга книги`: 1;
- `Командная сессия части`: 7;
- `Что сделать после чтения:`: 23;
- `Три оптики этой части`: 7;
- `Почему главу стоит переслать:`: 23;
- `Что унести из главы`: 23.

Current manuscript structure:

- main parts: 7;
- chapters: 23;
- raw DOCX paragraphs: 8652;
- raw DOCX non-empty paragraphs: 6550;
- Template2000n paragraphs: 8652;
- Template2000n non-empty paragraphs: 6550;
- raw/styled paragraph text equality: preserved;
- exact Markdown duplicate paragraph groups with 35+ words: 0;
- raw DOCX paragraphs with 250+ words: 0;
- visible Cyrillic words with Latin `s` suffix: 0;
- DOCX archive integrity: raw and Template2000n files are valid zip archives.

## Proof metrics

Raw Google Doc DOCX:

- `docs/publisher/artifacts/agent-arch-ru-google-doc-dedup-source-sync-2026-07-05.docx`
- rendered pages: 528;
- blank-like pages: 0;
- render contact sheet:
  `/tmp/agent_arch_ru_google_doc_mindset_shift_2026_07_05_render/contact-sheet.png`.

Template2000n derivative:

- `docs/publisher/artifacts/agent-arch-ru-template2000n-dedup-source-sync-2026-07-05.docx`
- rendered pages: 382;
- blank-like pages: 0;
- body paragraphs mapped to `Body Text`: 5335;
- render contact sheet:
  `/tmp/agent_arch_ru_template2000n_mindset_shift_2026_07_05_render/contact-sheet.png`.

Text and volume:

- builder approximate words: 107312;
- local Markdown word-token count: 116676;
- raw/styled text equality: true.

Machine-readable QA:

- `docs/publisher/ru-google-doc-dedup-source-sync-2026-07-05.render-qa.json`
- `docs/publisher/ru-template2000n-dedup-source-sync-2026-07-05.render-qa.json`
- `docs/publisher/ru-template2000n-dedup-source-sync-2026-07-05.metrics.json`

## Editorial effect

This pass gives the manuscript an explicit reader-transformation layer. The
book now tells the reader not only what to know, but how their judgment should
change: from model quality to allowed action, from API call to capability, from
logs to evidence, from demo to accountable launch.

The added material is deliberately short. It should make the book easier to
recommend because a reader can describe the shift after each part and chapter
without summarizing the whole technical argument.

## Remaining author-owned fields

The author still needs to fill or explicitly omit:

- public author name and byline;
- short author bio for the book;
- longer author bio for publisher metadata;
- role, public positioning and professional affiliation wording;
- verified experience claims that can be printed;
- public project links;
- public companion URL and versioning policy;
- acknowledgements;
- legal/compliance disclaimer wording;
- AI-use disclosure if required by the publisher;
- final publisher metadata and cover copy.
