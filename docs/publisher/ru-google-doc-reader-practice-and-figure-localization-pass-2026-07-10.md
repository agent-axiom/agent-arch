# RU Google Doc reader practice and figure localization pass - 2026-07-10

Target Google Doc: https://docs.google.com/document/d/1LyY2Psy2yaobn7VLmOwLTWm4QVrhp2I-ylE2B7V4pp4/edit

Final checked Google Doc revision:
`ALtnJHyI5sQTWaJ5l564NQw2V5m_CpUK0eCQH92naVVGfqGZT7Q6-Vg6Nw1QHySqsLxxaYV1Pbg0yJ7C8_Of1sO5aY-C1RvsZOvGJRnDWoo`

Final exported PDF for QA:
`/tmp/agent-arch-google-doc-reader-practice-final2-2026-07-10.pdf`

## Implemented in the Google Doc

- Added seven practical exercises at the actual major-part boundaries of the manuscript:
  - part I: page 50
  - part II: page 103
  - part III: page 133
  - part IV: page 177
  - part V: page 246
  - part VI: page 343
  - part VII: page 419
- Normalized raw GitHub URLs for the reference implementation into readable labels such as `GitHub: agent_runtime_ref/...`.
- Added companion-material framing for long command and file matrices, so the printed manuscript reads as an explanation first and a reference package second.
- Rechecked the document after cleanup to remove the accidental false `Практическое упражнение части VIII` insertion.

## Implemented in the repository

Localized the source SVG and regenerated PNG assets for the following figures:

- `docs/publisher/visuals/ru-figure-18-runtime-stack.svg`
- `docs/publisher/visuals/ru-figure-19-localhost-control-plane.svg`
- `docs/publisher/visuals/ru-figure-20-eval-integrity.svg`
- `docs/publisher/visuals/ru-figure-21-mcp-gateway.svg`
- `docs/publisher/visuals/ru-figure-22-durable-workflow-fiber.svg`

The figures now use Russian labels for the main conceptual blocks while keeping canonical technical terms where replacing them would reduce precision.

## QA evidence

- Google Docs export produced a 462-page PDF.
- Extracted text contains seven practical exercises and no false part VIII exercise.
- Extracted text contains no raw `github.com/agent-axiom/agent-arch` URLs after link normalization.
- Raster QA was performed with `pdftoppm` on all 462 pages at low resolution and on all exercise pages at higher resolution.
- Exercise-page contact sheet showed the exercises placed cleanly before the next major part or appendix.

## Known limitation

The Google Docs connector route updated the manuscript text directly, but did not complete in-place replacement of already inserted images. Google Docs `replaceImage` requires a publicly fetchable image URI; the connector-side local image sidecar supports inline image insertion, not replacement of an existing image object. A temporary Drive-uploaded image was therefore not usable for direct replacement without public image access.

The localized image assets are committed in the repository and should be applied to the Google Doc in the next layout pass, either through a public-asset image replacement route or through a DOCX/import pass.

## Author/editor follow-up

- Fill the `Об авторе` placeholders with final author biography, credentials, contacts, and preferred presentation.
- Decide whether the manuscript should explicitly materialize an eighth body part or whether front-matter claims should be normalized to the current seven major body parts plus appendices.
- Apply the official publisher template in the final DOCX/layout pass.
- Run a human line edit for rhythm, repeated explanations, and remaining optional English technical terms.
