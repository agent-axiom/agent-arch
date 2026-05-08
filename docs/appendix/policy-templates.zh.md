# 按场景组织的策略模板与检查清单

这一页的目的，是让书里的案例不仅能读，还能拿来做起点。

这里的意思不是“给你一份通用的生产策略 YAML”。相反，重点是展示：不同场景下，策略层会如何开始真正分化。

如果你先需要场景上下文，请先读[实战案例](case-studies.zh.md)。如果你想看项目接下来的待办，请看[社区路线图](community-roadmap.zh.md)。

## 如何阅读这些模板

最好把它们看成骨架，而不是成品：

- 系统把什么视为高风险；
- 审批边界放在哪里；
- 读取和写入动作如何分开；
- 哪些停止条件和升级规则是必要的；
- 哪些追踪和审计信号应该被视为强制项。

!!! example "重复工单线索的策略"
    对于贯穿的 support-triage 案例，`create_ticket` 不能只是一个写工具：它需要受治理的能力边界、强制 idempotency key、可追踪的写入意图、针对 `side_effect_unknown` 的停止条件，以及能在变更发布前捕获重复建单的 rollout/eval gate。

## 模板 1：支持分诊智能体

### 这类策略需要保证什么

在支持分诊场景里，你通常需要：

- 安全地读取客户上下文；
- 在信心不足时避免写动作；
- 当需要人工介入时，不要让模型假装问题已经解决；
- 明确限制工单创建和敏感更新。

### 策略骨架示例

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

### 检查清单

- 读取工具是否带租户范围？
- 智能体是否能诚实升级，而不是总想直接回答？
- `create_ticket` 是否被显式审批策略保护？
- 追踪里能不能看见为什么走到了写入路径？
- 对低置信度有没有停止条件？

## 模板 2：内部知识智能体

### 这类策略需要保证什么

在知识场景里，主要风险不是副作用，而是访问控制和依据质量。

你通常需要：

- 按角色隔离访问；
- 把检索限定在允许的来源内；
- 防止智能体混淆不可信内容和指令；
- 强制答案里带来源引用。

### 策略骨架示例

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

### 检查清单

- 检索路径上的基于角色过滤是否真的有效？
- 智能体返回的是来源支撑的答案，而不只是漂亮文本吗？
- 对依据较弱的情况有没有单独策略？
- 检索会不会泄漏私有知识区？
- 追踪能不能说明到底用了哪些文档？

## 模板 3：事故协调智能体

### 这类策略需要保证什么

在事故场景里，策略不只是管理访问，还要管理编排纪律。

你通常需要：

- 让整条运行共享一条追踪；
- 在交接时记录负责人；
- 限制高风险修复；
- 防止噪声输入演化成多余副作用。

### 策略骨架示例

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

### 检查清单

- 每个交接都有负责人和原因吗？
- 高风险修复默认是关闭的吗？
- 工单和通知受幂等性保护吗？
- 事故追踪能不能展示完整决策路径？
- 噪声告警会不会单独触发危险写入路径？

## 策略层的通用检查清单

不管是什么场景，都值得问这些问题：

- 你是否清楚系统里的 `read`、`write` 和 `advisory` 动作分别在哪里？
- 高风险动作是否有独立审批边界？
- 策略里能不能明确看出智能体应该停下，而不是继续推理的地方？
- 关键规则是不是只活在提示里？
- 安全团队能不能在不了解全部提示工程细节的情况下看懂策略工件？

如果连续几个问题的答案都是“不能”，说明你的策略层仍然过于隐式。

## 下一步做什么

- [实战案例](case-studies.zh.md)
- [第 3 章：安全边界与信任边界](../book/part-ii/chapter-3.zh.md)
- [第 17 章：策略层与能力目录](../book/part-vii/chapter-17.zh.md)
