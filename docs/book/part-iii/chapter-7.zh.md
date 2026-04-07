# 第 7 章：Retrieval、Compaction 与 Background Updates

## 1. 如果你不会把正确内容重新取出来，memory 就没用

当你已经把 short-term、long-term 和 profile memory 分开之后，下一个现实问题就是：agent 到底应该怎样把需要的记录重新带回 prompt？

很多系统就是从这里开始退化的：

- prompt 里塞进太多不相关上下文；
- retrieval 返回的是“相似”，却不是“有用”；
- summaries 越来越长，却没有更清晰；
- 每一次新迭代都只让上下文变得更重。

也就是说，问题已经不再是“有没有 memory”，而是 memory 已经变得太吵、太贵、太难读了。

## 2. Retrieval 不是“找回所有相似内容”，而是“挑出对当前任务有帮助的内容”

Retrieval 有一个坏习惯：如果你不限制它，它就会变得过于慷慨。结果进入 prompt 的，不是最有帮助的内容，而是 embedding 或 keyword overlap 上最相似的内容。

对 production 系统来说，更有用的思路是：

- retrieval 不需要返回很多；
- retrieval 必须是可解释的；
- retrieval 必须尊重 tenant、source 和 trust boundaries；
- retrieval 必须服从上下文预算。

一个正常的 retrieval pipeline，几乎总会同时考虑：

- tenant isolation；
- memory class；
- recency；
- confidence；
- provenance；
- policy filters。

## 3. 一个好的 prompt 爱的是高密度信号，不是完整性

人很容易以为“上下文越多，agent 越聪明”。实践里，情况往往相反：你塞进 prompt 的噪音越多，模型越难抓住真正的优先级。

所以 retrieval 回答的应该不是“我们能取出什么”，而是“什么能在此刻提高正确决策的概率”。

一个很有用的 practical rule：

- 3 条高度相关记录，通常比 20 条勉强相似记录更好；
- 一个带来源的小 summary，通常比长原始文档更好；
- 一个 profile hint，通常比整段偏好历史更好；
- 空 retrieval，通常比不可信且不可解释的 retrieval 更好。

## 4. Compaction 不是美容，而是保持系统可工作的手段

如果 memory layer 只会增长，那么 prompt assembly 迟早会变成一个没有规则的垃圾收集器。这就是为什么 compaction 必须是架构的一部分，而不是某次专项清理工程。

Compaction 可以意味着很多事：

- 把几条记录压成一个 summary；
- 删除过期的 working notes；
- 合并重复项；
- 把大 blob 替换成规范化 record 加 source link；
- 让旧记录降权，而不是永远留在前景里。

<div class="diagram-card">
<p>更适合把 retrieval 和 compaction 看成一整个 memory maintenance 循环</p>

``` mermaid
flowchart TD
    A["New run"] --> B["Query memory"]
    B --> C["Apply filters and ranking"]
    C --> D["Assemble prompt context"]
    D --> E["Model + tools"]
    E --> F["Create new memory candidates"]
    F --> G["Background compaction and review"]
    G --> H["Normalized memory store"]
    H --> B
```

</div>

## 5. 不是所有 memory 更新都应该发生在 hot path

这是 agent systems 里最有价值的架构转变之一。起初，几乎所有人都想把 memory 做成“立刻就好”：agent 看见了什么，就立刻重写 summary、更新 profile、保存 knowledge。

但这通常既昂贵又危险。

通常适合留在 hot path 里的：

- 最小 session state；
- 简短 working notes；
- 带清晰 TTL 的安全 transient records；
- 如果不更新，当前 workflow 就真的会断掉的内容。

通常更适合放到 background 的：

- 长会话的 compaction；
- summaries 重建；
- facts 规范化；
- deduplication；
- persistent write 前对 memory candidates 的复查。

Background updates 让 memory 变得整洁，而不只是“反应很快”。

## 6. 好系统会把 retrieval query 和 maintenance jobs 分开

在成熟架构里，几乎总会有两条不同路径：

- read path：为当前 run 快速而安全地取回上下文；
- maintenance path：不受 latency 压力地慢慢改进 memory store。

这不仅是性能问题，也是决策质量问题。当同一条链同时：

- 执行任务；
- 重建 summaries；
- 写 profile memory；
- 清理重复项；
- 更新 ranking metadata，

它很快就会变得脆弱且难以解释。

## 6.1. Frontier memory 正在走向 adaptive shaping，但 production 仍然需要纪律

最新的 memory research 正在把架构继续往前推：不只是存 records、偶尔做 compaction，而是试图根据真实使用模式逐步重塑整个 memory layer。

这很有吸引力，因为它暗示着一种更聪明的系统：

- summaries 可以持续演化；
- memory classes 可以变得更丰富；
- store 可以更贴近真实 recurring tasks。

但也正是在这里，最容易跳过 operational discipline。

在团队还没有稳定建立这些能力之前：

- provenance rules；
- revision semantics；
- reviewable memory writes；
- traceable maintenance jobs；
- 针对 derived artifacts 的 rollback path，

adaptive memory shaping 更适合被当作 research direction，而不是默认的 production pattern。

从工程上讲，这意味着一件很朴素的事：evolving memory 值得研究，但当前 live system contour 仍然应该建立在 explainable retrieval、controlled compaction 和可验证 provenance 之上。

## 7. 一个 retrieval 与 background updates 的 policy 示例

下面是一个很实用的模板。它不追求万能，但很清楚地展示了哪些决定应该被写明。

```yaml
retrieval:
  max_records: 5
  max_tokens: 1800
  allowed_classes:
    - short_term
    - long_term
    - profile
  require_tenant_match: true
  min_confidence: 0.75
  deny_sources:
    - raw_external_html
    - unreviewed_summary

compaction:
  run_mode: background_only
  summary_max_tokens: 400
  deduplicate: true
  merge_similar_records: true
  drop_expired_short_term: true
```

当这些规则是显式的，团队讨论 memory 时就不再停留在感觉，而会讨论真实限制和 trade-offs。

## 8. 一个 prompt assembly 前 ranking 的简单代码示例

下面不是一个“聪明”的 retrieval engine，而是一个故意写得可读的例子。它展示了 ranking 不应该只看 similarity，还应该看 trust、freshness 和重要性。

```python
from dataclasses import dataclass


@dataclass
class RetrievedRecord:
    text: str
    similarity: float
    confidence: float
    recency_weight: float
    trusted: bool


def score(record: RetrievedRecord) -> float:
    trust_bonus = 0.15 if record.trusted else -0.2
    return (
        record.similarity * 0.5
        + record.confidence * 0.25
        + record.recency_weight * 0.1
        + trust_bonus
    )


def select_for_prompt(records: list[RetrievedRecord], limit: int = 3) -> list[RetrievedRecord]:
    ranked = sorted(records, key=score, reverse=True)
    return ranked[:limit]
```

这套逻辑很粗，但有一个重要优点：它是可以讨论、可以测试、也可以逐步替换成更精细方案的，同时不会丢掉 explainability。

## 9. Summaries 应该帮助理解，而不是隐藏数据来源

团队常常把 summaries 当作“把更多 memory 挤进更少 token”的手段。这没问题，但有一个陷阱：summary 不能变成新的匿名真相。

一个好的 summary：

- 比原始记录更短；
- 保留 provenance；
- 不混 tenants；
- 不丢掉关键限制；
- 被标记为 derived artifact，而不是 raw fact。

一个糟糕的 summary：

- 听起来很自信，但没人知道它来自哪里；
- 把冲突事实混在一起；
- 丢失日期和数据 owner；
- 被当作 trusted instruction 喂给模型。

## 10. Retrieval systems 最常坏在哪里

这些问题通常会一遍遍重复：

- duplicates 被塞进 prompt；
- retrieval 不知道 class boundaries；
- ranking 不考虑 trust；
- summaries 变得过于泛化；
- 没有 background jobs，memory 只会膨胀；
- nobody knows why this exact chunk was retrieved.

最后这一点尤其重要。如果你已经无法解释为什么某段上下文进入了 prompt，那系统基本已经失去良好控制了。

## 11. 实用检查清单

如果你想快速检查 retrieval layer，可以问：

- 有没有 records 数量上限和 token budget？
- ranking 是否不仅考虑 similarity，也考虑 confidence、recency 和 trust？
- read path 和 maintenance path 是否分开了？
- compaction 是不是一个持续的维护过程，而不是偶尔手工清理？
- summary 能不能看到 provenance？
- 有没有防止跨 tenant 或错误 class 的 retrieval？

如果连续几个问题答案都是 “no”，那说明你已经有了 memory，但还没有形成 memory discipline。

## 12. 接下来读什么

到这里，关于 memory 的基础部分已经开始成形。接下来你可以继续深入 retention 和 deletion，也可以转去看 tools 和 execution。

- [第 6 章：Short-Term、Long-Term 与 Profile Memory](chapter-6.zh.md)
- [研究前沿：记忆、可观测性与多智能体可靠性](../../appendix/research-frontier.zh.md)
- [第 8 章：Execution Model 与 Tool Catalog](../part-iv/chapter-8.zh.md)
- [第三部分：记忆与知识](index.zh.md)
- [参考资料](../../appendix/sources.zh.md)
