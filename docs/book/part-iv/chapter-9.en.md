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

Once MCP adoption grows beyond one or two hand-maintained integrations, another concern appears: **who governs the MCP surface as a platform, not just as a local developer convenience?** Recent enterprise guidance from Cloudflare is useful here because it shows that the hard part is no longer merely “can the agent speak MCP,” but “how do teams discover, approve, route, and audit MCP endpoints at scale.”[^cloudflare-mcp]

That shift usually pushes the platform toward an explicit MCP control plane:

- local ad hoc MCP servers for experimentation;
- governed remote MCP servers for shared production capabilities;
- a discovery or portal layer for approved servers;
- identity enforcement at the access boundary;
- audit and DLP controls around the MCP path itself.

That gives you several immediate benefits:

- failures in one integration affect the central runtime less;
- network, secrets, and filesystem can be constrained per capability;
- it is easier to swap or upgrade one adapter without rewriting orchestration;
- contracts become clearer;
- capabilities are easier to test independently of the agent logic.

That matters especially when some tools are read-only, some write into external systems, and some execute code or shell commands.

### 5.1. Enterprise MCP Usually Needs a Control Plane, Not Just a Protocol

This is where many teams repeat the same maturity mistake. They standardize on MCP as a protocol, but they keep onboarding servers informally: somebody posts an endpoint in chat, another team copies it into a local config, and soon nobody can explain which MCP servers are approved, which ones are experimental, and which ones quietly bypass normal review.

A more mature model treats remote MCP as part of the platform control plane:

- the platform publishes approved MCP endpoints through a registry or portal;
- capability owners are explicit;
- authentication is mediated by a central identity layer rather than hidden inside each desktop client;
- policy and DLP checks can observe MCP traffic as a governed surface;
- retirement of an MCP endpoint is handled like any other lifecycle event.

Once identity becomes central, another design question appears: **who is actually authorizing the MCP call, and with whose user context?** A managed OAuth boundary is useful here because it prevents each MCP server from inventing its own ad hoc credential story.

That usually means:

- user delegation is issued through a governed identity layer;
- tokens are short-lived and attributable to a concrete principal;
- the MCP server receives scoped access rather than broad standing secrets;
- the platform can revoke or rotate access without rewriting every adapter.

That same model also clarifies when **local MCP** is still appropriate: prototyping, isolated experiments, or narrow team-local workflows. But the default for shared business capabilities should usually be: **remote, governed, discoverable, and auditable**.

### 5.2. Shadow MCP Is the New Shadow API Problem

Once MCP becomes easy to attach, teams can accidentally create a new variant of shadow IT: unregistered MCP servers that expose real business actions without clear ownership or review.[^cloudflare-mcp]

That anti-pattern usually has recognizable warning signs:

- capabilities are consumed from private config snippets rather than an approved catalog;
- nobody can name the owner of the MCP server;
- auth is handled with long-lived local secrets;
- no common audit trail exists for which agent used which MCP endpoint;
- the platform team discovers the server only after an incident.

A useful platform checklist is simple:

- Is this MCP server in the approved registry?
- Who owns its lifecycle and incident response?
- Which identity boundary protects access?
- Which policy bundle governs write actions and approvals?
- What telemetry proves which agent called it and with what decision context?

If those answers are missing, the issue is not just “an integration is undocumented.” The issue is that the platform has created a shadow capability path outside its own control model.

A good follow-up question is also: **can the platform explain the authorization chain for this MCP action?** In a governed setup, operators should be able to reconstruct:

- which user or service principal delegated access;
- which identity layer minted or brokered the token;
- which MCP server accepted the delegated scope;
- which agent run used that authorization to perform the action.

If that chain is missing, auditability is weaker than the protocol surface suggests.

### 5.3. Ephemeral Sandboxes Are Usually Better Than Permanent Environments

Another useful Google idea is that risky capabilities are often better served by short-lived execution environments.[^google-sandbox]

Why that is usually better:

- there is less chance that state leaks across runs;
- it is easier to constrain the lifetime of secrets and temporary files;
- cleanup is easier to explain;
- one dirty adapter is less likely to poison the next task.

Persistent workers sometimes win on latency, but they often lose on isolation and explainability. So the default stance for high-risk execution should usually be: **ephemeral first, persistence only by explicit need**.

## 6. Stateful MCP Changes What the Runtime Must Track

Another recent AWS signal is useful here: once MCP clients and servers support more stateful interaction patterns, MCP stops being just a stateless tool envelope and starts looking more like a sessioned runtime protocol.[^aws-stateful-mcp]

That changes the execution contract in several practical ways:

- the runtime may need to keep a `session_id` per MCP interaction, not just per user run;
- capabilities may emit progress notifications before a final result exists;
- the server may request elicitation or additional user input mid-flow;
- expiry and re-initialization become part of the normal lifecycle rather than edge cases;
- telemetry must explain not only which tool was called, but which MCP session instance carried the work.

If the platform keeps treating MCP as fully stateless after those patterns appear, pause/resume logic, approval routing, and trace reconstruction all become much harder than they need to be.

### 6.1. Stateless MCP and Stateful MCP Need Different Contracts

A useful distinction is simple:

- `stateless MCP`: one request, one response, little or no session continuity;
- `stateful MCP`: a bounded interaction session with progress, intermediate prompts, and possible resume or re-init semantics.

The second model usually needs more from the platform contract:

- session lifecycle ownership;
- expiry handling;
- resumability rules;
- telemetry for progress and elicitation events;
- policy fields that describe whether a paused session may resume automatically or requires renewed approval.

That does not make stateless MCP obsolete. It simply means the platform should not pretend both modes are operationally identical.

### 6.2. Progress, Elicitation, and Expiry Are Runtime Events, Not Transport Trivia

A useful operational lesson from AWS's stateful MCP direction is that the hard part is not merely storing a session handle.[^aws-stateful-mcp] The harder part is deciding how the runtime should react when the capability emits progress, requests more input, or expires before the work is done.

That usually forces the platform to define explicit behavior for at least four cases:

- `progress_update`: the capability is still working and the runtime should expose liveness without treating the call as stuck;
- `elicitation_requested`: the capability cannot continue until the user or operator supplies more input;
- `session_expired`: the prior capability session can no longer be resumed safely;
- `reinitialized_session`: the runtime deliberately opened a fresh capability session and linked it to the same higher-level user run.

Those are not small transport details. They shape how approval, telemetry, and operator response all behave.

### 6.3. A Good MCP Contract Should Explain What Happens After Interruption

If a stateful capability pauses mid-flow, the platform should not improvise its recovery logic.

It helps to make at least these rules explicit:

- whether the same capability session may resume after human approval;
- whether expiry cancels the run or triggers re-initialization;
- whether the next step requires fresh policy evaluation;
- whether the runtime preserves the same user-visible run while rotating the capability-side session;
- how telemetry links the old and new capability sessions during investigation.

Without those answers, a team may technically support stateful MCP while still leaving operators unable to explain what happened after an interruption.

## 7. Not Every Capability Needs the Same Isolation Level

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

- authentication mode;
- whether access is platform-owned or user-delegated;
- token lifetime and renewal rules;
- scope boundaries per capability;
- what gets logged about delegated authorization;
- what happens when delegated access is revoked mid-session.

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
    session_mode: stateful
    progress_events: true
    elicitation: manager_or_requester
    on_session_expiry: reinitialize_or_cancel
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

The same problems now repeat at two levels: at the individual adapter level, and at the MCP estate level.

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
