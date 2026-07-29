from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from agent_runtime_ref.idempotency import (
    IdempotencyStore,
    compute_idempotency_request_digest,
)
from agent_runtime_ref.models import ToolResult

NOW = datetime(2026, 7, 23, 10, 0, tzinfo=UTC)


def _digest(*, title: str = "Follow up") -> str:
    return compute_idempotency_request_digest(
        capability_name="create_ticket",
        arguments={"idempotency_key": "intent-001", "title": title},
        tenant_id="tenant-acme",
        principal_id="user-42",
    )


def test_successful_request_is_replayed_without_a_second_execution() -> None:
    store = IdempotencyStore(ttl=timedelta(hours=1))
    digest = _digest()

    first = store.reserve("intent-001", digest, now=NOW)
    store.complete(
        "intent-001",
        digest,
        ToolResult("create_ticket", "success", {"ticket_id": "T-42"}),
        now=NOW,
    )
    replay = store.reserve("intent-001", digest, now=NOW + timedelta(minutes=5))

    assert first.action == "execute"
    assert replay.action == "replay"
    assert replay.result == ToolResult(
        "create_ticket",
        "success",
        {"ticket_id": "T-42"},
    )


def test_same_key_with_different_payload_is_rejected() -> None:
    store = IdempotencyStore()
    store.reserve("intent-001", _digest(), now=NOW)

    decision = store.reserve(
        "intent-001",
        _digest(title="Escalate"),
        now=NOW,
    )

    assert decision.action == "conflict"
    assert decision.result is None


def test_in_progress_request_is_not_executed_concurrently() -> None:
    store = IdempotencyStore()
    digest = _digest()
    store.reserve("intent-001", digest, now=NOW)

    decision = store.reserve("intent-001", digest, now=NOW)

    assert decision.action == "wait"


def test_known_pre_dispatch_failure_can_be_retried() -> None:
    store = IdempotencyStore()
    digest = _digest()
    store.reserve("intent-001", digest, now=NOW)
    store.complete(
        "intent-001",
        digest,
        ToolResult(
            "create_ticket",
            "retryable_failure",
            {"reason": "tool_timeout", "effect_state": "not_executed"},
        ),
        now=NOW,
    )

    retry = store.reserve("intent-001", digest, now=NOW + timedelta(seconds=1))

    assert retry.action == "execute"


def test_unknown_effect_requires_reconciliation_even_after_ttl() -> None:
    store = IdempotencyStore(ttl=timedelta(seconds=1))
    digest = _digest()
    store.reserve("intent-001", digest, now=NOW)
    store.complete(
        "intent-001",
        digest,
        ToolResult(
            "create_ticket",
            "side_effect_unknown",
            {
                "reason": "post_dispatch_timeout",
                "effect_state": "side_effect_unknown",
            },
            side_effect_status="side_effect_unknown",
        ),
        now=NOW,
    )

    retry = store.reserve("intent-001", digest, now=NOW + timedelta(days=1))

    assert retry.action == "reconcile"


@pytest.mark.parametrize(
    ("outcome", "side_effect_status"),
    [
        ("success", "side_effect_unknown"),
        ("success", "partial_side_effect"),
        ("side_effect_unknown", "not_executed"),
        ("partial_side_effect", "not_executed"),
        ("side_effect_unknown", "partial_side_effect"),
        ("partial_side_effect", "side_effect_unknown"),
    ],
)
def test_unresolved_outcome_or_effect_prevents_replay(
    outcome: str,
    side_effect_status: str,
) -> None:
    store = IdempotencyStore()
    digest = _digest()
    store.reserve("intent-001", digest, now=NOW)
    store.complete(
        "intent-001",
        digest,
        ToolResult(
            "create_ticket",
            outcome,
            {"ticket_id": "T-42"},
            side_effect_status=side_effect_status,
        ),
        now=NOW,
    )

    retry = store.reserve(
        "intent-001",
        digest,
        now=NOW + timedelta(seconds=1),
    )

    assert retry.action == "reconcile"
    assert retry.result is not None
    assert retry.result.status == outcome
    assert retry.result.side_effect_status == side_effect_status


def test_completed_record_expires_after_configured_ttl() -> None:
    store = IdempotencyStore(ttl=timedelta(seconds=1))
    digest = _digest()
    store.reserve("intent-001", digest, now=NOW)
    store.complete(
        "intent-001",
        digest,
        ToolResult("create_ticket", "success", {"ticket_id": "T-42"}),
        now=NOW,
    )

    decision = store.reserve(
        "intent-001",
        digest,
        now=NOW + timedelta(seconds=2),
    )

    assert decision.action == "execute"
