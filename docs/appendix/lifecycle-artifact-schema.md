# Схема артефактов жизненного цикла

Эта страница собирает в одном месте минимальный contract layer для lifecycle-артефактов: change record, approved artifact bundle и retirement plan. Если trace schema отвечает на вопрос "что произошло", а eval schema отвечает на вопрос "как это оценивать", то lifecycle artifact schema отвечает на вопрос "что именно было одобрено, изменено, заменено или выведено из эксплуатации".

!!! example "Lifecycle artifact для duplicate-ticket thread"
    Для support-triage bundle должен удерживать вместе не только `policy_bundle` и `eval_dataset`, но и evidence о duplicate-ticket guard: требование `idempotency_key`, approval record, trace с `side_effect_unknown`, `duplicate_ticket_eval_passed` и rollout gate. Тогда incident review восстанавливает одну цепочку `change -> bundle -> approval -> trace -> eval -> rollout`, а не ищет доказательства по разным страницам.

!!! note "Canonical lifecycle cases"
    Lifecycle artifacts должны удерживать разные artifact chains для трех canonical cases. **Support triage** связывает change record, approved artifact bundle, approval record, trace, eval dataset, rollout gate и retirement plan для duplicate-ticket guard. **Internal knowledge assistant** связывает retrieval policy, memory policy, source provenance, access-control review и knowledge-base replacement plan. **Incident coordination** связывает escalation policy, notification capability, response ownership map, handoff artifact и post-incident learning retirement or replacement plan.

Она напрямую связана и со страницей [Сквозная цепочка доказательств: от запроса к решению о rollout](../book/part-v/evidence-spine.md), потому что lifecycle-артефакты входят в ту управляемую запись, на которую потом опираются judgment и incident review.

## 1. Зачем это нужно

У production-grade agent system есть несколько классов артефактов, которые нельзя держать только в голове команды или в wiki:

- change records;
- approved artifact bundles;
- retirement plans;
- replacement mappings;
- runtime-control schemas и contract-version linkages;
- operational approvals и lifecycle decisions;
- capability-session interruption, expiry и re-initialization rules, если они уже входят в runtime contract;
- delegated authorization rules, assumptions про principal binding и revoke behavior, если они уже входят в runtime contract;
- verifier contracts, grading rubrics и rules для evidence linkage, если release или assurance зависят от verifier output;
- структурированные handoff artifacts, если длинная работа пересекает границу context reset или role handoff.

Без этого change management быстро разваливается на устные договоренности. А incident review превращается в расследование того, кто и когда "примерно поменял policy или routing".

## 2. Базовые сущности

Минимальный lifecycle layer удобно строить вокруг трех сущностей:

- `change_record`
- `artifact_bundle`
- `retirement_plan`

Этого уже достаточно, чтобы связать design review, release gate, assurance loop и end-of-life discipline.

## 3. Change record

`change_record` описывает конкретное изменение и его operational semantics.

Минимальные поля:

```yaml
kind: change_record
change_id: chg-2026-04-07-001
title: "Tighten outbound policy for ticket_write"
change_type: policy_update
risk_level: high
owner: platform-safety
affected_surfaces:
  - policy_bundle
  - capability_contract
  - runtime_control_schema
  - capability_session_contract
  - sandbox_profile_contract
  - rollout_rules
eval_requirements:
  - offline_regression
  - targeted_safety_eval
approval_requirements:
  - safety_review
  - platform_review
rollback_unit:
  - policy_bundle:v4
  - approvals_bundle:v3
status: approved
```

Что здесь особенно важно:

- `affected_surfaces` не дает делать вид, будто изменение маленькое;
- `eval_requirements` связывает change management с eval loop;
- `rollback_unit` заставляет заранее понимать, что именно откатывается;
- `status` нужен не как бюрократия, а как operational fact.

А если в системе уже есть approval-bound, stateful capability sessions или sandbox-backed execution, change record почти всегда стоит делать достаточно явным, чтобы было видно, входили ли interruption behavior, expiry handling, re-init semantics, delegated authorization rules и sandbox profile contract в reviewed surface.

## 4. Approved artifact bundle

`artifact_bundle` фиксирует набор артефактов, которые считаются доверенными и совместимыми друг с другом в конкретной release-конфигурации. На практике это еще и контрактная поверхность, которая задает управляемую идентичность выпуска.

Эталонный runtime хранит этот contract в `artifacts.yaml`: `bundle_name` — например, `support-triage-runtime-bundle` — `version`, `provenance_required`, `signed` и `session_control_owner` описывают bundle identity и accountability; malformed identity и provenance fields явно падают с `bundle.version must be a string`, `bundle.version is required`, `'bundle.provenance_required' must be a boolean` и `'bundle.signed' must be a boolean`; `review_evidence` также может указывать на evidence refs вроде `trace:sandbox_profile_reviewed` и на evidence chain `duplicate_ticket_guard`; а `artifacts` явно перечисляет release-bearing files: `agent.yaml`, `capabilities.yaml`, `policy.yaml`, `memory.yaml`, `controls.yaml`, `approvals.yaml`, `runtime-controls.yaml`, `change.yaml`, `retirement.yaml`, `eval-dataset.json` и `runtime-control-bundle-metadata`.

```yaml
kind: artifact_bundle
bundle_id: bundle-2026-04-07-a
owner: platform-runtime
artifacts:
  model_route: gpt-5.4-tools
  policy_bundle: policy-v4
  approvals_bundle: approvals-v3
  controls_bundle: controls-v2
  runtime_control_schema: runtime-controls-v2
  sandbox_profile: sandbox-profile-v1
  capability_catalog: catalog-v5
  eval_dataset: eval-set-2026-04-07
  verifier_contract: verifier-v2
  contract_version: capability-contract-v5
review_evidence:
  sandbox_profile_reviewed:
    trace_event: sandbox_profile_reviewed
    workspace_manifest_ref: runtime-controls.yaml#runtime_controls.sandbox_profile.workspace
    permissions_profile: restricted-shell-network-denied
    network_secrets_posture: network:denied,secrets:none
    snapshot_policy: required_on_completion
    review_evidence_refs:
      - trace:trace-sandbox-review-001
      - eval:sandbox_profile_review
  duplicate_ticket_guard:
    idempotency_key_required: true
    eval_ref: eval:duplicate_ticket_eval_passed
    approval_ref: approval:apr-2026-04-07-001
    rollout_gate_ref: gate:gate-2026-04-07-001
status: approved
release_scope: canary
provenance:
  change_record: chg-2026-04-07-001
  reviewed_by:
    - safety-review
    - runtime-review
```

Этот слой полезен по трем причинам:

- он отделяет "есть артефакт" от "артефакт одобрен для релиза";
- он делает идентичность выпуска проверяемой, а не неявной договоренностью;
- он делает incident review и rollback гораздо короче.

А когда capability-session governance уже оформлена явно, bundle почти всегда стоит делать достаточно подробным, чтобы было видно не только contract version, но и какие session-control assumptions и семейство контрактов с verifier-ограничениями были одобрены вместе с ним:

- expiry policy;
- re-init policy;
- ownership для stuck или expired capability-session state;
- ожидания по linkage между approval events и session events;
- delegated authorization mode;
- требования к principal binding;
- revoke behavior для paused или in-flight actions;
- версия verifier contract, grading rubric и ожидания по evidence linkage, если rollout или assurance зависят от verifier judgments;
- sandbox profile review evidence, включая `sandbox_profile_reviewed` trace event, `workspace_manifest_ref` и ссылки на eval/rollout evidence, если release identity включает sandbox-backed execution.

## 5. Retirement plan

`retirement_plan` нужен не только для полного выключения агента, но и для controlled replacement capability, policy bundle или artifact family. Эталонный loader также явно фиксирует replacement identity: malformed replacement fields падают с `retirement.replacement_mode must be a string` и `retirement.replacement_mode is required`, рядом с уже описанной validation для `retirement.system_id`.

```yaml
kind: retirement_plan
retirement_id: retire-2026-04-ticket-write-v1
target: capability:ticket_write_v1
trigger: deprecated_capability
replacement: capability:ticket_write_v2
phases:
  - freeze_new_rollouts
  - dual_run
  - traffic_shift
  - expire_paused_runs
  - stop_background_routes
  - revoke_principal
  - archive_artifacts
historical_state:
  traces: retain_90_days
  approvals: retain_180_days
  memory: review_before_delete
status: planned
owner: platform-operations
```

Сильная сторона этого артефакта в том, что он заставляет думать не только о replacement, но и о следах старой системы:

- traces;
- approvals;
- paused-run state;
- ownership фоновых маршрутов;
- principals;
- memory;
- archived bundles;
- структурированные handoff artifacts, в которых фиксировались scope спринта, evaluator critique или решения на границе reset;
- expired capability-session state, если он все еще важен для audit или delayed operator response.

## 6. Как это связано с Part VIII

Эта схема напрямую поддерживает несколько глав:

- Chapter 20: change management;
- Chapter 21: assurance findings, которые становятся lifecycle input;
- Chapter 22: approved artifacts и provenance;
- Chapter 23: replacement и retirement.

Именно поэтому lifecycle artifacts полезно держать не как prose-only documentation, а как reviewable YAML или JSON contract.

Эталонный runtime отражает эту форму в `retirement.yaml`: `system_id` и `replacement_mode` идентифицируют retiring surface, причём эталонный пакет использует `staged_replacement` для controlled handover, `triggers` объясняют, почему начинается retirement (`deprecated_runtime`, `replacement_ready` и `unsafe_capability_pattern`), `required_steps` включает controls вроде `freeze_rollout`, `disable_risky_capabilities`, `stop_memory_write`, `expire_paused_runs`, `stop_background_routes`, `freeze_reinitialization`, `revoke_egress`, `archive_audit_state` и `set_retired_status`, а `session_control_owner`, `emergency_freeze_owner` и `archive_targets` явно фиксируют ownership и retained evidence. Archive list называет `telemetry_jsonl`, `session_exports`, `approval_history`, `paused_run_state`, `capability_session_state` и `runtime_control_bundle` — именно records, которые должны оставаться reviewable после retirement. Executable summary `check-retirement` возвращает `system_id`, `ready`, `triggers`, `missing_steps`, `required_steps`, `archive_targets`, `failed_run_archive_targets`, `support_duplicate_archive_targets` и `replacement_mode`, чтобы оператор видел и незавершённые retirement steps, и точные evidence bundles, которые переживают retirement ради degraded-path и duplicate-ticket review; malformed retirement step overrides падают с `Assessment signals must be a mapping`, `Assessment signal key must be a string`, `Assessment signal key must not be empty`, `Assessment signal keys must be unique` и `Assessment signal value must be a boolean: {field}`.

Lifecycle artifact loaders отделяют malformed release-state inputs от проваленных проверок: `change config must be a mapping`, `artifact bundle config must be a mapping` и `retirement config must be a mapping` отклоняют неверные корни; `change config keys must be strings`, `artifact bundle config keys must be strings` и `retirement config keys must be strings` отклоняют нестроковые YAML keys; `change.change_id must be a string`, `change.change_id is required`, `change.session_control_owner is required`, `change.emergency_freeze_owner is required`, `bundle.bundle_name must be a string`, `bundle.bundle_name is required`, `bundle.session_control_owner is required`, `retirement.system_id must be a string`, `retirement.system_id is required`, `retirement.session_control_owner is required` и `retirement.emergency_freeze_owner is required` отклоняют потерю identity/ownership; списки вроде `required_signals`, `artifacts` и `archive_targets` отклоняют неправильные значения через `{key} must be a list`, `{key} entries must be strings`, `{key} entries must not be empty` и `{key} entries must be unique`; artifact review evidence отклоняет malformed evidence maps через `artifact bundle review_evidence config must be a mapping`, `artifact bundle review_evidence config keys must be strings`, `artifact bundle review_evidence key must not be empty` и `artifact bundle review_evidence keys must be unique`.

## 7. Минимальные инварианты

Если делать совсем коротко, у healthy lifecycle artifact layer должны быть такие инварианты:

- каждый high-risk change имеет `change_record`;
- каждый production rollout указывает на `artifact_bundle`;
- каждый artifact bundle может служить конкретной записью об идентичности выпуска, а не просто рыхлым списком версий;
- каждый artifact bundle связывает runtime-control schema и contract version, если такие controls существуют;
- lineage verifier contract и идентичность семейства контрактов можно восстановить, если release или assurance зависят от graded outcomes;
- sandbox profile review evidence можно восстановить из bundle, trace или eval artifact, если rollout требовал `sandbox_profile_reviewed`;
- у deprecated artifact есть `retirement_plan` или явное исключение;
- retirement или replacement path объясняет, что происходит с paused runs, handoff artifacts и expired capability-session state, если такие контуры вообще есть;
- delegated authorization ownership и revoke behavior можно восстановить для затронутых runs, если такие controls существуют;
- lifecycle artifacts имеют owner и version;
- incident review может восстановить связку `change -> bundle -> run -> retirement`;
- session-control ownership можно восстановить для expired, paused или re-initialized capability paths.

## 8. Что чаще всего ломается

Проблемы обычно очень узнаваемые:

- bundle собирается "на словах", а не как артефакт;
- change records живут отдельно от eval requirements;
- retirement есть в roadmap, но не в operational config;
- replacement делается без dual-run semantics;
- historical state не имеет retention owner;
- provenance заканчивается на уровне git commit и не доходит до runtime bundle;
- paused-run и expired-session state теряются при replacement, хотя они еще могут быть нужны операторам;
- lineage verifier contract теряется, хотя от него зависели rollout или assurance decisions;
- bundle указывает `sandbox_profile`, но не хранит ссылку на review evidence по workspace, permissions и snapshot/resume policy.

## 9. Что сделать сразу

Сначала пройди по короткому списку и отдельно отметь все ответы «нет»:

- Есть ли у high-risk changes явные change records?
- Есть ли approved artifact bundle, а не просто список последних YAML-файлов?
- Можно ли по incident trace восстановить активный bundle и его идентичность выпуска?
- Можно ли понять, под каким семейством контрактов с verifier-ограничениями выпуск был одобрен?
- Если bundle включает `sandbox_profile`, можно ли найти review evidence для workspace, permissions и snapshot/resume policy?
- Есть ли retirement plan для deprecated capabilities и policy bundles?
- Есть ли owner у archived state после replacement?
- Понятен ли rollback unit на уровне lifecycle artifacts?

Если на несколько вопросов подряд ответ "нет", у тебя уже может быть хороший SDLC и даже хороший rollout, но lifecycle layer пока еще не собран до конца.

## Что делать дальше

- [Схема трасс и каталог событий](trace-schema.md)
- [Схема наборов для оценки и правил проверки](eval-schema.md)
- [Схема набора политик и контракта подтверждения](policy-bundle-schema.md)
- [Эталонный пакет](reference-package.md)
- [Глава 20. Change management для агентных систем](../book/part-viii/chapter-20.md)
- [Глава 22. Цепочка поставки, происхождение и доверенные артефакты](../book/part-viii/chapter-22.md)
- [Глава 23. Retirement, replacement и end-of-life discipline](../book/part-viii/chapter-23.md)
