# Final fact-check backlog

Date: 2026-06-28.

Status: backlog for the final pre-publication source verification pass. This
file does not claim that sources were rechecked today; it defines what must be
verified before final publisher submission.

## Why this is needed

The source catalog currently says the last editorial source review was
**2026-05-17**. Several chapter-level review notes point to next planned checks
on **2026-06-14** or **2026-06-17**. As of **2026-06-28**, those planned checks
are in the past.

Before publication, every fast-changing platform/API/security claim must be
checked against current primary sources and the date of that check must be
recorded.

## P0: platform and API claims

Verify against current primary documentation:

- OpenAI Agents SDK, Agent Builder, agent safety, agent evals, trace grading,
  background mode, tools, structured outputs, sandbox agents and agent memory.
- Anthropic agent workflow taxonomy, harness design, managed agents, evals,
  Claude Code security and multi-agent research references.
- LangGraph durable execution, persistence, memory, interrupts and multi-agent
  references.
- Google Cloud Vertex AI Agent Builder, Agent Sandbox, multi-agent architecture
  and AI controls references.
- Microsoft Azure/Entra/Copilot agent orchestration, maturity, observability,
  registry and autonomous-agent security references.
- Cloudflare Agents SDK state, scheduling, HITL, WebSockets, workflows, durable
  execution and remote MCP references.
- AWS Bedrock AgentCore/stateful MCP and Rust SDK references.
- GitHub Copilot cloud agent references.

Done when:

- source URL still resolves;
- title/product name is still current;
- claim in the manuscript is still true;
- publication date or last-modified date is recorded if available;
- stale or renamed products are either updated or generalized.

## P0: security and governance sources

Verify against current primary sources:

- OWASP AI Agent Security Cheat Sheet.
- OWASP Top 10 for Agentic Applications for 2026.
- OWASP MCP Security Cheat Sheet.
- OWASP MCP Tool Poisoning.
- OWASP MCP Top 10.
- OWASP Agentic Skills Top 10.
- OWASP Prompt Injection and RAG Security cheat sheets.
- NIST AI RMF 1.0.
- NIST Generative AI Profile.
- NIST SP 800-53 Rev. 5.
- NIST SP 800-218A.
- NIST adversarial ML taxonomy.
- CISA AI guidance.

Done when:

- names and versions match the current documents;
- no draft/final status is misrepresented;
- claims are phrased as guidance, not legal/compliance guarantees.

## P0: current-date chapter notes

Review and either remove from the print manuscript or update:

- `docs/book/part-v/chapter-13.md`: review note says next planned check was
  **2026-06-17**.
- `docs/book/part-iv/chapter-9.md`: review note says next planned check was
  **2026-06-17**.
- `docs/book/part-viii/chapter-20.md`: review note says next planned check was
  **2026-06-14**.
- `docs/book/part-viii/chapter-21.md`: review note says next planned check was
  **2026-06-17**.
- `docs/book/part-viii/chapter-22.md`: review note says next planned check was
  **2026-06-14**.
- `docs/book/part-viii/chapter-24.md`: review note says next planned check was
  **2026-06-17**.
- `docs/book/part-viii/chapter-25.md`: review note says next planned check was
  **2026-06-17**.
- `docs/book/part-viii/chapter-26.md`: review note says next planned check was
  **2026-06-17**.
- `docs/book/part-viii/chapter-27.md`: review note says next planned check was
  **2026-06-17**.

Done when:

- internal review notes are not printed as reader-facing stale metadata;
- source review date in `docs/appendix/sources.md` is updated after real
  verification;
- the Google Doc and Markdown agree.

## P1: protocol terminology

Verify current naming and status:

- MCP server/client/host terminology.
- MCP authorization specification status.
- Stateful vs stateless MCP claims.
- A2A specification status and relation to MCP.
- Agent registry, inventory and identity terminology in Microsoft/Google
  materials.

Done when:

- terms match primary sources;
- draft specs are called drafts where appropriate;
- the book does not imply universal standardization before it exists.

## P1: research frontier

Verify that research references are still appropriate and not overclaimed:

- memory architecture papers;
- agent trace/observability papers;
- verifier and trace-grading sources;
- multi-agent failure and reliability papers;
- HCI/HITL sources;
- incident/legal case references.

Done when:

- claims are framed as examples or research signals unless broadly established;
- no paper is treated as production consensus without evidence;
- legal/case references include jurisdiction and date.

## P1: model names and examples

Review examples that contain concrete model names or dated values:

- `allowed_models: ["gpt-5.4", "gpt-5-mini"]` in appendix policy examples;
- `model_route: gpt-5.4-tools` in lifecycle examples;
- dated release IDs, bundle IDs, trace IDs and incident IDs used as examples.

Done when:

- synthetic examples are clearly examples;
- model names are either current and intentional, or replaced by neutral
  placeholders;
- dated IDs are not mistaken for claims about real releases.

## P2: source catalog hygiene

Before final handoff:

- remove links that are no longer primary or stable;
- prefer official docs/research pages over secondary summaries;
- keep source categories aligned with book sections;
- add last-checked date after verification;
- keep non-print source catalogs in companion if the list grows too long.

## Verification record template

For each checked source, record:

```text
Source:
URL:
Checked on:
Primary/secondary:
Relevant manuscript locations:
Result: unchanged / updated / removed / generalized
Notes:
```
