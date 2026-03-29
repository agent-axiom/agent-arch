# 第 6 章：Short-Term、Long-Term 与 Profile Memory

## 1. 为什么“memory”这一个词反而会妨碍你

只要系统里出现了 memory，团队就会很容易用一个词去指代所有“当前 prompt 装不下的东西”。这对讨论来说很方便，但对架构来说是个糟糕抽象。

在实践里，你几乎总会有至少三层不同的东西：

- `short-term memory`，用于当前 run 或一小串步骤；
- `long-term memory`，用于长期知识、summaries 和 facts；
- `profile memory`，用于某个具体用户或账号的偏好、角色和习惯。

如果这几层不拆开，agent 很快就会：

- 把太多旧噪音重新塞回 prompt；
- 把用户偏好和世界事实混为一谈；
- 把 transient observations 存成长期真相；
- 破坏 explainability，因为你已经说不清某段上下文到底从哪来。

## 2. Short-term memory 是工作台，不是档案馆

最适合把 short-term memory 想成 agent 的工作台。它不是“永远的历史”，而是帮助 agent 不丢失当前线索的地方。

通常这里会放：

- 中间计划；
- 最近的 tool call 结果；
- 临时 hypotheses；
- 为当前 run 选出的上下文片段；
- 多步 workflow 的状态。

一个好的 short-term memory 有三个特征：

- 大小是受限的；
- 生命周期很短；
- 任务结束后就算丢掉，也不会太痛。

如果“永久记录”开始住进 short-term memory，那通常说明你没有 data model，只有一个被塞满的 buffer。

## 3. Long-term memory 不是拿来装一切的，而是装稳定知识的

Long-term memory 适合保存那些价值能跨过一次对话或一次 workflow 的记录。

它可能包括：

- 某个业务实体的已确认事实；
- 上一次会话的 summary；
- 某个长期 case 的累积知识；
- 为未来 retrieval 提前提取并规范化的笔记。

但这里有一个重要过滤条件：如果某条记录离开完整原始上下文以后就无法被合理复用，那它大概率不该进入 long-term memory。

团队经常会在这里高估“原始保存”的价值。Long-term memory 更适合存有意义、可类型化的记录，而不是无穷无尽的原始流。

## 4. Profile memory 不是 knowledge base

Profile memory 特别容易被做坏，因为它听起来很无害，好像只是“用户偏好”。但到了 production，它很快就会变成一个敏感层。

这里通常包括：

- 交流语言；
- 回复格式；
- 工作角色；
- 允许的动作渠道；
- 稳定的界面或交互偏好。

关键区别是，profile memory 回答的问题是“系统应该怎样更好地和这个人协作”，而不是“世界上什么是真的”。

如果 agent 开始往里面塞任意事实，profile memory 很快就会变成 personalization、流言和偶然观察的混合物。

<div class="diagram-card">
<p>不同类型的记忆解决不同问题，不应该挤进同一个 storage</p>

``` mermaid
flowchart LR
    A["Current run"] --> B["Short-term memory"]
    A --> C["Long-term memory"]
    A --> D["Profile memory"]
    B --> E["Planner state"]
    B --> F["Recent tool outputs"]
    C --> G["Validated facts"]
    C --> H["Session summaries"]
    D --> I["Preferences"]
    D --> J["User constraints"]
```

</div>

## 5. 好的架构会给每一层一个明确问题

这会极大帮助设计：

- `short-term memory`：为了不丢任务，现在必须记住什么？
- `long-term memory`：什么值得被保存，因为以后还会有用？
- `profile memory`：关于这个用户或账号，什么是真正稳定而且有用的？

如果一条记录对这些问题都答不上来，那它可能根本不该被保存。

## 6. 每一层都应该有自己的读写规则

这里最常见的架构错误，是同一个 pipeline 用完全一样的方式去读写所有 memory types。但这几乎总是错的。

例如：

- short-term memory 可以更自由地读，但保存时间应该极短；
- long-term memory 应该要求 provenance 和 tenant checks；
- profile memory 应该对 privacy、consent 和 explainability 更严格。

一个正常系统不仅知道自己存了 **什么**，还知道每一类东西 **如何** 进入 prompt。

```yaml
memory_classes:
  short_term:
    ttl: "2h"
    read_path: "runtime_only"
    write_policy: "immediate"
  long_term:
    ttl: "90d"
    read_path: "retrieval_with_filters"
    write_policy: "validated_only"
  profile:
    ttl: "365d"
    read_path: "personalization_only"
    write_policy: "explicit_or_high_confidence"
```

这段 YAML 不一定就是最终实现，但它逼着团队做一个重要决定：memory 不能在“反正就是数据库里的一段文本”这个层面被管理。

## 7. 什么通常应该放进 short-term memory

一个很有用的 practical rule：short-term memory 应该帮助 agent 现在行动，而不是变成长期真相的来源。

好的候选：

- 当前计划；
- 子任务状态；
- 最近两三次工具调用的结果；
- 关于哪些事情已经检查过的 working notes；
- 临时的 candidate summaries。

不好的候选：

- “永远有效”的用户偏好；
- 没清洗过的原始文档；
- 巨大的日志；
- 没有 TTL 的敏感数据；
- 后面会被重复当成真相的不确认事实。

## 8. 什么通常应该放进 long-term memory

Long-term memory 的意义是复用知识，而不是归档所有活动。

合理的内容包括：

- 已确认事实；
- 带 provenance 的仔细 summaries；
- 长期 case 的状态；
- 规范化后的 knowledge records；
- 指向文档的链接，而不是把巨大 payload 原样塞进去。

一个很实用的原则是：在 long-term memory 里，通常更值得存一个紧凑 record 加 source 链接，而不是把存储层做成永久 dump。

## 9. 什么通常应该放进 profile memory

Profile memory 最有价值的时候，是它让 agent 更好用，但不会开始基于不可靠猜测替用户做决定。

好的例子：

- “偏好简短回答”；
- “通常用俄语工作”；
- “修改 production 数据时需要确认”；
- “喜欢在一天结束时收到报告”。

不好的例子：

- 对动机或性格的推断；
- 只来自一次会话的随机猜测；
- 没有明确理由的敏感个人数据；
- 后面会被当成事实使用的猜测。

## 10. 一个简单的 memory routing 代码模板

下面是一个很简单的例子，展示核心想法：记录先分类，再进入对应的 storage。

```python
from dataclasses import dataclass


@dataclass
class MemoryRecord:
    kind: str
    content: str
    confidence: float


def select_memory_bucket(record: MemoryRecord) -> str | None:
    if record.kind in {"plan_step", "tool_result", "working_note"}:
        return "short_term"
    if record.kind in {"validated_fact", "session_summary", "case_state"} and record.confidence >= 0.8:
        return "long_term"
    if record.kind in {"language_preference", "format_preference", "approval_preference"}:
        return "profile"
    return None
```

这个例子故意写得很直白。实践里规则会更丰富，但核心思想不该变：memory 要先分类，而不是直接丢进一个共享容器。

## 11. 团队最常坏在哪里

常见问题通常长这样：

- profile memory 开始替代 authorization；
- long-term memory 被噪音填满；
- short-term memory 变得又大又贵；
- retrieval 返回内容时不考虑 class；
- 没人能解释为什么这段上下文会出现在答案里。

这些都不是“模型问题”，而是 memory layer 的架构问题。

## 12. Practical Checklist

如果你想快速检查设计，可以问：

- 你是否真的理解 short-term memory 和 long-term memory 的区别？
- profile memory 是否有独立语义，而不只是独立表？
- 每种记录类型的 TTL 能不能解释清楚？
- 哪一层 memory 会直接进 prompt，哪一层只能通过 retrieval，是否清楚？
- 长期记录是否有 provenance？
- 记录能不能被安全删除或修正？

如果这些问题都很难回答，那 memory 架构值得被简化，并按职责重新拆开。

## 13. 接下来读什么

这一部分接下来的自然步骤，就是讨论 agent 如何把正确片段拉回 prompt，以及为什么 compaction 有时候比“更多 retrieval”更重要。

- [第 5 章：为什么智能体需要记忆，以及为什么记忆很危险](chapter-5.zh.md)
- [第 7 章：Retrieval、Compaction 与 Background Updates](chapter-7.zh.md)
- [第三部分：记忆与知识](index.zh.md)
- [参考资料](../../appendix/sources.zh.md)
