# 第 11 章：追踪、跨度与结构化事件

## 1. 不要先从日志开始，要先从一次事故调查开始

继续沿用同一个支持场景。

用户写道：

> 我已经等了三天还没有开通访问权限。请检查状态，如果申请卡住了，就创建一个紧急工单。

智能体回复说工单已经创建。十分钟后，值班人员在 helpdesk 里看到了 **两张** 一模一样的工单。

这时团队面对的是一个非常具体的问题：

- 是模型自己重复发起了调用；
- 是 timeout 之后触发了 retry；
- 是工具返回了含糊不清的结果；
- 是 side effect 发生在 runtime 看到错误之前；
- 还是两个不同的 runs 各自创建了一张工单。

如果你手里只有 application logs 和几条指标，这个答案通常既慢又难找。

这就是为什么智能体系统的可观测性不该围绕“日志总量”来设计，而要围绕“能否还原一次 run 的历史”来设计。

## 2. 为什么普通日志几乎总是不够

当系统简单时，扁平日志和少量指标也许够用。但智能体系统几乎总是更复杂：

- 一个用户请求会变成多步骤 run；
- run 内部有 planning、retrieval、prompt assembly、tool calls 和 policy gates；
- 某些步骤会被放到后台；
- 错误出现的位置可能并不是它真正开始的地方。

如果你只用扁平日志看这些东西，很快就会失去因果关系。你能看到噪音，却看不到执行历史。

对于这个支持事故，这意味着一件很简单的事：没有好的 tracing，团队就无法知道是谁创建了重复工单，以及为什么会发生。

## 3. Trace 是一次 run 的故事，span 是一个有意义的步骤

这里最好先固定一个简单模型：

- `trace` 描述请求或 run 的完整路径；
- `span` 描述这条路径中的一个重要步骤；
- `structured events` 补充那些不该埋在自由文本里的精确信息。

对于同一个支持场景，一次 run 可能包含：

- policy evaluation；
- retrieval；
- model inference；
- tool execution；
- approval wait；
- background memory update。

当这种结构存在后，团队就不再把系统看成杂乱调用流，而是看成一串可观察的决策。

## 4. 在这个支持场景里，trace 应该长什么样

下面这张图的重要性不在“好看”，而在于它能告诉你故障到底可能发生在哪一层。

<div class="diagram-card">
<p>成熟的 trace 不该只展示模型，还应展示关键 control points</p>

``` mermaid
flowchart LR
    A["User request"] --> B["Run trace"]
    B --> C["Policy span"]
    B --> D["Retrieval span"]
    B --> E["Model span"]
    B --> F["Tool span: check status"]
    B --> G["Tool span: create ticket"]
    B --> H["Approval span"]
    B --> I["Memory update span"]
```

</div>

如果这个 trace 被正确采集，团队应该能很快看清：

- 第二次 tool call 是否发生在同一个 run 里；
- 是否出现了 retry；
- `idempotency_key` 是什么；
- `side_effect_unknown` 出现在哪一步；
- 是否存在 approval；
- 哪个 policy gate 放行了这个动作。

## 5. 哪些东西适合做成独立 span

没必要给每个小细节都建 span，但整个 run 只有一个 giant span 也几乎没用。

一个实用规则是：

- orchestration step 单独一个 span；
- retrieval 单独一个 span；
- model call 单独一个 span；
- 每次 tool call 单独一个 span；
- 如果 policy decision 会改变行为，就给它单独一个 span；
- 如果存在 human approval wait，也单独建一个 span。

这样 trace 既保持可读，又能真正告诉你时间、成本和可靠性到底花在了哪里。

## 6. 结构化事件在 plain text 只会碍事的地方最有价值

一个常见错误是：有价值的 operational facts 被写进了给人看的日志里，结果以后既无法分析，也无法调查。

结构化事件尤其适合这些地方：

- policy decisions；
- tool outcomes；
- prompt assembly metadata；
- token usage；
- cost attribution；
- idempotency keys；
- tenant 和 principal context；
- memory writes。

也就是说，event 应该回答的不是“这条日志怎么写”，而是“以后哪些信息需要被机器当作证据来分析”。

## 7. 好的 trace model 展示的是 control plane，而不只是 LLM latency

如果可观测性最终只剩模型响应时间，团队看到的 picture 会非常扭曲。

现实里，同一个支持 run 往往坏在别处：

- retrieval 开始返回噪音；
- policy engine 过度阻断；
- approval wait 被拉长；
- tool adapter 退化；
- background updates 堵住队列；
- prompt assembly 膨胀了上下文；
- write tool 返回了模糊结果。

所以 trace model 应覆盖整个 control flow，而不只是 inference step。

## 8. Trace 和 span 的最小字段集合

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

对于这个支持事故，这些字段已经足够把 runtime、tool gateway 和具体的外部 side effect 串起来。

## 9. tracing 的实用规则

如果要把 tracing 压缩成一组可执行规则，通常这些就够了：

1. 每个 run 都应该有一个不会在 policy、model 和 tool spans 之间丢失的 `trace_id`。
2. Trace 应该覆盖 control plane，而不只是 model latency。
3. 所有 tool calls、approval waits 和 policy decisions 都应该留下 machine-readable events。
4. 不确定性要明确记录：`side_effect_unknown` 比假装成 `success` 更有价值。
5. Redaction 和 schema stability 应该一开始就设计进去，而不是等第一次 incident review 之后再补。

## 10. 一个 tool execution 的 structured event 示例

下面这个模板能很好地展示正确的思路：

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

### 10.1. 对这个案例来说，还有四个字段特别重要

如果目标不只是做 dashboard，而是真正调查事故，通常还值得补上：

- `approval_id`
- `tool_principal`
- `request_id` 或其他业务对象 id
- `result_class`

正是这些字段，往往能帮你区分：

- duplicate tool call；
- late retry；
- 错误的 tenant scope；
- 模糊的 external response。

## 11. 一个简单的 span emission 示例

下面这个骨架不是为了替代 tracing SDK，而是为了说明一个原则：span 不只是开始和结束，它还必须把步骤类型和结果记录成可分析的结构。

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

这个例子故意很简单。它的重点不是替代 tracing SDK，而是强调：每个重要步骤都应该留下结构化的痕迹。

## 12. 哪些东西尤其不能原样写进日志

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

## 13. 智能体可观测性最常见的崩坏点

这些问题非常典型：

- trace 只覆盖 model call；
- tool calls 无法和原始 run 关联；
- policy decisions 在代码里可见，但在 telemetry 里不可见；
- events 有了，但没有 tenant/principal context；
- spans 太粗或太噪；
- event schema 经常变化，导致分析系统失效。

一旦这样，团队又会回到猜测和人工读日志的状态。

## 14. 给智能体可观测性做一次快速成熟度测试

团队不应该只因为已经有 dashboards、logs 和 model latency 图表，就把 observability 叫做成熟。

更高的标准应该是：

- 一次 run 可以被 end to end 重建出来；
- policy、model、tool 和 approval layers 都真正可见；
- 不确定性不会被压扁成伪装的 success；
- telemetry 既能支持 incident review，也能支持 release decisions；
- 敏感数据处理是被设计好的，而不是临时 improvisation。

如果这些条件不满足，系统也许已经会发 telemetry，但它还没有 operational observability。

## 15. 读完这一章后先做什么

如果你想快速检查可观测性模型，可以先过一遍这个短清单：

1. 能否通过一个 `trace_id` 重建完整 run 路径？
2. retrieval、model calls、tool calls 和 policy gates 是否都有独立 spans？
3. idempotency keys 和 policy decision ids 是否被记录？
4. telemetry 中是否带 tenant/principal context？
5. 能否看见 run 时间花在哪里、成本在哪里上涨？
6. 敏感 payloads 是否没有泄露到 traces 中？
7. structured event schema 是否稳定？

如果连续几个答案都是否，那可观测性还只是装饰性的，而不是运行层面的。

## 16. 接下来读什么

沿着同一条故事线，下一步也很明确：当团队已经能还原一次故障的完整路径后，就该定义什么才算系统每天都处在“健康”状态，也就是进入 SLO。

- [第 10 章：幂等性、重试、速率限制与回滚边界](../part-iv/chapter-10.zh.md)
- [第 12 章：智能体系统的 SLO](chapter-12.zh.md)
- [第 13 章：离线评测、在线评测与回归门禁](chapter-13.zh.md)
- [第五部分：可靠性与可观测性](index.zh.md)
- [参考来源](../../appendix/sources.zh.md)
