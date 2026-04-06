# Agent Architecture Book

[English version](README.md)
[Contributing guide](CONTRIBUTING.md)
[Code of Conduct](CODE_OF_CONDUCT.md)

Публикуемый сайт и книга о современной архитектуре безопасных AI-агентов.

## Что есть в этом репозитории

- сайт на GitHub Pages, собранный на `MkDocs` и `Material for MkDocs`
- многоязычная структура документации
- первая опубликованная часть книги о безопасной архитектуре агентов
- небольшой опорный пакет с исполняемым примером в `agent_runtime_ref/`
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
.venv/bin/python -m unittest discover -s tests
```

## Опорный пакет

В репозитории есть минимальный опорный пакет, который можно запустить:

```bash
.venv/bin/python -m agent_runtime_ref
```

Это компактная кодовая опора для книги:

- эталонный рантайм и слой политик;
- каталог возможностей и approved inventory;
- память, телеметрия, approvals и rollout checks;
- YAML-конфиги для operational skeleton.

Быстрые примеры:

```bash
.venv/bin/python -m agent_runtime_ref simulate-run
.venv/bin/python -m agent_runtime_ref inspect-agent
.venv/bin/python -m agent_runtime_ref inspect-session
.venv/bin/python -m agent_runtime_ref export-session --output artifacts/session-demo-001.json
```

Каноническое описание пакета, полный список CLI-команд и обзор конфигов вынесены на отдельную страницу:

- [Опорный пакет](docs/appendix/reference-package.md)

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
- `ty` для проверки типов
- `MkDocs + Material for MkDocs` для публикации
- `Mermaid` и `Observable Plot` для визуализаций

## Лицензия

Репозиторий опубликован под лицензией [CC BY-SA 4.0](LICENSE).
