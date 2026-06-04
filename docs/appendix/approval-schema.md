# Схема запроса на подтверждение и записи о решении

Эта страница описывает минимальный контрактный слой для подтверждения человеком в агентных системах: какие данные должен содержать запрос на подтверждение, как фиксируется решение и что должно остаться в журнале аудита после действия высокого риска.

Она напрямую связана со страницей [Сквозная цепочка доказательств: от запроса к решению о поэтапном выпуске](../book/part-v/evidence-spine.md), потому что подтверждение - одна из тех записей, которые делают управляемый запуск читаемым от запроса до решения о выпуске.

Если [набор политик](policy-bundle-schema.md) отвечает на вопрос "какие правила вообще действуют", то схема подтверждения отвечает на вопрос "как именно среда выполнения передает человеку право последнего решения".

## 1. Зачем нужна отдельная схема подтверждения

Очень частая ошибка устроена так:

- политика говорит, что действие относится к высокому риску;
- среда выполнения возвращает `approval_required`;
- дальше вся логика живет где-то в интерфейсе или в устной договоренности команды.

В этом случае ты теряешь:

- единый формат запроса;
- проверяемую запись о решении;
- воспроизводимый журнал аудита;
- связь между подтверждением и конкретным запуском или трассой.

Поэтому границу подтверждения лучше оформлять как машиночитаемый контракт, а не как "кнопку в интерфейсе".

## 2. Базовые сущности

Минимальная схема обычно строится вокруг трех сущностей:

- `approval_request`
- `approval_decision`
- `approval_audit_record`

Этого уже достаточно, чтобы связать слой политик, среду выполнения, схему трасс и артефакты жизненного цикла.

## 3. Запрос на подтверждение

`approval_request` создается тогда, когда среда выполнения сталкивается с действием, которое нельзя продолжать автоматически.

```yaml
kind: approval_request
approval_id: apr-2026-04-07-001
trace_id: trace-approval-001
session_id: session-approval-001
agent_id: support-triage-agent
tenant_id: tenant-acme
principal_id: user-42
capability: ticket_write
risk_tier: high
requested_action: create_incident_ticket
reason: write_path_requires_human_review
requested_fields:
  summary: "Open a Sev-2 onboarding incident"
  idempotency_key: ticket-req-2026-04-09-001
  target_system: jira
  destination: project://OPS
sandbox_context:
  sandbox_profile_contract: sandbox-profile-v1
  workspace_entries_reviewed: true
  permissions_profile: restricted-shell-network-denied
  network_secrets_posture: network:denied,secrets:none
  snapshot_policy: required_on_completion
required_role: oncall_manager
status: pending
```

Что здесь особенно важно:

- `trace_id` и `session_id` связывают approval с run history;
- `capability` и `requested_action` не дают подтверждению превратиться в абстрактное "да/нет";
- `required_role` помогает не смешивать любого проверяющего с нужным подтверждающим;
- `requested_fields` фиксируют именно те данные, которые человек реально подтверждает;
- `sandbox_context` нужен для действий, выполняемых через песочницу, чтобы подтверждающий видел материализацию рабочей области, права доступа и правила снимка/возобновления, а не только бизнес-данные.

## 4. Решение по запросу

`approval_decision` описывает, что именно решил человек и на каком основании.

```yaml
kind: approval_decision
approval_id: apr-2026-04-07-001
decision: approved
decided_by: oncall-manager-7
decided_at: 2026-04-07T11:42:00Z
role: oncall_manager
note: "Customer impact confirmed, proceed with ticket creation"
scope: single_request
expires_at: 2026-04-07T12:00:00Z
```

Здесь есть несколько важных инвариантов:

- решение должно ссылаться на конкретный `approval_id`;
- `decided_by` и `role` должны быть пригодны для аудита;
- `scope` не должен быть неявным;
- `expires_at` полезен, если подтверждение не должно жить бесконечно.

## 5. Аудиторская запись подтверждения

`approval_audit_record` связывает решение с реальным побочным действием или отказом от него.

```yaml
kind: approval_audit_record
approval_id: apr-2026-04-07-001
trace_id: trace-approval-001
decision: approved
executed: true
executed_capability: ticket_write
tool_principal: svc-ticket-writer
idempotency_key: ticket-req-2026-04-09-001
result_status: success
linked_events:
  - approval_requested
  - approval_resolved
  - tool_called
  - tool_succeeded
```

Это уже не просто "решение было принято", а понятный рабочий след:

- запросили;
- одобрили или отклонили;
- выполнили или не выполнили;
- понятно, каким субъектом было выполнено побочное действие.

## 6. Как это связано со схемой трасс

Схема подтверждения живет не отдельно, а рядом со схемой трасс:

- `approval_requested`
- `approval_resolved`
- `tool_called`
- `tool_succeeded`
- `tool_failed`

Именно поэтому хорошая цепочка подтверждения должна легко восстанавливаться как из отдельной аудиторской записи, так и из трассы. Если подтверждение участвует в разборе неудачного запуска или другом деградировавшем пути, такое восстановление должно сходиться и с экспортом сессии, включая поле `failure_reason`, а не останавливаться только на записи подтверждения.

!!! example "Запись подтверждения для цепочки с дублем тикета"
    В сценарии триажа обращений поддержки подтверждающий должен видеть `idempotency_key` вместе с данными запроса до нажатия кнопки подтверждения. Если `create_ticket` затем завершается по тайм-ауту, аудиторская запись сохраняет тот же ключ рядом с `approval_id`, `trace_id` и `tool_principal`, чтобы проверка отличала один подтвержденный замысел записи от повторного побочного действия после слепого повтора.

!!! note "Канонические сценарии подтверждений"
    Запись подтверждения нужна не только для пути записи. **Триаж обращений поддержки** требует явного подтверждения человеком, `idempotency_key` и доказательств восстановления после дубля тикета. **Внутренний ассистент знаний** чаще требует подтверждения или проверки для записей в память, исключений контроля доступа и решений о видимости источников. **Координация инцидентов** требует следа подтверждений для полномочий эскалации, побочных эффектов уведомлений, передачи владения ответом и обновлений обучения после инцидента.

## 7. Как это связано с набором политик

Набор политик отвечает на вопросы:

- какая возможность требует подтверждения;
- кто имеет право подтверждать;
- какие уровни риска вообще существуют;
- какие действия запрещены без человеческого шлюза.

Схема подтверждения отвечает за другой слой:

- как выглядит сам запрос;
- что именно человек подтверждает;
- как хранится решение;
- как это решение связывается с выполнением.

## 8. Связь с эталонным пакетом

В [agent_runtime_ref](https://github.com/agent-axiom/agent-arch/tree/main/agent_runtime_ref) уже есть рабочие примитивы, которые поддерживают эту модель:

- [approvals.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/approvals.py)
- [configs/approvals.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/approvals.yaml)
- CLI:
  - `inspect-approvals`
  - `resolve-approval`

`inspect-approvals` возвращает `trace_id`, `session_id`, `tenant_id`, `agent_id`, `count`, `approval_ids`, `pending_approval_ids`, `approval_capability_names`, `pending_approval_capability_names`, `approval_status_counts`, `idempotency_keys` и `approvals`; каждая запись подтверждения сохраняет `approval_id`, `tenant_id`, `agent_id`, `capability_name`, `requested_by`, `reviewer`, `reason`, `status`, `capability_session_id`, `capability_session_status`, `authorization_mode`, `delegated_principal_id`, `delegated_scope` и `idempotency_key`. `resolve-approval` возвращает `approval_id`, `approval_ids`, `trace_id`, `session_id`, `tenant_id`, `agent_id`, `capability_name`, `approval_capability_names`, `pending_approval_ids`, `pending_approval_capability_names`, `requested_by`, `status`, `reviewer`, `resolution_note`, `capability_session_id`, `capability_session_status`, `authorization_mode`, `delegated_principal_id`, `delegated_scope`, `idempotency_key`, `idempotency_keys` и `approval_status_counts`, поэтому исполняемая демонстрация сохраняет цепочку подтверждений, состояние сессии возможности, делегированные полномочия, намерение повторной записи и итоговый статус подтверждения видимыми до и после решения.

Встроенный `approvals.yaml` также явно задаёт рабочую политику подтверждений и валидирует форму верхнего уровня через `'approvals' must be a mapping`: `default_reviewer`, `escalation_sla_minutes` и настройки `delegated_authorization`, такие как `reviewer_required_for_user_delegation`, `require_principal_binding`, `require_scope_visibility`, `on_scope_revoked` и `subagent_inheritance`, описывают, кто проверяет делегированные действия, какие доказательства должны оставаться видимыми и может ли делегирование переходить к дочерним агентам. Загрузчик политик сохраняет проверяющего, эскалацию и доказательства делегированного разрешения с типовой защитой через `approvals.default_reviewer must be a string`, `approvals.default_reviewer is required`, `approvals.escalation_sla_minutes must be an integer`, `approvals.escalation_sla_minutes must be positive`, `approvals.delegated_authorization must be a mapping`, `approvals.delegated_authorization must be DelegatedAuthorizationPolicy`, `delegated_authorization.require_principal_binding must be a boolean` и `delegated_authorization.require_scope_visibility must be a boolean`. Цепочка подтверждений и сессий также отвергает неподдержанное доказательство делегированного разрешения через `Authorization mode is not supported: {authorization_mode}` и неподдержанные состояния подтверждения или сессии возможности через `Approval status is not supported: {status}`, а не сохраняет неизвестные режимы или статусы рядом с подтверждениями или экспортами сессии. Эталонная политика задаёт наследование дочерними агентами как `explicit_only`, поэтому делегированные полномочия не переходят в дочерний агент без явного указания в цепочке подтверждения.

Так подтверждение можно не только описывать, но и реально прогонять как часть демонстрационной среды выполнения.

## 9. Минимальные инварианты

Если коротко, у зрелого слоя подтверждений должны быть такие инварианты:

- у каждого запроса есть стабильный `approval_id`;
- подтверждение привязано к `trace_id` и `session_id`;
- ясно, какие данные были одобрены;
- подтверждающий и роль сохраняются в журнале аудита;
- побочное действие можно связать с конкретным решением по подтверждению;
- истекшее подтверждение не используется повторно.

## 10. Что чаще всего ломается

Типовые проблемы здесь довольно узнаваемы:

- запрос на подтверждение не содержит реальных данных действия;
- подтверждающий видит слишком мало контекста;
- решение хранится только в интерфейсе и не доходит до трассы;
- среда выполнения не различает "подтверждено один раз" и "подтверждено навсегда";
- подтверждение для действия в песочнице не показывает профиль песочницы, записи рабочей области или права доступа;
- побочное действие исполняется с другими данными, чем те, что были одобрены;
- никто не может восстановить, кто подтвердил рискованное действие.

## 11. Что сделать сразу

Сначала пройди по короткому списку и отдельно отметь все ответы «нет»:

- Есть ли у запроса на подтверждение явный `approval_id`?
- Привязано ли подтверждение к `trace_id` и `session_id`?
- Видит ли подтверждающий ровно те данные, которые потом идут в действие?
- Если действие выполняется в песочнице, видит ли подтверждающий контракт профиля песочницы, записи рабочей области, права доступа и правила снимка/возобновления?
- Сохраняются ли `decided_by`, `role` и `decision scope`?
- Можно ли связать подтверждение с реальным выполнением инструмента?
- Есть ли пригодная для аудита запись для подтвержденных и отклоненных путей?

Если на несколько вопросов подряд ответ "нет", у тебя есть человеческий шлюз по смыслу, но еще нет полноценного контракта подтверждения.

## Что делать дальше

- [Схема набора политик и контракта подтверждения](policy-bundle-schema.md)
- [Схема трасс и каталог событий](trace-schema.md)
- [Схема артефактов жизненного цикла](lifecycle-artifact-schema.md)
- [Эталонный пакет](reference-package.md)
- [Глава 4. Инструментальный шлюз, подтверждения и журнал аудита](../book/part-ii/chapter-4.md)
- [Глава 17. Слой политик и каталог возможностей](../book/part-vii/chapter-17.md)
