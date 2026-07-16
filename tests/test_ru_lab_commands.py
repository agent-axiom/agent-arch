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
