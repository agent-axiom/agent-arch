# Causal Debugging and Root-Cause Analysis for Agent Systems

Once a team already has traces, session summaries, and incident records, the next question is not just what failed, but what actually caused the failure.

Ordinary logs answer “what happened.” Causal debugging is for answering “which step, edge, or hidden dependency actually drove the system into the bad outcome.”

## 1. Why plain tracing is not enough

In agent systems, a long run may include:

- retrieval;
- a model step;
- a tool call;
- an approval path;
- a memory write;
- a handoff or orchestration step.

If the team reads those events as a flat sequence, it sees the order of events, but not necessarily:

- which step was decisive;
- which error was primary and which was secondary;
- where a failure created a cascade;
- what broke the system and what was only a consequence.

That is where ordinary trace review hits its limit.

## 2. What causal debugging means here

In practical terms, causal debugging means:

- isolate the suspect path;
- reconstruct dependencies between events;
- separate the trigger from downstream noise;
- identify which corrective action would actually change the outcome.

This is especially important in systems where one risky run can lead to:

- an unnecessary tool call;
- a bad approval request;
- memory contamination;
- rollback;
- incident escalation;
- a misleading postmortem conclusion.

## 3. Which nodes usually matter

Even a minimal causal graph for an agent system usually includes:

- user input or external trigger;
- retrieved context;
- model decision;
- policy decision;
- approval event;
- tool execution;
- memory write;
- final outcome.

Not every incident touches every node. But if the graph cannot express these link types, diagnosis quickly becomes too coarse.

## 4. Which questions the team should be able to ask

Useful causal debugging starts with good questions, not a pretty graph:

- which first step pushed the run into a risky path;
- which decision changed the trajectory;
- whether the policy gate caused the problem or merely failed to stop it;
- which tool call was the trigger and which was only a cascade effect;
- which corrective action changes the root cause rather than the symptom.

Without these questions, root-cause analysis quickly collapses into “the model behaved strangely.”

## 5. How this relates to traces and structured events

Causal debugging does not replace the [Trace Schema and Event Catalog](trace-schema.en.md). It builds on it.

A good trace layer already provides:

- `trace_id`
- `session_id`
- event types;
- policy decisions;
- approval outcomes;
- tool execution;
- memory events.

But causal debugging adds one more step: treating those events as a dependency network, not just as a list.

## 6. Where false causes often appear

Several traps are common:

- the team treats the last failed tool call as the cause, while the real trigger was in retrieved context;
- blame goes to the model step, while the actual problem was a stale policy bundle;
- an approval denial is read as a failure, even though it was the correct containment behavior;
- noisy retries hide the first bad decision;
- a memory write looks like the cause, even though it was only a late side effect.

That is why “the last strange event” and “the root cause” rarely match.

## 7. What is worth preserving for root-cause analysis

The minimal artifact set is usually:

- `trace_id`
- `session_id`
- `bundle_id`
- `change_id`
- `rollout_wave`
- the active policy bundle;
- the active approval mode;
- `tool_principal`;
- touched memory records;
- linked incident or postmortem id.

Without these links, the team will spend longer arguing about causes than fixing the system.

## 8. How this relates to multi-agent reliability

In multi-agent systems, causal debugging matters even more because you also get:

- handoff edges;
- delegated tasks;
- conflicting agent states;
- ambiguous responsibility across nodes.

This does not mean every team needs a full causal graph engine. But the more complex the orchestration, the more important it becomes to localize:

- where the coordination path failed;
- which handoff lost critical context;
- which agent was the real source of failure.

## 9. What should change after root-cause analysis

Good root-cause analysis should usually end with one of these updates:

- update the policy bundle;
- add or tighten an eval case;
- narrow capability exposure;
- refine approval scope;
- update the rollout gate;
- fix retrieval filtering;
- pause or revise the memory write path.

If diagnosis does not lead to artifact changes, it may be interesting, but it is not operationally strong.

## 10. Practical checklist

- Can the team separate the trigger from cascade effects?
- Can it distinguish a bad decision from correct containment?
- Are policy, approval, and tool edges visible in traces?
- Can the active bundle and rollout wave be reconstructed?
- Is it clear which corrective action changes the root cause?
- Does the team avoid reducing root cause to “the model failed” without deeper localization?

## See also

- [Trace Schema and Event Catalog](trace-schema.en.md)
- [Incident Record and Postmortem Linkage Schema](incident-record-schema.en.md)
- [Postmortem Template for Agent Systems](postmortem-template.en.md)
- [Incident Response Playbook for Agent Systems](incident-response-playbook.en.md)
- [Chapter 11. Traces, Spans, and Structured Events](../book/part-v/chapter-11.en.md)
- [Chapter 26. AI-Native Observability, Inventory Coverage, and Detection-Ready Telemetry](../book/part-viii/chapter-26.en.md)
