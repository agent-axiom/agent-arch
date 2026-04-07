# Trace Schema 与 Event Catalog

这一页要解决一个很实际的问题：怎样把关于 observability 的高层讨论，落到可以真正导出、检查并复用于 eval workflows 的事件结构上。

它同时连接本书的两部分：

- [第 11 章：追踪、跨度与结构化事件](../book/part-v/chapter-11.zh.md)
- [第 13 章：离线评测、在线评测与回归门禁](../book/part-v/chapter-13.zh.md)

以及可运行的 package：

- [参考包](reference-package.zh.md)

## 为什么需要显式的 trace schema

如果团队没有显式的 trace schema，通常会落入两种情况之一：

- 事件虽然存在，但只是一些临时拼出来的 JSON；
- 事件对调试有帮助，但很难用于 grading、audit 或 incident review。

所以最好把下面三层明确分开：

- `trace envelope`
- `event catalog`
- `payload contracts`

哪怕 runtime 还很小，也值得这样做。

## 最小 trace envelope

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

## trace 和 session 的关系

对于 agent systems 来说，一条 trace 往往不够。你几乎总是还需要更长的上下文：

- 一个 `trace_id` 描述一次 run；
- 一个 `session_id` 把多个 run 串起来；
- session-level summary 已经可以支持 eval、rollout review 和 postmortem。

这也是为什么 package 里已经有：

- `inspect-trace`
- `inspect-session`
- `session-eval-summary`
- `export-session`
- `export-eval-dataset`

## Reference runtime 的 event catalog

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

这不是所谓“完美通用 catalog”。它只是一个紧凑但已经有实际价值的 operational vocabulary，足以支持：

- trace inspection；
- regression seeds；
- session summaries；
- incident review。

## 为什么 payload contract 很重要

问题不在于事件太朴素，而在于没有 contract 的 payload 很快就会变成垃圾。

对每一种 event type，最好提前想清楚：

- 哪些字段是必需的；
- 哪些字段是稳定的；
- 哪些字段可以新增而不破坏 downstream tooling；
- 哪些字段对 grading 重要；
- 哪些字段对 audit 重要。

例如，`tool_policy_decision` 至少通常应该包含：

- `capability_name`
- `decision`
- `reason`
- `risk_tier`
- `tool_principal`

而 `memory_persisted` 通常应该包含：

- `memory_class`
- `kind`
- `provenance`
- `revision`

## package 现在已经支持什么

你可以直接这样查看：

```bash
.venv/bin/python -m agent_runtime_ref dump-events
.venv/bin/python -m agent_runtime_ref export-events --output artifacts/trace-demo.jsonl
.venv/bin/python -m agent_runtime_ref export-events --output artifacts/trace-demo.jsonl --redact-field user_input
.venv/bin/python -m agent_runtime_ref inspect-trace --input artifacts/trace-demo.jsonl
.venv/bin/python -m agent_runtime_ref export-session --output artifacts/session-demo-001.json
.venv/bin/python -m agent_runtime_ref export-eval-dataset --output artifacts/eval-dataset.json
```

这很重要，因为同一套 trace vocabulary 已经同时活在三个地方：

- runtime 里；
- 书里；
- eval-ready artifacts 里。

## production schema 应该继续补什么

Reference runtime 有意保持精简，所以更成熟的系统应该很快补上：

- 每个事件的 timestamp；
- 明确的 `span_id` 与 `parent_span_id`；
- 独立且稳定的 `run_id`；
- schema version 字段；
- `display payload` 与 `machine payload` 的分离；
- 敏感字段的 redaction rules。

只有这样，event stream 才会从 debug output 变成真正的 platform artifact。

## 实用检查清单

如果你想快速判断自己的 trace schema 是否已经不只是本地调试工具，可以问自己：

- 有没有稳定的 event catalog？
- 是否清楚区分了 `trace_id` 和 `session_id`？
- 每种 event type 的必需字段是否明确？
- 能不能从 trace 里还原出 policy decision 和 tool path？
- 能不能从 session export 构建 eval dataset？
- 有没有 redaction 与 schema versioning 的计划？

如果连续几个答案都是 “没有”，那你现在更像是拥有日志，而不是拥有真正的 trace schema。

## 延伸阅读

- [Eval Dataset Schema 与 Grading Contract](eval-schema.zh.md)
- [Policy Bundle Schema 与 Approval Contract](policy-bundle-schema.zh.md)
- [参考包](reference-package.zh.md)
- [第 13 章：离线评测、在线评测与回归门禁](../book/part-v/chapter-13.zh.md)
