# 第 11 章：追踪、跨度与结构化事件

## 1. 为什么普通日志对智能体系统来说几乎总是不够

当系统简单时，一些应用日志和少量指标可能就够了。但智能体系统几乎总是更复杂：

- 一个用户请求会变成多步骤 run；
- run 内部有 planning、retrieval、prompt assembly、工具调用和策略门禁；
- 某些步骤会被放到后台；
- 错误出现的位置可能并不是它真正开始的地方。

如果你只用扁平日志看这些东西，很快就会失去因果关系。你能看到噪音，却看不到一次 run 的完整故事。

这就是为什么智能体可观测性更适合从追踪开始，而不是寄希望于事后用 grep 还原真相。

## 2. Trace 是一次 run 的故事，span 是其中一个有意义的步骤

一个非常有用的简单模型是：

- `trace` 描述请求或 run 的完整路径；
- `span` 描述这条路径中的一个有意义步骤；
- `structured events` 补充那些不该埋在自由文本里的精确信息。

这对智能体系统特别有用，因为一次 run 可能包含：

- policy evaluation；
- retrieval；
- model inference；
- tool execution；
- approval wait；
- background memory update。

当这种结构存在后，团队就不再把系统看成杂乱调用流，而是看成一串可观察的决策。

## 3. 哪些东西适合做成独立 span

没必要给每个细节都建 span，但整个 run 只有一个 giant span 也几乎没用。

一个实用规则是：

- orchestration step 单独一个 span；
- retrieval 单独一个 span；
- model call 单独一个 span；
- 每次 tool call 单独一个 span；
- 如果 policy decision 会改变行为，就给它单独一个 span；
- 如果存在 human approval wait，也单独建一个 span。

这样 trace 既保持可读，又能真正告诉你时间、成本和可靠性到底花在了哪里。

<div class="diagram-card">
<p>成熟的 agent run trace 不该只展示模型调用，还应展示关键 control points</p>

``` mermaid
flowchart LR
    A["User request"] --> B["Run trace"]
    B --> C["Policy span"]
    B --> D["Retrieval span"]
    B --> E["Model span"]
    B --> F["Tool span"]
    B --> G["Approval span"]
    B --> H["Memory update span"]
```

</div>

## 4. 结构化事件在 plain text 只会碍事的地方最有价值

一个常见错误是：有价值的 operational facts 被写进了给人看的日志里，结果以后既无法分析，也无法调查。

结构化事件尤其适合这些地方：

- policy decisions；
- 工具结果；
- prompt assembly metadata；
- token usage；
- cost attribution；
- idempotency keys；
- tenant 和 principal context；
- memory writes。

也就是说，event 应该回答的不是“这条日志怎么写”，而是“以后哪些信息需要被机器分析”。

## 5. 好的 trace model 展示的是 control plane，而不只是 LLM latency

如果可观测性最终只剩模型响应时间，团队看到的 picture 会非常扭曲。

在现实里，run 的失败或退化经常发生在别处：

- retrieval 开始返回噪音；
- policy engine 过度阻断；
- approval wait 被拉长；
- tool adapter 退化；
- background updates 堵住队列；
- prompt assembly 膨胀了上下文。

所以 trace model 应覆盖整个 control flow，而不只是 inference step。

## 6. Trace 和 span 的最小字段集合

如果你希望系统真正便于调查，至少要有：

- `trace_id`
- `span_id`
- `parent_span_id`
- `run_id`
- `tenant_id`
- `principal_id`
- `agent_id` 或 workflow id
- `status`
- `duration_ms`
- 如果发生 model call，则有 `model_name`
- 如果发生 tool call，则有 `tool_name`
- 如果有 gate，则有 `policy_decision_id`

否则 observability 很快就会变成“看起来很好”，但实际上不太能用。

## 7. 一个 tool execution 的 structured event 示例

下面这个模板能很好地展示思路：

```yaml
event_type: tool_execution
trace_id: trc_01HXYZ
span_id: spn_02ABC
run_id: run_9842
tenant_id: tenant_acme
tool_name: create_ticket
status: success
duration_ms: 842
idempotency_key: act_77f1
policy_decision_id: pol_441
side_effect: created
```

它远比一条 “ticket tool ok” 的日志有用。

## 8. 一个简单的 span emission 示例

重点不是替代 tracing SDK，而是说明一个原则：每个重要步骤都应该留下结构化的痕迹。

```python
from dataclasses import dataclass
from time import monotonic


@dataclass
class SpanResult:
    name: str
    status: str
    duration_ms: int


def traced_step(name: str, fn):
    started = monotonic()
    try:
        fn()
        status = "success"
    except Exception:
        status = "failure"
        raise
    finally:
        duration_ms = int((monotonic() - started) * 1000)
        emit_span(SpanResult(name=name, status=status, duration_ms=duration_ms))


def emit_span(result: SpanResult) -> None:
    print({"span_name": result.name, "status": result.status, "duration_ms": result.duration_ms})
```

## 9. 哪些东西尤其不能原样写进日志

Observability 不应该变成数据泄漏渠道。

所以 traces 和 events 里必须特别谨慎对待：

- 完整 prompt bodies；
- 原始 retrieved documents；
- secrets 和 tokens；
- PII；
- 敏感 tool payloads。

最实用的规则是：

- 记录 metadata 和 derived facts；
- 在有帮助时记录 identifiers 和 hashes；
- 没有充分理由时，不要把完整敏感 payload 丢进通用 telemetry pipeline。

## 10. Agent observability 最常见的崩坏点

这些问题非常典型：

- trace 只覆盖 model call；
- tool calls 无法和原始 run 关联；
- policy decisions 在代码里可见，但在 telemetry 里不可见；
- events 有了，但没有 tenant/principal context；
- spans 太粗或太噪；
- event schema 经常变化，导致分析系统失效。

一旦这样，团队又会回到猜测和人工读日志的状态。

## 11. 实用检查清单

如果你想快速检查 observability model，可以问：

- 能否通过一个 `trace_id` 重建完整 run 路径？
- retrieval、model calls、tool calls 和 policy gates 是否都有独立 spans？
- idempotency keys 和 policy decision ids 是否被记录？
- telemetry 中是否带 tenant/principal context？
- 能否看见 run 时间花在哪里、成本在哪里上涨？
- 敏感 payloads 是否没有泄露到 traces 中？
- structured event schema 是否稳定？

如果连续几个答案都是否，那 observability 还只是装饰性的，而不是 operational 的。

## 12. 接下来读什么

下一个自然步骤就是定义什么才算“健康”的 agent system，也就是进入 SLO。

- [第 10 章：幂等性、重试、速率限制与回滚边界](../part-iv/chapter-10.md)
- [第五部分：可靠性与可观测性](index.zh.md)
- [参考来源](../../appendix/sources.md)
