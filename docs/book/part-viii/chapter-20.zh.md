# 第 20 章：智能体系统的变更管理

!!! info "时效说明"
    本章内容截至 2026 年 4 月 11 日。

    变化最快的部分：

    - 智能体系统的托管发布控制、审批流与分阶段 rollout 能力；
    - 不同平台如何界定承载发布意义的表面；
    - 围绕策略包、路由变更和托管更新的厂商接口。

    变化相对较慢的部分：

    - 基于风险的变更分类方法；
    - 必须把提示、策略、检索和能力变更当成真正的发布；
    - 变更评审必须与评测、审批和 rollout 门禁连接起来。

## 1. 为什么智能体系统需要单独的变更纪律

当团队已经承认自己不再只是活在 SDLC，而是已经进入 ADLC 之后，下一个非常实际的问题就是：到底什么算变更，以及这些变更应该如何治理？

在普通服务里，答案通常比较简单：

- 代码变了；
- 基础设施变了；
- 数据模式变了；
- 发布了一个版本。

对智能体系统来说，这已经不够。发布承载表面更宽，风险也不只来自代码。

所以变更管理在这里会变成一个独立的运行职能，而不是“有人往 main 推了一点东西”。

这也正是本章的核心承诺。它要帮助读者看见：承载发布意义的判断是如何变成一套运行纪律的，不是停留在抽象的风险提醒里，而是落实为一套可重复的方法，用来给变更分类、为不同变更匹配证据，并决定什么值得进入正式门禁。

如果你想看一页专门说明请求、策略、审批、追踪、评测、事故和 rollout 判断如何被维持在同一条链上，可以直接打开 [Evidence Spine](../part-v/evidence-spine.zh.md)。

!!! info "需要变更工件？"
    如果你需要更落地的工程层，可以打开 [Change Review 与 Rollout Gate Schema](../../appendix/change-rollout-schema.zh.md)、[Lifecycle Artifact Schema](../../appendix/lifecycle-artifact-schema.zh.md) 和 [Eval Dataset Schema 与 Grading Contract](../../appendix/eval-schema.zh.md)。

## 2. 在智能体系统里，什么都算变更

最好提前把所有真正会改变系统行为的表面都当成变更，而不只是代码：

- 模型选择或路由；
- 系统提示、例程和指令；
- 策略包；
- 能力契约；
- 审批规则；
- 委派授权规则与 token 处理假设；
- 检索语料；
- 记忆写入语义；
- 编排模式选择与 worker 委派边界；
- 能力会话中断与过期语义；
- 评测数据集与分级逻辑；
- 验证器评分规则、证据链接假设与失败归因规则；
- 发布参数。

如果这些东西被当成“小调优”直接发出去，团队几乎一定会失去对系统行为的控制。

## 3. 不是所有变更都一样危险

这里非常适合引入一个简单的变更分类。

例如：

- `low-risk`：措辞微调、无害的检索调优、内部可观测性变更；
- `medium-risk`：提示重构、排序变更、模型路由更新；
- `high-risk`：新增写入能力、策略放宽、记忆写入扩张、出口变更、自主性扩张，以及受审批约束的有状态能力的中断 / 重新初始化行为变更。

这不是完美分类，但它至少能帮助团队不再用同一种语气讨论所有变更。

<div class="diagram-card">
<p>好的变更管理，第一步往往是先把变更分类说清楚</p>

``` mermaid
flowchart LR
    A["提出变更"] --> B["变更分类"]
    B --> C["低风险"]
    B --> D["中风险"]
    B --> E["高风险"]
    C --> F["轻量验证"]
    D --> G["评测 + 评审"]
    E --> H["正式门禁 + 审批 + 分阶段 rollout"]
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
- 委派授权变更 -> principal 绑定检查、scope 可见性检查、暂停期间撤销行为，以及追踪与审批记录的连续性；
- 中断治理变更 -> 暂停运行过期检查、重新初始化行为检查、遥测链接检查、审批恢复不变量；
- 验证器变更 -> 假阳性检查、假阴性检查、证据链接检查、过程/结果评分一致性、失败归因评审，以及导出的失败运行字段可见性，例如 `failure_reason`；
- 编排模式变更 -> 路由类别覆盖、join-state 检查、worker 边界检查、评审点检查，以及特定模式的追踪连续性；
- 模型路由变更 -> 质量、延迟、安全、成本差值。

这是一条很重要的实践原则：评测策略应该跟变更类别绑定，而不是拿一套通用检查去覆盖所有变更。

## 7. 高风险变更应该经过正式门禁

当一个变更会影响自主性、副作用、记忆写入或出口边界时，只靠人工“看起来没问题”已经不够了。

这类变更最好通过正式门禁：

- 设计评审；
- 显式策略评审；
- 离线评测通过；
- 受影响路径的失败运行演练覆盖；
- 明确确认失败运行仍然能通过发布身份、追踪链接、会话级证据、导出字段（例如 `failure_reason`）、像 `latest_failure_reason` 这样的面向操作员的摘要，以及会话评审 中的 `traceable_failed_runs` 保持可追踪；
- 受限 rollout；
- 第一波监控；
- 清晰回滚路径。

而如果变更影响的是受审批约束或有状态能力流程，门禁通常还应该明确追问一个问题：

> 我们是否改变了中断行为、过期处理或重新初始化语义，从而在不改变用户可见功能集 的情况下，实质性改变了运行时控制？

这一类变化特别容易被低估，因为产品表面看起来没变，但运营风险画像 已经发生了实质漂移。

当发布证据依赖验证器输出时，也应保持同样的警惕。如果验证器评分规则、过程/结果评分或证据链接 发生变化，团队也应把它视为承载发布意义的控制变更，而不是隐藏在评测管线里的小改动。

运行时在不改变表面功能描述的情况下改变编排模式 时也是一样。把某条路径从固定工作流改成 `routing`、加入 `parallelization`，或者引入 `orchestrator-workers`，都可能实质性改变检查点行为、审批顺序、委派 worker 暴露面和失败恢复。这些也应该被当成承载发布意义的运行时控制变更。

OpenAI 和 Microsoft 虽然表述不同，但都指向同一个运营结论：智能体系统应该通过可度量的就绪性、分阶段采用和托管运营来增强，而不是靠希望驱动的发布。[^openai-guide][^microsoft-maturity]

## 8. 回滚比看起来更难

在普通系统里，回滚往往被理解成“回到上一个部署”。但在智能体系统里，这通常过于粗糙。

你往往需要能分别回滚：

- 提示或例程包；
- 策略包；
- 模型路由；
- 检索语料版本；
- 能力暴露；
- 审批阈值；
- 受审批约束的能力会话的中断与过期语义；
- 编排模式选择、worker-safe 目录暴露与委派 worker 评审边界。

如果这些东西都被塞进一个不可分的部署工件，回滚就会太粗暴，也太慢。

## 9. 变更管理必须考虑影响半径

好的流程几乎都会问一句：“如果这次变更错了，最大伤害会有多大？”

有用的影响半径控制手段包括：

- 影子模式；
- 金丝雀租户；
- 能力子集；
- 先只读；
- 先要求审批；
- 分阶段启用记忆写入。

这对智能体特别重要，因为副作用和策略回归往往不会马上显形。

## 10. 来源证明不只是供应链话题

Google Research 很清楚地表明，来源证明不只是安全概念，它也是运营概念。[^google-supply-chain]

对变更管理来说，这意味着你必须能回答：

- 到底是哪一个提示包进了生产环境；
- 当时启用的是哪一个策略配置；
- 用的是哪一版评测集；
- 哪条模型路由在生效；
- 当时启用的是哪一版验证器契约与证据链接规则；
- 谁批准了这个变更。

如果回答不了这些问题，变更评审和事故调查很快就会退化成“靠记忆回溯”。

而这些来源证明信息也越来越应该包含运行时控制细节：

- 当时生效的是哪条暂停/恢复策略；
- 暂停运行受哪条过期规则管理；
- 重新初始化是 allowed、denied 还是 approval-bound；
- 当时生效的是哪种委派授权模式、principal 绑定规则和撤销行为；
- 事故发生时生效的是哪一个能力会话契约版本。

## 11. 一个变更策略示例

下面这个骨架很实用：

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

关键不在于字段本身，而在于变更流程变成了机器可读、可讨论、可审计的对象。

## 12. 一个简单的变更分类器

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

它故意很简单，但方向是对的：先把推理形式化，再自动化门禁。

## 13. 最容易坏掉的地方

这些问题会一遍又一遍出现：

- 提示变更不被当成正式发布；
- 策略变更没有评测就直接上线；
- 编排模式变更被当成“实现细节”放过去；
- 新工具暴露被当成“技术小改动”；
- 回滚只停留在口头上；
- 没有人做影响分析；
- 对低风险和高风险变更强行套同一个流程。

如果这样做，团队要么活在混乱里，要么把自己压进过重的流程里。

## 14. 给变更纪律做一次快速成熟度测试

团队不应该只因为变更会经过评审并跑过 CI，就把发布流程称为成熟。

更高的标准应该是：

- 提示、策略、检索和能力变更都被当成真正的发布；
- 变更风险是被显式分类的，而不是靠感觉猜；
- 评测和门禁是按变更类型匹配的；
- 影响半径在 rollout 前就被限制，而不是事后再解释；
- 回滚能在真正承载风险的层面上工作。

如果这些条件大多不成立，那团队也许已经有交付机制，但还没有真正适用于智能体系统的变更纪律。

## 15. 实用检查清单

如果你想快速判断自己的变更流程是否成熟，可以问：

- 你们是否把提示、策略和检索变更当成真正的发布？
- 是否有基于风险的变更分类法？
- 评测是否和具体变更类型绑定？
- 自主性、出口和写入能力是否有正式门禁？
- 提示、策略和模型路由能否独立回滚？
- 每次 rollout 的影响半径是否清楚？

如果连续几个问题的答案都是“否”，那你们现在还没有变更管理，只有惯性下的变更交付。

## 16. 接下来读什么

在变更管理之后，最自然的下一步就是保证回路：红队测试、漏洞管理、检测与响应。到那一步，生命周期就不再只是发布纪律，而会真正变成持续运营的保护机制。

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
