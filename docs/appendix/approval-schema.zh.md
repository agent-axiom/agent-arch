# Approval Request 与 Decision Schema

这一页描述 agent systems 里 human approval 的最小 contract layer：approval request 长什么样，decision record 长什么样，以及 high-risk action 之后应该在 audit trail 里留下什么。

如果 [policy bundle](policy-bundle-schema.zh.md) 回答的是“当前到底有哪些规则在生效”，那么 approval schema 回答的就是“runtime 如何把最后一道决定权交给人”。

## 1. 为什么要单独有 approval schema

一种非常常见的失败路径是：

- policy 说某个 action 属于 high-risk；
- runtime 返回 `approval_required`；
- 后面的逻辑全都散落在 UI 或团队口头约定里。

这样会丢掉：

- 稳定的 request 格式；
- 可审查的 decision record；
- 可重复的 audit trail；
- approval 与具体 run 或 trace 之间的连接。

所以审批边界最好被建模成 machine-readable contract，而不是界面上的一颗按钮。

## 2. 核心实体

一个最小可用的 approval schema，通常围绕三个实体：

- `approval_request`
- `approval_decision`
- `approval_audit_record`

这已经足够把 policy layer、runtime、trace schema 和生命周期工件串起来。

## 3. Approval request

`approval_request` 会在 runtime 遇到不能自动继续的 action 时被创建。

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

这里最重要的是：

- `trace_id` 和 `session_id` 把 approval 绑到 run history 上；
- `capability` 和 `requested_action` 防止 approval 退化成抽象的 yes/no；
- `required_role` 让“谁都能看一眼”与“真正有权限批准的人”区分开；
- `requested_fields` 固定了人类真正批准的 payload。

## 4. Approval decision

`approval_decision` 用来表达人到底做了什么决定，以及依据是什么。

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

这里的关键不变量是：

- decision 必须指向具体的 `approval_id`；
- `decided_by` 和 `role` 要能进入 audit；
- `scope` 必须明确；
- `expires_at` 对于不能长期复用的 approval 很重要。

## 5. Approval audit record

`approval_audit_record` 把 decision 和真实的 side effect 或拒绝执行联系起来。

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

这样它就不再只是“有人点了同意”，而是一个完整的 operational record：

- 请求被提出；
- 它被批准或拒绝；
- action 被执行或没有执行；
- 具体由哪个 principal 产生了 side effect 也可追踪。

## 6. 它和 trace schema 的关系

Approval schema 不应该独立存在，而应该和 trace schema 通过这些事件接起来：

- `approval_requested`
- `approval_resolved`
- `tool_called`
- `tool_succeeded`
- `tool_failed`

这也是为什么好的 approval flow 应该既能从 audit record 还原，也能从 trace 还原。

## 7. 它和 policy bundle 的关系

Policy bundle 回答的是：

- 哪个 capability 需要 approval；
- 谁可以 approve；
- 有哪些 risk tiers；
- 哪些 action 没有人类门禁就绝对不能执行。

Approval schema 回答的是另一层：

- 请求本身长什么样；
- 人到底批准了什么；
- decision 怎么被保存；
- 这个 decision 怎么和执行关联。

## 8. 它和 reference package 的关系

[agent_runtime_ref](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref) 已经包含了支撑这套模型的 operational primitives：

- [approvals.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/approvals.py)
- [configs/approvals.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/approvals.yaml)
- CLI：
  - `inspect-approvals`
  - `resolve-approval`

这让 approval 不只是概念说明，而是真的可以在 demo runtime 里跑起来。

## 9. 最小不变量

一个成熟的 approval layer，至少应该保证：

- 每个 request 都有稳定的 `approval_id`；
- approval 绑定到 `trace_id` 和 `session_id`；
- 被批准的 payload 是明确的；
- approver 和 role 会进入 audit trail；
- side effect 能追溯到具体 approval decision；
- 过期 approval 不会被静默复用。

## 10. 最常见的断裂点

这里的典型问题通常很容易识别：

- approval request 不包含真实 action payload；
- approver 看到的上下文太少；
- decision 只存在于 UI，没有进入 trace；
- runtime 不区分“只批准这一次”和“永远都批准”；
- side effect 执行时用的 payload 和批准时不是同一个；
- 事后没人能还原到底是谁批准了这个 risky action。

## 11. 实用检查清单

你可以快速问自己：

- approval request 是否有明确的 `approval_id`？
- approval 是否绑定到 `trace_id` 和 `session_id`？
- approver 看到的是不是之后真正会执行的 payload？
- `decided_by`、`role` 和 `decision scope` 是否被保存？
- approval 能不能与真实的 tool execution 对上？
- approved 和 rejected 两种路径是否都有 audit-friendly record？

如果连续几个答案都是“否”，那说明你虽然已经有人工门禁，但还没有真正完整的 approval contract。

## 延伸阅读

- [Policy Bundle Schema 与 Approval Contract](policy-bundle-schema.zh.md)
- [Trace Schema 与 Event Catalog](trace-schema.zh.md)
- [Lifecycle Artifact Schema](lifecycle-artifact-schema.zh.md)
- [Reference Package](reference-package.zh.md)
- [第 4 章：Tool Gateway、Approval 与 Audit Trail](../book/part-ii/chapter-4.zh.md)
- [第 17 章：策略层与能力目录](../book/part-vii/chapter-17.zh.md)
