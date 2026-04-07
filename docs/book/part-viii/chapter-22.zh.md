# 第 22 章：Supply Chain、Provenance 与 Approved Artifacts

## 1. 为什么 agent systems 的 supply chain 比普通服务更宽

当工程师听到“software supply chain”时，通常会想到一些熟悉的东西：

- package dependencies；
- containers；
- CI/CD artifacts；
- build outputs 的签名和 provenance。

但对 agent systems 来说，这还不够。

问题在于，production behavior 在这里不只依赖代码。它还依赖：

- model artifacts；
- prompt 和 routine bundles；
- policy configs；
- retrieval corpora；
- capability contracts；
- eval datasets；
- approval rules；
- rollout bundles。

也就是说，agent 的 supply chain 更宽，是因为系统本身就更宽。

## 2. 什么是智能体系统里的 approved artifact

这里最好先给出一个很直白的定义：

approved artifact 就是任何一个被允许进入 production 的 artifact，因为它拥有 owner、provenance、review status 和清晰的 operational role。

这意味着 approved artifacts 不只是镜像或 wheel files。

在 agent platform 里，它们往往包括：

- approved model route；
- approved prompt bundle；
- approved policy bundle；
- approved capability contract；
- approved retrieval source；
- approved eval set；
- approved rollout template。

如果团队没有这个概念，就很容易落入一种隐式信任： “这个 artifact 应该没问题，因为之前有人用过。”

## 3. Provenance 是为了回答非常实际的问题

Google Research 的一个关键观点是：AI systems 的 provenance 不只是 formal security idea，它也是 operational necessity。[^google-supply-chain]

你必须能快速回答：

- 这个 model 从哪里来；
- 现在激活的是哪一个 prompt bundle；
- 事故发生时生效的是哪一个 policy config；
- 当时使用的是哪一版 retrieval corpus；
- release 是被哪一个 eval set 验证的；
- 这个 change 是谁批准的。

如果这些问题无法快速回答，change management 和 incident review 很快就会失控。

## 4. 智能体需要多条 chains of trust，而不是一条

在普通系统里，团队通常只想一条信任链： “代码在 CI 里构建过，容器也签名了，所以没问题。”

对 agent systems 来说，更好的思路是维护多条相互连接的信任链：

- code and build chain；
- model chain；
- prompt and routine chain；
- policy chain；
- capability chain；
- data and retrieval chain；
- eval chain。

<div class="diagram-card">
<p>与其只想一条 supply chain，不如把它看成几条相互关联的 chains of trust</p>

``` mermaid
flowchart LR
    A["Code and build"] --> G["Approved release bundle"]
    B["Model artifacts"] --> G
    C["Prompt and routine bundles"] --> G
    D["Policy bundles"] --> G
    E["Capability contracts"] --> G
    F["Eval datasets and reports"] --> G
```

</div>

## 5. Approved inventory 和 approved artifacts 不是一回事

这两个概念很接近，但并不相同。

`approved inventory` 回答的是：

- 平台上哪些 runtimes、gateways、capabilities 和 patterns 本身就是允许的。

`approved artifacts` 回答的是：

- 当前到底有哪些具体版本和 bundles 被批准运行。

例如：

- capability `create_ticket` 可以属于 approved inventory；
- 但 `policy_bundle_v12` 或 `prompt_bundle_support_v7` 是 approved artifact。

这个区别很重要，因为 inventory 提供 platform-level 框架，而 approved artifacts 提供 release-level 纪律。

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
- approval thresholds。

## 7. Eval datasets 也应该被当成 trusted artifacts

很多团队容易把 eval dataset 看得太轻： “这不就是一组例子吗？”

其实它是一个关键的 governance artifact。

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

## 9. 一个 approved artifact policy 示例

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
    - eval_dataset
    - retrieval_source
```

它帮助团队把讨论从“看起来像个正常配置”切换成“这是一个真正的 production artifact”。

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


def artifact_ready(record: ArtifactRecord) -> bool:
    return (
        record.has_owner
        and record.has_version
        and record.has_provenance
        and record.review_passed
    )
```

重点很简单：trusted artifact 应该由明确属性定义，而不是靠直觉判断。

## 12. Artifact discipline 最容易坏在哪里

常见的问题通常是这些：

- prompt bundles 没有版本；
- eval datasets quietly 变化；
- capability contracts 被编辑却没有 review trail；
- 没有人知道 incident 发生时到底是哪一个 exact artifact 在运行；
- deprecated patterns 在 production 里活得太久；
- approved inventory 只存在于 wiki，而不存在于 operational tooling。

一旦出现这些问题，平台失去可控性往往不是因为一次大事故，而是因为几百个小 artifact 都处于未跟踪状态。

## 13. 实用检查清单

如果你想快速检查 artifact discipline，可以问：

- 所有 production artifacts 都有 owner 吗？
- model、prompt、policy 和 eval artifacts 都有版本吗？
- incident review 时能快速恢复 provenance 吗？
- 平台是否有 approved inventory？
- 你们能区分 platform-approved pattern 和 release-approved artifact 吗？
- deprecated artifact 能被快速阻断吗？

如果连续几个问题的答案都是“否”，那你们还没有真正的 artifact governance layer。

## 14. 接下来读什么

在 supply chain 和 artifact discipline 之后，这一部分最后一个自然主题就是 retirement、replacement 和 end-of-life discipline。成熟的系统不仅要能上线和修复，也要能优雅地下线。

## 15. 值得配套阅读的 Reference Pages

- [Policy Bundle Schema 与 Approval Contract](../../appendix/policy-bundle-schema.zh.md)
- [Lifecycle Artifact Schema](../../appendix/lifecycle-artifact-schema.zh.md)
- [Reference Package](../../appendix/reference-package.zh.md)

- [第 21 章：Assurance Loop：Red Teaming、Detection 与 Response](chapter-21.zh.md)
- [第 17 章：策略层与能力目录](../part-vii/chapter-17.zh.md)
- [第 18 章：生产上线检查清单](../part-vii/chapter-18.zh.md)
- [参考来源](../../appendix/sources.zh.md)

[^google-supply-chain]: [Google Research, Securing the AI Software Supply Chain](https://research.google/pubs/securing-the-ai-software-supply-chain/)
