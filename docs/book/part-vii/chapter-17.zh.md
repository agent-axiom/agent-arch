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

## 4. Capability catalog 里值得存什么

一个实用的字段集合通常包括：

- capability name；
- owner；
- mode: read / write / high_risk；
- transport: mcp / gateway / sandboxed_exec；
- input schema；
- output shape；
- approval requirement；
- idempotency requirement；
- timeout 和 retry defaults。

有了这样的 contract，runtime 才能以可预测的方式运行，而不是对每个 capability 临时适配。

## 5. Policy decision 应该是对象，而不只是 bool

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
- optional constraints。

这会大幅提升 explainability，也让 telemetry 更有价值。

## 6. 一个 policy contract 示例

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

## 7. 一个 capability catalog contract 示例

你可以把 catalog 大致设计成这样：

```yaml
capabilities:
  search_docs:
    owner: knowledge_platform
    mode: read
    transport: mcp
    timeout_seconds: 5
    approval: none
  create_ticket:
    owner: support_platform
    mode: write
    transport: gateway
    timeout_seconds: 15
    approval: manager
    idempotency_key_required: true
  run_shell:
    owner: platform_runtime
    mode: high_risk
    transport: sandboxed_exec
    timeout_seconds: 10
    approval: always
```

这样的 catalog 已经在定义 operational semantics，而不只是 capability 名字。

## 8. 一个简单的 policy decision skeleton

重点在于：runtime 拿到的不只是“准不准”，而是结构化决策。

```python
from dataclasses import dataclass


@dataclass
class PolicyDecision:
    action: str
    reason: str
    policy_id: str


def evaluate_capability(name: str) -> PolicyDecision:
    if name == "search_docs":
        return PolicyDecision(action="allow", reason="low_risk_read", policy_id="cap_001")
    if name == "create_ticket":
        return PolicyDecision(action="approval_required", reason="write_action", policy_id="cap_014")
    return PolicyDecision(action="deny", reason="unsupported_capability", policy_id="cap_999")
```

即使这么简单的代码，也已经给 telemetry、approval UI flow 和事后调查提供了正确的形状。

## 9. 一个简单的 capability lookup skeleton

再来一个很实用的点：runtime 不应该直接知道 capability 细节，而应该从 catalog 中取。

```python
from dataclasses import dataclass


@dataclass
class CapabilitySpec:
    name: str
    mode: str
    transport: str
    timeout_seconds: int


def get_capability(name: str) -> CapabilitySpec | None:
    registry = {
        "search_docs": CapabilitySpec("search_docs", "read", "mcp", 5),
        "create_ticket": CapabilitySpec("create_ticket", "write", "gateway", 15),
    }
    return registry.get(name)
```

这同样看起来很“无聊”。很好。Catalog layer 本来就应该无聊、稳定、可审阅。

## 10. Policy 和 catalog 最常见的崩坏点

这些问题非常常见：

- policy rules 散落在 runtime 代码各处；
- capability contract 不完整；
- capability ownership 不清晰；
- approval logic 直接嵌进 orchestration；
- memory policy 和 execution policy 好像互不相干；
- catalog 和真实 adapter 的行为逐渐漂移。

一旦这样，参考实现就不再是 reference，而是又退回成一堆约定。

## 11. 实用检查清单

如果你想快速检查这一层，可以问：

- 你有没有独立的 policy layer，而不是一堆散落的 `if`？
- policy 返回的是不是 structured decision？
- 你有没有统一的 capability catalog？
- capabilities 是否拥有 owner、transport 和 risk semantics？
- runtime 是否使用 catalog，而不是 direct calls？
- policy decisions 是否能在 telemetry 里看到？

如果连续多个答案都是“没有”，那说明 skeleton 已经有了，但 contract core 还没真正搭起来。

## 12. 下一步做什么

先把 policy decisions 和 capability contracts 固定下来，再检查同一套系统是否已经准备好 first rollout。

参考实现的下一步很自然：组装 production rollout checklist，把 blueprint 和 contract core 变成一个真正可落地的 go-live framework。

- [第 16 章：基础运行时蓝图](chapter-16.zh.md)
- [第 18 章：生产上线检查清单](chapter-18.zh.md)
- [第七部分：参考实现](index.zh.md)
- [参考来源](../../appendix/sources.zh.md)

## 13. 值得配套阅读的参考页

- [Policy Bundle Schema 与 Approval Contract](../../appendix/policy-bundle-schema.zh.md)
- [Lifecycle Artifact Schema](../../appendix/lifecycle-artifact-schema.zh.md)
- [Reference Package](../../appendix/reference-package.zh.md)

- [第 16 章：基础运行时蓝图](chapter-16.zh.md)
- [第 18 章：生产上线检查清单](chapter-18.zh.md)
- [第七部分：参考实现](index.zh.md)
- [参考来源](../../appendix/sources.zh.md)
