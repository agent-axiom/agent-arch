#!/usr/bin/env python3
"""Apply conservative Russian terminology replacements to manuscript Markdown."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REPLACEMENTS = [
    ("companion-материалов", "сопроводительных материалов"),
    (
        "Companion: [публичный URL / версия v1.0-book / errata route - заполнить].",
        "Сопроводительные материалы: [публичный URL / версия v1.0-book / маршрут исправлений - заполнить].",
    ),
    ("в online companion", "в онлайн-сопровождении"),
    ("online companion", "онлайн-сопровождение"),
    ("companion route", "маршрут сопроводительных материалов"),
    ("companion artifact", "сопроводительный артефакт"),
    ("Что остается в companion", "Что остается в сопроводительных материалах"),
    ("Что уходит в companion", "Что уходит в сопроводительные материалы"),
    ("в companion", "в сопроводительные материалы"),
    ("обычным workflow", "обычным рабочим процессом"),
    ("Обычный workflow", "Обычный рабочий процесс"),
    ("жесткий workflow", "жесткий рабочий процесс"),
    ("Хороший workflow", "Хороший рабочий процесс"),
    ("workflow почти всегда", "рабочий процесс почти всегда"),
    ("workflow становится", "рабочий процесс становится"),
    ("rollout-план", "план поэтапного выпуска"),
    ("rollout-плана", "плана поэтапного выпуска"),
    ("остановить rollout", "остановить поэтапный выпуск"),
    ("rollout, assurance loop, incident response", "поэтапный выпуск, контур заверения, реагирование на инциденты"),
    ("до ADLC, rollout, incident response", "до ADLC, поэтапного выпуска, реагирования на инциденты"),
    ("incident response", "реагирование на инциденты"),
    ("production checklist", "производственный чеклист"),
    ("incident checklist", "инцидентный чеклист"),
    ("readiness checklist", "чеклист готовности"),
    ("policy gateway", "шлюз политик"),
    ("tool gateway", "шлюз инструментов"),
    ("агентный runtime", "агентную среду исполнения"),
    ("runtime решает", "среда исполнения решает"),
    ("вне prompt", "вне промпта"),
    ("один prompt", "один промпт"),
    ("tool contracts", "контракты инструментов"),
    ("обычным tool call", "обычным вызовом инструмента"),
    ("внутренние tool calls", "внутренние вызовы инструментов"),
    ("после неудачного tool call", "после неудачного вызова инструмента"),
    ("до tool call", "до вызова инструмента"),
    (
        "для selection, policy decision, approval, tool call и normalized result",
        "для selection, policy decision, approval, вызова инструмента и normalized result",
    ),
    ("через approval, tool call, trace", "через approval, вызов инструмента, trace"),
    ("timeout или human review", "timeout или человеческую проверку"),
    ("без human review", "без человеческой проверки"),
    ("обычным вызов инструмента", "обычным вызовом инструмента"),
    ("внутренние вызов инструментаs", "внутренние вызовы инструментов"),
    ("вызов инструментаs", "вызовы инструментов"),
    ("после неудачного вызов инструмента", "после неудачного вызова инструмента"),
    ("до вызов инструмента", "до вызова инструмента"),
    (
        "для selection, policy decision, approval, вызов инструмента и normalized result",
        "для selection, policy decision, approval, вызова инструмента и normalized result",
    ),
    ("timeout или человеческой проверки", "timeout или человеческую проверку"),
    ("AI tooling disclosure", "раскрытие использования ИИ-инструментов"),
    ("developer tooling", "инструменты для разработчиков"),
]


def apply_replacements(path: Path) -> dict[str, int]:
    text = path.read_text(encoding="utf-8")
    counts: dict[str, int] = {}
    for old, new in REPLACEMENTS:
        count = text.count(old)
        if count:
            text = text.replace(old, new)
        counts[old] = count
    path.write_text(text, encoding="utf-8")
    return counts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()

    result = {str(path): apply_replacements(path) for path in args.paths}
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
