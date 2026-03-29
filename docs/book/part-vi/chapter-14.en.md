# Chapter 14. Platform Team vs Product Teams

## 1. Why an Agent Platform Usually Breaks on Ownership, Not Code

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

## 10. What Usually Breaks in the Operating Model

The same problems repeat often:

- the platform becomes a bottleneck for every decision;
- products bypass the platform completely;
- ownership is unclear;
- reusable primitives are too low-level;
- there is no process for deviations;
- the platform roadmap is disconnected from product-team pain.

That leads to the classic fork: either the platform helps nobody, or product teams see it as an obstacle.

## 11. Practical Checklist

If you want to review your operating model quickly, go through these questions:

- Is it clear what is owned by the platform team?
- Is it clear what stays with product teams?
- Do you have a golden path, not just "a set of capabilities"?
- Is it obvious who approves new risky capabilities?
- Is there a process for deviations from the standard path?
- Does the platform actually reduce the number of local runtime implementations?

If the answer is "no" several times in a row, you probably no longer have a technical problem. You have an organizational design problem.

## 12. What to Read Next

The next natural step in this part is to look at how to build shared gateways, reusable templates, and anti-zoo patterns so that the operating model does not remain just words.

- [Chapter 13. Offline Evals, Online Evals, and Regression Gates](../part-v/chapter-13.en.md)
- [Chapter 15. Golden Paths, Shared Gateways, and Anti-Zoo Patterns](chapter-15.en.md)
- [Part VI. Operating Model](index.en.md)
- [Sources](../../appendix/sources.en.md)
