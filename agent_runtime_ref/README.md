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

For the record-linkage view across traces, approvals, evals, incidents, and rollout judgment, read [Evidence Spine: From Request to Rollout Judgment](../docs/book/part-v/evidence-spine.en.md).

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
python3 -m agent_runtime_ref inspect-session --simulate-failure tool_timeout
python3 -m agent_runtime_ref check-controls --signal policy_traces_present=false
python3 -m agent_runtime_ref check-change --signal failed_run_drill_checked=false
python3 -m agent_runtime_ref simulate-run --simulate-failure tool_timeout
python3 -m agent_runtime_ref export-events --simulate-failure upstream_unavailable --output /tmp/agent-runtime-failed-trace.jsonl
python3 -m agent_runtime_ref session-eval-summary --simulate-failure tool_timeout
python3 -m agent_runtime_ref session-replay --simulate-failure tool_timeout --user-input "Please create a ticket for this issue."
python3 -m agent_runtime_ref export-session --simulate-failure tool_timeout --output /tmp/agent-runtime-failed-session.json
python3 -m agent_runtime_ref export-eval-dataset --output /tmp/agent-runtime-eval.json
python3 -m agent_runtime_ref export-eval-dataset --scenario failed_run_timeout --output /tmp/agent-runtime-failed-eval.json
```

The failure-injection flags are intentionally small, but useful for the book's failure-rich runtime examples: they let the reference runtime execute explicit failed runs, emit `run_failed` trace events, and keep the concrete failure reason visible in runtime output and CLI JSON as `failure_reason` instead of collapsing everything into happy-path or approval-wait scenarios.

That same line now also reaches the rollout/change side of the package: the demo `change.yaml` includes a `failed_run_drill_checked` gate signal so degraded paths are part of release review, not an afterthought. `inspect-lifecycle` now surfaces both failed-run gate signals and `failed_run_archive_targets` directly, `check-change` breaks out `missing_failed_run_signals`, `check-retirement` exposes the same `failed_run_archive_targets` that must survive shutdown, and `check-controls` now isolates failed-run-related control gaps through `failed_run_controls` while also naming `preserved_failed_run_controls` and a top-level `failed_run_controls_healthy` summary, so operators can see lifecycle and control-plane expectations without opening the YAML first.

The eval export now also includes a dedicated failed-run scenario, so the same reference package can demonstrate not only failed traces, but failed-run judgment artifacts and session summaries with `traceable_failed_runs`. That path is now covered by the local pytest suite too, so the package's degraded-path examples are executable rather than only described, and the same failed condition is surfaced consistently through `failure_reason` in session export and CLI output. The `export-eval-dataset` command summary now also returns aggregate `failed_runs`, `traceable_failed_runs`, and `latest_failure_reason`, so operators can confirm degraded-path coverage without opening the JSON artifact first.

The same is now true for `inspect-session`, `session-eval-summary`, `session-replay`, and `export-session`: failed drills can be replayed directly into session-level inspection surfaces, and the command summaries surface `failed_runs`, `traceable_failed_runs`, and the latest failure reason instead of leaving the operator to inspect raw JSON first. Those session surfaces also keep delegated-authorization context next to failed-run evidence, so operators can review both failure cause and acting identity in one place. `inspect-approvals` now follows that same line by exposing delegated authorization context directly in approval inspection output, and `resolve-approval` returns the same context after a decision so approval lineage stays visible through closure as well.

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
