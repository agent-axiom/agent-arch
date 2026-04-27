# 第 27 章：智能体清单、注册表与蔓延治理

!!! info "时效说明"
    本章内容截至 2026 年 4 月 11 日。

    变化最快的部分：

    - 面向智能体清单发现、注册表同步与治理自动化的平台能力；
    - 各家平台对智能体、助手与类智能体实体的分类方法；
    - 面向大规模智能体群体的漂移检测与策略执行实践。

    变化相对较慢的部分：

    - 必须区分清单与注册表；
    - 每个生产级智能体都需要负责人、生命周期状态、能力记录与运行时控制责任归属；
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
- 哪些仍然挂着暂停中的审批、后台路由、已废弃的契约路径或陈旧的校验器契约。

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

Microsoft 直接把不完整的清单和智能体蔓延，与盲区、执行不一致和发现滞后联系在一起。 [^ms-inventory][^ms-agentic-risk]

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
- 暂停运行、后台运行与能力会话的责任归属
- 可观测性状态
- 校验器或评测证据状态
- 生效中与已废弃的校验器契约关联
- 制品包关联
- 退役计划关联

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

- 在 `production` 前限制自主性；
- 追踪已废弃的智能体；
- 看出哪些智能体还不该拥有完整的出口访问权或完整的审批路径；
- 在替换和退役过程中避免灰色地带。

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

- “这只是个内部助手”；
- “这个智能体是临时的”；
- “注册表先不加，之后再补”；
- “这里做审批太重了”；
- “遥测以后再接”。

几个月后，正是这些例外，构成了整个智能体群体里最不透明的部分。

所以更稳妥的默认规则应该很简单：

- 如果一个实体可以代表组织行动、读取敏感上下文或调用工具，它至少应该进入清单；
- 如果它进入生产轮廓，就必须进入注册表。

## 8. 注册表如何连接可观测性

前一章已经说明，清单覆盖率本身就是证据层的一部分。

注册表会把这层关系再拉紧一步：

- 追踪数据可以挂上注册表元数据；
- 检测可以按生命周期状态来做；
- 事件可以按负责人、风险层级和审批模式过滤；
- 发布证据不只看追踪数据，也可以看注册表记录的状态与校验器证据关联。

也就是说，注册表会把可观测性从“原始事件流”提升成受治理的运行地图。

但它不应该和来源链混在一起。来源链保留的是哪一组已批准制品与哪一个版本支撑了行为；注册表保留的是，这条路径属于哪一个命名的生产实体、负责人和生命周期状态。

这也是本章和上一章之间最清晰的边界。可观测性保存证据；注册表则把这些证据绑定到整个智能体群体里的命名实体、负责人、生命周期状态与问责路径。

这同样也是它和来源链章节的边界。来源链回答系统运行在什么受治理版本或已批准包之下；注册表回答的是，哪一个生产实体拥有这条路径，以及现在该由谁负责。

## 8.1. 没有持续校验的注册表会变得整洁，但不再准确

这里不应该高估注册表本身。注册表的存在，并不能自动证明控制层真的在工作。

如果注册表：

- 不和真实遥测覆盖率对账；
- 不和活跃主体对账；
- 不和活跃能力对账；
- 不和发布或保障流程依赖的校验器证据对账；
- 不参与退役清理，

那它很快就会变成一幅整洁、但部分失真的智能体群体图景。

所以，更成熟的理解方式是：注册表不应只是静态目录，而应该是持续校验的控制面。

## 9. 注册表如何连接审批和策略

注册表不应该去复制策略包或审批契约。

它的职责是：

- 标明某个智能体关联的是哪套策略包和审批模式；
- 标明它是否有权使用某一组能力；
- 标明哪些已批准的 MCP 服务器、发现来源与认证模式属于这个智能体受治理的能力面；
- 标明它当前所处的生命周期状态。

如果没有这层连接，就很容易出现这种状态：

- 策略变了；
- 审批流程变了；
- 追踪能力变强了；
- 但没人知道到底哪些智能体本来就该用这些控制。

当审批和长时间运行的工作都变成显式运行路径之后，这一点会更加重要。

这时注册表还应该帮助回答：

- 哪些智能体被允许因审批而暂停运行；
- 哪些智能体可以继续使用后台模式；
- 哪些智能体可以重新初始化有状态能力会话，以及对应的审批模式是什么；
- 卡住的暂停运行由谁负责；
- 老化的后台运行由谁负责；
- 能力会话过期漂移与紧急冻结动作由谁负责；
- 它们的审批与能力载荷应该遵循哪个契约版本；
- 哪个校验器或评分契约被信任为它们高风险评测证据的依据；
- 智能体群体里是否还有地方在引用已废弃的校验器契约；
- 已批准注册表之外是否已经出现了影子 MCP 端点。

否则，整个智能体群体表面上看起来像是受治理的，实际却仍然隐藏着运行层面的模糊地带。

所以注册表与其说是发布谱系层，不如说是运行问责层。它是一张智能体群体级的责任地图，确保决策、事件与漂移始终挂在正确的实体上。

而这种模糊通常最先在事件响应里造成伤害。团队可能已经有遥测、策略和审批，却仍然会卡在一个最基本的智能体群体问题上：此刻到底是哪一个生产实体应该为这条路径负责？

## 10. 一个最小智能体注册表记录示例

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

这条记录已经足以把这个智能体与负责人、控制约束、生命周期，以及校验器感知的证据预期连接起来。

放到整个智能体群体的尺度上看，它还能帮助回答一个团队很容易漏掉的问题：哪些校验器契约仍在使用，哪些已经废弃，以及哪些智能体还依赖旧版本。

## 11. 一个简单的注册表健康检查

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

这里的逻辑很直接：一个没有负责人、没有生命周期状态、没有可观测性关联的智能体，不应该被视为可进入生产的实体。

## 12. 最常见的失效模式

- 一些智能体已经在生产环境里运行，却不在清单中；
- 清单虽然存在，但生命周期状态没有持续维护；
- 注册表并不知道主体和审批的实际情况；
- 已废弃的智能体仍保留着工具路径的访问权；
- 注册表记录无法说明谁负责暂停中的审批或老化的后台运行；
- 契约版本已经漂移，但注册表仍指向过时的控制假设；
- 多个注册表之间发生漂移；
- 平台团队认识一批智能体，而安全团队认识另一批。

## 13. 给智能体治理做一次快速成熟度测试

团队不应该只因为已经有一张注册表电子表格和一个大概的已部署智能体数量，就觉得自己已经控制住了整个智能体群体。

更高的标准应该是：

- 清单和注册表被当成不同的控制面；
- 每个生产级智能体都有负责人、生命周期状态和策略关联；
- 遥测覆盖率能持续和注册表对账；
- 暂停中的审批、后台运行责任归属与契约版本也是注册表控制面的一部分；
- 已废弃和失去负责人的智能体能在变成盲区之前被找到；
- 治理能区分已发现实体和已批准的生产级智能体。

如果这些条件大多不成立，那团队也许已经有一些零散的可见性碎片，但还没有真正建立起智能体治理。

这时的注册表仍然更像松散目录。成熟的注册表更像一个问责层，会持续对账生产实体、控制责任归属与生命周期真相。

## 14. 实用检查清单

- 你能快速说出处于活跃、已废弃和已退役状态的智能体数量吗？
- 每个生产级智能体都有负责人吗？
- 注册表记录是否和策略包、审批模式、运行时控制责任归属、`bundle_id` 关联？
- 清单能不能显示哪些智能体没有发出遥测？
- 你能不能快速找出失去负责人或已经废弃、但主体还活着的智能体？
- 你有没有明确区分“被发现”与“被批准进入生产”？

如果连续几个答案都是“否”，那说明你已经有一整套智能体群体，但还没有真正把智能体治理建立起来。

## 15. 值得配套阅读的参考页

- [Lifecycle Artifact Schema](../../appendix/lifecycle-artifact-schema.zh.md)
- [Policy Bundle Schema 与 Approval Contract](../../appendix/policy-bundle-schema.zh.md)
- [Approval Request 与 Decision Schema](../../appendix/approval-schema.zh.md)
- [Trace Schema 与 Event Catalog](../../appendix/trace-schema.zh.md)
- [研究前沿：记忆、可观测性与多智能体可靠性](../../appendix/research-frontier.zh.md)

- [第 23 章：退役、替换与生命周期终止纪律](chapter-23.zh.md)
- [第 24 章：智能体失配与内部人风险](chapter-24.zh.md)
- [第 26 章：AI-Native Observability、Inventory Coverage 与 Detection-Ready Telemetry](chapter-26.zh.md)

[^ms-inventory]: Microsoft Learn, [Complete production infrastructure inventory](https://learn.microsoft.com/en-us/security/zero-trust/sfi/complete-production-infrastructure-inventory)
[^ms-agentic-risk]: Microsoft Learn, [Reduce autonomous agentic AI risk](https://learn.microsoft.com/en-us/security/zero-trust/sfi/manage-agentic-risk)
