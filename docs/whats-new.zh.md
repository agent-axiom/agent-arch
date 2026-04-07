# 最新进展

这一页是面向读者的简短更新日志，用来展示这本书和参考运行时最近有哪些重要增强。它不是 git history 的替代品，而是让读者快速看到项目是否持续演进。

_更新于 2026 年 4 月 8 日。_

## Book

### 第八部分：智能体系统生命周期

现在全书已经包含 `SDLC -> ADLC`、change management、assurance loop、supply chain、retirement、misalignment、behavioral evals、AI-native observability 与 inventory control 的完整内容。

Why it matters：
- 现在这本书覆盖的不只是架构与上线，还覆盖了智能体系统发布后的生命周期管理。

## Reference

### 可复用的参考层

站点现在已经包含以下参考页：

- traces 与 event catalog；
- eval datasets 与 grading contract；
- policy bundles 与 approvals；
- change review 与 rollout gates；
- lifecycle artifacts；
- memory retrieval contracts。

Why it matters：
- 读者现在可以从解释性章节直接跳到可审阅的 schemas 与 contract artifacts。

## Runtime

### 可运行的参考运行时

仓库中的 [agent_runtime_ref](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref) 现在支持：

- approvals；
- controls；
- lifecycle artifacts；
- session export；
- eval dataset export；
- 带 redaction 与 schema versioning 的 trace export。

Why it matters：
- 这本书现在不只依赖叙述性章节，也有可运行的 reference implementation 作为支撑。

## Practical Appendix

### 更强的实践附录

站点已经包含：

- glossary；
- cheat sheets；
- case studies；
- policy templates；
- research frontier 页面；
- community roadmap。

Why it matters：
- 读者现在可以不按线性顺序通读全书，也能直接进入 checklists、case studies、glossary 与 practical assets。

## 这对读者意味着什么

- 你可以把这本书当作 handbook 使用。
- 你可以把参考页当作工程起点复用。
- 你可以运行示例运行时，而不仅仅是阅读 Markdown。
- 你可以把架构建立在 OpenAI、Anthropic、Google、Microsoft 与 NIST 的近年资料之上。

## 继续阅读

- [从这里开始](start-here.zh.md)
- [参考层](reference.zh.md)
- [全书计划](book/plan.zh.md)
- [参考来源](appendix/sources.zh.md)
