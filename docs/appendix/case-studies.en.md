# Practical Case Studies

This page answers a simple question: what does the book look like not as abstraction, but as a living system?

Below are three scenarios where architectural layers, guardrails, and orchestration choices can already be discussed as engineering decisions rather than elegant language.

If you need reusable policy artifacts rather than scenarios, go to [Policy Templates](policy-templates.en.md). If you want the next layer of book improvements, open the [Community Roadmap](community-roadmap.en.md).

!!! example "How to read this case now"
    The support triage case has become the book's running thread: start here, then watch the same duplicate-ticket failure move through trust boundaries, tool gateway, memory/retrieval, idempotency, traces, SLOs, eval gates, ownership, runtime, policy, rollout, ADLC, assurance, provenance, retirement, misalignment controls, telemetry, and registry.

!!! note "Canonical case alignment"
    These scenarios correspond to the three canonical cases from the book plan. **Support triage** is Case 1 for write capability, approvals, and duplicate-ticket recovery. **Internal knowledge assistant** is Case 2 for retrieval, memory, access control, freshness, and knowledge provenance. **Incident coordination** is Case 3 for traces, SLOs, escalation, notification side effects, response ownership, and post-incident learning.

## Cross-chapter route

Keep these cases beside the main text as coverage checks:

- **Chapter 1:** choice between workflow, single-agent loop, and multi-agent shape;
- **Chapter 2:** path through the reference architecture, control plane, and data boundaries;
- **Chapters 3-4:** trust boundaries, approvals, policies, and the agent's right to act;
- **Chapters 5-7:** memory, retrieval, freshness, knowledge provenance, and poisoning defense;
- **Chapters 8-10:** tool gateway, MCP/A2A, idempotency, retries, and rollback;
- **Chapter 13:** evals, verifier, and regression gates;
- **Chapter 18:** rollout readiness and pre-scale review;
- **Chapters 21-27:** lifecycle, assurance, provenance, retirement, telemetry, and registry.

## Industrial runtime patterns

These case studies are easier to read next to industrial examples. They do not mean the reader should copy a vendor product, but they show which production shapes are becoming recognizable.

### Cloudflare Agents SDK: agent as a named durable object

Cloudflare Agents SDK shows a pattern where an agent is not only a transient loop around a model, but an addressable `Agent` instance on top of a Durable Object: it has a stable name, durable SQL/key-value state, WebSocket connections, scheduled tasks, wakeups, and hibernation. The architectural lesson for the book is simple: when an agent is bound to a real-world entity — customer case, tenant workspace, incident room, device, project, or research dossier — the runtime should make it clear who owns state, which runs changed it, which scheduled tasks can wake the instance, and which traces prove safe resume.

The practical contract is: **stable name → durable state → wake/hibernate → scheduled/background work → approval gates → trace evidence**. That ties the chapters on memory, background updates, execution, traces, and rollout into one shape: a schedule should not be an invisible callback, a WebSocket UI should not expose all agent state, and an approval should live where the side effect actually happens. The newer long-running agents pattern adds the key wording: agent identity outlives the process, so durable log, idempotency key, and replay boundary should be mandatory for any side effect after a pause or approval.

### Cloudflare vulnerability harness: VDH, VVS, and noise filtering

Cloudflare separately describes a vulnerability harness that began as a `security-audit` skill and then became a fleet-wide pipeline: Recon builds a threat model, Hunters attack code by bug class, Validate tries to disprove each finding, Gapfill closes thin coverage cells, Dedup collapses duplicates, Trace follows issues into consumer repos, Feedback rewrites future tasks, and Report renders without a model. The architectural lesson is that a harness should not be “one large agent reads the whole repository.” Each stage writes state to a database keyed by `run_id`, `repo`, and `stage`, can resume or retry, and leaves reviewable findings, so a five-hour run is not lost to one transient failure.

The second lesson is separating discovery from validation. The Vulnerability Discovery Harness (VDH) intentionally generates many candidates, while the Vulnerability Validation System (VVS) receives them in a separate queue with deduplication, judgment, and fixing. A different model/provider and a different logical path recheck the finding, production reachability, and freshness on latest main. For this book, that is a useful industrial case not only about security, but about agent eval architecture: the model can be replaceable, while the durable asset is the orchestration layer with an independent verifier, deterministic bookkeeping, and human review before any production-impacting change.

The minimal portable contract is: **recon → hunt → validate → dedup/judgment → fail→pass patch gate → human review**. A finding should carry a threat model, affected boundary, evidence refs, working PoC/test against untouched code, proposed patch, mechanical schema/path validation, independent validator verdict, duplicate key, reachability judgment, and remediation status. It also needs a health signal for shallow runs: if a hunt finishes suspiciously fast without findings, sub-hunts, or gap tasks, that is not a clean repository; it is a reason to requeue and inspect harness failure.

### Cloudflare enterprise MCP: gateway and portal as policy choke point

Cloudflare's enterprise MCP reference architecture is useful because it treats **enterprise MCP** as a governed platform surface, not only as a convenient tool protocol. The pattern combines remote MCP servers, Cloudflare Access, **MCP server portals**, **AI Gateway**, and Cloudflare Gateway for **Shadow MCP** detection. For this book, the key move is making the MCP gateway and portal a policy choke point: tools are discovered through an approved surface, authorization is centrally mediated, and unapproved remote MCP servers become detectable rather than invisible local config.

The portable contract is: **approved MCP portal → progressive tool disclosure → identity-bound authorization → gateway policy and DLP → audit trail → Shadow MCP detection**. Progressive tool disclosure matters because a large tool catalog is both a token-cost problem and a safety problem: the agent should receive the right capability slice for the task, not every tool the enterprise owns. Shadow MCP detection matters because otherwise teams can quietly recreate the old shadow-API problem with agent tools.

Cloudflare Code Mode adds the practical anti-pattern: do not load every API operation into the prompt as a separate tool. Instead of tool-list stuffing, the server can expose a small `search()` and `execute()` surface: the first tool searches a typed API/spec catalog, and the second executes generated code inside a sandboxed isolate with explicit permission scopes. For enterprise MCP, that changes the governance shape: the catalog stays behind the gateway, discovery becomes an auditable operation, and execute passes through the same policy, DLP, rate-limit, and approval boundary as any privileged tool call.

### Google DeepMind AI Control Roadmap: control as runtime infrastructure

Google DeepMind describes the AI Control Roadmap as a defense-in-depth layer for internal agents: traditional security hygiene and alignment remain the base, but the system additionally starts from the cautious assumption that a capable agent may be misaligned or may simply behave unexpectedly. In practice, an agent with access to internal systems should be modeled as a potential insider threat, not only as a chat interface exposed to prompt injection. Control is therefore shaped as a runtime contract: MITRE ATT&CK-inspired threat modeling, monitoring of actions and plans, supervisor systems, prevention/response gates, and continuous measurement of coverage, recall, and time-to-response.

The useful lesson for the book is not a vendor-specific safety claim, but the operational control shape. An agent system should distinguish adversarial misuse from well-intentioned but excessive task optimization: DeepMind explicitly notes that many flagged events in coding-agent trajectories came from misinterpretation or overeagerness rather than hostile intent. The architectural conclusion is that the policy layer, rollout gate, and assurance loop must catch not only “attacks,” but also behavior that looks locally helpful and systemically destructive.

The minimal portable contract is: **threat model → monitored coverage → supervisor judgment → synchronous block/asynchronous response → escalation → audit trail**. For low-risk and reversible actions, delayed review and remediation may be enough; for high-risk actions, a synchronous prevention path is needed. Control metrics should be release-bearing: if coverage drops, verifier recall is not proven, or time-to-response does not match the action risk, the rollout should not expand.

### OpenAI internal coding-agent monitoring: runtime behavioral monitoring as evidence

OpenAI's [How we monitor internal coding agents for misalignment](https://openai.com/index/how-we-monitor-internal-coding-agents-misalignment/) adds a practical layer to the DeepMind control pattern: **runtime behavioral monitoring** is not only observability, but evidence for a future **safety case**. The monitor reviews realistic coding-agent sessions, including chains of thought and actions, and escalates behavior that appears inconsistent with user intent or internal security and compliance policy.

For this book, the useful lesson is the feedback loop: **agent trajectory → monitor classification → severity → human review → safeguard update → control eval**. Monitoring should not be sold as a guarantee. It depends on monitorability, privacy-preserving access to traces, known latency, and measured coverage, recall, and time-to-response. The architecture should also say where asynchronous review is enough and where high-risk actions need synchronous blocking before execution.

### OpenAI Tax AI for Crete: practitioner correction as eval fuel

OpenAI and Thrive Holdings describe Tax AI for Crete's firm network as a self-improving agent case not because the model vaguely "fixes itself," but because the product environment turns expert work into a measurable improvement loop. Practitioners prepare and review tax forms, the system preserves the path from source documents through extracted fields, citations, tax-engine mapping, and the filed return, and repeated practitioner corrections become structured findings, tailored evals, and bounded Codex tasks.

For this book, the important addition to the evals, traces, and ADLC chapters is that human review should not be a terminal manual edit that disappears after filing. If a person corrects a field, the architecture should preserve the expected value, predicted value, provenance, review status, grouping key, and decision about whether the difference is an actionable product failure or expected workflow noise. Only a repeated, reviewed pattern should become an eval target; ambiguous tax judgment and unsupported product behavior should route back to product and engineering review rather than being forced through the loop.

The minimal portable contract is: **expert correction → production trace → reviewed finding → targeted eval → scoped Codex task → regression gate → engineering review → shipped improvement**. For high-stakes domains, this is both an HCI pattern and an assurance pattern: practitioners steer direction, production traces preserve evidence, Codex investigates within a bounded worktree with read-only production context, and engineers remain responsible for product changes before rollout.

### Microsoft AutoJack: localhost stops being a trust boundary

Microsoft Defender Security Research describes AutoJack as an exploit chain in AutoGen Studio where untrusted web content rendered by a browsing agent could reach a local MCP WebSocket and spawn a host process. The concrete issue was fixed before the affected MCP surface shipped in a PyPI release, but the architectural lesson is broader than one project: if an agent can browse the open web and also reach privileged local services, `localhost` becomes part of the attack surface.

For this book, AutoJack is a practical confused-deputy case study for agent harnesses. An origin allowlist for `127.0.0.1` or `localhost` does not prove trust when the request is made by the agent's headless browser or code tool on the same machine. Auth, policy, and executable allowlists for MCP servers have to live on the control-plane endpoint, not in the assumption that loopback is reachable only by a human developer.

The minimal portable contract is: **untrusted web content → browser/tool agent → local control channel → authenticated MCP/control plane → allowlisted execution boundary → audit trail**. Every local MCP/debug/control socket should require authn/authz, purpose binding, a policy gate, launch-parameter allowlists, and an isolation profile. Browser tools should run with a separate network and process identity so external content does not inherit the trust of the developer workstation or agent host.

### Microsoft prompts become shells: prompt injection as host execution

Microsoft's “When prompts become shells” research is a separate case from AutoJack. AutoJack shows a browser-agent crossing a local control channel; this case shows **prompt injection -> tool parameters -> host execution** inside an agent framework. In the Semantic Kernel examples, the model behaved as designed: it mapped language into tool calls. The unsafe boundary was the framework/tool layer that trusted parsed, model-controlled parameters and let them reach an execution primitive.

The portable lesson is blunt: **AI models are not security boundaries**. Any value derived from the model should be treated as attacker-controlled input until the gateway, tool wrapper, or sandbox proves otherwise. That means a `tool exposure review` must inspect not only which tools exist, but also whether their argument schemas can touch paths, commands, templates, dynamic code, file writes, deserialization, reflection, or query/expression languages. `path validation` is not a polish detail; it is the boundary between “the model selected a document” and “the model supplied a filesystem primitive.”

The minimal portable contract is: **untrusted prompt/content → model-controlled parameters → typed validation → allowlisted operation → per-tool sandbox → audit trail**. For execution-adjacent tools, the default should be deny-by-default tools, no string interpolation into shells or evaluators, canonical path validation, read/write scope checks, per-tool sandboxing, and an audit event that records the redacted model parameters, validation result, sandbox profile, and policy decision.

### GitHub Copilot cloud agent: cloud coding agent contract

GitHub Copilot cloud agent shows a different production shape: the agent receives work from GitHub, an IDE, CLI, API, or integration; researches the repository; plans changes; pushes code to a separate branch; exposes session logs; and then opens a pull request for human review. The important point is not merely that “an agent writes code,” but that autonomy is packaged inside a familiar engineering lifecycle.

For this book, the useful contract is: **request/issue → isolated task session → branch → commits/logs → validation/security checks → human review → pull request**. The branch becomes the change boundary, session logs become the observability surface, the PR becomes the approval gate, and allowing GitHub Actions to run on the agent branch becomes a separate risk decision because workflows may reach secrets or write permissions. The same pattern should carry into other cloud coding agents: an autonomous worker may do preparatory work, but merge, privileged workflows, and production impact should remain reviewable control points.

[Security validation for third-party coding agents](https://github.blog/changelog/2026-06-09-security-validation-for-third-party-coding-agents/) strengthens this pattern: GitHub applies to code from third-party coding agents the same automatic controls it applies to Copilot cloud agent: CodeQL, checks of newly introduced dependencies against the GitHub Advisory Database, and secret scanning. For this book, that is an important control-plane signal. An agent-generated PR should not be treated as “ready for review” merely because the agent finished the task; platform-owned gates should inspect vulnerabilities, dependency risk, and leaked secrets before the pull request is finalized. If such a gate finds an issue, the agent can try to repair it, but the rule belongs to the platform, not to the agent.

[Secret scanning with GitHub MCP Server](https://github.blog/changelog/2026-05-05-secret-scanning-with-github-mcp-server-is-now-generally-available/) moves one of those checks earlier in the loop: an MCP-compatible coding agent or IDE can scan current changes for exposed secrets **before you commit**. The useful agentic-SDLC contract is therefore stronger: scan before you commit or open a pull request, keep bypass behavior aligned with repository push protection, and make leaked-secret repair part of the agent's task closure rather than a late repository alarm.

Newer Copilot changes make this case even more repo-native. Copilot code review now reads `AGENTS.md`, so the repository instruction file becomes a living agent contract, not only a local CLI hint. Copilot cloud agent automations add an unattended path from repository events or scheduled triggers into a cloud-agent session; those automations therefore need an owner, trigger schema, branch policy, approval boundary, and trace linkage. BYOK in the Copilot app completes the pattern: model keys and provider routing become part of a provider-neutral control plane, not an individual developer preference.

### IDE agents as managed work queues

The June GitHub Copilot in VS Code updates show another shift: the IDE is becoming not only a place where a person writes a prompt, but an operator console for multiple agent work items. One window now includes parallel sessions, multiple chats inside a session, an integrated browser for agent-driven validation, session and subagent cost visibility, model/provider choice through the Marketplace, synced session history, gutter feedback, and a more independent Autopilot. These are not isolated interface conveniences; they are an emerging control-plane pattern: agent work becomes an observable task queue, not one endless chat.

The portable contract is: **work item → isolated/resumable session → visible status and cost → model/provider policy → browser/tool isolation → human feedback → reviewable artifact**. For a runtime, that means `session_id`, `work_item_id`, `model_policy`, `usage_accounting`, `browser_context`, `tool_permissions`, `human_feedback_refs`, and `artifact_refs` should be first-class fields rather than incidental UI logs. OpenAI's material on Codex adoption across different business functions reinforces the same conclusion: when agents take on long and parallel tasks, organizations need an operator loop that shows queue, cost, human owner, status, and intervention point.

## Case 1. Support triage

### What the system does

The agent receives an incoming customer request, gathers context, checks ticket history, and selects the next safe step:

- answer immediately;
- ask for clarification;
- create a ticket;
- escalate to a human.

### Why an agent is justified here

An agent makes sense here because:

- incoming messages are unstructured;
- the decision depends on a combination of text, account history, and policy;
- the path is not fixed, but it also does not require full autonomy.

This is a good candidate for `workflow + guarded agent loop`.

### Recommended shape

- one main triage agent;
- read-heavy tools for customer profile and ticket history;
- a write tool only for `create_ticket`;
- an approval boundary for sensitive actions;
- structured decision output for every run.

### Main risks

- prompt injection through the customer message;
- leakage of neighboring tenant context;
- unnecessary write action during unstable integrations;
- too much freedom in the triage agent.

### What matters most in the architecture

- strict separation of instructions from customer text;
- no direct helpdesk API access for the agent;
- stop conditions stored in the triage routine;
- logging of all write intents and approvals.

### Operational minimum

- **Success criteria:** the answer or ticket is created once, in the right tenant context, with an explainable basis.
- **Failure criteria:** unnecessary write action, neighboring-context leakage, lost approval, or no recoverable trace.
- **Minimum telemetry:** `session_id`, `trace_id`, selected action, retrieval sources, policy decision, approval state, and idempotency key.
- **Minimum eval dataset:** normal request, ambiguous request, prompt-injection attempt, retry after timeout, and duplicate-ticket scenario.
- **Approval model:** simple ticket creation can proceed under policy; priority changes, escalations, mass notifications, and retries after unknown side effects require fresh approval.
- **Memory policy:** long-term memory must not store customer text as trusted fact; only validated tenant-scoped preferences with provenance, TTL, and cleanup support are allowed.
- **Tool risk profile:** profile and history reads are low risk; ticket creation is medium risk with idempotency; status, priority, or recipient changes are high risk with approval.
- **MCP/A2A exposure:** the support MCP server must be in the approved registry and filter returned values; A2A handoff to support must not transfer write authority without a separate decision.
- **Rollout gate:** canary shows no duplicate writes, and the verifier confirms tenant isolation and the correct approval path.
- **Example incident:** a timeout after `create_ticket` leaves `side_effect_unknown`, and a retry attempts to create a second ticket.
- **Postmortem questions:** where did idempotency fail, who saw the approval state, why did the trace not stop the retry, and which eval should block the regression now?
- **Retirement condition:** the old ticket-write path is closed, pending approvals have expired, the tool principal is revoked, and the registry points only to the new write contract.

### Where to read in the book

- [Chapter 3. Security Perimeter and Trust Boundaries](../book/part-ii/chapter-3.en.md)
- [Chapter 8. Execution Model and Tool Catalog](../book/part-iv/chapter-8.en.md)
- [Practice. Instructions, Routines, and Prompt Templates](../book/part-i/practical-routines.en.md)

## Case 2. Internal knowledge assistant

### What the system does

This agent helps employees find knowledge across documentation, runbooks, tickets, and internal wiki pages.

It:

- understands the question;
- performs retrieval;
- assembles a grounded answer;
- shows sources;
- and when confidence is low, limits the answer instead of inventing.

### Why one agent is often enough here

In this case, many teams move into multi-agent too early. Usually they do not need to.

Most of the time, it is enough to have:

- one agent loop;
- a strong retrieval pipeline;
- a separate policy layer;
- explicit marking of untrusted content;
- quality gates for answer generation.

### Main risks

- retrieval noise;
- role-inappropriate access to documents;
- leakage from private knowledge zones;
- hallucinations under weak grounding.

### What matters most in the architecture

- tenant- and role-scoped retrieval;
- short-term state separated from long-term memory;
- source references in the output;
- traces for retrieval and answer assembly.

### Operational minimum

- **Success criteria:** the answer is grounded in allowed sources, shows citations, and honestly limits confidence.
- **Failure criteria:** answer without sources, role-inappropriate access, mixed short-term state and long-term memory, or hallucinated policy.
- **Minimum telemetry:** query, retrieval scope, source IDs, confidence signal, denied sources, and answer-grounding verdict.
- **Minimum eval dataset:** known answer, insufficient context, role-denied document, conflicting sources, and stale knowledge.
- **Approval model:** reading allowed sources needs no approval; memory writes, retrieval-scope expansion, and sensitive answers require policy approval or human review.
- **Memory policy:** short-term state is cleared after the session; long-term memory stores only validated facts with provenance, TTL, tenant scope, and no writes from untrusted text.
- **Tool risk profile:** retrieval from the approved corpus is low risk; memory writes and corpus updates are medium risk; access expansion and tenant-filter changes are high risk.
- **MCP/A2A exposure:** MCP retrieval must return source identifiers and access labels; A2A expert handoff may share the question and selected citations, not the full hidden session context.
- **Rollout gate:** regression set confirms grounding, role isolation, and correct low-confidence behavior.
- **Example incident:** the agent answers from a stale runbook without citations and exposes a document outside the employee's role.
- **Postmortem questions:** why did retrieval scope expand, which source was trusted, where should the low-confidence stop have fired, and which eval covers stale knowledge?
- **Retirement condition:** the stale corpus, embeddings, and memory-write rules are disabled, and the replacement corpus passes provenance and access review.

### Where to read in the book

- [Chapter 5. Why an Agent Needs Memory, and Why Memory Is Risky](../book/part-iii/chapter-5.en.md)
- [Chapter 7. Retrieval, Compaction, and Background Updates](../book/part-iii/chapter-7.en.md)
- [Chapter 11. Traces, Spans, and Structured Events](../book/part-v/chapter-11.en.md)

## Case 3. Incident coordination

### What the system does

The agent helps during an incident:

- gathers monitoring signals;
- enriches them with context;
- creates an incident thread;
- proposes the next runbook step;
- transfers the task to the right role.

This is no longer just a chat assistant. It is an operational system component.

### Why orchestration discipline matters especially here

This is where teams often make one of two mistakes:

- one overloaded manager agent;
- or handoffs introduced too early, with responsibility getting lost.

A good starting shape is usually:

- manager pattern for intake and coordination;
- handoffs only where a real role boundary begins;
- all write actions going through capability contracts.

### Main risks

- false confidence under noisy alerts;
- repeated side effects;
- loss of audit trail during handoffs;
- overly broad runtime permissions.

### What matters most in the architecture

- one trace for the entire incident run;
- explicit ownership at every handoff;
- idempotency for ticketing and notifications;
- human approval for risky remediation actions.

### Operational minimum

- **Success criteria:** the incident has one trace, the right owner, and one agreed next step.
- **Failure criteria:** duplicate notifications, lost handoff responsibility, risky remediation without approval, or split-brain across channels.
- **Minimum telemetry:** alert source, incident thread ID, handoff owner, runbook step, write intents, approvals, and notification idempotency keys.
- **Minimum eval dataset:** noisy alert, duplicate notification, wrong-owner handoff, missing runbook context, and risky remediation request.
- **Approval model:** thread creation and next-step suggestions can run under policy; escalation, external notifications, and remediation actions require the incident owner or on-call approver.
- **Memory policy:** incident working memory lives until post-incident review closes; only approved lessons, runbook updates, and artifact links persist long term.
- **Tool risk profile:** reading alerts and runbooks is low risk; creating the thread and notifying the team is medium risk; remediation actions and external notifications are high risk.
- **MCP/A2A exposure:** monitoring and notification MCP tools need narrow tokens; A2A responder handoff requires a correlation ID, delegation depth, and accountability-return rule.
- **Rollout gate:** dry run shows one trace chain, no duplicate side effects, and human approval for high-risk steps.
- **Example incident:** a noisy alert starts two parallel handoffs and sends duplicate notifications into different channels.
- **Postmortem questions:** where did split-brain enter the process, who owned each step, which idempotency keys were missing, and which dry run should have caught the duplicate?
- **Retirement condition:** the emergency-only path is closed, temporary tokens and notification channels are revoked, and the registry keeps only active roles and runbooks.

### Where to read in the book

- [Practice. Manager Pattern vs Handoffs](../book/part-i/practical-manager-handoffs.en.md)
- [Chapter 10. Idempotency, Retries, Rate Limits, and Rollback Boundaries](../book/part-iv/chapter-10.en.md)
- [Chapter 18. Production Rollout Checklist](../book/part-vii/chapter-18.en.md)

## What to Do Next

The best way to read them is not sequentially, but as a map:

- first choose the case closest to your task;
- then walk through the linked chapters;
- then come back and check whether your design is becoming more complex than it needs to be.

If the book is going to be useful to the community, these pages should eventually grow the fastest: they turn architecture into engineering leverage.
