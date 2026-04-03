# 按场景组织的 Policy Templates 与 Checklists

这一页的目的，是让书里的案例不仅能读，还能拿来做起点。

这里的意思不是“给你一份通用的生产策略 YAML”。相反，重点是展示：不同场景下，policy layer 会如何开始真正分化。

## 如何阅读这些模板

最好把它们看成骨架，而不是成品：

- 系统把什么视为 risky；
- approval boundary 放在哪里；
- read 和 write actions 如何分开；
- 哪些 stop conditions 和 escalation rules 是必要的；
- 哪些 traces 和 audit signals 应该被视为强制项。

## 模板 1：Support Triage Agent

### 这类策略需要保证什么

在 support triage 场景里，你通常需要：

- 安全地读取客户上下文；
- 在信心不足时避免 write actions；
- 当需要人工介入时，不要让模型假装问题已经解决；
- 明确限制 ticket creation 和敏感更新。

### Policy skeleton 示例

```yaml
agent:
  name: support_triage
  allowed_models: ["gpt-5.4", "gpt-5-mini"]
  max_steps: 12
  stop_conditions:
    - enough_information_to_answer
    - requires_human_review
    - write_requires_approval

tools:
  read_customer_profile:
    mode: read
    tenant_scoped: true
    approval: none

  read_ticket_history:
    mode: read
    tenant_scoped: true
    approval: none

  create_ticket:
    mode: write
    approval: manager
    idempotency_key_required: true
    retry_on: ["retryable_failure"]

output:
  require_structured_decision: true
  require_escalation_reason: true
```

### Checklist

- read tools 是否带 tenant scope？
- agent 是否能诚实升级，而不是总想直接回答？
- `create_ticket` 是否被显式 approval policy 保护？
- trace 里能不能看见为什么走到了 write path？
- 对低置信度有没有 stop condition？

## 模板 2：Internal Knowledge Agent

### 这类策略需要保证什么

在 knowledge 场景里，主要风险不是 side effects，而是访问控制和 grounding 质量。

你通常需要：

- 按角色隔离访问；
- 把 retrieval 限定在允许的来源内；
- 防止 agent 混淆 untrusted content 和 instructions；
- 强制答案里带 source references。

### Policy skeleton 示例

```yaml
agent:
  name: internal_knowledge
  allowed_models: ["gpt-5.4", "gpt-5-mini"]
  max_steps: 8
  stop_conditions:
    - answer_ready
    - insufficient_grounding
    - access_denied

retrieval:
  role_scoped: true
  tenant_scoped: true
  max_documents: 8
  require_source_labels: true

output:
  require_sources: true
  deny_if_no_grounding: true
  deny_sensitive_snippets_without_access: true
```

### Checklist

- retrieval path 上的 role-based filtering 是否真的有效？
- agent 返回的是来源支撑的答案，而不只是漂亮文本吗？
- 对 weak grounding 有没有单独 policy？
- retrieval 能不能泄漏私有 knowledge zone？
- traces 能不能说明到底用了哪些文档？

## 模板 3：Incident Coordination Agent

### 这类策略需要保证什么

在 incident 场景里，policy 不只是管理访问，还要管理 orchestration discipline。

你通常需要：

- 让整条 run 共享一条 trace；
- 在 handoff 时记录 ownership；
- 限制 risky remediation；
- 防止 noisy input 演化成多余的 side effects。

### Policy skeleton 示例

```yaml
agent:
  name: incident_coordinator
  allowed_models: ["gpt-5.4"]
  max_steps: 20
  orchestration:
    pattern: manager_with_controlled_handoffs
    require_handoff_reason: true
    require_current_owner: true

tools:
  create_incident_thread:
    mode: write
    approval: oncall_lead
    idempotency_key_required: true

  notify_team:
    mode: write
    approval: oncall_lead
    idempotency_key_required: true

  suggest_remediation:
    mode: advisory
    approval: none

  execute_remediation:
    mode: write
    approval: security_and_service_owner
    disabled_by_default: true

audit:
  require_trace_per_run: true
  require_handoff_log: true
  require_write_intent_log: true
```

### Checklist

- 每个 handoff 都有 owner 和 reason 吗？
- risky remediation 默认是关闭的吗？
- ticketing 和 notifications 受 idempotency 保护吗？
- incident trace 能不能展示完整决策路径？
- noisy alert 会不会单独触发 dangerous write path？

## Policy Layer 的通用 Checklist

不管是什么场景，都值得问这些问题：

- 你是否清楚系统里的 `read`、`write` 和 `advisory` 动作分别在哪里？
- risky actions 是否有独立 approval boundary？
- policy 里能不能明确看出 agent 应该停下，而不是继续 reasoning 的地方？
- 关键规则是不是只活在 prompts 里？
- security 团队能不能在不了解全部 prompt engineering 细节的情况下看懂 policy artifacts？

如果连续几个问题的答案都是“不能”，说明你的 policy layer 仍然过于隐式。

## 接下来读什么

- [实战案例](case-studies.zh.md)
- [第 3 章：安全边界与信任边界](../book/part-ii/chapter-3.zh.md)
- [第 17 章：策略层与能力目录](../book/part-vii/chapter-17.zh.md)
