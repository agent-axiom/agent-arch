# Agent Architecture Book

[English version](README.md)

Публикуемый сайт и книга о современной архитектуре безопасных AI-агентов.

## Что есть в этом репозитории

- сайт на GitHub Pages, собранный на `MkDocs` и `Material for MkDocs`
- многоязычная структура документации
- первая опубликованная часть книги о безопасной архитектуре агентов
- современный Python-first стек на базе `uv`

## Локальная разработка

```bash
uv sync --group docs --group dev
uv run mkdocs serve
```

Локальный сайт будет доступен по адресу `http://127.0.0.1:8000/`.

## Проверки

```bash
uv run ruff check .
uv run ty check
uv run mkdocs build --strict
```

## Опциональные исследовательские зависимости

Если тебе нужны ноутбуки или инструменты для анализа данных:

```bash
uv sync --group research
```

В группу `research` уже включены `marimo` и `polars`.

## Публикация

В репозитории настроен GitHub Actions workflow для GitHub Pages:

- сборка через `uv`
- строгая проверка `mkdocs build --strict`
- деплой в Pages из ветки `docs-prod`

## Первый запуск GitHub Pages

У `actions/configure-pages@v5` есть важное ограничение: если Pages еще ни разу не были включены в репозитории, стандартный `GITHUB_TOKEN` может не суметь автоматически создать Pages site.

Есть два корректных варианта:

1. Один раз вручную включить Pages в `Settings -> Pages` и выбрать `GitHub Actions`.
2. Добавить секрет `PAGES_PAT` с нужными правами, и workflow сможет включить Pages автоматически.

Если для environment `github-pages` заданы ограничения по веткам, нужно явно разрешить деплой из `docs-prod`.

Для `PAGES_PAT` нужен отдельный токен, а не `GITHUB_TOKEN`:

- для Personal Access Token: `repo` или Pages write permission
- для GitHub App: `administration:write` и `pages:write`

## Модель веток

- `main` — основная ветка разработки и источник правды
- `docs-prod` — ветка публикации для GitHub Pages

## Стек

- `uv` для окружения и зависимостей
- `ruff` для linting
- `ty` для type checking
- `MkDocs + Material for MkDocs` для публикации
- `Mermaid` и `Observable Plot` для визуализаций
