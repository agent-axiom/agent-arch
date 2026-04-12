# Chapter 16. Baseline Runtime Blueprint

!!! info "How to read this chapter"
    It helps to keep one practical question in mind rather than an abstract runtime topic:

    - where the run loop for the same support agent should actually live;
    - how not to collapse policy, memory, execution, and telemetry into one handler;
    - how to build a skeleton that survives not only the demo, but the rollout that follows.

    If those answers are fuzzy, the system usually keeps working only until the first serious change or incident.

## 1. Why a Reference Runtime Matters If You Already Have an Architecture

The architecture chapters are useful because they give you language and a frame. But at some point almost everyone asks the same question: "Fine, but what should this look like as a system you can actually build?"

In the running support case, that is no longer theoretical. The agent can already check status, read memory, open a ticket through the gateway, and emit traces. But without an explicit runtime shape, those steps quickly spread across local handlers, ad hoc retries, and accidental integration bypasses.

That is where the reference runtime matters.

Its job is not to become the only possible implementation. Its job is to:

- fix the core modules in place;
- show the flow of one run;
- separate mandatory layers from optional enhancements;
- give the team a starting point without unnecessary magic.

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

## 8. What Is Worth Building Into the Baseline From the Start

Some things are tempting to "add later", but in practice it is better to include them from day one:

- a `trace_id` on every run;
- tenant/principal context;
- policy decision hooks;
- a capability registry instead of direct calls;
- structured telemetry;
- a basic background task hook.

If those are absent from the baseline, the system usually reaches them later through a painful retrofit.

## 9. What You Do Not Need to Overcomplicate in the First Reference Version

At the start, you do not need all of this immediately:

- a complex planner with many modes;
- a multi-stage memory compaction pipeline;
- sophisticated model routing;
- a full self-healing loop;
- a dozen golden paths.

The value of a reference runtime is not maximal power. It is clarity of form. A small clean implementation is better than a universal machine nobody understands.

## 10. Example Runtime Configuration

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
```

This is useful because it keeps the runtime contract explicit and portable between environments.

## 11. Common Mistakes

Very typical problems:

- orchestration and adapters are glued together;
- policy checks are not called on every required path;
- memory is attached as a random helper;
- tool calls bypass catalog/gateway;
- background updates are missing;
- telemetry was added as an afterthought.

So the system may "work", but the runtime shape is already blocking growth.

## 12. What to Do Right Away

Start with this short list and mark every "no" explicitly:

- Are orchestration, policy, memory, execution, and telemetry visible as separate layers?
- Is there a single run context with tenant/principal metadata?
- Is there a capability registry instead of direct calls?
- Are tracing hooks built into the base path?
- Is there a safe point for background updates?
- Can you explain one run flow without reading ten files at once?

If the answer is "no" several times in a row, you do not have a reference runtime yet. You just have an early model integration in a product.

## 13. What to Do Next

First make the runtime shape explicit, then add the policy layer and capability contracts on top of it.

The next logical step in Part VII is to add an explicit policy layer and capability catalog on top of this blueprint, so the reference implementation becomes close to an operational skeleton.

- [Chapter 15. Golden Paths, Shared Gateways, and Anti-Zoo Patterns](../part-vi/chapter-15.en.md)
- [Chapter 17. Policy Layer and Capability Catalog](chapter-17.en.md)
- [Part VII. Reference Implementation](index.en.md)
- [Sources](../../appendix/sources.en.md)
