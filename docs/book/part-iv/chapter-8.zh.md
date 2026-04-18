# 第 8 章：执行模型与工具目录

## 1. 继续看同一个支持场景，但这次进入 write path

继续沿用前几章的同一个场景。

用户写道：

> 我已经等了三天还没有开通访问权限。请检查状态，如果申请卡住了，就创建一个紧急工单。

乍一看，这个任务很简单：

- 智能体读取消息；
- 调用检查状态的工具；
- 如果申请确实卡住，再调用创建工单的工具；
- 返回答复。

在演示里，这几乎就够了。在生产环境里，最贵的错误恰恰从这里开始。

因为现在的问题已经不只是 **模型想做什么**。真正的问题是：

- 它究竟被允许调用哪些工具；
- 在什么 tenant scope 下才允许；
- 哪些参数才算有效；
- read 和 write 操作在哪里分开；
- 如果外部服务在 side effect 之后卡住，该怎么办；
- 事后怎么证明工单到底创建了一次还是两次。

所以，工具调用不能被设计成模型旁边的小 helper，而必须被设计成平台的 execution layer。

## 2. 智能体不应该直接接触工具

这里最有价值的工程习惯之一其实很朴素：智能体永远不应该直接获得真实集成的访问权限。

你需要的是一个执行层，它能够：

- 知道可用工具目录；
- 校验输入参数；
- 应用 policy checks；
- 区分 read 和 write 操作；
- 管理 retries、timeouts 和 idempotency；
- 发出 audit events。

对于同一个支持场景，这意味着模型不应该直接调用 helpdesk API 或 IAM service。它应该只和 execution layer 说话。

## 3. 一个请求如何穿过 execution layer

现在把同一个场景看成一条执行路径。

### 3.1. 先由模型提出一个 read tool

要判断申请是否卡住，智能体需要一个状态检查工具。这是 read path：

- 它不应该改变外部世界；
- 它需要正确的 tenant scope；
- 它应该返回干净、结构化的结果。

### 3.2. 然后系统再决定 write tool 是否被允许

如果状态显示申请确实卡住，下一步可能就是 `create_support_ticket`。但这已经进入 write path：

- 这里会产生 side effect；
- 可能需要 approval；
- 需要 idempotency key；
- 需要更严格的 audit trail。

### 3.3. 然后 execution layer 接手那些不体面的现实问题

也正是在这里，演示里很少出现的问题开始出现：

- helpdesk 在创建工单后超时；
- 工具只返回 partial success；
- 模型在 retry 后重复调用；
- 外部服务返回了意外的 payload；
- runtime 已经无法确定 side effect 是否真的发生。

这已经不是“tool calling”而已，而是执行纪律。

<div class="diagram-card">
<p>模型不应该直接与外部世界通信，而应该通过执行层</p>

``` mermaid
flowchart LR
    A["Prompt + policy context"] --> B["Model"]
    B --> C["Tool request"]
    C --> D["Execution layer"]
    D --> E["Catalog lookup"]
    D --> F["Policy / validation"]
    D --> G["Retry / timeout / idempotency"]
    G --> H["External system"]
    H --> D
    D --> I["Structured tool result"]
    I --> B
```

</div>

## 4. 工具目录是平台接口，不是随机函数的集合

如果你把目录看成“函数调用的文件夹”，它很快就会变成一个集成垃圾场。更有用的理解方式是：工具目录是执行层的公共接口。

在这个支持场景里，目录应该明确告诉你，智能体到底能做什么：

- `check_access_request_status`
- `get_user_profile`
- `create_support_ticket`
- `request_human_approval`

一个好的目录通常会保存：

- 稳定的工具名；
- 工具目的描述；
- 输入 schema；
- risk class；
- side-effect level；
- allowed callers 或 capabilities；
- timeout、retry policy 和 idempotency expectations。

这会让 execution layer 变得可检查：团队看到的不是“模型也许会调什么”，而是一个具体的平台契约。

## 4.1. 过大的工具目录会伤害选择质量，而不是扩大自由

另一个非常实际的问题会在目录变得过大时出现。

模型一次看到的 tools 越多：

- 它就要为工具描述消耗越多 prompt tokens；
- 那些彼此相似的 contracts 就会越长；
- 区分接近能力的难度也会越高；
- 选择阶段的注意力也会被稀释。

这也是为什么"干脆把所有工具都展示给模型"通常不是好主意。选择质量下降，不是因为模型"变笨了"，而是因为候选集合本身太嘈杂。

这里一个很实用的模式通常叫作 semantic tool filtering：

- 完整 registry 仍然保留在 platform layer；
- 但某一次 run 只会看到一个狭窄而相关的子集；
- 通常是 3 到 5 个 tools，而不是几十个。

这在 overlapping capabilities 上尤其重要，因为它们之间差异很细：多个 search tools、多个 write adapters、多个相似的 orchestration actions。

还有一个很有用的 practical rule：如果模型一开始看到的就是一个过于嘈杂的目录，那么 retries 并不能真正修复 tool selection 问题。

## 5. 必须区分 read tools 和 write tools

这看上去似乎很明显，但实践里很多系统几乎把它们当成同一类对象来描述。

对于同一个支持智能体，`check_access_request_status` 和 `create_support_ticket` 不是简单的两个工具，而是两种不同的风险类别。

`read tools` 通常：

- 风险更低；
- 更适合自动调用；
- 对 grounding 和 retrieval 更有帮助；
- 需要访问控制，但不一定总要 approval。

`write tools` 通常：

- 会产生 side effects；
- 需要更强的 validation；
- 必须有明确的 rollback boundaries；
- 经常需要 idempotency key 和 human approval。

如果 read 和 write operations 都被塞进一个模糊的“tool call”概念里，execution layer 很快就会失控。

### 5.1. 另一个有用的分类：data、action、orchestration

OpenAI 的实践指南里还有一个很有用的简化：tools 不只适合按 `read` 和 `write` 分，也适合按它们在系统中的角色来分。[^openai-practical]

- `data tools` 读取并返回上下文：状态检查、retrieval、CRM 读取；
- `action tools` 改变外部世界：创建工单、发送邮件、更新记录；
- `orchestration tools` 帮助 runtime 自身工作：请求 approval、handoff、调用 planner。

这两条分类轴可以一起使用：

- `data tools` 通常更接近 `read`；
- `action tools` 通常更接近 `write`；
- `orchestration tools` 可能两者都有，但它们有单独的 operational 含义。

Anthropic 的 workflow taxonomy 在这里又补上了一层很有用的纪律。[^anthropic] 目录不应该只告诉模型“有哪些工具存在”，还应该说明“这些工具在哪些 orchestration patterns 里才是安全可用的”。

例如：

- `data tool` 也许适合放进 `routing`、`prompt chaining` 或 `parallelization`；
- `write action tool` 也许只适合出现在 approval interrupt 之后，或者只适合放进边界非常紧的 workflow；
- `orchestration tool`，比如 `request_human_approval` 或 `handoff_to_specialist`，会直接改变 execution graph，因此需要更严格的 trace 和 ownership rules；
- `orchestrator-workers` 模式可能需要一个显式的 worker-safe catalog 子集，而不是把父级全部 tool surface 都暴露出去。

所以，成熟的 tool catalog 最终不会只是一个“可调用函数列表”。它会变成 execution patterns 与允许 side effects 之间的 boundary contract。

## 6. 工具契约应该无聊而严格

Agent 系统里最糟糕的习惯之一，就是允许模型自己即兴决定调用格式。

在好的设计里，一个工具应该拥有明确契约：

- 清晰的必填字段；
- 可理解的 enum 和约束；
- 正常的错误消息；
- 显式的返回格式；
- timeout 或 duplicate request 时可预测的行为。

对于这个支持场景，它可以长这样：

```yaml
tools:
  check_access_request_status:
    description: "Read the current status of an access request"
    kind: "read"
    risk: "low"
    timeout_seconds: 10
    input_schema:
      required: ["request_id", "tenant_id"]
      properties:
        request_id: {type: string}
        tenant_id: {type: string}

  create_support_ticket:
    description: "Create a support ticket in the internal helpdesk"
    kind: "write"
    risk: "medium"
    idempotent: true
    timeout_seconds: 15
    input_schema:
      required: ["title", "queue", "requester_id", "tenant_id", "idempotency_key"]
      properties:
        title: {type: string, maxLength: 200}
        queue: {type: string, enum: ["support", "security", "ops"]}
        requester_id: {type: string}
        tenant_id: {type: string}
        idempotency_key: {type: string}
        description: {type: string}
```

它看起来很普通。很好。契约层越少魔法，工具层就越稳定。

## 7. Execution layer 应该统一错误语义

另一个非常常见的问题是：每个外部服务都用自己的风格返回错误，而智能体几乎原样接收。

在同一个支持场景里，这很容易变成一锅粥：

- IAM service 返回 HTTP 500；
- helpdesk 回了 `"created": true`，却没有 `ticket_id`；
- 老旧适配器返回 HTML；
- timeout 发生在 side effect 之后；
- 下游 API 返回空 body。

Execution layer 应该把这些统一成可用的 outcome：

- `success`
- `retryable_failure`
- `validation_failure`
- `permission_denied`
- `side_effect_unknown`

这会大幅提高 explainability，也让智能体能做出更成熟的动作：重试、请求审批、升级给人、或者安全停止。

## 8. Idempotency 和 retries 不能事后再补

几乎所有真实集成最终都会给你至少一种不愉快场景：

- side effect 已经发生后才 timeout；
- retry 之后重复调用；
- partial success；
- 两个 run 之间出现 race condition；
- 外部服务响应时间远超预期。

如果 idempotency 没有内建进执行设计，智能体很快就会做出那些在普通系统里已经很难排查的重复动作。

对于这个支持场景，一个很实际的规则是：任何会创建工单、更新记录或发送消息的 write tool，在第一次 production rollout 之前都必须有明确的 idempotency strategy。

## 9. execution layer 的实用规则

如果要把 production 里真正有用的规则压缩成一小组，通常就是这些：

1. 每个工具都应该有 owner、schema、risk class 和 contract lifecycle。
2. Read path 和 write path 必须在第一次 rollout 之前就分开，而不是等第一次 incident 之后再补。
3. 每个 write tool 在接触真实流量前都必须有 idempotency strategy。
4. 所有 tool outcomes 都应该先被规范化，再返回给模型。
5. 只要 side effect 可能已经发生，停下来通常比盲目 retry 更安全。

## 10. 团队最常做错什么

Execution layer 往往会在同样的地方出问题：

- 直接给模型外部 API 的访问权；
- 把 read tools 和 write tools 混成一个模糊类别；
- 让 tools 在不同 orchestration patterns 之间随意泄漏，却没有说明 routing、parallelization、approval interrupts 和 worker delegation 到底哪些才被允许；
- 把 retries 藏在 adapter 深处，却没有 audit trail 和 idempotency；
- 把原始 payload 直接返回给模型，而不是给出规范化结果；
- 不给 catalog layer 设 owner 和 deprecation policy。

## 11. 一个简单的 execution layer skeleton

下面不是 production runtime，而是一个 skeleton，用来展示责任如何拆分：lookup、validate、execute、normalize result。

```python
from dataclasses import dataclass


@dataclass
class ToolSpec:
    name: str
    kind: str
    timeout_seconds: int
    idempotent: bool


@dataclass
class ToolResult:
    status: str
    payload: dict


def execute_tool(spec: ToolSpec, args: dict) -> ToolResult:
    if spec.kind not in {"read", "write"}:
        return ToolResult(status="validation_failure", payload={"reason": "unknown tool kind"})

    if spec.kind == "write" and "idempotency_key" not in args:
        return ToolResult(status="validation_failure", payload={"reason": "missing idempotency key"})

    # In production this call would go through policy checks, a gateway, and typed adapters.
    return ToolResult(status="success", payload={"tool": spec.name})
```

关键不在于这个例子有多复杂，而在于工具不是直接由模型决定后立刻执行的。

## 12. Tool results 也需要设计

如果 tool result 太原始，模型就又重新获得了危险的即兴空间。

好的 result 应该：

- 简短；
- 结构化；
- 不夹带无关技术噪音；
- 具备 machine-readable status；
- 对不确定性保持诚实。

糟糕的 result 则会：

- 把完整外部 payload 整段扔回来；
- 混杂 user-facing text 和系统细节；
- 无法区分“没找到”和“系统挂了”；
- 不说明 side effect 是否真的发生。

## 13. Tool catalog 应该缓慢演化

如果 tools 每天都变、没有兼容性和版本管理，智能体系统很快就会像是在对接一个极不稳定的 private API。

所以 catalog layer 很适合具备这些习惯：

- versioned contracts；
- deprecation policy；
- 每个工具都有 owner；
- schema 和 result shape 的测试；
- 新 write tools 引入前做 capability review。

这是无聊的平台工作，而不是浪漫的即兴发挥。正因为如此，它才可靠。

## 14. 给 tool layer 做一次快速成熟度测试

团队不应该只因为 tools 已经能被调用，就把 execution layer 叫做成熟。

更强的标准应该是这样：

- 目录是显式的，并且有人负责；
- read、write 和 orchestration 语义可以被清楚区分；
- idempotency 是在事故发生前设计好的；
- 不确定性不会被伪装成 success；
- 模型不会变成直接对接外部集成的表面。

如果只缺一两项，系统也许还能运行。但如果大多数都缺失，那这个 tool layer 仍然只是原型包装层。

## 15. 读完这一章后先做什么

如果你想快速检查 execution layer，可以用这个短清单：

1. 你有真正的 tool catalog，而不是一堆函数吗？
2. read 和 write tools 分开了吗？
3. 参数有 schema validation 吗？
4. 外部错误被统一了吗？
5. timeouts、retries 和 idempotency 都考虑了吗？
6. 能看出 side effect 是否发生了吗？
7. 每个工具都有 owner 和 contract lifecycle 吗？

如果连续几个答案都是否，那说明你的智能体虽然已经能调用 tools，但 execution model 还远未成熟。

## 16. 接下来读什么

这一部分接下来的自然主题是：sandbox execution、MCP 作为集成契约，以及 retries 和 rollback boundaries 的规则。也正是在那里，你会看到同一个支持智能体并不只是“会调工具”，而是通过成熟执行层去调工具。

- [第 7 章：检索、压缩与后台更新](../part-iii/chapter-7.zh.md)
- [第四部分：工具与执行](index.zh.md)
- [参考来源](../../appendix/sources.zh.md)

[^openai-practical]: [OpenAI, A practical guide to building agents (PDF)](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
