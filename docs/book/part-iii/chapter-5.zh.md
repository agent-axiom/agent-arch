# 第 5 章：为什么智能体需要记忆，以及为什么记忆很危险

## 1. 先看一种会活过当前请求的错误

继续沿用前几章里的同一个支持场景。

某次用户写道：

> 如果访问权限还没开通，直接创建紧急工单，不要再花时间确认。

智能体处理了这封邮件，创建了工单，还顺手把这句话保存成了用户的长期偏好。

两周后，又来了一个不同的请求：

> 访问部分可用，但有些角色消失了。请检查状态，并告诉我到底哪里出了问题。

这次更合理的做法是先检查细节，而不是立刻升级处理。但智能体从画像记忆里取出了旧记录，直接创建了紧急工单，没有做当前案例真正需要的澄清。

问题不在于一次糟糕的回答。真正的问题在于：

- 旧记录活过了原来的运行；
- 错误变成了持续性的行为；
- 团队已经很难快速说清这个决定到底从哪里来；
- 后果会在更晚、也更不同的上下文里再次冒出来。

这就是记忆带来的核心变化：它会把错误变成持久状态。

**Memory-risk case-spine note：**memory design 应该把三个 canonical cases 作为不同 durable-state risks 来闭合。Support triage 需要针对 profile preference 的 memory-write policy、saved user phrases 的 provenance、tenant isolation，以及 ticket-write behavior 复用旧上下文前的 review。Internal knowledge assistant 需要 retrieval-memory split、source grounding、freshness evidence、tenant-filter enforcement，以及 unvalidated summaries 的 quarantine。Incident coordination 需要 scoped incident memory、responder-role visibility、notification history provenance、rollback notes 和 post-incident cleanup rules。

## 2. 但没有记忆，智能体也会很快撞到天花板

与此同时，记忆又确实是需要的。

没有记忆，同一个支持智能体很快就会让用户和团队都感到烦躁：

- 已经知道的信息还是会反复追问；
- 一分钟前刚查过状态，下一步又忘了；
- 中断后的流程很难平滑续上；
- 同样的事实会被一遍遍重新拉取，运行成本也会上升。

所以真正的分叉并不是“要不要记忆”。真正的分叉是：

- 要么记忆让系统更有用、更稳；
- 要么记忆让系统更不可预测、更不安全，也更难运维。

## 3. 记忆不是一个盒子，而是几层不同的状态

当团队说“我们来加记忆”时，通常混在一起的其实是几种不同的东西：

- 短生命周期的当前运行上下文；
- 只在单个会话里有效的会话上下文；
- 带有稳定偏好的画像记忆；
- 关于用户或业务实体的已验证事实；
- 过去会话的摘要；
- 执行产物，比如工具输出或追踪笔记。

如果这些都被塞进一个地方，混乱很快就会开始。所以第一条规则很简单：不要把记忆设计成一个抽象存储。要把它设计成几种不同的边界，它们有不同的生命周期、负责人和写入规则。

<div class="diagram-card">
<p>更适合把智能体记忆理解为几层状态，而不是一个数据库</p>

``` mermaid
flowchart TD
    A["用户请求"] --> B["会话上下文"]
    B --> C["规划器 / 运行时"]
    C --> D["短期工作记忆"]
    C --> E["画像记忆"]
    C --> F["知识检索"]
    D --> G["提示组装"]
    E --> G
    F --> G
    G --> H["模型响应"]
```

</div>

## 4. 最大的错误：把记忆当成单纯的便利功能

记忆有一个麻烦的性质：它能活过单次运行。这意味着，一次写入错误的寿命，会比一次模型回答错误更长。

如果智能体曾经：

- 把错误事实存成“用户偏好”；
- 把原始用户文本片段写进画像记忆；
- 把敏感的内部备注带进摘要；
- 把不该返回给该租户的数据写进检索存储，

那问题就会变成持久化。你不一定能在单条追踪里看到它。它会在后面的别的对话、别的提示里再次出现，有时甚至会影响到别的用户。

所以，记忆写入路径必须被视为敏感的写路径，而不是方便的自动化。

## 5. 记忆也有自己的信任边界

把记忆看成信任边界，而不是中性存储，会很有帮助。

对于同一个支持智能体，至少有四种不同的数据来源：

- 可信系统注释；
- 内部服务的已验证输出；
- 用户提供内容；
- 来自外部工具、文档或邮件的内容。

这些不是同一种东西。如果你保存时不标记来源，后面的运行时就无法判断哪些内容可以作为指令级上下文，哪些只能作为参考。

一个正常规则大致是：

- 可信元数据可以参与策略决策；
- 用户内容不应该突然变成系统指令；
- 检索文本在被证明之前都应该视为不可信；
- 摘要同样有来源，不是“默认真相”。

## 6. 最危险的一条路：在热路径里直接写入长期记忆

团队很容易这么做：模型一答完，运行时立刻 `save_memory()`，然后把这当作一种方便的自动化。短期看起来很顺手，长期几乎总会出问题。

为什么这对同一个支持智能体尤其危险：

- 用户一句随口的话就可能变成“长期偏好”；
- 一段工具输出可能在没经过校验的情况下进入画像记忆；
- 邮件里的敏感片段可能活过原始请求；
- 一次糟糕的写入会影响后面几十次回答。

为什么这条路径在系统层面危险：

- 写入发生在延迟压力下；
- 没人验证什么才值得写入记忆；
- 没有规范化和清理步骤；
- 没有独立的租户隔离策略；
- 很难解释某个事实为什么会进入记忆。

所以即使是很强的智能体，也最好遵循一个很朴素的原则：默认情况下，写入长期记忆要么被策略明确允许，要么被移到后台流水线。

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

## 7. 一个好的记忆系统写得比你想象中更少

一开始，几乎每个人都会觉得记忆应该越多越好。但在实践里，一个好的记忆系统通常赢在筛选严格，而不是数量巨大。

通常值得写入的东西应该满足：

- 对未来的运行有用；
- 有明确的负责人和租户；
- 能向人解释清楚；
- 不携带多余敏感数据；
- 不会把提示变成垃圾堆。

每次写入前一个很有用的问题是：

> 如果这段内容三周后在别的上下文里再次出现，我能舒服地解释清楚它为什么在这里吗？

如果这个答案都不太稳，那大概率就不该写。

## 8. 一个最小可用的记忆写入策略

如果你想从不过度复杂的方式开始，可以把记忆写入策略想成这样：

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

### 8.1. 最好把记忆读取策略和记忆写入策略分开

Google 最近材料里一个很实用的提醒是：记忆应该被当成可治理的子系统，而不只是“装上下文的存储”。[^google-agent-overview][^google-govern]

它带来的直接结论是：**读规则和写规则几乎不应该完全一样**。

比如：

- 写入长期记忆可能要求校验、来源和后台审查；
- 读取长期记忆可能只允许通过检索过滤器；
- 写入画像记忆可能要求明确信号或高置信度；
- 读取画像记忆可能只允许个性化层使用，而不该直接给策略引擎。

如果不把这些路径拆开，系统很快就会活在一种危险逻辑里：任何东西只要曾经被写进去，后面几乎就能在任何地方读出来。

这已经不是记忆设计，而是安静制造事故的方式。

### 8.2. 持久记忆默认就应该带来源

对于任何能活过一个运行的记录，最好默认至少保留：

- `source_type`；
- `source_id`；
- `writer_identity`；
- `tenant_id`；
- `written_at`；
- `confidence` 或 `validation_state`。

这些字段看起来像额外负担，但一旦智能体在别的上下文里自信地重复了某个“事实”，团队马上就会想知道它到底从哪里来的。

### 8.3. Memory poisoning 是安全场景，不只是数据质量问题

最危险的记忆失败往往看起来不像工具漏洞，而像是一个有害或错误的事实被安静写入了可信层。比如，用户原话、未经验证的 retrieval 结果，或某次事故 summary 进入长期记忆，开始看起来像稳定知识，并在几次运行之后影响决策。

最小 memory poisoning 场景应该检查：

- `untrusted write`：未经验证的来源是否能进入 persistent memory；
- `delayed activation`：这条记录是否会在之后的 run 或另一个 session 中才影响行为；
- `cross-tenant contamination`：记录是否可能跨越 tenant boundary 或访问角色；
- `policy influence`：未经验证的记忆是否会用于 policy decision、approval 或 tool selection；
- `provenance check`：operator 是否能看到 source、writer identity、validation state 和写入时间；
- `quarantine and rollback`：是否能禁用这条记录、重放 affected traces，并解释哪些回答被它改变。

实用规则很简单：任何能活过当前运行的记忆，不只需要 data-quality review，也需要 threat-model review。否则系统就会得到一条长期攻击通道，而它表面上看起来只是普通个性化。

## 9. 记忆设计的实用规则

如果要把最早期的设计决策压缩成一组规则，通常就是这样：

1. 先把会话上下文和持久记忆分开，再去争论更复杂的记忆功能。
2. 宁可少写，也要写得清楚：已验证事实通常比原始文本更有价值。
3. 写规则应该比读规则更严格。
4. 每一条能长期存在的记录，都应该带上来源、租户元数据和写入者身份。
5. 只要一条写入可能活过当前运行，默认就更适合放进后台路径。

## 10. 团队最常做错什么

最常见的错误会一再出现：

- 把原始用户表述直接保存成稳定偏好；
- 把画像记忆、检索存储和执行产物混在一起；
- 让摘要在没有来源和校验状态的情况下长期存在；
- 在策略决策里使用未经验证的记忆；
- 很久都不设计删除、复核和记录退役路径。

## 11. 生产团队必须能快速回答什么

对于同一个支持场景，在出现奇怪的记忆驱动行为之后，团队应该能很快回答：

- 到底是哪条记录进入了画像记忆；
- 它来自哪里；
- 是谁写进去的；
- 它是否通过了校验；
- 为什么它被允许写给这个租户；
- 它已经影响了后续哪些运行。

如果这些问题回答不了，记忆子系统就已经成了系统性风险。

## 12. 读完这一章后先做什么

如果你刚开始做记忆设计，可以先按这个短顺序来：

1. 先把会话上下文和持久记忆分开。
2. 再定义哪些记录类型是允许存在的。
3. 然后补上来源和租户元数据。
4. 最后才去自动化写路径。

如果顺序反过来，记忆很快就会变成平台把所有没设计清楚的东西都丢进去的地方。

## 13. 接下来读什么

这一部分后面的章节会继续拆解：

- 短期记忆和长期记忆到底差在哪；
- 为什么画像记忆应该和检索存储分开；
- 为什么摘要更适合放到后台更新；
- 压缩如何帮你保持上下文干净。

对这个支持场景来说，下一步就是把工作上下文、用户档案和持久记忆拆开，这样后面的执行层才不会建立在脏状态之上。

目前最重要的要点很简单：只有当记忆被设计成一个受控的系统层，而不是无节制堆文本的地方时，它才真正有用。

- [第三部分：记忆与知识](index.zh.md)
- [第 6 章：短期记忆、长期记忆与用户画像记忆](chapter-6.zh.md)
- [第 4 章：工具网关、审批与审计轨迹](../part-ii/chapter-4.zh.md)
- [参考资料](../../appendix/sources.zh.md)

[^google-agent-overview]: [Google Cloud, Vertex AI Agent Builder overview](https://docs.cloud.google.com/agent-builder/overview)
[^google-govern]: [Google Cloud, More ways to build, scale, and govern AI agents with Vertex AI Agent Builder](https://cloud.google.com/blog/products/ai-machine-learning/more-ways-to-build-and-scale-ai-agents-with-vertex-ai-agent-builder)
