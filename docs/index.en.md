# Secure AI Agent Architecture

A modern practical book for engineers and platform leaders who want to build not demo agents, but production systems that are observable, controllable, and safe.

> This book takes Dmitry Vikulin's article on reliable AI agents as a starting point and expands it into a platform architecture with governance, policy enforcement, human approval, observability, evals, and operational controls.

[Open the book plan](book/plan.md){ .md-button .md-button--primary }
[Read Part I](book/part-i/index.md){ .md-button }
[View sources](appendix/sources.md){ .md-button }

## Where to invest first

This interactive chart is a quick rule of thumb: in most real systems, control, safety, and observability deserve attention earlier than maximum autonomy.

<div class="plot-card" data-plot="agent-priority"></div>

## What is inside

- Architectural patterns: workflow, router, planner, subagents, human-in-the-loop.
- Security: IAM, policy-as-code, prompt injection defenses, sandboxing, data boundaries.
- Reliability: checkpoints, idempotency, retries, graceful degradation.
- Transparency: traces, metrics, evals, regression control.
- Platform design: gateways, shared runtime, knowledge plane, tool plane, control plane.

## The main idea

The most common mistake in agent systems is to start with autonomy instead of controllability. Practice from Anthropic, OpenAI, LangGraph, and enterprise platforms from Google points to a more stable path:

1. Build a **predictable workflow** first.
2. Add autonomy **locally and measurably**.
3. Route all risky actions through **policy, approval, and tracing**.
4. Keep quality through **evals and telemetry**, not promises about the model.

## Why MkDocs was selected

`MkDocs + Material for MkDocs` still remains a pragmatic choice in 2026 for a Python-first documentation book: it is actively maintained, fast to build, and fits naturally with a Markdown workflow and a Python toolchain based on `uv`.[^mkdocs][^material][^uv]

If the project later needs richer UI components and MDX-style composition, `Astro Starlight` is the most likely upgrade path. For the first public version, however, the Python-first stack is simpler and more reliable.[^starlight]

## Sources behind this architecture

- Original framing for the agent building blocks: [vikulin.ai](https://vikulin.ai/library/tpost/ai_agent_architecture)
- "Workflow before agents": [Anthropic, Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- Durable execution, memory, and HITL: [LangGraph docs](https://docs.langchain.com/oss/javascript/langgraph)
- Tracing and agent evals: [OpenAI docs](https://developers.openai.com/api/docs/guides/agents-sdk)
- Risk management and security controls: [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework), [OWASP Prompt Injection Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)

[^mkdocs]: [MkDocs User Guide](https://www.mkdocs.org/).
[^material]: [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).
[^uv]: [uv project guide](https://docs.astral.sh/uv/guides/projects/).
[^starlight]: [Starlight documentation](https://starlight.astro.build/).
