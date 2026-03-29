from __future__ import annotations

from typing import cast

from agent_runtime_ref.background import BackgroundWorker
from agent_runtime_ref.catalog import CapabilityCatalog
from agent_runtime_ref.execution import execute_tool
from agent_runtime_ref.memory import MemoryStore
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
        memory: MemoryStore | None = None,
        background: BackgroundWorker | None = None,
    ) -> None:
        self.catalog = catalog or CapabilityCatalog()
        self.policy = policy or PolicyEngine()
        self.telemetry = telemetry or TelemetryEmitter()
        self.memory = memory or MemoryStore()
        self.background = background or BackgroundWorker(
            memory_store=self.memory,
            policy=self.policy,
            telemetry=self.telemetry,
        )

    def run(self, request: RunRequest) -> RunResult:
        self.telemetry.emit(
            "run_start",
            request.trace_id,
            user_input=request.user_input,
            tenant_id=request.tenant_id,
            principal_id=request.principal_id,
        )
        precheck = self.policy.precheck(request)
        self.telemetry.emit(
            "policy_precheck",
            request.trace_id,
            action=precheck.action,
            reason=precheck.reason,
            policy_id=precheck.policy_id,
        )
        if precheck.action != "allow":
            result = RunResult(output_text="Request denied by policy.", status="denied")
            self.telemetry.emit(
                "run_complete",
                request.trace_id,
                status=result.status,
                output_preview=result.output_text[:80],
            )
            return result

        context = RunContext(
            tenant_id=request.tenant_id,
            principal_id=request.principal_id,
            trace_id=request.trace_id,
        )
        context.retrieved_records = self.memory.retrieve(
            request.user_input,
            request.tenant_id,
            limit=3,
        )
        context.retrieved_context = self._retrieve_context(context, request)

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
        result = RunResult(output_text=model_output.text, status="success")
        self.telemetry.emit(
            "run_complete",
            request.trace_id,
            status=result.status,
            output_preview=result.output_text[:80],
        )
        return result

    def _retrieve_context(self, context: RunContext, request: RunRequest) -> list[str]:
        self.telemetry.emit(
            "retrieval",
            request.trace_id,
            source="memory_store",
            records=str(len(context.retrieved_records)),
        )
        return [
            f"tenant={request.tenant_id}",
            *[record.content for record in context.retrieved_records],
        ]

    def _call_model(
        self,
        request: RunRequest,
        context: RunContext,
        *,
        second_pass: bool = False,
    ) -> ModelOutput:
        lowered = request.user_input.lower()
        if second_pass:
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
        result = self.background.process_post_run(request, context, model_output)
        self.telemetry.emit(
            "background_update_scheduled",
            request.trace_id,
            action="processed",
            persisted_records=str(result.persisted_records),
            compacted_records=str(result.compacted_records),
            tool_results=str(len(context.tool_results)),
            output_preview=model_output.text[:40],
        )
