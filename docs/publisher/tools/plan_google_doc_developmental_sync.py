#!/usr/bin/env python3
"""Plan a range-safe Google Docs batch update from two publisher DOCX files.

The old DOCX provides the baseline already present in Google Docs. The new DOCX
provides only the developmental-editing delta. The planner aligns both files to
the trusted-read outline, refuses destructive ranges that cross tables or inline
objects, and emits native Docs requests in descending index order.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any


def _strip_markdown_link_targets(value: str) -> str:
    parts: list[str] = []
    cursor = 0

    while cursor < len(value):
        label_start = value.find("[", cursor)
        if label_start < 0:
            parts.append(value[cursor:])
            break

        label_end = value.find("](", label_start + 1)
        if label_end < 0:
            parts.append(value[cursor:])
            break

        url_start = label_end + 2
        if not value.startswith(("https://", "http://", "mailto:"), url_start):
            parts.append(value[cursor:url_start])
            cursor = url_start
            continue

        depth = 1
        url_end = url_start
        while url_end < len(value) and depth:
            if value[url_end] == "(":
                depth += 1
            elif value[url_end] == ")":
                depth -= 1
            url_end += 1

        if depth:
            parts.append(value[cursor:])
            break

        parts.append(value[cursor:label_start])
        parts.append(value[label_start + 1 : label_end])
        cursor = url_end

    return "".join(parts)


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", _strip_markdown_link_targets(value)).strip()


def utf16_length(value: str) -> int:
    return len(value.encode("utf-16-le")) // 2


@dataclass(frozen=True)
class TargetRun:
    start: int
    end: int
    bold: bool | None
    italic: bool | None
    font_name: str | None
    link_url: str | None = None
    link_fragment: str | None = None


@dataclass(frozen=True)
class TargetParagraph:
    text: str
    normalized: str
    named_style: str
    page_break_before: bool
    list_kind: str | None
    nesting_level: int
    runs: tuple[TargetRun, ...]


def numbering_formats(document: Any) -> dict[tuple[int, int], str]:
    from docx.oxml.ns import qn

    root = document.part.numbering_part.element
    abstract_by_num: dict[int, int] = {}
    for number in root.findall(qn("w:num")):
        num_id = int(number.get(qn("w:numId")))
        abstract = number.find(qn("w:abstractNumId"))
        if abstract is not None:
            abstract_by_num[num_id] = int(abstract.get(qn("w:val")))

    formats: dict[tuple[int, int], str] = {}
    for abstract in root.findall(qn("w:abstractNum")):
        abstract_id = int(abstract.get(qn("w:abstractNumId")))
        for level in abstract.findall(qn("w:lvl")):
            ilvl = int(level.get(qn("w:ilvl")))
            num_format = level.find(qn("w:numFmt"))
            if num_format is not None:
                formats[(abstract_id, ilvl)] = num_format.get(qn("w:val"))

    return {
        (num_id, ilvl): value
        for num_id, abstract_id in abstract_by_num.items()
        for (candidate, ilvl), value in formats.items()
        if candidate == abstract_id
    }


def docs_named_style(style_name: str) -> str:
    match = re.fullmatch(r"Heading (\d)", style_name, flags=re.IGNORECASE)
    if match:
        return f"HEADING_{match.group(1)}"
    if style_name.casefold() == "title":
        return "TITLE"
    if style_name.casefold() == "subtitle":
        return "SUBTITLE"
    return "NORMAL_TEXT"


def load_docx_paragraphs(path: Path) -> list[TargetParagraph]:
    from docx import Document

    document = Document(str(path))
    formats = numbering_formats(document)
    result: list[TargetParagraph] = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        if not text:
            continue

        list_kind: str | None = None
        nesting_level = 0
        properties = paragraph._p.pPr
        numbering = properties.numPr if properties is not None else None
        if numbering is not None and numbering.numId is not None:
            num_id = int(numbering.numId.val)
            nesting_level = int(numbering.ilvl.val) if numbering.ilvl is not None else 0
            num_format = formats.get((num_id, nesting_level), "bullet")
            list_kind = "number" if num_format not in {"bullet", "none"} else "bullet"

        run_offset = 0
        runs: list[TargetRun] = []
        for item in paragraph.iter_inner_content():
            item_runs = item.runs if type(item).__name__ == "Hyperlink" else (item,)
            link_url = getattr(item, "url", None) or None
            link_fragment = getattr(item, "fragment", None) or None
            for run in item_runs:
                run_text = run.text
                if not run_text:
                    continue
                start = run_offset
                end = start + utf16_length(run_text)
                runs.append(
                    TargetRun(
                        start=start,
                        end=end,
                        bold=run.bold,
                        italic=run.italic,
                        font_name=run.font.name,
                        link_url=link_url,
                        link_fragment=link_fragment,
                    )
                )
                run_offset = end

        if run_offset != utf16_length(paragraph.text):
            raise ValueError(f"Run offsets do not cover paragraph text: {paragraph.text[:120]!r}")

        result.append(
            TargetParagraph(
                text=text,
                normalized=normalize(text),
                named_style=docs_named_style(paragraph.style.name),
                page_break_before=bool(paragraph.paragraph_format.page_break_before),
                list_kind=list_kind,
                nesting_level=nesting_level,
                runs=tuple(runs),
            )
        )

    return result


def load_outline(path: Path, tab_id: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    all_paragraphs = [p for p in payload["paragraphs"] if p["tabId"] == tab_id]
    body_paragraphs = [p for p in all_paragraphs if normalize(p["text"]) and p.get("table") is None]
    return all_paragraphs, body_paragraphs


def build_alignment(old: list[str], live: list[str]) -> dict[int, int]:
    matcher = difflib.SequenceMatcher(None, old, live, autojunk=False)
    mapping = {
        old_start + offset: live_start + offset
        for old_start, live_start, size in matcher.get_matching_blocks()
        for offset in range(size)
    }
    live_positions: dict[str, list[int]] = {}
    for index, value in enumerate(live):
        live_positions.setdefault(value, []).append(index)

    for old_index, value in enumerate(old):
        if old_index in mapping or len(live_positions.get(value, [])) != 1:
            continue
        live_index = live_positions[value][0]
        previous = [index for index in mapping if index < old_index]
        following = [index for index in mapping if index > old_index]
        previous_live = mapping[max(previous)] if previous else -1
        following_live = mapping[min(following)] if following else len(live)
        if previous_live < live_index < following_live:
            mapping[old_index] = live_index
    return mapping


def nearest_mapped_before(mapping: dict[int, int], index: int) -> tuple[int, int]:
    candidates = [old_index for old_index in mapping if old_index < index]
    if not candidates:
        raise ValueError(f"No stable paragraph before old index {index}")
    old_index = max(candidates)
    return old_index, mapping[old_index]


def nearest_mapped_after(mapping: dict[int, int], index: int) -> tuple[int, int]:
    candidates = [old_index for old_index in mapping if old_index >= index]
    if not candidates:
        raise ValueError(f"No stable paragraph after old index {index}")
    old_index = min(candidates)
    return old_index, mapping[old_index]


def _resolve_insert_range(
    old_start: int,
    mapping: dict[int, int],
    live: list[dict[str, Any]],
) -> tuple[int, int, dict[str, Any]]:
    before_old, before_live = nearest_mapped_before(mapping, old_start)
    after_old, after_live = nearest_mapped_after(mapping, old_start)
    if before_old + 1 == after_old:
        index = live[after_live]["startIndex"]
    else:
        index = live[before_live]["endIndex"]
    return (
        index,
        index,
        {
            "before": live[before_live]["text"],
            "after": live[after_live]["text"],
            "unmapped_old": 0,
        },
    )


def _resolve_fuzzy_single_paragraph(
    old_start: int,
    old_end: int,
    mapping: dict[int, int],
    live: list[dict[str, Any]],
    old_values: list[str],
) -> tuple[int, int, dict[str, Any]] | None:
    if old_end != old_start + 1 or old_start in mapping:
        return None

    _, before_live = nearest_mapped_before(mapping, old_start)
    _, after_live = nearest_mapped_after(mapping, old_end)
    candidates = []
    for live_index in range(before_live + 1, after_live):
        ratio = difflib.SequenceMatcher(
            None,
            old_values[old_start],
            normalize(live[live_index]["text"]),
            autojunk=False,
        ).ratio()
        candidates.append((ratio, live_index))
    candidates.sort(reverse=True)
    if not candidates or candidates[0][0] < 0.85:
        return None

    best_ratio, best_live = candidates[0]
    second_ratio = candidates[1][0] if len(candidates) > 1 else 0.0
    if best_ratio - second_ratio < 0.05:
        return None

    paragraph = live[best_live]
    return (
        paragraph["startIndex"],
        paragraph["endIndex"],
        {
            "first": paragraph["text"],
            "last": paragraph["text"],
            "unmapped_old": 1,
            "fuzzy_ratio": round(best_ratio, 6),
        },
    )


def _resolve_mapped_span(
    opcode: tuple[str, int, int, int, int],
    mapping: dict[int, int],
    live: list[dict[str, Any]],
) -> tuple[int, int, dict[str, Any]]:
    _, old_start, old_end, _, _ = opcode
    mapped_inside = [mapping[index] for index in range(old_start, old_end) if index in mapping]
    first_old_is_mapped = old_start in mapping
    last_old_is_mapped = old_end - 1 in mapping

    if first_old_is_mapped:
        start = live[mapping[old_start]]["startIndex"]
    else:
        _, before_live = nearest_mapped_before(mapping, old_start)
        start = live[before_live]["endIndex"]

    if last_old_is_mapped:
        end = live[mapping[old_end - 1]]["endIndex"]
    else:
        _, after_live = nearest_mapped_after(mapping, old_end)
        end = live[after_live]["startIndex"]

    if mapped_inside and any(a >= b for a, b in zip(mapped_inside, mapped_inside[1:])):
        raise ValueError(f"Non-monotonic live mapping for opcode {opcode}")
    if start >= end:
        raise ValueError(f"Invalid live range {start}:{end} for opcode {opcode}")

    return (
        start,
        end,
        {
            "first": next(p["text"] for p in live if p["startIndex"] >= start),
            "last": next(p["text"] for p in reversed(live) if p["endIndex"] <= end),
            "unmapped_old": sum(index not in mapping for index in range(old_start, old_end)),
        },
    )


def resolve_live_range(
    opcode: tuple[str, int, int, int, int],
    mapping: dict[int, int],
    live: list[dict[str, Any]],
    old_values: list[str],
) -> tuple[int, int, dict[str, Any]]:
    tag, old_start, old_end, _, _ = opcode
    if tag == "insert":
        return _resolve_insert_range(old_start, mapping, live)

    fuzzy_range = _resolve_fuzzy_single_paragraph(old_start, old_end, mapping, live, old_values)
    if fuzzy_range is not None:
        return fuzzy_range
    return _resolve_mapped_span(opcode, mapping, live)


def _paragraph_style_request(
    paragraph: TargetParagraph,
    start: int,
    end: int,
    tab_id: str,
) -> dict[str, Any]:
    return {
        "updateParagraphStyle": {
            "range": {"startIndex": start, "endIndex": end, "tabId": tab_id},
            "paragraphStyle": {
                "namedStyleType": paragraph.named_style,
                "pageBreakBefore": paragraph.page_break_before,
            },
            "fields": "namedStyleType,pageBreakBefore",
        }
    }


def _text_style_requests(
    paragraph: TargetParagraph,
    start: int,
    tab_id: str,
) -> list[dict[str, Any]]:
    requests: list[dict[str, Any]] = []
    for run in paragraph.runs:
        text_style: dict[str, Any] = {}
        fields: list[str] = []
        if run.bold is not None:
            text_style["bold"] = run.bold
            fields.append("bold")
        if run.italic is not None:
            text_style["italic"] = run.italic
            fields.append("italic")
        if run.font_name:
            text_style["weightedFontFamily"] = {"fontFamily": run.font_name}
            fields.append("weightedFontFamily")
        if run.link_url:
            text_style["link"] = {"url": run.link_url}
            fields.append("link")
        if fields and run.end > run.start:
            requests.append(
                {
                    "updateTextStyle": {
                        "range": {
                            "startIndex": start + run.start,
                            "endIndex": start + run.end,
                            "tabId": tab_id,
                        },
                        "textStyle": text_style,
                        "fields": ",".join(fields),
                    }
                }
            )
    return requests


def _iter_list_groups(
    paragraphs: list[TargetParagraph],
) -> Iterator[tuple[int, int]]:
    group_start = 0
    while group_start < len(paragraphs):
        paragraph = paragraphs[group_start]
        if paragraph.list_kind is None:
            group_start += 1
            continue
        group_end = group_start + 1
        while (
            group_end < len(paragraphs)
            and paragraphs[group_end].list_kind == paragraph.list_kind
            and paragraphs[group_end].nesting_level == paragraph.nesting_level
        ):
            group_end += 1
        yield group_start, group_end
        group_start = group_end


def _bullet_request(
    paragraph: TargetParagraph,
    start: int,
    end: int,
    tab_id: str,
) -> dict[str, Any]:
    return {
        "createParagraphBullets": {
            "range": {"startIndex": start, "endIndex": end, "tabId": tab_id},
            "bulletPreset": (
                "NUMBERED_DECIMAL_NESTED"
                if paragraph.list_kind == "number"
                else "BULLET_DISC_CIRCLE_SQUARE"
            ),
        }
    }


def style_requests(
    paragraphs: list[TargetParagraph], start: int, tab_id: str
) -> list[dict[str, Any]]:
    if not paragraphs:
        return []

    requests: list[dict[str, Any]] = []
    full_text = "\n".join(paragraph.text for paragraph in paragraphs) + "\n"
    full_end = start + utf16_length(full_text)
    requests.append(
        {
            "deleteParagraphBullets": {
                "range": {"startIndex": start, "endIndex": full_end, "tabId": tab_id}
            }
        }
    )

    cursor = start
    paragraph_ranges: list[tuple[int, int]] = []
    for paragraph in paragraphs:
        paragraph_end = cursor + utf16_length(paragraph.text)
        style_end = paragraph_end + 1
        paragraph_ranges.append((cursor, style_end))
        requests.append(_paragraph_style_request(paragraph, cursor, style_end, tab_id))
        requests.extend(_text_style_requests(paragraph, cursor, tab_id))
        cursor = style_end

    for group_start, group_end in _iter_list_groups(paragraphs):
        paragraph = paragraphs[group_start]
        requests.append(
            _bullet_request(
                paragraph,
                paragraph_ranges[group_start][0],
                paragraph_ranges[group_end - 1][1],
                tab_id,
            )
        )

    return requests


def selected_opcodes(
    opcodes: list[tuple[str, int, int, int, int]], skip_numbers: list[int]
) -> tuple[list[tuple[int, tuple[str, int, int, int, int]]], list[int]]:
    """Return numbered opcodes to apply and the protected opcodes left for manual sync."""
    skipped = set(skip_numbers)
    selected = [
        (number, opcode) for number, opcode in enumerate(opcodes, start=1) if number not in skipped
    ]
    return selected, sorted(skipped.intersection(range(1, len(opcodes) + 1)))


def replacement_text(paragraphs: list[TargetParagraph], preserve_trailing_break: bool) -> str:
    """Build replacement text without duplicating a table-adjacent paragraph break."""
    if not paragraphs:
        return ""
    value = "\n".join(paragraph.text for paragraph in paragraphs) + "\n"
    return value[:-1] if preserve_trailing_break else value


def replacement_delete_end(end: int, preserve_trailing_break: bool) -> int:
    """Keep the final paragraph mark when it is also the boundary of a native table."""
    return end - 1 if preserve_trailing_break else end


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outline", type=Path, required=True)
    parser.add_argument("--control-inventory", type=Path, required=True)
    parser.add_argument("--old-docx", type=Path, required=True)
    parser.add_argument("--new-docx", type=Path, required=True)
    parser.add_argument("--tab-id", default="t.0")
    parser.add_argument("--revision-id", required=True)
    parser.add_argument("--allow-inline-index", type=int, action="append", default=[])
    parser.add_argument(
        "--skip-opcode",
        type=int,
        action="append",
        default=[],
        help=(
            "Exclude a numbered diff opcode from the automatic plan so protected "
            "tables or images can be updated separately."
        ),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    all_live, live = load_outline(args.outline, args.tab_id)
    old = load_docx_paragraphs(args.old_docx)
    new = load_docx_paragraphs(args.new_docx)
    old_norm = [paragraph.normalized for paragraph in old]
    new_norm = [paragraph.normalized for paragraph in new]
    live_norm = [normalize(paragraph["text"]) for paragraph in live]

    alignment = build_alignment(old_norm, live_norm)
    opcodes = [
        opcode
        for opcode in difflib.SequenceMatcher(
            None, old_norm, new_norm, autojunk=False
        ).get_opcodes()
        if opcode[0] != "equal"
    ]

    controls = json.loads(args.control_inventory.read_text(encoding="utf-8"))
    native_elements = controls["derivedControlInventory"]["nativeElements"]
    inline_indexes = {
        element["startIndex"]
        for element in native_elements
        if element["type"] == "inlineObjectElement" and element["tabId"] == args.tab_id
    }
    table_ranges = [
        (paragraph["startIndex"], paragraph["endIndex"])
        for paragraph in all_live
        if paragraph.get("table") is not None
    ]
    table_start_indexes = {
        paragraph["table"]["tableStartIndex"]
        for paragraph in all_live
        if paragraph.get("table") is not None
    }

    operations: list[dict[str, Any]] = []
    selected, skipped_opcodes = selected_opcodes(opcodes, args.skip_opcode)
    for number, opcode in selected:
        tag, old_start, old_end, new_start, new_end = opcode
        start, end, anchors = resolve_live_range(opcode, alignment, live, old_norm)
        if start != end:
            crossed_images = sorted(index for index in inline_indexes if start <= index < end)
            crossed_tables = [
                (table_start, table_end)
                for table_start, table_end in table_ranges
                if table_start < end and table_end > start
            ]
            unexpected_images = [
                index for index in crossed_images if index not in args.allow_inline_index
            ]
            if unexpected_images or crossed_tables:
                raise ValueError(
                    f"Opcode {number} crosses protected structure: "
                    f"images={unexpected_images}, tables={crossed_tables}"
                )
        operations.append(
            {
                "number": number,
                "tag": tag,
                "old_range": [old_start, old_end],
                "new_range": [new_start, new_end],
                "startIndex": start,
                "endIndex": end,
                "preserveTrailingParagraphBreak": end in table_start_indexes,
                "anchors": anchors,
                "paragraphs": new[new_start:new_end],
            }
        )

    operations.sort(key=lambda operation: operation["startIndex"], reverse=True)
    for previous, current in zip(operations, operations[1:]):
        if current["endIndex"] > previous["startIndex"]:
            raise ValueError(f"Overlapping operations {previous['number']} and {current['number']}")

    requests: list[dict[str, Any]] = []
    audit: list[dict[str, Any]] = []
    for operation in operations:
        request_start = len(requests)
        start = operation["startIndex"]
        end = operation["endIndex"]
        preserve_trailing_break = operation["preserveTrailingParagraphBreak"]
        paragraphs = operation.pop("paragraphs")
        if end > start:
            requests.append(
                {
                    "deleteContentRange": {
                        "range": {
                            "startIndex": start,
                            "endIndex": replacement_delete_end(end, preserve_trailing_break),
                            "tabId": args.tab_id,
                        }
                    }
                }
            )
        if paragraphs:
            requests.append(
                {
                    "insertText": {
                        "location": {"index": start, "tabId": args.tab_id},
                        "text": replacement_text(paragraphs, preserve_trailing_break),
                    }
                }
            )
            requests.extend(style_requests(paragraphs, start, args.tab_id))
        audit.append(
            {
                **operation,
                "requestRange": [request_start, len(requests)],
                "insertedParagraphs": len(paragraphs),
                "insertedTextPreview": paragraphs[0].text[:160] if paragraphs else "",
            }
        )

    output = {
        "revisionId": args.revision_id,
        "tabId": args.tab_id,
        "summary": {
            "oldParagraphs": len(old),
            "newParagraphs": len(new),
            "liveParagraphs": len(live),
            "changedOpcodes": len(opcodes),
            "mappedChangedOldParagraphs": sum(
                index in alignment
                for _, old_start, old_end, _, _ in opcodes
                for index in range(old_start, old_end)
            ),
            "changedOldParagraphs": sum(
                old_end - old_start for _, old_start, old_end, _, _ in opcodes
            ),
            "changedNewParagraphs": sum(
                new_end - new_start for _, _, _, new_start, new_end in opcodes
            ),
            "requests": len(requests),
            "inlineObjectsProtected": len(inline_indexes),
            "inlineObjectsExplicitlyRelocated": sorted(args.allow_inline_index),
            "tableParagraphRangesProtected": len(table_ranges),
            "skippedOpcodes": skipped_opcodes,
        },
        "audit": audit,
        "requests": requests,
    }
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(output["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
