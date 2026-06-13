# Чеклист готовности русской версии к издательству

Status: working gate for Russian publisher submission.

## Verdict scale

- **Ready:** можно отправлять редактору как издательский пакет.
- **Almost ready:** можно показывать доверенному редактору/агенту как предварительный пакет.
- **Not ready:** не отправлять как готовую рукопись; сначала закрыть блокеры.

Current status: **Not ready as a final publisher submission; strong enough for internal editorial packaging.**

## P0 gates before external submission

- [x] Целевая подача выбрана: Russian publisher package.
- [x] Рабочая Google Doc-рукопись создана и доступна для чтения/записи:
      <https://docs.google.com/document/d/1LyY2Psy2yaobn7VLmOwLTWm4QVrhp2I-ylE2B7V4pp4>.
- [x] Для Russian package sample manifest указывает RU source paths, not `.en.md` paths.
- [x] Есть отдельная assembly map for print manuscript:
      `docs/publisher/ru-manuscript-map.md`.
- [x] Есть source map от договорной структуры к Markdown-источникам:
      `docs/publisher/ru-source-map.md`.
- [x] Зафиксировано правило синхронизации repository -> Google Doc:
      `docs/publisher/ru-google-doc-workflow.md`.
- [x] Publisher-facing packet v0.1 drafted:
      `docs/publisher/ru-publisher-packet-v0.1.md`.
- [x] Publisher-facing packet v0.1 compact block synced to the Google Doc.
- [x] Chapter 1 working sample loaded into the Google Doc manuscript.
- [x] Chapter 1 first Russian publisher line edit applied and synced to the Google Doc.
- [x] Терминологическая политика применена к Chapter 1 and source Chapter 13 samples.
- [x] Chapter 1 passed first Russian line edit.
- [x] Source Chapter 13 passed first Russian line edit.
- [ ] Текущая web-структура 8/27 сжата в договорную структуру 7/23.
- [ ] Book/reference split is explicit: runtime/schema details moved or marked as companion-only in the manuscript.
- [ ] Author bio / credential framing is provided by the author.
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
4. Chapter 1 sample from `docs/book/part-i/chapter-1.md`.
5. Chapter 13 sample from `docs/book/part-v/chapter-13.md` if the editor asks for technical depth.
6. Companion-site description.
7. Author bio and platform note.
8. Status note: public web manuscript exists; publisher manuscript is being assembled from it.

Working packet source:

- `docs/publisher/ru-publisher-packet-v0.1.md`

Do not include:

- full schema appendices;
- full CLI reference;
- generated site files;
- internal editorial backlog;
- raw source catalog unless requested.
