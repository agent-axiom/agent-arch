# 第 27 章：智能体清单、注册表与蔓延治理

!!! info "时效说明"
    本章内容截至 2026 年 4 月 11 日。

    变化最快的部分：

    - 面向智能体清单发现、注册表同步与治理自动化的平台能力；
    - 各家平台对智能体、助手与类智能体实体的分类方法；
    - 面向大规模智能体群体的漂移检测与策略执行实践。

    变化相对较慢的部分：

    - 必须区分清单与注册表；
    - 每个生产级智能体都需要负责人、生命周期状态、能力记录与 runtime-control 责任归属；
    - 定期审查仍然是避免蔓延变成治理盲区的关键。

## 1. 为什么几乎每个成功的智能体计划都会出现蔓延

一旦第一批智能体系统证明了价值，组织里通常很快就会出现同一种局面：

- 一个团队做了支持智能体；
- 另一个团队做了内部知识智能体；
- 第三个团队加了工作流助手；
- 第四个团队为了本地任务快速拼了一个窄场景智能体。

这些决定单看都可能很合理。问题会在后面出现，因为很快就没人能快速回答：

- 到底一共有多少个智能体；
- 哪些真的在生产环境里运行，哪些只是“临时的”；
- 它们的负责人是谁；
- 它们到底拥有哪些能力；
- 它们用了哪些身份、连接器和工具主体；
- 哪些其实还活着；
- 哪些仍然挂着暂停中的审批、后台路由、已废弃的契约路径或陈旧的 verifier contracts。

这正是值得被称作 `agent sprawl` 的状态。

注册表这一层首先是为了做成一件事，让整个智能体群体具备可追责性。对于任何生产级智能体，团队都应该能快速回答：谁拥有它、哪些控制约束它、哪些证据描述它，以及一旦它发生漂移该由谁采取行动。

这种可追责性就是本章的重心。注册表并不拥有证据主干，也不拥有遥测基底。它真正拥有的是，从受治理实体到负责人、状态和问责路径之间的映射。

这也正是本章的核心承诺。它要帮助读者把注册表看成整个智能体群体的问责层：在这里，受治理实体不再只是模糊的一群工具和助手，而会变成拥有负责人、生命周期状态与明确责任的可追责生产系统。

## 2. 为什么蔓延不只是组织问题

表面上看，这像是一个管理问题：对象太多、秩序太差。

但在实践里，蔓延很快就会变成风险放大器：

- 失去负责人的智能体还在继续运行；
- 已废弃的智能体仍保留着系统和数据访问权；
- 不同团队对审批要求和策略边界的理解并不一致；
- 可观测性覆盖会碎片化；
- 清单漂移会让发布门禁和事故复盘变得不可靠。

Microsoft 直接把不完整的清单和智能体蔓延与 blind spots、inconsistent enforcement、delayed detection 联系在一起。 [^ms-inventory][^ms-agentic-risk]

## 3. 清单和注册表不是同一层

最好把下面两层分开看：

- `agent inventory`（智能体清单）
- `agent registry`（智能体注册表）

清单回答的问题是：

- 环境里到底有哪些类智能体实体存在。

注册表回答的是更严格的问题：

- 其中哪些已经被识别、分类、治理，并允许进入生产轮廓。

也就是说：

- 清单解决的是可见性完整性；
- 注册表解决的是治理。

没有清单，你就不知道完整的智能体群体是什么样。
没有注册表，你就无法有把握地说哪些智能体已经获批、受治理，而且在运行上可被追责。

## 4. 一个最小智能体记录应该包含什么

对生产级智能体系统来说，一个最小的注册表记录通常至少应该包含：

- `agent_id`
- 负责团队
- 业务用途
- 生命周期状态
- 允许使用的能力
- 运行时身份
- 工具主体
- 审批要求
- paused runs、background runs 与 capability sessions 的责任归属
- 可观测性状态
- verifier 或 eval evidence 状态
- 生效中与已废弃的 verifier-contract linkage
- artifact bundle linkage
- retirement plan linkage

它存在的意义不是“多一张表”，而是把智能体这个实体明确地接到：

- 安全控制；
- 运行责任；
- 生命周期决策。

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

- 在 `production` 前限制 autonomy；
- 追踪已废弃的智能体；
- 看出哪些智能体还不该拥有完整的出口访问权或完整的审批路径；
- 在 replacement 和 retirement 中避免灰色地带。

## 6. 注册表不只是给安全团队用的

一个好的 `agent registry` 不只服务于安全或治理。

它同样服务于：

- 平台团队；
- 产品团队；
- SRE / 运营团队；
- 审计 / 合规团队；
- 事件响应人员。

对平台团队来说，它展示哪些模式正在真实扩张。
对运营团队来说，它告诉你半夜该叫谁。
对事件响应来说，它告诉你到底哪些智能体可能参与了某个事件。

## 7. 蔓延往往是从“小例外”开始的

现实里，动物园几乎从来不是正式策略。

它通常是从一些小放松开始：

- “这只是个内部 helper”；
- “这个 agent 是临时的”；
- “registry 先不加，之后再补”；
- “这里做 approval 太重了”；
- “telemetry 以后再接”。

几个月后，正是这些例外，构成了整个智能体群体里最不透明的部分。

所以更稳妥的默认规则应该很简单：

- 如果一个实体可以代表组织行动、读取敏感上下文或调用工具，它至少应该进入 inventory；
- 如果它进入生产轮廓，就必须进入 registry。

## 8. 注册表如何连接可观测性

前一章已经说明，inventory coverage 本身就是证据层的一部分。

注册表会把这层关系再拉紧一步：

- traces 可以挂上 registry metadata；
- detections 可以按 lifecycle state 来做；
- incidents 可以按 owner、risk tier 和 approval mode 过滤；
- release evidence 不只看 traces，也可以看 registry record 的状态与 verifier-evidence linkage。

也就是说，注册表会把可观测性从“原始事件流”提升成受治理的运行地图。

但它不应该和 provenance 混在一起。Provenance 保留的是哪一组 approved artifacts 与哪一个 version 支撑了行为；registry 保留的是，这条 path 属于哪一个命名的生产实体、负责人和生命周期状态。

这也是本章和上一章之间最清晰的边界。可观测性保存 evidence；registry 则把这些 evidence 绑定到整个智能体群体里的命名实体、负责人、生命周期状态与问责路径。

这同样也是它和 provenance chapter 的边界。Provenance 回答系统运行在什么 governed version 或 approved bundle 之下；registry 回答的是，哪一个生产实体拥有这条 path，以及现在该由谁负责。

## 8.1. 没有持续校验的注册表会变得整洁，但不再准确

这里不应该高估 registry 本身。Registry 的存在，并不能自动证明控制层真的在工作。

如果 registry：

- 不和真实 telemetry coverage 对账；
- 不和活跃 principals 对账；
- 不和 active capabilities 对账；
- 不和 rollout 或 assurance 依赖的 verifier evidence 对账；
- 不参与 retirement hygiene，

那它很快就会变成一幅整洁、但部分失真的智能体群体图景。

所以，更成熟的理解方式是：registry 不应只是静态目录，而应该是持续校验的控制面。

## 9. 注册表如何连接 approvals 和 policies

注册表不应该去复制 policy bundle 或 approval contract。

它的职责是：

- 标明某个 agent 关联的是哪套 policy bundle 和 approval mode；
- 标明它是否有权使用某一组 capabilities；
- 标明哪些 approved MCP servers、discovery sources 与 auth modes 属于这个 agent 的 governed capability surface；
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
- 哪些 agents 可以 re-initialize stateful capability sessions，以及对应的 approval mode 是什么；
- stuck paused runs 由谁负责；
- aging background runs 由谁负责；
- capability-session expiry drift 与 emergency freeze actions 由谁负责；
- 它们的 approval 与 capability payload 应该遵循哪个 contract version；
- 哪个 verifier 或 grading contract 被信任为它们 high-risk eval evidence 的依据；
- 智能体群体里是否还有地方在引用已废弃的 verifier contracts；
- approved registry 之外是否已经出现了 shadow MCP endpoints。

否则，整个智能体群体表面上看起来像是 governed 的，实际却仍然隐藏着运行层面的模糊地带。

所以 registry 与其说是 release lineage 层，不如说是 operational answerability 层。它是一张智能体群体级的 ownership map，确保决策、事件与漂移始终挂在正确的实体上。

而这种模糊通常最先在 incident response 里造成伤害。团队可能已经有 telemetry、policies 和 approvals，却仍然会卡在一个最基本的智能体群体问题上：此刻到底是哪一个 production entity 应该为这条 path 负责？

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
  mcp_surface:
    approved_servers:
      - support-registry/ticketing-mcp
    discovery_sources:
      - platform_registry
    auth_mode: managed_oauth
  policy_bundle: policy-v4
  approval_mode: required_for_high_risk
  runtime_controls:
    approval_pause_allowed: true
    background_mode_allowed: true
    capability_session_mode: stateful
    reinit_policy: approval_bound
    paused_run_owner: support-ops
    capability_session_owner: support-ops
    contract_version: capability-contract-v3
  observability:
    trace_enabled: true
    inventory_covered: true
    verifier_evidence_linked: true
  verifier_contract: verifier-v2
  deprecated_verifier_contracts:
    - verifier-v1
  artifacts:
    bundle_id: bundle-2026-04-07-a
  retirement_plan: retire-support-v1
```

这条记录已经足以把这个智能体与负责人、控制约束、生命周期，以及 verifier-aware evidence expectations 连接起来。

放到整个智能体群体的尺度上看，它还能帮助回答一个团队很容易漏掉的问题：哪些 verifier contracts 仍在使用，哪些已经废弃，以及哪些 agents 还依赖旧版本。

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
    has_capability_session_owner: bool


def registry_ready(state: AgentRegistryState) -> bool:
    return (
        state.has_owner
        and state.has_lifecycle_state
        and state.has_policy_linkage
        and state.has_observability
        and state.has_runtime_control_linkage
        and state.has_capability_session_owner
    )
```

这里的逻辑很直接：一个没有 owner、没有 lifecycle state、没有 observability linkage 的 agent，不应该被视为可进入生产的实体。

## 12. 最常见的 failure modes

- 一些 agents 已经在生产环境里运行，却不在 inventory 中；
- inventory 虽然存在，但 lifecycle states 没有持续维护；
- registry 并不知道 principals 和 approvals 的实际情况；
- 已废弃的 agents 仍保留着 tool paths 的访问权；
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

如果这些条件大多不成立，那团队也许已经有一些零散的可见性碎片，但还没有真正建立起智能体治理。

这时的 registry 仍然更像 loose catalog。成熟的 registry 更像一个 accountability layer，会持续对账 production entities、control ownership 与 lifecycle truth。

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

- [第 23 章：Retirement、Replacement 与 End-of-Life Discipline](chapter-23.zh.md)
- [第 24 章：智能体失配与内部人风险](chapter-24.zh.md)
- [第 26 章：AI-Native Observability、Inventory Coverage 与 Detection-Ready Telemetry](chapter-26.zh.md)

[^ms-inventory]: Microsoft Learn, [Complete production infrastructure inventory](https://learn.microsoft.com/en-us/security/zero-trust/sfi/complete-production-infrastructure-inventory)
[^ms-agentic-risk]: Microsoft Learn, [Reduce autonomous agentic AI risk](https://learn.microsoft.com/en-us/security/zero-trust/sfi/manage-agentic-risk)
