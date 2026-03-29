# 第三部分：记忆与知识

到了这个阶段，你的 agent 已经不只是会推理，也不只是能安全地调用工具。接下来会出现一个新的诱惑：给它加上 memory，这样它就不用每次 run 都从零开始。

这一步是对的，但也正是在这里，很多系统开始悄悄积累技术债：

- 什么都往 memory 里存；
- 不区分 profile memory 和工作上下文；
- 把不可信文本不加检查地重新塞回 prompt；
- 直接在 hot path 写 memory，一次错误立刻变成 persistent。

这一部分我们会拆解，怎样让 memory 真正有用，而不是把它做成一个长期存在的注入源、泄漏源和怪异行为来源。

## 本部分内容

- [第 5 章：为什么智能体需要记忆，以及为什么记忆很危险](chapter-5.zh.md)
- [第 6 章：Short-Term、Long-Term 与 Profile Memory](chapter-6.zh.md)
- [第 7 章：Retrieval、Compaction 与 Background Updates](chapter-7.zh.md)

再往后，就可以自然深入 retention、deletion 和 memory governance。
