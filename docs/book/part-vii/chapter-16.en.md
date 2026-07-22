# Chapter 16. Baseline Runtime Blueprint

!!! info "How to read this chapter"
    It helps to keep one practical question in mind rather than an abstract runtime topic:

    - where the run loop for the same support agent should actually live;
    - how not to collapse policy, memory, execution, and telemetry into one handler;
    - how to build a skeleton that survives not only the demo, but the rollout that follows.

    If those answers are fuzzy, the system usually keeps working only until the first serious change or incident.

## 1. Why a Reference Runtime Matters If You Already Have an Architecture

The architecture chapters are useful because they give you language and a frame. But at some point almost everyone asks the same question: "Fine, but what should this look like as a system you can actually build?"

That is the distinct promise of this chapter. It should help the reader cross one important boundary: from agreeing with the book's argument to seeing how that argument becomes runnable structure.

In the running support case, that is no longer theoretical. The agent can already check status, read memory, open a ticket through the gateway, and emit traces. But without an explicit runtime shape, those steps quickly spread across local handlers, ad hoc retries, and accidental integration bypasses.

That is where the reference runtime matters.

Its job is not to become the only possible implementation. Its job is to:

- fix the core modules in place;
- show the flow of one run;
- separate mandatory layers from optional enhancements;
- give the team a starting point without unnecessary magic.

That is also why this chapter should be read as a chapter about runnable structure under change pressure, not only as a chapter about module boundaries. The real question is whether the runtime now has a shape that can survive new policies, new tools, longer-lived runs, interrupts, and rollout pressure without dissolving back into handlers and exceptions.

## 2. A Minimally Mature Runtime Is Already More Than One Model

It helps to drop the picture of "an agent = one model call plus tools" right away.

A minimally mature runtime usually includes:

- an ingress layer;
- a run coordinator;
- policy hooks;
- a memory access layer;
- a tool/capability execution layer;
- a telemetry emitter;
- result assembly.

So the runtime is not "the place where the LLM is called". It is an orchestrated loop around the model.

## 3. What the Basic Flow of One Run Looks Like

For a reference implementation, it is useful to think about a run roughly like this:

1. accept the request and build run context;
2. run policy pre-checks;
3. assemble relevant context from memory/retrieval;
4. call the model;
5. if a tool call is needed, route it through the execution layer;
6. emit telemetry;
7. assemble the final result;
8. schedule background updates.

That is already far beyond "just chat with function calls", and it should be.

<div class="diagram-card">
<p>Even a baseline runtime already has several mandatory control points</p>

``` mermaid
flowchart LR
    A["Ingress"] --> B["Run context"]
    B --> C["Policy pre-check"]
    C --> D["Memory / retrieval"]
    D --> E["Model step"]
    E --> F{"Tool needed?"}
    F -->|No| G["Result assembly"]
    F -->|Yes| H["Execution layer"]
    H --> I["Tool result"]
    I --> E
    G --> J["Telemetry + background tasks"]
```

</div>

## 4. Which Modules Are Worth Keeping Separate Right Away

There are several boundaries worth making explicit in code even in version one:

- `runtime.py` or `orchestrator.py` for the run loop;
- `policy.py` for policy decisions;
- `memory.py` for retrieval and memory writes;
- `catalog.py` for the capability registry;
- `execution.py` for tool dispatch;
- `telemetry.py` for spans and structured events.

When all of this is packed into one big handler, the first demos come fast, but the system becomes painful to mature almost immediately.

!!! example "Case thread: where duplicate protection lives"
    In the support-triage runtime, duplicate-ticket protection should not hide inside the helpdesk adapter. `runtime.py` should own run context and the retry branch, `execution.py` should execute the write tool through an idempotent contract, `telemetry.py` should record `side_effect_unknown`, and `policy.py` plus the rollout gate should decide whether the run may continue. Then one incident does not spread across handlers.

**Runtime case-spine note:** the baseline runtime should support all three canonical cases without local bypasses. Support triage needs a write-capability path with approval hooks, idempotency contract, and duplicate-ticket telemetry. Internal knowledge assistant needs a retrieval path with source grounding, tenant filters, freshness checks, and guarded memory writes. Incident coordination needs an escalation path with responder-role checks, notification dispatch, incident-state updates, and post-incident background tasks.

## 5. Do Not Mix Orchestration With Business Adapters

One of the most expensive mistakes in early implementations is when the runtime knows too much about concrete external systems.

Then orchestration code starts to contain:

- branch logic for specific tools;
- knowledge of external payload shapes;
- local retries for specific APIs;
- ad hoc redaction;
- custom escape hatches for particular integrations.

The reference runtime should show the opposite idea: orchestration works through contracts, and adapters live at the edge of the system.

## 6. Example of a Minimal Project Structure

Here is a very grounded starting structure:

```text
agent_runtime/
  orchestrator.py
  policy.py
  memory.py
  catalog.py
  execution.py
  telemetry.py
  models.py
  background.py
```

This is not the only correct layout. But it already helps avoid throwing everything into one file and mixing control layers together.

## 7. A Simple Orchestrator Skeleton

This is not a production runtime, but a blueprint skeleton. It shows how run steps are separated and where the key control points should live.

```python
from dataclasses import dataclass


@dataclass
class RunRequest:
    user_input: str
    tenant_id: str
    principal_id: str


@dataclass
class RunResult:
    output_text: str
    status: str


def run_agent(request: RunRequest) -> RunResult:
    policy_check(request)
    context = retrieve_context(request)
    model_output = call_model(request, context)

    if model_output.get("tool_request"):
        tool_result = execute_tool(model_output["tool_request"])
        emit_event("tool_execution", tool_result)
        model_output = call_model(request, context + [tool_result])

    schedule_background_updates(request, model_output)
    return RunResult(output_text=model_output["text"], status="success")
```

The core point is simple: even the baseline runtime should already show policy, retrieval, tool execution, and background updates as separate stages.

## 8. Long-Running Runs Are Part of the Baseline, Not an Advanced Add-On

A common runtime mistake is to assume that every useful run should complete in one synchronous request. That assumption holds only while the system is still demo-shaped.

In a real support case, some runs are naturally longer-lived:

- waiting for approval;
- waiting for a tool with unstable latency;
- waiting for a second model pass after tool execution;
- waiting for a deferred follow-up or background update.

Recent OpenAI guidance is useful here because it treats background execution as a first-class runtime concern rather than a workaround for timeout problems.[^openai-background]

OpenAI's June 2026 Codex research gives the same point market evidence, not only architecture evidence: agentic AI changes the unit of knowledge work from a single interaction to delegated, long-horizon tasks, and by May 2026, 80.6% of sampled individual Codex users had made at least one request estimated to exceed 30 minutes of human work, 70.2% had made one estimated to exceed one hour, and 25.6% had made one estimated to exceed eight hours.[^openai-agents-transforming-work] Those thresholds are model-estimated, so they should be treated as directional rather than exact time accounting. But as a runtime signal, they point to a different control surface: measure not only request latency, but task horizon estimates, agent runtime, parallel workstreams, checkpoint age, and attention budget. OpenAI's Codex-maxxing guide phrases the operating pattern in plainer terms: break ambitious goals into verifiable steps, preserve context across workstreams, and decide explicitly where execution can be delegated to Codex versus where human oversight is most valuable.[^openai-codex-maxxing]

That is the right mental model for a baseline runtime too. The runtime should already distinguish between:

- `synchronous runs` that can safely finish in one foreground pass;
- `background runs` that continue after the initial response;
- `resumable runs` that pause on approval, external input, or deferred work.

### 8.1. Harness vs Runtime

LangChain draws a useful boundary: a harness gives the agent prompts, tools, skills, and the reasoning loop, while the production runtime is responsible for long work surviving crashes, deploys, human waits, and operational constraints.[^langchain-production-runtime] The book should not blur “a good agent harness” into “system architecture.” The harness can improve action quality, but the runtime must own durable execution, checkpoint boundaries, provenance-managed memory, tenant isolation, human-in-the-loop waits, observability, sandbox boundaries, and open integration protocols such as MCP/A2A.

Cloudflare/Flue material makes this boundary a little sharper: a production agent stack has at least three layers, not two.[^cloudflare-flue-platform] The **framework** layer gives project structure, conventions, integrations, CLI, and developer experience. The **harness** owns the agentic loop: tool calls, context management, observations, and progress toward the task. The **runtime/platform** owns compute, state, and storage primitives that the layers above cannot fake: durable execution, sandboxed dynamic code execution, durable filesystem/workspace state, dynamic workflows, bindings, credential isolation, and recovery. This distinction is useful because many teams buy or build a framework and then still need a platform contract for crash recovery, untrusted code, long waits, and filesystem state.

Project Think packages the same lesson as a practical **primitive -> failure mode -> runtime implication** frame: durable execution with fibers handles lost progress after eviction; sub-agents handle the failure mode where one agent holds the whole context; persistent sessions handle client disconnects and movement across surfaces; sandboxed code execution handles untrusted generated code; the execution ladder helps choose between a foreground run, background run, workflow, and fiber; self-authored extensions are useful only when the runtime preserves a capability boundary, review evidence, and a rollback path.[^cloudflare-project-think] So this is not just another vendor example. It is a useful checklist for the chapter: when a primitive is named, the adjacent failure mode and runtime obligation should be named too.

A minimal requirements table looks like this:

| Production requirement | Runtime primitive |
| --- | --- |
| Run survives crash or deploy | durable run record, checkpoint boundary, resume cursor |
| Human waits for hours or days | explicit wait state, approval/refusal record, timeout policy |
| Tool or workflow step is retried | idempotency key, lease/retry policy, duplicate-write guard |
| Agent resumes after external input | resume event, expected event schema, stale-event handling |
| Work crosses tenants or workspaces | tenant/principal context, scoped stores, policy decision trace |
| Operator investigates behavior | trace span ids, evidence refs, exported session/run record |
| Runtime exposes tools and subagents | capability catalog, sandbox profile, MCP/A2A boundary contract |

The short version: the prompt/tool/skill layer defines **what the agent can do**, and the runtime layer defines **how that execution stays governable, resumable, and investigable**. Without that boundary, teams often call the whole thing an “agent harness” and only later discover that crash recovery, multi-tenancy, approval sleep/resume, and observability live in separate places with no shared contract.

AWS AgentCore and GitHub security validation for third-party coding agents are useful recent production references for that same contract.[^aws-agentcore-agentops][^aws-agentcore-coding-agents][^github-third-party-coding-agent-validation] AgentCore AgentOps makes traces, latency, token/cost metrics, session history, PII redaction, and governance signals visible; the coding-agent hosting example adds isolated session, persistent workspace, scoped credentials, and the ability to close the laptop while the agent continues inside a managed environment; GitHub validation shows that agent-generated code should pass platform-owned CodeQL, dependency risk, and secret scanning gates before the result is treated as ready for review.

The portable production runtime contract is therefore: **isolated session → durable workspace → scoped credentials → egress/tool boundary → trace and cost ledger → PII redaction → platform security validation → human review artifact**. For the reference runtime, this is not a requirement to use AWS or GitHub. It is a checklist: the runtime should know where the workspace lives, which credentials were available, which network/tool boundaries applied, how much the run cost, which sensitive fields were redacted, which security gates checked the staged output, and which artifact a human later reviews.

Cloudflare's vulnerability harness adds a useful applied example to this boundary.[^cloudflare-vulnerability-harness] Their security-audit skill did not become one large agent; it became a pipeline with Recon, Hunt, Validate, Gapfill, Dedup, Trace, Feedback, and Report stages. The important runtime detail is that every stage writes state into a SQLite database keyed by `run_id`, `repo`, and `stage`, so a stage can resume, retry, or be pulled into a later run without losing already discovered findings. That is a runtime boundary: the model performs narrow work, while the harness owns durable state, queues, coverage cells, validation status, and evidence.

In a vendor-neutral contract, that harness should carry:

- `harness_run_id`, `target_repo`, `stage_name`, `stage_attempt`, `stage_status`;
- `coverage_cell` for an area × attack-class pair or another reviewable slice;
- `finding_candidate_id`, `validator_verdict`, `dedup_key`, `judgment_status`;
- `model_provider` and `model_version` as execution variables, not the architecture's foundation;
- `shallow_run_signal` when a stage finishes suspiciously fast without findings, sibling tasks, or gapfill work;
- `fix_gate_status`, including targeted before/after tests and clean fail→pass evidence;
- `human_review_ref` for any change that could reach production.

That makes the harness model-agnostic and failure-aware. If a frontier model changes, a provider changes caching, or a transient API error arrives as text inside `200 OK`, durable orchestration still has to classify, retry, and preserve evidence instead of treating empty output as success.

Anthropic's workflow taxonomy sharpens this further because different orchestration patterns create different checkpoint needs.[^anthropic] A `prompt chaining` path may checkpoint between fixed stages, `routing` may checkpoint only at classification and handoff boundaries, `parallelization` needs join-state visibility, and `orchestrator-workers` needs parent/worker coordination state that survives partial completion.

LangGraph persistence makes the same point at checkpoint granularity: durable state is organized by thread, checkpoints are saved at super-step boundaries, and successful node writes inside a failed super-step can be kept as pending writes instead of being recomputed on resume.[^langgraph-persistence] The architectural lesson is that “checkpointing” is not one boolean. A runtime should name the cursor that resumes work, the boundary at which replay is allowed, and the partial writes that must not be duplicated after failure.

Google Agent Executor expresses a similar layer as a distributed runtime primitive: an agent execution graph should survive long-running jobs, disconnections, trajectory branching, and restore from an event log instead of depending on one live process.[^google-agent-executor] For the baseline runtime, that becomes a vendor-neutral requirement: if a user closes the client, an operator starts an alternate branch, or the system restores agent state after failure, the runtime needs a session event log, snapshot/restore boundary, single-writer or session-consistency rule, and explicit ownership over the active execution branch.

Their later harness work adds one more practical runtime lesson: long-running application work often needs an explicit distinction between **compaction** and **context reset**.[^anthropic-harness] Compaction keeps the same agent alive on a shortened history, which preserves continuity but may keep the same context anxiety and drift. A reset starts a fresh agent and depends on a structured handoff artifact that carries state, next steps, and evaluation context forward. That is not just a prompt trick. It is runtime architecture, because once resets are part of the harness, the platform must decide what state is durable enough to survive them and what review artifact the next agent inherits.

The handoff artifact still does not become an authorization artifact. The runtime should persist a [Context Continuity Envelope](../../appendix/continuity-envelope-schema.en.md), validate its digest and lineage, reconcile any unknown external effect, reload identity and contract versions from their systems of record, and then authorize the next capability call again. A successful rehydration means only that continuity was reconstructed; it never means that the summary approved an action.

A baseline implementation can make the boundary explicit with this sequence:

1. Before compaction, stop at a safe boundary, flush the append-only session log, checkpoint the workflow cursor, and persist unresolved obligations.
2. Persist control fields without summarization, create the derived summary, bind it to its source event range with `summary_sha256`, and emit `context_compaction`.
3. After reset, load the envelope from governed storage and validate schema, digest, event lineage, tenant, principal, delegated scope, policy, capability, approval, budget, sandbox, and checkpoint state.
4. If an external effect is unknown, return `blocked_on_reconciliation`; if any binding changed, emit `continuity_validation_failed` and stop.
5. Only after validation and any required reconciliation succeed, rebuild the disposable context view, emit `context_rehydration`, and run policy plus authorization again before the next capability call.

So bounded autonomy is not only a policy issue. It is also a runtime-state design issue: every allowed execution pattern implies its own pause, resume, reset, and completion semantics.

If the runtime has no explicit shape for those cases, long-running work usually leaks into ad hoc retries, duplicated requests, and hidden state transitions.

### 8.2. Sandbox Session State Is Runtime State Too

OpenAI Agents SDK Sandbox Agents make a useful distinction that belongs in baseline runtime design: `Manifest` describes the fresh workspace contract, while a concrete run may receive a live sandbox session, serialized `session_state`, or start from a `snapshot`.[^openai-sandbox-agents]

OpenAI's Responses API computer-environment writeup describes the same layer as an agent computer: the model proposes an action, the platform executes a shell command in an isolated container, returns a streamed observation, and the next model turn decides whether to continue.[^openai-computer-environment] The important architectural boundary is that model decision and command execution are not the same thing. The model proposes; the runtime owns isolation, filesystem/artifact persistence, optional structured storage, restricted network access, timeout/cancellation, and observable tool output.

A stronger version of that contract also records each **bounded tool-output cap** and each **concurrent tool session**. Output caps are not cosmetic truncation; they are context-budget controls that preserve useful evidence without letting raw logs flood the next turn. Concurrent sessions are not just faster execution; they need separate session ids, timeout/cancellation state, output envelopes, and failure attribution so one shell, browser, or data-processing branch cannot silently overwrite another branch's observation.

For a reference runtime, that means sandbox state should not disappear inside a tool adapter. A minimally useful model should track, next to `run_id` and `trace_id`, at least:

- `sandbox_session_id`;
- `sandbox_manifest_version`;
- `sandbox_permissions_profile`;
- `snapshot_id` when the run starts from a saved workspace;
- materialized workspace entries, or a link to a reviewed manifest;
- whether this sandbox can be resumed, snapshotted, or must be recreated.

Then long-running work over files, shell, and memory does not become an opaque directory on disk. It becomes part of the same runtime-control layer that already holds approvals, background runs, capability sessions, and [trace evidence](../../appendix/trace-schema.en.md).

### 8.3. Stateful Named Agent Instance as a Runtime Topology

Cloudflare Agents SDK shows another useful baseline pattern: an agent can be not only a transient execution loop, but a **named durable runtime object**. In that model, each agent instance runs on a Durable Object with its own durable SQL/key-value state, WebSocket connections, scheduled tasks, the ability to wake on an event, and the ability to hibernate when idle.[^cloudflare-agents]

Cloudflare's newer wording makes the boundary even clearer: an agent is a **durable identity, not an always-on process**.[^cloudflare-long-running-agents] Architecturally, that matters more than the specific platform. `agent_instance_id` should outlive a process, deploy, hibernation, and connection break; the active process is only a temporary executor for the next event. So the runtime contract should show what persists as named-instance state and what disappears on eviction.

| Boundary | Survives restart/hibernation | Does not survive restart/hibernation |
| --- | --- | --- |
| Agent state | `this.state`, durable SQL/key-value tables, schema-migrated instance metadata | class fields, local variables, unstored closures |
| Work over time | scheduled tasks, queued/background work, fiber checkpoints, durable workflow steps | `setTimeout`, `setInterval`, open fetches, promise chains |
| Sessions and UI | connection state, persisted conversation/history refs, resumable stream cursor | open WebSocket frame, browser tab process, in-memory callback |
| Side effects | idempotency key, approval record, durable execution log, evidence refs | "already called" boolean in memory, partial tool call without a ledger |

The practical invariant is: anything that may create an external side effect after human waiting, failure, or restart needs a durable log, idempotency key, and replay boundary. Otherwise "resume after pause" becomes re-execution with a hope that local memory is still alive.

This is worth importing into the book as an architectural shape, not as “use Cloudflare.” When an agent is bound to the stable name of a real thing — a customer case, project, device, tenant workspace, room, thread, or research dossier — the runtime should explicitly separate:

- `agent_instance_id`, which outlives a single run;
- `run_id`, which describes one execution;
- `session_id`, which describes a user-facing or transport session;
- durable agent state, which survives disconnects, deploys, hibernation, and background wake-ups;
- external knowledge stores, which are not the private mutable state of one instance.

This pattern is especially useful for chat, voice, workflow, and monitoring agents where users expect continuity rather than stateless request/response behavior. It also adds risks the baseline runtime should make visible: tenant isolation for named instances, leakage across WebSocket sessions, replay/resume after hibernation, scheduled side effects without an active user, and durable-state migrations when the agent version changes.

So the reference runtime does not need to implement Durable Objects, but it does need an abstraction such as `AgentInstanceStore` and `SchedulerBoundary`: a place where operators can see which named instance owns state, which runs changed it, which scheduled tasks may wake it, and which traces prove safe resume.

The scheduling side matters in particular: Cloudflare shows delayed, scheduled, cron, and interval tasks that survive restarts, persist in SQLite, and wake the agent through Durable Object alarms.[^cloudflare-schedule] The architectural takeaway for the book is that a schedule should not remain an invisible callback. It should be represented as a durable control record with an owner instance, payload schema, idempotency key, overlap policy, next fire time, and trace linkage.

GitHub Copilot cloud agent automations show the same boundary in a repo-native form: unattended work can start from repository events or scheduled triggers, not only from a manual request.[^github-copilot-automations] If such an automation starts Copilot cloud agent, the runtime should record `automation_id`, trigger source, owner, branch policy, allowed events, approval boundary, and evidence refs. Copilot code review support for `AGENTS.md` adds a neighboring contract: repo instructions become input to the review agent and should be versioned as a policy-bearing artifact, not as a verbal convention.[^github-copilot-agents-md] BYOK in the Copilot app extends the provider-neutral control plane to provider routing: keys, scopes, and provider choice should live in a governed access model, not a hidden per-user setting.[^github-copilot-byok]

The real-time side adds one more boundary: connection state is not agent state. In Cloudflare Agents WebSocket model, a connection has its own `id`, `uri`, per-connection `state`, tags, lifecycle hooks, and the option to disable protocol messages such as identity/state/MCP for a specific connection.[^cloudflare-websockets] For a baseline runtime, that means broadcast, presence, approval UI, and streaming updates should pass through connection-scoped authorization and traceable fan-out, not directly expose the whole durable state of the agent.

The vendor-neutral pattern is a **durable agent actor**: stable identity, local durable state, resumable sessions, scheduled wake-ups, and traceable handoff to governed stores. Its local state may hold instance-scoped facts such as open workflow cursor, UI/session preferences, per-instance queue position, last processed event, schedule metadata, and small cached views that can be rebuilt. It should not silently become the system of record for user profile memory, tenant knowledge, secrets, policy, audit logs, or cross-instance facts. Those belong in governed stores with provenance, retention, export, and access-control contracts.

The anti-pattern is hidden durable memory: a named agent accumulates private state, later retrieves or acts on it as if it were validated knowledge, and gives operators no export, audit trail, schema migration path, or deletion story. Durable actor state is useful only when its ownership and lifecycle are explicit.

### 8.4. Recoverable Internal Tasks / Fibers

Cloudflare adds one more useful boundary to this topology: durable work can live not only as an external workflow, but also as a **recoverable internal task** inside the agent itself.[^cloudflare-fibers] In its API, `runFiber()` registers work in SQLite, keeps the Durable Object alive while it runs, lets the agent checkpoint intermediate state with `stash()`, and calls `onFiberRecovered()` on the next activation if the object was evicted mid-task. `startFiber()` fits background work that must be durably accepted, deduplicated through an idempotency key, inspected or canceled later, and not keep the original request open.

The vendor-neutral takeaway is that a baseline runtime should distinguish at least four levels of long work:

- **synchronous run:** short work in the current request/response loop;
- **background/resumable run:** a user-visible run that can be backgrounded, observed, and resumed;
- **durable workflow:** a multi-step orchestration spine with retries, waits, approvals, and external events;
- **internal recoverable fiber:** part of the agent's own loop that survives eviction/restart through a checkpoint and recovery hook.

A minimal contract for the last level includes `fiber_id`, `fiber_name`, `fiber_status`, `fiber_idempotency_key`, `fiber_checkpoint_ref` or `stash_snapshot`, `recovery_handler`, `cancellation_status`, `last_safe_step`, `owner_agent_instance_id`, and `evidence_refs`. That contract must not become hidden durable memory or a system of record. The checkpoint exists to continue an expensive task safely, not to quietly store profile facts, tenant knowledge, secrets, or policy state.

In the [reference package](../../appendix/reference-package.en.md), durable named-agent topology remains a contract surface, not a full Durable Object/fiber implementation: session/run exports leave room for `agent_instance_id`, `durable_state_version`, `scheduled_wakeup_id`, and `resumable_stream_id`, and a production adapter can extend them with fiber evidence such as `fiber_id`, `fiber_status`, `fiber_checkpoint_ref`, and `last_safe_step`. For the small runtime these fields are usually empty; the book shows the boundary of a durable named instance and recoverable internal task without turning the package into a vendor-specific SDK.

The Cloudflare Agents SDK changelog adds a more operational layer to that boundary: a **detached sub-agent run** through `runAgentTool`, **durable milestones**, a single `runTurn` entry point, and recovery after `deploy/eviction/reconnect`.[^cloudflare-agents-background-subagents] This names a practical failure class: deploy, Durable Object eviction, connection churn, or a hung stream happens during an agent run. The runtime should not abandon the work as `interrupted` if it has a durable backbone, `continuation_id`, `last_durable_checkpoint`, idempotency key, and bounded reconcile path.

Cloudflare's separate changelog about outbound connections shows that even a "live" stream is a runtime contract, not just a network detail.[^cloudflare-outbound-connections] A Durable Object now stays active while it has an active outbound connection or outbound WebSocket, but only within the stated keepalive window. Architecturally, a long-running LLM stream needs `stream_id`, `connection_keepalive_deadline`, `last_emitted_offset`, `resume_strategy`, and a fallback checkpoint. Otherwise the team may treat the stream as durable even though the usual eviction model returns after the limit or connection close.

Delegated tools add a neighboring rule. When a sub-agent receives **client-provided tools** through `clientTools` and `onClientToolCall`, that is not only callback convenience.[^cloudflare-agents-recovery] The parent runtime should store the allowlist for those tools, owner/caller identity, argument schema, expiration, and trace evidence. Otherwise the delegated sub-agent receives implicit capability leaks. The recovery path should also repair unfinished tool calls: the stream stall watchdog and interrupted tool-call repair should return the run to the last durable checkpoint, not repeat a side effect from transcript memory.

### 8.5. Agent shell + durable workflow spine

The next useful Cloudflare pattern is to avoid putting all long work into one agent event loop. The agent can be the **stateful interaction boundary**: it owns instance identity, WebSocket/HTTP session, local state, user callbacks, and the current conversation view. The workflow then becomes the **durable execution boundary**: it owns steps, retries, waiting for external events, long approval gates, and recovery after failure.[^cloudflare-workflows]

<div class="diagram-card">
<p>A live agent and a durable workflow solve different problems</p>

``` mermaid
flowchart LR
    S["Session / state store"] --> A["Agent runtime shell"]
    A --> W["Durable workflow spine"]
    W --> E["Tool / external event / approval step"]
    W --> L["Audit + evidence log"]
    A --> U["User-facing stream / WebSocket"]
    E --> L
```

</div>

In the reference shape, the agent shell may report progress, accept new messages, and show approval UI, but the durable workflow should own what cannot be lost: step id, idempotency key, retry/timeout policy, external-event wait, approval decision, and evidence refs. Then agent restart or WebSocket disconnect does not turn long work into a half-remembered user conversation.

In Cloudflare's HITL API, that appears as `waitForApproval()` inside the workflow: the wait can last **months or longer** without a live agent process, while the agent shell exposes `approveWorkflow()` and `rejectWorkflow()` for the human decision. For this book, the important part is the boundary, not the API name: pending approval, timeout, escalation, and audit trail must be durable execution state.

Cloudflare Agents SDK v0.16.1 shows the same contract on the Codemode runtime side: the model gets one `codemode` tool, writes code against typed globals, and the runtime keeps a durable execution log.[^cloudflare-agents-sdk-0161] When code reaches an approval-gated action, execution pauses and returns a pending approval; after approval, completed calls replay from the durable log, the approved action runs, and the same code continues. In vendor-neutral terms, that is a useful minimal contract for an approval gate:

- `approval_id`, `approval_status`, `requested_action`, `risk_tier`, `approver_ref`;
- `execution_log_ref` for already completed deterministic/tool calls;
- `replay_policy`, separating safe replay from repeated side effects;
- `idempotency_key` for the post-approval action;
- `resume_cursor`, `timeout_policy`, and `evidence_refs`.

That gate belongs in the durable workflow or runtime log, not in a UI callback. The UI may show the approval button, but the execution system must own pending state, replay, and continuation after the decision.

Dynamic Workflows sharpen the same contract: `run(event, step)` becomes a durable plan where `step.do()` executes a durable step, `step.sleep()` or `step.sleepUntil()` makes waiting explicit, and `step.waitForEvent()` moves external signals or human approval into the execution model itself.[^cloudflare-dynamic-workflows] For an agent runtime, this is the boundary: the agent may choose or generate the plan, but the platform must own replay, retry, sleep/wait state, already completed step results, and which events can safely resume work.

Saga rollbacks in Cloudflare Workflows add the failure side of the same boundary: compensation should sit beside the forward step as metadata, not in a distant `catch` block.[^cloudflare-workflow-rollbacks] When a workflow fails terminally, the runtime can find eligible `step.do()` calls with rollback handlers, pass each handler the persisted `output` or `undefined`, run compensation in reverse `step-start` order, and after a restart rebuild the needed handlers through replay without repeating completed side effects. For agent workflows, that is a useful contract: if a step reserves money, inventory, an account, a deployment slot, or an external quota, `compensation_ref` and `rollback_idempotency_key` should be part of the step record from the start.

In a vendor-neutral contract, each durable step therefore needs `step_id`, `step_type`, `idempotency_key`, `input_schema`, `output_ref`, `retry_policy`, `wait_event_type`, `approval_ref`, `compensation_ref`, `rollback_idempotency_key`, `rollback_retry_policy`, `timeout_policy`, and `evidence_refs`. Otherwise "workflow" becomes a long function hoping retry is enough, not a governed execution spine.

### 8.6. Temporary Deploy Identity and Human Handoff

Cloudflare Temporary Accounts add one more practical pattern to durable workflows: an agent can receive a **temporary account** for deployment, and a human can later claim the result into a normal account.[^cloudflare-temporary-accounts] That is not just developer convenience. Architecturally, it is a lease model for agent deployment: the agent receives a bounded identity, executes a deployment step, leaves evidence, and ownership then transfers to a human or team.

In a vendor-neutral runtime contract, that capability should be explicit:

- `temporary_principal_id` and `principal_issuer`;
- `lease_ttl`, `scope`, `allowed_deploy_targets`, and `egress_policy`;
- `deployment_artifact_ref`, `deployment_url`, `rollback_ref`, and `evidence_refs`;
- `claim_status`, `claimed_by`, `claim_deadline`, and `unclaimed_cleanup_policy`;
- `approval_ref` for the transition from temporary deploy to owned production surface.

The core rule is that a temporary account must not become a new standing service user. It is a work lease for one agent step, with short lifetime, narrow scope, trace linkage, and a clear final state: claimed, expired, revoked, or cleaned up. If claim/handoff is not modeled, agent deployment can quietly create a live resource without an owner outside the normal lifecycle registry.

## 9. Stateful Tool Sessions Belong in the Baseline Too

Once the execution layer includes stateful MCP-style capabilities, the baseline runtime needs one more explicit boundary: **run state is not the same thing as capability session state**.[^aws-stateful-mcp]

That distinction matters because a single user-visible run may now involve:

- one runtime `run_id`;
- one or more MCP `session_id` values for external capabilities;
- progress notifications emitted before the final answer;
- elicitation or intermediate prompts that pause the run until more input arrives;
- re-initialization if the capability session expires before the run is complete.

If those states are collapsed into one opaque object, operators cannot explain what resumed, what expired, and what has to be retried.

### 9.1. The Runtime Should Treat Capability Session Lifecycle as First-Class State

A minimally mature runtime should usually track at least:

- `run_id`
- `trace_id`
- `capability_session_id`
- `capability_session_status`
- `expires_at`
- `resume_token` or equivalent continuation handle
- `approval_state` when a stateful tool flow pauses on approval

That does not mean every tool needs a heavyweight session model. It means the runtime should have a place to represent one when the protocol requires it.

### 9.2. Progress and Elicitation Should Feed the Same Resume Model

Another useful implication from stateful MCP guidance is that progress events and elicitation requests should not be treated as exotic side channels. They should enter the same runtime control model as approvals and background resumption.

That becomes even more important once the runtime supports multiple orchestration patterns. Progress from a `parallelization` branch, a worker delegated by `orchestrator-workers`, or a gated `prompt chaining` stage should not disappear into pattern-specific adapters. It should feed one shared control surface for status, resumption, expiry, and operator visibility.

In practice, that means the baseline runtime benefits from one shared set of rules for:

- `in_progress` work that is still alive inside a capability session;
- `waiting_for_input` or `waiting_for_approval` pauses;
- `resumable` work that can continue with the same capability session;
- `reinitialize_required` work where the capability session expired and must be rebuilt before continuing.

Without those distinctions, session expiry tends to look like a random failure even when it is actually a normal lifecycle event.

## 10. What Is Worth Building Into the Baseline From the Start

Some things are tempting to "add later", but in practice it is better to include them from day one:

- a `trace_id` on every run;
- tenant/principal context;
- policy decision hooks;
- a capability registry instead of direct calls;
- structured telemetry;
- a basic background task hook;
- a visible run status model such as `queued / in_progress / completed / failed / canceled`;
- a way to poll, resume, or cancel long-running work without inventing a second hidden runtime.

If those are absent from the baseline, the system usually reaches them later through a painful retrofit.

## 11. A Minimal Skeleton for Background and Resumable Work

Even a baseline runtime should have a simple way to represent work that outlives the first request.

```python
from dataclasses import dataclass


@dataclass
class RunHandle:
    run_id: str
    status: str


def start_run(request: RunRequest) -> RunHandle:
    run_id = create_run_record(request)
    enqueue_run(run_id)
    return RunHandle(run_id=run_id, status="queued")


def continue_run(run_id: str):
    run = load_run(run_id)
    if run.status in {"canceled", "completed", "failed"}:
        return run

    update_status(run_id, "in_progress")
    result = execute_run_steps(run)
    update_status(run_id, result.status)
    return result
```

The point is not complexity. The point is to make long-lived work explicit enough that operators can observe it, clients can poll it, and the runtime can resume or cancel it without guesswork.

## 12. What You Do Not Need to Overcomplicate in the First Reference Version

At the start, you do not need all of this immediately:

- a complex planner with many modes;
- a multi-stage memory compaction pipeline;
- sophisticated model routing;
- a full self-healing loop;
- a dozen golden paths.

The value of a reference runtime is not maximal power. It is clarity of form. A small clean implementation is better than a universal machine nobody understands.

### 12.1. Runtime as a split between session, harness, and hands

Another way to test the maturity of the reference runtime is to ask whether its parts can be replaced independently. In the managed-agent shape, session, harness, and hands are separated as interfaces rather than treated as details of one process.[^anthropic-managed-agents] Anthropic frames this as decoupling brain from hands: the model/harness may fail or change, the sandbox/tool executor may be recreated, and the session log remains an external durable record from which a new harness can wake with `wake(sessionId)`.

For the reference package, that means:

- session remains an append-only evidence log and survives executor failure;
- harness can change as a control loop without migrating the user's workspace;
- sandbox/tools act as contained hands with explicit network, filesystem, secrets, and snapshot profiles;
- debugging happens through trace, lifecycle summary, and sandbox profile, not through direct access to an environment containing user data.

This fits the earlier sections of the chapter: background execution, resumable runs, and capability sessions stop being “a long request inside a container” and become a governed binding between session state, control loop, and contained execution surface. The maturity test is simple: can the platform replace the model, harness, sandbox, or a specific hand capability without losing session history, audit trail, or the operator's ability to explain what happened?

The practical contract is stricter than “keep the history.” **The session is not the context window**: it is an external log and state API from which the harness assembles the next prompt, but it does not need to fit entirely inside the model. A minimum runtime interface looks like this:

- session API: `wake(sessionId)`, `getEvents()`, and `emitEvent(id, event)` for reading the durable log and writing new decisions;
- hands API: `execute(name, input)` for invoking a concrete capability and `provision({resources})` for issuing sandbox/tool resources under a policy profile;
- failure contract: sandbox, tool executor, policy proxy, or resource-provisioning failure should return to the harness as an ordinary `tool-call error`, not as a hidden process crash;
- secret boundary: tokens are never reachable from the sandbox; the sandbox receives a brokered capability, not raw credentials.

Then the brain can make a mistake, the hands can fail, the session can survive both events, and replay can see a specific boundary: resource exhaustion, policy denial, sandbox startup failure, or a managed tool error. That makes the managed-agent split not only scalable, but investigable.


## 13. Example Runtime Configuration

Here is an example config that defines the runtime shape without hardcoding every decision:

```yaml
runtime:
  max_tool_hops: 3
  require_trace_id: true
  enable_background_updates: true
  default_model: gpt-5.4
  policy:
    precheck_required: true
  telemetry:
    emit_structured_events: true
  execution:
    gateway_required: true
  background:
    enabled: true
    resumable_runs: true
    allow_cancel: true
  capability_sessions:
    track_session_ids: true
    emit_progress_events: true
    support_reinit_on_expiry: true
```

This is useful because it keeps the runtime contract explicit and portable between environments.

## 14. Common Mistakes

Very typical problems:

- orchestration and adapters are glued together;
- policy checks are not called on every required path;
- memory is attached as a random helper;
- tool calls bypass catalog/gateway;
- background updates are missing;
- telemetry was added as an afterthought;
- long-running work is hidden behind retries instead of being modeled explicitly;
- background execution exists, but operators cannot poll, resume, or cancel it cleanly.

So the system may "work", but the runtime shape is already blocking growth.

## 15. A Fast Maturity Test for the Baseline Runtime

A team should not think it has a reference runtime only because it has a working agent, a few modules, and successful demos.

A stronger bar is this:

- orchestration, policy, memory, execution, and telemetry are visibly separate layers;
- the run context carries identity and control metadata from the start;
- capability execution flows through contracts rather than direct adapter calls;
- tracing and background hooks exist in the base path rather than as retrofits;
- long-running work has an explicit status and continuation model rather than hidden retries;
- one run can be explained as a stable skeleton, not as scattered local logic.

If most of those conditions are missing, the team may have an implementation, but it still does not have a real baseline runtime blueprint.

## 16. What to Do Right Away

Start with this short list and mark every "no" explicitly:

- Are orchestration, policy, memory, execution, and telemetry visible as separate layers?
- Is there a single run context with tenant/principal metadata?
- Is there a capability registry instead of direct calls?
- Are tracing hooks built into the base path?
- Is there a safe point for background updates?
- Can long-running work be queued, observed, resumed, and canceled explicitly?
- Can you explain one run flow without reading ten files at once?

If the answer is "no" several times in a row, you do not have a reference runtime yet. You just have an early model integration in a product.

## 17. What to Do Next

First make the runtime shape explicit, then add the policy layer and capability contracts on top of it.

The next logical step in Part VII is to add an explicit policy layer and capability catalog on top of this blueprint, so the reference implementation becomes close to an operational skeleton.

- [Chapter 15. Golden Paths, Shared Gateways, and Anti-Zoo Patterns](../part-vi/chapter-15.en.md)
- [Chapter 17. Policy Layer and Capability Catalog](chapter-17.en.md)
- [Part VII. Reference Implementation](index.en.md)
- [Sources](../../appendix/sources.en.md)

[^anthropic]: Anthropic, [Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents).

[^aws-stateful-mcp]: [AWS, Introducing stateful MCP client capabilities on Amazon Bedrock AgentCore Runtime](https://aws.amazon.com/blogs/machine-learning/introducing-stateful-mcp-client-capabilities-on-amazon-bedrock-agentcore-runtime/)

[^aws-agentcore-agentops]: AWS, [AgentOps: Operationalize agentic AI at scale with Amazon Bedrock AgentCore](https://aws.amazon.com/blogs/machine-learning/agentops-operationalize-agentic-ai-at-scale-with-amazon-bedrock-agentcore/)

[^aws-agentcore-coding-agents]: AWS, [It’s safe to close your laptop now: Hosting coding agents on Amazon Bedrock AgentCore](https://aws.amazon.com/blogs/machine-learning/its-safe-to-close-your-laptop-now-hosting-coding-agents-on-amazon-bedrock-agentcore/)

[^github-third-party-coding-agent-validation]: GitHub Changelog, [Security validation for third-party coding agents](https://github.blog/changelog/2026-06-09-security-validation-for-third-party-coding-agents/)

[^openai-background]: [OpenAI, Background mode](https://developers.openai.com/api/docs/guides/background)

[^openai-agents-transforming-work]: OpenAI, [How agents are transforming work](https://openai.com/index/how-agents-are-transforming-work/)

[^openai-codex-maxxing]: OpenAI, [Codex-maxxing for long-running work](https://openai.com/index/codex-maxxing-long-running-work/)

[^langgraph-persistence]: [LangGraph, Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

[^google-agent-executor]: Google, [Introducing Agent Executor: a new runtime for AI agents](https://developers.googleblog.com/en/introducing-agent-executor-a-new-runtime-for-ai-agents/).

[^langchain-production-runtime]: LangChain, [The Runtime Behind Production Deep Agents](https://www.langchain.com/blog/runtime-behind-production-deep-agents).

[^anthropic-harness]: Anthropic, [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents).

[^anthropic-managed-agents]: Anthropic, [Scaling Managed Agents: Decoupling the brain from the hands](https://www.anthropic.com/engineering/managed-agents).

[^cloudflare-vulnerability-harness]: Cloudflare Blog, [Build your own vulnerability harness](https://blog.cloudflare.com/build-your-own-vulnerability-harness/).

[^cloudflare-flue-platform]: Cloudflare Blog, [Bringing more agent harnesses and frameworks to Cloudflare, starting with Flue](https://blog.cloudflare.com/agents-platform-flue-sdk/).

[^cloudflare-project-think]: Cloudflare Blog, [Project Think: building the next generation of AI agents on Cloudflare](https://blog.cloudflare.com/project-think/).

[^cloudflare-websockets]: [Cloudflare Agents SDK, WebSockets](https://developers.cloudflare.com/agents/api-reference/websockets/)

[^cloudflare-fibers]: [Cloudflare Agents SDK, Durable execution with fibers](https://developers.cloudflare.com/agents/runtime/execution/durable-execution/)

[^cloudflare-outbound-connections]: Cloudflare Changelog, [Outbound connections keep Durable Objects alive](https://developers.cloudflare.com/changelog/post/2026-06-19-outbound-connections-keep-dos-alive/)

[^cloudflare-workflows]: [Cloudflare Agents SDK, Workflows](https://developers.cloudflare.com/agents/concepts/workflows/)

[^cloudflare-dynamic-workflows]: Cloudflare Blog, [Introducing Dynamic Workflows: durable execution that follows the user, not the other way around](https://blog.cloudflare.com/dynamic-workflows/)

[^cloudflare-workflow-rollbacks]: Cloudflare Blog, [How we built saga rollbacks for Cloudflare Workflows](https://blog.cloudflare.com/rollbacks-for-workflows/)

[^cloudflare-schedule]: [Cloudflare Agents SDK, Schedule tasks](https://developers.cloudflare.com/agents/api-reference/schedule-tasks/)

[^cloudflare-agents]: [Cloudflare, Build Agents on Cloudflare](https://developers.cloudflare.com/agents/)

[^cloudflare-long-running-agents]: [Cloudflare Agents SDK, Long-running agents](https://developers.cloudflare.com/agents/concepts/agentic-patterns/long-running-agents/)

[^cloudflare-agents-sdk-0161]: Cloudflare Changelog, [Agents SDK improves browser automation, code execution, and recovery](https://developers.cloudflare.com/changelog/post/2026-06-16-agents-sdk-v0161/)
[^cloudflare-agents-background-subagents]: Cloudflare Changelog, [Agents SDK adds background sub-agents and a unified turn entry point](https://developers.cloudflare.com/changelog/product-group/ai/)
[^cloudflare-agents-recovery]: Cloudflare Changelog, [Agents SDK improves browser automation, code execution, and recovery](https://developers.cloudflare.com/changelog/product-group/ai/)

[^cloudflare-temporary-accounts]: Cloudflare Changelog, [Temporary Accounts: From agent deployments to claimed accounts](https://developers.cloudflare.com/changelog/2026-06-22-temporary-accounts/)

[^github-copilot-automations]: GitHub Changelog, [Schedule and automate tasks with Copilot cloud agent](https://github.blog/changelog/2026-06-02-schedule-and-automate-tasks-with-copilot-cloud-agent/)

[^github-copilot-agents-md]: GitHub Changelog, [Copilot code review: AGENTS.md support and UI improvements](https://github.blog/changelog/2026-06-18-copilot-code-review-agents-md-support-and-ui-improvements/)

[^github-copilot-byok]: GitHub Changelog, [GitHub Copilot app support for BYOK](https://github.blog/changelog/2026-06-23-github-copilot-app-support-for-byok/)

[^openai-sandbox-agents]: [OpenAI Agents SDK, Sandbox Agents](https://openai.github.io/openai-agents-python/sandbox_agents/), [Sandbox Concepts](https://openai.github.io/openai-agents-python/sandbox/guide/), [Sandbox clients](https://openai.github.io/openai-agents-python/sandbox/clients/), and [Agent memory](https://openai.github.io/openai-agents-python/sandbox/memory/)

[^openai-computer-environment]: OpenAI, [From model to agent: Equipping the Responses API with a computer environment](https://openai.com/index/equip-responses-api-computer-environment/)
