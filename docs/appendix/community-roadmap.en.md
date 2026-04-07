# Community Roadmap

The book already has a strong core: architecture, safety, memory, execution, observability, organizational design, and a runnable reference package. So what follows is not a general wishlist, but the backlog for the **next layer of value**.

## What Is Already Done

- a [Start Here](../start-here.en.md) page;
- a first set of [Practical Case Studies](case-studies.en.md);
- a first set of [Policy Templates](policy-templates.en.md);
- a runnable reference package and its [package docs](reference-package.en.md);
- a dedicated [Publishing Stack](stack.en.md) page.

## How I Select the Next Steps

Each item below passes three tests:

- it can be applied quickly in real work;
- it helps the wider community, not only the author of the book;
- it improves international readability, not only technical depth.

## Next 10 Improvements

### 1. A multilingual glossary

Add a shared `ru/en/zh` glossary for key terms:

- agent runtime;
- policy gate;
- trust boundary;
- profile memory;
- retrieval;
- compaction;
- rollout gate;
- capability catalog.

Why it matters: the book already has solid terminology, but a glossary will make reading, translation, linking, and community contributions much easier.

### 2. One-page cheat sheets

Add short practical sheets for:

- safety checklist;
- memory checklist;
- rollout checklist;
- observability checklist;
- tool gateway checklist.

Why it matters: these are the pages people actually save, share with teammates, and use the same day.

### 3. Extend the case studies set

The current cases are already useful, but the book should add 2-3 more:

- enterprise workflow agent;
- CRM/task agent;
- security-sensitive assistant.

Why it matters: the more recognizable scenarios readers see, the easier it is to map the architecture to their own systems.

### 4. Extend the policy template set

The book already contains first examples, but the community needs more explicit templates:

- tool approval policy;
- memory write policy;
- egress policy;
- rollout gate policy;
- retrieval policy.

Why it matters: a template people can copy and adapt is more valuable than a long explanation of why the template matters.

### 5. A trace schema and event catalog

Add a dedicated telemetry reference page:

- what event types exist;
- which fields are mandatory;
- what a `trace_id` should look like;
- which spans count as baseline;
- what should never appear in events.

Why it matters: observability becomes much stronger when the community has a shared event model, not only a shared idea.

### 6. More realistic scenarios in `agent_runtime_ref`

The package is already useful, but the next step should add:

- one knowledge scenario;
- one high-risk scenario with approval;
- one denied-by-policy scenario;
- sample JSONL traces in the docs.

Why it matters: a runnable reference package should not only show a happy path. It should teach production-like behavior.

### 7. A contribution kit for the community

Make external contribution easier:

- a page called `How to contribute patterns`;
- a template for new case studies;
- a template for glossary entries;
- a template for new policy templates.

Why it matters: a good open handbook grows faster when contributors know exactly how to help.

### 8. Stronger internal linking and chapter journeys

The book should make chapter movement easier:

- clearer "what to read next" cues;
- stronger links between architecture, case studies, and templates;
- short decision paths inside parts.

Why it matters: the book becomes more useful when readers do not get lost between strong but dense sections.

### 9. A discoverability layer

Add a more systematic discoverability layer:

- glossary;
- cheatsheets;
- stronger internal linking between chapters;
- social preview assets;
- more structured landing copy in `ru/en/zh`.

Why it matters: even a strong book does not help the community if people cannot find it, understand it quickly, and share it easily.

### 10. Social and sharing assets

The project should include lightweight sharing assets:

- social preview assets;
- a few shareable cheat sheets;
- short landing summaries in `ru/en/zh`.

Why it matters: international reach grows when the book is easy not only to read, but also to share.

## What to Do First

If only three steps happen next, I would do:

1. Glossary
2. Cheat sheets
3. Trace schema and event catalog

That would produce the fastest growth in practical value without rewriting the architectural chapters.

## What Would Change in a Month

If this backlog is executed, the project will gain:

- a much clearer entry point for new readers;
- more pages people can quote and share;
- more reusable artifacts for teams;
- a better contribution path for the community;
- a stronger international profile.

## The Next Practical Step

If we follow this roadmap, the next best page to build is the multilingual glossary, followed by the first set of cheat sheets.

- [Home](../index.en.md)
- [Book Plan](../book/plan.en.md)
- [Reference Package](reference-package.en.md)
- [Sources](sources.en.md)
