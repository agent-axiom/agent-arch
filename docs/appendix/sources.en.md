# Sources

Below is the main set of primary sources used by the current version of the book. Access date: **April 22, 2026**.

!!! info "How to read this list"
    It is useful to separate these sources not only by topic, but also by the strength of support they provide:

    - `Normative frame`: NIST, OWASP, CISA, and related documents that define stable governance contours;
    - `Platform practice`: OpenAI, Anthropic, LangGraph, Google Cloud, Microsoft, and similar material showing how teams assemble those contours in production;
    - `HCI, HITL, and human oversight`: sources that show where automation fails and how to keep a human in the loop;
    - `Research frontier`: newer papers on memory, observability, verifier design, and multi-agent reliability.

    If you need the strongest base for Parts I, V, and VIII, start with the normative frame and the HCI/HITL layer. If you need current engineering practice, read the platform docs and recent research, but always pay attention to publication dates.

## Normative Frameworks and Governance Contours

- OWASP, [LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
- NIST, [AI RMF 1.0](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10)
- NIST, [AI RMF: Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- NIST, [SP 800-53 Rev. 5: Security and Privacy Controls for Information Systems and Organizations](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
- NIST, [SP 800-218A: Secure Software Development Practices for Generative AI and Dual-Use Foundation Models](https://csrc.nist.gov/pubs/sp/800/218/a/final)
- NIST, [Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations](https://www.nist.gov/publications/adversarial-machine-learning-taxonomy-and-terminology-attacks-and-mitigations-0)
- CISA, [Artificial Intelligence](https://www.cisa.gov/ai)

## Agent Architecture and Platform Patterns

- Dmitry Vikulin, [Architecture of Reliable AI Agents](https://vikulin.ai/library/tpost/ai_agent_architecture)
- Anthropic, [Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
- OpenAI, [A practical guide to building agents (PDF)](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
- OpenAI, [Agents SDK](https://developers.openai.com/api/docs/guides/agents-sdk)
- OpenAI, [Agent Builder](https://platform.openai.com/docs/guides/agent-builder)
- LangGraph, [Overview](https://docs.langchain.com/oss/javascript/langgraph)
- LangGraph, [Durable execution](https://docs.langchain.com/oss/javascript/langgraph/durable-execution)
- LangGraph, [Memory overview](https://docs.langchain.com/oss/python/langgraph/memory)
- LangChain, [Multi-agent](https://docs.langchain.com/oss/python/langchain/multi-agent)
- Google Cloud, [Achieve agentic productivity with Vertex AI Agent Builder](https://cloud.google.com/blog/products/ai-machine-learning/get-started-with-vertex-ai-agent-builder)
- Google Cloud, [More ways to build, scale, and govern AI agents with Vertex AI Agent Builder](https://cloud.google.com/blog/products/ai-machine-learning/more-ways-to-build-and-scale-ai-agents-with-vertex-ai-agent-builder)
- Google Cloud, [Vertex AI Agent Builder overview](https://docs.cloud.google.com/agent-builder/overview)
- Google Cloud Architecture Center, [Multi-agent AI system in Google Cloud](https://docs.cloud.google.com/architecture/multiagent-ai-system)
- Microsoft Azure Architecture Center, [AI Agent Orchestration Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)
- Cloudflare, [Build and deploy Remote Model Context Protocol (MCP) servers to Cloudflare](https://blog.cloudflare.com/remote-model-context-protocol-servers-mcp/)

## Observability, Evals, and Verifier Design

- OpenAI, [Agent evals](https://platform.openai.com/docs/guides/agent-evals)
- OpenAI, [Trace grading](https://platform.openai.com/docs/guides/trace-grading)
- OpenAI, [Background mode](https://developers.openai.com/api/docs/guides/background)
- OpenAI, [Using tools](https://developers.openai.com/api/docs/guides/tools)
- OpenAI, [Structured model outputs](https://developers.openai.com/api/docs/guides/structured-outputs)
- Microsoft Learn, [Observability for Generative AI and agentic AI systems](https://learn.microsoft.com/en-us/security/zero-trust/sfi/observability-ai-systems)
- Google Cloud, [Observability and monitoring](https://docs.cloud.google.com/docs/observability)
- AWS, [Introducing stateful MCP client capabilities on Amazon Bedrock AgentCore Runtime](https://aws.amazon.com/blogs/machine-learning/introducing-stateful-mcp-client-capabilities-on-amazon-bedrock-agentcore-runtime/)
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
- Google Research, [Security Assurance in the Age of Generative AI](https://research.google/pubs/security-assurance-in-the-age-of-generative-ai/)
- Google Research, [Securing the AI Software Supply Chain](https://research.google/pubs/securing-the-ai-software-supply-chain/)
- Google Research, [An Introduction to Google’s Approach for Secure AI Agents](https://research.google/pubs/an-introduction-to-googles-approach-for-secure-ai-agents/)
- Google Research, [Identifying and Mitigating the Security Risks of Generative AI](https://research.google/pubs/identifying-and-mitigating-the-security-risks-of-generative-ai/)
- Anthropic, [Claude Code Security](https://docs.anthropic.com/en/docs/claude-code/security)
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
