# 第 8 章：执行模型与工具目录

## 1. 为什么工具调用不只是“模型选了一个函数”

当智能体开始调用工具时，很多团队最初都会把它看成一个很简单的机制：

- 定义工具；
- 暴露给模型；
- 接收 function call；
- 执行动作。

这在演示里能工作。但在生产环境里，几乎总是不够。

工具调用不只是“模型想调用什么”，还涉及：

- 哪些动作本身就允许发生；
- 在什么上下文中才允许；
- 谁拥有调用契约；
- validation、重试和副作用在哪里处理；
- 部分失败时系统如何表现。

所以执行模型应该被设计成平台层，而不是 LLM API 外面的一层小 helper。

## 2. 智能体不应该直接接触工具

最有价值的架构习惯之一就是：智能体永远不应该直接获得真实集成的访问权限。

你需要的是一个执行层，它能够：

- 知道可用工具目录；
- 校验输入参数；
- 应用 policy checks；
- 区分 read 和 write 操作；
- 管理 retries、timeouts 和 idempotency；
- 发出 audit events。

这在工具会影响真实系统时尤其重要，比如工单、CRM、数据库、文件、消息和支付。

## 3. 工具目录是平台接口，不是随机函数的目录

如果你把目录看成“调用函数的文件夹”，它很快就会变成一个集成垃圾场。更有用的理解方式是：工具目录是执行层的公共接口。

一个好的工具目录通常会保存：

- 稳定的 tool name；
- 目的描述；
- input schema；
- risk class；
- side-effect level；
- allowed callers 或 capabilities；
- timeout、retry policy 和 idempotency expectations。

<div class="diagram-card">
<p>模型不应该直接和外部世界通信，而应该通过 execution layer</p>

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

## 4. Read tools 和 write tools 不是一回事

这看上去似乎很明显，但实践里很多系统几乎把它们当成同一类对象来描述。

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

## 5. 工具契约应该无聊而严格

Agent 系统里最糟糕的习惯之一，就是允许模型自己即兴决定调用格式。

在好的设计里，一个工具应该拥有明确契约：

- 清晰的必填字段；
- 可理解的 enum 和约束；
- 正常的错误消息；
- 显式的返回格式；
- timeout 或 duplicate request 时可预测的行为。

正常的工具 schema，远比一整屏“聪明”的描述更有价值。

```yaml
tools:
  create_ticket:
    description: "Create a support ticket in the internal helpdesk"
    kind: "write"
    risk: "medium"
    idempotent: true
    timeout_seconds: 15
    input_schema:
      required: ["title", "queue", "requester_id"]
      properties:
        title: {type: string, maxLength: 200}
        queue: {type: string, enum: ["support", "security", "ops"]}
        requester_id: {type: string}
        description: {type: string}
```

它看起来很普通。很好。契约层越少魔法，工具层就越稳定。

## 6. Execution layer 应该统一错误语义

另一个非常常见的问题是：每个外部服务都用自己的风格返回错误，而智能体几乎原样接收。

然后模型看到的就成了一锅粥：

- 某处是 HTTP 500；
- 某处是 `"failed": true`；
- 某处是 HTML 页面；
- 某处是 stack trace；
- 某处是空响应。

Execution layer 应该把这些统一成可用的 outcome：

- `success`
- `retryable_failure`
- `validation_failure`
- `permission_denied`
- `side_effect_unknown`

这会大幅提高 explainability，也让智能体能做出更成熟的动作：重试、请求审批、升级给人、或者安全停止。

## 7. Idempotency 和 retries 不能事后再补

几乎所有真实集成最终都会给你至少一种不愉快场景：

- side effect 已经发生后才 timeout；
- retry 之后重复调用；
- partial success；
- 多个 run 之间的 race condition；
- 外部服务响应时间远超预期。

如果 idempotency 没有内建进执行设计，智能体很快就会做出那些在普通系统里已经很难排查的重复动作。

## 8. 一个简单的 execution layer skeleton

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

## 9. Tool results 也需要设计

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

## 10. Tool catalog 应该缓慢演化

如果 tools 每天都变、没有兼容性和版本管理，智能体系统很快就会像是在对接一个极不稳定的 private API。

所以 catalog layer 很适合具备这些习惯：

- versioned contracts；
- deprecation policy；
- 每个工具都有 owner；
- schema 和 result shape 的测试；
- 新 write tools 引入前做 capability review。

这是无聊的平台工作，而不是浪漫的即兴发挥。正因为如此，它才可靠。

## 11. 实用检查清单

如果你想快速检查 execution layer，可以问：

- 你有真正的 tool catalog，而不是一堆函数吗？
- read 和 write tools 分开了吗？
- 参数有 schema validation 吗？
- 外部错误被统一了吗？
- timeouts、retries 和 idempotency 都考虑了吗？
- 能看出 side effect 是否发生了吗？
- 每个工具都有 owner 和 contract lifecycle 吗？

如果连续几个答案都是否，那说明你的智能体虽然已经能调用 tools，但 execution model 还远未成熟。

## 12. 接下来读什么

这一部分接下来的自然主题是：sandbox execution、MCP 作为集成契约，以及 retries 和 rollback boundaries 的规则。

- [第 7 章：检索、压缩与后台更新](../part-iii/chapter-7.md)
- [第四部分：工具与执行](index.zh.md)
- [参考来源](../../appendix/sources.md)
