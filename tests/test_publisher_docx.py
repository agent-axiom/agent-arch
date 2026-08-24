import ast
import hashlib
import json
import os
import posixpath
import re
import subprocess
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

import pytest

from docs.publisher.tools import normalize_docx_figure_caption_order, sync_ru_docx_visuals

ROOT = Path(__file__).resolve().parents[1]
EDITORIAL_BUILDER = ROOT / "docs/publisher/tools/build_ru_editorial_docx.py"
RAW_EDITORIAL_DOCX = ROOT / (
    "docs/publisher/artifacts/agent-arch-ru-google-doc-publication-readiness-2026-08-14.docx"
)
EDITORIAL_TEMPLATE_DOCX = ROOT / (
    "docs/publisher/artifacts/agent-arch-ru-template2000n-publication-readiness-2026-08-14.docx"
)
EDITORIAL_MANUSCRIPT = ROOT / "docs/publisher/ru-manuscript-editorial-2026-07-13.md"
CURRENT_RAW_DOCX = ROOT / (
    "docs/publisher/artifacts/agent-arch-ru-google-doc-book-standards-2026-08-23.docx"
)
CURRENT_TEMPLATE_DOCX = ROOT / (
    "docs/publisher/artifacts/agent-arch-ru-template2000n-book-standards-2026-08-23.docx"
)
RAW_A11Y = ROOT / "docs/publisher/ru-google-doc-book-standards-2026-08-23.a11y.json"
RAW_RENDER_QA = ROOT / "docs/publisher/ru-google-doc-book-standards-2026-08-23.render-qa.json"
TEMPLATE_A11Y = ROOT / "docs/publisher/ru-template2000n-book-standards-2026-08-23.a11y.json"
TEMPLATE_FONT_AUDIT = ROOT / (
    "docs/publisher/ru-template2000n-book-standards-2026-08-23.font-audit.json"
)
TEMPLATE_METRICS = ROOT / (
    "docs/publisher/ru-template2000n-book-standards-2026-08-23.metrics.json"
)
TEMPLATE_RENDER_QA = ROOT / (
    "docs/publisher/ru-template2000n-book-standards-2026-08-23.render-qa.json"
)
TEMPLATE_VISUAL_AUDIT = ROOT / (
    "docs/publisher/ru-template2000n-book-standards-2026-08-23.visual-audit.json"
)
VISUAL_LAYOUT_AUDIT = ROOT / "docs/publisher/ru-visual-layout-audit-2026-08-24.json"
INLINE_DIAGRAMS = ROOT / "docs/publisher/ru-inline-diagrams-2026-07-13.json"
NUMBERED_DIAGRAMS = ROOT / "docs/publisher/ru-numbered-diagrams-2026-07-15.json"
DIAGRAM_RENDERER = ROOT / "docs/publisher/tools/render_ru_inline_diagrams.mjs"
EXPECTED_TABLE_COUNT = 12
EXPECTED_IMAGE_COUNT = 57

PACKAGE_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
OFFICE_REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
DRAWING_NS = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
DRAWINGML_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
DC_NS = "http://purl.org/dc/elements/1.1/"
CP_NS = "http://schemas.openxmlformats.org/package/2006/metadata/core-properties"


def paragraph_uses_monospace_font(paragraph: ET.Element) -> bool:
    styled_characters = 0
    monospace_characters = 0
    monospace_run_seen = False
    for run in paragraph.findall(f"{{{WORD_NS}}}r"):
        run_text = "".join(
            node.text or "" for node in run.findall(f".//{{{WORD_NS}}}t")
        )
        fonts = run.find(f"{{{WORD_NS}}}rPr/{{{WORD_NS}}}rFonts")
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


def active_on_off_property(paragraph: ET.Element, name: str) -> bool:
    property_node = paragraph.find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}{name}")
    return property_node is not None and property_node.attrib.get(
        f"{{{WORD_NS}}}val", "1"
    ) not in {"0", "false", "off"}


def test_visual_audit_accepts_every_current_manuscript_image() -> None:
    assert (
        len(sync_ru_docx_visuals.parse_manuscript_visuals(EDITORIAL_MANUSCRIPT))
        == EXPECTED_IMAGE_COUNT
    )


def test_mermaid_visuals_reserve_space_below_cluster_titles() -> None:
    report = json.loads(VISUAL_LAYOUT_AUDIT.read_text(encoding="utf-8"))

    assert report["rendered"] == 56
    assert report["violations"] == []
    assert report["minimum_effective_font_pt"] >= 8.5
    assert report["cluster_title_violations"] == []
    assert report["cluster_title_edge_violations"] == []
    assert report["node_label_violations"] == []
    assert report["minimum_cluster_title_gap_px"] >= 12


def test_mermaid_renderer_rejects_hidden_edges_and_intrinsic_label_clipping() -> None:
    source = DIAGRAM_RENDERER.read_text(encoding="utf-8")

    assert "if (crossedLabel.opaque_background) continue;" not in source
    assert "scrollWidth" in source
    assert "clientWidth" in source


def test_generated_mermaid_svgs_are_valid_standalone_xml() -> None:
    for manifest_path in (INLINE_DIAGRAMS, NUMBERED_DIAGRAMS):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for diagram in manifest["diagrams"]:
            svg_path = ROOT / "docs/publisher/visuals" / diagram["filename"].replace(
                ".png", ".svg"
            )
            ET.parse(svg_path)


def test_mermaid_sources_connect_nodes_instead_of_cluster_frames() -> None:
    for manifest_path in (INLINE_DIAGRAMS, NUMBERED_DIAGRAMS):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for diagram in manifest["diagrams"]:
            source = diagram["mermaid"]
            cluster_ids = set(re.findall(r"^subgraph\s+([A-Za-z][\w-]*)", source, re.M))
            linked_cluster_ids = {
                endpoint
                for left, right in re.findall(
                    r"^\s*([A-Za-z][\w-]*)\s*(?:-->|-\.->|~~~)(?:\|[^\n]*?\|)?\s*"
                    r"([A-Za-z][\w-]*)",
                    source,
                    re.M,
                )
                for endpoint in (left, right)
                if endpoint in cluster_ids
            }
            assert linked_cluster_ids == set(), (
                f"{diagram['filename']} links cluster frames: "
                f"{sorted(linked_cluster_ids)}"
            )


def test_independently_reviewed_decisions_have_explicit_safe_branches() -> None:
    inline = {
        item["filename"]: item["mermaid"]
        for item in json.loads(INLINE_DIAGRAMS.read_text(encoding="utf-8"))["diagrams"]
    }

    assert 'V -->|"Да"| Y' in inline["ru-inline-diagram-05.png"]
    assert 'V -->|"Нет"| Q' in inline["ru-inline-diagram-05.png"]
    assert 'U -->|"Нет"| E' in inline["ru-inline-diagram-10.png"]
    assert 'U -->|"Да"| F' in inline["ru-inline-diagram-10.png"]
    assert 'F -->|"Эффекта нет"| E' in inline["ru-inline-diagram-10.png"]
    assert 'F -->|"Исход неизвестен"| H' in inline["ru-inline-diagram-10.png"]
    assert 'G -->|"Да"| H' in inline["ru-inline-diagram-29.png"]
    assert 'G -->|"Нет"| R' in inline["ru-inline-diagram-29.png"]


def test_visual_audit_uses_the_parsed_manuscript_count_for_docx_validation() -> None:
    validate = getattr(sync_ru_docx_visuals, "validate_docx_image_counts", None)

    assert validate is not None
    validate(EXPECTED_IMAGE_COUNT, EXPECTED_IMAGE_COUNT, EXPECTED_IMAGE_COUNT)
    with pytest.raises(ValueError, match="raw=56, template=57, expected=57"):
        validate(56, 57, 57)


def test_visual_resize_is_idempotent_at_the_print_height_limit() -> None:
    drawing = ET.fromstring(
        f'<w:drawing xmlns:w="{WORD_NS}" xmlns:wp="{DRAWING_NS}" '
        f'xmlns:a="{DRAWINGML_NS}">'
        '<wp:extent cx="5943600" cy="5943600"/>'
        '<a:xfrm><a:ext cx="5943600" cy="5943600"/></a:xfrm>'
        "</w:drawing>"
    )
    image = ROOT / "docs/publisher/visuals/ru-figure-13-autonomy-ladder.png"

    first = sync_ru_docx_visuals.resize_drawing(drawing, image)
    first_xml = ET.tostring(drawing)
    second = sync_ru_docx_visuals.resize_drawing(drawing, image)

    assert first == second
    assert first[1] <= sync_ru_docx_visuals.MAX_FIGURE_HEIGHT
    assert ET.tostring(drawing) == first_xml


def test_visual_resize_expands_small_legacy_placeholders_to_the_print_frame() -> None:
    drawing = ET.fromstring(
        f'<w:drawing xmlns:w="{WORD_NS}" xmlns:wp="{DRAWING_NS}" '
        f'xmlns:a="{DRAWINGML_NS}">'
        f'<wp:extent cx="{sync_ru_docx_visuals.EMU_PER_INCH}" '
        f'cy="{sync_ru_docx_visuals.EMU_PER_INCH}"/>'
        f'<a:xfrm><a:ext cx="{sync_ru_docx_visuals.EMU_PER_INCH}" '
        f'cy="{sync_ru_docx_visuals.EMU_PER_INCH}"/></a:xfrm>'
        "</w:drawing>"
    )
    image = ROOT / "docs/publisher/visuals/ru-figure-01-book-map.png"

    width, height = sync_ru_docx_visuals.resize_drawing(drawing, image)

    assert width > sync_ru_docx_visuals.EMU_PER_INCH
    assert width <= sync_ru_docx_visuals.MAX_FIGURE_WIDTH
    assert height <= sync_ru_docx_visuals.MAX_FIGURE_HEIGHT


def test_caption_normalizer_moves_only_captions_that_precede_images() -> None:
    paragraphs: list[str] = []
    for number in range(1, 26):
        caption = f"<w:p><w:r><w:t>Рисунок {number}. Схема {number}</w:t></w:r></w:p>"
        image = "<w:p><w:r><w:drawing/></w:r></w:p>"
        paragraphs.extend((caption, image) if number <= 20 else (image, caption))
    payload = (
        f'<w:document xmlns:w="{WORD_NS}"><w:body>'
        + "".join(paragraphs)
        + "</w:body></w:document>"
    ).encode()

    normalized, metrics = normalize_docx_figure_caption_order.normalize_document_xml(
        payload
    )
    document = ET.fromstring(normalized)
    children = list(document.find(f"{{{WORD_NS}}}body"))

    assert metrics == {
        "numbered_captions": 25,
        "captions_moved": 20,
        "captions_already_after_images": 5,
        "captions_after_images": 25,
    }
    for index, paragraph in enumerate(children):
        text = "".join(paragraph.itertext()).strip()
        if not text.startswith("Рисунок "):
            continue
        assert index > 0
        assert children[index - 1].find(f".//{{{WORD_NS}}}drawing") is not None


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
        value = "".join(node.text or "" for node in paragraph.findall(f".//{{{WORD_NS}}}t"))
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
        value = "".join(node.text or "" for node in paragraph.findall(f".//{{{WORD_NS}}}t"))
        if re.match(r"^S\d{3}\.", value):
            source_paragraphs.append(paragraph)

    assert len(source_paragraphs) == 2
    for paragraph in source_paragraphs:
        indent = paragraph.find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}ind")
        assert indent is not None
        assert int(indent.attrib[f"{{{WORD_NS}}}left"]) > 0
        assert int(indent.attrib[f"{{{WORD_NS}}}hanging"]) > 0
        assert paragraph.find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}keepNext") is None


def test_editorial_renderer_keeps_multiline_code_blocks_together(tmp_path: Path) -> None:
    runtime_python = Path(
        os.environ.get(
            "CODEX_DOCUMENT_PYTHON",
            Path.home()
            / ".cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3",
        )
    )
    if not runtime_python.is_file():
        pytest.skip("bundled document runtime is unavailable")

    output = tmp_path / "code-block.docx"
    script = r"""
import sys
from pathlib import Path
from docx import Document
from lxml import html

sys.path.insert(0, sys.argv[1])
from docs.publisher.tools import build_ru_editorial_docx

document = Document()
root = html.fragment_fromstring(
    "<h2>Глава 1. Тест</h2>"
    "<p><strong>Команда.</strong> Запустите сценарий:</p>"
    "<pre><code>first line\nsecond line\nlast line</code></pre>",
    create_parent="div",
)
renderer = build_ru_editorial_docx.DocxRenderer(
    document,
    Path(sys.argv[1]) / "docs/publisher/ru-manuscript-editorial-2026-07-13.md",
)
renderer.render(root)
document.save(sys.argv[2])
"""
    subprocess.run(
        [str(runtime_python), "-c", script, str(ROOT), str(output)],
        cwd=ROOT,
        check=True,
    )

    with ZipFile(output) as archive:
        document = ET.fromstring(archive.read("word/document.xml"))

    intro_paragraph = None
    code_paragraphs = []
    for paragraph in document.findall(f".//{{{WORD_NS}}}p"):
        value = "".join(node.text or "" for node in paragraph.findall(f".//{{{WORD_NS}}}t"))
        if value == "Команда. Запустите сценарий:":
            intro_paragraph = paragraph
        elif value in {"first line", "second line", "last line"}:
            code_paragraphs.append(paragraph)

    assert intro_paragraph is not None
    assert intro_paragraph.find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}keepNext") is not None
    assert len(code_paragraphs) == 3
    for paragraph in code_paragraphs:
        assert paragraph.find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}keepLines") is not None
    for paragraph in code_paragraphs[:-1]:
        assert paragraph.find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}keepNext") is not None
    assert code_paragraphs[-1].find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}keepNext") is None


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


def test_current_book_standards_artifacts_pass_machine_gates() -> None:
    raw_a11y = json.loads(RAW_A11Y.read_text(encoding="utf-8"))
    raw_render = json.loads(RAW_RENDER_QA.read_text(encoding="utf-8"))
    template_a11y = json.loads(TEMPLATE_A11Y.read_text(encoding="utf-8"))
    font_audit = json.loads(TEMPLATE_FONT_AUDIT.read_text(encoding="utf-8"))
    metrics = json.loads(TEMPLATE_METRICS.read_text(encoding="utf-8"))
    template_render = json.loads(TEMPLATE_RENDER_QA.read_text(encoding="utf-8"))
    visual_audit = json.loads(TEMPLATE_VISUAL_AUDIT.read_text(encoding="utf-8"))

    assert raw_a11y["counts"] == {"high": 0, "medium": 0, "low": 2}
    assert template_a11y["counts"] == {"high": 0, "medium": 0, "low": 2}
    assert raw_render["pages"] == 539
    assert raw_render["blank_like_pages"] == []
    assert raw_render["page_sizes"] == [{"count": 539, "height": 2002, "width": 1547}]
    assert raw_render["edge_touch_pages"] == []
    assert template_render["pages"] == 380
    assert template_render["blank_like_pages"] == []
    assert template_render["page_sizes"] == [
        {"count": 380, "height": 2002, "width": 1547}
    ]
    assert template_render["edge_touch_pages"] == []
    for report in (raw_render, template_render):
        assert min(report["minimum_ink_margins_pixels"].values()) >= 150
    assert font_audit["passed"] is True
    assert font_audit["embedded_font_registrations"] == [
        "Noto Sans Symbols Regular",
        "Noto Sans Symbols Bold",
        "Roboto Mono Regular",
        "Roboto Mono Bold",
        "Roboto Mono Italic",
        "Roboto Mono BoldItalic",
    ]
    assert metrics["document_text_equality"] is True
    assert metrics["media_byte_equality"] is True
    assert metrics["media_files"] == EXPECTED_IMAGE_COUNT
    assert metrics["approximate_words"] >= 95_000
    assert visual_audit["docx"]["raw_media_matches_source"] is True
    assert visual_audit["docx"]["template_media_order_matches_raw"] is True
    assert visual_audit["docx"]["numbered_figure_caption_pairs"] == 25
    assert visual_audit["docx"]["alpha_images"] == 0
    assert visual_audit["pdf"]["images"] == EXPECTED_IMAGE_COUNT

    for docx_path in (CURRENT_RAW_DOCX, CURRENT_TEMPLATE_DOCX):
        with ZipFile(docx_path) as archive:
            current_document = ET.fromstring(archive.read("word/document.xml"))
        tables = current_document.findall(f".//{{{WORD_NS}}}tbl")
        assert len(tables) == EXPECTED_TABLE_COUNT
        for table in tables:
            rows = table.findall(f"{{{WORD_NS}}}tr")
            assert rows
            header = rows[0].find(
                f"{{{WORD_NS}}}trPr/{{{WORD_NS}}}tblHeader"
            )
            assert header is not None
            assert header.attrib.get(f"{{{WORD_NS}}}val", "1") not in {
                "0",
                "false",
                "off",
            }
            for row in rows:
                keep_together = row.find(
                    f"{{{WORD_NS}}}trPr/{{{WORD_NS}}}cantSplit"
                )
                assert keep_together is not None
                assert keep_together.attrib.get(f"{{{WORD_NS}}}val", "1") not in {
                    "0",
                    "false",
                    "off",
                }

    for docx_path in (CURRENT_RAW_DOCX, CURRENT_TEMPLATE_DOCX):
        with ZipFile(docx_path) as archive:
            document_xml = archive.read("word/document.xml")
            font_table_xml = archive.read("word/fontTable.xml")

        document = ET.fromstring(document_xml)
        text = "".join(document.itertext())
        assert "Политика последовательности проверяет всю траекторию" in text
        assert text.count("approval -> resume -> execute -> audit") == 3
        assert "approval → resume → execute → audit" not in text
        assert b"Nova Mono" not in font_table_xml

        parent_by_child = {
            child: parent for parent in document.iter() for child in list(parent)
        }
        captions: list[tuple[int, ET.Element]] = []
        for paragraph in document.findall(f".//{{{WORD_NS}}}p"):
            paragraph_value = "".join(
                node.text or "" for node in paragraph.findall(f".//{{{WORD_NS}}}t")
            ).strip()
            match = re.fullmatch(r"Рисунок (\d+)\. .+", paragraph_value)
            if match:
                captions.append((int(match.group(1)), paragraph))

        assert [number for number, _ in captions] == list(range(1, 26))
        for number, caption in captions:
            parent = parent_by_child[caption]
            siblings = list(parent)
            previous = next(
                (
                    candidate
                    for candidate in reversed(siblings[: siblings.index(caption)])
                    if candidate.tag == f"{{{WORD_NS}}}p"
                    and (
                        candidate.find(f".//{{{WORD_NS}}}drawing") is not None
                        or "".join(
                            node.text or ""
                            for node in candidate.findall(f".//{{{WORD_NS}}}t")
                        ).strip()
                    )
                ),
                None,
            )
            assert previous is not None, f"Figure {number} has no preceding paragraph"
            assert previous.find(f".//{{{WORD_NS}}}drawing") is not None
            image_keep_next = previous.find(
                f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}keepNext"
            )
            caption_keep_lines = caption.find(
                f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}keepLines"
            )
            assert image_keep_next is not None
            assert image_keep_next.attrib.get(f"{{{WORD_NS}}}val", "1") not in {
                "0",
                "false",
                "off",
            }
            assert caption_keep_lines is not None
            assert caption_keep_lines.attrib.get(f"{{{WORD_NS}}}val", "1") not in {
                "0",
                "false",
                "off",
            }


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
    assert len(image_properties) == EXPECTED_IMAGE_COUNT
    assert all(node.attrib.get("descr", "").strip() for node in image_properties)

    hyperlinks = [
        node
        for node in relationships.findall(f"{{{PACKAGE_REL_NS}}}Relationship")
        if node.attrib.get("Type", "").endswith("/hyperlink")
    ]
    assert len(document.findall(f".//{{{WORD_NS}}}hyperlink")) >= 104
    assert len(hyperlinks) >= 104


def test_template2000n_prioritizes_list_style_over_inline_code_font() -> None:
    builder = ROOT / "docs/publisher/tools/build_template2000n_derivative.py"
    source = builder.read_text(encoding="utf-8")

    list_branch = source.index('elif paragraph.find("w:pPr/w:numPr", NS) is not None:')
    program_branch = source.index("elif paragraph_is_monospace(paragraph):")

    assert list_branch < program_branch


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
            header = rows[0].find(f"{{{WORD_NS}}}trPr/{{{WORD_NS}}}tblHeader")
            assert header is not None
            assert header.attrib.get(f"{{{WORD_NS}}}val", "1") not in {
                "0",
                "false",
                "off",
            }
            for row in rows:
                keep_together = row.find(f"{{{WORD_NS}}}trPr/{{{WORD_NS}}}cantSplit")
                assert keep_together is not None
                assert keep_together.attrib.get(f"{{{WORD_NS}}}val", "1") not in {
                    "0",
                    "false",
                    "off",
                }


def test_editorial_docx_has_no_empty_numbered_paragraphs() -> None:
    for docx_path in (CURRENT_RAW_DOCX, CURRENT_TEMPLATE_DOCX):
        with ZipFile(docx_path) as archive:
            document = ET.fromstring(archive.read("word/document.xml"))

        empty_numbered = []
        for index, paragraph in enumerate(document.findall(f".//{{{WORD_NS}}}p")):
            text = "".join(
                node.text or "" for node in paragraph.findall(f".//{{{WORD_NS}}}t")
            ).strip()
            if (
                not text
                and paragraph.find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}numPr") is not None
            ):
                empty_numbered.append(index)

        assert empty_numbered == []


def test_editorial_page_break_headings_have_no_leading_empty_paragraph() -> None:
    for docx_path in (CURRENT_RAW_DOCX, CURRENT_TEMPLATE_DOCX):
        with ZipFile(docx_path) as archive:
            document = ET.fromstring(archive.read("word/document.xml"))

        paragraphs = document.findall(f".//{{{WORD_NS}}}body/{{{WORD_NS}}}p")
        for index, paragraph in enumerate(paragraphs):
            if not active_on_off_property(paragraph, "pageBreakBefore"):
                continue
            assert index > 0
            previous_text = "".join(
                node.text or ""
                for node in paragraphs[index - 1].findall(f".//{{{WORD_NS}}}t")
            ).strip()
            assert previous_text


def test_editorial_code_blocks_avoid_orphaned_opening_lines() -> None:
    for docx_path in (CURRENT_RAW_DOCX, CURRENT_TEMPLATE_DOCX):
        with ZipFile(docx_path) as archive:
            document = ET.fromstring(archive.read("word/document.xml"))

        paragraphs = document.findall(f".//{{{WORD_NS}}}body/{{{WORD_NS}}}p")
        code_blocks: list[list[ET.Element]] = []
        current_block: list[ET.Element] = []
        for paragraph in paragraphs:
            if paragraph_uses_monospace_font(paragraph):
                current_block.append(paragraph)
                continue
            if current_block:
                code_blocks.append(current_block)
                current_block = []
        if current_block:
            code_blocks.append(current_block)

        assert len(code_blocks) >= 30
        for block in code_blocks:
            assert all(active_on_off_property(paragraph, "keepLines") for paragraph in block)
            for index, paragraph in enumerate(block):
                expected = (
                    index < len(block) - 1
                    and (index + 1)
                    % sync_ru_docx_visuals.MAX_CODE_PARAGRAPHS_PER_KEEP_GROUP
                    != 0
                )
                assert active_on_off_property(paragraph, "keepNext") is expected


def test_inline_visual_titles_stay_with_their_images() -> None:
    for docx_path in (CURRENT_RAW_DOCX, CURRENT_TEMPLATE_DOCX):
        with ZipFile(docx_path) as archive:
            document = ET.fromstring(archive.read("word/document.xml"))

        paragraphs = document.findall(f".//{{{WORD_NS}}}p")
        matched_titles = 0
        for index, paragraph in enumerate(paragraphs):
            image_properties = paragraph.find(f".//{{{DRAWING_NS}}}docPr")
            if image_properties is None:
                continue
            description = image_properties.attrib.get("descr", "").strip()
            previous_paragraph = next(
                (
                    candidate
                    for candidate in reversed(paragraphs[:index])
                    if "".join(
                        node.text or ""
                        for node in candidate.findall(f".//{{{WORD_NS}}}t")
                    ).strip()
                ),
                None,
            )
            if previous_paragraph is None:
                continue
            previous_text = "".join(
                node.text or ""
                for node in previous_paragraph.findall(f".//{{{WORD_NS}}}t")
            ).strip()
            if previous_text != description:
                continue

            matched_titles += 1
            keep_next = previous_paragraph.find(
                f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}keepNext"
            )
            assert keep_next is not None
            assert keep_next.attrib.get(f"{{{WORD_NS}}}val", "1") not in {
                "0",
                "false",
                "off",
            }

        assert matched_titles >= 10


def test_editorial_docx_has_print_navigation_language_and_metadata() -> None:
    for docx_path in (RAW_EDITORIAL_DOCX, EDITORIAL_TEMPLATE_DOCX):
        with ZipFile(docx_path) as archive:
            document = ET.fromstring(archive.read("word/document.xml"))
            settings = ET.fromstring(archive.read("word/settings.xml"))
            styles = ET.fromstring(archive.read("word/styles.xml"))
            core = ET.fromstring(archive.read("docProps/core.xml"))
            footer_names = [
                name for name in archive.namelist() if re.fullmatch(r"word/footer\d+\.xml", name)
            ]
            footer_xml = b"\n".join(archive.read(name) for name in footer_names)

        instructions = " ".join(
            node.text or "" for node in document.findall(f".//{{{WORD_NS}}}instrText")
        )
        document_text = "\n".join(
            node.text or "" for node in document.findall(f".//{{{WORD_NS}}}t")
        )
        style_languages = {
            node.attrib.get(f"{{{WORD_NS}}}val") for node in styles.findall(f".//{{{WORD_NS}}}lang")
        }

        assert 'TOC \\o "1-2"' in instructions
        assert settings.find(f"{{{WORD_NS}}}updateFields") is not None
        assert b"PAGE" in footer_xml
        assert "ru-RU" in style_languages
        assert core.findtext(f"{{{DC_NS}}}title") == "Архитектура безопасных ИИ-агентов"
        assert core.findtext(f"{{{DC_NS}}}language") == "ru-RU"
        assert core.findtext(f"{{{DC_NS}}}subject")
        assert core.findtext(f"{{{CP_NS}}}keywords")
        assert (
            len(re.findall(r"^Таблица \d+\. .+$", document_text, re.MULTILINE))
            == EXPECTED_TABLE_COUNT
        )


def test_editorial_heading_styles_define_pdf_outline_levels() -> None:
    for docx_path in (RAW_EDITORIAL_DOCX, EDITORIAL_TEMPLATE_DOCX):
        with ZipFile(docx_path) as archive:
            styles = ET.fromstring(archive.read("word/styles.xml"))

        for level in range(1, 5):
            style = styles.find(f".//{{{WORD_NS}}}style[@{{{WORD_NS}}}styleId='Heading{level}']")
            assert style is not None
            outline_level = style.find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}outlineLvl")
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
            and (style := paragraph.find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}pStyle")) is not None
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
        value = "".join(node.text or "" for node in paragraph.findall(f".//{{{WORD_NS}}}t")).strip()
        if re.fullmatch(r"Таблица \d+\. .+", value):
            captions.append(paragraph)

    assert len(captions) == EXPECTED_TABLE_COUNT
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
        assert len(tables) == EXPECTED_TABLE_COUNT
        for table_index, table in enumerate(tables, start=1):
            widths = [
                int(column.attrib[f"{{{WORD_NS}}}w"])
                for column in table.findall(f"{{{WORD_NS}}}tblGrid/{{{WORD_NS}}}gridCol")
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
                (style := paragraph_node.find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}pStyle")) is not None
                and style.attrib.get(f"{{{WORD_NS}}}val") == "Heading2"
                and (match := re.fullmatch(r"Глава (\d+)\. .+", paragraph.strip()))
            )
        ]
        text = "\n".join(paragraphs)

        assert chapter_numbers == list(range(1, 29))
        assert "create_support_ticket" not in text
        assert "Покрытие обязательным подтверждением и трассировкой" in text
        assert "except GatewayTimeout" in text
        figure_leads = re.findall(r"^На рисунке \d+ .+$", text, re.MULTILINE)
        assert len(figure_leads) == 25
        assert all("представлена схема" not in lead for lead in figure_leads)
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
            page_break = paragraph.find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}pageBreakBefore")
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
    relative_paths = re.findall(r"^!\[[^\]]+\]\((visuals/[^)]+)\)$", manuscript, re.MULTILINE)
    expected_hashes = [
        hashlib.sha256((EDITORIAL_MANUSCRIPT.parent / path).read_bytes()).hexdigest()
        for path in relative_paths
    ]
    raw_targets, raw_hashes = ordered_embedded_images(CURRENT_RAW_DOCX)
    template_targets, _ = ordered_embedded_images(CURRENT_TEMPLATE_DOCX)

    assert len(relative_paths) == EXPECTED_IMAGE_COUNT
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
                    node.text or "" for node in candidate.findall(f".//{{{WORD_NS}}}t")
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
