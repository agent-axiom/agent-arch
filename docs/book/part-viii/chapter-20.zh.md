# 第 20 章：智能体系统的变更管理

!!! info "时效说明"
    本章内容截至 2026 年 4 月 11 日。

    变化最快的部分：

    - 智能体系统的托管发布控制、审批流与分阶段 rollout 能力；
    - 不同平台如何界定 release-bearing surfaces；
    - 围绕 policy bundles、routing changes 和托管更新的厂商接口。

    变化相对较慢的部分：

    - 基于风险的变更分类方法；
    - 必须把 prompts、policies、retrieval 和 capability changes 当成真正的发布；
    - 变更评审必须与 evals、approvals 和 rollout gates 连接起来。

## 1. 为什么智能体系统需要单独的变更纪律

当团队已经承认自己不再只是活在 SDLC，而是已经进入 ADLC 之后，下一个非常实际的问题就是：到底什么算变更，以及这些变更应该如何治理？

在普通服务里，答案通常比较简单：

- 代码变了；
- 基础设施变了；
- 数据模式变了；
- 发布了一个版本。

对智能体系统来说，这已经不够。发布承载表面更宽，风险也不只来自代码。

所以变更管理在这里会变成一个独立的运行职能，而不是“有人往 main 推了一点东西”。

!!! info "需要 change 工件？"
    如果你需要更落地的工程层，可以打开 [Change Review 与 Rollout Gate Schema](../../appendix/change-rollout-schema.zh.md)、[Lifecycle Artifact Schema](../../appendix/lifecycle-artifact-schema.zh.md) 和 [Eval Dataset Schema 与 Grading Contract](../../appendix/eval-schema.zh.md)。

## 2. 在智能体系统里，什么都算变更

最好提前把所有真正会改变系统行为的表面都当成变更，而不只是代码：

- 模型选择或路由；
- 系统提示、例程和指令；
- 策略包；
- 能力契约；
- 审批规则；
- delegated authorization rules 与 token-handling assumptions；
- 检索语料；
- 记忆写入语义；
- orchestration-pattern selection 与 worker-delegation boundaries；
- capability-session interruption 与 expiry semantics；
- 评测数据集与分级逻辑；
- verifier rubric、evidence linkage assumptions 与 failure attribution rules；
- 发布参数。

如果这些东西被当成“小调优”直接发出去，团队几乎一定会失去对系统行为的控制。

## 3. 不是所有变更都一样危险

这里非常适合引入一个简单的变更分类。

例如：

- `low-risk`：措辞微调、无害的检索调优、内部可观测性变更；
- `medium-risk`：提示重构、排序变更、模型路由更新；
- `high-risk`：新增写入能力、策略放宽、记忆写入扩张、出口变更、自主性扩张，以及 approval-bound stateful capabilities 的 interruption / re-init behavior 变更。

这不是完美分类，但它至少能帮助团队不再用同一种语气讨论所有变更。

<div class="diagram-card">
<p>好的 change management，第一步往往是先把 change 分类说清楚</p>

``` mermaid
flowchart LR
    A["Change proposed"] --> B["Classify change"]
    B --> C["Low risk"]
    B --> D["Medium risk"]
    B --> E["High risk"]
    C --> F["Light validation"]
    D --> G["Eval + review"]
    E --> H["Formal gate + approval + staged rollout"]
```

</div>

## 4. 最常见的错误：把提示变更当成“不算正式发布”

智能体团队里最常见的一句话是：“我们又没改代码，只是调了一下系统提示。”

这是一种危险的逻辑。

一个提示、例程或指令变更可能会：

- 改变工具选择；
- 改变智能体的风险偏好；
- 增加成本；
- 打乱升级纪律；
- 偏离原有的策略意图；
- 在关键场景上降低表现。

所以在生产级系统里，提示变更通常也应该被纳入发布纪律。

## 5. 最小变更包应该是可评审的

有意义的变更，最好都能被整理成一个小而完整的可评审包：

- 改了什么；
- 为什么改；
- 这是什么风险等级；
- 哪些评测能覆盖它；
- 有哪些回滚钩子；
- 发布的影响半径是什么。

如果一个变更只以“我稍微优化了一下行为”的形式出现，团队几乎不可能做出高质量评审。

## 6. 评测应该和变更类型绑定

不是所有变更都需要同一套验证方式。

更实用的逻辑通常是：

- 提示或例程变更 -> 任务评测、策略敏感场景、成本检查；
- 策略变更 -> 拒绝/允许场景、滥用场景、审计覆盖；
- 检索变更 -> 相关性检查、泄漏检查、上下文预算检查；
- 工具变更 -> 契约测试、幂等性检查、审批路径验证；
- delegated authorization changes -> principal-binding checks、scope-visibility checks、revoke-during-pause behavior，以及 traces 与 approval records 的 continuity；
- interruption-governance 变更 -> paused-run expiry checks、re-init behavior checks、telemetry linkage checks、approval-resume invariants；
- verifier changes -> false-positive checks、false-negative checks、evidence-linkage checks、process/outcome grading consistency，以及 failure-attribution review；
- orchestration-pattern changes -> routing-class coverage、join-state checks、worker-boundary checks、review-point checks，以及 pattern-specific trace continuity；
- 模型路由变更 -> 质量、延迟、安全、成本差值。

这是一条很重要的实践原则：评测策略应该跟变更类别绑定，而不是拿一套通用检查去覆盖所有变更。

## 7. High-risk changes 应该经过 formal gates

当一个 change 会影响 autonomy、side effects、memory writes 或 egress boundaries 时，只靠人工“看起来没问题”已经不够了。

这类变更最好通过 formal gates：

- design review；
- explicit policy review；
- offline eval pass；
- limited rollout；
- first wave monitoring；
- clear rollback path。

而如果 change 影响的是 approval-bound 或 stateful capability flows，门禁通常还应该明确追问一个问题：

> 我们是否改变了 interruption behavior、expiry handling 或 re-initialization semantics，从而在不改变 user-visible feature set 的情况下，实质性改变了 runtime control？

这一类变化特别容易被低估，因为产品表面看起来没变，但 operational risk profile 已经发生了实质漂移。

当 release evidence 依赖 verifier outputs 时，也应保持同样的警惕。如果 verifier rubric、process/outcome grading 或 evidence linkage 发生变化，团队也应把它视为 release-bearing control change，而不是隐藏在 eval plumbing 里的小改动。

runtime 在不改变表面功能描述的情况下改变 orchestration pattern 时也是一样。把某条路径从 fixed workflow 改成 `routing`、加入 `parallelization`，或者引入 `orchestrator-workers`，都可能实质性改变 checkpoint behavior、approval ordering、delegated worker exposure 和 failure recovery。这些也应该被当成 release-bearing runtime-control changes。

OpenAI 和 Microsoft 虽然表述不同，但都指向同一个 operational 结论：agent systems 应该通过 measurable readiness、staged adoption 和 managed operations 来增强，而不是靠 hope-driven shipping。[^openai-guide][^microsoft-maturity]

## 8. Rollback 比看起来更难

在普通系统里，rollback 往往被理解成“回到上一个 deploy”。但在智能体系统里，这通常过于粗糙。

你往往需要能分别回滚：

- prompt 或 routine bundle；
- policy bundle；
- model route；
- retrieval corpus version；
- capability exposure；
- approval threshold；
- approval-bound capability sessions 的 interruption 与 expiry semantics；
- orchestration-pattern selection、worker-safe catalog exposure 与 delegated worker review boundaries。

如果这些东西都被塞进一个不可分的 deploy artifact，rollback 就会太粗暴，也太慢。

## 9. Change management 必须考虑 blast radius

好的 process 几乎都会问一句：“如果这次 change 错了，最大伤害会有多大？”

有用的 blast-radius 控制手段包括：

- shadow mode；
- canary tenants；
- subset of capabilities；
- read-only first；
- approval-required first；
- staged memory write enablement。

这对 agents 特别重要，因为 side effects 和 policy regressions 往往不会马上显形。

## 10. Provenance 不只是 supply-chain 话题

Google Research 很清楚地表明，provenance 不只是 security 概念，它也是 operational 概念。[^google-supply-chain]

对 change management 来说，这意味着你必须能回答：

- 到底是哪一个 prompt bundle 进了 production；
- 当时启用的是哪一个 policy config；
- 用的是哪一版 eval set；
- 哪条 model route 在生效；
- 当时启用的是哪一版 verifier contract 与 evidence-linkage rules；
- 谁批准了这个 change。

如果回答不了这些问题，change review 和 incident investigation 很快就会退化成“靠记忆回溯”。

而这些 provenance 信息也越来越应该包含 runtime-control details：

- 当时生效的是哪条 pause/resume policy；
- paused runs 受哪条 expiry rule 管理；
- re-init 是 allowed、denied 还是 approval-bound；
- 当时生效的是哪种 delegated authorization mode、principal-binding rule 和 revoke behavior；
- 事故发生时生效的是哪一个 capability-session contract version。

## 11. 一个 change policy 示例

下面这个 skeleton 很实用：

```yaml
changes:
  low_risk:
    require_code_review: true
    require_offline_eval: false
    rollout_mode: direct
  medium_risk:
    require_code_review: true
    require_offline_eval: true
    rollout_mode: canary
  high_risk:
    require_code_review: true
    require_policy_review: true
    require_offline_eval: true
    require_approval: true
    rollout_mode: staged
```

关键不在于字段本身，而在于 change process 变成了 machine-readable、可讨论、可审计的对象。

## 12. 一个简单的 change classifier

下面这个代码片段展示的是核心思路：

```python
from dataclasses import dataclass


@dataclass
class ChangeRequest:
    touches_prompt: bool = False
    touches_policy: bool = False
    touches_write_capability: bool = False
    touches_egress: bool = False


def classify_change(change: ChangeRequest) -> str:
    if change.touches_write_capability or change.touches_egress:
        return "high_risk"
    if change.touches_policy or change.touches_prompt:
        return "medium_risk"
    return "low_risk"
```

它故意很简单，但方向是对的：先把 reasoning formalize，再自动化 gate。

## 13. 最容易坏掉的地方

这些问题会一遍又一遍出现：

- prompt changes 不被当成正式发布；
- policy changes 没有 evals 就直接上线；
- orchestration-pattern changes 被当成“实现细节”放过去；
- new tool exposure 被当成“技术小改动”；
- rollback 只停留在口头上；
- 没有人做 impact analysis；
- 对 low-risk 和 high-risk changes 强行套同一个流程。

如果这样做，团队要么活在混乱里，要么把自己压进过重的流程里。

## 14. 给 change discipline 做一次快速成熟度测试

团队不应该只因为 changes 会经过 review 并跑过 CI，就把 release process 称为成熟。

更高的标准应该是：

- prompt、policy、retrieval 和 capability changes 都被当成真正的 releases；
- change risk 是被显式分类的，而不是靠感觉猜；
- evals 和 gates 是按变更类型匹配的；
- blast radius 在 rollout 前就被限制，而不是事后再解释；
- rollback 能在真正承载风险的层面上工作。

如果这些条件大多不成立，那团队也许已经有 delivery mechanics，但还没有真正适用于 agent systems 的 change discipline。

## 15. 实用检查清单

如果你想快速判断自己的 change process 是否成熟，可以问：

- 你们是否把 prompt、policy 和 retrieval changes 当成真正的 releases？
- 是否有基于风险的 change taxonomy？
- evals 是否和具体 change type 绑定？
- autonomy、egress 和 write-capabilities 是否有 formal gate？
- prompt、policy 和 model route 能否独立 rollback？
- 每次 rollout 的 blast radius 是否清楚？

如果连续几个问题的答案都是“否”，那你们现在还没有 change management，只有惯性下的变更交付。

## 16. 接下来读什么

在 change management 之后，最自然的下一步就是 assurance loop：red teaming、vulnerability management、detection and response。到那一步，lifecycle 就不再只是 release discipline，而会真正变成持续运营的保护机制。

## 17. 值得配套阅读的参考页

- [Eval Dataset Schema 与 Grading Contract](../../appendix/eval-schema.zh.md)
- [Policy Bundle Schema 与 Approval Contract](../../appendix/policy-bundle-schema.zh.md)
- [Lifecycle Artifact Schema](../../appendix/lifecycle-artifact-schema.zh.md)

- [第 19 章：从 SDLC 到 ADLC](chapter-19.zh.md)
- [第 13 章：离线评测、在线评测与回归门禁](../part-v/chapter-13.zh.md)
- [第 18 章：生产上线检查清单](../part-vii/chapter-18.zh.md)
- [参考来源](../../appendix/sources.zh.md)

[^openai-guide]: [OpenAI, A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
[^microsoft-maturity]: [Microsoft Learn, Agentic AI adoption maturity model](https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/maturity-model-overview)
[^google-supply-chain]: [Google Research, Securing the AI Software Supply Chain](https://research.google/pubs/securing-the-ai-software-supply-chain/)
