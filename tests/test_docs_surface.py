import re
from pathlib import Path

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


def test_public_book_canonical_redirects_are_configured() -> None:
    mkdocs_config = _load_mkdocs_config()
    scripts = mkdocs_config["extra_javascript"]

    assert "javascripts/canonical-redirects.js" in scripts

    redirect_script = _read("docs/javascripts/canonical-redirects.js")
    for route in ('"/book"', '"/en/book"', '"/zh/book"'):
        assert route in redirect_script
    assert 'projectPrefix = "/agent-arch"' in redirect_script


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

    for path in checked_files:
        text = _read(path)
        for error in required_errors:
            assert error in text, (path, error)


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

    for path in checked_files:
        text = _read(path)
        for error in required_errors:
            assert error in text, (path, error)


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

    for path in checked_files:
        text = _read(path)
        for error in required_errors:
            assert error in text, (path, error)


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

    for path in checked_files:
        text = _read(path)
        for error in required_errors:
            assert error in text, (path, error)


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

    for path in checked_files:
        text = _read(path)
        for error in required_errors:
            assert error in text, (path, error)


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

    for path in checked_files:
        text = _read(path)
        for error in required_errors:
            assert error in text, (path, error)


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

    for path in checked_files:
        text = _read(path)
        for error in required_errors:
            assert error in text, (path, error)


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

    for path in checked_files:
        text = _read(path)
        for error in required_errors:
            assert error in text, (path, error)


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
