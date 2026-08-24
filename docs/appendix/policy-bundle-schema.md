# Схема набора политик и контракта подтверждения

Эта страница связывает несколько уже написанных тем:

- [Глава 4. Инструментальный шлюз, подтверждения и журнал аудита](../book/part-ii/chapter-4.md)
- [Глава 17. Слой политик и каталог возможностей](../book/part-vii/chapter-17.md)
- [Глава 20. Управление изменениями в агентных системах](../book/part-viii/chapter-20.md)
- [Сквозная цепочка доказательств: от запроса к решению о rollout](../book/part-v/evidence-spine.md)

И опирается на эталонный пакет:

- [Эталонный пакет](reference-package.md)

Если страницы о схеме трасс и схеме оценки отвечают на вопросы:

- как описывать фактическое поведение;
- как описывать ожидаемое поведение;

то эта страница отвечает на третий вопрос:

- как описывать управляющие правила, которые стоят между рассуждением и внешним действием.

## Почему набор политик полезно мыслить как артефакт

Одна из самых частых ошибок в агентных системах устроена так:

- правила частично живут в инструкции;
- частично в коде шлюза;
- частично в интерфейсе подтверждения;
- частично в голове команды.

Пока система маленькая, это может работать. Но как только появляется управление изменениями, аудит и поэтапная раскатка, такой слой политик становится слишком размытым.

Поэтому полезно собирать набор политик как отдельный артефакт.

## Что такое набор политик

Под набором политик здесь удобно понимать набор связанных правил, который выпускается как единое целое:

- политика среды выполнения;
- политика инструментов;
- политика подтверждений;
- правила управления средой выполнения для паузы, возобновления и фоновых путей;
- правила записи в память;
- правила эскалации;
- правила исходящего сетевого доступа;
- ожидания относительно доверенных контрактов проверяющего для оценок высокого риска и доказательств раскатки.

Смысл не в том, что все должно лежать в одном YAML-файле. Смысл в том, что такой набор должен быть:

- версионируемым;
- проверяемым;
- трассируемым;
- пригодным к выпуску.

!!! note "Канонические сценарии политик"
    Пакет политик не должен выглядеть одинаково во всех трех канонических сценариях. **Триаж обращений поддержки** требует политики подтверждения для записывающей возможности, доказательств идемпотентности и средств восстановления после дубля тикета. **Внутренний ассистент знаний** требует политики поиска, правил записи в память, проверок свежести, контроля доступа и происхождения знаний. **Координация инцидентов** требует правил эскалации, побочных эффектов уведомлений, владения ответом и шлюзов обучения после инцидента.

## Минимальная структура набора политик

Минимально полезный набор может выглядеть так:

```yaml
bundle:
  bundle_id: policy-support-triage-2026-04-07
  version: 2026.04.07
  owner_team: platform-safety
  applies_to:
    agent_ids: ["support-triage-ref"]
  artifacts:
    - policy.yaml
    - approvals.yaml
    - controls.yaml
  contract_version: capability-contract-v3
  release_identity: release-support-triage-2026-04-07-canary
```

Это еще не сами правила. Это оболочка, которая отвечает на вопрос:

«Что именно мы сейчас считаем артефактом политики для этой агентной системы?»

А когда управление выпуском становится по-настоящему значимым, она должна отвечать и на следующий вопрос:

«В определении какой идентичности выпуска участвует этот набор?»

## Почему контракт подтверждения нельзя прятать внутри описательного текста

Очень часто логика подтверждения описывается словами:

- «если риск высокий, нужно подтверждение»;
- «руководитель одобряет создание тикета»;
- «команда безопасности подтверждает опасные действия».

Этого недостаточно.

Контракт подтверждения полезно делать явным:

- кто может одобрять;
- какой класс действий требует подтверждения;
- какие поля должны попасть в запрос на подтверждение;
- какие решения допустимы;
- что происходит после reject;
- можно ли приостановить запуск, возобновить его, дать ему истечь или отменить;
- что должно остаться в журнале аудита.

## Пример контракта подтверждения

Ниже рабочий каркас:

```yaml
approval_contract:
  capability: create_ticket
  risk_tier: high
  bundle_version: 2026.04.07
  release_identity: release-support-triage-2026-04-07-canary
  required_reviewers:
    - manager
  request_fields:
    - trace_id
    - session_id
    - idempotency_key
    - requested_by
    - reason
    - tool_arguments_redacted
  allowed_decisions:
    - approved
    - rejected
  runtime_controls:
    pause_allowed: true
    max_wait_seconds: 1800
    on_expiry: cancel_run
  on_reject: stop_run
```

Смысл тут простой: подтверждение должно быть не галочкой в интерфейсе, а машиночитаемым рабочим контрактом. А если подтверждение влияет на выпуск, такой контракт должен еще и явно показывать, к какой версии набора и к какой идентичности выпуска относится человеческое решение.

!!! example "Контракт политики для цепочки дубля тикета"
    Для кейса разбора обращений поддержки контракт `create_ticket` должен требовать `idempotency_key` уже в запросе на подтверждение, а не только во время выполнения инструмента. Тогда человек, шлюз и трасса видят одно и то же намерение записи, набор политик может запретить повтор без сверки при `side_effect_unknown`, а проверка раскатки оценивает управляемую возможность, а не свободный вызов инструмента.

## Как набор политик связан с жизненным циклом

Из Части VIII здесь особенно важны две мысли:

- изменения политик — это значимые изменения выпуска;
- набор политик должен участвовать в управлении изменениями как полноценный артефакт.

То есть для команды полезно отвечать не только на вопрос:

«Какая политика у нас в принципе?»

Но и на вопрос:

«Какая именно версия набора политик была активна в момент этой раскатки или инцидента?»

А если среда выполнения уже обращается с наборами как с управляемыми поверхностями выпуска, неизбежно появляется и следующий вопрос:

«В формировании какой идентичности выпуска участвовал этот набор политик?»

## Как набор политик связан с трассами

Связь очень практическая:

- трасса показывает, какое решение политики реально сработало;
- набор политик показывает, откуда это решение взялось;
- контракт подтверждения показывает, как должен был выглядеть человеческий шлюз;
- идентичность выпуска показывает, к какой именно управляемой поверхности выпуска относилось это решение.

Без этой связки из четырех элементов расследование быстро превращается в угадайку.

## Что уже умеет эталонная среда исполнения

В `agent_runtime_ref` сейчас уже есть:

- [policy.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/policy.yaml)
- [approvals.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/approvals.yaml)
- [controls.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/controls.yaml)
- [change.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/change.yaml)
- [runtime-controls.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/runtime-controls.yaml)

То есть пакет уже живет в модели, где политики, подтверждения и контракты управления средой выполнения не просто побочные настройки, а отдельные управляемые артефакты. Исполняемый шлюз `check-controls` делает набор средств управления тоже проверяемым: он возвращает `healthy`, `required_controls`, `blocked_findings_expected`, `missing_controls`, `failed_run_controls`, `preserved_failed_run_controls`, `failed_run_controls_healthy`, `support_duplicate_controls`, `preserved_support_duplicate_controls`, `support_duplicate_controls_healthy`, `blocking_findings` и `inventory_drift`, где вложенные поля `has_drift`, `missing_from_catalog` и `missing_from_inventory` отделяют отказы политик и средств управления от дрейфа каталога возможностей.

И здесь эта же среда явно фиксирует форму входного набора средств управления: проверка конфигурации средств управления сообщает `Controls policy config must be a mapping`, `'controls' must be a mapping`, `'controls.require' must be a list`, `'controls.block_if' must be a list`, `controls.require entries must be strings`, `controls.require entries must not be empty`, `controls.require entries must be unique`, `controls.block_if entries must be strings`, `controls.block_if entries must not be empty` и `controls.block_if entries must be unique`; переопределения сигналов сообщают `Assessment signals must be a mapping`, `Assessment signal key must be a string`, `Assessment signal key must not be empty`, `Assessment signal keys must be unique` и `Assessment signal value must be a boolean: {field}`. Поэтому оператор может отличить испорченный набор политик от провалившейся, но корректно сформированной оценки средств управления.

## Production extension: правила политики траектории

Проверка одного вызова не ловит ограничения, зависящие от всей
последовательности. Для таких случаев промышленную схему полезно расширить
декларативным разделом `trajectory_policy`. Ниже минимальная переносимая форма,
а не YAML-конфигурация, которую уже загружает `AgentRuntime`:

```yaml
trajectory_policy:
  policy_id: transfer-trajectory
  policy_version: 2026.08.23
  history_contract:
    source: trusted_immutable_snapshot
    expected_history_ref: required_on_request
    expected_history_version: required_on_request
    required_integrity: verified
    required_status: current
    request_snapshot_identity: [tenant_id, subject_id]
    snapshot_policy_identity: [policy_id, policy_version]
    on_absent_malformed_missing_corrupt_stale_or_unverified: deny
  request_fingerprint:
    algorithm: sha256_canonical_json
    include:
      - action
      - tenant_id
      - subject_id
      - expected_history_ref
      - expected_history_version
      - sequence_number
      - window_id
      - policy_id
      - policy_version
      - sorted_significant_fingerprints
      - sorted_counter_deltas
    caller_supplied_value_allowed: false
  numeric_contract:
    type: decimal
    minimum: "0"
    maximum: "999999999999.999999"
    maximum_scale: 6
    local_precision: 32
    trap_rounding_and_decimal_errors: true
    on_arithmetic_error: deny
  collection_contract:
    maximum_fingerprints_per_request_or_snapshot: 16
    maximum_counters_per_request_or_snapshot: 32
  rules:
    - kind: value_binding
      rule_id: destination-binding
      fingerprint_name: destination
    - kind: cumulative_limit
      rule_id: daily-amount-limit
      counter_name: amount
      limit: "100.00"
      window_id: from_request_and_snapshot
      required_window_state: open
    - kind: required_predecessor
      rule_id: destination-confirmed-first
      predecessor: confirm_destination
    - kind: required_approval
      rule_id: transfer-approval
      approval_scope: transfer
      bind_to: request_fingerprint
  decisions:
    - allow
    - deny
    - approval_required
```

Минимальные declarative rule kinds имеют узкий смысл:

- `value_binding` сравнивает fingerprint текущего поля с fingerprint того же
  поля в доверенной истории;
- `cumulative_limit` складывает сохранённый счётчик и текущую дельту только в
  совпадающем открытом окне с точной арифметикой из `numeric_contract`;
- `required_predecessor` требует именованный более ранний шаг в
  `observed_sequence`;
- `required_approval` ищет активную запись нужного `approval_scope`, связанную
  с текущим `request_fingerprint`.

`request_fingerprint` не является свободным полем request. Исполняемый контракт
канонически сериализует перечисленную identity запроса, сортирует fingerprints
и counter deltas по имени, нормализует Decimal без потери точности и вычисляет
SHA-256. Поэтому approval от прежних action, tenant/subject, history ref/version,
sequence, window или policy id/version не авторизует изменённый запрос.

Значения счётчиков принимаются только как конечные неотрицательные `Decimal` со
scale не более 6 и значением не более `999999999999.999999`. Сложение выполняется
в локальном `Decimal` context с precision 32 и traps для округления и
арифметических ошибок, поэтому поведение не зависит от глобального context.
Выход суммы за диапазон или иная arithmetic failure закрыто дают `deny` с
причиной `counter_arithmetic_error`; в telemetry попадает состояние
`arithmetic_error`, а не число.

Запрос и снимок истории содержат не более 16 отпечатков и 32 счётчиков каждый.
Эти границы проверяются при создании объектов и не позволяют формально
допустимому запросу переполнить строковые сводки обязательного события аудита.
Максимальные разрешённые наборы укладываются в лимит 8192 символов для каждого
поля телеметрии даже при несовпадающих именах в запросе и снимке.

Для `required_approval` binding проверяется до состояния записи. Любая
`rejected`, `revoked` или `expired` запись требуемого scope, связанная именно с
текущим `request_fingerprint`, закрыто даёт `deny` с причиной
`required_approval_inactive`, даже если рядом есть `approved`. Записи того же
scope для другого request не отменяют текущий binding: при отсутствии записи
для текущего fingerprint результатом будет `approval_required` с причиной
`approval_binding_mismatch`. Перед `allow` агрегированное `approval_state`
обязано согласовываться с однородным состоянием связанных записей; отсутствие
записей при агрегированном `approved`, смешанные `approved`/`pending` или иное
расхождение дают `deny` с причиной `approval_state_mismatch`.

Исполняемый учебный контракт в `agent_runtime_ref/trajectory.py` отражает эту
семантику frozen dataclasses, но намеренно не парсит приведённый YAML и не
подключён к `AgentRuntime`. `TrajectoryRequest` содержит `action`,
`tenant_id`, `subject_id`, `expected_history_ref`, `expected_history_version`,
`sequence_number`, `fingerprints`, `counters` и `window_id`. Доверенный
`TrajectorySnapshot` содержит как минимум `history_ref`, `history_version`,
`tenant_id`, `subject_id`, `policy_id`, `policy_version`, `integrity`, `status`,
`observed_sequence`, нормализованные `fingerprints`, `counters`, `window_id`,
`window_state`, `approval_records` и `approval_state`. Каждая запись
подтверждения хранит `approval_id`, `scope`, связанный с вычисленным запросом
`request_fingerprint` и `state`; сырые реквизиты и секреты в snapshot или
событие решения не входят.

Evaluator получает request и готовый snapshot явными аргументами. Он не читает
историю из model context, prompt, памяти модели или compaction summary. `None`
на публичной границе даёт `deny/history_missing`, а mapping или объект чужого
типа — `deny/history_malformed`; их содержимое не отражается в решении. Затем он
закрыто отклоняет missing, corrupt, stale и unverified history, несовпадение
history ref/version, request/snapshot identity, snapshot/policy identity, номера
последовательности или окна и детерминированно проверяет rules в объявленном
порядке. Результат несёт `policy_id`, `policy_version`,
`rule_id`, `reason`, `history_ref`, `history_version`, `sequence_summary`,
`sequence_ref`, `fingerprints`, `counters`, `window_id`, `window_state`,
`approval_state` и `decision`; точная форма события описана в
[схеме трасс](trace-schema.md).

Само значение `integrity: verified` является входным утверждением доверенного
поставщика snapshot. Production-контур обязан отдельно проверять подпись,
происхождение и актуальность, а также обеспечивать транзакционную фиксацию
версии, счётчиков, решения и внешнего эффекта. Учебная функция этого не делает.

Идентификаторы исполняемого контракта ограничены lowercase ASCII slug длиной до
64 символов; history references — lowercase URI-like значениями длиной до 256
символов без whitespace/control characters. Финальный строковый telemetry
payload также проверяется allowlist и лимитом длины. Это только structural
safeguard: доверенный provider обязан отдельно не допускать семантические
секреты внутри формально допустимых identifiers, references и hashes.

Валидация исполняемого контракта использует следующие стабильные сообщения:
`Trajectory field must be a string: {field}`,
`Trajectory field is required: {field}`,
`Trajectory identifier is invalid: {field}`,
`Trajectory reference is invalid: {field}`,
`Trajectory telemetry value is invalid: {field}`,
`Trajectory field must be an integer: {field}`,
`Trajectory integer must not be negative: {field}`,
`Trajectory integer must be positive: {field}`,
`Trajectory field is not supported: {field}={normalized}`,
`Trajectory fingerprint must be sha256: {field}`,
`Trajectory counter value must be a Decimal: {field}`,
`Trajectory counter value must be finite: {field}`,
`Trajectory counter value must not be negative: {field}`,
`Trajectory counter scale exceeds maximum: {field}`,
`Trajectory counter value exceeds maximum: {field}`,
`Trajectory {label} must be a tuple`,
`Trajectory {label} entries must be {item_type.__name__}`,
`Trajectory {label} must contain at most {maximum} entries`,
`Trajectory {label} names must be unique`,
`Trajectory approval record IDs must be unique`,
`Trajectory counter limit must be positive: {counter_name}`,
`Trajectory policy must contain at least one rule`,
`Trajectory rules entries must be trajectory rule objects`,
`Trajectory rule IDs must be unique`,
`Trajectory fingerprint request must be TrajectoryRequest`,
`Trajectory fingerprint policy must be TrajectoryPolicy`,
`Trajectory request must be TrajectoryRequest`,
`Trajectory policy must be TrajectoryPolicy`.

## Что должна добавить промышленная схема

Как только в среде выполнения появляются MCP с состоянием и возобновляемые сессии возможностей, набор политик уже должен описывать не только допустимость возможности “в принципе”, но и то, как управляется ее живой жизненный цикл сессии.

Здесь почти сразу становятся полезны такие поля:

- `trusted_verifier_contracts`
- `verifier_contract_required_for_high_risk`
- `on_untrusted_verifier_contract`
- `capability_session_mode`
- `resume_policy`
- `on_session_expiry`
- `progress_event_policy`
- `elicitation_policy`
- `reinit_requires_approval`
- `approval_mode`
- `approval_delegate`
- `classifier_verdict_policy`
- `escalate_to_human_if`
- `subagent_handoff_policy`
- `authorization_mode`
- `delegated_principal_policy`
- `token_reuse_policy`
- `on_authorization_revoke`
- `mcp_discovery_source`
- `mcp_server_owner`
- `mcp_auth_mode`
- `shadow_mcp_handling`

Именно они не дают ситуации, когда набор политик формально одобряет возможность, но оставляет ее реальный жизненный цикл сессии вне контроля.

Microsoft Foundry Open Trust Stack полезен здесь как внешний ориентир: политика должна компилироваться в именованные runtime checkpoints, а не оставаться prose рядом с eval report.[^microsoft-open-trust-stack] В переносимом YAML это может выглядеть так:

```yaml
control_checkpoints:
  - checkpoint: tool_execution
    policy_requirement: no_external_write_without_approval
    predicate: risk_tier == "high" and side_effect == "external_write"
    action: require_approval
    audit_fields:
      - checkpoint
      - policy_requirement
      - predicate_result
      - action
      - control_version
      - eval_case_id
      - trace_id
```

Минимальный contract surface: `checkpoint`, `policy_requirement`, `predicate` или `judge`, `action`, `control_version`, `eval_case_id`, `trace_id` и `observed_signal`. Checkpoints стоит называть по местам агентного цикла: `input`, `llm`, `state`, `tool_execution` и `output`. Тогда failed eval можно связать не только с prompt diff, но и с конкретным runtime hook, audit event и regression case.

Таксономия паттернов рабочих процессов у Anthropic добавляет сюда еще одно полезное контрактное измерение.[^anthropic] По мере взросления набор политик должен описывать не только то, разрешена ли возможность вообще, но и в каких схемах оркестрации она допустима.

Здесь быстро становятся полезны и такие поля, как:

- `allowed_orchestration_patterns`
- `disallowed_orchestration_patterns`
- `worker_inheritance_policy`
- `worker_capability_subset`
- `review_required_before_worker_write`

Именно они помогают управляемому контракту отвечать на вопросы:

- можно ли вызывать возможность внутри `prompt chaining`, `routing` или `parallelization`;
- наследуют ли делегированные исполнители в схеме `orchestrator-workers` контекст подтверждения или делегированной авторизации;
- может ли исполнитель запросить дополнительные возможности или работает только с ограниченным подмножеством;
- должен ли результат исполнителя пройти проверку до того, как будет выполнена любая записывающая возможность.

Заодно они помогают избежать и второго дрейфа: когда путь подтверждения с делегированием уже существует в поведении продукта, но все еще не представлен как управляемый контракт.

Как только система взрослеет, для набора политик почти сразу полезно добавить:

- `bundle_version`
- `artifact_lineage`
- `change_id`
- `release_identity`
- `approval_contracts`
- `runtime_control_schema`
- `sandbox_profile_contract`
- `sandbox_profile_review_required`
- `contract_version`
- `deprecated_rules`
- `redaction_policy`

Если возможность может выполняться через путь с песочницей, набор политик также должен ссылаться на контракт профиля песочницы или явно требовать его разбора, иначе рабочая область, права оболочки и файловой системы и поведение снимка/возобновления останутся вне идентичности выпуска.

Это превращает слой политик из набора файлов в полноценную поверхность выпуска.

## Почему набор политик и каталог возможностей нельзя разводить слишком далеко

Есть плохая крайность: набор политик живет отдельно, каталог возможностей отдельно, правила подтверждения отдельно, и между ними нет устойчивых ссылок.

Тогда быстро появляются проблемы:

- возможность есть в каталоге, но для нее нет контракта подтверждения;
- политика знает имя возможности, которой уже нет;
- аудит видит решение, но не может связать его с версией набора.

Поэтому практическое правило простое:

- каталог возможностей описывает, что система умеет;
- набор политик описывает, как, при каких условиях и в каких схемах оркестрации это можно использовать;
- контракт подтверждения описывает, где система обязана остановиться и уступить человеку;
- контракт авторизации описывает, от чьей идентичности и с какой делегированной областью действия вообще может быть выполнено действие;
- контракт управления MCP описывает, из какого утвержденного реестра пришла возможность, кто владеет MCP-сервером, каким режимом авторизации она защищена и что делать, если обнаружен теневой путь MCP;
- политика контрактов проверяющего описывает, каким контрактам проверяющего вообще можно доверять для оценивания высокого риска, доказательств раскатки и решений по заверению.

Эталонная среда исполнения делает этот стык конкретным в `capabilities.yaml` и `policy.yaml`: записи возможностей содержат `tool_principal`, `risk_tier`, `network_access`, `allowed_egress`, `timeout_seconds` и `idempotency_key_required`, а policy-записи содержат `run_precheck`, `require_tenant`, `deny_if_principal_missing`, решения по возможностям для `search_docs`, `create_ticket` и `run_shell`, записываемые в память `allow_kinds` (`validated_fact` и `session_summary`) и исполнительный уровень `allow_network_access`. И здесь загрузчик политик явно валидирует эту структуру: `Policy config must be a mapping`, `'policy' must be a mapping`, `'run_precheck' must be a mapping`, `'run_precheck.require_tenant' must be a boolean`, `'run_precheck.deny_if_principal_missing' must be a boolean`, `'{label}' must be a boolean`, `'memory_write' must be a mapping`, `'allow_kinds' must be a list`, `memory_write.allow_kinds entries must be strings`, `memory_write.allow_kinds entries must not be empty`, `memory_write.allow_kinds entries must be unique`, `'execution' must be a mapping`, `'allow_network_access' must be a list`, `execution.allow_network_access entries must be strings`, `execution.allow_network_access entries must not be empty`, `execution.allow_network_access entries must be unique`, `Policy capability names must be strings`, `Policy capability name must not be empty`, `Policy capability names must be unique`, `Policy capability entries must be CapabilityPolicy`, `Policy precheck request must be RunRequest`, `Policy context must be RunContext`, `Policy tool request must be ToolRequest`, `Policy capability must be CapabilitySpec`, `'capabilities' must be a mapping`, `Policy action must be a string`, `Policy action is not supported: {action}`, `Policy field must be a string: {field}`, `Policy field is required: {field}`, `Policy decision must be a string`, `Policy decision is not supported: {decision}`, `Policy approver must be a string`, `Policy approver must not be empty: {capability_name}`, `Policy memory kind must be a string`, `Policy memory kind must not be empty` и `Policy for capability {name!r} must be a mapping`.

## Что сделать сразу

Сначала пройди по короткому списку и отдельно отметь все ответы «нет»:

- Есть ли версионированный набор политик?
- Можно ли связать его с раскаткой и разбором инцидента?
- Контракт подтверждения машиночитаем или только описан словами?
- Ясно ли, какие поля обязан содержать запрос на подтверждение?
- Есть ли связь между набором политик и каталогом возможностей?
- Можно ли понять, какая версия политики и какая идентичность выпуска были активны в момент трассы?
- Явно ли описано, каким контрактам проверяющего можно доверять для оценивания высокого риска или доказательств раскатки?

Если несколько ответов подряд «нет», значит слой политик у тебя пока существует, но еще не оформлен как полноценный рабочий артефакт.

## Что делать дальше

- [Схема трасс и каталог событий](trace-schema.md)
- [Схема наборов для оценки и правил проверки](eval-schema.md)
- [Схема артефактов жизненного цикла](lifecycle-artifact-schema.md)
- [Эталонный пакет](reference-package.md)
- [Шаблоны политик и проверочные списки по кейсам](policy-templates.md)

[^anthropic]: [Anthropic, Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
[^microsoft-open-trust-stack]: Microsoft Foundry Blog, [Build agents you can trust across any framework with open evals and a control standard](https://devblogs.microsoft.com/foundry/build-2026-open-trust-stack-ai-agents/).
