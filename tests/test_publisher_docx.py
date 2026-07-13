from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
FINAL_TEMPLATE_DOCX = (
    ROOT / "docs/publisher/artifacts/agent-arch-ru-template2000n-final-2026-07-11.docx"
)

PACKAGE_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
OFFICE_REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def test_template2000n_final_preserves_embedded_font_registrations() -> None:
    with ZipFile(FINAL_TEMPLATE_DOCX) as archive:
        names = set(archive.namelist())
        font_table = ET.fromstring(archive.read("word/fontTable.xml"))
        relationships = ET.fromstring(archive.read("word/_rels/fontTable.xml.rels"))
        numbering_xml = archive.read("word/numbering.xml")

    font_relationships = {
        node.attrib["Id"]: node.attrib["Target"]
        for node in relationships.findall(f"{{{PACKAGE_REL_NS}}}Relationship")
        if node.attrib.get("Type", "").endswith("/font")
    }
    registered_relationships = {
        node.attrib[f"{{{OFFICE_REL_NS}}}id"]
        for tag in ("embedRegular", "embedBold", "embedItalic", "embedBoldItalic")
        for node in font_table.findall(f".//{{{WORD_NS}}}{tag}")
    }

    assert font_relationships
    assert font_relationships.keys() == registered_relationships
    assert {f"word/{target}" for target in font_relationships.values()} <= names
    font_names = {
        node.attrib[f"{{{WORD_NS}}}name"] for node in font_table.findall(f"{{{WORD_NS}}}font")
    }
    assert "Roboto Mono" in font_names
    assert b"Noto Sans Symbols" not in numbering_xml
