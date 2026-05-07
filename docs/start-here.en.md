# Start Here

If you just arrived at this book, start with one question: do you need an impressive demo agent, or a system that can survive production reality?

This book is written for the second case. It is most useful when read as one argument about how agent systems mature: from prompt-heavy prototypes to governed systems with trust boundaries, a policy layer, approvals, observability, evals, and lifecycle discipline.

Building agents is boring, but the result is staggering: discipline around trust boundaries, traces, approvals, and rollout turns a demo into a system that can be improved safely.

This page exists for one reason: to help you choose a reading route quickly.

## If You Read Only One Thing

If you want the shortest entry into the book's thesis, read [Chapter 1. Why an Agent Needs a Platform, Not Magic](book/part-i/chapter-1.en.md).

That chapter states the main claim plainly: a production agent system cannot be built as "a model plus some tools." It has to be designed as a governed operational system.

## What Kind of Book This Is

This is not a guide to one framework and not a catalog of AI features. It is a practical architecture book for teams that need to run agents in real environments with write paths, human approvals, access boundaries, telemetry, evals, and explicit operational ownership.

## A 30-Minute Route

If you have little time, read this path:

1. [Chapter 1. Why an Agent Needs a Platform, Not Magic](book/part-i/chapter-1.en.md)
2. [Chapter 3. Security Perimeter and Trust Boundaries](book/part-ii/chapter-3.en.md)
3. [Chapter 8. Execution Model and Tool Catalog](book/part-iv/chapter-8.en.md)
4. [Part V. Reliability and Observability](book/part-v/index.en.md)
5. [Chapter 18. Production Rollout Checklist](book/part-vii/chapter-18.en.md)

After that route, you should already have a working frame for:

- where the real trust boundaries of an agent live;
- what safe tool execution looks like;
- why a smart model is not enough without traces, SLO, and evals;
- what is required before the first serious rollout.

## Reading Paths by Role

### If You Are a Product Engineer

1. [Part I. Foundations](book/part-i/index.en.md)
2. [Part II. Security Perimeter](book/part-ii/index.en.md)
3. [Part IV. Tools and Execution](book/part-iv/index.en.md)
4. [Part VII. Reference Implementation](book/part-vii/index.en.md)

This route is for moving quickly from an agent idea to a runnable architecture.

### If You Are a Platform Engineer

1. [Chapter 2. Reference Architecture for a Safe Agent](book/part-i/chapter-2.en.md)
2. [Part III. Memory and Knowledge](book/part-iii/index.en.md)
3. [Part IV. Tools and Execution](book/part-iv/index.en.md)
4. [Part V. Reliability and Observability](book/part-v/index.en.md)
5. [Part VII. Reference Implementation](book/part-vii/index.en.md)

This route is for teams assembling a platform skeleton, not just a thin wrapper around one model.

### If You Are a Security Engineer

1. [Part II. Security Perimeter](book/part-ii/index.en.md)
2. [Chapter 5. Why an Agent Needs Memory, and Why Memory Is Risky](book/part-iii/chapter-5.en.md)
3. [Chapter 9. Sandbox Execution and MCP as an Integration Contract](book/part-iv/chapter-9.en.md)
4. [Chapter 10. Idempotency, Retries, Rate Limits, and Rollback Boundaries](book/part-iv/chapter-10.en.md)
5. [Chapter 18. Production Rollout Checklist](book/part-vii/chapter-18.en.md)

This route is useful if you need to see not only model risk, but real execution risk.

### If You Are a Lead or Architect

1. [Chapter 1. Why an Agent Needs a Platform, Not Magic](book/part-i/chapter-1.en.md)
2. [Part V. Reliability and Observability](book/part-v/index.en.md)
3. [Part VI. Organizational Model](book/part-vi/index.en.md)
4. [Chapter 18. Production Rollout Checklist](book/part-vii/chapter-18.en.md)

This route is for keeping an initiative inside real operational discipline instead of shipping only a demo.

## If You Want Code and Artifacts First

If executable support matters more than linear reading, start here:

- [Reference Package](appendix/reference-package.en.md)
- [Chapter 16. Baseline Runtime Blueprint](book/part-vii/chapter-16.en.md)
- [Chapter 17. Policy Layer and Capability Catalog](book/part-vii/chapter-17.en.md)
- [Reference Pages](reference.en.md)

This is useful if you want a runtime skeleton, policy contracts, memory paths, telemetry, and rollout artifacts right away.

## If You Need To Solve One Specific Problem Fast

### Safe Tool Execution

- [Chapter 4. Tool Gateway, Approval, and Audit Trail](book/part-ii/chapter-4.en.md)
- [Chapter 8. Execution Model and Tool Catalog](book/part-iv/chapter-8.en.md)
- [Chapter 9. Sandbox Execution and MCP as an Integration Contract](book/part-iv/chapter-9.en.md)
- [Chapter 10. Idempotency, Retries, Rate Limits, and Rollback Boundaries](book/part-iv/chapter-10.en.md)

### Memory and Retrieval

- [Chapter 5. Why an Agent Needs Memory, and Why Memory Is Risky](book/part-iii/chapter-5.en.md)
- [Chapter 6. Short-Term, Long-Term, and Profile Memory](book/part-iii/chapter-6.en.md)
- [Chapter 7. Retrieval, Compaction, and Background Updates](book/part-iii/chapter-7.en.md)
- [Memory Record and Retrieval Contract Schema](appendix/memory-retrieval-schema.en.md)

### Observability, Evals, and Rollout

- [Chapter 11. Traces, Spans, and Structured Events](book/part-v/chapter-11.en.md)
- [Chapter 13. Offline Evals, Online Evals, and Regression Gates](book/part-v/chapter-13.en.md)
- [Chapter 18. Production Rollout Checklist](book/part-vii/chapter-18.en.md)
- [Chapter 20. Change Management for Agent Systems](book/part-viii/chapter-20.en.md)

## What To Keep Open Next to the Book

- [Book Plan](book/plan.en.md)
- [Why This Book Exists](appendix/why-this-book.en.md)
- [Glossary](appendix/glossary.en.md)
- [Cheat Sheets](appendix/cheat-sheets.en.md)
- [Sources](appendix/sources.en.md)

If this book feels closer to you than another AI landing page about "autonomy," you are in the right place.
