# Mechanical placeholder and link scan report

Date: 2026-06-29.

Scope: local manuscript repository scan for Russian book, appendix, companion
and publisher-facing control files. Binary DOCX artifacts under
`docs/publisher/artifacts/**` were excluded from the classification pass. The
old untracked export `docs/publisher/artifacts/agent-arch-ru-google-doc-2026-06-26.txt`
was observed in the working tree but was not included in this report.

This pass is a mechanical readiness check. It does not replace live source
verification or visual proof QA.

## Commands run

```bash
rg -n --ignore-case -e 'TODO|FIXME|TBD|XXX' docs/book docs/appendix docs/companion
```

Result: no matches.

```bash
rg -n -e '\[заполнить\]|\[fill\]' \
  docs/book docs/appendix docs/companion \
  docs/publisher/ru-manuscript-full.md \
  docs/publisher/ru-author-query-packet-2026-06-28.md \
  docs/publisher/ru-author-open-fields-2026-06-28.md \
  docs/publisher/ru-publisher-packet-v0.1.md
```

Result: intentional author-owned placeholders only:

- `docs/publisher/ru-manuscript-full.md`: public projects and links;
- `docs/publisher/ru-author-query-packet-2026-06-28.md`: two author answer
  slots;
- `docs/publisher/ru-publisher-packet-v0.1.md`: publisher packet author-name
  placeholder and surrounding instructions;
- `docs/publisher/ru-author-open-fields-2026-06-28.md`: checklist item to
  remove final placeholders after author input.

```bash
rg -n --glob '!docs/publisher/artifacts/**' \
  -e '1LyY2Psy2yaobn7VLmOwLTWm4QVrhp2I-ylE2B7V4pp4|compressed/staging snapshot|Compressed/staging snapshot' \
  docs/book docs/appendix docs/companion docs/publisher
```

Result: the old 71-page Google Doc appears only in historical workflow,
assembly, map and packet files as the compressed/staging snapshot. The current
full manuscript source remains:

<https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>

```bash
rg -n --glob '!docs/publisher/artifacts/**' \
  -e 'Следующая плановая проверка|Последняя редакционная проверка' \
  docs/book docs/appendix docs/companion docs/publisher
```

Result: review-date banners remain in selected chapters and in
`docs/publisher/ru-manuscript-full.md`. These are not placeholders, but they
should be updated or removed after live source verification.

## Classification

| Class | Status | Notes |
| --- | --- | --- |
| `TODO` / `FIXME` / `TBD` / `XXX` in book, appendix, companion | Clear | No matches in the focused scan. |
| Author-owned placeholders | Intentional blocker | Must be filled by the author, not generated automatically. |
| Old compressed Google Doc link | Historical only | Allowed in workflow/map/evolution files; must not be used as the editor handoff source. |
| Review-date banners | Needs final policy | Keep only if the publisher wants visible freshness notes; otherwise remove from print-facing chapters after source verification. |
| Companion `skeleton` labels | Release hygiene | Acceptable in changelog/errata staging files, but should be revised before a public companion v1.0 tag. |
| External web links | Pending live verification | Local scan found references; live freshness/status verification remains separate. |

## Blocking items before publisher submission

1. Author must fill or explicitly omit all author-owned fields:
   `Об авторе`, public name, role, verified experience, public projects,
   public links, acknowledgements and publisher-facing author line.
2. Run live source verification for cited official/vendor/security/research
   sources and update `docs/publisher/ru-source-verification-records-2026-06-28.md`.
3. Decide review-date policy for print-facing chapters: update dates after
   verification or remove freshness banners from the publisher proof.
4. Re-run final DOCX export and render QA after author-owned fields are filled.
5. Confirm the external packet points only to the full Google Doc and fresh
   DOCX proofs, not to the compressed/staging snapshot.

## Outcome

The mechanical scan did not find accidental TODO/FIXME debt in the book,
appendix or companion content. The remaining issues are known handoff blockers:
author-owned factual fields, live source verification, final proof export and
publisher packet assembly.
