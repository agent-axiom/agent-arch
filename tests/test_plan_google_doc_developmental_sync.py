import re
from pathlib import Path
from typing import Any

import pytest

from docs.publisher.tools.plan_google_doc_developmental_sync import (
    TargetParagraph,
    TargetRun,
    build_alignment,
    normalize,
    resolve_live_range,
    style_requests,
)


def _target_paragraph(
    text: str,
    *,
    named_style: str = "NORMAL_TEXT",
    page_break_before: bool = False,
    list_kind: str | None = None,
    nesting_level: int = 0,
    runs: tuple[TargetRun, ...] = (),
) -> TargetParagraph:
    return TargetParagraph(
        text=text,
        normalized=normalize(text),
        named_style=named_style,
        page_break_before=page_break_before,
        list_kind=list_kind,
        nesting_level=nesting_level,
        runs=runs,
    )


def _live_paragraph(text: str, start: int, end: int) -> dict[str, Any]:
    return {"text": text, "startIndex": start, "endIndex": end}


def test_normalize_matches_google_outline_links_to_docx_text() -> None:
    linked = (
        "S042. [Microsoft Azure Architecture Center, AI Agent Orchestration "
        "Patterns](https://learn.microsoft.com/ai/agent-patterns), дата обращения: "
        "15 июля 2026 года."
    )
    plain = (
        "S042. Microsoft Azure Architecture Center, AI Agent Orchestration "
        "Patterns, дата обращения: 15 июля 2026 года."
    )

    assert normalize(linked) == normalize(plain)
    assert build_alignment([normalize(plain)], [normalize(linked)]) == {0: 0}
    assert normalize("[RFC](https://example.com/spec(v2))") == "RFC"


def test_resolve_live_range_places_adjacent_insert_at_following_paragraph() -> None:
    live = [
        _live_paragraph("Before", 10, 20),
        _live_paragraph("After", 20, 30),
    ]

    assert resolve_live_range(("insert", 1, 1, 1, 2), {0: 0, 1: 1}, live, ["Before", "After"]) == (
        20,
        20,
        {"before": "Before", "after": "After", "unmapped_old": 0},
    )


def test_resolve_live_range_places_gapped_insert_after_previous_paragraph() -> None:
    live = [
        _live_paragraph("Before", 10, 20),
        _live_paragraph("Live-only paragraph", 20, 30),
        _live_paragraph("After", 30, 40),
    ]

    assert resolve_live_range(
        ("insert", 2, 2, 2, 3), {0: 0, 2: 2}, live, ["Before", "Old gap", "After"]
    ) == (
        20,
        20,
        {"before": "Before", "after": "After", "unmapped_old": 0},
    )


def test_resolve_live_range_accepts_one_unambiguous_fuzzy_paragraph() -> None:
    live = [
        _live_paragraph("Before", 10, 20),
        _live_paragraph("Target paragraph", 20, 30),
        _live_paragraph("Unrelated live paragraph", 30, 40),
        _live_paragraph("After", 40, 50),
    ]

    start, end, metadata = resolve_live_range(
        ("replace", 1, 2, 1, 2),
        {0: 0, 2: 3},
        live,
        ["Before", "Target paragraph", "After"],
    )

    assert (start, end) == (20, 30)
    assert metadata == {
        "first": "Target paragraph",
        "last": "Target paragraph",
        "unmapped_old": 1,
        "fuzzy_ratio": 1.0,
    }
    assert metadata["fuzzy_ratio"] >= 0.85


@pytest.mark.parametrize(
    "candidate_texts",
    [
        ("Target paragraph!", "Target paragraph?"),
        ("Completely unrelated", "Nothing similar"),
    ],
    ids=["ambiguous", "sub-threshold"],
)
def test_resolve_live_range_falls_back_when_fuzzy_match_is_rejected(
    candidate_texts: tuple[str, str],
) -> None:
    first_candidate, last_candidate = candidate_texts
    live = [
        _live_paragraph("Before", 10, 20),
        _live_paragraph(first_candidate, 20, 30),
        _live_paragraph(last_candidate, 30, 40),
        _live_paragraph("After", 40, 50),
    ]

    assert resolve_live_range(
        ("replace", 1, 2, 1, 2),
        {0: 0, 2: 3},
        live,
        ["Before", "Target paragraph", "After"],
    ) == (
        20,
        40,
        {
            "first": first_candidate,
            "last": last_candidate,
            "unmapped_old": 1,
        },
    )


@pytest.mark.parametrize(
    ("mapping", "unmapped_old"),
    [
        ({1: 1, 2: 2, 3: 3}, 0),
        ({0: 0, 2: 2, 3: 3}, 1),
        ({1: 1, 2: 2, 4: 4}, 1),
        ({0: 0, 2: 2, 4: 4}, 2),
    ],
    ids=["mapped", "unmapped-start", "unmapped-end", "unmapped-both"],
)
def test_resolve_live_range_handles_mapped_and_unmapped_endpoints(
    mapping: dict[int, int], unmapped_old: int
) -> None:
    live = [
        _live_paragraph("A", 10, 20),
        _live_paragraph("B", 20, 30),
        _live_paragraph("C", 30, 40),
        _live_paragraph("D", 40, 50),
        _live_paragraph("E", 50, 60),
    ]

    assert resolve_live_range(
        ("replace", 1, 4, 1, 4), mapping, live, ["A", "B", "C", "D", "E"]
    ) == (
        20,
        50,
        {"first": "B", "last": "D", "unmapped_old": unmapped_old},
    )


@pytest.mark.parametrize(
    ("mapping", "message"),
    [
        ({1: 2, 2: 1}, "Non-monotonic live mapping"),
        ({0: 2, 3: 1}, "Invalid live range 40:20"),
    ],
    ids=["non-monotonic-takes-precedence", "invalid-range"],
)
def test_resolve_live_range_rejects_unsafe_ranges(mapping: dict[int, int], message: str) -> None:
    live = [
        _live_paragraph("A", 10, 20),
        _live_paragraph("B", 20, 30),
        _live_paragraph("C", 30, 40),
    ]
    opcode = ("replace", 1, 3, 1, 3)

    with pytest.raises(ValueError, match=message):
        resolve_live_range(opcode, mapping, live, ["A", "B", "C", "D"])


def test_style_requests_reset_inherited_page_breaks() -> None:
    paragraphs = [
        _target_paragraph("Обычный абзац"),
        _target_paragraph(
            "Новая глава",
            named_style="HEADING_2",
            page_break_before=True,
        ),
    ]

    requests = style_requests(paragraphs, start=100, tab_id="t.0")
    updates = [
        request["updateParagraphStyle"]
        for request in requests
        if "updateParagraphStyle" in request
    ]

    assert [update["paragraphStyle"]["pageBreakBefore"] for update in updates] == [False, True]
    assert all(update["fields"] == "namedStyleType,pageBreakBefore" for update in updates)


def test_style_requests_uses_utf16_offsets_for_astral_text() -> None:
    paragraphs = [
        TargetParagraph(
            text="A😀B",
            normalized="A😀B",
            named_style="NORMAL_TEXT",
            page_break_before=False,
            list_kind=None,
            nesting_level=0,
            runs=(
                TargetRun(0, 0, bold=True, italic=True, font_name="Ignored"),
                TargetRun(0, 1, bold=None, italic=None, font_name=None),
                TargetRun(1, 3, bold=False, italic=True, font_name="Noto Sans"),
                TargetRun(3, 4, bold=True, italic=None, font_name=None),
            ),
        )
    ]

    requests = style_requests(paragraphs, start=10, tab_id="t.0")

    assert requests == [
        {"deleteParagraphBullets": {"range": {"startIndex": 10, "endIndex": 15, "tabId": "t.0"}}},
        {
            "updateParagraphStyle": {
                "range": {"startIndex": 10, "endIndex": 15, "tabId": "t.0"},
                "paragraphStyle": {
                    "namedStyleType": "NORMAL_TEXT",
                    "pageBreakBefore": False,
                },
                "fields": "namedStyleType,pageBreakBefore",
            }
        },
        {
            "updateTextStyle": {
                "range": {"startIndex": 11, "endIndex": 13, "tabId": "t.0"},
                "textStyle": {
                    "bold": False,
                    "italic": True,
                    "weightedFontFamily": {"fontFamily": "Noto Sans"},
                },
                "fields": "bold,italic,weightedFontFamily",
            }
        },
        {
            "updateTextStyle": {
                "range": {"startIndex": 13, "endIndex": 14, "tabId": "t.0"},
                "textStyle": {"bold": True},
                "fields": "bold",
            }
        },
    ]
    assert requests[1]["updateParagraphStyle"]["range"]["endIndex"] == 15
    assert list(requests[2]["updateTextStyle"]["textStyle"]) == [
        "bold",
        "italic",
        "weightedFontFamily",
    ]


def test_style_requests_group_only_contiguous_lists_of_same_kind_and_nesting() -> None:
    paragraphs = [
        _target_paragraph("A", list_kind="bullet", nesting_level=0),
        _target_paragraph("B", list_kind="bullet", nesting_level=0),
        _target_paragraph("C", list_kind="bullet", nesting_level=1),
        _target_paragraph("D", list_kind="number", nesting_level=1),
        _target_paragraph("E", list_kind="number", nesting_level=1),
        _target_paragraph("F"),
        _target_paragraph("G", list_kind="bullet", nesting_level=0),
    ]

    requests = style_requests(paragraphs, start=50, tab_id="t.7")
    bullet_requests = [
        request["createParagraphBullets"]
        for request in requests
        if "createParagraphBullets" in request
    ]

    assert [next(iter(request)) for request in requests] == [
        "deleteParagraphBullets",
        *("updateParagraphStyle" for _ in paragraphs),
        *("createParagraphBullets" for _ in range(4)),
    ]
    assert bullet_requests == [
        {
            "range": {"startIndex": 50, "endIndex": 54, "tabId": "t.7"},
            "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE",
        },
        {
            "range": {"startIndex": 54, "endIndex": 56, "tabId": "t.7"},
            "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE",
        },
        {
            "range": {"startIndex": 56, "endIndex": 60, "tabId": "t.7"},
            "bulletPreset": "NUMBERED_DECIMAL_NESTED",
        },
        {
            "range": {"startIndex": 62, "endIndex": 64, "tabId": "t.7"},
            "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE",
        },
    ]


def test_google_doc_alt_text_script_matches_manuscript_images() -> None:
    root = Path(__file__).parents[1]
    manuscript = (
        root / "docs/publisher/ru-manuscript-editorial-2026-07-13.md"
    ).read_text(encoding="utf-8")
    script = (
        root / "docs/publisher/tools/set_google_doc_image_alt_text.gs"
    ).read_text(encoding="utf-8")

    expected = re.findall(r"^!\[([^]]+)]\([^)]+\)$", manuscript, flags=re.MULTILINE)
    array_body = script.split("const ALT_DESCRIPTIONS = [", 1)[1].split("];", 1)[0]
    actual = re.findall(r"^  '(.+)',?$", array_body, flags=re.MULTILINE)

    assert len(expected) == 56
    assert actual == [description.rstrip(".") + "." for description in expected]
