# 为什么需要这本书

关于 AI agents 的材料已经很多了。真正更少的是那些把 agent system 当成必须在 production 里被设计、约束、发布、调查和维护的系统来讨论的材料。

这本书就是为了补上这个缺口。

## 它不是什么

它不是：

- 某个框架的手册；
- 某个 vendor 产品的指南；
- prompt 集合；
- benchmark 和 AI 新闻巡礼；
- 没有架构模型的 security checklist。

## 它想做什么

这本书把 agent systems 看成受治理的 production systems，它们应该具备：

- trust boundaries；
- 受 policy 约束的 execution；
- 面向 risky actions 的 approvals；
- memory 与 context discipline；
- traces、SLO 与 evals；
- rollout control、ownership 与 lifecycle governance。

它的主要目标不是帮助人们做出“最自主的 agent”，而是帮助他们做出一个在运行中值得信任的系统。

## 和框架文档相比

框架文档在你已经知道自己想构建什么系统时非常有用。它们通常很擅长解释 orchestration patterns、state graphs、SDK usage 和 integration details。

但它们很少回答这类问题：

- agent 到底该被允许做什么；
- 哪些 actions 必须经过 approval；
- memory 应该怎样被约束；
- 怎样在不失去控制的前提下发布 changes；
- incident 之后应该怎样做 review。

这本书试图站在框架之上，而不是和框架争论。

## 和 vendor docs 相比

Vendor docs 往往给出通往 demo 的最短路径。这当然有用，但它天然受限于单一 vendor 的 surface。

这本书试图让架构站在 product surface 之上，并把更稳定的工程纪律和变化更快的 platform tooling 分开。

## 和 security checklist 方法相比

Checklist approach 是必要的，但它本身并不会自动变成一套可工作的架构。它会告诉你该看哪里，却不会告诉你怎样把 runtime、approvals、telemetry、ownership 和 lifecycle 连接成一个受治理的 contour。

这正是这本书试图完成的事情。

## 希望达到什么结果

读完这本书后，读者应该：

- 看清 trust 与 action boundaries 真正在哪里；
- 理解如何捕获 run behavior，而不是只从症状去猜；
- 知道怎样定义 health 与 risk budgets；
- 知道怎样产出关于 quality 与 regression risk 的 reviewable judgments；
- 能把 rollout、response、lineage 与 accountability 区分成不同的 operational functions。

如果这些问题比另一篇 agent theater 更接近你的现实，那么这本书就是为你写的。
