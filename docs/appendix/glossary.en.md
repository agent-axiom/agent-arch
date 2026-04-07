# Glossary

This page is a quick reference for the key terms used across the book. It does not replace the chapters, but it makes it easier to recall a term and jump to the right section.

## Agent runtime

The execution environment of the agent: the place where the run loop, context assembly, tool calls, policy checks, memory, and telemetry live.

Read next:

- [Chapter 2. Reference Architecture for a Safe Agent](../book/part-i/chapter-2.en.md)
- [Chapter 16. Baseline Runtime Blueprint](../book/part-vii/chapter-16.en.md)

## Control plane

The governance layer of the platform. This usually includes policies, the capability catalog, approvals, rollout checks, and audit logic.

Read next:

- [Chapter 2. Reference Architecture for a Safe Agent](../book/part-i/chapter-2.en.md)
- [Chapter 17. Policy Layer and Capability Catalog](../book/part-vii/chapter-17.en.md)

## Trust boundary

A boundary between zones with different levels of trust and control. Examples include the edges between user input, memory, tools, and external systems.

Read next:

- [Chapter 3. Security Perimeter and Trust Boundaries](../book/part-ii/chapter-3.en.md)

## Policy gate

A decision point where the system determines whether it may execute an action, read data, write memory, or call a tool.

Read next:

- [Chapter 4. Tool Gateway, Approval, and Audit Trail](../book/part-ii/chapter-4.en.md)
- [Chapter 17. Policy Layer and Capability Catalog](../book/part-vii/chapter-17.en.md)

## Capability catalog

The registry of what an agent can do: which tools exist, who owns them, what risk they carry, which transport they use, and what restrictions apply.

Read next:

- [Chapter 8. Execution Model and Tool Catalog](../book/part-iv/chapter-8.en.md)
- [Chapter 17. Policy Layer and Capability Catalog](../book/part-vii/chapter-17.en.md)

## Approved inventory

The explicit set of capabilities approved for a specific agent or agent class. This prevents teams from confusing “exists in the catalog” with “allowed for use.”

Read next:

- [Chapter 14. Platform Team vs Product Teams](../book/part-vi/chapter-14.en.md)
- [Chapter 15. Golden Paths, Shared Gateways, and Anti-Zoo Patterns](../book/part-vi/chapter-15.en.md)

## Tool gateway

The control point before a tool call. It checks the actor, policy, risk tier, approval requirements, and egress rules before the call is allowed to continue.

Read next:

- [Chapter 4. Tool Gateway, Approval, and Audit Trail](../book/part-ii/chapter-4.en.md)
- [Chapter 8. Execution Model and Tool Catalog](../book/part-iv/chapter-8.en.md)

## Sandbox execution

Running a tool in an isolated environment to limit side effects and reduce access to the network, filesystem, and other sensitive resources.

Read next:

- [Chapter 9. Sandbox Execution and MCP as an Integration Contract](../book/part-iv/chapter-9.en.md)

## Egress policy

The rules that define where an agent or tool may connect outward: which domains, services, and types of network access are allowed.

Read next:

- [Chapter 9. Sandbox Execution and MCP as an Integration Contract](../book/part-iv/chapter-9.en.md)

## Short-term memory

Short-lived memory for the current session or run. It helps maintain near-term context and usually should not be retained forever.

Read next:

- [Chapter 6. Short-Term, Long-Term, and Profile Memory](../book/part-iii/chapter-6.en.md)

## Long-term memory

Persistent memory that survives beyond a single session. It requires stronger discipline because a bad write can persist and spread.

Read next:

- [Chapter 5. Why Agents Need Memory and Why It Is Dangerous](../book/part-iii/chapter-5.en.md)
- [Chapter 6. Short-Term, Long-Term, and Profile Memory](../book/part-iii/chapter-6.en.md)

## Profile memory

A dedicated memory layer for user preferences, stable traits, or working profile information. It is not the full interaction archive, but a curated set of validated facts.

Read next:

- [Chapter 6. Short-Term, Long-Term, and Profile Memory](../book/part-iii/chapter-6.en.md)

## Retrieval

The selection of relevant records from memory or the knowledge layer for a specific run. Good retrieval brings in a small amount of highly relevant context.

Read next:

- [Chapter 7. Retrieval, Compaction, and Background Updates](../book/part-iii/chapter-7.en.md)

## Compaction

Background memory maintenance: merging, summarizing, deduplicating, and rebuilding records so the memory layer does not turn into a dump.

Read next:

- [Chapter 7. Retrieval, Compaction, and Background Updates](../book/part-iii/chapter-7.en.md)

## Provenance

The origin of a piece of data: where it came from, how it entered memory, which rule allowed it, and how much it should be trusted.

Read next:

- [Chapter 5. Why Agents Need Memory and Why It Is Dangerous](../book/part-iii/chapter-5.en.md)
- [Chapter 6. Short-Term, Long-Term, and Profile Memory](../book/part-iii/chapter-6.en.md)

## Approval gate

A stage where the system does not execute a risky action automatically, but instead routes it to a human or other trusted role for confirmation.

Read next:

- [Chapter 4. Tool Gateway, Approval, and Audit Trail](../book/part-ii/chapter-4.en.md)
- [Chapter 18. Production Rollout Checklist](../book/part-vii/chapter-18.en.md)

## Trace

The connected history of a single agent run: what steps happened, which policy decisions were made, which tools were called, and how the run ended.

Read next:

- [Chapter 11. Traces, Spans, and Structured Events](../book/part-v/chapter-11.en.md)

## Span

A single segment inside a trace. Examples include a retrieval span, a tool execution span, or an approval span.

Read next:

- [Chapter 11. Traces, Spans, and Structured Events](../book/part-v/chapter-11.en.md)

## Rollout gate

A readiness check before launch or traffic expansion. It typically considers safety, evals, observability, ownership, and operational controls.

Read next:

- [Chapter 12. SLO for Agent Systems](../book/part-v/chapter-12.en.md)
- [Chapter 18. Production Rollout Checklist](../book/part-vii/chapter-18.en.md)

## Eval dataset

A set of examples, runs, or sessions used for regression checks and quality evaluation before rollout or after changes.

Read next:

- [Chapter 13. Offline Evals, Online Evals, and Regression Gates](../book/part-v/chapter-13.en.md)
- [Reference Package](reference-package.en.md)
