# 第三部分：记忆与知识

到了这个阶段，你的智能体已经不只是会推理，也不只是能安全地走到动作边界。在同一个支持场景里，接下来会出现一个新的诱惑：给它加上记忆，这样它就不用每次运行都从零开始，也能保留用户历史。

!!! info "这一部分的快速路线"
    如果你想快速读完关键部分，可以这样走：

    - [第 5 章](chapter-5.zh.md)：先理解为什么记忆本身就有风险；
    - [第 6 章](chapter-6.zh.md)：把不同类型的记忆按职责拆开；
    - [第 7 章](chapter-7.zh.md)：再决定这些记录怎样安全地回到提示里。

    这三步合在一起，才构成一个可以被当作工程系统讨论的记忆层，而不是一句“给智能体加记忆”。

!!! note "Part III canonical case routes"
    在 memory/retrieval layer 中，三个 canonical cases 会检查不同风险。**Support triage** 检查 temporary ticket state、duplicate-ticket context 和 approved playbook retrieval。**Internal knowledge assistant** 检查 source attribution、freshness window、tenant boundary 和 memory provenance。**Incident coordination** 检查 incident timeline、owner handoff summaries、escalation status 和 post-incident lessons。

<div class="book-cover" markdown="1">

![记忆与知识部分封面](../../assets/images/part-iii-memory.png)

</div>

## 这一部分解决什么问题

这一步是对的，但也正是在这里，很多系统开始悄悄积累技术债。对于这个支持智能体来说，如果记忆层不是受控层，原本有价值的状态很快就会变成持久错误来源。

- 什么都往记忆里存；
- 不区分用户画像记忆和工作上下文；
- 把不可信文本不加检查地重新塞回提示；
- 直接在热路径写记忆，一次错误立刻变成持久状态。

这一部分我们会拆解，怎样让记忆真正有用，而不是把它做成一个长期存在的注入源、泄漏源和怪异行为来源。

## 本部分内容

- [第 5 章：为什么智能体需要记忆，以及为什么记忆很危险](chapter-5.zh.md)
- [第 6 章：短期记忆、长期记忆与用户画像记忆](chapter-6.zh.md)
  这一章继续同一个支持场景，讲的是团队应该把运行结束后的哪些东西留下来，哪些东西绝不能固化进记忆。
- [第 7 章：检索、压缩与后台更新](chapter-7.zh.md)

## 这一部分之后去哪里

读完这一部分之后，下一步自然就是 [第四部分](../part-iv/index.zh.md)：同一个智能体不仅要记住上下文，还要通过受控工具、沙箱和执行契约去真正做事。
