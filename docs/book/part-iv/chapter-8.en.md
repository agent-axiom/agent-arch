# Chapter 8. Execution Model and Tool Catalog

## 1. Start with the Same Support Case, but Now on the Write Path

Continue with the same scenario from the first chapters.

The user writes:

> I have been waiting three days for access activation. Check the status, and create an urgent ticket if the request is stuck.

At first glance, the task looks simple:

- the agent reads the message;
- calls a status-check tool;
- if the request is really stuck, calls a ticket-creation tool;
- returns an answer.

In a demo, that is almost enough. In production, this is exactly where the expensive mistakes begin.

Because now the question is no longer only **what the model wanted to do**. The real questions are:

- which tool it is allowed to call at all;
- in what tenant scope that is permitted;
- which arguments count as valid;
- where read and write operations are separated;
- what to do if an external service stalls after the side effect;
- how to prove later whether the ticket was created once or twice.

That is why tool calling must be designed not as a helper around the model, but as the execution layer of the platform.

## 2. The Agent Should Not Talk to Tools Directly

One of the most useful engineering habits here is a boring one: the agent should never get direct access to real integrations.

Instead, you want an execution layer that:

- knows the catalog of available tools;
- validates input arguments;
- applies policy checks;
- separates read and write operations;
- manages retries, timeouts, and idempotency;
- emits audit events.

For the same support case, that means the model should not call the helpdesk API or IAM service directly. It should talk only to the execution layer.

## 3. How One Request Moves Through the Execution Layer

Now look at the same scenario as an execution path.

### 3.1. First the Model Proposes a Read Tool

To understand whether the request is stuck, the agent needs a status-check tool. That is a read path:

- it should not change the outside world;
- it needs the correct tenant scope;
- it should return a clean structured result.

### 3.2. Then the System Decides Whether the Write Tool Is Allowed

If the status says the request is really stuck, the next step may be `create_support_ticket`. But that is already a write path:

- now there is a side effect;
- approval may be required;
- an idempotency key is needed;
- a stricter audit trail is needed.

### 3.3. Then the Execution Layer Takes Over the Ugly Reality

This is where the scenarios that demos ignore start appearing:

- the helpdesk times out after creating the ticket;
- the tool returns partial success;
- the model repeats the call after a retry;
- the external service returns an unexpected payload;
- the runtime is no longer sure whether the side effect happened.

That is no longer just "tool calling." That is execution discipline.

<div class="diagram-card">
<p>The model should not talk to the external world directly, but to the execution layer</p>

``` mermaid
flowchart LR
    A["Prompt + policy context"] --> B["Model"]
    B --> C["Tool request"]
    C --> D["Execution layer"]
    D --> E["Catalog lookup"]
    D --> F["Policy / validation"]
    D --> G["Retry / timeout / idempotency"]
    G --> H["External system"]
    H --> D
    D --> I["Structured tool result"]
    I --> B
```

</div>

## 4. A Tool Catalog Is a Platform Interface, Not a Folder of Random Functions

If you treat a catalog like "a directory of calls," it quickly becomes a junkyard of integrations. It is much more useful to think of it as the public interface of the execution layer.

In the support scenario, the catalog should make it explicit what the agent can actually do:

- `check_access_request_status`
- `get_user_profile`
- `create_support_ticket`
- `request_human_approval`

A good catalog usually has:

- a stable tool name;
- a description of its purpose;
- an input schema;
- risk class;
- side-effect level;
- allowed callers or capabilities;
- timeout, retry policy, and idempotency expectations.

That makes the execution layer inspectable: the team sees not "something the model might call," but a concrete platform contract.

## 5. Read Tools and Write Tools Are Not the Same

This sounds obvious, but in practice many systems describe them almost identically.

For the same support agent, `check_access_request_status` and `create_support_ticket` are not just two tools. They are two different risk classes.

`read tools` usually:

- are less dangerous;
- can more often be called automatically;
- help with grounding and retrieval;
- need access control, but not always approval.

`write tools` usually:

- create side effects;
- require stronger validation;
- need explicit rollback boundaries;
- often require an idempotency key and human approval.

If read and write operations collapse into one vague category of "tool call," the execution layer quickly loses control.

### 5.1. Another Useful Taxonomy: Data, Action, and Orchestration

The OpenAI practical guide includes another helpful simplification: tools are useful to classify not only as `read` and `write`, but also by their role in the system.[^openai-practical]

- `data tools` read and return context: status checks, retrieval, CRM reads;
- `action tools` change the external world: create a ticket, send an email, update a record;
- `orchestration tools` help the runtime itself: request approval, hand off work, call a planner.

Those two axes work well together:

- `data tools` are usually close to `read`;
- `action tools` are usually close to `write`;
- `orchestration tools` can be either, but they have a separate operational meaning.

## 6. A Tool Contract Should Be Boring and Strict

One of the worst habits in agent systems is allowing the model to improvise the call format.

In a good design, a tool has a contract:

- clear required fields;
- understandable enums and constraints;
- sane error messages;
- an explicit response shape;
- predictable behavior on timeout or duplicate request.

For the support case, that can look like this:

```yaml
tools:
  check_access_request_status:
    description: "Read the current status of an access request"
    kind: "read"
    risk: "low"
    timeout_seconds: 10
    input_schema:
      required: ["request_id", "tenant_id"]
      properties:
        request_id: {type: string}
        tenant_id: {type: string}

  create_support_ticket:
    description: "Create a support ticket in the internal helpdesk"
    kind: "write"
    risk: "medium"
    idempotent: true
    timeout_seconds: 15
    input_schema:
      required: ["title", "queue", "requester_id", "tenant_id", "idempotency_key"]
      properties:
        title: {type: string, maxLength: 200}
        queue: {type: string, enum: ["support", "security", "ops"]}
        requester_id: {type: string}
        tenant_id: {type: string}
        idempotency_key: {type: string}
        description: {type: string}
```

It looks ordinary. Good. The less magic in the contract layer, the more stable the tooling layer becomes.

## 7. The Execution Layer Should Normalize Errors

Another common failure: every external service returns errors in its own style, and the agent gets them almost unprocessed.

In the same support case, that easily turns into chaos:

- the IAM service returns HTTP 500;
- the helpdesk answers `"created": true` but does not send `ticket_id`;
- an old integration adapter returns HTML;
- the timeout happens after the side effect;
- a downstream API returns an empty body.

The execution layer should normalize those into sane outcomes:

- `success`
- `retryable_failure`
- `validation_failure`
- `permission_denied`
- `side_effect_unknown`

That sharply improves explainability and lets the agent make grown-up decisions: retry, request approval, escalate to a human, or stop safely.

## 8. Idempotency and Retries Cannot Be an Afterthought

Almost every real integration eventually gives you at least one unpleasant scenario:

- a timeout after the side effect already happened;
- a duplicate call after a retry;
- partial success;
- a race condition between two runs;
- an external service responding later than the expected window.

If idempotency is not built into execution design, the agent starts doing exactly the kinds of duplicate actions that are already painful in ordinary systems.

For the support case, the practical rule is simple: any write tool that can create a ticket, update a record, or send a message needs an explicit idempotency strategy before the first production rollout.

## 9. A Simple Execution Layer Skeleton

This is not a production runtime, but a skeleton that shows the right separation of responsibilities: lookup, validate, execute, normalize result.

```python
from dataclasses import dataclass


@dataclass
class ToolSpec:
    name: str
    kind: str
    timeout_seconds: int
    idempotent: bool


@dataclass
class ToolResult:
    status: str
    payload: dict


def execute_tool(spec: ToolSpec, args: dict) -> ToolResult:
    if spec.kind not in {"read", "write"}:
        return ToolResult(status="validation_failure", payload={"reason": "unknown tool kind"})

    if spec.kind == "write" and "idempotency_key" not in args:
        return ToolResult(status="validation_failure", payload={"reason": "missing idempotency key"})

    # In production this call would go through policy checks, a gateway, and typed adapters.
    return ToolResult(status="success", payload={"tool": spec.name})
```

What matters is not how rich the example is. What matters is that the tool is not executed directly from the model's choice.

## 10. Tool Results Also Need Design

If a tool result is too raw, the model gets dangerous room for improvisation again.

A good result is:

- short;
- structured;
- free of unnecessary technical noise;
- machine-readable in status;
- honest about uncertainty.

A bad result:

- dumps the full external payload;
- mixes user-facing text and system detail;
- does not distinguish "nothing found" from "system failed";
- hides whether a side effect happened.

## 11. The Tool Catalog Should Evolve Slowly

If tools change every day without compatibility and versioning, the agent system starts behaving like a client built on top of an unstable private API.

That is why the catalog layer benefits from:

- versioned contracts;
- a deprecation policy;
- an owner for each tool;
- schema and result-shape tests;
- capability review before adding new write tools.

This is boring platform work, not romantic improvisation. That is why it works.

## 12. What to Do Right After This Chapter

If you want to review your execution layer quickly, use this short list:

1. Do you have a real tool catalog instead of just a pile of functions?
2. Are read and write tools separated?
3. Is there schema validation for arguments?
4. Are external system errors normalized?
5. Are timeouts, retries, and idempotency handled?
6. Can you tell whether a side effect happened?
7. Does every tool have an owner and a contract lifecycle?

If the answer is "no" several times in a row, your agent can already call tools, but the execution model is still immature.

## 13. What to Read Next

The next natural topics in this part are sandbox execution, MCP as an integration contract, and the rules for retries and rollback boundaries. That is where it becomes clear how the same support agent not only calls tools, but does so through a mature execution layer.

- [Chapter 7. Retrieval, Compaction, and Background Updates](../part-iii/chapter-7.en.md)
- [Part IV. Tools and Execution](index.en.md)
- [Sources](../../appendix/sources.en.md)

[^openai-practical]: [OpenAI, A practical guide to building agents (PDF)](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
