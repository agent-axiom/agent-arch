# Схема трасс и каталог событий

Эта страница нужна для одного практического перехода: от разговора про наблюдаемость к структуре событий, которую можно реально экспортировать, читать и использовать в eval workflows.

Она опирается сразу на две части книги:

- [Глава 11. Трассы, спаны и структурированные события](../book/part-v/chapter-11.md)
- [Глава 13. Офлайн-оценки, онлайн-оценки и регрессионные шлюзы](../book/part-v/chapter-13.md)

И на исполняемый пакет:

- [Опорный пакет](reference-package.md)

## Зачем вообще нужна явная схема трасс

Если у команды нет явной схемы трасс, обычно происходит одно из двух:

- события есть, но они собраны как набор ad hoc JSON-полей;
- события вроде бы полезны для отладки, но плохо подходят для grading, audit и incident review.

Поэтому у production-grade agent system полезно отделять:

- `trace envelope`
- `event catalog`
- `payload contracts`

Даже если первый runtime еще маленький.

## Минимальный trace envelope

В `agent_runtime_ref` сейчас используется намеренно простой envelope:

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

На практике production schema почти всегда стоит расширять еще и так:

- `session_id`
- `agent_id`
- `tenant_id`
- `principal_id`
- `event_ts`
- `span_id`
- `parent_span_id`

В reference runtime часть этих полей пока живет внутри `payload`, чтобы схема оставалась компактной и легко читаемой. При этом сериализованный event уже несет `schema_version`, а export path умеет делать redaction выбранных полей.

## Как связаны trace и session

Для agent systems одной трассы обычно мало. Тебе почти всегда нужен еще и более длинный контекст:

- один `trace_id` описывает один run;
- одна `session_id` связывает несколько запусков в цепочку;
- session-level summary уже можно использовать для evals, rollout review и postmortem.

Именно поэтому package поддерживает:

- `inspect-trace`
- `inspect-session`
- `session-eval-summary`
- `export-session`
- `export-eval-dataset`

## Каталог событий reference runtime

Ниже текущий минимальный event catalog.

| Event type | Когда появляется | Зачем нужен |
| --- | --- | --- |
| `run_start` | в начале запуска | фиксирует входные параметры и идентичность актора |
| `context_layers_built` | после сборки контекста | показывает, какие context layers реально попали в run |
| `tool_policy_decision` | перед tool execution | фиксирует policy gate и причину allow/deny/approval |
| `approval_requested` | при high-risk write path | показывает, что система ушла в human review queue |
| `memory_persisted` | после background write | фиксирует provenance и revision memory record |
| `run_complete` | в конце запуска | замыкает run-level outcome |
| `span` | вокруг отдельных вызовов | дает простую latency и status telemetry |

Это не “идеальный универсальный каталог”. Это базовый рабочий словарь, на который уже можно опирать:

- trace inspection;
- regression seeds;
- session summaries;
- incident review.

## Что важно в payload contracts

Проблема не в том, что события “малоэмоциональные”. Проблема в том, что без контрактов payload быстро превращается в мусор.

Для каждого event type полезно заранее решить:

- какие поля обязательны;
- какие поля считаются stable;
- какие поля можно добавлять без поломки downstream tooling;
- какие поля нужны для grading;
- какие поля нужны для audit.

Например, для `tool_policy_decision` минимальный payload обычно должен включать:

- `capability_name`
- `decision`
- `reason`
- `risk_tier`
- `tool_principal`

А для `memory_persisted`:

- `memory_class`
- `kind`
- `provenance`
- `revision`

## Что уже умеет package

Практически это можно посмотреть так:

```bash
.venv/bin/python -m agent_runtime_ref dump-events
.venv/bin/python -m agent_runtime_ref export-events --output artifacts/trace-demo.jsonl
.venv/bin/python -m agent_runtime_ref export-events --output artifacts/trace-demo.jsonl --redact-field user_input
.venv/bin/python -m agent_runtime_ref inspect-trace --input artifacts/trace-demo.jsonl
.venv/bin/python -m agent_runtime_ref export-session --output artifacts/session-demo-001.json
.venv/bin/python -m agent_runtime_ref export-eval-dataset --output artifacts/eval-dataset.json
```

Это полезно потому, что один и тот же trace vocabulary начинает жить сразу в трех местах:

- в runtime;
- в книге;
- в eval-ready артефактах.

## Что стоит добавить в production schema

Reference runtime intentionally small, поэтому в более взрослой системе стоит почти сразу добавить:

- timestamp в каждом событии;
- явные `span_id` и `parent_span_id`;
- `run_id` как отдельный stable identifier;
- version поля для event schema;
- разделение `display payload` и `machine payload`;
- redaction rules для чувствительных полей.

Именно эти вещи превращают event stream из debug output в полноценный артефакт платформы.

## Практический чеклист

Если хочешь быстро понять, годится ли твоя trace schema уже не только для локальной отладки, пройди по вопросам:

- Есть ли стабильный event catalog?
- Есть ли разделение между `trace_id` и `session_id`?
- Понятно ли, какие поля обязательны для каждого event type?
- Можно ли по trace восстановить policy decision и tool path?
- Можно ли по session export собирать eval dataset?
- Есть ли plan на redaction и schema versioning?

Если на несколько вопросов подряд ответ “нет”, значит у тебя пока есть логирование, но еще нет нормальной trace schema.

## См. также

- [Схема eval datasets и grading contract](eval-schema.md)
- [Схема policy bundle и approval contract](policy-bundle-schema.md)
- [Схема lifecycle-артефактов](lifecycle-artifact-schema.md)
- [Опорный пакет](reference-package.md)
- [Глава 13. Офлайн-оценки, онлайн-оценки и регрессионные шлюзы](../book/part-v/chapter-13.md)
