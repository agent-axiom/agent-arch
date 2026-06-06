# Схема проверки изменений и шлюза поэтапного выпуска

Эта страница собирает в одном месте минимальный контрактный слой для проверки изменений и шлюза поэтапного выпуска в агентных системах. Он нужен в тот момент, когда команда уже понимает, что изменения в политике, промптах, маршрутизации моделей, поиске или доступе к инструментам нельзя выпускать "по ощущению", но еще не оформила эти проверки в явные артефакты.

Если [схема артефактов жизненного цикла](lifecycle-artifact-schema.md) отвечает на вопрос "какие сущности жизненного цикла вообще должны существовать", то эта схема проверки изменений и поэтапного выпуска отвечает на вопрос "какие поля нужны, чтобы реально принять решение о выпуске".

## 1. Зачем нужен отдельный слой схем

Проверка изменений в агентной системе часто распадается на несколько несвязанных фрагментов:

- инженерное ревью в pull request;
- ревью безопасности где-то в отдельном документе;
- результаты оценивания в CI;
- решение о поэтапном выпуске в чате или устно на созвоне.

Пока система маленькая, это может работать терпимо. Но как только появляется несколько ответственных, высокорисковые действия и поэтапный выпуск, такая схема перестает быть управляемой.

Отдельный слой полезен потому, что он:

- связывает запись изменения с требованиями к оценкам;
- фиксирует шлюз выпуска явно, а не в памяти команды;
- сохраняет стратегию раскатки и радиус воздействия;
- облегчает разбор инцидента и откат.

## 2. Базовые сущности

Минимальный слой здесь обычно строится вокруг двух сущностей:

- `change_review_record`
- `rollout_gate_record`

Этого уже достаточно, чтобы связать Part V, Part VII и Part VIII в одну дисциплину эксплуатации.

## 3. Запись проверки изменений

`change_review_record` описывает, что именно изменилось, кто это проверил и какие условия должны быть выполнены до выкладки.

```yaml
kind: change_review_record
review_id: cr-2026-04-07-001
change_id: chg-2026-04-07-001
owner: platform-runtime
change_type: policy_update
risk_level: high
affected_surfaces:
  - policy_bundle
  - approval_contract
  - delegated_authorization_contract
  - runtime_control_schema
  - capability_session_contract
  - sandbox_profile_contract
  - failed_run_handling
  - rollout_rules
required_reviews:
  - engineering
  - safety
  - runtime_owner
required_evals:
  - offline_regression
  - targeted_safety_eval
  - trace_regression_check
  - failed_run_drill
  - sandbox_profile_review
  - verifier_quality_check
status: approved
```

Ключевые поля здесь такие:

- `affected_surfaces` не дает замаскировать опасное изменение под "небольшую настройку";
- `required_reviews` делает ownership явным;
- `required_evals` помогает не спорить каждый раз заново, что именно надо прогонять;
- `status` нужен как рабочий факт, а не как украшение в тексте.

## 4. Запись шлюза раскатки

`rollout_gate_record` фиксирует уже не качество изменения само по себе, а готовность выпускать его в конкретную волну rollout.

```yaml
kind: rollout_gate_record
gate_id: gate-2026-04-07-001
change_id: chg-2026-04-07-001
bundle_id: bundle-2026-04-07-a
rollout_wave: canary
traffic_scope: 5_percent
required_checks:
  - telemetry_ready
  - oncall_ready
  - rollback_plan_ready
  - approval_path_verified
  - high_risk_flow_checked
  - duplicate_ticket_eval_passed
  - sandbox_profile_reviewed
  - failed_run_traceability_verified
blocking_findings: []
decision: go
# sandbox_profile_reviewed означает, что workspace materialization, permissions
# и snapshot/resume policy были явно проверены для sandbox-backed paths.
# failed_run_traceability_verified означает, что для degraded paths
# проверены traces, release identity и экспортируемые поля вроде failure_reason.
decided_by:
  - runtime_owner
  - safety_owner
```

Этот слой нужен потому, что даже хорошая проверка изменений еще не означает автоматическую готовность к раскатке.

!!! example "Шлюз раскатки для цепочки дубля тикета"
    Для канареечного шлюза разбора обращений поддержки нужно проверять не только `offline_eval_pass`, но и конкретный `duplicate_ticket_eval_passed`: тайм-аут после `create_ticket` воспроизведен, `trace_id` и `idempotency_key` сохранены, исход — один побочный эффект тикета или остановка `side_effect_unknown`, а `blocking_findings` остаются пустыми только если слепой повтор не вернулся.

!!! note "Канонические сценарии раскатки"
    Шлюз раскатки должен проверять разные сигналы готовности для трех канонических сценариев. **Триаж обращений поддержки** требует прохождения оценки дублей тикетов, плана отката, готовности подтверждений и доказательств идемпотентности. **Внутренний ассистент знаний** требует окна свежести поиска, проверки привязки к источникам, проверки происхождения памяти и подтверждения контроля доступа. **Координация инцидентов** требует тренировки эскалации, проверки побочных эффектов уведомлений, готовности владения ответом и шлюза обучения после инцидента.

Это еще важнее, когда раскатка опирается на более содержательные выводы проверяющего, а не только на двоичный статус «прошло/не прошло». Тогда запись шлюза должна явно показывать, проверялись ли для затронутых высокорисковых путей качество проверяющего и связность его доказательной базы.

Как только в среде исполнения появляются подтверждения и состояния сессий возможностей, шлюз еще должен явно фиксировать, было ли поведение при прерывании отдельно проверено, а не просто принято по умолчанию.

## 5. Чем проверка изменений отличается от шлюза раскатки

Эти два слоя часто путают, хотя задачи у них разные:

- `change_review_record` отвечает на вопрос: "можно ли в принципе выпускать это изменение";
- `rollout_gate_record` отвечает на вопрос: "можно ли выпускать его сейчас и в таком масштабе".

Из-за этого у них и поля разные:

- проверка изменений больше смотрит на тип изменения, риски и обязательные оценки;
- шлюз раскатки больше смотрит на телеметрию, готовность дежурной смены, откат, охват трафика, готовность живого контура и обработку прерываний для путей с подтверждением или состоянием сессии.

На практике это обычно означает, что gate должен еще явно фиксировать:

- проверялось ли capability-session expiry behavior до rollout;
- является ли re-init для затронутого path denied, allowed или approval-bound;
- проверялась ли delegated authorization continuity между run traces, approval records и session export;
- были ли changes в orchestration pattern отдельно reviewed как runtime-control changes до rollout;
- был ли sandbox profile contract, включая workspace materialization, permissions и snapshot/resume policy, включен в review, если изменение затрагивает sandbox-backed execution;
- кто owner у emergency freeze, если interruption semantics начнут дрейфовать после релиза.

## 6. Как это связано со схемой оценивания

Проверка изменений и шлюз раскатки тесно связаны со [схемой оценивания](eval-schema.md):

- проверка указывает, какие оценки обязательны;
- шлюз смотрит, достаточно ли результатов для конкретной волны раскатки;
- инциденты и находки потом возвращаются обратно в список обязательных проверок;
- регрессии проверяющего и сбои в связывании доказательств тоже становятся находками, важными для раскатки.

То есть слой оценивания не живет отдельно от дисциплины выпуска, а становится одной из опор шлюза.

## 7. Как это связано со схемой трасс

Шлюз раскатки особенно полезен, когда схема трасс уже собрана:

- по трассам видно, прошли ли высокорисковые пути;
- по сводкам сессий видно, есть ли регрессии;
- по структурированным событиям можно понять, что именно было проверено перед выпуском;
- по сигналам прерывания и истечения срока видно, не деградируют ли запуски с подтверждением раньше, чем это заметят операторы;
- доказательства проверяющего показывают, действительно ли суждения о процессе и исходе, использованные при разборе раскатки, прослеживаются.

Поэтому у зрелой команды трасса и шлюз раскатки почти всегда стоят рядом.

Видимость неудачных запусков тоже должна доходить до решения о выпуске. Если пути инструментов с большим числом тайм-аутов, сбой проверки или сбои внешних зависимостей видны только как очередные неудачные демонстрационные запуски, шлюз раскатки не сможет отделить продуктовый риск от деградации рантайма. Зрелый шлюз должен видеть, что такие неудачные запуски были специально проверены, что их трассы и конкретные причины сбоев, например в `failure_reason`, остались пригодны для разбора и что и штатный путь, и деградировавший путь управлялись одной и той же идентичностью выпуска.

## 8. Как это связано со справочным пакетом

В [agent_runtime_ref](https://github.com/agent-axiom/agent-arch/tree/main/agent_runtime_ref) уже есть куски этой модели:

- [rollout.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/rollout.py)
- [lifecycle.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/lifecycle.py)
- [configs/rollout.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/rollout.yaml)
- [configs/change.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/change.yaml)
- [configs/runtime-controls.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/runtime-controls.yaml)
- CLI:
  - `check-rollout`
  - `check-change`

`check-rollout` возвращает `ready`, `required_checks`, `blocked_checks`, `missing_required`, `support_duplicate_required`, `missing_support_duplicate_required`, `support_duplicate_required_ready`, `blocking_signals` и `rollout_mode`; internally rollout policy normalizes `block_if` into `blocked_checks`, поэтому executable gate сохраняет то же различие между отсутствующей required evidence и явными blockers, что и schema, а release automation отдельно видит duplicate-ticket evidence.

Встроенный `rollout.yaml` делает inputs gate конкретными и валидирует их через `Rollout policy config must be a mapping`, `'rollout' must be a mapping`, `'require' must be a list`, `'block_if' must be a list`, `'rollout_mode' must be a mapping`, `{label} entries must be strings`, `{label} entries must not be empty`, `{label} entries must be unique`, `rollout.rollout_mode keys must be strings`, `rollout.rollout_mode values must be scalar: {field}`, `rollout.rollout_mode entries must not be empty` и `rollout.rollout_mode entries must be unique`: required evidence включает `trace_coverage`, `policy_prechecks`, `capability_owners`, `offline_eval_pass`, `duplicate_ticket_eval_passed`, `slo_defined`, `rollback_plan` и `oncall_owner`; `rollout_mode` задаёт `initial`, `max_tenant_exposure_pct` и `require_shadow_period`; а `block_if` называет жёсткие blockers вроде `unknown_side_effect_path_missing`, `direct_tool_access_present` и `policy_decisions_not_traced`. Runtime signal overrides и direct assessment inputs тоже валидируются: `Signal key must not be empty: {raw_signal!r}`, `Unsupported boolean value in signal: {raw_signal!r}`, `Lifecycle change must be ChangeRecord`, `Lifecycle retirement plan must be RetirementPlan`, `Assessment signals must be a mapping`, `Assessment signal key must be a string`, `Assessment signal key must not be empty`, `Assessment signal keys must be unique`, `Assessment signal value must be a boolean: {field}` и `Rollout policy must be RolloutPolicy`, `Rollout readiness must be RolloutReadiness`, `Rollout readiness flag must be a boolean: {field}`.

Соседний `change.yaml` также задаёт проверяемую поверхность изменения: `change_id` равен `chg-2026-04-07-support-runtime`, `change_type` — `capability_contract_update`, `risk_level` — `high`, а `rollout_strategy` — `staged_canary`. Его `required_signals` перечисляет доказательства выпуска — `design_review_passed`, `offline_eval_passed`, `duplicate_ticket_eval_passed`, `policy_diff_reviewed`, `rollback_plan_ready`, `session_expiry_behavior_checked`, `reinit_policy_reviewed`, `sandbox_profile_reviewed` и `failed_run_drill_checked`, а `approval_roles` фиксирует `platform-owner` и `security-reviewer` как обязательных проверяющих. `check-change` возвращает `change_id`, `ready`, `required_signals`, `approval_roles`, `missing_signals`, `failed_run_signals`, `missing_failed_run_signals`, `support_duplicate_signals`, `missing_support_duplicate_signals`, `support_duplicate_signals_ready`, `rollout_strategy` и `risk_level`, чтобы проверка выпуска отличала общую недостающую доказательную базу от готовности деградировавшего пути и сценария дубля тикета. Загрузчик изменений также отделяет неправильно оформленные записи проверки от проваленных шлюзов через `change config must be a mapping`, `change config keys must be strings`, `change.change_id must be a string`, `change.change_id is required`, `change.change_type must be a string`, `change.change_type is required`, `change.risk_level must be a string`, `change.risk_level is required`, `change.rollout_strategy must be a string`, `change.rollout_strategy is required`, `change.session_control_owner is required` и `change.emergency_freeze_owner is required`; списки вроде `artifacts`, `required_signals` и `approval_roles` отклоняют неправильные значения через `{key} must be a list`, `{key} entries must be strings`, `{key} entries must not be empty` и `{key} entries must be unique`.

Книга теперь показывает не только идею шлюза, но и исполняемый каркас этого контура.

## 9. Минимальные инварианты

Если коротко, у здорового change-rollout слоя должны быть такие инварианты:

- high-risk change не попадает в rollout без review record;
- rollout gate указывает конкретный `bundle_id` и `rollout_wave`;
- required checks и blocking findings видны явно;
- decision всегда имеет owner;
- review и gate можно восстановить по incident trace;
- interruption behavior для approval-bound или stateful capability sessions проверяется до rollout;
- expiry и re-init behavior для capability sessions проверяются до rollout;
- delegated authorization continuity между run traces, approval records и session export проверяется до rollout;
- качество verifier'а и linkage его evidence проверяются до rollout, если release control зависит от graded outcomes;
- changes в orchestration pattern проверяются до rollout, особенно если они добавляют routing, parallelization или delegated worker surfaces;
- sandbox profile changes проверяются до rollout, особенно если они меняют workspace entries, shell/filesystem permissions или snapshot/resume behavior;
- rollback plan не живет только в головах команды.

## 10. Что чаще всего ломается

Типовые проблемы обычно такие:

- review и rollout decision живут в разных местах и не связаны;
- gating criteria не versioned;
- telemetry readiness проверяется "на глаз";
- safety findings не считаются blocker'ами;
- качество verifier'а или linkage его evidence предполагаются, а не проверяются;
- capability-session expiry или re-init behavior остаются неоформленными;
- changes в orchestration pattern проходят как «деталь реализации» без явного review;
- rollout wave описан слишком расплывчато;
- никто не может объяснить, почему изменение вообще было допущено в canary.

## 11. Что сделать сразу

Сначала пройди по короткому списку и отдельно отметь все ответы «нет»:

- Есть ли явный review record для high-risk changes?
- Есть ли отдельный rollout gate, а не только "review approved"?
- Видно ли, какие checks обязаны пройти перед rollout?
- Есть ли связка `change_id -> bundle_id -> rollout_wave`?
- Видно ли, что verifier quality и evidence-linkage checks присутствуют, когда graded outcomes влияют на release?
- Сохраняются ли blocking findings и decision owners?
- Можно ли по incident review восстановить, какой gate пропустил изменение?

Если на несколько вопросов подряд ответ "нет", у тебя уже может быть change process, но еще нет полноценного rollout gate layer.

## Что делать дальше

- [Схема наборов для оценки и правил проверки](eval-schema.md)
- [Схема артефактов жизненного цикла](lifecycle-artifact-schema.md)
- [Схема набора политик и контракта подтверждения](policy-bundle-schema.md)
- [Эталонный пакет](reference-package.md)
- [Глава 18. Чеклист промышленного запуска](../book/part-vii/chapter-18.md)
- [Глава 20. Управление изменениями в агентных системах](../book/part-viii/chapter-20.md)
