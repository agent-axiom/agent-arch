# Agent Architecture Book

![Coverage](docs/assets/badges/coverage.svg)

[English version](README.md)
[中文版](README.zh.md)
[Contributing guide](CONTRIBUTING.md)
[Code of Conduct](CODE_OF_CONDUCT.md)

Практическая книга и документационный сайт о безопасной, управляемой и готовой к production архитектуре (production-ready architecture) AI-агентов.

Этот проект для тех, кто хочет строить не магию для демо, а спокойные, контролируемые и безопасные агентные системы (controlled and safe agent systems), которые выдерживают контакт с реальными пользователями (real users), реальными инструментами (real tools) и реальной эксплуатацией (real operations).

![Превью книги об архитектуре агентов](docs/assets/images/readme.png)

## Зачем существует этот репозиторий

Большинство материалов про агентов оптимизируют путь к быстрому демо (quick demo). Реальным системам нужно больше, чем удачный промптинг (prompting) и вызовы инструментов (tool calls). Им нужны:

- явные границы доверия (trust boundaries)
- слой политик (policy layer) и подтверждений (approvals)
- дисциплина памяти (memory discipline)
- наблюдаемость (observability) и оценки (evals)
- контроль раскатки (rollout control) и управление жизненным циклом (lifecycle governance)

Этот репозиторий существует, чтобы документировать всю эту операционную модель целиком.

## Что есть в этом репозитории

- многоязычная книга по архитектуре безопасных AI-агентов
- документационный сайт на GitHub Pages, собранный на `MkDocs` и `Material for MkDocs`
- исполняемая эталонная среда исполнения (runtime) в `agent_runtime_ref/`
- практические схемы, чеклисты и операционные артефакты
- современный Python-first стек на базе `uv`

## Почему это стоит читать

- **Нейтральная к поставщикам архитектура (vendor-neutral architecture).** Книга опирается на принципы и операционные модели, которые переживут любой конкретный фреймворк (framework) или провайдера моделей (model provider).
- **Производственная реальность (production reality) вместо театра агентов (agent theater).** Фокус на политиках, подтверждениях, наблюдаемости, оценках (evals) и дисциплине жизненного цикла.
- **Исполняемый эталонный слой.** В репозитории есть не только концептуальный текст (conceptual prose), но и исполняемые эталонные артефакты (reference assets).
- **Один сквозной кейс по всему стеку (full-stack case).** Триаж поддержки / ветка дубля тикета (support-triage / duplicate-ticket thread) связывает книгу, эталонные схемы (reference schemas) и `agent_runtime_ref`, чтобы читатель мог проследить один инцидент от поиска (retrieval) и выполнения инструментов (tool execution) до телеметрии (telemetry), оценок (evals), раскатки (rollout), жизненного цикла (lifecycle) и управления реестром (registry control).
- **Три канонических сценария (canonical cases) для проверки покрытия (coverage check).** Триаж поддержки (Support triage) покрывает записывающие возможности (write capabilities) и подтверждения (approvals), внутренний ассистент знаний (Internal knowledge assistant) — поиск (retrieval), память (memory), свежесть (freshness) и происхождение знаний (knowledge provenance), а координация инцидентов (Incident coordination) — трассы (traces), эскалацию (escalation), побочные эффекты уведомлений (notification side effects), владельца реагирования (response ownership) и обучение после инцидента (post-incident learning).

## С чего начать

- Сайт проекта: <https://agent-axiom.github.io/agent-arch/>
- Главная страница книги: [docs/index.md](docs/index.md)
- Навигационная стартовая страница: [docs/start-here.md](docs/start-here.md)
- Сквозная цепочка схем безопасного агента (Safe-agent schema spine): [схема трасс (trace schema)](docs/appendix/trace-schema.md), [схема оценок (eval schema)](docs/appendix/eval-schema.md) и [схема памяти/поиска (memory/retrieval schema)](docs/appendix/memory-retrieval-schema.md) связывают модель угроз MCP (MCP threat model), контракт доверия передачи A2A (A2A handoff trust contract), запись вердикта проверяющего (verifier verdict record), запись действия управления (governance action record), поля ревью отравления памяти (memory poisoning review fields) и единые доказательства угроз агенту (unified agent threat evidence).
- Эталонная среда исполнения (runtime): [docs/appendix/reference-package.md](docs/appendix/reference-package.md)

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

## Эталонный пакет

В репозитории есть минимальный эталонный пакет, который можно запустить:

```bash
.venv/bin/python -m agent_runtime_ref
```

Это компактная кодовая опора (compact code support) для книги:

- эталонная среда исполнения (runtime) и слой политик (policy layer)
- каталог возможностей (capability catalog) и утвержденный инвентарь (approved inventory)
- путь памяти (memory path), телеметрия (telemetry), подтверждения (approvals) и проверки раскатки (rollout checks)
- артефакты жизненного цикла (lifecycle artifacts) для записей изменений (change records), пакетов артефактов (artifact bundles) и планов вывода из эксплуатации (retirement plans)
- видимый контракт профиля песочницы (sandbox profile contract) и доказательства ревью песочницы (sandbox review evidence) в инспекции жизненного цикла (lifecycle inspection)
- YAML-конфиги (YAML configs) для операционного скелета (operational skeleton)

Быстрые примеры (quick examples):

```bash
.venv/bin/python -m agent_runtime_ref simulate-run
.venv/bin/python -m agent_runtime_ref inspect-agent
.venv/bin/python -m agent_runtime_ref inspect-lifecycle
.venv/bin/python -m agent_runtime_ref inspect-session
.venv/bin/python -m agent_runtime_ref export-session --output artifacts/session-demo-001.json
.venv/bin/python -m agent_runtime_ref export-eval-dataset --output artifacts/eval-dataset.json
```

Каноническое описание пакета (canonical package description), полный список команд CLI (CLI commands) и обзор конфигурации (config overview) вынесены на отдельную страницу:

- [Эталонная среда исполнения (runtime reference package)](docs/appendix/reference-package.md)

## Опциональные исследовательские зависимости (optional research dependencies)

Если тебе нужны ноутбуки (notebooks) или инструменты анализа данных (data analysis tools):

```bash
uv sync --group research
```

В исследовательскую группу (research group) уже включены `marimo` и `polars`.

## Публикация (publishing)

В репозитории настроен рабочий процесс GitHub Actions (GitHub Actions workflow) для GitHub Pages:

- сборка (build) через `uv`
- строгая проверка (strict check) `mkdocs build --strict`
- деплой (deploy) в Pages из ветки публикации (publishing branch) `docs-prod`

Перед публикацией прогоните локальные проверки (local checks) и убедитесь, что `main` может обновить обе удалённые ветки fast-forward способом:

```bash
.venv/bin/ruff check .
.venv/bin/ty check
.venv/bin/pytest --cov=agent_runtime_ref --cov-report=term-missing
.venv/bin/mkdocs build --strict
git diff --check
git status --short --branch
git rev-list --left-right --count origin/main...HEAD
git rev-list --left-right --count origin/docs-prod...HEAD
```

Когда учётные данные на запись (write credentials) настроены, публикуйте только fast-forward push-командами (fast-forward push commands):

```bash
git push origin main
git push origin HEAD:docs-prod
```

Не делайте force-push в `docs-prod`; это намеренно только ветка-триггер (trigger branch) для GitHub Pages.

## Первый запуск GitHub Pages

У `actions/configure-pages@v5` есть важное ограничение: если Pages еще ни разу не были включены в репозитории, стандартный `GITHUB_TOKEN` может не суметь автоматически создать сайт Pages.

Есть два корректных варианта:

1. Один раз вручную включить Pages в `Settings -> Pages` и выбрать `GitHub Actions`.
2. Добавить секрет `PAGES_PAT` с нужными правами, и рабочий процесс сможет включить Pages автоматически.

Если для окружения `github-pages` заданы ограничения по веткам, нужно явно разрешить деплой из `docs-prod`.

Для `PAGES_PAT` нужен отдельный токен, а не `GITHUB_TOKEN`:

- для Personal Access Token: `repo` или Pages write permission
- для GitHub App: `administration:write` и `pages:write`

## Модель веток

- `main` — основная ветка разработки и источник правды
- `docs-prod` — ветка публикации для GitHub Pages

## Стек

- `uv` для окружения и зависимостей
- `ruff` для линтинга
- `ty` для проверки типов
- `MkDocs + Material for MkDocs` для публикации
- `Mermaid` и `Observable Plot` для визуализаций

## Лицензия

Репозиторий опубликован под лицензией [CC BY-SA 4.0](LICENSE).
