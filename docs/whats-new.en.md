# What's New

This page is a short reader-facing log of major additions to the book and reference runtime. It is not a replacement for git history; it exists to show that the project is active and what is already here.

_Current as of April 29, 2026._

## Book

### Part VIII on the lifecycle of agent systems

The book now includes a full block on `SDLC -> ADLC`, change management, assurance loops, supply chain, retirement, misalignment, behavioral evals, AI-native observability, and inventory control.

Why it matters: the site now covers not only architecture and rollout, but the lifecycle of an agent system after release.

### A stronger production contour across Parts I-V

The book now includes sharper bridges between architecture, retrieval, execution, and eval discipline:

- Part I now separates runtime architecture more explicitly from the training layer and the product surface;
- Part II now gives a clearer taxonomy for `prompt injection`, `jailbreaking`, and `action hallucination`;
- Part III now strengthens the retrieval contour with `semantic gap`, `HyDE`, `RAG first`, and a clearer distinction between continued pretraining and `SFT`;
- Part IV now adds practical guidance for large tool catalogs, `semantic tool filtering`, and explicit `MCP host / client / server` roles;
- Part V now adds a stronger product framing for `latency budget` and a more practical treatment of `LLM-as-a-judge`.

Why it matters: the book now covers not only the baseline platform layers, but also the everyday production questions that tend to surface between design review, eval loops, and rollout.

## Reference

### A reusable reference layer

The site now includes reference pages for:

- traces and event catalog;
- eval datasets and grading contracts;
- policy bundles and approvals;
- change review and rollout gates;
- lifecycle artifacts;
- memory retrieval contracts.

Why it matters: readers can now move directly from explanatory chapters to reviewable schemas and contract artifacts.

## Runtime

### Runnable reference runtime

The repository includes [`agent_runtime_ref`](https://github.com/agent-axiom/agent-arch/tree/main/agent_runtime_ref), a small runnable package that now supports:

- approvals and delegated authorization context;
- controls and lifecycle runtime-control inspection;
- lifecycle artifacts;
- session export and replay summaries;
- eval dataset export;
- trace export with redaction, redacted summaries, replay preservation, and schema versioning.

Why it matters: the book is now backed by runnable code, not only narrative documentation.

## Practical Appendix

### A stronger practical appendix

The site now includes:

- a glossary;
- cheat sheets;
- case studies;
- policy templates;
- a research frontier page;
- a community roadmap.

Why it matters: readers have fast access to checklists, case studies, glossary entries, and practical assets without reading the entire book linearly.

## Navigation

### Stronger entry pages

Updated:

- [Start Here](start-here.en.md);
- [Reference Layer](reference.en.md);
- [Cheat Sheets](appendix/cheat-sheets.en.md).

Those pages now make it easier to find short paths into topics such as:

- `semantic tool filtering`;
- `HyDE` and `RAG vs training`;
- `latency budget` and routed pipelines;
- `LLM-as-a-judge` and judge calibration;
- the difference between `prompt injection`, `jailbreaking`, and `action hallucination`.

Why it matters: the new topics are now visible not only inside individual chapters, but also at the reader entry-point level.

## Publish Readiness

### A cleaner site before publication

Before the next deploy, a publisher-facing quality pass was started and moved forward:

- draft and planning pages are excluded from the published site and sitemap;
- OpenGraph/Twitter metadata and a social preview image were added;
- the search index, sitemap, robots file, local assets, anchors, alt text, and external links were checked;
- the READMEs in all three languages now include a fast-forward publish checklist for `main` and `docs-prod`.

Why it matters: the published site should keep moving toward a polished reader-facing product, not feel like a raw build of Markdown files.

## What this means for readers

- You can use the book as a handbook.
- You can reuse the reference pages as engineering starting points.
- You can run the example runtime instead of reading only Markdown.
- You can anchor the architecture in recent material from OpenAI, Anthropic, Google, Microsoft, and NIST.

## Continue

- [Start Here](start-here.en.md)
- [Reference Layer](reference.en.md)
- [Book Plan](book/plan.en.md)
- [Sources](appendix/sources.en.md)
