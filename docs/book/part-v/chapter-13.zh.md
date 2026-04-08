# 第 13 章：离线评测、在线评测与回归门禁

## 1. 为什么只有追踪和 SLO 还不足以改进系统

当你已经有了追踪和 SLO，很容易产生一种感觉：可观测性“差不多做完了”。但这其实只是走到一半。

追踪帮你理解发生了什么。
SLO 帮你定义什么叫系统健康。

但最重要的工程问题还在：如何避免把退化版本发出去，以及如何系统性地提升质量？

这就是评测闭环的起点。

!!! info "需要配套的 schema 和工程工件？"
    如果你需要的不只是原理说明，可以直接打开 [Trace Schema 与 Event Catalog](../../appendix/trace-schema.zh.md) 和 [Eval Dataset Schema 与 Grading Contract](../../appendix/eval-schema.zh.md)。

## 2. 离线评测的作用，是在发布之前改变系统

离线评测回答的是一个非常实际的问题：“如果我们修改提示、策略、检索、模型路由或工具行为，系统在已知场景上会变好还是变坏？”

好的 offline evals 通常围绕这些东西构建：

- 精选任务集；
- golden answers 或 expected outcomes；
- 对策略敏感的边界场景；
- 棘手的检索场景；
- 高风险工具工作流。

它们的价值在于：你可以在生产流量到来之前比较系统版本。

## 3. 在线评测之所以必要，是因为真实世界总比测试集更大

即使很好的离线评测，也无法覆盖生产环境中真正发生的一切：

- 用户会提出新的任务类型；
- 输入分布会漂移；
- 外部系统会退化；
- 检索基础会不断变大；
- 策略规则在新数据上会表现不同。

所以在线评测不是离线评测的替代，而是第二条闭环：

- 评估真实流量上的行为；
- 捕捉 drift；
- 发现静默回退；
- 观察系统在真实运行条件下的表现。

## 4. 最好的形态不是“离线或在线”，而是两条闭环同时存在

一种非常实用的模型是：

- 离线评测在发布前阻挡明显回退；
- 在线评测在发布后发现新问题；
- 追踪提供分析原料；
- SLO 提供运行边界；
- 回归门禁阻止质量悄悄下滑。

<div class="diagram-card">
<p>最好把 eval loop 理解成持续循环，而不是一次性检查</p>

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

## 4.1. 当静态案例不够时，user simulator 很有价值

Google 最近的材料还强调了一个很实用的层次：eval loop 最好不要只靠固定 test set，还可以补上一层 user simulator。[^google-govern]

这在下面这些问题上特别有帮助：

- agent 在长对话里会怎么表现；
- 回答不完美之后行为会不会跑偏；
- 系统会不会正确发起澄清；
- 多轮场景里 policy path 会不会断掉；
- 用户说法更有变化时 orchestration 会不会退化。

Static eval set 很适合比较 known cases。User simulator 更适合检查行为动态，而不只是看一个预设样例上的分数。

## 4.2. Continuous eval loop 应该反过来影响 rollout decisions

当你已经有了 online evals、trace grading 和 simulated conversations，下一步就很关键：这些结果不能只是被记录下来，它们应该真正影响 release process。

一个健康的 operational 模型通常是：

- offline evals 在发布前拦住明显 regressions；
- user simulator 帮你测试那些难以固化进静态 dataset 的场景；
- online evals 和 trace grading 捕捉 drift 与新 failure modes；
- rollout gates 决定是否继续扩大暴露范围。

也就是说，eval loop 最好不要被看成“独立的分析活动”，而应该被视为 change management 的一部分。

## 5. 追踪分级对智能体系统特别有价值

普通应用往往只要业务 KPI 和错误率就够了。智能体系统不行，因为质量经常藏在一次运行内部，而不只在最终答案上。

追踪分级的价值在于，你可以评估：

- retrieval 是否合适；
- 工具调用是否必要；
- prompt 是否被过度塞满；
- 是否发生了不必要的升级；
- 是否遵守了策略约束；
- workflow 是否高效。

这在最终结果看起来还“不错”，但系统已经悄悄变慢、变贵或变危险时特别重要。

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

## 5.2. Coordination failure 也应该成为 eval design 的一部分

如果系统使用交接、管理者模式，或者多个协作智能体，那么只检查“答案对不对”已经不够。

还需要额外观察：

- handoff 过程中是否丢失上下文；
- 是否出现 conflicting actions；
- 验证纪律是否退化；
- 是否出现更多不必要的委派步骤；
- 协作失效能否从追踪中被定位。

因此，多智能体可靠性研究在这里的价值，不是鼓励默认把运行时做得更复杂，而是在提醒我们：编排越复杂，评测设计就必须越丰富。

## 6. Eval dataset 里应该放什么

一个很常见的错误是：eval dataset 主要由舒服的 demo 场景组成。这种集合几乎帮不上什么忙。

好的 dataset 通常会包含：

- happy-path 任务；
- ambiguous user requests；
- prompt injection attempts；
- retrieval edge cases；
- missing-data scenarios；
- tool timeout 和 partial failure cases；
- approval-required flows；
- cross-tenant 和 privacy-sensitive cases。

真正的工程价值，通常正是在这些困难又不舒服的场景里。

## 7. Regression gate 应该是形式化的，而不是“大家看了一眼”

团队常会说：“我们测过了，感觉没有更差。” 对 production-grade 的 agent system 来说，这远远不够。

回归门禁更有价值的做法，是把它定义为一组明确规则，例如：

- critical eval set 上的 success rate 不能下降；
- safety metrics 不能退化；
- cost per task 不能超过阈值；
- escalation rate 不能升高；
- 提示预算或每次运行的工具数量不能超过上限。

这样发布决策就不会只依赖改动作者的直觉。

## 8. 一个 eval gate policy 示例

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

这些数字不是普适标准。重要的是 gate 要可机读，团队对它的争论应发生在标准层，而不是感觉层。

## 9. 一个简单的 regression decision 示例

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

代码刻意很简单。恰恰是这种简单性，让 gate 对团队而言可理解、可讨论。

## 10. 在线评测必须和发布策略连起来

一个非常有用的做法是不要把大变更一次性打给所有人，而是使用：

- shadow mode；
- canary rollout；
- limited tenant exposure；
- model routing experiments；
- staged policy rollout。

这样在线评测就不只是“上线后看看会不会出事”，而是发布流程中的受控阶段。

### 10.1. 好的模拟器不会替代真实数据，只会补充真实数据

也要注意不要高估 user simulator。

它不能替代：

- 真实 production traces；
- 真实 complaint patterns；
- 真实的 cost 与 latency distributions；
- 真实 incident postmortems。

但它很适合作为 offline dataset 和 live rollout 之间的中间层，因为它能更快帮助你检查：

- conversational robustness；
- handoff behavior；
- escalation discipline；
- fallback quality；
- policy-sensitive turns。

## 11. Eval culture 最常见的崩坏点

这些问题很常见：

- offline evals 太像玩具；
- online evals 和 traces 断开；
- regression gates 只看 success rate；
- safety regressions 不阻止 rollout；
- cost regressions 不被当成真正的 regressions；
- dataset 不更新，系统开始优化陈旧场景。

一旦如此，eval loop 就会退化成 ritual，而不是改进机制。

## 12. 实用检查清单

如果你想快速检查 eval loop，可以问：

- 是否有针对关键场景的 curated offline eval set？
- 是否有和 traces、SLO 相连的 online eval signal？
- 是否不仅能 grade final answer，也能 grade run 本身？
- rollout 前是否存在 formal regression gate？
- 是否把 safety 和 cost 也放进了 gate，而不只是 task success？
- eval dataset 是否会依据真实事故持续更新？

如果连续几个答案都是否，那说明你可能已经有 observability，但还没有真正的 learning loop。

## 13. 接下来读什么

Part V 到这里已经是一个完整的 operational block：traces、SLO 和 eval loop。下一步自然就是组织模型，因为这种平台最终既会碰到代码问题，也会碰到团队设计问题。

## 14. 值得配套阅读的参考页

- [Trace Schema 与 Event Catalog](../../appendix/trace-schema.zh.md)
- [Eval Dataset Schema 与 Grading Contract](../../appendix/eval-schema.zh.md)
- [Lifecycle Artifact Schema](../../appendix/lifecycle-artifact-schema.zh.md)
- [研究前沿：记忆、可观测性与多智能体可靠性](../../appendix/research-frontier.zh.md)

- [第 12 章：智能体系统的 SLO](chapter-12.zh.md)
- [第 25 章：Behavioral Evals、Control Evals 与 Automated Red Teaming](../part-viii/chapter-25.zh.md)
- [第五部分：可靠性与可观测性](index.zh.md)
- [参考来源](../../appendix/sources.md)

[^google-govern]: [Google Cloud, More ways to build, scale, and govern AI agents with Vertex AI Agent Builder](https://cloud.google.com/blog/products/ai-machine-learning/more-ways-to-build-and-scale-ai-agents-with-vertex-ai-agent-builder)
