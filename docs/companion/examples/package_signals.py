from __future__ import annotations

from collections.abc import Mapping


def required_signals_observed(
    signals: object,
    required_refs: Mapping[str, set[str]],
) -> bool:
    """Check package claims after generic manifest schema/integrity verification."""
    if isinstance(signals, dict):
        entries = signals.items()
    elif isinstance(signals, list):
        entries = ((item.get("id"), item) for item in signals if isinstance(item, dict))
    else:
        return False
    by_id = {key.strip(): value for key, value in entries if isinstance(key, str)}
    for signal_id, expected_refs in required_refs.items():
        signal = by_id.get(signal_id)
        if not isinstance(signal, dict) or signal.get("value") is not True:
            return False
        references = signal.get("artifact_refs")
        if not isinstance(references, list) or not all(isinstance(ref, str) for ref in references):
            return False
        if not expected_refs <= set(references):
            return False
    return True
