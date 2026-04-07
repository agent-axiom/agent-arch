# 第 23 章：Retirement、Replacement 与 End-of-Life Discipline

## 1. 为什么成熟的智能体系统必须学会“离场”

很多团队对 lifecycle 的理解停留在这里：

- 想出系统；
- 把它做出来；
- 保护它；
- 观察它；
- 安全地发布变更。

但任何 production system 还有一个必经阶段：它迟早要被替换、关闭或退役。

这对 agent systems 尤其重要，因为它们通常会留下很长的 operational tail：

- memory state；
- tool access；
- approvals 与 audit trails；
- external integrations；
- user expectations；
- dependent workflows。

也就是说，retirement 不是“删掉服务然后忘记它”，而是一个被管理的 operational process。

## 2. 什么时候应该开始考虑 retirement

最好不要把 retirement 当成遥远又尴尬的话题。

在实践里，常见 trigger 包括：

- runtime 或 model 已经过时；
- capability contract 不再被认为安全；
- maintenance cost 太高；
- quality 已经到顶，必须 replacement；
- 新的 platform path 正在替代旧路径；
- regulatory 或 governance requirements 发生变化；
- 产品问题本身已经不存在。

如果团队没有明确的 retirement triggers，旧的 agent systems 几乎总会活得比安全和有用所允许的更久。

## 3. Retirement 和 replacement 不是一回事

最好把这两个场景分开：

- `retirement`：系统或 capability 直接退出运行；
- `replacement`：旧系统下线之前或同时，由一个新系统接手。

这个区别很重要。

在 retirement 里，核心问题是如何安全地下掉旧系统。

在 replacement 里，核心问题是如何在不丢失质量、控制和历史的前提下完成受控迁移。

## 4. 最大的风险，是系统虽然“退役了”却仍然能行动

最糟糕的一类 operational 错误通常是这样发生的：

- 团队以为系统“基本已经关了”；
- 但它仍然保留着：
  - active tool principal；
  - live connector；
  - memory access；
  - 旧 rollout path；
  - background job。

形式上系统已经“死了”，但在 operational 上它仍然能行动。

这对 agents 特别危险，因为 autonomous 和 semi-autonomous execution paths 很容易被忘掉。

## 5. Retirement 最好按层收缩

好的 end-of-life process 很少是一个动作完成的。通常更适合按层来做：

- 停止新的 rollout waves；
- 关闭 risky capabilities；
- 把 write actions 切到 approval-only 或直接 disable；
- 停止 memory writes；
- 停止 background jobs；
- 撤销 egress access；
- 关闭 principals、secrets 和 connectors；
- 固化 final audit state。

<div class="diagram-card">
<p>更稳妥的 retirement，更像是一步步缩小 operational surface</p>

``` mermaid
flowchart LR
    A["Freeze rollout"] --> B["Disable risky capabilities"]
    B --> C["Disable writes and background jobs"]
    C --> D["Revoke egress and principals"]
    D --> E["Archive audit and memory state"]
    E --> F["Mark system retired"]
```

</div>

## 6. Memory 和 audit data 需要单独的纪律

一旦系统退役，一个不舒服的问题就出现了：积累下来的 state 该怎么办？

团队通常需要分别决定：

- 什么要 archive；
- 什么要 delete；
- 什么要 anonymize；
- traces 和 approvals 保留多久；
- archived state 的 owner 是谁；
- replacement 是否可以复用旧 datasets 和 memory artifacts。

所以 retirement 影响的不只是 running system，还包括整个 historical operational footprint。

## 7. Replacement 应该分阶段，而不是二元切换

当旧系统被新系统替换时，最自然的冲动是：“直接 cutover，然后继续前进。”

对 agent systems 来说，这通常太冒险。

更安全的是 staged replacement：

- shadow comparison；
- limited tenant migration；
- dual-run for critical scenarios；
- side-by-side evals；
- staged traffic shift；
- 只有在信心足够时才 final cutover。

这也是 replacement 和 rollout discipline 最接近的地方，只不过 replacement 还多了一个问题：如何在新旧系统之间保持 continuity。

## 8. 老的 capabilities 和 patterns 应该被正式 deprecate

最好不仅有 `approved inventory`，还要有 `deprecated inventory`。

例如：

- deprecated runtime；
- deprecated prompt bundle family；
- deprecated gateway pattern；
- deprecated memory strategy；
- deprecated capability contract。

这很重要，因为 retirement 几乎总是从“明确宣布这条路不再是正常路径”开始，而不是从突然关机开始。

## 9. 面向用户的过渡也是 lifecycle 的一部分

如果 agent system 影响到用户或内部 workflow，那么 end-of-life 不能只在 platform layer 内部完成。

最好单独想清楚：

- 需要通知谁；
- 哪些 flows 会变化；
- 哪些 expectations 需要重新设置；
- 会有哪些 fallback paths；
- 老的 integrations 还要支持多久。

这对 internal agent systems 尤其重要，因为它们很快就会长进团队的真实工作习惯里。

## 10. 一个 retirement policy 示例

下面这个 skeleton 很实用：

```yaml
retirement:
  triggers:
    - deprecated_runtime
    - unsafe_capability_pattern
    - maintenance_cost_exceeded
    - replacement_ready
  required_steps:
    - freeze_rollout
    - disable_risky_capabilities
    - stop_memory_write
    - revoke_egress
    - archive_audit_state
    - set_retired_status
```

它的价值不在于 YAML 本身，而在于把 retirement 变成了明确的 operational contract。

## 11. 一个 replacement readiness check 示例

下面这个代码片段展示的是正确的 gate 形态：

```python
from dataclasses import dataclass


@dataclass
class ReplacementState:
    shadow_eval_passed: bool
    migration_plan_ready: bool
    risky_capabilities_disabled: bool
    archive_plan_ready: bool


def ready_for_replacement(state: ReplacementState) -> bool:
    return (
        state.shadow_eval_passed
        and state.migration_plan_ready
        and state.risky_capabilities_disabled
        and state.archive_plan_ready
    )
```

重点很简单：replacement 也应该有 gate，而不是“凭感觉切换”。

## 12. End-of-life discipline 最常坏在哪里

这些问题非常常见：

- 系统被认为已经 retired，但 principals 还活着；
- background jobs 没关；
- memory write path 仍然在工作；
- archived state 没有 owner；
- deprecated patterns 存活太久；
- replacement 没有 dual-run 或 staged migration。

正是这些小细节，会把一个“几乎完整”的 lifecycle 重新变成事故来源。

## 13. 实用检查清单

如果你想快速检查自己的 end-of-life discipline，可以问：

- 系统是否有明确的 retirement triggers？
- capabilities 能否按阶段关闭，而不是只能“一键全关”？
- shutdown 后 memory、traces 和 approvals 怎么处理，是否清楚？
- 是否有 staged replacement plan？
- principals、connectors 和 egress access 能否快速撤销？
- archived artifacts 和 historical state 的 owner 是否明确？

如果连续几个问题的答案都是“否”，那你的 lifecycle 其实还停留在 release，而不是完整运营。

## 14. 接下来读什么

这章把 Part VIII 真正闭合成一个完整的 operational cycle：

- SDLC -> ADLC；
- change management；
- assurance loop；
- artifact governance；
- retirement and replacement。

现在这一部分已经不仅能解释架构，还能作为 production-grade agent systems 的 lifecycle handbook 使用。

## 15. 值得配套阅读的参考页

- [Lifecycle Artifact Schema](../../appendix/lifecycle-artifact-schema.zh.md)
- [Policy Bundle Schema 与 Approval Contract](../../appendix/policy-bundle-schema.zh.md)
- [Reference Package](../../appendix/reference-package.zh.md)

- [第 19 章：从 SDLC 到 ADLC](chapter-19.zh.md)
- [第 22 章：Supply Chain、Provenance 与 Approved Artifacts](chapter-22.zh.md)
- [第八部分：智能体系统生命周期](index.zh.md)
- [参考来源](../../appendix/sources.zh.md)
