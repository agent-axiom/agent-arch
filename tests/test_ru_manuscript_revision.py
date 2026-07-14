from __future__ import annotations

import json
import re
import struct
import xml.etree.ElementTree as ET
from pathlib import Path

from docs.publisher.tools.revise_ru_manuscript import revise

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/publisher/ru-manuscript-google-doc-final-2026-07-11.md"
EXPECTED = ROOT / "docs/publisher/ru-manuscript-editorial-2026-07-13.md"
MANIFEST = ROOT / "docs/publisher/ru-inline-diagrams-2026-07-13.json"
VISUALS = ROOT / "docs/publisher/visuals"


def test_revision_is_reproducible(tmp_path: Path) -> None:
    output = tmp_path / "manuscript.md"
    manifest = tmp_path / "diagrams.json"

    revise(SOURCE, output, manifest)

    assert output.read_bytes() == EXPECTED.read_bytes()
    data = json.loads(manifest.read_text(encoding="utf-8"))
    assert len(data["diagrams"]) == 29
    assert [item["number"] for item in data["diagrams"]] == list(range(1, 30))


def test_revision_has_clean_reader_facing_structure() -> None:
    text = EXPECTED.read_text(encoding="utf-8")

    assert "\nflowchart " not in text
    assert "Практическое дополнение 2026" not in text
    assert "Что изменилось после предыдущей проверки" not in text
    assert "Статус: полнообъемная сборка" not in text
    assert "Источник правды:" not in text
    assert "подсказкими" not in text
    assert "над программного каркасами" not in text
    assert "Команды сессий и оценок явно показывают поля сводки" not in text
    assert "inspect-lifecycle теперь тоже показывает" not in text
    assert "Второй вариант специально добавлен как сценарий с явным отказом" not in text
    assert "свой локальная среда исполнения" not in text
    assert "happy path" not in text
    assert "Golden path" not in text
    assert "золотые пути" not in text
    assert text.count("companion-справочник") >= 19
    assert "developers.openai.com/api/docs/guides/agents-sdk" not in text
    assert "openai.github.io/openai-agents-python" in text

    headings = []
    for line in text.splitlines():
        match = re.match(r"^(#{1,6})\s+(.+)$", line)
        if match:
            headings.append((len(match.group(1)), match.group(2)))

    assert len(headings) == 723
    assert not any(not title.strip(" *_") for _, title in headings)
    assert not any(
        current[0] > previous[0] + 1 for previous, current in zip(headings, headings[1:])
    )
    assert len(re.findall(r"^## Глава \d+", text, re.MULTILINE)) == 28
    assert len(re.findall(r"Рисунок \d+\\?\.", text)) == 25
    assert len(re.findall(r"Лабораторная работа \d+\\?\.", text)) == 7


def test_inline_diagrams_are_publisher_ready() -> None:
    diagrams = json.loads(MANIFEST.read_text(encoding="utf-8"))["diagrams"]

    for diagram in diagrams:
        stem = Path(diagram["filename"]).stem
        svg_path = VISUALS / f"{stem}.svg"
        png_path = VISUALS / diagram["filename"]

        root = ET.fromstring(svg_path.read_text(encoding="utf-8"))
        namespace = {
            "svg": "http://www.w3.org/2000/svg",
            "xhtml": "http://www.w3.org/1999/xhtml",
        }
        title = root.find("svg:title", namespace)
        assert title is not None
        assert title.text == diagram["caption"]
        assert any((node.text or "").strip() for node in root.findall(".//xhtml:p", namespace))

        png = png_path.read_bytes()
        assert png[:8] == b"\x89PNG\r\n\x1a\n"
        width, height = struct.unpack(">II", png[16:24])
        assert (width, height) == (1600, 900)
        assert png[25] == 2  # Truecolor RGB without an alpha channel.
