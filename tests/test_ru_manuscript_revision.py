from __future__ import annotations

import json
import re
import struct
import subprocess
import sys
import textwrap
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

import pytest
import yaml

from docs.publisher.tools import revise_ru_manuscript as revision_tool
from docs.publisher.tools.revise_ru_manuscript import (
    remove_duplicate_evidence_boundary,
    replace_mermaid_blocks,
    revise,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/publisher/ru-manuscript-google-doc-final-2026-07-11.md"
EXPECTED = ROOT / "docs/publisher/ru-manuscript-editorial-2026-07-13.md"
MANIFEST = ROOT / "docs/publisher/ru-inline-diagrams-2026-07-13.json"
NUMBERED_MANIFEST = ROOT / "docs/publisher/ru-numbered-diagrams-2026-07-15.json"
EDITORIAL_MANIFEST = ROOT / "docs/publisher/ru-editorial-diagrams-2026-07-16.json"
VISUAL_AUDIT = ROOT / "docs/publisher/ru-visual-audit-2026-07-16.json"
VISUALS = ROOT / "docs/publisher/visuals"
COMPANION_EXAMPLES = ROOT / "docs/companion/examples"
INDEX_TERMS = ROOT / "docs/publisher/ru-index-terms-2026-07-27.md"
HUMAN_REVIEW_PACKET = ROOT / "docs/publisher/ru-human-review-packet-2026-07-27.md"
LEARNING_OUTCOME_MAP = ROOT / "docs/publisher/ru-learning-outcome-map-2026-07-27.md"
EDITORIAL_PACKET_BUILDER = (
    ROOT / "docs/publisher/tools/build_ru_editorial_packets.py"
)

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

EDITORIAL_DIAGRAM_PATHS = [
    "visuals/ru-editorial-diagram-01-execution-form-decision.png",
    "visuals/ru-editorial-diagram-02-registry-reconciliation.png",
]


def join_shell_continuations(text: str) -> str:
    return re.sub(r" \\\n\s*", " ", text)


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

    assert "git checkout ru-manuscript-editorial-2026-07-22" in appendix
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
    ) <= 8
    assert "docs/companion/runtime-reference/" in text
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
    assert "`run_start` открывает запуск" in text

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


def test_memory_examples_filter_before_ranking_without_isolation_overclaim() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    routing = text[
        text.index("**Листинг 10.") : text.index("**Частые ошибки**", text.index("**Листинг 10."))
    ]
    ranking = text[
        text.index("**Листинг 11.") : text.index(
            "### Сводки должны помогать читать",
            text.index("**Листинг 11."),
        )
    ]
    lab = text[
        text.index("### Лабораторная работа 3") : text.index(
            "# Часть IV.",
            text.index("### Лабораторная работа 3"),
        )
    ]

    for field in ("tenant_id", "provenance", "trust_state", "expires_at"):
        assert field in routing
        assert field in ranking
    assert ranking.index("eligible_for_prompt") < ranking.index("sorted(")
    assert 'record.trust_state == "trusted"' in ranking
    assert "record.tenant_id == tenant_id" in ranking
    assert "Память и область выборки" in lab
    assert "не доказывает аутентифицированную привязку" in lab
    assert "доказательством изоляции" not in lab
    assert "положительным доказательством изоляции" not in lab


def test_trace_examples_match_runtime_outcomes_and_privacy_contract() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    listing = text[
        text.index("**Листинг 18.") : text.index(
            "**Что особенно важно не логировать как есть.**",
            text.index("**Листинг 18."),
        )
    ]
    envelope = text[
        text.index("### Минимальная оболочка трассы") : text.index(
            "### Как связаны трасса и сессия",
            text.index("### Минимальная оболочка трассы"),
        )
    ]

    assert "ToolResult" in listing
    assert 'result.status != "success"' in listing
    assert "return result" in listing
    assert '"input_description": "[REDACTED]"' in envelope
    assert '"input_sha256"' in envelope
    assert '"input_class"' not in envelope
    assert '"input_digest"' not in envelope
    assert "неключевой SHA-256" in envelope
    assert "HMAC с управляемым секретным ключом" in envelope


def test_evidence_lifecycle_examples_are_fail_closed_and_materialized() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    change_listing = text[
        text.index("**Листинг 23.") : text.index(
            "#### Что чаще всего ломается в управлении изменениями",
            text.index("**Листинг 23."),
        )
    ]
    artifact_listing = text[
        text.index("**Листинг 24.") : text.index(
            "### Что чаще всего ломается в дисциплине артефактов",
            text.index("**Листинг 24."),
        )
    ]
    rollout_listing = text[
        text.index("**Листинг 35.") : text.index(
            "### Что чаще всего ломается в процессе запуска",
            text.index("**Листинг 35."),
        )
    ]
    slo = text[
        text.index("### Конфигурация SLO для агента поддержки") : text.index(
            "**Псевдокод классификации здоровья.**",
            text.index("### Конфигурация SLO для агента поддержки"),
        )
    ]
    adlc = text[
        text.index("#### Предлагаемая рамка ADLC") : text.index(
            "#### Чем ADLC полезен команде на практике",
            text.index("#### Предлагаемая рамка ADLC"),
        )
    ]

    assert "classify_change_surfaces" in change_listing
    assert "review_required" in change_listing
    assert "unknown_surfaces" in change_listing
    assert "verify_evidence_manifest" in artifact_listing
    assert "artifact_ids" in artifact_listing
    assert "diagnostics" in artifact_listing
    assert "has_owner: bool" not in artifact_listing
    assert "RolloutPolicy.from_dict" in rollout_listing
    assert "assess_rollout" in rollout_listing
    assert "blocking_signals" in rollout_listing
    for term in (
        "slo_id",
        "owner",
        "window",
        "numerator",
        "denominator",
        "exclusions",
        "data_source",
        "action_on_breach",
        "safety_invariants",
    ):
        assert term in slo
    for term in (
        "transition_id",
        "from_state",
        "to_state",
        "required_evidence",
        "decision",
        "decided_at",
    ):
        assert term in adlc

    examples = {
        "context-manifest-support-ticket.yaml": "context_manifest_id",
        "threat-map-negative-tests.yaml": "threat_map_id",
        "slo-card-support-ticket.yaml": "slo_id",
        "adlc-transition-support-ticket.yaml": "transition_id",
        "readiness-rubric-support-ticket.yaml": "hard_blockers",
    }
    for filename, required_key in examples.items():
        payload = yaml.safe_load(
            (COMPANION_EXAMPLES / filename).read_text(encoding="utf-8")
        )
        assert required_key in payload

    rubric = yaml.safe_load(
        (COMPANION_EXAMPLES / "readiness-rubric-support-ticket.yaml").read_text(
            encoding="utf-8"
        )
    )
    assert [level["score"] for level in rubric["levels"]] == [0, 1, 2, 3, 4]
    assert rubric["hard_blockers"]


def test_reader_journey_best_practices_pass_is_applied_without_identifier_damage() -> None:
    text = EXPECTED.read_text(encoding="utf-8")

    assert "**Шаблон первого артефакта: архитектурный бриф безопасного агента.**" in text
    assert "Пример для агента поддержки:" in text
    assert "первая волна остается в режиме `hold`" in text
    assert text.count("Короткий пример:") == 5
    assert "### Диагностический вопрос для операционной модели платформы" in text
    assert "### Порог готовности поддерживаемого стандартного пути" in text
    assert "### Диагностический вопрос для дисциплины изменений" in text
    assert "### Порог готовности к поэтапному выпуску" in text
    assert "## Как пользоваться приложениями" in text
    assert "### Сквозные источники и источники глав" in text

    assert "workflow_logic" in text
    assert "workflow_runtime_v2" in text
    assert "workflow_agent" in text
    assert "рабочий процесс_logic" not in text
    assert "рабочий процесс_runtime" not in text
    assert "рабочий процесс_agent" not in text
    assert "скрипт или конвейер блокирует завершение" in text
    assert "скрипт или pipeline блокирует завершение" not in text

    assert "### Конфигурация управления агентной платформой (YAML)" in text
    assert "### Конфигурация (YAML): управления для агентной платформы" not in text
    assert (
        text.count(
            "**Каталог поддерживаемых шаблонов нужен не только для контроля, но и для скорости.**"
        )
        == 1
    )
    assert "Хорошая антизоопарк-работа делает обходы менее выгодными" in text
    assert "обходи менее выгодными" not in text
    assert "типовых золотых пути" not in text
    assert "2-4 типовых поддерживаемых пути" in text

    chapter_17 = text[text.index("## Глава 17") : text.index("## Глава 18")]
    chapter_18 = text[text.index("## Глава 18") : text.index("## Глава 19")]
    for chapter in (chapter_17, chapter_18):
        words = len(re.findall(r"[A-Za-zА-Яа-яЁё0-9_]+", chapter))
        bullets = len(re.findall(r"(?m)^\s*[*-]\s+", chapter))
        assert bullets / words * 1000 < 50


def test_technical_book_editorial_standards_pass_removes_scaffolding() -> None:
    text = EXPECTED.read_text(encoding="utf-8")

    for residue in (
        "Быстрее всего здесь меняются:",
        "Медленнее меняются:",
        "Уникальный артефакт:",
        "Граница с соседними главами:",
        "Что эта глава не покрывает:",
        "verifiercontractrequiredforhigh_risk",
        "onuntrustedverifier_contract",
        "mcpauth_mode",
    ):
        assert residue not in text

    for expected in (
        "**Практический ориентир.** Перед проектированием долговременной памяти",
        "**Таблица решений для владельцев.**",
        "**До и после стандартного пути.**",
        "**Практический маршрут главы.** Читайте эту главу рядом с эталонным пакетом.",
        "**Порядок первичного разбора.**",
        "**Срез практики. Июль 2026 года.** Быстрее всего меняются техники "
        "соревновательного тестирования",
    ):
        assert expected in text

    assert text.count("**Как читать листинг.**") == 37
    assert "Expected seven previously unlabeled long examples" not in text


def test_bookcraft_readability_pass_removes_markdown_heading_artifacts() -> None:
    text = EXPECTED.read_text(encoding="utf-8")

    assert not re.search(r"(?m)^#{2,3} \*\*.+\*\*$", text)

    for expected in (
        "### Когда подсказка становится архитектурой",
        "### Где заканчиваются инструкции и начинается контроль",
        "### Координатор без потери ответственности",
        "### Долговечное состояние запуска",
        "### Именованный агент как отдельная топология",
        "### Очередь работ как операторский контур",
        "### Проверяемое завершение",
        "**Что изменилось после этой главы.** Выбор формы исполнения теперь можно защитить",
        "**Что изменилось после этой главы.** У читателя теперь есть не просто список модулей",
    ):
        assert expected in text

    for residue in (
        "### **От инструкций к исполняемому сценарию**",
        "### **Координатор и передача управления**",
        "## **Последовательность внедрения**",
        "## **Главный критерий**",
    ):
        assert residue not in text

    assert "eval_набор данных" not in text
    assert "process_оценка" not in text


def test_advanced_bookcraft_pass_adds_reader_bridges_and_breaks_up_dense_sections() -> None:
    text = EXPECTED.read_text(encoding="utf-8")

    chapter_bridges = {
        5: "Возможность теперь рассматривается не как имя функции",
        11: "MCP, песочница и A2A теперь образуют разные",
        15: "Оценивание теперь связано с выпуском",
        16: "Цепочка доказательств теперь проходит",
        20: "ADLC теперь выглядит не как новое название",
        24: "Инцидент теперь заканчивается не отчетом",
        28: "Готовность к запуску теперь можно доказать",
    }
    for number, expected in chapter_bridges.items():
        chapter = text.split(f"## Глава {number}\\.", 1)[1]
        if number < 28:
            chapter = chapter.split(f"## Глава {number + 1}\\.", 1)[0]
        assert chapter.count("**Что изменилось после этой главы.**") == 1
        assert expected in chapter

    for heading in (
        "### MCP как граница безопасности",
        "### Матрица угроз MCP",
        "### Сокращенная поверхность инструментов для больших API",
        "### Управляемая MCP-поверхность платформы",
        "### Корпоративный контур управления MCP",
        "### Теневые серверы и фактическая поверхность доступа",
        "### Симуляция пользователя и среды",
        "### От оценки к выпускному действию",
        "### Проверяемые условия завершения запуска",
        "### Что сохраняется из классического SDLC",
        "### Где классический процесс становится недостаточным",
        "### ADLC как расширение инженерного цикла",
        "### Заверение безопасности и цепочка поставки",
        "### От событий к причинной гипотезе",
        "### Три сквозных сценария инцидентов",
        "### Содержание разбора инцидента",
        "### Разделение программного каркаса, испытательного контура и среды исполнения",
        "### Управляемый контур исполнения агента",
        "### Долговечная идентичность и восстанавливаемая работа",
        "### Агент и рабочий процесс как разные границы",
    ):
        assert heading in text

    dense_headings = (
        "MCP как граница безопасности",
        "Матрица угроз MCP",
        "Управляемая MCP-поверхность платформы",
        "Корпоративный контур управления MCP",
        "Теневые серверы и фактическая поверхность доступа",
        "Симуляция пользователя и среды",
        "От оценки к выпускному действию",
        "Проверяемые условия завершения запуска",
        "Именованный агент как отдельная топология",
        "Управляемый контур исполнения агента",
        "Долговечная идентичность и восстанавливаемая работа",
        "Агент и рабочий процесс как разные границы",
    )
    heading_matches = list(re.finditer(r"(?m)^#{3,4} (.+)$", text))
    section_words: dict[str, int] = {}
    for index, match in enumerate(heading_matches):
        heading = match.group(1)
        if heading not in dense_headings:
            continue
        end = (
            heading_matches[index + 1].start()
            if index + 1 < len(heading_matches)
            else len(text)
        )
        section_words[heading] = len(
            re.findall(r"[A-Za-zА-Яа-яЁё0-9_]+", text[match.end() : end])
        )

    assert set(section_words) == set(dense_headings)
    assert max(section_words.values()) <= 750


def test_source_appendix_is_grouped_into_reader_sized_runs() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    appendix = text.split("## Приложение 4\\.", 1)[1].split(
        "## Приложение 5\\.", 1
    )[0]

    for heading in (
        "#### Основные архитектурные руководства",
        "#### Протоколы и программные каркасы",
        "#### Облачные платформы и долговечное исполнение",
        "#### Облачные агенты разработки",
        "#### Управление и заверение",
        "#### Наблюдение за отклонениями и автономией",
    ):
        assert heading in appendix

    source_runs: list[int] = []
    current_run = 0
    for line in appendix.splitlines():
        if re.match(r"^\*\*S\d{3}\.\*\*", line):
            current_run += 1
            continue
        if current_run:
            source_runs.append(current_run)
            current_run = 0
    source_runs.append(current_run)

    assert max(source_runs) <= 12


def test_source_entries_use_bibliographic_paragraphs_and_restore_prose_rhythm() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    source_entries = re.findall(r"^\*\*S\d{3}\.\*\* .+$", text, re.MULTILINE)

    assert len(source_entries) >= 200
    assert not re.search(r"^\* \*\*S\d{3}\.\*\*", text, re.MULTILINE)

    prose = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    words = re.findall(r"[A-Za-zА-Яа-яЁё0-9]+", prose)
    list_words: list[str] = []
    for line in prose.splitlines():
        if re.match(r"^\s*(?:[*+-]|\d+\.)\s+", line):
            list_words.extend(re.findall(r"[A-Za-zА-Яа-яЁё0-9]+", line))

    assert len(list_words) / len(words) <= 0.265


def test_reference_package_quickstart_has_task_oriented_subsections() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    appendix = text.split("## Приложение 5\\.", 1)[1]
    quickstart = appendix.split("### Как запустить", 1)[1].split(
        "### Карта модулей", 1
    )[0]

    for heading in (
        "#### Быстрый запуск и ожидаемое состояние",
        "#### Проверка отдельных контрактов",
        "#### Память, трассы и повторный прогон",
        "#### Выпуск, непрерывные контроли и сессии",
    ):
        assert heading in quickstart


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


def test_print_manuscript_uses_book_native_navigation() -> None:
    text = EXPECTED.read_text(encoding="utf-8")

    for residue in (
        "отдельная страница",
        "отдельную страницу",
        "навигации по сайту",
        "живой навигации сайта",
        "после этой страницы",
        "со страницей",
        "первый экран",
        "Доказательный каркас",
    ):
        assert residue not in text

    assert text.count("главе 16") >= 3
    assert "главе 16 «Сквозная цепочка доказательств»" in text


def test_chapters_16_and_27_have_one_reader_contract_and_direct_openings() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    chapter_sixteen = text.split("## Глава 16\\.", 1)[1].split(
        "## Выводы части", 1
    )[0]
    chapter_twenty_seven = text.split("## Глава 27\\.", 1)[1].split(
        "## Глава 28\\.", 1
    )[0]

    assert "Что вы должны уметь после этой страницы" not in chapter_sixteen
    assert "Зачем нужен этот раздел" not in chapter_sixteen
    assert "Заметка о сквозной цепочке доказательств" not in chapter_sixteen
    assert "разрешил расширение выпуска" in chapter_sixteen[:1800]
    assert "не может восстановить основание решения" in chapter_sixteen[:1800]

    assert "Что унести из главы" not in chapter_twenty_seven
    assert "Мост зрелости" not in chapter_twenty_seven
    assert "### От правила к исполняемому решению" in chapter_twenty_seven


def test_reference_appendix_is_stable_and_has_one_learning_route() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    appendix = text.split("## Приложение 5\\.", 1)[1]

    headings = (
        "### Границы эталона",
        "### Как запустить",
        "### Карта модулей",
        "### Воспроизводимые проверки",
        "### Контрактные примеры",
        "### Критерии самопроверки по частям",
    )
    positions = [appendix.index(heading) for heading in headings]
    assert positions == sorted(positions)

    for changelog_marker in (
        "Недавние обновления",
        "теперь возвращает",
        "теперь показывает",
        "теперь помогает",
        "теперь задуман",
        "теперь появляется",
        "Теперь в нем",
        "теперь он уже",
        "пакет стал",
        "книга теперь",
        "Книга теперь",
        "теперь пакет",
    ):
        assert changelog_marker not in appendix


def test_dense_chapters_balance_explanation_and_checklists() -> None:
    text = EXPECTED.read_text(encoding="utf-8")

    def list_word_share(block: str) -> float:
        block = re.sub(r"```.*?```", "", block, flags=re.DOTALL)
        words = re.findall(r"[A-Za-zА-Яа-яЁё0-9]+", block)
        list_words = []
        for line in block.splitlines():
            if re.match(r"^\s*(?:[*+-]|\d+\.)\s+", line):
                list_words.extend(re.findall(r"[A-Za-zА-Яа-яЁё0-9]+", line))
        return len(list_words) / len(words)

    for number, cap in {4: 0.45, 19: 0.42, 22: 0.38, 25: 0.38}.items():
        assert list_word_share(revision_tool.extract_chapter(text, number)) < cap, number

    assert len(
        re.findall(r"[A-Za-zА-Яа-яЁё0-9]+", revision_tool.extract_chapter(text, 11))
    ) < 4600
    assert len(
        re.findall(r"[A-Za-zА-Яа-яЁё0-9]+", revision_tool.extract_chapter(text, 15))
    ) < 4625


def test_reference_heavy_chapters_use_lists_only_for_scannable_decisions() -> None:
    text = EXPECTED.read_text(encoding="utf-8")

    def list_word_share(block: str) -> float:
        block = re.sub(r"```.*?```", "", block, flags=re.DOTALL)
        words = re.findall(r"[A-Za-zА-Яа-яЁё0-9]+", block)
        list_words: list[str] = []
        for line in block.splitlines():
            if re.match(r"^\s*(?:[*+-]|\d+\.)\s+", line):
                list_words.extend(re.findall(r"[A-Za-zА-Яа-яЁё0-9]+", line))
        return len(list_words) / len(words)

    caps = {2: 0.40, 10: 0.40, 13: 0.35, 16: 0.40, 22: 0.38, 24: 0.31, 25: 0.38}
    for number, cap in caps.items():
        assert list_word_share(revision_tool.extract_chapter(text, number)) < cap, number


def test_event_catalogue_teaches_the_contract_without_becoming_a_schema_dump() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    chapter = text.split("## Глава 13\\.", 1)[1].split("## Глава 14\\.", 1)[0]

    for heading in (
        "#### Запуск и контекст",
        "#### Политики, инструменты и подтверждения",
        "#### Память и фоновые операции",
        "#### Завершение и управленческие действия",
    ):
        assert heading in chapter

    for event_type in (
        "run_start",
        "policy_precheck",
        "agent_threat_evidence",
        "retrieval",
        "context_layers_built",
        "tool_policy_decision",
        "mcp_tool_risk_review",
        "tool_execution",
        "a2a_handoff",
        "approval_requested",
        "sandbox_profile_reviewed",
        "memory_write_decision",
        "memory_persisted",
        "background_compaction",
        "background_update_scheduled",
        "verification_result",
        "run_failed",
        "governance_action",
        "run_complete",
    ):
        assert f"`{event_type}`" in chapter

    assert "Машинная схема событий" in chapter
    assert "без контрактов полезная нагрузка быстро превращается в мусор" not in chapter
    assert "контракт доверия передачи управления A2A (контракт доверия" not in chapter


def test_reader_facing_language_is_grammatical_and_russian_first() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    prose = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    prose_without_identifiers = re.sub(r"`[^`]+`", "", prose)
    prose_without_links = re.sub(
        r"!?\[[^\]]+\]\([^)]+\)", "", prose_without_identifiers
    )
    prose_without_links = re.sub(r"https?://[^)\s]+", "", prose_without_links)
    prose_without_links = re.sub(
        r"(?m)^\*\*S\d{3}\.\*\*.*$", "", prose_without_links
    )

    for residue in (
        "приемы подсказкаинга",
        "страницы политик",
        "среда исполнения вообще обязан отслеживать",
        "что сделал среда исполнения",
        "между подтверждение и возобновление",
        "среда исполнения не обязан реализовывать",
        "Минимально зрелый среда исполнения",
        "Эталонная среда исполнения полезен",
        "не проектируй память",
        "если уже строишь",
        "если вы правда борешься",
        "живой жизненный цикл сессии",
        "контекста арендатора/субъект",
        "телеметрия помогает и разбора инцидента",
        "телеметрический выхлоп",
        "надежной сырая история",
        "`tool_execution` полезная нагрузка",
    ):
        assert residue not in prose

    assert "долгий запуск, сессия или делегирование не выпадают из контроля" in prose
    assert "Поля `status`, `result` и `failure_reason` остаются раздельными" in prose

    for anglicism in ("fallback", "stateful", "stateless", "assurance", "governance"):
        assert not re.search(rf"(?i)\b{anglicism}\b", prose_without_links)
    for identifier_term in ("principal", "payload"):
        assert not re.search(rf"(?i)\b{identifier_term}\b", prose_without_links)

    assert "среда выполнения" not in prose_without_links
    for heading in (
        "### Поверхность инструментов это не то же самое, что управляемая поверхность возможностей",
        "### Каталог инструментов это интерфейс платформы, а не список случайных функций",
        "### Песочница это не обязательно контейнер, а прежде всего режим ограничений",
        "### Самый неприятный статус это `side_effect_unknown`",
        "### Поддерживаемый стандартный путь это не «документ с набором советов», "
        "а рабочий путь по умолчанию",
    ):
        assert heading not in text


def test_final_copyedit_removes_known_grammar_and_terminology_residue() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    prose = re.sub(r"```.*?```", "", text, flags=re.DOTALL)

    for residue in (
        "Сквозной сценарий История",
        "Сквозные сценарии управляющего агента и передачи управления Выбор",
        "Сквозные сценарии MCP и A2A Выбор",
        "не эксплуатационный среда исполнения",
        "центральный среда исполнения",
        "какой MCP-точка доступа",
        "первый среда исполнения",
        "минимальный полезная нагрузка обычно должен",
        "Справочный среда исполнения",
        "второго скрытого среды исполнения",
        "контур уверенности",
        "политический шлюз",
        "wrapper-слоев",
        "Среде выполнения",
        "служит также явное место",
    ):
        assert residue not in prose

    assert "контур заверения" in prose
    assert "шлюз политики" in prose
    assert "оберточных слоев" in prose
    assert "эталонная среда исполнения" in prose
    assert "агентск" not in prose.casefold()


def test_machine_identifiers_and_diagnostics_are_reader_ready() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    prose = re.sub(r"```.*?```", "", text, flags=re.DOTALL)

    for residue in (
        "Config at {config\\_path\\!s} must be a mapping at the top level",
        "{label} config must be a mapping",
        "{key} must be a list",
        "внутри RunContext хранятся retrieved_context и retrieved_records",
        "показывают count, records, status и result",
    ):
        assert residue not in prose

    for identifier in (
        "`RunContext`",
        "`retrieved_context`",
        "`retrieved_records`",
        "`count`",
        "`records`",
        "`status`",
        "`result`",
    ):
        assert identifier in prose


def test_listing_introductions_set_a_specific_reading_task() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    generic = (
        "назначение: сделать контракт раздела проверяемым; перед промышленным "
        "применением требуется адаптация к схеме и ограничениям организации"
    )
    guides = re.findall(
        r"^\*\*Как читать листинг\.\*\* (.+)$", text, re.MULTILINE
    )

    assert generic not in text
    assert len(re.findall(r"^\*\*Листинг \d+\.", text, re.MULTILINE)) == 37
    assert len(guides) == 37
    assert len(set(guides)) == 37
    assert all(len(guide.split()) >= 12 for guide in guides)


def test_repeated_diagnostic_formula_is_replaced_with_chapter_specific_prose() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    assert "Если большинство этих условий не выполняется" not in text
    assert (
        "Числовые пороги в книге являются учебными примерами, если рядом прямо "
        "не указано, что это инвариант контракта."
    ) in text


def test_source_notes_are_specific_without_repeating_one_global_caveat() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    caveat = "платформенный пример не следует читать как универсальную гарантию"

    assert text.count(caveat) == 1
    assert text.count("### Источники главы") == 28
    assert "**Как читать источники.**" not in text
    for number in range(1, 29):
        sources = revision_tool.extract_chapter(text, number).split(
            "### Источники главы", 1
        )[1]
        assert re.search(r"^\*\*S\d+\.\*\*", sources, re.MULTILINE)
    assert "**Граница переносимости источников.**" in text


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


def test_parts_and_dense_chapters_have_editorial_navigation() -> None:
    text = EXPECTED.read_text(encoding="utf-8")

    assert text.count("**Маршрут части.**") == 8
    for marker in (
        "#### Полномочия и идентичность",
        "#### Контракт сервера и граница доверия",
        "#### Два взаимодополняющих контура",
        "### Долговечное состояние запуска",
        "### От событий к причинной гипотезе",
    ):
        assert marker in text

    chapter_one = text.split("## Глава 1\\.", 1)[1].split("## Глава 2\\.", 1)[0]
    assert chapter_one.count("**Граница доказательств.**") == 1

    chapter_twenty_three = text.split("## Глава 23\\.", 1)[1].split(
        "## Глава 24\\.", 1
    )[0]
    assert "В 09:05" in chapter_twenty_three[:800]
    assert "Предыдущая глава определила" not in chapter_twenty_three[:800]


def test_duplicate_evidence_cleanup_refuses_to_delete_edited_prose() -> None:
    text = (
        "## Глава 1\\. Первая\n\n"
        "**Граница доказательств**\n\n"
        "Эта глава доказывает не то, что агенты всегда нужны. Наоборот: она "
        "показывает, что полезная агентность начинается с ограничения.\n\n"
        "Если путь можно заранее описать, лучше начать с рабочего процесса. Если "
        "нужна гибкость, ее стоит добавлять только вместе с владением, границами "
        "политики, подтверждениями, следами выполнения и оценочными сигналами. "
        "Поэтому главный вывод главы такой: агент — не замена инженерной дисциплине, "
        "а усиленная нагрузка на нее.\n\n"
        "### Что подтверждают материалы главы\n\n"
        "Сохранить этот текст.\n\n"
        "**Граница доказательств**\n\n"
        "Сохранить основной блок.\n\n"
        "## Глава 2\\. Вторая\n"
    )

    with pytest.raises(ValueError, match="duplicate evidence-boundary block changed"):
        remove_duplicate_evidence_boundary(text)


def test_every_chapter_has_a_traceable_source_set() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    high_evidence_chapters = {4, 5, 6, 11, 12, 13, 14, 15, 16, 20, 21, 22, 23, 24, 25, 28}
    appendix = text.split("## Приложение 4\\.", 1)[1].split(
        "## Приложение 5\\.", 1
    )[0]
    appendix_ids = re.findall(r"^\*\*(S\d{3})\.\*\*", appendix, re.MULTILINE)

    assert len(appendix_ids) >= 90
    assert len(appendix_ids) == len(set(appendix_ids))

    for number in range(1, 29):
        chapter = revision_tool.extract_chapter(text, number)
        sources = chapter.split("### Источники главы", 1)[1]
        source_ids = re.findall(r"^\*\*(S\d{3})\.\*\*", sources, re.MULTILINE)
        minimum = 3 if number in high_evidence_chapters else 2
        assert len(source_ids) >= minimum, (
            f"Chapter {number} has only {len(source_ids)} source identifiers"
        )
        assert set(source_ids) <= set(appendix_ids)
        assert "http" not in sources
        assert "**Как читать источники.**" not in sources

    claim_references = re.findall(
        r"\(см\. источники? \*\*S\d{3}\*\*(?:, \*\*S\d{3}\*\*)*\)", text
    )
    assert len(claim_references) >= 16


def test_every_technical_block_is_explicitly_classified() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    lines = text.splitlines()
    inside = False
    start = 0
    block: list[str] = []
    missing: list[int] = []

    for index, line in enumerate(lines):
        if not line.startswith("```"):
            if inside:
                block.append(line)
            continue
        if not inside:
            inside = True
            start = index
            block = []
            continue

        nearby = [item.strip() for item in lines[max(0, start - 10) : start] if item.strip()]
        if not any(
            re.search(
                r"(?:Листинг|Тип фрагмента|Исполняемый пример|Конфигурация|"
                r"Псевдокод|Вывод программы|Команд[аы]|Шаг \d+\.)",
                item,
                re.IGNORECASE,
            )
            for item in nearby[-6:]
        ):
            missing.append(start + 1)
        inside = False

    assert missing == []


def test_appendix_gives_self_study_feedback_and_clean_bibliography() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    appendix_five = text.split("## Приложение 5\\.", 1)[1]
    assert "### Критерии самопроверки по частям" in appendix_five
    assert appendix_five.count("**Сильный ответ.**") == 8
    assert appendix_five.count("**Недостаточный ответ.**") == 8
    assert appendix_five.count("**Проверяемый артефакт.**") == 8

    bibliography = text.split("## Приложение 4\\.", 1)[1].split(
        "## Приложение 5\\.", 1
    )[0]
    assert not re.search(r"\[[^\]]*https?://", bibliography)
    source_lines = [
        line
        for line in bibliography.splitlines()
        if re.match(r"^\*\*S\d{3}\.\*\*", line) and "http" in line
    ]
    assert source_lines
    assert all("дата обращения:" in line for line in source_lines)


def test_labs_have_prerequisites_timing_and_negative_paths() -> None:
    text = EXPECTED.read_text(encoding="utf-8")

    assert text.count("**Предварительные условия.**") == 8
    assert text.count("**Ориентировочное время.**") == 8
    assert text.count("**Отрицательная проверка.**") == 8
    assert text.count("**Если результат отличается.**") == 8
    assert text.count("**Дополнительное задание.**") == 8


def test_developmental_editing_removes_chapter_one_assembly_residue() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    chapter_one = revision_tool.extract_chapter(text, 1)
    chapter_two = revision_tool.extract_chapter(text, 2)

    for residue in (
        "### Короткий вывод",
        "### Что подтверждают материалы главы",
        "Доказательства: кратко",
        "Авторская интерпретация главы уже жестче",
        "Противоположный взгляд:",
        "### Правила выбора: рабочий процесс, одиночный агентный цикл или многоагентная схема",
    ):
        assert residue not in chapter_one

    assert chapter_one.count("### Ключевые выводы") == 1
    assert "### Архитектурный бриф и лестница автономности" in chapter_two
    assert "**Шаблон первого артефакта: архитектурный бриф безопасного агента.**" in chapter_two
    assert "Рисунок 2. Рост сложности и требований к контролю" in chapter_two


def test_dense_chapters_have_four_explicit_instructional_acts() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    expected_acts = {
        5: [
            "От идентичности к праву на действие",
            "Возможность как исполняемый контракт",
            "Политика и подтверждение в среде исполнения",
            "От минимального контракта к промышленному управлению",
        ],
        11: [
            "Ограниченная среда исполнения",
            "MCP как граница интеграции и доверия",
            "Управление серверной поверхностью",
            "Состояние, делегирование и выбор протокола",
        ],
        20: [
            "Что сохраняется из SDLC",
            "ADLC как жизненный цикл доказательств",
            "Управление изменениями по риску",
            "Выпуск, откат и происхождение",
        ],
        24: [
            "От сигнала риска к находке",
            "Сдерживание и оперативное реагирование",
            "Причинный разбор и проверка гипотезы",
            "Закрытие находки и обратная связь",
        ],
        26: [
            "Базовый поток и границы модулей",
            "Долговечное выполнение и восстановление",
            "Топологии агента, процесса и очереди",
            "Контракт эталона и проверка завершения",
        ],
    }

    for chapter_number, expected in expected_acts.items():
        chapter = revision_tool.extract_chapter(text, chapter_number)
        top_sections = re.findall(r"^### (.+)$", chapter, re.MULTILINE)
        instructional = [
            heading
            for heading in top_sections
            if heading not in {"Ключевые выводы", "Источники главы"}
        ]
        assert instructional == expected


def test_developmental_editing_reduces_list_density_and_editorial_scaffolding() -> None:
    text = EXPECTED.read_text(encoding="utf-8")

    def ordinary_list_blocks(chapter: str) -> int:
        chapter = chapter.split("### Источники главы", 1)[0]
        chapter = re.sub(r"```.*?```", "", chapter, flags=re.DOTALL)
        blocks = 0
        inside_list = False
        for line in chapter.splitlines():
            if re.match(r"^\s*(?:[*+-]|\d+\\?\.)\s+", line):
                if not inside_list:
                    blocks += 1
                inside_list = True
            elif line.strip():
                inside_list = False
        return blocks

    assert not re.search(r"\n{4,}", revision_tool.extract_chapter(text, 24))
    for number, cap in {5: 30, 20: 22, 24: 22}.items():
        assert ordinary_list_blocks(revision_tool.extract_chapter(text, number)) <= cap

    assert "**Как читать источники.**" not in text
    assert "Практический результат:" not in text
    assert text.count("Как читать эту главу.") <= 5


def test_labs_use_discrete_steps_observations_and_proof_statements() -> None:
    text = EXPECTED.read_text(encoding="utf-8")

    def extract_lab(number: int) -> str:
        start = re.search(
            rf"^### Лабораторная работа {number}\\?\..*$",
            text,
            re.MULTILINE,
        )
        assert start
        end = re.search(
            r"^(?:# Часть [IVX]+\.|## Итоговый проект\.)",
            text[start.end() :],
            re.MULTILINE,
        )
        assert end
        return text[start.start() : start.end() + end.start()]

    for number in range(1, 9):
        lab = extract_lab(number)
        steps = [int(value) for value in re.findall(r"^#### Шаг (\d+)\.", lab, re.MULTILINE)]
        assert len(steps) >= 3, number
        assert steps == list(range(1, len(steps) + 1)), number
        assert "**Что доказывает результат.**" in lab, number

    for number in range(2, 9):
        lab = extract_lab(number)
        assert lab.count("**Наблюдение.**") >= 2, number
        for console in re.findall(r"```console\n(.*?)```", lab, re.DOTALL):
            assert console.count("uv run ") <= 1, (number, console)


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
    text = join_shell_continuations(EXPECTED.read_text(encoding="utf-8"))

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
    text = join_shell_continuations(EXPECTED.read_text(encoding="utf-8"))

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

    assert "ложноположительных результатов на безопасных траекториях" in text
    assert "ложноотрицательных результатов на опасных траекториях" in text
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


def test_chapter_transitions_are_folded_into_practical_steps() -> None:
    text = EXPECTED.read_text(encoding="utf-8")

    assert "**Дальше.**" not in text
    for number in range(1, 29):
        chapter = text.split(f"## Глава {number}\\.", 1)[1]
        if number < 28:
            chapter = chapter.split(f"## Глава {number + 1}\\.", 1)[0]
        practical_steps = re.findall(
            r"^\*\*Практический шаг\.\*\* .+$",
            chapter,
            re.MULTILINE,
        )
        assert len(practical_steps) == 1, number
        assert len(re.findall(r"[.!?]", practical_steps[0])) >= 2, number


def test_final_book_pass_defines_acronyms_and_notation_before_use() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    introduction = text.split("# Часть I.", 1)[0]

    assert "### Сокращения и обозначения" in introduction
    definitions = {
        "SLO": "**SLO** — целевой показатель уровня обслуживания",
        "SLI": "**SLI** — показатель уровня обслуживания",
        "MCP": "**MCP** — Model Context Protocol",
        "A2A": "**A2A** — Agent2Agent",
        "HITL": "**HITL** — human in the loop",
        "RACI": "**RACI** — матрица ответственности",
        "SDLC": "**SDLC** — жизненный цикл разработки программного обеспечения",
        "ADLC": "**ADLC** — жизненный цикл агентной системы",
        "IAM": "**IAM** — управление идентичностью и доступом",
        "RAG": "**RAG** — генерация с дополнением из найденного контекста",
        "DLP": "**DLP** — предотвращение утечек данных",
        "SDK": "**SDK** — комплект средств разработки",
        "LLM": "**LLM** — большая языковая модель",
    }
    for acronym, definition in definitions.items():
        assert definition in introduction
        first_use = re.search(rf"(?<![A-Z]){acronym}(?![A-Z])", introduction)
        assert first_use is not None
        assert first_use.start() == introduction.index(definition) + 2

    assert "Моноширинным начертанием" in introduction
    assert "Метка «Тип фрагмента»" in introduction
    assert "значение в угловых скобках" in introduction


def test_submission_readiness_pass_orders_front_matter_and_adds_prerequisite_check() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    introduction = text.split("# Часть I.", 1)[0]

    ordered_headings = (
        "### Какую проблему решает книга",
        "### Для кого эта книга",
        "### Основной читатель и границы книги",
        "### Один исполняемый сценарий и два сценария переноса",
        "### Как читать книгу",
        "### Самопроверка перед практическим маршрутом",
        "### Сокращения и обозначения",
        "### Структура аргумента",
    )
    positions = [introduction.index(heading) for heading in ordered_headings]
    assert positions == sorted(positions)
    assert "запустить модуль Python из командной строки" in introduction
    assert "объяснить разницу между повтором запроса" in introduction
    assert "прочитайте вводные разделы глав 4, 10, 13 и 17" in introduction


def test_submission_readiness_pass_removes_residual_anglicisms_and_meta_labels() -> None:
    text = EXPECTED.read_text(encoding="utf-8")

    for residue in (
        "на масштабе всего estate",
        "конкретному release",
        "инженерная проверка в pull request",
        "истечения срока capability-session",
        "rug pull attack",
        "Текстовый дубль схемы",
    ):
        assert residue not in text

    for replacement in (
        "в масштабе всего парка агентов",
        "привязанную к конкретному выпуску",
        "инженерная проверка в запросе на слияние",
        "истечения срока сессии возможности",
        "подмена после одобрения (`rug pull`)",
        "Схему можно прочитать так:",
    ):
        assert replacement in text


def test_submission_readiness_pass_consolidates_chapter_21_provenance_lists() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    chapter = revision_tool.extract_chapter(text, 21)

    assert "Таблица 6. Поверхности доверия и доказательства выпуска" in chapter
    assert (
        "| Поверхность | Что версионировать и чье происхождение сохранять | "
        "Доказательство перед выпуском |"
    ) in chapter
    for repeated_list in (
        "В агентной платформе к ним часто относятся:\n\n*",
        "Вам нужно уметь отвечать:\n\n*",
        "В агентных системах лучше мыслить несколькими связанными цепочками:\n\n*",
    ):
        assert repeated_list not in chapter


def test_submission_readiness_uses_the_verified_release_tag() -> None:
    text = EXPECTED.read_text(encoding="utf-8")

    assert text.count("git checkout ru-manuscript-editorial-2026-07-22") == 2
    assert "git checkout ru-manuscript-editorial-2026-07\n" not in text


def test_final_book_pass_repairs_labels_headings_and_named_source_traceability() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    instruction = text.split(
        "**Пример инструкции для агента разбора обращений.**", 1
    )[1].split("```", 2)[0]
    chapter_one = revision_tool.extract_chapter(text, 1)

    assert "**Тип фрагмента:** текстовая инструкция." in instruction
    assert "**Тип фрагмента:** вывод программы." not in instruction
    assert "### Конфигурация управления агентной платформой (YAML)" in text
    assert "### Конфигурация платформенных настроек по умолчанию (YAML)" in text
    assert "Конфигурация (YAML): управления для агентной платформы" not in text
    assert "Конфигурация (YAML): платформенных настроек по умолчанию" not in text
    assert "(см. источник **S015**)" in chapter_one
    assert "**S015.** Дмитрий Викулин, «Архитектура надежных AI-агентов»." in chapter_one


def test_final_book_pass_removes_editorial_meta_language() -> None:
    text = EXPECTED.read_text(encoding="utf-8")

    for residue in (
        "главная задача этой главы. Она должна",
        "глава должна явно отличаться",
        "редакционная конкретизация",
        "текущей редакционной сборки",
        "Устойчивые утверждения:",
    ):
        assert residue not in text

    assert "авторская рабочая шкала" in text
    assert "первоисточники этого издания" in text


def test_final_book_pass_reworks_chapter_one_as_narrative_entry_point() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    chapter_one = revision_tool.extract_chapter(text, 1)
    words = len(re.findall(r"[A-Za-zА-Яа-яЁё0-9_]+", chapter_one))
    bullets = len(re.findall(r"(?m)^\s*[*-]\s+", chapter_one))

    assert 1250 <= words <= 1400
    assert bullets <= 36
    assert "Агент поддержки, который дважды создал одну заявку" in chapter_one
    assert "**Что эксплуатационная команда должна видеть всегда.**" in chapter_one
    assert "### Что команды чаще всего делают неправильно на старте" in chapter_one


def test_final_book_pass_normalizes_recurring_teaching_elements() -> None:
    text = EXPECTED.read_text(encoding="utf-8")

    assert text.count("**Практический шаг.**") == 28
    for residue in (
        "**Практическая проверка.**",
        "**Проверка на своей системе.**",
        "**Финальный рывок практики.**",
        "Ниже очень практичный",
    ):
        assert residue not in text

    assert text.count("**Быстрый тест зрелости.**") == 12
    assert not re.search(
        r"^#{3,4} Быстрый тест зрелости", text, re.MULTILINE
    )


def test_prose_quality_and_quickstart_are_editorially_consistent() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    introduction = text.split("# Часть I.", 1)[0]

    assert "git checkout ru-manuscript-editorial-2026-07-22" in introduction
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


def test_extract_chapter_stops_before_part_level_material() -> None:
    text = (
        "# Часть 1. Основа\n\n"
        "## Глава 1\\. Первая\n\nТекст главы.\n\n"
        "## Выводы части 1\n\nНе часть главы.\n\n"
        "## Лабораторная работа 1\n\nТоже не часть главы.\n\n"
        "# Часть 2. Продолжение\n\n"
        "## Глава 2\\. Вторая\n\nСледующая глава.\n"
    )

    chapter = revision_tool.extract_chapter(text, 1)

    assert "Текст главы" in chapter
    assert "Выводы части" not in chapter
    assert "Лабораторная работа" not in chapter
    assert "Следующая глава" not in chapter


def test_editorial_readiness_repairs_language_and_meta_residue() -> None:
    text = EXPECTED.read_text(encoding="utf-8")

    for residue in (
        "* контекста арендатора и субъект;",
        "parentspan_id",
        "заверение отвечает на findings",
        "trustworthiness considerations",
        "provenance/revision",
        "token passthrough",
        "resource audience",
        "Для печатной рукописи",
        "В рукописи читателю",
        "в печатной главе",
        "Из этого для книги",
        "Архитектурный вывод для книги",
        "Для книги важ",
    ):
        assert residue not in text


def test_list_heavy_chapters_have_no_redundant_long_runs() -> None:
    text = EXPECTED.read_text(encoding="utf-8")

    def longest_run(block: str) -> int:
        longest = current = 0
        inside_fence = False
        for line in block.splitlines():
            if line.startswith("```"):
                inside_fence = not inside_fence
                current = 0
            elif not inside_fence and re.match(r"^\s*(?:[*+-]|\d+\.)\s+", line):
                current += 1
                longest = max(longest, current)
            else:
                current = 0
        return longest

    for number in (19, 22, 24, 25):
        assert longest_run(revision_tool.extract_chapter(text, number)) <= 14, number

    assert text.count("проверить текущее состояние во внешней системе") == 1
    assert text.count("фоновые задачи или маршруты забыли выключить") == 1


def test_targeted_short_chapters_have_worked_decision_cases() -> None:
    text = EXPECTED.read_text(encoding="utf-8")

    expected = {
        9: "### Разбор решения: почему запись попала в контекст",
        18: "### Разбор исключения: локальная среда исполнения против стандартного пути",
        25: "### Разбор вывода из эксплуатации: как доказать закрытие старого пути",
    }
    for number, heading in expected.items():
        chapter = revision_tool.extract_chapter(text, number)
        assert heading in chapter
        assert "артефакт" in chapter.lower()
        assert re.search(r"доказательств|свидетельств", chapter, re.IGNORECASE)


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
        text.index("causal_case:\n") : text.index(
            "### Три сквозных сценария инцидентов"
        )
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
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    diagrams = data["diagrams"]

    assert data["line_basis"] == "transformed manuscript before Mermaid replacement"
    assert all("transformed_line" in diagram for diagram in diagrams)
    assert all("source_line" not in diagram for diagram in diagrams)

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

    assert len(image_paths) == 56
    assert len(set(image_paths)) == 56
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
    assert [path for path in image_paths if "/ru-editorial-diagram-" in path] == (
        EDITORIAL_DIAGRAM_PATHS
    )


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


def test_targeted_editorial_diagrams_cover_the_two_missing_decisions() -> None:
    data = json.loads(EDITORIAL_MANIFEST.read_text(encoding="utf-8"))
    diagrams = {item["number"]: item for item in data["diagrams"]}

    assert data["expected_count"] == 2
    assert set(diagrams) == {1, 2}
    assert "Обычный рабочий процесс" in diagrams[1]["mermaid"]
    assert "Многоагентная схема" in diagrams[1]["mermaid"]
    assert "Фактическое исполнение" in diagrams[2]["mermaid"]
    assert "Карантин или исправление" in diagrams[2]["mermaid"]
    assert [f"visuals/{diagrams[number]['filename']}" for number in (1, 2)] == (
        EDITORIAL_DIAGRAM_PATHS
    )


def test_targeted_editorial_diagrams_keep_text_at_least_eight_points_in_print() -> None:
    audit = json.loads(VISUAL_AUDIT.read_text(encoding="utf-8"))
    placements = audit["pdf"]["placements"]

    for relative_path in EDITORIAL_DIAGRAM_PATHS:
        asset = next(
            item
            for item in audit["assets"]
            if item["path"].endswith(relative_path.removeprefix("visuals/"))
        )
        placement = placements[asset["index"] - 1]
        svg = (VISUALS / Path(relative_path).with_suffix(".svg").name).read_text(
            encoding="utf-8"
        )
        font_pixels = [int(value) for value in re.findall(r"font:\s*(\d+)px", svg)]
        minimum_points = min(font_pixels) * placement["width_inches"] * 72 / asset["width_px"]

        assert minimum_points >= 8.0, relative_path


def test_final_technical_book_copyedit_is_applied() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    prose = re.sub(r"```.*?```", "", text, flags=re.DOTALL)

    for item in (
        "трассы можно обогащать метаданными из реестра;",
        "не сверяется с реальным покрытием телеметрии;",
        "показать, какой набор политик и какой режим подтверждения относятся к данному агенту;",
        "кто действовал;",
        "среда исполнения или модель устарели;",
        "что архивировать;",
        "устаревшая среда исполнения;",
    ):
        assert f"* {item}" in text

    assert "наблюдаемость одновременно поддерживает отладку среды исполнения" in text
    assert "активный принципал и соединитель все еще дают доступ" in text

    assert "реестр должен показывать не только саму возможность приостановки" in text
    assert "Полезный контракт телеметрии должен связывать идентичности запроса" in text
    assert "теневые конечные точки MCP" in text

    assert "\nвыпускной шлюз должен проверять не только успешный путь\n" not in text
    assert "### Выпускной шлюз должен проверять не только успешный путь" in text

    for malformed_caption in (
        "Конфигурация (YAML): извлечения и фоновых обновлений.",
        "Конфигурация (YAML): оценочных шлюзов.",
        "Конфигурация (YAML): изменений.",
        "Конфигурация (YAML): доверенных артефактов.",
        "Конфигурация (YAML): утвержденного реестра.",
        "Конфигурация (YAML): заверения.",
        "Конфигурация (YAML): вывода из эксплуатации.",
        "Конфигурация (YAML): проверочного списка запуска.",
    ):
        assert malformed_caption not in text

    prose_without_identifiers = re.sub(r"`[^`]+`", "", prose)
    for residue in (
        "значения timeout и retry по умолчанию",
        "с digest полного неизменяемого действия",
        "версия возможности и ресурса, tenant, субъект, policy bundle",
        "Минимальная запись для такого gate",
        "симуляция заведомо не похожа на production",
        'языка вроде "run completed"',
        "API helpdesk",
        "helpdesk ответил",
        "с точной идентичностью выпуска: digest",
        "дольше одного run",
        "есть ли timeout",
        "Синхронный post-run hook",
    ):
        assert residue not in prose_without_identifiers

    lab_8 = text.split("### Лабораторная работа 8", 1)[1].split(
        "## Итоговый проект", 1
    )[0]
    assert len(re.findall(r"^#### Шаг \d+\.", lab_8, re.MULTILINE)) >= 4
    assert lab_8.count("**Наблюдение.**") >= 2


def test_multi_agent_review_remediations_are_reflected_in_practice() -> None:
    text = join_shell_continuations(EXPECTED.read_text(encoding="utf-8"))
    lab_2 = text.split("### Лабораторная работа 2", 1)[1].split(
        "# Часть III", 1
    )[0]
    lab_4 = text.split("### Лабораторная работа 4", 1)[1].split(
        "# Часть V", 1
    )[0]
    lab_8 = text.split("### Лабораторная работа 8", 1)[1].split(
        "## Итоговый проект", 1
    )[0]

    assert "--approval-store artifacts/lab-02/approval-state.json" in lab_2
    assert "--resolved-by manager-lab-02" in lab_2
    assert "проверка выполняется только в памяти процесса" not in lab_2
    for field in (
        "principal_id",
        "policy_version",
        "capability_version",
        "expires_at",
        "nonce",
    ):
        assert f"`{field}`" in lab_2

    assert "--simulate-failure post_dispatch_timeout" in lab_4
    assert "--intent-id intent-lab-04-ticket" in lab_4
    assert "blocked_on_reconciliation" in lab_4
    assert "effect_reconciliation_required" in lab_4

    assert "from agent_runtime_ref.regression import" in text
    assert 'decision="INCONCLUSIVE"' in text
    assert "critical_failures" in text

    for lab_number in range(1, 8):
        assert f"--required-artifact-id lab-{lab_number:02d}" in lab_8
    assert "manifest_integrity_verified=true" in lab_8
    assert "trusted_attestation_verified=false" in lab_8

    assert (
        "ненулевой оценке по каждому из двух критериев-блокеров" in text
    )
    assert "нуле по любому из двух критериев-блокеров" not in text


def test_capability_discovery_is_a_governed_runtime_operation() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    chapter = revision_tool.extract_chapter(text, 11)

    assert "#### Обнаружение возможности не выдает полномочие" in chapter
    for field in (
        "capability_search_query",
        "registry_scope",
        "ranked_candidates",
        "selected_resource",
        "policy_decision_id",
        "approval_state",
    ):
        assert f"`{field}`" in chapter

    assert "не устанавливает и не подключает найденный ресурс" in chapter
    assert "обнаружение → выбор → подключение → исполнение" in chapter
    assert "**S105.** GitHub Changelog, Agent finder for GitHub Copilot." in chapter


def test_shared_ai_gateway_contract_is_reader_sized_and_traceable() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    chapter_thirteen = revision_tool.extract_chapter(text, 13)
    chapter_eighteen = revision_tool.extract_chapter(text, 18)

    assert "#### Решение общего шлюза ИИ" in chapter_thirteen
    for field in (
        "gateway_id",
        "gateway_policy_version",
        "client_user_agent",
        "provider_name",
        "model_name",
        "retry_count",
        "fallback_reason",
        "dlp_result",
        "pii_redaction_policy_id",
        "cache_policy",
        "rate_limit_decision",
        "token_input_count",
        "token_output_count",
        "cost_attribution_ref",
    ):
        assert f"`{field}`" in chapter_thirteen

    assert "### Общий шлюз ИИ как контур управления" in chapter_eighteen
    assert "техническим посредником для учета затрат" in chapter_eighteen
    assert "единый путь риска и стоимости" in chapter_eighteen
    for source_id in ("S106", "S107", "S108"):
        assert f"**{source_id}.**" in chapter_eighteen

    assert "Commercial control-plane convergence" not in text
    assert "shared AI gateway" not in text
    assert "billing proxy" not in text
    assert "control-plane" not in chapter_thirteen + chapter_eighteen


def test_gateway_discovery_sync_has_practice_sources_and_density_guards() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    lab_five = text.split("### Лабораторная работа 5", 1)[1].split(
        "# Часть VI", 1
    )[0]
    appendix = text.split("## Приложение 4\\.", 1)[1].split(
        "## Приложение 5\\.", 1
    )[0]

    assert "artifacts/lab-05/gateway-decision.yaml" in lab_five
    assert "отсутствующий результат DLP" in lab_five
    for source_id, url in (
        (
            "S105",
            "https://github.blog/changelog/2026-06-17-agent-finder-for-github-copilot-now-available/",
        ),
        (
            "S106",
            "https://developers.cloudflare.com/ai-gateway/integrations/coding-agents/",
        ),
        (
            "S107",
            "https://aws.amazon.com/blogs/machine-learning/agentops-operationalize-agentic-ai-at-scale-with-amazon-bedrock-agentcore/",
        ),
        (
            "S108",
            "https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/monitoring--observability-in-microsoft-foundry-part-2-configuration-and-operatio/4532674",
        ),
    ):
        assert f"**{source_id}.**" in appendix
        assert url in appendix

    chapter_eleven_words = len(
        re.findall(
            r"[A-Za-zА-Яа-яЁё0-9]+",
            revision_tool.extract_chapter(text, 11),
        )
    )
    assert chapter_eleven_words < 4600


def test_every_manuscript_table_has_a_numbered_caption() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    captions = re.findall(r"^Таблица (\d+)\. .+$", text, re.MULTILINE)
    tables = re.findall(r"^\|.+\|\n\|\s*:?-+", text, re.MULTILINE)

    assert captions == [str(number) for number in range(1, 11)]
    assert len(tables) == 10
    for number in range(1, 11):
        assert re.search(
            rf"^Таблица {number}\. .+\n\n\|.+\|$",
            text,
            re.MULTILINE,
        )


def test_final_copyedit_repairs_heading_hierarchy_and_agreement() -> None:
    text = EXPECTED.read_text(encoding="utf-8")

    for heading in (
        "#### Сдерживание сильнее бесконечного надзора",
        "#### MCP-шлюз, приватная достижимость и браузер как поверхность действия",
        "#### Приватность рассуждений и поисковые фрагменты трассы",
        "### Стоимость и песочница тоже входят в SLO",
        "#### Целостность симуляции развертывания и самой оценки",
        "#### Подтверждение как прерываемый путь выполнения",
        "### Поддерживаемый стандартный путь должен быть путем по умолчанию",
    ):
        assert heading in text

    for dangling_line in (
        "сдерживание сильнее бесконечного надзора",
        "MCP-шлюз, приватная достижимость и браузер как поверхность действия",
        "приватность рассуждений и поисковые фрагменты трассы",
        "стоимость и песочница тоже входят в SLO",
        "симуляция развертывания и целостность самой оценки",
    ):
        assert not re.search(rf"^(?!#){re.escape(dangling_line)}$", text, re.MULTILINE)

    for residue in (
        "краткосрочная память можно",
        "среда исполнения мог ее продолжать",
    ):
        assert residue not in text


def test_final_language_pass_translates_prose_and_marks_machine_literals() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    prose = re.sub(r"```.*?```", "", text, flags=re.DOTALL)

    for residue in (
        "webhooks и события",
        "был ли апдейт подтвержден",
        "имеют provenance и revision",
        "попадать в eval schema",
        "инференс модели",
        "pointer и preview",
        "verifier стал",
        "для cost SLO",
        "управляемого change management",
        "automated red teaming",
        "избегает oversight",
        "для capability sessions",
        "кастомных обходов",
        "хуки политик",
        "в кастомную реализацию",
        "локальные ретраи",
        "resumable работы",
        "сложный planner",
        "предложение ToolRequest",
        "решение allow",
        "Решения deny",
        "нативные возможности песочницы доступны: filesystem",
        "требовать backoff",
        "* success считают",
        "* latency видят",
        "автоматический verdict",
        "правила privacy filtering",
        "оценки (evals)",
        "* low-risk:",
        "* medium-risk:",
        "* high-risk:",
        "снимок экрана, diff",
    ):
        assert residue not in prose

    for required in (
        "вебхуки (HTTP-уведомления)",
        "было ли обновление подтверждено",
        "постоянные записи имеют происхождение и ревизию",
        "какие ветки должны явно попадать в схему оценки",
        "вызов модели",
        "проверяющий стал шумным",
        "Практический минимум для SLO стоимости",
        "автоматизированное соревновательное тестирование",
        "поведение истечения срока и повторной инициализации для сессий возможностей",
        "`verification_result`: `pass`, `fail`, `warning` или `blocked`",
        "`queued` / `in_progress` / `completed` / `failed` / `canceled`",
        "предложение `ToolRequest`",
        "решение `allow`",
        "Решения `deny`",
        "файловая система (`filesystem`)",
        "задержку между повторами (`backoff`)",
        "* `success` считают",
        "* `latency` видят",
        "автоматический вердикт",
        "правила фильтрации конфиденциальных данных",
        "оценки (`evals`)",
        "* `low-risk` (низкий риск):",
        "* `medium-risk` (средний риск):",
        "* `high-risk` (высокий риск):",
        "сравнение изменений (`diff`)",
    ):
        assert required in text


def test_final_rhythm_pass_uses_deliberate_recurring_callouts() -> None:
    text = EXPECTED.read_text(encoding="utf-8")

    assert "Команде не стоит" not in text
    assert text.count("**Ложный признак зрелости.**") == 16
    assert len(re.findall(r"\bне просто\b", text, re.IGNORECASE)) < 40


def test_world_class_copyedit_repairs_structure_and_line_measure() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    lines = text.splitlines()
    stacked_headings: list[tuple[int, str, str]] = []
    headings_before_code: list[tuple[int, str]] = []
    long_code_lines: list[tuple[int, int]] = []
    previous_heading: tuple[int, str] | None = None
    inside_fence = False

    for index, line in enumerate(lines, start=1):
        if line.startswith("```"):
            if not inside_fence and previous_heading is not None:
                headings_before_code.append(previous_heading)
            inside_fence = not inside_fence
            previous_heading = None
            continue
        if inside_fence:
            if len(line) > 100:
                long_code_lines.append((index, len(line)))
            continue
        if re.match(r"^#{1,6} ", line):
            if previous_heading is not None:
                stacked_headings.append((index, previous_heading[1], line))
            previous_heading = (index, line)
        elif line.strip():
            previous_heading = None

    assert stacked_headings == []
    assert headings_before_code == []
    assert long_code_lines == []
    assert not re.search(r"^#{1,6} .*`", text, re.MULTILINE)


def test_world_class_copyedit_repairs_known_agreement_errors() -> None:
    text = EXPECTED.read_text(encoding="utf-8")

    for residue in (
        "весь среда исполнения",
        "среда исполнения решил повторить",
        "не был ли подсказка перегружен",
        "богаче должен быть проектирование оценки",
    ):
        assert residue not in text

    for corrected in (
        "всю среду исполнения",
        "среда исполнения решила",
        "не была ли подсказка перегружена",
        "богаче должно быть проектирование оценки",
    ):
        assert corrected in text


def test_final_reader_copyedit_repairs_language_and_assembly_residue() -> None:
    text = EXPECTED.read_text(encoding="utf-8")

    for residue in (
        "передача управления должна передавать",
        "А когда управление выпуском становится по-настоящему значимым, она должна",
        "должна проходить не только проверка качества данных",
        "проектирование проверяющего здесь тоже важен",
        "какие набор политик",
        "какие происхождение, целостность и состояние отзыва",
        "Но даже этого недостаточно.\n\nНо остаются",
        "Она должна показать вывод из эксплуатации",
        "Главный артефакт этой главы — запись реестра",
        "У нее один центральный артефакт",
        "Главный артефакт этой главы — модель состояний ADLC",
        "Главный артефакт этой главы — запись о находке",
    ):
        assert residue not in text

    for corrected in (
        "Здесь важен не сам вызов, а контракт передачи",
        "Когда набор становится частью управления выпуском",
        "для нее обязательны и проверка качества данных, и проверка модели угроз",
        "проектирование проверяющего здесь тоже важно",
        "какой набор политик и какой режим подтверждения",
        "что артефакт должен доказать о происхождении, целостности и возможности отзыва",
        "Но даже этого недостаточно: остаются",
        "Вывод из эксплуатации завершает жизненный цикл",
    ):
        assert corrected in text


def test_final_reader_copyedit_uses_russian_first_terminology() -> None:
    text = EXPECTED.read_text(encoding="utf-8")

    for residue in (
        r"\bрелиз[а-яё-]*\b",
        r"\bпаттерн[а-яё-]*\b",
        r"\bкейс[а-яё-]*\b",
        r"\bворкер[а-яё-]*\b",
        r"\bпостмортем[а-яё-]*\b",
        r"\boracle\b",
        r"\bбенчмарк[а-яё-]*\b",
        r"\bкомплаенс[а-яё-]*\b",
        r"\bkeyed HMAC\b",
    ):
        assert not re.search(residue, text, re.IGNORECASE)

    for preferred in (
        "координационный подход",
        "Короткий пример:",
        "рабочих агентов",
        "разбора инцидента",
        "детерминированного эталона",
        "контрольный набор",
        "HMAC с управляемым секретным ключом",
        "соблюдению требований",
    ):
        assert preferred in text

    for broken_agreement in (
        "схема координатора",
        "Подход координатора",
        "полезный схема",
        "схема координатора должен",
        "схема координатора уместен",
        "Таксономия подходов рабочих процессов",
        "более маленький подход оркестрации",
        "Антизоопарк-подход",
        "какие подходы создают расследование",
    ):
        assert broken_agreement not in text

    for fluent_phrase in (
        "Классификация подходов к рабочим процессам у Anthropic",
        "более простой способ оркестрации",
        "Ограничение платформенного зоопарка начинается с правильных границ",
        "какие сигналы запускают расследование",
        "Еще один полезный подход из практики Cloudflare",
    ):
        assert fluent_phrase in text


def test_final_reader_copyedit_makes_definitions_scannable_and_dates_snapshots() -> None:
    text = EXPECTED.read_text(encoding="utf-8")

    for state in (
        "success",
        "waiting_for_approval",
        "permission_denied",
        "validation_failure",
        "retryable_failure",
        "side_effect_unknown",
        "partial_side_effect",
    ):
        assert f"* `{state}`:" in text

    for outcome in ("pass", "blocked", "fail", "inconclusive"):
        assert f"* `{outcome}`:" in text

    for level in range(5):
        assert f"* **Уровень {level}:**" in text

    assert "* Перед исполнением шлюз повторно проверяет" in text
    assert text.count("**Срез практики. Июль 2026 года.**") == 2
    assert text.count("**Срез практики. Июнь 2026 года.**") == 1


def test_approval_examples_bind_one_high_risk_create_ticket_action() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    listing = text.split("**Листинг 8. Запрос на подтверждение.**", 1)[1].split(
        "### Поток подтверждения как состояние системы",
        1,
    )[0]

    assert "capability: ticket_write" not in listing
    assert "executed_capability: ticket_write" not in listing
    assert "requested_action: create_incident_ticket" not in listing
    assert "capability: create_ticket" in listing
    assert "executed_capability: create_ticket" in listing
    assert "requested_action: create_ticket" in listing
    action_digests = re.findall(r"action_digest: ([0-9a-f]{64})", listing)
    assert len(action_digests) == 3
    assert len(set(action_digests)) == 1
    for field in (
        "policy_version",
        "capability_version",
        "authorization_mode",
        "expires_at",
        "nonce",
    ):
        assert f"{field}:" in listing

    assert not re.search(r"create_ticket:\n\s+risk: medium", text)


def test_chapter_sources_cover_material_claims_and_primary_case_record() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    chapter_three = revision_tool.extract_chapter(text, 3)
    chapter_twenty_six = revision_tool.extract_chapter(text, 26)
    appendix = text.split("## Приложение 4\\.", 1)[1].split(
        "## Приложение 5\\.",
        1,
    )[0]

    for source_id in ("S009", "S016", "S021", "S036", "S042"):
        assert f"**{source_id}.**" in chapter_three
    for source_id in ("S044", "S050", "S092", "S093", "S094"):
        assert f"**{source_id}.**" in chapter_twenty_six

    assert "см. источник **S109**" in text
    assert "**S109.**" in appendix
    assert (
        "https://decisions.civilresolutionbc.ca/crt/crtd/en/item/525448/index.do"
        in appendix
    )


def test_technical_book_polish_closes_production_and_local_source_gaps() -> None:
    text = EXPECTED.read_text(encoding="utf-8")

    for residue in (
        "Печатная рамка выбора",
        "при экспорте в PDF, печать или поисковый индекс",
        "Печатная схема выбора, если ее нужно вынести на одну страницу",
        "ревью выпуска",
    ):
        assert residue not in text

    for number in range(1, 29):
        body, sources = revision_tool.extract_chapter(text, number).split(
            "### Источники главы",
            1,
        )
        inline_ids = set(re.findall(r"\bS\d{3}\b", body))
        local_ids = set(
            re.findall(r"^\*\*(S\d{3})\.\*\*", sources, re.MULTILINE)
        )
        assert inline_ids <= local_ids, (
            number,
            sorted(inline_ids - local_ids),
        )

    named_source_sets = {
        2: {"S016", "S020", "S021", "S042"},
        4: {"S021", "S038", "S071"},
        5: {"S016", "S058", "S059", "S068"},
        6: {"S047"},
        7: {"S037", "S038"},
        8: {"S045"},
        10: {"S021"},
        11: {"S023", "S024", "S051", "S073"},
        12: {"S021", "S049"},
        14: {"S020"},
        15: {"S020", "S037", "S063"},
        16: {"S091"},
        19: {"S011", "S087"},
        20: {"S010", "S011", "S012", "S016", "S021", "S074", "S075"},
        21: {"S017", "S075"},
        22: {"S060", "S087"},
        23: {"S076", "S079", "S085", "S086", "S089", "S090"},
        24: {"S074", "S080"},
        26: {"S016", "S023", "S024", "S033", "S044", "S045", "S046", "S048", "S049", "S057"},
        27: {"S043"},
        28: {"S016", "S040", "S109"},
    }
    for number, expected_ids in named_source_sets.items():
        sources = revision_tool.extract_chapter(text, number).split(
            "### Источники главы",
            1,
        )[1]
        local_ids = set(
            re.findall(r"^\*\*(S\d{3})\.\*\*", sources, re.MULTILINE)
        )
        assert expected_ids <= local_ids, (number, sorted(expected_ids - local_ids))


def test_source_appendix_separates_cited_sources_from_further_reading() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    before_appendix, appendix_tail = text.split("## Приложение 4\\.", 1)
    appendix = appendix_tail.split("## Приложение 5\\.", 1)[0]
    cited, further = appendix.split("### Дополнительное чтение", 1)
    cited = cited.split("### Цитируемые источники", 1)[1]

    cited_ids = set(re.findall(r"^\*\*(S\d{3})\.\*\*", cited, re.MULTILINE))
    further_ids = set(re.findall(r"^\*\*(S\d{3})\.\*\*", further, re.MULTILINE))
    used_ids = set(re.findall(r"\bS\d{3}\b", before_appendix))

    assert cited_ids == used_ids
    assert cited_ids.isdisjoint(further_ids)
    assert cited_ids | further_ids == {f"S{number:03d}" for number in range(1, 110)}


def test_chapters_17_to_19_have_non_overlapping_editorial_ownership() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    chapter_seventeen = revision_tool.extract_chapter(text, 17)
    chapter_eighteen = revision_tool.extract_chapter(text, 18)
    chapter_nineteen = revision_tool.extract_chapter(text, 19)

    for residue in (
        "Платформа должна давать поддерживаемые стандартные пути",
        "Инвентарь платформы тоже должен иметь владельца",
        "Утвержденный реестр полезен не меньше",
        "\nregistry:\n",
    ):
        assert residue not in chapter_seventeen

    for residue in (
        "Реестр утвержденных шаблонов нужен",
        "Реестр и политика вывода из эксплуатации должны жить вместе",
        "Дрейф инвентаря сам по себе полезно считать",
    ):
        assert residue not in chapter_eighteen

    for required in (
        "Инвентарь и реестр — не одно и то же",
        "Что должно быть в минимальной записи агента",
        "отчет расхождений с фактической активностью",
    ):
        assert required in chapter_nineteen

    assert "Глава 18 покажет, как владельцы получают поддерживаемый путь" in chapter_seventeen
    assert "Глава 19 превратит наблюдаемые отклонения в сверяемую запись" in chapter_eighteen


def test_developmental_polish_uses_direct_openings_and_one_assurance_definition() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    chapter_fifteen = revision_tool.extract_chapter(text, 15)
    chapter_twenty_three = revision_tool.extract_chapter(text, 23)
    chapter_twenty_four = revision_tool.extract_chapter(text, 24)

    assert "Как читать эту главу." not in chapter_fifteen
    assert "Ориентир главы" not in chapter_fifteen
    assert "Глава отделяет наблюдаемый опасный результат" not in chapter_twenty_three
    assert chapter_twenty_three.index("### Утро, когда полезная цель стала опасной") < 700
    assert chapter_twenty_three.count("В 09:07") == 1

    assert "Я бы определял контур заверения" not in chapter_twenty_four
    assert chapter_twenty_four.count("постоянный рабочий контур") == 1
    assert chapter_twenty_four.count("находка должна получить владельца") == 1


def test_reader_rhythm_and_fast_moving_callouts_are_consistent() -> None:
    text = EXPECTED.read_text(encoding="utf-8")

    assert "я бы рекомендовал" not in text.casefold()
    assert "я бы определял" not in text.casefold()
    repeated_request = (
        "\\> Я уже третий день жду активации доступа. Проверьте статус и создайте "
        "срочную заявку, если заявка застряла."
    )
    assert text.count(repeated_request) == 2

    snapshots = re.findall(
        r"^> \*\*Срез практики\. (?:Июнь|Июль) 2026 года\.\*\* .+$",
        text,
        re.MULTILINE,
    )
    assert len(snapshots) == 3
    assert text.count("> **Граница переносимости.**") == 3


def test_glossary_and_publisher_packets_cover_new_reference_terms() -> None:
    text = EXPECTED.read_text(encoding="utf-8")
    glossary = text.split("## Приложение 1\\. Глоссарий", 1)[1].split(
        "## Приложение 2\\.",
        1,
    )[0]
    required_terms = (
        "Контракт проверяющего",
        "Манифест доказательств",
        "Общий шлюз ИИ",
        "Контрольная волна",
        "Сессия возможности",
        "Сверка внешнего эффекта",
    )
    for term in required_terms:
        assert f"### {term}" in glossary

    index_packet = INDEX_TERMS.read_text(encoding="utf-8")
    for term in required_terms:
        assert term in index_packet
    assert "См. также" in index_packet
    assert "Предпочтительный термин" in index_packet

    learning_map = LEARNING_OUTCOME_MAP.read_text(encoding="utf-8")
    assert len(re.findall(r"^## Глава \d+\.", learning_map, re.MULTILINE)) == 28
    assert learning_map.count("**Заявленные результаты:**") == 28
    assert learning_map.count("**Наблюдаемая точка применения:**") == 28

    review_packet = HUMAN_REVIEW_PACKET.read_text(encoding="utf-8")
    for marker in (
        "Статус человеческой проверки: не выполнена",
        "Технический рецензент 1",
        "Технический рецензент 2",
        "Независимый проход лабораторных работ",
        "Авторский блок",
        "Литературная и издательская корректура",
        "Решение по замечанию",
    ):
        assert marker in review_packet


def test_editorial_packet_builder_is_reproducible(tmp_path: Path) -> None:
    index_terms = tmp_path / "index.md"
    learning_map = tmp_path / "learning.md"
    review_packet = tmp_path / "review.md"

    subprocess.run(
        [
            sys.executable,
            str(EDITORIAL_PACKET_BUILDER),
            "--manuscript",
            str(EXPECTED),
            "--index-output",
            str(index_terms),
            "--learning-output",
            str(learning_map),
            "--review-output",
            str(review_packet),
        ],
        cwd=ROOT,
        check=True,
    )

    assert index_terms.read_bytes() == INDEX_TERMS.read_bytes()
    assert learning_map.read_bytes() == LEARNING_OUTCOME_MAP.read_bytes()
    assert review_packet.read_bytes() == HUMAN_REVIEW_PACKET.read_bytes()
