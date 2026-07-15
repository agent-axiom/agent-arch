from __future__ import annotations

import json
import re
import struct
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

from docs.publisher.tools.revise_ru_manuscript import replace_mermaid_blocks, revise

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
    assert text.count("companion-справочник") >= 12
    assert "developers.openai.com/api/docs/guides/agents-sdk" not in text
    assert "openai.github.io/openai-agents-python" in text

    headings = []
    for line in text.splitlines():
        match = re.match(r"^(#{1,6})\s+(.+)$", line)
        if match:
            headings.append((len(match.group(1)), match.group(2)))

    assert len(headings) == 741
    assert not any(not title.strip(" *_") for _, title in headings)
    assert not any(
        current[0] > previous[0] + 1 for previous, current in zip(headings, headings[1:])
    )
    assert len(re.findall(r"^## Глава \d+", text, re.MULTILINE)) == 28
    assert len(re.findall(r"^### Итог главы$", text, re.MULTILINE)) == 28
    assert text.count("**Задача части.**") == 7
    assert len(re.findall(r"Рисунок \d+\\?\.", text)) == 25
    assert len(re.findall(r"^На рисунке \d+ представлена схема", text, re.MULTILINE)) == 25
    assert len(re.findall(r"Лабораторная работа \d+\\?\.", text)) == 7
    for pseudo_table_header in (
        "| Ситуация | Что чаще лучше |",
        "| Угроза | Где ловить в первую очередь |",
        "| Поле каталога | Что фиксировать |",
        "| Вопрос | Скорее MCP |",
        "| Event type | Когда появляется |",
    ):
        assert pseudo_table_header not in text
    assert "**Внедрение инструкций** — где ловить в первую очередь:" in text
    assert "`run_start` — когда:" in text

    for residue in (
        "**Практическая проверка**",
        "**Связь со следующей главой.**",
        "**Сопутствующие материалы**",
        "Этот раздел собирает в одном месте минимальный контрактный слой для "
        "артефактов жизненного цикла",
        "### Что должно существовать всегда",
        "Заметка о сквозных сценариях",
        "Канонические сценарии",
    ):
        assert residue not in text


def test_revision_has_reproducible_practical_path() -> None:
    text = EXPECTED.read_text(encoding="utf-8")

    assert "uv sync --group dev" in text
    assert "inspect-memory --tenant-id tenant-beta --memory-class profile" in text
    assert "`count=0`, пустые `memory_ids` и `records`" in text
    assert "export-events --trace-id trace-lab-05-01 --session-id session-lab-05" in text
    assert "check-rollout --signal duplicate_ticket_eval_passed=false" in text
    assert "не на вымышленном совпадении" in text
    assert "### Расчетный пример: SLO известного внешнего эффекта" in text
    assert "расход бюджета ошибок = 130 / 100 = 130 %" in text
    assert len(re.findall(r"^### Этап [1-5]\.", text, re.MULTILINE)) == 5
    assert "### Рубрика проекта" in text
    assert "Финальное решение для текущего эталонного пакета остается `hold`" in text


def test_revision_repairs_key_pseudocode_and_language_residue() -> None:
    text = EXPECTED.read_text(encoding="utf-8")

    assert "    def run_manager(" in text
    assert "        for step in plan:" in text
    assert "    class PolicyDecision:" in text
    assert "        requires_approval: bool = False" in text
    assert "    class RunRequest:" in text
    assert "        policy_check(request)" in text

    for residue in (
        "среда исполнения не должен",
        "Зачем нужна этот раздел",
        "к проверочный списоку",
        "хорошо настроенная поэтапный выпуск",
        "если вы только подходишь",
        "решайтете",
        "Практический паттерн Microsoft",
        "Практический паттерн AWS",
        "Чеклист Google Cloud",
        "предел экспозиции",
    ):
        assert residue not in text


def test_revision_has_no_unintended_placeholders_or_duplicate_prose() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    author_block, reader_facing_text = text.split("## Как использовать примеры безопасно", 1)
    reader_facing_text = reader_facing_text.split("\n[image1]:", 1)[0]

    assert "\\[заполнить" in author_block
    assert "\\[согласовать формулировку с издательством\\]" in author_block
    for residue in ("TODO", "FIXME", "TBD", "\\[заполнить", "\\[имя / публичное имя\\]"):
        assert residue not in reader_facing_text

    prose_blocks = []
    for raw_block in re.split(r"\n\s*\n", text):
        block = " ".join(line.strip() for line in raw_block.splitlines()).strip()
        if len(block) < 180 or block.startswith(
            ("```", "![", "[image", "* [", "##", "# ")
        ):
            continue
        if "data:image/" in block:
            continue
        prose_blocks.append(re.sub(r"\s+", " ", block))

    duplicates = [block for block, count in Counter(prose_blocks).items() if count > 1]
    assert duplicates == []


def test_revision_keeps_new_chapter_numbering_and_control_examples_consistent() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    text = EXPECTED.read_text(encoding="utf-8")

    assert "* Глава 20\\. Агентное несоответствие целей и внутренний риск." in source
    assert "главы 1, 3, 4, 10, 13, 16 и 23\\." not in source
    assert "create\\_support\\_ticket" not in source

    for stale_reference in (
        "Если запуск выявил серьезную проблему, в игру вступает глава 22\\.",
        "глава 22 по-прежнему отвечает за реагирование в контуре заверения",
        "глава 23 по-прежнему отвечает за происхождение",
        "Главы 24 и 24",
        "из глав 25 и 26",
        "глав 19-24",
        "из глав 25 и 26",
        "create_support_ticket",
        "create\\_support\\_ticket",
    ):
        assert stale_reference not in text

    assert "в игру вступает глава 21\\." in text
    assert "Глава 20\\. Агентное несоответствие целей и внутренний риск" in text
    assert "Глава 24\\. Наблюдаемость для ИИ-систем и телеметрия обнаружения" in text
    assert "Глава 25\\. Инвентаризация агентов, реестр и контроль разрастания" in text
    assert "из глав 26 и 27" in text
    assert "главы 19–25" in text

    assert "Покрытие обязательным подтверждением и трассировкой" in text
    assert "все высокорисковые внешние эффекты" in text
    assert "Цель для обеих долей — 100%" in text
    assert "занятые минуты проверяющих" in text

    causal_record = text[text.index("causal\\_case:") : text.index("#### Три сквозных сценария")]
    assert "edges:" in causal_record
    assert causal_record.count("evidence\\_ref") == 3

    interceptor_example = text[
        text.index("request, request\\_meta") : text.index("Каждая ветка обязана вернуть")
    ]
    assert "except RequestInterceptorFailure" in interceptor_example
    assert "except PolicyEvaluationFailure" in interceptor_example
    assert "except GatewayTimeout" in interceptor_example
    assert "except ResponseInterceptorFailure" in interceptor_example
    assert 'status="side_effect_unknown"' in interceptor_example


def test_block_beta_diagram_is_replaced_with_a_publisher_image() -> None:
    blocks = [
        f"""Readable control path {number}

block-beta
columns 2
A["Policy"]
B["Gateway"]
A --> B"""
        for number in range(1, 30)
    ]
    source = "\n\nFollowing paragraph.\n\n".join(blocks)

    output, manifest = replace_mermaid_blocks(source, "visuals")

    assert "block-beta" not in output
    assert "![Readable control path 1](visuals/ru-inline-diagram-01.png)" in output
    assert manifest[0]["mermaid"].startswith("block-beta\ncolumns 2")


def test_inline_diagrams_are_publisher_ready() -> None:
    diagrams = json.loads(MANIFEST.read_text(encoding="utf-8"))["diagrams"]
    multirow_diagrams = {1, 8, 13, 14, 20, 23, 28}

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
        html_labels = root.findall(".//xhtml:p", namespace)
        svg_labels = root.findall(".//svg:text", namespace)
        assert any(
            "".join(node.itertext()).strip() for node in [*html_labels, *svg_labels]
        )

        png = png_path.read_bytes()
        assert png[:8] == b"\x89PNG\r\n\x1a\n"
        width, height = struct.unpack(">II", png[16:24])
        assert (width, height) == (1600, 900)
        assert png[25] == 2  # Truecolor RGB without an alpha channel.
        if diagram["number"] in multirow_diagrams:
            assert diagram["mermaid"].startswith("block-beta\n")
