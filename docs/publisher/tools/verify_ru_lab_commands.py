"""Verify literal shell commands in the Russian manuscript laboratories.

The verifier never executes a shell block. Shells are invoked with ``-n`` for
syntax-only parsing, and only explicitly allowlisted ``agent_runtime_ref``
commands are selected for subprocess smoke tests.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

SHELL_LANGUAGES = frozenset({"bash", "console", "sh", "shell", "zsh"})
DEFAULT_SHELL_CANDIDATES = ("sh", "zsh")
SAFE_RUNTIME_SUBCOMMANDS = frozenset(
    {
        "check-change",
        "check-controls",
        "check-retirement",
        "check-rollout",
        "export-eval-dataset",
        "export-events",
        "export-session",
        "inspect-agent",
        "inspect-approvals",
        "inspect-lifecycle",
        "inspect-memory",
        "inspect-trace",
        "replay-run",
        "resolve-approval",
        "simulate-run",
    }
)
_LAB_HEADING = re.compile(r"^(?P<marks>#{2,6})\s+Лабораторная работа\s+(?P<number>\d+)\\?\.")
_HEADING = re.compile(r"^(?P<marks>#{1,6})\s+")
_FENCE = re.compile(r"^\s*(?P<fence>`{3,}|~{3,})(?P<info>[^`]*)$")
_CONTROL_OPERATORS = frozenset({"&", "&&", ";", ";;", "<", "<<", ">", ">>", "|", "||"})
_SMOKE_PATH_FLAGS = frozenset({"--evidence-manifest", "--input", "--output"})
_REPO_PATH_FLAGS = frozenset({"--config", "--config-dir"})
_SHELL_VARIABLE = re.compile(r"\$(?:[A-Za-z_][A-Za-z0-9_]*|\{[A-Za-z_][A-Za-z0-9_]*\})")


@dataclass(frozen=True, slots=True)
class LabShellBlock:
    lab_number: int
    kind: str
    text: str
    start_line: int


@dataclass(frozen=True, slots=True)
class RuntimeCommand:
    lab_number: int
    text: str
    argv: tuple[str, ...]
    line: int


@dataclass(frozen=True, slots=True)
class VerificationIssue:
    lab_number: int
    command: str
    stage: str
    message: str

    def format(self) -> str:
        command = " ".join(self.command.split())
        return f"Лабораторная работа {self.lab_number}: {self.stage}: `{command}`: {self.message}"


@dataclass(frozen=True, slots=True)
class SmokeResult:
    command: RuntimeCommand
    returncode: int
    stdout: str
    stderr: str
    cwd: Path


@dataclass(frozen=True, slots=True)
class VerificationReport:
    blocks: tuple[LabShellBlock, ...]
    runtime_commands: tuple[RuntimeCommand, ...]
    smoke_results: tuple[SmokeResult, ...]
    issues: tuple[VerificationIssue, ...]

    @property
    def ok(self) -> bool:
        return not self.issues

    def format_issues(self) -> str:
        return "\n".join(issue.format() for issue in self.issues)


def extract_lab_shell_blocks(markdown: str) -> tuple[LabShellBlock, ...]:
    """Extract shell-like fenced and indented code blocks from lab sections."""

    lines = markdown.splitlines()
    blocks: list[LabShellBlock] = []
    current_lab: int | None = None
    lab_heading_level: int | None = None
    index = 0

    while index < len(lines):
        line = lines[index]
        lab_match = _LAB_HEADING.match(line)
        if lab_match:
            current_lab = int(lab_match.group("number"))
            lab_heading_level = len(lab_match.group("marks"))
            index += 1
            continue

        heading_match = _HEADING.match(line)
        if (
            current_lab is not None
            and heading_match
            and lab_heading_level is not None
            and len(heading_match.group("marks")) <= lab_heading_level
        ):
            current_lab = None
            lab_heading_level = None
            index += 1
            continue

        fence_match = _FENCE.match(line)
        if fence_match:
            fence = fence_match.group("fence")
            info = fence_match.group("info").strip().lower()
            language = info.split(maxsplit=1)[0] if info else ""
            content, next_index = _read_fenced_block(lines, index, fence)
            if current_lab is not None and language in SHELL_LANGUAGES:
                blocks.append(
                    LabShellBlock(
                        lab_number=current_lab,
                        kind=language,
                        text="\n".join(content),
                        start_line=index + 2,
                    )
                )
            index = next_index
            continue

        if current_lab is not None and _is_indented_code_line(line):
            content, next_index = _read_indented_block(lines, index)
            text = "\n".join(content)
            if _looks_like_shell_block(text):
                blocks.append(
                    LabShellBlock(
                        lab_number=current_lab,
                        kind="indented",
                        text=text,
                        start_line=index + 1,
                    )
                )
            index = next_index
            continue

        index += 1

    return tuple(blocks)


def extract_runtime_commands(
    blocks: Sequence[LabShellBlock],
) -> tuple[RuntimeCommand, ...]:
    """Select direct ``python -m agent_runtime_ref`` commands from shell blocks."""

    commands: list[RuntimeCommand] = []
    for block in blocks:
        for command_text, line_offset in _logical_commands(block.text):
            argv = _runtime_argv(command_text)
            if argv is None:
                continue
            commands.append(
                RuntimeCommand(
                    lab_number=block.lab_number,
                    text=command_text,
                    argv=argv,
                    line=block.start_line + line_offset,
                )
            )
    return tuple(commands)


def verify_text(
    markdown: str,
    *,
    repo_root: str | Path,
    shells: Sequence[str] | None = None,
    run_smoke: bool = True,
) -> VerificationReport:
    """Verify laboratory shell blocks and optionally smoke safe runtime commands."""

    root = Path(repo_root).resolve()
    blocks = extract_lab_shell_blocks(markdown)
    commands = extract_runtime_commands(blocks)
    selected_shells = _available_default_shells() if shells is None else tuple(shells)
    issues = list(_check_shell_syntax(blocks, shells=selected_shells))
    issues.extend(_check_runtime_selection(blocks, commands))
    smoke_results: tuple[SmokeResult, ...] = ()

    if run_smoke and not issues:
        smoke_results, smoke_issues = _smoke_runtime_commands(commands, repo_root=root)
        issues.extend(smoke_issues)

    return VerificationReport(
        blocks=blocks,
        runtime_commands=commands,
        smoke_results=smoke_results,
        issues=tuple(issues),
    )


def verify_manuscript(
    manuscript: str | Path,
    *,
    repo_root: str | Path,
    shells: Sequence[str] | None = None,
    run_smoke: bool = True,
) -> VerificationReport:
    """Read and verify one Markdown manuscript."""

    path = Path(manuscript)
    return verify_text(
        path.read_text(encoding="utf-8"),
        repo_root=repo_root,
        shells=shells,
        run_smoke=run_smoke,
    )


def _read_fenced_block(
    lines: Sequence[str], start: int, opening_fence: str
) -> tuple[list[str], int]:
    marker = opening_fence[0]
    minimum_length = len(opening_fence)
    content: list[str] = []
    index = start + 1
    closing = re.compile(rf"^\s*{re.escape(marker)}{{{minimum_length},}}\s*$")
    while index < len(lines):
        if closing.match(lines[index]):
            return content, index + 1
        content.append(lines[index])
        index += 1
    return content, index


def _is_indented_code_line(line: str) -> bool:
    return line.startswith("    ") or line.startswith("\t")


def _read_indented_block(lines: Sequence[str], start: int) -> tuple[list[str], int]:
    content: list[str] = []
    index = start
    while index < len(lines):
        line = lines[index]
        if line.startswith("    "):
            content.append(line[4:])
            index += 1
            continue
        if line.startswith("\t"):
            content.append(line[1:])
            index += 1
            continue
        if not line.strip() and _next_nonblank_is_indented(lines, index + 1):
            content.append("")
            index += 1
            continue
        break
    return content, index


def _next_nonblank_is_indented(lines: Sequence[str], start: int) -> bool:
    for line in lines[start:]:
        if not line.strip():
            continue
        return _is_indented_code_line(line)
    return False


def _looks_like_shell_block(text: str) -> bool:
    return "agent_runtime_ref" in text and "python" in text


def _logical_commands(text: str) -> tuple[tuple[str, int], ...]:
    commands: list[tuple[str, int]] = []
    parts: list[str] = []
    start_offset = 0

    for offset, raw_line in enumerate(text.splitlines()):
        line = _strip_console_prompt(raw_line).strip()
        if not parts and (not line or line.startswith("#")):
            continue
        if not parts:
            start_offset = offset
        if _has_line_continuation(line):
            parts.append(line[:-1].rstrip())
            continue
        parts.append(line)
        command = " ".join(part for part in parts if part).strip()
        if command:
            commands.append((command, start_offset))
        parts = []

    if parts:
        commands.append((" ".join(parts).strip(), start_offset))
    return tuple(commands)


def _strip_console_prompt(line: str) -> str:
    stripped = line.lstrip()
    if stripped.startswith("$ ") or stripped.startswith("% "):
        prefix_length = len(line) - len(stripped)
        return line[:prefix_length] + stripped[2:]
    return line


def _has_line_continuation(line: str) -> bool:
    backslashes = len(line) - len(line.rstrip("\\"))
    return backslashes % 2 == 1


def _runtime_argv(command: str) -> tuple[str, ...] | None:
    try:
        tokens = shlex.split(command, comments=True, posix=True)
    except ValueError:
        return None
    if not tokens:
        return None

    python_index: int | None = None
    if len(tokens) >= 3 and tokens[:2] == ["uv", "run"]:
        python_index = 2
    elif _is_python_launcher(tokens[0]):
        python_index = 0

    if python_index is None or not _is_python_launcher(tokens[python_index]):
        return None
    if tokens[python_index + 1 : python_index + 3] != ["-m", "agent_runtime_ref"]:
        return None
    argv = tokens[python_index + 3 :]
    return tuple(argv) if argv else ("simulate-run",)


def _is_python_launcher(token: str) -> bool:
    name = Path(token).name
    return name == "python" or name == "python3" or name.startswith("python3.")


def _available_default_shells() -> tuple[str, ...]:
    available = tuple(
        shell for shell in DEFAULT_SHELL_CANDIDATES if shutil.which(shell) is not None
    )
    return available or DEFAULT_SHELL_CANDIDATES[:1]


def _check_shell_syntax(
    blocks: Sequence[LabShellBlock], *, shells: Sequence[str]
) -> tuple[VerificationIssue, ...]:
    issues: list[VerificationIssue] = []
    for shell in shells:
        executable = shutil.which(shell)
        if executable is None:
            for block in blocks:
                issues.append(
                    VerificationIssue(
                        lab_number=block.lab_number,
                        command=_block_snippet(block),
                        stage="shell availability",
                        message=f"required syntax checker is unavailable: {shell}",
                    )
                )
            continue
        for block in blocks:
            try:
                completed = subprocess.run(
                    [executable, "-n"],
                    input=_syntax_text(block.text),
                    text=True,
                    capture_output=True,
                    check=False,
                    timeout=5,
                )
            except subprocess.TimeoutExpired:
                issues.append(
                    VerificationIssue(
                        lab_number=block.lab_number,
                        command=_block_snippet(block),
                        stage="shell syntax",
                        message=f"{shell} -n timed out",
                    )
                )
                continue
            if completed.returncode != 0:
                detail = completed.stderr.strip() or completed.stdout.strip() or "syntax error"
                issues.append(
                    VerificationIssue(
                        lab_number=block.lab_number,
                        command=_block_snippet(block),
                        stage="shell syntax",
                        message=f"{shell} -n: {detail}",
                    )
                )
    return tuple(issues)


def _syntax_text(text: str) -> str:
    return "\n".join(_strip_console_prompt(line) for line in text.splitlines()) + "\n"


def _block_snippet(block: LabShellBlock) -> str:
    commands = _logical_commands(block.text)
    if commands:
        return commands[0][0]
    return f"shell block at line {block.start_line}"


def _check_runtime_selection(
    blocks: Sequence[LabShellBlock], commands: Sequence[RuntimeCommand]
) -> tuple[VerificationIssue, ...]:
    selected = {(command.lab_number, command.line, command.text) for command in commands}
    issues: list[VerificationIssue] = []
    for block in blocks:
        for text, offset in _logical_commands(block.text):
            if not _contains_runtime_module_reference(text):
                continue
            key = (block.lab_number, block.start_line + offset, text)
            if key not in selected:
                issues.append(
                    VerificationIssue(
                        lab_number=block.lab_number,
                        command=text,
                        stage="runtime selection",
                        message="command is not a direct python -m agent_runtime_ref invocation",
                    )
                )
    return tuple(issues)


def _contains_runtime_module_reference(command: str) -> bool:
    try:
        tokens = shlex.split(command, comments=True, posix=True)
    except ValueError:
        return "agent_runtime_ref" in command
    return any(
        tokens[index : index + 2] == ["-m", "agent_runtime_ref"] for index in range(len(tokens) - 1)
    )


def _smoke_runtime_commands(
    commands: Sequence[RuntimeCommand], *, repo_root: Path
) -> tuple[tuple[SmokeResult, ...], tuple[VerificationIssue, ...]]:
    results: list[SmokeResult] = []
    issues: list[VerificationIssue] = []
    with tempfile.TemporaryDirectory(prefix="ru-lab-smoke-") as temp_dir:
        cwd = Path(temp_dir).resolve()
        (cwd / "tmp").mkdir()
        environment = _clean_environment(repo_root=repo_root, cwd=cwd)

        for command in commands:
            if not command.argv:
                issues.append(_smoke_issue(command, "runtime command has no subcommand"))
                continue
            subcommand = command.argv[0]
            if subcommand not in SAFE_RUNTIME_SUBCOMMANDS:
                issues.append(
                    _smoke_issue(
                        command,
                        f"subcommand is not in the safe smoke allowlist: {subcommand}",
                    )
                )
                continue
            if _contains_control_operator(command.text):
                issues.append(
                    _smoke_issue(
                        command,
                        "shell control operators are forbidden in smoke commands",
                    )
                )
                continue

            argv = _prepare_smoke_argv(command, cwd=cwd, repo_root=repo_root)
            try:
                completed = subprocess.run(
                    argv,
                    cwd=cwd,
                    env=environment,
                    text=True,
                    capture_output=True,
                    check=False,
                    timeout=30,
                )
            except subprocess.TimeoutExpired:
                issues.append(_smoke_issue(command, "subprocess timed out after 30 seconds"))
                continue

            result = SmokeResult(
                command=command,
                returncode=completed.returncode,
                stdout=completed.stdout,
                stderr=completed.stderr,
                cwd=cwd,
            )
            results.append(result)
            if completed.returncode != 0:
                detail = _subprocess_detail(completed)
                issues.append(_smoke_issue(command, f"exit code {completed.returncode}: {detail}"))

    return tuple(results), tuple(issues)


def _smoke_issue(command: RuntimeCommand, message: str) -> VerificationIssue:
    return VerificationIssue(
        lab_number=command.lab_number,
        command=command.text,
        stage="clean-room smoke",
        message=message,
    )


def _contains_control_operator(command: str) -> bool:
    lexer = shlex.shlex(command, posix=True, punctuation_chars=";&|<>")
    lexer.whitespace_split = True
    lexer.commenters = "#"
    try:
        return any(token in _CONTROL_OPERATORS for token in lexer)
    except ValueError:
        return True


def _prepare_smoke_argv(command: RuntimeCommand, *, cwd: Path, repo_root: Path) -> list[str]:
    args = list(command.argv)
    prepared: list[str] = []
    index = 0
    while index < len(args):
        token = args[index]
        if token in _SMOKE_PATH_FLAGS and index + 1 < len(args):
            value = _sandbox_path(args[index + 1], cwd=cwd)
            if token == "--output":
                value.parent.mkdir(parents=True, exist_ok=True)
            elif token == "--evidence-manifest":
                _write_smoke_evidence_manifest(value)
            prepared.extend((token, str(value)))
            index += 2
            continue
        if token in _REPO_PATH_FLAGS and index + 1 < len(args):
            raw_value = args[index + 1]
            if token == "--config-dir" and _SHELL_VARIABLE.search(raw_value):
                value = _copy_clean_runtime_configs(
                    command,
                    cwd=cwd,
                    repo_root=repo_root,
                )
            else:
                value = Path(raw_value)
                if not value.is_absolute():
                    value = repo_root / value
            prepared.extend((token, str(value)))
            index += 2
            continue
        prepared.append(token)
        index += 1
    return [sys.executable, "-m", "agent_runtime_ref", *prepared]


def _copy_clean_runtime_configs(
    command: RuntimeCommand,
    *,
    cwd: Path,
    repo_root: Path,
) -> Path:
    source = repo_root / "agent_runtime_ref/configs"
    copies = cwd / "runtime-config-copies"
    copies.mkdir(parents=True, exist_ok=True)
    destination = Path(
        tempfile.mkdtemp(
            prefix=f"lab-{command.lab_number:02d}-line-{command.line}-",
            dir=copies,
        )
    )
    shutil.copytree(source, destination, dirs_exist_ok=True)
    return destination


def _sandbox_path(raw_path: str, *, cwd: Path) -> Path:
    path = Path(raw_path)
    safe_parts = [part for part in path.parts if part not in {"", ".", "..", path.anchor}]
    if not safe_parts:
        safe_parts = ["artifact"]
    return cwd.joinpath(*safe_parts)


def _write_smoke_evidence_manifest(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    artifact = path.parent / "smoke-evaluation.json"
    artifact.write_text('{"passed": true}\n', encoding="utf-8")
    payload = {
        "version": 1,
        "issuer": "ru-lab-command-verifier",
        "subject": "clean-room-smoke",
        "measured_at": "2026-01-01T00:00:00Z",
        "artifacts": [
            {
                "id": "smoke-evaluation",
                "path": artifact.name,
                "sha256": hashlib.sha256(artifact.read_bytes()).hexdigest(),
            }
        ],
        "signals": {
            "duplicate_ticket_eval_passed": {
                "value": True,
                "artifact_refs": ["smoke-evaluation"],
            }
        },
    }
    path.write_text(json.dumps(payload, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def _clean_environment(*, repo_root: Path, cwd: Path) -> dict[str, str]:
    environment = {
        "PATH": os.environ.get("PATH", ""),
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONNOUSERSITE": "1",
        "PYTHONPATH": str(repo_root),
        "TMPDIR": str(cwd / "tmp"),
    }
    for key in ("LANG", "LC_ALL"):
        if value := os.environ.get(key):
            environment[key] = value
    return environment


def _subprocess_detail(completed: subprocess.CompletedProcess[str]) -> str:
    detail = completed.stderr.strip() or completed.stdout.strip() or "no output"
    compact = " ".join(detail.split())
    return compact[-600:]


def _default_repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _default_manuscript(repo_root: Path) -> Path:
    publisher_dir = repo_root / "docs/publisher"
    candidates = sorted(publisher_dir.glob("ru-manuscript-editorial-*.md"))
    if candidates:
        return candidates[-1]
    return publisher_dir / "ru-manuscript-full.md"


def build_parser() -> argparse.ArgumentParser:
    repo_root = _default_repo_root()
    parser = argparse.ArgumentParser(
        description="Verify literal shell commands in Russian manuscript laboratories"
    )
    parser.add_argument(
        "manuscript",
        nargs="?",
        type=Path,
        default=_default_manuscript(repo_root),
    )
    parser.add_argument("--repo-root", type=Path, default=repo_root)
    parser.add_argument(
        "--shell",
        action="append",
        dest="shells",
        default=None,
        help=(
            "Syntax checker to run; repeat for several shells "
            "(default: installed checkers among sh and zsh)"
        ),
    )
    parser.add_argument(
        "--syntax-only",
        action="store_true",
        help="Skip clean-room subprocess smoke tests",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    shells = tuple(args.shells) if args.shells else None
    try:
        report = verify_manuscript(
            args.manuscript,
            repo_root=args.repo_root,
            shells=shells,
            run_smoke=not args.syntax_only,
        )
    except (OSError, UnicodeError) as error:
        print(f"Cannot read manuscript {args.manuscript}: {error}", file=sys.stderr)
        return 2

    if not report.ok:
        print(report.format_issues(), file=sys.stderr)
        return 1
    print(
        "OK: "
        f"{len(report.blocks)} shell blocks, "
        f"{len(report.runtime_commands)} runtime commands, "
        f"{len(report.smoke_results)} clean-room smoke runs"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
