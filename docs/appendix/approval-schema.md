# Схема approval request и decision record

Эта страница описывает минимальный contract layer для human approval в agent systems: как выглядит запрос на подтверждение, как выглядит решение, и что именно должно остаться в audit trail после high-risk действия.

Если [policy bundle](policy-bundle-schema.md) отвечает на вопрос "какие правила вообще действуют", то approval schema отвечает на вопрос "как именно рантайм передает человеку право последнего решения".

## 1. Зачем нужен отдельный approval schema

Очень частая ошибка выглядит так:

- policy говорит, что действие high-risk;
- runtime возвращает `approval_required`;
- дальше вся логика живет где-то в UI или в устной договоренности команды.

В этом случае ты теряешь:

- единый формат запроса;
- проверяемый decision record;
- повторяемую audit trail;
- связь между approval и конкретным run или trace.

Поэтому approval boundary лучше оформлять как machine-readable contract, а не как "кнопку в интерфейсе".

## 2. Базовые сущности

Минимальная схема обычно строится вокруг трех сущностей:

- `approval_request`
- `approval_decision`
- `approval_audit_record`

Этого уже достаточно, чтобы связать policy layer, runtime, trace schema и lifecycle artifacts.

## 3. Approval request

`approval_request` создается тогда, когда runtime сталкивается с действием, которое нельзя продолжать автоматически.

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
  target_system: jira
  destination: project://OPS
required_role: oncall_manager
status: pending
```

Что здесь особенно важно:

- `trace_id` и `session_id` связывают approval с run history;
- `capability` и `requested_action` не дают approval превратиться в абстрактное "да/нет";
- `required_role` помогает не смешивать любого reviewer с нужным approver;
- `requested_fields` фиксируют именно тот payload, который человек реально подтверждает.

## 4. Approval decision

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
- `decided_by` и `role` должны быть audit-friendly;
- `scope` не должен быть неявным;
- `expires_at` полезен, если approval не должен жить бесконечно.

## 5. Approval audit record

`approval_audit_record` связывает решение с реальным side effect или отказом от него.

```yaml
kind: approval_audit_record
approval_id: apr-2026-04-07-001
trace_id: trace-approval-001
decision: approved
executed: true
executed_capability: ticket_write
tool_principal: svc-ticket-writer
result_status: success
linked_events:
  - approval_requested
  - approval_resolved
  - tool_called
  - tool_succeeded
```

Это уже не просто "решение было принято", а понятный operational след:

- запросили;
- одобрили или отклонили;
- выполнили или не выполнили;
- понятно, каким principal был сделан side effect.

## 6. Как это связано с trace schema

Approval schema живет не отдельно, а рядом с trace schema:

- `approval_requested`
- `approval_resolved`
- `tool_called`
- `tool_succeeded`
- `tool_failed`

Именно поэтому хороший approval flow должен легко восстанавливаться как из отдельного audit record, так и из trace.

## 7. Как это связано с policy bundle

Policy bundle отвечает на вопросы:

- какая capability требует approval;
- кто имеет право approve;
- какие risk tiers вообще существуют;
- какие действия запрещены без human gate.

Approval schema отвечает на другой слой:

- как выглядит сам запрос;
- что именно человек подтверждает;
- как хранится решение;
- как это решение связывается с выполнением.

## 8. Связь с reference package

В [agent_runtime_ref](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref) уже есть operational primitives, которые поддерживают эту модель:

- [approvals.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/approvals.py)
- [configs/approvals.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/approvals.yaml)
- CLI:
  - `inspect-approvals`
  - `resolve-approval`

Это полезно тем, что approval можно не только описывать, но и реально прогонять как часть demo runtime.

## 9. Минимальные инварианты

Если коротко, у зрелого approval layer должны быть такие инварианты:

- у каждого запроса есть стабильный `approval_id`;
- approval привязан к `trace_id` и `session_id`;
- ясно, какой payload был одобрен;
- approver и role сохраняются в audit trail;
- side effect можно связать с конкретным approval decision;
- expired approval не используется повторно.

## 10. Что чаще всего ломается

Типовые проблемы здесь довольно узнаваемы:

- approval request не содержит реального action payload;
- approver видит слишком мало контекста;
- решение хранится только в UI и не доходит до trace;
- runtime не различает `approved once` и `approved forever`;
- side effect исполняется другим payload, чем тот, который был одобрен;
- никто не может восстановить, кто подтвердил рискованное действие.

## 11. Практический чеклист

Если хочешь быстро проверить свой approval layer, пройди по вопросам:

- Есть ли у approval request явный `approval_id`?
- Привязан ли approval к `trace_id` и `session_id`?
- Видит ли approver ровно тот payload, который потом идет в действие?
- Сохраняются ли `decided_by`, `role` и `decision scope`?
- Можно ли связать approval с реальным tool execution?
- Есть ли audit-friendly record для approved и rejected путей?

Если на несколько вопросов подряд ответ "нет", у тебя есть human gate по смыслу, но еще нет полноценного approval contract.

## См. также

- [Схема policy bundle и approval contract](policy-bundle-schema.md)
- [Схема трасс и каталог событий](trace-schema.md)
- [Схема lifecycle-артефактов](lifecycle-artifact-schema.md)
- [Опорный пакет](reference-package.md)
- [Глава 4. Tool gateway, approval и audit trail](../book/part-ii/chapter-4.md)
- [Глава 17. Слой политик и каталог возможностей](../book/part-vii/chapter-17.md)
