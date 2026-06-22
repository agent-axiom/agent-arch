# Runtime reference companion: configs

Статус: companion-материал к русской издательской рукописи.

Эта страница хранит механические формы, которые не должны перегружать печатную главу про песочницу выполнения, MCP boundary и runtime controls. В книге остается аргумент: зачем нужна граница выполнения, кто ей владеет и какие доказательства она должна оставить. Здесь остаются точные поля для ревью и повторяемой проверки.

## Где смотреть исходники

- Пакет: `agent_runtime_ref/`
- Конфиги: `agent_runtime_ref/configs/`
- Основной runtime-control файл: `agent_runtime_ref/configs/runtime-controls.yaml`
- Тесты поверхности: `tests/test_agent_runtime_ref.py`, `tests/test_docs_surface.py`
- Печатная привязка: глава 11, глава 21 и глава 23 русской рукописи

## Execution boundary review

Минимальная карточка границы выполнения нужна до подключения write-capability. Она фиксирует не только имя capability, но и класс изоляции, владельцев, MCP boundary, риск и ожидаемый side effect.

```yaml
execution_boundary_review:
  capability: create_ticket
  owner: support-ops
  runtime_owner: platform-runtime
  mcp_server_id: mcp.support.ticketing.v3
  boundary_class:
    logical_policy: required
    process_isolation: required
    runtime_sandbox: required_for_write_path
    network_boundary: internal_or_brokered
    identity_boundary: user_delegated_or_platform_owned
  risk_tier: high
  side_effect: external_ticket_write
```

Проверка на ревью:

- capability не описана как "обычная функция", если она пишет во внешнюю систему;
- runtime owner и владелец интеграции названы явно;
- risk tier связан с политикой подтверждения и sandbox profile;
- side effect можно найти в trace, approval и recovery packet.

## Sandbox profile

Профиль песочницы должен быть исполняемым контрактом, а не общей фразой "запускается безопасно".

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

Для разных capabilities профиль должен отличаться. `search_docs`, `create_ticket` и `run_shell` не должны получать один широкий профиль "на всякий случай".

## Workspace review

Рабочая область проверяется отдельно от флага `filesystem: true`.

```yaml
sandbox_context:
  sandbox_profile_contract: sandbox-profile-v1
  workspace_entries_reviewed: true
  permissions_profile: restricted-shell-network-denied
  network_secrets_posture: network:denied,secrets:none
  snapshot_policy: required_on_completion
```

На ревью нужно пройти каждую запись workspace:

- откуда она берется: локальная директория, архив, inline file, artifact или snapshot;
- доступна ли она на чтение или запись;
- содержит ли она tenant data, secrets, source code, logs или результаты прошлых запусков;
- должна ли она попасть в snapshot;
- можно ли использовать ее при resume без повторного ревью.

## Network, secrets and identity

Сетевой режим и секреты не должны оставаться на усмотрение адаптера.

```yaml
network_policy:
  denied: "нет исходящего сетевого доступа"
  internal_only: "доступ только к внутренним адресам платформы"
  allowlisted_external: "только заранее утвержденные внешние endpoints"
  brokered_via_gateway: "весь egress идет через контролируемый шлюз"
```

Стартовая позиция для рискованного выполнения: `network: denied`, `secrets: none`. Исключение должно быть записано как часть capability contract и runtime-control bundle.

## MCP boundary

MCP-сервер публикует tools и resources, но это не делает его доверенной зоной.

```yaml
mcp_boundary:
  server_id: mcp.support.ticketing.v3
  owner: platform-integrations
  registry_state: approved
  tool_contract_version: capability-contract-v5
  tool_definition_hash: sha256:...
  auth_mode: delegated_oauth
  token_scope:
    - ticket.read
    - ticket.write_limited
  token_ttl: 15m
  user_delegation_required: true
  server_isolation_profile: remote_ephemeral_sandbox
  schema_change_requires_review: true
```

Повторное ревью требуется при изменении:

- tool description или tool schema;
- token scope;
- owner;
- isolation profile;
- auth mode;
- registry state.

## Tool content controls

Tool description и tool result нужно считать недоверенным содержимым.

```yaml
tool_content_controls:
  tool_description_source: approved_registry
  description_hash_verified: true
  result_treated_as_untrusted_content: true
  return_value_filtering: strip_instructions_and_classify_data
  prompt_boundary_marker_required: true
  dlp_check_required_for_external_results: true
```

Практическое правило: результат инструмента - это свидетельство, а не инструкция. Он не должен менять system prompt, policy, список разрешенных tools или требования к approval.

## Execution flow

Минимальный поток для write-capability:

```yaml
execution_flow:
  - model_requests_capability
  - validate_arguments
  - resolve_capability_contract
  - resolve_sandbox_profile
  - review_mcp_boundary
  - tool_policy_decision
  - approval_requested
  - approval_resolved
  - execute_in_sandbox
  - emit_trace_events
  - verify_result
```

Этот поток должен быть виден в trace и проверяться eval/regression gate для рискованных capability.

