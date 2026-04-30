# 第 17 章：策略层与能力目录

!!! info "怎样读这一章"
    不要把这一章当成抽象的策略层讨论，更有用的是抓住一个很实际的问题：

    - 谁来决定同一个支持智能体的这次运行到底能不能启动；
    - 谁来决定它能不能读上下文、开工单、写入记忆；
    - 这些决定应该放在哪里，才能不散进编排代码。

    如果这些答案都藏在零散的代码分支里，说明运行时虽然已经有了，但系统的契约核心还没有真正搭起来。

## 1. 为什么没有策略层的参考运行时仍然过于天真

即使你已经有一个干净的运行时回路，这依然不够。没有显式的策略层，系统仍然过于信任环境：

这正是本章的独特承诺。它应该帮助读者看清运行时的契约核心真正在哪里，也说明为什么一个可运行系统在可允许性、风险与能力控制仍然藏在编排代码里时，依然算不上成熟。

在贯穿全书的支持场景里，这一点在第 16 章之后立刻就会出现。运行时已经能接收请求、拼上下文、调用模型，并走到网关。可一旦智能体准备开紧急工单、把摘要写进记忆，或者继续请求下一步外部动作，系统需要的就不只是回路，而是对可允许性与风险的明确判断。

- 无法可靠地区分允许的运行和不允许的运行；
- 工具调用很难被一致地控制；
- 记忆写入靠零散约定存在；
- 产品特定限制会很快渗进编排代码。

所以，参考实现里的下一个必需层就是策略层。

它的目标不是“拖慢系统”，而是让访问、风险和可允许性的决定不再散落在随机的 `if` 分支里。

因此，本章最好不要只被读成一章关于策略页面的说明，它也应该被读成一章关于受治理决策的说明。问题不在于团队有没有把一些规则写下来，而在于运行时是否终于拥有了一个可审查的契约核心，能够解释为什么某次运行被允许、被暂停、被拒绝、被收窄，或被升级处理。

如果你想看这种受治理策略决策之后如何继续连接到追踪、审批、评测判断、事故和 rollout，可以直接打开单独的 [Evidence Spine](../part-v/evidence-spine.zh.md) 页面。

!!! info "需要契约层的配套页面？"
    如果你想直接看更落地的工程形式，可以打开 [Policy Bundle Schema 与 Approval Contract](../../appendix/policy-bundle-schema.zh.md)、[Approval Request 与 Decision Record Schema](../../appendix/approval-schema.zh.md) 和 [参考运行时包](../../appendix/reference-package.zh.md)。

## 2. 策略层应该回答小而清晰的问题

弱的策略层总想成为“系统的大脑”。强的策略层恰好相反：它只解决一组有限而清晰的问题。

例如：

- 这次运行能不能开始；
- 这段上下文能不能读；
- 这个能力能不能调用；
- 是否需要审批；
- 这段内容能不能写入记忆；
- 这个结果能不能向外返回；
- 当高风险 rollout 或保证依赖评分证据时，哪些验证器契约可以被信任。

当这些问题被明确表达出来后，运行时会更容易解释，护栏的修改也不再混乱。

## 3. 能力目录不是名字列表，而是契约层

很容易把目录做成“可用工具列表”。但好的目录要做得更多：

- 描述能力契约；
- 保存风险画像；
- 声明传输与执行模式；
- 记录幂等预期；
- 固定负责人归属和生命周期。

所以能力目录不是“为了方便的清单”，而是平台能力的中心控制点。

<div class="diagram-card">
<p>策略层与能力目录一起构成参考实现的契约核心</p>

``` mermaid
flowchart LR
    A["运行请求"] --> B["运行时编排器"]
    B --> C["策略层"]
    B --> D["能力目录"]
    C --> E["允许 / 拒绝 / 审批"]
    D --> F["能力契约"]
    E --> G["执行层"]
    F --> G
```

</div>

## 4. 工具表面不等于受治理能力表面

OpenAI 最近关于工具使用的材料有一个很有用的区分，而很多团队在实践里会把它混掉：模型也许能看到工具、MCP 服务器、托管能力或本地函数，但运行时仍然必须决定这些东西究竟属于哪一种控制面。[^openai-tools]

这个区分很重要。

弱实现会说：

- 这里有一张模型可调用的工具列表。

更强的实现会说：

- 这里是受治理能力表面；
- 其中哪一部分会暴露给模型；
- 执行通过哪一种传输走；
- 哪些能力可以直接调用，哪些必须通过网关 broker，哪些根本不暴露。

这就是为什么能力目录必须放在原始工具定义之上。它防止运行时混淆：

- 模型可以提到什么；
- 运行时可以路由什么；
- 平台真正愿意执行什么。

## 5. 能力目录里值得存什么

一旦平台开始接入类似有状态 MCP 能力，目录就不能只描述传输和风险，还必须帮助运行时判断：这个能力是无会话、绑定会话、可中断，还是可以跨多轮恢复。

因此，更成熟的目录往往还需要补充这类字段：

- 能力会话模式：`stateless/stateful`；
- 是否允许 elicitation；
- 是否会发出进度事件；
- 会话过期的处理方式；
- 恢复是否需要新的审批，还是可以沿用现有决策；
- 能力是否允许自动重新初始化远端会话。

如果没有这些字段，策略层可能在原则上批准了某个能力，却仍然无法治理它在真实运行时会话中的行为。

Anthropic 的工作流分类又补上了一个缺失的治理维度。[^anthropic] 策略层不应该只决定某个能力单独看来能不能用，它还应该决定这个能力可以出现在什么编排模式里。

他们后续关于 harness 设计的工作又补上一层密切相关的经验：一旦系统通过 planner、generator、evaluator 这些角色在长时间任务上协作，策略要治理的就不再只是某一次 tool call，而是这个工具调用周围的 **角色契约**。[^anthropic-harness] 如果 generator 提出 sprint，evaluator 负责打分，而 planner 重新塑造 scope，那么平台就需要明确规则，规定谁可以定义完成标准，谁可以评估质量，谁有权触发 reset，以及在上下文重置之后哪份交接工件才算权威。

例如，策略契约可能需要明确说明一个 capability：

- 可以安全地用于 `prompt chaining`，但不能用于 unconstrained loop；
- 只允许在 `routing` 的某些请求类别里被调用；
- 只有在各分支都是 read-only 时，才允许放进 `parallelization`；
- 是否允许被 `orchestrator-workers` 里的委派 worker 调用，还是只允许 parent runtime 调用。

这样能力治理才会绑定到运行时形态上，而不是假装同一个工具契约在任何执行模式里都同样安全。

一个实用的字段集合通常包括：

- 能力名称；
- owner；
- mode: read/write/high_risk；
- transport: mcp/gateway/sandboxed_exec；
- exposure: direct/brokered/restricted；
- 输入 schema；
- output shape；
- 审批要求；
- 幂等要求；
- 超时和重试默认值。

有了这样的契约，运行时才能以可预测的方式运行，而不是对每个能力临时适配。

## 6. 审批应该表现成可中断运行时路径，而不是旁路的人类对话

当审批被建模为运行时控制流的一部分，而不是系统外部的手工流程时，策略层才会真正落地。LangGraph 的 interrupts 模型在这里很有用，因为它把 pause、审查与 resume 变成了显式运行时基础件，而不是临时人工补丁。[^langgraph-interrupts]

这也是策略密集型智能体系统更合理的形状。

当一个高风险能力走到审批边界时，运行时应该能够：

- 暂停这次运行；
- 暴露待处理动作及其上下文；
- 等待外部决策；
- 用结构化结果恢复执行。

这比“给操作员发条消息，然后希望外围代码还记得自己停在哪”强得多。

进一步看，最好把审批分成两种模式：

- 面向少量真正高风险动作的直接人工审批；
- 面向重复性、低上下文决策的分类器介导的审批路径，用来减少人工审查带来的审批疲劳。

第二种路径不该被理解成“去掉审批”，而应被理解成委派控制，只是它需要更严格的证据：

- 是哪个分类器或门禁做出的判断；
- 它当时看到了什么证据；
- 在什么条件下必须升级给人工；
- 子智能体或后续动作如何继承这种委派审批，或者在什么条件下失效；
- 当 rollout 或 assurance 依赖验证器输出时，哪些验证器契约可以被信任来给这些高风险路径分级。

## 7. 策略决策应该是对象，而不只是 bool

一个很有用的工程习惯：不要把策略决策简化成 `True/False`。

通常更有用的是返回类似：

- `allow`
- `deny`
- `approval_required`
- `sanitize_and_continue`
- `escalate`

以及额外信息：

- 原因代码；
- 策略 ID；
- 风险类别；
- 可选约束；
- allowed 编排模式或明确的 pattern restrictions；
- 面向高风险路径的可信验证器契约或验证器契约要求；
- 必要时还包括审批或恢复要求。

这会大幅提升可解释性，也让遥测更有价值。

## 8. 一个策略契约示例

下面是一个非常简单但实用的模板：

```yaml
policy:
  run_precheck:
    require_tenant: true
    deny_if_principal_missing: true
  capabilities:
    search_docs:
      decision: allow
    create_ticket:
      decision: approval_required
      approver: manager
    run_shell:
      decision: deny
  memory_write:
    allow_kinds:
      - validated_fact
      - session_summary
```

它的价值不在完整，而在显式。你可以围绕具体规则讨论，并且知道它到底应用在什么地方。

随着验证器感知治理成为生产模型的一部分，这种显式性也应该扩展到验证器信任。高风险路径不应依赖“碰巧存在的某个 verifier”。策略层应该能明确说明哪些验证器契约是 trusted 的、什么时候必须要求它们，以及如果发布路径中出现不可信验证器契约应该怎么办。

## 9. 一个能力目录契约示例

你可以把目录大致设计成这样：

```yaml
capabilities:
  search_docs:
    owner: knowledge_platform
    mode: read
    transport: mcp
    exposure: direct
    timeout_seconds: 5
    approval: none
  create_ticket:
    owner: support_platform
    mode: write
    transport: gateway
    exposure: brokered
    timeout_seconds: 15
    approval: manager
    idempotency_key_required: true
  run_shell:
    owner: platform_runtime
    mode: high_risk
    transport: sandboxed_exec
    exposure: restricted
    timeout_seconds: 10
    approval: always
```

这样的目录已经在定义运行语义，而不只是能力名称。它还明确了某个能力是面向模型、由运行时代理，还是仅供操作员使用。

## 10. 结构化输出很重要，因为契约必须在接触代码后仍然成立

对有状态能力流来说，这一点会更加严格。如果审批、暂停/恢复、会话过期和重新初始化决策都只写在散文说明里，运行时就无法安全判断：自己是在继续同一个受治理的会话，还是无意中打开了一个新的会话。

因此，策略工件最好逐步把这些字段也结构化下来：

- `capability_session_id`
- `capability_session_mode`
- `resume_policy`
- `on_session_expiry`
- `progress_event_policy`
- `elicitation_policy`

这些字段可以帮助运行时把审批控制和能力会话控制放进同一套模型里，而不是任由它们漂移成两套隐含系统。

随着审批系统继续成熟，契约往往还需要补充分类器支持的审批控制的字段，例如：

- `approval_mode`
- `approval_delegate`
- `classifier_verdict`
- `escalate_to_human_if`
- `subagent_handoff_policy`

这些字段能让委派审批路径变成显式的运行时契约，而不是藏在产品逻辑或界面行为里。

同样的纪律也应该延伸到委派 worker。如果 runtime 支持 `orchestrator-workers` 路径，策略层应该能够明确说明：

- worker 是否继承 parent 的审批上下文；
- 委派审批是否会在交接边界失效；
- worker 是否可以请求额外能力，还是只能使用 worker-safe 子集；
- 在任何写入能力被执行之前，worker 输出是否必须先经过审查。

同样的纪律也应该延伸到身份边界。如果某个能力通过 MCP 或其他 brokered 传输使用委派用户授权，那么策略层也应该能明确说明：

- 访问到底是平台拥有还是用户委派；
- 委派作用域在暂停运行之后能否继续复用；
- 被撤销授权会触发 cancel、re-approval 还是 re-initialization；
- 子智能体是否可以继承同一份委派授权上下文。

这样委派审批和委派授权才能留在同一套受治理契约模型里，而不会演变成彼此无关的例外。

现在参考运行时也已经把这些假设直接带进执行工件：`run_start`、`approval_requested`、`tool_execution`、`run_complete`、审批记录和会话导出都可以保留同一份委派授权上下文。这样 rollout 和事故调查就不需要再从侧面线索里反推委派身份。

OpenAI 最近关于结构化输出的材料，对策略层也很有帮助。[^openai-structured]

如果运行时仍然需要猜测策略结果、审批请求或能力载荷是否按预期形态返回，那么契约其实只完成了一半。

所以对策略密集型系统来说，下面这些关键工件最好都做成结构显式：

- 策略决策；
- 审批请求；
- 审批结果；
- 能力输入与输出。

目的不是为了形式优雅，而是为了减少运行时逻辑、审计记录和周边控制面之间的静默漂移。

## 11. 一个简单的策略决策骨架

重点在于：运行时拿到的不只是“准不准”，而是结构化决策。

```python
from dataclasses import dataclass


@dataclass
class PolicyDecision:
    action: str
    reason: str
    policy_id: str
    approval_mode: str = "human"
    escalate_to_human: bool = False
    requires_approval: bool = False


def evaluate_capability(name: str) -> PolicyDecision:
    if name == "search_docs":
        return PolicyDecision(action="allow", reason="low_risk_read", policy_id="cap_001")
    if name == "create_ticket":
        return PolicyDecision(action="approval_required", reason="write_action", policy_id="cap_014", requires_approval=True)
    return PolicyDecision(action="deny", reason="unsupported_capability", policy_id="cap_999")
```

即使这么简单的代码，也已经给遥测、审批界面流和事后调查提供了正确的形状。

## 12. 一个简单的能力查找骨架

再来一个很实用的点：运行时不应该直接知道能力细节，而应该从目录中取。

```python
from dataclasses import dataclass


@dataclass
class CapabilitySpec:
    name: str
    mode: str
    transport: str
    exposure: str
    timeout_seconds: int


def get_capability(name: str) -> CapabilitySpec | None:
    registry = {
        "search_docs": CapabilitySpec("search_docs", "read", "mcp", "direct", 5),
        "create_ticket": CapabilitySpec("create_ticket", "write", "gateway", "brokered", 15),
    }
    return registry.get(name)
```

这同样看起来很“无聊”。很好。目录层本来就应该无聊、稳定、可审阅。

## 13. 常见错误

这些问题非常常见：

- 策略规则散落在运行时代码各处；
- 能力契约不完整；
- 暴露给模型的工具被误当成自动获批的能力；
- 能力负责人归属不清晰；
- 审批逻辑直接嵌进编排；
- 审批虽然存在，但没有被建模成运行时内显式的暂停/恢复路径；
- 缺少结构化契约，导致策略与审批载荷在形态上逐渐漂移；
- 记忆策略和执行策略好像互不相干；
- 目录和真实适配器的行为逐渐漂移。

一旦这样，参考实现就不再是参考，而是又退回成一堆约定。

## 14. 给策略层和能力目录做一次快速成熟度测试

团队不应该只因为已经有几条策略检查和一张工具列表，就觉得自己已经搭好了智能体系统的契约核心。

更高的标准应该是：

- 策略决策是显式对象，而不是散落的布尔值；
- 能力契约携带负责人归属、传输、暴露方式、风险和审批语义；
- 运行时代码依赖目录，而不是直接调用和临时例外；
- 审批被建模成显式可中断路径，而不是流程外的人工绕路；
- 记忆策略、执行策略和审批策略属于同一个可见的控制面；
- 遥测不只展示发生了什么，还能展示是哪条策略和哪个能力契约在起作用。

如果这些条件大多不成立，那运行时也许已经存在，但契约核心还没有真正搭起来。

## 15. 现在就该做什么

先过一遍这份短清单，把所有回答为“否”的地方单独记下来：

- 你有没有独立的策略层，而不是一堆散落的 `if`？
- 策略返回的是不是结构化决策？
- 你有没有统一的能力目录？
- 能力是否拥有负责人、传输、暴露方式和风险语义？
- 运行时是否使用目录，而不是直接调用？
- 审批能否显式暂停并恢复一次运行？
- 策略决策是否能在遥测里看到？

如果连续多个答案都是“没有”，那说明骨架已经有了，但契约核心还没真正搭起来。

## 16. 下一步做什么

先把策略决策和能力契约固定下来，再检查同一套系统是否已经准备好首次 rollout。

参考实现的下一步很自然：组装生产 rollout 检查清单，把蓝图和契约核心变成一个真正可落地的上线框架。

- [第 16 章：基础运行时蓝图](chapter-16.zh.md)
- [第 18 章：生产上线检查清单](chapter-18.zh.md)
- [第七部分：参考实现](index.zh.md)
- [参考来源](../../appendix/sources.zh.md)

[^anthropic]: [Anthropic, Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
[^openai-tools]: [OpenAI, Using tools](https://developers.openai.com/api/docs/guides/tools)
[^langgraph-interrupts]: [LangGraph, Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)
[^openai-structured]: [OpenAI, Structured model outputs](https://developers.openai.com/api/docs/guides/structured-outputs)

## 17. 值得配套阅读的参考页

- [Policy Bundle Schema 与 Approval Contract](../../appendix/policy-bundle-schema.zh.md)
- [Lifecycle Artifact Schema](../../appendix/lifecycle-artifact-schema.zh.md)
- [Reference Package](../../appendix/reference-package.zh.md)

这一章是整个运行时控制集群的契约枢纽。最值得继续看的下一步，是第 18 章里把这些路径变成 rollout 门禁，以及第 21 章里把同样的审批与策略路径变成保证响应。

- [第 16 章：基础运行时蓝图](chapter-16.zh.md)
- [第 18 章：生产上线检查清单](chapter-18.zh.md)
- [第七部分：参考实现](index.zh.md)
- [参考来源](../../appendix/sources.zh.md)

[^anthropic-harness]: Anthropic, [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps).
