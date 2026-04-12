# 第一部分：基础

第一部分回答一个核心问题：如果把智能体系统当作平台型产品而不是玩具来设计，**现代安全智能体架构**应该是什么样子。

!!! info "第一部分的快速路线"
    如果时间有限，可以这样读：

    - [第 1 章](chapter-1.md)：先判断这里到底需不需要 agent，而不是普通 workflow；
    - [第 2 章](chapter-2.md)：顺着一个请求走完参考架构；
    - [第二部分](../part-ii/index.zh.md)：再去看真正的信任边界在哪里。

    只走完这条路线，也已经足够把系统当作工程轮廓来讨论，而不是停留在概念层面。

## 这一部分解决什么问题

- 智能体不等于 LLM。LLM 只负责部分决策。
- 安全不能作为 MVP 之后的“外层包装”，它必须内建在 runtime 中。
- 大多数生产场景受益的并不是最大自治，而是正确组合 `workflow + guarded autonomy`。
- 多智能体设计的价值不在“好看”，而在上下文隔离、团队职责边界和并行执行。[^anthropic][^langgraph-multi]

## 读完这一部分后，你应该得到什么

读完第一部分后，读者应当获得：

- 一张安全智能体平台的参考架构图；
- 一套判断何时真的需要 agent、何时 workflow 更合适的标准；
- 在 workflow、single-agent 与 subagents 之间做选择的标准；
- 没有这些层就会让系统变脆弱的必需清单；
- 能够与平台、安全、产品团队讨论架构的共同语言。

## 本部分内容

- [第 1 章：为什么智能体需要平台，而不是魔法](chapter-1.zh.md)
- [第 2 章：安全智能体的参考架构](chapter-2.zh.md)
  这一章沿用第 1 章的 support 场景，展示同一个请求如何穿过平台各层。
- [实践篇：Instructions、Routines 与 Prompt Templates](practical-routines.zh.md)
- [实践篇：Manager Pattern vs Handoffs](practical-manager-handoffs.zh.md)
- [为什么选择这套发布技术栈](../../appendix/stack.md)
- [参考文献与来源](../../appendix/sources.zh.md)

## 这一部分之后去哪里

读完这一部分之后，你应该已经有了一个可以落地的基本轮廓：这里到底需不需要 agent、最小平台长什么样、真实的信任边界从哪里开始。

下一步就很自然地进入 [第二部分](../part-ii/index.zh.md)：把同一个请求带进 security perimeter、tool gateway 和 approval boundary。

[^anthropic]: [Anthropic, Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
[^langgraph-multi]: [LangChain, Multi-agent](https://docs.langchain.com/oss/python/langchain/multi-agent)
