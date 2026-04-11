# 第 5 章：为什么智能体需要记忆，以及为什么记忆很危险

## 1. 先看一种会活过当前请求的错误

继续沿用前几章里的同一个支持场景。

某次用户写道：

> 如果访问权限还没开通，直接创建紧急工单，不要再花时间确认。

智能体处理了这封邮件，创建了工单，还顺手把这句话保存成了用户的长期偏好。

两周后，又来了一个不同的请求：

> 访问部分可用，但有些角色消失了。请检查状态，并告诉我到底哪里出了问题。

这次更合理的做法是先检查细节，而不是立刻升级处理。但智能体从 profile memory 里取出了旧记录，直接创建了紧急工单，没有做当前案例真正需要的澄清。

问题不在于一次糟糕的回答。真正的问题在于：

- 旧记录活过了原来的 run；
- 错误变成了持续性的行为；
- 团队已经很难快速说清这个决定到底从哪里来；
- 后果会在更晚、也更不同的上下文里再次冒出来。

这就是记忆带来的核心变化：它会把错误变成持久状态。

## 2. 但没有记忆，智能体也会很快撞到天花板

与此同时，记忆又确实是需要的。

没有记忆，同一个支持智能体很快就会让用户和团队都感到烦躁：

- 已经知道的信息还是会反复追问；
- 一分钟前刚查过状态，下一步又忘了；
- 中断后的流程很难平滑续上；
- 同样的事实会被一遍遍重新拉取，run 成本也会上升。

所以真正的分叉并不是“要不要 memory”。真正的分叉是：

- 要么记忆让系统更有用、更稳；
- 要么记忆让系统更不可预测、更不安全，也更难运维。

## 3. 记忆不是一个盒子，而是几层不同的状态

当团队说“我们来加 memory”时，通常混在一起的其实是几种不同的东西：

- 短生命周期的当前 run context；
- 只在单个会话里有效的 session context；
- 带有稳定偏好的 profile memory；
- 关于用户或业务实体的 validated facts；
- 过去会话的 summaries；
- execution artifacts，比如 tool outputs 或 trace notes。

如果这些都被塞进一个地方，混乱很快就会开始。所以第一条规则很简单：不要把 memory 设计成一个抽象 storage。要把它设计成几种不同的边界，它们有不同的生命周期、owner 和写入规则。

<div class="diagram-card">
<p>更适合把智能体记忆理解为几层状态，而不是一个数据库</p>

``` mermaid
flowchart TD
    A["用户请求"] --> B["会话上下文"]
    B --> C["规划器 / 运行时"]
    C --> D["短期工作记忆"]
    C --> E["画像记忆"]
    C --> F["知识检索"]
    D --> G["Prompt 组装"]
    E --> G
    F --> G
    G --> H["模型响应"]
```

</div>

## 4. 最大的错误：把记忆当成单纯的便利功能

记忆有一个麻烦的性质：它能活过单次 run。这意味着，一次写入错误的寿命，会比一次模型回答错误更长。

如果智能体曾经：

- 把错误事实存成“用户偏好”；
- 把原始用户文本片段写进 profile memory；
- 把敏感的内部备注带进 summary；
- 把不该返回给该 tenant 的数据写进 retrieval store，

那问题就会变成 persistent。你不一定能在单条 trace 里看到它。它会在后面的别的对话、别的 prompt 里再次出现，有时甚至会影响到别的用户。

所以，memory write path 必须被视为敏感的 write path，而不是方便的自动化。

## 5. 记忆也有自己的信任边界

把 memory 看成 trust boundary，而不是中性存储，会很有帮助。

对于同一个支持智能体，至少有四种不同的数据来源：

- trusted system annotations；
- internal services 的 validated outputs；
- user-provided content；
- 来自外部工具、文档或邮件的内容。

这些不是同一种东西。如果你保存时不标记来源，后面的 runtime 就无法判断哪些内容可以作为 instruction-grade context，哪些只能作为 reference。

一个正常规则大致是：

- trusted metadata 可以参与 policy decisions；
- user content 不应该突然变成 system instruction；
- retrieved text 在被证明之前都应该视为 untrusted；
- summaries 同样有 provenance，不是“默认真相”。

## 6. 最危险的一条路：在 hot path 里直接写入长期记忆

团队很容易这么做：模型一答完，runtime 立刻 `save_memory()`，然后把这当作一种方便的自动化。短期看起来很顺手，长期几乎总会出问题。

为什么这对同一个支持智能体尤其危险：

- 用户一句随口的话就可能变成“长期偏好”；
- 一段 tool output 可能在没经过 validation 的情况下进入 profile memory；
- 邮件里的敏感片段可能活过原始请求；
- 一次糟糕的写入会影响后面几十次回答。

为什么这条路径在系统层面危险：

- 写入发生在 latency 压力下；
- 没人验证什么才算 memory-worthy；
- 没有规范化和清理步骤；
- 没有独立的 tenant isolation policy；
- 很难解释某个事实为什么会进入 memory。

所以即使是很强的智能体，也最好遵循一个很朴素的原则：默认情况下，写入 long-term memory 要么被 policy 明确允许，要么被移到 background pipeline。

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

这段代码故意写得很简单。它的价值不在“聪明”，而在于规则是可见、可审计的。

## 7. 一个好的 memory system 写得比你想象中更少

一开始，几乎每个人都会觉得 memory 应该越多越好。但在实践里，一个好的 memory system 通常赢在筛选严格，而不是数量巨大。

通常值得写入的东西应该满足：

- 对未来的 runs 有用；
- 有明确的 owner 和 tenant；
- 能向人解释清楚；
- 不携带多余敏感数据；
- 不会把 prompt 变成垃圾堆。

每次写入前一个很有用的问题是：

> 如果这段内容三周后在别的上下文里再次出现，我能舒服地解释清楚它为什么在这里吗？

如果这个答案都不太稳，那大概率就不该写。

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

这不是魔法，而是让写入路径变得可见、可控、可讨论。

### 8.1. 最好把 memory read policy 和 memory write policy 分开

Google 最近材料里一个很实用的提醒是：memory 应该被当成可治理的 subsystem，而不只是“装上下文的 storage”。[^google-agent-overview][^google-govern]

它带来的直接结论是：**读规则和写规则几乎不应该完全一样**。

比如：

- 写入 long-term memory 可能要求 validation、provenance 和 background review；
- 读取 long-term memory 可能只允许通过 retrieval filters；
- 写入 profile memory 可能要求 explicit signal 或 high confidence；
- 读取 profile memory 可能只允许 personalization layer 使用，而不该直接给 policy engine。

如果不把这些路径拆开，系统很快就会活在一种危险逻辑里：任何东西只要曾经被写进去，后面几乎就能在任何地方读出来。

这已经不是 memory design，而是安静制造 incident 的方式。

### 8.2. Persistent memory 默认就应该带 provenance

对于任何能活过一个 run 的记录，最好默认至少保留：

- `source_type`；
- `source_id`；
- `writer_identity`；
- `tenant_id`；
- `written_at`；
- `confidence` 或 `validation_state`。

这些字段看起来像额外负担，但一旦智能体在别的上下文里自信地重复了某个“事实”，团队马上就会想知道它到底从哪里来的。

## 9. memory design 的实用规则

如果要把最早期的设计决策压缩成一组规则，通常就是这样：

1. 先把 session context 和 persistent memory 分开，再去争论更复杂的 memory features。
2. 宁可少写，也要写得清楚：validated facts 通常比原始文本更有价值。
3. 写规则应该比读规则更严格。
4. 每一条能长期存在的记录，都应该带上 provenance、tenant metadata 和 writer identity。
5. 只要一条写入可能活过当前 run，默认就更适合放进 background path。

## 10. 团队最常做错什么

最常见的错误会一再出现：

- 把原始用户表述直接保存成稳定偏好；
- 把 profile memory、retrieval store 和 execution artifacts 混在一起；
- 让 summaries 在没有 provenance 和 validation state 的情况下长期存在；
- 在 policy decisions 里使用未经验证的记忆；
- 很久都不设计删除、复核和记录退役路径。

## 11. 生产团队必须能快速回答什么

对于同一个支持场景，在出现奇怪的 memory-driven behavior 之后，团队应该能很快回答：

- 到底是哪条记录进入了 profile memory；
- 它来自哪里；
- 是谁写进去的；
- 它是否通过了 validation；
- 为什么它被允许写给这个 tenant；
- 它已经影响了后续哪些 runs。

如果这些问题回答不了，memory subsystem 就已经成了系统性风险。

## 12. 读完这一章后先做什么

如果你刚开始做 memory design，可以先按这个短顺序来：

1. 先把 session context 和 persistent memory 分开。
2. 再定义哪些 record types 是允许存在的。
3. 然后补上 provenance 和 tenant metadata。
4. 最后才去自动化 write path。

如果顺序反过来，memory 很快就会变成平台把所有没设计清楚的东西都丢进去的地方。

## 13. 接下来读什么

这一部分后面的章节会继续拆解：

- short-term memory 和 long-term memory 到底差在哪；
- 为什么 profile memory 应该和 retrieval store 分开；
- 为什么 summaries 更适合放到 background 更新；
- compaction 如何帮你保持上下文干净。

对这个支持场景来说，下一步就是把工作上下文、用户档案和持久记忆拆开，这样后面的执行层才不会建立在脏状态之上。

目前最重要的 takeaway 很简单：只有当 memory 被设计成一个受控的系统层，而不是无节制堆文本的地方时，它才真正有用。

- [第三部分：记忆与知识](index.zh.md)
- [第 6 章：Short-Term、Long-Term 与 Profile Memory](chapter-6.zh.md)
- [第 4 章：Tool Gateway、Approval 与 Audit Trail](../part-ii/chapter-4.zh.md)
- [参考资料](../../appendix/sources.zh.md)

[^google-agent-overview]: [Google Cloud, Vertex AI Agent Builder overview](https://docs.cloud.google.com/agent-builder/overview)
[^google-govern]: [Google Cloud, More ways to build, scale, and govern AI agents with Vertex AI Agent Builder](https://cloud.google.com/blog/products/ai-machine-learning/more-ways-to-build-and-scale-ai-agents-with-vertex-ai-agent-builder)
