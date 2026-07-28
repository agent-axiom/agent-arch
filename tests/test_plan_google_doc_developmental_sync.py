import re
from pathlib import Path

from docs.publisher.tools.plan_google_doc_developmental_sync import (
    TargetParagraph,
    build_alignment,
    normalize,
    style_requests,
)


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


def test_style_requests_reset_inherited_page_breaks() -> None:
    paragraphs = [
        TargetParagraph(
            text="Обычный абзац",
            normalized="Обычный абзац",
            named_style="NORMAL_TEXT",
            page_break_before=False,
            list_kind=None,
            nesting_level=0,
            runs=(),
        ),
        TargetParagraph(
            text="Новая глава",
            normalized="Новая глава",
            named_style="HEADING_2",
            page_break_before=True,
            list_kind=None,
            nesting_level=0,
            runs=(),
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
