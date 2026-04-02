# Community Roadmap

The book already has a strong core: architecture, safety, memory, execution, observability, organizational design, and a runnable reference package. But if the goal is to attract readers from all over the world, the next layer is not "more theory". It is **faster practical value**.

Below is a focused backlog of 10 improvements. These are not abstract wishes. They are concrete upgrades that make the book more useful for engineers, platform teams, security specialists, and open source contributors.

## Selection Rule

Each item below passes three tests:

- it can be applied quickly in real work;
- it helps the wider community, not only the author of the book;
- it improves international readability, not only technical depth.

## Top 10 Improvements

### 1. A `Start here` page

Add a short landing page for new readers:

- what this book is;
- who it is for;
- where engineers should start;
- where security teams should start;
- where the ready-to-use templates and code live.

Why it matters: most readers do not begin with chapter 1. They want to find their path quickly.

### 2. A multilingual glossary

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

### 3. One-page cheat sheets

Add short practical sheets for:

- safety checklist;
- memory checklist;
- rollout checklist;
- observability checklist;
- tool gateway checklist.

Why it matters: these are the pages people actually save, share with teammates, and use the same day.

### 4. A small set of case studies

Add 3-5 short real-world scenarios:

- support agent;
- internal knowledge agent;
- enterprise workflow agent;
- CRM/task agent;
- security-sensitive assistant.

Why it matters: case studies help readers recognize their own context and map the architecture to real systems.

### 5. Ready-to-use policy templates

The book already contains examples, but the community needs more explicit templates:

- tool approval policy;
- memory write policy;
- egress policy;
- rollout gate policy;
- retrieval policy.

Why it matters: a template people can copy and adapt is more valuable than a long explanation of why the template matters.

### 6. A trace schema and event catalog

Add a dedicated telemetry reference page:

- what event types exist;
- which fields are mandatory;
- what a `trace_id` should look like;
- which spans count as baseline;
- what should never appear in events.

Why it matters: observability becomes much stronger when the community has a shared event model, not only a shared idea.

### 7. More realistic scenarios in `agent_runtime_ref`

The package is already useful, but the next step should add:

- one knowledge scenario;
- one high-risk scenario with approval;
- one denied-by-policy scenario;
- sample JSONL traces in the docs.

Why it matters: a runnable reference package should not only show a happy path. It should teach production-like behavior.

### 8. A contribution kit for the community

Make external contribution easier:

- a page called `How to contribute patterns`;
- a template for new case studies;
- a template for glossary entries;
- a template for new policy templates.

Why it matters: a good open handbook grows faster when contributors know exactly how to help.

### 9. A stronger home page

The home page is already solid, but it can become more useful for first-time visitors:

- a clear "Who this is for" block;
- a "What you can take away in 30 minutes" block;
- a "What makes this different" block.

Why it matters: global reach starts with clarity, not with chapter count.

### 10. A discoverability layer

Add a more systematic discoverability layer:

- `Start here`;
- glossary;
- cheatsheets;
- stronger internal linking between chapters;
- social preview assets;
- more structured landing copy in `ru/en/zh`.

Why it matters: even a strong book does not help the community if people cannot find it, understand it quickly, and share it easily.

## What to Do First

If only three steps happen next, I would do:

1. `Start here`
2. Glossary
3. Cheat sheets

That would produce the fastest growth in practical value without rewriting the architectural chapters.

## What Would Change in a Month

If this backlog is executed, the project will gain:

- a much clearer entry point for new readers;
- more pages people can quote and share;
- more reusable artifacts for teams;
- a better contribution path for the community;
- a stronger international profile.

## The Next Practical Step

If we follow this roadmap, the next best page to build is `Start here`, followed immediately by the multilingual glossary.

- [Home](../index.en.md)
- [Book Plan](../book/plan.en.md)
- [Reference Package](reference-package.en.md)
- [Sources](sources.en.md)
