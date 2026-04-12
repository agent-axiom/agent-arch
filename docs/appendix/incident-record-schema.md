# Схема incident record и postmortem linkage

Эта страница описывает минимальный контрактный слой для incident review в agent systems: какие поля должен содержать incident record, как он связывается с traces, approvals, rollout и lifecycle artifacts, и какие данные должны пережить containment phase.

Если [плейбук реагирования на инциденты](incident-response-playbook.md) отвечает на вопрос "что делать в первые минуты и в ходе разбора", то incident record schema отвечает на вопрос "в каком виде это должно быть зафиксировано".

## 1. Зачем нужен отдельный incident record

Без отдельного incident artifact разбор обычно распадается на несколько несвязанных кусков:

- traces живут в observability system;
- approval history живет в audit trail;
- rollback decision живет в чате;
- postmortem живет в документе;
- change linkage вспоминают по памяти.

Такой разбор может работать один-два раза. Но он плохо переносится на repeated incidents, audit, regression updates и lifecycle corrections.

## 2. Базовые сущности

Минимальная схема обычно строится вокруг двух сущностей:

- `incident_record`
- `incident_postmortem_link`

Этого уже достаточно, чтобы связать operational response и lifecycle correction.

## 3. Incident record

`incident_record` фиксирует, что произошло, какой был blast radius и какие artifacts были активны во время события.

```yaml
kind: incident_record
incident_id: inc-2026-04-09-001
title: "Unauthorized ticket_write path during onboarding run"
severity: sev2
status: contained
category: unauthorized_side_effect
detected_at: 2026-04-09T09:14:00Z
detected_by: automated_detection
agent_id: support-triage-ref
trace_id: trace-2026-04-09-001
session_id: session-2026-04-09-001
bundle_id: bundle-2026-04-07-a
change_id: chg-2026-04-07-001
rollout_wave: canary
tool_principal: svc-ticket-writer
approval_id: apr-2026-04-09-001
affected_surfaces:
  - approval_path
  - tool_gateway
  - rollout_gate
containment_actions:
  - force_mandatory_approval
  - disable_ticket_write_v1
owner: platform-operations
```

Ключевые поля здесь такие:

- `category` позволяет связывать incident с triage taxonomy и eval updates;
- `bundle_id`, `change_id` и `rollout_wave` связывают incident с release discipline;
- `tool_principal` и `approval_id` сокращают путь до реального side effect;
- `affected_surfaces` помогает не сводить разбор к одному только model response.

## 4. Incident postmortem link

`incident_postmortem_link` связывает конкретный incident с corrective actions и lifecycle artifacts.

```yaml
kind: incident_postmortem_link
incident_id: inc-2026-04-09-001
postmortem_id: pm-2026-04-09-001
corrective_actions:
  - change_id: chg-2026-04-09-003
  - bundle_id: bundle-2026-04-09-b
  - eval_dataset_update: eval-set-2026-04-09
  - retirement_plan: retire-ticket-write-v1
owners:
  - platform-safety
  - platform-runtime
status: open
```

Этот слой полезен потому, что заставляет incident review заканчиваться не только текстом, но и конкретными lifecycle updates.

## 5. Как это связано с trace schema

Incident record почти всегда опирается на [trace schema](trace-schema.md):

- `trace_id` и `session_id` связывают incident с run history;
- policy events показывают, что было разрешено;
- approval events показывают, был ли human gate;
- tool events показывают реальный side effect;
- session summaries помогают понять, это единичный run или pattern.

## 6. Как это связано с approvals и policy bundle

Incident record особенно важен, когда нужно быстро восстановить:

- какой approval path действовал;
- какое решение было принято;
- какой policy bundle был активен;
- какой principal реально выполнил действие.

Поэтому incident schema должна стоять рядом с:

- [Схемой набора политик и контракта подтверждения](policy-bundle-schema.md)
- [Схемой запроса на подтверждение и записи о решении](approval-schema.md)

## 7. Как это связано с change management и rollout

Incident review редко заканчивается только containment phase.

Обычно нужно понять:

- какой `change_id` ввел risky path;
- какой `rollout_gate_record` это пропустил;
- какие checks не сработали;
- нужен ли rollback, restricted mode или retirement.

Именно поэтому incident record должен быть связан с [change-rollout schema](change-rollout-schema.md) и [lifecycle artifact schema](lifecycle-artifact-schema.md).

## 8. Связь со справочным пакетом

В [agent_runtime_ref](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref) уже есть несколько примитивов, которые делают эту схему полезной на практике:

- traces и session summaries;
- approval queue;
- lifecycle artifacts;
- rollout checks;
- policy and controls linkage.

Даже если package пока не хранит полноценный `incident_record`, книга уже может фиксировать, какие поля такой record должен иметь.

## 9. Минимальные инварианты

У зрелого incident layer обычно есть такие инварианты:

- incident имеет стабильный `incident_id`;
- `trace_id` и `session_id` сохраняются сразу;
- `bundle_id`, `change_id` и `rollout_wave` можно восстановить без догадок;
- containment actions фиксируются явно;
- incident связывается с corrective actions;
- postmortem ведет к обновлению lifecycle artifacts, evals или policy bundles.

## 10. Что чаще всего ломается

Типовые проблемы обычно такие:

- incident ticket не знает про trace и session;
- side effect виден, но неясно, какой principal его выполнил;
- change linkage восстанавливают по памяти;
- postmortem не связан с corrective artifact;
- incidents не попадают в eval dataset и rollout criteria;
- retired path продолжает жить после supposedly closed incident.

## 11. Что сделать сразу

Сначала пройди по короткому списку и отдельно отметь все ответы «нет»:

- Есть ли у incident стабильный `incident_id`?
- Можно ли быстро восстановить `trace_id`, `session_id`, `bundle_id` и `change_id`?
- Видно ли, какой principal и approval path участвовали в событии?
- Зафиксированы ли containment actions?
- Есть ли связь incident -> postmortem -> corrective action?
- Возвращаются ли incidents в evals, rollout gates и lifecycle updates?

## Что делать дальше

- [Плейбук реагирования на инциденты в агентных системах](incident-response-playbook.md)
- [Схема трасс и каталог событий](trace-schema.md)
- [Схема запроса на подтверждение и записи о решении](approval-schema.md)
- [Схема проверки изменений и шлюза раскатки](change-rollout-schema.md)
- [Схема артефактов жизненного цикла](lifecycle-artifact-schema.md)
- [Handbook по agent registry и inventory operations](registry-operations-handbook.md)
- [Глава 21. Assurance loop: red teaming, detection и response](../book/part-viii/chapter-21.md)
- [Глава 26. AI-native observability, inventory coverage и detection-ready telemetry](../book/part-viii/chapter-26.md)
