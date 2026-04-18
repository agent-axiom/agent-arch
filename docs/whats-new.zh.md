# 最新进展

这一页是面向读者的简短更新日志，用来展示这本书和参考运行时最近有哪些重要增强。它不是 git history 的替代品，而是让读者快速看到项目是否持续演进。

_更新于 2026 年 4 月 18 日。_

## 书籍

### 第八部分：智能体系统生命周期

现在全书已经包含 `SDLC -> ADLC`、change management、assurance loop、supply chain、retirement、misalignment、behavioral evals、AI-native observability 与 inventory control 的完整内容。

为什么这很重要：
- 现在这本书覆盖的不只是架构与上线，还覆盖了智能体系统发布后的生命周期管理。

### 第一到第五部分的 production contour 更完整了

书里现在补上了更多连接 architecture、retrieval、execution 和 eval discipline 的桥：

- 第一部分更明确地区分了 runtime architecture、training layer 和 product surface；
- 第二部分加入了更清晰的 `prompt injection`、`jailbreaking` 与 `action hallucination` taxonomy；
- 第三部分加强了 retrieval contour：`semantic gap`、`HyDE`、`RAG first`，以及 continued pretraining 与 `SFT` 的区别；
- 第四部分补上了大工具目录、`semantic tool filtering` 和 `MCP host / client / server` 角色的 practical guidance；
- 第五部分补强了 `latency budget` 的产品视角，以及更实用的 `LLM-as-a-judge` framing。

为什么这很重要：
- 这本书现在覆盖的不只是基础 platform layers，也更贴近日常 production 团队在 design review、eval loop 和 rollout 之间反复遇到的问题。

## 参考层

### 可复用的参考层

站点现在已经包含以下参考页：

- 追踪与事件目录；
- 评测数据集与评分契约；
- 策略包与审批；
- 变更评审与发布门禁；
- 生命周期工件；
- 记忆检索契约。

为什么这很重要：
- 读者现在可以从解释性章节直接跳到可审阅的模式与契约工件。

## 运行时

### 可运行的参考运行时

仓库中的 [agent_runtime_ref](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref) 现在支持：

- 审批；
- 控制项；
- 生命周期工件；
- 会话导出；
- 评测数据集导出；
- 带脱敏与模式版本控制的追踪导出。

为什么这很重要：
- 这本书现在不只依赖叙述性章节，也有可运行的参考实现作为支撑。

## 实践附录

### 更强的实践附录

站点已经包含：

- 术语表；
- 速查清单；
- 案例研究；
- 策略模板；
- 研究前沿页面；
- 社区路线图。

为什么这很重要：
- 读者现在可以不按线性顺序通读全书，也能直接进入检查清单、案例研究、术语表与实践工件。

## 导航

### 入口页更强了

已更新：

- [从这里开始](start-here.zh.md)；
- [参考层](reference.zh.md)；
- [速查清单](appendix/cheat-sheets.zh.md)。

这些页面现在更容易把读者带到下面这些主题：

- `semantic tool filtering`；
- `HyDE` 与 `RAG vs training`；
- `latency budget` 与 routed pipelines；
- `LLM-as-a-judge` 与 judge calibration；
- `prompt injection`、`jailbreaking` 与 `action hallucination` 的区别。

为什么这很重要：
- 这些新主题现在不只藏在单个章节里，也已经出现在读者真正会先打开的入口页上。

## 这对读者意味着什么

- 你可以把这本书当作手册使用。
- 你可以把参考页当作工程起点复用。
- 你可以运行示例运行时，而不仅仅是阅读 Markdown。
- 你可以把架构建立在 OpenAI、Anthropic、Google、Microsoft 与 NIST 的近年资料之上。

## 继续阅读

- [从这里开始](start-here.zh.md)
- [参考层](reference.zh.md)
- [全书计划](book/plan.zh.md)
- [参考来源](appendix/sources.zh.md)
