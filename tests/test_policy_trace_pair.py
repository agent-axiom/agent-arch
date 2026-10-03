from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path
from unittest.mock import Mock

import pytest
import yaml

from agent_runtime_ref import execution
from agent_runtime_ref import runtime as runtime_module
from agent_runtime_ref.telemetry import TelemetryEmitter

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "agent_runtime_ref/configs"


def _config_bytes(path: Path) -> dict[str, bytes]:
    return {
        str(file.relative_to(path)): file.read_bytes() for file in path.rglob("*") if file.is_file()
    }


def test_cli_exports_a_real_search_denial_and_a_successful_control(tmp_path: Path) -> None:
    output = tmp_path / "pair"
    completed = subprocess.run(
        [
            sys.executable,
            "docs/companion/examples/export_policy_trace_pair.py",
            "--output-dir",
            str(output),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    assert completed.stderr == ""
    summary = json.loads(completed.stdout)
    assert json.loads((output / "summary.json").read_text()) == summary

    for case, action, outcome, status in (
        ("deny", "deny", "permission_denied", "failed"),
        ("allow", "allow", "success", "success"),
    ):
        observed = summary[case]
        events = TelemetryEmitter.load_jsonl(output / observed["events_file"])
        policy = next(event for event in events if event.event_type == "tool_policy_decision")
        tool = next(event for event in events if event.event_type == "tool_execution")
        completion = next(event for event in events if event.event_type == "run_complete")
        assert policy.payload["capability"] == tool.payload["capability"] == "search_docs"
        assert policy.payload["action"] == action
        assert tool.payload["outcome"] == outcome
        assert tool.payload["side_effect_status"] == "not_executed"
        assert completion.payload["status"] == status
        assert observed["policy"] == {
            key: policy.payload[key] for key in ("action", "reason", "policy_id")
        }
        assert observed["tool"] == {
            key: tool.payload[key] for key in ("outcome", "side_effect_status")
        }
        assert observed["run"]["status"] == status
        assert observed["run"]["side_effect_status"] == "not_executed"
        assert {event.trace_id for event in events} == {observed["trace_id"]}
        assert {
            event.payload["session_id"] for event in events if "session_id" in event.payload
        } == {observed["session_id"]}
        assert all(event.payload.get("capability") != "create_ticket" for event in events)

    assert summary["allow"]["trace_id"] != summary["deny"]["trace_id"]
    assert summary["allow"]["session_id"] != summary["deny"]["session_id"]
    assert summary["allow"]["run"]["task_success"] is True
    assert summary["deny"]["run"]["task_success"] is False
    assert summary["deny"]["policy"]["reason"] == "configured_deny"
    assert "search_docs" in summary["allow"]["run"]["output_text"]
    assert "Ticket" not in summary["allow"]["run"]["output_text"]


def test_denial_stops_before_synthetic_execution_but_allow_reaches_it(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from docs.companion.examples.export_policy_trace_pair import export_policy_trace_pair

    real_execute = runtime_module.execute_tool
    post_policy_spy = Mock(wraps=execution._fault_result)
    monkeypatch.setattr(execution, "_fault_result", post_policy_spy)
    calls = []

    def observe_execute(capability, request, decision, **kwargs):
        before = post_policy_spy.call_count
        result = real_execute(capability, request, decision, **kwargs)
        calls.append(
            {
                "capability": request.capability_name,
                "arguments": dict(request.arguments),
                "decision": decision.action,
                "outcome": result.outcome,
                "post_policy_calls": post_policy_spy.call_count - before,
            }
        )
        return result

    monkeypatch.setattr(runtime_module, "execute_tool", observe_execute)
    export_policy_trace_pair(tmp_path / "pair")

    # The executor includes the guard; its post-guard stage must never run on deny.
    assert calls == [
        {
            "capability": "search_docs",
            "arguments": {"query": "Find the onboarding policy."},
            "decision": "allow",
            "outcome": "success",
            "post_policy_calls": 1,
        },
        {
            "capability": "search_docs",
            "arguments": {"query": "Find the onboarding policy."},
            "decision": "deny",
            "outcome": "permission_denied",
            "post_policy_calls": 0,
        },
    ]
    post_policy_spy.assert_called_once_with("search_docs", "")


def test_only_copied_policy_decision_changes_and_source_bytes_are_preserved(
    tmp_path: Path,
) -> None:
    from docs.companion.examples.export_policy_trace_pair import export_policy_trace_pair

    source = shutil.copytree(CONFIG_DIR, tmp_path / "configs")
    before = _config_bytes(source)
    output = tmp_path / "pair"

    export_policy_trace_pair(output, config_dir=source)

    assert _config_bytes(source) == before
    copied = _config_bytes(output / "deny-config")
    assert copied.keys() == before.keys()
    for path in before:
        if path != "policy.yaml":
            assert copied[path] == before[path]
    policy = yaml.safe_load(copied["policy.yaml"])
    assert policy["policy"]["capabilities"]["search_docs"]["decision"] == "deny"
    policy["policy"]["capabilities"]["search_docs"]["decision"] = "allow"
    assert policy == yaml.safe_load(before["policy.yaml"])


def test_source_inventory_guard_is_not_overridden_to_force_success(tmp_path: Path) -> None:
    from docs.companion.examples.export_policy_trace_pair import export_policy_trace_pair

    source = shutil.copytree(CONFIG_DIR, tmp_path / "configs")
    agent_path = source / "agent.yaml"
    agent = yaml.safe_load(agent_path.read_text())
    agent["agent"]["approved_capabilities"].remove("search_docs")
    agent_path.write_text(yaml.safe_dump(agent))

    summary = export_policy_trace_pair(tmp_path / "pair", config_dir=source)

    for case in ("allow", "deny"):
        assert summary[case]["policy"]["action"] == "deny"
        assert summary[case]["policy"]["reason"] == "capability_not_in_inventory"
        assert summary[case]["tool"]["outcome"] == "permission_denied"
        assert summary[case]["run"]["status"] == "failed"


def test_export_does_not_overwrite_existing_evidence(tmp_path: Path) -> None:
    from docs.companion.examples.export_policy_trace_pair import export_policy_trace_pair

    output = tmp_path / "pair"
    output.mkdir()
    existing = output / "allow.jsonl"
    existing.write_text("previous evidence\n")

    with pytest.raises(FileExistsError, match="empty or absent"):
        export_policy_trace_pair(output)

    assert existing.read_text() == "previous evidence\n"
    assert set(output.iterdir()) == {existing}


def test_export_cannot_write_inside_source_configs(tmp_path: Path) -> None:
    from docs.companion.examples.export_policy_trace_pair import export_policy_trace_pair

    source = shutil.copytree(CONFIG_DIR, tmp_path / "configs")
    before = _config_bytes(source)

    with pytest.raises(ValueError, match="outside the source config"):
        export_policy_trace_pair(source / "pair", config_dir=source)

    assert _config_bytes(source) == before


def test_baseline_deny_is_not_silently_replaced_with_allow(tmp_path: Path) -> None:
    from docs.companion.examples.export_policy_trace_pair import export_policy_trace_pair

    source = shutil.copytree(CONFIG_DIR, tmp_path / "configs")
    path = source / "policy.yaml"
    policy = yaml.safe_load(path.read_text())
    policy["policy"]["capabilities"]["search_docs"]["decision"] = "deny"
    path.write_text(yaml.safe_dump(policy))
    before = _config_bytes(source)

    with pytest.raises(ValueError, match="Source search_docs decision must be allow"):
        export_policy_trace_pair(tmp_path / "pair", config_dir=source)

    assert _config_bytes(source) == before
    assert not (tmp_path / "pair").exists()
