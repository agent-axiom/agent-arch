# Схема проверки изменений и шлюза раскатки

Эта страница собирает в одном месте минимальный контрактный слой для change review и rollout gate в агентных системах. Он нужен в тот момент, когда команда уже понимает, что изменения в policy, prompt, model routing, retrieval или tool exposure нельзя выпускать "по ощущению", но еще не оформила эти проверки в явные артефакты.

Если [схема lifecycle-артефактов](lifecycle-artifact-schema.md) отвечает на вопрос "какие сущности жизненного цикла вообще должны существовать", то change-rollout schema отвечает на вопрос "какие поля нужны, чтобы реально принять решение о выпуске".

## 1. Зачем нужен отдельный слой схем

У agent system change review часто распадается на несколько несвязанных фрагментов:

- engineering review в pull request;
- safety review где-то в отдельном документе;
- eval results в CI;
- rollout decision в чате или устно на созвоне.

Пока система маленькая, это может работать терпимо. Но как только появляется несколько owners, high-risk actions и staged rollout, такая схема перестает быть управляемой.

Отдельный machine-readable слой полезен потому, что он:

- связывает change record с eval requirements;
- фиксирует release gate явно, а не в памяти команды;
- сохраняет rollout strategy и blast radius;
- облегчает incident review и rollback.

## 2. Базовые сущности

Минимальный слой здесь обычно строится вокруг двух сущностей:

- `change_review_record`
- `rollout_gate_record`

Этого уже достаточно, чтобы связать Part V, Part VII и Part VIII в одну operational discipline.

## 3. Change review record

`change_review_record` описывает, что именно изменилось, кто это reviewed и какие условия должны быть выполнены до выкладки.

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
  - verifier_quality_check
status: approved
```

Ключевые поля здесь такие:

- `affected_surfaces` не дает замаскировать опасное изменение под "небольшую настройку";
- `required_reviews` делает ownership явным;
- `required_evals` помогает не спорить каждый раз заново, что именно надо прогонять;
- `status` нужен как operational факт, а не как украшение в markdown.

## 4. Rollout gate record

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
blocking_findings: []
decision: go
decided_by:
  - runtime_owner
  - safety_owner
```

Этот слой нужен потому, что даже хороший change review еще не означает автоматическую готовность к rollout.

Это еще важнее, когда rollout опирается на richer verifier outputs, а не только на binary pass/fail status. Тогда gate record должен явно показывать, проверялись ли для затронутых high-risk paths качество verifier'а и linkage его evidence.

Как только в runtime появляются approval и stateful capability sessions, gate еще должен явно фиксировать, было ли interruption behavior отдельно проверено, а не просто принято по умолчанию.

## 5. Чем change review отличается от rollout gate

Эти два слоя часто путают, хотя задачи у них разные:

- `change_review_record` отвечает на вопрос: "можно ли в принципе выпускать это изменение";
- `rollout_gate_record` отвечает на вопрос: "можно ли выпускать его сейчас и в таком масштабе".

Из-за этого у них и поля разные:

- review больше смотрит на тип изменения, риски и required evals;
- rollout gate больше смотрит на telemetry, on-call, rollback, traffic scope, live readiness и interruption handling для approval-bound или stateful capability paths.

На практике это обычно означает, что gate должен еще явно фиксировать:

- проверялось ли capability-session expiry behavior до rollout;
- является ли re-init для затронутого path denied, allowed или approval-bound;
- проверялась ли delegated authorization continuity между run traces, approval records и session export;
- были ли changes в orchestration pattern отдельно reviewed как runtime-control changes до rollout;
- кто owner у emergency freeze, если interruption semantics начнут дрейфовать после релиза.

## 6. Как это связано с eval schema

Change review и rollout gate тесно связаны с [eval schema](eval-schema.md):

- review указывает, какие evals обязательны;
- gate смотрит, достаточно ли результатов для конкретной rollout wave;
- incidents и findings потом возвращаются обратно в список required checks;
- verifier regressions и failures в evidence linkage тоже становятся rollout-relevant findings.

То есть eval layer не живет отдельно от release discipline, а становится одной из опор gate.

## 7. Как это связано со схемой трасс

Rollout gate особенно полезен, когда trace schema уже собрана:

- по traces видно, прошли ли high-risk paths;
- по session summaries видно, есть ли regressions;
- по structured events можно понять, что именно было проверено перед выпуском;
- по interruption и expiry signals видно, не деградируют ли approval-bound runs раньше, чем это заметят операторы;
- verifier evidence показывает, действительно ли process/outcome judgments, использованные в rollout review, traceable.

Поэтому у зрелой команды trace и rollout gate почти всегда стоят рядом.

Видимость failed runs тоже должна доходить до release judgment. Если timeout-heavy tool paths, validation failure или сбои внешних зависимостей видны только как очередные неудачные demo runs, rollout gate не сможет отделить product risk от деградации рантайма. Зрелый gate должен видеть, что такие failed runs были специально проверены, что их traces остались пригодны для review и что и happy path, и degraded path управлялись одной и той же release identity.

## 8. Как это связано со справочным пакетом

В [agent_runtime_ref](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref) уже есть куски этой модели:

- [rollout.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/rollout.py)
- [lifecycle.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/lifecycle.py)
- [configs/rollout.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/rollout.yaml)
- [configs/change.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/change.yaml)
- [configs/runtime-controls.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/runtime-controls.yaml)
- CLI:
  - `check-rollout`
  - `check-change`

Книга теперь показывает не только идею gate, но и runnable skeleton этого gate.

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
- [Справочный пакет](reference-package.md)
- [Глава 18. Чеклист промышленного запуска](../book/part-vii/chapter-18.md)
- [Глава 20. Change management для агентных систем](../book/part-viii/chapter-20.md)
