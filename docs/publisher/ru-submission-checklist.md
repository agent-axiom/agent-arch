# Чеклист готовности русской версии к издательству

Status: working gate for Russian publisher submission.

## Verdict scale

- **Ready:** можно отправлять редактору как издательский пакет.
- **Almost ready:** можно показывать доверенному редактору/агенту как предварительный пакет.
- **Not ready:** не отправлять как готовую рукопись; сначала закрыть блокеры.

Current status: **Structurally assembled, but volume-incomplete. Do not send as
a trusted editor review package yet. Google Doc contains the 7-part / 23-chapter
structure and a compressed editorial assembly, but it must be expanded from the
Markdown source corpus into full manuscript volume before external review.
Remaining blockers are manuscript expansion, author fields, publisher styles,
DOCX/export QA after styles and final external proofread.**

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
- [x] Есть верхнеуровневая редакционная дорожная карта:
      `docs/publisher/ru-editorial-roadmap.md`.
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
- [x] Google Doc contains the full 7-part / 23-chapter structure including
      appendices.
- [ ] Google Doc contains full manuscript volume expanded from the Markdown
      source corpus, not only compressed chapter assembly.
- [x] Introduction and Part I first compression/editorial pass completed in
      local assembly and synced to Google Doc.
- [x] Part II and Part III first compression/editorial pass completed in local
      assembly and synced to Google Doc.
- [x] Part IV and Part V first compression/editorial pass completed in local
      assembly and synced to Google Doc.
- [x] Part VI and Part VII first compression/editorial pass completed in local
      assembly and synced to Google Doc.
- [x] Appendices first compression/editorial pass completed in local assembly
      and synced to Google Doc.
- [x] Текущая web-структура 8/27 сжата в договорную структуру 7/23.
- [x] Book/reference split is explicit: runtime/schema details moved or marked as companion-only in the manuscript.
- [x] High-level roadmap for structural, terminology, cross-reference and
      companion-boundary passes is created.
- [x] Introduction and Part I structural pass completed and synced to Google
      Doc.
- [x] Part II and Part III structural pass completed and synced to Google Doc.
- [x] Part IV and Part V structural pass completed and synced to Google Doc.
- [x] Part VI, Part VII and appendices structural pass completed and synced to
      Google Doc.
- [x] First terminology/glossary anchor batch completed for Part VI, Part VII
      and appendices.
- [x] Second terminology anchor batch completed for Introduction and Parts I-V.
- [ ] Author bio / credential framing fields are filled by the author.
- [x] Стилевые файлы БХВ получены и применены или явно отложены.

## P1 gates before serious editor review

- [x] Working/publisher service blocks are separated from manuscript body for
      final delivery.
- [x] Structural editorial pass is complete across all parts.
- [x] `case-spine note` and `canonical cases` are removed from Russian reader-facing prose or turned into Russian reader-facing labels.
- [x] Russian headings avoid unnecessary English terms.
- [x] `tools`, `agents`, `rollout`, `runtime`, `review`, `registry`, `inventory`, `assurance`, `retirement`, and `end-of-life` follow the terminology policy.
- [x] Repeated maturity-check endings are intentionally templated rather than accidentally repetitive.
- [x] Dense CLI/runtime details are moved to online companion or summarized.
- [x] All Mermaid diagrams have print-safe fallback prose or captions.
- [x] Long tables and code blocks are reviewed for PDF/print readability.
- [x] Public companion links are stable.

## P2 gates before final manuscript delivery

- [ ] Full Russian proofread completed after manuscript expansion.
- [x] Cross-references checked after print assembly.
- [x] Glossary matches the terminology policy.
- [x] Bibliography/source catalog is curated for book use rather than web completeness.
- [x] Figure captions are complete for current manuscript scope.
- [x] Code examples have consistent formatting and line length for current manuscript scope.
- [ ] БХВ style package is applied to the final export shape.
- [ ] DOCX/export QA is completed after publisher style application.
- [ ] Independent external proofread is completed after the export shape is stable.
- [x] Final `mkdocs build --strict` passes.
- [x] Final docs surface tests pass.
- [x] `git diff --check` is clean.

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
9. Status note: public web manuscript exists; publisher manuscript is assembled
   from it in Google Doc and remains blocked only by author fields, publisher
   styles, export QA and final external proofread.

Before sending:

- do not use the external cover note until the author fields are filled;
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
