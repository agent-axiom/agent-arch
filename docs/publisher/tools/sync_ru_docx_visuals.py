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
MAX_FIGURE_HEIGHT = int(5.6 * EMU_PER_INCH)
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
    if ppr.find(f"w:{name}", NS) is None:
        ppr.append(ET.Element(f"{{{NS['w']}}}{name}"))


def find_preceding_paragraph(
    parent: ET.Element,
    start: ET.Element,
    pattern: re.Pattern[str],
) -> ET.Element:
    children = list(parent)
    start_index = children.index(start)
    checked = 0
    for candidate in reversed(children[:start_index]):
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
    raise ValueError(f"Preceding paragraph not found for pattern {pattern.pattern}")


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
    width = int(extent.get("cx", "0"))
    if width <= 0:
        raise ValueError("Drawing width is missing")
    height = round(width * pixel_height / pixel_width)
    if height > MAX_FIGURE_HEIGHT:
        scale = MAX_FIGURE_HEIGHT / height
        width = round(width * scale)
        height = MAX_FIGURE_HEIGHT

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
            if visual["figure_number"]:
                figure_heights.append(height)

            for properties in drawing.findall(".//wp:docPr", NS):
                properties.set("title", "Иллюстрация к рукописи")
                properties.set("descr", str(visual["alt"])[:1000])

            number = visual["figure_number"]
            if not number:
                continue
            parent = parent_by_child.get(paragraph)
            if parent is None:
                raise ValueError(f"Figure {number} has no document parent")
            caption = find_nearby_paragraph(
                parent,
                paragraph,
                re.compile(rf"^Рисунок {number}\."),
            )
            reference = find_preceding_paragraph(
                parent,
                caption,
                re.compile(rf"^На рисунке {number} представлена схема"),
            )
            title = str(visual["figure_title"])
            set_paragraph_text(caption, f"Рисунок {number}. {title}")
            set_paragraph_text(
                reference,
                f"На рисунке {number} представлена схема «{title}».",
            )
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
