# 第二部分：安全边界

如果说第一部分是在搭建基础架构图景，那么这一部分里，同一个支持智能体第一次真正走到高风险地带：接触数据、调用工具、执行带副作用的动作。

!!! info "这一部分的快速路线"
    如果你想快速读完关键部分，可以这样走：

    - [第 3 章](chapter-3.zh.md)：先看信任边界到底在哪里；
    - [第 4 章](chapter-4.zh.md)：再看系统在真正执行动作前必须在哪里停下；
    - [第 5 章](../part-iii/chapter-5.zh.md)：最后决定这种 run 结束后，智能体到底允许记住什么。

    这三步已经足够组成一个可工作的 production contour，而不只是安全术语表。

这一部分的意义，是避免你产生一个危险错觉，好像 agent 的安全可以“以后再补”。对这条贯穿全书的支持场景来说，正是在这里你会清楚看到：如果边界没有先定义好，智能体就会从“帮忙”滑向“制造新风险”。

- 如果 trust boundaries 没有提前定义好，agent 很快就会把多余上下文一起拖进来；
- 如果 tools 没有隔离，一个糟糕的调用就会变成真实 incident；
- 如果 policy、approval 和 audit 没有嵌进 runtime，团队会在最不合适的时候失去控制。

## 这一部分解决什么问题

- agent systems 关键威胁的地图；
- 一套实用的 security perimeter 模型；
- 一组控制点：ingress、prompt assembly、model gateway、retrieval、tools、egress；
- policy-as-code 和 gated execution 示例；
- 一个能和 security 团队认真讨论的基础，而不是只停留在抽象口号上。

## 本部分内容

- [第 3 章：安全边界与信任边界](chapter-3.zh.md)
- [第 4 章：Tool Gateway、Approval 与 Audit Trail](chapter-4.zh.md)
  这一章继续同一个 support 场景，讲的是系统准备把“判断”变成外部动作的那一刻。
- [第一部分：基础](../part-i/index.zh.md)
- [参考资料](../../appendix/sources.zh.md)

## 这一部分之后去哪里

这一部分之后，下一步自然就是进入 [第三部分](../part-iii/index.zh.md)：决定智能体到底允许记住什么，retrieval 怎样把上下文带回来，以及怎样不让记忆层变成新的风险来源。
