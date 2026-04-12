# 实践篇：Manager Pattern vs Handoffs

## 1. 为什么这个选择很重要

团队一旦开始讨论 multi-agent，几乎总会出现同样的诱惑：

- 一个 agent 负责规划；
- 一个负责搜索；
- 第三个负责写；
- 第四个负责审查；
- 图画出来非常好看。

问题是，好看的图和稳定的系统并不是一回事。

在实践里，一个最有价值的问题通常是：

> 这里到底该用 manager pattern，还是 handoffs？

这不是审美问题，而是下面这些问题：

- 谁持有全局上下文；
- 下一步责任到底住在哪里；
- blast radius 怎么控制；
- 以后故障怎么调查。

OpenAI 的实用指南在这里特别有价值，因为它提醒你不要默认把 multi-agent 浪漫化，而是先看清楚：协调到底住在哪里，责任又应该住在哪里。[^openai-practical]

## 2. 什么是 Manager Pattern

`manager pattern` 的意思是，你有一个中心 orchestrator，它：

- 持有整个 run 的目标；
- 决定调用哪个 specialist；
- 接收结果；
- 组装最终答案或下一步计划。

它很像“manager 把 specialists 当工具来调用”。

manager pattern 的优点：

- 控制点单一；
- 更容易统一管理 global policy；
- 更方便保留 audit trail；
- 更容易控制 budget 和 max steps。

缺点：

- manager 很容易长成 bottleneck；
- 太多上下文会堆到一个地方；
- 如果 routing logic 出错，整个系统都会变脆。

## 3. 什么是 Handoff Pattern

`handoff pattern` 的意思是，当前 agent 可以把控制权交给另一个 agent，而后者在一段时间内成为该任务阶段的主要负责人。

它更像“责任被交给下一个角色”。

handoffs 的优点：

- 角色和 ownership 分得更清楚；
- 更容易做上下文隔离；
- 更容易做 domain-specialized behavior；
- 不容易把一个中央 orchestrator 压垮。

缺点：

- 更难看清全局 run；
- 更难形成统一 audit narrative；
- handoff boundary 必须设计得很仔细；
- state、intent 和 constraints 在转交时更容易丢。

## 4. 最有用的实用原则

简短地说：

- 当你需要一个统一协调中心时，`manager pattern` 更合适；
- 当任务天然在不同角色或领域之间流转时，`handoffs` 更合适。

所以真正的问题不是“哪个更现代”，而是“责任应该住在哪里”。

## 5. 什么时候 Manager Pattern 往往更合适

manager pattern 通常在这些情况下很好用：

- 任务长度短到中等；
- 需要统一 budget control；
- 各个子任务用到的 tools 和 policy 基本相同；
- 团队想要更强的 explainability；
- 有一个主要 runtime owner。

典型例子：

- support triage；
- 最终只需要一个统一答案的 research assistant；
- 调用多个 read-heavy capabilities 的 internal copilot；
- specialist agents 本质上更像 typed tools 的场景。

在这些地方，manager pattern 往往是最无聊、也最正确的答案。

## 6. 什么时候 Handoffs 更好

handoffs 通常在这些情况下更有优势：

- 任务真的跨越了不同 domain boundaries；
- 每个角色都需要自己的上下文和 guardrails；
- ownership 已经分散到不同团队；
- 有必要显著缩小当前 agent 的认知范围；
- 下一阶段更像责任转移，而不是 helper 调用。

典型例子：

- sales qualification -> solution agent -> legal review agent；
- incident intake -> security investigation -> remediation coordinator；
- 由不同 business units 拥有的 onboarding 流程。

这里 handoff 往往比一个假装什么都懂的 central manager 更自然。

## 7. 常见错误

这两种模式都有自己的典型失败方式。

manager pattern 常见问题：

- manager 扛了太多上下文；
- specialist agents 薄到几乎没有意义；
- routing 藏在 prompt 里，而不是显式 policy；
- central orchestrator 变成 single point of confusion。

handoffs 常见问题：

- constraints 和 intent 在转交时丢失；
- 下一个 agent 拿到的 state 过少或过多；
- 最终结果到底谁负责变得不清楚；
- trace 变得断裂而难读。

所以关键不是“哪个模式更强”，而是“哪个模式你能平稳运维”。

## 8. 一个简单的 Decision Table

下面这个表很适合作为起点。

| 场景 | 通常更合适的选择 |
| --- | --- |
| 需要统一控制 steps、cost 和 policy | `manager pattern` |
| 角色和领域天然分离 | `handoffs` |
| specialist 更像 capability tool | `manager pattern` |
| 下一个参与者需要自己的 context boundary | `handoffs` |
| 更看重统一 audit story | `manager pattern` |
| 更看重 role-specific agent 的局部自治 | `handoffs` |

这张表不能替代设计，但能很好地去掉不少多余浪漫主义。

## 9. 如何避免过早走错

通常最健康的路线是：

1. 先 single-agent loop；
2. 如果需要协调多个 specialist path，再进入 manager pattern；
3. 只有当真实 domain boundaries 已经出现时，再走向 handoffs。

这不是教条，而是防止过早复杂化的好方法。

## 10. 代码草图：Manager Pattern

```python
def run_manager(task: str, specialists: dict[str, callable]) -> dict:
    plan = ["research", "draft", "review"]
    results: dict[str, dict] = {}

    for step in plan:
        worker = specialists[step]
        results[step] = worker(task=task, prior_results=results)

    return {"status": "success", "results": results}
```

这里的重点不是 manager 要“无限思考”，而是它持有计划、调用 specialists，并把结果重新收拢起来。

## 11. 代码草图：Handoff Pattern

```python
def handoff(state: dict, next_agent: callable) -> dict:
    transfer_packet = {
        "goal": state["goal"],
        "constraints": state["constraints"],
        "relevant_context": state["relevant_context"],
    }
    return next_agent(transfer_packet)
```

关键不在调用本身，而在于 handoff 传递的应该是精心整理过的 transfer packet，而不是一整团混乱 state。

## 12. 对安全最重要的是什么

如果你用 manager pattern，重点检查：

- manager 会不会拿到过宽的权限；
- 它会不会“替所有人”绕过 approval boundary；
- 它会不会变成所有 tenant context 泄漏的中心点。

如果你用 handoffs，重点检查：

- policy constraints 在转交后是否还保留；
- risk classification 会不会丢；
- untrusted context 会不会不经标记就传给下一个 agent；
- trace 里能不能看清是谁接管了控制权。

也就是说，这里的安全不是“叠加在 orchestration 上面”的东西，而是 orchestration semantics 本身的一部分。

## 13. 现在就该做什么

先过一遍这份短清单，把所有回答为 “no” 的地方单独记下来：

- 谁拥有全局 run goal？
- 谁对 final outcome 负责？
- budget control 住在哪里？
- stop conditions 住在哪里？
- traces 能不能解释任务为什么从一个 agent 交给另一个？
- 你是不是太早走向了 handoffs，而其实 manager pattern 更简单？
- manager 有没有变成一个什么都做的中央怪物？

如果这些答案都很模糊，说明模式还没真正架构化成熟。

## 14. 下一步做什么

- [实践篇：Instructions、Routines 与 Prompt Templates](practical-routines.zh.md)
- [第 2 章：安全智能体的参考架构](chapter-2.zh.md)
- [第四部分：工具与执行](../part-iv/index.zh.md)
- [参考来源](../../appendix/sources.zh.md)

[^openai-practical]: [OpenAI, A practical guide to building agents (PDF)](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
