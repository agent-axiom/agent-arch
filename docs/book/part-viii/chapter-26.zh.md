# 第 26 章：AI 原生可观测性、清单覆盖率与可用于检测的遥测

!!! info "时效说明"
    最近一次编辑审查：**2026 年 5 月 17 日**。上一次审查：**2026 年 5 月 14 日**。下一次计划审查：**2026 年 6 月 17 日**。

    自上次审查以来的变化：MCP/A2A 安全面、验证器契约、治理感知遥测以及出版就绪问题，现在都有具体契约覆盖和文档表面检查。

    变化最快的部分：

    - 面向智能体系统的遥测产品与厂商追踪能力；
    - 面向漂移、滥用和异常工具行为的检测启发式；
    - 面向诊断的追踪以及跨系统关联的新兴约定。

    变化相对较慢的部分：

    - 必须建设可直接用于证据链的遥测，而不只是调试日志；
    - 可观测性必须和审批（approvals）、运行时控制状态（runtime-control states）、策略决策（policy decisions）、工具主体（tool principals）、契约版本（contract versions）与工件包（artifact bundles）关联；
    - 完整的清单覆盖率仍然是检测和事故评审的前提。

## 1. 为什么智能体的可观测性不能只看延迟和错误率

在普通服务里，可观测性往往先看一组很熟悉的东西：

- 延迟；
- 错误率；
- 吞吐量；
- 资源利用率。

但对智能体系统来说，这远远不够。

这里要始终保持一个简单区分：保障负责决定什么时候需要遏制、由谁来响应；可观测性则通过保留可被信任的证据，让这些发布（release）、事故（incident）与治理决策（governance decision）真正有据可依。

系统可能：

- 没有宕机；
- 响应很快；
- 一直返回 HTTP 200；
- 但行为依然危险、低质或者失控。

Microsoft 对这个转变的表述很准确：对智能体系统来说，我们需要把传统的日志、指标和追踪演进成 AI 原生信号（AI-native signals），让系统不仅能说明“发生了请求”，还能说明“系统究竟是怎么行为的”。[^ms-observability]

## 2. 可观测性不只是为了调试

在智能体平台里，可观测性至少承担五种角色：

- 运行时调试；
- 事故重建；
- 滥用检测；
- 发布证据；
- 治理覆盖率。

如果追踪（traces）只是给开发者排查本地缺陷（bug）用的，这已经不够了。

在生产环境里，你还需要回答：

- 一共存在多少智能体（agents）；
- 其中多少是真正可观测的；
- 它们实际调用了哪些能力（capabilities）；
- 高风险动作出现在哪里；
- 哪些审批（approvals）被请求、批准或绕过；
- 发布（rollout）之后出现了哪些行为变化。

## 3. 什么是 AI 原生信号（AI-native signals）

对智能体系统来说，一个有用的遥测契约通常包括：

- 请求身份（request identity）；
- `run_id`、`trace_id`、`session_id`；
- 行动者（actor）与智能体身份（agent identity）；
- 检索出处（retrieval provenance）；
- 工具调用（tool invocations）；
- 工具权限（tool permissions）与主体（principals）；
- 策略决策（policy decisions）；
- 审批（approvals）；
- 暂停运行（paused runs）的状态与等待时长；
- 审批积压信号（approval backlog signals）；
- 能力会话（capability sessions）的状态、到期原因（expiry reason）与重新初始化状态（re-init status）；
- 编排模式选择（orchestration-pattern selection）与委派工作者谱系（delegated worker lineage）；
- 后台运行（background runs）的状态与运行时长；
- 输出摘要（output summaries）；
- 脱敏状态（redaction status）；
- 验证器输出（verifier outputs），例如 `process_score`、`outcome_score` 与 `failure_attribution`；
- 活跃验证器契约（active verifier contract）与验证器契约版本（verifier contract version）；
- 包（bundle）、版本（version）、发布波次（rollout wave）与契约版本（contract version）。

为了避免这份清单变成一堆没有结构的字段，可以把它看成五组信号（signals）：

1. **身份与范围（Identity and scope）：** 谁在行动、代表谁行动、处在哪个租户/请求范围（tenant/request scope）中。
2. **控制证据（Control evidence）：** 哪些策略决策（policy decisions）、审批（approvals）、配额（quotas）和能力会话（capability sessions）约束了这次运行（run）。
3. **执行状态（Execution state）：** 选择了哪种编排模式（orchestration pattern），运行（run）在哪里被暂停/后台化/委派（paused/backgrounded/delegated），又如何恢复（resumed）。
4. **质量证据（Quality evidence）：** 哪些验证器输出（verifier outputs）、评测裁决（eval verdicts）和失败归因（failure attribution）连接到了结果（outcome）。
5. **发布与工件上下文（Release and artifact context）：** 哪个包（bundle）、契约版本（contract version）与发布波次（rollout wave）支撑了这次运行（run）。

也就是说，追踪（traces）不该只告诉你“哪里坏了”，还应该告诉你：

- 是谁在行动；
- 穿过了哪一层控制层；
- 拥有哪些权限；
- 依据哪套规则；
- 属于哪个工件包（artifact bundle）；
- 最终造成了什么副作用。

这也正是为什么运行时控制信号（runtime-control signals）不能继续被当成隐藏的实现细节。只要系统里存在暂停/恢复路径（pause/resume paths）、后台执行（background execution）和契约版本转换（contract-version transitions），它们就已经属于证据层。

但这并不意味着可观测性成了工件谱系的拥有者。可观测性负责在跨运行（runs）的范围内保留和关联证据；而来源证明层仍然回答，后续决策依赖的是哪一个受治理工件、已批准版本或发布身份。

这也正是本章的核心承诺。它要帮助读者把可观测性看成整个生命周期的证据基底：这一层把运行时行为、控制信号、审批（approvals）与跨系统活动保留得足够可见，使保障（assurance）、发布（rollout）、判断（judgment）与注册表函数（registry functions）都能建立在同一份运行记录之上。本章的主要工件是追踪与遥测覆盖记录（trace and telemetry coverage record）：一张说明哪些智能体（agents）、能力（capabilities）、控制路径（control paths）与副作用（side effects）真正可观测、哪些地方仍有盲点（blind spots）的覆盖图。

## 4. 清单覆盖率其实也是可观测性

一个经常被忽略的关键点是：可观测性的起点不是漂亮的追踪查看器（trace viewer），而是先知道到底有哪些系统存在。

Microsoft 直接把完整生产清单视为可信遥测的前提。[^ms-inventory]

对智能体资产来说，这意味着你应该知道：

- 哪些智能体（agents）正在活跃（active）；
- 哪些已经弃用（deprecated）；
- 它们挂着哪些连接器（connectors）和能力（capabilities）；
- 使用哪些主体（principals）；
- 哪些真的在发遥测（telemetry）；
- 还有哪些盲点（blind spots）没覆盖。

如果没有清单覆盖（inventory coverage），你就没有完整的可观测性（observability）。你只有一块被局部照亮的舞台。

## 5. 行为基线比原始流量更重要

在智能体系统里，“请求量比平时更高”这个信号本身并不说明太多。

更重要的是看偏离正常行为的模式：

- 风险工具调用（risky tool calls）异常增多；
- 审批拒绝（approval denials）上升；
- 审批积压（approval backlog）老化或卡住的暂停运行（stuck paused runs）出现；
- 记忆写入模式（memory write pattern）变化；
- 检索画像（retrieval profile）改变；
- 异常出口目的地（unusual egress destinations）激增；
- 能力会话到期峰值（capability-session expiry spikes）或异常重新初始化率（re-init rate）；
- 中断（interruption）之后审批（approval）与恢复（resume）的不匹配；
- 编排模式选择（orchestration-pattern selection）或工作者边界穿越（worker-boundary crossings）的异常变化；
- 会话长度（session length）或工具跳数（tool hop count）拉长。

从这里开始，可观测性就真正和安全检测、运行治理连在一起了。

但它不应该直接塌缩成这些功能本身。可观测性是证据基底，它让保障（assurance）、发布（rollout）与注册表函数（registry functions）能基于同一份可追踪记录推理，而不是依赖彼此冲突的仪表板（dashboards）、截图（screenshots）或事后回忆。

这个基底讨论的是跨运行（runs）与系统（systems）可用的遥测（telemetry）。它并不等同于出处骨干（provenance backbone），后者负责长期保留已批准工件身份（approved artifact identity）与决策谱系（decision lineage）。

## 6. 什么叫可用于检测的遥测

检测就绪遥测（Detection-ready telemetry）并不只是“我们有日志”。

它意味着这些遥测已经足够支撑：

- 调查；
- 关联；
- 滥用检测；
- 控制验证。

从工程上说，这通常要求：

- 统一标识符（identifiers）；
- 稳定模式（schemas）；
- 脱敏规则（redaction rules）；
- 留存策略（retention policy）；
- 追踪（traces）、审批（approvals）、策略决策（policy decisions）、运行时控制状态（runtime-control states）、能力会话事件（capability-session events）、编排模式事件（orchestration-pattern events）、[验证器证据（verifier evidence）](../../appendix/eval-schema.zh.md)、验证器契约身份（verifier contract identity）和生命周期工件（lifecycle artifacts）之间的链接。

如果一条追踪（trace）无法关联到 `approval_id`、`tool_principal`、`policy_bundle`、`contract_version`、`rollout_wave`，以及关于该运行（run）如何被判定的 [验证器证据（verifier evidence）](../../appendix/eval-schema.zh.md)，那它也许对调试有帮助，但作为证据层（evidence layer）还是太弱。

Microsoft 的可观测性（observability）指南把覆盖问题（coverage）说得更具体：团队应该衡量有多少比例的 AI 系统（AI systems）会发出日志（logs）和追踪（traces），有多少比例的发布（releases）运行过标准评测套件（evaluation suite），以及有多少比例的滥用/安全场景（abuse/security scenarios）已经被遥测（telemetry）覆盖。[^ms-observability] 这样，可观测性（observability）就不再只是“我们有仪表板（dashboards）”，而是变成可度量的生产义务（production obligation）：清单覆盖（inventory coverage）、发布评测覆盖（release-eval coverage）和检测场景覆盖（detection-scenario coverage）。

!!! example "贯穿案例：工单写入（ticket-write）控制评测的遥测（telemetry）"
    支持分诊（support-triage）的控制评测只有在遥测（telemetry）已经具备检测就绪状态（detection-ready）时，才真正能服务发布（rollout）。对每一次 `create_support_ticket` 运行（run），追踪（trace）都应该关联 `approval_id`、`tool_principal`、`policy_bundle`、`contract_version`、`rollout_wave`、结果（outcome）、`side_effect_unknown`，以及过程/结果验证器裁决（process/outcome verifier verdict）。这样团队看到的不只是“没有重复工单”，还包括工单写入路径（ticket-write paths）中有多少真正可观测，哪里还有绕过路径（bypass path）盲区，以及金丝雀（canary）是否可以安全扩大。

**可观测性案例主线说明（Observability case-spine note）：**[追踪与遥测覆盖记录（trace and telemetry coverage record）](../../appendix/trace-schema.zh.md) 应该展示三个规范案例（canonical cases）的可观测性覆盖（observability coverage）。支持分诊（Support triage）需要覆盖工单写入路径（ticket-write paths）、[审批链接（approval linkage）](../../appendix/approval-schema.zh.md)、`tool_principal`、[`policy_bundle`](../../appendix/policy-bundle-schema.zh.md)、`contract_version`、重复结果（duplicate outcome）和绕过盲点（bypass blind spots）。内部知识助手（Internal knowledge assistant）需要覆盖 [检索来源追踪（retrieval provenance）](../../appendix/memory-retrieval-schema.zh.md)、来源扎根裁决（source-grounding verdicts）、租户过滤决策（tenant-filter decisions）、[记忆写入事件（memory-write events）](../../appendix/memory-retrieval-schema.zh.md) 和新鲜度漂移（freshness drift）。事故协调（Incident coordination）需要覆盖升级路径（escalation path）、通知送达（notification delivery）、响应者角色身份（responder-role identity）、[事故状态转换（incident-state transitions）](../../appendix/incident-record-schema.zh.md)、回滚事件（rollback events）和 [事故后控制变更（post-incident control changes）](../../appendix/lifecycle-artifact-schema.zh.md)。

## 7. 为什么没有可观测性的治理往往很脆

治理往往会被写成：

- 策略包（policy bundles）；
- 评审流程（review processes）；
- 发布门禁（release gates）；
- 审批契约（approval contracts）。

但如果没有可观测性，这一切很容易退化成纸面控制。

强治理真正需要的是：

- 看到真实行为；
- 发现漂移（drift）；
- 衡量覆盖率（coverage）；
- 区分受治理路径（governed path）和绕过路径（bypass path）；
- 在事故发生前发现卡住的审批（stuck approvals）、老化的后台运行（aging background runs）、能力会话到期漂移（capability-session expiry drift）、审批恢复误用（approval-resume misuse）、编排模式漂移（orchestration-pattern drift）、验证器质量漂移（verifier-quality drift）与契约不匹配（contract mismatches）。

所以对智能体系统来说，最好把可观测性理解成`治理的证据层`。

### 7.1. 治理感知遥测（Governance-aware telemetry）会闭合执行闭环（enforcement loop）

下一个成熟度层级，不只是“看见事件”，而是让遥测（telemetry）可以直接服务治理动作。治理感知遥测（Governance-aware telemetry）应该回流到控制闭环，作为策略决策（policy decisions）、遏制（containment）、发布门禁（rollout gates）和事故响应（incident response）的输入。

最小闭环契约（closed-loop contract）可以这样定义：

- `policy_decision_feedback`：哪些遥测信号（telemetry signals）会改变后续策略决策（policy decision）或风险层级（risk tier）；
- `containment_decision`：哪个信号会把运行（run）、智能体（agent）、能力（capability）或发布波次（rollout wave）置为暂停/隔离状态（paused / quarantined state）；
- `rollout_gate_input`：哪些覆盖（coverage）、验证器（verifier）和漂移信号（drift signals）会阻止金丝雀（canary）扩大；
- `incident_response_trigger`：哪些模式（patterns）会创建调查（investigation）、升级（escalation）或复盘任务（postmortem task）；
- `registry_update_signal`：哪些盲点（blind spots）、过期负责人（stale owners）或影子能力（shadow capabilities）需要更新清单（inventory）。

为了避免这只停留在漂亮图示里，每一个这样的事件都应该保存成一个小的[治理动作记录（governance action record）](../../appendix/trace-schema.zh.md)：

- `governance_action_id`：治理动作的稳定标识符；
- `source_signal`：触发该动作的遥测信号（telemetry signal）或检测场景（detection scenario）；
- `decision_owner`：负责该决定的角色或团队；
- `action_state`：开放（`open`）、已接受（`accepted`）、已豁免（`waived`）、已遏制（`contained`）、已关闭（`closed`）；
- `evidence_refs`：指向追踪（trace）、验证器输出（verifier output）、策略决策（policy decision）和发布门禁（rollout gate）的链接；
- `review_deadline`：该动作必须被重新审查或关闭的时间。

这样，遥测（telemetry）就不只是仪表板信号（dashboard signal）。它会成为可审查治理队列（governance queue）的输入，团队可以看到谁做了决定、依据哪些证据，以及为什么控制闭环可以重新被视为受治理。

这样，遥测（telemetry）就不再只是事后的证据（evidence）。它会变成治理闭环（governance loop）的运行输入：观察（observe）→ 策略决策（policy decision）→ 遏制（containment）或发布动作（rollout action）→ 关于结果的新证据（evidence）。

这种框架（framing）也把本章和保障章节、注册表章节清楚地区分开来。保障负责遏制与响应；注册表负责资产问责；可观测性则是让二者都可审计的共享基底。

它也应该和来源链章节（provenance chapter）保持分离。可观测性关注系统是否发出了足够的证据（evidence）、覆盖（coverage）与关联（correlation），足以支持调查和检测；来源链（provenance）关注的是，后续决策究竟由哪一组已批准工件（approved artifacts）、契约版本（contract version）或受治理包（governed bundle）来支撑。

### 7.2. 将闭环映射到 NIST AI RMF（Mapping the Loop to NIST AI RMF）

这个闭环（closed loop）也提供了一种务实方式，把可观测性（observability）映射到 NIST AI RMF，而不是把本章变成合规清单（compliance checklist）。[^nist-ai-rmf]

- **治理（Govern）**：`decision_owner`、`review_deadline` 和注册表覆盖（registry coverage）说明谁拥有这个信号（signal），以及哪条治理队列（governance queue）必须关闭它。
- **映射（Map）**：`source_signal`、清单覆盖（inventory coverage）和绕过路径遥测（bypass-path telemetry）说明实际处于风险（risk）中的是哪个智能体（agent）、能力（capability）、租户（tenant）或发布表面（rollout surface）。
- **度量（Measure）**：`evidence_refs`、验证器输出（verifier outputs）、覆盖率（coverage ratios）、漂移信号（drift signals）和检测场景（detection scenarios）把风险（risk）变成可观测证据（observable evidence）。
- **管理（Manage）**：`policy_decision_feedback`、`containment_decision`、`rollout_gate_input` 和 `incident_response_trigger` 说明证据（evidence）之后触发了哪项控制动作（control action）。

这个映射（mapping）故意保持可操作（operational）。问题不是仪表板（dashboard）有没有写治理（Govern）、映射（Map）、度量（Measure）、管理（Manage），而是审查者（reviewer）是否能把一个遥测信号（telemetry signal）追踪到负责人（owner）、风险表面（risk surface）、度量证据（measurement evidence）和最终控制动作（control action）。

## 8. 研究前沿正在把可观测性推向哪里

最新的智能体可观测性研究还在继续往前走：它们试图把追踪（traces）从“方便阅读的事件日志”推进成“因果诊断层”。

这里有两点对本书尤其有价值。

第一，单有追踪查看器（trace viewer）并不够。即使事件流（event stream）的界面再漂亮，也不等于真正具备可回答性。如果：

- 追踪词汇表（trace vocabulary）太弱；
- 一个运行（run）无法关联到会话（session）、审批（approval）和工件包（artifact bundle）；
- 根因（root cause）仍然只能靠人工通读长转录（transcript）来重建，

那么可观测性依然不够成熟。

第二，因果诊断很有前景，但现在还不适合被讲成已经解决的问题。研究已经给出了值得跟进的方向，但生产纪律目前仍然要建立在更稳的基础上：

- 稳定事件目录（stable event catalog）；
- 模式版本控制（schema versioning）；
- 脱敏规则（redaction rules）；
- 会话感知追踪（session-aware traces）；
- 遥测（telemetry）、审批（approvals）和生命周期工件（lifecycle artifacts）之间的明确链接（linkage）。

也就是说，前沿研究的价值不在于让我们承诺“完全可解释性”，而在于提醒我们：可观测性的长期方向应该是从日志记录走向可诊断性。

<div class="diagram-card">
<p>AI 原生可观测性（AI-native observability）最好被理解成遥测（telemetry）、清单（inventory）与治理证据（governance evidence）的组合</p>

``` mermaid
flowchart LR
    A["清单覆盖 / Inventory coverage"] --> D["AI 原生可观测性 / AI-native observability"]
    B["运行时遥测 / Runtime telemetry"] --> D
    C["策略与审批证据 / Policy and approval evidence"] --> D
    D --> E["事故重建 / Incident reconstruction"]
    D --> F["行为基线 / Behavioral baselines"]
    D --> G["滥用检测 / Abuse detection"]
    D --> H["发布证据 / Release evidence"]
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

- 追踪（traces）只覆盖“主运行时（runtime）”，却没覆盖真正的适配器（adapters）；
- 智能体（agents）存在于清单（inventory）之外；
- 审批（approvals）单独记录，却不和追踪（traces）关联；
- 暂停运行（paused runs）与后台运行（background runs）明明存在，但它们的年龄（age）和责任归属（ownership）在遥测（telemetry）中不可见；
- 遥测（telemetry）覆盖了正常路径（happy path），却没覆盖绕过路径（bypass path）；
- 契约版本漂移（contract-version drift）只有在载荷（payload）不再匹配预期时才被发现；
- 编排模式漂移（orchestration-pattern drift）或工作者边界穿越（worker-boundary crossings）没有成为一等遥测；
- [验证器证据（verifier evidence）](../../appendix/eval-schema.zh.md) 与追踪（traces）或截图（screenshots）脱节；
- 漂移（drift）只能靠用户抱怨才发现；
- 留存（retention）和脱敏规则（redaction rules）与取证需求不一致。

## 12. 给 AI 原生可观测性（AI-native observability）做一次快速成熟度测试

团队不应该只因为已经有追踪（traces）、仪表板（dashboards）和日志管线（log pipeline），就觉得自己已经具备生产级可观测性。

更高的标准应该是：

- 清单覆盖（inventory coverage）和遥测覆盖（telemetry coverage）被当成同一个控制问题；
- 高风险动作（high-risk actions）能关联到审批（approvals）、主体（principals）、工件包（artifact bundles）、契约版本（contract versions）、已审查的编排模式（reviewed orchestration patterns）与 [验证器证据（verifier evidence）](../../appendix/eval-schema.zh.md)；
- 除了原始遥测（raw telemetry）之外，还有行为基线（behavioral baselines）；
- 暂停运行年龄（paused-run age）、审批积压（approval backlog）与后台运行老化（background-run aging）都是一等信号；
- 未观测智能体（unobserved agents）被当成治理风险，而不只是记账缺口；
- 遥测（telemetry）能作为发布与事故决策证据（release and incident decisions evidence）。

如果这些条件大多不成立，那团队也许已经有可观测性工具，但还没有真正作为治理层的 AI 原生可观测性（AI-native observability）。

## 13. 实用检查清单

- 你知道生产资产里到底有多少智能体（agents）吗？
- 其中多少百分比真的会发结构化遥测（structured telemetry）？
- 你能把一个高风险动作（high-risk action）关联到 `trace_id`、`approval_id`、`tool_principal`、`contract_version`、`bundle_id`、当前编排模式（orchestration pattern）和 [验证器证据（verifier evidence）](../../appendix/eval-schema.zh.md) 吗？
- 你有没有行为基线（behavioral baselines），而不只是原始仪表板（raw dashboards）？
- 你能否在用户抱怨之前看到暂停运行年龄（paused-run age）、审批积压（approval backlog）和后台运行老化（aging background runs）？
- 你会不会把未观测智能体（unobserved agents）当成一个单独的风险类别？
- 你能把可观测性当成发布证据（release evidence），而不是只当调试辅助（debug aid）吗？

如果连续几个答案都是“否”，那你的可观测性虽然已经存在，但还没有变成治理层。

这通常意味着平台还只能描述活动，却还不能提供那种足以让审查者（reviewer）、事故负责人（incident owner）或智能体群体治理者（estate governor）有信心依赖的稳定证据。

## 14. 本章的证据模型

本章应该被读成一层证据就绪度（evidence readiness），而不是日志清单（logging checklist）：

- **稳定主张：** 如果高风险动作（high-risk actions）、审批（approvals）、主体（principals）、工件（artifacts）与 [验证器证据（verifier evidence）](../../appendix/eval-schema.zh.md) 事后无法关联，智能体系统就无法被治理。
- **厂商实践：** 当前可观测性（observability）与基础设施清单（infrastructure inventory）指南越来越把遥测覆盖（telemetry coverage）和资产覆盖（asset coverage）视为生产控制，而不只是调试辅助（debugging aids）。
- **运行时实践：** 结构化事件（structured events）、清单覆盖检查（inventory coverage checks）、行为基线（behavioral baselines）与检测就绪字段（detection-ready fields）让追踪（traces）可以用于发布审查（release review）和事故响应（incident response）。
- **作者解释：** AI 原生可观测性（AI-native observability）是评测（evals）、保障（assurance）、注册表（registry）与生命周期治理（lifecycle governance）之间的桥梁。
- **快速变化层：** 追踪产品（tracing products）、检测器（detectors）与遥测管线（telemetry pipelines）会继续变化；但可归因、可审查证据（attributable, reviewable evidence）的需求不会。

## 15. 值得配套阅读的参考页

- [追踪模式与事件目录](../../appendix/trace-schema.zh.md)
- [评测数据集模式与打分契约](../../appendix/eval-schema.zh.md)
- [策略包模式与审批契约](../../appendix/policy-bundle-schema.zh.md)
- [审批请求与决策记录模式](../../appendix/approval-schema.zh.md)
- [生命周期工件模式](../../appendix/lifecycle-artifact-schema.zh.md)
- [变更评审与发布门禁模式](../../appendix/change-rollout-schema.zh.md)
- [记忆记录与检索契约模式](../../appendix/memory-retrieval-schema.zh.md)
- [研究前沿：记忆、可观测性与多智能体可靠性](../../appendix/research-frontier.zh.md)

- [第 11 章：追踪、跨度与结构化事件](../part-v/chapter-11.zh.md)
- [第 13 章：离线评测、在线评测与回归门禁](../part-v/chapter-13.zh.md)
- [第 21 章：保障闭环：红队测试、检测与响应](chapter-21.zh.md)
- [第 25 章：行为评测、控制评测与自动化红队测试](chapter-25.zh.md)
- [第 27 章：智能体清单、注册表与蔓延治理](chapter-27.zh.md)

[^ms-observability]: Microsoft Learn, [Observability for Generative AI and agentic AI systems](https://learn.microsoft.com/en-us/security/zero-trust/sfi/observability-ai-systems)
[^ms-inventory]: Microsoft Learn, [Complete production infrastructure inventory](https://learn.microsoft.com/en-us/security/zero-trust/sfi/complete-production-infrastructure-inventory)

[^nist-ai-rmf]: NIST, [Artificial Intelligence Risk Management Framework (AI RMF 1.0)](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10)
