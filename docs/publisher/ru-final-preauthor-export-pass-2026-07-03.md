# Final pre-author export pass

Date: 2026-07-03.

Status: completed as a pre-author export pass. This is not final publisher
submission because author-owned facts and publisher/editor style-route
acceptance are still open.

## Implemented plan

1. Checked the current Google Doc front matter through connector readback.
2. Confirmed that the `Об авторе` block still contains author-owned
   placeholders and must not be filled by Codex.
3. Exported a fresh raw DOCX from the current Google Doc.
4. Rebuilt a fresh Template2000n derivative using the macro-free style route.
5. Repeated DOCX archive integrity checks and render QA for both DOCX outputs.
6. Prepared the pre-author publisher packet state and next-goal ledger.

## Google Doc state

- Google Doc:
  <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>
- Connector revision:
  `ALtnJHwG2y0y6xdziVEBWf1jHm7r6i_bkXLaj0f_p_1raU2fzYu7XbniNYm86oBYvk_aFiwhUgAkAa8LnjW7E-hl6iMi5fJR-77zzvllovI`
- Connector modified time:
  `2026-07-02T22:46:03.373Z`

Observed author-owned placeholders include:

- `[Имя автора / публичное имя]`;
- `[текущая роль, специализация или независимое позиционирование]`;
- `[заполнить]`;
- companion URL/version/errata placeholders;
- legal/compliance disclaimer and AI tooling disclosure placeholders;
- title/subtitle/cover-copy/imprint metadata placeholders.

## Artifacts

Raw Google Docs export:

- `docs/publisher/artifacts/agent-arch-ru-final-preauthor-raw-2026-07-03.docx`
- SHA-256:
  `1e7654ba0dbfa195b691ef2f1c9f8394cbf3463d18061b0c829b30b2ba696b30`
- paragraphs: `8179`
- non-empty paragraphs: `6105`
- approximate words: `99587`

Template2000n pre-author derivative:

- `docs/publisher/artifacts/agent-arch-ru-template2000n-final-preauthor-2026-07-03.docx`
- SHA-256:
  `bcaf2fb7bff6d4290528987da0159f9d3d81b6aa477f3d4f7b8f86bfeba5a564`
- paragraphs: `8179`
- non-empty paragraphs: `6105`
- approximate words: `99587`

Machine-readable QA:

- `docs/publisher/ru-final-preauthor-export-pass-2026-07-03.render-qa.json`

## Render QA

Raw Google Docs export:

- pages: `489`
- PNG pages: `489`
- blank-like pages: `0`
- contact sheet:
  `/tmp/agent-arch-ru-final-preauthor-raw-contact-2026-07-03.png`

Template2000n pre-author derivative:

- pages: `361`
- PNG pages: `361`
- blank-like pages: `0`
- contact sheet:
  `/tmp/agent-arch-ru-template2000n-final-preauthor-contact-2026-07-03.png`

Both contact sheets were visually spot-checked: first page, lowest-density
pages and final page were not blank and did not show obvious clipping or
overlap on the sampled pages.

## Integrity

- Raw DOCX archive integrity: passed.
- Template2000n DOCX archive integrity: passed.
- Raw/styled paragraph count equality: preserved.
- Raw/styled paragraph text equality: preserved.

## Style note

The fresh export remains a pre-final proof. It is suitable for editorial review
and for publisher style-route discussion, but not for final publisher
submission. Final delivery still requires:

- author-owned fields filled or explicitly omitted;
- publisher/editor acceptance of the macro-free Template2000n route or a
  replacement route;
- independent proofread after final export shape is stable;
- a new post-author raw export, Template2000n rebuild and render QA pass.
