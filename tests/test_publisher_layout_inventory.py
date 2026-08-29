import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from zipfile import ZipFile

import pytest

from docs.publisher.tools import generate_publisher_layout_v2 as layout_v2

ROOT = Path(__file__).resolve().parents[1]
LAYOUT_TOOL = ROOT / "docs/publisher/tools/generate_publisher_layout_v2.py"
LAYOUT_INVENTORY = ROOT / "docs/publisher/ru-publisher-layout-v2-inventory.json"
LAYOUT_LEDGER = ROOT / "docs/publisher/ru-publisher-layout-v2-review-ledger.json"


def test_publisher_layout_generator_is_checked_in() -> None:
    assert LAYOUT_TOOL.is_file()


def test_markdown_parser_ignores_headings_and_listings_inside_fences() -> None:
    manuscript = (
        "## Глава 1\\. Настоящая\n"
        "**Листинг 1. Реальный.**\n"
        "```python\n"
        "## Глава 99\\. Не заголовок\n"
        "**Листинг 42. Не подпись.**\n"
        "``` \t\n"
        "# Заключение. Финал\n"
    )

    parsed = layout_v2.parse_markdown(manuscript)

    assert parsed["headings"] == [
        {
            "id": "heading-chapter-01",
            "kind": "chapter",
            "level": 2,
            "title": "Глава 1. Настоящая",
            "source_line": 1,
        },
        {
            "id": "heading-conclusion",
            "kind": "conclusion",
            "level": 1,
            "title": "Заключение. Финал",
            "source_line": 7,
        },
    ]
    assert parsed["formal_listing_count"] == 1
    assert parsed["code_blocks"] == [
        {
            "index": 1,
            "language": "python",
            "source_line_start": 4,
            "source_line_end": 5,
            "line_count": 2,
            "nearest_formal_listing": {"number": 1, "title": "Реальный"},
        }
    ]


def test_mermaid_metrics_count_implicit_edge_endpoints() -> None:
    assert layout_v2.mermaid_graph_metrics("flowchart LR\nA --> B") == (2, 1)


def test_mermaid_metrics_strip_comments_and_count_explicit_declarations() -> None:
    source = """flowchart LR
%% HiddenA --> HiddenB
A --> B %% HiddenC --> HiddenD
C["Declared node"]
B -.-> C
"""

    assert layout_v2.mermaid_graph_metrics(source) == (3, 2)


def test_hashes_normalize_text_and_canonicalize_json() -> None:
    assert layout_v2.sha256_text("alpha\r\nbeta\rgamma\n") == layout_v2.sha256_text(
        "alpha\nbeta\ngamma\n"
    )
    assert layout_v2.sha256_json({"b": 2, "a": 1}) == layout_v2.sha256_json(
        json.loads('{ "a": 1, "b": 2 }')
    )
    assert layout_v2.canonical_json_bytes({"b": 2, "a": 1}) == (b'{\n  "a": 1,\n  "b": 2\n}\n')


def test_binary_hash_retains_raw_bytes() -> None:
    lf_payload = b"binary\ncontent\n"
    crlf_payload = b"binary\r\ncontent\r\n"

    assert layout_v2.sha256_bytes(lf_payload) == hashlib.sha256(lf_payload).hexdigest()
    assert layout_v2.sha256_bytes(lf_payload) != layout_v2.sha256_bytes(crlf_payload)


def test_docx_placed_sizes_follow_relationship_media_identity(tmp_path: Path) -> None:
    first_image = tmp_path / "first.png"
    second_image = tmp_path / "second.png"
    first_image.write_bytes(b"first-image-payload")
    second_image.write_bytes(b"second-image-payload")
    docx_path = tmp_path / "placements.docx"
    emu = layout_v2.EMU_PER_INCH
    document_xml = f"""\
<w:document xmlns:w="{layout_v2.WORD_NS}"
 xmlns:wp="{layout_v2.DRAWING_NS}"
 xmlns:a="{layout_v2.DRAWINGML_NS}"
 xmlns:r="{layout_v2.OFFICE_REL_NS}">
  <w:body>
    <w:p><w:r><w:drawing>
      <wp:inline><wp:extent cx="{2 * emu}" cy="{3 * emu}"/>
        <a:graphic><a:graphicData><a:blip r:embed="rIdSecond"/></a:graphicData></a:graphic>
      </wp:inline>
    </w:drawing></w:r></w:p>
    <w:p><w:r><w:drawing>
      <wp:inline><wp:extent cx="{4 * emu}" cy="{5 * emu}"/>
        <a:graphic><a:graphicData><a:blip r:embed="rIdFirst"/></a:graphicData></a:graphic>
      </wp:inline>
    </w:drawing></w:r></w:p>
  </w:body>
</w:document>
"""
    relationships_xml = f"""\
<Relationships xmlns="{layout_v2.PACKAGE_REL_NS}">
  <Relationship Id="rIdFirst" Type="{layout_v2.OFFICE_REL_NS}/image"
    Target="media/image1.png"/>
  <Relationship Id="rIdSecond" Type="{layout_v2.OFFICE_REL_NS}/image"
    Target="media/image2.png"/>
</Relationships>
"""
    with ZipFile(docx_path, "w") as archive:
        archive.writestr("word/document.xml", document_xml)
        archive.writestr("word/_rels/document.xml.rels", relationships_xml)
        archive.writestr("word/media/image1.png", first_image.read_bytes())
        archive.writestr("word/media/image2.png", second_image.read_bytes())

    sizes = layout_v2.docx_placed_image_sizes(docx_path, [first_image, second_image])

    assert sizes == {
        "first.png": {"width": 4.0, "height": 5.0},
        "second.png": {"width": 2.0, "height": 3.0},
    }


def sample_inventory() -> dict[str, object]:
    return {
        "diagrams": [{"id": "diagram-01"}],
        "code_blocks": [{"id": "code-block-001"}],
        "headings": [{"id": "heading-chapter-01"}],
    }


def reviewed_ledger(
    status: str = "pass",
) -> tuple[dict[str, object], layout_v2.ReviewLedger]:
    inventory = sample_inventory()
    ledger = layout_v2.build_review_ledger(inventory, fresh=True)
    entry = ledger["entries"][0]
    entry.update(
        {
            "status": status,
            "severity": None if status == "pass" else "major",
            "notes": "Checked at final placement" if status == "pass" else "Text overlaps edge",
            "reviewed_by": "layout-editor",
            "reviewed_at": "2026-08-30T12:00:00Z",
            "evidence_refs": ["render:template2000n:page-12"],
        }
    )
    return inventory, ledger


def test_fresh_ledger_uses_generator_defaults() -> None:
    inventory = sample_inventory()

    ledger = layout_v2.build_review_ledger(inventory, fresh=True)

    assert ledger["entries"] == [
        {
            "id": "review-diagram-01",
            "inventory_id": "diagram-01",
            "item_type": "diagram",
            "status": "pending",
            "severity": None,
            "notes": "",
        },
        {
            "id": "review-code-block-001",
            "inventory_id": "code-block-001",
            "item_type": "code_block",
            "status": "pending",
            "severity": None,
            "notes": "",
        },
        {
            "id": "review-heading-chapter-01",
            "inventory_id": "heading-chapter-01",
            "item_type": "heading",
            "status": "pending",
            "severity": None,
            "notes": "",
        },
    ]


@pytest.mark.parametrize("status", ["pass", "fail"])
def test_ledger_validation_allows_review_progress(status: str) -> None:
    inventory, ledger = reviewed_ledger(status)

    layout_v2.validate_review_ledger(inventory, ledger)


def test_ledger_validation_requires_one_entry_per_inventory_item() -> None:
    inventory = sample_inventory()
    ledger = layout_v2.build_review_ledger(inventory, fresh=True)
    ledger["entries"].append(copy.deepcopy(ledger["entries"][0]))

    with pytest.raises(ValueError, match="exactly one review entry"):
        layout_v2.validate_review_ledger(inventory, ledger)


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("status", "done", "status"),
        ("status", [], "status"),
        ("severity", "critical", "severity"),
        ("severity", [], "severity"),
        ("notes", [], "notes"),
    ],
)
def test_ledger_validation_rejects_invalid_review_fields(
    field: str, value: object, message: str
) -> None:
    inventory, ledger = reviewed_ledger()
    ledger["entries"][0][field] = value

    with pytest.raises(ValueError, match=message):
        layout_v2.validate_review_ledger(inventory, ledger)


def test_ledger_validation_requires_completed_review_evidence() -> None:
    inventory = sample_inventory()
    ledger = layout_v2.build_review_ledger(inventory, fresh=True)
    ledger["entries"][0].update({"status": "pass", "severity": None})

    with pytest.raises(ValueError, match="reviewed_by"):
        layout_v2.validate_review_ledger(inventory, ledger)


def test_normal_regeneration_preserves_review_progress() -> None:
    inventory, ledger = reviewed_ledger()

    regenerated = layout_v2.build_review_ledger(inventory, existing_ledger=ledger)
    reset = layout_v2.build_review_ledger(inventory, existing_ledger=ledger, fresh=True)

    assert regenerated["entries"][0] == ledger["entries"][0]
    assert reset["entries"][0] == {
        "id": "review-diagram-01",
        "inventory_id": "diagram-01",
        "item_type": "diagram",
        "status": "pending",
        "severity": None,
        "notes": "",
    }


def test_generated_inventory_preserves_all_frozen_facts() -> None:
    committed = json.loads(LAYOUT_INVENTORY.read_text(encoding="utf-8"))

    generated = layout_v2.build_inventory(ROOT)

    assert generated == committed
    assert generated["counts"] == {
        "parts": 8,
        "chapters": 28,
        "appendices": 5,
        "formal_listings": 37,
        "fenced_code_blocks": 141,
        "manuscript_images": 57,
        "mermaid_diagrams": 56,
        "inline_diagrams": 29,
        "numbered_diagrams": 25,
        "editorial_diagrams": 2,
        "reader_facing_headings": 43,
    }


def test_publisher_layout_generator_check_matches_committed_json() -> None:
    completed = subprocess.run(
        [sys.executable, str(LAYOUT_TOOL), "--check"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert LAYOUT_INVENTORY.read_bytes() == layout_v2.canonical_json_bytes(
        json.loads(LAYOUT_INVENTORY.read_text(encoding="utf-8"))
    )
    assert LAYOUT_LEDGER.read_bytes() == layout_v2.canonical_json_bytes(
        json.loads(LAYOUT_LEDGER.read_text(encoding="utf-8"))
    )
