# Agent Architecture Book

Публикуемый сайт-книга по современной архитектуре безопасных AI-агентов.

## Локальный запуск

```bash
uv sync --group docs --group dev
uv run mkdocs serve
```

Сайт будет доступен по адресу `http://127.0.0.1:8000/`.

## Проверки

```bash
uv run ruff check .
uvx ty check
uv run mkdocs build --strict
```

## Исследовательские зависимости

Если понадобятся интерактивные ноутбуки и анализ данных:

```bash
uv sync --group research
```

В группе `research` уже предусмотрены `marimo` и `polars`.

## Публикация

В репозитории настроен GitHub Actions workflow для GitHub Pages:

- сборка через `uv`
- строгая проверка `mkdocs build --strict`
- публикация артефакта в Pages

### Первый запуск GitHub Pages

У `actions/configure-pages@v5` есть важное ограничение: если Pages еще ни разу не были включены в репозитории, стандартный `GITHUB_TOKEN` не может их активировать автоматически.

Есть два корректных варианта:

1. Один раз вручную включить Pages в `Settings -> Pages` и выбрать режим GitHub Actions.
2. Добавить секрет `PAGES_PAT` с правами, достаточными для включения Pages, и workflow сделает это сам.

Для `PAGES_PAT` нужен не `GITHUB_TOKEN`, а отдельный токен:

- для Personal Access Token: `repo` или Pages write permission;
- для GitHub App: `administration:write` и `pages:write`.
