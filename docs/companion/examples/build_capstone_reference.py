from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Sequence

import yaml


def _run_runtime(repo_root: Path, args: Sequence[str]) -> dict[str, object]:
    completed = subprocess.run(
        [sys.executable, "-m", "agent_runtime_ref", *args],
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=True,
    )
    payload = json.loads(completed.stdout)
    if not isinstance(payload, dict):
        raise TypeError("agent_runtime_ref must return a JSON object")
    return payload


def _write_json(path: Path, payload: object) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git_revision(repo_root: Path) -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=True,
    )
    return completed.stdout.strip()


def build_capstone(
    output_dir: Path,
    *,
    repo_root: Path,
    measured_at: str,
) -> dict[str, object]:
    output_dir = output_dir.resolve()
    repo_root = repo_root.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    agent = _run_runtime(repo_root, ("inspect-agent",))
    approval = _run_runtime(
        repo_root,
        (
            "inspect-approvals",
            "--approval-store",
            str(output_dir / "01-approval-state.json"),
            "--trace-id",
            "trace-capstone-approval",
            "--session-id",
            "session-capstone",
            "--user-input",
            "Please create a ticket for this onboarding issue.",
        ),
    )
    lifecycle = _run_runtime(repo_root, ("inspect-lifecycle",))
    _write_json(output_dir / "01-agent.json", agent)
    _write_json(output_dir / "01-approval.json", approval)
    _write_json(output_dir / "01-lifecycle.json", lifecycle)

    baseline = f"""# Исходное состояние итогового проекта

- Версия репозитория: `{_git_revision(repo_root)}`.
- Агент: `{agent.get("agent_id", "support-triage-ref")}`.
- Записывающая возможность: `create_ticket`.
- Запрос подтверждения: `trace-capstone-approval`.

Эталон показывает контракт и закрытые отказы, но не доказывает промышленную
аутентификацию проверяющего, атомарное потребление подтверждения или сверку с
реальной системой заявок.
"""
    (output_dir / "01-baseline.md").write_text(baseline, encoding="utf-8")

    normal_trace = output_dir / "02-normal-trace.jsonl"
    timeout_trace = output_dir / "02-timeout-trace.jsonl"
    _run_runtime(
        repo_root,
        (
            "export-events",
            "--trace-id",
            "trace-capstone-normal",
            "--session-id",
            "session-capstone",
            "--output",
            str(normal_trace),
        ),
    )
    _run_runtime(
        repo_root,
        (
            "export-events",
            "--trace-id",
            "trace-capstone-timeout",
            "--session-id",
            "session-capstone",
            "--simulate-failure",
            "tool_timeout",
            "--output",
            str(timeout_trace),
        ),
    )
    normal_summary = _run_runtime(repo_root, ("inspect-trace", "--input", str(normal_trace)))
    timeout_summary = _run_runtime(
        repo_root,
        ("inspect-trace", "--input", str(timeout_trace)),
    )
    _write_json(output_dir / "02-normal-trace-summary.json", normal_summary)
    _write_json(output_dir / "02-timeout-trace-summary.json", timeout_summary)
    comparison = """# Сравнение трасс

| Путь | Итог | Внешний эффект | Допустимый следующий шаг |
| :--- | :--- | :------------- | :----------------------- |
| Обычный | Ожидание подтверждения | Не выполнен | Получить решение человека |
| Тайм-аут | Отказ `tool_timeout` | Неизвестен | Сверить внешнее состояние |

Тайм-аут транспорта не является доказательством отсутствия заявки. Повтор
запрещен до результата сверки по устойчивому бизнес-ключу.
"""
    (output_dir / "02-trace-comparison.md").write_text(comparison, encoding="utf-8")

    reconciliation = {
        "version": 1,
        "business_key": "support-request:onboarding-issue:user-42",
        "query": "lookup_ticket_by_business_key",
        "possible_results": ["not_found", "found_once", "found_multiple", "unknown"],
        "owner": "support-platform-on-call",
        "automatic_retry_allowed": False,
        "required_before_retry": "verification_result=not_found",
    }
    (output_dir / "03-reconciliation.yaml").write_text(
        yaml.safe_dump(reconciliation, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )

    eval_path = output_dir / "04-eval.json"
    _run_runtime(
        repo_root,
        (
            "export-eval-dataset",
            "--scenario",
            "failed_run_timeout",
            "--session-prefix",
            "session-capstone",
            "--output",
            str(eval_path),
        ),
    )
    rollout = _run_runtime(
        repo_root,
        ("check-rollout", "--signal", "duplicate_ticket_eval_passed=false"),
    )
    _write_json(output_dir / "04-rollout-hold.json", rollout)

    plan = """# Путь к ограниченной волне

Переход к `limited_wave` возможен только после доверенной аттестации оценки
дублей, промышленной сверки внешнего эффекта, долговечного подтверждения,
проверенной изоляции арендаторов и испытанного отката. Для каждого свойства
нужны владелец, источник сигнала, отрицательная проверка и срок пересмотра.

До выполнения этих условий решение остается `hold`.
"""
    (output_dir / "05-limited-wave-plan.md").write_text(plan, encoding="utf-8")

    release_decision: dict[str, object] = {
        "version": 1,
        "decision": "hold",
        "next_eligible_decision": "limited_wave",
        "blocking_findings": [
            "unknown_external_effect_not_reconciled",
            "trusted_duplicate_ticket_attestation_missing",
        ],
        "owner": "support-platform-release-owner",
        "evidence_refs": [
            "02-timeout-trace.jsonl",
            "03-reconciliation.yaml",
            "04-rollout-hold.json",
        ],
    }
    _write_json(output_dir / "release-decision.json", release_decision)

    readme = """# Эталон итогового проекта

Из корня репозитория выполните:

```console
uv run python docs/companion/examples/build_capstone_reference.py \\
  --output-dir artifacts/capstone
```

Пакет намеренно завершает решение `hold`: учебный стенд подтверждает форму
доказательств, но не заменяет промышленную аттестацию и внешнюю сверку.
"""
    (output_dir / "README.md").write_text(readme, encoding="utf-8")

    artifact_files = sorted(
        path
        for path in output_dir.iterdir()
        if path.is_file() and path.name != "evidence-manifest.yaml"
    )
    artifacts = [
        {
            "id": path.stem.replace("_", "-").replace(".", "-"),
            "path": path.name,
            "sha256": _sha256(path),
        }
        for path in artifact_files
    ]
    manifest = {
        "version": 1,
        "issuer": "agent-arch-capstone-reference",
        "subject": "support-triage-ref",
        "measured_at": measured_at,
        "artifacts": artifacts,
        "signals": {
            "capstone_package_built": {
                "value": True,
                "artifact_refs": [item["id"] for item in artifacts],
            }
        },
    }
    (output_dir / "evidence-manifest.yaml").write_text(
        yaml.safe_dump(manifest, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    return release_decision


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build the Russian book capstone package.")
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/capstone"))
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[3],
    )
    parser.add_argument("--measured-at", default="2026-08-03T00:00:00Z")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = build_capstone(
        args.output_dir,
        repo_root=args.repo_root,
        measured_at=args.measured_at,
    )
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
