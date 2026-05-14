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


def test_publisher_packet_has_public_link_availability_record() -> None:
    required_markers = (
        "Public Link Availability Record",
        "Last checked: **2026-05-14**",
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
