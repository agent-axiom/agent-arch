# 第 13 章：离线评测、在线评测与回归门禁

## 1. 为什么只有 traces 和 SLO 还不足以改进系统

当你已经有了 traces 和 SLO，很容易产生一种感觉：observability “差不多做完了”。但这其实只是走到一半。

Traces 帮你理解发生了什么。
SLO 帮你定义什么叫系统健康。

但最重要的工程问题还在：如何避免把退化版本发出去，以及如何系统性地提升质量？

这就是 eval loop 的起点。

## 2. Offline evals 的作用，是在 rollout 之前改变系统

Offline evals 回答的是一个非常实际的问题：“如果我们修改 prompt、policy、retrieval、model routing 或 tool behavior，系统在已知场景上会变好还是变坏？”

好的 offline evals 通常围绕这些东西构建：

- curated task sets；
- golden answers 或 expected outcomes；
- 对 policy 敏感的 edge cases；
- 棘手的 retrieval scenarios；
- high-risk tool workflows。

它们的价值在于：你可以在生产流量到来之前比较系统版本。

## 3. Online evals 之所以必要，是因为真实世界总比测试集更大

即使很好的 offline evals，也无法覆盖 production 中真正发生的一切：

- 用户会提出新的任务类型；
- 输入分布会漂移；
- 外部系统会退化；
- retrieval 基础会不断变大；
- policy rules 在新数据上会表现不同。

所以 online evals 不是 offline 的替代，而是第二条闭环：

- 评估真实流量上的行为；
- 捕捉 drift；
- 发现 silent regressions；
- 观察系统在真实 operational 条件下的表现。

## 4. 最好的形态不是“offline 或 online”，而是两条闭环同时存在

一种非常实用的模型是：

- offline evals 在发布前阻挡明显 regressions；
- online evals 在发布后发现新问题；
- traces 提供分析原料；
- SLO 提供 operational 边界；
- regression gates 阻止质量悄悄下滑。

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

## 5. Trace grading 对 agent systems 特别有价值

普通应用往往只要 business KPI 和 error rate 就够了。Agent systems 不行，因为质量经常藏在 run 内部，而不只在最终答案上。

Trace grading 的价值在于，你可以评估：

- retrieval 是否合适；
- tool call 是否必要；
- prompt 是否被过度塞满；
- 是否发生 unnecessary escalation；
- 是否遵守了 policy constraints；
- workflow 是否高效。

这在 final result 看起来还“不错”，但系统已经悄悄变慢、变贵或变危险时特别重要。

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

Regression gate 更有价值的做法，是把它定义为一组明确规则，例如：

- critical eval set 上的 success rate 不能下降；
- safety metrics 不能退化；
- cost per task 不能超过阈值；
- escalation rate 不能升高；
- prompt budget 或 tool count per run 不能超过上限。

这样 rollout 决策就不会只依赖改动作者的直觉。

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

## 10. Online evals 必须和 rollout strategy 连起来

一个非常有用的做法是不要把大变更一次性打给所有人，而是使用：

- shadow mode；
- canary rollout；
- limited tenant exposure；
- model routing experiments；
- staged policy rollout。

这样 online evals 就不只是“上线后看看会不会出事”，而是 release process 中的受控阶段。

## 11. Eval culture 最常见的崩坏点

这些问题很常见：

- offline evals 太像玩具；
- online evals 和 traces 断开；
- regression gates 只看 success rate；
- safety regressions 不阻止 rollout；
- cost regressions 不被当成真正的 regressions；
- dataset 不更新，系统开始优化陈旧场景。

一旦如此，eval loop 就会退化成 ritual，而不是改进机制。

## 12. Practical checklist

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

- [第 12 章：智能体系统的 SLO](chapter-12.zh.md)
- [第五部分：可靠性与可观测性](index.zh.md)
- [参考来源](../../appendix/sources.md)
