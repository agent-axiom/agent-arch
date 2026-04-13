# agent_runtime_ref

Small runnable reference runtime for Parts VII and VIII of the book.

## What it is

This package is not a production framework. It is a compact code anchor for:

- runtime structure
- policy and capability control
- approval pause/resume flow
- rollout gates
- lifecycle artifacts
- trace/session/eval exports

The full narrative lives in the book and appendix pages. This README is only a local developer quickstart.

## Quickstart

From the repository root:

```bash
python3 -m agent_runtime_ref
```

Other useful commands:

```bash
python3 -m agent_runtime_ref inspect-agent
python3 -m agent_runtime_ref inspect-memory --memory-class profile
python3 -m agent_runtime_ref inspect-approvals
python3 -m agent_runtime_ref inspect-lifecycle
python3 -m agent_runtime_ref export-eval-dataset --output /tmp/agent-runtime-eval.json
```

## Tests

Project test config lives at the repository root in `pyproject.toml`.

Install dev dependencies first, for example with `uv`:

```bash
uv sync --group dev
uv run pytest
```

Or with pip:

```bash
python3 -m pip install -e .
python3 -m pip install pytest pytest-cov
python3 -m pytest
```

## Reading path

- Chapter 17, policy layer and capability contracts
- Chapter 18, rollout gates around approval and runtime behavior
- Chapter 21, assurance response
- Chapter 22, artifact and lifecycle linkage
