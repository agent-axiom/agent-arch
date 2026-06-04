# Эталонный пакет

В репозитории теперь есть небольшой исполняемый каркас: [agent_runtime_ref](https://github.com/agent-axiom/agent-arch/tree/main/agent_runtime_ref).

Его задача не в том, чтобы стать промышленным фреймворком. Он нужен как минимальная кодовая опора для **частей VII и VIII** книги.

Этот пакет намеренно задуман как практическая опора реализации, а не как параллельный продукт. Его ценность в том, что читатель может посмотреть на работающую структуру системы, которая стоит за аргументом книги, не превращая проект в руководство по фреймворку.

Чего эта страница **не** обещает:

- она не заменяет книжное объяснение того, зачем вообще существуют эти слои;
- она не должна быть главным местом, где читатель разбирается в архитектурных компромиссах;
- она не пытается превратить репозиторий в универсальный фреймворк для агентов.

Здесь собран полный разбор пакета: командный интерфейс, конфигурации, структура и связь с книгой. Чтобы первый экран не превращался в справочник по среде выполнения, читай страницу по слоям:

- **Быстрый запуск** — раздел «Как запустить» и первые команды.
- **Минимальная архитектурная карта** — раздел «Что внутри».
- **Контракты конфигов** — раздел «Примерные конфиги».
- **Расширенные детали жизненного цикла и контроля** — разделы проверки и инспекции жизненного цикла ниже.
- **Ссылки на исходники** — списки файлов в `agent_runtime_ref`.

!!! summary "Маршрут чтения"
    Используй эту страницу как карту, а не как последовательную главу: **Быстрый запуск** для первого запуска, **Архитектурная карта** для понимания слоев, **Примеры команд** для воспроизводимых действий, **Контракты конфигураций** для проверки настроек, **Расширенный контроль жизненного цикла** для сценариев части VIII и **Внутреннее устройство среды выполнения** только когда нужно сверить конкретный модуль.

Практичный маршрут чтения такой:

- глава 16 для базовой среды выполнения и состояния сессии возможности;
- глава 17 для слоя политик и контрактов возможностей;
- [сквозная цепочка доказательств](../book/part-v/evidence-spine.md) для записи от запроса до решения о поэтапном выпуске;
- глава 18 для шлюзов поэтапного выпуска вокруг подтверждений и поведения среды выполнения;
- глава 21 для ответа контура заверения;
- глава 22 и схема жизненного цикла для связи управляемых артефактов, идентичности выпуска, цепочки проверочного контракта и происхождения делегированного разрешения;
- главы 23-27 для прерывания, истечения срока, повторной инициализации, вывода из эксплуатации, наблюдаемости, владения реестром, обязательств по доказательствам проверки и управления жизненным циклом делегированного разрешения вокруг сессий возможностей.

!!! example "Опора выполнения для триажа обращений поддержки"
    Встроенный `support-triage-ref` показывает тот же сквозной случай в исполняемой форме: идентичность агента, одобренные возможности `search_docs`/`create_ticket`, ожидание подтверждения, идентификаторы трассы и сессии, проверки жизненного цикла и экспорт оценки. Поэтому цепочку с дублем тикета из книги можно проверять не только как текстовое описание, но и как исполняемую поверхность контракта.

!!! note "Каноническая область выполнения сценариев"
    Эталонный пакет исполняет **Триаж обращений поддержки** как исполняемую базовую линию для записывающих возможностей, подтверждений и восстановления после дубля тикета. **Внутренний ассистент знаний** и **Координация инцидентов** остаются контрольными линзами покрытия для той же архитектуры: первый проверяет поиск, память, свежесть и происхождение знаний, второй — трассы, эскалацию, побочные эффекты уведомлений, владение ответом и обучение после инцидента. Если добавлять их как исполняемые конфигурации, они должны повторять те же контракты политик, телеметрии, жизненного цикла и реестра, а не становиться отдельными демонстрациями.

Недавние обновления контрактов делают эту поверхность полезнее для проверки: контекст делегированного разрешения сохраняется через командные демонстрации, сессии, экспорты оценок и повторные прогоны; обезличивание экспорта трасс теперь покрывает сводки команд вместе с артефактами JSONL; инспекция жизненного цикла показывает предположения управления средой выполнения; а защита документации фиксирует стабильные ошибки валидации, задающие эти границы.

## Что внутри

- [runtime.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/runtime.py)
  Основной `AgentRuntime`, который собирает контекст запуска, извлечение контекста, шаг модели, выполнение инструментов и точку подключения фонового обновления.
- [policy.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/policy.py)
  Небольшой движок политик со структурированными решениями.
- [catalog.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/catalog.py)
  Реестр возможностей с описанием эксплуатационной семантики, уровня риска и контракта исходящего обмена.
- [identity.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/identity.py)
  Явная идентичность агента и утвержденный инвентарь возможностей, с которыми среда выполнения вообще имеет право работать.
- [config.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/config.py)
  Загрузчик YAML для идентичности агента, утвержденного инвентаря, политик, каталога возможностей и политики выкладки.
- [memory.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/memory.py)
  Типизированные записи памяти, происхождение, ревизии и хранилище в памяти процесса с изоляцией по арендаторам.
- [background.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/background.py)
  Фоновый контур обслуживания для постоянных записей в память, сохранения с учетом происхождения и уплотнения.
- [execution.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/execution.py)
  Простой вызов возможностей через выполнение, учитывающее контракт, уровень риска и политику исходящего обмена.
- [telemetry.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/telemetry.py)
  Эмиттер телеметрии в памяти процесса для структурированных событий и отрезков выполнения.
- [rollout.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/rollout.py)
  Минимальный шлюз проверки готовности перед выкладкой.
- [controls.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/controls.py)
  Проверка непрерывных контролей и расхождения инвентаря с утвержденным реестром.
- [approvals.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/approvals.py)
  Шлюзы подтверждения, семантика паузы/возобновления, простая очередь человеческой проверки для действий высокого риска и та поверхность управления, где состояние подтверждения должно оставаться синхронизированным с состоянием сессии возможности.

Эта же поверхность управления средой выполнения естественно расширяется и на предположения делегированного разрешения: какой субъект делегировал доступ, переживает ли такая авторизация паузу/возобновление и что делает среда выполнения, если делегированный доступ отозвали до завершения действия.

- [lifecycle.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/lifecycle.py)
  Артефакты жизненного цикла для записи изменения, набора артефактов, записей об идентичности выпуска, схем управления средой выполнения, цепочки проверочного контракта и плана вывода из эксплуатации, плюс проверки готовности для этих состояний.

## Как запустить

```bash
.venv/bin/python -m agent_runtime_ref
```

Ожидаемый результат:

```json
{"agent_id": "support-triage-ref", "request_agent_id": "support-triage-ref", "session_id": "session-demo-001", "tenant_id": "tenant-acme", "principal_id": "user-42", "authorization_mode": "platform_owned", "delegated_principal_id": "", "delegated_scope": "", "result": "Ticket request is waiting for human approval (apr-001).", "status": "success", "failure_reason": "", "trace_id": "trace-demo-001", "idempotency_keys": ["trace-demo-001"], "approval_ids": ["apr-001"], "approval_capability_names": ["create_ticket"], "approval_status_counts": {"pending": 1}, "event_types": ["run_start", "policy_precheck", "retrieval", "context_layers_built", "span", "tool_policy_decision", "approval_requested", "sandbox_profile_reviewed", "tool_execution", "memory_write_decision", "memory_persisted", "background_compaction", "background_update_scheduled", "run_complete"], "events": 14, "memory_records": 4, "memory_record_ids": ["mem-001", "mem-002", "mem-003", "mem-004"], "pending_approvals": 1, "pending_approval_ids": ["apr-001"], "pending_approval_capability_names": ["create_ticket"], "config_dir": ".../agent_runtime_ref/configs"}
```

Явный запуск рантайма через подкоманду:

```bash
.venv/bin/python -m agent_runtime_ref simulate-run
.venv/bin/python -m agent_runtime_ref simulate-run --simulate-failure tool_timeout
```

Второй вариант специально добавлен как сценарий с явным отказом. Он позволяет пакету показать, что даже разрешенная возможность может завершиться как управляемый неудачный запуск с явной телеметрией, а не раствориться за общим успешным путем. `simulate-run` возвращает `agent_id`, `request_agent_id`, `config_dir`, `trace_id`, `idempotency_keys`, `approval_ids`, `approval_capability_names`, `pending_approval_ids`, `pending_approval_capability_names`, `approval_status_counts`, `event_types`, `session_id`, `tenant_id`, `principal_id`, `authorization_mode`, `delegated_principal_id`, `delegated_scope`, `status`, `result`, `events`, `memory_records`, `memory_record_ids`, `pending_approvals`, `pending_approval_ids`, `pending_approval_capability_names` и опциональный `failure_reason`. Общие переопределения идентичности и трассы включают `--config-dir`, `--agent-id`, `--tenant-id`, `--principal-id`, `--trace-id` и `--session-id`, чтобы примеры можно было сделать детерминированными без редактирования конфигураций. Более специальные переключатели включают `--limit` для инспекции памяти, `--approval-id` для закрытия подтверждения, `--replay-trace-id` для повторного прогона трассы, `--trace-prefix` для команд сессий и `--session-prefix` для экспортов оценочных наборов.

Просмотр идентичности агента и утвержденного инвентаря:

```bash
.venv/bin/python -m agent_runtime_ref inspect-agent
```

`inspect-agent` возвращает `agent_id`, `display_name`, `owner_team`, `runtime_principal`, `approved_capabilities`, `catalog_capability_names`, `write_capabilities`, `write_capability_egress`, `approval_required_capabilities`, `approval_required_capability_bindings`, `idempotency_required_capabilities`, `idempotency_required_capability_bindings` и `catalog_capabilities`, чтобы проверка инвентаря могла сопоставить настроенную идентичность с каталогом возможностей. Во встроенном `agent.yaml` эта идентичность имеет `agent_id` `support-triage-ref`, `display_name` `Support triage reference agent`, `owner_team` `agent_platform`, `runtime_principal` `svc-support-triage-ref` и утверждена только для `search_docs` и `create_ticket`; каталог возможностей затем помечает `search_docs` как принадлежащую `knowledge_platform` и связывает ее с `svc-knowledge-reader`, а `create_ticket` как принадлежащую `support_platform` и связывает с `svc-ticket-writer`. Каждая запись `catalog_capabilities` также несёт `name`, `owner`, `mode`, `transport`, `risk_tier`, `network_access`, `tool_principal`, `approval_required`, `idempotency_key_required` и `allowed_egress`, чтобы проверяющие видели идентичность возможности, позицию по повторной записи и позицию по исходящему обмену в одном ответе. Для сквозной цепочки с дублем тикета это означает, что `create_ticket` виден как принадлежащий поддержке, высокорисковый, посреднический, привязанный к `svc-ticket-writer` и требующий `idempotency_key` до безопасного повтора или сверки; `approval_required_capability_bindings` и `idempotency_required_capability_bindings` напрямую повторяют владельца и привязку инструментального субъекта этой записывающей возможности, а `write_capability_egress` повторяет ее посредническую цель исходящего обмена `tickets.internal`, чтобы операторам не приходилось сначала сканировать весь список каталога. Загрузчики идентичности и каталога валидируют эту форму через ошибки вроде `'agent' must be a mapping`, `agent.id must be a string`, `agent.id is required`, `agent.display_name is required`, `agent.owner_team is required`, `agent.runtime_principal is required`, `'approved_capabilities' must be a list`, `Agent inventory config must be a mapping`, `Agent identity config must be a mapping`, `approved_capabilities entries must be strings`, `approved_capabilities entries must not be empty`, `approved_capabilities entries must be unique`, `approved_capabilities lookup must be a string`, `'capabilities' must be a mapping`, `Capability spec for {name!r} must be a mapping`, `Capability names must be strings`, `Capability name must not be empty`, `Capability names must be unique`, `Capability catalog entries must be CapabilitySpec`, `capabilities.{capability_name}.{key} must be a string`, `capabilities.{capability_name}.{key} is required`, `{label}.{key} must be a string`, `{label} must be a string` и `capabilities.{capability_name}.timeout_seconds must be positive`, `'{label}.{key}' must be an integer` и `'{label}.{key}' must be a boolean`, `{label}.approval must be a string`, `{label}.approval must not be empty`, `{label}.approval is not supported: {approval}`, `'allowed_egress' must be a list`, `allowed_egress entries must be strings`, `allowed_egress entries must not be empty` и `allowed_egress entries must be unique`.

Просмотр артефактов жизненного цикла из части VIII, включая связь управления средой выполнения и идентичность выпуска:

```bash
.venv/bin/python -m agent_runtime_ref inspect-lifecycle
.venv/bin/python -m agent_runtime_ref check-controls --signal policy_traces_present=false
.venv/bin/python -m agent_runtime_ref check-change --signal offline_eval_passed=false
.venv/bin/python -m agent_runtime_ref check-change --signal failed_run_drill_checked=false
.venv/bin/python -m agent_runtime_ref check-retirement --step revoke_egress=false
```

`inspect-lifecycle` теперь тоже показывает `sandbox_profile` из `runtime-controls.yaml`, включая `sandbox_profile.workspace_entries` и `sandbox_profile_summary` (`workspace_paths`, `shell`, `network`, `secrets`, `snapshot`), а также `artifact_bundle.bundle_name`, `artifact_bundle.version`, `artifact_bundle.provenance_required`, `artifact_bundle.signed`, `artifact_bundle.review_evidence_keys`, `artifact_bundle.review_evidence` с `duplicate_ticket_guard`, `artifact_bundle.sandbox_profile_review_evidence`, `artifact_bundle.duplicate_ticket_guard_evidence`, `change.change_type`, `change.risk_level`, `change.rollout_strategy`, `change.affected_surfaces`, `change.required_signals`, `change.approval_roles`, `change.session_control_owner` (`support-ops`), `change.emergency_freeze_owner`, `artifact_bundle.session_control_owner`, `retirement.session_control_owner`, `retirement.emergency_freeze_owner`, `failed_run_archive_targets`, `controls.failed_run_control_expectations`, `controls.failed_run_control_domains`, `controls.failed_run_control_count`, `controls.failed_run_control_summary`, `controls.failed_run_control_status`, `controls.failed_run_control_review_required`, `controls.failed_run_control_owner`, `controls.failed_run_control_source`, `controls.failed_run_control_last_review`, `controls.failed_run_control_next_review`, `controls.failed_run_control_release_binding`, `controls.support_duplicate_control_expectations`, `controls.support_duplicate_control_domains`, `controls.support_duplicate_control_count`, `controls.support_duplicate_control_summary`, `controls.support_duplicate_control_status` и `controls.support_duplicate_control_release_binding`, так что оператор видит в одной сводке жизненного цикла владение, ответственность за заморозку, срок хранения, контроль трасс и происхождения, а также контроль доказательств по дублям тикетов.
Та же сводка управления средой выполнения опирается на `runtime-controls.yaml`, включая `pause_allowed`, `resume_allowed`, `background_mode_allowed`, `max_wait_seconds`, `on_expiry`, `contract_version`, `capability_session_owner`, `capability_sessions`, `track_session_ids`, `resume_allowed`, `allow_progress_events`, `allow_elicitation`, `on_session_expiry: reinitialize_or_cancel`, `expiry_policy` и `expiry_signal_owner`, чтобы возобновляемые сессии возможностей явно показывали ход выполнения, запрос дополнительных данных и предположения об истечении срока. Значения по умолчанию для `delegated_authorization` тоже явные: `authorization_mode` равен `user_delegated_or_platform_owned`, `delegated_principal_policy` — `explicit_principal_binding_required`, `token_reuse_policy` — `reuse_within_valid_paused_run_only`, `on_authorization_revoke` — `cancel_or_reapprove`, `subagent_inheritance` — `denied_by_default`, а возобновляемые и повторно инициализируемые цепочки используют `resume_existing_session_if_valid`. Загрузчик профиля песочницы валидирует эти формы управления средой выполнения ошибками `runtime_controls config must be a mapping`, `runtime_controls.sandbox_profile config must be a mapping`, `runtime_controls.sandbox_profile.{key} config must be a mapping`, `runtime_controls.sandbox_profile.workspace.entries must be a list`, а прямое построение отвергает некорректные корни песочницы через `Sandbox profile config must be a mapping`, некорректные секции песочницы через `Sandbox profile {key} config must be a mapping`, некорректные значения доказательств песочницы через `Sandbox profile {section}.{key} must be a string` или некорректные записи рабочей области через `Sandbox profile workspace entries must be a list`.
`check-change` возвращает `change_id`, `ready`, `required_signals`, `approval_roles`, `missing_signals`, `failed_run_signals`, `missing_failed_run_signals`, `support_duplicate_signals`, `missing_support_duplicate_signals`, `support_duplicate_signals_ready`, `rollout_strategy` и `risk_level`; его обязательные сигналы включают `duplicate_ticket_eval_passed`, чтобы доказательства регрессии по дублю тикета проверялись и на готовности изменения, и на готовности поэтапного выпуска.
Загрузчики списков жизненного цикла отвергают некорректные, пустые и повторяющиеся записи через `{key} must be a list`, `{key} entries must be strings`, `{key} entries must not be empty` и `{key} entries must be unique`. `check-retirement` возвращает `system_id`, `ready`, `triggers`, `missing_steps`, `required_steps`, `archive_targets`, `failed_run_archive_targets`, `support_duplicate_archive_targets` и `replacement_mode`, чтобы оператор видел, какие записи телеметрии, сессий и подтверждений должны пережить вывод из эксплуатации ради последующего разбора деградировавшего пути.
`check-controls` возвращает `healthy`, `required_controls`, `blocked_findings_expected`, `missing_controls`, `failed_run_controls`, `preserved_failed_run_controls`, `failed_run_controls_healthy`, `support_duplicate_controls`, `preserved_support_duplicate_controls`, `support_duplicate_controls_healthy`, `blocking_findings` и `inventory_drift`; вложенный объект `inventory_drift` показывает `has_drift`, `missing_from_catalog` и `missing_from_inventory`, чтобы пробелы трасс/происхождения и расхождения инвентаря возможностей можно было разбирать отдельно от общей гигиены управления. Его входы в `controls.yaml` требуют `registry_reviewed`, `capability_owners_confirmed`, `memory_provenance_enforced`, `policy_traces_present`, `duplicate_ticket_eval_passed` и `idempotency_keys_present`; валидируемая форма задается ошибками `'controls' must be a mapping`, `'controls.require' must be a list`, `'controls.block_if' must be a list`, `{label} entries must be strings`, `{label} entries must not be empty` и `{label} entries must be unique`, а политика контролей нормализует их в `required_controls`; `block_if` считает `direct_tool_access_present` и `unmanaged_runtime_present` жесткими блокерами, суммируется как `blocked_findings_expected` и во время оценки становится `blocking_findings`.

Просмотр записей памяти:

```bash
.venv/bin/python -m agent_runtime_ref inspect-memory --memory-class profile
```

`inspect-memory` теперь возвращает `config_dir`, `count`, `memory_ids` и `records`; каждая запись показывает не только содержимое, но и `provenance` с `revision`.
`dump-events` теперь возвращает `trace_id`, `status`, `result`, `event_count`, `event_types`, `failure_reason`, `approval_ids`, `approval_capability_names`, `pending_approval_ids`, `pending_approval_capability_names`, `approval_status_counts`, `idempotency_keys` и `events` в JSON-ответе для упражнений по деградировавшим путям.

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

`export-events` возвращает `output_path`, `trace_id`, `session_id`, `tenant_id`, `principal_id`, `agent_id`, `authorization_mode`, `delegated_principal_id`, `delegated_scope`, `status`, `result`, `event_count`, `event_types`, `redact_fields`, `approval_ids`, `approval_capability_names`, `pending_approval_ids`, `pending_approval_capability_names`, `approval_status_counts`, `idempotency_keys` и опциональный `failure_reason`, чтобы обезличивание и доказательства деградировавшего пути были видны уже в сводке команды.

Если нужен обезличенный экспорт для внешнего разбора, можно сразу скрыть чувствительные поля:

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

`dump-events` возвращает `status`, `result`, `failure_reason`, `trace_id`, `session_id`, `tenant_id`, `principal_id`, `agent_id`, `authorization_mode`, `delegated_principal_id`, `delegated_scope`, `event_count`, `event_types`, `approval_ids`, `approval_capability_names`, `pending_approval_ids`, `pending_approval_capability_names`, `approval_status_counts`, `idempotency_keys` и `events`; `inspect-trace` возвращает `trace_id`, `session_id`, `tenant_id`, `principal_id`, `agent_id`, `authorization_mode`, `delegated_principal_id`, `delegated_scope`, `status`, `output_preview`, `event_count`, `event_types`, `failure_reason`, `approval_ids`, `approval_capability_names`, `pending_approval_ids`, `pending_approval_capability_names`, `approval_status_counts`, `idempotency_keys` и `events`; `export-events` тоже показывает сводку `approval_ids`, `approval_capability_names`, `pending_approval_ids`, `pending_approval_capability_names`, `approval_status_counts` и `idempotency_keys` рядом с `redact_fields`, чтобы цепочка подтверждений, цепочка возможностей подтверждения, статус подтверждения и цепочка повторной записи были видны до ручного просмотра отдельных данных. `replay-run` возвращает `source_trace_id`, `replay_trace_id`, `source_session_id`, `replay_session_id`, `source_tenant_id`, `replay_tenant_id`, `source_principal_id`, `replay_principal_id`, `source_agent_id`, `replay_agent_id`, `source_authorization_mode`, `replay_authorization_mode`, `source_delegated_principal_id`, `replay_delegated_principal_id`, `source_delegated_scope`, `replay_delegated_scope`, `status`, `result`, `source_status`, `source_output_preview`, `source_failure_reason`, `replay_status`, `replay_output_preview`, `replay_failure_reason`, `event_count`, `event_types`, `source_event_count`, `source_event_types`, `replay_event_count`, `replay_event_types`, `idempotency_keys`, `source_idempotency_keys`, `replay_idempotency_keys`, `approval_ids`, `source_approval_ids`, `replay_approval_ids`, `pending_approval_ids`, `source_pending_approval_ids`, `replay_pending_approval_ids`, `approval_capability_names`, `source_approval_capability_names`, `replay_approval_capability_names`, `pending_approval_capability_names`, `source_pending_approval_capability_names`, `replay_pending_approval_capability_names`, `approval_status_counts`, `source_approval_status_counts` и `replay_approval_status_counts`, чтобы расследование и повторный прогон сохраняли исходную и повторную цепочки возможностей подтверждения, статусов и ключей записи.

Проверка политики выкладки с переопределением сигналов:

```bash
.venv/bin/python -m agent_runtime_ref check-rollout --signal offline_eval_pass=false
```

Проверка поэтапного выпуска возвращает `ready`, `required_checks`, `blocked_checks`, `missing_required`, `support_duplicate_required`, `missing_support_duplicate_required`, `support_duplicate_required_ready`, `blocking_signals` и `rollout_mode`; обязательные доказательства включают `duplicate_ticket_eval_passed`, чтобы автоматизация отличала отсутствующее регрессионное доказательство по дублю тикета от явно блокирующих сигналов; переопределения сигналов принимают логические пары `key=value` и отвергают неизвестное логическое значение через `Unsupported boolean value in signal: {raw_signal!r}`. Неудачные пути командного интерфейса среды выполнения также сохраняют стабильные сообщения для оператора: `Config path must be a string or path-like object`, `Session output path must be a string or path-like object`, `Telemetry path must be a string or path-like object`, `CLI field must be a string: {field}`, `CLI field is required: {field}`, `CLI field is not supported: {field}={value}; expected one of: {expected}`, `CLI field must be an integer: {field}`, `CLI field must be non-negative: {field}`, `CLI field entries must be a sequence: {field}`, `CLI field entries must be unique: {field}`, `Runtime request must be RunRequest`, `Run request field must be a string: {field}`, `Run request field is required: {field}`, `Delegated authorization field is required: {field}`, `Signal must be a string`, `Signal must use key=value format: {raw_signal!r}`, `Signal key must not be empty: {raw_signal!r}`, `Background request must be RunRequest`, `Background context must be RunContext`, `Background model_output must be ModelOutput`, `Background context tool_results must be a list`, `Background context tool_results entries must be ToolResult`, `Background memory_store must be MemoryStore`, `Background policy must be PolicyEngine`, `Background telemetry must be TelemetryEmitter`, `Runtime catalog must be CapabilityCatalog`, `Runtime policy must be PolicyEngine`, `Runtime telemetry must be TelemetryEmitter`, `Runtime memory must be MemoryStore`, `Runtime approvals must be ApprovalQueue`, `Runtime sessions must be SessionStore`, `Runtime agent must be AgentIdentity`, `Runtime background must be BackgroundWorker`, `Approval queue policy must be ApprovalPolicy`, `Approval policy config must be a mapping`, `Capability catalog config must be a mapping`, `Controls policy config must be a mapping`, `Memory store config must be a mapping`, `Policy config must be a mapping`, `Rollout policy config must be a mapping`, `Telemetry event must be a mapping`, `Approval field must be a string: {field}`, `Approval field is required: {field}`, `Approval status is not supported: {status}`, `Approval decision is not supported: {decision}`, `Controls inventory must be ApprovedInventory`, `Controls catalog must be CapabilityCatalog`, `Controls policy must be ControlsPolicy`, `Controls inventory_drift must be InventoryDrift`, `Lifecycle change must be ChangeRecord`, `Lifecycle retirement plan must be RetirementPlan`, `Assessment signals must be a mapping`, `Assessment signal key must be a string`, `Assessment signal key must not be empty`, `Assessment signal keys must be unique`, `Assessment signal value must be a boolean: {field}`, `Rollout policy must be RolloutPolicy`, `Rollout readiness must be RolloutReadiness`, `Rollout readiness flag must be a boolean: {field}`, `Policy action is not supported: {action}`, `Policy field must be a string: {field}`, `Policy field is required: {field}`, `Tool capability must be CapabilitySpec`, `Tool request must be ToolRequest`, `Tool policy decision must be PolicyDecision`, `Policy precheck request must be RunRequest`, `Policy context must be RunContext`, `Policy tool request must be ToolRequest`, `Policy capability must be CapabilitySpec`, `Tool request capability name must be a string`, `Tool request capability name must not be empty`, `Tool request arguments must be a mapping`, `Tool request argument key must be a string`, `Tool request argument key must not be empty`, `Tool request argument keys must be unique`, `Tool request argument value must be a string: {argument_key}`, `Tool request capability does not match catalog entry: {capability_name} != {capability.name}`, `Tool result status must be a string`, `Tool result status must not be empty`, `Tool result payload must be a mapping`, `Tool result payload key must be a string`, `Tool result payload key must not be empty`, `Tool result payload keys must be unique`, `Tool result payload value must be a string: {payload_key}`, `Approval request not found: {approval_id}`, `Approval request is not pending: {approval_id}`, `No pending approval requests were generated for this run`, `Session field must be a string: {field}`, `Session field is required: {field}`, `Session status is not supported: {status}`, `Session tenant_id does not match existing session: {session_id}`, `Session principal_id does not match existing session: {session_id}`, `Session trace_id already exists: {trace_id}`, `Session field entries must be a sequence: {field}`, `Session field entries must be unique: {field}`, `Session field entries must be unique: session_id`, `Session runs must be a sequence`, `Session runs entries must be RunRecord`, `Session field entries must be a sequence: session_id`, `Session eval specs must be a mapping`, `Session not found: {session_id}`, `Telemetry event field must not be empty: event_type`, `Telemetry event field must not be empty: trace_id`, `Telemetry event field must not be empty: schema_version`, `Telemetry schema version is not supported: {schema_version}`, `Telemetry redact field must not be empty`, `Trace ID request must be a string`, `Trace ID not found in event file: {requested_trace_id}`, `Trace file contains multiple trace IDs; pass --trace-id explicitly`, `Trace file does not contain a run_start event`, `Model step must return ModelOutput`, `Model output text must be a string` и `Model output tool_request must be ToolRequest`.

Проверка непрерывных контролей и расхождения с реестром:

```bash
.venv/bin/python -m agent_runtime_ref check-controls --signal registry_reviewed=false
```

Просмотр и разрешение демонстрационных запросов на подтверждение:

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

`inspect-approvals` теперь возвращает `trace_id`, `session_id`, `tenant_id`, `agent_id`, `count`, `approval_ids`, `pending_approval_ids`, `approval_capability_names`, `pending_approval_capability_names`, `approval_status_counts`, `idempotency_keys` и `approvals`, включая `tenant_id`, `agent_id`, поля жизненного цикла сессии возможности (`capability_session_id`, `capability_session_status`), контекст делегированного разрешения: `authorization_mode`, `delegated_principal_id` и `delegated_scope`, а также `idempotency_key`, так что проверку цепочки подтверждения можно напрямую сопоставить с доказательствами сессии и намерением повторной записи. `resolve-approval` возвращает `approval_id`, `approval_ids`, `trace_id`, `session_id`, `tenant_id`, `agent_id`, `capability_name`, `approval_capability_names`, `pending_approval_ids`, `pending_approval_capability_names`, `requested_by`, `status`, `reviewer`, `resolution_note`, `capability_session_id`, `capability_session_status`, тот же делегированный контекст, `idempotency_key`, `idempotency_keys` и `approval_status_counts` после принятого решения, чтобы сессия возможности, действующая идентичность, цепочка идемпотентности и итоговый статус подтверждения не терялись на этапе закрытия.
`inspect-session` показывает историю запусков на уровне сессии и связанные `trace_id`. Теперь туда тоже можно инъецировать упражнение с отказом, а сводка сохраняет `failed_runs`, `traceable_failed_runs`, `trace_ids`, `failed_trace_ids`, `latest_failure_reason`, а также поля отдельных запусков `output_text`, `failure_reason`, `request_agent_id`, `capability_session_id`, `capability_session_status` и `idempotency_key`.
`session-eval-summary` возвращает короткую рабочую сводку по серии запусков, включая неудачные запуски и `traceable_failed_runs`, а не сводя все обратно только к успехам и отказам. Теперь туда можно напрямую инъецировать упражнение с отказом, а сводка сразу показывает `latest_failure_reason` для быстрого разбора.
`session-replay` позволяет прогнать несколько связанных запросов в одной `session_id`. Теперь туда тоже можно инъецировать упражнение с отказом, а сводка повторного прогона сохраняет `failed_runs`, `traceable_failed_runs`, `trace_ids`, `failed_trace_ids` и `latest_failure_reason` вместе с полями отдельных запусков `failure_reason` и `request_agent_id`.
`export-session` сохраняет сессию как структурированный JSON, который уже можно использовать как исходный материал для офлайн-оценок. Теперь он еще и сохраняет поля жизненного цикла сессии возможности (`capability_session_id`, `capability_session_status`), контекст делегированного разрешения, включая `authorization_mode`, `delegated_principal_id` и `delegated_scope`, а также `idempotency_key` и `approval_id`, а в сводке самой команды показывает `failed_runs`, `traceable_failed_runs`, `trace_ids`, `failed_trace_ids` и `latest_failure_reason` для упражнений с отказом.

Команды сессий и оценок явно показывают поля сводки: `inspect-session` возвращает `session_id`, `tenant_id`, `principal_id`, `trace_count`, `trace_ids`, `failed_trace_ids`, `latest_status`, `latest_failure_reason`, `idempotency_keys`, `approval_ids`, `approval_capability_names`, `pending_approval_ids`, `pending_approval_capability_names`, `approval_status_counts`, `summary` и `runs`; `session-eval-summary` возвращает `session_id`, `total_runs`, `success_runs`, `approval_wait_runs`, `denied_runs`, `failed_runs`, `traceable_failed_runs`, `trace_ids`, `failed_trace_ids`, `idempotency_keys`, `approval_ids`, `approval_capability_names`, `pending_approval_ids`, `pending_approval_capability_names`, `approval_status_counts`, `latest_status`, `latest_trace_id` и `latest_failure_reason`; `session-replay` возвращает `session_id`, `run_count`, `trace_ids`, `failed_trace_ids`, `idempotency_keys`, `approval_ids`, `approval_capability_names`, `pending_approval_ids`, `pending_approval_capability_names`, `approval_status_counts`, `latest_failure_reason`, `summary` и `runs`; `export-session` возвращает `output_path`, `session_id`, `total_runs`, `failed_runs`, `traceable_failed_runs`, `trace_ids`, `failed_trace_ids`, `idempotency_keys`, `approval_ids`, `approval_capability_names`, `pending_approval_ids`, `pending_approval_capability_names`, `approval_status_counts`, `latest_trace_id` и `latest_failure_reason`; экспортированный JSON сессии также несёт на верхнем уровне `total_runs`, `failed_runs`, `traceable_failed_runs`, `trace_ids`, `failed_trace_ids`, `idempotency_keys`, `approval_ids`, `approval_capability_names`, `pending_approval_ids`, `pending_approval_capability_names`, `approval_status_counts`, `latest_failure_reason`, `latest_trace_id` и идентификатор `session` рядом с вложенной `summary`; `export-eval-dataset` возвращает `dataset_name`, `output_path`, `session_count`, `session_ids`, `run_count`, `failed_runs`, `traceable_failed_runs`, `trace_ids`, `failed_trace_ids`, `idempotency_keys`, `approval_ids`, `approval_capability_names`, `pending_approval_ids`, `pending_approval_capability_names`, `approval_status_counts`, `duplicate_ticket_scenarios`, `latest_failure_reason` и `sessions` как список `session_id`, а экспортированный артефакт оценочного набора несёт на верхнем уровне `failed_runs`, `traceable_failed_runs`, `trace_ids`, `failed_trace_ids`, `idempotency_keys`, `approval_ids`, `approval_capability_names`, `pending_approval_ids`, `pending_approval_capability_names`, `approval_status_counts` и `latest_failure_reason`. Каждая экспортированная оценочная сессия несёт на верхнем уровне `trace_ids`, `failed_trace_ids`, `idempotency_keys`, `approval_ids`, `approval_capability_names`, `pending_approval_ids`, `pending_approval_capability_names` и `approval_status_counts` рядом с `summary.trace_ids`, `summary.failed_trace_ids`, `summary.idempotency_keys`, `summary.approval_ids`, `summary.approval_capability_names`, `summary.pending_approval_ids`, `summary.pending_approval_capability_names` и `summary.approval_status_counts`, а также `session` и блок `eval` с `scenario`, `labels`, `expected_outcomes` и `grading_rules`; вложенные записи запусков сохраняют `request_agent_id` и `user_input` для каждого запуска. По умолчанию `dataset_name` равен `agent-runtime-ref-eval-seed`, если вызывающий не передал `--dataset-name`; экспорт оценок также валидирует внутреннюю основу `session_prefix` перед генерацией `session_id`, а команды сессий валидируют внутреннюю основу `trace_prefix` перед генерацией `trace_id`.

Теперь среда выполнения также считает пути инструментов с неуспешным исходом, например отказ валидации, полноценным итогом запуска. Вместо того чтобы делать вид, будто запуск завершился успешно, она фиксирует неудачный запуск, пишет явное событие `run_failed` и конечное `run_complete.failure_reason` для неудачных или отклоненных запусков, а затем сохраняет этот статус вместе с конкретной причиной сбоя в поле `failure_reason` в экспорте сессии, инспекции трассы, сводках повторного прогона и выводе командного интерфейса.
`export-eval-dataset` собирает несколько встроенных сценариев сессий в один JSON-артефакт, готовый к оценке: отдельное упражнение с неудачным запуском содержит `duplicate_ticket_eval_passed`, `max_ticket_side_effects: 1` и блокирующий `duplicate_ticket_guard`; сценарий чтения профильной памяти `profile_memory` содержит метки `memory_read`, `profile_lookup` и `grounded_answer`; сценарий нескольких запусков с подтверждением и памятью `mixed_session` содержит метки `multi_run`, `approval_then_memory` и `session_evals`, плюс `required_run_count` и `approval_status_counts` как ожидаемые исходы; сценарий `support_ticket`, опирающийся на подтверждение, содержит метку `sandbox_profile_review`, ожидаемый исход `sandbox_profile_reviewed` и блокирующее правило оценки `sandbox_profile_review`. Сводка самой команды теперь тоже показывает агрегированные `failed_runs`, `traceable_failed_runs`, `trace_ids`, `failed_trace_ids` и `latest_failure_reason`.

Этот путь оценки теперь полезно читать вместе с более богатым проверочным контрактом из приложения: для длинных сценариев пакет должен помогать представить, как набор данных со временем может нести `process_score`, `outcome_score`, `failure_attribution` и связанные доказательства проверки, а не только один тонкий вердикт.

Вместе эти команды теперь помогают показать важное различие из глав 16 и 17:

- пользовательскую `session_id`, которая связывает несколько запусков;
- `trace_id` каждого конкретного запуска для расследований;
- состояние сессии со стороны возможности, которое может быть поставлено на паузу, истечь, возобновиться или потребовать повторной инициализации.

Пакет по-прежнему намеренно маленький, но теперь он уже отражает, что управляемая среда выполнения иногда обязана объяснять все три контура отдельно, не сливая их в один непрозрачный объект состояния.

Это же место теперь полезно и как привязка для урока Anthropic про устройство испытательного контура: долгая прикладная работа может требовать явных сбросов контекста, структурированных артефактов передачи и разделения ролей планирования, генерации и оценки, а не одного непрерывного агентного цикла. Эталонный пакет не реализует такой контур целиком, но уже показывает те стыки среды выполнения, в которых должны жить безопасная передача после сброса, контракты коротких рабочих отрезков, проверка оценщиком и возобновленное состояние управления.

Это еще и полезный якорь для управления, учитывающего проверяющий контракт: если поэтапный выпуск или заверение зависят от результата оценки, среда выполнения должна сохранять достаточно связей между трассой, сессией и артефактами, чтобы объяснять не только что произошло, но и почему проверяющий оценил запуск именно так.

Это должно тянуться и в обработку жизненного цикла. Управляемая эталонная среда выполнения должна уметь объяснять, какой проверочный контракт и какая идентичность выпуска были активны для релиза, какие доказательства еще нужно хранить после вывода из эксплуатации, чтобы обосновывать прежние решения поэтапного выпуска или заверения, и какие структурированные артефакты передачи должны пережить сброс контекста или передачу роли, если именно они определяли, что выводимой системе было разрешено делать.

Теперь в нем отражена и четвертая рабочая забота: контекст делегированного разрешения, под которым вообще исполнялось действие. Этот контекст теперь появляется в телеметрии запуска, записях подтверждения и экспорте сессии, чтобы среда выполнения могла объяснять не только что произошло, но и от чьей делегированной идентичности и в какой области это произошло.

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

В [configs](https://github.com/agent-axiom/agent-arch/tree/main/agent_runtime_ref/configs) лежат стартовые файлы для среды выполнения и жизненного цикла:

- [agent.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/agent.yaml)
- [policy.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/policy.yaml)
- [capabilities.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/capabilities.yaml)
- [memory.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/memory.yaml)
- [rollout.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/rollout.yaml)
- [controls.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/controls.yaml)
- [approvals.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/approvals.yaml)
- [change.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/change.yaml)
  В шлюзе изменений теперь есть явные сигналы `failed_run_drill_checked` и `sandbox_profile_reviewed`, чтобы проверка поэтапного выпуска высокого риска не относила деградировавшие пути или изменения профиля песочницы к чему-то вне проверки.
- [artifacts.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/artifacts.yaml)
- [runtime-controls.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/runtime-controls.yaml)
- [retirement.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/retirement.yaml)

Это уже не просто статические примеры. `config.py` умеет загружать эти YAML-файлы в идентичность агента, утвержденный инвентарь, среду выполнения, слои контекста, хранилище памяти, политику выкладки, артефакты жизненного цикла с идентичностью выпуска и другие элементы жизненного цикла, поэтому пакет стал ближе к реальному эксплуатационному каркасу. Общие загрузчики также явно показывают некорректные формы YAML: `Config at {config_path!s} must be a mapping at the top level`, `{label} config must be a mapping` и `{key} must be a list`.

При этом набор управления средой выполнения теперь задуман еще и как явное место для правил подтверждения и управления сессиями, включая паузу/возобновление, фоновую обработку, истечение срока, политику повторной инициализации, владение сессиями возможностей и границу между пользовательским запуском и сессией со стороны возможности.

### Минимальный профиль песочницы

Если расширять пакет в сторону выполнения через песочницу, полезно начинать не с новой большой подсистемы, а с небольшого профиля, который делает рабочую область и права явными:

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

Такой пример не делает эталонную среду выполнения полноценным оркестратором песочниц. Он фиксирует поверхность контракта, которую главы 9 и 16 требуют от настоящей среды выполнения с песочницей: манифест, права, материализация рабочей области, состояние сессии и политика снимка/возобновления должны быть видимыми для проверки.

### Паттерн долговечного агентного исполнителя

В будущем примере эталонной среды выполнения стоит отдельно смоделировать границу долговечного агентного исполнителя из главы 16. Среде выполнения не нужна зависящая от поставщика реализация Durable Object, но ей нужен видимый контракт для стабильной идентичности агента, локального состояния экземпляра, возобновляемых сессий, запланированных пробуждений и передачи в управляемые хранилища.

Допустимое локальное состояние узкое: курсор рабочего процесса, позиция очереди для экземпляра, предпочтения соединения/сессии, последнее обработанное событие, метаданные расписания и восстанавливаемые кэшированные представления. Профильная память, знания арендатора, секреты, политика, журналы аудита и факты между экземплярами должны оставаться в управляемых хранилищах с правилами происхождения, срока хранения, экспорта и контроля доступа.

Минимальная config surface:

- `agent_instance_id`, `tenant_id`, `owner_ref` и `schema_version`;
- `state_class`: `ephemeral`, `instance_local`, `governed_memory_ref` или `external_record_ref`;
- `resume_policy`, `hibernation_policy` и `state_migration_policy`;
- `schedule_records` с экземпляром-владельцем, ключом идемпотентности, политикой пересечения, временем следующего запуска и связью с трассой;
- `connection_scope` для WebSocket/потокового распространения и видимости интерфейса подтверждения;
- `export_ref`, `delete_ref` и `audit_refs`, чтобы скрытая долговечная память была невозможна.

### Паттерн агентной оболочки и долговечного стержня процесса

Для будущего расширения эталонной среды выполнения полезно держать отдельный паттерн: агент не обязан владеть всей долгой работой. Он может быть оболочкой взаимодействия — `agent_instance_id`, состояние сессии, пользовательский поток, разрешение в области соединения, интерфейс подтверждения. Рядом с ним долговечный стержень процесса должен владеть шагами, повторами, ожиданием внешних событий, долговечными записями подтверждения, ключами идемпотентности и ссылками на доказательства.

Минимальная поверхность контракта для такого примера:

- `workflow_instance_id` рядом с `agent_instance_id`, `run_id` и `trace_id`;
- `durable_step_id`, `step_status`, `retry_policy`, `timeout_policy` и `idempotency_key`;
- `waiting_for`: внешнее событие, подтверждение, таймер или сверка;
- `approval_id` и `approval_decision_ref`, если рабочий процесс остановлен на человеческом шлюзе;
- `progress_event_id`, который явно не считается долговечным шагом;
- `evidence_refs`, связывающие возобновление процесса с аудитом и экспортом событий.

Такой паттерн хорошо дополняет текущие фоновые обновления: фоновая задача может быть простой отложенной работой, а стержень процесса — проверяемой долговечной процедурой, которая переживает часы ожидания, сбои и ручные решения.

## Почему это полезно

Книга теперь опирается не только на текстовые объяснения, но и на реальный кодовый каркас:

- легче обсуждать архитектуру на уровне файлов и контрактов;
- легче расширять пакет следующими примерами;
- легче перейти от главы к исполняемому прототипу;
- легче показать путь, управляемый конфигурацией, а не только жестко зашитое демо;
- легче связать эталонную среду выполнения с главами про память, извлечение контекста, фоновые обновления и управление средой выполнения;
- легче обсуждать, откуда взялась каждая запись памяти, какая у нее ревизия и какая версия контракта управления средой выполнения была активна;
- легче держать на виду идентичность выпуска, цепочку проверочного контракта и обязательства вывода из эксплуатации рядом с решениями по управлению средой выполнения и артефактами;
- легче держать отдельно, но согласованно, состояние подтверждения, состояние сессии среды выполнения, состояние сессии возможности и доказательства проверки.

Отдельно полезно то, что теперь пакет можно не только запускать, но и инспектировать снаружи:

- `inspect-memory` показывает исходно загруженную память и фильтрацию по `tenant` и `memory_class`;
- `dump-events` показывает структурированную трассу одного запуска без чтения исходников;
- `export-events` сохраняет трассу в JSONL для разбора вне процесса;
- `export-events` умеет добавлять `schema_version` и делать обезличивание при экспорте по выбранным полям;
- путь `export-events`, опирающийся на подтверждение, пишет `sandbox_profile_reviewed`, чтобы доказательства трассы совпадали с набором жизненного цикла и правилом оценки;
- `inspect-trace` позволяет читать и фильтровать сохраненные трассы;
- `replay-run` поднимает повторный прогон по `run_start` из сохраненной трассы.

Проще всего читать этот пакет так:

- книгу использовать для архитектуры, последовательности и аргумента об операционной модели;
- этот пакет использовать для исполняемой структуры, поверхностей конфигурации и примеров инспекции;
- схемы приложения использовать, чтобы видеть границы контрактов, которые среда выполнения пытается сделать явными.

## Что делать дальше

- [Схема трасс и каталог событий](trace-schema.md)
- [Схема наборов для оценки и правил проверки](eval-schema.md)
- [Схема набора политик и контракта подтверждения](policy-bundle-schema.md)
- [Схема артефактов жизненного цикла](lifecycle-artifact-schema.md)
- [Глава 17. Слой политик и каталог возможностей](../book/part-vii/chapter-17.md)


Буквальные маркеры среды выполнения также включают `eval_gate` и `session_idempotency_summary`, чтобы доказательства оценки и идемпотентности оставались документированными.
