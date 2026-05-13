# 第 18 章：生产上线检查清单

## 1. 从团队必须说“上”还是“不上”的那一刻开始

继续沿用同一个支持场景。

团队已经走了很长一段路：

- 画清了架构；
- 加入了策略层；
- 把记忆和工具执行分开；
- 接上了追踪和结构化事件；
- 修掉了由错误重试路径引发的重复工单问题。

现在最难的问题来了：

> 这个智能体现在能不能至少先放给前 5% 的租户？

也正是在这里，“我们已经做了很多”和“这套系统真的可以上线”之间的差别会暴露出来。

这正是本章的独特承诺。它应该帮助读者再跨过一条边界：从一个可运行、受治理的系统，走到一个团队真的能在上线/不上线时刻为之负责的系统。

即使你已经有了：

- 干净的运行时；
- 策略层；
- 能力目录；
- 可观测性和评测闭环，

这仍然不意味着系统已经可以安全上线。

生产就绪性和“演示能跑”之间真正的区别在于：你不仅要知道系统在顺畅路径里怎么表现，还要知道它在压力下、失败时和各种不愉快边缘场景里会怎么表现。

这正是 rollout 检查清单存在的原因。

!!! info "需要 rollout 工件？"
    如果你需要可审阅的工程工件层，可以直接查看 [Change Review 与 Rollout Gate Schema](../../appendix/change-rollout-schema.zh.md) 和 [Lifecycle Artifact Schema](../../appendix/lifecycle-artifact-schema.zh.md)。

## 2. 检查清单不是官僚流程，而是防止自我欺骗的工具

几乎每个团队都见过类似场景：

- “测试里看起来都没问题”；
- “我们以为审批肯定能工作”；
- “没想到会出现这种输入”；
- “如果出事我们再快速回滚”。

问题不在于团队不认真，而在于智能体系统太容易制造一种虚假的“已经准备好了”的感觉。

对于这个支持智能体，风险很具体：如果 rollout 出问题，后果会很快流到外部世界：

- 会出现重复工单；
- 用户会看到错误状态；
- 支持团队会收到额外噪音；
- 事故调查会在副作用已经发生之后才开始。

这不是理论风险：Moffatt v. Air Canada 案例已经说明，即使是面向用户的 AI 场景，也可能转化为外部损害和公司责任。[^moffatt]

好的上线检查清单不是为了仪式感，而是为了在事故前暴露隐藏缺口，而不是事后补救。

## 3. 第一波 rollout 前必须真正闭合什么

这才是 rollout 纪律在实践中的真正形状。团队在决定的不是“这个功能看起来有没有前景”，而是每一个与发布相关的轮廓是否已经被审查到足以承受部分失败、暂停、漂移与回滚。

对智能体平台来说，通常至少有七个必须覆盖的块：

- 运行时正确性；
- 安全与策略；
- 能力执行；
- 可观测性；
- 评测与 SLO 就绪性；
- 运营就绪性；
- 负责人归属与回滚规划。

只要其中有一块没有真正闭合，系统就已经暴露在意外之下。这也是为什么 rollout 应该被看成多个轮廓的收敛问题，而不是某一个团队拥有的一盏绿色信号灯。

对于这个支持场景，这意味着：即使只是 5% 金丝雀，团队也必须能回答的不只是“顺畅路径通不通”，而是“在部分失败下到底会发生什么”。

!!! example "贯穿案例：重复工单后的金丝雀"
    在把支持智能体放到 5% rollout 之前，团队不应该只展示一次成功的状态检查和工单创建。评审应该看到：重复工单回归门已经通过，`create_support_ticket` 有幂等策略，`side_effect_unknown` 会让运行停在对账前，traces 保留了结果，而且回滚负责人已经明确。否则，金丝雀测试的是希望，而不是就绪性。

## 4. 运行时正确性

这一层适合问一些非常接地气的问题：

- 核心顺畅路径是否通过；
- 工具跳数是否受限；
- 空输入/格式错误输入是否被正确处理；
- 检索为空时运行是否仍能安全运行；
- 模型失败时运行时是否安全失效；
- 前台与后台动作是否已经分开。

对于这个支持智能体，这意味着类似的问题：

- 没有经过验证的 `request_id` 时，是否可能仍然创建工单；
- 在查不到请求状态时，运行能否安全结束；
- 前台路径已经判定失败后，后台写入是否还会继续。

这是基础层。如果它本身不稳，后面的检查价值都会下降。

## 5. 安全与策略就绪性

在 rollout 前尤其要确认：

- 预检查和出口护栏是否存在；
- 策略决策是否能在追踪里看到；
- 高风险动作是否真的需要审批；
- 是否存在绕过网关的直接访问路径；
- 记忆写入是否受策略约束；
- 多租户边界是否在真实场景下验证过。

这里是团队最容易高估自己准备度的地方：策略可能已经写在代码里，但并没有真正嵌进所有关键路径。

对于这个支持场景，最关键的问题是：

> 智能体是否能通过哪怕一条路径，在绕过策略和审计轨迹的情况下创建工单、读取状态，或者写入档案记忆？

如果答案是“能”或“不确定”，那 rollout 还太早。

## 6. 能力就绪性

每个要进生产环境的能力，都值得过一遍简短的运行模板：

- 是否有负责人；
- 传输方式是否明确；
- 是否有超时；
- 是否有重试策略；
- 是否有幂等策略；
- 未知副作用路径是否清楚；
- 结果遥测是否已经接好。

如果一个能力连这个最低标准都没过，那它还不是生产级能力，它只是一个方便的集成。

在这个支持智能体里，`create_support_ticket` 和 `check_access_request_status` 虽然都在同一个目录里，但就绪负担并不一样：

- 读取能力可能在超时和遥测规范后就接近可用；
- 写入能力没有幂等性、结果归一化和清晰回滚故事就还不算就绪。

<div class="diagram-card">
<p>上线就绪性最好理解为多个轮廓的交集，而不是一个总状态灯</p>

``` mermaid
flowchart LR
    A["运行时"] --> H["生产就绪"]
    B["安全"] --> H
    C["能力"] --> H
    D["可观测性"] --> H
    E["评测与 SLO"] --> H
    F["运维就绪性"] --> H
    G["负责人归属与回滚"] --> H
```

</div>

## 7. 可观测性与评测就绪性

非常常见的错误是：系统准备上线了，却想着“正常追踪以后再补”。

进入生产环境前，至少应该确认：

- 每次运行都有 `trace_id`；
- 关键 span 已经存在；
- 策略决策和工具结果可见；
- SLO 已定义；
- 离线评测通过；
- 受影响的高风险路径已单独演练过失败运行演练；
- 这些失败路径仍然能通过追踪链接、发布身份、会话级证据与导出字段（例如 `failure_reason`）保持可追踪；
- 当发布证据依赖评分判断时，验证器质量已被审查；
- 回归门禁已经文档化；
- 在线监控已经为第一波上线做好准备。

否则第一个事故就会变成盲查。

对于这个支持智能体，这一点尤其重要，因为第一批金丝雀租户几乎一定会带来不完美输入。如果团队看不到：

- 智能体到底走了哪条路径；
- 是否发生了重复工具调用；
- 用的 `idempotency_key` 是什么；
- 哪个策略门禁做了决策，

那第一波 rollout 本身就已经变成了彩票。

## 8. 审批路径就绪性

一旦审批被建模成显式运行时路径，rollout 就绪性也必须把这条路径算进去。

团队也许已经在纸面上写好了策略规则，但如果审批造成隐藏队列、负责人归属不清，或者运行会无限期停在 paused 状态，系统依然还没准备好进生产。

在 rollout 前，至少应该检查：

- 审批延迟是否被度量；
- 审批队列是否有负责人；
- 暂停运行是否有超时或过期规则；
- 是否有可见的积压阈值；
- resume/cancel 行为是否明确；
- 人工审查不可用时是否存在回退路径；
- 能力会话过期是否被当成可见 rollout 信号，而不是隐藏传输故障；
- 当有状态能力会话已无法安全 resume 时，重新初始化行为是否已定义。

这对同一个支持智能体会立刻变得重要。如果创建工单的路径会因为审批而暂停，团队就必须知道这次运行会等五秒、三十分钟，还是无限期等待。这不是用户体验细节，而是生产行为的一部分。

一个非常实用的 rollout 门禁是：

> 我们是否知道现在有多少运行正在等待审批，它们已经等了多久，如果没有人在时限内响应系统会做什么，以及当底层能力会话更早过期时运行时又会做什么？

如果答案是否定的，那审批仍然只是一个未被治理的旁路通道。

### 8.1. 有状态能力的中断也必须进入 rollout 就绪性

一旦审批和有状态 MCP 或其他可恢复的能力会话结合在一起，rollout 就绪性就必须把中断语义直接纳入检查。

这意味着团队至少要能回答这些问题：

- 有多少运行正在等待人工审批，同时能力会话仍然存活；
- 有多少运行已经越过能力会话过期，现在需要重新初始化；
- 重新初始化是保留同一个用户可见运行 ID，还是创建新的运营线程；
- 重新初始化之后的下一步是否会触发新的策略决策；
- 遥测能否把原始暂停状态与恢复或重新初始化状态关联起来。

如果这些问题答不上来，rollout 可能在审批层看起来正常，但在能力会话层已经开始退化。

Anthropic 的工作流分类在这里又增加了一个 rollout 维度。[^anthropic] 对于模式感知运行时，编排模式的变化应该被视为承载发布意义的行为，而不是不可见的实现细节。

他们后续关于 harness 设计的工作又把 rollout 含义推进了一步。[^anthropic-harness] 一旦系统依赖 planner/generator/evaluator 分工、sprint 契约，以及跨长时间会话传递的结构化交接工件，rollout 就不能只审查最终给用户看到的输出。团队还必须确认重置、evaluator feedback 与交接工件在数小时执行过程中，是否持续维护着同一个发布契约。

在 rollout 前，团队应该能够明确说出：

- 某条路径现在是否改成了 `routing`，而过去还是固定工作流；
- `parallelization` 是否引入了新的 join-state、duplicate-read 或审批顺序风险；
- `orchestrator-workers` 是否增加了委派 worker 表面、worker-safe 目录或新的审查点；
- `prompt chaining` 是否插入了新的检查点，从而改变 expiry、pause 或重试语义。

这很重要，因为模式变更即使不改变表面功能描述，也会改变生产行为。

对委派授权也是一样。如果运行时支持用户委派访问，那么 rollout 就绪性还应该覆盖：

- 追踪是否保留 `authorization_mode`、委派 principal 与委派 scope；
- 审批记录是否保持与原始运行相同的授权上下文；
- 会话导出是否还能说明动作到底是在谁的委派身份下执行；
- 如果运行正在暂停中而委派访问被撤销，运行时会怎么处理。

否则团队在策略和审批维度上看起来准备好了，但在生产里依然解释不清到底是谁授权了写入路径。

## 9. 运营就绪性

还有一个团队很容易忘记的层：

- 是否有值班负责人；
- 是否已经对 SLO 燃烧和安全事故配好告警；
- 人工回退路径是否清楚；
- 回滚流程是否明确；
- 上线影响范围是否受限；
- 常见失败是否有 runbook。

这听起来像“运维的事”，但没有这一层，系统依然只是实验品，而不是生产级系统。

对于这个支持场景，人工回退路径必须尤其具体：

- 关停智能体后由谁接管流量；
- 怎样停止写入路径；
- 如何标记金丝雀批次中创建的可疑工单；
- 失败 rollout 的后果由谁清理。

## 10. rollout 就绪性的实用规则

如果要把最有用的运营规则压缩成一组，通常这些就够了：

1. 没有追踪覆盖、回滚计划和明确负责人，就不应该开始 rollout。
2. 没有幂等性、结果归一化和策略可见性的写入能力，不应该进入 canary。
3. 高风险流程必须独立于顺畅路径单独验证。
4. 金丝雀、影子和影响半径限制应该是设计的一部分，而不是出事后的临时发挥。
5. 审批队列、暂停运行时长和人工审查积压应该被当成 rollout 信号，而不是看不见的运维噪音。
6. 编排模式选择的变化应该被当成运行时控制变更，并在 rollout 前显式审查。
7. 如果发布证据依赖验证器判断，那么一旦验证器质量或证据链接不再可信，就应先停 rollout。
8. 如果团队已经不再信任追踪、审批处理或评测，就应该先停 rollout，而不是继续“边上边看”。

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

下面这个骨架展示的是：如何把就绪性看成一组必须同时满足的条件。

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

## 13. 上线流程最常见的崩坏点

这些失败模式非常典型：

- 一上来就把 rollout 放给太多流量；
- 团队把追踪当成“非阻塞细节”；
- 负责人归属只存在于文档里，值班机制没准备好；
- 回滚计划实际上只是“出事了再回滚”；
- 能力负责人根本不知道真实发布时间窗；
- 安全回归没被当成阻断项；
- 暂停运行不断累积，因为审批队列没有负责人；
- 审批延迟直到用户已经在等待时才第一次被看见。

对于这个支持智能体，这些问题往往会更危险地表现出来：

- 金丝雀很快变成大范围 rollout；
- 重复工单事故被当成“小集成问题”；
- 记忆写入回归不阻断发布；
- 团队已经不信任自己的 traces，却还在继续 rollout。

一旦这样，rollout 流程就还不是生产级纪律，而只是过于乐观的发布。

## 14. 给 rollout 就绪性做一次快速成熟度测试

团队不应该只因为演示能跑、检查清单看起来大多是绿色、第一波 canary 似乎很小，就觉得自己已经准备好进生产。

更高的标准应该是：

- 高风险路径被独立于顺畅路径单独验证；
- 追踪、策略可见性和回滚在扩大暴露前就值得信任；
- 写入能力具备幂等性和明确的未知结果路径；
- 影响半径是按设计被限制的，而不是靠乐观控制；
- 审批积压、超时与 resume/cancel 行为都被明确规定；
- 负责人归属、值班机制和人工回退路径都足够具体。

如果这些条件大多不成立，那团队也许已经有上线动能，但还没有真正的 rollout 就绪性。

## 15. 读完这一章后先做什么

如果你想在 rollout 前快速判断就绪性，可以先过一遍这个短清单：

1. 是否存在正式的就绪门禁？
2. 这次 rollout 的负责人和值班机制是否明确？
3. 追踪、策略决策和工具结果是否都会进入遥测？
4. 是否有金丝雀/影子阶段？
5. 是否有回滚计划和影响半径限制？
6. 高风险流程是否被单独验证，而不是只测了顺畅路径？
7. 审批是否对暂停运行设有可见的超时/backlog 规则？

如果连续多个答案都是“没有”，那这次 rollout 就应该视为未准备好，即使演示看起来很顺。

## 16. 接下来读什么

到这里，参考实现已经闭合了同一个支持智能体及其平台最基本的运行骨架。下一步就是生命周期纪律：如何变更、发布、调查和下线这样的系统，同时不丢掉控制力。

## 17. 值得配套阅读的参考页

- [Trace Schema 与 Event Catalog](../../appendix/trace-schema.zh.md)
- [Policy Bundle Schema 与 Approval Contract](../../appendix/policy-bundle-schema.zh.md)
- [Lifecycle Artifact Schema](../../appendix/lifecycle-artifact-schema.zh.md)

这一章把第 17 章里的受治理运行时路径变成 rollout 纪律。相同的审批、pause/resume 与控制信号，接下来会在第 21 章里继续作为保证回路的一部分出现。

- [第 17 章：策略层与能力目录](chapter-17.zh.md)
- [第七部分：参考实现](index.zh.md)
- [第八部分：智能体系统的生命周期](../part-viii/index.zh.md)
- [参考来源](../../appendix/sources.zh.md)

[^anthropic]: [Anthropic, Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
[^moffatt]: American Bar Association, [BC Tribunal Confirms Companies Remain Liable for Information Provided by AI Chatbot](https://www.americanbar.org/groups/business_law/resources/business-law-today/2024-february/bc-tribunal-confirms-companies-remain-liable-information-provided-ai-chatbot/)
[^anthropic-harness]: Anthropic, [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps).
