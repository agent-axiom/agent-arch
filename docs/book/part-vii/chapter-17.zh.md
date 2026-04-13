# 第 17 章：策略层与能力目录

!!! info "怎样读这一章"
    不要把这一章当成抽象的 policy layer 讨论，更有用的是抓住一个很实际的问题：

    - 谁来决定同一个 support agent 这个 run 到底能不能启动；
    - 谁来决定它能不能读上下文、开工单、写入 memory；
    - 这些决定应该放在哪里，才能不散进 orchestration code。

    如果这些答案都藏在零散的代码分支里，说明 runtime 虽然已经有了，但系统的 contract core 还没有真正搭起来。

## 1. 为什么没有策略层的 reference runtime 仍然过于天真

即使你已经有一个干净的 runtime loop，这依然不够。没有显式的策略层，系统仍然过于信任环境：

在贯穿全书的 support 场景里，这一点在第 16 章之后立刻就会出现。runtime 已经能接收请求、拼上下文、调用模型，并走到 gateway。可一旦智能体准备开紧急工单、把摘要写进 memory，或者继续请求下一步外部动作，系统需要的就不只是 loop，而是对可允许性与风险的明确判断。

- 无法可靠地区分允许的 run 和不允许的 run；
- tool calls 很难被一致地控制；
- memory writes 靠零散约定存在；
- 产品特定限制会很快渗进 orchestration code。

所以，参考实现里的下一个必需层就是 policy layer。

它的目标不是“拖慢系统”，而是让访问、风险和可允许性的决定不再散落在随机的 `if` 分支里。

!!! info "需要契约层的配套页面？"
    如果你想直接看更落地的工程形式，可以打开 [Policy Bundle Schema 与 Approval Contract](../../appendix/policy-bundle-schema.zh.md)、[Approval Request 与 Decision Record Schema](../../appendix/approval-schema.zh.md) 和 [参考运行时包](../../appendix/reference-package.zh.md)。

## 2. 策略层应该回答小而清晰的问题

弱的策略层总想成为“系统的大脑”。强的策略层恰好相反：它只解决一组有限而清晰的问题。

例如：

- 这个 run 能不能开始；
- 这段上下文能不能读；
- 这个 capability 能不能调用；
- 是否需要 approval；
- 这段内容能不能写入 memory；
- 这个结果能不能向外返回。

当这些问题被明确表达出来后，runtime 会更容易解释，guardrails 的修改也不再混乱。

## 3. Capability 目录不是名字列表，而是契约层

很容易把 catalog 做成“可用 tools 列表”。但好的 catalog 要做得更多：

- 描述 capability contract；
- 保存 risk profile；
- 声明 transport 和 execution mode；
- 记录 idempotency expectations；
- 固定 ownership 和 lifecycle。

所以 capability catalog 不是“为了方便的 inventory”，而是平台能力的中心控制点。

<div class="diagram-card">
<p>策略层与能力目录一起构成参考实现的 contract core</p>

``` mermaid
flowchart LR
    A["Run request"] --> B["Runtime orchestrator"]
    B --> C["Policy layer"]
    B --> D["Capability catalog"]
    C --> E["Allow / deny / approve"]
    D --> F["Capability contract"]
    E --> G["Execution layer"]
    F --> G
```

</div>

## 4. Tool surface 不等于 governed capability surface

OpenAI 最近关于 tooling 的材料有一个很有用的区分，而很多团队在实践里会把它混掉：模型也许能看到 tools、MCP servers、hosted capabilities 或 local functions，但 runtime 仍然必须决定这些东西究竟属于哪一种 control surface。[^openai-tools]

这个区分很重要。

弱实现会说：

- 这里有一张模型可调用的 tools 列表。

更强的实现会说：

- 这里是 governed capability surface；
- 其中哪一部分会暴露给模型；
- 执行通过哪一种 transport 走；
- 哪些 capabilities 可以直接调用，哪些必须通过 gateway broker，哪些根本不暴露。

这就是为什么 capability catalog 必须放在原始 tool definitions 之上。它防止 runtime 混淆：

- 模型可以提到什么；
- runtime 可以路由什么；
- 平台真正愿意执行什么。

## 5. Capability catalog 里值得存什么

一个实用的字段集合通常包括：

- capability name；
- owner；
- mode: read / write / high_risk；
- transport: mcp / gateway / sandboxed_exec；
- exposure: direct / brokered / restricted；
- input schema；
- output shape；
- approval requirement；
- idempotency requirement；
- timeout 和 retry defaults。

有了这样的 contract，runtime 才能以可预测的方式运行，而不是对每个 capability 临时适配。

## 6. Approval 应该表现成 interruptible runtime path，而不是旁路的人类对话

当 approval 被建模为 runtime control flow 的一部分，而不是系统外部的手工流程时，policy layer 才会真正落地。LangGraph 的 interrupts 模型在这里很有用，因为它把 pause、review 与 resume 变成了显式 runtime primitives，而不是 ad hoc 的人工补丁。[^langgraph-interrupts]

这也是 policy-heavy agent systems 更合理的形状。

当一个 high-risk capability 走到 approval boundary 时，runtime 应该能够：

- 暂停这次 run；
- 暴露 pending action 及其上下文；
- 等待外部决策；
- 用结构化 outcome 恢复执行。

这比“给 operator 发条消息，然后希望外围代码还记得自己停在哪”强得多。

## 7. Policy decision 应该是对象，而不只是 bool

一个很有用的工程习惯：不要把 policy decision 简化成 `True/False`。

通常更有用的是返回类似：

- `allow`
- `deny`
- `approval_required`
- `sanitize_and_continue`
- `escalate`

以及额外信息：

- reason code；
- policy id；
- risk class；
- optional constraints；
- 必要时还包括 approval 或 resume requirements。

这会大幅提升 explainability，也让 telemetry 更有价值。

## 8. 一个 policy contract 示例

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

## 9. 一个 capability catalog contract 示例

你可以把 catalog 大致设计成这样：

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

这样的 catalog 已经在定义 operational semantics，而不只是 capability 名字。它还明确了某个 capability 是 model-facing、runtime-brokered，还是仅供 operator 使用。

## 10. Structured outputs 很重要，因为 contracts 必须在接触代码后仍然成立

OpenAI 最近关于 structured outputs 的材料，对 policy layer 也很有帮助。[^openai-structured]

如果 runtime 仍然需要猜测 policy result、approval request 或 capability payload 是否按预期形态返回，那么 contract 其实只完成了一半。

所以对 policy-heavy systems 来说，下面这些关键 artifacts 最好都做成结构显式：

- policy decisions；
- approval requests；
- approval outcomes；
- capability inputs 与 outputs。

目的不是为了形式优雅，而是为了减少 runtime logic、audit records 和 surrounding control surface 之间的静默漂移。

## 11. 一个简单的 policy decision skeleton

重点在于：runtime 拿到的不只是“准不准”，而是结构化决策。

```python
from dataclasses import dataclass


@dataclass
class PolicyDecision:
    action: str
    reason: str
    policy_id: str
    requires_approval: bool = False


def evaluate_capability(name: str) -> PolicyDecision:
    if name == "search_docs":
        return PolicyDecision(action="allow", reason="low_risk_read", policy_id="cap_001")
    if name == "create_ticket":
        return PolicyDecision(action="approval_required", reason="write_action", policy_id="cap_014", requires_approval=True)
    return PolicyDecision(action="deny", reason="unsupported_capability", policy_id="cap_999")
```

即使这么简单的代码，也已经给 telemetry、approval UI flow 和事后调查提供了正确的形状。

## 12. 一个简单的 capability lookup skeleton

再来一个很实用的点：runtime 不应该直接知道 capability 细节，而应该从 catalog 中取。

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

这同样看起来很“无聊”。很好。Catalog layer 本来就应该无聊、稳定、可审阅。

## 13. 常见错误

这些问题非常常见：

- policy rules 散落在 runtime 代码各处；
- capability contract 不完整；
- 暴露给模型的 tools 被误当成自动获批的 capabilities；
- capability ownership 不清晰；
- approval logic 直接嵌进 orchestration；
- approval 虽然存在，但没有被建模成 runtime 内显式的 pause/resume path；
- 缺少 structured contracts，导致 policy 与 approval payload 在形态上逐渐漂移；
- memory policy 和 execution policy 好像互不相干；
- catalog 和真实 adapter 的行为逐渐漂移。

一旦这样，参考实现就不再是 reference，而是又退回成一堆约定。

## 14. 给 policy layer 和 capability catalog 做一次快速成熟度测试

团队不应该只因为已经有几条 policy checks 和一张 tools 列表，就觉得自己已经搭好了 agent system 的 contract core。

更高的标准应该是：

- policy decisions 是显式对象，而不是散落的 booleans；
- capability contracts 携带 ownership、transport、exposure、risk 和 approval semantics；
- runtime code 依赖 catalog，而不是 direct calls 和 ad hoc exceptions；
- approval 被建模成显式 interruptible path，而不是流程外的人工绕路；
- memory policy、execution policy 和 approval policy 属于同一个可见的 control surface；
- telemetry 不只展示发生了什么，还能展示是哪条 policy 和哪个 capability contract 在起作用。

如果这些条件大多不成立，那 runtime 也许已经存在，但 contract core 还没有真正搭起来。

## 15. 现在就该做什么

先过一遍这份短清单，把所有回答为 “no” 的地方单独记下来：

- 你有没有独立的 policy layer，而不是一堆散落的 `if`？
- policy 返回的是不是 structured decision？
- 你有没有统一的 capability catalog？
- capabilities 是否拥有 owner、transport、exposure 和 risk semantics？
- runtime 是否使用 catalog，而不是 direct calls？
- approval 能否显式暂停并恢复一次 run？
- policy decisions 是否能在 telemetry 里看到？

如果连续多个答案都是“没有”，那说明 skeleton 已经有了，但 contract core 还没真正搭起来。

## 16. 下一步做什么

先把 policy decisions 和 capability contracts 固定下来，再检查同一套系统是否已经准备好 first rollout。

参考实现的下一步很自然：组装 production rollout checklist，把 blueprint 和 contract core 变成一个真正可落地的 go-live framework。

- [第 16 章：基础运行时蓝图](chapter-16.zh.md)
- [第 18 章：生产上线检查清单](chapter-18.zh.md)
- [第七部分：参考实现](index.zh.md)
- [参考来源](../../appendix/sources.zh.md)

[^openai-tools]: [OpenAI, Using tools](https://developers.openai.com/api/docs/guides/tools)
[^langgraph-interrupts]: [LangGraph, Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)
[^openai-structured]: [OpenAI, Structured model outputs](https://developers.openai.com/api/docs/guides/structured-outputs)

## 17. 值得配套阅读的参考页

- [Policy Bundle Schema 与 Approval Contract](../../appendix/policy-bundle-schema.zh.md)
- [Lifecycle Artifact Schema](../../appendix/lifecycle-artifact-schema.zh.md)
- [Reference Package](../../appendix/reference-package.zh.md)

这一章是整个 runtime-control cluster 的契约枢纽。最值得继续看的下一步，是第 18 章里把这些路径变成 rollout gates，以及第 21 章里把同样的 approval 与 policy paths 变成 assurance response。

- [第 16 章：基础运行时蓝图](chapter-16.zh.md)
- [第 18 章：生产上线检查清单](chapter-18.zh.md)
- [第七部分：参考实现](index.zh.md)
- [参考来源](../../appendix/sources.zh.md)
