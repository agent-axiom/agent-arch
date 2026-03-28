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

