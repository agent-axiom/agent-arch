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

That is the right mental model for a baseline runtime too. The runtime should already distinguish between:

- `synchronous runs` that can safely finish in one foreground pass;
- `background runs` that continue after the initial response;
- `resumable runs` that pause on approval, external input, or deferred work.

Anthropic's workflow taxonomy sharpens this further because different orchestration patterns create different checkpoint needs.[^anthropic] A `prompt chaining` path may checkpoint between fixed stages, `routing` may checkpoint only at classification and handoff boundaries, `parallelization` needs join-state visibility, and `orchestrator-workers` needs parent/worker coordination state that survives partial completion.

Their later harness work adds one more practical runtime lesson: long-running application work often needs an explicit distinction between **compaction** and **context reset**.[^anthropic-harness] Compaction keeps the same agent alive on a shortened history, which preserves continuity but may keep the same context anxiety and drift. A reset starts a fresh agent and depends on a structured handoff artifact that carries state, next steps, and evaluation context forward. That is not just a prompt trick. It is runtime architecture, because once resets are part of the harness, the platform must decide what state is durable enough to survive them and what review artifact the next agent inherits.

So bounded autonomy is not only a policy issue. It is also a runtime-state design issue: every allowed execution pattern implies its own pause, resume, reset, and completion semantics.

If the runtime has no explicit shape for those cases, long-running work usually leaks into ad hoc retries, duplicated requests, and hidden state transitions.

### 8.1. Sandbox Session State Is Runtime State Too

OpenAI Agents SDK Sandbox Agents make a useful distinction that belongs in baseline runtime design: `Manifest` describes the fresh workspace contract, while a concrete run may receive a live sandbox session, serialized `session_state`, or start from a `snapshot`.[^openai-sandbox-agents]

For a reference runtime, that means sandbox state should not disappear inside a tool adapter. A minimally useful model should track, next to `run_id` and `trace_id`, at least:

- `sandbox_session_id`;
- `sandbox_manifest_version`;
- `sandbox_permissions_profile`;
- `snapshot_id` when the run starts from a saved workspace;
- materialized workspace entries, or a link to a reviewed manifest;
- whether this sandbox can be resumed, snapshotted, or must be recreated.

Then long-running work over files, shell, and memory does not become an opaque directory on disk. It becomes part of the same runtime-control layer that already holds approvals, background runs, capability sessions, and trace evidence.

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

[^openai-background]: [OpenAI, Background mode](https://developers.openai.com/api/docs/guides/background)

[^anthropic-harness]: Anthropic, [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps).

[^openai-sandbox-agents]: [OpenAI Agents SDK, Sandbox Agents](https://openai.github.io/openai-agents-python/sandbox_agents/), [Sandbox Concepts](https://openai.github.io/openai-agents-python/sandbox/guide/), [Sandbox clients](https://openai.github.io/openai-agents-python/sandbox/clients/), and [Agent memory](https://openai.github.io/openai-agents-python/sandbox/memory/)
