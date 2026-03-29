# 第六部分：组织模型

到这里，我们已经搭好了大部分技术骨架：

- 架构；
- 安全；
- 记忆；
- execution layer；
- observability 和 eval loop。

但接下来，瓶颈通常不再是技术，而是组织本身。

即使是一个不错的 agent platform，也很快会遇到这些问题：

- 谁拥有底层能力；
- 谁负责 policy 和 guardrails；
- 产品团队如何使用平台而不把它弄碎；
- 怎么避免公司内部出现五套互不兼容的 agent runtime。

这一部分我们会聊 operating model：谁负责什么，golden path 应该怎么做，以及怎样避免把平台做成一堆分散的本地方案。

## 本部分内容

- [第 14 章：Platform Team vs Product Teams](chapter-14.zh.md)
- [第 15 章：Golden Paths、Shared Gateways 与 Anti-Zoo Patterns](chapter-15.zh.md)

这一部分之后，最自然的下一步就是补完 platform roadmap，然后进入 reference implementation。
