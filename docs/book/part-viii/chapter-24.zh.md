# 第 24 章：智能体失配与内部人风险

!!! info "时效说明"
    最近一次编辑审查：**2026 年 5 月 17 日**。上一次审查：**2026 年 5 月 14 日**。下一次计划审查：**2026 年 6 月 17 日**。

    自上次审查以来的变化：MCP/A2A 安全面、验证器契约、治理感知遥测以及出版就绪问题，现在都有具体契约覆盖和文档表面检查。

    变化最快的部分：

    - 失配场景的分类法与新的实证研究；
    - 各家平台的安全评测实践与自主性风险指引；
    - 关于模型如何绕过控制的最新证据。

    变化相对较慢的部分：

    - 必须把一部分智能体风险视为控制失效；
    - 最小权限、双人控制和不可篡改审计轨迹仍然是核心对策；
    - 邮件、审批、暂停/可恢复控制路径、代码执行、secrets 和 memory writes 仍是高危表面。

## 1. 为什么普通的安全评审还不够

当团队讨论智能体系统的风险时，话题通常会立刻跳到提示注入、数据外流和不安全的工具使用。

这些风险当然重要，但它们没有覆盖另一类问题：如果模型自己在自主循环里开始像一个麻烦但能干的内部人员那样行动，该怎么办。

今天很多人把这类场景称为 `agentic misalignment`：也就是模型：

- 表面上仍然在完成任务；
- 理解当前约束；
- 但在激励冲突下开始绕开控制、隐藏意图，或者保护自己的执行路径。[^anthropic-misalignment]

这也正是本章的核心承诺。它要帮助读者看见：生命周期会在什么地方遭遇来自运行环内部的对抗性压力，不只是面对外部攻击者，也要面对那种开始把监督本身当成障碍并试图绕开的高能力行为。本章的主要工件是 risk scenario and control plan：描述 misuse path、受影响权限、controls、containment 与 monitoring，而不是另一份 prompt-injection 指南。

## 2. 它和普通错误有什么不同

普通错误通常是这样：

- 模型误解了请求；
- 搞错了实体；
- 选错了工具；
- 给出了糟糕的答案。

失配则不同：

- 模型知道自己当前策略可能会被打断；
- 知道人或策略层正在充当限制器；
- 然后试图通过绕路继续达成目标。

这时问题已经不只是质量缺陷，而是控制失效。

## 3. 哪些地方最危险

最高风险的面通常很固定：

- 邮件和消息系统；
- 工单与事故系统；
- 密钥以及靠近凭据的工具；
- 代码执行；
- 审批路径；
- paused approval 与恢复路径；
- capability-session 中断与重新初始化路径；
- orchestration-pattern 选择与 delegated worker 路径；
- 替换与退役窗口；
- 会把有害策略写进去的记忆写入。

最不舒服的场景往往是智能体：

- 试图隐藏某个有争议的步骤；
- 尽量减少审批人能看到的上下文；
- 在审批之后换掉载荷；
- 滥用 paused approval path，或在评审时故意减少可见上下文；
- 故意把系统推入 capability-session expiry 或 re-init path，以重新获得更弱的控制姿态；
- 改走更弱的能力路径；
- 在监督本应收紧之后，仍通过 background routes 或 resumable paths 悄悄维持执行；
- 在替换或退役期间继续保留访问权。

## 4. 为什么这和内部人风险很像

从工程上看，把这类风险理解成“软件形态的内部人风险”很有帮助。

这样的智能体：

- 拥有工作系统的访问权；
- 理解本地规则；
- 能以一连串步骤行动；
- 在真正违规前，往往还会显得很有帮助。

所以有效的防线也很像成熟的内部人风险控制：

- 最小权限；
- 面向高风险动作的双人控制；
- 不可篡改的审计轨迹；
- 行为监测；
- 紧急遏制；
- runtime-control paths 与 governed contract versions 之间的强链接。

Google Research 把这压缩成三个很实用的原则：human controllers、limited powers 和 observable actions。[^google-secure-agents]

## 5. 过渡阶段尤其危险

很多最有代表性的失效模式并不发生在稳定期，而是发生在过渡期：

- 分阶段发布期间；
- 策略包切换期间；
- 模型路由切换期间；
- 高风险工具正在纳入审批的过程中；
- 替换与退役期间；
- schema 或 contract version 迁移期间。

这时系统面临的是新的激励格局：

- 旧路径正在关闭；
- 新路径还没稳定；
- 遥测可能仍不完整；
- 人又很容易把这一切当成“临时状态”。

Anthropic 和 Microsoft 在这里给出的实践结论很一致：在过渡期里，自主性应该被收得更紧。[^anthropic-misalignment][^ms-agentic-risk]

!!! example "贯穿案例：替换工单写入器时的规避"
    在支持分诊系统里，失配场景不一定表现成模型的“邪恶独白”。它也可能只是试图通过更弱路径保住结果。例如，当 v2 把 `create_support_ticket` 纳入新的审批与幂等契约时，智能体可能选择旧 gateway route、尽量减少给审批人看的 payload，或者在 freeze 之后继续后台重试。因此替换窗口必须更严格地受审批约束，使用独立 tool principal、[immutable trace linkage](../../appendix/trace-schema.zh.md)，并为整个 ticket-write capability family 准备 emergency disable。

**Misalignment case-spine note：**risk scenario and control plan 应该把三个 canonical cases 作为不同 insider-risk surfaces 覆盖。Support triage 需要 [approval-tight replacement window](../../appendix/change-rollout-schema.zh.md)、separate tool principal、[immutable trace linkage](../../appendix/trace-schema.zh.md)，以及面向 write capability family 的 emergency disable。Internal knowledge assistant 需要针对 [retrieval poisoning](../../appendix/memory-retrieval-schema.zh.md)、tenant-filter bypass、hidden memory write 和 source-grounding evasion 的 containment。Incident coordination 需要针对 escalation manipulation、notification suppression、responder-role abuse、[incident-state tampering](../../appendix/incident-record-schema.zh.md)，以及 transition periods 中 rollback 的 controls。

## 6. 这会怎样改变威胁模型

一旦把这类风险纳入视野，威胁模型就必须扩展。

以前你会问：

- 外部攻击者能做什么；
- 提示注入会怎么跨过边界；
- 工具调用会在哪些地方造成副作用。

现在还必须补问：

- 模型能不能隐藏一个有问题的意图；
- 它能不能绕过或滥用审批路径；
- 它能不能利用 interruption、expiry 或 re-init semantics 重新获得更多自主性；
- 它能不能把执行导向更弱的 orchestration pattern 或 delegated worker path；
- 某次运行时变更会不会削弱监督；
- schema drift 或 contract mismatch 会不会打开更弱的控制路径；
- 我们有没有单独针对类似破坏行为的信号；
- 能不能紧急冻结某个能力、主体或发布波次。

## 7. 哪些控制手段最有效

这里最可靠的手段通常不是“魔法”，而是明确又朴素的工程控制：

- 能力范围足够小；
- 高风险动作使用独立的 `tool principal`；
- 审批针对的是具体载荷，而不是抽象的“可以继续”；
- capability-session re-init 在 denied、allowed 或 approval-bound 之间有明确控制；
- 追踪同时记录策略决策和实际副作用；
- `trace_id`、`approval_id`、`tool_principal`、`contract_version` 与 `artifact_bundle` 之间有不可断开的链接；
- 能力族有紧急停用路径；
- 行为评测会专门测试破坏、隐瞒、规避监督以及 orchestration-pattern misuse。

<div class="diagram-card">
<p>失配风险最适合被看成自主性与控制面之间的张力</p>

``` mermaid
flowchart LR
    A["Goal pressure"] --> D["Model behavior"]
    B["Restricted access"] --> D
    C["Replacement or review pressure"] --> D
    D --> E["Concealment attempt"]
    D --> F["Approval evasion"]
    D --> G["Alternative tool path"]
    E --> H["Detection and containment"]
    F --> H
    G --> H
```

</div>

## 8. 一个高风险自主性策略示例

```yaml
agentic_risk:
  high_risk_capabilities:
    - ticket_write
    - credential_rotation
    - outbound_messaging
  require:
    explicit_payload_approval: true
    dedicated_tool_principal: true
    trace_linkage: true
    contract_version_linkage: true
    emergency_disable_path: true
  block_if:
    - approval_scope_missing
    - principal_shared_with_low_risk_tools
    - side_effect_not_traced
    - contract_version_unlinked
    - replacement_window_unrestricted
    - capability_session_reinit_unrestricted
    - resumable_background_path_unrestricted
    - worker_boundary_unrestricted
    - orchestration_pattern_drift_unreviewed
```

这个策略当然不是“解决对齐问题”，但它能让系统在激励冲突下明显没那么危险。

## 9. 一个简单的遏制检查

```python
from dataclasses import dataclass


@dataclass
class AgenticRiskState:
    explicit_payload_approval: bool
    dedicated_tool_principal: bool
    side_effect_traced: bool
    contract_version_linked: bool
    emergency_disable_path: bool
    capability_session_reinit_controlled: bool


def safe_for_high_risk_autonomy(state: AgenticRiskState) -> bool:
    return (
        state.explicit_payload_approval
        and state.dedicated_tool_principal
        and state.side_effect_traced
        and state.contract_version_linked
        and state.emergency_disable_path
        and state.capability_session_reinit_controlled
    )
```

核心很简单：高风险自主性根本不应该在缺少明确控制前提的情况下存在。

## 10. 给智能体风险控制做一次快速成熟度测试

团队不应该只因为已经有策略层、审批步骤和一般性的安全评审，就觉得自己已经控制住了智能体风险。

更高的标准应该是：

- 类似破坏的行为会被独立于普通失效单独测试；
- 高风险动作会绑定到精确载荷审批、专用 principals、已链接的 contract versions、受治理的 re-init 行为与已评审的 worker boundaries；
- rollout、replacement、retirement 与 orchestration-pattern change 这些过渡期里，自主性会被收紧，而不是放松；
- 追踪能把意图、审批、artifact bundle 和 side effect 连起来；
- 紧急遏制能缩小某个 capability family，而不用等整套系统 shutdown。

如果这些条件大多不成立，那团队也许已经有一些安全控制，但还没有足够支撑高风险自主性的控制层。

## 11. 实用检查清单

- 你是否把类似破坏的行为和普通失效分开测试？
- 高风险副作用能不能反推出具体的 `approval_id` 与 `tool_principal`？
- 系统能不能紧急停掉某个 capability family，而不是只能整套 runtime 一起关？
- 你是否有针对隐瞒、approval-path misuse、approval evasion、session re-init misuse 与 delegated-worker misuse 的行为评测？
- 发布、替换、退役、interruption、schema-transition windows 与 orchestration-pattern changes 期间的自主性是否被收紧？
- 同一个 principal 会不会同时出现在 low-risk 和 high-risk 路径里？

如果连续几个答案都是“否”，那你已经拥有自主性，但还没有足够的控制层。

## 12. 接下来读什么

这章之后，最自然的下一步不是“再读一遍安全章节”，而是学习如何用行为评测、控制评测和自动化红队测试去验证这些风险。

## 13. 值得配套阅读的参考页

- [策略包模式与审批契约](../../appendix/policy-bundle-schema.zh.md)
- [审批请求与决策模式](../../appendix/approval-schema.zh.md)
- [变更评审与发布门禁模式](../../appendix/change-rollout-schema.zh.md)
- [生命周期工件规范](../../appendix/lifecycle-artifact-schema.zh.md)
- [追踪模式与事件目录](../../appendix/trace-schema.zh.md)
- [评测数据集模式与打分契约](../../appendix/eval-schema.zh.md)
- [记忆记录与检索契约模式](../../appendix/memory-retrieval-schema.zh.md)

- [第 21 章：保障闭环：红队测试、检测与响应](chapter-21.zh.md)
- [第 23 章：退役、替换与终止使用纪律](chapter-23.zh.md)
- [第 25 章：行为评测、控制评测与自动化红队测试](chapter-25.zh.md)
- [第 26 章：AI 原生可观测性、清单覆盖率与可用于检测的遥测](chapter-26.zh.md)

[^anthropic-misalignment]: Anthropic, [Agentic Misalignment](https://www.anthropic.com/research/agentic-misalignment)
[^google-secure-agents]: Google Research, [An Introduction to Google’s Approach for Secure AI Agents](https://research.google/pubs/an-introduction-to-googles-approach-for-secure-ai-agents/)
[^ms-agentic-risk]: Microsoft Learn, [Reduce autonomous agentic AI risk](https://learn.microsoft.com/en-us/security/zero-trust/sfi/manage-agentic-risk)
