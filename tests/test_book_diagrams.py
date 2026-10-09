"""Publication guards for editable, localized book diagrams."""

import hashlib
import json
import math
import re
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs/assets/diagrams/manifest.json"
ROWS = json.loads(MANIFEST.read_text())["diagrams"]


def _assert_unoccluded_labels(elements):
    for index, backing in enumerate(elements):
        if backing.get("customData", {}).get("sourceKind") != "label-backing":
            continue
        for text in elements[:index]:
            if text["type"] != "text":
                continue
            overlaps = max(backing["x"], text["x"]) < min(
                backing["x"] + backing["width"], text["x"] + text["width"]
            ) and max(backing["y"], text["y"]) < min(
                backing["y"] + backing["height"], text["y"] + text["height"]
            )
            assert not overlaps, f"Backing {backing['id']} hides text {text['id']}"


def test_all_localizations_have_the_same_diagram_inventory():
    groups = {lang: set() for lang in ("ru", "en", "zh")}
    for row in ROWS:
        groups[row["language"]].add(row["id"].split("-", 1)[1])
    assert groups["ru"] == groups["en"] == groups["zh"]
    assert len(ROWS) == len({row["id"] for row in ROWS})
    assert len(groups["ru"]) >= 29


def test_no_mermaid_fences_or_external_mermaid_runtime_remain():
    for page in (ROOT / "docs").rglob("*.md"):
        assert not re.search(r"^```\s*mermaid\b", page.read_text(), re.MULTILINE), page
    assert "mermaid-init" not in (ROOT / "mkdocs.yml").read_text()


@pytest.mark.parametrize("row", ROWS, ids=lambda row: row["id"])
def test_scene_and_export_are_complete_and_linked(row):
    scene_path, svg_path = ROOT / row["scene"], ROOT / row["svg"]
    assert hashlib.sha256(scene_path.read_bytes()).hexdigest() == row["sceneSha256"]
    assert hashlib.sha256(svg_path.read_bytes()).hexdigest() == row["svgSha256"]
    scene = json.loads(scene_path.read_text())
    assert scene["type"] == "excalidraw"
    assert scene["version"] == 2
    elements = [e for e in scene["elements"] if not e.get("isDeleted")]
    ids = {e["id"] for e in elements}
    assert len(ids) == len(elements)
    counts = Counter(e["type"] for e in elements)
    assert counts["image"] == 0
    assert counts["text"] == row["labels"] > 0
    assert counts["arrow"] == row["arrows"] > 0
    assert scene.get("files", {}) == {}
    for element in elements:
        assert all(math.isfinite(element[k]) for k in ("x", "y", "width", "height"))
        for key in ("startBinding", "endBinding"):
            if element.get(key):
                assert element[key]["elementId"] in ids
    _assert_unoccluded_labels(elements)
    svg = ET.fromstring(svg_path.read_bytes())
    svg_text = " ".join(svg.itertext())
    assert not list(svg.iter("{http://www.w3.org/2000/svg}image"))
    assert not list(svg.iter("{http://www.w3.org/2000/svg}script"))
    for element in elements:
        if element["type"] == "text":
            for line in element["text"].splitlines():
                assert line in svg_text
    page = (ROOT / row["page"]).read_text()
    assert scene_path.name in page
    assert svg_path.name in page
    assert f"<!-- excalidraw:{row['id']} -->" in page


def test_every_scene_is_in_the_manifest():
    actual = {
        str(p.relative_to(ROOT)) for p in (ROOT / "docs/assets/diagrams").rglob("*.excalidraw")
    }
    assert actual == {row["scene"] for row in ROWS}
