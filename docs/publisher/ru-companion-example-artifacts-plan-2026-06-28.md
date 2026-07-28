# Companion example artifacts plan

Date: 2026-06-28.

Status: initial executable artifact set generated; remaining examples tracked
for the final companion release.

## Generated artifacts

These artifacts are generated from `agent_runtime_ref` and are safe to use as
companion examples for editor review. They are examples, not production
records.

| Artifact | Source command | Purpose |
| --- | --- | --- |
| `docs/companion/artifacts/trace-demo.jsonl` | `uv run python -m agent_runtime_ref export-events --output docs/companion/artifacts/trace-demo.jsonl` | Happy-path/approval-wait trace showing policy, retrieval, approval and run completion evidence. |
| `docs/companion/artifacts/trace-failed-tool-timeout.jsonl` | `uv run python -m agent_runtime_ref export-events --simulate-failure tool_timeout --output docs/companion/artifacts/trace-failed-tool-timeout.jsonl` | Failed-run trace showing `tool_timeout`, `run_failed` and terminal failure evidence. |
| `docs/companion/artifacts/trace-post-dispatch-timeout.jsonl` | `uv run python -m agent_runtime_ref export-events --simulate-failure post_dispatch_timeout --output docs/companion/artifacts/trace-post-dispatch-timeout.jsonl` | Unknown-effect trace showing `side_effect_unknown`, the reconciliation event and a blocked retry path. |
| `docs/companion/artifacts/session-failed-tool-timeout.json` | `uv run python -m agent_runtime_ref export-session --simulate-failure tool_timeout --output docs/companion/artifacts/session-failed-tool-timeout.json` | Session-level evidence linking failed and subsequent runs. |
| `docs/companion/artifacts/eval-failed-run-timeout.json` | `uv run python -m agent_runtime_ref export-eval-dataset --scenario failed_run_timeout --output docs/companion/artifacts/eval-failed-run-timeout.json` | Regression seed for a known pre-dispatch failure and failed-run traceability. |
| `docs/companion/artifacts/eval-unknown-effect-reconciliation.json` | `uv run python -m agent_runtime_ref export-eval-dataset --scenario unknown_effect_reconciliation --output docs/companion/artifacts/eval-unknown-effect-reconciliation.json` | Duplicate-ticket guard seed for an unknown post-dispatch effect and mandatory reconciliation. |

## How these support the book

- Chapters 13-16 can point to trace, session and eval evidence without printing
  long JSON/JSONL blocks.
- Chapters 21-23 can use the artifacts as proof that the reference runtime has
  executable surfaces, not only prose descriptions.
- Appendix/source material can keep the full payloads online while the book
  explains the architectural decision behind them.

## Remaining release artifacts

Before public companion release, add:

- release decision record example;
- incident record example;
- capability contract example;
- production readiness checklist example;
- redacted trace example;
- approval-resolution example;
- rollout gate example.

## Regeneration rule

Regenerate these artifacts whenever `agent_runtime_ref` CLI output contracts
change. The companion release should never contain stale JSON/JSONL surfaces
that no longer match the executable reference package.

Verification commands:

```bash
uv run python -m agent_runtime_ref inspect-trace --input docs/companion/artifacts/trace-demo.jsonl
uv run python -m agent_runtime_ref inspect-trace --input docs/companion/artifacts/trace-failed-tool-timeout.jsonl
python3 -m json.tool docs/companion/artifacts/session-failed-tool-timeout.json
python3 -m json.tool docs/companion/artifacts/eval-failed-run-timeout.json
```
