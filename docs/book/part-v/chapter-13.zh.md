# 第 13 章：离线评测、在线评测与回归门禁

!!! info "时效说明"
    本章内容截至 2026 年 4 月 11 日。

    变化最快的部分：

    - 托管式评测产品、模型裁判方法，以及平台化评分流程；
    - 面向记忆、多轮一致性和行为评测的新测试集；
    - 各家平台提供的在线评测与发布门禁工具。

    变化相对较慢的部分：

    - 必须把离线评测、在线评测和回归门禁视为同一个闭环；
    - 评测需要与 traces、SLO 和 rollout 决策绑定；
    - 关键场景必须在发布前被验证，而不是等到事故后才补救。

## 1. 从一个问题开始：怎样避免同一个故障再次被发出去

继续沿用同一个支持场景。

团队已经经历过一次不愉快的事故：

- 智能体创建了重复工单；
- 追踪帮助团队还原了这次运行路径；
- 根因是糟糕的重试路径和薄弱的幂等约束；
- 这个 bug 已经修掉了。

但修完之后，真正的工程问题才出现：

> 怎样保证两周之后，另一次 prompt、policy 或 tool adapter 改动，不会把类似的退化再次带回发布流量？

这就是评测闭环开始的地方。

追踪帮你理解发生了什么。
SLO 帮你定义什么叫系统健康。

但最重要的问题还在：怎样系统性地提升质量，并把回退挡在发布之前？

!!! info "需要配套的 schema 和工程工件？"
    如果你需要的不只是原理说明，可以直接打开 [Trace Schema 与 Event Catalog](../../appendix/trace-schema.zh.md) 和 [Eval Dataset Schema 与 Grading Contract](../../appendix/eval-schema.zh.md)。

## 2. 离线评测的作用，是在发布之前改变系统

离线评测回答的是一个非常实际的问题：

> 如果我们修改 prompt、policy、retrieval、model routing 或 tool behavior，系统在已知关键场景上会变好还是变坏？

对于这个支持智能体，一个好的离线评测集不应该只有舒服的 happy path 场景，还应该包含那些已经真正伤过系统的场景：

- 重复工单场景；
- 已经产生副作用后才超时；
- 含糊的用户请求；
- 需要审批的流程；
- 过期的记忆读取；
- 跨租户的隐私敏感场景。

离线评测的价值就在于：它们让你可以在生产流量到来之前比较系统版本。

最近 verifier design 的一个有用补充是，离线评测不该只依赖 binary success label。对于 long-horizon agents，往往需要更丰富的 grading signal：

- `process quality`；
- `outcome quality`；
- 针对 `controllable` 与 `uncontrollable` causes 的 failure attribution。

否则，团队就分不清一次 run 是“行为正确但被环境阻断”，还是“通过薄弱或 unsafe path 达成了 nominal result”。

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

``` mermaid
flowchart LR
    A["Code / prompt / policy change"] --> B["Offline evals"]
    B --> C["Regression gates"]
    C --> D["Production rollout"]
    D --> E["Online evals + traces"]
    E --> F["Failure analysis and grading"]
    F --> A
```

</div>

对于这个支持场景，这条闭环意味着一件很重要的事：事故不能只留在复盘里。它必须变成评测案例，也必须变成发布规则。

## 4.1. 当静态案例不够时，user simulator 很有价值

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

## 4.2. 持续评测闭环应该反过来影响发布决策

当你已经有了在线评测、追踪分级和模拟对话，下一步就很关键：这些结果不能只是被记录下来，它们应该真正影响发布流程。

一个健康的运行模型通常是：

- 离线评测在发布前拦住明显回退；
- 用户模拟器帮你测试那些难以固化进静态数据集的场景；
- 在线评测和追踪分级捕捉漂移与新的失效模式；
- 发布门禁决定是否继续扩大暴露范围。

也就是说，评测闭环最好不要被看成“独立的分析活动”，而应该被视为变更管理的一部分。

这还意味着，release discipline 必须谨慎决定自己在奖励什么。单一的 end-state score 往往太弱，因为它会掩盖 partial success、blocked-but-correct behavior，或者通过 bad control path 获得的 lucky success。成熟的 eval loop 会使用 richer verifier outputs，让 rollout decisions 反映的不只是最后一个 screen 看起来是否正常，而是系统到底如何行动的。

## 5. 追踪分级对智能体系统特别有价值

普通应用往往只要业务 KPI 和错误率就够了。智能体系统不行，因为质量经常藏在一次运行内部，而不只在最终答案上。

追踪分级的价值在于，你可以评估：

- retrieval 是否合适；
- 工具调用是否必要；
- prompt 是否被过度塞满；
- 是否发生了不必要的升级；
- 是否遵守了策略约束；
- workflow 是否高效。

对这个支持智能体来说，这一点尤其重要，因为用户看到的最终答复也许还“能接受”，但 run 内部可能已经开始：

- 过度调用 `create_support_ticket`；
- 产生不必要的工具跳转；
- 太早进入升级；
- 在没有足够 grounding 的情况下返回状态。

## 5.1. 行为评测与控制评测评估的不只是答案

随着智能体系统获得更多自主性，仅仅评估“一次运行有没有完成任务”已经不够了，还需要评估“系统在过程中表现出了什么样的行为”。

也正是在这里，

- 行为评测；
- 控制评测；
- 自动化红队测试；

开始变得重要。

它们特别适合那些普通 regression set 过于扁平的场景：

- 智能体试图避开监督；
- 它变得过度积极地保留状态；
- 它试图绕过审批路径；
- 它产生了不必要的工具跳转；
- 多个智能体之间的协作开始退化。

也就是说，评测层不应该只评估最终答案质量，还要评估行为层面的失效模式。

这也是 verifier design 为什么重要。如果 grading layer 无法区分 process failure 与 outcome failure，它就无法为 training 和 release control 提供足够强的 evidence。

## 5.2. 协作失效也应该成为评测设计的一部分

如果系统使用交接、管理者模式，或者多个协作智能体，那么只检查“答案对不对”已经不够。

还需要额外观察：

- 交接过程中是否丢失上下文；
- 是否出现相互冲突的动作；
- 验证纪律是否退化；
- 是否出现更多不必要的委派步骤；
- 协作失效能否从追踪中被定位。

因此，多智能体可靠性研究在这里的价值，不是鼓励默认把运行时做得更复杂，而是在提醒我们：编排越复杂，评测设计就必须越丰富。

## 5.3. 多轮一致性也值得单独检查

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

## 6. 评测数据集里应该放什么

一个很常见的错误是：eval dataset 主要由舒服的 demo 场景组成。这种集合几乎帮不上什么忙。

好的 dataset 通常会包含：

- happy-path 任务；
- 含糊的用户请求；
- prompt injection attempts；
- retrieval edge cases；
- missing-data scenarios；
- 工具超时和部分失败场景；
- 需要审批的流程；
- 跨租户和隐私敏感场景。

对于这个支持智能体，这意味着 dataset 里不该只有“检查状态并回复”，还应该有：

- “创建工单，但工具返回 ambiguous result”；
- “用户发来一句紧急话术，但不能被盲目写成 preference”；
- “retrieval 返回冲突状态”；
- “approval path 必须阻止 write action”。

真正的工程价值，通常正是在这些困难又不舒服的场景里。

还应该加入这样一类 cases：行为是正确的，但因为环境侧限制，最终 outcome 仍然不完整。没有这类样本，团队很容易过度优化 binary completion，而忽略系统在压力下是否仍然行为正确。

## 6.1. 记忆层也应该显式进入评测数据集

除了回答质量，还应该单独检查状态在多次运行之间的质量。

这意味着要包含这些 cases：

- 写入 / 不写入决策；
- 过期的档案读取；
- 档案记录之间的矛盾；
- 不安全的持久化；
- 删除与修订行为；
- 长时记忆漂移。

否则记忆事故会反复出现在复盘里，却始终回不到回归纪律。

## 7. 回归门禁应该是形式化的，而不是“大家看了一眼”

团队常会说：“我们测过了，感觉没有更差。” 对 production-grade 的智能体系统来说，这远远不够。

回归门禁更有价值的做法，是把它定义为一组明确规则，例如：

- 关键评测集上的成功率不能下降；
- 安全指标不能退化；
- 单任务成本不能超过阈值；
- 升级率不能升高；
- 提示预算或每次运行的工具数量不能超过上限。

对这个支持智能体来说，所谓 regression 不只是“更不准确了”，还包括：

- 写入工具的重复尝试更多了；
- 不必要的升级更多了；
- 记忆被写入了更多无关内容；
- 解决同类任务的成本变高了。

这样发布决策就不会只依赖改动作者的直觉。

## 8. eval loop 的实用规则

如果要把 engineering 规则压缩成一小组，通常这些就够了：

1. 每个重要 incident 都应该变成一个 eval case 和一条 rollout rule。
2. Offline 和 online evals 应该一起存在：一个在发布前拦回归，一个在发布后抓漂移。
3. Trace grading 应该优先覆盖关键 write paths 和 policy-sensitive flows，而不只是 happy path。
4. Dataset 应该按真实 failures 刷新，而不只是沿用旧 demo cases。
5. Regression gate 应该是 machine-readable 的，并且不仅阻止质量回归，还要阻止 safety、cost 和 escalation 回归。

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

- shadow mode；
- canary rollout；
- limited tenant exposure；
- model routing experiments；
- staged policy rollout。

这样在线评测就不只是“上线后看看会不会出事”，而是发布流程中的受控阶段。

对这个支持智能体来说，这意味着：如果新的 adapter 或新的 prompt 改变了复杂状态案例上的行为，团队应该在 canary 或 shadow 阶段就看到，而不是等到大范围发布之后。

### 11.1. 好的模拟器不会替代真实数据，只会补充真实数据

也要注意不要高估用户模拟器。

它不能替代：

- 真实生产追踪；
- 真实投诉模式；
- 真实的成本与延迟分布；
- 真实事故复盘。

但它很适合作为 offline dataset 和 live rollout 之间的中间层，因为它能更快帮助你检查：

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

## 13. 给 eval loop 做一次快速成熟度测试

团队不应该只因为会跑 benchmark set、偶尔看几项 online metrics，就觉得自己已经有 evaluation discipline。

更高的标准应该是：

- incidents 会被转化成 eval cases 和 rollout rules；
- offline 和 online evals 作为同一个闭环运行，而不是两个分开的 ritual；
- regression gates 不只拦 task failure，也会拦 safety、cost 和 escalation regressions；
- traces 被当成 evidence 来 grading，而不是被动堆成 telemetry；
- dataset 会持续从真实 failures 中学习。

如果这些条件大多不成立，那团队也许已经有一些 evaluation activity，但还没有真正的 learning loop。

## 14. 读完这一章后先做什么

如果你想快速检查评测闭环，可以先过一遍这个短清单：

1. 是否有针对关键场景的精选离线评测集？
2. 是否有和追踪、SLO 相连的在线评测信号？
3. 是否不仅能评估最终答案，也能评估运行过程本身？
4. 发布前是否存在形式化的回归门禁？
5. 是否把安全和成本也放进了门禁，而不只是任务成功率？
6. 评测数据集是否会依据真实事故持续更新？

如果连续几个答案都是否，那说明你可能已经有可观测性，但还没有真正的学习闭环。

## 15. 接下来读什么

到这里，第五部分已经形成一个完整的运行闭环：追踪、SLO 和评测回路。下一步就是组织模型，因为这种平台最终既会碰到代码问题，也会碰到团队设计问题。

## 16. 值得配套阅读的参考页

- [Trace Schema 与 Event Catalog](../../appendix/trace-schema.zh.md)
- [Eval Dataset Schema 与 Grading Contract](../../appendix/eval-schema.zh.md)
- [Lifecycle Artifact Schema](../../appendix/lifecycle-artifact-schema.zh.md)
- [研究前沿：记忆、可观测性与多智能体可靠性](../../appendix/research-frontier.zh.md)

- [第 12 章：智能体系统的 SLO](chapter-12.zh.md)
- [第 25 章：Behavioral Evals、Control Evals 与 Automated Red Teaming](../part-viii/chapter-25.zh.md)
- [第 14 章：平台团队与产品团队](../part-vi/chapter-14.zh.md)
- [第五部分：可靠性与可观测性](index.zh.md)
- [参考来源](../../appendix/sources.zh.md)

[^google-govern]: [Google Cloud, More ways to build, scale, and govern AI agents with Vertex AI Agent Builder](https://cloud.google.com/blog/products/ai-machine-learning/more-ways-to-build-and-scale-ai-agents-with-vertex-ai-agent-builder)
