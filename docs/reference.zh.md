# 参考层

如果这本书回答的是**为什么**安全智能体系统应该这样构建，那么参考层回答的就是：**哪些工件、模式页与契约页应该被明确固定下来**。

这一层是有意作为支持层存在的，而不是主要阅读入口。它的作用是用可复用的工程材料来支撑本书的论证，而不是替代本书本身的 reader journey。

当你需要下面这些东西时，这一节最有用：

- 快速找到合适的契约页；
- 准备 design review 或 rollout review；
- 为团队抽取可复用的工程工件；
- 从概念章节切换到更落地的工程材料。

如果你刚进入这个项目，最好先读本书本体。等你需要 supporting schemas、checklists 和 contract surfaces 来支撑主要论证时，再来到这里。

这一层**不**承诺的事情是：

- 它不会取代本书本身的 reader journey；
- 它不会按章节去解释主要的 causal argument；
- 它也不应该成为读者学习 trade-offs 与层间边界的主要地方。

## 从这里开始

如果只想快速进入，建议按这个顺序看：

1. [术语表](appendix/glossary.zh.md)
2. [速查清单](appendix/cheat-sheets.zh.md)
3. [参考运行时包](appendix/reference-package.zh.md)

## 模式页与契约页

- [Trace Schema 与 Event Catalog](appendix/trace-schema.zh.md)
- [Eval Dataset Schema 与 Grading Contract](appendix/eval-schema.zh.md)
- [Policy Bundle Schema 与 Approval Contract](appendix/policy-bundle-schema.zh.md)
- [Approval Request 与 Decision Record Schema](appendix/approval-schema.zh.md)
- [Incident Record 与 Postmortem Linkage Schema](appendix/incident-record-schema.zh.md)
- [Change Review 与 Rollout Gate Schema](appendix/change-rollout-schema.zh.md)
- [Lifecycle Artifact Schema](appendix/lifecycle-artifact-schema.zh.md)
- [Memory Record 与 Retrieval Contract Schema](appendix/memory-retrieval-schema.zh.md)
- [智能体系统中的 Causal Debugging 与 Root-Cause Analysis](appendix/causal-debugging.zh.md)
- [智能体系统的 Memory Eval Patterns](appendix/memory-eval-patterns.zh.md)
- [智能体系统的 Tool Failure Recovery Patterns](appendix/tool-failure-recovery.zh.md)

## 实践页面

- [参考运行时包](appendix/reference-package.zh.md)
- [案例研究](appendix/case-studies.zh.md)
- [按场景组织的 Policy Templates 与 Checklists](appendix/policy-templates.zh.md)
- [智能体系统事故响应手册](appendix/incident-response-playbook.zh.md)
- [智能体 registry 与 inventory 运维手册](appendix/registry-operations-handbook.zh.md)
- [智能体系统 Postmortem 模板](appendix/postmortem-template.zh.md)

## 按主题快速进入

如果你不需要整个 reference layer，只想快速进入一个具体问题，可以直接走这些短路线：

- Tool catalog 设计、semantic tool filtering、read/write taxonomy：[第 8 章：执行模型与工具目录](book/part-iv/chapter-8.zh.md)
- MCP host/client/server 角色、capability transport、sandbox boundary：[第 9 章：沙箱执行与 MCP 作为集成契约](book/part-iv/chapter-9.zh.md)
- Semantic gap、HyDE、RAG vs training：[第 7 章：检索、压缩与后台更新](book/part-iii/chapter-7.zh.md)
- Latency budget、fast path / slow path、routed pipeline：[第 12 章：智能体系统的 SLO](book/part-v/chapter-12.zh.md)
- LLM-as-a-judge、calibration 与 judge-human agreement：[第 13 章：离线评测、在线评测与回归门禁](book/part-v/chapter-13.zh.md)

## 继续阅读

- [从这里开始](start-here.zh.md)
- [全书计划](book/plan.zh.md)
- [研究前沿：记忆、可观测性与多智能体可靠性](appendix/research-frontier.zh.md)
- [参考来源](appendix/sources.zh.md)

最简单的规则是：
- 用本书理解 argument 与 sequencing；
- 用参考层查看 support artifacts 与 implementation-facing detail。
