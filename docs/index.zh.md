# 安全 AI 智能体架构

这本书写给那些需要的不是炫目的演示，而是能够承受生产现实（production reality）的智能体系统团队。

它的中心论点很简单：**智能体需要平台，而不是魔法**。一旦系统拥有高风险动作（risky actions）、记忆（memory）、审批（approvals）、发布（rollout）和长期运维尾部（long operational tail），单靠模型加几个工具（tools）就不够了。你需要明确的信任边界、策略层（policy layer）、受控执行（controlled execution）、可观测性（observability）、质量评估（quality assessment）与生命周期纪律（lifecycle discipline）。

构建智能体很枯燥，但结果令人震撼：团队得到的不是一次性炫技（one-off trick），而是一个可以约束（constrain）、观察（observe）、发布（ship）并无需猜测地持续改进（improve without guessing）的系统。

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

- 想构建智能体功能（agent features）、又不想把系统做成提示和例外堆的产品工程师。
- 需要共享运行时（runtime）、策略层（policy layer）、审批（approvals）、可观测性（observability）和受控发布（rollout）的平台团队。
- 关心信任边界（trust boundaries）、高风险执行路径（risky execution paths）和滥用表面（abuse surfaces）的安全工程师。
- 需要可复用工程纪律、而不是智能体剧场的技术负责人和架构师。

## 它应该改变读者什么思维

读完这本书，读者应该停止把智能体想成“LLM 加一点编排（orchestration）”，而开始把它想成一个受治理的生产系统（governed production system）：

- 有明确的信任边界（trust boundaries）与动作边界（action boundaries）；
- 策略约束的执行（policy-constrained execution）；
- 高风险路径（risky paths）有审批（approvals）；
- 具备运行级可观测性（run-level observability）与证据（evidence）；
- 拥有发布纪律（rollout discipline）、负责人机制（ownership）与生命周期治理（lifecycle governance）。

## 这本书怎么读

如果你只想要最短入口，就从 [第 1 章](book/part-i/chapter-1.zh.md) 开始。如果你需要按角色或任务选择路线，就打开[从这里开始](start-here.zh.md)。如果你更关心结构与状态，就看[全书计划](book/plan.zh.md)。如果你需要可复用工件（reusable artifacts）、模式（schemas）和契约（contracts），就进入[参考层（reference layer）](reference.zh.md)。

穿过全书的最短实用途径大致是：

1. [第 1 章：为什么智能体需要的是平台，而不是魔法](book/part-i/chapter-1.zh.md)
2. [第 3 章：安全边界与信任边界](book/part-ii/chapter-3.zh.md)
3. [第 8 章：执行模型与工具目录](book/part-iv/chapter-8.zh.md)
4. [第五部分：可靠性与可观测性](book/part-v/index.zh.md)
5. [第 18 章：生产上线检查清单](book/part-vii/chapter-18.zh.md)

!!! note "规范案例地图（Canonical case map）"
    阅读这条路线时，要同时保留三个规范案例（canonical cases）。**支持分流（Support triage）** 检查写入能力（write capabilities）、审批（approvals）和重复工单恢复（duplicate-ticket recovery）。**内部知识助手（Internal knowledge assistant）** 检查检索（retrieval）、记忆（memory）、新鲜度（freshness）和知识来源（knowledge provenance）。**事件协调（Incident coordination）** 检查追踪（traces）、升级（escalation）、通知副作用（notification side effects）、响应归属（response ownership）和事件后学习（post-incident learning）。

!!! note "安全智能体模式主线（Safe-agent schema spine）"
    如果需要一条简短的安全智能体架构（safe-agent architecture）路线，可以从 [追踪模式（trace schema）](appendix/trace-schema.zh.md)、[评测模式（eval schema）](appendix/eval-schema.zh.md) 和 [记忆/检索模式（memory/retrieval schema）](appendix/memory-retrieval-schema.zh.md) 开始。这条主线（spine）连接 MCP 威胁模型（MCP threat model）、A2A 移交信任契约（A2A handoff trust contract）、验证器裁决记录（verifier verdict record）、治理动作记录（governance action record）、记忆投毒审查字段（memory poisoning review fields）和统一智能体威胁证据（unified agent threat evidence）。

## 这里已经有什么

- 已发布的俄文核心原稿（core manuscript），覆盖从架构基础到生命周期治理（lifecycle governance）的八个部分。
- 可用于阅读、但仍在进行编辑清理（editorial cleanup）的 `en` 与 `zh` 翻译层。
- 可运行的参考包 `agent_runtime_ref`。
- 覆盖追踪（traces）、评测（evals）、策略包（policy bundles）、审批（approvals）、记忆与生命周期工件（lifecycle artifacts）的参考页面。
- 实战案例、检查清单、策略模板与术语表。
- 正在推进的书稿与公开站点表面编辑打磨（editorial pass）。

## 这本书不打算成为什么

它不是某个框架（framework）的手册，不是提示技巧合集（prompt tricks），也不是 AI 市场巡礼（AI market overview）。本书站在具体 SDK 和平台文档（platform docs）之上，去回答更棘手的问题：智能体到底该被允许做什么，写入路径（write path）应该怎样受限，应该观察什么，变更应该怎样发布，系统上线后到底谁负责。

## 接下来去哪里

<div class="button-stack" markdown="1">

[从这里开始](start-here.zh.md){ .md-button .md-button--primary }
[进入第一部分](book/part-i/index.zh.md){ .md-button }
[打开参考包](appendix/reference-package.zh.md){ .md-button }

</div>
