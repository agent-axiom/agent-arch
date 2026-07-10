# Russian Google Doc frontier enrichment pass - 2026-07-10

Target manuscript: https://docs.google.com/document/d/1LyY2Psy2yaobn7VLmOwLTWm4QVrhp2I-ylE2B7V4pp4/edit?tab=t.0

Final checked Google Docs revision:
`ALtnJHyCpvRXsXX7HqnEAIzYcl5LAnB1VsO35l5JM2Eukg5iumy2lkWyfcbp2RtFyxBbE_CgeIAe3gKo7mGH6ABwD__02StWHNiSky36iTA`

## Source harvest

The pass selectively harvested recent `origin/main` material without merging the branch, because the local publisher branch also contains manuscript and visual assets that would be removed by a direct merge.

Primary source commits inspected:

- `95fad607` - Document agent containment patterns
- `6f1a00eb` - Add agent architecture frontier updates
- `753a7f89` - Polish frontier update integration
- `a0b239de` - Align managed agent split coverage
- `7631be84` - Add eval integrity audit contract

Main source areas reviewed:

- chapters 3, 4, 9, 11, 12, 13, 16, 17, and 18
- appendices for eval schema, trace schema, reference package, research frontier, and case studies
- `skills/safe-agent-architecture` references

## Google Doc updates

Added ten editorial blocks under the shared label `Практическое дополнение 2026`:

1. `Safe Agent Architecture Brief`
2. `сдерживание сильнее бесконечного надзора`
3. `политика выбирает не только возможность, но и hands`
4. `tool descriptions, prompt-to-tool-to-execution и аудит сдерживания`
5. `MCP gateway, private reachability и browser как поверхность действия`
6. `reasoning privacy и searchable spans`
7. `стоимость и песочница тоже входят в SLO`
8. `deployment simulation и целостность самой оценки`
9. `framework, harness и runtime - разные слои`
10. `launch gate должен проверять не только happy path`

Added five new inline figures to the Google Doc:

- `Рисунок 3.x. Localhost не является trust boundary`
- `Рисунок 9.2. MCP gateway и progressive disclosure`
- `Рисунок V.1. Поток записи оценки и аудита`
- `Рисунок 16.2. Framework / Harness / Runtime как три разных слоя`
- `Рисунок 16.3. Durable workflow spine и recoverable internal fiber`

Google Docs inline object IDs returned by the insert pass:

- `kix.2f91qsvbwzwy` - localhost control-plane figure
- `kix.z31m0h6ntnms` - MCP gateway figure
- `kix.depdthfurg4p` - eval integrity figure
- `kix.rdt1wowgnoxp` - runtime stack figure
- `kix.3u9iz1rhnvw4` - durable workflow figure

## Local visual assets

New figure sources:

- `docs/publisher/visuals/ru-figure-18-runtime-stack.svg`
- `docs/publisher/visuals/ru-figure-19-localhost-control-plane.svg`
- `docs/publisher/visuals/ru-figure-20-eval-integrity.svg`
- `docs/publisher/visuals/ru-figure-21-mcp-gateway.svg`
- `docs/publisher/visuals/ru-figure-22-durable-workflow-fiber.svg`

Generated PNG exports:

- `docs/publisher/visuals/ru-figure-18-runtime-stack.png`
- `docs/publisher/visuals/ru-figure-19-localhost-control-plane.png`
- `docs/publisher/visuals/ru-figure-20-eval-integrity.png`
- `docs/publisher/visuals/ru-figure-21-mcp-gateway.png`
- `docs/publisher/visuals/ru-figure-22-durable-workflow-fiber.png`

All PNGs are 1600x900, 8-bit sRGB.

## Verification

Google Doc export:

- exported final Google Doc to PDF
- PDF page count: 456 pages
- PDF producer: Google Docs Renderer
- generated low-resolution raster contact sheet for all 456 pages
- generated high-resolution contact sheet for color/figure pages: 23, 54, 65, 147, 208, 230, 346, 347, 349, and 395
- verified new figures are present, readable, and not clipped
- fixed inherited italic styling around the chapter 16 inserted block and re-exported the PDF

Text extraction checks from the final PDF:

- no `[[RU_FIGURE_*]]` markers remain
- `Практическое дополнение 2026` appears 10 times
- key frontier topics are present in extracted text: localhost/loopback, containment, MCP gateway, `eval_audit_record`, deployment simulation, reasoning privacy/searchable spans, framework/harness/runtime, durable workflow/recoverable internal fiber

Repository checks:

- `git diff --check`
- PNG identity check for the five new images
- `uv run --group docs mkdocs build --strict`

## Open author-owned fields

Before publisher submission, the author still needs to fill or approve:

- `Об авторе` block: public name, role, short experience line, public links, and confirmed facts
- any publisher-specific style requirements from the BHV template package
- final decision on whether English technical terms such as `runtime`, `harness`, `eval`, `gateway`, `sandbox`, `trace`, and `launch gate` should stay as terms of art or be partially localized in chapter-level copy editing

## Suggested next manuscript work

1. Run a chapter-by-chapter terminology pass for the newly added 2026 blocks.
2. Normalize figure numbering after the publisher template/style pass.
3. Convert several dense practical blocks into tables or checklists where the publisher layout permits it.
4. Add short "what to practice in the repo" callouts after the new runtime/eval/MCP blocks.
5. Do a final source/link pass so repeated GitHub URLs, appendix links, and figure references are consistent.
