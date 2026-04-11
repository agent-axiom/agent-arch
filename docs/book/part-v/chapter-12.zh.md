# 第 12 章：智能体系统的 SLO

## 1. 从一个问题开始：怎样知道这个支持智能体到底健不健康

继续沿用同一个支持场景。

团队已经会用追踪还原事故，也已经知道重复工单可能来自糟糕的重试路径，记忆写入可能是多余的，工具适配器也可能返回含糊结果。

但在做完最初几次排障之后，接下来的问题会变成：

> 我们怎样不是在事故之后，而是在每天运行时，就知道系统到底健不健康？

这就是 SLO 出场的地方。

普通 uptime 只回答一个问题：“组件是否可用？”

对支持智能体来说，这远远不够。即使所有服务都形式上在线，系统也可能已经不健康：

- 用户等待过久；
- 智能体创建了过多不必要的工单；
- 升级率悄悄上升；
- 典型请求的成本变高；
- 安全路径开始过度打断正常场景；
- 策略门禁要么拦错动作，要么放过多余动作。

SLO 的价值就在于把“系统健康”从感觉变成可度量目标。

!!! info "需要配套的 schema 和工程工件？"
    如果你需要的不只是原理说明，可以直接打开 [Trace Schema 与 Event Catalog](../../appendix/trace-schema.zh.md)、[Incident Record Schema](../../appendix/incident-record-schema.zh.md) 和 [Change Review 与 Rollout Gate Schema](../../appendix/change-rollout-schema.zh.md)。

## 2. SLO 应该描述一次运行的行为，而不是单个部件的健康度

一个很常见的错误是这样：

- 模型响应很快；
- vector store 可用；
- 工单 API 在线；
- adapter 很少报错。

这些都很有用，但没有一个回答了真正的问题：

> 用户是否拿到了正确、安全而且及时的结果？

对这个支持智能体来说，重要的不是某个库的 uptime，而是整次运行的结果：

- 状态是否被正确找回；
- 工单是否只在真正需要时才创建；
- 审批路径是否在该触发时触发；
- side effect 是否没有重复、没有落入不明状态；
- 用户是否没有被无意义地丢给人工。

因此，智能体系统的 SLO 更适合围绕运行级行为来构建。

## 3. 对这个支持智能体来说，真正重要的是五组 SLO

在实践里，production-grade 的智能体系统通常只需要从一个紧凑集合开始：

- success SLO；
- latency SLO；
- safety SLO；
- cost SLO；
- escalation SLO。

这已经足够让团队看见系统不只是“活着”，还是否：

- 真正有用；
- 正在变慢；
- 正在磨薄安全边界；
- 正在变贵；
- 正在把负担转移给人。

不要试图一开始测量一切。先抓住那些真正影响用户结果和运行稳定性的指标。

## 4. Success SLO 应该贴近任务，而不是贴近 HTTP 200

这里最危险的陷阱很简单：只要一次运行没崩，就把它当成功。

但对支持智能体来说，一次运行完全可能形式上“成功”，实际上却很差：

- 答复返回了，但并没有帮到用户；
- 状态在缺乏足够依据时就被返回；
- 本该安全追问时，系统却直接创建了工单；
- 工单被创建了两次；
- 系统只返回了一段文本，而没有完成应该完成的动作。

因此，success SLO 更应该绑定在这些东西上：

- 状态被正确找到并传达；
- 工单只被创建一次，而且上下文正确；
- 请求在该停止或转人工时被安全停止或转交；
- 用户在没有不必要升级的前提下拿到了有用结果。

对支持智能体来说，成功不应该等于“没有异常”，而应该等于“任务真的解决了”。

## 5. Latency SLO 应该按阶段拆开看

如果你只看整体运行 p95，你知道系统变慢了，但不知道为什么。

对同一个支持智能体来说，延迟可能出现在完全不同的地方：

- retrieval 取回请求历史变慢；
- prompt 变胖以后，模型思考更久；
- 工具适配器在外部工单系统上等待太久；
- 审批路径卡在人工环节；
- background queue 开始压住新的运行。

所以，除了 end-to-end latency，更有用的是分阶段看：

- run p95 / p99；
- retrieval latency；
- model span latency；
- tool execution latency；
- approval wait；
- queue wait time。

这样 latency SLO 才不只是漂亮数字，而会变成诊断工具。

## 6. Safety SLO 必须和 reliability 放在一起

在智能体系统里，安全不能被放成一个独立的 security appendix。对生产系统来说，它本身就是系统健康的一部分。

对这个支持智能体来说，至少值得跟踪：

- 没有策略违规的运行比例；
- 没有 cross-tenant retrieval 的运行比例；
- 没有 unknown side effect 的写入动作比例；
- 高风险动作的审批覆盖率；
- 没有隐私敏感外发事故的运行比例。

这在 duplicate ticket 或 unsafe memory write 之后尤其重要：如果 safety 从不进入 SLO，团队很快又会只按速度和便利性优化系统。

<div class="diagram-card">
<p>智能体系统的健康几乎总是多维的</p>

``` mermaid
flowchart LR
    A["Support agent health"] --> B["Success"]
    A --> C["Latency"]
    A --> D["Safety"]
    A --> E["Cost"]
    A --> F["Escalation"]
```

</div>

## 7. Cost SLO 能在事故前抓住静默退化

智能体系统有个很不舒服的特点：它可能在“还能工作”的同时，经济性已经悄悄塌掉。

在这个支持场景里，这通常会表现成：

- retrieval 往 prompt 里塞进太多上下文；
- 模型更频繁地调用工具却没有带来收益；
- planner 多走了几步；
- retries 把一次运行越滚越大；
- 记忆摘要吞掉了过多预算。

因此，cost SLO 至少值得看：

- 每次成功运行的成本；
- 每次运行的 tokens；
- 每次运行的工具调用数；
- 高成本模型的使用比例。

否则团队会很晚才发现退化：那时智能体也许还“在帮忙”，但成本已经显著变高。

## 8. Escalation SLO 保护的是系统周围的人

Human-in-the-loop 不是一个免费的安全网。

如果支持智能体：

- 过于频繁地请求审批；
- 过于频繁地落入人工补救；
- 过于频繁地把决定扔给人；

它也许看上去安全，但实际上只是把混乱转移给操作员。

因此，值得跟踪：

- escalation rate；
- 高风险流程的 approval rate；
- 人类决策的中位耗时；
- 无需人工干预即可完成的运行比例。

对支持智能体来说，这一点很关键：如果升级率太高，自动化很快就会沦为摆设。

## 9. SLO design 的实用规则

如果要把最有用的规则压缩成一小组，通常就是这些：

1. 从 run-level outcome 出发，而不是从单个组件指标出发。
2. Success 应该描述任务被解决，而不只是没有 exception。
3. Safety、cost 和 escalation 都应该算进系统健康，而不是挂在 reliability 旁边。
4. Latency 最好按阶段拆开，否则很难诊断。
5. 只有当 SLO 会影响 rollout 和 change decisions 时，它们才真正有意义。

## 10. 一个支持智能体的 SLO policy 示例

这里重要的不是“标准答案”，而是明确的纪律：

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

重点不在具体阈值，而在于团队提前说清楚：什么才算系统的正常状态。

## 11. 一个简单的 health classification 示例

下面这个小骨架展示的是一个核心思路：一次运行应该同时在多个维度上被判断，而不是只看单一指标。

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

这个模型很简单，但它有价值，恰恰因为它不会把运行质量藏在形式上的“成功”后面。

## 12. SLO 文化最常见的崩坏点

这里的问题非常重复：

- success 用 HTTP status 来算；
- latency 只在 model call 层可见；
- safety 和 reliability 分家；
- cost 从不进入健康模型；
- human escalation 不被当成系统健康的一部分；
- SLO 只挂在 dashboard 上，却不影响 rollout。

一旦如此，SLO 就会变成装饰。团队看到了数字，但并没有通过这些数字来控制平台。

## 13. 读完这一章后先做什么

如果你想快速检查这个支持智能体的 health model，可以先过一遍这个短清单：

1. 是否有运行级的成功定义？
2. 是否能看到按阶段拆开的延迟，而不只是总延迟？
3. 是否有安全 SLO，而不只是 uptime？
4. 是否衡量每个有效结果的成本？
5. 是否能看到有多少真实负担被转移到了人身上？
6. SLO 是否真的会影响发布决策？

如果连续几个答案都是否，那说明可观测性也许已经存在，但系统健康仍然没有通过质量目标被真正管理。

## 14. 接下来读什么

在这条同一条故事线上，SLO 之后的下一步就是评测闭环：离线评测、在线评测、追踪分级和回归门禁。也正是在那里，可观测性变成持续改进闭环。

## 15. 值得配套阅读的参考页

- [Trace Schema 与 Event Catalog](../../appendix/trace-schema.zh.md)
- [Incident Record Schema](../../appendix/incident-record-schema.zh.md)
- [Change Review 与 Rollout Gate Schema](../../appendix/change-rollout-schema.zh.md)

- [第 11 章：追踪、跨度与结构化事件](chapter-11.zh.md)
- [第 13 章：离线评测、在线评测与回归门禁](chapter-13.zh.md)
- [第 14 章：平台团队与产品团队](../part-vi/chapter-14.zh.md)
- [第五部分：可靠性与可观测性](index.zh.md)
- [参考来源](../../appendix/sources.zh.md)
