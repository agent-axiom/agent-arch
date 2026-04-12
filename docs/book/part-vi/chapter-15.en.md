# Chapter 15. Golden Paths, Shared Gateways, and Anti-Zoo Patterns

!!! info "How to read this chapter"
    It helps to keep one practical question in mind rather than a generic platform-pattern topic:

    - how to make sure a product team does not rebuild its own local runtime from scratch;
    - which shared layers should arrive preassembled: gateway, policy hooks, tracing, and rollout defaults;
    - how to push the operating model to the point where the next chapter naturally becomes a reference implementation.

    Without that transition, the operating model stays declarative while teams still rebuild the system separately.

## 1. Why Even a Good Operating Model Falls Apart Without Engineering Templates

Once you decide who owns the platform and who owns the product, the next question appears: what exactly should teams reuse in practice?

In the running support case, this already turns into something concrete: the team should not have to rebuild the same run loop, policy hooks, tool gateway, and tracing just to launch the same support agent. If the platform does not provide that path, the operating model stays on paper while the engineering shape falls back into local variants.

If there is no answer, the familiar pattern shows up:

- each team writes its own runtime wrapper;
- policy hooks look different everywhere;
- tool adapters drift across contracts;
- rollout practices live in local wikis;
- observability wiring is copied by hand and slowly diverges.

So formally you may have an operating model, but in practice you still have many local systems with similar but incompatible implementations.

## 2. A Golden Path Is Not a "Best Practices Document". It Is the Default Working Path

It is important not to confuse a golden path with a set of recommendations.

Recommendations are read selectively.
A golden path in a good platform product feels like something that is genuinely easier to use than to bypass.

It usually includes:

- a starter runtime template;
- pre-wired tracing and eval hooks;
- policy integration by default;
- an approved tool gateway;
- deployment and rollout defaults;
- examples of typical product workflows.

A golden path is good when a team benefits from staying on it.

## 3. Shared Gateways Exist So You Do Not Replicate Critical Mistakes Across the Company

There are several layers that are especially risky to leave to local improvisation:

- access to external capabilities;
- policy enforcement;
- secret handling;
- audit trail;
- approval workflows;
- telemetry emission.

If every team implements them alone, the organization almost certainly reproduces the same mistakes in five versions.

That is why a shared gateway is not bureaucracy. It is a way to solve the most expensive and sensitive problems once, centrally, and well.

<div class="diagram-card">
<p>The golden path should reduce the number of local implementations of critical layers</p>

``` mermaid
flowchart LR
    A["Product team A"] --> D["Shared gateway and platform primitives"]
    B["Product team B"] --> D
    C["Product team C"] --> D
    D --> E["Policy, tracing, approvals, capability access"]
```

</div>

## 4. A Reusable Template Should Be Opinionated, Not Abstract

A very common platform-team mistake is making the template as neutral as possible so that it can "fit everyone."

In practice, that rarely helps anyone. It is so generic and requires so much manual assembly that teams still move to custom implementations.

A good template is usually opinionated:

- it defines the basic run structure;
- it already includes policy hooks;
- it is already wired to tracing;
- it has an approved deployment path;
- it contains working examples;
- it supports a limited number of extension points.

Yes, that is less "universal." But it is much more useful for a real organization.

## 5. You Do Not Need One Golden Path for Every Type of Agent

Maturity matters here too. One path is rarely equally good for:

- Q&A agents;
- workflow agents;
- approval-heavy agents;
- high-risk action agents;
- internal copilots.

So a practical approach usually looks like this:

- one base platform core;
- 2-4 standard golden paths;
- a shared gateway and observability substrate;
- controlled deviations for special cases.

That is better than either one giant template for the whole world or total chaos.

## 6. An Anti-Zoo Pattern Starts by Limiting Freedom in the Right Places

The term "platform zoo" usually means the same thing:

- too many runtimes;
- too many ways to connect tools;
- too many local policy engines;
- too many telemetry schemas;
- too many almost-identical wrapper layers.

The right way to reduce that zoo is not by banning everything. It is by putting clear constraints in the right places:

- one contract layer;
- one shared gateway;
- a limited set of supported runtime patterns;
- platform review for risky deviations;
- a deprecation policy for old bypass paths.

### 6.1. A Registry of Approved Patterns Helps Not Only With Control, but Also With Speed

When the platform has a live list of approved patterns, product teams can answer two common questions much faster:

1. What can be used without separate review?
2. What already counts as a risky deviation?

A good registry usually contains:

- supported runtime templates;
- approved gateways;
- approved capability classes;
- allowed connector patterns;
- deprecated local bypasses.

This is useful not only for the security team. It also speeds up engineering work because teams do not start from scratch every time.

## 7. Example Platform Defaults Policy

Here is a practical template that makes golden paths and deviations explicit:

```yaml
platform_defaults:
  required:
    - shared_tool_gateway
    - standard_trace_schema
    - policy_hooks
    - eval_gate_in_ci
  supported_templates:
    - qa_agent
    - workflow_agent
    - approval_agent
  deviations_require_review:
    - custom_runtime
    - direct_tool_access
    - custom_telemetry_schema
    - bypass_of_policy_layer
```

That policy does not kill speed. It removes ambiguity.

### 7.1. Registry and Deprecation Policy Should Live Together

A weak pattern looks like this: the platform has "recommended paths," but no formal list of what is no longer acceptable.

A much stronger setup is the combination of:

- an approved registry;
- visible deviations;
- deprecation windows;
- a review path for exceptions.

That is what keeps an anti-zoo strategy from turning into an endless plea to "please use the standard path."

## 8. Shared Gateways Help Not Only With Safety, but Also With Speed of Evolution

When the critical path is centralized, the platform team can:

- update contracts in one place;
- improve the audit trail once for everyone;
- change rollout guardrails without rewriting ten products;
- roll out new policy capabilities faster;
- fix mass operational issues faster.

So a shared gateway is not only about control. It is also about scalable engineering improvement.

## 9. What Usually Breaks in Anti-Zoo Efforts

There are many recurring mistakes here too:

- the golden path is too heavy, so teams bypass it;
- the shared gateway is too slow or too awkward;
- exceptions become normal practice;
- templates get stale quickly;
- the platform team does not track where teams actually leave the path;
- deprecation is promised, but never enforced.

Then the organization formally talks about standardization while practically producing new variants of the old chaos.

## 10. What to Measure If You Really Want to Fight the Zoo

Useful operational metrics here are:

- number of local runtime forks;
- number of direct tool-access paths that bypass the gateway;
- share of agents built on supported templates;
- median time to launch a new workflow on the golden path;
- number of active deviations without an owner;
- time to deprecate unsafe patterns.

That is much more useful than simply counting "how many teams use the platform."

### 10.1. Inventory Drift Is Worth Measuring on Its Own

It is also useful to track drift inside the platform inventory itself:

- how many runtimes are not registered;
- how many active agents live outside approved templates;
- how many connectors have no owner;
- how many deviations remain beyond their review window.

If those numbers rise, the anti-zoo strategy may still exist formally, but it is already losing in practice.

## 11. Practical Checklist

If you want to review your anti-zoo strategy quickly, ask:

- Do you have a real golden path that is easier to use than to bypass?
- Is there a shared gateway for sensitive capabilities?
- Is the set of supported runtime patterns limited?
- Are deviations visible, and do they have owners?
- Can the platform deprecate unsafe local patterns?
- Does the new platform layer actually reduce copy-paste and local forks?

If the answer is "no" several times in a row, then you are not building a platform product yet. You are building a library with good intentions.

## 12. What to Do Next

First verify that the golden path and shared gateway are genuinely easier to use than to bypass, then see how that path becomes runtime code.

The next step after this chapter is no longer another org chart. It is the code skeleton: seeing how the golden path, shared gateway, and approved runtime patterns get fixed inside the reference implementation.

- [Chapter 14. Platform Team vs Product Teams](chapter-14.en.md)
- [Chapter 16. Baseline Runtime Blueprint](../part-vii/chapter-16.en.md)
- [Part VI. Operating Model](index.en.md)
- [Sources](../../appendix/sources.en.md)
