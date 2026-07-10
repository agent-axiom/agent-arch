# Sources

Below is the main set of primary sources used by the current version of the book. Last editorial source review: **June 26, 2026**.

!!! info "How to read this list"
    It is useful to separate these sources not only by topic, but also by the strength of support they provide:

    - `Normative frame`: NIST, OWASP, CISA, and related documents that define stable governance contours;
    - `Platform practice`: OpenAI, Anthropic, LangGraph, Google Cloud, Microsoft, and similar material showing how teams assemble those contours in production;
    - `HCI, HITL, and human oversight`: sources that show where automation fails and how to keep a human in the loop;
    - `Research frontier`: newer papers on memory, observability, verifier design, and multi-agent reliability.

    If you need the strongest base for Parts I, V, and VIII, start with the normative frame and the HCI/HITL layer. If you need current engineering practice, read the platform docs and recent research, but always pay attention to publication dates.

!!! note "Canonical source routes"
    Use the sources as a fast route for the three canonical cases. **Support triage** starts with OWASP, OpenAI agent guides, HITL sources, policy/approval material, trace grading, and incident cases. **Internal knowledge assistant** starts with LangGraph memory, OpenAI Agent memory, retrieval/eval sources, provenance-oriented governance, and the memory research frontier. **Incident coordination** starts with NIST/AI RMF, Google/Microsoft governance, observability sources, multi-agent reliability research, incident review, and rollout/control-plane material.

## Normative Frameworks and Governance Contours

### Agent-specific security

- OWASP, [AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)
- OWASP, [MCP Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/MCP_Security_Cheat_Sheet.html)
- OWASP, [LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
- OWASP, [RAG Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/RAG_Security_Cheat_Sheet.html)

### Governance and baseline controls

- NIST, [AI RMF 1.0](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10)
- NIST, [AI RMF: Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- NIST, [SP 800-53 Rev. 5: Security and Privacy Controls for Information Systems and Organizations](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
- NIST, [SP 800-218A: Secure Software Development Practices for Generative AI and Dual-Use Foundation Models](https://csrc.nist.gov/pubs/sp/800/218/a/final)
- NIST, [Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations](https://www.nist.gov/publications/adversarial-machine-learning-taxonomy-and-terminology-attacks-and-mitigations-0)
- CISA, [Artificial Intelligence](https://www.cisa.gov/ai)

## Agent Architecture and Platform Patterns

- Dmitry Vikulin, [Architecture of Reliable AI Agents](https://vikulin.ai/library/tpost/ai_agent_architecture)
- Anthropic, [Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
- Anthropic, [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- Anthropic, [How we contain Claude across products](https://www.anthropic.com/engineering/how-we-contain-claude)
- Anthropic, [Scaling Managed Agents: Decoupling the brain from the hands](https://www.anthropic.com/engineering/managed-agents)
- Anthropic, [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- Snowflake Documentation, [Cortex Analyst](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst)
- Databricks Documentation, [Genie Spaces](https://docs.databricks.com/aws/en/genie/)
- Microsoft Learn, [Copilot for Power BI overview](https://learn.microsoft.com/en-us/power-bi/create-reports/copilot-introduction)
- OpenAI, [A practical guide to building agents (PDF)](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
- OpenAI, [Agents SDK](https://developers.openai.com/api/docs/guides/agents-sdk)
- OpenAI Agents SDK, [Sandbox Agents](https://openai.github.io/openai-agents-python/sandbox_agents/), [Sandbox Concepts](https://openai.github.io/openai-agents-python/sandbox/guide/), [Sandbox clients](https://openai.github.io/openai-agents-python/sandbox/clients/), and [Agent memory](https://openai.github.io/openai-agents-python/sandbox/memory/)
- OpenAI, [Agent Builder](https://platform.openai.com/docs/guides/agent-builder)
- OpenAI, [Running Codex safely at OpenAI](https://openai.com/index/running-codex-safely/)
- OpenAI, [How agents are transforming work](https://openai.com/index/how-agents-are-transforming-work/)
- OpenAI, [Codex-maxxing for long-running work](https://openai.com/index/codex-maxxing-long-running-work/)
- OpenAI, [Building self-improving tax agents with Codex](https://openai.com/index/building-self-improving-tax-agents-with-codex/)
- OpenAI, [From model to agent: Equipping the Responses API with a computer environment](https://openai.com/index/equip-responses-api-computer-environment/)
- LangGraph, [Overview](https://docs.langchain.com/oss/javascript/langgraph)
- LangGraph, [Durable execution](https://docs.langchain.com/oss/javascript/langgraph/durable-execution)
- LangGraph, [Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)
- LangGraph, [Memory overview](https://docs.langchain.com/oss/python/langgraph/memory)
- LangChain, [Multi-agent](https://docs.langchain.com/oss/python/langchain/multi-agent)
- LangChain, [The Runtime Behind Production Deep Agents](https://www.langchain.com/blog/runtime-behind-production-deep-agents)
- LangChain, [Choosing the Right Multi-Agent Architecture](https://www.langchain.com/blog/choosing-the-right-multi-agent-architecture)
- Google Cloud, [Achieve agentic productivity with Vertex AI Agent Builder](https://cloud.google.com/blog/products/ai-machine-learning/get-started-with-vertex-ai-agent-builder)
- Google Cloud, [More ways to build, scale, and govern AI agents with Vertex AI Agent Builder](https://cloud.google.com/blog/products/ai-machine-learning/more-ways-to-build-and-scale-ai-agents-with-vertex-ai-agent-builder)
- Google Cloud, [20 questions for the Agentic Enterprise](https://cloud.google.com/blog/products/ai-machine-learning/20-questions-for-the-agentic-enterprise)
- Google Cloud, [Vertex AI Agent Builder overview](https://docs.cloud.google.com/agent-builder/overview)
- Google Cloud Architecture Center, [Multi-agent AI system in Google Cloud](https://docs.cloud.google.com/architecture/multiagent-ai-system)
- Google, [Introducing Agent Executor: a new runtime for AI agents](https://developers.googleblog.com/en/introducing-agent-executor-a-new-runtime-for-ai-agents/)
- Google, [google/ax: Agent Executor](https://github.com/google/ax)
- Google Cloud, [Beyond Static Prompts: Building Scale-Proof, Polymorphic Multi-Agent Systems with Google's ADK](https://cloud.google.com/blog/topics/developers-practitioners/beyond-static-prompts-with-google-adk)
- Microsoft Azure Architecture Center, [AI Agent Orchestration Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)
- Cloudflare, [Build Agents on Cloudflare](https://developers.cloudflare.com/agents/)
- Cloudflare Agents SDK, [Store and sync state](https://developers.cloudflare.com/agents/api-reference/store-and-sync-state/) and [Schedule tasks](https://developers.cloudflare.com/agents/api-reference/schedule-tasks/)
- Cloudflare Agents SDK, [Human in the Loop](https://developers.cloudflare.com/agents/concepts/human-in-the-loop/) and [WebSockets](https://developers.cloudflare.com/agents/api-reference/websockets/)
- Cloudflare Agents SDK, [Workflows](https://developers.cloudflare.com/agents/concepts/workflows/), [Durable execution](https://developers.cloudflare.com/agents/api-reference/durable-execution/), and [Durable execution with fibers](https://developers.cloudflare.com/agents/runtime/execution/durable-execution/)
- Cloudflare Agents SDK, [Long-running agents](https://developers.cloudflare.com/agents/concepts/agentic-patterns/long-running-agents/)
- Cloudflare Changelog, [Agents SDK improves browser automation, code execution, and recovery](https://developers.cloudflare.com/changelog/post/2026-06-16-agents-sdk-v0161/)
- Cloudflare Changelog, [Agents SDK adds background sub-agents and a unified turn entry point](https://developers.cloudflare.com/changelog/product-group/ai/)
- Cloudflare Changelog, [Agents SDK improves browser automation, code execution, and recovery](https://developers.cloudflare.com/changelog/product-group/ai/)
- Cloudflare Blog, [Project Think: building the next generation of AI agents on Cloudflare](https://blog.cloudflare.com/project-think/)
- Cloudflare Changelog, [Temporary Accounts: From agent deployments to claimed accounts](https://developers.cloudflare.com/changelog/2026-06-22-temporary-accounts/)
- Cloudflare Blog, [How we built saga rollbacks for Cloudflare Workflows](https://blog.cloudflare.com/rollbacks-for-workflows/)
- Cloudflare Blog, [Build your own vulnerability harness](https://blog.cloudflare.com/build-your-own-vulnerability-harness/)
- Cloudflare Blog, [Bringing more agent harnesses and frameworks to Cloudflare, starting with Flue](https://blog.cloudflare.com/agents-platform-flue-sdk/)
- Cloudflare, [Build and deploy Remote Model Context Protocol (MCP) servers to Cloudflare](https://blog.cloudflare.com/remote-model-context-protocol-servers-mcp/)
- Cloudflare, [Scaling MCP adoption: reference architecture for safer enterprise MCP](https://blog.cloudflare.com/enterprise-mcp/)
- Cloudflare, [Code Mode: give agents an entire API in 1,000 tokens](https://blog.cloudflare.com/code-mode-mcp/)
- Cloudflare Blog, [Your site, your rules: new AI traffic options for all customers](https://blog.cloudflare.com/content-independence-day-ai-options/)
- GitHub Docs, [GitHub Copilot cloud agent](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent)
- GitHub Docs, [Using Copilot cloud agent on GitHub](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-on-github) and [Configuring settings for GitHub Copilot cloud agent](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/configuring-agent-settings)
- GitHub Changelog, [Browser tools for GitHub Copilot in VS Code are generally available](https://github.blog/changelog/2026-07-01-browser-tools-for-github-copilot-in-vs-code-are-generally-available/)
- GitHub Changelog, [GitHub Copilot in Visual Studio Code, June 2026 releases](https://github.blog/changelog/2026-07-08-github-copilot-in-visual-studio-code-june-2026-releases/)
- GitHub Blog, [Under the hood: Security architecture of GitHub Agentic Workflows](https://github.blog/ai-and-ml/generative-ai/under-the-hood-security-architecture-of-github-agentic-workflows/)
- GitHub Agentic Workflows, [Security Architecture](https://github.github.com/gh-aw/introduction/architecture/)
- GitHub Blog, [How we built an internal data analytics agent](https://github.blog/ai-and-ml/github-copilot/how-we-built-an-internal-data-analytics-agent/)
- GitHub Blog, [Evaluating performance and efficiency of the GitHub Copilot agentic harness across models and tasks](https://github.blog/ai-and-ml/github-copilot/evaluating-performance-and-efficiency-of-the-github-copilot-agentic-harness-across-models-and-tasks/)
- GitHub Changelog, [Security validation for third-party coding agents](https://github.blog/changelog/2026-06-09-security-validation-for-third-party-coding-agents/)
- GitHub Changelog, [Secret scanning with GitHub MCP Server is now generally available](https://github.blog/changelog/2026-05-05-secret-scanning-with-github-mcp-server-is-now-generally-available/)

## Observability, Evals, and Verifier Design

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
- Cloudflare Changelog, [Spend limits are now available for AI Gateway](https://developers.cloudflare.com/changelog/post/2026-06-05-spend-limits/)
- Cloudflare Docs, [AI Gateway spend limits](https://developers.cloudflare.com/ai-gateway/features/spend-limits/)
- LangChain, [State of Agent Engineering](https://www.langchain.com/state-of-agent-engineering)
- Microsoft Learn, [Observability for Generative AI and agentic AI systems](https://learn.microsoft.com/en-us/security/zero-trust/sfi/observability-ai-systems)
- Microsoft Azure AI Foundry Blog, [AI Observability Starter Kit for Microsoft Foundry agents](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/ai-observability-starter-kit-for-microsoft-foundry-agents/4522751)
- Microsoft Azure Blog, [From insight to action: The next phase of agentic cloud operations](https://azure.microsoft.com/en-us/blog/from-insight-to-action-the-next-phase-of-agentic-cloud-operations/)
- Google Cloud, [Observability and monitoring](https://docs.cloud.google.com/docs/observability)
- AWS, [AgentOps: Operationalize agentic AI at scale with Amazon Bedrock AgentCore](https://aws.amazon.com/blogs/machine-learning/agentops-operationalize-agentic-ai-at-scale-with-amazon-bedrock-agentcore/)
- AWS, [Debugging production agents with Amazon Bedrock AgentCore Observability](https://aws.amazon.com/blogs/machine-learning/debugging-production-agents-with-amazon-bedrock-agentcore-observability/)
- AWS, [Evaluate AI agents systematically with Agent-EvalKit](https://aws.amazon.com/blogs/machine-learning/evaluate-ai-agents-systematically-with-agent-evalkit/)
- AWS, [ToolSimulator: scalable tool testing for AI agents](https://aws.amazon.com/blogs/machine-learning/toolsimulator-scalable-tool-testing-for-ai-agents/)
- AWS, [Introducing stateful MCP client capabilities on Amazon Bedrock AgentCore Runtime](https://aws.amazon.com/blogs/machine-learning/introducing-stateful-mcp-client-capabilities-on-amazon-bedrock-agentcore-runtime/)
- AWS Open Source Blog, [Governing AI Assets at Scale with MCP Gateway and Registry](https://aws.amazon.com/blogs/opensource/governing-ai-assets-at-scale-with-mcp-gateway-and-registry/)
- arXiv, [The Art of Building Verifiers for Computer Use Agents](https://arxiv.org/abs/2604.06240v1)
- GitHub, [microsoft/fara](https://github.com/microsoft/fara)

## HCI, HITL, and Human Oversight

- Microsoft Research, [Guidelines for Human-AI Interaction](https://www.microsoft.com/en-us/research/publication/guidelines-for-human-ai-interaction/)
- LangChain Deep Agents, [Human-in-the-loop](https://docs.langchain.com/oss/javascript/deepagents/human-in-the-loop)
- LangGraph, [Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)
- OpenReview, [The Illusion of Consensus in Human-Centered Interactive AI](https://openreview.net/forum?id=eJtBEBmYGB)
- Microsoft Learn, [Agentic AI adoption maturity model](https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/maturity-model-overview)

## Governance, Security, and Operational Assurance

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
- Anthropic, [Agentic Misalignment](https://www.anthropic.com/research/agentic-misalignment)
- Anthropic, [Strengthening Red Teams](https://alignment.anthropic.com/2025/strengthening-red-teams/)
- Anthropic, [Introducing Bloom](https://www.anthropic.com/research/bloom)
- Anthropic, [Findings from a Pilot Anthropic-OpenAI Alignment Evaluation Exercise](https://alignment.anthropic.com/2025/openai-findings/)
- MLCommons, [AILuminate v1.0 Release](https://mlcommons.org/2024/12/mlcommons-ailuminate-v1-0-release/)
- Microsoft Learn, [Secure autonomous agentic AI systems](https://learn.microsoft.com/en-us/security/zero-trust/sfi/secure-agentic-systems)
- Microsoft Learn, [Reduce autonomous agentic AI risk](https://learn.microsoft.com/en-us/security/zero-trust/sfi/manage-agentic-risk)
- Microsoft Learn, [Complete production infrastructure inventory](https://learn.microsoft.com/en-us/security/zero-trust/sfi/complete-production-infrastructure-inventory)
- Microsoft Learn, [Agent Registry convergence with Microsoft Agent 365](https://learn.microsoft.com/en-us/entra/agent-id/identity-platform/agent-registry-convergence)

## Incidents and Cases

- American Bar Association, [BC Tribunal Confirms Companies Remain Liable for Information Provided by AI Chatbot](https://www.americanbar.org/groups/business_law/resources/business-law-today/2024-february/bc-tribunal-confirms-companies-remain-liable-information-provided-ai-chatbot/)
- Microsoft Security Blog, [When prompts become shells: RCE vulnerabilities in AI agent frameworks](https://www.microsoft.com/en-us/security/blog/2026/05/07/prompts-become-shells-rce-vulnerabilities-ai-agent-frameworks/)
- Microsoft Security Blog, [AutoJack: How a single page can RCE the host running your AI agent](https://www.microsoft.com/en-us/security/blog/2026/06/18/autojack-single-page-rce-host-running-ai-agent/)
- Microsoft Security Blog, [Securing AI agents: When AI tools move from reading to acting](https://www.microsoft.com/en-us/security/blog/2026/06/30/securing-ai-agents-ai-tools-move-from-reading-acting/)

## Research Frontier: Memory, Observability, and Multi-Agent Reliability

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

## Publishing, Build, and the Book Platform Layer

- MkDocs, [Official documentation](https://www.mkdocs.org/)
- Material for MkDocs, [Official documentation](https://squidfunk.github.io/mkdocs-material/)
- uv, [Working on projects](https://docs.astral.sh/uv/guides/projects/)
- ty, [Official documentation](https://docs.astral.sh/ty/)
- Starlight, [Official documentation](https://starlight.astro.build/)

## Rust and the Infrastructure Layer of Agent Runtimes

- AWS, [AWS SDK for Rust is generally available](https://aws.amazon.com/about-aws/whats-new/2023/11/aws-sdk-rust/)
- AWS Docs, [Code examples for Amazon Bedrock Runtime using AWS SDK for Rust](https://docs.aws.amazon.com/sdk-for-rust/latest/dg/rust_bedrock-runtime_code_examples.html)
- docs.rs, [aws-sdk-bedrockagentruntime](https://docs.rs/aws-sdk-bedrockagentruntime/latest/aws_sdk_bedrockagentruntime/)
- Microsoft Learn, [Azure SDK for Rust](https://learn.microsoft.com/en-us/azure/developer/rust/sdk/overview)
- Rig, [Official documentation](https://docs.rig.rs/)
- docs.rs, [rig-core](https://docs.rs/rig-core)
- GitHub, [0xPlaygrounds/rig](https://github.com/0xPlaygrounds/rig)

## How To Use This List

If you extend the book further, this order is convenient:

1. Risk and control framing: NIST, OWASP, CISA.
2. Architectural patterns and runtime discipline: Anthropic, OpenAI, LangGraph, Google Cloud, Microsoft.
3. Observability, evals, and verifier layers: OpenAI, Microsoft, arXiv, GitHub.
4. HCI, HITL, and cases: Microsoft Research, OpenReview, ABA.
5. Research frontier: memory, consistency, observability, and multi-agent failure modes.

For reading the book itself, one more split is useful:

- `Stable core`: normative frameworks, architecture, policy, execution, and observability;
- `Fast-moving layer`: eval tooling, verifier design, inventory governance, frontier research, and newer cases.
