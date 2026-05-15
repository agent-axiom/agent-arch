# Practice. MCP for Tools, A2A for Agents

Many teams mix up two different problems too early:

- how to connect tools and external systems;
- how to organize collaboration between multiple agents.

Because of that, `MCP` and `A2A` start to look interchangeable. In reality, they belong to different architectural levels.

## 1. The Short Rule

If you want the shortest version:

- `MCP` is for working with tools, resources, and adapters;
- `A2A` is for exchanging tasks, context, and results between agents.

In other words, one protocol is mainly about **agent-to-tool**, while the other is about **agent-to-agent**.[^google-mcp-a2a][^google-multiagent]

## 2. When You Almost Certainly Need MCP

`MCP` is useful when you have one or more external capabilities that need to be connected systematically:

- document search;
- CRM;
- helpdesk;
- internal APIs;
- file resources;
- knowledge bases;
- execution sandboxes.

In that situation, the main goal is not to "build a society of agents," but to:

- standardize the contract;
- separate adapters from the core runtime;
- simplify policy checks;
- centralize logging, auth, and isolation.

That is where `MCP` fits naturally.

## 3. When You Actually Need A2A

`A2A` makes sense when you no longer just have tools, but truly distinct agents with separate responsibility:

- a coordinator;
- a researcher;
- an analyst;
- an executor;
- a domain specialist.

And they need to:

- hand tasks to each other;
- delegate work;
- exchange status;
- return results not as tool payloads, but as the work product of another agent.

That means `A2A` appears not where you need "one more adapter," but where real agent boundaries already exist in the system.

### 3.1. A2A Needs Governance, Not Just a Handoff Protocol

If one agent can hand a task to another agent, the platform must govern not only the message but also trust between operational roles. Otherwise A2A quickly becomes an opaque delegation chain where nobody can explain who was allowed to act, which policy applied, or who owns the result.

A minimal governance contract for A2A should record:

- the identity of the calling agent and the executing agent;
- the boundaries and lifetime of delegated authority;
- capability discovery: which roles an agent may discover and call;
- an audit trail for the handoff, intermediate status, and final result;
- policy checks before delegation and before external side effects.

The simple production test is this: if an incident review cannot reconstruct which agent delegated what to whom, under which policy, and with which scope, the A2A contour is not production-ready yet.

## 4. The Typical Mistake: Building Multi-Agent Too Early

In practice, the confusion usually looks like this:

1. The team has one runtime.
2. It needs to connect three systems.
3. Instead of capability contracts, the team starts designing multi-agent orchestration.

That is almost always unnecessary complexity.

If the system still has no real reason to split responsibility between agents, then:

- tools are better connected through `MCP`;
- orchestration is better kept inside one runtime;
- multi-agent coordination is better postponed.

A good practical rule is: **if the entity does not make its own decisions and does not have its own operational role, it is probably not an agent yet. It is a capability**.

### 4.1. Multi-agent reliability research currently reinforces skepticism

This point is worth one more practical note. Recent papers on multi-agent reliability do not yet provide a strong reason to make runtimes more complex by default. If anything, they show how quickly coordination failures, verification gaps, and ambiguity grow when a system is split without a clear need.

The practical reading is:

- the research does not say “build more agents”;
- the research says “if you already build multi-agent systems, use explicit contracts, verification loops, and diagnosable handoffs”;
- the current best practice is still `single-agent first`.

That is why `A2A` should be introduced not because it looks architecturally elegant, but because the system already contains separate operational roles that can no longer be honestly described as tools.

### 4.2. Agreement between several agents is not independent verification

Even if several agents reach a similar conclusion, that still does not prove the system has produced an independent verification signal.

The common problems are familiar:

- agents see the same contaminated context;
- the reasoning paths are too similar;
- the manager agent nudges downstream agents toward the expected answer;
- the consensus looks convincing while resting on the same bad assumption.

That is why multi-agent agreement is better treated as a signal, not as proof of correctness.

## 5. Decision Table

| Question | More likely `MCP` | More likely `A2A` |
| --- | --- | --- |
| Do you need to connect an external API or resource? | Yes | No |
| Do you need a typed contract for tools? | Yes | No |
| Is there a separate agent with its own role and lifecycle? | No | Yes |
| Do you need delegation between agents? | No | Yes |
| Do you need to isolate adapter behavior and policy path? | Yes | Sometimes |
| Do you need to pass a task to another agent runtime? | No | Yes |

## 6. What This Looks Like in a Mature Architecture

In a mature platform, these ideas do not compete. They sit on different layers.

<div class="diagram-card">
<p>MCP and A2A complement each other instead of replacing each other</p>

``` mermaid
flowchart LR
    A["Coordinator agent"] --> B["A2A handoff"]
    B --> C["Specialist agent"]
    A --> D["MCP client"]
    C --> E["MCP client"]
    D --> F["Tool / resource server"]
    E --> G["Tool / resource server"]
```

</div>

The healthy pattern is:

- an agent works with tools through `MCP`;
- an agent works with another agent through `A2A`;
- policy and audit should cover both directions.

!!! note "MCP/A2A case-spine note"
    The MCP-vs-A2A choice shows up differently across the three canonical cases. **Support triage** usually keeps helpdesk, CRM, and ticket-write tools behind an MCP boundary, and only adds A2A when a separate responsible role appears. **Internal knowledge assistant** tests the knowledge server, retrieval adapter, source attribution, and tenant boundary through MCP. **Incident coordination** more often needs A2A handoff between intake, investigation, remediation, and owner record, while notification tools and incident state resources still remain under MCP/policy audit.

## 7. When Not to Use A2A

There are a few red flags:

- you want to use a second agent only as an API wrapper;
- the second agent has no separate policy surface;
- it has no separate operational identity;
- it can be described more simply as a capability contract;
- parallelism and specialization do not produce clear value.

In all those cases, it is better to stay with `MCP` or even an ordinary gateway/adapter layer.

## 8. Minimal Code Sketch

Below is a very small sketch that shows the difference in thinking:

```python
def call_tool_via_mcp(tool_name: str, payload: dict) -> dict:
    return {"kind": "tool_result", "tool": tool_name, "payload": payload}


def delegate_via_a2a(agent_name: str, task: dict) -> dict:
    return {"kind": "agent_result", "agent": agent_name, "task": task}
```

The point is not the code itself, but the interaction type:

- a tool call returns a capability result;
- an A2A handoff returns the work result of another agent.

Those are different operational semantics, and it is useful not to blur them together.

## 9. What to Do Right Away

Start with this short list and mark every "no" explicitly:

- Do I need a new agent or just a new capability?
- Does this entity have its own role, policy surface, and lifecycle?
- Is this a delegation problem or an integration problem?
- Can I explain why `MCP` is not enough here?
- Am I building a multi-agent topology earlier than I actually need?

If those questions are hard to answer, it is usually safer to choose `MCP` first, not `A2A`.

## 10. What to Do Next

- [Part IV. Tools and Execution](index.en.md)
- [Chapter 9. Sandbox Execution and MCP as an Integration Contract](chapter-9.en.md)
- [Chapter 10. Idempotency, Retries, Rate Limits, and Rollback Boundaries](chapter-10.en.md)
- [Research Frontier: Memory, Observability, and Multi-Agent Reliability](../../appendix/research-frontier.en.md)
- [Sources](../../appendix/sources.en.md)

[^google-mcp-a2a]: [Google Cloud, Building Connected Agents with MCP and A2A](https://cloud.google.com/blog/topics/developers-practitioners/building-connected-agents-with-mcp-and-a2a)
[^google-multiagent]: [Google Cloud Architecture Center, Multi-agent AI system in Google Cloud](https://docs.cloud.google.com/architecture/multiagent-ai-system)
