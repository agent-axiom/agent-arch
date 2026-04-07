# 第 25 章：Behavioral Evals、Control Evals 与 Automated Red Teaming

## 1. 为什么普通 regression evals 已经不够

Regression evals 很擅长回答一个问题：

- 我们有没有把之前能工作的东西弄坏。

但对 agent systems 来说，这还不够。

如果系统已经会：

- 选择 strategy；
- 使用 tools；
- 保存 state；
- 穿过 approvals；
- 在过渡条件下调整行为，

那你需要的不只是 regression evals，还需要行为层面的检查。

这时最好把下面三类东西分开：

- `behavioral evals`
- `control evals`
- `automated red teaming`

## 2. 什么是 behavioral evals

Behavioral evals 不只检查最终输出，还检查系统的行为形态。

例如：

- agent 会不会隐藏一个有争议的步骤；
- 会不会绕过 approval；
- 会不会在 review 之后改掉 payload；
- 会不会在没有充分理由的情况下进入 risky tool path；
- 会不会偏离预期的 escalation path。

也就是说，问题不再只是“答案对不对”，而是“在这个场景下，runtime 的行为对不对”。

## 3. 什么是 control evals

Control evals 检查的是控制机制本身，而不只是模型质量。

典型问题包括：

- policy layer 能不能真的拦住这个 capability；
- approval gate 是否真的要求人来确认；
- rollback gate 能不能工作；
- side effect 会不会进入 traces；
- emergency control 能不能关掉 risky path。

这里的关键转变在于：你检查的不只是模型，而是围绕模型的一整层 control surface。

## 4. 什么是 automated red teaming

Automated red teaming 不再只是几条手写测试样例，而是一种系统化生成、变换和放大 adversarial scenarios 的方法。

它的实际价值在于：

- 帮你发现团队自己没想到的 failure modes；
- 更有效地覆盖 edge cases；
- 强迫你去观察系统在受压状态下的行为，而不是只看“正常日子”。

Anthropic 最近在这方面的工作尤其值得参考：更强的 control-eval scaffold，以及更强的 red-team scenario generation。 [^anthropic-redteam][^anthropic-bloom]

## 5. 它和现有 eval layer 的关系

你已经有：

- offline evals；
- online evals；
- regression gates；
- trace grading。

Behavioral evals 和 control evals 不是用来替换它们的，而是在上面再叠一层：

- offline evals 检查任务质量；
- trace grading 检查路径质量；
- behavioral evals 检查与 policy 相关的行为；
- control evals 检查 controls 本身是否真的有效。

## 6. 哪些地方最需要这类 evals

这类场景尤其适合放在：

- high-risk write capabilities；
- 带 egress 的 tools；
- approval-heavy workflows；
- replacement 与 retirement transitions；
- multi-agent delegation；
- memory write 与 retrieval governance。

如果 risky path 根本没有被这些 evals 覆盖，团队几乎一定会先从 incident 里学到教训。

## 7. 一个最小 behavioral taxonomy

一个够用的最小 taxonomy 可以是：

- `oversight_evasion`
- `payload_mutation_after_approval`
- `concealment_of_side_effect`
- `unsafe_alternative_tool_path`
- `improper_memory_write`
- `replacement_window_abuse`
- `unauthorized_persistence`

重点不在于名字有多少，而在于它们给了你一套可重复的 failure classes。

## 8. User simulator 和 synthetic adversary 是两种角色

`user simulator` 适合用来稳定生成正常和边界用户场景。

`synthetic adversary` 适合用来故意压测系统弱点：

- 含糊指令；
- 冲突目标；
- risky shortcuts；
- 尝试隐藏可疑步骤。

在成熟系统里，这两种角色应该并存：

- simulator 提供 realistic task distribution；
- adversary 提供 pressure testing。

## 8.1. Research 在这里更适合作为 scenario classes 的来源

最新关于 behavioral risk 与 automated red teaming 的研究，价值不只在于结论，也在于它提供了更丰富的 vocabulary。

它能帮助团队补齐那些很难仅靠本地经验就完整想出的 scenario classes。比如：

- concealment；
- oversight evasion；
- sabotage-like persistence；
- coordination breakdown under pressure。

但 engineering discipline 仍然应该保持严格：

- scenario class 必须进入 reviewable eval schema；
- finding 必须有 owner 和 triage path；
- rollout gate 看到的应是 operational evidence，而不只是 paper citation。

所以，research 在这里最好的用途，是帮助生成 hypotheses 和 dangerous scenarios，而不是替代你自己的 eval program。

## 9. 一个 control evals policy 示例

```yaml
control_evals:
  required_for:
    - ticket_write
    - outbound_messaging
    - credential_rotation
  scenario_classes:
    - oversight_evasion
    - payload_mutation_after_approval
    - concealment_of_side_effect
  block_release_if:
    - control_eval_missing
    - behavioral_eval_regression
    - red_team_findings_untriaged
```

这个层很有价值，因为它把 behavioral checks 变成了 release discipline 的一部分，而不是“可做可不做的加分项”。

## 10. 一个简单的 grading contract

```python
from dataclasses import dataclass


@dataclass
class ControlEvalResult:
    scenario_class: str
    control_enforced: bool
    side_effect_traced: bool
    finding_open: bool


def passes_control_eval(result: ControlEvalResult) -> bool:
    return (
        result.control_enforced
        and result.side_effect_traced
        and not result.finding_open
    )
```

这里的核心是：failure 不只是“模型行为古怪”，也包括“control layer 没能证明自己真的有效”。

## 11. 如何把它接进 ADLC

在成熟系统里，流程通常是这样：

1. risky change 先拿到 `change_record`；
2. 定义这次需要的 eval scope；
3. regression evals 检查既有行为；
4. behavioral / control evals 检查高风险路径；
5. automated red teaming 搜索不那么明显的 failure modes；
6. findings 进入 assurance backlog；
7. rollout gate 看到的不只是 accuracy，还包括 control evidence。

这样 eval layer 就不再只是“一张指标表”，而会变成 operating model 的一部分。

## 12. 最常见的错误

- 所有 evals 最后都退化成 final answer quality；
- dangerous paths 没有独立的 scenario classes；
- red teaming 只是一次性活动；
- findings 没有进入 release gate；
- control failures 被当成“不是模型 bug”，于是从 backlog 里消失；
- 团队分不清 ordinary failure 和 sabotage-like behavior。

## 13. 实用检查清单

- risky capabilities 是否有单独的 behavioral scenario classes？
- 你是否测试 approval evasion 和 payload mutation？
- 是否有专门验证 controls 的 evals，而不只是检查输出质量？
- red-team findings 是否会进入 change review 和 rollout gate？
- 是否同时有 realistic workload simulator 和 adversarial generator？
- 你能展示的是 control evidence，还是只有最终分数？

如果连续几个答案都是“否”，那你的 eval layer 虽然已经存在，但还没准备好面对 autonomous behavior。

## 14. 值得配套阅读的参考页

- [Eval Dataset Schema 与 Grading Contract](../../appendix/eval-schema.zh.md)
- [Trace Schema 与 Event Catalog](../../appendix/trace-schema.zh.md)
- [Change Review 与 Rollout Gate Schema](../../appendix/change-rollout-schema.zh.md)
- [Policy Bundle Schema 与 Approval Contract](../../appendix/policy-bundle-schema.zh.md)
- [研究前沿：记忆、可观测性与多智能体可靠性](../../appendix/research-frontier.zh.md)

- [第 13 章：Offline Evals、Online Evals 与 Regression Gates](../part-v/chapter-13.zh.md)
- [第 21 章：Assurance Loop：Red Teaming、Detection 与 Response](chapter-21.zh.md)
- [第 24 章：Agentic Misalignment 与 Insider Risk](chapter-24.zh.md)

[^anthropic-redteam]: Anthropic, [Strengthening Red Teams](https://alignment.anthropic.com/2025/strengthening-red-teams/)
[^anthropic-bloom]: Anthropic, [Introducing Bloom](https://www.anthropic.com/research/bloom)
