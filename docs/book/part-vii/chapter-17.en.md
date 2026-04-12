# Chapter 17. Policy Layer and Capability Catalog

!!! info "How to read this chapter"
    It helps to keep one practical question in mind rather than an abstract policy topic:

    - who decides whether the same support agent may start this run at all;
    - who decides whether it may read context, open a ticket, or write into memory;
    - where those decisions should live so they do not dissolve into orchestration code.

    If those answers are hidden in random code paths, the runtime exists, but the contract core of the system is still missing.

## 1. Why a Reference Runtime Is Still Too Naive Without a Policy Layer

Even if you already have a clean runtime loop, that is still not enough. Without an explicit policy layer, the system remains too trusting:

In the running support case, this appears immediately after Chapter 16. The runtime can already accept a request, assemble context, call the model, and reach the gateway. But the moment the agent is about to open an urgent ticket, write a summary into memory, or request another external step, the system needs more than a loop. It needs an explicit decision about admissibility and risk.

- you cannot reliably distinguish allowed runs from forbidden ones;
- tool calls are hard to control consistently;
- memory writes live on scattered conventions;
- product-specific restrictions leak into orchestration code very quickly.

That is why the next mandatory layer in the reference implementation is the policy layer.

Its job is not to "slow the system down". Its job is to make decisions about access, risk, and admissibility explicit instead of scattering them across random `if` branches.

!!! info "Need the contract layer?"
    For the more applied view, open the [Policy Bundle Schema and Approval Contract](../../appendix/policy-bundle-schema.en.md), the [Approval Request and Decision Record Schema](../../appendix/approval-schema.en.md), and the [Reference Package](../../appendix/reference-package.en.md).

## 2. A Policy Layer Should Answer Small and Clear Questions

A weak policy layer tries to become "the smart brain of the system". A strong policy layer does the opposite: it solves a limited set of clear questions.

For example:

- can this run start at all;
- can this context be read;
- can this capability be invoked;
- is approval required;
- can this be written into memory;
- can this result be returned outward.

When those questions are explicit, the runtime becomes easier to explain, and guardrail changes stop being chaotic.

## 3. A Capability Catalog Is Not Just a Registry of Names

It is very easy to slide into a catalog that only stores a list of available tools. A good catalog does more:

- it describes the capability contract;
- stores the risk profile;
- declares transport and execution mode;
- captures idempotency expectations;
- records ownership and lifecycle.

So the capability catalog is not "inventory for convenience". It is the central control point for platform capabilities.

<div class="diagram-card">
<p>Together, the policy layer and the capability catalog form the contract core of the reference implementation</p>

``` mermaid
flowchart LR
    A["Run request"] --> B["Runtime orchestrator"]
    B --> C["Policy layer"]
    B --> D["Capability catalog"]
    C --> E["Allow / deny / approve"]
    D --> F["Capability contract"]
    E --> G["Execution layer"]
    F --> G
```

</div>

## 4. What Is Worth Storing in a Capability Catalog

A practical field set usually looks like this:

- capability name;
- owner;
- mode: read / write / high_risk;
- transport: mcp / gateway / sandboxed_exec;
- input schema;
- output shape;
- approval requirement;
- idempotency requirement;
- timeout and retry defaults.

With that contract, the runtime can already behave predictably instead of adapting ad hoc to every capability.

## 5. A Policy Decision Should Be an Object, Not Just a Bool

A very useful engineering habit: do not reduce policy decisions to `True/False`.

It is often much more useful to return something like:

- `allow`
- `deny`
- `approval_required`
- `sanitize_and_continue`
- `escalate`

And additionally:

- reason code;
- policy id;
- risk class;
- optional constraints.

That greatly improves explainability and makes telemetry far more useful.

## 6. Example Policy Contract

Here is a very simple but practical template:

```yaml
policy:
  run_precheck:
    require_tenant: true
    deny_if_principal_missing: true
  capabilities:
    search_docs:
      decision: allow
    create_ticket:
      decision: approval_required
      approver: manager
    run_shell:
      decision: deny
  memory_write:
    allow_kinds:
      - validated_fact
      - session_summary
```

Its power is not completeness. Its power is explicitness. You can argue about a specific rule and understand where it applies.

## 7. Example Capability Catalog Contract

It helps to think about the catalog roughly like this:

```yaml
capabilities:
  search_docs:
    owner: knowledge_platform
    mode: read
    transport: mcp
    timeout_seconds: 5
    approval: none
  create_ticket:
    owner: support_platform
    mode: write
    transport: gateway
    timeout_seconds: 15
    approval: manager
    idempotency_key_required: true
  run_shell:
    owner: platform_runtime
    mode: high_risk
    transport: sandboxed_exec
    timeout_seconds: 10
    approval: always
```

That kind of catalog already defines operational semantics, not just names.

## 8. A Simple Policy Decision Skeleton

The point here is that the runtime receives not only permission, but a structured decision.

```python
from dataclasses import dataclass


@dataclass
class PolicyDecision:
    action: str
    reason: str
    policy_id: str


def evaluate_capability(name: str) -> PolicyDecision:
    if name == "search_docs":
        return PolicyDecision(action="allow", reason="low_risk_read", policy_id="cap_001")
    if name == "create_ticket":
        return PolicyDecision(action="approval_required", reason="write_action", policy_id="cap_014")
    return PolicyDecision(action="deny", reason="unsupported_capability", policy_id="cap_999")
```

Even code this small already gives the right shape for telemetry, approval UI flows, and investigations.

## 9. A Simple Capability Lookup Skeleton

And one more practical piece: the runtime should not know capability details directly, it should fetch them from the catalog.

```python
from dataclasses import dataclass


@dataclass
class CapabilitySpec:
    name: str
    mode: str
    transport: str
    timeout_seconds: int


def get_capability(name: str) -> CapabilitySpec | None:
    registry = {
        "search_docs": CapabilitySpec("search_docs", "read", "mcp", 5),
        "create_ticket": CapabilitySpec("create_ticket", "write", "gateway", 15),
    }
    return registry.get(name)
```

This also looks boring. Good. The catalog layer should be boring, stable, and inspectable.

## 10. Common Mistakes

These problems are very typical:

- policy rules are scattered across runtime code;
- the capability contract is incomplete;
- capability ownership is unclear;
- approval logic is embedded directly into orchestration;
- memory policy and execution policy behave as if they were unrelated;
- the catalog and real adapters drift apart in behavior.

When that happens, the reference implementation stops being a reference and becomes a bundle of conventions again.

## 11. What to Do Right Away

Start with this short list and mark every "no" explicitly:

- Do you have a separate policy layer instead of a pile of `if` branches?
- Does policy return a structured decision?
- Is there a single capability catalog?
- Do capabilities have owner, transport, and risk semantics?
- Does the runtime use the catalog rather than direct calls?
- Are policy decisions visible in telemetry?

If the answer is "no" several times in a row, the skeleton exists, but the contract core is not assembled yet.

## 12. What to Do Next

First make policy decisions and capability contracts explicit, then check whether that same system is ready for its first rollout.

The next logical step in the reference implementation is to assemble a production rollout checklist, so you move from blueprint and contract core into a practical go-live framework.

- [Chapter 16. Baseline Runtime Blueprint](chapter-16.en.md)
- [Chapter 18. Production Rollout Checklist](chapter-18.en.md)
- [Part VII. Reference Implementation](index.en.md)
- [Sources](../../appendix/sources.en.md)

## 13. Useful Reference Pages

- [Policy Bundle Schema and Approval Contract](../../appendix/policy-bundle-schema.en.md)
- [Lifecycle Artifact Schema](../../appendix/lifecycle-artifact-schema.en.md)
- [Reference Package](../../appendix/reference-package.en.md)

- [Chapter 16. Baseline Runtime Blueprint](chapter-16.en.md)
- [Chapter 18. Production Rollout Checklist](chapter-18.en.md)
- [Part VII. Reference Implementation](index.en.md)
- [Sources](../../appendix/sources.en.md)
