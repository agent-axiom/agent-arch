# 第 27 章：Agent Inventory、Registry 与 Sprawl 治理

!!! info "时效说明"
    本章内容截至 2026 年 4 月 11 日。

    变化最快的部分：

    - inventory discovery、registry sync 和 governance automation 的平台能力；
    - 各家平台对 agents、assistants 和 agent-like entities 的分类方法；
    - 面向大规模 estate 的 drift detection 与 policy enforcement 实践。

    变化相对较慢的部分：

    - 必须区分 inventory 和 registry；
    - 每个生产级 agent 都需要 owner、lifecycle state、capability record 和 runtime-control ownership；
    - 定期 review 仍然是避免 sprawl 变成 blind spot 的关键。

## 1. 为什么几乎每个成功的 agent 计划都会出现 sprawl

一旦第一批 agent systems 证明了价值，组织里通常很快就会出现同一种局面：

- 一个团队做了 support agent；
- 另一个团队做了 internal knowledge agent；
- 第三个团队加了 workflow assistant；
- 第四个团队为了本地任务快速拼了一个窄场景 agent。

这些决定单看都可能很合理。问题会在后面出现，因为很快就没人能快速回答：

- 到底一共有多少 agents；
- 哪些真的是 production，哪些只是“临时的”；
- 它们的 owner 是谁；
- 它们有哪些 capabilities；
- 用了哪些 identities、connectors 和 tool principals；
- 哪些其实还活着；
- 哪些仍然挂着 paused approvals、background routes 或 deprecated contract paths。

这正是值得被称作 `agent sprawl` 的状态。

## 2. 为什么 sprawl 不只是组织问题

表面上看，这像是一个管理问题：对象太多、秩序太差。

但在实践里，sprawl 很快就会变成 risk multiplier：

- orphaned agents 在没有 owner 的情况下继续运行；
- deprecated agents 还保留着 systems 和 data 的访问权；
- 不同团队对 approvals 和 policy boundaries 的理解不一样；
- observability coverage 会碎片化；
- inventory drift 会让 release gates 和 incident review 变得不可靠。

Microsoft 直接把不完整 inventory 和 agent sprawl 与 blind spots、inconsistent enforcement、delayed detection 联系在一起。 [^ms-inventory][^ms-agentic-risk]

## 3. Inventory 和 registry 不是同一层

最好把下面两层分开看：

- `agent inventory`
- `agent registry`

Inventory 回答的问题是：

- 环境里到底有哪些 agent-like entities 存在。

Registry 回答的是更严格的问题：

- 其中哪些已经被识别、分类、治理，并允许进入 production contours。

也就是说：

- inventory 解决的是可见性完整性；
- registry 解决的是治理。

没有 inventory，你不知道完整 estate。
没有 registry，你就无法有把握地说哪些 agents 是 approved 和 governed 的。

## 4. 一个最小 agent record 应该包含什么

对 production-grade agent systems 来说，一个最小的 registry record 通常至少应该包含：

- `agent_id`
- owner team
- business purpose
- lifecycle state
- allowed capabilities
- runtime identity
- tool principals
- approval requirements
- paused runs 与 background runs 的 ownership
- observability status
- artifact bundle linkage
- retirement plan linkage

它存在的意义不是“多一张表”，而是把 agent 这个实体明确地接到：

- security controls；
- operational ownership；
- lifecycle decisions。

## 5. Lifecycle states 比大多数团队想象的重要

太简单的 “active / inactive” 模型很快就会失效。

至少更实用的最小集合应该是：

- `proposed`
- `development`
- `pilot`
- `production`
- `restricted`
- `deprecated`
- `retired`

这样会更容易：

- 在 production 前限制 autonomy；
- 追踪 deprecated agents；
- 看出哪些 agents 还不该拥有 full egress 或 full approval paths；
- 在 replacement 和 retirement 中避免灰色地带。

## 6. Registry 不只是给 security team 用的

一个好的 agent registry 不只服务于 security 或 governance。

它同样服务于：

- platform team；
- product teams；
- SRE / operations；
- audit / compliance；
- incident responders。

对 platform team 来说，它展示哪些 patterns 真正在扩展。
对 operations 来说，它告诉你半夜该叫谁。
对 incident response 来说，它告诉你到底哪些 agents 可能参与了某个事件。

## 7. Sprawl 往往是从“小例外”开始的

现实里，动物园几乎从来不是正式策略。

它通常是从一些小放松开始：

- “这只是个内部 helper”；
- “这个 agent 是临时的”；
- “registry 先不加，之后再补”；
- “这里做 approval 太重了”；
- “telemetry 以后再接”。

几个月后，正是这些例外，构成了整个 estate 里最不透明的部分。

所以更稳妥的默认规则应该很简单：

- 如果一个实体可以代表组织行动、读取敏感上下文或调用 tools，它至少应该进入 inventory；
- 如果它进入 production contour，就必须进入 registry。

## 8. Registry 如何连接 observability

前一章已经说明，inventory coverage 本身就是 evidence layer 的一部分。

Registry 会把这层关系再拉紧一步：

- traces 可以挂上 registry metadata；
- detections 可以按 lifecycle state 来做；
- incidents 可以按 owner、risk tier 和 approval mode 过滤；
- release evidence 不只看 traces，也可以看 registry record 的状态。

也就是说，registry 会把 observability 从“原始事件流”提升成受治理的 operational map。

## 8.1. 没有 continuous verification 的 registry 会变得整洁，但不再准确

这里不应该高估 registry 本身。Registry 的存在，并不能自动证明 control layer 真的在工作。

如果 registry：

- 不和真实 telemetry coverage 对账；
- 不和活跃 principals 对账；
- 不和 active capabilities 对账；
- 不参与 retirement hygiene，

那它很快就会变成一幅整洁、但部分失真的 estate 图景。

所以，更成熟的理解方式是：registry 不应只是静态目录，而应该是 continuously verified control surface。

## 9. Registry 如何连接 approvals 和 policies

Registry 不应该去复制 policy bundle 或 approval contract。

它的职责是：

- 标明某个 agent 关联的是哪套 policy bundle 和 approval mode；
- 标明它是否有权使用某一组 capabilities；
- 标明它当前所处的 lifecycle state。

如果没有这层连接，就很容易出现这种状态：

- policy 变了；
- approval flow 变了；
- traces 变强了；
- 但没人知道到底哪些 agents 本来就该用这些 controls。

当 approval 和 long-running work 都变成显式 runtime paths 之后，这一点会更加重要。

这时 registry 还应该帮助回答：

- 哪些 agents 被允许因为 approval 而暂停 run；
- 哪些 agents 可以继续使用 background mode；
- stuck paused runs 由谁负责；
- aging background runs 由谁负责；
- 它们的 approval 与 capability payload 应该遵循哪个 contract version。

否则，整个 estate 表面上看起来像是 governed 的，实际却仍然隐藏着运行层面的模糊地带。

## 10. 一个最小 agent registry record 示例

```yaml
agent:
  agent_id: support-triage-ref
  owner_team: customer-platform
  business_purpose: support_ticket_triage
  lifecycle_state: production
  runtime_identity: agent://support-triage-ref
  tool_principals:
    - svc-ticket-writer
  allowed_capabilities:
    - ticket_read
    - ticket_write
  policy_bundle: policy-v4
  approval_mode: required_for_high_risk
  runtime_controls:
    approval_pause_allowed: true
    background_mode_allowed: true
    paused_run_owner: support-ops
    contract_version: capability-contract-v3
  observability:
    trace_enabled: true
    inventory_covered: true
  artifacts:
    bundle_id: bundle-2026-04-07-a
  retirement_plan: retire-support-v1
```

这个 record 已经足以把 agent 和 ownership、controls、lifecycle 连接起来。

## 11. 一个简单的 registry health check

```python
from dataclasses import dataclass


@dataclass
class AgentRegistryState:
    has_owner: bool
    has_lifecycle_state: bool
    has_policy_linkage: bool
    has_observability: bool
    has_runtime_control_linkage: bool


def registry_ready(state: AgentRegistryState) -> bool:
    return (
        state.has_owner
        and state.has_lifecycle_state
        and state.has_policy_linkage
        and state.has_observability
        and state.has_runtime_control_linkage
    )
```

这里的逻辑很直接：一个没有 owner、没有 lifecycle state、没有 observability linkage 的 agent，不应该被视为 production-ready entity。

## 12. 最常见的 failure modes

- agents 已经在生产环境里，但不在 inventory 中；
- inventory 存在，但 lifecycle states 没有维护；
- registry 不知道 principals 和 approvals；
- deprecated agents 还保留着 tool paths 的访问权；
- registry record 无法说明谁负责 paused approvals 或 aging background runs；
- contract versions 已经漂移，但 registry 仍指向过时的 control assumptions；
- 多个 registry 之间发生漂移；
- platform team 认识一批 agents，而 security team 认识另一批。

## 13. 给 agent governance 做一次快速成熟度测试

团队不应该只因为已经有一张 registry spreadsheet 和一个大概的 deployed agents 数量，就觉得自己已经控制住了整个 agent estate。

更高的标准应该是：

- inventory 和 registry 被当成不同的 control surfaces；
- 每个 production agent 都有 owner、lifecycle state 和 policy linkage；
- telemetry coverage 能持续和 registry 对账；
- paused approvals、background-run ownership 与 contract versions 也是 registry control surface 的一部分；
- deprecated 和 orphaned agents 能在变成 blind spots 之前被找到；
- governance 能区分 discovered entities 和 approved production agents。

如果这些条件大多不成立，那团队也许已经有一些 visibility fragments，但还没有真正的 agent governance。

## 14. 实用检查清单

- 你能快速说出 active、deprecated 和 retired agents 的数量吗？
- 每个 production agent 都有 owner 吗？
- registry record 是否和 policy bundle、approval mode、runtime-control ownership、bundle_id 关联？
- inventory 能不能显示哪些 agents 没有发 telemetry？
- 你能不能快速找出 orphaned 或 deprecated、但 principals 还活着的 agents？
- 你有没有明确区分“被发现”与“被批准进入 production”？

如果连续几个答案都是“否”，那说明你已经有 agent estate，但还没有真正的 agent governance。

## 15. 值得配套阅读的参考页

- [Lifecycle Artifact Schema](../../appendix/lifecycle-artifact-schema.zh.md)
- [Policy Bundle Schema 与 Approval Contract](../../appendix/policy-bundle-schema.zh.md)
- [Approval Request 与 Decision Schema](../../appendix/approval-schema.zh.md)
- [Trace Schema 与 Event Catalog](../../appendix/trace-schema.zh.md)
- [研究前沿：记忆、可观测性与多智能体可靠性](../../appendix/research-frontier.zh.md)

- [第 26 章：AI-Native Observability、Inventory Coverage 与 Detection-Ready Telemetry](chapter-26.zh.md)
- [第 23 章：Retirement、Replacement 与 End-of-Life Discipline](chapter-23.zh.md)

[^ms-inventory]: Microsoft Learn, [Complete production infrastructure inventory](https://learn.microsoft.com/en-us/security/zero-trust/sfi/complete-production-infrastructure-inventory)
[^ms-agentic-risk]: Microsoft Learn, [Reduce autonomous agentic AI risk](https://learn.microsoft.com/en-us/security/zero-trust/sfi/manage-agentic-risk)
