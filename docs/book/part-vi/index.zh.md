# 第六部分：组织模型

到这里，我们已经搭好了大部分技术骨架：

- 架构；
- 安全；
- 记忆；
- 执行层；
- 可观测性和评测闭环。

但接下来，瓶颈通常不再是技术，而是组织本身。

即使是一个不错的智能体平台，也很快会遇到这些问题：

- 谁拥有底层能力；
- 谁负责策略与护栏；
- 产品团队如何使用平台而不把它弄碎；
- 怎么避免公司内部出现五套互不兼容的智能体运行时。

这一部分我们会讨论组织运作方式：谁负责什么，黄金路径应该怎么做，以及怎样避免把平台做成一堆分散的本地方案。

!!! info "这一部分的快速路线"
    如果你想快速读完关键部分，可以这样走：

    - [第 14 章](chapter-14.zh.md)：先看 platform ownership 和 product ownership 的边界在哪里；
    - [第 15 章](chapter-15.zh.md)：再看这条边界怎样落成 golden paths 和 shared gateways；
    - [第七部分](../part-vii/index.zh.md)：最后看组织模型怎样在参考实现里被固定下来。

    这三步合在一起，说明 operating model 不是给组织结构图看的，而是用来稳住整套 production system 的。

## 这一部分解决什么问题

## 本部分内容

- [第 14 章：平台团队与产品团队](chapter-14.zh.md)
  这一章继续同一个 support 场景，但切到 ownership 层：runtime、policies、gateways 和 platform incidents 到底该由谁负责。
- [第 15 章：黄金路径、共享网关与反动物园模式](chapter-15.zh.md)

## 这一部分之后去哪里

这一部分之后，下一步就是进入 [第七部分](../part-vii/index.zh.md)：把 ownership 边界、golden paths 和 shared gateways 继续固定进 reference implementation、policy layer 和 rollout skeleton。
