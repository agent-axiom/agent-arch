from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
FINAL_TEMPLATE_DOCX = (
    ROOT / "docs/publisher/artifacts/agent-arch-ru-template2000n-final-2026-07-11.docx"
)
EDITORIAL_TEMPLATE_DOCX = (
    ROOT / "docs/publisher/artifacts/agent-arch-ru-template2000n-editorial-2026-07-13.docx"
)

PACKAGE_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
OFFICE_REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
DRAWING_NS = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"


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


def test_template2000n_editorial_has_semantic_styles_and_image_alt_text() -> None:
    with ZipFile(EDITORIAL_TEMPLATE_DOCX) as archive:
        document = ET.fromstring(archive.read("word/document.xml"))
        styles = ET.fromstring(archive.read("word/styles.xml"))
        relationships = ET.fromstring(archive.read("word/_rels/document.xml.rels"))

    style_ids = {
        node.attrib[f"{{{WORD_NS}}}styleId"] for node in styles.findall(f"{{{WORD_NS}}}style")
    }
    assert {
        "Title",
        "BodyText",
        "Heading1",
        "Heading2",
        "Heading3",
        "Heading4",
        "Style16",
        "Style17",
        "Style18",
        "Style20",
        "Style21",
        "Style23",
        "Style24",
        "Style28",
    } <= style_ids

    unstyled_non_empty = []
    for paragraph in document.findall(f".//{{{WORD_NS}}}p"):
        text = "".join(node.text or "" for node in paragraph.findall(f".//{{{WORD_NS}}}t")).strip()
        style = paragraph.find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}pStyle")
        if text and style is None:
            unstyled_non_empty.append(text)
    assert unstyled_non_empty == []

    image_properties = document.findall(f".//{{{DRAWING_NS}}}docPr")
    assert len(image_properties) == 49
    assert all(node.attrib.get("descr", "").strip() for node in image_properties)

    hyperlinks = [
        node
        for node in relationships.findall(f"{{{PACKAGE_REL_NS}}}Relationship")
        if node.attrib.get("Type", "").endswith("/hyperlink")
    ]
    assert len(hyperlinks) >= 100


def test_template2000n_editorial_images_have_no_alpha_channel() -> None:
    alpha_images = []
    with ZipFile(EDITORIAL_TEMPLATE_DOCX) as archive:
        for name in archive.namelist():
            if not name.startswith("word/media/") or not name.lower().endswith(".png"):
                continue
            image = archive.read(name)
            color_type = image[25]
            if color_type in {4, 6} or b"tRNS" in image:
                alpha_images.append(name)

    assert alpha_images == []
