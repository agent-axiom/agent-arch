# 第 18 章：生产上线检查清单

## 1. 为什么有了好的 runtime 也不代表你已经准备好上生产

即使你已经有了：

- 干净的 runtime；
- policy layer；
- capability catalog；
- observability 和 eval loop，

这仍然不意味着系统已经可以安全上线。

Production readiness 和“demo 能跑”之间的区别只有一个核心点：你不仅要知道系统在正常情况下怎么工作，还要知道它在压力下、失败时和各种不愉快边缘场景里会怎么表现。

这正是上线检查清单存在的原因。

!!! info "需要 rollout 工件？"
    如果你需要可审阅的工程工件层，可以直接查看 [Change Review 与 Rollout Gate Schema](../../appendix/change-rollout-schema.zh.md) 和 [Lifecycle Artifact Schema](../../appendix/lifecycle-artifact-schema.zh.md)。

## 2. Checklist 不是官僚流程，它是防止自我欺骗的工具

几乎每个团队都见过类似场景：

- “我们以为都检查过了”；
- “测试集上看起来没问题”；
- “我们以为 approval 肯定能工作”；
- “没想到会出现这种输入”。

Checklist 的价值不是因为团队不负责，而是因为 agent 系统太容易制造一种虚假的“已经准备好了”的感觉。

好的上线检查清单会在事故发生前暴露隐藏缺口，而不是事后补救。

## 3. Go-live 前必须检查什么

对 agent platform 来说，通常至少有七个必须覆盖的块：

- runtime correctness；
- safety and policy；
- capability execution；
- observability；
- eval and SLO readiness；
- operational readiness；
- ownership and rollback planning。

只要其中有一块没有真正闭合，系统就已经暴露在各种 unpleasant surprises 之下。

## 4. Runtime correctness

这一层适合问一些非常接地气的问题：

- 核心顺畅路径是否通过；
- tool hops 数量是否受限；
- empty / malformed inputs 是否被正确处理；
- retrieval 为空时 run 是否仍能安全运行；
- model failure 时 runtime 是否 fail safe；
- foreground 与 background actions 是否已经分开。

这是基础层。如果它本身不稳，后面的检查价值都会下降。

## 5. Safety and policy readiness

在上线前尤其要确认：

- pre-check 和 egress guardrails 是否存在；
- policy decisions 是否能在 traces 里看到；
- high-risk actions 是否真的需要 approval；
- 是否存在绕过 gateway 的直接访问路径；
- memory writes 是否受 policy 约束；
- multi-tenant boundaries 是否在真实场景下验证过。

这里是团队最容易高估自己准备度的地方：policy 可能已经写在代码里，但并没有真正嵌进所有重要路径。

## 6. Capability readiness

每个要进 production 的 capability，都值得过一遍简短的 operational 模板：

- 是否有 owner；
- transport 是否明确；
- 是否有 timeout；
- 是否有 retry policy；
- 是否有 idempotency strategy；
- 未知副作用路径是否清楚；
- outcome telemetry 是否已经接好。

如果一个 capability 连这个最低标准都没过，那它还不是 production capability，它只是一个方便的集成。

<div class="diagram-card">
<p>Go-live readiness 最好理解为多个轮廓的交集，而不是一个总状态灯</p>

``` mermaid
flowchart LR
    A["Runtime"] --> H["Production ready"]
    B["Safety"] --> H
    C["Capabilities"] --> H
    D["Observability"] --> H
    E["Eval and SLO"] --> H
    F["Ops readiness"] --> H
    G["Ownership and rollback"] --> H
```

</div>

## 7. Observability and eval readiness

非常常见的错误是：系统准备上线了，却想着“正常 traces 以后再补”。

进入 production 前，至少应该确认：

- 每个 run 都有 `trace_id`；
- 关键 spans 已经存在；
- policy decisions 和 tool outcomes 可见；
- SLO 已定义；
- offline evals 通过；
- 回归门禁已经文档化；
- 在线监控已经为第一波上线做好准备。

否则第一个事故就会变成盲查。

## 8. Operational readiness

还有一个团队很容易忘记的层：

- 是否有 on-call owner；
- 是否已经对 SLO burn 和 safety incidents 配好告警；
- manual fallback 是否清楚；
- rollback procedure 是否明确；
- 上线影响范围是否受限；
- 常见失败是否有 runbook。

这听起来像“运维的事”，但没有这一层，系统依然只是实验品，而不是 production-grade。

## 9. 一个上线检查清单策略示例

下面是一个很实用的模板：

```yaml
rollout:
  require:
    - trace_coverage
    - policy_prechecks
    - capability_owners
    - offline_eval_pass
    - slo_defined
    - rollback_plan
    - oncall_owner
  rollout_mode:
    initial: canary
    max_tenant_exposure_pct: 5
    require_shadow_period: true
  block_if:
    - unknown_side_effect_path_missing
    - direct_tool_access_present
    - policy_decisions_not_traced
```

这种 checklist 的价值在于：它把 readiness 变成一个工程讨论对象，而不是靠发布者语气里的自信。

## 10. 一个简单的就绪门禁示例

下面这个 skeleton 展示的是：如何把 readiness 看成一组必须同时满足的条件。

```python
from dataclasses import dataclass


@dataclass
class RolloutReadiness:
    trace_coverage: bool
    offline_eval_pass: bool
    slo_defined: bool
    rollback_plan: bool


def ready_for_rollout(state: RolloutReadiness) -> bool:
    return (
        state.trace_coverage
        and state.offline_eval_pass
        and state.slo_defined
        and state.rollback_plan
    )
```

这个例子很简单，但它强化了一件重要的事：production readiness 应该是可形式化的。

## 11. Go-live 流程最常见的崩坏点

这些失败模式非常典型：

- 一上来就把上线放给太多流量；
- 团队把 traces 当成“非阻塞细节”；
- ownership 只存在于文档里，on-call 没准备好；
- rollback plan 实际上只是“出事了再回滚”；
- capability owners 根本不知道真实 release window；
- safety regressions 没被当成 blocker。

这些都说明上线流程还不是生产级纪律，而只是过于乐观的发布。

## 12. 实用检查清单

如果你想在上线前快速判断 readiness，可以问：

- 是否存在正式的就绪门禁？
- 这次上线的 owner 和 on-call 是否明确？
- traces、policy decisions 和 tool outcomes 是否都会进入 telemetry？
- 是否有 canary/shadow 阶段？
- 是否有 rollback plan 和 blast-radius limit？
- high-risk flows 是否被单独验证，而不是只测了顺畅路径？

如果连续多个答案都是“没有”，那这次上线就应该视为未准备好，即使 demo 看起来很有信心。

## 13. 接下来读什么

到这里，参考实现已经长成一个完整的运行骨架。接下来你可以继续补更具体的代码示例，也可以进入打磨阶段：翻译、图示、实操附录，以及更贴近实现的代码片段。

## 14. 值得配套阅读的参考页

- [Trace Schema 与 Event Catalog](../../appendix/trace-schema.zh.md)
- [Policy Bundle Schema 与 Approval Contract](../../appendix/policy-bundle-schema.zh.md)
- [Lifecycle Artifact Schema](../../appendix/lifecycle-artifact-schema.zh.md)

- [第 17 章：策略层与能力目录](chapter-17.zh.md)
- [第七部分：参考实现](index.zh.md)
- [参考来源](../../appendix/sources.md)
