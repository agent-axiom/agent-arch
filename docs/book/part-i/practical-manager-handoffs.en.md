# Practice. Manager Pattern vs Handoffs

## 1. Why This Choice Matters

The moment a team reaches the multi-agent topic, the same temptation appears:

- one agent plans;
- another searches;
- a third writes;
- a fourth reviews;
- and the diagram looks very impressive.

The problem is that an impressive diagram and a stable system are not the same thing.

In practice, one of the most useful questions is:

> Do we need a manager pattern here, or handoffs?

This is not an aesthetic question. It is a question of:

- who owns the global context;
- where responsibility for the next step lives;
- how blast radius is constrained;
- how failures will be investigated later.

OpenAI's practical guide is useful here because it pushes against romanticizing multi-agent by default and instead asks where coordination really lives and where responsibility should live.[^openai-practical]

## 2. What the Manager Pattern Is

`manager pattern` means you have one central orchestrator that:

- owns the overall run goal;
- decides which specialist to call;
- gets results back;
- assembles the final answer or next plan.

It is close to the model of "a manager calling specialists as tools."

Pros of manager pattern:

- a single control point;
- easier global policy control;
- more convenient audit trail;
- easier budget and max-step control.

Cons:

- the manager can grow into a bottleneck;
- too much context accumulates in one place;
- the whole system becomes fragile if the manager routes poorly.

## 3. What the Handoff Pattern Is

`handoff pattern` means the current agent can transfer control to another agent, and that agent temporarily becomes the main owner of its part of the task.

This is closer to the model of "responsibility passes to the next role."

Pros of handoffs:

- cleaner role and ownership separation;
- easier context isolation;
- easier domain-specialized behavior;
- lower risk of one central orchestrator becoming overloaded.

Cons:

- harder to see the global run picture;
- harder to build one coherent audit narrative;
- handoff boundaries must be designed carefully;
- higher risk of losing state, intent, or constraints during transfer.

## 4. The Most Useful Practical Rule

In short:

- `manager pattern` is better when you need one coordination center;
- `handoffs` are better when the task naturally moves between different roles or domains.

So the real question is not "which one is more modern," but "where should responsibility live?"

## 5. When the Manager Pattern Is Usually Right

Manager pattern usually works well if:

- the task is short or medium in length;
- you need unified budget control;
- tools and policy are almost the same across subtasks;
- the team wants maximum explainability;
- there is one primary runtime owner.

Typical examples:

- support triage;
- a research assistant with one final answer;
- an internal copilot calling several read-heavy capabilities;
- an agent where specialists are basically typed tools.

!!! note "Manager/handoff case-spine note"
    The manager-vs-handoff choice changes across the three canonical cases. **Support triage** usually benefits from a manager pattern because the approved write routine and ticket state should stay in one audit story. **Internal knowledge assistant** often remains manager-led while read-heavy capabilities, source attribution, and tenant boundary can stay in one controlled context. **Incident coordination** reaches handoffs sooner because escalation, security investigation, remediation, and owner record often move across different accountable roles.

In these cases, manager pattern is often the most boring and most correct answer.

## 6. When Handoffs Are Better

Handoffs usually win if:

- the task truly crosses domain boundaries;
- each role needs its own context and guardrails;
- ownership is already split across teams;
- it helps to narrow the cognitive scope of the current agent;
- the next step feels more like transfer of responsibility than a helper call.

Typical examples:

- sales qualification -> solution agent -> legal review agent;
- incident intake -> security investigation -> remediation coordinator;
- onboarding flows owned by different business units.

Here, handoff is often more natural than a central manager pretending to understand everything equally well.

## 7. Common Mistakes

Both patterns have typical failure modes.

For manager pattern:

- the manager carries too much context;
- specialist agents become too thin to matter;
- routing lives in a prompt instead of explicit policy;
- the central orchestrator becomes a single point of confusion.

For handoffs:

- constraints and intent get lost in transfer;
- the next agent gets too little or too much state;
- it becomes unclear who owns the final outcome;
- the trace becomes fragmented and hard to read.

So the main question is not "which pattern is more powerful," but "which pattern can you operate calmly?"

## 8. A Simple Decision Table

This is a good starting orientation.

| Situation | What is usually better |
| --- | --- |
| Unified control of steps, cost, and policy is needed | `manager pattern` |
| Roles and domains are naturally separated | `handoffs` |
| A specialist behaves like a capability tool | `manager pattern` |
| The next participant needs its own context boundary | `handoffs` |
| One coherent audit story matters most | `manager pattern` |
| Local autonomy of a role-specific agent matters most | `handoffs` |

This table does not replace design, but it removes a lot of unnecessary romance.

## 9. How Not to Be Wrong Too Early

The healthiest strategy usually looks like this:

1. start with a single-agent loop;
2. move to manager pattern if several specialist paths need coordination;
3. only then move to handoffs if real domain boundaries are visible.

This is not dogma. It is a good defense against premature complexity.

## 10. Code Sketch: Manager Pattern

```python
def run_manager(task: str, specialists: dict[str, callable]) -> dict:
    plan = ["research", "draft", "review"]
    results: dict[str, dict] = {}

    for step in plan:
        worker = specialists[step]
        results[step] = worker(task=task, prior_results=results)

    return {"status": "success", "results": results}
```

The point is not that the manager should "think forever." The point is that it owns the plan, calls specialists, and assembles the result.

## 11. Code Sketch: Handoff Pattern

```python
def handoff(state: dict, next_agent: callable) -> dict:
    transfer_packet = {
        "goal": state["goal"],
        "constraints": state["constraints"],
        "relevant_context": state["relevant_context"],
    }
    return next_agent(transfer_packet)
```

What matters here is not the call itself, but the fact that a handoff should pass a deliberate transfer packet, not the whole chaotic state blob.

## 12. What Matters Most for Safety

If you use manager pattern, check:

- whether the manager has too much privilege;
- whether it can bypass approval boundaries "on behalf of everyone";
- whether it becomes the place through which all tenant contexts can leak.

If you use handoffs, check:

- whether policy constraints survive the transfer;
- whether risk classification is preserved;
- whether untrusted context is passed to the next agent without marking;
- whether the trace shows who actually took control.

So safety here is not something "on top of orchestration." It is part of orchestration semantics itself.

## 13. What to Do Right Away

Start with this short list and mark every "no" explicitly:

- Who owns the global run goal?
- Who owns the final outcome?
- Where does budget control live?
- Where do stop conditions live?
- Can the traces explain who handed the task to whom and why?
- Did you move to handoffs too early when manager pattern would have been simpler?
- Has the manager become a central monster that does everything at once?

If the answers are blurry, the pattern is not mature yet.

## 14. What to Do Next

- [Practice. Instructions, Routines, and Prompt Templates](practical-routines.en.md)
- [Chapter 2. Reference Architecture for a Safe Agent](chapter-2.en.md)
- [Part IV. Tools and Execution](../part-iv/index.en.md)
- [Sources](../../appendix/sources.en.md)

[^openai-practical]: [OpenAI, A practical guide to building agents (PDF)](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
