# Ruff Policy Hooks And Complexity Refactoring Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Enforce `C901` and `PLR0912` with `ruff-policy-hooks` and refactor all 45 existing diagnostics without changing observable runtime or publishing behavior.

**Architecture:** Pin the suppression-policy hook and select the two exact Ruff rules first, then remove violations in isolated behavior-preserving batches. Each complex entry point remains stable while validation, classification, dispatch, and formatting branches move into private helpers; focused tests and a target Ruff command gate every batch.

**Tech Stack:** Python 3.12, uv, Ruff 0.15.x, pre-commit 4.x, ruff-policy-hooks v0.4.0, pytest, ty, MkDocs, GitHub Actions.

---

## File Map

**Create**

- `.pre-commit-config.yaml` — pinned suppression policy.
- `.github/workflows/quality.yml` — pull-request and main-branch quality gate.
- `tests/test_quality_policy.py` — executable assertions for the repository policy.

**Modify: configuration and guidance**

- `pyproject.toml` — development dependency and Ruff selectors.
- `uv.lock` — locked pre-commit dependency graph.
- `README.md`, `CONTRIBUTING.md` — local policy and validation commands.

**Modify: runtime**

- `agent_runtime_ref/__main__.py`
- `agent_runtime_ref/continuity.py`
- `agent_runtime_ref/evidence.py`
- `agent_runtime_ref/execution.py`
- `agent_runtime_ref/policy.py`
- `agent_runtime_ref/runtime.py`
- `agent_runtime_ref/session.py`

**Modify: publisher tools**

- `docs/publisher/tools/audit_ru_visuals.py`
- `docs/publisher/tools/build_ru_editorial_docx.py`
- `docs/publisher/tools/build_template2000n_derivative.py`
- `docs/publisher/tools/plan_google_doc_developmental_sync.py`
- `docs/publisher/tools/revise_ru_manuscript.py`
- `docs/publisher/tools/sync_ru_docx_visuals.py`
- `docs/publisher/tools/apply_ru_terminology_replacements.py`
- `docs/publisher/tools/render_qa_metrics.py`

**Modify: tests only when characterization is missing**

- `tests/test_agent_runtime_evidence.py`
- `tests/test_agent_runtime_ref.py`
- `tests/test_continuity.py`
- `tests/test_plan_google_doc_developmental_sync.py`
- `tests/test_publisher_docx.py`
- `tests/test_ru_manuscript_revision.py`

## Baseline Constraints

- The isolated worktree starts at commit `7f9f25da`.
- `mkdocs build --strict` passes.
- The full suite has one known baseline failure because the original working
  tree contains an uncommitted regenerated
  `docs/publisher/ru-learning-outcome-map-2026-07-27.md`. The user's version
  matches fresh generator output byte-for-byte and must not be copied into a
  feature commit. Run the final full suite after fast-forwarding the feature
  branch into the original working tree.
- `ty check agent_runtime_ref` passes. Keep that supported scope explicit in
  CI and contributor commands instead of narrowing project-wide `ty` discovery
  in `pyproject.toml`; optional publisher scripts have external runtime
  dependencies and are not part of this type gate.

### Task 1: Make The Policy Executable

**Files:**
- Create: `.pre-commit-config.yaml`
- Create: `tests/test_quality_policy.py`
- Modify: `pyproject.toml`
- Modify: `uv.lock`

- [ ] **Step 1: Write the failing policy contract test**

```python
from __future__ import annotations

import tomllib
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_complexity_suppressions_are_protected() -> None:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert {"C901", "PLR0912"} <= set(project["tool"]["ruff"]["lint"]["select"])
    assert "src" not in project["tool"].get("ty", {})

    config = yaml.safe_load((ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8"))
    repository = next(
        item for item in config["repos"]
        if item["repo"] == "https://github.com/ternaus/ruff-policy-hooks"
    )
    assert repository["rev"] == "v0.4.0"
    hook = next(item for item in repository["hooks"] if item["id"] == "check-ruff-suppressions")
    assert hook["args"] == ["--protect=C901,PLR0912"]
```

- [ ] **Step 2: Run the test and verify the missing policy fails**

Run: `uv run pytest tests/test_quality_policy.py -q`

Expected: FAIL because `.pre-commit-config.yaml` and the protected selectors do not exist.

- [ ] **Step 3: Add the exact Ruff policy**

```toml
[dependency-groups]
dev = [
  "pre-commit>=4.3,<5",
  "pytest>=8.4,<9",
  "pytest-cov>=7,<8",
  "ruff>=0.15.8,<0.16",
  "ty>=0.0.26,<0.1",
]

[tool.ruff.lint]
select = ["E", "F", "I", "C901", "PLR0912"]

```

```yaml
repos:
  - repo: https://github.com/ternaus/ruff-policy-hooks
    rev: v0.4.0
    hooks:
      - id: check-ruff-suppressions
        args: ["--protect=C901,PLR0912"]
```

- [ ] **Step 4: Lock dependencies and validate configuration**

Run: `uv lock`

Run: `uv sync --group docs --group dev`

Run: `uv run pre-commit validate-config`

Expected: all commands exit 0.

- [ ] **Step 5: Run the policy test and hook**

Run: `uv run pytest tests/test_quality_policy.py -q`

Run: `uv run pre-commit run check-ruff-suppressions --all-files`

Expected: PASS; the hook finds no protected suppressions even though Ruff still reports the 45 complexity diagnostics.

- [ ] **Step 6: Commit**

```bash
git add .pre-commit-config.yaml pyproject.toml uv.lock tests/test_quality_policy.py
git commit -m "build: enforce Ruff suppression policy"
```

### Task 2: Clear The Existing E And I Baseline

**Files:**
- Modify: `docs/publisher/tools/apply_ru_terminology_replacements.py`
- Modify: `docs/publisher/tools/plan_google_doc_developmental_sync.py`
- Modify: `docs/publisher/tools/render_qa_metrics.py`

- [ ] **Step 1: Record the six existing diagnostics**

Run: `uv run ruff check docs/publisher/tools/apply_ru_terminology_replacements.py docs/publisher/tools/plan_google_doc_developmental_sync.py docs/publisher/tools/render_qa_metrics.py --select E,F,I --no-cache`

Expected: three `I001` diagnostics and three `E501` diagnostics.

- [ ] **Step 2: Apply reviewed import fixes and wrap the three long replacement entries**

Run: `uv run ruff check docs/publisher/tools/apply_ru_terminology_replacements.py docs/publisher/tools/plan_google_doc_developmental_sync.py docs/publisher/tools/render_qa_metrics.py --select I --fix`

Rewrite long tuple entries using adjacent string literals, for example:

```python
(
    "long source phrase",
    "first half of the replacement "
    "and its continuation",
),
```

- [ ] **Step 3: Verify and commit**

Run: `uv run ruff check . --select E,F,I --no-cache`

Expected: PASS.

```bash
git add docs/publisher/tools/apply_ru_terminology_replacements.py docs/publisher/tools/plan_google_doc_developmental_sync.py docs/publisher/tools/render_qa_metrics.py
git commit -m "style: clear existing Ruff baseline"
```

### Task 3: Simplify Continuity Validation

**Files:**
- Modify: `agent_runtime_ref/continuity.py:70-263`
- Test: `tests/test_continuity.py`

- [ ] **Step 1: Add direct delegated-envelope characterization**

Add parameterized cases asserting the existing messages for missing delegated principal, missing delegated scope, unsupported schema, malformed digest prefix, and a false reauthorization flag.

```python
@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("delegated_principal_id", "", "Continuity field is required: delegated_principal_id"),
        ("delegated_scope", "", "Continuity field is required: delegated_scope"),
    ],
)
def test_delegated_envelope_requires_bound_identity(field: str, value: str, message: str) -> None:
    values = valid_envelope_fields(authorization_mode="user_delegated")
    values[field] = value
    with pytest.raises(ValueError, match=message):
        ContinuityEnvelope(**values)
```

- [ ] **Step 2: Run focused tests and the failing Ruff gate**

Run: `uv run pytest tests/test_continuity.py -q`

Run: `uv run ruff check agent_runtime_ref/continuity.py --select C901,PLR0912 --no-cache`

Expected: tests pass; Ruff reports two `C901` diagnostics.

- [ ] **Step 3: Extract delegated and time validation without changing precedence**

```python
def _validate_delegated_fields(mode: str, principal_id: str, scope: str) -> None:
    if mode != "user_delegated":
        return
    if not principal_id:
        raise ValueError("Continuity field is required: delegated_principal_id")
    if not scope:
        raise ValueError("Continuity field is required: delegated_scope")


def _normalize_rehydration_time(now: datetime | None) -> datetime:
    current = datetime.now(UTC) if now is None else now
    if not isinstance(current, datetime):
        raise TypeError("Continuity validation time must be a datetime")
    if current.tzinfo is None:
        raise ValueError("Continuity validation time must include a timezone")
    return current.astimezone(UTC)
```

Keep unresolved side effects ahead of drift comparisons.

- [ ] **Step 4: Verify and commit**

Run: `uv run pytest tests/test_continuity.py -q`

Run: `uv run ruff check agent_runtime_ref/continuity.py --select C901,PLR0912 --no-cache`

Expected: PASS.

```bash
git add agent_runtime_ref/continuity.py tests/test_continuity.py
git commit -m "refactor: simplify continuity validation"
```

### Task 4: Split Tool Execution Outcomes

**Files:**
- Modify: `agent_runtime_ref/execution.py:13-98`

- [ ] **Step 1: Run the behavior tests and failing gate**

Run: `uv run pytest tests/test_agent_runtime_ref.py::TestExecutionAndPolicyBranches tests/test_machine_states.py -q`

Run: `uv run ruff check agent_runtime_ref/execution.py --select C901 --no-cache`

Expected: tests pass; Ruff reports `execute_tool` at complexity 12.

- [ ] **Step 2: Extract ordered outcome classifiers**

```python
def _policy_or_validation_result(
    capability: CapabilitySpec,
    capability_name: str,
    arguments: dict[str, str],
    decision: PolicyDecision,
) -> ToolResult | None:
    if decision.action == "deny":
        return ToolResult(capability_name, "permission_denied", {"reason": decision.reason})
    if decision.action == "approval_required":
        return ToolResult(capability_name, "approval_required", {"reason": decision.reason})
    if capability.idempotency_key_required and "idempotency_key" not in arguments:
        return ToolResult(capability_name, "validation_failure", {"reason": "missing_idempotency_key"})
    return None


def _fault_result(capability_name: str, test_fault: str) -> ToolResult | None:
    if test_fault == "tool_timeout":
        return ToolResult(
            capability_name=capability_name,
            status="retryable_failure",
            payload={"reason": "tool_timeout", "effect_state": "not_executed"},
        )
    if test_fault == "post_dispatch_timeout":
        return ToolResult(
            capability_name=capability_name,
            status="side_effect_unknown",
            payload={
                "reason": "post_dispatch_timeout",
                "effect_state": "side_effect_unknown",
                "reconciliation_required": "true",
            },
            side_effect_status="side_effect_unknown",
        )
    if test_fault == "upstream_unavailable":
        return ToolResult(
            capability_name=capability_name,
            status="retryable_failure",
            payload={"reason": "upstream_unavailable", "effect_state": "not_executed"},
        )
    return None
```

`execute_tool` must call policy/validation before fault injection and then build the unchanged success payload.

- [ ] **Step 3: Verify and commit**

Run the two commands from Step 1; both must pass.

```bash
git add agent_runtime_ref/execution.py
git commit -m "refactor: split tool execution outcomes"
```

### Task 5: Decompose Policy Parsing And Decisions

**Files:**
- Modify: `agent_runtime_ref/policy.py:165-313`
- Test: `tests/test_agent_runtime_ref.py`

- [ ] **Step 1: Run policy branch tests and record four Ruff diagnostics**

Run: `uv run pytest tests/test_agent_runtime_ref.py::TestExecutionAndPolicyBranches -q`

Run: `uv run ruff check agent_runtime_ref/policy.py --select C901,PLR0912 --no-cache`

- [ ] **Step 2: Extract configuration readers**

```python
def _read_capability_policies(raw: object) -> dict[str, CapabilityPolicy]:
    if not isinstance(raw, Mapping):
        raise TypeError("'capabilities' must be a mapping")
    result: dict[str, CapabilityPolicy] = {}
    # Populate result with the existing name, shape, decision, approver, and duplicate checks.
    return result
```

- [ ] **Step 3: Extract decision stages with explicit `None` fallthrough**

Extract `_tool_guard_decision` for tenant → principal → requester → inventory →
network → egress checks, `_configured_capability_decision` for configured
allow/approval/deny with `None` as fallthrough, and
`_default_capability_decision` for unknown → critical → read →
approval-required → write → unsupported classification. Give each helper the
same typed inputs that its moved branch chain currently reads.

Keep the create-ticket validation-drill allowance after guard checks and before configured/default policy.

- [ ] **Step 4: Verify and commit**

Run the commands from Step 1; expect PASS and zero protected diagnostics.

```bash
git add agent_runtime_ref/policy.py tests/test_agent_runtime_ref.py
git commit -m "refactor: stage policy decisions"
```

### Task 6: Decompose Evidence Signal Validation

**Files:**
- Modify: `agent_runtime_ref/evidence.py:442-526`
- Test: `tests/test_agent_runtime_evidence.py`

- [ ] **Step 1: Run evidence tests and record two Ruff diagnostics**

Run: `uv run pytest tests/test_agent_runtime_evidence.py -q`

Run: `uv run ruff check agent_runtime_ref/evidence.py --select C901,PLR0912 --no-cache`

- [ ] **Step 2: Split normalization, entry validation, and reference validation**

Create `_normalize_signal_entries(raw, diagnostics)` returning the existing
`(raw_id, raw_signal, location)` tuples,
`_validate_signal_artifact_refs(raw_signal, location, artifact_ids,
diagnostics)` for the non-empty list and known-artifact checks, and
`_validate_signal_entry(raw_id, raw_signal, location, artifact_ids, seen_ids,
diagnostics)` returning the normalized `(signal_id, value)` pair or `None`.
Preserve diagnostic order: id, duplicate, mapping/value, artifact references.

- [ ] **Step 3: Verify multi-diagnostic order and commit**

Run: `uv run pytest tests/test_agent_runtime_evidence.py -q`

Run: `uv run ruff check agent_runtime_ref/evidence.py --select C901,PLR0912 --no-cache`

Expected: PASS.

```bash
git add agent_runtime_ref/evidence.py tests/test_agent_runtime_evidence.py
git commit -m "refactor: split evidence signal checks"
```

### Task 7: Simplify Runtime Construction And Request Normalization

**Files:**
- Modify: `agent_runtime_ref/runtime.py:87-549`
- Test: `tests/test_agent_runtime_ref.py`

- [ ] **Step 1: Add missing malformed-idempotency characterization**

Extend the existing direct-dependency matrix with:

```python
("idempotency", object(), "Runtime idempotency must be IdempotencyStore"),
```

- [ ] **Step 2: Run runtime tests and record four Ruff diagnostics**

Run: `uv run pytest tests/test_agent_runtime_ref.py::TestRuntimeCore tests/test_agent_runtime_ref.py::TestRuntimeControlPaths tests/test_machine_states.py tests/test_review_remediations.py -q`

Run: `uv run ruff check agent_runtime_ref/runtime.py --select C901,PLR0912 --no-cache`

- [ ] **Step 3: Extract component construction while preserving worker dependency order**

```python
T = TypeVar("T")

def _runtime_component(value: T | None, expected: type[T], factory: Callable[[], T], label: str) -> T:
    component = factory() if value is None else value
    if not isinstance(component, expected):
        raise TypeError(f"Runtime {label} must be {expected.__name__}")
    return component
```

Keep sandbox, default agent, and background worker in dedicated helpers because the worker captures the already-normalized memory, policy, and telemetry instances.

- [ ] **Step 4: Extract `_normalize_run_request`, `_legacy_tool_status`, and `_reconciliation_effect`**

Move normalization in its original field order. Do not consolidate the three terminal session/event branches.

- [ ] **Step 5: Verify and commit**

Run the commands from Step 2; expect PASS.

```bash
git add agent_runtime_ref/runtime.py tests/test_agent_runtime_ref.py
git commit -m "refactor: normalize runtime setup"
```

### Task 8: Simplify Eval Dataset Export

**Files:**
- Modify: `agent_runtime_ref/session.py:544-659`

- [ ] **Step 1: Run session export tests and record `C901`**

Run: `uv run pytest tests/test_agent_runtime_ref.py -q -k 'eval_dataset or eval_export'`

Run: `uv run ruff check agent_runtime_ref/session.py --select C901 --no-cache`

- [ ] **Step 2: Extract validation helpers**

Create `_normalize_eval_session_ids(session_ids)` for sequence, field, and
uniqueness validation; `_normalize_eval_specs(eval_specs)` for mapping, key,
duplicate, and spec validation; and `_latest_failed_run(store, session_ids)`
for reverse session/run traversal. Retain the current concrete return types:
normalized tuples/mappings and `RunRecord | None`.

Create the destination directory at the same point as before so invalid inputs retain existing side effects.

- [ ] **Step 3: Verify and commit**

Run the commands from Step 1; expect PASS.

```bash
git add agent_runtime_ref/session.py
git commit -m "refactor: split eval export helpers"
```

### Task 9: Replace CLI Branch Chains With Dispatch

**Files:**
- Modify: `agent_runtime_ref/__main__.py:1216-1313,2777-2842`

- [ ] **Step 1: Run CLI tests and record four Ruff diagnostics**

Run: `uv run pytest tests/test_agent_runtime_ref.py::TestCli -q`

Run: `uv run ruff check agent_runtime_ref/__main__.py --select C901,PLR0912 --no-cache`

- [ ] **Step 2: Extract rollout evidence and action selection**

```python
def _recommended_rollout_action(*, manifest_present: bool, evidence_verified: bool, has_overrides: bool, ready: bool) -> str:
    if not manifest_present:
        return "attach_verified_evidence"
    if not evidence_verified:
        return "repair_evidence_manifest"
    if has_overrides:
        return "remove_manual_overrides"
    if not ready:
        return "collect_missing_evidence"
    return "attach_trusted_attestation"
```

Move evidence loading to `_collect_rollout_evidence` and preserve diagnostics and evidence-mode ordering.

- [ ] **Step 3: Add typed handler dispatch and command-default normalization**

Build `COMMAND_HANDLERS` as a typed mapping from every parser command name to
its existing handler, with each command included exactly once. Use
`_normalize_cli_argv` and `_apply_command_defaults`; keep `parser.error` for
unsupported commands and preserve `[] -> simulate-run`.

- [ ] **Step 4: Verify and commit**

Run the commands from Step 1; expect PASS.

```bash
git add agent_runtime_ref/__main__.py
git commit -m "refactor: dispatch runtime CLI commands"
```

### Task 10: Refactor Google Docs Range And Style Planning

**Files:**
- Modify: `docs/publisher/tools/plan_google_doc_developmental_sync.py:235-407`
- Test: `tests/test_plan_google_doc_developmental_sync.py`

- [ ] **Step 1: Add range and UTF-16 characterization tests**

Cover adjacent/gapped insertion, unique fuzzy match, ambiguous fallback, mapped/unmapped endpoints, non-monotonic ranges, astral characters, zero-length runs, and list-kind/nesting boundaries.

Name the focused cases
`test_resolve_live_range_accepts_one_unambiguous_fuzzy_paragraph` and
`test_style_requests_uses_utf16_offsets_for_astral_text`. The first must assert
the resolved start/end and a `fuzzy_ratio >= 0.85`; the second must construct a
complete `TargetParagraph` using the existing fixture defaults and assert that
`A😀B` advances a start index of 10 to an end index of 15.

- [ ] **Step 2: Run tests and record three Ruff diagnostics**

Run: `uv run pytest tests/test_plan_google_doc_developmental_sync.py -q`

Run: `uv run ruff check docs/publisher/tools/plan_google_doc_developmental_sync.py --select C901,PLR0912 --no-cache`

- [ ] **Step 3: Extract range and request helpers**

Add `_resolve_insert_range`, `_resolve_fuzzy_single_paragraph`, `_resolve_mapped_span`, `_paragraph_style_request`, `_text_style_requests`, `_iter_list_groups`, and `_bullet_request`. Keep cursor orchestration in `style_requests`.

- [ ] **Step 4: Verify and commit**

Run the commands from Step 2; expect PASS.

```bash
git add docs/publisher/tools/plan_google_doc_developmental_sync.py tests/test_plan_google_doc_developmental_sync.py
git commit -m "refactor: split Google Docs sync planning"
```

### Task 11: Refactor Visual Audit And DOCX Synchronization

**Files:**
- Modify: `docs/publisher/tools/audit_ru_visuals.py:133-183`
- Modify: `docs/publisher/tools/sync_ru_docx_visuals.py:188-303`
- Test: `tests/test_publisher_docx.py`

- [ ] **Step 1: Add helper-level characterization for media and captions**

Use compact XML fixtures to assert media hash/order, blank alt text, aspect/height/alpha rejection, missing captions, and duplicate target rejection.

- [ ] **Step 2: Run publisher tests and record three Ruff diagnostics**

Run: `uv run pytest tests/test_publisher_docx.py -q`

Run: `uv run ruff check docs/publisher/tools/audit_ru_visuals.py docs/publisher/tools/sync_ru_docx_visuals.py --select C901,PLR0912 --no-cache`

- [ ] **Step 3: Extract audit and synchronization stages**

Create `_validate_docx_media`, `_validate_numbered_figure_captions`, `_image_relationship_targets`, `_ordered_drawings`, `_synchronize_drawing`, and `_write_docx_archive`. Preserve temporary-directory ownership and caption relocation order.

- [ ] **Step 4: Verify and commit**

Run the commands from Step 2; expect PASS.

```bash
git add docs/publisher/tools/audit_ru_visuals.py docs/publisher/tools/sync_ru_docx_visuals.py tests/test_publisher_docx.py
git commit -m "refactor: stage DOCX visual processing"
```

### Task 12: Refactor Editorial DOCX Rendering

**Files:**
- Modify: `docs/publisher/tools/build_ru_editorial_docx.py:558-834`
- Test: `tests/test_publisher_docx.py`

- [ ] **Step 1: Add fresh-render branch coverage**

Add cases for image-only and title paragraphs, captions, blockquotes, horizontal rules, recursive containers, empty tables, monospace cells, header repetition, and identifier-biased first-column widths.

- [ ] **Step 2: Run tests and record three Ruff diagnostics**

Run: `uv run pytest tests/test_publisher_docx.py -q`

Run: `uv run ruff check docs/publisher/tools/build_ru_editorial_docx.py --select C901,PLR0912 --no-cache`

- [ ] **Step 3: Extract renderer methods**

Move paragraph, blockquote, and horizontal-rule rendering to `_render_paragraph`, `_render_blockquote`, and `_render_horizontal_rule`. Split table cells, width selection, and width application into `_render_table_cell`, `_table_column_shares`, and `_apply_table_column_widths`.

- [ ] **Step 4: Verify and commit**

Run the commands from Step 2; expect PASS.

```bash
git add docs/publisher/tools/build_ru_editorial_docx.py tests/test_publisher_docx.py
git commit -m "refactor: split editorial DOCX rendering"
```

### Task 13: Refactor Template Semantic Style Mapping

**Files:**
- Modify: `docs/publisher/tools/build_template2000n_derivative.py:204-307`
- Test: `tests/test_publisher_docx.py`

- [ ] **Step 1: Add one behavioral XML fixture covering all categories**

Assert exact `Counter` entries for table header/body, picture/alt text, callout heading/body, captions, list, program, body, preserved heading, and callout reset.

- [ ] **Step 2: Run tests and record two Ruff diagnostics**

Run: `uv run pytest tests/test_publisher_docx.py -q`

Run: `uv run ruff check docs/publisher/tools/build_template2000n_derivative.py --select C901,PLR0912 --no-cache`

- [ ] **Step 3: Extract semantic decisions**

Add `_table_paragraph_styles`, `_next_nonempty_paragraph_text`, `_style_image_paragraph`, and `_semantic_paragraph_style`; move label and preserved-style sets to module constants. Blank paragraphs must not clear a pending callout; headings and images must.

- [ ] **Step 4: Verify and commit**

Run the commands from Step 2; expect PASS.

```bash
git add docs/publisher/tools/build_template2000n_derivative.py tests/test_publisher_docx.py
git commit -m "refactor: classify template paragraph styles"
```

### Task 14: Split Early Manuscript Structure Restorers

**Files:**
- Modify: `docs/publisher/tools/revise_ru_manuscript.py:2990-3292`
- Test: `tests/test_ru_manuscript_revision.py`

- [ ] **Step 1: Add synthetic structural characterization**

Cover blank-separated pseudo-tables, malformed rows, degraded Python fragment bounds, duplicate structured anchors, first-seen source deduplication, and the minimum restoration count.

- [ ] **Step 2: Run reproducibility and record four Ruff diagnostics**

Run: `uv run pytest tests/test_ru_manuscript_revision.py::test_revision_is_reproducible tests/test_ru_manuscript_revision.py -q -k 'pseudo_table or listing or structured'`

Run: `uv run ruff check docs/publisher/tools/revise_ru_manuscript.py --select C901,PLR0912 --no-cache`

- [ ] **Step 3: Extract stable scanning helpers**

Add `_pseudo_table_cells`, `_consume_pseudo_table`, `_degraded_fragment_bounds`, `_fragment_key_coverage`, `_collect_structured_source_blocks`, `_index_unfenced_lines_by_key`, `_select_unique_structured_anchor`, and `_restore_structured_block`. Preserve listing-spec iteration and longest-first block ordering.

- [ ] **Step 4: Verify the three target symbols and commit**

Run focused tests plus:

`uv run ruff check docs/publisher/tools/revise_ru_manuscript.py --select C901,PLR0912 --no-cache`

Expected: only the eight later violating symbols remain.

```bash
git add docs/publisher/tools/revise_ru_manuscript.py tests/test_ru_manuscript_revision.py
git commit -m "refactor: split manuscript structure recovery"
```

### Task 15: Split Manuscript Fence And Heading Classification

**Files:**
- Modify: `docs/publisher/tools/revise_ru_manuscript.py:4380-4509,5320-5371`
- Test: `tests/test_ru_manuscript_revision.py`

- [ ] **Step 1: Add boundary tests**

Cover blank-separated command groups, unclosed fences, single-line JSON, label windows, protected H3 titles, and 69-vs-70-word sections.

- [ ] **Step 2: Extract helpers in pipeline-neutral order**

Add `_unescape_technical_line`, `_is_command_line`, `_consume_command_group`, `_is_single_line_json`, `_iter_fenced_blocks`, `_has_nearby_listing_intro`, `_nearest_h3_title`, `_technical_block_label`, `_demote_h4_lines`, `_short_h3_section_bounds`, and `_is_demotable_short_h3`.

- [ ] **Step 3: Verify reproducibility, structural tests, and Ruff**

Run: `uv run pytest tests/test_ru_manuscript_revision.py::test_revision_is_reproducible tests/test_ru_manuscript_revision.py -q -k 'technical_block or heading or command or json'`

Run the target Ruff command; expect five later symbols to remain.

- [ ] **Step 4: Commit**

```bash
git add docs/publisher/tools/revise_ru_manuscript.py tests/test_ru_manuscript_revision.py
git commit -m "refactor: classify manuscript blocks"
```

### Task 16: Split Source Apparatus Reconstruction

**Files:**
- Modify: `docs/publisher/tools/revise_ru_manuscript.py:8638-8751`
- Test: `tests/test_ru_manuscript_revision.py`

- [ ] **Step 1: Add source-order characterization**

Assert appendix-order IDs, reverse chapter processing, first-two citation IDs, MCP security source insertion, and unchanged exception text for missing apparatus.

- [ ] **Step 2: Extract source helpers**

Add `_ensure_mcp_security_source`, `_number_source_appendix`, `_chapter_source_ids`, `_claim_citation_span`, and `_rewrite_chapter_source_apparatus`. Keep `range(28, 0, -1)` in the driver.

- [ ] **Step 3: Verify and commit**

Run: `uv run pytest tests/test_ru_manuscript_revision.py::test_revision_is_reproducible tests/test_ru_manuscript_revision.py -q -k 'source or citation'`

Run target Ruff; expect four later symbols to remain.

```bash
git add docs/publisher/tools/revise_ru_manuscript.py tests/test_ru_manuscript_revision.py
git commit -m "refactor: split source apparatus rebuild"
```

### Task 17: Split Post-Audit And World-Class Editorial Passes

**Files:**
- Modify: `docs/publisher/tools/revise_ru_manuscript.py:10447-11566`
- Test: `tests/test_ru_manuscript_revision.py`

- [ ] **Step 1: Add legacy/current/duplicate-anchor characterization**

Test the existing three-state behavior for a legacy anchor, already-current text, and duplicate current text. Test stacked-heading bridges and quoted shell lines.

- [ ] **Step 2: Split the post-audit pass by contract domain**

Create `_apply_post_audit_memory_contracts`, `_apply_post_audit_trace_contracts`, `_apply_post_audit_evidence_contracts`, and `_apply_post_audit_release_contracts`. The driver order is memory → trace/privacy → evidence → release.

- [ ] **Step 3: Split the world-class pass by transformation stage**

Create `_apply_required_world_class_replacements`, `_normalize_create_ticket_risk`, `_strengthen_approval_chain`, `_extend_case_and_chapter_sources`, `_insert_stacked_heading_bridges`, `_label_heading_adjacent_fences`, `_repair_world_class_listing_layout`, and `_wrap_world_class_shell_lines` in that order.

- [ ] **Step 4: Verify and commit**

Run: `uv run pytest tests/test_ru_manuscript_revision.py::test_revision_is_reproducible tests/test_ru_manuscript_revision.py -q -k 'memory_examples or trace_examples or evidence_lifecycle or world_class'`

Run target Ruff; expect two later symbols to remain.

```bash
git add docs/publisher/tools/revise_ru_manuscript.py tests/test_ru_manuscript_revision.py
git commit -m "refactor: stage manuscript editorial passes"
```

### Task 18: Split August Editorial Helpers And Print Reflow

**Files:**
- Modify: `docs/publisher/tools/revise_ru_manuscript.py:13541-14620`
- Test: `tests/test_ru_manuscript_revision.py`

- [ ] **Step 1: Add print boundary characterization**

Cover quoted, splittable, and unsplittable shell lines; exact 81-column acceptance; required replacement order; and duplicate chapter-source insertion.

- [ ] **Step 2: Hoist the four nested August helpers**

Create `_replace_once_in_chapter`, `_replace_pattern_once_in_chapter`, `_insert_before_chapter_heading`, `_append_unique_chapter_sources`, and `_replace_required_occurrences`. Leave the straight-line editorial order unchanged.

- [ ] **Step 3: Split print reflow**

Create `_apply_required_print_width_replacements`, `_split_temp_directory_guard_patterns`, `_reflow_shell_fences`, and `_oversized_fenced_lines`; reuse `_split_shell_line_for_print`.

- [ ] **Step 4: Verify zero manuscript diagnostics and commit**

Run: `uv run pytest tests/test_ru_manuscript_revision.py::test_revision_is_reproducible tests/test_ru_manuscript_revision.py -q -k 'august_editorial or technical_book_polish or print_width'`

Run: `uv run ruff check docs/publisher/tools/revise_ru_manuscript.py --select C901,PLR0912 --no-cache`

Expected: PASS.

```bash
git add docs/publisher/tools/revise_ru_manuscript.py tests/test_ru_manuscript_revision.py
git commit -m "refactor: split final manuscript polish"
```

### Task 19: Prove The Entire Protected Baseline Is Clean

**Files:**
- Modify only files exposed by the checks.

- [ ] **Step 1: Run protected Ruff rules repository-wide**

Run: `uv run ruff check . --select C901,PLR0912 --no-cache`

Expected: PASS with zero diagnostics.

- [ ] **Step 2: Run the full configured Ruff and policy gates**

Run: `uv run ruff check . --no-cache`

Run: `uv run pre-commit run check-ruff-suppressions --all-files`

Expected: PASS.

- [ ] **Step 3: Run the supported type target**

Run: `uv run ty check agent_runtime_ref`

Expected: `All checks passed!` for the explicit `agent_runtime_ref` target.

- [ ] **Step 4: Commit any strictly mechanical cleanup**

Inspect `git status --short`, add only the explicitly reviewed cleanup paths,
and commit them with `git commit -m "style: close Ruff policy baseline"`.

Skip the commit if no cleanup was needed.

### Task 20: Add CI Enforcement And Contributor Guidance

**Files:**
- Create: `.github/workflows/quality.yml`
- Modify: `README.md`
- Modify: `CONTRIBUTING.md`
- Test: `tests/test_quality_policy.py`

- [ ] **Step 1: Extend the policy test with workflow assertions**

```python
def test_quality_workflow_runs_ruff_ty_and_policy() -> None:
    workflow = (ROOT / ".github/workflows/quality.yml").read_text(encoding="utf-8")
    for command in (
        "uv run ruff check .",
        "uv run ty check agent_runtime_ref",
        "uv run pre-commit run --all-files",
    ):
        assert command in workflow
```

- [ ] **Step 2: Run and confirm the missing workflow fails**

Run: `uv run pytest tests/test_quality_policy.py -q`

Expected: FAIL because `quality.yml` does not exist.

- [ ] **Step 3: Add the quality workflow**

```yaml
name: quality

on:
  pull_request:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  quality:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v6.0.2
      - uses: astral-sh/setup-uv@v8.1.0
      - run: uv python install 3.12
      - run: uv sync --group dev
      - run: uv run ruff check .
      - run: uv run ty check agent_runtime_ref
      - run: uv run pre-commit run --all-files
```

- [ ] **Step 4: Document local installation and full checks**

Add `uv run pre-commit install`, `uv run pre-commit run --all-files`, and the protected-rule rationale to `CONTRIBUTING.md`; keep the README check block consistent.

- [ ] **Step 5: Verify and commit**

Run: `uv run pytest tests/test_quality_policy.py -q`

Run: `uv run pre-commit run --all-files`

Expected: PASS.

```bash
git add .github/workflows/quality.yml README.md CONTRIBUTING.md tests/test_quality_policy.py
git commit -m "ci: enforce Ruff policy checks"
```

### Task 21: Final Verification And Integration

**Files:**
- No planned code changes.

- [ ] **Step 1: Verify the isolated branch**

Run:

```bash
uv sync --locked --group docs --group dev
uv run ruff check . --no-cache
uv run ty check agent_runtime_ref
uv run pre-commit run --all-files
uv run pytest --cov=agent_runtime_ref --cov-report=term-missing \
  --ignore=tests/test_ru_manuscript_revision.py
uv run pytest tests/test_ru_manuscript_revision.py -q \
  -k 'not test_editorial_packet_builder_is_reproducible'
uv run mkdocs build --strict
git diff --check
git status --short --branch
```

Expected: all commands pass; the isolated branch is clean.

- [ ] **Step 2: Review the branch diff**

Run: `git diff 7f9f25da..HEAD --check`

Run: `git diff 7f9f25da..HEAD --stat`

Confirm that no threshold, protected ignore, protected `noqa`, unrelated publisher artifact, or generated user file was added.

- [ ] **Step 3: Fast-forward the original working branch**

From `/Users/if/PycharmProjects/agent-axiom/agent-arch`, run:

```bash
git merge --ff-only codex/ruff-policy-hooks
```

The two pre-existing modified publisher files and untracked artifacts must remain present and unstaged.

- [ ] **Step 4: Run the true full suite in the original working tree**

Run:

```bash
uv sync --locked --group docs --group dev
uv run ruff check . --no-cache
uv run ty check agent_runtime_ref
uv run pre-commit run --all-files
uv run pytest --cov=agent_runtime_ref --cov-report=term-missing
uv run mkdocs build --strict
git diff --check
```

Expected: all checks pass, including the editorial packet reproducibility test against the user's regenerated learning-outcome map.
