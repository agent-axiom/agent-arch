#!/usr/bin/env python3
"""Synchronize manuscript visuals into an existing DOCX without reflowing its prose."""

from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import re
import shutil
import struct
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory
from xml.etree import ElementTree as ET

NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
}
PACKAGE_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
EMU_PER_INCH = 914_400
PNG_DENSITY = 300
MAX_FIGURE_WIDTH = int(6.5 * EMU_PER_INCH)
MAX_FIGURE_HEIGHT = int(6.3 * EMU_PER_INCH)
MAX_CODE_PARAGRAPHS_PER_KEEP_GROUP = 12
EXPECTED_MANUSCRIPT_VISUALS = 57

for prefix, uri in NS.items():
    ET.register_namespace(prefix, uri)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def png_dimensions(path: Path) -> tuple[int, int]:
    payload = path.read_bytes()[:24]
    if payload[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"Expected PNG visual: {path}")
    return struct.unpack(">II", payload[16:24])


def validate_docx_image_counts(
    raw_count: int,
    template_count: int,
    expected_count: int,
) -> None:
    if raw_count != expected_count or template_count != expected_count:
        raise ValueError(
            "Unexpected DOCX image counts: "
            f"raw={raw_count}, template={template_count}, expected={expected_count}"
        )


def parse_manuscript_visuals(manuscript: Path) -> list[dict[str, object]]:
    lines = manuscript.read_text(encoding="utf-8").splitlines()
    visuals: list[dict[str, object]] = []
    image_pattern = re.compile(r"^!\[(.*)\]\((visuals/[^)]+)\)$")
    caption_pattern = re.compile(r"^Рисунок (\d+)\. (.+)$")

    for index, line in enumerate(lines):
        image = image_pattern.fullmatch(line)
        if image is None:
            continue
        next_non_empty = next(
            (candidate for candidate in lines[index + 1 :] if candidate.strip()),
            "",
        )
        caption = caption_pattern.fullmatch(next_non_empty)
        relative_path = image.group(2)
        asset_path = manuscript.parent / relative_path
        if not asset_path.is_file():
            raise FileNotFoundError(asset_path)
        visuals.append(
            {
                "alt": image.group(1),
                "relative_path": relative_path,
                "path": asset_path,
                "figure_number": int(caption.group(1)) if caption else None,
                "figure_title": caption.group(2) if caption else None,
            }
        )

    if len(visuals) != EXPECTED_MANUSCRIPT_VISUALS:
        raise ValueError(
            f"Expected {EXPECTED_MANUSCRIPT_VISUALS} manuscript visuals, found {len(visuals)}"
        )
    numbered = [item["figure_number"] for item in visuals if item["figure_number"]]
    if numbered != list(range(1, 26)):
        raise ValueError(f"Unexpected numbered figures: {numbered}")
    return visuals


def paragraph_text(paragraph: ET.Element) -> str:
    return "".join(node.text or "" for node in paragraph.findall(".//w:t", NS)).strip()


def set_paragraph_text(paragraph: ET.Element, value: str) -> None:
    nodes = paragraph.findall(".//w:t", NS)
    if not nodes:
        raise ValueError(f"Cannot replace text in empty paragraph: {value}")
    nodes[0].text = value
    for node in nodes[1:]:
        node.text = ""


def set_paragraph_flag(paragraph: ET.Element, name: str) -> None:
    ppr = paragraph.find("w:pPr", NS)
    if ppr is None:
        ppr = ET.Element(f"{{{NS['w']}}}pPr")
        paragraph.insert(0, ppr)
    flag = ppr.find(f"w:{name}", NS)
    if flag is None:
        flag = ET.Element(f"{{{NS['w']}}}{name}")
        ppr.append(flag)
    flag.set(f"{{{NS['w']}}}val", "1")


def disable_paragraph_flag(paragraph: ET.Element, name: str) -> None:
    ppr = paragraph.find("w:pPr", NS)
    if ppr is None:
        return
    flag = ppr.find(f"w:{name}", NS)
    if flag is not None:
        flag.set(f"{{{NS['w']}}}val", "0")


def paragraph_uses_monospace_font(paragraph: ET.Element) -> bool:
    styled_characters = 0
    monospace_characters = 0
    monospace_run_seen = False
    for run in paragraph.findall("w:r", NS):
        run_text = "".join(node.text or "" for node in run.findall(".//w:t", NS))
        fonts = run.find("w:rPr/w:rFonts", NS)
        if fonts is None:
            continue
        is_monospace = any(
            "mono" in value.lower() or "courier" in value.lower()
            for value in fonts.attrib.values()
        )
        monospace_run_seen = monospace_run_seen or is_monospace
        if not run_text.strip():
            continue
        styled_characters += len(run_text)
        if is_monospace:
            monospace_characters += len(run_text)
    if styled_characters == 0:
        return monospace_run_seen
    return monospace_characters / styled_characters >= 0.8


def keep_code_blocks_together(document: ET.Element) -> tuple[int, int]:
    code_blocks = 0
    code_paragraphs = 0
    current_block: list[ET.Element] = []

    def finish_block() -> None:
        nonlocal code_blocks, code_paragraphs, current_block
        if not current_block:
            return
        code_blocks += 1
        code_paragraphs += len(current_block)
        for paragraph in current_block:
            set_paragraph_flag(paragraph, "keepLines")
        for index, paragraph in enumerate(current_block):
            keep_with_next = (
                index < len(current_block) - 1
                and (index + 1) % MAX_CODE_PARAGRAPHS_PER_KEEP_GROUP != 0
            )
            if keep_with_next:
                set_paragraph_flag(paragraph, "keepNext")
            else:
                disable_paragraph_flag(paragraph, "keepNext")
        current_block = []

    for paragraph in document.findall(".//w:body/w:p", NS):
        if paragraph_uses_monospace_font(paragraph):
            current_block.append(paragraph)
        else:
            finish_block()
    finish_block()
    return code_blocks, code_paragraphs


def remove_paragraph_numbering(paragraph: ET.Element) -> bool:
    ppr = paragraph.find("w:pPr", NS)
    if ppr is None:
        return False
    numbering = ppr.find("w:numPr", NS)
    if numbering is None:
        return False
    ppr.remove(numbering)
    return True


def remove_empty_numbered_paragraphs(document: ET.Element) -> int:
    parent_by_child = {child: parent for parent in document.iter() for child in list(parent)}
    removed = 0
    for paragraph in document.findall(".//w:p", NS):
        if paragraph_text(paragraph) or paragraph.find(".//w:drawing", NS) is not None:
            continue
        if paragraph.find("w:pPr/w:numPr", NS) is None:
            continue
        parent = parent_by_child.get(paragraph)
        if parent is None:
            raise ValueError("Empty numbered paragraph has no document parent")
        parent.remove(paragraph)
        removed += 1
    return removed


def on_off_property_is_active(element: ET.Element | None) -> bool:
    return element is not None and element.get(f"{{{NS['w']}}}val", "1") not in {
        "0",
        "false",
        "off",
    }


def remove_empty_paragraphs_before_page_breaks(document: ET.Element) -> int:
    body = document.find("w:body", NS)
    if body is None:
        raise ValueError("DOCX document has no body")
    removed = 0
    index = 1
    while index < len(body):
        paragraph = body[index]
        page_break = paragraph.find("w:pPr/w:pageBreakBefore", NS)
        if paragraph.tag != f"{{{NS['w']}}}p" or not on_off_property_is_active(page_break):
            index += 1
            continue
        previous = body[index - 1]
        if (
            previous.tag == f"{{{NS['w']}}}p"
            and not paragraph_text(previous)
            and previous.find(".//w:drawing", NS) is None
            and previous.find(".//w:pict", NS) is None
            and previous.find(".//w:sectPr", NS) is None
            and previous.find(".//w:bookmarkStart", NS) is None
        ):
            body.remove(previous)
            removed += 1
            index -= 1
            continue
        index += 1
    return removed


def set_table_row_flag(row: ET.Element, name: str) -> bool:
    row_properties = row.find("w:trPr", NS)
    if row_properties is None:
        row_properties = ET.Element(f"{{{NS['w']}}}trPr")
        row.insert(0, row_properties)
    flag = row_properties.find(f"w:{name}", NS)
    created = flag is None
    if flag is None:
        flag = ET.Element(f"{{{NS['w']}}}{name}")
        row_properties.append(flag)
    flag.set(f"{{{NS['w']}}}val", "1")
    return created


def normalize_table_rows(document: ET.Element) -> tuple[int, int]:
    headers = 0
    rows_kept_together = 0
    for table in document.findall(".//w:tbl", NS):
        for row_index, row in enumerate(table.findall("w:tr", NS)):
            set_table_row_flag(row, "cantSplit")
            rows_kept_together += 1
            if row_index == 0:
                set_table_row_flag(row, "tblHeader")
                headers += 1
    return headers, rows_kept_together


def previous_non_empty_paragraph(
    parent: ET.Element,
    start: ET.Element,
) -> ET.Element | None:
    children = list(parent)
    start_index = children.index(start)
    return next(
        (
            candidate
            for candidate in reversed(children[:start_index])
            if candidate.tag == f"{{{NS['w']}}}p" and paragraph_text(candidate)
        ),
        None,
    )


def find_nearby_paragraph(
    parent: ET.Element,
    start: ET.Element,
    pattern: re.Pattern[str],
) -> ET.Element:
    children = list(parent)
    start_index = children.index(start)
    for candidates in (
        reversed(children[:start_index]),
        iter(children[start_index + 1 :]),
    ):
        checked = 0
        for candidate in candidates:
            if candidate.tag != f"{{{NS['w']}}}p":
                continue
            text = paragraph_text(candidate)
            if not text:
                continue
            checked += 1
            if pattern.match(text):
                return candidate
            if checked >= 4:
                break
    raise ValueError(f"Nearby paragraph not found for pattern {pattern.pattern}")


def resize_drawing(drawing: ET.Element, image_path: Path) -> tuple[int, int]:
    pixel_width, pixel_height = png_dimensions(image_path)
    extent = drawing.find(".//wp:extent", NS)
    if extent is None:
        raise ValueError("Drawing has no wp:extent")
    existing_width = int(extent.get("cx", "0"))
    if existing_width <= 0:
        raise ValueError("Drawing width is missing")
    max_width_for_height = MAX_FIGURE_HEIGHT * pixel_width // pixel_height
    native_width = pixel_width * EMU_PER_INCH // PNG_DENSITY
    width = min(MAX_FIGURE_WIDTH, max_width_for_height, native_width)
    height = round(width * pixel_height / pixel_width)
    if height > MAX_FIGURE_HEIGHT:
        raise ValueError("Deterministic image scaling exceeded the height limit")

    extent.set("cx", str(width))
    extent.set("cy", str(height))
    for shape_extent in drawing.findall(".//a:xfrm/a:ext", NS):
        shape_extent.set("cx", str(width))
        shape_extent.set("cy", str(height))
    return width, height


def synchronize(
    input_docx: Path,
    manuscript: Path,
    output_docx: Path,
) -> dict[str, object]:
    visuals = parse_manuscript_visuals(manuscript)

    with TemporaryDirectory() as temporary_directory:
        root = Path(temporary_directory) / "docx"
        root.mkdir()
        with zipfile.ZipFile(input_docx) as archive:
            archive.extractall(root)

        document_path = root / "word/document.xml"
        relationships_path = root / "word/_rels/document.xml.rels"
        document = ET.fromstring(document_path.read_bytes())
        relationships = ET.fromstring(relationships_path.read_bytes())
        table_headers_repeated, table_rows_kept_together = normalize_table_rows(document)
        empty_numbered_paragraphs_removed = remove_empty_numbered_paragraphs(document)
        empty_paragraphs_before_page_breaks_removed = (
            remove_empty_paragraphs_before_page_breaks(document)
        )
        code_blocks_kept_together, code_paragraphs_kept_together = keep_code_blocks_together(
            document
        )
        targets = {
            node.attrib["Id"]: posixpath.normpath(f"word/{node.attrib['Target']}")
            for node in relationships.findall(f"{{{PACKAGE_REL_NS}}}Relationship")
            if node.attrib.get("Type", "").endswith("/image")
        }

        parent_by_child = {child: parent for parent in document.iter() for child in list(parent)}
        drawings: list[tuple[ET.Element, ET.Element, ET.Element]] = []
        for paragraph in document.findall(".//w:p", NS):
            for drawing in paragraph.findall(".//w:drawing", NS):
                blip = drawing.find(".//a:blip", NS)
                if blip is not None:
                    drawings.append((paragraph, drawing, blip))

        if len(drawings) != len(visuals):
            raise ValueError(
                f"DOCX has {len(drawings)} drawings; manuscript has {len(visuals)} visuals"
            )

        media_targets: list[str] = []
        figure_heights: list[int] = []
        inline_visual_titles_kept = 0
        image_numbering_removed = 0
        for visual, (paragraph, drawing, blip) in zip(visuals, drawings):
            relationship_id = blip.get(f"{{{NS['r']}}}embed", "")
            target = targets.get(relationship_id)
            if target is None:
                raise ValueError(f"Image relationship is missing: {relationship_id}")
            destination = root / target
            source = Path(visual["path"])
            destination.write_bytes(source.read_bytes())
            media_targets.append(target)

            width, height = resize_drawing(drawing, source)
            if remove_paragraph_numbering(paragraph):
                image_numbering_removed += 1
            if visual["figure_number"]:
                figure_heights.append(height)

            for properties in drawing.findall(".//wp:docPr", NS):
                properties.set("title", "Иллюстрация к рукописи")
                properties.set("descr", str(visual["alt"])[:1000])

            number = visual["figure_number"]
            if not number:
                parent = parent_by_child.get(paragraph)
                if parent is None:
                    raise ValueError("Inline visual has no document parent")
                title = previous_non_empty_paragraph(parent, paragraph)
                if title is not None and paragraph_text(title) == visual["alt"]:
                    set_paragraph_flag(title, "keepNext")
                    inline_visual_titles_kept += 1
                continue
            parent = parent_by_child.get(paragraph)
            if parent is None:
                raise ValueError(f"Figure {number} has no document parent")
            caption = find_nearby_paragraph(
                parent,
                paragraph,
                re.compile(rf"^Рисунок {number}\."),
            )
            title = str(visual["figure_title"])
            set_paragraph_text(caption, f"Рисунок {number}. {title}")
            set_paragraph_flag(paragraph, "keepNext")
            set_paragraph_flag(caption, "keepLines")
            parent.remove(caption)
            image_index = list(parent).index(paragraph)
            parent.insert(image_index + 1, caption)

        if len(set(media_targets)) != len(media_targets):
            raise ValueError("Multiple drawings unexpectedly share one media target")

        document_path.write_bytes(ET.tostring(document, encoding="utf-8", xml_declaration=True))

        temporary_output = Path(temporary_directory) / "output.docx"
        with zipfile.ZipFile(
            temporary_output,
            "w",
            compression=zipfile.ZIP_DEFLATED,
        ) as archive:
            for path in sorted(root.rglob("*")):
                if path.is_file():
                    archive.write(path, path.relative_to(root).as_posix())

        output_docx.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(temporary_output, output_docx)

    return {
        "input_docx": str(input_docx),
        "manuscript": str(manuscript),
        "output_docx": str(output_docx),
        "output_bytes": output_docx.stat().st_size,
        "output_sha256": sha256(output_docx),
        "visuals_synchronized": len(visuals),
        "numbered_figures_reordered": len(figure_heights),
        "media_targets_unique": len(media_targets),
        "table_headers_repeated": table_headers_repeated,
        "table_rows_kept_together": table_rows_kept_together,
        "empty_numbered_paragraphs_removed": empty_numbered_paragraphs_removed,
        "empty_paragraphs_before_page_breaks_removed": (
            empty_paragraphs_before_page_breaks_removed
        ),
        "code_blocks_kept_together": code_blocks_kept_together,
        "code_paragraphs_kept_together": code_paragraphs_kept_together,
        "image_numbering_removed": image_numbering_removed,
        "inline_visual_titles_kept": inline_visual_titles_kept,
        "max_numbered_figure_height_inches": round(
            max(figure_heights) / EMU_PER_INCH,
            3,
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-docx", required=True, type=Path)
    parser.add_argument("--manuscript", required=True, type=Path)
    parser.add_argument("--output-docx", required=True, type=Path)
    parser.add_argument("--metrics-json", type=Path)
    args = parser.parse_args()

    metrics = synchronize(args.input_docx, args.manuscript, args.output_docx)
    payload = json.dumps(metrics, ensure_ascii=False, indent=2, sort_keys=True)
    if args.metrics_json:
        args.metrics_json.write_text(payload + "\n", encoding="utf-8")
    print(payload)


if __name__ == "__main__":
    main()
