# Online Companion

The online companion holds material that should remain versioned, testable, and independently updateable outside the print manuscript.

The book keeps the argument, decision criteria, and minimal contract forms. This section keeps complete CLI walkthroughs, runtime configurations, trace and event catalogs, evaluation datasets, sources, and reference walkthroughs.

## Main routes

- [Runtime configs and MCP boundary](runtime-reference/configs.md)
- [Runtime CLI](runtime-reference/cli.md)
- [Eval datasets](runtime-reference/eval-datasets.md)
- [Traces and events](runtime-reference/traces-and-events.md)
- [Templates](templates/index.md)
- [Checklists](checklists/index.md)
- [Changelog](changelog.md)
- [Errata](errata.md)
- Example artifacts:
  `artifacts/trace-demo.jsonl`,
  `artifacts/trace-failed-tool-timeout.jsonl`,
  `artifacts/trace-post-dispatch-timeout.jsonl`,
  `artifacts/session-failed-tool-timeout.json`,
  `artifacts/eval-failed-run-timeout.json`,
  `artifacts/eval-unknown-effect-reconciliation.json`
- Filled examples:
  `examples/capability-contract-support-ticket.md`,
  `examples/release-decision-record-support-ticket.md`,
  `examples/incident-record-support-ticket-timeout.md`,
  `examples/production-readiness-support-ticket.md`,
  `examples/context-manifest-support-ticket.yaml`,
  `examples/threat-map-negative-tests.yaml`,
  `examples/slo-card-support-ticket.yaml`,
  `examples/adlc-transition-support-ticket.yaml`,
  `examples/readiness-rubric-support-ticket.yaml`
- [Complete reference package walkthrough](../appendix/reference-package.en.md)
- [Complete source list](../appendix/sources.en.md)

## Practice path for a safe agent

Readers who want to reproduce the material should start with the [complete reference package walkthrough](../appendix/reference-package.en.md). It connects chapters to `agent_runtime_ref` files, CLI commands, companion artifacts, and tests. The shortest practical path is `inspect-agent` for inventory, `simulate-run` for a controlled run, `dump-events` and `inspect-trace` for evidence, `inspect-approvals` for the human gate, `export-eval-dataset` for evaluations, and `check-rollout` and `check-controls` for the release decision.

## What belongs here

- Complete YAML configurations and review forms.
- CLI commands and expected JSON surfaces.
- Trace and event catalogs plus validation-message catalogs.
- Evaluation datasets, verifier contracts, and rollout judgment examples.
- Long source catalogs, changelog, errata, and update rules.

## What stays in the book

- Why an architectural decision is needed.
- Which risk it controls.
- Who owns the action and its evidence.
- How a team knows that runtime, policy, trace, evaluation gate, and rollout are ready.

## Chapter map {#chapter-map}

This map connects every print chapter to the corresponding topic in the online book and the closest executable or reference artifact. Link names matter more than internal site numbering: if the online structure changes, readers can still find the topic and its verifiable artifact instead of guessing which web chapter has the same number.

| Print chapter | Online topic | Practice and reference |
| ---: | --- | --- |
| 1 | [Why an agent needs a platform](../book/part-i/chapter-1.en.md) | [Reference package](../appendix/reference-package.en.md) |
| 2 | [Execution forms](../book/part-i/chapter-2.en.md), [manager and handoffs](../book/part-i/practical-manager-handoffs.en.md) | [Practical request patterns](../book/part-i/practical-routines.en.md) |
| 3 | [Safe agent architecture](../book/part-i/chapter-2.en.md) | [Technology stack map](../appendix/stack.en.md) |
| 4 | [Trust boundaries](../book/part-ii/chapter-3.en.md) | [Policy templates](../appendix/policy-templates.en.md) |
| 5 | [Policy layer and capability catalog](../book/part-vii/chapter-17.en.md) | [Policy bundle schema](../appendix/policy-bundle-schema.en.md) |
| 6 | [Tool gateway and approvals](../book/part-ii/chapter-4.en.md) | [Approval schema](../appendix/approval-schema.en.md) |
| 7 | [Memory risks](../book/part-iii/chapter-5.en.md) | [Memory evaluation patterns](../appendix/memory-eval-patterns.en.md) |
| 8 | [Memory types and lifecycle](../book/part-iii/chapter-6.en.md) | [Memory retrieval schema](../appendix/memory-retrieval-schema.en.md) |
| 9 | [Context retrieval and compaction](../book/part-iii/chapter-7.en.md) | [Continuity envelope](../appendix/continuity-envelope-schema.en.md) |
| 10 | [Execution model and tools](../book/part-iv/chapter-8.en.md) | [Configuration reference](runtime-reference/configs.md) |
| 11 | [Sandbox and MCP](../book/part-iv/chapter-9.en.md), [MCP and A2A boundary](../book/part-iv/practical-mcp-a2a.en.md) | [Tool failure recovery](../appendix/tool-failure-recovery.en.md) |
| 12 | [Retries, limits, and rollback](../book/part-iv/chapter-10.en.md) | [Tool failure recovery](../appendix/tool-failure-recovery.en.md) |
| 13 | [Traces and events](../book/part-v/chapter-11.en.md) | [Trace and event catalog](runtime-reference/traces-and-events.md) |
| 14 | [Agent-system SLOs](../book/part-v/chapter-12.en.md) | [Filled SLO card](examples/slo-card-support-ticket.yaml) |
| 15 | [Evaluations and regression gates](../book/part-v/chapter-13.en.md) | [Evaluation datasets](runtime-reference/eval-datasets.md) |
| 16 | [End-to-end evidence spine](../book/part-v/evidence-spine.en.md) | [Change review and rollout schema](../appendix/change-rollout-schema.en.md) |
| 17 | [Platform and product teams](../book/part-vi/chapter-14.en.md) | [Capability contract template](templates/capability-contract.md) |
| 18 | [Supported golden paths](../book/part-vi/chapter-15.en.md) | [Filled golden-path contract](examples/capability-contract-support-ticket.md) |
| 19 | [Agent inventory and registry](../book/part-viii/chapter-27.en.md) | [Registry operations handbook](../appendix/registry-operations-handbook.en.md) |
| 20 | [From SDLC to ADLC](../book/part-viii/chapter-19.en.md), [change management](../book/part-viii/chapter-20.en.md) | [ADLC transition example](examples/adlc-transition-support-ticket.yaml) |
| 21 | [Provenance and trusted artifacts](../book/part-viii/chapter-22.en.md) | [Lifecycle artifact schema](../appendix/lifecycle-artifact-schema.en.md) |
| 22 | [Observability and detection telemetry](../book/part-viii/chapter-26.en.md) | [Trace schema](../appendix/trace-schema.en.md) |
| 23 | [Goal misalignment and insider risk](../book/part-viii/chapter-24.en.md), [behavioral evaluations](../book/part-viii/chapter-25.en.md) | [Negative threat-model scenarios](examples/threat-map-negative-tests.yaml) |
| 24 | [Assurance and response](../book/part-viii/chapter-21.en.md) | [Incident response playbook](../appendix/incident-response-playbook.en.md) |
| 25 | [Decommissioning and replacement](../book/part-viii/chapter-23.en.md) | [Lifecycle artifact schema](../appendix/lifecycle-artifact-schema.en.md) |
| 26 | [Baseline runtime](../book/part-vii/chapter-16.en.md) | [CLI reference](runtime-reference/cli.md) |
| 27 | [Policies and capability catalog](../book/part-vii/chapter-17.en.md) | [Executable trajectory-policy scenarios](examples/trajectory-policy-scenarios.en.md) |
| 28 | [Production launch checklist](../book/part-vii/chapter-18.en.md) | [Production readiness checklist](checklists/production-readiness.md) |
