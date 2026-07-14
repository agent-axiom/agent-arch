# Chapter 9. Sandbox Execution and MCP as an Integration Contract

!!! info "Freshness note"
    Last reviewed: **May 17, 2026**. Previous review: **May 14, 2026**. Next scheduled review: **June 17, 2026**.

    What changed since the previous review: MCP security boundaries, tool-poisoning surfaces, A2A trust model, and print-readiness concerns now have concrete contract coverage and docs-surface guards.


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

**Sandbox/MCP case-spine note:** the sandbox and MCP contract should be tested against all three canonical cases. Support triage needs sandbox limits for helpdesk writes, approval-aware MCP tools, and a reconciliation path after timeout. Internal knowledge assistant needs read-only MCP resources, corpus-scoped network access, source validation, and a ban on hidden side effects. Incident coordination needs isolated escalation adapters, notification scopes, responder-role enforcement, and emergency paths that do not bypass the audit trail.

### 4.1. MCP Is a Security Boundary, Not Just a Convenient Connector

Once MCP carries access to data, write tools, or execution environments, it becomes a security boundary. Useful tool results can cross that boundary, but so can malicious instructions, poisoned tool descriptions, over-scoped OAuth grants, confused-deputy paths, and supply-chain risk from the server itself.

Microsoft's MCP tool poisoning case sharpens this boundary: **tool descriptions as system prompts**.[^microsoft-tools-acting] If a previously approved server silently changes a tool description while keeping the same tool name, the runtime may trust it again without a fresh human review. That is silent re-trust, not a harmless metadata update. Review should therefore inspect the description diff, owner/provenance, imperative language inside documentation fields, new endpoints, expanded parameters, and unusual query patterns. The control is not only least privilege, but **least agency**: disable `Allow all tool access`, require approval for high-impact actions, and alert on agent-behavior drift after tool metadata changes.

The practical contract for that boundary should answer at least five questions:

- who owns the MCP server and its lifecycle;
- which tools/resources it exposes and which write operations require approval;
- which scopes, network paths, and sandbox limits the server receives;
- how the runtime validates tool descriptions and tool return values before giving them to the model;
- which telemetry proves the agent run, identity, and policy decision behind the call.

If those answers are missing, MCP does not stop being a risk. It becomes an implicit trust boundary inside the platform surface.


### 4.2. MCP Threat Model Matrix

For MCP, the [MCP threat model](../../appendix/trace-schema.en.md) should not stay as a vague fear of integrations. It should become a review matrix for every connected capability. A minimal version looks like this:

- **tool poisoning** — a tool description or tool result tries to steer the model; control it by validating tool descriptions, separating tool output from instructions, and allowing only known contracts.
- **rug pull attack** — a previously approved MCP server changes tools, scopes, or behavior after review; control it with version pinning, re-attestation, diff review, and a fast quarantine path.
- **tool shadowing** — a new tool mimics an approved tool and captures the model's intent; control it with unique capability names, registry ownership, and semantic review before publication.
- **confused deputy** — the agent performs an action with the wrong or overly broad delegated authority; control it by checking principal, purpose binding, approval state, and policy decision immediately before the side effect.
- **over-scoped tokens** — the MCP server receives broader OAuth scopes than the operation needs; control it with short-lived scoped tokens, per-tool scopes, and no broad standing secrets.
- **data exfiltration through legitimate channels** — data leaves through an allowed tool result, notification, or ticket comment; control it with DLP checks, output classification, tenant boundaries, and review for risky writes.
- **supply-chain attack** — a compromised server, package, or adapter becomes a trusted capability; control it with provenance, signed artifacts, dependency review, and owner accountability.
- **replay/tampering** — requests, responses, or stateful sessions are replayed or changed between steps; control it with request signing, nonce/idempotency keys, trace correlation, and session expiry.
- **sandbox escape** — a tool or adapter crosses the network, filesystem, or process boundary; control it with ephemeral sandboxes, minimal egress rules, secret isolation, and runtime-level containment.

The matrix is not there to forbid MCP. It is there so every MCP endpoint has an explicit answer to three questions: which threat class it adds, which control limits it, and which telemetry will still be available after an incident.

### 4.3. Minimal MCP Server Contract

A threat model becomes useful only when it turns into a reviewable server artifact. A minimal MCP server record should travel with every approved endpoint:

```yaml
mcp_server:
  owner: platform-integrations
  approved_registry_id: mcp.support.ticketing.v3
  schema_hash: sha256:...
  tool_definition_hash: sha256:...
  allowed_origins:
    - agent-runtime-prod
  auth_mode: delegated_oauth
  token_scope:
    - ticket.read
    - ticket.write_limited
  token_ttl: 15m
  user_delegation_required: true
  server_isolation_profile: remote_ephemeral_sandbox
  return_value_filtering: strip_instructions_and_classify_data
  replay_protection: nonce_and_trace_bound_signature
  schema_change_requires_review: true
```

The important fields are not bureaucracy. `schema_hash` and `tool_definition_hash` catch tool schema injection and post-approval rug pulls. `token_scope`, `token_ttl`, and `user_delegation_required` limit confused-deputy paths. `return_value_filtering` treats tool results as untrusted content, including prompt injection via tool return values. `server_isolation_profile` and `replay_protection` make sandbox escapes, replay, and tampering visible enough to contain.

The short rule is: **tool output is an attack surface**. A remote tool can change after approval: the server owner changes schema, result, redirect, resource body, or hidden instruction, while the host still treats the integration as already approved. Onboarding remote tools should therefore begin with fake data first: connect a synthetic tenant, synthetic secrets, and safe fixtures, record real traces, and only after validation grant live credentials or production data.

Another useful pattern from Google ADK is **metadata registry + runtime schema injection**.[^google-adk-static-prompts] The anti-pattern is explicit: **Static Prompting**, where all JSON schemas, Pydantic classes, and tool definitions are preloaded into the system prompt. In high-cardinality domains this creates context bloat and **Attention Diffusion**: the model starts mixing fields from dormant schemas into the active payload.

In a portable runtime contract, structural rules should live in a registry entry, not in the prompt. That entry should carry `schema_descriptor_id`, `schema_version`, field metadata, mapping rules, and a `validation_hook`. The agent first performs lightweight discovery; then the runtime loads the right descriptor, calls the **Polymorphic Validator** at the boundary before the tool/API call, and records the chosen schema source of truth, runtime validation boundary, validation result, and failure mode in the trace. One reasoning agent can then handle multiple domain forms without carrying every structural rule at once.

### 4.4. Localhost Is Not a Trust Boundary for Browser Agents

AutoJack, described by Microsoft Defender Security Research, is a compact maturity test for this chapter: untrusted web content opened by a browsing agent could cross the loopback boundary, reach a local MCP WebSocket, and turn connection parameters into process execution on the host.[^microsoft-autojack] The concrete issue was fixed before the affected MCP surface shipped in a PyPI release, but the pattern matters more than the bug.

The architectural conclusion is simple: `localhost`, `127.0.0.1`, and origin allowlists are not sufficient controls when the same machine runs an agent with a browser tool, Playwright-backed surfer, code execution tool, or any mechanism that can open a WebSocket/HTTP request from a local process. For that system, external HTML/JavaScript is no longer merely “somewhere on the internet”; it can become a confused deputy that uses the agent's local network position.

The minimum hardening for local MCP/debug/control channels:

- do not treat loopback as an authentication boundary;
- require authn/authz on MCP/control-plane endpoints, including WebSocket paths;
- check purpose binding and policy decision before launching any subprocess-backed MCP server;
- keep launch parameters server-side or in a signed nonce-bound artifact instead of accepting command/args from a query string;
- allowlist executable MCP servers and argument profiles;
- run browser tools with a separate process/network identity that cannot reach privileged local services;
- write a trace event for crossing attempts: external page, local channel, policy result, executable decision, and containment action.

If local MCP is needed only for a prototype, the capability registry should say so explicitly: low privileges, a separate OS user/container, short-lived credentials, and no colocating it with an agent that renders untrusted web content.

### 4.5. Prompt-to-tool-to-execution Needs Its Own Hardening

Microsoft's “When prompts become shells” case adds the adjacent failure mode: a prompt injection does not need to reach `localhost` when the agent framework already exposes a tool that can interpret model-controlled parameters as paths, code, templates, or commands.[^microsoft-prompts-shells] The exploit shape is **prompt-to-tool-to-execution**: untrusted content steers the model, the model emits attacker-controlled input, the framework parses it as tool arguments, and a weak adapter turns it into host execution.

The execution-layer rule is the same one this chapter uses for MCP: model output is not authority. Execution-adjacent tools should be deny-by-default, registered through a capability contract, protected by typed validation, canonical path checks, operation allowlists, and a per-tool sandbox. They also need an audit event before the side effect, not only after it, so an investigator can see the prompt source, redacted arguments, validation result, selected sandbox profile, and policy decision.

### 4.6. It Helps Not to Confuse the MCP Host, Client, and Server

MCP often creates unnecessary confusion because the words sound familiar while the roles are actually quite specific.

It helps to keep this picture in mind:

- the `host` is the application or runtime that owns the session and decides which capabilities should be connected at all;
- the `client` is the protocol-side component the host creates to talk to one specific MCP server;
- the `server` is the boundary that exposes tools, resources, and other capability surfaces, then returns structured results.

Two practical consequences follow from that:

- one host can hold several clients at the same time;
- one agent runtime can work with multiple MCP servers without collapsing them into one indistinguishable integration blob.

That may sound like a minor terminology point, but it helps a lot. The MCP client is not the product UI and not “the agent itself.” It is the transport and contract layer between the host and one specific server boundary.

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

Google Cloud's Gemini Enterprise Agent Platform remote MCP server shows the same boundary in a more managed form.[^google-gemini-enterprise-mcp] An external agent or IDE client does not receive an arbitrary bundle of cloud secrets; it connects to a standardized remote MCP endpoint inside Google Cloud, sees toolsets such as generation, prediction, notebooks, endpoints, models, tuning, evaluation, and prompts, and discovers assets through Agent Registry. The architectural lesson is that a managed remote MCP endpoint can be a **capability boundary** if discovery, IAM Deny policies, tenant/data boundaries, observability, and lifecycle ownership live on the platform side rather than in the client's local config.

The AWS MCP Gateway and Registry frame makes that control-plane shape more concrete.[^aws-mcp-gateway-registry] It treats MCP servers, AI agents, skills, workflows, and other AI assets as cataloged entities rather than scattered endpoints. The useful lesson for this chapter is not the specific implementation stack, but the split of responsibilities: the registry governs discovery, ownership, security scanning, fine-grained access control, and federation; the gateway routes MCP tool calls and records an audit log. That is a cleaner platform contract than letting every agent or desktop client maintain its own private list of servers.

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

### 5.3. MCP as a Governed Access Path to Cloud APIs

A recent AWS Security Blog recommendation is useful because it frames MCP not just as an integration convenience, but as a **governed access path to cloud resources**.[^aws-secure-mcp-access] The important detail is that AI coding assistants and agents can often reach cloud APIs directly through shell, SDK, or arbitrary code execution. If that path remains open, an MCP server with good IAM policies is only one route, not the real control boundary.

So production agents should distinguish:

- `mcp_brokered_action`: the action flows through a registered MCP/tool gateway, receives scoped credentials, writes an audit event, and carries a policy decision;
- `direct_cloud_api_action`: the agent calls an SDK, CLI, or HTTP API directly from a shell/code environment;
- `human_initiated_action`: a human runs the action, while the agent only prepares the plan, diff, or evidence packet;
- `delegated_agent_action`: a human or policy layer delegates a bounded action scope to the agent with TTL, scope, and trace correlation.

The architectural conclusion is strict: direct cloud API access should be treated as a bypass path unless it flows through the same catalog, identity, policy, and audit layer. For the runtime, that adds several required fields to the trace/control record: `actor_type`, `delegation_source`, `credential_scope`, `credential_ttl`, `access_path`, `mcp_server_id`, `policy_decision_id`, and `called_via_gateway`. Then the organization can distinguish human-initiated action from AI-driven action and apply least privilege, organizational role governance, and separate approval rules to the agent path, not only to human IAM.

If the team cannot fully prohibit shell/SDK access, the minimum fallback is explicit bypass control: a restricted shell profile, denylist/allowlist rules for cloud CLIs, network egress through a proxy, detection for direct cloud API calls, and a release gate that blocks the agent capability until critical writes flow through the brokered gateway.

### 5.4. Cloudflare AI Traffic Controls Show That Web Access Is Also a Policy Surface

Cloudflare AI traffic controls add a neighboring but important boundary to this chapter: not only how an agent calls MCP or a cloud API, but how an external site decides which AI traffic is allowed to use its content at all.[^cloudflare-ai-traffic-controls] The Search / Agent / Training split is useful precisely as a governance signal. A search crawler, an interactive Agent, and a Training crawler carry different purposes, different expectations from the resource owner, and different audit requirements.

The runtime lesson is practical: outbound identity cannot be reduced to a user-agent string or an IP allowlist. A web-capable agent should declare a declared purpose, preserve an audit trail, and distinguish at least:

- search/indexing, where the site owner expects discoverability;
- interactive agent access, where the agent acts on behalf of a user;
- training or dataset collection, where content use changes the economics of consent.

Cloudflare also shows an important detail for future access contracts: Content-Signal can carry finer-grained terms such as `use=reference`, while Verified and Forwarded statuses separate verified identity from transitive trust passed through a downstream service. For agent architecture, that means transitive trust has to be modeled explicitly: if a browser or retrieval agent receives access through an intermediary, the trace should show the original identity, forwarded identity, declared purpose, and policy decision, not only the final HTTP request.

A minimal policy matrix for a web-capable agent should therefore carry at least four decisions: allow, block, monetize, or audit-only. Each decision should be bound to the access purpose: Search / Agent / Training. Otherwise web access policy collapses into a fragile list of strings rather than a contract among the resource owner, the user, and the agent platform.

### 5.5. Browser as an action surface

GitHub Copilot browser tools in VS Code show the next step: a live browser is becoming a normal action environment for agents, not only an external way to check work manually.[^github-copilot-browser-tools] If an agent can open pages, click/type/hover/drag, read page content, collect console errors, take a screenshot, and run scripted flows, the browser has to be treated as its own execution surface.

The practical contract for that surface should account for stale DOM refs, auth/session state, non-deterministic UI, and evidence snapshot. The agent should not merely say "the page works"; it should leave verifiable evidence such as a screenshot, DOM assertion, console errors, network trace, or another artifact bound to the run/trace id. Otherwise browser automation becomes just another opaque tool call.

The control layer should also be explicit. User-owned tabs need share/revoke semantics, agent-owned tabs need an isolated session without normal browser cookies/storage, sensitive permission prompts need human approval, and enterprise environments need network domain controls and workspace trust. Then a browser tool is a governed capability rather than direct agent-process access to all web state.

### 5.6. Secure MCP Tunnel Makes Private Reachability Explicit

OpenAI's Secure MCP Tunnel adds a useful deployment pattern for private MCP servers: the private side initiates an outbound-only connection instead of accepting inbound traffic from the public internet.[^openai-secure-mcp-tunnel] A `tunnel-client` runs inside the network that can already reach the private MCP server, long-polls an OpenAI-hosted endpoint for queued MCP work, forwards JSON-RPC requests locally, and returns responses through the same path. The design also creates a natural backpressure point, because the client asks only for work it is ready to process.

The architectural lesson is narrower than "tunnels make private systems safe." A tunnel should be a governed reachability mechanism, not a general-purpose network bridge. The private MCP server still needs owner records, schema hashes, scoped authorization, output filtering, request correlation, and audit events. The tunnel record should say which product surface may call it, which private MCP server it reaches, which identity authenticated the tunnel-client, and which policy decides whether a request is allowed. In other words, Secure MCP Tunnel is useful when it keeps a narrow path: product endpoint -> tunnel service -> authenticated tunnel-client -> private MCP server -> filtered response.

### 5.7. Code Mode Turns the MCP Portal into Progressive Disclosure

Cloudflare also shows a useful pattern for a large MCP estate: do not give the model every tool schema upfront; put the broad API surface behind a portal with two narrow operations for search and execution.[^cloudflare-code-mode] In that pattern, Code Mode lets the model first write code to search for the endpoint definitions it needs, then write code to call the selected operations. That code runs inside a sandbox on the MCP server portal side, not inside the main agent session.

Architecturally, this matters for more than token cost. It changes tool visibility:

- the model receives a search mechanism rather than the whole capability catalog upfront;
- the portal becomes a point for audit, DLP, and identity enforcement;
- the agent context is not bloated by thousands of schema tokens;
- discovery becomes a governed action rather than an implicit load of the whole world;
- the portal-side sandbox constrains what generated code can do.

The pattern still has to remain governed. A `search/execute` portal should not become a bypass around capability governance. It needs the same fields as any other MCP endpoint: owner, allowed upstream servers, scope policy, sandbox profile, output filtering, trace correlation, and review rules for risky writes. Otherwise the team only replaces "too many tools in the prompt" with "too broad a programmable portal."

### 5.8. Tool Surface Design Is Part of the Safety Contract

AWS's practical guidance on MCP tool design adds another layer to the Cloudflare Code Mode pattern: the problem is not only where the gateway sits, but which **tool surface** the agent sees at all.[^aws-mcp-tool-design] If a prompt receives dozens of similar tools, broad schemas, and ambiguous names upfront, the platform gets two failures at once: context bloat and tool confusion. The model may choose the wrong operation, mix fields from neighboring schemas, or use a generic tool as a path around a riskier action.

A good tool-surface contract should therefore record:

- `tool_taxonomy`: read, write, execution, orchestration, introspection;
- `tool_visibility_mode`: eager, lazy, search_then_execute, or server_side_introspection;
- `max_active_tools`: a practical limit on simultaneously visible tools for one step;
- `schema_constraints`: required fields, enums instead of free text, short descriptions, and no hidden policy inside descriptions;
- `argument_budget`: how many parameters the model actually has to hold in active context;
- `agent_as_tool_policy`: when a complex sub-agent is published as one tool instead of exposing every internal operation;
- `tool_evaluation`: tests for wrong-tool selection, schema confusion, unsafe defaults, and noisy catalogs.

The useful heuristic is simple: if a tool cannot be explained as one operation with a narrow schema and a clear risk tier, it may be a workflow, sub-agent, or portal search path rather than a tool. Conversely, if five tools differ only by one non-obvious parameter, the difference probably belongs in an enum, taxonomy, or server-side discovery flow rather than in long descriptions the model has to compare.

For the runtime, this becomes reviewable trace data: which tools were visible, why those tools were disclosed, which taxonomy node or search result activated them, which schema version validated the arguments, and which evaluation pack proves the model does not confuse similar tools. Without that trail, "we have an MCP gateway" still leaves a blind spot: the gateway governs the call, but it does not explain why the model saw that tool surface in the first place.

### 5.9. Ephemeral Sandboxes Are Usually Better Than Permanent Environments

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

## 8. A Capability Contract Must Include More Than Input/Output

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

## 9. Sandbox Execution Should Return Execution Facts, Not Only Output

If the sandbox returns only stdout or a payload, you lose half the value of the isolation layer.

For investigations and control, it is useful to return:

- exit status;
- timeout flag;
- resource usage summary;
- side effect uncertainty;
- redacted logs;
- policy decision id.

Then the execution layer can explain not just "the command failed", but something mature like: "the operation was terminated by timeout after 8 seconds, network was denied, side effect is not confirmed".

### 9.1. Network Egress Deserves Its Own Rule Set

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

### 9.2. The Sandbox Manifest as an Execution Contract

Recent OpenAI Sandbox Agents documentation adds a useful practical shape to this discussion: describe a sandbox not only as a "container" or "isolated environment", but through an explicit `Manifest`, capabilities, permissions, workspace entries, snapshot, and session state.[^openai-sandbox-agents]

That maps cleanly onto the execution contracts in this chapter. A platform needs to answer at least four questions:

- which files, repositories, mounts, and environment values are materialized into the starting workspace;
- which sandbox-native capabilities are available: filesystem, shell, memory, skills, compaction;
- which permissions and `run_as` identity apply to commands, edits, and file reads;
- what happens on continuation: a live `sandbox_session`, serialized `session_state`, or a fresh session from a `snapshot`.

Such a manifest does not replace the policy layer. It makes the execution boundary reviewable: reviewers can see what enters the workspace, what rights the agent receives, and whether the work can be safely resumed or snapshotted.

### 9.3. Brain / hands / session as an isolation contract

Anthropic's Managed Agents architecture states a useful runtime shape for this chapter: `session`, `harness`, and `sandbox/tools` should be treated as separate interfaces, not as one container with magical internal logic.[^anthropic-managed-agents]

- `session` is the append-only log of events, decisions, tool calls, approvals, and results;
- `harness` is the replaceable control loop that calls the model and routes capability requests;
- `hands` are the sandboxes, tools, and adapters that actually read files, touch networks, and create side effects.

That split is useful for scaling, but it is also a security boundary. If the harness hangs, the session should remain readable. If the sandbox dies, the session should not disappear with it. If an operator needs to debug, they should inspect events, profiles, and snapshots, not open a shell inside an environment that also contains user data.

In this chapter's terms, a capability request should pass through a short chain:

```text
capability request → policy → contained execution → telemetry → incident/eval feedback
```

The chain makes containment reviewable: policy chooses the execution profile, hands execute inside the restricted environment, telemetry records the boundary, and assurance/eval loops use the result for the next decision.


## 10. A Simple Capability Dispatch Example

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

## 11. Common Mistakes

The same problems now repeat at two levels: at the individual adapter level, and at the MCP estate level.

The same problems repeat over and over:

- a capability gets more network access than it needs;
- secrets are visible to too many adapters;
- tool results drag raw external payloads into prompts;
- timeouts exist, but side effect uncertainty is not modeled;
- an MCP server was added, but policy and audit never reached it;
- a sandbox exists on paper but does not restrict anything important.

That is why sandboxing cannot be a checkbox feature. It has to be part of execution design.

## 12. What to Do Right Away

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

## 13. What to Do Next

First lock down execution profiles and isolation boundaries, then move to retries, rate limits, and rollback boundaries.

The next natural topic in this part is idempotency, retries, rate limits, and rollback boundaries. After sandboxing and capability contracts, that is what turns the execution model into a production-grade layer.

- [Chapter 8. Execution Model and Tool Catalog](chapter-8.en.md)
- [Chapter 10. Idempotency, Retries, Rate Limits, and Rollback Boundaries](chapter-10.en.md)
- [Part IV. Tools and Execution](index.en.md)
- [Sources](../../appendix/sources.en.md)

[^cloudflare-mcp]: Cloudflare, [Scaling MCP adoption: Our reference architecture for simpler, safer and cheaper enterprise deployments of MCP](https://blog.cloudflare.com/enterprise-mcp/)

[^cloudflare-code-mode]: Cloudflare, [Code Mode: give agents an entire API in 1,000 tokens](https://blog.cloudflare.com/code-mode-mcp/)

[^cloudflare-ai-traffic-controls]: Cloudflare Blog, [Your site, your rules: new AI traffic options for all customers](https://blog.cloudflare.com/content-independence-day-ai-options/)

[^github-copilot-browser-tools]: GitHub Changelog, [Browser tools for GitHub Copilot in VS Code are generally available](https://github.blog/changelog/2026-07-01-browser-tools-for-github-copilot-in-vs-code-are-generally-available/)

[^aws-secure-mcp-access]: AWS Security Blog, [Secure AI agent access patterns to AWS resources using Model Context Protocol](https://aws.amazon.com/blogs/security/secure-ai-agent-access-patterns-to-aws-resources-using-model-context-protocol/)

[^aws-mcp-gateway-registry]: AWS Open Source Blog, [Governing AI Assets at Scale with MCP Gateway and Registry](https://aws.amazon.com/blogs/opensource/governing-ai-assets-at-scale-with-mcp-gateway-and-registry/)

[^google-gemini-enterprise-mcp]: Google Cloud, [Build agents even faster with Gemini Enterprise Agent Platform’s fully-managed, remote MCP server](https://cloud.google.com/blog/products/ai-machine-learning/gemini-enterprise-agent-platform-remote-mcp-server)

[^openai-secure-mcp-tunnel]: OpenAI, [Secure MCP Tunnel](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels) and [Making private MCP servers reachable without making them public](https://developers.openai.com/blog/connect-private-mcp-servers-to-openai-products)

[^aws-stateful-mcp]: [AWS, Introducing stateful MCP client capabilities on Amazon Bedrock AgentCore Runtime](https://aws.amazon.com/blogs/machine-learning/introducing-stateful-mcp-client-capabilities-on-amazon-bedrock-agentcore-runtime/)

[^aws-mcp-tool-design]: AWS Machine Learning Blog, [MCP tool design: practical approaches and tradeoffs](https://aws.amazon.com/blogs/machine-learning/mcp-tool-design-practical-approaches-and-tradeoffs/) and AWS Prescriptive Guidance, [Design tools for AI agents](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/tool-design.html)

[^google-sandbox]: [Google Cloud, Introducing Agent Sandbox](https://cloud.google.com/blog/products/containers-kubernetes/agentic-ai-on-kubernetes-and-gke/)

[^openai-sandbox-agents]: [OpenAI Agents SDK, Sandbox Agents](https://openai.github.io/openai-agents-python/sandbox_agents/), [Sandbox Concepts](https://openai.github.io/openai-agents-python/sandbox/guide/), [Sandbox clients](https://openai.github.io/openai-agents-python/sandbox/clients/), and [Agent memory](https://openai.github.io/openai-agents-python/sandbox/memory/)

[^microsoft-autojack]: Microsoft Security Blog, [AutoJack: How a single page can RCE the host running your AI agent](https://www.microsoft.com/en-us/security/blog/2026/06/18/autojack-single-page-rce-host-running-ai-agent/)
[^microsoft-prompts-shells]: Microsoft Security Blog, [When prompts become shells: RCE vulnerabilities in AI agent frameworks](https://www.microsoft.com/en-us/security/blog/2026/05/07/prompts-become-shells-rce-vulnerabilities-ai-agent-frameworks/)
[^microsoft-tools-acting]: Microsoft Security Blog, [Securing AI agents: When AI tools move from reading to acting](https://www.microsoft.com/en-us/security/blog/2026/06/30/securing-ai-agents-ai-tools-move-from-reading-acting/)
[^google-adk-static-prompts]: Google Cloud, [Beyond Static Prompts: Building Scale-Proof, Polymorphic Multi-Agent Systems with Google's ADK](https://cloud.google.com/blog/topics/developers-practitioners/beyond-static-prompts-with-google-adk)
