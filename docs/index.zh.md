# 安全 AI 智能体架构

这是一本面向工程师与平台负责人的现代实践手册，目标不是构建演示级 agent，而是构建可观测、可治理且安全的生产系统。

> 本书以 Dmitry Vikulin 关于可靠 AI 智能体的文章为起点，将其扩展为完整的平台架构：包含治理、策略执行、人工审批、可观测性、评测体系与运维控制。

[查看全书计划](book/plan.md){ .md-button .md-button--primary }
[阅读第一部分](book/part-i/index.md){ .md-button }
[查看参考来源](appendix/sources.md){ .md-button }

## 应该先投入什么

下面这张交互图可以当成一条经验法则：在大多数真实系统里，控制、安全与可观测性通常都比“最大自治”更值得优先建设。

<div class="plot-card" data-plot="agent-priority"></div>

## 书中内容

- 架构模式：workflow、router、planner、subagents、human-in-the-loop。
- 安全：IAM、policy-as-code、prompt injection 防护、sandbox、数据边界。
- 可靠性：checkpoints、幂等性、重试、优雅降级。
- 透明性：traces、metrics、evals、回归控制。
- 平台设计：gateways、shared runtime、knowledge plane、tool plane、control plane。

## 核心观点

智能体系统最常见的错误，是先追求自治，而不是先保证可控性。Anthropic、OpenAI、LangGraph 以及 Google 企业平台的实践更接近下面这条路径：

1. 先构建**可预测的 workflow**。
2. 再按局部、可度量的方式加入自治能力。
3. 所有高风险动作都必须经过**policy、approval 与 tracing**。
4. 质量依赖**evals 与 telemetry**，而不是对模型能力的想象。

## 为什么选择 MkDocs

在 2026 年，`MkDocs + Material for MkDocs` 依然是 Python-first 文档书籍的务实方案：生态仍然活跃、构建速度快、非常适合 Markdown 工作流，并且能自然接入基于 `uv` 的 Python 工具链。[^mkdocs][^material][^uv]

如果后续项目需要更多 UI 组件和接近 MDX 的表达能力，`Astro Starlight` 是最自然的升级方向。但对于第一版公开发布，Python-first 栈更简单，也更稳定。[^starlight]

## 本架构所依据的来源

- 智能体基础模块框架：[vikulin.ai](https://vikulin.ai/library/tpost/ai_agent_architecture)
- “先 workflow，后 agents”： [Anthropic, Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- Durable execution、memory 与 HITL： [LangGraph docs](https://docs.langchain.com/oss/javascript/langgraph)
- Tracing 与 agent evals： [OpenAI docs](https://developers.openai.com/api/docs/guides/agents-sdk)
- 风险管理与安全控制： [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework), [OWASP Prompt Injection Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)

[^mkdocs]: [MkDocs User Guide](https://www.mkdocs.org/).
[^material]: [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).
[^uv]: [uv project guide](https://docs.astral.sh/uv/guides/projects/).
[^starlight]: [Starlight documentation](https://starlight.astro.build/).
