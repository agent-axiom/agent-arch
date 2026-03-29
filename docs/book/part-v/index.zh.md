# 第五部分：可靠性与可观测性

到这里，我们已经有了：

- 架构框架；
- 安全边界；
- 记忆与 retrieval；
- 带 contracts、sandbox 和 side-effect discipline 的 execution layer。

接下来就会碰到一个更成熟的问题：你到底如何真正理解这个 agent system 在现实里做了什么？

如果没有好的 observability，再强的架构也会很快退化成猜测：

- 为什么某个 run 变贵了；
- workflow 到底在哪一层坏掉了；
- 哪个 policy gate 触发了；
- 是哪个 tool 给出了坏结果；
- 为什么用户会收到这个具体回答。

这一部分会拆解如何构建 traces、SLO 和 eval loops，让 agent system 不只是“能上线”，而是真正可以被稳定运营。

## 本部分内容

- [第 11 章：追踪、跨度与结构化事件](chapter-11.zh.md)
- [第 12 章：智能体系统的 SLO](chapter-12.zh.md)
- [第 13 章：离线评测、在线评测与回归门禁](chapter-13.zh.md)

Part V 现在已经形成一个完整的 operational block；下一步自然就是组织模型和平台 operating model。
