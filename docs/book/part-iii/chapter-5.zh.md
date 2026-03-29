# 第 5 章：为什么智能体需要记忆，以及为什么记忆很危险

## 1. 为什么没有记忆的智能体很快会撞到天花板

如果一个 agent 没有 memory，那么每一次新的 run 几乎都像从白纸开始。对于简单任务这还能忍，但到了真实场景很快就会出问题：

- agent 记不住用户偏好；
- 它会忘掉自己一分钟前做过什么；
- 同样的事实一遍又一遍重新去拉；
- 它无法平滑地接续一个长流程。

所以 memory 看起来像下一个自然步骤。这没错。但这里有一个重要分叉：memory 既可以让 agent 更有用，也可以让整套系统变得更不可预测。

## 2. 记忆不是一个盒子，而是几层不同的东西

当团队说“我们来加 memory”时，通常混在一起的其实是几种不同的东西：

- 短生命周期的 run working context；
- user profile 和稳定偏好；
- 关于世界和业务实体的提取事实；
- 过去会话的 summaries；
- execution artifacts，比如 trace notes 或 tool outputs。

如果这些都被塞进同一个地方，混乱会很快发生。所以第一条规则很简单：不要把 memory 设计成一个抽象 storage。要把它设计成几种不同的边界，它们有不同的生命周期、信任等级和写入规则。

<div class="diagram-card">
<p>更适合把 agent memory 理解为几层，而不是一整个数据库</p>

``` mermaid
flowchart TD
    A["User request"] --> B["Session context"]
    B --> C["Planner / runtime"]
    C --> D["Short-term working memory"]
    C --> E["Profile memory"]
    C --> F["Knowledge retrieval"]
    D --> G["Prompt assembly"]
    E --> G
    F --> G
    G --> H["Model response"]
```

</div>

## 3. 最大的错误：把 memory 当成单纯的便利功能

Memory 有一个很烦的性质：它能活过单次 run。这意味着，一次写入错误的寿命，会比单次模型回答错误更长。

如果 agent 曾经：

- 把一个错误事实存成“用户偏好”；
- 把一段不可信文本写进了 profile memory；
- 把敏感文档片段带进 summary；
- 把不该返回给该 tenant 的东西写进 retrieval store，

那问题就变成 persistent 了。你不一定能在单条 trace 里看到它。它会在后面的别的对话、别的 prompt 里重新冒出来，有时甚至影响到别的用户。

所以，memory write path 必须被视为 security-sensitive path，而不是“一个小技术细节”。

## 4. 记忆也有自己的 trust boundaries

把 memory 看成 trust boundary，而不是中性存储，会很有帮助。

至少有四种不同的数据来源：

- trusted system annotations；
- internal services 的 validated outputs；
- user-provided content；
- 来自 external tools 或 documents 的内容。

这些不是同一种东西。如果你保存时不标记来源，后面的 runtime 就没法判断，哪些内容可以作为 instruction-grade context，哪些只能作为 reference。

一个正常规则大致是：

- trusted metadata 可以进入 policy decisions；
- user content 不应该突然变成 system instruction；
- retrieved text 在被证明之前都应该视为 untrusted；
- summaries 同样有 provenance，不是“默认真相”。

## 5. 最危险的一条路：在 hot path 里不加过滤直接写 memory

团队很容易这么做：模型一答完，runtime 立刻 `save_memory()`，然后把这当作一种方便的自动化。短期看起来很顺手，长期几乎总会出问题。

为什么危险：

- 写入发生在 latency 压力下；
- 没人验证什么才算 memory-worthy；
- 没有规范化和清理步骤；
- 没有 tenant isolation policy；
- 很难解释为什么某个事实会进入 memory。

所以即使是很“聪明”的 agents，也最好遵循一个很无聊但很有用的原则：默认情况下，写入 long-term memory 必须要么被 policy 明确允许，要么被移到 background pipeline。

下面是一个简单例子：

```python
from dataclasses import dataclass


@dataclass
class MemoryCandidate:
    kind: str
    tenant_id: str
    content: str
    source: str
    contains_pii: bool = False


def should_persist(candidate: MemoryCandidate) -> bool:
    if candidate.kind not in {"profile_preference", "validated_fact", "session_summary"}:
        return False
    if candidate.source not in {"trusted_service", "approved_summarizer"}:
        return False
    if candidate.contains_pii:
        return False
    return True
```

这段代码故意写得很简单。它的力量不在“聪明”，而在于规则是可见、可审计的。

## 6. 一个好的 memory system 写得比你想象中更少

一开始，几乎每个人都会觉得 memory 应该多多益善。但在实践里，一个好的 memory system 通常赢在筛选严格，而不是数量巨大。

通常值得写入的东西应该满足：

- 对未来的 runs 有用；
- 有明确的 owner 和 tenant；
- 能向人解释清楚；
- 不携带多余敏感数据；
- 不会把 prompt 变成垃圾堆。

每次写入前一个很有用的问题是：“如果这段内容三周后在别的上下文里再次出现，我能舒服地解释清楚它为什么在这里吗？”

如果这个答案都不太稳，那大概率就不该写。

## 7. Memory 影响的不只是质量，还有安全

这也是为什么 memory 不只是 UX 话题：

- 它会影响数据泄漏；
- 它会改变 prompt injection 的攻击面；
- 它会制造长期错误；
- 它会让 incident 调查变难；
- 它会抬高 provenance、retention 和 deletion 的要求。

在一个设计良好的平台里，memory subsystem 通常会有：

- 分开的 record types；
- retention rules；
- 清晰 ownership；
- provenance metadata；
- 删除和纠正机制；
- persistent write 前的 policy gates。

这已经不是“聊天历史”了，而是一个真正的架构层。

## 8. 一个最小可用的 memory write policy

如果你想从不过度复杂的方式开始，可以把 memory write policy 想成这样：

```yaml
memory:
  allowed_kinds:
    - profile_preference
    - validated_fact
    - session_summary
  deny_sources:
    - raw_user_prompt
    - external_html
    - unvalidated_tool_output
  require_tenant_id: true
  reject_if_contains:
    - secrets
    - access_tokens
    - payment_card_data
  write_mode:
    profile_preference: background_review
    validated_fact: immediate_if_trusted
    session_summary: background_only
```

这依然不是魔法，而是让写入路径变得可见、可控、可讨论。

## 9. 如果你现在还没有 memory，该从哪里开始

如果你刚开始接触这个主题，一个不错的顺序是：

1. 先把 session context 和 persistent memory 分开。
2. 然后定义哪些 record types 是允许存在的。
3. 再加 provenance 和 tenant metadata。
4. 最后才去自动化 write path。

如果反过来做，memory 很快就会变成平台把所有没设计清楚的东西都丢进去的地方。

## 10. 接下来读什么

这一部分后面的章节会继续拆解：

- short-term memory 和 long-term memory 到底差在哪；
- 为什么 profile memory 应该和 retrieval store 分开；
- 为什么 summaries 更适合放到 background 更新；
- compaction 如何帮你保持上下文干净。

目前最重要的 takeaway 很简单：只有当 memory 被设计成一个受控的系统层，而不是无节制堆文本的地方时，它才真正有用。

- [第三部分：记忆与知识](index.zh.md)
- [第 6 章：Short-Term、Long-Term 与 Profile Memory](chapter-6.zh.md)
- [第 4 章：Tool Gateway、Approval 与 Audit Trail](../part-ii/chapter-4.zh.md)
- [参考资料](../../appendix/sources.zh.md)
