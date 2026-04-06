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

Внутри уже есть эталонный рантайм, слой политик, каталог возможностей, явная identity агента, approved inventory возможностей, сборка context layers, provenance памяти, risk tiers инструментов, egress-aware execution contracts, approval gates, фоновый контур обслуживания, эмиттер телеметрии, шлюз проверки готовности к запуску и загрузчик конфигурации из YAML для частей III и VII книги.

Можно запускать и более наглядные демонстрационные команды:

```bash
.venv/bin/python -m agent_runtime_ref simulate-run
.venv/bin/python -m agent_runtime_ref inspect-agent
.venv/bin/python -m agent_runtime_ref inspect-memory --memory-class profile
.venv/bin/python -m agent_runtime_ref dump-events --user-input "Please open a ticket for this issue."
.venv/bin/python -m agent_runtime_ref export-events --output artifacts/trace-demo.jsonl
.venv/bin/python -m agent_runtime_ref inspect-trace --input artifacts/trace-demo.jsonl
.venv/bin/python -m agent_runtime_ref replay-run --input artifacts/trace-demo.jsonl
.venv/bin/python -m agent_runtime_ref check-rollout --signal offline_eval_pass=false
.venv/bin/python -m agent_runtime_ref check-controls --signal registry_reviewed=false
.venv/bin/python -m agent_runtime_ref inspect-approvals
.venv/bin/python -m agent_runtime_ref resolve-approval --decision approved --note "manager approved demo request"
.venv/bin/python -m agent_runtime_ref simulate-run --user-input "What language preference do you remember?"
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
- `ty` для проверки типов
- `MkDocs + Material for MkDocs` для публикации
- `Mermaid` и `Observable Plot` для визуализаций

## Лицензия

Репозиторий опубликован под лицензией [CC BY-SA 4.0](LICENSE).
