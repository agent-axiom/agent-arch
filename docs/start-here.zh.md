# 从这里开始

如果你是第一次来到这本书，不需要从头到尾线性阅读。它不是小说，也不是“把整个 AI 世界都讲一遍”的综述。它更像一本实践手册，讨论的是如何构建安全、可控、可运营的 AI 智能体，而不是把项目变成一堆 prompt、脚本和侥幸心理。

这页存在的目的有两个：

- 让你快速判断这本书是否适合你；
- 帮你为自己的角色找到一条最短阅读路径。

## 这本书适合谁

如果你属于下面这些角色，这本书会特别有帮助：

- 正在把智能体能力接入产品的工程师；
- 想搭建共享 runtime 和 policy layer 的平台工程师；
- 需要分析 trust boundaries 和高风险执行路径的安全工程师；
- 试图让智能体系统具备 production discipline 的技术负责人或架构师；
- 寻找实践型 open handbook，而不是 AI 营销页面的开源贡献者。

如果你要的是一个冷静、成熟、可解释的系统，而不是“世界上最自主的智能体”，那你来对地方了。

## 30 分钟能带走什么

如果你时间不多，我建议按这个顺序读：

1. [第 1 章：为什么智能体需要平台，而不是魔法](book/part-i/chapter-1.zh.md)
2. [第 3 章：安全边界与信任边界](book/part-ii/chapter-3.zh.md)
3. [第 8 章：执行模型与工具目录](book/part-iv/chapter-8.zh.md)
4. [第 11 章：追踪、跨度与结构化事件](book/part-v/chapter-11.zh.md)
5. [第 18 章：生产上线检查清单](book/part-vii/chapter-18.zh.md)

读完这五章，你就已经能得到：

- 一套可工作的架构框架；
- 一套 trust boundaries 模型；
- 对安全 tool execution 的基本理解；
- 一套 observability 基线；
- 一套 production go-live discipline。

## 按角色推荐阅读路径

### 如果你是产品工程师

建议按这个顺序读：

1. [第一部分：基础](book/part-i/index.zh.md)
2. [第二部分：安全边界](book/part-ii/index.zh.md)
3. [第四部分：工具与执行](book/part-iv/index.zh.md)
4. [第七部分：参考实现](book/part-vii/index.zh.md)

这条路径的目标，是尽快从一个 agent idea 走到 runnable architecture。

### 如果你是平台工程师

建议按这个顺序读：

1. [第 2 章：安全智能体的参考架构](book/part-i/chapter-2.zh.md)
2. [第三部分：记忆与知识](book/part-iii/index.zh.md)
3. [第四部分：工具与执行](book/part-iv/index.zh.md)
4. [第五部分：可靠性与可观测性](book/part-v/index.zh.md)
5. [第七部分：参考实现](book/part-vii/index.zh.md)

这条路径的目标，是搭出 platform-grade skeleton，而不只是一个 agent wrapper。

### 如果你是安全工程师

建议按这个顺序读：

1. [第二部分：安全边界](book/part-ii/index.zh.md)
2. [第 5 章：为什么智能体需要记忆，以及它为何危险](book/part-iii/chapter-5.zh.md)
3. [第 9 章：沙箱执行与 MCP 作为集成契约](book/part-iv/chapter-9.zh.md)
4. [第 10 章：幂等性、重试、速率限制与回滚边界](book/part-iv/chapter-10.zh.md)
5. [第 18 章：生产上线检查清单](book/part-vii/chapter-18.zh.md)

这条路径的目标，是不仅理解 prompt risks，还要真正理解 execution risks。

### 如果你是负责人或架构师

建议按这个顺序读：

1. [第 1 章：为什么智能体需要平台，而不是魔法](book/part-i/chapter-1.zh.md)
2. [第五部分：可靠性与可观测性](book/part-v/index.zh.md)
3. [第六部分：组织模型](book/part-vi/index.zh.md)
4. [第 18 章：生产上线检查清单](book/part-vii/chapter-18.zh.md)

这条路径的目标，是理解如何避免一个智能体项目在运营和 ownership 层面失控。

## 如果你更想先看代码

如果 runnable artifacts 比线性阅读更重要，可以从这里开始：

- [参考包](appendix/reference-package.zh.md)
- [第 16 章：基础运行时蓝图](book/part-vii/chapter-16.zh.md)
- [第 17 章：策略层与能力目录](book/part-vii/chapter-17.zh.md)

这些内容已经能给你：

- 最小 runtime；
- policy layer；
- capability catalog；
- memory path；
- telemetry；
- rollout checks。

## 如果你更想看模板和项目方向

建议先看这些页面：

- [全书计划](book/plan.zh.md)
- [社区路线图](appendix/community-roadmap.zh.md)
- [参考来源](appendix/sources.zh.md)

这是最快理解项目未来方向，以及它如何服务更大社区的方式。

## 这本书和别的内容有什么不同

这本书的立场很明确：

- workflow 比魔法更重要；
- 安全比炫目的 demo 更重要；
- execution layer 比“聪明的 tool calling”更重要；
- observability 比“好像能跑”更重要；
- platform thinking 比一堆局部 agent hacks 更重要。

所以这不是一本关于“最自主智能体”的书，而是一本关于成熟、安全、可解释 agent platform 的书。

## 下一步去哪里

如果你想马上开始：

- [打开全书计划](book/plan.zh.md){ .md-button .md-button--primary }
- [进入第一部分](book/part-i/index.zh.md){ .md-button }
- [查看参考包](appendix/reference-package.zh.md){ .md-button }

如果你想参与贡献：

- [Contributing guide](https://github.com/agent-axiom/agent-arch/blob/main/CONTRIBUTING.md)
- [社区路线图](appendix/community-roadmap.zh.md)
