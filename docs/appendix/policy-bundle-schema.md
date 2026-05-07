# Схема набора политик и контракта подтверждения

Эта страница связывает несколько уже написанных тем:

- [Глава 4. Инструментальный шлюз, подтверждения и журнал аудита](../book/part-ii/chapter-4.md)
- [Глава 17. Слой политик и каталог возможностей](../book/part-vii/chapter-17.md)
- [Глава 20. Change management для агентных систем](../book/part-viii/chapter-20.md)
- [Сквозная цепочка доказательств: от запроса к решению о rollout](../book/part-v/evidence-spine.md)

И опирается на справочный пакет:

- [Справочный пакет](reference-package.md)

Если страницы о схеме трасс и схеме оценки отвечают на вопросы:

- как описывать фактическое поведение;
- как описывать ожидаемое поведение;

то эта страница отвечает на третий вопрос:

- как описывать управляющие правила, которые стоят между рассуждением и внешним действием.

## Почему набор политик полезно мыслить как артефакт

Одна из самых частых ошибок в агентных системах устроена так:

- правила частично живут в prompt;
- частично в коде шлюза;
- частично в интерфейсе подтверждения;
- частично в голове команды.

Пока система маленькая, это может работать. Но как только появляется управление изменениями, аудит и поэтапная раскатка, такой слой политик становится слишком размытым.

Поэтому полезно собирать `policy bundle` как отдельный артефакт.

## Что такое набор политик

Под `policy bundle` здесь удобно понимать набор связанных правил, который выпускается как единое целое:

- runtime policy;
- tool policy;
- approval policy;
- runtime-control rules для pause/resume и background paths;
- memory write rules;
- escalation rules;
- egress rules;
- expectations around trusted verifier contracts for high-risk eval и rollout evidence.

Смысл не в том, что все должно лежать в одном YAML-файле. Смысл в том, что такой набор должен быть:

- versioned;
- reviewable;
- traceable;
- releasable.

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

## Как набор политик связан с жизненным циклом

Из Part VIII здесь особенно важны две мысли:

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

## Что уже умеет справочный рантайм

В `agent_runtime_ref` сейчас уже есть:

- [policy.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/policy.yaml)
- [approvals.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/approvals.yaml)
- [controls.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/controls.yaml)
- [change.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/change.yaml)
- [runtime-controls.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/runtime-controls.yaml)

То есть пакет уже живет в модели, где политики, подтверждения и runtime-control contracts не просто побочные настройки, а отдельные управляемые артефакты.

## Что должна добавить промышленная схема

Как только в runtime появляются stateful MCP и resumable capability sessions, набор политик уже должен описывать не только допустимость capability “в принципе”, но и то, как управляется ее живая session lifecycle.

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

Именно они не дают ситуации, когда policy bundle формально одобряет capability, но оставляет ее реальный session lifecycle вне контроля.

Таксономия workflow-паттернов у Anthropic добавляет сюда еще одно полезное контрактное измерение.[^anthropic] По мере взросления policy bundle должен описывать не только то, разрешена ли capability вообще, но и в каких orchestration patterns она допустима.

Здесь быстро становятся полезны и такие поля, как:

- `allowed_orchestration_patterns`
- `disallowed_orchestration_patterns`
- `worker_inheritance_policy`
- `worker_capability_subset`
- `review_required_before_worker_write`

Именно они помогают governed contract отвечать на вопросы:

- можно ли вызывать capability внутри `prompt chaining`, `routing` или `parallelization`;
- наследуют ли delegated workers в `orchestrator-workers` approval или delegated authorization context;
- может ли worker запросить дополнительные capabilities или работает только с ограниченным subset;
- должен ли worker output пройти review до того, как будет выполнена любая write-capability.

Заодно они помогают избежать и второго дрейфа: когда delegated approval path уже существует в product behavior, но все еще не представлен как governed contract.

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

Если capability может выполняться в sandbox-backed path, policy bundle также должен ссылаться на sandbox profile contract или явно требовать его review, иначе workspace, shell/filesystem permissions и snapshot/resume behavior останутся вне release identity.

Это превращает слой политик из набора файлов в полноценную поверхность выпуска.

## Почему набор политик и каталог возможностей нельзя разводить слишком далеко

Есть плохая крайность: набор политик живет отдельно, каталог возможностей отдельно, правила подтверждения отдельно, и между ними нет устойчивых ссылок.

Тогда быстро появляются проблемы:

- возможность есть в каталоге, но для нее нет контракта подтверждения;
- политика знает имя возможности, которой уже нет;
- аудит видит решение, но не может связать его с версией набора.

Поэтому практическое правило простое:

- каталог возможностей описывает, что система умеет;
- набор политик описывает, как, при каких условиях и в каких orchestration patterns это можно использовать;
- контракт подтверждения описывает, где система обязана остановиться и уступить человеку;
- authorization contract описывает, под чьей identity и с каким delegated scope действие вообще может быть выполнено;
- MCP governance contract описывает, из какого approved registry пришла capability, кто owner у MCP server, какой auth mode ее защищает и что делать, если обнаружен shadow MCP path;
- verifier contract policy описывает, каким verifier contracts вообще можно доверять для high-risk grading, rollout evidence или assurance decisions.

Reference runtime делает этот стык конкретным в `capabilities.yaml` и `policy.yaml`: capability entries содержат `tool_principal`, `risk_tier`, `network_access`, `allowed_egress`, `timeout_seconds` и `idempotency_key_required`, а policy entries содержат `run_precheck`, `require_tenant`, `deny_if_principal_missing`, capability decisions для `search_docs`, `create_ticket` и `run_shell`, memory-write `allow_kinds` (`validated_fact` и `session_summary`) и execution-level `allow_network_access`. Policy loader явно валидирует эту структуру: `'policy' must be a mapping`, `'run_precheck' must be a mapping`, `'run_precheck.require_tenant' must be a boolean`, `'run_precheck.deny_if_principal_missing' must be a boolean`, `'{label}' must be a boolean`, `'memory_write' must be a mapping`, `'allow_kinds' must be a list`, `memory_write.allow_kinds entries must be strings`, `memory_write.allow_kinds entries must not be empty`, `memory_write.allow_kinds entries must be unique`, `'execution' must be a mapping`, `'allow_network_access' must be a list`, `execution.allow_network_access entries must be strings`, `execution.allow_network_access entries must not be empty`, `execution.allow_network_access entries must be unique`, `Policy capability names must be strings`, `Policy capability name must not be empty`, `Policy capability names must be unique`, `Policy capability entries must be CapabilityPolicy`, `Policy precheck request must be RunRequest`, `Policy context must be RunContext`, `Policy tool request must be ToolRequest`, `Policy capability must be CapabilitySpec`, `Policy decision must be a string`, `Policy decision is not supported: {decision}`, `Policy approver must be a string`, `Policy approver must not be empty: {capability_name}`, `Policy memory kind must be a string`, `Policy memory kind must not be empty` и `Policy for capability {name!r} must be a mapping`.

## Что сделать сразу

Сначала пройди по короткому списку и отдельно отметь все ответы «нет»:

- Есть ли версионированный набор политик?
- Можно ли связать его с раскаткой и разбором инцидента?
- Контракт подтверждения машиночитаем или только описан словами?
- Ясно ли, какие поля обязан содержать запрос на подтверждение?
- Есть ли связь между набором политик и каталогом возможностей?
- Можно ли понять, какая версия политики и какая идентичность выпуска были активны в момент трассы?
- Явно ли описано, каким verifier contracts можно доверять для high-risk grading или rollout evidence?

Если несколько ответов подряд «нет», значит слой политик у тебя пока существует, но еще не оформлен как полноценный рабочий артефакт.

## Что делать дальше

- [Схема трасс и каталог событий](trace-schema.md)
- [Схема наборов для оценки и правил проверки](eval-schema.md)
- [Схема артефактов жизненного цикла](lifecycle-artifact-schema.md)
- [Справочный пакет](reference-package.md)
- [Шаблоны политик и проверочные списки по кейсам](policy-templates.md)

[^anthropic]: [Anthropic, Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
