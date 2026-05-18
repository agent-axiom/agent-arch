# 第 26 章：AI 原生可观测性、清单覆盖率与可用于检测的遥测

!!! info "时效说明"
    最近一次编辑审查：**2026 年 5 月 14 日**。下一次计划审查：**2026 年 6 月 14 日**。

    自上次审查以来的变化：MCP/A2A 安全面、验证器契约、治理感知遥测以及出版就绪问题，已经被明确列为近期编辑任务。

    变化最快的部分：

    - 面向智能体系统的遥测产品与厂商追踪能力；
    - 面向漂移、滥用和异常工具行为的检测启发式；
    - 面向诊断的追踪以及跨系统关联的新兴约定。

    变化相对较慢的部分：

    - 必须建设可直接用于证据链的遥测，而不只是调试日志；
    - 可观测性必须和 approvals、runtime-control states、policy decisions、tool principals、contract versions 与 artifact bundles 关联；
    - 完整的清单覆盖率仍然是检测和事故评审的前提。

## 1. 为什么智能体的可观测性不能只看延迟和错误率

在普通服务里，可观测性往往先看一组很熟悉的东西：

- 延迟；
- 错误率；
- 吞吐量；
- 资源利用率。

但对智能体系统来说，这远远不够。

这里要始终保持一个简单区分：保障负责决定什么时候需要遏制、由谁来响应；可观测性则通过保留可被信任的证据，让这些 release、incident 与 governance decision 真正有据可依。

系统可能：

- 没有宕机；
- 响应很快；
- 一直返回 HTTP 200；
- 但行为依然危险、低质或者失控。

Microsoft 对这个转变的表述很准确：对智能体系统来说，我们需要把传统的日志、指标和追踪演进成 `AI-native signals`，让系统不仅能说明“发生了请求”，还能说明“系统究竟是怎么行为的”。[^ms-observability]

## 2. 可观测性不只是为了调试

在智能体平台里，可观测性至少承担五种角色：

- 运行时调试；
- 事故重建；
- 滥用检测；
- 发布证据；
- 治理覆盖率。

如果 traces 只是给开发者排查本地 bug 用的，这已经不够了。

在生产环境里，你还需要回答：

- 一共存在多少 agents；
- 其中多少是真正可观测的；
- 它们实际调用了哪些 capabilities；
- 高风险动作出现在哪里；
- 哪些 approvals 被请求、批准或绕过；
- rollout 之后出现了哪些行为变化。

## 3. 什么是 AI-native signals

对智能体系统来说，一个有用的遥测契约通常包括：

- request identity；
- `run_id`、`trace_id`、`session_id`；
- actor 与 agent identity；
- retrieval provenance；
- tool invocations；
- tool permissions 与 principals；
- policy decisions；
- approvals；
- paused runs 的状态与等待时长；
- approval backlog signals；
- capability sessions 的状态、expiry reason 与 re-init status；
- orchestration-pattern selection 与 delegated worker lineage；
- background runs 的状态与运行时长；
- output summaries；
- redaction status；
- verifier outputs，例如 `process_score`、`outcome_score` 与 `failure_attribution`；
- active verifier contract 与 verifier contract version；
- bundle、version、rollout wave 与 contract version。

为了避免这份清单变成一堆没有结构的字段，可以把它看成五组 signals：

1. **Identity and scope：** 谁在行动、代表谁行动、处在哪个 tenant/request scope 中。
2. **Control evidence：** 哪些 policy decisions、approvals、quotas 和 capability sessions 约束了这次 run。
3. **Execution state：** 选择了哪种 orchestration pattern，run 在哪里 paused/backgrounded/delegated，又如何 resumed。
4. **Quality evidence：** 哪些 verifier outputs、eval verdicts 和 failure attribution 连接到了 outcome。
5. **Release and artifact context：** 哪个 bundle、contract version 与 rollout wave 支撑了这次 run。

也就是说，traces 不该只告诉你“哪里坏了”，还应该告诉你：

- 是谁在行动；
- 穿过了哪一层控制层；
- 拥有哪些权限；
- 依据哪套规则；
- 属于哪个 artifact bundle；
- 最终造成了什么副作用。

这也正是为什么 runtime-control signals 不能继续被当成隐藏的实现细节。只要系统里存在 pause/resume paths、background execution 和 contract-version transitions，它们就已经属于证据层。

但这并不意味着可观测性成了 工件谱系 的拥有者。可观测性负责在跨 runs 的范围内保留和关联证据；而 来源证明层 仍然回答，后续决策依赖的是哪一个 受治理工件、已批准版本或发布身份。

这也正是本章的核心承诺。它要帮助读者把可观测性看成整个生命周期的证据基底：这一层把运行时行为、控制信号、approvals 与跨系统活动保留得足够可见，使 assurance、rollout、judgment 与 registry functions 都能建立在同一份运行记录之上。本章的主要工件是 trace and telemetry coverage record：一张说明哪些 agents、capabilities、control paths 与 side effects 真正可观测、哪些地方仍有 blind spots 的覆盖图。

## 4. 清单覆盖率其实也是可观测性

一个经常被忽略的关键点是：可观测性的起点不是漂亮的 trace viewer，而是先知道到底有哪些系统存在。

Microsoft 直接把完整生产清单视为可信遥测的前提。[^ms-inventory]

对智能体资产来说，这意味着你应该知道：

- 哪些 agents 正在 active；
- 哪些已经 deprecated；
- 它们挂着哪些 connectors 和 capabilities；
- 使用哪些 principals；
- 哪些真的在发 telemetry；
- 还有哪些 blind spots 没覆盖。

如果没有 inventory coverage，你就没有完整的 observability。你只有一块被局部照亮的舞台。

## 5. 行为基线比原始流量更重要

在智能体系统里，“请求量比平时更高”这个信号本身并不说明太多。

更重要的是看偏离正常行为的模式：

- risky tool calls 异常增多；
- approval denials 上升；
- approval backlog 老化或 stuck paused runs 出现；
- memory write pattern 变化；
- retrieval profile 改变；
- unusual egress destinations 激增；
- capability-session expiry spikes 或异常 re-init rate；
- interruption 之后 approval 与 resume 的不匹配；
- orchestration-pattern selection 或 worker-boundary crossings 的异常变化；
- session length 或 tool hop count 拉长。

从这里开始，可观测性就真正和安全检测、运行治理连在一起了。

但它不应该直接塌缩成这些功能本身。可观测性是证据基底，它让 assurance、rollout 与 registry functions 能基于同一份可追踪记录推理，而不是依赖彼此冲突的 dashboards、screenshots 或事后回忆。

这个基底讨论的是跨 runs 与 systems 可用的 telemetry。它并不等同于 provenance backbone，后者负责长期保留 approved artifact identity 与 decision lineage。

## 6. 什么叫可用于检测的遥测

`Detection-ready telemetry` 并不只是“我们有日志”。

它意味着这些遥测已经足够支撑：

- 调查；
- 关联；
- 滥用检测；
- 控制验证。

从工程上说，这通常要求：

- 统一 identifiers；
- 稳定 schemas；
- redaction rules；
- retention policy；
- traces、approvals、policy decisions、runtime-control states、capability-session events、orchestration-pattern events、[verifier evidence](../../appendix/eval-schema.zh.md)、verifier contract identity 和 lifecycle artifacts 之间的链接。

如果一条 trace 无法关联到 `approval_id`、`tool_principal`、`policy_bundle`、`contract_version`、`rollout_wave`，以及关于该 run 如何被判定的 [verifier evidence](../../appendix/eval-schema.zh.md)，那它也许对调试有帮助，但作为 evidence layer 还是太弱。

Microsoft 的 observability 指南把 coverage 问题说得更具体：团队应该衡量有多少比例的 AI systems 会发出 logs 和 traces，有多少比例的 releases 运行过标准 evaluation suite，以及有多少比例的 abuse/security scenarios 已经被 telemetry 覆盖。[^ms-observability] 这样，observability 就不再只是“我们有 dashboards”，而是变成可度量的 production obligation：inventory coverage、release-eval coverage 和 detection-scenario coverage。

!!! example "贯穿案例：ticket-write 控制评测的 telemetry"
    support-triage 的控制评测只有在 telemetry 已经 detection-ready 时，才真正能服务 rollout。对每一次 `create_support_ticket` run，trace 都应该关联 `approval_id`、`tool_principal`、`policy_bundle`、`contract_version`、`rollout_wave`、outcome、`side_effect_unknown`，以及 process/outcome verifier verdict。这样团队看到的不只是“没有重复工单”，还包括 ticket-write paths 中有多少真正可观测，哪里还有盲区 bypass path，以及 canary 是否可以安全扩大。

**Observability case-spine note：**trace and telemetry coverage record 应该展示三个 canonical cases 的 observability coverage。Support triage 需要覆盖 ticket-write paths、approval linkage、`tool_principal`、`policy_bundle`、`contract_version`、duplicate outcome 和 bypass blind spots。Internal knowledge assistant 需要覆盖 retrieval provenance、source-grounding verdicts、tenant-filter decisions、memory-write events 和 freshness drift。Incident coordination 需要覆盖 escalation path、notification delivery、responder-role identity、incident-state transitions、rollback events 和 post-incident control changes。

## 7. 为什么没有可观测性的治理往往很脆

治理往往会被写成：

- policy bundles；
- review processes；
- release gates；
- approval contracts。

但如果没有可观测性，这一切很容易退化成纸面控制。

强治理真正需要的是：

- 看到真实行为；
- 发现 drift；
- 衡量 coverage；
- 区分 governed path 和 bypass path；
- 在事故发生前发现 stuck approvals、aging background runs、capability-session expiry drift、approval-resume misuse、orchestration-pattern drift、verifier-quality drift 与 contract mismatches。

所以对智能体系统来说，最好把可观测性理解成`治理的证据层`。

### 7.1. Governance-aware telemetry 会闭合 enforcement loop

下一个成熟度层级，不只是“看见事件”，而是让 telemetry 可以直接服务治理动作。`Governance-aware telemetry` 应该回流到控制闭环，作为 policy decisions、containment、rollout gates 和 incident response 的输入。

最小 closed-loop contract 可以这样定义：

- `policy_decision_feedback`：哪些 telemetry signals 会改变后续 policy decision 或 risk tier；
- `containment_decision`：哪个信号会把 run、agent、capability 或 rollout wave 置为 paused / quarantined state；
- `rollout_gate_input`：哪些 coverage、verifier 和 drift signals 会阻止 canary 扩大；
- `incident_response_trigger`：哪些 patterns 会创建 investigation、escalation 或 postmortem task；
- `registry_update_signal`：哪些 blind spots、stale owners 或 shadow capabilities 需要更新 inventory。

为了避免这只停留在漂亮图示里，每一个这样的事件都应该保存成一个小的 [governance action record](../../appendix/trace-schema.zh.md)：

- `governance_action_id`：治理动作的稳定标识符；
- `source_signal`：触发该动作的 telemetry signal 或 detection scenario；
- `decision_owner`：负责该决定的角色或团队；
- `action_state`：`open`、`accepted`、`waived`、`contained`、`closed`；
- `evidence_refs`：指向 trace、verifier output、policy decision 和 rollout gate 的链接；
- `review_deadline`：该动作必须被重新审查或关闭的时间。

这样 telemetry 就不只是 dashboard signal。它会成为可审查 governance queue 的输入，团队可以看到谁做了决定、依据哪些证据，以及为什么控制闭环可以重新被视为受治理。

这样，telemetry 就不再只是事后的 evidence。它会变成 governance loop 的运行输入：observe → policy decision → containment 或 rollout action → 关于结果的新 evidence。

这种 framing 也把本章和保障章节、注册表章节清楚地区分开来。保障负责遏制与响应；注册表负责资产问责；可观测性则是让二者都可审计的共享基底。

它也应该和 provenance chapter 保持分离。可观测性关注系统是否发出了足够的 evidence、coverage 与 correlation，足以支持调查和检测；provenance 关注的是，后续决策究竟由哪一组 approved artifacts、contract version 或 governed bundle 来支撑。

## 8. 研究前沿正在把可观测性推向哪里

最新的智能体可观测性研究还在继续往前走：它们试图把 traces 从“方便阅读的事件日志”推进成“因果诊断层”。

这里有两点对本书尤其有价值。

第一，单有 trace viewer 并不够。即使 event stream 的界面再漂亮，也不等于真正具备可回答性。如果：

- trace vocabulary 太弱；
- 一个 run 无法关联到 session、approval 和 artifact bundle；
- root cause 仍然只能靠人工通读长 transcript 来重建，

那么可观测性依然不够成熟。

第二，因果诊断很有前景，但现在还不适合被讲成已经解决的问题。研究已经给出了值得跟进的方向，但生产纪律目前仍然要建立在更稳的基础上：

- stable event catalog；
- schema versioning；
- redaction rules；
- session-aware traces；
- telemetry、approvals 和 lifecycle artifacts 之间的明确 linkage。

也就是说，前沿研究的价值不在于让我们承诺“完全可解释性”，而在于提醒我们：可观测性的长期方向应该是从日志记录走向可诊断性。

<div class="diagram-card">
<p>AI-native observability 最好被理解成 telemetry、inventory 与 governance evidence 的组合</p>

``` mermaid
flowchart LR
    A["Inventory coverage"] --> D["AI-native observability"]
    B["Runtime telemetry"] --> D
    C["Policy and approval evidence"] --> D
    D --> E["Incident reconstruction"]
    D --> F["Behavioral baselines"]
    D --> G["Abuse detection"]
    D --> H["Release evidence"]
```

</div>

## 9. 一个最小可观测性覆盖策略

```yaml
observability:
  require:
    request_identity: true
    trace_ids: true
    session_ids: true
    policy_decisions: true
    tool_principals: true
    approval_linkage: true
    paused_run_visibility: true
    capability_session_visibility: true
    background_run_visibility: true
    orchestration_pattern_visibility: true
    worker_boundary_visibility: true
    verifier_evidence_linkage: true
    verifier_contract_visibility: true
    contract_version_linkage: true
    artifact_bundle_linkage: true
  kpis:
    min_agent_inventory_coverage_pct: 95
    min_trace_coverage_pct: 95
    min_high_risk_action_trace_pct: 100
  block_if:
    - untracked_high_risk_agent_exists
    - approval_events_not_linked
    - paused_runs_not_visible
    - capability_session_events_not_visible
    - orchestration_pattern_events_not_visible
    - worker_boundary_crossings_not_visible
    - verifier_evidence_not_linked
    - verifier_contract_missing
    - contract_version_missing
    - bundle_version_missing
```

这样的策略能帮助团队把可观测性当成必需的生产层，而不是平台团队的可选加分项。

## 10. 一个简单的覆盖率检查

```python
from dataclasses import dataclass


@dataclass
class ObservabilityCoverage:
    inventory_coverage_pct: int
    trace_coverage_pct: int
    high_risk_trace_coverage_pct: int
    paused_run_visibility: bool
    capability_session_visibility: bool
    orchestration_pattern_visibility: bool
    verifier_evidence_linked: bool


def observability_ready(state: ObservabilityCoverage) -> bool:
    return (
        state.inventory_coverage_pct >= 95
        and state.trace_coverage_pct >= 95
        and state.high_risk_trace_coverage_pct == 100
        and state.paused_run_visibility
        and state.capability_session_visibility
        and state.orchestration_pattern_visibility
        and state.verifier_evidence_linked
    )
```

这里的重点不是具体数字，而是可观测性就绪度也应该变成明确的门禁。

## 11. 最常见的失效模式

- traces 只覆盖“主 runtime”，却没覆盖真正的 adapters；
- agents 存在于 inventory 之外；
- approvals 单独记录，却不和 traces 关联；
- paused runs 与 background runs 明明存在，但它们的年龄和 ownership 在 telemetry 中不可见；
- telemetry 覆盖了 happy path，却没覆盖 bypass path；
- contract-version drift 只有在 payload 不再匹配预期时才被发现；
- orchestration-pattern drift 或 worker-boundary crossings 没有成为一等遥测；
- [verifier evidence](../../appendix/eval-schema.zh.md) 与 traces 或 screenshots 脱节；
- drift 只能靠用户抱怨才发现；
- retention 和 redaction rules 与取证需求不一致。

## 12. 给 AI-native observability 做一次快速成熟度测试

团队不应该只因为已经有 traces、dashboards 和 log pipeline，就觉得自己已经具备生产级可观测性。

更高的标准应该是：

- inventory coverage 和 telemetry coverage 被当成同一个控制问题；
- high-risk actions 能关联到 approvals、principals、artifact bundles、contract versions、reviewed orchestration patterns 与 [verifier evidence](../../appendix/eval-schema.zh.md)；
- 除了 raw telemetry 之外，还有 behavioral baselines；
- paused-run age、approval backlog 与 background-run aging 都是一等信号；
- unobserved agents 被当成治理风险，而不只是记账缺口；
- telemetry 能作为 release 和 incident decisions 的 evidence。

如果这些条件大多不成立，那团队也许已经有可观测性工具，但还没有真正作为治理层的 AI-native observability。

## 13. 实用检查清单

- 你知道生产资产里到底有多少 agents 吗？
- 其中多少百分比真的会发 structured telemetry？
- 你能把一个 high-risk action 关联到 `trace_id`、`approval_id`、`tool_principal`、`contract_version`、`bundle_id`、当前 orchestration pattern 和 [verifier evidence](../../appendix/eval-schema.zh.md) 吗？
- 你有没有 behavioral baselines，而不只是 raw dashboards？
- 你能否在用户抱怨之前看到 paused-run age、approval backlog 和 aging background runs？
- 你会不会把 unobserved agents 当成一个单独的风险类别？
- 你能把可观测性当成 release evidence，而不是只当 debug aid 吗？

如果连续几个答案都是“否”，那你的可观测性虽然已经存在，但还没有变成治理层。

这通常意味着平台还只能描述活动，却还不能提供那种足以让 reviewer、incident owner 或 estate governor 有信心依赖的稳定证据。

## 14. 本章的证据模型

本章应该被读成一层 evidence readiness，而不是 logging checklist：

- **稳定主张：** 如果 high-risk actions、approvals、principals、artifacts 与 [verifier evidence](../../appendix/eval-schema.zh.md) 事后无法关联，智能体系统就无法被治理。
- **厂商实践：** 当前 observability 与 infrastructure inventory 指南越来越把 telemetry coverage 和 asset coverage 视为生产控制，而不只是 debugging aids。
- **运行时实践：** structured events、inventory coverage checks、behavioral baselines 与 detection-ready fields 让 traces 可以用于 release review 和 incident response。
- **作者解释：** AI-native observability 是 evals、assurance、registry 与 lifecycle governance 之间的桥梁。
- **快速变化层：** tracing products、detectors 与 telemetry pipelines 会继续变化；但 attributable、reviewable evidence 的需求不会。

## 15. 值得配套阅读的参考页

- [Trace Schema 与 Event Catalog](../../appendix/trace-schema.zh.md)
- [Eval Dataset Schema 与 Grading Contract](../../appendix/eval-schema.zh.md)
- [Policy Bundle Schema 与 Approval Contract](../../appendix/policy-bundle-schema.zh.md)
- [Change Review 与 Rollout Gate Schema](../../appendix/change-rollout-schema.zh.md)
- [研究前沿：记忆、可观测性与多智能体可靠性](../../appendix/research-frontier.zh.md)

- [第 11 章：追踪、跨度与结构化事件](../part-v/chapter-11.zh.md)
- [第 13 章：离线评测、在线评测与回归门禁](../part-v/chapter-13.zh.md)
- [第 21 章：保障闭环：红队测试、检测与响应](chapter-21.zh.md)
- [第 25 章：行为评测、控制评测与自动化红队测试](chapter-25.zh.md)
- [第 27 章：智能体清单、注册表与蔓延治理](chapter-27.zh.md)

[^ms-observability]: Microsoft Learn, [Observability for Generative AI and agentic AI systems](https://learn.microsoft.com/en-us/security/zero-trust/sfi/observability-ai-systems)
[^ms-inventory]: Microsoft Learn, [Complete production infrastructure inventory](https://learn.microsoft.com/en-us/security/zero-trust/sfi/complete-production-infrastructure-inventory)
