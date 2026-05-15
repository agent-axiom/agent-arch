# 第四部分：工具与执行

到这里为止，我们已经为同一个支持智能体搭好了三个重要层次：

- 平台架构；
- 安全边界；
- 记忆与检索纪律。

现在该进入真正的执行层了，也就是智能体不再只是“聪明的文本”，而是开始真正做事：查询状态、创建工单、拉人介入，或者安全停下来的地方。

<div class="book-cover" markdown="1">

![工具与执行部分封面](../../assets/images/part-iv.png)

</div>

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

    - [第 8 章](chapter-8.zh.md)：先看运行时怎样选择下一步和能力；
    - [第 9 章](chapter-9.zh.md)：再看这个能力怎样经过沙箱与契约层；
    - [第 10 章](chapter-10.zh.md)：最后固定执行怎样处理重试、超时和不确定的副作用。

    这三章合在一起，才构成一个可以被当作生产层讨论的执行模型，而不只是“智能体会调工具”。

!!! note "Part IV canonical case routes"
    在 execution layer 中，三个 canonical cases 会落到不同 tool boundaries 上。**Support triage** 检查 ticket-write capability、approval gate、idempotency key 和 duplicate-ticket recovery。**Internal knowledge assistant** 检查 retrieval adapter、source attribution、tenant boundary 和 read-only MCP contract。**Incident coordination** 检查 escalation tool、notification side effects、incident state updates 和 rollback boundary。

## 本部分内容

- [第 8 章：执行模型与工具目录](chapter-8.zh.md)
- [第 9 章：沙箱执行与 MCP 作为集成契约](chapter-9.zh.md)
  这一章继续同一个支持场景，讲的是智能体已经准备碰到外部系统，而平台必须决定传输、沙箱和执行边界的那一刻。
- [实践篇：MCP 用于工具，A2A 用于智能体](practical-mcp-a2a.zh.md)
- [第 10 章：幂等性、重试、速率限制与回滚边界](chapter-10.zh.md)

## 这一部分之后去哪里

这一部分之后，下一步自然就是 [第五部分](../part-v/index.zh.md)：看这套执行模型在生产里是否真的健康，怎样为它设置 SLO，以及怎样把退化挡在发布之外。
