# Full source URL availability pass

Date: 2026-06-29.

Status: full source catalog URL availability pass completed. This is not yet a
full semantic source audit.

Evidence file:

- `docs/publisher/ru-source-url-live-check-2026-06-29.tsv`

## Scope

All URLs listed in `docs/appendix/sources.md` were checked with live HTTP
requests on 2026-06-29.

Summary:

- source URL rows checked: 106;
- HTTP 200: 102;
- HTTP 403: 3;
- HTTP 000 timeout: 1.

## Sources requiring manual follow-up

These URLs did not provide clean automated HTTP 200 content in the final TSV
run:

- `https://www.microsoft.com/en-us/research/publication/guidelines-for-human-ai-interaction/`
  returned HTTP 403.
- `https://docs.anthropic.com/en/docs/claude-code/security` timed out in the
  final run. An earlier live check observed a canonical redirect to
  `https://code.claude.com/docs/en/security`, so this needs a browser or retry
  check rather than immediate removal.
- `https://mlcommons.org/2024/12/mlcommons-ailuminate-v1-0-release/` returned
  HTTP 403.
- `https://www.americanbar.org/groups/business_law/resources/business-law-today/2024-february/bc-tribunal-confirms-companies-remain-liable-information-provided-ai-chatbot/`
  returned HTTP 403.

OpenReview links returned HTTP 200, but the effective URL was a challenge
redirect. Treat these as browser/API-gated until manually opened and matched to
the manuscript claim.

## Redirects to record

The pass found route changes that should be reflected in final source wording
or source notes:

- OpenAI Agents SDK:
  `https://developers.openai.com/api/docs/guides/agents-sdk` ->
  `https://developers.openai.com/api/docs/guides/agents`
- OpenAI Agent Builder:
  `https://platform.openai.com/docs/guides/agent-builder` ->
  `https://developers.openai.com/api/docs/guides/agent-builder`
- OpenAI Agent Builder safety:
  `https://platform.openai.com/docs/guides/agent-builder-safety` ->
  `https://developers.openai.com/api/docs/guides/agent-builder-safety`
- OpenAI agent evals:
  `https://platform.openai.com/docs/guides/agent-evals` ->
  `https://developers.openai.com/api/docs/guides/agent-evals`
- OpenAI trace grading:
  `https://platform.openai.com/docs/guides/trace-grading` ->
  `https://developers.openai.com/api/docs/guides/trace-grading`
- LangGraph JavaScript overview:
  `https://docs.langchain.com/oss/javascript/langgraph` ->
  `https://docs.langchain.com/oss/javascript/langgraph/overview`
- LangGraph durable execution:
  `https://docs.langchain.com/oss/javascript/langgraph/durable-execution` ->
  `https://docs.langchain.com/oss/javascript/langgraph/persistence`
- LangGraph memory:
  `https://docs.langchain.com/oss/python/langgraph/memory` ->
  `https://docs.langchain.com/oss/python/concepts/memory`
- Google Agent Builder:
  `https://docs.cloud.google.com/agent-builder/overview` ->
  `https://docs.cloud.google.com/gemini-enterprise-agent-platform/overview`
- Cloudflare Agents state:
  `https://developers.cloudflare.com/agents/api-reference/store-and-sync-state/`
  -> `https://developers.cloudflare.com/agents/runtime/lifecycle/state/`
- Cloudflare Agents schedule:
  `https://developers.cloudflare.com/agents/api-reference/schedule-tasks/` ->
  `https://developers.cloudflare.com/agents/runtime/execution/schedule-tasks/`
- Cloudflare Agents human-in-the-loop:
  `https://developers.cloudflare.com/agents/concepts/human-in-the-loop/` ->
  `https://developers.cloudflare.com/agents/concepts/agentic-patterns/human-in-the-loop/`
- Cloudflare Agents WebSockets:
  `https://developers.cloudflare.com/agents/api-reference/websockets/` ->
  `https://developers.cloudflare.com/agents/runtime/communication/websockets/`
- Cloudflare Agents durable execution:
  `https://developers.cloudflare.com/agents/api-reference/durable-execution/`
  -> `https://developers.cloudflare.com/agents/runtime/execution/durable-execution/`
- Microsoft Copilot maturity model:
  `https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/maturity-model-overview`
  -> `https://learn.microsoft.com/en-us/agents/adoption-maturity-model/`
- Microsoft Agent Registry:
  `https://learn.microsoft.com/en-us/entra/identity-platform/agent-registry-convergence`
  -> `https://learn.microsoft.com/en-us/identity-platform/agent-registry-convergence`
- Rust `rig-core` API:
  `https://docs.rs/rig-core/` -> `https://docs.rs/rig-core/latest/rig_core/`

## Editorial decision

Update the source appendix to say that a full live URL availability pass was
completed on 2026-06-29, with four automated follow-ups still open. Do not mark
every source claim as semantically verified until the gated, redirected and
fast-moving platform claims are manually checked against the manuscript text.

Use conservative wording for volatile product surfaces, especially OpenAI,
Google, Microsoft, Anthropic/LangGraph and Cloudflare routes that changed.

