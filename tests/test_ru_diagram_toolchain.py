import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PUBLISHER_PACKAGE = ROOT / "docs/publisher/package.json"
PUBLISHER_LOCK = ROOT / "docs/publisher/package-lock.json"
COVERAGE_WORKFLOW = ROOT / ".github/workflows/coverage.yml"


def test_publisher_node_toolchain_is_exactly_pinned() -> None:
    package = json.loads(PUBLISHER_PACKAGE.read_text(encoding="utf-8"))
    lock = json.loads(PUBLISHER_LOCK.read_text(encoding="utf-8"))

    assert package["private"] is True
    assert package["engines"] == {"node": ">=20"}
    assert package["devDependencies"] == {
        "mermaid": "11.17.2",
        "playwright": "1.62.1",
        "sharp": "0.35.4",
    }
    assert package["scripts"] == {
        "test": "npm run test:unit && npm run test:e2e",
        "test:unit": "node --test ../../tests/test_ru_diagram_renderer_contract.mjs",
        "test:e2e": (
            "node --test ../../tests/test_ru_diagram_renderer_e2e.mjs "
            "../../tests/test_ru_diagram_svg_geometry_e2e.mjs"
        ),
    }
    assert lock["lockfileVersion"] == 3
    assert lock["packages"][""]["engines"] == {"node": ">=20"}
    assert lock["packages"][""]["devDependencies"] == package["devDependencies"]
    for dependency, version in package["devDependencies"].items():
        assert lock["packages"][f"node_modules/{dependency}"]["version"] == version


def test_ci_runs_publisher_node_contract_and_browser_tests_without_skipping() -> None:
    workflow = yaml.safe_load(COVERAGE_WORKFLOW.read_text(encoding="utf-8"))
    trigger = workflow[True]
    job = workflow["jobs"]["publisher-diagram-renderer"]
    steps = job["steps"]

    assert trigger["pull_request"]["paths"] == [
        ".github/workflows/coverage.yml",
        "docs/publisher/package.json",
        "docs/publisher/package-lock.json",
        "docs/publisher/tools/ru_diagram_renderer_contract.mjs",
        "docs/publisher/tools/ru_diagram_svg_geometry.mjs",
        "docs/publisher/tools/render_ru_inline_diagrams.mjs",
        "tests/fixtures/ru_diagram_renderer/**",
        "tests/ru_diagram_renderer_e2e_harness.mjs",
        "tests/ru_diagram_test_environment.mjs",
        "tests/test_ru_diagram_renderer_*.mjs",
        "tests/test_ru_diagram_svg_geometry_e2e.mjs",
    ]
    assert job["runs-on"] == "ubuntu-latest"
    assert job["timeout-minutes"] == 20
    assert {
        "name": "Setup Node",
        "uses": "actions/setup-node@v6.5.0",
        "with": {
            "node-version": "20.19.5",
            "cache": "npm",
            "cache-dependency-path": "docs/publisher/package-lock.json",
        },
    } in steps
    assert {
        "name": "Install publisher Node dependencies",
        "run": ("npm ci --prefix docs/publisher"),
    } in steps
    assert {
        "name": "Install Chromium",
        "run": ("npm exec --prefix docs/publisher -- playwright install --with-deps chromium"),
    } in steps
    assert {
        "name": "Run publisher Node and browser tests",
        "run": ("npm test --prefix docs/publisher"),
    } in steps
