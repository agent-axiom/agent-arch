# Live source verification actions

Date: 2026-06-29.

Status: ready-to-run action packet. No live source verification is claimed in
this file.

Purpose: turn the prepared source verification packet into an execution order
that can be run before final publisher submission.

## Preconditions

- Use primary sources first: official product documentation, official research
  pages, standard bodies and project repositories.
- Do not update `docs/appendix/sources.md` last-checked date until the current
  source has actually been opened and reviewed.
- Record every checked batch in
  `docs/publisher/ru-source-verification-records-2026-06-28.md`.
- Treat moving platform pages as unstable: when a claim depends on a current
  product feature, either verify it live or generalize the wording.
- Do not replace author-owned fields during source verification.

## Execution order

| Step | Batch | Why first | Output |
| --- | --- | --- | --- |
| 1 | OpenAI, Anthropic, LangGraph | Fast-changing agent/runtime/eval APIs. | Verified titles, current URLs, affected chapters. |
| 2 | Google, Microsoft, Cloudflare, AWS, GitHub | Platform architecture and production examples. | Product names, feature status, renamed pages. |
| 3 | OWASP, NIST, CISA | Security/governance wording and standard status. | Version/status notes, no compliance overclaims. |
| 4 | MCP and A2A | Draft/final protocol wording changes quickly. | Terminology and status decisions. |
| 5 | Research and case references | Need freshness and claim-strength calibration. | Keep, generalize, move to frontier, or remove. |
| 6 | Print metadata sweep | Chapter freshness notes must not be stale. | Updated or removed review-date banners. |

## Local locating commands

Use these commands before opening browser tabs so each source check has a
manuscript location list.

```bash
rg -n "OpenAI|Agents SDK|Agent Builder|Trace grading|Background mode|Structured model outputs|Sandbox Agents" docs/book docs/appendix
rg -n "Anthropic|Building Effective AI Agents|Harness design|Claude Code|managed agents|multi-agent research" docs/book docs/appendix
rg -n "LangGraph|LangChain|durable execution|persistence|interrupts|memory overview" docs/book docs/appendix
rg -n "Google Cloud|Vertex AI|Agent Sandbox|Recommended AI Controls|multi-agent AI system" docs/book docs/appendix
rg -n "Microsoft|Azure|Copilot|Agent Registry|observability for.*agentic|maturity model" docs/book docs/appendix
rg -n "Cloudflare|AWS|Bedrock AgentCore|GitHub Copilot cloud agent" docs/book docs/appendix
rg -n "OWASP|NIST|CISA|AI RMF|SP 800-53|SP 800-218A|MCP Top 10" docs/book docs/appendix
rg -n "Model Context Protocol|MCP|Agent2Agent|A2A" docs/book docs/appendix
rg -n "OpenReview|arXiv|MLCommons|American Bar Association|Air Canada" docs/book docs/appendix
```

## Live check method

For every source:

1. Open the primary URL from `docs/appendix/sources.md`.
2. Record current page title and, when visible, publication/update date.
3. Compare the manuscript claim with the current source.
4. Classify the result:
   `unchanged`, `url-updated`, `title-updated`, `claim-generalized`,
   `source-replaced`, `source-removed`, `needs-author/editor-decision`.
5. Update affected manuscript text only after the classification is clear.
6. Add the exact record to
   `docs/publisher/ru-source-verification-records-2026-06-28.md`.

## Update rules

| Situation | Manuscript action |
| --- | --- |
| URL redirects but content is still the same source | Update URL and note redirect. |
| Product/page renamed but claim still true | Update title/name and keep the claim. |
| Feature status changed or page disappeared | Generalize the claim or replace the source. |
| Draft spec became final or vice versa | Update protocol-status wording in chapter 9, glossary and sources. |
| Research source remains speculative | Keep as research frontier, not production consensus. |
| Legal/case source remains valid | Keep jurisdiction and date visible. |

## Files to update after live verification

1. `docs/appendix/sources.md`
2. `docs/book/part-iv/chapter-9.md`
3. `docs/book/part-v/chapter-13.md`
4. `docs/book/part-viii/chapter-20.md`
5. `docs/book/part-viii/chapter-21.md`
6. `docs/book/part-viii/chapter-22.md`
7. `docs/book/part-viii/chapter-24.md`
8. `docs/book/part-viii/chapter-25.md`
9. `docs/book/part-viii/chapter-26.md`
10. `docs/book/part-viii/chapter-27.md`
11. `docs/publisher/ru-final-fact-check-backlog-2026-06-28.md`
12. `docs/publisher/ru-source-verification-records-2026-06-28.md`

## Done definition

The live source pass is complete only when:

- every P0 source group has a filled verification record;
- stale chapter review-date banners are updated or removed from print flow;
- the source catalog has a current last-checked date;
- protocol draft/final language has been rechecked;
- fast-changing product claims are current or generalized;
- the final external packet includes the verification record and does not claim
  unchecked links are current.
