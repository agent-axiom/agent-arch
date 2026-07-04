# Google Doc visual/edit pass

Date: 2026-07-05.

Status: completed as the current publisher-prep checkpoint. This is still not
the final publisher submission because author-owned fields, public companion
metadata, external proofread and publisher acceptance of the style route remain
open.

Google Doc:

- <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>

Final known Google Doc revision for this pass:

- `ALtnJHxx8GXfQQfPMrGfG7STCXtscwWkhPzWpj1AJa-vee0UADj3vnwYNiZkKG2wGfd2Xkdsizblmxq8xb8YyumfJxKOb8ujAWDn1wNGphY`

## Implemented plan

1. Checked the current manuscript against the repository source and the latest
   Google Doc state.
2. Fixed high-level logical and structural issues: outdated chapter references,
   repeated heading resets, duplicate long reference-package blocks and
   companion-boundary wording.
3. Added a visual layer: 12 Russian-language diagrams with captions and alt
   descriptions. In the Markdown source they are placed at the relevant chapter
   points; in the Google Doc they are also available as a final
   editor-facing visualization block for layout placement.
4. Compressed long CLI/API/reference excerpts in the print manuscript and moved
   detailed command/API material to a companion file.
5. Rechecked excessive anglicisms and mixed-language leftovers. Plain-prose
   replacements were applied where they were safe; stable technical terms,
   identifiers, paths and architecture terms such as `runtime`, `trace`,
   `rollout`, `sandbox`, `MCP`, `verifier`, `capability` remain intentional.
6. Saved a fresh authenticated raw DOCX export from the updated Google Doc.
7. Rebuilt the Template2000n derivative from that fresh raw DOCX baseline and
   preserved text equality.
8. Rendered both DOCX artifacts to page PNGs, checked page counts, blank-like
   pages, DOCX archive integrity, embedded images and low-density pages.

## Google Doc changes

Direct Google Doc edits applied in this pass:

- guarded cross-reference cleanup:
  `Глава 18. Чеклист промышленного запуска` ->
  `Глава 23. Чеклист промышленного запуска`;
- guarded architecture-title cleanup:
  `Глава 2. Референсная архитектура безопасного агента` ->
  `Глава 3. Референсная архитектура безопасной агентной системы`;
- Russian terminology cleanup around rollout/production/owner/review/payload/
  dataset wording where the term was not required as a stable engineering name;
- targeted repairs after the terminology batch, including broken inflections
  such as `набор оценкиs`, `проверочный списокs` and
  `до промышленный поэтапный выпуск`;
- final compression of the long `memory.yaml` paragraph so that no paragraph in
  the exported DOCX is 250+ words;
- insertion of the `Визуализации для редакции` block with 12 embedded PNG
  figures, captions and alt text.

## Repository manuscript changes

Updated:

- `docs/publisher/ru-manuscript-full.md`;
- `docs/publisher/ru-companion-cli-api-reference-2026-07-05.md`;
- `docs/publisher/visuals/`.

The print manuscript now keeps short architectural explanations for CLI/API
examples and points the reader to the companion route for full command
transcripts, validation messages, trace/event catalogs, payload details and
runtime reference material.

## Visualizations

Added 12 PNG figures:

1. Book map.
2. Agent trust boundaries.
3. Safe agent reference architecture.
4. Capability contract path.
5. Memory and retrieval.
6. Approval gateway.
7. Sandbox and MCP boundary.
8. Idempotency and recovery.
9. Evidence chain.
10. ADLC lifecycle.
11. Assurance, incident registry and retirement loop.
12. Launch readiness.

DOCX media check:

- raw Google Doc export: 12 embedded `word/media/*.png` files, total `657713`
  bytes;
- Template2000n derivative: 12 embedded `word/media/*.png` files, total
  `657713` bytes.

## DOCX artifacts

Fresh raw Google Docs export:

- `docs/publisher/artifacts/agent-arch-ru-google-doc-visual-edit-2026-07-05.docx`
- bytes: `1273901`
- SHA-256:
  `90e32536e1befa07bfa2882f3d3d71f040ab39e5550e09f83aad1407f3092761`
- paragraphs: `8245`
- non-empty paragraphs: `6139`
- approximate words: `100045`

Template2000n derivative from that raw export:

- `docs/publisher/artifacts/agent-arch-ru-template2000n-visual-edit-2026-07-05.docx`
- bytes: `1281054`
- SHA-256:
  `49cf319e43e15191fbebcb69fb87dca402d7aa4b81b21c1438d5308aee99d813`
- paragraphs: `8245`
- non-empty paragraphs: `6139`
- approximate words: `100045`
- no-style body paragraphs mapped to `Body Text`: `4983`
- raw/styled paragraph text equality: preserved

The attached legacy `Template2000n.dot` was converted to DOCX with headless
LibreOffice using an isolated temporary user profile. No Template2000n macros
were executed.

## QA checks

DOCX archive integrity:

- raw Google Doc export: `unzip -t` passed;
- Template2000n derivative: `unzip -t` passed.

Long paragraph scan:

- raw Google Doc export: `0` paragraphs with 250+ words;
- Template2000n derivative: `0` paragraphs with 250+ words.

Known broken markers absent in the repository source:

- old Chapter 18 launch-checklist reference;
- old Chapter 2 reference-architecture reference;
- `раскат` / `выклад` prose leftovers;
- `набор оценкиs`;
- `проверочный списокs`;
- `до промышленный поэтапный выпуск`.

## Render QA

Raw Google Docs export:

- pages: `501`;
- blank-like pages: `0`;
- contact sheet:
  `/tmp/agent_arch_ru_google_doc_visual_edit_2026_07_05_final_render/contact-sheet.png`;
- visual spot-check: first page, low-density pages and final figure page render
  correctly.

Template2000n derivative:

- pages: `366`;
- blank-like pages: `0`;
- contact sheet:
  `/tmp/agent_arch_ru_template2000n_visual_edit_2026_07_05_final_render/contact-sheet.png`;
- visual spot-check: opening matter and final visualization pages render
  correctly.

Machine-readable QA:

- `docs/publisher/ru-google-doc-visual-edit-pass-2026-07-05.render-qa.json`
- `docs/publisher/ru-template2000n-visual-edit-2026-07-05.metrics.json`

## Remaining author-owned fields

The author still needs to fill or explicitly omit:

- public author name/byline;
- short and long author bio;
- role/public positioning;
- verified experience claims;
- public project links;
- public online-support URL, versioning, changelog and errata route;
- acknowledgements;
- legal/compliance disclaimer wording if publisher requires it;
- AI-use disclosure wording if publisher requires it;
- final title, subtitle, cover copy and imprint metadata.

## Decision

The current Google Doc is no longer only a compressed editorial assembly. It is
an expanded working manuscript with the current visual layer, fresh DOCX export
and Template2000n proof. The best current publisher-facing proof artifact is
the Template2000n visual/edit DOCX on `366` rendered pages. Final submission
still requires author-owned facts, external proofread and publisher/editor
acceptance of the final style route.
