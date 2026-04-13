# 第 22 章：供应链、来源追踪与已批准工件

!!! info "时效说明"
    本章内容截至 2026 年 4 月 11 日。

    变化最快的部分：

    - 面向模型与配置的 attestation、signing 和 provenance 工具；
    - 围绕 artifact governance 和托管供应链控制的厂商能力；
    - 将 prompt、policy 和 eval 工件当作可评审单元的实践。

    变化相对较慢的部分：

    - 每个已批准工件都需要 owner、provenance 和 review status；
    - 应该建立多条 trust chains，而不是只依赖一条总链；
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
- 审批规则与 schemas；
- runtime-control schemas；
- 发布工件包。

也就是说，智能体的供应链更宽，是因为系统本身就更宽。

## 2. 什么是智能体系统里的已批准工件

这里最好先给出一个很直白的定义：

已批准工件就是任何一个被允许进入生产环境的工件，因为它拥有负责人、来源证明、审查状态和清晰的运行角色。

这意味着已批准工件不只是镜像或 wheel 文件。

在智能体平台里，它们往往包括：

- 已批准的模型路由；
- 已批准的提示包；
- 已批准的策略包；
- 已批准的能力契约；
- 已批准的 approval schema；
- 已批准的 runtime-control schema；
- 已批准的检索来源；
- 已批准的评测集；
- 已批准的发布模板。

如果团队没有这个概念，就很容易落入一种隐式信任：“这个工件应该没问题，因为之前有人用过。”

## 3. 来源证明是为了回答非常实际的问题

Google Research 的一个关键观点是：AI 系统的来源证明不只是正式安全概念，它也是运行上的必需品。[^google-supply-chain]

你必须能快速回答：

- 这个模型从哪里来；
- 现在激活的是哪一个提示包；
- 事故发生时生效的是哪一个策略配置；
- 当时使用的是哪一版检索语料；
- 发布是被哪一个评测集验证的；
- 当时生效的是哪个 contract version 与 approval schema；
- 这个变更是谁批准的。

如果这些问题无法快速回答，变更管理和事故复盘很快就会失控。

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
- approval 与 runtime-control 链；
- 数据与检索链；
- 评测链。

<div class="diagram-card">
<p>与其只想一条供应链，不如把它看成几条相互关联的信任链</p>

``` mermaid
flowchart LR
    A["Code and build"] --> G["Approved release bundle"]
    B["Model artifacts"] --> G
    C["Prompt and routine bundles"] --> G
    D["Policy bundles"] --> G
    E["Capability contracts"] --> G
    F["Approval and runtime-control schemas"] --> G
    H["Eval datasets and reports"] --> G
```

</div>

## 5. 已批准清单和已批准工件不是一回事

这两个概念很接近，但并不相同。

`approved inventory` 回答的是：

- 平台上哪些运行时、网关、能力和模式本身就是允许的。

`approved artifacts` 回答的是：

- 当前到底有哪些具体版本和工件包被批准运行。

例如：

- capability `create_ticket` 可以属于 approved inventory；
- 但 `policy_bundle_v12` 或 `prompt_bundle_support_v7` 是 approved artifact。

这个区别很重要，因为清单提供平台级框架，而已批准工件提供发布级纪律。

## 6. 没有 provenance 的 prompt bundle，本质上就是一个 supply-chain 缺口

团队很容易把 prompt changes 当成“活的文本”，而不是 release artifact。

但如果你不知道：

- 谁改了 prompt；
- 现在 production 里是哪一个版本；
- 哪些 evals 覆盖了它；
- 它在哪个 rollout wave 上生效；

那这个 prompt bundle 在 operational 上并不比来源不明的 build artifact 更可靠。

同样的逻辑也适用于：

- routines；
- policy YAML；
- retrieval configs；
- approval thresholds；
- 用来定义 paused/background behavior 的 runtime-control schemas。

## 7. Eval 数据集也应该被当成可信工件

很多团队容易把 eval dataset 看得太轻： “这不就是一组例子吗？”

其实它是一个关键的治理工件。

如果它：

- 来源不清晰；
- 没有版本；
- 没有 owner；
- 在不同 release 之间 quietly 变化；

那团队就会在 shaky foundation 上做 release decisions。

所以成熟的 ADLC 应该把 eval datasets 纳入 approved artifact model。

## 8. Capability contracts 和 egress rules 也属于 supply chain

在 agent systems 里，tool contract 不只是文档，它本身就是 trusted operational surface 的一部分。

对于一个 capability，团队最好明确知道：

- 谁是 owner；
- 风险等级是什么；
- 使用哪个 tool principal；
- network access profile 是什么；
- 允许哪些 egress destinations；
- 采用什么 approval semantics。

如果这些 contract 被悄悄改动，没有 provenance，也没有 review trail，那么这种 change 可能和未审查代码发布一样危险。

approval 与 runtime-control schemas 也是一样。如果团队在没有 governed artifact discipline 的情况下修改 timeout、pause/resume behavior、expiry semantics 或预期 payload 结构，那么即使模型和源码都没动，production behavior 也已经变了。

## 9. 一个已批准工件策略示例

下面这个 skeleton 很实用：

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
    - eval_dataset
    - retrieval_source
```

它帮助团队把讨论从“看起来像个正常配置”切换成“这是一个真正的生产工件”。

## 10. 一个 approved inventory policy 示例

下面是更偏 platform-level 的例子：

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
  deprecated_patterns:
    - direct_prod_tool_access
    - unversioned_prompt_override
```

这个 inventory 的价值不在于“看起来整齐”，而在于它为平台提供了一张清晰的 trusted / untrusted operational patterns 地图。

## 11. 一个 artifact readiness check 示例

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

重点很简单：可信工件应该由明确属性定义，而不是靠直觉判断。

## 12. Artifact discipline 最容易坏在哪里

常见的问题通常是这些：

- prompt bundles 没有版本；
- eval datasets quietly 变化；
- capability contracts 被编辑却没有 review trail；
- approval 或 runtime-control schemas 发生变化，却没有 version discipline；
- 没有人知道 incident 发生时到底是哪一个 exact artifact 在运行；
- incident evidence 中缺少 contract-version linkage；
- deprecated patterns 在 production 里活得太久；
- approved inventory 只存在于 wiki，而不存在于 operational tooling。

一旦出现这些问题，平台失去可控性往往不是因为一次大事故，而是因为几百个小工件都处于未跟踪状态。

## 13. 给 artifact governance 做一次快速成熟度测试

团队不应该只因为 builds 已签名、几份 configs 也放进了 version control，就觉得自己已经有 supply-chain discipline。

更高的标准应该是：

- prompt、policy、eval、capability、approval 和 runtime-control artifacts 都被当成 production artifacts；
- provenance 能在 incident review 和 rollout decisions 中被快速恢复；
- approved inventory 和 approved artifacts 被当成不同的 control layers 来管理；
- deprecated patterns 能在它们悄悄留在 production 之前被阻断；
- trust 绑定在显式 artifact properties 上，而不是靠社会性继承。

如果这些条件大多不成立，那团队也许已经有一些 artifact hygiene，但还没有真正的 artifact governance。

## 14. 实用检查清单

如果你想快速检查工件纪律，可以问：

- 所有生产工件都有 owner 吗？
- model、prompt、policy、approval-schema、runtime-control 和 eval 工件都有版本吗？
- incident review 时能快速恢复 provenance 与生效中的 contract/schema versions 吗？
- 平台是否有 approved inventory？
- 你们能区分平台批准的模式和发布批准的工件吗？
- 已废弃工件能被快速阻断吗？

如果连续几个问题的答案都是“否”，那你们还没有真正的工件治理层。

## 15. 接下来读什么

在供应链和工件纪律之后，这一部分最后一个自然主题就是 retirement、replacement 和 end-of-life discipline。成熟的系统不仅要能上线和修复，也要能优雅地下线。

## 16. 值得配套阅读的参考页

- [Policy Bundle Schema 与 Approval Contract](../../appendix/policy-bundle-schema.zh.md)
- [Lifecycle Artifact Schema](../../appendix/lifecycle-artifact-schema.zh.md)
- [Reference Package](../../appendix/reference-package.zh.md)

- [第 21 章：Assurance Loop：Red Teaming、Detection 与 Response](chapter-21.zh.md)
- [第 17 章：策略层与能力目录](../part-vii/chapter-17.zh.md)
- [第 18 章：生产上线检查清单](../part-vii/chapter-18.zh.md)
- [参考来源](../../appendix/sources.zh.md)

[^google-supply-chain]: [Google Research, Securing the AI Software Supply Chain](https://research.google/pubs/securing-the-ai-software-supply-chain/)
