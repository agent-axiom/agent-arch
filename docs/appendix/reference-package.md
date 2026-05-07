# Справочный пакет

В репозитории теперь есть небольшой исполняемый каркас: [agent_runtime_ref](https://github.com/agent-axiom/agent-arch/tree/main/agent_runtime_ref).

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

- [runtime.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/runtime.py)
  Основной `AgentRuntime`, который собирает контекст запуска, извлечение контекста, шаг модели, выполнение инструментов и хук фонового обновления.
- [policy.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/policy.py)
  Небольшой движок политик со структурированными решениями.
- [catalog.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/catalog.py)
  Реестр возможностей с описанием эксплуатационной семантики, risk tier и egress-контракта.
- [identity.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/identity.py)
  Явная identity агента и approved inventory возможностей, с которыми рантайм вообще имеет право работать.
- [config.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/config.py)
  Загрузчик YAML для identity агента, approved inventory, политик, каталога возможностей и политики выкладки.
- [memory.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/memory.py)
  Типизированные записи памяти, provenance, ревизии и in-memory-хранилище с изоляцией по тенантам.
- [background.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/background.py)
  Фоновый контур обслуживания для постоянных записей в память, provenance-aware сохранения и уплотнения.
- [execution.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/execution.py)
  Простой вызов возможностей через выполнение, учитывающее контракт, risk tier и egress policy.
- [telemetry.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/telemetry.py)
  In-memory-эмиттер телеметрии для структурированных событий и спанов.
- [rollout.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/rollout.py)
  Минимальный шлюз проверки готовности перед выкладкой.
- [controls.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/controls.py)
  Проверка continuous controls и inventory drift для approved registry.
- [approvals.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/approvals.py)
  Approval gates, pause/resume semantics, простая human review queue для high-risk действий и тот control surface, где approval state должен оставаться синхронизирован с capability session state.

Этот же runtime-control surface естественно расширяется и на delegated authorization assumptions: какой principal делегировал доступ, переживает ли такая авторизация pause/resume и что делает runtime, если delegated access отозвали до завершения действия.

- [lifecycle.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/lifecycle.py)
  Lifecycle-артефакты для change record, artifact bundle, записей об идентичности выпуска, runtime-control schemas, verifier-contract lineage и retirement plan, плюс readiness-проверки для этих состояний.

## Как запустить

```bash
.venv/bin/python -m agent_runtime_ref
```

Ожидаемый результат:

```json
{"agent_id": "support-triage-ref", "session_id": "session-demo-001", "result": "Ticket request is waiting for human approval (apr-001).", "status": "success", "failure_reason": "", "trace_id": "trace-demo-001", "events": 14, "memory_records": 4, "pending_approvals": 1, "config_dir": ".../agent_runtime_ref/configs"}
```

Явный запуск рантайма через подкоманду:

```bash
.venv/bin/python -m agent_runtime_ref simulate-run
.venv/bin/python -m agent_runtime_ref simulate-run --simulate-failure tool_timeout
```

Второй вариант специально добавлен как небольшой failure-rich сценарий. Он позволяет пакету показать, что даже разрешенная capability может завершиться как управляемый failed run с явной телеметрией, а не раствориться за общим happy path. `simulate-run` возвращает `agent_id`, `config_dir`, `trace_id`, `session_id`, `status`, `result`, `events`, `memory_records`, `pending_approvals` и опциональный `failure_reason`. Common identity and trace overrides включают `--config-dir`, `--agent-id`, `--tenant-id`, `--principal-id`, `--trace-id` и `--session-id`, чтобы examples можно было сделать deterministic без редактирования configs. Более специальные selectors включают `--limit` для memory inspection, `--approval-id` для approval closure, `--replay-trace-id` для trace replay, `--trace-prefix` для session commands и `--session-prefix` для eval dataset exports.

Просмотр identity агента и approved inventory:

```bash
.venv/bin/python -m agent_runtime_ref inspect-agent
```

`inspect-agent` возвращает `agent_id`, `display_name`, `owner_team`, `runtime_principal`, `approved_capabilities` и `catalog_capabilities`, чтобы inventory review мог сопоставить configured identity с capability catalog. Во встроенном `agent.yaml` эта identity принадлежит `agent_platform`, выполняется как `svc-support-triage-ref` и approved только для `search_docs` и `create_ticket`; capability catalog затем помечает `search_docs` как owned by `knowledge_platform` и связывает его с `svc-knowledge-reader`, а `create_ticket` как owned by `support_platform` и связывает с `svc-ticket-writer`. Каждая `catalog_capabilities` entry также несёт `name`, `owner`, `risk_tier`, `network_access`, `tool_principal` и `allowed_egress`, чтобы reviewers видели capability identity и egress posture в одном response. Identity/catalog loaders validate эту форму через ошибки вроде `'agent' must be a mapping`, `agent.id must be a string`, `agent.id is required`, `agent.display_name is required`, `agent.owner_team is required`, `agent.runtime_principal is required`, `'approved_capabilities' must be a list`, `Agent inventory config must be a mapping`, `Agent identity config must be a mapping`, `approved_capabilities entries must be strings`, `approved_capabilities entries must not be empty`, `approved_capabilities entries must be unique`, `approved_capabilities lookup must be a string`, `'capabilities' must be a mapping`, `Capability spec for {name!r} must be a mapping`, `Capability names must be strings`, `Capability name must not be empty`, `Capability names must be unique`, `Capability catalog entries must be CapabilitySpec`, `capabilities.{capability_name}.{key} must be a string`, `capabilities.{capability_name}.{key} is required`, `{label}.{key} must be a string`, `{label} must be a string` и `capabilities.{capability_name}.timeout_seconds must be positive`, `'{label}.{key}' must be an integer` и `'{label}.{key}' must be a boolean`, `{label}.approval must be a string`, `{label}.approval must not be empty`, `{label}.approval is not supported: {approval}`, `'allowed_egress' must be a list`, `allowed_egress entries must be strings`, `allowed_egress entries must not be empty` и `allowed_egress entries must be unique`.

Просмотр lifecycle-артефактов из Part VIII, включая runtime-control linkage и идентичность выпуска:

```bash
.venv/bin/python -m agent_runtime_ref inspect-lifecycle
.venv/bin/python -m agent_runtime_ref check-controls --signal policy_traces_present=false
.venv/bin/python -m agent_runtime_ref check-change --signal offline_eval_passed=false
.venv/bin/python -m agent_runtime_ref check-change --signal failed_run_drill_checked=false
.venv/bin/python -m agent_runtime_ref check-retirement --step revoke_egress=false
```

`inspect-lifecycle` теперь тоже показывает `sandbox_profile` из `runtime-controls.yaml`, включая `sandbox_profile.workspace_entries`, а также `artifact_bundle.review_evidence`, `artifact_bundle.sandbox_profile_review_evidence`, `change.affected_surfaces`, `change.required_signals`, `change.approval_roles`, `change.session_control_owner` (`support-ops`), `change.emergency_freeze_owner`, `artifact_bundle.session_control_owner`, `retirement.session_control_owner`, `retirement.emergency_freeze_owner`, `failed_run_archive_targets`, `controls.failed_run_control_expectations`, `controls.failed_run_control_domains`, `controls.failed_run_control_count`, `controls.failed_run_control_summary`, `controls.failed_run_control_status`, `controls.failed_run_control_review_required`, `controls.failed_run_control_owner`, `controls.failed_run_control_source`, `controls.failed_run_control_last_review`, `controls.failed_run_control_next_review` и `controls.failed_run_control_release_binding`, так что оператор видит в одном lifecycle summary ownership, freeze responsibility, retention и trace/provenance-контроль.
Та же runtime-control summary опирается на `runtime-controls.yaml`, включая `background_mode_allowed`, `capability_session_owner`, `capability_sessions`, `track_session_ids`, `resume_allowed`, `allow_progress_events`, `allow_elicitation`, `on_session_expiry: reinitialize_or_cancel`, `expiry_policy` и `expiry_signal_owner`, чтобы resumable capability sessions явно показывали progress, elicitation и expiry assumptions. Delegated-authorization defaults тоже явные: `authorization_mode` равен `user_delegated_or_platform_owned`, `delegated_principal_policy` — `explicit_principal_binding_required`, `token_reuse_policy` — `reuse_within_valid_paused_run_only`, `on_authorization_revoke` — `cancel_or_reapprove`, `subagent_inheritance` — `denied_by_default`, а resumable/reinit flows используют `resume_existing_session_if_valid`. Sandbox-profile loader валидирует эти runtime-control shapes ошибками `runtime_controls config must be a mapping`, `runtime_controls.sandbox_profile config must be a mapping`, `runtime_controls.sandbox_profile.{key} config must be a mapping`, `runtime_controls.sandbox_profile.workspace.entries must be a list`, а direct construction отвергает malformed sandbox roots через `Sandbox profile config must be a mapping`, malformed sandbox evidence values через `Sandbox profile {section}.{key} must be a string` или malformed workspace entries через `Sandbox profile workspace entries must be a list`.
`check-change` возвращает `change_id`, `ready`, `missing_signals`, `missing_failed_run_signals`, `rollout_strategy` и `risk_level`, чтобы пробелы degraded-path rollout review не прятались внутри общего списка missing signals.
Lifecycle list loaders reject malformed, blank, and duplicate entries with `{key} entries must be strings`, `{key} entries must not be empty`, and `{key} entries must be unique`. `check-retirement` возвращает `system_id`, `ready`, `missing_steps`, `failed_run_archive_targets` и `replacement_mode`, чтобы оператор видел, какие telemetry/session/approval records должны пережить retirement ради последующего degraded-path review.
`check-controls` возвращает `healthy`, `missing_controls`, `failed_run_controls`, `preserved_failed_run_controls`, `failed_run_controls_healthy`, `blocking_findings` и `inventory_drift`; вложенный объект `inventory_drift` показывает `has_drift`, `missing_from_catalog` и `missing_from_inventory`, чтобы trace/provenance-пробелы и capability inventory mismatches можно было разбирать отдельно от общей control hygiene. Его inputs в `controls.yaml` требуют `registry_reviewed`, `capability_owners_confirmed`, `memory_provenance_enforced` и `policy_traces_present`, with validation shapes `'controls' must be a mapping`, `'controls.require' must be a list`, `'controls.block_if' must be a list`, `{label} entries must be strings`, `{label} entries must not be empty` и `{label} entries must be unique`, а controls policy normalizes их в `required_controls`; `block_if` считает `direct_tool_access_present` и `unmanaged_runtime_present` жёсткими blockers и во время evaluation становится `blocked_findings`.

Просмотр записей памяти:

```bash
.venv/bin/python -m agent_runtime_ref inspect-memory --memory-class profile
```

`inspect-memory` теперь возвращает `config_dir`, `count` и `records`; каждая запись показывает не только содержимое, но и `provenance` с `revision`.
`dump-events` теперь возвращает `trace_id`, `status`, `result`, `event_count`, `events` и `failure_reason` в JSON-ответе для degraded-path drills.

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

`export-events` возвращает `output_path`, `trace_id`, `status`, `result`, `event_count`, `redact_fields` и опциональный `failure_reason`, чтобы redaction и degraded-path evidence были видны уже в command summary.

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

`inspect-trace` возвращает `trace_id`, `event_count` и `events`; `replay-run` возвращает `source_trace_id`, `replay_trace_id`, `status`, `result` и `event_count`, чтобы investigation и replay сохраняли source/run lineage.

Проверка политики выкладки с переопределением сигналов:

```bash
.venv/bin/python -m agent_runtime_ref check-rollout --signal offline_eval_pass=false
```

Rollout check возвращает `ready`, `missing_required`, `blocking_signals` и `rollout_mode`, чтобы automation отличала отсутствующие required evidence от явно блокирующих сигналов; signal overrides принимают boolean `key=value` pairs и отвергают неизвестный boolean text через `Unsupported boolean value in signal: {raw_signal!r}`. Runtime CLI failure paths также сохраняют стабильные operator-facing messages: `Config path must be a string or path-like object`, `Session output path must be a string or path-like object`, `Telemetry path must be a string or path-like object`, `CLI field must be a string: {field}`, `CLI field is required: {field}`, `CLI field entries must be a sequence: {field}`, `CLI field entries must be unique: {field}`, `Runtime request must be RunRequest`, `Run request field must be a string: {field}`, `Run request field is required: {field}`, `Delegated authorization field is required: {field}`, `Signal must be a string`, `Signal must use key=value format: {raw_signal!r}`, `Background request must be RunRequest`, `Background context must be RunContext`, `Background model_output must be ModelOutput`, `Background memory_store must be MemoryStore`, `Background policy must be PolicyEngine`, `Background telemetry must be TelemetryEmitter`, `Runtime catalog must be CapabilityCatalog`, `Runtime policy must be PolicyEngine`, `Runtime telemetry must be TelemetryEmitter`, `Runtime memory must be MemoryStore`, `Runtime approvals must be ApprovalQueue`, `Runtime sessions must be SessionStore`, `Runtime agent must be AgentIdentity`, `Runtime background must be BackgroundWorker`, `Approval queue policy must be ApprovalPolicy`, `Approval policy config must be a mapping`, `Capability catalog config must be a mapping`, `Controls policy config must be a mapping`, `Memory store config must be a mapping`, `Policy config must be a mapping`, `Rollout policy config must be a mapping`, `Telemetry event must be a mapping`, `Approval field must be a string: {field}`, `Approval field is required: {field}`, `Approval decision is not supported: {decision}`, `Policy action is not supported: {action}`, `Policy field must be a string: {field}`, `Policy field is required: {field}`, `Tool capability must be CapabilitySpec`, `Tool request must be ToolRequest`, `Tool policy decision must be PolicyDecision`, `Policy precheck request must be RunRequest`, `Policy context must be RunContext`, `Policy tool request must be ToolRequest`, `Policy capability must be CapabilitySpec`, `Tool request capability name must be a string`, `Tool request capability name must not be empty`, `Tool request arguments must be a mapping`, `Tool request argument key must be a string`, `Tool request argument key must not be empty`, `Tool request argument value must be a string: {argument_key}`, `Tool request capability does not match catalog entry: {capability_name} != {capability.name}`, `Tool result status must be a string`, `Tool result status must not be empty`, `Tool result payload must be a mapping`, `Tool result payload key must be a string`, `Tool result payload key must not be empty`, `Tool result payload keys must be unique`, `Tool result payload value must be a string: {payload_key}`, `Approval request not found: {approval_id}`, `Approval request is not pending: {approval_id}`, `No pending approval requests were generated for this run`, `Session field must be a string: {field}`, `Session field is required: {field}`, `Session status is not supported: {status}`, `Session tenant_id does not match existing session: {session_id}`, `Session principal_id does not match existing session: {session_id}`, `Session trace_id already exists: {trace_id}`, `Session field entries must be a sequence: {field}`, `Session field entries must be unique: {field}`, `Session field entries must be unique: session_id`, `Session runs must be a sequence`, `Session runs entries must be RunRecord`, `Session field entries must be a sequence: session_id`, `Session eval specs must be a mapping`, `Session not found: {session_id}`, `Telemetry event field must not be empty: event_type`, `Telemetry event field must not be empty: trace_id`, `Telemetry event field must not be empty: schema_version`, `Telemetry schema version is not supported: {schema_version}`, `Telemetry redact field must not be empty`, `Trace ID request must be a string`, `Trace ID not found in event file: {requested_trace_id}`, `Trace file contains multiple trace IDs; pass --trace-id explicitly`, `Trace file does not contain a run_start event` и `Model step must return ModelOutput`.

Проверка continuous controls и drift по реестру:

```bash
.venv/bin/python -m agent_runtime_ref check-controls --signal registry_reviewed=false
```

Просмотр и разрешение demo approval requests:

```bash
.venv/bin/python -m agent_runtime_ref inspect-approvals
.venv/bin/python -m agent_runtime_ref resolve-approval --decision approved --note "manager approved demo request"
.venv/bin/python -m agent_runtime_ref inspect-session
.venv/bin/python -m agent_runtime_ref inspect-session --simulate-failure tool_timeout
.venv/bin/python -m agent_runtime_ref session-eval-summary
.venv/bin/python -m agent_runtime_ref session-eval-summary --simulate-failure tool_timeout
.venv/bin/python -m agent_runtime_ref session-replay --user-input "Please create a ticket for this onboarding issue." --user-input "What language preference do you remember?"
.venv/bin/python -m agent_runtime_ref session-replay --simulate-failure tool_timeout --user-input "Please create a ticket for this issue."
.venv/bin/python -m agent_runtime_ref export-session --output artifacts/session-demo-001.json
.venv/bin/python -m agent_runtime_ref export-session --simulate-failure tool_timeout --output artifacts/session-demo-failed.json
.venv/bin/python -m agent_runtime_ref export-eval-dataset --output artifacts/eval-dataset.json
.venv/bin/python -m agent_runtime_ref export-eval-dataset --scenario failed_run_timeout --output artifacts/eval-failed-run.json
```

`inspect-approvals` теперь возвращает `trace_id`, `session_id`, `count` и `approvals`, включая capability-session lifecycle fields (`capability_session_id`, `capability_session_status`) и delegated authorization context: `authorization_mode`, `delegated_principal_id` и `delegated_scope`, так что review approval path можно напрямую сопоставить с session evidence. `resolve-approval` возвращает `approval_id`, `status`, `reviewer`, `resolution_note`, `capability_session_id`, `capability_session_status` и тот же delegated context после принятого решения, чтобы capability-session и acting-identity lineage не терялись на этапе closure.
`inspect-session` показывает session-level историю запусков и связанные `trace_id`. Теперь туда тоже можно инъецировать failed drill, а summary сохраняет `failed_runs`, `traceable_failed_runs`, `latest_failure_reason`, а также per-run поля `output_text`, `failure_reason`, `capability_session_id` и `capability_session_status`.
`session-eval-summary` возвращает короткую operational summary по серии запусков, включая и failed runs, и `traceable_failed_runs`, а не сводя все обратно только к успехам и отказам. Теперь туда можно напрямую инъецировать failed drill, а summary сразу показывает и `latest_failure_reason` для быстрого разбора.
`session-replay` позволяет прогнать несколько связанных запросов в одной `session_id`. Теперь туда тоже можно инъецировать failed drill, а replay summary сохраняет `failed_runs`, `traceable_failed_runs` и `latest_failure_reason` вместе с per-run полем `failure_reason`.
`export-session` сохраняет сессию как структурированный JSON, который уже можно использовать как seed для offline evals. Теперь он еще и сохраняет capability-session lifecycle fields (`capability_session_id`, `capability_session_status`) и delegated authorization context, включая `authorization_mode`, `delegated_principal_id` и `delegated_scope`, а в summary самой CLI-команды показывает `failed_runs`, `traceable_failed_runs` и `latest_failure_reason` для failed drills.

Session и eval команды явно показывают summary fields: `inspect-session` возвращает `session_id`, `tenant_id`, `principal_id`, `trace_count`, `latest_status`, `summary` и `runs`; `session-eval-summary` возвращает `session_id`, `total_runs`, `success_runs`, `approval_wait_runs`, `denied_runs`, `failed_runs`, `traceable_failed_runs`, `latest_status`, `latest_trace_id` и `latest_failure_reason`; `session-replay` возвращает `session_id`, `run_count`, `summary` и `runs`; `export-session` возвращает `output_path`, `session_id`, `total_runs`, `failed_runs`, `traceable_failed_runs`, `latest_trace_id` и `latest_failure_reason`; `export-eval-dataset` возвращает `dataset_name`, `output_path`, `session_count`, `run_count`, `failed_runs`, `traceable_failed_runs`, `latest_failure_reason` и `sessions`; по умолчанию `dataset_name` равен `agent-runtime-ref-eval-seed`, если caller не передал `--dataset-name`; eval export также валидирует внутренний seed `session_prefix` перед генерацией session IDs, а session commands валидируют внутренний seed `trace_prefix` перед генерацией trace IDs.

Теперь рантайм также считает tool paths с неуспешным исходом, например validation failure, полноценным итогом запуска. Вместо того чтобы делать вид, будто run завершился успешно, он фиксирует failed run, пишет явное событие `run_failed` и сохраняет и в session export, и в CLI output этот статус вместе с конкретной причиной сбоя в поле `failure_reason`.
`export-eval-dataset` собирает несколько встроенных session-сценариев в один eval-ready JSON artifact, включая отдельный failed-run drill scenario, profile lookup scenario `profile_memory` с labels `memory_read`, `profile_lookup` и `grounded_answer`, multi-run approval-plus-memory scenario `mixed_session` с labels `multi_run`, `approval_then_memory` и `session_evals`, плюс `required_run_count` как expected outcome, а также approval-backed сценарий `support_ticket` с label `sandbox_profile_review`, expected outcome `sandbox_profile_reviewed` и blocking `sandbox_profile_review` grading rule, а summary самой команды теперь тоже показывает агрегированные `failed_runs`, `traceable_failed_runs` и `latest_failure_reason`.

Этот eval path теперь полезно читать вместе с richer verifier contract из appendix: для long-horizon scenarios пакет должен помогать представить, как dataset со временем может нести `process_score`, `outcome_score`, `failure_attribution` и linked verifier evidence, а не только один тонкий verdict.

Вместе эти команды теперь помогают показать важное различие из Chapters 16 и 17:

- пользовательскую `session_id`, которая связывает несколько runs;
- `trace_id` каждого конкретного run для расследований;
- capability-side session state, которая может pause, expire, resume или требовать re-initialization.

Пакет по-прежнему намеренно маленький, но теперь он уже отражает, что governed runtime иногда обязан объяснять все три контура отдельно, не сливая их в один непрозрачный state object.

Это же место теперь полезно и как привязка для нового урока Anthropic про harness design: длинная application-работа может требовать явных context resets, структурированных handoff artifacts и разделения ролей planner/generator/evaluator, а не одного непрерывного agent loop. Справочный пакет не реализует такой harness целиком, но уже показывает те швы рантайма, в которых должны жить reset-safe handoff, sprint contracts, evaluator review и resumed control state.

Это еще и полезный якорь для verifier-aware governance: если rollout или assurance зависят от eval output, runtime должен сохранять достаточно связей между trace, session и artifacts, чтобы объяснять не только что произошло, но и почему verifier оценил run именно так.

Это должно тянуться и в lifecycle handling. Governed reference runtime должен уметь объяснять, какой verifier contract и какая идентичность выпуска были активны для релиза, какие evidence еще нужно хранить после retirement, чтобы обосновывать прежние rollout или assurance decisions, и какие структурированные handoff artifacts должны пережить context reset или role handoff, если именно они определяли, что retiring system было разрешено делать.

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

В [configs](https://github.com/agent-axiom/agent-arch/tree/main/agent_runtime_ref/configs) лежат стартовые файлы для рантайма и lifecycle:

- [agent.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/agent.yaml)
- [policy.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/policy.yaml)
- [capabilities.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/capabilities.yaml)
- [memory.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/memory.yaml)
- [rollout.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/rollout.yaml)
- [controls.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/controls.yaml)
- [approvals.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/approvals.yaml)
- [change.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/change.yaml)
  В change gate теперь есть явные сигналы `failed_run_drill_checked` и `sandbox_profile_reviewed`, чтобы review high-risk rollout не относился к деградировавшим путям или sandbox profile changes как к чему-то вне проверки.
- [artifacts.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/artifacts.yaml)
- [runtime-controls.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/runtime-controls.yaml)
- [retirement.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/retirement.yaml)

Это уже не просто статические примеры. `config.py` умеет загружать эти YAML-файлы в identity агента, approved inventory, рантайм, context layers, хранилище памяти, политику выкладки, lifecycle-артефакты с идентичностью выпуска и другие элементы жизненного цикла, поэтому пакет стал ближе к реальному эксплуатационному каркасу. Generic loaders также явно показывают malformed YAML shapes: `Config at {config_path!s} must be a mapping at the top level`, `{label} config must be a mapping` и `{key} must be a list`.

При этом runtime-control bundle теперь задуман еще и как явное место для approval и session-governance правил, включая pause/resume, background handling, expiry, re-init policy, ownership capability sessions и границу между user run и capability-side session.

### Минимальный sandbox profile

Если расширять пакет в сторону sandbox-backed execution, полезно начинать не с новой большой подсистемы, а с небольшого profile, который делает workspace и права явными:

```yaml
sandbox_profile:
  manifest_version: 1
  workspace:
    entries:
      - path: repo
        source: local_dir
        read_only: false
      - path: task.md
        source: inline_file
        read_only: true
  capabilities:
    filesystem: true
    shell: restricted
    memory: read_write
    skills: read_only
  permissions:
    network: denied
    secrets: none
    run_as: sandbox_user
  state:
    resume: allowed
    snapshot: required_on_completion
    persist_session_state: true
```

Такой пример не делает reference runtime полноценным sandbox orchestrator. Он фиксирует contract surface, который Chapters 9 и 16 требуют от настоящего sandbox-backed runtime: manifest, permissions, workspace materialization, session state и snapshot/resume policy должны быть видимыми для review.

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
- approval-backed `export-events` path пишет `sandbox_profile_reviewed`, чтобы trace evidence совпадал с lifecycle bundle и eval grading rule;
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
