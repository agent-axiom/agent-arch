# Выбор стека публикации

Эта страница объясняет, почему для книги выбран именно этот стек публикации.

## Короткий ответ

`MkDocs + Material for MkDocs` остается сильным выбором для Markdown-first книги на Python-стеке:

- низкий порог входа;
- быстрый билд;
- отличный поиск и навигация из коробки;
- простая публикация в GitHub Pages;
- естественная интеграция с `uv`, `ruff` и `ty`.[^mkdocs][^material][^uv][^ty]

При этом экосистема сейчас находится в переходной точке: в этом репозитории стек намеренно зафиксирован на `mkdocs<2`, чтобы сохранить совместимость с текущими плагинами и темой и не тащить в первую версию книги ненужный migration-risk.

!!! note "Канонические сценарии публикации (Canonical publishing cases)"
    Стек публикации (Publishing stack) должен поддерживать три канонических сценария (canonical cases) как маршруты чтения (reader routes), а не только страницы сборки (build pages). **Триаж обращений поддержки (Support triage)** требует быстрой сборки (fast build), деплоя на GitHub Pages (GitHub Pages deployment), поиска/навигации (search/navigation), читаемых примеров политик/подтверждений (policy/approval examples) и стабильных ссылок на артефакты трасс/оценок (trace/eval artifacts). **Внутренний ассистент знаний (Internal knowledge assistant)** требует авторства с приоритетом Markdown (Markdown-first authoring), многоязычных страниц (multilingual pages), поверхности глоссария/поиска (glossary/search surface), ссылок на источники (source links) и обновлений материалов памяти/поиска без лишнего трения (low-friction updates for memory/retrieval material). **Координация инцидентов (Incident coordination)** требует строгого шлюза сборки (strict build gate), воспроизводимых команд документации (reproducible docs commands), стабильной навигации к страницам инцидентов/раскаток (stable navigation to incident/rollout pages), видимых diff'ов в стиле журнала изменений (visible changelog-style diffs) и дисциплины миграционного риска (migration-risk discipline).

## Почему я не ушел сразу в Astro Starlight

`Starlight` очень хорош, если вам нужны:

- MDX и собственные UI-компоненты;
- более тяжелая фронтенд-кастомизация;
- тесная связка с экосистемой Astro.[^starlight]

Но для этой книги сейчас важнее другое:

- писать быстро;
- публиковать надежно;
- держать весь authoring-stack в Python;
- не усложнять CI и локальную сборку без реальной необходимости.

Поэтому первая версия сделана на MkDocs, а не на Astro.

## Принятая технологическая база

### Базовый стек

- `uv` для управления Python, виртуальной средой и dependency groups;
- `MkDocs` и `Material for MkDocs` для генерации сайта;
- `ruff` для linting;
- `ty` как быстрый type checker по мере появления Python-утилит в репозитории.

### Опциональный research-стек

- `marimo` для интерактивных исследовательских ноутбуков;
- `polars` для анализа логов, traces и eval datasets.

В текущем каркасе `marimo` и `polars` уже заведены как отдельная группа `research`, но пока не используются в книге напрямую.

## Команды проекта

```bash
uv sync --group docs --group dev
uv run mkdocs serve
uv run mkdocs build --strict
uv run ruff check .
uvx ty check
```

## Когда стоит мигрировать в Starlight

Переход имеет смысл, если в книге появятся:

- React/Vue/Svelte-компоненты внутри глав;
- много кастомного интерактива;
- docs-as-app вместо docs-as-book.

Пока таких требований нет.

[^mkdocs]: [MkDocs](https://www.mkdocs.org/)
[^material]: [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
[^uv]: [uv: Working on projects](https://docs.astral.sh/uv/guides/projects/)
[^ty]: [ty documentation](https://docs.astral.sh/ty/)
[^starlight]: [Starlight documentation](https://starlight.astro.build/)
