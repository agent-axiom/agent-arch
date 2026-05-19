# Publisher Packet Draft

Purpose:

- keep publisher-facing packet notes separate from the MkDocs site tree;
- keep the web site broad;
- keep the book-shaped manuscript, sample strategy, positioning, cover note, comparable shelf, and companion links together.

Status: working editorial artifact, not a public navigation page and not final email copy.

## Positioning

- **Working title:** Secure AI Agent Architecture.
- **Reader:** senior product engineers, platform engineers, security engineers, staff engineers, and technical leads.
- **Reader need:** ship AI agents with tool access, memory, approvals, observability, and evals.
- **Operating need:** preserve rollout discipline and lifecycle ownership.
- **Promise:** move from prompt demos to governed agent systems with explicit engineering contracts.
- **Contract examples:** identity, policy, tools, memory, traces, evals, rollout, and retirement.
- **Non-goal:** not a framework manual, not a prompt-trick book, and not a survey of vendor products.

## One-Page Positioning Memo Draft

**Title:** Secure AI Agent Architecture

**Subtitle:** From prompt demos to governed production systems.

**Primary reader:**

- platform and product architects responsible for agent systems;
- systems that can read private context, call tools, request approvals, write to external systems, and survive incidents.

**Problem:**

- most teams can build an impressive demo before they can explain the production control model;
- the missing model covers identity, policy, side effects, memory provenance, and eval gates;
- it also covers trace evidence, rollout ownership, and retirement.

**Why now:**

- agent systems are moving from isolated assistants into production workflows;
- those workflows now carry real permissions, long-running state, delegated work, and regulated evidence needs.

**Unique promise:**

- the book treats agents as production systems;
- it leads with architecture and workflow-first design;
- it makes control boundaries explicit;
- it ties evals to release judgment;
- it treats registry, provenance, observability, and retirement as lifecycle governance.

**Competing shelf:**

- cloud architecture;
- secure software design;
- MLOps/LLMOps;
- practical AI engineering books;
- distinction: governed agent behavior, not only model quality, prompts, or generic platform operations.

**Manuscript status:**

- public open manuscript with runnable reference package;
- core argument and sample-chapter structure are strong;
- publisher packet is drafted for editorial assembly;
- remaining pre-submission work: human author-bio framing and independent sample-chapter copy-edit;
- remaining packet decisions: sample selection and publisher-specific formatting.

**Companion assets:**

- reference runtime;
- schemas;
- checklists;
- case studies;
- source catalog;
- public documentation site.

## Print Manuscript Shape

Target:

- 6 parts;
- about 20 chapters;
- keep schemas, runtime command details, long checklists, and source catalogs in the online companion.

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
- schema appendices for traces, eval datasets, approvals, memory, and lifecycle artifacts;
- schema appendices for incident records, rollout gates, and policy bundles;
- command-output field lists and validation-error catalogs;
- case-study worksheets and templates;
- policy templates and checklists;
- community roadmap;
- source catalog and research frontier pages.

## Sample Chapter Candidates

### Chapter 1 — strongest publisher sample

Why:

- carries the thesis;
- starts from a failure story;
- shows how the book differs from prompt-hype or framework documentation.

Current strengths:

- opens from a concrete Support triage failure story;
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

Why:

- evals, traces, failure attribution, regression gates, and release judgment show production maturity.

Current strengths:

- includes a Support triage duplicate-ticket example;
- follows it from trace to verifier attribution, regression gate, rollout owner action, and release judgment;
- distinguishes behavioral evals, control evals, rollout gates, and verifier outputs;
- includes calibrated judge/human-review guidance;
- includes an evidence model;
- includes practical maturity and post-chapter checklists.

Remaining before external submission:

- independent copy-edit pass for print rhythm.

## Sample Chapter Export Manifest Draft

Use this manifest when assembling the first external packet.
It keeps the sample reproducible and prevents companion-link drift.

**Primary sample:**

- role: Chapter 1 as the first editorial sample;
- source path: `docs/book/part-i/chapter-1.en.md`;
- public URL: <https://agent-axiom.github.io/agent-arch/en/book/part-i/chapter-1/>.

**Secondary technical sample:**

- role: Chapter 13 as the technical credibility sample;
- source path: `docs/book/part-v/chapter-13.en.md`;
- public URL: <https://agent-axiom.github.io/agent-arch/en/book/part-v/chapter-13/>;
- send only when an editor asks for deeper eval, verifier, and rollout-gate proof.

**Export metadata to include:**

- title;
- subtitle;
- author placeholder;
- packet version `publisher-packet-2026-05`;
- sample role;
- source path;
- public URL;
- export date;
- companion-site URL.

**Pre-export checks:**

- selected sample has the current chapter-ending template;
- no unresolved TODO/editorial comments;
- no dependence on site navigation for context;
- no oversized runtime field lists;
- all footnotes and links survive the export.

**No-go signals:**

- stale public URL;
- mismatched source path;
- missing export date;
- missing packet version;
- sending Chapter 13 as the first sample without a specific technical-credibility reason.

## Sample Copy-Edit Handoff Brief Draft

Use this brief when handing Chapter 1, and optionally Chapter 13, to an independent copy editor for print rhythm.

**Copy-edit scope:**

- sentence flow;
- opening hook;
- paragraph cadence;
- transitions between failure story and architecture argument;
- consistency of `agent`, `workflow`, `runtime`, `policy`, `approval`, `trace`, `eval`, and `governance` terms;
- whether the chapter can stand alone without site navigation.

**Do not rewrite:**

- technical claims;
- case-spine roles;
- source references;
- companion-link boundaries;
- code identifiers;
- schema names;
- the workflow-first / governed-systems thesis.

**Questions for the editor:**

- Where does the sample feel too dense?
- Where does jargon appear before context?
- Which paragraph should be shortened for print?
- Does the ending template feel like a useful close rather than a checklist pasted onto the chapter?

**Return format:**

- annotated sample;
- short summary of top 5 changes;
- unresolved questions;
- suggested cuts that would move material to the online companion.

**No-go signals:**

- copy edits that weaken safety claims;
- edits that remove the Support triage through-line;
- changes that blur print vs companion boundaries;
- rewrites that turn the chapter into a framework tutorial.

## Editorial Compression Rules

- Every print chapter needs one main question.
- Every print chapter needs one unique artifact or decision framework.
- Avoid repeating governance language unless the chapter owns a distinct role.
- Keep long field lists online.
- Use Support triage as the primary running case.
- Use Internal knowledge assistant and Incident coordination as secondary contrast cases.
- End chapters with: what to remember, common failure modes, design-review use, companion assets, and next chapter.

## Author / Platform Credibility Note Draft

Use this as a conservative draft until the final bio is written.

Project platform:

- public multilingual book site;
- runnable reference runtime;
- configuration examples;
- tests;
- appendix material that demonstrates the operating model in concrete artifacts.

Claim supported by those artifacts:

- production AI agents should be designed as governed systems, not as prompt demos.

Credibility points to emphasize:

- the manuscript connects architecture, safety, observability, evals, rollout, and lifecycle ownership;
- those topics are treated as one operating model rather than separate concerns;
- the companion material includes runnable/reference artifacts;
- readers can inspect the contracts behind the prose;
- the book is written for practitioners who need to ship and operate agents;
- it is not only for readers who want to understand model behavior in the abstract;
- the multilingual surface broadens reach without changing the technical promise.

Bio gap to fill before submission:

- add a short human author bio with role;
- include relevant production/engineering background;
- include public writing or project links;
- record constraints on how personal credentials should be presented.

## Author Bio Input Brief Draft

Before this packet becomes external email copy, collect the human-authored facts.
Do not let the manuscript artifact invent those facts.

**Required inputs:**

- preferred author name;
- current role or independent label;
- 2-3 sentence production/engineering background;
- relevant public project links;
- public writing/talk links, if any;
- geographic/language framing, if the author wants it included.

**Optional inputs:**

- prior books or publications;
- notable systems shipped;
- open-source maintainership;
- security/reliability/AI platform experience;
- communities or companies that can be named publicly.

**Tone constraints:**

- avoid inflated authority claims;
- avoid unverifiable employment claims;
- avoid private client details;
- avoid credentials that cannot be shown to an editor;
- prefer concrete artifact-backed credibility;
- useful credibility artifacts: public book site, runnable reference runtime, tests, schemas, and companion material.

**Bio slots to prepare:**

- one-line byline;
- 50-word short bio;
- 100-word proposal bio;
- one credential sentence for the cover note.

**No-go signals:**

- missing preferred name;
- unverifiable claims;
- private employer/client details;
- bio text that makes the project sound like a vendor framework rather than a systems architecture book.

## Comparable Books Draft

Use these as shelf-positioning references, not as direct substitutes:

- **Designing Data-Intensive Applications**
  - Comparable angle: systems-thinking discipline.
  - Difference: applies that operational seriousness to agent behavior, policy, memory, evals, and lifecycle.
- **Designing Machine Learning Systems**
  - Comparable angle: production ML framing.
  - Difference: narrows the lens to agent systems with tools, approvals, traces, rollout gates, and runtime control.
- **AI Engineering**
  - Comparable angle: practical LLM application building.
  - Difference: goes deeper on governed side effects, evidence, registry, and production accountability.
- **Building Secure & Reliable Systems**
  - Comparable angle: security/reliability posture.
  - Difference: translates those instincts into agent-specific trust boundaries, approvals, evals, and observability.
- **Site Reliability Engineering**
  - Comparable angle: operational culture.
  - Difference: focuses on how autonomy, memory, tools, and lifecycle should be observable and governable.

Short differentiation:

- not trying to be the broadest AI overview;
- not trying to be the deepest ML training book;
- narrower shelf claim: architect production AI agents as governed systems;
- key controls: explicit rights, evidence, side-effect control, eval gates, and lifecycle ownership.

## Print Manuscript vs Online Companion Draft

Print manuscript:

- carries the argument, chapter questions, decision frameworks, failure stories, and durable operating model;
- keeps long field lists, exhaustive schemas, and fast-moving implementation details out of the main reading path;
- uses Support triage as the primary through-line;
- uses Internal knowledge assistant and Incident coordination as contrast cases.

Online companion:

- hosts the multilingual public site;
- keeps runnable reference-runtime material, schemas, configs, and tests close to the text;
- can evolve with tooling, eval practice, and implementation details;
- avoids forcing the print manuscript to chase every framework change.

Practical pitch line:

- the book should read cleanly in print;
- the companion site proves that the architecture is concrete enough to run, test, and inspect.

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

Pitch usage:

- send the public site and the two sample chapters first;
- keep the source/runtime/test links as proof points;
- use those proof points for editors who want to verify that the companion is concrete.

## Public Link Availability Record

Last checked: **2026-05-19** for packet version `publisher-packet-2026-05`.

Checked links:

- public book site;
- English landing page;
- Chinese landing page;
- Chapter 1 sample;
- Chapter 13 technical sample;
- reference runtime source;
- runtime README;
- runtime configs;
- runtime tests.

Result: all nine checked public links returned HTTP 200 during the packet-readiness pass on 2026-05-19.

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
> I am preparing **Secure AI Agent Architecture**, a practical systems book for platform engineers, product engineers,
> security engineers, staff engineers, and technical leads.
>
> The book is for teams that need to ship AI agents with real tool access, memory, approvals, observability, evals,
> rollout discipline, and lifecycle ownership.
>
> The premise is that production agents should be treated as governed systems, not prompt demos.
> Identity, policy, tools, memory, traces, eval gates, rollout, and retirement become explicit engineering contracts.
>
> The manuscript is paired with a public multilingual companion site and runnable reference material.
> The architecture is therefore not only described, but inspectable.
>
> I would lead with Chapter 1 as the sample chapter.
> Chapter 13 is available as a secondary technical sample if you would like to see the eval and release-gate treatment.
>
> I would be glad to share the positioning memo, publisher-ready table of contents, sample chapter, and companion links
> for review.

Before sending:

- replace the greeting;
- add the final author bio/credential sentence;
- tailor the final paragraph to the target editor or imprint.

## Target Editor / Imprint Formatting Brief Draft

When a real editor or imprint is chosen, adapt the packet without changing its technical claims.

**Inputs to collect:**

- editor name;
- imprint;
- submission channel;
- requested proposal format;
- attachment rules;
- word/page limits;
- sample-chapter policy;
- comparable-title expectations;
- whether links are allowed in the first email.

**Formatting decisions:**

- decide whether the first contact sends only the cover note and links;
- decide whether to send a short proposal PDF;
- decide whether to attach the Chapter 1 sample;
- decide whether Chapter 13 should also be attached as a technical sample;
- match file names to packet version `publisher-packet-2026-05`.

Example filename:

- `secure-ai-agent-architecture-proposal-publisher-packet-2026-05.pdf`.

**Tailoring rules:**

- keep title, reader, problem, unique promise, print/companion split, and governed-systems positioning stable;
- tailor examples and comparable titles to the imprint;
- do not overstate market size;
- do not overstate author credentials;
- do not overstate Chinese edition readiness;
- do not overstate framework maturity.

**No-go signals:**

- unknown editor name;
- unknown attachment policy;
- ignored page limits;
- broken filename/version convention;
- pitch language that turns the companion runtime into a promised production framework.

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

Default recommendation:

- lead with Chapter 1 only;
- use it because it carries the thesis and reads best as a first editorial sample;
- keep Chapter 13 ready as a second attachment or follow-up;
- send Chapter 13 when the conversation turns to technical credibility.

## Print/PDF Readiness Gate Draft

Before any print-style PDF or sample-chapter export is sent externally, run a separate pass for print friction.
Do not assume the web page will translate cleanly.

**Print/PDF checks:**

- exported sample chapter has stable heading hierarchy, page breaks, footnotes, and code-block wrapping;
- diagrams, tables, admonitions, and callout boxes remain readable in grayscale and on narrow pages;
- URLs are visible enough for print readers;
- companion-only links are grouped instead of scattered through the prose;
- long schema tables and command-output field lists stay in the online companion;
- validation-error catalogs and runtime internals stay in the online companion;
- screenshots or generated figures, if added later, have source files and alt-text notes;
- the export includes title, subtitle, author placeholder, packet version, and sample-chapter date.

**No-go signals:**

- broken heading levels;
- clipped code blocks;
- unreadable diagrams;
- orphaned footnotes;
- missing packet version;
- print sample that depends on live site navigation to make sense.

## Submission Release Discipline Draft

Treat the publisher packet as a small release, not as a loose collection of notes.

**Packet version:** `publisher-packet-2026-05` until a target editor or imprint requires a different format.

**Freeze scope before sending:**

- cover note;
- one-page positioning memo;
- publisher-ready TOC;
- selected sample chapter;
- author/platform credibility note;
- comparable-books note;
- print/companion split;
- public links.

**Pre-send gates:**

- author bio and credential framing are final enough for the chosen editor;
- selected sample chapter has had an independent print-rhythm copy-edit;
- public site, sample-chapter links, repository links, runtime links, and test links have passed fresh checks;
- Chinese surfaces remain labeled as draft localization preview unless a finished Chinese edition is prepared;
- packet attachments match the order in “Recommended Submission Packet Order”;
- no runtime internals or validation-error catalogs are moved into the print manuscript packet by accident;
- no long schema tables are moved into the print manuscript packet by accident.

**No-go signals:**

- missing author bio;
- unverified links;
- unclear sample selection;
- publisher-specific format not applied;
- claim that implies the Chinese layer is a finished edition.

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

## External Submission Blocker Register

The packet is drafted, link-checked, and internally gated.
It should not be sent externally until these human/editorial blockers are closed.

Print-friendly blocker list. Each item keeps the original fields as short sub-bullets:

- **Author bio and credential framing**
  - Current state: open.
  - Owner/input needed: human author supplies preferred name, role, public links, and credential constraints.
  - Packet action when closed: replace placeholder bio and cover-note credential sentence.
- **Independent sample copy-edit**
  - Current state: open.
  - Owner/input needed: copy editor returns annotated Chapter 1 sample and top 5 changes.
  - Packet action when closed: apply accepted edits and update sample export date.
- **Sample selection**
  - Current state: default chosen, not target-specific.
  - Owner/input needed: editor/imprint policy or author decision confirms Chapter 1 only vs Chapter 1 plus Chapter 13.
  - Packet action when closed: freeze attachment list and proposal order.
- **Target editor / imprint formatting**
  - Current state: open.
  - Owner/input needed: target editor, imprint, submission channel, attachment rules, and page limits.
  - Packet action when closed: tailor cover note, file names, and proposal format.

**Submission state:** not externally sendable until all four blockers are closed or explicitly waived by the author.

## Blocker Waiver / Decision Log Draft

Use this log if the author decides to waive a blocker or make a target-specific packet decision.
Do not remove the blocker register; record why the exception is safe enough for the chosen submission.

Print-friendly waiver log starter:

- **Date:** TBD.
- **Decision:** no waivers yet.
- **Applies to blocker:** n/a.
- **Decider:** n/a.
- **Rationale:** all four blockers remain open.
- **Follow-up:** collect author/editor inputs before external submission.

**Waiver rules:**

- every waiver needs a named decider, date, scope, rationale, and follow-up owner;
- no invented author credentials;
- no unverified links;
- no claim that the Chinese layer is a finished edition;
- no promise that the companion runtime is a production framework.

**No-go signals:**

- anonymous waiver;
- global waiver without scope;
- waived link check after URLs changed;
- waived copy-edit after substantive sample edits;
- waiver text that contradicts the packet's governed-systems positioning.
