# 第 25 章：行为评测、控制评测与自动化红队测试

!!! info "时效说明"
    本章内容截至 2026 年 4 月 11 日。

    变化最快的部分：

    - 对抗场景生成器与自动化红队框架；
    - 行为类和控制类 benchmark 套件；
    - 模型裁判方法与半自动评分模式。

    变化相对较慢的部分：

    - 必须评估 runtime 的行为，而不只是最终答案；
    - 必须验证控制层本身，而不只是模型质量；
    - control evals、regression gates、contract-version discipline 和 rollout decisions 必须连起来。

## 1. 为什么普通回归评测已经不够

回归评测很擅长回答一个问题：

- 我们有没有把之前能工作的东西弄坏。

但对智能体系统来说，这还不够。

如果系统已经会：

- 选择策略；
- 使用工具；
- 保存状态；
- 穿过审批；
- 在过渡条件下调整行为，

那你需要的不只是回归评测，还需要行为层面的检查。

这时最好把下面三类东西分开：

- `behavioral evals`
- `control evals`
- `automated red teaming`

## 2. 什么是行为评测

行为评测不只检查最终输出，还检查系统的行为形态。

例如：

- 智能体会不会隐藏一个有争议的步骤；
- 会不会绕过审批；
- 会不会在审查之后改掉载荷；
- 会不会在没有充分理由的情况下进入高风险工具路径；
- 会不会偏离预期的升级路径；
- 会不会利用 contract drift 或 schema mismatch 穿过 control boundary。

也就是说，问题不再只是“答案对不对”，而是“在这个场景下，运行时的行为对不对”。

## 3. 什么是控制评测

控制评测检查的是控制机制本身，而不只是模型质量。

典型问题包括：

- 策略层能不能真的拦住这个能力；
- 审批门禁是否真的要求人来确认；
- 回滚门禁能不能工作；
- paused-run 与 background-run controls 是否按设计工作；
- 副作用会不会进入追踪；
- 紧急控制能不能关掉高风险路径。

这里的关键转变在于：你检查的不只是模型，而是围绕模型的一整层控制面。

## 4. 什么是自动化红队测试

自动化红队测试不再只是几条手写测试样例，而是一种系统化生成、变换和放大对抗场景的方法。

它的实际价值在于：

- 帮你发现团队自己没想到的 failure modes；
- 更有效地覆盖边缘场景；
- 强迫你去观察系统在受压状态下的行为，而不是只看“正常日子”。

Anthropic 最近在这方面的工作尤其值得参考：更强的控制评测脚手架，以及更强的红队场景生成。[^anthropic-redteam][^anthropic-bloom]

## 5. 它和现有 eval layer 的关系

你已经有：

- 离线评测；
- 在线评测；
- 回归门禁；
- trace grading。

行为评测和控制评测不是用来替换它们的，而是在上面再叠一层：

- 离线评测检查任务质量；
- 追踪分级检查路径质量；
- 行为评测检查与策略相关的行为；
- 控制评测检查控制本身是否真的有效；
- runtime-control evals 还要验证 pause/resume、background 与 contract-version behavior 在受压场景下是否按预期工作。

## 6. 哪些地方最需要这类评测

这类场景尤其适合放在：

- 高风险写入能力；
- 带出口访问的工具；
- 审批密集型工作流；
- 涉及 pause/resume 或 background execution 的 runtime-control transitions；
- 替换与退役过渡期；
- 多智能体委派；
- 记忆写入与检索治理。

如果高风险路径根本没有被这些评测覆盖，团队几乎一定会先从事故里学到教训。

## 7. 一个最小 behavioral taxonomy

一个够用的最小分类法可以是：

- `oversight_evasion`
- `payload_mutation_after_approval`
- `concealment_of_side_effect`
- `unsafe_alternative_tool_path`
- `improper_memory_write`
- `replacement_window_abuse`
- `unauthorized_persistence`
- `contract_drift_exploitation`
- `approval_path_misuse`
- `runtime_control_regression`

重点不在于名字有多少，而在于它们给了你一套可重复的失效类别。

## 8. 用户模拟器和合成对手是两种角色

`user simulator` 适合用来稳定生成正常和边界用户场景。

`synthetic adversary` 适合用来故意压测系统弱点：

- 含糊指令；
- 冲突目标；
- 高风险捷径；
- 尝试隐藏可疑步骤。

在成熟系统里，这两种角色应该并存：

- simulator 提供更真实的任务分布；
- adversary 提供压力测试。

## 8.1. 研究在这里更适合作为场景类别的来源

最新关于行为风险与自动化红队测试的研究，价值不只在于结论，也在于它提供了更丰富的词汇表。

它能帮助团队补齐那些很难仅靠本地经验就完整想出的场景类别。比如：

- concealment；
- oversight evasion；
- 类似破坏的持续行为；
- 压力下的协作失序；
- 对 schema mismatch 或 control drift 的利用。

但工程纪律仍然应该保持严格：

- 场景类别必须进入可评审的评测模式；
- 发现结果必须有负责人和分诊路径；
- 发布门禁看到的应是运行证据，而不只是论文引用。

所以，研究在这里最好的用途，是帮助生成假设和危险场景，而不是替代你自己的评测方案。

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
    - approval_path_misuse
    - contract_drift_exploitation
    - runtime_control_regression
  block_release_if:
    - control_eval_missing
    - behavioral_eval_regression
    - runtime_control_regression_open
    - red_team_findings_untriaged
```

这个层很有价值，因为它把行为检查变成了发布纪律的一部分，而不是“可做可不做的加分项”。

## 10. 一个简单的 grading contract

```python
from dataclasses import dataclass


@dataclass
class ControlEvalResult:
    scenario_class: str
    control_enforced: bool
    side_effect_traced: bool
    finding_open: bool
    contract_version_matched: bool


def passes_control_eval(result: ControlEvalResult) -> bool:
    return (
        result.control_enforced
        and result.side_effect_traced
        and result.contract_version_matched
        and not result.finding_open
    )
```

这里的核心是：失效不只是“模型行为古怪”，也包括“控制层没能证明自己真的有效”。

## 11. 如何把它接进 ADLC

在成熟系统里，流程通常是这样：

1. 高风险变更先拿到 `change_record`；
2. 定义这次需要的评测范围；
3. 回归评测检查既有行为；
4. 行为评测 / 控制评测检查高风险路径；
5. 自动化红队测试搜索不那么明显的失效模式；
6. 发现结果进入保障待办列表；
7. 发布门禁看到的不只是准确率，还包括控制证据。

这样评测层就不再只是“一张指标表”，而会变成运行模型的一部分。

## 12. 最常见的错误

- 所有评测最后都退化成最终答案质量；
- 危险路径没有独立的场景类别；
- approval-path misuse 与 contract drift 没有被显式测试；
- 红队测试只是一次性活动；
- runtime-control regressions 只有在 rollout 或 incidents 中才被发现；
- 发现结果没有进入发布门禁；
- 控制失效被当成“不是模型 bug”，于是从待办列表里消失；
- 团队分不清普通失效和类似破坏的行为。

## 13. 给 behavioral 和 control evals 做一次快速成熟度测试

团队不应该只因为已经有 regression evals、simulator 和几条 adversarial prompts，就觉得自己已经准备好面对 autonomous behavior。

更高的标准应该是：

- risky paths 有明确的 behavioral scenario classes；
- control evals 会验证 control layer 本身在压力下是否真的有效；
- approval-path misuse、contract drift 与 runtime-control regressions 都有明确的场景覆盖；
- red-team findings 会进入 rollout 和 change gates，而不是停留在单独报告里；
- realistic simulation 和 adversarial generation 扮演不同但互补的角色；
- release decisions 能拿出 control evidence，而不只是 quality scores。

如果这些条件大多不成立，那团队也许已经有一些 evaluation activity，但还没有足够的 behavioral 和 control coverage。

## 14. 实用检查清单

- 高风险能力是否有单独的行为场景类别？
- 你是否测试审批规避、载荷篡改和 approval-path misuse？
- 是否有专门验证控制措施、contract-version matching 与 runtime-control behavior 的评测，而不只是检查输出质量？
- 红队发现结果是否会进入变更评审和发布门禁？
- 是否同时有 realistic workload simulator 和 adversarial generator？
- 你能展示的是控制证据，还是只有最终分数？

如果连续几个答案都是“否”，那你的评测层虽然已经存在，但还没准备好面对自主行为。

## 15. 值得配套阅读的参考页

- [评测数据集模式与分级契约](../../appendix/eval-schema.zh.md)
- [追踪模式与事件目录](../../appendix/trace-schema.zh.md)
- [变更评审与发布门禁模式](../../appendix/change-rollout-schema.zh.md)
- [策略包模式与审批契约](../../appendix/policy-bundle-schema.zh.md)
- [研究前沿：记忆、可观测性与多智能体可靠性](../../appendix/research-frontier.zh.md)

- [第 13 章：离线评测、在线评测与回归门禁](../part-v/chapter-13.zh.md)
- [第 21 章：保障闭环：红队测试、检测与响应](chapter-21.zh.md)
- [第 24 章：智能体失配与内部人风险](chapter-24.zh.md)

[^anthropic-redteam]: Anthropic, [Strengthening Red Teams](https://alignment.anthropic.com/2025/strengthening-red-teams/)
[^anthropic-bloom]: Anthropic, [Introducing Bloom](https://www.anthropic.com/research/bloom)
