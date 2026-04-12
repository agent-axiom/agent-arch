# Rust vs Python and TypeScript for Agent Platforms

This page does not answer “which language is better in general”. It answers a more useful question:

**which language is the better fit for a specific layer of an agent platform today**.

## Short answer

For most teams in 2026, the practical setup looks like this:

- **Python** or **TypeScript** for the fastest iteration around agent behavior;
- **Rust** for long-lived platform services where strict contracts, performance, and reliability matter most;
- a mixed stack is usually better than forcing a single-language ideology.

## Decision matrix

| Criterion | Rust | Python | TypeScript |
| --- | --- | --- | --- |
| Fast applied iteration | weaker | very strong | very strong |
| Vendor SDK maturity around agents | uneven | strong | strong |
| Strict contract services | very strong | medium | medium |
| Gateway/runtime performance | very strong | weaker | medium |
| Infrastructure network services | very strong | medium | medium |
| Eval and experiment loop | medium | very strong | strong |
| MCP server and integration layer | strong | strong | strong |
| Control plane and policy enforcement | very strong | medium | medium |

## When to choose Rust

Rust is especially justified when you are building:

- a shared tool gateway;
- a policy engine;
- an approval service;
- a trace ingestion pipeline;
- an audit-oriented control plane;
- an MCP server with strict reliability requirements;
- a memory or indexing service under heavier load.

In those places the language helps make the system drier, more stable, and more predictable.

## When to choose Python

Python is usually the best choice when you need to:

- change agent behavior quickly;
- iterate on prompts, routines, and evals;
- stay close to a data-heavy stack;
- use the freshest examples from model providers;
- run research-heavy or experiment-heavy workflows.

Python wins most often when the real bottleneck is not service performance but team learning speed.

## When to choose TypeScript

TypeScript is especially practical when:

- most of the product already lives in the JS/TS ecosystem;
- the agent sits close to the web/backend application;
- a shared type model across frontend, backend, and tool contracts matters;
- the team wants to ship applied integrations quickly without changing stacks.

TypeScript is often the most practical language for the product-facing agent layer.

## Where a mixed stack is usually better

For real teams, the healthiest setup often looks like this:

1. Product-facing behavior and experiments live in Python or TypeScript.
2. Gateways, policies, approvals, and observability move into stricter services over time.
3. Rust appears where the platform becomes a long-lived engineering system, not just a fast experimentation layer.

That is usually better than arguing about the “right language” before the actual platform constraints are clear.

## Common mistakes

- choosing Rust too early for language purity;
- keeping Python in a high-throughput gateway that is already bottlenecked by infrastructure constraints;
- forcing TypeScript into low-level control-plane components only because it already exists in the product;
- picking the language before you know where the long-term operational burden will live.

## Practical rule

If the layer is primarily about:

- **behavior iteration** — usually Python/TypeScript;
- **platform control** — usually Rust;
- **product integration** — often TypeScript;
- **eval and experimentation** — often Python.

## What to Do Right Away

Before choosing a language, it helps to fix:

- where the trust boundary sits;
- which services will be long-lived;
- where the strongest contract layer is needed;
- which vendor SDKs are actually required;
- where delivery speed matters more than operating reliability, and where the reverse is true.

After that, the language choice becomes much less ideological.

## Conclusion

For agent systems today, the right answer is rarely “everything in Rust” or “everything in Python”.

The more mature answer is usually:

- **Python/TypeScript** accelerate agent behavior development;
- **Rust** strengthens the platform layer around that behavior.

That is why Rust fits the book best as a language for **agent platform services**, not as the single mainline path for building agents.

## What to Do Next

- [Rust for Agent Platforms](rust-agent-platforms.en.md)
- [Chapter 8. Execution Model and Tool Catalog](../book/part-iv/chapter-8.en.md)
- [Chapter 17. Policy Layer and Capability Catalog](../book/part-vii/chapter-17.en.md)
- [Reference Package](reference-package.en.md)
- [Sources](sources.en.md)
