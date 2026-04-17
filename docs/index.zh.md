# 安全 AI 智能体架构

这本书面向那些想构建真实生产级智能体系统的人，而不是只做一个看起来聪明的演示。

它的中心论点很简单：**智能体需要平台，而不是魔法**。如果团队把智能体当成“带工具的 prompt”，它也许会在 demo 中显得聪明，但一旦出现高风险动作、记忆、审批、发布和长期运维压力，系统就会暴露出真正的问题。

这是一本关于安全、可治理、可用于生产环境的 AI 智能体架构的实践型书籍。它面向那些已经意识到，提示词和工具调用远远不够，还需要围绕智能体建立完整运行体系的团队，包括信任边界、策略执行、审批、evidence capture、health budgets、eval judgment 与生命周期管理。

> 它以 Dmitry Vikulin 关于可靠 AI 智能体的文章为起点，进一步扩展为平台级视角：策略执行、人工审批、可观测性、评测体系、运维纪律与生命周期管理。

<div class="hero-actions" markdown="1">

[从这里开始](start-here.zh.md){ .md-button .md-button--primary }
[查看全书计划](book/plan.zh.md){ .md-button }
[查看参考运行时](appendix/reference-package.zh.md){ .md-button }

</div>

<div class="book-cover" markdown="1">

![本书封面](assets/images/hero-home.png)

</div>

## 为什么会有这本书

大多数智能体内容都在优化“更快做出演示”。但真实系统通常不是在 demo 里失败，而是在 reasoning 与 action 的边界、记忆层、审批路径、rollout、drift 和长期运营责任上失败。这本书的目标，就是把这整套运行模型讲清楚。

它的目标不是帮助读者做出“最自主的智能体”，而是帮助读者做出能承受生产现实的系统。

## 这本书适合谁

- 正在把智能体能力接入真实产品的工程师。
- 正在搭建共享运行时、策略、注册表、审批与可观测性层的平台团队。
- 需要看到信任边界与高风险执行路径的安全工程师。
- 更关心工程纪律而不是“智能体表演”的技术负责人和架构师。

## 你今天就能带走什么

- 一条从“先工作流后智能体”走向受控自治的实践路径。
- 关于策略层、审批、记忆、评测、可观测性与生命周期的章节。
- 一个可运行的参考运行时，包含会话导出、评测数据集导出、审批、控制项和生命周期工件。
- 一组参考页，覆盖追踪模式、评测模式、策略包、审批、发布门禁、记忆检索和生命周期工件。
- 可以直接复用的案例研究、检查清单和策略模板。

## 这到底是一本什么书

这首先是一本文向生产级智能体系统的实践架构书和 operating model。

它不是某个框架的手册，不是 prompt engineering 指南，也不是 AI 生态热点巡礼。参考页和可运行运行时存在，是为了支撑本书的论证，而不是取代本书本身。

它也是一部刻意塑形的书，而不只是把许多好主题堆在一起。Operational chapters 被按角色拆开，让读者能感觉到 production discipline 是如何被搭起来的：

- traces 捕获 raw run history；
- SLO 定义 health budgets 与 risk budgets；
- evals 产出 reviewable judgments；
- assurance 负责 response；
- provenance 与 artifacts 保存 evidence backbone；
- observability 提供 evidence substrate；
- registry 负责整个 estate 的 accountability。

而这种形状也应该被读者感受到为一串 outcomes，而不只是 chapter taxonomy：
- Part V 教会读者如何捕获 run history、定义可容忍的 budgets，并产出 reviewable judgments；
- Part VIII 教会读者如何把 lifecycle response、governed lineage、evidence visibility 与整个 estate 的 accountability 读成一个 production contour。

## 项目当前状态

- `Published core`：全书八个部分已经完整发布。
- `Expanding now`：入口页、参考层与站点导航仍在继续打磨。
- `Reference assets available`：模式、检查清单、案例研究与可运行参考运行时已经可用。

## 三条实用阅读路径

### 如果你在做产品型智能体

1. [第 1 章：为什么智能体需要平台，而不是魔法](book/part-i/chapter-1.zh.md)
2. [第 3 章：安全边界与信任边界](book/part-ii/chapter-3.zh.md)
3. [第 8 章：执行模型与工具目录](book/part-iv/chapter-8.zh.md)
4. [第 13 章：离线评测、在线评测与回归门禁](book/part-v/chapter-13.zh.md)

### 如果你在做平台或基础设施

1. [第 2 章：安全智能体的参考架构](book/part-i/chapter-2.zh.md)
2. [第 4 章：工具网关、审批与审计轨迹](book/part-ii/chapter-4.zh.md)
3. [第 17 章：策略层与能力目录](book/part-vii/chapter-17.zh.md)
4. [第 20 章：智能体系统的变更管理](book/part-viii/chapter-20.zh.md)

### 如果你更关注安全、控制与运维

1. [第 21 章：保障闭环：红队演练、检测与响应](book/part-viii/chapter-21.zh.md)
2. [第 22 章：供应链、来源链与已批准工件](book/part-viii/chapter-22.zh.md)
3. [第 26 章：面向 AI 的可观测性、清单覆盖率与可检测遥测](book/part-viii/chapter-26.zh.md)
4. [第 27 章：智能体清单、注册表与蔓延控制](book/part-viii/chapter-27.zh.md)

## 这个项目已经具备什么

- 完整的 `ru / en / zh` 三语内容。
- 带有 `pytest` 覆盖的可运行 `agent_runtime_ref` 包。
- 一套完整的参考层，涵盖模式与契约页面。
- 包含案例、速查清单、术语表与路线图的实践型附录。

## 核心工程观点

智能体系统最常见的错误很简单：先追求自治，再补可控性。更稳妥的路径通常是：

1. 先构建**可预测的工作流**。
2. 再按局部、可度量的方式加入自治。
3. 所有高风险动作都经过**策略、审批与追踪**。
4. 用**health budgets、eval judgment、遥测与生命周期纪律**维持质量。

## 参考层在哪里

如果你需要的是可复用的工程产物，先看这些页面：

- [追踪模式与事件目录](appendix/trace-schema.zh.md)
- [评测数据集模式与评分契约](appendix/eval-schema.zh.md)
- [策略包模式与审批契约](appendix/policy-bundle-schema.zh.md)
- [生命周期工件模式](appendix/lifecycle-artifact-schema.zh.md)
- [记忆记录与检索契约模式](appendix/memory-retrieval-schema.zh.md)

## 继续阅读

[从这里开始](start-here.zh.md){ .md-button .md-button--primary }
[打开参考页面](appendix/trace-schema.zh.md){ .md-button }
[查看来源](appendix/sources.zh.md){ .md-button }
