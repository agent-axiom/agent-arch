#!/usr/bin/env python3
"""Build a macro-free Template2000n DOCX derivative from a raw Google Docs DOCX."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import zipfile
from collections import Counter
from pathlib import Path
from tempfile import TemporaryDirectory
from xml.etree import ElementTree as ET

from docx import Document


NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
ET.register_namespace("w", NS["w"])


STYLE_PARTS = {
    "word/styles.xml",
    "word/fontTable.xml",
    "word/theme/theme1.xml",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def paragraph_texts(path: Path) -> list[str]:
    return [paragraph.text for paragraph in Document(str(path)).paragraphs]


def word_count(texts: list[str]) -> int:
    return sum(len(text.split()) for text in texts)


def style_counts(path: Path) -> Counter[str]:
    counts: Counter[str] = Counter()
    doc = Document(str(path))
    for paragraph in doc.paragraphs:
        style = paragraph.style.name if paragraph.style is not None else "<none>"
        counts[style] += 1
    return counts


def remove_heading_numbering(styles_xml: bytes) -> bytes:
    root = ET.fromstring(styles_xml)
    for style in root.findall("w:style", NS):
        style_id = style.get(f"{{{NS['w']}}}styleId", "")
        if style_id not in {"Heading1", "Heading2", "Heading3", "Heading4", "Heading5"}:
            continue
        ppr = style.find("w:pPr", NS)
        if ppr is None:
            continue
        for numpr in list(ppr.findall("w:numPr", NS)):
            ppr.remove(numpr)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def map_bodytext(document_xml: bytes) -> tuple[bytes, int]:
    root = ET.fromstring(document_xml)
    changed = 0
    for paragraph in root.findall(".//w:p", NS):
        texts = [node.text or "" for node in paragraph.findall(".//w:t", NS)]
        if not "".join(texts).strip():
            continue
        ppr = paragraph.find("w:pPr", NS)
        if ppr is not None and ppr.find("w:pStyle", NS) is not None:
            continue
        if ppr is None:
            ppr = ET.Element(f"{{{NS['w']}}}pPr")
            paragraph.insert(0, ppr)
        pstyle = ET.Element(f"{{{NS['w']}}}pStyle")
        pstyle.set(f"{{{NS['w']}}}val", "BodyText")
        ppr.insert(0, pstyle)
        changed += 1
    return ET.tostring(root, encoding="utf-8", xml_declaration=True), changed


def build(raw_docx: Path, template_docx: Path, output_docx: Path) -> dict[str, object]:
    with TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        raw_dir = tmpdir / "raw"
        template_dir = tmpdir / "template"
        raw_dir.mkdir()
        template_dir.mkdir()

        with zipfile.ZipFile(raw_docx) as zf:
            zf.extractall(raw_dir)
        with zipfile.ZipFile(template_docx) as zf:
            zf.extractall(template_dir)

        for part in STYLE_PARTS:
            src = template_dir / part
            dst = raw_dir / part
            if not src.exists():
                raise FileNotFoundError(f"Template part missing: {part}")
            if part == "word/styles.xml":
                dst.write_bytes(remove_heading_numbering(src.read_bytes()))
            else:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(src, dst)

        document_xml = raw_dir / "word" / "document.xml"
        mapped_xml, bodytext_mapped = map_bodytext(document_xml.read_bytes())
        document_xml.write_bytes(mapped_xml)

        if output_docx.exists():
            output_docx.unlink()
        with zipfile.ZipFile(output_docx, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for path in sorted(raw_dir.rglob("*")):
                if path.is_file():
                    zf.write(path, path.relative_to(raw_dir).as_posix())

    raw_texts = paragraph_texts(raw_docx)
    output_texts = paragraph_texts(output_docx)
    equal_text = raw_texts == output_texts
    if not equal_text:
        raise AssertionError("Raw and Template2000n paragraph text differ")

    raw_counts = style_counts(raw_docx)
    output_counts = style_counts(output_docx)
    return {
        "raw_docx": str(raw_docx),
        "template_docx": str(template_docx),
        "output_docx": str(output_docx),
        "output_bytes": output_docx.stat().st_size,
        "output_sha256": sha256(output_docx),
        "paragraphs": len(output_texts),
        "non_empty_paragraphs": sum(1 for text in output_texts if text.strip()),
        "approximate_words": word_count(output_texts),
        "bodytext_mapped": bodytext_mapped,
        "text_equality": equal_text,
        "raw_style_counts": dict(raw_counts),
        "output_style_counts": dict(output_counts),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-docx", required=True, type=Path)
    parser.add_argument("--template-docx", required=True, type=Path)
    parser.add_argument("--output-docx", required=True, type=Path)
    parser.add_argument("--metrics-json", type=Path)
    args = parser.parse_args()

    metrics = build(args.raw_docx, args.template_docx, args.output_docx)
    payload = json.dumps(metrics, ensure_ascii=False, indent=2, sort_keys=True)
    if args.metrics_json:
        args.metrics_json.write_text(payload + "\n", encoding="utf-8")
    print(payload)


if __name__ == "__main__":
    main()
