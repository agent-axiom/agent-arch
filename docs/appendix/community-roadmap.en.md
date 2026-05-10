# Community Roadmap

The book already has a strong core: architecture, safety, memory, execution, observability, organizational design, and a runnable reference package. So what follows is not a general wishlist, but the backlog for the **next layer of value**.

## What Is Already Done

- a [Start Here](../start-here.en.md) page;
- a [multilingual glossary](glossary.en.md);
- a [cheat sheets page](cheat-sheets.en.md);
- a representative set of [Practical Case Studies](case-studies.en.md);
- reusable [Policy Templates](policy-templates.en.md);
- a runnable reference package and its [package docs](reference-package.en.md);
- reference schemas for traces, evals, policies, approvals, memory, rollout, and lifecycle artifacts;
- a dedicated [Publishing Stack](stack.en.md) page.

## How I Select the Next Steps

Each item below passes three tests:

- it can be applied quickly in real work;
- it helps the wider community, not only the author of the book;
- it improves international readability, not only technical depth.

## Next 10 Improvements

### 1. Extend the case studies set

The current cases are already useful, but the book should add 2-3 more:

- enterprise workflow agent;
- CRM/task agent;
- security-sensitive assistant.

Why it matters: the more recognizable scenarios readers see, the easier it is to map the architecture to their own systems.

### 2. Extend the policy template set

The book already contains first examples, but the community needs more explicit templates:

- tool approval policy;
- memory write policy;
- egress policy;
- rollout gate policy;
- retrieval policy.

Why it matters: a template people can copy and adapt is more valuable than a long explanation of why the template matters.

### 3. Richer trace examples and visual QA

The trace schema and event catalog exist already. The next step is to make them easier to validate and read:

- add more realistic JSONL trace examples;
- show one successful run, one approval wait, one denied run, and one failed run;
- keep the rendered schema pages free of broken tables, list joins, and raw diagram blocks;
- add a lightweight rendered-site QA checklist for the most visible pages.

Why it matters: observability becomes much stronger when the community has both a shared event model and concrete examples of how it appears in the published site.

### 4. More realistic scenarios in `agent_runtime_ref`

The package is already useful, but the next step should add:

- one knowledge scenario;
- one high-risk scenario with approval;
- one denied-by-policy scenario;
- sample JSONL traces in the docs.

Why it matters: a runnable reference package should not only show a happy path. It should teach production-like behavior.

### 5. A contribution kit for the community

Make external contribution easier:

- a page called `How to contribute patterns`;
- a template for new case studies;
- a template for glossary entries;
- a template for new policy templates.

Why it matters: a good open handbook grows faster when contributors know exactly how to help.

### 6. Stronger internal linking and chapter journeys

The book should make chapter movement easier:

- clearer "what to read next" cues;
- stronger links between architecture, case studies, and templates;
- short decision paths inside parts.

Why it matters: the book becomes more useful when readers do not get lost between strong but dense sections.

### 7. A discoverability layer

Add a more systematic discoverability layer:

- glossary;
- cheatsheets;
- stronger internal linking between chapters;
- social preview assets;
- more structured landing copy in `ru/en/zh`.

Why it matters: even a strong book does not help the community if people cannot find it, understand it quickly, and share it easily.

### 8. Social and sharing assets

The project should include lightweight sharing assets:

- social preview assets;
- a few shareable cheat sheets;
- short landing summaries in `ru/en/zh`.

Why it matters: international reach grows when the book is easy not only to read, but also to share.

## What to Do First

If only three steps happen next, I would do:

1. Trace schema and event catalog
2. Contribution kit
3. Expand the case studies set

That would produce the fastest growth in practical value without rewriting the architectural chapters.

## What Would Change in a Month

If this backlog is executed, the project will gain:

- a much clearer entry point for new readers;
- more pages people can quote and share;
- more reusable artifacts for teams;
- a better contribution path for the community;
- a stronger international profile.

## The Next Practical Step

If we follow this roadmap, the next best step is a trace schema and event catalog, followed by a contribution kit.

- [Home](../index.en.md)
- [Book Plan](../book/plan.en.md)
- [Reference Package](reference-package.en.md)
- [Sources](sources.en.md)
