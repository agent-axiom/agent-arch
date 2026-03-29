from __future__ import annotations

from typing import cast

from agent_runtime_ref.catalog import CapabilityCatalog
from agent_runtime_ref.execution import execute_tool
from agent_runtime_ref.models import (
    ModelOutput,
    RunContext,
    RunRequest,
    RunResult,
    ToolRequest,
    ToolResult,
)
from agent_runtime_ref.policy import PolicyDecision, PolicyEngine
from agent_runtime_ref.telemetry import TelemetryEmitter


class AgentRuntime:
    """Minimal runnable skeleton for the book's reference implementation."""

    def __init__(
        self,
        catalog: CapabilityCatalog | None = None,
        policy: PolicyEngine | None = None,
        telemetry: TelemetryEmitter | None = None,
    ) -> None:
        self.catalog = catalog or CapabilityCatalog()
        self.policy = policy or PolicyEngine()
        self.telemetry = telemetry or TelemetryEmitter()

    def run(self, request: RunRequest) -> RunResult:
        precheck = self.policy.precheck(request)
        self.telemetry.emit(
            "policy_precheck",
            request.trace_id,
            action=precheck.action,
            reason=precheck.reason,
            policy_id=precheck.policy_id,
        )
        if precheck.action != "allow":
            return RunResult(output_text="Request denied by policy.", status="denied")

        context = RunContext(
            tenant_id=request.tenant_id,
            principal_id=request.principal_id,
            trace_id=request.trace_id,
        )
        context.retrieved_context = self._retrieve_context(request)

        model_output = self.telemetry.traced_call(
            request.trace_id,
            "model_step",
            lambda: self._call_model(request, context),
        )
        if not isinstance(model_output, ModelOutput):
            raise TypeError("Model step must return ModelOutput")

        if model_output.tool_request is not None:
            self._handle_tool_request(context, request, model_output.tool_request)
            model_output = self._call_model(request, context, second_pass=True)

        self._schedule_background_updates(request, context, model_output)
        return RunResult(output_text=model_output.text, status="success")

    def _retrieve_context(self, request: RunRequest) -> list[str]:
        self.telemetry.emit("retrieval", request.trace_id, source="mock_memory", records="1")
        return [f"tenant={request.tenant_id}", "knowledge: reference runtime skeleton"]

    def _call_model(
        self,
        request: RunRequest,
        context: RunContext,
        *,
        second_pass: bool = False,
    ) -> ModelOutput:
        del context
        lowered = request.user_input.lower()
        if second_pass:
            return ModelOutput(text="Ticket request accepted and ready for follow-up.")
        if "ticket" in lowered:
            return ModelOutput(
                text="I need to create a ticket before I can answer fully.",
                tool_request=ToolRequest(
                    capability_name="create_ticket",
                    arguments={
                        "title": "Agent follow-up",
                        "queue": "support",
                        "requester_id": request.principal_id,
                        "idempotency_key": request.trace_id,
                    },
                ),
            )
        return ModelOutput(text="Reference runtime completed without tool usage.")

    def _handle_tool_request(
        self,
        context: RunContext,
        request: RunRequest,
        tool_request: ToolRequest,
    ) -> PolicyDecision:
        capability = self.catalog.get(tool_request.capability_name)
        decision = self.policy.evaluate_tool(context, tool_request, capability)
        self.telemetry.emit(
            "tool_policy_decision",
            request.trace_id,
            capability=tool_request.capability_name,
            action=decision.action,
            reason=decision.reason,
            policy_id=decision.policy_id,
        )
        if capability is None:
            context.tool_results.append(
                execute_tool(
                    capability=self.catalog.get("search_docs") or self.catalog.all()[0],
                    tool_request=tool_request,
                    decision=PolicyDecision("deny", "capability_unknown", "cap_404"),
                ),
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
        context.tool_results.append(tool_result)
        self.telemetry.emit(
            "tool_execution",
            request.trace_id,
            capability=tool_result.capability_name,
            status=tool_result.status,
        )
        return decision

    def _schedule_background_updates(
        self,
        request: RunRequest,
        context: RunContext,
        model_output: ModelOutput,
    ) -> None:
        decision = self.policy.allow_memory_write("session_summary")
        self.telemetry.emit(
            "background_update_scheduled",
            request.trace_id,
            action=decision.action,
            tool_results=str(len(context.tool_results)),
            output_preview=model_output.text[:40],
        )
