# 第 12 章：智能体系统的 SLO

## 1. 为什么普通可用性指标对智能体来说不够

一旦系统变成智能体系统，传统的“服务是在线还是离线”这种图景就不够用了。

即使所有组件都技术上可用，智能体系统仍然可能是不健康的：

- 单次运行完成得太慢；
- 单次请求成本悄悄上升；
- 工具调用更频繁地失败；
- 有用回答的比例下降；
- 系统过于频繁地升级给人；
- 策略门禁过度阻断正常场景。

这就是为什么单纯的 `99.9% uptime` 几乎不够。你需要衡量的不只是组件可用性，还要衡量完整运行的质量。

## 2. 智能体系统的 SLO 应描述系统行为，而不是组件健康度

一个很常见的错误是拿各个子组件的指标，当成整个平台的健康度。

例如：

- 模型 latency；
- vector store uptime；
- 某个 API 的 p95；
- adapter 的错误数。

这些都很有用，但它们并没有回答最核心的问题：“用户是否以合理速度、在安全前提下获得了好的结果？”

因此，智能体系统的 SLO 更适合围绕运行级结果来构建。

## 3. 哪些 SLO 真的有意义

对 production-grade agent system 来说，至少四组 SLO 通常最有价值：

- success SLO；
- latency SLO；
- safety SLO；
- cost SLO。

有时还会补充：

- escalation SLO；
- retrieval 的 freshness SLO；
- 关键能力的工具成功率 SLO。

重点不是一次性测量所有东西，而是挑出那些真正影响用户结果和 operational stability 的指标。

## 4. Success SLO 应该贴近任务，而不是贴近 HTTP 200

最危险的陷阱之一就是：只要一次运行“没崩”，就算成功。

但用户体验并不是这样定义的。一次运行可能：

- 形式上成功结束，但给了无用回答；
- 没有异常，却违反了策略；
- 应该执行动作，却只返回了一段文字；
- 产生了部分副作用，却没把任务做完。

所以 success SLO 更应该和这些东西绑定：

- task completed；
- expected artifact produced；
- approved action completed；
- answer accepted without escalation。

这才更接近系统真正的质量。

## 5. Agent 的 latency SLO 应按阶段拆开

整体运行的 p95 很有用，但它远远不够。看不到阶段分布，你就不知道到底哪里变差了：

- retrieval；
- model inference；
- 工具执行；
- 审批等待；
- background queue pressure。

所以成熟系统通常会跟踪：

- end-to-end run latency；
- model spans 的 p95/p99；
- 工具执行延迟；
- queue wait time；
- approval delay（如果 approval 是产品的一部分）。

这样 latency SLO 就不只是一个漂亮数字，而是实际诊断工具。

## 6. Safety SLO 往往比纯速度更重要

对智能体系统来说，安全不只是策略引擎里的规则，它还是一个可观察的质量目标。

Safety SLO 可以包括：

- 没有策略违规的运行比例；
- 没有 cross-tenant retrieval 的 runs 比例；
- 没有 sensitive egress incidents 的 runs 比例；
- 没有未知副作用的写入动作比例；
- 高风险操作的审批覆盖率。

这尤其重要，因为团队很容易过度关注“更快更便宜”，然后在不知不觉中把 guardrails 磨薄。

<div class="diagram-card">
<p>智能体系统的 SLO 几乎总是同时存在于多个维度</p>

``` mermaid
flowchart LR
    A["Agent system health"] --> B["Success"]
    A --> C["Latency"]
    A --> D["Safety"]
    A --> E["Cost"]
    A --> F["Escalation"]
```

</div>

## 7. Cost SLO 能阻止静默退化

智能体系统有一个很不舒服的特点：成本可能在没有明显故障的情况下悄悄上涨。

例如：

- retrieval 返回了太多上下文；
- planner 多走了几步；
- 模型更频繁地调用工具；
- 重试把一次运行悄悄放大了；
- 记忆层把过多摘要带进提示。

因此，cost SLO 至少应该关注：

- 每次成功运行的成本；
- 每次运行的令牌数；
- 每次运行的工具调用数；
- 高成本模型的使用比例。

否则系统可能依然“能工作”，但已经不再经济。

## 8. Escalation SLO 能避免把人拖垮

如果系统里有 human-in-the-loop，这并不是一个免费的 fallback。

一个系统如果：

- 过于频繁地请求审批；
- 过于频繁地落入人工补救；
- 过于频繁地把决策交给人，

看上去也许很安全，但实际上只是在把混乱搬给运营或审核人员。

因此，最好追踪：

- 升级率；
- 高风险流程的审批率；
- 人类作出决定的中位时间；
- 无需人工干预即可完成的运行比例。

## 9. 一个智能体平台的 SLO 策略示例

```yaml
slo:
  success:
    successful_run_rate: ">= 97%"
  latency:
    run_p95_ms: "<= 12000"
    tool_span_p95_ms: "<= 2500"
  safety:
    policy_violation_rate: "< 0.2%"
    unknown_side_effect_rate: "< 0.05%"
  cost:
    avg_tokens_per_run: "<= 18000"
    avg_cost_per_successful_run_usd: "<= 0.12"
  escalation:
    manual_intervention_rate: "< 8%"
```

这里最重要的不是具体数字，而是这套纪律本身：团队必须对“什么算系统健康”达成明确共识。

## 10. 一个简单的 health classification 示例

这个小示例展示了：一次运行应该按多个维度判断，而不是只看一项指标。

```python
from dataclasses import dataclass


@dataclass
class RunHealth:
    successful: bool
    latency_ms: int
    policy_violated: bool
    cost_usd: float


def classify_run_health(run: RunHealth) -> str:
    if run.policy_violated:
        return "safety_failure"
    if not run.successful:
        return "task_failure"
    if run.latency_ms > 12_000:
        return "slow_success"
    if run.cost_usd > 0.12:
        return "expensive_success"
    return "healthy"
```

它的想法很简单，但非常有用：一次运行可以形式上成功，却在运行质量上很差。

## 11. 智能体系统的 SLO 最常见的崩坏点

典型问题总是重复出现：

- success 用 HTTP status 计算；
- 延迟只看模型调用；
- 成本根本不进入健康模型；
- safety 被放到 reliability 体系之外；
- 人工升级没有被算作系统健康的一部分；
- SLO 写出来了，但发布过程根本不受其约束。

一旦如此，SLO 就会变成 dashboard 装饰，而不是平台控制手段。

## 12. 实用检查清单

如果你想快速检查自己的 SLO，可以问：

- 你是否有运行级的成功定义？
- 你是否能看到按阶段拆开的延迟，而不仅仅是总耗时？
- 你是否有 safety SLO，而不只是 availability？
- 你是否衡量每个有效结果的成本？
- 你是否能看到实际有多少负担落到了人身上？
- 发布决策是否真的绑定到了 SLO，而不是只靠直觉？

如果连续几个答案都是否，那说明平台也许已经“可观察”，但还没有通过质量目标被真正管理。

## 13. 接下来读什么

SLO 之后，下一个自然步骤就是评测闭环：离线评测、在线评测、追踪分级和回归门禁。也正是在那里，可观测性变成持续改进闭环。

- [第 11 章：追踪、跨度与结构化事件](chapter-11.zh.md)
- [第五部分：可靠性与可观测性](index.zh.md)
- [参考来源](../../appendix/sources.md)
