# 安全 AI 智能体架构

这本书写给那些需要的不是炫目的演示，而是能够承受生产现实的智能体系统团队。

它的中心论点很简单：**智能体需要平台，而不是魔法**。一旦系统拥有高风险动作、记忆、审批、发布和长期运维尾部，单靠模型加几个工具就不够了。你需要明确的信任边界、策略层、受控执行、可观测性、质量判断与生命周期纪律。

构建智能体很枯燥，但结果令人震撼：团队得到的不是一次性的炫技，而是一个可以约束、观察、发布并持续改进的系统，不必靠猜。

!!! info "中文本地化预览"
    中文层目前是可阅读的本地化预览，而不是面向出版社的最终中文版。它适合社区预览、结构审查和术语对齐；正式出版前仍需要完整中文编辑、术语统一、图表/导出 QA 和母语审校。

<div class="hero-actions" markdown="1">

[从这里开始](start-here.zh.md){ .md-button .md-button--primary }
[阅读第 1 章](book/part-i/chapter-1.zh.md){ .md-button }
[打开全书计划](book/plan.zh.md){ .md-button }

</div>

<div class="book-cover" markdown="1">

![本书封面](assets/images/hero-home.png)

</div>

## 这本书适合谁

- 想构建智能体功能、又不想把系统做成提示和例外堆的产品工程师。
- 需要共享运行时、策略层、审批、可观测性和受控发布的平台团队。
- 关心信任边界、高风险执行路径和滥用表面的安全工程师。
- 需要可复用工程纪律、而不是智能体剧场的技术负责人和架构师。

## 它应该改变读者什么思维

读完这本书，读者应该停止把智能体想成“LLM 加一点编排”，而开始把它想成一个受治理的生产系统：

- 有明确的信任与动作边界；
- 执行受策略约束；
- 高风险路径有审批；
- 具备运行级可观测性与证据；
- 拥有发布纪律、负责人机制与生命周期治理。

## 这本书怎么读

如果你只想要最短入口，就从 [第 1 章](book/part-i/chapter-1.zh.md) 开始。如果你需要按角色或任务选择路线，就打开[从这里开始](start-here.zh.md)。如果你更关心结构与状态，就看[全书计划](book/plan.zh.md)。如果你需要可复用工件、Schema 和契约，就进入[参考层](reference.zh.md)。

穿过全书的最短实用途径大致是：

1. [第 1 章：为什么智能体需要的是平台，而不是魔法](book/part-i/chapter-1.zh.md)
2. [第 3 章：安全边界与信任边界](book/part-ii/chapter-3.zh.md)
3. [第 8 章：执行模型与工具目录](book/part-iv/chapter-8.zh.md)
4. [第五部分：可靠性与可观测性](book/part-v/index.zh.md)
5. [第 18 章：生产上线检查清单](book/part-vii/chapter-18.zh.md)

!!! note "规范案例地图（Canonical case map）"
    阅读这条路线时，要同时保留三个规范案例（canonical cases）。**支持分流（Support triage）** 检查写入能力（write capabilities）、审批（approvals）和重复工单恢复（duplicate-ticket recovery）。**内部知识助手（Internal knowledge assistant）** 检查检索（retrieval）、记忆（memory）、新鲜度（freshness）和知识来源（knowledge provenance）。**事件协调（Incident coordination）** 检查追踪（traces）、升级（escalation）、通知副作用（notification side effects）、响应归属（response ownership）和事件后学习（post-incident learning）。

!!! note "Safe-agent schema spine"
    如果需要一条简短的 safe-agent architecture 路线，可以从 [trace schema](appendix/trace-schema.zh.md)、[eval schema](appendix/eval-schema.zh.md) 和 [memory/retrieval schema](appendix/memory-retrieval-schema.zh.md) 开始。这个 spine 连接 MCP threat model、A2A handoff trust contract、verifier verdict record、governance action record、memory poisoning review fields 和 unified agent threat evidence。

## 这里已经有什么

- 已发布的俄文核心原稿，覆盖从架构基础到生命周期治理的八个部分。
- 可用于阅读、但仍在进行编辑清理的 `en` 与 `zh` 翻译层。
- 可运行的参考包 `agent_runtime_ref`。
- 覆盖追踪、评测、策略包、审批、记忆与生命周期工件的参考页面。
- 实战案例、检查清单、策略模板与术语表。
- 正在推进的书稿与公开站点表面编辑打磨。

## 这本书不打算成为什么

它不是某个框架的手册，不是提示技巧合集，也不是 AI 市场巡礼。本书站在具体 SDK 和平台文档之上，去回答更棘手的问题：智能体到底该被允许做什么，写入路径应该怎样受限，应该观察什么，变更应该怎样发布，系统上线后到底谁负责。

## 接下来去哪里

<div class="button-stack" markdown="1">

[从这里开始](start-here.zh.md){ .md-button .md-button--primary }
[进入第一部分](book/part-i/index.zh.md){ .md-button }
[打开参考包](appendix/reference-package.zh.md){ .md-button }

</div>
