# Policy Bundle Schema and Approval Contract

This page connects several topics already covered in the book:

- [Chapter 4. Tool Gateway, Approval, and Audit Trail](../book/part-ii/chapter-4.en.md)
- [Chapter 17. Policy Layer and Capability Catalog](../book/part-vii/chapter-17.en.md)
- [Chapter 20. Change Management for Agent Systems](../book/part-viii/chapter-20.en.md)
- [Evidence Spine: From Request to Rollout Judgment](../book/part-v/evidence-spine.en.md)

And it is grounded in the runnable package:

- [Reference Package](reference-package.en.md)

If the trace schema and eval schema pages answer:

- how to describe actual behavior;
- how to describe expected behavior;

then this page answers the third question:

- how to describe the governing rules that stand between reasoning and side effects.

## Why a policy bundle should be treated as an artifact

One of the most common mistakes in agent systems looks like this:

- policy rules partly live in prompts;
- partly in gateway code;
- partly in an approval UI;
- partly in the team’s memory.

That may work while the system is small. But as soon as change management, audit, and staged rollout appear, the policy layer becomes too blurry.

That is why it is useful to package a `policy bundle` as a first-class artifact.

## Proposed extension: credential-to-identity binding

Motivation: [LangChain Connections](https://www.langchain.com/blog/connections-managed-credentials-and-per-caller-identity-for-managed-deep-agents). This is a proposed internal contract, not new OAuth fields or an implemented reference-runtime resolver. `credential_owner` (`agent` or `user`) is independent of `credential_type` (`secret` or `oauth`).

Include non-secret references `connection_ref`, `credential_ref`, `deployment_ref`, `tenant_ref`, `requester_principal_ref`, `effective_principal_ref`, plus `credential_owner`, `credential_type`, `policy_version`, and `authorization_checked_at` in policy evidence. Derive the requester from verified inbound context and the effective principal from a trusted provider binding; the model cannot assign either through tool arguments. For user-owned credentials, the resolver must verify ownership by the current user and tenant. If the effective principal is unknown, block operations requiring that binding. Keep secret values and tokens out of traces, prompts, and cache keys.

Acceptance scenarios for a future implementation:

1. Preserve all four owner/type combinations without inferring ownership from OAuth; agent-owned OAuth remains a shared identity.
2. Users A and B call the same connection: neither A's private results nor credentials reach B; reject a tool-argument `user_id` substitution.
3. Missing user grant: do not execute the dependent operation or fall back to a shared credential. Access consent does not replace action approval.
4. Caller/tenant changes or access is revoked during a pause: do not reuse the old credential, cache, or allow decision without revalidation.
5. An explicit policy permits a shared account: audit records requester and effective principal separately, with no credential values in evidence.


## Proposed extension: partial OAuth grants

This is a production contract proposal, not a claim that the reference runtime implements these fields. Motivation: [Cloudflare, From all-or-nothing to task-based OAuth consent](https://blog.cloudflare.com/task-based-oauth-consent/). The fields below are internal policy evidence, not new standard OAuth fields.

- `requested_scopes`: scopes of the specific authorization request.
- `granted_scopes`: the actual set from a verified authorization-server response or another trusted provider mechanism; neither a guess from the request nor an assumption that every token is a JWT.
- `required_scopes`: minimum permissions for the selected operation, not mandatory consent-UI scopes.
- `missing_scopes`: required minus granted; a nonempty set blocks the operation before side effects.
- `grant_ref`, `authorization_checked_at`: a non-secret grant reference and check time; together with subject, task, tool, resource, and policy version they make the decision reviewable. Never log the token itself.

Illustrative example (scope names and evidence fields are not standardized):

```yaml
oauth_scope_evidence:
  grant_ref: grant-42
  authorization_checked_at: "2026-09-08T00:00:00Z"
  requested_scopes: [tickets.read, tickets.write]
  granted_scopes: [tickets.read]
  required_scopes: [tickets.write]
  missing_scopes: [tickets.write]
  decision: deny
  reason: insufficient_granted_scope
```

Scope checking does not replace resource/audience/expiry validation, current policy, or separate action approval. If the grant cannot be established reliably, stop the sensitive operation; never substitute requested for granted. Refresh/resume requires current authorization context, and the downstream service retains its own authorization checks.

Acceptance scenarios for this proposed contract:

1. Read-only grant: produce an independently permitted summary, never invoke the write tool, and label the outcome partial.
2. A missing scope is essential to the task: stop with an explicit reason, without retries, credential substitution, or hidden access expansion.
3. Scope present but resource or task outside policy: deny; a broad grant cannot override task-scoped authority.
4. Write permission disappears after refresh/resume: do not reuse the old allow decision.
5. Unknown grant or complete consent refusal: never execute based on requested scopes. Action approval cannot substitute for the grant.

## Proposed extension: MCP catalog cache

This is an internal contract proposal, not an implemented `agent_runtime_ref` feature or a ready-to-use FastMCP configuration. `ttlMs` and `cacheScope` are server hints documented by FastMCP; the other fields below propose normalized evidence. Sources: [LangChain: MCP in LangChain](https://www.langchain.com/blog/mcp-in-langchain-stateless-protocol-elicitation-and-more) / [FastMCP: Response caching](https://gofastmcp.com/clients/client#response-caching).

```yaml
catalog_cache_evidence:
  target_id: support-mcp-prod
  protocol_version: "2026-07-28"
  request_fingerprint: tools-list-page-1
  partition_ref: verified-tenant-a-principal-7-authz-v3
  policy_version: support-policy-v8
  server_ttl_ms: 60000          # ttlMs
  server_cache_scope: public   # cacheScope
  local_max_ttl_ms: 30000
  effective_ttl_ms: 30000
  fetched_at: "2026-09-08T07:00:00Z"
  expires_at: "2026-09-08T07:00:30Z"
  catalog_digest_ref: catalog-snapshot-42
  cache_hit: true
  authorization_decision_ref: fresh-tool-call-decision-43
```

Derive `partition_ref` from verified tenant/principal and access context; keep secrets and tokens out of keys and logs. `target_id` must uniquely identify the server; `request_fingerprint` identifies the listing method and parameters, including a page or filter. Example strings are illustrative. `server_cache_scope` records the received `cacheScope` without widening its meaning. Local policy can retain stricter isolation even for `public` responses.

TTL bounds snapshot reuse: effective lifetime must not exceed server `ttlMs` or the local cap. Zero TTL permits no reuse; for missing or invalid hints this conservative contract requires a network read without cache reuse. That is local policy, not a claim about every SDK default. If an expired catalog cannot be refreshed, do not turn the stale snapshot into authority for a sensitive invocation. In FastMCP, `refresh` fetches and updates the cache; `bypass` neither serves nor stores a cached response.

Acceptance scenarios for the proposed contract:

1. Two users in one tenant with different permissions: the first catalog never serves the second. Sharing requires both server-marked `public` and permitting local policy.
2. Permission revoked before TTL expires: current authorization denies invocation; a cache hit cannot reuse an old allow, and authorization-dependent visibility is invalidated.
3. Definition change detected: refresh and recheck schema, risk, and approval; never automatically carry old approval onto a different contract.
4. Expired, zero, or invalid TTL: network read; server unavailability cannot authorize bypassing checks.
5. Principal, grant, or policy-version change: a different partition or invalidation; neither metadata nor access decisions cross context boundaries.

## Proposed extension: compound resource authorization

This is a proposed internal contract, not a ready-to-use Cloudflare configuration or an implemented `agent_runtime_ref` feature. Operation names and identifiers below are illustrative; the access distinctions come from [Workers roles](https://developers.cloudflare.com/workers/authorization/).

```yaml
compound_authorization_evidence:
  principal_ref: verified-ci-principal
  task_ref: approved-route-change
  plan_ref: immutable-plan-42
  policy_version: deploy-policy-v3
  requirements:
    - action: worker.update
      resource_ref: account-a/worker-a
      required_access: Editor
      decision: allow
    - action: route.write
      resource_ref: account-a/zone-a
      required_access: Workers Routes Write
      decision: deny
  decision: deny
  reason: missing_zone_route_permission
```

The adapter derives `requirements` from canonical account, Worker, and affected-zone identifiers, including both old and new zones when moving a route. A model-supplied list is not evidence of completeness. Every check uses current verified authority for the same principal; aggregate `allow` requires **all** checks to pass, task-scope compliance, and separate approval where required. `unknown`, unavailable checks, or any `deny` block the compound change. Audit records retain reasons and non-secret evidence references, never tokens.

Preflight does not create a transaction across APIs. Check the full plan before the first mutation; recheck authority and targets immediately before individual calls and after pauses, while the service retains its own authorization. A changed plan needs a new decision and, where necessary, approval. If authority is revoked after some calls, stop further mutations and reconcile actual effects; record the partial outcome and authorize recovery separately. Never promise automatic rollback or broaden credentials to finish.

Proposed checks (not results of executed Cloudflare calls):

1. Access is scoped to Worker A: reading or changing Worker B is denied even for the same operation name.
2. `Metadata Read-Only` permits A's telemetry, not code reads; `Content Read-Only` does not permit deployment.
3. `Editor` permits an in-policy update of existing A, not deletion or creation of a new Worker.
4. Deployment without route changes needs no zone permission; adding, changing, or removing a route without `Workers Routes Write` on any affected zone is blocked before mutation.
5. All compound-operation permissions are present: only the verified plan within task scope can be allowed. Substituting a zone after approval requires a new check.
6. Revocation between steps denies the next step; completed effects are recorded as partial, not complete success or guaranteed rollback.

## What a policy bundle is

Here, it is useful to define a `policy bundle` as a related set of rules that ships together:

- runtime policy;
- tool policy;
- approval policy;
- runtime-control rules for pause/resume and background paths;
- memory write rules;
- escalation rules;
- egress rules;
- trusted verifier-contract expectations for high-risk eval and rollout evidence.

The point is not that everything must live in one YAML file. The point is that the bundle should be:

- versioned;
- reviewable;
- traceable;
- releasable.

!!! note "Canonical policy cases"
    A policy bundle should not look identical across the three canonical cases. **Support triage** needs write-capability approval policy, idempotency evidence, and duplicate-ticket recovery controls. **Internal knowledge assistant** needs retrieval policy, memory write rules, freshness checks, access control, and knowledge provenance. **Incident coordination** needs escalation rules, notification side effects, response ownership, and post-incident learning gates.

## Minimal policy bundle structure

A minimally useful bundle can look like this:

```yaml
bundle:
  bundle_id: policy-support-triage-2026-04-07
  version: 2026.04.07
  owner_team: platform-safety
  applies_to:
    agent_ids: ["support-triage-ref"]
  artifacts:
    - policy.yaml
    - approvals.yaml
    - controls.yaml
  contract_version: capability-contract-v3
  release_identity: release-support-triage-2026-04-07-canary
```

This is not yet the rules themselves. It is the envelope that answers:

"What exactly do we currently treat as the policy artifact for this agent system?"

And once release-bearing governance matters, it should also answer:

"Which release identity is this bundle helping define?"

## Why the approval contract should not hide inside prose

Approval logic is often described only in words:

- “high-risk actions need confirmation”;
- “manager approves ticket creation”;
- “security signs off on dangerous actions”.

That is not enough.

It is useful to make the approval contract explicit:

- who may approve;
- which action class requires approval;
- which fields must appear in the approval request;
- which decisions are allowed;
- what happens after rejection;
- whether a run may pause, resume, expire, or cancel;
- what must remain in the audit trail.

## Example approval contract

Here is a workable skeleton:

```yaml
approval_contract:
  capability: create_ticket
  risk_tier: high
  bundle_version: 2026.04.07
  release_identity: release-support-triage-2026-04-07-canary
  required_reviewers:
    - manager
  request_fields:
    - trace_id
    - session_id
    - idempotency_key
    - requested_by
    - reason
    - tool_arguments_redacted
  allowed_decisions:
    - approved
    - rejected
  runtime_controls:
    pause_allowed: true
    max_wait_seconds: 1800
    on_expiry: cancel_run
  on_reject: stop_run
```

The point is simple: approval should be a machine-readable operational contract, not just a checkbox in a UI. And when approvals are release-bearing, that contract should also make clear which bundle version and release identity the human decision belonged to.

!!! example "Policy contract for the duplicate-ticket thread"
    For support-triage, the `create_ticket` contract should require `idempotency_key` in the approval request, not only during tool execution. Then the human, gateway, and trace see the same write intent, the policy bundle can forbid retry without reconciliation on `side_effect_unknown`, and rollout review checks a governed capability rather than a loose tool call.

## How the policy bundle connects to the lifecycle

From Part VIII, two ideas matter most here:

- policy changes are release-bearing changes;
- the policy bundle should participate in change management as a full artifact.

That means the team should answer not only:

"What policy do we have in general?"

but also:

"Which exact policy bundle version was active during this rollout or incident?"

And once the runtime treats bundles as governed release surfaces, the next question becomes unavoidable too:

"Which release identity did this policy bundle participate in?"

## How the policy bundle connects to traces

The connection is very practical:

- the trace shows which policy decision actually fired;
- the policy bundle shows where that decision came from;
- the approval contract shows what the human gate should have looked like;
- release identity tells the investigator which governed release surface that decision belonged to.

Without that quartet, investigation quickly turns into guesswork.

## What the reference runtime already supports

In `agent_runtime_ref`, there are already:

- [policy.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/policy.yaml)
- [approvals.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/approvals.yaml)
- [controls.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/controls.yaml)
- [change.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/change.yaml)
- [runtime-controls.yaml](https://github.com/agent-axiom/agent-arch/blob/main/agent_runtime_ref/configs/runtime-controls.yaml)

So the package already lives in a model where policy, approvals, and runtime-control contracts are not “secondary settings”, but governed artifacts tied to concrete bundle versions and release-bearing control surfaces. The executable `check-controls` gate makes the control bundle reviewable too: it returns `healthy`, `required_controls`, `blocked_findings_expected`, `missing_controls`, `failed_run_controls`, `preserved_failed_run_controls`, `failed_run_controls_healthy`, `support_duplicate_controls`, `preserved_support_duplicate_controls`, `support_duplicate_controls_healthy`, `blocking_findings`, and `inventory_drift`, whose nested fields `has_drift`, `missing_from_catalog`, and `missing_from_inventory` separate policy/control failures from capability inventory drift.

The same gate keeps the control-bundle input shape explicit: controls config validation reports `Controls policy config must be a mapping`, `'controls' must be a mapping`, `'controls.require' must be a list`, `'controls.block_if' must be a list`, `controls.require entries must be strings`, `controls.require entries must not be empty`, `controls.require entries must be unique`, `controls.block_if entries must be strings`, `controls.block_if entries must not be empty`, and `controls.block_if entries must be unique`; signal overrides report `Assessment signals must be a mapping`, `Assessment signal key must be a string`, `Assessment signal key must not be empty`, `Assessment signal keys must be unique`, and `Assessment signal value must be a boolean: {field}`. That means an operator can distinguish a malformed policy bundle from a failing but well-formed control assessment.

## What a production schema should add

As stateful MCP and resumable capability sessions enter the runtime, the policy bundle also needs to describe how those sessions are governed, not just whether a capability is allowed in principle.

Useful additions now include:

- `trusted_verifier_contracts`
- `verifier_contract_required_for_high_risk`
- `on_untrusted_verifier_contract`
- `capability_session_mode`
- `resume_policy`
- `on_session_expiry`
- `progress_event_policy`
- `elicitation_policy`
- `reinit_requires_approval`
- `approval_mode`
- `approval_delegate`
- `classifier_verdict_policy`
- `escalate_to_human_if`
- `subagent_handoff_policy`
- `authorization_mode`
- `delegated_principal_policy`
- `token_reuse_policy`
- `on_authorization_revoke`
- `mcp_discovery_source`
- `mcp_server_owner`
- `mcp_auth_mode`
- `shadow_mcp_handling`

That prevents a policy bundle from approving a capability statically while leaving the live session lifecycle uncontrolled.

Microsoft Foundry's Open Trust Stack is useful here as an external reference point: policy should compile into named runtime checkpoints instead of remaining prose beside an eval report.[^microsoft-open-trust-stack] In portable YAML, that can look like this:

```yaml
control_checkpoints:
  - checkpoint: tool_execution
    policy_requirement: no_external_write_without_approval
    predicate: risk_tier == "high" and side_effect == "external_write"
    action: require_approval
    audit_fields:
      - checkpoint
      - policy_requirement
      - predicate_result
      - action
      - control_version
      - eval_case_id
      - trace_id
```

The minimal contract surface is: `checkpoint`, `policy_requirement`, `predicate` or `judge`, `action`, `control_version`, `eval_case_id`, `trace_id`, and `observed_signal`. Checkpoints should be named by the places in the agent cycle: `input`, `llm`, `state`, `tool_execution`, and `output`. Then a failed eval can connect not only to a prompt diff, but also to a specific runtime hook, audit event, and regression case.

Anthropic's workflow taxonomy adds another useful contract dimension here.[^anthropic] Mature policy bundles increasingly need to state not only whether a capability is allowed, but which orchestration patterns it is allowed to participate in.

Useful additions now include fields such as:

- `allowed_orchestration_patterns`
- `disallowed_orchestration_patterns`
- `worker_inheritance_policy`
- `worker_capability_subset`
- `review_required_before_worker_write`

Those fields help the governed contract answer questions like:

- whether a capability may run inside `prompt chaining`, `routing`, or `parallelization`;
- whether delegated workers in `orchestrator-workers` inherit approval or delegated authorization context;
- whether a worker may request additional capabilities or only use a constrained subset;
- whether worker output must be reviewed before any write-capability is exercised.

It also helps prevent a second drift: delegated approval paths that exist in product behavior, but are not actually represented in the governed contract.

As soon as the system grows up, it is useful to add at least:

- `bundle_version`
- `artifact_lineage`
- `change_id`
- `release_identity`
- `approval_contracts`
- `runtime_control_schema`
- `sandbox_profile_contract`
- `sandbox_profile_review_required`
- `contract_version`
- `deprecated_rules`
- `redaction_policy`

If a capability can run on a sandbox-backed path, the policy bundle should also point to the sandbox profile contract or explicitly require its review; otherwise workspace, shell/filesystem permissions, and snapshot/resume behavior stay outside release identity.

That turns the policy layer from a set of files into a real release surface.

## Why the policy bundle and capability catalog should not drift apart

There is a bad extreme where the policy bundle lives separately, the capability catalog lives separately, and approval rules live separately, with weak links between them.

Then problems appear quickly:

- a capability exists in the catalog, but has no approval contract;
- policy refers to a capability name that no longer exists;
- audit sees a decision, but cannot connect it to a bundle version.

So the practical rule is simple:

- the capability catalog describes what the system can do;
- the policy bundle describes how, under which conditions, and in which orchestration patterns that capability may be used;
- the approval contract describes where reasoning must stop and hand control to a human;
- the authorization contract describes under whose identity and delegated scope the action may execute;
- the MCP governance contract describes whether the capability came from an approved registry, who owns the MCP server, which auth mode protects it, and what happens when a shadow MCP path is discovered;
- the verifier contract policy describes which verifier contracts may be trusted for high-risk grading, rollout evidence, or assurance decisions.

The reference runtime makes that join concrete in `capabilities.yaml` and `policy.yaml`: capability entries carry `tool_principal`, `risk_tier`, `network_access`, `allowed_egress`, `timeout_seconds`, and `idempotency_key_required`, while policy entries carry `run_precheck`, `require_tenant`, `deny_if_principal_missing`, capability decisions for `search_docs`, `create_ticket`, and `run_shell`, memory-write `allow_kinds` (`validated_fact` and `session_summary`), and execution-level `allow_network_access`. The policy loader validates this structure explicitly: `Policy config must be a mapping`, `'policy' must be a mapping`, `'run_precheck' must be a mapping`, `'run_precheck.require_tenant' must be a boolean`, `'run_precheck.deny_if_principal_missing' must be a boolean`, `'{label}' must be a boolean`, `'memory_write' must be a mapping`, `'allow_kinds' must be a list`, `memory_write.allow_kinds entries must be strings`, `memory_write.allow_kinds entries must not be empty`, `memory_write.allow_kinds entries must be unique`, `'execution' must be a mapping`, `'allow_network_access' must be a list`, `execution.allow_network_access entries must be strings`, `execution.allow_network_access entries must not be empty`, `execution.allow_network_access entries must be unique`, `Policy capability names must be strings`, `Policy capability name must not be empty`, `Policy capability names must be unique`, `Policy capability entries must be CapabilityPolicy`, `Policy precheck request must be RunRequest`, `Policy context must be RunContext`, `Policy tool request must be ToolRequest`, `Policy capability must be CapabilitySpec`, `'capabilities' must be a mapping`, `Policy action must be a string`, `Policy action is not supported: {action}`, `Policy field must be a string: {field}`, `Policy field is required: {field}`, `Policy decision must be a string`, `Policy decision is not supported: {decision}`, `Policy approver must be a string`, `Policy approver must not be empty: {capability_name}`, `Policy memory kind must be a string`, `Policy memory kind must not be empty`, and `Policy for capability {name!r} must be a mapping`.

## What to Do Right Away

Start with this short list and mark every "no" explicitly:

- Do you have a versioned policy bundle?
- Can you connect the bundle to rollout and incident review?
- Is the approval contract machine-readable, or only described in prose?
- Is it clear which fields an approval request must contain?
- Is there a stable link between the policy bundle and the capability catalog?
- Can you tell which policy version and release identity were active for a given trace?
- Is it explicit which verifier contracts are trusted for high-risk grading or rollout evidence?

If several answers are “no,” your policy layer exists, but is not yet shaped as a full operational artifact.

## What to Do Next

- [Trace Schema and Event Catalog](trace-schema.en.md)
- [Eval Dataset Schema and Grading Contract](eval-schema.en.md)
- [Lifecycle Artifact Schema](lifecycle-artifact-schema.en.md)
- [Reference Package](reference-package.en.md)
- [Policy Templates and Checklists by Use Case](policy-templates.en.md)

[^anthropic]: [Anthropic, Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
[^microsoft-open-trust-stack]: Microsoft Foundry Blog, [Build agents you can trust across any framework with open evals and a control standard](https://devblogs.microsoft.com/foundry/build-2026-open-trust-stack-ai-agents/).
