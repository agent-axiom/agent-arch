from __future__ import annotations

import json
import re
import struct
import textwrap
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

import yaml

from docs.publisher.tools.revise_ru_manuscript import replace_mermaid_blocks, revise

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/publisher/ru-manuscript-google-doc-final-2026-07-11.md"
EXPECTED = ROOT / "docs/publisher/ru-manuscript-editorial-2026-07-13.md"
MANIFEST = ROOT / "docs/publisher/ru-inline-diagrams-2026-07-13.json"
NUMBERED_MANIFEST = ROOT / "docs/publisher/ru-numbered-diagrams-2026-07-15.json"
VISUALS = ROOT / "docs/publisher/visuals"

NUMBERED_FIGURE_PATHS = [
    "visuals/ru-figure-01-book-map.png",
    "visuals/ru-figure-13-autonomy-ladder.png",
    "visuals/ru-figure-03-reference-architecture.png",
    "visuals/ru-figure-02-trust-boundaries.png",
    "visuals/ru-figure-19-localhost-control-plane.png",
    "visuals/ru-figure-04-capability-contract-path.png",
    "visuals/ru-figure-16-capability-endpoint-contract.png",
    "visuals/ru-figure-06-approval-gateway.png",
    "visuals/ru-figure-25-memory-write-lifecycle.png",
    "visuals/ru-figure-05-memory-retrieval.png",
    "visuals/ru-figure-07-sandbox-mcp.png",
    "visuals/ru-figure-21-mcp-gateway.png",
    "visuals/ru-figure-08-idempotency-recovery.png",
    "visuals/ru-figure-20-eval-integrity.png",
    "visuals/ru-figure-15-eval-audit-record-flow.png",
    "visuals/ru-figure-09-evidence-chain.png",
    "visuals/ru-figure-10-adlc-lifecycle.png",
    "visuals/ru-figure-11-assurance-incident-registry.png",
    "visuals/ru-figure-23-incident-response-state.png",
    "visuals/ru-figure-18-runtime-stack.png",
    "visuals/ru-figure-22-durable-workflow-fiber.png",
    "visuals/ru-figure-14-brain-hands-session.png",
    "visuals/ru-figure-17-rollout-simulation-fidelity.png",
    "visuals/ru-figure-12-launch-readiness.png",
    "visuals/ru-figure-24-capstone-evidence-package.png",
]


def test_revision_is_reproducible(tmp_path: Path) -> None:
    output = tmp_path / "manuscript.md"
    manifest = tmp_path / "diagrams.json"

    revise(SOURCE, output, manifest)

    assert output.read_bytes() == EXPECTED.read_bytes()
    data = json.loads(manifest.read_text(encoding="utf-8"))
    assert len(data["diagrams"]) == 29
    assert [item["number"] for item in data["diagrams"]] == list(range(1, 30))


def test_reference_package_quickstart_matches_runtime_contract() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    appendix = text[
        text.index("### Как запустить") : text.index(
            "Явный запуск среды исполнения через подкоманду:"
        )
    ]

    assert "git checkout ru-manuscript-editorial-2026-07" in appendix
    assert '"status": "waiting_for_approval"' in appendix
    assert '"events": 10' in appendix
    assert '"memory_records": 3' in appendix
    assert '"task_success": null' in appendix
    assert '"side_effect_status": "not_executed"' in appendix

    for stale_value in (
        "885bc9639d5c5c4f43adc62ca3c80be124787ccf",
        '"status": "success"',
        '"events": 14',
        '"memory_records": 4',
    ):
        assert stale_value not in appendix


def test_revision_has_clean_reader_facing_structure() -> None:
    text = EXPECTED.read_text(encoding="utf-8")

    assert not any(line.endswith((" ", "\t")) for line in text.splitlines())
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
    assert "companion-справочник" not in text
    assert len(
        re.findall(r"сопроводительн(?:ый справочник|ом справочнике)", text)
    ) >= 12
    assert "developers.openai.com/api/docs/guides/agents-sdk" not in text
    assert "openai.github.io/openai-agents-python" in text

    headings = []
    for line in text.splitlines():
        match = re.match(r"^(#{1,6})\s+(.+)$", line)
        if match:
            headings.append((len(match.group(1)), match.group(2)))

    assert len(headings) < 700
    assert not any(not title.strip(" *_") for _, title in headings)
    assert not any(
        current[0] > previous[0] + 1 for previous, current in zip(headings, headings[1:])
    )
    assert len(re.findall(r"^## Глава \d+", text, re.MULTILINE)) == 28
    assert len(re.findall(r"^### Ключевые выводы$", text, re.MULTILINE)) == 28
    assert text.count("**Задача части.**") == 8
    assert len(re.findall(r"Рисунок \d+\\?\.", text)) == 25
    assert len(re.findall(r"^На рисунке \d+ представлена схема", text, re.MULTILINE)) == 25
    assert len(re.findall(r"Лабораторная работа \d+\\?\.", text)) == 8
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


def test_reader_facing_text_has_no_editorial_navigation_residue() -> None:
    text = EXPECTED.read_text(encoding="utf-8")

    for residue in (
        "Печатная глава",
        "Роль главы в части VI",
        "откройте отдельную страницу",
        "Нужны схемы",
        "Сквозные сценарии процедур",
        "Канонические маршруты сценариев",
        "Что изменилось после предыдущей проверки",
    ):
        assert residue not in text


def test_python_listings_are_fenced_and_syntax_checked() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    outside_fence: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence and re.match(r"^(?:@dataclass|@dataclass\(|class |def |async def )", line):
            outside_fence.append(line)

    assert outside_fence == []

    python_blocks = re.findall(r"```python\n(.*?)\n```", text, re.DOTALL)
    assert len(python_blocks) >= 20
    for index, block in enumerate(python_blocks, start=1):
        compile(textwrap.dedent(block), f"manuscript-listing-{index}.py", "exec")


def test_yaml_and_console_blocks_are_machine_readable() -> None:
    text = EXPECTED.read_text(encoding="utf-8")

    yaml_blocks = re.findall(r"```yaml\n(.*?)\n```", text, re.DOTALL)
    assert len(yaml_blocks) >= 12
    for index, block in enumerate(yaml_blocks, start=1):
        parsed = yaml.safe_load(block)
        assert parsed is not None, f"YAML listing {index} is empty"

    console_blocks = re.findall(r"```console\n(.*?)\n```", text, re.DOTALL)
    assert len(console_blocks) >= 15
    assert all("\\--" not in block and "\\_" not in block for block in console_blocks)
    assert len(re.findall(r"^\*\*Листинг \d+\.", text, re.MULTILINE)) >= 30
    assert "•" not in text

    outside_fence: list[str] = []
    in_fence = False
    forbidden_starts = (
        "instructions:",
        "routines:",
        "bundle:",
        "kind: `approval_",
        "kind: `memory_record`",
        "kind: `retrieval_",
        "tools:",
        "`scenario_id`:",
        "kind: `change_review_record`",
        "kind: `rollout_gate_record`",
        "`causal_case`:",
        "`control_plane_readiness`:",
        "`agentic_internal_risk`:",
        "postmortem:",
        "kind: `incident_",
    )
    for line in text.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence and line.strip().startswith(forbidden_starts):
            outside_fence.append(line)
    assert outside_fence == []


def test_chapters_have_a_consistent_learning_contract_and_sources() -> None:
    text = EXPECTED.read_text(encoding="utf-8")

    assert text.count("**После главы вы сможете:**") == 28
    assert text.count("**Артефакт главы:**") == 28
    assert len(re.findall(r"^### Ключевые выводы$", text, re.MULTILINE)) == 28
    assert len(re.findall(r"^### Источники главы$", text, re.MULTILINE)) == 28
    assert "От наблюдаемого отклонения к внутреннему риску" in text


def test_labs_have_prerequisites_timing_and_negative_paths() -> None:
    text = EXPECTED.read_text(encoding="utf-8")

    assert text.count("**Предварительные условия.**") == 8
    assert text.count("**Ориентировочное время.**") == 8
    assert text.count("**Отрицательная проверка.**") == 8
    assert text.count("**Если результат отличается.**") == 8
    assert text.count("**Дополнительное задание.**") == 8


def test_terminology_and_glossary_are_editorially_consistent() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    prose = re.sub(r"```.*?```", "", text, flags=re.DOTALL)

    for residue in (
        "read tools",
        "write tools",
        "action tools",
        "orchestration tools",
        "process isolation",
        "short-term memory",
        "long-term memory",
        "profile memory",
        "static context",
        "turn context",
        "cached context",
        "query patterns",
        "risk tier",
        "credential scope",
        "tenant boundary",
        "blast radius",
        "tool call",
        "по проектированиеу",
        "approved inventory",
        "approved artifacts",
        "deprecated patterns",
        "active / inactive",
        "approval path здесь избыточен",
        "из\\-за",
        "Поэтому надежное правило по умолчанию здесь простое: Поэтому",
    ):
        assert residue not in prose

    assert not re.search(r"(?:part|lab)-`[ivx0-9]+/[^`]+``", text)

    for term in (
        "### Происхождение данных",
        "### Контракт возможности",
        "### Ключ идемпотентности",
        "### Неизвестный внешний эффект",
        "### Выпускной шлюз",
        "### Агентное несоответствие целей",
    ):
        assert term in text

    provenance = text.split("### Происхождение данных", 1)[1].split("\n### ", 1)[0]
    assert "Читать дальше:" in provenance
    assert re.search(r"глав(?:а|ы) \d", provenance, re.IGNORECASE)


def test_source_access_date_is_consistent() -> None:
    text = EXPECTED.read_text(encoding="utf-8")

    assert "дата доступа зафиксированы 14 июля 2026 года" not in text
    assert "дата доступа зафиксированы 15 июля 2026 года" in text


def test_revision_has_reproducible_practical_path() -> None:
    text = EXPECTED.read_text(encoding="utf-8")

    assert "uv sync --frozen --group dev" in text
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


def test_laboratory_commands_are_literal_and_build_one_evidence_manifest() -> None:
    text = EXPECTED.read_text(encoding="utf-8")

    assert "mkdir -p `artifacts/lab-05`" not in text
    assert "--output `artifacts/lab-05/" not in text
    assert "--input `artifacts/lab-05/" not in text

    for number in range(1, 9):
        lab_start = text.index(f"### Лабораторная работа {number}\\.")
        next_lab = text.find("### Лабораторная работа ", lab_start + 1)
        lab = text[lab_start : next_lab if next_lab != -1 else len(text)]
        assert f"artifacts/lab-{number:02d}" in lab
        assert "artifacts/evidence-manifest.yaml" in lab

    lab_eight = text.split("### Лабораторная работа 8\\.", 1)[1]
    lab_eight = lab_eight.split("## Итоговый проект", 1)[0]
    assert "--evidence-manifest artifacts/evidence-manifest.yaml" in lab_eight
    assert "recommended_action" in lab_eight


def test_machine_contract_examples_and_statuses_are_canonical() -> None:
    text = EXPECTED.read_text(encoding="utf-8")

    assert "`permission_failure`" not in text
    assert "sideeffectunknown" not in text
    assert "`permission_denied`" in text
    assert "`side_effect_unknown`" in text

    json_blocks = re.findall(r"```json\n(.*?)\n```", text, re.DOTALL)
    assert len(json_blocks) >= 3
    for index, block in enumerate(json_blocks, start=1):
        parsed = json.loads(block)
        assert parsed is not None, f"JSON listing {index} is empty"

    assert '\n{\n\n"`event_type`"' not in text
    assert '\n{\n\n"`scenario_id`"' not in text
    assert "\n`capability:`\n" not in text

    assert (
        "ложноположительных срабатываний на безопасных траекториях, ошибочно "
        "признанных опасными"
    ) in text
    assert (
        "ложноотрицательных срабатываний на опасных траекториях, ошибочно "
        "признанных безопасными"
    ) in text
    assert text.rstrip().endswith("документированными.")


def test_reader_route_is_honest_and_part_conclusions_are_explicit() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    introduction = text.split("# Часть I.", 1)[0]

    assert "### Основной читатель и границы книги" in introduction
    assert "**Основной читатель.**" in introduction
    assert "**В книгу намеренно не входит.**" in introduction
    assert "### Один исполняемый сценарий и два сценария переноса" in introduction
    assert "### Три сквозных сценария" not in introduction
    assert "### Канонические состояния выполнения" in introduction
    assert "`waiting_for_approval`" in introduction
    assert "`side_effect_unknown`" in introduction

    assert text.count("## Выводы части") == 8
    assert "### Минимальный исполняемый маршрут" in text
    assert "Матрица доказательств эталонного пакета" in text
    for level in (
        "Реализовано эталонным пакетом",
        "Продемонстрировано декларативно",
        "Требуется доказать в промышленной системе",
    ):
        assert level in text


def test_lifecycle_material_is_split_and_ordered_for_learning() -> None:
    text = EXPECTED.read_text(encoding="utf-8")

    parts = re.findall(r"^# Часть ([IVX]+)\. (.+)$", text, re.MULTILINE)
    assert parts == [
        ("I", "От демо-агента к платформе"),
        ("II", "Безопасность и контур управления"),
        ("III", "Память, знания и контекст"),
        ("IV", "Инструменты, выполнение и интеграция"),
        ("V", "Надежность, наблюдаемость и оценки"),
        ("VI", "Операционная модель, реестр и доверенные артефакты"),
        ("VII", "Заверение, реагирование и завершение жизненного цикла"),
        ("VIII", "Эталонная реализация и промышленный запуск"),
    ]

    expected_lifecycle_chapters = [
        (17, "Платформенная команда и продуктовые команды"),
        (18, "Поддерживаемые стандартные пути, общие шлюзы и борьба с агентным зоопарком"),
        (19, "Инвентаризация агентов, реестр и контроль разрастания"),
        (20, "От SDLC к ADLC: жизненный цикл агентной системы"),
        (21, "Цепочка поставки, происхождение и доверенные артефакты"),
        (22, "Наблюдаемость для ИИ-систем и телеметрия обнаружения"),
        (23, "Агентное несоответствие целей и внутренний риск"),
        (24, "Контур заверения: соревновательное тестирование, обнаружение и реагирование"),
        (25, "Вывод из эксплуатации, замена и дисциплина завершения жизненного цикла"),
    ]
    headings = [
        (int(number), title)
        for number, title in re.findall(r"^## Глава (\d+)\\\. (.+)$", text, re.MULTILINE)
    ]
    assert headings[16:25] == expected_lifecycle_chapters


def test_each_chapter_ends_before_part_level_material() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    chapters = re.findall(
        r"(?ms)^## Глава (\d+)\\\..*?"
        r"(?=^## Глава \d+\\\.|^## Выводы части|^# Часть |^# Заключение)",
        text,
    )
    assert chapters == [str(number) for number in range(1, 29)]

    for match in re.finditer(
        r"(?ms)^## Глава (\d+)\\\..*?"
        r"(?=^## Глава \d+\\\.|^## Выводы части|^# Часть |^# Заключение)",
        text,
    ):
        chapter = match.group(0)
        assert chapter.count("### Ключевые выводы") == 1
        assert chapter.count("### Источники главы") == 1
        assert chapter.index("### Ключевые выводы") < chapter.index("### Источники главы")
        assert "## Выводы части" not in chapter


def test_prose_quality_and_quickstart_are_editorially_consistent() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    introduction = text.split("# Часть I.", 1)[0]

    assert "git checkout ru-manuscript-editorial-2026-07" in introduction
    assert "uv sync --frozen --group dev" in introduction
    assert re.search(
        r"семантики «ровно один раз»\s*\(`exactly-once`\)", introduction
    )

    for residue in (
        "только тогда думай про многоагентную схему",
        "Главное практическое правило: отделяй инструкции от данных",
        "вне основного среды исполнения",
        "трасса остаётся читаемым",
        "Каталог событий справочного среды исполнения",
        "экспериментальная поэтапный выпуск",
        "не ушел ли среда исполнения",
        "у основного среды исполнения",
        "обнаруживать бесхозные, дублирующие и устаревшие агенты",
        "Эталонный runtime",
        "донаблюдать в проде",
        "Trace ID request must be a string, Trace ID not found in event file",
    ):
        assert residue not in text
    assert not re.search(r"среда исполнения обязан(?:\s|[.,;:])", text)
    assert not re.search(
        r"версия 2 в сценарии разбора обращений поддержки заменил(?:\s|,)", text
    )

    prose = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    prose = re.sub(r"`[^`]+`", "", prose)
    assert "“" not in prose
    assert "”" not in prose
    assert not re.search(r'"[^"\n]*[А-Яа-яЁё][^"\n]*"', prose)


def test_appendix_bibliography_has_unique_urls() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    appendix = text.split("## Приложение 4\\.", 1)[1].split("## Приложение 5\\.", 1)[0]
    urls = [
        url.replace("\\_", "_").replace("\\-", "-")
        for url in re.findall(r"\]\((https?://[^)]+)\)", appendix)
    ]
    assert len(urls) == len(set(urls))


def test_fast_moving_sources_use_canonical_versioned_links() -> None:
    text = EXPECTED.read_text(encoding="utf-8")

    for stale in (
        "platform.openai.com/docs/guides/agent-builder",
        "modelcontextprotocol.io/specification/draft/basic/authorization",
        "github.com/a2aproject/A2A/blob/main/docs/specification.md",
        "docs.langchain.com/oss/javascript/langgraph/durable-execution",
        "developers.cloudflare.com/agents/api-reference/durable-execution",
        "docs.cloud.google.com/agent-builder/overview",
        "gpt-5.4",
        "gpt-5-mini",
    ):
        assert stale not in text

    for canonical in (
        "developers.openai.com/api/docs/guides/agent-builder",
        "modelcontextprotocol.io/specification/2025-11-25/basic/authorization",
        "a2a-protocol.org/latest/specification/",
        "docs.langchain.com/oss/python/langgraph/persistence",
        "developers.cloudflare.com/agents/runtime/execution/durable-execution/",
        "docs.cloud.google.com/gemini-enterprise-agent-platform/overview",
        "approved-reasoning-model",
    ):
        assert canonical in text


def test_revision_repairs_key_pseudocode_and_language_residue() -> None:
    text = EXPECTED.read_text(encoding="utf-8")

    assert "```pseudocode\ndef run_manager(" in text
    assert "    for step in plan:" in text
    assert "class PolicyDecision:" in text
    assert "    requires_approval: bool = False" in text
    assert "class RunRequest:" in text
    assert "    policy_check(request)" in text

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
            ("```", "![", "[image", "* [", "* Глава", "##", "# ")
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

    assert "в игру вступает глава 24\\." in text
    assert "Глава 23\\. Агентное несоответствие целей и внутренний риск" in text
    assert "Глава 22\\. Наблюдаемость для ИИ-систем и телеметрия обнаружения" in text
    assert "Глава 19\\. Инвентаризация агентов, реестр и контроль разрастания" in text
    assert "из глав 26 и 27" in text
    assert "главы 19–25" in text

    assert "Покрытие обязательным подтверждением и трассировкой" in text
    assert "все высокорисковые внешние эффекты" in text
    assert "Цель для обеих долей — 100%" in text
    assert "занятые минуты проверяющих" in text

    causal_record = text[
        text.index("causal_case:\n") : text.index("**Три сквозных сценария.**")
    ]
    assert "edges:" in causal_record
    assert causal_record.count("evidence_ref:") == 3

    interceptor_example = text[
        text.index("request, request_meta") : text.index("Каждая ветка обязана вернуть")
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
        assert 480 <= width <= 1680
        assert 280 <= height <= 1280
        assert png[25] == 2  # Truecolor RGB without an alpha channel.


def test_revision_uses_explicit_unique_visual_assets_and_caption_order() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    image_paths = re.findall(r"^!\[[^\]]+\]\((visuals/[^)]+)\)$", text, re.MULTILINE)

    assert len(image_paths) == 54
    assert len(set(image_paths)) == 54
    assert [path for path in image_paths if "/ru-figure-" in path] == NUMBERED_FIGURE_PATHS
    assert [path for path in image_paths if "/ru-inline-diagram-" in path] == [
        f"visuals/ru-inline-diagram-{number:02d}.png" for number in range(1, 30)
    ]
    assert "![][image" not in text
    assert "data:image/" not in text
    assert not re.search(r"^\[image\d+\]:", text, re.MULTILINE)

    non_empty_lines = [line for line in text.splitlines() if line.strip()]
    captions = 0
    for index, line in enumerate(non_empty_lines):
        match = re.fullmatch(r"Рисунок (\d+)\\?\. .+", line)
        if match is None:
            continue
        captions += 1
        assert non_empty_lines[index - 1].startswith("![")
        assert NUMBERED_FIGURE_PATHS[int(match.group(1)) - 1] in non_empty_lines[index - 1]
    assert captions == 25


def test_diagram_semantics_preserve_safety_invariants_and_russian_terminology() -> None:
    diagrams = {
        item["number"]: item
        for item in json.loads(MANIFEST.read_text(encoding="utf-8"))["diagrams"]
    }
    combined = "\n".join(item["mermaid"] for item in diagrams.values())

    for residue in ("\\+", "backoff", "Span ", "baseline", '|"allow"|', '|"deny'):
        assert residue not in combined

    assert "Контролируемое чтение" in diagrams[5]["mermaid"]
    assert "Политика записи" in diagrams[5]["mermaid"]
    assert "Подтверждено отсутствие эффекта" in diagrams[10]["mermaid"]
    assert "Состояние по-прежнему неизвестно" in diagrams[10]["mermaid"]
    assert 'B["Успешность"] --> A["Здоровье агента поддержки"]' in diagrams[12]["mermaid"]
    assert diagrams[13]["caption"] == "Контур изменения, оценки, выпуска и обратной связи"
    assert "Поддерживаемый стандартный путь" in diagrams[15]["mermaid"]
    assert "Обратная связь продукта" in diagrams[15]["mermaid"]
    assert 'A["Требования"] --> B["Проектирование"]' in diagrams[17]["mermaid"]
    assert "Сквозные поверхности ADLC" in diagrams[17]["mermaid"]
    assert "Проверка происхождения и целостности" in diagrams[19]["mermaid"]
    assert "Попытка обхода старым маршрутом" in diagrams[21]["mermaid"]
    assert "Обнаружение и сдерживание" in diagrams[22]["mermaid"]
    assert "Наблюдаемый причинный путь" in diagrams[23]["mermaid"]
    assert "Контрфактический контроль" in diagrams[23]["mermaid"]
    assert "Сужение рабочей поверхности" in diagrams[24]["mermaid"]
    assert diagrams[19]["caption"] == (
        "Проверенный пакет выпуска объединяет связанные цепочки доверия"
    )
    assert "Проверка результата" in diagrams[25]["mermaid"]
    assert "Телеметрия и аудит" in diagrams[25]["mermaid"]
    assert "<-->" in diagrams[26]["mermaid"]
    assert '|"Требуется подтверждение"|' in diagrams[27]["mermaid"]
    assert "Решение человека" in diagrams[27]["mermaid"]


def test_numbered_diagram_manifest_covers_every_redesigned_figure() -> None:
    data = json.loads(NUMBERED_MANIFEST.read_text(encoding="utf-8"))
    diagrams = {item["number"]: item for item in data["diagrams"]}

    assert set(diagrams) == {1, 2, 6, 7, 8, 10, 11, 12, 13, 14, 17, 21, 22, 24, 25}
    assert "Часть VI" in diagrams[1]["mermaid"]
    assert "Часть VII" in diagrams[1]["mermaid"]
    assert "Часть VIII" in diagrams[1]["mermaid"]
    assert "Сложность эксплуатации и риск" in diagrams[2]["mermaid"]
    assert "Неизменное намерение + ключ идемпотентности" in diagrams[6]["mermaid"]
    assert '|"Разрешить"|' in diagrams[8]["mermaid"]
    assert '|"Запретить"|' in diagrams[8]["mermaid"]
    assert '|"Требуется подтверждение"|' in diagrams[8]["mermaid"]
    assert "Карантин" in diagrams[10]["mermaid"]
    assert "Политика исходящих соединений" in diagrams[11]["mermaid"]
    assert "Сверка внешнего состояния" in diagrams[13]["mermaid"]
    assert "Работа и наблюдение" in diagrams[17]["mermaid"]
    assert "Логическое И" in diagrams[24]["mermaid"]
    assert "РАСШИРИТЬ / УДЕРЖАТЬ" in diagrams[25]["mermaid"]
