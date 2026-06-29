# Source verification packet

Date: 2026-06-28.

Status: ready for the final semantic source-check pass. A representative P0
live-pass and a full source catalog URL availability pass were completed on
2026-06-29, but manual follow-up and claim-level semantic verification remain
open.

## Context

`docs/appendix/sources.md` currently records **2026-05-17** as the last source
review date. Several chapter notes planned checks for **2026-06-14** and
**2026-06-17**. As of **2026-06-29**, a P0 live-pass checked representative
OpenAI, Anthropic, Google Cloud, Microsoft, OWASP, MCP, NIST and A2A primary
routes, and a full URL availability pass checked all 106 source URL rows. The
final publication pass must still complete manual/browser follow-up for blocked
or challenge-gated sources and semantic checks for fast-moving platform claims
before the manuscript is submitted as final.

## Verification batches

### Batch 1. OpenAI sources

Check:

- Agents SDK;
- Agent Builder;
- agent safety guidance;
- agent evals and trace grading;
- background mode;
- tools and structured outputs;
- sandbox agents and agent memory.

Record:

- URL;
- current page title;
- checked date;
- manuscript locations affected;
- result: unchanged, wording updated, source removed or claim generalized.

### Batch 2. Anthropic sources

Check:

- Building Effective AI Agents;
- harness design for long-running application development;
- managed agents;
- evals;
- Claude Code security;
- multi-agent research;
- red-team/alignment references.

### Batch 3. Platform architecture sources

Check:

- LangGraph durable execution, persistence, memory and interrupts;
- Google Cloud Vertex AI Agent Builder, Agent Sandbox, AI controls and
  multi-agent architecture;
- Microsoft Azure/Entra/Copilot agent orchestration, observability, agent
  registry and autonomous-agent security;
- Cloudflare Agents SDK and remote MCP references;
- AWS Bedrock AgentCore/stateful MCP references;
- GitHub Copilot cloud agent references.

### Batch 4. Security and governance sources

Check:

- OWASP AI Agent Security Cheat Sheet;
- OWASP Top 10 for Agentic Applications for 2026;
- OWASP MCP Security Cheat Sheet, Tool Poisoning and MCP Top 10;
- OWASP Agentic Skills Top 10;
- OWASP Prompt Injection and RAG cheat sheets;
- NIST AI RMF, Generative AI Profile, SP 800-53, SP 800-218A and adversarial ML
  taxonomy;
- CISA AI guidance.

### Batch 5. Protocol and terminology status

Check:

- MCP host/client/server terminology;
- MCP authorization specification status;
- stateful vs stateless MCP wording;
- A2A specification status;
- agent registry/inventory/identity terminology.

### Batch 6. Research and case references

Check:

- OpenReview/arXiv research references used as frontier signals;
- Microsoft Research HCI/HITL guidance;
- legal/incident case references such as the Air Canada chatbot case;
- MLCommons AILuminate reference;
- Rust/platform SDK references.

## Required manuscript updates after verification

After live verification, update:

- `docs/appendix/sources.md` last-checked date;
- stale chapter review notes;
- footnotes whose product/page names changed;
- claims that are too specific for a changing API;
- companion source routes if a source moved or was deprecated;
- `docs/publisher/ru-final-fact-check-backlog-2026-06-28.md`.

## Evidence format

Use this record for each checked source:

```text
Source:
URL:
Checked on:
Primary/secondary:
Manuscript locations:
Current source title/version:
Result: unchanged / updated / removed / generalized
Change needed:
Reviewer:
```

Prepared batch records:

- `docs/publisher/ru-source-verification-records-2026-06-28.md`
- `docs/publisher/ru-live-source-verification-actions-2026-06-29.md`
- `docs/publisher/ru-live-source-verification-pass-2026-06-29.md`

## Done definition

The source verification pass is complete only when:

- every P0 source in the fact-check backlog has a record;
- `docs/appendix/sources.md` has a current last-checked date;
- stale internal review notes are removed from final print flow or updated;
- no final manuscript claim depends on an unchecked fast-changing platform page;
- editor/publisher packet clearly distinguishes verified current facts from
  evergreen architectural guidance.
