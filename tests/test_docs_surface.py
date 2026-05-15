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


def test_public_book_canonical_redirects_are_configured() -> None:
    mkdocs_config = _load_mkdocs_config()
    scripts = mkdocs_config["extra_javascript"]

    assert "javascripts/canonical-redirects.js" in scripts

    redirect_script = _read("docs/javascripts/canonical-redirects.js")
    for route in ('"/book"', '"/en/book"', '"/zh/book"'):
        assert route in redirect_script
    assert 'projectPrefix = "/agent-arch"' in redirect_script


def _canonical_redirects_for(pathname: str, search: str = "", hash_: str = "") -> list[str]:
    node = shutil.which("node")
    if node is None:
        pytest.skip("node is required to execute canonical-redirects.js")

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


def test_book_improvement_blueprint_records_review_remediation_status() -> None:
    required_markers = (
        "Implementation status, 15 May 2026",
        "P0:",
        "P1:",
        "P2:",
        "P3:",
        "draft-localization status",
        "MCP security boundary",
        "three canonical case spines",
        "publisher packet is drafted and internally gated",
        "Still blocked before external submission",
    )

    _assert_files_contain_all(("docs/book-improvement-blueprint.md",), required_markers)


def test_publisher_packet_has_core_positioning_and_companion_boundary() -> None:
    required_markers = (
        "Publisher Packet Draft",
        "Positioning",
        "One-Page Positioning Memo Draft",
        "Print Manuscript Shape",
        "Online Companion Boundary",
        "Working title: **Secure AI Agent Architecture**",
        "Subtitle:** From prompt demos to governed production systems.",
        "Primary reader",
        "Unique promise",
        "Companion assets",
        "Keep schemas, runtime command details, long checklists, and source catalogs in the online companion.",
        "runnable `agent_runtime_ref` package",
        "command-output field lists and validation-error catalogs",
        "any print sample that depends on live site navigation",
    )

    _assert_files_contain_all(("docs/publisher-ready-toc.md",), required_markers)


def test_publisher_packet_has_blocker_waiver_decision_log() -> None:
    required_markers = (
        "Blocker Waiver / Decision Log Draft",
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
        "not externally sendable",
        "Author bio and credential framing",
        "Independent sample copy-edit",
        "Sample selection",
        "Target editor / imprint formatting",
        "Owner/input needed",
        "Packet action when closed",
        "explicitly waived by the author",
    )

    _assert_files_contain_all(("docs/publisher-ready-toc.md",), required_markers)


def test_publisher_packet_has_sample_copy_edit_handoff_brief() -> None:
    required_markers = (
        "Sample Copy-Edit Handoff Brief Draft",
        "Copy-edit scope",
        "sentence flow",
        "opening hook",
        "paragraph cadence",
        "Do not rewrite",
        "workflow-first / governed-systems thesis",
        "Questions for the editor",
        "Return format",
        "top 5 changes",
        "No-go signals",
    )

    _assert_files_contain_all(("docs/publisher-ready-toc.md",), required_markers)


def test_publisher_packet_has_public_link_availability_record() -> None:
    required_markers = (
        "Public Link Availability Record",
        "Last checked: **2026-05-15**",
        "publisher-packet-2026-05",
        "public book site",
        "Chapter 1 sample",
        "Chapter 13 technical sample",
        "reference runtime source",
        "runtime README",
        "runtime configs",
        "runtime tests",
        "HTTP 200",
    )

    _assert_files_contain_all(("docs/publisher-ready-toc.md",), required_markers)


def test_publisher_packet_has_target_editor_formatting_brief() -> None:
    required_markers = (
        "Target Editor / Imprint Formatting Brief Draft",
        "Inputs to collect",
        "editor name",
        "imprint",
        "submission channel",
        "attachment rules",
        "sample-chapter policy",
        "Formatting decisions",
        "secure-ai-agent-architecture-proposal-publisher-packet-2026-05.pdf",
        "Tailoring rules",
        "No-go signals",
    )

    _assert_files_contain_all(("docs/publisher-ready-toc.md",), required_markers)


def test_publisher_packet_has_author_bio_input_brief() -> None:
    required_markers = (
        "Author Bio Input Brief Draft",
        "Required inputs",
        "preferred author name",
        "production/engineering background",
        "public project links",
        "Tone constraints",
        "avoid inflated authority claims",
        "Bio slots to prepare",
        "50-word short bio",
        "100-word proposal bio",
        "No-go signals",
    )

    _assert_files_contain_all(("docs/publisher-ready-toc.md",), required_markers)


def test_publisher_packet_has_sample_chapter_export_manifest() -> None:
    required_markers = (
        "Sample Chapter Export Manifest Draft",
        "Primary sample",
        "docs/book/part-i/chapter-1.en.md",
        "https://agent-axiom.github.io/agent-arch/en/book/part-i/chapter-1/",
        "Secondary technical sample",
        "docs/book/part-v/chapter-13.en.md",
        "https://agent-axiom.github.io/agent-arch/en/book/part-v/chapter-13/",
        "publisher-packet-2026-05",
        "Export metadata to include",
        "Pre-export checks",
        "technical-credibility reason",
    )

    _assert_files_contain_all(("docs/publisher-ready-toc.md",), required_markers)


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


def test_publisher_packet_has_submission_release_discipline() -> None:
    required_markers = (
        "Submission Release Discipline Draft",
        "publisher-packet-2026-05",
        "Freeze scope before sending",
        "Pre-send gates",
        "fresh availability check",
        "draft localization preview",
        "No-go signals",
    )

    _assert_files_contain_all(("docs/publisher-ready-toc.md",), required_markers)


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
        "incident-state events",
    )
    checked_files = (
        "docs/book/part-v/chapter-11.md",
        "docs/book/part-v/chapter-11.en.md",
        "docs/book/part-v/chapter-11.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


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


def test_chapter_15_golden_paths_thread_three_canonical_cases() -> None:
    required_markers = (
        "Golden-path case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "anti-zoo strategy",
        "workflow-agent template",
        "approved write gateway",
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


def test_chapter_19_adlc_threads_three_canonical_cases() -> None:
    required_markers = (
        "ADLC case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "lifecycle state model",
        "release-bearing surfaces",
        "write-capability contract",
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


def test_chapter_21_assurance_threads_three_canonical_cases() -> None:
    required_markers = (
        "Assurance case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "finding and response record",
        "containment paths",
        "duplicate-outcome detection",
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


def test_chapter_22_supply_chain_threads_three_canonical_cases() -> None:
    required_markers = (
        "Supply-chain case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "approved artifact bundle",
        "provenance",
        "capability contract",
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


def test_chapter_25_control_evals_threads_three_canonical_cases() -> None:
    required_markers = (
        "Control-eval case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "eval gate and verifier contract",
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
        "notification delivery",
        "post-incident control changes",
    )
    checked_files = (
        "docs/book/part-viii/chapter-26.md",
        "docs/book/part-viii/chapter-26.en.md",
        "docs/book/part-viii/chapter-26.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


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
        "internal knowledge assistant",
        "incident coordination",
        "deprecated write paths",
        "paused approvals",
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


def test_chapter_27_registry_threads_three_canonical_cases() -> None:
    required_markers = (
        "Registry case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "write-capability owners",
        "approval mode",
        "retirement plan",
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


def test_chapter_7_retrieval_threads_three_canonical_cases() -> None:
    required_markers = (
        "Retrieval case-spine note",
        "Support triage",
        "internal knowledge assistant",
        "incident coordination",
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
        "internal knowledge assistant",
        "incident coordination",
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


def test_evidence_spine_threads_three_canonical_cases() -> None:
    required_markers = (
        "Case-spine routing note",
        "Support triage",
        "internal knowledge assistant",
        "incident coordination",
        "approvals",
        "retrieval provenance",
        "response ownership",
        "post-incident rollout judgment",
    )
    checked_files = (
        "docs/book/part-v/evidence-spine.md",
        "docs/book/part-v/evidence-spine.en.md",
        "docs/book/part-v/evidence-spine.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


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
        "policy, telemetry, lifecycle",
        "registry contracts",
    )
    checked_files = (
        "docs/appendix/reference-package.md",
        "docs/appendix/reference-package.en.md",
        "docs/appendix/reference-package.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


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
        "Draft localization preview",
        "finished Chinese edition",
        "正式出版前",
    )

    for path in checked_files:
        _assert_files_contain_all((path,), required_markers)


def test_governance_aware_telemetry_contract_is_documented() -> None:
    required_fields = (
        "Governance-aware telemetry",
        "policy_decision_feedback",
        "containment_decision",
        "rollout_gate_input",
        "incident_response_trigger",
        "registry_update_signal",
    )
    checked_files = (
        "docs/book/part-viii/chapter-26.md",
        "docs/book/part-viii/chapter-26.en.md",
        "docs/book/part-viii/chapter-26.zh.md",
    )

    for path in checked_files:
        _assert_files_contain_all((path,), required_fields)


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
    )
    checked_files = (
        "docs/book/part-ii/chapter-3.md",
        "docs/book/part-ii/chapter-3.en.md",
        "docs/book/part-ii/chapter-3.zh.md",
    )

    for path in checked_files:
        _assert_files_contain_all((path,), required_threats)


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
            "delegated authority",
        ),
        "docs/book/part-iv/practical-mcp-a2a.en.md": (
            "A2A Needs Governance",
            "delegated authority",
        ),
        "docs/book/part-iv/practical-mcp-a2a.zh.md": (
            "A2A 需要治理",
            "delegated authority",
        ),
    }

    for path, markers in expected.items():
        _assert_files_contain_all((path,), markers)


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
