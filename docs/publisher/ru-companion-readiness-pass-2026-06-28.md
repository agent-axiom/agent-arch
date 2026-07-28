# Companion readiness pass

Date: 2026-06-28.

Status: stronger editor-handoff companion package, not ready for public book
release until author-owned URL/version/license inputs are filled.

## Verdict

The online companion is strong enough to support editorial review because it has
the expected routes, runtime reference pages, release-candidate templates,
release-candidate checklist, executable example artifacts, changelog and errata
policy. It is not yet release-ready because public URL/version/license metadata
remain open.

## Current companion inventory

Companion docs:

- `docs/companion/index.md`
- `docs/companion/changelog.md`
- `docs/companion/errata.md`
- `docs/companion/runtime-reference/cli.md`
- `docs/companion/runtime-reference/configs.md`
- `docs/companion/runtime-reference/eval-datasets.md`
- `docs/companion/runtime-reference/traces-and-events.md`
- `docs/companion/templates/index.md`
- `docs/companion/templates/capability-contract.md`
- `docs/companion/templates/incident-record.md`
- `docs/companion/templates/release-decision-record.md`
- `docs/companion/checklists/index.md`
- `docs/companion/checklists/production-readiness.md`
- `docs/companion/artifacts/trace-demo.jsonl`
- `docs/companion/artifacts/trace-failed-tool-timeout.jsonl`
- `docs/companion/artifacts/session-failed-tool-timeout.json`
- `docs/companion/artifacts/eval-failed-run-timeout.json`

Runtime/config anchor:

- `agent_runtime_ref/README.md`
- `agent_runtime_ref/__main__.py`
- `agent_runtime_ref/configs/agent.yaml`
- `agent_runtime_ref/configs/approvals.yaml`
- `agent_runtime_ref/configs/artifacts.yaml`
- `agent_runtime_ref/configs/capabilities.yaml`
- `agent_runtime_ref/configs/change.yaml`
- `agent_runtime_ref/configs/controls.yaml`
- `agent_runtime_ref/configs/memory.yaml`
- `agent_runtime_ref/configs/policy.yaml`
- `agent_runtime_ref/configs/retirement.yaml`
- `agent_runtime_ref/configs/rollout.yaml`
- `agent_runtime_ref/configs/runtime-controls.yaml`

## What is already usable

- Companion index explains what lives online vs in print.
- Runtime CLI page lists operational command surfaces.
- Runtime reference has configs, trace/event and eval dataset routes.
- Template routes exist for capability contract, release decision record and
  incident record, with release-candidate headers.
- Checklist route exists for production readiness, with owner/use-case/version
  notes.
- Example artifacts exist for trace, failed trace, session export and eval
  dataset review.
- Changelog defines a book-versioning policy.
- Errata page defines a correction policy.
- `agent_runtime_ref` is covered by repository tests and can serve as the
  executable proof anchor for chapters 21-23.

## Release blockers

### P0: public URL and version

`docs/companion/errata.md` still says the public companion URL and first book
release version are not finalized. These must be filled before publication.

### P1: companion/source cross-links

The book promises that long YAML/CLI/runtime/reference material lives in the
companion. Before final submission, high-value references in chapters 21-23 and
appendices should point to stable companion routes rather than internal source
paths.

### P1: remaining examples

The companion now includes generated trace/session/eval artifacts. Before
public release, add example filled records for release decision, incident
record, capability contract and production readiness checklist.

## Editor note

For the current editor handoff, the companion should be treated as a boundary
artifact: it proves that detailed runtime material has a home outside the book.
The editor does not need to validate every command yet, but should flag any
place where the print manuscript relies on companion material that is not
currently represented by a route.

## Author-owned companion inputs

- Public companion URL.
- Public repository URL, if different.
- Release version for the first book edition.
- Errata route.
- Changelog route.
- License or usage terms for templates.
- Whether issues/discussions are enabled.
