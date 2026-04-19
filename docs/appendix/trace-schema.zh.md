# 追踪模式与事件目录

这一页要解决一个很实际的问题：怎样把关于可观测性的高层讨论，落到可以真正导出、检查并复用于评测流程的事件结构上。

它同时连接本书的两部分：

- [第 11 章：追踪、跨度与结构化事件](../book/part-v/chapter-11.zh.md)
- [第 13 章：离线评测、在线评测与回归门禁](../book/part-v/chapter-13.zh.md)
- [Evidence Spine：从请求到 rollout judgment](../book/part-v/evidence-spine.zh.md)

以及可运行的参考包：

- [参考包](reference-package.zh.md)

## 为什么需要显式的追踪模式

如果团队没有显式的追踪模式，通常会落入两种情况之一：

- 事件虽然存在，但只是一些临时拼出来的 JSON；
- 事件对调试有帮助，但很难用于分级、审计或事故复盘。

所以最好把下面三层明确分开：

- `trace envelope`
- `event catalog`
- `payload contracts`
- `verifier contract identity`
- `verifier evidence linkage`

哪怕 runtime 还很小，也值得这样做。

## 最小追踪信封

`agent_runtime_ref` 目前使用的是一个有意保持精简的 envelope：

```json
{
  "event_type": "run_start",
  "trace_id": "trace-demo-001",
  "payload": {
    "agent_id": "support-triage-ref",
    "tenant_id": "tenant-acme",
    "principal_id": "user-42",
    "session_id": "session-demo-001",
    "user_input": "Please create a ticket for this onboarding issue."
  }
}
```

最小可用字段集是：

- `event_type`
- `trace_id`
- `payload`

到了 production，通常还应该再补上：

- `session_id`
- `agent_id`
- `tenant_id`
- `principal_id`
- `event_ts`
- `span_id`
- `parent_span_id`

在 reference runtime 里，其中一些字段暂时放在 `payload` 里，这样结构更小，也更方便阅读。同时，序列化后的事件现在会带上 `schema_version`，导出路径也支持按字段做 redaction。

## 追踪和会话的关系

对于智能体系统来说，一条追踪往往不够。你几乎总是还需要更长的上下文：

- 一个 `trace_id` 描述一次运行；
- 一个 `session_id` 把多个 run 串起来；
- 会话级摘要已经可以支持评测、发布审查和复盘。

这也是为什么 package 里已经有：

- `inspect-trace`
- `inspect-session`
- `session-eval-summary`
- `export-session`
- `export-eval-dataset`

## 参考运行时的事件目录

下面是当前最小 event catalog。

| Event type | 何时出现 | 为什么重要 |
| --- | --- | --- |
| `run_start` | run 开始时 | 记录输入与 actor identity |
| `context_layers_built` | context 组装完成后 | 说明哪些 context layers 真正进入了这次 run |
| `tool_policy_decision` | tool execution 前 | 记录 policy gate 以及 allow/deny/approval 的原因 |
| `approval_requested` | high-risk write path 上 | 表示执行已经进入 human review queue |
| `memory_persisted` | background write 后 | 记录 memory record 的 provenance 和 revision |
| `run_complete` | run 结束时 | 闭合 run-level outcome |
| `span` | 单个调用周围 | 提供基础 latency 与 status telemetry |

这不是所谓“完美通用目录”。它只是一个紧凑但已经有实际价值的运行词汇表，足以支持：

在更成熟的 production vocabulary 里，也应该预留 verifier-aware evidence 的位置，让 traces 不只解释 runtime 做了什么，还能解释 verifier 依据什么来判断 process quality、outcome quality 或 failure attribution。

- 追踪检查；
- 回归种子数据；
- 会话摘要；
- 事故复盘。

## 为什么载荷契约很重要

问题不在于事件太朴素，而在于没有契约的载荷很快就会变成垃圾。

对每一种 event type，最好提前想清楚：

- 哪些字段是必需的；
- 哪些字段是稳定的；
- 哪些字段可以新增而不破坏下游工具；
- 哪些字段对分级重要；
- 哪些字段对审计重要。

例如，`tool_policy_decision` 至少通常应该包含：

- `capability_name`
- `decision`
- `reason`
- `risk_tier`
- `tool_principal`

而 `memory_persisted` 通常应该包含：

如果系统依赖 verifier-aware evals，也很适合单独定义一个 event 或 linked payload contract 来承载 verifier evidence，例如：

- `verifier_id`
- `verifier_contract_version`
- `process_score`
- `outcome_score`
- `failure_attribution`
- `evidence_refs`

而 `memory_persisted` 通常应该包含：

- `memory_class`
- `kind`
- `provenance`
- `revision`

## 参考包现在已经支持什么

你可以直接这样查看：

```bash
.venv/bin/python -m agent_runtime_ref dump-events
.venv/bin/python -m agent_runtime_ref export-events --output artifacts/trace-demo.jsonl
.venv/bin/python -m agent_runtime_ref export-events --output artifacts/trace-demo.jsonl --redact-field user_input
.venv/bin/python -m agent_runtime_ref inspect-trace --input artifacts/trace-demo.jsonl
.venv/bin/python -m agent_runtime_ref export-session --output artifacts/session-demo-001.json
.venv/bin/python -m agent_runtime_ref export-eval-dataset --output artifacts/eval-dataset.json
```

这很重要，因为同一套追踪词汇已经同时活在三个地方：

- 运行时里；
- 书里；
- 评测工件里。

## 生产级模式还应该补什么

参考运行时有意保持精简，所以更成熟的系统应该很快补上：

- 每个事件的 timestamp；
- 明确的 `span_id` 与 `parent_span_id`；
- 独立且稳定的 `run_id`；
- schema version 字段；
- `display payload` 与 `machine payload` 的分离；
- 敏感字段的脱敏规则；
- 把 traces 与 verifier evidence、screenshots 或 grading artifacts 显式关联起来的方式；
- 稳定记录是哪个 verifier contract version 产出该 grading output 的方式。

只有这样，事件流才会从调试输出变成真正的平台工件。

## 现在就该做什么

先过一遍这份短清单，把所有回答为 “no” 的地方单独记下来：

- 有没有稳定的事件目录？
- 是否清楚区分了 `trace_id` 和 `session_id`？
- 每种 event type 的必需字段是否明确？
- 能不能从追踪里还原出策略决策和工具路径？
- 能不能从会话导出结果构建评测数据集？
- 能不能把 trace 关联到用于 grading 或 rollout review 的 verifier evidence？
- 能不能看出是哪一个 verifier contract version 产出了这份 grading output？
- 有没有脱敏与模式版本化的计划？

如果连续几个答案都是“没有”，那你现在更像是拥有日志，而不是拥有真正的追踪模式。

## 下一步做什么

- [Eval Dataset Schema 与 Grading Contract](eval-schema.zh.md)
- [Policy Bundle Schema 与 Approval Contract](policy-bundle-schema.zh.md)
- [Lifecycle Artifact Schema](lifecycle-artifact-schema.zh.md)
- [参考包](reference-package.zh.md)
- [第 13 章：离线评测、在线评测与回归门禁](../book/part-v/chapter-13.zh.md)
