import ast
import base64
import hashlib
import json
import os
import posixpath
import re
import struct
import subprocess
import sys
import zlib
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
        "agent-arch-ru-google-doc-unified-visuals-2026-08-02.docx"
    )
)
EDITORIAL_TEMPLATE_DOCX = (
    ROOT
    / (
        "docs/publisher/artifacts/"
        "agent-arch-ru-template2000n-unified-visuals-2026-08-02.docx"
    )
)
EDITORIAL_MANUSCRIPT = ROOT / "docs/publisher/ru-manuscript-editorial-2026-07-13.md"
EXPECTED_TABLE_COUNT = 11

PACKAGE_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
CONTENT_TYPES_NS = "http://schemas.openxmlformats.org/package/2006/content-types"
OFFICE_REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
DRAWING_NS = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
DRAWINGML_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
DC_NS = "http://purl.org/dc/elements/1.1/"
CP_NS = "http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
PRESERVED_DOCX_MEMBER = "customXml/preserved.xml"
PRESERVED_DOCX_PAYLOAD = b"<preserved>fixture-member</preserved>"
FIXTURE_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
)


def document_runtime_python() -> Path:
    override = os.environ.get("CODEX_DOCUMENT_PYTHON")
    if override is None:
        runtime_python = Path(sys.executable)
        source = "sys.executable"
    else:
        runtime_python = Path(override)
        source = "CODEX_DOCUMENT_PYTHON"
    if not runtime_python.is_file() or not os.access(runtime_python, os.X_OK):
        raise RuntimeError(
            f"{source} must point to an existing executable: {runtime_python}"
        )
    return runtime_python


def render_editorial_fixture(
    tmp_path: Path,
    source: str,
) -> tuple[ET.Element, dict[str, int]]:
    runtime_python = document_runtime_python()

    source_path = tmp_path / "fixture.html"
    manuscript_path = tmp_path / "manuscript.md"
    image_path = tmp_path / "visuals/fixture.png"
    output = tmp_path / "fixture.docx"
    metrics_path = tmp_path / "metrics.json"
    source_path.write_text(source, encoding="utf-8")
    manuscript_path.write_text("# Fixture manuscript\n", encoding="utf-8")
    image_path.parent.mkdir()
    image_path.write_bytes(FIXTURE_PNG)
    script = r'''
import json
import sys
from pathlib import Path

from docx import Document
from lxml import html

sys.path.insert(0, sys.argv[1])
from docs.publisher.tools import build_ru_editorial_docx

root_path = Path(sys.argv[2])
document = Document()
root = html.fragment_fromstring(
    root_path.read_text(encoding="utf-8"),
    create_parent="div",
)
renderer = build_ru_editorial_docx.DocxRenderer(
    document,
    Path(sys.argv[3]),
)
renderer.render(root)
document.save(sys.argv[4])
Path(sys.argv[5]).write_text(
    json.dumps(renderer.metrics, ensure_ascii=False),
    encoding="utf-8",
)
'''
    subprocess.run(
        [
            str(runtime_python),
            "-c",
            script,
            str(ROOT),
            str(source_path),
            str(manuscript_path),
            str(output),
            str(metrics_path),
        ],
        cwd=ROOT,
        check=True,
    )

    with ZipFile(output) as archive:
        document_xml = ET.fromstring(archive.read("word/document.xml"))
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    return document_xml, metrics


def paragraph_text(paragraph: ET.Element) -> str:
    return "".join(
        node.text or "" for node in paragraph.findall(f".//{{{WORD_NS}}}t")
    )


def map_template_semantic_styles_in_runtime(
    document_xml: bytes,
) -> tuple[ET.Element, dict[str, int]]:
    script = r'''
import base64
import json
import sys

sys.path.insert(0, sys.argv[1])
from docs.publisher.tools.build_template2000n_derivative import map_semantic_styles

document_xml, mappings = map_semantic_styles(sys.stdin.buffer.read())
sys.stdout.write(
    json.dumps(
        {
            "document_xml": base64.b64encode(document_xml).decode("ascii"),
            "mappings": mappings,
        },
        ensure_ascii=False,
    )
)
'''
    completed = subprocess.run(
        [str(document_runtime_python()), "-c", script, str(ROOT)],
        input=document_xml,
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    payload = json.loads(completed.stdout)
    return ET.fromstring(base64.b64decode(payload["document_xml"])), payload["mappings"]


def template_semantic_style_fixture_xml() -> bytes:
    return f'''<?xml version="1.0" encoding="utf-8"?>
<w:document xmlns:w="{WORD_NS}" xmlns:wp="{DRAWING_NS}">
  <w:body>
    <w:p><w:r><w:t>Вводный текст</w:t></w:r></w:p>
    <w:tbl>
      <w:tr><w:tc><w:p><w:r><w:t>Заголовок таблицы</w:t></w:r></w:p></w:tc></w:tr>
      <w:tr><w:tc><w:p><w:r><w:t>Ячейка таблицы</w:t></w:r></w:p></w:tc></w:tr>
    </w:tbl>
    <w:p><w:r><w:t>Практическая проверка.</w:t></w:r></w:p>
    <w:p/>
    <w:p><w:r><w:t>Тело после пустого абзаца</w:t></w:r></w:p>
    <w:p><w:r><w:t>Таблица 4. Проверочная таблица</w:t></w:r></w:p>
    <w:p>
      <w:pPr><w:numPr/></w:pPr>
      <w:r><w:rPr><w:rFonts w:ascii="Roboto Mono"/></w:rPr><w:t>Элемент списка</w:t></w:r>
    </w:p>
    <w:p>
      <w:r><w:rPr><w:rFonts w:ascii="Courier New"/></w:rPr><w:t>print('ok')</w:t></w:r>
    </w:p>
    <w:p>
      <w:pPr><w:pStyle w:val="Heading1"/></w:pPr>
      <w:r><w:t>Сохраненный заголовок</w:t></w:r>
    </w:p>
    <w:p><w:r><w:t>Частые ошибки.</w:t></w:r></w:p>
    <w:p>
      <w:pPr><w:pStyle w:val="Heading2"/></w:pPr>
      <w:r><w:t>Заголовок сбрасывает выноску</w:t></w:r>
    </w:p>
    <w:p><w:pPr><w:pStyle w:val="Title"/></w:pPr><w:r><w:t>Title</w:t></w:r></w:p>
    <w:p><w:pPr><w:pStyle w:val="Heading3"/></w:pPr><w:r><w:t>H3</w:t></w:r></w:p>
    <w:p><w:pPr><w:pStyle w:val="Heading4"/></w:pPr><w:r><w:t>H4</w:t></w:r></w:p>
    <w:p><w:pPr><w:pStyle w:val="Heading5"/></w:pPr><w:r><w:t>H5</w:t></w:r></w:p>
    <w:p><w:r><w:t>Текст после заголовка</w:t></w:r></w:p>
    <w:p><w:r><w:t>Граница доказательств.</w:t></w:r></w:p>
    <w:p><w:r><w:drawing><wp:inline>
      <wp:docPr id="1" name="Reset image" descr=""/>
    </wp:inline></w:drawing></w:r></w:p>
    <w:p><w:r><w:t>Рисунок 8. Подпись после изображения</w:t></w:r></w:p>
    <w:p><w:r><w:t>Текст после изображения</w:t></w:r></w:p>
    <w:p><w:r><w:t>Опорный текст</w:t></w:r></w:p>
    <w:p>
      <w:r><w:t>Текст внутри изображения</w:t><w:drawing><wp:inline>
        <wp:docPr id="2" name="Existing alt" descr="Готовое описание"/>
      </wp:inline></w:drawing></w:r>
    </w:p>
    <w:p><w:r><w:drawing><wp:inline>
      <wp:docPr id="3" name="Fallback image" descr=""/>
    </wp:inline></w:drawing></w:r></w:p>
  </w:body>
</w:document>
'''.encode()


def test_document_runtime_python_defaults_to_current_interpreter(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("CODEX_DOCUMENT_PYTHON", raising=False)

    assert document_runtime_python() == Path(sys.executable)


def test_document_runtime_python_validates_explicit_override(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("CODEX_DOCUMENT_PYTHON", sys.executable)
    assert document_runtime_python() == Path(sys.executable)

    missing_python = tmp_path / "missing-python"
    monkeypatch.setenv("CODEX_DOCUMENT_PYTHON", str(missing_python))
    with pytest.raises(
        RuntimeError,
        match=re.escape(
            "CODEX_DOCUMENT_PYTHON must point to an existing executable: "
            f"{missing_python}"
        ),
    ):
        document_runtime_python()


def _png_payload(*, seed: int, alpha: bool = False) -> bytes:
    color_type = 6 if alpha else 2
    channels = 4 if alpha else 3
    pixel = bytes((seed + offset) % 256 for offset in range(channels))
    scanlines = b"\x00" + pixel * 2

    def chunk(kind: bytes, payload: bytes) -> bytes:
        checksum = zlib.crc32(kind + payload) & 0xFFFFFFFF
        return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", checksum)

    header = struct.pack(">IIBBBBB", 2, 1, 8, color_type, 0, 0, 0)
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", header)
        + chunk(b"IDAT", zlib.compress(scanlines))
        + chunk(b"IEND", b"")
    )


def _text_paragraph(parent: ET.Element, text: str) -> ET.Element:
    paragraph = ET.SubElement(parent, f"{{{WORD_NS}}}p")
    run = ET.SubElement(paragraph, f"{{{WORD_NS}}}r")
    node = ET.SubElement(run, f"{{{WORD_NS}}}t")
    node.text = text
    return paragraph


def _drawing_paragraph(
    parent: ET.Element,
    *,
    index: int,
    relationship_id: str,
    description: str,
    extent: tuple[int, int],
) -> tuple[ET.Element, ET.Element, ET.Element]:
    paragraph = ET.SubElement(parent, f"{{{WORD_NS}}}p")
    drawing = ET.SubElement(paragraph, f"{{{WORD_NS}}}drawing")
    inline = ET.SubElement(drawing, f"{{{DRAWING_NS}}}inline")
    width, height = extent
    ET.SubElement(
        inline,
        f"{{{DRAWING_NS}}}extent",
        {"cx": str(width), "cy": str(height)},
    )
    ET.SubElement(
        inline,
        f"{{{DRAWING_NS}}}docPr",
        {"id": str(index), "name": f"Picture {index}", "descr": description},
    )
    graphic = ET.SubElement(inline, f"{{{DRAWINGML_NS}}}graphic")
    blip = ET.SubElement(graphic, f"{{{DRAWINGML_NS}}}blip")
    blip.set(f"{{{OFFICE_REL_NS}}}embed", relationship_id)
    transform = ET.SubElement(graphic, f"{{{DRAWINGML_NS}}}xfrm")
    ET.SubElement(
        transform,
        f"{{{DRAWINGML_NS}}}ext",
        {"cx": str(width), "cy": str(height)},
    )
    return paragraph, drawing, blip


def _write_docx_fixture(
    path: Path,
    payloads: list[bytes],
    *,
    drawing_relationship_ids: list[str] | None = None,
    relationship_targets: list[str] | None = None,
    descriptions: list[str] | None = None,
    extents: list[tuple[int, int]] | None = None,
    numbered_count: int = 0,
    captions_before_drawings: bool = False,
    missing_caption: int | None = None,
) -> None:
    count = len(payloads)
    relationship_ids = [f"rId{index}" for index in range(1, count + 1)]
    drawing_relationship_ids = drawing_relationship_ids or relationship_ids
    relationship_targets = relationship_targets or [
        f"media/image-{index}.png" for index in range(1, count + 1)
    ]
    descriptions = descriptions or [f"Alternative text {index}" for index in range(1, count + 1)]
    extents = extents or [
        (2 * sync_ru_docx_visuals.EMU_PER_INCH, sync_ru_docx_visuals.EMU_PER_INCH)
        for _ in range(count)
    ]

    document = ET.Element(f"{{{WORD_NS}}}document")
    body = ET.SubElement(document, f"{{{WORD_NS}}}body")
    for index, (relationship_id, description, extent) in enumerate(
        zip(drawing_relationship_ids, descriptions, extents, strict=True),
        start=1,
    ):
        if captions_before_drawings and index <= numbered_count:
            _text_paragraph(
                body,
                f"На рисунке {index} представлена схема «Старое название {index}».",
            )
            if index != missing_caption:
                _text_paragraph(body, f"Рисунок {index}. Старое название {index}")
        _drawing_paragraph(
            body,
            index=index,
            relationship_id=relationship_id,
            description=description,
            extent=extent,
        )
        if not captions_before_drawings and index <= numbered_count and index != missing_caption:
            _text_paragraph(body, f"Рисунок {index}. Название {index}")
    ET.SubElement(body, f"{{{WORD_NS}}}sectPr")

    relationships = ET.Element(f"{{{PACKAGE_REL_NS}}}Relationships")
    media: dict[str, bytes] = {}
    for relationship_id, target, payload in zip(
        relationship_ids,
        relationship_targets,
        payloads,
        strict=True,
    ):
        ET.SubElement(
            relationships,
            f"{{{PACKAGE_REL_NS}}}Relationship",
            {
                "Id": relationship_id,
                "Type": f"{OFFICE_REL_NS}/image",
                "Target": target,
            },
        )
        media.setdefault(f"word/{target}", payload)
    ET.SubElement(
        relationships,
        f"{{{PACKAGE_REL_NS}}}Relationship",
        {
            "Id": "rIdPreserved",
            "Type": f"{OFFICE_REL_NS}/customXml",
            "Target": "../customXml/preserved.xml",
        },
    )

    package_relationships = ET.Element(f"{{{PACKAGE_REL_NS}}}Relationships")
    ET.SubElement(
        package_relationships,
        f"{{{PACKAGE_REL_NS}}}Relationship",
        {
            "Id": "rId1",
            "Type": f"{OFFICE_REL_NS}/officeDocument",
            "Target": "word/document.xml",
        },
    )
    content_types = ET.Element(f"{{{CONTENT_TYPES_NS}}}Types")
    for extension, content_type in (
        ("rels", "application/vnd.openxmlformats-package.relationships+xml"),
        ("xml", "application/xml"),
        ("png", "image/png"),
    ):
        ET.SubElement(
            content_types,
            f"{{{CONTENT_TYPES_NS}}}Default",
            {"Extension": extension, "ContentType": content_type},
        )
    ET.SubElement(
        content_types,
        f"{{{CONTENT_TYPES_NS}}}Override",
        {
            "PartName": "/word/document.xml",
            "ContentType": (
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document.main+xml"
            ),
        },
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(path, "w") as archive:
        archive.writestr(
            "[Content_Types].xml",
            ET.tostring(content_types, encoding="utf-8", xml_declaration=True),
        )
        archive.writestr(
            "_rels/.rels",
            ET.tostring(package_relationships, encoding="utf-8", xml_declaration=True),
        )
        archive.writestr(
            "word/document.xml",
            ET.tostring(document, encoding="utf-8", xml_declaration=True),
        )
        archive.writestr(
            "word/_rels/document.xml.rels",
            ET.tostring(relationships, encoding="utf-8", xml_declaration=True),
        )
        archive.writestr(PRESERVED_DOCX_MEMBER, PRESERVED_DOCX_PAYLOAD)
        for target, payload in media.items():
            archive.writestr(target, payload)


def _write_manuscript_fixture(root: Path, payloads: list[bytes]) -> Path:
    visuals_directory = root / "visuals"
    visuals_directory.mkdir(parents=True)
    lines: list[str] = []
    for index, payload in enumerate(payloads, start=1):
        relative_path = f"visuals/image-{index}.png"
        (root / relative_path).write_bytes(payload)
        lines.extend((f"![Alt {index}]({relative_path})", ""))
        if index <= 25:
            lines.extend((f"Рисунок {index}. Новое название {index}", ""))
    manuscript = root / "manuscript.md"
    manuscript.write_text("\n".join(lines), encoding="utf-8")
    return manuscript


def _audit_visuals(root: Path, payloads: list[bytes]) -> list[dict[str, object]]:
    root.mkdir(parents=True)
    visuals: list[dict[str, object]] = []
    for index, payload in enumerate(payloads, start=1):
        path = root / f"image-{index}.png"
        path.write_bytes(payload)
        visuals.append(
            {
                "path": str(path),
                "figure_number": index,
                "figure_title": f"Название {index}",
                "alt": f"Alternative text {index}",
            }
        )
    return visuals


def _audit_docx_in_runtime(
    raw_docx: Path,
    template_docx: Path,
    visuals: list[dict[str, object]],
) -> dict[str, object]:
    script = r"""
import json
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1])
from docs.publisher.tools import audit_ru_visuals

visuals = json.loads(sys.argv[4])
for visual in visuals:
    visual["path"] = Path(visual["path"])
try:
    metrics = audit_ru_visuals.audit_docx(Path(sys.argv[2]), Path(sys.argv[3]), visuals)
except ValueError as error:
    result = {"error": str(error)}
else:
    result = {"metrics": metrics}
print(json.dumps(result, ensure_ascii=False, sort_keys=True))
"""
    completed = subprocess.run(
        [
            str(document_runtime_python()),
            "-c",
            script,
            str(ROOT),
            str(raw_docx),
            str(template_docx),
            json.dumps(visuals, ensure_ascii=False),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


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
    runtime_python = document_runtime_python()

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
    runtime_python = document_runtime_python()

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


def test_editorial_renderer_preserves_nested_block_dispatch_and_formatting(
    tmp_path: Path,
) -> None:
    document, metrics = render_editorial_fixture(
        tmp_path,
        """
        <p><img src="visuals/fixture.png" alt="Проверочная схема"></p>
        <p>Свежий заголовок</p>
        <h1>Часть I. Проверка диспетчеризации</h1>
        <section><article>
          <p>Таблица 7. Проверочная подпись</p>
          <blockquote><p>Цитата <strong>важна</strong></p></blockquote>
          <hr>
          <ul><li>Маркер<ol><li>Вложенный номер</li></ol></li></ul>
          <pre><code>alpha
beta</code></pre>
          <table>
            <thead><tr><th>Ключ</th><th>Значение</th></tr></thead>
            <tbody><tr><td>один</td><td>два</td></tr></tbody>
          </table>
          <aside><p>Рекурсивный хвост</p></aside>
        </article></section>
        """,
    )

    body = document.find(f"{{{WORD_NS}}}body")
    assert body is not None
    rendered_blocks = []
    for child in body:
        if child.tag == f"{{{WORD_NS}}}tbl":
            rendered_blocks.append("table")
        elif child.tag == f"{{{WORD_NS}}}p":
            text = paragraph_text(child)
            if child.find(f".//{{{WORD_NS}}}drawing") is not None:
                rendered_blocks.append("image")
            elif child.find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}pBdr") is not None:
                rendered_blocks.append("rule")
            elif child.find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}numPr") is not None:
                rendered_blocks.append(f"list:{text}")
            elif child.find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}shd") is not None:
                rendered_blocks.append(f"code:{text}")
            else:
                rendered_blocks.append(text)
    assert rendered_blocks[:2] == ["image", "Свежий заголовок"]
    assert rendered_blocks[-9:] == [
        "Таблица 7. Проверочная подпись",
        "Цитата важна",
        "rule",
        "list:Маркер",
        "list:Вложенный номер",
        "code:alpha",
        "code:beta",
        "table",
        "Рекурсивный хвост",
    ]

    paragraphs = document.findall(f".//{{{WORD_NS}}}p")
    by_text = {paragraph_text(paragraph): paragraph for paragraph in paragraphs}

    title = by_text["Свежий заголовок"]
    title_properties = title.find(f"{{{WORD_NS}}}pPr")
    assert title_properties is not None
    title_spacing = title_properties.find(f"{{{WORD_NS}}}spacing")
    assert title_spacing is not None
    assert title_spacing.attrib[f"{{{WORD_NS}}}before"] == "0"
    assert title_spacing.attrib[f"{{{WORD_NS}}}after"] == "60"
    assert title_properties.find(f"{{{WORD_NS}}}keepNext") is not None
    title_run_properties = title.find(f"{{{WORD_NS}}}r/{{{WORD_NS}}}rPr")
    assert title_run_properties is not None
    title_fonts = title_run_properties.find(f"{{{WORD_NS}}}rFonts")
    assert title_fonts is not None
    assert set(title_fonts.attrib.values()) == {"Arial"}
    assert title_run_properties.find(f"{{{WORD_NS}}}sz").attrib[f"{{{WORD_NS}}}val"] == "52"
    assert title_run_properties.find(f"{{{WORD_NS}}}color").attrib[
        f"{{{WORD_NS}}}val"
    ] == "000000"
    assert title_run_properties.find(f"{{{WORD_NS}}}b").attrib[
        f"{{{WORD_NS}}}val"
    ] == "0"

    image = next(
        paragraph
        for paragraph in paragraphs
        if paragraph.find(f".//{{{WORD_NS}}}drawing") is not None
    )
    assert image.find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}jc").attrib[
        f"{{{WORD_NS}}}val"
    ] == "center"
    assert image.find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}keepNext") is not None
    image_properties = image.find(f".//{{{DRAWING_NS}}}docPr")
    assert image_properties is not None
    assert image_properties.attrib["title"] == "Иллюстрация к рукописи"
    assert image_properties.attrib["descr"] == "Проверочная схема"

    caption = by_text["Таблица 7. Проверочная подпись"]
    caption_properties = caption.find(f"{{{WORD_NS}}}pPr")
    assert caption_properties is not None
    assert caption_properties.find(f"{{{WORD_NS}}}pStyle").attrib[
        f"{{{WORD_NS}}}val"
    ] == "Caption"
    assert caption_properties.find(f"{{{WORD_NS}}}keepNext") is not None
    assert caption_properties.find(f"{{{WORD_NS}}}keepLines") is not None

    quote = by_text["Цитата важна"]
    quote_indent = quote.find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}ind")
    assert quote_indent is not None
    assert quote_indent.attrib[f"{{{WORD_NS}}}left"] == "432"
    quote_runs = quote.findall(f"{{{WORD_NS}}}r")
    assert all(run.find(f"{{{WORD_NS}}}rPr/{{{WORD_NS}}}i") is not None for run in quote_runs)
    assert quote_runs[-1].find(f"{{{WORD_NS}}}rPr/{{{WORD_NS}}}b") is not None

    rule = next(
        paragraph
        for paragraph in paragraphs
        if paragraph.find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}pBdr") is not None
    )
    bottom_border = rule.find(
        f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}pBdr/{{{WORD_NS}}}bottom"
    )
    assert bottom_border is not None
    assert {
        name.split("}")[-1]: value for name, value in bottom_border.attrib.items()
    } == {"val": "single", "sz": "4", "color": "B7B7B7"}

    list_paragraphs = [
        paragraph
        for paragraph in paragraphs
        if paragraph.find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}numPr") is not None
    ]
    assert [
        paragraph.find(
            f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}numPr/{{{WORD_NS}}}ilvl"
        ).attrib[f"{{{WORD_NS}}}val"]
        for paragraph in list_paragraphs
    ] == ["0", "1"]

    code_paragraphs = [
        paragraph
        for paragraph in paragraphs
        if (
            shading := paragraph.find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}shd")
        )
        is not None
        and shading.attrib[f"{{{WORD_NS}}}fill"] == "F5F5F5"
    ]
    assert [paragraph_text(paragraph) for paragraph in code_paragraphs] == ["alpha", "beta"]
    for paragraph in code_paragraphs:
        run_properties = paragraph.find(f"{{{WORD_NS}}}r/{{{WORD_NS}}}rPr")
        assert run_properties is not None
        assert set(
            run_properties.find(f"{{{WORD_NS}}}rFonts").attrib.values()
        ) == {"Roboto Mono"}
        assert run_properties.find(f"{{{WORD_NS}}}sz").attrib[
            f"{{{WORD_NS}}}val"
        ] == "17"
        assert paragraph.find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}keepLines") is not None

    assert metrics | {
        "images": 1,
        "lists": 2,
        "list_items": 2,
        "code_lines": 2,
        "tables": 1,
    } == metrics


def test_editorial_renderer_preserves_table_layout_and_pagination(
    tmp_path: Path,
) -> None:
    document, metrics = render_editorial_fixture(
        tmp_path,
        """
        <section>
          <table></table>
          <article><table>
            <thead><tr><th>Identifier</th><th>State</th><th>Notes</th></tr></thead>
            <tbody>
              <tr>
                <td><code>agent_runtime_policy</code></td><td>ready</td>
                <td>Detailed explanatory value for proportional sizing</td>
              </tr>
              <tr><td>worker</td><td><code>mono</code></td><td>middle</td></tr>
              <tr><td>tail</td><td>done</td><td>last</td></tr>
            </tbody>
          </table></article>
        </section>
        """,
    )

    tables = document.findall(f".//{{{WORD_NS}}}tbl")
    assert len(tables) == 1
    assert metrics["tables"] == 1
    assert metrics["paragraphs"] == 0
    table = tables[0]

    table_properties = table.find(f"{{{WORD_NS}}}tblPr")
    assert table_properties is not None
    assert table_properties.find(f"{{{WORD_NS}}}jc").attrib[
        f"{{{WORD_NS}}}val"
    ] == "left"
    assert table_properties.find(f"{{{WORD_NS}}}tblLayout").attrib[
        f"{{{WORD_NS}}}type"
    ] == "fixed"

    widths = [
        int(column.attrib[f"{{{WORD_NS}}}w"])
        for column in table.findall(f"{{{WORD_NS}}}tblGrid/{{{WORD_NS}}}gridCol")
    ]
    assert len(widths) == 3
    assert 0.319 <= widths[0] / sum(widths) <= 0.321

    rows = table.findall(f"{{{WORD_NS}}}tr")
    assert len(rows) == 4
    repeat_header = rows[0].find(f"{{{WORD_NS}}}trPr/{{{WORD_NS}}}tblHeader")
    assert repeat_header is not None
    assert repeat_header.attrib[f"{{{WORD_NS}}}val"] == "true"
    assert all(
        row.find(f"{{{WORD_NS}}}trPr/{{{WORD_NS}}}cantSplit") is not None
        for row in rows
    )

    for row_index, row in enumerate(rows):
        cells = row.findall(f"{{{WORD_NS}}}tc")
        assert len(cells) == 3
        for column_index, cell in enumerate(cells):
            assert int(
                cell.find(f"{{{WORD_NS}}}tcPr/{{{WORD_NS}}}tcW").attrib[
                    f"{{{WORD_NS}}}w"
                ]
            ) == widths[column_index]
            assert cell.find(f"{{{WORD_NS}}}tcPr/{{{WORD_NS}}}vAlign").attrib[
                f"{{{WORD_NS}}}val"
            ] == "center"
            paragraph = cell.find(f"{{{WORD_NS}}}p")
            assert paragraph is not None
            assert paragraph.find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}jc").attrib[
                f"{{{WORD_NS}}}val"
            ] == ("center" if row_index == 0 else "left")
            assert (
                paragraph.find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}keepNext") is not None
            ) == (row_index in {0, 1, 2})
            shading = cell.find(f"{{{WORD_NS}}}tcPr/{{{WORD_NS}}}shd")
            if row_index == 0:
                assert shading is not None
                assert shading.attrib[f"{{{WORD_NS}}}fill"] == "EDEDED"
                assert all(
                    run.find(f"{{{WORD_NS}}}rPr/{{{WORD_NS}}}b") is not None
                    for run in paragraph.findall(f"{{{WORD_NS}}}r")
                )
            else:
                assert shading is None

    monospace = next(
        run
        for run in table.findall(f".//{{{WORD_NS}}}r")
        if paragraph_text(run) == "agent_runtime_policy"
    )
    monospace_properties = monospace.find(f"{{{WORD_NS}}}rPr")
    assert monospace_properties is not None
    assert set(
        monospace_properties.find(f"{{{WORD_NS}}}rFonts").attrib.values()
    ) == {"Roboto Mono"}
    assert monospace_properties.find(f"{{{WORD_NS}}}sz").attrib[
        f"{{{WORD_NS}}}val"
    ] == "16"


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


def test_template2000n_semantic_style_mapping_characterization() -> None:
    document, mappings = map_template_semantic_styles_in_runtime(
        template_semantic_style_fixture_xml()
    )

    assert mappings == {
        "body_text": 4,
        "table_header": 1,
        "table_body": 1,
        "callout_heading": 3,
        "callout_body": 1,
        "table_caption": 1,
        "list": 1,
        "program": 1,
        "picture": 3,
        "picture_kept_with_caption": 1,
        "image_alt_text": 3,
        "figure_caption": 1,
    }

    style_attribute = f"{{{WORD_NS}}}val"
    paragraphs = document.findall(f".//{{{WORD_NS}}}p")
    by_text = {paragraph_text(paragraph): paragraph for paragraph in paragraphs}
    expected_styles = {
        "Вводный текст": "BodyText",
        "Заголовок таблицы": "Style20",
        "Ячейка таблицы": "Style21",
        "Практическая проверка.": "Style24",
        "Тело после пустого абзаца": "Style23",
        "Таблица 4. Проверочная таблица": "Style17",
        "Элемент списка": "Style18",
        "print('ok')": "Style16",
        "Сохраненный заголовок": "Heading1",
        "Частые ошибки.": "Style24",
        "Заголовок сбрасывает выноску": "Heading2",
        "Title": "Title",
        "H3": "Heading3",
        "H4": "Heading4",
        "H5": "Heading5",
        "Текст после заголовка": "BodyText",
        "Граница доказательств.": "Style24",
        "Рисунок 8. Подпись после изображения": "Style17",
        "Текст после изображения": "BodyText",
        "Опорный текст": "BodyText",
    }
    assert {
        text: by_text[text].find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}pStyle").attrib[
            style_attribute
        ]
        for text in expected_styles
    } == expected_styles

    blank_paragraph = next(paragraph for paragraph in paragraphs if len(paragraph) == 0)
    assert blank_paragraph.find(f"{{{WORD_NS}}}pPr") is None

    table_caption = by_text["Таблица 4. Проверочная таблица"]
    assert table_caption.find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}keepNext") is not None
    assert table_caption.find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}keepLines") is not None

    figure_caption = by_text["Рисунок 8. Подпись после изображения"]
    assert figure_caption.find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}keepLines") is not None

    images = [
        paragraph
        for paragraph in paragraphs
        if paragraph.find(f".//{{{WORD_NS}}}drawing") is not None
    ]
    assert [
        paragraph.find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}pStyle").attrib[
            style_attribute
        ]
        for paragraph in images
    ] == ["Style28", "Style28", "Style28"]
    assert images[0].find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}keepNext") is not None
    assert images[1].find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}keepNext") is None
    assert images[2].find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}keepNext") is None

    image_properties = document.findall(f".//{{{DRAWING_NS}}}docPr")
    assert [properties.attrib["title"] for properties in image_properties] == [
        "Иллюстрация к рукописи",
        "Иллюстрация к рукописи",
        "Иллюстрация к рукописи",
    ]
    assert [properties.attrib["descr"] for properties in image_properties] == [
        "Рисунок 8. Подпись после изображения",
        "Готовое описание",
        "Опорный текст",
    ]


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
        assert (
            len(re.findall(r"^Таблица \d+\. .+$", document_text, re.MULTILINE))
            == EXPECTED_TABLE_COUNT
        )


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


def test_audit_docx_characterizes_media_order_and_metrics(tmp_path: Path) -> None:
    payloads = [_png_payload(seed=index) for index in range(1, 26)]
    visuals = _audit_visuals(tmp_path / "assets", payloads)
    raw_docx = tmp_path / "raw.docx"
    template_docx = tmp_path / "template.docx"
    _write_docx_fixture(raw_docx, payloads, numbered_count=25)
    _write_docx_fixture(template_docx, payloads, numbered_count=25)

    result = _audit_docx_in_runtime(raw_docx, template_docx, visuals)

    assert result == {
        "metrics": {
            "alpha_images": 0,
            "max_aspect_error": 0.0,
            "max_height_inches": 1.0,
            "numbered_figure_caption_pairs": 25,
            "raw_images": 25,
            "raw_media_matches_source": True,
            "template_images": 25,
            "template_media_order_matches_raw": True,
        }
    }

    swapped_payloads = [payloads[1], payloads[0], *payloads[2:]]
    _write_docx_fixture(raw_docx, swapped_payloads, numbered_count=25)
    assert _audit_docx_in_runtime(raw_docx, template_docx, visuals) == {
        "error": "Raw DOCX media no longer matches manuscript visual order"
    }

    _write_docx_fixture(raw_docx, payloads, numbered_count=25)
    relationship_ids = ["rId2", "rId1", *[f"rId{index}" for index in range(3, 26)]]
    _write_docx_fixture(
        template_docx,
        payloads,
        drawing_relationship_ids=relationship_ids,
        numbered_count=25,
    )
    assert _audit_docx_in_runtime(raw_docx, template_docx, visuals) == {
        "error": "Template2000n changed media relationship order"
    }


@pytest.mark.parametrize(
    ("case", "expected_error"),
    [
        ("blank-alt", "Template2000n contains an image without alternative text"),
        ("aspect", "A Template2000n image is geometrically distorted"),
        ("height", "A Template2000n image exceeds the print-height limit"),
        ("alpha", "Template2000n contains an alpha-channel image"),
    ],
)
def test_audit_docx_rejects_invalid_template_media(
    tmp_path: Path,
    case: str,
    expected_error: str,
) -> None:
    payloads = [_png_payload(seed=index) for index in range(1, 26)]
    visuals = _audit_visuals(tmp_path / "assets", payloads)
    raw_docx = tmp_path / "raw.docx"
    template_docx = tmp_path / "template.docx"
    _write_docx_fixture(raw_docx, payloads, numbered_count=25)

    descriptions = [f"Alternative text {index}" for index in range(1, 26)]
    extents = [
        (2 * sync_ru_docx_visuals.EMU_PER_INCH, sync_ru_docx_visuals.EMU_PER_INCH) for _ in payloads
    ]
    template_payloads = list(payloads)
    if case == "blank-alt":
        descriptions[0] = " "
    elif case == "aspect":
        extents[0] = (
            sync_ru_docx_visuals.EMU_PER_INCH,
            sync_ru_docx_visuals.EMU_PER_INCH,
        )
    elif case == "height":
        extents[0] = (
            14 * sync_ru_docx_visuals.EMU_PER_INCH,
            7 * sync_ru_docx_visuals.EMU_PER_INCH,
        )
    else:
        template_payloads[0] = _png_payload(seed=1, alpha=True)
    _write_docx_fixture(
        template_docx,
        template_payloads,
        descriptions=descriptions,
        extents=extents,
        numbered_count=25,
    )

    assert _audit_docx_in_runtime(raw_docx, template_docx, visuals) == {"error": expected_error}


def test_audit_docx_rejects_a_missing_numbered_caption(tmp_path: Path) -> None:
    payloads = [_png_payload(seed=index) for index in range(1, 26)]
    visuals = _audit_visuals(tmp_path / "assets", payloads)
    raw_docx = tmp_path / "raw.docx"
    template_docx = tmp_path / "template.docx"
    _write_docx_fixture(raw_docx, payloads, numbered_count=25)
    _write_docx_fixture(
        template_docx,
        payloads,
        numbered_count=25,
        missing_caption=7,
    )

    assert _audit_docx_in_runtime(raw_docx, template_docx, visuals) == {
        "error": "Caption does not follow figure 7"
    }


@pytest.mark.parametrize(
    ("case", "expected_error"),
    [
        ("count", "DOCX has 55 drawings; manuscript has 56 visuals"),
        ("relationship", "Image relationship is missing: rMissing"),
        ("duplicate", "Multiple drawings unexpectedly share one media target"),
    ],
)
def test_synchronize_rejects_invalid_docx_structure(
    tmp_path: Path,
    case: str,
    expected_error: str,
) -> None:
    source_payloads = [_png_payload(seed=index) for index in range(1, 57)]
    manuscript = _write_manuscript_fixture(tmp_path / "source", source_payloads)
    input_payloads = [_png_payload(seed=index + 100) for index in range(1, 57)]
    relationship_ids = [f"rId{index}" for index in range(1, 57)]
    targets = [f"media/image-{index}.png" for index in range(1, 57)]
    if case == "count":
        input_payloads = input_payloads[:-1]
        relationship_ids = relationship_ids[:-1]
        targets = targets[:-1]
    elif case == "relationship":
        relationship_ids[0] = "rMissing"
    else:
        targets[1] = targets[0]

    input_docx = tmp_path / "input.docx"
    output_docx = tmp_path / "nested/output.docx"
    _write_docx_fixture(
        input_docx,
        input_payloads,
        drawing_relationship_ids=relationship_ids,
        relationship_targets=targets,
        numbered_count=min(25, len(input_payloads)),
        captions_before_drawings=True,
    )

    with pytest.raises(ValueError, match=re.escape(expected_error)):
        sync_ru_docx_visuals.synchronize(input_docx, manuscript, output_docx)
    assert not output_docx.exists()


def test_synchronize_drawing_rejects_a_numbered_figure_without_a_parent(
    tmp_path: Path,
) -> None:
    root = tmp_path / "docx"
    destination = root / "word/media/image-1.png"
    destination.parent.mkdir(parents=True)
    original_payload = _png_payload(seed=200)
    destination.write_bytes(original_payload)
    source = tmp_path / "source.png"
    source_payload = _png_payload(seed=1)
    source.write_bytes(source_payload)
    body = ET.Element(f"{{{WORD_NS}}}body")
    drawing_parts = _drawing_paragraph(
        body,
        index=1,
        relationship_id="rId1",
        description="Old alternative text",
        extent=(
            2 * sync_ru_docx_visuals.EMU_PER_INCH,
            sync_ru_docx_visuals.EMU_PER_INCH,
        ),
    )
    original_drawing_xml = ET.tostring(drawing_parts[1])
    visual: sync_ru_docx_visuals.VisualRecord = {
        "path": source,
        "relative_path": "visuals/source.png",
        "figure_number": 1,
        "figure_title": "Новое название 1",
        "alt": "Alt 1",
    }

    with pytest.raises(ValueError, match="Figure 1 has no document parent"):
        sync_ru_docx_visuals._synchronize_drawing(
            root,
            visual,
            drawing_parts,
            {"rId1": "word/media/image-1.png"},
            {},
        )
    assert destination.read_bytes() == original_payload
    assert ET.tostring(drawing_parts[1]) == original_drawing_xml


def test_synchronize_preserves_caption_relocation_media_and_metrics(tmp_path: Path) -> None:
    source_payloads = [_png_payload(seed=index) for index in range(1, 57)]
    manuscript = _write_manuscript_fixture(tmp_path / "source", source_payloads)
    input_docx = tmp_path / "input.docx"
    output_docx = tmp_path / "nested/output.docx"
    _write_docx_fixture(
        input_docx,
        [_png_payload(seed=index + 100) for index in range(1, 57)],
        numbered_count=25,
        captions_before_drawings=True,
    )

    metrics = sync_ru_docx_visuals.synchronize(input_docx, manuscript, output_docx)

    subprocess.run(
        [
            str(document_runtime_python()),
            "-c",
            "import sys; from docx import Document; Document(sys.argv[1])",
            str(output_docx),
        ],
        cwd=ROOT,
        check=True,
    )
    assert metrics == {
        "input_docx": str(input_docx),
        "manuscript": str(manuscript),
        "output_docx": str(output_docx),
        "output_bytes": output_docx.stat().st_size,
        "output_sha256": hashlib.sha256(output_docx.read_bytes()).hexdigest(),
        "visuals_synchronized": 56,
        "numbered_figures_reordered": 25,
        "media_targets_unique": 56,
        "max_numbered_figure_height_inches": 1.0,
    }
    targets, hashes = ordered_embedded_images(output_docx)
    assert len(targets) == len(set(targets)) == 56
    assert hashes == [hashlib.sha256(payload).hexdigest() for payload in source_payloads]

    with ZipFile(output_docx) as archive:
        assert archive.namelist() == sorted(archive.namelist())
        assert archive.read(PRESERVED_DOCX_MEMBER) == PRESERVED_DOCX_PAYLOAD
        document = ET.fromstring(archive.read("word/document.xml"))
    paragraphs = document.findall(f".//{{{WORD_NS}}}p")
    first_drawing_index = next(
        index
        for index, paragraph in enumerate(paragraphs)
        if paragraph.find(f".//{{{WORD_NS}}}drawing") is not None
    )
    texts = [
        "".join(node.text or "" for node in paragraph.findall(f".//{{{WORD_NS}}}t"))
        for paragraph in paragraphs
    ]
    assert texts[first_drawing_index - 1] == "На рисунке 1 представлена схема «Новое название 1»."
    assert texts[first_drawing_index + 1] == "Рисунок 1. Новое название 1"
    image_paragraph = paragraphs[first_drawing_index]
    caption = paragraphs[first_drawing_index + 1]
    assert image_paragraph.find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}keepNext") is not None
    assert caption.find(f"{{{WORD_NS}}}pPr/{{{WORD_NS}}}keepLines") is not None
    properties = image_paragraph.find(f".//{{{DRAWING_NS}}}docPr")
    assert properties is not None
    assert properties.attrib["title"] == "Иллюстрация к рукописи"
    assert properties.attrib["descr"] == "Alt 1"
    extents = image_paragraph.findall(f".//{{{DRAWINGML_NS}}}ext")
    assert [(node.attrib["cx"], node.attrib["cy"]) for node in extents] == [
        (
            str(2 * sync_ru_docx_visuals.EMU_PER_INCH),
            str(sync_ru_docx_visuals.EMU_PER_INCH),
        )
    ]
