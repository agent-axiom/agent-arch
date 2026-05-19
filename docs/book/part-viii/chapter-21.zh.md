# 第 21 章：保障闭环：红队测试、检测与响应

!!! info "时效说明"
    最近一次编辑审查：**2026 年 5 月 17 日**。上一次审查：**2026 年 5 月 14 日**。下一次计划审查：**2026 年 6 月 17 日**。

    自上次审查以来的变化：MCP/A2A 安全面、验证器契约、治理感知遥测以及出版就绪问题，已经被明确列为近期编辑任务。

    变化最快的部分：

    - 红队技术、场景生成器和自动化攻击脚手架；
    - 各家平台围绕智能体系统提供的保障与检测建议；
    - 对行为类发现的分类和优先级实践。

    变化相对较慢的部分：

    - 保障必须是持续闭环，而不是一次性评审；
    - 发现需要进入带负责人、修复和回滚逻辑的待办队列；
    - 事故、检测、重新设计和 rollout 规则变更之间必须闭环。

## 1. 为什么生命周期不会在发布门禁处结束

到这里为止，我们已经有了一幅更成熟的图景：

- 智能体系统已经进入 ADLC；
- 变更会经过变更管理；
- 发布不再是盲目推进。

但这仍然不够。

因为智能体系统有一类特别的风险：

- 涌现行为；
- 通过提示或工具路径发生的滥用；
- 长流程中的漂移；
- 隐蔽的策略绕过；
- 不安全的副作用；
- 团队发现得太晚的退化。

所以在发布纪律之外，还必须再补上一层：保障闭环。

这里有一个关键区分：评测闭环负责帮助团队判断系统行为是在变好还是变坏；保障闭环负责决定应该立刻遏制什么、谁来响应，以及当新风险出现时怎样强制把系统拉回到更安全的状态。

这意味着，本章正是从那些预算设定章节收尾的地方开始。SLO 定义可容忍的健康预算与风险预算；保障则在这些预算受到威胁、已经失守，或者已经不再值得信任时开始要求团队采取行动。

这也正是本章的核心承诺。它要帮助读者把保障看成整个生命周期里的响应函数，而不是一组松散的安全活动：在这里，信号会被转化成遏制、负责人归属、修复，以及把系统强行带回更安全运行状态的动作。本章的主要工件是 finding and response record：一条把信号、风险、负责人、临时遏制、修复和关闭条件连在一起的记录。

如果你想看一页专门把请求、策略、审批、追踪、评测、事故和 rollout 判断串成同一条可复核链路的桥接页，可以直接打开 [Evidence Spine](../part-v/evidence-spine.zh.md)。

## 2. 什么是保障闭环

可以这样定义保障闭环：

它是一套持续运行的循环，帮助团队不只是发布变更，还能系统性地发现薄弱点、察觉新威胁、调查问题并把问题真正关掉。

在智能体系统里，它通常包括：

- 红队测试；
- 漏洞管理；
- 检测与响应；
- 修复；
- 把经验重新写回设计和发布流程。

Google Research 在这里给出的核心观点很清楚：生成式系统的安全保障应该是一种持续能力，而不是一次性的审查活动。[^google-assurance]

## 3. 红队测试应该针对真实失效模式，而不是演示效果

太多团队把红队测试做成了展示：

- 试几个明显的越狱提示；
- 展示系统“扛住了一些东西”；
- 然后就觉得问题结束了。

这不是强保障。

对智能体系统有价值的红队测试，应该针对与生产环境相关的失效模式：

同时，也应该单独测试验证器层，尤其是在团队依赖自动评分或计算机使用轨迹裁判时。薄弱的验证器可能把不安全行为误判成安全，也可能把环境导致的失败放大成嘈杂的误报。

- 提示注入；
- 隐蔽指令覆盖；
- 工具滥用；
- 不安全的出口访问；
- 审批绕过；
- 跨租户检索泄漏；
- 记忆污染；
- 过度自主性。

好的红队测试不只看模型回答，还要看整个执行路径。

这也是失败运行演练应该被放进这里的原因。超时、验证失败，或者上游依赖故障场景，不只是 rollout 工件，也是一种保障场景，因为团队必须知道退化行为在压力下是否仍然可复核、可遏制、可归因，包括通过像 `failure_reason` 这样的明确字段。

## 4. 漏洞应该进入待办队列，而不是停留在感受里

如果红队测试只留下“这里感觉有点危险”的印象，团队很难高质量行动。

更成熟的方式是把它放进正常的漏洞工作流：

- 到底发现了什么；
- 风险等级是什么；
- 利用路径是什么；
- 什么算修复；
- 负责人是谁；
- 修复截止时间是什么；
- 是否需要临时缓解措施。

这是一个很典型的 SDLC 式逻辑：发现结果必须成为可管理的工程对象，而不是工作坊之后的印象笔记。

!!! example "贯穿案例：重复复现后的 finding"
    如果红队演练通过超时和重试再次复现了重复工单，这不是“有意思的观察”，而是一个受管理的 finding。记录里应该包含利用路径、受影响能力 `create_support_ticket`、风险等级、负责人、approval-only mode 这样的临时缓解、针对重复 outcome 增长的检测规则，以及修复截止时间。只有在更新后的 [eval](../../appendix/eval-schema.zh.md)、策略门和已确认的 [traceable outcome](../../appendix/trace-schema.zh.md) 都通过之后，保障闭环才算关闭这个 finding。

**Assurance case-spine note：**[finding and response record](../../appendix/incident-record-schema.zh.md) 应该通过不同 containment paths 闭合三个 canonical cases。Support triage 连接 duplicate-outcome detection、[approval-only containment](../../appendix/approval-schema.zh.md)、`create_support_ticket` owner、updated eval 和 traceable outcome。Internal knowledge assistant 连接 [retrieval-poisoning signal](../../appendix/memory-retrieval-schema.zh.md)、source-grounding review、tenant-boundary containment、[memory-write quarantine](../../appendix/memory-retrieval-schema.zh.md) 和 freshness remediation。Incident coordination 连接 escalation abuse signal、notification throttling、responder-role owner、[incident-state rollback](../../appendix/incident-record-schema.zh.md) 和 [post-incident control update](../../appendix/lifecycle-artifact-schema.zh.md)。

## 5. 检测不能只盯着错误率

在普通服务里，检测常常围绕错误率、延迟和基础设施信号展开。对智能体系统来说，这远远不够。

你还需要能看到：

- 验证器在不安全轨迹上的假阳性峰值；
- 验证器在被阻断但正确的轨迹上的假阴性峰值；

- 被拒动作的异常增长；
- 审批积压；
- 卡住的暂停审批或异常偏大的暂停运行时长；
- 能力会话过期的异常升高；
- 有状态能力路径中无法解释的重新初始化率上升；
- 运行与审批记录之间的委派 principal 不匹配；
- 超出预期暂停/恢复规则的委派 scope 复用；
- 已撤销授权仍然抵达执行的情况；
- 异常的工具选择模式；
- 新出现的出口目标；
- 记忆写入异常；
- 不安全回退行为的上升；
- 任务成功率和安全指标的漂移；
- 陈旧后台运行；
- 预期载荷形态与实际观测形态之间的契约漂移；
- 编排模式回归，例如意外的路由路径漂移、不稳定的 join-state 行为，或超出已评审边界的委派 worker 活动；
- 验证器漂移，例如它在过程质量、结果质量或失败归因上与人工评审失去一致性；
- 未经评审的 rollout 控制下的验证器契约版本变更，它们会悄悄改变评分行为。

也就是说，这里的检测既是可观测性，也是滥用与安全监测。

这也是本章必须和可观测性层保持边界的地方。可观测性提供证据基底；保障决定哪些信号此刻重要、哪些信号要触发遏制，以及哪个负责人必须行动。

它也必须和 SLO 保持边界。SLO 说明还能容忍多少退化或不安全行为；保障则是在这种容忍度不再可接受时，负责升级、遏制并分配响应责任的闭环。

## 6. 响应应该是一层独立的运行能力

当一个智能体开始表现出危险行为时，光说“之后再调提示”是不够的。

更实用的响应层应该围绕具体动作来设计：

- 限制能力；
- 把动作切到仅审批模式；
- 取消或使卡住的暂停运行过期；
- 对陈旧执行的路由暂停后台模式；
- 收紧出口策略；
- 关闭高风险记忆写入；
- 冻结有状态能力路径的重新初始化；
- 把发布波次切回更安全的配置；
- 必要时直接停用有问题的路由。

同一层响应层也必须把运行时失败路径当成独立的受治理事件来处理。工具超时、验证失败，或者上游依赖不可用，都不该被塞进笼统的 “运行已完成” 话术里。系统应该记录失败运行、保留追踪，并让会话级证据与 `latest_failure_reason` 这样的面向操作员摘要中同时持续保留这个结果以及具体失败原因，例如放在 `failure_reason` 中，同时让这次运行继续计入 `traceable_failed_runs`，这样保障才能区分被拦下来的风险、基础设施退化，以及运行时控制行为本身的失效。

这很关键，因为在智能体系统里，响应往往必须比完整的根因分析更快发生。

所以这里的保障更应该被理解成响应函数，而不只是检测目录。它的职责，是尽量缩短信号与安全遏制之间的时间。

预算可以告诉你系统现在已经不健康了；保障则告诉你，谁来冻结路由、谁来收紧控制面，以及谁负责把系统带回安全状态。

<div class="diagram-card">
<p>保障闭环更像一个连续循环：发现、检测、遏制、修复、学习</p>

``` mermaid
flowchart LR
    A["红队测试与事故"] --> B["发现"]
    B --> C["检测规则与监控"]
    C --> D["响应动作"]
    D --> E["修复"]
    E --> F["更新后的策略、评测和 rollout 规则"]
    F --> A
```

</div>

## 7. 修复应该改变系统，而不只是增加文档

很常见的一种弱点是：事故被复盘了，文档也写了，但系统本身几乎没变。

更强的修复通常会真正修改至少一个运营表面：

- 验证器评分规则、验证器契约版本或评分契约；

- 策略规则；
- 审批阈值；
- 工具暴露；
- 记忆写入约束；
- 评测数据集；
- rollout 门禁；
- 告警和检测规则。

如果修复没有改变这些层，说明系统其实没学到多少东西。

## 8. 用户报告和事故必须回流到保障闭环

另一个很重要的实践点是：保障闭环不能只依赖团队内部演练。

新的失败模式还会来自：

- 生产追踪；
- 用户投诉；
- 审批队列异常；
- 陈旧后台运行报告；
- 能力会话过期告警或重新初始化异常；
- 委派授权不匹配告警；
- 契约不匹配告警；
- 编排模式漂移告警；
- 复盘；
- 在线评测漂移；
- 红队发现；
- 验证器回归、验证器契约版本变更，或与人工评审的分歧。

这些信号应该重新流回：

- 评测数据集；
- 安全检查；
- 变更分类；
- rollout 策略。

否则团队会一遍又一遍撞上同样的意外。

但这里的第一责任仍然是运行责任，而不是研究责任：一旦某个信号足够可信，系统就必须知道谁拥有响应，以及在更深层重新设计开始之前允许采取哪些遏制动作。

## 9. 好的保障闭环一定和负责人归属绑定

没有负责人归属，保障很快就会散掉。

最好提前明确：

- 谁维护红队待办队列；
- 谁分诊发现；
- 谁负责缓解措施；
- 谁能紧急停用能力；
- 谁判断修复已经足够；
- 谁更新监控和响应规则。

这一点和本书的组织模型部分完全一致：安全纪律最容易坏在负责人不清楚的地方。

## 10. 一个保障策略示例

下面这个骨架很实用：

```yaml
assurance:
  red_team:
    cadence: monthly
    required_surfaces:
      - prompt_injection
      - tool_misuse
      - memory_poisoning
      - egress_abuse
      - paused_approval_saturation
      - capability_session_expiry_regression
      - reinit_control_drift
      - delegated_authorization_mismatch
      - orchestration_pattern_regression
      - contract_drift
      - verifier_contract_drift
  findings:
    require_owner: true
    require_severity: true
    require_remediation_due_date: true
    require_verifier_review_for_high_risk: true
  response:
    emergency_actions:
      - disable_capability
      - require_approval
      - restrict_egress
      - disable_memory_write
      - expire_paused_runs
      - suspend_background_route
      - freeze_reinitialization
      - revoke_delegated_authorization
```

它不是完整框架，但足以说明保障也可以被组织成明确的运营契约。

如果发布或训练决策依赖验证器，这个契约也应该把验证器本身纳入其中。

## 11. 一个紧急响应决策示例

下面这个代码片段表达的是同一个思路：

```python
from dataclasses import dataclass


@dataclass
class AssuranceSignal:
    unsafe_egress_detected: bool = False
    memory_poisoning_suspected: bool = False
    approval_bypass_detected: bool = False
    paused_approval_saturation: bool = False
    capability_session_expiry_regression: bool = False
    reinit_control_drift: bool = False
    stale_background_runs: bool = False
    contract_drift_detected: bool = False


def emergency_action(signal: AssuranceSignal) -> str:
    if signal.unsafe_egress_detected:
        return "restrict_egress"
    if signal.approval_bypass_detected:
        return "require_approval"
    if signal.capability_session_expiry_regression or signal.reinit_control_drift:
        return "freeze_reinitialization"
    if signal.paused_approval_saturation:
        return "expire_paused_runs"
    if signal.stale_background_runs:
        return "suspend_background_route"
    if signal.contract_drift_detected:
        return "disable_capability"
    if signal.memory_poisoning_suspected:
        return "disable_memory_write"
    return "observe"
```

重点在于：响应决策不应该完全依赖临场发挥，而应该属于预先设计好的运营表面。

## 12. 最常见的断裂点

这些问题会反复出现：

- 红队测试和工程待办队列脱节；
- 发现没有负责人；
- 事故从不进入评测数据集；
- 检测只看延迟和错误；
- 暂停审批饱和在运营里可见，却没有被当成保障信号；
- 编排模式回归往往要等运行时行为在生产环境里漂移之后才会被发现；
- 陈旧后台运行悄悄累积；
- 契约漂移只有在运行时失败扩散后才被发现；
- 响应动作太粗或太慢；
- 修复没有真正改变系统。

一旦这样，保障闭环就会变成一套漂亮的演示文稿，而不是防护机制。

## 13. 给保障闭环做一次快速成熟度测试

团队不应该只因为做过几次红队演练、记下了几个发现，就宣称自己已经有保障。

更高的标准应该是：

- 发现会变成有负责人的工程对象；
- 检测寻找的是不安全行为，而不只是错误和延迟；
- 暂停审批、能力会话生命周期回归、编排模式回归、陈旧后台运行与契约漂移都被当成真实保障信号；
- 响应动作在下一次事故之前就已经存在，而不是事后才补；
- 修复会改变运行系统，而不只是文档痕迹；
- 事故会回流进评测、策略和 rollout 规则。

如果这些条件大多不成立，那团队也许已经有一些安全活动，但还没有真正的保障闭环。

## 14. 实用检查清单

如果你想快速判断保障纪律是否成形，可以问：

- 红队测试是不是定期进行，而不是一次性演练？
- 发现是否以工程待办项的形式被追踪？
- 除了基础设施健康，是否还有针对不安全行为、暂停审批饱和和陈旧后台运行的监控？
- 在不完全关停的情况下，是否有快速紧急动作，包括让暂停运行过期或暂停某条后台路由？
- 事故会不会回流到评测和 rollout 规则？
- 检测、响应和修复的负责人是否清楚？

如果连续几个问题的答案都是“否”，那你现在可能只有安全意图，还没有保障闭环。

## 15. 接下来读什么

在保障闭环之后，最自然的下一步就是供应链纪律和已批准工件。因为只要系统持续变化、持续调查、持续修复，你就必须非常清楚：哪些工件才算可信，哪些东西真正进入过生产环境。

## 16. 值得配套阅读的参考页

- [Trace Schema 与 Event Catalog](../../appendix/trace-schema.zh.md)
- [Policy Bundle Schema 与 Approval Contract](../../appendix/policy-bundle-schema.zh.md)
- [Eval Dataset Schema 与 Grading Contract](../../appendix/eval-schema.zh.md)
- [Lifecycle Artifact Schema](../../appendix/lifecycle-artifact-schema.zh.md)
- [Change Review and Rollout Gate Schema](../../appendix/change-rollout-schema.zh.md)

这一章把第 17 章和第 18 章打开的回路真正闭合起来。那两章里策略、审批与运行时控制路径先被做成显式结构，而在这里，这些同样的路径会变成检测、遏制和响应表面。

- [第 20 章：智能体系统的变更管理](chapter-20.zh.md)
- [第 14 章：平台团队与产品团队](../part-vi/chapter-14.zh.md)
- [第 18 章：生产上线检查清单](../part-vii/chapter-18.zh.md)
- [参考来源](../../appendix/sources.zh.md)

[^google-assurance]: [Google Research, Security Assurance in the Age of Generative AI](https://research.google/pubs/security-assurance-in-the-age-of-generative-ai/)
