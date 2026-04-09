# 实践篇：MCP 用于 Tools，A2A 用于 Agents

很多团队会过早把两类问题混在一起：

- 如何连接 tools 和 external systems；
- 如何让多个 agents 相互协作。

于是 `MCP` 和 `A2A` 看起来就像可以互换的东西。实际上，它们属于不同的架构层级。

## 1. 一条最短规则

如果要最短版本：

- `MCP` 用于连接 tools、resources 和 adapters；
- `A2A` 用于 agents 之间交换任务、上下文与结果。

换句话说，一个协议主要解决 **agent-to-tool**，另一个协议主要解决 **agent-to-agent**。[^google-mcp-a2a][^google-multiagent]

## 2. 什么情况下你几乎一定需要 MCP

如果你有一个或多个外部 capability 需要被系统化接入，`MCP` 很自然：

- 文档搜索；
- CRM；
- helpdesk；
- internal APIs；
- 文件资源；
- 知识库；
- 执行沙箱。

这时你的主要目标不是“构建一个 agent 社会”，而是：

- 标准化 contract；
- 把 adapters 从 core runtime 中分离出去；
- 简化 policy checks；
- 集中处理 logging、auth 和 isolation。

这正是 `MCP` 最合适的位置。

## 3. 什么情况下你才真的需要 A2A

当系统里已经不只是 tools，而是出现了真正独立的 agents，并且它们各自承担不同职责时，`A2A` 才合理：

- coordinator；
- researcher；
- analyst；
- executor；
- domain specialist。

这些 agents 需要：

- 相互分发任务；
- 委派工作；
- 交换状态；
- 返回的不是 tool payload，而是另一个 agent 的工作结果。

也就是说，`A2A` 出现的前提不是“我还想再接一个 adapter”，而是系统里已经存在真实的 agent boundaries。

## 4. 典型错误：过早做 multi-agent

实践里最常见的混淆往往是这样：

1. 团队现在只有一个 runtime。
2. 需要接入三套系统。
3. 团队没有先做 capability contracts，而是直接开始设计 multi-agent orchestration。

这几乎总是额外复杂度。

如果系统里还没有真正需要拆分 agent responsibility 的理由，那么：

- tools 更适合通过 `MCP` 接入；
- orchestration 更适合留在一个 runtime 里；
- multi-agent coordination 最好先不要过早引入。

一个很好用的 practical rule 是：**如果这个实体不会独立做决策，也没有独立的 operational role，那它大概率还不是 agent，而只是 capability**。

## 4.1. 当前 multi-agent reliability research 更多是在强化谨慎态度

这里还值得补上一点。最新的 multi-agent reliability 研究，目前并没有给出足够强的理由，支持团队默认把 runtime 提前做得更复杂。相反，它更清楚地展示了：一旦系统在没有明确必要性的前提下被拆开，coordination failures、verification gaps 和 ambiguity 会迅速增长。

所以更实际的解读应该是：

- research 并不是在说“多建一些 agents”；
- research 更像是在说“如果你已经决定做 multi-agent，就必须有明确 contracts、verification loops 和可诊断的 handoffs”；
- 当前 best practice 依然是 `single-agent first`。

因此，引入 `A2A` 的理由不应该只是“架构上看起来更漂亮”，而应该是系统里确实已经存在无法再诚实描述成 tools 的独立 operational roles。

## 4.2. 多个 agents 的一致意见不等于独立验证

即便多个 agents 得出了相似结论，也不代表系统已经获得了真正独立的 verification signal。

常见问题通常包括：

- agents 看到的是同一份 contaminated context；
- reasoning paths 过于相似；
- manager agent 在无形中把 downstream agents 推向预期答案；
- consensus 看起来很有说服力，但其实建立在同一个 bad assumption 上。

所以 multi-agent agreement 更适合作为一种 signal，而不是 correctness proof。

## 5. Decision table

| 问题 | 更像 `MCP` | 更像 `A2A` |
| --- | --- | --- |
| 你需要连接 external API 或 resource 吗？ | 是 | 否 |
| 你需要 tool 的 typed contract 吗？ | 是 | 否 |
| 这里是否存在独立 agent，并且有自己的 role 和 lifecycle？ | 否 | 是 |
| 你需要 agents 之间 delegation 吗？ | 否 | 是 |
| 你需要隔离 adapter behavior 和 policy path 吗？ | 是 | 有时 |
| 你需要把任务发给另一个 agent runtime 吗？ | 否 | 是 |

## 6. 在成熟架构里它们长什么样

在成熟平台中，这两者通常不是竞争关系，而是位于不同层次。

<div class="diagram-card">
<p>MCP 和 A2A 是互补关系，不是替代关系</p>

``` mermaid
flowchart LR
    A["Coordinator agent"] --> B["A2A handoff"]
    B --> C["Specialist agent"]
    A --> D["MCP client"]
    C --> E["MCP client"]
    D --> F["Tool / resource server"]
    E --> G["Tool / resource server"]
```

</div>

健康的模式通常是：

- agent 通过 `MCP` 使用 tools；
- agent 通过 `A2A` 与另一个 agent 协作；
- policy 和 audit 要覆盖这两个方向。

## 7. 什么情况下不要用 A2A

下面这些都是危险信号：

- 你只是想把第二个 agent 当成 API wrapper；
- 第二个 agent 没有独立的 policy surface；
- 它没有独立的 operational identity；
- 用 capability contract 就能更简单地描述；
- 并行化与 specialization 并没有带来明确价值。

在这些情况下，继续使用 `MCP`，甚至普通的 gateway/adapter layer，通常更合理。

## 8. 一个最小 code sketch

下面这个极简示例，展示的是思维方式差异：

```python
def call_tool_via_mcp(tool_name: str, payload: dict) -> dict:
    return {"kind": "tool_result", "tool": tool_name, "payload": payload}


def delegate_via_a2a(agent_name: str, task: dict) -> dict:
    return {"kind": "agent_result", "agent": agent_name, "task": task}
```

重点不在代码本身，而在交互语义：

- tool call 返回的是 capability result；
- A2A handoff 返回的是另一个 agent 的工作结果。

这两者的 operational semantics 不一样，最好不要混在一起。

## 9. 实用检查清单

如果你拿不准，就问自己：

- 我需要的是一个新 agent，还是一个新 capability？
- 这个实体是否拥有自己的 role、policy surface 和 lifecycle？
- 这是 delegation problem，还是 integration problem？
- 我能不能解释为什么这里 `MCP` 不够用？
- 我是不是在真正需要之前，就过早做 multi-agent topology？

如果这些问题都答得不太稳，通常更安全的选择是先用 `MCP`，而不是 `A2A`。

## 10. 接下来读什么

- [第四部分：工具与执行](index.zh.md)
- [第 9 章：沙箱执行与 MCP 作为集成契约](chapter-9.zh.md)
- [第 10 章：幂等性、重试、速率限制与回滚边界](chapter-10.zh.md)
- [研究前沿：记忆、可观测性与多智能体可靠性](../../appendix/research-frontier.zh.md)
- [参考来源](../../appendix/sources.zh.md)

[^google-mcp-a2a]: [Google Cloud, Building Connected Agents with MCP and A2A](https://cloud.google.com/blog/topics/developers-practitioners/building-connected-agents-with-mcp-and-a2a)
[^google-multiagent]: [Google Cloud Architecture Center, Multi-agent AI system in Google Cloud](https://docs.cloud.google.com/architecture/multiagent-ai-system)
