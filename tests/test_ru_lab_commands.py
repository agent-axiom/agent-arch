import json
from pathlib import Path
from textwrap import dedent

from docs.publisher.tools import verify_ru_lab_commands as verifier

REPO_ROOT = Path(__file__).resolve().parents[1]
VERIFIER_PATH = REPO_ROOT / "docs/publisher/tools/verify_ru_lab_commands.py"


def test_ru_lab_command_verifier_is_available() -> None:
    assert VERIFIER_PATH.is_file(), f"missing verifier: {VERIFIER_PATH}"


def test_extracts_fenced_and_indented_shell_blocks_only_from_laboratories() -> None:
    markdown = dedent(
        r"""
        ```console
        python -m agent_runtime_ref outside-the-labs
        ```

        ### Лабораторная работа 2\. Подтверждение

        ```bash
        uv run python -m agent_runtime_ref inspect-agent
        uv run python -m agent_runtime_ref inspect-approvals \
          --trace-id trace-lab-02
        ```

        ```python
        print("not a shell block")
        ```

        ### Лабораторная работа 3. Память

        **Команды.**

            .venv/bin/python -m agent_runtime_ref inspect-memory --tenant-id tenant-acme
            python -m agent_runtime_ref inspect-memory --tenant-id tenant-beta

        # Часть IV

        ```sh
        python -m agent_runtime_ref outside-the-labs-again
        ```
        """
    )

    blocks = verifier.extract_lab_shell_blocks(markdown)
    commands = verifier.extract_runtime_commands(blocks)

    assert [(block.lab_number, block.kind) for block in blocks] == [
        (2, "bash"),
        (3, "indented"),
    ]
    assert [command.lab_number for command in commands] == [2, 2, 3, 3]
    assert commands[1].argv[-2:] == ("--trace-id", "trace-lab-02")
    assert all("outside-the-labs" not in command.text for command in commands)


def test_shell_syntax_error_names_the_laboratory_and_command() -> None:
    markdown = dedent(
        """
        ### Лабораторная работа 4. Расследование

        ```sh
        if true; then
          python -m agent_runtime_ref inspect-agent
        ```
        """
    )

    report = verifier.verify_text(
        markdown,
        repo_root=REPO_ROOT,
        shells=("sh",),
        run_smoke=False,
    )

    assert not report.ok
    diagnostic = report.format_issues()
    assert "Лабораторная работа 4" in diagnostic
    assert "if true; then" in diagnostic
    assert "sh -n" in diagnostic


def test_default_shell_syntax_uses_only_available_checkers(monkeypatch) -> None:
    markdown = dedent(
        """
        ### Лабораторная работа 2. Переносимая проверка

        ```sh
        python -m agent_runtime_ref inspect-agent
        ```
        """
    )
    system_sh = verifier.shutil.which("sh")
    assert system_sh is not None
    monkeypatch.setattr(
        verifier.shutil,
        "which",
        lambda shell: system_sh if shell == "sh" else None,
    )

    report = verifier.verify_text(
        markdown,
        repo_root=REPO_ROOT,
        run_smoke=False,
    )

    assert report.ok, report.format_issues()


def test_explicit_missing_shell_remains_an_error(monkeypatch) -> None:
    markdown = dedent(
        """
        ### Лабораторная работа 2. Явная проверка

        ```sh
        python -m agent_runtime_ref inspect-agent
        ```
        """
    )
    monkeypatch.setattr(verifier.shutil, "which", lambda _shell: None)

    report = verifier.verify_text(
        markdown,
        repo_root=REPO_ROOT,
        shells=("zsh",),
        run_smoke=False,
    )

    assert not report.ok
    assert "required syntax checker is unavailable: zsh" in report.format_issues()


def test_smoke_executes_only_allowlisted_runtime_commands_in_clean_tmp(
    tmp_path: Path,
) -> None:
    sentinel = tmp_path / "must-survive.txt"
    sentinel.write_text("untouched", encoding="utf-8")
    markdown = dedent(
        f"""
        ### Лабораторная работа 2. Безопасный smoke

        ```sh
        rm -f {sentinel}
        uv run python -m agent_runtime_ref inspect-agent
        ```
        """
    )

    report = verifier.verify_text(
        markdown,
        repo_root=REPO_ROOT,
        shells=("sh",),
        run_smoke=True,
    )

    assert report.ok, report.format_issues()
    assert sentinel.read_text(encoding="utf-8") == "untouched"
    assert len(report.smoke_results) == 1
    result = report.smoke_results[0]
    assert result.returncode == 0
    assert result.cwd != REPO_ROOT
    assert not result.cwd.exists()


def test_smoke_replaces_variable_config_dir_with_clean_repo_copy() -> None:
    markdown = dedent(
        """
        ### Лабораторная работа 2. Временная конфигурация

        ```sh
        LAB_CONFIG=$(mktemp -d)
        cp -R agent_runtime_ref/configs/. "$LAB_CONFIG/"
        uv run python -m agent_runtime_ref check-controls \
          --config-dir "$LAB_CONFIG"
        ```
        """
    )

    report = verifier.verify_text(
        markdown,
        repo_root=REPO_ROOT,
        shells=("sh",),
        run_smoke=True,
    )

    assert report.ok, report.format_issues()
    assert len(report.smoke_results) == 1
    payload = json.loads(report.smoke_results[0].stdout)
    assert payload["healthy"] is True
    assert payload["missing_controls"] == []


def test_subshell_scenario_keeps_runtime_command_directly_parseable() -> None:
    markdown = dedent(
        r"""
        ### Лабораторная работа 2. Самодостаточный сценарий

        ```sh
        (
        set -eu
        LAB_PREFIX="${TMPDIR:-/tmp}/agent-arch-lab-02."
        LAB_CONFIG=
        cleanup_lab_config() {
          case "${LAB_CONFIG:-}" in
            "") ;;
            "$LAB_PREFIX"[A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9])
              rm -rf "${LAB_CONFIG:?}"
              LAB_CONFIG=
              ;;
            *) return 1 ;;
          esac
        }
        trap cleanup_lab_config 0
        if ! LAB_CONFIG=$(mktemp -d "${LAB_PREFIX}XXXXXX"); then
          exit 1
        fi
        case "$LAB_CONFIG" in
          "$LAB_PREFIX"[A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9]) ;;
          *) exit 1 ;;
        esac
        cp -R agent_runtime_ref/configs/. "$LAB_CONFIG/"
        uv run python -m agent_runtime_ref check-controls \
          --config-dir "$LAB_CONFIG"
        )
        ```
        """
    )

    report = verifier.verify_text(
        markdown,
        repo_root=REPO_ROOT,
        shells=("sh",),
        run_smoke=True,
    )

    assert report.ok, report.format_issues()
    assert len(report.runtime_commands) == 1
    assert report.runtime_commands[0].argv[:2] == (
        "check-controls",
        "--config-dir",
    )
    assert len(report.smoke_results) == 1


def test_variable_config_dirs_receive_independent_full_copies(tmp_path: Path) -> None:
    first = verifier.RuntimeCommand(
        lab_number=2,
        text=('uv run python -m agent_runtime_ref check-controls --config-dir "$LAB_CONFIG"'),
        argv=("check-controls", "--config-dir", "$LAB_CONFIG"),
        line=10,
    )
    second = verifier.RuntimeCommand(
        lab_number=2,
        text=('uv run python -m agent_runtime_ref check-controls --config-dir "${LAB_CONFIG}"'),
        argv=("check-controls", "--config-dir", "${LAB_CONFIG}"),
        line=20,
    )

    first_argv = verifier._prepare_smoke_argv(
        first,
        cwd=tmp_path,
        repo_root=REPO_ROOT,
    )
    first_config = Path(first_argv[first_argv.index("--config-dir") + 1])
    assert first_config != REPO_ROOT / "agent_runtime_ref/configs"
    assert {path.name for path in first_config.iterdir() if path.is_file()} == {
        path.name for path in (REPO_ROOT / "agent_runtime_ref/configs").iterdir() if path.is_file()
    }
    (first_config / "capabilities.yaml").write_text(
        "capabilities: {}\n",
        encoding="utf-8",
    )

    second_argv = verifier._prepare_smoke_argv(
        second,
        cwd=tmp_path,
        repo_root=REPO_ROOT,
    )
    second_config = Path(second_argv[second_argv.index("--config-dir") + 1])
    assert second_config != first_config
    assert (second_config / "capabilities.yaml").read_bytes() == (
        REPO_ROOT / "agent_runtime_ref/configs/capabilities.yaml"
    ).read_bytes()


def test_non_allowlisted_runtime_command_is_rejected_with_context() -> None:
    markdown = dedent(
        """
        ### Лабораторная работа 6. Жизненный цикл

        ```zsh
        python -m agent_runtime_ref delete-production
        ```
        """
    )

    report = verifier.verify_text(
        markdown,
        repo_root=REPO_ROOT,
        shells=("sh",),
        run_smoke=True,
    )

    assert not report.ok
    diagnostic = report.format_issues()
    assert "Лабораторная работа 6" in diagnostic
    assert "python -m agent_runtime_ref delete-production" in diagnostic
    assert "allowlist" in diagnostic


def test_current_ru_manuscript_commands_pass_syntax_and_clean_room_smoke() -> None:
    manuscript = REPO_ROOT / "docs/publisher/ru-manuscript-editorial-2026-07-13.md"

    report = verifier.verify_manuscript(manuscript, repo_root=REPO_ROOT)

    assert report.ok, report.format_issues()
    assert {command.lab_number for command in report.runtime_commands} == {
        2,
        3,
        4,
        5,
        6,
        7,
        8,
    }
    assert len(report.runtime_commands) == 23
    assert report.smoke_results
