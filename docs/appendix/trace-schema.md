# Схема трасс и каталог событий

Эта страница переводит разговор о наблюдаемости в практическую плоскость: к структуре событий, которую можно экспортировать, читать и использовать в оценочных сценариях.

Она опирается сразу на две части книги:

- [Глава 11. Трассы, спаны и структурированные события](../book/part-v/chapter-11.md)
- [Глава 13. Офлайн-оценки, онлайн-оценки и регрессионные шлюзы](../book/part-v/chapter-13.md)
- [Сквозная цепочка доказательств: от запроса к решению о rollout](../book/part-v/evidence-spine.md)

И на исполняемый пакет:

- [Эталонный пакет](reference-package.md)

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

В справочном рантайме часть этих полей пока живет внутри `payload`, чтобы схема оставалась компактной и читаемой. При этом сериализованное событие уже несет `schema_version` и `redacted_fields`, а экспорт умеет маскировать выбранные поля. Event loader явно проверяет эту форму: `Telemetry path must be a string or path-like object`, `Telemetry event line is not valid JSON: {line_number}`, `Telemetry event must be a mapping`, `Telemetry event is missing required field: {required_field}`, `Telemetry event field must be a string: {field}`, `Telemetry event field must not be empty: {field}`, `Telemetry schema version is not supported: {schema_version}`, `Telemetry event payload must be a mapping`, `Telemetry event payload key must be a string`, `Telemetry event payload key must not be empty`, `Telemetry event payload keys must be unique`, `Telemetry event payload value must be a string: {payload_key}`, `Telemetry event redacted_fields must be a tuple`, `Telemetry event redacted_fields must be a list`, `Telemetry event redacted_fields entries must be strings`, `Telemetry redact field must not be empty` и `Telemetry redact field is not present in events: {missing}`.

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

`dump-events`, `export-events` и `inspect-trace` также держат command response пригодным для triage, а не только raw JSONL dump: они показывают `session_id`, `tenant_id`, `principal_id`, `agent_id`, `authorization_mode`, `delegated_principal_id`, `delegated_scope`, `status`, `result`, `output_preview`, `failure_reason`, `approval_ids`, `approval_capability_names`, `pending_approval_ids`, `pending_approval_capability_names`, `approval_status_counts` и непустые `idempotency_keys` до того, как оператору придется вручную просматривать каждый `approval_requested` или `tool_execution` payload. `replay-run` затем отдельно возвращает `source_idempotency_keys` и `replay_idempotency_keys`, явно показывая, что replay — новый run со своим duplicate-write key, а не тихое повторное использование исходного write.

Trace replay валидирует эти evidence до того, как они могут стать seed для нового run: `Trace ID request must be a string`, `Trace ID not found in event file: {requested_trace_id}`, `Trace file does not contain any trace IDs`, `Trace file contains multiple trace IDs; pass --trace-id explicitly`, `Trace file does not contain a run_start event`, `Trace file contains multiple run_start events`, `Trace run_start event is missing replay fields: {missing_keys}`, `Trace run_start event has redacted replay fields: {redacted_keys}`, `Trace run_start replay field must be a string: {field}` и `Trace run_start replay field must not be empty: {field}`.

## Каталог событий справочного рантайма

Ниже текущий минимальный каталог событий.

| Event type | Когда появляется | Зачем нужен |
| --- | --- | --- |
| `run_start` | в начале запуска | фиксирует входные параметры и идентичность актора |
| `policy_precheck` | сразу после допуска запуска | фиксирует policy precheck action, reason и policy ID |
| `agent_threat_evidence` | когда threat-model control оставляет доказательство | связывает threat class с trace/evidence identifiers |
| `retrieval` | при извлечении memory context | фиксирует source и число retrieved records |
| `context_layers_built` | после сборки контекста | показывает, какие слои контекста реально попали в запуск; internally `RunContext` хранит `retrieved_context` и `retrieved_records` до обработки `tool_request` |
| `tool_policy_decision` | перед выполнением инструмента | фиксирует решение политики и причину allow/deny/approval |
| `mcp_tool_risk_review` | при review MCP tool/server риска | связывает threat class, registry evidence, scope review и quarantine state |
| `tool_execution` | после capability call или approval handoff | фиксирует capability status и tool-principal context |
| `a2a_handoff` | когда один agent делегирует работу другому agent | фиксирует delegation chain, authorization и failure-attribution context |
| `approval_requested` | при high-risk write path | показывает, что система ушла в очередь человеческой проверки |
| `sandbox_profile_reviewed` | при проверке sandbox-backed path | фиксирует review workspace, permissions и snapshot/resume evidence |
| `memory_write_decision` | перед фоновой записью памяти | фиксирует, разрешена или запрещена candidate memory write |
| `memory_persisted` | после фоновой записи | фиксирует происхождение и ревизию записи памяти |
| `background_compaction` | после background memory maintenance | фиксирует tenant-level compaction results |
| `background_update_scheduled` | после постановки или завершения background work | фиксирует background update status для запуска |
| `run_failed` | когда tool failure становится итогом запуска | сохраняет явную failed-run traceability |
| `governance_action` | когда telemetry signal запускает policy, containment, rollout или registry decision | связывает governance action record с trace evidence |
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

Для `agent_threat_evidence` полезно сохранять evidence markers из unified agent threat evidence model, чтобы threat rows можно было проверить по traces, а не только по prose:

- `prompt_boundary_event`
- `retrieval_source_id`
- `memory_record_id`
- `delegation_trace_id`
- `tenant_id`
- `cost_budget_event`
- `decision_trace_id`

Например, для `tool_policy_decision` минимальный `payload` обычно должен включать:

- `capability_name`
- `decision`
- `reason`
- `risk_tier`
- `tool_principal`

Для `mcp_tool_risk_review` production trace должен фиксировать MCP threat-model evidence, а не только итоговый allow/deny:

- `threat_class`
- `mcp_server_id`
- `capability_name`
- `tool_contract_version`
- `registry_owner`
- `scope_review`
- `quarantine_state`
- `evidence_refs`

`threat_class` лучше держать в словаре из MCP threat model: `tool poisoning`, `rug pull attack`, `tool shadowing`, `confused deputy`, `over-scoped tokens`, `data exfiltration through legitimate channels`, `supply-chain attack`, `replay/tampering`, `sandbox escape`.

Для `a2a_handoff` payload должен сохранять A2A handoff trust contract, а не только текст делегированного сообщения:

- `agent_identity`
- `delegation_chain`
- `allowed_collaboration_graph`
- `inter_agent_authorization`
- `policy_inheritance`
- `non_repudiation`
- `failure_attribution`

!!! example "Trace для duplicate-ticket thread"
    В support-triage кейсе события `tool_policy_decision`, `approval_requested`, `tool_execution` и финальный outcome должны связываться через один `trace_id`, `session_id`, `approval_id`, `tool_principal` и `idempotency_key`. Если `create_ticket` вернулся с timeout и статус side effect неизвестен, trace должен показать `side_effect_unknown`, а не маскировать run как успешный или повторять write без reconciliation.

!!! note "Canonical trace cases"
    Три canonical cases требуют разных trace emphases. **Support triage** связывает approval events, `idempotency_key`, tool side effects и duplicate-ticket recovery evidence. **Internal knowledge assistant** должен сохранять retrieval spans, memory access, source attribution, freshness checks и access control decisions. **Incident coordination** должен показывать escalation timeline, notification side effects, response ownership, handoff events и post-incident learning.

А для sandbox-backed run полезно заранее зарезервировать поля, которые связывают трассу с execution boundary:

- `sandbox_session_id`
- `sandbox_manifest_version`
- `sandbox_permissions_profile`
- `snapshot_id`
- `workspace_manifest_ref`

Если rollout или eval требует `sandbox_profile_review`, трасса должна также уметь ссылаться на review evidence, а не только на state fields:

- `sandbox_profile_contract`
- `workspace_entries_reviewed`
- `permissions_profile`
- `network_secrets_posture`
- `snapshot_policy`
- `reviewed_by`
- `review_evidence_refs`

Если система опирается на verifier-aware evals, полезно отдельно определить event или linked payload contract для verifier verdict record:

- `verdict_id`
- `verifier_id`
- `verifier_contract_version`
- `input_refs`
- `process_score`
- `outcome_score`
- `failure_attribution`
- `blocking_decision`
- `comparison_baseline`
- `reviewer_override`
- `evidence_refs`

А для `governance_action` полезно фиксировать поля governance action record, которые делают telemetry управленческим действием, а не просто dashboard-сигналом:

- `governance_action_id`
- `source_signal`
- `decision_owner`
- `action_state`
- `evidence_refs`
- `review_deadline`

`source_signal` лучше держать в ограниченном словаре, согласованном с governance-aware telemetry: `policy_decision_feedback`, `containment_decision`, `rollout_gate_input`, `incident_response_trigger`, `registry_update_signal`.

Для `memory_write_decision` в memory poisoning review трасса должна сохранять те же review fields, что и memory schema:

- `write_trust_boundary`
- `activation_policy`
- `contamination_scope`
- `policy_influence`
- `provenance_check`
- `quarantine_state`
- `rollback_ref`

А для `memory_persisted`:

- `memory_class`
- `kind`
- `provenance`
- `revision`

Текущие reference payloads также используют operational metadata fields: `runtime_principal`, `authorization_mode`, `delegated_principal_id`, `delegated_scope`, `policy_id`, `static_items`, `session_items`, `retrieved_items`, `tool_items`, `approval_id`, `reviewer`, `capability_session_id`, `capability_session_status`, `tool_status`, `output_preview`, `memory_id`, `revision_mode`, `compacted_records`, `persisted_records`, `tool_results`, `span_name`, and `duration_ms`. Tool request/result model validation относится к той же trace boundary: malformed tool calls падают с `Tool request capability name must be a string`, `Tool request capability name must not be empty`, `Tool request arguments must be a mapping`, `Tool request argument key must be a string`, `Tool request argument key must not be empty`, `Tool request argument keys must be unique`, `Tool request argument value must be a string: {argument_key}`, а malformed tool results падают с `Tool result status must be a string`, `Tool result status must not be empty`, `Tool result payload must be a mapping`, `Tool result payload key must be a string`, `Tool result payload key must not be empty`, `Tool result payload keys must be unique` и `Tool result payload value must be a string: {payload_key}`.

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
- sandbox state fields для runs, которые материализуют workspace, используют shell/filesystem capabilities или продолжаются из snapshot;
- event или linked payload для `sandbox_profile_reviewed`, чтобы rollout/eval evidence по workspace, permissions и snapshot/resume policy была traceable.

Именно эти вещи превращают поток событий из отладочного вывода в полноценный артефакт платформы.

## Что сделать сразу

Сначала пройди по короткому списку и отдельно отметь все ответы «нет»:

- Есть ли стабильный каталог событий?
- Есть ли разделение между `trace_id` и `session_id`?
- Понятно ли, какие поля обязательны для каждого типа событий?
- Можно ли по трассе восстановить решение политики и путь инструмента?
- Можно ли по экспорту сессии собирать набор для оценки?
- Можно ли связать трассу с verifier evidence, которое использовалось для grading или rollout review?
- Если rollout требует `sandbox_profile_review`, есть ли trace evidence для workspace entries, permissions и snapshot/resume policy?
- Можно ли понять, какая версия verifier contract породила этот grading output?
- Есть ли план по маскированию данных и версионированию схемы?

Если на несколько вопросов подряд ответ «нет», значит у тебя пока есть логирование, но еще нет полноценной схемы трасс.

## Что делать дальше

- [Схема наборов для оценки и правил проверки](eval-schema.md)
- [Схема набора политик и контракта подтверждения](policy-bundle-schema.md)
- [Схема артефактов жизненного цикла](lifecycle-artifact-schema.md)
- [Эталонный пакет](reference-package.md)
- [Глава 13. Офлайн-оценки, онлайн-оценки и регрессионные шлюзы](../book/part-v/chapter-13.md)
