#!/usr/bin/env python3
"""Audit publisher font declarations and embedded font registrations."""

from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from docx import Document

WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
OFFICE_REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PACKAGE_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"


def style_font(document: Document, style_name: str) -> dict[str, object]:
    style = document.styles[style_name]
    return {
        "style": style_name,
        "font": style.font.name,
        "size_points": style.font.size.pt if style.font.size else None,
    }


def embedded_registrations(path: Path) -> tuple[list[str], int, bool]:
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
        font_table = ET.fromstring(archive.read("word/fontTable.xml"))
        relationships = ET.fromstring(archive.read("word/_rels/fontTable.xml.rels"))
        numbering = archive.read("word/numbering.xml")

    relationship_targets = {
        node.attrib["Id"]: node.attrib["Target"]
        for node in relationships.findall(f"{{{PACKAGE_REL_NS}}}Relationship")
        if node.attrib.get("Type", "").endswith("/font")
    }
    registrations: list[str] = []
    registered_ids: set[str] = set()
    for font in font_table.findall(f"{{{WORD_NS}}}font"):
        name = font.attrib[f"{{{WORD_NS}}}name"]
        for variant in ("embedRegular", "embedBold", "embedItalic", "embedBoldItalic"):
            node = font.find(f"{{{WORD_NS}}}{variant}")
            if node is None:
                continue
            relationship_id = node.attrib[f"{{{OFFICE_REL_NS}}}id"]
            registered_ids.add(relationship_id)
            registrations.append(f"{name} {variant.removeprefix('embed')}")

    targets_exist = registered_ids == relationship_targets.keys() and all(
        f"word/{target}" in names for target in relationship_targets.values()
    )
    numbering_is_clean = b"Noto Sans Symbols" not in numbering
    return registrations, len(relationship_targets), targets_exist and numbering_is_clean


def audit(path: Path) -> dict[str, object]:
    document = Document(str(path))
    body = style_font(document, "Normal")
    program = style_font(document, "Программа")
    registrations, embedded_files, registrations_valid = embedded_registrations(path)

    expected_registrations = {
        "Noto Sans Symbols Regular",
        "Noto Sans Symbols Bold",
        "Roboto Mono Regular",
        "Roboto Mono Bold",
        "Roboto Mono Italic",
        "Roboto Mono BoldItalic",
    }
    passed = (
        body == {"style": "Normal", "font": "Times New Roman", "size_points": 10.0}
        and program == {"style": "Программа", "font": "Courier New", "size_points": 9.0}
        and set(registrations) == expected_registrations
        and embedded_files == 6
        and registrations_valid
    )
    return {
        "schema_version": 1,
        "input": str(path),
        "template_body_style": body,
        "template_program_style": program,
        "embedded_font_registrations": registrations,
        "embedded_font_files": embedded_files,
        "registrations_and_targets_valid": registrations_valid,
        "passed": passed,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--output-json", required=True, type=Path)
    args = parser.parse_args()

    result = audit(args.input)
    args.output_json.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
