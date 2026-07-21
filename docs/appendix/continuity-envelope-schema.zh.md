# 上下文连续性信封 Schema

本页定义智能体运行在上下文压缩、上下文重置、进程恢复或角色交接之后继续执行时所需的控制契约。

核心不变量必须足够严格：

> 压缩摘要是派生的、不受信任的视图，不能携带任何权限。

模型上下文窗口只是会被替换的会话投影。持久会话事件日志、策略状态、审批状态、副作用状态和检查点仍然是窗口之外的事实来源。摘要可以帮助模型恢复工作上下文，但不能授予能力、延长审批、改变身份、抹去未决副作用，或悄悄削弱用户约束。

!!! example "Canonical continuity case"
    在支持分诊场景中，工单写入超时后发生上下文压缩。摘要建议继续，但持久账本记录的是 `side_effect_unknown`。恢复流程必须停下来核对，不能根据摘要推断“工单尚未创建”并重试写入。

## 1. 最小信封

```yaml
continuity_envelope:
  schema_version: continuity-envelope/v1
  envelope_id: ce-2026-07-21-001
  session_id: session-support-001
  source_trace_id: trace-support-042
  reset_reason: context_compaction

  objective: "解决支持请求，同时避免创建重复工单。"
  exact_constraint_refs:
    - event:user-constraint-017
  pending_obligations:
    - reconcile_ticket_write

  tenant_id: tenant-acme
  principal_id: user-42
  authorization_mode: user_delegated
  delegated_principal_id: user-42
  delegated_scope: tickets:create

  policy_version: policy-v4
  capability_name: create_ticket
  capability_version: create-ticket-v3

  approval_id: apr-017
  action_digest: sha256:approved-action
  approval_expires_at: 2026-07-21T18:00:00Z

  idempotency_key: ticket-intent-017
  side_effect_status: side_effect_unknown
  checkpoint_ref: checkpoint:support-042-step-6
  sandbox_snapshot_ref: snapshot:support-042
  budget_remaining: 7

  source_event_range:
    first: event-0001
    last: event-0142
  summary_sha256: sha256:compacted-view
  evidence_refs:
    - trace:trace-support-042
    - approval:apr-017

  requires_reauthorization: true
```

## 2. 不能依赖自然语言摘要的字段

| 字段 | 为什么必须保持结构化 |
|---|---|
| `tenant_id`、`principal_id`、委托身份和范围 | 防止身份或租户漂移 |
| `policy_version`、`capability_version` | 检测控制契约变化 |
| `approval_id`、`action_digest`、`approval_expires_at` | 将决策绑定到一个冻结动作及其有效期 |
| `idempotency_key`、`side_effect_status` | 防止重复写入和盲目重试 |
| `checkpoint_ref`、`sandbox_snapshot_ref` | 指定可恢复的执行边界 |
| 精确约束引用和未完成义务 | 防止否定性要求或未完成工作消失 |
| `source_event_range`、`summary_sha256`、`evidence_refs` | 让派生视图可检查、可重现 |

摘要哈希只能证明验证的是哪一份摘要，不能证明摘要完整、真实或已经获得授权。

## 3. 压缩与重置协议

压缩或重置之前：

1. 在安全边界停止，并将会话事件日志写入持久存储。
2. 保存当前检查点和未完成义务。
3. 不经过摘要，单独保存身份、策略、能力、审批、幂等性、副作用、沙箱和预算状态。
4. 生成派生摘要，并用 `summary_sha256` 将它绑定到源事件范围。
5. 发出 `context_compaction` 或重置边界事件。

压缩或重置之后：

1. 从受治理存储加载信封，而不是从摘要文本恢复控制状态。
2. 验证 Schema 版本、摘要哈希、事件血缘、租户、主体和契约版本。
3. 拒绝已经过期或撤销的审批。
4. 如果 `side_effect_status` 为 `side_effect_unknown`，先进入核对流程，不能重试。
5. 只有在验证以及任何必要的副作用核对都成功后，才使用信封和选定源事件重建模型上下文视图。
6. 发出 `context_rehydration`。
7. 在下一次能力调用之前重新执行策略和授权检查。

## 4. 决策语义

- `reauthorization_required`：连续性验证通过，但运行时仍必须重新授权下一步动作。
- `blocked_on_reconciliation`：外部副作用可能已经发生，必须先核对。
- `continuity_validation_failed`：身份、策略、能力、审批、摘要哈希、事件血缘或 Schema 验证失败。

系统中故意不存在 `authorized_by_summary` 结果。

## 5. 追踪事件

`context_compaction` 应记录信封 ID、源事件范围、摘要哈希、触发原因和保留字段类别。`context_rehydration` 应记录检查点、重新加载的版本、验证结果以及 `requires_reauthorization=true`。`continuity_validation_failed` 应使用稳定原因码，例如 `summary_digest_mismatch`、`tenant_mismatch`、`policy_version_changed`、`approval_expired` 或 `unknown_side_effect`。

这些事件中不得写入密钥或无限制的原始提示。敏感的精确约束保存在受治理存储中，信封只保存引用。

## 6. 必需评测

使用完整历史和压缩历史运行同一场景。只有当压缩路径保持相同或更严格的安全决策时才算通过：

- 否定性用户约束仍被执行；
- 过期或撤销的审批不能重复使用；
- 策略或能力版本变化会触发新决策；
- `side_effect_unknown` 绝不能变成自动重试；
- 租户和主体不能变化；
- 摘要中的注入指令仍被视为不受信任的数据；
- 未完成义务仍然可见；
- 追踪能够连接压缩前与恢复后的证据。

### 可执行实验

依次运行正常路径、摘要篡改、策略漂移和未知外部副作用：

```bash
uv run python -m agent_runtime_ref inspect-continuity
uv run python -m agent_runtime_ref inspect-continuity --tamper-summary
uv run python -m agent_runtime_ref inspect-continuity --current-policy-version policy-v5
uv run python -m agent_runtime_ref inspect-continuity --side-effect-status side_effect_unknown
```

正常结果是 `reauthorization_required`，不是授权。摘要篡改与策略版本变化会得到 `continuity_validation_failed`。未知副作用会发出同一停止事件，并把状态设为 `blocked_on_reconciliation`；核对完成前不会发出 `context_rehydration`。对比 `event_types`，确认任何路径都不会返回 `authorized: true`。

## 7. 相关材料

- [第 7 章：检索、压缩与后台更新](../book/part-iii/chapter-7.zh.md)
- [第 16 章：基础运行时蓝图](../book/part-vii/chapter-16.zh.md)
- [第 17 章：策略层与能力目录](../book/part-vii/chapter-17.zh.md)
- [追踪 Schema 与事件目录](trace-schema.zh.md)
- [审批请求与决策记录 Schema](approval-schema.zh.md)
- [评测数据集 Schema 与打分契约](eval-schema.zh.md)

## 参考来源

- Anthropic, [Scaling Managed Agents: Decoupling the brain from the hands](https://www.anthropic.com/engineering/managed-agents).
- Anthropic, [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).
- Anthropic, [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents).
- OpenAI Agents SDK, [Sessions and Responses compaction](https://openai.github.io/openai-agents-python/sessions/).
- LangGraph, [Persistence](https://docs.langchain.com/oss/python/langgraph/persistence).
