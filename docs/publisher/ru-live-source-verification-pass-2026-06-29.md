# P0 live source verification pass

Date: 2026-06-29.

Status: representative P0 live-pass for fast-moving platform, security,
governance and protocol sources. This is not a complete verification of every
source in the bibliography.

## Method

The pass checked primary source URLs with live HTTP requests and browser opens
where appropriate. Results below are limited to the checked representative
pages. Claims that depend on the full source catalog still require a final
source-review pass before publisher submission.

## Checked sources

| Source group | Representative URL checked | Result | Manuscript action |
| --- | --- | --- | --- |
| OpenAI agents | <https://developers.openai.com/api/docs/guides/agents-sdk> | HTTP 301 to `/api/docs/guides/agents`, then HTTP 200. | Record redirect; use current Agents guide URL in future source cleanup. |
| OpenAI agent evals | <https://platform.openai.com/docs/guides/agent-evals> | HTTP 301 to `developers.openai.com/api/docs/guides/agent-evals`, then HTTP 200. | Record redirect; keep claims generalized. |
| OpenAI structured outputs | <https://developers.openai.com/api/docs/guides/structured-outputs> | HTTP 200. | No immediate manuscript change beyond current source-date note. |
| Anthropic agents | <https://www.anthropic.com/engineering/building-effective-agents> | HTTP 200. | Keep as primary engineering reference. |
| Google Cloud agent platform | <https://docs.cloud.google.com/agent-builder/overview> | HTTP 301 to `/gemini-enterprise-agent-platform/overview`, then HTTP 200. | Record product/page rename risk; avoid brittle Vertex/Agent Builder wording until full pass. |
| Microsoft agent patterns | <https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns> | HTTP 200. | Keep as primary architecture reference. |
| OWASP AI Agent Security Cheat Sheet | <https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html> | HTTP 200. | Keep as primary security reference. |
| MCP security best practices | <https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices> | HTTP 200. | Keep as primary protocol-security reference. |
| NIST AI RMF | <https://www.nist.gov/itl/ai-risk-management-framework> | HTTP 200. | Keep as governance reference; full NIST/CISA batch remains open. |
| A2A specification | <https://github.com/a2aproject/A2A/blob/main/docs/specification.md> | HTTP 200. | Keep status wording conservative; avoid overstating maturity. |

## Decisions

- Do not mark the entire source catalog as fully reverified on 2026-06-29.
- Do mark the main source appendix and stale chapter banners with a P0 live-pass
  note dated 2026-06-29.
- Record redirects as follow-up cleanup items because URLs and product names
  changed for key OpenAI and Google routes.
- Keep volatile platform feature claims generalized until the full source batch
  records are filled.

## Still open

- Full OpenAI batch: Agent Builder, safety guidance, trace grading, background
  mode, tools, sandbox agents and memory.
- Full Anthropic batch: managed agents, evals, Claude Code security,
  multi-agent research and alignment/red-team references.
- LangGraph/LangChain runtime source batch.
- Cloudflare, AWS and GitHub Copilot platform source batches.
- Full OWASP family: Agentic Top 10, MCP Security Cheat Sheet, MCP Top 10,
  Tool Poisoning, Agentic Skills Top 10, Prompt Injection and RAG cheat sheets.
- Full NIST/CISA governance batch.
- Research, case and legal-reference verification.

