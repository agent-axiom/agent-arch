# Редакционная дорожная карта русской рукописи

Status: execution roadmap after structural, terminology, cross-reference,
companion-boundary and current-source print-readability passes.

Google Doc target:

- `Архитектура безопасных ИИ-агентов`
- <https://docs.google.com/document/d/1LyY2Psy2yaobn7VLmOwLTWm4QVrhp2I-ylE2B7V4pp4>

## Current verdict

На 2026-06-15 Google Doc уже содержит договорную рукопись целиком: введение,
7 частей, 23 главы и приложения. Structural, terminology, cross-reference,
companion-boundary and current-source print-readability passes завершены.

Это почти готовая рукопись для доверенного редакторского чтения, но не финальная
издательская сдача. Остаются внешние зависимости: авторские поля, стилевые файлы
БХВ, DOCX/export QA после применения стилей и финальная внешняя вычитка.

## Workstream 1. Разделить рукопись и рабочие материалы

Задача: сделать очевидным, что служебные блоки в начале Google Doc не являются
текстом книги.

Что сделать:

- явно пометить служебные блоки как `не включать в финальную сдачу`;
- добавить заметный раздел `Начало основного текста книги` перед введением;
- решить, нужен ли отдельный Google Doc для publisher packet, cover note and
  editorial roadmap.

Definition of done:

- редактор видит, где начинается книга;
- служебные блоки не могут случайно попасть в финальный DOCX;
- repository -> Google Doc sync rule остается явным.

Progress:

- 2026-06-15: Google Doc contains `Начало основного текста книги`; working
  blocks are treated as service/front-matter material and excluded from final
  delivery unless explicitly promoted.

## Workstream 2. Structural editorial pass

Задача: проверить книгу как цельную аргументационную дугу, а не набор
синхронизированных глав.

Что проверить:

- каждая часть отвечает на отдельный крупный вопрос;
- переходы между частями объясняют, почему следующий слой нужен именно сейчас;
- сквозной кейс поддержки не исчезает и не становится декоративным;
- повторяющиеся объяснения runtime, policy, memory, tools, evals and rollout
  не перегружают читателя;
- финальная часть действительно приводит к launch decision, а не обрывается на
  reference implementation.

Definition of done:

- у каждой части есть сильный вводный тезис и понятный выход;
- главы читаются последовательно, но сохраняют практическую автономность;
- нет крупных провалов между архитектурой, эксплуатацией и организационной
  моделью.

Progress:

- 2026-06-14: Introduction and Part I completed as the first structural batch.
- 2026-06-14: Parts II-III completed as the second structural batch.
- 2026-06-14: Parts IV-V completed as the third structural batch.
- 2026-06-14: Parts VI-VII and appendices completed; first full structural
  pass across the manuscript is complete.

## Workstream 3. Terminology pass

Задача: закрепить единый русский словарь для повторяющихся технических
понятий.

Ключевые группы:

- agent, tool, capability, gateway;
- runtime, run, trace, span, event;
- policy, approval, principal, tenant;
- rollout, gate, registry, inventory;
- assurance, incident, retirement, end-of-life;
- eval, verifier, rubric, evidence chain.

Definition of done:

- glossary matches manuscript vocabulary;
- first occurrence of a key English term has a Russian explanation;
- headings avoid English unless the term is essential for industry lookup;
- terms are consistent across introduction, chapters and appendices.

Progress:

- 2026-06-14: first terminology/glossary anchor batch completed for
  `capability`, `principal`, `tenant`, `lifecycle`, `inventory`,
  `assurance loop`, `runtime`, `registry` and `retirement` in Part VI,
  Part VII and appendices.
- 2026-06-15: second terminology anchor batch completed for reader-facing
  `runtime`, `workflow`, `policy layer`, `tool gateway`, `capability model`,
  `rollout`, `trace` and `evidence chain` anchors in Introduction and
  Parts I-V.
- 2026-06-15: third terminology consistency batch completed for reader-facing
  ADLC, assurance, registry, retirement, reference runtime, launch checklist
  and appendix checklist/postmortem language in Parts VI-VII and appendices.

## Workstream 4. Cross-reference and continuity pass

Задача: проверить внутренние связи после сжатия web-структуры 8/27 в печатную
структуру 7/23.

Что проверить:

- ссылки на предыдущие и будущие главы;
- promises made in introduction;
- references to companion material;
- consistency of chapter numbers and part numbers;
- whether Chapter 13 as follow-up technical sample is still described correctly
  after full manuscript assembly.

Progress:

- 2026-06-15: reader-facing `case-spine note` and `canonical cases` labels were
  checked across the assembled manuscript sources; no stale service labels remain.
- 2026-06-15: stale web-structure references were checked across assembled
  manuscript sources; no reader-facing references to Part VIII or chapters
  24-27 remain, and the 7/23 structure is stable.

Definition of done:

- no stale web-structure references remain in reader-facing prose;
- companion references are deliberate and useful;
- chapter and part numbering are stable.

## Workstream 5. Book/companion boundary pass

Задача: убедиться, что печатная книга не превращается в справочник API, но и не
теряет практическую глубину.

Что проверить:

- long schemas, YAML, CLI walkthroughs and registry operations stay in companion;
- print manuscript keeps enough examples to be operationally useful;
- appendices are short working aids, not a duplicate online reference package;
- source catalog is curated for book use rather than web completeness.

Definition of done:

- each heavy technical artifact has an explicit home: book summary or companion;
- reader can understand the design without opening companion immediately;
- companion remains useful as executable/reference layer.

Progress:

- 2026-06-15: companion boundary checked across assembled manuscript sources;
  YAML, CLI walkthroughs, reference outputs, registry operations and long
  schemas are consistently assigned to the online companion.
- 2026-06-15: current manuscript-source print-readability scan found no
  Mermaid blocks, Markdown tables or fenced code blocks in the assembled
  publisher manuscript sources.

## Workstream 6. Publisher front matter and final delivery prep

Задача: подготовить рукопись к внешнему редакторскому циклу.

Что сделать:

- fill author bio and credential framing fields;
- update cover note only after manuscript-only structure is stable;
- apply БХВ styles when received;
- run DOCX/export QA after style application;
- only then prepare external package.

Definition of done:

- author placeholders are gone;
- Google Doc or exported DOCX has publisher-ready structure;
- final checks include proofread, cross-reference review, glossary match,
  `git diff --check`, `uv run pytest`, and `uv run mkdocs build --strict`.

Progress:

- 2026-06-15: author fields remain intentionally open for the author; БХВ style
  files are explicitly deferred until received.
- 2026-06-15: current-source proofread, cross-reference, glossary, source
  catalog, figure/code and print-readability gates are complete for the
  assembled manuscript. DOCX/export QA remains blocked until styles are applied.

## Recommended execution order

1. Separate working material from the manuscript body.
2. Run structural editorial pass by parts.
3. Run terminology and glossary pass.
4. Run cross-reference and companion-boundary pass.
5. Fill author/front matter dependencies.
6. Apply publisher styles and perform export QA.
