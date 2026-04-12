# Agent Architecture Book

[English version](README.md)
[中文版](README.zh.md)
[Contributing guide](CONTRIBUTING.md)
[Code of Conduct](CODE_OF_CONDUCT.md)

Практическая книга и документационный сайт о безопасной, управляемой и production-ready архитектуре AI-агентов.

Этот проект для тех, кто хочет строить не магию для демо, а спокойные, контролируемые и безопасные агентные системы, которые выдерживают контакт с реальными пользователями, реальными инструментами и реальной эксплуатацией.

![Превью книги об архитектуре агентов](docs/assets/images/readme.png)

## Зачем существует этот репозиторий

Большинство материалов про агентов оптимизируют путь к быстрому демо. Реальным системам нужно больше, чем clever prompting и вызовы инструментов. Им нужны:

- явные границы доверия
- слой политик и подтверждений
- дисциплина памяти
- наблюдаемость и оценки
- контроль раскатки и управление жизненным циклом

Этот репозиторий существует, чтобы документировать всю эту операционную модель целиком.

## Что есть в этом репозитории

- многоязычная книга по архитектуре безопасных AI-агентов
- документационный сайт на GitHub Pages, собранный на `MkDocs` и `Material for MkDocs`
- исполняемый справочный рантайм в `agent_runtime_ref/`
- практические схемы, чеклисты и операционные артефакты
- современный Python-first стек на базе `uv`

## Почему это стоит читать

- **Vendor-neutral архитектура.** Книга опирается на принципы и операционные модели, которые переживут любой конкретный фреймворк или model provider.
- **Production reality вместо agent theater.** Фокус на политиках, подтверждениях, наблюдаемости, evals и дисциплине жизненного цикла.
- **Исполняемый справочный слой.** В репозитории есть не только текст, но и рабочие reference assets.

## С чего начать

- Сайт проекта: <https://agent-axiom.github.io/agent-arch/>
- Главная страница книги: [docs/index.md](docs/index.md)
- Навигационная стартовая страница: [docs/start-here.md](docs/start-here.md)
- Справочный рантайм: [docs/appendix/reference-package.md](docs/appendix/reference-package.md)

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
uv run pytest --cov=agent_runtime_ref --cov-report=term-missing
uv run mkdocs build --strict
```

## Справочный пакет

В репозитории есть минимальный справочный пакет, который можно запустить:

```bash
.venv/bin/python -m agent_runtime_ref
```

Это компактная кодовая опора для книги:

- справочный рантайм и слой политик
- каталог возможностей и approved inventory
- память, телеметрия, approvals и rollout checks
- lifecycle-артефакты для change records, artifact bundles и retirement plans
- YAML-конфиги для operational skeleton

Быстрые примеры:

```bash
.venv/bin/python -m agent_runtime_ref simulate-run
.venv/bin/python -m agent_runtime_ref inspect-agent
.venv/bin/python -m agent_runtime_ref inspect-lifecycle
.venv/bin/python -m agent_runtime_ref inspect-session
.venv/bin/python -m agent_runtime_ref export-session --output artifacts/session-demo-001.json
.venv/bin/python -m agent_runtime_ref export-eval-dataset --output artifacts/eval-dataset.json
```

Каноническое описание пакета, полный список CLI-команд и обзор конфигов вынесены на отдельную страницу:

- [Справочный пакет](docs/appendix/reference-package.md)

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
