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

## 4. A Tool Surface Is Not the Same Thing as a Governed Capability Surface

Recent OpenAI tooling guidance is useful because it makes a distinction many teams blur in practice: a model may see tools, MCP servers, hosted capabilities, or local functions, but the runtime still has to decide what kind of control surface those things belong to.[^openai-tools]

That distinction matters.

A weak implementation says:

- here is a list of tools the model can call.

A stronger implementation says:

- here is the governed capability surface;
- here is which part of it is exposed to the model;
- here is which transport carries execution;
- here is which capabilities are callable directly, which are brokered through a gateway, and which are not exposed at all.

This is why a capability catalog should sit above raw tool definitions. It prevents the runtime from confusing:

- what the model can mention;
- what the runtime can route;
- what the platform is actually willing to execute.

## 5. What Is Worth Storing in a Capability Catalog

Once the platform accepts stateful MCP-style capabilities, the catalog also has to describe more than transport and risk. It should help the runtime know whether a capability is sessionless, session-bound, interruptible, or resumable across multiple turns.

That means a mature catalog may also need fields such as:

- capability session mode: `stateless / stateful`;
- whether elicitation is allowed;
- whether progress events are emitted;
- session expiry behavior;
- whether resume requires a fresh approval or may continue under the existing decision;
- whether the capability may reinitialize its remote session automatically.

Without those fields, the policy layer can approve a capability in principle but still fail to govern how its live runtime session behaves in practice.

A practical field set usually looks like this:

- capability name;
- owner;
- mode: read / write / high_risk;
- transport: mcp / gateway / sandboxed_exec;
- exposure: direct / brokered / restricted;
- input schema;
- output shape;
- approval requirement;
- idempotency requirement;
- timeout and retry defaults.

With that contract, the runtime can already behave predictably instead of adapting ad hoc to every capability.

## 6. Approval Should Look Like an Interruptible Runtime Path, Not a Side Conversation

A policy layer becomes much more real when approval is modeled as part of runtime control flow rather than as a manual process outside the system. LangGraph's interrupt model is useful here because it makes pause, review, and resume explicit runtime primitives instead of ad hoc human workarounds.[^langgraph-interrupts]

That is the right shape for policy-heavy agent systems too.

When a high-risk capability reaches an approval boundary, the runtime should be able to:

- pause the run;
- surface the pending action and its context;
- wait for an external decision;
- resume with a structured outcome.

That is much stronger than sending a message to an operator and hoping the surrounding code still remembers what it was doing.

A useful next step is to distinguish two approval patterns:

- direct human approval for rare or very high-risk actions;
- classifier-mediated approval paths for repetitive low-context decisions where manual review causes approval fatigue.

That second path should not be treated as “approval removed.” It should be treated as delegated control with stricter evidence requirements:

- what classifier or gate made the decision;
- what evidence was visible to it;
- when it must escalate to a human;
- how subagent or follow-on actions inherit or lose that delegated approval.

## 7. A Policy Decision Should Be an Object, Not Just a Bool

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
- optional constraints;
- optional approval or resume requirements.

That greatly improves explainability and makes telemetry far more useful.

## 8. Example Policy Contract

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

## 9. Example Capability Catalog Contract

It helps to think about the catalog roughly like this:

```yaml
capabilities:
  search_docs:
    owner: knowledge_platform
    mode: read
    transport: mcp
    exposure: direct
    timeout_seconds: 5
    approval: none
  create_ticket:
    owner: support_platform
    mode: write
    transport: gateway
    exposure: brokered
    timeout_seconds: 15
    approval: manager
    idempotency_key_required: true
  run_shell:
    owner: platform_runtime
    mode: high_risk
    transport: sandboxed_exec
    exposure: restricted
    timeout_seconds: 10
    approval: always
```

That kind of catalog already defines operational semantics, not just names. It also makes explicit whether a capability is model-facing, runtime-brokered, or operator-only.

## 10. Structured Outputs Matter Because Contracts Should Survive Contact With Code

Stateful capability flows make this even more important. If approval, pause/resume, session expiry, and re-init decisions are all encoded only in prose, the runtime cannot safely decide whether it is continuing the same governed session or accidentally opening a new one.

That is why policy artifacts should increasingly capture structured fields like:

- `capability_session_id`
- `capability_session_mode`
- `resume_policy`
- `on_session_expiry`
- `progress_event_policy`
- `elicitation_policy`

Those fields help the runtime keep approval control and capability session control aligned instead of letting them drift into separate implicit systems.

As approval systems mature, the contract may also need fields for classifier-backed approval control, such as:

- `approval_mode`
- `approval_delegate`
- `classifier_verdict`
- `escalate_to_human_if`
- `subagent_handoff_policy`

Those additions help the runtime represent a delegated approval path explicitly instead of hiding it in product logic or UI behavior.

The same discipline should hold across the identity boundary too. If a capability uses delegated user authorization through MCP or another brokered transport, the policy layer should be able to state whether:

- access is platform-owned or user-delegated;
- delegated scopes may be reused across a paused run;
- revoked authorization forces cancel, re-approval, or re-initialization;
- subagents are allowed to inherit the same delegated authorization context.

That keeps delegated approval and delegated authorization inside one governed contract model instead of letting them evolve as unrelated exceptions.

Recent OpenAI guidance on structured outputs is useful for the policy layer too.[^openai-structured]

A contract is only half real if the runtime still has to guess whether a policy result, approval request, or capability payload came back in the expected shape.

That is why policy-heavy systems benefit from making key artifacts structurally explicit:

- policy decisions;
- approval requests;
- approval outcomes;
- capability inputs and outputs.

The goal is not elegance for its own sake. The goal is to reduce silent drift between runtime logic, audit records, and the surrounding control surface.

## 11. A Simple Policy Decision Skeleton

The point here is that the runtime receives not only permission, but a structured decision.

```python
from dataclasses import dataclass


@dataclass
class PolicyDecision:
    action: str
    reason: str
    policy_id: str
    approval_mode: str = "human"
    escalate_to_human: bool = False
    requires_approval: bool = False


def evaluate_capability(name: str) -> PolicyDecision:
    if name == "search_docs":
        return PolicyDecision(action="allow", reason="low_risk_read", policy_id="cap_001")
    if name == "create_ticket":
        return PolicyDecision(action="approval_required", reason="write_action", policy_id="cap_014", requires_approval=True)
    return PolicyDecision(action="deny", reason="unsupported_capability", policy_id="cap_999")
```

Even code this small already gives the right shape for telemetry, approval UI flows, and investigations.

## 12. A Simple Capability Lookup Skeleton

And one more practical piece: the runtime should not know capability details directly, it should fetch them from the catalog.

```python
from dataclasses import dataclass


@dataclass
class CapabilitySpec:
    name: str
    mode: str
    transport: str
    exposure: str
    timeout_seconds: int


def get_capability(name: str) -> CapabilitySpec | None:
    registry = {
        "search_docs": CapabilitySpec("search_docs", "read", "mcp", "direct", 5),
        "create_ticket": CapabilitySpec("create_ticket", "write", "gateway", "brokered", 15),
    }
    return registry.get(name)
```

This also looks boring. Good. The catalog layer should be boring, stable, and inspectable.

## 13. Common Mistakes

These problems are very typical:

- policy rules are scattered across runtime code;
- the capability contract is incomplete;
- tools exposed to the model are treated as if they were automatically approved capabilities;
- capability ownership is unclear;
- approval logic is embedded directly into orchestration;
- approval exists as a human process, but not as an explicit pause/resume path in the runtime;
- structured contracts are missing, so policy and approval payloads drift in shape;
- memory policy and execution policy behave as if they were unrelated;
- the catalog and real adapters drift apart in behavior.

When that happens, the reference implementation stops being a reference and becomes a bundle of conventions again.

## 14. A Fast Maturity Test for the Policy Layer and Capability Catalog

A team should not think it has assembled the contract core of its agent system only because it has a few policy checks and a list of tools.

A stronger bar is this:

- policy decisions are explicit objects rather than scattered booleans;
- capability contracts carry ownership, transport, exposure, risk, and approval semantics;
- runtime code depends on the catalog instead of direct calls and ad hoc exceptions;
- approval is modeled as an explicit interruptible path rather than as an off-path manual workaround;
- memory policy, execution policy, and approval policy belong to one visible control surface;
- telemetry can expose not only what happened, but which policy and capability contract governed it.

If most of those conditions are missing, the runtime may exist, but the contract core is still not assembled.

## 15. What to Do Right Away

Start with this short list and mark every "no" explicitly:

- Do you have a separate policy layer instead of a pile of `if` branches?
- Does policy return a structured decision?
- Is there a single capability catalog?
- Do capabilities have owner, transport, exposure, and risk semantics?
- Does the runtime use the catalog rather than direct calls?
- Can approval pause and resume a run explicitly?
- Are policy decisions visible in telemetry?

If the answer is "no" several times in a row, the skeleton exists, but the contract core is not assembled yet.

## 16. What to Do Next

First make policy decisions and capability contracts explicit, then check whether that same system is ready for its first rollout.

The next logical step in the reference implementation is to assemble a production rollout checklist, so you move from blueprint and contract core into a practical go-live framework.

- [Chapter 16. Baseline Runtime Blueprint](chapter-16.en.md)
- [Chapter 18. Production Rollout Checklist](chapter-18.en.md)
- [Part VII. Reference Implementation](index.en.md)
- [Sources](../../appendix/sources.en.md)

[^openai-tools]: [OpenAI, Using tools](https://developers.openai.com/api/docs/guides/tools)
[^langgraph-interrupts]: [LangGraph, Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)
[^openai-structured]: [OpenAI, Structured model outputs](https://developers.openai.com/api/docs/guides/structured-outputs)

## 17. Useful Reference Pages

- [Policy Bundle Schema and Approval Contract](../../appendix/policy-bundle-schema.en.md)
- [Lifecycle Artifact Schema](../../appendix/lifecycle-artifact-schema.en.md)
- [Reference Package](../../appendix/reference-package.en.md)

This chapter is the contract hinge for the rest of the runtime-control cluster. The most useful next steps are Chapter 18 for rollout gates and Chapter 21 for assurance response built on the same approval and policy paths.

- [Chapter 16. Baseline Runtime Blueprint](chapter-16.en.md)
- [Chapter 18. Production Rollout Checklist](chapter-18.en.md)
- [Part VII. Reference Implementation](index.en.md)
- [Sources](../../appendix/sources.en.md)
