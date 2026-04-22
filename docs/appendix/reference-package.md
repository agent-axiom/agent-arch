# Справочный пакет

В репозитории теперь есть небольшой исполняемый каркас: [agent_runtime_ref](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref).

Его задача не в том, чтобы стать промышленным фреймворком. Он нужен как минимальная кодовая опора для **частей VII и VIII** книги.

Этот пакет намеренно задуман как практическая опора реализации, а не как параллельный продукт. Его ценность в том, что читатель может посмотреть на работающую структуру системы, которая стоит за аргументом книги, не превращая проект в руководство по фреймворку.

Чего эта страница **не** обещает:

- она не заменяет книжное объяснение того, зачем вообще существуют эти слои;
- она не должна быть главным местом, где читатель разбирается в архитектурных компромиссах;
- она не пытается превратить репозиторий в универсальный фреймворк для агентов.

Здесь собран полный разбор пакета: CLI, конфиги, структура и связь с книгой.

Практичный маршрут чтения такой:

- Chapter 16 для baseline runtime и capability session state,
- Chapter 17 для policy layer и capability contracts,
- [Сквозная цепочка доказательств](../book/part-v/evidence-spine.md) для end-to-end записи от запроса до rollout judgment,
- Chapter 18 для rollout gates вокруг approval и runtime behavior,
- Chapter 21 для assurance response,
- Chapter 22 и lifecycle schema для governed artifact linkage, идентичности выпуска, verifier-contract lineage и delegated authorization provenance,
- Chapters 23-27 для interruption, expiry, re-init, retirement, observability, registry ownership, obligations по verifier evidence и delegated-authorization lifecycle control вокруг capability sessions.

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
  Approval gates, pause/resume semantics, простая human review queue для high-risk действий и тот control surface, где approval state должен оставаться синхронизирован с capability session state.

Этот же runtime-control surface естественно расширяется и на delegated authorization assumptions: какой principal делегировал доступ, переживает ли такая авторизация pause/resume и что делает runtime, если delegated access отозвали до завершения действия.
- [lifecycle.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/lifecycle.py)
  Lifecycle-артефакты для change record, artifact bundle, записей об идентичности выпуска, runtime-control schemas, verifier-contract lineage и retirement plan, плюс readiness-проверки для этих состояний.

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
.venv/bin/python -m agent_runtime_ref simulate-run --simulate-failure tool_timeout
```

Второй вариант специально добавлен как небольшой failure-rich сценарий. Он позволяет пакету показать, что даже разрешенная capability может завершиться как управляемый failed run с явной телеметрией, а не раствориться за общим happy path.

Просмотр identity агента и approved inventory:

```bash
.venv/bin/python -m agent_runtime_ref inspect-agent
```

Просмотр lifecycle-артефактов из Part VIII, включая runtime-control linkage и идентичность выпуска:

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
`dump-events` теперь тоже возвращает `failure_reason` в JSON-ответе для degraded-path drills.

Вывод структурированных событий для одного запуска:

```bash
.venv/bin/python -m agent_runtime_ref dump-events --user-input "Please open a ticket for this issue."
.venv/bin/python -m agent_runtime_ref dump-events --simulate-failure tool_timeout
```

Экспорт событий в JSONL для разбора и повторного прогона:

```bash
.venv/bin/python -m agent_runtime_ref export-events --output artifacts/trace-demo.jsonl
.venv/bin/python -m agent_runtime_ref export-events --simulate-failure upstream_unavailable --output artifacts/trace-demo-failed.jsonl
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
.venv/bin/python -m agent_runtime_ref export-session --simulate-failure tool_timeout --output artifacts/session-demo-failed.json
.venv/bin/python -m agent_runtime_ref export-eval-dataset --output artifacts/eval-dataset.json
.venv/bin/python -m agent_runtime_ref export-eval-dataset --scenario failed_run_timeout --output artifacts/eval-failed-run.json
```

`inspect-session` показывает session-level историю запусков и связанные `trace_id`.
`session-eval-summary` возвращает короткую operational summary по серии запусков, включая и failed runs, и `traceable_failed_runs`, а не сводя все обратно только к успехам и отказам.
`session-replay` позволяет прогнать несколько связанных запросов в одной `session_id`.
`export-session` сохраняет сессию как структурированный JSON, который уже можно использовать как seed для offline evals. Теперь он еще и сохраняет delegated authorization context, включая `authorization_mode`, `delegated_principal_id` и `delegated_scope`, а в summary самой CLI-команды показывает `failed_runs`, `traceable_failed_runs` и `latest_failure_reason` для failed drills.

Теперь рантайм также считает tool paths с неуспешным исходом, например validation failure, полноценным итогом запуска. Вместо того чтобы делать вид, будто run завершился успешно, он фиксирует failed run, пишет явное событие `run_failed` и сохраняет и в session export, и в CLI output этот статус вместе с конкретной причиной сбоя в поле `failure_reason`.
`export-eval-dataset` собирает несколько встроенных session-сценариев в один eval-ready JSON artifact, включая отдельный failed-run drill scenario.

Этот eval path теперь полезно читать вместе с richer verifier contract из appendix: для long-horizon scenarios пакет должен помогать представить, как dataset со временем может нести `process_score`, `outcome_score`, `failure_attribution` и linked verifier evidence, а не только один тонкий verdict.

Вместе эти команды теперь помогают показать важное различие из Chapters 16 и 17:

- пользовательскую `session_id`, которая связывает несколько runs;
- `trace_id` каждого конкретного run для расследований;
- capability-side session state, которая может pause, expire, resume или требовать re-initialization.

Пакет по-прежнему намеренно маленький, но теперь он уже отражает, что governed runtime иногда обязан объяснять все три контура отдельно, не сливая их в один непрозрачный state object.

Это еще и полезный якорь для verifier-aware governance: если rollout или assurance зависят от eval output, runtime должен сохранять достаточно связей между trace, session и artifacts, чтобы объяснять не только что произошло, но и почему verifier оценил run именно так.

Это должно тянуться и в lifecycle handling. Governed reference runtime должен уметь объяснять, какой verifier contract и какая идентичность выпуска были активны для релиза, а также какие evidence еще нужно хранить после retirement, чтобы обосновывать прежние rollout или assurance decisions.

Теперь в нем отражен и четвертый operational concern: delegated authorization context, под которым вообще исполнялось действие. Этот контекст теперь появляется в run telemetry, approval records и session export, чтобы runtime мог объяснять не только что произошло, но и под чьей delegated identity и scope это произошло.

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
  В change gate теперь есть явный сигнал `failed_run_drill_checked`, чтобы review high-risk rollout не относился к деградировавшим путям как к чему-то вне проверки.
- [artifacts.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/artifacts.yaml)
- [runtime-controls.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/runtime-controls.yaml)
- [retirement.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/retirement.yaml)

Это уже не просто статические примеры. `config.py` умеет загружать эти YAML-файлы в identity агента, approved inventory, рантайм, context layers, хранилище памяти, политику выкладки, lifecycle-артефакты с идентичностью выпуска и другие элементы жизненного цикла, поэтому пакет стал ближе к реальному эксплуатационному каркасу.

При этом runtime-control bundle теперь задуман еще и как явное место для approval и session-governance правил, включая pause/resume, background handling, expiry, re-init policy, ownership capability sessions и границу между user run и capability-side session.

## Почему это полезно

Книга теперь опирается не только на текстовые объяснения, но и на реальный кодовый каркас:

- легче обсуждать архитектуру на уровне файлов и контрактов;
- легче расширять пакет следующими примерами;
- легче перейти от главы к исполняемому прототипу;
- легче показать путь, управляемый конфигурацией, а не только жестко зашитое демо;
- легче связать эталонный рантайм с главами про память, извлечение контекста, фоновые обновления и runtime-control governance;
- легче обсуждать, откуда взялся каждый memory record, какая у него ревизия и какая contract/runtime-control version была активна;
- легче держать на виду идентичность выпуска, verifier-contract lineage и retirement obligations рядом с runtime-control и artifact decisions;
- легче держать отдельно, но согласованно, approval state, runtime session state, capability session state и verifier evidence.

Отдельно полезно то, что теперь package можно не только запускать, но и инспектировать снаружи:

- `inspect-memory` показывает исходно загруженную память и фильтрацию по `tenant` и `memory_class`;
- `dump-events` показывает структурированную трассу одного запуска без чтения исходников;
- `export-events` сохраняет трассу в JSONL для разбора вне процесса;
- `export-events` умеет добавлять `schema_version` и делать export-time redaction по выбранным полям;
- `inspect-trace` позволяет читать и фильтровать сохраненные трассы;
- `replay-run` поднимает повторный прогон по `run_start` из сохраненной трассы.

Проще всего читать этот пакет так:

- книгу использовать для architecture, sequence и operating-model argument;
- этот пакет использовать для runnable structure, config surfaces и inspection examples;
- appendix schemas использовать, чтобы видеть contract boundaries, которые runtime пытается сделать явными.

## Что делать дальше

- [Схема трасс и каталог событий](trace-schema.md)
- [Схема наборов для оценки и правил проверки](eval-schema.md)
- [Схема набора политик и контракта подтверждения](policy-bundle-schema.md)
- [Схема артефактов жизненного цикла](lifecycle-artifact-schema.md)
- [Глава 17. Слой политик и каталог возможностей](../book/part-vii/chapter-17.md)
