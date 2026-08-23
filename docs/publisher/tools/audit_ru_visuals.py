#!/usr/bin/env python3
"""Audit manuscript visual assets, DOCX mappings, and final PDF placements."""

from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import zipfile
from io import BytesIO
from pathlib import Path
from xml.etree import ElementTree as ET

import pdfplumber
from PIL import Image, ImageChops, ImageDraw

MIN_CONTENT_FILL_WIDTH = 0.88
MIN_CONTENT_FILL_HEIGHT = 0.78
MAX_PRINT_IMAGE_HEIGHT_INCHES = 6.35

if __package__:
    from .sync_ru_docx_visuals import (
        EMU_PER_INCH,
        NS,
        PACKAGE_REL_NS,
        paragraph_text,
        parse_manuscript_visuals,
        validate_docx_image_counts,
    )
else:
    from sync_ru_docx_visuals import (  # type: ignore[no-redef]
        EMU_PER_INCH,
        NS,
        PACKAGE_REL_NS,
        paragraph_text,
        parse_manuscript_visuals,
        validate_docx_image_counts,
    )


def payload_hash(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def content_fill(path: Path) -> tuple[float, float]:
    with Image.open(path).convert("RGB") as image:
        difference = ImageChops.difference(image, Image.new("RGB", image.size, "white"))
        box = difference.getbbox()
        if box is None:
            return 0.0, 0.0
        return (
            (box[2] - box[0]) / image.width,
            (box[3] - box[1]) / image.height,
        )


def audit_assets(visuals: list[dict[str, object]]) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for index, visual in enumerate(visuals, start=1):
        path = Path(visual["path"])
        with Image.open(path) as image:
            width, height = image.size
            has_alpha = "A" in image.mode or "transparency" in image.info
        fill_width, fill_height = content_fill(path)
        if has_alpha:
            raise ValueError(f"Visual has an alpha channel: {path}")
        if (
            fill_width < MIN_CONTENT_FILL_WIDTH
            or fill_height < MIN_CONTENT_FILL_HEIGHT
        ):
            raise ValueError(
                f"Visual has excessive whitespace: {path} ({fill_width:.3f}, {fill_height:.3f})"
            )
        results.append(
            {
                "index": index,
                "path": str(path),
                "width_px": width,
                "height_px": height,
                "content_fill_width": round(fill_width, 4),
                "content_fill_height": round(fill_height, 4),
                "sha256": payload_hash(path.read_bytes()),
            }
        )
    return results


def ordered_docx_images(
    path: Path,
) -> tuple[list[dict[str, object]], list[ET.Element], ET.Element]:
    with zipfile.ZipFile(path) as archive:
        document = ET.fromstring(archive.read("word/document.xml"))
        relationships = ET.fromstring(archive.read("word/_rels/document.xml.rels"))
        targets = {
            node.attrib["Id"]: posixpath.normpath(f"word/{node.attrib['Target']}")
            for node in relationships.findall(f"{{{PACKAGE_REL_NS}}}Relationship")
            if node.attrib.get("Type", "").endswith("/image")
        }
        results: list[dict[str, object]] = []
        image_paragraphs: list[ET.Element] = []
        for paragraph in document.findall(".//w:p", NS):
            for drawing in paragraph.findall(".//w:drawing", NS):
                blip = drawing.find(".//a:blip", NS)
                extent = drawing.find(".//wp:extent", NS)
                properties = drawing.find(".//wp:docPr", NS)
                if blip is None or extent is None or properties is None:
                    continue
                target = targets[blip.attrib[f"{{{NS['r']}}}embed"]]
                payload = archive.read(target)
                with Image.open(BytesIO(payload)) as image:
                    pixel_width, pixel_height = image.size
                    has_alpha = "A" in image.mode or "transparency" in image.info
                width = int(extent.attrib["cx"])
                height = int(extent.attrib["cy"])
                results.append(
                    {
                        "target": target,
                        "sha256": payload_hash(payload),
                        "descr": properties.attrib.get("descr", ""),
                        "width_inches": width / EMU_PER_INCH,
                        "height_inches": height / EMU_PER_INCH,
                        "pixel_width": pixel_width,
                        "pixel_height": pixel_height,
                        "has_alpha": has_alpha,
                        "aspect_error": abs((width / height) - (pixel_width / pixel_height)),
                    }
                )
                image_paragraphs.append(paragraph)
    return results, image_paragraphs, document


def _validate_docx_media(
    raw: list[dict[str, object]],
    template: list[dict[str, object]],
    visuals: list[dict[str, object]],
) -> None:
    validate_docx_image_counts(len(raw), len(template), len(visuals))

    expected_hashes = [payload_hash(Path(item["path"]).read_bytes()) for item in visuals]
    if [item["sha256"] for item in raw] != expected_hashes:
        raise ValueError("Raw DOCX media no longer matches manuscript visual order")
    if [item["target"] for item in template] != [item["target"] for item in raw]:
        raise ValueError("Template2000n changed media relationship order")
    if any(not item["descr"].strip() for item in template):
        raise ValueError("Template2000n contains an image without alternative text")
    if any(item["aspect_error"] > 0.002 for item in template):
        raise ValueError("A Template2000n image is geometrically distorted")
    if any(item["height_inches"] > MAX_PRINT_IMAGE_HEIGHT_INCHES for item in template):
        raise ValueError("A Template2000n image exceeds the print-height limit")
    if any(item["has_alpha"] for item in template):
        raise ValueError("Template2000n contains an alpha-channel image")


def _validate_numbered_figure_captions(
    visuals: list[dict[str, object]],
    image_paragraphs: list[ET.Element],
    document: ET.Element,
) -> int:
    paragraphs = document.findall(".//w:p", NS)
    paragraph_index = {paragraph: index for index, paragraph in enumerate(paragraphs)}
    numbered_pairs = 0
    for visual, image_paragraph in zip(visuals, image_paragraphs, strict=True):
        number = visual["figure_number"]
        if not number:
            continue
        index = paragraph_index[image_paragraph]
        following = next(
            (paragraph for paragraph in paragraphs[index + 1 :] if paragraph_text(paragraph)),
            None,
        )
        if following is None or not paragraph_text(following).startswith(f"Рисунок {number}."):
            raise ValueError(f"Caption does not follow figure {number}")
        numbered_pairs += 1
    if numbered_pairs != 25:
        raise ValueError(f"Expected 25 numbered figure-caption pairs, found {numbered_pairs}")
    return numbered_pairs


def audit_docx(
    raw_docx: Path,
    template_docx: Path,
    visuals: list[dict[str, object]],
) -> dict[str, object]:
    raw, _, _ = ordered_docx_images(raw_docx)
    template, template_paragraphs, template_document = ordered_docx_images(template_docx)
    _validate_docx_media(raw, template, visuals)
    numbered_pairs = _validate_numbered_figure_captions(
        visuals,
        template_paragraphs,
        template_document,
    )

    return {
        "raw_images": len(raw),
        "template_images": len(template),
        "raw_media_matches_source": True,
        "template_media_order_matches_raw": True,
        "numbered_figure_caption_pairs": numbered_pairs,
        "max_height_inches": round(max(item["height_inches"] for item in template), 3),
        "max_aspect_error": round(max(item["aspect_error"] for item in template), 6),
        "alpha_images": 0,
    }


def make_contact_sheets(
    pdf_path: Path,
    render_dir: Path,
    output_dir: Path,
    placements: list[dict[str, object]],
) -> list[str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    cells: list[Image.Image] = []
    with pdfplumber.open(pdf_path) as pdf:
        placement_index = 0
        for page_number, page in enumerate(pdf.pages, start=1):
            if not page.images:
                continue
            page_path = render_dir / f"page-{page_number}.png"
            if not page_path.exists():
                candidates = [
                    path
                    for path in render_dir.glob("page-*.png")
                    if path.stem.rsplit("-", 1)[-1].isdigit()
                    and int(path.stem.rsplit("-", 1)[-1]) == page_number
                ]
                if len(candidates) != 1:
                    raise FileNotFoundError(
                        f"Expected one rendered image for page {page_number}, "
                        f"found {len(candidates)}"
                    )
                page_path = candidates[0]
            with Image.open(page_path).convert("RGB") as page_image:
                scale_x = page_image.width / page.width
                scale_y = page_image.height / page.height
                for image in page.images:
                    left = max(0, round(float(image["x0"]) * scale_x) - 20)
                    right = min(
                        page_image.width,
                        round(float(image["x1"]) * scale_x) + 20,
                    )
                    top = max(0, round(float(image["top"]) * scale_y) - 70)
                    bottom = min(
                        page_image.height,
                        round(float(image["bottom"]) * scale_y) + 150,
                    )
                    crop = page_image.crop((left, top, right, bottom))
                    ratio = min(560 / crop.width, 650 / crop.height)
                    crop = crop.resize(
                        (max(1, round(crop.width * ratio)), max(1, round(crop.height * ratio)))
                    )
                    cell = Image.new("RGB", (600, 720), "white")
                    draw = ImageDraw.Draw(cell)
                    placement = placements[placement_index]
                    label = (
                        f"visual {placement_index + 1:02d} | page {page_number} | "
                        f"{placement['width_inches']:.2f} x {placement['height_inches']:.2f} in"
                    )
                    draw.text((16, 14), label, fill="black")
                    cell.paste(crop, ((cell.width - crop.width) // 2, 52))
                    cells.append(cell)
                    placement_index += 1

    if len(cells) != len(placements):
        raise ValueError(
            f"Contact-sheet crops do not match placements: {len(cells)} != {len(placements)}"
        )

    outputs: list[str] = []
    for sheet_index, start in enumerate(range(0, len(cells), 12), start=1):
        batch = cells[start : start + 12]
        sheet = Image.new("RGB", (1800, 2880), "white")
        for index, cell in enumerate(batch):
            sheet.paste(cell, ((index % 3) * 600, (index // 3) * 720))
        path = output_dir / f"visual-placement-contact-{sheet_index:02d}.png"
        sheet.save(path)
        outputs.append(str(path))
    return outputs


def audit_pdf(
    pdf_path: Path,
    render_dir: Path,
    contact_dir: Path,
    visuals: list[dict[str, object]],
) -> dict[str, object]:
    placements: list[dict[str, object]] = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            for image in page.images:
                width = float(image["x1"]) - float(image["x0"])
                height = float(image["bottom"]) - float(image["top"])
                placements.append(
                    {
                        "page": page_number,
                        "width_inches": width / 72,
                        "height_inches": height / 72,
                        "within_page": (
                            float(image["x0"]) >= 0
                            and float(image["x1"]) <= page.width
                            and float(image["top"]) >= 0
                            and float(image["bottom"]) <= page.height
                        ),
                    }
                )

    if len(placements) != len(visuals):
        raise ValueError(f"PDF has {len(placements)} images; expected {len(visuals)}")
    if any(not placement["within_page"] for placement in placements):
        raise ValueError("A PDF image extends outside its page")
    contact_sheets = make_contact_sheets(
        pdf_path,
        render_dir,
        contact_dir,
        placements,
    )
    return {
        "images": len(placements),
        "pages_with_images": len({item["page"] for item in placements}),
        "first_image_page": placements[0]["page"],
        "last_image_page": placements[-1]["page"],
        "min_width_inches": round(min(item["width_inches"] for item in placements), 3),
        "max_width_inches": round(max(item["width_inches"] for item in placements), 3),
        "max_height_inches": round(max(item["height_inches"] for item in placements), 3),
        "contact_sheets": contact_sheets,
        "placements": placements,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manuscript", required=True, type=Path)
    parser.add_argument("--raw-docx", required=True, type=Path)
    parser.add_argument("--template-docx", required=True, type=Path)
    parser.add_argument("--pdf", required=True, type=Path)
    parser.add_argument("--render-dir", required=True, type=Path)
    parser.add_argument("--contact-dir", required=True, type=Path)
    parser.add_argument("--output-json", required=True, type=Path)
    args = parser.parse_args()

    visuals = parse_manuscript_visuals(args.manuscript)
    if len({str(item["relative_path"]) for item in visuals}) != len(visuals):
        raise ValueError("Manuscript visual paths are not unique")

    result = {
        "manuscript_visuals": len(visuals),
        "unique_visual_paths": len(visuals),
        "assets": audit_assets(visuals),
        "docx": audit_docx(args.raw_docx, args.template_docx, visuals),
        "pdf": audit_pdf(args.pdf, args.render_dir, args.contact_dir, visuals),
    }
    payload = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)
    args.output_json.write_text(payload + "\n", encoding="utf-8")
    print(payload)


if __name__ == "__main__":
    main()
