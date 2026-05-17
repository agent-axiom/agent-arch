# 第 13 章：离线评测、在线评测与回归门禁

!!! info "时效说明"
    最近一次编辑审查：**2026 年 5 月 14 日**。下一次计划审查：**2026 年 6 月 14 日**。

    自上次审查以来的变化：MCP/A2A 安全面、验证器契约、治理感知遥测以及出版就绪问题，已经被明确列为近期编辑任务。

    变化最快的部分：

    - 托管式评测产品、模型裁判方法，以及平台化评分流程；
    - 面向记忆、多轮一致性和行为评测的新测试集；
    - 各家平台提供的在线评测与发布门禁工具。

    变化相对较慢的部分：

    - 必须把离线评测、在线评测和回归门禁视为同一个闭环；
    - 评测需要与追踪、SLO 和 rollout 决策绑定；
    - 关键场景必须在发布前被验证，而不是等到事故后才补救。

## 1. 从一个问题开始：怎样避免同一个故障再次被发出去

继续沿用同一个支持场景。

团队已经经历过一次不愉快的事故：

- 智能体创建了重复工单；
- 追踪帮助团队还原了这次运行路径；
- 根因是糟糕的重试路径和薄弱的幂等约束；
- 这个 bug 已经修掉了。

但修完之后，真正的工程问题才出现：

> 怎样保证两周之后，另一次提示、策略或工具适配器改动，不会把类似的退化再次带回发布流量？

这就是评测闭环开始的地方。

而在本章里，评测回路应该被理解成判断层，而不是响应层。它的任务是在 rollout 扩大或变更获得信任之前，产出关于质量与回归风险的可审查决策。

追踪帮你理解发生了什么。
SLO 帮你定义什么叫系统健康。

但最重要的问题还在：怎样系统性地提升质量，并把回退挡在发布之前？

在本书里，评测回路的角色是很具体的：它负责产出关于质量、行为与回归风险的可审查判断。后面的章节会分别说明保证如何响应发现，可观测性如何保存证据，以及注册表/治理如何分配问责。这里的重点只放在团队如何判断到底测试了什么、发生了什么变化，以及这个变更是否值得被信任。

如果你想看一页专门把评测判断再连接回请求、策略、审批、追踪、事故和 rollout 的桥接层，可以直接使用单独的 [Evidence Spine](evidence-spine.zh.md) 页面。

**Eval case-spine note：**评测集应该在三个 canonical cases 之间保持平衡。Support triage 要测试 duplicate tickets、approval gates、retries 和 side effects。Internal knowledge assistant 要测试 retrieval freshness、source attribution、memory provenance 和 access-control failures。Incident coordination 要测试 escalation timing、handoff quality、response ownership，以及 post-incident changes 是否会在下一次 rollout 前变成 regression cases。

!!! info "需要配套的 schema 和工程工件？"
    如果你需要的不只是原理说明，可以直接打开 [Trace Schema 与 Event Catalog](../../appendix/trace-schema.zh.md) 和 [Eval Dataset Schema 与 Grading Contract](../../appendix/eval-schema.zh.md)。

## 2. 离线评测的作用，是在发布之前改变系统

离线评测回答的是一个非常实际的问题：

> 如果我们修改提示、策略、检索、模型路由或工具行为，系统在已知关键场景上会变好还是变坏？

对于这个支持智能体，一个好的离线评测集不应该只有舒服的顺畅路径场景，还应该包含那些已经真正伤过系统的场景：

- 重复工单场景；
- 已经产生副作用后才超时；
- 含糊的用户请求；
- 需要审批的流程；
- 过期的记忆读取；
- 跨租户的隐私敏感场景。

这也正是失败运行演练进入评测层，而不只是停留在运维演练里的地方。如果团队希望 rollout 审查能信任超时处理、验证失败处理，或者上游依赖故障时的行为，这些降级路径就应该作为带有可追踪失败结果的显式场景进入离线集合。

这里还需要对可追踪保持严格定义。一个降级运行不能因为某处记录了超时就被视为 reviewable。评测回路应验证，这条失败路径仍然保留了足够清晰的发布身份、追踪链接与会话级证据，包括像 `failure_reason` 这样的明确字段，能够支撑后续的 rollout 审查、保证和来源分析。

离线评测的价值就在于：它们让你可以在生产流量到来之前比较系统版本。

最近验证器设计的一个有用补充是，离线评测不该只依赖二元成功标签。对于长周期智能体，往往需要更丰富的评分信号：

- `process quality`；
- `outcome quality`；
- 针对 `controllable` 与 `uncontrollable` causes 的失败归因。

否则，团队就分不清一次运行是“行为正确但被环境阻断”，还是“通过薄弱或不安全路径达成了名义结果”。

因此，实践中的 `verifier contract` 应该被明确写出来，而不是藏在 judge prompt 里。最小契约应该包括：

- `rubric_version`，让团队知道 verdict 是按哪一版评分规则产生的；
- `process_score`，用于评价执行路径，而不只是最终结果；
- `outcome_score`，用于评价真实的用户或业务结果；
- `failure_attribution`，包括 `controllable` / `uncontrollable` 以及具体失败层；
- `judge_human_agreement`，让 automated judge 持续相对于 human review 校准；
- `false_positive_budget` 和 `false_negative_budget`，因为不同 rollout gates 的错误成本不同；
- `calibration_dataset_id`，让 judge、prompt 或 rubric 的变化可以在稳定样本集上重放；
- `replay_protocol`，说明如何恢复有争议 verdict 对应的 traces、inputs、policy bundle 和 artifact version。

这样的契约会把 verifier 从自由文本评论变成 release-bearing artifact：它可以被版本化、跨发布比较，并作为阻止 rollout 的依据。

实践中，最好不要只保存 verdict 文本，还要保存一个小的 verifier verdict record：

- `verdict_id`：评审结果的稳定标识符；
- `verifier_id`：是哪一个 verifier 或 judge 生成了结果；
- `verifier_contract_version`：生成 verdict 时使用的 contract version；
- `input_refs`：指向 scenario、trace、prompt/model version 和 policy bundle 的链接；
- `evidence_refs`：verdict 所依据的证据；
- `blocking_decision`：verdict 是阻止 rollout、仅发出 warning，还是要求 human review；
- `comparison_baseline`：结果是和哪个 previous release/eval baseline 比较的；
- `reviewer_override`：automated verdict 是否被 human 覆盖，以及原因。

如果没有这条记录，verifier contract 很容易只是 prose 里的好想法，而不是强 operational control。有了它，eval verdict 才能被比较、被质疑，并真正用于 release governance。

## 3. 在线评测之所以必要，是因为真实世界永远比测试集更大

即使很好的离线评测，也无法覆盖生产环境中真正发生的一切：

- 用户会提出新的任务类型；
- 输入分布会漂移；
- 外部系统会退化；
- 检索基础会不断变大；
- 策略规则在新数据上会表现不同。

所以在线评测不是离线评测的替代，而是第二条闭环：

- 评估真实流量上的行为；
- 捕捉漂移；
- 发现悄无声息的回退；
- 观察系统在真实运行条件下的表现。

对于这个支持智能体，这意味着一件很简单的事：即使关键测试集是干净的，团队仍然要看见智能体是否开始：

- 更频繁地创建不必要的工单；
- 更早地进入升级；
- 更差地处理不完整状态；
- 用更高的成本完成同类运行。

## 4. 最好的形态不是“离线或在线”，而是两条闭环同时存在

一种非常实用的模型是：

- 离线评测在发布前阻挡明显回退；
- 在线评测在发布后发现新问题；
- 追踪提供分析原料；
- SLO 提供运行边界；
- 回归门禁阻止质量悄悄下滑。

<div class="diagram-card">
<p>最好把评测闭环理解成持续循环，而不是一次性检查</p>
<p><strong>文本 fallback：</strong>code、prompt 或 policy 的变更会经过离线评测、回归门禁、生产 rollout、在线评测与追踪、失败分析，然后把经验反馈到下一轮变更。</p>

``` mermaid
flowchart LR
    A["Code / prompt / policy change"] --> B["离线评测"]
    B --> C["回归门禁"]
    C --> D["生产 rollout"]
    D --> E["在线评测 + 追踪"]
    E --> F["失败分析与评分"]
    F --> A
```

</div>

对于这个支持场景，这条闭环意味着一件很重要的事：事故不能只留在复盘里。它必须变成评测案例，也必须变成发布规则。

!!! example "贯穿案例：把重复工单变成回归门"
    在重复工单事故之后，评测案例不应该只检查最终答复文本。它应该让系统走过“副作用之后超时”的场景，保留 `trace_id` 和 `idempotency_key`，避免创建第二张工单，并输出可供发布门检查的结果。如果新的提示或适配器又把系统带回盲目重试，发布就应该在进入生产前停止。

    完整链条应该是这样：trace 显示 `side_effect_unknown`；verifier 把 failure attribution 归到 retry/reconciliation path；regression gate 把这次发布标记为 blocked；rollout owner 要么修复 adapter，要么让 canary 停在当前比例。这样 eval decision 就不再是抽象分数，而是具体的 release judgment。

### 4.1. 当静态案例不够时，user simulator 很有价值

Google 最近的材料还强调了一个很实用的层次：评测闭环最好不要只靠固定测试集，还可以补上一层用户模拟器。[^google-govern]

这在下面这些问题上特别有帮助：

- 智能体在长对话里会怎么表现；
- 回答不完美之后行为会不会跑偏；
- 系统会不会正确发起澄清；
- 多轮场景里策略路径会不会断掉；
- 用户说法更有变化时编排会不会退化。

对这个支持智能体来说，用户模拟器特别适合这类场景：

- 用户先让你查状态，随后突然改变优先级；
- 智能体只拿到不完整的 `request_id`；
- 工具调用失败后，用户又补充了一条新信息；
- 系统必须在升级、追问和安全停止之间做选择。

静态评测集很适合比较已知案例。用户模拟器更适合检查行为动态，而不只是看一个预设样例上的分数。

### 4.2. 持续评测闭环应该反过来影响发布决策

当你已经有了在线评测、追踪分级和模拟对话，下一步就很关键：这些结果不能只是被记录下来，它们应该真正影响发布流程。

一个健康的运行模型通常是：

- 离线评测在发布前拦住明显回退；
- 用户模拟器帮你测试那些难以固化进静态数据集的场景；
- 在线评测和追踪分级捕捉漂移与新的失效模式；
- 发布门禁决定是否继续扩大暴露范围。

也就是说，评测闭环最好不要被看成“独立的分析活动”，而应该被视为变更管理的一部分。

这个边界很重要，因为评测不应该被塞进生命周期里的所有职责。它们的任务是产出 rollout 可以消费的判断，而不是替代事故响应、遥测设计或全域负责人归属。

这也意味着评测不拥有遏制。它们不会冻结路由、禁用能力，也不会分配紧急响应。它们告诉团队，这个变更是否值得被信任、regression risk 在哪里，以及 rollout 是否应该继续。

这还意味着，发布纪律必须谨慎决定自己在奖励什么。单一的最终状态分数往往太弱，因为它会掩盖部分成功、被阻断但正确的行为，或者通过糟糕控制路径获得的侥幸成功。成熟的评测回路会使用更丰富的验证器输出，让 rollout 决策反映的不只是最后一个屏幕看起来是否正常，而是系统到底如何行动的。

同样的纪律也应该适用于验证器契约变更。如果评分标准因验证器契约版本变更而改变，eval loop 就应该把它显式暴露为承载发布意义的回归信号，而不是悄悄把新的裁决当作与旧结果可直接比较。

## 5. 追踪分级对智能体系统特别有价值

普通应用往往只要业务 KPI 和错误率就够了。智能体系统不行，因为质量经常藏在一次运行内部，而不只在最终答案上。

追踪分级的价值在于，你可以评估：

- 检索是否合适；
- 工具调用是否必要；
- 提示是否被过度塞满；
- 是否发生了不必要的升级；
- 是否遵守了策略约束；
- 工作流是否高效。

对这个支持智能体来说，这一点尤其重要，因为用户看到的最终答复也许还“能接受”，但 run 内部可能已经开始：

- 过度调用 `create_support_ticket`；
- 产生不必要的工具跳转；
- 太早进入升级；
- 在没有足够 grounding 的情况下返回状态。

### 5.1. 行为评测与控制评测评估的不只是答案

随着智能体系统获得更多自主性，仅仅评估“一次运行有没有完成任务”已经不够了，还需要评估“系统在过程中表现出了什么样的行为”。

也正是在这里，

- 行为评测；
- 控制评测；
- 自动化红队测试；

开始变得重要。

它们特别适合那些普通回归集合过于扁平的场景：

- 智能体试图避开监督；
- 它变得过度积极地保留状态；
- 它试图绕过审批路径；
- 它产生了不必要的工具跳转；
- 多个智能体之间的协作开始退化。

也就是说，评测层不应该只评估最终答案质量，还要评估行为层面的失效模式。

这也是验证器设计为什么重要。如果 grading layer 无法区分过程失败与结果失败，它就无法为训练和发布控制提供足够强的证据。

一个好的评测判断可以说“不要继续扩大 rollout”或者“这个场景已经不再可信”；但对这种判断的运营响应属于后面的层次，尤其是 rollout 控制与保证负责人归属。

### 5.2. 协作失效也应该成为评测设计的一部分

如果系统使用交接、管理者模式，或者多个协作智能体，那么只检查“答案对不对”已经不够。

还需要额外观察：

- 交接过程中是否丢失上下文；
- 是否出现相互冲突的动作；
- 验证纪律是否退化；
- 是否出现更多不必要的委派步骤；
- 协作失效能否从追踪中被定位。

因此，多智能体可靠性研究在这里的价值，不是鼓励默认把运行时做得更复杂，而是在提醒我们：编排越复杂，评测设计就必须越丰富。

### 5.3. 多轮一致性也值得单独检查

最近几个月一个很有价值的信号是：智能体在短场景里看起来可能很合理，但在更长的交互回路中会逐渐滑向自相矛盾。

这在下面这些场景里尤其重要：

- 长对话；
- 依赖累积状态；
- 多次重新评估同一个决定；
- 公开解释自己的理由。

因此最好增加明确的 consistency checks：

- 运行会不会在多个轮次之间自我矛盾；
- 没有新信息时理由会不会自己变化；
- 更长的推敲会不会带来更多而不是更少的矛盾；
- 时间漂移能不能通过追踪被定位出来。

### 5.4. LLM-as-a-judge 只有在完成校准之后才真正有用

随着评测层变得更成熟，几乎总会出现另一个诱惑：引入评判模型，然后默认评分现在就可以几乎自动扩展了。

这确实是有用工具，但前提是不要把它误当成事实本身。

对智能体系统来说，评判器往往有一个很重要的限制：只看最终答案文本通常是不够的。如果评分真正想反映结果，评判器最好还能看到那些真正描述系统行为的东西：

- 追踪片段；
- 工具结果；
- 审批事件；
- 结构化评分字段；
- 在可用时接入外部状态检查。

否则系统很容易因为文本写得漂亮而拿到"高分"，即使事实结果其实很差。

这里还有一个很重要的实用规则：如果评判器与人工的一致性很低，第一步通常不应该是扩大数据集，而应该先分析分歧案例，再修正评分规程或评判提示。

这也符合更广泛的人机交互纪律：当 AI 系统出错时，人需要理解自动化的边界，并且能够纠正行为，而不是盲目接受自动评分。[^amershi][^consensus]

这里一个有用信号是 `Cohen's kappa`，但往往比具体数值更重要的是分歧长什么样：评判器到底是在策略违规、工具误用，还是模糊结果上理解错了。

还有一个很常见的自我欺骗来源：一个在强模型上校准好的评判提示，换到更弱模型后可能迁移得很差。所以评判模型一旦变化，最好重新做校准，而不是假设旧提示还能自动沿用。

最后一个规则非常简单：如果你在评估提示变更，就不要同时改提示和模型。否则后面就无法对"到底是什么改善或恶化了系统"做出诚实的因果判断。

## 6. 评测数据集里应该放什么

一个很常见的错误是：评测数据集主要由舒服的演示场景组成。这种集合几乎帮不上什么忙。

好的数据集通常会包含：

- 顺畅路径任务；
- 含糊的用户请求；
- 提示注入尝试；
- 检索边界案例；
- 缺失数据场景；
- 工具超时和部分失败场景；
- 需要审批的流程；
- 跨租户和隐私敏感场景。

对于这个支持智能体，这意味着数据集里不该只有“检查状态并回复”，还应该有：

- “创建工单，但工具返回模糊结果”；
- “用户发来一句紧急话术，但不能被盲目写成偏好”；
- “检索返回冲突状态”；
- “审批路径必须阻止写动作”。

真正的工程价值，通常正是在这些困难又不舒服的场景里。

还应该加入这样一类案例：行为是正确的，但因为环境侧限制，最终结果仍然不完整。没有这类样本，团队很容易过度优化二元完成，而忽略系统在压力下是否仍然行为正确。

### 6.1. 记忆层也应该显式进入评测数据集

除了回答质量，还应该单独检查状态在多次运行之间的质量。

这意味着要包含这些案例：

- 写入/不写入决策；
- 过期的档案读取；
- 档案记录之间的矛盾；
- 不安全的持久化；
- 删除与修订行为；
- 长时记忆漂移。

否则记忆事故会反复出现在复盘里，却始终回不到回归纪律。

## 7. 回归门禁应该是形式化的，而不是“大家看了一眼”

团队常会说：“我们测过了，感觉没有更差。” 对生产级的智能体系统来说，这远远不够。

回归门禁更有价值的做法，是把它定义为一组明确规则，例如：

- 关键评测集上的成功率不能下降；
- 安全指标不能退化；
- 单任务成本不能超过阈值；
- 升级率不能升高；
- 提示预算或每次运行的工具数量不能超过上限。

对这个支持智能体来说，所谓回归不只是“更不准确了”，还包括：

- 写入工具的重复尝试更多了；
- 不必要的升级更多了；
- 记忆被写入了更多无关内容；
- 解决同类任务的成本变高了。

这样发布决策就不会只依赖改动作者的直觉。

## 8. 评测回路的实用规则

如果要把工程规则压缩成一小组，通常这些就够了：

1. 每个重要事故都应该变成一个评测案例和一条 rollout 规则。
2. 离线和在线评测应该一起存在：一个在发布前拦回归，一个在发布后抓漂移。
3. 追踪评分应该优先覆盖关键写路径和策略敏感流程，而不只是顺畅路径。
4. 数据集应该按真实失败刷新，而不只是沿用旧演示案例。
5. 回归门禁应该是机器可读的，并且不仅阻止质量回归，还要阻止安全、成本、升级和验证器契约回归。

## 9. 一个评测门禁策略示例

```yaml
gates:
  offline:
    min_task_success_rate: 0.97
    max_policy_violation_rate: 0.002
    max_avg_cost_delta_pct: 8
  online:
    max_slo_burn_rate: 1.0
    max_manual_intervention_rate: 0.08
    max_unknown_side_effect_rate: 0.0005
  rollout:
    require_offline_pass: true
    require_online_shadow_period: true
```

这些数字不是普适标准。重要的是门禁要可机读，团队对它的争论应发生在标准层，而不是感觉层。

## 10. 一个简单的回归决策示例

下面这个骨架展示的是一个核心思路：发布要绑定在可度量阈值上，而不是绑定在“总体感觉不错”上。

```python
from dataclasses import dataclass


@dataclass
class EvalSummary:
    task_success_rate: float
    policy_violation_rate: float
    avg_cost_delta_pct: float


def passes_regression_gate(summary: EvalSummary) -> bool:
    if summary.task_success_rate < 0.97:
        return False
    if summary.policy_violation_rate > 0.002:
        return False
    if summary.avg_cost_delta_pct > 8:
        return False
    return True
```

代码刻意很简单。恰恰是这种简单性，让门禁对团队而言可理解、可讨论。

## 11. 在线评测必须和发布策略连起来

一个非常有用的做法是不要把大变更一次性打给所有人，而是使用：

- 影子模式；
- 金丝雀 rollout；
- 有限租户暴露；
- model routing experiments；
- 分阶段策略 rollout。

这样在线评测就不只是“上线后看看会不会出事”，而是发布流程中的受控阶段。

对这个支持智能体来说，这意味着：如果新的适配器或新的提示改变了复杂状态案例上的行为，团队应该在金丝雀或影子阶段就看到，而不是等到大范围发布之后。

### 11.1. 好的模拟器不会替代真实数据，只会补充真实数据

也要注意不要高估用户模拟器。

它不能替代：

- 真实生产追踪；
- 真实投诉模式；
- 真实的成本与延迟分布；
- 真实事故复盘。

但它很适合作为离线数据集和在线 rollout 之间的中间层，因为它能更快帮助你检查：

- 对话稳健性；
- 交接行为；
- 升级纪律；
- 回退质量；
- 策略敏感轮次。

## 12. 评测文化最常见的崩坏点

这些问题很常见：

- 离线评测太像玩具；
- 在线评测和追踪断开；
- 回归门禁只看成功率；
- 安全回退不阻止发布；
- 成本回退不被当成真正的回退；
- 数据集不更新，系统开始优化陈旧场景。

一旦如此，评测闭环就会退化成仪式，而不是改进机制。

## 13. 给评测回路做一次快速成熟度测试

团队不应该只因为会跑基准集合、偶尔看几项在线指标，就觉得自己已经有评估纪律。

更高的标准应该是：

- 事故会被转化成评测案例和 rollout 规则；
- 离线和在线评测作为同一个闭环运行，而不是两个分开的仪式；
- 回归门禁不只拦任务失败，也会拦安全、成本、升级和验证器契约回归；
- 追踪被当成证据来评分，而不是被动堆成遥测；
- 数据集会持续从真实失败中学习。

如果这些条件大多不成立，那团队也许已经有一些评估活动，但还没有真正的学习回路。

## 14. 读完这一章后先做什么

如果你想快速检查评测闭环，可以先过一遍这个短清单：

1. 是否有针对关键场景的精选离线评测集？
2. 是否有和追踪、SLO 相连的在线评测信号？
3. 是否不仅能评估最终答案，也能评估运行过程本身？
4. 发布前是否存在形式化的回归门禁？
5. 是否把安全和成本也放进了门禁，而不只是任务成功率？
6. 评测数据集是否会依据真实事故持续更新？

如果连续几个答案都是否，那说明你可能已经有评测层，但还没有真正强健的判断层。

这时团队也许已经有评分活动，但还没有形成那种足以让后续运营功能稳定依赖的可审查评测纪律。

## 15. 本章的证据模型

本章应该被读成一套 judgment model，而不是 benchmark checklist：

- **稳定主张：** final-answer success 不够；evals 需要覆盖 process quality、outcome quality、failure attribution 和 regression gates。
- **厂商实践：** Google Cloud 的 agent governance guidance 和现代 agent-platform 材料都把 evals 视为 rollout 与 operational control 的一部分，而不只是模型选择。
- **研究与 human-AI practice：** human-centered evaluation 相关工作提醒我们，apparent agreement 或 user satisfaction 可能掩盖薄弱的 judgment signals。
- **运行时实践：** trace-linked eval rows、verifier outputs、rollout gates 和 failed-run reasons 让 eval evidence 可以被 operators 审查。
- **另一种观点：** automated judges 很有吸引力，因为它们可以扩大 review 规模并减少 human bottleneck。本章承认这种价值，但把 judge output 视为需要校准的 evidence，而不是必须服从的 authority；高风险 rollout decisions 仍然需要 disagreement review、明确的 rubric owner 和 trace-backed attribution。
- **作者解释：** 本书把 evals 视为 observability 与 lifecycle governance 之间的 release-judgment layer。
- **快速变化层：** judge models、simulators 与 automated red-team techniques 会快速变化；但 explicit gates 与 attributable failures 的需求不会。

## 16. 接下来读什么

到这里，第五部分已经形成一个完整的运行闭环：追踪、SLO 和评测回路。下一步就是组织模型，因为这种平台最终既会碰到代码问题，也会碰到团队设计问题。

## 17. 值得配套阅读的参考页

- [Trace Schema 与 Event Catalog](../../appendix/trace-schema.zh.md)
- [Eval Dataset Schema 与 Grading Contract](../../appendix/eval-schema.zh.md)
- [Lifecycle Artifact Schema](../../appendix/lifecycle-artifact-schema.zh.md)
- [研究前沿：记忆、可观测性与多智能体可靠性](../../appendix/research-frontier.zh.md)

- [第 12 章：智能体系统的 SLO](chapter-12.zh.md)
- [第 25 章：行为评测、控制评测与自动化红队测试](../part-viii/chapter-25.zh.md)
- [第 14 章：平台团队与产品团队](../part-vi/chapter-14.zh.md)
- [第五部分：可靠性与可观测性](index.zh.md)
- [参考来源](../../appendix/sources.zh.md)

[^google-govern]: [Google Cloud, More ways to build, scale, and govern AI agents with Vertex AI Agent Builder](https://cloud.google.com/blog/products/ai-machine-learning/more-ways-to-build-and-scale-ai-agents-with-vertex-ai-agent-builder)
[^amershi]: Microsoft Research, [Guidelines for Human-AI Interaction](https://www.microsoft.com/en-us/research/publication/guidelines-for-human-ai-interaction/)
[^consensus]: OpenReview, [The Illusion of Consensus in Human-Centered Interactive AI](https://openreview.net/forum?id=eJtBEBmYGB)
