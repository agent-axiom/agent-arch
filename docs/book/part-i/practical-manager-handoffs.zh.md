# 实践篇：Manager Pattern vs Handoffs

## 1. 为什么这个选择很重要

团队一旦开始讨论多智能体，几乎总会出现同样的诱惑：

- 一个智能体负责规划；
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
- 爆炸半径怎么控制；
- 以后故障怎么调查。

OpenAI 的实用指南在这里特别有价值，因为它提醒你不要默认把多智能体浪漫化，而是先看清楚：协调到底住在哪里，责任又应该住在哪里。[^openai-practical]

## 2. 什么是 Manager Pattern

`manager pattern` 的意思是，你有一个中心 orchestrator，它：

- 持有整个 run 的目标；
- 决定调用哪个 specialist；
- 接收结果；
- 组装最终答案或下一步计划。

它很像“管理器把专家当工具来调用”。

manager pattern 的优点：

- 控制点单一；
- 更容易统一管理全局策略；
- 更方便保留审计轨迹；
- 更容易控制预算和最大步骤数。

缺点：

- 管理器很容易长成瓶颈；
- 太多上下文会堆到一个地方；
- 如果路由逻辑出错，整个系统都会变脆。

## 3. 什么是 Handoff Pattern

`handoff pattern` 的意思是，当前智能体可以把控制权交给另一个智能体，而后者在一段时间内成为该任务阶段的主要负责人。

它更像“责任被交给下一个角色”。

handoffs 的优点：

- 角色和负责人机制分得更清楚；
- 更容易做上下文隔离；
- 更容易做领域专门化行为；
- 不容易把一个中央编排器压垮。

缺点：

- 更难看清全局运行；
- 更难形成统一审计叙事；
- 交接边界必须设计得很仔细；
- 状态、意图和约束在转交时更容易丢。

## 4. 最有用的实用原则

简短地说：

- 当你需要一个统一协调中心时，`manager pattern` 更合适；
- 当任务天然在不同角色或领域之间流转时，`handoffs` 更合适。

所以真正的问题不是“哪个更现代”，而是“责任应该住在哪里”。

## 5. 什么时候 Manager Pattern 往往更合适

manager pattern 通常在这些情况下很好用：

- 任务长度短到中等；
- 需要统一预算控制；
- 各个子任务用到的工具和策略基本相同；
- 团队想要更强的可解释性；
- 有一个主要运行时负责人。

典型例子：

- 支持分流；
- 最终只需要一个统一答案的研究助手；
- 调用多个重读取能力的内部副驾驶；
- 专家智能体本质上更像类型化工具的场景。

!!! note "Manager/handoff case-spine note"
    manager-vs-handoff 选择会随三个 canonical cases 改变。**Support triage** 通常更适合 manager pattern，因为 approved write routine 和 ticket state 应该留在同一条 audit story 中。**Internal knowledge assistant** 在 read-heavy capabilities、source attribution 和 tenant boundary 仍可放进同一个 controlled context 时，通常也保持 manager-led。**Incident coordination** 更早需要 handoffs，因为 escalation、security investigation、remediation 和 owner record 往往会跨过不同 accountable roles。

在这些地方，manager pattern 往往是最无聊、也最正确的答案。

## 6. 什么时候 Handoffs 更好

handoffs 通常在这些情况下更有优势：

- 任务真的跨越了不同领域边界；
- 每个角色都需要自己的上下文和防护栏；
- 负责人机制已经分散到不同团队；
- 有必要显著缩小当前智能体的认知范围；
- 下一阶段更像责任转移，而不是辅助器调用。

典型例子：

- 销售资格确认→解决方案智能体→法务评审智能体；
- 事故接收→安全调查→修复协调；
- 由不同业务单元拥有的入职流程。

这里交接往往比一个假装什么都懂的中央管理器更自然。

## 7. 常见错误

这两种模式都有自己的典型失败方式。

manager pattern 常见问题：

- 管理器扛了太多上下文；
- 专家智能体薄到几乎没有意义；
- 路由藏在提示里，而不是显式策略；
- 中央编排器变成单点混乱源。

handoffs 常见问题：

- 约束和意图在转交时丢失；
- 下一个智能体拿到的状态过少或过多；
- 最终结果到底谁负责变得不清楚；
- 追踪变得断裂而难读。

所以关键不是“哪个模式更强”，而是“哪个模式你能平稳运维”。

## 8. 一个简单的 Decision Table

下面这个表很适合作为起点。

| 场景 | 通常更合适的选择 |
| --- | --- |
| 需要统一控制步骤、成本和策略 | `manager pattern` |
| 角色和领域天然分离 | `handoffs` |
| 专家更像能力工具 | `manager pattern` |
| 下一个参与者需要自己的上下文边界 | `handoffs` |
| 更看重统一审计叙事 | `manager pattern` |
| 更看重特定角色智能体的局部自治 | `handoffs` |

这张表不能替代设计，但能很好地去掉不少多余浪漫主义。

## 9. 如何避免过早走错

通常最健康的路线是：

1. 先做单智能体循环；
2. 如果需要协调多个专家路径，再进入管理器模式；
3. 只有当真实领域边界已经出现时，再走向交接。

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

这里的重点不是管理器要“无限思考”，而是它持有计划、调用专家，并把结果重新收拢起来。

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

关键不在调用本身，而在于交接传递的应该是精心整理过的转交包，而不是一整团混乱状态。

## 12. 对安全最重要的是什么

如果你用 manager pattern，重点检查：

- 管理器会不会拿到过宽的权限；
- 它会不会“替所有人”绕过审批边界；
- 它会不会变成所有租户上下文泄漏的中心点。

如果你用 handoffs，重点检查：

- 策略约束在转交后是否还保留；
- 风险分类会不会丢；
- 不受信任上下文会不会不经标记就传给下一个智能体；
- 追踪里能不能看清是谁接管了控制权。

也就是说，这里的安全不是“叠加在编排上面”的东西，而是编排语义本身的一部分。

## 13. 现在就该做什么

先过一遍这份短清单，把所有回答为“否”的地方单独记下来：

- 谁拥有全局运行目标？
- 谁对最终结果负责？
- 预算控制住在哪里？
- 停止条件住在哪里？
- 追踪能不能解释任务为什么从一个智能体交给另一个？
- 你是不是太早走向了交接，而其实管理器模式更简单？
- 管理器有没有变成一个什么都做的中央怪物？

如果这些答案都很模糊，说明模式还没真正架构化成熟。

## 14. 下一步做什么

- [实践篇：Instructions、Routines 与 Prompt Templates](practical-routines.zh.md)
- [第 2 章：安全智能体的参考架构](chapter-2.zh.md)
- [第四部分：工具与执行](../part-iv/index.zh.md)
- [参考来源](../../appendix/sources.zh.md)

[^openai-practical]: [OpenAI, A practical guide to building agents (PDF)](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
