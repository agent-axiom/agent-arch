from __future__ import annotations

import ast
import json
import shutil
from pathlib import Path
from typing import Any, cast

import pytest

from agent_runtime_ref.config import (
    load_agent_profile,
    load_capability_catalog,
    load_controls_policy,
    load_memory_store,
    load_policy_engine,
    load_rollout_policy,
    load_yaml_file,
)
from agent_runtime_ref.controls import assess_controls, assess_inventory_drift
from agent_runtime_ref.execution import execute_tool
from agent_runtime_ref.lifecycle import assess_change_gate, assess_retirement
from agent_runtime_ref.memory import MemoryStore
from agent_runtime_ref.models import ModelOutput, RunContext, RunRequest, ToolRequest
from agent_runtime_ref.policy import CapabilityPolicy, PolicyDecision, PolicyEngine
from agent_runtime_ref.rollout import RolloutReadiness, assess_rollout, ready_for_rollout
from agent_runtime_ref.runtime import AgentRuntime


def _runtime_public_doc_paths() -> list[Path]:
    return [
        Path("agent_runtime_ref/README.md"),
        *sorted(Path("docs/appendix").glob("*.md")),
    ]


def _runtime_public_docs_text() -> str:
    return "\n".join(
        path.read_text(encoding="utf-8") for path in _runtime_public_doc_paths()
    )


def _runtime_source_paths() -> list[Path]:
    return sorted(Path("agent_runtime_ref").glob("*.py"))


def _parse_python_source(source_path: Path) -> ast.Module:
    return ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))


def _runtime_source_trees() -> list[ast.Module]:
    return [_parse_python_source(source_path) for source_path in _runtime_source_paths()]


def _runtime_cli_tree() -> ast.Module:
    return _parse_python_source(Path("agent_runtime_ref/__main__.py"))


def _runtime_config_paths() -> list[Path]:
    return sorted(Path("agent_runtime_ref/configs").glob("*.yaml"))


def _assert_all_documented(items: list[str], docs_text: str) -> None:
    missing = [item for item in items if item not in docs_text]
    assert missing == []


def _module_dict_string_keys(tree: ast.Module) -> dict[str, set[str]]:
    module_dict_keys: dict[str, set[str]] = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            targets = node.targets
            value = node.value
        elif isinstance(node, ast.AnnAssign):
            targets = [node.target]
            value = node.value
        else:
            continue
        if not isinstance(value, ast.Dict):
            continue
        for target in targets:
            if isinstance(target, ast.Name):
                module_dict_keys[target.id] = {
                    key.value
                    for key in value.keys
                    if isinstance(key, ast.Constant) and isinstance(key.value, str)
                }
    return module_dict_keys


def _render_raise_message(message: ast.expr) -> str | None:
    if isinstance(message, ast.Constant) and isinstance(message.value, str):
        return message.value
    if not isinstance(message, ast.JoinedStr):
        return None

    parts: list[str] = []
    for value in message.values:
        if isinstance(value, ast.Constant) and isinstance(value.value, str):
            parts.append(value.value)
        elif isinstance(value, ast.FormattedValue):
            expression = ast.unparse(value.value)
            conversion = {-1: "", 97: "!a", 114: "!r", 115: "!s"}[
                value.conversion
            ]
            parts.append("{" + expression + conversion + "}")
    return "".join(parts)


def _runtime_error_messages(trees: list[ast.Module]) -> list[str]:
    runtime_errors: set[str] = set()
    for tree in trees:
        for node in ast.walk(tree):
            if not isinstance(node, ast.Raise) or not isinstance(node.exc, ast.Call):
                continue
            error_name = getattr(node.exc.func, "id", "")
            if error_name not in {"TypeError", "ValueError", "RuntimeError"}:
                continue
            if not node.exc.args:
                continue
            message = _render_raise_message(node.exc.args[0])
            if message is not None:
                runtime_errors.add(message)
    return sorted(runtime_errors)


def _dataclass_field_names(tree: ast.Module) -> set[str]:
    field_names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        is_dataclass = any(
            (isinstance(decorator, ast.Name) and decorator.id == "dataclass")
            or (
                isinstance(decorator, ast.Call)
                and getattr(decorator.func, "id", "") == "dataclass"
            )
            for decorator in node.decorator_list
        )
        if not is_dataclass:
            continue
        for statement in node.body:
            if isinstance(statement, ast.AnnAssign) and isinstance(
                statement.target, ast.Name
            ):
                field_names.add(statement.target.id)
    return field_names


def _runtime_dataclass_fields(trees: list[ast.Module]) -> set[str]:
    runtime_fields: set[str] = set()
    for tree in trees:
        runtime_fields.update(_dataclass_field_names(tree))
    return runtime_fields


def _runtime_public_dataclass_fields(trees: list[ast.Module]) -> list[str]:
    return sorted(field for field in _runtime_dataclass_fields(trees) if "_" in field)


def _runtime_json_keys(tree: ast.Module, documented_key_names: set[str]) -> set[str]:
    runtime_keys: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        for key in node.keys:
            if isinstance(key, ast.Constant) and isinstance(key.value, str):
                if "_" in key.value or key.value in documented_key_names:
                    runtime_keys.add(key.value)
    return runtime_keys


def _runtime_documented_json_keys(
    trees: list[ast.Module], documented_key_names: set[str]
) -> set[str]:
    runtime_keys: set[str] = set()
    for tree in trees:
        runtime_keys.update(_runtime_json_keys(tree, documented_key_names))
    return runtime_keys


def _runtime_public_json_keys(trees: list[ast.Module]) -> list[str]:
    documented_key_names = {
        "approvals",
        "events",
        "labels",
        "result",
        "runs",
        "sessions",
        "status",
    }
    return sorted(_runtime_documented_json_keys(trees, documented_key_names))


def _runtime_config_root_keys(configs: list[dict[str, object]]) -> list[str]:
    root_keys: set[str] = set()
    for config in configs:
        root_keys.update(str(key) for key in config)
    return sorted(root_keys)


def _runtime_config_file_names(config_paths: list[Path]) -> list[str]:
    return sorted(path.name for path in config_paths)


def _nested_config_keys(value: object) -> set[str]:
    config_keys: set[str] = set()
    if isinstance(value, dict):
        for key, nested_value in value.items():
            if isinstance(key, str) and "_" in key:
                config_keys.add(key)
            config_keys.update(_nested_config_keys(nested_value))
    elif isinstance(value, list):
        for nested_value in value:
            config_keys.update(_nested_config_keys(nested_value))
    return config_keys


def _runtime_config_nested_keys(configs: list[dict[str, object]]) -> list[str]:
    config_keys: set[str] = set()
    for config in configs:
        config_keys.update(_nested_config_keys(config))
    return sorted(config_keys)


def _cli_method_calls(tree: ast.Module, method_name: str) -> list[ast.Call]:
    return [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == method_name
    ]


def _cli_subcommand_names(tree: ast.Module) -> list[str]:
    return sorted(
        node.args[0].value
        for node in _cli_method_calls(tree, "add_parser")
        if node.args
        and isinstance(node.args[0], ast.Constant)
        and isinstance(node.args[0].value, str)
    )


def _cli_option_flags(tree: ast.Module) -> list[str]:
    return sorted(
        arg.value
        for node in _cli_method_calls(tree, "add_argument")
        for arg in node.args
        if isinstance(arg, ast.Constant)
        and isinstance(arg.value, str)
        and arg.value.startswith("--")
    )


def _documented_literal_markers(tree: ast.Module) -> list[str]:
    literal_markers = {
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant)
        and isinstance(node.value, str)
        and node.value[:1].islower()
        and all(char.islower() or char.isdigit() or char in "_:" for char in node.value)
    }
    return sorted(
        marker
        for marker in literal_markers
        if "_" in marker or marker.startswith("trace:")
    )


def _cli_choice_values(tree: ast.Module) -> list[str]:
    module_dict_keys = _module_dict_string_keys(tree)
    runtime_choices: set[str] = set()
    for node in _cli_method_calls(tree, "add_argument"):
        for keyword in node.keywords:
            if keyword.arg != "choices":
                continue
            if isinstance(keyword.value, (ast.List, ast.Tuple, ast.Set)):
                runtime_choices.update(
                    item.value
                    for item in keyword.value.elts
                    if isinstance(item, ast.Constant) and isinstance(item.value, str)
                )
            elif (
                isinstance(keyword.value, ast.Call)
                and isinstance(keyword.value.func, ast.Name)
                and keyword.value.func.id == "tuple"
                and len(keyword.value.args) == 1
                and isinstance(keyword.value.args[0], ast.Name)
            ):
                runtime_choices.update(module_dict_keys[keyword.value.args[0].id])
    return sorted(runtime_choices)


@pytest.fixture(scope="class")
def runtime_public_docs_text() -> str:
    return _runtime_public_docs_text()


@pytest.fixture(scope="class")
def runtime_source_trees() -> list[ast.Module]:
    return _runtime_source_trees()


@pytest.fixture(scope="class")
def runtime_cli_tree() -> ast.Module:
    return _runtime_cli_tree()


@pytest.fixture(scope="class")
def runtime_config_paths() -> list[Path]:
    return _runtime_config_paths()


@pytest.fixture(scope="class")
def runtime_config_documents(
    runtime_config_paths: list[Path],
) -> list[dict[str, object]]:
    return [load_yaml_file(config_path) for config_path in runtime_config_paths]


class TestRuntimeDocsParity:
    def test_runtime_error_messages_remain_documented(
        self, runtime_public_docs_text: str, runtime_source_trees: list[ast.Module]
    ) -> None:
        """Keep operator-facing runtime failures aligned with public docs."""
        runtime_errors = _runtime_error_messages(runtime_source_trees)

        _assert_all_documented(runtime_errors, runtime_public_docs_text)

    def test_runtime_literal_markers_remain_documented(
        self, runtime_public_docs_text: str, runtime_cli_tree: ast.Module
    ) -> None:
        """Keep public docs aligned with scenario labels and runtime markers."""
        documented_markers = _documented_literal_markers(runtime_cli_tree)

        _assert_all_documented(documented_markers, runtime_public_docs_text)

    def test_runtime_config_files_remain_documented(
        self, runtime_public_docs_text: str, runtime_config_paths: list[Path]
    ) -> None:
        """Keep bundled runtime config filenames aligned with public docs."""
        config_files = _runtime_config_file_names(runtime_config_paths)

        _assert_all_documented(config_files, runtime_public_docs_text)

    def test_runtime_config_root_keys_remain_documented(
        self, runtime_public_docs_text: str, runtime_config_documents: list[dict[str, object]]
    ) -> None:
        """Keep bundled runtime config root keys aligned with public docs."""
        root_keys = _runtime_config_root_keys(runtime_config_documents)

        _assert_all_documented(root_keys, runtime_public_docs_text)

    def test_runtime_config_nested_keys_remain_documented(
        self, runtime_public_docs_text: str, runtime_config_documents: list[dict[str, object]]
    ) -> None:
        """Keep bundled runtime config nested keys aligned with public docs."""
        config_keys = _runtime_config_nested_keys(runtime_config_documents)

        _assert_all_documented(config_keys, runtime_public_docs_text)

    def test_runtime_cli_subcommands_remain_documented(
        self, runtime_public_docs_text: str, runtime_cli_tree: ast.Module
    ) -> None:
        """Keep argparse subcommands aligned with public docs."""
        runtime_subcommands = _cli_subcommand_names(runtime_cli_tree)

        _assert_all_documented(runtime_subcommands, runtime_public_docs_text)

    def test_runtime_cli_flags_remain_documented(
        self, runtime_public_docs_text: str, runtime_cli_tree: ast.Module
    ) -> None:
        """Keep argparse option flags aligned with public docs."""
        runtime_flags = _cli_option_flags(runtime_cli_tree)

        _assert_all_documented(runtime_flags, runtime_public_docs_text)

    def test_runtime_cli_choices_remain_documented(
        self, runtime_public_docs_text: str, runtime_cli_tree: ast.Module
    ) -> None:
        """Keep argparse choice values aligned with public docs."""
        runtime_choices = _cli_choice_values(runtime_cli_tree)

        _assert_all_documented(runtime_choices, runtime_public_docs_text)

    def test_runtime_dataclass_fields_remain_documented(
        self, runtime_public_docs_text: str, runtime_source_trees: list[ast.Module]
    ) -> None:
        """Keep public dataclass field names aligned with docs."""
        runtime_fields = _runtime_public_dataclass_fields(runtime_source_trees)

        _assert_all_documented(runtime_fields, runtime_public_docs_text)

    def test_runtime_json_keys_remain_documented(
        self, runtime_public_docs_text: str, runtime_source_trees: list[ast.Module]
    ) -> None:
        """Keep public JSON output/config keys aligned with docs."""
        runtime_keys = _runtime_public_json_keys(runtime_source_trees)

        _assert_all_documented(runtime_keys, runtime_public_docs_text)

    def test_reference_package_documents_approval_session_lineage(self) -> None:
        """Keep multilingual approval docs aligned with closure/session lineage."""
        for path in (
            Path("docs/appendix/reference-package.en.md"),
            Path("docs/appendix/reference-package.md"),
            Path("docs/appendix/reference-package.zh.md"),
        ):
            text = path.read_text(encoding="utf-8")
            assert "inspect-approvals" in text
            assert "resolve-approval" in text
            assert "capability_session_id" in text
            assert "capability_session_status" in text

    def test_reference_package_documents_session_capability_lineage(self) -> None:
        """Keep session docs aligned with per-run capability-session fields."""
        for path in (
            Path("docs/appendix/reference-package.en.md"),
            Path("docs/appendix/reference-package.md"),
            Path("docs/appendix/reference-package.zh.md"),
        ):
            text = path.read_text(encoding="utf-8")
            assert "inspect-session" in text
            assert "export-session" in text
            assert "capability_session_id" in text
            assert "capability_session_status" in text

    def test_approval_schema_documents_policy_loader_errors(self) -> None:
        """Keep approval schema docs aligned with policy validation errors."""
        required_errors = (
            "approvals.default_reviewer must be a string",
            "approvals.default_reviewer is required",
            "approvals.escalation_sla_minutes must be an integer",
            "approvals.escalation_sla_minutes must be positive",
        )
        for path in (
            Path("docs/appendix/approval-schema.en.md"),
            Path("docs/appendix/approval-schema.md"),
            Path("docs/appendix/approval-schema.zh.md"),
        ):
            text = path.read_text(encoding="utf-8")
            for error in required_errors:
                assert error in text

    def test_approval_schema_documents_capability_session_lineage(self) -> None:
        """Keep approval schema docs aligned with approval CLI lineage fields."""
        for path in (
            Path("docs/appendix/approval-schema.en.md"),
            Path("docs/appendix/approval-schema.md"),
            Path("docs/appendix/approval-schema.zh.md"),
        ):
            text = path.read_text(encoding="utf-8")
            assert "inspect-approvals" in text
            assert "resolve-approval" in text
            assert "capability_session_id" in text
            assert "capability_session_status" in text

    def test_approval_schema_documents_authorization_mode_validation(self) -> None:
        """Keep approval docs aligned with delegated-authorization validation."""
        for path in (
            Path("docs/appendix/approval-schema.en.md"),
            Path("docs/appendix/approval-schema.md"),
            Path("docs/appendix/approval-schema.zh.md"),
        ):
            text = path.read_text(encoding="utf-8")
            assert "authorization_mode" in text
            assert "delegated_authorization" in text
            assert "Authorization mode is not supported: {authorization_mode}" in text

    def test_trace_schema_documents_loader_validation_errors(self) -> None:
        """Keep trace schema docs aligned with telemetry loader validation."""
        required_errors = (
            "Telemetry event line is not valid JSON: {line_number}",
            "Telemetry event must be a mapping",
            "Telemetry event is missing required field: {required_field}",
            "Telemetry event field must be a string: {field}",
            "Telemetry event field must not be empty: {field}",
            "Telemetry schema version is not supported: {schema_version}",
            "Telemetry event payload must be a mapping",
            "payload must be a mapping",
            "Telemetry event payload value must be a string: {payload_key}",
            "Telemetry event redacted_fields must be a tuple",
            "redacted_fields must be a list",
            "redacted_fields entries must be strings",
            "Telemetry redact field must not be empty",
            "Telemetry redact field is not present in events: {missing}",
        )
        for path in (
            Path("docs/appendix/trace-schema.en.md"),
            Path("docs/appendix/trace-schema.md"),
            Path("docs/appendix/trace-schema.zh.md"),
        ):
            text = path.read_text(encoding="utf-8")
            for error in required_errors:
                assert error in text

    def test_trace_schema_documents_replay_validation_errors(self) -> None:
        """Keep trace schema docs aligned with replay evidence validation."""
        required_errors = (
            "Trace ID not found in event file: {requested_trace_id}",
            "Trace file does not contain any trace IDs",
            "Trace file contains multiple trace IDs; pass --trace-id explicitly",
            "Trace file does not contain a run_start event",
            "Trace file contains multiple run_start events",
            "Trace run_start event is missing replay fields: {missing_keys}",
            "Trace run_start event has redacted replay fields: {redacted_keys}",
            "Trace run_start replay field must be a string: {field}",
            "Trace run_start replay field must not be empty: {field}",
        )
        for path in (
            Path("docs/appendix/trace-schema.en.md"),
            Path("docs/appendix/trace-schema.md"),
            Path("docs/appendix/trace-schema.zh.md"),
        ):
            text = path.read_text(encoding="utf-8")
            for error in required_errors:
                assert error in text

    def test_eval_schema_documents_runtime_export_contract(self) -> None:
        """Keep eval schema docs aligned with bundled dataset export shape."""
        required_terms = (
            "agent-runtime-ref-eval-seed",
            "session_count",
            "run_count",
            "failed_runs",
            "traceable_failed_runs",
            "latest_failure_reason",
            "failed_run_timeout",
            "profile_memory",
            "memory_read",
            "profile_lookup",
            "grounded_answer",
            "mixed_session",
            "multi_run",
            "approval_then_memory",
            "session_evals",
            "required_run_count",
            "support_ticket",
            "sandbox_profile_review",
            "sandbox_profile_reviewed",
        )
        for path in (
            Path("docs/appendix/eval-schema.en.md"),
            Path("docs/appendix/eval-schema.md"),
            Path("docs/appendix/eval-schema.zh.md"),
        ):
            text = path.read_text(encoding="utf-8")
            for term in required_terms:
                assert term in text

    def test_reference_package_documents_eval_artifact_contract(self) -> None:
        """Keep reference package docs aligned with nested eval artifact fields."""
        required_terms = (
            "support_ticket",
            "sandbox_profile_review",
            "sandbox_profile_reviewed",
            "required_run_count",
            "expected outcome",
        )
        for path in (
            Path("docs/appendix/reference-package.en.md"),
            Path("docs/appendix/reference-package.md"),
            Path("docs/appendix/reference-package.zh.md"),
        ):
            text = path.read_text(encoding="utf-8")
            assert "export-eval-dataset" in text
            for term in required_terms:
                assert term in text

    def test_reference_package_documents_sandbox_profile_loader_errors(self) -> None:
        """Keep lifecycle docs aligned with sandbox-profile config validation."""
        required_errors = (
            "runtime_controls config must be a mapping",
            "runtime_controls.sandbox_profile config must be a mapping",
            "runtime_controls.sandbox_profile.{key} config must be a mapping",
            "runtime_controls.sandbox_profile.workspace.entries must be a list",
            "Sandbox profile workspace entries must be a list",
        )
        for path in (
            Path("docs/appendix/reference-package.en.md"),
            Path("docs/appendix/reference-package.md"),
            Path("docs/appendix/reference-package.zh.md"),
        ):
            text = path.read_text(encoding="utf-8")
            assert "inspect-lifecycle" in text
            assert "sandbox_profile" in text
            for error in required_errors:
                assert error in text

    def test_reference_package_documents_inventory_validation_errors(self) -> None:
        """Keep inspect-agent docs aligned with inventory/catalog validation."""
        required_errors = (
            "approved_capabilities entries must be strings",
            "approved_capabilities entries must not be empty",
            "approved_capabilities entries must be unique",
            "'allowed_egress' must be a list",
            "allowed_egress entries must be strings",
            "allowed_egress entries must not be empty",
            "allowed_egress entries must be unique",
        )
        for path in (
            Path("docs/appendix/reference-package.en.md"),
            Path("docs/appendix/reference-package.md"),
            Path("docs/appendix/reference-package.zh.md"),
        ):
            text = path.read_text(encoding="utf-8")
            assert "inspect-agent" in text
            assert "approved_capabilities" in text
            assert "allowed_egress" in text
            for error in required_errors:
                assert error in text

    def test_reference_package_documents_tool_request_validation_errors(self) -> None:
        """Keep runtime docs aligned with tool request boundary validation."""
        required_errors = (
            "Tool request capability name must be a string",
            "Tool request capability name must not be empty",
            "Tool request arguments must be a mapping",
            "Tool request argument key must be a string",
            "Tool request argument key must not be empty",
            "Tool request argument value must be a string: {argument_key}",
            "Tool request capability does not match catalog entry: "
            "{capability_name} != {capability.name}",
        )
        for path in (
            Path("docs/appendix/reference-package.en.md"),
            Path("docs/appendix/reference-package.md"),
            Path("docs/appendix/reference-package.zh.md"),
        ):
            text = path.read_text(encoding="utf-8")
            assert "Runtime CLI failure paths" in text
            for error in required_errors:
                assert error in text

    def test_reference_package_documents_session_state_conflict_errors(self) -> None:
        """Keep runtime docs aligned with session and approval state conflicts."""
        required_errors = (
            "Approval request is not pending: {approval_id}",
            "Session tenant_id does not match existing session: {session_id}",
            "Session principal_id does not match existing session: {session_id}",
            "Session trace_id already exists: {trace_id}",
            "Session field entries must be unique: {field}",
            "Session field entries must be unique: session_id",
        )
        for path in (
            Path("docs/appendix/reference-package.en.md"),
            Path("docs/appendix/reference-package.md"),
            Path("docs/appendix/reference-package.zh.md"),
        ):
            text = path.read_text(encoding="utf-8")
            assert "Runtime CLI failure paths" in text
            for error in required_errors:
                assert error in text

    def test_change_rollout_schema_documents_signal_validation_errors(self) -> None:
        """Keep rollout docs aligned with signal override validation."""
        required_errors = (
            "Signal key must not be empty: {raw_signal!r}",
            "Unsupported boolean value in signal: {raw_signal!r}",
            "Assessment signal key must be a string",
            "Assessment signal key must not be empty",
            "Assessment signal keys must be unique",
            "Assessment signal value must be a boolean: {field}",
            "Rollout readiness flag must be a boolean: {field}",
        )
        for path in (
            Path("docs/appendix/change-rollout-schema.en.md"),
            Path("docs/appendix/change-rollout-schema.md"),
            Path("docs/appendix/change-rollout-schema.zh.md"),
        ):
            text = path.read_text(encoding="utf-8")
            assert "check-rollout" in text
            assert "check-change" in text
            for error in required_errors:
                assert error in text


class TestFailurePaths:
    def test_config_loader_rejects_non_mapping_yaml(self, tmp_path: Path) -> None:
        from agent_runtime_ref.config import load_yaml_file

        bad_config = tmp_path / "bad.yaml"
        bad_config.write_text("- not\n- a\n- mapping\n", encoding="utf-8")

        with pytest.raises(TypeError, match="must be a mapping"):
            load_yaml_file(bad_config)

    def test_runtime_denied_precheck_records_session_evidence(self) -> None:
        runtime = AgentRuntime()
        result = runtime.run(
            RunRequest(
                user_input="hi",
                tenant_id="tenant-acme",
                principal_id="",
                trace_id="trace-denied-001",
                session_id="session-denied-001",
                agent_id="agent-runtime-ref",
            ),
        )
        assert result.status == "denied"
        session = runtime.sessions.get_session("session-denied-001")
        assert session is not None
        assert session.traces == ["trace-denied-001"]
        runs = runtime.sessions.runs_for_session("session-denied-001")
        assert len(runs) == 1
        assert runs[0].status == "denied"
        assert runs[0].failure_reason == "principal_missing"
        event_types = [event.event_type for event in runtime.telemetry.events]
        assert event_types == ["run_start", "policy_precheck", "run_complete"]
        run_complete = runtime.telemetry.events[-1]
        assert run_complete.payload["session_id"] == "session-denied-001"

    def test_runtime_marks_validation_failure_tool_path_as_failed(self) -> None:
        runtime = AgentRuntime()
        result = runtime.run(
            RunRequest(
                user_input="Please create a ticket without the usual safeguards.",
                tenant_id="tenant-acme",
                principal_id="user-42",
                trace_id="trace-tool-failure-001",
                session_id="session-tool-failure-001",
                agent_id="agent-runtime-ref",
                authorization_mode="human_approved",
            ),
        )
        assert result.status == "failed"
        assert "validation_failure" in result.output_text
        session = runtime.sessions.get_session("session-tool-failure-001")
        assert session is not None
        runs = runtime.sessions.runs_for_session("session-tool-failure-001")
        assert runs[-1].status == "failed"
        summary = runtime.sessions._session_payload("session-tool-failure-001")["summary"]
        assert summary["failed_runs"] == 1
        assert summary["traceable_failed_runs"] == 1
        exported_run = runtime.sessions._session_payload("session-tool-failure-001")["runs"][-1]
        assert exported_run["failure_reason"] == "missing_idempotency_key"
        event_types = [event.event_type for event in runtime.telemetry.events]
        assert "run_failed" in event_types
        run_failed = next(
            event for event in runtime.telemetry.events if event.event_type == "run_failed"
        )
        assert run_failed.payload["tool_status"] == "validation_failure"

    def test_cli_inspect_trace_requires_trace_id_for_multi_trace_file(
        self, cli_json, tmp_path: Path
    ) -> None:
        first = tmp_path / "first.jsonl"
        second = tmp_path / "second.jsonl"
        merged = tmp_path / "merged.jsonl"

        code_a, _ = cli_json(
            [
                "export-events",
                "--user-input",
                "Please create a ticket for this onboarding issue.",
                "--trace-id",
                "trace-multi-a",
                "--output",
                str(first),
            ],
        )
        code_b, _ = cli_json(
            [
                "export-events",
                "--user-input",
                "What language preference do you remember?",
                "--trace-id",
                "trace-multi-b",
                "--output",
                str(second),
            ],
        )
        assert code_a == 0 and code_b == 0
        merged.write_text(
            first.read_text(encoding="utf-8") + second.read_text(encoding="utf-8"), encoding="utf-8"
        )

        from agent_runtime_ref.__main__ import main

        with pytest.raises(ValueError, match="multiple trace IDs"):
            main(["inspect-trace", "--input", str(merged)])

    def test_cli_inspect_trace_rejects_empty_event_file(self, tmp_path: Path) -> None:
        output_path = tmp_path / "empty.jsonl"
        output_path.write_text("", encoding="utf-8")

        from agent_runtime_ref.__main__ import main

        with pytest.raises(ValueError, match="Trace file does not contain any trace IDs"):
            main(["inspect-trace", "--input", str(output_path)])

    def test_cli_inspect_trace_rejects_invalid_json_event_lines(
        self, tmp_path: Path
    ) -> None:
        output_path = tmp_path / "invalid-json-event.jsonl"
        output_path.write_text("\n{not-json}\n", encoding="utf-8")

        from agent_runtime_ref.__main__ import main

        with pytest.raises(
            ValueError, match="Telemetry event line is not valid JSON: 2"
        ):
            main(["inspect-trace", "--input", str(output_path)])

    def test_cli_inspect_trace_rejects_non_mapping_event_records(
        self, tmp_path: Path
    ) -> None:
        output_path = tmp_path / "non-mapping-event.jsonl"
        output_path.write_text(json.dumps(["not", "an", "event"]) + "\n", encoding="utf-8")

        from agent_runtime_ref.__main__ import main

        with pytest.raises(TypeError, match="Telemetry event must be a mapping"):
            main(["inspect-trace", "--input", str(output_path)])

    @pytest.mark.parametrize("missing_field", ["event_type", "trace_id"])
    def test_cli_inspect_trace_rejects_events_missing_required_fields(
        self, missing_field: str, tmp_path: Path
    ) -> None:
        event = {
            "schema_version": "1.0",
            "event_type": "run_start",
            "trace_id": "trace-missing-field",
            "payload": {},
            "redacted_fields": [],
        }
        event.pop(missing_field)
        output_path = tmp_path / "missing-field.jsonl"
        output_path.write_text(json.dumps(event) + "\n", encoding="utf-8")

        from agent_runtime_ref.__main__ import main

        with pytest.raises(
            ValueError,
            match=f"Telemetry event is missing required field: {missing_field}",
        ):
            main(["inspect-trace", "--input", str(output_path)])

    @pytest.mark.parametrize("empty_field", ["event_type", "trace_id"])
    def test_cli_inspect_trace_rejects_events_with_empty_required_fields(
        self, empty_field: str, tmp_path: Path
    ) -> None:
        event = {
            "schema_version": "1.0",
            "event_type": "run_start",
            "trace_id": "trace-empty-field",
            "payload": {},
            "redacted_fields": [],
        }
        event[empty_field] = " "
        output_path = tmp_path / "empty-field.jsonl"
        output_path.write_text(json.dumps(event) + "\n", encoding="utf-8")

        from agent_runtime_ref.__main__ import main

        with pytest.raises(
            ValueError,
            match=f"Telemetry event field must not be empty: {empty_field}",
        ):
            main(["inspect-trace", "--input", str(output_path)])

    @pytest.mark.parametrize(
        ("event_patch", "expected_message"),
        [
            ({"schema_version": " "}, "Telemetry event field must not be empty: schema_version"),
            (
                {"schema_version": "2.0"},
                "Telemetry schema version is not supported: 2.0",
            ),
            ({"payload": []}, "payload must be a mapping"),
            ({"redacted_fields": "trace_id"}, "redacted_fields must be a list"),
        ],
    )
    def test_cli_inspect_trace_rejects_malformed_event_shapes(
        self, event_patch: dict[str, object], expected_message: str, tmp_path: Path
    ) -> None:
        event: dict[str, object] = {
            "schema_version": "1.0",
            "event_type": "run_start",
            "trace_id": "trace-bad-shape",
            "payload": {},
            "redacted_fields": [],
        }
        event.update(event_patch)
        output_path = tmp_path / "bad-shape.jsonl"
        output_path.write_text(json.dumps(event) + "\n", encoding="utf-8")

        from agent_runtime_ref.__main__ import main

        with pytest.raises((TypeError, ValueError), match=expected_message):
            main(["inspect-trace", "--input", str(output_path)])

    def test_cli_replay_run_rejects_empty_event_file(self, tmp_path: Path) -> None:
        output_path = tmp_path / "empty.jsonl"
        output_path.write_text("", encoding="utf-8")

        from agent_runtime_ref.__main__ import main

        with pytest.raises(ValueError, match="Trace file does not contain any trace IDs"):
            main(["replay-run", "--input", str(output_path)])

    def test_cli_rejects_malformed_sandbox_profile_config(
        self, config_dir: Path, tmp_path: Path
    ) -> None:
        from agent_runtime_ref.__main__ import main

        bad_config_dir = tmp_path / "configs"
        shutil.copytree(config_dir, bad_config_dir)
        (bad_config_dir / "runtime-controls.yaml").write_text(
            "runtime_controls:\n  sandbox_profile:\n    - not-a-mapping\n",
            encoding="utf-8",
        )

        expected = "runtime_controls.sandbox_profile config must be a mapping"
        with pytest.raises(TypeError, match=expected):
            main(["inspect-lifecycle", "--config-dir", str(bad_config_dir)])
        with pytest.raises(TypeError, match=expected):
            main(["simulate-run", "--config-dir", str(bad_config_dir)])

        (bad_config_dir / "runtime-controls.yaml").write_text(
            "runtime_controls:\n"
            "  sandbox_profile:\n"
            "    manifest_version: 1\n"
            "    workspace:\n"
            "      - not-a-mapping\n",
            encoding="utf-8",
        )
        with pytest.raises(
            TypeError,
            match="runtime_controls.sandbox_profile.workspace config must be a mapping",
        ):
            main(["inspect-lifecycle", "--config-dir", str(bad_config_dir)])

        (bad_config_dir / "runtime-controls.yaml").write_text(
            "runtime_controls:\n"
            "  sandbox_profile:\n"
            "    manifest_version: 1\n"
            "    workspace:\n"
            "      entries: src\n",
            encoding="utf-8",
        )
        expected_entries = "runtime_controls.sandbox_profile.workspace.entries must be a list"
        with pytest.raises(TypeError, match=expected_entries):
            main(["inspect-lifecycle", "--config-dir", str(bad_config_dir)])
        with pytest.raises(TypeError, match=expected_entries):
            main(["simulate-run", "--config-dir", str(bad_config_dir)])

    def test_cli_replay_run_rejects_incomplete_run_start_payload(
        self, tmp_path: Path
    ) -> None:
        output_path = tmp_path / "incomplete-run-start.jsonl"
        output_path.write_text(
            json.dumps(
                {
                    "schema_version": "1.0",
                    "event_type": "run_start",
                    "trace_id": "trace-incomplete-replay",
                    "payload": {"tenant_id": "tenant-acme"},
                    "redacted_fields": [],
                }
            )
            + "\n",
            encoding="utf-8",
        )

        from agent_runtime_ref.__main__ import main

        with pytest.raises(
            ValueError,
            match="Trace run_start event is missing replay fields: user_input, principal_id",
        ):
            main(["replay-run", "--input", str(output_path)])

    def test_cli_replay_run_rejects_multiple_run_start_events(
        self, tmp_path: Path
    ) -> None:
        output_path = tmp_path / "multiple-run-start.jsonl"
        run_start_payload = {
            "user_input": "What language preference do you remember?",
            "tenant_id": "tenant-acme",
            "principal_id": "user-42",
        }
        events = [
            {
                "schema_version": "1.0",
                "event_type": "run_start",
                "trace_id": "trace-ambiguous-replay",
                "payload": run_start_payload,
                "redacted_fields": [],
            },
            {
                "schema_version": "1.0",
                "event_type": "run_start",
                "trace_id": "trace-ambiguous-replay",
                "payload": {**run_start_payload, "user_input": "Please create a ticket."},
                "redacted_fields": [],
            },
        ]
        output_path.write_text(
            "".join(json.dumps(event) + "\n" for event in events),
            encoding="utf-8",
        )

        from agent_runtime_ref.__main__ import main

        with pytest.raises(ValueError, match="Trace file contains multiple run_start events"):
            main(["replay-run", "--input", str(output_path)])

    @pytest.mark.parametrize(
        ("field", "value"),
        [
            ("user_input", ["not", "text"]),
            ("tenant_id", {"tenant": "acme"}),
            ("principal_id", 42),
            ("session_id", ["session-replay-001"]),
            ("agent_id", {"agent": "support-triage-ref"}),
        ],
    )
    def test_cli_replay_run_rejects_non_string_run_start_payload_fields(
        self, field: str, value: object, tmp_path: Path
    ) -> None:
        payload: dict[str, object] = {
            "user_input": "What language preference do you remember?",
            "tenant_id": "tenant-acme",
            "principal_id": "user-42",
            "session_id": "session-replay-001",
            "agent_id": "support-triage-ref",
        }
        payload[field] = value
        output_path = tmp_path / "non-string-run-start.jsonl"
        output_path.write_text(
            json.dumps(
                {
                    "schema_version": "1.0",
                    "event_type": "run_start",
                    "trace_id": "trace-non-string-replay",
                    "payload": payload,
                    "redacted_fields": [],
                }
            )
            + "\n",
            encoding="utf-8",
        )

        from agent_runtime_ref.__main__ import main

        with pytest.raises(
            TypeError,
            match=f"Telemetry event payload value must be a string: {field}",
        ):
            main(["replay-run", "--input", str(output_path)])

    @pytest.mark.parametrize(
        "field",
        ["user_input", "tenant_id", "principal_id", "session_id", "agent_id"],
    )
    def test_cli_replay_run_rejects_blank_run_start_payload_fields(
        self, field: str, tmp_path: Path
    ) -> None:
        payload = {
            "user_input": "What language preference do you remember?",
            "tenant_id": "tenant-acme",
            "principal_id": "user-42",
            "session_id": "session-blank-replay-source",
            "agent_id": "support-triage-ref",
        }
        payload[field] = "   "
        output_path = tmp_path / "blank-run-start.jsonl"
        output_path.write_text(
            json.dumps(
                {
                    "schema_version": "1.0",
                    "event_type": "run_start",
                    "trace_id": "trace-blank-replay",
                    "payload": payload,
                    "redacted_fields": [],
                }
            )
            + "\n",
            encoding="utf-8",
        )

        from agent_runtime_ref.__main__ import main

        with pytest.raises(
            ValueError,
            match=f"Trace run_start replay field must not be empty: {field}",
        ):
            main(["replay-run", "--input", str(output_path)])

    def test_cli_replay_run_rejects_non_string_redacted_fields(
        self, tmp_path: Path
    ) -> None:
        output_path = tmp_path / "non-string-redacted-fields.jsonl"
        output_path.write_text(
            json.dumps(
                {
                    "schema_version": "1.0",
                    "event_type": "run_start",
                    "trace_id": "trace-non-string-redacted-fields",
                    "payload": {
                        "user_input": "[REDACTED]",
                        "tenant_id": "tenant-acme",
                        "principal_id": "user-1",
                    },
                    "redacted_fields": [["user_input"]],
                }
            )
            + "\n",
            encoding="utf-8",
        )

        from agent_runtime_ref.__main__ import main

        with pytest.raises(TypeError, match="redacted_fields entries must be strings"):
            main(["replay-run", "--input", str(output_path)])

    @pytest.mark.parametrize("field", ["user_input", "session_id", "agent_id"])
    def test_cli_replay_run_rejects_redacted_run_start_payload(
        self, field: str, tmp_path: Path
    ) -> None:
        output_path = tmp_path / "redacted-run-start.jsonl"
        payload = {
            "user_input": "What language preference do you remember?",
            "tenant_id": "tenant-acme",
            "principal_id": "user-42",
            "session_id": "session-redacted-replay-source",
            "agent_id": "support-triage-ref",
        }
        payload[field] = "[REDACTED]"
        output_path.write_text(
            json.dumps(
                {
                    "schema_version": "1.0",
                    "event_type": "run_start",
                    "trace_id": "trace-redacted-replay-source",
                    "payload": payload,
                    "redacted_fields": [field],
                }
            )
            + "\n",
            encoding="utf-8",
        )

        from agent_runtime_ref.__main__ import main

        with pytest.raises(
            ValueError,
            match=f"Trace run_start event has redacted replay fields: {field}",
        ):
            main(["replay-run", "--input", str(output_path)])

    def test_cli_replay_run_rejects_untrimmed_redacted_run_start_fields(
        self, tmp_path: Path
    ) -> None:
        output_path = tmp_path / "untrimmed-redacted-run-start.jsonl"
        output_path.write_text(
            json.dumps(
                {
                    "schema_version": "1.0",
                    "event_type": "run_start",
                    "trace_id": "trace-untrimmed-redacted-replay",
                    "payload": {
                        "user_input": "[REDACTED]",
                        "tenant_id": "tenant-acme",
                        "principal_id": "user-1",
                    },
                    "redacted_fields": [" user_input ", "user_input"],
                }
            )
            + "\n",
            encoding="utf-8",
        )

        from agent_runtime_ref.__main__ import main

        with pytest.raises(
            ValueError,
            match="Trace run_start event has redacted replay fields: user_input",
        ):
            main(["replay-run", "--input", str(output_path)])

    def test_cli_replay_run_rejects_missing_trace_id(self, cli_json, tmp_path: Path) -> None:
        output_path = tmp_path / "trace.jsonl"
        code, _ = cli_json(
            [
                "export-events",
                "--user-input",
                "What language preference do you remember?",
                "--trace-id",
                "trace-replay-source-2",
                "--output",
                str(output_path),
            ],
        )
        assert code == 0

        from agent_runtime_ref.__main__ import main

        with pytest.raises(ValueError, match="Trace ID not found"):
            main(
                [
                    "replay-run",
                    "--input",
                    str(output_path),
                    "--trace-id",
                    "trace-does-not-exist",
                ]
            )

    def test_cli_simulate_run_supports_failure_injection(self, cli_json) -> None:
        code, payload = cli_json(
            [
                "simulate-run",
                "--trace-id",
                "trace-cli-failure-001",
                "--simulate-failure",
                "tool_timeout",
            ]
        )
        assert code == 0
        assert payload["status"] == "failed"
        assert payload["failure_reason"] == "tool_timeout"
        assert "tool_timeout" in payload["result"]

    @pytest.mark.parametrize(
        ("command", "expected_status", "expected_failure_reason"),
        [
            (
                ["simulate-run", "--simulate-failure", "tool_timeout"],
                "failed",
                "tool_timeout",
            ),
            (
                ["simulate-run", "--simulate-failure", "upstream_unavailable"],
                "failed",
                "upstream_unavailable",
            ),
            (["simulate-run", "--tenant-id", " "], "denied", "tenant_missing"),
            (["simulate-run", "--principal-id", " "], "denied", "principal_missing"),
            (["simulate-run", "--agent-id", " "], "denied", "agent_identity_missing"),
        ],
    )
    def test_cli_simulate_run_non_happy_paths_keep_documented_contract(
        self,
        command: list[str],
        expected_status: str,
        expected_failure_reason: str,
        cli_json,
    ) -> None:
        code, payload = cli_json(command)
        assert code == 0
        assert set(payload) == {
            "agent_id",
            "session_id",
            "result",
            "status",
            "failure_reason",
            "trace_id",
            "events",
            "memory_records",
            "pending_approvals",
            "config_dir",
        }
        assert payload["agent_id"] == "support-triage-ref"
        assert payload["session_id"] == "session-demo-001"
        assert payload["status"] == expected_status
        assert payload["failure_reason"] == expected_failure_reason
        assert payload["trace_id"] == "trace-demo-001"
        assert payload["pending_approvals"] == 0
        assert payload["config_dir"].endswith("agent_runtime_ref/configs")

    def test_cli_export_events_supports_failure_injection(self, cli_json, tmp_path: Path) -> None:
        output_path = tmp_path / "failed-trace.jsonl"
        code, payload = cli_json(
            [
                "export-events",
                "--trace-id",
                "trace-cli-export-failure-001",
                "--simulate-failure",
                "upstream_unavailable",
                "--output",
                str(output_path),
            ]
        )
        assert code == 0
        assert set(payload) == {
            "output_path",
            "trace_id",
            "status",
            "result",
            "event_count",
            "redact_fields",
            "failure_reason",
        }
        assert payload["output_path"] == str(output_path)
        assert payload["trace_id"] == "trace-cli-export-failure-001"
        assert payload["status"] == "failed"
        assert payload["failure_reason"] == "upstream_unavailable"
        assert "upstream_unavailable" in payload["result"]
        assert payload["redact_fields"] == []
        assert output_path.exists()
        lines = output_path.read_text(encoding="utf-8").strip().splitlines()
        assert payload["event_count"] == len(lines)
        assert any("run_failed" in line for line in lines)

    def test_cli_dump_events_surfaces_failure_reason(self, cli_json) -> None:
        code, payload = cli_json(
            [
                "dump-events",
                "--trace-id",
                "trace-cli-dump-failure-001",
                "--simulate-failure",
                "tool_timeout",
            ]
        )
        assert code == 0
        assert set(payload) == {
            "status",
            "result",
            "failure_reason",
            "trace_id",
            "event_count",
            "events",
        }
        assert payload["trace_id"] == "trace-cli-dump-failure-001"
        assert payload["status"] == "failed"
        assert payload["failure_reason"] == "tool_timeout"
        assert "tool_timeout" in payload["result"]
        assert payload["event_count"] == len(payload["events"])
        assert any(event["event_type"] == "run_failed" for event in payload["events"])

    def test_cli_run_event_commands_normalize_session_id_for_lookup(
        self, cli_json, tmp_path: Path
    ) -> None:
        padded_session_id = " session-cli-normalized-001 "
        simulate_code, simulate_payload = cli_json(
            ["simulate-run", "--session-id", padded_session_id]
        )
        assert simulate_code == 0
        assert simulate_payload["session_id"] == "session-cli-normalized-001"

        dump_code, dump_payload = cli_json(["dump-events", "--session-id", padded_session_id])
        assert dump_code == 0
        run_start = next(
            event for event in dump_payload["events"] if event["event_type"] == "run_start"
        )
        assert run_start["payload"]["session_id"] == "session-cli-normalized-001"

        output_path = tmp_path / "normalized-session-trace.jsonl"
        export_code, export_payload = cli_json(
            ["export-events", "--session-id", padded_session_id, "--output", str(output_path)]
        )
        assert export_code == 0
        assert export_payload["status"] == "success"
        assert output_path.exists()

    def test_cli_trace_commands_normalize_trace_id_for_lineage(
        self, cli_json, tmp_path: Path
    ) -> None:
        padded_trace_id = " trace-cli-normalized-001 "
        simulate_code, simulate_payload = cli_json(
            ["simulate-run", "--trace-id", padded_trace_id]
        )
        assert simulate_code == 0
        assert simulate_payload["trace_id"] == "trace-cli-normalized-001"

        dump_code, dump_payload = cli_json(["dump-events", "--trace-id", padded_trace_id])
        assert dump_code == 0
        assert dump_payload["trace_id"] == "trace-cli-normalized-001"
        assert {event["trace_id"] for event in dump_payload["events"]} == {
            "trace-cli-normalized-001"
        }

        output_path = tmp_path / "normalized-trace.jsonl"
        export_code, export_payload = cli_json(
            ["export-events", "--trace-id", padded_trace_id, "--output", str(output_path)]
        )
        assert export_code == 0
        assert export_payload["trace_id"] == "trace-cli-normalized-001"

        inspect_code, inspect_payload = cli_json(
            ["inspect-trace", "--input", str(output_path), "--trace-id", padded_trace_id]
        )
        assert inspect_code == 0
        assert inspect_payload["trace_id"] == "trace-cli-normalized-001"

        replay_code, replay_payload = cli_json(
            [
                "replay-run",
                "--input",
                str(output_path),
                "--trace-id",
                padded_trace_id,
                "--replay-trace-id",
                " trace-cli-normalized-replay-001 ",
            ]
        )
        assert replay_code == 0
        assert replay_payload["source_trace_id"] == "trace-cli-normalized-001"
        assert replay_payload["replay_trace_id"] == "trace-cli-normalized-replay-001"

    def test_cli_session_commands_normalize_session_id_for_lookup(
        self, cli_json, tmp_path: Path
    ) -> None:
        padded_session_id = " session-cli-normalized-002 "
        commands = [
            ["inspect-session", "--session-id", padded_session_id],
            ["session-eval-summary", "--session-id", padded_session_id],
            ["session-replay", "--session-id", padded_session_id],
            [
                "export-session",
                "--session-id",
                padded_session_id,
                "--output",
                str(tmp_path / "normalized-session.json"),
            ],
        ]
        for command in commands:
            code, payload = cli_json(command)
            assert code == 0
            assert payload["session_id"] == "session-cli-normalized-002"

    def test_cli_export_eval_dataset_includes_sandbox_profile_review_rule(
        self, cli_json, tmp_path: Path
    ) -> None:
        output_path = tmp_path / "eval-dataset.json"
        code, payload = cli_json(
            [
                "export-eval-dataset",
                "--output",
                str(output_path),
                "--scenario",
                "support_ticket",
            ]
        )
        assert code == 0
        assert payload["session_count"] == 1
        data = json.loads(output_path.read_text(encoding="utf-8"))
        session = data["sessions"][0]
        assert "sandbox_profile_review" in session["eval"]["labels"]
        assert session["eval"]["expected_outcomes"]["sandbox_profile_reviewed"] is True
        sandbox_rule = next(
            rule
            for rule in session["eval"]["grading_rules"]
            if rule["type"] == "sandbox_profile_review"
        )
        assert set(sandbox_rule) == {"type", "expected", "blocking"}
        assert sandbox_rule["blocking"] is True
        assert sandbox_rule["expected"] == {
            "sandbox_profile_contract": "sandbox-profile-v1",
            "workspace_entries_reviewed": True,
            "permissions_profile": "restricted-shell-network-denied",
            "network_secrets_posture": "network:denied,secrets:none",
            "snapshot_policy": "required_on_completion",
        }

    def test_cli_export_eval_dataset_includes_failed_run_scenario(
        self, cli_json, tmp_path: Path
    ) -> None:
        output_path = tmp_path / "eval-dataset.json"
        code, payload = cli_json(
            [
                "export-eval-dataset",
                "--output",
                str(output_path),
                "--scenario",
                "failed_run_timeout",
            ]
        )
        assert code == 0
        assert payload["session_count"] == 1
        assert payload["failed_runs"] == 1
        assert payload["traceable_failed_runs"] == 1
        assert payload["latest_failure_reason"] == "tool_timeout"
        data = json.loads(output_path.read_text(encoding="utf-8"))
        session = data["sessions"][0]
        assert session["summary"]["failed_runs"] == 1
        assert session["runs"][-1]["failure_reason"] == "tool_timeout"
        assert session["eval"]["expected_outcomes"]["failed_run_traceable"] is True

    def test_cli_export_eval_dataset_rejects_blank_export_fields(self) -> None:
        from agent_runtime_ref.__main__ import main

        with pytest.raises(ValueError, match="CLI field is required: dataset_name"):
            main(["export-eval-dataset", "--dataset-name", " "])
        with pytest.raises(ValueError, match="CLI field is required: session_prefix"):
            main(["export-eval-dataset", "--session-prefix", " "])

    def test_cli_session_commands_reject_blank_trace_prefix(self) -> None:
        from agent_runtime_ref.__main__ import main

        for command in (
            "inspect-session",
            "session-eval-summary",
            "session-replay",
            "export-session",
        ):
            with pytest.raises(ValueError, match="CLI field is required: trace_prefix"):
                main([command, "--trace-prefix", " "])

    def test_cli_export_eval_dataset_rejects_duplicate_scenarios(self) -> None:
        from agent_runtime_ref.__main__ import main

        with pytest.raises(ValueError, match="CLI field entries must be unique: scenario"):
            main(
                [
                    "export-eval-dataset",
                    "--scenario",
                    "support_ticket",
                    "--scenario",
                    "support_ticket",
                ]
            )

    def test_cli_export_eval_dataset_rejects_unknown_scenarios(self) -> None:
        from agent_runtime_ref.__main__ import main

        with pytest.raises(
            ValueError,
            match="CLI field is not supported: scenario=suport_ticket",
        ):
            main(["export-eval-dataset", "--scenario", " suport_ticket "])


class TestExecutionAndPolicyBranches:
    def test_execute_tool_returns_denied_payload(self, config_dir: Path) -> None:
        capability = load_capability_catalog(config_dir / "capabilities.yaml").get("search_docs")
        assert capability is not None
        result = execute_tool(
            capability,
            ToolRequest(capability_name="search_docs", arguments={"query": "policy"}),
            PolicyDecision("deny", "configured_deny", "cap_410"),
        )
        assert result.status == "denied"
        assert result.payload["reason"] == "configured_deny"

    def test_execute_tool_returns_approval_required_payload(self, config_dir: Path) -> None:
        capability = load_capability_catalog(config_dir / "capabilities.yaml").get("create_ticket")
        assert capability is not None
        result = execute_tool(
            capability,
            ToolRequest(capability_name="create_ticket", arguments={"title": "x"}),
            PolicyDecision("approval_required", "write_action", "cap_201"),
        )
        assert result.status == "approval_required"
        assert result.payload["reason"] == "write_action"

    def test_execute_tool_returns_validation_failure_without_idempotency_key(
        self, config_dir: Path
    ) -> None:
        capability = load_capability_catalog(config_dir / "capabilities.yaml").get("create_ticket")
        assert capability is not None
        result = execute_tool(
            capability,
            ToolRequest(capability_name="create_ticket", arguments={"title": "x"}),
            PolicyDecision("allow", "approved_write", "cap_202"),
        )
        assert result.status == "validation_failure"
        assert result.payload["reason"] == "missing_idempotency_key"

        normalized_result = execute_tool(
            capability,
            ToolRequest(
                capability_name="create_ticket",
                arguments={" idempotency_key ": "ticket-123"},
            ),
            PolicyDecision("allow", "approved_write", "cap_202"),
        )
        assert normalized_result.status == "success"

    def test_execute_tool_can_simulate_timeout_failure(self, config_dir: Path) -> None:
        capability = load_capability_catalog(config_dir / "capabilities.yaml").get("search_docs")
        assert capability is not None
        result = execute_tool(
            capability,
            ToolRequest(
                capability_name="search_docs",
                arguments={"query": "policy", "simulate_failure": "tool_timeout"},
            ),
            PolicyDecision("allow", "low_risk_read", "cap_101"),
        )
        assert result.status == "failed"
        assert result.payload["reason"] == "tool_timeout"

    def test_execute_tool_can_simulate_upstream_unavailable_failure(
        self, config_dir: Path
    ) -> None:
        capability = load_capability_catalog(config_dir / "capabilities.yaml").get("search_docs")
        assert capability is not None
        result = execute_tool(
            capability,
            ToolRequest(
                capability_name="search_docs",
                arguments={"query": "policy", "simulate_failure": "upstream_unavailable"},
            ),
            PolicyDecision("allow", "low_risk_read", "cap_101"),
        )
        assert result.status == "failed"
        assert result.payload["reason"] == "upstream_unavailable"

    def test_execute_tool_success_includes_contract_payload(self, config_dir: Path) -> None:
        capability = load_capability_catalog(config_dir / "capabilities.yaml").get("search_docs")
        assert capability is not None
        result = execute_tool(
            capability,
            ToolRequest(capability_name=" search_docs ", arguments={"query": "architecture"}),
            PolicyDecision(" allow ", "low_risk_read", "cap_101"),
        )
        assert result.capability_name == "search_docs"
        assert result.status == "success"
        assert result.payload["transport"] == capability.transport
        assert result.payload["tool_principal"] == capability.tool_principal

    def test_execute_tool_rejects_bad_request_arguments(self, config_dir: Path) -> None:
        capability = load_capability_catalog(config_dir / "capabilities.yaml").get("search_docs")
        assert capability is not None
        bad_arguments = cast(dict[str, str], [])
        with pytest.raises(TypeError, match="Tool request arguments must be a mapping"):
            execute_tool(
                capability,
                ToolRequest(capability_name="search_docs", arguments=bad_arguments),
                PolicyDecision("allow", "low_risk_read", "cap_101"),
            )

        with pytest.raises(
            TypeError,
            match="Tool request argument key must be a string",
        ):
            execute_tool(
                capability,
                ToolRequest(
                    capability_name="search_docs",
                    arguments=cast(dict[str, str], {1: "policy"}),
                ),
                PolicyDecision("allow", "low_risk_read", "cap_101"),
            )

        with pytest.raises(
            ValueError,
            match="Tool request argument key must not be empty",
        ):
            execute_tool(
                capability,
                ToolRequest(
                    capability_name="search_docs",
                    arguments={" ": "policy"},
                ),
                PolicyDecision("allow", "low_risk_read", "cap_101"),
            )

        with pytest.raises(
            TypeError,
            match="Tool request argument value must be a string: query",
        ):
            execute_tool(
                capability,
                ToolRequest(
                    capability_name="search_docs",
                    arguments=cast(dict[str, str], {" query ": 2}),
                ),
                PolicyDecision("allow", "low_risk_read", "cap_101"),
            )

    @pytest.mark.parametrize(
        ("capability_name", "expected_message"),
        [
            (" ", "Tool request capability name must not be empty"),
            (
                "create_ticket",
                "Tool request capability does not match catalog entry: "
                "create_ticket != search_docs",
            ),
        ],
    )
    def test_execute_tool_rejects_bad_request_capability_names(
        self, capability_name: str, expected_message: str, config_dir: Path
    ) -> None:
        capability = load_capability_catalog(config_dir / "capabilities.yaml").get("search_docs")
        assert capability is not None
        with pytest.raises(ValueError, match=expected_message):
            execute_tool(
                capability,
                ToolRequest(capability_name=capability_name, arguments={"query": "policy"}),
                PolicyDecision("allow", "low_risk_read", "cap_101"),
            )

        with pytest.raises(TypeError, match="Tool request capability name must be a string"):
            execute_tool(
                capability,
                ToolRequest(
                    capability_name=cast(str, 7),
                    arguments={"query": "policy"},
                ),
                PolicyDecision("allow", "low_risk_read", "cap_101"),
            )
        with pytest.raises(ValueError, match="Tool request capability name must not be empty"):
            load_capability_catalog(config_dir / "capabilities.yaml").get(" ")

    @pytest.mark.parametrize("action", ["", "escalate"])
    def test_execute_tool_rejects_unsupported_policy_actions(
        self, action: str, config_dir: Path
    ) -> None:
        capability = load_capability_catalog(config_dir / "capabilities.yaml").get("search_docs")
        assert capability is not None
        with pytest.raises(ValueError, match=f"Policy action is not supported: {action}"):
            execute_tool(
                capability,
                ToolRequest(capability_name="search_docs", arguments={"query": "policy"}),
                PolicyDecision(action, "malformed_policy_action", "cap_bad"),
            )

    def test_policy_from_dict_rejects_bad_shapes(self) -> None:
        with pytest.raises(TypeError, match="'policy' must be a mapping"):
            PolicyEngine.from_dict({"policy": []})
        with pytest.raises(TypeError, match="'run_precheck' must be a mapping"):
            PolicyEngine.from_dict({"policy": {"run_precheck": []}})
        with pytest.raises(TypeError, match="'capabilities' must be a mapping"):
            PolicyEngine.from_dict({"policy": {"capabilities": []}})
        with pytest.raises(TypeError, match="'memory_write' must be a mapping"):
            PolicyEngine.from_dict({"policy": {"memory_write": []}})
        with pytest.raises(TypeError, match="'execution' must be a mapping"):
            PolicyEngine.from_dict({"policy": {"execution": []}})
        with pytest.raises(TypeError, match="'run_precheck.require_tenant' must be a boolean"):
            PolicyEngine.from_dict(
                {"policy": {"run_precheck": {"require_tenant": "false"}}}
            )
        with pytest.raises(
            TypeError,
            match="'run_precheck.deny_if_principal_missing' must be a boolean",
        ):
            PolicyEngine.from_dict(
                {
                    "policy": {
                        "run_precheck": {"deny_if_principal_missing": "true"}
                    }
                }
            )
        with pytest.raises(ValueError, match="Policy capability name must not be empty"):
            PolicyEngine.from_dict({"policy": {"capabilities": {" ": {"decision": "allow"}}}})
        with pytest.raises(TypeError, match="Policy decision must be a string"):
            PolicyEngine.from_dict(
                {"policy": {"capabilities": {"search_docs": {"decision": 7}}}}
            )
        with pytest.raises(ValueError, match="Policy decision is not supported: escalate"):
            PolicyEngine.from_dict(
                {"policy": {"capabilities": {"search_docs": {"decision": "escalate"}}}}
            )
        with pytest.raises(ValueError, match="Policy decision is not supported: "):
            PolicyEngine.from_dict(
                {"policy": {"capabilities": {"search_docs": {"decision": " "}}}}
            )
        with pytest.raises(TypeError, match="Policy capability names must be strings"):
            PolicyEngine.from_dict(
                {"policy": {"capabilities": {7: {"decision": "allow"}}}}
            )
        with pytest.raises(TypeError, match="Policy approver must be a string"):
            PolicyEngine.from_dict(
                {
                    "policy": {
                        "capabilities": {
                            "create_ticket": {
                                "decision": "approval_required",
                                "approver": 7,
                            }
                        }
                    }
                }
            )
        with pytest.raises(
            ValueError, match="Policy approver must not be empty: create_ticket"
        ):
            PolicyEngine.from_dict(
                {
                    "policy": {
                        "capabilities": {
                            "create_ticket": {
                                "decision": "approval_required",
                                "approver": " ",
                            }
                        }
                    }
                }
            )
        with pytest.raises(ValueError, match="Policy capability names must be unique"):
            PolicyEngine.from_dict(
                {
                    "policy": {
                        "capabilities": {
                            "search_docs": {"decision": "allow"},
                            " search_docs ": {"decision": "deny"},
                        }
                    }
                }
            )
        normalized_policy = PolicyEngine.from_dict(
            {
                "policy": {
                    "capabilities": {
                        "search_docs": {"decision": " allow "},
                        "create_ticket": {
                            "decision": "approval_required",
                            "approver": " runtime-review ",
                        },
                    }
                }
            }
        )
        assert normalized_policy.capability_policies["search_docs"].decision == "allow"
        assert normalized_policy.capability_policies["create_ticket"].approver == "runtime-review"
        direct_policy = PolicyEngine(
            capability_policies={
                " search_docs ": CapabilityPolicy(" allow "),
                " create_ticket ": CapabilityPolicy(
                    " approval_required ",
                    " runtime-review ",
                ),
            }
        )
        assert direct_policy.capability_policies["search_docs"].decision == "allow"
        assert direct_policy.capability_policies["create_ticket"].approver == "runtime-review"
        with pytest.raises(TypeError, match="Policy capability names must be strings"):
            PolicyEngine(
                capability_policies=cast(
                    dict[str, CapabilityPolicy],
                    {7: CapabilityPolicy("allow")},
                )
            )
        with pytest.raises(ValueError, match="Policy capability name must not be empty"):
            PolicyEngine(capability_policies={" ": CapabilityPolicy("allow")})
        with pytest.raises(ValueError, match="Policy capability names must be unique"):
            PolicyEngine(
                capability_policies={
                    "search_docs": CapabilityPolicy("allow"),
                    " search_docs ": CapabilityPolicy("deny"),
                }
            )
        with pytest.raises(TypeError, match="Policy decision must be a string"):
            CapabilityPolicy(cast(str, 7))
        with pytest.raises(TypeError, match="Policy approver must be a string"):
            CapabilityPolicy("approval_required", cast(str, 7))
        with pytest.raises(ValueError, match="Policy decision is not supported: escalate"):
            CapabilityPolicy(" escalate ")
        with pytest.raises(
            ValueError,
            match="Policy approver must not be empty: create_ticket",
        ):
            PolicyEngine(
                capability_policies={
                    "create_ticket": CapabilityPolicy("approval_required", " ")
                }
            )
        with pytest.raises(
            TypeError, match="memory_write.allow_kinds entries must be strings"
        ):
            PolicyEngine.from_dict(
                {"policy": {"memory_write": {"allow_kinds": [7]}}}
            )
        with pytest.raises(ValueError, match="memory_write.allow_kinds entries must not be empty"):
            PolicyEngine.from_dict(
                {"policy": {"memory_write": {"allow_kinds": [" "]}}}
            )
        with pytest.raises(
            ValueError, match="memory_write.allow_kinds entries must be unique"
        ):
            PolicyEngine.from_dict(
                {
                    "policy": {
                        "memory_write": {
                            "allow_kinds": ["validated_fact", " validated_fact "]
                        }
                    }
                }
            )
        with pytest.raises(
            TypeError, match="execution.allow_network_access entries must be strings"
        ):
            PolicyEngine.from_dict(
                {"policy": {"execution": {"allow_network_access": [7]}}}
            )
        with pytest.raises(
            ValueError, match="execution.allow_network_access entries must not be empty"
        ):
            PolicyEngine.from_dict(
                {"policy": {"execution": {"allow_network_access": [""]}}}
            )
        with pytest.raises(
            ValueError, match="execution.allow_network_access entries must be unique"
        ):
            PolicyEngine.from_dict(
                {
                    "policy": {
                        "execution": {
                            "allow_network_access": ["restricted", " restricted "]
                        }
                    }
                }
            )

    def test_policy_precheck_denies_missing_tenant_and_agent(self) -> None:
        engine = PolicyEngine()
        tenant_missing = engine.precheck(
            RunRequest(
                user_input="hi",
                tenant_id="",
                principal_id="user-1",
                trace_id="trace-precheck-tenant",
                agent_id="agent-runtime-ref",
            ),
        )
        agent_missing = engine.precheck(
            RunRequest(
                user_input="hi",
                tenant_id="tenant-acme",
                principal_id="user-1",
                trace_id="trace-precheck-agent",
                agent_id="",
            ),
        )
        assert tenant_missing.reason == "tenant_missing"
        assert agent_missing.reason == "agent_identity_missing"

    def test_policy_evaluate_tool_covers_configured_allow_and_deny(self, config_dir: Path) -> None:
        capability = load_capability_catalog(config_dir / "capabilities.yaml").get("search_docs")
        assert capability is not None
        context = RunContext(
            tenant_id="tenant-acme", principal_id="user-1", trace_id="trace-pol-001"
        )
        allow_engine = PolicyEngine(
            capability_policies={" search_docs ": CapabilityPolicy(" allow ")}
        )
        deny_engine = PolicyEngine(capability_policies={"search_docs": CapabilityPolicy("deny")})
        allow_decision = allow_engine.evaluate_tool(
            context,
            ToolRequest(capability_name="search_docs", arguments={"query": "x"}),
            capability,
        )
        deny_decision = deny_engine.evaluate_tool(
            context,
            ToolRequest(capability_name="search_docs", arguments={"query": "x"}),
            capability,
        )
        assert allow_decision.reason == "configured_allow"
        assert deny_decision.reason == "configured_deny"

    def test_policy_evaluate_tool_covers_network_and_mode_branches(self) -> None:
        from agent_runtime_ref.catalog import CapabilitySpec

        engine = PolicyEngine(allowed_network_access={" restricted "})
        context = RunContext(
            tenant_id="tenant-acme", principal_id="user-1", trace_id="trace-pol-002"
        )
        blocked_network = CapabilitySpec(
            name="external_tool",
            owner="platform",
            mode="read",
            transport="gateway",
            timeout_seconds=5,
            tool_principal="svc-external",
            risk_tier="low",
            network_access="open",
            allowed_egress=("example.com",),
        )
        approved_write = CapabilitySpec(
            name=" write_tool ",
            owner=" platform ",
            mode=" write ",
            transport=" gateway ",
            timeout_seconds=5,
            tool_principal=" svc-write ",
            risk_tier=" medium ",
            network_access=" restricted ",
            allowed_egress=(" internal ",),
            approval_required=False,
        )
        unsupported_mode = CapabilitySpec(
            name="odd_tool",
            owner="platform",
            mode="admin",
            transport="gateway",
            timeout_seconds=5,
            tool_principal="svc-admin",
            risk_tier="medium",
            network_access="restricted",
            allowed_egress=("internal",),
        )
        blocked = engine.evaluate_tool(
            context,
            ToolRequest(capability_name="external_tool", arguments={}),
            blocked_network,
        )
        write_allowed = engine.evaluate_tool(
            context,
            ToolRequest(capability_name="write_tool", arguments={}),
            approved_write,
        )
        unsupported = engine.evaluate_tool(
            context,
            ToolRequest(capability_name="odd_tool", arguments={}),
            unsupported_mode,
        )
        assert blocked.reason == "network_access_not_allowed"
        assert write_allowed.reason == "approved_write"
        assert unsupported.reason == "unsupported_mode"

        with pytest.raises(
            TypeError,
            match="execution.allow_network_access entries must be strings",
        ):
            PolicyEngine(allowed_network_access=cast(set[str], {7}))
        with pytest.raises(
            ValueError,
            match="execution.allow_network_access entries must not be empty",
        ):
            PolicyEngine(allowed_network_access={" "})
        with pytest.raises(
            ValueError,
            match="execution.allow_network_access entries must be unique",
        ):
            PolicyEngine(allowed_network_access={"restricted", " restricted "})

    def test_policy_evaluate_tool_covers_critical_risk_branch(self) -> None:
        from agent_runtime_ref.catalog import CapabilitySpec

        capability = CapabilitySpec(
            name="critical_tool",
            owner="platform",
            mode="read",
            transport="gateway",
            timeout_seconds=5,
            tool_principal="svc-critical",
            risk_tier="critical",
            network_access="restricted",
            allowed_egress=("internal",),
        )
        decision = PolicyEngine().evaluate_tool(
            RunContext(tenant_id="tenant-acme", principal_id="user-1", trace_id="trace-pol-003"),
            ToolRequest(capability_name="critical_tool", arguments={}),
            capability,
        )
        assert decision.action == "approval_required"
        assert decision.reason == "critical_risk_tier"

    def test_policy_allow_memory_write_normalizes_kind(self) -> None:
        decision = PolicyEngine(allowed_memory_kinds={"profile"}).allow_memory_write(
            "session_summary"
        )
        assert decision.action == "deny"
        assert decision.reason == "memory_kind_denied"

        allowed = PolicyEngine(allowed_memory_kinds={" session_summary "}).allow_memory_write(
            " session_summary "
        )
        assert allowed.action == "allow"
        assert allowed.reason == "memory_kind_allowed"

        with pytest.raises(
            TypeError,
            match="memory_write.allow_kinds entries must be strings",
        ):
            PolicyEngine(allowed_memory_kinds=cast(set[str], {7}))
        with pytest.raises(
            ValueError,
            match="memory_write.allow_kinds entries must not be empty",
        ):
            PolicyEngine(allowed_memory_kinds={" "})
        with pytest.raises(
            ValueError,
            match="memory_write.allow_kinds entries must be unique",
        ):
            PolicyEngine(allowed_memory_kinds={"session_summary", " session_summary "})
        with pytest.raises(TypeError, match="Policy memory kind must be a string"):
            PolicyEngine().allow_memory_write(cast(str, 7))
        with pytest.raises(ValueError, match="Policy memory kind must not be empty"):
            PolicyEngine().allow_memory_write(" ")


class TestRuntimeCore:
    def test_config_loader_builds_runtime_components(
        self,
        config_dir: Path,
        runtime_from_config: AgentRuntime,
    ) -> None:
        result = runtime_from_config.run(
            RunRequest(
                user_input="Please open a ticket for this issue.",
                tenant_id="tenant-acme",
                principal_id="user-7",
                trace_id="trace-config-001",
                agent_id=runtime_from_config.agent.agent_id,
            ),
        )
        assert result.status == "success"
        assert runtime_from_config.agent.agent_id == "support-triage-ref"
        assert runtime_from_config.catalog.get("create_ticket") is not None
        assert runtime_from_config.policy.allow_memory_write("session_summary").action == "allow"
        assert len(runtime_from_config.memory.all()) >= 4

        from agent_runtime_ref.identity import AgentIdentity

        direct_agent = AgentIdentity(
            agent_id=" support-triage-ref ",
            display_name=" Support Triage ",
            owner_team=" support-ops ",
            runtime_principal=" svc-agent-runtime-ref ",
        )
        direct_runtime = AgentRuntime(agent=direct_agent)
        direct_result = direct_runtime.run(
            RunRequest(
                user_input="Summarize the current architecture.",
                tenant_id="tenant-acme",
                principal_id="user-7",
                trace_id="trace-direct-agent-identity-001",
                agent_id=" support-triage-ref ",
            ),
        )
        assert direct_result.status == "success"
        assert direct_runtime.agent.agent_id == "support-triage-ref"
        assert direct_runtime.agent.runtime_principal == "svc-agent-runtime-ref"
        run_start = direct_runtime.telemetry.events[0]
        assert run_start.payload["agent_id"] == "support-triage-ref"
        assert run_start.payload["runtime_principal"] == "svc-agent-runtime-ref"

    @pytest.mark.parametrize(
        ("user_input", "expected_fragment"),
        [
            ("Summarize the current architecture.", "Reference runtime completed"),
            ("What language preference do you remember?", "Retrieved profile hint"),
        ],
    )
    def test_runtime_paths_return_expected_output(
        self,
        user_input: str,
        expected_fragment: str,
    ) -> None:
        runtime = AgentRuntime()
        result = runtime.run(
            RunRequest(
                user_input=user_input,
                tenant_id="tenant-acme",
                principal_id="user-1",
                trace_id="trace-runtime-001",
                agent_id="agent-runtime-ref",
            ),
        )
        assert result.status == "success"
        assert expected_fragment in result.output_text

    def test_runtime_rejects_blank_user_input(self) -> None:
        runtime = AgentRuntime()
        with pytest.raises(ValueError, match="Run request field is required: user_input"):
            runtime.run(
                RunRequest(
                    user_input=" ",
                    tenant_id="tenant-acme",
                    principal_id="user-1",
                    trace_id="trace-blank-input-001",
                    agent_id="agent-runtime-ref",
                ),
            )
        assert runtime.telemetry.events == []

    def test_runtime_rejects_blank_trace_and_session_ids_before_telemetry(self) -> None:
        required_fields = {
            "trace_id": {
                "trace_id": " ",
                "session_id": "session-runtime-required-001",
            },
            "session_id": {
                "trace_id": "trace-runtime-required-001",
                "session_id": " ",
            },
        }
        for field, payload in required_fields.items():
            runtime = AgentRuntime()
            with pytest.raises(ValueError, match=f"Run request field is required: {field}"):
                runtime.run(
                    RunRequest(
                        user_input="Summarize the current architecture.",
                        tenant_id="tenant-acme",
                        principal_id="user-1",
                        agent_id="agent-runtime-ref",
                        **payload,
                    ),
                )
            assert runtime.telemetry.events == []

        runtime = AgentRuntime()
        result = runtime.run(
            RunRequest(
                user_input="Summarize the current architecture.",
                tenant_id=" tenant-acme ",
                principal_id=" user-1 ",
                trace_id=" trace-runtime-normalized-001 ",
                session_id=" session-runtime-normalized-001 ",
                agent_id=" agent-runtime-ref ",
            ),
        )
        assert result.status == "success"
        assert runtime.telemetry.events[0].payload["tenant_id"] == "tenant-acme"
        assert runtime.telemetry.events[0].payload["principal_id"] == "user-1"
        assert runtime.telemetry.events[0].payload["agent_id"] == "agent-runtime-ref"
        assert runtime.telemetry.events[0].trace_id == "trace-runtime-normalized-001"
        assert runtime.sessions.get_session("session-runtime-normalized-001") is not None

    def test_runtime_rejects_bad_direct_sandbox_workspace_entries(self) -> None:
        runtime = AgentRuntime(sandbox_profile={"workspace": {"entries": "src"}})
        with pytest.raises(TypeError, match="Sandbox profile workspace entries must be a list"):
            runtime.run(
                RunRequest(
                    user_input="Please open a ticket for this issue.",
                    tenant_id="tenant-acme",
                    principal_id="user-1",
                    trace_id="trace-bad-sandbox-001",
                    session_id="session-bad-sandbox-001",
                    agent_id="agent-runtime-ref",
                ),
            )
        event_types = [event.event_type for event in runtime.telemetry.events]
        assert "sandbox_profile_reviewed" not in event_types

    def test_runtime_rejects_malformed_request_fields_before_telemetry(self) -> None:
        malformed_fields = (
            ("user_input", {"user_input": cast(str, 7)}),
            ("tenant_id", {"tenant_id": cast(str, 7)}),
            ("principal_id", {"principal_id": cast(str, 7)}),
            ("trace_id", {"trace_id": cast(str, 7)}),
            ("session_id", {"session_id": cast(str, 7)}),
            ("agent_id", {"agent_id": cast(str, 7)}),
            ("authorization_mode", {"authorization_mode": cast(str, 7)}),
            ("delegated_principal_id", {"delegated_principal_id": cast(str, 7)}),
            ("delegated_scope", {"delegated_scope": cast(str, 7)}),
        )
        for field, override in malformed_fields:
            runtime = AgentRuntime()
            request = RunRequest(
                user_input="Summarize the current architecture.",
                tenant_id="tenant-acme",
                principal_id="user-1",
                trace_id="trace-runtime-type-001",
                session_id="session-runtime-type-001",
                agent_id="agent-runtime-ref",
            )
            for key, value in override.items():
                setattr(request, key, value)
            with pytest.raises(TypeError, match=f"Run request field must be a string: {field}"):
                runtime.run(request)
            assert runtime.telemetry.events == []
            assert runtime.sessions.get_session("session-runtime-type-001") is None

    def test_runtime_rejects_blank_authorization_mode_before_telemetry(self) -> None:
        runtime = AgentRuntime()
        with pytest.raises(ValueError, match="Run request field is required: authorization_mode"):
            runtime.run(
                RunRequest(
                    user_input="Summarize the current architecture.",
                    tenant_id="tenant-acme",
                    principal_id="user-1",
                    trace_id="trace-blank-authz-001",
                    session_id="session-blank-authz-001",
                    agent_id="agent-runtime-ref",
                    authorization_mode=" ",
                ),
            )
        with pytest.raises(
            ValueError,
            match="Authorization mode is not supported: magic_token",
        ):
            runtime.run(
                RunRequest(
                    user_input="Summarize the current architecture.",
                    tenant_id="tenant-acme",
                    principal_id="user-1",
                    trace_id="trace-unknown-authz-001",
                    session_id="session-unknown-authz-001",
                    agent_id="agent-runtime-ref",
                    authorization_mode=" magic_token ",
                ),
            )
        assert runtime.telemetry.events == []
        assert runtime.sessions.get_session("session-unknown-authz-001") is None

        normalized = AgentRuntime()
        result = normalized.run(
            RunRequest(
                user_input="Summarize the current architecture.",
                tenant_id="tenant-acme",
                principal_id="user-1",
                trace_id="trace-authz-normalized-001",
                session_id="session-authz-normalized-001",
                agent_id="agent-runtime-ref",
                authorization_mode=" platform_owned ",
            ),
        )
        assert result.status == "success"
        run = normalized.sessions.runs_for_session("session-authz-normalized-001")[0]
        assert run.authorization_mode == "platform_owned"

    def test_runtime_uses_tool_path_for_ticket_request(self) -> None:
        runtime = AgentRuntime()
        result = runtime.run(
            RunRequest(
                user_input="Please open a ticket for this issue.",
                tenant_id="tenant-acme",
                principal_id="user-2",
                trace_id="trace-ticket-001",
                agent_id="agent-runtime-ref",
            ),
        )
        assert result.status == "success"
        assert "waiting for human approval" in result.output_text
        assert len(runtime.approvals.pending()) == 1

    def test_runtime_normalizes_model_tool_capability_before_policy(self) -> None:
        class PaddedToolRuntime(AgentRuntime):
            def _call_model(
                self,
                request: RunRequest,
                context: RunContext,
                *,
                second_pass: bool = False,
            ) -> ModelOutput:
                if second_pass:
                    return ModelOutput(text="Padded tool request was handled safely.")
                return ModelOutput(
                    text="needs create ticket",
                    tool_request=ToolRequest(
                        capability_name=" create_ticket ",
                        arguments={"idempotency_key": "ticket-123"},
                    ),
                )

        runtime = PaddedToolRuntime()
        result = runtime.run(
            RunRequest(
                user_input="Please create a ticket for this issue.",
                tenant_id="tenant-acme",
                principal_id="user-2",
                trace_id="trace-padded-tool-001",
                agent_id="agent-runtime-ref",
            ),
        )
        approval = runtime.approvals.pending()[0]
        policy_event = next(
            event
            for event in runtime.telemetry.events
            if event.event_type == "tool_policy_decision"
        )
        execution_event = next(
            event for event in runtime.telemetry.events if event.event_type == "tool_execution"
        )

        assert result.status == "success"
        assert approval.capability_name == "create_ticket"
        assert policy_event.payload["capability"] == "create_ticket"
        assert policy_event.payload["reason"] == "write_action"
        assert execution_event.payload["capability"] == "create_ticket"

    def test_runtime_handles_unknown_tool_capability_as_policy_denial(self) -> None:
        class UnknownToolRuntime(AgentRuntime):
            def _call_model(
                self,
                request: RunRequest,
                context: RunContext,
                *,
                second_pass: bool = False,
            ) -> ModelOutput:
                if second_pass:
                    return ModelOutput(text="Unknown tool was denied safely.")
                return ModelOutput(
                    text="needs unavailable tool",
                    tool_request=ToolRequest(
                        capability_name="missing_capability",
                        arguments={},
                    ),
                )

        runtime = UnknownToolRuntime()
        result = runtime.run(
            RunRequest(
                user_input="Call the missing capability.",
                tenant_id="tenant-acme",
                principal_id="user-2",
                trace_id="trace-unknown-tool-001",
                agent_id="agent-runtime-ref",
            ),
        )
        session_run = runtime.sessions.runs_for_session("session-demo-001")[0]
        policy_events = [
            event
            for event in runtime.telemetry.events
            if event.event_type == "tool_policy_decision"
        ]
        execution_events = [
            event for event in runtime.telemetry.events if event.event_type == "tool_execution"
        ]

        assert result.status == "failed"
        assert session_run.status == "failed"
        assert session_run.failure_reason == "capability_unknown"
        assert "missing_capability returned denied" in session_run.output_text
        assert runtime.telemetry.events[-1].event_type == "run_complete"
        assert policy_events[0].payload["reason"] == "capability_unknown"
        assert policy_events[0].payload["policy_id"] == "cap_404"
        assert execution_events[0].payload["capability"] == "missing_capability"
        assert execution_events[0].payload["status"] == "denied"

    def test_runtime_rejects_bad_second_pass_model_output(self) -> None:
        class BadSecondPassRuntime(AgentRuntime):
            def _call_model(
                self,
                request: RunRequest,
                context: RunContext,
                *,
                second_pass: bool = False,
            ) -> ModelOutput:
                if second_pass:
                    return cast(ModelOutput, {"text": "not a model output"})
                return ModelOutput(
                    text="needs a tool",
                    tool_request=ToolRequest(
                        capability_name="search_docs",
                        arguments={"query": "architecture"},
                    ),
                )

        runtime = BadSecondPassRuntime()
        with pytest.raises(TypeError, match="Model step must return ModelOutput"):
            runtime.run(
                RunRequest(
                    user_input="Summarize the current architecture.",
                    tenant_id="tenant-acme",
                    principal_id="user-2",
                    trace_id="trace-bad-second-pass-model-001",
                    agent_id="agent-runtime-ref",
                ),
            )
        assert runtime.sessions.runs_for_session("session-demo-001") == ()
        assert {event.event_type for event in runtime.telemetry.events} >= {
            "tool_execution",
            "span",
        }
        assert "run_complete" not in {event.event_type for event in runtime.telemetry.events}

    def test_background_persisted_records_include_revision_and_provenance(self) -> None:
        runtime = AgentRuntime()
        runtime.run(
            RunRequest(
                user_input="Please open a ticket for this issue.",
                tenant_id="tenant-acme",
                principal_id="user-3",
                trace_id="trace-memory-001",
                agent_id="agent-runtime-ref",
            ),
        )
        persisted_event = next(
            event for event in runtime.telemetry.events if event.event_type == "memory_persisted"
        )
        assert "provenance" in persisted_event.payload
        assert "revision" in persisted_event.payload
        assert persisted_event.payload["revision"] == "1"

    def test_runtime_emits_context_layers(self) -> None:
        runtime = AgentRuntime()
        runtime.run(
            RunRequest(
                user_input="What language preference do you remember?",
                tenant_id="tenant-acme",
                principal_id="user-4",
                trace_id="trace-context-001",
                agent_id="agent-runtime-ref",
            ),
        )
        context_event = next(
            event
            for event in runtime.telemetry.events
            if event.event_type == "context_layers_built"
        )
        assert int(context_event.payload["static_items"]) >= 1
        assert int(context_event.payload["retrieved_items"]) >= 1

    def test_memory_store_filters_by_tenant(self) -> None:
        store = MemoryStore()
        records = store.retrieve("language preference", " tenant-acme ", limit=5)
        assert records
        assert all(record.tenant_id == "tenant-acme" for record in records)
        assert all(record.provenance for record in records)

    def test_memory_store_rejects_blank_lookup_tenant(self) -> None:
        store = MemoryStore()
        with pytest.raises(TypeError, match="Memory lookup field must be a string: tenant_id"):
            store.retrieve("language preference", cast(str, 7))
        with pytest.raises(TypeError, match="Memory lookup field must be a string: tenant_id"):
            store.compact(cast(str, 7))
        with pytest.raises(ValueError, match="Memory lookup field is required: tenant_id"):
            store.retrieve("language preference", " ")
        with pytest.raises(ValueError, match="Memory lookup field is required: tenant_id"):
            store.compact(" ")

    def test_memory_store_rejects_malformed_retrieve_limits(self) -> None:
        store = MemoryStore()
        with pytest.raises(TypeError, match="Memory lookup limit must be an integer"):
            store.retrieve("language preference", "tenant-acme", limit=True)
        with pytest.raises(TypeError, match="Memory lookup limit must be an integer"):
            store.retrieve("language preference", "tenant-acme", limit=cast(int, "2"))
        with pytest.raises(ValueError, match="Memory lookup limit must be non-negative"):
            store.retrieve("language preference", "tenant-acme", limit=-1)


class TestRuntimeControlPaths:
    def test_runtime_control_config_exposes_session_governance_ownership(
        self, config_dir: Path
    ) -> None:
        from agent_runtime_ref.config import load_yaml_file

        payload = load_yaml_file(config_dir / "runtime-controls.yaml")
        controls = payload["runtime_controls"]
        capability_sessions = controls["capability_sessions"]

        assert controls["capability_session_owner"] == "support-ops"
        assert controls["expiry_signal_owner"] == "support-ops"
        assert controls["emergency_freeze_owner"] == "platform-runtime"
        assert capability_sessions["expiry_policy"] == "reinitialize_or_cancel"
        assert capability_sessions["reinit_policy"] == "resume_existing_session_if_valid"

    def test_runtime_control_config_exposes_sandbox_profile_contract(
        self, config_dir: Path
    ) -> None:
        payload = load_yaml_file(config_dir / "runtime-controls.yaml")
        sandbox_profile = payload["runtime_controls"]["sandbox_profile"]

        assert sandbox_profile["manifest_version"] == 1
        assert sandbox_profile["workspace"]["entries"] == [
            {"path": "repo", "source": "local_dir", "read_only": False},
            {"path": "task.md", "source": "inline_file", "read_only": True},
        ]
        assert sandbox_profile["capabilities"] == {
            "filesystem": True,
            "shell": "restricted",
            "memory": "read_write",
            "skills": "read_only",
        }
        assert sandbox_profile["permissions"] == {
            "network": "denied",
            "secrets": "none",
            "run_as": "sandbox_user",
        }
        assert sandbox_profile["state"] == {
            "resume": "allowed",
            "snapshot": "required_on_completion",
            "persist_session_state": True,
        }

    def test_lifecycle_configs_expose_session_governance_ownership(self, config_dir: Path) -> None:
        from agent_runtime_ref.config import load_yaml_file

        change = load_yaml_file(config_dir / "change.yaml")["change"]
        retirement = load_yaml_file(config_dir / "retirement.yaml")["retirement"]
        bundle = load_yaml_file(config_dir / "artifacts.yaml")["bundle"]

        assert "runtime-controls.yaml" in change["artifacts"]
        assert "capability_session_contract" in change["affected_surfaces"]
        assert "sandbox_profile_contract" in change["affected_surfaces"]
        assert "session_expiry_behavior_checked" in change["required_signals"]
        assert "sandbox_profile_reviewed" in change["required_signals"]
        assert change["session_control_owner"] == "support-ops"
        assert change["emergency_freeze_owner"] == "platform-runtime"

        assert "freeze_reinitialization" in retirement["required_steps"]
        assert "capability_session_state" in retirement["archive_targets"]
        assert retirement["session_control_owner"] == "support-ops"
        assert retirement["emergency_freeze_owner"] == "platform-runtime"

        assert bundle["version"] == "2026.04.16"
        assert bundle["session_control_owner"] == "support-ops"
        assert "runtime-control-bundle-metadata" in bundle["artifacts"]

    def test_runtime_approval_request_emits_expected_trace_signals(self) -> None:
        runtime = AgentRuntime()
        trace_id = "trace-approval-signals-001"
        session_id = "session-approval-signals-001"
        result = runtime.run(
            RunRequest(
                user_input="Please create a ticket for this onboarding issue.",
                tenant_id="tenant-acme",
                principal_id="user-22",
                trace_id=trace_id,
                session_id=session_id,
                agent_id="agent-runtime-ref",
            ),
        )
        assert result.status == "success"
        approval_requested = next(
            event for event in runtime.telemetry.events if event.event_type == "approval_requested"
        )
        tool_execution = next(
            event for event in runtime.telemetry.events if event.event_type == "tool_execution"
        )
        session_record = runtime.sessions.get_session(session_id)
        assert approval_requested.trace_id == trace_id
        assert approval_requested.payload["status"] == "pending"
        assert approval_requested.payload["capability_session_id"].startswith("cap-session-")
        assert approval_requested.payload["capability_session_status"] == "pending"
        assert tool_execution.payload["status"] == "approval_required"
        assert tool_execution.payload["tool_principal"] == "pending_review"
        assert len(runtime.approvals.pending()) == 1
        assert session_record is not None
        run_record = runtime.sessions.runs_for_session(session_id)[0]
        assert run_record.capability_session_id.startswith("cap-session-")
        assert run_record.capability_session_status == "pending"

    def test_approval_queue_resolution_updates_capability_session_status(self) -> None:
        from agent_runtime_ref.approvals import ApprovalPolicy, ApprovalQueue

        policy = ApprovalPolicy(default_reviewer=" manager ", escalation_sla_minutes=30)
        queue_with_direct_policy = ApprovalQueue(policy)
        default_review_request = queue_with_direct_policy.submit(
            trace_id="trace-approval-default-reviewer-001",
            capability_name="create_ticket",
            requested_by="user-1",
            reviewer=None,
            reason="write_action",
            session_id="session-approval-default-reviewer-001",
        )
        assert policy.default_reviewer == "manager"
        assert default_review_request.reviewer == "manager"

        queue = AgentRuntime().approvals
        request = queue.submit(
            trace_id=" trace-approval-resolve-001 ",
            capability_name=" create_ticket ",
            requested_by=" user-1 ",
            reviewer=" manager ",
            reason=" write_action ",
            session_id=" session-approval-resolve-001 ",
        )
        resolved = queue.resolve(
            " apr-001 ",
            decision=" approved ",
            note=" ok ",
        )
        assert request.trace_id == "trace-approval-resolve-001"
        assert request.capability_name == "create_ticket"
        assert request.requested_by == "user-1"
        assert request.reviewer == "manager"
        assert request.reason == "write_action"
        assert request.session_id == "session-approval-resolve-001"
        assert resolved.status == "approved"
        assert resolved.capability_session_status == "approved"
        assert resolved.resolution_note == "ok"

    def test_approval_queue_rejects_blank_submit_evidence_fields(self) -> None:
        required_fields = (
            ("trace_id", " ", "create_ticket", "user-1", None, "write_action"),
            (
                "capability_name",
                "trace-approval-required-001",
                " ",
                "user-1",
                None,
                "write_action",
            ),
            (
                "requested_by",
                "trace-approval-required-001",
                "create_ticket",
                " ",
                None,
                "write_action",
            ),
            (
                "reviewer",
                "trace-approval-required-001",
                "create_ticket",
                "user-1",
                " ",
                "write_action",
            ),
            ("reason", "trace-approval-required-001", "create_ticket", "user-1", None, " "),
            (
                "session_id",
                "trace-approval-required-001",
                "create_ticket",
                "user-1",
                None,
                "write_action",
            ),
        )
        for field, trace_id, capability_name, requested_by, reviewer, reason in required_fields:
            queue = AgentRuntime().approvals
            with pytest.raises(ValueError, match=f"Approval field is required: {field}"):
                queue.submit(
                    trace_id=trace_id,
                    capability_name=capability_name,
                    requested_by=requested_by,
                    reviewer=reviewer,
                    reason=reason,
                    session_id=(
                        " " if field == "session_id" else "session-approval-required-001"
                    ),
                )
            assert queue.all() == ()

    def test_approval_queue_rejects_malformed_submit_evidence_fields(self) -> None:
        malformed_fields = (
            ("trace_id", {"trace_id": cast(str, 7)}),
            ("capability_name", {"capability_name": cast(str, 7)}),
            ("requested_by", {"requested_by": cast(str, 7)}),
            ("reviewer", {"reviewer": cast(str | None, 7)}),
            ("reason", {"reason": cast(str, 7)}),
            ("session_id", {"session_id": cast(str, 7)}),
            ("authorization_mode", {"authorization_mode": cast(str, 7)}),
        )
        for field, override in malformed_fields:
            queue = AgentRuntime().approvals
            kwargs = {
                "trace_id": "trace-approval-type-001",
                "capability_name": "create_ticket",
                "requested_by": "user-1",
                "reviewer": None,
                "reason": "write_action",
                "session_id": "session-approval-type-001",
            }
            kwargs.update(override)
            with pytest.raises(TypeError, match=f"Approval field must be a string: {field}"):
                queue.submit(**cast(Any, kwargs))
            assert queue.all() == ()

    def test_approval_queue_rejects_unknown_authorization_mode(self) -> None:
        queue = AgentRuntime().approvals
        with pytest.raises(
            ValueError,
            match="Authorization mode is not supported: magic_token",
        ):
            queue.submit(
                trace_id="trace-approval-unknown-authz-001",
                capability_name="create_ticket",
                requested_by="user-1",
                reviewer=None,
                reason="write_action",
                session_id="session-approval-unknown-authz-001",
                authorization_mode=" magic_token ",
            )
        assert queue.all() == ()

    def test_approval_queue_requires_delegated_submit_identity_fields(self) -> None:
        required_fields = {
            "delegated_principal_id": {
                "delegated_principal_id": " ",
                "delegated_scope": "tickets.write",
            },
            "delegated_scope": {
                "delegated_principal_id": "user-1",
                "delegated_scope": " ",
            },
        }
        for field, delegated_fields in required_fields.items():
            queue = AgentRuntime().approvals
            with pytest.raises(ValueError, match=f"Approval field is required: {field}"):
                queue.submit(
                    trace_id="trace-approval-delegated-required-001",
                    capability_name="create_ticket",
                    requested_by="user-1",
                    reviewer=None,
                    reason="write_action",
                    session_id="session-approval-delegated-required-001",
                    authorization_mode=" user_delegated ",
                    **delegated_fields,
                )
            assert queue.all() == ()

        malformed_fields = {
            "delegated_principal_id": {
                "delegated_principal_id": cast(str, 7),
                "delegated_scope": "tickets.write",
            },
            "delegated_scope": {
                "delegated_principal_id": "user-1",
                "delegated_scope": cast(str, 7),
            },
        }
        for field, delegated_fields in malformed_fields.items():
            queue = AgentRuntime().approvals
            with pytest.raises(TypeError, match=f"Approval field must be a string: {field}"):
                queue.submit(
                    trace_id="trace-approval-delegated-type-001",
                    capability_name="create_ticket",
                    requested_by="user-1",
                    reviewer=None,
                    reason="write_action",
                    session_id="session-approval-delegated-type-001",
                    authorization_mode=" user_delegated ",
                    **delegated_fields,
                )
            assert queue.all() == ()

        queue = AgentRuntime().approvals
        request = queue.submit(
            trace_id="trace-approval-delegated-normalized-001",
            capability_name="create_ticket",
            requested_by="user-1",
            reviewer=None,
            reason="write_action",
            session_id="session-approval-delegated-normalized-001",
            authorization_mode=" user_delegated ",
            delegated_principal_id=" user-1 ",
            delegated_scope=" tickets.write ",
        )
        assert request.authorization_mode == "user_delegated"
        assert request.delegated_principal_id == "user-1"
        assert request.delegated_scope == "tickets.write"

    def test_approval_queue_rejects_unsupported_resolution_decisions(self) -> None:
        queue = AgentRuntime().approvals
        request = queue.submit(
            trace_id="trace-approval-bad-decision-001",
            capability_name="create_ticket",
            requested_by="user-1",
            reviewer=None,
            reason="write_action",
            session_id="session-approval-bad-decision-001",
        )
        with pytest.raises(TypeError, match="Approval field must be a string: decision"):
            queue.resolve(request.approval_id, decision=cast(str, 7))
        with pytest.raises(TypeError, match="Approval field must be a string: note"):
            queue.resolve(request.approval_id, decision="approved", note=cast(str, 7))
        with pytest.raises(ValueError, match="Approval field is required: decision"):
            queue.resolve(request.approval_id, decision=" ")
        with pytest.raises(ValueError, match="Approval decision is not supported: maybe"):
            queue.resolve(request.approval_id, decision="maybe")
        assert request.status == "pending"
        assert request.capability_session_status == "pending"

    def test_approval_queue_rejects_blank_resolution_id(self) -> None:
        queue = AgentRuntime().approvals
        request = queue.submit(
            trace_id="trace-approval-blank-resolve-001",
            capability_name="create_ticket",
            requested_by="user-1",
            reviewer=None,
            reason="write_action",
            session_id="session-approval-blank-resolve-001",
        )
        with pytest.raises(ValueError, match="Approval field is required: approval_id"):
            queue.resolve(" ", decision="approved")
        assert request.status == "pending"
        assert request.capability_session_status == "pending"

    def test_approval_queue_rejects_duplicate_resolution(self) -> None:
        queue = AgentRuntime().approvals
        request = queue.submit(
            trace_id="trace-approval-duplicate-resolve-001",
            capability_name="create_ticket",
            requested_by="user-1",
            reviewer=None,
            reason="write_action",
            session_id="session-approval-duplicate-resolve-001",
        )
        queue.resolve(request.approval_id, decision="approved", note="first decision")

        with pytest.raises(
            ValueError,
            match=f"Approval request is not pending: {request.approval_id}",
        ):
            queue.resolve(request.approval_id, decision="rejected", note="second decision")
        assert request.status == "approved"
        assert request.capability_session_status == "approved"
        assert request.resolution_note == "first decision"

    def test_session_export_includes_capability_session_fields(self, tmp_path: Path) -> None:
        runtime = AgentRuntime()
        session_id = "session-export-capability-001"
        runtime.run(
            RunRequest(
                user_input="Please create a ticket for this onboarding issue.",
                tenant_id="tenant-acme",
                principal_id="user-55",
                trace_id="trace-export-capability-001",
                session_id=session_id,
                agent_id="agent-runtime-ref",
            ),
        )
        output_path = tmp_path / "session.json"
        runtime.sessions.export_session_json(f" {session_id} ", output_path=output_path)
        payload = json.loads(output_path.read_text(encoding="utf-8"))
        assert payload["session"]["session_id"] == session_id
        assert payload["runs"][0]["capability_session_id"].startswith("cap-session-")
        assert payload["runs"][0]["capability_session_status"] == "pending"

    def test_session_export_rejects_blank_session_id(self, tmp_path: Path) -> None:
        from agent_runtime_ref.session import SessionStore

        store = SessionStore()
        output_path = tmp_path / "blank-session.json"
        with pytest.raises(ValueError, match="Session field is required: session_id"):
            store.export_session_json(" ", output_path=output_path)
        assert not output_path.exists()

    def test_session_store_rejects_blank_identity_fields(self) -> None:
        from agent_runtime_ref.session import RunRecord, SessionStore, summarize_session

        store = SessionStore()
        required_fields = {
            "session_id": {
                "session_id": " ",
                "tenant_id": "tenant-acme",
                "principal_id": "user-1",
                "trace_id": "trace-session-required-001",
                "status": "success",
            },
            "trace_id": {
                "session_id": "session-required-001",
                "tenant_id": "tenant-acme",
                "principal_id": "user-1",
                "trace_id": " ",
                "status": "success",
            },
            "status": {
                "session_id": "session-required-001",
                "tenant_id": "tenant-acme",
                "principal_id": "user-1",
                "trace_id": "trace-session-required-001",
                "status": " ",
            },
            "user_input": {
                "session_id": "session-required-001",
                "tenant_id": "tenant-acme",
                "principal_id": "user-1",
                "trace_id": "trace-session-required-001",
                "status": "success",
                "user_input": " ",
            },
            "output_text": {
                "session_id": "session-required-001",
                "tenant_id": "tenant-acme",
                "principal_id": "user-1",
                "trace_id": "trace-session-required-001",
                "status": "success",
                "output_text": " ",
            },
            "failure_reason": {
                "session_id": "session-required-001",
                "tenant_id": "tenant-acme",
                "principal_id": "user-1",
                "trace_id": "trace-session-required-001",
                "status": "failed",
                "failure_reason": " ",
            },
        }
        for field, payload in required_fields.items():
            request = {"user_input": "hello", "output_text": "done", **payload}
            with pytest.raises(ValueError, match=f"Session field is required: {field}"):
                store.register_run(**request)

        record = store.register_run(
            session_id=" session-normalized-001 ",
            tenant_id=" tenant-acme ",
            principal_id=" user-1 ",
            trace_id=" trace-normalized-001 ",
            status=" success ",
            user_input=" hello ",
            output_text=" done ",
        )
        assert record.session_id == "session-normalized-001"
        assert record.trace_id == "trace-normalized-001"
        assert record.status == "success"
        assert record.user_input == "hello"
        assert record.output_text == "done"
        session = store.get_session(" session-normalized-001 ")
        assert session is not None
        assert session.session_id == "session-normalized-001"
        runs = store.runs_for_session(" session-normalized-001 ")
        assert len(runs) == 1
        assert runs[0].trace_id == "trace-normalized-001"

        direct_record = RunRecord(
            trace_id=" trace-direct-normalized-001 ",
            session_id=" session-direct-normalized-001 ",
            status=" failed ",
            user_input=" hello ",
            output_text=" failed cleanly ",
            failure_reason=" tool_timeout ",
            capability_session_id=" cap-session-001 ",
            capability_session_status=" failed ",
            authorization_mode=" user_delegated ",
            delegated_principal_id=" user-1 ",
            delegated_scope=" tickets.write ",
        )
        assert direct_record.status == "failed"
        assert direct_record.failure_reason == "tool_timeout"
        assert direct_record.authorization_mode == "user_delegated"
        assert direct_record.delegated_scope == "tickets.write"
        summary = summarize_session(
            " session-direct-normalized-001 ",
            (direct_record,),
        )
        assert summary.failed_runs == 1
        assert summary.traceable_failed_runs == 1
        with pytest.raises(ValueError, match="Session field is required: failure_reason"):
            RunRecord(
                trace_id="trace-direct-failed-required-001",
                session_id="session-direct-failed-required-001",
                status="failed",
                user_input="hello",
                output_text="failed cleanly",
                failure_reason=" ",
            )
        with pytest.raises(TypeError, match="Session field must be a string: trace_id"):
            RunRecord(
                trace_id=cast(str, 7),
                session_id="session-direct-type-001",
                status="success",
                user_input="hello",
                output_text="done",
            )
        with pytest.raises(TypeError, match="Session field must be a string: failure_reason"):
            RunRecord(
                trace_id="trace-direct-type-001",
                session_id="session-direct-type-001",
                status="failed",
                user_input="hello",
                output_text="done",
                failure_reason=cast(str, 7),
            )
        with pytest.raises(ValueError, match="Session status is not supported: maybe"):
            RunRecord(
                trace_id="trace-direct-bad-status-001",
                session_id="session-direct-bad-status-001",
                status=" maybe ",
                user_input="hello",
                output_text="done",
            )

    def test_session_store_rejects_malformed_identity_fields(self) -> None:
        from agent_runtime_ref.session import SessionStore

        malformed_fields = (
            ("session_id", {"session_id": cast(str, 7)}),
            ("tenant_id", {"tenant_id": cast(str, 7)}),
            ("principal_id", {"principal_id": cast(str, 7)}),
            ("trace_id", {"trace_id": cast(str, 7)}),
            ("status", {"status": cast(str, 7)}),
            ("user_input", {"user_input": cast(str, 7)}),
            ("output_text", {"output_text": cast(str, 7)}),
            ("failure_reason", {"status": "failed", "failure_reason": cast(str, 7)}),
            ("capability_session_id", {"capability_session_id": cast(str, 7)}),
            (
                "capability_session_status",
                {"capability_session_status": cast(str, 7)},
            ),
            ("authorization_mode", {"authorization_mode": cast(str, 7)}),
            ("delegated_principal_id", {"delegated_principal_id": cast(str, 7)}),
            ("delegated_scope", {"delegated_scope": cast(str, 7)}),
        )
        for field, override in malformed_fields:
            store = SessionStore()
            request = {
                "session_id": "session-type-001",
                "tenant_id": "tenant-acme",
                "principal_id": "user-1",
                "trace_id": "trace-session-type-001",
                "status": "success",
                "user_input": "hello",
                "output_text": "done",
            }
            request.update(override)
            with pytest.raises(TypeError, match=f"Session field must be a string: {field}"):
                store.register_run(**cast(Any, request))
            assert store.get_session("session-type-001") is None

    def test_session_lookup_rejects_blank_session_id(self) -> None:
        from agent_runtime_ref.session import SessionStore

        store = SessionStore()
        with pytest.raises(ValueError, match="Session field is required: session_id"):
            store.get_session(" ")
        with pytest.raises(ValueError, match="Session field is required: session_id"):
            store.runs_for_session(" ")

    def test_session_store_rejects_unsupported_run_statuses(self) -> None:
        from agent_runtime_ref.session import SessionStore

        store = SessionStore()
        with pytest.raises(ValueError, match="Session status is not supported: sucess"):
            store.register_run(
                session_id="session-bad-status-001",
                tenant_id="tenant-acme",
                principal_id="user-1",
                trace_id="trace-bad-status-001",
                status="sucess",
                user_input="hello",
                output_text="done",
            )
        assert store.get_session("session-bad-status-001") is None

    def test_session_store_rejects_session_tenant_mismatch(self) -> None:
        from agent_runtime_ref.session import SessionStore

        store = SessionStore()
        store.register_run(
            session_id="session-identity-stable-001",
            tenant_id="tenant-acme",
            principal_id="user-1",
            trace_id="trace-session-identity-001",
            status="success",
            user_input="hello",
            output_text="done",
        )

        with pytest.raises(
            ValueError,
            match="Session tenant_id does not match existing session: session-identity-stable-001",
        ):
            store.register_run(
                session_id="session-identity-stable-001",
                tenant_id="tenant-other",
                principal_id="user-1",
                trace_id="trace-session-identity-002",
                status="success",
                user_input="hello again",
                output_text="done again",
            )

        session = store.get_session("session-identity-stable-001")
        assert session is not None
        assert session.tenant_id == "tenant-acme"
        assert session.traces == ["trace-session-identity-001"]
        assert len(store.runs_for_session("session-identity-stable-001")) == 1

    def test_session_store_rejects_session_principal_mismatch(self) -> None:
        from agent_runtime_ref.session import SessionStore

        store = SessionStore()
        store.register_run(
            session_id="session-principal-stable-001",
            tenant_id="tenant-acme",
            principal_id="user-1",
            trace_id="trace-session-principal-001",
            status="success",
            user_input="hello",
            output_text="done",
        )

        with pytest.raises(
            ValueError,
            match=(
                "Session principal_id does not match existing session: "
                "session-principal-stable-001"
            ),
        ):
            store.register_run(
                session_id="session-principal-stable-001",
                tenant_id="tenant-acme",
                principal_id="user-2",
                trace_id="trace-session-principal-002",
                status="success",
                user_input="hello again",
                output_text="done again",
            )

        session = store.get_session("session-principal-stable-001")
        assert session is not None
        assert session.principal_id == "user-1"
        assert session.traces == ["trace-session-principal-001"]
        assert len(store.runs_for_session("session-principal-stable-001")) == 1

    def test_session_store_rejects_duplicate_trace_id(self) -> None:
        from agent_runtime_ref.session import SessionStore

        store = SessionStore()
        store.register_run(
            session_id="session-duplicate-trace-001",
            tenant_id="tenant-acme",
            principal_id="user-1",
            trace_id="trace-session-duplicate-001",
            status="success",
            user_input="hello",
            output_text="done",
        )

        with pytest.raises(
            ValueError,
            match="Session trace_id already exists: trace-session-duplicate-001",
        ):
            store.register_run(
                session_id="session-duplicate-trace-001",
                tenant_id="tenant-acme",
                principal_id="user-1",
                trace_id="trace-session-duplicate-001",
                status="success",
                user_input="hello again",
                output_text="done again",
            )

        session = store.get_session("session-duplicate-trace-001")
        assert session is not None
        assert session.traces == ["trace-session-duplicate-001"]
        assert len(store.runs_for_session("session-duplicate-trace-001")) == 1

    def test_session_store_rejects_duplicate_trace_id_across_sessions(self) -> None:
        from agent_runtime_ref.session import SessionStore

        store = SessionStore()
        store.register_run(
            session_id="session-duplicate-trace-a-001",
            tenant_id="tenant-acme",
            principal_id="user-1",
            trace_id="trace-session-global-duplicate-001",
            status="success",
            user_input="hello",
            output_text="done",
        )

        with pytest.raises(
            ValueError,
            match="Session trace_id already exists: trace-session-global-duplicate-001",
        ):
            store.register_run(
                session_id="session-duplicate-trace-b-001",
                tenant_id="tenant-acme",
                principal_id="user-1",
                trace_id="trace-session-global-duplicate-001",
                status="success",
                user_input="hello in another session",
                output_text="done in another session",
            )

        assert store.get_session("session-duplicate-trace-b-001") is None
        assert len(store.runs_for_session("session-duplicate-trace-a-001")) == 1

    def test_session_store_requires_delegated_authorization_identity(self) -> None:
        from agent_runtime_ref.session import SessionStore

        required_fields = {
            "authorization_mode": {
                "authorization_mode": " ",
            },
            "delegated_principal_id": {
                "authorization_mode": "user_delegated",
                "delegated_principal_id": " ",
                "delegated_scope": "tickets.write",
            },
            "delegated_scope": {
                "authorization_mode": "user_delegated",
                "delegated_principal_id": "user-1",
                "delegated_scope": " ",
            },
        }
        for field, delegated_fields in required_fields.items():
            store = SessionStore()
            with pytest.raises(ValueError, match=f"Session field is required: {field}"):
                store.register_run(
                    session_id="session-delegated-required-001",
                    tenant_id="tenant-acme",
                    principal_id="user-1",
                    trace_id="trace-delegated-required-001",
                    status="success",
                    user_input="hello",
                    output_text="done",
                    **delegated_fields,
                )
            assert store.get_session("session-delegated-required-001") is None

        store = SessionStore()
        with pytest.raises(
            ValueError,
            match="Authorization mode is not supported: magic_token",
        ):
            store.register_run(
                session_id="session-delegated-unknown-authz-001",
                tenant_id="tenant-acme",
                principal_id="user-1",
                trace_id="trace-delegated-unknown-authz-001",
                status="success",
                user_input="hello",
                output_text="done",
                authorization_mode=" magic_token ",
            )
        assert store.get_session("session-delegated-unknown-authz-001") is None

        record = store.register_run(
            session_id="session-delegated-normalized-001",
            tenant_id="tenant-acme",
            principal_id="user-1",
            trace_id="trace-delegated-normalized-001",
            status="success",
            user_input="hello",
            output_text="done",
            capability_session_id=" cap-session-001 ",
            capability_session_status=" pending ",
            authorization_mode=" user_delegated ",
            delegated_principal_id=" user-1 ",
            delegated_scope=" tickets.write ",
        )
        assert record.capability_session_id == "cap-session-001"
        assert record.capability_session_status == "pending"
        assert record.authorization_mode == "user_delegated"
        assert record.delegated_principal_id == "user-1"
        assert record.delegated_scope == "tickets.write"

    def test_session_store_requires_eval_dataset_name(self, tmp_path: Path) -> None:
        from agent_runtime_ref.session import SessionStore

        store = SessionStore()
        store.register_run(
            session_id="session-eval-name-required-001",
            tenant_id="tenant-acme",
            principal_id="user-1",
            trace_id="trace-eval-name-required-001",
            status="success",
            user_input="hello",
            output_text="done",
        )
        with pytest.raises(ValueError, match="Session field is required: dataset_name"):
            store.export_eval_dataset_json(
                ("session-eval-name-required-001",),
                output_path=tmp_path / "eval.json",
                dataset_name=" ",
            )
        assert not (tmp_path / "eval.json").exists()

        output_path = tmp_path / "normalized-eval.json"
        store.export_eval_dataset_json(
            (" session-eval-name-required-001 ",),
            output_path=output_path,
            dataset_name=" eval-seed ",
        )
        payload = json.loads(output_path.read_text(encoding="utf-8"))
        assert payload["dataset_name"] == "eval-seed"
        assert payload["sessions"][0]["session"]["session_id"] == "session-eval-name-required-001"

        output_path = tmp_path / "normalized-eval-spec.json"
        store.export_eval_dataset_json(
            ("session-eval-name-required-001",),
            output_path=output_path,
            dataset_name="eval-seed",
            eval_specs={" session-eval-name-required-001 ": {"labels": ["happy_path"]}},
        )
        payload = json.loads(output_path.read_text(encoding="utf-8"))
        assert payload["sessions"][0]["eval"]["labels"] == ["happy_path"]

    def test_session_store_rejects_duplicate_eval_session_ids(self, tmp_path: Path) -> None:
        from agent_runtime_ref.session import SessionStore

        store = SessionStore()
        store.register_run(
            session_id="session-eval-duplicate-001",
            tenant_id="tenant-acme",
            principal_id="user-1",
            trace_id="trace-eval-duplicate-001",
            status="success",
            user_input="hello",
            output_text="done",
        )
        output_path = tmp_path / "duplicate-eval.json"

        with pytest.raises(
            ValueError,
            match="Session field entries must be unique: session_id",
        ):
            store.export_eval_dataset_json(
                ("session-eval-duplicate-001", " session-eval-duplicate-001 "),
                output_path=output_path,
                dataset_name="eval-seed",
            )
        assert not output_path.exists()
        with pytest.raises(
            ValueError,
            match="Session field entries must be unique: session_id",
        ):
            store.export_eval_dataset_json(
                ("session-eval-duplicate-001",),
                output_path=output_path,
                dataset_name="eval-seed",
                eval_specs={
                    "session-eval-duplicate-001": {"labels": ["happy_path"]},
                    " session-eval-duplicate-001 ": {"labels": ["duplicate"]},
                },
            )

    def test_cli_check_retirement_detects_runtime_control_shutdown_gaps(self, cli_json) -> None:
        exit_code, payload = cli_json(
            [
                "check-retirement",
                "--step",
                "expire_paused_runs=false",
                "--step",
                "stop_background_routes=false",
            ],
        )
        assert exit_code == 0
        assert set(payload) == {
            "system_id",
            "ready",
            "missing_steps",
            "failed_run_archive_targets",
            "replacement_mode",
        }
        assert payload["system_id"] == "support-triage-ref"
        assert not payload["ready"]
        assert payload["missing_steps"] == [
            "expire_paused_runs",
            "stop_background_routes",
        ]
        assert payload["failed_run_archive_targets"] == [
            "telemetry_jsonl",
            "session_exports",
            "approval_history",
        ]
        assert payload["replacement_mode"] == "staged_replacement"

    def test_cli_check_change_accepts_runtime_control_signal_contract(self, cli_json) -> None:
        exit_code, payload = cli_json(
            [
                "check-change",
                "--signal",
                "offline_eval_passed=true",
            ]
        )
        assert exit_code == 0
        assert set(payload) == {
            "change_id",
            "ready",
            "missing_signals",
            "missing_failed_run_signals",
            "rollout_strategy",
            "risk_level",
        }
        assert payload["change_id"] == "chg-2026-04-07-support-runtime"
        assert payload["ready"] is True
        assert payload["missing_signals"] == []
        assert payload["missing_failed_run_signals"] == []
        assert payload["rollout_strategy"] == "staged_canary"
        assert payload["risk_level"] == "high"


class TestMeaningfulMemoryAndLifecycleCoverage:
    def test_memory_store_from_dict_rejects_bad_shapes(self) -> None:
        from agent_runtime_ref.memory import MemoryRecord, MemoryStore

        with pytest.raises(TypeError, match="'memory' must be a mapping"):
            MemoryStore.from_dict({"memory": []})
        with pytest.raises(TypeError, match="'seed_records' must be a list"):
            MemoryStore.from_dict({"memory": {"seed_records": "x"}})
        with pytest.raises(TypeError, match="Memory record #1 must be a mapping"):
            MemoryStore.from_dict({"memory": {"seed_records": ["x"]}})
        with pytest.raises(
            TypeError, match="Memory record #1 field must be a string: tenant_id"
        ):
            MemoryStore.from_dict(
                {
                    "memory": {
                        "seed_records": [
                            {
                                "tenant_id": 7,
                                "memory_class": "profile",
                                "kind": "language_preference",
                                "content": "concise replies",
                                "source": "trusted_profile",
                            }
                        ]
                    }
                }
            )
        with pytest.raises(
            ValueError, match="Memory record #1 field is required: tenant_id"
        ):
            MemoryStore.from_dict(
                {
                    "memory": {
                        "seed_records": [
                            {
                                "memory_class": "profile",
                                "kind": "language_preference",
                                "content": "concise replies",
                                "source": "trusted_profile",
                            }
                        ]
                    }
                }
            )
        with pytest.raises(
            ValueError, match="Memory record #1 field is required: content"
        ):
            MemoryStore.from_dict(
                {
                    "memory": {
                        "seed_records": [
                            {
                                "tenant_id": "tenant-acme",
                                "memory_class": "profile",
                                "kind": "language_preference",
                                "content": " ",
                                "source": "trusted_profile",
                            }
                        ]
                    }
                }
            )
        with pytest.raises(
            TypeError, match="Memory record #1 field must be a string: memory_id"
        ):
            MemoryStore.from_dict(
                {
                    "memory": {
                        "seed_records": [
                            {
                                "memory_id": 7,
                                "tenant_id": "tenant-acme",
                                "memory_class": "profile",
                                "kind": "language_preference",
                                "content": "concise replies",
                                "source": "trusted_profile",
                            }
                        ]
                    }
                }
            )
        with pytest.raises(
            ValueError, match="Memory record #1 field is required: memory_id"
        ):
            MemoryStore.from_dict(
                {
                    "memory": {
                        "seed_records": [
                            {
                                "memory_id": " ",
                                "tenant_id": "tenant-acme",
                                "memory_class": "profile",
                                "kind": "language_preference",
                                "content": "concise replies",
                                "source": "trusted_profile",
                            }
                        ]
                    }
                }
            )
        with pytest.raises(
            TypeError, match="Memory record #1 field must be a string: provenance"
        ):
            MemoryStore.from_dict(
                {
                    "memory": {
                        "seed_records": [
                            {
                                "memory_id": "mem-custom",
                                "tenant_id": "tenant-acme",
                                "memory_class": "profile",
                                "kind": "language_preference",
                                "content": "concise replies",
                                "source": "trusted_profile",
                                "provenance": 7,
                            }
                        ]
                    }
                }
            )
        record = MemoryStore.from_dict(
            {
                "memory": {
                    "seed_records": [
                        {
                            "memory_id": " mem-custom ",
                            "tenant_id": "tenant-acme",
                            "memory_class": "profile",
                            "kind": "language_preference",
                            "content": "concise replies",
                            "source": "trusted_profile",
                        }
                    ]
                }
            }
        ).all()[0]
        assert record.memory_id == "mem-custom"
        for confidence in ("0.9", True):
            with pytest.raises(
                TypeError, match="Memory record #1 confidence must be a number"
            ):
                MemoryStore.from_dict(
                    {
                        "memory": {
                            "seed_records": [
                                {
                                    "tenant_id": "tenant-acme",
                                    "memory_class": "profile",
                                    "kind": "language_preference",
                                    "content": "concise replies",
                                    "source": "trusted_profile",
                                    "confidence": confidence,
                                }
                            ]
                        }
                    }
                )
        for confidence in (2, float("nan"), float("inf")):
            with pytest.raises(
                ValueError, match="Memory record #1 confidence must be between 0 and 1"
            ):
                MemoryStore.from_dict(
                    {
                        "memory": {
                            "seed_records": [
                                {
                                    "tenant_id": "tenant-acme",
                                    "memory_class": "profile",
                                    "kind": "language_preference",
                                    "content": "concise replies",
                                    "source": "trusted_profile",
                                    "confidence": confidence,
                                }
                            ]
                        }
                    }
                )
        for revision in ("2", True):
            with pytest.raises(
                TypeError, match="Memory record #1 revision must be an integer"
            ):
                MemoryStore.from_dict(
                    {
                        "memory": {
                            "seed_records": [
                                {
                                    "tenant_id": "tenant-acme",
                                    "memory_class": "profile",
                                    "kind": "language_preference",
                                    "content": "concise replies",
                                    "source": "trusted_profile",
                                    "revision": revision,
                                }
                            ]
                        }
                    }
                )
        with pytest.raises(
            ValueError, match="Memory record #1 revision must be positive"
        ):
            MemoryStore.from_dict(
                {
                    "memory": {
                        "seed_records": [
                            {
                                "tenant_id": "tenant-acme",
                                "memory_class": "profile",
                                "kind": "language_preference",
                                "content": "concise replies",
                                "source": "trusted_profile",
                                "revision": 0,
                            }
                        ]
                    }
                }
            )

        direct_record = MemoryRecord(
            memory_id=" mem-direct ",
            tenant_id=" tenant-acme ",
            memory_class=" profile ",
            kind=" language_preference ",
            content=" concise replies ",
            source=" trusted_profile ",
            confidence=0.9,
            provenance=" user_confirmed ",
            revision=2,
        )
        assert direct_record.memory_id == "mem-direct"
        assert direct_record.tenant_id == "tenant-acme"
        assert direct_record.provenance == "user_confirmed"
        assert MemoryStore(records=[direct_record]).retrieve(
            "concise", " tenant-acme "
        ) == [direct_record]
        with pytest.raises(TypeError, match="Memory record field must be a string: tenant_id"):
            MemoryRecord(
                memory_id="mem-direct",
                tenant_id=cast(str, 7),
                memory_class="profile",
                kind="language_preference",
                content="concise replies",
                source="trusted_profile",
                confidence=0.9,
            )
        with pytest.raises(ValueError, match="Memory record field is required: tenant_id"):
            MemoryRecord(
                memory_id="mem-direct",
                tenant_id=" ",
                memory_class="profile",
                kind="language_preference",
                content="concise replies",
                source="trusted_profile",
                confidence=0.9,
            )
        with pytest.raises(TypeError, match="Memory record confidence must be a number"):
            MemoryRecord(
                memory_id="mem-direct",
                tenant_id="tenant-acme",
                memory_class="profile",
                kind="language_preference",
                content="concise replies",
                source="trusted_profile",
                confidence=cast(float, "0.9"),
            )
        with pytest.raises(ValueError, match="Memory record confidence must be between 0 and 1"):
            MemoryRecord(
                memory_id="mem-direct",
                tenant_id="tenant-acme",
                memory_class="profile",
                kind="language_preference",
                content="concise replies",
                source="trusted_profile",
                confidence=2,
            )
        with pytest.raises(TypeError, match="Memory record revision must be an integer"):
            MemoryRecord(
                memory_id="mem-direct",
                tenant_id="tenant-acme",
                memory_class="profile",
                kind="language_preference",
                content="concise replies",
                source="trusted_profile",
                confidence=0.9,
                revision=True,
            )

    def test_memory_store_replace_revision_increments_prior_version(self) -> None:
        from agent_runtime_ref.memory import MemoryCandidate, MemoryStore

        store = MemoryStore()
        first = store.persist(
            MemoryCandidate(
                tenant_id="tenant-acme",
                memory_class="long_term",
                kind="validated_fact",
                content="First version",
                source="trusted_service",
                confidence=0.9,
                provenance="policy_review",
                revision_mode=" replace ",
            ),
        )
        second = store.persist(
            MemoryCandidate(
                tenant_id="tenant-acme",
                memory_class="long_term",
                kind="validated_fact",
                content="Second version",
                source="trusted_service",
                confidence=0.95,
                provenance="policy_review",
                revision_mode="replace",
            ),
        )
        assert first.revision >= 2
        assert second.revision == first.revision + 1

    def test_memory_store_rejects_unsupported_candidate_revision_modes(self) -> None:
        from agent_runtime_ref.memory import MemoryCandidate, MemoryStore

        store = MemoryStore()
        with pytest.raises(
            ValueError,
            match="Memory candidate revision mode is not supported: repalce",
        ):
            store.persist(
                MemoryCandidate(
                    tenant_id="tenant-acme",
                    memory_class="long_term",
                    kind="validated_fact",
                    content="Second version",
                    source="trusted_service",
                    confidence=0.95,
                    provenance="policy_review",
                    revision_mode="repalce",
                ),
            )
        with pytest.raises(
            TypeError,
            match="Memory candidate revision mode must be a string",
        ):
            store.persist(
                MemoryCandidate(
                    tenant_id="tenant-acme",
                    memory_class="long_term",
                    kind="validated_fact",
                    content="Second version",
                    source="trusted_service",
                    confidence=0.95,
                    provenance="policy_review",
                    revision_mode=cast(str, ["replace"]),
                ),
            )

    def test_memory_store_rejects_bad_candidate_confidence(self) -> None:
        from agent_runtime_ref.memory import MemoryCandidate, MemoryStore

        for confidence in (-0.1, 1.1, float("nan"), float("inf")):
            store = MemoryStore()
            with pytest.raises(
                ValueError,
                match="Memory candidate confidence must be between 0 and 1",
            ):
                store.persist(
                    MemoryCandidate(
                        tenant_id="tenant-acme",
                        memory_class="long_term",
                        kind="validated_fact",
                        content="Candidate version",
                        source="trusted_service",
                        confidence=confidence,
                        provenance="policy_review",
                    ),
                )
        for confidence in (True, "0.9"):
            store = MemoryStore()
            with pytest.raises(
                TypeError,
                match="Memory candidate confidence must be a number",
            ):
                store.persist(
                    MemoryCandidate(
                        tenant_id="tenant-acme",
                        memory_class="long_term",
                        kind="validated_fact",
                        content="Candidate version",
                        source="trusted_service",
                        confidence=cast(float, confidence),
                        provenance="policy_review",
                    ),
                )

    def test_memory_store_requires_candidate_lineage_fields(self) -> None:
        from agent_runtime_ref.memory import MemoryCandidate, MemoryStore

        def candidate_with(**overrides: str) -> MemoryCandidate:
            values = {
                "tenant_id": "tenant-acme",
                "memory_class": "long_term",
                "kind": "validated_fact",
                "content": "Candidate version",
                "source": "trusted_service",
                "provenance": "policy_review",
            } | overrides
            return MemoryCandidate(
                tenant_id=values["tenant_id"],
                memory_class=values["memory_class"],
                kind=values["kind"],
                content=values["content"],
                source=values["source"],
                confidence=0.9,
                provenance=values["provenance"],
            )

        for field in ("tenant_id", "memory_class", "kind", "content", "source", "provenance"):
            store = MemoryStore()
            with pytest.raises(
                TypeError,
                match=f"Memory candidate field must be a string: {field}",
            ):
                store.persist(candidate_with(**{field: cast(str, 7)}))
            with pytest.raises(
                ValueError,
                match=f"Memory candidate field is required: {field}",
            ):
                store.persist(candidate_with(**{field: " "}))

        store = MemoryStore()
        record = store.persist(
            MemoryCandidate(
                tenant_id=" tenant-acme ",
                memory_class=" long_term ",
                kind=" validated_fact ",
                content=" Candidate version ",
                source=" trusted_service ",
                confidence=0.9,
                provenance=" policy_review ",
                revision_mode=" replace ",
            ),
        )
        assert record.tenant_id == "tenant-acme"
        assert record.memory_class == "long_term"
        assert record.kind == "validated_fact"
        assert record.content == "Candidate version"
        assert record.source == "trusted_service"
        assert record.provenance == "policy_review"

    def test_memory_store_compaction_is_tenant_scoped(self) -> None:
        from agent_runtime_ref.memory import MemoryCandidate, MemoryStore

        store = MemoryStore()
        store.persist(
            MemoryCandidate(
                tenant_id="tenant-acme",
                memory_class="short_term",
                kind="working_note",
                content="Duplicate note",
                source="session_state",
                confidence=0.5,
                provenance="demo",
            ),
        )
        store.persist(
            MemoryCandidate(
                tenant_id="tenant-acme",
                memory_class="short_term",
                kind="working_note",
                content="Duplicate note",
                source="session_state",
                confidence=0.5,
                provenance="demo",
            ),
        )
        store.persist(
            MemoryCandidate(
                tenant_id="tenant-other",
                memory_class="short_term",
                kind="working_note",
                content="Duplicate note",
                source="session_state",
                confidence=0.5,
                provenance="demo",
            ),
        )
        removed = store.compact(" tenant-acme ")
        assert removed >= 1
        remaining_other = [record for record in store.all() if record.tenant_id == "tenant-other"]
        assert len(remaining_other) == 1

    def test_memory_score_prefers_trusted_profile_signal(self) -> None:
        from agent_runtime_ref.memory import MemoryRecord, MemoryStore

        low = MemoryRecord(
            memory_id="mem-low",
            tenant_id="tenant-acme",
            memory_class="short_term",
            kind="note",
            content="language preference maybe english",
            source="session_state",
            confidence=0.4,
        )
        high = MemoryRecord(
            memory_id="mem-high",
            tenant_id="tenant-acme",
            memory_class="profile",
            kind="language_preference",
            content="language preference concise english",
            source="trusted_profile",
            confidence=0.9,
        )
        assert MemoryStore._score(high, {"language", "preference"}) > MemoryStore._score(
            low, {"language", "preference"}
        )

    def test_lifecycle_helpers_reject_bad_shapes(self) -> None:
        from agent_runtime_ref.lifecycle import ArtifactBundle, ChangeRecord, RetirementPlan

        with pytest.raises(TypeError, match="change config must be a mapping"):
            ChangeRecord.from_dict({"change": []})
        with pytest.raises(TypeError, match="change config keys must be strings"):
            ChangeRecord.from_dict({"change": {7: "malformed"}})
        with pytest.raises(TypeError, match="artifact bundle config must be a mapping"):
            ArtifactBundle.from_dict({"bundle": []})
        with pytest.raises(TypeError, match="retirement config must be a mapping"):
            RetirementPlan.from_dict({"retirement": []})
        valid_change = {
            "change_id": "x",
            "change_type": "y",
            "risk_level": "z",
            "rollout_strategy": "gradual",
            "session_control_owner": "support-ops",
            "emergency_freeze_owner": "platform-runtime",
        }
        with pytest.raises(TypeError, match="artifacts must be a list"):
            ChangeRecord.from_dict(
                {
                    "change": {
                        **valid_change,
                        "artifacts": "bad",
                        "required_signals": [],
                        "approval_roles": [],
                    }
                }
            )
        with pytest.raises(TypeError, match="change.change_id must be a string"):
            ChangeRecord.from_dict({"change": {**valid_change, "change_id": 7}})
        with pytest.raises(ValueError, match="change.change_id is required"):
            ChangeRecord.from_dict(
                {
                    "change": {
                        "change_type": "y",
                        "risk_level": "z",
                        "rollout_strategy": "gradual",
                    }
                }
            )
        with pytest.raises(TypeError, match="required_signals entries must be strings"):
            ChangeRecord.from_dict(
                {
                    "change": {
                        **valid_change,
                        "required_signals": [7],
                    }
                }
            )
        with pytest.raises(ValueError, match="required_signals entries must not be empty"):
            ChangeRecord.from_dict(
                {
                    "change": {
                        **valid_change,
                        "required_signals": [" "],
                    }
                }
            )
        with pytest.raises(ValueError, match="required_signals entries must be unique"):
            ChangeRecord.from_dict(
                {
                    "change": {
                        **valid_change,
                        "required_signals": ["offline_eval", " offline_eval "],
                    }
                }
            )
        with pytest.raises(ValueError, match="change.session_control_owner is required"):
            ChangeRecord.from_dict(
                {
                    "change": {
                        **valid_change,
                        "session_control_owner": " ",
                    }
                }
            )
        with pytest.raises(ValueError, match="change.emergency_freeze_owner is required"):
            ChangeRecord.from_dict(
                {
                    "change": {
                        **valid_change,
                        "emergency_freeze_owner": " ",
                    }
                }
            )
        valid_bundle = {
            "bundle_name": "bundle",
            "version": "1",
            "session_control_owner": "support-ops",
        }
        with pytest.raises(TypeError, match="bundle.bundle_name must be a string"):
            ArtifactBundle.from_dict({"bundle": {**valid_bundle, "bundle_name": 7}})
        with pytest.raises(ValueError, match="bundle.bundle_name is required"):
            ArtifactBundle.from_dict({"bundle": {"version": "1"}})
        with pytest.raises(TypeError, match="'bundle.provenance_required' must be a boolean"):
            ArtifactBundle.from_dict(
                {
                    "bundle": {
                        **valid_bundle,
                        "provenance_required": "false",
                    }
                }
            )
        with pytest.raises(TypeError, match="'bundle.signed' must be a boolean"):
            ArtifactBundle.from_dict(
                {"bundle": {**valid_bundle, "signed": "false"}}
            )
        with pytest.raises(ValueError, match="bundle.session_control_owner is required"):
            ArtifactBundle.from_dict(
                {"bundle": {**valid_bundle, "session_control_owner": " "}}
            )
        bundle = ArtifactBundle.from_dict({"bundle": {**valid_bundle, "signed": True}})
        assert bundle.provenance_required is True
        assert bundle.signed is True
        with pytest.raises(TypeError, match="artifacts entries must be strings"):
            ArtifactBundle.from_dict(
                {"bundle": {**valid_bundle, "artifacts": [7]}}
            )
        with pytest.raises(ValueError, match="artifacts entries must not be empty"):
            ArtifactBundle.from_dict(
                {"bundle": {**valid_bundle, "artifacts": [""]}}
            )
        valid_retirement = {
            "system_id": "legacy",
            "replacement_mode": "none",
            "session_control_owner": "support-ops",
            "emergency_freeze_owner": "platform-runtime",
        }
        with pytest.raises(TypeError, match="retirement.system_id must be a string"):
            RetirementPlan.from_dict({"retirement": {**valid_retirement, "system_id": 7}})
        with pytest.raises(ValueError, match="retirement.system_id is required"):
            RetirementPlan.from_dict({"retirement": {"replacement_mode": "none"}})
        with pytest.raises(ValueError, match="retirement.session_control_owner is required"):
            RetirementPlan.from_dict(
                {"retirement": {**valid_retirement, "session_control_owner": " "}}
            )
        with pytest.raises(ValueError, match="retirement.emergency_freeze_owner is required"):
            RetirementPlan.from_dict(
                {"retirement": {**valid_retirement, "emergency_freeze_owner": " "}}
            )
        with pytest.raises(TypeError, match="archive_targets entries must be strings"):
            RetirementPlan.from_dict(
                {
                    "retirement": {
                        **valid_retirement,
                        "archive_targets": [7],
                    }
                }
            )
        with pytest.raises(ValueError, match="archive_targets entries must not be empty"):
            RetirementPlan.from_dict(
                {
                    "retirement": {
                        **valid_retirement,
                        "archive_targets": [" "],
                    }
                }
            )
        with pytest.raises(ValueError, match="archive_targets entries must be unique"):
            RetirementPlan.from_dict(
                {
                    "retirement": {
                        **valid_retirement,
                        "archive_targets": ["telemetry_jsonl", " telemetry_jsonl "],
                    }
                }
            )

        direct_change = ChangeRecord(
            change_id=" change-001 ",
            change_type=" rollout ",
            risk_level=" medium ",
            rollout_strategy=" gradual ",
            artifacts=(" runtime.py ",),
            affected_surfaces=(" cli ",),
            required_signals=(" offline_eval_passed ",),
            approval_roles=(" approver ",),
            session_control_owner=" support-ops ",
            emergency_freeze_owner=" platform-runtime ",
        )
        assert direct_change.change_id == "change-001"
        assert direct_change.session_control_owner == "support-ops"
        assert direct_change.required_signals == ("offline_eval_passed",)
        direct_bundle = ArtifactBundle(
            bundle_name=" bundle ",
            version=" 1 ",
            provenance_required=True,
            signed=False,
            session_control_owner=" support-ops ",
            artifacts=(" runtime.py ",),
            review_evidence={" sandbox_profile_reviewed ": True},
        )
        assert direct_bundle.bundle_name == "bundle"
        assert direct_bundle.session_control_owner == "support-ops"
        assert direct_bundle.artifacts == ("runtime.py",)
        assert " sandbox_profile_reviewed " in direct_bundle.review_evidence
        direct_plan = RetirementPlan(
            system_id=" legacy-system ",
            replacement_mode=" none ",
            triggers=(" inactivity_window ",),
            required_steps=(" revoke_egress ",),
            session_control_owner=" support-ops ",
            emergency_freeze_owner=" platform-runtime ",
            archive_targets=(" telemetry_jsonl ",),
        )
        assert direct_plan.system_id == "legacy-system"
        assert direct_plan.session_control_owner == "support-ops"
        assert direct_plan.required_steps == ("revoke_egress",)
        with pytest.raises(TypeError, match="change.change_id must be a string"):
            ChangeRecord(
                **{**valid_change, "change_id": cast(str, 7)},
                artifacts=(),
                affected_surfaces=(),
                required_signals=(),
                approval_roles=(),
            )
        with pytest.raises(ValueError, match="change.change_id is required"):
            ChangeRecord(
                **{**valid_change, "change_id": " "},
                artifacts=(),
                affected_surfaces=(),
                required_signals=(),
                approval_roles=(),
            )
        with pytest.raises(TypeError, match="'bundle.signed' must be a boolean"):
            ArtifactBundle(
                **valid_bundle,
                provenance_required=True,
                signed=cast(bool, "false"),
                artifacts=(),
                review_evidence={},
            )
        with pytest.raises(
            TypeError,
            match="artifact bundle review_evidence config must be a mapping",
        ):
            ArtifactBundle(
                **valid_bundle,
                provenance_required=True,
                signed=False,
                artifacts=(),
                review_evidence=cast(dict[str, object], []),
            )
        with pytest.raises(
            TypeError,
            match="artifact bundle review_evidence config keys must be strings",
        ):
            ArtifactBundle(
                **valid_bundle,
                provenance_required=True,
                signed=False,
                artifacts=(),
                review_evidence=cast(dict[str, object], {7: True}),
            )
        with pytest.raises(ValueError, match="retirement.system_id is required"):
            RetirementPlan(
                **{**valid_retirement, "system_id": " "},
                triggers=(),
                required_steps=(),
                archive_targets=(),
            )
        with pytest.raises(TypeError, match="required_signals entries must be strings"):
            ChangeRecord(
                **valid_change,
                artifacts=(),
                affected_surfaces=(),
                required_signals=cast(tuple[str, ...], (7,)),
                approval_roles=(),
            )
        with pytest.raises(ValueError, match="required_signals entries must be unique"):
            ChangeRecord(
                **valid_change,
                artifacts=(),
                affected_surfaces=(),
                required_signals=("offline_eval", " offline_eval "),
                approval_roles=(),
            )

    def test_lifecycle_assessments_report_ready_when_complete(self, config_dir: Path) -> None:
        from agent_runtime_ref.config import load_change_record, load_retirement_plan

        change = load_change_record(config_dir / "change.yaml")
        change = type(change)(
            change_id=change.change_id,
            change_type=change.change_type,
            risk_level=change.risk_level,
            rollout_strategy=change.rollout_strategy,
            artifacts=change.artifacts,
            affected_surfaces=change.affected_surfaces,
            required_signals=tuple(f" {signal} " for signal in change.required_signals),
            approval_roles=change.approval_roles,
            session_control_owner=change.session_control_owner,
            emergency_freeze_owner=change.emergency_freeze_owner,
        )
        change_assessment = assess_change_gate(
            change,
            {f" {signal} ": True for signal in change.required_signals},
        )
        assert change_assessment.ready
        assert change_assessment.missing_signals == ()

        plan = load_retirement_plan(config_dir / "retirement.yaml")
        plan = type(plan)(
            system_id=plan.system_id,
            replacement_mode=plan.replacement_mode,
            triggers=plan.triggers,
            required_steps=tuple(f" {step} " for step in plan.required_steps),
            session_control_owner=plan.session_control_owner,
            emergency_freeze_owner=plan.emergency_freeze_owner,
            archive_targets=plan.archive_targets,
        )
        retirement_assessment = assess_retirement(
            plan,
            {f" {step} ": True for step in plan.required_steps},
        )
        assert retirement_assessment.ready
        assert retirement_assessment.missing_steps == ()

        with pytest.raises(TypeError, match="Assessment signal key must be a string"):
            assess_change_gate(change, cast(dict[str, bool], {1: True}))
        with pytest.raises(ValueError, match="Assessment signal key must not be empty"):
            assess_change_gate(change, {" ": True})
        with pytest.raises(ValueError, match="Assessment signal keys must be unique"):
            assess_change_gate(
                change,
                {" offline_eval_passed ": True, "offline_eval_passed": True},
            )
        with pytest.raises(
            TypeError,
            match="Assessment signal value must be a boolean: offline_eval_passed",
        ):
            assess_change_gate(
                change,
                cast(dict[str, bool], {"offline_eval_passed": "false"}),
            )
        with pytest.raises(
            TypeError,
            match="Assessment signal value must be a boolean: revoke_egress",
        ):
            assess_retirement(plan, cast(dict[str, bool], {"revoke_egress": "false"}))

    def test_change_gate_can_block_on_missing_failed_run_drill(self, config_dir: Path) -> None:
        from agent_runtime_ref.config import load_change_record

        change = load_change_record(config_dir / "change.yaml")
        observed = {signal: True for signal in change.required_signals}
        observed["failed_run_drill_checked"] = False
        assessment = assess_change_gate(change, observed)
        assert not assessment.ready
        assert assessment.missing_signals == ("failed_run_drill_checked",)


class TestLowCoverageModuleBranches:
    def test_controls_policy_from_dict_rejects_bad_shapes(self) -> None:
        from agent_runtime_ref.controls import ControlsPolicy

        with pytest.raises(TypeError, match="'controls' must be a mapping"):
            ControlsPolicy.from_dict({"controls": []})
        with pytest.raises(TypeError, match="'controls.require' must be a list"):
            ControlsPolicy.from_dict({"controls": {"require": "x"}})
        with pytest.raises(TypeError, match="'controls.block_if' must be a list"):
            ControlsPolicy.from_dict({"controls": {"require": [], "block_if": "x"}})
        with pytest.raises(TypeError, match="controls.require entries must be strings"):
            ControlsPolicy.from_dict({"controls": {"require": [7]}})
        with pytest.raises(TypeError, match="controls.block_if entries must be strings"):
            ControlsPolicy.from_dict({"controls": {"require": [], "block_if": [7]}})
        with pytest.raises(ValueError, match="controls.require entries must not be empty"):
            ControlsPolicy.from_dict({"controls": {"require": [" "]}})
        with pytest.raises(ValueError, match="controls.block_if entries must not be empty"):
            ControlsPolicy.from_dict({"controls": {"require": [], "block_if": [""]}})
        with pytest.raises(ValueError, match="controls.require entries must be unique"):
            ControlsPolicy.from_dict(
                {"controls": {"require": ["registry_reviewed", " registry_reviewed "]}}
            )
        with pytest.raises(ValueError, match="controls.block_if entries must be unique"):
            ControlsPolicy.from_dict(
                {"controls": {"require": [], "block_if": ["finding", " finding "]}}
            )

        policy = ControlsPolicy(
            required_controls=(" registry_reviewed ",),
            blocked_findings=(" manual_override ",),
        )
        assert policy.required_controls == ("registry_reviewed",)
        assert policy.blocked_findings == ("manual_override",)
        with pytest.raises(TypeError, match="controls.require entries must be strings"):
            ControlsPolicy(
                required_controls=cast(tuple[str, ...], (7,)),
                blocked_findings=(),
            )
        with pytest.raises(ValueError, match="controls.require entries must be unique"):
            ControlsPolicy(
                required_controls=("registry_reviewed", " registry_reviewed "),
                blocked_findings=(),
            )

    def test_assess_controls_marks_inventory_drift_as_blocking(self) -> None:
        from agent_runtime_ref.controls import ControlsPolicy, InventoryDrift, assess_controls

        assessment = assess_controls(
            ControlsPolicy(
                required_controls=(" registry_reviewed ",),
                blocked_findings=(" manual_override ",),
            ),
            {"registry_reviewed": True, "manual_override": False},
            inventory_drift=InventoryDrift(
                missing_from_catalog=("ghost_cap",),
                missing_from_inventory=(),
            ),
        )
        assert not assessment.healthy
        assert "inventory_drift_present" in assessment.blocking_findings

    def test_structured_event_rejects_direct_bad_identity_fields(self) -> None:
        from agent_runtime_ref.telemetry import StructuredEvent

        with pytest.raises(
            TypeError,
            match="Telemetry event field must be a string: event_type",
        ):
            StructuredEvent(
                event_type=cast(str, 7),
                trace_id="trace-direct",
                payload={},
            )
        with pytest.raises(
            ValueError,
            match="Telemetry event field must not be empty: event_type",
        ):
            StructuredEvent(event_type=" ", trace_id="trace-direct", payload={})
        with pytest.raises(
            ValueError,
            match="Telemetry event field must not be empty: trace_id",
        ):
            StructuredEvent(event_type="run_start", trace_id=" ", payload={})
        with pytest.raises(
            ValueError,
            match="Telemetry schema version is not supported: 2.0",
        ):
            StructuredEvent(
                event_type="run_start",
                trace_id="trace-direct",
                payload={},
                schema_version="2.0",
            )

        event = StructuredEvent(
            event_type=" run_start ",
            trace_id=" trace-direct ",
            payload={},
            schema_version=" 1.0 ",
        )
        assert event.event_type == "run_start"
        assert event.trace_id == "trace-direct"
        assert event.schema_version == "1.0"

    def test_structured_event_rejects_direct_bad_payload_shapes(self) -> None:
        from agent_runtime_ref.telemetry import StructuredEvent

        bad_payload = cast(dict[str, str], [])
        bad_redacted_fields = cast(tuple[str, ...], "user_input")
        payload = cast(dict[str, str], {"count": 1})
        bad_payload_key = cast(dict[str, str], {1: "count"})
        with pytest.raises(TypeError, match="Telemetry event payload must be a mapping"):
            StructuredEvent(
                event_type="run_start", trace_id="trace-direct", payload=bad_payload
            )
        with pytest.raises(TypeError, match="Telemetry event redacted_fields must be a tuple"):
            StructuredEvent(
                event_type="run_start",
                trace_id="trace-direct",
                payload={},
                redacted_fields=bad_redacted_fields,
            )

        with pytest.raises(
            TypeError,
            match="Telemetry event payload key must be a string",
        ):
            StructuredEvent(
                event_type="run_start",
                trace_id="trace-direct",
                payload=bad_payload_key,
            )
        with pytest.raises(
            ValueError,
            match="Telemetry event payload key must not be empty",
        ):
            StructuredEvent(
                event_type="run_start",
                trace_id="trace-direct",
                payload={" ": "count"},
            )
        with pytest.raises(
            ValueError,
            match="Telemetry event payload keys must be unique",
        ):
            StructuredEvent(
                event_type="run_start",
                trace_id="trace-direct",
                payload={" count ": "1", "count": "2"},
            )
        with pytest.raises(
            TypeError,
            match="Telemetry event payload value must be a string: count",
        ):
            StructuredEvent(
                event_type="run_start",
                trace_id="trace-direct",
                payload=payload,
                redacted_fields=("count",),
            )
        with pytest.raises(TypeError, match="redacted_fields entries must be strings"):
            StructuredEvent(
                event_type="run_start",
                trace_id="trace-direct",
                payload={},
                redacted_fields=cast(tuple[str, ...], (1,)),
            )

        event = StructuredEvent(
            event_type="run_start",
            trace_id="trace-direct",
            payload={"count": "1"},
            redacted_fields=("count",),
        )
        assert event.payload == {"count": "1"}
        assert event.redacted_fields == ("count",)
        normalized_event = StructuredEvent(
            event_type="run_start",
            trace_id="trace-direct",
            payload={" count ": "1"},
            redacted_fields=(" count ",),
        )
        assert normalized_event.payload == {"count": "1"}
        assert normalized_event.redacted_fields == ("count",)

    def test_structured_event_from_dict_rejects_bad_shapes(self) -> None:
        from agent_runtime_ref.telemetry import StructuredEvent

        with pytest.raises(
            TypeError,
            match="Telemetry event field must be a string: event_type",
        ):
            StructuredEvent.from_dict({"event_type": 7, "trace_id": "t", "payload": {}})
        with pytest.raises(
            TypeError,
            match="Telemetry event field must be a string: schema_version",
        ):
            StructuredEvent.from_dict(
                {"event_type": "x", "trace_id": "t", "schema_version": 1, "payload": {}}
            )
        with pytest.raises(TypeError, match="payload must be a mapping"):
            StructuredEvent.from_dict({"event_type": "x", "trace_id": "t", "payload": []})
        with pytest.raises(TypeError, match="redacted_fields must be a list"):
            StructuredEvent.from_dict(
                {"event_type": "x", "trace_id": "t", "payload": {}, "redacted_fields": "x"}
            )
        with pytest.raises(TypeError, match="redacted_fields entries must be strings"):
            StructuredEvent.from_dict(
                {"event_type": "x", "trace_id": "t", "payload": {}, "redacted_fields": [1]}
            )
        with pytest.raises(ValueError, match="Telemetry event payload key must not be empty"):
            StructuredEvent.from_dict(
                {"event_type": "x", "trace_id": "t", "payload": {" ": "1"}}
            )
        normalized = StructuredEvent.from_dict(
            {"event_type": "x", "trace_id": "t", "payload": {" count ": "1"}}
        )
        assert normalized.payload == {"count": "1"}

    def test_telemetry_events_for_trace_and_unredacted_export(self, tmp_path: Path) -> None:
        from agent_runtime_ref.telemetry import TelemetryEmitter

        emitter = TelemetryEmitter()
        emitter.emit("run_start", "trace-a", user_input="hello")
        emitter.emit("run_complete", "trace-b", status="success")
        events = emitter.events_for_trace(" trace-a ")
        assert len(events) == 1
        assert events[0].trace_id == "trace-a"
        with pytest.raises(TypeError, match="Telemetry event field must be a string: trace_id"):
            emitter.events_for_trace(cast(str, 7))
        with pytest.raises(
            ValueError,
            match="Telemetry event field must not be empty: trace_id",
        ):
            emitter.events_for_trace(" ")

        output_path = tmp_path / "events.jsonl"
        emitter.export_jsonl(output_path)
        loaded = TelemetryEmitter.load_jsonl(output_path)
        assert len(loaded) == 2
        assert loaded[0].payload["user_input"] == "hello"

    def test_telemetry_export_normalizes_redact_fields(self, tmp_path: Path) -> None:
        from agent_runtime_ref.telemetry import REDACTED_VALUE, TelemetryEmitter

        emitter = TelemetryEmitter()
        emitter.emit("run_start", "trace-a", user_input="hello", tenant_id="tenant-acme")
        output_path = tmp_path / "redacted-events.jsonl"
        emitter.export_jsonl(output_path, redact_fields=(" user_input ", "user_input"))

        loaded = TelemetryEmitter.load_jsonl(output_path)
        assert loaded[0].payload["user_input"] == REDACTED_VALUE
        assert loaded[0].payload["tenant_id"] == "tenant-acme"
        assert loaded[0].redacted_fields == ("user_input",)

    def test_telemetry_export_rejects_empty_redact_fields(self, tmp_path: Path) -> None:
        from agent_runtime_ref.telemetry import TelemetryEmitter

        emitter = TelemetryEmitter()
        emitter.emit("run_start", "trace-a", user_input="hello")
        with pytest.raises(TypeError, match="redacted_fields entries must be strings"):
            emitter.export_jsonl(
                tmp_path / "events.jsonl",
                redact_fields=cast(tuple[str, ...], (1,)),
            )
        with pytest.raises(ValueError, match="Telemetry redact field must not be empty"):
            emitter.export_jsonl(tmp_path / "events.jsonl", redact_fields=(" ",))

    def test_traced_call_emits_failure_span(self) -> None:
        from agent_runtime_ref.telemetry import TelemetryEmitter

        emitter = TelemetryEmitter()
        with pytest.raises(RuntimeError, match="boom"):
            emitter.traced_call(
                "trace-fail", "failing_span", lambda: (_ for _ in ()).throw(RuntimeError("boom"))
            )
        span = emitter.events[-1]
        assert span.event_type == "span"
        assert span.payload["status"] == "failure"

    def test_rollout_policy_from_dict_rejects_bad_shapes(self) -> None:
        from agent_runtime_ref.rollout import RolloutPolicy

        with pytest.raises(TypeError, match="'rollout' must be a mapping"):
            RolloutPolicy.from_dict({"rollout": []})
        with pytest.raises(TypeError, match="'require' must be a list"):
            RolloutPolicy.from_dict({"rollout": {"require": "x"}})
        with pytest.raises(TypeError, match="'block_if' must be a list"):
            RolloutPolicy.from_dict({"rollout": {"require": [], "block_if": "x"}})
        with pytest.raises(TypeError, match="'rollout_mode' must be a mapping"):
            RolloutPolicy.from_dict(
                {"rollout": {"require": [], "block_if": [], "rollout_mode": []}}
            )
        with pytest.raises(TypeError, match="rollout.require entries must be strings"):
            RolloutPolicy.from_dict({"rollout": {"require": [7]}})
        with pytest.raises(TypeError, match="rollout.block_if entries must be strings"):
            RolloutPolicy.from_dict({"rollout": {"require": [], "block_if": [7]}})
        with pytest.raises(ValueError, match="rollout.require entries must not be empty"):
            RolloutPolicy.from_dict({"rollout": {"require": [" "]}})
        with pytest.raises(ValueError, match="rollout.block_if entries must not be empty"):
            RolloutPolicy.from_dict({"rollout": {"require": [], "block_if": [""]}})
        with pytest.raises(ValueError, match="rollout.require entries must be unique"):
            RolloutPolicy.from_dict(
                {"rollout": {"require": ["trace_coverage", " trace_coverage "]}}
            )
        with pytest.raises(ValueError, match="rollout.block_if entries must be unique"):
            RolloutPolicy.from_dict(
                {"rollout": {"require": [], "block_if": ["finding", " finding "]}}
            )
        with pytest.raises(TypeError, match="rollout.rollout_mode keys must be strings"):
            RolloutPolicy.from_dict(
                {"rollout": {"require": [], "block_if": [], "rollout_mode": {1: "canary"}}}
            )
        with pytest.raises(ValueError, match="rollout.rollout_mode entries must not be empty"):
            RolloutPolicy.from_dict(
                {"rollout": {"require": [], "block_if": [], "rollout_mode": {" ": "canary"}}}
            )
        with pytest.raises(ValueError, match="rollout.rollout_mode entries must not be empty"):
            RolloutPolicy.from_dict(
                {"rollout": {"require": [], "block_if": [], "rollout_mode": {"initial": " "}}}
            )
        with pytest.raises(ValueError, match="rollout.rollout_mode entries must be unique"):
            RolloutPolicy.from_dict(
                {
                    "rollout": {
                        "require": [],
                        "block_if": [],
                        "rollout_mode": {" initial ": "canary", "initial": "shadow"},
                    }
                }
            )
        assert RolloutPolicy.from_dict(
            {
                "rollout": {
                    "require": [],
                    "block_if": [],
                    "rollout_mode": {" initial ": " canary "},
                }
            }
        ).rollout_mode == {"initial": "canary"}

        policy = RolloutPolicy(
            required_checks=(" trace_coverage ",),
            blocked_checks=(" direct_tool_access_present ",),
            rollout_mode={" initial ": " canary "},
        )
        assert policy.required_checks == ("trace_coverage",)
        assert policy.blocked_checks == ("direct_tool_access_present",)
        assert policy.rollout_mode == {"initial": "canary"}
        with pytest.raises(TypeError, match="rollout.require entries must be strings"):
            RolloutPolicy(
                required_checks=cast(tuple[str, ...], (7,)),
                blocked_checks=(),
                rollout_mode={},
            )
        with pytest.raises(ValueError, match="rollout.require entries must be unique"):
            RolloutPolicy(
                required_checks=("trace_coverage", " trace_coverage "),
                blocked_checks=(),
                rollout_mode={},
            )
        with pytest.raises(ValueError, match="rollout.rollout_mode entries must be unique"):
            RolloutPolicy(
                required_checks=(),
                blocked_checks=(),
                rollout_mode={" initial ": "canary", "initial": "shadow"},
            )

    def test_ready_for_rollout_false_when_flags_missing(self) -> None:
        assert not ready_for_rollout(
            RolloutReadiness(
                trace_coverage=True,
                offline_eval_pass=True,
                slo_defined=False,
                rollback_plan=True,
            ),
        )
        with pytest.raises(
            TypeError,
            match="Rollout readiness flag must be a boolean: slo_defined",
        ):
            ready_for_rollout(
                RolloutReadiness(
                    trace_coverage=True,
                    offline_eval_pass=True,
                    slo_defined=cast(bool, "false"),
                    rollback_plan=True,
                ),
            )

    def test_approval_policy_rejects_bad_shapes(self) -> None:
        from agent_runtime_ref.approvals import ApprovalPolicy

        with pytest.raises(TypeError, match="'approvals' must be a mapping"):
            ApprovalPolicy.from_dict({"approvals": []})
        with pytest.raises(TypeError, match="approvals.default_reviewer must be a string"):
            ApprovalPolicy.from_dict({"approvals": {"default_reviewer": 7}})
        with pytest.raises(ValueError, match="approvals.default_reviewer is required"):
            ApprovalPolicy.from_dict({"approvals": {"default_reviewer": " "}})
        for escalation_sla_minutes in ("30", True):
            with pytest.raises(
                TypeError,
                match="approvals.escalation_sla_minutes must be an integer",
            ):
                ApprovalPolicy.from_dict(
                    {"approvals": {"escalation_sla_minutes": escalation_sla_minutes}}
                )
        with pytest.raises(
            ValueError, match="approvals.escalation_sla_minutes must be positive"
        ):
            ApprovalPolicy.from_dict({"approvals": {"escalation_sla_minutes": 0}})

        assert ApprovalPolicy(
            default_reviewer=" manager ",
            escalation_sla_minutes=30,
        ).default_reviewer == "manager"
        with pytest.raises(TypeError, match="approvals.default_reviewer must be a string"):
            ApprovalPolicy(default_reviewer=cast(str, 7), escalation_sla_minutes=30)
        with pytest.raises(ValueError, match="approvals.default_reviewer is required"):
            ApprovalPolicy(default_reviewer=" ", escalation_sla_minutes=30)
        with pytest.raises(
            TypeError,
            match="approvals.escalation_sla_minutes must be an integer",
        ):
            ApprovalPolicy(default_reviewer="manager", escalation_sla_minutes=True)
        with pytest.raises(
            ValueError,
            match="approvals.escalation_sla_minutes must be positive",
        ):
            ApprovalPolicy(default_reviewer="manager", escalation_sla_minutes=0)

    def test_catalog_loader_rejects_bad_shapes(self) -> None:
        from agent_runtime_ref.catalog import CapabilityCatalog, CapabilitySpec

        with pytest.raises(TypeError, match="'capabilities' must be a mapping"):
            CapabilityCatalog.from_dict({"capabilities": []})
        with pytest.raises(TypeError, match="Capability names must be strings"):
            CapabilityCatalog.from_dict({"capabilities": {7: {}}})
        with pytest.raises(ValueError, match="Capability name must not be empty"):
            CapabilityCatalog.from_dict({"capabilities": {" ": {}}})
        with pytest.raises(TypeError, match="Capability spec for 'search_docs' must be a mapping"):
            CapabilityCatalog.from_dict({"capabilities": {"search_docs": []}})
        with pytest.raises(ValueError, match="Capability names must be unique"):
            CapabilityCatalog.from_dict(
                {
                    "capabilities": {
                        "search_docs": {},
                        " search_docs ": {},
                    }
                }
            )
        required_capability_fields = {
            "owner": "knowledge_platform",
            "mode": "read",
            "transport": "mcp",
            "tool_principal": "svc-knowledge-reader",
            "risk_tier": "low",
            "network_access": "restricted",
        }
        with pytest.raises(TypeError, match="'allowed_egress' must be a list"):
            CapabilityCatalog.from_dict(
                {
                    "capabilities": {
                        "search_docs": {
                            **required_capability_fields,
                            "allowed_egress": "docs.internal",
                        }
                    }
                }
            )
        with pytest.raises(TypeError, match="allowed_egress entries must be strings"):
            CapabilityCatalog.from_dict(
                {
                    "capabilities": {
                        "search_docs": {
                            **required_capability_fields,
                            "allowed_egress": [7],
                        }
                    }
                }
            )
        with pytest.raises(ValueError, match="allowed_egress entries must not be empty"):
            CapabilityCatalog.from_dict(
                {
                    "capabilities": {
                        "search_docs": {
                            **required_capability_fields,
                            "allowed_egress": [""],
                        }
                    }
                }
            )
        with pytest.raises(ValueError, match="allowed_egress entries must be unique"):
            CapabilityCatalog.from_dict(
                {
                    "capabilities": {
                        "search_docs": {
                            **required_capability_fields,
                            "allowed_egress": ["docs.internal", " docs.internal "],
                        }
                    }
                }
            )
        with pytest.raises(
            TypeError,
            match="capabilities.search_docs.owner must be a string",
        ):
            CapabilityCatalog.from_dict(
                {
                    "capabilities": {
                        "search_docs": {
                            **required_capability_fields,
                            "owner": 7,
                        }
                    }
                }
            )
        with pytest.raises(ValueError, match="capabilities.search_docs.owner is required"):
            CapabilityCatalog.from_dict(
                {
                    "capabilities": {
                        "search_docs": {
                            "mode": "read",
                            "transport": "mcp",
                            "tool_principal": "svc-knowledge-reader",
                            "risk_tier": "low",
                            "network_access": "restricted",
                        }
                    }
                }
            )
        with pytest.raises(
            ValueError, match="capabilities.search_docs.tool_principal is required"
        ):
            CapabilityCatalog.from_dict(
                {
                    "capabilities": {
                        "search_docs": {
                            "owner": "knowledge_platform",
                            "mode": "read",
                            "transport": "mcp",
                            "tool_principal": " ",
                            "risk_tier": "low",
                            "network_access": "restricted",
                        }
                    }
                }
            )
        for timeout_seconds in ("5", True):
            with pytest.raises(
                TypeError,
                match="'capabilities.search_docs.timeout_seconds' must be an integer",
            ):
                CapabilityCatalog.from_dict(
                    {
                        "capabilities": {
                            "search_docs": {
                                **required_capability_fields,
                                "timeout_seconds": timeout_seconds,
                            }
                        }
                    }
                )
        with pytest.raises(
            ValueError, match="capabilities.search_docs.timeout_seconds must be positive"
        ):
            CapabilityCatalog.from_dict(
                {
                    "capabilities": {
                        "search_docs": {
                            **required_capability_fields,
                            "timeout_seconds": 0,
                        }
                    }
                }
            )
        with pytest.raises(
            TypeError,
            match="capabilities.search_docs.approval must be a string",
        ):
            CapabilityCatalog.from_dict(
                {
                    "capabilities": {
                        "search_docs": {
                            **required_capability_fields,
                            "approval": 7,
                        }
                    }
                }
            )
        with pytest.raises(
            ValueError,
            match="capabilities.search_docs.approval must not be empty",
        ):
            CapabilityCatalog.from_dict(
                {
                    "capabilities": {
                        "search_docs": {
                            **required_capability_fields,
                            "approval": " ",
                        }
                    }
                }
            )
        with pytest.raises(
            ValueError,
            match="capabilities.search_docs.approval is not supported: mgr",
        ):
            CapabilityCatalog.from_dict(
                {
                    "capabilities": {
                        "search_docs": {
                            **required_capability_fields,
                            "approval": "mgr",
                        }
                    }
                }
            )
        with pytest.raises(
            TypeError,
            match="'capabilities.search_docs.idempotency_key_required' must be a boolean",
        ):
            CapabilityCatalog.from_dict(
                {
                    "capabilities": {
                        "search_docs": {
                            **required_capability_fields,
                            "idempotency_key_required": "false",
                        }
                    }
                }
            )
        catalog = CapabilityCatalog.from_dict(
            {
                "capabilities": {
                    "search_docs": {
                        **required_capability_fields,
                        "approval": " manager ",
                        "idempotency_key_required": True,
                    }
                }
            }
        )
        capability = catalog.get("search_docs")
        assert capability is not None
        assert capability.approval_required is True
        assert capability.idempotency_key_required is True

        direct_capability = CapabilitySpec(
            name=" search_docs ",
            owner=" knowledge_platform ",
            mode=" read ",
            transport=" mcp ",
            timeout_seconds=5,
            tool_principal=" svc-knowledge-reader ",
            risk_tier=" low ",
            network_access=" restricted ",
            allowed_egress=(" docs.internal ",),
        )
        assert direct_capability.name == "search_docs"
        assert direct_capability.allowed_egress == ("docs.internal",)
        direct_catalog = CapabilityCatalog(registry={" search_docs ": direct_capability})
        assert direct_catalog.get("search_docs") is direct_capability
        with pytest.raises(TypeError, match="Tool request capability name must be a string"):
            direct_catalog.get(cast(str, 7))
        with pytest.raises(TypeError, match="Capability names must be strings"):
            CapabilityCatalog(
                registry=cast(
                    dict[str, CapabilitySpec],
                    {7: direct_capability},
                )
            )
        with pytest.raises(ValueError, match="Capability names must be unique"):
            CapabilityCatalog(
                registry={
                    "search_docs": direct_capability,
                    " search_docs ": direct_capability,
                }
            )
        with pytest.raises(TypeError, match="capability.name must be a string"):
            CapabilitySpec(
                name=cast(str, 7),
                owner="knowledge_platform",
                mode="read",
                transport="mcp",
                timeout_seconds=5,
                tool_principal="svc-knowledge-reader",
                risk_tier="low",
                network_access="restricted",
                allowed_egress=("docs.internal",),
            )
        with pytest.raises(ValueError, match="capability.name is required"):
            CapabilitySpec(
                name=" ",
                owner="knowledge_platform",
                mode="read",
                transport="mcp",
                timeout_seconds=5,
                tool_principal="svc-knowledge-reader",
                risk_tier="low",
                network_access="restricted",
                allowed_egress=("docs.internal",),
            )
        with pytest.raises(TypeError, match="allowed_egress entries must be strings"):
            CapabilitySpec(
                name="search_docs",
                owner="knowledge_platform",
                mode="read",
                transport="mcp",
                timeout_seconds=5,
                tool_principal="svc-knowledge-reader",
                risk_tier="low",
                network_access="restricted",
                allowed_egress=cast(tuple[str, ...], (7,)),
            )
        with pytest.raises(ValueError, match="allowed_egress entries must be unique"):
            CapabilitySpec(
                name="search_docs",
                owner="knowledge_platform",
                mode="read",
                transport="mcp",
                timeout_seconds=5,
                tool_principal="svc-knowledge-reader",
                risk_tier="low",
                network_access="restricted",
                allowed_egress=("docs.internal", " docs.internal "),
            )
        with pytest.raises(
            TypeError,
            match="'capability.timeout_seconds' must be an integer",
        ):
            CapabilitySpec(
                name="search_docs",
                owner="knowledge_platform",
                mode="read",
                transport="mcp",
                timeout_seconds=cast(int, "5"),
                tool_principal="svc-knowledge-reader",
                risk_tier="low",
                network_access="restricted",
                allowed_egress=("docs.internal",),
            )
        with pytest.raises(ValueError, match="capability.timeout_seconds must be positive"):
            CapabilitySpec(
                name="search_docs",
                owner="knowledge_platform",
                mode="read",
                transport="mcp",
                timeout_seconds=0,
                tool_principal="svc-knowledge-reader",
                risk_tier="low",
                network_access="restricted",
                allowed_egress=("docs.internal",),
            )
        with pytest.raises(
            TypeError,
            match="'capability.approval_required' must be a boolean",
        ):
            CapabilitySpec(
                name="search_docs",
                owner="knowledge_platform",
                mode="read",
                transport="mcp",
                timeout_seconds=5,
                tool_principal="svc-knowledge-reader",
                risk_tier="low",
                network_access="restricted",
                allowed_egress=("docs.internal",),
                approval_required=cast(bool, "false"),
            )

    def test_identity_loaders_reject_bad_shapes_and_allow_lookup(self) -> None:
        from agent_runtime_ref.identity import AgentIdentity, ApprovedInventory, load_agent_identity

        with pytest.raises(TypeError, match="'agent' must be a mapping"):
            ApprovedInventory.from_agent_config({"agent": []})
        with pytest.raises(TypeError, match="'approved_capabilities' must be a list"):
            ApprovedInventory.from_agent_config({"agent": {"approved_capabilities": "x"}})
        with pytest.raises(
            TypeError, match="approved_capabilities entries must be strings"
        ):
            ApprovedInventory.from_agent_config({"agent": {"approved_capabilities": [7]}})
        with pytest.raises(
            ValueError, match="approved_capabilities entries must not be empty"
        ):
            ApprovedInventory.from_agent_config({"agent": {"approved_capabilities": [" "]}})
        with pytest.raises(
            ValueError, match="approved_capabilities entries must be unique"
        ):
            ApprovedInventory.from_agent_config(
                {"agent": {"approved_capabilities": ["search_docs", " search_docs "]}}
            )
        with pytest.raises(TypeError, match="'agent' must be a mapping"):
            load_agent_identity({"agent": []})
        with pytest.raises(TypeError, match="agent.id must be a string"):
            load_agent_identity(
                {
                    "agent": {
                        "id": 7,
                        "display_name": "Reference Runtime",
                        "owner_team": "agent_platform",
                        "runtime_principal": "svc-agent-runtime-ref",
                    }
                }
            )
        with pytest.raises(ValueError, match="agent.id is required"):
            load_agent_identity(
                {
                    "agent": {
                        "display_name": "Reference Runtime",
                        "owner_team": "agent_platform",
                        "runtime_principal": "svc-agent-runtime-ref",
                    }
                }
            )
        with pytest.raises(ValueError, match="agent.runtime_principal is required"):
            load_agent_identity(
                {
                    "agent": {
                        "id": "agent-runtime-ref",
                        "display_name": "Reference Runtime",
                        "owner_team": "agent_platform",
                        "runtime_principal": " ",
                    }
                }
            )

        direct_agent = AgentIdentity(
            agent_id=" agent-runtime-ref ",
            display_name=" Reference Runtime ",
            owner_team=" agent_platform ",
            runtime_principal=" svc-agent-runtime-ref ",
        )
        assert direct_agent.agent_id == "agent-runtime-ref"
        assert direct_agent.runtime_principal == "svc-agent-runtime-ref"
        with pytest.raises(TypeError, match="agent.id must be a string"):
            AgentIdentity(
                agent_id=cast(str, 7),
                display_name="Reference Runtime",
                owner_team="agent_platform",
                runtime_principal="svc-agent-runtime-ref",
            )
        with pytest.raises(ValueError, match="agent.id is required"):
            AgentIdentity(
                agent_id=" ",
                display_name="Reference Runtime",
                owner_team="agent_platform",
                runtime_principal="svc-agent-runtime-ref",
            )

        inventory = ApprovedInventory(capabilities=frozenset({" search_docs "}))
        assert inventory.capabilities == frozenset({"search_docs"})
        assert inventory.allows(" search_docs ")
        with pytest.raises(TypeError, match="approved_capabilities lookup must be a string"):
            inventory.allows(cast(str, 7))
        assert not inventory.allows("create_ticket")
        with pytest.raises(
            TypeError,
            match="approved_capabilities entries must be strings",
        ):
            ApprovedInventory(capabilities=cast(frozenset[str], frozenset({7})))
        with pytest.raises(
            ValueError,
            match="approved_capabilities entries must not be empty",
        ):
            ApprovedInventory(capabilities=frozenset({" "}))
        with pytest.raises(
            ValueError,
            match="approved_capabilities entries must be unique",
        ):
            ApprovedInventory(capabilities=frozenset({"search_docs", " search_docs "}))


class TestPolicyAndControls:
    def test_policy_denies_missing_principal(self) -> None:
        engine = PolicyEngine()
        decision = engine.precheck(
            RunRequest(
                user_input="hi",
                tenant_id="tenant-acme",
                principal_id="",
                trace_id="trace-deny-001",
                agent_id="agent-runtime-ref",
            ),
        )
        assert decision.action == "deny"

    def test_policy_denies_capability_outside_approved_inventory(self, config_dir: Path) -> None:
        catalog = load_capability_catalog(config_dir / "capabilities.yaml")
        memory = load_memory_store(config_dir / "memory.yaml")
        agent, approved_inventory = load_agent_profile(config_dir / "agent.yaml")
        restricted_inventory = type(approved_inventory)(frozenset({"search_docs"}))
        policy = load_policy_engine(
            config_dir / "policy.yaml",
            approved_inventory=restricted_inventory,
        )
        runtime = AgentRuntime(catalog=catalog, policy=policy, memory=memory, agent=agent)
        runtime.run(
            RunRequest(
                user_input="Please open a ticket for this issue.",
                tenant_id="tenant-acme",
                principal_id="user-2",
                trace_id="trace-inventory-001",
                agent_id=agent.agent_id,
            ),
        )
        tool_event = next(
            event
            for event in runtime.telemetry.events
            if event.event_type == "tool_policy_decision"
        )
        assert tool_event.payload["reason"] == "capability_not_in_inventory"

    def test_policy_denies_capability_without_egress_policy(self, config_dir: Path) -> None:
        catalog = load_capability_catalog(config_dir / "capabilities.yaml")
        _, approved_inventory = load_agent_profile(config_dir / "agent.yaml")
        policy = load_policy_engine(
            config_dir / "policy.yaml",
            approved_inventory=approved_inventory,
        )
        broken_spec = catalog.get("search_docs")
        assert broken_spec is not None

        from agent_runtime_ref.catalog import CapabilitySpec

        decision = policy.evaluate_tool(
            RunContext(
                tenant_id="tenant-acme",
                principal_id="user-2",
                trace_id="trace-egress-001",
            ),
            ToolRequest(
                capability_name="search_docs",
                arguments={"query": "onboarding policy"},
            ),
            CapabilitySpec(
                name=broken_spec.name,
                owner=broken_spec.owner,
                mode=broken_spec.mode,
                transport=broken_spec.transport,
                timeout_seconds=broken_spec.timeout_seconds,
                tool_principal=broken_spec.tool_principal,
                risk_tier=broken_spec.risk_tier,
                network_access="restricted",
                allowed_egress=(),
                approval_required=broken_spec.approval_required,
                idempotency_key_required=broken_spec.idempotency_key_required,
            ),
        )
        assert decision.action == "deny"
        assert decision.reason == "egress_policy_missing"

    def test_policy_rejects_malformed_tool_argument_values(self) -> None:
        policy = PolicyEngine()
        with pytest.raises(
            TypeError,
            match="Tool request capability name must be a string",
        ):
            policy.evaluate_tool(
                RunContext(
                    tenant_id="tenant-acme",
                    principal_id="user-2",
                    trace_id="trace-bad-tool-capability-001",
                ),
                ToolRequest(
                    capability_name=cast(str, 7),
                    arguments={"idempotency_key": "ticket-123"},
                ),
                None,
            )
        with pytest.raises(
            TypeError,
            match="Tool request argument key must be a string",
        ):
            policy.evaluate_tool(
                RunContext(
                    tenant_id="tenant-acme",
                    principal_id="user-2",
                    trace_id="trace-bad-tool-arg-key-001",
                ),
                ToolRequest(
                    capability_name="create_ticket",
                    arguments=cast(dict[str, str], {1: "ticket-123"}),
                ),
                None,
            )

        with pytest.raises(
            ValueError,
            match="Tool request argument key must not be empty",
        ):
            policy.evaluate_tool(
                RunContext(
                    tenant_id="tenant-acme",
                    principal_id="user-2",
                    trace_id="trace-blank-tool-arg-key-001",
                ),
                ToolRequest(
                    capability_name="create_ticket",
                    arguments={" ": "ticket-123"},
                ),
                None,
            )

        with pytest.raises(
            TypeError,
            match="Tool request argument value must be a string: idempotency_key",
        ):
            policy.evaluate_tool(
                RunContext(
                    tenant_id="tenant-acme",
                    principal_id="user-2",
                    trace_id="trace-bad-tool-arg-001",
                ),
                ToolRequest(
                    capability_name="create_ticket",
                    arguments=cast(dict[str, str], {"idempotency_key": 123}),
                ),
                None,
            )

    @pytest.mark.parametrize(
        ("offline_eval_pass", "expected_ready"),
        [(True, True), (False, False)],
    )
    def test_rollout_gate_requires_all_flags(
        self,
        offline_eval_pass: bool,
        expected_ready: bool,
    ) -> None:
        readiness = RolloutReadiness(
            trace_coverage=True,
            offline_eval_pass=offline_eval_pass,
            slo_defined=True,
            rollback_plan=True,
        )
        assert ready_for_rollout(readiness) is expected_ready

    def test_rollout_policy_detects_blockers(self, config_dir: Path) -> None:
        policy = load_rollout_policy(config_dir / "rollout.yaml")
        policy = type(policy)(
            required_checks=tuple(f" {check} " for check in policy.required_checks),
            blocked_checks=tuple(f" {check} " for check in policy.blocked_checks),
            rollout_mode=policy.rollout_mode,
        )
        assessment = assess_rollout(
            policy,
            {
                " trace_coverage ": True,
                "policy_prechecks": True,
                "capability_owners": True,
                "offline_eval_pass": True,
                "slo_defined": True,
                "rollback_plan": True,
                "oncall_owner": True,
                " direct_tool_access_present ": True,
            },
        )
        assert not assessment.ready
        assert "direct_tool_access_present" in assessment.blocking_signals

        with pytest.raises(TypeError, match="Assessment signal key must be a string"):
            assess_rollout(policy, cast(dict[str, bool], {1: True}))
        with pytest.raises(ValueError, match="Assessment signal key must not be empty"):
            assess_rollout(policy, {" ": True})
        with pytest.raises(ValueError, match="Assessment signal keys must be unique"):
            assess_rollout(policy, {" trace_coverage ": True, "trace_coverage": True})
        with pytest.raises(
            TypeError,
            match="Assessment signal value must be a boolean: trace_coverage",
        ):
            assess_rollout(policy, cast(dict[str, bool], {"trace_coverage": "false"}))

    def test_controls_policy_detects_inventory_drift(self, config_dir: Path) -> None:
        policy = load_controls_policy(config_dir / "controls.yaml")
        catalog = load_capability_catalog(config_dir / "capabilities.yaml")
        _, approved_inventory = load_agent_profile(config_dir / "agent.yaml")
        drift = assess_inventory_drift(approved_inventory, catalog)
        assessment = assess_controls(
            policy,
            {
                " registry_reviewed ": True,
                "capability_owners_confirmed": True,
                "memory_provenance_enforced": True,
                "policy_traces_present": True,
                "direct_tool_access_present": False,
                " unmanaged_runtime_present ": False,
            },
            inventory_drift=drift,
        )
        assert assessment.healthy
        assert not assessment.inventory_drift.has_drift

        with pytest.raises(TypeError, match="Assessment signal key must be a string"):
            assess_controls(
                policy,
                cast(dict[str, bool], {1: True}),
                inventory_drift=drift,
            )
        with pytest.raises(ValueError, match="Assessment signal key must not be empty"):
            assess_controls(policy, {" ": True}, inventory_drift=drift)
        with pytest.raises(ValueError, match="Assessment signal keys must be unique"):
            assess_controls(
                policy,
                {" registry_reviewed ": True, "registry_reviewed": True},
                inventory_drift=drift,
            )
        with pytest.raises(
            TypeError,
            match="Assessment signal value must be a boolean: registry_reviewed",
        ):
            assess_controls(
                policy,
                cast(dict[str, bool], {"registry_reviewed": "false"}),
                inventory_drift=drift,
            )


class TestDelegatedAuthorizationConfig:
    def test_runtime_controls_capture_delegated_authorization_contract(
        self, config_dir: Path
    ) -> None:
        runtime_controls = load_yaml_file(config_dir / "runtime-controls.yaml")
        delegated = runtime_controls["runtime_controls"]["delegated_authorization"]
        assert delegated["authorization_mode"] == "user_delegated_or_platform_owned"
        assert delegated["delegated_principal_policy"] == "explicit_principal_binding_required"
        assert delegated["token_reuse_policy"] == "reuse_within_valid_paused_run_only"
        assert delegated["on_authorization_revoke"] == "cancel_or_reapprove"
        assert delegated["subagent_inheritance"] == "denied_by_default"

    def test_approvals_capture_delegated_authorization_review_rules(self, config_dir: Path) -> None:
        approvals = load_yaml_file(config_dir / "approvals.yaml")
        delegated = approvals["approvals"]["delegated_authorization"]
        assert delegated["reviewer_required_for_user_delegation"] == "manager"
        assert delegated["require_principal_binding"] is True
        assert delegated["require_scope_visibility"] is True
        assert delegated["on_scope_revoked"] == "cancel_or_reapprove"
        assert delegated["subagent_inheritance"] == "explicit_only"


class TestDelegatedAuthorizationRuntime:
    def test_runtime_requires_delegated_identity_fields_for_user_delegation(self) -> None:
        required_fields = {
            "delegated_principal_id": {
                "delegated_principal_id": " ",
                "delegated_scope": "tickets.write",
            },
            "delegated_scope": {
                "delegated_principal_id": "user-1",
                "delegated_scope": " ",
            },
        }
        for field, payload in required_fields.items():
            runtime = AgentRuntime()
            with pytest.raises(
                ValueError,
                match=f"Delegated authorization field is required: {field}",
            ):
                runtime.run(
                    RunRequest(
                        user_input="Please create a ticket for this onboarding issue.",
                        tenant_id="tenant-acme",
                        principal_id="user-1",
                        trace_id=f"trace-authz-required-{field}",
                        session_id=f"session-authz-required-{field}",
                        agent_id="agent-runtime-ref",
                        authorization_mode="user_delegated",
                        **payload,
                    ),
                )
            assert runtime.telemetry.events == []

    def test_runtime_emits_and_exports_delegated_authorization_fields(self) -> None:
        runtime = AgentRuntime()
        result = runtime.run(
            RunRequest(
                user_input="Please create a ticket for this onboarding issue.",
                tenant_id="tenant-acme",
                principal_id="user-1",
                trace_id="trace-authz-001",
                session_id="session-authz-001",
                agent_id="agent-runtime-ref",
                authorization_mode=" user_delegated ",
                delegated_principal_id=" user-1 ",
                delegated_scope=" tickets.write ",
            ),
        )
        assert result.status == "success"

        approval_request = runtime.approvals.all()[0]
        assert approval_request.authorization_mode == "user_delegated"
        assert approval_request.delegated_principal_id == "user-1"
        assert approval_request.delegated_scope == "tickets.write"

        approval_event = next(
            event for event in runtime.telemetry.events if event.event_type == "approval_requested"
        )
        assert approval_event.payload["authorization_mode"] == "user_delegated"
        assert approval_event.payload["delegated_principal_id"] == "user-1"
        assert approval_event.payload["delegated_scope"] == "tickets.write"

        tool_event = next(
            event for event in runtime.telemetry.events if event.event_type == "tool_execution"
        )
        assert tool_event.payload["authorization_mode"] == "user_delegated"
        assert tool_event.payload["delegated_principal_id"] == "user-1"
        assert tool_event.payload["delegated_scope"] == "tickets.write"

        session_run = runtime.sessions.runs_for_session("session-authz-001")[0]
        assert session_run.authorization_mode == "user_delegated"
        assert session_run.delegated_principal_id == "user-1"
        assert session_run.delegated_scope == "tickets.write"

    def test_session_export_includes_delegated_authorization_fields(self, tmp_path: Path) -> None:
        runtime = AgentRuntime()
        runtime.run(
            RunRequest(
                user_input="Please create a ticket for this onboarding issue.",
                tenant_id="tenant-acme",
                principal_id="user-1",
                trace_id="trace-authz-export-001",
                session_id="session-authz-export-001",
                agent_id="agent-runtime-ref",
                authorization_mode="user_delegated",
                delegated_principal_id="user-1",
                delegated_scope="tickets.write",
            ),
        )
        output_path = tmp_path / "session-authz.json"
        runtime.sessions.export_session_json("session-authz-export-001", output_path=output_path)
        payload = json.loads(output_path.read_text(encoding="utf-8"))
        run = payload["runs"][0]
        assert run["authorization_mode"] == "user_delegated"
        assert run["delegated_principal_id"] == "user-1"
        assert run["delegated_scope"] == "tickets.write"


class TestLifecycleArtifacts:
    def test_change_gate_detects_missing_signal(self, config_dir: Path) -> None:
        from agent_runtime_ref.config import load_change_record

        change = load_change_record(config_dir / "change.yaml")
        assessment = assess_change_gate(
            change,
            {
                "design_review_passed": True,
                "offline_eval_passed": False,
                "policy_diff_reviewed": True,
                "rollback_plan_ready": True,
            },
        )
        assert not assessment.ready
        assert assessment.missing_signals == (
            "offline_eval_passed",
            "session_expiry_behavior_checked",
            "reinit_policy_reviewed",
            "sandbox_profile_reviewed",
            "failed_run_drill_checked",
        )

    def test_retirement_assessment_detects_incomplete_step(self, config_dir: Path) -> None:
        from agent_runtime_ref.config import load_retirement_plan

        plan = load_retirement_plan(config_dir / "retirement.yaml")
        assessment = assess_retirement(
            plan,
            {
                "freeze_rollout": True,
                "disable_risky_capabilities": True,
                "stop_memory_write": True,
                "expire_paused_runs": True,
                "stop_background_routes": True,
                "revoke_egress": False,
                "archive_audit_state": True,
                "set_retired_status": True,
            },
        )
        assert not assessment.ready
        assert assessment.missing_steps == ("freeze_reinitialization", "revoke_egress")


class TestCli:
    @pytest.mark.parametrize("command", [[], ["simulate-run"]])
    def test_cli_simulate_run_returns_json(
        self,
        command: list[str],
        cli_json,
    ) -> None:
        exit_code, payload = cli_json(command)
        assert exit_code == 0
        assert set(payload) == {
            "agent_id",
            "session_id",
            "result",
            "status",
            "failure_reason",
            "trace_id",
            "events",
            "memory_records",
            "pending_approvals",
            "config_dir",
        }
        assert payload["agent_id"] == "support-triage-ref"
        assert payload["session_id"] == "session-demo-001"
        assert payload["result"] == "Ticket request is waiting for human approval (apr-001)."
        assert payload["status"] == "success"
        assert payload["failure_reason"] == ""
        assert payload["trace_id"] == "trace-demo-001"
        assert payload["events"] == 14
        assert payload["memory_records"] == 4
        assert payload["pending_approvals"] == 1
        assert payload["config_dir"].endswith("agent_runtime_ref/configs")

    def test_cli_inspect_memory_filters_records(self, cli_json) -> None:
        exit_code, payload = cli_json(["inspect-memory", "--memory-class", "profile"])
        assert exit_code == 0
        assert set(payload) == {"config_dir", "count", "records"}
        assert payload["config_dir"].endswith("agent_runtime_ref/configs")
        assert payload["count"] == len(payload["records"])
        assert payload["count"] >= 1
        for item in payload["records"]:
            assert set(item) == {
                "memory_id",
                "tenant_id",
                "memory_class",
                "kind",
                "source",
                "confidence",
                "provenance",
                "revision",
                "content",
            }
            assert item["memory_class"] == "profile"

    def test_cli_inspect_memory_normalizes_filter_values(self, cli_json) -> None:
        exit_code, payload = cli_json(
            [
                "inspect-memory",
                "--tenant-id",
                " tenant-acme ",
                "--memory-class",
                " profile ",
            ]
        )
        assert exit_code == 0
        assert payload["count"] >= 1
        assert all(item["tenant_id"] == "tenant-acme" for item in payload["records"])
        assert all(item["memory_class"] == "profile" for item in payload["records"])

    def test_cli_inspect_memory_rejects_negative_limit(self) -> None:
        from agent_runtime_ref.__main__ import main

        with pytest.raises(ValueError, match="CLI field must be non-negative: limit"):
            main(["inspect-memory", "--limit", "-1"])

    def test_cli_inspect_agent_returns_identity_and_inventory(self, cli_json) -> None:
        exit_code, payload = cli_json(["inspect-agent"])
        assert exit_code == 0
        assert set(payload) == {
            "agent_id",
            "display_name",
            "owner_team",
            "runtime_principal",
            "approved_capabilities",
            "catalog_capabilities",
        }
        assert payload["agent_id"] == "support-triage-ref"
        assert payload["display_name"] == "Support Triage Reference Agent"
        assert payload["owner_team"] == "agent_platform"
        assert payload["runtime_principal"] == "svc-support-triage-ref"
        assert payload["approved_capabilities"] == ["create_ticket", "search_docs"]
        for item in payload["catalog_capabilities"]:
            assert set(item) == {
                "name",
                "owner",
                "risk_tier",
                "network_access",
                "tool_principal",
                "allowed_egress",
            }
        search_docs = next(
            item for item in payload["catalog_capabilities"] if item["name"] == "search_docs"
        )
        create_ticket = next(
            item for item in payload["catalog_capabilities"] if item["name"] == "create_ticket"
        )
        assert search_docs["owner"] == "knowledge_platform"
        assert search_docs["network_access"] == "restricted"
        assert search_docs["tool_principal"] == "svc-knowledge-reader"
        assert search_docs["allowed_egress"] == ["docs.internal"]
        assert create_ticket["risk_tier"] == "high"
        assert create_ticket["owner"] == "support_platform"
        assert create_ticket["network_access"] == "brokered"
        assert create_ticket["tool_principal"] == "svc-ticket-writer"
        assert create_ticket["allowed_egress"] == ["tickets.internal"]

    @pytest.mark.parametrize(
        ("command", "expected_key"),
        [
            (["dump-events", "--user-input", "Please open a ticket for this issue."], "events"),
            (["inspect-session"], "runs"),
            (["session-eval-summary"], "total_runs"),
        ],
    )
    def test_cli_commands_return_json_payloads(
        self,
        command: list[str],
        expected_key: str,
        cli_json,
    ) -> None:
        exit_code, payload = cli_json(command)
        assert exit_code == 0
        assert expected_key in payload

    @pytest.mark.parametrize(
        ("command", "expected_summary"),
        [
            (
                ["session-eval-summary"],
                {
                    "total_runs": 1,
                    "success_runs": 1,
                    "approval_wait_runs": 1,
                    "denied_runs": 0,
                    "failed_runs": 0,
                    "traceable_failed_runs": 0,
                    "latest_failure_reason": "",
                    "latest_trace_id": "trace-session-001",
                    "latest_status": "success",
                },
            ),
            (
                [
                    "session-eval-summary",
                    "--user-input",
                    "Please create a ticket for this onboarding issue.",
                    "--user-input",
                    "What language preference do you remember?",
                ],
                {
                    "total_runs": 2,
                    "success_runs": 2,
                    "approval_wait_runs": 1,
                    "denied_runs": 0,
                    "failed_runs": 0,
                    "traceable_failed_runs": 0,
                    "latest_failure_reason": "",
                    "latest_trace_id": "trace-session-002",
                    "latest_status": "success",
                },
            ),
            (
                [
                    "session-eval-summary",
                    "--simulate-failure",
                    "tool_timeout",
                    "--user-input",
                    "Trigger a timeout while creating a ticket.",
                ],
                {
                    "total_runs": 1,
                    "success_runs": 0,
                    "approval_wait_runs": 0,
                    "denied_runs": 0,
                    "failed_runs": 1,
                    "traceable_failed_runs": 1,
                    "latest_failure_reason": "tool_timeout",
                    "latest_trace_id": "trace-session-001",
                    "latest_status": "failed",
                },
            ),
        ],
    )
    def test_cli_session_eval_summary_keeps_documented_contract(
        self,
        command: list[str],
        expected_summary: dict[str, object],
        cli_json,
    ) -> None:
        exit_code, payload = cli_json(command)
        assert exit_code == 0
        assert set(payload) == {
            "session_id",
            "total_runs",
            "success_runs",
            "approval_wait_runs",
            "denied_runs",
            "failed_runs",
            "traceable_failed_runs",
            "latest_failure_reason",
            "latest_trace_id",
            "latest_status",
        }
        assert payload["session_id"] == "session-demo-001"
        for key, value in expected_summary.items():
            assert payload[key] == value

    def test_cli_session_eval_summary_surfaces_failed_run_fields(self, cli_json) -> None:
        exit_code, payload = cli_json(
            [
                "session-eval-summary",
                "--user-input",
                "Please create a ticket for this issue.",
                "--trace-prefix",
                "trace-session-failure",
                "--session-id",
                "session-failure-summary-001",
                "--simulate-failure",
                "tool_timeout",
            ]
        )
        assert exit_code == 0
        assert payload["failed_runs"] == 1
        assert payload["traceable_failed_runs"] == 1
        assert payload["latest_failure_reason"] == "tool_timeout"

    def test_cli_session_eval_summary_counts_precheck_denials(self, cli_json) -> None:
        exit_code, payload = cli_json(
            [
                "session-eval-summary",
                "--tenant-id",
                " ",
                "--session-id",
                "session-denied-summary-001",
            ]
        )
        assert exit_code == 0
        assert payload["total_runs"] == 1
        assert payload["denied_runs"] == 1
        assert payload["latest_status"] == "denied"

    def test_cli_dump_events_reports_event_count(self, cli_json) -> None:
        exit_code, payload = cli_json(
            [
                "dump-events",
                "--user-input",
                "Please open a ticket for this issue.",
                "--trace-id",
                "trace-cli-dump-success-001",
            ]
        )
        assert exit_code == 0
        assert set(payload) == {
            "status",
            "result",
            "failure_reason",
            "trace_id",
            "event_count",
            "events",
        }
        assert payload["trace_id"] == "trace-cli-dump-success-001"
        assert payload["status"] == "success"
        assert payload["failure_reason"] == ""
        assert payload["result"] == "Ticket request is waiting for human approval (apr-001)."
        assert payload["event_count"] == len(payload["events"])

    def test_cli_export_and_inspect_trace(self, cli_json, tmp_path: Path) -> None:
        output_path = tmp_path / "trace.jsonl"
        export_code, export_payload = cli_json(
            [
                "export-events",
                "--user-input",
                "Please open a ticket for this issue.",
                "--trace-id",
                "trace-export-001",
                "--output",
                str(output_path),
            ],
        )
        assert export_code == 0
        assert set(export_payload) == {
            "output_path",
            "trace_id",
            "status",
            "result",
            "event_count",
            "redact_fields",
            "failure_reason",
        }
        assert output_path.exists()
        assert export_payload["output_path"] == str(output_path)
        assert export_payload["trace_id"] == "trace-export-001"
        assert export_payload["status"] == "success"
        assert export_payload["failure_reason"] == ""
        assert export_payload["result"] == "Ticket request is waiting for human approval (apr-001)."
        assert export_payload["redact_fields"] == []
        assert export_payload["event_count"] == len(
            output_path.read_text(encoding="utf-8").splitlines()
        )

        inspect_code, inspect_payload = cli_json(
            [
                "inspect-trace",
                "--input",
                str(output_path),
            ],
        )
        assert inspect_code == 0
        assert set(inspect_payload) == {"trace_id", "event_count", "events"}
        assert inspect_payload["trace_id"] == "trace-export-001"
        assert inspect_payload["event_count"] == len(inspect_payload["events"])
        assert any(item["event_type"] == "run_complete" for item in inspect_payload["events"])
        assert any(
            item["payload"].get("session_id") == "session-demo-001"
            for item in inspect_payload["events"]
        )
        assert all(item["schema_version"] == "1.0" for item in inspect_payload["events"])

    def test_cli_export_trace_supports_redaction(self, cli_json, tmp_path: Path) -> None:
        output_path = tmp_path / "trace-redacted.jsonl"
        export_code, export_payload = cli_json(
            [
                "export-events",
                "--user-input",
                "Please open a ticket for this issue.",
                "--trace-id",
                "trace-redacted-001",
                "--output",
                str(output_path),
                "--redact-field",
                " user_input ",
                "--redact-field",
                "user_input",
            ],
        )
        assert export_code == 0
        assert set(export_payload) == {
            "output_path",
            "trace_id",
            "status",
            "result",
            "event_count",
            "redact_fields",
            "failure_reason",
        }
        assert export_payload["output_path"] == str(output_path)
        assert export_payload["trace_id"] == "trace-redacted-001"
        assert export_payload["status"] == "success"
        assert export_payload["failure_reason"] == ""
        assert export_payload["redact_fields"] == ["user_input"]
        assert output_path.exists()
        assert export_payload["event_count"] == len(
            output_path.read_text(encoding="utf-8").splitlines()
        )

        inspect_code, inspect_payload = cli_json(
            [
                "inspect-trace",
                "--input",
                str(output_path),
            ],
        )
        assert inspect_code == 0
        run_start = next(
            item for item in inspect_payload["events"] if item["event_type"] == "run_start"
        )
        assert run_start["payload"]["user_input"] == "[REDACTED]"
        assert run_start["redacted_fields"] == ["user_input"]
        run_complete = next(
            item for item in inspect_payload["events"] if item["event_type"] == "run_complete"
        )
        assert run_complete["redacted_fields"] == []

    def test_cli_export_trace_rejects_unknown_redact_fields(
        self, tmp_path: Path
    ) -> None:
        output_path = tmp_path / "trace-unknown-redaction.jsonl"

        from agent_runtime_ref.__main__ import main

        with pytest.raises(
            ValueError,
            match="Telemetry redact field is not present in events: does_not_exist",
        ):
            main(
                [
                    "export-events",
                    "--user-input",
                    "Please open a ticket for this issue.",
                    "--trace-id",
                    "trace-unknown-redaction",
                    "--output",
                    str(output_path),
                    "--redact-field",
                    "does_not_exist",
                ]
            )
        assert not output_path.exists()

    def test_cli_export_trace_preserves_runtime_control_event_order(
        self, cli_json, tmp_path: Path
    ) -> None:
        output_path = tmp_path / "trace-ordered.jsonl"
        export_code, _ = cli_json(
            [
                "export-events",
                "--user-input",
                "Please create a ticket for this onboarding issue.",
                "--trace-id",
                "trace-ordered-001",
                "--output",
                str(output_path),
            ],
        )
        assert export_code == 0

        inspect_code, inspect_payload = cli_json(["inspect-trace", "--input", str(output_path)])
        assert inspect_code == 0
        event_types = [item["event_type"] for item in inspect_payload["events"]]
        assert event_types[0] == "run_start"
        assert event_types[-1] == "run_complete"
        assert "policy_precheck" in event_types
        assert "approval_requested" in event_types
        assert "sandbox_profile_reviewed" in event_types
        assert "tool_execution" in event_types
        assert (
            event_types.index("approval_requested")
            < event_types.index("sandbox_profile_reviewed")
            < event_types.index("tool_execution")
            < event_types.index("run_complete")
        )
        sandbox_review = next(
            item
            for item in inspect_payload["events"]
            if item["event_type"] == "sandbox_profile_reviewed"
        )
        assert sandbox_review["payload"]["sandbox_profile_contract"] == "sandbox-profile-v1"
        assert sandbox_review["payload"]["workspace_entries_reviewed"] == "true"
        assert sandbox_review["payload"]["snapshot_policy"] == "required_on_completion"
        assert "eval:sandbox_profile_review" in sandbox_review["payload"]["review_evidence_refs"]

    def test_cli_export_trace_keeps_single_trace_and_session_consistent(
        self, cli_json, tmp_path: Path
    ) -> None:
        output_path = tmp_path / "trace-consistent.jsonl"
        export_code, export_payload = cli_json(
            [
                "export-events",
                "--user-input",
                "Please create a ticket for this onboarding issue.",
                "--trace-id",
                "trace-consistent-001",
                "--session-id",
                "session-consistent-001",
                "--output",
                str(output_path),
            ],
        )
        assert export_code == 0
        assert export_payload["trace_id"] == "trace-consistent-001"

        inspect_code, inspect_payload = cli_json(["inspect-trace", "--input", str(output_path)])
        assert inspect_code == 0
        assert all(item["trace_id"] == "trace-consistent-001" for item in inspect_payload["events"])
        session_ids = {
            item["payload"]["session_id"]
            for item in inspect_payload["events"]
            if "session_id" in item["payload"]
        }
        assert session_ids == {"session-consistent-001"}

    def test_cli_replay_run_uses_exported_trace(self, cli_json, tmp_path: Path) -> None:
        output_path = tmp_path / "trace.jsonl"
        export_code, _ = cli_json(
            [
                "export-events",
                "--user-input",
                "What language preference do you remember?",
                "--trace-id",
                "trace-replay-source",
                "--output",
                str(output_path),
            ],
        )
        assert export_code == 0

        replay_code, replay_payload = cli_json(
            [
                "replay-run",
                "--input",
                str(output_path),
                "--replay-trace-id",
                "trace-replay-target",
            ],
        )
        assert replay_code == 0
        assert set(replay_payload) == {
            "source_trace_id",
            "replay_trace_id",
            "status",
            "result",
            "event_count",
        }
        assert replay_payload["source_trace_id"] == "trace-replay-source"
        assert replay_payload["replay_trace_id"] == "trace-replay-target"
        assert replay_payload["status"] == "success"
        assert replay_payload["result"] == (
            "Retrieved profile hint: User usually prefers concise English answers."
        )
        assert replay_payload["event_count"] == len(
            output_path.read_text(encoding="utf-8").splitlines()
        )

    def test_cli_check_rollout_reports_missing_signal(self, cli_json) -> None:
        exit_code, payload = cli_json(
            [
                "check-rollout",
                "--signal",
                "trace_coverage=true",
                "--signal",
                "offline_eval_pass=false",
            ],
        )
        assert exit_code == 0
        assert set(payload) == {
            "ready",
            "missing_required",
            "blocking_signals",
            "rollout_mode",
        }
        assert not payload["ready"]
        assert payload["missing_required"] == ["offline_eval_pass"]
        assert payload["blocking_signals"] == []
        assert payload["rollout_mode"] == {
            "initial": "canary",
            "max_tenant_exposure_pct": "5",
            "require_shadow_period": "True",
        }

    def test_cli_check_rollout_reports_blocking_signal(self, cli_json) -> None:
        exit_code, payload = cli_json(
            [
                "check-rollout",
                "--signal",
                "unknown_side_effect_path_missing=true",
            ],
        )
        assert exit_code == 0
        assert set(payload) == {
            "ready",
            "missing_required",
            "blocking_signals",
            "rollout_mode",
        }
        assert not payload["ready"]
        assert payload["missing_required"] == []
        assert payload["blocking_signals"] == ["unknown_side_effect_path_missing"]
        assert payload["rollout_mode"] == {
            "initial": "canary",
            "max_tenant_exposure_pct": "5",
            "require_shadow_period": "True",
        }

    @pytest.mark.parametrize(
        ("raw_signal", "expected_message"),
        [
            ("trace_coverage", "Signal must use key=value format"),
            ("=true", "Signal key must not be empty"),
            ("trace_coverage=maybe", "Unsupported boolean value in signal"),
        ],
    )
    def test_cli_check_rollout_rejects_invalid_signal_values(
        self, raw_signal: str, expected_message: str
    ) -> None:
        from agent_runtime_ref.__main__ import main

        with pytest.raises(ValueError, match=expected_message):
            main(["check-rollout", "--signal", raw_signal])

    def test_cli_check_controls_reports_control_failure(self, cli_json) -> None:
        exit_code, payload = cli_json(
            [
                "check-controls",
                "--signal",
                "registry_reviewed=false",
            ],
        )
        assert exit_code == 0
        assert set(payload) == {
            "healthy",
            "missing_controls",
            "failed_run_controls",
            "preserved_failed_run_controls",
            "failed_run_controls_healthy",
            "blocking_findings",
            "inventory_drift",
        }
        assert not payload["healthy"]
        assert payload["missing_controls"] == ["registry_reviewed"]
        assert payload["failed_run_controls"] == []
        assert payload["preserved_failed_run_controls"] == [
            "policy_traces_present",
            "memory_provenance_enforced",
        ]
        assert payload["failed_run_controls_healthy"] is True
        assert payload["blocking_findings"] == []
        assert not payload["inventory_drift"]["has_drift"]
        assert payload["inventory_drift"] == {
            "has_drift": False,
            "missing_from_catalog": [],
            "missing_from_inventory": [],
        }

    @pytest.mark.parametrize(
        ("raw_signal", "expected_message"),
        [
            ("registry_reviewed", "Signal must use key=value format"),
            ("registry_reviewed=maybe", "Unsupported boolean value in signal"),
        ],
    )
    def test_cli_check_controls_rejects_invalid_signal_values(
        self, raw_signal: str, expected_message: str
    ) -> None:
        from agent_runtime_ref.__main__ import main

        with pytest.raises(ValueError, match=expected_message):
            main(["check-controls", "--signal", raw_signal])

    def test_cli_inspect_lifecycle_returns_all_artifacts(self, cli_json) -> None:
        exit_code, payload = cli_json(["inspect-lifecycle"])
        assert exit_code == 0
        assert set(payload) == {
            "change",
            "artifact_bundle",
            "retirement",
            "sandbox_profile",
            "controls",
        }
        assert set(payload["change"]) == {
            "change_id",
            "change_type",
            "risk_level",
            "rollout_strategy",
            "artifacts",
            "affected_surfaces",
            "required_signals",
            "approval_roles",
            "session_control_owner",
            "emergency_freeze_owner",
            "failed_run_signals",
        }
        assert set(payload["artifact_bundle"]) == {
            "bundle_name",
            "version",
            "provenance_required",
            "signed",
            "session_control_owner",
            "artifacts",
            "review_evidence",
            "sandbox_profile_review_evidence",
        }
        assert set(payload["retirement"]) == {
            "system_id",
            "replacement_mode",
            "triggers",
            "required_steps",
            "session_control_owner",
            "emergency_freeze_owner",
            "archive_targets",
            "failed_run_archive_targets",
        }
        assert set(payload["sandbox_profile"]) == {
            "manifest_version",
            "workspace_entries",
            "capabilities",
            "permissions",
            "state",
        }
        assert payload["change"]["change_id"] == "chg-2026-04-07-support-runtime"
        assert payload["change"]["artifacts"] == [
            "agent.yaml",
            "capabilities.yaml",
            "policy.yaml",
            "runtime-controls.yaml",
            "eval-dataset.json",
        ]
        assert payload["change"]["affected_surfaces"] == [
            "capability_contract",
            "runtime_control_schema",
            "capability_session_contract",
            "sandbox_profile_contract",
            "failed_run_handling",
        ]
        assert payload["change"]["required_signals"] == [
            "design_review_passed",
            "offline_eval_passed",
            "policy_diff_reviewed",
            "rollback_plan_ready",
            "session_expiry_behavior_checked",
            "reinit_policy_reviewed",
            "sandbox_profile_reviewed",
            "failed_run_drill_checked",
        ]
        assert payload["change"]["failed_run_signals"] == ["failed_run_drill_checked"]
        assert payload["artifact_bundle"]["bundle_name"] == "support-triage-runtime-bundle"
        assert payload["change"]["session_control_owner"] == "support-ops"
        assert payload["change"]["emergency_freeze_owner"] == "platform-runtime"
        assert payload["change"]["approval_roles"] == [
            "platform-owner",
            "security-reviewer",
        ]
        assert payload["artifact_bundle"]["artifacts"] == [
            "agent.yaml",
            "capabilities.yaml",
            "policy.yaml",
            "memory.yaml",
            "controls.yaml",
            "approvals.yaml",
            "runtime-controls.yaml",
            "change.yaml",
            "retirement.yaml",
            "eval-dataset.json",
            "runtime-control-bundle-metadata",
        ]
        assert payload["artifact_bundle"]["session_control_owner"] == "support-ops"
        assert set(payload["artifact_bundle"]["review_evidence"]) == {
            "sandbox_profile_reviewed"
        }
        sandbox_review = payload["artifact_bundle"]["sandbox_profile_review_evidence"]
        assert (
            payload["artifact_bundle"]["review_evidence"]["sandbox_profile_reviewed"]
            == sandbox_review
        )
        assert set(sandbox_review) == {
            "trace_event",
            "workspace_manifest_ref",
            "permissions_profile",
            "network_secrets_posture",
            "snapshot_policy",
            "review_evidence_refs",
        }
        assert sandbox_review["trace_event"] == "sandbox_profile_reviewed"
        assert (
            sandbox_review["workspace_manifest_ref"]
            == "runtime-controls.yaml#runtime_controls.sandbox_profile.workspace"
        )
        assert sandbox_review["permissions_profile"] == "restricted-shell-network-denied"
        assert sandbox_review["network_secrets_posture"] == "network:denied,secrets:none"
        assert sandbox_review["snapshot_policy"] == "required_on_completion"
        assert "eval:sandbox_profile_review" in sandbox_review["review_evidence_refs"]
        assert payload["retirement"]["system_id"] == "support-triage-ref"
        assert payload["retirement"]["session_control_owner"] == "support-ops"
        assert payload["retirement"]["emergency_freeze_owner"] == "platform-runtime"
        assert payload["retirement"]["triggers"] == [
            "deprecated_runtime",
            "replacement_ready",
            "unsafe_capability_pattern",
        ]
        assert payload["retirement"]["required_steps"] == [
            "freeze_rollout",
            "disable_risky_capabilities",
            "stop_memory_write",
            "expire_paused_runs",
            "stop_background_routes",
            "freeze_reinitialization",
            "revoke_egress",
            "archive_audit_state",
            "set_retired_status",
        ]
        assert payload["retirement"]["archive_targets"] == [
            "telemetry_jsonl",
            "session_exports",
            "approval_history",
            "paused_run_state",
            "capability_session_state",
            "runtime_control_bundle",
        ]
        assert payload["retirement"]["failed_run_archive_targets"] == [
            "telemetry_jsonl",
            "session_exports",
            "approval_history",
        ]
        assert set(payload["controls"]) == {
            "failed_run_control_expectations",
            "failed_run_control_domains",
            "failed_run_control_count",
            "failed_run_control_summary",
            "failed_run_control_status",
            "failed_run_control_review_required",
            "failed_run_control_owner",
            "failed_run_control_source",
            "failed_run_control_last_review",
            "failed_run_control_next_review",
            "failed_run_control_release_binding",
        }
        assert payload["controls"]["failed_run_control_expectations"] == [
            "policy_traces_present",
            "memory_provenance_enforced",
        ]
        assert payload["controls"]["failed_run_control_domains"] == [
            "traceability",
            "memory_provenance",
        ]
        assert payload["controls"]["failed_run_control_count"] == 2
        assert payload["controls"]["failed_run_control_summary"] == (
            "2 failed-run control expectations across traceability and memory provenance"
        )
        assert payload["controls"]["failed_run_control_status"] == "covered"
        assert payload["controls"]["failed_run_control_review_required"] is True
        assert payload["controls"]["failed_run_control_owner"] == "runtime-governance"
        assert payload["controls"]["failed_run_control_source"] == "runtime-controls.yaml"
        assert payload["controls"]["failed_run_control_last_review"] == "release-readiness"
        assert payload["controls"]["failed_run_control_next_review"] == "rollout-gate"
        assert payload["controls"]["failed_run_control_release_binding"] == "required"
        assert payload["sandbox_profile"]["manifest_version"] == 1
        assert payload["sandbox_profile"]["workspace_entries"] == [
            {"path": "repo", "source": "local_dir", "read_only": False},
            {"path": "task.md", "source": "inline_file", "read_only": True},
        ]
        assert all(
            set(entry) == {"path", "source", "read_only"}
            for entry in payload["sandbox_profile"]["workspace_entries"]
        )
        assert payload["sandbox_profile"]["permissions"] == {
            "network": "denied",
            "secrets": "none",
            "run_as": "sandbox_user",
        }
        assert payload["sandbox_profile"]["capabilities"] == {
            "filesystem": True,
            "memory": "read_write",
            "shell": "restricted",
            "skills": "read_only",
        }
        assert payload["sandbox_profile"]["state"] == {
            "persist_session_state": True,
            "resume": "allowed",
            "snapshot": "required_on_completion",
        }

    @pytest.mark.parametrize(
        ("command", "expected_missing"),
        [
            (
                ["check-change", "--signal", "offline_eval_passed=false"],
                "offline_eval_passed",
            ),
            (
                ["check-retirement", "--step", "revoke_egress=false"],
                "revoke_egress",
            ),
        ],
    )
    def test_cli_lifecycle_checks_report_missing_items(
        self,
        command: list[str],
        expected_missing: str,
        cli_json,
    ) -> None:
        exit_code, payload = cli_json(command)
        assert exit_code == 0
        assert not payload["ready"]
        missing = payload.get("missing_signals", payload.get("missing_steps", []))
        assert expected_missing in missing

    @pytest.mark.parametrize(
        ("command", "expected_message"),
        [
            (
                ["check-change", "--signal", "offline_eval_passed"],
                "Signal must use key=value format",
            ),
            (
                ["check-change", "--signal", "offline_eval_passed=maybe"],
                "Unsupported boolean value in signal",
            ),
            (
                ["check-retirement", "--step", "revoke_egress"],
                "Signal must use key=value format",
            ),
            (
                ["check-retirement", "--step", "revoke_egress=maybe"],
                "Unsupported boolean value in signal",
            ),
        ],
    )
    def test_cli_lifecycle_checks_reject_invalid_signal_values(
        self, command: list[str], expected_message: str
    ) -> None:
        from agent_runtime_ref.__main__ import main

        with pytest.raises(ValueError, match=expected_message):
            main(command)

    def test_cli_check_change_surfaces_failed_run_specific_missing_signals(
        self,
        cli_json,
    ) -> None:
        exit_code, payload = cli_json(
            ["check-change", "--signal", "failed_run_drill_checked=false"]
        )
        assert exit_code == 0
        assert set(payload) == {
            "change_id",
            "ready",
            "missing_signals",
            "missing_failed_run_signals",
            "rollout_strategy",
            "risk_level",
        }
        assert payload["change_id"] == "chg-2026-04-07-support-runtime"
        assert not payload["ready"]
        assert payload["missing_signals"] == ["failed_run_drill_checked"]
        assert payload["missing_failed_run_signals"] == ["failed_run_drill_checked"]
        assert payload["rollout_strategy"] == "staged_canary"
        assert payload["risk_level"] == "high"

    def test_cli_check_controls_surfaces_failed_run_related_controls(
        self,
        cli_json,
    ) -> None:
        exit_code, payload = cli_json(["check-controls", "--signal", "policy_traces_present=false"])
        assert exit_code == 0
        assert set(payload) == {
            "healthy",
            "missing_controls",
            "failed_run_controls",
            "preserved_failed_run_controls",
            "failed_run_controls_healthy",
            "blocking_findings",
            "inventory_drift",
        }
        assert not payload["healthy"]
        assert payload["missing_controls"] == ["policy_traces_present"]
        assert payload["failed_run_controls"] == ["policy_traces_present"]
        assert payload["preserved_failed_run_controls"] == [
            "memory_provenance_enforced"
        ]
        assert payload["failed_run_controls_healthy"] is False
        assert payload["blocking_findings"] == []
        assert payload["inventory_drift"] == {
            "has_drift": False,
            "missing_from_catalog": [],
            "missing_from_inventory": [],
        }

    def test_cli_check_retirement_surfaces_failed_run_archive_targets(
        self,
        cli_json,
    ) -> None:
        exit_code, payload = cli_json(["check-retirement"])
        assert exit_code == 0
        assert set(payload) == {
            "system_id",
            "ready",
            "missing_steps",
            "failed_run_archive_targets",
            "replacement_mode",
        }
        assert payload["system_id"] == "support-triage-ref"
        assert payload["ready"] is True
        assert payload["missing_steps"] == []
        assert payload["failed_run_archive_targets"] == [
            "telemetry_jsonl",
            "session_exports",
            "approval_history",
        ]
        assert payload["replacement_mode"] == "staged_replacement"

    def test_cli_inspect_approvals_returns_pending_item(self, cli_json) -> None:
        exit_code, payload = cli_json(["inspect-approvals"])
        assert exit_code == 0
        assert set(payload) == {"trace_id", "session_id", "count", "approvals"}
        assert payload["trace_id"] == "trace-approval-001"
        assert payload["session_id"] == "session-approval-001"
        assert payload["count"] == len(payload["approvals"])
        assert payload["count"] >= 1
        approval = payload["approvals"][0]
        assert set(approval) == {
            "approval_id",
            "capability_name",
            "requested_by",
            "reviewer",
            "reason",
            "status",
            "capability_session_id",
            "capability_session_status",
            "authorization_mode",
            "delegated_principal_id",
            "delegated_scope",
        }
        assert approval["approval_id"] == "apr-001"
        assert approval["capability_name"] == "create_ticket"
        assert approval["requested_by"] == "user-42"
        assert approval["reviewer"] == "manager"
        assert approval["reason"] == "approver:manager"
        assert approval["status"] == "pending"
        assert approval["capability_session_id"] == "cap-session-001"
        assert approval["capability_session_status"] == "pending"
        assert approval["authorization_mode"] == "platform_owned"
        assert approval["delegated_principal_id"] == ""
        assert approval["delegated_scope"] == ""

    def test_cli_inspect_approvals_surfaces_delegated_auth_context(self, cli_json) -> None:
        exit_code, payload = cli_json(
            [
                "inspect-approvals",
                "--tenant-id",
                "tenant-acme",
                "--principal-id",
                "manager-1",
                "--session-id",
                "session-approval-authz-001",
                "--trace-id",
                "trace-approval-authz-001",
                "--agent-id",
                "support-triage-ref",
            ]
        )
        assert exit_code == 0
        assert payload["count"] >= 1
        approval = payload["approvals"][0]
        assert "authorization_mode" in approval
        assert "delegated_principal_id" in approval
        assert "delegated_scope" in approval

    def test_cli_approval_commands_normalize_lineage_ids(self, cli_json) -> None:
        exit_code, payload = cli_json(
            [
                "inspect-approvals",
                "--session-id",
                " session-approval-normalized-001 ",
                "--trace-id",
                " trace-approval-normalized-001 ",
            ]
        )
        assert exit_code == 0
        assert payload["session_id"] == "session-approval-normalized-001"
        assert payload["trace_id"] == "trace-approval-normalized-001"
        assert payload["approvals"][0]["capability_session_id"].startswith("cap-session-")

        resolve_code, resolve_payload = cli_json(
            [
                "resolve-approval",
                "--decision",
                "approved",
                "--session-id",
                " session-approval-normalized-002 ",
                "--trace-id",
                " trace-approval-normalized-002 ",
            ]
        )
        assert resolve_code == 0
        assert resolve_payload["status"] == "approved"
        assert resolve_payload["capability_session_id"].startswith("cap-session-")

    def test_cli_resolve_approval_marks_item_resolved(self, cli_json) -> None:
        exit_code, payload = cli_json(
            [
                "resolve-approval",
                "--decision",
                "approved",
                "--note",
                "manager approved demo request",
            ],
        )
        assert exit_code == 0
        assert set(payload) == {
            "approval_id",
            "status",
            "reviewer",
            "resolution_note",
            "capability_session_id",
            "capability_session_status",
            "authorization_mode",
            "delegated_principal_id",
            "delegated_scope",
        }
        assert payload["approval_id"] == "apr-001"
        assert payload["status"] == "approved"
        assert payload["reviewer"] == "manager"
        assert payload["resolution_note"] == "manager approved demo request"
        assert payload["capability_session_id"] == "cap-session-001"
        assert payload["capability_session_status"] == "approved"
        assert payload["authorization_mode"] == "platform_owned"
        assert payload["delegated_principal_id"] == ""
        assert payload["delegated_scope"] == ""

    def test_cli_resolve_approval_marks_item_rejected(self, cli_json) -> None:
        exit_code, payload = cli_json(
            [
                "resolve-approval",
                "--decision",
                "rejected",
                "--note",
                "manager rejected demo request",
            ],
        )
        assert exit_code == 0
        assert set(payload) == {
            "approval_id",
            "status",
            "reviewer",
            "resolution_note",
            "capability_session_id",
            "capability_session_status",
            "authorization_mode",
            "delegated_principal_id",
            "delegated_scope",
        }
        assert payload["approval_id"] == "apr-001"
        assert payload["status"] == "rejected"
        assert payload["reviewer"] == "manager"
        assert payload["resolution_note"] == "manager rejected demo request"
        assert payload["capability_session_id"] == "cap-session-001"
        assert payload["capability_session_status"] == "rejected"
        assert payload["authorization_mode"] == "platform_owned"
        assert payload["delegated_principal_id"] == ""
        assert payload["delegated_scope"] == ""

    def test_cli_resolve_approval_normalizes_approval_id(self, cli_json) -> None:
        exit_code, payload = cli_json(
            [
                "resolve-approval",
                "--approval-id",
                " apr-001 ",
                "--decision",
                "approved",
            ]
        )
        assert exit_code == 0
        assert payload["approval_id"] == "apr-001"
        assert payload["status"] == "approved"

    def test_cli_resolve_approval_rejects_unknown_approval_id(self) -> None:
        from agent_runtime_ref.__main__ import main

        with pytest.raises(ValueError, match="Approval request not found: apr-missing"):
            main(["resolve-approval", "--approval-id", "apr-missing"])

    def test_cli_resolve_approval_surfaces_delegated_auth_context(self, cli_json) -> None:
        exit_code, payload = cli_json(
            [
                "resolve-approval",
                "--decision",
                "approved",
                "--note",
                "manager approved delegated request",
            ],
        )
        assert exit_code == 0
        assert "authorization_mode" in payload
        assert "delegated_principal_id" in payload
        assert "delegated_scope" in payload

    @staticmethod
    def _assert_session_run_contract(run: dict[str, object]) -> None:
        assert set(run) == {
            "trace_id",
            "status",
            "user_input",
            "output_text",
            "failure_reason",
            "capability_session_id",
            "capability_session_status",
            "authorization_mode",
            "delegated_principal_id",
            "delegated_scope",
        }

    @staticmethod
    def _assert_session_summary_contract(summary: dict[str, object]) -> None:
        assert set(summary) == {
            "total_runs",
            "success_runs",
            "approval_wait_runs",
            "denied_runs",
            "failed_runs",
            "traceable_failed_runs",
            "latest_failure_reason",
            "latest_trace_id",
            "latest_status",
        }

    def test_cli_session_replay_runs_multiple_inputs(self, cli_json) -> None:
        exit_code, payload = cli_json(
            [
                "session-replay",
                "--user-input",
                "Please create a ticket for this onboarding issue.",
                "--user-input",
                "What language preference do you remember?",
            ],
        )
        assert exit_code == 0
        assert set(payload) == {"session_id", "run_count", "summary", "runs"}
        assert payload["session_id"] == "session-demo-001"
        assert payload["run_count"] == 2
        self._assert_session_summary_contract(payload["summary"])
        assert payload["summary"]["total_runs"] == 2
        assert payload["summary"]["approval_wait_runs"] == 1
        assert payload["summary"]["latest_trace_id"] == "trace-session-002"
        self._assert_session_run_contract(payload["runs"][0])
        self._assert_session_run_contract(payload["runs"][1])
        assert payload["runs"][0]["capability_session_id"].startswith("cap-session-")
        assert payload["runs"][0]["capability_session_status"] == "pending"
        assert payload["runs"][0]["authorization_mode"] == "platform_owned"
        assert payload["runs"][0]["delegated_principal_id"] == ""
        assert payload["runs"][0]["delegated_scope"] == ""
        assert payload["runs"][1]["trace_id"] == "trace-session-002"

    def test_cli_session_replay_surfaces_failed_run_fields(self, cli_json) -> None:
        exit_code, payload = cli_json(
            [
                "session-replay",
                "--user-input",
                "Please create a ticket for this issue.",
                "--simulate-failure",
                "tool_timeout",
                "--session-id",
                "session-replay-failure-001",
                "--trace-prefix",
                "trace-replay-failure",
            ],
        )
        assert exit_code == 0
        assert payload["summary"]["failed_runs"] == 1
        assert payload["summary"]["traceable_failed_runs"] == 1
        assert payload["summary"]["latest_failure_reason"] == "tool_timeout"
        self._assert_session_run_contract(payload["runs"][0])
        assert payload["runs"][0]["failure_reason"] == "tool_timeout"

    def test_cli_inspect_session_with_multiple_inputs_returns_both_runs(self, cli_json) -> None:
        exit_code, payload = cli_json(
            [
                "inspect-session",
                "--user-input",
                "Please create a ticket for this onboarding issue.",
                "--user-input",
                "What language preference do you remember?",
            ],
        )
        assert exit_code == 0
        assert set(payload) == {
            "session_id",
            "tenant_id",
            "principal_id",
            "trace_count",
            "latest_status",
            "summary",
            "runs",
        }
        assert payload["session_id"] == "session-demo-001"
        assert payload["tenant_id"] == "tenant-acme"
        assert payload["principal_id"] == "user-42"
        assert payload["trace_count"] == 2
        assert payload["latest_status"] == "success"
        self._assert_session_summary_contract(payload["summary"])
        assert payload["summary"]["total_runs"] == 2
        self._assert_session_run_contract(payload["runs"][0])
        self._assert_session_run_contract(payload["runs"][1])
        assert "waiting for human approval" in payload["runs"][0]["output_text"]
        assert payload["runs"][0]["capability_session_id"].startswith("cap-session-")
        assert payload["runs"][0]["capability_session_status"] == "pending"
        assert payload["runs"][0]["authorization_mode"] == "platform_owned"
        assert payload["runs"][0]["delegated_principal_id"] == ""
        assert payload["runs"][0]["delegated_scope"] == ""
        assert "Retrieved profile hint" in payload["runs"][1]["output_text"]

    def test_cli_inspect_session_surfaces_failed_run_fields(self, cli_json) -> None:
        exit_code, payload = cli_json(
            [
                "inspect-session",
                "--user-input",
                "Please create a ticket for this issue.",
                "--simulate-failure",
                "tool_timeout",
                "--session-id",
                "session-inspect-failure-001",
                "--trace-prefix",
                "trace-inspect-failure",
            ],
        )
        assert exit_code == 0
        assert payload["summary"]["failed_runs"] == 1
        assert payload["summary"]["traceable_failed_runs"] == 1
        assert payload["summary"]["latest_failure_reason"] == "tool_timeout"
        self._assert_session_run_contract(payload["runs"][0])
        assert payload["runs"][0]["failure_reason"] == "tool_timeout"

    def test_cli_export_session_writes_structured_json(
        self,
        cli_json,
        tmp_path: Path,
    ) -> None:
        output_path = tmp_path / "session.json"
        exit_code, payload = cli_json(
            [
                "export-session",
                "--output",
                str(output_path),
            ],
        )
        assert exit_code == 0
        assert output_path.exists()
        assert set(payload) == {
            "session_id",
            "output_path",
            "total_runs",
            "failed_runs",
            "traceable_failed_runs",
            "latest_failure_reason",
            "latest_trace_id",
        }
        assert payload["session_id"] == "session-demo-001"
        assert payload["output_path"] == str(output_path)
        assert payload["total_runs"] == 2
        exported = json.loads(output_path.read_text(encoding="utf-8"))
        assert set(exported) == {"session", "summary", "runs"}
        assert exported["session"] == {
            "session_id": "session-demo-001",
            "tenant_id": "tenant-acme",
            "principal_id": "user-42",
            "traces": ["trace-session-001", "trace-session-002"],
        }
        assert set(exported["summary"]) == {
            "total_runs",
            "success_runs",
            "approval_wait_runs",
            "denied_runs",
            "failed_runs",
            "traceable_failed_runs",
            "latest_trace_id",
            "latest_status",
        }
        assert exported["summary"]["total_runs"] == 2
        assert len(exported["runs"]) == 2
        self._assert_session_run_contract(exported["runs"][0])
        self._assert_session_run_contract(exported["runs"][1])

    def test_cli_export_session_surfaces_latest_failure_reason(
        self,
        cli_json,
        tmp_path: Path,
    ) -> None:
        output_path = tmp_path / "failed-session.json"
        exit_code, payload = cli_json(
            [
                "export-session",
                "--user-input",
                "Please create a ticket for this issue.",
                "--simulate-failure",
                "tool_timeout",
                "--output",
                str(output_path),
            ],
        )
        assert exit_code == 0
        assert set(payload) == {
            "session_id",
            "output_path",
            "total_runs",
            "failed_runs",
            "traceable_failed_runs",
            "latest_failure_reason",
            "latest_trace_id",
        }
        assert payload["output_path"] == str(output_path)
        assert payload["failed_runs"] == 1
        assert payload["traceable_failed_runs"] == 1
        assert payload["latest_failure_reason"] == "tool_timeout"
        exported = json.loads(output_path.read_text(encoding="utf-8"))
        assert exported["summary"]["failed_runs"] == 1
        assert exported["runs"][0]["failure_reason"] == "tool_timeout"

    def test_cli_export_eval_dataset_writes_multi_session_json(
        self,
        cli_json,
        tmp_path: Path,
    ) -> None:
        output_path = tmp_path / "eval-dataset.json"
        exit_code, payload = cli_json(
            [
                "export-eval-dataset",
                "--output",
                str(output_path),
            ],
        )
        assert exit_code == 0
        assert output_path.exists()
        assert set(payload) == {
            "dataset_name",
            "output_path",
            "session_count",
            "run_count",
            "failed_runs",
            "traceable_failed_runs",
            "latest_failure_reason",
            "sessions",
        }
        assert payload["dataset_name"] == "agent-runtime-ref-eval-seed"
        assert payload["output_path"] == str(output_path)
        assert payload["session_count"] == 4
        assert payload["run_count"] == 5
        assert payload["failed_runs"] == 1
        assert payload["traceable_failed_runs"] == 1
        assert payload["latest_failure_reason"] == "tool_timeout"
        assert payload["sessions"] == [
            "session-eval-support",
            "session-eval-memory",
            "session-eval-mixed",
            "session-eval-failed-run",
        ]
        exported = json.loads(output_path.read_text(encoding="utf-8"))
        assert set(exported) == {"dataset_name", "session_count", "run_count", "sessions"}
        assert exported["dataset_name"] == "agent-runtime-ref-eval-seed"
        assert exported["session_count"] == 4
        assert exported["run_count"] == 5
        assert len(exported["sessions"]) == 4
        assert exported["sessions"][0]["eval"]["labels"]
        assert set(exported["sessions"][0]["eval"]) == {
            "scenario",
            "labels",
            "expected_outcomes",
            "grading_rules",
        }
        mixed_session = next(
            session
            for session in exported["sessions"]
            if session["session"]["session_id"] == "session-eval-mixed"
        )
        assert "required_run_count" not in mixed_session["eval"]["labels"]
        assert mixed_session["eval"]["expected_outcomes"]["required_run_count"] == 2
        assert any(
            session["summary"]["approval_wait_runs"] >= 1 for session in exported["sessions"]
        )
        assert any(session["summary"]["total_runs"] >= 2 for session in exported["sessions"])
