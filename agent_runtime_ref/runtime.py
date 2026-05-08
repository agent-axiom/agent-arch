from __future__ import annotations

from typing import cast

from agent_runtime_ref.approvals import ApprovalQueue
from agent_runtime_ref.background import BackgroundWorker
from agent_runtime_ref.catalog import CapabilityCatalog
from agent_runtime_ref.execution import execute_tool, normalize_tool_capability_name
from agent_runtime_ref.identity import AgentIdentity
from agent_runtime_ref.memory import MemoryStore
from agent_runtime_ref.models import (
    ModelOutput,
    RunContext,
    RunRequest,
    RunResult,
    ToolRequest,
    ToolResult,
    normalize_tool_arguments,
)
from agent_runtime_ref.policy import PolicyDecision, PolicyEngine
from agent_runtime_ref.session import SessionStore
from agent_runtime_ref.telemetry import TelemetryEmitter


def _read_optional_request_string(value: str, *, field: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"Run request field must be a string: {field}")
    return value.strip()


def _read_required_request_string(value: str, *, field: str) -> str:
    normalized = _read_optional_request_string(value, field=field)
    if not normalized:
        raise ValueError(f"Run request field is required: {field}")
    return normalized


def _read_required_delegated_string(value: str, *, field: str) -> str:
    normalized = _read_optional_request_string(value, field=field)
    if not normalized:
        raise ValueError(f"Delegated authorization field is required: {field}")
    return normalized


def _read_authorization_mode(value: str) -> str:
    authorization_mode = _read_required_request_string(value, field="authorization_mode")
    if authorization_mode not in {"platform_owned", "user_delegated", "human_approved"}:
        raise ValueError(f"Authorization mode is not supported: {authorization_mode}")
    return authorization_mode


def _read_model_output(value: object) -> ModelOutput:
    if not isinstance(value, ModelOutput):
        raise TypeError("Model step must return ModelOutput")
    if not isinstance(value.text, str):
        raise TypeError("Model output text must be a string")
    if value.tool_request is not None and not isinstance(value.tool_request, ToolRequest):
        raise TypeError("Model output tool_request must be ToolRequest")
    return value


def _read_workspace_entries(workspace: dict[str, object]) -> list[object]:
    entries = workspace.get("entries", [])
    if not isinstance(entries, list):
        raise TypeError("Sandbox profile workspace entries must be a list")
    return cast(list[object], entries)


class AgentRuntime:
    """Minimal runnable skeleton for the book's reference implementation."""

    def __init__(
        self,
        catalog: CapabilityCatalog | None = None,
        policy: PolicyEngine | None = None,
        telemetry: TelemetryEmitter | None = None,
        memory: MemoryStore | None = None,
        background: BackgroundWorker | None = None,
        agent: AgentIdentity | None = None,
        approvals: ApprovalQueue | None = None,
        sessions: SessionStore | None = None,
        sandbox_profile: dict[str, object] | None = None,
    ) -> None:
        if catalog is None:
            catalog = CapabilityCatalog()
        if not isinstance(catalog, CapabilityCatalog):
            raise TypeError("Runtime catalog must be CapabilityCatalog")
        self.catalog = catalog
        if policy is None:
            policy = PolicyEngine()
        if not isinstance(policy, PolicyEngine):
            raise TypeError("Runtime policy must be PolicyEngine")
        self.policy = policy
        if telemetry is None:
            telemetry = TelemetryEmitter()
        if not isinstance(telemetry, TelemetryEmitter):
            raise TypeError("Runtime telemetry must be TelemetryEmitter")
        self.telemetry = telemetry
        if memory is None:
            memory = MemoryStore()
        if not isinstance(memory, MemoryStore):
            raise TypeError("Runtime memory must be MemoryStore")
        self.memory = memory
        if approvals is None:
            approvals = ApprovalQueue()
        if not isinstance(approvals, ApprovalQueue):
            raise TypeError("Runtime approvals must be ApprovalQueue")
        self.approvals = approvals
        if sessions is None:
            sessions = SessionStore()
        if not isinstance(sessions, SessionStore):
            raise TypeError("Runtime sessions must be SessionStore")
        self.sessions = sessions
        if sandbox_profile is None:
            sandbox_profile = {}
        if not isinstance(sandbox_profile, dict):
            raise TypeError("Sandbox profile config must be a mapping")
        self.sandbox_profile = sandbox_profile
        if agent is None:
            agent = AgentIdentity(
                agent_id="agent-runtime-ref",
                display_name="Reference Runtime",
                owner_team="agent_platform",
                runtime_principal="svc-agent-runtime-ref",
            )
        if not isinstance(agent, AgentIdentity):
            raise TypeError("Runtime agent must be AgentIdentity")
        self.agent = agent
        if background is None:
            background = BackgroundWorker(
                memory_store=self.memory,
                policy=self.policy,
                telemetry=self.telemetry,
            )
        if not isinstance(background, BackgroundWorker):
            raise TypeError("Runtime background must be BackgroundWorker")
        self.background = background

    def run(self, request: RunRequest) -> RunResult:
        if not isinstance(request, RunRequest):
            raise TypeError("Runtime request must be RunRequest")
        request.user_input = _read_required_request_string(
            request.user_input,
            field="user_input",
        )
        request.tenant_id = _read_optional_request_string(
            request.tenant_id,
            field="tenant_id",
        )
        request.principal_id = _read_optional_request_string(
            request.principal_id,
            field="principal_id",
        )
        request.trace_id = _read_required_request_string(
            request.trace_id,
            field="trace_id",
        )
        request.session_id = _read_required_request_string(
            request.session_id,
            field="session_id",
        )
        request.agent_id = _read_optional_request_string(request.agent_id, field="agent_id")
        request.authorization_mode = _read_authorization_mode(request.authorization_mode)
        request.delegated_principal_id = _read_optional_request_string(
            request.delegated_principal_id,
            field="delegated_principal_id",
        )
        request.delegated_scope = _read_optional_request_string(
            request.delegated_scope,
            field="delegated_scope",
        )
        if request.authorization_mode == "user_delegated":
            request.delegated_principal_id = _read_required_delegated_string(
                request.delegated_principal_id,
                field="delegated_principal_id",
            )
            request.delegated_scope = _read_required_delegated_string(
                request.delegated_scope,
                field="delegated_scope",
            )
        capability_session_id = ""
        capability_session_status = ""
        authorization_mode = request.authorization_mode
        delegated_principal_id = request.delegated_principal_id
        delegated_scope = request.delegated_scope
        idempotency_key = ""
        approval_id = ""
        self.telemetry.emit(
            "run_start",
            request.trace_id,
            user_input=request.user_input,
            tenant_id=request.tenant_id,
            principal_id=request.principal_id,
            session_id=request.session_id,
            agent_id=request.agent_id,
            runtime_principal=self.agent.runtime_principal,
            authorization_mode=authorization_mode,
            delegated_principal_id=delegated_principal_id,
            delegated_scope=delegated_scope,
        )
        precheck = self.policy.precheck(request)
        self.telemetry.emit(
            "policy_precheck",
            request.trace_id,
            action=precheck.action,
            reason=precheck.reason,
            policy_id=precheck.policy_id,
            agent_id=request.agent_id,
            session_id=request.session_id,
        )
        if precheck.action != "allow":
            result = RunResult(output_text="Request denied by policy.", status="denied")
            self.sessions.register_run(
                session_id=request.session_id,
                tenant_id=request.tenant_id,
                principal_id=request.principal_id,
                trace_id=request.trace_id,
                status=result.status,
                user_input=request.user_input,
                output_text=result.output_text,
                failure_reason=precheck.reason,
                authorization_mode=authorization_mode,
                delegated_principal_id=delegated_principal_id,
                delegated_scope=delegated_scope,
            )
            self.telemetry.emit(
                "run_complete",
                request.trace_id,
                session_id=request.session_id,
                status=result.status,
                output_preview=result.output_text[:80],
                authorization_mode=authorization_mode,
                delegated_principal_id=delegated_principal_id,
                delegated_scope=delegated_scope,
            )
            return result

        context = RunContext(
            tenant_id=request.tenant_id,
            principal_id=request.principal_id,
            trace_id=request.trace_id,
            session_id=request.session_id,
            agent=self.agent,
        )
        context.retrieved_records = self.memory.retrieve(
            request.user_input,
            request.tenant_id,
            limit=3,
        )
        context.retrieved_context = self._retrieve_context(context, request)
        self.telemetry.emit(
            "context_layers_built",
            request.trace_id,
            session_id=request.session_id,
            static_items=str(len(context.context_layers.get("static", []))),
            session_items=str(len(context.context_layers.get("session", []))),
            retrieved_items=str(len(context.context_layers.get("retrieved", []))),
            tool_items=str(len(context.context_layers.get("tool", []))),
        )

        model_output = cast(
            ModelOutput,
            self.telemetry.traced_call(
                request.trace_id,
                "model_step",
                lambda: _read_model_output(self._call_model(request, context)),
            ),
        )

        if model_output.tool_request is not None:
            self._handle_tool_request(context, request, model_output.tool_request)
            latest_tool = context.tool_results[-1] if context.tool_results else None
            if latest_tool is not None:
                capability_session_id = latest_tool.payload.get("capability_session_id", "")
                capability_session_status = latest_tool.payload.get(
                    "capability_session_status", latest_tool.status
                )
                authorization_mode = latest_tool.payload.get(
                    "authorization_mode", authorization_mode
                )
                delegated_principal_id = latest_tool.payload.get(
                    "delegated_principal_id", delegated_principal_id
                )
                delegated_scope = latest_tool.payload.get("delegated_scope", delegated_scope)
                idempotency_key = latest_tool.payload.get("idempotency_key", idempotency_key)
                approval_id = latest_tool.payload.get("approval_id", approval_id)
                if latest_tool.status in {"denied", "validation_failure", "failed"}:
                    failure_reason = latest_tool.payload.get("reason", latest_tool.status)
                    result = RunResult(
                        output_text=(
                            "Runtime halted before side effects completed: "
                            f"{latest_tool.capability_name} returned {latest_tool.status} "
                            f"({failure_reason})."
                        ),
                        status="failed",
                    )
                    self.sessions.register_run(
                        session_id=request.session_id,
                        tenant_id=request.tenant_id,
                        principal_id=request.principal_id,
                        trace_id=request.trace_id,
                        status=result.status,
                        user_input=request.user_input,
                        output_text=result.output_text,
                        failure_reason=str(failure_reason),
                        capability_session_id=capability_session_id,
                        capability_session_status=capability_session_status,
                        authorization_mode=authorization_mode,
                        delegated_principal_id=delegated_principal_id,
                        delegated_scope=delegated_scope,
                        idempotency_key=idempotency_key,
                        approval_id=approval_id,
                    )
                    self.telemetry.emit(
                        "run_failed",
                        request.trace_id,
                        session_id=request.session_id,
                        capability=latest_tool.capability_name,
                        tool_status=latest_tool.status,
                        authorization_mode=authorization_mode,
                        delegated_principal_id=delegated_principal_id,
                        delegated_scope=delegated_scope,
                        idempotency_key=idempotency_key,
                    )
                    self.telemetry.emit(
                        "run_complete",
                        request.trace_id,
                        session_id=request.session_id,
                        status=result.status,
                        output_preview=result.output_text[:80],
                        authorization_mode=authorization_mode,
                        delegated_principal_id=delegated_principal_id,
                        delegated_scope=delegated_scope,
                    )
                    return result
            model_output = _read_model_output(
                self._call_model(request, context, second_pass=True)
            )

        self._schedule_background_updates(request, context, model_output)
        result = RunResult(output_text=model_output.text, status="success")
        self.sessions.register_run(
            session_id=request.session_id,
            tenant_id=request.tenant_id,
            principal_id=request.principal_id,
            trace_id=request.trace_id,
            status=result.status,
            user_input=request.user_input,
            output_text=result.output_text,
            failure_reason="",
            capability_session_id=capability_session_id,
            capability_session_status=capability_session_status,
            authorization_mode=authorization_mode,
            delegated_principal_id=delegated_principal_id,
            delegated_scope=delegated_scope,
            idempotency_key=idempotency_key,
            approval_id=approval_id,
        )
        self.telemetry.emit(
            "run_complete",
            request.trace_id,
            session_id=request.session_id,
            status=result.status,
            output_preview=result.output_text[:80],
            authorization_mode=authorization_mode,
            delegated_principal_id=delegated_principal_id,
            delegated_scope=delegated_scope,
        )
        return result

    def _retrieve_context(self, context: RunContext, request: RunRequest) -> list[str]:
        static_layer = [
            f"agent_id={request.agent_id}",
            f"runtime_principal={self.agent.runtime_principal}",
        ]
        session_layer = [
            f"session_id={request.session_id}",
            f"tenant={request.tenant_id}",
            f"principal={request.principal_id}",
        ]
        retrieved_layer = [record.content for record in context.retrieved_records]
        context.context_layers = {
            "static": static_layer,
            "session": session_layer,
            "retrieved": retrieved_layer,
            "tool": [],
        }
        self.telemetry.emit(
            "retrieval",
            request.trace_id,
            session_id=request.session_id,
            source="memory_store",
            records=str(len(context.retrieved_records)),
        )
        return [*static_layer, *session_layer, *retrieved_layer]

    def _call_model(
        self,
        request: RunRequest,
        context: RunContext,
        *,
        second_pass: bool = False,
    ) -> ModelOutput:
        lowered = request.user_input.lower()
        if second_pass:
            latest_tool = context.tool_results[-1] if context.tool_results else None
            if latest_tool is not None and latest_tool.status == "approval_required":
                approval_id = latest_tool.payload.get("approval_id", "pending")
                return ModelOutput(
                    text=f"Ticket request is waiting for human approval ({approval_id}).",
                )
            return ModelOutput(text="Ticket request accepted and ready for follow-up.")
        if "language" in lowered or "preference" in lowered:
            profile_hint = next(
                (
                    record.content
                    for record in context.retrieved_records
                    if record.memory_class == "profile"
                ),
                "No stable preference was found.",
            )
            return ModelOutput(text=f"Retrieved profile hint: {profile_hint}")
        if "ticket" in lowered:
            arguments = {
                "title": "Agent follow-up",
                "queue": "support",
                "requester_id": request.principal_id,
            }
            if "without the usual safeguards" not in lowered:
                arguments["idempotency_key"] = request.trace_id
            if "simulate_failure=tool_timeout" in lowered:
                arguments["simulate_failure"] = "tool_timeout"
            if "simulate_failure=upstream_unavailable" in lowered:
                arguments["simulate_failure"] = "upstream_unavailable"
            return ModelOutput(
                text="I need to create a ticket before I can answer fully.",
                tool_request=ToolRequest(
                    capability_name="create_ticket",
                    arguments=arguments,
                ),
            )
        return ModelOutput(
            text=(
                "Reference runtime completed without tool usage. "
                f"Retrieved {len(context.retrieved_records)} memory records."
            ),
        )

    def _handle_tool_request(
        self,
        context: RunContext,
        request: RunRequest,
        tool_request: ToolRequest,
    ) -> PolicyDecision:
        tool_request.capability_name = normalize_tool_capability_name(
            tool_request.capability_name
        )
        tool_request.arguments = normalize_tool_arguments(tool_request.arguments)
        capability = self.catalog.get(tool_request.capability_name)
        decision = self.policy.evaluate_tool(context, tool_request, capability)
        self.telemetry.emit(
            "tool_policy_decision",
            request.trace_id,
            agent_id=request.agent_id,
            session_id=request.session_id,
            capability=tool_request.capability_name,
            action=decision.action,
            reason=decision.reason,
            policy_id=decision.policy_id,
        )
        if capability is None:
            tool_result = ToolResult(
                capability_name=tool_request.capability_name,
                status="denied",
                payload={
                    "reason": decision.reason,
                    "authorization_mode": request.authorization_mode,
                    "delegated_principal_id": request.delegated_principal_id,
                    "delegated_scope": request.delegated_scope,
                },
            )
            context.tool_results.append(tool_result)
            context.context_layers.setdefault("tool", []).append(
                f"{tool_result.capability_name}:{tool_result.status}",
            )
            self.telemetry.emit(
                "tool_execution",
                request.trace_id,
                session_id=request.session_id,
                capability=tool_result.capability_name,
                status=tool_result.status,
                tool_principal="n/a",
                authorization_mode=tool_result.payload["authorization_mode"],
                delegated_principal_id=tool_result.payload["delegated_principal_id"],
                delegated_scope=tool_result.payload["delegated_scope"],
            )
            return decision
        if decision.action == "approval_required":
            approver = (
                decision.reason.split("approver:", 1)[1]
                if decision.reason.startswith("approver:")
                else None
            )
            approval_request = self.approvals.submit(
                trace_id=request.trace_id,
                capability_name=tool_request.capability_name,
                requested_by=request.principal_id,
                reviewer=approver,
                reason=decision.reason,
                session_id=request.session_id,
                authorization_mode=request.authorization_mode,
                delegated_principal_id=request.delegated_principal_id,
                delegated_scope=request.delegated_scope,
                idempotency_key=tool_request.arguments.get("idempotency_key", ""),
            )
            self.telemetry.emit(
                "approval_requested",
                request.trace_id,
                session_id=request.session_id,
                approval_id=approval_request.approval_id,
                capability=approval_request.capability_name,
                reviewer=approval_request.reviewer,
                status=approval_request.status,
                capability_session_id=approval_request.capability_session_id,
                capability_session_status=approval_request.capability_session_status,
                authorization_mode=approval_request.authorization_mode,
                delegated_principal_id=approval_request.delegated_principal_id,
                delegated_scope=approval_request.delegated_scope,
                idempotency_key=approval_request.idempotency_key,
            )
            self._emit_sandbox_profile_reviewed(
                request=request,
                reviewer=approval_request.reviewer,
            )
            tool_result = ToolResult(
                capability_name=tool_request.capability_name,
                status="approval_required",
                payload={
                    "reason": decision.reason,
                    "approval_id": approval_request.approval_id,
                    "reviewer": approval_request.reviewer,
                    "capability_session_id": approval_request.capability_session_id,
                    "capability_session_status": approval_request.capability_session_status,
                    "authorization_mode": approval_request.authorization_mode,
                    "delegated_principal_id": approval_request.delegated_principal_id,
                    "delegated_scope": approval_request.delegated_scope,
                    "idempotency_key": approval_request.idempotency_key,
                },
            )
            context.tool_results.append(tool_result)
            context.context_layers.setdefault("tool", []).append(
                f"{tool_result.capability_name}:{tool_result.status}",
            )
            self.telemetry.emit(
                "tool_execution",
                request.trace_id,
                session_id=request.session_id,
                capability=tool_result.capability_name,
                status=tool_result.status,
                tool_principal="pending_review",
                authorization_mode=tool_result.payload["authorization_mode"],
                delegated_principal_id=tool_result.payload["delegated_principal_id"],
                delegated_scope=tool_result.payload["delegated_scope"],
                idempotency_key=tool_result.payload["idempotency_key"],
            )
            return decision

        tool_result = cast(
            ToolResult,
            self.telemetry.traced_call(
                request.trace_id,
                f"tool:{tool_request.capability_name}",
                lambda: execute_tool(capability, tool_request, decision),
            ),
        )
        tool_result.payload["authorization_mode"] = tool_result.payload.get(
            "authorization_mode", request.authorization_mode
        )
        tool_result.payload["delegated_principal_id"] = tool_result.payload.get(
            "delegated_principal_id", request.delegated_principal_id
        )
        tool_result.payload["delegated_scope"] = tool_result.payload.get(
            "delegated_scope", request.delegated_scope
        )
        tool_result.payload["idempotency_key"] = tool_result.payload.get(
            "idempotency_key", tool_request.arguments.get("idempotency_key", "")
        )
        context.tool_results.append(tool_result)
        context.context_layers.setdefault("tool", []).append(
            f"{tool_result.capability_name}:{tool_result.status}",
        )
        self.telemetry.emit(
            "tool_execution",
            request.trace_id,
            session_id=request.session_id,
            capability=tool_result.capability_name,
            status=tool_result.status,
            tool_principal=tool_result.payload.get("tool_principal", "n/a"),
            authorization_mode=tool_result.payload.get(
                "authorization_mode", request.authorization_mode
            ),
            delegated_principal_id=tool_result.payload.get(
                "delegated_principal_id", request.delegated_principal_id
            ),
            delegated_scope=tool_result.payload.get("delegated_scope", request.delegated_scope),
            idempotency_key=tool_result.payload.get("idempotency_key", ""),
        )
        return decision

    def _emit_sandbox_profile_reviewed(
        self,
        *,
        request: RunRequest,
        reviewer: str,
    ) -> None:
        if not self.sandbox_profile:
            return
        manifest_version = self.sandbox_profile.get("manifest_version", "unknown")
        workspace = self._sandbox_profile_mapping("workspace")
        workspace_entries = _read_workspace_entries(workspace)
        shell_mode = self._sandbox_profile_nested_value("capabilities", "shell")
        network = self._sandbox_profile_nested_value("permissions", "network")
        secrets = self._sandbox_profile_nested_value("permissions", "secrets")
        snapshot_policy = self._sandbox_profile_nested_value("state", "snapshot")
        self.telemetry.emit(
            "sandbox_profile_reviewed",
            request.trace_id,
            session_id=request.session_id,
            sandbox_profile_contract=f"sandbox-profile-v{manifest_version}",
            workspace_entries_reviewed=str(bool(workspace_entries)).lower(),
            workspace_manifest_ref="runtime-controls.yaml#runtime_controls.sandbox_profile.workspace",
            permissions_profile=f"{shell_mode}-shell-network-{network}",
            network_secrets_posture=f"network:{network},secrets:{secrets}",
            snapshot_policy=str(snapshot_policy),
            reviewed_by=reviewer or "runtime-review",
            review_evidence_refs=f"trace:{request.trace_id};eval:sandbox_profile_review",
        )

    def _sandbox_profile_mapping(self, key: str) -> dict[str, object]:
        value = self.sandbox_profile.get(key, {})
        if not isinstance(value, dict):
            raise TypeError(f"Sandbox profile {key} config must be a mapping")
        return cast(dict[str, object], value)

    def _sandbox_profile_nested_value(self, section: str, key: str) -> str:
        value = self._sandbox_profile_mapping(section).get(key, "unknown")
        if not isinstance(value, str):
            raise TypeError(f"Sandbox profile {section}.{key} must be a string")
        return value

    def _schedule_background_updates(
        self,
        request: RunRequest,
        context: RunContext,
        model_output: ModelOutput,
    ) -> None:
        result = self.background.process_post_run(request, context, model_output)
        self.telemetry.emit(
            "background_update_scheduled",
            request.trace_id,
            session_id=request.session_id,
            action="processed",
            persisted_records=str(result.persisted_records),
            compacted_records=str(result.compacted_records),
            tool_results=str(len(context.tool_results)),
            output_preview=model_output.text[:40],
        )
