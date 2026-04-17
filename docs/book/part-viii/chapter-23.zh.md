# 第 23 章：退役、替换与终止使用纪律

## 1. 为什么成熟的智能体系统必须学会“离场”

很多团队对生命周期的理解停留在这里：

- 想出系统；
- 把它做出来；
- 保护它；
- 观察它；
- 安全地发布变更。

但任何生产系统还有一个必经阶段：它迟早要被替换、关闭或退役。

这对智能体系统尤其重要，因为它们通常会留下很长的运行尾部：

- 记忆状态；
- 工具访问；
- 审批与审计轨迹；
- paused-run state 与 background-run state；
- capability-session state 与 interruption lineage；
- orchestration-pattern lineage 与 worker-boundary decisions；
- delegated authorization lineage 与 revoke state；
- verifier-contract lineage 与 verifier evidence retention obligations；
- 外部集成；
- 用户预期；
- 依赖它的工作流。

也就是说，退役不是“删掉服务然后忘记它”，而是一个被管理的运行过程。

## 2. 什么时候应该开始考虑退役

最好不要把退役当成遥远又尴尬的话题。

在实践里，常见触发条件包括：

- 运行时或模型已经过时；
- 能力契约不再被认为安全；
- 维护成本太高；
- 质量已经到顶，必须替换；
- 新的平台路径正在替代旧路径；
- 监管或治理要求发生变化；
- 产品问题本身已经不存在。

如果团队没有明确的退役触发条件，旧的智能体系统几乎总会活得比安全和有用所允许的更久。

## 3. 退役和替换不是一回事

最好把这两个场景分开：

- `retirement`：系统或能力直接退出运行；
- `replacement`：旧系统下线之前或同时，由一个新系统接手。

这个区别很重要。

在退役里，核心问题是如何安全地下掉旧系统。

在替换里，核心问题是如何在不丢失质量、控制和历史的前提下完成受控迁移。

## 4. 最大的风险，是系统虽然“退役了”却仍然能行动

最糟糕的一类运行错误通常是这样发生的：

- 团队以为系统“基本已经关了”；
- 但它仍然保留着：
- 活跃的工具主体；
- 仍然在线的连接器；
- 记忆访问权；
- 旧的上线路径；
- 后台任务；
- 可恢复的 paused approval path；
- 已过期但仍可通过旧路径 re-initialize 的 capability session；
- 仍被 gateways 接受的旧 runtime-control schema。

形式上系统已经“死了”，但在运行上它仍然能行动。

这对智能体特别危险，因为自主和半自主的执行路径很容易被忘掉。

## 5. 退役最好按层收缩

好的终止使用流程很少是一个动作完成的。通常更适合按层来做：

- 停止新的上线波次；
- 关闭高风险能力；
- 把写入动作切到仅审批模式，或者直接停用；
- 停止记忆写入；
- 让 paused runs 过期或直接取消；
- 停止后台任务与 background routes；
- 关闭或归档 capability-session state，并阻断不受控的 re-init；
- 停用已废弃的 orchestration patterns，并撤销 worker-safe catalog exposure；
- 撤销 delegated authorization paths，并归档它们最终的 lineage；
- retire 已废弃的 verifier contracts，并保留解释既往 rollout 或 assurance decisions 所需的 evidence；
- 撤销出口访问；
- 关闭主体、密钥和连接器；
- 固化最终审计状态。

<div class="diagram-card">
<p>更稳妥的退役，更像是一步步缩小运行面</p>

``` mermaid
flowchart LR
    A["Freeze rollout"] --> B["Disable risky capabilities"]
    B --> C["Disable writes and background jobs"]
    C --> D["Revoke egress and principals"]
    D --> E["Archive audit and memory state"]
    E --> F["Mark system retired"]
```

</div>

## 6. 记忆与审计数据需要单独的纪律

一旦系统退役，一个不舒服的问题就出现了：积累下来的状态该怎么办？

团队通常需要分别决定：

- 什么要归档；
- 什么要删除；
- 什么要匿名化；
- 追踪和审批保留多久；
- 归档状态的负责人是谁；
- 替换后的系统是否可以复用旧数据集和记忆工件；
- 是否需要保留 delegated authorization records，以说明旧动作到底在谁的 identity 下执行；
- 是否需要保留 verifier evidence 与 verifier-contract history，以解释为何早先的 releases 会被判定为可接受。

所以退役影响的不只是正在运行的系统，还包括整段历史运行足迹。

## 7. 替换应该分阶段，而不是二元切换

当旧系统被新系统替换时，最自然的冲动是：“直接切换过去，然后继续前进。”

对智能体系统来说，这通常太冒险。

更安全的是分阶段替换：

- 影子对比；
- 小范围租户迁移；
- 在关键场景里双运行；
- 并行评测；
- 分阶段切流；
- 只有在信心足够时才做最终切换。

这也是替换和上线纪律最接近的地方，只不过替换还多了一个问题：如何在新旧系统之间保持连续性。

## 8. 老的能力和模式应该被正式废弃

最好不仅有 `approved inventory`，还要有 `deprecated inventory`。

例如：

- 已废弃的运行时；
- 已废弃的提示包族；
- 已废弃的网关模式；
- 已废弃的记忆策略；
- 已废弃的能力契约；
- 已废弃的 approval schema；
- 已废弃的 runtime-control schema；
- 已废弃的 orchestration pattern 或 worker-boundary policy；
- 已废弃的 capability-session contract；
- 已废弃的 verifier contract。

这很重要，因为退役几乎总是从“明确宣布这条路不再是正常路径”开始，而不是从突然关机开始。

## 9. 面向用户的过渡也是生命周期的一部分

如果智能体系统影响到用户或内部工作流，那么终止使用不能只在平台层内部完成。

最好单独想清楚：

- 需要通知谁；
- 哪些流程会变化；
- 哪些预期需要重新设置；
- 会有哪些回退路径；
- 老的集成还要支持多久。

这对内部智能体系统尤其重要，因为它们很快就会长进团队的真实工作习惯里。

## 10. 一个 retirement policy 示例

下面这个骨架很实用：

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
    - expire_paused_runs
    - stop_background_routes
    - freeze_reinitialization
    - disable_deprecated_patterns
    - revoke_worker_capability_exposure
    - retire_verifier_contracts
    - revoke_egress
    - archive_audit_state
    - set_retired_status
```

它的价值不在于 YAML 本身，而在于把退役变成了明确的运行契约。

## 11. 一个 replacement readiness check 示例

下面这个代码片段展示的是正确的门禁形态：

```python
from dataclasses import dataclass


@dataclass
class ReplacementState:
    shadow_eval_passed: bool
    migration_plan_ready: bool
    risky_capabilities_disabled: bool
    archive_plan_ready: bool
    paused_runs_drained: bool
    capability_sessions_resolved: bool


def ready_for_replacement(state: ReplacementState) -> bool:
    return (
        state.shadow_eval_passed
        and state.migration_plan_ready
        and state.risky_capabilities_disabled
        and state.archive_plan_ready
        and state.paused_runs_drained
        and state.capability_sessions_resolved
    )
```

重点很简单：替换也应该有门禁，而不是“凭感觉切换”。

## 12. 终止使用纪律最常坏在哪里

这些问题非常常见：

- 系统被认为已经退役，但主体还活着；
- 后台任务没关；
- 记忆写入路径仍然在工作；
- paused approvals 在 retirement 之后仍然可以 resume；
- 已过期 capability sessions 仍可通过陈旧控制路径 re-initialize；
- 已废弃的 orchestration patterns 或 worker-boundary policies 在 retirement 后仍然可用；
- 已废弃的 verifier contracts 或 verifier evidence obligations 在 retirement 后仍然不清楚；
- background routes 被遗忘没有关闭；
- 归档状态没有负责人；
- deprecated schemas 仍然被 gateways 或 runtimes 接受；
- 已废弃模式存活太久；
- 替换没有双运行或分阶段迁移。

正是这些小细节，会把一个“几乎完整”的 lifecycle 重新变成事故来源。

## 13. 给 end-of-life discipline 做一次快速成熟度测试

团队不应该只因为会把流量切走、再把系统标成 deprecated，就觉得自己已经会做 retirement。

更高的标准应该是：

- 系统会在被宣布 retired 之前先失去行动能力；
- principals、connectors、memory writes、paused runs、capability sessions、orchestration patterns 与 background jobs 会被有意识地逐层收缩；
- replacement 是 staged 的，而不是二元 cutover；
- deprecated approval 与 runtime-control schemas 会被真正关闭，而不是作为隐藏兼容路径长期残留；
- archived state 有 owner，也有 retention decision；
- deprecated patterns 会变成真正被阻断的 paths，而不只是 warnings。

如果这些条件大多不成立，那团队也许已经有一些 shutdown mechanics，但还没有真正的 end-of-life discipline。

## 14. 实用检查清单

如果你想快速检查自己的终止使用纪律，可以问：

- 系统是否有明确的退役触发条件？
- 能力能否按阶段关闭，而不是只能“一键全关”？
- 关闭后记忆、追踪、审批、paused-run state 和 capability-session state 怎么处理，是否清楚？
- 是否有分阶段替换计划？
- 主体、连接器、出口访问、paused approvals、capability-session re-init 和 background routes 能否快速撤销或排空？
- 已归档工件和历史状态的负责人是否明确？

如果连续几个问题的答案都是“否”，那你的生命周期其实还停留在发布，而不是完整运营。

## 15. 接下来读什么

这章把 Part VIII 真正闭合成一个完整的运行闭环：

- SDLC -> ADLC；
- 变更管理；
- 保障闭环；
- 工件治理；
- 退役与替换。

现在这一部分已经不仅能解释架构，还能作为生产级 agent systems 的生命周期手册使用。

## 16. 值得配套阅读的参考页

- [生命周期工件规范](../../appendix/lifecycle-artifact-schema.zh.md)
- [策略包模式与审批契约](../../appendix/policy-bundle-schema.zh.md)
- [参考包](../../appendix/reference-package.zh.md)

- [第 19 章：从 SDLC 到 ADLC](chapter-19.zh.md)
- [第 22 章：供应链、来源追踪与已批准工件](chapter-22.zh.md)
- [第 24 章：智能体失配与内部人风险](chapter-24.zh.md)
- [第 27 章：Agent Inventory、Registry 与 Sprawl 治理](chapter-27.zh.md)
- [第八部分：智能体系统生命周期](index.zh.md)
- [参考来源](../../appendix/sources.zh.md)
