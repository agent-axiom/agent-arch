# 记忆记录与检索契约 Schema

这一页把智能体系统里记忆与检索所需的最小契约层放在一起：记忆记录长什么样、检索请求应该带哪些字段，以及记忆层至少要满足哪些约束，才能避免它变成泄漏、噪声和错误自信的来源。

如果 [追踪 Schema 与事件目录](trace-schema.zh.md) 回答的是“这些东西如何出现在遥测里”，而 [生命周期工件 Schema](lifecycle-artifact-schema.zh.md) 回答的是“哪些东西算受治理的运行工件”，那么记忆与检索 Schema 回答的就是“记忆层里到底允许存在什么样的记录和过滤规则”。

## 1. 为什么需要单独的模式层

记忆里最常见的失败路径通常是这样的：

- 智能体记住了某些东西；
- 检索返回了某些东西；
- 但团队已经无法有把握地回答：
  - 这到底是什么类型的记录；
  - 它从哪里来；
  - 谁本来有权读取它；
- 它为什么会进入提示。

所以，把记忆层描述成“我们有个向量存储”远远不够。更稳妥的做法是把它描述成类型化记录和类型化检索规则。

## 2. 核心实体

一个最小可用的层，通常围绕三个实体就够了：

- `memory_record`
- `retrieval_query`
- `retrieval_result`

这已经足够把第 5-7 章、策略层、追踪 Schema 和参考运行时串起来。

## 3. 记忆记录

`memory_record` 描述记忆层里的单条具体记录。

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

- `tenant_id` 防止检索跨越租户边界；
- `memory_class` 区分 `short_term`、`long_term` 和 `profile`；
- `source` 与 `provenance` 能帮助区分观察结果和已验证事实；
- `revision` 让历史不会被静默覆盖；
- `trust_level` 防止所有记录被一视同仁。

## 4. 检索查询

`retrieval_query` 描述的不是一个简单文本搜索，而是完整的记忆读取上下文。

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

这很重要，因为检索不应该是“神秘搜索”，而应该是正常的受控读取路径。

## 5. 检索结果

`retrieval_result` 记录运行时最终决定放回上下文里的内容。

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

- 为什么偏偏是这些记录进了提示；
- 到底哪些限制起了作用；
- 有多少记录被过滤掉了。

## 6. 它和策略层的关系

记忆读取路径和记忆写入路径几乎不应该共用同一套规则：

- 写入路径更关注校验、来源证明和保留规则；
- 读取路径更关注租户边界、信任过滤器和类别限制。

所以，一个好的记忆模式几乎总是和策略即代码并排存在。

## 7. 它和追踪 Schema 的关系

[追踪 Schema](trace-schema.zh.md) 里已经有一些字段和事件直接支撑记忆纪律：

- `context_layers_built`
- `memory_persisted`
- `memory_class`
- `provenance`
- `revision`

这说明记忆与检索契约不只是一个独立文档，它还是清晰遥测的基础。

## 8. 它和参考包的关系

[agent_runtime_ref](https://github.com/agent-axiom/agent-arch/tree/main/agent_runtime_ref) 已经有支撑这套模型的运行原语：

- [memory.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/memory.py)
- [background.py](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/background.py)
- [configs/memory.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/memory.yaml)
- CLI：
  - `inspect-memory`

内置的 `memory.yaml` 通过 `seed_records` 把这件事具体化：每条 seed record 都带有稳定的 `memory_id`，以及 `tenant_id`、`memory_class`、`kind`、`content`、`source`、`confidence`、`provenance` 和 `revision`，因此 demo 可以同时展示 retrieval filtering 与记录 lineage。Reference seeds（`mem-001`、`mem-002` 和 `mem-003`）有意覆盖 `trusted_profile`、`trusted_service` 与 `session_state` sources，并包含 `ephemeral_session_note` 这样的 provenance，让 retrieval examples 能呈现不同的 trust 与 persistence levels。

这很有价值，因为书里不只是解释记忆契约，也给出了可运行的骨架。

## 9. 最小不变量

一个健康的记忆与检索层，至少应该保证：

- 每条记录都有 `tenant_id` 和 `memory_class`；
- 持久记录带有 `provenance` 和 `revision`；
- 检索总是受类别和数量限制；
- 检索请求明确知道“谁在读、为什么读”；
- 检索结果能从追踪里还原；
- 摘要不是默认真相。

## 10. 最常见的断裂点

这里的典型问题通常很容易识别：

- 检索返回的是“相似”，却不是“有用”；
- 记忆记录没有按信任等级区分；
- 摘要静默覆盖了更可靠的事实；
- 检索忽略租户边界；
- 提示吞进了太多未经筛选的上下文；
- 来源证明只存在于文档里，不存在于运行时里。

## 11. 现在就该做什么

先过一遍这份短清单，把所有回答为“否”的地方单独记下来：

- 每条记录是否都有 `tenant_id`、`memory_class`、`provenance` 和 `revision`？
- 记忆读取策略和记忆写入策略是否真的不同？
- 检索是否受信任等级、类别和数量限制？
- 你能解释某条记录为什么进入了提示吗？
- 是否有防止跨租户检索的保护？
- 记忆决策是否能在追踪和会话导出里看到？

如果连续几个答案都是“否”，那说明你已经有了记忆，但还没有真正的记忆纪律。

## 下一步做什么

- [追踪 Schema 与事件目录](trace-schema.zh.md)
- [评测数据集 Schema 与打分契约](eval-schema.zh.md)
- [生命周期工件 Schema](lifecycle-artifact-schema.zh.md)
- [参考包](reference-package.zh.md)
- [第 5 章：为什么智能体需要记忆，以及为什么记忆很危险](../book/part-iii/chapter-5.zh.md)
- [第 6 章：短期记忆、长期记忆与用户画像记忆](../book/part-iii/chapter-6.zh.md)
- [第 7 章：检索、压缩与后台更新](../book/part-iii/chapter-7.zh.md)
