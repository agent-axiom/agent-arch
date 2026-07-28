# Источники

Ниже собраны основные первоисточники, на которые опирается текущая версия книги. Дата последней редакционной проверки источников: **24 июля 2026 года**. Полная автоматизированная проверка доступности URL выполнена **29 июня 2026 года**, ручная проверка проблемных адресов — **30 июня 2026 года**. Microsoft Research, Anthropic Claude Code Security и MLCommons подтверждены чтением заголовка и содержимого страницы, кейс Air Canada переведен на официальный первоисточник CRT, а записи OpenReview отнесены к исследовательским материалам и не используются как основные доказательства в финальном редакторском пакете.

!!! info "Как читать этот список"
    Полезно разделять источники не только по теме, но и по силе опоры:

    - `Нормативный каркас`: NIST, OWASP, CISA и другие документы, которые задают устойчивые контуры управления;
    - `Платформенная практика`: OpenAI, Anthropic, LangGraph, Google Cloud, Microsoft и другие материалы о том, как эти контуры реально собирают в промышленной эксплуатации;
    - `HCI, HITL и человеческий надзор`: источники, которые показывают, где automation ошибается и как удерживать человека в петле;
    - `Исследовательский фронтир`: свежие статьи про память, наблюдаемость, дизайн проверяющих и надежность многоагентных систем.

    Если нужна самая надежная база для Parts I, V и VIII, начинай с нормативного каркаса и слоя HCI/HITL. Если нужна текущая инженерная практика, смотри платформенные документы и свежие исследования, но всегда учитывай дату публикации.

!!! note "Канонические маршруты источников"
    Используй источники как быстрый маршрут для трех канонических сценариев. **Триаж обращений поддержки** начинается с OWASP, руководств OpenAI по агентам, источников о человеке в контуре, материалов по политикам и подтверждениям, оценки трасс и кейсов инцидентов. **Внутренний ассистент знаний** начинается с материалов LangGraph о памяти, материалов OpenAI о памяти агента, источников по поиску и оценке, управления с акцентом на происхождение данных и исследовательского фронтира памяти. **Координация инцидентов** начинается с NIST/AI RMF, материалов Google и Microsoft по управлению, источников наблюдаемости, исследований надежности многоагентных систем, разбора инцидентов и материалов по выпуску и управляющему слою.

## Нормативные рамки и контуры управления

### Безопасность агентных систем

- OWASP, [AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)
- OWASP GenAI Security Project, [OWASP Top 10 for Agentic Applications for 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
- OWASP, [MCP Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/MCP_Security_Cheat_Sheet.html)
- OWASP, [MCP Tool Poisoning](https://owasp.org/www-community/attacks/MCP_Tool_Poisoning)
- OWASP, [MCP Top 10](https://owasp.org/www-project-mcp-top-10/)
- OWASP, [Agentic Skills Top 10](https://owasp.org/www-project-agentic-skills-top-10/)
- OWASP, [LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
- OWASP, [RAG Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/RAG_Security_Cheat_Sheet.html)

### Управление и базовые меры контроля

- NIST, [AI RMF 1.0](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10)
- NIST, [AI RMF: Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- NIST, [SP 800-53 Rev. 5: Security and Privacy Controls for Information Systems and Organizations](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
- NIST, [SP 800-218A: Secure Software Development Practices for Generative AI and Dual-Use Foundation Models](https://csrc.nist.gov/pubs/sp/800/218/a/final)
- NIST, [Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations](https://www.nist.gov/publications/adversarial-machine-learning-taxonomy-and-terminology-attacks-and-mitigations-0)
- CISA, [Artificial Intelligence](https://www.cisa.gov/ai)

## Архитектура агентных систем и платформенные паттерны

- Дмитрий Викулин, [«Архитектура надежных AI-агентов»](https://vikulin.ai/library/tpost/ai_agent_architecture)
- Anthropic, [Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
- Anthropic, [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- Anthropic, [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- Anthropic, [How we contain Claude across products](https://www.anthropic.com/engineering/how-we-contain-claude)
- Anthropic, [Scaling Managed Agents: Decoupling the brain from the hands](https://www.anthropic.com/engineering/managed-agents)
- Anthropic, [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- Anthropic, [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- Anthropic, [Agentic coding and persistent returns to expertise](https://www.anthropic.com/research/claude-code-expertise)
- Anthropic, [An update on recent Claude Code quality reports](https://www.anthropic.com/engineering/april-23-postmortem)
- Anthropic Institute, [When AI builds itself](https://www.anthropic.com/institute/recursive-self-improvement)
- Snowflake Documentation, [Cortex Analyst](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst)
- Databricks Documentation, [Genie Spaces](https://docs.databricks.com/aws/en/genie/)
- Microsoft Learn, [Copilot for Power BI overview](https://learn.microsoft.com/en-us/power-bi/create-reports/copilot-introduction)
- OpenAI, [A practical guide to building agents (PDF)](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
- OpenAI, [Agents SDK](https://openai.github.io/openai-agents-python/)
- OpenAI Agents SDK, [Sandbox Agents](https://openai.github.io/openai-agents-python/sandbox_agents/), [Sandbox Concepts](https://openai.github.io/openai-agents-python/sandbox/guide/), [Sandbox clients](https://openai.github.io/openai-agents-python/sandbox/clients/) и [Agent memory](https://openai.github.io/openai-agents-python/sandbox/memory/)
- OpenAI, [Agent Builder](https://platform.openai.com/docs/guides/agent-builder)
- OpenAI, [Safety in building agents](https://platform.openai.com/docs/guides/agent-builder-safety)
- OpenAI, [Running Codex safely at OpenAI](https://openai.com/index/running-codex-safely/)
- OpenAI, [How agents are transforming work](https://openai.com/index/how-agents-are-transforming-work/)
- OpenAI, [Codex-maxxing for long-running work](https://openai.com/index/codex-maxxing-long-running-work/)
- OpenAI, [Building self-improving tax agents with Codex](https://openai.com/index/building-self-improving-tax-agents-with-codex/)
- OpenAI, [From model to agent: Equipping the Responses API with a computer environment](https://openai.com/index/equip-responses-api-computer-environment/)
- Model Context Protocol, [Security Best Practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices)
- Model Context Protocol, [Authorization specification](https://modelcontextprotocol.io/specification/draft/basic/authorization)
- Agent2Agent Protocol, [A2A specification](https://github.com/a2aproject/A2A/blob/main/docs/specification.md)
- LangGraph, [Overview](https://docs.langchain.com/oss/javascript/langgraph)
- LangGraph, [Durable execution](https://docs.langchain.com/oss/javascript/langgraph/durable-execution)
- LangGraph, [Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)
- LangGraph, [Memory overview](https://docs.langchain.com/oss/python/langgraph/memory)
- LangChain, [Multi-agent](https://docs.langchain.com/oss/python/langchain/multi-agent)
- LangChain, [The Runtime Behind Production Deep Agents](https://www.langchain.com/blog/runtime-behind-production-deep-agents)
- LangChain, [Choosing the Right Multi-Agent Architecture](https://www.langchain.com/blog/choosing-the-right-multi-agent-architecture)
- LangChain, [How to Choose the Right Sandbox for AI Agents](https://www.langchain.com/blog/how-to-choose-the-right-sandbox-for-your-agent)
- LangChain, [The Art of Loop Engineering](https://www.langchain.com/blog/the-art-of-loop-engineering)
- Google Cloud, [Achieve agentic productivity with Vertex AI Agent Builder](https://cloud.google.com/blog/products/ai-machine-learning/get-started-with-vertex-ai-agent-builder)
- Google Cloud, [More ways to build, scale, and govern AI agents with Vertex AI Agent Builder](https://cloud.google.com/blog/products/ai-machine-learning/more-ways-to-build-and-scale-ai-agents-with-vertex-ai-agent-builder)
- Google Cloud, [20 questions for the Agentic Enterprise](https://cloud.google.com/blog/products/ai-machine-learning/20-questions-for-the-agentic-enterprise)
- Google Cloud, [Vertex AI Agent Builder overview](https://docs.cloud.google.com/agent-builder/overview)
- Google Cloud Architecture Center, [Multi-agent AI system in Google Cloud](https://docs.cloud.google.com/architecture/multiagent-ai-system)
- Google Cloud, [Build agents even faster with Gemini Enterprise Agent Platform’s fully-managed, remote MCP server](https://cloud.google.com/blog/products/ai-machine-learning/gemini-enterprise-agent-platform-remote-mcp-server)
- Google, [Introducing Agent Executor: a new runtime for AI agents](https://developers.googleblog.com/en/introducing-agent-executor-a-new-runtime-for-ai-agents/)
- Google, [google/ax: Agent Executor](https://github.com/google/ax)
- Google Cloud, [Beyond Static Prompts: Building Scale-Proof, Polymorphic Multi-Agent Systems with Google's ADK](https://cloud.google.com/blog/topics/developers-practitioners/beyond-static-prompts-with-google-adk)
- Microsoft Azure Architecture Center, [AI Agent Orchestration Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)
- Cloudflare, [Build Agents on Cloudflare](https://developers.cloudflare.com/agents/)
- Cloudflare Agents SDK, [Store and sync state](https://developers.cloudflare.com/agents/api-reference/store-and-sync-state/) и [Schedule tasks](https://developers.cloudflare.com/agents/api-reference/schedule-tasks/)
- Cloudflare Agents SDK, [Human-in-the-loop patterns](https://developers.cloudflare.com/agents/concepts/agentic-patterns/human-in-the-loop/) и [WebSockets](https://developers.cloudflare.com/agents/api-reference/websockets/)
- Cloudflare Agents SDK, [Using Agents with Workflows](https://developers.cloudflare.com/agents/concepts/workflows/), [Run Workflows](https://developers.cloudflare.com/agents/runtime/execution/run-workflows/), [Durable execution](https://developers.cloudflare.com/agents/api-reference/durable-execution/) и [Durable execution with fibers](https://developers.cloudflare.com/agents/runtime/execution/durable-execution/)
- Cloudflare Agents SDK, [Long-running agents](https://developers.cloudflare.com/agents/concepts/agentic-patterns/long-running-agents/)
- Cloudflare, [Rules of Durable Objects](https://developers.cloudflare.com/durable-objects/best-practices/rules-of-durable-objects/)
- Cloudflare Changelog, [Agents SDK improves browser automation, code execution, and recovery](https://developers.cloudflare.com/changelog/post/2026-06-16-agents-sdk-v0161/)
- Cloudflare Changelog, [Outbound connections keep Durable Objects alive](https://developers.cloudflare.com/changelog/post/2026-06-19-outbound-connections-keep-dos-alive/)
- Cloudflare Changelog, [Agents SDK adds background sub-agents and a unified turn entry point](https://developers.cloudflare.com/changelog/product-group/ai/)
- Cloudflare Changelog, [Agents SDK improves browser automation, code execution, and recovery](https://developers.cloudflare.com/changelog/product-group/ai/)
- Cloudflare Blog, [Project Think: building the next generation of AI agents on Cloudflare](https://blog.cloudflare.com/project-think/)
- Cloudflare Blog, [Agents that remember: introducing Agent Memory](https://blog.cloudflare.com/introducing-agent-memory/)
- Cloudflare Changelog, [Temporary Accounts: From agent deployments to claimed accounts](https://developers.cloudflare.com/changelog/2026-06-22-temporary-accounts/)
- Cloudflare Blog, [Introducing Dynamic Workflows: durable execution that follows the user, not the other way around](https://blog.cloudflare.com/dynamic-workflows/)
- Cloudflare Blog, [How we built saga rollbacks for Cloudflare Workflows](https://blog.cloudflare.com/rollbacks-for-workflows/)
- Cloudflare Blog, [Build your own vulnerability harness](https://blog.cloudflare.com/build-your-own-vulnerability-harness/)
- Cloudflare Blog, [Bringing more agent harnesses and frameworks to Cloudflare, starting with Flue](https://blog.cloudflare.com/agents-platform-flue-sdk/)
- Cloudflare, [Build and deploy Remote Model Context Protocol (MCP) servers to Cloudflare](https://blog.cloudflare.com/remote-model-context-protocol-servers-mcp/)
- Cloudflare, [Scaling MCP adoption: reference architecture for safer enterprise MCP](https://blog.cloudflare.com/enterprise-mcp/)
- Cloudflare, [Connect your AI agents to MCP servers with Cloudflare Access](https://blog.cloudflare.com/zero-trust-mcp-server-portals/)
- Cloudflare, [Code Mode: give agents an entire API in 1,000 tokens](https://blog.cloudflare.com/code-mode-mcp/)
- Cloudflare Blog, [Your site, your rules: new AI traffic options for all customers](https://blog.cloudflare.com/content-independence-day-ai-options/)
- Cloudflare Blog, [Announcing the Monetization Gateway](https://blog.cloudflare.com/monetization-gateway/)
- GitHub Docs, [GitHub Copilot cloud agent](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent)
- GitHub Docs, [Using Copilot cloud agent on GitHub](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-on-github) и [Configuring settings for GitHub Copilot cloud agent](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/configuring-agent-settings)
- GitHub Changelog, [Browser tools for GitHub Copilot in VS Code are generally available](https://github.blog/changelog/2026-07-01-browser-tools-for-github-copilot-in-vs-code-are-generally-available/)
- GitHub Changelog, [Agent finder for GitHub Copilot now available](https://github.blog/changelog/2026-06-17-agent-finder-for-github-copilot-now-available/)
- GitHub Changelog, [GitHub Copilot in Visual Studio Code, June 2026 releases](https://github.blog/changelog/2026-07-08-github-copilot-in-visual-studio-code-june-2026-releases/)
- GitHub Blog, [Under the hood: Security architecture of GitHub Agentic Workflows](https://github.blog/ai-and-ml/generative-ai/under-the-hood-security-architecture-of-github-agentic-workflows/)
- GitHub Agentic Workflows, [Security Architecture](https://github.github.com/gh-aw/introduction/architecture/)
- GitHub Blog, [How we built an internal data analytics agent](https://github.blog/ai-and-ml/github-copilot/how-we-built-an-internal-data-analytics-agent/)
- GitHub Blog, [Evaluating performance and efficiency of the GitHub Copilot agentic harness across models and tasks](https://github.blog/ai-and-ml/github-copilot/evaluating-performance-and-efficiency-of-the-github-copilot-agentic-harness-across-models-and-tasks/)
- GitHub Changelog, [Security validation for third-party coding agents](https://github.blog/changelog/2026-06-09-security-validation-for-third-party-coding-agents/)
- GitHub Changelog, [Agentic autofix for code scanning alerts in public preview](https://github.blog/changelog/2026-07-10-agentic-autofix-for-code-scanning-alerts-in-public-preview/)
- GitHub Changelog, [Secret scanning with GitHub MCP Server is now generally available](https://github.blog/changelog/2026-05-05-secret-scanning-with-github-mcp-server-is-now-generally-available/)
- GitHub Blog, [Building an agentic memory system for GitHub Copilot](https://github.blog/ai-and-ml/github-copilot/building-an-agentic-memory-system-for-github-copilot/)
- GitHub Blog, [GitHub Copilot is moving to usage-based billing](https://github.blog/news-insights/company-news/github-copilot-is-moving-to-usage-based-billing/)
- GitHub Changelog, [GitHub Copilot code review will start consuming GitHub Actions minutes on June 1, 2026](https://github.blog/changelog/2026-04-27-github-copilot-code-review-will-start-consuming-github-actions-minutes-on-june-1-2026/)
- GitHub Docs, [About GitHub Copilot Memory](https://docs.github.com/copilot/concepts/agents/copilot-memory)
- arXiv, [Adoption and Impact of Command-Line AI Coding Agents: A Study of Microsoft's Early 2026 Rollout of Claude Code and GitHub Copilot CLI](https://arxiv.org/abs/2607.01418)

## Наблюдаемость, оценки и дизайн проверяющих

- OpenAI, [Agent evals](https://platform.openai.com/docs/guides/agent-evals)
- OpenAI, [Separating signal from noise in coding evaluations](https://openai.com/index/separating-signal-from-noise-coding-evaluations/)
- OpenAI, [Deprecations](https://developers.openai.com/api/docs/deprecations)
- OpenAI, [Predicting model behavior before release by simulating deployment](https://openai.com/index/deployment-simulation/)
- OpenAI, [How we monitor internal coding agents for misalignment](https://openai.com/index/how-we-monitor-internal-coding-agents-misalignment/)
- OpenAI, [Trace grading](https://platform.openai.com/docs/guides/trace-grading)
- OpenAI, [Background mode](https://developers.openai.com/api/docs/guides/background)
- OpenAI, [Using tools](https://developers.openai.com/api/docs/guides/tools)
- OpenAI, [Structured model outputs](https://developers.openai.com/api/docs/guides/structured-outputs)
- OpenAI, [Introducing AgentKit](https://openai.com/index/introducing-agentkit/)
- OpenAI, [Secure MCP Tunnel](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels)
- OpenAI, [Making private MCP servers reachable without making them public](https://developers.openai.com/blog/connect-private-mcp-servers-to-openai-products)
- GitHub Changelog, [Schedule and automate tasks with Copilot cloud agent](https://github.blog/changelog/2026-06-02-schedule-and-automate-tasks-with-copilot-cloud-agent/)
- GitHub Changelog, [Copilot code review: AGENTS.md support and UI improvements](https://github.blog/changelog/2026-06-18-copilot-code-review-agents-md-support-and-ui-improvements/)
- GitHub Changelog, [GitHub Copilot app support for BYOK](https://github.blog/changelog/2026-06-23-github-copilot-app-support-for-byok/)
- GitHub Blog, [Better tools made Copilot code review worse. Here's how we actually improved it](https://github.blog/ai-and-ml/github-copilot/better-tools-made-copilot-code-review-worse-heres-how-we-actually-improved-it/)
- Cloudflare Changelog, [Spend limits are now available for AI Gateway](https://developers.cloudflare.com/changelog/post/2026-06-05-spend-limits/)
- Cloudflare Docs, [AI Gateway spend limits](https://developers.cloudflare.com/ai-gateway/features/spend-limits/)
- Cloudflare Docs, [AI Gateway: Coding Agents](https://developers.cloudflare.com/ai-gateway/integrations/coding-agents/)
- LangChain, [State of Agent Engineering](https://www.langchain.com/state-of-agent-engineering)
- LangChain, [Agent Evaluation Readiness Checklist](https://www.langchain.com/blog/agent-evaluation-readiness-checklist)
- Microsoft Learn, [Observability for Generative AI and agentic AI systems](https://learn.microsoft.com/en-us/security/zero-trust/sfi/observability-ai-systems)
- Microsoft Azure AI Foundry Blog, [AI Observability Starter Kit for Microsoft Foundry agents](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/ai-observability-starter-kit-for-microsoft-foundry-agents/4522751)
- Microsoft Azure AI Foundry Blog, [Monitoring & Observability in Microsoft Foundry, Part 2: Configuration and Operations](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/monitoring--observability-in-microsoft-foundry-part-2-configuration-and-operatio/4532674)
- Microsoft Azure Blog, [From insight to action: The next phase of agentic cloud operations](https://azure.microsoft.com/en-us/blog/from-insight-to-action-the-next-phase-of-agentic-cloud-operations/)
- Google Cloud, [Observability and monitoring](https://docs.cloud.google.com/docs/observability)
- Google Cloud, [Evaluate your agents](https://docs.cloud.google.com/gemini-enterprise-agent-platform/optimize/evaluation/evaluate-agents)
- Google Cloud, [Continuous evaluation with online monitors](https://docs.cloud.google.com/gemini-enterprise-agent-platform/optimize/evaluation/evaluate-online)
- Google Cloud Blog, [Evaluate agent performance](https://cloud.google.com/blog/products/data-analytics/evaluate-agent-performance)
- AWS, [AgentOps: Operationalize agentic AI at scale with Amazon Bedrock AgentCore](https://aws.amazon.com/blogs/machine-learning/agentops-operationalize-agentic-ai-at-scale-with-amazon-bedrock-agentcore/)
- AWS, [It’s safe to close your laptop now: Hosting coding agents on Amazon Bedrock AgentCore](https://aws.amazon.com/blogs/machine-learning/its-safe-to-close-your-laptop-now-hosting-coding-agents-on-amazon-bedrock-agentcore/)
- AWS, [Debugging production agents with Amazon Bedrock AgentCore Observability](https://aws.amazon.com/blogs/machine-learning/debugging-production-agents-with-amazon-bedrock-agentcore-observability/)
- AWS, [Evaluate AI agents systematically with Agent-EvalKit](https://aws.amazon.com/blogs/machine-learning/evaluate-ai-agents-systematically-with-agent-evalkit/)
- AWS, [ToolSimulator: scalable tool testing for AI agents](https://aws.amazon.com/blogs/machine-learning/toolsimulator-scalable-tool-testing-for-ai-agents/)
- AWS, [MCP tool design: practical approaches and tradeoffs](https://aws.amazon.com/blogs/machine-learning/mcp-tool-design-practical-approaches-and-tradeoffs/)
- AWS Prescriptive Guidance, [Design tools for AI agents](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/tool-design.html)
- AWS, [Secure AI agents with Policy and Lambda interceptors in Amazon Bedrock AgentCore gateway](https://aws.amazon.com/blogs/machine-learning/secure-ai-agents-with-policy-and-lambda-interceptors-in-amazon-bedrock-agentcore-gateway/)
- AWS, [How Smartsheet built a remote MCP server on AWS](https://aws.amazon.com/blogs/machine-learning/how-smartsheet-built-a-remote-mcp-server-on-aws/)
- AWS, [Introducing stateful MCP client capabilities on Amazon Bedrock AgentCore Runtime](https://aws.amazon.com/blogs/machine-learning/introducing-stateful-mcp-client-capabilities-on-amazon-bedrock-agentcore-runtime/)
- AWS, [Extending MCP support for Amazon Bedrock AgentCore Gateway](https://aws.amazon.com/blogs/machine-learning/extending-mcp-support-for-amazon-bedrock-agentcore-gateway-2/)
- AWS Open Source Blog, [Governing AI Assets at Scale with MCP Gateway and Registry](https://aws.amazon.com/blogs/opensource/governing-ai-assets-at-scale-with-mcp-gateway-and-registry/)
- arXiv, [The Art of Building Verifiers for Computer Use Agents](https://arxiv.org/abs/2604.06240v1)
- GitHub, [microsoft/fara](https://github.com/microsoft/fara)

## HCI, HITL и человеческий надзор

- Microsoft Research, [Guidelines for Human-AI Interaction](https://www.microsoft.com/en-us/research/publication/guidelines-for-human-ai-interaction/)
- LangChain Deep Agents, [Human-in-the-loop](https://docs.langchain.com/oss/javascript/deepagents/human-in-the-loop)
- LangGraph, [Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)
- OpenReview, [The Illusion of Consensus in Human-Centered Interactive AI](https://openreview.net/forum?id=eJtBEBmYGB) *(demoted research lead; не primary evidence для финального редакторского пакета)*
- Microsoft Learn, [Agentic AI adoption maturity model](https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/maturity-model-overview)

## Управление, безопасность и операционная гарантия

- Google Cloud, [How Google secures AI Agents](https://cloud.google.com/blog/products/identity-security/cloud-ciso-perspectives-how-google-secures-ai-agents)
- Google Cloud, [Recommended AI Controls framework](https://cloud.google.com/blog/products/identity-security/audit-smarter-introducing-our-recommended-ai-controls-framework)
- Google Cloud, [Introducing Agent Sandbox](https://cloud.google.com/blog/products/containers-kubernetes/agentic-ai-on-kubernetes-and-gke/)
- Google DeepMind, [Securing the future of AI agents](https://deepmind.google/blog/securing-the-future-of-ai-agents/)
- AWS Security Blog, [Secure AI agent access patterns to AWS resources using Model Context Protocol](https://aws.amazon.com/blogs/security/secure-ai-agent-access-patterns-to-aws-resources-using-model-context-protocol/)
- Google Research, [Security Assurance in the Age of Generative AI](https://research.google/pubs/security-assurance-in-the-age-of-generative-ai/)
- Google Research, [Securing the AI Software Supply Chain](https://research.google/pubs/securing-the-ai-software-supply-chain/)
- Google Research, [An Introduction to Google’s Approach for Secure AI Agents](https://research.google/pubs/an-introduction-to-googles-approach-for-secure-ai-agents/)
- Google Research, [Identifying and Mitigating the Security Risks of Generative AI](https://research.google/pubs/identifying-and-mitigating-the-security-risks-of-generative-ai/)
- Anthropic, [Claude Code Security](https://docs.anthropic.com/en/docs/claude-code/security)
- Anthropic, [Responsible Scaling Policy](https://www.anthropic.com/responsible-scaling-policy)
- Anthropic, [Frontier Safety Roadmap](https://www.anthropic.com/responsible-scaling-policy/roadmap)
- Anthropic, [Redeploying Fable 5](https://www.anthropic.com/news/redeploying-fable-5)
- Anthropic, [Agentic Misalignment](https://www.anthropic.com/research/agentic-misalignment)
- Anthropic, [Strengthening Red Teams](https://alignment.anthropic.com/2025/strengthening-red-teams/)
- Anthropic, [Introducing Bloom](https://www.anthropic.com/research/bloom)
- Anthropic, [Findings from a Pilot Anthropic-OpenAI Alignment Evaluation Exercise](https://alignment.anthropic.com/2025/openai-findings/)
- MLCommons, [AILuminate v1.0 Release](https://mlcommons.org/2024/12/mlcommons-ailuminate-v1-0-release/)
- Microsoft Learn, [Secure autonomous agentic AI systems](https://learn.microsoft.com/en-us/security/zero-trust/sfi/secure-agentic-systems)
- Microsoft Learn, [Reduce autonomous agentic AI risk](https://learn.microsoft.com/en-us/security/zero-trust/sfi/manage-agentic-risk)
- Microsoft Learn, [Complete production infrastructure inventory](https://learn.microsoft.com/en-us/security/zero-trust/sfi/complete-production-infrastructure-inventory)
- Microsoft Learn, [Agent Registry convergence with Microsoft Agent 365](https://learn.microsoft.com/en-us/entra/agent-id/identity-platform/agent-registry-convergence)
- Microsoft Foundry Blog, [Build agents you can trust across any framework with open evals and a control standard](https://devblogs.microsoft.com/foundry/build-2026-open-trust-stack-ai-agents/)
- Microsoft Learn, [Convert agent traces into evaluation datasets](https://learn.microsoft.com/en-us/azure/foundry/observability/how-to/traces-to-dataset)
- Microsoft Research, [Systematic debugging for AI agents: introducing the AgentRx framework](https://www.microsoft.com/en-us/research/blog/systematic-debugging-for-ai-agents-introducing-the-agentrx-framework/)
- Microsoft Research, [AgentRx: Diagnosing AI Agent Failures from Execution Trajectories](https://www.microsoft.com/en-us/research/publication/agentrx-diagnosing-ai-agent-failures-from-execution-trajectories/)
- GitHub, [microsoft/AgentRx](https://github.com/microsoft/AgentRx)

## Инциденты и кейсы

- Civil Resolution Tribunal, [Moffatt v. Air Canada](https://decisions.civilresolutionbc.ca/crt/crtd/en/item/525448/index.do)
- American Bar Association, [BC Tribunal Confirms Companies Remain Liable for Information Provided by AI Chatbot](https://www.americanbar.org/groups/business_law/resources/business-law-today/2024-february/bc-tribunal-confirms-companies-remain-liable-information-provided-ai-chatbot/)
- Microsoft Security Blog, [When prompts become shells: RCE vulnerabilities in AI agent frameworks](https://www.microsoft.com/en-us/security/blog/2026/05/07/prompts-become-shells-rce-vulnerabilities-ai-agent-frameworks/)
- Microsoft Security Blog, [AutoJack: How a single page can RCE the host running your AI agent](https://www.microsoft.com/en-us/security/blog/2026/06/18/autojack-single-page-rce-host-running-ai-agent/)
- Microsoft Security Blog, [Securing AI agents: When AI tools move from reading to acting](https://www.microsoft.com/en-us/security/blog/2026/06/30/securing-ai-agents-ai-tools-move-from-reading-acting/)
- Microsoft Research, [Red-teaming a network of agents: Understanding what breaks when AI agents interact at scale](https://www.microsoft.com/en-us/research/blog/red-teaming-a-network-of-agents-understanding-what-breaks-when-ai-agents-interact-at-scale/)
- OpenAI, [OpenAI and Hugging Face partner to address security incident during model evaluation](https://openai.com/index/hugging-face-model-evaluation-security-incident/)
- Hugging Face, [Security incident disclosure — July 2026](https://huggingface.co/blog/security-incident-july-2026)
- arXiv, [ExploitGym: Can AI Agents Turn Security Vulnerabilities into Real Attacks?](https://arxiv.org/abs/2605.11086)

## Исследовательские leads: память, наблюдаемость и надежность многоагентных систем

_Редакционный статус 2026-06-30: OpenReview-ссылки ниже демотированы в непервичные research leads. Не использовать их как primary evidence в финальном publisher packet без отдельной ручной сверки метаданных через браузер или иной подтвержденный доступ._

- OpenReview, [EVOLVE-MEM: A Self-Adaptive Hierarchical Memory Architecture for Next-Generation Agentic AI Systems](https://openreview.net/forum?id=dfPQrg1WA5)
- OpenReview, [MemGen: Weaving Generative Latent Memory for Self-Evolving Agents](https://openreview.net/forum?id=vI56m4Iu4e)
- OpenReview, [AgentTrace: A Structured Logging Framework for Agent System Observability](https://openreview.net/forum?id=8IkLxhPY3G)
- OpenReview, [AgentTrace: Causal Graph Tracing for Root Cause Analysis in Deployed Multi-Agent Systems](https://openreview.net/forum?id=22qiB2JpzZ)
- OpenReview, [Evaluation of Multi-Turn Consistency in LLM Agents: Survival Analysis and Failure-Rationale Taxonomy](https://openreview.net/forum?id=FwFd5UFsJH)
- OpenReview, [AMA-Bench: Evaluating Long-Horizon Memory for Agentic Applications](https://openreview.net/forum?id=GoSVL7mLcM)
- OpenReview, [Aegis: Automated Error Generation and Attribution for Multi-Agent Systems](https://openreview.net/forum?id=zqcYoxXiN3)
- OpenReview, [PALADIN: Self-Correcting Language Model Agents to Cure Tool-Failure Cases](https://openreview.net/forum?id=NVTtoO297p)
- OpenReview, [Why Do Multiagent Systems Fail?](https://openreview.net/forum?id=wM521FqPvI)
- arXiv, [Symphony: A Decentralized Multi-Agent Framework for Scalable Collective Intelligence](https://arxiv.org/abs/2508.20019)
- arXiv, [SYMPHONY: Synergistic Multi-agent Planning with Heterogeneous Language Model Assembly](https://arxiv.org/abs/2601.22623)

## Публикация, сборка и платформенный слой книги

- MkDocs, [Official documentation](https://www.mkdocs.org/)
- Material for MkDocs, [Official documentation](https://squidfunk.github.io/mkdocs-material/)
- uv, [Working on projects](https://docs.astral.sh/uv/guides/projects/)
- ty, [Official documentation](https://docs.astral.sh/ty/)
- Starlight, [Official documentation](https://starlight.astro.build/)

## Rust и инфраструктурный слой агентных рантаймов

- AWS, [AWS SDK for Rust is generally available](https://aws.amazon.com/about-aws/whats-new/2023/11/aws-sdk-rust/)
- AWS Docs, [Code examples for Amazon Bedrock Runtime using AWS SDK for Rust](https://docs.aws.amazon.com/sdk-for-rust/latest/dg/rust_bedrock-runtime_code_examples.html)
- docs.rs, [aws-sdk-bedrockagentruntime](https://docs.rs/aws-sdk-bedrockagentruntime/latest/aws_sdk_bedrockagentruntime/)
- Microsoft Learn, [Azure SDK for Rust](https://learn.microsoft.com/en-us/azure/developer/rust/sdk/overview)
- Rig, [Official documentation](https://docs.rig.rs/)
- docs.rs, [rig-core](https://docs.rs/rig-core)
- GitHub, [0xPlaygrounds/rig](https://github.com/0xPlaygrounds/rig)

## Как использовать этот список

Если развивать книгу дальше, удобнее идти в таком порядке:

1. Нормативный каркас риска и контроля: NIST, OWASP, CISA.
2. Архитектурные паттерны и дисциплина среды исполнения: Anthropic, OpenAI, LangGraph, Google Cloud, Microsoft.
3. Наблюдаемость, оценки и слой проверяющих: OpenAI, Microsoft, arXiv, GitHub.
4. HCI, HITL и кейсы: Microsoft Research, LangGraph/LangChain HITL, официальный CRT source по Air Canada.
5. Исследовательские leads: память, согласованность поведения, наблюдаемость и режимы отказа многоагентных систем; OpenReview использовать только как непервичный lead до отдельной сверки.

Для чтения самой книги полезно держать еще одну развилку:

- `Устойчивое ядро`: нормативные рамки, архитектура, политики, выполнение и наблюдаемость.
- `Быстро меняющийся слой`: инструменты оценивания, дизайн проверяющих, управление реестром, свежие исследования и свежие кейсы.
