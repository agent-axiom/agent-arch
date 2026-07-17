import ast
import hashlib
import posixpath
import re
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

import pytest

from docs.publisher.tools import sync_ru_docx_visuals

ROOT = Path(__file__).resolve().parents[1]
EDITORIAL_BUILDER = ROOT / "docs/publisher/tools/build_ru_editorial_docx.py"
RAW_EDITORIAL_DOCX = (
    ROOT
    / (
        "docs/publisher/artifacts/"
        "agent-arch-ru-google-doc-editorial-final-polish-2026-07-17.docx"
    )
)
EDITORIAL_TEMPLATE_DOCX = (
    ROOT
    / (
        "docs/publisher/artifacts/"
        "agent-arch-ru-template2000n-editorial-final-polish-2026-07-17.docx"
    )
)
EDITORIAL_MANUSCRIPT = ROOT / "docs/publisher/ru-manuscript-editorial-2026-07-13.md"

PACKAGE_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
OFFICE_REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
DRAWING_NS = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
DRAWINGML_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"


def test_visual_audit_accepts_every_current_manuscript_image() -> None:
    assert len(sync_ru_docx_visuals.parse_manuscript_visuals(EDITORIAL_MANUSCRIPT)) == 56


def test_visual_audit_uses_the_parsed_manuscript_count_for_docx_validation() -> None:
    validate = getattr(sync_ru_docx_visuals, "validate_docx_image_counts", None)

    assert validate is not None
    validate(56, 56, 56)
    with pytest.raises(ValueError, match="raw=55, template=56, expected=56"):
        validate(55, 56, 56)


def test_editorial_builder_knows_all_eight_part_boundaries() -> None:
    tree = ast.parse(EDITORIAL_BUILDER.read_text(encoding="utf-8"))
    assignment = next(
        node
        for node in tree.body
        if isinstance(node, ast.Assign)
        and any(
            isinstance(target, ast.Name) and target.id == "FIRST_CHAPTERS_IN_PART"
            for target in node.targets
        )
    )
    assert ast.literal_eval(assignment.value) == {1, 4, 7, 10, 13, 17, 22, 26}


def ordered_embedded_images(path: Path) -> tuple[list[str], list[str]]:
    with ZipFile(path) as archive:
        document = ET.fromstring(archive.read("word/document.xml"))
        relationships = ET.fromstring(archive.read("word/_rels/document.xml.rels"))
        targets = {
            node.attrib["Id"]: posixpath.normpath(f"word/{node.attrib['Target']}")
            for node in relationships.findall(f"{{{PACKAGE_REL_NS}}}Relationship")
            if node.attrib.get("Type", "").endswith("/image")
        }
        ordered_targets = [
            targets[blip.attrib[f"{{{OFFICE_REL_NS}}}embed"]]
            for blip in document.findall(f".//{{{DRAWINGML_NS}}}blip")
        ]
        hashes = [hashlib.sha256(archive.read(target)).hexdigest() for target in ordered_targets]
    return ordered_targets, hashes


def test_template2000n_final_preserves_embedded_font_registrations() -> None:
    with ZipFile(EDITORIAL_TEMPLATE_DOCX) as archive:
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
    assert len(image_properties) == 56
    assert all(node.attrib.get("descr", "").strip() for node in image_properties)

    hyperlinks = [
        node
        for node in relationships.findall(f"{{{PACKAGE_REL_NS}}}Relationship")
        if node.attrib.get("Type", "").endswith("/hyperlink")
    ]
    assert len(document.findall(f".//{{{WORD_NS}}}hyperlink")) >= 120
    assert len(hyperlinks) >= 90


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


def test_current_docx_exports_match_the_28_chapter_manuscript() -> None:
    for docx_path in (RAW_EDITORIAL_DOCX, EDITORIAL_TEMPLATE_DOCX):
        with ZipFile(docx_path) as archive:
            document = ET.fromstring(archive.read("word/document.xml"))

        paragraph_nodes = document.findall(f".//{{{WORD_NS}}}p")
        paragraphs = [
            "".join(node.text or "" for node in paragraph.findall(f".//{{{WORD_NS}}}t"))
            for paragraph in paragraph_nodes
        ]
        chapter_numbers = [
            int(match.group(1))
            for paragraph, paragraph_node in zip(paragraphs, paragraph_nodes)
            if (
                (style := paragraph_node.find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}pStyle"))
                is not None
                and style.attrib.get(f"{{{WORD_NS}}}val") == "Heading2"
                and (match := re.fullmatch(r"Глава (\d+)\. .+", paragraph.strip()))
            )
        ]
        text = "\n".join(paragraphs)

        assert chapter_numbers == list(range(1, 29))
        assert "create_support_ticket" not in text
        assert "Покрытие обязательным подтверждением и трассировкой" in text
        assert "except GatewayTimeout" in text
        assert len(re.findall(r"^На рисунке \d+ представлена схема", text, re.MULTILINE)) == 25
        assert "дата доступа зафиксированы 15 июля 2026 года" in text
        assert "дата доступа зафиксированы 14 июля 2026 года" not in text
        assert text.count("После главы вы сможете:") == 28
        assert text.count("Артефакт главы:") == 28
        assert text.count("Предварительные условия.") == 8
        assert text.count("Отрицательная проверка.") == 8
        assert len(re.findall(r"Листинг \d+\.", text)) >= 30
        assert "agentic_internal_risk:" in text
        assert "control_plane_readiness:" in text


def test_editorial_page_breaks_only_start_reader_facing_sections() -> None:
    for docx_path in (RAW_EDITORIAL_DOCX, EDITORIAL_TEMPLATE_DOCX):
        with ZipFile(docx_path) as archive:
            document = ET.fromstring(archive.read("word/document.xml"))

        paragraphs = document.findall(f".//{{{WORD_NS}}}p")
        page_breaks = []
        previous_text = None
        for paragraph in paragraphs:
            text = "".join(
                node.text or "" for node in paragraph.findall(f".//{{{WORD_NS}}}t")
            ).strip()
            page_break = paragraph.find(
                f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}pageBreakBefore"
            )
            if page_break is not None:
                value = page_break.attrib.get(f"{{{WORD_NS}}}val", "true")
                if value not in {"false", "0", "off"}:
                    style = paragraph.find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}pStyle")
                    page_breaks.append((text, style.attrib.get(f"{{{WORD_NS}}}val")))
                    assert text
                    assert previous_text
            previous_text = text

        assert len(page_breaks) == 30
        assert all(style in {"Heading1", "Heading2"} for _, style in page_breaks)


def test_raw_docx_embeds_the_exact_visual_assets_in_manuscript_order() -> None:
    manuscript = EDITORIAL_MANUSCRIPT.read_text(encoding="utf-8")
    relative_paths = re.findall(
        r"^!\[[^\]]+\]\((visuals/[^)]+)\)$", manuscript, re.MULTILINE
    )
    expected_hashes = [
        hashlib.sha256((EDITORIAL_MANUSCRIPT.parent / path).read_bytes()).hexdigest()
        for path in relative_paths
    ]
    raw_targets, raw_hashes = ordered_embedded_images(RAW_EDITORIAL_DOCX)
    template_targets, _ = ordered_embedded_images(EDITORIAL_TEMPLATE_DOCX)

    assert len(relative_paths) == 56
    assert raw_hashes == expected_hashes
    assert template_targets == raw_targets


def test_numbered_figure_captions_follow_images_and_stay_with_them() -> None:
    with ZipFile(EDITORIAL_TEMPLATE_DOCX) as archive:
        document = ET.fromstring(archive.read("word/document.xml"))

    paragraphs = document.findall(f".//{{{WORD_NS}}}p")
    numbered_pairs = 0
    for index, paragraph in enumerate(paragraphs):
        if paragraph.find(f".//{{{DRAWING_NS}}}docPr") is None:
            continue
        next_paragraph = next(
            (
                candidate
                for candidate in paragraphs[index + 1 :]
                if "".join(
                    node.text or ""
                    for node in candidate.findall(f".//{{{WORD_NS}}}t")
                ).strip()
            ),
            None,
        )
        assert next_paragraph is not None
        next_text = "".join(
            node.text or "" for node in next_paragraph.findall(f".//{{{WORD_NS}}}t")
        ).strip()
        if re.fullmatch(r"Рисунок \d+\. .+", next_text) is None:
            continue

        numbered_pairs += 1
        image_style = paragraph.find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}pStyle")
        caption_style = next_paragraph.find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}pStyle")
        assert image_style is not None
        assert image_style.attrib[f"{{{WORD_NS}}}val"] == "Style28"
        assert paragraph.find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}keepNext") is not None
        assert caption_style is not None
        assert caption_style.attrib[f"{{{WORD_NS}}}val"] == "Style17"
        assert next_paragraph.find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}keepLines") is not None

    assert numbered_pairs == 25
