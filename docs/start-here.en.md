# Start Here

If you just arrived at this book, you do not need to read it strictly from top to bottom. This is not a novel and not a survey of everything in the AI ecosystem. It is a practical handbook on how to build safe, controllable AI agents without turning the project into a pile of prompts, scripts, and hope.

This page exists for two reasons:

- to help you decide quickly whether this book is relevant to you;
- to give you a short reading path for your specific role.

If you want the high-level message of the book, use the [homepage](index.en.md). If you need structure and current status, open the [book plan](book/plan.en.md).

## Who This Book Is For

This book is especially useful if you are:

- an engineer building agent features into a product;
- a platform engineer trying to assemble a shared runtime and policy layer;
- a security engineer who needs to reason about trust boundaries and risky execution paths;
- a tech lead or architect trying to keep an agent system inside production discipline;
- an open source contributor looking for a practical handbook instead of an AI marketing page.

If you want a calm, mature system instead of "the most autonomous agent in the world," you are in the right place.

## What You Can Take Away in 30 Minutes

If you only have a short window, I would read this path:

1. [Chapter 1. Why Agents Need a Platform, Not Magic](book/part-i/chapter-1.en.md)
2. [Chapter 3. Security Perimeter and Trust Boundaries](book/part-ii/chapter-3.en.md)
3. [Chapter 8. Execution Model and Tool Catalog](book/part-iv/chapter-8.en.md)
4. [Chapter 11. Traces, Spans, and Structured Events](book/part-v/chapter-11.en.md)
5. [Chapter 18. Production Rollout Checklist](book/part-vii/chapter-18.en.md)

After those five chapters, you will already have:

- a working architectural frame;
- a model for trust boundaries;
- a picture of safe tool execution;
- a practical observability baseline;
- a production go-live discipline.

## Reading Paths by Role

### If You Are a Product Engineer

I would go in this order:

1. [Part I. Foundations](book/part-i/index.en.md)
2. [Part II. Security Perimeter](book/part-ii/index.en.md)
3. [Part IV. Tools and Execution](book/part-iv/index.en.md)
4. [Part VII. Reference Implementation](book/part-vii/index.en.md)

The goal of this route is to move quickly from an agent idea to a runnable architecture.

### If You Are a Platform Engineer

I would go in this order:

1. [Chapter 2. Reference Architecture for a Safe Agent](book/part-i/chapter-2.en.md)
2. [Part III. Memory and Knowledge](book/part-iii/index.en.md)
3. [Part IV. Tools and Execution](book/part-iv/index.en.md)
4. [Part V. Reliability and Observability](book/part-v/index.en.md)
5. [Part VII. Reference Implementation](book/part-vii/index.en.md)

The goal of this route is to build a platform-grade skeleton, not only an agent wrapper.

### If You Are a Security Engineer

I would go in this order:

1. [Part II. Security Perimeter](book/part-ii/index.en.md)
2. [Chapter 5. Why Agents Need Memory and Why It Is Dangerous](book/part-iii/chapter-5.en.md)
3. [Chapter 9. Sandbox Execution and MCP as an Integration Contract](book/part-iv/chapter-9.en.md)
4. [Chapter 10. Idempotency, Retries, Rate Limits, and Rollback Boundaries](book/part-iv/chapter-10.en.md)
5. [Chapter 18. Production Rollout Checklist](book/part-vii/chapter-18.en.md)

The goal of this route is to understand not only prompt risks, but real execution risks.

### If You Are a Lead or Architect

I would go in this order:

1. [Chapter 1. Why Agents Need a Platform, Not Magic](book/part-i/chapter-1.en.md)
2. [Part V. Reliability and Observability](book/part-v/index.en.md)
3. [Part VI. Organizational Model](book/part-vi/index.en.md)
4. [Chapter 18. Production Rollout Checklist](book/part-vii/chapter-18.en.md)

The goal of this route is to understand how not to let an agent initiative collapse at the operational and ownership layers.

## If You Want Code First

If runnable artifacts matter more to you than linear reading, start here:

- [Reference Package](appendix/reference-package.en.md)
- [Chapter 16. Baseline Runtime Blueprint](book/part-vii/chapter-16.en.md)
- [Chapter 17. Policy Layer and Capability Catalog](book/part-vii/chapter-17.en.md)

Those pages already give you:

- a minimal runtime;
- a policy layer;
- a capability catalog;
- a memory path;
- telemetry;
- rollout checks.

## If You Want Templates and Project Direction

Start with these pages:

- [Book Plan](book/plan.en.md)
- [Glossary](appendix/glossary.en.md)
- [Cheat Sheets](appendix/cheat-sheets.en.md)
- [Practical Case Studies](appendix/case-studies.en.md)
- [Policy Templates and Checklists by Use Case](appendix/policy-templates.en.md)
- [Community Roadmap](appendix/community-roadmap.en.md)
- [Sources](appendix/sources.en.md)

That is the shortest way to understand where the project is going and how it can help the wider community.

## What Makes This Book Different

The stance of this book is straightforward:

- workflow matters more than magic;
- safety matters more than a flashy demo;
- the execution layer matters more than "smart tool calling";
- observability matters more than the feeling that "it seems to work";
- platform thinking matters more than a collection of local agent hacks.

So this is not a book about "the most autonomous agent." It is a book about a mature, safe, explainable agent platform.

## Where to Go Next

If you want to start right now:

- [Open the Book Plan](book/plan.en.md){ .md-button .md-button--primary }
- [Go to Part I](book/part-i/index.en.md){ .md-button }
- [Open the Reference Package](appendix/reference-package.en.md){ .md-button }

If you want to contribute:

- [Contributing guide](https://github.com/agent-axiom/agent-arch/blob/main/CONTRIBUTING.md)
- [Community Roadmap](appendix/community-roadmap.en.md)
