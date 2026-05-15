# Chapter 19. From SDLC to ADLC

## 1. Why it is worth revisiting classical SDLC first

When teams start building agent systems, they often feel tempted to say that “old processes no longer work” and that they now need a completely new lifecycle.

That is a poor starting point.

Classical software development lifecycle discipline is still necessary, because it gives the baseline engineering structure:

- requirements;
- design;
- implementation;
- testing;
- release;
- operations;
- retirement.

NIST makes the same move in its SSDF profile for generative AI: secure development practices for generative systems should not be invented from scratch, but extended on top of existing secure software discipline.[^nist-ssdfa]

So an agent system does not replace SDLC. It makes the default form of SDLC incomplete.

That is the real promise of this chapter. It is not to rename the software lifecycle with new letters. It is to show why the governed system assembled in Part VII now needs a lifecycle frame wide enough to hold model behavior, policy movement, retrieval drift, tool-side effects, evidence, and retirement decisions over time.

## 2. What remains the same

If you remove the hype, a lot remains familiar:

- requirements still need to be explicit;
- architecture still needs design review;
- integrations still need owners and contracts;
- risky changes still need controlled release;
- incidents still require postmortems and corrective action.

This matters psychologically for teams. ADLC should not look like “magic beyond engineering.” It should look like a disciplined extension of engineering.

## 3. What changes in agent systems

This is where the real difference begins.

In a conventional system, behavior is driven mostly by code and relatively deterministic logic. In an agent system, additional mutable surfaces appear:

- model behavior is probabilistic;
- prompts and routines can change outcomes as much as code;
- retrieval and memory change system inputs without changing business logic;
- tools create real side effects;
- policy changes can reshape whole classes of tasks;
- online drift can appear even when “nothing broke” in the release.

That is exactly why the NIST AI RMF GenAI Profile emphasizes that trustworthiness considerations must extend across design, development, use, and evaluation, not only release time.[^nist-genai]

## 4. ADLC is best understood as SDLC plus new surfaces of change

The most practical engineering model is simple:

`ADLC = SDLC + model behavior + prompts/routines + policies + retrieval/memory + tools + evals + governed autonomy`

The new lifecycle exists not because “agents are magical,” but because there are more moving parts that can change and must be released and governed. The main artifact of this chapter is the ADLC state model: a map of states and transitions, not another generic governance checklist.

<div class="diagram-card">
<p>ADLC works best as an extension of SDLC, not a replacement for it</p>

``` mermaid
flowchart LR
    A["Classical SDLC"] --> B["Requirements"]
    A --> C["Design"]
    A --> D["Implementation"]
    A --> E["Testing"]
    A --> F["Release"]
    A --> G["Operations"]
    A --> H["Retirement"]

    H --> I["ADLC adds"]
    I --> J["Model behavior"]
    I --> K["Prompts and routines"]
    I --> L["Policies and approvals"]
    I --> M["Retrieval and memory"]
    I --> N["Tool side effects"]
    I --> O["Evals and controlled autonomy"]
```

</div>

## 5. Which artifacts become release-bearing

In ordinary SDLC, teams usually focus on code, infrastructure, and schemas. In ADLC, the release-bearing artifact set is wider:

- model selection and routing;
- system instructions and routines;
- policy configs;
- capability contracts;
- retrieval corpora;
- memory write rules;
- eval datasets;
- approval policies;
- rollout gates.

!!! example "Case thread: duplicates as an ADLC change"
    In the support-triage system, fixing the duplicate-ticket incident does not end with a retry-code patch. The release-bearing artifacts now include a new eval dataset, the policy bundle for `side_effect_unknown`, the capability contract for `create_support_ticket`, the canary rollout gate, and the trace schema used later to investigate the outcome. In ADLC, those changes should move as one reviewable change set; otherwise the team ships code while leaving the lifecycle broken.

**ADLC case-spine note:** the lifecycle state model should track all three canonical cases as different release-bearing surfaces. Support triage links code change, policy bundle, write-capability contract, duplicate-ticket evals, and rollout gate. Internal knowledge assistant links retrieval corpus, source-grounding evals, memory-write rules, tenant filters, and freshness review. Incident coordination links escalation policy, responder-role map, notification contract, incident-state schema, and post-incident lessons as one governed change set.

This is one of the most important operational shifts. If a team treats only code as a release, it will miss risky agent changes.

## 6. Why tests are no longer enough

Tests remain important, but they are not enough.

Agent systems need a broader assurance contour:

- deterministic tests for code and contracts;
- offline evals for known scenarios;
- simulators or scenario-based checks for multi-step behavior;
- online monitoring for drift and emergent failures;
- policy checks for risky paths;
- approval and rollout gates to limit blast radius.

OpenAI and Anthropic reach a similar practical conclusion from different angles: first establish a baseline, then iterate under control, rather than jumping straight to autonomy.[^openai-guide][^anthropic-agents]

## 7. Security assurance also needs its own lifecycle

In a conventional service, security review often focuses on code, dependencies, infrastructure, and access. That is not sufficient for agents.

Google Research makes a strong case that security assurance should run as a continuous loop, not as a one-time review: red teaming, vulnerability management, detection and response, threat intelligence, and remediation must live next to release processes, not after them.[^google-assurance]

That is an important point for this book: agent security is not just a prompt-injection checklist. It is an operational function.

## 8. The agent supply chain is wider than package dependencies

Another useful correction from Google is that an AI software supply chain includes not just libraries and containers, but also provenance for models, data, configs, pipelines, and evaluation artifacts.[^google-supply-chain]

For an agent system, that matters because otherwise you cannot answer:

- where this model came from;
- which dataset validated this release;
- which policy bundle was in production;
- which retrieval corpus was active;
- which prompt or routine changed between rollout waves.

In other words, provenance in ADLC is not decorative. It is required for normal change management and incident investigation, including recovery of exported failed-run evidence such as `failure_reason` when a release path degrades.

## 9. A good ADLC starts with intake and design review, not release

If an agent initiative enters engineering only when “something already exists,” architecture and governance problems will surface too late.

Useful early-stage lifecycle questions include:

- do we really need an agent here, or would a workflow be enough;
- what is the autonomy budget;
- which side effects are even allowed;
- where are the trust boundaries;
- which capabilities are high-risk;
- do we need a memory layer;
- which evals must exist before a pilot.

Those are already the first steps of ADLC.

## 10. A practical ADLC frame

For a production-grade agent system, I would recommend at least these stages:

1. Intake and suitability review
2. Architecture and safety design review
3. Build and integration
4. Eval baseline
5. Staged rollout
6. Steady-state operations
7. Incident response and corrective action
8. Retirement or replacement

<div class="diagram-card">
<p>ADLC should be treated as a continuous loop, not a path that ends at first launch</p>

``` mermaid
flowchart LR
    A["Intake"] --> B["Design review"]
    B --> C["Build and integration"]
    C --> D["Eval baseline"]
    D --> E["Staged rollout"]
    E --> F["Operations"]
    F --> G["Incidents and corrective actions"]
    G --> H["Retirement or replacement"]
    H --> A
```

</div>

## 11. Why this matters in practice

If all of this is presented as “best practices,” teams often treat it as optional advice.

If it is presented as a lifecycle model, more useful questions appear:

- which stage are we in;
- what is missing to move forward;
- which artifact must exist before the next gate;
- who owns the next decision;
- what risk are we taking if we skip a stage.

That is what makes ADLC practical: it turns an agent program from a hype discussion into a governed engineering program.

## 12. What not to do

Some mistakes show up over and over again:

- declaring that “normal engineering no longer works” for agents;
- treating ADLC as just a new label for prompt iteration;
- assuming a rollout checklist covers the entire lifecycle;
- failing to treat prompt, policy, and retrieval changes as release-bearing;
- disconnecting evals from change management;
- ignoring retirement discipline until the very end.

If that happens, ADLC becomes a nice phrase without operational value.

## 13. Practical checklist

If you want to tell quickly whether you already need a full ADLC, ask:

- Do you ship prompt, policy, or model changes in addition to code changes?
- Does the system produce risky side effects?
- Does it use retrieval, memory, or other mutable knowledge surfaces?
- Do release decisions depend on evals?
- Do you already need staged rollout, approval gates, and incident review?
- Do you need to explain which exact artifact was in production during an incident?

If the answer is “yes” several times in a row, you are already living in ADLC, even if you do not call it that yet.

## 14. What to read next

After this transition chapter, the natural next topics are change management, assurance loops, and supply chain discipline. But even now it is useful to connect it back to what the book already contains:

- [Chapter 13. Offline Evals, Online Evals, and Regression Gates](../part-v/chapter-13.en.md)
- [Chapter 18. Production Rollout Checklist](../part-vii/chapter-18.en.md)
- [Part VI. Organizational Model](../part-vi/index.en.md)
- [Sources](../../appendix/sources.en.md)

[^nist-ssdfa]: [NIST SP 800-218A: Secure Software Development Practices for Generative AI and Dual-Use Foundation Models](https://csrc.nist.gov/pubs/sp/800/218/a/final)
[^nist-genai]: [NIST AI RMF: Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
[^openai-guide]: [OpenAI, A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
[^anthropic-agents]: [Anthropic, Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
[^google-assurance]: [Google Research, Security Assurance in the Age of Generative AI](https://research.google/pubs/security-assurance-in-the-age-of-generative-ai/)
[^google-supply-chain]: [Google Research, Securing the AI Software Supply Chain](https://research.google/pubs/securing-the-ai-software-supply-chain/)
