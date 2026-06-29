# Source verification records

Date: 2026-06-28. Updated with full URL availability pass on 2026-06-29 and
targeted follow-up on 2026-06-30.

Status: prepared records for live verification, plus a full URL availability
pass recorded on 2026-06-29. The 2026-06-29 pass verifies URL availability, not
full semantic alignment of every source claim.

Use these records during the final source-check pass. Fill `Checked on`,
`Current source title/version`, `Result` and `Change needed` only after opening
the current primary source.

## Full source URL availability pass: 2026-06-29

Evidence:

- `docs/publisher/ru-full-source-verification-pass-2026-06-29.md`
- `docs/publisher/ru-source-url-live-check-2026-06-29.tsv`

Result:

- source URL rows checked: 106;
- HTTP 200: 102;
- HTTP 403: 3;
- HTTP 000 timeout: 1;
- OpenReview rows returned HTTP 200 but effective challenge URLs, so they
  require manual/browser or API verification before final semantic closure.

Manual follow-up remains for:

- Microsoft Research Human-AI Interaction Guidelines, blocked by HTTP 403;
- Anthropic Claude Code Security, timed out in final TSV run after an earlier
  canonical redirect observation;
- MLCommons AILuminate release page, blocked by HTTP 403;
- ABA Business Law Today Air Canada chatbot article, blocked by HTTP 403;
- OpenReview research links, challenge-gated despite HTTP 200 responses.

Editorial decision: update source appendix wording to record the 2026-06-29
full URL availability pass, but do not claim full semantic verification until
manual checks and volatile platform-route wording are closed.

## Targeted source follow-up: 2026-06-30

Evidence:

- `docs/publisher/ru-source-follow-up-pass-2026-06-30.md`
- `docs/publisher/ru-source-follow-up-live-check-2026-06-30.tsv`

Result:

- Microsoft Research Human-AI Interaction Guidelines: title/body route
  confirmed; keep source despite HEAD 403.
- Anthropic Claude Code Security: old docs route redirects to current
  `https://code.claude.com/docs/en/security`; source catalog and Russian
  chapter footnote updated.
- MLCommons AILuminate: HTTP 200 and expected title confirmed; keep source.
- Air Canada chatbot case: ABA article remains Cloudflare challenge-gated;
  Russian source catalog and chapter footnote now use official Civil Resolution
  Tribunal decision as primary source.
- OpenReview records: public page and API remain challenge-gated; keep as
  research leads only until manual browser/API metadata verification is done.

Editorial decision: the actionable URL cleanup is complete for the four
problem URLs from the automated pass. The remaining source gate is OpenReview
metadata verification plus a final semantic pass over fast-moving platform
claims before final publisher submission.

## P0 live-pass summary: 2026-06-29

Status: representative P0 live-pass completed for key primary platform,
security, governance and protocol pages. This does not close the full source
catalog.

```text
Source group: OpenAI agent platform and API docs
Representative sources checked: Agents guide, agent evals, structured outputs.
Checked on: 2026-06-29
Primary/secondary: primary
Manuscript locations: docs/appendix/sources.md; chapters 9, 13, 15, 21-23
Current source title/version: current OpenAI docs routes resolved live; Agents SDK and agent evals route through developers.openai.com.
Result: partially verified
Change needed: record redirects from platform.openai.com and agents-sdk route; keep volatile feature claims generalized until the full OpenAI batch is checked.
Reviewer: Codex
```

```text
Source group: Anthropic agent engineering and safety sources
Representative sources checked: Building Effective AI Agents.
Checked on: 2026-06-29
Primary/secondary: primary
Manuscript locations: docs/appendix/sources.md; chapters 2, 13, 18, 20
Current source title/version: live Anthropic engineering page resolved.
Result: partially verified
Change needed: keep as primary engineering reference; full Anthropic safety/evals/research batch remains open.
Reviewer: Codex
```

```text
Source group: Google Cloud agent platform and controls sources
Representative sources checked: Agent Builder overview route.
Checked on: 2026-06-29
Primary/secondary: primary
Manuscript locations: docs/appendix/sources.md; chapters 9, 18, 20, 23
Current source title/version: docs.cloud.google.com/agent-builder/overview redirects to /gemini-enterprise-agent-platform/overview.
Result: partially verified
Change needed: update product/page wording during the full source cleanup; avoid brittle Vertex/Agent Builder naming in final text.
Reviewer: Codex
```

```text
Source group: Microsoft agent architecture, observability, registry and security sources
Representative sources checked: Azure AI agent orchestration/design patterns.
Checked on: 2026-06-29
Primary/secondary: primary
Manuscript locations: docs/appendix/sources.md; chapters 13, 17-20, 23
Current source title/version: live Microsoft Learn page resolved.
Result: partially verified
Change needed: keep as primary architecture reference; observability, registry and security sub-sources remain open.
Reviewer: Codex
```

```text
Source group: OWASP agentic and GenAI security sources
Representative sources checked: AI Agent Security Cheat Sheet.
Checked on: 2026-06-29
Primary/secondary: primary
Manuscript locations: docs/appendix/sources.md; chapters 4, 7, 9, 20, 23
Current source title/version: live OWASP Cheat Sheet Series page resolved.
Result: partially verified
Change needed: keep as primary security reference; full OWASP family remains open.
Reviewer: Codex
```

```text
Source group: NIST/CISA governance and control sources
Representative sources checked: NIST AI Risk Management Framework page.
Checked on: 2026-06-29
Primary/secondary: primary
Manuscript locations: docs/appendix/sources.md; chapters 4, 17-20, 23
Current source title/version: live NIST AI RMF page resolved.
Result: partially verified
Change needed: keep as governance reference; full NIST/CISA batch remains open.
Reviewer: Codex
```

```text
Source group: MCP and A2A protocol status
Representative sources checked: MCP security best practices, A2A specification.
Checked on: 2026-06-29
Primary/secondary: primary
Manuscript locations: docs/appendix/sources.md; chapter 9; case studies; glossary
Current source title/version: live MCP docs and A2A specification page resolved.
Result: partially verified
Change needed: keep MCP/A2A maturity wording conservative; full authorization/terminology pass remains open.
Reviewer: Codex
```

## OpenAI batch

```text
Source group: OpenAI agent platform and API docs
Representative sources: Agents SDK, Agent Builder, safety in building agents,
agent evals, trace grading, background mode, tools, structured outputs,
sandbox agents, agent memory.
Checked on:
Primary/secondary: primary
Manuscript locations: docs/appendix/sources.md; chapters 9, 13, 15, 21-23
Current source title/version:
Result: pending
Change needed:
Reviewer:
```

## Anthropic batch

```text
Source group: Anthropic agent engineering and safety sources
Representative sources: Building Effective AI Agents, harness design,
managed agents, evals, Claude Code security, multi-agent research, red-team and
alignment references.
Checked on:
Primary/secondary: primary
Manuscript locations: docs/appendix/sources.md; chapters 2, 13, 18, 20
Current source title/version:
Result: pending
Change needed:
Reviewer:
```

## LangGraph batch

```text
Source group: LangGraph and LangChain agent runtime sources
Representative sources: durable execution, persistence, memory, interrupts,
multi-agent patterns.
Checked on:
Primary/secondary: primary
Manuscript locations: docs/appendix/sources.md; chapters 2, 7-9, 18
Current source title/version:
Result: pending
Change needed:
Reviewer:
```

## Google Cloud batch

```text
Source group: Google Cloud agent platform and controls sources
Representative sources: Vertex AI Agent Builder, Agent Sandbox, multi-agent
architecture, recommended AI controls, AI agent security materials.
Checked on:
Primary/secondary: primary
Manuscript locations: docs/appendix/sources.md; chapters 9, 18, 20, 23
Current source title/version:
Result: pending
Change needed:
Reviewer:
```

## Microsoft batch

```text
Source group: Microsoft agent architecture, observability, registry and
security sources
Representative sources: Azure AI agent orchestration patterns, Copilot Studio
maturity model, observability for agentic AI, secure autonomous agentic AI
systems, agent registry convergence.
Checked on:
Primary/secondary: primary
Manuscript locations: docs/appendix/sources.md; chapters 13, 17-20, 23
Current source title/version:
Result: pending
Change needed:
Reviewer:
```

## Cloudflare and AWS batch

```text
Source group: Cloudflare Agents SDK and AWS AgentCore/stateful MCP sources
Representative sources: Cloudflare Agents, state, scheduling, HITL,
WebSockets, workflows, durable execution, remote MCP; AWS stateful MCP client
capabilities and Rust SDK references.
Checked on:
Primary/secondary: primary
Manuscript locations: docs/appendix/sources.md; chapter 9; appendices on Rust
and case studies
Current source title/version:
Result: pending
Change needed:
Reviewer:
```

## OWASP batch

```text
Source group: OWASP agentic and GenAI security sources
Representative sources: AI Agent Security Cheat Sheet, Top 10 for Agentic
Applications for 2026, MCP Security Cheat Sheet, MCP Tool Poisoning, MCP Top
10, Agentic Skills Top 10, Prompt Injection and RAG cheat sheets.
Checked on:
Primary/secondary: primary
Manuscript locations: docs/appendix/sources.md; chapters 4, 7, 9, 20, 23
Current source title/version:
Result: pending
Change needed:
Reviewer:
```

## NIST and CISA batch

```text
Source group: NIST/CISA governance and control sources
Representative sources: AI RMF, Generative AI Profile, SP 800-53, SP 800-218A,
adversarial ML taxonomy, CISA AI guidance.
Checked on:
Primary/secondary: primary
Manuscript locations: docs/appendix/sources.md; chapters 4, 17-20, 23
Current source title/version:
Result: pending
Change needed:
Reviewer:
```

## Protocol status batch

```text
Source group: MCP and A2A protocol status
Representative sources: MCP security best practices, MCP authorization
specification, A2A specification.
Checked on:
Primary/secondary: primary
Manuscript locations: docs/appendix/sources.md; chapter 9; case studies;
glossary
Current source title/version:
Result: pending
Change needed:
Reviewer:
```

## Research and case references batch

```text
Source group: research frontier and incident/legal cases
Representative sources: OpenReview/arXiv papers on memory, tracing, verifiers
and multi-agent failures; Microsoft Research HCI guidance; MLCommons
AILuminate; legal/incident case references.
Checked on:
Primary/secondary: mixed
Manuscript locations: docs/appendix/sources.md; chapters 13-16, 20; appendices
Current source title/version:
Result: pending
Change needed:
Reviewer:
```
