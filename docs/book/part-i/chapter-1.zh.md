# 第 1 章：为什么智能体需要的是平台，而不是魔法

## 1. 常见错误从哪里开始

当人们第一次构建 agent system 时，几乎总会有同样的诱惑：

- 先拿一个强模型；
- 接上几个 tools；
- 写一个很有野心的 prompt；
- 看看这个 agent 能不能显得“足够自主”。

在 demo 里，这有时甚至真的能跑起来。但一旦你开始认真想 production，一个不太舒服的事实就会冒出来：真正的问题不是 agent 有多聪明，而是它有多可控。

## 2. Vikulin 提得很好的地方，以及现在已经不够的地方

Dmitry Vikulin 的文章很好地提出了起点问题：一个可靠的 agent 到底由哪些模块组成。[^vikulin] 这是正确的起点。但如果你想把系统推进到真实使用阶段，光有模块清单已经不够了。

在实践里，强团队很快会变成另一种画法：

- 先选 **最简单、可执行的模式**；
- 把危险动作移到单独的 **control plane**；
- 只有在已经有 **policy、telemetry 和 rollback boundary** 的地方，才允许更多 autonomy。[^anthropic][^openai-evals][^langgraph-durable]

所以，现代系统更适合被设计成“安全 agent execution 的平台”，而不是“一个聪明的 agent”。

## 3. 默认先 workflow，必要时才加 agent 性

Anthropic 很明确地区分了 `workflows` 和 `agents`，并建议先从更简单的路径开始。[^anthropic] 这是整个主题里最有用的实践原则之一。

如果把它翻译成工程语言，大概是这样：

- 如果执行路径已知，就写 workflow；
- 如果只是在一个小范围里做 tool selection，就用 single-agent loop；
- 如果任务天然能拆成独立子任务，再引入 subagents；
- 如果你都说不清为什么需要 autonomy，那大概率现在还不需要它。

这个建议有点无聊，但它非常有效。

## 4. 什么时候真的需要 agent，什么时候其实不需要

OpenAI 的实用指南里有一个很健康的提醒：不是因为任务“听起来很现代”，就一定该上 agent。[^openai-practical]

通常只有在至少满足下面一个条件时，agent 才真正有意义：

- 系统在执行过程中必须连续做出一些不那么显然的决策；
- 规则过于分支化，用硬编码维护起来太贵；
- 关键价值来自非结构化数据，比如邮件、文档、笔记或网页内容。

如果情况更像下面这样，workflow 往往是更诚实的选择：

- 步骤几乎总是固定的；
- 状态转移很容易形式化；
- 可解释性和可重复性比灵活推理更重要；
- write path 的风险很高，但 autonomy 带来的收益并不明显。

一个很实用的判断方式是：

- `workflow` 适合执行路径事先就很清楚的任务；
- `single-agent loop` 适合路径不固定、但边界很窄的任务；
- `multi-agent` 只有在一个 loop 已经因为上下文、职责或并行性而变得拥挤时才值得引入。

简短地说：agent 性应该为你买来真正有价值的灵活性，而不是把清楚的设计换成时髦的复杂性。

## 5. 为什么“魔法感”比你想的更早失效

只押注在一个聪明模型上，很快就会变贵，原因通常有这些：

- 成本不可预测；
- 行为漂移；
- auditability 很弱；
- 结果难以复现；
- incident 很难调查。

最烦的是，这些问题一开始通常并不明显。只要场景还短、还安全，看上去一切都很好。然后你加入：

- 长上下文；
- 外部系统；
- 私有数据；
- approvals；
- 多种访问角色，

系统就会突然不再是“带工具的 LLM”那么简单。

## 6. 值得依赖的四个原则

### 5.1. 先控制，再自治

先把路径做得可预测，再一点点放大 agent 的自由度。

### 5.2. 安全不能挂在边上

如果 policy、identity 和 approvals 没有嵌进 runtime，后面你修的就不是演进，而是在做紧急抢修。

### 5.3. 状态必须是显式的

长任务不应该因为某个进程重启，就把步骤、approval 或 side effects 丢掉。

### 5.4. 可观测性比“看起来聪明”更重要

如果 agent “看起来很聪明”，但你没有 traces、evals 和 step metadata，那你其实并没有控制这个系统。[^openai-sdk][^openai-evals]

## 7. Production 团队必须始终看见什么

一个最低可用的集合是：

- agent 生成了什么计划；
- 调用了哪些工具；
- 什么上下文被送进了模型；
- 质量到底在哪一步下降了；
- 每一步在 latency 和 tokens 上花了多少。

一旦这些信息从视野里消失，agent 就会开始变成黑箱。

## 8. 一个简短结论

如果你只想记住这一章的一句话，那就记这句：

> 一个好的 agent 产品，并不是从最大自治开始，而是从一个可预测的平台开始，自治是在这个平台上被逐步加进去的。

这也是为什么下一章不再聊“聪明”，而是聊平台架构：为了安全地运行这样一个系统，到底需要哪些层。

## 9. 接下来读什么

- [第一部分：基础](index.zh.md)
- [第 2 章：安全智能体的参考架构](chapter-2.zh.md)
- [全书计划](../plan.zh.md)

[^vikulin]: [Dmitry Vikulin，《可靠 AI Agents 的架构》](https://vikulin.ai/library/tpost/ai_agent_architecture)
[^anthropic]: [Anthropic, Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
[^langgraph-durable]: [LangGraph, Durable execution](https://docs.langchain.com/oss/javascript/langgraph/durable-execution)
[^openai-practical]: [OpenAI, A practical guide to building agents (PDF)](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
[^openai-sdk]: [OpenAI, Agents SDK](https://developers.openai.com/api/docs/guides/agents-sdk)
[^openai-evals]: [OpenAI, Agent evals](https://platform.openai.com/docs/guides/agent-evals)
