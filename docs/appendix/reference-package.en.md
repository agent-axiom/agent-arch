# Reference Package

The repository now includes a small runnable skeleton: [agent_runtime_ref](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref).

Its job is not to become a production framework. It exists as a minimal code anchor for **Part VII** of the book.

## What Is Inside

- [runtime.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/runtime.py)
  The main `AgentRuntime`, which assembles run context, retrieval, the model step, tool execution, and the background update hook.
- [policy.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/policy.py)
  A small policy engine with structured decisions.
- [catalog.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/catalog.py)
  A capability registry with operational semantics.
- [config.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/config.py)
  A YAML loader for policy, capability catalog, and rollout policy.
- [memory.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/memory.py)
  Typed memory records, retrieval, and a tenant-scoped in-memory store.
- [background.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/background.py)
  A background maintenance path for persistent memory writes and compaction.
- [execution.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/execution.py)
  A simple capability dispatch layer through contract-aware execution.
- [telemetry.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/telemetry.py)
  An in-memory telemetry emitter for structured events and spans.
- [rollout.py](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/rollout.py)
  A minimal readiness gate before rollout.

## How to Run It

```bash
.venv/bin/python -m agent_runtime_ref
```

Expected output:

```json
{"result": "Ticket request accepted and ready for follow-up.", "status": "success", "events": 9, "memory_records": 4, "config_dir": ".../agent_runtime_ref/configs"}
```

Explicit runtime execution via subcommand:

```bash
.venv/bin/python -m agent_runtime_ref simulate-run
```

Inspect memory records:

```bash
.venv/bin/python -m agent_runtime_ref inspect-memory --memory-class profile
```

Dump structured events for one run:

```bash
.venv/bin/python -m agent_runtime_ref dump-events --user-input "Please open a ticket for this issue."
```

Rollout policy check with signal overrides:

```bash
.venv/bin/python -m agent_runtime_ref check-rollout --signal offline_eval_pass=false
```

A request that actually reads profile memory:

```bash
.venv/bin/python -m agent_runtime_ref simulate-run --user-input "What language preference do you remember?"
```

## How to Verify It

```bash
uv run ruff check .
uv run ty check
.venv/bin/python -m unittest discover -s tests
```

## Sample Configs

There are four starter files in [configs](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs):

- [policy.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/policy.yaml)
- [capabilities.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/capabilities.yaml)
- [memory.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/memory.yaml)
- [rollout.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/rollout.yaml)

These are no longer just static examples. `config.py` can load those YAML files into the runtime, the policy engine, the memory store, and the rollout policy, so the package is now closer to a real operational skeleton.

## Why This Is Useful

The book now relies not only on Markdown explanations, but also on a real code skeleton:

- it is easier to discuss architecture at the level of files and contracts;
- it is easier to extend the package with more examples;
- it is easier to move from a chapter to a runnable prototype;
- it is easier to show a config-driven path instead of only a hardcoded demo;
- it is easier to connect the reference runtime to the chapters about memory, retrieval, and background updates.

There is also a practical usability win now:

- `inspect-memory` shows seeded memory and filtering by `tenant` and `memory_class`;
- `dump-events` shows the structured trace of one run without reading the source code.
