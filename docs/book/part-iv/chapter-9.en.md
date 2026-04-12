# Chapter 9. Sandbox Execution and MCP as an Integration Contract

!!! info "How to read this chapter"
    It helps to keep one concrete transition in mind:

    - the agent has already chosen a capability;
    - the agent is already about to reach an external tool or adapter;
    - the platform now has to decide through which transport that action may execute at all and inside which limits.

    If that transition is not explicit, sandboxing and MCP quickly turn into vocabulary rather than execution discipline.

## 1. Why an Execution Layer Without a Sandbox Quickly Becomes Too Trusting

In the running support case, this is very concrete: the agent has already decided to check the request status or create a ticket through an external system. From this point, the question is no longer "what is the next smart step," but "through which boundary is the system even allowed to execute it."

Once an agent has access to tools, the next danger is almost always the same: system boundaries start to blur.

The agent can now:

- read data;
- run operations;
- call external services;
- receive responses from unpredictable environments.

If all of that executes "as is", without isolation and contracts, the platform quickly accumulates problems:

- a tool returns untrusted payloads in unexpected formats;
- an integration hangs or exceeds a resource budget;
- a side effect happens outside the expected policy path;
- one badly designed adapter drags the whole runtime down.

That is why the execution layer is not just a router. It is also a sandbox boundary.

## 2. A Sandbox Is Not Necessarily a Container, It Is First a Set of Limits

When people say "sandbox", many immediately think of Docker, a VM, or a separate process. Those are possible implementations, but architecturally the important thing is different: a sandbox defines the limits of what a capability is allowed to do.

A good sandbox usually limits:

- network access;
- file system access;
- access to secrets;
- CPU and memory budgets;
- allowed syscalls or execution mode;
- operation lifetime.

In other words, the sandbox answers: "What happens if a tool or adapter behaves worse than we expected?"

This is not only security. It is also blast-radius control.

### 2.1. It Helps to Distinguish Levels of Isolation

In practice, the word `sandbox` often hides several different levels:

- `logical isolation`: policy checks, capability contracts, allowlists;
- `process isolation`: separate process, timeout, resource limits;
- `runtime isolation`: separate execution environment, reduced filesystem, constrained network egress, minimal secrets.

That matters because many teams think they "have a sandbox" while in reality they only have the first level. For low-risk reads that can be enough, but for high-risk execution you almost always need a stronger runtime boundary.[^google-sandbox]

A good practical question here is: **if the capability behaves worse than expected, what exactly stops it: logic, process boundaries, or the execution environment itself?**

## 3. You Cannot Treat an External Integration Like a Simple Function

A common mistake looks like this: an external service is wrapped in a function, and the agent sees it as just another call.

But a real integration is almost always:

- less stable than local code;
- less cleanly typed;
- dependent on permissions and environment;
- capable of returning partial or unsafe results;
- subject to its own latency and rate limits.

That is why it is more useful to treat integrations as capability endpoints with a contract, not as convenient helper methods.

## 4. MCP Is Useful Precisely as a Contract Layer

MCP is not useful because it is fashionable. It is useful because it gives you a clear contract boundary between the agent and an external capability.

In a good design, MCP gives you several benefits:

- a standardized way to describe tools and resources;
- a separate server boundary;
- a clearer lifecycle for connected capabilities;
- the ability to keep adapters outside the core runtime;
- a natural point for policy checks, logging, and isolation.

That becomes especially valuable once you have not one runtime and one integration, but a set of capabilities you want to connect systematically rather than chaotically.

<div class="diagram-card">
<p>MCP is useful as a contract layer between the runtime and external capabilities</p>

``` mermaid
flowchart LR
    A["Agent runtime"] --> B["Execution layer"]
    B --> C["Policy and validation"]
    C --> D["MCP client"]
    D --> E["MCP server"]
    E --> F["Typed adapter"]
    F --> G["External API / system"]
    G --> F
    F --> E
    E --> D
    D --> B
```

</div>

## 5. Why Move Adapters Out of the Core Runtime

That gives you several immediate benefits:

- failures in one integration affect the central runtime less;
- network, secrets, and filesystem can be constrained per capability;
- it is easier to swap or upgrade one adapter without rewriting orchestration;
- contracts become clearer;
- capabilities are easier to test independently of the agent logic.

That matters especially when some tools are read-only, some write into external systems, and some execute code or shell commands.

### 5.1. Ephemeral Sandboxes Are Usually Better Than Permanent Environments

Another useful Google idea is that risky capabilities are often better served by short-lived execution environments.[^google-sandbox]

Why that is usually better:

- there is less chance that state leaks across runs;
- it is easier to constrain the lifetime of secrets and temporary files;
- cleanup is easier to explain;
- one dirty adapter is less likely to poison the next task.

Persistent workers sometimes win on latency, but they often lose on isolation and explainability. So the default stance for high-risk execution should usually be: **ephemeral first, persistence only by explicit need**.

## 6. Not Every Capability Needs the Same Isolation Level

It is useful to split integrations into at least three classes:

- low-risk read capabilities;
- medium-risk business actions;
- high-risk execution capabilities.

Examples:

- `read_kb` or `search_docs` can run with softer controls;
- `create_ticket` or `update_crm_record` need stricter policy and audit;
- `run_shell`, `exec_sql`, or `deploy_job` need the strongest sandbox and approval.

If every tool gets the same soft execution profile, the platform becomes either unsafe or incident-prone.

## 7. A Capability Contract Must Include More Than Input/Output

Many teams do a decent job describing input schema, but the operational contract is missing. In practice, that part is often more important.

It helps to define explicitly:

- read or write nature;
- network policy;
- secret scope;
- allowed environments;
- timeout budget;
- retry policy;
- approval requirement;
- logging and redaction rules.

```yaml
capabilities:
  search_docs:
    transport: mcp
    mode: read
    network: internal_only
    secrets: none
    timeout_seconds: 8
    approval: none
  create_ticket:
    transport: mcp
    mode: write
    network: internal_only
    secrets: service_account_helpdesk
    timeout_seconds: 15
    approval: manager_for_high_priority
  run_shell:
    transport: sandboxed_exec
    mode: high_risk
    network: denied
    filesystem: workspace_only
    secrets: none
    timeout_seconds: 10
    approval: always
```

This is no longer just a function description. It is a behavioral contract for a capability.

## 8. Sandbox Execution Should Return Execution Facts, Not Only Output

If the sandbox returns only stdout or a payload, you lose half the value of the isolation layer.

For investigations and control, it is useful to return:

- exit status;
- timeout flag;
- resource usage summary;
- side effect uncertainty;
- redacted logs;
- policy decision id.

Then the execution layer can explain not just "the command failed", but something mature like: "the operation was terminated by timeout after 8 seconds, network was denied, side effect is not confirmed".

### 8.1. Network Egress Deserves Its Own Rule Set

Many incidents happen not because a capability "broke," but because it was able to reach a destination nobody expected.

That is why network egress should be described not as a footnote of sandboxing, but as its own contract surface:

- `denied`;
- `internal_only`;
- `allowlisted_external`;
- `brokered_via_gateway`.

If that is not fixed explicitly, it becomes very hard to explain later why a tool suddenly called out to an external destination while technically "breaking no rule."

For a production-grade platform, a good default is often:

- read-only internal tools: `internal_only`;
- external API adapters: `allowlisted_external`;
- code execution and shell-like tools: `denied` by default.

## 9. A Simple Capability Dispatch Example

This small skeleton shows the core idea: transport and execution profile are chosen from the capability contract, not invented by the model on the fly.

```python
from dataclasses import dataclass


@dataclass
class CapabilitySpec:
    name: str
    transport: str
    mode: str
    timeout_seconds: int


def dispatch_capability(spec: CapabilitySpec, args: dict) -> dict:
    if spec.transport == "mcp":
        return {"status": "success", "transport": "mcp", "capability": spec.name}
    if spec.transport == "sandboxed_exec" and spec.mode == "high_risk":
        return {"status": "approval_required", "capability": spec.name}
    return {"status": "validation_failure", "reason": "unsupported capability profile"}
```

It is intentionally simple, but it locks in the right idea: the way execution happens is determined by the platform, not improvised by the model every time.

## 10. Common Mistakes

The same problems repeat over and over:

- a capability gets more network access than it needs;
- secrets are visible to too many adapters;
- tool results drag raw external payloads into prompts;
- timeouts exist, but side effect uncertainty is not modeled;
- an MCP server was added, but policy and audit never reached it;
- a sandbox exists on paper but does not restrict anything important.

That is why sandboxing cannot be a checkbox feature. It has to be part of execution design.

## 11. What to Do Right Away

Start with this short list and mark every "no" explicitly:

- Are adapters separated from the core runtime?
- Is there a per-capability execution profile?
- Are network, filesystem, and secrets constrained?
- Is it clear which isolation level is used: logical, process, or runtime?
- Is transport explicit: direct, MCP, sandboxed exec?
- Does the system distinguish trustworthy from only partially trusted results?
- Do you store execution facts beyond business payload?
- Are ephemeral sandboxes used where high-risk execution exists?
- Can you explain why a capability was allowed in this specific run?

If those answers are vague, the capability layer is still a pile of useful integrations, not a managed platform.

## 12. What to Do Next

First lock down execution profiles and isolation boundaries, then move to retries, rate limits, and rollback boundaries.

The next natural topic in this part is idempotency, retries, rate limits, and rollback boundaries. After sandboxing and capability contracts, that is what turns the execution model into a production-grade layer.

- [Chapter 8. Execution Model and Tool Catalog](chapter-8.en.md)
- [Chapter 10. Idempotency, Retries, Rate Limits, and Rollback Boundaries](chapter-10.en.md)
- [Part IV. Tools and Execution](index.en.md)
- [Sources](../../appendix/sources.en.md)

[^google-sandbox]: [Google Cloud, Introducing Agent Sandbox](https://cloud.google.com/blog/products/containers-kubernetes/agentic-ai-on-kubernetes-and-gke/)
