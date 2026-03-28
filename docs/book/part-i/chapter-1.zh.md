# 第 1 章：现代安全架构

## 1. 从“可靠智能体”到“安全平台”

Dmitry Vikulin 的文章提出了一个正确的起点问题：一个可靠智能体究竟由哪些模块组成。[^vikulin] 但对于 2026 年来说，这已经不够了。领先团队的实践更趋于以下模式：

- 先选择**最简单且可执行的模式**；
- 将高风险动作放入独立的 **control plane**；
- 只有在存在 **policy、telemetry 与 rollback boundary** 时才允许自治。[^anthropic][^openai-evals][^langgraph-durable]

因此，更合理的设计方式不是“一个很聪明的 agent”，而是一个**安全智能体执行平台**。

## 2. 架构原则

### 2.1 默认使用 workflow，只在必要处引入 agent autonomy

Anthropic 明确区分 `workflows` 与 `agents`，并建议先从更简单的方案开始。[^anthropic] 由此可以得到很强的平台原则：

- 如果执行路径已知，就写 workflow；
- 如果只是在狭窄边界内需要选择工具，就用 single-agent loop；
- 如果任务天然可拆成独立子任务，就用 subagents；
- 如果说不清自治的必要性，大概率就还不需要它。

### 2.2 所有高风险操作都必须经过 policy boundary

模型不应直接读取 secrets、写入关键系统或无限制调用外部接口。任何对 model、memory 与 tools 的访问都应经过带统一检查的 gateway：

- 认证与授权；
- 脱敏与数据分级；
- prompt injection 检查；
- 对敏感动作进行人工审批；
- 对决策过程和执行事件进行完整 tracing。[^owasp][^anthropic-security][^nist-genai]

### 2.3 状态必须显式、可恢复

长任务失败并不只因为模型本身，也因为状态容易丢失。LangGraph 文档把 durable execution 与 checkpoints 放在 orchestration runtime 的中心位置。[^langgraph-durable] 这意味着：

- 任务状态保存在进程外；
- 步骤应当是幂等的；
- 副作用必须隔离；
- 失败后或人工审批暂停后可以继续恢复执行。

### 2.4 可观测性比“魔法感”更重要

OpenAI 和其他平台越来越强调 traces、evals 与 trace grading，因为没有这些，agent 仍然是黑盒。[^openai-sdk][^openai-evals] 生产团队必须能看见：

- agent 生成了什么计划；
- 调用了哪些工具；
- 给模型喂了什么上下文；
- 质量在哪一步退化；
- 每一步的延迟和 token 成本是多少。

## 3. 参考架构

下表可作为企业级安全智能体平台的基线。

| 层 | 作用 | 为什么必需 |
| --- | --- | --- |
| Interface layer | 聊天、API、事件接入、webhooks | 将用户通道与 runtime 分离 |
| Identity and session layer | 用户、服务账号、thread、tenant、request scope | IAM、审计与隔离的基础 |
| Agent control plane | Policies、approvals、model policies、tool catalog、quotas | 可治理能力所在 |
| Orchestration runtime | Workflow graph、planner、router、subagents、checkpoints | 任务真正执行的地方 |
| Cognition plane | Model router、prompt compiler、structured outputs、validators | 让模型成为组件，而不是世界中心 |
| Memory and knowledge plane | Short-term state、long-term memory、retrieval、summaries | 防止上下文无限膨胀 |
| Tool execution plane | Sandboxed tools、MCP servers、connectors、副作用隔离 | 降低 blast radius |
| Telemetry and eval plane | Traces、metrics、logs、datasets、graders、regression gates | 让质量可度量 |

## 4. 这些层如何协同

### 4.1 Interface layer

进入系统的请求不应直接送入 orchestrator。它首先应被赋予：

- `tenant_id`；
- `principal`；
- 风险等级；
- 当前访问策略引用；
- session 与 trace 标识。

这样从第一步开始就具备审计和事故排查能力。

### 4.2 Agent control plane

这是大多数 demo 架构里缺失的关键层。它负责的不是“智能”本身，而是**系统是否被允许以智能方式行动**。

最少应该包含：

- 带允许 use cases 的模型目录；
- 带审批等级的工具目录；
- 脱敏和数据泄漏防护规则；
- 成本、延迟和 agent loop 深度预算；
- dev、staging、prod 的环境策略。

示例 policy-as-code：

```yaml
agent_policy:
  model_access:
    allowed_models: ["gpt-5.4", "gpt-5-mini", "claude-sonnet"]
    deny_if_contains: ["pci_raw", "prod_secrets"]
  tools:
    read_kb:
      approval: none
    jira_create_ticket:
      approval: manager
    prod_db_write:
      approval: security_and_owner
      allowed_environments: ["staging"]
  runtime:
    max_steps: 24
    max_parallel_subagents: 4
    require_checkpoint_every_step: true
```

### 4.3 Orchestration runtime

这一层负责选择执行模式：

- 用 deterministic workflow 处理强规则场景；
- 用 routed workflow 处理分支选择；
- 用 plan-and-execute 处理长任务；
- 用 planner + subagents 处理独立子任务；
- 对高风险操作使用 HITL interrupts。[^langgraph-hitl][^openai-builder]

这里最重要的工程原则很简单：orchestration runtime 应当尽量**无聊**。越“魔法”，越难预测成本、行为与故障模式。

### 4.4 Cognition plane

这里不是一台“大模型”，而是一组可控组件：

- planner model；
- executor model；
- classifier 或 extractor model；
- structured output validator；
- 用于降级时的 fallback model。

这种级联结构符合 model routing 与 graceful degradation 的工程实践：昂贵的 reasoning 只在真正需要的地方使用。[^vikulin][^openai-models]

### 4.5 Memory and knowledge plane

现代智能体记忆至少分成两类：

- **short-term state**：当前执行状态、tool results、中间决策；
- **long-term memory**：用户事实、profiles、episodes、领域资产。[^langgraph-memory]

必须避免把 memory 和 retrieval 混为一谈：

- memory 存的是系统决定要记住的内容；
- retrieval 取的是外部知识库中的相关文档；
- compaction 与 summarization 用于压缩活跃上下文中的噪声。

### 4.6 Tool execution plane

工具不能被视为简单的 function call。它本身就是风险区域。

安全的 tool plane 至少包含：

- sandbox 或受限执行环境；
- 工具与参数 allowlist；
- 在非必要场景下禁止直接网络访问；
- 每个 connector 独立 secret；
- 面向有副作用系统的幂等适配器。

Anthropic 在 Claude Code 的安全文档中也特别强调了 permissions、isolated contexts 与对敏感网络和 shell 操作的手工审批。[^anthropic-security]

### 4.7 Telemetry and eval plane

最低限度的生产配置应包括：

- 每次运行的 distributed traces；
- 对 model calls、retrieval 与 tools 的 spans；
- 每一步的成本与延迟；
- 参考任务数据集；
- 在发布新的 prompt、policy 或 model 组合前进行 regression gates。[^openai-evals][^openai-trace]

如果没有这些，团队并不是在控制 agent，而只是在旁观它。

## 5. 安全到底部署在哪里

智能体系统中的安全不应集中在一个“guardrail service”里，而应该分布在多个控制点：

| 控制点 | 检查内容 |
| --- | --- |
| Pre-ingress filters | 明确危险的输入、secrets、禁止附件 |
| Prompt assembly | 指令与数据混淆、untrusted content boundaries |
| Model gateway | Model allowlist、预算、moderation、routing |
| Retrieval gateway | 文档权限、tenant isolation、metadata filters |
| Tool gateway | 参数校验、审批、副作用类别 |
| Egress filters | 数据泄漏、PII、不安全外发内容 |
| Observability backend | 审计链路与事故调查 |

这种做法与 OWASP 的 prompt injection 防护建议，以及 NIST AI RMF / GenAI Profile 的生命周期风险治理框架是高度一致的。[^owasp][^nist-rmf][^nist-genai]

## 6. 参考 operating model

为了避免平台变成“动物园”，建议这样分工：

- platform team 负责 gateways、policies、telemetry 与 golden templates；
- product teams 负责具体 agent 与业务逻辑；
- security team 定义风险等级、审批规则和控制点；
- evaluation owner 维护任务集、graders 与回归控制。

Google 的企业智能体平台实践也强调 centralized visibility、governance 与 managed access，而不仅仅是 orchestration。[^google-agentspace][^google-agent-builder]

## 7. 实践结论

现代生产级智能体不是“带工具的 LLM”，而是一套系统，其中：

1. orchestration 被有意简化；
2. autonomy 被 policy 约束；
3. memory 与 retrieval 被分离；
4. tools 通过隔离 gateway 执行；
5. 每一步都能通过 traces 与 evals 被看见；
6. 人类可以中断或批准高风险动作。

去掉其中任何一项，最后得到的不是脆弱 demo，就是不安全系统。

## 8. 下一步阅读

- [全书计划](../plan.md)
- [第一部分：基础](index.md)
- [发布技术栈](../../appendix/stack.md)
- [来源与参考文献](../../appendix/sources.md)

[^vikulin]: [Dmitry Vikulin, "Architecture of Reliable AI Agents"](https://vikulin.ai/library/tpost/ai_agent_architecture)
[^anthropic]: [Anthropic, Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
[^anthropic-security]: [Anthropic, Claude Code Security](https://docs.anthropic.com/en/docs/claude-code/security)
[^owasp]: [OWASP, LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
[^nist-rmf]: [NIST, AI RMF 1.0](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10)
[^nist-genai]: [NIST, AI RMF: Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
[^langgraph-durable]: [LangGraph, Durable execution](https://docs.langchain.com/oss/javascript/langgraph/durable-execution)
[^langgraph-memory]: [LangGraph, Memory overview](https://docs.langchain.com/oss/python/langgraph/memory)
[^langgraph-hitl]: [LangChain Deep Agents, Human-in-the-loop](https://docs.langchain.com/oss/javascript/deepagents/human-in-the-loop)
[^openai-sdk]: [OpenAI, Agents SDK](https://developers.openai.com/api/docs/guides/agents-sdk)
[^openai-evals]: [OpenAI, Agent evals](https://platform.openai.com/docs/guides/agent-evals)
[^openai-trace]: [OpenAI, Trace grading](https://platform.openai.com/docs/guides/trace-grading)
[^openai-builder]: [OpenAI, Agent Builder](https://platform.openai.com/docs/guides/agent-builder)
[^openai-models]: [OpenAI, Models](https://developers.openai.com/api/docs/models)
[^google-agentspace]: [Google Agentspace](https://cloud.google.com/products/agentspace)
[^google-agent-builder]: [Vertex AI Agent Builder](https://cloud.google.com/products/agent-builder)

