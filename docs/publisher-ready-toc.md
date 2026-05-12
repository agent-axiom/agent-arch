# Publisher-Ready TOC Draft

Purpose: keep a publisher-facing table of contents separate from the MkDocs site tree. The web site can stay broad; this draft is the tighter book-shaped manuscript.

Status: working editorial artifact, not a public navigation page.

## Positioning

Working title: **Secure AI Agent Architecture**.

Reader: senior product engineers, platform engineers, security engineers, staff engineers, and technical leads who need to ship AI agents with tool access, memory, approvals, observability, evals, rollout discipline, and lifecycle ownership.

Promise: explain how to move from prompt demos to governed agent systems where identity, policy, tools, memory, traces, evals, rollout, and retirement are explicit engineering contracts.

Non-goal: this is not a framework manual, not a prompt-trick book, and not a survey of vendor products.

## One-Page Positioning Memo Draft

**Title:** Secure AI Agent Architecture

**Subtitle:** From prompt demos to governed production systems.

**Primary reader:** platform and product architects responsible for agent systems that can read private context, call tools, request approvals, write to external systems, and survive incidents.

**Problem:** most teams can build an impressive demo before they can explain identity, policy, side effects, memory provenance, eval gates, trace evidence, rollout ownership, or retirement.

**Why now:** agent systems are moving from isolated assistants into production workflows with real permissions, long-running state, delegated work, and regulated evidence needs.

**Unique promise:** the book treats agents as production systems: architecture first, workflow-first by default, explicit control boundaries, evals tied to release judgment, and lifecycle governance through registry, provenance, observability, and retirement.

**Competing shelf:** cloud architecture, secure software design, MLOps/LLMOps, and practical AI engineering books. The distinction is the focus on governed agent behavior rather than only model quality, prompts, or generic platform operations.

**Manuscript status:** public open manuscript with runnable reference package; core argument is strong, while sample chapter polish, print compression, and localization cleanup continue.

**Companion assets:** reference runtime, schemas, checklists, case studies, source catalog, and public documentation site.

## Print Manuscript Shape

Target: 6 parts, about 20 chapters. Keep schemas, runtime command details, long checklists, and source catalogs in the online companion.

### Part I — Why Agents Need Platforms

1. Why an Agent Needs a Platform, Not Magic
2. Anatomy of a Production Agent System
3. Trust Boundaries, Identity, and the Right to Act

### Part II — Context, Memory, and Retrieval

4. Context as a Runtime Contract
5. Memory, Provenance, and Persistence
6. Retrieval, Compaction, and Background Updates

### Part III — Tools, Side Effects, and Execution

7. Execution Model and Tool Catalog
8. Sandboxes, MCP, and Integration Boundaries
9. Retries, Idempotency, Rollback, and Failure Recovery

### Part IV — Reliability, Observability, and Evals

10. Trace Schema and Observability for Agent Runs
11. SLOs and Degraded-Path Evidence
12. Offline Evals, Online Evals, and Regression Gates
13. Behavioral and Control Evals for Agent Systems

### Part V — Shipping and Operating Agents

14. Production Rollout Checklist
15. Change Review, Approval Gates, and Release Identity
16. Incident Response and Assurance
17. Supply Chain, Provenance, and Artifact Lineage

### Part VI — Lifecycle, Governance, and Retirement

18. Capability Sessions, Pause/Resume, and Expiry
19. Registry, Ownership, and Inventory Control
20. Retirement, Replacement, and Long-Term Accountability

## Online Companion Boundary

Move or keep these primarily online:

- runnable `agent_runtime_ref` package and CLI walkthrough;
- schema appendices for traces, eval datasets, approvals, memory, lifecycle artifacts, incident records, rollout gates, and policy bundles;
- command-output field lists and validation-error catalogs;
- case-study worksheets and templates;
- policy templates and checklists;
- community roadmap;
- source catalog and research frontier pages.

## Sample Chapter Candidates

### Chapter 1 — strongest publisher sample

Why: it carries the thesis, starts from a failure story, and shows how the book differs from prompt-hype or framework documentation.

Current strengths:

- opens from a concrete support-triage failure story;
- states the workflow-first / constrained-agency thesis;
- includes a text-safe workflow vs single-agent vs multi-agent rule;
- includes a short "what this chapter proves" section;
- includes an evidence model.

Needs before submission:

- one clean platform diagram or visual summary;
- explicit competing views;
- tighter design-review checklist;
- final copy-edit pass for print rhythm.

### Chapter 12 or 13 — strongest technical credibility sample

Why: evals, traces, failure attribution, regression gates, and release judgment show production maturity.

Needs before submission:

- one complete support-triage example from trace to eval decision;
- clear distinction between behavioral evals, control evals, and release gates;
- calibrated judge/human-review discussion;
- compact evidence model;
- practical checklist.

## Editorial Compression Rules

- Every print chapter needs one main question.
- Every print chapter needs one unique artifact or decision framework.
- Avoid repeating governance language unless the chapter owns a distinct role.
- Keep long field lists online.
- Use Support Triage as the primary running case; use Internal Knowledge and Incident Coordination as secondary contrast cases.
- End chapters with: what to remember, common failure modes, design-review use, companion assets, and next chapter.

## Pitch Packet Checklist

Before sending to a publisher:

- one-page positioning memo;
- this publisher-ready TOC;
- one polished sample chapter;
- short author/platform credibility note;
- explanation of print manuscript vs online companion;
- 3-5 comparable books and why this one is different;
- links to the public site and runnable reference package.
