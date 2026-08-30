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


def test_docx_baseline_placements_use_alt_text_and_report_payload_sync(tmp_path: Path) -> None:
    first_image = tmp_path / "first.png"
    second_image = tmp_path / "second.png"
    first_image.write_bytes(b"first-image-payload")
    second_image.write_bytes(b"current-second-image-payload")
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
        <wp:docPr id="1" name="second.png" descr="Second diagram"/>
        <a:graphic><a:graphicData><a:blip r:embed="rIdSecond"/></a:graphicData></a:graphic>
      </wp:inline>
    </w:drawing></w:r></w:p>
    <w:p><w:r><w:drawing>
      <wp:inline><wp:extent cx="{4 * emu}" cy="{5 * emu}"/>
        <wp:docPr id="2" name="first.png" descr="First diagram"/>
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
        archive.writestr("word/media/image2.png", b"baseline-second-image-payload")

    placements = layout_v2.docx_baseline_image_placements(
        docx_path,
        {
            "First diagram": first_image,
            "Second diagram": second_image,
        },
    )

    assert placements == {
        "first.png": {
            "size_inches": {"width": 4.0, "height": 5.0},
            "payload_match": True,
            "artifact_sync_status": "synchronized",
        },
        "second.png": {
            "size_inches": {"width": 2.0, "height": 3.0},
            "payload_match": False,
            "artifact_sync_status": "pending",
        },
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
            "evidence_refs": [
                {
                    "kind": "render",
                    "path": "docs/publisher/qa/layout-v2/example.json",
                    "sha256": "a" * 64,
                }
            ],
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


def test_ledger_rejects_overall_pass_while_any_gate_is_pending() -> None:
    inventory, ledger = reviewed_ledger()
    ledger["entries"][0]["gate_statuses"] = {
        "source": "pass",
        "standalone_render": "pass",
        "preview_placement": "pass",
        "final_publisher_placement": "pending",
    }

    with pytest.raises(ValueError, match="cannot pass while review gates are incomplete"):
        layout_v2.validate_review_ledger(inventory, ledger)


def test_review_progress_comes_from_an_independent_update_not_the_generated_ledger() -> None:
    inventory, reviewed = reviewed_ledger()
    review_updates = {"diagram-01": reviewed["entries"][0]}

    regenerated = layout_v2.build_review_ledger(inventory, review_updates=review_updates)
    reset = layout_v2.build_review_ledger(
        inventory,
        review_updates=review_updates,
        fresh=True,
    )

    assert regenerated["entries"][0] == reviewed["entries"][0]
    assert reset["entries"][0] == {
        "id": "review-diagram-01",
        "inventory_id": "diagram-01",
        "item_type": "diagram",
        "status": "pending",
        "severity": None,
        "notes": "",
    }


def test_build_outputs_never_reads_inventory_or_ledger_as_generator_inputs(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    generated_outputs = {LAYOUT_INVENTORY.resolve(), LAYOUT_LEDGER.resolve()}
    original_load_json = layout_v2._load_json

    def guarded_load_json(path: Path) -> object:
        assert path.resolve() not in generated_outputs
        return original_load_json(path)

    monkeypatch.setattr(layout_v2, "_load_json", guarded_load_json)

    outputs = layout_v2.build_outputs(ROOT, review_updates={})

    assert set(outputs) == {LAYOUT_INVENTORY, LAYOUT_LEDGER}


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

    task_3a_filenames = {
        "ru-figure-01-book-map.png",
        "ru-figure-03-reference-architecture.png",
        "ru-figure-04-capability-contract-path.png",
        "ru-inline-diagram-01.png",
        "ru-inline-diagram-03.png",
    }
    for diagram in generated["diagrams"]:
        assert "current_placed_size_inches" not in diagram
        placements = diagram["baseline_docx_placements"]
        assert set(placements) == {
            "google-doc-book-standards",
            "template2000n-book-standards",
        }
        expected_payload_match = diagram["filename"] not in task_3a_filenames
        for placement in placements.values():
            assert placement["payload_match"] is expected_payload_match
            assert placement["artifact_sync_status"] == (
                "synchronized" if expected_payload_match else "pending"
            )
            assert placement["size_inches"]["width"] > 0
            assert placement["size_inches"]["height"] > 0


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
