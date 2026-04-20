# 第 18 章：生产上线检查清单

## 1. 从团队必须说“上”还是“不上”的那一刻开始

继续沿用同一个支持场景。

团队已经走了很长一段路：

- 画清了架构；
- 加入了 policy layer；
- 把 memory 和 tool execution 分开；
- 接上了 traces 和 structured events；
- 修掉了由错误 retry 路径引发的重复工单问题。

现在最难的问题来了：

> 这个智能体现在能不能至少先放给前 5% 的 tenants？

也正是在这里，“我们已经做了很多” 和 “这套系统真的可以上线” 之间的差别会暴露出来。

这正是本章的 distinct promise。它应该帮助读者再跨过一条边界：从一个可运行、受治理的系统，走到一个团队真的能在 go/no-go 时刻为之负责的系统。

即使你已经有了：

- 干净的 runtime；
- 策略层；
- 能力目录；
- 可观测性和评测闭环，

这仍然不意味着系统已经可以安全上线。

生产就绪性和“demo 能跑”之间真正的区别在于：你不仅要知道系统在 happy path 里怎么表现，还要知道它在压力下、失败时和各种不愉快边缘场景里会怎么表现。

这正是 rollout checklist 存在的原因。

!!! info "需要 rollout 工件？"
    如果你需要可审阅的工程工件层，可以直接查看 [Change Review 与 Rollout Gate Schema](../../appendix/change-rollout-schema.zh.md) 和 [Lifecycle Artifact Schema](../../appendix/lifecycle-artifact-schema.zh.md)。

## 2. Checklist 不是官僚流程，而是防止自我欺骗的工具

几乎每个团队都见过类似场景：

- “测试里看起来都没问题”；
- “我们以为 approval 肯定能工作”；
- “没想到会出现这种输入”；
- “如果出事我们再快速回滚”。

问题不在于团队不认真，而在于 agent 系统太容易制造一种虚假的“已经准备好了”的感觉。

对于这个支持智能体，风险很具体：如果 rollout 出问题，后果会很快流到外部世界：

- 会出现重复工单；
- 用户会看到错误状态；
- 支持团队会收到额外噪音；
- 事故调查会在 side effects 已经发生之后才开始。

好的上线检查清单不是为了仪式感，而是为了在事故前暴露隐藏缺口，而不是事后补救。

## 3. 第一波 rollout 前必须真正闭合什么

这才是 rollout discipline 在实践中的真正形状。团队在决定的不是“这个功能看起来有没有前景”，而是每一个与 release 相关的 contour 是否已经被审查到足以承受 partial failure、pause、drift 与 rollback。

对 agent platform 来说，通常至少有七个必须覆盖的块：

- runtime correctness；
- safety and policy；
- capability execution；
- observability；
- eval and SLO readiness；
- operational readiness；
- ownership and rollback planning。

只要其中有一块没有真正闭合，系统就已经暴露在意外之下。这也是为什么 rollout 应该被看成多个 contour 的收敛问题，而不是某一个团队拥有的一盏绿色信号灯。

对于这个支持场景，这意味着：即使只是 5% canary，团队也必须能回答的不只是“happy path 通不通”，而是“在 partial failure 下到底会发生什么”。

## 4. Runtime correctness

这一层适合问一些非常接地气的问题：

- 核心顺畅路径是否通过；
- tool hops 数量是否受限；
- empty / malformed inputs 是否被正确处理；
- 检索为空时运行是否仍能安全运行；
- 模型失败时运行时是否安全失效；
- foreground 与 background actions 是否已经分开。

对于这个支持智能体，这意味着类似的问题：

- 没有经过验证的 `request_id` 时，是否可能仍然创建工单；
- 在查不到请求状态时，run 能否安全结束；
- foreground path 已经判定失败后，background write 是否还会继续。

这是基础层。如果它本身不稳，后面的检查价值都会下降。

## 5. Safety and policy readiness

在 rollout 前尤其要确认：

- pre-check 和 egress guardrails 是否存在；
- policy decisions 是否能在 traces 里看到；
- high-risk actions 是否真的需要 approval；
- 是否存在绕过 gateway 的直接访问路径；
- memory writes 是否受 policy 约束；
- multi-tenant boundaries 是否在真实场景下验证过。

这里是团队最容易高估自己准备度的地方：policy 可能已经写在代码里，但并没有真正嵌进所有关键路径。

对于这个支持场景，最关键的问题是：

> 智能体是否能通过哪怕一条路径，在绕过 policy 和 audit trail 的情况下创建工单、读取状态，或者写入 profile memory？

如果答案是“能”或“不确定”，那 rollout 还太早。

## 6. Capability readiness

每个要进生产环境的能力，都值得过一遍简短的运行模板：

- 是否有 owner；
- 传输方式是否明确；
- 是否有 timeout；
- 是否有 retry policy；
- 是否有 idempotency strategy；
- 未知副作用路径是否清楚；
- 结果遥测是否已经接好。

如果一个能力连这个最低标准都没过，那它还不是生产级能力，它只是一个方便的集成。

在这个支持智能体里，`create_support_ticket` 和 `check_access_request_status` 虽然都在同一个目录里，但 readiness burden 并不一样：

- read capability 可能在 timeout 和 telemetry 规范后就接近可用；
- write capability 没有 idempotency、outcome normalization 和清晰 rollback story 就还不算 ready。

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

进入生产环境前，至少应该确认：

- 每个 run 都有 `trace_id`；
- 关键 spans 已经存在；
- policy decisions 和 tool outcomes 可见；
- SLO 已定义；
- 离线评测通过；
- 受影响的 high-risk paths 已单独演练过 failed-run drills；
- 当 release evidence 依赖 graded judgments 时，verifier quality 已被审查；
- 回归门禁已经文档化；
- 在线监控已经为第一波上线做好准备。

否则第一个事故就会变成盲查。

对于这个支持智能体，这一点尤其重要，因为第一批 canary tenants 几乎一定会带来不完美输入。如果团队看不到：

- 智能体到底走了哪条路径；
- 是否发生了 duplicate tool call；
- 用的 `idempotency_key` 是什么；
- 哪个 policy gate 做了决策，

那第一波 rollout 本身就已经变成了彩票。

## 8. Approval path readiness

一旦 approval 被建模成显式 runtime path，rollout readiness 也必须把这条路径算进去。

团队也许已经在纸面上写好了 policy rules，但如果 approval 造成隐藏队列、ownership 不清，或者 run 会无限期停在 paused 状态，系统依然还没准备好进 production。

在 rollout 前，至少应该检查：

- approval latency 是否被度量；
- approval queue 是否有 owner；
- paused runs 是否有 timeout 或 expiry rule；
- 是否有可见的 backlog threshold；
- resume/cancel 行为是否明确；
- human review 不可用时是否存在 fallback；
- capability-session expiry 是否被当成可见 rollout signal，而不是隐藏 transport failure；
- 当 stateful capability session 已无法安全 resume 时，re-initialization behavior 是否已定义。

这对同一个支持智能体会立刻变得重要。如果创建工单的路径会因为 approval 而暂停，团队就必须知道这次 run 会等五秒、三十分钟，还是无限期等待。这不是 UX 细节，而是 production behavior 的一部分。

一个非常实用的 rollout gate 是：

> 我们是否知道现在有多少 runs 正在等待 approval，它们已经等了多久，如果没有人在时限内响应系统会做什么，以及当底层 capability session 更早过期时 runtime 又会做什么？

如果答案是否定的，那 approval 仍然只是一个未被治理的 side channel。

### 8.1. Stateful capability 的 interruptions 也必须进入 rollout readiness

一旦 approval 和 stateful MCP 或其他可恢复的 capability session 结合在一起，rollout readiness 就必须把 interruption semantics 直接纳入检查。

这意味着团队至少要能回答这些问题：

- 有多少 runs 正在等待 human approval，同时 capability session 仍然存活；
- 有多少 runs 已经越过 capability-session expiry，现在需要 re-init；
- re-initialization 是保留同一个 user-visible run id，还是创建新的 operational thread；
- re-init 之后的下一步是否会触发 fresh policy decision；
- telemetry 能否把原始 paused state 与 resumed 或 reinitialized state 关联起来。

如果这些问题答不上来，rollout 可能在 approval layer 看起来正常，但在 capability-session layer 已经开始退化。

Anthropic 的 workflow taxonomy 在这里又增加了一个 rollout 维度。[^anthropic] 对于 pattern-aware runtime，orchestration pattern 的变化应该被视为 release-bearing behavior，而不是不可见的实现细节。

在 rollout 前，团队应该能够明确说出：

- 某条路径现在是否改成了 `routing`，而过去还是 fixed workflow；
- `parallelization` 是否引入了新的 join-state、duplicate-read 或 approval-ordering 风险；
- `orchestrator-workers` 是否增加了 delegated worker surfaces、worker-safe catalogs 或新的 review points；
- `prompt chaining` 是否插入了新的 checkpoints，从而改变 expiry、pause 或 retry semantics。

这很重要，因为 pattern changes 即使不改变表面功能描述，也会改变 production behavior。

对 delegated authorization 也是一样。如果 runtime 支持 user-delegated access，那么 rollout readiness 还应该覆盖：

- traces 是否保留 `authorization_mode`、delegated principal 与 delegated scope；
- approval records 是否保持与原始 run 相同的 authorization context；
- session export 是否还能说明动作到底是在谁的 delegated identity 下执行；
- 如果 run 正在暂停中而 delegated access 被撤销，runtime 会怎么处理。

否则团队在 policy 和 approval 维度上看起来准备好了，但在生产里依然解释不清到底是谁授权了 write path。

## 9. Operational readiness

还有一个团队很容易忘记的层：

- 是否有 on-call owner；
- 是否已经对 SLO burn 和 safety incidents 配好告警；
- manual fallback 是否清楚；
- rollback procedure 是否明确；
- 上线影响范围是否受限；
- 常见失败是否有 runbook。

这听起来像“运维的事”，但没有这一层，系统依然只是实验品，而不是生产级系统。

对于这个支持场景，manual fallback 必须尤其具体：

- 关停智能体后由谁接管流量；
- 怎样停止 write path；
- 如何标记 canary wave 中创建的可疑工单；
- 失败 rollout 的后果由谁清理。

## 10. rollout readiness 的实用规则

如果要把最有用的 operational 规则压缩成一组，通常这些就够了：

1. 没有 trace coverage、rollback plan 和明确 owner，就不应该开始 rollout。
2. 没有 idempotency、outcome normalization 和 policy visibility 的 write capability，不应该进入 canary。
3. High-risk flows 必须独立于 happy path 单独验证。
4. Canary、shadow 和 blast-radius limits 应该是设计的一部分，而不是出事后的临时 improvisation。
5. Approval queue、paused-run age 和 human-review backlog 应该被当成 rollout signals，而不是看不见的运维噪音。
6. orchestration pattern 选择的变化应该被当成 runtime-control changes，并在 rollout 前显式 review。
7. 如果 release evidence 依赖 verifier judgments，那么一旦 verifier quality 或 evidence linkage 不再可信，就应先停 rollout。
8. 如果团队已经不再信任 traces、approval handling 或 evals，就应该先停 rollout，而不是继续“边上边看”。

## 11. 一个上线检查清单策略示例

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
    - approval_queue_owner
    - session_expiry_signals_visible
    - orchestration_pattern_reviewed
  rollout_mode:
    initial: canary
    max_tenant_exposure_pct: 5
    require_shadow_period: true
  block_if:
    - unknown_side_effect_path_missing
    - direct_tool_access_present
    - policy_decisions_not_traced
    - approval_backlog_unbounded
    - paused_runs_without_expiry
    - capability_session_reinit_unmodeled
    - orchestration_pattern_change_unreviewed
```

这种检查清单的价值在于：它把就绪性变成一个工程讨论对象，而不是靠发布者语气里的自信。

## 12. 一个简单的就绪门禁示例

下面这个 skeleton 展示的是：如何把 readiness 看成一组必须同时满足的条件。

```python
from dataclasses import dataclass


@dataclass
class RolloutReadiness:
    trace_coverage: bool
    offline_eval_pass: bool
    slo_defined: bool
    rollback_plan: bool
    approval_path_defined: bool


def ready_for_rollout(state: RolloutReadiness) -> bool:
    return (
        state.trace_coverage
        and state.offline_eval_pass
        and state.slo_defined
        and state.rollback_plan
        and state.approval_path_defined
    )
```

这个例子很简单，但它强化了一件重要的事：生产就绪性应该是可形式化的。

## 13. Go-live 流程最常见的崩坏点

这些失败模式非常典型：

- 一上来就把 rollout 放给太多流量；
- 团队把 traces 当成“非阻塞细节”；
- ownership 只存在于文档里，on-call 没准备好；
- rollback plan 实际上只是“出事了再回滚”；
- 能力负责人根本不知道真实发布时间窗；
- safety regressions 没被当成 blocker；
- paused runs 不断累积，因为 approval queue 没有 owner；
- approval latency 直到用户已经在等待时才第一次被看见。

对于这个支持智能体，这些问题往往会更危险地表现出来：

- canary 很快变成 broad rollout；
- duplicate ticket incident 被当成“小集成问题”；
- memory write regressions 不阻断发布；
- 团队已经不信任自己的 traces，却还在继续 rollout。

一旦这样，rollout process 就还不是生产级纪律，而只是过于乐观的发布。

## 14. 给 rollout readiness 做一次快速成熟度测试

团队不应该只因为 demo 能跑、checklist 看起来大多是绿色、第一波 canary 似乎很小，就觉得自己已经准备好进 production。

更高的标准应该是：

- high-risk paths 被独立于 happy path 单独验证；
- traces、policy visibility 和 rollback 在扩大暴露前就值得信任；
- write capabilities 具备 idempotency 和明确的 unknown-outcome path；
- blast radius 是按设计被限制的，而不是靠乐观控制；
- approval backlog、timeout 与 resume/cancel behavior 都被明确规定；
- ownership、on-call 和 manual fallback 都足够具体。

如果这些条件大多不成立，那团队也许已经有 launch momentum，但还没有真正的 rollout readiness。

## 15. 读完这一章后先做什么

如果你想在 rollout 前快速判断 readiness，可以先过一遍这个短清单：

1. 是否存在正式的 readiness gate？
2. 这次 rollout 的 owner 和 on-call 是否明确？
3. traces、policy decisions 和 tool outcomes 是否都会进入 telemetry？
4. 是否有 canary/shadow 阶段？
5. 是否有 rollback plan 和 blast-radius limit？
6. high-risk flows 是否被单独验证，而不是只测了顺畅路径？
7. approval 是否对 paused runs 设有可见的 timeout/backlog 规则？

如果连续多个答案都是“没有”，那这次 rollout 就应该视为未准备好，即使 demo 看起来很顺。

## 16. 接下来读什么

到这里，参考实现已经闭合了同一个支持智能体及其平台最基本的运行骨架。下一步就是生命周期纪律：如何变更、发布、调查和下线这样的系统，同时不丢掉控制力。

## 17. 值得配套阅读的参考页

- [Trace Schema 与 Event Catalog](../../appendix/trace-schema.zh.md)
- [Policy Bundle Schema 与 Approval Contract](../../appendix/policy-bundle-schema.zh.md)
- [Lifecycle Artifact Schema](../../appendix/lifecycle-artifact-schema.zh.md)

这一章把第 17 章里的 governed runtime path 变成 rollout discipline。相同的 approval、pause/resume 与 control signals，接下来会在第 21 章里继续作为 assurance loop 的一部分出现。

- [第 17 章：策略层与能力目录](chapter-17.zh.md)
- [第七部分：参考实现](index.zh.md)
- [第八部分：智能体系统的生命周期](../part-viii/index.zh.md)
- [参考来源](../../appendix/sources.zh.md)
