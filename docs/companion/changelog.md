# Companion changelog

Status: public practice draft, unreleased (2026-10-03).

The previous practice baseline was
`6fa79caa76d53b82953f285f8452b9b0ccd6c50d`. The corrections below require a
commit containing them; pin that exact revision when reproducing the corrected
exercise. This is not a published book-edition release.
No `v1.0-book` tag exists as of this draft.

## Unreleased

- Added `examples/export_policy_trace_pair.py` to export one deterministic
  `search_docs` request through the normal reference policy/execution path with
  allow and deny configurations. It preserves source configs and existing
  output evidence. Tests cover both outcomes and verify that deny stops before
  the executor's post-policy stage. The adapter remains synthetic and offline.
- Replaced the fixed rejection JSON in
  `examples/run_lab_negative_scenario.py` with a version and lease-owner check
  before a local side-effect callback. The stale attempt has no callback effect;
  a positive control accepts the current claim and records its callback effect.
- Preserved the existing `stale-run-completion` result fields and added the
  `lab26-negative-lease` scenario alias. The `scenario` field echoes the name
  used. New `side_effects`, `positive_control` and `evidence_scope` fields expose
  the observed callback effects and the local, sequential scope of the check.
- Added focused tests for version mismatch independently of owner mismatch,
  missing or incorrect lease owner, valid completion, callback failure, and
  CLI JSON export under both scenario names.
- Clarified the public practice draft status and recorded the baseline
  limitation in [Errata](errata.md). Existing templates, checklists and example
  artifacts remain working practice materials, not an edition release.

## Proposed release versioning

- `v1.0-book`: reserved for materials matching the first published book edition;
  this tag has not been created.
- `v1.0.x`: typo fixes and small clarifications.
- `v1.1`: new templates, new cases or materially changed guidance.
- `main`: current working state, not an immutable book-edition reference.

These are proposed naming rules, not announcements of existing releases or tags.
