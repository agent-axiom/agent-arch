import ast
import hashlib
import os
import posixpath
import re
import subprocess
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
        "agent-arch-ru-google-doc-final-reader-copyedit-2026-07-23.docx"
    )
)
EDITORIAL_TEMPLATE_DOCX = (
    ROOT
    / (
        "docs/publisher/artifacts/"
        "agent-arch-ru-template2000n-final-reader-copyedit-2026-07-23.docx"
    )
)
EDITORIAL_MANUSCRIPT = ROOT / "docs/publisher/ru-manuscript-editorial-2026-07-13.md"

PACKAGE_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
OFFICE_REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
DRAWING_NS = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
DRAWINGML_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
DC_NS = "http://purl.org/dc/elements/1.1/"
CP_NS = "http://schemas.openxmlformats.org/package/2006/metadata/core-properties"


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


def test_editorial_renderer_adds_resolvable_internal_bookmarks_and_links(
    tmp_path: Path,
) -> None:
    runtime_python = Path(
        os.environ.get(
            "CODEX_DOCUMENT_PYTHON",
            Path.home()
            / ".cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3",
        )
    )
    if not runtime_python.is_file():
        pytest.skip("bundled document runtime is unavailable")

    output = tmp_path / "internal-links.docx"
    script = r'''
import sys
from pathlib import Path
from docx import Document
from lxml import html

sys.path.insert(0, sys.argv[1])
from docs.publisher.tools import build_ru_editorial_docx

document = Document()
root = html.fragment_fromstring(
    """
    <h2>Глава 1. Начало</h2>
    <p>Продолжение находится в главе 16; см. рисунок 3, таблицу 4 и листинг 12.</p>
    <h2>Глава 16. Доказательства</h2>
    <p>Рисунок 3. Цепочка доказательств</p>
    <p>Таблица 4. Выпускные сигналы</p>
    <p><strong>Листинг 12. Проверка решения.</strong></p>
    """,
    create_parent="div",
)
renderer = build_ru_editorial_docx.DocxRenderer(
    document,
    Path(sys.argv[1]) / "docs/publisher/ru-manuscript-editorial-2026-07-13.md",
)
renderer.render(root)
document.save(sys.argv[2])
'''
    subprocess.run(
        [str(runtime_python), "-c", script, str(ROOT), str(output)],
        cwd=ROOT,
        check=True,
    )

    with ZipFile(output) as archive:
        document = ET.fromstring(archive.read("word/document.xml"))

    bookmarks = document.findall(f".//{{{WORD_NS}}}bookmarkStart")
    names = [node.attrib[f"{{{WORD_NS}}}name"] for node in bookmarks]
    identifiers = [node.attrib[f"{{{WORD_NS}}}id"] for node in bookmarks]
    assert names == ["ch_1", "ch_16", "fig_3", "table_4", "listing_12"]
    assert len(identifiers) == len(set(identifiers))

    hyperlinks = document.findall(f".//{{{WORD_NS}}}hyperlink")
    anchors = [
        node.attrib[f"{{{WORD_NS}}}anchor"]
        for node in hyperlinks
        if f"{{{WORD_NS}}}anchor" in node.attrib
    ]
    assert anchors == ["ch_16", "fig_3", "table_4", "listing_12"]
    assert set(anchors) <= set(names)

    for paragraph in document.findall(f".//{{{WORD_NS}}}p"):
        value = "".join(
            node.text or "" for node in paragraph.findall(f".//{{{WORD_NS}}}t")
        )
        if re.match(r"^(?:Рисунок 3|Таблица 4|Листинг 12)\.", value):
            assert paragraph.find(f"{{{WORD_NS}}}hyperlink") is None


def test_editorial_renderer_formats_sources_as_breakable_hanging_paragraphs(
    tmp_path: Path,
) -> None:
    runtime_python = Path(
        os.environ.get(
            "CODEX_DOCUMENT_PYTHON",
            Path.home()
            / ".cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3",
        )
    )
    if not runtime_python.is_file():
        pytest.skip("bundled document runtime is unavailable")

    output = tmp_path / "source-paragraph.docx"
    script = r'''
import sys
from pathlib import Path
from docx import Document
from lxml import html

sys.path.insert(0, sys.argv[1])
from docs.publisher.tools import build_ru_editorial_docx

document = Document()
root = html.fragment_fromstring(
    """
    <h3>Источники главы</h3>
    <p><strong>S001.</strong> OWASP, AI Agent Security Cheat Sheet.</p>
    <p><strong>S002.</strong> NIST, AI RMF 1.0.</p>
    """,
    create_parent="div",
)
renderer = build_ru_editorial_docx.DocxRenderer(
    document,
    Path(sys.argv[1]) / "docs/publisher/ru-manuscript-editorial-2026-07-13.md",
)
renderer.render(root)
document.save(sys.argv[2])
'''
    subprocess.run(
        [str(runtime_python), "-c", script, str(ROOT), str(output)],
        cwd=ROOT,
        check=True,
    )

    with ZipFile(output) as archive:
        document = ET.fromstring(archive.read("word/document.xml"))

    source_paragraphs = []
    for paragraph in document.findall(f".//{{{WORD_NS}}}p"):
        value = "".join(
            node.text or "" for node in paragraph.findall(f".//{{{WORD_NS}}}t")
        )
        if re.match(r"^S\d{3}\.", value):
            source_paragraphs.append(paragraph)

    assert len(source_paragraphs) == 2
    for paragraph in source_paragraphs:
        indent = paragraph.find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}ind")
        assert indent is not None
        assert int(indent.attrib[f"{{{WORD_NS}}}left"]) > 0
        assert int(indent.attrib[f"{{{WORD_NS}}}hanging"]) > 0
        assert paragraph.find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}keepNext") is None


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
    assert len(document.findall(f".//{{{WORD_NS}}}hyperlink")) >= 104
    assert len(hyperlinks) >= 104


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


def test_editorial_tables_repeat_headers_and_keep_rows_together() -> None:
    for docx_path in (RAW_EDITORIAL_DOCX, EDITORIAL_TEMPLATE_DOCX):
        with ZipFile(docx_path) as archive:
            document = ET.fromstring(archive.read("word/document.xml"))

        tables = document.findall(f".//{{{WORD_NS}}}tbl")
        assert tables
        for table in tables:
            rows = table.findall(f"{{{WORD_NS}}}tr")
            assert rows[0].find(
                f"{{{WORD_NS}}}trPr/{{{WORD_NS}}}tblHeader"
            ) is not None
            assert all(
                row.find(f"{{{WORD_NS}}}trPr/{{{WORD_NS}}}cantSplit") is not None
                for row in rows
            )


def test_editorial_docx_has_print_navigation_language_and_metadata() -> None:
    for docx_path in (RAW_EDITORIAL_DOCX, EDITORIAL_TEMPLATE_DOCX):
        with ZipFile(docx_path) as archive:
            document = ET.fromstring(archive.read("word/document.xml"))
            settings = ET.fromstring(archive.read("word/settings.xml"))
            styles = ET.fromstring(archive.read("word/styles.xml"))
            core = ET.fromstring(archive.read("docProps/core.xml"))
            footer_names = [
                name
                for name in archive.namelist()
                if re.fullmatch(r"word/footer\d+\.xml", name)
            ]
            footer_xml = b"\n".join(archive.read(name) for name in footer_names)

        instructions = " ".join(
            node.text or ""
            for node in document.findall(f".//{{{WORD_NS}}}instrText")
        )
        document_text = "\n".join(
            node.text or "" for node in document.findall(f".//{{{WORD_NS}}}t")
        )
        style_languages = {
            node.attrib.get(f"{{{WORD_NS}}}val")
            for node in styles.findall(f".//{{{WORD_NS}}}lang")
        }

        assert 'TOC \\o "1-2"' in instructions
        assert settings.find(f"{{{WORD_NS}}}updateFields") is not None
        assert b"PAGE" in footer_xml
        assert "ru-RU" in style_languages
        assert core.findtext(f"{{{DC_NS}}}title") == "Архитектура безопасных ИИ-агентов"
        assert core.findtext(f"{{{DC_NS}}}language") == "ru-RU"
        assert core.findtext(f"{{{DC_NS}}}subject")
        assert core.findtext(f"{{{CP_NS}}}keywords")
        assert len(re.findall(r"^Таблица \d+\. .+$", document_text, re.MULTILINE)) == 10


def test_editorial_heading_styles_define_pdf_outline_levels() -> None:
    for docx_path in (RAW_EDITORIAL_DOCX, EDITORIAL_TEMPLATE_DOCX):
        with ZipFile(docx_path) as archive:
            styles = ET.fromstring(archive.read("word/styles.xml"))

        for level in range(1, 5):
            style = styles.find(
                f".//{{{WORD_NS}}}style"
                f"[@{{{WORD_NS}}}styleId='Heading{level}']"
            )
            assert style is not None
            outline_level = style.find(
                f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}outlineLvl"
            )
            assert outline_level is not None
            assert outline_level.attrib.get(f"{{{WORD_NS}}}val") == str(level - 1)


def test_editorial_toc_has_a_readable_static_result_before_word_updates_it() -> None:
    for docx_path in (RAW_EDITORIAL_DOCX, EDITORIAL_TEMPLATE_DOCX):
        with ZipFile(docx_path) as archive:
            document = ET.fromstring(archive.read("word/document.xml"))

        paragraphs = document.findall(f".//{{{WORD_NS}}}p")
        paragraph_texts = [
            "".join(node.text or "" for node in paragraph.findall(f".//{{{WORD_NS}}}t"))
            for paragraph in paragraphs
        ]
        text = "\n".join(paragraph_texts)
        first_body_heading = next(
            index
            for index, (paragraph, value) in enumerate(zip(paragraphs, paragraph_texts))
            if value == "Об авторе"
            and (
                style := paragraph.find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}pStyle")
            )
            is not None
            and style.attrib.get(f"{{{WORD_NS}}}val") == "Heading2"
        )
        toc_text = "\n".join(paragraph_texts[:first_body_heading])
        assert "Оглавление обновится при открытии документа." not in text
        assert "Часть I. От демо-агента к платформе" in toc_text
        assert "Глава 1. Почему агенту нужна платформа, а не магия" in toc_text
        assert "Глава 28. Проверочный список промышленного запуска" in toc_text
        assert "Приложение 5. Эталонный пакет и воспроизводимые упражнения" in toc_text


def test_template2000n_table_captions_use_caption_style_and_stay_with_tables() -> None:
    with ZipFile(EDITORIAL_TEMPLATE_DOCX) as archive:
        document = ET.fromstring(archive.read("word/document.xml"))

    captions = []
    for paragraph in document.findall(f".//{{{WORD_NS}}}p"):
        value = "".join(
            node.text or "" for node in paragraph.findall(f".//{{{WORD_NS}}}t")
        ).strip()
        if re.fullmatch(r"Таблица \d+\. .+", value):
            captions.append(paragraph)

    assert len(captions) == 10
    for paragraph in captions:
        properties = paragraph.find(f"{{{WORD_NS}}}pPr")
        assert properties is not None
        style = properties.find(f"{{{WORD_NS}}}pStyle")
        assert style is not None
        assert style.attrib[f"{{{WORD_NS}}}val"] == "Style17"
        assert properties.find(f"{{{WORD_NS}}}keepNext") is not None
        assert properties.find(f"{{{WORD_NS}}}keepLines") is not None


def test_editorial_table_columns_have_readable_minimum_width() -> None:
    for docx_path in (RAW_EDITORIAL_DOCX, EDITORIAL_TEMPLATE_DOCX):
        with ZipFile(docx_path) as archive:
            document = ET.fromstring(archive.read("word/document.xml"))

        tables = document.findall(f".//{{{WORD_NS}}}tbl")
        assert len(tables) == 10
        for table_index, table in enumerate(tables, start=1):
            widths = [
                int(column.attrib[f"{{{WORD_NS}}}w"])
                for column in table.findall(
                    f"{{{WORD_NS}}}tblGrid/{{{WORD_NS}}}gridCol"
                )
            ]
            total_width = sum(widths)
            assert min(widths) / total_width >= 0.14, (
                f"table {table_index} in {docx_path.name} has a column narrower "
                "than 14% of the table width"
            )


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
