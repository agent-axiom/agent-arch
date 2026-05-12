# Reference Layer

If the book explains **why** a safe agent system should be built this way, the reference layer helps answer **what exactly should be captured in artifacts, schemas, and contract pages**.

This layer is intentionally supportive, not primary. It exists to anchor the book's argument in reusable engineering materials, not to replace the reader journey of the book itself.

Use this section when you need to:

- find the right contract page quickly;
- prepare a design review or rollout review;
- extract reusable artifacts for your team;
- move from conceptual chapters to applied engineering materials.

If you are new to the project, start with the book first. Come here when you want the supporting schemas, checklists, and contract surfaces behind the main argument.

What this layer does **not** promise:

- it does not replace the book's reader journey;
- it does not explain the main causal argument chapter by chapter;
- it does not try to be the primary place where trade-offs and layer boundaries are learned.

## Start here

For a short path in, start with:

1. [Glossary](appendix/glossary.en.md)
2. [Cheat Sheets](appendix/cheat-sheets.en.md)
3. [Reference Package](appendix/reference-package.en.md)

!!! example "Support-triage artifact route"
    If you read the book through the support-triage case, keep the trace, eval dataset, policy bundle, approval record, incident record, change rollout, lifecycle artifact, and registry operations pages next to it. Those contracts turn the duplicate-ticket incident from a story into a reviewable artifact set.

## Schemas and contract pages

- [Trace Schema and Event Catalog](appendix/trace-schema.en.md)
- [Eval Dataset Schema and Grading Contract](appendix/eval-schema.en.md)
- [Policy Bundle Schema and Approval Contract](appendix/policy-bundle-schema.en.md)
- [Approval Request and Decision Record Schema](appendix/approval-schema.en.md)
- [Incident Record and Postmortem Linkage Schema](appendix/incident-record-schema.en.md)
- [Change Review and Rollout Gate Schema](appendix/change-rollout-schema.en.md)
- [Lifecycle Artifact Schema](appendix/lifecycle-artifact-schema.en.md)
- [Memory Record and Retrieval Contract Schema](appendix/memory-retrieval-schema.en.md)
- [Causal Debugging and Root-Cause Analysis for Agent Systems](appendix/causal-debugging.en.md)
- [Memory Eval Patterns for Agent Systems](appendix/memory-eval-patterns.en.md)
- [Tool Failure Recovery Patterns for Agent Systems](appendix/tool-failure-recovery.en.md)

## Practical pages

- [Reference Package](appendix/reference-package.en.md)
- [Case Studies](appendix/case-studies.en.md)
- [Policy Templates and Checklists by Use Case](appendix/policy-templates.en.md)
- [Incident Response Playbook for Agent Systems](appendix/incident-response-playbook.en.md)
- [Handbook for Agent Registry and Inventory Operations](appendix/registry-operations-handbook.en.md)
- [Postmortem Template for Agent Systems](appendix/postmortem-template.en.md)

## Fast Topic Routes

If you do not need the whole reference layer, but only a short path into one concrete topic, start here:

- Tool catalog design, semantic tool filtering, and read/write taxonomy: [Chapter 8. Execution Model and Tool Catalog](book/part-iv/chapter-8.en.md)
- MCP host/client/server roles, capability transport, and sandbox boundaries: [Chapter 9. Sandbox Execution and MCP as an Integration Contract](book/part-iv/chapter-9.en.md)
- Semantic gap, HyDE, and RAG vs training: [Chapter 7. Retrieval, Compaction, and Background Updates](book/part-iii/chapter-7.en.md)
- Latency budget, fast path / slow path, and routed pipelines: [Chapter 12. SLO for Agent Systems](book/part-v/chapter-12.en.md)
- LLM-as-a-judge, calibration, and judge-human agreement: [Chapter 13. Offline Evals, Online Evals, and Regression Gates](book/part-v/chapter-13.en.md)

## Continue

- [Start Here](start-here.en.md)
- [Book Plan](book/plan.en.md)
- [Research Frontier: Memory, Observability, and Multi-Agent Reliability](appendix/research-frontier.en.md)
- [Sources](appendix/sources.en.md)

The simplest rule is:

- use the book for argument and sequencing;
- use the reference layer for support artifacts and implementation-facing detail.
