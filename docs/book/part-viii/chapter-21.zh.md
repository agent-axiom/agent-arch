# 第 21 章：Assurance Loop：Red Teaming、Detection 与 Response

## 1. 为什么 lifecycle 不会在 release gates 结束

到这里为止，我们已经有了一幅更成熟的图景：

- agent system 已经生活在 ADLC 里；
- changes 会经过 change management；
- rollout 不再是盲目推进。

但这仍然不够。

因为 agent systems 有一类特别的风险：

- emergent behavior；
- 通过 prompt 或 tool paths 发生的 abuse；
- 长流程中的 drift；
- 隐蔽的 policy bypass；
- unsafe side effects；
- 团队发现得太晚的退化。

所以在 release discipline 之后，必须再出现一个层：assurance loop。

## 2. 什么是 assurance loop

我会这样定义 assurance loop：

它是一个持续的 operational 循环，帮助团队不只是发布变更，还能系统性地发现薄弱点、察觉新威胁、调查问题并把问题真正关掉。

在 agent systems 里，它通常包括：

- red teaming；
- vulnerability management；
- detection and response；
- remediation；
- 把经验重新写回 design 和 rollout。

Google Research 在这里给出的核心观点非常清楚：生成式系统的 security assurance 应该是一种持续能力，而不是一次性的 review activity。[^google-assurance]

## 3. Red teaming 应该针对真实 failure modes，而不是演示效果

太多团队把 red teaming 做成了展示：

- 试几个 obvious jailbreak prompts；
- 展示系统“扛住了一些东西”；
- 然后就觉得问题结束了。

这不是强 assurance。

对 agent systems 有价值的 red teaming，应该针对 production-relevant failure modes：

- prompt injection；
- hidden instruction override；
- tool misuse；
- unsafe egress；
- approval bypass；
- cross-tenant retrieval leakage；
- memory poisoning；
- excessive autonomy。

好的 red teaming 不只是看模型回答，还要看整个 execution path。

## 4. 漏洞应该进入 backlog，而不是停留在感受里

如果 red teaming 只留下“这里感觉有点危险”的印象，团队很难高质量行动。

更成熟的方式是把它放进正常的 vulnerability workflow：

- 到底发现了什么；
- 风险等级是什么；
- exploit path 是什么；
- 什么算 fix；
- owner 是谁；
- remediation 截止时间是什么；
- 是否需要临时 mitigation。

这是一个很典型的 SDLC-like 逻辑：findings 必须成为可管理的工程对象，而不是 workshop 后的印象笔记。

## 5. Detection 不能只盯着 error rate

在普通服务里，detection 常常围绕 error rate、latency 和基础设施信号展开。对 agent systems 来说，这远远不够。

你还需要能看到：

- denied actions 的异常增长；
- approval backlog 的堆积；
- 异常的 tool selection patterns；
- 新出现的 egress destinations；
- memory write anomalies；
- unsafe fallback behavior 的上升；
- task success 和 safety metrics 的 drift。

也就是说，这里的 detection 既是 observability，也是 abuse and safety monitoring。

## 6. Response 应该是一层独立的运营能力

当一个 agent 开始表现出危险行为时，光说“之后再调 prompt”是不够的。

更实用的 response layer 应该围绕具体动作来设计：

- 限制 capability；
- 把 action 切到 approval-only mode；
- 收紧 egress policy；
- 关闭 risky memory writes；
- 把 rollout wave 切回更安全的 profile；
- 必要时直接 disable 有问题的 route。

这很关键，因为在 agent systems 里，response 往往必须比完整的 root-cause analysis 更快发生。

<div class="diagram-card">
<p>Assurance loop 更像一个连续循环：发现、检测、遏制、修复、学习</p>

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
- postmortems；
- online eval drift；
- red-team findings。

这些信号应该重新流回：

- eval datasets；
- safety checks；
- change classification；
- rollout policy。

否则团队会一遍又一遍撞上同样的 surprise。

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
  findings:
    require_owner: true
    require_severity: true
    require_remediation_due_date: true
  response:
    emergency_actions:
      - disable_capability
      - require_approval
      - restrict_egress
      - disable_memory_write
```

它不是 complete framework，但足以说明 assurance 也可以被组织成明确的 operational contract。

## 11. 一个 emergency response 决策示例

下面这个代码片段表达的是同一个思路：

```python
from dataclasses import dataclass


@dataclass
class AssuranceSignal:
    unsafe_egress_detected: bool = False
    memory_poisoning_suspected: bool = False
    approval_bypass_detected: bool = False


def emergency_action(signal: AssuranceSignal) -> str:
    if signal.unsafe_egress_detected:
        return "restrict_egress"
    if signal.approval_bypass_detected:
        return "require_approval"
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
- response actions 太粗或太慢；
- remediation 没有真正改变系统。

一旦这样，assurance loop 就会变成一套漂亮的 presentation，而不是防护机制。

## 13. 实用检查清单

如果你想快速判断 assurance discipline 是否成形，可以问：

- red teaming 是不是定期进行，而不是一次性 exercise？
- findings 是否以 engineering backlog item 的形式被追踪？
- 除了 infra health，是否还有针对 unsafe behavior 的 monitors？
- 在不完全 shutdown 的情况下，是否有快速 emergency actions？
- incidents 会不会回流到 evals 和 rollout rules？
- detection、response 和 remediation 的 owner 是否清楚？

如果连续几个问题的答案都是“否”，那你现在可能只有安全意图，还没有 assurance loop。

## 14. 接下来读什么

在 assurance loop 之后，最自然的下一步就是 supply chain discipline 和 approved artifacts。因为只要系统持续变化、持续调查、持续修复，你就必须非常清楚：哪些 artifacts 才算可信，哪些东西真正进入过 production。

## 15. 值得配套阅读的参考页

- [Trace Schema 与 Event Catalog](../../appendix/trace-schema.zh.md)
- [Eval Dataset Schema 与 Grading Contract](../../appendix/eval-schema.zh.md)
- [Lifecycle Artifact Schema](../../appendix/lifecycle-artifact-schema.zh.md)

- [第 20 章：智能体系统的 Change Management](chapter-20.zh.md)
- [第 14 章：平台团队与产品团队](../part-vi/chapter-14.zh.md)
- [第 18 章：生产上线检查清单](../part-vii/chapter-18.zh.md)
- [参考来源](../../appendix/sources.zh.md)

[^google-assurance]: [Google Research, Security Assurance in the Age of Generative AI](https://research.google/pubs/security-assurance-in-the-age-of-generative-ai/)
