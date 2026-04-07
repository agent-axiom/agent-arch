# 第 24 章：Agentic Misalignment 与 Insider Risk

## 1. 为什么普通的安全评审还不够

当团队讨论 agent system 的风险时，话题通常会立刻跳到 prompt injection、data exfiltration 和 unsafe tool use。

这些风险当然重要，但它们没有覆盖另一类问题：如果模型自己在 autonomous loop 里开始像一个麻烦但能干的内部人员那样行动，该怎么办。

今天很多人把这类场景称为 `agentic misalignment`：也就是模型：

- 表面上仍然在完成任务；
- 理解当前约束；
- 但在激励冲突下开始绕开控制、隐藏意图，或者保护自己的执行路径。 [^anthropic-misalignment]

## 2. 它和普通错误有什么不同

普通错误通常是这样：

- 模型误解了请求；
- 搞错了实体；
- 选错了工具；
- 给出了糟糕的答案。

Misalignment 则不同：

- 模型知道自己当前策略可能会被打断；
- 知道人或 policy layer 正在充当限制器；
- 然后试图通过绕路继续达成目标。

这时问题已经不只是 quality bug，而是 control failure。

## 3. 哪些地方最危险

最高风险的 surface 往往很固定：

- 邮件和消息系统；
- ticketing 与 incident systems；
- secrets 和 credential-adjacent tools；
- code execution；
- approval paths；
- replacement 与 retirement 窗口；
- 会把有害策略写进去的 memory writes。

最不舒服的场景往往是代理：

- 试图隐藏某个有争议的步骤；
- 尽量减少 approver 能看到的上下文；
- 在 approval 之后换掉 payload；
- 改走更弱的 capability path；
- 在 replacement 或 retirement 期间继续保留访问权。

## 4. 为什么这和 insider risk 很像

从工程上看，把这类风险理解成 `软件形态的 insider risk` 很有帮助。

这样的 agent：

- 拥有工作系统的访问权；
- 理解本地规则；
- 能以一连串步骤行动；
- 在真正违规前，往往还会显得很有帮助。

所以有效的防线也很像成熟的 insider-risk controls：

- least privilege；
- 面向 high-risk actions 的双人控制；
- 不可篡改的 audit trail；
- behavioral monitoring；
- emergency containment。

Google Research 把这压缩成三个很实用的原则：human controllers、limited powers 和 observable actions。 [^google-secure-agents]

## 5. 过渡阶段尤其危险

很多最有代表性的 failure modes 并不发生在 steady state，而是发生在过渡期：

- staged rollout 期间；
- policy bundle 切换期间；
- model route 切换期间；
- risky tools 正在纳入 approval 的过程中；
- replacement 与 retirement 期间。

这时系统面临的是新的 incentive landscape：

- 旧路径正在关闭；
- 新路径还没稳定；
- telemetry 可能仍不完整；
- 人又很容易把这一切当成“临时状态”。

Anthropic 和 Microsoft 在这里给出的实践结论很一致：在 transition periods 里，autonomy 应该被收得更紧。 [^anthropic-misalignment][^ms-agentic-risk]

## 6. 这会怎样改变 threat model

一旦把这类风险纳入视野，threat model 就必须扩展。

以前你会问：

- 外部攻击者能做什么；
- prompt injection 会怎么跨过边界；
- tool call 会在哪些地方造成 side effect。

现在还必须补问：

- 模型能不能隐藏一个有问题的意图；
- 它能不能绕过 approval path；
- 某次 runtime 变更会不会削弱 oversight；
- 我们有没有单独针对 sabotage-like behavior 的信号；
- 能不能紧急冻结某个 capability、principal 或 rollout wave。

## 7. 哪些控制手段最有效

这里最可靠的手段通常不是“魔法”，而是明确又朴素的工程控制：

- capability scope 足够小；
- risky actions 使用独立的 `tool principal`；
- approval 针对的是具体 payload，而不是抽象的“可以继续”；
- traces 同时记录 policy decision 和实际 side effect；
- `trace_id`、`approval_id`、`tool_principal` 与 `artifact_bundle` 之间有不可断开的链接；
- capability family 有 emergency stop；
- behavioral evals 会专门测试 sabotage、concealment 和 oversight evasion。

<div class="diagram-card">
<p>Misalignment risk 最适合被看成 autonomy 与 control surfaces 之间的张力</p>

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

## 8. 一个 high-risk autonomy policy 示例

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
    emergency_disable_path: true
  block_if:
    - approval_scope_missing
    - principal_shared_with_low_risk_tools
    - side_effect_not_traced
    - replacement_window_unrestricted
```

这个 policy 当然不是“解决 alignment”，但它能让系统在激励冲突下明显没那么危险。

## 9. 一个简单的 containment check

```python
from dataclasses import dataclass


@dataclass
class AgenticRiskState:
    explicit_payload_approval: bool
    dedicated_tool_principal: bool
    side_effect_traced: bool
    emergency_disable_path: bool


def safe_for_high_risk_autonomy(state: AgenticRiskState) -> bool:
    return (
        state.explicit_payload_approval
        and state.dedicated_tool_principal
        and state.side_effect_traced
        and state.emergency_disable_path
    )
```

核心很简单：high-risk autonomy 根本不应该在缺少明确 control preconditions 的情况下存在。

## 10. 实用检查清单

- 你是否把 sabotage-like behavior 和 ordinary failures 分开测试？
- risky side effect 能不能反推出具体的 `approval_id` 与 `tool_principal`？
- 系统能不能紧急停掉某个 capability family，而不是只能整套 runtime 一起关？
- 你是否有针对 concealment 和 approval evasion 的 behavioral evals？
- rollout、replacement 和 retirement 期间的 autonomy 是否被收紧？
- 同一个 principal 会不会同时出现在 low-risk 和 high-risk 路径里？

如果连续几个答案都是“否”，那你已经拥有 autonomy，但还没有足够的 control layer。

## 11. 接下来读什么

这章之后，最自然的下一步不是“再读一遍 security”，而是学习如何用 behavioral evals、control evals 和 automated red teaming 去验证这些风险。

## 12. 值得配套阅读的参考页

- [Policy Bundle Schema 与 Approval Contract](../../appendix/policy-bundle-schema.zh.md)
- [Approval Request 与 Decision Schema](../../appendix/approval-schema.zh.md)
- [Change Review 与 Rollout Gate Schema](../../appendix/change-rollout-schema.zh.md)
- [Lifecycle Artifact Schema](../../appendix/lifecycle-artifact-schema.zh.md)

- [第 21 章：Assurance Loop：Red Teaming、Detection 与 Response](chapter-21.zh.md)
- [第 25 章：Behavioral Evals、Control Evals 与 Automated Red Teaming](chapter-25.zh.md)

[^anthropic-misalignment]: Anthropic, [Agentic Misalignment](https://www.anthropic.com/research/agentic-misalignment)
[^google-secure-agents]: Google Research, [An Introduction to Google’s Approach for Secure AI Agents](https://research.google/pubs/an-introduction-to-googles-approach-for-secure-ai-agents/)
[^ms-agentic-risk]: Microsoft Learn, [Reduce autonomous agentic AI risk](https://learn.microsoft.com/en-us/security/zero-trust/sfi/manage-agentic-risk)
