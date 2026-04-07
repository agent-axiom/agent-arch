# Memory Record 与 Retrieval Contract Schema

这一页把 agent systems 里的 memory 和 retrieval 所需的最小 contract layer 放在一起：memory record 长什么样、retrieval query 应该带哪些字段、以及 memory layer 至少要满足哪些约束，才能避免它变成泄漏、噪声和错误自信的来源。

如果 [trace schema 与 event catalog](trace-schema.zh.md) 回答的是“这些东西如何出现在 telemetry 里”，而 [lifecycle artifact schema](lifecycle-artifact-schema.zh.md) 回答的是“哪些东西算受治理的 operational artifact”，那么 memory-retrieval schema 回答的就是“memory layer 里到底允许存在什么样的记录和过滤规则”。

## 1. 为什么需要单独的 schema layer

memory 里最常见的失败路径通常是这样的：

- agent 记住了某些东西；
- retrieval 返回了某些东西；
- 但团队已经无法有把握地回答：
  - 这到底是什么类型的记录；
  - 它从哪里来；
  - 谁本来有权读取它；
  - 它为什么会进入 prompt。

所以，把 memory layer 描述成“我们有个 vector store”远远不够。更稳妥的做法是把它描述成 typed records 和 typed retrieval rules。

## 2. 核心实体

一个最小可用的层，通常围绕三个实体就够了：

- `memory_record`
- `retrieval_query`
- `retrieval_result`

这已经足够把 Chapters 5-7、policy layer、trace schema 和 reference runtime 串起来。

## 3. Memory record

`memory_record` 描述 memory layer 里的单条具体记录。

```yaml
kind: memory_record
record_id: mem-tenant-acme-001
tenant_id: tenant-acme
memory_class: profile
key: preferred_language
value: English
source: user_confirmed_preference
provenance: user_confirmed_preference
revision: 1
trust_level: high
created_at: 2026-04-07T12:00:00Z
retention: long_term
```

这里最关键的是：

- `tenant_id` 防止 retrieval 穿越 tenant boundary；
- `memory_class` 区分 `short_term`、`long_term` 和 `profile`；
- `source` 与 `provenance` 能帮助区分 observation 和 validated fact；
- `revision` 让历史不会被静默覆盖；
- `trust_level` 防止所有记录被一视同仁。

## 4. Retrieval query

`retrieval_query` 描述的不是一个简单文本搜索，而是完整的 memory read context。

```yaml
kind: retrieval_query
trace_id: trace-001
session_id: session-001
tenant_id: tenant-acme
principal_id: user-42
purpose: answer_generation
allowed_classes:
  - profile
  - long_term
filters:
  trust_min: medium
  max_age_days: 90
  require_provenance: true
limit: 5
```

这很重要，因为 retrieval 不应该是“神秘搜索”，而应该是正常的 gated read path。

## 5. Retrieval result

`retrieval_result` 记录 runtime 最终决定放回上下文里的内容。

```yaml
kind: retrieval_result
trace_id: trace-001
session_id: session-001
selected_records:
  - record_id: mem-tenant-acme-001
    memory_class: profile
    trust_level: high
    provenance: user_confirmed_preference
  - record_id: mem-tenant-acme-177
    memory_class: long_term
    trust_level: medium
    provenance: validated_service_rule
selection_reason:
  - profile_match
  - tenant_match
  - trust_filter_passed
excluded_records: 12
```

这样团队后面就能解释：

- 为什么偏偏是这些记录进了 prompt；
- 到底哪些限制起了作用；
- 有多少记录被过滤掉了。

## 6. 它和 policy layer 的关系

Memory read path 和 memory write path 几乎不应该共用同一套规则：

- write path 更关注 validation、provenance 和 retention；
- read path 更关注 tenant boundary、trust filters 和 class restrictions。

所以，一个好的 memory schema 几乎总是和 policy-as-code 并排存在。

## 7. 它和 trace schema 的关系

[trace schema](trace-schema.zh.md) 里已经有一些字段和事件直接支撑 memory discipline：

- `context_layers_built`
- `memory_persisted`
- `memory_class`
- `provenance`
- `revision`

这说明 memory-retrieval contract 不只是一个独立文档，它还是清晰 telemetry 的基础。

## 8. 它和 reference package 的关系

[agent_runtime_ref](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref) 已经有支撑这套模型的 operational primitives：

- [memory.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/memory.py)
- [background.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/background.py)
- [configs/memory.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/memory.yaml)
- CLI：
  - `inspect-memory`

这很有价值，因为书里不只是解释 memory contract，也给出了 runnable skeleton。

## 9. 最小不变量

一个健康的 memory-retrieval layer，至少应该保证：

- 每条记录都有 `tenant_id` 和 `memory_class`；
- persistent records 带有 `provenance` 和 `revision`；
- retrieval 总是受 class 和数量限制；
- retrieval query 明确知道“谁在读、为什么读”；
- retrieval result 能从 trace 里还原；
- summaries 不是默认真相。

## 10. 最常见的断裂点

这里的典型问题通常很容易识别：

- retrieval 返回的是“相似”，却不是“有用”；
- memory records 没有按 trust level 区分；
- summaries 静默覆盖了更可靠的事实；
- retrieval 忽略 tenant boundary；
- prompt 吞进了太多未经筛选的上下文；
- provenance 只存在于文档里，不存在于 runtime 里。

## 11. 实用检查清单

你可以快速问自己：

- 每条记录是否都有 `tenant_id`、`memory_class`、`provenance` 和 `revision`？
- memory read policy 和 memory write policy 是否真的不同？
- retrieval 是否受 trust、class 和数量限制？
- 你能解释某条记录为什么进入了 prompt 吗？
- 是否有防止跨 tenant retrieval 的保护？
- memory decisions 是否能在 trace 和 session export 里看到？

如果连续几个答案都是“否”，那说明你已经有了 memory，但还没有真正的 memory discipline。

## 延伸阅读

- [Trace Schema 与 Event Catalog](trace-schema.zh.md)
- [Eval Dataset Schema 与 Grading Contract](eval-schema.zh.md)
- [Lifecycle Artifact Schema](lifecycle-artifact-schema.zh.md)
- [Reference Package](reference-package.zh.md)
- [第 5 章：为什么智能体需要记忆，以及它为什么危险](../book/part-iii/chapter-5.zh.md)
- [第 6 章：Short-Term、Long-Term 与 Profile Memory](../book/part-iii/chapter-6.zh.md)
- [第 7 章：Retrieval、Compaction 与 Background Updates](../book/part-iii/chapter-7.zh.md)
