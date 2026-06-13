# Чеклист готовности русской версии к издательству

Status: working gate for Russian publisher submission.

## Verdict scale

- **Ready:** можно отправлять редактору как издательский пакет.
- **Almost ready:** можно показывать доверенному редактору/агенту как предварительный пакет.
- **Not ready:** не отправлять как готовую рукопись; сначала закрыть блокеры.

Current status: **Not ready as a final publisher submission; Google Doc now
contains Introduction, Parts I-VII and appendices, with the first
compression/editorial pass applied to Introduction and Part I. The remaining
body still needs compression, line editing, cross-reference review and publisher
formatting.**

## P0 gates before external submission

- [x] Целевая подача выбрана: Russian publisher package.
- [x] Рабочая Google Doc-рукопись создана и доступна для чтения/записи:
      <https://docs.google.com/document/d/1LyY2Psy2yaobn7VLmOwLTWm4QVrhp2I-ylE2B7V4pp4>.
- [x] Для Russian package sample manifest указывает RU source paths, not `.en.md` paths.
- [x] Есть отдельная assembly map for print manuscript:
      `docs/publisher/ru-manuscript-map.md`.
- [x] Есть source map от договорной структуры к Markdown-источникам:
      `docs/publisher/ru-source-map.md`.
- [x] Есть ledger эволюции рукописи:
      `docs/publisher/ru-manuscript-evolution.md`.
- [x] Зафиксировано правило синхронизации repository -> Google Doc:
      `docs/publisher/ru-google-doc-workflow.md`.
- [x] Publisher-facing packet v0.1 drafted:
      `docs/publisher/ru-publisher-packet-v0.1.md`.
- [x] Publisher-facing packet v0.1 compact block synced to the Google Doc.
- [x] Author/platform note template with fill-in fields added to packet v0.1.
- [x] Author/platform note compact template synced to the Google Doc.
- [x] Default first-packet sample scope fixed as Chapter 1 only.
- [x] Chapter 13 fixed as follow-up technical sample by request.
- [x] Russian cover note draft created:
      `docs/publisher/ru-cover-note-draft.md`.
- [x] Chapter 1 working sample loaded into the Google Doc manuscript.
- [x] Chapter 1 first Russian publisher line edit applied and synced to the Google Doc.
- [x] Терминологическая политика применена к Chapter 1 and source Chapter 13 samples.
- [x] Chapter 1 passed first Russian line edit.
- [x] Source Chapter 13 passed first Russian line edit.
- [x] Introduction and Part I rough assembly source created:
      `docs/publisher/ru-manuscript-assembly-part-i.md`.
- [x] Introduction and Part I rough assembly synced to the Google Doc.
- [x] Part II and Part III rough assembly source created:
      `docs/publisher/ru-manuscript-assembly-part-ii-iii.md`.
- [x] Part II and Part III rough assembly completed in Google Doc.
- [x] Part IV and Part V rough assembly source created:
      `docs/publisher/ru-manuscript-assembly-part-iv-v.md`.
- [x] Part IV and Part V rough assembly completed in Google Doc.
- [x] Part VI and Part VII rough assembly source created:
      `docs/publisher/ru-manuscript-assembly-part-vi-vii.md`.
- [x] Part VI and Part VII rough assembly completed in Google Doc.
- [x] Appendices rough assembly source created:
      `docs/publisher/ru-manuscript-assembly-appendices.md`.
- [x] Appendices rough assembly completed in Google Doc.
- [x] Google Doc contains the full manuscript body including appendices, not only
      skeleton plus chapter rough assembly.
- [x] Introduction and Part I first compression/editorial pass completed in
      local assembly and synced to Google Doc.
- [ ] Текущая web-структура 8/27 сжата в договорную структуру 7/23.
- [ ] Book/reference split is explicit: runtime/schema details moved or marked as companion-only in the manuscript.
- [ ] Author bio / credential framing fields are filled by the author.
- [ ] Стилевые файлы БХВ получены и применены или явно отложены.

## P1 gates before serious editor review

- [ ] `case-spine note` and `canonical cases` are removed from Russian reader-facing prose or turned into Russian reader-facing labels.
- [ ] Russian headings avoid unnecessary English terms.
- [ ] `tools`, `agents`, `rollout`, `runtime`, `review`, `registry`, `inventory`, `assurance`, `retirement`, and `end-of-life` follow the terminology policy.
- [ ] Repeated maturity-check endings are intentionally templated rather than accidentally repetitive.
- [ ] Dense CLI/runtime details are moved to online companion or summarized.
- [ ] All Mermaid diagrams have print-safe fallback prose or captions.
- [ ] Long tables and code blocks are reviewed for PDF/print readability.
- [ ] Public companion links are stable.

## P2 gates before final manuscript delivery

- [ ] Full Russian proofread completed.
- [ ] Cross-references checked after print assembly.
- [ ] Glossary matches the terminology policy.
- [ ] Bibliography/source catalog is curated for book use rather than web completeness.
- [ ] Figure captions are complete.
- [ ] Code examples have consistent formatting and line length.
- [ ] Final `mkdocs build --strict` passes.
- [ ] Final docs surface tests pass.
- [ ] `git diff --check` is clean.

## Recommended first external packet

Include:

1. One-page Russian positioning memo.
2. Договорная структура 7 частей / 23 главы.
3. Source map from repository Markdown to publisher manuscript chapters.
4. Cover note draft from `docs/publisher/ru-cover-note-draft.md`.
5. Chapter 1 sample from `docs/book/part-i/chapter-1.md`.
6. Chapter 13 sample from `docs/book/part-v/chapter-13.md` only if the editor asks for technical depth.
7. Companion-site description.
8. Author bio and platform note.
9. Status note: public web manuscript exists; publisher manuscript is being assembled from it.

Before sending:

- do not use the external cover note until the Google Doc shows manuscript volume;
- fill every `[заполнить]` field in `docs/publisher/ru-publisher-packet-v0.1.md`;
- replace the cover-note author placeholder with the final short author line;
- keep Chapter 13 out of the first packet unless the editor explicitly asks for technical depth;
- verify Google Doc access for the editor.

Working packet source:

- `docs/publisher/ru-publisher-packet-v0.1.md`
- `docs/publisher/ru-cover-note-draft.md`

Do not include:

- full schema appendices;
- full CLI reference;
- generated site files;
- internal editorial backlog;
- raw source catalog unless requested.
