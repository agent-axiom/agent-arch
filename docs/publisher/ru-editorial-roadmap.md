# Редакционная дорожная карта русской рукописи

Status: high-level roadmap after full first compression/editorial pass.

Google Doc target:

- `Архитектура безопасных ИИ-агентов`
- <https://docs.google.com/document/d/1LyY2Psy2yaobn7VLmOwLTWm4QVrhp2I-ylE2B7V4pp4>

## Current verdict

На 2026-06-14 Google Doc уже содержит договорную рукопись целиком: введение,
7 частей, 23 главы и приложения. Первый compression/editorial pass завершен по
всей рукописи.

Это не финальная издательская сдача. Следующий этап - не дописывание объема, а
доведение рукописи до редакционно устойчивого состояния: отделить рабочие
материалы, проверить сквозную дугу книги, закрепить терминологию, сверить
внутренние ссылки и подготовить front matter.

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

## Recommended execution order

1. Separate working material from the manuscript body.
2. Run structural editorial pass by parts.
3. Run terminology and glossary pass.
4. Run cross-reference and companion-boundary pass.
5. Fill author/front matter dependencies.
6. Apply publisher styles and perform export QA.
