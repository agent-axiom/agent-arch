# План книги

Я строю эту книгу как инженерный playbook, а не как обзор фреймворков. Идея простая: каждая часть отвечает на один практический вопрос, который у тебя неизбежно возникнет, если ты попытаешься довести агентную систему до production.

## Структура

### Часть I. Основания

- Глава 1. Почему агенту нужна платформа, а не магия.
- Глава 2. Референсная архитектура безопасного агента.

Статус: часть написана и разбита на короткие главы.

### Часть II. Контур безопасности

- Глава 3. Контур безопасности и границы доверия.
- Глава 4. Tool gateway, approval и audit trail.

### Часть III. Память и знания

- Глава 5. Зачем агенту память и почему она опасна.
- Глава 6. Short-term, long-term и profile memory.
- Глава 7. Retrieval, compaction и background updates.
- Когда память писать в hot path, а когда в background.

Статус: три главы части написаны.

### Часть IV. Инструменты и выполнение

- Глава 8. Execution model и каталог инструментов.
- Глава 9. Sandbox execution и MCP как контракт интеграции.
- Глава 10. Idempotency, retries, rate limits и rollback boundaries.

Статус: три главы части написаны.

### Часть V. Надежность и observability

- Глава 11. Traces, spans и structured events.
- Глава 12. SLO для агентных систем.
- Глава 13. Offline evals, online evals и regression gates.

Статус: три главы части написаны.

### Часть VI. Организационная модель

- Глава 14. Platform team vs product teams.
- Глава 15. Golden paths, shared gateways и anti-zoo patterns.

Статус: две первые главы части написаны.

### Часть VII. Reference implementation

- Глава 16. Базовый runtime blueprint.
- Глава 17. Policy layer и capability catalog.
- Набор проверок перед production rollout.

Статус: две первые главы части написаны.

## Роадмап публикации

1. Зафиксировать архитектурную рамку и терминологию.
2. Дописать безопасность как отдельный слой, а не подпункт.
3. Добавить reference diagrams, интерактивные схемы и operational checklists.
4. Подготовить практический reference implementation.
5. Подключить примеры evals и policy configs.

## Что уже готово

- Каркас сайта для GitHub Pages.
- Навигация и структура книги.
- Первые семь частей уже имеют рабочую структуру, и reference implementation началась.
- Базовый визуальный слой: Mermaid и интерактивные графики через Observable Plot.
- Отдельная страница со стеком публикации.
- База источников для дальнейших глав.

[Перейти к первой части](part-i/index.md){ .md-button .md-button--primary }
