# Google Doc editorial readiness pass: 2026-06-21

Status: applied editorial-readiness pass for the full Russian Google Doc
manuscript.

Working Google Doc:

- `Архитектура безопасных ИИ-агентов — полная рукопись`
- <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>
- tab: `t.0`

Repository branch:

- `codex/ru-reference-package-inspect-terms-20260608`

## 1. Purpose

This pass continued the previous front matter and navigation cleanup. The goal
was not to add bulk volume, but to make the manuscript more book-ready before
the future DOCX/template phase.

The five implemented work items were:

1. front matter pass for title, annotation, author block, foreword and reading
   guidance;
2. navigation pass for `Карта книги`;
3. chapter 11 technical-density pass;
4. code/YAML reading policy pass;
5. DOCX-readiness report and export QA.

## 2. Google Doc edits

### Front matter

Additional paragraph boundaries were inserted in the opening material so that
the title note, annotation and reader guidance do not collapse into adjacent
headings during export.

The pass specifically cleaned transitions around:

- `Аннотация`;
- `Рукопись соединяет...`;
- `Практический результат...`;
- `Шаблоны...`;
- `Как читать эту книгу`;
- `Как устроена логика книги`;
- `Три маршрута чтения`.

### Navigation

The `Карта книги` section was kept as a reader-facing map, not a build note. The
visible scaffold marker in the heading `- Карта архитектурных решений` was
removed. One wording in the map was normalized from `проектное ревью` to
`архитектурное review`, keeping the editorial voice consistent with the rest of
the manuscript.

### Chapter 11

`Глава 11. Песочница выполнения и MCP как интеграционный контракт` now starts
with a short reader frame:

- `Как читать эту главу`

The frame states that the chapter is a print architecture chapter, not a full
MCP manual. It directs long schemas, CLI output and error catalogs to the
online companion while preserving the print chapter's focus on runtime
boundaries, host/client/server responsibility and evidence after execution.

### Code and YAML

The front matter now contains a reader-facing section:

- `Как читать листинги и YAML`

This section explains that listings, YAML and trace fragments in the printed
book should be read as architecture artifacts: contract shape, important fields,
responsibility boundary and evidence. Full executable detail belongs in the
online companion unless it is necessary to understand the risk or verification
model in the chapter.

## 3. DOCX-readiness implications

The current Google Doc should remain a semantic manuscript, not a final styled
Word file. This pass improves the future DOCX stage because:

1. front matter has cleaner paragraph boundaries for export;
2. the navigation block has an explicit role;
3. chapter 11 has a print/companion boundary at the point of reading;
4. listing semantics are described for readers and future style mapping;
5. code-like blocks have a policy that can map cleanly to
   `VBACodeHead` / `VBACodeText` in the publisher template bridge.

Next DOCX-oriented work should not run the `.dot` macros automatically. Use
`docs/publisher/ru-template2000n-style-bridge.md` as the mapping guide and
apply styles only after a clean Google Docs export.

## 4. Remaining editorial work

Open items after this pass:

1. decide whether `Карта книги` remains in print as a reading guide or becomes
   a shorter generated table of contents;
2. audit chapter 11 for individual long blocks that can move to companion;
3. audit late runtime/package material for listing captions and truncation;
4. run a full front matter visual QA beyond spot checks;
5. run final cross-reference and terminology pass before external delivery.

## 5. Verification

Completed in the final QA step of this pass:

- exported the current Google Doc to PDF:
  `/private/tmp/agent_arch_editorial_readiness_20260621_final.pdf`;
- confirmed PDF metadata with `pdfinfo`:
  - page count: `707`;
  - page size: `612 x 792 pts`;
  - producer: `Skia/PDF m151 Google Docs Renderer`;
- checked extracted late-section markers with `pypdf`:
  - `runtime_skeleton_contract`: page `551`;
  - `capability_release_contract`: page `575`;
  - `rollout_decision_record`: pages `600`, `612`;
- rendered and visually inspected spot pages:
  - page `2`: annotation starts as a separate front matter section;
  - page `18`: `Как читать листинги и YAML` starts as a separate section;
  - page `19`: following `Границы ответственности` section remains separated;
  - page `37`: `Карта книги` and `Карта архитектурных решений` render without
    the scaffold dash;
  - page `260`: chapter 11 starts with one clean `Как читать эту главу` frame,
    without the duplicate phrase from the first export attempt.

Limitations:

- this was a targeted spot-check export QA, not a full visual inspection of all
  `707` pages;
- `pypdf` did not reliably extract the Cyrillic marker strings from the Google
  Docs PDF, so Cyrillic checks were verified visually from rendered pages.
