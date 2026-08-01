# Карта русской издательской рукописи

Status: current-state pointer plus historical contractual baseline. План-проспект
к договору авторского заказа N 4-5/26 от 15 мая 2026 года сохранен ниже как
история исходной 23-главной структуры, но больше не описывает текущую сборку.

## Текущее каноническое состояние

- редактируемый снимок рукописи:
  `docs/publisher/ru-manuscript-google-doc-final-2026-07-11.md`;
- детерминированная редакционная сборка:
  `docs/publisher/ru-manuscript-editorial-2026-07-13.md`;
- издательская рукопись: <https://docs.google.com/document/d/1LyY2Psy2yaobn7VLmOwLTWm4QVrhp2I-ylE2B7V4pp4/edit>;
- ревизия Google Doc:
  `AIroW37DrV8dNIYvUEV4d5pOla46Wwq6WopW3RWy18Hy0wJwUNzmMRpRfxpU-LXjQBCZv9zKOxq82sIury9MhmTP3x55NmDU2pjFkh8ELnk`;
- структура: 8 частей, 28 глав, приложения;
- учебный контур: 8 лабораторных работ и итоговый проект;
- визуальный контур: 25 пронумерованных рисунков и 31 встроенная схема,
  всего 56 изображений;
- табличный контур: 11 таблиц;
- объём издательской сборки: около 96 984 слов;
- проверочный экспорт живого Google Doc: 506 страниц Letter;
- Google-ориентированная производная: 481 страница Letter;
- проверочная производная Template2000n: 355 страниц Letter, пустых технических
  страниц нет;
- финальные артефакты: исходный DOCX, PDF и макросвободная производная DOCX
  со стилями Template2000n в `docs/publisher/artifacts/`;
- итог текущего прохода и проверки:
  `docs/publisher/ru-reader-experience-pass-2026-08-01.md`.

Смысловые изменения возвращаются из Google Doc в канонический Markdown. Старые
Google Docs, DOCX-артефакты и показатели страниц ниже являются историческими
контрольными точками, а не текущим издательским доказательством.

## Назначение

Публичная версия в репозитории остается широкой веб-версией: 8 частей, 27 глав,
практические страницы, справочные приложения и исполняемый эталонный пакет.
Издательская рукопись собирается как отдельный слой: 8 частей, 28 глав,
введение и приложения. Google Doc используется как рабочая издательская
рукопись, но смысловые изменения должны возвращаться в Markdown.

Карта источников для сборки:

- `docs/publisher/ru-source-map.md`

Историческая рабочая Google Doc-рукопись:

- <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>

Редакционная карта проверки книжной готовности:

- <https://docs.google.com/document/d/1XoU_nWZkpKGU7SxZ0pgmE_dfcNNggQokZsbzind7kXc>

Историческая контрольная точка до финального прохода:

- Google Doc export modified time:
  `2026-07-02T22:46:03.373Z`
- Google Doc revision after 2026-07-04 terminology update:
  `ALtnJHwPMvOVdwcrz2tbGM0rdze_Ped9LzfMOgWtZCTtkIG1K5pXx008c-6ckzYavZt9Wn-LtRrB9r16Q37qcoztxBoKsxdBLmi6LKr_EW4`
- Raw DOCX:
  `docs/publisher/artifacts/agent-arch-ru-final-preauthor-raw-2026-07-03.docx`
- Template2000n DOCX:
  `docs/publisher/artifacts/agent-arch-ru-template2000n-quality-sync-2026-07-04.docx`
- Render QA: raw baseline 489 pages, Template2000n quality-sync 357 pages, 0
  blank-like pages.
- Current quality-sync pass:
  `docs/publisher/ru-google-doc-quality-sync-pass-2026-07-04.md`.
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

Текущая полнообъемная Google Doc-рукопись:

- <https://docs.google.com/document/d/1LyY2Psy2yaobn7VLmOwLTWm4QVrhp2I-ylE2B7V4pp4>

## Текущий целевой формат

- рабочее название: `Архитектура безопасных ИИ-агентов`;
- введение: 8-12 стр.;
- 8 частей;
- 28 глав;
- приложения: 20-30 стр.;
- ориентировочный общий диапазон по плану-проспекту: 425-497 стр. до
  фактической версточной проверки.

## Историческая договорная структура

Ниже сохранена исходная 23-главная карта плана-проспекта. Актуальная структура
глав 1-28 зафиксирована в `docs/publisher/ru-source-map.md` и каноническом
Markdown; этот раздел не следует использовать для текущей нумерации ссылок.

### Введение

Диапазон: 8-12 стр.

Состав:

- для кого эта книга;
- почему агент - это не prompt-трюк, а production-система;
- как читать книгу;
- чем книга отличается от фреймворк-туториалов.

### Часть I. От демо-агента к платформе

Диапазон: 55-85 стр.

1. Почему агенту нужна платформа, а не магия.
2. Когда нужен агент: рабочий процесс, одиночный агентный цикл, многоагентная схема.
3. Референсная архитектура безопасной агентной системы.

Редакторский фокус:

- сохранить сильный открывающий тезис;
- сделать главу 1 первой примерной главой;
- развести выбор формы исполнения и архитектурную схему по разным главам.

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

- показать побочные эффекты и инструментальный шлюз через модель решения;
- оставить детали протокола в онлайн-приложении.

### Часть V. Надежность, наблюдаемость и оценки

Диапазон: 60-70 стр.

13. Трассы, спаны и структурированные события.
14. SLO для агентных систем.
15. Офлайн- и онлайн-оценки и регрессионные шлюзы.
16. Сквозная цепочка доказательств: от запроса к поэтапному выпуску.

Редакторский фокус:

- использовать главу 15 как технический образец при необходимости;
- держать трассы, оценки и поэтапный выпуск как единую доказательную модель, а
  не три справочника.

### Часть VI. Организационная модель и жизненный цикл

Диапазон: 60-70 стр.

17. Платформенная команда и продуктовые команды.
18. Golden paths, общие шлюзы и борьба с агентным зоопарком.
19. От SDLC к ADLC: жизненный цикл агентной системы.
20. Контур заверения, реагирование на инциденты, реестр и вывод из эксплуатации.

Редакторский фокус:

- сжать текущий поздний веб-материал в управляемую дугу жизненного цикла;
- не тащить в печать все подробности реестра, инцидентов и справочных
  материалов.

### Часть VII. Эталонная реализация и промышленный запуск

Диапазон: 40-50 стр.

21. Базовая схема среды исполнения.
22. Слой политик и каталог возможностей.
23. Чеклист промышленного запуска.

Редакторский фокус:

- дать исполнимую структуру без руководства по командной строке;
- оставить команды, контракты конфигурации и внутренние детали среды исполнения
  в онлайн-приложении.

### Приложения

Диапазон: 20-30 стр.

1. Глоссарий.
2. Чеклисты.
3. Шаблон incident/postmortem.
4. Источники и онлайн-приложение.

## Граница онлайн-приложения

Оставить преимущественно в онлайн-приложении:

- исполняемый пакет `agent_runtime_ref` и пошаговый разбор командного запуска;
- приложения со схемами трасс, оценок, подтверждений, политик, памяти,
  жизненного цикла, изменений и инцидентов;
- длинные выводы командной строки;
- каталоги ошибок валидации;
- полные YAML/JSON-примеры;
- каталог источников за пределами отобранной печатной библиографии;
- дорожная карта сообщества;
- подробные шаблоны политик и рабочие листы.

## Примерные главы

Основной образец:

- путь источника: `docs/book/part-i/chapter-1.md`;
- печатная роль: глава 1;
- причина: самая сильная тезисная глава и открывающая история отказа.

Второй технический образец:

- путь источника: `docs/book/part-v/chapter-13.md`;
- печатная роль: глава 15;
- причина: оценки, трассы, выводы проверяющего, регрессионные шлюзы и релизное
  суждение.

Дополнительное отличие по жизненному циклу:

- пути источников: `docs/book/part-viii/chapter-21.md`,
  `docs/book/part-viii/chapter-23.md`, `docs/book/part-viii/chapter-26.md`,
  `docs/book/part-viii/chapter-27.md`;
- печатная роль: глава 20;
- причина: заверение, реестр, вывод из эксплуатации и подотчетность обычно
  хуже раскрыты в конкурирующих книгах.

## First editorial pass order

1. Синхронизировать карту источников с договорной структурой.
2. Подготовить главу 1 в Google Doc.
3. Вернуть редакционные изменения главы 1 в Markdown.
4. Подготовить технический образец из текущей главы 13 как печатную главу 15.
5. Сжать текущую часть VIII в печатные главы 19-20.
6. Провести терминологический проход по примерным главам.
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

2026-07-04 targeted editorial quality pass:

- quality pass report:
  `docs/publisher/ru-editorial-quality-pass-2026-07-04.md`;
- next 100 editorial quality goals:
  `docs/publisher/ru-editorial-100-editorial-quality-iterations-2026-07-04.md`;
- Google Doc revision after targeted Chapter 20-21 bridge insertion:
  `ALtnJHynC5_zU9n9cmTvBjPl9UMeD7Uve6QHp3PDDm33ZwWHCfBekh00ktjv4-xnUtiwP6hL7W39I4iTLk77MaTY60Z8DnRkpVQxhi5p46U`;
- repository changes: Chapter 20-21 bridge paragraphs added to
  `docs/publisher/ru-manuscript-full.md`; excessive anglicisms reduced in
  `docs/publisher/ru-source-map.md` and this map;
- next proof risk: a fresh raw/Template2000n export has not been created after
  this targeted Google Doc edit, so page counts remain those from 2026-07-03
  until the next export/render QA.

2026-07-04 quality-sync terminology and Template2000n pass:

- Google Doc revision after terminology cleanup:
  `ALtnJHwPMvOVdwcrz2tbGM0rdze_Ped9LzfMOgWtZCTtkIG1K5pXx008c-6ckzYavZt9Wn-LtRrB9r16Q37qcoztxBoKsxdBLmi6LKr_EW4`;
- Google Doc exact terminology replacements: 293, followed by 23 grammatical
  corrections;
- readback confirmed no exact `online companion`, `policy gateway`,
  `tool gateway` or `incident response` in the updated Google Doc;
- Template2000n quality-sync proof:
  `docs/publisher/artifacts/agent-arch-ru-template2000n-quality-sync-2026-07-04.docx`;
- render QA: raw baseline 489 pages and Template2000n quality-sync 357 pages,
  0 blank-like pages;
- report:
  `docs/publisher/ru-google-doc-quality-sync-pass-2026-07-04.md`;
- next 100 quality-sync/export goals:
  `docs/publisher/ru-editorial-100-quality-sync-export-iterations-2026-07-04.md`;
- next proof risk: because the Google Doc changed after the latest saved raw
  DOCX baseline, a fresh authenticated raw DOCX export is required before a
  final publisher proof can be claimed.
