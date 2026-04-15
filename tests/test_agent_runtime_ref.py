from __future__ import annotations

import json
from pathlib import Path

import pytest

from agent_runtime_ref.config import (
    load_agent_profile,
    load_capability_catalog,
    load_controls_policy,
    load_memory_store,
    load_policy_engine,
    load_rollout_policy,
)
from agent_runtime_ref.controls import assess_controls, assess_inventory_drift
from agent_runtime_ref.execution import execute_tool
from agent_runtime_ref.lifecycle import assess_change_gate, assess_retirement
from agent_runtime_ref.memory import MemoryStore
from agent_runtime_ref.models import RunContext, RunRequest, ToolRequest
from agent_runtime_ref.policy import CapabilityPolicy, PolicyDecision, PolicyEngine
from agent_runtime_ref.rollout import RolloutReadiness, assess_rollout, ready_for_rollout
from agent_runtime_ref.runtime import AgentRuntime


class TestFailurePaths:
    def test_config_loader_rejects_non_mapping_yaml(self, tmp_path: Path) -> None:
        from agent_runtime_ref.config import load_yaml_file

        bad_config = tmp_path / "bad.yaml"
        bad_config.write_text("- not\n- a\n- mapping\n", encoding="utf-8")

        with pytest.raises(TypeError, match="must be a mapping"):
            load_yaml_file(bad_config)

    def test_runtime_denied_precheck_returns_denied_and_no_session_record(self) -> None:
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
        assert runtime.sessions.get_session("session-denied-001") is None
        event_types = [event.event_type for event in runtime.telemetry.events]
        assert event_types == ["run_start", "policy_precheck", "run_complete"]

    def test_cli_inspect_trace_requires_trace_id_for_multi_trace_file(self, cli_json, tmp_path: Path) -> None:
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
        merged.write_text(first.read_text(encoding="utf-8") + second.read_text(encoding="utf-8"), encoding="utf-8")

        from agent_runtime_ref.__main__ import main

        with pytest.raises(ValueError, match="multiple trace IDs"):
            main(["inspect-trace", "--input", str(merged)])

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
            main([
                "replay-run",
                "--input",
                str(output_path),
                "--trace-id",
                "trace-does-not-exist",
            ])


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

    def test_execute_tool_returns_validation_failure_without_idempotency_key(self, config_dir: Path) -> None:
        capability = load_capability_catalog(config_dir / "capabilities.yaml").get("create_ticket")
        assert capability is not None
        result = execute_tool(
            capability,
            ToolRequest(capability_name="create_ticket", arguments={"title": "x"}),
            PolicyDecision("allow", "approved_write", "cap_202"),
        )
        assert result.status == "validation_failure"
        assert result.payload["reason"] == "missing_idempotency_key"

    def test_execute_tool_success_includes_contract_payload(self, config_dir: Path) -> None:
        capability = load_capability_catalog(config_dir / "capabilities.yaml").get("search_docs")
        assert capability is not None
        result = execute_tool(
            capability,
            ToolRequest(capability_name="search_docs", arguments={"query": "architecture"}),
            PolicyDecision("allow", "low_risk_read", "cap_101"),
        )
        assert result.status == "success"
        assert result.payload["transport"] == capability.transport
        assert result.payload["tool_principal"] == capability.tool_principal

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
        context = RunContext(tenant_id="tenant-acme", principal_id="user-1", trace_id="trace-pol-001")
        allow_engine = PolicyEngine(capability_policies={"search_docs": CapabilityPolicy("allow")})
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

        engine = PolicyEngine(allowed_network_access={"restricted"})
        context = RunContext(tenant_id="tenant-acme", principal_id="user-1", trace_id="trace-pol-002")
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
            name="write_tool",
            owner="platform",
            mode="write",
            transport="gateway",
            timeout_seconds=5,
            tool_principal="svc-write",
            risk_tier="medium",
            network_access="restricted",
            allowed_egress=("internal",),
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

    def test_policy_allow_memory_write_denies_unknown_kind(self) -> None:
        decision = PolicyEngine(allowed_memory_kinds={"profile"}).allow_memory_write("session_summary")
        assert decision.action == "deny"
        assert decision.reason == "memory_kind_denied"


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
            event
            for event in runtime.telemetry.events
            if event.event_type == "memory_persisted"
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
        records = store.retrieve("language preference", "tenant-acme", limit=5)
        assert records
        assert all(record.tenant_id == "tenant-acme" for record in records)
        assert all(record.provenance for record in records)


class TestRuntimeControlPaths:
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
        queue = AgentRuntime().approvals
        request = queue.submit(
            trace_id="trace-approval-resolve-001",
            capability_name="create_ticket",
            requested_by="user-1",
            reviewer=None,
            reason="write_action",
            session_id="session-approval-resolve-001",
        )
        resolved = queue.resolve(request.approval_id, decision="approved", note="ok")
        assert resolved.status == "approved"
        assert resolved.capability_session_status == "approved"

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
        runtime.sessions.export_session_json(session_id, output_path=output_path)
        payload = json.loads(output_path.read_text(encoding="utf-8"))
        assert payload["runs"][0]["capability_session_id"].startswith("cap-session-")
        assert payload["runs"][0]["capability_session_status"] == "pending"

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
        assert not payload["ready"]
        assert "expire_paused_runs" in payload["missing_steps"]
        assert "stop_background_routes" in payload["missing_steps"]

    def test_cli_check_change_accepts_runtime_control_signal_contract(self, cli_json) -> None:
        exit_code, payload = cli_json([
            "check-change",
            "--signal",
            "offline_eval_passed=true",
        ])
        assert exit_code == 0
        assert "ready" in payload
        assert "rollout_strategy" in payload


class TestMeaningfulMemoryAndLifecycleCoverage:
    def test_memory_store_from_dict_rejects_bad_shapes(self) -> None:
        from agent_runtime_ref.memory import MemoryStore

        with pytest.raises(TypeError, match="'memory' must be a mapping"):
            MemoryStore.from_dict({"memory": []})
        with pytest.raises(TypeError, match="'seed_records' must be a list"):
            MemoryStore.from_dict({"memory": {"seed_records": "x"}})
        with pytest.raises(TypeError, match="Memory record #1 must be a mapping"):
            MemoryStore.from_dict({"memory": {"seed_records": ["x"]}})

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
                revision_mode="replace",
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
        removed = store.compact("tenant-acme")
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
        assert MemoryStore._score(high, {"language", "preference"}) > MemoryStore._score(low, {"language", "preference"})

    def test_lifecycle_helpers_reject_bad_shapes(self) -> None:
        from agent_runtime_ref.lifecycle import ArtifactBundle, ChangeRecord, RetirementPlan

        with pytest.raises(TypeError, match="change config must be a mapping"):
            ChangeRecord.from_dict({"change": []})
        with pytest.raises(TypeError, match="artifact bundle config must be a mapping"):
            ArtifactBundle.from_dict({"bundle": []})
        with pytest.raises(TypeError, match="retirement config must be a mapping"):
            RetirementPlan.from_dict({"retirement": []})
        with pytest.raises(TypeError, match="artifacts must be a list"):
            ChangeRecord.from_dict({"change": {"change_id": "x", "change_type": "y", "risk_level": "z", "rollout_strategy": "gradual", "artifacts": "bad", "required_signals": [], "approval_roles": []}})

    def test_lifecycle_assessments_report_ready_when_complete(self, config_dir: Path) -> None:
        from agent_runtime_ref.config import load_change_record, load_retirement_plan

        change = load_change_record(config_dir / "change.yaml")
        change_assessment = assess_change_gate(
            change,
            {signal: True for signal in change.required_signals},
        )
        assert change_assessment.ready
        assert change_assessment.missing_signals == ()

        plan = load_retirement_plan(config_dir / "retirement.yaml")
        retirement_assessment = assess_retirement(
            plan,
            {step: True for step in plan.required_steps},
        )
        assert retirement_assessment.ready
        assert retirement_assessment.missing_steps == ()


class TestLowCoverageModuleBranches:
    def test_controls_policy_from_dict_rejects_bad_shapes(self) -> None:
        from agent_runtime_ref.controls import ControlsPolicy

        with pytest.raises(TypeError, match="'controls' must be a mapping"):
            ControlsPolicy.from_dict({"controls": []})
        with pytest.raises(TypeError, match="'controls.require' must be a list"):
            ControlsPolicy.from_dict({"controls": {"require": "x"}})
        with pytest.raises(TypeError, match="'controls.block_if' must be a list"):
            ControlsPolicy.from_dict({"controls": {"require": [], "block_if": "x"}})

    def test_assess_controls_marks_inventory_drift_as_blocking(self) -> None:
        from agent_runtime_ref.controls import ControlsPolicy, InventoryDrift, assess_controls

        assessment = assess_controls(
            ControlsPolicy(required_controls=("registry_reviewed",), blocked_findings=("manual_override",)),
            {"registry_reviewed": True, "manual_override": False},
            inventory_drift=InventoryDrift(
                missing_from_catalog=("ghost_cap",),
                missing_from_inventory=(),
            ),
        )
        assert not assessment.healthy
        assert "inventory_drift_present" in assessment.blocking_findings

    def test_structured_event_from_dict_rejects_bad_shapes(self) -> None:
        from agent_runtime_ref.telemetry import StructuredEvent

        with pytest.raises(TypeError, match="payload must be a mapping"):
            StructuredEvent.from_dict({"event_type": "x", "trace_id": "t", "payload": []})
        with pytest.raises(TypeError, match="redacted_fields must be a list"):
            StructuredEvent.from_dict({"event_type": "x", "trace_id": "t", "payload": {}, "redacted_fields": "x"})

    def test_telemetry_events_for_trace_and_unredacted_export(self, tmp_path: Path) -> None:
        from agent_runtime_ref.telemetry import TelemetryEmitter

        emitter = TelemetryEmitter()
        emitter.emit("run_start", "trace-a", user_input="hello")
        emitter.emit("run_complete", "trace-b", status="success")
        assert len(emitter.events_for_trace("trace-a")) == 1

        output_path = tmp_path / "events.jsonl"
        emitter.export_jsonl(output_path)
        loaded = TelemetryEmitter.load_jsonl(output_path)
        assert len(loaded) == 2
        assert loaded[0].payload["user_input"] == "hello"

    def test_traced_call_emits_failure_span(self) -> None:
        from agent_runtime_ref.telemetry import TelemetryEmitter

        emitter = TelemetryEmitter()
        with pytest.raises(RuntimeError, match="boom"):
            emitter.traced_call("trace-fail", "failing_span", lambda: (_ for _ in ()).throw(RuntimeError("boom")))
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
            RolloutPolicy.from_dict({"rollout": {"require": [], "block_if": [], "rollout_mode": []}})

    def test_ready_for_rollout_false_when_flags_missing(self) -> None:
        assert not ready_for_rollout(
            RolloutReadiness(
                trace_coverage=True,
                offline_eval_pass=True,
                slo_defined=False,
                rollback_plan=True,
            ),
        )

    def test_identity_loaders_reject_bad_shapes_and_allow_lookup(self) -> None:
        from agent_runtime_ref.identity import ApprovedInventory, load_agent_identity

        with pytest.raises(TypeError, match="'agent' must be a mapping"):
            ApprovedInventory.from_agent_config({"agent": []})
        with pytest.raises(TypeError, match="'approved_capabilities' must be a list"):
            ApprovedInventory.from_agent_config({"agent": {"approved_capabilities": "x"}})
        with pytest.raises(TypeError, match="'agent' must be a mapping"):
            load_agent_identity({"agent": []})

        inventory = ApprovedInventory(capabilities=frozenset({"search_docs"}))
        assert inventory.allows("search_docs")
        assert not inventory.allows("create_ticket")


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
        assessment = assess_rollout(
            policy,
            {
                "trace_coverage": True,
                "policy_prechecks": True,
                "capability_owners": True,
                "offline_eval_pass": True,
                "slo_defined": True,
                "rollback_plan": True,
                "oncall_owner": True,
                "direct_tool_access_present": True,
            },
        )
        assert not assessment.ready
        assert "direct_tool_access_present" in assessment.blocking_signals

    def test_controls_policy_detects_inventory_drift(self, config_dir: Path) -> None:
        policy = load_controls_policy(config_dir / "controls.yaml")
        catalog = load_capability_catalog(config_dir / "capabilities.yaml")
        _, approved_inventory = load_agent_profile(config_dir / "agent.yaml")
        drift = assess_inventory_drift(approved_inventory, catalog)
        assessment = assess_controls(
            policy,
            {
                "registry_reviewed": True,
                "capability_owners_confirmed": True,
                "memory_provenance_enforced": True,
                "policy_traces_present": True,
                "direct_tool_access_present": False,
                "unmanaged_runtime_present": False,
            },
            inventory_drift=drift,
        )
        assert assessment.healthy
        assert not assessment.inventory_drift.has_drift


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
        assert assessment.missing_signals == ("offline_eval_passed",)

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
        assert assessment.missing_steps == ("revoke_egress",)


class TestCli:
    def test_cli_simulate_run_returns_json(self, cli_json) -> None:
        exit_code, payload = cli_json([])
        assert exit_code == 0
        assert payload["agent_id"] == "support-triage-ref"
        assert payload["session_id"] == "session-demo-001"
        assert payload["status"] == "success"
        assert payload["events"] >= 1
        assert payload["memory_records"] >= 3
        assert payload["pending_approvals"] >= 1

    def test_cli_inspect_memory_filters_records(self, cli_json) -> None:
        exit_code, payload = cli_json(["inspect-memory", "--memory-class", "profile"])
        assert exit_code == 0
        assert payload["count"] >= 1
        assert all(item["memory_class"] == "profile" for item in payload["records"])
        assert all("provenance" in item for item in payload["records"])
        assert all("revision" in item for item in payload["records"])

    def test_cli_inspect_agent_returns_identity_and_inventory(self, cli_json) -> None:
        exit_code, payload = cli_json(["inspect-agent"])
        assert exit_code == 0
        assert payload["agent_id"] == "support-triage-ref"
        assert "create_ticket" in payload["approved_capabilities"]
        assert any(item["name"] == "search_docs" for item in payload["catalog_capabilities"])
        assert any(item["risk_tier"] == "high" for item in payload["catalog_capabilities"])

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
        assert output_path.exists()
        assert export_payload["trace_id"] == "trace-export-001"

        inspect_code, inspect_payload = cli_json(
            [
                "inspect-trace",
                "--input",
                str(output_path),
            ],
        )
        assert inspect_code == 0
        assert inspect_payload["trace_id"] == "trace-export-001"
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
                "user_input",
            ],
        )
        assert export_code == 0
        assert export_payload["redact_fields"] == ["user_input"]

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

    def test_cli_export_trace_preserves_runtime_control_event_order(self, cli_json, tmp_path: Path) -> None:
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
        assert "tool_execution" in event_types
        assert event_types.index("approval_requested") < event_types.index("tool_execution") < event_types.index("run_complete")

    def test_cli_export_trace_keeps_single_trace_and_session_consistent(self, cli_json, tmp_path: Path) -> None:
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
        assert replay_payload["source_trace_id"] == "trace-replay-source"
        assert replay_payload["replay_trace_id"] == "trace-replay-target"
        assert replay_payload["status"] == "success"

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
        assert not payload["ready"]
        assert "offline_eval_pass" in payload["missing_required"]

    def test_cli_check_controls_reports_control_failure(self, cli_json) -> None:
        exit_code, payload = cli_json(
            [
                "check-controls",
                "--signal",
                "registry_reviewed=false",
            ],
        )
        assert exit_code == 0
        assert not payload["healthy"]
        assert "registry_reviewed" in payload["missing_controls"]
        assert not payload["inventory_drift"]["has_drift"]

    def test_cli_inspect_lifecycle_returns_all_artifacts(self, cli_json) -> None:
        exit_code, payload = cli_json(["inspect-lifecycle"])
        assert exit_code == 0
        assert payload["change"]["change_id"] == "chg-2026-04-07-support-runtime"
        assert payload["artifact_bundle"]["bundle_name"] == "support-triage-runtime-bundle"
        assert "runtime-controls.yaml" in payload["artifact_bundle"]["artifacts"]
        assert payload["retirement"]["system_id"] == "support-triage-ref"
        assert "expire_paused_runs" in payload["retirement"]["required_steps"]
        assert "stop_background_routes" in payload["retirement"]["required_steps"]

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

    def test_cli_inspect_approvals_returns_pending_item(self, cli_json) -> None:
        exit_code, payload = cli_json(["inspect-approvals"])
        assert exit_code == 0
        assert payload["count"] >= 1
        assert payload["approvals"][0]["status"] == "pending"

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
        assert payload["status"] == "approved"
        assert payload["resolution_note"] == "manager approved demo request"

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
        assert payload["run_count"] == 2
        assert payload["summary"]["total_runs"] == 2
        assert payload["summary"]["approval_wait_runs"] == 1
        assert payload["summary"]["latest_trace_id"] == "trace-session-002"
        assert payload["runs"][1]["trace_id"] == "trace-session-002"

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
        assert payload["trace_count"] == 2
        assert payload["summary"]["total_runs"] == 2
        assert "waiting for human approval" in payload["runs"][0]["output_text"]
        assert "Retrieved profile hint" in payload["runs"][1]["output_text"]

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
        assert payload["session_id"] == "session-demo-001"
        assert payload["total_runs"] == 2
        exported = json.loads(output_path.read_text(encoding="utf-8"))
        assert exported["summary"]["total_runs"] == 2
        assert len(exported["runs"]) == 2

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
        assert payload["dataset_name"] == "agent-runtime-ref-eval-seed"
        assert payload["session_count"] == 3
        assert payload["run_count"] == 4
        exported = json.loads(output_path.read_text(encoding="utf-8"))
        assert exported["dataset_name"] == "agent-runtime-ref-eval-seed"
        assert exported["session_count"] == 3
        assert exported["run_count"] == 4
        assert len(exported["sessions"]) == 3
        assert exported["sessions"][0]["eval"]["labels"]
        assert "expected_outcomes" in exported["sessions"][0]["eval"]
        assert any(
            session["summary"]["approval_wait_runs"] >= 1
            for session in exported["sessions"]
        )
        assert any(
            session["summary"]["total_runs"] >= 2
            for session in exported["sessions"]
        )
