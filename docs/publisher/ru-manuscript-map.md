# Карта русской издательской рукописи

Status: editorial assembly map. Основано на плане-проспекте к договору
авторского заказа N 4-5/26 от 15 мая 2026 года.

## Назначение

Публичная версия в репозитории остается широкой web-версией: 8 частей, 27 глав,
практические страницы, справочные приложения и исполняемый reference package.
Издательская рукопись собирается как отдельный слой: 7 частей, 23 главы,
введение и приложения. Google Doc используется как рабочая издательская
рукопись, но смысловые изменения должны возвращаться в Markdown.

Source map для сборки:

- `docs/publisher/ru-source-map.md`

Полная рабочая Google Doc-рукопись:

- <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>

Редакционная карта book-readiness pass:

- <https://docs.google.com/document/d/1XoU_nWZkpKGU7SxZ0pgmE_dfcNNggQokZsbzind7kXc>

Текущий editorial-ready proof:

- Google Doc export modified time:
  `2026-07-02T22:46:03.373Z`
- Raw DOCX:
  `docs/publisher/artifacts/agent-arch-ru-final-preauthor-raw-2026-07-03.docx`
- Template2000n DOCX:
  `docs/publisher/artifacts/agent-arch-ru-template2000n-final-preauthor-2026-07-03.docx`
- Render QA: raw 489 pages, Template2000n pre-author 361 pages, 0
  blank-like pages.
- Late-practice layout/style debt: closed for the current proof.
- Legacy long H2/H3 body-like paragraphs: reduced by 200 false outline
  entries; remaining long-heading candidates require final human TOC review.
- Template2000n.dot style package: applied through a conservative macro-free
  DOCX style route.
- Text sequence equality: preserved between raw and Template2000n proofs.
- Current final editorial handoff plan:
  `docs/publisher/ru-final-editorial-handoff-plan-2026-07-03.md`.
- Current Template2000n acceptance gate:
  `docs/publisher/ru-template2000n-acceptance-gate-2026-07-03.md`.
- Current pre-author export pass:
  `docs/publisher/ru-final-preauthor-export-pass-2026-07-03.md`.

Compressed/staging snapshot:

- <https://docs.google.com/document/d/1LyY2Psy2yaobn7VLmOwLTWm4QVrhp2I-ylE2B7V4pp4>

## Целевой формат по плану-проспекту

- рабочее название: `Архитектура безопасных ИИ-агентов`;
- введение: 8-12 стр.;
- 7 частей;
- 23 главы;
- приложения: 20-30 стр.;
- ориентировочный общий диапазон по плану-проспекту: 425-497 стр. до
  фактической версточной проверки.

## Договорная структура

### Введение

Диапазон: 8-12 стр.

Состав:

- для кого эта книга;
- почему агент - это не prompt-трюк, а production-система;
- как читать книгу;
- чем книга отличается от фреймворк-туториалов.

### Часть I. От demo-агента к платформе

Диапазон: 55-85 стр.

1. Почему агенту нужна платформа, а не магия.
2. Когда нужен агент: workflow, single-agent, multi-agent.
3. Референсная архитектура безопасной агентной системы.

Редакторский фокус:

- сохранить сильный opening argument;
- сделать главу 1 первым sample chapter;
- развести выбор формы исполнения и архитектурный blueprint по разным главам.

### Часть II. Безопасность и контур управления

Диапазон: 60-70 стр.

4. Контур безопасности и границы доверия.
5. Identity, session, policy layer и capability model.
6. Инструментальный шлюз, подтверждения и журнал аудита.

Редакторский фокус:

- заменить лишние англоязычные вставки русскими формами там, где это не имена
  протоколов или полей;
- показать право на действие как инженерный контракт.

### Часть III. Память, знания и контекст

Диапазон: 45-55 стр.

7. Зачем агенту память и почему она опасна.
8. Краткосрочная, долгосрочная и профильная память.
9. Извлечение контекста, уплотнение и фоновые обновления.

Редакторский фокус:

- не превращать главу в schema reference;
- держать provenance, freshness и tenant boundary в основном объяснении.

### Часть IV. Инструменты, выполнение и интеграция

Диапазон: 55-65 стр.

10. Модель выполнения и каталог инструментов.
11. Песочница выполнения и MCP как интеграционный контракт.
12. Идемпотентность, повторы, лимиты и границы отката.

Редакторский фокус:

- показать side effects и tool gateway через decision model;
- оставить protocol detail в online companion.

### Часть V. Надежность, наблюдаемость и оценки

Диапазон: 60-70 стр.

13. Трассы, спаны и структурированные события.
14. SLO для агентных систем.
15. Offline/online evals и регрессионные шлюзы.
16. Сквозная цепочка доказательств: от запроса к rollout.

Редакторский фокус:

- использовать главу 15 как технический sample при необходимости;
- держать trace/eval/rollout как один evidence model, а не три справочника.

### Часть VI. Организационная модель и жизненный цикл

Диапазон: 60-70 стр.

17. Платформенная команда и продуктовые команды.
18. Golden paths, общие шлюзы и борьба с агентным зоопарком.
19. От SDLC к ADLC: жизненный цикл агентной системы.
20. Assurance loop, incident response, registry и retirement.

Редакторский фокус:

- сжать текущий поздний web-материал в управляемый lifecycle arc;
- не тащить в печать весь registry/incident/reference detail.

### Часть VII. Эталонная реализация и промышленный запуск

Диапазон: 40-50 стр.

21. Базовая схема runtime.
22. Слой политик и каталог возможностей.
23. Чеклист промышленного запуска.

Редакторский фокус:

- дать исполнимую структуру без CLI manual;
- оставить команды, config contracts и runtime internals в companion.

### Приложения

Диапазон: 20-30 стр.

1. Глоссарий.
2. Чеклисты.
3. Шаблон incident/postmortem.
4. Источники и online companion.

## Online companion boundary

Оставить преимущественно online:

- runnable `agent_runtime_ref` package и CLI walkthrough;
- schema appendices for trace/eval/approval/policy/memory/lifecycle/change/incident;
- long CLI outputs;
- validation error catalogs;
- full YAML/JSON examples;
- source catalog beyond curated print bibliography;
- community roadmap;
- detailed policy templates and worksheets.

## Sample chapters

Primary sample:

- source path: `docs/book/part-i/chapter-1.md`;
- print role: глава 1;
- reason: strongest thesis chapter and opening failure story.

Secondary technical sample:

- source path: `docs/book/part-v/chapter-13.md`;
- print role: глава 15;
- reason: evals, traces, verifier outputs, regression gates and release judgment.

Optional lifecycle differentiator:

- source paths: `docs/book/part-viii/chapter-21.md`,
  `docs/book/part-viii/chapter-23.md`, `docs/book/part-viii/chapter-26.md`,
  `docs/book/part-viii/chapter-27.md`;
- print role: глава 20;
- reason: assurance, registry, retirement and accountability are less covered in
  competing books.

## First editorial pass order

1. Синхронизировать source map с договорной структурой.
2. Подготовить главу 1 в Google Doc.
3. Вернуть редакционные изменения главы 1 в Markdown.
4. Подготовить технический sample из текущей главы 13 как печатную главу 15.
5. Сжать текущую часть VIII в печатные главы 19-20.
6. Провести terminology pass по sample chapters.
7. После получения стилей БХВ выполнить DOCX formatting pass.

## Current proof status

2026-06-28 editorial-ready proof:

- canonical working manuscript: Google Doc
  <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>;
- raw DOCX proof:
  `docs/publisher/artifacts/agent-arch-ru-editorial-ready-2026-06-28.docx`;
- raw render: 499 pages, 0 blank-like pages;
- Template2000n proof:
  `docs/publisher/artifacts/agent-arch-ru-template2000n-editorial-ready-2026-06-28.docx`;
- Template2000n render: 315 pages, 0 blank-like pages;
- long H2 body-style debt: closed;
- long H3 body-style debt: closed;
- text sequence equality: preserved between raw and Template2000n proofs;
- next proof risk: final author-owned facts, companion metadata and external
  proofread before final delivery.

2026-07-03 legacy outline/style proof:

- canonical working manuscript: Google Doc
  <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>;
- raw DOCX proof:
  `docs/publisher/artifacts/agent-arch-ru-legacy-outline-style-pass-2026-07-03.docx`;
- raw render: 489 pages, 0 blank-like pages;
- Template2000n proof:
  `docs/publisher/artifacts/agent-arch-ru-template2000n-legacy-outline-style-pass-2026-07-03.docx`;
- Template2000n render: 351 pages, 0 blank-like pages;
- heading paragraphs reduced from 1352 to 1152 while preserving 6105
  non-empty paragraphs and 99587 words;
- text sequence equality: preserved between raw and Template2000n proofs;
- next proof risk: author-owned fields, external proofread, publisher-approved
  style requirements and final export QA.

2026-07-03 Template2000n official style proof:

- canonical working manuscript: Google Doc
  <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>;
- raw DOCX proof:
  `docs/publisher/artifacts/agent-arch-ru-publisher-style-raw-2026-07-03.docx`;
- raw render: 489 pages, 0 blank-like pages;
- Template2000n official-style proof:
  `docs/publisher/artifacts/agent-arch-ru-template2000n-official-style-pass-2026-07-03.docx`;
- Template2000n official-style render: 357 pages, 0 blank-like pages;
- source template: `/Users/if/Downloads/Telegram Desktop/Template2000n.dot`;
- template route: converted `.dot` to DOCX style source without running VBA,
  copied styles/theme/font table, preserved raw numbering, removed heading
  `numPr`, and mapped body paragraphs to `BodyText`;
- text sequence equality: preserved between raw and Template2000n proofs;
- next proof risk: author-owned fields, full human proofread,
  publisher/editor acceptance of the macro-free Template2000n route and final
  export QA.

2026-07-03 final editorial handoff planning pass:

- final editorial handoff plan:
  `docs/publisher/ru-final-editorial-handoff-plan-2026-07-03.md`;
- author fill packet for the current proof:
  `docs/publisher/ru-author-editorial-fill-packet-2026-07-03.md`;
- Google Doc and DOCX handoff policy:
  `docs/publisher/ru-google-doc-docx-handoff-policy-2026-07-03.md`;
- style acceptance gate:
  `docs/publisher/ru-template2000n-acceptance-gate-2026-07-03.md`;
- next 100 final handoff goals:
  `docs/publisher/ru-editorial-100-final-handoff-iterations-2026-07-03.md`;
- decision: the current packet is suitable for trusted editor review, but final
  publisher submission remains blocked until author-owned fields, style route
  acceptance, external proofread and post-author export/render QA are closed.

2026-07-03 final pre-author export/render pass:

- raw DOCX proof:
  `docs/publisher/artifacts/agent-arch-ru-final-preauthor-raw-2026-07-03.docx`;
- raw render: 489 pages, 0 blank-like pages;
- Template2000n pre-author proof:
  `docs/publisher/artifacts/agent-arch-ru-template2000n-final-preauthor-2026-07-03.docx`;
- Template2000n render: 361 pages, 0 blank-like pages;
- export/render report:
  `docs/publisher/ru-final-preauthor-export-pass-2026-07-03.md`;
- pre-author publisher packet:
  `docs/publisher/ru-preauthor-publisher-submission-packet-2026-07-03.md`;
- next 100 post-preauthor goals:
  `docs/publisher/ru-editorial-100-post-preauthor-iterations-2026-07-03.md`;
- decision: this is the current strongest working editor packet, but it still
  must not be labelled final publisher submission until the author-owned
  placeholders are replaced or explicitly omitted.
