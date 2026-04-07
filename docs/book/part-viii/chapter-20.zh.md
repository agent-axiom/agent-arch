# 第 20 章：智能体系统的 Change Management

## 1. 为什么智能体系统需要单独的 change discipline

当团队已经承认自己不再只是活在 SDLC，而是已经进入 ADLC 之后，下一个非常实际的问题就是：到底什么算变更，以及这些变更应该如何治理？

在普通服务里，答案通常比较简单：

- 代码变了；
- 基础设施变了；
- 数据模式变了；
- 发布了一个版本。

对智能体系统来说，这已经不够。release-bearing surface 更宽，风险也不只来自代码。

所以 change management 在这里会变成一个独立的 operational function，而不是“有人往 main 推了一点东西”。

## 2. 在智能体系统里，什么都算 change

最好提前把所有真正会改变系统行为的表面都当成 change，而不只是代码：

- model selection 或 routing；
- system prompts、routines 和 instructions；
- policy bundles；
- capability contracts；
- approval rules；
- retrieval corpora；
- memory write semantics；
- eval datasets 与 grading logic；
- rollout parameters。

如果这些东西被当成“小调优”直接发出去，团队几乎一定会失去对系统行为的控制。

## 3. 不是所有 change 都一样危险

这里非常适合引入一个简单的 change taxonomy。

例如：

- `low-risk`：措辞微调、无害的 retrieval tuning、内部 observability changes；
- `medium-risk`：prompt restructuring、ranking changes、model routing updates；
- `high-risk`：new write-capabilities、policy relaxations、memory write expansion、egress changes、autonomy expansion。

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

## 4. 最常见的错误：把 prompt change 当成“不算正式发布”

智能体团队里最常见的一句话是：“我们又没改代码，只是调了一下 system prompt。”

这是一种危险的逻辑。

一个 prompt、routine 或 instruction change 可能会：

- 改变 tool selection；
- 改变 agent 的 risk appetite；
- 增加 cost；
- 打乱 escalation discipline；
- 偏离原有的 policy intent；
- 在关键场景上降低 performance。

所以在 production-grade 系统里，prompt change 通常也应该被纳入 release discipline。

## 5. 最小 change packet 应该是可评审的

有意义的 change，最好都能被整理成一个小而完整的 reviewable packet：

- 改了什么；
- 为什么改；
- 这是什么 risk class；
- 哪些 evals 能覆盖它；
- 有哪些 rollback hooks；
- rollout 的 blast radius 是什么。

如果一个变更只以“我稍微优化了一下行为”的形式出现，团队几乎不可能做出高质量评审。

## 6. Evals 应该和 change type 绑定

不是所有 change 都需要同一套验证方式。

更实用的逻辑通常是：

- prompt 或 routine changes -> task evals、policy-sensitive scenarios、cost checks；
- policy changes -> deny/allow cases、abuse scenarios、audit coverage；
- retrieval changes -> relevance checks、leakage checks、context budget checks；
- tool changes -> contract tests、idempotency checks、approval path validation；
- model routing changes -> quality、latency、safety、cost deltas。

这是一条很重要的实践原则：eval strategy 应该跟 change class 绑定，而不是拿一套通用检查去覆盖所有变更。

## 7. High-risk changes 应该经过 formal gates

当一个 change 会影响 autonomy、side effects、memory writes 或 egress boundaries 时，只靠人工“看起来没问题”已经不够了。

这类变更最好通过 formal gates：

- design review；
- explicit policy review；
- offline eval pass；
- limited rollout；
- first wave monitoring；
- clear rollback path。

OpenAI 和 Microsoft 虽然表述不同，但都指向同一个 operational 结论：agent systems 应该通过 measurable readiness、staged adoption 和 managed operations 来增强，而不是靠 hope-driven shipping。[^openai-guide][^microsoft-maturity]

## 8. Rollback 比看起来更难

在普通系统里，rollback 往往被理解成“回到上一个 deploy”。但在智能体系统里，这通常过于粗糙。

你往往需要能分别回滚：

- prompt 或 routine bundle；
- policy bundle；
- model route；
- retrieval corpus version；
- capability exposure；
- approval threshold。

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
- 谁批准了这个 change。

如果回答不了这些问题，change review 和 incident investigation 很快就会退化成“靠记忆回溯”。

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
- new tool exposure 被当成“技术小改动”；
- rollback 只停留在口头上；
- 没有人做 impact analysis；
- 对 low-risk 和 high-risk changes 强行套同一个流程。

如果这样做，团队要么活在混乱里，要么把自己压进过重的流程里。

## 14. 实用检查清单

如果你想快速判断自己的 change process 是否成熟，可以问：

- 你们是否把 prompt、policy 和 retrieval changes 当成真正的 releases？
- 是否有基于风险的 change taxonomy？
- evals 是否和具体 change type 绑定？
- autonomy、egress 和 write-capabilities 是否有 formal gate？
- prompt、policy 和 model route 能否独立 rollback？
- 每次 rollout 的 blast radius 是否清楚？

如果连续几个问题的答案都是“否”，那你们现在还没有 change management，只有惯性下的变更交付。

## 15. 接下来读什么

在 change management 之后，最自然的下一步就是 assurance loop：red teaming、vulnerability management、detection and response。到那一步，lifecycle 就不再只是 release discipline，而会真正变成持续运营的保护机制。

## 16. 值得配套阅读的 Reference Pages

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
