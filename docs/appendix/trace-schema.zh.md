# 追踪 Schema 与事件目录

这一页要解决一个很实际的问题：怎样把关于可观测性的高层讨论，落到可以真正导出、检查并复用于评测流程的事件结构上。

它同时连接本书的两部分：

- [第 11 章：追踪、跨度与结构化事件](../book/part-v/chapter-11.zh.md)
- [第 13 章：离线评测、在线评测与回归门禁](../book/part-v/chapter-13.zh.md)
- [Evidence Spine：从请求到发布判断](../book/part-v/evidence-spine.zh.md)

以及可运行的参考包：

- [参考包](reference-package.zh.md)

## 为什么需要显式的追踪模式

如果团队没有显式的追踪模式，通常会落入两种情况之一：

- 事件虽然存在，但只是一些临时拼出来的 JSON；
- 事件对调试有帮助，但很难用于分级、审计或事故复盘。

所以最好把下面三层明确分开：

- 追踪信封
- 事件目录
- 载荷契约
- 验证器契约身份
- 验证器证据链接

哪怕运行时还很小，也值得这样做。

## 最小追踪信封

`agent_runtime_ref` 目前使用的是一个有意保持精简的信封：

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

到了生产环境，通常还应该再补上：

- `session_id`
- `agent_id`
- `tenant_id`
- `principal_id`
- `event_ts`
- `span_id`
- `parent_span_id`

到了 production observability，通常还需要让 spans 可搜索、可用于 regression review 的字段：

- `span_type`
- `input_ref`
- `output_ref`
- `latency_ms`
- `retry_count`
- `token_input_count`
- `token_output_count`
- `token_cost`
- `approval_state`
- `pii_redacted`
- `redaction_policy_id`
- `retention_class`
- `trace_search_tags`
- `workspace_id`
- `workspace_persistence`
- `credential_scope`
- `egress_profile`
- `security_validation_status`
- `validation_gate_results`
- `human_review_artifact_ref`

在参考运行时里，其中一些字段暂时放在 `payload` 里，这样结构更小，也更方便阅读。同时，序列化后的事件现在会带上 `schema_version` 和 `redacted_fields`，导出路径也支持按字段做脱敏。Event loader 会显式校验这个 shape：`Telemetry path must be a string or path-like object`、`Telemetry event line is not valid JSON: {line_number}`、`Telemetry event must be a mapping`、`Telemetry event is missing required field: {required_field}`、`Telemetry event field must be a string: {field}`、`Telemetry event field must not be empty: {field}`、`Telemetry schema version is not supported: {schema_version}`、`Telemetry event payload must be a mapping`、`Telemetry event payload key must be a string`、`Telemetry event payload key must not be empty`、`Telemetry event payload keys must be unique`、`Telemetry event payload value must be a string: {payload_key}`、`Telemetry event redacted_fields must be a tuple`、`Telemetry event redacted_fields must be a list`、`Telemetry event redacted_fields entries must be strings`、`Telemetry redact field must not be empty` 和 `Telemetry redact field is not present in events: {missing}`。

## 追踪和会话的关系

对于智能体系统来说，一条追踪往往不够。你几乎总是还需要更长的上下文：

- 一个 `trace_id` 描述一次运行；
- 一个 `session_id` 把多次运行串起来；
- 会话级摘要已经可以支持评测、发布审查和复盘。

这也是为什么包里已经有：

- `inspect-trace`
- `inspect-session`
- `session-eval-summary`
- `export-session`
- `export-eval-dataset`

`dump-events`、`export-events` 和 `inspect-trace` 也会让命令响应本身可用于分诊（triage），而不只是原始 JSONL 转储（raw JSONL dump）：它们会在操作者手动扫描每个 `approval_requested` 或 `tool_execution` 载荷（payload）之前，直接暴露 `session_id`、`tenant_id`、`principal_id`、`agent_id`、`authorization_mode`、`delegated_principal_id`、`delegated_scope`、`status`、`result`、`output_preview`、`failure_reason`、`approval_ids`、`approval_capability_names`、`pending_approval_ids`、`pending_approval_capability_names`、`approval_status_counts` 和非空 `idempotency_keys`。`replay-run` 随后会分别返回 `source_idempotency_keys` 和 `replay_idempotency_keys`，明确说明重放（replay）是带有自身重复写入键（key）的新运行（new run），而不是静默复用原始写入。

追踪重放（Trace replay）会先校验这些证据（evidence），然后才允许它们作为新运行（new run）的种子（seed）：`Trace ID request must be a string`、`Trace ID not found in event file: {requested_trace_id}`、`Trace file does not contain any trace IDs`、`Trace file contains multiple trace IDs; pass --trace-id explicitly`、`Trace file does not contain a run_start event`、`Trace file contains multiple run_start events`、`Trace run_start event is missing replay fields: {missing_keys}`、`Trace run_start event has redacted replay fields: {redacted_keys}`、`Trace run_start replay field must be a string: {field}` 和 `Trace run_start replay field must not be empty: {field}`。

## 参考运行时的事件目录

下面是当前最小事件目录。

| 事件类型 | 何时出现 | 为什么重要 |
| --- | --- | --- |
| `run_start` | 运行开始时 | 记录输入与行动者身份 |
| `policy_precheck` | 运行准入后立刻出现 | 记录 policy precheck 的 action、reason 和 policy ID |
| `agent_threat_evidence` | threat-model control 留下 evidence 时 | 将 threat class 连接到 trace/evidence identifiers |
| `retrieval` | 获取 memory context 时 | 记录 source 与 retrieved records 数量 |
| `context_layers_built` | 上下文组装完成后 | 说明哪些上下文层真正进入了这次运行；internally `RunContext` 会在处理 `tool_request` 前保留 `retrieved_context` 与 `retrieved_records` |
| `tool_policy_decision` | 工具执行前 | 记录策略门禁以及允许、拒绝或需要审批的原因 |
| `mcp_tool_risk_review` | MCP tool/server risk review 期间 | 连接 threat class、registry evidence、scope review 与 quarantine state |
| `tool_execution` | capability call 或 approval handoff 后 | 记录 capability status 与 tool-principal context |
| `a2a_handoff` | 一个 agent 将工作委派给另一个 agent 时 | 记录 delegation chain、authorization 与 failure-attribution context |
| `subagent_delegation_decision` | manager 决定是否启动 subagents 时 | 记录 fanout gate、budget 与 delegation reason |
| `durable_agent_instance_state` | named agent instance 加载、休眠、唤醒或保存 durable state 时 | 记录 owner instance、state version、wakeup 与 resumable stream linkage |
| `resumable_agent_recovery` | run 在 deploy/eviction/connection churn 后继续时 | 记录 `continuation_id`、`last_durable_checkpoint`、`recovery_reason` 和 `client_tool_allowlist` |
| `approval_requested` | 高风险写入路径上 | 表示执行已经进入人工评审队列 |
| `sandbox_profile_reviewed` | 由沙箱（sandbox）支撑的路径被评审时 | 记录工作区（workspace）、权限（permissions）与快照/恢复证据复核（snapshot/resume evidence review） |
| `memory_write_decision` | 后台写入记忆前 | 记录 candidate memory write 被允许还是拒绝 |
| `memory_persisted` | 后台写入后 | 记录记忆记录的来源和修订 |
| `background_compaction` | background memory maintenance 后 | 记录 tenant-level compaction results |
| `background_update_scheduled` | background work 排队或完成后 | 记录该运行的 background update status |
| `verification_result` | 运行验证停止条件时 | 记录 stop condition、verifier actor、verification mechanism、pass/fail/warning/blocked result 与 evidence links |
| `run_failed` | 工具失败成为运行结果时 | 保留明确的 failed-run traceability |
| `governance_action` | telemetry signal 触发 policy、containment、rollout 或 registry decision 时 | 将 governance action record 连接到 trace evidence |
| `run_complete` | 运行结束时 | 闭合运行级结果 |
| `span` | 单个调用周围 | 提供基础延迟与状态遥测 |

这不是所谓“完美通用目录”。它只是一个紧凑但已经有实际价值的运行词汇表，足以支持：

在更成熟的生产词汇表里，也应该预留验证器感知证据的位置，让追踪不只解释运行时做了什么，还能解释验证器依据什么来判断过程质量、结果质量或失败归因。

- 追踪检查；
- 回归种子数据；
- 会话摘要；
- 事故复盘。

## 为什么载荷契约很重要

问题不在于事件太朴素，而在于没有契约的载荷很快就会变成垃圾。

对每一种事件类型，最好提前想清楚：

- 哪些字段是必需的；
- 哪些字段是稳定的；
- 哪些字段可以新增而不破坏下游工具；
- 哪些字段对分级重要；
- 哪些字段对审计重要。

对于 `agent_threat_evidence`，应保留统一智能体威胁证据模型（unified agent threat evidence model）中的证据标记（evidence markers），让威胁行（threat rows）能通过追踪（traces）检查，而不只停留在散文说明（prose）：

- `prompt_boundary_event`
- `rejected_instruction_trace`
- `tool_output_sanitized`
- `untrusted_content_marker`
- `policy_decision_trace`
- `retrieval_source_id`
- `freshness_score`
- `quarantine_event`
- `memory_record_id`
- `validation_state`
- `rollback_replay_evidence`
- `tool_call_id`
- `approval_record`
- `argument_validation_result`
- `subject_id`
- `delegation_trace_id`
- `caller_callee_identity_check`
- `step_budget_event`
- `stop_reason`
- `escalation_decision`
- `tenant_id`
- `egress_decision`
- `redaction_dlp_result`
- `cost_budget_event`
- `rate_limit_decision`
- `circuit_breaker_state`
- `agent_identity_mode`
- `agent_registry_record`
- `capability_loading_mode`
- `semantic_policy_decision`
- `agent_gateway_audit_event`
- `handoff_id`
- `containment_state`
- `verifier_verdict`
- `artifact_digest`
- `registry_decision`
- `sandbox_profile_id`
- `decision_trace_id`
- `immutable_log_pointer`
- `evidence_completeness_flag`

例如，`tool_policy_decision` 至少通常应该包含：

- `capability_name`
- `decision`
- `reason`
- `risk_tier`
- `tool_principal`

对于 `mcp_tool_risk_review`，生产追踪（production trace）应记录 MCP 威胁模型证据（MCP threat-model evidence），而不只是最终允许/拒绝决策（allow/deny decision）：

- `threat_class`
- `mcp_server_id`
- `capability_name`
- `tool_contract_version`
- `registry_owner`
- `scope_review`
- `quarantine_state`
- `evidence_refs`

`threat_class` 应保持在 MCP 威胁模型（MCP threat model）词汇表内：`tool poisoning`、`rug pull attack`、`tool shadowing`、`confused deputy`、`over-scoped tokens`、`data exfiltration through legitimate channels`、`supply-chain attack`、`replay/tampering`、`sandbox escape`、`local control-plane crossing`。

`local control-plane crossing` 覆盖 AutoJack 这类场景：不可信 web content 进入 browser/tool agent，利用它的本地网络位置，调用 `localhost` 上的 MCP/debug/control socket，并试图把 control-plane 参数变成 host command execution。对这类事件，trace 至少应记录：

- `untrusted_content_origin`
- `browser_tool_identity`
- `local_control_channel`
- `loopback_auth_result`
- `mcp_server_params_source`
- `executable_allowlist_result`
- `containment_action`

对于 `a2a_handoff`，载荷（payload）应保留 A2A 交接信任契约（A2A handoff trust contract），而不只是委派消息文本：

- `agent_identity`
- `delegation_chain`
- `allowed_collaboration_graph`
- `inter_agent_authorization`
- `policy_inheritance`
- `non_repudiation`
- `failure_attribution`

对于 `subagent_delegation_decision`，载荷不仅要保存 fanout 事实，还要保存这次决策的经济性：

- `subagent_count`
- `delegation_reason`
- `independence_assessment`
- `shared_context_need`
- `write_risk`
- `context_handoff_size`
- `token_budget`
- `tool_budget`
- `merge_conflict_risk`
- `fanout_decision`

!!! example "重复工单线索的 trace"
    在支持分流（support-triage）案例里，`tool_policy_decision`、`approval_requested`、`tool_execution` 和最终结果（outcome）应该由同一个 `trace_id`、`session_id`、`approval_id`、`tool_principal` 与 `idempotency_key` 连接起来。如果 `create_ticket` 超时且副作用状态未知，追踪（trace）应显示 `side_effect_unknown`，而不是把运行伪装成成功，或在没有调和（reconciliation）的情况下重复写入。

!!! note "规范追踪案例（Canonical trace cases）"
    三个规范案例（canonical cases）需要不同的追踪重点（trace emphases）。**支持分流（Support triage）** 要把审批事件（approval events）、`idempotency_key`、工具副作用（tool side effects）和重复工单恢复证据（duplicate-ticket recovery evidence）连起来。**内部知识助手（Internal knowledge assistant）** 应保留检索跨度（retrieval spans）、记忆访问（memory access）、来源归因（source attribution）、新鲜度检查（freshness checks）和访问控制决策（access control decisions）。**事件协调（Incident coordination）** 应展示升级时间线（escalation timeline）、通知副作用（notification side effects）、响应归属（response ownership）、交接事件（handoff events）和事件后学习（post-incident learning）。

对于由沙箱（sandbox）支撑的运行，也应该预留把追踪和执行边界关联起来的字段：

- `sandbox_session_id`
- `sandbox_manifest_version`
- `sandbox_permissions_profile`
- `snapshot_id`
- `workspace_manifest_ref`

如果发布（rollout）或评测（eval）要求 `sandbox_profile_review`，追踪还应该能指向复核证据（review evidence），而不只是状态字段（state fields）：

- `sandbox_profile_contract`
- `workspace_entries_reviewed`
- `permissions_profile`
- `network_secrets_posture`
- `snapshot_policy`
- `reviewed_by`
- `review_evidence_refs`

对于 **governed agent execution loop**，trace 应该把 sandbox boundary、policy-mediated tools/network、staged output 和 validation gates 连接成一条可复核路径：

- `execution_loop_id`
- `bounded_workspace_ref`
- `tool_policy_ref`
- `network_policy_decision`
- `approval_decision_id`
- `staged_output_ref`
- `validation_gate_results`
- `monitoring_signal_id`
- `constraint_bypass_attempt`

对于 **agentic enterprise control plane**，也应该记录智能体不是带有隐式权限的本地脚本，而是经过受治理的控制路径：

- `agent_identity_mode`
- `agent_registry_record`
- `agent_gateway_audit_event`
- `semantic_policy_decision`
- `capability_loading_mode`
- `cost_control_signal`

对于 **model_tool_gateway_boundary**，trace 应该说明一个 gateway/control-plane 回路如何同时连接 tool side effects、model/provider routing、cost 和 capacity：

- `provider_route_decision`
- `cost_capacity_signal`
- `capacity_backpressure_decision`
- `budget_exhausted`

对于 **networked_agent_message**，trace 应该说明来自另一个 agent 的消息为什么仍然是数据，而没有变成 authority：

- `source_agent_id`
- `principal_id`
- `message_provenance_chain`
- `peer_originated_instruction`
- `propagation_depth`
- `fanout_anomaly_score`
- `sybil_independence_check`
- `quarantine_event`

如果系统依赖验证器感知评测，也很适合单独定义一个事件或关联载荷契约来承载验证器裁决记录（verifier verdict record）：

- `verdict_id`
- `verifier_id`
- `verifier_contract_version`
- `input_refs`
- `process_score`
- `outcome_score`
- `failure_attribution`
- `blocking_decision`
- `comparison_baseline`
- `reviewer_override`
- `evidence_refs`

对于 `governance_action`，应该记录治理动作记录字段（governance action record fields），让遥测（telemetry）变成治理动作，而不只是仪表板信号（dashboard signal）：

- `governance_action_id`
- `source_signal`
- `decision_owner`
- `action_state`
- `evidence_refs`
- `review_deadline`

`source_signal` 应保持在与 governance-aware telemetry 对齐的受限词汇表内：`policy_decision_feedback`、`containment_decision`、`rollout_gate_input`、`incident_response_trigger`、`registry_update_signal`。

对于记忆投毒复核（memory poisoning review）中的 `memory_write_decision`，追踪（trace）应保留与记忆模式（memory schema）相同的记忆投毒复核字段（memory poisoning review fields）：

- `write_trust_boundary`
- `activation_policy`
- `contamination_scope`
- `policy_influence`
- `provenance_check`
- `quarantine_state`
- `rollback_ref`

而 `memory_persisted` 通常应该包含：

- `memory_class`
- `kind`
- `provenance`
- `revision`

当前参考载荷（reference payloads）也使用这些操作元数据字段（operational metadata fields）：`runtime_principal`, `authorization_mode`, `delegated_principal_id`, `delegated_scope`, `policy_id`, `static_items`, `session_items`, `retrieved_items`, `tool_items`, `approval_id`, `reviewer`, `capability_session_id`, `capability_session_status`, `tool_status`, `output_preview`, `model_output_preview`, `reasoning_summary`, `reasoning_reference`, `encrypted_reasoning_item`, `memory_id`, `revision_mode`, `compacted_records`, `persisted_records`, `tool_results`, `span_name` 和 `duration_ms`，以及 `span_type`, `input_ref`, `output_ref`, `latency_ms`, `retry_count`, `token_input_count`, `token_output_count`, `token_cost`, `approval_state`, `pii_redacted`, `redaction_policy_id`, `retention_class`, `trace_search_tags`, `subagent_count`, `delegation_reason`, `context_handoff_size`, `token_budget`, `merge_conflict_risk`, `agent_instance_id`, `durable_state_version`, `scheduled_wakeup_id` 和 `resumable_stream_id`。工具请求/结果模型校验（Tool request/result model validation）也属于同一条追踪边界（trace boundary）：畸形模型输出（malformed model outputs）会以 `Model output reasoning_summary must be a string`、`Model output reasoning_reference must be a string` 或 `Model output encrypted_reasoning_item must be a string` 失败；畸形工具调用（malformed tool calls）会以 `Tool request capability name must be a string`、`Tool request capability name must not be empty`、`Tool request arguments must be a mapping`、`Tool request argument key must be a string`、`Tool request argument key must not be empty`、`Tool request argument keys must be unique`、`Tool request argument value must be a string: {argument_key}` 失败；畸形工具结果（malformed tool results）会以 `Tool result status must be a string`、`Tool result status must not be empty`、`Tool result payload must be a mapping`、`Tool result payload key must be a string`、`Tool result payload key must not be empty`、`Tool result payload keys must be unique` 和 `Tool result payload value must be a string: {payload_key}` 失败。

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

- 每个事件的时间戳；
- 明确的 `span_id` 与 `parent_span_id`；
- 独立且稳定的 `run_id`；
- 模式版本字段；
- 展示载荷与机器载荷的分离；
- 敏感字段的脱敏规则；
- 把追踪与验证器证据、截图或打分工件显式关联起来的方式；
- 稳定记录是哪个验证器契约版本产出该打分输出的方式；
- 沙箱状态字段（sandbox state fields），用于那些会物化工作区（workspace）、使用 shell/文件系统能力（shell/filesystem capabilities），或从快照（snapshot）继续的运行（runs）；
- 用于 `sandbox_profile_reviewed` 的事件（event）或关联载荷（linked payload），确保工作区（workspace）、权限（permissions）与快照/恢复策略（snapshot/resume policy）的发布/评测证据（rollout/eval evidence）可以被追踪。
- `governed_execution_loop_step` 事件，用来展示 bounded workspace、Agent Workflow Firewall 或其他 network gate、approval decision、staged output、Safe Outputs / validation gates 和 audit/monitoring signal；
- production runtime contract 字段：`workspace_id`、`workspace_persistence`、`credential_scope`、`egress_profile`、`cost_ledger_ref`、`security_validation_status`、`validation_gate_results` 和 `human_review_artifact_ref`；

只有这样，事件流才会从调试输出变成真正的平台工件。

## 现在就该做什么

先过一遍这份短清单，把所有回答为“否”的地方单独记下来：

- 有没有稳定的事件目录？
- 是否清楚区分了 `trace_id` 和 `session_id`？
- 每种事件类型的必需字段是否明确？
- 能不能从追踪里还原出策略决策和工具路径？
- 能不能从会话导出结果构建评测数据集？
- 能不能把追踪关联到用于打分或发布评审的验证器证据？
- 如果发布（rollout）要求 `sandbox_profile_review`，是否有关于工作区条目（workspace entries）、权限（permissions）与快照/恢复策略（snapshot/resume policy）的追踪证据（trace evidence）？
- 对 agent-generated patch/PR，是否存在 governed agent execution loop 路径：bounded workspace、policy-mediated tools/network、approval gates、staged output、automated validation 和 audit/monitoring？
- Trace 是否显示 Safe Outputs、CodeQL、secret scanning、dependency risk 或其他 validation gate 已在外部写入前检查 staged output？
- Trace 是否显示使用了哪个 isolated session 和 durable workspace，哪些 scoped credentials 与 egress/tool boundaries 生效，以及哪个 `human_review_artifact_ref` 关闭这项工作？
- 当 agent 试图绕过 network allow/deny、approval gate 或 staged output boundary 时，是否有单独的 `constraint_bypass_attempt` failure mode？
- 能不能看出是哪一个验证器契约版本产出了这份打分输出？
- 有没有脱敏与模式版本化的计划？

如果连续几个答案都是“没有”，那你现在更像是拥有日志，而不是拥有真正的追踪模式。

## 下一步做什么

- [评测数据集模式与打分契约](eval-schema.zh.md)
- [策略包模式与审批契约](policy-bundle-schema.zh.md)
- [生命周期工件模式](lifecycle-artifact-schema.zh.md)
- [参考包](reference-package.zh.md)
- [第 13 章：离线评测、在线评测与回归门禁](../book/part-v/chapter-13.zh.md)
