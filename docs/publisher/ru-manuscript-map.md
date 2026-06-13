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

Рабочая Google Doc-рукопись:

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
