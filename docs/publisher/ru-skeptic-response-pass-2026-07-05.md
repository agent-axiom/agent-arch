# RU skeptic response pass

Date: 2026-07-05.

Status: synced to the existing working Google Doc and recorded as the current
reader-facing proof pair. This is still not the final publisher submission:
author-owned fields, public companion metadata, external proofread and final
publisher acceptance remain open.

Google Doc:

- <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI/edit>

Final known Google Doc revision:

- `ALtnJHyKPoEL5XDwXyqfgL2sILc_-RIQ9xR63ygk_d-R7C8YnZawqrJCyP3_rwneb23SCZJhRxPPeCYvWaiyyaDlNYaxZVt95Y5PJZhwFTc`

## Implemented changes

1. Added `С кем спорит эта книга` after the recurring production case in the
   introduction. The block frames skeptical objections as useful engineering
   pressure, not as a strawman.
2. Added seven `Типичное возражение` blocks, one per main part. Each block
   states a plausible objection and answers it through ownership, policy,
   evidence, rollback or operational responsibility.
3. Added 23 `Что ответить скептику` lines inside chapter takeaway blocks, after
   `Фраза для пересказа` and before `Почему главу стоит переслать`.
4. Removed one local Markdown-only duplicate of the minimal sandbox profile
   from the appendix-level reference material. The current Google Doc proof did
   not contain that duplicate block, but the repository source record is now
   cleaner.
5. Rebuilt the Template2000n derivative from the current raw proof and uploaded
   the updated raw DOCX back to the same Google Doc.
6. Verified Google Doc readback for the new labels:
   `С кем спорит эта книга`, `Типичное возражение` and
   `Что ответить скептику:`.

## Structural QA

Required marker counts in Markdown, raw DOCX and Template2000n DOCX:

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
- raw DOCX paragraphs: 8605;
- raw DOCX non-empty paragraphs: 6503;
- Template2000n paragraphs: 8605;
- Template2000n non-empty paragraphs: 6503;
- raw/styled paragraph text equality: preserved;
- raw DOCX paragraphs with 250+ words: 0;
- visible Cyrillic words with Latin `s` suffix: 0;
- DOCX archive integrity: raw and Template2000n files are valid zip archives.

## Proof metrics

Raw Google Doc DOCX:

- `docs/publisher/artifacts/agent-arch-ru-google-doc-dedup-source-sync-2026-07-05.docx`
- rendered pages: 525;
- blank-like pages: 0;
- render contact sheet:
  `/tmp/agent_arch_ru_google_doc_skeptic_response_2026_07_05_render/contact-sheet.png`.

Template2000n derivative:

- `docs/publisher/artifacts/agent-arch-ru-template2000n-dedup-source-sync-2026-07-05.docx`
- rendered pages: 379;
- blank-like pages: 0;
- body paragraphs mapped to `Body Text`: 5289;
- render contact sheet:
  `/tmp/agent_arch_ru_template2000n_skeptic_response_2026_07_05_render/contact-sheet.png`.

Text and volume:

- builder approximate words: 106615;
- local Markdown word-token count: 115986;
- raw/styled text equality: true.

Machine-readable QA:

- `docs/publisher/ru-google-doc-dedup-source-sync-2026-07-05.render-qa.json`
- `docs/publisher/ru-template2000n-dedup-source-sync-2026-07-05.render-qa.json`
- `docs/publisher/ru-template2000n-dedup-source-sync-2026-07-05.metrics.json`

## Editorial effect

This pass strengthens the book for real discussions with skeptical engineers,
architects and managers. The manuscript now gives readers short, reusable
answers to objections such as:

- "we only need a quick model check";
- "roles and prompts are enough";
- "memory is just personalization";
- "tools are ordinary API calls";
- "traces and evals can wait";
- "each team can build its own agent stack";
- "a green demo is enough to launch".

The added material is intentionally short. It should help the reader defend the
book's architecture in meetings without turning chapters into polemics.

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
