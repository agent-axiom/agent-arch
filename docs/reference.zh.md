# 参考层

如果这本书回答的是**为什么**安全智能体系统应该这样构建，那么参考层回答的就是：**哪些工件、模式页与契约页应该被明确固定下来**。

这一层是有意作为支持层存在的，而不是主要阅读入口。它的作用是用可复用的工程材料来支撑本书的论证，而不是替代本书本身的阅读路径。

当你需要下面这些东西时，这一节最有用：

- 快速找到合适的契约页；
- 准备设计评审或发布评审；
- 为团队抽取可复用的工程工件；
- 从概念章节切换到更落地的工程材料。

如果你刚进入这个项目，最好先读本书本体。等你需要支撑性的 Schema、检查清单和契约表面来支撑主要论证时，再来到这里。

这一层**不**承诺的事情是：

- 它不会取代本书本身的阅读路径；
- 它不会按章节去解释主要的因果论证；
- 它也不应该成为读者学习取舍与层间边界的主要地方。

## 从这里开始

如果只想快速进入，建议按这个顺序看：

1. [术语表](appendix/glossary.zh.md)
2. [速查表](appendix/cheat-sheets.zh.md)
3. [参考包](appendix/reference-package.zh.md)

!!! example "support-triage 工件路线"
    如果你按 support-triage 案例来读这本书，可以把 traces、评测数据集、policy bundle、审批记录、事故记录、变更发布、生命周期工件和 registry operations 这些页面放在旁边。正是这些契约把重复工单事故从故事变成可审阅的工件集合。

!!! note "Canonical case artifacts"
    三个 canonical cases 会从不同工件集合进入参考层。**Support triage** 依赖 approval record、policy bundle、trace schema 和 duplicate-ticket recovery evidence。**Internal knowledge assistant** 需要 memory/retrieval contract、freshness checks、access control 和 knowledge provenance。**Incident coordination** 连接 incident record、escalation evidence、notification side effects、response ownership 和 post-incident learning。

## 模式页与契约页

- [追踪 Schema 与事件目录](appendix/trace-schema.zh.md)
- [评测数据集 Schema 与打分契约](appendix/eval-schema.zh.md)
- [策略包 Schema 与审批契约](appendix/policy-bundle-schema.zh.md)
- [审批请求与决策记录 Schema](appendix/approval-schema.zh.md)
- [事故记录与事后复盘链接 Schema](appendix/incident-record-schema.zh.md)
- [变更评审与发布门禁 Schema](appendix/change-rollout-schema.zh.md)
- [生命周期工件 Schema](appendix/lifecycle-artifact-schema.zh.md)
- [记忆记录与检索契约 Schema](appendix/memory-retrieval-schema.zh.md)
- [智能体系统中的因果调试与根因分析](appendix/causal-debugging.zh.md)
- [智能体系统的记忆评测模式](appendix/memory-eval-patterns.zh.md)
- [智能体系统的工具失败恢复模式](appendix/tool-failure-recovery.zh.md)

## 实践页面

- [参考包](appendix/reference-package.zh.md)
- [案例研究](appendix/case-studies.zh.md)
- [按场景组织的策略模板与检查清单](appendix/policy-templates.zh.md)
- [智能体系统事故响应手册](appendix/incident-response-playbook.zh.md)
- [智能体注册表与清单运维手册](appendix/registry-operations-handbook.zh.md)
- [智能体系统事后复盘模板](appendix/postmortem-template.zh.md)

## 按主题快速进入

如果你不需要整个参考层，只想快速进入一个具体问题，可以直接走这些短路线：

- 工具目录设计、语义化工具过滤、读/写分类法：[第 8 章：执行模型与工具目录](book/part-iv/chapter-8.zh.md)
- MCP 主机/客户端/服务器角色、能力传输、沙箱边界：[第 9 章：沙箱执行与 MCP 作为集成契约](book/part-iv/chapter-9.zh.md)
- 语义鸿沟、HyDE、RAG 与训练的取舍：[第 7 章：检索、压缩与后台更新](book/part-iii/chapter-7.zh.md)
- 延迟预算、快路径/慢路径、路由管线：[第 12 章：智能体系统的 SLO](book/part-v/chapter-12.zh.md)
- LLM-as-a-judge、校准与评审器/人类一致性：[第 13 章：离线评测、在线评测与回归门禁](book/part-v/chapter-13.zh.md)

## 继续阅读

- [从这里开始](start-here.zh.md)
- [全书计划](book/plan.zh.md)
- [研究前沿：记忆、可观测性与多智能体可靠性](appendix/research-frontier.zh.md)
- [参考来源](appendix/sources.zh.md)

最简单的规则是：

- 用本书理解论证与章节顺序；
- 用参考层查看支撑工件与面向实现的细节。
