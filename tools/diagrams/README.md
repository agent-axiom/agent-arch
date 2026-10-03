# Editable Book Diagrams

Excalidraw scenes in `docs/assets/diagrams/{ru,en,zh}/` are the editable sources.
SVG files beside them are the website exports. Open a `.excalidraw` file in the
Excalidraw editor to change its native shapes, labels or arrows. Do not replace
the scene with a screenshot.

## Export

From this directory, with Node.js 22 or newer and pnpm:

```sh
pnpm install --frozen-lockfile
pnpm exec playwright install chromium
pnpm test
node export.mjs ../../docs/assets/diagrams/ru/part-i-chapter-1-01.excalidraw
```

The exporter uses Excalidraw's own SVG API and fails on image-only scenes,
invalid geometry, duplicate IDs or broken arrow bindings. `CHROMIUM_PATH` can
select an already installed browser. Headless export is local; diagram contents
are not uploaded to the Excalidraw web service.

## Review

- Check labels, branch conditions, direction and the number of relationships.
- Keep colors supplementary: meaning must remain clear in grayscale.
- Use regular sans-serif text and light fills. Keep background opaque white.
- Check long labels, overlapping arrows and translations at readable size.
- Re-export each changed language and update the asset checksums in the manifest.
- Run `python -m pytest tests/test_book_diagrams.py` and `mkdocs build --strict`
  from the repository root after updating images and references.

The website shows the complete diagram within the reading column.
Clicking a diagram or its adjacent link opens its full-resolution SVG;
the adjacent source link downloads the editable scene. No Mermaid runtime or
third-party renderer is required when reading the book.
