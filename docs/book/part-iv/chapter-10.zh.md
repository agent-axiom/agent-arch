# 第 10 章：幂等性、重试、速率限制与回滚边界

## 1. 为什么最贵的失败常常看起来只是“我们又调了一次”

当智能体系统开始执行真实动作时，最糟糕的事故来源之一其实非常朴素：重复调用。

从外面看，它通常显得很无害：

- 请求卡住了；
- runtime 决定重试；
- integration 不稳定；
- 智能体试图“帮忙”，于是把动作又发了一次。

但在现实里，这意味着：

- 两张一模一样的工单；
- 给同一个客户发两封邮件；
- 重复收费；
- CRM 被重复写入；
- 同一个对象被改了好几次。

所以问题不在于模型的推理本身，而在于 execution layer 还不会安全地生活在部分失败的世界里。

## 2. Idempotency 不是 nice-to-have，而是基本保险

Idempotency 回答的是一个极其简单的问题：“如果系统误把这次调用重复执行了一遍，会发生什么？”

对于 write operations，一个好的答案应该是二选一：

- 重复调用不会改变最终结果；
- 系统可以可靠识别重复请求，并避免再次产生 side effect。

如果没有这个性质，任何网络不稳定、timeout 或 run 之间的 race 都会变得非常昂贵。

## 3. 没有错误分类的 retry 只会放大混乱

一种非常糟糕的策略是：“请求失败了，那就再重试三次”。

在 production 中，这很危险，因为不同错误完全不是一回事：

- `validation_failure` 几乎从不该重试；
- `permission_denied` 不会因为多试几次就变好；
- `retryable_failure` 才可能需要 backoff；
- `side_effect_unknown` 需要谨慎，而不是盲目重复。

所以 retry policy 应该依赖 outcome class，而不是“再试试也许行”的情绪。

## 4. 最糟糕的状态是 `side_effect_unknown`

有一类失败尤其让人头痛：你已经不知道 side effect 到底有没有发生。

例如：

- 请求发给外部服务后超时；
- commit 之后连接断开；
- adapter 崩溃，确认没有落库；
- 外部 API 的响应让最终状态不清楚。

这正是 naive retry 最危险的场景。有时正确动作不是“重试”，而是：

- 到外部系统检查当前状态；
- 执行 reconciliation；
- 交给人处理；
- 停止 workflow 并明确记录这种不确定性。

## 5. Rate limits 也是 safety design 的一部分

如果团队只把 rate limits 当成性能问题，execution layer 就会低估它的架构意义。

实际上，rate limits 还用来避免：

- 一个 runaway agent 把外部系统打挂；
- 循环 planning 变成 tool call 雪崩；
- 高成本 capability 吃掉所有预算；
- retry storm 把 integration 打死。

所以 limit 不应该只存在于 whole service 层面，还应该出现在：

- per tool；
- per tenant；
- per workflow；
- per risk class。

## 6. Rollback boundary 必须提前定义

最危险的事情之一，就是在事故里才发现某个操作“其实根本无法回滚”。

对于每个 write capability，最好提前搞清楚：

- 这个动作能不能撤销；
- 这个动作能不能安全重复；
- point of no return 在哪里；
- 什么 compensating action 是允许的；
- 什么时候必须人工 reconciliation。

也就是说，rollback boundary 不是“以后再说”，它本身就是工具和 workflow contract 的一部分。

<div class="diagram-card">
<p>发生 side effect 之后，execution layer 必须区分 safe retry、reconcile 和 stop 路径</p>

``` mermaid
flowchart TD
    A["Tool request"] --> B["Execute write action"]
    B --> C{"Outcome known?"}
    C -->|Yes, success| D["Store result and continue"]
    C -->|Retryable failure| E["Retry with policy and backoff"]
    C -->|Unknown side effect| F["Reconcile or request human review"]
    C -->|Validation or permission failure| G["Stop and surface error"]
```

</div>

## 7. 好的 execution contract 会显式保存 operational semantics

仅仅知道输入 schema 和返回 shape 还不够。对危险操作来说，contract 还必须记录：

- 这个动作是否 idempotent；
- 是否必须有 idempotency key；
- 哪些错误是 retryable；
- retries 上限是多少；
- 频率限制是什么；
- unknown outcome 怎么处理；
- 是否存在 rollback 或 compensating action。

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

## 8. 一个简单的 retry decision 示例

下面不是 production policy engine，而是一个小 skeleton。它的目的就是说明：retry 应该依赖 outcome class，而不是普遍 reflex。

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

重要的不是代码本身，而是系统因此拥有了一张明确的 operational decision table。

## 9. Idempotency key 必须成为协议的一部分

如果某个 write tool “支持 idempotency” 只停留在口头上，而 key：

- 不是必填；
- 在不同层生成方式不一致；
- 在 retry path 中丢失；
- 没有被记录到日志，

那它几乎就不算真正的 idempotency。

好的实践是：

- 在 workflow 或 action boundary 上生成 key；
- 贯穿整个 execution path 传递它；
- 在 audit trail 里记录它；
- 用它做 reconciliation 和调查。

## 10. Execution reliability 最常见的崩坏点

这些问题非常典型：

- retries 被打在不该重试的错误上；
- unknown outcome 被当成普通 failure；
- rate limits 只放在入口，不放在 tools 上；
- rollback 被承诺了，但实际上不存在；
- idempotency key 在 planner 和 adapter 之间丢失；
- 智能体在重复尝试上被给了太多自由度。

这都说明 execution layer 还没有长成 production-grade 的 failure model。

## 11. 实用检查清单

如果你想快速检查 execution reliability，可以问：

- write tools 是否有明确的 idempotency strategy？
- 系统是否区分 `retryable_failure` 和 `side_effect_unknown`？
- retries 是否绑定在 policy 上，而不是通用 helper？
- 是否有 per-tool 或 per-tenant 的 rate limits？
- 你是否清楚每个危险动作的 rollback boundary？
- runtime 能否做 reconciliation，而不是盲重试？
- traces 和 audit logs 中能否看到 idempotency key？

如果连续几个答案都是否，那下一次 integration 不稳定时，几乎一定会变成重复写入、噪音或手工事故排查。

## 12. 接下来读什么

Part IV 到这里已经把基础 execution layer 收束起来了：contracts、sandbox、capability transport，以及 side effects discipline。接下来就很自然地进入整个 agent system 层面的 reliability 和 observability。

- [第 9 章：沙箱执行与 MCP 作为集成契约](chapter-9.zh.md)
- [第四部分：工具与执行](index.zh.md)
- [参考来源](../../appendix/sources.md)
