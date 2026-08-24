#!/usr/bin/env python3
"""Place numbered Russian figure captions immediately after their images."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
DRAWING_NS = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
NS = {"w": WORD_NS, "wp": DRAWING_NS}
CAPTION_PATTERN = re.compile(r"^Рисунок (\d+)\. .+")
EXPECTED_CAPTIONS = 25


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def paragraph_text(paragraph: ET.Element) -> str:
    return "".join(node.text or "" for node in paragraph.findall(".//w:t", NS)).strip()


def has_drawing(paragraph: ET.Element) -> bool:
    return paragraph.find(".//w:drawing", NS) is not None


def significant_sibling(
    parent: ET.Element,
    start_index: int,
    direction: int,
) -> ET.Element | None:
    children = list(parent)
    index = start_index + direction
    while 0 <= index < len(children):
        candidate = children[index]
        if candidate.tag == f"{{{WORD_NS}}}p" and (
            paragraph_text(candidate) or has_drawing(candidate)
        ):
            return candidate
        index += direction
    return None


def normalize_document_xml(payload: bytes) -> tuple[bytes, dict[str, object]]:
    for _, namespace in ET.iterparse(io.BytesIO(payload), events=("start-ns",)):
        prefix, uri = namespace
        if prefix != "xml":
            ET.register_namespace(prefix, uri)
    document = ET.fromstring(payload)
    parent_by_child = {
        child: parent for parent in document.iter() for child in list(parent)
    }
    captions: list[tuple[int, ET.Element, ET.Element]] = []
    for paragraph in document.findall(".//w:p", NS):
        match = CAPTION_PATTERN.fullmatch(paragraph_text(paragraph))
        if match:
            parent = parent_by_child.get(paragraph)
            if parent is None:
                raise ValueError(f"Figure caption {match.group(1)} has no parent")
            captions.append((int(match.group(1)), paragraph, parent))

    numbers = [number for number, _, _ in captions]
    if numbers != list(range(1, EXPECTED_CAPTIONS + 1)):
        raise ValueError(f"Unexpected numbered figure captions: {numbers}")

    moved = 0
    already_after = 0
    for number, caption, parent in captions:
        caption_index = list(parent).index(caption)
        previous = significant_sibling(parent, caption_index, -1)
        following = significant_sibling(parent, caption_index, 1)
        if previous is not None and has_drawing(previous):
            already_after += 1
            continue
        if following is None or not has_drawing(following):
            raise ValueError(f"No adjacent image found for figure caption {number}")
        parent.remove(caption)
        parent.insert(list(parent).index(following) + 1, caption)
        moved += 1

    for number, caption, parent in captions:
        previous = significant_sibling(parent, list(parent).index(caption), -1)
        if previous is None or not has_drawing(previous):
            raise ValueError(f"Figure caption {number} does not follow its image")

    normalized = ET.tostring(
        document,
        encoding="UTF-8",
        xml_declaration=True,
    )
    return normalized, {
        "numbered_captions": len(captions),
        "captions_moved": moved,
        "captions_already_after_images": already_after,
        "captions_after_images": len(captions),
    }


def normalize_docx(input_docx: Path, output_docx: Path) -> dict[str, object]:
    if input_docx.resolve() == output_docx.resolve():
        raise ValueError("Input and output DOCX paths must differ")
    with zipfile.ZipFile(input_docx) as source:
        source.testzip()
        document_xml, metrics = normalize_document_xml(source.read("word/document.xml"))
        output_docx.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            dir=output_docx.parent,
            prefix=f".{output_docx.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary:
            temporary_path = Path(temporary.name)
        try:
            with zipfile.ZipFile(temporary_path, "w") as destination:
                for info in source.infolist():
                    payload = (
                        document_xml
                        if info.filename == "word/document.xml"
                        else source.read(info)
                    )
                    destination.writestr(info, payload)
            temporary_path.replace(output_docx)
        finally:
            temporary_path.unlink(missing_ok=True)

    with zipfile.ZipFile(output_docx) as result:
        invalid_entry = result.testzip()
        if invalid_entry is not None:
            raise ValueError(f"Invalid DOCX entry after normalization: {invalid_entry}")
    return {
        "input_docx": str(input_docx),
        "output_docx": str(output_docx),
        "output_bytes": output_docx.stat().st_size,
        "output_sha256": sha256(output_docx),
        **metrics,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-docx", required=True, type=Path)
    parser.add_argument("--output-docx", required=True, type=Path)
    parser.add_argument("--metrics-json", type=Path)
    args = parser.parse_args()

    metrics = normalize_docx(args.input_docx, args.output_docx)
    payload = json.dumps(metrics, ensure_ascii=False, indent=2, sort_keys=True)
    if args.metrics_json:
        args.metrics_json.parent.mkdir(parents=True, exist_ok=True)
        args.metrics_json.write_text(payload + "\n", encoding="utf-8")
    print(payload)


if __name__ == "__main__":
    main()
