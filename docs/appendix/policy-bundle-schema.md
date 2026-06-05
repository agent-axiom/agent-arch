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

- versioned;
- reviewable;
- traceable;
- releasable.

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
- «manager approves ticket creation»;
- «security signs off on dangerous actions».

Этого недостаточно.

Контракт подтверждения полезно делать явным:

- кто может одобрять;
- какой класс действий требует подтверждения;
- какие поля должны попасть в запрос на подтверждение;
- какие решения допустимы;
- что происходит после reject;
- может ли run pause, resume, expire или cancel;
- что должно остаться в журнале аудита.

## Пример контракта подтверждения

Ниже рабочий skeleton:

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

А если runtime уже обращается с наборами как с управляемыми поверхностями выпуска, неизбежно появляется и следующий вопрос:

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

Этот же шлюз явно фиксирует форму входного набора средств управления: проверка конфигурации средств управления сообщает `Controls policy config must be a mapping`, `'controls' must be a mapping`, `'controls.require' must be a list`, `'controls.block_if' must be a list`, `controls.require entries must be strings`, `controls.require entries must not be empty`, `controls.require entries must be unique`, `controls.block_if entries must be strings`, `controls.block_if entries must not be empty` и `controls.block_if entries must be unique`; переопределения сигналов сообщают `Assessment signals must be a mapping`, `Assessment signal key must be a string`, `Assessment signal key must not be empty`, `Assessment signal keys must be unique` и `Assessment signal value must be a boolean: {field}`. Поэтому оператор может отличить испорченный набор политик от провалившейся, но корректно сформированной оценки средств управления.

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

Таксономия паттернов рабочих процессов у Anthropic добавляет сюда еще одно полезное контрактное измерение.[^anthropic] По мере взросления набор политик должен описывать не только то, разрешена ли возможность вообще, но и в каких схемах оркестрации она допустима.

Здесь быстро становятся полезны и такие поля, как:

- `allowed_orchestration_patterns`
- `disallowed_orchestration_patterns`
- `worker_inheritance_policy`
- `worker_capability_subset`
- `review_required_before_worker_write`

Именно они помогают управляемому контракту отвечать на вопросы:

- можно ли вызывать capability внутри `prompt chaining`, `routing` или `parallelization`;
- наследуют ли делегированные исполнители в схеме `orchestrator-workers` контекст подтверждения или делегированной авторизации;
- может ли worker запросить дополнительные capabilities или работает только с ограниченным subset;
- должен ли worker output пройти review до того, как будет выполнена любая write-capability.

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

Эталонный runtime делает этот стык конкретным в `capabilities.yaml` и `policy.yaml`: capability entries содержат `tool_principal`, `risk_tier`, `network_access`, `allowed_egress`, `timeout_seconds` и `idempotency_key_required`, а policy entries содержат `run_precheck`, `require_tenant`, `deny_if_principal_missing`, capability decisions для `search_docs`, `create_ticket` и `run_shell`, memory-write `allow_kinds` (`validated_fact` и `session_summary`) и execution-level `allow_network_access`. Policy loader явно валидирует эту структуру: `Policy config must be a mapping`, `'policy' must be a mapping`, `'run_precheck' must be a mapping`, `'run_precheck.require_tenant' must be a boolean`, `'run_precheck.deny_if_principal_missing' must be a boolean`, `'{label}' must be a boolean`, `'memory_write' must be a mapping`, `'allow_kinds' must be a list`, `memory_write.allow_kinds entries must be strings`, `memory_write.allow_kinds entries must not be empty`, `memory_write.allow_kinds entries must be unique`, `'execution' must be a mapping`, `'allow_network_access' must be a list`, `execution.allow_network_access entries must be strings`, `execution.allow_network_access entries must not be empty`, `execution.allow_network_access entries must be unique`, `Policy capability names must be strings`, `Policy capability name must not be empty`, `Policy capability names must be unique`, `Policy capability entries must be CapabilityPolicy`, `Policy precheck request must be RunRequest`, `Policy context must be RunContext`, `Policy tool request must be ToolRequest`, `Policy capability must be CapabilitySpec`, `'capabilities' must be a mapping`, `Policy action must be a string`, `Policy action is not supported: {action}`, `Policy field must be a string: {field}`, `Policy field is required: {field}`, `Policy decision must be a string`, `Policy decision is not supported: {decision}`, `Policy approver must be a string`, `Policy approver must not be empty: {capability_name}`, `Policy memory kind must be a string`, `Policy memory kind must not be empty` и `Policy for capability {name!r} must be a mapping`.

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
