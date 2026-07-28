# Google Doc front matter and navigation pass: 2026-06-21

Status: structural cleanup pass applied to the full Russian Google Doc manuscript.

Working Google Doc:

- `Архитектура безопасных ИИ-агентов — полная рукопись`
- <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>
- tab: `t.0`

Repository branch:

- `codex/ru-reference-package-inspect-terms-20260608`

## 1. Purpose

The previous stabilization pass proved that the manuscript had book-scale
volume and that the late technical chapters exported correctly after bullet
cleanup. This pass addressed the next structural risks:

1. front matter heading/body text was visually and textually merged in several
   places;
2. the early navigation block looked like possible assembly scaffolding rather
   than an intentional map for the reader;
3. the main-body part and chapter titles needed stable Google Docs heading
   styles for outline/export behavior;
4. code/YAML material needed a clear print-production policy before the future
   DOCX/template pass.

## 2. Google Doc changes

Direct Google Docs edits were applied with connector readback and revision
guards.

### Front matter paragraph breaks

The following merged heading/body transitions were normalized by adding explicit
paragraph breaks:

- `Что получит читатель`;
- `Ключевые слова`;
- `Короткая версия`;
- `Факты для заполнения перед публикацией`;
- `Предисловие к русской версии`;
- `Почему эта версия нужна сейчас`;
- `Как устроена русская редакция`;
- `Что считать хорошим результатом чтения`;
- `Как читать примеры и шаблоны`;
- `Границы ответственности`;
- `Как читать эту книгу`;
- `Как устроена логика книги`;
- `Три маршрута чтения`.

The intent is not final typography. The intent is to preserve a clean logical
boundary between headings and body text before the publisher style pass.

### Navigation block

The repeated part/chapter overview before the main body is now explicitly
introduced as:

- `Карта книги`

This makes the block a deliberate reader-facing navigation section instead of
ambiguous build scaffolding.

### Main-body heading hierarchy

The main body was normalized as:

- parts I-VII: `HEADING_1`;
- chapters 1-23: `HEADING_2`.

Only the body occurrences were targeted. Repeated strings in front matter,
cross-references and appendices were not intentionally promoted to chapter
headings. `Глава 20` required special handling because the exact heading appears
several times before the actual body chapter; the body occurrence is the one
after chapter 19 and before part VII.

## 3. Code and YAML policy for the print manuscript

The current Google Doc should preserve logical listing boundaries, not final
Word styling. The future DOCX pass should map those boundaries to the
publisher-template family described in
`docs/publisher/ru-template2000n-style-bridge.md`:

- listing title or label: `VBACodeHead` / `InsertListingHeader`;
- code body: `VBACodeText`;
- code symbols or UI terms where needed: `VBACodeSymb`, `ScreenTerm`,
  `ScreenTermEng`;
- explanatory body text: `BodyText`;
- tables around listings: `TableHead`, `TableText`, `TableHeadCol`.

Print-book rules for technical examples:

1. Every listing must have a local reason to exist: it should demonstrate a
   decision, contract, boundary, or verification step from the surrounding
   chapter.
2. Long YAML/JSON/Python blocks should be shortened for print when the omitted
   detail is mechanical. The full version belongs in the online companion.
3. A listing should be preceded by context and followed by interpretation. The
   reader should know what to inspect and why it matters.
4. Listing names should be stable enough to cross-reference from prose,
   checklists and appendices.
5. Code-like material must not be converted into Google Docs bullet lists.
   Accidental bullets change both visual rhythm and semantic intent.
6. Runtime contracts, policy examples and rollout records should keep field
   names stable. Russian prose may explain them, but the fields themselves stay
   in the language of the executable artifact.

This keeps the Google Doc useful for writing and review while leaving final
formatting to the DOCX/template phase.

## 4. Remaining publisher-production work

This pass does not finish the book. It reduces structural risk before the next
editorial/content passes.

Open items:

1. full visual QA of all front-matter pages beyond the spot-checked pages;
2. final decision on whether the `Карта книги` section should stay in print or
   become a generated table of contents / reading guide;
3. chapter 11 companion-boundary review, because protocol/runtime detail is
   still dense for a print chapter;
4. code/YAML style application after DOCX export and publisher-template mapping;
5. final cross-reference and terminology pass before external handoff.

## 5. Verification

Fresh checks from this pass:

- Google Doc connector identity:
  - document id: `1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI`;
  - title: `Архитектура безопасных ИИ-агентов — полная рукопись`;
  - tab: `t.0`.
- Latest exported PDF:
  - local QA file:
    `/private/tmp/agent_arch_frontmatter_navigation_20260621.pdf`;
  - `pdfinfo` page count: 705;
  - Google Docs PDF renderer: `Skia/PDF m151 Google Docs Renderer`.
- Marker checks:
  - `runtime_skeleton_contract`: page 549;
  - `capability_release_contract`: page 573;
  - `rollout_decision_record`: pages 598 and 610.
- Visual spot checks:
  - page 3: `Что получит читатель` renders as a separate heading;
  - page 4: numbered reader outcomes and `Ключевые слова` render as separate
    blocks;
  - page 36: `Карта книги` renders as a separate heading before the navigation
    section;
  - page 48: main body start renders with separate part and chapter headings;
  - page 535: late body start renders with separate part VII and chapter 21
    headings.

Limitations:

- full rendered visual QA of all 705 pages was not performed;
- PDF text extraction did not reliably find Cyrillic front-matter labels, so
  front-matter verification used page raster inspection instead;
- the existing heading `- Карта архитектурных решений` still contains a leading
  dash in the navigation section and should be cleaned in a later editorial
  pass if the section stays in print.
