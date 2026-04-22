# 安全 AI 智能体架构

这本书写给那些需要的不是炫目的 demo，而是能够承受生产现实的 agent system 的团队。

它的中心论点很简单：**智能体需要平台，而不是魔法**。一旦系统拥有 risky actions、memory、approvals、rollout 和长期运维尾部，单靠模型加几个 tools 就不够了。你需要明确的 trust boundaries、policy layer、受控 execution、observability、quality judgment 与 lifecycle discipline。

<div class="hero-actions" markdown="1">

[从这里开始](start-here.zh.md){ .md-button .md-button--primary }
[阅读第 1 章](book/part-i/chapter-1.zh.md){ .md-button }
[打开全书计划](book/plan.zh.md){ .md-button }

</div>

<div class="book-cover" markdown="1">

![本书封面](assets/images/hero-home.png)

</div>

## 这本书适合谁

- 想构建 agent features、又不想把系统做成 prompts 和 exceptions 堆的产品工程师。
- 需要共享 runtime、policy layer、approvals、observability 和受控 rollout 的平台团队。
- 关心 trust boundaries、risky execution paths 和 abuse surfaces 的安全工程师。
- 需要可复用工程纪律、而不是 agent theater 的技术负责人和架构师。

## 它应该改变读者什么思维

读完这本书，读者应该停止把 agent 想成“LLM 加一点 orchestration”，而开始把它想成一个受治理的 production system：

- 有明确的 trust 与 action boundaries；
- execution 受 policy 约束；
- risky paths 有 approvals；
- 具备 run-level observability 与 evidence；
- 拥有 rollout discipline、ownership 与 lifecycle governance。

## 这本书怎么读

如果你只想要最短入口，就从 [第 1 章](book/part-i/chapter-1.zh.md) 开始。如果你需要按角色或任务选择路线，就打开[从这里开始](start-here.zh.md)。如果你更关心结构与状态，就看[全书计划](book/plan.zh.md)。如果你需要可复用工件、schema 和 contract，就进入[参考层](reference.zh.md)。

穿过全书的最短实用途径大致是：

1. [第 1 章：为什么智能体需要平台，而不是魔法](book/part-i/chapter-1.zh.md)
2. [第 3 章：安全边界与信任边界](book/part-ii/chapter-3.zh.md)
3. [第 8 章：执行模型与工具目录](book/part-iv/chapter-8.zh.md)
4. [第五部分：可靠性与可观测性](book/part-v/index.zh.md)
5. [第 18 章：生产上线检查清单](book/part-vii/chapter-18.zh.md)

## 这里已经有什么

- 完整的俄文原稿，以及 `en` 和 `zh` 翻译页。
- 从架构基础到 lifecycle governance 的八个部分。
- 可运行的参考包 `agent_runtime_ref`。
- 覆盖 traces、evals、policy bundles、approvals、memory 与 lifecycle artifacts 的参考页面。
- 实战案例、检查清单、policy templates 与 glossary。

## 这本书不打算成为什么

它不是某个框架的手册，不是 prompt tricks 合集，也不是 AI 市场巡礼。本书站在具体 SDK 和 platform docs 之上，去回答更棘手的问题：agent 到底该被允许做什么，write path 应该怎样受限，应该观察什么，变更应该怎样发布，系统上线后到底谁负责。

## 接下来去哪里

<div class="button-stack" markdown="1">

[从这里开始](start-here.zh.md){ .md-button .md-button--primary }
[进入第一部分](book/part-i/index.zh.md){ .md-button }
[打开参考包](appendix/reference-package.zh.md){ .md-button }

</div>
