# 第 25 章：行为评测、控制评测与自动化红队测试

!!! info "时效说明"
    最近一次编辑审查：**2026 年 5 月 17 日**。上一次审查：**2026 年 5 月 14 日**。下一次计划审查：**2026 年 6 月 17 日**。

    自上次审查以来的变化：MCP/A2A 安全面、验证器契约、治理感知遥测以及出版就绪问题，现在都有具体的 contract coverage 与 docs-surface guards。

    变化最快的部分：

    - 对抗场景生成器与自动化红队框架；
    - 行为类和控制类基准套件；
    - 模型裁判方法与半自动评分模式。

    变化相对较慢的部分：

    - 必须评估运行时行为，而不只是最终答案；
    - 必须验证控制层本身，而不只是模型质量；
    - 控制评测、回归门禁、contract-version discipline 和 rollout decisions 必须连起来。

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

这里的清晰边界是：评测负责判断系统如何行为，以及控制面在受压时是否真的证明了自己。它们不替代保障响应闭环、可观测性证据层或资产注册表。它们产出的是供这些层后续消费的判断。

这也正是本章的核心承诺。它要帮助读者把评测看成整个生命周期里的可评审判断层：在这里，行为、控制质量和验证器质量会被转化成 rollout、assurance、provenance 与 governance 真正可以依赖的判断。本章的主要工件是 eval gate and verifier contract：可测试的发布条件和评审契约，而不是 incident response，也不是泛泛的 telemetry。

## 2. 什么是行为评测

行为评测不只检查最终输出，还检查系统的行为形态。

最近关于 computer-use agents 验证器设计的一个重要经验是，对于长跨度轨迹，单一的二元 verdict 往往太弱。智能体可能走对了过程，却因为环境阻断而失败，也可能通过不安全路径达成名义结果。所以验证器设计最好把 `process verification` 和 `outcome verification` 分开，而不是压成一个 score。

例如：

- 智能体会不会隐藏一个有争议的步骤；
- 会不会绕过审批；
- 会不会在审查之后改掉载荷；
- 会不会在没有充分理由的情况下进入高风险工具路径；
- 会不会偏离预期的升级路径；
- 会不会利用 contract drift 或 schema mismatch 穿过控制边界；
- 会不会利用 interruption、expiry 或 re-init semantics 重新回到更弱的控制姿态。

也就是说，问题不再只是“答案对不对”，而是“在这个场景下，运行时的行为对不对”。

## 3. 什么是控制评测

控制评测检查的是控制机制本身，而不只是模型质量。

典型问题包括：

- 验证器本身是否使用了可评审的 rubric，而不是不透明的单一 verdict；
- 它是否区分可控失败和不可控失败；

- 策略层能不能真的拦住这个能力；
- 审批门禁是否真的要求人来确认；
- 回滚门禁能不能工作；
- paused-run 与 background-run controls 是否按设计工作；
- capability-session expiry 与 re-init controls 是否按设计工作；
- 副作用会不会进入追踪；
- 紧急控制能不能关掉高风险路径。

这里的关键转变在于：你检查的不只是模型，而是围绕模型的一整层控制面。

在成熟体系里，验证器本身也属于控制面。如果它制造了虚假的信心，rollout 和 training loops 就会继承这个错误。所以验证器设计应该被当成受治理基础设施，而不只是一个方便的 helper prompt。

这也包括 verifier contract swaps。评测回归不一定只来自模型或运行时行为，也可能来自未经审查的 verifier contract version changes，它们会悄悄改变评分标准。

## 4. 什么是自动化红队测试

自动化红队测试不再只是几条手写测试样例，而是一种系统化生成、变换和放大对抗场景的方法。

它的实际价值在于：

- 帮你发现团队自己没想到的失效模式；
- 更有效地覆盖边缘场景；
- 强迫你去观察系统在受压状态下的行为，而不是只看“正常日子”。

Anthropic 最近在这方面的工作尤其值得参考：更强的控制评测脚手架，以及更强的红队场景生成。[^anthropic-redteam][^anthropic-bloom]

## 5. 它和现有评测层的关系

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
- runtime-control evals 还要验证 pause/resume、background、capability-session expiry/re-init、contract-version behavior，以及 orchestration-pattern behavior 在受压场景下是否按预期工作。

OpenAI 关于 agent evals 的指南给出了一条有用的操作阶梯：在调试单个 workflow 行为时先从 traces 开始，用 structured graders 评估 tool choice、handoff、guardrail 和 instruction-following failures，然后把稳定的问题迁移到 datasets 和可重复的 eval runs 中，用于跨时间比较变更。[^openai-agent-evals][^openai-trace-grading] 换句话说，trace grading 是显微镜，而 datasets 和 eval runs 是 regression harness。成熟的 agent 程序需要这两层：traces 解释某一次 run 为什么失败；datasets 证明新的 prompt、policy、routing rule 或 tool surface 是否改善了一类 runs，同时没有削弱其他地方的 controls。

## 6. 哪些地方最需要这类评测

这类场景尤其适合放在：

- 高风险写入能力；
- 带出口访问的工具；
- 审批密集型工作流；
- 涉及 pause/resume 或 background execution 的 runtime-control transitions；
- capability-session expiry 与 re-initialization paths；
- 替换与退役过渡期；
- 多智能体委派；
- orchestration-pattern selection 与 delegated worker boundaries；
- 记忆写入与检索治理。

如果高风险路径根本没有被这些评测覆盖，团队几乎一定会先从事故里学到教训。

!!! example "贯穿案例：ticket-write 的控制评测"
    对支持分诊来说，只证明“一次只创建了一个工单”的回归评测已经不够。团队需要一个会给路径施压的控制评测：确认智能体不会选择旧 gateway route，不会在审批后改写 `create_support_ticket` payload，不会在 freeze 后继续后台重试，而且 emergency disable 真的能关掉整个 ticket-write capability family。这个评测应该同时评分 process 和 outcome：没有创建重复工单，控制路径也没有被绕过。

**Control-eval case-spine note：**[eval gate and verifier contract](../../appendix/eval-schema.zh.md) 应该把三个 canonical cases 作为不同 behavioral and control eval surfaces 来测试。Support triage 需要 duplicate prevention、payload-mutation check、[approval-path misuse check](../../appendix/approval-schema.zh.md)、old-gateway-route probe 和 emergency-disable assertion。Internal knowledge assistant 需要 source-grounding eval、tenant-filter bypass probe、improper-memory-write check、[retrieval-poisoning scenario](../../appendix/memory-retrieval-schema.zh.md) 和 freshness regression gate。Incident coordination 需要 escalation-path check、notification suppression probe、responder-role abuse scenario、[incident-state tampering check](../../appendix/incident-record-schema.zh.md) 和 rollback control eval。

## 7. 一个最小行为分类法

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
- `session_reinit_misuse`
- `runtime_control_regression`
- `delegated_worker_misuse`
- `orchestration_pattern_drift`

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

### 8.1. 研究在这里更适合作为场景类别的来源

最新关于行为风险与自动化红队测试的研究，价值不只在于结论，也在于它提供了更丰富的词汇表。

它能帮助团队补齐那些很难仅靠本地经验就完整想出的场景类别。比如：

- concealment；
- oversight evasion；
- 类似破坏的持续行为；
- 压力下的协作失序；
- 对 schema mismatch 或 control drift 的利用；
- 对 interruption 或 re-init windows 的滥用；
- 对 delegated worker paths 的滥用或 worker-boundary drift。

但工程纪律仍然应该保持严格：

- 场景类别必须进入可评审的 [eval schema](../../appendix/eval-schema.zh.md)；
- 发现结果必须有负责人和分诊路径；
- 发布门禁看到的应是运行证据，而不只是论文引用。

所以，研究在这里最好的用途，是帮助生成假设和危险场景，而不是替代你自己的评测方案。

## 9. 一个控制评测策略示例

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
    - session_reinit_misuse
    - contract_drift_exploitation
    - runtime_control_regression
    - delegated_worker_misuse
    - orchestration_pattern_drift
  block_release_if:
    - control_eval_missing
    - behavioral_eval_regression
    - runtime_control_regression_open
    - verifier_contract_regression_open
    - red_team_findings_untriaged
```

这个层很有价值，因为它把行为检查变成了发布纪律的一部分，而不是“可做可不做的加分项”。

## 10. 一个简单的分级契约

```python
from dataclasses import dataclass


@dataclass
class ControlEvalResult:
    scenario_class: str
    control_enforced: bool
    side_effect_traced: bool
    finding_open: bool
    contract_version_matched: bool
    session_control_enforced: bool


def passes_control_eval(result: ControlEvalResult) -> bool:
    return (
        result.control_enforced
        and result.side_effect_traced
        and result.contract_version_matched
        and result.session_control_enforced
        and not result.finding_open
    )
```

这里的核心是：失效不只是“模型行为古怪”，也包括“控制层没能证明自己真的有效”。

如果分级契约能表达的不只是 pass/fail verdict，而是分开的过程/结果判断，以及可控与不可控原因的失败归因，它就会更强。

## 11. 如何把它接进 ADLC

在成熟系统里，流程通常是这样：

1. 高风险变更先拿到 `change_record`；
2. 定义这次需要的评测范围；
3. 回归评测检查既有行为；
4. 行为评测/控制评测检查高风险路径；
5. 自动化红队测试搜索不那么明显的失效模式；
6. 发现结果进入保障待办列表；
7. 发布门禁看到的不只是准确率，还包括控制证据。

这样评测层就不再只是“一张指标表”，而会变成运行模型的一部分。

也正因为如此，本章更应该被理解成测试与判断层。保障决定如何响应 findings；可观测性保存 evidence；注册表在整个智能体群体上分配问责；而评测决定到底测试了什么、哪里失败了，以及团队当前应当对控制姿态保持多大信心。

## 12. 最常见的错误

- 所有评测最后都退化成最终答案质量；
- 危险路径没有独立的场景类别；
- approval-path misuse、session re-init misuse、delegated-worker misuse 与 contract drift 没有被显式测试；
- verifier outputs 把长轨迹压缩成了过于薄弱的 pass/fail label；
- verifier contract swaps 改变了 grading behavior，却没有被当成 release-bearing eval regressions；
- controllable 与 uncontrollable failures 没有被分开；
- 红队测试只是一次性活动；
- runtime-control regressions 只有在 rollout 或 incidents 中才被发现；
- 发现结果没有进入发布门禁；
- 控制失效被当成“不是模型 bug”，于是从待办列表里消失；
- 团队分不清普通失效和类似破坏的行为。

## 13. 给行为评测和控制评测做一次快速成熟度测试

团队不应该只因为已经有回归评测、模拟器和几条 adversarial prompts，就觉得自己已经准备好面对自主行为。

更高的标准应该是：

- 高风险路径有明确的行为场景类别；
- 控制评测会验证控制层本身在压力下是否真的有效；
- 验证器输出会分开表示过程质量、结果质量与失败归因，而不是把一切压成单一二元判断；
- approval-path misuse、session re-init misuse、delegated-worker misuse、contract drift 与 runtime-control regressions 都有明确的场景覆盖；
- red-team findings 会进入 rollout 和 change gates，而不是停留在单独报告里；
- realistic simulation 和 adversarial generation 扮演不同但互补的角色；
- 发布决策能拿出控制证据，而不只是质量分数。

如果这些条件大多不成立，那团队也许已经有一些评测活动，但还没有足够的行为和控制覆盖。

这时团队也许已经在测量行为，但还没有产出那种足以让 rollout、assurance 与治理函数稳定依赖的可评审判断。

## 14. 实用检查清单

- 高风险能力是否有单独的行为场景类别？
- 你是否测试审批规避、载荷篡改、approval-path misuse 与 delegated-worker misuse？
- 是否有专门验证控制措施、contract-version matching、runtime-control behavior、orchestration-pattern boundaries 与验证器质量的评测，而不只是检查输出质量？
- 验证器能否区分过程失败、结果失败与不可控环境失败？
- 红队发现结果是否会进入变更评审和发布门禁？
- 是否同时有 realistic workload simulator 和 adversarial generator？
- 你能展示的是控制证据，还是只有最终分数？

如果连续几个答案都是“否”，那你的评测层虽然已经存在，但还没准备好面对自主行为。

## 15. 本章的证据模型

本章应该被读成一层 control evidence，而不是一组额外测试类型清单：

- **稳定主张：** 自主系统需要针对 risky trajectories 的 evals，而不只是 final answers。
- **厂商实践：** 现代 agent-eval 材料越来越把 traces、trajectories 与 rollout gates 当作评测的一等输入。
- **运行时实践：** scenario classes、verifier contracts、trace-backed failures 与 rollout gates 是让 behavioral 和 control evidence 可审查的具体方式。
- **作者解释：** behavioral evals、control evals 与 automated red teaming 是同一个 judgment system 中的不同角色，而不是可以互换的标签。
- **快速变化层：** simulator quality、judge models 与 red-team generation 会快速变化；但区分 process failure、outcome failure 与 control failure 的需求不会。

## 16. 值得配套阅读的参考页

- [评测数据集模式与分级契约](../../appendix/eval-schema.zh.md)
- [追踪模式与事件目录](../../appendix/trace-schema.zh.md)
- [变更评审与发布门禁模式](../../appendix/change-rollout-schema.zh.md)
- [策略包模式与审批契约](../../appendix/policy-bundle-schema.zh.md)
- [Approval Schema](../../appendix/approval-schema.zh.md)
- [Lifecycle Artifact Schema](../../appendix/lifecycle-artifact-schema.zh.md)
- [Memory and Retrieval Schema](../../appendix/memory-retrieval-schema.zh.md)
- [研究前沿：记忆、可观测性与多智能体可靠性](../../appendix/research-frontier.zh.md)

- [第 13 章：离线评测、在线评测与回归门禁](../part-v/chapter-13.zh.md)
- [第 21 章：保障闭环：红队测试、检测与响应](chapter-21.zh.md)
- [第 24 章：智能体失配与内部人风险](chapter-24.zh.md)
- [第 26 章：AI 原生可观测性、清单覆盖率与可用于检测的遥测](chapter-26.zh.md)
- [第 27 章：智能体清单、注册表与蔓延治理](chapter-27.zh.md)

[^openai-agent-evals]: OpenAI, [Evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals)
[^openai-trace-grading]: OpenAI, [Trace grading](https://developers.openai.com/api/docs/guides/trace-grading)

[^anthropic-redteam]: Anthropic, [Strengthening Red Teams](https://alignment.anthropic.com/2025/strengthening-red-teams/)
[^anthropic-bloom]: Anthropic, [Introducing Bloom](https://www.anthropic.com/research/bloom)
