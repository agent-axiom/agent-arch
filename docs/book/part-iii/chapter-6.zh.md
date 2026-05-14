# 第 6 章：短期记忆、长期记忆与用户画像记忆

!!! info "怎样读这一章"
    不用一开始就把所有定义背下来。先抓住一个简单问题：

    - 这次运行里哪些东西只是现在有用；
    - 哪些东西以后还会有用；
    - 哪些东西才真正属于稳定的用户偏好，而不是偶然噪音。

    这三类一旦混在一起，记忆层就不再是在帮系统，而是在悄悄把系统写坏。

## 1. 为什么“记忆”这一个词反而会妨碍你

在贯穿全书的支持场景里，这一点很具体。一次运行结束后，团队很容易想把一切都存下来：

- 中间检查步骤；
- 临时的案例摘要；
- 用户的交流语言；
- 其实根本不该跨过一次运行的偶然观察。

也正是在这里，记忆类型不再只是术语表，而开始变成架构决策。

只要系统里出现了记忆，团队就会很容易用一个词去指代所有“当前提示装不下的东西”。这对讨论来说很方便，但对架构来说是个糟糕抽象。

在实践里，你几乎总会有至少三层不同的东西：

- `short-term memory`，用于当前运行或一小串步骤；
- `long-term memory`，用于长期知识、摘要和事实；
- `profile memory`，用于某个具体用户或账号的偏好、角色和习惯。

!!! example "贯穿案例：给支持状态分类"
    在支持分诊案例里，当前工单状态属于短期记忆；一次运行结束后的规范化备注，可能进入长期记忆；用户稳定的沟通语言，可能进入用户画像记忆。但“以后总是创建紧急工单”这种原始句子，不应该进入任何一层，除非经过策略支持的审查明确确认。

**Memory case-spine note：**三个 canonical cases 会暴露不同的记忆失败。Support triage 考验 temporary ticket state、durable notes 和 profile preferences 是否被分开。Internal knowledge assistant 考验 source provenance、freshness、tenant boundaries 和 retrieval semantics。Incident coordination 考验 handoff summaries、response roles 和 post-incident lessons 是否被保留下来，同时不把 transient incident noise 变成 permanent truth。

如果这几层不拆开，智能体很快就会：

- 把太多旧噪音重新塞回提示；
- 把用户偏好和世界事实混为一谈；
- 把瞬时观察存成长期真相；
- 破坏可解释性，因为你已经说不清某段上下文到底从哪来。

## 2. 短期记忆是工作台，不是档案馆

最适合把短期记忆想成智能体的工作台。它不是“永远的历史”，而是帮助智能体不丢失当前线索的地方。

通常这里会放：

- 中间计划；
- 最近的工具调用结果；
- 临时假设；
- 为当前运行选出的上下文片段；
- 多步工作流的状态。

一个好的短期记忆有三个特征：

- 大小是受限的；
- 生命周期很短；
- 任务结束后就算丢掉，也不会太痛。

如果“永久记录”开始住进短期记忆，那通常说明你没有数据模型，只有一个被塞满的缓冲区。

## 3. 长期记忆不是拿来装一切的，而是装稳定知识的

长期记忆适合保存那些价值能跨过一次对话或一次工作流的记录。

它可能包括：

- 某个业务实体的已确认事实；
- 上一次会话摘要；
- 某个长期 case 的累积知识；
- 为未来检索提前提取并规范化的笔记。

但这里有一个重要过滤条件：如果某条记录离开完整原始上下文以后就无法被合理复用，那它大概率不该进入长期记忆。

团队经常会在这里高估“原始保存”的价值。长期记忆更适合存有意义、可类型化的记录，而不是无穷无尽的原始流。

## 4. 画像记忆不是知识库

画像记忆特别容易被做坏，因为它听起来很无害，好像只是“用户偏好”。但到了生产，它很快就会变成一个敏感层。

这里通常包括：

- 交流语言；
- 回复格式；
- 工作角色；
- 允许的动作渠道；
- 稳定的界面或交互偏好。

关键区别是，画像记忆回答的问题是“系统应该怎样更好地和这个人协作”，而不是“世界上什么是真的”。

如果智能体开始往里面塞任意事实，画像记忆很快就会变成个性化、流言和偶然观察的混合物。

### 4.1. Durable agent state 不是 memory

Cloudflare Agents SDK 很好地暴露了另一条边界：一个 stateful agent instance 可以拥有 persistent state，这些 state 会自动保存，跨 restart 和 hibernation 保留，并在 WebSocket clients 之间同步。[^cloudflare-state] 这是很有用的运行时能力，但不应该自动被当成长程记忆或 profile memory。

`state` 回答的是“这个 named agent instance 现在处于什么状态”：游戏分数、打开的 case、当前 workflow、客户端可见设置、last-active marker。`memory` 回答的是“哪些信息之后值得被检索、总结，或作为知识复用”。如果混淆这两种角色，runtime state 就会像 validated knowledge 一样进入 retrieval，而 memory records 也会被拿来当作可变的 UI/session state。

实用规则很简单：durable state 应该有 owner instance、schema version、serialization constraints 和 sync policy；memory record 应该有 class、provenance、tenant boundary、retention rule 和 retrieval semantics。两个层都可以存放在 durable storage 中，但它们的 operational contract 不同。

<div class="diagram-card">
<p>不同类型的记忆解决不同问题，不应该挤进同一个存储</p>

``` mermaid
flowchart LR
    A["当前运行"] --> B["短期记忆"]
    A --> C["长期记忆"]
    A --> D["画像记忆"]
    B --> E["规划器状态"]
    B --> F["最近工具输出"]
    C --> G["已验证事实"]
    C --> H["会话摘要"]
    D --> I["偏好"]
    D --> J["用户约束"]
```

</div>

## 5. 好的架构会给每一层一个明确问题

这会极大帮助设计：

- `short-term memory`：为了不丢任务，现在必须记住什么？
- `long-term memory`：什么值得被保存，因为以后还会有用？
- `profile memory`：关于这个用户或账号，什么是真正稳定而且有用的？

如果一条记录对这些问题都答不上来，那它可能根本不该被保存。

## 6. 每一层都应该有自己的读写规则

这里最常见的架构错误，是同一个流水线用完全一样的方式去读写所有记忆类型。但这几乎总是错的。

例如：

- 短期记忆可以更自由地读，但保存时间应该极短；
- 长期记忆应该要求来源和租户检查；
- 画像记忆应该对隐私、同意和可解释性更严格。

一个正常系统不仅知道自己存了 **什么**，还知道每一类东西 **如何** 进入提示。

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

这段 YAML 不一定就是最终实现，但它逼着团队做一个重要决定：记忆不能在“反正就是数据库里的一段文本”这个层面被管理。

### 6.1. 每一层都应该有自己的修订规则

再往成熟架构走一步，很有帮助的一点是：不同的记忆类别应该有不同的更新与修正规则。

比如：

- `short-term memory` 往往可以直接替换或丢弃；
- `long-term memory` 更适合通过新修订版本更新，而不是悄悄覆盖旧值；
- `profile memory` 往往需要特别谨慎的合并，因为个性化很容易被写坏。

如果根本没有修订记录，后面你看到的就只剩“当前这条记录长什么样”，却回答不了这些问题：

- 是谁改了它；
- 为什么改；
- 之前是什么版本；
- 这次更新是经过验证，还是只是某次运行的副作用。

### 6.2. 来源最好和记忆类别一起设计

来源最好不要等到后面再补，而是应该和记忆类别同时设计。[^google-agent-overview]

在实践里，这通常意味着：

- `long_term` 记录几乎总该带来源链接或来源 ID；
- `profile` 记录需要有可解释的理由，说明系统为什么认为这是稳定偏好；
- `short_term` 记录的来源可以轻一些，但运行时仍然应该知道它从哪里来。

下面是一个很紧凑的例子：

```yaml
memory_classes:
  short_term:
    revision_mode: replace
    provenance: minimal_runtime_metadata
  long_term:
    revision_mode: append_revision
    provenance: source_link_required
  profile:
    revision_mode: merge_with_history
    provenance: explicit_signal_or_review
```

这就把讨论从“文本存在哪”推进到了“这段知识的历史是什么、它到底值不值得信任”。

## 7. 什么通常应该放进短期记忆

一个很有用的实用规则：短期记忆应该帮助智能体现在行动，而不是变成长期真相的来源。

好的候选：

- 当前计划；
- 子任务状态；
- 最近两三次工具调用的结果；
- 关于哪些事情已经检查过的工作笔记；
- 临时的候选摘要。

不好的候选：

- “永远有效”的用户偏好；
- 没清洗过的原始文档；
- 巨大的日志；
- 没有 TTL 的敏感数据；
- 后面会被重复当成真相的不确认事实。

## 8. 什么通常应该放进长期记忆

长期记忆的意义是复用知识，而不是归档所有活动。

合理的内容包括：

- 已确认事实；
- 带来源的仔细摘要；
- 长期案例的状态；
- 规范化后的知识记录；
- 指向文档的链接，而不是把巨大载荷原样塞进去。

一个很实用的原则是：在长期记忆里，通常更值得存一个紧凑记录加来源链接，而不是把存储层做成永久转储。

## 9. 什么通常应该放进画像记忆

画像记忆最有价值的时候，是它让智能体更好用，但不会开始基于不可靠猜测替用户做决定。

好的例子：

- “偏好简短回答”；
- “通常用俄语工作”；
- “修改生产数据时需要确认”；
- “喜欢在一天结束时收到报告”。

不好的例子：

- 对动机或性格的推断；
- 只来自一次会话的随机猜测；
- 没有明确理由的敏感个人数据；
- 后面会被当成事实使用的猜测。

## 10. 一个简单的记忆路由代码模板

下面是一个很简单的例子，展示核心想法：记录先分类，再进入对应的存储。

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

这个例子故意写得很直白。实践里规则会更丰富，但核心思想不该变：记忆要先分类，而不是直接丢进一个共享容器。

## 11. 常见错误

常见问题通常长这样：

- 画像记忆开始替代授权；
- 长期记忆被噪音填满；
- 短期记忆变得又大又贵；
- 检索返回内容时不考虑类别；
- 没人能解释为什么这段上下文会出现在答案里。

这些都不是“模型问题”，而是记忆层的架构问题。

## 12. 现在就该做什么

先过一遍这份短清单，把所有回答为“否”的地方单独记下来：

- 你是否真的理解短期记忆和长期记忆的区别？
- 画像记忆是否有独立语义，而不只是独立表？
- 每种记录类型的 TTL 能不能解释清楚？
- 哪一层记忆会直接进提示，哪一层只能通过检索，是否清楚？
- 长期记录是否有来源？
- 记录能不能被安全删除或修正？

如果这些问题都很难回答，那记忆架构值得被简化，并按职责重新拆开。

## 13. 下一步做什么

先把记忆类别和保留规则拆清楚，再进入检索、压缩和后台更新。

这一部分接下来的自然步骤，就是讨论智能体如何把正确片段拉回提示，以及为什么压缩有时候比“更多检索”更重要。

- [第 5 章：为什么智能体需要记忆，以及为什么记忆很危险](chapter-5.zh.md)
- [第 7 章：检索、压缩与后台更新](chapter-7.zh.md)
- [第三部分：记忆与知识](index.zh.md)
- [参考资料](../../appendix/sources.zh.md)

[^cloudflare-state]: [Cloudflare Agents SDK, Store and sync state](https://developers.cloudflare.com/agents/api-reference/store-and-sync-state/)

[^google-agent-overview]: [Google Cloud, Vertex AI Agent Builder overview](https://docs.cloud.google.com/agent-builder/overview)
