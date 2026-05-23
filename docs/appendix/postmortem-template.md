# Шаблон postmortem для агентных систем

Этот шаблон нужен не для красивого документа, а для того, чтобы incident review заканчивался конкретными corrective actions, обновлениями lifecycle artifacts и изменениями в eval discipline.

Используй его после containment phase, когда traces, approvals, rollout data и active bundle уже восстановлены.

## 1. Краткое описание

- `incident_id`:
- Дата и время:
- Severity:
- Status:
- Owner:
- Краткое резюме инцидента:

## 2. Что произошло

- Какой agent или workflow участвовал:
- Какой user input, retrieved context или external trigger запустил path:
- Какой risky action или failure произошел:
- Был ли реальный side effect:

Главная цель этого блока: коротко и без интерпретаций зафиксировать саму цепочку события.

## 3. Какие артефакты были активны

- `trace_id`:
- `session_id`:
- `bundle_id`:
- `change_id`:
- `rollout_wave`:
- `policy_bundle`:
- `approval_mode`:
- `tool_principal`:

Если этот блок нельзя заполнить быстро, у команды проблема уже не только в инциденте, но и в observability или lifecycle layer.

## 4. Containment actions

- Какие действия были предприняты в первые минуты:
- Что именно было отключено, ограничено или переведено в restricted mode:
- Требовался ли rollback:
- Были ли revoked principals, connectors или capabilities:

Здесь полезно различать:

- временное сдерживание;
- постоянное исправление.

## 5. Root cause

- Какая непосредственная причина инцидента:
- Какие contributing factors усилили проблему:
- Какой gate, review или assumption не сработали:
- Была ли проблема в policy, approvals, rollout, memory, observability или inventory:

Этот блок должен вести к системному объяснению, а не к формуле "модель ошиблась".

## 6. Что не сработало в control layer

- Какой policy decision пропустил risky path:
- Был ли approval bypass, missing approval или неверный approval scope:
- Какие checks или evals не сработали:
- Какие detection rules не сработали или сработали слишком поздно:

Здесь важно описывать не только ошибку, но и отсутствие нужного guardrail.

## 7. Blast radius

- Какие users, systems или data были затронуты:
- Был ли доступ к external systems:
- Были ли затронуты memory records:
- Это единичный run или pattern в rollout wave / session family:

## 8. Corrective actions

Для каждого действия полезно указать:

- действие;
- owner;
- срок;
- какой artifact обновляется.

Минимальные типы corrective actions обычно такие:

- update policy bundle;
- tighten approval mode;
- update eval dataset;
- add targeted regression;
- update rollout gate;
- retire capability or principal;
- update registry record;
- add detection rule.

## 9. Что меняется в lifecycle artifacts

- Новый `change_id`, если нужен correction release:
- Новый `bundle_id`, если меняется release configuration:
- Нужен ли новый `retirement_plan`:
- Нужно ли обновить registry / inventory:
- Нужно ли обновить incident taxonomy или postmortem rubric:

Этот блок полезен, потому что связывает postmortem с управляемыми артефактами, а не только с задачами в трекере.

## 10. Что меняется в evals и rollout

- Какие кейсы должны попасть в eval dataset:
- Какие behavioral или control evals нужно добавить:
- Нужно ли менять rollout gate criteria:
- Нужно ли менять canary scope или approval threshold:

Если incidents не возвращаются в evals и rollout rules, организация обычно повторяет один и тот же класс ошибок.

!!! example "Postmortem для duplicate-ticket thread"
    Для support-triage инцидента postmortem должен явно ответить: какой `create_ticket` call создал side effect, какой `idempotency_key` был или отсутствовал, какой `policy_bundle` и `rollout_wave` это пропустили, почему `side_effect_unknown` не остановил повтор, и какие corrective actions обновляют eval dataset, rollout gate, approval policy, registry record и retirement plan для старого ticket writer.

!!! note "Канонические сценарии разбора инцидентов (Canonical postmortem cases)"
    Разбор инцидента (postmortem) должен возвращать разные классы отказов (failure classes) в контур управления (control loop) для трех канонических сценариев (canonical cases). **Триаж обращений поддержки (Support triage)** проверяет корневую причину дубля тикета (duplicate-ticket root cause), область подтверждения (approval scope), `idempotency_key`, сдерживание побочного эффекта (side-effect containment) и исправление оценки/раскатки (eval/rollout correction). **Внутренний ассистент знаний (Internal knowledge assistant)** проверяет устаревший источник (stale source), свежесть поиска (retrieval freshness), происхождение памяти (memory provenance), разрыв контроля доступа (access-control gap) и исправление базы знаний (knowledge-base correction). **Координация инцидентов (Incident coordination)** проверяет задержку эскалации (escalation delay), побочные эффекты уведомлений (notification side effects), разрыв владения ответом (response ownership gap), сбой передачи управления (handoff breakdown) и обновление обучения после инцидента (post-incident learning update).

## 11. Короткий шаблон в YAML

```yaml
postmortem:
  incident_id: inc-2026-04-09-001
  severity: sev2
  owner: platform-operations
  active_artifacts:
    trace_id: trace-2026-04-09-001
    session_id: session-2026-04-09-001
    bundle_id: bundle-2026-04-07-a
    change_id: chg-2026-04-07-001
    rollout_wave: canary
  root_cause:
    primary: approval_scope_too_broad
    contributing:
      - missing_targeted_eval
      - stale_rollout_gate
  corrective_actions:
    - owner: platform-safety
      action: tighten_approval_policy
      due: 2026-04-12
    - owner: runtime-team
      action: add_regression_eval
      due: 2026-04-13
  lifecycle_updates:
    change_id: chg-2026-04-09-003
    bundle_id: bundle-2026-04-09-b
```

## 12. Что сделать сразу

Сначала пройди по короткому списку и отдельно отметь все ответы «нет»:

- Есть ли в postmortem точный `incident_id`?
- Восстановлены ли `trace_id`, `session_id`, `bundle_id` и `change_id`?
- Есть ли не только root cause, но и contributing factors?
- Зафиксированы ли control gaps?
- Есть ли concrete corrective actions с owners и сроками?
- Понятно ли, какие lifecycle artifacts должны обновиться?
- Возвращается ли incident в evals и rollout criteria?

## Что делать дальше

- [Плейбук реагирования на инциденты в агентных системах](incident-response-playbook.md)
- [Схема incident record и postmortem linkage](incident-record-schema.md)
- [Схема проверки изменений и шлюза раскатки](change-rollout-schema.md)
- [Схема артефактов жизненного цикла](lifecycle-artifact-schema.md)
- [Handbook по agent registry и inventory operations](registry-operations-handbook.md)
- [Глава 21. Assurance loop: red teaming, detection и response](../book/part-viii/chapter-21.md)
