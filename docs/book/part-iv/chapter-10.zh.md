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

!!! example "贯穿案例：工单结果未知"
    在支持分诊案例里，最危险的时刻并不是推理错误，而是调用 `create_support_ticket` 后发生超时。如果 helpdesk 可能已经创建了工单，在没有幂等键的情况下重复调用，就会把一个客户请求变成两个事故。正确分支应该先用 correlation ID 查找工单，然后要么把找到的结果绑定回 trace，要么停止运行并请操作员确认状态。

**可靠性案例主线说明（Reliability case-spine note）：**重试（retries）、速率限制（rate limits）和回滚边界（rollback boundaries）应该用三个规范案例（canonical cases）来测试。支持分诊（Support triage）需要幂等键（idempotency keys）、重复工单检测（duplicate-ticket detection），以及重试（retry）之前的对账（reconciliation）。内部知识助手（Internal knowledge assistant）需要检索扇出（retrieval fan-out）的速率限制、新鲜度退避（freshness backoff），并禁止重复写入陈旧记忆（stale memory writes）。事故协调（Incident coordination）需要升级去重（escalation de-duplication）、通知节流（notification throttling）、事故状态变更（incident-state changes）的清晰回滚边界（clear rollback boundary），以及 `side_effect_unknown` 时的人工确认（human confirmation）。

### 4.1. 恢复分支也应该被显式设计

最近关于工具失败案例的研究还强化了另一点：恢复路径不应该只是执行层的临场即兴发挥。

最好预先定义：

- 哪些结果类别应该进入对账，而不是重试；
- 哪些部分成功应该生成后续任务；
- 恢复本身在什么情况下也需要审批；
- 哪些分支必须进入 [评测模式（eval schema）](../../appendix/eval-schema.zh.md)；
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

### 5.1. 共享配额需要共享冷却，而不仅是局部退避

多个独立运行即使各自遵守退避，也可能加重共享同一供应商或网关配额的其他运行的过载。Cloudflare 的 CryptoLabe 使用一个全局 Durable Object，调节所有模型请求，包括重试；某次扫描遇到限流时，所有扫描共享冷却期。[^cloudflare-cryptolabe]

本书建议的契约是：**首次请求或重试 → 有界共享队列 → 调节器许可 → 发送**。协调范围应对应真实配额池：供应商/网关、账号或项目、模型/模型组及区域——仅采用实际决定限额的维度。不同凭据可能消耗同一配额，因此每进程一个限流器并不足够。独立配额池不应一起暂停。使用安全的配额池引用，不保存秘密值。

确认是临时限流后，适配器更新共享的 `cooldown_until`，不能缩短已有暂停；遵守有效的 `Retry-After`，缺少该信息时按策略进行有界退避。冷却结束后，以并发限制和随机抖动逐步放行，不能同时释放整个队列。暂停不会取消已经发送的请求。队列应限制长度，支持截止时间与取消，并在运行/租户间公平分配；每次运行自身的尝试次数和费用预算仍有效。

所有实际网络尝试都必须经过该路径，包括 SDK/workflow 隐藏重试，以及使用相同配额池的降级路径。应将内置重试接入调节器，或关闭它们并由单一组件负责重试。请求速率控制不能代替令牌量、并发数、费用预算或幂等性控制。

并非每个 `429` 都是临时过载：费用上限耗尽需要明确的预算决策，而不是等待后继续消耗。根据供应商文档中的响应分类；原因未知时，限制后续尝试并升级处理。共享冷却不能重置任务截止时间。这是建议契约，不是参考运行时已实现的功能；协调器位置和恢复见[第 16 章](../part-vii/chapter-16.zh.md)。

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

### 7.1. Durable step 不等于 progress reporting

Cloudflare Agents SDK 很有用地区分了留在 agent 内部的工作，以及更适合放进 Workflows 的工作：agent 负责实时通信和 interaction boundary state，workflow 负责 durable multi-step execution、automatic retries、等待外部事件和恢复。[^cloudflare-workflows]

对本章来说，这是一条可靠性边界。**Durable step** 应该有稳定标识符、幂等键、replay policy、retry policy、timeout 和 audit linkage。**Progress reporting**——WebSocket 消息、streaming update 或 UI state——不应该成为事实来源。如果用户已经看到了进度，但 durable step 没有提交，运行时应该从最后一个 durable checkpoint 恢复，而不是相信用户界面里最后显示的消息。

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

### 付费调用：重试请求不等于重试付款

付费工具至少有三个独立结果：操作是否执行、支付是否结算、结果是否送达。Monetization Gateway 文档给出的顺序是：验证授权 → 源站执行并准备响应 → 结算 → 向买方交付。[^cloudflare-paid-call] 因此响应丢失不能证明未扣款，结算失败也不能证明源站未执行任何操作。

本书建议：关联业务操作、请求及支付授权标识，但分别记录 `payment_state`、`execution_state` 和 `result_state`，明确保留 `unknown`。未签名的 HTTP 402 是付款条件，不是付款许可。使用首次获准签名重发请求是协议步骤；超时后的重试则需要核对。在检查结算、操作状态及已保存结果的获取方式前，不应签发新的支付授权或重复业务动作。

支付幂等不意味着工具幂等。使用双方支持的键和核对渠道；任意添加一个请求头不会自动产生去重。若集成无法确定结果，应保留不确定性并升级处理，而非自动再次扣款。退款、业务补偿和结果重发是不同操作，分别需要权限。这是架构建议，不是 x402 或 Cloudflare 的恰好一次保证。

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
[^cloudflare-workflows]: [Cloudflare Agents SDK, Workflows](https://developers.cloudflare.com/agents/concepts/workflows/)

[^cloudflare-cryptolabe]: Cloudflare, [CryptoLabe：利用 AI 规划后量子迁移](https://blog.cloudflare.com/ai-driven-cryptography-discovery/), 2026-09-29.

[^cloudflare-paid-call]: Cloudflare, [Monetization Gateway beta：HTTP 402 付费调用](https://blog.cloudflare.com/monetization-gateway-beta/); [x402 协议](https://developers.cloudflare.com/monetization-gateway/x402/), 2026-09-30.
