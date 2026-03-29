# Chapter 8. Execution Model and Tool Catalog

## 1. Why Tool Calling Is More Than "The Model Chose a Function"

When an agent starts calling tools, many teams first see it as a simple mechanism:

- define tools;
- expose them to the model;
- receive a function call;
- execute the action.

That works in a demo. In production, it is almost never enough.

Tool calling is not only a question of "what the model wanted to call". It is also a question of:

- which actions are allowed at all;
- in what context they are permitted;
- who owns the call contract;
- where validation, retries, and side effects happen;
- how the system behaves under partial failure.

That is why the execution model should be designed as a platform layer, not as a thin helper around an LLM API.

## 2. The Agent Should Not Talk to Tools Directly

One of the most useful architecture habits: the agent should never get direct access to real integrations.

Instead, you want an execution layer that:

- knows the catalog of available tools;
- validates input arguments;
- applies policy checks;
- separates read and write operations;
- manages retries, timeouts, and idempotency;
- emits audit events.

That matters especially when tools affect real systems: tickets, CRM, databases, files, messages, payments.

## 3. A Tool Catalog Is a Platform Interface, Not a Folder of Random Functions

If you treat a catalog like "a directory of calls", it quickly turns into a junkyard of integrations. It is much more useful to think of the catalog as the public interface of the execution layer.

A good tool catalog usually stores:

- a stable tool name;
- a description of its purpose;
- an input schema;
- risk class;
- side-effect level;
- allowed callers or capabilities;
- timeout, retry policy, and idempotency expectations.

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

## 4. Read Tools and Write Tools Are Not the Same

This sounds obvious, but in practice many systems describe them almost identically.

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

If read and write operations collapse into one vague category of "tool call", the execution layer quickly loses control.

## 5. A Tool Contract Should Be Boring and Strict

One of the worst habits in agent systems is allowing the model to improvise the call format.

In a good design, a tool has a contract:

- clear required fields;
- understandable enums and constraints;
- sane error messages;
- an explicit response shape;
- predictable behavior on timeout or duplicate request.

A normal tool schema is more valuable than a "smart" half-page description.

```yaml
tools:
  create_ticket:
    description: "Create a support ticket in the internal helpdesk"
    kind: "write"
    risk: "medium"
    idempotent: true
    timeout_seconds: 15
    input_schema:
      required: ["title", "queue", "requester_id"]
      properties:
        title: {type: string, maxLength: 200}
        queue: {type: string, enum: ["support", "security", "ops"]}
        requester_id: {type: string}
        description: {type: string}
```

It looks ordinary. Good. The less magic in the contract layer, the more stable the tooling layer becomes.

## 6. The Execution Layer Should Normalize Errors

Another common failure: every external service returns errors in its own style, and the agent gets them almost unprocessed.

Then the model receives a chaotic stream:

- HTTP 500 in one place;
- `"failed": true` somewhere else;
- an HTML page somewhere else;
- a stack trace somewhere else;
- an empty response elsewhere.

The execution layer should normalize those into sane outcomes:

- `success`
- `retryable_failure`
- `validation_failure`
- `permission_denied`
- `side_effect_unknown`

That sharply improves explainability and lets the agent make grown-up decisions: retry, request approval, escalate to a human, or stop safely.

## 7. Idempotency and Retries Cannot Be an Afterthought

Almost every real integration eventually gives you at least one unpleasant scenario:

- a timeout after the side effect already happened;
- a duplicate call after a retry;
- partial success;
- a race condition between runs;
- an external service responding later than expected.

If idempotency is not built into execution design, the agent starts doing exactly the kinds of duplicate actions that are already painful in ordinary systems.

## 8. A Simple Execution Layer Skeleton

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

## 9. Tool Results Also Need Design

If a tool result is too raw, the model gets space for dangerous improvisation again.

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

## 10. The Tool Catalog Should Evolve Slowly

If tools change every day without compatibility and versioning, the agent system starts behaving like a client on top of an unstable private API.

That is why the catalog layer benefits from:

- versioned contracts;
- a deprecation policy;
- an owner for each tool;
- schema and result-shape tests;
- capability review before adding new write tools.

This is boring platform work, not romantic improvisation. That is why it works.

## 11. Practical Checklist

If you want to quickly review your execution layer, ask:

- Do you have a real tool catalog instead of just a pile of functions?
- Are read and write tools separated?
- Is there schema validation for arguments?
- Are external system errors normalized?
- Are timeouts, retries, and idempotency handled?
- Can you tell whether a side effect happened?
- Does every tool have an owner and a contract lifecycle?

If the answer is "no" several times in a row, your agent can already call tools, but the execution model is still immature.

## 12. What to Read Next

The next natural topics in this part are sandbox execution, MCP as an integration contract, and the rules for retries and rollback boundaries.

- [Chapter 7. Retrieval, Compaction, and Background Updates](../part-iii/chapter-7.md)
- [Part IV. Tools and Execution](index.en.md)
- [Sources](../../appendix/sources.md)
