# 第 21 章：保障闭环：红队测试、检测与响应

!!! info "时效说明"
    本章内容截至 2026 年 4 月 11 日。

    变化最快的部分：

    - 红队技术、场景生成器和自动化攻击脚手架；
    - 各家平台围绕智能体系统提供的保障与检测建议；
    - 对行为类 findings 的分类和优先级实践。

    变化相对较慢的部分：

    - 保障必须是持续闭环，而不是一次性评审；
    - findings 需要进入带 owner、remediation 和 rollback logic 的 backlog；
    - incidents、detection、redesign 和 rollout 规则变更之间必须闭环。

## 1. 为什么生命周期不会在发布门禁处结束

到这里为止，我们已经有了一幅更成熟的图景：

- 智能体系统已经进入 ADLC；
- 变更会经过变更管理；
- 发布不再是盲目推进。

但这仍然不够。

因为智能体系统有一类特别的风险：

- 涌现行为；
- 通过提示或工具路径发生的滥用；
- 长流程中的漂移；
- 隐蔽的策略绕过；
- 不安全的副作用；
- 团队发现得太晚的退化。

所以在发布纪律之外，还必须再补上一层：保障闭环。

这里有一个关键区分：eval loop 负责帮助团队判断系统行为是在变好还是变坏；assurance loop 负责决定应该立刻遏制什么、谁来响应，以及当新风险出现时怎样强制把系统拉回到更安全的状态。

这意味着，本章正是从那些 budget-setting chapters 停下来的地方开始。SLO 定义可容忍的 health budgets 与 risk budgets；assurance 则在这些 budgets 受到威胁、已经失守，或者已经不再值得信任时开始要求团队采取行动。

这也正是本章的核心承诺。它要帮助读者把 assurance 看成整个生命周期里的 response function，而不是一组松散的 security activities：在这里，signals 会被转化成 containment、ownership、remediation，以及把系统强行带回更安全运行状态的动作。

如果你想看一页专门把 request、policy、approvals、traces、evals、incidents 和 rollout judgment 串成同一条可复核链路的桥接页，可以直接打开 [Evidence Spine](../part-v/evidence-spine.zh.md)。

## 2. 什么是保障闭环

可以这样定义保障闭环：

它是一套持续运行的循环，帮助团队不只是发布变更，还能系统性地发现薄弱点、察觉新威胁、调查问题并把问题真正关掉。

在智能体系统里，它通常包括：

- 红队测试；
- 漏洞管理；
- 检测与响应；
- 修复；
- 把经验重新写回设计和发布流程。

Google Research 在这里给出的核心观点很清楚：生成式系统的安全保障应该是一种持续能力，而不是一次性的审查活动。[^google-assurance]

## 3. 红队测试应该针对真实失效模式，而不是演示效果

太多团队把红队测试做成了展示：

- 试几个明显的越狱提示；
- 展示系统“扛住了一些东西”；
- 然后就觉得问题结束了。

这不是强保障。

对智能体系统有价值的红队测试，应该针对与生产环境相关的失效模式：

同时，也应该单独测试 verifier layer，尤其是在团队依赖 automated grading 或 computer-use trajectory judges 时。薄弱的 verifier 可能把不安全行为误判成安全，也可能把 environment-caused failure 放大成嘈杂的 false alarms。

- prompt injection；
- 隐蔽指令覆盖；
- 工具滥用；
- 不安全的出口访问；
- 审批绕过；
- cross-tenant retrieval leakage；
- memory poisoning；
- 过度自主性。

好的红队测试不只看模型回答，还要看整个执行路径。

这也是 failed-run drills 应该被放进这里的原因。timeout、validation failure，或者上游依赖故障场景，不只是 rollout artifact，也是一种 assurance scenario，因为团队必须知道退化行为在压力下是否仍然可复核、可遏制、可归因，包括通过像 `failure_reason` 这样的明确字段。

## 4. 漏洞应该进入 backlog，而不是停留在感受里

如果 red teaming 只留下“这里感觉有点危险”的印象，团队很难高质量行动。

更成熟的方式是把它放进正常的漏洞工作流：

- 到底发现了什么；
- 风险等级是什么；
- 利用路径是什么；
- 什么算 fix；
- 负责人是谁；
- 修复截止时间是什么；
- 是否需要临时缓解措施。

这是一个很典型的 SDLC 式逻辑：发现结果必须成为可管理的工程对象，而不是工作坊之后的印象笔记。

## 5. 检测不能只盯着错误率

在普通服务里，检测常常围绕错误率、延迟和基础设施信号展开。对智能体系统来说，这远远不够。

你还需要能看到：

- verifier 在 unsafe trajectories 上的 false-positive spikes；
- verifier 在 blocked-but-correct trajectories 上的 false-negative spikes；

- 被拒动作的异常增长；
- 审批积压；
- stuck paused approvals 或异常偏大的 paused-run age；
- capability-session expiry 的异常升高；
- stateful capability paths 中无法解释的 re-initialization rate 上升；
- run 与 approval records 之间的 delegated principal mismatch；
- 超出预期 pause/resume rules 的 delegated scope reuse；
- revoked authorization 仍然抵达 execution 的情况；
- 异常的工具选择模式；
- 新出现的出口目标；
- 记忆写入异常；
- 不安全回退行为的上升；
- 任务成功率和安全指标的漂移；
- stale background runs；
- 预期 payload 形态与实际观测形态之间的 contract drift；
- orchestration-pattern regressions，例如意外的 routing-path drift、不稳定的 join-state behavior，或超出 reviewed boundaries 的 delegated worker activity；
- verifier drift，例如它在 process quality、outcome quality 或 failure attribution 上与人工评审失去一致性；
- 未经 reviewed rollout control 的 verifier contract version changes，它们会悄悄改变 grading behavior。

也就是说，这里的检测既是可观测性，也是滥用与安全监测。

这也是本章必须和 observability layer 保持边界的地方。Observability 提供 evidence substrate；assurance 决定哪些信号此刻重要、哪些信号要触发 containment，以及哪个 owner 必须行动。

它也必须和 SLO 保持边界。SLO 说明还能容忍多少退化或不安全行为；assurance 则是在这种容忍度不再可接受时，负责升级、遏制并分配响应责任的闭环。

## 6. 响应应该是一层独立的运行能力

当一个智能体开始表现出危险行为时，光说“之后再调提示”是不够的。

更实用的响应层应该围绕具体动作来设计：

- 限制能力；
- 把动作切到仅审批模式；
- 取消或使 stuck paused runs 过期；
- 对 stale executions 的 route 暂停 background mode；
- 收紧出口策略；
- 关闭高风险记忆写入；
- 冻结 stateful capability path 的 re-initialization；
- 把发布波次切回更安全的配置；
- 必要时直接停用有问题的路由。

同一层 response layer 也必须把 runtime failure paths 当成独立的受治理事件来处理。Tool timeout、validation failure，或者上游依赖不可用，都不该被塞进笼统的 "run completed" 话术里。系统应该记录 failed run、保留 trace，并让 session-level evidence 中同时持续保留这个结果以及具体失败原因，例如放在 `failure_reason` 中，这样 assurance 才能区分被拦下来的风险、基础设施退化，以及 runtime-control behavior 本身的失效。

这很关键，因为在智能体系统里，响应往往必须比完整的根因分析更快发生。

所以这里的 assurance 更应该被理解成 response function，而不只是 detection catalog。它的职责，是尽量缩短 signal 与 safe containment 之间的时间。

Budget 可以告诉你系统现在已经不健康了；assurance 则告诉你，谁来 freeze route、谁来 tighten control surface，以及谁负责把系统带回安全状态。

<div class="diagram-card">
<p>保障闭环更像一个连续循环：发现、检测、遏制、修复、学习</p>

``` mermaid
flowchart LR
    A["Red teaming and incidents"] --> B["Findings"]
    B --> C["Detection rules and monitors"]
    C --> D["Response actions"]
    D --> E["Remediation"]
    E --> F["Updated policy, evals, and rollout rules"]
    F --> A
```

</div>

## 7. Remediation 应该改变系统，而不只是增加文档

很常见的一种弱点是：incident 被复盘了，文档也写了，但系统本身几乎没变。

更强的 remediation 通常会真正修改至少一个 operational surface：

- verifier rubric、verifier contract version 或 grading contract；

- policy rules；
- approval thresholds；
- tool exposure；
- memory write constraints；
- eval datasets；
- rollout gates；
- alerting 和 detection rules。

如果 remediation 没有改变这些层，说明系统其实没学到多少东西。

## 8. User reports 和 incidents 必须回流到 assurance loop

另一个很重要的实践点是：assurance loop 不能只依赖团队内部的 exercise。

新的 failure modes 还会来自：

- production traces；
- user complaints；
- approval queue anomalies；
- stale background-run reports；
- capability-session expiry alerts 或 re-init anomalies；
- delegated-authorization mismatch alerts；
- contract-mismatch alerts；
- orchestration-pattern drift alerts；
- postmortems；
- online eval drift；
- red-team findings；
- verifier regressions、verifier contract version changes 或与 human review 的分歧。

这些信号应该重新流回：

- eval datasets；
- safety checks；
- change classification；
- rollout policy。

否则团队会一遍又一遍撞上同样的 surprise。

但这里的第一责任仍然是运行责任，而不是研究责任：一旦某个 signal 足够可信，系统就必须知道谁拥有 response，以及在更深层 redesign 开始之前允许采取哪些 containment moves。

## 9. 好的 assurance loop 一定和 ownership 绑定

没有 ownership，assurance 很快就会散掉。

最好提前明确：

- 谁维护 red-team backlog；
- 谁 triage findings；
- 谁负责 mitigations；
- 谁能 emergency-disable capability；
- 谁判断 remediation 已经足够；
- 谁更新 monitoring 和 response rules。

这一点和本书的组织模型部分完全一致：security discipline 最容易坏在 owner 不清楚的地方。

## 10. 一个 assurance policy 示例

下面这个 skeleton 很实用：

```yaml
assurance:
  red_team:
    cadence: monthly
    required_surfaces:
      - prompt_injection
      - tool_misuse
      - memory_poisoning
      - egress_abuse
      - paused_approval_saturation
      - capability_session_expiry_regression
      - reinit_control_drift
      - delegated_authorization_mismatch
      - orchestration_pattern_regression
      - contract_drift
      - verifier_contract_drift
  findings:
    require_owner: true
    require_severity: true
    require_remediation_due_date: true
    require_verifier_review_for_high_risk: true
  response:
    emergency_actions:
      - disable_capability
      - require_approval
      - restrict_egress
      - disable_memory_write
      - expire_paused_runs
      - suspend_background_route
      - freeze_reinitialization
      - revoke_delegated_authorization
```

它不是 complete framework，但足以说明 assurance 也可以被组织成明确的 operational contract。

如果 release 或 training decisions 依赖 verifier，这个 contract 也应该把 verifier 本身纳入其中。

## 11. 一个 emergency response 决策示例

下面这个代码片段表达的是同一个思路：

```python
from dataclasses import dataclass


@dataclass
class AssuranceSignal:
    unsafe_egress_detected: bool = False
    memory_poisoning_suspected: bool = False
    approval_bypass_detected: bool = False
    paused_approval_saturation: bool = False
    capability_session_expiry_regression: bool = False
    reinit_control_drift: bool = False
    stale_background_runs: bool = False
    contract_drift_detected: bool = False


def emergency_action(signal: AssuranceSignal) -> str:
    if signal.unsafe_egress_detected:
        return "restrict_egress"
    if signal.approval_bypass_detected:
        return "require_approval"
    if signal.capability_session_expiry_regression or signal.reinit_control_drift:
        return "freeze_reinitialization"
    if signal.paused_approval_saturation:
        return "expire_paused_runs"
    if signal.stale_background_runs:
        return "suspend_background_route"
    if signal.contract_drift_detected:
        return "disable_capability"
    if signal.memory_poisoning_suspected:
        return "disable_memory_write"
    return "observe"
```

重点在于：response decision 不应该完全依赖临场 improvisation，而应该属于预先设计好的 operational surface。

## 12. 最常见的断裂点

这些问题会反复出现：

- red teaming 和 engineering backlog 脱节；
- findings 没有 owner；
- incidents 从不进入 eval datasets；
- detection 只看 latency 和 errors；
- paused approval saturation 在 operations 里可见，却没有被当成 assurance signal；
- orchestration-pattern regressions 往往要等 runtime behavior 在 production 里漂移之后才会被发现；
- stale background runs 悄悄累积；
- contract drift 只有在 runtime failures 扩散后才被发现；
- response actions 太粗或太慢；
- remediation 没有真正改变系统。

一旦这样，assurance loop 就会变成一套漂亮的 presentation，而不是防护机制。

## 13. 给 assurance loop 做一次快速成熟度测试

团队不应该只因为做过几次 red-team exercises、记下了几个 findings，就宣称自己已经有 assurance。

更高的标准应该是：

- findings 会变成有 owner 的 engineering objects；
- detection 寻找的是 unsafe behavior，而不只是 errors 和 latency；
- paused approvals、capability-session lifecycle regressions、orchestration-pattern regressions、stale background runs 与 contract drift 都被当成真实 assurance signals；
- response actions 在下一次 incident 之前就已经存在，而不是事后才补；
- remediation 会改变 operating system，而不只是文档痕迹；
- incidents 会回流进 evals、policies 和 rollout rules。

如果这些条件大多不成立，那团队也许已经有一些 security activity，但还没有真正的 assurance loop。

## 14. 实用检查清单

如果你想快速判断 assurance discipline 是否成形，可以问：

- red teaming 是不是定期进行，而不是一次性 exercise？
- findings 是否以 engineering backlog item 的形式被追踪？
- 除了 infra health，是否还有针对 unsafe behavior、paused-approval saturation 和 stale background runs 的 monitors？
- 在不完全 shutdown 的情况下，是否有快速 emergency actions，包括让 paused runs 过期或暂停某条 background route？
- incidents 会不会回流到 evals 和 rollout rules？
- detection、response 和 remediation 的 owner 是否清楚？

如果连续几个问题的答案都是“否”，那你现在可能只有安全意图，还没有 assurance loop。

## 15. 接下来读什么

在 assurance loop 之后，最自然的下一步就是 supply chain discipline 和 approved artifacts。因为只要系统持续变化、持续调查、持续修复，你就必须非常清楚：哪些 artifacts 才算可信，哪些东西真正进入过 production。

## 16. 值得配套阅读的参考页

- [Trace Schema 与 Event Catalog](../../appendix/trace-schema.zh.md)
- [Policy Bundle Schema 与 Approval Contract](../../appendix/policy-bundle-schema.zh.md)
- [Eval Dataset Schema 与 Grading Contract](../../appendix/eval-schema.zh.md)
- [Lifecycle Artifact Schema](../../appendix/lifecycle-artifact-schema.zh.md)

这一章把第 17 章和第 18 章打开的回路真正闭合起来。那两章里 policy、approval 与 runtime-control paths 先被做成显式结构，而在这里，这些同样的路径会变成 detection、containment 和 response surfaces。

- [第 20 章：智能体系统的 Change Management](chapter-20.zh.md)
- [第 14 章：平台团队与产品团队](../part-vi/chapter-14.zh.md)
- [第 18 章：生产上线检查清单](../part-vii/chapter-18.zh.md)
- [参考来源](../../appendix/sources.zh.md)

[^google-assurance]: [Google Research, Security Assurance in the Age of Generative AI](https://research.google/pubs/security-assurance-in-the-age-of-generative-ai/)
