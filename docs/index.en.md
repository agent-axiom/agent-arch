# Secure AI Agent Architecture

This book is for people who want to build not demo magic, but calm, controllable, and safe production agent systems.

> It starts from Dmitry Vikulin's article on reliable AI agents and expands it into a platform-level view: policy enforcement, human approval, observability, evals, operational discipline, and lifecycle management.

[Start here](start-here.en.md){ .md-button .md-button--primary }
[Open the book plan](book/plan.en.md){ .md-button }
[Explore the reference runtime](appendix/reference-package.en.md){ .md-button }

<div class="book-cover" markdown="1">

![Book cover](assets/images/hero-home.png)

</div>

## Who this is for

- Engineers shipping agent features into real products.
- Platform teams building shared runtime, policy, registry, approvals, and observability layers.
- Security engineers who need explicit trust boundaries and risky execution paths.
- Tech leads and architects who care more about operational discipline than agent theater.

## What you can take into work today

- A practical path from workflow-first systems to bounded autonomy.
- Chapters on policy layers, approvals, memory, evals, observability, and lifecycle.
- A runnable reference runtime with session export, eval dataset export, approvals, controls, and lifecycle artifacts.
- Reference pages for trace schema, eval schema, policy bundles, approvals, rollout gates, memory retrieval, and lifecycle artifacts.
- Case studies, checklists, and policy templates you can reuse as starting artifacts.

## Project Status

- `Published core`: all eight parts of the book are already published.
- `Expanding now`: entry pages, the reference layer, and site navigation are actively being improved.
- `Reference assets available`: schemas, checklists, case studies, and a runnable runtime are already available.

## Three useful reading paths

### If you are building a product agent

1. [Chapter 1. Why Agents Need a Platform, Not Magic](book/part-i/chapter-1.en.md)
2. [Chapter 3. Security Perimeter and Trust Boundaries](book/part-ii/chapter-3.en.md)
3. [Chapter 8. Execution Model and Tool Catalog](book/part-iv/chapter-8.en.md)
4. [Chapter 13. Offline Evals, Online Evals, and Regression Gates](book/part-v/chapter-13.en.md)

### If you are building platform infrastructure

1. [Chapter 2. Reference Architecture for a Safe Agent](book/part-i/chapter-2.en.md)
2. [Chapter 4. Tool Gateway, Approval, and Audit Trail](book/part-ii/chapter-4.en.md)
3. [Chapter 17. Policy Layer and Capability Catalog](book/part-vii/chapter-17.en.md)
4. [Chapter 20. Change Management for Agent Systems](book/part-viii/chapter-20.en.md)

### If you care about safety, control, and operations

1. [Chapter 21. Assurance Loop: Red Teaming, Detection, and Response](book/part-viii/chapter-21.en.md)
2. [Chapter 22. Supply Chain, Provenance, and Approved Artifacts](book/part-viii/chapter-22.en.md)
3. [Chapter 26. AI-Native Observability, Inventory Coverage, and Detection-Ready Telemetry](book/part-viii/chapter-26.en.md)
4. [Chapter 27. Agent Inventory, Registry, and Sprawl Control](book/part-viii/chapter-27.en.md)

## What already exists here

- A full book in `ru / en / zh`.
- A runnable [agent_runtime_ref](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref) package with `pytest` coverage.
- A strong reference layer with schema and contract pages.
- A practical appendix with case studies, checklists, a glossary, and roadmap pages.

## The core engineering idea

The most common mistake in agent systems is simple: teams chase autonomy first and controllability second. In practice, the more stable path is:

1. Build a **predictable workflow** first.
2. Add autonomy **locally and measurably**.
3. Route risky actions through **policy, approval, and tracing**.
4. Keep quality through **evals, telemetry, and lifecycle discipline**.

## Where the reference layer lives

If you need reusable artifacts, start with:

- [Trace Schema and Event Catalog](appendix/trace-schema.en.md)
- [Eval Dataset Schema and Grading Contract](appendix/eval-schema.en.md)
- [Policy Bundle Schema and Approval Contract](appendix/policy-bundle-schema.en.md)
- [Lifecycle Artifact Schema](appendix/lifecycle-artifact-schema.en.md)
- [Memory Record and Retrieval Contract Schema](appendix/memory-retrieval-schema.en.md)

## Continue

[Start here](start-here.en.md){ .md-button .md-button--primary }
[Open reference pages](appendix/trace-schema.en.md){ .md-button }
[View sources](appendix/sources.en.md){ .md-button }
