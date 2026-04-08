# Справочный пакет

В репозитории теперь есть небольшой исполняемый каркас: [agent_runtime_ref](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref).

Его задача не в том, чтобы стать промышленным фреймворком. Он нужен как минимальная кодовая опора для **частей VII и VIII** книги.

Здесь собран полный разбор пакета: CLI, конфиги, структура и связь с книгой.

## Что внутри

- [runtime.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/runtime.py)
  Основной `AgentRuntime`, который собирает контекст запуска, извлечение контекста, шаг модели, выполнение инструментов и хук фонового обновления.
- [policy.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/policy.py)
  Небольшой движок политик со структурированными решениями.
- [catalog.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/catalog.py)
  Реестр возможностей с описанием эксплуатационной семантики, risk tier и egress-контракта.
- [identity.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/identity.py)
  Явная identity агента и approved inventory возможностей, с которыми рантайм вообще имеет право работать.
- [config.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/config.py)
  Загрузчик YAML для identity агента, approved inventory, политик, каталога возможностей и политики выкладки.
- [memory.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/memory.py)
  Типизированные записи памяти, provenance, ревизии и in-memory-хранилище с изоляцией по тенантам.
- [background.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/background.py)
  Фоновый контур обслуживания для постоянных записей в память, provenance-aware сохранения и уплотнения.
- [execution.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/execution.py)
  Простой вызов возможностей через выполнение, учитывающее контракт, risk tier и egress policy.
- [telemetry.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/telemetry.py)
  In-memory-эмиттер телеметрии для структурированных событий и спанов.
- [rollout.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/rollout.py)
  Минимальный шлюз проверки готовности перед выкладкой.
- [controls.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/controls.py)
  Проверка continuous controls и inventory drift для approved registry.
- [approvals.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/approvals.py)
  Approval gates и простая human review queue для high-risk действий.
- [lifecycle.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/lifecycle.py)
  Lifecycle-артефакты для change record, artifact bundle и retirement plan, плюс readiness-проверки для этих состояний.

## Как запустить

```bash
.venv/bin/python -m agent_runtime_ref
```

Ожидаемый результат:

```json
{"result": "Ticket request accepted and ready for follow-up.", "status": "success", "events": 9, "memory_records": 4, "config_dir": ".../agent_runtime_ref/configs"}
```

Явный запуск рантайма через подкоманду:

```bash
.venv/bin/python -m agent_runtime_ref simulate-run
```

Просмотр identity агента и approved inventory:

```bash
.venv/bin/python -m agent_runtime_ref inspect-agent
```

Просмотр lifecycle-артефактов из Part VIII:

```bash
.venv/bin/python -m agent_runtime_ref inspect-lifecycle
.venv/bin/python -m agent_runtime_ref check-change --signal offline_eval_passed=false
.venv/bin/python -m agent_runtime_ref check-retirement --step revoke_egress=false
```

Просмотр записей памяти:

```bash
.venv/bin/python -m agent_runtime_ref inspect-memory --memory-class profile
```

`inspect-memory` показывает не только содержимое, но и `provenance` с `revision`.

Вывод структурированных событий для одного запуска:

```bash
.venv/bin/python -m agent_runtime_ref dump-events --user-input "Please open a ticket for this issue."
```

Экспорт событий в JSONL для разбора и повторного прогона:

```bash
.venv/bin/python -m agent_runtime_ref export-events --output artifacts/trace-demo.jsonl
```

Если нужен redacted export для внешнего разбора, можно сразу скрыть чувствительные поля:

```bash
.venv/bin/python -m agent_runtime_ref export-events --output artifacts/trace-demo.jsonl --redact-field user_input
```

Просмотр одной трассы из JSONL-файла:

```bash
.venv/bin/python -m agent_runtime_ref inspect-trace --input artifacts/trace-demo.jsonl
```

Повторный прогон по сохраненной трассе:

```bash
.venv/bin/python -m agent_runtime_ref replay-run --input artifacts/trace-demo.jsonl
```

Проверка политики выкладки с переопределением сигналов:

```bash
.venv/bin/python -m agent_runtime_ref check-rollout --signal offline_eval_pass=false
```

Проверка continuous controls и drift по реестру:

```bash
.venv/bin/python -m agent_runtime_ref check-controls --signal registry_reviewed=false
```

Просмотр и разрешение demo approval requests:

```bash
.venv/bin/python -m agent_runtime_ref inspect-approvals
.venv/bin/python -m agent_runtime_ref resolve-approval --decision approved --note "manager approved demo request"
.venv/bin/python -m agent_runtime_ref inspect-session
.venv/bin/python -m agent_runtime_ref session-eval-summary
.venv/bin/python -m agent_runtime_ref session-replay --user-input "Please create a ticket for this onboarding issue." --user-input "What language preference do you remember?"
.venv/bin/python -m agent_runtime_ref export-session --output artifacts/session-demo-001.json
.venv/bin/python -m agent_runtime_ref export-eval-dataset --output artifacts/eval-dataset.json
```

`inspect-session` показывает session-level историю запусков и связанные `trace_id`.
`session-eval-summary` возвращает короткую operational summary по серии запусков.
`session-replay` позволяет прогнать несколько связанных запросов в одной `session_id`.
`export-session` сохраняет сессию как структурированный JSON, который уже можно использовать как seed для offline evals.
`export-eval-dataset` собирает несколько встроенных session-сценариев в один eval-ready JSON artifact.

Запрос, который действительно читает профильную память:

```bash
.venv/bin/python -m agent_runtime_ref simulate-run --user-input "What language preference do you remember?"
```

## Как проверить

```bash
uv run ruff check .
uv run ty check
uv run pytest --cov=agent_runtime_ref --cov-report=term-missing
```

## Примерные конфиги

В [configs](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs) лежат стартовые файлы для рантайма и lifecycle:

- [agent.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/agent.yaml)
- [policy.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/policy.yaml)
- [capabilities.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/capabilities.yaml)
- [memory.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/memory.yaml)
- [rollout.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/rollout.yaml)
- [controls.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/controls.yaml)
- [approvals.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/approvals.yaml)
- [change.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/change.yaml)
- [artifacts.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/artifacts.yaml)
- [retirement.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/retirement.yaml)

Это уже не просто статические примеры. `config.py` умеет загружать эти YAML-файлы в identity агента, approved inventory, рантайм, context layers, хранилище памяти, политику выкладки и lifecycle-артефакты, поэтому пакет стал ближе к реальному эксплуатационному каркасу.

## Почему это полезно

Книга теперь опирается не только на текстовые объяснения, но и на реальный кодовый каркас:

- легче обсуждать архитектуру на уровне файлов и контрактов;
- легче расширять пакет следующими примерами;
- легче перейти от главы к исполняемому прототипу;
- легче показать путь, управляемый конфигурацией, а не только жестко зашитое демо;
- легче связать эталонный рантайм с главами про память, извлечение контекста и фоновые обновления.
- легче обсуждать, откуда взялся каждый memory record и какая у него ревизия.

Отдельно полезно то, что теперь package можно не только запускать, но и инспектировать снаружи:

- `inspect-memory` показывает исходно загруженную память и фильтрацию по `tenant` и `memory_class`;
- `dump-events` показывает структурированную трассу одного запуска без чтения исходников;
- `export-events` сохраняет трассу в JSONL для разбора вне процесса;
- `export-events` умеет добавлять `schema_version` и делать export-time redaction по выбранным полям;
- `inspect-trace` позволяет читать и фильтровать сохраненные трассы;
- `replay-run` поднимает повторный прогон по `run_start` из сохраненной трассы.

## См. также

- [Схема трасс и каталог событий](trace-schema.md)
- [Схема наборов для оценки и правил проверки](eval-schema.md)
- [Схема набора политик и контракта подтверждения](policy-bundle-schema.md)
- [Схема артефактов жизненного цикла](lifecycle-artifact-schema.md)
- [Глава 17. Слой политик и каталог возможностей](../book/part-vii/chapter-17.md)
