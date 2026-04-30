# 第 10 章：幂等性、重试、速率限制与回滚边界

## 1. 为什么最贵的失败常常看起来只是“我们又调了一次”

当智能体系统开始执行真实动作时，最糟糕的事故来源之一其实非常朴素：重复调用。

从外面看，它通常显得很无害：

- 请求卡住了；
- 运行时决定重试；
- 集成不稳定；
- 智能体试图“帮忙”，于是把动作又发了一次。

但在现实里，这意味着：

- 两张一模一样的工单；
- 给同一个客户发两封邮件；
- 重复收费；
- CRM 被重复写入；
- 同一个对象被改了好几次。

所以问题不在于模型的推理本身，而在于执行层还不会安全地生活在部分失败的世界里。

## 2. 幂等性不是可有可无的加分项，而是基本保险

幂等性回答的是一个极其简单的问题：“如果系统误把这次调用重复执行了一遍，会发生什么？”

对于写操作，一个好的答案应该是二选一：

- 重复调用不会改变最终结果；
- 系统可以可靠识别重复请求，并避免再次产生副作用。

如果没有这个性质，任何网络不稳定、超时或运行之间的竞态都会变得非常昂贵。

## 3. 没有错误分类的重试只会放大混乱

一种非常糟糕的策略是：“请求失败了，那就再重试三次”。

在生产中，这很危险，因为不同错误完全不是一回事：

- `validation_failure` 几乎从不该重试；
- `permission_denied` 不会因为多试几次就变好；
- `retryable_failure` 才可能需要退避；
- `side_effect_unknown` 需要谨慎，而不是盲目重复。

所以重试策略应该依赖结果类别，而不是“再试试也许行”的情绪。

## 4. 最糟糕的状态是 `side_effect_unknown`

有一类失败尤其让人头痛：你已经不知道副作用到底有没有发生。

例如：

- 请求发给外部服务后超时；
- commit 之后连接断开；
- 适配器崩溃，确认没有落库；
- 外部 API 的响应让最终状态不清楚。

这正是天真重试最危险的场景。有时正确动作不是“重试”，而是：

- 到外部系统检查当前状态；
- 执行对账；
- 交给人处理；
- 停止工作流并明确记录这种不确定性。

## 4.1. 恢复分支也应该被显式设计

最近关于工具失败案例的研究还强化了另一点：恢复路径不应该只是执行层的临场即兴发挥。

最好预先定义：

- 哪些结果类别应该进入对账，而不是重试；
- 哪些部分成功应该生成后续任务；
- 恢复本身在什么情况下也需要审批；
- 哪些分支必须进入评估数据集；
- 哪些危险恢复路径应该直接停下，而不是“再试一次”。

很多严重事故不是发生在顺畅路径，而是发生在设计糟糕的恢复分支。

## 5. 速率限制也是安全设计的一部分

如果团队只把速率限制当成性能问题，执行层就会低估它的架构意义。

实际上，速率限制还用来避免：

- 一个失控智能体把外部系统打挂；
- 循环规划变成工具调用雪崩；
- 高成本能力吃掉所有预算；
- 重试风暴把集成打死。

所以限制不应该只存在于整个服务层面，还应该出现在：

- 每个工具；
- 每个租户；
- 每个工作流；
- 每个风险等级。

## 6. 回滚边界必须提前定义

最危险的事情之一，就是在事故里才发现某个操作“其实根本无法回滚”。

对于每个写能力，最好提前搞清楚：

- 这个动作能不能撤销；
- 这个动作能不能安全重复；
- point of no return 在哪里；
- 什么补偿动作是允许的；
- 什么时候必须人工对账。

也就是说，回滚边界不是“以后再说”，它本身就是工具和工作流契约的一部分。

<div class="diagram-card">
<p>发生副作用之后，执行层必须区分安全重试、对账和停止路径</p>

``` mermaid
flowchart TD
    A["工具请求"] --> B["执行写动作"]
    B --> C{"结果已知？"}
    C -->|是，成功| D["保存结果并继续"]
    C -->|可重试失败| E["按策略与退避重试"]
    C -->|未知副作用| F["对账或请求人工审查"]
    C -->|校验或权限失败| G["停止并暴露错误"]
```

</div>

## 7. 好的执行契约会显式保存运营语义

仅仅知道输入 schema 和返回形状还不够。对危险操作来说，契约还必须记录：

- 这个动作是否幂等；
- 是否必须有幂等键；
- 哪些错误可重试；
- 重试上限是多少；
- 频率限制是什么；
- 未知结果怎么处理；
- 是否存在回滚或补偿动作。

```yaml
tools:
  create_ticket:
    mode: write
    idempotent: true
    idempotency_key_required: true
    retry:
      max_attempts: 3
      backoff: exponential
      retry_on: ["retryable_failure"]
    rate_limit:
      per_tenant_per_minute: 20
    rollback:
      strategy: "none"
      reconcile_on_unknown: true

  send_email:
    mode: write
    idempotent: false
    idempotency_key_required: false
    retry:
      max_attempts: 1
      retry_on: []
    rate_limit:
      per_user_per_hour: 10
    rollback:
      strategy: "manual_only"
      reconcile_on_unknown: true
```

这个 YAML 的价值在于，它逼着团队正视一个不舒服的事实：不是所有动作都同样适合自动化。

## 8. 一个简单的重试决策示例

下面不是生产策略引擎，而是一个小骨架。它的目的就是说明：重试应该依赖结果类别，而不是普遍条件反射。

```python
from dataclasses import dataclass


@dataclass
class ExecutionOutcome:
    status: str
    attempts: int
    max_attempts: int


def next_step(outcome: ExecutionOutcome) -> str:
    if outcome.status in {"validation_failure", "permission_denied"}:
        return "stop"
    if outcome.status == "retryable_failure" and outcome.attempts < outcome.max_attempts:
        return "retry_with_backoff"
    if outcome.status == "side_effect_unknown":
        return "reconcile"
    if outcome.status == "success":
        return "continue"
    return "escalate"
```

重要的不是代码本身，而是系统因此拥有了一张明确的运营决策表。

## 9. 智能体循环必须有明确的停止条件

OpenAI 指南里的另一个实践建议也很值得形式化：run loop 必须有清楚的 stop conditions。[^openai-practical]

好的 runtime 结束 run，不是因为“模型看起来安静下来了”，而是因为明确原因：

- 已经得到最终的结构化结果；
- 不再需要 tool calls；
- 出现不可恢复的错误；
- 达到步骤数或预算上限；
- 触发 approval boundary，需要人接手。

这听起来很乏味，但正是这些规则防止智能体滑进无穷 planning、无意义 retries，或者装饰性的 tool hops。

## 10. 幂等键必须成为协议的一部分

如果某个写工具“支持幂等性”只停留在口头上，而 key：

- 不是必填；
- 在不同层生成方式不一致；
- 在重试路径中丢失；
- 没有被记录到日志，

那它几乎就不算真正的幂等性。

好的实践是：

- 在工作流或动作边界上生成 key；
- 贯穿整个执行路径传递它；
- 在审计轨迹里记录它；
- 用它做对账和调查。

## 11. 常见错误

这些问题非常典型：

- 重试被打在不该重试的错误上；
- 未知结果被当成普通失败；
- 速率限制只放在入口，不放在工具上；
- 回滚被承诺了，但实际上不存在；
- 幂等键在规划器和适配器之间丢失；
- 智能体在重复尝试上被给了太多自由度。

这都说明执行层还没有长成生产级失败模型。

## 12. 现在就该做什么

先过一遍这份短清单，把所有回答为“否”的地方单独记下来：

- 写工具是否有明确的幂等策略？
- 系统是否区分 `retryable_failure` 和 `side_effect_unknown`？
- 重试是否绑定在策略上，而不是通用助手？
- 是否有每个工具或每个租户的速率限制？
- 你是否清楚每个危险动作的回滚边界？
- 运行时能否做对账，而不是盲重试？
- 追踪和审计日志中能否看到幂等键？

如果连续几个答案都是否，那下一次集成不稳定时，几乎一定会变成重复写入、噪音或手工事故排查。

## 13. 下一步做什么

第四部分到这里已经把基础执行层收束起来了：契约、沙箱、能力传输，以及副作用纪律。接下来就很自然地进入整个智能体系统层面的可靠性和可观测性。

- [第 11 章：追踪、Span 与结构化事件](../part-v/chapter-11.zh.md)
- [第 9 章：沙箱执行与 MCP 作为集成契约](chapter-9.zh.md)
- [第四部分：工具与执行](index.zh.md)
- [参考来源](../../appendix/sources.zh.md)

[^openai-practical]: [OpenAI, A practical guide to building agents (PDF)](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
