# Схема трасс и каталог событий

Эта страница переводит разговор о наблюдаемости в практическую плоскость: к структуре событий, которую можно экспортировать, читать и использовать в оценочных сценариях.

Она опирается сразу на две части книги:

- [Глава 11. Трассы, спаны и структурированные события](../book/part-v/chapter-11.md)
- [Глава 13. Офлайн-оценки, онлайн-оценки и регрессионные шлюзы](../book/part-v/chapter-13.md)
- [Сквозная цепочка доказательств: от запроса к решению о rollout](../book/part-v/evidence-spine.md)

И на исполняемый пакет:

- [Справочный пакет](reference-package.md)

## Зачем вообще нужна явная схема трасс

Если у команды нет явной схемы трасс, обычно происходит одно из двух:

- события есть, но они собраны как набор ad hoc JSON-полей;
- события вроде бы полезны для отладки, но плохо подходят для оценки, аудита и разбора инцидентов.

Поэтому в промышленной агентной системе полезно отделять:

- оболочку трассы;
- каталог событий;
- контракты полезной нагрузки;
- identity verifier contract;
- verifier evidence linkage.

Даже если первый рантайм еще маленький.

## Минимальная оболочка трассы

В `agent_runtime_ref` сейчас используется намеренно простая оболочка:

```json
{
  "event_type": "run_start",
  "trace_id": "trace-demo-001",
  "payload": {
    "agent_id": "support-triage-ref",
    "tenant_id": "tenant-acme",
    "principal_id": "user-42",
    "session_id": "session-demo-001",
    "user_input": "Please create a ticket for this onboarding issue."
  }
}
```

Минимально полезный набор полей такой:

- `event_type`
- `trace_id`
- `payload`

На практике промышленную схему почти всегда стоит расширять еще и так:

- `session_id`
- `agent_id`
- `tenant_id`
- `principal_id`
- `event_ts`
- `span_id`
- `parent_span_id`

В справочном рантайме часть этих полей пока живет внутри `payload`, чтобы схема оставалась компактной и читаемой. При этом сериализованное событие уже несет `schema_version`, а экспорт умеет маскировать выбранные поля.

## Как связаны трасса и сессия

Для агентных систем одной трассы обычно мало. Почти всегда нужен и более длинный контекст:

- один `trace_id` описывает один запуск;
- одна `session_id` связывает несколько запусков в цепочку;
- сводку по сессии уже можно использовать для оценок, проверки раскатки и постмортема.

Именно поэтому пакет поддерживает:

- `inspect-trace`
- `inspect-session`
- `session-eval-summary`
- `export-session`
- `export-eval-dataset`

## Каталог событий справочного рантайма

Ниже текущий минимальный каталог событий.

| Event type | Когда появляется | Зачем нужен |
| --- | --- | --- |
| `run_start` | в начале запуска | фиксирует входные параметры и идентичность актора |
| `context_layers_built` | после сборки контекста | показывает, какие слои контекста реально попали в запуск |
| `tool_policy_decision` | перед выполнением инструмента | фиксирует решение политики и причину allow/deny/approval |
| `approval_requested` | при high-risk write path | показывает, что система ушла в очередь человеческой проверки |
| `memory_persisted` | после фоновой записи | фиксирует происхождение и ревизию записи памяти |
| `run_complete` | в конце запуска | фиксирует итог запуска |
| `span` | вокруг отдельных вызовов | дает простую телеметрию задержки и статуса |

Это не универсальный каталог на все случаи. Это базовый рабочий словарь, на который уже можно опирать:

В более зрелой production-схеме в этом словаре полезно сразу оставлять место и для verifier-aware evidence, чтобы трассы могли объяснять не только что сделал runtime, но и на каких данных verifier оценил process quality, outcome quality или failure attribution.

- просмотр трасс;
- заготовки для регрессий;
- сводки по сессиям;
- разбор инцидентов.

## Что важно в контрактах полезной нагрузки

Проблема не в том, что события сухие. Проблема в том, что без контрактов `payload` быстро превращается в мусор.

Для каждого типа событий полезно заранее решить:

- какие поля обязательны;
- какие поля считаются стабильными;
- какие поля можно добавлять без поломки downstream tooling;
- какие поля нужны для оценки;
- какие поля нужны для аудита.

Например, для `tool_policy_decision` минимальный `payload` обычно должен включать:

- `capability_name`
- `decision`
- `reason`
- `risk_tier`
- `tool_principal`

А для sandbox-backed run полезно заранее зарезервировать поля, которые связывают трассу с execution boundary:

- `sandbox_session_id`
- `sandbox_manifest_version`
- `sandbox_permissions_profile`
- `snapshot_id`
- `workspace_manifest_ref`

Если система опирается на verifier-aware evals, полезно отдельно определить event или linked payload contract и для verifier evidence, например:

- `verifier_id`
- `verifier_contract_version`
- `process_score`
- `outcome_score`
- `failure_attribution`
- `evidence_refs`

А для `memory_persisted`:

- `memory_class`
- `kind`
- `provenance`
- `revision`

## Что уже умеет пакет

Практически это можно посмотреть так:

```bash
.venv/bin/python -m agent_runtime_ref dump-events
.venv/bin/python -m agent_runtime_ref export-events --output artifacts/trace-demo.jsonl
.venv/bin/python -m agent_runtime_ref export-events --output artifacts/trace-demo.jsonl --redact-field user_input
.venv/bin/python -m agent_runtime_ref inspect-trace --input artifacts/trace-demo.jsonl
.venv/bin/python -m agent_runtime_ref export-session --output artifacts/session-demo-001.json
.venv/bin/python -m agent_runtime_ref export-eval-dataset --output artifacts/eval-dataset.json
```

Это полезно потому, что один и тот же словарь трасс начинает жить сразу в трех местах:

- в рантайме;
- в книге;
- в артефактах для оценки.

## Что стоит добавить в промышленную схему

Справочный рантайм намеренно небольшой, поэтому в более зрелой системе стоит почти сразу добавить:

- timestamp в каждом событии;
- явные `span_id` и `parent_span_id`;
- `run_id` как отдельный стабильный идентификатор;
- версионирование схемы событий;
- разделение `display payload` и `machine payload`;
- правила маскирования чувствительных полей;
- явный способ связывать трассы с verifier evidence, screenshots или grading artifacts;
- стабильный способ фиксировать, какая версия verifier contract породила grading output;
- sandbox state fields для runs, которые материализуют workspace, используют shell/filesystem capabilities или продолжаются из snapshot.

Именно эти вещи превращают поток событий из отладочного вывода в полноценный артефакт платформы.

## Что сделать сразу

Сначала пройди по короткому списку и отдельно отметь все ответы «нет»:

- Есть ли стабильный каталог событий?
- Есть ли разделение между `trace_id` и `session_id`?
- Понятно ли, какие поля обязательны для каждого типа событий?
- Можно ли по трассе восстановить решение политики и путь инструмента?
- Можно ли по экспорту сессии собирать набор для оценки?
- Можно ли связать трассу с verifier evidence, которое использовалось для grading или rollout review?
- Можно ли понять, какая версия verifier contract породила этот grading output?
- Есть ли план по маскированию данных и версионированию схемы?

Если на несколько вопросов подряд ответ «нет», значит у тебя пока есть логирование, но еще нет полноценной схемы трасс.

## Что делать дальше

- [Схема наборов для оценки и правил проверки](eval-schema.md)
- [Схема набора политик и контракта подтверждения](policy-bundle-schema.md)
- [Схема артефактов жизненного цикла](lifecycle-artifact-schema.md)
- [Справочный пакет](reference-package.md)
- [Глава 13. Офлайн-оценки, онлайн-оценки и регрессионные шлюзы](../book/part-v/chapter-13.md)
