from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "docs/publisher/tools/prepare_diagram_review_evidence.py"
SPEC = importlib.util.spec_from_file_location("prepare_diagram_review_evidence", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
evidence = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(evidence)


def renderer_report(count: int = 7) -> dict[str, object]:
    return {
        "violations": [],
        "results": [
            {
                "filename": f"diagram-{index:02d}.png",
                "source_sha256": f"{index:064x}",
                "svg_sha256": f"{index + 1:064x}",
                "png_sha256": f"{index + 2:064x}",
                "effective_font_pt": 10.0,
                "viewbox_aspect_ratio": 1.5,
                "aspect_ratio_override": None,
                "violations": [],
            }
            for index in range(1, count + 1)
        ],
    }


def test_standalone_review_never_claims_docx_placement() -> None:
    report = renderer_report(2)

    review = evidence.standalone_review("3B1", report, "Reviewer", "2026-08-30")

    assert review["status"] == "standalone_pass"
    assert review["preview_placement"] == "pending_task_7"
    assert review["final_publisher_placement"] == "pending_task_7"
    assert "placements" not in review
    assert "rendered_pages" not in review
    assert all(
        item["gates"]["preview_placement"] == "pending"
        for item in review["asset_reviews"]
    )
    assert all(item["aspect_ratio_override"] is None for item in review["asset_reviews"])


def test_standalone_review_preserves_documented_aspect_override() -> None:
    report = renderer_report(1)
    override = {
        "reviewed_by": "Independent reviewer",
        "reviewed_on": "2026-08-30",
        "reason": "Intentional full-height portrait workflow.",
    }
    report["results"][0]["aspect_ratio_override"] = override

    review = evidence.standalone_review("3B1", report, "Reviewer", "2026-08-30")

    assert review["asset_reviews"][0]["aspect_ratio_override"] == override


@pytest.mark.parametrize(("reviewer", "reviewed_on"), [("", "2026-08-30"), ("R", "30-08-2026")])
def test_standalone_review_rejects_invalid_review_metadata(
    reviewer: str,
    reviewed_on: str,
) -> None:
    with pytest.raises(ValueError):
        evidence.standalone_review("3B1", renderer_report(1), reviewer, reviewed_on)


def test_contact_sheet_geometry_is_fixed_and_paginated(tmp_path: Path) -> None:
    report = renderer_report(7)
    visuals = tmp_path / "visuals"
    output = tmp_path / "review"
    visuals.mkdir()
    output.mkdir()
    for result in report["results"]:
        Image.new("RGB", (640, 360), "white").save(visuals / result["filename"])

    paths = evidence.make_contact_sheets(report, visuals, output, grayscale=False)

    assert [path.name for path in paths] == ["contact-sheet-01.png", "contact-sheet-02.png"]
    assert all(Image.open(path).size == (4200, 3900) for path in paths)
