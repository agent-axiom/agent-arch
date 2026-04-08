# Схема lifecycle-артефактов

Эта страница собирает в одном месте минимальный contract layer для lifecycle-артефактов: change record, approved artifact bundle и retirement plan. Если trace schema отвечает на вопрос "что произошло", а eval schema отвечает на вопрос "как это оценивать", то lifecycle artifact schema отвечает на вопрос "что именно было одобрено, изменено, заменено или выведено из эксплуатации".

## 1. Зачем это нужно

У production-grade agent system есть несколько классов артефактов, которые нельзя держать только в голове команды или в wiki:

- change records;
- approved artifact bundles;
- retirement plans;
- replacement mappings;
- operational approvals и lifecycle decisions.

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

## 4. Approved artifact bundle

`artifact_bundle` фиксирует набор артефактов, которые считаются доверенными и совместимыми друг с другом в конкретной release-конфигурации.

```yaml
kind: artifact_bundle
bundle_id: bundle-2026-04-07-a
owner: platform-runtime
artifacts:
  model_route: gpt-5.4-tools
  policy_bundle: policy-v4
  approvals_bundle: approvals-v3
  controls_bundle: controls-v2
  capability_catalog: catalog-v5
  eval_dataset: eval-set-2026-04-07
status: approved
release_scope: canary
provenance:
  change_record: chg-2026-04-07-001
  reviewed_by:
    - safety-review
    - runtime-review
```

Этот слой полезен по двум причинам:

- он отделяет "есть артефакт" от "артефакт одобрен для релиза";
- он делает incident review и rollback гораздо короче.

## 5. Retirement plan

`retirement_plan` нужен не только для полного выключения агента, но и для controlled replacement capability, policy bundle или artifact family.

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
- principals;
- memory;
- archived bundles.

## 6. Как это связано с Part VIII

Эта схема напрямую поддерживает несколько глав:

- Chapter 20: change management;
- Chapter 21: assurance findings, которые становятся lifecycle input;
- Chapter 22: approved artifacts и provenance;
- Chapter 23: replacement и retirement.

Именно поэтому lifecycle artifacts полезно держать не как prose-only documentation, а как reviewable YAML или JSON contract.

## 7. Минимальные инварианты

Если делать совсем коротко, у healthy lifecycle artifact layer должны быть такие инварианты:

- каждый high-risk change имеет `change_record`;
- каждый production rollout указывает на `artifact_bundle`;
- у deprecated artifact есть `retirement_plan` или явное исключение;
- lifecycle artifacts имеют owner и version;
- incident review может восстановить связку `change -> bundle -> run -> retirement`.

## 8. Что чаще всего ломается

Проблемы обычно очень узнаваемые:

- bundle собирается "на словах", а не как артефакт;
- change records живут отдельно от eval requirements;
- retirement есть в roadmap, но не в operational config;
- replacement делается без dual-run semantics;
- historical state не имеет retention owner;
- provenance заканчивается на уровне git commit и не доходит до runtime bundle.

## 9. Практический чеклист

Если хочешь быстро проверить этот слой, пройди по вопросам:

- Есть ли у high-risk changes явные change records?
- Есть ли approved artifact bundle, а не просто список последних YAML-файлов?
- Можно ли по incident trace восстановить активный bundle?
- Есть ли retirement plan для deprecated capabilities и policy bundles?
- Есть ли owner у archived state после replacement?
- Понятен ли rollback unit на уровне lifecycle artifacts?

Если на несколько вопросов подряд ответ "нет", у тебя уже может быть хороший SDLC и даже хороший rollout, но lifecycle layer пока еще не собран до конца.

## См. также

- [Схема трасс и каталог событий](trace-schema.md)
- [Схема eval datasets и grading contract](eval-schema.md)
- [Схема policy bundle и approval contract](policy-bundle-schema.md)
- [Справочный пакет](reference-package.md)
- [Глава 20. Change management для агентных систем](../book/part-viii/chapter-20.md)
- [Глава 22. Supply chain, provenance и approved artifacts](../book/part-viii/chapter-22.md)
- [Глава 23. Retirement, replacement и end-of-life discipline](../book/part-viii/chapter-23.md)
