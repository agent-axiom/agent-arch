# Схема change review и rollout gate

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
  - rollout_rules
required_reviews:
  - engineering
  - safety
  - runtime_owner
required_evals:
  - offline_regression
  - targeted_safety_eval
  - trace_regression_check
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

## 5. Чем change review отличается от rollout gate

Эти два слоя часто путают, хотя задачи у них разные:

- `change_review_record` отвечает на вопрос: "можно ли в принципе выпускать это изменение";
- `rollout_gate_record` отвечает на вопрос: "можно ли выпускать его сейчас и в таком масштабе".

Из-за этого у них и поля разные:

- review больше смотрит на тип изменения, риски и required evals;
- rollout gate больше смотрит на telemetry, on-call, rollback, traffic scope и live readiness.

## 6. Как это связано с eval schema

Change review и rollout gate тесно связаны с [eval schema](eval-schema.md):

- review указывает, какие evals обязательны;
- gate смотрит, достаточно ли результатов для конкретной rollout wave;
- incidents и findings потом возвращаются обратно в список required checks.

То есть eval layer не живет отдельно от release discipline, а становится одной из опор gate.

## 7. Как это связано со схемой трасс

Rollout gate особенно полезен, когда trace schema уже собрана:

- по traces видно, прошли ли high-risk paths;
- по session summaries видно, есть ли regressions;
- по structured events можно понять, что именно было проверено перед выпуском.

Поэтому у зрелой команды trace и rollout gate почти всегда стоят рядом.

## 8. Как это связано с опорным пакетом

В [agent_runtime_ref](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref) уже есть куски этой модели:

- [rollout.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/rollout.py)
- [lifecycle.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/lifecycle.py)
- [configs/rollout.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/rollout.yaml)
- [configs/change.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/change.yaml)
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
- rollback plan не живет только в головах команды.

## 10. Что чаще всего ломается

Типовые проблемы обычно такие:

- review и rollout decision живут в разных местах и не связаны;
- gating criteria не versioned;
- telemetry readiness проверяется "на глаз";
- safety findings не считаются blocker'ами;
- rollout wave описан слишком расплывчато;
- никто не может объяснить, почему изменение вообще было допущено в canary.

## 11. Практический чеклист

Если хочешь быстро проверить свой release discipline, пройди по вопросам:

- Есть ли явный review record для high-risk changes?
- Есть ли отдельный rollout gate, а не только "review approved"?
- Видно ли, какие checks обязаны пройти перед rollout?
- Есть ли связка `change_id -> bundle_id -> rollout_wave`?
- Сохраняются ли blocking findings и decision owners?
- Можно ли по incident review восстановить, какой gate пропустил изменение?

Если на несколько вопросов подряд ответ "нет", у тебя уже может быть change process, но еще нет полноценного rollout gate layer.

## См. также

- [Схема eval datasets и grading contract](eval-schema.md)
- [Схема lifecycle-артефактов](lifecycle-artifact-schema.md)
- [Схема policy bundle и approval contract](policy-bundle-schema.md)
- [Справочный пакет](reference-package.md)
- [Глава 18. Чеклист промышленного запуска](../book/part-vii/chapter-18.md)
- [Глава 20. Change management для агентных систем](../book/part-viii/chapter-20.md)
