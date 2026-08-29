from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
LOCALIZATIONS = ("md", "en.md", "zh.md")


def chapter(part: str, number: int, localization: str) -> str:
    return (ROOT / f"docs/book/{part}/chapter-{number}.{localization}").read_text(encoding="utf-8")


@pytest.mark.parametrize("localization", LOCALIZATIONS)
def test_approval_required_pauses_before_gateway_dispatch(localization: str) -> None:
    text = chapter("part-i", 2, localization)

    approval = text.index('if decision.action == "approval_required":')
    pause = text.index("approval_service.request_pause", approval)
    dispatch = text.index("gateway.call", approval)

    assert approval < pause < dispatch


@pytest.mark.parametrize("localization", LOCALIZATIONS)
def test_capability_risk_is_checked_before_transport(localization: str) -> None:
    text = chapter("part-iv", 9, localization)

    risk = text.index('if spec.mode == "high_risk":')
    transport = text.index('if spec.transport == "mcp":', risk)

    assert risk < transport


@pytest.mark.parametrize("localization", LOCALIZATIONS)
def test_run_health_keeps_external_effect_and_control_state(localization: str) -> None:
    text = chapter("part-v", 12, localization)

    assert "external_effect_known: bool" in text
    assert "required_controls_passed: bool" in text
    assert 'return "unknown_external_effect"' in text
    assert 'return "control_failure"' in text


@pytest.mark.parametrize("localization", LOCALIZATIONS)
def test_durable_resume_uses_lease_idempotency_and_version_guard(localization: str) -> None:
    text = chapter("part-vii", 16, localization)

    claim = text.index("claim_run(")
    execute = text.index("execute_run_steps(", claim)
    complete = text.index("complete_run(", execute)

    assert claim < execute < complete
    assert "lease_seconds=30" in text[claim:execute]
    assert "idempotency_scope=run.run_id" in text[execute:complete]
    assert "expected_version=run.version" in text[complete:]


@pytest.mark.parametrize("localization", LOCALIZATIONS)
def test_emergency_decision_is_owned_and_observable(localization: str) -> None:
    text = chapter("part-viii", 21, localization)

    decision = text.index("class EmergencyDecision:")
    body = text[decision : text.index("def emergency_action", decision)]

    assert "action: str" in body
    assert "owner: str" in body
    assert "evidence_event: str" in body
