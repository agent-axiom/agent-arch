# Схема трасс и каталог событий

Эта страница переводит разговор о наблюдаемости в практическую плоскость: к структуре событий, которую можно экспортировать, читать и использовать в оценочных сценариях.

Она опирается сразу на две части книги:

- [Глава 11. Трассы, спаны и структурированные события](../book/part-v/chapter-11.md)
- [Глава 13. Офлайн-оценки, онлайн-оценки и регрессионные шлюзы](../book/part-v/chapter-13.md)
- [Сквозная цепочка доказательств: от запроса к решению о раскатке](../book/part-v/evidence-spine.md)

И на исполняемый пакет:

- [Эталонный пакет](reference-package.md)

## Зачем вообще нужна явная схема трасс

Если у команды нет явной схемы трасс, обычно происходит одно из двух:

- события есть, но они собраны как разрозненный набор JSON-полей;
- события вроде бы полезны для отладки, но плохо подходят для оценки, аудита и разбора инцидентов.

Поэтому в промышленной агентной системе полезно отделять:

- оболочку трассы;
- каталог событий;
- контракты полезной нагрузки;
- контракт идентичности проверяющего;
- связь с доказательствами проверяющего.

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

В справочном рантайме часть этих полей пока живет внутри `payload`, чтобы схема оставалась компактной и читаемой. При этом сериализованное событие уже несет `schema_version` и `redacted_fields`, а экспорт умеет маскировать выбранные поля. Загрузчик событий явно проверяет эту форму: `Telemetry path must be a string or path-like object`, `Telemetry event line is not valid JSON: {line_number}`, `Telemetry event must be a mapping`, `Telemetry event is missing required field: {required_field}`, `Telemetry event field must be a string: {field}`, `Telemetry event field must not be empty: {field}`, `Telemetry schema version is not supported: {schema_version}`, `Telemetry event payload must be a mapping`, `Telemetry event payload key must be a string`, `Telemetry event payload key must not be empty`, `Telemetry event payload keys must be unique`, `Telemetry event payload value must be a string: {payload_key}`, `Telemetry event redacted_fields must be a tuple`, `Telemetry event redacted_fields must be a list`, `Telemetry event redacted_fields entries must be strings`, `Telemetry redact field must not be empty` и `Telemetry redact field is not present in events: {missing}`.
Для production observability поверх этого почти всегда нужны поля, которые делают spans searchable и пригодными для regression review:

- `span_type`
- `input_ref`
- `output_ref`
- `latency_ms`
- `retry_count`
- `token_input_count`
- `token_output_count`
- `token_cost`
- `approval_state`
- `pii_redacted`
- `redaction_policy_id`
- `retention_class`
- `trace_search_tags`

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

`dump-events`, `export-events` и `inspect-trace` также делают ответ команд пригодным для разбора, а не только сырым дампом JSONL: они показывают `session_id`, `tenant_id`, `principal_id`, `agent_id`, `authorization_mode`, `delegated_principal_id`, `delegated_scope`, `status`, `result`, `output_preview`, `failure_reason`, `approval_ids`, `approval_capability_names`, `pending_approval_ids`, `pending_approval_capability_names`, `approval_status_counts` и непустые `idempotency_keys` до того, как оператору придется вручную просматривать каждый `approval_requested` или `tool_execution` payload. `replay-run` затем отдельно возвращает `source_idempotency_keys` и `replay_idempotency_keys`, явно показывая, что повтор — новый запуск со своим ключом защиты от дублей записи, а не тихое повторное использование исходной операции записи.

Повтор трассы проверяет эти доказательства до того, как они могут стать исходным материалом для нового запуска: `Trace ID request must be a string`, `Trace ID not found in event file: {requested_trace_id}`, `Trace file does not contain any trace IDs`, `Trace file contains multiple trace IDs; pass --trace-id explicitly`, `Trace file does not contain a run_start event`, `Trace file contains multiple run_start events`, `Trace run_start event is missing replay fields: {missing_keys}`, `Trace run_start event has redacted replay fields: {redacted_keys}`, `Trace run_start replay field must be a string: {field}` и `Trace run_start replay field must not be empty: {field}`.

## Каталог событий справочного рантайма

Ниже текущий минимальный каталог событий.

| Event type | Когда появляется | Зачем нужен |
| --- | --- | --- |
| `run_start` | в начале запуска | фиксирует входные параметры и идентичность актора |
| `policy_precheck` | сразу после допуска запуска | фиксирует действие, причину и идентификатор политики предварительной проверки |
| `agent_threat_evidence` | когда средство контроля из модели угроз оставляет доказательство | связывает класс угрозы с идентификаторами трассы и доказательств |
| `retrieval` | при извлечении контекста памяти | фиксирует источник и число найденных записей |
| `context_layers_built` | после сборки контекста | показывает, какие слои контекста реально попали в запуск; внутри `RunContext` хранятся `retrieved_context` и `retrieved_records` до обработки `tool_request` |
| `tool_policy_decision` | перед выполнением инструмента | фиксирует решение политики и причину: разрешить, запретить или запросить подтверждение |
| `mcp_tool_risk_review` | при разборе риска инструмента или сервера MCP | связывает класс угрозы, доказательства из реестра, проверку области доступа и состояние карантина |
| `tool_execution` | после вызова возможности или передачи на подтверждение | фиксирует статус возможности и контекст принципала инструмента |
| `a2a_handoff` | когда один агент делегирует работу другому агенту | фиксирует цепочку делегирования, авторизацию и контекст атрибуции сбоя |
| `approval_requested` | при высокорисковом пути записи | показывает, что система ушла в очередь человеческой проверки |
| `sandbox_profile_reviewed` | при проверке пути на базе песочницы | фиксирует проверенное рабочее пространство, профиль разрешений и доказательства по снимкам и возобновлению |
| `memory_write_decision` | перед фоновой записью памяти | фиксирует, разрешена или запрещена кандидатная запись в память |
| `policy_precheck` | сразу после допуска запуска | фиксирует policy precheck action, reason и policy ID |
| `agent_threat_evidence` | когда threat-model control оставляет доказательство | связывает threat class с trace/evidence identifiers |
| `retrieval` | при извлечении memory context | фиксирует source и число retrieved records |
| `context_layers_built` | после сборки контекста | показывает, какие слои контекста реально попали в запуск; internally `RunContext` хранит `retrieved_context` и `retrieved_records` до обработки `tool_request` |
| `model_reasoning_evidence` | после model step, если provider/runtime вернул privacy-preserving reasoning evidence | связывает model output с summary/reference/encrypted artifact без хранения raw reasoning |
| `tool_policy_decision` | перед выполнением инструмента | фиксирует решение политики и причину allow/deny/approval |
| `mcp_tool_risk_review` | при review MCP tool/server риска | связывает threat class, registry evidence, scope review и quarantine state |
| `tool_execution` | после capability call или approval handoff | фиксирует capability status и tool-principal context |
| `a2a_handoff` | когда один agent делегирует работу другому agent | фиксирует delegation chain, authorization и failure-attribution context |
| `subagent_delegation_decision` | когда manager решает запускать или не запускать subagents | фиксирует fanout gate, budget и причину делегирования |
| `durable_agent_instance_state` | когда named agent instance загружается, засыпает, просыпается или сохраняет durable state | фиксирует owner instance, state version, wakeup и resumable stream linkage |
| `resumable_agent_recovery` | когда run продолжается после deploy/eviction/connection churn | фиксирует `continuation_id`, `last_durable_checkpoint`, `recovery_reason` и `client_tool_allowlist` |
| `approval_requested` | при high-risk write path | показывает, что система ушла в очередь человеческой проверки |
| `sandbox_profile_reviewed` | при проверке sandbox-backed path | фиксирует review workspace, permissions и snapshot/resume evidence |
| `memory_write_decision` | перед фоновой записью памяти | фиксирует, разрешена или запрещена candidate memory write |
| `memory_persisted` | после фоновой записи | фиксирует происхождение и ревизию записи памяти |
| `background_compaction` | после фонового обслуживания памяти | фиксирует результаты уплотнения на уровне арендатора |
| `background_update_scheduled` | после постановки или завершения фоновой работы | фиксирует статус фонового обновления для запуска |
| `verification_result` | когда запуск проверяет условие завершения | фиксирует условие остановки, актор проверки, команду или механизм проверки, статусы pass/fail/warning/blocked и ссылки на доказательства |
| `run_failed` | когда сбой инструмента становится итогом запуска | сохраняет явную трассируемость неуспешного запуска |
| `governance_action` | когда сигнал телеметрии запускает решение по политике, сдерживанию, раскатке или реестру | связывает запись управленческого действия с доказательствами трассы |
| `run_complete` | в конце запуска | фиксирует итог запуска |
| `span` | вокруг отдельных вызовов | дает простую телеметрию задержки и статуса |

Это не универсальный каталог на все случаи. Это базовый рабочий словарь, на который уже можно опирать:

В более зрелой промышленной схеме в этом словаре полезно сразу оставлять место и для доказательств с учетом проверяющего, чтобы трассы могли объяснять не только что сделал рантайм, но и на каких данных проверяющий оценил качество процесса, качество результата или атрибуцию сбоя.

- просмотр трасс;
- заготовки для регрессий;
- сводки по сессиям;
- разбор инцидентов.

## Что важно в контрактах полезной нагрузки

Проблема не в том, что события сухие. Проблема в том, что без контрактов `payload` быстро превращается в мусор.

Для каждого типа событий полезно заранее решить:

- какие поля обязательны;
- какие поля считаются стабильными;
- какие поля можно добавлять без поломки зависимых инструментов;
- какие поля нужны для оценки;
- какие поля нужны для аудита.

Для `agent_threat_evidence` полезно сохранять маркеры доказательств из единой модели доказательств угроз агенту (unified agent threat evidence model), чтобы строки угроз можно было проверить по трассам, а не только по объясняющему тексту:

- `prompt_boundary_event`
- `rejected_instruction_trace`
- `tool_output_sanitized`
- `untrusted_content_marker`
- `policy_decision_trace`
- `retrieval_source_id`
- `freshness_score`
- `quarantine_event`
- `memory_record_id`
- `validation_state`
- `rollback_replay_evidence`
- `tool_call_id`
- `approval_record`
- `argument_validation_result`
- `subject_id`
- `delegation_trace_id`
- `caller_callee_identity_check`
- `step_budget_event`
- `stop_reason`
- `escalation_decision`
- `tenant_id`
- `egress_decision`
- `redaction_dlp_result`
- `cost_budget_event`
- `rate_limit_decision`
- `circuit_breaker_state`
- `handoff_id`
- `containment_state`
- `verifier_verdict`
- `artifact_digest`
- `registry_decision`
- `sandbox_profile_id`
- `decision_trace_id`
- `immutable_log_pointer`
- `evidence_completeness_flag`

Например, для `tool_policy_decision` минимальный `payload` обычно должен включать:

- `capability_name`
- `decision`
- `reason`
- `risk_tier`
- `tool_principal`

Для `mcp_tool_risk_review` производственная трасса должна фиксировать доказательства модели угроз MCP (MCP threat-model evidence), а не только решение о разрешении или запрете (allow/deny): итоговое решение: разрешить или запретить:

- `threat_class`
- `mcp_server_id`
- `capability_name`
- `tool_contract_version`
- `registry_owner`
- `scope_review`
- `quarantine_state`
- `evidence_refs`

`threat_class` лучше держать в словаре модели угроз MCP (MCP threat model): `tool poisoning`, `rug pull attack`, `tool shadowing`, `confused deputy`, `over-scoped tokens`, `data exfiltration through legitimate channels`, `supply-chain attack`, `replay/tampering`, `sandbox escape`.
`threat_class` лучше держать в словаре из MCP threat model: `tool poisoning`, `rug pull attack`, `tool shadowing`, `confused deputy`, `over-scoped tokens`, `data exfiltration through legitimate channels`, `supply-chain attack`, `replay/tampering`, `sandbox escape`, `local control-plane crossing`.

`local control-plane crossing` нужен для сценария AutoJack-класса: недоверенный web content попадает в browser/tool agent, использует его локальную сетевую позицию, обращается к `localhost` MCP/debug/control socket и пытается превратить control-plane параметр в host command execution. Для такого события trace должен сохранять хотя бы:

- `untrusted_content_origin`
- `browser_tool_identity`
- `local_control_channel`
- `loopback_auth_result`
- `mcp_server_params_source`
- `executable_allowlist_result`
- `containment_action`

Для `a2a_handoff` payload должен сохранять контракт доверия для передачи управления A2A (A2A handoff trust contract), а не только текст делегированного сообщения:

- `agent_identity`
- `delegation_chain`
- `allowed_collaboration_graph`
- `inter_agent_authorization`
- `policy_inheritance`
- `non_repudiation`
- `failure_attribution`

!!! example "Трасса для цепочки дубля тикета"
    В кейсе разбора обращений поддержки события `tool_policy_decision`, `approval_requested`, `tool_execution` и финальный исход должны связываться через один `trace_id`, `session_id`, `approval_id`, `tool_principal` и `idempotency_key`. Если `create_ticket` вернулся с тайм-аутом и статус побочного эффекта неизвестен, трасса должна показать `side_effect_unknown`, а не маскировать запуск как успешный или повторять запись без сверки.
Для `subagent_delegation_decision` payload должен сохранять не только факт fanout, но и экономику решения:

- `subagent_count`
- `delegation_reason`
- `independence_assessment`
- `shared_context_need`
- `write_risk`
- `context_handoff_size`
- `token_budget`
- `tool_budget`
- `merge_conflict_risk`
- `fanout_decision`

Для `model_reasoning_evidence` payload должен различать наблюдаемость и приватность reasoning:

- `model_output_preview`
- `reasoning_summary`
- `reasoning_reference`
- `encrypted_reasoning_item`
- `tool_evidence_refs`
- `governance_access_path`

Сырой chain-of-thought или полный reasoning transcript не должен попадать в обычный trace export. Если расследованию нужен доступ к encrypted artifact, этот доступ должен идти через отдельный governance path с purpose, approval, retention и redaction/DLP checks.

Для `durable_agent_instance_state` payload должен показывать, что long-lived agent не является безымянным request handler:

- `agent_instance_id`
- `durable_state_version`
- `state_store`
- `scheduled_wakeup_id`
- `wakeup_reason`
- `resumable_stream_id`
- `connection_id`
- `idempotency_key`
- `state_transition`

!!! example "Trace для duplicate-ticket thread"
    В support-triage кейсе события `tool_policy_decision`, `approval_requested`, `tool_execution` и финальный outcome должны связываться через один `trace_id`, `session_id`, `approval_id`, `tool_principal` и `idempotency_key`. Если `create_ticket` вернулся с timeout и статус side effect неизвестен, trace должен показать `side_effect_unknown`, а не маскировать run как успешный или повторять write без reconciliation.

!!! note "Канонические сценарии трассировки"
    Три канонических сценария требуют разных акцентов трассировки. **Триаж обращений поддержки** связывает события подтверждений, `idempotency_key`, побочные эффекты инструментов и доказательства восстановления после дубля тикета. **Внутренний ассистент знаний** должен сохранять спаны поиска, доступ к памяти, привязку к источникам, проверки свежести и решения контроля доступа. **Координация инцидентов** должна показывать линию времени эскалации, побочные эффекты уведомлений, владение ответом, события передачи управления и обучение после инцидента.

Для пути на базе песочницы полезно заранее зарезервировать поля, которые связывают трассу с границей исполнения:

- `sandbox_session_id`
- `sandbox_manifest_version`
- `sandbox_permissions_profile`
- `snapshot_id`
- `workspace_manifest_ref`

Если для раскатки или оценки нужен `sandbox_profile_review`, трасса должна также уметь ссылаться на доказательства проверки, а не только на поля состояния:

- `sandbox_profile_contract`
- `workspace_entries_reviewed`
- `permissions_profile`
- `network_secrets_posture`
- `snapshot_policy`
- `reviewed_by`
- `review_evidence_refs`

Если система опирается на оценки с учетом проверяющего, полезно отдельно определить событие, контракт данных или связанный payload для записи вердикта проверяющего (verifier verdict record):

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

А для `governance_action` полезно фиксировать поля записи управленческого действия, которые делают телеметрию управленческим действием, а не просто сигналом панели:

- `governance_action_id`
- `source_signal`
- `decision_owner`
- `action_state`
- `evidence_refs`
- `review_deadline`

`source_signal` лучше держать в ограниченном словаре, согласованном с управленческой телеметрией: `policy_decision_feedback`, `containment_decision`, `rollout_gate_input`, `incident_response_trigger`, `registry_update_signal`.

Для `memory_write_decision` при проверке отравления памяти трасса должна сохранять те же поля проверки отравления памяти, что и схема памяти:

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

Текущие эталонные полезные нагрузки также используют операционные метаданные: `runtime_principal`, `authorization_mode`, `delegated_principal_id`, `delegated_scope`, `policy_id`, `static_items`, `session_items`, `retrieved_items`, `tool_items`, `approval_id`, `reviewer`, `capability_session_id`, `capability_session_status`, `tool_status`, `output_preview`, `memory_id`, `revision_mode`, `compacted_records`, `persisted_records`, `tool_results`, `span_name` и `duration_ms`. Проверка модели запросов и результатов инструмента относится к той же границе трассировки: неправильные обращения к инструменту падают с `Tool request capability name must be a string`, `Tool request capability name must not be empty`, `Tool request arguments must be a mapping`, `Tool request argument key must be a string`, `Tool request argument key must not be empty`, `Tool request argument keys must be unique`, `Tool request argument value must be a string: {argument_key}`, а неправильные результаты инструмента падают с `Tool result status must be a string`, `Tool result status must not be empty`, `Tool result payload must be a mapping`, `Tool result payload key must be a string`, `Tool result payload key must not be empty`, `Tool result payload keys must be unique` и `Tool result payload value must be a string: {payload_key}`.
Текущие reference payloads также используют operational metadata fields: `runtime_principal`, `authorization_mode`, `delegated_principal_id`, `delegated_scope`, `policy_id`, `static_items`, `session_items`, `retrieved_items`, `tool_items`, `approval_id`, `reviewer`, `capability_session_id`, `capability_session_status`, `tool_status`, `output_preview`, `model_output_preview`, `reasoning_summary`, `reasoning_reference`, `encrypted_reasoning_item`, `memory_id`, `revision_mode`, `compacted_records`, `persisted_records`, `tool_results`, `span_name`, `duration_ms`, `span_type`, `input_ref`, `output_ref`, `latency_ms`, `retry_count`, `token_input_count`, `token_output_count`, `token_cost`, `approval_state`, `pii_redacted`, `redaction_policy_id`, `retention_class`, `trace_search_tags`, `subagent_count`, `delegation_reason`, `context_handoff_size`, `token_budget`, `merge_conflict_risk`, `agent_instance_id`, `durable_state_version`, `scheduled_wakeup_id` and `resumable_stream_id`. Tool request/result/model validation относится к той же trace boundary: malformed model outputs падают с `Model output reasoning_summary must be a string`, `Model output reasoning_reference must be a string` или `Model output encrypted_reasoning_item must be a string`; malformed tool calls падают с `Tool request capability name must be a string`, `Tool request capability name must not be empty`, `Tool request arguments must be a mapping`, `Tool request argument key must be a string`, `Tool request argument key must not be empty`, `Tool request argument keys must be unique`, `Tool request argument value must be a string: {argument_key}`, а malformed tool results падают с `Tool result status must be a string`, `Tool result status must not be empty`, `Tool result payload must be a mapping`, `Tool result payload key must be a string`, `Tool result payload key must not be empty`, `Tool result payload keys must be unique` и `Tool result payload value must be a string: {payload_key}`.

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

- временную метку в каждом событии;
- явные `span_id` и `parent_span_id`;
- `run_id` как отдельный стабильный идентификатор;
- версионирование схемы событий;
- разделение отображаемой и машинной полезной нагрузки;
- правила маскирования чувствительных полей;
- явный способ связывать трассы с доказательствами проверяющего, снимками экрана или артефактами оценивания;
- поля `stop_condition`, `verification_command`, `verification_result`, `verifier_actor` и `evidence_refs` для проверяемого завершения запуска;
- стабильный способ фиксировать, какая версия контракта проверяющего породила результат оценивания;
- поля состояния песочницы для запусков, которые материализуют рабочую область, используют возможности оболочки или файловой системы либо продолжаются из снимка состояния;
- событие или связанная полезная нагрузка для `sandbox_profile_reviewed`, чтобы доказательства раскатки и оценки по рабочей области, правам и политике снимков/возобновления были прослеживаемыми.
- стабильный способ фиксировать, какая версия verifier contract породила grading output;
- sandbox state fields для runs, которые материализуют workspace, используют shell/filesystem capabilities или продолжаются из snapshot;
- event или linked payload для `sandbox_profile_reviewed`, чтобы rollout/eval evidence по workspace, permissions и snapshot/resume policy была traceable.
- fanout fields для subagent delegation: `subagent_count`, `delegation_reason`, `context_handoff_size`, `token_budget`, `tool_budget` и `merge_conflict_risk`.
- privacy-preserving reasoning fields: `reasoning_summary`, `reasoning_reference`, `encrypted_reasoning_item` и `model_output_preview`, но не raw reasoning transcript.
- durable named-agent fields: `agent_instance_id`, `durable_state_version`, `scheduled_wakeup_id` и `resumable_stream_id`, чтобы session export связывал run с long-lived actor state.
- recovery fields: `continuation_id`, `last_durable_checkpoint`, `recovery_reason` и `client_tool_allowlist`, чтобы deploy/eviction/connection churn не превращались в потерянный run или неявно расширенную делегацию.

Именно эти вещи превращают поток событий из отладочного вывода в полноценный артефакт платформы.

## Что сделать сразу

Сначала пройди по короткому списку и отдельно отметь все ответы «нет»:

- Есть ли стабильный каталог событий?
- Есть ли разделение между `trace_id` и `session_id`?
- Понятно ли, какие поля обязательны для каждого типа событий?
- Можно ли по трассе восстановить решение политики и путь инструмента?
- Можно ли по экспорту сессии собирать набор для оценки?
- Можно ли связать трассу с доказательствами проверяющего, которые использовались для оценивания или разбора раскатки?
- Есть ли событие или payload, где видно, какое условие завершения проверялось, кем и с каким результатом?
- Если раскатка требует `sandbox_profile_review`, есть ли доказательства в трассе для записей рабочей области, прав и политики снимков/возобновления?
- Можно ли понять, какая версия контракта проверяющего породила этот результат оценивания?
- Если rollout требует `sandbox_profile_review`, есть ли trace evidence для workspace entries, permissions и snapshot/resume policy?
- Если manager запускает subagents, видно ли по traces, почему fanout был разрешен, каким был budget и насколько рискован merge?
- Если trace содержит reasoning evidence, хранится ли только summary/reference/encrypted pointer, а не сырой chain-of-thought?
- Если агент является durable named instance, видно ли по trace/session export, какое состояние было загружено, чем оно изменилось и какой wake/resume path продолжил работу?
- Можно ли понять, какая версия verifier contract породила этот grading output?
- Есть ли план по маскированию данных и версионированию схемы?

Если на несколько вопросов подряд ответ «нет», значит у тебя пока есть логирование, но еще нет полноценной схемы трасс.

## Что делать дальше

- [Схема наборов для оценки и правил проверки](eval-schema.md)
- [Схема набора политик и контракта подтверждения](policy-bundle-schema.md)
- [Схема артефактов жизненного цикла](lifecycle-artifact-schema.md)
- [Эталонный пакет](reference-package.md)
- [Глава 13. Офлайн-оценки, онлайн-оценки и регрессионные шлюзы](../book/part-v/chapter-13.md)
