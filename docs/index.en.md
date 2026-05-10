# Secure AI Agent Architecture

This book is for teams that need not a flashy demo, but an agent system that can survive production reality.

Its central thesis is simple: **an agent needs a platform, not magic**. As soon as a system gains risky actions, memory, approvals, rollout, and a long operational tail, a model with a few tools stops being enough. You need explicit trust boundaries, a policy layer, controlled execution, observability, quality judgment, and lifecycle discipline.

Building agents is boring, but the result is staggering: instead of a flashy one-off trick, the team gets a system it can constrain, observe, ship, and improve without guessing.

<div class="hero-actions" markdown="1">

[Start Here](start-here.en.md){ .md-button .md-button--primary }
[Read Chapter 1](book/part-i/chapter-1.en.md){ .md-button }
[Open the Book Plan](book/plan.en.md){ .md-button }

</div>

<div class="book-cover" markdown="1">

![Book cover](assets/images/hero-home.png)

</div>

## Who This Book Is For

- Product engineers who want to build agent features without turning the system into a pile of prompts and exceptions.
- Platform teams that need a shared runtime, policy layer, approvals, observability, and controlled rollout.
- Security engineers who care about trust boundaries, risky execution paths, and abuse surfaces.
- Tech leads and architects who need reproducible engineering discipline instead of agent theater.

## What It Should Change in the Reader's Thinking

After this book, the reader should stop thinking of an agent as "an LLM plus some orchestration" and start thinking of it as a governed production system:

- with explicit trust and action boundaries;
- with execution constrained by policy;
- with approvals for risky paths;
- with run-level observability and evidence;
- with rollout discipline, ownership, and lifecycle governance.

## How To Read the Book

If you need the shortest entry, start with [Chapter 1](book/part-i/chapter-1.en.md). If you need a route by role or task, open [Start Here](start-here.en.md). If structure and status matter more, use the [Book Plan](book/plan.en.md). If you want reusable artifacts, schemas, and contracts, go to the [reference layer](reference.en.md).

The shortest useful path through the book looks like this:

1. [Chapter 1. Why an Agent Needs a Platform, Not Magic](book/part-i/chapter-1.en.md)
2. [Chapter 3. Security Perimeter and Trust Boundaries](book/part-ii/chapter-3.en.md)
3. [Chapter 8. Execution Model and Tool Catalog](book/part-iv/chapter-8.en.md)
4. [Part V. Reliability and Observability](book/part-v/index.en.md)
5. [Chapter 18. Production Rollout Checklist](book/part-vii/chapter-18.en.md)

## What Already Exists Here

- Published Russian core manuscript across eight book parts, from architectural foundations to lifecycle governance.
- Draft `en` and `zh` translation layers that are useful for reading, but still going through editorial cleanup.
- The runnable `agent_runtime_ref` reference package.
- Reference pages for traces, evals, policy bundles, approvals, memory, and lifecycle artifacts.
- Practical case studies, checklists, policy templates, and a glossary.
- Active editorial pass on the book manuscript and public site surface.

## What the Book Is Not Trying To Be

This is not a manual for one framework, not a prompt-trick collection, and not a tour of the AI market. The book sits above specific SDKs and platform docs and asks harder questions instead: what an agent should be allowed to do, how to constrain the write path, what to observe, how to ship changes, and who owns the system after launch.

## Where To Go Next

<div class="button-stack" markdown="1">

[Start Here](start-here.en.md){ .md-button .md-button--primary }
[Go to Part I](book/part-i/index.en.md){ .md-button }
[Open the Reference Package](appendix/reference-package.en.md){ .md-button }

</div>
