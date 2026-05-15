# Chapter 14. Platform Team vs Product Teams

!!! info "How to read this chapter"
    It helps to keep one very practical question in mind rather than a generic org-design topic:

    - who owns the runtime;
    - who approves policy changes and risky capabilities;
    - who is responsible when the same support agent breaks at the gateway, tracing, or approval layer.

    If those answers are not explicit, the technical architecture starts to spread apart even while the code still appears to work.

## 1. Why an Agent Platform Usually Breaks on Ownership, Not Code

In the running support case, this is very concrete: the agent already exists, the tool gateway already exists, traces already exist, approvals are already wired in. But the moment the first platform-grade incident happens, the main question is no longer "what broke," but "who is actually responsible for fixing and changing the shared layer."

At the beginning, everything looks simple: a few enthusiasts, one or two agents, a couple of integrations, and fast experiments. That is normal.

The problems start later:

- product teams build local agent runtimes;
- each team writes policy checks its own way;
- observability is emitted in three incompatible formats;
- tool adapters get duplicated;
- nobody is sure who should fix platform-grade incidents.

So the system may still work technically, but organizationally it is already starting to spread apart.

## 2. The Platform Team Should Not Take Every Decision Away From Product Teams

There is one bad extreme: the platform team tries to become the single approval point for every agent decision.

Then this happens:

- the platform becomes a bottleneck;
- product teams lose speed;
- every change queues behind one team;
- the platform layer grows into a heavy machine.

That model does not work. The platform team is not there to build every agent feature itself. Its job is to provide stable shared layers and safe default paths.

## 3. The Opposite Extreme Is Bad Too: Full Federation

Some companies go the other way: "let every team decide how to build agents on its own."

That quickly gives you:

- incompatible contracts;
- different security posture;
- uneven eval quality;
- uneven observability;
- local platforms inside each team.

In the short term it looks like freedom. In the long term it almost always turns into a zoo.

## 4. A Mature Model Usually Looks Like Platform + Product Split

A good operating model usually splits responsibility roughly like this:

`platform team` owns:

- orchestration primitives;
- policy framework;
- tool and capability contracts;
- observability and eval substrate;
- shared gateways;
- baseline security model.

`product teams` own:

- user workflows;
- product-specific prompts and policies;
- domain logic;
- acceptance criteria for task success;
- integration of platform primitives into the actual product.

<div class="diagram-card">
<p>Platform and product should not duplicate each other, because they own different responsibility layers</p>

``` mermaid
flowchart LR
    A["Platform team"] --> B["Runtime, policy, observability, gateways"]
    C["Product teams"] --> D["User workflows, domain logic, UX outcomes"]
    B --> E["Golden paths and shared primitives"]
    D --> E
```

</div>

!!! example "Case thread: who fixes the shared layer"
    After the duplicate-ticket incident, the product team should own how the support workflow answers the user and when it escalates. But the platform team should own the runtime retry policy, idempotency contract, trace schema, and rollout gate, because those decisions serve every write-capability scenario, not only one agent. If that split is not explicit before the incident, the next incident becomes another ownership dispute.

**Ownership case-spine note:** the platform/product split should be explicit for all three canonical cases. Support triage divides ownership across the product workflow, approval policy, write-capability contract, and duplicate-ticket response. Internal knowledge assistant divides corpus ownership, retrieval policy, memory-write rules, and access-control review. Incident coordination divides incident roles, escalation authority, notification ownership, and post-incident change ownership so the platform team does not become a bottleneck and product teams do not build three incompatible control planes.

## 5. The Platform Should Offer Golden Paths, Not Just Low-Level Pieces

If the platform team only ships a bag of parts, product teams will still assemble systems in different ways.

A golden path usually includes:

- a baseline runtime template;
- ready-made policy hooks;
- standard tracing and eval wiring;
- an approved tool gateway pattern;
- guidance for memory usage;
- rollout and regression defaults.

So a good platform product helps teams not only "be able to build", but also "build the right way by default."

## 6. Ownership Should Be Explicit at Every Layer

It is very useful to decide early who owns what:

- who can change platform contracts;
- who approves new write capabilities;
- who owns policy schemas;
- who owns the telemetry schema;
- who is on-call for platform incidents;
- who decides when a product may leave the golden path.

If ownership is fuzzy, almost any incident turns into a long organizational ping-pong game.

### 6.1. Platform Inventory Should Have an Owner Too

One useful Google lesson here is that governance does not stop at a policy framework. A platform also needs an explicit inventory of what the organization is actually running.[^google-ai-controls][^google-agent-overview]

At minimum, it is useful to see:

- which agent runtimes exist;
- which capabilities are approved;
- which gateways are considered approved;
- which connectors and secrets are in use;
- which deviations are active;
- who owns each of those objects.

Without that inventory, a platform almost inevitably drifts into rumor-driven governance: everything looks "under control" until an incident reveals that nobody really knows which agents and tools are operating in production.

## 7. Not Every Deviation Should Be Forbidden, But It Should Be Intentional

Sometimes a product team really does need a special case:

- a non-standard workflow;
- a separate capability;
- a different latency/cost trade-off;
- an experimental rollout.

That is fine. The difference between a mature platform and chaos is that a deviation is:

- visible;
- discussed;
- limited in blast radius;
- owned by someone;
- prevented from quietly becoming the new default.

## 8. Example Governance Policy for an Agent Platform

Here is a very practical template:

```yaml
governance:
  platform_owned:
    - runtime_contracts
    - policy_framework
    - telemetry_schema
    - shared_tool_gateway
  product_owned:
    - workflow_logic
    - domain_prompts
    - task_success_criteria
  requires_platform_review:
    - new_write_capability
    - custom_policy_engine
    - telemetry_schema_change
    - direct_external_tool_access
```

That YAML will not solve every organizational problem, but it is very good at removing the endless question: "who is actually supposed to decide this?"

### 8.1. An Approved Registry Is Nearly as Important as a Policy Schema

Teams often discuss policy in detail, but barely discuss the registry. Yet the registry answers:

- what is actually platform-approved;
- what may run without additional review;
- what currently lives in the exception zone;
- what should already be retired.

A simple example:

```yaml
registry:
  approved_runtimes:
    - agent_runtime_v3
    - workflow_runtime_v2
  approved_gateways:
    - shared_tool_gateway
    - approval_gateway
  deprecated_patterns:
    - direct_prod_tool_access
    - local_policy_engine_without_audit
```

That registry does not replace governance. It makes governance executable.

## 9. A Platform Should Be Measured by How Much Chaos It Removes

It is important not to fall into vanity metrics like:

- how many tools were added;
- how many MCP servers were launched;
- how many product teams "adopted the platform."

A strong platform should reduce:

- duplication;
- the number of custom bypasses;
- the cost of adding a new workflow;
- incident investigation time;
- the number of unsafe deviations.

Otherwise you can build a lot and still fail to get systemically better.

### 9.1. Continuous Controls Are Better Than One-Time Reviews

Another practical upgrade is to catch risky changes not only through manual approvals, but also through continuous controls.

For example, the platform can automatically check:

- whether direct tool access appeared outside the gateway;
- whether a new connector exists without an owner;
- whether a runtime drifted away from an approved template;
- whether a new secret scope appeared without review;
- whether a deprecated pattern is still alive past its deadline.

That matters because platform governance usually breaks not during the nice architecture presentation, but months later through quiet exceptions and bypasses.

## 10. Common Mistakes

The same problems repeat often:

- the platform becomes a bottleneck for every decision;
- products bypass the platform completely;
- ownership is unclear;
- reusable primitives are too low-level;
- there is no process for deviations;
- the platform roadmap is disconnected from product-team pain.

That leads to the classic fork: either the platform helps nobody, or product teams see it as an obstacle.

## 11. A Fast Maturity Test for the Platform Operating Model

A team should not think it has solved platform ownership only because it created a platform team and documented a few review rules.

A stronger bar is this:

- platform and product ownership are explicit at the layer where incidents actually happen;
- golden paths remove chaos rather than just publish reusable pieces;
- deviations are visible, owned, and bounded rather than socially tolerated;
- platform inventory and approved registry make governance executable;
- the platform is measured by reduced duplication and bypasses, not adoption theater.

If most of those conditions are missing, the organization may have a platform label, but it still does not have a real platform operating model.

## 12. What to Do Right Away

Start with this short list and mark every "no" explicitly:

- Is it clear what is owned by the platform team?
- Is it clear what stays with product teams?
- Do you have a golden path, not just "a set of capabilities"?
- Is it obvious who approves new risky capabilities?
- Is there a process for deviations from the standard path?
- Does the platform actually reduce the number of local runtime implementations?

If the answer is "no" several times in a row, you probably no longer have a technical problem. You have an organizational design problem.

## 13. What to Do Next

First make ownership explicit, then see how that ownership model becomes golden paths, shared gateways, and anti-zoo patterns.

The next natural step in this part is to look at how to build shared gateways, reusable templates, and anti-zoo patterns so that the operating model does not remain just words.

- [Chapter 13. Offline Evals, Online Evals, and Regression Gates](../part-v/chapter-13.en.md)
- [Chapter 15. Golden Paths, Shared Gateways, and Anti-Zoo Patterns](chapter-15.en.md)
- [Part VI. Operating Model](index.en.md)
- [Sources](../../appendix/sources.en.md)

[^google-ai-controls]: [Google Cloud, Recommended AI Controls framework](https://cloud.google.com/blog/products/identity-security/audit-smarter-introducing-our-recommended-ai-controls-framework)
[^google-agent-overview]: [Google Cloud, Vertex AI Agent Builder overview](https://docs.cloud.google.com/agent-builder/overview)
