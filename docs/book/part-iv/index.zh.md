# 第四部分：工具与执行

到这里为止，我们已经为同一个支持智能体搭好了三个重要层次：

- 平台架构；
- 安全边界；
- 记忆与检索纪律。

现在该进入真正的执行层了，也就是智能体不再只是“聪明的文本”，而是开始真正做事：查询状态、创建工单、拉人介入，或者安全停下来的地方。

最贵的问题通常正是在这里出现：

- 错误的工具调用；
- 意外的副作用；
- 不稳定的集成；
- 缺少幂等保护的重复操作；
- 对外部系统过于宽松的访问。

## 这一部分解决什么问题

这一部分会拆解执行层应该如何设计，让智能体不是直接伸手去碰外部世界，而是通过清晰的契约、限制和安全网关来工作。

!!! info "这一部分的快速路线"
    如果你想快速读完关键部分，可以这样走：

    - [第 8 章](chapter-8.zh.md)：先看 runtime 怎样选择下一步和 capability；
    - [第 9 章](chapter-9.zh.md)：再看这个 capability 怎样经过 sandbox 与 contract layer；
    - [第 10 章](chapter-10.zh.md)：最后固定 execution 怎样处理 retries、timeouts 和不确定的 side effects。

    这三章合在一起，才构成一个可以被当作 production layer 讨论的 execution model，而不只是“智能体会调工具”。

## 本部分内容

- [第 8 章：执行模型与工具目录](chapter-8.zh.md)
- [第 9 章：沙箱执行与 MCP 作为集成契约](chapter-9.zh.md)
  这一章继续同一个 support 场景，讲的是智能体已经准备碰到外部系统，而平台必须决定 transport、sandbox 和 execution boundary 的那一刻。
- [实践篇：MCP 用于工具，A2A 用于智能体](practical-mcp-a2a.zh.md)
- [第 10 章：幂等性、重试、速率限制与回滚边界](chapter-10.zh.md)

## 这一部分之后去哪里

这一部分之后，下一步自然就是 [第五部分](../part-v/index.zh.md)：看这套 execution model 在生产里是否真的健康，怎样为它设置 SLO，以及怎样把退化挡在 rollout 之外。
