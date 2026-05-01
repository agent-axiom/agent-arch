# 审批请求与决策记录 Schema

这一页描述智能体系统里人工审批的最小契约层：审批请求长什么样，决策记录长什么样，以及高风险动作之后应该在审计轨迹里留下什么。

它也直接连接到书里的 [Evidence Spine：从请求到发布判断](../book/part-v/evidence-spine.zh.md)，因为审批正是让一次受治理运行从请求一直保持可读到发布判断的关键记录之一。

如果 [策略包](policy-bundle-schema.zh.md) 回答的是“当前到底有哪些规则在生效”，那么审批 Schema 回答的就是“运行时如何把最后一道决定权交给人”。

## 1. 为什么要单独有审批 Schema

一种非常常见的失败路径是：

- 策略说某个动作属于高风险；
- 运行时返回 `approval_required`；
- 后面的逻辑全都散落在界面或团队口头约定里。

这样会丢掉：

- 稳定的请求格式；
- 可审查的决策记录；
- 可重复的审计轨迹；
- 审批与具体运行或追踪之间的连接。

所以审批边界最好被建模成机器可读的契约，而不是界面上的一颗按钮。

## 2. 核心实体

一个最小可用的审批 Schema，通常围绕三个实体：

- `approval_request`
- `approval_decision`
- `approval_audit_record`

这已经足够把策略层、运行时、追踪 Schema 和生命周期工件串起来。

## 3. 审批请求

`approval_request` 会在运行时遇到不能自动继续的动作时被创建。

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
sandbox_context:
  sandbox_profile_contract: sandbox-profile-v1
  workspace_entries_reviewed: true
  permissions_profile: restricted-shell-network-denied
  network_secrets_posture: network:denied,secrets:none
  snapshot_policy: required_on_completion
required_role: oncall_manager
status: pending
```

这里最重要的是：

- `trace_id` 和 `session_id` 把审批绑到运行历史上；
- `capability` 和 `requested_action` 防止审批退化成抽象的是/否；
- `required_role` 让“谁都能看一眼”与“真正有权限批准的人”区分开；
- `requested_fields` 固定了人类真正批准的载荷；
- `sandbox_context` 对由 sandbox 支撑的动作很重要，审批人需要看到 workspace materialization、permissions 与 snapshot/resume policy，而不只是业务载荷。

## 4. 审批决策

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

- 决策必须指向具体的 `approval_id`；
- `decided_by` 和 `role` 要能进入审计；
- `scope` 必须明确；
- `expires_at` 对于不能长期复用的审批很重要。

## 5. 审批审计记录

`approval_audit_record` 把决策和真实的副作用或拒绝执行联系起来。

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

这样它就不再只是“有人点了同意”，而是一条完整的运营记录：

- 请求被提出；
- 它被批准或拒绝；
- 动作被执行或没有执行；
- 具体由哪个主体产生了副作用也可追踪。

## 6. 它和追踪 Schema 的关系

审批 Schema 不应该独立存在，而应该和追踪 Schema 通过这些事件接起来：

- `approval_requested`
- `approval_resolved`
- `tool_called`
- `tool_succeeded`
- `tool_failed`

这也是为什么好的审批流程应该既能从审计记录还原，也能从追踪还原。如果审批出现在失败运行演练或其他退化路径里，这种还原还应该和会话导出对得上，包括 `failure_reason` 这样的字段，而不是只停留在审批记录本身。

## 7. 它和策略包的关系

策略包回答的是：

- 哪个能力需要审批；
- 谁可以批准；
- 有哪些风险等级；
- 哪些动作没有人类门禁就绝对不能执行。

审批 Schema 回答的是另一层：

- 请求本身长什么样；
- 人到底批准了什么；
- 决策怎么被保存；
- 这个决策怎么和执行关联。

## 8. 它和参考包的关系

[agent_runtime_ref](https://github.com/agent-axiom/agent-arch/tree/main/agent_runtime_ref) 已经包含了支撑这套模型的运营基础构件：

- [approvals.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/approvals.py)
- [configs/approvals.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/approvals.yaml)
- CLI：
  - `inspect-approvals`
  - `resolve-approval`

`inspect-approvals` 会返回 `trace_id`、`session_id`、`count` 和 `approvals`；`resolve-approval` 会返回 `approval_id`、`status`、`reviewer`、`resolution_note`、`authorization_mode`、`delegated_principal_id` 和 `delegated_scope`，因此可运行 demo 在决策前后都会保留可见的 approval lineage 与 delegated authority。

内置的 `approvals.yaml` 也会明确 approval operating policy：`default_reviewer`、`escalation_sla_minutes`，以及 `delegated_authorization` 下的 `reviewer_required_for_user_delegation`、`require_principal_binding`、`require_scope_visibility`、`on_scope_revoked` 和 `subagent_inheritance`，共同说明谁来评审 delegated actions、哪些 evidence 必须保持可见，以及 delegation 是否可以传递给 subagents。Reference policy 将 subagent inheritance 设为 `explicit_only`，因此 delegated authority 不会流入 child agent，除非 approval path 明确点名。

这让审批不只是概念说明，而是真的可以在演示运行时里跑起来。

## 9. 最小不变量

一个成熟的审批层，至少应该保证：

- 每个请求都有稳定的 `approval_id`；
- 审批绑定到 `trace_id` 和 `session_id`；
- 被批准的载荷是明确的；
- 审批人和角色会进入审计轨迹；
- 副作用能追溯到具体审批决策；
- 过期审批不会被静默复用。

## 10. 最常见的断裂点

这里的典型问题通常很容易识别：

- 审批请求不包含真实动作载荷；
- 审批人看到的上下文太少；
- 决策只存在于界面，没有进入追踪；
- 运行时不区分“只批准这一次”和“永远都批准”；
- 由 sandbox 支撑的审批隐藏了 sandbox profile、workspace entries 或 permissions；
- 副作用执行时用的载荷和批准时不是同一个；
- 事后没人能还原到底是谁批准了这个高风险动作。

## 11. 现在就该做什么

先过一遍这份短清单，把所有回答为“否”的地方单独记下来：

- 审批请求是否有明确的 `approval_id`？
- 审批是否绑定到 `trace_id` 和 `session_id`？
- 审批人看到的是不是之后真正会执行的载荷？
- 如果动作由 sandbox 支撑，审批人是否能看到 sandbox profile contract、workspace entries、permissions 与 snapshot/resume policy？
- `decided_by`、`role` 和决策范围是否被保存？
- 审批能不能与真实的工具执行对上？
- 批准和拒绝两种路径是否都有便于审计的记录？

如果连续几个答案都是“否”，那说明你虽然已经有人工门禁，但还没有真正完整的审批契约。

## 下一步做什么

- [策略包 Schema 与审批契约](policy-bundle-schema.zh.md)
- [追踪 Schema 与事件目录](trace-schema.zh.md)
- [生命周期工件 Schema](lifecycle-artifact-schema.zh.md)
- [参考包](reference-package.zh.md)
- [第 4 章：工具网关、审批与审计轨迹](../book/part-ii/chapter-4.zh.md)
- [第 17 章：策略层与能力目录](../book/part-vii/chapter-17.zh.md)
