#!/usr/bin/env python3
"""Collect simple render QA metrics from DOCX page PNGs."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from PIL import Image, ImageChops, ImageStat


PAGE_RE = re.compile(r"page-(\d+)\.png$")


def page_number(path: Path) -> int:
    match = PAGE_RE.search(path.name)
    if not match:
        raise ValueError(f"Unexpected page image name: {path.name}")
    return int(match.group(1))


def density(path: Path) -> float:
    image = Image.open(path).convert("RGB")
    white = Image.new("RGB", image.size, (255, 255, 255))
    diff = ImageChops.difference(image, white).convert("L")
    stat = ImageStat.Stat(diff)
    return float(stat.mean[0]) / 255.0


def make_contact_sheet(paths: list[Path], output: Path, thumb_width: int = 320) -> None:
    thumbs: list[Image.Image] = []
    for path in paths:
        image = Image.open(path).convert("RGB")
        ratio = thumb_width / image.width
        thumb = image.resize((thumb_width, int(image.height * ratio)))
        thumbs.append(thumb)

    cols = min(4, len(thumbs)) or 1
    rows = (len(thumbs) + cols - 1) // cols
    cell_h = max((thumb.height for thumb in thumbs), default=1) + 32
    sheet = Image.new("RGB", (cols * thumb_width, rows * cell_h), "white")

    for idx, (path, thumb) in enumerate(zip(paths, thumbs, strict=True)):
        x = (idx % cols) * thumb_width
        y = (idx // cols) * cell_h
        sheet.paste(thumb, (x, y + 32))
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output)


def collect(render_dir: Path, contact_sheet: Path | None) -> dict[str, object]:
    pages = sorted(render_dir.glob("page-*.png"), key=page_number)
    scored = [(page_number(path), density(path), path) for path in pages]
    blank_like = [page for page, score, _ in scored if score < 0.0005]
    lowest = sorted(scored, key=lambda item: item[1])[:10]

    selected_numbers = []
    if scored:
        selected_numbers.extend([1, scored[-1][0]])
    selected_numbers.extend(page for page, _, _ in lowest)
    selected_numbers = list(dict.fromkeys(selected_numbers))
    selected_paths = [path for page, _, path in scored if page in selected_numbers]
    if contact_sheet is not None:
        make_contact_sheet(selected_paths, contact_sheet)

    return {
        "render_dir": str(render_dir),
        "pages": len(pages),
        "blank_like_pages": blank_like,
        "lowest_density_pages": [
            {"page": page, "density": score} for page, score, _ in lowest
        ],
        "contact_sheet": str(contact_sheet) if contact_sheet is not None else None,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("render_dir", type=Path)
    parser.add_argument("--contact-sheet", type=Path)
    parser.add_argument("--output-json", type=Path)
    args = parser.parse_args()

    metrics = collect(args.render_dir, args.contact_sheet)
    payload = json.dumps(metrics, ensure_ascii=False, indent=2, sort_keys=True)
    if args.output_json:
        args.output_json.write_text(payload + "\n", encoding="utf-8")
    print(payload)


if __name__ == "__main__":
    main()
