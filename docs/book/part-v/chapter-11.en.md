# Chapter 11. Traces, Spans, and Structured Events

## 1. Start Not with Logs, but with One Incident Investigation

Continue with the same support case.

The user writes:

> I have been waiting three days for access activation. Check the status, and create an urgent ticket if the request is stuck.

The agent replies that the ticket was created. Ten minutes later, an operator sees **two** identical tickets in the helpdesk for the same issue.

Now the team has a very concrete question:

- did the model repeat the call itself;
- did a retry fire after a timeout;
- did the tool return an ambiguous result;
- did the side effect happen before the runtime saw the error;
- or were the tickets created by two different runs.

If all you have is application logs and a few metrics, the answer is usually slow and painful to recover.

That is why observability for agent systems should be built not around "logs in general," but around the ability to reconstruct the history of one run.

In this chapter, that means something deliberately limited: tracing is the capture layer for one run, not yet the estate-wide substrate for detection, correlation, and operations across many runs.

The role of tracing in this book is narrower than the whole observability layer. Tracing captures the raw history of execution. Later chapters will show how observability turns that history into an evidence substrate, how evals turn it into judgments, and how assurance or governance consume those outputs.

If you want to see how tracing connects to policy, approvals, evals, incidents, and rollout judgment as one operating record, use the dedicated [Evidence Spine](evidence-spine.en.md) page as the bridge.

## 2. Why Ordinary Logs Are Almost Never Enough

When a system is simple, flat logs and a few metrics can be enough. But an agent system is almost always more complicated:

- one user request turns into a multi-step run;
- inside the run there is planning, retrieval, prompt assembly, tool calls, and policy gates;
- some steps go into the background;
- the failure may show up somewhere other than where it began.

If you look at all of that only through flat logs, you quickly lose cause and effect. You see noise, but not the execution history.

For our support incident, that means a simple thing: without good tracing, the team will not know who created the duplicate ticket or why it happened.

## 3. A Trace Is the Story of One Run, a Span Is a Meaningful Step

It helps to anchor a simple model:

- a `trace` describes the full path of a request or run;
- a `span` describes one meaningful step within that path;
- `structured events` add precise facts that should not be hidden in free-form text.

For the same support case, one run may include:

- policy evaluation;
- retrieval;
- model inference;
- tool execution;
- approval wait;
- background memory update.

When that structure exists, the team stops seeing the system as a chaotic stream of calls and starts seeing a chain of observable decisions.

That distinction matters because this chapter is not asking how to aggregate, correlate, or alert across the estate. It is asking what raw execution history must survive so those later functions can exist at all.

## 4. What the Trace Should Look Like in the Support Scenario

The point of the diagram below is not just to look nice. It is to show where the failure can actually happen.

<div class="diagram-card">
<p>A mature trace should show not only the model, but all major control points</p>

``` mermaid
flowchart LR
    A["User request"] --> B["Run trace"]
    B --> C["Policy span"]
    B --> D["Retrieval span"]
    B --> E["Model span"]
    B --> F["Tool span: check status"]
    B --> G["Tool span: create ticket"]
    B --> H["Approval span"]
    B --> I["Memory update span"]
```

</div>

If this trace is built correctly, the team should quickly see:

- whether the second tool call happened inside the same run;
- whether there was a retry;
- what the `idempotency_key` was;
- at which step `side_effect_unknown` appeared;
- whether there was approval;
- which policy gate allowed the action.

!!! example "Case thread: trace as the answer to the dispute"
    In the support-triage incident, the trace should not merely say “ticket created.” It should show the linked `trace_id`, `session_id`, `idempotency_key`, policy decision, approval status, and final `create_support_ticket` outcome. Then the dispute “did the model repeat the call, or did retry create the duplicate?” becomes a check against one event chain instead of a guess.

**Trace case-spine note:** the trace structure should distinguish all three canonical cases. Support triage needs linked tool spans, approval status, `idempotency_key`, and the final `create_support_ticket` outcome. Internal knowledge assistant needs retrieval spans with source identifiers, freshness markers, tenant scope, and memory-write events. Incident coordination needs escalation spans, notification outcomes, responder-role changes, and incident-state events so post-incident review sees the decision chain, not only the final status.

## 5. What Should Become Separate Spans

You do not need a span for every tiny detail. But one giant span for the whole run is almost useless too.

A good practical rule is:

- one span for each orchestration step;
- one span for retrieval;
- one span for the model call;
- one span for each tool call;
- one span for a policy decision if it changes behavior;
- one span for human approval wait if it exists.

That keeps the trace readable while still showing where the time, money, and reliability actually went.

## 6. Structured Events Matter Where Plain Text Only Gets in the Way

A common mistake is that useful operational facts get written into human-readable logs and later become impossible to analyze or investigate programmatically.

Structured events are especially useful for:

- policy decisions;
- tool outcomes;
- prompt assembly metadata;
- token usage;
- cost attribution;
- idempotency keys;
- tenant and principal context;
- memory writes;
- [verifier evidence](../../appendix/eval-schema.en.md) for how the run was later graded.

An event should answer not "what should I write in a log line?" but "what will we need later as machine-readable evidence?"

That distinction matters. A trace is not yet a verdict, a policy decision, or an incident response action. It is the raw capture layer that makes those later functions possible.

## 7. A Good Trace Model Shows the Control Plane, Not Only LLM Latency

If observability collapses into model response time only, the team gets a distorted picture.

In reality, the same support run often breaks elsewhere:

- retrieval starts returning noise;
- the policy engine blocks too much;
- approval waits become long;
- a tool adapter degrades;
- background updates clog a queue;
- prompt assembly inflates context;
- a write tool returns an ambiguous outcome.

So a good trace model should cover the full control flow, not only the inference step.

But it should still remain a trace model. It captures execution history for later investigation. The later observability layer is where teams connect many traces into estate-wide evidence, detection logic, and operational visibility.

This chapter therefore stays at the capture boundary: what must be recorded, how it should be structured, and what must survive later review. The later observability chapter is about estate-wide evidence and detection, not about redefining what a trace is.

## 8. The Minimum Set of Fields for Traces and Spans

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

For the support incident, that is already enough to tie together the runtime, the tool gateway, and the specific external side effect.

In a more mature eval program, it also becomes useful to preserve enough linkage for verifier-aware review: not only what happened in the run, but which trace and screenshots later supported a `process_score`, `outcome_score`, or `failure_attribution` judgment.

## 9. Practical Rules for Tracing

If you need a short operational frame, rules like these are usually enough:

1. Every run should have one `trace_id` that survives across policy, model, and tool spans.
2. The trace should cover the control plane, not only model latency.
3. All tool calls, approval waits, and policy decisions should emit machine-readable events.
4. Uncertainty should be logged explicitly: `side_effect_unknown` is more useful than fake `success`.
5. Redaction and schema stability should be designed up front, not after the first incident review.
6. If eval or rollout depends on verifier judgments, traces should preserve explicit linkage to [verifier evidence](../../appendix/eval-schema.en.md).

## 10. Example Structured Event for Tool Execution

Here is a simple template that shows the right style of thinking:

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

That event is much more useful than a line like "ticket tool ok."

### 10.1. Four More Fields Matter in This Case

If the goal is not only dashboards but real incident investigation, it is usually worth adding:

- `approval_id`
- `tool_principal`
- `request_id` or another business object id
- `result_class`
- `verifier_id`
- `evidence_refs`

Those fields make it easier to connect operational telemetry to later grading or rollout review, instead of forcing teams to reconstruct [verifier evidence](../../appendix/eval-schema.en.md) from scratch.

They also often make the difference between:

- a duplicate tool call;
- a late retry;
- the wrong tenant scope;
- an ambiguous external response.

## 11. A Simple Span Emission Example

Below is a small skeleton that shows the core idea: a span should not only start and stop, but also record the type of step and the outcome in a form suitable for analysis.

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

This example is intentionally simple. Its point is not to replace a tracing SDK, but to show the principle: every important step should leave behind a structured trace.

## 12. What You Especially Should Not Log As-Is

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

## 13. What Usually Breaks in Agent Observability

These problems are very recognizable:

- the trace covers only the model call;
- tool calls are not tied to the original run;
- policy decisions are visible in code but not in telemetry;
- events exist, but without tenant/principal context;
- spans are too large or too noisy;
- event schema changes chaotically, and analytics break.

When that happens, the team goes back to guesswork and manual log reading.

At that point, the system may have telemetry exhaust, but it still does not have reliable raw run history.

## 14. A Fast Maturity Test for Agent Observability

A team should not consider observability mature only because it has dashboards, logs, and model latency charts.

A stronger bar is this:

- one run can be reconstructed end to end;
- policy, model, tool, and approval layers are all visible;
- uncertainty is preserved instead of flattened into fake success;
- telemetry can support both incident review and release decisions;
- sensitive data handling is designed, not improvised.

If those conditions are missing, the system may emit telemetry, but it still does not have operational observability.

## 15. What to Do Right After This Chapter

If you want to review your observability model quickly, use this short checklist:

1. Can you reconstruct the full path of one run from a single `trace_id`?
2. Are there separate spans for retrieval, model calls, tool calls, and policy gates?
3. Are idempotency keys and policy decision ids logged?
4. Is tenant/principal context present in telemetry?
5. Can you see where the run spent time and where cost increased?
6. Are sensitive payloads kept out of traces?
7. Is the structured event schema stable?

If the answer is "no" several times in a row, your observability is still decorative, not operational.

## 16. What to Read Next

The next step in the same story is straightforward: once the team can reconstruct the path of one failure, it needs to define what "healthy" means every day. That means moving to SLO.

- [Chapter 10. Idempotency, Retries, Rate Limits, and Rollback Boundaries](../part-iv/chapter-10.en.md)
- [Chapter 12. SLO for Agent Systems](chapter-12.en.md)
- [Chapter 13. Offline Evals, Online Evals, and Regression Gates](chapter-13.en.md)
- [Part V. Reliability and Observability](index.en.md)
- [Sources](../../appendix/sources.en.md)
