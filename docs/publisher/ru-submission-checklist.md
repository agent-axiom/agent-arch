# Чеклист готовности русской версии к издательству

Status: working gate for Russian publisher submission.

## Verdict scale

- **Ready:** можно отправлять редактору как издательский пакет.
- **Almost ready:** можно показывать доверенному редактору/агенту как предварительный пакет.
- **Not ready:** не отправлять как готовую рукопись; сначала закрыть блокеры.

Current status: **Not ready as a final publisher submission; strong enough for internal editorial packaging.**

## P0 gates before external submission

- [ ] Целевая подача выбрана: Russian publisher package, English publisher package, or dual-track package.
- [ ] Для Russian package sample manifest указывает RU source paths, not `.en.md` paths.
- [ ] Есть отдельная assembly map for print manuscript.
- [ ] Терминологическая политика применена к sample chapters.
- [ ] Chapter 1 passed Russian line edit.
- [ ] Chapter 13 passed Russian line edit.
- [ ] Part VIII compression plan is applied or explicitly deferred with a waiver.
- [ ] Book/reference split is explicit: runtime/schema details moved or marked as companion-only.
- [ ] Author bio / credential framing is provided by the author.
- [ ] Target editor/imprint formatting requirements are known or explicitly waived.

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
2. Proposed print table of contents.
3. Chapter 1 sample.
4. Chapter 13 sample if the editor asks for technical depth.
5. Companion-site description.
6. Author bio and platform note.
7. Status note: public web manuscript exists; publisher manuscript is being assembled from it.

Do not include:

- full schema appendices;
- full CLI reference;
- generated site files;
- internal editorial backlog;
- raw source catalog unless requested.
