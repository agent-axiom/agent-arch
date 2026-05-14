# Publisher Packet Draft

Purpose: keep publisher-facing packet notes separate from the MkDocs site tree. The web site can stay broad; this draft keeps the tighter book-shaped manuscript, sample strategy, positioning, cover note, comparable shelf, and companion links in one editorial artifact.

Status: working editorial artifact, not a public navigation page and not final email copy.

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

**Manuscript status:** public open manuscript with runnable reference package; core argument and sample-chapter structure are strong. The publisher packet is drafted for editorial assembly; remaining pre-submission work is human author-bio framing, independent sample-chapter copy-edit, sample-selection decision, and publisher-specific formatting.

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

## Sample Chapter Export Manifest Draft

Use this manifest when assembling the first external packet so the sample is reproducible and the companion links do not drift.

**Primary sample:** Chapter 1, `docs/book/part-i/chapter-1.en.md`, public URL <https://agent-axiom.github.io/agent-arch/en/book/part-i/chapter-1/>.

**Secondary technical sample:** Chapter 13, `docs/book/part-v/chapter-13.en.md`, public URL <https://agent-axiom.github.io/agent-arch/en/book/part-v/chapter-13/>. Send it only when an editor asks for deeper eval, verifier, and rollout-gate proof.

**Export metadata to include:** title, subtitle, author placeholder, packet version `publisher-packet-2026-05`, sample role, source path, public URL, export date, and companion-site URL.

**Pre-export checks:** selected sample has the current chapter-ending template, no unresolved TODO/editorial comments, no dependence on site navigation for context, no oversized runtime field lists, and all footnotes/links survive the export.

**No-go signals:** stale public URL, mismatched source path, missing export date, missing packet version, or sending Chapter 13 as the first sample without a specific technical-credibility reason.

## Sample Copy-Edit Handoff Brief Draft

Use this brief when handing Chapter 1, and optionally Chapter 13, to an independent copy editor for print rhythm.

**Copy-edit scope:** sentence flow, opening hook, paragraph cadence, transitions between failure story and architecture argument, consistency of `agent`, `workflow`, `runtime`, `policy`, `approval`, `trace`, `eval`, and `governance` terms, and whether the chapter can stand alone without site navigation.

**Do not rewrite:** technical claims, case-spine roles, source references, companion-link boundaries, code identifiers, schema names, or the workflow-first / governed-systems thesis.

**Questions for the editor:** where does the sample feel too dense, where does jargon appear before context, which paragraph should be shortened for print, and whether the ending template feels like a useful close rather than a checklist pasted onto the chapter.

**Return format:** annotated sample, short summary of top 5 changes, unresolved questions, and any suggested cuts that would move material to the online companion.

**No-go signals:** copy edits that weaken safety claims, remove the support-triage through-line, blur print vs companion boundaries, or turn the chapter into a framework tutorial.

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

## Author Bio Input Brief Draft

Before this packet becomes external email copy, collect the human-authored facts that should not be invented by the manuscript artifact.

**Required inputs:** preferred author name, current role or independent label, 2-3 sentence production/engineering background, relevant public project links, public writing/talk links if any, and geographic/language framing if the author wants it included.

**Optional inputs:** prior books or publications, notable systems shipped, open-source maintainership, security/reliability/AI platform experience, and communities or companies that can be named publicly.

**Tone constraints:** avoid inflated authority claims, unverifiable employment claims, private client details, or credentials that cannot be shown to an editor. Prefer concrete artifact-backed credibility: public book site, runnable reference runtime, tests, schemas, and maintained companion material.

**Bio slots to prepare:** one-line byline, 50-word short bio, 100-word proposal bio, and one credential sentence for the cover note.

**No-go signals:** missing preferred name, unverifiable claims, private employer/client details, or a bio that makes the project sound like a vendor framework rather than a systems architecture book.

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

## Public Link Availability Record

Last checked: **2026-05-14** for packet version `publisher-packet-2026-05`.

Checked links: public book site, English landing page, Chinese landing page, Chapter 1 sample, Chapter 13 technical sample, reference runtime source, runtime README, runtime configs, and runtime tests.

Result: all checked public links returned HTTP 200 during the packet-readiness pass.

Before external submission, rerun the check and update this record if any URL, branch, or packet version changes.

## Pitch Packet Checklist

Before sending to a publisher:

- one-page positioning memo;
- this publisher-ready TOC;
- one polished sample chapter;
- author/platform credibility note;
- print manuscript vs online companion note;
- comparable-books note;
- public site and runnable reference links.

## Cover Note Draft

Use this as a short editable note, not as final email copy:

> Dear [Editor],
>
> I am preparing **Secure AI Agent Architecture**, a practical systems book for platform engineers, product engineers, security engineers, staff engineers, and technical leads who need to ship AI agents with real tool access, memory, approvals, observability, evals, rollout discipline, and lifecycle ownership.
>
> The book's premise is that production agents should be treated as governed systems, not prompt demos. It explains how identity, policy, tools, memory, traces, eval gates, rollout, and retirement become explicit engineering contracts.
>
> The manuscript is paired with a public multilingual companion site and runnable reference material, so the architecture is not only described but inspectable. I would lead with Chapter 1 as the sample chapter; Chapter 13 is available as a secondary technical sample if you would like to see the eval and release-gate treatment in more depth.
>
> I would be glad to share the positioning memo, publisher-ready table of contents, sample chapter, and companion links for review.

Before sending, replace the greeting, add the final author bio/credential sentence, and tailor the final paragraph to the target editor or imprint.

## Target Editor / Imprint Formatting Brief Draft

When a real editor or imprint is chosen, adapt the packet without changing its technical claims.

**Inputs to collect:** editor name, imprint, submission channel, requested proposal format, attachment rules, word/page limits, sample-chapter policy, comparable-title expectations, and whether links are allowed in the first email.

**Formatting decisions:** choose whether the first contact sends only the cover note and links, a short proposal PDF, the Chapter 1 sample, or Chapter 1 plus Chapter 13. Match file names to the packet version, for example `secure-ai-agent-architecture-proposal-publisher-packet-2026-05.pdf`.

**Tailoring rules:** keep the title, reader, problem, unique promise, print/companion split, and governed-systems positioning stable. Tailor examples and comparable titles to the imprint, but do not overstate market size, author credentials, Chinese edition readiness, or framework maturity.

**No-go signals:** unknown editor name, unknown attachment policy, ignored page limits, broken filename/version convention, or pitch language that turns the companion runtime into a promised production framework.

## Recommended Submission Packet Order

Default packet order:

1. short cover note with title, reader, problem, and unique promise;
2. one-page positioning memo;
3. publisher-ready table of contents;
4. Chapter 1 as the primary sample chapter;
5. optional Chapter 13 technical sample if the editor asks for proof of production depth;
6. author/platform credibility note;
7. comparable-books note;
8. public site, runtime, config, and test links as companion proof points.

Default recommendation: lead with Chapter 1 only. It carries the thesis and reads best as a first editorial sample. Keep Chapter 13 ready as a second attachment or follow-up when the conversation turns to technical credibility.

## Print/PDF Readiness Gate Draft

Before any print-style PDF or sample-chapter export is sent externally, run a separate pass for print friction rather than assuming the web page will translate cleanly.

**Print/PDF checks:**

- exported sample chapter has stable heading hierarchy, page breaks, footnotes, and code-block wrapping;
- diagrams, tables, admonitions, and callout boxes remain readable in grayscale and on narrow pages;
- URLs are visible enough for print readers, while companion-only links are grouped instead of scattered through the prose;
- long schema tables, command-output field lists, validation-error catalogs, and runtime internals stay in the online companion;
- screenshots or generated figures, if added later, have source files and alt-text notes;
- the export includes title, subtitle, author placeholder, packet version, and sample-chapter date.

**No-go signals:** broken heading levels, clipped code blocks, unreadable diagrams, orphaned footnotes, missing packet version, or any print sample that depends on live site navigation to make sense.

## Submission Release Discipline Draft

Treat the publisher packet as a small release, not as a loose collection of notes.

**Packet version:** `publisher-packet-2026-05` until a target editor or imprint requires a different format.

**Freeze scope before sending:** cover note, one-page positioning memo, publisher-ready TOC, selected sample chapter, author/platform credibility note, comparable-books note, print/companion split, and public links.

**Pre-send gates:**

- author bio and credential framing are final enough for the chosen editor;
- selected sample chapter has had an independent print-rhythm copy-edit;
- public site, sample-chapter links, repository links, runtime links, and test links have passed a fresh availability check;
- Chinese surfaces remain labeled as draft localization preview unless a finished Chinese edition is actually prepared;
- packet attachments match the order in “Recommended Submission Packet Order”;
- no runtime internals, validation-error catalogs, or long schema tables are moved into the print manuscript packet by accident.

**No-go signals:** missing author bio, unverified links, unclear sample selection, publisher-specific format not applied, or any claim that implies the Chinese layer is a finished edition.

## Pitch Packet Status

Drafted and ready for editorial assembly:

- positioning memo;
- publisher-ready TOC shape;
- Chapter 1 as primary sample-chapter candidate;
- Chapter 13 as technical credibility sample;
- platform credibility note;
- comparable-books note;
- print/companion split;
- public and runtime/reference links.

Still needs human/editorial input before external submission:

- final author bio and credential framing;
- independent copy-edit of the selected sample chapter for print rhythm;
- decision on whether to send Chapter 1 only or include Chapter 13 as a secondary technical sample;
- final publisher-specific formatting after the target editor or imprint is chosen.
