import re
from pathlib import Path

from docs.publisher.tools.plan_google_doc_developmental_sync import (
    TargetParagraph,
    TargetRun,
    build_alignment,
    normalize,
    replacement_delete_end,
    replacement_text,
    selected_opcodes,
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
        request["updateParagraphStyle"] for request in requests if "updateParagraphStyle" in request
    ]

    assert [update["paragraphStyle"]["pageBreakBefore"] for update in updates] == [False, True]
    assert all(update["fields"] == "namedStyleType,pageBreakBefore" for update in updates)


def test_style_requests_restore_external_hyperlinks() -> None:
    paragraph = TargetParagraph(
        text="Официальная спецификация",
        normalized="Официальная спецификация",
        named_style="NORMAL_TEXT",
        page_break_before=False,
        list_kind=None,
        nesting_level=0,
        runs=(
            TargetRun(
                start=0,
                end=23,
                bold=None,
                italic=None,
                font_name=None,
                link_url="https://example.com/spec",
            ),
        ),
    )

    requests = style_requests([paragraph], start=100, tab_id="t.0")
    link_updates = [
        request["updateTextStyle"]
        for request in requests
        if request.get("updateTextStyle", {}).get("textStyle", {}).get("link")
    ]

    assert link_updates == [
        {
            "range": {"startIndex": 100, "endIndex": 123, "tabId": "t.0"},
            "textStyle": {"link": {"url": "https://example.com/spec"}},
            "fields": "link",
        }
    ]


def test_protected_opcode_is_left_for_manual_structured_sync() -> None:
    opcodes = [
        ("replace", 1, 2, 1, 3),
        ("insert", 4, 4, 5, 6),
        ("delete", 7, 8, 9, 9),
    ]

    selected, skipped = selected_opcodes(opcodes, [2, 99])

    assert selected == [(1, opcodes[0]), (3, opcodes[2])]
    assert skipped == [2]


def test_table_adjacent_replacement_preserves_existing_paragraph_break() -> None:
    paragraph = TargetParagraph(
        text="Подпись перед таблицей",
        normalized="Подпись перед таблицей",
        named_style="NORMAL_TEXT",
        page_break_before=False,
        list_kind=None,
        nesting_level=0,
        runs=(),
    )

    assert replacement_delete_end(240, preserve_trailing_break=True) == 239
    assert replacement_text([paragraph], preserve_trailing_break=True) == paragraph.text
    assert replacement_delete_end(240, preserve_trailing_break=False) == 240
    assert replacement_text([paragraph], preserve_trailing_break=False) == (paragraph.text + "\n")


def test_google_doc_alt_text_script_matches_manuscript_images() -> None:
    root = Path(__file__).parents[1]
    manuscript = (root / "docs/publisher/ru-manuscript-editorial-2026-07-13.md").read_text(
        encoding="utf-8"
    )
    script = (root / "docs/publisher/tools/set_google_doc_image_alt_text.gs").read_text(
        encoding="utf-8"
    )

    expected = re.findall(r"^!\[([^]]+)]\([^)]+\)$", manuscript, flags=re.MULTILINE)
    array_body = script.split("const ALT_DESCRIPTIONS = [", 1)[1].split("];", 1)[0]
    actual = re.findall(r"^  '(.+)',?$", array_body, flags=re.MULTILINE)

    assert len(expected) == 57
    assert actual == [description.rstrip(".") + "." for description in expected]
