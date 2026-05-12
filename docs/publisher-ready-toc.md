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
- includes an explicit competing-view note for the agent-first argument;
- includes a short "what this chapter proves" section;
- includes a mini design-review checklist;
- includes a compact platform visual summary;
- includes an evidence model.

Structural readiness:

- ready as the first sample-chapter candidate for editorial review.

Remaining before external submission:

- independent copy-edit pass for print rhythm.

### Chapter 13 — strongest technical credibility sample

Why: evals, traces, failure attribution, regression gates, and release judgment show production maturity.

Current strengths:

- includes a support-triage duplicate-ticket example from trace to verifier attribution, regression gate, rollout owner action, and release judgment;
- distinguishes behavioral evals, control evals, rollout gates, and verifier outputs;
- includes calibrated judge/human-review guidance;
- includes an evidence model;
- includes practical maturity and post-chapter checklists.

Remaining before external submission:

- independent copy-edit pass for print rhythm.

## Editorial Compression Rules

- Every print chapter needs one main question.
- Every print chapter needs one unique artifact or decision framework.
- Avoid repeating governance language unless the chapter owns a distinct role.
- Keep long field lists online.
- Use Support Triage as the primary running case; use Internal Knowledge and Incident Coordination as secondary contrast cases.
- End chapters with: what to remember, common failure modes, design-review use, companion assets, and next chapter.

## Author / Platform Credibility Note Draft

Use this as a conservative draft until the final bio is written:

The project already has more than a manuscript outline: it has a public multilingual book site, a runnable reference runtime, configuration examples, tests, and appendix material that demonstrate the operating model in concrete artifacts. That platform supports the book's central claim: production AI agents should be designed as governed systems, not as prompt demos.

Credibility points to emphasize:

- the manuscript connects architecture, safety, observability, evals, rollout, and lifecycle ownership rather than treating them as separate topics;
- the companion material includes runnable/reference artifacts, so readers can inspect the contracts behind the prose;
- the book is written for practitioners who need to ship and operate agents, not only understand model behavior in the abstract;
- the multilingual surface broadens reach without changing the technical promise.

Bio gap to fill before submission: add a short human author bio with role, relevant production/engineering background, public writing or project links, and any constraints on how personal credentials should be presented.

## Comparable Books Draft

Use these as shelf-positioning references, not as direct substitutes:

- **Designing Data-Intensive Applications** — comparable in systems-thinking discipline; this book applies that level of operational seriousness to agent behavior, policy, memory, evals, and lifecycle.
- **Designing Machine Learning Systems** — comparable in production ML framing; this book narrows the lens to agent systems with tools, approvals, traces, rollout gates, and runtime control.
- **AI Engineering** — comparable in practical LLM application building; this book goes deeper on governed side effects, evidence, registry, and production accountability.
- **Building Secure & Reliable Systems** — comparable in security/reliability posture; this book translates those instincts into agent-specific trust boundaries, approvals, evals, and observability.
- **Site Reliability Engineering** — comparable in operational culture; this book focuses on the agent-specific question of how autonomy, memory, tools, and lifecycle should be made observable and governable.

Short differentiation: the book is not trying to be the broadest AI overview or the deepest ML training book. Its shelf claim is narrower: **how to architect production AI agents as governed systems with explicit rights, evidence, side-effect control, eval gates, and lifecycle ownership**.

## Print Manuscript vs Online Companion Draft

Print manuscript:

- carries the argument, chapter questions, decision frameworks, failure stories, and durable operating model;
- keeps long field lists, exhaustive schemas, and fast-moving implementation details out of the main reading path;
- uses Support Triage as the primary through-line, with Internal Knowledge and Incident Coordination as contrast cases.

Online companion:

- hosts the multilingual public site;
- keeps runnable reference-runtime material, schemas, configs, and tests close to the text;
- can evolve with tooling, eval practice, and implementation details without forcing the print manuscript to chase every framework change.

Practical pitch line: the book should read cleanly in print, while the companion site proves that the architecture is concrete enough to run, test, and inspect.

## Public Links Draft

Use these links in the final pitch packet after a fresh availability check:

- **Public book site:** <https://agent-axiom.github.io/agent-arch/>
- **English landing page:** <https://agent-axiom.github.io/agent-arch/en/>
- **Chinese landing page:** <https://agent-axiom.github.io/agent-arch/zh/>
- **Sample chapter candidate:** <https://agent-axiom.github.io/agent-arch/en/book/part-i/chapter-1/>
- **Technical credibility sample:** <https://agent-axiom.github.io/agent-arch/en/book/part-v/chapter-13/>
- **Reference runtime source:** <https://github.com/agent-axiom/agent-arch/tree/main/agent_runtime_ref>
- **Runnable reference package README:** <https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/README.md>
- **Runtime configs:** <https://github.com/agent-axiom/agent-arch/tree/main/agent_runtime_ref/configs>
- **Runtime tests:** <https://github.com/agent-axiom/agent-arch/tree/main/tests>

Pitch usage: send the public site and the two sample chapters first; keep the source/runtime/test links as proof points for editors who want to verify that the companion is concrete.

## Pitch Packet Checklist

Before sending to a publisher:

- one-page positioning memo;
- this publisher-ready TOC;
- one polished sample chapter;
- author/platform credibility note;
- print manuscript vs online companion note;
- comparable-books note;
- public site and runnable reference links.
