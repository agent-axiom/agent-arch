# Ruff Suppression Policy And Complexity Refactoring Design

## Goal

Adopt `ruff-policy-hooks` as an enforced repository guardrail and remove every
existing `C901` and `PLR0912` violation without weakening Ruff's default
complexity thresholds, adding protected suppressions, or changing observable
runtime and publishing behavior.

## Current State

The repository uses Ruff 0.15.x from the development dependency group. Its
configuration selects `E`, `F`, and `I`, but the repository has no pre-commit
configuration and CI does not currently run Ruff or a suppression-policy hook.

A diagnostic Ruff pass over all 50 tracked Python files found 45 diagnostics at
29 function locations in 13 files when `C901` and `PLR0912` are selected. A
separate pass with the existing rule set found six tracked `E` or `I`
diagnostics. One large publisher script contains a file-level
`# ruff: noqa: E501`; that unrelated suppression is outside the new protected
policy and is not part of this refactoring.

The working tree also contains unrelated publisher documentation, generated
artifacts, and `.tmp` files. They belong to existing work and must not be
modified, staged, or committed as part of this change.

## Chosen Approach

Use incremental, behavior-preserving helper extraction. Each complex function
will retain its public entry point while cohesive branches move into named,
testable helpers. Prefer early returns, data-driven dispatch, and small pure
transformations where they make the existing control flow clearer. Introduce a
new class or strategy abstraction only when the code already represents a
stable domain boundary; do not add abstractions solely to satisfy a metric.

Rejected alternatives are a large structural rewrite, which creates
unnecessary regression risk, and Ruff per-file ignores or raised thresholds,
which would contradict the requirement to remediate every violation.

## Policy And Tooling Integration

1. Extend Ruff's selected rules with the exact codes `C901` and `PLR0912`.
   Keep the default thresholds of complexity greater than 10 and branches
   greater than 12.
2. Add `.pre-commit-config.yaml` with `ternaus/ruff-policy-hooks` pinned to tag
   `v0.4.0`, hook ID `check-ruff-suppressions`, and
   `--protect=C901,PLR0912`.
3. Add `pre-commit` to the development dependency group and update `uv.lock`.
4. Add a dedicated quality workflow that runs the repository's Ruff check and
   `pre-commit run --all-files` for every pull request, every push to `main`,
   and manual dispatch. The policy hook itself does not run Ruff, so both
   checks are required.
5. Update contributor-facing validation instructions so the local and CI gates
   agree.

No `# noqa` for `C901` or `PLR0912`, blanket `# noqa`, global ignores,
per-file ignores, threshold increases, or CLI-only policy overrides may be used
to make the gate pass.

## Refactoring Batches

### Runtime And Policy Core

Refactor the affected functions in:

- `agent_runtime_ref/__main__.py`
- `agent_runtime_ref/continuity.py`
- `agent_runtime_ref/evidence.py`
- `agent_runtime_ref/execution.py`
- `agent_runtime_ref/policy.py`
- `agent_runtime_ref/runtime.py`
- `agent_runtime_ref/session.py`

Preserve public imports, command names, argument parsing, exit behavior, event
ordering, serialized schemas, validation messages, approval semantics, and
policy decisions. CLI command dispatch may move to command-specific helpers,
but the existing `main()` entry point remains.

### Publisher Tools

Refactor the affected functions in:

- `docs/publisher/tools/audit_ru_visuals.py`
- `docs/publisher/tools/build_ru_editorial_docx.py`
- `docs/publisher/tools/build_template2000n_derivative.py`
- `docs/publisher/tools/plan_google_doc_developmental_sync.py`
- `docs/publisher/tools/sync_ru_docx_visuals.py`

Separate input normalization, structural decisions, document mutations, and
result construction where those responsibilities are currently interleaved.
Preserve generated document structure, ordering, style mapping, range
boundaries, and diagnostic output.

### Legacy Manuscript Transformation Pipeline

Refactor the affected functions in
`docs/publisher/tools/revise_ru_manuscript.py` as a separate batch. Extract
named predicates and transformations around each established editorial pass
instead of redesigning the pipeline. Preserve pass order, replacement order,
idempotence expectations, source anchors, fenced block handling, and generated
manuscript bytes wherever tests currently require deterministic output.

## Testing And Regression Control

Before changing a complex function whose branches are not adequately covered,
add focused characterization tests for its observable outcomes. Then perform
the smallest refactoring that makes both protected rules pass. Run focused
tests after each function or cohesive group and the full suite after each
batch.

Tests should assert behavior rather than helper implementation. Existing tests
remain the primary regression contract; new tests should cover branch
boundaries exposed during decomposition, especially error paths, default
values, ordering, and generated artifact structure.

The six existing tracked `E` and `I` diagnostics will be fixed as part of the
same quality pass. Automatic Ruff fixes may be used only where the resulting
diff is reviewed and behavior-neutral.

## Error Handling And Compatibility

Refactoring must not broaden exception handling, replace specific failures with
generic ones, suppress errors, or change which layer owns validation. Helpers
should either return an explicit intermediate result or raise the same
exception type with the same user-facing message as the original path.

The new hook supports Python 3.10 and later and therefore fits the repository's
Python 3.12 requirement. The hook is pinned by tag for reproducibility. Its
known stale `--version` output in tag `v0.4.0` does not affect policy behavior;
the repository records the actual pinned tag in pre-commit configuration.

## Verification And Acceptance Criteria

The work is complete only when all of the following are true:

1. Ruff selects `C901` and `PLR0912` globally with unchanged thresholds.
2. Ruff reports zero `C901`, `PLR0912`, `E`, `F`, and `I` diagnostics for all
   tracked Python code.
3. `pre-commit run check-ruff-suppressions --all-files` and
   `pre-commit run --all-files` both pass.
4. `ty check` passes.
5. The complete pytest suite with coverage passes.
6. `mkdocs build --strict` passes.
7. `git diff --check` passes.
8. No protected suppression or complexity-policy exception is introduced.
9. No pre-existing unrelated working-tree file is changed, staged, or included
   in a commit.
