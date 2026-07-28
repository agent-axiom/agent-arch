# Final placeholder and link scan workflow

Date: 2026-06-28.

Status: ready for the final pre-submission QA pass.

## Purpose

Before publisher submission, the manuscript needs a mechanical scan for
unintended placeholders, stale internal notes and broken or unstable links.
This workflow separates author-owned placeholders from defects.

## Placeholder classes

Allowed until author fills data:

- author bio fields;
- public author links;
- title/subtitle/cover copy;
- companion URL/version/errata/changelog;
- legal/compliance disclaimer;
- AI tooling disclosure;
- acknowledgements;
- publisher metadata.

Not allowed in final submission:

- accidental `[заполнить]` in reader-facing prose;
- TODO/FIXME comments;
- stale `skeleton` labels in release companion routes;
- expired internal review notes in print flow;
- placeholder URLs in publisher-facing files;
- old compressed-manuscript links presented as the main manuscript.

## Scan commands

Run from repository root:

```bash
rg -n "TODO|FIXME|\\[заполнить\\]|\\[fill\\]|placeholder|skeleton|not finalized" docs/book docs/appendix docs/companion docs/publisher
rg -n "Следующая плановая проверка|Последняя редакционная проверка" docs/book docs/appendix
rg -n "1LyY2Psy2yaobn7VLmOwLTWm4QVrhp2I-ylE2B7V4pp4" docs/publisher docs/companion docs/book docs/appendix
```

Interpretation:

- hits in author-owned packets are allowed until author data is supplied;
- hits in reader-facing manuscript or final external packet require a decision;
- `skeleton` is allowed only in historical reports, not in release-candidate
  companion routes;
- stale review-date notes should not appear in final print flow.

## Link scan

Run:

```bash
uv run --group docs mkdocs build --strict
```

Then review source verification records for external links that need live
checking. `mkdocs build --strict` is not enough for temporal accuracy: it can
catch build/link issues, but it cannot prove that a platform claim is current.

## Google Doc scan

After author fields are filled and final comments are resolved:

1. Export raw DOCX.
2. Extract text or inspect via the document connector.
3. Search for `[заполнить]`, `TODO`, `FIXME`, `placeholder`, stale review
   notes and old compressed-document links.
4. Rebuild Template2000n proof only after the raw export is clean.

## Completion criteria

The final scan is complete when:

- all unexpected placeholder hits are removed or documented;
- author-owned placeholders are either filled or explicitly deferred;
- source verification records exist for fast-changing external claims;
- strict docs build passes;
- raw and Template2000n proof exports pass render QA after author fields.
