from __future__ import annotations

from dataclasses import dataclass

from agent_runtime_ref.memory import MemoryCandidate, MemoryStore
from agent_runtime_ref.models import ModelOutput, RunContext, RunRequest
from agent_runtime_ref.policy import PolicyEngine
from agent_runtime_ref.telemetry import TelemetryEmitter


@dataclass(frozen=True, slots=True)
class BackgroundUpdateResult:
    persisted_records: int
    compacted_records: int


class BackgroundWorker:
    """Background maintenance path for memory writes and compaction."""

    def __init__(
        self,
        *,
        memory_store: MemoryStore,
        policy: PolicyEngine,
        telemetry: TelemetryEmitter,
    ) -> None:
        self.memory_store = memory_store
        self.policy = policy
        self.telemetry = telemetry

    def process_post_run(
        self,
        request: RunRequest,
        context: RunContext,
        model_output: ModelOutput,
    ) -> BackgroundUpdateResult:
        candidates = self._build_candidates(request, context, model_output)
        persisted = 0
        for candidate in candidates:
            decision = self.policy.allow_memory_write(candidate.kind)
            self.telemetry.emit(
                "memory_write_decision",
                request.trace_id,
                kind=candidate.kind,
                action=decision.action,
                reason=decision.reason,
                memory_class=candidate.memory_class,
            )
            if decision.action != "allow":
                continue
            self.memory_store.persist(candidate)
            persisted += 1
        compacted = self.memory_store.compact(request.tenant_id)
        self.telemetry.emit(
            "background_compaction",
            request.trace_id,
            tenant_id=request.tenant_id,
            compacted_records=str(compacted),
        )
        return BackgroundUpdateResult(
            persisted_records=persisted,
            compacted_records=compacted,
        )

    @staticmethod
    def _build_candidates(
        request: RunRequest,
        context: RunContext,
        model_output: ModelOutput,
    ) -> list[MemoryCandidate]:
        candidates = [
            MemoryCandidate(
                tenant_id=request.tenant_id,
                memory_class="long_term",
                kind="session_summary",
                content=(
                    f"User asked: {request.user_input}. "
                    f"Runtime returned: {model_output.text}"
                ),
                source="approved_summarizer",
                confidence=0.82,
            ),
        ]
        if context.tool_results:
            successful_tools = [
                result.capability_name
                for result in context.tool_results
                if result.status == "success"
            ]
            if successful_tools:
                candidates.append(
                    MemoryCandidate(
                        tenant_id=request.tenant_id,
                        memory_class="long_term",
                        kind="validated_fact",
                        content=(
                            "Successful tool actions in this run: "
                            + ", ".join(successful_tools)
                        ),
                        source="trusted_service",
                        confidence=0.9,
                    ),
                )
        return candidates
