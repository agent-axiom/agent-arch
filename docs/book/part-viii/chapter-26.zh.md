# 第 26 章：AI 原生可观测性、清单覆盖率与可用于检测的遥测

!!! info "时效说明"
    本章内容截至 2026 年 4 月 11 日。

    变化最快的部分：

    - 面向智能体系统的遥测产品与厂商追踪能力；
    - 面向漂移、滥用和异常工具行为的检测启发式；
    - 面向诊断的追踪以及跨系统关联的新兴约定。

    变化相对较慢的部分：

    - 必须建设可直接用于证据链的遥测，而不只是调试日志；
    - 可观测性必须和 approvals、runtime-control states、policy decisions、tool principals、contract versions 与 artifact bundles 关联；
    - 完整的清单覆盖率仍然是 detection 和 incident review 的前提。

## 1. 为什么智能体的可观测性不能只看延迟和错误率

在普通服务里，可观测性往往先看一组很熟悉的东西：

- 延迟；
- 错误率；
- 吞吐量；
- 资源利用率。

但对智能体系统来说，这远远不够。

这里要始终保持一个简单区分：assurance 负责决定什么时候需要 containment、由谁来响应；可观测性则通过保留可被信任的 evidence，让这些 release、incident 与 governance decision 真正有据可依。

系统可能：

- 没有宕机；
- 响应很快；
- 一直返回 HTTP 200；
- 但行为依然危险、低质或者失控。

Microsoft 对这个转变的表述很准确：对 agentic systems 来说，我们需要把传统的 logs、metrics 和 traces 演进成 `AI-native signals`，让系统不仅能说明“发生了请求”，还能说明“系统究竟是怎么行为的”。 [^ms-observability]

## 2. 可观测性不只是为了调试

在 agent platform 里，observability 至少承担五种角色：

- runtime debugging；
- incident reconstruction；
- abuse detection；
- release evidence；
- governance coverage。

如果 traces 只是给开发者排查本地 bug 用的，这已经不够了。

在 production 里，你还需要回答：

- 一共存在多少 agents；
- 其中多少是真正可观测的；
- 它们实际调用了哪些 capabilities；
- high-risk actions 出现在哪里；
- 哪些 approvals 被请求、批准或绕过；
- rollout 之后出现了哪些 behavior shifts。

## 3. 什么是 AI-native signals

对 agent systems 来说，一个有用的 telemetry contract 通常包括：

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

也就是说，traces 不该只告诉你“哪里坏了”，还应该告诉你：

- 是谁在行动；
- 穿过了哪一层 control layer；
- 拥有哪些权限；
- 依据哪套规则；
- 属于哪个 artifact bundle；
- 最终造成了什么 side effect。

这也正是为什么 runtime-control signals 不能继续被当成隐藏的 implementation detail。只要系统里存在 pause/resume paths、background execution 和 contract-version transitions，它们就已经属于 evidence layer。

但这并不意味着 observability 成了 artifact lineage 的拥有者。Observability 负责在跨 runs 的范围内保留和关联 evidence；而 provenance layer 仍然回答，后续决策依赖的是哪一个 governed artifact、approved version 或 release identity。

这也正是本章的核心承诺。它要帮助读者把 observability 看成整个生命周期的 evidence substrate：这一层把 runtime behavior、control signals、approvals 与跨系统活动保留得足够可见，使 assurance、rollout、judgment 与 registry functions 都能建立在同一份 operational record 之上。

## 4. Inventory coverage 其实也是 observability

一个经常被忽略的关键点是：observability 的起点不是漂亮的 trace viewer，而是先知道到底有哪些 systems 存在。

Microsoft 直接把 complete production inventory 视为 trusted telemetry 的前提。 [^ms-inventory]

对 agent estate 来说，这意味着你应该知道：

- 哪些 agents 正在 active；
- 哪些已经 deprecated；
- 它们挂着哪些 connectors 和 capabilities；
- 使用哪些 principals；
- 哪些真的在发 telemetry；
- 还有哪些 blind spots 没覆盖。

如果没有 inventory coverage，你就没有完整的 observability。你只有一块被局部照亮的舞台。

## 5. Behavioral baselines 比 raw volume 更重要

在 agent systems 里，“请求量比平时更高”这个信号本身并不说明太多。

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

从这里开始，observability 就真正和 security detection、operational governance 连在一起了。

但它不应该直接塌缩成这些功能本身。Observability 是 evidence substrate，它让 assurance、rollout 与 registry functions 能基于同一份 traceable record 推理，而不是依赖彼此冲突的 dashboards、screenshots 或事后回忆。

这个 substrate 讨论的是跨 runs 与 systems 可用的 telemetry。它并不等同于 provenance backbone，后者负责长期保留 approved artifact identity 与 decision lineage。

## 6. 什么叫 detection-ready telemetry

`Detection-ready telemetry` 并不只是“我们有日志”。

它意味着这些 telemetry 已经足够支撑：

- 调查；
- correlation；
- abuse detection；
- control verification。

从工程上说，这通常要求：

- 统一 identifiers；
- 稳定 schemas；
- redaction rules；
- retention policy；
- traces、approvals、policy decisions、runtime-control states、capability-session events、orchestration-pattern events、verifier evidence、verifier contract identity 和 lifecycle artifacts 之间的链接。

如果一条 trace 无法关联到 `approval_id`、`tool_principal`、`policy_bundle`、`contract_version`、`rollout_wave`，以及关于该 run 如何被判定的 verifier evidence，那它也许对调试有帮助，但作为 evidence layer 还是太弱。

## 7. 为什么没有 observability 的 governance 往往很脆

Governance 往往会被写成：

- policy bundles；
- review processes；
- release gates；
- approval contracts。

但如果没有 observability，这一切很容易退化成纸面控制。

强治理真正需要的是：

- 看到真实行为；
- 发现 drift；
- 衡量 coverage；
- 区分 governed path 和 bypass path；
- 在事故发生前发现 stuck approvals、aging background runs、capability-session expiry drift、approval-resume misuse、orchestration-pattern drift、verifier-quality drift 与 contract mismatches。

所以对 agent systems 来说，最好把 observability 理解成 `governance 的证据层`。

这种 framing 也把本章和 assurance chapter、registry chapter 清楚地区分开来。Assurance 负责 containment 与 response；registry 负责 estate accountability；observability 则是让二者都可审计的 shared substrate。

它也应该和 provenance chapter 保持分离。Observability 关注系统是否发出了足够的 evidence、coverage 与 correlation，足以支持调查和 detection；provenance 关注的是，后续决策究竟由哪一组 approved artifacts、contract version 或 governed bundle 来支撑。

## 8. Research frontier 正在把 observability 推向哪里

最新的 agent observability 研究还在继续往前走：它们试图把 traces 从“方便阅读的事件日志”推进成“因果诊断层”。

这里有两点对本书尤其有价值。

第一，单有 trace viewer 并不够。即使 event stream 的界面再漂亮，也不等于真正具备 answerability。如果：

- trace vocabulary 太弱；
- 一个 run 无法关联到 session、approval 和 artifact bundle；
- root cause 仍然只能靠人工通读长 transcript 来重建，

那么可观测性依然不够成熟。

第二，causal diagnosis 很有前景，但现在还不适合被讲成 solved problem。Research 已经给出了值得跟进的方向，但 production discipline 目前仍然要建立在更稳的基础上：

- stable event catalog；
- schema versioning；
- redaction rules；
- session-aware traces；
- telemetry、approvals 和 lifecycle artifacts 之间的明确 linkage。

也就是说，frontier 的价值不在于让我们承诺“完全 explainability”，而在于提醒我们：observability 的长期方向应该是从 logging 走向 diagnosability。

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

## 9. 一个最小 observability coverage policy

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

这样的 policy 能帮助团队把 observability 当成必需的 production layer，而不是平台团队的可选加分项。

## 10. 一个简单的 coverage check

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

这里的重点不是具体数字，而是 observability readiness 也应该变成明确的 gate。

## 11. 最常见的 failure modes

- traces 只覆盖“主 runtime”，却没覆盖真正的 adapters；
- agents 存在于 inventory 之外；
- approvals 单独记录，却不和 traces 关联；
- paused runs 与 background runs 明明存在，但它们的年龄和 ownership 在 telemetry 中不可见；
- telemetry 覆盖了 happy path，却没覆盖 bypass path；
- contract-version drift 只有在 payload 不再匹配预期时才被发现；
- orchestration-pattern drift 或 worker-boundary crossings 没有成为 first-class telemetry；
- verifier evidence 与 traces 或 screenshots 脱节；
- drift 只能靠用户抱怨才发现；
- retention 和 redaction rules 与 forensic needs 不一致。

## 12. 给 AI-native observability 做一次快速成熟度测试

团队不应该只因为已经有 traces、dashboards 和 log pipeline，就觉得自己已经具备 production observability。

更高的标准应该是：

- inventory coverage 和 telemetry coverage 被当成同一个 control problem；
- high-risk actions 能关联到 approvals、principals、artifact bundles、contract versions、reviewed orchestration patterns 与 verifier evidence；
- 除了 raw telemetry 之外，还有 behavioral baselines；
- paused-run age、approval backlog 与 background-run aging 都是 first-class signals；
- unobserved agents 被当成 governance risk，而不只是记账缺口；
- telemetry 能作为 release 和 incident decisions 的 evidence。

如果这些条件大多不成立，那团队也许已经有 observability tooling，但还没有真正作为 governance layer 的 AI-native observability。

## 13. 实用检查清单

- 你知道 production estate 里到底有多少 agents 吗？
- 其中多少百分比真的会发 structured telemetry？
- 你能把一个 high-risk action 关联到 `trace_id`、`approval_id`、`tool_principal`、`contract_version`、`bundle_id`、当前 orchestration pattern 和 verifier evidence 吗？
- 你有没有 behavioral baselines，而不只是 raw dashboards？
- 你能否在用户抱怨之前看到 paused-run age、approval backlog 和 aging background runs？
- 你会不会把 unobserved agents 当成一个单独的 risk class？
- 你能把 observability 当成 release evidence，而不是只当 debug aid 吗？

如果连续几个答案都是“否”，那你的 observability 虽然已经存在，但还没有变成 governance layer。

这通常意味着平台还只能描述 activity，却还不能提供那种足以让 reviewer、incident owner 或 estate governor 有信心依赖的稳定 evidence。

## 14. 值得配套阅读的参考页

- [Trace Schema 与 Event Catalog](../../appendix/trace-schema.zh.md)
- [Eval Dataset Schema 与 Grading Contract](../../appendix/eval-schema.zh.md)
- [Policy Bundle Schema 与 Approval Contract](../../appendix/policy-bundle-schema.zh.md)
- [Change Review 与 Rollout Gate Schema](../../appendix/change-rollout-schema.zh.md)
- [研究前沿：记忆、可观测性与多智能体可靠性](../../appendix/research-frontier.zh.md)

- [第 11 章：Traces、Spans 与 Structured Events](../part-v/chapter-11.zh.md)
- [第 13 章：Offline Evals、Online Evals 与 Regression Gates](../part-v/chapter-13.zh.md)
- [第 21 章：保障闭环：红队测试、检测与响应](chapter-21.zh.md)
- [第 25 章：行为评测、控制评测与自动化红队测试](chapter-25.zh.md)
- [第 27 章：智能体清单、注册表与蔓延治理](chapter-27.zh.md)

[^ms-observability]: Microsoft Learn, [Observability for Generative AI and agentic AI systems](https://learn.microsoft.com/en-us/security/zero-trust/sfi/observability-ai-systems)
[^ms-inventory]: Microsoft Learn, [Complete production infrastructure inventory](https://learn.microsoft.com/en-us/security/zero-trust/sfi/complete-production-infrastructure-inventory)
