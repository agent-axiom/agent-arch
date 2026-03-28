# 第一部分：基础

第一部分回答一个核心问题：如果把智能体系统当作平台型产品而不是玩具来设计，**现代安全智能体架构**应该是什么样子。

## 在实现前必须先理解的事情

- 智能体不等于 LLM。LLM 只负责部分决策。
- 安全不能作为 MVP 之后的“外层包装”，它必须内建在 runtime 中。
- 大多数生产场景受益的并不是最大自治，而是正确组合 `workflow + guarded autonomy`。
- 多智能体设计的价值不在“好看”，而在上下文隔离、团队职责边界和并行执行。[^anthropic][^langgraph-multi]

## 这一部分的产出

读完第一部分后，读者应当获得：

- 一张安全智能体平台的参考架构图；
- 在 workflow、single-agent 与 subagents 之间做选择的标准；
- 没有这些层就会让系统变脆弱的必需清单；
- 能够与平台、安全、产品团队讨论架构的共同语言。

## 导航

- [第 1 章：现代安全架构](chapter-1.md)
- [为什么选择这套发布技术栈](../../appendix/stack.md)
- [参考文献与来源](../../appendix/sources.md)

[^anthropic]: [Anthropic, Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
[^langgraph-multi]: [LangChain, Multi-agent](https://docs.langchain.com/oss/python/langchain/multi-agent)

