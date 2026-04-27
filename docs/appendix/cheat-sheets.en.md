# Cheat Sheets

This page is for quick working checks. If you do not want to reread an entire part before a design review, an agent launch, or a team discussion, start here.

## Safety checklist

- Are trust boundaries explicit between user input, memory, tools, and external systems?
- Do you distinguish prompt injection, jailbreaking, and action hallucination instead of collapsing them into one vague “LLM risk” bucket?
- Is there a policy gate before every sensitive action, not only before the model call?
- Are low-risk and high-risk tools clearly separated?
- Is there an approval gate for actions with irreversible side effects?
- Are allowed egress destinations and the network access profile defined?
- Does the system write an audit trail for policy decisions, approvals, and tool execution?
- Is there a clear stop condition for the run loop?

Read next:

- [Chapter 3. Security Perimeter and Trust Boundaries](../book/part-ii/chapter-3.en.md)
- [Chapter 4. Tool Gateway, Approval, and Audit Trail](../book/part-ii/chapter-4.en.md)

## Memory checklist

- Are short-term, long-term, and profile memory separated?
- Does retrieval account for the semantic gap between user language and document language?
- If you use query rewriting or HyDE, is it clear that this is retrieval aid rather than a new source of “facts”?
- Are memory read and memory write governed by different rules?
- Is provenance stored for persistent records?
- Is there a policy for what may be written into memory?
- Is there a compaction or background maintenance path?
- Is retrieval bounded by volume and relevance?
- Do you first try to improve RAG and corpus freshness before jumping to training?
- Is there a clear deletion or revision strategy?

Read next:

- [Chapter 5. Why an Agent Needs Memory, and Why Memory Is Risky](../book/part-iii/chapter-5.en.md)
- [Chapter 7. Retrieval, Compaction, and Background Updates](../book/part-iii/chapter-7.en.md)

## Rollout checklist

- Does the agent have a clear owner, not just a vague team?
- Is there a minimum eval baseline before launch?
- Is there a rollout gate with safety, observability, and approval requirements?
- Is it clear which scenarios count as blocking failures?
- Is the latency budget defined from the user's patience window, not only from model p95?
- Is there a runbook for failures, denials, and approval backlog?
- Is there a channel for incident review and postmortems?
- Can you quickly disable a high-risk capability without shutting down the whole system?

Read next:

- [Chapter 12. SLO for Agent Systems](../book/part-v/chapter-12.en.md)
- [Chapter 18. Production Rollout Checklist](../book/part-vii/chapter-18.en.md)

## Observability checklist

- Does every run have a trace_id?
- Are there baseline spans for retrieval, model step, tool execution, approval, and memory write?
- Are there structured events instead of raw logs only?
- Can you see which policy decision the gateway made?
- Can you see which tool principal executed the side effect?
- Can you distinguish success, denied, approval_wait, and failure?
- Is there a way to aggregate runs into session-level or eval-level summaries?
- If you use LLM-as-a-judge, is the judge calibrated against human review and outcome checks?
- Are you avoiding model-and-prompt changes in the same experiment when you need a causal eval conclusion?

Read next:

- [Chapter 11. Traces, Spans, and Structured Events](../book/part-v/chapter-11.en.md)
- [Chapter 13. Offline Evals, Online Evals, and Regression Gates](../book/part-v/chapter-13.en.md)

## Tool gateway checklist

- Does every capability have an owner, risk tier, and approved inventory status?
- Is it clear whether a tool is read-only or write-capable?
- Are you hiding an overly large tool catalog from the model behind a relevant subset instead of showing everything at once?
- Is there an execution profile: sandbox, network access, allowed egress?
- Does the gateway check actor identity and policy before execution?
- Are idempotency semantics and retry policy defined?
- Is it clear when approval is required and when a tool may execute automatically?
- Is there an audit trail for every external action?
- Does the team understand the MCP host, client, and server roles instead of treating them as one generic “integration”?

Read next:

- [Chapter 8. Execution Model and Tool Catalog](../book/part-iv/chapter-8.en.md)
- [Chapter 9. Sandbox Execution and MCP as an Integration Contract](../book/part-iv/chapter-9.en.md)
- [Chapter 10. Idempotency, Retries, Rate Limits, and Rollback Boundaries](../book/part-iv/chapter-10.en.md)

## What to Do Next

- Before a design review: run through the safety, memory, and tool gateway blocks.
- Before launch: run through the rollout and observability blocks.
- During incident review: use the observability and safety blocks as the review frame.

- [Start Here](../start-here.en.md)
- [Glossary](glossary.en.md)
- [Policy Templates and Checklists by Use Case](policy-templates.en.md)
