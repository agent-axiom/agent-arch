import json
import re
import shutil
import subprocess
import textwrap
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]


class MkDocsConfigLoader(yaml.SafeLoader):
    pass


def _construct_python_name(loader: yaml.SafeLoader, node: yaml.Node) -> str:
    return loader.construct_scalar(node)


MkDocsConfigLoader.add_multi_constructor(
    "tag:yaml.org,2002:python/name:",
    lambda loader, _suffix, node: _construct_python_name(loader, node),
)


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def _load_mkdocs_config() -> dict:
    return yaml.load(_read("mkdocs.yml"), Loader=MkDocsConfigLoader)


def _assert_files_contain_all(paths: tuple[str, ...], expected: tuple[str, ...]) -> None:
    for path in paths:
        text = _read(path)
        for item in expected:
            assert item in text, (path, item)


def test_all_book_chapters_carry_case_spine_markers() -> None:
    chapter_paths = sorted(Path("docs/book").glob("part-*/chapter-*.md"))

    assert chapter_paths

    missing = []
    for path in chapter_paths:
        text = _read(str(path))
        if "case-spine" not in text.lower() and "case spine" not in text.lower():
            missing.append(str(path))

    assert missing == []


def test_all_appendix_pages_carry_canonical_case_markers() -> None:
    appendix_paths = sorted(Path("docs/appendix").glob("*.md"))

    assert appendix_paths

    missing = []
    for path in appendix_paths:
        text = _read(str(path))
        if "Canonical " not in text:
            missing.append(str(path))

    assert missing == []


def test_all_book_part_indexes_surface_three_canonical_cases() -> None:
    part_index_paths = sorted(Path("docs/book").glob("part-*/index*.md"))
    required_markers = (
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
    )

    assert part_index_paths

    missing = []
    for path in part_index_paths:
        text = _read(str(path))
        absent = [marker for marker in required_markers if marker not in text]
        if absent:
            missing.append((str(path), absent))

    assert missing == []


def test_public_markdown_do_not_use_deprecated_canonical_case_labels() -> None:
    doc_paths = sorted(Path("docs").glob("**/*.md")) + sorted(Path(".").glob("README*.md"))
    deprecated_markers = (
        "Support Triage Agent",
        "Internal Knowledge Agent",
        "Incident Coordination Agent",
        "Support Triage",
        "Internal Knowledge",
        "Incident Coordination",
        "Internal enterprise knowledge assistant",
        "Approval-bound high-risk action agent",
        "support triage, internal knowledge, incident coordination",
    )

    assert doc_paths

    hits = []
    for path in doc_paths:
        text = _read(str(path))
        found = [marker for marker in deprecated_markers if marker in text]
        if found:
            hits.append((str(path), found))

    assert hits == []


def test_public_markdown_do_not_use_stale_publisher_packet_labels() -> None:
    doc_paths = sorted(Path("docs").glob("**/*.md")) + sorted(Path(".").glob("README*.md"))
    deprecated_markers = (
        "publisher-ready TOC",
        "Publisher-Ready TOC",
        "publisher-ready table of contents",
        "publisher-ready table-of-contents",
    )

    assert doc_paths

    hits = []
    for path in doc_paths:
        text = _read(str(path))
        found = [marker for marker in deprecated_markers if marker in text]
        if found:
            hits.append((str(path), found))

    assert hits == []


def test_public_book_canonical_redirects_are_configured() -> None:
    mkdocs_config = _load_mkdocs_config()
    scripts = mkdocs_config["extra_javascript"]

    assert "javascripts/canonical-redirects.js" in scripts

    redirect_script = _read("docs/javascripts/canonical-redirects.js")
    for route in (
        '"/book"',
        '"/en/book"',
        '"/zh/book"',
        '"/start-here"',
        '"/reference"',
        '"/appendix/sources"',
        '"/book/part-i/chapter-1"',
        '"/book/part-v/chapter-13"',
    ):
        assert route in redirect_script
    assert 'projectPrefix = "/agent-arch"' in redirect_script


def _canonical_redirects_for(pathname: str, search: str = "", hash_: str = "") -> list[str]:
    node = shutil.which("node")
    if node is None:
        raise pytest.skip.Exception("node is required to execute canonical-redirects.js")

    redirect_script = _read("docs/javascripts/canonical-redirects.js")
    harness = f"""
    const redirects = [];
    const location = {{
      origin: "https://agent-axiom.github.io",
      pathname: {json.dumps(pathname)},
      search: {json.dumps(search)},
      hash: {json.dumps(hash_)},
      get href() {{
        return this.origin + this.pathname + this.search + this.hash;
      }},
      replace(url) {{
        redirects.push(url);
      }}
    }};
    global.window = {{ location }};
    {redirect_script}
    process.stdout.write(JSON.stringify(redirects));
    """
    result = subprocess.run(
        [node, "-e", textwrap.dedent(harness)],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def test_public_book_canonical_redirects_do_not_reload_current_canonical_urls() -> None:
    assert _canonical_redirects_for("/agent-arch/book/") == []
    assert _canonical_redirects_for("/agent-arch/en/book/") == []
    assert _canonical_redirects_for("/agent-arch/zh/book/") == []


def test_public_book_canonical_redirects_add_trailing_slash_to_entrypoints() -> None:
    assert _canonical_redirects_for("/agent-arch/book", "?tab=toc", "#intro") == [
        "https://agent-axiom.github.io/agent-arch/book/?tab=toc#intro"
    ]
    assert _canonical_redirects_for("/agent-arch/reference", "?view=schemas", "#top") == [
        "https://agent-axiom.github.io/agent-arch/reference/?view=schemas#top"
    ]
    assert _canonical_redirects_for("/agent-arch/appendix/sources") == [
        "https://agent-axiom.github.io/agent-arch/appendix/sources/"
    ]
    assert _canonical_redirects_for("/agent-arch/book/part-i/chapter-1") == [
        "https://agent-axiom.github.io/agent-arch/book/part-i/chapter-1/"
    ]
    assert _canonical_redirects_for("/agent-arch/book/part-v/chapter-13") == [
        "https://agent-axiom.github.io/agent-arch/book/part-v/chapter-13/"
    ]


def test_public_book_extensionless_fallback_redirect_pages_exist() -> None:
    expected_pages = {
        "docs/book.html": ("ru", "book/"),
        "docs/en/book.html": ("en", "book/"),
        "docs/zh/book.html": ("zh", "book/"),
        "docs/start-here.html": ("ru", "start-here/"),
        "docs/reference.html": ("ru", "reference/"),
        "docs/appendix/sources.html": ("ru", "sources/"),
        "docs/book/part-i/chapter-1.html": ("ru", "chapter-1/"),
        "docs/book/part-v/chapter-13.html": ("ru", "chapter-13/"),
    }

    for page_path, (language, target) in expected_pages.items():
        page = _read(page_path)
        assert f'<html lang="{language}">' in page
        assert f'content="0; url={target}"' in page
        assert f'<link rel="canonical" href="{target}">' in page
        assert "window.location.replace" in page
        assert "window.location.search + window.location.hash" in page


def test_translated_markdown_pages_have_no_cyrillic_residue() -> None:
    translated_paths = sorted((ROOT / "docs").rglob("*.en.md")) + sorted(
        (ROOT / "docs").rglob("*.zh.md")
    )

    assert translated_paths

    leaked_lines = []
    for path in translated_paths:
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if re.search(r"[А-Яа-яЁё]", line):
                leaked_lines.append((str(path.relative_to(ROOT)), line_number, line.strip()))

    assert leaked_lines == []


def test_translated_navigation_values_have_no_cyrillic_residue() -> None:
    mkdocs_config = _load_mkdocs_config()
    locales = {}
    for plugin in mkdocs_config["plugins"]:
        if isinstance(plugin, dict) and "i18n" in plugin:
            locales = {language["locale"]: language for language in plugin["i18n"]["languages"]}
            break

    leaked_values = []
    for locale in ("en", "zh"):
        for target in locales[locale]["nav_translations"].values():
            if re.search(r"[А-Яа-яЁё]", str(target)):
                leaked_values.append((locale, target))

    assert leaked_values == []


def test_translated_navigation_has_no_known_russian_leaks() -> None:
    mkdocs_config = _load_mkdocs_config()
    locales = {}
    for plugin in mkdocs_config["plugins"]:
        if isinstance(plugin, dict) and "i18n" in plugin:
            locales = {language["locale"]: language for language in plugin["i18n"]["languages"]}
            break

    forbidden = (
        "Глава 24",
        "Глава 25",
        "Глава 26",
        "Глава 27",
        "План интеграции идей Google",
        "Схема ",
    )
    for locale in ("en", "zh"):
        nav_targets = locales[locale]["nav_translations"].values()
        for target in nav_targets:
            assert all(fragment not in str(target) for fragment in forbidden), (locale, target)


def test_part_viii_role_map_is_present_in_all_languages() -> None:
    expected_by_file = {
        "docs/book/part-viii/index.md": (
            "Карта ролей этой части",
            "Lifecycle frame",
            "Change management",
            "Assurance",
            "Provenance",
            "Retirement",
            "Misalignment и insider risk",
            "Behavioral/control evals",
            "Observability",
            "Inventory и registry",
        ),
        "docs/book/part-viii/index.en.md": (
            "Role Map for This Part",
            "Lifecycle frame",
            "Change management",
            "Assurance",
            "Provenance",
            "Retirement",
            "Misalignment and insider risk",
            "Behavioral/control evals",
            "Observability",
            "Inventory and registry",
        ),
        "docs/book/part-viii/index.zh.md": (
            "这一部分的角色地图",
            "生命周期框架",
            "变更管理",
            "保障闭环",
            "来源追踪",
            "退役",
            "失配与内部人风险",
            "行为/控制评测",
            "可观测性",
            "清单与注册表",
        ),
    }

    for relative_path, markers in expected_by_file.items():
        text = _read(relative_path)
        missing = [marker for marker in markers if marker not in text]
        assert not missing, f"{relative_path} missing role-map markers: {missing}"


def test_part_viii_role_map_links_schema_backed_artifacts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/index.md": (
            "[Change packet](../../appendix/change-rollout-schema.md)",
            "[Finding and response record](../../appendix/incident-record-schema.md)",
            "[Approved artifact bundle]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[Retirement plan](../../appendix/lifecycle-artifact-schema.md)",
            "[Eval gate and verifier contract](../../appendix/eval-schema.md)",
            "[Trace and telemetry coverage record]"
            "(../../appendix/trace-schema.md)",
            "[Registry record](../../appendix/registry-operations-handbook.md)",
        ),
        "docs/book/part-viii/index.en.md": (
            "[Change packet](../../appendix/change-rollout-schema.en.md)",
            "[Finding and response record]"
            "(../../appendix/incident-record-schema.en.md)",
            "[Approved artifact bundle]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[Retirement plan](../../appendix/lifecycle-artifact-schema.en.md)",
            "[Eval gate and verifier contract](../../appendix/eval-schema.en.md)",
            "[Trace and telemetry coverage record]"
            "(../../appendix/trace-schema.en.md)",
            "[Registry record]"
            "(../../appendix/registry-operations-handbook.en.md)",
        ),
        "docs/book/part-viii/index.zh.md": (
            "[变更包](../../appendix/change-rollout-schema.zh.md)",
            "[Finding 与响应记录]"
            "(../../appendix/incident-record-schema.zh.md)",
            "[已批准工件包]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[退役计划](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[Eval gate 与 verifier contract](../../appendix/eval-schema.zh.md)",
            "[Trace 与 telemetry 覆盖记录]"
            "(../../appendix/trace-schema.zh.md)",
            "[Registry record]"
            "(../../appendix/registry-operations-handbook.zh.md)",
        ),
    }

    for relative_path, expected_snippets in expected_snippets_by_file.items():
        text = _read(relative_path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (relative_path, expected_snippet)


def test_part_viii_role_map_is_print_friendly() -> None:
    role_map_markers = {
        "docs/book/part-viii/index.md": "## В этой части",
        "docs/book/part-viii/index.en.md": "## In This Part",
        "docs/book/part-viii/index.zh.md": "## 本部分内容",
    }

    for relative_path, next_heading in role_map_markers.items():
        text = _read(relative_path)
        role_map = text.split("##", 2)[2].split(next_heading, 1)[0]
        assert "|" not in role_map, relative_path
        assert "print-friendly" in role_map.lower(), relative_path
        assert role_map.count("- **") >= 9, relative_path


def test_book_improvement_blueprint_records_review_remediation_status() -> None:
    required_markers = (
        "Implementation status, 20 May 2026",
        "P0:",
        "P1:",
        "P2:",
        "P3:",
        "draft-localization status",
        "MCP threat model",
        "trace schema",
        "eval schema",
        "memory/retrieval schema",
        "three canonical case spines",
        "print-friendly",
        "publisher packet is drafted and internally gated",
        "packet TOC section",
        "20 May 2026 public-link record",
        "Still blocked before external submission",
    )

    _assert_files_contain_all(("docs/book-improvement-blueprint.md",), required_markers)
    text = _read("docs/book-improvement-blueprint.md")
    assert "publisher-ready TOC" not in text
    assert "publisher-ready table of contents" not in text


def test_publisher_packet_has_core_positioning_and_companion_boundary() -> None:
    required_markers = (
        "Publisher Packet Draft",
        "Positioning",
        "One-Page Positioning Memo Draft",
        "Print Manuscript Shape",
        "Online Companion Boundary",
        "- **Working title:** Secure AI Agent Architecture.",
        "**Subtitle:** From prompt demos to governed production systems.",
        "**Primary reader:**",
        "**Unique promise:**",
        "**Companion assets:**",
        (
            "keep schemas, runtime command details, long checklists, and source catalogs "
            "in the online companion."
        ),
        "runnable `agent_runtime_ref` package",
        "command-output field lists and validation-error catalogs",
        "print sample that depends on live site navigation",
    )

    _assert_files_contain_all(("docs/publisher-ready-toc.md",), required_markers)


def test_publisher_packet_positioning_memo_is_print_friendly() -> None:
    text = _read("docs/publisher-ready-toc.md")
    opening_section = text.split("## Positioning", 1)[0]
    positioning_section = text.split("## Positioning", 1)[1].split(
        "## Print Manuscript Shape",
        1,
    )[0]
    required_opening_markers = (
        "- keep the book-shaped manuscript, sample strategy, positioning, and cover note together;",
        "- keep the comparable shelf and companion links in the same packet artifact.",
    )
    forbidden_inline_markers = (
        "Purpose: keep publisher-facing packet notes separate",
        (
            "keep the book-shaped manuscript, sample strategy, positioning, "
            "cover note, comparable shelf"
        ),
        "Reader: senior product engineers",
        "senior product engineers, platform engineers, security engineers, staff engineers",
        "Promise: explain how to move from prompt demos",
        "**Primary reader:** platform and product architects",
        (
            "systems that can read private context, call tools, request approvals, "
            "write to external systems"
        ),
        "**Problem:** most teams can build",
        "**Unique promise:** the book treats agents as production systems:",
        "**Competing shelf:** cloud architecture",
        "**Manuscript status:** public open manuscript",
        "**Companion assets:** reference runtime",
    )

    for marker in required_opening_markers:
        assert marker in opening_section
    for marker in forbidden_inline_markers:
        assert marker not in opening_section
        assert marker not in positioning_section
    assert opening_section.count("\n- ") >= 4
    assert (
        "- **Reader:** senior product engineers, platform engineers, and security engineers."
        in positioning_section
    )
    assert "- **Reader extension:** staff engineers and technical leads." in positioning_section
    assert (
        "- systems that can read private context, call tools, and request approvals;"
        in positioning_section
    )
    assert (
        "- systems that can write to external systems and survive incidents."
        in positioning_section
    )
    assert (
        "- those workflows now carry real permissions and long-running state;"
        in positioning_section
    )
    assert (
        "- they also carry delegated work and regulated evidence needs."
        in positioning_section
    )
    assert (
        "- those workflows now carry real permissions, long-running state, delegated work, "
        "and regulated evidence needs."
        not in positioning_section
    )
    assert positioning_section.count("\n- ") >= 33
    assert all(len(line) <= 120 for line in opening_section.splitlines())
    assert all(len(line) <= 110 for line in positioning_section.splitlines())


def test_publisher_packet_manuscript_shape_boundary_is_print_friendly() -> None:
    text = _read("docs/publisher-ready-toc.md")
    section = text.split("## Print Manuscript Shape", 1)[1].split(
        "## Sample Chapter Candidates",
        1,
    )[0]
    required_markers = (
        "Target:",
        "- 6 parts;",
        "- about 20 chapters;",
        (
            "- keep schemas, runtime command details, long checklists, "
            "and source catalogs in the online companion."
        ),
        "Online Companion Boundary",
        (
            "- schema appendices for traces, eval datasets, approvals, memory, "
            "and lifecycle artifacts;"
        ),
        "- schema appendices for incident records, rollout gates, and policy bundles;",
    )
    forbidden_inline_markers = (
        "Target: 6 parts, about 20 chapters.",
        (
            "schema appendices for traces, eval datasets, approvals, memory, "
            "lifecycle artifacts, incident records"
        ),
    )

    for marker in required_markers:
        assert marker in section
    for marker in forbidden_inline_markers:
        assert marker not in section
    assert section.count("\n- ") >= 9
    assert all(len(line) <= 135 for line in section.splitlines())



def test_publisher_packet_sample_candidates_are_print_friendly() -> None:
    text = _read("docs/publisher-ready-toc.md")
    section = text.split("## Sample Chapter Candidates", 1)[1].split(
        "## Sample Chapter Export Manifest Draft",
        1,
    )[0]
    required_markers = (
        "### Chapter 1 — strongest publisher sample",
        "Why:",
        "- carries the thesis;",
        "- starts from a failure story;",
        "- shows how the book differs from prompt-hype or framework documentation.",
        "### Chapter 13 — strongest technical credibility sample",
        "- includes a Support triage duplicate-ticket example;",
        (
            "- follows it from trace to verifier attribution, regression gate, "
            "rollout owner action, and release judgment;"
        ),
    )
    forbidden_inline_markers = (
        "Why: it carries the thesis, starts from a failure story",
        "Why: evals, traces, failure attribution, regression gates",
        "includes a Support triage duplicate-ticket example from trace to verifier attribution",
    )

    for marker in required_markers:
        assert marker in section
    for marker in forbidden_inline_markers:
        assert marker not in section
    assert section.count("\n- ") >= 19
    assert all(len(line) <= 135 for line in section.splitlines())



def test_publisher_packet_has_blocker_waiver_decision_log() -> None:
    required_markers = (
        "Blocker Waiver / Decision Log Draft",
        "Print-friendly waiver log starter",
        "no waivers yet",
        "all four blockers remain open",
        "Waiver rules",
        "named decider",
        "date",
        "scope",
        "follow-up owner",
        "No-go signals",
        "governed-systems positioning",
    )

    _assert_files_contain_all(("docs/publisher-ready-toc.md",), required_markers)


def test_publisher_packet_has_external_submission_blocker_register() -> None:
    required_markers = (
        "External Submission Blocker Register",
        "Print-friendly blocker list",
        "not externally sendable",
        "Author bio and credential framing",
        "Independent sample copy-edit",
        "Sample selection",
        "Target editor / imprint formatting",
        "Owner/input needed",
        "Packet action when closed",
        "author explicitly waives",
    )

    _assert_files_contain_all(("docs/publisher-ready-toc.md",), required_markers)


def test_publisher_packet_blocker_sections_are_print_friendly() -> None:
    text = _read("docs/publisher-ready-toc.md")
    blocker_section = text.split("## External Submission Blocker Register", 1)[1].split(
        "## Blocker Waiver / Decision Log Draft",
        1,
    )[0]
    waiver_section = text.split("## Blocker Waiver / Decision Log Draft", 1)[1]
    forbidden_inline_labels = (
        "current state: open; Owner/input needed:",
        "current state: default chosen, not target-specific; Owner/input needed:",
        "**Date:** TBD; **decision:** no waivers yet;",
        "**Waiver rules:** every waiver needs",
        "**No-go signals:** anonymous waiver",
    )

    assert "|" not in blocker_section
    assert "|" not in waiver_section
    assert blocker_section.count("- **") >= 4
    assert blocker_section.count("  - Current state:") == 4
    assert blocker_section.count("  - Owner/input needed:") == 4
    assert blocker_section.count("  - Packet action when closed:") == 4
    assert "  - Scope options: Chapter 1 only, or Chapter 1 plus Chapter 13." in blocker_section
    assert "confirms Chapter 1 only vs Chapter 1 plus Chapter 13" not in blocker_section
    assert (
        "**Submission state:** not externally sendable until all four blockers are closed."
        in blocker_section
    )
    assert "author explicitly waives the remaining blockers." in blocker_section
    assert "until all four blockers are closed or explicitly waived" not in blocker_section
    assert waiver_section.count("- **") >= 6
    for marker in forbidden_inline_labels:
        assert marker not in blocker_section
        assert marker not in waiver_section
    assert all(len(line) <= 110 for line in blocker_section.splitlines())
    assert all(len(line) <= 135 for line in waiver_section.splitlines())


def test_publisher_packet_has_sample_copy_edit_handoff_brief() -> None:
    required_markers = (
        "Sample Copy-Edit Handoff Brief Draft",
        "Copy-edit scope",
        "- sentence flow;",
        "- opening hook;",
        "- paragraph cadence;",
        "Do not rewrite",
        "workflow-first / governed-systems thesis",
        "Questions for the editor",
        "Return format",
        "top 5 changes",
        "No-go signals",
    )

    _assert_files_contain_all(("docs/publisher-ready-toc.md",), required_markers)


def test_publisher_packet_copy_edit_handoff_is_print_friendly() -> None:
    text = _read("docs/publisher-ready-toc.md")
    section = text.split("## Sample Copy-Edit Handoff Brief Draft", 1)[1].split(
        "## Editorial Compression Rules",
        1,
    )[0]
    forbidden_inline_labels = (
        "**Copy-edit scope:** sentence flow",
        "**Do not rewrite:** technical claims",
        "**Questions for the editor:** where does",
        "**Return format:** annotated sample",
        "**No-go signals:** copy edits",
    )

    for marker in forbidden_inline_labels:
        assert marker not in section
    assert "Use this brief when handing Chapter 1 to an independent copy editor" in section
    assert "Include Chapter 13 only if the packet needs a second technical sample." in section
    assert (
        "Use this brief when handing Chapter 1, and optionally Chapter 13, "
        "to an independent copy editor"
        not in section
    )
    assert (
        "- consistency of `agent`, `workflow`, `runtime`, `policy`, and `approval` terms;"
        in section
    )
    assert "- consistency of `trace`, `eval`, and `governance` terms;" in section
    assert "`approval`, `trace`, `eval`, and `governance` terms" not in section
    assert section.count("\n- ") >= 25
    assert all(len(line) <= 110 for line in section.splitlines())


def test_publisher_packet_editorial_compression_rules_are_print_friendly() -> None:
    text = _read("docs/publisher-ready-toc.md")
    section = text.split("## Editorial Compression Rules", 1)[1].split(
        "## Author / Platform Credibility Note Draft",
        1,
    )[0]
    required_markers = (
        "- Use Support triage as the primary running case.",
        "- Use Internal knowledge assistant and Incident coordination as secondary contrast cases.",
        "- End chapters with what to remember and common failure modes.",
        "- Also end with design-review use, companion assets, and the next chapter.",
    )
    forbidden_inline_markers = (
        "Use Support triage as the primary running case; use Internal knowledge assistant",
        (
            "- End chapters with: what to remember, common failure modes, "
            "design-review use, companion assets, and next chapter."
        ),
    )

    for marker in required_markers:
        assert marker in section
    for marker in forbidden_inline_markers:
        assert marker not in section
    assert section.count("\n- ") >= 7
    assert all(len(line) <= 135 for line in section.splitlines())



def test_publisher_packet_has_public_link_availability_record() -> None:
    required_markers = (
        "Public Link Availability Record",
        "Last checked: **2026-05-20**",
        "publisher-packet-2026-05",
        "Checked links:",
        "- public book site;",
        "- English landing page;",
        "- Chinese landing page;",
        "- Chapter 1 sample;",
        "- Chapter 13 technical sample;",
        "- reference runtime source;",
        "- runtime README;",
        "- runtime configs;",
        "- runtime tests.",
        "HTTP 200",
        "all nine checked public links",
        "2026-05-20",
    )

    _assert_files_contain_all(("docs/publisher-ready-toc.md",), required_markers)


def test_publisher_packet_public_links_are_print_friendly() -> None:
    text = _read("docs/publisher-ready-toc.md")
    section = text.split("## Public Links Draft", 1)[1].split(
        "## Public Link Availability Record",
        1,
    )[0]

    assert "Pitch usage:" in section
    assert "Pitch usage: send the public site" not in section
    assert "- send the public site and the two sample chapters first;" in section
    assert "- keep the source/runtime/test links as proof points;" in section
    assert "- use those proof points for editors who want to verify" in section
    assert "- **Runnable reference package README:**\n" in section
    assert "**Runnable reference package README:** <https://" not in section
    assert section.count("\n- ") >= 12
    assert section.count("\n  - ") >= 1
    assert all(len(line) <= 120 for line in section.splitlines())


def test_publisher_packet_public_link_record_is_print_friendly() -> None:
    text = _read("docs/publisher-ready-toc.md")
    section = text.split("## Public Link Availability Record", 1)[1].split(
        "## Pitch Packet Checklist",
        1,
    )[0]

    assert "Checked links: public book site," not in section
    assert "Before external submission, rerun the check." in section
    assert "Update this record if any URL, branch, or packet version changes." in section
    assert "rerun the check and update this record" not in section
    assert section.count("\n- ") == 9
    assert all(len(line) <= 110 for line in section.splitlines())


def test_publisher_packet_cover_note_is_print_friendly() -> None:
    text = _read("docs/publisher-ready-toc.md")
    section = text.split("## Cover Note Draft", 1)[1].split(
        "## Target Editor / Imprint Formatting Brief Draft",
        1,
    )[0]
    required_markers = (
        "Dear [Editor]",
        "I am preparing **Secure AI Agent Architecture**",
        "The book is for teams that need to ship AI agents",
        "The premise is that production agents should be treated as governed systems",
        "Identity, policy, tools, memory, and traces become explicit engineering contracts.",
        "So do eval gates, rollout, and retirement.",
        "Chapter 13 is available as a secondary technical sample",
        "It shows the eval and release-gate treatment.",
        "Before sending:",
        "- replace the greeting;",
        "- add the final author bio/credential sentence;",
        "- tailor the final paragraph to the target editor or imprint.",
    )
    forbidden_inline_markers = (
        "who need to ship AI agents with real tool access, memory, approvals",
        "The book's premise is that production agents should be treated",
        (
            "The manuscript is paired with a public multilingual companion site "
            "and runnable reference material, so"
        ),
        "Before sending, replace the greeting",
        "platform engineers, product engineers,",
        "approvals, observability, evals,",
        "traces, eval gates, rollout, and retirement become explicit engineering contracts",
        "if you would like to see the eval and release-gate treatment",
        "sample chapter, and companion links",
        "publisher-ready table of contents",
    )

    assert "positioning memo, publisher packet, and sample chapter" in section
    for marker in required_markers:
        assert marker in section
    for marker in forbidden_inline_markers:
        assert marker not in section
    assert section.count("\n> ") >= 16
    assert section.count("\n- ") == 3
    assert all(len(line) <= 110 for line in section.splitlines())



def test_publisher_packet_has_target_editor_formatting_brief() -> None:
    required_markers = (
        "Target Editor / Imprint Formatting Brief Draft",
        "Inputs to collect",
        "- editor name;",
        "- imprint;",
        "- submission channel;",
        "- attachment rules;",
        "- sample-chapter policy;",
        "Formatting decisions",
        "publisher-packet-2026-05",
        "secure-ai-agent-architecture-proposal-publisher-packet-2026-05.pdf",
        "Tailoring rules",
        "No-go signals",
    )

    _assert_files_contain_all(("docs/publisher-ready-toc.md",), required_markers)


def test_publisher_packet_target_editor_brief_is_print_friendly() -> None:
    text = _read("docs/publisher-ready-toc.md")
    section = text.split("## Target Editor / Imprint Formatting Brief Draft", 1)[1].split(
        "## Recommended Submission Packet Order",
        1,
    )[0]
    forbidden_inline_labels = (
        "**Inputs to collect:** editor name",
        "**Formatting decisions:** choose whether",
        "**Tailoring rules:** keep the title",
        "**No-go signals:** unknown editor name",
    )

    for marker in forbidden_inline_labels:
        assert marker not in section
    assert section.count("\n- ") >= 25
    assert all(len(line) <= 130 for line in section.splitlines())


def test_publisher_packet_author_platform_note_is_print_friendly() -> None:
    text = _read("docs/publisher-ready-toc.md")
    section = text.split("## Author / Platform Credibility Note Draft", 1)[1].split(
        "## Author Bio Input Brief Draft",
        1,
    )[0]
    required_markers = (
        "Project platform:",
        "- public multilingual book site;",
        "- runnable reference runtime;",
        "- configuration examples;",
        "Claim supported by those artifacts:",
        "- production AI agents should be designed as governed systems, not as prompt demos.",
        "- the companion material includes runnable/reference artifacts;",
        "- readers can inspect the contracts behind the prose;",
        "- the book is written for practitioners who need to ship and operate agents;",
        "- it is not only for readers who want to understand model behavior in the abstract;",
        "Bio gap to fill before submission:",
        "- add a short human author bio with role;",
    )
    forbidden_inline_markers = (
        "Use this as a conservative draft until the final bio is written:",
        "The project already has more than a manuscript outline:",
        "the companion material includes runnable/reference artifacts, so readers can inspect",
        "not only understand model behavior in the abstract",
        "Bio gap to fill before submission: add a short human author bio",
    )

    for marker in required_markers:
        assert marker in section
    for marker in forbidden_inline_markers:
        assert marker not in section
    assert section.count("\n- ") >= 11
    assert all(len(line) <= 135 for line in section.splitlines())



def test_publisher_packet_has_author_bio_input_brief() -> None:
    required_markers = (
        "Author Bio Input Brief Draft",
        "Before this packet becomes external email copy, collect the human-authored facts.",
        "Do not let the manuscript artifact invent those facts.",
        "Required inputs",
        "- preferred author name;",
        "production/engineering background",
        "public project links",
        "Tone constraints",
        "- avoid inflated authority claims;",
        "- prefer concrete artifact-backed credibility;",
        "useful credibility artifacts: public book site",
        "useful supporting artifacts: tests, schemas, and companion material.",
        "Bio slots to prepare",
        "- 50-word short bio;",
        "- 100-word proposal bio;",
        "No-go signals",
    )

    _assert_files_contain_all(("docs/publisher-ready-toc.md",), required_markers)


def test_publisher_packet_author_bio_brief_is_print_friendly() -> None:
    text = _read("docs/publisher-ready-toc.md")
    section = text.split("## Author Bio Input Brief Draft", 1)[1].split(
        "## Comparable Books Draft",
        1,
    )[0]
    forbidden_inline_labels = (
        (
            "Before this packet becomes external email copy, collect the "
            "human-authored facts that should not be invented"
        ),
        "**Required inputs:** preferred author name",
        "**Optional inputs:** prior books",
        "prefer concrete artifact-backed credibility: public book site",
        "**Tone constraints:** avoid inflated",
        "**Bio slots to prepare:** one-line byline",
        "**No-go signals:** missing preferred name",
    )

    for marker in forbidden_inline_labels:
        assert marker not in section
    assert "runnable reference runtime, tests, schemas" not in section
    assert section.count("\n- ") >= 25
    assert all(len(line) <= 110 for line in section.splitlines())


def test_publisher_packet_comparable_books_are_print_friendly() -> None:
    text = _read("docs/publisher-ready-toc.md")
    section = text.split("## Comparable Books Draft", 1)[1].split(
        "## Print Manuscript vs Online Companion Draft",
        1,
    )[0]
    required_markers = (
        "**Designing Data-Intensive Applications**",
        "Comparable angle: systems-thinking discipline.",
        "Difference: applies that operational seriousness",
        "**Designing Machine Learning Systems**",
        "Comparable angle: production ML framing.",
        "**AI Engineering**",
        "**Building Secure & Reliable Systems**",
        "**Site Reliability Engineering**",
        "Short differentiation:",
        "- narrower shelf claim: architect production AI agents as governed systems;",
        (
            "- key controls: explicit rights, evidence, side-effect control, "
            "eval gates, and lifecycle ownership."
        ),
    )
    forbidden_inline_markers = (
        "— comparable in systems-thinking discipline;",
        "— comparable in production ML framing;",
        "Short differentiation: the book is not trying",
    )

    for marker in required_markers:
        assert marker in section
    for marker in forbidden_inline_markers:
        assert marker not in section
    assert "runtime control." in section
    assert "approvals, evals, and observability." in section
    assert "rollout gates, and runtime control" not in section
    assert "trust boundaries, approvals, evals, and observability" not in section
    assert section.count("\n  - Comparable angle:") == 5
    assert section.count("\n  - Difference:") == 7
    assert all(len(line) <= 110 for line in section.splitlines())



def test_publisher_packet_print_companion_split_is_print_friendly() -> None:
    text = _read("docs/publisher-ready-toc.md")
    section = text.split("## Print Manuscript vs Online Companion Draft", 1)[1].split(
        "## Public Links Draft",
        1,
    )[0]
    required_markers = (
        "Print manuscript:",
        "Online companion:",
        "Practical pitch line:",
        "- keeps long field lists and exhaustive schemas out of the main reading path;",
        "- keeps fast-moving implementation details in the companion;",
        "- uses Support triage as the primary through-line;",
        "- uses Internal knowledge assistant and Incident coordination as contrast cases.",
        "- the book should read cleanly in print;",
        (
            "- the companion site proves that the architecture is concrete enough "
            "to run, test, and inspect."
        ),
    )
    forbidden_inline_markers = (
        "Practical pitch line: the book should read cleanly in print",
        "uses Support triage as the primary through-line, with Internal knowledge assistant",
        "long field lists, exhaustive schemas, and fast-moving implementation details",
        "while the companion site proves",
    )

    for marker in required_markers:
        assert marker in section
    for marker in forbidden_inline_markers:
        assert marker not in section
    assert section.count("\n- ") >= 10
    assert all(len(line) <= 110 for line in section.splitlines())



def test_publisher_packet_has_sample_chapter_export_manifest() -> None:
    required_markers = (
        "Sample Chapter Export Manifest Draft",
        "Use this manifest when assembling the first external packet.",
        "It keeps the sample reproducible and prevents companion-link drift.",
        "Primary sample",
        "role: Chapter 1 as the first editorial sample",
        "source path: `docs/book/part-i/chapter-1.en.md`",
        "https://agent-axiom.github.io/agent-arch/en/book/part-i/chapter-1/",
        "Secondary technical sample",
        "role: Chapter 13 as the technical credibility sample",
        "source path: `docs/book/part-v/chapter-13.en.md`",
        "https://agent-axiom.github.io/agent-arch/en/book/part-v/chapter-13/",
        "publisher-packet-2026-05",
        "Export metadata to include",
        "Pre-export checks",
        "technical-credibility reason",
    )

    _assert_files_contain_all(("docs/publisher-ready-toc.md",), required_markers)


def test_publisher_packet_sample_export_manifest_is_print_friendly() -> None:
    text = _read("docs/publisher-ready-toc.md")
    section = text.split("## Sample Chapter Export Manifest Draft", 1)[1].split(
        "## Sample Copy-Edit Handoff Brief Draft",
        1,
    )[0]

    forbidden_inline_labels = (
        (
            "Use this manifest when assembling the first external packet so "
            "the sample is reproducible"
        ),
        "**Primary sample:** Chapter 1",
        "**Secondary technical sample:** Chapter 13,",
        "**Export metadata to include:** title, subtitle",
        "**Pre-export checks:** selected sample",
        "**No-go signals:** stale public URL",
    )

    for marker in forbidden_inline_labels:
        assert marker not in section
    assert section.count("\n- ") >= 20
    assert all(len(line) <= 130 for line in section.splitlines())


def test_publisher_packet_submission_order_is_print_friendly() -> None:
    text = _read("docs/publisher-ready-toc.md")
    section = text.split("## Recommended Submission Packet Order", 1)[1].split(
        "## Print/PDF Readiness Gate Draft",
        1,
    )[0]
    required_markers = (
        "Default recommendation:",
        "3. publisher packet table-of-contents section;",
        "- lead with Chapter 1 only;",
        "- use it because it carries the thesis and reads best as a first editorial sample;",
        "- keep Chapter 13 ready as a second attachment or follow-up;",
        "- send Chapter 13 when the conversation turns to technical credibility.",
    )
    forbidden_inline_markers = (
        "Default recommendation: lead with Chapter 1 only.",
        "Keep Chapter 13 ready as a second attachment or follow-up",
        "publisher-ready table of contents",
    )

    for marker in required_markers:
        assert marker in section
    for marker in forbidden_inline_markers:
        assert marker not in section
    assert section.count("\n- ") >= 4
    assert all(len(line) <= 110 for line in section.splitlines())



def test_publisher_packet_has_print_pdf_readiness_gate() -> None:
    required_markers = (
        "Print/PDF Readiness Gate Draft",
        "Print/PDF checks",
        "stable heading hierarchy",
        "page breaks",
        "code-block wrapping",
        "readable in grayscale",
        "online companion",
        "packet version",
        "sample-chapter date",
        "clipped code blocks",
        "live site navigation",
    )

    _assert_files_contain_all(("docs/publisher-ready-toc.md",), required_markers)


def test_publisher_packet_print_pdf_gate_is_print_friendly() -> None:
    text = _read("docs/publisher-ready-toc.md")
    section = text.split("## Print/PDF Readiness Gate Draft", 1)[1].split(
        "## Submission Release Discipline Draft",
        1,
    )[0]
    forbidden_inline_markers = (
        "**No-go signals:** broken heading levels",
        "URLs are visible enough for print readers, while companion-only links",
        "long schema tables, command-output field lists, validation-error catalogs",
        "or any print sample that depends on live site navigation",
    )

    for marker in forbidden_inline_markers:
        assert marker not in section
    assert "run a print-friction pass." in section
    assert "run a separate pass for print friction" not in section
    assert "**No-go signals:**\n" in section
    assert "- URLs are visible enough for print readers;" in section
    assert "- companion-only links are grouped instead of scattered through the prose;" in section
    assert (
        "- long schema tables and command-output field lists stay in the online companion;"
        in section
    )
    assert (
        "- validation-error catalogs and runtime internals stay in the online companion;"
        in section
    )
    assert section.count("\n- ") >= 14
    assert all(len(line) <= 110 for line in section.splitlines())



def test_publisher_packet_has_submission_release_discipline() -> None:
    required_markers = (
        "Submission Release Discipline Draft",
        "publisher-packet-2026-05",
        "Freeze scope before sending",
        "Pre-send gates",
        "fresh checks",
        "draft localization preview",
        "No-go signals",
    )

    _assert_files_contain_all(("docs/publisher-ready-toc.md",), required_markers)


def test_publisher_packet_submission_release_scope_is_print_friendly() -> None:
    text = _read("docs/publisher-ready-toc.md")
    section = text.split("## Submission Release Discipline Draft", 1)[1].split(
        "## External Submission Blocker Register",
        1,
    )[0]
    required_markers = (
        "**Freeze scope before sending:**",
        "- cover note;",
        "- one-page positioning memo;",
        "- publisher packet TOC section;",
        "- selected sample chapter;",
        "- author/platform credibility note;",
        "- comparable-books note;",
        "- print/companion split;",
        "- public links.",
    )
    forbidden_inline_markers = (
        "**Freeze scope before sending:** cover note",
        "- publisher-ready TOC;",
        "publisher-ready table of contents",
        "author/platform credibility note, comparable-books note",
        (
            "public site, sample-chapter links, repository links, runtime links, "
            "and test links have passed a fresh availability check"
        ),
        "no runtime internals, validation-error catalogs, or long schema tables are moved",
    )

    for marker in required_markers:
        assert marker in section
    for marker in forbidden_inline_markers:
        assert marker not in section
    assert "**No-go signals:**\n" in section
    assert "**No-go signals:** missing author bio" not in section
    assert (
        "- no runtime internals or validation-error catalogs are moved into "
        "the print manuscript packet"
    ) in section
    assert (
        "- no long schema tables are moved into the print manuscript packet by accident."
        in section
    )
    assert all(len(line) <= 110 for line in section.splitlines())


def test_publisher_packet_all_lines_are_print_export_friendly() -> None:
    text = _read("docs/publisher-ready-toc.md")
    overlong_lines = [
        (line_number, len(line), line)
        for line_number, line in enumerate(text.splitlines(), start=1)
        if len(line) > 110
    ]

    assert "- this publisher packet;" in text
    assert "publisher packet table-of-contents section" in text
    assert "publisher packet TOC section" in text
    assert "publisher-ready table of contents" not in text
    assert "publisher-ready TOC" not in text
    assert overlong_lines == []



def test_chapter_17_policy_catalog_threads_three_canonical_cases() -> None:
    required_markers = (
        "Policy case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "write capabilities",
        "approval requirements",
        "read capabilities",
        "corpus scope",
        "memory-write permissions",
        "emergency-only policy overrides",
    )
    checked_files = (
        "docs/book/part-vii/chapter-17.md",
        "docs/book/part-vii/chapter-17.en.md",
        "docs/book/part-vii/chapter-17.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_chapter_8_execution_layer_threads_three_canonical_cases() -> None:
    required_markers = (
        "Execution case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "read tools",
        "write tools",
        "approval handoff",
        "idempotency keys",
        "retrieval tools",
        "corpus filters",
        "responder-role checks",
        "timeout paths",
    )
    checked_files = (
        "docs/book/part-iv/chapter-8.md",
        "docs/book/part-iv/chapter-8.en.md",
        "docs/book/part-iv/chapter-8.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_chapter_9_sandbox_mcp_threads_three_canonical_cases() -> None:
    required_markers = (
        "Sandbox/MCP case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "sandbox limits",
        "approval-aware MCP tools",
        "reconciliation path",
        "read-only MCP resources",
        "corpus-scoped network access",
        "source validation",
        "responder-role enforcement",
        "audit trail",
    )
    checked_files = (
        "docs/book/part-iv/chapter-9.md",
        "docs/book/part-iv/chapter-9.en.md",
        "docs/book/part-iv/chapter-9.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_chapter_10_reliability_threads_three_canonical_cases() -> None:
    required_markers = (
        "Reliability case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "idempotency keys",
        "duplicate-ticket detection",
        "reconciliation",
        "retrieval fan-out",
        "freshness backoff",
        "stale memory writes",
        "notification throttling",
        "side_effect_unknown",
    )
    checked_files = (
        "docs/book/part-iv/chapter-10.md",
        "docs/book/part-iv/chapter-10.en.md",
        "docs/book/part-iv/chapter-10.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_chapter_10_recovery_branches_link_to_eval_schema() -> None:
    expected_links_by_file = {
        "docs/book/part-iv/chapter-10.md": "../../appendix/eval-schema.md",
        "docs/book/part-iv/chapter-10.en.md": "../../appendix/eval-schema.en.md",
        "docs/book/part-iv/chapter-10.zh.md": "../../appendix/eval-schema.zh.md",
    }

    for path, expected_link in expected_links_by_file.items():
        text = _read(path)
        assert f"]({expected_link})" in text, (path, expected_link)


def test_chapter_11_traces_thread_three_canonical_cases() -> None:
    required_markers = (
        "Trace case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "tool spans",
        "approval status",
        "idempotency_key",
        "retrieval spans",
        "source identifiers",
        "freshness markers",
        "memory-write events",
        "verifier evidence",
        "incident-state events",
    )
    checked_files = (
        "docs/book/part-v/chapter-11.md",
        "docs/book/part-v/chapter-11.en.md",
        "docs/book/part-v/chapter-11.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_chapter_11_trace_verifier_evidence_eval_link_is_clickable() -> None:
    expected_links_by_file = {
        "docs/book/part-v/chapter-11.md": "../../appendix/eval-schema.md",
        "docs/book/part-v/chapter-11.en.md": "../../appendix/eval-schema.en.md",
        "docs/book/part-v/chapter-11.zh.md": "../../appendix/eval-schema.zh.md",
    }

    for path, expected_link in expected_links_by_file.items():
        assert f"]({expected_link})" in _read(path), (path, expected_link)


def test_chapter_11_practical_rules_link_verifier_evidence() -> None:
    expected_snippets_by_file = {
        "docs/book/part-v/chapter-11.md": (
            "явную связь с [verifier evidence](../../appendix/eval-schema.md)"
        ),
        "docs/book/part-v/chapter-11.en.md": (
            "explicit linkage to [verifier evidence](../../appendix/eval-schema.en.md)"
        ),
        "docs/book/part-v/chapter-11.zh.md": (
            "指向[验证器证据（verifier evidence）](../../appendix/eval-schema.zh.md)的显式链接"
        ),
    }

    for path, expected_snippet in expected_snippets_by_file.items():
        assert expected_snippet in _read(path), (path, expected_snippet)


def test_chapter_11_evidence_refs_link_verifier_evidence() -> None:
    expected_snippets_by_file = {
        "docs/book/part-v/chapter-11.md": (
            "заново собирать [verifier evidence](../../appendix/eval-schema.md)"
        ),
        "docs/book/part-v/chapter-11.en.md": (
            "reconstruct [verifier evidence](../../appendix/eval-schema.en.md)"
        ),
        "docs/book/part-v/chapter-11.zh.md": (
            "重建[验证器证据（verifier evidence）](../../appendix/eval-schema.zh.md)"
        ),
    }

    for path, expected_snippet in expected_snippets_by_file.items():
        assert expected_snippet in _read(path), (path, expected_snippet)


def test_chapter_12_slo_threads_three_canonical_cases() -> None:
    required_markers = (
        "SLO case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "health budgets",
        "duplicate-ticket rate",
        "approval latency",
        "side_effect_unknown",
        "retrieval freshness",
        "source-grounding success",
        "access-control denials",
        "responder handoff latency",
    )
    checked_files = (
        "docs/book/part-v/chapter-12.md",
        "docs/book/part-v/chapter-12.en.md",
        "docs/book/part-v/chapter-12.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_chapter_14_ownership_threads_three_canonical_cases() -> None:
    required_markers = (
        "Ownership case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "platform/product split",
        "approval policy",
        "write-capability contract",
        "trace schema",
        "corpus ownership",
        "retrieval policy",
        "memory-write rules",
        "escalation authority",
        "post-incident change ownership",
    )
    checked_files = (
        "docs/book/part-vi/chapter-14.md",
        "docs/book/part-vi/chapter-14.en.md",
        "docs/book/part-vi/chapter-14.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_chapter_14_ownership_trace_schema_link_is_clickable() -> None:
    expected_links_by_file = {
        "docs/book/part-vi/chapter-14.md": "../../appendix/trace-schema.md",
        "docs/book/part-vi/chapter-14.en.md": "../../appendix/trace-schema.en.md",
        "docs/book/part-vi/chapter-14.zh.md": "../../appendix/trace-schema.zh.md",
    }

    for path, expected_link in expected_links_by_file.items():
        assert f"]({expected_link})" in _read(path), (path, expected_link)


def test_chapter_15_golden_paths_thread_three_canonical_cases() -> None:
    required_markers = (
        "Golden-path case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "anti-zoo strategy",
        "workflow-agent template",
        "approved write gateway",
        "trace",
        "eval",
        "duplicate-ticket evals",
        "knowledge-agent template",
        "source grounding",
        "memory-write guardrails",
        "incident-agent template",
    )
    checked_files = (
        "docs/book/part-vi/chapter-15.md",
        "docs/book/part-vi/chapter-15.en.md",
        "docs/book/part-vi/chapter-15.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_chapter_15_golden_path_trace_eval_links_are_clickable() -> None:
    expected_links_by_file = {
        "docs/book/part-vi/chapter-15.md": (
            "../../appendix/trace-schema.md",
            "../../appendix/eval-schema.md",
        ),
        "docs/book/part-vi/chapter-15.en.md": (
            "../../appendix/trace-schema.en.md",
            "../../appendix/eval-schema.en.md",
        ),
        "docs/book/part-vi/chapter-15.zh.md": (
            "../../appendix/trace-schema.zh.md",
            "../../appendix/eval-schema.zh.md",
        ),
    }

    for path, expected_links in expected_links_by_file.items():
        text = _read(path)
        for link in expected_links:
            assert f"]({link})" in text, (path, link)


def test_chapter_16_runtime_blueprint_threads_three_canonical_cases() -> None:
    required_markers = (
        "Runtime case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "baseline runtime",
        "approval hooks",
        "idempotency contract",
        "duplicate-ticket telemetry",
        "trace evidence",
        "source grounding",
        "tenant filters",
        "guarded memory writes",
        "incident-state updates",
    )
    checked_files = (
        "docs/book/part-vii/chapter-16.md",
        "docs/book/part-vii/chapter-16.en.md",
        "docs/book/part-vii/chapter-16.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_chapter_16_runtime_trace_evidence_link_is_clickable() -> None:
    expected_links_by_file = {
        "docs/book/part-vii/chapter-16.md": "../../appendix/trace-schema.md",
        "docs/book/part-vii/chapter-16.en.md": "../../appendix/trace-schema.en.md",
        "docs/book/part-vii/chapter-16.zh.md": "../../appendix/trace-schema.zh.md",
    }

    for path, expected_link in expected_links_by_file.items():
        assert f"]({expected_link})" in _read(path), (path, expected_link)


def test_chapter_18_rollout_threads_three_canonical_cases() -> None:
    required_markers = (
        "Rollout case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "production checklist",
        "duplicate-ticket regression gate",
        "approval coverage",
        "idempotency strategy",
        "traces",
        "retrieval freshness gate",
        "source-grounding evals",
        "tenant-boundary checks",
        "post-incident regression plan",
    )
    checked_files = (
        "docs/book/part-vii/chapter-18.md",
        "docs/book/part-vii/chapter-18.en.md",
        "docs/book/part-vii/chapter-18.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_chapter_18_rollout_trace_links_are_clickable() -> None:
    expected_links_by_file = {
        "docs/book/part-vii/chapter-18.md": "../../appendix/trace-schema.md",
        "docs/book/part-vii/chapter-18.en.md": "../../appendix/trace-schema.en.md",
        "docs/book/part-vii/chapter-18.zh.md": "../../appendix/trace-schema.zh.md",
    }

    for path, expected_link in expected_links_by_file.items():
        assert f"]({expected_link})" in _read(path), (path, expected_link)


def test_chapter_19_adlc_threads_three_canonical_cases() -> None:
    required_markers = (
        "ADLC case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "lifecycle state model",
        "release-bearing surfaces",
        "write-capability contract",
        "eval dataset",
        "trace schema",
        "duplicate-ticket evals",
        "retrieval corpus",
        "source-grounding evals",
        "responder-role map",
        "governed change set",
    )
    checked_files = (
        "docs/book/part-viii/chapter-19.md",
        "docs/book/part-viii/chapter-19.en.md",
        "docs/book/part-viii/chapter-19.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_chapter_19_read_next_links_lifecycle_contracts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-19.md": (
            "[Схема артефактов жизненного цикла]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[Схема change review и rollout gate]"
            "(../../appendix/change-rollout-schema.md)",
            "[Схема набора политик и контракта подтверждения]"
            "(../../appendix/policy-bundle-schema.md)",
            "[Схема памяти и извлечения]"
            "(../../appendix/memory-retrieval-schema.md)",
        ),
        "docs/book/part-viii/chapter-19.en.md": (
            "[Lifecycle Artifact Schema]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[Change Review and Rollout Gate Schema]"
            "(../../appendix/change-rollout-schema.en.md)",
            "[Policy Bundle Schema and Approval Contract]"
            "(../../appendix/policy-bundle-schema.en.md)",
            "[Memory and Retrieval Schema]"
            "(../../appendix/memory-retrieval-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-19.zh.md": (
            "[Lifecycle Artifact Schema]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[Change Review and Rollout Gate Schema]"
            "(../../appendix/change-rollout-schema.zh.md)",
            "[Policy Bundle Schema 与 Approval Contract]"
            "(../../appendix/policy-bundle-schema.zh.md)",
            "[Memory and Retrieval Schema]"
            "(../../appendix/memory-retrieval-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_19_adlc_release_artifact_schema_links_are_clickable() -> None:
    expected_links_by_file = {
        "docs/book/part-viii/chapter-19.md": (
            "../../appendix/eval-schema.md",
            "../../appendix/trace-schema.md",
            "../../appendix/policy-bundle-schema.md",
            "../../appendix/change-rollout-schema.md",
            "../../appendix/memory-retrieval-schema.md",
            "../../appendix/incident-record-schema.md",
        ),
        "docs/book/part-viii/chapter-19.en.md": (
            "../../appendix/eval-schema.en.md",
            "../../appendix/trace-schema.en.md",
            "../../appendix/policy-bundle-schema.en.md",
            "../../appendix/change-rollout-schema.en.md",
            "../../appendix/memory-retrieval-schema.en.md",
            "../../appendix/incident-record-schema.en.md",
        ),
        "docs/book/part-viii/chapter-19.zh.md": (
            "../../appendix/eval-schema.zh.md",
            "../../appendix/trace-schema.zh.md",
            "../../appendix/policy-bundle-schema.zh.md",
            "../../appendix/change-rollout-schema.zh.md",
            "../../appendix/memory-retrieval-schema.zh.md",
            "../../appendix/incident-record-schema.zh.md",
        ),
    }

    for path, expected_links in expected_links_by_file.items():
        text = _read(path)
        for link in expected_links:
            assert f"]({link})" in text, (path, link)


def test_chapter_21_assurance_threads_three_canonical_cases() -> None:
    required_markers = (
        "Assurance case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "finding and response record",
        "containment paths",
        "duplicate-outcome detection",
        "updated eval",
        "traceable outcome",
        "approval-only containment",
        "retrieval-poisoning signal",
        "tenant-boundary containment",
        "notification throttling",
        "post-incident control update",
    )
    checked_files = (
        "docs/book/part-viii/chapter-21.md",
        "docs/book/part-viii/chapter-21.en.md",
        "docs/book/part-viii/chapter-21.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_chapter_21_assurance_case_spine_links_are_clickable() -> None:
    expected_links_by_file = {
        "docs/book/part-viii/chapter-21.md": (
            "../../appendix/eval-schema.md",
            "../../appendix/trace-schema.md",
            "../../appendix/incident-record-schema.md",
            "../../appendix/approval-schema.md",
            "../../appendix/memory-retrieval-schema.md",
            "../../appendix/lifecycle-artifact-schema.md",
        ),
        "docs/book/part-viii/chapter-21.en.md": (
            "../../appendix/eval-schema.en.md",
            "../../appendix/trace-schema.en.md",
            "../../appendix/incident-record-schema.en.md",
            "../../appendix/approval-schema.en.md",
            "../../appendix/memory-retrieval-schema.en.md",
            "../../appendix/lifecycle-artifact-schema.en.md",
        ),
        "docs/book/part-viii/chapter-21.zh.md": (
            "../../appendix/eval-schema.zh.md",
            "../../appendix/trace-schema.zh.md",
            "../../appendix/incident-record-schema.zh.md",
            "../../appendix/approval-schema.zh.md",
            "../../appendix/memory-retrieval-schema.zh.md",
            "../../appendix/lifecycle-artifact-schema.zh.md",
        ),
    }

    for path, expected_links in expected_links_by_file.items():
        text = _read(path)
        for link in expected_links:
            assert f"]({link})" in text, (path, link)


def test_chapter_21_useful_refs_include_change_rollout_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-21.md": (
            "[Схема change review и rollout gate]"
            "(../../appendix/change-rollout-schema.md)"
        ),
        "docs/book/part-viii/chapter-21.en.md": (
            "[Change Review and Rollout Gate Schema]"
            "(../../appendix/change-rollout-schema.en.md)"
        ),
        "docs/book/part-viii/chapter-21.zh.md": (
            "[Change Review and Rollout Gate Schema]"
            "(../../appendix/change-rollout-schema.zh.md)"
        ),
    }

    for path, expected_snippet in expected_snippets_by_file.items():
        assert expected_snippet in _read(path), (path, expected_snippet)


def test_chapter_22_supply_chain_threads_three_canonical_cases() -> None:
    required_markers = (
        "Supply-chain case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "approved artifact bundle",
        "provenance",
        "capability contract",
        "eval dataset",
        "trace schema",
        "approval schema",
        "approved retrieval corpus",
        "source-grounding rubric",
        "responder-role map",
        "post-incident artifact update",
    )
    checked_files = (
        "docs/book/part-viii/chapter-22.md",
        "docs/book/part-viii/chapter-22.en.md",
        "docs/book/part-viii/chapter-22.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_chapter_22_supply_chain_schema_links_are_clickable() -> None:
    expected_links_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "../../appendix/eval-schema.md",
            "../../appendix/policy-bundle-schema.md",
            "../../appendix/approval-schema.md",
            "../../appendix/trace-schema.md",
            "../../appendix/change-rollout-schema.md",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "../../appendix/eval-schema.en.md",
            "../../appendix/policy-bundle-schema.en.md",
            "../../appendix/approval-schema.en.md",
            "../../appendix/trace-schema.en.md",
            "../../appendix/change-rollout-schema.en.md",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "../../appendix/eval-schema.zh.md",
            "../../appendix/policy-bundle-schema.zh.md",
            "../../appendix/approval-schema.zh.md",
            "../../appendix/trace-schema.zh.md",
            "../../appendix/change-rollout-schema.zh.md",
        ),
    }

    for path, expected_links in expected_links_by_file.items():
        text = _read(path)
        for link in expected_links:
            assert f"]({link})" in text, (path, link)


def test_chapter_22_provenance_questions_link_approval_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "contract version и [approval schema](../../appendix/approval-schema.md)"
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "contract version and [approval schema](../../appendix/approval-schema.en.md)"
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "契约版本与[审批模式（approval schema）](../../appendix/approval-schema.zh.md)"
        ),
    }

    for path, expected_snippet in expected_snippets_by_file.items():
        assert expected_snippet in _read(path), (path, expected_snippet)


def test_chapter_22_provenance_questions_link_policy_bundle() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "какой [policy bundle](../../appendix/policy-bundle-schema.md) был активен"
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "which [policy bundle](../../appendix/policy-bundle-schema.en.md) was active"
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "哪一个[策略包（policy bundle）](../../appendix/policy-bundle-schema.zh.md)"
        ),
    }

    for path, expected_snippet in expected_snippets_by_file.items():
        assert expected_snippet in _read(path), (path, expected_snippet)


def test_chapter_22_artifact_inventory_links_lifecycle_artifacts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[capability contract](../../appendix/lifecycle-artifact-schema.md)",
            "[runtime-control schema](../../appendix/lifecycle-artifact-schema.md)",
            "[правила interruption и re-initialization для capability sessions]"
            "(../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[capability contract](../../appendix/lifecycle-artifact-schema.en.md)",
            "[runtime-control schema](../../appendix/lifecycle-artifact-schema.en.md)",
            "[capability-session interruption and re-initialization rules]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[能力契约（capability contract）]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[运行时控制模式（runtime-control schema）]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[能力会话中断与重新初始化规则]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_supply_chain_surface_links_control_schemas() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[правила и схемы approval](../../appendix/approval-schema.md)",
            "[схемы runtime-control](../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[approval rules and schemas](../../appendix/approval-schema.en.md)",
            "[runtime-control schemas]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[审批规则与模式](../../appendix/approval-schema.zh.md)",
            "[运行时控制模式](../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_supply_chain_surface_links_artifact_families() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[конфигурации политик](../../appendix/policy-bundle-schema.md)",
            "[корпуса для извлечения](../../appendix/memory-retrieval-schema.md)",
            "[контракты возможностей](../../appendix/lifecycle-artifact-schema.md)",
            "[наборы для оценки](../../appendix/eval-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[policy configs](../../appendix/policy-bundle-schema.en.md)",
            "[retrieval corpora](../../appendix/memory-retrieval-schema.en.md)",
            "[capability contracts](../../appendix/lifecycle-artifact-schema.en.md)",
            "[eval datasets](../../appendix/eval-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[策略配置](../../appendix/policy-bundle-schema.zh.md)",
            "[检索语料](../../appendix/memory-retrieval-schema.zh.md)",
            "[能力契约](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[评测数据集](../../appendix/eval-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_supply_chain_surface_links_rollout_bundles() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[наборы для раскатки](../../appendix/change-rollout-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[rollout bundles](../../appendix/change-rollout-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[发布工件包](../../appendix/change-rollout-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_approved_model_route_links_lifecycle_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "утвержденный [маршрут к модели]"
            "(../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "approved [model route]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "已批准的[模型路由](../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_approved_prompt_bundle_links_lifecycle_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "утвержденный [набор prompt-правил]"
            "(../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "approved [prompt bundle]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "已批准的[提示包](../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_prompt_bundle_provenance_links_eval_rollout_schemas() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[оценки](../../appendix/eval-schema.md) ее покрыли",
            "[волне раскатки](../../appendix/change-rollout-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[evals](../../appendix/eval-schema.en.md) covered it",
            "[rollout wave](../../appendix/change-rollout-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[评测](../../appendix/eval-schema.zh.md)覆盖了它",
            "[rollout 波次](../../appendix/change-rollout-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_prompt_bundle_provenance_links_owner_version_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[кто менял prompt](../../appendix/lifecycle-artifact-schema.md)",
            "[какая версия](../../appendix/lifecycle-artifact-schema.md) сейчас в проде",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[who changed the prompt](../../appendix/lifecycle-artifact-schema.en.md)",
            "[which version](../../appendix/lifecycle-artifact-schema.en.md) "
            "is in production",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[谁改了提示](../../appendix/lifecycle-artifact-schema.zh.md)",
            "生产环境里是[哪一个版本](../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_prompt_bundle_related_routines_link_lifecycle_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[routines](../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[routines](../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[例程](../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_supply_chain_surface_links_model_prompt_artifacts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[маршруты к моделям](../../appendix/lifecycle-artifact-schema.md)",
            "[наборы prompt- и routine-правил]"
            "(../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[model artifacts](../../appendix/lifecycle-artifact-schema.en.md)",
            "[prompt and routine bundles]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[模型工件](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[提示和例程包](../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_provenance_questions_link_model_prompt_artifacts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[откуда взялась эта модель](../../appendix/lifecycle-artifact-schema.md)",
            "[набор prompt-правил](../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[where this model came from]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[prompt bundle](../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[这个模型从哪里来](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[提示包](../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_trust_chain_links_data_retrieval_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[цепочкой данных и извлечения]"
            "(../../appendix/memory-retrieval-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[data and retrieval chain]"
            "(../../appendix/memory-retrieval-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[数据与检索链](../../appendix/memory-retrieval-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_trust_chain_links_eval_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[цепочкой оценки](../../appendix/eval-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[eval chain](../../appendix/eval-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[评测链](../../appendix/eval-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_trust_chain_links_policy_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[цепочкой политик](../../appendix/policy-bundle-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[policy chain](../../appendix/policy-bundle-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[策略链](../../appendix/policy-bundle-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_trust_chain_links_capability_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[цепочкой возможностей](../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[capability chain](../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[能力链](../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_trust_chain_links_approval_runtime_control_schemas() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[approval](../../appendix/approval-schema.md) и "
            "[runtime-control](../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[approval](../../appendix/approval-schema.en.md) and "
            "[runtime-control](../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[审批](../../appendix/approval-schema.zh.md)与"
            "[运行时控制](../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_trust_chain_links_session_authorization_schemas() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[цепочкой правил управления capability sessions]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[цепочкой delegated authorization]"
            "(../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[capability-session governance chain]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[delegated authorization chain]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[能力会话治理链](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[委派授权链](../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_trust_chain_links_model_prompt_schemas() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[цепочкой моделей](../../appendix/lifecycle-artifact-schema.md)",
            "[цепочкой prompt- и routine-правил]"
            "(../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[model chain](../../appendix/lifecycle-artifact-schema.en.md)",
            "[prompt and routine chain]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[模型链](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[提示与例程链](../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_provenance_questions_link_eval_dataset() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "какой [eval dataset](../../appendix/eval-schema.md) подтвердил выпуск",
            "считать [eval dataset](../../appendix/eval-schema.md) чем-то второстепенным",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "which [eval dataset](../../appendix/eval-schema.en.md) validated the release",
            "treat an [eval dataset](../../appendix/eval-schema.en.md) as secondary",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "哪一个[评测数据集（eval dataset）](../../appendix/eval-schema.zh.md)验证",
            "把[评测数据集（eval dataset）](../../appendix/eval-schema.zh.md)看得太轻",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_runtime_control_schema_links_are_clickable() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[approval schema](../../appendix/approval-schema.md)",
            "[runtime-control schema](../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[approval schemas](../../appendix/approval-schema.en.md)",
            "[runtime-control schemas](../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[审批模式（approval schema）](../../appendix/approval-schema.zh.md)",
            "[运行时控制模式（runtime-control schema）]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_trusted_artifact_examples_link_schema_contracts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[policy YAML](../../appendix/policy-bundle-schema.md)",
            "[конфигурациям извлечения](../../appendix/memory-retrieval-schema.md)",
            "[порогам подтверждения](../../appendix/approval-schema.md)",
            "[runtime-control schemas](../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[policy YAML](../../appendix/policy-bundle-schema.en.md)",
            "[retrieval configs](../../appendix/memory-retrieval-schema.en.md)",
            "[approval thresholds](../../appendix/approval-schema.en.md)",
            "[runtime-control schemas](../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[策略 YAML](../../appendix/policy-bundle-schema.zh.md)",
            "[检索配置](../../appendix/memory-retrieval-schema.zh.md)",
            "[审批阈值](../../appendix/approval-schema.zh.md)",
            "[运行时控制模式](../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_artifact_discipline_failures_link_schema_contracts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[наборы для оценки](../../appendix/eval-schema.md)",
            "[контракты возможностей](../../appendix/lifecycle-artifact-schema.md)",
            "[approval schemas](../../appendix/approval-schema.md) или "
            "[runtime-control schemas](../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[eval datasets](../../appendix/eval-schema.en.md)",
            "[capability contracts](../../appendix/lifecycle-artifact-schema.en.md)",
            "[approval schemas](../../appendix/approval-schema.en.md) or "
            "[runtime-control schemas](../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[评测数据集](../../appendix/eval-schema.zh.md)",
            "[能力契约](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[审批模式](../../appendix/approval-schema.zh.md)或"
            "[运行时控制模式](../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_maturity_bar_links_production_artifact_contracts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[policy](../../appendix/policy-bundle-schema.md)-",
            "[eval](../../appendix/eval-schema.md)-",
            "[capability](../../appendix/lifecycle-artifact-schema.md)-",
            "[approval](../../appendix/approval-schema.md)-",
            "[runtime-control](../../appendix/lifecycle-artifact-schema.md)-",
            "[verifier](../../appendix/eval-schema.md)-артефакты",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[policy](../../appendix/policy-bundle-schema.en.md)",
            "[eval](../../appendix/eval-schema.en.md)",
            "[capability](../../appendix/lifecycle-artifact-schema.en.md)",
            "[approval](../../appendix/approval-schema.en.md)",
            "[runtime-control](../../appendix/lifecycle-artifact-schema.en.md)",
            "[verifier](../../appendix/eval-schema.en.md) artifacts",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[策略](../../appendix/policy-bundle-schema.zh.md)",
            "[评测](../../appendix/eval-schema.zh.md)",
            "[能力](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[审批](../../appendix/approval-schema.zh.md)",
            "[runtime-control](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[verifier](../../appendix/eval-schema.zh.md) 工件",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_approved_inventory_links_registry_handbook() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[утвержденный реестр](../../appendix/registry-operations-handbook.md)",
            "[approved inventory](../../appendix/registry-operations-handbook.md)",
            "[утвержденный реестр платформы]"
            "(../../appendix/registry-operations-handbook.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[approved inventory](../../appendix/registry-operations-handbook.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[已批准清单](../../appendix/registry-operations-handbook.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_checklist_links_platform_and_release_artifacts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[шаблон, разрешенный на уровне платформы]"
            "(../../appendix/change-rollout-schema.md)",
            "[артефакта, разрешенного к выпуску]"
            "(../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[platform-approved pattern](../../appendix/change-rollout-schema.en.md)",
            "[release-approved artifact]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[平台批准的模式](../../appendix/change-rollout-schema.zh.md)",
            "[发布批准的工件](../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_deprecated_artifacts_link_lifecycle_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[устаревшие шаблоны](../../appendix/lifecycle-artifact-schema.md)",
            "[deprecated patterns](../../appendix/lifecycle-artifact-schema.md)",
            "[устаревший артефакт](../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[deprecated patterns](../../appendix/lifecycle-artifact-schema.en.md)",
            "[deprecated artifact](../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[已废弃模式](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[已废弃工件](../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_incident_evidence_links_schema_lineage() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[доказательном слое](../../appendix/trace-schema.md)",
            "[verifier lineage](../../appendix/eval-schema.md)",
            "[активные версии контрактов и схем](../../appendix/trace-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[contract-version linkage](../../appendix/trace-schema.en.md)",
            "[incident evidence](../../appendix/incident-record-schema.en.md)",
            "[verifier-contract lineage](../../appendix/eval-schema.en.md)",
            "[active contract/schema versions](../../appendix/trace-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[事故证据](../../appendix/incident-record-schema.zh.md)",
            "[契约版本链接](../../appendix/trace-schema.zh.md)",
            "[验证器契约血缘](../../appendix/eval-schema.zh.md)",
            "[生效中的契约/模式版本](../../appendix/trace-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_checklist_links_production_artifact_ownership() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[рабочих артефактов](../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[production artifacts](../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[生产工件](../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_approved_artifact_definition_links_lifecycle_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[Доверенный артефакт](../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[approved artifact](../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[已批准工件](../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_approved_artifact_bundle_links_lifecycle_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[approved artifact bundle](../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[approved artifact bundle]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[approved artifact bundle]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_duplicate_ticket_release_bundle_links_lifecycle_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[approved release bundle](../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[approved release bundle]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[已批准发布包](../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_inventory_artifact_distinction_links_both_contracts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[approved inventory](../../appendix/registry-operations-handbook.md) отвечает",
            "[approved artifacts](../../appendix/lifecycle-artifact-schema.md) отвечает",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[approved inventory]"
            "(../../appendix/registry-operations-handbook.en.md) answers",
            "[approved artifacts]"
            "(../../appendix/lifecycle-artifact-schema.en.md) answers",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[已批准清单](../../appendix/registry-operations-handbook.zh.md)回答的是",
            "[已批准工件](../../appendix/lifecycle-artifact-schema.zh.md)回答的是",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_approved_artifact_versions_bundles_link_lifecycle_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "конкретные [версии и наборы]"
            "(../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "exact [versions and bundles]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[具体版本和工件包](../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_release_discipline_links_bundle_and_verifier_contracts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[управляемой версией, утвержденным набором]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[семейством контрактов с verifier-ограничениями]"
            "(../../appendix/eval-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[governed version, approved bundle]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[verifier-bearing contract family]"
            "(../../appendix/eval-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[受治理版本、已批准包](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[带有验证器约束的契约族](../../appendix/eval-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_governed_lineage_links_release_identity_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[доверенных артефактов, идентичности выпуска и версий]"
            "(../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[approved artifacts, release identity, and decision-bearing versions]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[已批准工件、发布身份与承载决策版本]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_core_promise_links_reviewed_release_identity() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[проверенный набор артефактов]"
            "(../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[reviewed artifact set, trusted contract version, and approved "
            "release identity](../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[哪一组已评审工件、哪一个可信契约版本，以及哪一个已批准发布身份]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_capability_contract_checklist_links_control_schemas() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[кто владелец](../../appendix/lifecycle-artifact-schema.md)",
            "[какой уровень риска](../../appendix/approval-schema.md)",
            "[какой инструментальный principal]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[какой профиль сетевого доступа]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[какие направления выхода разрешены]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[как устроена семантика подтверждения]"
            "(../../appendix/approval-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[who the owner is](../../appendix/lifecycle-artifact-schema.en.md)",
            "[what the risk tier is](../../appendix/approval-schema.en.md)",
            "[which tool principal is used]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[what the network access profile is]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[which egress destinations are allowed]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[which approval semantics apply](../../appendix/approval-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[谁是负责人](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[风险等级是什么](../../appendix/approval-schema.zh.md)",
            "[使用哪个工具 principal](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[网络访问配置是什么](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[允许哪些出口目标](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[采用什么审批语义](../../appendix/approval-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_runtime_control_provenance_checklist_links_control_schemas() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[paused runs истекали или могли ждать бесконечно]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[capability-session re-init была allowed, denied или approval-bound]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[telemetry обязана была связывать исходную и reinitialized "
            "capability sessions](../../appendix/trace-schema.md)",
            "[approval](../../appendix/approval-schema.md) и "
            "[session-control logic](../../appendix/lifecycle-artifact-schema.md)",
            "[delegated access была platform-owned или user-delegated]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[principal-binding rule и revoke behavior]"
            "(../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[paused runs expired or waited indefinitely]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[capability-session re-init was allowed, denied, or approval-bound]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[telemetry was expected to link the original and reinitialized "
            "capability sessions](../../appendix/trace-schema.en.md)",
            "[approval](../../appendix/approval-schema.en.md) and "
            "[session-control logic](../../appendix/lifecycle-artifact-schema.en.md)",
            "[delegated access was platform-owned or user-delegated]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[principal-binding rule and revoke behavior]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[暂停运行是会过期，还是可以无限等待]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[能力会话重新初始化是 allowed、denied，还是 approval-bound]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[遥测是否应该把原始能力会话和重新初始化后的能力会话关联起来]"
            "(../../appendix/trace-schema.zh.md)",
            "[审批](../../appendix/approval-schema.zh.md)与"
            "[会话控制逻辑](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[委派访问是平台拥有还是用户委派]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[principal 绑定规则与撤销行为]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_harness_handoff_artifacts_link_lifecycle_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[структурированных handoff artifacts]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[какой handoff artifact перенес scope, какой evaluator critique "
            "изменил следующий sprint и на какой reset boundary активный "
            "контекст сменился](../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[structured handoff artifacts]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[which handoff artifact carried scope, which evaluator critique "
            "shaped the next sprint, and which reset boundary changed the "
            "active context](../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[结构化交接工件](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[是哪一份交接工件传递了 scope、哪一条 evaluator critique "
            "改变了下一轮 sprint，以及是在什么重置边界上，活动上下文发生了变化]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_boundary_parity_links_telemetry_and_contract_family() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[Telemetry](../../appendix/trace-schema.md) может показать",
            "pause, re-init или delegated action",
            "[проверенная contract family](../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[Telemetry](../../appendix/trace-schema.en.md) may show",
            "[pause, re-init, or delegated action]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[reviewed contract family]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[遥测](../../appendix/trace-schema.zh.md)也许能告诉你",
            "[暂停、重新初始化或委派动作]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[经过评审的契约族]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_failed_run_provenance_links_identity_and_eval_fields() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[набор доверенных артефактов и какая идентичность выпуска]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[экспортируемое поле, например `failure_reason`]"
            "(../../appendix/eval-schema.md)",
            "[`latest_failure_reason`](../../appendix/eval-schema.md)",
            "[`traceable_failed_runs`](../../appendix/eval-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[approved artifact set and release identity]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[exported failure field such as `failure_reason`]"
            "(../../appendix/eval-schema.en.md)",
            "[`latest_failure_reason`](../../appendix/eval-schema.en.md)",
            "[`traceable_failed_runs`](../../appendix/eval-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[哪一组已批准工件与哪一个发布身份]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[导出字段，例如 `failure_reason`](../../appendix/eval-schema.zh.md)",
            "[`latest_failure_reason`](../../appendix/eval-schema.zh.md)",
            "[`traceable_failed_runs`](../../appendix/eval-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_maturity_bar_links_inventory_and_artifacts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[approved inventory](../../appendix/registry-operations-handbook.md) "
            "и [approved artifacts](../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[approved inventory]"
            "(../../appendix/registry-operations-handbook.en.md) and "
            "[approved artifacts](../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[已批准清单](../../appendix/registry-operations-handbook.zh.md)"
            "和[已批准工件](../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_links_verifier_contract_to_eval_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "какой [verifier contract](../../appendix/eval-schema.md)",
            "[verifier contracts](../../appendix/eval-schema.md)",
            "[verifier contract](../../appendix/eval-schema.md) не просто оценивает качество",
            "активного [verifier contract](../../appendix/eval-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "which [verifier contract](../../appendix/eval-schema.en.md)",
            "[verifier contracts](../../appendix/eval-schema.en.md)",
            "[verifier contract](../../appendix/eval-schema.en.md) does not merely score quality",
            "active [verifier contract](../../appendix/eval-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "哪一版[验证器契约（verifier contract）](../../appendix/eval-schema.zh.md)",
            "[验证器契约（verifier contract）](../../appendix/eval-schema.zh.md)",
            "[验证器契约（verifier contract）](../../appendix/eval-schema.zh.md)不只是给质量打分",
            "生效的[验证器契约（verifier contract）](../../appendix/eval-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_links_grading_and_evidence_rules_to_eval_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[rubric definitions и правила связывания доказательной базы]"
            "(../../appendix/eval-schema.md)",
            "[grading rubric и правила связывания доказательной базы]"
            "(../../appendix/eval-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[grading rules and evidence-linkage rules]"
            "(../../appendix/eval-schema.en.md)",
            "[grading rubric and evidence-linkage rules]"
            "(../../appendix/eval-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[评分规则与证据链接规则](../../appendix/eval-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_links_session_and_delegation_rules_to_lifecycle_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[interruption или expiry policy]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[delegated authorization mode, principal binding и revoke policy]"
            "(../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[interruption or expiry policy]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[delegated authorization mode, principal binding, and revoke policy]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[中断或过期策略](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[委派授权模式、principal 绑定与撤销策略]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_links_orchestration_rules_to_change_rollout_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[governance-правила для orchestration pattern и определения worker-safe catalog]"
            "(../../appendix/change-rollout-schema.md)",
            "[orchestration pattern и какая worker-boundary policy]"
            "(../../appendix/change-rollout-schema.md)",
            "[изменения в orchestration pattern]"
            "(../../appendix/change-rollout-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[orchestration-pattern governance rules and worker-safe catalog definitions]"
            "(../../appendix/change-rollout-schema.en.md)",
            "[orchestration pattern and worker-boundary policy]"
            "(../../appendix/change-rollout-schema.en.md)",
            "[orchestration-pattern governance changes]"
            "(../../appendix/change-rollout-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[编排模式治理规则与 worker-safe 目录定义]"
            "(../../appendix/change-rollout-schema.zh.md)",
            "[编排模式与 worker 边界策略]"
            "(../../appendix/change-rollout-schema.zh.md)",
            "[编排模式治理变更]"
            "(../../appendix/change-rollout-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_artifact_inventory_links_rollout_gate() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "утвержденный [rollout gate](../../appendix/change-rollout-schema.md)"
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "approved [rollout gate](../../appendix/change-rollout-schema.en.md)"
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "已批准的[发布门禁（rollout gate）]"
            "(../../appendix/change-rollout-schema.zh.md)"
        ),
    }

    for path, expected_snippet in expected_snippets_by_file.items():
        assert expected_snippet in _read(path), (path, expected_snippet)


def test_chapter_22_provenance_questions_link_retrieval_corpus() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "какой [retrieval corpus](../../appendix/memory-retrieval-schema.md) использовался",
            "[approved retrieval corpus](../../appendix/memory-retrieval-schema.md)",
            "[source-grounding rubric, tenant-filter config, memory-write policy "
            "и freshness attestation](../../appendix/memory-retrieval-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "which [retrieval corpus](../../appendix/memory-retrieval-schema.en.md) was used",
            "[approved retrieval corpus](../../appendix/memory-retrieval-schema.en.md)",
            "[source-grounding rubric, tenant-filter config, memory-write policy, "
            "and freshness attestation](../../appendix/memory-retrieval-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "哪一版[检索语料（retrieval corpus）]"
            "(../../appendix/memory-retrieval-schema.zh.md)",
            "[approved retrieval corpus](../../appendix/memory-retrieval-schema.zh.md)",
            "[source-grounding rubric、tenant-filter config、memory-write policy "
            "和 freshness attestation](../../appendix/memory-retrieval-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_duplicate_ticket_case_links_release_artifacts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[policy bundle](../../appendix/policy-bundle-schema.md) для `side_effect_unknown`",
            "[capability contract](../../appendix/lifecycle-artifact-schema.md) "
            "`create_support_ticket`",
            "[rollout gate](../../appendix/change-rollout-schema.md), "
            "[approval schema](../../appendix/approval-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "`side_effect_unknown` [policy bundle](../../appendix/policy-bundle-schema.en.md)",
            "`create_support_ticket` [capability contract]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[rollout gate](../../appendix/change-rollout-schema.en.md), "
            "[approval schema](../../appendix/approval-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "`side_effect_unknown` [策略包（policy bundle）]"
            "(../../appendix/policy-bundle-schema.zh.md)",
            "`create_support_ticket` [能力契约（capability contract）]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[rollout gate](../../appendix/change-rollout-schema.zh.md)、"
            "[审批模式（approval schema）](../../appendix/approval-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_incident_case_spine_links_incident_artifacts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[escalation-policy bundle, notification contract и responder-role map]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[incident-state schema](../../appendix/incident-record-schema.md)",
            "[post-incident artifact update](../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[escalation-policy bundle, notification contract, and responder-role map]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[incident-state schema](../../appendix/incident-record-schema.en.md)",
            "[post-incident artifact update](../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[escalation-policy bundle、notification contract、responder-role map]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[incident-state schema](../../appendix/incident-record-schema.zh.md)",
            "[post-incident artifact update](../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_practical_checklist_links_artifact_version_contracts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[policy](../../appendix/policy-bundle-schema.md)-",
            "[approval](../../appendix/approval-schema.md)-",
            "[runtime-control](../../appendix/lifecycle-artifact-schema.md)-",
            "[eval- и verifier](../../appendix/eval-schema.md)-артефактов",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[policy](../../appendix/policy-bundle-schema.en.md)",
            "[approval-schema](../../appendix/approval-schema.en.md)",
            "[runtime-control](../../appendix/lifecycle-artifact-schema.en.md)",
            "[eval, and verifier](../../appendix/eval-schema.en.md) artifacts",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[策略](../../appendix/policy-bundle-schema.zh.md)",
            "[approval-schema](../../appendix/approval-schema.zh.md)",
            "[runtime-control](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[评测和验证器](../../appendix/eval-schema.zh.md)工件",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_useful_refs_include_supply_chain_schema_pages() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[Схема approval](../../appendix/approval-schema.md)",
            "[Схема change review и rollout gate]"
            "(../../appendix/change-rollout-schema.md)",
            "[Схема наборов для оценки и правил проверки]"
            "(../../appendix/eval-schema.md)",
            "[Схема трасс и каталог событий](../../appendix/trace-schema.md)",
            "[Схема памяти и извлечения]"
            "(../../appendix/memory-retrieval-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[Approval Schema](../../appendix/approval-schema.en.md)",
            "[Change Review and Rollout Gate Schema]"
            "(../../appendix/change-rollout-schema.en.md)",
            "[Eval Dataset Schema and Grading Contract]"
            "(../../appendix/eval-schema.en.md)",
            "[Trace Schema and Event Catalog](../../appendix/trace-schema.en.md)",
            "[Memory and Retrieval Schema]"
            "(../../appendix/memory-retrieval-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[Approval Schema](../../appendix/approval-schema.zh.md)",
            "[Change Review and Rollout Gate Schema]"
            "(../../appendix/change-rollout-schema.zh.md)",
            "[Eval Dataset Schema and Grading Contract]"
            "(../../appendix/eval-schema.zh.md)",
            "[Trace Schema and Event Catalog](../../appendix/trace-schema.zh.md)",
            "[Memory and Retrieval Schema]"
            "(../../appendix/memory-retrieval-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_24_misalignment_threads_three_canonical_cases() -> None:
    required_markers = (
        "Misalignment case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "risk scenario and control plan",
        "insider-risk surfaces",
        "approval-tight replacement window",
        "separate tool principal",
        "immutable trace linkage",
        "retrieval poisoning",
        "tenant-filter bypass",
        "notification suppression",
        "incident-state tampering",
    )
    checked_files = (
        "docs/book/part-viii/chapter-24.md",
        "docs/book/part-viii/chapter-24.en.md",
        "docs/book/part-viii/chapter-24.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_chapter_24_misalignment_useful_refs_include_risk_evidence_contracts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-24.md": (
            "[Схема трасс и каталог событий](../../appendix/trace-schema.md)",
            "[Схема наборов для оценки и правил проверки]"
            "(../../appendix/eval-schema.md)",
            "[Схема памяти и извлечения]"
            "(../../appendix/memory-retrieval-schema.md)",
        ),
        "docs/book/part-viii/chapter-24.en.md": (
            "[Trace Schema and Event Catalog](../../appendix/trace-schema.en.md)",
            "[Eval Dataset Schema and Grading Contract]"
            "(../../appendix/eval-schema.en.md)",
            "[Memory and Retrieval Schema]"
            "(../../appendix/memory-retrieval-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-24.zh.md": (
            "[Trace Schema 与 Event Catalog](../../appendix/trace-schema.zh.md)",
            "[Eval Dataset Schema 与 Grading Contract]"
            "(../../appendix/eval-schema.zh.md)",
            "[Memory and Retrieval Schema]"
            "(../../appendix/memory-retrieval-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_24_misalignment_case_spine_links_are_clickable() -> None:
    expected_links_by_file = {
        "docs/book/part-viii/chapter-24.md": (
            "../../appendix/change-rollout-schema.md",
            "../../appendix/trace-schema.md",
            "../../appendix/memory-retrieval-schema.md",
            "../../appendix/incident-record-schema.md",
        ),
        "docs/book/part-viii/chapter-24.en.md": (
            "../../appendix/change-rollout-schema.en.md",
            "../../appendix/trace-schema.en.md",
            "../../appendix/memory-retrieval-schema.en.md",
            "../../appendix/incident-record-schema.en.md",
        ),
        "docs/book/part-viii/chapter-24.zh.md": (
            "../../appendix/change-rollout-schema.zh.md",
            "../../appendix/trace-schema.zh.md",
            "../../appendix/memory-retrieval-schema.zh.md",
            "../../appendix/incident-record-schema.zh.md",
        ),
    }

    for path, expected_links in expected_links_by_file.items():
        text = _read(path)
        for expected_link in expected_links:
            assert f"]({expected_link})" in text, (path, expected_link)


def test_chapter_25_control_evals_threads_three_canonical_cases() -> None:
    required_markers = (
        "Control-eval case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "eval gate and verifier contract",
        "eval schema",
        "behavioral and control eval surfaces",
        "payload-mutation check",
        "approval-path misuse check",
        "source-grounding eval",
        "retrieval-poisoning scenario",
        "notification suppression probe",
        "rollback control eval",
    )
    checked_files = (
        "docs/book/part-viii/chapter-25.md",
        "docs/book/part-viii/chapter-25.en.md",
        "docs/book/part-viii/chapter-25.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_chapter_25_useful_refs_include_control_surface_contracts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-25.md": (
            "[Схема approval](../../appendix/approval-schema.md)",
            "[Схема артефактов жизненного цикла]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[Схема памяти и извлечения]"
            "(../../appendix/memory-retrieval-schema.md)",
        ),
        "docs/book/part-viii/chapter-25.en.md": (
            "[Approval Schema](../../appendix/approval-schema.en.md)",
            "[Lifecycle Artifact Schema]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[Memory and Retrieval Schema]"
            "(../../appendix/memory-retrieval-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-25.zh.md": (
            "[Approval Schema](../../appendix/approval-schema.zh.md)",
            "[Lifecycle Artifact Schema]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[Memory and Retrieval Schema]"
            "(../../appendix/memory-retrieval-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_25_control_eval_case_spine_links_are_clickable() -> None:
    expected_links_by_file = {
        "docs/book/part-viii/chapter-25.md": (
            "../../appendix/eval-schema.md",
            "../../appendix/approval-schema.md",
            "../../appendix/memory-retrieval-schema.md",
            "../../appendix/incident-record-schema.md",
        ),
        "docs/book/part-viii/chapter-25.en.md": (
            "../../appendix/eval-schema.en.md",
            "../../appendix/approval-schema.en.md",
            "../../appendix/memory-retrieval-schema.en.md",
            "../../appendix/incident-record-schema.en.md",
        ),
        "docs/book/part-viii/chapter-25.zh.md": (
            "../../appendix/eval-schema.zh.md",
            "../../appendix/approval-schema.zh.md",
            "../../appendix/memory-retrieval-schema.zh.md",
            "../../appendix/incident-record-schema.zh.md",
        ),
    }

    for path, expected_links in expected_links_by_file.items():
        text = _read(path)
        for expected_link in expected_links:
            assert f"]({expected_link})" in text, (path, expected_link)


def test_chapter_26_observability_threads_three_canonical_cases() -> None:
    required_markers = (
        "Observability case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "trace and telemetry coverage record",
        "observability coverage",
        "ticket-write paths",
        "bypass blind spots",
        "retrieval provenance",
        "source-grounding verdicts",
        "verifier evidence",
        "notification delivery",
        "post-incident control changes",
    )
    checked_files = (
        "docs/book/part-viii/chapter-26.md",
        "docs/book/part-viii/chapter-26.en.md",
        "docs/book/part-viii/chapter-26.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_chapter_26_useful_refs_include_observability_contracts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-26.md": (
            "[Схема approval](../../appendix/approval-schema.md)",
            "[Схема артефактов жизненного цикла]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[Схема памяти и извлечения]"
            "(../../appendix/memory-retrieval-schema.md)",
        ),
        "docs/book/part-viii/chapter-26.en.md": (
            "[Approval Schema](../../appendix/approval-schema.en.md)",
            "[Lifecycle Artifact Schema]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[Memory and Retrieval Schema]"
            "(../../appendix/memory-retrieval-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-26.zh.md": (
            "[Approval Schema](../../appendix/approval-schema.zh.md)",
            "[Lifecycle Artifact Schema]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[Memory and Retrieval Schema]"
            "(../../appendix/memory-retrieval-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_26_observability_case_spine_links_are_clickable() -> None:
    expected_links_by_file = {
        "docs/book/part-viii/chapter-26.md": (
            "../../appendix/trace-schema.md",
            "../../appendix/approval-schema.md",
            "../../appendix/policy-bundle-schema.md",
            "../../appendix/memory-retrieval-schema.md",
            "../../appendix/incident-record-schema.md",
            "../../appendix/lifecycle-artifact-schema.md",
        ),
        "docs/book/part-viii/chapter-26.en.md": (
            "../../appendix/trace-schema.en.md",
            "../../appendix/approval-schema.en.md",
            "../../appendix/policy-bundle-schema.en.md",
            "../../appendix/memory-retrieval-schema.en.md",
            "../../appendix/incident-record-schema.en.md",
            "../../appendix/lifecycle-artifact-schema.en.md",
        ),
        "docs/book/part-viii/chapter-26.zh.md": (
            "../../appendix/trace-schema.zh.md",
            "../../appendix/approval-schema.zh.md",
            "../../appendix/policy-bundle-schema.zh.md",
            "../../appendix/memory-retrieval-schema.zh.md",
            "../../appendix/incident-record-schema.zh.md",
            "../../appendix/lifecycle-artifact-schema.zh.md",
        ),
    }

    for path, expected_links in expected_links_by_file.items():
        text = _read(path)
        for expected_link in expected_links:
            assert f"]({expected_link})" in text, (path, expected_link)


def test_chapter_26_verifier_evidence_eval_link_is_clickable() -> None:
    expected_links_by_file = {
        "docs/book/part-viii/chapter-26.md": "../../appendix/eval-schema.md",
        "docs/book/part-viii/chapter-26.en.md": "../../appendix/eval-schema.en.md",
        "docs/book/part-viii/chapter-26.zh.md": "../../appendix/eval-schema.zh.md",
    }

    for path, expected_link in expected_links_by_file.items():
        assert f"]({expected_link})" in _read(path), (path, expected_link)


def test_chapter_26_weak_evidence_layer_links_verifier_evidence() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-26.md": (
            "и [verifier evidence](../../appendix/eval-schema.md) о том"
        ),
        "docs/book/part-viii/chapter-26.en.md": (
            "and [verifier evidence](../../appendix/eval-schema.en.md) for how"
        ),
        "docs/book/part-viii/chapter-26.zh.md": (
            "[verifier evidence](../../appendix/eval-schema.zh.md)，那它也许"
        ),
    }

    for path, expected_snippet in expected_snippets_by_file.items():
        assert expected_snippet in _read(path), (path, expected_snippet)


def test_chapter_26_observability_breakages_link_verifier_evidence() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-26.md": (
            "[verifier evidence](../../appendix/eval-schema.md) оторван"
        ),
        "docs/book/part-viii/chapter-26.en.md": (
            "[verifier evidence](../../appendix/eval-schema.en.md) is detached"
        ),
        "docs/book/part-viii/chapter-26.zh.md": (
            "[verifier evidence](../../appendix/eval-schema.zh.md) 与 traces"
        ),
    }

    for path, expected_snippet in expected_snippets_by_file.items():
        assert expected_snippet in _read(path), (path, expected_snippet)


def test_chapter_26_maturity_bar_links_verifier_evidence() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-26.md": (
            "reviewed orchestration patterns и [verifier evidence]"
            "(../../appendix/eval-schema.md)"
        ),
        "docs/book/part-viii/chapter-26.en.md": (
            "reviewed orchestration patterns, and [verifier evidence]"
            "(../../appendix/eval-schema.en.md)"
        ),
        "docs/book/part-viii/chapter-26.zh.md": (
            "reviewed orchestration patterns 与 [verifier evidence]"
            "(../../appendix/eval-schema.zh.md)"
        ),
    }

    for path, expected_snippet in expected_snippets_by_file.items():
        assert expected_snippet in _read(path), (path, expected_snippet)


def test_chapter_26_practical_checklist_links_verifier_evidence() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-26.md": (
            "активным orchestration pattern и [verifier evidence]"
            "(../../appendix/eval-schema.md)"
        ),
        "docs/book/part-viii/chapter-26.en.md": (
            "active orchestration pattern, and [verifier evidence]"
            "(../../appendix/eval-schema.en.md)"
        ),
        "docs/book/part-viii/chapter-26.zh.md": (
            "当前 orchestration pattern 和 [verifier evidence]"
            "(../../appendix/eval-schema.zh.md)"
        ),
    }

    for path, expected_snippet in expected_snippets_by_file.items():
        assert expected_snippet in _read(path), (path, expected_snippet)


def test_chapter_26_evidence_model_links_verifier_evidence() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-26.md": (
            "artifacts и [verifier evidence](../../appendix/eval-schema.md)"
        ),
        "docs/book/part-viii/chapter-26.en.md": (
            "artifacts, and [verifier evidence](../../appendix/eval-schema.en.md)"
        ),
        "docs/book/part-viii/chapter-26.zh.md": (
            "artifacts 与 [verifier evidence](../../appendix/eval-schema.zh.md)"
        ),
    }

    for path, expected_snippet in expected_snippets_by_file.items():
        assert expected_snippet in _read(path), (path, expected_snippet)


def test_chapter_2_architecture_threads_three_canonical_cases() -> None:
    required_markers = (
        "Architecture case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "reference architecture",
        "ingress identity",
        "control plane",
        "approval gate",
        "tool gateway",
        "retrieval scope",
        "tenant boundary",
        "notification tool boundary",
    )
    checked_files = (
        "docs/book/part-i/chapter-2.md",
        "docs/book/part-i/chapter-2.en.md",
        "docs/book/part-i/chapter-2.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_chapter_1_platform_threads_three_canonical_cases() -> None:
    required_markers = (
        "Platform case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "platform, not magic",
        "ticket writes",
        "incident reconstruction",
        "retrieval scope",
        "source grounding",
        "tenant boundaries",
        "notification side effects",
        "governed execution system",
    )
    checked_files = (
        "docs/book/part-i/chapter-1.md",
        "docs/book/part-i/chapter-1.en.md",
        "docs/book/part-i/chapter-1.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_chapter_5_memory_risk_threads_three_canonical_cases() -> None:
    required_markers = (
        "Memory-risk case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "durable-state risks",
        "memory-write policy",
        "profile preference",
        "tenant isolation",
        "retrieval-memory split",
        "tenant-filter enforcement",
        "notification history provenance",
        "post-incident cleanup rules",
    )
    checked_files = (
        "docs/book/part-iii/chapter-5.md",
        "docs/book/part-iii/chapter-5.en.md",
        "docs/book/part-iii/chapter-5.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_memory_retrieval_schema_includes_poisoning_review_fields() -> None:
    required_markers = (
        "memory poisoning",
        "memory poisoning review fields",
        "write_trust_boundary",
        "untrusted_write",
        "activation_policy",
        "delayed_activation_review",
        "contamination_scope",
        "policy_influence",
        "provenance_check",
        "quarantine_state",
        "rollback_ref",
        "quarantine and rollback",
    )
    checked_files = (
        "docs/appendix/memory-retrieval-schema.md",
        "docs/appendix/memory-retrieval-schema.en.md",
        "docs/appendix/memory-retrieval-schema.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_chapter_5_memory_poisoning_scenario_is_documented() -> None:
    required_markers = (
        "memory poisoning",
        "memory poisoning review fields",
        "untrusted write",
        "delayed activation",
        "cross-tenant contamination",
        "policy influence",
        "provenance check",
        "quarantine and rollback",
        "threat-model review",
    )
    checked_files = (
        "docs/book/part-iii/chapter-5.md",
        "docs/book/part-iii/chapter-5.en.md",
        "docs/book/part-iii/chapter-5.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_chapter_5_memory_poisoning_schema_links_are_clickable() -> None:
    expected_links_by_file = {
        "docs/book/part-iii/chapter-5.md": (
            "../../appendix/memory-retrieval-schema.md",
            "../../appendix/trace-schema.md",
        ),
        "docs/book/part-iii/chapter-5.en.md": (
            "../../appendix/memory-retrieval-schema.en.md",
            "../../appendix/trace-schema.en.md",
        ),
        "docs/book/part-iii/chapter-5.zh.md": (
            "../../appendix/memory-retrieval-schema.zh.md",
            "../../appendix/trace-schema.zh.md",
        ),
    }

    for path, expected_links in expected_links_by_file.items():
        text = _read(path)
        for link in expected_links:
            assert f"]({link})" in text, (path, link)


def test_chapter_3_trust_boundaries_thread_three_canonical_cases() -> None:
    required_markers = (
        "Trust-boundary case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "read/decide/act split",
        "ticket writes",
        "retrieved documents",
        "source authority",
        "memory writes",
        "external notifications",
    )
    checked_files = (
        "docs/book/part-ii/chapter-3.md",
        "docs/book/part-ii/chapter-3.en.md",
        "docs/book/part-ii/chapter-3.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_chapter_23_retirement_threads_three_canonical_cases() -> None:
    required_markers = (
        "Retirement case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "deprecated write paths",
        "paused approvals",
        "verifier evidence",
        "stale corpora",
        "obsolete embeddings",
        "emergency-only capabilities",
        "notification channels",
    )
    checked_files = (
        "docs/book/part-viii/chapter-23.md",
        "docs/book/part-viii/chapter-23.en.md",
        "docs/book/part-viii/chapter-23.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)
    for path in checked_files:
        text = _read(path)
        assert "internal knowledge assistant" not in text, path
        assert "incident coordination" not in text, path


def test_chapter_23_retirement_verifier_evidence_eval_link_is_clickable() -> None:
    expected_links_by_file = {
        "docs/book/part-viii/chapter-23.md": "../../appendix/eval-schema.md",
        "docs/book/part-viii/chapter-23.en.md": "../../appendix/eval-schema.en.md",
        "docs/book/part-viii/chapter-23.zh.md": "../../appendix/eval-schema.zh.md",
    }

    for path, expected_link in expected_links_by_file.items():
        assert f"]({expected_link})" in _read(path), (path, expected_link)


def test_chapter_23_retirement_useful_refs_include_retirement_contracts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-23.md": (
            "[Схема approval](../../appendix/approval-schema.md)",
            "[Схема наборов для оценки и правил проверки]"
            "(../../appendix/eval-schema.md)",
            "[Схема памяти и извлечения]"
            "(../../appendix/memory-retrieval-schema.md)",
        ),
        "docs/book/part-viii/chapter-23.en.md": (
            "[Approval Schema](../../appendix/approval-schema.en.md)",
            "[Eval Dataset Schema and Grading Contract]"
            "(../../appendix/eval-schema.en.md)",
            "[Memory and Retrieval Schema]"
            "(../../appendix/memory-retrieval-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-23.zh.md": (
            "[Approval Schema](../../appendix/approval-schema.zh.md)",
            "[Eval Dataset Schema 与 Grading Contract]"
            "(../../appendix/eval-schema.zh.md)",
            "[Memory and Retrieval Schema]"
            "(../../appendix/memory-retrieval-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_23_retirement_breakages_link_verifier_evidence() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-23.md": (
            "obligations по [verifier evidence](../../appendix/eval-schema.md)"
        ),
        "docs/book/part-viii/chapter-23.en.md": (
            "[verifier evidence](../../appendix/eval-schema.en.md) obligations"
        ),
        "docs/book/part-viii/chapter-23.zh.md": (
            "[verifier evidence](../../appendix/eval-schema.zh.md) obligations"
        ),
    }

    for path, expected_snippet in expected_snippets_by_file.items():
        assert expected_snippet in _read(path), (path, expected_snippet)


def test_chapter_23_deprecated_inventory_links_control_contracts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-23.md": (
            "[approved inventory](../../appendix/registry-operations-handbook.md)",
            "[deprecated inventory](../../appendix/registry-operations-handbook.md)",
            "[deprecated capability contract]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[deprecated approval schema](../../appendix/approval-schema.md)",
            "[deprecated runtime-control schema]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[deprecated orchestration pattern или worker-boundary policy]"
            "(../../appendix/change-rollout-schema.md)",
            "[deprecated capability-session contract]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[deprecated verifier contract](../../appendix/eval-schema.md)",
        ),
        "docs/book/part-viii/chapter-23.en.md": (
            "[approved inventory](../../appendix/registry-operations-handbook.en.md)",
            "[deprecated inventory](../../appendix/registry-operations-handbook.en.md)",
            "[deprecated capability contract]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[deprecated approval schema](../../appendix/approval-schema.en.md)",
            "[deprecated runtime-control schema]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[deprecated orchestration pattern or worker-boundary policy]"
            "(../../appendix/change-rollout-schema.en.md)",
            "[deprecated capability-session contract]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[deprecated verifier contract](../../appendix/eval-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-23.zh.md": (
            "[已批准清单（approved inventory）]"
            "(../../appendix/registry-operations-handbook.zh.md)",
            "[已废弃清单（deprecated inventory）]"
            "(../../appendix/registry-operations-handbook.zh.md)",
            "[已废弃的能力契约](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[已废弃的 approval schema](../../appendix/approval-schema.zh.md)",
            "[已废弃的 runtime-control schema]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[已废弃的 orchestration pattern 或 worker-boundary policy]"
            "(../../appendix/change-rollout-schema.zh.md)",
            "[已废弃的 capability-session contract]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[已废弃的 verifier contract](../../appendix/eval-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_23_right_to_act_risks_link_retirement_contracts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-23.md": (
            "[active tool principal](../../appendix/lifecycle-artifact-schema.md)",
            "[доступ к memory](../../appendix/memory-retrieval-schema.md)",
            "[старый путь rollout](../../appendix/change-rollout-schema.md)",
            "[resumable paused approval path](../../appendix/approval-schema.md)",
            "[expired capability session, которую все еще можно re-initialize "
            "через старый path](../../appendix/lifecycle-artifact-schema.md)",
            "[старая runtime-control schema, которую gateways все еще принимают]"
            "(../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-23.en.md": (
            "[active tool principal](../../appendix/lifecycle-artifact-schema.en.md)",
            "[memory access](../../appendix/memory-retrieval-schema.en.md)",
            "[old rollout path](../../appendix/change-rollout-schema.en.md)",
            "[resumable paused approval path](../../appendix/approval-schema.en.md)",
            "[expired capability session that can still be re-initialized "
            "through an old path](../../appendix/lifecycle-artifact-schema.en.md)",
            "[old runtime-control schema still accepted by gateways]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-23.zh.md": (
            "[活跃的工具主体](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[记忆访问权](../../appendix/memory-retrieval-schema.zh.md)",
            "[旧的上线路径](../../appendix/change-rollout-schema.zh.md)",
            "[可恢复的 paused approval path](../../appendix/approval-schema.zh.md)",
            "[已过期但仍可通过旧路径 re-initialize 的 capability session]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[仍被 gateways 接受的旧 runtime-control schema]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_23_old_ticket_writer_example_links_retirement_controls() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-23.md": (
            "[закрыть tool principal](../../appendix/lifecycle-artifact-schema.md)",
            "[отозвать gateway exposure]"
            "(../../appendix/registry-operations-handbook.md)",
            "[истечь paused approvals](../../appendix/approval-schema.md)",
            "[остановить background retries]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[сохранить audit trail](../../appendix/trace-schema.md)",
        ),
        "docs/book/part-viii/chapter-23.en.md": (
            "[close the tool principal]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[revoke gateway exposure]"
            "(../../appendix/registry-operations-handbook.en.md)",
            "[expire paused approvals](../../appendix/approval-schema.en.md)",
            "[stop background retries]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[preserve the audit trail](../../appendix/trace-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-23.zh.md": (
            "[关闭工具主体](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[撤销 gateway exposure]"
            "(../../appendix/registry-operations-handbook.zh.md)",
            "[让 paused approvals 过期](../../appendix/approval-schema.zh.md)",
            "[停止后台重试](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[保留审计轨迹](../../appendix/trace-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_23_layered_retirement_checklist_links_control_surfaces() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-23.md": (
            "[остановить новые rollout waves](../../appendix/change-rollout-schema.md)",
            "[запретить risky capabilities]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[перевести write actions в approval-only или disable]"
            "(../../appendix/approval-schema.md)",
            "[остановить memory writes](../../appendix/memory-retrieval-schema.md)",
            "[истечь или отменить paused runs]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[отключить background jobs и background routes]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[закрыть или архивировать capability-session state и запретить "
            "uncontrolled re-init](../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-23.en.md": (
            "[stop new rollout waves](../../appendix/change-rollout-schema.en.md)",
            "[disable risky capabilities]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[move write actions to approval-only or disable them]"
            "(../../appendix/approval-schema.en.md)",
            "[stop memory writes](../../appendix/memory-retrieval-schema.en.md)",
            "[expire or cancel paused runs]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[stop background jobs and background routes]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[close or archive capability-session state and block uncontrolled "
            "re-init](../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-23.zh.md": (
            "[停止新的上线波次](../../appendix/change-rollout-schema.zh.md)",
            "[关闭高风险能力](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[把写入动作切到仅审批模式，或者直接停用]"
            "(../../appendix/approval-schema.zh.md)",
            "[停止记忆写入](../../appendix/memory-retrieval-schema.zh.md)",
            "[让 paused runs 过期或直接取消]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[停止后台任务与 background routes]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[关闭或归档 capability-session state，并阻断不受控的 re-init]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_23_layered_retirement_evidence_links_control_surfaces() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-23.md": (
            "[выключить deprecated orchestration patterns и отозвать worker-safe "
            "catalog exposure](../../appendix/change-rollout-schema.md)",
            "[отозвать delegated authorization paths]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[архивировать их final lineage](../../appendix/trace-schema.md)",
            "[вывести из эксплуатации deprecated verifier contracts и сохранить "
            "evidence, нужные для объяснения прежних rollout или assurance "
            "decisions](../../appendix/eval-schema.md)",
            "[`failure_reason`](../../appendix/eval-schema.md)",
            "[архивировать handoff artifacts, которые несли scope спринта, "
            "evaluator critique или решения на границе reset]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[отозвать egress access](../../appendix/lifecycle-artifact-schema.md)",
            "[закрыть principals, secrets и connectors]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[зафиксировать final audit state](../../appendix/trace-schema.md)",
        ),
        "docs/book/part-viii/chapter-23.en.md": (
            "[disable deprecated orchestration patterns and revoke worker-safe "
            "catalog exposure](../../appendix/change-rollout-schema.en.md)",
            "[revoke delegated authorization paths]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[archive their final lineage](../../appendix/trace-schema.en.md)",
            "[retire deprecated verifier contracts and preserve the evidence "
            "needed to explain prior rollout or assurance decisions]"
            "(../../appendix/eval-schema.en.md)",
            "[`failure_reason`](../../appendix/eval-schema.en.md)",
            "[archive handoff artifacts that carried sprint scope, evaluator "
            "critique, or reset-boundary decisions]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[revoke egress access](../../appendix/lifecycle-artifact-schema.en.md)",
            "[close principals, secrets, and connectors]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[record the final audit state](../../appendix/trace-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-23.zh.md": (
            "[停用已废弃的 orchestration patterns，并撤销 worker-safe catalog exposure]"
            "(../../appendix/change-rollout-schema.zh.md)",
            "[撤销 delegated authorization paths]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[归档它们最终的 lineage](../../appendix/trace-schema.zh.md)",
            "[退役已废弃的 verifier contracts，并保留解释既往 rollout 或保障决策所需的证据]"
            "(../../appendix/eval-schema.zh.md)",
            "[`failure_reason`](../../appendix/eval-schema.zh.md)",
            "[归档那些承载 sprint scope、evaluator critique 或 reset-boundary "
            "decisions 的 handoff artifacts]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[撤销出口访问](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[关闭主体、密钥和连接器]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[固化最终审计状态](../../appendix/trace-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_23_memory_audit_retention_links_state_contracts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-23.md": (
            "[что архивировать](../../appendix/lifecycle-artifact-schema.md)",
            "[что удалить](../../appendix/memory-retrieval-schema.md)",
            "[что anonymize](../../appendix/memory-retrieval-schema.md)",
            "[traces](../../appendix/trace-schema.md) и "
            "[approvals](../../appendix/approval-schema.md)",
            "[кто остается owner у archived state]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[datasets](../../appendix/eval-schema.md) и "
            "[memory artifacts](../../appendix/memory-retrieval-schema.md)",
            "[delegated authorization records]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[историю verifier contracts](../../appendix/eval-schema.md)",
        ),
        "docs/book/part-viii/chapter-23.en.md": (
            "[what to archive](../../appendix/lifecycle-artifact-schema.en.md)",
            "[what to delete](../../appendix/memory-retrieval-schema.en.md)",
            "[what to anonymize](../../appendix/memory-retrieval-schema.en.md)",
            "[traces](../../appendix/trace-schema.en.md) and "
            "[approvals](../../appendix/approval-schema.en.md)",
            "[who remains the owner of archived state]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[datasets](../../appendix/eval-schema.en.md) and "
            "[memory artifacts](../../appendix/memory-retrieval-schema.en.md)",
            "[delegated authorization records]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[verifier-contract history](../../appendix/eval-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-23.zh.md": (
            "[什么要归档](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[什么要删除](../../appendix/memory-retrieval-schema.zh.md)",
            "[什么要匿名化](../../appendix/memory-retrieval-schema.zh.md)",
            "[追踪](../../appendix/trace-schema.zh.md)和"
            "[审批](../../appendix/approval-schema.zh.md)",
            "[归档状态的负责人是谁]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[数据集](../../appendix/eval-schema.zh.md)和"
            "[记忆工件](../../appendix/memory-retrieval-schema.zh.md)",
            "[delegated authorization records]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[verifier-contract history](../../appendix/eval-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_23_staged_replacement_links_rollout_eval_lifecycle() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-23.md": (
            "[shadow comparison](../../appendix/eval-schema.md)",
            "[limited tenant migration](../../appendix/change-rollout-schema.md)",
            "[dual-run for critical scenarios]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[side-by-side evals](../../appendix/eval-schema.md)",
            "[staged traffic shift](../../appendix/change-rollout-schema.md)",
            "[final cutover only after confidence is high]"
            "(../../appendix/change-rollout-schema.md)",
        ),
        "docs/book/part-viii/chapter-23.en.md": (
            "[shadow comparison](../../appendix/eval-schema.en.md)",
            "[limited tenant migration](../../appendix/change-rollout-schema.en.md)",
            "[dual-run for critical scenarios]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[side-by-side evals](../../appendix/eval-schema.en.md)",
            "[staged traffic shift](../../appendix/change-rollout-schema.en.md)",
            "[final cutover only after confidence is high]"
            "(../../appendix/change-rollout-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-23.zh.md": (
            "[影子对比](../../appendix/eval-schema.zh.md)",
            "[小范围租户迁移](../../appendix/change-rollout-schema.zh.md)",
            "[在关键场景里双运行](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[并行评测](../../appendix/eval-schema.zh.md)",
            "[分阶段切流](../../appendix/change-rollout-schema.zh.md)",
            "[只有在信心足够时才做最终切换]"
            "(../../appendix/change-rollout-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_23_breakage_list_links_retirement_control_surfaces() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-23.md": (
            "[principals еще живы](../../appendix/lifecycle-artifact-schema.md)",
            "[background jobs забыли выключить]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[memory write path остался активным]"
            "(../../appendix/memory-retrieval-schema.md)",
            "[paused approvals остались resumable после retirement]"
            "(../../appendix/approval-schema.md)",
            "[expired capability sessions все еще можно re-initialize через "
            "stale control paths](../../appendix/lifecycle-artifact-schema.md)",
            "[deprecated orchestration patterns или worker-boundary policies "
            "остаются рабочими после retirement]"
            "(../../appendix/change-rollout-schema.md)",
        ),
        "docs/book/part-viii/chapter-23.en.md": (
            "[principals are still active]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[background jobs were forgotten]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[memory write path remained live]"
            "(../../appendix/memory-retrieval-schema.en.md)",
            "[paused approvals were left resumable after retirement]"
            "(../../appendix/approval-schema.en.md)",
            "[expired capability sessions could still be re-initialized through "
            "stale control paths](../../appendix/lifecycle-artifact-schema.en.md)",
            "[deprecated orchestration patterns or worker-boundary policies "
            "remained usable after retirement]"
            "(../../appendix/change-rollout-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-23.zh.md": (
            "[主体还活着](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[后台任务没关](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[记忆写入路径仍然在工作]"
            "(../../appendix/memory-retrieval-schema.zh.md)",
            "[paused approvals 在退役之后仍然可以恢复]"
            "(../../appendix/approval-schema.zh.md)",
            "[已过期 capability sessions 仍可通过陈旧控制路径 re-initialize]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[已废弃的 orchestration patterns 或 worker-boundary policies 在退役后仍然可用]"
            "(../../appendix/change-rollout-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_23_breakage_list_links_retirement_completion_controls() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-23.md": (
            "[background routes забыли выключить]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[archived state никому не принадлежит]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[deprecated schemas все еще принимаются gateways или runtime]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[deprecated patterns остаются рабочими слишком долго]"
            "(../../appendix/change-rollout-schema.md)",
            "[dual-run](../../appendix/lifecycle-artifact-schema.md) или "
            "[staged migration](../../appendix/change-rollout-schema.md)",
        ),
        "docs/book/part-viii/chapter-23.en.md": (
            "[background routes were forgotten]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[archived state belongs to nobody]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[deprecated schemas still remain accepted by gateways or runtimes]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[deprecated patterns remain usable too long]"
            "(../../appendix/change-rollout-schema.en.md)",
            "[dual-run](../../appendix/lifecycle-artifact-schema.en.md) or "
            "[staged migration](../../appendix/change-rollout-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-23.zh.md": (
            "[background routes 被遗忘没有关闭]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[归档状态没有负责人]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[已废弃的 schemas 仍然被 gateways 或 runtimes 接受]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[已废弃模式存活太久]"
            "(../../appendix/change-rollout-schema.zh.md)",
            "[双运行](../../appendix/lifecycle-artifact-schema.zh.md)或"
            "[分阶段迁移](../../appendix/change-rollout-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_27_registry_threads_three_canonical_cases() -> None:
    required_markers = (
        "Registry case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "write-capability owners",
        "approval mode",
        "retirement plan",
        "verifier evidence",
        "corpus owners",
        "freshness review",
        "incident-role owners",
        "lifecycle state",
    )
    checked_files = (
        "docs/book/part-viii/chapter-27.md",
        "docs/book/part-viii/chapter-27.en.md",
        "docs/book/part-viii/chapter-27.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_chapter_27_useful_refs_include_registry_evidence_contracts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-27.md": (
            "[Схема наборов для оценки и правил проверки]"
            "(../../appendix/eval-schema.md)",
            "[Схема памяти и извлечения]"
            "(../../appendix/memory-retrieval-schema.md)",
        ),
        "docs/book/part-viii/chapter-27.en.md": (
            "[Eval Dataset Schema and Grading Contract]"
            "(../../appendix/eval-schema.en.md)",
            "[Memory and Retrieval Schema]"
            "(../../appendix/memory-retrieval-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-27.zh.md": (
            "[Eval Dataset Schema 与 Grading Contract]"
            "(../../appendix/eval-schema.zh.md)",
            "[Memory and Retrieval Schema]"
            "(../../appendix/memory-retrieval-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_27_registry_case_spine_links_are_clickable() -> None:
    expected_links_by_file = {
        "docs/book/part-viii/chapter-27.md": (
            "../../appendix/eval-schema.md",
            "../../appendix/registry-operations-handbook.md",
            "../../appendix/approval-schema.md",
            "../../appendix/lifecycle-artifact-schema.md",
            "../../appendix/memory-retrieval-schema.md",
        ),
        "docs/book/part-viii/chapter-27.en.md": (
            "../../appendix/eval-schema.en.md",
            "../../appendix/registry-operations-handbook.en.md",
            "../../appendix/approval-schema.en.md",
            "../../appendix/lifecycle-artifact-schema.en.md",
            "../../appendix/memory-retrieval-schema.en.md",
        ),
        "docs/book/part-viii/chapter-27.zh.md": (
            "../../appendix/eval-schema.zh.md",
            "../../appendix/registry-operations-handbook.zh.md",
            "../../appendix/approval-schema.zh.md",
            "../../appendix/lifecycle-artifact-schema.zh.md",
            "../../appendix/memory-retrieval-schema.zh.md",
        ),
    }

    for path, expected_links in expected_links_by_file.items():
        text = _read(path)
        for expected_link in expected_links:
            assert f"]({expected_link})" in text, (path, expected_link)


def test_chapter_20_useful_refs_include_change_rollout_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-20.md": (
            "[Схема change review и rollout gate]"
            "(../../appendix/change-rollout-schema.md)"
        ),
        "docs/book/part-viii/chapter-20.en.md": (
            "[Change Review and Rollout Gate Schema]"
            "(../../appendix/change-rollout-schema.en.md)"
        ),
        "docs/book/part-viii/chapter-20.zh.md": (
            "[Change Review and Rollout Gate Schema]"
            "(../../appendix/change-rollout-schema.zh.md)"
        ),
    }

    for path, expected_snippet in expected_snippets_by_file.items():
        assert expected_snippet in _read(path), (path, expected_snippet)


def test_chapter_20_change_packets_thread_three_canonical_cases() -> None:
    required_markers = (
        "Change case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "approval rules",
        "write capabilities",
        "retrieval corpus",
        "freshness windows",
        "memory write semantics",
        "incident state",
    )
    checked_files = (
        "docs/book/part-viii/chapter-20.md",
        "docs/book/part-viii/chapter-20.en.md",
        "docs/book/part-viii/chapter-20.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_chapter_20_change_case_spine_links_are_clickable() -> None:
    expected_links_by_file = {
        "docs/book/part-viii/chapter-20.md": (
            "../../appendix/approval-schema.md",
            "../../appendix/memory-retrieval-schema.md",
            "../../appendix/incident-record-schema.md",
        ),
        "docs/book/part-viii/chapter-20.en.md": (
            "../../appendix/approval-schema.en.md",
            "../../appendix/memory-retrieval-schema.en.md",
            "../../appendix/incident-record-schema.en.md",
        ),
        "docs/book/part-viii/chapter-20.zh.md": (
            "../../appendix/approval-schema.zh.md",
            "../../appendix/memory-retrieval-schema.zh.md",
            "../../appendix/incident-record-schema.zh.md",
        ),
    }

    for path, expected_links in expected_links_by_file.items():
        text = _read(path)
        for expected_link in expected_links:
            assert f"]({expected_link})" in text, (path, expected_link)


def test_chapter_7_retrieval_threads_three_canonical_cases() -> None:
    required_markers = (
        "Retrieval case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "current ticket state",
        "source attribution",
        "freshness windows",
        "tenant filters",
        "stale-index detection",
        "durable lessons",
    )
    checked_files = (
        "docs/book/part-iii/chapter-7.md",
        "docs/book/part-iii/chapter-7.en.md",
        "docs/book/part-iii/chapter-7.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)
    for path in checked_files:
        text = _read(path)
        assert "internal knowledge assistant" not in text, path
        assert "incident coordination" not in text, path


def test_chapter_6_memory_threads_three_canonical_cases() -> None:
    required_markers = (
        "Memory case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "temporary ticket state",
        "source provenance",
        "freshness",
        "tenant boundaries",
        "handoff summaries",
        "post-incident lessons",
    )
    checked_files = (
        "docs/book/part-iii/chapter-6.md",
        "docs/book/part-iii/chapter-6.en.md",
        "docs/book/part-iii/chapter-6.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_chapter_4_gateway_threads_three_canonical_cases() -> None:
    required_markers = (
        "Gateway case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "governed writes",
        "scoped reads",
        "retrieval limits",
        "escalation tools",
        "notification tools",
        "incident state",
    )
    checked_files = (
        "docs/book/part-ii/chapter-4.md",
        "docs/book/part-ii/chapter-4.en.md",
        "docs/book/part-ii/chapter-4.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)
    for path in checked_files:
        text = _read(path)
        assert "internal knowledge assistant" not in text, path
        assert "incident coordination" not in text, path


def test_chapter_13_eval_suite_threads_three_canonical_cases() -> None:
    required_markers = (
        "Eval case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "duplicate tickets",
        "retrieval freshness",
        "memory provenance",
        "escalation timing",
        "response ownership",
        "regression cases",
    )
    checked_files = (
        "docs/book/part-v/chapter-13.md",
        "docs/book/part-v/chapter-13.en.md",
        "docs/book/part-v/chapter-13.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_chapter_13_verifier_verdict_schema_links_are_clickable() -> None:
    expected_links_by_file = {
        "docs/book/part-v/chapter-13.md": (
            "../../appendix/eval-schema.md",
            "../../appendix/trace-schema.md",
        ),
        "docs/book/part-v/chapter-13.en.md": (
            "../../appendix/eval-schema.en.md",
            "../../appendix/trace-schema.en.md",
        ),
        "docs/book/part-v/chapter-13.zh.md": (
            "../../appendix/eval-schema.zh.md",
            "../../appendix/trace-schema.zh.md",
        ),
    }

    for path, expected_links in expected_links_by_file.items():
        text = _read(path)
        for link in expected_links:
            assert f"]({link})" in text, (path, link)


def test_evidence_spine_threads_three_canonical_cases() -> None:
    required_markers = (
        "Case-spine routing note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "approvals",
        "retrieval provenance",
        "response ownership",
        "post-incident rollout judgment",
    )
    deprecated_markers = (
        "support-triage agent",
        "internal knowledge assistant stresses",
        "incident coordination stresses",
    )
    checked_files = (
        "docs/book/part-v/evidence-spine.md",
        "docs/book/part-v/evidence-spine.en.md",
        "docs/book/part-v/evidence-spine.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)
    for path in checked_files:
        text = _read(path)
        for marker in deprecated_markers:
            assert marker not in text, (path, marker)


def test_chapter_1_decision_frame_is_print_friendly() -> None:
    chapter_sections = {
        "docs/book/part-i/chapter-1.md": ("## 6.", "## 7.", "Быстрый выбор"),
        "docs/book/part-i/chapter-1.en.md": ("## 6.", "## 7.", "Fast decision"),
        "docs/book/part-i/chapter-1.zh.md": ("## 6.", "## 7.", "快速判断"),
    }

    for path, (start_marker, end_marker, title_marker) in chapter_sections.items():
        text = _read(path)
        section = text.split(start_marker, 1)[1].split(end_marker, 1)[0]
        assert title_marker in section
        assert "|" not in section
        assert "workflow" in section
        assert "single-agent loop" in section
        assert "multi-agent" in section


def test_chapter_2_layer_map_is_print_friendly() -> None:
    chapter_sections = {
        "docs/book/part-i/chapter-2.md": ("## 4.", "## 5.", "Входной слой"),
        "docs/book/part-i/chapter-2.en.md": ("## 4.", "## 5.", "Interface layer"),
        "docs/book/part-i/chapter-2.zh.md": ("## 4.", "## 5.", "接口层"),
    }

    for path, (start_marker, end_marker, title_marker) in chapter_sections.items():
        text = _read(path)
        section = text.split(start_marker, 1)[1].split(end_marker, 1)[0]
        assert title_marker in section
        assert "|" not in section
        assert "control" in section or "управления" in section or "控制" in section
        assert "runtime" in section or "рантайм" in section or "运行时" in section
        assert "Telemetry" in section or "Телеметрия" in section or "遥测" in section


def test_reference_final_rule_stays_as_separate_bullet_list() -> None:
    expected = {
        "docs/reference.md": (
            "Самое простое правило такое:\n\n- книгу используй",
            "- справочный слой используй",
        ),
        "docs/reference.en.md": (
            "The simplest rule is:\n\n- use the book",
            "- use the reference layer",
        ),
        "docs/reference.zh.md": (
            "最简单的规则是：\n\n- 用本书",
            "- 用参考层",
        ),
    }

    for path, markers in expected.items():
        text = _read(path)
        for marker in markers:
            assert marker in text, (path, marker)


def test_russian_reference_fast_topic_routes_are_localized() -> None:
    text = _read("docs/reference.md")

    assert "Каталог инструментов, семантическая фильтрация инструментов" in text
    assert "классификация чтения/записи" in text
    assert "Роли MCP: `host`, `client` и `server`" in text
    assert "Семантический разрыв (`semantic gap`), `HyDE`" in text
    assert "выбор между RAG и обучением модели (`RAG vs training`)" in text
    assert "Бюджет задержки (`latency budget`)" in text
    assert "быстрый/медленный путь и маршрутизированные конвейеры" in text
    assert "Оценка через `LLM-as-a-judge`, калибровка" in text
    assert "согласие судьи с человеком (`judge-human agreement`)" in text

    forbidden_markers = (
        "- Tool catalog, semantic tool filtering, read/write taxonomy:",
        "- MCP host/client/server, capability transport, sandbox boundary:",
        "- Semantic gap, HyDE, RAG vs training:",
        "- Latency budget, fast path / slow path, routed pipeline:",
        "- LLM-as-a-judge, calibration и judge-human agreement:",
    )

    for marker in forbidden_markers:
        assert marker not in text, marker


def test_english_book_plan_matches_home_publication_status() -> None:
    required_markers = (
        "Current publication status",
        "RU core manuscript",
        "published across eight book parts",
        "EN translation layer",
        "readable draft in editorial cleanup",
        "ZH translation layer",
        "readable draft localization preview in editorial cleanup",
        "Reference layer",
        "active companion material",
        "Runtime package",
        "runnable reference implementation and examples, not a production framework",
        "Publisher package",
        "in progress",
        "not a finished submission packet",
    )
    deprecated_markers = (
        "first chapter is published",
        "First chapter is published",
        "first part",
        "First part",
        "first set of practical case studies",
        "source base for the next chapters",
    )

    plan = _read("docs/book/plan.en.md")
    home = _read("docs/index.en.md")

    for marker in required_markers:
        assert marker in plan
    assert "Published Russian core manuscript across eight book parts" in home
    assert "Draft `en` and `zh` translation layers" in home
    for marker in deprecated_markers:
        assert marker not in plan


def test_whats_new_publisher_readiness_claim_stays_scoped() -> None:
    expected_by_file = {
        "docs/whats-new.md": (
            "Актуально на 20 мая 2026 года",
            "Издательский проход качества идет, но еще не закрыт полностью.",
            "черновые и плановые страницы исключены из опубликованного сайта",
            "исключены из опубликованного сайта и карты сайта (sitemap)",
            "метаданные для OpenGraph и Twitter и изображение для предпросмотра в соцсетях",
            "проверены поисковый индекс, карта сайта (sitemap), файл robots, "
            "локальные ресурсы, якоря",
            "альтернативный текст (alt text) и внешние ссылки",
            "резервные канонические редиректы (canonical) покрывают основные точки входа",
            "запись о доступности публичных ссылок обновлена 20 мая 2026 года",
            "все девять ссылок из издательского пакета вернули HTTP 200",
            "реестр блокеров, журнал решений/исключений, ограничение длины строк",
            "названия издательского пакета устойчивы для печати и экспорта",
            "карта ролей части VIII теперь устойчива для печати",
            "файлы README на трех языках теперь содержат чек-лист быстрой синхронизации публикации",
            "До статуса готовности к публикации еще остаются",
            "проверка слоев EN/ZH",
            "независимая проверка качества (QA) HTML/PDF и экспорта",
            "редакционная полировка глав-образцов",
            "упаковка печатной рукописи/онлайн-компаньона под конкретного издателя",
            "не выглядеть как черновая сборка из файлов Markdown",
        ),
        "docs/whats-new.en.md": (
            "Current as of May 20, 2026",
            "The publisher-facing quality pass is in progress, not fully closed.",
            "draft and planning pages are excluded from the published site",
            "OpenGraph/Twitter metadata and a social preview image",
            "search index, sitemap, robots file",
            "canonical fallback redirects cover the main hand-copied entry points",
            "public-link availability record was refreshed on May 20, 2026",
            "all nine publisher-packet links returned HTTP 200",
            "line-length guard, and packet labels are print/export-friendly",
            "Part VIII role map is now print-friendly",
            "Remaining before this can be called publisher-ready",
            "deep EN/ZH cleanup",
            "independent rendering/export QA",
            "sample-chapter polish",
        ),
        "docs/whats-new.zh.md": (
            "更新于 2026 年 5 月 20 日",
            "### 发布前站点表面更干净",
            "面向出版的质量检查正在进行中，但还没有完全关闭。",
            "已完成的站点工作：",
            "草稿与规划页面已从发布站点和站点地图（sitemap）中排除",
            "OpenGraph/Twitter 元数据和社交预览图（social preview image）",
            "检查了搜索索引（search index）、站点地图（sitemap）、robots 文件（robots file）",
            "本地资源（local assets）、锚点（anchors）",
            "图片替代文本（alt text）和外部链接（external links）",
            "基础导航和规范备用重定向（canonical fallback redirects）"
            "已覆盖人们最容易手动复制的主要入口",
            "公共链接可用性记录（public-link availability record）已在 2026 年 5 月 20 日刷新",
            "出版材料包（publisher packet）中的九个链接全部返回 HTTP 200",
            "出版材料包（publisher packet）的阻塞项登记表（blocker register）",
            "豁免与决策日志（waiver/decision log）",
            "行长限制（line-length guard）与材料包标签（packet labels）现在都适合打印和导出",
            "第 VIII 部分角色图（role map）现在适合打印和导出",
            "快速同步发布检查清单（quick sync publish checklist）",
            "在称为出版就绪之前",
            "EN/ZH 清理（deep EN/ZH cleanup）",
            "独立 HTML/PDF 渲染/导出质量检查（independent rendering/export QA）",
            "样章打磨（sample-chapter polish）",
            "面向具体出版社的纸质稿件与在线配套材料包装",
            "publisher-specific print/companion packaging",
        ),
    }
    forbidden = (
        "publisher-facing layer is fully closed",
        "publisher-facing слой полностью закрыт",
        "面向出版的质量层已经完全关闭",
        "### 发布前站点更干净了",
        "已经完成：",
        "Current as of May 19, 2026",
        "исключены из опубликованного сайта и sitemap",
        "Актуально на 19 мая 2026 года",
        "更新于 2026 年 5 月 19 日",
        "canonical fallback redirects покрывают основные entry points",
        "сырая сборка из Markdown-файлов",
        "сырая сборка из файлов Markdown",
        "резервные canonical redirects покрывают основные точки входа",
        "резервные canonical-редиректы покрывают основные точки входа",
        "basic navigation 和 canonical fallback redirects",
        "publisher-packet links вернули HTTP 200",
        "publisher packet вернули HTTP 200",
        "названия publisher packet устойчивы",
        "九个 publisher-packet links 全部返回 HTTP 200",
        "九个 publisher packet 链接全部返回 HTTP 200",
        "公共链接可用性记录已在 2026 年 5 月 20 日刷新",
        "печати/export",
        "打印/export",
        "打印/导出",
        "第 VIII 部分角色图现在适合打印导出",
        "第 VIII 部分角色图现在适合打印和导出",
        "role map части VIII",
        "Part VIII 角色图",
        "checklist быстрой синхронизации публикации",
        "快速同步发布检查清单。",
        "README на трех языках теперь содержит чек-лист",
        "OpenGraph/Twitter metadata и социальная preview-картинка",
        "метаданные OpenGraph/Twitter и изображение для социальных превью",
        "социальная превью-картинка",
        "изображение для социальных превью",
        "проверены search index, sitemap, robots",
        "проверены поисковый индекс, sitemap, robots, локальные ресурсы",
        "проверены поисковый индекс, sitemap, файл robots",
        "локальные assets",
        "локальные ресурсы, anchors, alt text",
        "локальные ресурсы, якоря, alt-тексты",
        "альтернативные тексты (alt text)",
        "EN/ZH-проверка",
        "проверка EN/ZH-слоев",
        "EN/ZH-слоев",
        "深层 EN/ZH 清理、",
        "независимый HTML/PDF/export QA",
        "независимый QA HTML/PDF/экспорта",
        "независимая проверка качества (QA) HTML/PDF/экспорта",
        "blocker register, waiver/decision log, ограничение длины строк",
        "publisher packet blocker register、waiver/decision log",
        "реестр блокеров, waiver/decision log",
        "publisher packet 阻塞项登记表、waiver/decision log",
        "publisher packet 中的九个链接全部返回 HTTP 200",
        "publisher packet 阻塞项登记表、豁免/决策日志、行长限制",
        "出版材料包（publisher packet）的阻塞项登记表、豁免/决策日志、行长限制",
        "出版材料包（publisher packet）的阻塞项登记表、豁免与决策日志、行长限制",
        "阻塞项登记表（blocker register）、豁免与决策日志、行长限制",
        "豁免与决策日志（waiver/decision log）、行长限制与材料包标签",
        "packet 标签现在都适合打印和导出",
        "OpenGraph/Twitter metadata 和社交预览图",
        "OpenGraph/Twitter 元数据和社交预览图；",
        "robots 文件、本地资源、锚点",
        "robots 文件、本地资源（local assets）",
        "草稿与规划页面已从发布站点和 sitemap 中排除",
        "检查了搜索索引、sitemap、robots",
        "检查了搜索索引、站点地图（sitemap）",
        "图片 alt 文本和外部链接",
        "图片替代文本（alt text）和外部链接；",
        "独立 HTML/PDF/export QA",
        "独立 HTML/PDF/导出 QA",
        "独立 HTML/PDF/导出质量检查（QA）",
        "基础导航和 canonical fallback redirects 已覆盖",
        "基础导航和 canonical 备用重定向已覆盖",
        "面向具体出版社的纸质稿件/在线配套材料包装",
        "面向具体出版社的纸质稿件与在线配套材料包装。",
        "独立 HTML/PDF 渲染/导出质量检查（independent rendering/export QA）、样章打磨，",
    )

    for path, expected_markers in expected_by_file.items():
        text = _read(path)
        for marker in expected_markers:
            assert marker in text, (path, marker)
        for marker in forbidden:
            assert marker not in text, (path, marker)


def test_russian_whats_new_intro_note_is_localized() -> None:
    text = _read("docs/whats-new.md")

    assert "крупных улучшений книги и эталонного пакета" in text
    assert "не заменяет историю Git" in text
    assert "как развивается проект и какие слои уже появились" in text
    assert "крупных улучшений книги и опорного пакета" not in text
    assert "насколько проект живой и какие слои уже появились" not in text
    assert "не заменяет git history" not in text


def test_chinese_whats_new_intro_note_is_localized() -> None:
    text = _read("docs/whats-new.zh.md")

    assert "Git 历史记录（Git history）的替代品" in text
    assert "不是 Git 历史的替代品" not in text


def test_russian_whats_new_section_headings_are_localized() -> None:
    text = _read("docs/whats-new.md")

    expected_headings = (
        "## Книга",
        "## Справочный слой",
        "## Эталонная среда исполнения",
        "## Практическое приложение",
        "## Навигация",
        "## Готовность к публикации",
    )
    stale_headings = (
        "## Book",
        "## Reference",
        "## Runtime",
        "## Practical Appendix",
        "## Navigation",
        "## Publish readiness",
    )

    for heading in expected_headings:
        assert heading in text
    for heading in stale_headings:
        assert heading not in text


def test_russian_whats_new_runtime_heading_is_localized() -> None:
    text = _read("docs/whats-new.md")

    assert "### Возможности эталонной среды исполнения (runtime)" in text
    assert "### Runnable reference runtime" not in text
    assert "### Исполняемый эталонный runtime" not in text
    assert "### Исполняемая эталонная среда исполнения (runtime)" not in text


def test_russian_whats_new_reader_value_note_is_localized() -> None:
    text = _read("docs/whats-new.md")

    assert "Можно читать книгу как практическое руководство." in text
    assert "Можно использовать справочные страницы как инженерные заготовки." in text
    assert "Можно запускать примерный исполняемый пакет, а не только читать файлы Markdown." in text
    assert "Можно читать книгу как handbook." not in text
    assert "Можно использовать reference pages как инженерные заготовки." not in text
    assert "Можно запускать примерный runtime, а не только читать Markdown." not in text
    assert "Можно запускать примерный исполняемый пакет, а не только читать Markdown." not in text
    assert (
        "Можно запускать примерный исполняемый пакет, а не только читать Markdown-файлы."
        not in text
    )


def test_russian_whats_new_canonical_case_note_is_localized() -> None:
    text = _read("docs/whats-new.md")

    assert '!!! note "Обновление канонических сценариев"' in text
    assert "сквозная карта трех канонических сценариев (canonical cases)" in text
    assert "Триаж обращений поддержки (Support triage)" in text
    assert "внутренний ассистент знаний (Internal knowledge assistant)" in text
    assert "координация инцидентов (Incident coordination)" in text
    assert "главах книги" in text
    assert "публичных точках входа" in text
    assert "справочных страницах" in text
    assert "артефактах приложений" in text
    assert "проверки покрытия защищают главы и страницы приложений" in text
    assert '!!! note "Canonical case update"' not in text
    assert '!!! note "Обновление canonical cases"' not in text
    assert "сквозная карта трех canonical cases" not in text
    assert "**Support triage**, **Internal knowledge assistant**" not in text
    assert "book chapters" not in text
    assert "public entry points" not in text
    assert "reference pages" not in text
    assert "appendix artifacts" not in text
    assert "chapters и appendix pages" not in text
    assert "coverage guards" not in text


def test_russian_whats_new_safe_agent_note_is_localized() -> None:
    text = _read("docs/whats-new.md")

    assert '!!! note "Обновление схем безопасного агента (safe-agent)"' in text
    assert (
        "связали прозу, приложения и защитные проверки для архитектуры "
        "безопасного агента (`safe-agent`)"
        in text
    )
    assert "модель угроз для MCP и контракт `mcp_server`" in text
    assert "контракт доверия для передачи управления A2A (handoff)" in text
    assert "артефакт делегирования доверия (trust-delegation)" in text
    assert "карта эшелонированной защиты (defense-in-depth)" in text
    assert "запись вердикта проверяющего (verifier verdict)" in text
    assert "запись управленческого действия (governance action)" in text
    assert "сопоставление телеметрии с NIST AI RMF" in text
    assert "поля проверки отравления памяти (memory poisoning)" in text
    assert "единая модель доказательств угроз агентам (evidence)" in text
    assert "[схеме trace](appendix/trace-schema.md)" in text
    assert "[схеме eval](appendix/eval-schema.md)" in text
    assert "[схеме memory/retrieval](appendix/memory-retrieval-schema.md)" in text
    assert '!!! note "Safe-agent schema update"' not in text
    assert '!!! note "Обновление safe-agent схем"' not in text
    assert '!!! note "Обновление схем safe-agent"' not in text
    assert "защитные проверки для safe-agent архитектуры" not in text
    assert "защитные проверки для архитектуры safe-agent" not in text
    assert "связали prose, appendices и guards" not in text
    assert "связали прозу, приложения и guards" not in text
    assert "MCP threat model и `mcp_server` contract" not in text
    assert "модель угроз MCP и контракт `mcp_server`" not in text
    assert "A2A handoff trust contract" not in text
    assert "контракт доверия для A2A handoff" not in text
    assert "контракт доверия для передачи A2A (handoff)" not in text
    assert "trust-delegation artifact" not in text
    assert "артефакт trust-delegation" not in text
    assert "defense-in-depth control map" not in text
    assert "карта defense-in-depth controls" not in text
    assert "карта defense-in-depth-контролей" not in text
    assert "verifier verdict record" not in text
    assert "запись verifier verdict" not in text
    assert "governance action record" not in text
    assert "запись governance action" not in text
    assert "NIST AI RMF telemetry mapping" not in text
    assert "сопоставление телеметрии NIST AI RMF" not in text
    assert "memory poisoning review fields" not in text
    assert "поля проверки memory poisoning" not in text
    assert "unified agent threat evidence" not in text
    assert "единая evidence-модель угроз агентам" not in text
    assert "[trace schema](appendix/trace-schema.md)" not in text
    assert "[eval schema](appendix/eval-schema.md)" not in text
    assert "[memory/retrieval schema](appendix/memory-retrieval-schema.md)" not in text


def test_russian_whats_new_book_note_is_localized() -> None:
    text = _read("docs/whats-new.md")

    assert "пакет замечаний издательской проверки качества (QA)" in text
    assert "рамка принятия решений в Главе 1" in text
    assert "для HTML/PDF и извлечения в простой текст" in text
    assert "часто обновляемые главы, «Источники» и «Что нового»" in text
    assert "особенностей отображения таблиц" in text
    assert "подвижные разделы по безопасности агентов" in text
    assert "издательского QA" not in text
    assert "decision frame в Главе 1" not in text
    assert "для HTML/PDF/plain-text extraction" not in text
    assert "извлечения в plain text" not in text
    assert "fast-moving главы" not in text
    assert "быстро меняющиеся главы" not in text
    assert "Sources и What’s New" not in text
    assert "agent-security разделы" not in text
    assert "особенностей рендера таблиц" not in text


def test_chinese_whats_new_book_note_is_localized() -> None:
    text = _read("docs/whats-new.zh.md")

    assert "### 2026 年 5 月 14 日编辑质量检查（QA）" in text
    assert "第一组出版就绪质量检查（QA）问题已经关闭" in text
    assert "更适合 HTML/PDF 与纯文本抽取的文字块" in text
    assert "快速变化的智能体安全（agent-security）章节" in text
    assert "### 2026 年 5 月 14 日编辑 QA" not in text
    assert "第一组出版就绪 QA 问题已经关闭" not in text
    assert "HTML/PDF/纯文本抽取" not in text
    assert "快速变化的 agent-security 章节" not in text


def test_chinese_whats_new_lifecycle_note_is_localized() -> None:
    text = _read("docs/whats-new.zh.md")

    assert "从软件开发生命周期到智能体开发生命周期（`SDLC→ADLC`）的迁移" in text
    assert "AI 原生（`AI-native`）可观测性" in text
    assert "现在全书已经包含 `SDLC→ADLC`、变更管理" not in text
    assert "AI 原生可观测性" not in text


def test_russian_whats_new_lifecycle_note_is_localized() -> None:
    text = _read("docs/whats-new.md")

    assert "Часть VIII про жизненный цикл агентной системы" in text
    assert "переход от `SDLC` к `ADLC`" in text
    assert "управление изменениями" in text
    assert "контур обеспечения доверия (assurance)" in text
    assert "цепочку поставки" in text
    assert "вывод из эксплуатации" in text
    assert "расхождение целей (misalignment)" in text
    assert "поведенческие оценки (evals)" in text
    assert (
        "наблюдаемость систем, изначально ориентированных на AI "
        "(`AI-native`, observability)"
        in text
    )
    assert "контроль инвентаризации (inventory)" in text
    assert "change management" not in text
    assert "блок про `SDLC -> ADLC`" not in text
    assert "assurance loop" not in text
    assert "контур assurance" not in text
    assert "supply chain" not in text
    assert "retirement" not in text
    assert "вывод из эксплуатации, misalignment" not in text
    assert "behavioral evals" not in text
    assert "поведенческие evals" not in text
    assert "AI-native observability" not in text
    assert "AI-native-наблюдаемость (observability)" not in text
    assert "наблюдаемость AI-native-систем (observability)" not in text
    assert "inventory control" not in text
    assert "контроль inventory" not in text
    assert "контроль инвентаря (inventory)" not in text


def test_chinese_whats_new_production_note_is_localized() -> None:
    text = _read("docs/whats-new.zh.md")

    assert "提示注入（`prompt injection`）、越狱（`jailbreaking`）" in text
    assert "动作幻觉（`action hallucination`）分类法" in text
    assert "语义鸿沟（`semantic gap`）" in text
    assert "RAG 优先（`RAG first`）" in text
    assert "持续预训练（`continued pretraining`）与 `SFT` 的区别" in text
    assert "大型工具目录、语义工具过滤（`semantic tool filtering`）" in text
    assert "MCP 主机/客户端/服务器（`MCP host/client/server`）角色" in text
    assert "延迟预算（`latency budget`）" in text
    assert "以 LLM 作为评审器（`LLM-as-a-judge`）" in text
    assert "`prompt injection`、`jailbreaking` 与 `action hallucination` 分类法" not in text
    assert "检索轮廓：`semantic gap`、`HyDE`、`RAG first`" not in text
    assert "持续预训练与 `SFT` 的区别" not in text
    assert "持续预训练（continued pretraining）与 `SFT` 的区别" not in text
    assert "大工具目录、`semantic tool filtering` 和 `MCP host/client/server` 角色" not in text
    assert "补上了大工具目录、语义工具过滤" not in text
    assert "`latency budget` 的产品视角" not in text
    assert "实用的 `LLM-as-a-judge` 表述" not in text


def test_russian_whats_new_production_note_is_localized() -> None:
    text = _read("docs/whats-new.md")

    assert "Усилен эксплуатационный контур (production) в частях I-V" in text
    assert (
        "между архитектурой, поиском по знаниям (retrieval), исполнением "
        "и дисциплиной оценивания (eval)"
        in text
    )
    assert "архитектура исполнения (runtime), слой обучения и продуктовая поверхность" in text
    assert "более четкая таксономия для инъекций промптов (`prompt injection`)" in text
    assert "джейлбрейка (`jailbreak`)" in text
    assert "галлюцинаций действий (`action hallucination`)" in text
    assert "усилен контур поиска по знаниям (retrieval)" in text
    assert "семантический разрыв (`semantic gap`)" in text
    assert "подход «сначала RAG» (`RAG first`)" in text
    assert "различие между продолженным предобучением (continued pretraining) и `SFT`" in text
    assert "добавлены практические правила для больших каталогов инструментов" in text
    assert "семантическая фильтрация инструментов" in text
    assert "явные роли MCP: `host`, `client` и `server`" in text
    assert "продуктовый разбор бюджета задержки (`latency budget`)" in text
    assert "практическая рамка для оценки через `LLM-as-a-judge`" in text
    assert "базовые платформенные слои" in text
    assert "между обсуждением дизайна, циклом оценивания (eval) и раскаткой" in text
    assert "повседневные вопросы эксплуатационной команды" in text
    assert "читательских точек входа" in text
    assert "семантическая фильтрация инструментов (`semantic tool filtering`)" in text
    assert "`HyDE` и выбор между RAG и обучением модели (`RAG vs training`)" in text
    assert "бюджет задержки (`latency budget`) и маршрутизированные конвейеры" in text
    assert "оценку через `LLM-as-a-judge` и калибровку судьи (judge calibration)" in text
    assert "инъекцией промптов (`prompt injection`)" in text
    assert "джейлбрейком (`jailbreak`)" in text
    assert "галлюцинациями действий (`action hallucination`)" in text
    assert "Усилен production contour" not in text
    assert "Усилен production-контур" not in text
    assert "между архитектурой, retrieval, execution и eval discipline" not in text
    assert "между архитектурой, retrieval, execution и eval-дисциплиной" not in text
    assert "исполнением и eval-дисциплиной" not in text
    assert "между архитектурой, retrieval, исполнением и eval-дисциплиной" not in text
    assert "между архитектурой, retrieval-поиском" not in text
    assert "training layer и product surface" not in text
    assert "training layer и продуктовая поверхность" not in text
    assert "runtime-архитектура, training-слой" not in text
    assert "training-слой" not in text
    assert "более четкая taxonomy для `prompt injection`" not in text
    assert "более четкая таксономия для `prompt injection`" not in text
    assert "`jailbreak` и `action hallucination`" not in text
    assert "`prompt injection`, `jailbreak`" not in text
    assert "усилен retrieval contour" not in text
    assert "retrieval-контур: `semantic gap`" not in text
    assert "усилен retrieval-контур" not in text
    assert "`HyDE`, `RAG first`, различие" not in text
    assert "подход RAG-first (`RAG first`)" not in text
    assert "различие между continued pretraining и `SFT`" not in text
    assert "различие между дообучением (continued pretraining)" not in text
    assert "добавлены practical rules для больших tool catalogs" not in text
    assert "практические правила для больших tool catalogs" not in text
    assert "каталогов инструментов, `semantic tool filtering`" not in text
    assert "явные роли `MCP host / client / server`" not in text
    assert "продуктовый взгляд на `latency budget`" not in text
    assert "продуктовый взгляд на бюджет задержки (`latency budget`)" not in text
    assert "practical framing для `LLM-as-a-judge`" not in text
    assert "практическая рамка для `LLM-as-a-judge`" not in text
    assert "базовые platform layers" not in text
    assert "между design review, eval loop и rollout" not in text
    assert "reader entry points" not in text
    assert "latency budget` и routed pipelines" not in text
    assert "`latency budget` и маршрутизированные конвейеры" not in text
    assert "- `semantic tool filtering`;" not in text
    assert "- `HyDE` и `RAG vs training`;" not in text
    assert "`HyDE` и выбор между RAG и обучением (`RAG vs training`)" not in text
    assert "`LLM-as-a-judge` и judge calibration" not in text
    assert "- `LLM-as-a-judge` и калибровку судьи" not in text
    assert "между дизайн-ревью, eval loop и rollout" not in text
    assert "между дизайн-ревью, циклом оценивания (eval) и раскаткой" not in text
    assert "между дизайн-ревью, eval-циклом" not in text
    assert "между дизайн-ревью, eval-циклом и rollout" not in text
    assert "повседневные вопросы production-команды" not in text


def test_chinese_whats_new_navigation_topics_are_localized() -> None:
    text = _read("docs/whats-new.zh.md")

    assert "### 读者入口页更清晰" in text
    assert "已更新的入口页：" in text
    assert "### 入口页更强了" not in text
    assert "已更新：" not in text
    assert "语义工具过滤（`semantic tool filtering`）" in text
    assert "`HyDE` 与 RAG 与训练之间的取舍（`RAG vs training`）" in text
    assert "延迟预算（`latency budget`）与路由管线" in text
    assert "以 LLM 作为评审器（`LLM-as-a-judge`）与评审器校准" in text
    assert "提示注入（`prompt injection`）、越狱（`jailbreaking`）" in text
    assert "动作幻觉（`action hallucination`）的区别" in text

    forbidden_markers = (
        "- `semantic tool filtering`；",
        "- `HyDE` 与 `RAG vs training`；",
        "`HyDE` 与 RAG 和训练取舍（`RAG vs training`）",
        "`HyDE` 与 RAG 和训练之间的取舍（`RAG vs training`）",
        "- `latency budget` 与路由管线；",
        "- `LLM-as-a-judge` 与评审器校准；",
        "- `prompt injection`、`jailbreaking` 与 `action hallucination` 的区别。",
    )

    for marker in forbidden_markers:
        assert marker not in text, marker


def test_chinese_whats_new_runtime_note_is_localized() -> None:
    text = _read("docs/whats-new.zh.md")

    assert "委派授权上下文（delegated authorization context）" in text
    assert "控制机制与生命周期内的运行时控制检查（runtime-control inspection）" in text
    assert "生命周期工件（lifecycle artifacts）" in text
    assert "会话导出与回放摘要（replay summaries）" in text
    assert "评测数据集导出（eval dataset export）" in text
    assert "带数据遮蔽（redaction）、遮蔽后摘要（redacted summaries）" in text
    assert "回放保留（replay preservation）" in text
    assert "模式版本控制（schema versioning）" in text
    assert "追踪导出（trace export）" in text

    forbidden_markers = (
        "审批与 delegated authorization context",
        "控制项与 lifecycle runtime-control inspection",
        "控制项与生命周期内的运行时控制检查",
        "- 生命周期工件；\n- 会话导出与回放摘要",
        "会话导出与 replay summaries",
        "- 评测数据集导出；",
        "带 redaction、redacted summaries、replay preservation 与 schema versioning",
        "schema versioning）的追踪导出。",
    )

    for marker in forbidden_markers:
        assert marker not in text, marker


def test_russian_whats_new_runtime_note_is_localized() -> None:
    text = _read("docs/whats-new.md")

    assert "согласования (approvals) и контекст делегирования авторизации" in text
    assert "контрольные механизмы и проверку управления исполнением (`runtime-control`)" in text
    assert "в жизненном цикле (lifecycle)" in text
    assert "артефакты жизненного цикла (lifecycle)" in text
    assert "экспорт сессий и сводки воспроизведения (replay)" in text
    assert "экспорт оценочных наборов данных (eval)" in text
    assert "экспорт наборов данных eval" not in text
    assert "экспорт трасс (trace) с маскированием данных (redaction), очищенными сводками" in text
    assert "сохранением воспроизведения (replay)" in text
    assert "версионированием схем" in text
    assert "описательные главы" in text
    assert "работающую эталонную реализацию" in text

    forbidden_markers = (
        "approvals и delegated authorization context",
        "approvals и контекст делегированной авторизации",
        "согласования (approvals) и контекст делегированной авторизации",
        "controls и lifecycle runtime-control inspection",
        "controls и проверку runtime-control в lifecycle",
        "контрольные механизмы и проверку runtime-control в lifecycle",
        "контрольные механизмы и проверку runtime-control в жизненном цикле (lifecycle)",
        "lifecycle artifacts",
        "lifecycle-артефакты",
        "session export и replay summaries",
        "экспорт сессий и replay-сводки",
        "eval dataset export",
        "экспорт eval-наборов данных",
        "trace export с redaction",
        "экспорт trace с redaction",
        "экспорт trace с редактированием (redaction)",
        "экспорт трасс (trace) с редактированием (redaction)",
        "редактированными сводками",
        "redacted summaries",
        "replay preservation",
        "сохранением replay",
        "schema versioning",
        "narrative chapters",
        "runnable reference implementation",
    )

    for marker in forbidden_markers:
        assert marker not in text, marker


def test_russian_whats_new_reference_note_is_localized() -> None:
    text = _read("docs/whats-new.md")

    assert "### Переиспользуемые схемы и артефакты" in text
    assert "### Справочный слой с переиспользуемыми схемами" not in text
    assert "отдельные справочные страницы" in text
    assert "- трассировки (traces) и каталог событий;" in text
    assert "- оценочные наборы данных (eval) и контракт оценивания;" in text
    assert "- наборы данных eval и контракт оценивания;" not in text
    assert "- пакеты политик и контуры согласований (approvals);" in text
    assert "- ревью изменений и контрольные этапы раскатки;" in text
    assert "- артефакты жизненного цикла (lifecycle);" in text
    assert "- контракты поиска и извлечения из памяти." in text
    assert "проверяемым схемам и артефактам" in text

    forbidden_markers = (
        "Справочный слой с reusable schemas",
        "reference pages для",
        "- traces и event catalog;",
        "- traces и каталог событий;",
        "- трассы (traces) и каталог событий;",
        "- eval datasets и grading contract;",
        "- eval-наборы данных и контракт оценивания;",
        "- policy bundles и approvals;",
        "- пакеты политик и approvals-контуры;",
        "- change review и rollout gates;",
        "- ревью изменений и rollout gates;",
        "- ревью изменений и rollout-гейты;",
        "- ревью изменений и гейты раскатки;",
        "- lifecycle-артефакты;",
        "- memory retrieval contracts.",
        "- контракты извлечения из памяти.",
        "reviewable схемам",
    )

    for marker in forbidden_markers:
        assert marker not in text, marker


def test_chinese_whats_new_reference_note_is_localized() -> None:
    text = _read("docs/whats-new.zh.md")

    assert "### 可复用的模式与契约" in text
    assert "### 可复用的参考层" not in text
    assert "追踪与事件目录（traces and event catalog）" in text
    assert "评测数据集与评分契约（eval datasets and grading contracts）" in text
    assert "策略包与审批（policy bundles and approvals）" in text
    assert "变更评审与发布门禁（change review and rollout gates）" in text
    assert "生命周期工件（lifecycle artifacts）" in text
    assert "记忆检索契约（memory retrieval contracts）" in text
    assert "- 追踪与事件目录；" not in text
    assert "- 评测数据集与评分契约；" not in text
    assert "- 策略包与审批；" not in text
    assert "- 变更评审与发布门禁；" not in text
    assert "- 生命周期工件；\n- 记忆检索契约" not in text
    assert "- 记忆检索契约。" not in text


def test_chinese_whats_new_practical_appendix_note_is_localized() -> None:
    text = _read("docs/whats-new.zh.md")

    assert "### 检查清单与实践工件" in text
    assert "术语表（glossary）" in text
    assert "速查清单（cheat sheets）" in text
    assert "案例研究（case studies）" in text
    assert "策略模板（policy templates）" in text
    assert "研究前沿页面（research frontier page）" in text
    assert "社区路线图（community roadmap）" in text
    assert "### 更强的实践附录" not in text
    assert "- 术语表；" not in text
    assert "- 速查清单；" not in text
    assert "- 案例研究；" not in text
    assert "- 策略模板；" not in text
    assert "- 研究前沿页面；" not in text
    assert "- 社区路线图。" not in text


def test_russian_whats_new_practical_appendix_note_is_localized() -> None:
    text = _read("docs/whats-new.md")

    assert "## Практическое приложение" in text
    assert "### Практические материалы приложения" in text
    assert "### Практическое приложение" not in text
    assert "- глоссарий;" in text
    assert "- шпаргалки;" in text
    assert "- кейсы;" in text
    assert "- шаблоны политик;" in text
    assert "- исследовательский фронтир;" in text
    assert "- дорожная карта сообщества." in text
    assert "глоссарий и практические материалы" in text

    forbidden_markers = (
        "Практический appendix",
        "- glossary;",
        "- cheat sheets;",
        "- case studies;",
        "- policy templates;",
        "- research frontier;",
        "- community roadmap.",
        "glossary и practical assets",
    )

    for marker in forbidden_markers:
        assert marker not in text, marker


def test_book_plan_defines_three_case_spines() -> None:
    required_markers = (
        "Case-spine map",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "side effects",
        "context quality",
        "response and governance",
    )
    checked_files = (
        "docs/book/plan.md",
        "docs/book/plan.en.md",
        "docs/book/plan.zh.md",
    )
    deprecated_markers = (
        "support triage for side effects",
        "support triage для side effects",
        "support triage 对应 side effects",
        "internal knowledge for context quality",
        "internal knowledge для context quality",
        "internal knowledge 对应 context quality",
        "incident coordination for response and governance",
        "incident coordination для response and governance",
        "incident coordination 对应 response and governance",
    )

    _assert_files_contain_all(checked_files, required_markers)
    for path in checked_files:
        text = _read(path)
        for marker in deprecated_markers:
            assert marker not in text, (path, marker)


def test_practical_routines_threads_three_canonical_cases() -> None:
    required_markers = (
        "Routine case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "approved write routine",
        "retrieval routine",
        "source attribution",
        "tenant boundary",
        "incident escalation routine",
        "notification handoff",
        "owner record",
    )
    checked_files = (
        "docs/book/part-i/practical-routines.md",
        "docs/book/part-i/practical-routines.en.md",
        "docs/book/part-i/practical-routines.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_practical_manager_handoffs_threads_three_canonical_cases() -> None:
    required_markers = (
        "Manager/handoff case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "approved write routine",
        "ticket state",
        "audit story",
        "read-heavy capabilities",
        "source attribution",
        "tenant boundary",
        "escalation",
        "owner record",
        "accountable roles",
    )
    checked_files = (
        "docs/book/part-i/practical-manager-handoffs.md",
        "docs/book/part-i/practical-manager-handoffs.en.md",
        "docs/book/part-i/practical-manager-handoffs.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_practical_mcp_a2a_threads_three_canonical_cases() -> None:
    required_markers = (
        "MCP/A2A case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "helpdesk",
        "CRM",
        "ticket-write tools",
        "MCP boundary",
        "responsible role",
        "knowledge server",
        "retrieval adapter",
        "source attribution",
        "tenant boundary",
        "A2A handoff",
        "owner record",
        "notification tools",
        "incident state resources",
        "MCP/policy audit",
    )
    checked_files = (
        "docs/book/part-iv/practical-mcp-a2a.md",
        "docs/book/part-iv/practical-mcp-a2a.en.md",
        "docs/book/part-iv/practical-mcp-a2a.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_part_iv_index_surfaces_three_execution_case_routes() -> None:
    required_markers = (
        "Part IV canonical case routes",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "execution layer",
        "tool boundaries",
        "ticket-write capability",
        "approval gate",
        "idempotency key",
        "duplicate-ticket recovery",
        "retrieval adapter",
        "source attribution",
        "tenant boundary",
        "read-only MCP contract",
        "escalation tool",
        "notification side effects",
        "incident state updates",
        "rollback boundary",
    )
    checked_files = (
        "docs/book/part-iv/index.md",
        "docs/book/part-iv/index.en.md",
        "docs/book/part-iv/index.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_part_iii_index_surfaces_three_memory_case_routes() -> None:
    required_markers = (
        "Part III canonical case routes",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "memory/retrieval layer",
        "temporary ticket state",
        "duplicate-ticket context",
        "approved playbook retrieval",
        "source attribution",
        "freshness window",
        "tenant boundary",
        "memory provenance",
        "incident timeline",
        "owner handoff summaries",
        "escalation status",
        "post-incident lessons",
    )
    checked_files = (
        "docs/book/part-iii/index.md",
        "docs/book/part-iii/index.en.md",
        "docs/book/part-iii/index.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_part_ii_index_surfaces_three_security_case_routes() -> None:
    required_markers = (
        "Part II canonical case routes",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "security perimeter",
        "control points",
        "tool gateway",
        "approval stop",
        "audit trail",
        "least-privilege access",
        "ticket writes",
        "retrieval boundary",
        "access control",
        "prompt assembly",
        "egress filtering",
        "protected reads",
        "escalation tools",
        "notification approvals",
        "incident-data boundary",
        "side effects during response",
    )
    checked_files = (
        "docs/book/part-ii/index.md",
        "docs/book/part-ii/index.en.md",
        "docs/book/part-ii/index.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_part_i_index_surfaces_three_foundation_case_routes() -> None:
    required_markers = (
        "Part I canonical case routes",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "foundations layer",
        "canonical cases",
        "architecture shape",
        "workflow vs agent boundary",
        "right to act",
        "guarded autonomy",
        "first risky write path",
        "read-only workflow",
        "retrieval need",
        "memory discipline",
        "source-grounded answers",
        "coordination loop",
        "escalation trigger",
        "handoff boundary",
        "single-agent first decision",
    )
    checked_files = (
        "docs/book/part-i/index.md",
        "docs/book/part-i/index.en.md",
        "docs/book/part-i/index.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_part_v_index_surfaces_three_reliability_case_routes() -> None:
    required_markers = (
        "Part V canonical case routes",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "reliability/observability layer",
        "evidence routes",
        "trace coverage",
        "ticket writes",
        "duplicate-ticket regression",
        "approval-path evidence",
        "retrieval quality",
        "source-grounding judgment",
        "freshness budget",
        "memory-provenance evidence",
        "escalation latency",
        "notification delivery",
        "response ownership",
        "post-incident rollout judgment",
    )
    checked_files = (
        "docs/book/part-v/index.md",
        "docs/book/part-v/index.en.md",
        "docs/book/part-v/index.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_part_vi_index_surfaces_three_ownership_case_routes() -> None:
    required_markers = (
        "Part VI canonical case routes",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "operating model",
        "ownership boundaries",
        "ticket-write defaults",
        "approval mode",
        "duplicate-ticket recovery path",
        "corpus ownership",
        "access review",
        "retrieval quality",
        "knowledge provenance",
        "escalation authority",
        "notification policy",
        "response ownership",
        "post-incident action items",
    )
    checked_files = (
        "docs/book/part-vi/index.md",
        "docs/book/part-vi/index.en.md",
        "docs/book/part-vi/index.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_part_vii_index_surfaces_three_runtime_case_routes() -> None:
    required_markers = (
        "Part VII canonical case routes",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "reference implementation",
        "runtime paths",
        "run loop",
        "capability catalog",
        "approval pause/resume",
        "rollout checklist",
        "ticket writes",
        "memory/retrieval service",
        "read capability policy",
        "source attribution",
        "tenant isolation",
        "escalation capability",
        "notification side effects",
        "incident state handoff",
        "rollout readiness evidence",
    )
    checked_files = (
        "docs/book/part-vii/index.md",
        "docs/book/part-vii/index.en.md",
        "docs/book/part-vii/index.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_book_index_surfaces_three_canonical_cases() -> None:
    required_markers = (
        "Canonical case map",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "write capabilities",
        "duplicate-ticket recovery",
        "tenant boundaries",
        "source grounding",
        "notification side effects",
        "post-incident learning",
        "control surfaces",
    )
    checked_files = (
        "docs/book/index.md",
        "docs/book/index.en.md",
        "docs/book/index.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_multilingual_book_index_canonical_case_map_is_localized() -> None:
    russian_text = _read("docs/book/index.md")
    chinese_text = _read("docs/book/index.zh.md")

    assert "Каноническая карта сценариев" in russian_text
    assert "канонических сценария (canonical cases)" in russian_text
    assert "записывающих возможностей (write capabilities)" in russian_text
    assert "поиск (retrieval)" in russian_text
    assert "поверхностей управления (control surfaces)" in russian_text

    assert "规范案例地图" in chinese_text
    assert "规范案例（canonical cases）" in chinese_text
    assert "写入能力（write capabilities）" in chinese_text
    assert "检索（retrieval）" in chinese_text
    assert "控制表面（control surfaces）" in chinese_text

    forbidden_markers = (
        "Support triage остается",
        "для write capabilities",
        "что retrieval, memory",
        "проверяет traces",
        "три canonical cases",
        "Support triage 仍然是",
        "是 write capabilities",
        "检查 retrieval、memory",
        "检查 traces、SLO",
        "三个 canonical cases",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_multilingual_book_index_support_case_example_is_localized() -> None:
    russian_text = _read("docs/book/index.md")
    chinese_text = _read("docs/book/index.zh.md")

    assert "триажа поддержки (support-triage)" in russian_text
    assert "поиска (retrieval)" in russian_text
    assert "выполнения инструментов (tool execution)" in russian_text
    assert "восстановления после дубля тикета (duplicate-ticket recovery)" in russian_text
    assert "контролей несоответствия (misalignment controls)" in russian_text

    assert "支持分诊（support-triage）" in chinese_text
    assert "检索（retrieval）" in chinese_text
    assert "工具执行（tool execution）" in chinese_text
    assert "重复工单恢复（duplicate-ticket recovery）" in chinese_text
    assert "失配控制（misalignment controls）" in chinese_text

    forbidden_markers = (
        "следить за кейсом support-triage",
        "от retrieval и tool execution",
        "duplicate-ticket recovery, traces",
        "misalignment controls, telemetry",
        "跟随 support-triage 案例",
        "重复工单恢复、traces",
        "失配控制、telemetry",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_multilingual_book_index_promise_bullets_are_localized() -> None:
    russian_text = _read("docs/book/index.md")
    chinese_text = _read("docs/book/index.zh.md")

    assert "рабочего процесса (workflow)" in russian_text
    assert "управляемый запуск (run)" in russian_text
    assert "политику (policy)" in russian_text
    assert "доказательства (evidence)" in russian_text
    assert "ответственность оператора (operator accountability)" in russian_text

    assert "工作流（workflow）" in chinese_text
    assert "运行（run）" in chinese_text
    assert "策略（policy）" in chinese_text
    assert "证据（evidence）" in chinese_text
    assert "操作员问责（operator accountability）" in chinese_text

    forbidden_markers = (
        "достаточно обычного workflow",
        "управляемый run через policy",
        "execution, evidence, approval",
        "рассматривать memory, evals",
        "operator accountability как",
        "普通工作流就够了",
        "策略、执行、证据、审批、发布",
        "记忆、评测、来源谱系、退役",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_multilingual_book_index_direct_entry_links_are_localized() -> None:
    russian_text = _read("docs/book/index.md")
    chinese_text = _read("docs/book/index.zh.md")

    assert "[Перейти к Сквозной цепочке доказательств (Evidence Spine)]" in russian_text
    assert "[Перейти к жизненному циклу агентной системы]" in russian_text
    assert "[跳到证据主线（Evidence Spine）]" in chinese_text
    assert "[跳到智能体系统生命周期]" in chinese_text

    forbidden_markers = (
        "[Перейти к Evidence Spine]",
        "[跳到 Evidence Spine]",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_case_studies_align_with_three_canonical_cases() -> None:
    required_markers = (
        "Canonical case alignment",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "write capability",
        "duplicate-ticket recovery",
        "access control",
        "knowledge provenance",
        "notification side effects",
        "response ownership",
        "post-incident learning",
    )
    checked_files = (
        "docs/appendix/case-studies.md",
        "docs/appendix/case-studies.en.md",
        "docs/appendix/case-studies.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)
    deprecated_markers = (
        "Support Triage Agent",
        "Internal Knowledge Agent",
        "Incident Coordination Agent",
    )
    for path in checked_files:
        text = _read(path)
        for marker in deprecated_markers:
            assert marker not in text, (path, marker)


def test_multilingual_case_studies_alignment_note_is_localized() -> None:
    russian_text = _read("docs/appendix/case-studies.md")
    chinese_text = _read("docs/appendix/case-studies.zh.md")

    assert "Выравнивание канонических сценариев" in russian_text
    assert "каноническим сценариям (canonical cases)" in russian_text
    assert "записывающую возможность (write capability)" in russian_text
    assert "контроль доступа (access control)" in russian_text
    assert "побочные эффекты уведомлений (notification side effects)" in russian_text

    assert "规范案例对齐" in chinese_text
    assert "规范案例（canonical cases）" in chinese_text
    assert "写入能力（write capability）" in chinese_text
    assert "访问控制（access control）" in chinese_text
    assert "通知副作用（notification side effects）" in chinese_text

    forbidden_markers = (
        "трем canonical cases",
        "про write capability",
        "про retrieval",
        "про traces",
        "三个 canonical cases",
        "承载 write capability",
        "承载 retrieval",
        "承载 traces",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_readmes_surface_three_canonical_cases() -> None:
    required_markers = (
        "canonical cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "write capabilities",
        "approvals",
        "knowledge provenance",
        "notification side effects",
        "response ownership",
        "post-incident learning",
    )
    checked_files = (
        "README.md",
        "README.ru.md",
        "README.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_multilingual_readme_canonical_case_intro_is_localized() -> None:
    russian_text = _read("README.ru.md")
    chinese_text = _read("README.zh.md")

    assert "Производственная реальность (production reality)" in russian_text
    assert "театра агентов (agent theater)" in russian_text
    assert "Триаж поддержки (Support triage)" in russian_text
    assert "записывающие возможности (write capabilities)" in russian_text
    assert "происхождение знаний (knowledge provenance)" in russian_text
    assert "побочные эффекты уведомлений (notification side effects)" in russian_text

    assert "生产现实（production reality）" in chinese_text
    assert "智能体表演（agent theater）" in chinese_text
    assert "支持分诊（Support triage）" in chinese_text
    assert "写入能力（write capabilities）" in chinese_text
    assert "知识来源（knowledge provenance）" in chinese_text
    assert "通知副作用（notification side effects）" in chinese_text

    forbidden_markers = (
        "Production reality вместо agent theater",
        "Support-triage / duplicate-ticket thread",
        "Три canonical cases",
        "Support triage покрывает write capabilities",
        "Internal knowledge assistant — retrieval",
        "Incident coordination — traces",
        "support-triage / duplicate-ticket thread 把",
        "三个 canonical cases",
        "Support triage 覆盖 write capabilities",
        "Internal knowledge assistant 覆盖 retrieval",
        "Incident coordination 覆盖 traces",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_multilingual_readme_purpose_prompting_term_is_localized() -> None:
    russian_text = _read("README.ru.md")
    chinese_text = _read("README.zh.md")

    assert "промптинг (prompting)" in russian_text
    assert "提示词技巧（prompting）" in chinese_text

    forbidden_markers = (
        "удачный prompting",
        "提示词技巧和工具调用",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_readmes_surface_safe_agent_schema_spine() -> None:
    required_markers = (
        "Safe-agent schema spine",
        "trace schema",
        "eval schema",
        "memory/retrieval schema",
        "MCP threat model",
        "A2A handoff trust contract",
        "verifier verdict record",
        "governance action record",
        "memory poisoning review fields",
        "unified agent threat evidence",
    )
    checked_files = (
        "README.md",
        "README.ru.md",
        "README.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_multilingual_readme_safe_agent_schema_spine_is_localized() -> None:
    russian_text = _read("README.ru.md")
    chinese_text = _read("README.zh.md")

    assert "Сквозная цепочка схем безопасного агента (Safe-agent schema spine)" in russian_text
    assert "схема трасс (trace schema)" in russian_text
    assert "схема оценок (eval schema)" in russian_text
    assert "модель угроз MCP (MCP threat model)" in russian_text
    assert "единые доказательства угроз агенту (unified agent threat evidence)" in russian_text

    assert "安全智能体模式主线（Safe-agent schema spine）" in chinese_text
    assert "追踪模式（trace schema）" in chinese_text
    assert "评测模式（eval schema）" in chinese_text
    assert "MCP 威胁模型（MCP threat model）" in chinese_text
    assert "统一智能体威胁证据（unified agent threat evidence）" in chinese_text

    forbidden_markers = (
        "- Safe-agent schema spine:",
        "trace schema](docs/appendix/trace-schema.md), [eval schema",
        "связывают MCP threat model",
        "verifier verdict record, governance action record",
        "- Safe-agent schema spine：",
        "连接 MCP threat model",
        "verifier verdict record、governance action record",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_multilingual_readme_runtime_artifact_bullets_are_localized() -> None:
    russian_text = _read("README.ru.md")
    chinese_text = _read("README.zh.md")

    assert "эталонная среда исполнения (runtime)" in russian_text
    assert "Эталонная среда исполнения (runtime):" in russian_text
    assert "команд CLI (CLI commands)" in russian_text
    assert "Эталонная среда исполнения (runtime reference package)" in russian_text
    assert "утвержденный инвентарь (approved inventory)" in russian_text
    assert "подтверждения (approvals)" in russian_text
    assert "проверки раскатки (rollout checks)" in russian_text
    assert "контракт профиля песочницы (sandbox profile contract)" in russian_text
    assert "операционного скелета (operational skeleton)" in russian_text

    assert "参考运行时（runtime）" in chinese_text
    assert "参考运行时包（reference package）" in chinese_text
    assert "CLI 命令列表（CLI commands）" in chinese_text
    assert "参考运行时包（runtime reference package）" in chinese_text
    assert "已批准清单（approved inventory）" in chinese_text
    assert "审批（approvals）" in chinese_text
    assert "发布检查（rollout checks）" in chinese_text
    assert "沙箱配置契约（sandbox profile contract）" in chinese_text
    assert "运行骨架（operational skeleton）" in chinese_text

    forbidden_markers = (
        "эталонный runtime",
        "Эталонный runtime",
        "- [Эталонный пакет]",
        "- 参考包：[docs/appendix/reference-package",
        "完整 CLI 列表",
        "каталог возможностей и approved inventory",
        "approvals и rollout checks",
        "lifecycle-артефакты для change records",
        "sandbox profile contract и sandbox review evidence",
        "для operational skeleton",
        "lifecycle inspection 中可见",
        "用于 operational skeleton",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_start_here_surfaces_three_canonical_case_routes() -> None:
    required_markers = (
        "Canonical case routes",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "write capabilities",
        "approvals",
        "duplicate-ticket recovery",
        "knowledge provenance",
        "notification side effects",
        "response ownership",
        "post-incident learning",
    )
    checked_files = (
        "docs/start-here.md",
        "docs/start-here.en.md",
        "docs/start-here.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_multilingual_start_here_intro_terms_are_localized() -> None:
    russian_text = _read("docs/start-here.md")
    chinese_text = _read("docs/start-here.zh.md")

    assert "производственную реальность (production reality)" in russian_text
    assert "перегруженных промптами (prompt-heavy prototypes)" in russian_text
    assert "границами доверия (trust boundaries)" in russian_text
    assert "слоем политик (policy layer)" in russian_text
    assert "производственную агентную систему (production agent system)" in russian_text
    assert "пути записи (write paths)" in russian_text
    assert "реальные границы доверия (trust boundaries)" in russian_text
    assert "трасс (traces), SLO и оценок (evals)" in russian_text
    assert "серьезной раскатки (rollout)" in russian_text

    assert "生产现实（production reality）" in chinese_text
    assert "提示堆出来的原型（prompt-heavy prototypes）" in chinese_text
    assert "信任边界（trust boundaries）" in chinese_text
    assert "策略层（policy layer）" in chinese_text
    assert "生产级智能体系统（production agent system）" in chinese_text
    assert "写入路径（write paths）" in chinese_text
    assert "真实信任边界（trust boundaries）" in chinese_text
    assert "追踪（traces）、SLO 和评测（evals）" in chinese_text
    assert "认真发布（rollout）之前" in chinese_text

    forbidden_markers = (
        "реальность production",
        "от prompt-heavy прототипов",
        "границами доверия, policy layer",
        "дисциплина вокруг trust boundaries",
        "production agent system нельзя",
        "набор tools",
        "есть write paths",
        "реальные trust boundaries",
        "без traces, SLO и evals",
        "серьезного rollout",
        "生产现实的系统",
        "提示堆出来的原型，",
        "信任边界、策略层、审批",
        "生产级智能体系统不能",
        "几个工具”，",
        "有写入路径、人工审批",
        "真实信任边界在哪里",
        "没有追踪、SLO 和评测",
        "认真发布之前",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_multilingual_start_here_canonical_routes_note_is_localized() -> None:
    russian_text = _read("docs/start-here.md")
    chinese_text = _read("docs/start-here.zh.md")

    assert "Канонические маршруты сценариев" in russian_text
    assert "канонических сценария (canonical cases)" in russian_text
    assert "записывающие возможности (write capabilities)" in russian_text
    assert "поиск (retrieval)" in russian_text
    assert "трассы (traces)" in russian_text

    assert "规范案例路线" in chinese_text
    assert "规范案例（canonical cases）" in chinese_text
    assert "写入能力（write capabilities）" in chinese_text
    assert "检索（retrieval）" in chinese_text
    assert "追踪（traces）" in chinese_text

    forbidden_markers = (
        "три canonical cases",
        "ведет через write capabilities",
        "подсвечивает retrieval, memory",
        "проверяет traces, escalation",
        "三个 canonical cases",
        "承载 write capabilities",
        "突出 retrieval、memory",
        "检查 traces、escalation",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_multilingual_start_here_support_case_example_is_localized() -> None:
    russian_text = _read("docs/start-here.md")
    chinese_text = _read("docs/start-here.zh.md")

    assert "триажа поддержки (support-triage)" in russian_text
    assert "поиска (retrieval)" in russian_text
    assert "безопасного выполнения инструментов (safe tool execution)" in russian_text
    assert "восстановление после дубля тикета (duplicate-ticket recovery)" in russian_text
    assert "платформенному контракту (incident-to-platform-contract path)" in russian_text

    assert "支持分诊（support-triage）" in chinese_text
    assert "检索（retrieval）" in chinese_text
    assert "安全工具执行（safe tool execution）" in chinese_text
    assert "重复工单恢复（duplicate-ticket recovery）" in chinese_text
    assert "从事故到平台契约的路径（incident-to-platform-contract path）" in chinese_text

    forbidden_markers = (
        "историей support-triage",
        "начинается с retrieval",
        "проходит через duplicate-ticket recovery",
        "misalignment controls, telemetry",
        "incident-to-platform-contract путь",
        "跟着 support-triage 故事",
        "重复工单恢复、traces",
        "进入 rollout、ADLC",
        "失配控制、telemetry",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_multilingual_start_here_code_artifact_route_is_localized() -> None:
    russian_text = _read("docs/start-here.md")
    chinese_text = _read("docs/start-here.zh.md")

    assert "скелет среды исполнения (runtime skeleton)" in russian_text
    assert "контракты политик (policy contracts)" in russian_text
    assert "путь памяти (memory path)" in russian_text
    assert "телеметрия (telemetry)" in russian_text
    assert "артефакты раскатки (rollout artifacts)" in russian_text

    assert "运行时骨架（runtime skeleton）" in chinese_text
    assert "策略契约（policy contracts）" in chinese_text
    assert "记忆路径（memory path）" in chinese_text
    assert "遥测（telemetry）" in chinese_text
    assert "发布工件（rollout artifacts）" in chinese_text

    forbidden_markers = (
        "скелет runtime (runtime skeleton)",
        "нужны runtime skeleton",
        "policy contracts, memory path",
        "telemetry и rollout-артефакты",
        "需要运行时骨架、策略契约",
        "记忆路径、遥测和发布工件",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_multilingual_start_here_change_management_link_is_localized() -> None:
    russian_text = _read("docs/start-here.md")
    chinese_text = _read("docs/start-here.zh.md")

    assert "Управление изменениями (Change management) для агентных систем" in russian_text
    assert "智能体系统的变更管理（Change management）" in chinese_text

    forbidden_markers = (
        "Глава 20. Change management для агентных систем",
        "智能体系统的变更管理](book/part-viii/chapter-20",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_homepage_surfaces_three_canonical_cases() -> None:
    required_markers = (
        "Canonical case map",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "write capabilities",
        "approvals",
        "duplicate-ticket recovery",
        "knowledge provenance",
        "notification side effects",
        "response ownership",
        "post-incident learning",
    )
    checked_files = (
        "docs/index.md",
        "docs/index.en.md",
        "docs/index.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_multilingual_homepage_canonical_case_map_is_localized() -> None:
    russian_text = _read("docs/index.md")
    chinese_text = _read("docs/index.zh.md")

    assert "Каноническая карта сценариев" in russian_text
    assert "канонических сценария (canonical cases)" in russian_text
    assert "записывающие возможности (write capabilities)" in russian_text
    assert "поиск (retrieval)" in russian_text
    assert "трассы (traces)" in russian_text

    assert "规范案例地图" in chinese_text
    assert "规范案例（canonical cases）" in chinese_text
    assert "写入能力（write capabilities）" in chinese_text
    assert "检索（retrieval）" in chinese_text
    assert "追踪（traces）" in chinese_text

    forbidden_markers = (
        "три canonical cases",
        "проверяет write capabilities",
        "проверяет retrieval, memory",
        "проверяет traces, escalation",
        "三个 canonical cases",
        "检查 write capabilities",
        "检查 retrieval、memory",
        "检查 traces、escalation",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_multilingual_homepage_platform_terms_are_localized() -> None:
    russian_text = _read("docs/index.md")
    chinese_text = _read("docs/index.zh.md")

    assert "рискованные действия (risky actions)" in russian_text
    assert "инструментов (tools)" in russian_text
    assert "слой политик (policy layer)" in russian_text
    assert "агентные функции (agent features)" in russian_text
    assert "общая среда исполнения (runtime)" in russian_text
    assert "границы доверия (trust boundaries)" in russian_text
    assert "рискованные пути исполнения (risky execution paths)" in russian_text
    assert "поверхности злоупотреблений (abuse surfaces)" in russian_text
    assert "наблюдаемостью уровня запуска (run-level observability)" in russian_text
    assert "управлением жизненным циклом (lifecycle governance)" in russian_text

    assert "高风险动作（risky actions）" in chinese_text
    assert "工具（tools）" in chinese_text
    assert "策略层（policy layer）" in chinese_text
    assert "智能体功能（agent features）" in chinese_text
    assert "共享运行时（runtime）" in chinese_text
    assert "信任边界（trust boundaries）" in chinese_text
    assert "高风险执行路径（risky execution paths）" in chinese_text
    assert "滥用表面（abuse surfaces）" in chinese_text
    assert "运行级可观测性（run-level observability）" in chinese_text
    assert "生命周期治理（lifecycle governance）" in chinese_text

    forbidden_markers = (
        "появляются risky actions",
        "нескольких tools",
        "Нужны явные границы доверия, policy layer",
        "строить agent features",
        "общий runtime, policy layer, approvals",
        "важны trust boundaries, risky execution paths",
        "явными trust и action boundaries",
        "с execution под контролем",
        "с approvals для рискованных путей",
        "run-level observability и evidence",
        "rollout discipline, ownership и lifecycle governance",
        "高风险动作、记忆",
        "几个工具就不够",
        "共享运行时、策略层、审批",
        "信任边界、高风险执行路径",
        "运行级可观测性与证据",
        "发布纪律、负责人机制",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_homepage_surfaces_safe_agent_schema_spine() -> None:
    required_markers = (
        "Safe-agent schema spine",
        "trace schema",
        "eval schema",
        "memory/retrieval schema",
        "MCP threat model",
        "A2A handoff trust contract",
        "verifier verdict record",
        "governance action record",
        "memory poisoning review fields",
        "unified agent threat evidence",
    )
    checked_files = (
        "docs/index.md",
        "docs/index.en.md",
        "docs/index.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_multilingual_homepage_safe_agent_schema_spine_is_localized() -> None:
    russian_text = _read("docs/index.md")
    chinese_text = _read("docs/index.zh.md")

    assert "Цепочка схем безопасного агента (Safe-agent schema spine)" in russian_text
    assert "архитектуре безопасного агента (safe-agent architecture)" in russian_text
    assert "схемы трасс (trace schema)" in russian_text
    assert "схемы оценок (eval schema)" in russian_text
    assert "схемы памяти/поиска (memory/retrieval schema)" in russian_text
    assert "модель угроз MCP (MCP threat model)" in russian_text
    assert "контракт доверия передачи A2A (A2A handoff trust contract)" in russian_text
    assert "запись вердикта проверяющего (verifier verdict record)" in russian_text
    assert "единые доказательства угроз агенту (unified agent threat evidence)" in russian_text

    assert "安全智能体模式主线（Safe-agent schema spine）" in chinese_text
    assert "安全智能体架构（safe-agent architecture）" in chinese_text
    assert "追踪模式（trace schema）" in chinese_text
    assert "评测模式（eval schema）" in chinese_text
    assert "记忆/检索模式（memory/retrieval schema）" in chinese_text
    assert "MCP 威胁模型（MCP threat model）" in chinese_text
    assert "A2A 移交信任契约（A2A handoff trust contract）" in chinese_text
    assert "验证器裁决记录（verifier verdict record）" in chinese_text
    assert "统一智能体威胁证据（unified agent threat evidence）" in chinese_text

    forbidden_markers = (
        '!!! note "Safe-agent schema spine"',
        "путь по safe-agent architecture",
        "начни с [trace schema]",
        "Этот spine связывает MCP threat model",
        "A2A handoff trust contract, verifier verdict record",
        "memory poisoning review fields и unified agent threat evidence",
        "safe-agent architecture 路线",
        "从 [trace schema]",
        "这个 spine 连接 MCP threat model",
        "A2A handoff trust contract、verifier verdict record",
        "memory poisoning review fields 和 unified agent threat evidence",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_multilingual_homepage_existing_scope_terms_are_localized() -> None:
    russian_text = _read("docs/index.md")
    chinese_text = _read("docs/index.zh.md")

    assert "основная рукопись (core manuscript)" in russian_text
    assert "управления жизненным циклом (lifecycle governance)" in russian_text
    assert "редакторскую очистку (editorial cleanup)" in russian_text
    assert "схемами трасс (traces)" in russian_text
    assert "оценок (evals)" in russian_text
    assert "пакетов политик (policy bundles)" in russian_text
    assert "подтверждений (approvals)" in russian_text
    assert "артефактов жизненного цикла (lifecycle artifacts)" in russian_text
    assert "редакторский проход (editorial pass)" in russian_text
    assert "трюков с промптами (prompt tricks)" in russian_text
    assert "платформенной документацией (platform docs)" in russian_text
    assert "путь записи (write path)" in russian_text

    assert "核心原稿（core manuscript）" in chinese_text
    assert "生命周期治理（lifecycle governance）" in chinese_text
    assert "编辑清理（editorial cleanup）" in chinese_text
    assert "追踪（traces）" in chinese_text
    assert "评测（evals）" in chinese_text
    assert "策略包（policy bundles）" in chinese_text
    assert "审批（approvals）" in chinese_text
    assert "生命周期工件（lifecycle artifacts）" in chinese_text
    assert "编辑打磨（editorial pass）" in chinese_text
    assert "提示技巧合集（prompt tricks）" in chinese_text
    assert "平台文档（platform docs）" in chinese_text
    assert "写入路径（write path）" in chinese_text

    forbidden_markers = (
        "core-рукопись",
        "до lifecycle governance",
        "проходящие editorial cleanup",
        "схемами traces, evals",
        "policy bundles, approvals",
        "lifecycle-артефактов",
        "Активный editorial pass",
        "сборник prompt tricks",
        "SDK и platform docs",
        "ограничивать write path",
        "生命周期治理的八个部分",
        "编辑清理的 `en`",
        "覆盖追踪、评测、策略包、审批",
        "生命周期工件的参考页面",
        "公开站点表面编辑打磨。",
        "提示技巧合集，也不是",
        "平台文档之上",
        "写入路径应该怎样受限",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_public_entry_safe_agent_schema_spine_links_are_clickable() -> None:
    expected_links_by_file = {
        "README.md": (
            "docs/appendix/trace-schema.en.md",
            "docs/appendix/eval-schema.en.md",
            "docs/appendix/memory-retrieval-schema.en.md",
        ),
        "README.ru.md": (
            "docs/appendix/trace-schema.md",
            "docs/appendix/eval-schema.md",
            "docs/appendix/memory-retrieval-schema.md",
        ),
        "README.zh.md": (
            "docs/appendix/trace-schema.zh.md",
            "docs/appendix/eval-schema.zh.md",
            "docs/appendix/memory-retrieval-schema.zh.md",
        ),
        "docs/index.md": (
            "appendix/trace-schema.md",
            "appendix/eval-schema.md",
            "appendix/memory-retrieval-schema.md",
        ),
        "docs/index.en.md": (
            "appendix/trace-schema.en.md",
            "appendix/eval-schema.en.md",
            "appendix/memory-retrieval-schema.en.md",
        ),
        "docs/index.zh.md": (
            "appendix/trace-schema.zh.md",
            "appendix/eval-schema.zh.md",
            "appendix/memory-retrieval-schema.zh.md",
        ),
        "docs/start-here.md": (
            "appendix/trace-schema.md",
            "appendix/eval-schema.md",
            "appendix/memory-retrieval-schema.md",
        ),
        "docs/start-here.en.md": (
            "appendix/trace-schema.en.md",
            "appendix/eval-schema.en.md",
            "appendix/memory-retrieval-schema.en.md",
        ),
        "docs/start-here.zh.md": (
            "appendix/trace-schema.zh.md",
            "appendix/eval-schema.zh.md",
            "appendix/memory-retrieval-schema.zh.md",
        ),
    }

    for path, expected_links in expected_links_by_file.items():
        text = _read(path)
        for link in expected_links:
            assert f"]({link})" in text, (path, link)


def test_reference_layer_surfaces_three_canonical_case_artifacts() -> None:
    required_markers = (
        "Canonical case artifacts",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "approval record",
        "policy bundle",
        "duplicate-ticket recovery evidence",
        "memory/retrieval contract",
        "freshness checks",
        "access control",
        "knowledge provenance",
        "notification side effects",
        "response ownership",
        "post-incident learning",
    )
    checked_files = (
        "docs/reference.md",
        "docs/reference.en.md",
        "docs/reference.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_multilingual_reference_case_artifacts_note_is_localized() -> None:
    russian_text = _read("docs/reference.md")
    chinese_text = _read("docs/reference.zh.md")

    assert "Канонические артефакты сценариев" in russian_text
    assert "канонических сценария (canonical cases)" in russian_text
    assert "запись подтверждения (approval record)" in russian_text
    assert "контракт памяти/поиска (memory/retrieval contract)" in russian_text
    assert "запись инцидента (incident record)" in russian_text

    assert "规范案例工件" in chinese_text
    assert "规范案例（canonical cases）" in chinese_text
    assert "审批记录（approval record）" in chinese_text
    assert "记忆/检索契约（memory/retrieval contract）" in chinese_text
    assert "事件记录（incident record）" in chinese_text

    forbidden_markers = (
        "Три canonical cases",
        "опирается на approval record",
        "требует memory/retrieval contract",
        "связывает incident record",
        "三个 canonical cases",
        "依赖 approval record",
        "需要 memory/retrieval contract",
        "连接 incident record",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_multilingual_reference_support_triage_artifact_route_is_localized() -> None:
    russian_text = _read("docs/reference.md")
    chinese_text = _read("docs/reference.zh.md")

    assert "Артефактный маршрут триажа поддержки (support-triage)" in russian_text
    assert "трассы (traces)" in russian_text
    assert "набор данных оценок (eval dataset)" in russian_text
    assert "пакет политик (policy bundle)" in russian_text
    assert "запись подтверждения (approval record)" in russian_text
    assert "запись инцидента (incident record)" in russian_text
    assert "раскатку изменений (change rollout)" in russian_text
    assert "артефакты жизненного цикла (lifecycle artifacts)" in russian_text
    assert "операции реестра (registry operations)" in russian_text
    assert "инцидент с дублем тикета (duplicate-ticket incident)" in russian_text

    assert "支持分诊工件路线（support-triage）" in chinese_text
    assert "追踪（traces）" in chinese_text
    assert "评测数据集（eval dataset）" in chinese_text
    assert "策略包（policy bundle）" in chinese_text
    assert "审批记录（approval record）" in chinese_text
    assert "事故记录（incident record）" in chinese_text
    assert "变更发布（change rollout）" in chinese_text
    assert "生命周期工件（lifecycle artifacts）" in chinese_text
    assert "注册表运维（registry operations）" in chinese_text
    assert "重复工单事故（duplicate-ticket incident）" in chinese_text

    forbidden_markers = (
        'example "Артефактный маршрут support-triage"',
        "кейс support-triage",
        "страницы про traces, eval dataset",
        "policy bundle, approval record",
        "incident record, change rollout",
        "lifecycle artifacts и registry operations",
        "duplicate-ticket incident из рассказа",
        'example "support-triage 工件路线"',
        "按 support-triage 案例",
        "把 traces、评测数据集",
        "policy bundle、审批记录",
        "registry operations 这些页面",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_multilingual_reference_practice_links_are_localized() -> None:
    russian_text = _read("docs/reference.md")
    chinese_text = _read("docs/reference.zh.md")

    assert "постмортемом (postmortem)" in russian_text
    assert "реестру агентов (agent registry)" in russian_text
    assert "операциям инвентаря (inventory operations)" in russian_text
    assert "Шаблон постмортема (postmortem)" in russian_text
    assert "многоагентных систем (multi-agent systems)" in russian_text

    assert "智能体注册表（agent registry）" in chinese_text
    assert "清单运维（inventory operations）" in chinese_text
    assert "事后复盘（postmortem）模板" in chinese_text
    assert "多智能体（multi-agent）可靠性" in chinese_text

    forbidden_markers = (
        "связи с postmortem",
        "по registry агентов и inventory operations",
        "Шаблон postmortem",
        "multi-agent систем",
        "智能体注册表与清单运维手册",
        "智能体系统事后复盘模板",
        "多智能体可靠性",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_multilingual_reference_safe_agent_schema_spine_is_localized() -> None:
    russian_text = _read("docs/reference.md")
    chinese_text = _read("docs/reference.zh.md")

    assert "Цепочка схем безопасного агента (Safe-agent schema spine)" in russian_text
    assert "архитектуре безопасного агента (safe-agent architecture)" in russian_text
    assert "схему трасс (trace schema)" in russian_text
    assert "схему оценок (eval schema)" in russian_text
    assert "схему памяти/поиска (memory/retrieval schema)" in russian_text
    assert "модель угроз MCP (MCP threat model)" in russian_text
    assert "контракт доверия передачи A2A (A2A handoff trust contract)" in russian_text
    assert "запись вердикта проверяющего (verifier verdict record)" in russian_text
    assert "единые доказательства угроз агенту (unified agent threat evidence)" in russian_text

    assert "安全智能体模式主线（Safe-agent schema spine）" in chinese_text
    assert "安全智能体架构（safe-agent architecture）" in chinese_text
    assert "追踪模式（trace schema）" in chinese_text
    assert "评测模式（eval schema）" in chinese_text
    assert "记忆/检索模式（memory/retrieval schema）" in chinese_text
    assert "MCP 威胁模型（MCP threat model）" in chinese_text
    assert "A2A 移交信任契约（A2A handoff trust contract）" in chinese_text
    assert "验证器裁决记录（verifier verdict record）" in chinese_text
    assert "统一智能体威胁证据（unified agent threat evidence）" in chinese_text

    forbidden_markers = (
        '!!! note "Safe-agent schema spine"',
        "маршрут по safe-agent architecture",
        "рядом [trace schema]",
        "связаны MCP threat model",
        "A2A handoff trust contract, verifier verdict record",
        "memory poisoning review fields и unified agent threat evidence",
        "safe-agent architecture 的短路线",
        "[trace schema]",
        "连接了 MCP threat model",
        "A2A handoff trust contract、verifier verdict record",
        "memory poisoning review fields 和 unified agent threat evidence",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_part_viii_index_surfaces_three_canonical_lifecycle_cases() -> None:
    required_markers = (
        "Canonical lifecycle cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "write-capability change packets",
        "approvals",
        "duplicate-ticket recovery evidence",
        "corpus ownership",
        "freshness review",
        "access control",
        "knowledge provenance",
        "escalation authority",
        "notification side effects",
        "response ownership",
        "post-incident learning",
    )
    checked_files = (
        "docs/book/part-viii/index.md",
        "docs/book/part-viii/index.en.md",
        "docs/book/part-viii/index.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_reference_package_scopes_three_canonical_cases_to_runtime() -> None:
    from agent_runtime_ref.config import load_agent_profile

    agent, _ = load_agent_profile(ROOT / "agent_runtime_ref/configs/agent.yaml")
    required_markers = (
        "Canonical case runtime scope",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "runnable baseline",
        "write capabilities",
        "approvals",
        "duplicate-ticket recovery",
        "coverage lenses",
        "retrieval",
        "memory",
        "freshness",
        "knowledge provenance",
        "notification side effects",
        "response ownership",
        "post-incident learning",
        "runnable configs",
        f"agent_id `{agent.agent_id}`",
        f"`{agent.display_name}`",
        f"owner_team `{agent.owner_team}`",
        f"runtime_principal `{agent.runtime_principal}`",
        "policy, telemetry, lifecycle",
        "registry contracts",
    )
    checked_files = (
        "docs/appendix/reference-package.md",
        "docs/appendix/reference-package.en.md",
        "docs/appendix/reference-package.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_multilingual_reference_package_runtime_scope_note_is_localized() -> None:
    russian_text = _read("docs/appendix/reference-package.md")
    chinese_text = _read("docs/appendix/reference-package.zh.md")

    assert "Канонический runtime-scope сценариев" in russian_text
    assert "исполняемую базовую линию (runnable baseline)" in russian_text
    assert "записывающих возможностей (write capabilities)" in russian_text
    assert "линзами покрытия (coverage lenses)" in russian_text
    assert "поиск (retrieval)" in russian_text
    assert "трассы (traces)" in russian_text

    assert "规范案例运行时范围" in chinese_text
    assert "可运行基线（runnable baseline）" in chinese_text
    assert "写入能力（write capabilities）" in chinese_text
    assert "覆盖视角（coverage lenses）" in chinese_text
    assert "检索（retrieval）" in chinese_text
    assert "追踪（traces）" in chinese_text

    forbidden_markers = (
        "как runnable baseline для write capabilities",
        "остаются coverage lenses",
        "проверяет retrieval, memory",
        "traces, escalation, notification side effects",
        "как runnable configs",
        "作为 runnable baseline，用来承载 write capabilities",
        "仍是同一架构的 coverage lenses",
        "检查 retrieval、memory",
        "检查 traces、escalation",
        "做成 runnable configs",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_policy_bundle_schema_surfaces_three_canonical_policy_cases() -> None:
    required_markers = (
        "Canonical policy cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "write-capability approval policy",
        "idempotency evidence",
        "duplicate-ticket recovery controls",
        "retrieval policy",
        "memory write rules",
        "freshness checks",
        "access control",
        "knowledge provenance",
        "escalation rules",
        "notification side effects",
        "response ownership",
        "post-incident learning gates",
    )
    checked_files = (
        "docs/appendix/policy-bundle-schema.md",
        "docs/appendix/policy-bundle-schema.en.md",
        "docs/appendix/policy-bundle-schema.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_multilingual_policy_bundle_case_note_is_localized() -> None:
    russian_text = _read("docs/appendix/policy-bundle-schema.md")
    chinese_text = _read("docs/appendix/policy-bundle-schema.zh.md")

    assert "Канонические сценарии политик" in russian_text
    assert "Пакет политик (policy bundle)" in russian_text
    assert "политики подтверждения для записывающей возможности" in russian_text
    assert "доказательств идемпотентности (idempotency evidence)" in russian_text
    assert "политики поиска (retrieval policy)" in russian_text
    assert "правил эскалации (escalation rules)" in russian_text

    assert "规范策略案例" in chinese_text
    assert "策略包（policy bundle）" in chinese_text
    assert "写入能力审批策略（write-capability approval policy）" in chinese_text
    assert "幂等证据（idempotency evidence）" in chinese_text
    assert "检索策略（retrieval policy）" in chinese_text
    assert "升级规则（escalation rules）" in chinese_text

    forbidden_markers = (
        "Policy bundle не должен выглядеть",
        "во всех трех canonical cases",
        "требует write-capability approval policy",
        "требует retrieval policy",
        "требует escalation rules",
        "三个 canonical cases 的 policy bundle",
        "需要 write-capability approval policy",
        "需要 retrieval policy",
        "需要 escalation rules",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_approval_schema_surfaces_three_canonical_approval_cases() -> None:
    required_markers = (
        "Canonical approval cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "explicit human approval",
        "idempotency_key",
        "duplicate-ticket recovery evidence",
        "memory writes",
        "access-control exceptions",
        "source visibility decisions",
        "approval trail",
        "escalation authority",
        "notification side effects",
        "response ownership transfer",
        "post-incident learning updates",
    )
    checked_files = (
        "docs/appendix/approval-schema.md",
        "docs/appendix/approval-schema.en.md",
        "docs/appendix/approval-schema.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_multilingual_approval_schema_case_note_is_localized() -> None:
    russian_text = _read("docs/appendix/approval-schema.md")
    chinese_text = _read("docs/appendix/approval-schema.zh.md")

    assert "Канонические сценарии подтверждений" in russian_text
    assert "Запись подтверждения (approval record)" in russian_text
    assert "пути записи (write path)" in russian_text
    assert "явного подтверждения человеком (explicit human approval)" in russian_text
    assert "исключений контроля доступа (access-control exceptions)" in russian_text
    assert "следа подтверждений (approval trail)" in russian_text

    assert "规范审批案例" in chinese_text
    assert "审批记录（approval record）" in chinese_text
    assert "写入路径（write path）" in chinese_text
    assert "明确的人工审批（explicit human approval）" in chinese_text
    assert "访问控制例外（access-control exceptions）" in chinese_text
    assert "审批轨迹（approval trail）" in chinese_text

    forbidden_markers = (
        "Approval record нужен не только для write path",
        "требует explicit human approval",
        "требует approval trail для escalation authority",
        "Approval record 不只服务于 write path",
        "需要 explicit human approval",
        "需要一条 approval trail",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_trace_schema_surfaces_three_canonical_trace_cases() -> None:
    required_markers = (
        "Canonical trace cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "approval events",
        "idempotency_key",
        "tool side effects",
        "duplicate-ticket recovery evidence",
        "retrieval spans",
        "memory access",
        "source attribution",
        "freshness checks",
        "access control decisions",
        "escalation timeline",
        "notification side effects",
        "response ownership",
        "handoff events",
        "post-incident learning",
    )
    checked_files = (
        "docs/appendix/trace-schema.md",
        "docs/appendix/trace-schema.en.md",
        "docs/appendix/trace-schema.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_multilingual_trace_schema_case_note_is_localized() -> None:
    russian_text = _read("docs/appendix/trace-schema.md")
    chinese_text = _read("docs/appendix/trace-schema.zh.md")

    assert "Канонические сценарии трассировки" in russian_text
    assert "акцентов трассировки (trace emphases)" in russian_text
    assert "события подтверждений (approval events)" in russian_text
    assert "спаны поиска (retrieval spans)" in russian_text
    assert "таймлайн эскалации (escalation timeline)" in russian_text

    assert "规范追踪案例" in chinese_text
    assert "追踪重点（trace emphases）" in chinese_text
    assert "审批事件（approval events）" in chinese_text
    assert "检索跨度（retrieval spans）" in chinese_text
    assert "升级时间线（escalation timeline）" in chinese_text

    forbidden_markers = (
        "Три canonical cases требуют разных trace emphases",
        "связывает approval events",
        "сохранять retrieval spans",
        "показывать escalation timeline",
        "三个 canonical cases 需要不同的 trace emphases",
        "把 approval events",
        "保留 retrieval spans",
        "展示 escalation timeline",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_trace_schema_includes_agent_threat_evidence_markers() -> None:
    required_markers = (
        "agent_threat_evidence",
        "unified agent threat evidence",
        "prompt_boundary_event",
        "rejected_instruction_trace",
        "tool_output_sanitized",
        "untrusted_content_marker",
        "policy_decision_trace",
        "retrieval_source_id",
        "freshness_score",
        "quarantine_event",
        "memory_record_id",
        "validation_state",
        "rollback_replay_evidence",
        "tool_call_id",
        "approval_record",
        "argument_validation_result",
        "subject_id",
        "delegation_trace_id",
        "caller_callee_identity_check",
        "step_budget_event",
        "stop_reason",
        "escalation_decision",
        "tenant_id",
        "egress_decision",
        "redaction_dlp_result",
        "cost_budget_event",
        "rate_limit_decision",
        "circuit_breaker_state",
        "handoff_id",
        "containment_state",
        "verifier_verdict",
        "artifact_digest",
        "registry_decision",
        "sandbox_profile_id",
        "decision_trace_id",
        "immutable_log_pointer",
        "evidence_completeness_flag",
    )
    checked_files = (
        "docs/appendix/trace-schema.md",
        "docs/appendix/trace-schema.en.md",
        "docs/appendix/trace-schema.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_trace_schema_includes_mcp_tool_risk_review_fields() -> None:
    required_markers = (
        "mcp_tool_risk_review",
        "threat_class",
        "mcp_server_id",
        "tool_contract_version",
        "registry_owner",
        "scope_review",
        "quarantine_state",
        "evidence_refs",
        "tool poisoning",
        "rug pull attack",
        "tool shadowing",
        "confused deputy",
        "over-scoped tokens",
        "data exfiltration through legitimate channels",
        "supply-chain attack",
        "replay/tampering",
        "sandbox escape",
    )
    checked_files = (
        "docs/appendix/trace-schema.md",
        "docs/appendix/trace-schema.en.md",
        "docs/appendix/trace-schema.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_trace_schema_includes_a2a_handoff_trust_contract_fields() -> None:
    required_markers = (
        "a2a_handoff",
        "A2A handoff trust contract",
        "agent_identity",
        "delegation_chain",
        "allowed_collaboration_graph",
        "inter_agent_authorization",
        "policy_inheritance",
        "non_repudiation",
        "failure_attribution",
    )
    checked_files = (
        "docs/appendix/trace-schema.md",
        "docs/appendix/trace-schema.en.md",
        "docs/appendix/trace-schema.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_trace_schema_includes_memory_poisoning_decision_fields() -> None:
    required_markers = (
        "memory_write_decision",
        "memory poisoning",
        "write_trust_boundary",
        "activation_policy",
        "contamination_scope",
        "policy_influence",
        "provenance_check",
        "quarantine_state",
        "rollback_ref",
    )
    checked_files = (
        "docs/appendix/trace-schema.md",
        "docs/appendix/trace-schema.en.md",
        "docs/appendix/trace-schema.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_trace_schema_includes_governance_action_event_fields() -> None:
    required_markers = (
        "governance_action",
        "governance action record",
        "governance_action_id",
        "source_signal",
        "decision_owner",
        "action_state",
        "evidence_refs",
        "review_deadline",
        "policy_decision_feedback",
        "containment_decision",
        "rollout_gate_input",
        "incident_response_trigger",
        "registry_update_signal",
    )
    checked_files = (
        "docs/appendix/trace-schema.md",
        "docs/appendix/trace-schema.en.md",
        "docs/appendix/trace-schema.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_trace_schema_includes_verifier_verdict_record_fields() -> None:
    required_markers = (
        "verifier verdict record",
        "verdict_id",
        "verifier_id",
        "verifier_contract_version",
        "input_refs",
        "process_score",
        "outcome_score",
        "failure_attribution",
        "blocking_decision",
        "comparison_baseline",
        "reviewer_override",
        "evidence_refs",
    )
    checked_files = (
        "docs/appendix/trace-schema.md",
        "docs/appendix/trace-schema.en.md",
        "docs/appendix/trace-schema.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_eval_schema_surfaces_three_canonical_eval_cases() -> None:
    required_markers = (
        "Canonical eval cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "approval gates",
        "idempotency evidence",
        "retry behavior",
        "duplicate-ticket recovery",
        "retrieval freshness",
        "source attribution",
        "memory provenance",
        "access control",
        "grounded answer quality",
        "escalation timing",
        "notification side effects",
        "response ownership",
        "handoff quality",
        "post-incident learning regressions",
    )
    checked_files = (
        "docs/appendix/eval-schema.md",
        "docs/appendix/eval-schema.en.md",
        "docs/appendix/eval-schema.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_multilingual_eval_schema_case_note_is_localized() -> None:
    russian_text = _read("docs/appendix/eval-schema.md")
    chinese_text = _read("docs/appendix/eval-schema.zh.md")

    assert "Канонические сценарии оценок" in russian_text
    assert "Набор оценок (eval dataset)" in russian_text
    assert "регрессию дублей тикетов (duplicate-ticket regression)" in russian_text
    assert "шлюзы подтверждения (approval gates)" in russian_text
    assert "свежесть поиска (retrieval freshness)" in russian_text
    assert "сроки эскалации (escalation timing)" in russian_text

    assert "规范评测案例" in chinese_text
    assert "评测数据集（eval dataset）" in chinese_text
    assert "重复工单回归（duplicate-ticket regression）" in chinese_text
    assert "审批门禁（approval gates）" in chinese_text
    assert "检索新鲜度（retrieval freshness）" in chinese_text
    assert "升级时序（escalation timing）" in chinese_text

    forbidden_markers = (
        "Eval dataset должен покрывать",
        "только duplicate-ticket regression",
        "проверяет approval gates",
        "проверяет retrieval freshness",
        "проверяет escalation timing",
        "Eval dataset 不应该只覆盖 duplicate-ticket regression",
        "检查 approval gates",
        "检查 retrieval freshness",
        "检查 escalation timing",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_eval_schema_includes_verifier_verdict_record_fields() -> None:
    required_markers = (
        "verifier verdict record",
        "verifier_outputs",
        "verdict_id",
        "verifier_id",
        "verifier_contract_version",
        "input_refs",
        "blocking_decision",
        "comparison_baseline",
        "reviewer_override",
        "verifier_evidence_refs",
    )
    checked_files = (
        "docs/appendix/eval-schema.md",
        "docs/appendix/eval-schema.en.md",
        "docs/appendix/eval-schema.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_incident_record_schema_surfaces_three_canonical_incident_cases() -> None:
    required_markers = (
        "Canonical incident cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "corrective paths",
        "unknown write",
        "idempotency_key",
        "duplicate-ticket recovery",
        "eval/update gate",
        "stale retrieval",
        "source attribution gaps",
        "memory contamination",
        "access control breach",
        "knowledge provenance repair",
        "escalation delay",
        "notification side effects",
        "response ownership gap",
        "handoff failure",
        "post-incident learning update",
    )
    checked_files = (
        "docs/appendix/incident-record-schema.md",
        "docs/appendix/incident-record-schema.en.md",
        "docs/appendix/incident-record-schema.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_multilingual_incident_record_case_note_is_localized() -> None:
    russian_text = _read("docs/appendix/incident-record-schema.md")
    chinese_text = _read("docs/appendix/incident-record-schema.zh.md")

    assert "Канонические сценарии инцидентов" in russian_text
    assert "Запись инцидента (incident record)" in russian_text
    assert "пути исправления (corrective paths)" in russian_text
    assert "запись с неизвестным исходом (unknown write)" in russian_text
    assert "устаревший поиск (stale retrieval)" in russian_text
    assert "задержку эскалации (escalation delay)" in russian_text

    assert "规范事故案例" in chinese_text
    assert "事故记录（incident record）" in chinese_text
    assert "纠正路径（corrective paths）" in chinese_text
    assert "结果未知的写入（unknown write）" in chinese_text
    assert "陈旧检索（stale retrieval）" in chinese_text
    assert "升级延迟（escalation delay）" in chinese_text

    forbidden_markers = (
        "Incident record должен оставлять",
        "разные corrective paths",
        "фиксирует unknown write",
        "фиксирует stale retrieval",
        "фиксирует escalation delay",
        "Incident record 应为三个 canonical cases",
        "不同 corrective paths",
        "记录 unknown write",
        "记录 stale retrieval",
        "记录 escalation delay",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_change_rollout_schema_surfaces_three_canonical_rollout_cases() -> None:
    required_markers = (
        "Canonical rollout cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "readiness signals",
        "duplicate-ticket eval pass",
        "rollback plan",
        "approval readiness",
        "idempotency evidence",
        "retrieval freshness window",
        "source attribution review",
        "memory provenance review",
        "access control signoff",
        "escalation drill",
        "notification side effects review",
        "response ownership readiness",
        "post-incident learning gate",
    )
    checked_files = (
        "docs/appendix/change-rollout-schema.md",
        "docs/appendix/change-rollout-schema.en.md",
        "docs/appendix/change-rollout-schema.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_multilingual_change_rollout_case_note_is_localized() -> None:
    russian_text = _read("docs/appendix/change-rollout-schema.md")
    chinese_text = _read("docs/appendix/change-rollout-schema.zh.md")

    assert "Канонические сценарии раскатки" in russian_text
    assert "Шлюз раскатки (rollout gate)" in russian_text
    assert "сигналы готовности (readiness signals)" in russian_text
    assert "плана отката (rollback plan)" in russian_text
    assert "окна свежести поиска (retrieval freshness window)" in russian_text
    assert "тренировки эскалации (escalation drill)" in russian_text

    assert "规范发布案例" in chinese_text
    assert "发布门禁（rollout gate）" in chinese_text
    assert "就绪信号（readiness signals）" in chinese_text
    assert "回滚计划（rollback plan）" in chinese_text
    assert "检索新鲜度窗口（retrieval freshness window）" in chinese_text
    assert "升级演练（escalation drill）" in chinese_text

    forbidden_markers = (
        "Rollout gate должен проверять",
        "разные readiness signals",
        "требует duplicate-ticket eval pass",
        "требует retrieval freshness window",
        "требует escalation drill",
        "Rollout gate 应为三个 canonical cases",
        "检查不同 readiness signals",
        "需要 duplicate-ticket eval pass",
        "需要 retrieval freshness window",
        "需要 escalation drill",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_lifecycle_artifact_schema_surfaces_three_canonical_lifecycle_cases() -> None:
    required_markers = (
        "Canonical lifecycle cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "artifact chains",
        "change record",
        "approved artifact bundle",
        "approval record",
        "eval dataset",
        "rollout gate",
        "retirement plan",
        "duplicate-ticket guard",
        "retrieval policy",
        "memory policy",
        "source provenance",
        "access-control review",
        "knowledge-base replacement plan",
        "escalation policy",
        "notification capability",
        "response ownership map",
        "handoff artifact",
        "post-incident learning retirement or replacement plan",
    )
    checked_files = (
        "docs/appendix/lifecycle-artifact-schema.md",
        "docs/appendix/lifecycle-artifact-schema.en.md",
        "docs/appendix/lifecycle-artifact-schema.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_multilingual_lifecycle_artifact_case_note_is_localized() -> None:
    russian_text = _read("docs/appendix/lifecycle-artifact-schema.md")
    chinese_text = _read("docs/appendix/lifecycle-artifact-schema.zh.md")

    assert "Канонические сценарии жизненного цикла" in russian_text
    assert "Артефакты жизненного цикла (lifecycle artifacts)" in russian_text
    assert "цепочки артефактов (artifact chains)" in russian_text
    assert "запись изменения (change record)" in russian_text
    assert "политику поиска (retrieval policy)" in russian_text
    assert "политику эскалации (escalation policy)" in russian_text

    assert "规范生命周期案例" in chinese_text
    assert "生命周期工件（lifecycle artifacts）" in chinese_text
    assert "工件链（artifact chains）" in chinese_text
    assert "变更记录（change record）" in chinese_text
    assert "检索策略（retrieval policy）" in chinese_text
    assert "升级策略（escalation policy）" in chinese_text

    forbidden_markers = (
        "Lifecycle artifacts должны удерживать",
        "разные artifact chains",
        "связывает change record",
        "связывает retrieval policy",
        "связывает escalation policy",
        "Lifecycle artifacts 应为三个 canonical cases",
        "不同 artifact chains",
        "把 change record",
        "连接 retrieval policy",
        "连接 escalation policy",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_memory_retrieval_schema_surfaces_three_canonical_memory_cases() -> None:
    required_markers = (
        "Canonical memory cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "memory boundaries",
        "requester context",
        "ticket state",
        "idempotency_key",
        "short-lived working notes",
        "retrieval freshness",
        "source attribution",
        "tenant filters",
        "memory provenance",
        "access control",
        "incident timeline",
        "response ownership",
        "handoff summaries",
        "escalation status",
        "post-incident lessons",
        "transient incident noise",
        "durable truth",
    )
    checked_files = (
        "docs/appendix/memory-retrieval-schema.md",
        "docs/appendix/memory-retrieval-schema.en.md",
        "docs/appendix/memory-retrieval-schema.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_multilingual_memory_retrieval_case_note_is_localized() -> None:
    russian_text = _read("docs/appendix/memory-retrieval-schema.md")
    chinese_text = _read("docs/appendix/memory-retrieval-schema.zh.md")

    assert "Канонические сценарии памяти" in russian_text
    assert "Контракт памяти и поиска (memory and retrieval contract)" in russian_text
    assert "границы памяти (memory boundaries)" in russian_text
    assert "контекст запрашивающего (requester context)" in russian_text
    assert "свежести поиска (retrieval freshness)" in russian_text
    assert "временный шум инцидента (transient incident noise)" in russian_text

    assert "规范记忆案例" in chinese_text
    assert "记忆与检索契约（memory and retrieval contract）" in chinese_text
    assert "记忆边界（memory boundaries）" in chinese_text
    assert "请求者上下文（requester context）" in chinese_text
    assert "检索新鲜度（retrieval freshness）" in chinese_text
    assert "临时事件噪声（transient incident noise）" in chinese_text

    forbidden_markers = (
        "Memory and retrieval contract должен",
        "разные memory boundaries",
        "хранит requester context",
        "требует retrieval freshness",
        "transient incident noise в durable truth",
        "Memory and retrieval contract 应为三个 canonical cases",
        "不同 memory boundaries",
        "保存 requester context",
        "需要 retrieval freshness",
        "transient incident noise 变成 durable truth",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_postmortem_template_surfaces_three_canonical_postmortem_cases() -> None:
    required_markers = (
        "Canonical postmortem cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "failure classes",
        "control loop",
        "duplicate-ticket root cause",
        "approval scope",
        "idempotency_key",
        "side-effect containment",
        "eval/rollout correction",
        "stale source",
        "retrieval freshness",
        "memory provenance",
        "access-control gap",
        "knowledge-base correction",
        "escalation delay",
        "notification side effects",
        "response ownership gap",
        "handoff breakdown",
        "post-incident learning update",
    )
    checked_files = (
        "docs/appendix/postmortem-template.md",
        "docs/appendix/postmortem-template.en.md",
        "docs/appendix/postmortem-template.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_multilingual_postmortem_template_case_note_is_localized() -> None:
    russian_text = _read("docs/appendix/postmortem-template.md")
    chinese_text = _read("docs/appendix/postmortem-template.zh.md")

    assert "Канонические сценарии разбора инцидентов" in russian_text
    assert "Разбор инцидента (postmortem)" in russian_text
    assert "классы отказов (failure classes)" in russian_text
    assert "контур управления (control loop)" in russian_text
    assert "корневую причину дубля тикета (duplicate-ticket root cause)" in russian_text
    assert "задержку эскалации (escalation delay)" in russian_text

    assert "规范事后复盘案例" in chinese_text
    assert "事后复盘（postmortem）" in chinese_text
    assert "失败类别（failure classes）" in chinese_text
    assert "控制循环（control loop）" in chinese_text
    assert "重复工单根因（duplicate-ticket root cause）" in chinese_text
    assert "升级延迟（escalation delay）" in chinese_text

    forbidden_markers = (
        "Postmortem должен возвращать",
        "разные failure classes",
        "в control loop",
        "проверяет duplicate-ticket root cause",
        "проверяет stale source",
        "проверяет escalation delay",
        "Postmortem 应把三个 canonical cases",
        "不同 failure classes",
        "回流到 control loop",
        "检查 duplicate-ticket root cause",
        "检查 stale source",
        "检查 escalation delay",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_incident_response_playbook_surfaces_three_canonical_response_cases() -> None:
    required_markers = (
        "Canonical response cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "containment paths",
        "write capability",
        "approval evidence",
        "idempotency_key",
        "side-effect status",
        "rollout wave",
        "retrieval scope",
        "pauses memory writes",
        "source provenance",
        "tenant boundary evidence",
        "access-control decision",
        "escalation status",
        "notification side effects",
        "response ownership",
        "handoff state",
        "emergency rollback owner",
    )
    checked_files = (
        "docs/appendix/incident-response-playbook.md",
        "docs/appendix/incident-response-playbook.en.md",
        "docs/appendix/incident-response-playbook.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_multilingual_incident_response_playbook_case_note_is_localized() -> None:
    russian_text = _read("docs/appendix/incident-response-playbook.md")
    chinese_text = _read("docs/appendix/incident-response-playbook.zh.md")

    assert "Канонические сценарии реагирования" in russian_text
    assert "Реагирование на инцидент (incident response)" in russian_text
    assert "пути сдерживания (containment paths)" in russian_text
    assert "записывающую возможность (write capability)" in russian_text
    assert "область поиска (retrieval scope)" in russian_text
    assert "статус эскалации (escalation status)" in russian_text

    assert "规范响应案例" in chinese_text
    assert "事件响应（incident response）" in chinese_text
    assert "遏制路径（containment paths）" in chinese_text
    assert "写入能力（write capability）" in chinese_text
    assert "检索范围（retrieval scope）" in chinese_text
    assert "升级状态（escalation status）" in chinese_text

    forbidden_markers = (
        "Incident response должен выбирать",
        "разные containment paths",
        "трех canonical cases",
        "замораживает write capability",
        "ограничивает retrieval scope",
        "фиксирует escalation status",
        "Incident response 应为三个 canonical cases",
        "选择不同 containment paths",
        "冻结 write capability",
        "收窄 retrieval scope",
        "记录 escalation status",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_policy_templates_surface_three_canonical_policy_template_cases() -> None:
    required_markers = (
        "Canonical policy template cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "operational starters",
        "governed write capability",
        "approval boundary",
        "idempotency key",
        "traceable write intent",
        "duplicate-ticket guard",
        "role-scoped retrieval",
        "source references",
        "grounding checks",
        "tenant boundaries",
        "access-denied behavior",
        "controlled handoffs",
        "current owner",
        "notification approval",
        "risky remediation disabled by default",
        "incident trace coverage",
    )
    checked_files = (
        "docs/appendix/policy-templates.md",
        "docs/appendix/policy-templates.en.md",
        "docs/appendix/policy-templates.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)
    deprecated_markers = (
        "Support Triage Agent",
        "Internal Knowledge Agent",
        "Incident Coordination Agent",
    )
    for path in checked_files:
        text = _read(path)
        for marker in deprecated_markers:
            assert marker not in text, (path, marker)


def test_multilingual_policy_templates_case_note_is_localized() -> None:
    russian_text = _read("docs/appendix/policy-templates.md")
    chinese_text = _read("docs/appendix/policy-templates.zh.md")

    assert "Канонические сценарии шаблонов политик" in russian_text
    assert "операционными заготовками (operational starters)" in russian_text
    assert "управляемой записывающей возможности (governed write capability)" in russian_text
    assert "поиска по ролям (role-scoped retrieval)" in russian_text
    assert "управляемых передач (controlled handoffs)" in russian_text

    assert "规范策略模板案例" in chinese_text
    assert "运营起点（operational starters）" in chinese_text
    assert "受治理的写入能力（governed write capability）" in chinese_text
    assert "按角色限定的检索（role-scoped retrieval）" in chinese_text
    assert "受控交接（controlled handoffs）" in chinese_text

    forbidden_markers = (
        "являются operational starters",
        "трех canonical cases",
        "governed write capability, approval boundary",
        "role-scoped retrieval, source references",
        "controlled handoffs, current owner",
        "三个 canonical cases 的 operational starters",
        "从 governed write capability",
        "从 role-scoped retrieval",
        "从 controlled handoffs",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_registry_operations_handbook_surfaces_three_canonical_registry_cases() -> None:
    required_markers = (
        "Canonical registry cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "accountability anchors",
        "write capability",
        "approval mode",
        "idempotency controls",
        "policy bundle",
        "retirement linkage",
        "corpus owner",
        "retrieval policy",
        "tenant scope",
        "source provenance review",
        "freshness review cadence",
        "incident role owner",
        "escalation authority",
        "notification channel ownership",
        "emergency rollback owner",
        "emergency-only capabilities",
    )
    checked_files = (
        "docs/appendix/registry-operations-handbook.md",
        "docs/appendix/registry-operations-handbook.en.md",
        "docs/appendix/registry-operations-handbook.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_multilingual_registry_operations_case_note_is_localized() -> None:
    russian_text = _read("docs/appendix/registry-operations-handbook.md")
    chinese_text = _read("docs/appendix/registry-operations-handbook.zh.md")

    assert "Канонические сценарии реестра" in russian_text
    assert "Запись реестра (registry record)" in russian_text
    assert "якоря ответственности (accountability anchors)" in russian_text
    assert "возможности записи (write capability)" in russian_text
    assert "владельца корпуса (corpus owner)" in russian_text
    assert "владельца экстренного отката (emergency rollback owner)" in russian_text

    assert "规范注册表案例" in chinese_text
    assert "注册表记录（registry record）" in chinese_text
    assert "责任锚点（accountability anchors）" in chinese_text
    assert "写入能力（write capability）" in chinese_text
    assert "语料负责人（corpus owner）" in chinese_text
    assert "紧急回滚负责人（emergency rollback owner）" in chinese_text

    forbidden_markers = (
        "Registry record должен фиксировать",
        "разные accountability anchors",
        "требует owner для write capability",
        "требует corpus owner",
        "требует incident role owner",
        "Registry record 应为三个 canonical cases",
        "不同 accountability anchors",
        "需要 write capability",
        "需要 corpus owner",
        "需要 incident role owner",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_tool_failure_recovery_surfaces_three_canonical_recovery_cases() -> None:
    required_markers = (
        "Canonical recovery cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "failure surfaces",
        "side_effect_unknown",
        "idempotency lookup",
        "duplicate-ticket prevention",
        "manual reconciliation",
        "eval/rollout regression",
        "stale retrieval",
        "source lookup failure",
        "access-denied recovery",
        "memory write rollback",
        "grounded-answer recheck",
        "notification partial delivery",
        "escalation retry",
        "owner handoff repair",
        "emergency rollback decision",
        "post-incident learning capture",
    )
    checked_files = (
        "docs/appendix/tool-failure-recovery.md",
        "docs/appendix/tool-failure-recovery.en.md",
        "docs/appendix/tool-failure-recovery.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_multilingual_tool_failure_recovery_case_note_is_localized() -> None:
    russian_text = _read("docs/appendix/tool-failure-recovery.md")
    chinese_text = _read("docs/appendix/tool-failure-recovery.zh.md")

    assert "Канонические сценарии восстановления" in russian_text
    assert "Ветка восстановления (recovery branch)" in russian_text
    assert "поверхности отказа (failure surfaces)" in russian_text
    assert "поиске по идемпотентности (idempotency lookup)" in russian_text
    assert "устаревшем поиске (stale retrieval)" in russian_text
    assert "частичной доставке уведомлений (notification partial delivery)" in russian_text

    assert "规范恢复案例" in chinese_text
    assert "恢复分支（recovery branch）" in chinese_text
    assert "失败表面（failure surfaces）" in chinese_text
    assert "幂等性查找（idempotency lookup）" in chinese_text
    assert "陈旧检索（stale retrieval）" in chinese_text
    assert "通知部分送达（notification partial delivery）" in chinese_text

    forbidden_markers = (
        "Recovery branch должен",
        "failure surfaces для трех canonical cases",
        "idempotency lookup, duplicate-ticket prevention",
        "stale retrieval, source lookup failure",
        "notification partial delivery, escalation retry",
        "Recovery branch 应区分三个 canonical cases",
        "idempotency lookup、duplicate-ticket prevention",
        "stale retrieval、source lookup failure",
        "notification partial delivery、escalation retry",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_memory_eval_patterns_surface_three_canonical_memory_eval_cases() -> None:
    required_markers = (
        "Canonical memory eval cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "state quality",
        "requester context carryover",
        "ticket state retrieval",
        "idempotency_key",
        "no-write decision",
        "duplicate-ticket regression",
        "retrieval freshness",
        "source attribution",
        "tenant isolation",
        "memory provenance",
        "grounded-answer quality",
        "incident timeline recall",
        "response ownership handoff",
        "escalation status",
        "noisy alert filtering",
        "post-incident lesson retention",
    )
    checked_files = (
        "docs/appendix/memory-eval-patterns.md",
        "docs/appendix/memory-eval-patterns.en.md",
        "docs/appendix/memory-eval-patterns.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_multilingual_memory_eval_patterns_case_note_is_localized() -> None:
    russian_text = _read("docs/appendix/memory-eval-patterns.md")
    chinese_text = _read("docs/appendix/memory-eval-patterns.zh.md")

    assert "Канонические сценарии оценки памяти" in russian_text
    assert "Набор оценок памяти (memory eval suite)" in russian_text
    assert "качество состояния (state quality)" in russian_text
    assert "перенос контекста заявителя (requester context carryover)" in russian_text
    assert "свежесть поиска (retrieval freshness)" in russian_text
    assert "восстановление хронологии инцидента (incident timeline recall)" in russian_text

    assert "规范记忆评测案例" in chinese_text
    assert "记忆评测套件（memory eval suite）" in chinese_text
    assert "状态质量（state quality）" in chinese_text
    assert "请求者上下文延续（requester context carryover）" in chinese_text
    assert "检索新鲜度（retrieval freshness）" in chinese_text
    assert "事件时间线回忆（incident timeline recall）" in chinese_text

    forbidden_markers = (
        "Memory eval suite должен",
        "state quality для трех canonical cases",
        "проверяет requester context carryover",
        "проверяет retrieval freshness",
        "проверяет incident timeline recall",
        "Memory eval suite 应为三个 canonical cases",
        "分别检查 state quality",
        "检查 requester context carryover",
        "检查 retrieval freshness",
        "检查 incident timeline recall",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_causal_debugging_surfaces_three_canonical_causal_cases() -> None:
    required_markers = (
        "Canonical causal cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "decisive edges",
        "retrieved context",
        "approval decision",
        "idempotency_key",
        "tool execution",
        "duplicate-ticket cascade",
        "stale source",
        "retrieval filtering",
        "source attribution",
        "memory write",
        "access-control decision",
        "escalation trigger",
        "notification side effects",
        "handoff edge",
        "response ownership",
        "post-incident learning update",
    )
    checked_files = (
        "docs/appendix/causal-debugging.md",
        "docs/appendix/causal-debugging.en.md",
        "docs/appendix/causal-debugging.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_multilingual_causal_debugging_case_note_is_localized() -> None:
    russian_text = _read("docs/appendix/causal-debugging.md")
    chinese_text = _read("docs/appendix/causal-debugging.zh.md")

    assert "Канонические причинные сценарии" in russian_text
    assert "Причинная отладка (causal debugging)" in russian_text
    assert "решающие связи (decisive edges)" in russian_text
    assert "найденный контекст (retrieved context)" in russian_text
    assert "устаревший источник (stale source)" in russian_text
    assert "триггер эскалации (escalation trigger)" in russian_text

    assert "规范因果案例" in chinese_text
    assert "因果调试（causal debugging）" in chinese_text
    assert "决定性边（decisive edges）" in chinese_text
    assert "检索到的上下文（retrieved context）" in chinese_text
    assert "陈旧来源（stale source）" in chinese_text
    assert "升级触发器（escalation trigger）" in chinese_text

    forbidden_markers = (
        "Causal debugging должен искать",
        "разные decisive edges",
        "отделяет retrieved context",
        "отделяет stale source",
        "отделяет escalation trigger",
        "Causal debugging 应在三个 canonical cases",
        "不同 decisive edges",
        "区分 retrieved context",
        "区分 stale source",
        "区分 escalation trigger",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_cheat_sheets_surface_three_canonical_checklist_cases() -> None:
    required_markers = (
        "Canonical checklist cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "fast route",
        "safety",
        "tool gateway",
        "approval",
        "idempotency",
        "rollout checks",
        "memory",
        "retrieval",
        "source grounding",
        "tenant boundary",
        "observability checks",
        "incident review",
        "response ownership",
        "post-incident learning checks",
    )
    checked_files = (
        "docs/appendix/cheat-sheets.md",
        "docs/appendix/cheat-sheets.en.md",
        "docs/appendix/cheat-sheets.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_multilingual_cheat_sheet_canonical_case_note_is_localized() -> None:
    russian_text = _read("docs/appendix/cheat-sheets.md")
    chinese_text = _read("docs/appendix/cheat-sheets.zh.md")

    assert "Канонические сценарии для проверочных списков" in russian_text
    assert "блоки проверок как быстрый маршрут (fast route)" in russian_text
    assert "Триаж обращений поддержки (Support triage)" in russian_text
    assert "Внутренний ассистент знаний (Internal knowledge assistant)" in russian_text
    assert "Координация инцидентов (Incident coordination)" in russian_text
    assert "безопасности (safety), шлюза инструментов (tool gateway)" in russian_text
    assert "памяти (memory), поиска (retrieval)" in russian_text
    assert "разбора инцидента (incident review)" in russian_text

    assert "规范检查清单案例" in chinese_text
    assert "快速路线（fast route）" in chinese_text
    assert "支持分流（Support triage）" in chinese_text
    assert "内部知识助手（Internal knowledge assistant）" in chinese_text
    assert "事件协调（Incident coordination）" in chinese_text
    assert "安全（safety）、工具网关（tool gateway）" in chinese_text
    assert "记忆（memory）、检索（retrieval）" in chinese_text
    assert "事故复盘（incident review）" in chinese_text

    forbidden_markers = (
        "Используй эти checklist blocks как fast route",
        "начинается с safety, tool gateway, approval",
        "начинается с memory, retrieval, source grounding",
        "начинается с rollout, observability, incident review",
        "Use these checklist blocks 作为三个 canonical cases 的 fast route",
        "从 safety、tool gateway、approval",
        "从 memory、retrieval、source grounding",
        "从 rollout、observability、incident review",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_community_roadmap_surfaces_three_canonical_roadmap_cases() -> None:
    required_markers = (
        "Canonical roadmap cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "next layer of value",
        "richer trace examples",
        "approval policy templates",
        "duplicate-ticket evals",
        "runnable high-risk scenario",
        "knowledge scenario",
        "retrieval policy template",
        "memory eval patterns",
        "source-grounding QA",
        "incident trace examples",
        "escalation/notification templates",
        "response ownership checks",
        "post-incident learning assets",
    )
    checked_files = (
        "docs/appendix/community-roadmap.md",
        "docs/appendix/community-roadmap.en.md",
        "docs/appendix/community-roadmap.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_multilingual_community_roadmap_case_note_is_localized() -> None:
    russian_text = _read("docs/appendix/community-roadmap.md")
    chinese_text = _read("docs/appendix/community-roadmap.zh.md")

    assert "Канонические сценарии дорожной карты" in russian_text
    assert "Дорожная карта (roadmap)" in russian_text
    assert "следующий слой пользы (next layer of value)" in russian_text
    assert "Триаж обращений поддержки (Support triage)" in russian_text
    assert "примерам трасс инцидентов (incident trace examples)" in russian_text
    assert "артефактам обучения после инцидента (post-incident learning assets)" in russian_text

    assert "规范路线图案例" in chinese_text
    assert "路线图（roadmap）" in chinese_text
    assert "下一层价值（next layer of value）" in chinese_text
    assert "支持分流（Support triage）" in chinese_text
    assert "事件追踪示例（incident trace examples）" in chinese_text
    assert "事件后学习资产（post-incident learning assets）" in chinese_text

    forbidden_markers = (
        "Roadmap должен измерять next layer of value",
        "через три canonical cases",
        "задает приоритет для richer trace examples",
        "задает приоритет для knowledge scenario",
        "задает приоритет для incident trace examples",
        "Roadmap 应通过三个 canonical cases 衡量 next layer of value",
        "优先推动 richer trace examples",
        "优先推动 knowledge scenario",
        "优先推动 incident trace examples",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_google_integration_roadmap_surfaces_three_canonical_platform_cases() -> None:
    required_markers = (
        "Canonical Google integration cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "platform-grade ideas",
        "agent identity",
        "least privilege",
        "approval/audit linkage",
        "sandbox profile",
        "high-risk tools",
        "duplicate-ticket controls",
        "context layers",
        "memory governance",
        "retrieval policy",
        "source provenance",
        "tenant-aware access",
        "registry governance",
        "A2A boundaries",
        "continuous controls",
        "rollout gates",
        "escalation traces",
        "response ownership",
    )
    checked_files = (
        "docs/appendix/google-integration-roadmap.md",
        "docs/appendix/google-integration-roadmap.en.md",
        "docs/appendix/google-integration-roadmap.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_multilingual_google_integration_case_note_is_localized() -> None:
    russian_text = _read("docs/appendix/google-integration-roadmap.md")
    chinese_text = _read("docs/appendix/google-integration-roadmap.zh.md")

    assert "Канонические сценарии Google-интеграции" in russian_text
    assert "Дорожная карта Google-интеграции (Google integration roadmap)" in russian_text
    assert "идеи платформенного уровня (platform-grade ideas)" in russian_text
    assert "идентичность агента (agent identity)" in russian_text
    assert "слои контекста (context layers)" in russian_text
    assert "управление реестром (registry governance)" in russian_text

    assert "规范 Google 集成案例" in chinese_text
    assert "Google 集成路线图（Google integration roadmap）" in chinese_text
    assert "平台级想法（platform-grade ideas）" in chinese_text
    assert "智能体身份（agent identity）" in chinese_text
    assert "上下文层（context layers）" in chinese_text
    assert "注册表治理（registry governance）" in chinese_text

    forbidden_markers = (
        "Google integration roadmap полезнее",
        "platform-grade ideas на трех canonical cases",
        "проверяет agent identity",
        "проверяет context layers",
        "проверяет registry governance",
        "Google integration roadmap 在用三个 canonical cases",
        "检查 platform-grade ideas",
        "检查 agent identity",
        "检查 context layers",
        "检查 registry governance",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_research_frontier_surfaces_three_canonical_frontier_cases() -> None:
    required_markers = (
        "Canonical frontier cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "research frontier",
        "promising pattern",
        "production default",
        "agent memory",
        "trace-linked evals",
        "approval gates",
        "duplicate-ticket recovery",
        "rollback cost",
        "hierarchical memory",
        "source provenance",
        "retrieval freshness",
        "tenant-aware access",
        "auditability",
        "causal tracing",
        "multi-agent reliability",
        "handoff contracts",
        "incident review",
        "diagnosable system boundaries",
    )
    checked_files = (
        "docs/appendix/research-frontier.md",
        "docs/appendix/research-frontier.en.md",
        "docs/appendix/research-frontier.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_multilingual_research_frontier_case_note_is_localized() -> None:
    russian_text = _read("docs/appendix/research-frontier.md")
    chinese_text = _read("docs/appendix/research-frontier.zh.md")

    assert "Канонические сценарии исследовательского фронтира" in russian_text
    assert "Исследовательский фронтир (research frontier)" in russian_text
    assert "многообещающий паттерн (promising pattern)" in russian_text
    assert "память агента (agent memory)" in russian_text
    assert "иерархическую память (hierarchical memory)" in russian_text
    assert "причинную трассировку (causal tracing)" in russian_text

    assert "规范前沿案例" in chinese_text
    assert "研究前沿（research frontier）" in chinese_text
    assert "有前景的模式（promising pattern）" in chinese_text
    assert "智能体记忆（agent memory）" in chinese_text
    assert "分层记忆（hierarchical memory）" in chinese_text
    assert "因果追踪（causal tracing）" in chinese_text

    forbidden_markers = (
        "Research frontier стоит фильтровать",
        "через три canonical cases",
        "promising pattern не стал production default",
        "проверяет agent memory",
        "проверяет hierarchical memory",
        "проверяет causal tracing",
        "通过三个 canonical cases 过滤 research frontier",
        "避免 promising pattern 过早变成 production default",
        "检查 agent memory",
        "检查 hierarchical memory",
        "检查 causal tracing",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_language_stack_surfaces_three_canonical_language_cases() -> None:
    required_markers = (
        "Canonical language cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "Language choice",
        "canonical cases",
        "Python/TypeScript",
        "behavior iteration",
        "tool gateway",
        "approval service",
        "idempotency control",
        "audit trail",
        "stricter platform services",
        "retrieval experiments",
        "eval loop",
        "contract layer",
        "memory/index service",
        "source provenance",
        "tenant-aware access",
        "runtime reliability",
        "trace ingestion pipeline",
        "notification safety",
        "response ownership",
        "platform control",
    )
    checked_files = (
        "docs/appendix/rust-vs-python-typescript.md",
        "docs/appendix/rust-vs-python-typescript.en.md",
        "docs/appendix/rust-vs-python-typescript.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_multilingual_language_stack_case_note_is_localized() -> None:
    russian_text = _read("docs/appendix/rust-vs-python-typescript.md")
    chinese_text = _read("docs/appendix/rust-vs-python-typescript.zh.md")

    assert "Канонические сценарии выбора языка" in russian_text
    assert "Выбор языка (Language choice)" in russian_text
    assert "итераций поведения (behavior iteration)" in russian_text
    assert "шлюз инструментов (tool gateway)" in russian_text
    assert "эксперименты поиска (retrieval experiments)" in russian_text
    assert "надежность рантайма (runtime reliability)" in russian_text

    assert "规范语言案例" in chinese_text
    assert "语言选择（Language choice）" in chinese_text
    assert "行为迭代（behavior iteration）" in chinese_text
    assert "工具网关（tool gateway）" in chinese_text
    assert "检索实验（retrieval experiments）" in chinese_text
    assert "运行时可靠性（runtime reliability）" in chinese_text

    forbidden_markers = (
        "Language choice должен",
        "через три canonical cases",
        "для behavior iteration",
        "выносит tool gateway",
        "держит retrieval experiments",
        "runtime reliability, trace ingestion pipeline",
        "Language choice 应该通过三个 canonical cases",
        "做 behavior iteration",
        "把 tool gateway",
        "把 retrieval experiments",
        "runtime reliability、trace ingestion pipeline",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_rust_agent_platforms_surface_three_canonical_platform_cases() -> None:
    required_markers = (
        "Canonical Rust platform cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "Rust infrastructure",
        "canonical cases",
        "tool gateway",
        "policy enforcement service",
        "approval queue service",
        "idempotency semantics",
        "audit pipeline",
        "memory/index layers",
        "retrieval service boundaries",
        "source provenance",
        "tenant isolation",
        "trace processors",
        "long-lived runtime",
        "MCP-compatible integration layer",
        "egress control services",
        "notification safety",
        "control-plane reliability",
    )
    checked_files = (
        "docs/appendix/rust-agent-platforms.md",
        "docs/appendix/rust-agent-platforms.en.md",
        "docs/appendix/rust-agent-platforms.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_multilingual_rust_agent_platforms_case_note_is_localized() -> None:
    russian_text = _read("docs/appendix/rust-agent-platforms.md")
    chinese_text = _read("docs/appendix/rust-agent-platforms.zh.md")

    assert "Канонические сценарии Rust-платформы" in russian_text
    assert "Rust-инфраструктура (Rust infrastructure)" in russian_text
    assert "шлюз инструментов (tool gateway)" in russian_text
    assert "слои памяти/индекса (memory/index layers)" in russian_text
    assert "долгоживущий рантайм (long-lived runtime)" in russian_text

    assert "规范 Rust 平台案例" in chinese_text
    assert "Rust 基础设施（Rust infrastructure）" in chinese_text
    assert "工具网关（tool gateway）" in chinese_text
    assert "记忆/索引层（memory/index layers）" in chinese_text
    assert "长期运行时（long-lived runtime）" in chinese_text

    forbidden_markers = (
        "Rust infrastructure должен",
        "трех canonical cases",
        "проверяет tool gateway",
        "проверяет memory/index layers",
        "проверяет long-lived runtime",
        "Rust infrastructure 应该通过三个 canonical cases",
        "检查 tool gateway",
        "检查 memory/index layers",
        "检查 long-lived runtime",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_glossary_surfaces_three_canonical_routes() -> None:
    required_markers = (
        "Canonical glossary routes",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "fast route",
        "Tool gateway",
        "Approval gate",
        "Policy gate",
        "Capability catalog",
        "Trace",
        "Eval dataset",
        "Retrieval",
        "Long-term memory",
        "Profile memory",
        "Provenance",
        "Trust boundary",
        "Egress policy",
        "Agent runtime",
        "Control plane",
        "Rollout gate",
        "Span",
        "Approved inventory",
    )
    checked_files = (
        "docs/appendix/glossary.md",
        "docs/appendix/glossary.en.md",
        "docs/appendix/glossary.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_multilingual_glossary_routes_note_is_localized() -> None:
    russian_text = _read("docs/appendix/glossary.md")
    chinese_text = _read("docs/appendix/glossary.zh.md")

    assert "Канонические маршруты глоссария" in russian_text
    assert "глоссарий (glossary) как быстрый маршрут (fast route)" in russian_text
    assert "шлюза инструментов (Tool gateway)" in russian_text
    assert "долгосрочной памяти (Long-term memory)" in russian_text
    assert "контура управления (Control plane)" in russian_text
    assert "утвержденного реестра (Approved inventory)" in russian_text

    assert "规范术语表路线" in chinese_text
    assert "术语表（glossary）" in chinese_text
    assert "快速路线（fast route）" in chinese_text
    assert "工具网关（Tool gateway）" in chinese_text
    assert "长期记忆（Long-term memory）" in chinese_text
    assert "控制平面（Control plane）" in chinese_text
    assert "已批准清单（Approved inventory）" in chinese_text

    forbidden_markers = (
        "Используй glossary как fast route",
        "по трем canonical cases",
        "начинается с Tool gateway",
        "начинается с Retrieval",
        "начинается с Agent runtime",
        "Use the glossary 作为三个 canonical cases 的 fast route",
        "从 Tool gateway、Approval gate",
        "从 Retrieval、Long-term memory",
        "从 Agent runtime、Control plane",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_sources_surface_three_canonical_source_routes() -> None:
    required_markers = (
        "Canonical source routes",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "fast route",
        "OWASP",
        "OpenAI agent guides",
        "HITL sources",
        "policy/approval material",
        "trace grading",
        "incident cases",
        "LangGraph memory",
        "OpenAI Agent memory",
        "retrieval/eval sources",
        "provenance-oriented governance",
        "memory research frontier",
        "NIST/AI RMF",
        "Google/Microsoft governance",
        "observability sources",
        "multi-agent reliability research",
        "incident review",
        "rollout/control-plane material",
    )
    checked_files = (
        "docs/appendix/sources.md",
        "docs/appendix/sources.en.md",
        "docs/appendix/sources.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_multilingual_sources_canonical_routes_note_is_localized() -> None:
    russian_text = _read("docs/appendix/sources.md")
    chinese_text = _read("docs/appendix/sources.zh.md")

    assert "Канонические маршруты источников" in russian_text
    assert "источники (sources)" in russian_text
    assert "быстрый маршрут (fast route)" in russian_text
    assert "руководств OpenAI по агентам (OpenAI agent guides)" in russian_text
    assert "памяти LangGraph (LangGraph memory)" in russian_text
    assert "источников наблюдаемости (observability sources)" in russian_text

    assert "规范来源路线" in chinese_text
    assert "来源（sources）" in chinese_text
    assert "快速路线（fast route）" in chinese_text
    assert "OpenAI 智能体指南（OpenAI agent guides）" in chinese_text
    assert "LangGraph 记忆（LangGraph memory）" in chinese_text
    assert "可观测性来源（observability sources）" in chinese_text

    forbidden_markers = (
        "Используй sources как fast route",
        "трех canonical cases",
        "OpenAI agent guides, HITL sources",
        "LangGraph memory, OpenAI Agent memory",
        "observability sources, multi-agent reliability research",
        "Use the sources 作为三个 canonical cases 的 fast route",
        "OpenAI agent guides、HITL sources",
        "LangGraph memory、OpenAI Agent memory",
        "observability sources、multi-agent reliability research",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_sources_include_agent_specific_owasp_security_sources() -> None:
    required_markers = (
        "Agent-specific security",
        "AI Agent Security Cheat Sheet",
        "AI_Agent_Security_Cheat_Sheet.html",
        "MCP Security Cheat Sheet",
        "MCP_Security_Cheat_Sheet.html",
        "LLM Prompt Injection Prevention Cheat Sheet",
        "LLM_Prompt_Injection_Prevention_Cheat_Sheet.html",
        "RAG Security Cheat Sheet",
        "RAG_Security_Cheat_Sheet.html",
        "Governance and baseline controls",
    )
    checked_files = (
        "docs/appendix/sources.md",
        "docs/appendix/sources.en.md",
        "docs/appendix/sources.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_fast_moving_chapters_carry_may_17_review_dates() -> None:
    chapter_bases = (
        "docs/book/part-iv/chapter-9",
        "docs/book/part-v/chapter-13",
        "docs/book/part-viii/chapter-21",
        "docs/book/part-viii/chapter-24",
        "docs/book/part-viii/chapter-25",
        "docs/book/part-viii/chapter-26",
        "docs/book/part-viii/chapter-27",
    )
    expected_by_suffix = {
        ".md": (
            "Последняя редакционная проверка: **17 мая 2026 года**.",
            "Предыдущая проверка: **14 мая 2026 года**.",
            "Следующая плановая проверка: **17 июня 2026 года**.",
        ),
        ".en.md": (
            "Last reviewed: **May 17, 2026**.",
            "Previous review: **May 14, 2026**.",
            "Next scheduled review: **June 17, 2026**.",
        ),
        ".zh.md": (
            "最近一次编辑审查：**2026 年 5 月 17 日**。",
            "上一次审查：**2026 年 5 月 14 日**。",
            "下一次计划审查：**2026 年 6 月 17 日**。",
        ),
    }

    for base in chapter_bases:
        for suffix, expected_markers in expected_by_suffix.items():
            _assert_files_contain_all((f"{base}{suffix}",), expected_markers)


def test_fast_moving_chapter_review_notes_reflect_closed_editorial_work() -> None:
    chapter_bases = (
        "docs/book/part-iv/chapter-9",
        "docs/book/part-v/chapter-13",
        "docs/book/part-viii/chapter-20",
        "docs/book/part-viii/chapter-21",
        "docs/book/part-viii/chapter-22",
        "docs/book/part-viii/chapter-24",
        "docs/book/part-viii/chapter-25",
        "docs/book/part-viii/chapter-26",
        "docs/book/part-viii/chapter-27",
    )
    expected_by_suffix = {
        ".md": (
            "теперь имеют конкретное покрытие контрактами и проверки поверхности документации",
            "ближайшие редакционные задачи",
        ),
        ".en.md": (
            "now have concrete contract coverage and docs-surface guards",
            "near-term editorial work",
        ),
        ".zh.md": (
            "现在都有具体契约覆盖和文档表面检查",
            "近期编辑任务",
        ),
    }

    for base in chapter_bases:
        for suffix, (required, forbidden) in expected_by_suffix.items():
            text = _read(f"{base}{suffix}")
            assert required in text, (base, suffix)
            assert forbidden not in text, (base, suffix)


def test_why_this_book_surfaces_three_canonical_book_cases() -> None:
    required_markers = (
        "Canonical book cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "write actions",
        "approvals",
        "policy gates",
        "duplicate-ticket recovery",
        "audit trail",
        "polished demo",
        "retrieval",
        "memory boundaries",
        "source grounding",
        "provenance",
        "tenant-aware access",
        "prompt tricks",
        "traces",
        "SLOs",
        "escalation",
        "response ownership",
        "rollout control",
        "post-incident learning",
        "production incident",
    )
    checked_files = (
        "docs/appendix/why-this-book.md",
        "docs/appendix/why-this-book.en.md",
        "docs/appendix/why-this-book.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_multilingual_why_this_book_case_note_is_localized() -> None:
    russian_text = _read("docs/appendix/why-this-book.md")
    chinese_text = _read("docs/appendix/why-this-book.zh.md")

    assert "Канонические сценарии книги" in russian_text
    assert "канонических сценариях (canonical cases)" in russian_text
    assert "записывающие действия (write actions)" in russian_text
    assert "поиск (retrieval)" in russian_text
    assert "трассы (traces)" in russian_text
    assert "до production incident" in russian_text

    assert "规范书籍案例" in chinese_text
    assert "规范案例（canonical cases）" in chinese_text
    assert "写入动作（write actions）" in chinese_text
    assert "检索（retrieval）" in chinese_text
    assert "追踪（traces）" in chinese_text
    assert "production incident 之前" in chinese_text

    forbidden_markers = (
        "трех canonical cases",
        "почему write actions",
        "важнее polished demo",
        "почему retrieval, memory boundaries",
        "почему traces, SLOs",
        "三个 canonical cases",
        "为什么 write actions",
        "比 polished demo",
        "为什么 retrieval、memory boundaries",
        "为什么 traces、SLOs",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_publishing_stack_surfaces_three_canonical_publishing_cases() -> None:
    required_markers = (
        "Canonical publishing cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "Publishing stack",
        "canonical cases",
        "reader routes",
        "build pages",
        "fast build",
        "GitHub Pages deployment",
        "search/navigation",
        "policy/approval examples",
        "trace/eval artifacts",
        "Markdown-first authoring",
        "multilingual pages",
        "glossary/search surface",
        "source links",
        "memory/retrieval material",
        "strict build gate",
        "reproducible docs commands",
        "incident/rollout pages",
        "stable navigation",
        "visible changelog-style diffs",
        "migration-risk discipline",
    )
    checked_files = (
        "docs/appendix/stack.md",
        "docs/appendix/stack.en.md",
        "docs/appendix/stack.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_multilingual_publishing_stack_case_note_is_localized() -> None:
    russian_text = _read("docs/appendix/stack.md")
    chinese_text = _read("docs/appendix/stack.zh.md")

    assert "Канонические сценарии публикации" in russian_text
    assert "Стек публикации (Publishing stack)" in russian_text
    assert "маршруты чтения (reader routes)" in russian_text
    assert "быстрой сборки (fast build)" in russian_text
    assert "многоязычных страниц (multilingual pages)" in russian_text
    assert "строгого шлюза сборки (strict build gate)" in russian_text

    assert "规范发布案例" in chinese_text
    assert "发布栈（Publishing stack）" in chinese_text
    assert "阅读路线（reader routes）" in chinese_text
    assert "快速构建（fast build）" in chinese_text
    assert "多语言页面（multilingual pages）" in chinese_text
    assert "严格构建门禁（strict build gate）" in chinese_text

    forbidden_markers = (
        "Publishing stack должен",
        "три canonical cases как reader routes",
        "только build pages",
        "требует fast build",
        "требует Markdown-first authoring",
        "требует strict build gate",
        "Publishing stack 应该把三个 canonical cases",
        "支撑成 reader routes",
        "只是 build pages",
        "需要 fast build",
        "需要 Markdown-first authoring",
        "需要 strict build gate",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_start_here_surfaces_safe_agent_schema_spine() -> None:
    required_markers = (
        "Safe-agent schema spine",
        "trace-schema",
        "eval-schema",
        "memory-retrieval-schema",
        "MCP threat model",
        "A2A handoff trust contract",
        "verifier verdict record",
        "governance action record",
        "memory poisoning review fields",
        "unified agent threat evidence",
    )
    checked_files = (
        "docs/start-here.md",
        "docs/start-here.en.md",
        "docs/start-here.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_multilingual_start_here_safe_agent_schema_route_is_localized() -> None:
    russian_text = _read("docs/start-here.md")
    chinese_text = _read("docs/start-here.zh.md")

    assert "модель угроз MCP (MCP threat model)" in russian_text
    assert "контракт доверия передачи A2A (A2A handoff trust contract)" in russian_text
    assert "запись вердикта проверяющего (verifier verdict record)" in russian_text
    assert "запись действия управления (governance action record)" in russian_text
    assert "поля ревью отравления памяти (memory poisoning review fields)" in russian_text
    assert "единые доказательства угроз агенту (unified agent threat evidence)" in russian_text

    assert "MCP 威胁模型（MCP threat model）" in chinese_text
    assert "A2A 移交信任契约（A2A handoff trust contract）" in chinese_text
    assert "验证器裁决记录（verifier verdict record）" in chinese_text
    assert "治理动作记录（governance action record）" in chinese_text
    assert "记忆投毒审查字段（memory poisoning review fields）" in chinese_text
    assert "统一智能体威胁证据（unified agent threat evidence）" in chinese_text

    forbidden_markers = (
        "проверить MCP threat model",
        "A2A handoff trust contract, verifier verdict record",
        "governance action record, memory poisoning review fields",
        "检查 MCP threat model",
        "A2A handoff trust contract、verifier verdict record",
        "governance action record、memory poisoning review fields",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_reference_surfaces_safe_agent_schema_spine() -> None:
    required_markers = (
        "Safe-agent schema spine",
        "trace schema",
        "eval schema",
        "memory/retrieval schema",
        "MCP threat model",
        "A2A handoff trust contract",
        "verifier verdict record",
        "governance action record",
        "memory poisoning review fields",
        "unified agent threat evidence",
    )
    checked_files = (
        "docs/reference.md",
        "docs/reference.en.md",
        "docs/reference.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_reference_safe_agent_schema_spine_links_are_clickable() -> None:
    expected_links_by_file = {
        "docs/reference.md": (
            "appendix/trace-schema.md",
            "appendix/eval-schema.md",
            "appendix/memory-retrieval-schema.md",
        ),
        "docs/reference.en.md": (
            "appendix/trace-schema.en.md",
            "appendix/eval-schema.en.md",
            "appendix/memory-retrieval-schema.en.md",
        ),
        "docs/reference.zh.md": (
            "appendix/trace-schema.zh.md",
            "appendix/eval-schema.zh.md",
            "appendix/memory-retrieval-schema.zh.md",
        ),
    }

    for path, expected_links in expected_links_by_file.items():
        text = _read(path)
        for link in expected_links:
            assert f"]({link})" in text, (path, link)


def test_whats_new_surfaces_safe_agent_schema_update() -> None:
    required_markers = (
        "Safe-agent schema update",
        "May 19, 2026",
        "19 мая 2026 года",
        "2026 年 5 月 19 日",
        "MCP threat model",
        "mcp_server",
        "A2A handoff trust contract",
        "trust-delegation artifact",
        "defense-in-depth control map",
        "verifier verdict record",
        "governance action record",
        "NIST AI RMF telemetry mapping",
        "memory poisoning review fields",
        "unified agent threat evidence",
        "trace schema",
        "eval schema",
        "memory/retrieval schema",
    )
    checked_files = (
        "docs/whats-new.md",
        "docs/whats-new.en.md",
        "docs/whats-new.zh.md",
    )

    for marker in required_markers[:4]:
        assert any(marker in _read(path) for path in checked_files), marker
    _assert_files_contain_all(checked_files[1:], required_markers[4:])
    ru_text = _read("docs/whats-new.md")
    assert "модель угроз для MCP" in ru_text
    assert "контракт доверия для передачи управления A2A (handoff)" in ru_text
    assert "контракт доверия для A2A handoff" not in ru_text
    assert "контракт доверия для передачи A2A (handoff)" not in ru_text
    assert "артефакт делегирования доверия (trust-delegation)" in ru_text
    assert "артефакт trust-delegation" not in ru_text
    assert "карта эшелонированной защиты (defense-in-depth)" in ru_text
    assert "запись вердикта проверяющего (verifier verdict)" in ru_text
    assert "запись управленческого действия (governance action)" in ru_text
    assert "сопоставление телеметрии с NIST AI RMF" in ru_text
    assert "поля проверки отравления памяти (memory poisoning)" in ru_text
    assert "единая модель доказательств угроз агентам (evidence)" in ru_text
    assert "[схеме trace](appendix/trace-schema.md)" in ru_text
    assert "[схеме eval](appendix/eval-schema.md)" in ru_text
    assert "[схеме memory/retrieval](appendix/memory-retrieval-schema.md)" in ru_text
    assert "карта defense-in-depth controls" not in ru_text
    assert "карта defense-in-depth-контролей" not in ru_text
    assert "verifier verdict record" not in ru_text
    assert "запись verifier verdict" not in ru_text
    assert "governance action record" not in ru_text
    assert "запись governance action" not in ru_text
    assert "модель угроз MCP" not in ru_text
    assert "NIST AI RMF telemetry mapping" not in ru_text
    assert "сопоставление телеметрии NIST AI RMF" not in ru_text
    assert "memory poisoning review fields" not in ru_text
    assert "поля проверки memory poisoning" not in ru_text
    assert "unified agent threat evidence" not in ru_text
    assert "единая evidence-модель угроз агентам" not in ru_text
    assert "[trace schema](appendix/trace-schema.md)" not in ru_text
    assert "[eval schema](appendix/eval-schema.md)" not in ru_text
    assert "[memory/retrieval schema](appendix/memory-retrieval-schema.md)" not in ru_text
    _assert_files_contain_all(("docs/whats-new.md",), required_markers[5:6])

    zh_text = _read("docs/whats-new.zh.md")
    assert '!!! note "安全智能体架构（safe-agent）模式更新"' in zh_text
    assert "安全智能体架构（safe-agent architecture）" in zh_text
    assert "正文（prose）、附录（appendices）和防护检查（guards）" in zh_text
    assert "MCP 威胁模型（MCP threat model）" in zh_text
    assert "`mcp_server` 合约（contract）" in zh_text
    assert "A2A 交接信任合约（A2A handoff trust contract）" in zh_text
    assert "信任委派工件（trust-delegation artifact）" in zh_text
    assert "纵深防御控制图（defense-in-depth control map）" in zh_text
    assert "验证者裁决记录（verifier verdict record）" in zh_text
    assert "治理动作记录（governance action record）" in zh_text
    assert "NIST AI RMF 遥测映射（NIST AI RMF telemetry mapping）" in zh_text
    assert "记忆投毒审查字段（memory poisoning review fields）" in zh_text
    assert "统一智能体威胁证据（unified agent threat evidence）" in zh_text
    assert "[跟踪模式（trace schema）](appendix/trace-schema.zh.md)" in zh_text
    assert "[评测模式（eval schema）](appendix/eval-schema.zh.md)" in zh_text
    assert (
        "[记忆/检索模式（memory/retrieval schema）]"
        "(appendix/memory-retrieval-schema.zh.md)"
        in zh_text
    )
    assert '!!! note "Safe-agent schema update"' not in zh_text
    assert "safe-agent architecture 的 prose、appendices 和 guards" not in zh_text
    assert "MCP threat model 与 `mcp_server` contract" not in zh_text
    assert "`mcp_server` 合同（contract）" not in zh_text
    assert "A2A handoff trust contract 与 trust-delegation artifact" not in zh_text
    assert "A2A 交接信任合同（A2A handoff trust contract）" not in zh_text
    assert "defense-in-depth control map、verifier verdict record" not in zh_text
    assert "memory poisoning review fields 和 unified agent threat evidence" not in zh_text
    assert "[trace schema](appendix/trace-schema.zh.md)" not in zh_text
    assert "[eval schema](appendix/eval-schema.zh.md)" not in zh_text
    assert "[memory/retrieval schema](appendix/memory-retrieval-schema.zh.md)" not in zh_text


def test_whats_new_safe_agent_schema_update_links_are_clickable() -> None:
    expected_links_by_file = {
        "docs/whats-new.md": (
            "appendix/trace-schema.md",
            "appendix/eval-schema.md",
            "appendix/memory-retrieval-schema.md",
        ),
        "docs/whats-new.en.md": (
            "appendix/trace-schema.en.md",
            "appendix/eval-schema.en.md",
            "appendix/memory-retrieval-schema.en.md",
        ),
        "docs/whats-new.zh.md": (
            "appendix/trace-schema.zh.md",
            "appendix/eval-schema.zh.md",
            "appendix/memory-retrieval-schema.zh.md",
        ),
    }

    for path, expected_links in expected_links_by_file.items():
        text = _read(path)
        for link in expected_links:
            assert f"]({link})" in text, (path, link)


def test_whats_new_surfaces_canonical_case_update() -> None:
    required_markers = (
        "Canonical case update",
        "May 15, 2026",
        "15 мая 2026 года",
        "2026 年 5 月 15 日",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "book chapters",
        "public entry points",
        "reference pages",
        "appendix artifacts",
        "coverage guards",
        "chapters",
        "appendix pages",
    )
    checked_files = (
        "docs/whats-new.md",
        "docs/whats-new.en.md",
        "docs/whats-new.zh.md",
    )

    for marker in required_markers[:4]:
        assert any(marker in _read(path) for path in checked_files), marker
    _assert_files_contain_all(checked_files[1:], required_markers[4:7])
    _assert_files_contain_all(checked_files[1:], required_markers[7:])
    ru_text = _read("docs/whats-new.md")
    assert "Триаж обращений поддержки (Support triage)" in ru_text
    assert "внутренний ассистент знаний (Internal knowledge assistant)" in ru_text
    assert "координация инцидентов (Incident coordination)" in ru_text
    assert "главах книги" in ru_text
    assert "публичных точках входа" in ru_text
    assert "справочных страницах" in ru_text
    assert "артефактах приложений" in ru_text
    assert "проверки покрытия защищают главы и страницы приложений" in ru_text
    assert "**Support triage**, **Internal knowledge assistant**" not in ru_text
    assert "book chapters" not in ru_text
    assert "public entry points" not in ru_text
    assert "reference pages" not in ru_text
    assert "appendix artifacts" not in ru_text
    assert "chapters и appendix pages" not in ru_text
    assert "coverage guards" not in ru_text

    zh_text = _read("docs/whats-new.zh.md")
    assert '!!! note "规范案例更新"' in zh_text
    assert "三个规范案例（canonical cases）路线图" in zh_text
    assert "支持分流（Support triage）" in zh_text
    assert "内部知识助手（Internal knowledge assistant）" in zh_text
    assert "事件协调（Incident coordination）" in zh_text
    assert "章节（book chapters）" in zh_text
    assert "公共入口（public entry points）" in zh_text
    assert "参考页（reference pages）" in zh_text
    assert "附录工件（appendix artifacts）" in zh_text
    assert "覆盖率守卫（coverage guards）" in zh_text
    assert "章节与附录页面（appendix pages）丢失这些路线" in zh_text
    assert '!!! note "Canonical case update"' not in zh_text
    assert "三个 canonical cases 地图" not in zh_text
    assert "三个规范案例（canonical cases）地图" not in zh_text
    assert "**Support triage**、**Internal knowledge assistant**" not in zh_text
    assert "出现在 book chapters" not in zh_text
    assert "coverage guards 会防止 chapters" not in zh_text
    assert "章节（chapters）与附录页面" not in zh_text


def test_book_improvement_blueprint_reflects_safe_agent_schema_spine() -> None:
    required_markers = (
        "Implementation status, 20 May 2026",
        "MCP threat model",
        "mcp_server",
        "A2A handoff trust contract",
        "trust-delegation artifact",
        "unified agent threat evidence",
        "defense-in-depth control map",
        "verifier verdict record",
        "governance action record",
        "NIST AI RMF telemetry mapping",
        "memory poisoning review fields",
        "trace schema",
        "eval schema",
        "memory/retrieval schema",
    )

    _assert_files_contain_all(("docs/book-improvement-blueprint.md",), required_markers)


def test_book_improvement_blueprint_schema_spine_links_are_clickable() -> None:
    required_links = (
        "appendix/trace-schema.md",
        "appendix/eval-schema.md",
        "appendix/memory-retrieval-schema.md",
    )
    text = _read("docs/book-improvement-blueprint.md")

    for link in required_links:
        assert f"]({link})" in text, link


def test_editorial_artifacts_use_current_canonical_cases() -> None:
    checked_files = (
        "docs/book-improvement-blueprint.md",
        "docs/publisher-ready-toc.md",
        "docs/reader-journey-map.md",
    )
    required_markers = (
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
    )
    deprecated_markers = (
        "Support triage agent",
        "Internal enterprise knowledge assistant",
        "Approval-bound high-risk action agent",
        "high-risk action / approval-bound agent",
        "support triage, internal knowledge, incident coordination",
        "Support Triage",
        "Internal Knowledge",
        "Incident Coordination",
    )

    _assert_files_contain_all(checked_files, required_markers)
    for path in checked_files:
        text = _read(path)
        for marker in deprecated_markers:
            assert marker not in text, (path, marker)


def test_chapter_1_has_sample_chapter_ending_template() -> None:
    expected = {
        "docs/book/part-i/chapter-1.md": (
            "Шаблон завершения главы",
            "Что запомнить",
            "Типичные ошибки",
            "Что проверить в своей системе",
            "Companion assets",
            "Что читать дальше",
        ),
        "docs/book/part-i/chapter-1.en.md": (
            "Chapter ending template",
            "What to remember",
            "Common mistakes",
            "What to check in your system",
            "Companion assets",
            "What to read next",
        ),
        "docs/book/part-i/chapter-1.zh.md": (
            "章节结尾模板",
            "要记住什么",
            "常见错误",
            "检查自己的系统",
            "Companion assets",
            "接下来读什么",
        ),
    }

    for path, markers in expected.items():
        _assert_files_contain_all((path,), markers)


def test_chinese_entry_surfaces_disclose_draft_localization_status() -> None:
    checked_files = (
        "docs/index.zh.md",
        "docs/start-here.zh.md",
        "docs/book/plan.zh.md",
    )
    required_markers = (
        "中文本地化预览",
        "最终中文版",
        "正式出版前",
    )
    forbidden_markers = (
        "Draft localization preview",
        "draft localization preview",
        "finished Chinese edition",
    )

    for path in checked_files:
        text = _read(path)
        for marker in required_markers:
            assert marker in text, (path, marker)
        for marker in forbidden_markers:
            assert marker not in text, (path, marker)


def test_governance_aware_telemetry_contract_is_documented() -> None:
    required_fields = (
        "Governance-aware telemetry",
        "policy_decision_feedback",
        "containment_decision",
        "rollout_gate_input",
        "incident_response_trigger",
        "registry_update_signal",
        "governance_action_id",
        "source_signal",
        "decision_owner",
        "action_state",
        "evidence_refs",
        "review_deadline",
    )
    checked_files = (
        "docs/book/part-viii/chapter-26.md",
        "docs/book/part-viii/chapter-26.en.md",
        "docs/book/part-viii/chapter-26.zh.md",
    )

    for path in checked_files:
        _assert_files_contain_all((path,), required_fields)


def test_chapter_26_governance_telemetry_maps_to_nist_ai_rmf() -> None:
    required_fields = (
        "Mapping the Loop to NIST AI RMF",
        "Govern",
        "Map",
        "Measure",
        "Manage",
        "decision_owner",
        "review_deadline",
        "source_signal",
        "inventory coverage",
        "bypass-path telemetry",
        "evidence_refs",
        "verifier outputs",
        "coverage ratios",
        "drift signals",
        "detection scenarios",
        "policy_decision_feedback",
        "containment_decision",
        "rollout_gate_input",
        "incident_response_trigger",
        "control action",
        "[^nist-ai-rmf]",
    )
    checked_files = (
        "docs/book/part-viii/chapter-26.md",
        "docs/book/part-viii/chapter-26.en.md",
        "docs/book/part-viii/chapter-26.zh.md",
    )

    _assert_files_contain_all(checked_files, required_fields)


def test_verifier_contract_fields_are_documented() -> None:
    required_fields = (
        "rubric_version",
        "process_score",
        "outcome_score",
        "failure_attribution",
        "judge_human_agreement",
        "false_positive_budget",
        "false_negative_budget",
        "calibration_dataset_id",
        "replay_protocol",
        "verdict_id",
        "verifier_id",
        "verifier_contract_version",
        "input_refs",
        "evidence_refs",
        "blocking_decision",
        "comparison_baseline",
        "reviewer_override",
    )
    checked_files = (
        "docs/book/part-v/chapter-13.md",
        "docs/book/part-v/chapter-13.en.md",
        "docs/book/part-v/chapter-13.zh.md",
    )

    for path in checked_files:
        _assert_files_contain_all((path,), required_fields)


def test_agent_threat_model_matrix_covers_required_classes() -> None:
    required_threats = (
        "Prompt injection",
        "Indirect injection",
        "RAG poisoning",
        "Memory poisoning",
        "Tool abuse",
        "Confused deputy",
        "Excessive agency",
        "Data exfiltration",
        "Denial of wallet",
        "Cascading multi-agent failure",
        "Supply-chain compromise",
        "Missing audit trail",
        "Evidence / telemetry",
        "unified agent threat evidence model",
        "prompt_boundary_event",
        "retrieval_source_id",
        "memory_record_id",
        "delegation_trace_id",
        "tenant_id",
        "cost_budget_event",
        "decision_trace_id",
    )
    checked_files = (
        "docs/book/part-ii/chapter-3.md",
        "docs/book/part-ii/chapter-3.en.md",
        "docs/book/part-ii/chapter-3.zh.md",
    )

    for path in checked_files:
        _assert_files_contain_all((path,), required_threats)


def test_chapter_3_defense_in_depth_map_covers_control_layers() -> None:
    required_markers = (
        "defense_in_depth_map:",
        "ingress_control:",
        "content_policy_and_tenant_scope",
        "context_boundary:",
        "trusted_untrusted_content_labels",
        "retrieval_memory_gate:",
        "source_provenance_ttl_and_write_review",
        "model_gateway_policy:",
        "instruction_hierarchy_and_safety_policy",
        "tool_gateway_approval:",
        "risk_tier_arguments_and_human_gate",
        "mcp_a2a_boundary:",
        "server_contract_and_delegation_contract",
        "egress_filter:",
        "redaction_dlp_and_output_validation",
        "trace_evidence:",
        "agent_threat_evidence_and_governance_action",
        "trace schema",
    )
    checked_files = (
        "docs/book/part-ii/chapter-3.md",
        "docs/book/part-ii/chapter-3.en.md",
        "docs/book/part-ii/chapter-3.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_chapter_3_unified_threat_evidence_trace_links_are_clickable() -> None:
    expected_links_by_file = {
        "docs/book/part-ii/chapter-3.md": "../../appendix/trace-schema.md",
        "docs/book/part-ii/chapter-3.en.md": "../../appendix/trace-schema.en.md",
        "docs/book/part-ii/chapter-3.zh.md": "../../appendix/trace-schema.zh.md",
    }

    for path, expected_link in expected_links_by_file.items():
        assert f"]({expected_link})" in _read(path), (path, expected_link)


def test_mcp_threat_model_matrix_covers_required_attacks() -> None:
    expected = {
        "docs/book/part-iv/chapter-9.md": "MCP threat model matrix",
        "docs/book/part-iv/chapter-9.en.md": "MCP Threat Model Matrix",
        "docs/book/part-iv/chapter-9.zh.md": "MCP 威胁模型矩阵",
    }
    required_markers = (
        "MCP threat model",
        "tool poisoning",
        "rug pull attack",
        "tool shadowing",
        "confused deputy",
        "over-scoped tokens",
        "data exfiltration through legitimate channels",
        "supply-chain attack",
        "replay/tampering",
        "sandbox escape",
        "telemetry",
    )

    for path, heading in expected.items():
        _assert_files_contain_all((path,), (heading, *required_markers))


def test_chapter_9_mcp_server_contract_covers_required_controls() -> None:
    expected_headings = {
        "docs/book/part-iv/chapter-9.md": "Минимальный контракт MCP server",
        "docs/book/part-iv/chapter-9.en.md": "Minimal MCP Server Contract",
        "docs/book/part-iv/chapter-9.zh.md": "最小 MCP server contract",
    }
    required_fields = (
        "mcp_server:",
        "owner:",
        "approved_registry_id:",
        "schema_hash:",
        "tool_definition_hash:",
        "allowed_origins:",
        "auth_mode:",
        "token_scope:",
        "token_ttl:",
        "user_delegation_required:",
        "server_isolation_profile:",
        "return_value_filtering:",
        "replay_protection:",
        "schema_change_requires_review:",
        "tool schema injection",
        "prompt injection",
    )

    for path, heading in expected_headings.items():
        _assert_files_contain_all((path,), (heading, *required_fields))


def test_chapter_9_mcp_threat_model_trace_links_are_clickable() -> None:
    expected_links_by_file = {
        "docs/book/part-iv/chapter-9.md": "../../appendix/trace-schema.md",
        "docs/book/part-iv/chapter-9.en.md": "../../appendix/trace-schema.en.md",
        "docs/book/part-iv/chapter-9.zh.md": "../../appendix/trace-schema.zh.md",
    }

    for path, expected_link in expected_links_by_file.items():
        assert f"]({expected_link})" in _read(path), (path, expected_link)


def test_mcp_a2a_security_governance_sections_are_present() -> None:
    expected = {
        "docs/book/part-iv/chapter-9.md": (
            "MCP — это security boundary",
            "tool descriptions и tool return values",
        ),
        "docs/book/part-iv/chapter-9.en.md": (
            "MCP Is a Security Boundary",
            "tool descriptions and tool return values",
        ),
        "docs/book/part-iv/chapter-9.zh.md": (
            "MCP 是安全边界",
            "tool descriptions 和 tool return values",
        ),
        "docs/book/part-iv/practical-mcp-a2a.md": (
            "A2A требует governance",
            "A2A handoff trust contract",
            "delegated authority",
            "agent identity",
            "delegation chain",
            "allowed collaboration graph",
            "inter-agent authorization",
            "policy inheritance",
            "non-repudiation",
            "failure attribution",
        ),
        "docs/book/part-iv/practical-mcp-a2a.en.md": (
            "A2A Needs Governance",
            "A2A handoff trust contract",
            "delegated authority",
            "agent identity",
            "delegation chain",
            "allowed collaboration graph",
            "inter-agent authorization",
            "policy inheritance",
            "non-repudiation",
            "failure attribution",
        ),
        "docs/book/part-iv/practical-mcp-a2a.zh.md": (
            "A2A 需要治理",
            "A2A handoff trust contract",
            "delegated authority",
            "agent identity",
            "delegation chain",
            "allowed collaboration graph",
            "inter-agent authorization",
            "policy inheritance",
            "non-repudiation",
            "failure attribution",
        ),
    }

    for path, markers in expected.items():
        _assert_files_contain_all((path,), markers)


def test_practical_a2a_trust_delegation_contract_covers_required_controls() -> None:
    required_fields = (
        "A2A trust and delegation artifact",
        "a2a_trust_delegation:",
        "remote_agent_id:",
        "remote_agent_owner:",
        "trust_tier:",
        "allowed_tasks:",
        "forbidden_tasks:",
        "delegation_depth:",
        "context_sharing_policy:",
        "memory_sharing_policy:",
        "tool_access_via_remote_agent:",
        "approval_propagation:",
        "audit_correlation_id:",
        "failure_attribution:",
        "revocation_policy:",
        "delegation laundering",
        "context over-sharing",
        "remote-agent impersonation",
        "unbounded delegation chains",
        "conflicting actions",
        "lost accountability",
        "cross-agent prompt injection",
    )
    checked_files = (
        "docs/book/part-iv/practical-mcp-a2a.md",
        "docs/book/part-iv/practical-mcp-a2a.en.md",
        "docs/book/part-iv/practical-mcp-a2a.zh.md",
    )

    _assert_files_contain_all(checked_files, required_fields)


def test_practical_a2a_handoff_trust_trace_links_are_clickable() -> None:
    expected_links_by_file = {
        "docs/book/part-iv/practical-mcp-a2a.md": "../../appendix/trace-schema.md",
        "docs/book/part-iv/practical-mcp-a2a.en.md": "../../appendix/trace-schema.en.md",
        "docs/book/part-iv/practical-mcp-a2a.zh.md": "../../appendix/trace-schema.zh.md",
    }

    for path, expected_link in expected_links_by_file.items():
        assert f"]({expected_link})" in _read(path), (path, expected_link)


def test_chapter_1_decision_frame_is_extraction_safe() -> None:
    checked_files = (
        "docs/book/part-i/chapter-1.md",
        "docs/book/part-i/chapter-1.en.md",
        "docs/book/part-i/chapter-1.zh.md",
    )
    forbidden_table_headers = (
        "| Как выглядит задача |",
        "| If the task looks like this |",
        "| 任务看起来像什么 |",
    )
    required_text_markers = (
        "Короткая текстовая формула",
        "Text-only formula",
        "文本版公式",
    )

    for path in checked_files:
        text = _read(path)
        assert not any(header in text for header in forbidden_table_headers), path
    for path, marker in zip(checked_files, required_text_markers, strict=True):
        assert marker in _read(path), (path, marker)


def test_fast_moving_pages_have_may_2026_review_metadata() -> None:
    fast_moving_pages = (
        "docs/book/part-iv/chapter-9.md",
        "docs/book/part-iv/chapter-9.en.md",
        "docs/book/part-iv/chapter-9.zh.md",
        "docs/book/part-v/chapter-13.md",
        "docs/book/part-v/chapter-13.en.md",
        "docs/book/part-v/chapter-13.zh.md",
        "docs/book/part-viii/chapter-20.md",
        "docs/book/part-viii/chapter-20.en.md",
        "docs/book/part-viii/chapter-20.zh.md",
        "docs/book/part-viii/chapter-21.md",
        "docs/book/part-viii/chapter-21.en.md",
        "docs/book/part-viii/chapter-21.zh.md",
        "docs/book/part-viii/chapter-22.md",
        "docs/book/part-viii/chapter-22.en.md",
        "docs/book/part-viii/chapter-22.zh.md",
        "docs/book/part-viii/chapter-24.md",
        "docs/book/part-viii/chapter-24.en.md",
        "docs/book/part-viii/chapter-24.zh.md",
        "docs/book/part-viii/chapter-25.md",
        "docs/book/part-viii/chapter-25.en.md",
        "docs/book/part-viii/chapter-25.zh.md",
        "docs/book/part-viii/chapter-26.md",
        "docs/book/part-viii/chapter-26.en.md",
        "docs/book/part-viii/chapter-26.zh.md",
        "docs/book/part-viii/chapter-27.md",
        "docs/book/part-viii/chapter-27.en.md",
        "docs/book/part-viii/chapter-27.zh.md",
    )
    stale_markers = (
        "11 апреля 2026 года",
        "April 11, 2026",
        "2026 年 4 月 11 日",
    )

    for path in fast_moving_pages:
        text = _read(path)
        assert not any(marker in text for marker in stale_markers), path
        assert any(
            marker in text
            for marker in (
                "14 мая 2026 года",
                "May 14, 2026",
                "2026 年 5 月 14 日",
            )
        ), path

    _assert_files_contain_all(
        (
            "docs/appendix/sources.md",
            "docs/appendix/sources.en.md",
            "docs/appendix/sources.zh.md",
            "docs/whats-new.md",
            "docs/whats-new.en.md",
            "docs/whats-new.zh.md",
        ),
        ("2026",),
    )
    assert "22 апреля 2026 года" not in _read("docs/appendix/sources.md")
    assert "April 22, 2026" not in _read("docs/appendix/sources.en.md")
    assert "2026 年 4 月 22 日" not in _read("docs/appendix/sources.zh.md")
    assert "29 апреля 2026 года" not in _read("docs/whats-new.md")
    assert "April 29, 2026" not in _read("docs/whats-new.en.md")
    assert "2026 年 4 月 29 日" not in _read("docs/whats-new.zh.md")


def test_evidence_model_spine_is_present_in_key_chapters() -> None:
    expected = {
        "docs/book/part-i/chapter-1.md": "Модель доказательности этой главы",
        "docs/book/part-i/chapter-1.en.md": "Evidence Model for This Chapter",
        "docs/book/part-i/chapter-1.zh.md": "本章的证据模型",
        "docs/book/part-i/chapter-2.md": "Модель доказательности этой главы",
        "docs/book/part-i/chapter-2.en.md": "Evidence Model for This Chapter",
        "docs/book/part-i/chapter-2.zh.md": "本章的证据模型",
        "docs/book/part-v/chapter-13.md": "Модель доказательности этой главы",
        "docs/book/part-v/chapter-13.en.md": "Evidence Model for This Chapter",
        "docs/book/part-v/chapter-13.zh.md": "本章的证据模型",
        "docs/book/part-viii/chapter-25.md": "Модель доказательности этой главы",
        "docs/book/part-viii/chapter-25.en.md": "Evidence Model for This Chapter",
        "docs/book/part-viii/chapter-25.zh.md": "本章的证据模型",
        "docs/book/part-viii/chapter-26.md": "Модель доказательности этой главы",
        "docs/book/part-viii/chapter-26.en.md": "Evidence Model for This Chapter",
        "docs/book/part-viii/chapter-26.zh.md": "本章的证据模型",
        "docs/book/part-viii/chapter-27.md": "Модель доказательности этой главы",
        "docs/book/part-viii/chapter-27.en.md": "Evidence Model for This Chapter",
        "docs/book/part-viii/chapter-27.zh.md": "本章的证据模型",
    }

    for path, heading in expected.items():
        assert heading in _read(path), path


def test_book_numbered_subsections_do_not_render_as_top_level_duplicates() -> None:
    for path in (ROOT / "docs/book").rglob("*.md"):
        top_level_numbers = []
        for line in path.read_text(encoding="utf-8").splitlines():
            assert not re.match(r"^## \d+\.\d+\. ", line), path
            match = re.match(r"^## (\d+)\. ", line)
            if match:
                top_level_numbers.append(match.group(1))

        duplicates = {number for number in top_level_numbers if top_level_numbers.count(number) > 1}
        assert not duplicates, (path, sorted(duplicates, key=int))


def test_trace_schema_path_and_trace_id_errors_are_documented() -> None:
    required_errors = (
        "Telemetry path must be a string or path-like object",
        "Trace ID request must be a string",
    )
    checked_files = (
        "docs/appendix/trace-schema.md",
        "docs/appendix/trace-schema.en.md",
        "docs/appendix/trace-schema.zh.md",
    )

    _assert_files_contain_all(checked_files, required_errors)


def test_eval_schema_session_eval_errors_are_documented() -> None:
    required_errors = (
        "Session eval specs must be a mapping",
        "Session eval spec must be a mapping",
        "Session eval spec key must be a string",
        "Session eval spec key must not be empty",
        "Session eval spec keys must be unique",
    )
    checked_files = (
        "docs/appendix/eval-schema.md",
        "docs/appendix/eval-schema.en.md",
        "docs/appendix/eval-schema.zh.md",
    )

    _assert_files_contain_all(checked_files, required_errors)


def test_trace_schema_tool_model_errors_are_documented() -> None:
    required_errors = (
        "Tool request capability name must be a string",
        "Tool request capability name must not be empty",
        "Tool request arguments must be a mapping",
        "Tool request argument key must be a string",
        "Tool request argument key must not be empty",
        "Tool request argument keys must be unique",
        "Tool request argument value must be a string: {argument_key}",
        "Tool result status must be a string",
        "Tool result status must not be empty",
        "Tool result payload must be a mapping",
        "Tool result payload key must be a string",
        "Tool result payload key must not be empty",
        "Tool result payload keys must be unique",
        "Tool result payload value must be a string: {payload_key}",
    )
    checked_files = (
        "docs/appendix/trace-schema.md",
        "docs/appendix/trace-schema.en.md",
        "docs/appendix/trace-schema.zh.md",
    )

    _assert_files_contain_all(checked_files, required_errors)


def test_policy_schema_runtime_policy_errors_are_documented() -> None:
    required_errors = (
        "'capabilities' must be a mapping",
        "Policy action must be a string",
        "Policy action is not supported: {action}",
        "Policy field must be a string: {field}",
        "Policy field is required: {field}",
    )
    checked_files = (
        "docs/appendix/policy-bundle-schema.md",
        "docs/appendix/policy-bundle-schema.en.md",
        "docs/appendix/policy-bundle-schema.zh.md",
    )

    _assert_files_contain_all(checked_files, required_errors)


def test_memory_schema_loader_root_error_is_documented() -> None:
    checked_files = (
        "docs/appendix/memory-retrieval-schema.md",
        "docs/appendix/memory-retrieval-schema.en.md",
        "docs/appendix/memory-retrieval-schema.zh.md",
    )

    for path in checked_files:
        assert "Memory store config must be a mapping" in _read(path), path


def test_approval_schema_delegated_authorization_errors_are_documented() -> None:
    required_errors = (
        "approvals.delegated_authorization must be a mapping",
        "approvals.delegated_authorization must be DelegatedAuthorizationPolicy",
        "delegated_authorization.require_principal_binding must be a boolean",
        "delegated_authorization.require_scope_visibility must be a boolean",
    )
    checked_files = (
        "docs/appendix/approval-schema.md",
        "docs/appendix/approval-schema.en.md",
        "docs/appendix/approval-schema.zh.md",
    )

    _assert_files_contain_all(checked_files, required_errors)


def test_reference_package_has_reader_route_contract() -> None:
    required_markers = (
        "Reader-route contract",
        "Quick start",
        "Architecture map",
        "CLI examples",
        "Config contracts",
        "Advanced lifecycle-controls",
        "Runtime internals",
    )
    checked_files = (
        "docs/appendix/reference-package.md",
        "docs/appendix/reference-package.en.md",
        "docs/appendix/reference-package.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_reference_package_rollout_errors_are_documented() -> None:
    required_errors = (
        "Rollout policy must be RolloutPolicy",
        "Rollout readiness must be RolloutReadiness",
        "Rollout readiness flag must be a boolean: {field}",
    )
    checked_files = (
        "docs/appendix/reference-package.md",
        "docs/appendix/reference-package.en.md",
        "docs/appendix/reference-package.zh.md",
    )

    _assert_files_contain_all(checked_files, required_errors)


def test_reference_package_controls_lifecycle_errors_are_documented() -> None:
    required_errors = (
        "Controls inventory must be ApprovedInventory",
        "Controls catalog must be CapabilityCatalog",
        "Controls policy must be ControlsPolicy",
        "Controls inventory_drift must be InventoryDrift",
        "Lifecycle change must be ChangeRecord",
        "Lifecycle retirement plan must be RetirementPlan",
        "Assessment signals must be a mapping",
        "Assessment signal key must be a string",
        "Assessment signal key must not be empty",
        "Assessment signal keys must be unique",
        "Assessment signal value must be a boolean: {field}",
    )
    checked_files = (
        "docs/appendix/reference-package.md",
        "docs/appendix/reference-package.en.md",
        "docs/appendix/reference-package.zh.md",
    )

    _assert_files_contain_all(checked_files, required_errors)


def test_reference_package_cli_boundary_errors_are_documented() -> None:
    required_errors = (
        "CLI field is not supported: {field}={value}; expected one of: {expected}",
        "CLI field must be an integer: {field}",
        "CLI field must be non-negative: {field}",
        "Signal key must not be empty: {raw_signal!r}",
        "Unsupported boolean value in signal: {raw_signal!r}",
    )
    checked_files = (
        "docs/appendix/reference-package.md",
        "docs/appendix/reference-package.en.md",
        "docs/appendix/reference-package.zh.md",
    )

    _assert_files_contain_all(checked_files, required_errors)


def test_reference_package_model_output_errors_are_documented() -> None:
    required_errors = (
        "Model step must return ModelOutput",
        "Model output text must be a string",
        "Model output tool_request must be ToolRequest",
    )
    checked_files = (
        "docs/appendix/reference-package.md",
        "docs/appendix/reference-package.en.md",
        "docs/appendix/reference-package.zh.md",
    )

    _assert_files_contain_all(checked_files, required_errors)


def test_reference_package_lifecycle_runtime_control_fields_are_documented() -> None:
    required_fields = (
        "pause_allowed",
        "resume_allowed",
        "background_mode_allowed",
        "max_wait_seconds",
        "on_expiry",
        "contract_version",
        "capability_session_owner",
        "capability_sessions",
        "delegated_authorization",
    )
    checked_files = (
        "docs/appendix/reference-package.md",
        "docs/appendix/reference-package.en.md",
        "docs/appendix/reference-package.zh.md",
    )

    for path in checked_files:
        text = _read(path)
        lifecycle_section = text.split("inspect-lifecycle", maxsplit=1)[1]
        for field in required_fields:
            assert f"`{field}`" in lifecycle_section, (path, field)


def test_reference_package_export_events_identity_fields_are_documented() -> None:
    required_fields = (
        "session_id",
        "tenant_id",
        "principal_id",
        "agent_id",
        "authorization_mode",
        "delegated_principal_id",
        "delegated_scope",
    )
    checked_files = (
        "docs/appendix/reference-package.md",
        "docs/appendix/reference-package.en.md",
        "docs/appendix/reference-package.zh.md",
    )

    for path in checked_files:
        text = _read(path)
        export_events_section = text.split("export-events", maxsplit=1)[1]
        for field in required_fields:
            assert field in export_events_section, (path, field)


def test_reference_package_eval_artifact_fields_are_documented() -> None:
    required_fields = (
        "session",
        "eval",
        "scenario",
        "labels",
        "expected_outcomes",
        "grading_rules",
        "request_agent_id",
        "user_input",
    )
    checked_files = (
        "docs/appendix/reference-package.md",
        "docs/appendix/reference-package.en.md",
        "docs/appendix/reference-package.zh.md",
    )

    for path in checked_files:
        text = _read(path)
        eval_section = text.split("export-eval-dataset", maxsplit=1)[1]
        for field in required_fields:
            assert f"`{field}`" in eval_section, (path, field)


def test_markdown_rendering_regression_patterns_are_absent() -> None:
    checked_files = [
        "docs/book/part-i/chapter-1.en.md",
        "docs/book/part-i/chapter-1.md",
        "docs/book/part-i/chapter-1.zh.md",
        "docs/book/part-i/chapter-2.en.md",
        "docs/book/part-i/chapter-2.md",
        "docs/book/part-i/chapter-2.zh.md",
        "docs/whats-new.en.md",
        "docs/whats-new.md",
        "docs/whats-new.zh.md",
        "docs/appendix/reference-package.en.md",
        "docs/appendix/reference-package.md",
        "docs/appendix/reference-package.zh.md",
    ]
    forbidden_patterns = (
        "Why it matters: -",
        "Почему это важно: -",
        "为什么重要： -",
        "Layer What it does Why it hurts",
        "If the task looks like this Start with this Why",
        "Как выглядит задача С чего начинать Почему",
        "任务看起来像什么 从哪里开始 为什么",
        "delegated authorization assumptions explicit: which principal delegated access, whether "
        "that authorization may survive pause/resume, and what the runtime does if delegated "
        "access is revoked before the action completes.\n- [lifecycle.py]",
    )

    for path in checked_files:
        text = _read(path)
        for pattern in forbidden_patterns:
            assert pattern not in text, (path, pattern)
