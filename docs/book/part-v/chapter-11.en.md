# Chapter 11. Traces, Spans, and Structured Events

## 1. Why Ordinary Logs Are Almost Never Enough for an Agent System

When a system is simple, a set of application logs and a few metrics can be enough. But an agent system is almost always more complicated:

- one user request turns into a multi-step run;
- inside the run there is planning, retrieval, prompt assembly, tool calls, and policy gates;
- some steps go into the background;
- the failure may show up somewhere other than where it began.

If you look at all of that only through flat logs, you quickly lose cause and effect. You see noise, but not the run history.

That is why observability for agent systems should start with traces, not with the hope that someone will figure it out later using grep.

## 2. A Trace Is the Story of One Run, a Span Is a Meaningful Step Inside It

It helps to anchor a simple model:

- a `trace` describes the full path of a request or run;
- a `span` describes one meaningful step within that path;
- `structured events` add precise facts you should not hide in free-form text.

This is especially useful for agent systems, where one run may include:

- policy evaluation;
- retrieval;
- model inference;
- tool execution;
- approval wait;
- background memory update.

When that structure exists, the team stops looking at the system as a chaotic stream of calls and starts seeing it as a chain of observable decisions.

## 3. What Should Become Separate Spans

You do not need a span for every tiny detail. But one giant span for the whole run is almost useless too.

A good practical rule:

- one span for each orchestration step;
- one span for retrieval;
- one span for the model call;
- one span for each tool call;
- one span for a policy decision if it changes behavior;
- one span for human approval wait if it exists.

That keeps the trace readable while still showing where the time, money, and reliability actually went.

<div class="diagram-card">
<p>A mature agent run trace should show more than model latency. It should show the important control points.</p>

``` mermaid
flowchart LR
    A["User request"] --> B["Run trace"]
    B --> C["Policy span"]
    B --> D["Retrieval span"]
    B --> E["Model span"]
    B --> F["Tool span"]
    B --> G["Approval span"]
    B --> H["Memory update span"]
```

</div>

## 4. Structured Events Matter Where Plain Text Only Gets in the Way

A common mistake: useful operational facts are written as human-readable logs, and then they become impossible to analyze or investigate programmatically.

Structured events are especially useful for:

- policy decisions;
- tool outcomes;
- prompt assembly metadata;
- token usage;
- cost attribution;
- idempotency keys;
- tenant and principal context;
- memory writes.

An event should answer not "what should I write in a log line?" but "what will we need to analyze later as data?"

## 5. A Good Trace Model Shows the Control Plane, Not Only LLM Latency

If observability collapses into model response time only, the team gets a very distorted picture.

In practice a run often fails or degrades elsewhere:

- retrieval starts returning noise;
- the policy engine blocks too much;
- approval waits become long;
- a tool adapter degrades;
- background updates clog a queue;
- prompt assembly inflates context.

So a good trace model should cover the full control flow, not only the inference step.

## 6. The Minimum Set of Fields for Traces and Spans

To make the system genuinely investigation-friendly, it helps to have at least:

- `trace_id`
- `span_id`
- `parent_span_id`
- `run_id`
- `tenant_id`
- `principal_id`
- `agent_id` or workflow id
- `status`
- `duration_ms`
- `model_name` if there was a model call
- `tool_name` if there was a tool call
- `policy_decision_id` if there was a gate

Without that, observability quickly becomes beautiful but not very useful.

## 7. Example Structured Event for Tool Execution

Here is a simple template that shows the style of thinking:

```yaml
event_type: tool_execution
trace_id: trc_01HXYZ
span_id: spn_02ABC
run_id: run_9842
tenant_id: tenant_acme
tool_name: create_ticket
status: success
duration_ms: 842
idempotency_key: act_77f1
policy_decision_id: pol_441
side_effect: created
```

That event is much more useful than a line like "ticket tool ok".

## 8. A Simple Span Emission Example

The point here is not to replace a tracing SDK, but to show the principle: every important step should leave behind a structured trace.

```python
from dataclasses import dataclass
from time import monotonic


@dataclass
class SpanResult:
    name: str
    status: str
    duration_ms: int


def traced_step(name: str, fn):
    started = monotonic()
    try:
        fn()
        status = "success"
    except Exception:
        status = "failure"
        raise
    finally:
        duration_ms = int((monotonic() - started) * 1000)
        emit_span(SpanResult(name=name, status=status, duration_ms=duration_ms))


def emit_span(result: SpanResult) -> None:
    print({"span_name": result.name, "status": result.status, "duration_ms": result.duration_ms})
```

## 9. What You Especially Should Not Log As-Is

Observability should not turn into a data leak.

So traces and events need careful treatment of:

- full prompt bodies;
- raw retrieved documents;
- secrets and tokens;
- PII;
- sensitive tool payloads.

The practical rule is simple:

- log metadata and derived facts;
- log identifiers and hashes where useful;
- do not dump full sensitive payloads into generic telemetry pipelines without a very good reason.

## 10. What Usually Breaks in Agent Observability

These problems are very recognizable:

- the trace covers only the model call;
- tool calls are not tied to the original run;
- policy decisions are visible in code but not in telemetry;
- events exist, but without tenant/principal context;
- spans are too large or too noisy;
- event schema changes chaotically, and analytics break.

When that happens, the team goes back to guesswork and manual log reading.

## 11. Practical Checklist

If you want to quickly review your observability model, ask:

- Can you reconstruct the full path of one run from a single `trace_id`?
- Are there separate spans for retrieval, model calls, tool calls, and policy gates?
- Are idempotency keys and policy decision ids logged?
- Is tenant/principal context present in telemetry?
- Can you see where the run spent time and where cost increased?
- Are sensitive payloads kept out of traces?
- Is the structured event schema stable?

If the answer is "no" several times in a row, your observability is decorative, not operational.

## 12. What to Read Next

The next natural step is to define what a "healthy" agent system actually means. That means moving to SLO.

- [Chapter 10. Idempotency, Retries, Rate Limits, and Rollback Boundaries](../part-iv/chapter-10.md)
- [Part V. Reliability and Observability](index.en.md)
- [Sources](../../appendix/sources.md)
