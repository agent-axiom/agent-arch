# 第 22 章：供应链、来源追踪与已批准工件

!!! info "时效说明"
    最近一次编辑审查：**2026 年 5 月 14 日**。下一次计划审查：**2026 年 6 月 14 日**。

    自上次审查以来的变化：MCP/A2A 安全面、验证器契约、治理感知遥测以及出版就绪问题，已经被明确列为近期编辑任务。

    变化最快的部分：

    - 面向模型与配置的证明、签名和来源追踪工具；
    - 围绕工件治理和托管供应链控制的厂商能力；
    - 将提示、策略和评测工件当作可评审单元的实践。

    变化相对较慢的部分：

    - 每个已批准工件都需要负责人、来源追踪和审查状态；
    - 应该建立多条信任链，而不是只依赖一条总链；
    - 供应链纪律必须与事故复盘、变更管理和 rollout 连接起来。

## 1. 为什么智能体系统的供应链比普通服务更宽

当工程师听到“软件供应链”时，通常会想到一些熟悉的东西：

- 包依赖；
- 容器；
- CI/CD 工件；
- 构建产物的签名和来源证明。

但对智能体系统来说，这还不够。

问题在于，这里的生产行为不只依赖代码。它还依赖：

- 模型工件；
- 提示和例程包；
- 策略配置；
- 检索语料；
- 能力契约；
- 评测数据集；
- 验证器契约、评分规则与证据链接规则；
- 审批规则与模式；
- 运行时控制模式；
- 编排模式治理规则与 worker-safe 目录定义；
- 能力会话中断与重新初始化规则；
- 发布工件包。

也就是说，智能体的供应链更宽，是因为系统本身就更宽。

## 2. 什么是智能体系统里的已批准工件

这里最好先给出一个很直白的定义：

已批准工件就是任何一个被允许进入生产环境的工件，因为它拥有负责人、来源证明、审查状态、清晰的运行角色，以及在发布身份中的明确位置。

这意味着已批准工件不只是镜像或 wheel 文件。它们还是后续发布决策、保障判断或事故复盘必须能够准确追溯到的治理对象。

在智能体平台里，它们往往包括：

- 已批准的模型路由；
- 已批准的提示包；
- 已批准的[策略包（policy bundle）](../../appendix/policy-bundle-schema.zh.md)；
- 已批准的能力契约；
- 已批准的[审批模式（approval schema）](../../appendix/approval-schema.zh.md)；
- 已批准的运行时控制模式；
- 已批准的检索来源；
- 已批准的评测集；
- 已批准的发布模板。

如果团队没有这个概念，就很容易落入一种隐式信任：“这个工件应该没问题，因为之前有人用过。”

## 3. 来源证明是为了回答非常实际的问题

Google Research 的一个关键观点是：AI 系统的来源证明不只是正式安全概念，它也是运行上的必需品。[^google-supply-chain]

你必须能快速回答：

- 这个模型从哪里来；
- 现在激活的是哪一个提示包；
- 事故发生时生效的是哪一个[策略包（policy bundle）](../../appendix/policy-bundle-schema.zh.md)；
- 当时使用的是哪一版检索语料；
- 发布是被哪一个评测集验证的；
- 当时生效的是哪一版验证器契约、评分规则与证据链接规则；
- 当时生效的是哪个契约版本与[审批模式（approval schema）](../../appendix/approval-schema.zh.md)；
- 当时是哪一条中断或过期策略在治理这次运行；
- 当时是哪一种编排模式与 worker 边界策略在治理这次运行；
- 当时是哪种委派授权模式、principal 绑定与撤销策略在治理这次运行；
- 这个变更是谁批准的。

!!! example "贯穿案例：重复工单修复的 provenance"
    在重复工单事故之后，后续复盘需要能重建的不只是重试补丁对应的 commit。它还需要知道金丝雀期间生效的 [eval dataset](../../appendix/eval-schema.zh.md) 版本、`side_effect_unknown` 策略包、`create_support_ticket` 能力契约、rollout gate、审批模式和 [trace schema](../../appendix/trace-schema.zh.md)。如果其中任何一个工件只是“在聊天里某处”，而不是已批准发布包的一部分，团队就无法证明再次出现的重复工单到底发生在修复后的控制之下，还是旧规则集之下。

**Supply-chain case-spine note：**approved artifact bundle 应该为三个 canonical cases 保留 provenance。Support triage 需要 write path 的 [eval dataset](../../appendix/eval-schema.zh.md)、[policy bundle](../../appendix/policy-bundle-schema.zh.md)、capability contract、[approval schema](../../appendix/approval-schema.zh.md)、[trace schema](../../appendix/trace-schema.zh.md) 和 [rollout gate](../../appendix/change-rollout-schema.zh.md) 版本。Internal knowledge assistant 需要 approved retrieval corpus、source-grounding rubric、tenant-filter config、memory-write policy 和 freshness attestation。Incident coordination 需要 escalation-policy bundle、notification contract、responder-role map、incident-state schema 和 post-incident artifact update。

如果这些问题无法快速回答，变更管理和事故复盘很快就会失控。

这也是为什么本章里的来源追踪应该被狭义而具体地理解。它不是整个证据层。它是围绕已批准工件、发布身份与承载决策版本的受治理血缘层。

同样的规则也适用于失败运行。即使能力因为超时失败、审批路径以验证失败结束，或者上游依赖直接崩掉，后续复盘仍然需要知道，当时究竟是哪一组已批准工件与哪一个发布身份在支配这次失败，是哪一个导出字段，例如 `failure_reason`，保留了具体的失败条件，它是否还通过 `latest_failure_reason` 这样的面向操作员摘要字段保持可见，以及这次运行在会话评审中是否仍然计入 `traceable_failed_runs`。否则，组织就只会为顺畅路径保留来源追踪，而把退化行为当成无人负责的残留物。

这也正是本章的核心承诺。它要帮助读者看见证据怎样从一般性的遥测变成受治理的主干：这一层保存着后续事故复盘或治理决策究竟建立在哪一组已评审工件、哪一个可信契约版本，以及哪一个已批准发布身份之上。本章的主要工件是 approved artifact bundle：一组已评审的版本、契约和模式，而不是泛泛的 evidence 文件夹。

如果你想看一页专门展示这个受治理主干如何继续连回请求、策略、审批、追踪、评测、事故和 rollout 判断，可以直接打开 [Evidence Spine](../part-v/evidence-spine.zh.md)。

!!! info "需要供应链工件？"
    如果你需要契约层视角，可以直接查看 [生命周期工件规范](../../appendix/lifecycle-artifact-schema.zh.md)、[策略包模式与审批契约](../../appendix/policy-bundle-schema.zh.md) 和 [变更评审与发布门禁模式](../../appendix/change-rollout-schema.zh.md)。

## 4. 智能体需要多条信任链，而不是一条

在普通系统里，团队通常只想一条信任链： “代码在 CI 里构建过，容器也签名了，所以没问题。”

对智能体系统来说，更好的思路是维护多条相互连接的信任链：

- 代码与构建链；
- 模型链；
- 提示与例程链；
- 策略链；
- 能力链；
- 审批与运行时控制链；
- 能力会话治理链；
- 委派授权链；
- 数据与检索链；
- 评测链。

<div class="diagram-card">
<p>与其只想一条供应链，不如把它看成几条相互关联的信任链</p>

``` mermaid
flowchart LR
    A["代码与构建"] --> G["已批准发布包"]
    B["模型工件"] --> G
    C["提示与例程包"] --> G
    D["策略包"] --> G
    E["能力契约"] --> G
    F["审批与运行时控制模式"] --> G
    H["评测数据集与报告"] --> G
```

</div>

## 5. 已批准清单和已批准工件不是一回事

这两个概念很接近，但并不相同。

`已批准清单` 回答的是：

- 平台上哪些运行时、网关、能力和模式本身就是允许的。

`已批准工件` 回答的是：

- 当前到底有哪些具体版本和工件包被批准运行。

例如：

- 能力 `create_ticket` 可以属于已批准清单；
- 但 `policy_bundle_v12` 或 `prompt_bundle_support_v7` 是已批准工件。

这个区别很重要，因为清单提供平台级框架，而已批准工件提供发布级纪律。

而这里来源追踪的核心，正是这种发布级纪律。问题不只是系统有没有遥测，而是系统当时究竟运行在什么受治理版本、已批准包、已评审模式或带有验证器约束的契约族之下。

## 6. 没有来源追踪的提示包，本质上就是一个供应链缺口

团队很容易把提示变更当成“活的文本”，而不是发布工件。

但如果你不知道：

- 谁改了提示；
- 现在生产环境里是哪一个版本；
- 哪些评测覆盖了它；
- 它在哪个 rollout 波次上生效；

那这个提示包在运营上并不比来源不明的构建工件更可靠。

同样的逻辑也适用于：

- 例程；
- 策略 YAML；
- 检索配置；
- 审批阈值；
- 用来定义暂停/后台行为的运行时控制模式。

## 7. 评测数据集也应该被当成可信工件

很多团队容易把评测数据集看得太轻： “这不就是一组例子吗？”

其实它是一个关键的治理工件。

如果它：

- 来源不清晰；
- 没有版本；
- 没有负责人；
- 在不同发布之间悄悄变化；

那团队就会在摇晃的基础上做发布决策。

所以成熟的 ADLC 应该把评测数据集纳入已批准工件模型。

对验证器契约也越来越应该如此。如果发布或保障依赖过程分数、结果分数、失败归因或链接证据，那么验证器层就不再只是非正式的辅助逻辑，而是一个需要治理的生产工件。

这很重要，因为验证器契约不只是给质量打分。它还在定义系统会把什么算作可接受证据、能够精确命名哪些失败，以及哪些发布声明在事后可以被辩护。一旦验证器契约会影响发布判断、事故归因或保障状态，它的血缘就进入了证据主干，而不再只是一个可有可无的评测细节。

## 8. 能力契约和出口规则也属于供应链

在智能体系统里，工具契约不只是文档，它本身就是可信运营表面的一一部分。

对于一个能力，团队最好明确知道：

- 谁是负责人；
- 风险等级是什么；
- 使用哪个工具 principal；
- 网络访问配置是什么；
- 允许哪些出口目标；
- 采用什么审批语义。

如果这些契约被悄悄改动，没有来源追踪，也没有审查轨迹，那么这种变更可能和未审查代码发布一样危险。

审批与运行时控制模式也是一样。如果团队在没有受治理工件纪律的情况下修改超时、暂停/恢复行为、过期语义、重新初始化规则或预期载荷结构，那么即使模型和源码都没动，生产行为也已经变了。

这也意味着来源追踪不应只记录“存在某个运行时控制模式”，还应该逐步记录当时生效的是哪一个中断治理版本：

- 暂停运行是会过期，还是可以无限等待；
- 能力会话重新初始化是 allowed、denied，还是 approval-bound；
- 遥测是否应该把原始能力会话和重新初始化后的能力会话关联起来；
- 当时这条路径批准的是哪一种编排模式，以及 worker-safe 目录边界是否生效；
- 审批与会话控制逻辑当时是受同一个契约版本治理，还是已经发生漂移；
- 委派访问是平台拥有还是用户委派；
- 哪一条 principal 绑定规则与撤销行为在治理进行中或暂停动作。

Anthropic 后续关于 harness 设计的工作又补上了另一层供应链含义。[^anthropic-harness] 如果长时间运行的工作依赖上下文重置、planner/generator/evaluator 的角色分离、sprint 契约与结构化交接工件，那么这些交接工件就不能再被视为一次性的协调便条。它们本身也变成了承载来源追踪的工件。之后的事故评审或 rollout 争议，可能都需要知道是哪一份交接工件传递了 scope、哪一条 evaluator critique 改变了下一轮 sprint，以及是在什么重置边界上，活动上下文发生了变化，而用户可见运行却没有改变。

这些之所以是来源追踪问题，正是因为它们定义的是行为的受治理身份，而不只是说明这些行为有没有在遥测里被看见。

这也正是本章边界重要的地方。遥测也许能告诉你暂停、重新初始化或委派动作确实发生过，但来源追踪必须保留下来，说明究竟是哪一组经过评审的契约族让这些行为在当时被平台视为正当。没有这一层，事故复盘即使看见了事件，也依然解释不了平台为什么认为这些行为有效。

## 9. 一个已批准工件策略示例

下面这个骨架很实用：

```yaml
artifacts:
  require_owner: true
  require_version: true
  require_provenance: true
  require_review_status: true
  types:
    - model_route
    - prompt_bundle
    - policy_bundle
    - capability_contract
    - approval_schema
    - runtime_control_schema
    - capability_session_contract
    - verifier_contract
    - eval_dataset
    - retrieval_source
```

它帮助团队把讨论从“看起来像个正常配置”切换成“这是一个真正的生产工件”。

## 10. 一个已批准清单策略示例

下面是更偏平台级的例子：

```yaml
inventory:
  approved_runtimes:
    - agent_runtime_v3
  approved_gateways:
    - shared_tool_gateway
    - approval_gateway
  approved_patterns:
    - staged_rollout
    - approval_required_for_high_risk
    - governed_background_mode
    - reviewed_routing
    - bounded_parallelization
    - worker_safe_orchestrator_workers
  deprecated_patterns:
    - direct_prod_tool_access
    - unversioned_prompt_override
```

这个清单的价值不在于“看起来整齐”，而在于它为平台提供了一张清晰的可信/不可信运营模式地图。

## 11. 一个工件就绪检查示例

下面这个代码片段表达的是核心思路：

```python
from dataclasses import dataclass


@dataclass
class ArtifactRecord:
    has_owner: bool
    has_version: bool
    has_provenance: bool
    review_passed: bool
    schema_linked: bool


def artifact_ready(record: ArtifactRecord) -> bool:
    return (
        record.has_owner
        and record.has_version
        and record.has_provenance
        and record.review_passed
        and record.schema_linked
    )
```

重点很简单：可信工件应该由明确属性定义，而不是靠直觉判断。如果平台无法显式检查工件是否就绪，最后就一定会退回到社会性信任、陈旧默认值和脆弱的发布身份上。

## 12. 工件纪律最容易坏在哪里

常见的问题通常是这些：

- 提示包没有版本；
- 评测数据集悄悄变化；
- 能力契约被编辑却没有审查轨迹；
- 审批或运行时控制模式发生变化，却没有版本纪律；
- 编排模式治理变更没有工件血缘；
- 没有人知道事故发生时到底是哪一个精确工件在运行；
- 事故证据中缺少契约版本链接；
- 发布或保障 evidence 中缺少验证器契约血缘；
- 已废弃模式在生产环境里活得太久；
- 已批准清单只存在于 wiki，而不存在于运营工具。

一旦出现这些问题，平台失去可控性往往不是因为一次大事故，而是因为几百个小工件都处于未跟踪状态。

## 13. 给工件治理做一次快速成熟度测试

团队不应该只因为构建已签名、几份配置也放进了版本控制，就觉得自己已经有供应链纪律。

更高的标准应该是：

- 提示、策略、评测、能力、审批、runtime-control 和 verifier 工件都被当成生产工件；
- 来源追踪能在事故评审和 rollout 决策中被快速恢复；
- 发布和保障证据能回溯到当时生效的验证器契约与契约族；
- 已批准清单和已批准工件被当成不同的控制层来管理；
- 已废弃模式能在它们悄悄留在生产环境之前被阻断；
- 信任绑定在显式工件属性上，而不是靠社会性继承。

如果这些条件大多不成立，那团队也许已经有一些工件卫生，但还没有真正的工件治理。

## 14. 实用检查清单

如果你想快速检查工件纪律，可以问：

- 所有生产工件都有 owner 吗？
- 模型、提示、策略、approval-schema、runtime-control、评测和验证器工件都有版本吗？
- 事故评审时能快速恢复来源追踪、验证器血缘与生效中的契约/模式版本吗？
- 平台是否有已批准清单？
- 你们能区分平台批准的模式和发布批准的工件吗？
- 已废弃工件能被快速阻断吗？

如果连续几个问题的答案都是“否”，那你们还没有真正的工件治理层。

## 15. 接下来读什么

在供应链和工件纪律之后，这一部分最后一个自然主题就是退役、替换和生命周期终止纪律。成熟的系统不仅要能上线和修复，也要能优雅地下线。

## 16. 值得配套阅读的参考页

- [Policy Bundle Schema 与 Approval Contract](../../appendix/policy-bundle-schema.zh.md)
- [Lifecycle Artifact Schema](../../appendix/lifecycle-artifact-schema.zh.md)
- [参考包](../../appendix/reference-package.zh.md)

- [第 21 章：保障闭环：红队测试、检测与响应](chapter-21.zh.md)
- [第 17 章：策略层与能力目录](../part-vii/chapter-17.zh.md)
- [第 18 章：生产上线检查清单](../part-vii/chapter-18.zh.md)
- [参考来源](../../appendix/sources.zh.md)

[^google-supply-chain]: [Google Research, Securing the AI Software Supply Chain](https://research.google/pubs/securing-the-ai-software-supply-chain/)

[^anthropic-harness]: Anthropic, [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps).
