# План книги

Я строю эту книгу как инженерный playbook, а не как обзор фреймворков. Идея простая: каждая часть отвечает на один практический вопрос, который у тебя неизбежно возникнет, если ты попытаешься довести агентную систему до production.

## Структура

### Часть I. Основания

- Что такое современный агент и чем он отличается от workflow.
- Почему безопасная архитектура начинается с control plane, а не с "умного промпта".
- Референсная платформа безопасных агентов.

Статус: написана первая глава.

### Часть II. Контур безопасности

- Идентичность агента и machine IAM.
- Policy-as-code для моделей, памяти и инструментов.
- Prompt injection, data exfiltration, secret leakage, tool abuse.
- Human approval для опасных операций.

### Часть III. Память и знания

- Short-term vs long-term memory.
- Retrieval, compaction, summaries, profile memory.
- Когда память писать в hot path, а когда в background.

### Часть IV. Инструменты и выполнение

- Tool gateway и sandbox execution.
- MCP и контрактное подключение внешних систем.
- Idempotency, retries, rate limits, rollback boundaries.

### Часть V. Надежность и observability

- Traces, spans, structured events.
- SLO для агентских систем.
- Offline evals, online evals, trace grading, regression gates.

### Часть VI. Организационная модель

- Платформенная команда vs продуктовые команды.
- Шаблоны, golden paths, shared gateways.
- Как не превратить агентную платформу в зоопарк.

### Часть VII. Reference implementation

- Базовый runtime.
- Политики безопасности.
- Каталог инструментов.
- Набор проверок перед production rollout.

## Роадмап публикации

1. Зафиксировать архитектурную рамку и терминологию.
2. Дописать безопасность как отдельный слой, а не подпункт.
3. Добавить reference diagrams, интерактивные схемы и operational checklists.
4. Подготовить практический reference implementation.
5. Подключить примеры evals и policy configs.

## Что уже готово

- Каркас сайта для GitHub Pages.
- Навигация и структура книги.
- Первая часть с референсной архитектурой.
- Базовый визуальный слой: Mermaid и интерактивные графики через Observable Plot.
- Отдельная страница со стеком публикации.
- База источников для дальнейших глав.

[Перейти к первой части](part-i/index.md){ .md-button .md-button--primary }
