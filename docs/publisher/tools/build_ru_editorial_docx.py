from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.opc.constants import RELATIONSHIP_TYPE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from lxml import html
from PIL import Image

FIRST_CHAPTERS_IN_PART = {1, 4, 7, 10, 13, 17, 22, 26}
CODE_FONT = "Roboto Mono"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def markdown_to_html(manuscript: Path, node: Path, node_path: Path) -> str:
    script = r"""
import fs from "node:fs";
import {createRequire} from "node:module";
const require = createRequire(import.meta.url);
const {marked} = await import(require.resolve("marked"));
const source = fs.readFileSync(process.argv[1], "utf8");
process.stdout.write(marked.parse(source, {gfm: true}));
"""
    environment = os.environ.copy()
    environment["NODE_PATH"] = str(node_path)
    result = subprocess.run(
        [str(node), "--input-type=module", "-e", script, str(manuscript)],
        check=True,
        capture_output=True,
        text=True,
        env=environment,
    )
    return result.stdout


def clear_document_body(document: Document) -> None:
    body = document._element.body
    for child in list(body):
        if child.tag != qn("w:sectPr"):
            body.remove(child)


def set_run_font(run, name: str, size: float | None = None) -> None:
    run.font.name = name
    if size is not None:
        run.font.size = Pt(size)
    properties = run._r.get_or_add_rPr()
    fonts = properties.rFonts
    if fonts is None:
        fonts = OxmlElement("w:rFonts")
        properties.insert(0, fonts)
    for attribute in ("ascii", "hAnsi", "eastAsia", "cs"):
        fonts.set(qn(f"w:{attribute}"), name)


def set_page_break_before(paragraph) -> None:
    properties = paragraph._p.get_or_add_pPr()
    if properties.find(qn("w:pageBreakBefore")) is None:
        properties.append(OxmlElement("w:pageBreakBefore"))


def set_keep_next(paragraph) -> None:
    properties = paragraph._p.get_or_add_pPr()
    if properties.find(qn("w:keepNext")) is None:
        properties.append(OxmlElement("w:keepNext"))


def set_keep_lines(paragraph) -> None:
    properties = paragraph._p.get_or_add_pPr()
    if properties.find(qn("w:keepLines")) is None:
        properties.append(OxmlElement("w:keepLines"))


def add_hyperlink(paragraph, text: str, url: str) -> None:
    relationship_id = paragraph.part.relate_to(
        url,
        RELATIONSHIP_TYPE.HYPERLINK,
        is_external=True,
    )
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), relationship_id)
    run = OxmlElement("w:r")
    properties = OxmlElement("w:rPr")
    color = OxmlElement("w:color")
    color.set(qn("w:val"), "1155CC")
    underline = OxmlElement("w:u")
    underline.set(qn("w:val"), "single")
    properties.extend((color, underline))
    run.append(properties)
    value = OxmlElement("w:t")
    value.text = text
    run.append(value)
    hyperlink.append(run)
    paragraph._p.append(hyperlink)


def normalized_prose(text: str | None) -> str:
    return re.sub(r"\s+", " ", text or "")


@dataclass(frozen=True)
class InlineStyle:
    bold: bool = False
    italic: bool = False
    code: bool = False


def add_text(paragraph, value: str, style: InlineStyle) -> None:
    if not value:
        return
    if not paragraph.text and not paragraph._p.findall(qn("w:hyperlink")):
        value = value.lstrip()
    run = paragraph.add_run(value)
    run.bold = style.bold
    run.italic = style.italic
    if style.code:
        set_run_font(run, CODE_FONT, 9)
        run.font.color.rgb = RGBColor(55, 55, 55)


def render_inline(paragraph, element, style: InlineStyle = InlineStyle()) -> None:
    add_text(paragraph, normalized_prose(element.text), style)
    for child in element:
        tag = child.tag.lower() if isinstance(child.tag, str) else ""
        if tag in {"ul", "ol", "table", "pre"}:
            continue
        if tag == "strong":
            render_inline(paragraph, child, InlineStyle(True, style.italic, style.code))
        elif tag == "em":
            render_inline(paragraph, child, InlineStyle(style.bold, True, style.code))
        elif tag == "code":
            render_inline(paragraph, child, InlineStyle(style.bold, style.italic, True))
        elif tag == "a":
            add_hyperlink(paragraph, "".join(child.itertext()).strip(), child.get("href", ""))
        elif tag == "br":
            paragraph.add_run().add_break()
        elif tag != "img":
            render_inline(paragraph, child, style)
        add_text(paragraph, normalized_prose(child.tail), style)


class NumberingManager:
    def __init__(self, document: Document) -> None:
        self.root = document.part.numbering_part.element
        self.abstract_ids = {kind: self._find_abstract_id(kind) for kind in ("bullet", "decimal")}
        self.next_num_id = (
            max([int(node.get(qn("w:numId"))) for node in self.root.findall(qn("w:num"))] or [0])
            + 1
        )

    def _find_abstract_id(self, kind: str) -> int:
        for abstract in self.root.findall(qn("w:abstractNum")):
            level = abstract.find(qn("w:lvl"))
            if level is None:
                continue
            number_format = level.find(qn("w:numFmt"))
            if number_format is not None and number_format.get(qn("w:val")) == kind:
                return int(abstract.get(qn("w:abstractNumId")))
        raise ValueError(f"Base DOCX has no {kind} numbering definition")

    def new_list(self, kind: str) -> int:
        number_id = self.next_num_id
        self.next_num_id += 1
        number = OxmlElement("w:num")
        number.set(qn("w:numId"), str(number_id))
        abstract = OxmlElement("w:abstractNumId")
        abstract.set(qn("w:val"), str(self.abstract_ids[kind]))
        number.append(abstract)
        self.root.append(number)
        return number_id

    @staticmethod
    def apply(paragraph, number_id: int, level: int) -> None:
        properties = paragraph._p.get_or_add_pPr()
        number_properties = properties.find(qn("w:numPr"))
        if number_properties is None:
            number_properties = OxmlElement("w:numPr")
            properties.append(number_properties)
        indentation = OxmlElement("w:ilvl")
        indentation.set(qn("w:val"), str(min(level, 8)))
        number = OxmlElement("w:numId")
        number.set(qn("w:val"), str(number_id))
        number_properties.extend((indentation, number))


class DocxRenderer:
    def __init__(self, document: Document, manuscript: Path) -> None:
        self.document = document
        self.manuscript = manuscript
        self.numbering = NumberingManager(document)
        section = document.sections[0]
        self.usable_width = section.page_width - section.left_margin - section.right_margin
        self.usable_height = section.page_height - section.top_margin - section.bottom_margin
        self.metrics = {
            "headings": 0,
            "paragraphs": 0,
            "lists": 0,
            "list_items": 0,
            "tables": 0,
            "images": 0,
            "code_lines": 0,
            "page_breaks": 0,
        }
        self.is_first_element = True

    def render(self, root) -> None:
        for element in root:
            self.render_block(element)

    def add_paragraph(self):
        paragraph = self.document.add_paragraph()
        self.metrics["paragraphs"] += 1
        return paragraph

    def render_block(self, element, list_level: int = 0) -> None:
        tag = element.tag.lower() if isinstance(element.tag, str) else ""
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.render_heading(element, int(tag[1]))
        elif tag == "p":
            images = element.findall("img")
            prose = normalized_prose(element.text).strip()
            if len(images) == 1 and not prose and len(element) == 1:
                self.render_image(images[0])
            else:
                paragraph = self.add_paragraph()
                if self.is_first_element:
                    self.render_title(paragraph, element)
                else:
                    render_inline(paragraph, element)
                self.is_first_element = False
        elif tag in {"ul", "ol"}:
            self.render_list(element, list_level)
        elif tag == "pre":
            self.render_code_block(element)
        elif tag == "table":
            self.render_table(element)
        elif tag == "blockquote":
            for child in element:
                paragraph = self.add_paragraph()
                paragraph.paragraph_format.left_indent = Inches(0.3)
                render_inline(paragraph, child, InlineStyle(italic=True))
        elif tag == "hr":
            paragraph = self.add_paragraph()
            border = OxmlElement("w:pBdr")
            bottom = OxmlElement("w:bottom")
            bottom.set(qn("w:val"), "single")
            bottom.set(qn("w:sz"), "4")
            bottom.set(qn("w:color"), "B7B7B7")
            border.append(bottom)
            paragraph._p.get_or_add_pPr().append(border)
        else:
            for child in element:
                self.render_block(child, list_level)

    def render_title(self, paragraph, element) -> None:
        render_inline(paragraph, element)
        paragraph.paragraph_format.space_before = Pt(0)
        paragraph.paragraph_format.space_after = Pt(3)
        set_keep_next(paragraph)
        for run in paragraph.runs:
            set_run_font(run, "Arial", 26)
            run.bold = False
            run.font.color.rgb = RGBColor(0, 0, 0)

    def render_heading(self, element, level: int) -> None:
        paragraph = self.document.add_paragraph(style=f"Heading {min(level, 6)}")
        render_inline(paragraph, element)
        self.metrics["headings"] += 1
        text = paragraph.text.strip()
        page_break = level == 1
        if level == 2:
            match = re.fullmatch(r"Глава (\d+)\. .+", text)
            page_break = match is not None and int(match.group(1)) not in FIRST_CHAPTERS_IN_PART
        if page_break:
            set_page_break_before(paragraph)
            self.metrics["page_breaks"] += 1
        set_keep_next(paragraph)
        self.is_first_element = False

    def render_list(self, element, level: int) -> None:
        kind = "bullet" if element.tag.lower() == "ul" else "decimal"
        number_id = self.numbering.new_list(kind)
        self.metrics["lists"] += 1
        for item in element.findall("li"):
            paragraph = self.add_paragraph()
            self.numbering.apply(paragraph, number_id, level)
            render_inline(paragraph, item)
            self.metrics["list_items"] += 1
            for nested in item:
                if isinstance(nested.tag, str) and nested.tag.lower() in {"ul", "ol"}:
                    self.render_list(nested, level + 1)

    def render_code_block(self, element) -> None:
        code = element.find("code")
        value = "".join(code.itertext()) if code is not None else "".join(element.itertext())
        for line in value.rstrip("\n").split("\n"):
            paragraph = self.add_paragraph()
            paragraph.paragraph_format.left_indent = Inches(0.22)
            paragraph.paragraph_format.right_indent = Inches(0.12)
            paragraph.paragraph_format.space_before = Pt(0)
            paragraph.paragraph_format.space_after = Pt(0)
            paragraph.paragraph_format.line_spacing = 1.0
            set_keep_lines(paragraph)
            shading = OxmlElement("w:shd")
            shading.set(qn("w:fill"), "F5F5F5")
            paragraph._p.get_or_add_pPr().append(shading)
            run = paragraph.add_run(line or " ")
            set_run_font(run, CODE_FONT, 8.5)
            self.metrics["code_lines"] += 1

    def render_image(self, element) -> None:
        source = element.get("src", "")
        image_path = (self.manuscript.parent / source).resolve()
        if not image_path.is_file():
            raise FileNotFoundError(f"Missing manuscript image: {source}")
        with Image.open(image_path) as image:
            width_px, height_px = image.size
            dpi = image.info.get("dpi", (96, 96))
            dpi_x = float(dpi[0] or 96)
            dpi_y = float(dpi[1] or 96)
        natural_width = Inches(width_px / dpi_x)
        natural_height = Inches(height_px / dpi_y)
        scale = min(
            1.0,
            self.usable_width / natural_width,
            (self.usable_height * 0.82) / natural_height,
        )
        paragraph = self.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_keep_next(paragraph)
        shape = paragraph.add_run().add_picture(str(image_path), width=int(natural_width * scale))
        alt = element.get("alt", "").strip() or image_path.stem
        shape._inline.docPr.set("title", "Иллюстрация к рукописи")
        shape._inline.docPr.set("descr", alt[:250])
        self.metrics["images"] += 1

    def render_table(self, element) -> None:
        rows = element.xpath("./thead/tr | ./tbody/tr | ./tr")
        if not rows:
            return
        column_count = max(len(row.xpath("./th | ./td")) for row in rows)
        table = self.document.add_table(rows=len(rows), cols=column_count)
        table.autofit = False
        text_lengths = [1] * column_count
        for row_index, row in enumerate(rows):
            cells = row.xpath("./th | ./td")
            for column_index, cell in enumerate(cells):
                target = table.cell(row_index, column_index)
                paragraph = target.paragraphs[0]
                render_inline(
                    paragraph,
                    cell,
                    InlineStyle(bold=row_index == 0 or cell.tag.lower() == "th"),
                )
                text_lengths[column_index] = max(text_lengths[column_index], len(paragraph.text))
                if row_index == 0:
                    shading = OxmlElement("w:shd")
                    shading.set(qn("w:fill"), "EDEDED")
                    target._tc.get_or_add_tcPr().append(shading)
        total = sum(min(length, 48) for length in text_lengths)
        for column_index, length in enumerate(text_lengths):
            width = int(self.usable_width * min(length, 48) / total)
            table.columns[column_index].width = width
            for cell in table.columns[column_index].cells:
                cell.width = width
        self.metrics["tables"] += 1


def prune_unused_document_relationships(document: Document) -> None:
    used = {
        value
        for node in document._element.iter()
        for attribute, value in node.attrib.items()
        if attribute in {qn("r:id"), qn("r:embed"), qn("r:link")}
    }
    for relationship_id, relationship in list(document.part.rels.items()):
        if (
            relationship.reltype
            in {
                RELATIONSHIP_TYPE.IMAGE,
                RELATIONSHIP_TYPE.HYPERLINK,
            }
            and relationship_id not in used
        ):
            document.part.drop_rel(relationship_id)


def build(
    manuscript: Path,
    base_docx: Path,
    output_docx: Path,
    node: Path,
    node_path: Path,
) -> dict[str, object]:
    source_html = markdown_to_html(manuscript, node, node_path)
    root = html.fragment_fromstring(source_html, create_parent="div")
    document = Document(str(base_docx))
    clear_document_body(document)
    renderer = DocxRenderer(document, manuscript)
    renderer.render(root)
    prune_unused_document_relationships(document)
    output_docx.parent.mkdir(parents=True, exist_ok=True)
    document.save(str(output_docx))
    return {
        "manuscript": str(manuscript),
        "base_docx": str(base_docx),
        "output_docx": str(output_docx),
        "output_bytes": output_docx.stat().st_size,
        "output_sha256": sha256(output_docx),
        **renderer.metrics,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the Russian editorial DOCX")
    parser.add_argument("--manuscript", required=True, type=Path)
    parser.add_argument("--base-docx", required=True, type=Path)
    parser.add_argument("--output-docx", required=True, type=Path)
    parser.add_argument("--node", required=True, type=Path)
    parser.add_argument("--node-path", required=True, type=Path)
    parser.add_argument("--metrics-json", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    metrics = build(
        args.manuscript,
        args.base_docx,
        args.output_docx,
        args.node,
        args.node_path,
    )
    payload = json.dumps(metrics, ensure_ascii=False, indent=2, sort_keys=True)
    if args.metrics_json:
        args.metrics_json.write_text(payload + "\n", encoding="utf-8")
    print(payload)


if __name__ == "__main__":
    main()
