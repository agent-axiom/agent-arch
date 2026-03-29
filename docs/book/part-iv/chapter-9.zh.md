# 第 9 章：沙箱执行与 MCP 作为集成契约

## 1. 为什么没有 sandbox 的 execution layer 会很快变得过度信任

一旦智能体获得了工具访问能力，下一个危险几乎总是同一个：系统边界开始模糊。

智能体已经可以：

- 读取数据；
- 启动操作；
- 调用外部服务；
- 接收来自不可预测环境的响应。

如果这一切都“原样执行”，没有隔离和契约，平台很快就会积累问题：

- tool 以意外格式返回不可信 payload；
- integration 卡住或超出资源预算；
- side effect 在预期 policy path 之外发生；
- 一个设计糟糕的 adapter 拖垮整个 runtime。

所以 execution layer 不只是 router，它还是 sandbox boundary。

## 2. Sandbox 不一定是容器，它首先是一组限制

一说到 “sandbox”，很多人立刻想到 Docker、VM 或独立进程。这些都可以是实现方式，但架构上更重要的是：sandbox 定义了 capability 被允许做什么、不允许做什么。

好的 sandbox 通常会限制：

- 网络访问；
- 文件系统访问；
- secrets 访问；
- CPU 和 memory budgets；
- allowed syscalls 或 execution mode；
- 操作生命周期。

也就是说，sandbox 回答的是：“如果 tool 或 adapter 的行为比预期更糟，会发生什么？”

这不仅仅是安全问题，也是 blast radius 控制。

## 3. 不能把外部集成当成普通函数

一个常见错误是：把外部服务包成一个函数，然后让智能体把它当普通调用使用。

但真实集成几乎总是：

- 比本地代码更不稳定；
- 类型边界更脆弱；
- 依赖权限和环境；
- 可能返回部分成功或危险结果；
- 自带 latency 和 rate limits。

所以更好的做法是把集成视为带契约的 capability endpoint，而不是“方便的 helper method”。

## 4. MCP 的价值就在于契约层

MCP 有用，不是因为它“新潮”，而是因为它能在智能体和外部 capability 之间提供清晰的 contract boundary。

在好的设计里，MCP 会给你这些收益：

- 标准化描述 tools 和 resources 的方式；
- 独立的 server boundary；
- 更清晰的 capability lifecycle；
- adapter 可以放在核心 runtime 之外；
- 天然适合作为 policy checks、logging 和 isolation 的切入点。

当你有的不是一个 runtime + 一个 integration，而是一组能力时，这一点就尤其重要。

<div class="diagram-card">
<p>MCP 适合作为 runtime 和外部 capabilities 之间的契约层</p>

``` mermaid
flowchart LR
    A["Agent runtime"] --> B["Execution layer"]
    B --> C["Policy and validation"]
    C --> D["MCP client"]
    D --> E["MCP server"]
    E --> F["Typed adapter"]
    F --> G["External API / system"]
    G --> F
    F --> E
    E --> D
    D --> B
```

</div>

## 5. 为什么要把 adapters 移出 core runtime

这会带来很多直接收益：

- 单个 integration 的失败不容易拖垮 central runtime；
- 更容易按 capability 限制网络、secrets 和 filesystem；
- 不重写 orchestration 也能替换或升级某个 adapter；
- contracts 更清晰；
- capability 更容易独立测试。

当某些工具只读、某些会写外部系统、某些甚至执行代码或 shell 时，这一点尤其重要。

## 6. 不是所有 capability 都需要同等级别的隔离

把集成至少分成三类会很有帮助：

- low-risk read capabilities；
- medium-risk business actions；
- high-risk execution capabilities。

例如：

- `read_kb` 或 `search_docs` 可以用较轻的执行限制；
- `create_ticket` 或 `update_crm_record` 需要更严格的 policy 和 audit；
- `run_shell`、`exec_sql`、`deploy_job` 需要最强的 sandbox 和 approval。

如果所有工具都被放进同一种宽松 execution profile，平台要么不安全，要么很快就会因 side effects 产生事故。

## 7. Capability contract 不应只包含 input/output

很多团队对 input schema 还能描述得不错，但 operational contract 常常完全缺失。而实践中，这部分往往更关键。

最好明确写出：

- read 或 write 属性；
- network policy；
- secret scope；
- allowed environments；
- timeout budget；
- retry policy；
- approval requirement；
- logging 和 redaction rules。

```yaml
capabilities:
  search_docs:
    transport: mcp
    mode: read
    network: internal_only
    secrets: none
    timeout_seconds: 8
    approval: none
  create_ticket:
    transport: mcp
    mode: write
    network: internal_only
    secrets: service_account_helpdesk
    timeout_seconds: 15
    approval: manager_for_high_priority
  run_shell:
    transport: sandboxed_exec
    mode: high_risk
    network: denied
    filesystem: workspace_only
    secrets: none
    timeout_seconds: 10
    approval: always
```

这已经不只是函数描述，而是 capability 的行为契约。

## 8. Sandbox execution 应该返回 execution facts，而不只是 output

如果 sandbox 只返回 stdout 或 payload，你就丢掉了一半的隔离层价值。

为了调查和控制，最好还能返回：

- exit status；
- timeout flag；
- resource usage summary；
- side effect uncertainty；
- redacted logs；
- policy decision id。

这样 execution layer 才能解释得更成熟：不是“命令失败了”，而是“操作在 8 秒后超时中止、网络被禁止、side effect 未确认”。

## 9. 一个简单的 capability dispatch 示例

这个小 skeleton 展示的核心思想是：transport 和 execution profile 来自 capability contract，而不是由模型临时决定。

```python
from dataclasses import dataclass


@dataclass
class CapabilitySpec:
    name: str
    transport: str
    mode: str
    timeout_seconds: int


def dispatch_capability(spec: CapabilitySpec, args: dict) -> dict:
    if spec.transport == "mcp":
        return {"status": "success", "transport": "mcp", "capability": spec.name}
    if spec.transport == "sandboxed_exec" and spec.mode == "high_risk":
        return {"status": "approval_required", "capability": spec.name}
    return {"status": "validation_failure", "reason": "unsupported capability profile"}
```

它非常简单，但把一个正确前提固定下来：执行方式由平台决定，而不是模型每次重新发明。

## 10. Sandbox 和 capability layer 最常见的崩坏点

这些问题一再重复：

- 某个 capability 拿到了超出必要范围的 network access；
- secrets 对过多 adapters 可见；
- tool result 把原始外部 payload 直接拖进 prompt；
- timeout 存在，但 side effect uncertainty 没有被建模；
- MCP server 接上了，但 policy 和 audit 根本没延伸进去；
- sandbox 名义上存在，但没有限制任何关键东西。

所以 sandbox 不能只是 checkbox-feature，它必须成为 execution design 的一部分。

## 11. 实用检查清单

如果你想快速检查 capability layer，可以问：

- adapters 是否和 core runtime 分开？
- 是否存在 per-capability execution profile？
- network、filesystem 和 secrets 是否被约束？
- transport 是否显式：direct、MCP、sandboxed exec？
- 系统是否区分 trustworthy 和 partially trusted result？
- business payload 之外是否保留 execution facts？
- 能否解释为什么某个 capability 会在这个 run 中被允许？

如果这些答案很模糊，那说明 capability layer 还只是“一堆好用的集成”，而不是受管理的平台层。

## 12. 接下来读什么

这一部分下一个自然主题是：幂等性、重试、速率限制和回滚边界。经过 sandbox 和 capability contracts 之后，这才是把 execution model 变成 production-grade 的关键。

- [第 8 章：执行模型与工具目录](chapter-8.zh.md)
- [第四部分：工具与执行](index.zh.md)
- [参考来源](../../appendix/sources.md)
