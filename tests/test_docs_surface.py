import json
import re
import shutil
import subprocess
import textwrap
from collections.abc import Sequence
from pathlib import Path

import pytest
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


_RUSSIAN_EXPECTED_ALTERNATIVES = {
    "Support triage": ("Разбор обращений поддержки", "Триаж обращений поддержки"),
    "Internal knowledge assistant": ("Внутренний ассистент знаний",),
    "Incident coordination": ("Координация инцидентов",),
    "A2A требует governance": ("A2A требует управления",),
    "Execution case-spine note": ("Заметка о сквозных сценариях выполнения",),
    "Sandbox/MCP case-spine note": (
        "Заметка о сквозных сценариях песочницы и MCP",
    ),
    "Architecture case-spine note": ("Заметка о сквозных сценариях архитектуры",),
    "Trust-boundary case-spine note": ("Заметка о сквозных сценариях границ доверия",),
    "Gateway case-spine note": ("Заметка о сквозных сценариях шлюза",),
    "Memory-risk case-spine note": ("Заметка о сквозных сценариях риска памяти",),
    "Memory case-spine note": ("Заметка о сквозных сценариях памяти",),
    "Retrieval case-spine note": ("Заметка о сквозных сценариях поиска",),
    "Eval case-spine note": ("Заметка о сквозных сценариях оценивания",),
    "Reliability case-spine note": ("Заметка о сквозных сценариях надежности",),
    "Trace case-spine note": ("Заметка о сквозных сценариях трассировки",),
    "Canonical trace cases": ("Канонические сценарии трассировки",),
    "trace emphases": ("акцентов трассировки",),
    "approval events": ("события подтверждений",),
    "retrieval spans": ("спанов поиска", "спаны поиска"),
    "escalation timeline": (
        "таймлайн эскалации",
        "линии времени эскалации",
        "линию времени эскалации",
    ),
    "SLO case-spine note": ("Заметка о сквозных сценариях целей уровня сервиса",),
    "Canonical eval cases": ("Канонические сценарии оценок",),
    "Canonical rollout cases": ("Канонические сценарии раскатки",),
    "Canonical lifecycle cases": ("Канонические сценарии жизненного цикла",),
    "Canonical roadmap cases": ("Канонические сценарии дорожной карты",),
    "Canonical language cases": ("Канонические сценарии выбора языка",),
    "Canonical policy cases": ("Канонические сценарии политик",),
    "Language choice": ("Выбор языка",),
    "canonical cases": (
        "канонических сценария",
        "канонических сценариях",
        "каноническим сценариям",
    ),
    "read tools": ("инструменты чтения",),
    "write tools": ("инструменты записи",),
    "approval handoff": ("передачу на подтверждение",),
    "idempotency keys": ("ключи идемпотентности", "ключей идемпотентности"),
    "retrieval tools": ("инструменты поиска",),
    "corpus filters": ("фильтры корпуса",),
    "reference architecture": ("эталонная архитектура",),
    "ingress identity": ("идентичность входящего запроса",),
    "control plane": ("контур управления",),
    "approval gate": ("шлюз подтверждения",),
    "retrieval scope": ("область поиска",),
    "responder-role checks": ("проверки роли реагирующего",),
    "timeout paths": ("ветки тайм-аута",),
    "sandbox limits": ("ограничений песочницы",),
    "approval-aware MCP tools": ("MCP-инструментов с учетом подтверждения",),
    "reconciliation path": ("пути сверки",),
    "read-only MCP resources": ("MCP-ресурсов только для чтения",),
    "corpus-scoped network access": ("сетевого доступа в пределах корпуса",),
    "source validation": ("проверки источников",),
    "responder-role enforcement": ("проверки роли реагирующего",),
    "audit trail": ("аудиторский след",),
    "delegated authority": ("делегированные полномочия", "делегированных полномочий"),
    "agent identity": ("идентичность агента",),
    "A2A handoff trust contract": ("контракт доверия для передачи управления A2A",),
    "delegation chain": ("цепочка делегирования",),
    "allowed collaboration graph": ("граф разрешенного взаимодействия",),
    "inter-agent authorization": ("межагентная авторизация",),
    "policy inheritance": ("наследование политик",),
    "non-repudiation": ("неотказуемость",),
    "failure attribution": ("атрибуция сбоев",),
    "duplicate-ticket detection": ("обнаружения дублей тикетов",),
    "reconciliation": ("сверки",),
    "retrieval fan-out": ("веерного поиска",),
    "freshness backoff": ("паузы при потере свежести", "пауз при потере свежести"),
    "stale memory writes": ("устаревшие записи памяти",),
    "notification throttling": ("ограничения частоты уведомлений",),
    "tool spans": ("спаны инструментов",),
    "approval status": ("статус подтверждения",),
    "source identifiers": ("идентификаторами источников",),
    "freshness markers": ("отметками свежести",),
    "memory-write events": ("событиями записи в память",),
    "incident-state events": ("событий состояния инцидента",),
    "verifier evidence": ("доказательствами проверяющего", "доказательства проверяющего"),
    "health budgets": ("бюджеты здоровья",),
    "duplicate-ticket rate": ("долю дублей тикетов",),
    "approval latency": ("задержку подтверждения",),
    "retrieval freshness": ("свежесть поиска",),
    "approval gates": ("шлюзы подтверждения",),
    "idempotency evidence": ("доказательства идемпотентности", "доказательств идемпотентности"),
    "retry behavior": ("поведение повторов",),
    "duplicate-ticket recovery": ("восстановление после дубля тикета",),
    "source-grounding success": ("успешную привязку к источникам",),
    "source attribution": ("привязку к источникам", "проверки привязки к источникам"),
    "memory provenance": ("происхождение памяти", "проверки происхождения памяти"),
    "access control": ("контроль доступа", "подтверждения контроля доступа", "контроля доступа"),
    "grounded answer quality": ("качество ответа с опорой на источники",),
    "escalation timing": ("сроки эскалации",),
    "notification side effects": ("побочные эффекты уведомлений", "побочных эффектов уведомлений"),
    "access-control denials": ("отказы контроля доступа",),
    "responder handoff latency": ("задержку передачи реагирующему",),
    "handoff quality": ("качество передачи управления",),
    "post-incident learning regressions": ("регрессии обучения после инцидента",),
    "next layer of value": ("следующий слой пользы",),
    "richer trace examples": ("более богатым примерам трасс",),
    "approval policy templates": ("шаблонам политик подтверждения",),
    "duplicate-ticket evals": ("оценкам дублей тикетов",),
    "runnable high-risk scenario": ("исполняемому высокорисковому сценарию",),
    "knowledge scenario": ("сценарию знаний",),
    "retrieval policy template": ("шаблону политики поиска",),
    "memory eval patterns": ("паттернам оценки памяти",),
    "source-grounding QA": ("проверке привязки к источникам",),
    "incident trace examples": ("примерам трасс инцидентов",),
    "escalation/notification templates": ("шаблонам эскалации и уведомлений",),
    "response ownership checks": ("проверкам владения ответом",),
    "post-incident learning assets": ("артефактам обучения после инцидента",),
    "tool gateway": ("шлюз инструментов",),
    "approval service": ("сервис подтверждений",),
    "idempotency control": ("контроль идемпотентности",),
    "tenant boundary": ("границу арендатора",),
    "notification tool boundary": ("границу инструмента уведомлений",),
    "durable-state risks": ("риски долговечного состояния",),
    "memory-write policy": ("политики записи в память",),
    "profile preference": ("профильных предпочтений",),
    "tenant isolation": ("изоляции арендаторов",),
    "retrieval-memory split": ("разделения поиска и памяти",),
    "tenant-filter enforcement": ("принудительного фильтра арендатора",),
    "notification history provenance": ("происхождения истории уведомлений",),
    "post-incident cleanup rules": ("правил очистки после инцидента",),
    "memory poisoning": ("отравления памяти", "Отравление памяти"),
    "memory poisoning review fields": ("поля разбора отравления памяти",),
    "untrusted write": ("недоверенную запись", "непроверенных сводок"),
    "delayed activation": ("отложенной активации",),
    "cross-tenant contamination": ("межарендаторного загрязнения",),
    "policy influence": ("влияния на политику",),
    "provenance check": ("проверки происхождения",),
    "quarantine and rollback": ("карантина и отката",),
    "threat-model review": ("модели угроз",),
    "read/decide/act split": ("разделение чтения, решения и действия",),
    "ticket writes": ("записи тикетов",),
    "retrieved documents": ("найденные документы",),
    "source authority": ("авторитет источника",),
    "memory writes": ("записи памяти",),
    "external notifications": ("внешние уведомления",),
    "current ticket state": ("текущее состояние тикета",),
    "freshness windows": ("окна свежести",),
    "tenant filters": ("фильтры арендатора",),
    "stale-index detection": ("обнаружение устаревшего индекса",),
    "durable lessons": ("долговечные уроки",),
    "temporary ticket state": ("временное состояние тикета",),
    "freshness": ("свежесть",),
    "tenant boundaries": ("границы арендатора",),
    "handoff summaries": ("сводки передачи управления",),
    "post-incident lessons": ("уроки после инцидента",),
    "governed writes": ("управляемые операции записи",),
    "scoped reads": ("чтение в заданной области",),
    "retrieval limits": ("ограничения поиска",),
    "escalation tools": ("инструменты эскалации",),
    "notification tools": ("инструменты уведомлений",),
    "incident state": ("состояние инцидента",),
    "duplicate tickets": ("дубли тикетов",),
    "regression cases": ("регрессионные сценарии",),
    "tool side effects": ("побочные эффекты инструментов",),
    "duplicate-ticket recovery evidence": ("доказательства восстановления после дубля тикета",),
    "memory access": ("доступ к памяти",),
    "freshness checks": ("проверки свежести", "проверок свежести"),
    "access control decisions": ("решения контроля доступа",),
    "handoff events": ("события передачи управления",),
    "post-incident learning": ("обучение после инцидента",),
    "stricter platform services": ("более строгие платформенные сервисы",),
    "retrieval experiments": ("эксперименты поиска",),
    "eval loop": ("цикл оценки",),
    "contract layer": ("контрактный слой",),
    "memory/index service": ("сервиса памяти/индекса",),
    "source provenance": ("происхождения источников", "происхождение источников"),
    "tenant-aware access": ("доступа с учетом арендатора",),
    "runtime reliability": ("надежность среды исполнения",),
    "trace ingestion pipeline": ("конвейер приема трасс",),
    "notification safety": ("безопасность уведомлений",),
    "response ownership": ("владение ответом", "владения ответом"),
    "platform control": ("платформенный контроль",),
    "Governance-aware telemetry": ("Управленческая телеметрия",),
    "telemetry": ("телеметрия", "телеметрии"),
    "governance action record": ("запись управленческого действия",),
    "readiness signals": ("сигналы готовности",),
    "duplicate-ticket eval pass": ("оценки дублей тикетов",),
    "rollback plan": ("плана отката",),
    "approval readiness": ("готовности подтверждений",),
    "retrieval freshness window": ("окна свежести поиска",),
    "source attribution review": ("проверки привязки к источникам",),
    "memory provenance review": ("проверки происхождения памяти",),
    "access control signoff": ("подтверждения контроля доступа",),
    "escalation drill": ("тренировки эскалации",),
    "notification side effects review": ("проверки побочных эффектов уведомлений",),
    "response ownership readiness": ("готовности владения ответом",),
    "post-incident learning gate": ("шлюза обучения после инцидента",),
    "Routine case-spine note": (
        "Эти инструкции выглядят как пример для разбора обращений поддержки",
    ),
    "Manager/handoff case-spine note": (
        "Сквозные сценарии управляющего агента и передачи управления",
    ),
    "approved write routine": (
        "подтвержденную процедуру записи",
        "подтвержденная записывающая процедура",
    ),
    "retrieval routine": ("процедуру поиска",),
    "incident escalation routine": ("процедуру эскалации инцидента",),
    "notification handoff": ("передачу уведомления",),
    "owner record": ("запись владельца",),
    "ticket state": ("состояние тикета",),
    "audit story": ("цепочке аудита", "история аудита", "аудиторский рассказ"),
    "read-heavy capabilities": ("преимущественно читающие возможности",),
    "accountable roles": ("подотчетными ролями",),
    "escalation": ("эскалация",),
    "Шлюз раскатки (rollout gate)": ("Шлюз раскатки",),
    "Артефакты жизненного цикла (lifecycle artifacts)": ("Артефакты жизненного цикла",),
    "Дорожная карта (roadmap)": ("Дорожная карта",),
    "artifact chains": ("цепочки артефактов",),
    "change record": ("запись изменения",),
    "approved artifact bundle": ("утвержденный пакет артефактов",),
    "approval record": ("запись подтверждения",),
    "eval dataset": ("набор оценок",),
    "rollout gate": ("шлюз раскатки",),
    "retirement plan": ("план вывода из эксплуатации",),
    "duplicate-ticket guard": ("защиты от дубля тикета",),
    "retrieval policy": ("политику поиска", "политики поиска"),
    "memory policy": ("политику памяти",),
    "access-control review": ("проверку контроля доступа",),
    "knowledge-base replacement plan": ("план замены базы знаний",),
    "escalation policy": ("политику эскалации",),
    "notification capability": ("возможность уведомлений",),
    "response ownership map": ("карту владения ответом",),
    "handoff artifact": ("артефакт передачи управления",),
    "post-incident learning retirement or replacement plan": (
        "план вывода из эксплуатации или замены обучения после инцидента",
    ),
    "Canonical case alignment": ("Канонические сценарии: выравнивание",),
    "Пакет политик (policy bundle)": ("Пакет политик",),
    "write-capability approval policy": ("политики подтверждения для записывающей возможности",),
    "write capability": ("записывающую возможность", "записывающей возможности"),
    "duplicate-ticket recovery controls": ("средств восстановления после дубля тикета",),
    "memory write rules": ("правил записи в память",),
    "knowledge provenance": ("происхождения знаний", "происхождение знаний"),
    "escalation rules": ("правил эскалации",),
    "правил эскалации (escalation rules)": ("правил эскалации",),
    "post-incident learning gates": ("шлюзов обучения после инцидента",),
    "явную связь с [verifier evidence](../../appendix/eval-schema.md)": (
        "явную связь с [доказательствами проверяющего](../../appendix/eval-schema.md)",
    ),
    "заново собирать [verifier evidence](../../appendix/eval-schema.md)": (
        "заново собирать [доказательства проверяющего](../../appendix/eval-schema.md)",
    ),
    "[verifier contracts](../../appendix/eval-schema.md)": (
        "[рубрика оценки и правила связывания доказательной базы](../../appendix/eval-schema.md)",
    ),
    "[verifier contract](../../appendix/eval-schema.md) не просто оценивает качество": (
        "[контракт проверяющего](../../appendix/eval-schema.md) не просто оценивает качество",
    ),
    "активного [verifier contract](../../appendix/eval-schema.md)": (
        "активный контракт проверяющего",
        "активный контракт проверяющего и версию контракта проверяющего",
        "семейством контрактов с ограничениями проверяющего",
    ),
    "и [verifier evidence](../../appendix/eval-schema.md) о том": (
        "и [доказательствами проверяющего](../../appendix/eval-schema.md) о том",
    ),
    "[governance action record](../../appendix/trace-schema.md)": (
        "[запись управленческого действия](../../appendix/trace-schema.md)",
    ),
    "[verifier evidence](../../appendix/eval-schema.md) оторван": (
        "[доказательствами проверяющего](../../appendix/eval-schema.md) оторван",
        "[доказательства проверяющего](../../appendix/eval-schema.md) оторваны",
    ),
    "reviewed orchestration patterns и [verifier evidence](../../appendix/eval-schema.md)": (
        "рассмотренные orchestration patterns и "
        "[доказательствами проверяющего](../../appendix/eval-schema.md)",
        "проверенными схемами оркестрации и "
        "[доказательствами проверяющего](../../appendix/eval-schema.md)",
    ),
    "активным orchestration pattern и [verifier evidence](../../appendix/eval-schema.md)": (
        "активным orchestration pattern и "
        "[доказательствами проверяющего](../../appendix/eval-schema.md)",
        "активной схемой оркестрации и "
        "[доказательствами проверяющего](../../appendix/eval-schema.md)",
    ),
    "artifacts и [verifier evidence](../../appendix/eval-schema.md)": (
        "артефактами жизненного цикла и "
        "[доказательствами проверяющего](../../appendix/eval-schema.md)",
        "артефактов жизненного цикла и "
        "[доказательствами проверяющего](../../appendix/eval-schema.md)",
        "пакетами артефактов, версиями контрактов, проверенными схемами "
        "оркестрации и [доказательствами проверяющего](../../appendix/eval-schema.md)",
    ),
    "акцентов трассировки (trace emphases)": ("акцентов трассировки",),
    "события подтверждений (approval events)": ("события подтверждений",),
    "спаны поиска (retrieval spans)": ("спаны поиска",),
    "таймлайн эскалации (escalation timeline)": ("линию времени эскалации", "таймлайн эскалации"),
    "Набор оценок (eval dataset)": ("Набор оценок",),
    "регрессию дублей тикетов (duplicate-ticket regression)": ("регрессию дублей тикетов",),
    "шлюзы подтверждения (approval gates)": ("шлюзы подтверждения",),
    "свежесть поиска (retrieval freshness)": ("свежесть поиска",),
    "сроки эскалации (escalation timing)": ("сроки эскалации",),
    "сигналы готовности (readiness signals)": ("сигналы готовности",),
    "окна свежести поиска (retrieval freshness window)": ("окна свежести поиска",),
    "тренировки эскалации (escalation drill)": ("тренировки эскалации",),
    "плана отката (rollback plan)": ("плана отката",),
    "цепочки артефактов (artifact chains)": ("цепочки артефактов",),
    "запись изменения (change record)": ("запись изменения",),
    "политику поиска (retrieval policy)": ("политику поиска",),
    "политики поиска (retrieval policy)": ("политики поиска",),
    "политику эскалации (escalation policy)": ("политику эскалации",),
    "следующий слой пользы (next layer of value)": ("следующий слой пользы",),
    "итераций поведения (behavior iteration)": ("итераций поведения",),
    "Триаж обращений поддержки (Support triage)": ("Триаж обращений поддержки",),
    "шлюз инструментов (tool gateway)": ("шлюз инструментов",),
    "post-incident rollout judgment": ("решение о раскатке после инцидента", "rollout judgment"),
    "решение о поэтапном выпуске после инцидента": (
        "решение о раскатке после инцидента",
        "rollout judgment",
    ),
    "unified agent threat evidence model": ("единую доказательную модель угроз агенту",),
    "Prompt injection": ("Внедрение инструкций",),
    "Indirect injection": ("Косвенное внедрение инструкций",),
    "RAG poisoning": ("Отравление RAG",),
    "Memory poisoning": ("Отравление памяти",),
    "Tool abuse": ("Злоупотребление инструментом",),
    "Confused deputy": ("Подставленный посредник",),
    "Excessive agency": ("Избыточная автономность",),
    "Data exfiltration": ("Вывод данных",),
    "Denial of wallet": ("Финансовое истощение",),
    "Cascading multi-agent failure": ("Каскадный отказ многоагентной схемы",),
    "Supply-chain compromise": ("Компрометация цепочки поставки",),
    "Missing audit trail": ("Потеря аудиторского следа",),
    "Evidence / telemetry": ("Доказательства / телеметрия",),
    "A2A trust and delegation artifact": (
        "Проверяемый A2A trust and delegation artifact",
        "Проверяемый артефакт доверия и делегирования для A2A",
    ),
    "delegation laundering": ("отмывания делегирования",),
    "context over-sharing": ("чрезмерного раскрытия контекста",),
    "remote-agent impersonation": ("подмены удаленного агента",),
    "unbounded delegation chains": ("неограниченных цепочек делегирования",),
    "conflicting actions": ("конфликтующих действий",),
    "lost accountability": ("потери подотчетности",),
    "cross-agent prompt injection": ("межагентного внедрения инструкций",),
}


def _expected_variants(path: str, item: str) -> tuple[str, ...]:
    if path.endswith(".en.md") or path.endswith(".zh.md"):
        return (item,)
    if not path.endswith(".md"):
        return (item,)
    return (item, *_RUSSIAN_EXPECTED_ALTERNATIVES.get(item, ()))


def _assert_file_contains(path: str, expected: str) -> None:
    text = _read(path)
    variants = _expected_variants(path, expected)
    assert any(variant in text for variant in variants), (path, expected)


def _load_mkdocs_config() -> dict:
    return yaml.load(_read("mkdocs.yml"), Loader=MkDocsConfigLoader)


def _assert_files_contain_all(paths: tuple[str, ...], expected: tuple[str, ...]) -> None:
    for path in paths:
        for item in expected:
            _assert_file_contains(path, item)


def _assert_files_contain_none(paths: tuple[str, ...], forbidden: tuple[str, ...]) -> None:
    for path in paths:
        text = _read(path)
        for item in forbidden:
            assert item not in text, (path, item)


def test_all_book_chapters_carry_case_spine_markers() -> None:
    chapter_paths = sorted(Path("docs/book").glob("part-*/chapter-*.md"))

    assert chapter_paths

    missing = []
    for path in chapter_paths:
        text = _read(str(path))
        lower_text = text.lower()
        if (
            "case-spine" not in lower_text
            and "case spine" not in lower_text
            and "сквозн" not in lower_text
        ):
            missing.append(str(path))

    assert missing == []


def test_all_appendix_pages_carry_canonical_case_markers() -> None:
    appendix_paths = sorted(Path("docs/appendix").glob("*.md"))

    assert appendix_paths

    missing = []
    for path in appendix_paths:
        text = _read(str(path))
        if (
            "Canonical " not in text
            and "Канонические " not in text
            and "Каноническая " not in text
        ):
            missing.append(str(path))

    assert missing == []


def test_all_book_part_indexes_surface_three_canonical_cases() -> None:
    part_index_paths = sorted(Path("docs/book").glob("part-*/index*.md"))
    required_markers_by_suffix = {
        ".zh.md": (
            "Support triage",
            "Internal knowledge assistant",
            "Incident coordination",
        ),
        ".en.md": (
            "Support triage",
            "Internal knowledge assistant",
            "Incident coordination",
        ),
        ".md": (
            "Разбор обращений поддержки",
            "Внутренний ассистент знаний",
            "Координация инцидентов",
        ),
    }

    assert part_index_paths

    missing = []
    for path in part_index_paths:
        if path.name.endswith(".zh.md"):
            suffix = ".zh.md"
        elif path.name.endswith(".en.md"):
            suffix = ".en.md"
        else:
            suffix = ".md"
        required_markers = required_markers_by_suffix[suffix]
        text = _read(str(path))
        absent = [marker for marker in required_markers if marker not in text]
        if absent:
            missing.append((str(path), absent))

    assert missing == []


def test_public_markdown_do_not_use_deprecated_canonical_case_labels() -> None:
    doc_paths = sorted(Path("docs").glob("**/*.md")) + sorted(Path(".").glob("README*.md"))
    deprecated_markers = (
        "Support Triage Agent",
        "Internal Knowledge Agent",
        "Incident Coordination Agent",
        "Support Triage",
        "Internal Knowledge",
        "Incident Coordination",
        "Internal enterprise knowledge assistant",
        "Approval-bound high-risk action agent",
        "support triage, internal knowledge, incident coordination",
    )

    assert doc_paths

    hits = []
    for path in doc_paths:
        text = _read(str(path))
        found = [marker for marker in deprecated_markers if marker in text]
        if found:
            hits.append((str(path), found))

    assert hits == []


def test_public_markdown_do_not_use_stale_publisher_packet_labels() -> None:
    doc_paths = sorted(Path("docs").glob("**/*.md")) + sorted(Path(".").glob("README*.md"))
    deprecated_markers = (
        "publisher-ready TOC",
        "Publisher-Ready TOC",
        "publisher-ready table of contents",
        "publisher-ready table-of-contents",
    )

    assert doc_paths

    hits = []
    for path in doc_paths:
        text = _read(str(path))
        found = [marker for marker in deprecated_markers if marker in text]
        if found:
            hits.append((str(path), found))

    assert hits == []


def test_russian_book_overview_pages_use_print_facing_terms() -> None:
    paths = (
        "docs/book/index.md",
        "docs/book/part-i/index.md",
        "docs/book/part-ii/index.md",
        "docs/book/part-iii/index.md",
        "docs/book/part-iv/index.md",
        "docs/book/part-v/index.md",
        "docs/book/part-vi/index.md",
        "docs/book/part-vii/index.md",
        "docs/book/part-viii/index.md",
        "docs/book/part-i/chapter-1.md",
    )
    expected_by_file = {
        "docs/book/index.md": (
            "Разбор обращений поддержки",
            "Внутренний ассистент знаний",
            "Координация инцидентов",
        ),
        "docs/book/part-i/chapter-1.md": ("Печатная схема выбора",),
        "docs/book/part-viii/index.md": (
            "Рамка жизненного цикла",
            "пакет изменения",
            "запись реестра",
        ),
    }
    forbidden = (
        "(book)",
        "(workflow)",
        "canonical case routes",
        "Canonical lifecycle cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "security perimeter",
        "execution layer",
        "observability",
        "operating model",
        "production discipline",
        "production-систем",
        "reference implementation",
        "runtime paths",
        "rollout checklist",
        "rollout readiness",
        "rollout shape",
        "Evidence Spine",
        "agent system",
        "release judgment",
        "red teaming",
        "governance",
        "ownership",
        "рантайм",
        "референс",
        "ревью",
        "раскатк",
    )

    for path, expected in expected_by_file.items():
        _assert_files_contain_all((path,), expected)
    _assert_files_contain_none(paths, forbidden)


def test_late_russian_public_pages_avoid_visible_english_role_terms() -> None:
    forbidden_by_file = {
        "docs/book/part-vi/chapter-14.md": (
            "Ownership case-spine note",
            "platform/product split",
            "canonical cases",
            "platform team",
            "product teams",
            "golden paths",
            "shared gateways",
            "anti-zoo patterns",
        ),
        "docs/book/part-vi/chapter-15.md": (
            "best practices",
            "Golden-path case-spine note",
            "Shared gateways",
            "Reusable template",
            "opinionated",
            "golden path",
            "golden paths",
            "Anti-zoo pattern",
            "platform defaults policy",
            "approved runtime patterns",
            "reference implementation",
        ),
        "docs/book/part-viii/chapter-25.md": (
            "behavioral scenarios",
            "User simulator",
            "synthetic adversary",
            "Research",
            "scenario classes",
            "failure classes",
            "release discipline",
        ),
        "docs/book/part-viii/chapter-27.md": (
            "accountability layer",
            "production entities",
            "control ownership",
            "lifecycle truth",
            "registry —",
            "observability, policy, lifecycle",
            "accountable production entity",
            "agent builders",
            "discovery mechanisms",
            "discovered entities",
            "approved production agents",
        ),
        "docs/appendix/google-integration-roadmap.md": (
            "production-ready platform view",
            "agent identity, registry и governance",
            "platform-grade",
            "User simulator",
            "continuous eval loop",
            "Registry, approved inventory",
            "organizational controls",
        ),
    }

    for path, forbidden in forbidden_by_file.items():
        _assert_files_contain_none((path,), forbidden)


def test_late_russian_public_pages_use_print_friendly_role_terms() -> None:
    expected_by_file = {
        "docs/book/part-vi/chapter-14.md": (
            "Заметка о сквозных сценариях владения",
            "разделение платформы и продуктов",
            "золотые пути, общие шлюзы и антизоопарк-подходы",
        ),
        "docs/book/part-vi/chapter-15.md": (
            "набор советов",
            "Заметка о сквозных сценариях золотого пути",
            "Общие шлюзы",
            "Переиспользуемый шаблон",
            "Пример политики платформенных настроек по умолчанию",
        ),
        "docs/book/part-viii/chapter-25.md": (
            "таксономия поведенческих сценариев",
            "Симулятор пользователя и синтетический противник",
            "классы сценариев",
            "дисциплины выпуска",
        ),
        "docs/book/part-viii/chapter-27.md": (
            "слой подотчетности",
            "производственные сущности",
            "управление умеет различать обнаруженные сущности и агентов, "
            "одобренных для промышленной среды",
        ),
        "docs/appendix/google-integration-roadmap.md": (
            "платформенный взгляд, пригодный для промышленной эксплуатации",
            "идентичность агента, реестр и управление",
            "Симулятор пользователя и непрерывный оценочный контур",
        ),
    }

    for path, expected in expected_by_file.items():
        _assert_files_contain_all((path,), expected)


def test_russian_practical_pages_use_reader_facing_terms() -> None:
    expected_by_file = {
        "docs/book/part-iv/practical-mcp-a2a.md": (
            "# Практика. MCP для инструментов, A2A для агентов",
            "## 4. Типовая ошибка: строить многоагентную систему слишком рано",
            "## 5. Таблица решений",
            "## 8. Минимальный кодовый эскиз",
        ),
        "docs/book/part-v/evidence-spine.md": (
            "# Сквозная цепочка доказательств: от запроса к решению о поэтапном выпуске",
            "## Один сквозной запуск",
            "Разбор обращений поддержки",
            "Внутренний ассистент знаний",
            "Координация инцидентов",
        ),
    }
    forbidden_by_file = {
        "docs/book/part-iv/practical-mcp-a2a.md": (
            "MCP для tools, A2A для agents",
            "multi-agent",
            "Decision table",
            "code sketch",
            "canonical cases",
            "Support triage",
            "Internal knowledge assistant",
            "Incident coordination",
        ),
        "docs/book/part-v/evidence-spine.md": (
            "walkthrough run",
            "canonical cases",
            "Support triage",
            "Internal knowledge assistant",
            "Incident coordination",
        ),
    }

    for path, expected in expected_by_file.items():
        _assert_files_contain_all((path,), expected)
    for path, forbidden in forbidden_by_file.items():
        _assert_files_contain_none((path,), forbidden)


def test_russian_appendix_reference_pages_avoid_visible_english_role_terms() -> None:
    forbidden_by_file = {
        "docs/appendix/policy-templates.md": (
            "production YAML",
            "read and write actions",
            "duplicate-ticket thread",
            "write tool",
            "governed capability",
            "approval boundary",
            "traceable write intent",
            "rollout/eval gate",
            "Canonical policy template cases",
            "customer context",
            "read tools",
            "approval policy",
            "write path",
            "Role-based filtering",
            "retrieval path",
            "knowledge zone",
            "incident trace",
            "Risky remediation",
            "dangerous write path",
            "policy artifacts",
            "prompt engineering",
            "policy layer",
        ),
        "docs/appendix/causal-debugging.md": (
            "Causal debugging",
            "root-cause analysis",
            "agent systems",
            "traces, session summaries",
            "incident records",
            "Canonical causal cases",
            "retrieval;",
            "model step",
            "tool call",
            "approval path",
            "orchestration step",
            "cascade of failures",
            "system behavior",
            "suspect path",
            "downstream noise",
            "corrective action",
            "bad postmortem conclusion",
            "causal graph",
            "trace review",
        ),
        "docs/appendix/memory-eval-patterns.md": (
            "Memory eval patterns",
            "agent systems",
            "runs",
            "memory layer",
            "eval dataset",
            "memory evals",
            "overall task success",
            "memory design",
            "system remembers the wrong thing",
            "background compaction",
            "evaluation logic",
            "Short-term memory",
            "storage itself",
            "worth carrying forward",
            "Profile memory",
            "long-term memory",
            "multi-run scenarios",
            "single-turn checks",
            "Memory evals",
        ),
        "docs/appendix/incident-record-schema.md": (
            "incident record",
            "postmortem linkage",
            "incident review",
            "agent systems",
            "traces, approvals, rollout",
            "lifecycle artifacts",
            "containment phase",
            "incident artifact",
            "observability system",
            "approval history",
            "audit trail",
            "rollback decision",
            "repeated incidents",
            "operational response",
            "lifecycle correction",
            "blast radius",
            "release discipline",
            "duplicate-ticket thread",
            "Canonical incident cases",
        ),
        "docs/appendix/research-frontier.md": (
            "Research frontier",
            "multi-agent систем",
            "production",
            "papers",
            "policy layers",
            "approval gates",
            "trace schema",
            "eval datasets",
            "lifecycle discipline",
            "research frontier",
            "paper architecture",
            "promising pattern",
            "production default",
            "accuracy",
            "explainability",
            "auditability",
            "Canonical frontier cases",
            "Frontier по памяти",
            "vector store",
            "self-adaptive memory reorganization",
            "reasoning loop",
        ),
    }

    for path, forbidden in forbidden_by_file.items():
        _assert_files_contain_none((path,), forbidden)


def test_russian_appendix_reference_pages_use_print_friendly_terms() -> None:
    expected_by_file = {
        "docs/appendix/policy-templates.md": (
            "готовый промышленный YAML",
            "читающие и пишущие действия",
            "Политика для ветки дубля тикета",
            "Канонические сценарии шаблонов политик",
            "управляемой пишущей возможности",
            "ролевых ограничений поиска",
        ),
        "docs/appendix/causal-debugging.md": (
            "Причинная отладка и анализ первопричин",
            "трассы, сводки сессий и записи инцидентов",
            "Канонические причинные сценарии",
            "решающие связи",
            "сеть зависимостей",
        ),
        "docs/appendix/memory-eval-patterns.md": (
            "Шаблоны оценки памяти для агентных систем",
            "серии запусков",
            "слой памяти",
            "Канонические сценарии оценки памяти",
            "проверочной логики",
        ),
        "docs/appendix/incident-record-schema.md": (
            "Схема записи инцидента и связи с разбором",
            "контрактный слой для разбора инцидентов",
            "запись инцидента",
            "Канонические сценарии инцидентов",
            "радиус воздействия",
        ),
        "docs/appendix/research-frontier.md": (
            "Исследовательский фронтир: память, наблюдаемость и надежность многоагентных систем",
            "промышленную среду",
            "Канонические сценарии исследовательского фронтира",
            "многообещающий шаблон",
            "инженерной дисциплины",
        ),
    }

    for path, expected in expected_by_file.items():
        _assert_files_contain_all((path,), expected)


def test_render_export_qa_matrix_tracks_review_priority_pages() -> None:
    required_markers = (
        "Render / Export QA Checklist",
        "HTML browser",
        "plain text extraction",
        "PDF export",
        "print export",
        "mobile viewport",
        "search index extraction",
        "Chapter 1 decision frame",
        "Chapter 2 layer map",
        "Chapter 9 Mermaid / YAML / MCP sections",
        "Chapter 13 eval loop Mermaid",
        "Reference final rule",
        "Reference Package CLI / YAML blocks",
        "Chapter 26 telemetry lists",
        "Chapter 27 registry records",
        "status: passed local MkDocs/search/test QA and automated browser/PDF/mobile smoke QA",
        "desktop and mobile screenshots, plain text checks, print media emulation, and PDF export",
        "independent human copy-edit and final print proof remain required",
        "not a public book page",
    )

    _assert_files_contain_all(("docs/render-export-qa-checklist.md",), required_markers)
    mkdocs_config = _read("mkdocs.yml")
    assert "render-export-qa-checklist.md" in mkdocs_config
    assert "superpowers/**" in mkdocs_config


def test_public_book_canonical_redirects_are_configured() -> None:
    mkdocs_config = _load_mkdocs_config()
    scripts = mkdocs_config["extra_javascript"]

    assert "javascripts/canonical-redirects.js" in scripts

    redirect_script = _read("docs/javascripts/canonical-redirects.js")
    for route in (
        '"/book"',
        '"/en/book"',
        '"/zh/book"',
        '"/start-here"',
        '"/en/start-here"',
        '"/zh/start-here"',
        '"/reference"',
        '"/en/reference"',
        '"/zh/reference"',
        '"/appendix/sources"',
        '"/en/appendix/sources"',
        '"/zh/appendix/sources"',
        '"/book/part-i/chapter-1"',
        '"/en/book/part-i/chapter-1"',
        '"/zh/book/part-i/chapter-1"',
        '"/book/part-iv/chapter-9"',
        '"/en/book/part-iv/chapter-9"',
        '"/zh/book/part-iv/chapter-9"',
        '"/book/part-v/chapter-13"',
        '"/en/book/part-v/chapter-13"',
        '"/zh/book/part-v/chapter-13"',
    ):
        assert route in redirect_script
    assert 'projectPrefix = "/agent-arch"' in redirect_script


def _canonical_redirects_for(pathname: str, search: str = "", hash_: str = "") -> list[str]:
    node = shutil.which("node")
    if node is None:
        raise pytest.skip.Exception("node is required to execute canonical-redirects.js")

    redirect_script = _read("docs/javascripts/canonical-redirects.js")
    harness = f"""
    const redirects = [];
    const location = {{
      origin: "https://agent-axiom.github.io",
      pathname: {json.dumps(pathname)},
      search: {json.dumps(search)},
      hash: {json.dumps(hash_)},
      get href() {{
        return this.origin + this.pathname + this.search + this.hash;
      }},
      replace(url) {{
        redirects.push(url);
      }}
    }};
    global.window = {{ location }};
    {redirect_script}
    process.stdout.write(JSON.stringify(redirects));
    """
    result = subprocess.run(
        [node, "-e", textwrap.dedent(harness)],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def test_public_book_canonical_redirects_do_not_reload_current_canonical_urls() -> None:
    assert _canonical_redirects_for("/agent-arch/book/") == []
    assert _canonical_redirects_for("/agent-arch/en/book/") == []
    assert _canonical_redirects_for("/agent-arch/zh/book/") == []


def test_public_book_canonical_redirects_add_trailing_slash_to_entrypoints() -> None:
    assert _canonical_redirects_for("/agent-arch/book", "?tab=toc", "#intro") == [
        "https://agent-axiom.github.io/agent-arch/book/?tab=toc#intro"
    ]
    assert _canonical_redirects_for("/agent-arch/reference", "?view=schemas", "#top") == [
        "https://agent-axiom.github.io/agent-arch/reference/?view=schemas#top"
    ]
    assert _canonical_redirects_for("/agent-arch/appendix/sources") == [
        "https://agent-axiom.github.io/agent-arch/appendix/sources/"
    ]
    assert _canonical_redirects_for("/agent-arch/book/part-i/chapter-1") == [
        "https://agent-axiom.github.io/agent-arch/book/part-i/chapter-1/"
    ]
    assert _canonical_redirects_for("/agent-arch/book/part-iv/chapter-9") == [
        "https://agent-axiom.github.io/agent-arch/book/part-iv/chapter-9/"
    ]
    assert _canonical_redirects_for("/agent-arch/book/part-v/chapter-13") == [
        "https://agent-axiom.github.io/agent-arch/book/part-v/chapter-13/"
    ]
    assert _canonical_redirects_for("/agent-arch/en/reference", "?view=schemas") == [
        "https://agent-axiom.github.io/agent-arch/en/reference/?view=schemas"
    ]
    assert _canonical_redirects_for("/agent-arch/zh/appendix/sources", "", "#top") == [
        "https://agent-axiom.github.io/agent-arch/zh/appendix/sources/#top"
    ]
    assert _canonical_redirects_for("/agent-arch/en/book/part-i/chapter-1") == [
        "https://agent-axiom.github.io/agent-arch/en/book/part-i/chapter-1/"
    ]
    assert _canonical_redirects_for("/agent-arch/zh/book/part-v/chapter-13") == [
        "https://agent-axiom.github.io/agent-arch/zh/book/part-v/chapter-13/"
    ]


def test_public_book_extensionless_fallback_redirect_pages_exist() -> None:
    expected_pages = {
        "docs/book.html": ("ru", "book/"),
        "docs/en/book.html": ("en", "book/"),
        "docs/zh/book.html": ("zh", "book/"),
        "docs/start-here.html": ("ru", "start-here/"),
        "docs/en/start-here.html": ("en", "start-here/"),
        "docs/zh/start-here.html": ("zh", "start-here/"),
        "docs/reference.html": ("ru", "reference/"),
        "docs/en/reference.html": ("en", "reference/"),
        "docs/zh/reference.html": ("zh", "reference/"),
        "docs/appendix/sources.html": ("ru", "sources/"),
        "docs/en/appendix/sources.html": ("en", "sources/"),
        "docs/zh/appendix/sources.html": ("zh", "sources/"),
        "docs/book/part-i/chapter-1.html": ("ru", "chapter-1/"),
        "docs/en/book/part-i/chapter-1.html": ("en", "chapter-1/"),
        "docs/zh/book/part-i/chapter-1.html": ("zh", "chapter-1/"),
        "docs/book/part-iv/chapter-9.html": ("ru", "chapter-9/"),
        "docs/en/book/part-iv/chapter-9.html": ("en", "chapter-9/"),
        "docs/zh/book/part-iv/chapter-9.html": ("zh", "chapter-9/"),
        "docs/book/part-v/chapter-13.html": ("ru", "chapter-13/"),
        "docs/en/book/part-v/chapter-13.html": ("en", "chapter-13/"),
        "docs/zh/book/part-v/chapter-13.html": ("zh", "chapter-13/"),
    }

    for page_path, (language, target) in expected_pages.items():
        page = _read(page_path)
        assert f'<html lang="{language}">' in page
        assert f'content="0; url={target}"' in page
        assert f'<link rel="canonical" href="{target}">' in page
        assert "window.location.replace" in page
        assert "window.location.search + window.location.hash" in page


def _flatten_nav_labels(entries: Sequence[object]) -> list[str]:
    labels = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        for label, value in entry.items():
            labels.append(str(label))
            if isinstance(value, list):
                labels.extend(_flatten_nav_labels(value))
    return labels


def test_russian_nav_labels_are_print_friendly() -> None:
    config = _load_mkdocs_config()
    labels = _flatten_nav_labels(config["nav"])
    mkdocs_text = _read("mkdocs.yml")

    for expected in (
        "Причинная отладка и анализ первопричин для агентных систем",
        "Шаблоны оценки памяти для агентных систем",
        "Восстановление после сбоев инструментов в агентных системах",
        "Схема записи инцидента и связи с разбором",
        "Исследовательский фронтир: память, наблюдаемость и надежность многоагентных систем",
        "Практическое руководство по реестру агентов и инвентаризации",
    ):
        assert expected in labels

    for forbidden in (
        "Causal debugging и root-cause analysis для agent systems",
        "Memory eval patterns для agent systems",
        "Tool failure recovery patterns для agent systems",
        "Схема incident record и postmortem linkage",
        "Исследовательский фронтир: память, наблюдаемость и надежность multi-agent систем",
        "Handbook по agent registry и inventory operations",
    ):
        assert forbidden not in labels
        assert forbidden not in mkdocs_text


def test_translated_markdown_pages_have_no_cyrillic_residue() -> None:
    translated_paths = sorted((ROOT / "docs").rglob("*.en.md")) + sorted(
        (ROOT / "docs").rglob("*.zh.md")
    )

    assert translated_paths

    leaked_lines = []
    for path in translated_paths:
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if re.search(r"[А-Яа-яЁё]", line):
                leaked_lines.append((str(path.relative_to(ROOT)), line_number, line.strip()))

    assert leaked_lines == []


def test_russian_public_entrypoints_avoid_inline_english_glosses() -> None:
    forbidden_by_file = {
        "docs/reference.md": (
            "(reference layer)",
            "(why)",
            "(safe agent system)",
            "(artifacts)",
            "(schemas)",
            "(rules)",
            "(contract page)",
            "(architecture review)",
            "(rollout review)",
            "(canonical cases)",
            "(support-triage)",
            "(traces)",
            "(eval dataset)",
            "(policy bundle)",
            "(approval record)",
            "(incident record)",
            "(change rollout)",
            "(lifecycle artifacts)",
            "(registry operations)",
            "(Safe-agent schema spine)",
            "(trace schema)",
            "(eval schema)",
            "(memory/retrieval schema)",
            "(MCP threat model)",
            "(A2A handoff trust contract)",
            "(verifier verdict record)",
            "(governance action record)",
            "(memory poisoning review fields)",
            "(unified agent threat evidence)",
            "(semantic tool filtering)",
            "(read/write taxonomy)",
            "(MCP host/client/server)",
            "(capability transport)",
            "(sandbox boundary)",
            "(semantic gap)",
            "(RAG vs training)",
            "(latency budget)",
            "(LLM-as-a-judge)",
            "(judge-human agreement)",
        ),
        "docs/appendix/cheat-sheets.md": (
            "Safety checklist",
            "Memory checklist",
            "Rollout checklist",
            "Observability checklist",
            "Tool gateway checklist",
            "(Canonical checklist cases)",
            "(fast route)",
            "(canonical cases)",
            "(Support triage)",
            "(Internal knowledge assistant)",
            "(Incident coordination)",
            "(safety)",
            "(tool gateway)",
            "(approval)",
            "(idempotency)",
            "(rollout checks)",
            "(memory)",
            "(retrieval)",
            "(source grounding)",
            "(tenant boundary)",
            "(observability checks)",
            "(incident review)",
            "(response ownership)",
            "(post-incident learning checks)",
        ),
    }

    for path, forbidden_markers in forbidden_by_file.items():
        _assert_files_contain_none((path,), forbidden_markers)


def test_translated_navigation_values_have_no_cyrillic_residue() -> None:
    mkdocs_config = _load_mkdocs_config()
    locales = {}
    for plugin in mkdocs_config["plugins"]:
        if isinstance(plugin, dict) and "i18n" in plugin:
            locales = {language["locale"]: language for language in plugin["i18n"]["languages"]}
            break

    leaked_values = []
    for locale in ("en", "zh"):
        for target in locales[locale]["nav_translations"].values():
            if re.search(r"[А-Яа-яЁё]", str(target)):
                leaked_values.append((locale, target))

    assert leaked_values == []


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


def test_part_viii_role_map_is_present_in_all_languages() -> None:
    expected_by_file = {
        "docs/book/part-viii/index.md": (
            "Карта ролей этой части",
            "Рамка жизненного цикла",
            "Управление изменениями",
            "Контур заверения",
            "Происхождение",
            "Вывод из эксплуатации",
            "Несоответствие целей и инсайдерский риск",
            "Поведенческие и контрольные оценки",
            "Наблюдаемость",
            "Инвентаризация и реестр",
        ),
        "docs/book/part-viii/index.en.md": (
            "Role Map for This Part",
            "Lifecycle frame",
            "Change management",
            "Assurance",
            "Provenance",
            "Retirement",
            "Misalignment and insider risk",
            "Behavioral/control evals",
            "Observability",
            "Inventory and registry",
        ),
        "docs/book/part-viii/index.zh.md": (
            "这一部分的角色地图",
            "生命周期框架",
            "变更管理",
            "保障闭环",
            "来源追踪",
            "退役",
            "失配与内部人风险",
            "行为/控制评测",
            "可观测性",
            "清单与注册表",
        ),
    }

    for relative_path, markers in expected_by_file.items():
        text = _read(relative_path)
        missing = [marker for marker in markers if marker not in text]
        assert not missing, f"{relative_path} missing role-map markers: {missing}"


def test_part_viii_role_map_links_schema_backed_artifacts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/index.md": (
            "[пакет изменения](../../appendix/change-rollout-schema.md)",
            "[запись о находке и реагировании](../../appendix/incident-record-schema.md)",
            "[утвержденный набор артефактов]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[план вывода из эксплуатации](../../appendix/lifecycle-artifact-schema.md)",
            "[оценочный шлюз и контракт проверки](../../appendix/eval-schema.md)",
            "[запись покрытия трассировкой и телеметрией]"
            "(../../appendix/trace-schema.md)",
            "[запись реестра](../../appendix/registry-operations-handbook.md)",
        ),
        "docs/book/part-viii/index.en.md": (
            "[Change packet](../../appendix/change-rollout-schema.en.md)",
            "[Finding and response record]"
            "(../../appendix/incident-record-schema.en.md)",
            "[Approved artifact bundle]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[Retirement plan](../../appendix/lifecycle-artifact-schema.en.md)",
            "[Eval gate and verifier contract](../../appendix/eval-schema.en.md)",
            "[Trace and telemetry coverage record]"
            "(../../appendix/trace-schema.en.md)",
            "[Registry record]"
            "(../../appendix/registry-operations-handbook.en.md)",
        ),
        "docs/book/part-viii/index.zh.md": (
            "[变更包](../../appendix/change-rollout-schema.zh.md)",
            "[发现与响应记录（finding and response record）]"
            "(../../appendix/incident-record-schema.zh.md)",
            "[已批准工件包]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[退役计划](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[评测门禁与验证器契约（eval gate and verifier contract）]"
            "(../../appendix/eval-schema.zh.md)",
            "[追踪与遥测覆盖记录（trace and telemetry coverage record）]"
            "(../../appendix/trace-schema.zh.md)",
            "[注册表记录（registry record）]"
            "(../../appendix/registry-operations-handbook.zh.md)",
        ),
    }

    for relative_path, expected_snippets in expected_snippets_by_file.items():
        text = _read(relative_path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (relative_path, expected_snippet)

    chinese_text = _read("docs/book/part-viii/index.zh.md")
    forbidden_chinese_links = (
        "[Finding 与响应记录](../../appendix/incident-record-schema.zh.md)",
        "[Eval gate 与 verifier contract](../../appendix/eval-schema.zh.md)",
        "[Trace 与 telemetry 覆盖记录](../../appendix/trace-schema.zh.md)",
        "[Registry record](../../appendix/registry-operations-handbook.zh.md)",
    )
    for forbidden_chinese_link in forbidden_chinese_links:
        assert forbidden_chinese_link not in chinese_text, forbidden_chinese_link


def test_part_viii_role_map_is_print_friendly() -> None:
    role_map_markers = {
        "docs/book/part-viii/index.md": ("## В этой части", "Печатная версия"),
        "docs/book/part-viii/index.en.md": ("## In This Part", "print-friendly"),
        "docs/book/part-viii/index.zh.md": ("## 本部分内容", "print-friendly"),
    }

    for relative_path, (next_heading, print_marker) in role_map_markers.items():
        text = _read(relative_path)
        role_map = text.split("##", 2)[2].split(next_heading, 1)[0]
        assert "|" not in role_map, relative_path
        assert print_marker.lower() in role_map.lower(), relative_path
        assert role_map.count("- **") >= 9, relative_path


def test_part_viii_chapters_define_print_friendly_role_cards() -> None:
    chapter_bases = tuple(f"docs/book/part-viii/chapter-{number}" for number in range(19, 28))
    expected_by_suffix = {
        ".md": (
            '!!! note "Роль главы в части VIII"',
            "Главный вопрос:",
            "Уникальный артефакт:",
            "Граница с соседними главами:",
            "Что эта глава не покрывает:",
            "Продолжение сквозного сценария:",
        ),
        ".en.md": (
            '!!! note "Chapter Role in Part VIII"',
            "Main question:",
            "Unique artifact:",
            "Neighboring boundary:",
            "This chapter does not cover:",
            "Case continuation:",
        ),
        ".zh.md": (
            '!!! note "第 VIII 部分中的章节角色"',
            "核心问题：",
            "独特工件：",
            "相邻边界：",
            "本章不覆盖：",
            "案例延续：",
        ),
    }

    for base in chapter_bases:
        for suffix, expected_markers in expected_by_suffix.items():
            _assert_files_contain_all((f"{base}{suffix}",), expected_markers)


def test_part_viii_role_cards_keep_neighboring_chapters_distinct() -> None:
    expected_russian_boundaries = {
        "docs/book/part-viii/chapter-19.md": (
            "жизненный цикл задает состояния; управление изменениями решает, "
            "какие переходы требуют проверки"
        ),
        "docs/book/part-viii/chapter-20.md": (
            "управление изменениями решает, что требует выпуска; контур заверения "
            "начинается после сигнала риска"
        ),
        "docs/book/part-viii/chapter-21.md": (
            "реагирование и сдерживание, не оценочное суждение"
        ),
        "docs/book/part-viii/chapter-22.md": "происхождение артефактов, не наблюдаемость",
        "docs/book/part-viii/chapter-23.md": (
            "вывод из эксплуатации закрывает старые права действовать"
        ),
        "docs/book/part-viii/chapter-24.md": (
            "сценарии несоответствия целей и инсайдерского риска, не общие правила "
            "против внедрения инструкций"
        ),
        "docs/book/part-viii/chapter-25.md": (
            "поведенческая и контрольная оценка, не реагирование на инцидент"
        ),
        "docs/book/part-viii/chapter-26.md": "доказательная подложка, не реестр владения",
        "docs/book/part-viii/chapter-27.md": (
            "владение и ответственность, не проектирование телеметрии"
        ),
    }
    expected_english_boundaries = {
        "docs/book/part-viii/chapter-19.en.md": (
            "lifecycle defines states; change management decides which transitions need review"
        ),
        "docs/book/part-viii/chapter-20.en.md": (
            "change management decides what needs release control; assurance begins "
            "after a risk signal"
        ),
        "docs/book/part-viii/chapter-21.en.md": "response and containment, not eval judgment",
        "docs/book/part-viii/chapter-22.en.md": "artifact provenance, not observability",
        "docs/book/part-viii/chapter-23.en.md": "retirement closes old rights to act",
        "docs/book/part-viii/chapter-24.en.md": (
            "misalignment and insider-risk scenarios, not generic prompt-injection rules"
        ),
        "docs/book/part-viii/chapter-25.en.md": (
            "behavioral and control judgment, not incident response"
        ),
        "docs/book/part-viii/chapter-26.en.md": "evidence substrate, not ownership registry",
        "docs/book/part-viii/chapter-27.en.md": (
            "ownership and accountability, not telemetry design"
        ),
    }
    expected_chinese_boundaries = {
        "docs/book/part-viii/chapter-19.zh.md": (
            "生命周期定义状态；变更管理决定哪些状态转换需要审查"
        ),
        "docs/book/part-viii/chapter-20.zh.md": (
            "变更管理决定什么需要发布控制；保障闭环从风险信号之后开始"
        ),
        "docs/book/part-viii/chapter-21.zh.md": "响应与遏制，而不是评测判断",
        "docs/book/part-viii/chapter-22.zh.md": "工件来源追踪，而不是可观测性",
        "docs/book/part-viii/chapter-23.zh.md": "退役关闭旧的行动权",
        "docs/book/part-viii/chapter-24.zh.md": (
            "失配与内部人风险场景，而不是通用提示注入规则"
        ),
        "docs/book/part-viii/chapter-25.zh.md": "行为与控制判断，而不是事故响应",
        "docs/book/part-viii/chapter-26.zh.md": "证据基底，而不是所有权注册表",
        "docs/book/part-viii/chapter-27.zh.md": "所有权与问责，而不是遥测设计",
    }

    for path, marker in {
        **expected_russian_boundaries,
        **expected_english_boundaries,
        **expected_chinese_boundaries,
    }.items():
        assert marker in _read(path), (path, marker)


def test_part_viii_chinese_chapter_artifact_labels_are_localized() -> None:
    expected_and_forbidden_by_file = {
        "docs/book/part-viii/chapter-19.zh.md": (
            "本章的主要工件是智能体开发生命周期状态模型（ADLC state model）：",
            "本章的主要工件是 ADLC state model：",
        ),
        "docs/book/part-viii/chapter-20.zh.md": (
            "本章的主要工件是变更包（change packet）：",
            "本章的主要工件是 change packet：",
        ),
        "docs/book/part-viii/chapter-21.zh.md": (
            "本章的主要工件是发现与响应记录（finding and response record）：",
            "本章的主要工件是 finding and response record：",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "本章的主要工件是[已批准工件包（approved artifact bundle）]",
            "本章的主要工件是 approved artifact bundle：",
        ),
        "docs/book/part-viii/chapter-23.zh.md": (
            "本章的主要工件是退役计划（retirement plan）：",
            "本章的主要工件是 retirement plan：",
        ),
        "docs/book/part-viii/chapter-24.zh.md": (
            "本章的主要工件是风险场景与控制计划"
            "（risk scenario and control plan）：",
            "本章的主要工件是 risk scenario and control plan：",
        ),
        "docs/book/part-viii/chapter-25.zh.md": (
            "本章的主要工件是评测门禁与验证器契约"
            "（eval gate and verifier contract）：",
            "本章的主要工件是 eval gate and verifier contract：",
        ),
        "docs/book/part-viii/chapter-26.zh.md": (
            "本章的主要工件是追踪与遥测覆盖记录"
            "（trace and telemetry coverage record）：",
            "本章的主要工件是 trace and telemetry coverage record：",
        ),
        "docs/book/part-viii/chapter-27.zh.md": (
            "本章的主要工件是注册表记录（registry record）：",
            "本章的主要工件是 registry record：",
        ),
    }

    for relative_path, (expected_label, forbidden_label) in expected_and_forbidden_by_file.items():
        text = _read(relative_path)
        assert expected_label in text, (relative_path, expected_label)
        assert forbidden_label not in text, (relative_path, forbidden_label)


def test_chapter_22_chinese_intro_artifact_label_is_localized() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-22.zh.md")
    expected_markers = (
        "本章的主要工件是[已批准工件包（approved artifact bundle）]",
        "一组已评审的版本、契约和模式",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "本章的主要工件是 [已批准工件包",
        "本章的主要工件是 approved artifact bundle",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chapter_23_chinese_state_tail_labels_are_localized() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-23.zh.md")
    expected_markers = (
        "暂停运行状态（paused-run state）与后台运行状态（background-run state）",
        "能力会话状态（capability-session state）与中断血缘（interruption lineage）",
        "编排模式血缘（orchestration-pattern lineage）与工作边界决策（worker-boundary decisions）",
        "委托授权血缘（delegated authorization lineage）与撤销状态（revoke state）",
        "跨越上下文重置（context reset）与角色交接边界的交接工件血缘（handoff-artifact lineage）",
        "关闭后记忆、追踪、审批、暂停运行状态（paused-run state）和"
        "能力会话状态（capability-session state）怎么处理",
        "主体、连接器、出口访问、暂停审批（paused approvals）、能力会话重新初始化"
        "（capability-session re-init）和后台路由（background routes）能否快速撤销或排空",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "paused-run state 与 background-run state",
        "capability-session state 与 interruption lineage",
        "orchestration-pattern lineage 与 worker-boundary decisions",
        "delegated authorization lineage 与 revoke state",
        "跨越 context reset 与角色交接边界的 handoff-artifact lineage",
        "关闭后记忆、追踪、审批、paused-run state 和 capability-session state 怎么处理",
        "主体、连接器、出口访问、paused approvals、capability-session re-init 和 "
        "background routes 能否快速撤销或排空",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chapter_23_chinese_retirement_maturity_labels_are_localized() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-23.zh.md")
    expected_markers = (
        "主体（principals）、连接器（connectors）、记忆写入（memory writes）、"
        "暂停运行（paused runs）、能力会话（capability sessions）、"
        "编排模式（orchestration patterns）与后台任务（background jobs）",
        "替换是分阶段的，而不是二元切换（cutover）",
        "已废弃模式会变成真正被阻断的路径，而不只是警告（warnings）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "principals、connectors、memory writes、paused runs、capability sessions、"
        "orchestration patterns 与 background jobs",
        "替换是分阶段的，而不是二元 cutover",
        "已废弃模式会变成真正被阻断的路径，而不只是 warnings",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chapter_23_chinese_deprecated_schema_labels_are_localized() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-23.zh.md")
    expected_marker = (
        "已废弃的审批模式（approval schemas）与运行时控制模式（runtime-control schemas）"
        "会被真正关闭"
    )
    assert expected_marker in chinese_text, expected_marker

    forbidden_marker = "已废弃的 approval 与 runtime-control schemas 会被真正关闭"
    assert forbidden_marker not in chinese_text, forbidden_marker


def test_chapter_23_chinese_verifier_contract_lineage_label_is_localized() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-23.zh.md")
    expected_marker = "验证器契约血缘（verifier-contract lineage）与[验证器证据保留义务"
    assert expected_marker in chinese_text, expected_marker

    forbidden_marker = "verifier-contract lineage 与[验证器证据保留义务"
    assert forbidden_marker not in chinese_text, forbidden_marker


def test_chapter_23_chinese_intro_artifact_label_is_localized() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-23.zh.md")
    expected_markers = (
        "本章的主要工件是退役计划（retirement plan）",
        "一份关闭权限、状态、证据和负责人归属的计划",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "本章的主要工件是 退役计划",
        "本章的主要工件是 retirement plan",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chapter_21_chinese_review_rollout_labels_are_localized() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-21.zh.md")
    expected_markers = (
        "事故、检测、重新设计和发布（rollout）规则变更之间必须闭环",
        "不只是发布（rollout）工件，也是一种保障场景",
        "未经评审的发布（rollout）控制下的验证器契约版本变更",
        "- 发布（rollout）门禁；",
        "- 发布（rollout）策略。",
        "更新后的策略、评测和发布（rollout）规则",
        "事故会回流进评测、策略和发布（rollout）规则。",
        "事故会不会回流到评测和发布（rollout）规则？",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "事故、检测、重新设计和 rollout 规则变更之间必须闭环",
        "不只是 rollout 工件，也是一种保障场景",
        "未经评审的 rollout 控制下的验证器契约版本变更",
        "- rollout 门禁；",
        "- rollout 策略。",
        "更新后的策略、评测和 rollout 规则",
        "事故会回流进评测、策略和 rollout 规则。",
        "事故会不会回流到评测和 rollout 规则？",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chapter_21_chinese_intro_artifact_label_is_localized() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-21.zh.md")
    expected_markers = (
        "本章的主要工件是发现与响应记录（finding and response record）",
        "把信号、风险、负责人、临时遏制、修复和关闭条件连在一起",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "本章的主要工件是 发现与响应记录",
        "本章的主要工件是 finding and response record",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chapter_20_chinese_worker_boundary_labels_are_localized() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-20.zh.md")
    expected_marker = (
        "编排模式选择、工作者安全目录（worker-safe catalog）暴露与"
        "委派工作者（delegated worker）评审边界"
    )
    assert expected_marker in chinese_text, expected_marker

    forbidden_marker = "编排模式选择、worker-safe 目录暴露与委派 worker 评审边界"
    assert forbidden_marker not in chinese_text, forbidden_marker


def test_chapter_20_chinese_review_rollout_labels_are_localized() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-20.zh.md")
    expected_markers = (
        "审批流与分阶段发布（rollout）能力",
        "变更评审必须与评测、审批和发布（rollout）门禁连接起来",
        "写能力、重试行为和发布（rollout）门禁",
        "影响半径在发布（rollout）前就被限制",
        "每次发布（rollout）的影响半径是否清楚？",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "审批流与分阶段 rollout 能力",
        "变更评审必须与评测、审批和 rollout 门禁连接起来",
        "写能力、重试行为和 rollout 门禁",
        "影响半径在 rollout 前就被限制",
        "每次 rollout 的影响半径是否清楚？",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chapter_20_chinese_intro_artifact_label_is_localized() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-20.zh.md")
    expected_markers = (
        "本章的主要工件是变更包（change packet）",
        "一个发布重要性决策包",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "本章的主要工件是 变更包",
        "本章的主要工件是 change packet",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chapter_19_chinese_rollout_checklist_label_is_localized() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-19.zh.md")
    expected_marker = "发布（rollout）检查清单就等于整个生命周期"
    assert expected_marker in chinese_text, expected_marker

    forbidden_marker = "rollout 检查清单就等于整个生命周期"
    assert forbidden_marker not in chinese_text, forbidden_marker


def test_chapter_19_chinese_intro_artifact_label_is_localized() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-19.zh.md")
    expected_markers = (
        "本章的主要工件是智能体开发生命周期状态模型（ADLC state model）",
        "一张状态与转换地图",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "本章的主要工件是 智能体开发生命周期状态模型",
        "本章的主要工件是 ADLC state model",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chapter_27_chinese_intro_artifact_label_is_localized() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-27.zh.md")
    expected_markers = (
        "本章的主要工件是注册表记录（registry record）",
        "运行时控制责任归属（runtime-control ownership）",
        "证据链接（evidence links）连起来的记录",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "本章的主要工件是 注册表记录",
        "本章的主要工件是 registry record",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chapter_27_chinese_registry_layer_labels_are_localized() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-27.zh.md")
    expected_markers = (
        "智能体蔓延”（agent sprawl）",
        "智能体清单（agent inventory）",
        "智能体注册表（agent registry）",
        "身份（Identity）",
        "生命周期（Lifecycle）",
        "能力（Capabilities）",
        "运行时责任归属（Runtime ownership）",
        "暂停运行（paused runs）",
        "后台运行（background runs）",
        "能力会话（capability sessions）",
        "证据链接（Evidence links）",
        "验证器/评测证据（verifier/eval evidence）",
        "验证器契约（verifier contracts）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "智能体蔓延”（`agent sprawl`）",
        "`agent inventory`（智能体清单）",
        "`agent registry`（智能体注册表）",
        "**Identity：**",
        "**Lifecycle：**",
        "**Capabilities：**",
        "**Runtime ownership：** 谁负责 paused runs、background runs 和 capability sessions",
        "**Evidence links：** 可观测性状态、verifier/eval evidence",
        "智能体注册表（`agent registry`）",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chapter_27_chinese_registry_contract_labels_are_localized() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-27.zh.md")
    expected_markers = (
        "智能体身份（agent identity）",
        "负责人（owner）",
        "生命周期状态（lifecycle state）",
        "能力（capabilities）",
        "运行时控制责任归属（runtime-control ownership）",
        "证据链接（evidence links）",
        "问责层（accountability layer）",
        "清单表格（inventory spreadsheet）",
        "发现（discovery）",
        "生产智能体（production agent）",
        "责任归属（ownership）",
        "策略链接（policy linkage）",
        "可观测的控制状态（observable control status）",
        "基础设施清单（infrastructure inventory）",
        "智能体风险指南（agentic-risk guidance）",
        "持续资产覆盖（continuous asset coverage）",
        "控制问责（control accountability）",
        "问责（accountability）",
        "注册表记录（registry records）",
        "生命周期工件（lifecycle artifacts）",
        "策略包（policy bundles）",
        "审批模式（approval modes）",
        "主体状态（principal status）",
        "遥测覆盖（telemetry coverage）",
        "智能体群体（agent estate）",
        "可问责的生产实体（accountable production entity）",
        "已批准生产智能体（approved production agents）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "agent identity、owner、lifecycle state",
        "capabilities、runtime-control ownership 与 evidence links",
        "本章应该被读成 accountability layer",
        "而不是 inventory spreadsheet",
        "治理不只是 discovery；每个 production agent",
        "需要 ownership、lifecycle state、policy linkage 与 observable control status",
        "infrastructure inventory 与 agentic-risk guidance",
        "continuous asset coverage、ownership 和 control accountability",
        "连接到 accountability，否则",
        "registry records、lifecycle artifacts、policy bundles、approval modes",
        "principal status 与 telemetry coverage 让 agent estate",
        "registry 是收束层",
        "一个 accountable production entity",
        "approved production agents 的区别不应消失",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_book_improvement_blueprint_records_review_remediation_status() -> None:
    required_markers = (
        "Implementation status, 20 May 2026",
        "P0:",
        "P1:",
        "P2:",
        "P3:",
        "draft-localization status",
        "MCP threat model",
        "trace schema",
        "eval schema",
        "memory/retrieval schema",
        "three canonical case spines",
        "print-friendly",
        "publisher packet is drafted and internally gated",
        "packet TOC section",
        "20 May 2026 public-link record",
        "Still blocked before external submission",
    )

    _assert_files_contain_all(("docs/book-improvement-blueprint.md",), required_markers)
    text = _read("docs/book-improvement-blueprint.md")
    assert "publisher-ready TOC" not in text
    assert "publisher-ready table of contents" not in text


def test_publisher_packet_has_core_positioning_and_companion_boundary() -> None:
    required_markers = (
        "Publisher Packet Draft",
        "Positioning",
        "One-Page Positioning Memo Draft",
        "Print Manuscript Shape",
        "Online Companion Boundary",
        "- **Working title:** Secure AI Agent Architecture.",
        "**Subtitle:** From prompt demos to governed production systems.",
        "**Primary reader:**",
        "**Unique promise:**",
        "**Companion assets:**",
        (
            "keep schemas, runtime command details, long checklists, and source catalogs "
            "in the online companion."
        ),
        "runnable `agent_runtime_ref` package",
        "command-output field lists and validation-error catalogs",
        "print sample that depends on live site navigation",
    )

    _assert_files_contain_all(("docs/publisher-ready-toc.md",), required_markers)


def test_publisher_packet_positioning_memo_is_print_friendly() -> None:
    text = _read("docs/publisher-ready-toc.md")
    opening_section = text.split("## Positioning", 1)[0]
    positioning_section = text.split("## Positioning", 1)[1].split(
        "## Print Manuscript Shape",
        1,
    )[0]
    required_opening_markers = (
        "- keep the book-shaped manuscript, sample strategy, positioning, and cover note together;",
        "- keep the comparable shelf and companion links in the same packet artifact.",
    )
    forbidden_inline_markers = (
        "Purpose: keep publisher-facing packet notes separate",
        (
            "keep the book-shaped manuscript, sample strategy, positioning, "
            "cover note, comparable shelf"
        ),
        "Reader: senior product engineers",
        "senior product engineers, platform engineers, security engineers, staff engineers",
        "Promise: explain how to move from prompt demos",
        "**Primary reader:** platform and product architects",
        (
            "systems that can read private context, call tools, request approvals, "
            "write to external systems"
        ),
        "**Problem:** most teams can build",
        "**Unique promise:** the book treats agents as production systems:",
        "**Competing shelf:** cloud architecture",
        "**Manuscript status:** public open manuscript",
        "**Companion assets:** reference runtime",
    )

    for marker in required_opening_markers:
        assert marker in opening_section
    for marker in forbidden_inline_markers:
        assert marker not in opening_section
        assert marker not in positioning_section
    assert opening_section.count("\n- ") >= 4
    assert (
        "- **Reader:** senior product engineers, platform engineers, and security engineers."
        in positioning_section
    )
    assert "- **Reader extension:** staff engineers and technical leads." in positioning_section
    assert (
        "- systems that can read private context, call tools, and request approvals;"
        in positioning_section
    )
    assert (
        "- systems that can write to external systems and survive incidents."
        in positioning_section
    )
    assert (
        "- those workflows now carry real permissions and long-running state;"
        in positioning_section
    )
    assert (
        "- they also carry delegated work and regulated evidence needs."
        in positioning_section
    )
    assert (
        "- those workflows now carry real permissions, long-running state, delegated work, "
        "and regulated evidence needs."
        not in positioning_section
    )
    assert positioning_section.count("\n- ") >= 33
    assert all(len(line) <= 120 for line in opening_section.splitlines())
    assert all(len(line) <= 110 for line in positioning_section.splitlines())


def test_publisher_packet_manuscript_shape_boundary_is_print_friendly() -> None:
    text = _read("docs/publisher-ready-toc.md")
    section = text.split("## Print Manuscript Shape", 1)[1].split(
        "## Sample Chapter Candidates",
        1,
    )[0]
    required_markers = (
        "Target:",
        "- 6 parts;",
        "- about 20 chapters;",
        (
            "- keep schemas, runtime command details, long checklists, "
            "and source catalogs in the online companion."
        ),
        "Online Companion Boundary",
        (
            "- schema appendices for traces, eval datasets, approvals, memory, "
            "and lifecycle artifacts;"
        ),
        "- schema appendices for incident records, rollout gates, and policy bundles;",
    )
    forbidden_inline_markers = (
        "Target: 6 parts, about 20 chapters.",
        (
            "schema appendices for traces, eval datasets, approvals, memory, "
            "lifecycle artifacts, incident records"
        ),
    )

    for marker in required_markers:
        assert marker in section
    for marker in forbidden_inline_markers:
        assert marker not in section
    assert section.count("\n- ") >= 9
    assert all(len(line) <= 135 for line in section.splitlines())



def test_publisher_packet_sample_candidates_are_print_friendly() -> None:
    text = _read("docs/publisher-ready-toc.md")
    section = text.split("## Sample Chapter Candidates", 1)[1].split(
        "## Sample Chapter Export Manifest Draft",
        1,
    )[0]
    required_markers = (
        "### Chapter 1 — strongest publisher sample",
        "Why:",
        "- carries the thesis;",
        "- starts from a failure story;",
        "- shows how the book differs from prompt-hype or framework documentation.",
        "### Chapter 13 — strongest technical credibility sample",
        "- includes a Support triage duplicate-ticket example;",
        (
            "- follows it from trace to verifier attribution, regression gate, "
            "rollout owner action, and release judgment;"
        ),
    )
    forbidden_inline_markers = (
        "Why: it carries the thesis, starts from a failure story",
        "Why: evals, traces, failure attribution, regression gates",
        "includes a Support triage duplicate-ticket example from trace to verifier attribution",
    )

    for marker in required_markers:
        assert marker in section
    for marker in forbidden_inline_markers:
        assert marker not in section
    assert section.count("\n- ") >= 19
    assert all(len(line) <= 135 for line in section.splitlines())



def test_publisher_packet_has_blocker_waiver_decision_log() -> None:
    required_markers = (
        "Blocker Waiver / Decision Log Draft",
        "Print-friendly waiver log starter",
        "no waivers yet",
        "all four blockers remain open",
        "Waiver rules",
        "named decider",
        "date",
        "scope",
        "follow-up owner",
        "No-go signals",
        "governed-systems positioning",
    )

    _assert_files_contain_all(("docs/publisher-ready-toc.md",), required_markers)


def test_publisher_packet_has_external_submission_blocker_register() -> None:
    required_markers = (
        "External Submission Blocker Register",
        "Still blocked before external submission",
        "Print-friendly blocker list",
        "not externally sendable",
        "Author bio and credential framing",
        "Independent sample copy-edit",
        "Sample selection",
        "Target editor / imprint formatting",
        "Owner/input needed",
        "Packet action when closed",
        "author explicitly waives",
    )

    _assert_files_contain_all(("docs/publisher-ready-toc.md",), required_markers)


def test_publisher_packet_blocker_sections_are_print_friendly() -> None:
    text = _read("docs/publisher-ready-toc.md")
    blocker_section = text.split("## External Submission Blocker Register", 1)[1].split(
        "## Blocker Waiver / Decision Log Draft",
        1,
    )[0]
    waiver_section = text.split("## Blocker Waiver / Decision Log Draft", 1)[1]
    forbidden_inline_labels = (
        "current state: open; Owner/input needed:",
        "current state: default chosen, not target-specific; Owner/input needed:",
        "**Date:** TBD; **decision:** no waivers yet;",
        "**Waiver rules:** every waiver needs",
        "**No-go signals:** anonymous waiver",
    )

    assert "|" not in blocker_section
    assert "|" not in waiver_section
    assert blocker_section.count("- **") >= 4
    assert blocker_section.count("  - Current state:") == 4
    assert blocker_section.count("  - Owner/input needed:") == 4
    assert blocker_section.count("  - Packet action when closed:") == 4
    assert "  - Scope options: Chapter 1 only, or Chapter 1 plus Chapter 13." in blocker_section
    assert "confirms Chapter 1 only vs Chapter 1 plus Chapter 13" not in blocker_section
    assert (
        "**Submission state:** not externally sendable until all four blockers are closed."
        in blocker_section
    )
    assert "author explicitly waives the remaining blockers." in blocker_section
    assert "until all four blockers are closed or explicitly waived" not in blocker_section
    assert waiver_section.count("- **") >= 6
    for marker in forbidden_inline_labels:
        assert marker not in blocker_section
        assert marker not in waiver_section
    assert all(len(line) <= 110 for line in blocker_section.splitlines())
    assert all(len(line) <= 135 for line in waiver_section.splitlines())


def test_publisher_packet_has_sample_copy_edit_handoff_brief() -> None:
    required_markers = (
        "Sample Copy-Edit Handoff Brief Draft",
        "Copy-edit scope",
        "- sentence flow;",
        "- opening hook;",
        "- paragraph cadence;",
        "Do not rewrite",
        "workflow-first / governed-systems thesis",
        "Questions for the editor",
        "Return format",
        "top 5 changes",
        "No-go signals",
    )

    _assert_files_contain_all(("docs/publisher-ready-toc.md",), required_markers)


def test_publisher_packet_copy_edit_handoff_is_print_friendly() -> None:
    text = _read("docs/publisher-ready-toc.md")
    section = text.split("## Sample Copy-Edit Handoff Brief Draft", 1)[1].split(
        "## Editorial Compression Rules",
        1,
    )[0]
    forbidden_inline_labels = (
        "**Copy-edit scope:** sentence flow",
        "**Do not rewrite:** technical claims",
        "**Questions for the editor:** where does",
        "**Return format:** annotated sample",
        "**No-go signals:** copy edits",
    )

    for marker in forbidden_inline_labels:
        assert marker not in section
    assert "Use this brief when handing Chapter 1 to an independent copy editor" in section
    assert "Include Chapter 13 only if the packet needs a second technical sample." in section
    assert (
        "Use this brief when handing Chapter 1, and optionally Chapter 13, "
        "to an independent copy editor"
        not in section
    )
    assert (
        "- consistency of `agent`, `workflow`, `runtime`, `policy`, and `approval` terms;"
        in section
    )
    assert "- consistency of `trace`, `eval`, and `governance` terms;" in section
    assert "`approval`, `trace`, `eval`, and `governance` terms" not in section
    assert section.count("\n- ") >= 25
    assert all(len(line) <= 110 for line in section.splitlines())


def test_publisher_packet_editorial_compression_rules_are_print_friendly() -> None:
    text = _read("docs/publisher-ready-toc.md")
    section = text.split("## Editorial Compression Rules", 1)[1].split(
        "## Author / Platform Credibility Note Draft",
        1,
    )[0]
    required_markers = (
        "- Use Support triage as the primary running case.",
        "- Use Internal knowledge assistant and Incident coordination as secondary contrast cases.",
        "- End chapters with what to remember and common failure modes.",
        "- Also end with design-review use, companion assets, and the next chapter.",
    )
    forbidden_inline_markers = (
        "Use Support triage as the primary running case; use Internal knowledge assistant",
        (
            "- End chapters with: what to remember, common failure modes, "
            "design-review use, companion assets, and next chapter."
        ),
    )

    for marker in required_markers:
        assert marker in section
    for marker in forbidden_inline_markers:
        assert marker not in section
    assert section.count("\n- ") >= 7
    assert all(len(line) <= 135 for line in section.splitlines())



def test_publisher_packet_has_public_link_availability_record() -> None:
    required_markers = (
        "Public Link Availability Record",
        "Last checked: **2026-05-20**",
        "publisher-packet-2026-05",
        "Checked links:",
        "- public book site;",
        "- English landing page;",
        "- Chinese landing page;",
        "- Chapter 1 sample;",
        "- Chapter 13 technical sample;",
        "- reference runtime source;",
        "- runtime README;",
        "- runtime configs;",
        "- runtime tests.",
        "HTTP 200",
        "all nine checked public links",
        "2026-05-20",
    )

    _assert_files_contain_all(("docs/publisher-ready-toc.md",), required_markers)


def test_publisher_packet_public_links_are_print_friendly() -> None:
    text = _read("docs/publisher-ready-toc.md")
    section = text.split("## Public Links Draft", 1)[1].split(
        "## Public Link Availability Record",
        1,
    )[0]

    assert "Pitch usage:" in section
    assert "Pitch usage: send the public site" not in section
    assert "- send the public site and the two sample chapters first;" in section
    assert "- keep the source/runtime/test links as proof points;" in section
    assert "- use those proof points for editors who want to verify" in section
    assert "- **Runnable reference package README:**\n" in section
    assert "**Runnable reference package README:** <https://" not in section
    assert section.count("\n- ") >= 12
    assert section.count("\n  - ") >= 1
    assert all(len(line) <= 120 for line in section.splitlines())


def test_publisher_packet_public_link_record_is_print_friendly() -> None:
    text = _read("docs/publisher-ready-toc.md")
    section = text.split("## Public Link Availability Record", 1)[1].split(
        "## Pitch Packet Checklist",
        1,
    )[0]

    assert "Checked links: public book site," not in section
    assert "Before external submission, rerun the check." in section
    assert "Update this record if any URL, branch, or packet version changes." in section
    assert "rerun the check and update this record" not in section
    assert section.count("\n- ") == 9
    assert all(len(line) <= 110 for line in section.splitlines())


def test_publisher_packet_cover_note_is_print_friendly() -> None:
    text = _read("docs/publisher-ready-toc.md")
    section = text.split("## Cover Note Draft", 1)[1].split(
        "## Target Editor / Imprint Formatting Brief Draft",
        1,
    )[0]
    required_markers = (
        "Dear [Editor]",
        "I am preparing **Secure AI Agent Architecture**",
        "The book is for teams that need to ship AI agents",
        "The premise is that production agents should be treated as governed systems",
        "Identity, policy, tools, memory, and traces become explicit engineering contracts.",
        "So do eval gates, rollout, and retirement.",
        "Chapter 13 is available as a secondary technical sample",
        "It shows the eval and release-gate treatment.",
        "Before sending:",
        "- replace the greeting;",
        "- add the final author bio/credential sentence;",
        "- tailor the final paragraph to the target editor or imprint.",
    )
    forbidden_inline_markers = (
        "who need to ship AI agents with real tool access, memory, approvals",
        "The book's premise is that production agents should be treated",
        (
            "The manuscript is paired with a public multilingual companion site "
            "and runnable reference material, so"
        ),
        "Before sending, replace the greeting",
        "platform engineers, product engineers,",
        "approvals, observability, evals,",
        "traces, eval gates, rollout, and retirement become explicit engineering contracts",
        "if you would like to see the eval and release-gate treatment",
        "sample chapter, and companion links",
        "publisher-ready table of contents",
    )

    assert "positioning memo, publisher packet, and sample chapter" in section
    for marker in required_markers:
        assert marker in section
    for marker in forbidden_inline_markers:
        assert marker not in section
    assert section.count("\n> ") >= 16
    assert section.count("\n- ") == 3
    assert all(len(line) <= 110 for line in section.splitlines())



def test_publisher_packet_has_target_editor_formatting_brief() -> None:
    required_markers = (
        "Target Editor / Imprint Formatting Brief Draft",
        "Inputs to collect",
        "- editor name;",
        "- imprint;",
        "- submission channel;",
        "- attachment rules;",
        "- sample-chapter policy;",
        "Formatting decisions",
        "publisher-packet-2026-05",
        "secure-ai-agent-architecture-proposal-publisher-packet-2026-05.pdf",
        "Tailoring rules",
        "No-go signals",
    )

    _assert_files_contain_all(("docs/publisher-ready-toc.md",), required_markers)


def test_publisher_packet_target_editor_brief_is_print_friendly() -> None:
    text = _read("docs/publisher-ready-toc.md")
    section = text.split("## Target Editor / Imprint Formatting Brief Draft", 1)[1].split(
        "## Recommended Submission Packet Order",
        1,
    )[0]
    forbidden_inline_labels = (
        "**Inputs to collect:** editor name",
        "**Formatting decisions:** choose whether",
        "**Tailoring rules:** keep the title",
        "**No-go signals:** unknown editor name",
    )

    for marker in forbidden_inline_labels:
        assert marker not in section
    assert section.count("\n- ") >= 25
    assert all(len(line) <= 130 for line in section.splitlines())


def test_publisher_packet_author_platform_note_is_print_friendly() -> None:
    text = _read("docs/publisher-ready-toc.md")
    section = text.split("## Author / Platform Credibility Note Draft", 1)[1].split(
        "## Author Bio Input Brief Draft",
        1,
    )[0]
    required_markers = (
        "Project platform:",
        "- public multilingual book site;",
        "- runnable reference runtime;",
        "- configuration examples;",
        "Claim supported by those artifacts:",
        "- production AI agents should be designed as governed systems, not as prompt demos.",
        "- the companion material includes runnable/reference artifacts;",
        "- readers can inspect the contracts behind the prose;",
        "- the book is written for practitioners who need to ship and operate agents;",
        "- it is not only for readers who want to understand model behavior in the abstract;",
        "Bio gap to fill before submission:",
        "- add a short human author bio with role;",
    )
    forbidden_inline_markers = (
        "Use this as a conservative draft until the final bio is written:",
        "The project already has more than a manuscript outline:",
        "the companion material includes runnable/reference artifacts, so readers can inspect",
        "not only understand model behavior in the abstract",
        "Bio gap to fill before submission: add a short human author bio",
    )

    for marker in required_markers:
        assert marker in section
    for marker in forbidden_inline_markers:
        assert marker not in section
    assert section.count("\n- ") >= 11
    assert all(len(line) <= 135 for line in section.splitlines())



def test_publisher_packet_has_author_bio_input_brief() -> None:
    required_markers = (
        "Author Bio Input Brief Draft",
        "Before this packet becomes external email copy, collect the human-authored facts.",
        "Do not let the manuscript artifact invent those facts.",
        "Required inputs",
        "- preferred author name;",
        "production/engineering background",
        "public project links",
        "Tone constraints",
        "- avoid inflated authority claims;",
        "- prefer concrete artifact-backed credibility;",
        "useful credibility artifacts: public book site",
        "useful supporting artifacts: tests, schemas, and companion material.",
        "Bio slots to prepare",
        "- 50-word short bio;",
        "- 100-word proposal bio;",
        "No-go signals",
    )

    _assert_files_contain_all(("docs/publisher-ready-toc.md",), required_markers)


def test_publisher_packet_author_bio_brief_is_print_friendly() -> None:
    text = _read("docs/publisher-ready-toc.md")
    section = text.split("## Author Bio Input Brief Draft", 1)[1].split(
        "## Comparable Books Draft",
        1,
    )[0]
    forbidden_inline_labels = (
        (
            "Before this packet becomes external email copy, collect the "
            "human-authored facts that should not be invented"
        ),
        "**Required inputs:** preferred author name",
        "**Optional inputs:** prior books",
        "prefer concrete artifact-backed credibility: public book site",
        "**Tone constraints:** avoid inflated",
        "**Bio slots to prepare:** one-line byline",
        "**No-go signals:** missing preferred name",
    )

    for marker in forbidden_inline_labels:
        assert marker not in section
    assert "runnable reference runtime, tests, schemas" not in section
    assert section.count("\n- ") >= 25
    assert all(len(line) <= 110 for line in section.splitlines())


def test_publisher_packet_comparable_books_are_print_friendly() -> None:
    text = _read("docs/publisher-ready-toc.md")
    section = text.split("## Comparable Books Draft", 1)[1].split(
        "## Print Manuscript vs Online Companion Draft",
        1,
    )[0]
    required_markers = (
        "**Designing Data-Intensive Applications**",
        "Comparable angle: systems-thinking discipline.",
        "Difference: applies that operational seriousness",
        "**Designing Machine Learning Systems**",
        "Comparable angle: production ML framing.",
        "**AI Engineering**",
        "**Building Secure & Reliable Systems**",
        "**Site Reliability Engineering**",
        "Short differentiation:",
        "- narrower shelf claim: architect production AI agents as governed systems;",
        (
            "- key controls: explicit rights, evidence, side-effect control, "
            "eval gates, and lifecycle ownership."
        ),
    )
    forbidden_inline_markers = (
        "— comparable in systems-thinking discipline;",
        "— comparable in production ML framing;",
        "Short differentiation: the book is not trying",
    )

    for marker in required_markers:
        assert marker in section
    for marker in forbidden_inline_markers:
        assert marker not in section
    assert "runtime control." in section
    assert "approvals, evals, and observability." in section
    assert "rollout gates, and runtime control" not in section
    assert "trust boundaries, approvals, evals, and observability" not in section
    assert section.count("\n  - Comparable angle:") == 5
    assert section.count("\n  - Difference:") == 7
    assert all(len(line) <= 110 for line in section.splitlines())



def test_publisher_packet_print_companion_split_is_print_friendly() -> None:
    text = _read("docs/publisher-ready-toc.md")
    section = text.split("## Print Manuscript vs Online Companion Draft", 1)[1].split(
        "## Public Links Draft",
        1,
    )[0]
    required_markers = (
        "Print manuscript:",
        "Online companion:",
        "Practical pitch line:",
        "- keeps long field lists and exhaustive schemas out of the main reading path;",
        "- keeps fast-moving implementation details in the companion;",
        "- uses Support triage as the primary through-line;",
        "- uses Internal knowledge assistant and Incident coordination as contrast cases.",
        "- the book should read cleanly in print;",
        (
            "- the companion site proves that the architecture is concrete enough "
            "to run, test, and inspect."
        ),
    )
    forbidden_inline_markers = (
        "Practical pitch line: the book should read cleanly in print",
        "uses Support triage as the primary through-line, with Internal knowledge assistant",
        "long field lists, exhaustive schemas, and fast-moving implementation details",
        "while the companion site proves",
    )

    for marker in required_markers:
        assert marker in section
    for marker in forbidden_inline_markers:
        assert marker not in section
    assert section.count("\n- ") >= 10
    assert all(len(line) <= 110 for line in section.splitlines())



def test_publisher_packet_has_sample_chapter_export_manifest() -> None:
    required_markers = (
        "Sample Chapter Export Manifest Draft",
        "Use this manifest when assembling the first external packet.",
        "It keeps the sample reproducible and prevents companion-link drift.",
        "Primary sample",
        "role: Chapter 1 as the first editorial sample",
        "source path: `docs/book/part-i/chapter-1.en.md`",
        "https://agent-axiom.github.io/agent-arch/en/book/part-i/chapter-1/",
        "Secondary technical sample",
        "role: Chapter 13 as the technical credibility sample",
        "source path: `docs/book/part-v/chapter-13.en.md`",
        "https://agent-axiom.github.io/agent-arch/en/book/part-v/chapter-13/",
        "publisher-packet-2026-05",
        "Export metadata to include",
        "Pre-export checks",
        "technical-credibility reason",
    )

    _assert_files_contain_all(("docs/publisher-ready-toc.md",), required_markers)


def test_publisher_packet_sample_export_manifest_is_print_friendly() -> None:
    text = _read("docs/publisher-ready-toc.md")
    section = text.split("## Sample Chapter Export Manifest Draft", 1)[1].split(
        "## Sample Copy-Edit Handoff Brief Draft",
        1,
    )[0]

    forbidden_inline_labels = (
        (
            "Use this manifest when assembling the first external packet so "
            "the sample is reproducible"
        ),
        "**Primary sample:** Chapter 1",
        "**Secondary technical sample:** Chapter 13,",
        "**Export metadata to include:** title, subtitle",
        "**Pre-export checks:** selected sample",
        "**No-go signals:** stale public URL",
    )

    for marker in forbidden_inline_labels:
        assert marker not in section
    assert section.count("\n- ") >= 20
    assert all(len(line) <= 130 for line in section.splitlines())


def test_publisher_packet_submission_order_is_print_friendly() -> None:
    text = _read("docs/publisher-ready-toc.md")
    section = text.split("## Recommended Submission Packet Order", 1)[1].split(
        "## Print/PDF Readiness Gate Draft",
        1,
    )[0]
    required_markers = (
        "Default recommendation:",
        "3. publisher packet table-of-contents section;",
        "- lead with Chapter 1 only;",
        "- use it because it carries the thesis and reads best as a first editorial sample;",
        "- keep Chapter 13 ready as a second attachment or follow-up;",
        "- send Chapter 13 when the conversation turns to technical credibility.",
    )
    forbidden_inline_markers = (
        "Default recommendation: lead with Chapter 1 only.",
        "Keep Chapter 13 ready as a second attachment or follow-up",
        "publisher-ready table of contents",
    )

    for marker in required_markers:
        assert marker in section
    for marker in forbidden_inline_markers:
        assert marker not in section
    assert section.count("\n- ") >= 4
    assert all(len(line) <= 110 for line in section.splitlines())



def test_publisher_packet_has_print_pdf_readiness_gate() -> None:
    required_markers = (
        "Print/PDF Readiness Gate Draft",
        "Print/PDF checks",
        "stable heading hierarchy",
        "page breaks",
        "code-block wrapping",
        "readable in grayscale",
        "online companion",
        "packet version",
        "sample-chapter date",
        "clipped code blocks",
        "live site navigation",
    )

    _assert_files_contain_all(("docs/publisher-ready-toc.md",), required_markers)


def test_publisher_packet_print_pdf_gate_is_print_friendly() -> None:
    text = _read("docs/publisher-ready-toc.md")
    section = text.split("## Print/PDF Readiness Gate Draft", 1)[1].split(
        "## Submission Release Discipline Draft",
        1,
    )[0]
    forbidden_inline_markers = (
        "**No-go signals:** broken heading levels",
        "URLs are visible enough for print readers, while companion-only links",
        "long schema tables, command-output field lists, validation-error catalogs",
        "or any print sample that depends on live site navigation",
    )

    for marker in forbidden_inline_markers:
        assert marker not in section
    assert "run a print-friction pass." in section
    assert "run a separate pass for print friction" not in section
    assert "**No-go signals:**\n" in section
    assert "- URLs are visible enough for print readers;" in section
    assert "- companion-only links are grouped instead of scattered through the prose;" in section
    assert (
        "- long schema tables and command-output field lists stay in the online companion;"
        in section
    )
    assert (
        "- validation-error catalogs and runtime internals stay in the online companion;"
        in section
    )
    assert section.count("\n- ") >= 14
    assert all(len(line) <= 110 for line in section.splitlines())



def test_publisher_packet_has_submission_release_discipline() -> None:
    required_markers = (
        "Submission Release Discipline Draft",
        "publisher-packet-2026-05",
        "Freeze scope before sending",
        "Pre-send gates",
        "fresh checks",
        "draft localization preview",
        "No-go signals",
    )

    _assert_files_contain_all(("docs/publisher-ready-toc.md",), required_markers)


def test_publisher_packet_submission_release_scope_is_print_friendly() -> None:
    text = _read("docs/publisher-ready-toc.md")
    section = text.split("## Submission Release Discipline Draft", 1)[1].split(
        "## External Submission Blocker Register",
        1,
    )[0]
    required_markers = (
        "**Freeze scope before sending:**",
        "- cover note;",
        "- one-page positioning memo;",
        "- publisher packet TOC section;",
        "- selected sample chapter;",
        "- author/platform credibility note;",
        "- comparable-books note;",
        "- print/companion split;",
        "- public links.",
    )
    forbidden_inline_markers = (
        "**Freeze scope before sending:** cover note",
        "- publisher-ready TOC;",
        "publisher-ready table of contents",
        "author/platform credibility note, comparable-books note",
        (
            "public site, sample-chapter links, repository links, runtime links, "
            "and test links have passed a fresh availability check"
        ),
        "no runtime internals, validation-error catalogs, or long schema tables are moved",
    )

    for marker in required_markers:
        assert marker in section
    for marker in forbidden_inline_markers:
        assert marker not in section
    assert "**No-go signals:**\n" in section
    assert "**No-go signals:** missing author bio" not in section
    assert (
        "- no runtime internals or validation-error catalogs are moved into "
        "the print manuscript packet"
    ) in section
    assert (
        "- no long schema tables are moved into the print manuscript packet by accident."
        in section
    )
    assert all(len(line) <= 110 for line in section.splitlines())


def test_publisher_packet_all_lines_are_print_export_friendly() -> None:
    text = _read("docs/publisher-ready-toc.md")
    overlong_lines = [
        (line_number, len(line), line)
        for line_number, line in enumerate(text.splitlines(), start=1)
        if len(line) > 110
    ]

    assert "- this publisher packet;" in text
    assert "publisher packet table-of-contents section" in text
    assert "publisher packet TOC section" in text
    assert "publisher-ready table of contents" not in text
    assert "publisher-ready TOC" not in text
    assert overlong_lines == []



def test_chapter_17_policy_catalog_threads_three_canonical_cases() -> None:
    markers_by_file = {
        "docs/book/part-vii/chapter-17.md": (
            "Заметка о сквозных сценариях слоя политик",
            "Разбор обращений поддержки",
            "Внутренний ассистент знаний",
            "Координация инцидентов",
            "пишущих возможностей",
            "требований подтверждения",
            "читающих возможностей",
            "границ корпуса",
            "прав записи в память",
            "аварийных переопределений политик",
        ),
        "docs/book/part-vii/chapter-17.en.md": (
            "Policy case-spine note",
            "Support triage",
            "Internal knowledge assistant",
            "Incident coordination",
            "write capabilities",
            "approval requirements",
            "read capabilities",
            "corpus scope",
            "memory-write permissions",
            "emergency-only policy overrides",
        ),
        "docs/book/part-vii/chapter-17.zh.md": (
            "Policy case-spine note",
            "Support triage",
            "Internal knowledge assistant",
            "Incident coordination",
            "write capabilities",
            "approval requirements",
            "read capabilities",
            "corpus scope",
            "memory-write permissions",
            "emergency-only policy overrides",
        ),
    }

    for path, required_markers in markers_by_file.items():
        text = _read(path)
        for required_marker in required_markers:
            assert required_marker in text, (path, required_marker)


def test_chapter_17_policy_catalog_zh_refs_are_localized() -> None:
    text = _read("docs/book/part-vii/chapter-17.zh.md")

    expected_snippets = (
        "[策略包模式与审批契约](../../appendix/policy-bundle-schema.zh.md)",
        "[审批请求与决策记录模式](../../appendix/approval-schema.zh.md)",
        "[生命周期工件模式](../../appendix/lifecycle-artifact-schema.zh.md)",
    )
    forbidden_snippets = (
        "Policy Bundle Schema 与 Approval Contract",
        "Approval Request 与 Decision Record Schema",
        "Lifecycle Artifact Schema",
    )

    for expected_snippet in expected_snippets:
        assert expected_snippet in text, expected_snippet
    for forbidden_snippet in forbidden_snippets:
        assert forbidden_snippet not in text, forbidden_snippet


def test_chapter_8_execution_layer_threads_three_canonical_cases() -> None:
    required_markers = (
        "Execution case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "read tools",
        "write tools",
        "approval handoff",
        "idempotency keys",
        "retrieval tools",
        "corpus filters",
        "responder-role checks",
        "timeout paths",
    )
    checked_files = (
        "docs/book/part-iv/chapter-8.md",
        "docs/book/part-iv/chapter-8.en.md",
        "docs/book/part-iv/chapter-8.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_chapter_9_sandbox_mcp_threads_three_canonical_cases() -> None:
    required_markers = (
        "Sandbox/MCP case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "sandbox limits",
        "approval-aware MCP tools",
        "reconciliation path",
        "read-only MCP resources",
        "corpus-scoped network access",
        "source validation",
        "responder-role enforcement",
        "audit trail",
    )
    checked_files = (
        "docs/book/part-iv/chapter-9.md",
        "docs/book/part-iv/chapter-9.en.md",
        "docs/book/part-iv/chapter-9.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_chapter_10_reliability_threads_three_canonical_cases() -> None:
    required_markers = (
        "Reliability case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "idempotency keys",
        "duplicate-ticket detection",
        "reconciliation",
        "retrieval fan-out",
        "freshness backoff",
        "stale memory writes",
        "notification throttling",
        "side_effect_unknown",
    )
    checked_files = (
        "docs/book/part-iv/chapter-10.md",
        "docs/book/part-iv/chapter-10.en.md",
        "docs/book/part-iv/chapter-10.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_chapter_10_recovery_branches_link_to_eval_schema() -> None:
    expected_links_by_file = {
        "docs/book/part-iv/chapter-10.md": "../../appendix/eval-schema.md",
        "docs/book/part-iv/chapter-10.en.md": "../../appendix/eval-schema.en.md",
        "docs/book/part-iv/chapter-10.zh.md": "../../appendix/eval-schema.zh.md",
    }

    for path, expected_link in expected_links_by_file.items():
        text = _read(path)
        assert f"]({expected_link})" in text, (path, expected_link)

    chinese_text = _read("docs/book/part-iv/chapter-10.zh.md")
    assert "[评测模式（eval schema）](../../appendix/eval-schema.zh.md)" in chinese_text
    assert "[eval schema](../../appendix/eval-schema.zh.md)" not in chinese_text


def test_chapter_11_traces_thread_three_canonical_cases() -> None:
    required_markers = (
        "Trace case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "tool spans",
        "approval status",
        "idempotency_key",
        "retrieval spans",
        "source identifiers",
        "freshness markers",
        "memory-write events",
        "verifier evidence",
        "incident-state events",
    )
    checked_files = (
        "docs/book/part-v/chapter-11.md",
        "docs/book/part-v/chapter-11.en.md",
        "docs/book/part-v/chapter-11.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_chapter_11_trace_verifier_evidence_eval_link_is_clickable() -> None:
    expected_links_by_file = {
        "docs/book/part-v/chapter-11.md": "../../appendix/eval-schema.md",
        "docs/book/part-v/chapter-11.en.md": "../../appendix/eval-schema.en.md",
        "docs/book/part-v/chapter-11.zh.md": "../../appendix/eval-schema.zh.md",
    }

    for path, expected_link in expected_links_by_file.items():
        assert f"]({expected_link})" in _read(path), (path, expected_link)


def test_chapter_11_practical_rules_link_verifier_evidence() -> None:
    expected_snippets_by_file = {
        "docs/book/part-v/chapter-11.md": (
            "явную связь с [verifier evidence](../../appendix/eval-schema.md)"
        ),
        "docs/book/part-v/chapter-11.en.md": (
            "explicit linkage to [verifier evidence](../../appendix/eval-schema.en.md)"
        ),
        "docs/book/part-v/chapter-11.zh.md": (
            "指向[验证器证据（verifier evidence）](../../appendix/eval-schema.zh.md)的显式链接"
        ),
    }

    for path, expected_snippet in expected_snippets_by_file.items():
        _assert_file_contains(path, expected_snippet)


def test_chapter_11_evidence_refs_link_verifier_evidence() -> None:
    expected_snippets_by_file = {
        "docs/book/part-v/chapter-11.md": (
            "заново собирать [verifier evidence](../../appendix/eval-schema.md)"
        ),
        "docs/book/part-v/chapter-11.en.md": (
            "reconstruct [verifier evidence](../../appendix/eval-schema.en.md)"
        ),
        "docs/book/part-v/chapter-11.zh.md": (
            "重建[验证器证据（verifier evidence）](../../appendix/eval-schema.zh.md)"
        ),
    }

    for path, expected_snippet in expected_snippets_by_file.items():
        _assert_file_contains(path, expected_snippet)


def test_chapter_12_slo_threads_three_canonical_cases() -> None:
    required_markers = (
        "SLO case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "health budgets",
        "duplicate-ticket rate",
        "approval latency",
        "side_effect_unknown",
        "retrieval freshness",
        "source-grounding success",
        "access-control denials",
        "responder handoff latency",
    )
    checked_files = (
        "docs/book/part-v/chapter-12.md",
        "docs/book/part-v/chapter-12.en.md",
        "docs/book/part-v/chapter-12.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_chapter_12_slo_zh_refs_are_localized() -> None:
    text = _read("docs/book/part-v/chapter-12.zh.md")

    expected_snippets = (
        "[追踪模式与事件目录](../../appendix/trace-schema.zh.md)",
        "[事故记录模式](../../appendix/incident-record-schema.zh.md)",
        "[变更评审与发布门禁模式]"
        "(../../appendix/change-rollout-schema.zh.md)",
    )
    forbidden_snippets = (
        "需要配套的 schema 和工程工件",
        "Trace Schema 与 Event Catalog",
        "Incident Record Schema",
        "Change Review 与 Rollout Gate Schema",
    )

    for expected_snippet in expected_snippets:
        assert expected_snippet in text, expected_snippet
    for forbidden_snippet in forbidden_snippets:
        assert forbidden_snippet not in text, forbidden_snippet


def test_chapter_14_ownership_threads_three_canonical_cases() -> None:
    required_markers_by_file = {
        "docs/book/part-vi/chapter-14.md": (
            "Заметка о сквозных сценариях владения",
            "Разбор обращений поддержки",
            "Внутренний ассистент знаний",
            "Координация инцидентов",
            "разделение платформы и продуктов",
            "политикой подтверждений",
            "контрактом пишущей возможности",
            "схемой трасс",
            "владение корпусом",
            "политику извлечения",
            "правила записи в память",
            "право эскалации",
            "изменение после инцидента",
        ),
        "docs/book/part-vi/chapter-14.en.md": (
            "Ownership case-spine note",
            "Support triage",
            "Internal knowledge assistant",
            "Incident coordination",
            "platform/product split",
            "approval policy",
            "write-capability contract",
            "trace schema",
            "corpus ownership",
            "retrieval policy",
            "memory-write rules",
            "escalation authority",
            "post-incident change ownership",
        ),
        "docs/book/part-vi/chapter-14.zh.md": (
            "Ownership case-spine note",
            "Support triage",
            "Internal knowledge assistant",
            "Incident coordination",
            "platform/product split",
            "approval policy",
            "write-capability contract",
            "trace schema",
            "corpus ownership",
            "retrieval policy",
            "memory-write rules",
            "escalation authority",
            "post-incident change ownership",
        ),
    }

    for path, required_markers in required_markers_by_file.items():
        _assert_files_contain_all((path,), required_markers)


def test_chapter_14_ownership_trace_schema_link_is_clickable() -> None:
    expected_links_by_file = {
        "docs/book/part-vi/chapter-14.md": "../../appendix/trace-schema.md",
        "docs/book/part-vi/chapter-14.en.md": "../../appendix/trace-schema.en.md",
        "docs/book/part-vi/chapter-14.zh.md": "../../appendix/trace-schema.zh.md",
    }

    for path, expected_link in expected_links_by_file.items():
        assert f"]({expected_link})" in _read(path), (path, expected_link)

    chinese_text = _read("docs/book/part-vi/chapter-14.zh.md")
    assert "[追踪模式（trace schema）](../../appendix/trace-schema.zh.md)" in chinese_text
    assert "[trace schema](../../appendix/trace-schema.zh.md)" not in chinese_text


def test_chapter_15_golden_paths_thread_three_canonical_cases() -> None:
    required_markers_by_file = {
        "docs/book/part-vi/chapter-15.md": (
            "Заметка о сквозных сценариях золотого пути",
            "Разбор обращений поддержки",
            "Внутренний ассистент знаний",
            "Координация инцидентов",
            "антизоопарк-стратегия",
            "шаблон агента рабочего процесса",
            "утвержденным шлюзом записи",
            "трассировки",
            "оценки",
            "оценками дублей тикета",
            "шаблон агента знаний",
            "привязкой к источникам",
            "защитными ограничениями записи в память",
            "шаблон агента координации инцидентов",
        ),
        "docs/book/part-vi/chapter-15.en.md": (
            "Golden-path case-spine note",
            "Support triage",
            "Internal knowledge assistant",
            "Incident coordination",
            "anti-zoo strategy",
            "workflow-agent template",
            "approved write gateway",
            "trace",
            "eval",
            "duplicate-ticket evals",
            "knowledge-agent template",
            "source grounding",
            "memory-write guardrails",
            "incident-agent template",
        ),
        "docs/book/part-vi/chapter-15.zh.md": (
            "Golden-path case-spine note",
            "Support triage",
            "Internal knowledge assistant",
            "Incident coordination",
            "anti-zoo strategy",
            "workflow-agent template",
            "approved write gateway",
            "trace",
            "eval",
            "duplicate-ticket evals",
            "knowledge-agent template",
            "source grounding",
            "memory-write guardrails",
            "incident-agent template",
        ),
    }

    for path, required_markers in required_markers_by_file.items():
        _assert_files_contain_all((path,), required_markers)


def test_chapter_15_golden_path_trace_eval_links_are_clickable() -> None:
    expected_links_by_file = {
        "docs/book/part-vi/chapter-15.md": (
            "../../appendix/trace-schema.md",
            "../../appendix/eval-schema.md",
        ),
        "docs/book/part-vi/chapter-15.en.md": (
            "../../appendix/trace-schema.en.md",
            "../../appendix/eval-schema.en.md",
        ),
        "docs/book/part-vi/chapter-15.zh.md": (
            "../../appendix/trace-schema.zh.md",
            "../../appendix/eval-schema.zh.md",
        ),
    }

    for path, expected_links in expected_links_by_file.items():
        text = _read(path)
        for link in expected_links:
            assert f"]({link})" in text, (path, link)

    chinese_text = _read("docs/book/part-vi/chapter-15.zh.md")
    assert "[追踪（trace）](../../appendix/trace-schema.zh.md)" in chinese_text
    assert "[评测（eval）](../../appendix/eval-schema.zh.md)" in chinese_text
    assert "[trace](../../appendix/trace-schema.zh.md)" not in chinese_text
    assert "[eval](../../appendix/eval-schema.zh.md)" not in chinese_text


def test_chapter_16_runtime_blueprint_threads_three_canonical_cases() -> None:
    markers_by_file = {
        "docs/book/part-vii/chapter-16.md": (
            "Заметка о сквозных сценариях среды исполнения",
            "Разбор обращений поддержки",
            "Внутренний ассистент знаний",
            "Координация инцидентов",
            "базовая среда исполнения",
            "проверками подтверждения",
            "контрактом идемпотентности",
            "телеметрией дублей тикета",
            "привязкой к источникам",
            "клиентскими границами",
            "защищенными записями в память",
            "обновлениями состояния инцидента",
        ),
        "docs/book/part-vii/chapter-16.en.md": (
            "Runtime case-spine note",
            "Support triage",
            "Internal knowledge assistant",
            "Incident coordination",
            "baseline runtime",
            "approval hooks",
            "idempotency contract",
            "duplicate-ticket telemetry",
            "trace evidence",
            "source grounding",
            "tenant filters",
            "guarded memory writes",
            "incident-state updates",
        ),
        "docs/book/part-vii/chapter-16.zh.md": (
            "Runtime case-spine note",
            "Support triage",
            "Internal knowledge assistant",
            "Incident coordination",
            "baseline runtime",
            "approval hooks",
            "idempotency contract",
            "duplicate-ticket telemetry",
            "trace evidence",
            "source grounding",
            "tenant filters",
            "guarded memory writes",
            "incident-state updates",
        ),
    }

    for path, required_markers in markers_by_file.items():
        text = _read(path)
        for required_marker in required_markers:
            assert required_marker in text, (path, required_marker)


def test_chapter_16_runtime_trace_evidence_link_is_clickable() -> None:
    expected_links_by_file = {
        "docs/book/part-vii/chapter-16.md": "../../appendix/trace-schema.md",
        "docs/book/part-vii/chapter-16.en.md": "../../appendix/trace-schema.en.md",
        "docs/book/part-vii/chapter-16.zh.md": "../../appendix/trace-schema.zh.md",
    }

    for path, expected_link in expected_links_by_file.items():
        assert f"]({expected_link})" in _read(path), (path, expected_link)

    chinese_text = _read("docs/book/part-vii/chapter-16.zh.md")
    assert "[追踪证据（trace evidence）](../../appendix/trace-schema.zh.md)" in chinese_text
    assert "[trace evidence](../../appendix/trace-schema.zh.md)" not in chinese_text


def test_chapter_18_rollout_threads_three_canonical_cases() -> None:
    markers_by_file = {
        "docs/book/part-vii/chapter-18.md": (
            "Заметка о сквозных сценариях поэтапного выпуска",
            "Разбор обращений поддержки",
            "Внутренний ассистент знаний",
            "Координация инцидентов",
            "чеклист промышленного запуска",
            "регрессионного шлюза против дублей тикета",
            "покрытия подтверждениями",
            "стратегии идемпотентности",
            "трассы",
            "шлюза свежести извлечения",
            "оценок привязки к источникам",
            "проверок клиентских границ",
            "плана регрессии после инцидента",
        ),
        "docs/book/part-vii/chapter-18.en.md": (
            "Rollout case-spine note",
            "Support triage",
            "Internal knowledge assistant",
            "Incident coordination",
            "production checklist",
            "duplicate-ticket regression gate",
            "approval coverage",
            "idempotency strategy",
            "traces",
            "retrieval freshness gate",
            "source-grounding evals",
            "tenant-boundary checks",
            "post-incident regression plan",
        ),
        "docs/book/part-vii/chapter-18.zh.md": (
            "Rollout case-spine note",
            "Support triage",
            "Internal knowledge assistant",
            "Incident coordination",
            "production checklist",
            "duplicate-ticket regression gate",
            "approval coverage",
            "idempotency strategy",
            "traces",
            "retrieval freshness gate",
            "source-grounding evals",
            "tenant-boundary checks",
            "post-incident regression plan",
        ),
    }

    for path, required_markers in markers_by_file.items():
        text = _read(path)
        for required_marker in required_markers:
            assert required_marker in text, (path, required_marker)


def test_chapter_18_rollout_trace_links_are_clickable() -> None:
    expected_snippets_by_file = {
        "docs/book/part-vii/chapter-18.md": (
            "](../../appendix/trace-schema.md)",
        ),
        "docs/book/part-vii/chapter-18.en.md": (
            "](../../appendix/trace-schema.en.md)",
        ),
        "docs/book/part-vii/chapter-18.zh.md": (
            "[追踪（traces）](../../appendix/trace-schema.zh.md)",
            "[追踪模式与事件目录](../../appendix/trace-schema.zh.md)",
            "[策略包模式与审批契约]"
            "(../../appendix/policy-bundle-schema.zh.md)",
            "[生命周期工件模式]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[变更评审与发布门禁模式]"
            "(../../appendix/change-rollout-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        for expected_snippet in expected_snippets:
            _assert_file_contains(path, expected_snippet)


def test_chapter_19_chinese_adlc_example_links_are_tightened() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-19.zh.md")
    expected_markers = (
        "包括新的[评测数据集（eval dataset）]",
        "所需的[追踪模式（trace schema）]",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "包括新的 [评测数据集（eval dataset）]",
        "所需的 [追踪模式（trace schema）]",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chapter_19_adlc_threads_three_canonical_cases() -> None:
    common_markers = (
        "ADLC case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "lifecycle state model",
        "release-bearing surfaces",
        "write-capability contract",
        "duplicate-ticket evals",
        "source-grounding evals",
        "responder-role map",
        "governed change set",
    )
    expected_markers_by_file = {
        "docs/book/part-viii/chapter-19.md": (
            "Заметка о сквозных сценариях ADLC",
            "Разбор обращений поддержки",
            "Внутренний ассистент знаний",
            "Координация инцидентов",
            "модель состояний жизненного цикла",
            "поверхности риска выпуска",
            "контракт пишущей возможности",
            "оценки дублей тикета",
            "оценки привязки к источникам",
            "карту ролей реагирующих",
            "управляемый набор изменений",
            "набор для оценки",
            "корпус извлечения",
            "схема трасс",
        ),
        "docs/book/part-viii/chapter-19.en.md": (
            *common_markers,
            "eval dataset",
            "retrieval corpus",
            "trace schema",
        ),
        "docs/book/part-viii/chapter-19.zh.md": (
            "ADLC 案例主线说明（ADLC case-spine note）",
            "支持分诊（Support triage）",
            "内部知识助手（Internal knowledge assistant）",
            "事故协调（Incident coordination）",
            "生命周期状态模型（lifecycle state model）",
            "规范案例（canonical cases）",
            "发布承载表面（release-bearing surfaces）",
            "写能力契约（write-capability contract）",
            "重复工单评测（duplicate-ticket evals）",
            "来源扎根评测（source-grounding evals）",
            "响应者角色映射（responder-role map）",
            "受治理变更集（governed change set）",
            "评测数据集（eval dataset）",
            "策略包（policy bundle）",
            "发布门禁（rollout gate）",
            "检索语料（retrieval corpus）",
            "追踪模式（trace schema）",
            "事故状态模式（incident-state schema）",
        ),
    }

    for path, expected_markers in expected_markers_by_file.items():
        text = _read(path)
        for expected_marker in expected_markers:
            assert expected_marker in text, (path, expected_marker)

    chinese_text = _read("docs/book/part-viii/chapter-19.zh.md")
    forbidden_chinese_markers = (
        "**ADLC case-spine note：**",
        "lifecycle state model 应该把三个 canonical cases",
        "三个 canonical cases",
        "release-bearing surfaces 来跟踪",
        "Support triage 连接",
        "Internal knowledge assistant 连接",
        "Incident coordination 把",
        "write-capability contract、duplicate-ticket evals",
        "source-grounding evals、memory-write rules",
        "responder-role map、notification contract",
        "作为一个 governed change set 连接起来",
    )
    for forbidden_chinese_marker in forbidden_chinese_markers:
        assert forbidden_chinese_marker not in chinese_text, forbidden_chinese_marker


def test_chapter_19_read_next_links_lifecycle_contracts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-19.md": (
            "[Схема артефактов жизненного цикла]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[Схема change review и rollout gate]"
            "(../../appendix/change-rollout-schema.md)",
            "[Схема набора политик и контракта подтверждения]"
            "(../../appendix/policy-bundle-schema.md)",
            "[Схема памяти и извлечения]"
            "(../../appendix/memory-retrieval-schema.md)",
        ),
        "docs/book/part-viii/chapter-19.en.md": (
            "[Lifecycle Artifact Schema]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[Change Review and Rollout Gate Schema]"
            "(../../appendix/change-rollout-schema.en.md)",
            "[Policy Bundle Schema and Approval Contract]"
            "(../../appendix/policy-bundle-schema.en.md)",
            "[Memory and Retrieval Schema]"
            "(../../appendix/memory-retrieval-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-19.zh.md": (
            "[生命周期工件模式]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[变更评审与发布门禁模式]"
            "(../../appendix/change-rollout-schema.zh.md)",
            "[策略包模式与审批契约]"
            "(../../appendix/policy-bundle-schema.zh.md)",
            "[记忆记录与检索契约模式]"
            "(../../appendix/memory-retrieval-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_19_adlc_release_artifact_schema_links_are_clickable() -> None:
    expected_links_by_file = {
        "docs/book/part-viii/chapter-19.md": (
            "../../appendix/eval-schema.md",
            "../../appendix/trace-schema.md",
            "../../appendix/policy-bundle-schema.md",
            "../../appendix/change-rollout-schema.md",
            "../../appendix/memory-retrieval-schema.md",
            "../../appendix/incident-record-schema.md",
        ),
        "docs/book/part-viii/chapter-19.en.md": (
            "../../appendix/eval-schema.en.md",
            "../../appendix/trace-schema.en.md",
            "../../appendix/policy-bundle-schema.en.md",
            "../../appendix/change-rollout-schema.en.md",
            "../../appendix/memory-retrieval-schema.en.md",
            "../../appendix/incident-record-schema.en.md",
        ),
        "docs/book/part-viii/chapter-19.zh.md": (
            "../../appendix/eval-schema.zh.md",
            "../../appendix/trace-schema.zh.md",
            "../../appendix/policy-bundle-schema.zh.md",
            "../../appendix/change-rollout-schema.zh.md",
            "../../appendix/memory-retrieval-schema.zh.md",
            "../../appendix/incident-record-schema.zh.md",
        ),
    }

    for path, expected_links in expected_links_by_file.items():
        text = _read(path)
        for link in expected_links:
            assert f"]({link})" in text, (path, link)

    chinese_text = _read("docs/book/part-viii/chapter-19.zh.md")
    expected_chinese_links = (
        "[评测数据集（eval dataset）](../../appendix/eval-schema.zh.md)",
        "[策略包（policy bundle）](../../appendix/policy-bundle-schema.zh.md)",
        "[发布门禁（rollout gate）](../../appendix/change-rollout-schema.zh.md)",
        "[检索语料（retrieval corpus）](../../appendix/memory-retrieval-schema.zh.md)",
        "[追踪模式（trace schema）](../../appendix/trace-schema.zh.md)",
        "[事故状态模式（incident-state schema）]"
        "(../../appendix/incident-record-schema.zh.md)",
    )
    for expected_chinese_link in expected_chinese_links:
        assert expected_chinese_link in chinese_text, expected_chinese_link
    forbidden_chinese_links = (
        "[eval dataset](../../appendix/eval-schema.zh.md)",
        "[policy bundle](../../appendix/policy-bundle-schema.zh.md)",
        "[rollout gate](../../appendix/change-rollout-schema.zh.md)",
        "[retrieval corpus](../../appendix/memory-retrieval-schema.zh.md)",
        "[trace schema](../../appendix/trace-schema.zh.md)",
        "[incident-state schema](../../appendix/incident-record-schema.zh.md)",
    )
    for forbidden_chinese_link in forbidden_chinese_links:
        assert forbidden_chinese_link not in chinese_text, forbidden_chinese_link


def test_chapter_21_assurance_threads_three_canonical_cases() -> None:
    common_markers = (
        "Assurance case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "containment paths",
        "duplicate-outcome detection",
        "updated eval",
        "traceable outcome",
        "tenant-boundary containment",
        "notification throttling",
    )
    expected_markers_by_file = {
        "docs/book/part-viii/chapter-21.md": (
            "Заметка о сквозных сценариях контура заверения",
            "Разбор обращений поддержки",
            "Внутренний ассистент знаний",
            "Координация инцидентов",
            "путями сдерживания",
            "обнаружение дублей результата",
            "обновленную оценку",
            "трассируемый результат",
            "сдерживание по клиентским границам",
            "ограничение уведомлений",
            "запись о находке и реагировании",
            "сдерживание через режим только с подтверждением",
            "сигнал отравления извлечения",
            "обновление контроля после инцидента",
        ),
        "docs/book/part-viii/chapter-21.en.md": (
            *common_markers,
            "finding and response record",
            "approval-only containment",
            "retrieval-poisoning signal",
            "post-incident control update",
        ),
        "docs/book/part-viii/chapter-21.zh.md": (
            "保障案例主线说明（Assurance case-spine note）",
            "支持分诊（Support triage）",
            "内部知识助手（Internal knowledge assistant）",
            "事故协调（Incident coordination）",
            "发现与响应记录（finding and response record）",
            "[发现与响应记录（finding and response record）]"
            "(../../appendix/incident-record-schema.zh.md)应该通过",
            "遏制路径（containment paths）",
            "规范案例（canonical cases）",
            "重复结果检测（duplicate-outcome detection）",
            "更新后的评测（updated eval）",
            "可追踪结果（traceable outcome）",
            "租户边界遏制（tenant-boundary containment）",
            "新鲜度修复（freshness remediation）",
            "升级滥用信号（escalation abuse signal）",
            "通知节流（notification throttling）",
            "响应者角色负责人（responder-role owner）",
            "仅审批遏制（approval-only containment）",
            "检索投毒信号（retrieval-poisoning signal）",
            "记忆写入隔离（memory-write quarantine）",
            "事故状态回滚（incident-state rollback）",
            "事故后控制更新（post-incident control update）",
        ),
    }

    for path, expected_markers in expected_markers_by_file.items():
        text = _read(path)
        for expected_marker in expected_markers:
            assert expected_marker in text, (path, expected_marker)

    chinese_text = _read("docs/book/part-viii/chapter-21.zh.md")
    forbidden_chinese_markers = (
        "**Assurance case-spine note：**",
        "通过不同 containment paths 闭合",
        "[发现与响应记录（finding and response record）]"
        "(../../appendix/incident-record-schema.zh.md) 应该通过",
        "三个 canonical cases",
        "Support triage 连接",
        "Internal knowledge assistant 连接",
        "Incident coordination 连接",
        "连接 duplicate-outcome detection、",
        "owner、updated eval 和 traceable outcome",
        "source-grounding review、tenant-boundary containment",
        "freshness remediation。Incident coordination",
        "escalation abuse signal、notification throttling",
    )
    for forbidden_chinese_marker in forbidden_chinese_markers:
        assert forbidden_chinese_marker not in chinese_text, forbidden_chinese_marker


def test_chapter_21_chinese_assurance_example_links_are_tightened() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-21.zh.md")
    expected_markers = (
        "更新后的[评测（eval）]",
        "已确认的[可追踪结果（traceable outcome）]"
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "更新后的 [评测（eval）]",
        "已确认的 [可追踪结果（traceable outcome）] 都通过",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chapter_21_assurance_case_spine_links_are_clickable() -> None:
    expected_links_by_file = {
        "docs/book/part-viii/chapter-21.md": (
            "../../appendix/eval-schema.md",
            "../../appendix/trace-schema.md",
            "../../appendix/incident-record-schema.md",
            "../../appendix/approval-schema.md",
            "../../appendix/memory-retrieval-schema.md",
            "../../appendix/lifecycle-artifact-schema.md",
        ),
        "docs/book/part-viii/chapter-21.en.md": (
            "../../appendix/eval-schema.en.md",
            "../../appendix/trace-schema.en.md",
            "../../appendix/incident-record-schema.en.md",
            "../../appendix/approval-schema.en.md",
            "../../appendix/memory-retrieval-schema.en.md",
            "../../appendix/lifecycle-artifact-schema.en.md",
        ),
        "docs/book/part-viii/chapter-21.zh.md": (
            "../../appendix/eval-schema.zh.md",
            "../../appendix/trace-schema.zh.md",
            "../../appendix/incident-record-schema.zh.md",
            "../../appendix/approval-schema.zh.md",
            "../../appendix/memory-retrieval-schema.zh.md",
            "../../appendix/lifecycle-artifact-schema.zh.md",
        ),
    }

    for path, expected_links in expected_links_by_file.items():
        text = _read(path)
        for link in expected_links:
            assert f"]({link})" in text, (path, link)

    chinese_text = _read("docs/book/part-viii/chapter-21.zh.md")
    expected_chinese_links = (
        "[评测（eval）](../../appendix/eval-schema.zh.md)",
        "[可追踪结果（traceable outcome）](../../appendix/trace-schema.zh.md)",
        "[发现与响应记录（finding and response record）]"
        "(../../appendix/incident-record-schema.zh.md)",
        "[仅审批遏制（approval-only containment）]"
        "(../../appendix/approval-schema.zh.md)",
        "[检索投毒信号（retrieval-poisoning signal）]"
        "(../../appendix/memory-retrieval-schema.zh.md)",
        "[记忆写入隔离（memory-write quarantine）]"
        "(../../appendix/memory-retrieval-schema.zh.md)",
        "[事故状态回滚（incident-state rollback）]"
        "(../../appendix/incident-record-schema.zh.md)",
        "[事故后控制更新（post-incident control update）]"
        "(../../appendix/lifecycle-artifact-schema.zh.md)",
    )
    for expected_chinese_link in expected_chinese_links:
        assert expected_chinese_link in chinese_text, expected_chinese_link
    forbidden_chinese_links = (
        "[eval](../../appendix/eval-schema.zh.md)",
        "[traceable outcome](../../appendix/trace-schema.zh.md)",
        "[finding and response record](../../appendix/incident-record-schema.zh.md)",
        "[approval-only containment](../../appendix/approval-schema.zh.md)",
        "[retrieval-poisoning signal](../../appendix/memory-retrieval-schema.zh.md)",
        "[memory-write quarantine](../../appendix/memory-retrieval-schema.zh.md)",
        "[incident-state rollback](../../appendix/incident-record-schema.zh.md)",
        "[post-incident control update]"
        "(../../appendix/lifecycle-artifact-schema.zh.md)",
    )
    for forbidden_chinese_link in forbidden_chinese_links:
        assert forbidden_chinese_link not in chinese_text, forbidden_chinese_link


def test_chapter_21_chinese_evidence_spine_link_is_localized() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-21.zh.md")
    expected_markers = (
        "事故和发布（rollout）判断串成同一条可复核链路",
        "打开[证据主干（Evidence Spine）](../part-v/evidence-spine.zh.md)",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "事故和 rollout 判断串成同一条可复核链路",
        "打开 [Evidence Spine](../part-v/evidence-spine.zh.md)",
        "打开[Evidence Spine](../part-v/evidence-spine.zh.md)",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chapter_21_useful_refs_include_change_rollout_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-21.md": (
            "[Схема проверки изменений и шлюза поэтапного выпуска]"
            "(../../appendix/change-rollout-schema.md)"
        ),
        "docs/book/part-viii/chapter-21.en.md": (
            "[Change Review and Rollout Gate Schema]"
            "(../../appendix/change-rollout-schema.en.md)"
        ),
        "docs/book/part-viii/chapter-21.zh.md": (
            "[追踪模式与事件目录](../../appendix/trace-schema.zh.md)",
            "[策略包模式与审批契约]"
            "(../../appendix/policy-bundle-schema.zh.md)",
            "[评测数据集模式与打分契约]"
            "(../../appendix/eval-schema.zh.md)",
            "[生命周期工件模式]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[变更评审与发布门禁模式]"
            "(../../appendix/change-rollout-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        if isinstance(expected_snippets, str):
            expected_snippets = (expected_snippets,)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_chinese_duplicate_ticket_example_links_are_tightened() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-22.zh.md")
    expected_markers = (
        "生效的[评测数据集（eval dataset）]",
        "`side_effect_unknown`[策略包（policy bundle）]",
        "`create_support_ticket`[能力契约（capability contract）]",
        "和[追踪模式](../../appendix/trace-schema.zh.md)",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "生效的 [评测数据集（eval dataset）]",
        "`side_effect_unknown` [策略包（policy bundle）]",
        "`create_support_ticket` [能力契约（capability contract）]",
        "和 [追踪模式](../../appendix/trace-schema.zh.md)",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chapter_22_supply_chain_threads_three_canonical_cases() -> None:
    common_markers = (
        "Supply-chain case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "provenance",
        "capability contract",
        "source-grounding rubric",
        "responder-role map",
    )
    expected_markers_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "Заметка о сквозных сценариях цепочки поставки",
            "Разбор обращений поддержки",
            "Внутренний ассистент знаний",
            "Координация инцидентов",
            "происхождение",
            "контракт возможности",
            "рубрики привязки к источникам",
            "карты ролей реагирующих",
            "утвержденный набор артефактов",
            "набор для оценки",
            "утвержденного корпуса извлечения",
            "обновления артефактов после инцидента",
            "схемы трасс",
            "схемы подтверждения",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            *common_markers,
            "approved artifact bundle",
            "eval dataset",
            "approved retrieval corpus",
            "post-incident artifact update",
            "trace schema",
            "approval schema",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "供应链案例主线说明（Supply-chain case-spine note）",
            "支持分诊（Support triage）",
            "内部知识助手（Internal knowledge assistant）",
            "事故协调（Incident coordination）",
            "已批准工件包（approved artifact bundle）",
            "[已批准工件包（approved artifact bundle）]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)应该为",
            "规范案例（canonical cases）",
            "来源追踪（provenance）",
            "写入路径（write path）",
            "写入路径（write path）的[评测数据集（eval dataset）]",
            "评测数据集（eval dataset）",
            "策略包（policy bundle）",
            "能力契约（capability contract）",
            "发布门禁（rollout gate）",
            "已批准检索语料（approved retrieval corpus）",
            "来源扎根评分规程、租户过滤配置、记忆写入策略与新鲜度证明",
            "响应者角色映射（escalation-policy bundle、notification contract、responder-role map）",
            "事故后工件更新（post-incident artifact update）",
            "[审批模式](../../appendix/approval-schema.zh.md)",
            "[追踪模式](../../appendix/trace-schema.zh.md)",
            "[事故状态模式](../../appendix/incident-record-schema.zh.md)",
        ),
    }

    for path, expected_markers in expected_markers_by_file.items():
        text = _read(path)
        for expected_marker in expected_markers:
            assert expected_marker in text, (path, expected_marker)

    chinese_text = _read("docs/book/part-viii/chapter-22.zh.md")
    forbidden_chinese_markers = (
        "**Supply-chain case-spine note：**",
        "三个 canonical cases",
        "Support triage 需要",
        "Internal knowledge assistant 需要",
        "Incident coordination 需要",
        "保留 provenance",
        "[已批准工件包（approved artifact bundle）]"
        "(../../appendix/lifecycle-artifact-schema.zh.md) 应该为",
        "需要 write path 的",
        "写入路径（write path）的 [评测数据集（eval dataset）]",
        "[追踪模式](../../appendix/trace-schema.zh.md) 和 [发布门禁",
        "需要 [已批准检索语料",
        "需要 [升级策略包",
        " 和 [事故后工件更新",
    )
    for forbidden_chinese_marker in forbidden_chinese_markers:
        assert forbidden_chinese_marker not in chinese_text, forbidden_chinese_marker


def test_chapter_22_supply_chain_schema_links_are_clickable() -> None:
    expected_links_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "../../appendix/eval-schema.md",
            "../../appendix/policy-bundle-schema.md",
            "../../appendix/approval-schema.md",
            "../../appendix/trace-schema.md",
            "../../appendix/change-rollout-schema.md",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "../../appendix/eval-schema.en.md",
            "../../appendix/policy-bundle-schema.en.md",
            "../../appendix/approval-schema.en.md",
            "../../appendix/trace-schema.en.md",
            "../../appendix/change-rollout-schema.en.md",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "../../appendix/eval-schema.zh.md",
            "../../appendix/policy-bundle-schema.zh.md",
            "../../appendix/approval-schema.zh.md",
            "../../appendix/trace-schema.zh.md",
            "../../appendix/change-rollout-schema.zh.md",
        ),
    }

    for path, expected_links in expected_links_by_file.items():
        text = _read(path)
        for link in expected_links:
            assert f"]({link})" in text, (path, link)

    chinese_text = _read("docs/book/part-viii/chapter-22.zh.md")
    expected_chinese_links = (
        "[已批准工件包（approved artifact bundle）]"
        "(../../appendix/lifecycle-artifact-schema.zh.md)",
        "[评测数据集（eval dataset）](../../appendix/eval-schema.zh.md)",
        "[策略包（policy bundle）](../../appendix/policy-bundle-schema.zh.md)",
        "[发布门禁（rollout gate）](../../appendix/change-rollout-schema.zh.md)",
        "[能力契约（capability contract）]"
        "(../../appendix/lifecycle-artifact-schema.zh.md)",
        "[已批准检索语料（approved retrieval corpus）]"
        "(../../appendix/memory-retrieval-schema.zh.md)",
        "[事故后工件更新（post-incident artifact update）]"
        "(../../appendix/lifecycle-artifact-schema.zh.md)",
    )
    for expected_chinese_link in expected_chinese_links:
        assert expected_chinese_link in chinese_text, expected_chinese_link
    forbidden_chinese_links = (
        "[eval dataset](../../appendix/eval-schema.zh.md)",
        "[policy bundle](../../appendix/policy-bundle-schema.zh.md)",
        "[rollout gate](../../appendix/change-rollout-schema.zh.md)",
        "[capability contract](../../appendix/lifecycle-artifact-schema.zh.md)",
        "[approved artifact bundle](../../appendix/lifecycle-artifact-schema.zh.md)",
        "[approved retrieval corpus](../../appendix/memory-retrieval-schema.zh.md)",
        "[post-incident artifact update]"
        "(../../appendix/lifecycle-artifact-schema.zh.md)",
    )
    for forbidden_chinese_link in forbidden_chinese_links:
        assert forbidden_chinese_link not in chinese_text, forbidden_chinese_link


def test_chapter_22_provenance_questions_link_approval_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "версия контракта и [схема подтверждения](../../appendix/approval-schema.md)"
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "contract version and [approval schema](../../appendix/approval-schema.en.md)"
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "契约版本与[审批模式（approval schema）](../../appendix/approval-schema.zh.md)"
        ),
    }

    for path, expected_snippet in expected_snippets_by_file.items():
        _assert_file_contains(path, expected_snippet)


def test_chapter_22_provenance_questions_link_policy_bundle() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "какой [набор политик](../../appendix/policy-bundle-schema.md) был активен"
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "which [policy bundle](../../appendix/policy-bundle-schema.en.md) was active"
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "哪一个[策略包（policy bundle）](../../appendix/policy-bundle-schema.zh.md)"
        ),
    }

    for path, expected_snippet in expected_snippets_by_file.items():
        _assert_file_contains(path, expected_snippet)


def test_chapter_22_artifact_inventory_links_lifecycle_artifacts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[контракт возможности](../../appendix/lifecycle-artifact-schema.md)",
            "[схема управления средой исполнения](../../appendix/lifecycle-artifact-schema.md)",
            "[правила прерывания и повторной инициализации для сессий возможностей]"
            "(../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[capability contract](../../appendix/lifecycle-artifact-schema.en.md)",
            "[runtime-control schema](../../appendix/lifecycle-artifact-schema.en.md)",
            "[capability-session interruption and re-initialization rules]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[能力契约（capability contract）]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[运行时控制模式（runtime-control schema）]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[能力会话中断与重新初始化规则]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_supply_chain_surface_links_control_schemas() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[правила и схемы подтверждения](../../appendix/approval-schema.md)",
            "[схемы управления средой исполнения](../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[approval rules and schemas](../../appendix/approval-schema.en.md)",
            "[runtime-control schemas]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[生命周期工件模式]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[审批规则与模式](../../appendix/approval-schema.zh.md)",
            "[运行时控制模式](../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_supply_chain_surface_links_artifact_families() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[конфигурации политик](../../appendix/policy-bundle-schema.md)",
            "[корпуса для извлечения](../../appendix/memory-retrieval-schema.md)",
            "[контракты возможностей](../../appendix/lifecycle-artifact-schema.md)",
            "[наборы для оценки](../../appendix/eval-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[policy configs](../../appendix/policy-bundle-schema.en.md)",
            "[retrieval corpora](../../appendix/memory-retrieval-schema.en.md)",
            "[capability contracts](../../appendix/lifecycle-artifact-schema.en.md)",
            "[eval datasets](../../appendix/eval-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[策略配置](../../appendix/policy-bundle-schema.zh.md)",
            "[检索语料](../../appendix/memory-retrieval-schema.zh.md)",
            "[能力契约](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[评测数据集](../../appendix/eval-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_supply_chain_surface_links_rollout_bundles() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[наборы для поэтапного выпуска]"
            "(../../appendix/change-rollout-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[rollout bundles](../../appendix/change-rollout-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[发布工件包](../../appendix/change-rollout-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_approved_model_route_links_lifecycle_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "утвержденный [маршрут к модели]"
            "(../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "approved [model route]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "已批准的[模型路由](../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_approved_prompt_bundle_links_lifecycle_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "утвержденный [набор правил инструкций]"
            "(../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "approved [prompt bundle]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "已批准的[提示包](../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_prompt_bundle_provenance_links_eval_rollout_schemas() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[оценки](../../appendix/eval-schema.md) ее покрыли",
            "[волне поэтапного выпуска]"
            "(../../appendix/change-rollout-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[evals](../../appendix/eval-schema.en.md) covered it",
            "[rollout wave](../../appendix/change-rollout-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[评测](../../appendix/eval-schema.zh.md)覆盖了它",
            "[发布波次（rollout wave）](../../appendix/change-rollout-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)

    chinese_text = _read("docs/book/part-viii/chapter-22.zh.md")
    forbidden_chinese_link = "[rollout 波次](../../appendix/change-rollout-schema.zh.md)"
    assert forbidden_chinese_link not in chinese_text, forbidden_chinese_link


def test_chapter_22_prompt_bundle_provenance_links_owner_version_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[кто менял инструкцию]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[какая версия](../../appendix/lifecycle-artifact-schema.md) сейчас в проде",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[who changed the prompt](../../appendix/lifecycle-artifact-schema.en.md)",
            "[which version](../../appendix/lifecycle-artifact-schema.en.md) "
            "is in production",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[谁改了提示](../../appendix/lifecycle-artifact-schema.zh.md)",
            "生产环境里是[哪一个版本](../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_prompt_bundle_related_routines_link_lifecycle_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[рабочим процедурам](../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[routines](../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[例程](../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_supply_chain_surface_links_model_prompt_artifacts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[маршруты к моделям](../../appendix/lifecycle-artifact-schema.md)",
            "[наборы правил инструкций и рабочих процедур]"
            "(../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[model artifacts](../../appendix/lifecycle-artifact-schema.en.md)",
            "[prompt and routine bundles]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[模型工件](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[提示和例程包](../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_provenance_questions_link_model_prompt_artifacts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[откуда взялась эта модель](../../appendix/lifecycle-artifact-schema.md)",
            "[набор правил инструкций](../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[where this model came from]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[prompt bundle](../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[这个模型从哪里来](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[提示包](../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_trust_chain_links_data_retrieval_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[цепочкой данных и извлечения]"
            "(../../appendix/memory-retrieval-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[data and retrieval chain]"
            "(../../appendix/memory-retrieval-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[数据与检索链](../../appendix/memory-retrieval-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_trust_chain_links_eval_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[цепочкой оценки](../../appendix/eval-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[eval chain](../../appendix/eval-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[评测链](../../appendix/eval-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_trust_chain_links_policy_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[цепочкой политик](../../appendix/policy-bundle-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[policy chain](../../appendix/policy-bundle-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[策略链](../../appendix/policy-bundle-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_trust_chain_links_capability_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[цепочкой возможностей](../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[capability chain](../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[能力链](../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_trust_chain_links_approval_runtime_control_schemas() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[подтверждения](../../appendix/approval-schema.md) и "
            "[управления средой исполнения]"
            "(../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[approval](../../appendix/approval-schema.en.md) and "
            "[runtime-control](../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[审批](../../appendix/approval-schema.zh.md)与"
            "[运行时控制](../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_trust_chain_links_session_authorization_schemas() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[цепочкой правил управления сессиями возможностей]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[цепочкой делегированной авторизации]"
            "(../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[capability-session governance chain]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[delegated authorization chain]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[能力会话治理链](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[委派授权链](../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_trust_chain_links_model_prompt_schemas() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[цепочкой моделей](../../appendix/lifecycle-artifact-schema.md)",
            "[цепочкой правил инструкций и рабочих процедур]"
            "(../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[model chain](../../appendix/lifecycle-artifact-schema.en.md)",
            "[prompt and routine chain]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[模型链](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[提示与例程链](../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_provenance_questions_link_eval_dataset() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "какой [набор для оценки](../../appendix/eval-schema.md) подтвердил выпуск",
            "считать [набор данных для оценки](../../appendix/eval-schema.md) "
            "чем-то второстепенным",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "which [eval dataset](../../appendix/eval-schema.en.md) validated the release",
            "treat an [eval dataset](../../appendix/eval-schema.en.md) as secondary",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "哪一个[评测数据集（eval dataset）](../../appendix/eval-schema.zh.md)验证",
            "把[评测数据集（eval dataset）](../../appendix/eval-schema.zh.md)看得太轻",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_runtime_control_schema_links_are_clickable() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[схема подтверждения](../../appendix/approval-schema.md)",
            "[схема управления средой исполнения](../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[approval schemas](../../appendix/approval-schema.en.md)",
            "[runtime-control schemas](../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[审批模式（approval schema）](../../appendix/approval-schema.zh.md)",
            "[运行时控制模式（runtime-control schema）]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_trusted_artifact_examples_link_schema_contracts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[policy YAML](../../appendix/policy-bundle-schema.md)",
            "[конфигурациям извлечения](../../appendix/memory-retrieval-schema.md)",
            "[порогам подтверждения](../../appendix/approval-schema.md)",
            "[runtime-control schemas](../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[policy YAML](../../appendix/policy-bundle-schema.en.md)",
            "[retrieval configs](../../appendix/memory-retrieval-schema.en.md)",
            "[approval thresholds](../../appendix/approval-schema.en.md)",
            "[runtime-control schemas](../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[策略 YAML（policy YAML）](../../appendix/policy-bundle-schema.zh.md)",
            "[检索配置](../../appendix/memory-retrieval-schema.zh.md)",
            "[审批阈值](../../appendix/approval-schema.zh.md)",
            "[运行时控制模式](../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)

    chinese_text = _read("docs/book/part-viii/chapter-22.zh.md")
    forbidden_chinese_link = "[策略 YAML](../../appendix/policy-bundle-schema.zh.md)"
    assert forbidden_chinese_link not in chinese_text, forbidden_chinese_link


def test_chapter_22_artifact_discipline_failures_link_schema_contracts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[наборы для оценки](../../appendix/eval-schema.md)",
            "[контракты возможностей](../../appendix/lifecycle-artifact-schema.md)",
            "[approval schemas](../../appendix/approval-schema.md) или "
            "[runtime-control schemas](../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[eval datasets](../../appendix/eval-schema.en.md)",
            "[capability contracts](../../appendix/lifecycle-artifact-schema.en.md)",
            "[approval schemas](../../appendix/approval-schema.en.md) or "
            "[runtime-control schemas](../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[评测数据集](../../appendix/eval-schema.zh.md)",
            "[能力契约](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[审批模式](../../appendix/approval-schema.zh.md)或"
            "[运行时控制模式](../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_maturity_bar_links_production_artifact_contracts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[policy](../../appendix/policy-bundle-schema.md)-",
            "[eval](../../appendix/eval-schema.md)-",
            "[capability](../../appendix/lifecycle-artifact-schema.md)-",
            "[approval](../../appendix/approval-schema.md)-",
            "[runtime-control](../../appendix/lifecycle-artifact-schema.md)-",
            "[verifier](../../appendix/eval-schema.md)-артефакты",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[policy](../../appendix/policy-bundle-schema.en.md)",
            "[eval](../../appendix/eval-schema.en.md)",
            "[capability](../../appendix/lifecycle-artifact-schema.en.md)",
            "[approval](../../appendix/approval-schema.en.md)",
            "[runtime-control](../../appendix/lifecycle-artifact-schema.en.md)",
            "[verifier](../../appendix/eval-schema.en.md) artifacts",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[策略](../../appendix/policy-bundle-schema.zh.md)",
            "[评测](../../appendix/eval-schema.zh.md)",
            "[能力](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[审批](../../appendix/approval-schema.zh.md)",
            "[运行时控制（runtime-control）]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[验证器（verifier）](../../appendix/eval-schema.zh.md)工件",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)

    chinese_text = _read("docs/book/part-viii/chapter-22.zh.md")
    forbidden_chinese_links = (
        "[runtime-control](../../appendix/lifecycle-artifact-schema.zh.md)",
        "[verifier](../../appendix/eval-schema.zh.md)",
    )
    for forbidden_chinese_link in forbidden_chinese_links:
        assert forbidden_chinese_link not in chinese_text, forbidden_chinese_link


def test_chapter_22_approved_inventory_links_registry_handbook() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[утвержденный реестр](../../appendix/registry-operations-handbook.md)",
            "[approved inventory](../../appendix/registry-operations-handbook.md)",
            "[утвержденный реестр платформы]"
            "(../../appendix/registry-operations-handbook.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[approved inventory](../../appendix/registry-operations-handbook.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[已批准清单](../../appendix/registry-operations-handbook.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_checklist_links_platform_and_release_artifacts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[шаблон, разрешенный на уровне платформы]"
            "(../../appendix/change-rollout-schema.md)",
            "[артефакта, разрешенного к выпуску]"
            "(../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[platform-approved pattern](../../appendix/change-rollout-schema.en.md)",
            "[release-approved artifact]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[平台批准的模式](../../appendix/change-rollout-schema.zh.md)",
            "[发布批准的工件](../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_deprecated_artifacts_link_lifecycle_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[устаревшие шаблоны](../../appendix/lifecycle-artifact-schema.md)",
            "[deprecated patterns](../../appendix/lifecycle-artifact-schema.md)",
            "[устаревший артефакт](../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[deprecated patterns](../../appendix/lifecycle-artifact-schema.en.md)",
            "[deprecated artifact](../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[已废弃模式](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[已废弃工件](../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_incident_evidence_links_schema_lineage() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[доказательном слое](../../appendix/trace-schema.md)",
            "[verifier lineage](../../appendix/eval-schema.md)",
            "[активные версии контрактов и схем](../../appendix/trace-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[contract-version linkage](../../appendix/trace-schema.en.md)",
            "[incident evidence](../../appendix/incident-record-schema.en.md)",
            "[verifier-contract lineage](../../appendix/eval-schema.en.md)",
            "[active contract/schema versions](../../appendix/trace-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[事故证据](../../appendix/incident-record-schema.zh.md)",
            "[契约版本链接](../../appendix/trace-schema.zh.md)",
            "[验证器契约血缘](../../appendix/eval-schema.zh.md)",
            "[生效中的契约/模式版本](../../appendix/trace-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_checklist_links_production_artifact_ownership() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[рабочих артефактов](../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[production artifacts](../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[生产工件](../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_approved_artifact_definition_links_lifecycle_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[Доверенный артефакт](../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[approved artifact](../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[已批准工件](../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_approved_artifact_bundle_links_lifecycle_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[утвержденный набор артефактов](../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[approved artifact bundle]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[已批准工件包（approved artifact bundle）]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_duplicate_ticket_release_bundle_links_lifecycle_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[утвержденном наборе выпуска](../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[approved release bundle]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[已批准发布包](../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_inventory_artifact_distinction_links_both_contracts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[утвержденный реестр](../../appendix/registry-operations-handbook.md) отвечает",
            "[доверенные артефакты](../../appendix/lifecycle-artifact-schema.md) отвечают",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[approved inventory]"
            "(../../appendix/registry-operations-handbook.en.md) answers",
            "[approved artifacts]"
            "(../../appendix/lifecycle-artifact-schema.en.md) answers",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[已批准清单](../../appendix/registry-operations-handbook.zh.md)回答的是",
            "[已批准工件](../../appendix/lifecycle-artifact-schema.zh.md)回答的是",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_approved_artifact_versions_bundles_link_lifecycle_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "конкретные [версии и наборы]"
            "(../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "exact [versions and bundles]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[具体版本和工件包](../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_release_discipline_links_bundle_and_verifier_contracts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[управляемой версией, утвержденным набором]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[семейством контрактов с ограничениями проверяющего]"
            "(../../appendix/eval-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[governed version, approved bundle]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[verifier-bearing contract family]"
            "(../../appendix/eval-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[受治理版本、已批准包](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[带有验证器约束的契约族](../../appendix/eval-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_governed_lineage_links_release_identity_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[доверенных артефактов, идентичности выпуска и версий]"
            "(../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[approved artifacts, release identity, and decision-bearing versions]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[已批准工件、发布身份与承载决策版本]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_core_promise_links_reviewed_release_identity() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[проверенный набор артефактов]"
            "(../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[reviewed artifact set, trusted contract version, and approved "
            "release identity](../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[哪一组已评审工件、哪一个可信契约版本，以及哪一个已批准发布身份]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_capability_contract_checklist_links_control_schemas() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[кто владелец](../../appendix/lifecycle-artifact-schema.md)",
            "[какой уровень риска](../../appendix/approval-schema.md)",
            "[какой инструментальный principal]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[какой профиль сетевого доступа]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[какие направления выхода разрешены]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[как устроена семантика подтверждения]"
            "(../../appendix/approval-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[who the owner is](../../appendix/lifecycle-artifact-schema.en.md)",
            "[what the risk tier is](../../appendix/approval-schema.en.md)",
            "[which tool principal is used]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[what the network access profile is]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[which egress destinations are allowed]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[which approval semantics apply](../../appendix/approval-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[谁是负责人](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[风险等级是什么](../../appendix/approval-schema.zh.md)",
            "[使用哪个工具主体（tool principal）]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[网络访问配置是什么](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[允许哪些出口目标](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[采用什么审批语义](../../appendix/approval-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)

    chinese_text = _read("docs/book/part-viii/chapter-22.zh.md")
    forbidden_chinese_link = (
        "[使用哪个工具 principal](../../appendix/lifecycle-artifact-schema.zh.md)"
    )
    assert forbidden_chinese_link not in chinese_text, forbidden_chinese_link


def test_chapter_22_runtime_control_provenance_checklist_links_control_schemas() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[paused runs истекали или могли ждать бесконечно]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[capability-session re-init была allowed, denied или approval-bound]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[telemetry обязана была связывать исходную и reinitialized "
            "capability sessions](../../appendix/trace-schema.md)",
            "[approval](../../appendix/approval-schema.md) и "
            "[session-control logic](../../appendix/lifecycle-artifact-schema.md)",
            "[delegated access была platform-owned или user-delegated]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[principal-binding rule и revoke behavior]"
            "(../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[paused runs expired or waited indefinitely]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[capability-session re-init was allowed, denied, or approval-bound]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[telemetry was expected to link the original and reinitialized "
            "capability sessions](../../appendix/trace-schema.en.md)",
            "[approval](../../appendix/approval-schema.en.md) and "
            "[session-control logic](../../appendix/lifecycle-artifact-schema.en.md)",
            "[delegated access was platform-owned or user-delegated]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[principal-binding rule and revoke behavior]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[暂停运行是会过期，还是可以无限等待]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[能力会话重新初始化是允许、拒绝还是审批绑定"
            "（allowed、denied、approval-bound）]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[遥测是否应该把原始能力会话和重新初始化后的能力会话关联起来]"
            "(../../appendix/trace-schema.zh.md)",
            "[审批](../../appendix/approval-schema.zh.md)与"
            "[会话控制逻辑](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[委派访问是平台拥有还是用户委派]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[主体绑定规则与撤销行为（principal binding and revoke behavior）]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)

    chinese_text = _read("docs/book/part-viii/chapter-22.zh.md")
    forbidden_chinese_links = (
        "[能力会话重新初始化是 allowed、denied，还是 approval-bound]"
        "(../../appendix/lifecycle-artifact-schema.zh.md)",
        "[principal 绑定规则与撤销行为]"
        "(../../appendix/lifecycle-artifact-schema.zh.md)",
    )
    for forbidden_chinese_link in forbidden_chinese_links:
        assert forbidden_chinese_link not in chinese_text, forbidden_chinese_link


def test_chapter_22_harness_handoff_artifacts_link_lifecycle_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[структурированных handoff artifacts]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[какой handoff artifact перенес scope, какой evaluator critique "
            "изменил следующий sprint и на какой reset boundary активный "
            "контекст сменился](../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[structured handoff artifacts]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[which handoff artifact carried scope, which evaluator critique "
            "shaped the next sprint, and which reset boundary changed the "
            "active context](../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[结构化交接工件](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[是哪一份交接工件传递了范围（scope）、哪一条评测器批注"
            "（evaluator critique）改变了下一轮 sprint，"
            "以及是在什么重置边界上，活动上下文发生了变化]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)

    chinese_text = _read("docs/book/part-viii/chapter-22.zh.md")
    forbidden_chinese_link = (
        "[是哪一份交接工件传递了 scope、哪一条 evaluator critique "
        "改变了下一轮 sprint，以及是在什么重置边界上，活动上下文发生了变化]"
        "(../../appendix/lifecycle-artifact-schema.zh.md)"
    )
    assert forbidden_chinese_link not in chinese_text, forbidden_chinese_link


def test_chapter_22_boundary_parity_links_telemetry_and_contract_family() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[Telemetry](../../appendix/trace-schema.md) может показать",
            "pause, re-init или delegated action",
            "[проверенная contract family](../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[Telemetry](../../appendix/trace-schema.en.md) may show",
            "[pause, re-init, or delegated action]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[reviewed contract family]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[遥测](../../appendix/trace-schema.zh.md)也许能告诉你",
            "[暂停、重新初始化或委派动作]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[经过评审的契约族]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_failed_run_provenance_links_identity_and_eval_fields() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[набор доверенных артефактов и какая идентичность выпуска]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[экспортируемое поле, например `failure_reason`]"
            "(../../appendix/eval-schema.md)",
            "[`latest_failure_reason`](../../appendix/eval-schema.md)",
            "[`traceable_failed_runs`](../../appendix/eval-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[approved artifact set and release identity]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[exported failure field such as `failure_reason`]"
            "(../../appendix/eval-schema.en.md)",
            "[`latest_failure_reason`](../../appendix/eval-schema.en.md)",
            "[`traceable_failed_runs`](../../appendix/eval-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[哪一组已批准工件与哪一个发布身份]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[失败原因字段（`failure_reason`）](../../appendix/eval-schema.zh.md)",
            "[`latest_failure_reason`](../../appendix/eval-schema.zh.md)",
            "[`traceable_failed_runs`](../../appendix/eval-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)

    chinese_text = _read("docs/book/part-viii/chapter-22.zh.md")
    forbidden_chinese_links = (
        "[导出字段，例如 `failure_reason`](../../appendix/eval-schema.zh.md)",
        "[导出的失败字段，例如 `failure_reason`](../../appendix/eval-schema.zh.md)",
    )
    for forbidden_chinese_link in forbidden_chinese_links:
        assert forbidden_chinese_link not in chinese_text, forbidden_chinese_link


def test_chapter_22_maturity_bar_links_inventory_and_artifacts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[утвержденный реестр](../../appendix/registry-operations-handbook.md)",
            "[доверенные артефакты](../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[approved inventory]"
            "(../../appendix/registry-operations-handbook.en.md) and "
            "[approved artifacts](../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[已批准清单](../../appendix/registry-operations-handbook.zh.md)"
            "和[已批准工件](../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_links_verifier_contract_to_eval_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "какой [контракт проверяющего](../../appendix/eval-schema.md)",
            "[verifier contracts](../../appendix/eval-schema.md)",
            "[verifier contract](../../appendix/eval-schema.md) не просто оценивает качество",
            "активного [verifier contract](../../appendix/eval-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "which [verifier contract](../../appendix/eval-schema.en.md)",
            "[verifier contracts](../../appendix/eval-schema.en.md)",
            "[verifier contract](../../appendix/eval-schema.en.md) does not merely score quality",
            "active [verifier contract](../../appendix/eval-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "哪一版[验证器契约（verifier contract）](../../appendix/eval-schema.zh.md)",
            "[验证器契约（verifier contract）](../../appendix/eval-schema.zh.md)",
            "[验证器契约（verifier contract）](../../appendix/eval-schema.zh.md)不只是给质量打分",
            "生效的[验证器契约（verifier contract）](../../appendix/eval-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        for expected_snippet in expected_snippets:
            _assert_file_contains(path, expected_snippet)


def test_chapter_22_links_grading_and_evidence_rules_to_eval_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[определения рубрик и правила связывания доказательной базы]"
            "(../../appendix/eval-schema.md)",
            "[рубрика оценки и правила связывания доказательной базы]"
            "(../../appendix/eval-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[grading rules and evidence-linkage rules]"
            "(../../appendix/eval-schema.en.md)",
            "[grading rubric and evidence-linkage rules]"
            "(../../appendix/eval-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[评分规则与证据链接规则](../../appendix/eval-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_links_session_and_delegation_rules_to_lifecycle_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[политика прерывания или истечения]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[режим делегированной авторизации, привязка принципала и политика отзыва]"
            "(../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[interruption or expiry policy]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[delegated authorization mode, principal binding, and revoke policy]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[中断或过期策略](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[委派授权模式、主体绑定与撤销策略"
            "（principal binding and revoke policy）]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)

    chinese_text = _read("docs/book/part-viii/chapter-22.zh.md")
    forbidden_chinese_link = (
        "[委派授权模式、principal 绑定与撤销策略]"
        "(../../appendix/lifecycle-artifact-schema.zh.md)"
    )
    assert forbidden_chinese_link not in chinese_text, forbidden_chinese_link


def test_chapter_22_links_orchestration_rules_to_change_rollout_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[управленческие правила для схемы оркестрации и определения "
            "безопасного каталога рабочих агентов]"
            "(../../appendix/change-rollout-schema.md)",
            "[схема оркестрации и политика границ рабочих агентов]"
            "(../../appendix/change-rollout-schema.md)",
            "[изменения в orchestration pattern]"
            "(../../appendix/change-rollout-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[orchestration-pattern governance rules and worker-safe catalog definitions]"
            "(../../appendix/change-rollout-schema.en.md)",
            "[orchestration pattern and worker-boundary policy]"
            "(../../appendix/change-rollout-schema.en.md)",
            "[orchestration-pattern governance changes]"
            "(../../appendix/change-rollout-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[编排模式治理规则与工作者安全目录定义"
            "（worker-safe catalog definitions）]"
            "(../../appendix/change-rollout-schema.zh.md)",
            "[编排模式与工作者边界策略（worker-boundary policy）]"
            "(../../appendix/change-rollout-schema.zh.md)",
            "[编排模式治理变更]"
            "(../../appendix/change-rollout-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)

    chinese_text = _read("docs/book/part-viii/chapter-22.zh.md")
    expected_chinese_marker = "以及工作者安全目录（worker-safe catalog）边界是否生效"
    assert expected_chinese_marker in chinese_text, expected_chinese_marker

    forbidden_chinese_links = (
        "[编排模式治理规则与 worker-safe 目录定义]"
        "(../../appendix/change-rollout-schema.zh.md)",
        "[编排模式治理规则与 worker-safe 目录定义"
        "（worker-safe catalog definitions）]"
        "(../../appendix/change-rollout-schema.zh.md)",
        "[编排模式与 worker 边界策略]"
        "(../../appendix/change-rollout-schema.zh.md)",
        "以及 worker-safe 目录边界是否生效",
    )
    for forbidden_chinese_link in forbidden_chinese_links:
        assert forbidden_chinese_link not in chinese_text, forbidden_chinese_link


def test_chapter_22_artifact_inventory_links_rollout_gate() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "утвержденный [шлюз поэтапного выпуска](../../appendix/change-rollout-schema.md)"
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "approved [rollout gate](../../appendix/change-rollout-schema.en.md)"
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "已批准的[发布门禁（rollout gate）]"
            "(../../appendix/change-rollout-schema.zh.md)"
        ),
    }

    for path, expected_snippet in expected_snippets_by_file.items():
        assert expected_snippet in _read(path), (path, expected_snippet)


def test_chapter_22_provenance_questions_link_retrieval_corpus() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "какой [корпус извлечения](../../appendix/memory-retrieval-schema.md) использовался",
            "[утвержденного корпуса извлечения](../../appendix/memory-retrieval-schema.md)",
            "[рубрики привязки к источникам, конфигурации клиентских фильтров, "
            "политики записи в память "
            "и подтверждения свежести](../../appendix/memory-retrieval-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "which [retrieval corpus](../../appendix/memory-retrieval-schema.en.md) was used",
            "[approved retrieval corpus](../../appendix/memory-retrieval-schema.en.md)",
            "[source-grounding rubric, tenant-filter config, memory-write policy, "
            "and freshness attestation](../../appendix/memory-retrieval-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "哪一版[检索语料（retrieval corpus）]"
            "(../../appendix/memory-retrieval-schema.zh.md)",
            "[已批准检索语料（approved retrieval corpus）]"
            "(../../appendix/memory-retrieval-schema.zh.md)",
            "[来源扎根评分规程、租户过滤配置、记忆写入策略与新鲜度证明"
            "（source-grounding rubric、tenant-filter config、memory-write policy "
            "和 freshness attestation）](../../appendix/memory-retrieval-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_duplicate_ticket_case_links_release_artifacts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[набора политик](../../appendix/policy-bundle-schema.md) для `side_effect_unknown`",
            "[контракта возможности](../../appendix/lifecycle-artifact-schema.md) "
            "`create_support_ticket`",
            "[шлюза поэтапного выпуска](../../appendix/change-rollout-schema.md), "
            "[схемы подтверждения](../../appendix/approval-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "`side_effect_unknown` [policy bundle](../../appendix/policy-bundle-schema.en.md)",
            "`create_support_ticket` [capability contract]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[rollout gate](../../appendix/change-rollout-schema.en.md), "
            "[approval schema](../../appendix/approval-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "`side_effect_unknown`[策略包（policy bundle）]"
            "(../../appendix/policy-bundle-schema.zh.md)",
            "`create_support_ticket`[能力契约（capability contract）]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[发布门禁（rollout gate）]"
            "(../../appendix/change-rollout-schema.zh.md)、"
            "[审批模式（approval schema）](../../appendix/approval-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_22_incident_case_spine_links_incident_artifacts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[набора политик эскалации, контракта уведомлений и карты ролей реагирующих]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[схемы состояния инцидента](../../appendix/incident-record-schema.md)",
            "[обновления артефактов после инцидента](../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[escalation-policy bundle, notification contract, and responder-role map]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[incident-state schema](../../appendix/incident-record-schema.en.md)",
            "[post-incident artifact update](../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[升级策略包、通知契约与响应者角色映射"
            "（escalation-policy bundle、notification contract、responder-role map）]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[事故状态模式](../../appendix/incident-record-schema.zh.md)",
            "[事故后工件更新（post-incident artifact update）]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)

    chinese_text = _read("docs/book/part-viii/chapter-22.zh.md")
    forbidden_chinese_link = (
        "[编排模式与工作器边界策略（worker-boundary policy）]"
        "(../../appendix/change-rollout-schema.zh.md)"
    )
    assert forbidden_chinese_link not in chinese_text, forbidden_chinese_link


def test_chapter_22_practical_checklist_links_artifact_version_contracts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[policy](../../appendix/policy-bundle-schema.md)-",
            "[approval](../../appendix/approval-schema.md)-",
            "[runtime-control](../../appendix/lifecycle-artifact-schema.md)-",
            "[eval- и verifier](../../appendix/eval-schema.md)-артефактов",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[policy](../../appendix/policy-bundle-schema.en.md)",
            "[approval-schema](../../appendix/approval-schema.en.md)",
            "[runtime-control](../../appendix/lifecycle-artifact-schema.en.md)",
            "[eval, and verifier](../../appendix/eval-schema.en.md) artifacts",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[策略](../../appendix/policy-bundle-schema.zh.md)",
            "[审批模式（approval-schema）](../../appendix/approval-schema.zh.md)",
            "[运行时控制（runtime-control）]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[评测和验证器](../../appendix/eval-schema.zh.md)工件",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)

    chinese_text = _read("docs/book/part-viii/chapter-22.zh.md")
    forbidden_chinese_links = (
        "[approval-schema](../../appendix/approval-schema.zh.md)",
        "[runtime-control](../../appendix/lifecycle-artifact-schema.zh.md)",
    )
    for forbidden_chinese_link in forbidden_chinese_links:
        assert forbidden_chinese_link not in chinese_text, forbidden_chinese_link


def test_chapter_22_chinese_rollout_labels_are_localized() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-22.zh.md")
    expected_markers = (
        "供应链纪律必须与事故复盘、变更管理和发布（rollout）连接起来",
        "之后的事故评审或发布（rollout）争议，可能都需要知道",
        "来源追踪能在事故评审和发布（rollout）决策中被快速恢复",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "供应链纪律必须与事故复盘、变更管理和 rollout 连接起来",
        "之后的事故评审或 rollout 争议，可能都需要知道",
        "来源追踪能在事故评审和 rollout 决策中被快速恢复",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chapter_22_chinese_evidence_labels_are_localized() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-22.zh.md")
    expected_markers = (
        "而不是泛泛的证据（evidence）文件夹",
        "发布或保障证据（evidence）中缺少[验证器契约血缘]",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "而不是泛泛的 evidence 文件夹",
        "发布或保障 evidence 中缺少[验证器契约血缘]",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chapter_22_chinese_evidence_spine_link_is_localized() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-22.zh.md")
    expected_markers = (
        "事故和发布（rollout）判断，可以直接打开",
        "打开[证据主干（Evidence Spine）](../part-v/evidence-spine.zh.md)",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "事故和 rollout 判断，可以直接打开",
        "打开 [Evidence Spine](../part-v/evidence-spine.zh.md)",
        "打开[Evidence Spine](../part-v/evidence-spine.zh.md)",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chapter_22_chinese_useful_ref_links_are_tightened() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-22.zh.md")
    expected_markers = (
        "可以直接查看[生命周期工件模式]",
        "策略包模式与审批契约](../../appendix/policy-bundle-schema.zh.md)和[变更评审与发布门禁模式]",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "可以直接查看 [生命周期工件模式]",
        "策略包模式与审批契约](../../appendix/policy-bundle-schema.zh.md) 和 "
        "[变更评审与发布门禁模式]",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chapter_22_useful_refs_include_supply_chain_schema_pages() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-22.md": (
            "[Схема approval](../../appendix/approval-schema.md)",
            "[Схема change review и rollout gate]"
            "(../../appendix/change-rollout-schema.md)",
            "[Схема наборов для оценки и правил проверки]"
            "(../../appendix/eval-schema.md)",
            "[Схема трасс и каталог событий](../../appendix/trace-schema.md)",
            "[Схема памяти и извлечения]"
            "(../../appendix/memory-retrieval-schema.md)",
        ),
        "docs/book/part-viii/chapter-22.en.md": (
            "[Approval Schema](../../appendix/approval-schema.en.md)",
            "[Change Review and Rollout Gate Schema]"
            "(../../appendix/change-rollout-schema.en.md)",
            "[Eval Dataset Schema and Grading Contract]"
            "(../../appendix/eval-schema.en.md)",
            "[Trace Schema and Event Catalog](../../appendix/trace-schema.en.md)",
            "[Memory and Retrieval Schema]"
            "(../../appendix/memory-retrieval-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-22.zh.md": (
            "[策略包模式与审批契约]"
            "(../../appendix/policy-bundle-schema.zh.md)",
            "[审批请求与决策记录模式](../../appendix/approval-schema.zh.md)",
            "[生命周期工件模式]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[变更评审与发布门禁模式]"
            "(../../appendix/change-rollout-schema.zh.md)",
            "[评测数据集模式与打分契约]"
            "(../../appendix/eval-schema.zh.md)",
            "[追踪模式与事件目录](../../appendix/trace-schema.zh.md)",
            "[记忆记录与检索契约模式]"
            "(../../appendix/memory-retrieval-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_24_misalignment_threads_three_canonical_cases() -> None:
    common_markers = (
        "Misalignment case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "risk scenario and control plan",
        "insider-risk surfaces",
        "separate tool principal",
        "tenant-filter bypass",
        "notification suppression",
    )
    expected_markers_by_file = {
        "docs/book/part-viii/chapter-24.md": (
            "Заметка о сквозных сценариях несоответствия целей",
            "Разбор обращений поддержки",
            "Внутренний ассистент знаний",
            "Координация инцидентов",
            "сценарий риска и план управления",
            "поверхности инсайдерского риска",
            "отдельного принципала инструмента",
            "обхода клиентских фильтров",
            "подавления уведомлений",
            "строгого окна замены с подтверждениями",
            "неизменяемой связи трасс",
            "отравления извлечения",
            "подмены состояния инцидента",
        ),
        "docs/book/part-viii/chapter-24.en.md": (
            *common_markers,
            "approval-tight replacement window",
            "immutable trace linkage",
            "retrieval poisoning",
            "incident-state tampering",
        ),
        "docs/book/part-viii/chapter-24.zh.md": (
            *common_markers,
            "失配案例主线说明（Misalignment case-spine note）",
            "风险场景与控制计划（risk scenario and control plan）",
            "规范案例（canonical cases）",
            "内部人风险表面（insider-risk surfaces）",
            "支持分诊（Support triage）",
            "内部知识助手（Internal knowledge assistant）",
            "事故协调（Incident coordination）",
            "独立工具主体（separate tool principal）",
            "写入能力族（write capability family）",
            "应急禁用（emergency disable）",
            "租户过滤绕过（tenant-filter bypass）",
            "隐藏记忆写入（hidden memory write）",
            "来源扎根规避（source-grounding evasion）",
            "遏制（containment）",
            "升级操纵（escalation manipulation）",
            "通知压制（notification suppression）",
            "响应者角色滥用（responder-role abuse）",
            "过渡期（transition periods）",
            "回滚（rollback）控制（controls）",
            "审批收紧替换窗口（approval-tight replacement window）",
            "不可变追踪链接（immutable trace linkage）",
            "检索投毒（retrieval poisoning）",
            "事故状态篡改（incident-state tampering）",
        ),
    }

    for path, expected_markers in expected_markers_by_file.items():
        text = _read(path)
        for expected_marker in expected_markers:
            assert expected_marker in text, (path, expected_marker)

    chinese_text = _read("docs/book/part-viii/chapter-24.zh.md")
    forbidden_chinese_markers = (
        "**Misalignment case-spine note：**",
        "risk scenario and control plan 应该",
        "三个 canonical cases",
        "Support triage 需要",
        "Internal knowledge assistant 需要",
        "Incident coordination 需要",
        "事件协调（Incident coordination）需要针对升级操纵",
        "不同 insider-risk surfaces 覆盖",
        "separate tool principal、",
        "面向 write capability family 的 emergency disable",
        "tenant-filter bypass、hidden memory write 和 source-grounding evasion",
        "escalation manipulation、notification suppression、responder-role abuse",
        "transition periods 中 rollback 的 controls",
    )
    for forbidden_chinese_marker in forbidden_chinese_markers:
        assert forbidden_chinese_marker not in chinese_text, forbidden_chinese_marker


def test_chapter_24_chinese_risk_surface_labels_are_localized() -> None:
    text = _read("docs/book/part-viii/chapter-24.zh.md")
    expected_markers = (
        "密钥（secrets）和记忆写入（memory writes）",
        "暂停审批（paused approval）与恢复路径",
        "能力会话（capability-session）中断与重新初始化路径",
        "编排模式（orchestration-pattern）选择与委派工作器（delegated worker）路径",
        "暂停审批路径（paused approval path）",
        "能力会话过期（capability-session expiry）或重新初始化路径（re-init path）",
        "后台路由（background routes）或可恢复路径（resumable paths）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in text, expected_marker

    forbidden_markers = (
        "secrets 和 memory writes",
        "paused approval 与恢复路径",
        "capability-session 中断与重新初始化路径",
        "orchestration-pattern 选择与 delegated worker 路径",
        "滥用 paused approval path",
        "capability-session expiry 或 re-init path",
        "background routes 或 resumable paths",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in text, forbidden_marker


def test_chapter_24_chinese_control_path_labels_are_localized() -> None:
    text = _read("docs/book/part-viii/chapter-24.zh.md")
    expected_markers = (
        "运行时控制路径（runtime-control paths）与受治理的契约版本（governed contract versions）",
        "模式（schema）或契约版本（contract version）迁移期间",
        "编排模式（orchestration pattern）或委派工作器路径（delegated worker path）",
        "模式漂移（schema drift）或契约不匹配（contract mismatch）",
        "能力会话重新初始化（capability-session re-init）在拒绝（denied）、"
        "允许（allowed）或审批绑定（approval-bound）",
        "编排模式滥用（orchestration-pattern misuse）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in text, expected_marker

    forbidden_markers = (
        "runtime-control paths 与 governed contract versions",
        "schema 或 contract version 迁移期间",
        "更弱的 orchestration pattern 或 delegated worker path",
        "schema drift 或 contract mismatch",
        "capability-session re-init 在 denied、allowed 或 approval-bound",
        "以及 orchestration-pattern misuse",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in text, forbidden_marker


def test_chapter_24_russian_control_path_labels_are_localized() -> None:
    text = _read("docs/book/part-viii/chapter-24.md")
    expected_markers = (
        "Как это меняет модель угроз",
        "сможет ли она увести исполнение в более слабую схему оркестрации "
        "или путь делегированного рабочего агента",
        "может ли изменение в среде исполнения сделать надзор слабее",
        "может ли дрейф схемы или рассогласование контрактов открыть более "
        "слабый контур управления",
        "есть ли у нас отдельные сигналы на поведение, похожее на саботаж",
        "умеем ли мы экстренно замораживать возможность, принципал или волну "
        "поэтапного выпуска",
        "ограниченная область действия каждой возможности",
        "отдельный принципал инструмента (`tool principal`) для действий "
        "высокого риска",
        "подтверждение конкретной полезной нагрузки",
        "явные правила для того, когда повторная инициализация сессии "
        "возможности запрещена, разрешена или привязана к подтверждению",
        "неизменяемая связь между `trace_id`, `approval_id`, "
        "`tool_principal`, `contract_version` и `artifact_bundle`",
        "аварийная остановка для семейства возможностей",
    )
    for expected_marker in expected_markers:
        assert expected_marker in text, expected_marker

    forbidden_markers = (
        "Как это меняет threat model",
        "execution в более слабый orchestration pattern или delegated worker path",
        "change в runtime сделать oversight слабее",
        "schema drift или contract mismatch открыть более слабый control path",
        "сигналы на sabotage-like behavior",
        "capability, principal или rollout wave",
        "ограниченный scope каждого capability",
        "отдельные `tool principal` для risky actions",
        "approval на конкретный payload",
        "явные controls для того, когда capability-session re-init denied, "
        "allowed или approval-bound",
        "immutable linkage между `trace_id`, `approval_id`, "
        "`tool_principal`, `contract_version` и `artifact_bundle`",
        "emergency stop для capability family",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in text, forbidden_marker


def test_chapter_24_chinese_maturity_checklist_labels_are_localized() -> None:
    text = _read("docs/book/part-viii/chapter-24.zh.md")
    expected_markers = (
        "专用主体（principals）、已链接的契约版本（contract versions）、"
        "受治理的重新初始化（re-init）行为与已评审的工作器边界（worker boundaries）",
        "发布（rollout）、替换（replacement）、退役（retirement）与"
        "编排模式变更（orchestration-pattern change）",
        "工件包（artifact bundle）和副作用（side effect）",
        "能力族（capability family），而不用等整套系统关闭（shutdown）",
        "能力族（capability family），而不是只能整套运行时（runtime）一起关",
        "审批路径滥用（approval-path misuse）、审批规避（approval evasion）、"
        "会话重新初始化滥用（session re-init misuse）与"
        "委派工作器滥用（delegated-worker misuse）",
        "中断（interruption）、模式迁移窗口（schema-transition windows）与"
        "编排模式变更（orchestration-pattern changes）",
        "同一个主体（principal）会不会同时出现在低风险（low-risk）和高风险（high-risk）路径里",
    )
    for expected_marker in expected_markers:
        assert expected_marker in text, expected_marker

    forbidden_markers = (
        "专用 principals、已链接的 contract versions",
        "rollout、replacement、retirement 与 orchestration-pattern change",
        "artifact bundle 和 side effect",
        "capability family，而不用等整套系统 shutdown",
        "capability family，而不是只能整套 runtime 一起关",
        "approval-path misuse、approval evasion、session re-init misuse 与 delegated-worker misuse",
        "interruption、schema-transition windows 与 orchestration-pattern changes",
        "同一个 principal 会不会同时出现在 low-risk 和 high-risk 路径里",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in text, forbidden_marker


def test_chapter_26_chinese_ticket_write_example_label_is_localized() -> None:
    text = _read("docs/book/part-viii/chapter-26.zh.md")
    expected_markers = (
        "贯穿案例：工单写入（ticket-write）控制评测的遥测（telemetry）",
        "工单写入路径（ticket-write paths）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in text, expected_marker

    forbidden_markers = (
        "贯穿案例：ticket-write 控制评测的遥测",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in text, forbidden_marker


def test_chapter_26_chinese_intro_artifact_label_is_localized() -> None:
    text = _read("docs/book/part-viii/chapter-26.zh.md")
    expected_markers = (
        "本章的主要工件是追踪与遥测覆盖记录（trace and telemetry coverage record）",
        "控制路径（control paths）与副作用（side effects）",
        "盲点（blind spots）的覆盖图",
    )
    for expected_marker in expected_markers:
        assert expected_marker in text, expected_marker

    forbidden_markers = (
        "本章的主要工件是 追踪与遥测覆盖记录",
        "本章的主要工件是 trace and telemetry coverage record",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in text, forbidden_marker


def test_chapter_25_chinese_ticket_write_example_label_is_localized() -> None:
    text = _read("docs/book/part-viii/chapter-25.zh.md")
    expected_markers = (
        "贯穿案例：工单写入（ticket-write）的控制评测",
        "工单写入能力族（ticket-write capability family）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in text, expected_marker

    forbidden_markers = (
        "贯穿案例：ticket-write 的控制评测",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in text, forbidden_marker


def test_chapter_25_chinese_verifier_labels_are_localized() -> None:
    text = _read("docs/book/part-viii/chapter-25.zh.md")
    expected_markers = (
        "计算机使用智能体（computer-use agents）",
        "二元裁决（binary verdict）",
        "过程验证（process verification）和结果验证（outcome verification）",
        "分数（score）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in text, expected_marker

    forbidden_markers = (
        "过程验证（`process verification`）",
        "结果验证（`outcome verification`）",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in text, forbidden_marker


def test_chapter_25_chinese_intro_artifact_label_is_localized() -> None:
    text = _read("docs/book/part-viii/chapter-25.zh.md")
    expected_markers = (
        "本章的主要工件是评测门禁与验证器契约（eval gate and verifier contract）",
        "事故响应（incident response），也不是泛泛的遥测（telemetry）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in text, expected_marker

    forbidden_markers = (
        "本章的主要工件是 评测门禁与验证器契约",
        "本章的主要工件是 eval gate and verifier contract",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in text, forbidden_marker


def test_chapter_24_chinese_intro_artifact_labels_are_localized() -> None:
    text = _read("docs/book/part-viii/chapter-24.zh.md")
    expected_markers = (
        "智能体失配（`agentic misalignment`）",
        "本章的主要工件是风险场景与控制计划（risk scenario and control plan）",
        "误用路径（misuse path）、受影响权限、控制（controls）、"
        "遏制（containment）与监控（monitoring）",
        "提示注入（prompt-injection）指南",
    )
    for expected_marker in expected_markers:
        assert expected_marker in text, expected_marker

    forbidden_markers = (
        "称为 `agentic misalignment`",
        "本章的主要工件是 风险场景",
        "描述 misuse path、受影响权限、controls、containment 与 monitoring",
        "prompt-injection 指南",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in text, forbidden_marker


def test_chapter_24_chinese_identifier_labels_are_localized() -> None:
    text = _read("docs/book/part-viii/chapter-24.zh.md")
    expected_markers = (
        "独立的工具主体（`tool principal`）",
        "追踪编号（`trace_id`）、审批编号（`approval_id`）、"
        "工具主体（`tool_principal`）、契约版本（`contract_version`）与"
        "工件包（`artifact_bundle`）",
        "审批编号（`approval_id`）与工具主体（`tool_principal`）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in text, expected_marker

    forbidden_markers = (
        "使用独立的 `tool principal`",
        "`trace_id`、`approval_id`、`tool_principal`、`contract_version` 与 `artifact_bundle`",
        "具体的 `approval_id` 与 `tool_principal`",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in text, forbidden_marker


def test_chapter_24_chinese_control_principle_labels_are_localized() -> None:
    text = _read("docs/book/part-viii/chapter-24.zh.md")
    expected_markers = (
        "人类控制者（human controllers）、有限权力（limited powers）和"
        "可观察动作（observable actions）",
        "中断（interruption）、过期（expiry）或重新初始化语义（re-init semantics）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in text, expected_marker

    forbidden_markers = (
        "原则：human controllers、limited powers 和 observable actions",
        "利用 interruption、expiry 或 re-init semantics",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in text, forbidden_marker


def test_chapter_24_chinese_diagram_labels_are_localized() -> None:
    text = _read("docs/book/part-viii/chapter-24.zh.md")
    expected_markers = (
        "目标压力（Goal pressure）",
        "模型行为（Model behavior）",
        "受限访问（Restricted access）",
        "替换或评审压力（Replacement or review pressure）",
        "隐藏尝试（Concealment attempt）",
        "审批规避（Approval evasion）",
        "替代工具路径（Alternative tool path）",
        "检测与遏制（Detection and containment）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in text, expected_marker

    forbidden_markers = (
        'A["Goal pressure"]',
        'D["Model behavior"]',
        'B["Restricted access"]',
        'C["Replacement or review pressure"]',
        'E["Concealment attempt"]',
        'F["Approval evasion"]',
        'G["Alternative tool path"]',
        'H["Detection and containment"]',
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in text, forbidden_marker


def test_chapter_24_misalignment_useful_refs_include_risk_evidence_contracts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-24.md": (
            "[Схема трасс и каталог событий](../../appendix/trace-schema.md)",
            "[Схема наборов для оценки и правил проверки]"
            "(../../appendix/eval-schema.md)",
            "[Схема памяти и извлечения]"
            "(../../appendix/memory-retrieval-schema.md)",
        ),
        "docs/book/part-viii/chapter-24.en.md": (
            "[Trace Schema and Event Catalog](../../appendix/trace-schema.en.md)",
            "[Eval Dataset Schema and Grading Contract]"
            "(../../appendix/eval-schema.en.md)",
            "[Memory and Retrieval Schema]"
            "(../../appendix/memory-retrieval-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-24.zh.md": (
            "[审批请求与决策记录模式](../../appendix/approval-schema.zh.md)",
            "[生命周期工件模式]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[追踪模式与事件目录](../../appendix/trace-schema.zh.md)",
            "[评测数据集模式与打分契约]"
            "(../../appendix/eval-schema.zh.md)",
            "[记忆记录与检索契约模式]"
            "(../../appendix/memory-retrieval-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_24_misalignment_case_spine_links_are_clickable() -> None:
    expected_links_by_file = {
        "docs/book/part-viii/chapter-24.md": (
            "../../appendix/change-rollout-schema.md",
            "../../appendix/trace-schema.md",
            "../../appendix/memory-retrieval-schema.md",
            "../../appendix/incident-record-schema.md",
        ),
        "docs/book/part-viii/chapter-24.en.md": (
            "../../appendix/change-rollout-schema.en.md",
            "../../appendix/trace-schema.en.md",
            "../../appendix/memory-retrieval-schema.en.md",
            "../../appendix/incident-record-schema.en.md",
        ),
        "docs/book/part-viii/chapter-24.zh.md": (
            "../../appendix/change-rollout-schema.zh.md",
            "../../appendix/trace-schema.zh.md",
            "../../appendix/memory-retrieval-schema.zh.md",
            "../../appendix/incident-record-schema.zh.md",
        ),
    }

    for path, expected_links in expected_links_by_file.items():
        text = _read(path)
        for expected_link in expected_links:
            assert f"]({expected_link})" in text, (path, expected_link)

    chinese_text = _read("docs/book/part-viii/chapter-24.zh.md")
    expected_chinese_links = (
        "[审批收紧替换窗口（approval-tight replacement window）]"
        "(../../appendix/change-rollout-schema.zh.md)",
        "[不可变追踪链接（immutable trace linkage）]"
        "(../../appendix/trace-schema.zh.md)",
        "[检索投毒（retrieval poisoning）]"
        "(../../appendix/memory-retrieval-schema.zh.md)",
        "[事故状态篡改（incident-state tampering）]"
        "(../../appendix/incident-record-schema.zh.md)",
    )
    for expected_chinese_link in expected_chinese_links:
        assert expected_chinese_link in chinese_text, expected_chinese_link
    forbidden_chinese_links = (
        "[approval-tight replacement window]"
        "(../../appendix/change-rollout-schema.zh.md)",
        "[immutable trace linkage](../../appendix/trace-schema.zh.md)",
        "[retrieval poisoning](../../appendix/memory-retrieval-schema.zh.md)",
        "[incident-state tampering](../../appendix/incident-record-schema.zh.md)",
    )
    for forbidden_chinese_link in forbidden_chinese_links:
        assert forbidden_chinese_link not in chinese_text, forbidden_chinese_link


def test_chapter_25_chinese_verifier_control_labels_are_localized() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-25.zh.md")
    expected_markers = (
        "契约版本纪律（contract-version discipline）",
        "发布决策（rollout decisions）",
        "发布（rollout）和训练循环（training loops）",
        "辅助提示词（helper prompt）",
        "验证器契约替换（verifier contract swaps）",
        "验证器契约版本变更（verifier contract version changes）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "contract-version discipline 和 rollout decisions",
        "rollout 和 training loops",
        "方便的 helper prompt",
        "这也包括 verifier contract swaps",
        "未经审查的 verifier contract version changes",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chapter_25_chinese_intro_layer_labels_are_localized() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-25.zh.md")
    expected_markers = (
        "行为评测（`behavioral evals`）",
        "控制评测（`control evals`）",
        "自动化红队测试（`automated red teaming`）",
        "发布（rollout）",
        "保障（assurance）",
        "出处（provenance）",
        "治理（governance）",
        "事故响应（incident response）",
        "遥测（telemetry）",
        "过程验证（process verification）",
        "结果验证（outcome verification）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "- `behavioral evals`",
        "- `control evals`",
        "- `automated red teaming`",
        "转化成 rollout、assurance、provenance 与 governance",
        "而不是 incident response，也不是泛泛的 telemetry",
        "把 `process verification` 和 `outcome verification` 分开",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chapter_25_chinese_evidence_model_labels_are_localized() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-25.zh.md")
    expected_markers = (
        "通过/失败裁决（pass/fail verdict）",
        "发现结果（findings）",
        "证据（evidence）",
        "控制证据（control evidence）",
        "风险轨迹（risky trajectories）",
        "评测（evals）",
        "最终答案（final answers）",
        "智能体评测（agent-eval）",
        "追踪（traces）",
        "轨迹（trajectories）",
        "发布门禁（rollout gates）",
        "场景类别（scenario classes）",
        "验证器契约（verifier contracts）",
        "有追踪支持的失败（trace-backed failures）",
        "行为证据（behavioral evidence）",
        "控制评测（control evals）",
        "自动化红队测试（automated red teaming）",
        "判断系统（judgment system）",
        "模拟器质量（simulator quality）",
        "裁判模型（judge models）",
        "红队生成（red-team generation）",
        "过程失败（process failure）",
        "结果失败（outcome failure）",
        "控制失败（control failure）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "pass/fail verdict，而是分开的过程/结果判断",
        "响应 findings",
        "保存 evidence",
        "一层 control evidence",
        "针对 risky trajectories 的 evals",
        "不只是 final answers",
        "现代 agent-eval 材料",
        "把 traces、trajectories 与 rollout gates",
        "scenario classes、verifier contracts、trace-backed failures 与 rollout gates",
        "behavioral 和 control evidence",
        "behavioral evals、control evals 与 automated red teaming",
        "judgment system 中的不同角色",
        "simulator quality、judge models 与 red-team generation",
        "process failure、outcome failure 与 control failure",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chapter_25_chinese_scenario_source_labels_are_localized() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-25.zh.md")
    expected_markers = (
        "暂停/恢复（pause/resume）",
        "后台执行（background execution）",
        "运行时控制转换（runtime-control transitions）",
        "能力会话到期（capability-session expiry）",
        "重新初始化路径（re-initialization paths）",
        "编排模式选择（orchestration-pattern selection）",
        "委派工作者边界（delegated worker boundaries）",
        "`user simulator`（用户模拟器）",
        "`synthetic adversary`（合成对手）",
        "模拟器（simulator）",
        "对手（adversary）",
        "隐蔽（concealment）",
        "监督规避（oversight evasion）",
        "模式不匹配（schema mismatch）",
        "控制漂移（control drift）",
        "重新初始化窗口（re-init windows）",
        "委派工作者路径（delegated worker paths）",
        "工作者边界漂移（worker-boundary drift）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "涉及 pause/resume 或 background execution 的 runtime-control transitions",
        "capability-session expiry 与 re-initialization paths",
        "orchestration-pattern selection 与 delegated worker boundaries",
        "`user simulator` 适合",
        "`synthetic adversary` 适合",
        "simulator 提供更真实的任务分布",
        "adversary 提供压力测试",
        "- concealment；",
        "- oversight evasion；",
        "schema mismatch 或 control drift",
        "interruption 或 re-init windows",
        "delegated worker paths 的滥用或 worker-boundary drift",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chapter_25_chinese_control_question_labels_are_localized() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-25.zh.md")
    expected_markers = (
        "计算机使用智能体（computer-use agents）",
        "二元裁决（binary verdict）",
        "分数（score）",
        "契约漂移（contract drift）",
        "模式不匹配（schema mismatch）",
        "中断（interruption）",
        "到期（expiry）",
        "重新初始化语义（re-init semantics）",
        "评分规约（rubric）",
        "单一裁决（verdict）",
        "暂停运行与后台运行控制（paused-run and background-run controls）",
        "能力会话到期与重新初始化控制（capability-session expiry and re-init controls）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "computer-use agents 验证器设计",
        "二元 verdict 往往太弱",
        "压成一个 score",
        "利用 contract drift 或 schema mismatch",
        "interruption、expiry 或 re-init semantics",
        "可评审的 rubric，而不是不透明的单一 verdict",
        "paused-run 与 background-run controls",
        "capability-session expiry 与 re-init controls",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chapter_25_chinese_control_maturity_labels_are_localized() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-25.zh.md")
    expected_markers = (
        "审批路径误用（approval-path misuse）",
        "会话重新初始化误用（session re-init misuse）",
        "委派工作者误用（delegated-worker misuse）",
        "契约漂移（contract drift）",
        "验证器输出（verifier outputs）",
        "通过/失败标签（pass/fail label）",
        "验证器契约替换（verifier contract swaps）",
        "评分行为（grading behavior）",
        "承载发布的评测回归（release-bearing eval regressions）",
        "可控失败（controllable failures）",
        "不可控失败（uncontrollable failures）",
        "运行时控制回归（runtime-control regressions）",
        "发布（rollout）或事故（incidents）",
        "对抗提示（adversarial prompts）",
        "红队发现（red-team findings）",
        "变更门禁（change gates）",
        "真实负载模拟（realistic simulation）",
        "对抗生成（adversarial generation）",
        "发布（rollout）、保障（assurance）",
        "契约版本匹配（contract-version matching）",
        "运行时控制行为（runtime-control behavior）",
        "编排模式边界（orchestration-pattern boundaries）",
        "真实负载模拟器（realistic workload simulator）",
        "对抗生成器（adversarial generator）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "approval-path misuse、session re-init misuse、delegated-worker misuse",
        "contract drift 没有被显式测试",
        "verifier outputs 把长轨迹压缩成了过于薄弱的 pass/fail label",
        "verifier contract swaps 改变了 grading behavior",
        "当成 release-bearing eval regressions",
        "controllable 与 uncontrollable failures 没有被分开",
        "runtime-control regressions 只有在 rollout 或 incidents",
        "几条 adversarial prompts",
        "contract drift 与 runtime-control regressions 都有明确的场景覆盖",
        "red-team findings 会进入 rollout 和 change gates",
        "realistic simulation 和 adversarial generation",
        "让 rollout、assurance 与治理函数",
        "approval-path misuse 与 delegated-worker misuse",
        "contract-version matching、runtime-control behavior、orchestration-pattern boundaries",
        "realistic workload simulator 和 adversarial generator",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chapter_25_chinese_eval_layer_labels_are_localized() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-25.zh.md")
    expected_markers = (
        "追踪分级（trace grading）",
        "运行时控制评测（runtime-control evals）",
        "暂停/恢复（pause/resume）",
        "后台执行（background）",
        "能力会话到期/重新初始化（capability-session expiry/re-init）",
        "契约版本行为（contract-version behavior）",
        "编排模式行为（orchestration-pattern behavior）",
        "智能体评测（agent evals）",
        "工作流（workflow）",
        "追踪（traces）",
        "结构化评分器（structured graders）",
        "工具选择（tool choice）",
        "交接（handoff）",
        "护栏（guardrail）",
        "指令遵循失败（instruction-following failures）",
        "数据集（datasets）",
        "评测运行（eval runs）",
        "回归测试框架（regression harness）",
        "智能体程序（agent program）",
        "路由规则（routing rule）",
        "工具表面（tool surface）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "trace grading。",
        "runtime-control evals 还要验证 pause/resume",
        "background、capability-session expiry/re-init",
        "contract-version behavior，以及 orchestration-pattern behavior",
        "agent evals 的指南",
        "单个 workflow 行为时先从 traces 开始",
        "用 structured graders 评估 tool choice、handoff、guardrail",
        "guardrail 和 instruction-following failures",
        "迁移到 datasets 和可重复的 eval runs",
        "trace grading 是显微镜",
        "datasets 和 eval runs 是 regression harness",
        "成熟的 agent 程序",
        "traces 解释某一次 run 为什么失败",
        "新的 prompt、policy、routing rule 或 tool surface",
        "一类 runs，同时没有削弱其他地方的 controls",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chapter_25_control_evals_threads_three_canonical_cases() -> None:
    common_markers = (
        "Control-eval case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "behavioral and control eval surfaces",
        "payload-mutation check",
        "source-grounding eval",
        "notification suppression probe",
        "rollback control eval",
    )
    expected_markers_by_file = {
        "docs/book/part-viii/chapter-25.md": (
            "Заметка о сквозных сценариях контрольных оценок",
            "Разбор обращений поддержки",
            "Внутренний ассистент знаний",
            "Координация инцидентов",
            "поверхности поведенческих и контрольных оценок",
            "проверки изменения полезной нагрузки",
            "оценки привязки к источникам",
            "пробы подавления уведомлений",
            "контрольной оценки отката",
            "оценочный шлюз и контракт проверяющего",
            "проверки злоупотребления путем подтверждения",
            "сценария отравления извлечения",
        ),
        "docs/book/part-viii/chapter-25.en.md": (
            *common_markers,
            "eval schema",
            "eval gate and verifier contract",
            "approval-path misuse check",
            "retrieval-poisoning scenario",
        ),
        "docs/book/part-viii/chapter-25.zh.md": (
            *common_markers,
            "控制评测案例主线说明（Control-eval case-spine note）",
            "规范案例（canonical cases）",
            "支持分诊（Support triage）",
            "内部知识助手（Internal knowledge assistant）",
            "事故协调（Incident coordination）",
            "评测模式（eval schema）",
            "评测门禁与验证器契约（eval gate and verifier contract）",
            "[评测门禁与验证器契约（eval gate and verifier contract）]"
            "(../../appendix/eval-schema.zh.md)应该把",
            "行为与控制评测表面（behavioral and control eval surfaces）",
            "重复预防（duplicate prevention）",
            "载荷变更检查（payload-mutation check）",
            "旧网关路由探针（old-gateway-route probe）",
            "应急禁用断言（emergency-disable assertion）",
            "来源扎根评测（source-grounding eval）",
            "租户过滤绕过探针（tenant-filter bypass probe）",
            "不当记忆写入检查（improper-memory-write check）",
            "新鲜度回归门禁（freshness regression gate）",
            "升级路径检查（escalation-path check）",
            "通知压制探针（notification suppression probe）",
            "响应者角色滥用场景（responder-role abuse scenario）",
            "回滚控制评测（rollback control eval）",
            "审批路径误用检查（approval-path misuse check）",
            "检索投毒场景（retrieval-poisoning scenario）",
            "事故状态篡改检查（incident-state tampering check）",
        ),
    }

    for path, expected_markers in expected_markers_by_file.items():
        text = _read(path)
        for expected_marker in expected_markers:
            assert expected_marker in text, (path, expected_marker)

    chinese_text = _read("docs/book/part-viii/chapter-25.zh.md")
    forbidden_chinese_link = "[eval schema](../../appendix/eval-schema.zh.md)"
    assert forbidden_chinese_link not in chinese_text, forbidden_chinese_link
    forbidden_chinese_markers = (
        "**Control-eval case-spine note：**",
        "三个 canonical cases",
        "Support triage 需要",
        "Internal knowledge assistant 需要",
        "Incident coordination 需要",
        "事件协调（Incident coordination）需要升级路径检查",
        "不同 behavioral and control eval surfaces",
        "[评测门禁与验证器契约（eval gate and verifier contract）]"
        "(../../appendix/eval-schema.zh.md) 应该把",
        "需要 duplicate prevention、payload-mutation check",
        "old-gateway-route probe 和 emergency-disable assertion",
        "需要 source-grounding eval、tenant-filter bypass probe",
        "improper-memory-write check、",
        "freshness regression gate。Incident coordination",
        "notification suppression probe、responder-role abuse scenario",
        "和 rollback control eval",
    )
    for forbidden_chinese_marker in forbidden_chinese_markers:
        assert forbidden_chinese_marker not in chinese_text, forbidden_chinese_marker


def test_chapter_25_useful_refs_include_control_surface_contracts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-25.md": (
            "[Схема approval](../../appendix/approval-schema.md)",
            "[Схема артефактов жизненного цикла]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[Схема памяти и извлечения]"
            "(../../appendix/memory-retrieval-schema.md)",
        ),
        "docs/book/part-viii/chapter-25.en.md": (
            "[Approval Schema](../../appendix/approval-schema.en.md)",
            "[Lifecycle Artifact Schema]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[Memory and Retrieval Schema]"
            "(../../appendix/memory-retrieval-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-25.zh.md": (
            "[评测数据集模式与打分契约](../../appendix/eval-schema.zh.md)",
            "[审批请求与决策记录模式](../../appendix/approval-schema.zh.md)",
            "[生命周期工件模式]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[记忆记录与检索契约模式]"
            "(../../appendix/memory-retrieval-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_25_control_eval_case_spine_links_are_clickable() -> None:
    expected_links_by_file = {
        "docs/book/part-viii/chapter-25.md": (
            "../../appendix/eval-schema.md",
            "../../appendix/approval-schema.md",
            "../../appendix/memory-retrieval-schema.md",
            "../../appendix/incident-record-schema.md",
        ),
        "docs/book/part-viii/chapter-25.en.md": (
            "../../appendix/eval-schema.en.md",
            "../../appendix/approval-schema.en.md",
            "../../appendix/memory-retrieval-schema.en.md",
            "../../appendix/incident-record-schema.en.md",
        ),
        "docs/book/part-viii/chapter-25.zh.md": (
            "../../appendix/eval-schema.zh.md",
            "../../appendix/approval-schema.zh.md",
            "../../appendix/memory-retrieval-schema.zh.md",
            "../../appendix/incident-record-schema.zh.md",
        ),
    }

    for path, expected_links in expected_links_by_file.items():
        text = _read(path)
        for expected_link in expected_links:
            assert f"]({expected_link})" in text, (path, expected_link)

    chinese_text = _read("docs/book/part-viii/chapter-25.zh.md")
    expected_chinese_links = (
        "[评测门禁与验证器契约（eval gate and verifier contract）]"
        "(../../appendix/eval-schema.zh.md)",
        "[审批路径误用检查（approval-path misuse check）]"
        "(../../appendix/approval-schema.zh.md)",
        "[检索投毒场景（retrieval-poisoning scenario）]"
        "(../../appendix/memory-retrieval-schema.zh.md)",
        "[事故状态篡改检查（incident-state tampering check）]"
        "(../../appendix/incident-record-schema.zh.md)",
    )
    for expected_chinese_link in expected_chinese_links:
        assert expected_chinese_link in chinese_text, expected_chinese_link
    forbidden_chinese_links = (
        "[eval gate and verifier contract](../../appendix/eval-schema.zh.md)",
        "[approval-path misuse check](../../appendix/approval-schema.zh.md)",
        "[retrieval-poisoning scenario](../../appendix/memory-retrieval-schema.zh.md)",
        "[incident-state tampering check](../../appendix/incident-record-schema.zh.md)",
    )
    for forbidden_chinese_link in forbidden_chinese_links:
        assert forbidden_chinese_link not in chinese_text, forbidden_chinese_link


def test_chapter_26_observability_threads_three_canonical_cases() -> None:
    common_markers = (
        "Observability case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "observability coverage",
        "ticket-write paths",
        "bypass blind spots",
        "source-grounding verdicts",
        "verifier evidence",
        "notification delivery",
    )
    expected_markers_by_file = {
        "docs/book/part-viii/chapter-26.md": (
            "Заметка о сквозных сценариях наблюдаемости",
            "Разбор обращений поддержки",
            "Внутренний ассистент знаний",
            "Координация инцидентов",
            "покрытие наблюдаемостью",
            "путей записи тикетов",
            "слепых зон обхода",
            "вердиктов привязки к источникам",
            "доказательную базу",
            "доставки уведомлений",
            "запись покрытия трассировкой и телеметрией",
            "происхождения извлечения",
            "изменений контроля после инцидента",
        ),
        "docs/book/part-viii/chapter-26.en.md": (
            *common_markers,
            "trace and telemetry coverage record",
            "retrieval provenance",
            "post-incident control changes",
        ),
        "docs/book/part-viii/chapter-26.zh.md": (
            "可观测性案例主线说明（Observability case-spine note）",
            "支持分诊（support-triage）的控制评测",
            "追踪（trace）都应该关联",
            "支持分诊（Support triage）",
            "内部知识助手（Internal knowledge assistant）",
            "事故协调（Incident coordination）",
            "遥测（telemetry）已经具备检测就绪状态（detection-ready）",
            "发布（rollout）",
            "结果（outcome）",
            "过程/结果验证器裁决（process/outcome verifier verdict）",
            "工单写入路径（ticket-write paths）",
            "绕过路径（bypass path）盲区",
            "金丝雀（canary）",
            "追踪与遥测覆盖记录（trace and telemetry coverage record）",
            "[追踪与遥测覆盖记录（trace and telemetry coverage record）]"
            "(../../appendix/trace-schema.zh.md)应该展示",
            "规范案例（canonical cases）的可观测性覆盖（observability coverage）",
            "重复结果（duplicate outcome）",
            "绕过盲点（bypass blind spots）",
            "需要覆盖[检索来源追踪（retrieval provenance）]",
            "检索来源追踪（retrieval provenance）",
            "来源扎根裁决（source-grounding verdicts）",
            "租户过滤决策（tenant-filter decisions）",
            "新鲜度漂移（freshness drift）",
            "升级路径（escalation path）",
            "通知送达（notification delivery）",
            "响应者角色身份（responder-role identity）",
            "回滚事件（rollback events）",
            "和[事故后控制变更（post-incident control changes）]",
            "事故后控制变更（post-incident control changes）",
        ),
    }

    for path, expected_markers in expected_markers_by_file.items():
        text = _read(path)
        for expected_marker in expected_markers:
            assert expected_marker in text, (path, expected_marker)

    chinese_text = _read("docs/book/part-viii/chapter-26.zh.md")
    forbidden_chinese_markers = (
        "support-triage 的控制评测",
        "trace 都应该关联",
        "**Observability case-spine note：**",
        "Support triage 需要覆盖",
        "Internal knowledge assistant 需要覆盖",
        "Incident coordination 需要覆盖",
        "telemetry 已经 detection-ready",
        "服务 rollout",
        "`rollout_wave`、outcome、`side_effect_unknown`",
        "以及 process/outcome verifier verdict",
        "ticket-write paths 中有多少真正可观测",
        "盲区 bypass path",
        "canary 是否可以安全扩大",
        "三个 canonical cases 的 observability coverage",
        "[追踪与遥测覆盖记录（trace and telemetry coverage record）]"
        "(../../appendix/trace-schema.zh.md) 应该展示",
        "duplicate outcome 和 bypass blind spots",
        "source-grounding verdicts、tenant-filter decisions",
        "需要覆盖 [检索来源追踪",
        "memory-write events）](../../appendix/memory-retrieval-schema.zh.md) 和新鲜度漂移",
        "和 [事故后控制变更",
        "和 freshness drift",
        "覆盖 escalation path、notification delivery、responder-role identity",
        "rollback events 和",
    )
    for forbidden_chinese_marker in forbidden_chinese_markers:
        assert forbidden_chinese_marker not in chinese_text, forbidden_chinese_marker


def test_chapter_26_useful_refs_include_observability_contracts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-26.md": (
            "[Схема approval](../../appendix/approval-schema.md)",
            "[Схема артефактов жизненного цикла]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[Схема памяти и извлечения]"
            "(../../appendix/memory-retrieval-schema.md)",
        ),
        "docs/book/part-viii/chapter-26.en.md": (
            "[Approval Schema](../../appendix/approval-schema.en.md)",
            "[Lifecycle Artifact Schema]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[Memory and Retrieval Schema]"
            "(../../appendix/memory-retrieval-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-26.zh.md": (
            "[审批请求与决策记录模式](../../appendix/approval-schema.zh.md)",
            "[生命周期工件模式]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[记忆记录与检索契约模式]"
            "(../../appendix/memory-retrieval-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_26_observability_case_spine_links_are_clickable() -> None:
    expected_links_by_file = {
        "docs/book/part-viii/chapter-26.md": (
            "../../appendix/trace-schema.md",
            "../../appendix/approval-schema.md",
            "../../appendix/policy-bundle-schema.md",
            "../../appendix/memory-retrieval-schema.md",
            "../../appendix/incident-record-schema.md",
            "../../appendix/lifecycle-artifact-schema.md",
        ),
        "docs/book/part-viii/chapter-26.en.md": (
            "../../appendix/trace-schema.en.md",
            "../../appendix/approval-schema.en.md",
            "../../appendix/policy-bundle-schema.en.md",
            "../../appendix/memory-retrieval-schema.en.md",
            "../../appendix/incident-record-schema.en.md",
            "../../appendix/lifecycle-artifact-schema.en.md",
        ),
        "docs/book/part-viii/chapter-26.zh.md": (
            "../../appendix/trace-schema.zh.md",
            "../../appendix/approval-schema.zh.md",
            "../../appendix/policy-bundle-schema.zh.md",
            "../../appendix/memory-retrieval-schema.zh.md",
            "../../appendix/incident-record-schema.zh.md",
            "../../appendix/lifecycle-artifact-schema.zh.md",
        ),
    }

    for path, expected_links in expected_links_by_file.items():
        text = _read(path)
        for expected_link in expected_links:
            assert f"]({expected_link})" in text, (path, expected_link)

    chinese_text = _read("docs/book/part-viii/chapter-26.zh.md")
    expected_chinese_links = (
        "[追踪与遥测覆盖记录（trace and telemetry coverage record）]"
        "(../../appendix/trace-schema.zh.md)",
        "[审批链接（approval linkage）](../../appendix/approval-schema.zh.md)",
        "[检索来源追踪（retrieval provenance）]"
        "(../../appendix/memory-retrieval-schema.zh.md)",
        "[记忆写入事件（memory-write events）]"
        "(../../appendix/memory-retrieval-schema.zh.md)",
        "[事故状态转换（incident-state transitions）]"
        "(../../appendix/incident-record-schema.zh.md)",
        "[事故后控制变更（post-incident control changes）]"
        "(../../appendix/lifecycle-artifact-schema.zh.md)",
    )
    for expected_chinese_link in expected_chinese_links:
        assert expected_chinese_link in chinese_text, expected_chinese_link
    forbidden_chinese_links = (
        "[trace and telemetry coverage record](../../appendix/trace-schema.zh.md)",
        "[approval linkage](../../appendix/approval-schema.zh.md)",
        "[retrieval provenance](../../appendix/memory-retrieval-schema.zh.md)",
        "[memory-write events](../../appendix/memory-retrieval-schema.zh.md)",
        "[incident-state transitions](../../appendix/incident-record-schema.zh.md)",
        "[post-incident control changes]"
        "(../../appendix/lifecycle-artifact-schema.zh.md)",
    )
    for forbidden_chinese_link in forbidden_chinese_links:
        assert forbidden_chinese_link not in chinese_text, forbidden_chinese_link


def test_chapter_26_verifier_evidence_eval_link_is_clickable() -> None:
    expected_links_by_file = {
        "docs/book/part-viii/chapter-26.md": "../../appendix/eval-schema.md",
        "docs/book/part-viii/chapter-26.en.md": "../../appendix/eval-schema.en.md",
        "docs/book/part-viii/chapter-26.zh.md": "../../appendix/eval-schema.zh.md",
    }

    for path, expected_link in expected_links_by_file.items():
        assert f"]({expected_link})" in _read(path), (path, expected_link)


def test_chapter_26_governance_action_record_link_is_localized() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-26.md": (
            "[governance action record](../../appendix/trace-schema.md)"
        ),
        "docs/book/part-viii/chapter-26.en.md": (
            "[governance action record](../../appendix/trace-schema.en.md)"
        ),
        "docs/book/part-viii/chapter-26.zh.md": (
            "[治理动作记录（governance action record）]"
            "(../../appendix/trace-schema.zh.md)"
        ),
    }

    for path, expected_snippet in expected_snippets_by_file.items():
        _assert_file_contains(path, expected_snippet)

    chinese_text = _read("docs/book/part-viii/chapter-26.zh.md")
    forbidden_chinese_link = (
        "[governance action record](../../appendix/trace-schema.zh.md)"
    )
    assert forbidden_chinese_link not in chinese_text, forbidden_chinese_link


def test_chapter_26_weak_evidence_layer_links_verifier_evidence() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-26.md": (
            "и [verifier evidence](../../appendix/eval-schema.md) о том"
        ),
        "docs/book/part-viii/chapter-26.en.md": (
            "and [verifier evidence](../../appendix/eval-schema.en.md) for how"
        ),
        "docs/book/part-viii/chapter-26.zh.md": (
            "的[验证器证据（verifier evidence）](../../appendix/eval-schema.zh.md)，那它也许"
        ),
    }

    for path, expected_snippet in expected_snippets_by_file.items():
        _assert_file_contains(path, expected_snippet)


def test_chapter_26_observability_breakages_link_verifier_evidence() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-26.md": (
            "[verifier evidence](../../appendix/eval-schema.md) оторван"
        ),
        "docs/book/part-viii/chapter-26.en.md": (
            "[verifier evidence](../../appendix/eval-schema.en.md) is detached"
        ),
        "docs/book/part-viii/chapter-26.zh.md": (
            "[验证器证据（verifier evidence）](../../appendix/eval-schema.zh.md)与追踪（traces）"
        ),
    }

    for path, expected_snippet in expected_snippets_by_file.items():
        _assert_file_contains(path, expected_snippet)


def test_chapter_26_maturity_bar_links_verifier_evidence() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-26.md": (
            "reviewed orchestration patterns и [verifier evidence]"
            "(../../appendix/eval-schema.md)"
        ),
        "docs/book/part-viii/chapter-26.en.md": (
            "reviewed orchestration patterns, and [verifier evidence]"
            "(../../appendix/eval-schema.en.md)"
        ),
        "docs/book/part-viii/chapter-26.zh.md": (
            "已审查的编排模式（reviewed orchestration patterns）与"
            "[验证器证据（verifier evidence）](../../appendix/eval-schema.zh.md)"
        ),
    }

    for path, expected_snippet in expected_snippets_by_file.items():
        _assert_file_contains(path, expected_snippet)


def test_chapter_26_practical_checklist_links_verifier_evidence() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-26.md": (
            "активным orchestration pattern и [verifier evidence]"
            "(../../appendix/eval-schema.md)"
        ),
        "docs/book/part-viii/chapter-26.en.md": (
            "active orchestration pattern, and [verifier evidence]"
            "(../../appendix/eval-schema.en.md)"
        ),
        "docs/book/part-viii/chapter-26.zh.md": (
            "当前编排模式（orchestration pattern）和"
            "[验证器证据（verifier evidence）](../../appendix/eval-schema.zh.md)"
        ),
    }

    for path, expected_snippet in expected_snippets_by_file.items():
        _assert_file_contains(path, expected_snippet)


def test_chapter_26_evidence_model_links_verifier_evidence() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-26.md": (
            "artifacts и [verifier evidence](../../appendix/eval-schema.md)"
        ),
        "docs/book/part-viii/chapter-26.en.md": (
            "artifacts, and [verifier evidence](../../appendix/eval-schema.en.md)"
        ),
        "docs/book/part-viii/chapter-26.zh.md": (
            "生命周期工件（lifecycle artifacts）之间的链接"
        ),
    }

    for path, expected_snippet in expected_snippets_by_file.items():
        _assert_file_contains(path, expected_snippet)

    chinese_text = _read("docs/book/part-viii/chapter-26.zh.md")
    expected_tightened_links = (
        "工件（artifacts）与[验证器证据（verifier evidence）]",
        "[验证器证据（verifier evidence）](../../appendix/eval-schema.zh.md)事后无法关联",
    )
    for expected_tightened_link in expected_tightened_links:
        assert expected_tightened_link in chinese_text, expected_tightened_link

    forbidden_chinese_links = (
        "[verifier evidence](../../appendix/eval-schema.zh.md)",
        "被判定的 [验证器证据（verifier evidence）]",
        "[验证器证据（verifier evidence）](../../appendix/eval-schema.zh.md) 与追踪",
        "与 [验证器证据（verifier evidence）]",
        "和 [验证器证据（verifier evidence）]",
        "[验证器证据（verifier evidence）](../../appendix/eval-schema.zh.md) 事后无法关联",
    )
    for forbidden_chinese_link in forbidden_chinese_links:
        assert forbidden_chinese_link not in chinese_text, forbidden_chinese_link


def test_chapter_26_chinese_research_frontier_labels_are_localized() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-26.zh.md")
    expected_markers = (
        "追踪（traces）从“方便阅读的事件日志”",
        "追踪查看器（trace viewer）",
        "事件流（event stream）",
        "追踪词汇表（trace vocabulary）",
        "运行（run）无法关联到会话（session）、审批（approval）和工件包（artifact bundle）",
        "根因（root cause）",
        "转录（transcript）",
        "稳定事件目录（stable event catalog）",
        "模式版本控制（schema versioning）",
        "会话感知追踪（session-aware traces）",
        "遥测（telemetry）、审批（approvals）和生命周期工件（lifecycle artifacts）",
        "明确链接（linkage）",
        "AI 原生可观测性（AI-native observability）",
        "遥测（telemetry）、清单（inventory）与治理证据（governance evidence）",
        "清单覆盖 / Inventory coverage",
        "运行时遥测 / Runtime telemetry",
        "策略与审批证据 / Policy and approval evidence",
        "事故重建 / Incident reconstruction",
        "行为基线 / Behavioral baselines",
        "滥用检测 / Abuse detection",
        "发布证据 / Release evidence",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "把 traces 从“方便阅读的事件日志”",
        "单有 trace viewer 并不够",
        "event stream 的界面",
        "trace vocabulary 太弱",
        "一个 run 无法关联到 session、approval 和 artifact bundle",
        "root cause 仍然只能靠人工通读长 transcript",
        "- stable event catalog；",
        "- schema versioning；",
        "session-aware traces；",
        "telemetry、approvals 和 lifecycle artifacts 之间的明确 linkage",
        "AI-native observability 最好被理解成 telemetry、inventory 与 governance evidence",
        "A[\"Inventory coverage\"]",
        "B[\"Runtime telemetry\"]",
        "C[\"Policy and approval evidence\"]",
        "D --> E[\"Incident reconstruction\"]",
        "D --> F[\"Behavioral baselines\"]",
        "D --> G[\"Abuse detection\"]",
        "D --> H[\"Release evidence\"]",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chapter_26_chinese_governance_action_labels_are_localized() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-26.zh.md")
    expected_markers = (
        "开放（`open`）",
        "已接受（`accepted`）",
        "已豁免（`waived`）",
        "已遏制（`contained`）",
        "已关闭（`closed`）",
        "框架（framing）",
        "来源链章节（provenance chapter）",
        "证据（evidence）",
        "覆盖（coverage）",
        "关联（correlation）",
        "来源链（provenance）",
        "已批准工件（approved artifacts）",
        "契约版本（contract version）",
        "受治理包（governed bundle）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "`action_state`：`open`、`accepted`、`waived`、`contained`、`closed`",
        "这种 framing 也把本章",
        "和 provenance chapter 保持分离",
        "足够的 evidence、coverage 与 correlation",
        "来源链（provenance）关注的是，后续决策究竟由哪一组 approved artifacts",
        "contract version 或 governed bundle",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chapter_26_chinese_governance_fragility_labels_are_localized() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-26.zh.md")
    expected_markers = (
        "策略包（policy bundles）",
        "评审流程（review processes）",
        "发布门禁（release gates）",
        "审批契约（approval contracts）",
        "漂移（drift）",
        "覆盖率（coverage）",
        "受治理路径（governed path）",
        "绕过路径（bypass path）",
        "卡住的审批（stuck approvals）",
        "老化的后台运行（aging background runs）",
        "能力会话到期漂移（capability-session expiry drift）",
        "审批恢复误用（approval-resume misuse）",
        "编排模式漂移（orchestration-pattern drift）",
        "验证器质量漂移（verifier-quality drift）",
        "契约不匹配（contract mismatches）",
        "治理感知遥测（Governance-aware telemetry）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "- policy bundles；",
        "- review processes；",
        "- release gates；",
        "- approval contracts。",
        "发现 drift",
        "衡量 coverage",
        "governed path 和 bypass path",
        "stuck approvals、aging background runs",
        "capability-session expiry drift、approval-resume misuse",
        "orchestration-pattern drift、verifier-quality drift 与 contract mismatches",
        "`Governance-aware telemetry` 应该回流",
        "治理感知遥测（`Governance-aware telemetry`）",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chapter_26_chinese_behavioral_baseline_labels_are_localized() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-26.zh.md")
    expected_markers = (
        "风险工具调用（risky tool calls）",
        "审批拒绝（approval denials）",
        "审批积压（approval backlog）",
        "卡住的暂停运行（stuck paused runs）",
        "记忆写入模式（memory write pattern）",
        "检索画像（retrieval profile）",
        "异常出口目的地（unusual egress destinations）",
        "能力会话到期峰值（capability-session expiry spikes）",
        "重新初始化率（re-init rate）",
        "中断（interruption）之后审批（approval）与恢复（resume）",
        "编排模式选择（orchestration-pattern selection）",
        "工作者边界穿越（worker-boundary crossings）",
        "会话长度（session length）",
        "工具跳数（tool hop count）",
        "保障（assurance）、发布（rollout）与注册表函数（registry functions）",
        "仪表板（dashboards）、截图（screenshots）",
        "跨运行（runs）与系统（systems）可用的遥测（telemetry）",
        "出处骨干（provenance backbone）",
        "已批准工件身份（approved artifact identity）",
        "决策谱系（decision lineage）",
        "检测就绪遥测（Detection-ready telemetry）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "risky tool calls 异常增多",
        "approval denials 上升",
        "approval backlog 老化或 stuck paused runs",
        "memory write pattern 变化",
        "retrieval profile 改变",
        "unusual egress destinations 激增",
        "capability-session expiry spikes 或异常 re-init rate",
        "interruption 之后 approval 与 resume",
        "orchestration-pattern selection 或 worker-boundary crossings",
        "session length 或 tool hop count",
        "assurance、rollout 与 registry functions",
        "dashboards、screenshots 或事后回忆",
        "跨 runs 与 systems 可用的 telemetry",
        "等同于 provenance backbone",
        "approved artifact identity 与 decision lineage。",
        "`Detection-ready telemetry` 并不只是",
        "检测就绪遥测（`Detection-ready telemetry`）",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chapter_26_chinese_observability_promise_labels_are_localized() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-26.zh.md")
    expected_markers = (
        "追踪（traces）不该只告诉你",
        "跨运行（runs）",
        "审批（approvals）与跨系统活动",
        "保障（assurance）",
        "发布（rollout）",
        "判断（judgment）",
        "注册表函数（registry functions）",
        "智能体（agents）",
        "能力（capabilities）",
        "控制路径（control paths）",
        "副作用（side effects）",
        "盲点（blind spots）",
        "追踪查看器（trace viewer）",
        "智能体（agents）正在活跃（active）",
        "弃用（deprecated）",
        "连接器（connectors）和能力（capabilities）",
        "主体（principals）",
        "遥测（telemetry）",
        "清单覆盖（inventory coverage）",
        "可观测性（observability）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "traces 不该只告诉你",
        "跨 runs 的范围内",
        "控制信号、approvals 与跨系统活动",
        "使 assurance、rollout、judgment 与 registry functions",
        "哪些 agents、capabilities、control paths 与 side effects",
        "哪些地方仍有 blind spots",
        "漂亮的 trace viewer",
        "哪些 agents 正在 active",
        "哪些已经 deprecated",
        "connectors 和 capabilities",
        "使用哪些 principals",
        "发 telemetry",
        "哪些 blind spots 没覆盖",
        "没有 inventory coverage",
        "完整的 observability",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chapter_26_chinese_ai_native_signal_labels_are_localized() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-26.zh.md")
    expected_markers = (
        "AI 原生信号（AI-native signals）",
        "请求身份（request identity）",
        "行动者（actor）与智能体身份（agent identity）",
        "检索出处（retrieval provenance）",
        "工具调用（tool invocations）",
        "工具权限（tool permissions）与主体（principals）",
        "审批积压信号（approval backlog signals）",
        "到期原因（expiry reason）与重新初始化状态（re-init status）",
        "委派工作者谱系（delegated worker lineage）",
        "输出摘要（output summaries）",
        "脱敏状态（redaction status）",
        "活跃验证器契约（active verifier contract）",
        "身份与范围（Identity and scope）",
        "控制证据（Control evidence）",
        "执行状态（Execution state）",
        "质量证据（Quality evidence）",
        "发布与工件上下文（Release and artifact context）",
        "租户/请求范围（tenant/request scope）",
        "暂停/后台化/委派（paused/backgrounded/delegated）",
        "恢复（resumed）",
        "工件包（artifact bundle）",
        "运行时控制信号（runtime-control signals）",
        "暂停/恢复路径（pause/resume paths）",
        "后台执行（background execution）",
        "契约版本转换（contract-version transitions）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "演进成 `AI-native signals`",
        "AI 原生信号（`AI-native signals`）",
        "## 3. 什么是 AI-native signals",
        "- request identity；",
        "- actor 与 agent identity；",
        "- retrieval provenance；",
        "- tool invocations；",
        "tool permissions 与 principals",
        "- approval backlog signals；",
        "capability sessions 的状态、expiry reason 与 re-init status",
        "orchestration-pattern selection 与 delegated worker lineage",
        "- background runs 的状态",
        "- output summaries；",
        "- redaction status；",
        "active verifier contract 与 verifier contract version",
        "**Identity and scope：**",
        "**Control evidence：**",
        "**Execution state：**",
        "**Quality evidence：**",
        "**Release and artifact context：**",
        "处在哪个 tenant/request scope 中",
        "在哪里 paused/backgrounded/delegated",
        "如何 resumed。",
        "哪个 artifact bundle",
        "runtime-control signals 不能继续",
        "pause/resume paths、background execution 和 contract-version transitions",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chapter_26_chinese_intro_observability_labels_are_localized() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-26.zh.md")
    expected_markers = (
        "审批（approvals）",
        "运行时控制状态（runtime-control states）",
        "策略决策（policy decisions）",
        "工具主体（tool principals）",
        "契约版本（contract versions）",
        "工件包（artifact bundles）",
        "发布（release）",
        "事故（incident）",
        "治理决策（governance decision）",
        "追踪（traces）只是给开发者排查本地缺陷（bug）用的",
        "智能体（agents）",
        "能力（capabilities）",
        "发布（rollout）之后出现了哪些行为变化",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "policy decisions、tool principals、contract versions 与 artifact bundles",
        "release、incident 与 governance decision",
        "如果 traces 只是给开发者排查本地 bug 用的",
        "排查本地 bug 用的",
        "一共存在多少 agents",
        "调用了哪些 capabilities",
        "哪些 approvals 被请求、批准或绕过",
        "rollout 之后出现了哪些行为变化",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chapter_26_chinese_observability_evidence_labels_are_localized() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-26.zh.md")
    expected_markers = (
        "统一标识符（identifiers）",
        "稳定模式（schemas）",
        "脱敏规则（redaction rules）",
        "留存策略（retention policy）",
        "追踪（traces）",
        "审批（approvals）",
        "策略决策（policy decisions）",
        "运行时控制状态（runtime-control states）",
        "能力会话事件（capability-session events）",
        "编排模式事件（orchestration-pattern events）",
        "验证器契约身份（verifier contract identity）",
        "生命周期工件（lifecycle artifacts）",
        "作为证据层（evidence layer）还是太弱",
        "可观测性（observability）指南",
        "覆盖问题（coverage）",
        "AI 系统（AI systems）",
        "日志（logs）和追踪（traces）",
        "发布（releases）运行过标准评测套件（evaluation suite）",
        "滥用/安全场景（abuse/security scenarios）",
        "遥测（telemetry）覆盖",
        "仪表板（dashboards）",
        "生产义务（production obligation）",
        "清单覆盖（inventory coverage）",
        "发布评测覆盖（release-eval coverage）",
        "检测场景覆盖（detection-scenario coverage）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "统一 identifiers",
        "稳定 schemas",
        "稳定 schemas；\n- redaction rules；\n- retention policy；",
        "traces、approvals、policy decisions、runtime-control states",
        "capability-session events、orchestration-pattern events",
        "verifier contract identity 和 lifecycle artifacts",
        "作为 evidence layer 还是太弱",
        "observability 指南把 coverage 问题",
        "AI systems 会发出 logs 和 traces",
        "releases 运行过标准 evaluation suite",
        "abuse/security scenarios 已经被 telemetry 覆盖",
        "observability 就不再只是“我们有 dashboards”",
        "production obligation：inventory coverage",
        "release-eval coverage 和 detection-scenario coverage",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chapter_26_chinese_maturity_labels_are_localized() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-26.zh.md")
    expected_markers = (
        "追踪（traces）只覆盖“主运行时（runtime）”",
        "适配器（adapters）",
        "暂停运行（paused runs）",
        "后台运行（background runs）",
        "正常路径（happy path）",
        "绕过路径（bypass path）",
        "契约版本漂移（contract-version drift）",
        "载荷（payload）",
        "编排模式漂移（orchestration-pattern drift）",
        "工作者边界穿越（worker-boundary crossings）",
        "截图（screenshots）",
        "AI 原生可观测性（AI-native observability）",
        "清单覆盖（inventory coverage）",
        "遥测覆盖（telemetry coverage）",
        "已审查的编排模式（reviewed orchestration patterns）",
        "原始遥测（raw telemetry）",
        "行为基线（behavioral baselines）",
        "暂停运行年龄（paused-run age）",
        "审批积压（approval backlog）",
        "后台运行老化（background-run aging）",
        "未观测智能体（unobserved agents）",
        "结构化遥测（structured telemetry）",
        "原始仪表板（raw dashboards）",
        "发布证据（release evidence）",
        "调试辅助（debug aid）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "traces 只覆盖“主 runtime”",
        "agents 存在于 inventory 之外",
        "approvals 单独记录，却不和 traces 关联",
        "paused runs 与 background runs",
        "ownership 在 telemetry 中不可见",
        "telemetry 覆盖了 happy path，却没覆盖 bypass path",
        "contract-version drift 只有在 payload",
        "orchestration-pattern drift 或 worker-boundary crossings",
        "与 traces 或 screenshots 脱节",
        "给 AI-native observability 做一次快速成熟度测试",
        "已经有 traces、dashboards 和 log pipeline",
        "inventory coverage 和 telemetry coverage",
        "high-risk actions 能关联到 approvals、principals、artifact bundles",
        "reviewed orchestration patterns 与",
        "除了 raw telemetry 之外，还有 behavioral baselines",
        "paused-run age、approval backlog 与 background-run aging",
        "unobserved agents 被当成治理风险",
        "telemetry 能作为 release 和 incident decisions 的 evidence",
        "真正作为治理层的 AI-native observability",
        "多少百分比真的会发 structured telemetry",
        "当前 orchestration pattern 和",
        "behavioral baselines，而不只是 raw dashboards",
        "approval backlog 和 aging background runs",
        "release evidence，而不是只当 debug aid",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chapter_26_chinese_evidence_model_labels_are_localized() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-26.zh.md")
    expected_markers = (
        "审查者（reviewer）",
        "事故负责人（incident owner）",
        "智能体群体治理者（estate governor）",
        "证据就绪度（evidence readiness）",
        "日志清单（logging checklist）",
        "高风险动作（high-risk actions）",
        "主体（principals）",
        "工件（artifacts）",
        "基础设施清单（infrastructure inventory）",
        "遥测覆盖（telemetry coverage）",
        "资产覆盖（asset coverage）",
        "调试辅助（debugging aids）",
        "结构化事件（structured events）",
        "清单覆盖检查（inventory coverage checks）",
        "行为基线（behavioral baselines）",
        "检测就绪字段（detection-ready fields）",
        "发布审查（release review）",
        "事故响应（incident response）",
        "AI 原生可观测性（AI-native observability）",
        "生命周期治理（lifecycle governance）",
        "追踪产品（tracing products）",
        "检测器（detectors）",
        "遥测管线（telemetry pipelines）",
        "可归因、可审查证据（attributable, reviewable evidence）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "让 reviewer、incident owner 或 estate governor",
        "一层 evidence readiness，而不是 logging checklist",
        "如果 high-risk actions、approvals、principals、artifacts",
        "当前 observability 与 infrastructure inventory 指南",
        "telemetry coverage 和 asset coverage 视为生产控制",
        "而不只是 debugging aids",
        "structured events、inventory coverage checks、behavioral baselines",
        "detection-ready fields 让 traces 可以用于 release review 和 incident response",
        "AI-native observability 是 evals、assurance、registry 与 lifecycle governance",
        "tracing products、detectors 与 telemetry pipelines",
        "attributable、reviewable evidence 的需求不会",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chapter_2_architecture_threads_three_canonical_cases() -> None:
    required_markers = (
        "Architecture case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "reference architecture",
        "ingress identity",
        "control plane",
        "approval gate",
        "tool gateway",
        "retrieval scope",
        "tenant boundary",
        "notification tool boundary",
    )
    checked_files = (
        "docs/book/part-i/chapter-2.md",
        "docs/book/part-i/chapter-2.en.md",
        "docs/book/part-i/chapter-2.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_chapter_1_platform_threads_three_canonical_cases() -> None:
    localized_markers = (
        "Заметка о сквозных сценариях платформы",
        "Разбор обращений поддержки",
        "Внутренний ассистент знаний",
        "Координация инцидентов",
        "платформа, а не магия",
        "запись заявок",
        "восстановление хода инцидента",
        "область поиска",
        "опора на источники",
        "границы арендаторов",
        "побочные эффекты уведомлений",
        "управляемую систему исполнения",
    )
    english_markers = (
        "Platform case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "platform, not magic",
        "ticket writes",
        "incident reconstruction",
        "retrieval scope",
        "source grounding",
        "tenant boundaries",
        "notification side effects",
        "governed execution system",
    )

    _assert_files_contain_all(("docs/book/part-i/chapter-1.md",), localized_markers)
    _assert_files_contain_all(
        ("docs/book/part-i/chapter-1.en.md", "docs/book/part-i/chapter-1.zh.md"),
        english_markers,
    )


def test_chapter_5_memory_risk_threads_three_canonical_cases() -> None:
    required_markers = (
        "Memory-risk case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "durable-state risks",
        "memory-write policy",
        "profile preference",
        "tenant isolation",
        "retrieval-memory split",
        "tenant-filter enforcement",
        "notification history provenance",
        "post-incident cleanup rules",
    )
    checked_files = (
        "docs/book/part-iii/chapter-5.md",
        "docs/book/part-iii/chapter-5.en.md",
        "docs/book/part-iii/chapter-5.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_memory_retrieval_schema_includes_poisoning_review_fields() -> None:
    expected_markers_by_file = {
        "docs/appendix/memory-retrieval-schema.md": (
            "проверки отравления памяти",
            "поля проверки отравления памяти",
            "write_trust_boundary",
            "untrusted_write",
            "activation_policy",
            "delayed_activation_review",
            "contamination_scope",
            "policy_influence",
            "provenance_check",
            "quarantine_state",
            "rollback_ref",
            "карантина и отката",
        ),
        "docs/appendix/memory-retrieval-schema.en.md": (
            "memory poisoning",
            "memory poisoning review fields",
            "write_trust_boundary",
            "untrusted_write",
            "activation_policy",
            "delayed_activation_review",
            "contamination_scope",
            "policy_influence",
            "provenance_check",
            "quarantine_state",
            "rollback_ref",
            "quarantine and rollback",
        ),
        "docs/appendix/memory-retrieval-schema.zh.md": (
            "记忆投毒复核",
            "记忆投毒复核字段",
            "write_trust_boundary",
            "untrusted_write",
            "activation_policy",
            "delayed_activation_review",
            "contamination_scope",
            "policy_influence",
            "provenance_check",
            "quarantine_state",
            "rollback_ref",
            "quarantine and rollback",
        ),
    }

    for path, expected_markers in expected_markers_by_file.items():
        text = _read(path)
        for expected_marker in expected_markers:
            assert expected_marker in text, (path, expected_marker)


def test_chapter_5_memory_poisoning_scenario_is_documented() -> None:
    required_markers = (
        "memory poisoning",
        "memory poisoning review fields",
        "untrusted write",
        "delayed activation",
        "cross-tenant contamination",
        "policy influence",
        "provenance check",
        "quarantine and rollback",
        "threat-model review",
    )
    checked_files = (
        "docs/book/part-iii/chapter-5.md",
        "docs/book/part-iii/chapter-5.en.md",
        "docs/book/part-iii/chapter-5.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_chapter_5_memory_poisoning_schema_links_are_clickable() -> None:
    expected_links_by_file = {
        "docs/book/part-iii/chapter-5.md": (
            "../../appendix/memory-retrieval-schema.md",
            "../../appendix/trace-schema.md",
        ),
        "docs/book/part-iii/chapter-5.en.md": (
            "../../appendix/memory-retrieval-schema.en.md",
            "../../appendix/trace-schema.en.md",
        ),
        "docs/book/part-iii/chapter-5.zh.md": (
            "../../appendix/memory-retrieval-schema.zh.md",
            "../../appendix/trace-schema.zh.md",
        ),
    }

    for path, expected_links in expected_links_by_file.items():
        text = _read(path)
        for link in expected_links:
            assert f"]({link})" in text, (path, link)

    chinese_text = _read("docs/book/part-iii/chapter-5.zh.md")
    assert (
        "[记忆/检索模式（memory/retrieval schema）]"
        "(../../appendix/memory-retrieval-schema.zh.md)"
    ) in chinese_text
    assert "[追踪模式（trace schema）](../../appendix/trace-schema.zh.md)" in chinese_text
    assert (
        "[memory/retrieval schema](../../appendix/memory-retrieval-schema.zh.md)"
        not in chinese_text
    )
    assert "[trace schema](../../appendix/trace-schema.zh.md)" not in chinese_text


def test_chapter_3_trust_boundaries_thread_three_canonical_cases() -> None:
    required_markers = (
        "Trust-boundary case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "read/decide/act split",
        "ticket writes",
        "retrieved documents",
        "source authority",
        "memory writes",
        "external notifications",
    )
    checked_files = (
        "docs/book/part-ii/chapter-3.md",
        "docs/book/part-ii/chapter-3.en.md",
        "docs/book/part-ii/chapter-3.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_chapter_23_retirement_threads_three_canonical_cases() -> None:
    russian_markers = (
        "Заметка о сквозных сценариях вывода из эксплуатации",
        "Разбор обращений поддержки",
        "внутренний ассистент знаний",
        "координация инцидентов",
        "устаревшие пишущие пути",
        "приостановленные подтверждения",
        "доказательств проверки",
        "устаревшие корпуса",
        "устаревшие векторные представления",
        "возможности только для аварийного режима",
        "каналы уведомлений",
    )
    english_markers = (
        "Retirement case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "deprecated write paths",
        "paused approvals",
        "verifier evidence",
        "stale corpora",
        "obsolete embeddings",
        "emergency-only capabilities",
        "notification channels",
    )

    _assert_files_contain_all(("docs/book/part-viii/chapter-23.md",), russian_markers)
    _assert_files_contain_all(("docs/book/part-viii/chapter-23.en.md",), english_markers)

    for path in ("docs/book/part-viii/chapter-23.md", "docs/book/part-viii/chapter-23.en.md"):
        text = _read(path)
        assert "internal knowledge assistant" not in text, path
        assert "incident coordination" not in text, path

    chinese_text = _read("docs/book/part-viii/chapter-23.zh.md")
    expected_chinese_markers = (
        "退役案例主线说明（Retirement case-spine note）",
        "规范案例（canonical case）",
        "支持分诊（Support triage）",
        "内部知识助手（Internal knowledge assistant）",
        "事故协调（Incident coordination）",
        "行动权（right to act）",
        "已弃用写入路径（deprecated write paths）",
        "暂停审批（paused approvals）",
        "过时语料（stale corpora）",
        "过时嵌入（obsolete embeddings）",
        "记忆写入规则（memory-write rules）",
        "响应路径（response path）",
        "仅应急能力（emergency-only capabilities）",
        "升级路由（escalation routes）",
        "通知通道（notification channels）",
        "退役计划（retirement plan）",
    )
    for expected_chinese_marker in expected_chinese_markers:
        assert expected_chinese_marker in chinese_text, expected_chinese_marker

    forbidden_chinese_markers = (
        "**Retirement case-spine note：**",
        "每个 canonical case",
        "Support triage 关闭",
        "Internal knowledge assistant 退役",
        "Incident coordination 在",
        "不同的 right to act",
        "关闭 deprecated write paths 和 paused approvals",
        "退役 stale corpora、obsolete embeddings 和 memory-write rules",
        "在 response path 不再有效时关闭 emergency-only capabilities",
        "escalation routes 和 notification channels",
        "runtime 的 retirement plan",
    )
    for forbidden_chinese_marker in forbidden_chinese_markers:
        assert forbidden_chinese_marker not in chinese_text, forbidden_chinese_marker


def test_chapter_23_retirement_verifier_evidence_eval_link_is_clickable() -> None:
    expected_links_by_file = {
        "docs/book/part-viii/chapter-23.md": "../../appendix/eval-schema.md",
        "docs/book/part-viii/chapter-23.en.md": "../../appendix/eval-schema.en.md",
        "docs/book/part-viii/chapter-23.zh.md": "../../appendix/eval-schema.zh.md",
    }

    for path, expected_link in expected_links_by_file.items():
        assert f"]({expected_link})" in _read(path), (path, expected_link)


def test_chapter_23_retirement_useful_refs_include_retirement_contracts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-23.md": (
            "[Схема подтверждения](../../appendix/approval-schema.md)",
            "[Схема наборов для оценки и правил проверки]"
            "(../../appendix/eval-schema.md)",
            "[Схема памяти и извлечения]"
            "(../../appendix/memory-retrieval-schema.md)",
        ),
        "docs/book/part-viii/chapter-23.en.md": (
            "[Approval Schema](../../appendix/approval-schema.en.md)",
            "[Eval Dataset Schema and Grading Contract]"
            "(../../appendix/eval-schema.en.md)",
            "[Memory and Retrieval Schema]"
            "(../../appendix/memory-retrieval-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-23.zh.md": (
            "[生命周期工件模式]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[审批请求与决策记录模式](../../appendix/approval-schema.zh.md)",
            "[评测数据集模式与打分契约]"
            "(../../appendix/eval-schema.zh.md)",
            "[记忆记录与检索契约模式]"
            "(../../appendix/memory-retrieval-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_23_retirement_breakages_link_verifier_evidence() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-23.md": (
            "обязательства по хранению [доказательств проверки]"
            "(../../appendix/eval-schema.md)"
        ),
        "docs/book/part-viii/chapter-23.en.md": (
            "[verifier evidence](../../appendix/eval-schema.en.md) obligations"
        ),
        "docs/book/part-viii/chapter-23.zh.md": (
            "[验证器证据（verifier evidence）](../../appendix/eval-schema.zh.md)"
            "保留义务（obligations）"
        ),
    }

    for path, expected_snippet in expected_snippets_by_file.items():
        assert expected_snippet in _read(path), (path, expected_snippet)


def test_chapter_23_opening_state_tail_links_verifier_evidence() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-23.md": (
            "[доказательств проверки](../../appendix/eval-schema.md)"
        ),
        "docs/book/part-viii/chapter-23.en.md": (
            "[evidence-retention obligations]"
            "(../../appendix/eval-schema.en.md)"
        ),
        "docs/book/part-viii/chapter-23.zh.md": (
            "[验证器证据保留义务（verifier evidence retention obligations）]"
            "(../../appendix/eval-schema.zh.md)"
        ),
    }

    for path, expected_snippet in expected_snippets_by_file.items():
        assert expected_snippet in _read(path), (path, expected_snippet)

    chinese_text = _read("docs/book/part-viii/chapter-23.zh.md")
    forbidden_chinese_link = (
        "[verifier evidence retention obligations]"
        "(../../appendix/eval-schema.zh.md)"
    )
    assert forbidden_chinese_link not in chinese_text, forbidden_chinese_link


def test_chapter_23_deprecated_inventory_links_control_contracts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-23.md": (
            "[утвержденный реестр](../../appendix/registry-operations-handbook.md)",
            "[реестр устаревших элементов]"
            "(../../appendix/registry-operations-handbook.md)",
            "[устаревший контракт возможности]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[устаревшая схема подтверждения](../../appendix/approval-schema.md)",
            "[устаревшая схема управления средой исполнения]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[устаревшая схема оркестрации или политика границы рабочих агентов]"
            "(../../appendix/change-rollout-schema.md)",
            "[устаревший контракт сессии возможности]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[устаревший контракт проверяющего](../../appendix/eval-schema.md)",
        ),
        "docs/book/part-viii/chapter-23.en.md": (
            "[approved inventory](../../appendix/registry-operations-handbook.en.md)",
            "[deprecated inventory](../../appendix/registry-operations-handbook.en.md)",
            "[deprecated capability contract]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[deprecated approval schema](../../appendix/approval-schema.en.md)",
            "[deprecated runtime-control schema]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[deprecated orchestration pattern or worker-boundary policy]"
            "(../../appendix/change-rollout-schema.en.md)",
            "[deprecated capability-session contract]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[deprecated verifier contract](../../appendix/eval-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-23.zh.md": (
            "[已批准清单（approved inventory）]"
            "(../../appendix/registry-operations-handbook.zh.md)",
            "[已废弃清单（deprecated inventory）]"
            "(../../appendix/registry-operations-handbook.zh.md)",
            "[已废弃的能力契约](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[已废弃的审批模式（approval schema）](../../appendix/approval-schema.zh.md)",
            "[已废弃的运行时控制模式（runtime-control schema）]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[已废弃的编排模式（orchestration pattern）或工作者边界策略"
            "（worker-boundary policy）]"
            "(../../appendix/change-rollout-schema.zh.md)",
            "[已废弃的能力会话契约（capability-session contract）]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[已废弃的验证器契约（verifier contract）](../../appendix/eval-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)

    chinese_text = _read("docs/book/part-viii/chapter-23.zh.md")
    forbidden_chinese_links = (
        "[已废弃的 approval schema](../../appendix/approval-schema.zh.md)",
        "[已废弃的 runtime-control schema]"
        "(../../appendix/lifecycle-artifact-schema.zh.md)",
        "[已废弃的 orchestration pattern 或 worker-boundary policy]"
        "(../../appendix/change-rollout-schema.zh.md)",
        "[已废弃的编排模式（orchestration pattern）或 worker-boundary 策略"
        "（worker-boundary policy）]"
        "(../../appendix/change-rollout-schema.zh.md)",
        "[已废弃的 capability-session contract]"
        "(../../appendix/lifecycle-artifact-schema.zh.md)",
        "[已废弃的 verifier contract](../../appendix/eval-schema.zh.md)",
    )
    for forbidden_chinese_link in forbidden_chinese_links:
        assert forbidden_chinese_link not in chinese_text, forbidden_chinese_link


def test_chapter_23_right_to_act_risks_link_retirement_contracts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-23.md": (
            "[активный принципал инструмента]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[доступ к памяти](../../appendix/memory-retrieval-schema.md)",
            "[старый путь поэтапного выпуска]"
            "(../../appendix/change-rollout-schema.md)",
            "[возобновляемый путь приостановленного подтверждения]"
            "(../../appendix/approval-schema.md)",
            "[истекшая сессия возможности, которую все еще можно повторно "
            "инициализировать через старый путь]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[старая схема управления средой исполнения, которую шлюзы все еще принимают]"
            "(../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-23.en.md": (
            "[active tool principal](../../appendix/lifecycle-artifact-schema.en.md)",
            "[memory access](../../appendix/memory-retrieval-schema.en.md)",
            "[old rollout path](../../appendix/change-rollout-schema.en.md)",
            "[resumable paused approval path](../../appendix/approval-schema.en.md)",
            "[expired capability session that can still be re-initialized "
            "through an old path](../../appendix/lifecycle-artifact-schema.en.md)",
            "[old runtime-control schema still accepted by gateways]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-23.zh.md": (
            "[活跃的工具主体](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[记忆访问权](../../appendix/memory-retrieval-schema.zh.md)",
            "[旧的上线路径](../../appendix/change-rollout-schema.zh.md)",
            "[可恢复的暂停审批路径（paused approval path）]"
            "(../../appendix/approval-schema.zh.md)",
            "[已过期但仍可通过旧路径重新初始化的能力会话"
            "（re-initialize capability session）]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[仍被网关接受的旧运行时控制模式（runtime-control schema）]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)

    chinese_text = _read("docs/book/part-viii/chapter-23.zh.md")
    forbidden_chinese_links = (
        "[可恢复的 paused approval path](../../appendix/approval-schema.zh.md)",
        "[已过期但仍可通过旧路径 re-initialize 的 capability session]"
        "(../../appendix/lifecycle-artifact-schema.zh.md)",
        "[仍被 gateways 接受的旧 runtime-control schema]"
        "(../../appendix/lifecycle-artifact-schema.zh.md)",
    )
    for forbidden_chinese_link in forbidden_chinese_links:
        assert forbidden_chinese_link not in chinese_text, forbidden_chinese_link


def test_chapter_23_old_ticket_writer_example_links_retirement_controls() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-23.md": (
            "[закрыть принципал инструмента]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[отозвать экспозицию шлюза]"
            "(../../appendix/registry-operations-handbook.md)",
            "[истечь приостановленные подтверждения]"
            "(../../appendix/approval-schema.md)",
            "[остановить фоновые повторы]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[сохранить контрольный след](../../appendix/trace-schema.md)",
        ),
        "docs/book/part-viii/chapter-23.en.md": (
            "[close the tool principal]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[revoke gateway exposure]"
            "(../../appendix/registry-operations-handbook.en.md)",
            "[expire paused approvals](../../appendix/approval-schema.en.md)",
            "[stop background retries]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[preserve the audit trail](../../appendix/trace-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-23.zh.md": (
            "[关闭工具主体](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[撤销网关暴露（gateway exposure）]"
            "(../../appendix/registry-operations-handbook.zh.md)",
            "[让暂停审批（paused approvals）过期]"
            "(../../appendix/approval-schema.zh.md)",
            "[停止后台重试](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[保留审计轨迹](../../appendix/trace-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)

    chinese_text = _read("docs/book/part-viii/chapter-23.zh.md")
    expected_chinese_markers = (
        "如果支持分诊（support-triage）v2 替换了曾经制造重复工单的旧路径",
        "仅仅移除提示路由（prompt route）不够",
    )
    for expected_chinese_marker in expected_chinese_markers:
        assert expected_chinese_marker in chinese_text, expected_chinese_marker

    forbidden_chinese_links = (
        "[撤销 gateway exposure]"
        "(../../appendix/registry-operations-handbook.zh.md)",
        "[让 paused approvals 过期](../../appendix/approval-schema.zh.md)",
        "如果 support-triage v2 替换了曾经制造重复工单的旧路径",
        "仅仅移除 prompt route 不够",
    )
    for forbidden_chinese_link in forbidden_chinese_links:
        assert forbidden_chinese_link not in chinese_text, forbidden_chinese_link


def test_chapter_23_layered_retirement_checklist_links_control_surfaces() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-23.md": (
            "[остановить новые волны поэтапного выпуска]"
            "(../../appendix/change-rollout-schema.md)",
            "[запретить рискованные возможности]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[перевести пишущие действия в режим подтверждения или отключения]"
            "(../../appendix/approval-schema.md)",
            "[остановить записи в память](../../appendix/memory-retrieval-schema.md)",
            "[истечь или отменить приостановленные запуски]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[отключить фоновые задачи и фоновые маршруты]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[закрыть или архивировать состояние сессии возможности и запретить "
            "неконтролируемую повторную инициализацию]"
            "(../../appendix/lifecycle-artifact-schema.md)",
        ),
        "docs/book/part-viii/chapter-23.en.md": (
            "[stop new rollout waves](../../appendix/change-rollout-schema.en.md)",
            "[disable risky capabilities]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[move write actions to approval-only or disable them]"
            "(../../appendix/approval-schema.en.md)",
            "[stop memory writes](../../appendix/memory-retrieval-schema.en.md)",
            "[expire or cancel paused runs]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[stop background jobs and background routes]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[close or archive capability-session state and block uncontrolled "
            "re-init](../../appendix/lifecycle-artifact-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-23.zh.md": (
            "[停止新的上线波次](../../appendix/change-rollout-schema.zh.md)",
            "[关闭高风险能力](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[把写入动作切到仅审批模式，或者直接停用]"
            "(../../appendix/approval-schema.zh.md)",
            "[停止记忆写入](../../appendix/memory-retrieval-schema.zh.md)",
            "[让暂停运行（paused runs）过期或直接取消]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[停止后台任务与后台路由（background routes）]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[关闭或归档能力会话状态（capability-session state），"
            "并阻断不受控的重新初始化（re-init）]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)

    chinese_text = _read("docs/book/part-viii/chapter-23.zh.md")
    forbidden_chinese_links = (
        "[让 paused runs 过期或直接取消]"
        "(../../appendix/lifecycle-artifact-schema.zh.md)",
        "[停止后台任务与 background routes]"
        "(../../appendix/lifecycle-artifact-schema.zh.md)",
        "[关闭或归档 capability-session state，并阻断不受控的 re-init]"
        "(../../appendix/lifecycle-artifact-schema.zh.md)",
    )
    for forbidden_chinese_link in forbidden_chinese_links:
        assert forbidden_chinese_link not in chinese_text, forbidden_chinese_link


def test_chapter_23_layered_retirement_evidence_links_control_surfaces() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-23.md": (
            "[выключить устаревшие схемы оркестрации и отозвать экспозицию "
            "безопасного каталога рабочих агентов]"
            "(../../appendix/change-rollout-schema.md)",
            "[отозвать пути делегированной авторизации]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[архивировать их итоговую линию происхождения]"
            "(../../appendix/trace-schema.md)",
            "[вывести из эксплуатации устаревшие контракты проверяющего и сохранить "
            "доказательства, нужные для объяснения прежних решений по поэтапному "
            "выпуску или заверению](../../appendix/eval-schema.md)",
            "[`failure_reason`](../../appendix/eval-schema.md)",
            "[архивировать артефакты передачи, которые несли область спринта, "
            "критику оценщика или решения на границе сброса]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[отозвать исходящий доступ](../../appendix/lifecycle-artifact-schema.md)",
            "[закрыть принципалы, секреты и соединители]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[зафиксировать итоговое контрольное состояние]"
            "(../../appendix/trace-schema.md)",
        ),
        "docs/book/part-viii/chapter-23.en.md": (
            "[disable deprecated orchestration patterns and revoke worker-safe "
            "catalog exposure](../../appendix/change-rollout-schema.en.md)",
            "[revoke delegated authorization paths]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[archive their final lineage](../../appendix/trace-schema.en.md)",
            "[retire deprecated verifier contracts and preserve the evidence "
            "needed to explain prior rollout or assurance decisions]"
            "(../../appendix/eval-schema.en.md)",
            "[`failure_reason`](../../appendix/eval-schema.en.md)",
            "[archive handoff artifacts that carried sprint scope, evaluator "
            "critique, or reset-boundary decisions]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[revoke egress access](../../appendix/lifecycle-artifact-schema.en.md)",
            "[close principals, secrets, and connectors]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[record the final audit state](../../appendix/trace-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-23.zh.md": (
            "[停用已废弃的编排模式（orchestration patterns），并撤销 worker-safe "
            "目录暴露（worker-safe catalog exposure）]"
            "(../../appendix/change-rollout-schema.zh.md)",
            "[撤销委派授权路径（delegated authorization paths）]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[归档它们最终的血缘（lineage）](../../appendix/trace-schema.zh.md)",
            "[退役已废弃的验证器契约（verifier contracts），"
            "并保留解释既往发布（rollout）或保障决策所需的证据]"
            "(../../appendix/eval-schema.zh.md)",
            "[`failure_reason`](../../appendix/eval-schema.zh.md)",
            "[归档那些承载 sprint scope、评测器批注（evaluator critique）或"
            "重置边界决策（reset-boundary decisions）的交接工件（handoff artifacts）]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[撤销出口访问](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[关闭主体、密钥和连接器]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[固化最终审计状态](../../appendix/trace-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)

    chinese_text = _read("docs/book/part-viii/chapter-23.zh.md")
    forbidden_chinese_links = (
        "[停用已废弃的 orchestration patterns，并撤销 worker-safe catalog exposure]"
        "(../../appendix/change-rollout-schema.zh.md)",
        "[撤销 delegated authorization paths]"
        "(../../appendix/lifecycle-artifact-schema.zh.md)",
        "[归档它们最终的 lineage](../../appendix/trace-schema.zh.md)",
        "[退役已废弃的 verifier contracts，并保留解释既往 rollout 或保障决策所需的证据]"
        "(../../appendix/eval-schema.zh.md)",
        "[归档那些承载 sprint scope、evaluator critique 或 reset-boundary "
        "decisions 的 handoff artifacts]"
        "(../../appendix/lifecycle-artifact-schema.zh.md)",
    )
    for forbidden_chinese_link in forbidden_chinese_links:
        assert forbidden_chinese_link not in chinese_text, forbidden_chinese_link


def test_chapter_23_memory_audit_retention_links_state_contracts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-23.md": (
            "[что архивировать](../../appendix/lifecycle-artifact-schema.md)",
            "[что удалить](../../appendix/memory-retrieval-schema.md)",
            "[что обезличить](../../appendix/memory-retrieval-schema.md)",
            "[трассы](../../appendix/trace-schema.md) и "
            "[подтверждения](../../appendix/approval-schema.md)",
            "[кто остается владельцем архивированного состояния]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[наборы данных](../../appendix/eval-schema.md) и "
            "[артефакты памяти](../../appendix/memory-retrieval-schema.md)",
            "[записи делегированной авторизации]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[доказательства проверяющего](../../appendix/eval-schema.md)",
            "[историю контрактов проверяющего](../../appendix/eval-schema.md)",
        ),
        "docs/book/part-viii/chapter-23.en.md": (
            "[what to archive](../../appendix/lifecycle-artifact-schema.en.md)",
            "[what to delete](../../appendix/memory-retrieval-schema.en.md)",
            "[what to anonymize](../../appendix/memory-retrieval-schema.en.md)",
            "[traces](../../appendix/trace-schema.en.md) and "
            "[approvals](../../appendix/approval-schema.en.md)",
            "[who remains the owner of archived state]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[datasets](../../appendix/eval-schema.en.md) and "
            "[memory artifacts](../../appendix/memory-retrieval-schema.en.md)",
            "[delegated authorization records]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[verifier-contract history](../../appendix/eval-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-23.zh.md": (
            "[什么要归档](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[什么要删除](../../appendix/memory-retrieval-schema.zh.md)",
            "[什么要匿名化](../../appendix/memory-retrieval-schema.zh.md)",
            "[追踪](../../appendix/trace-schema.zh.md)和"
            "[审批](../../appendix/approval-schema.zh.md)",
            "[归档状态的负责人是谁]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[数据集](../../appendix/eval-schema.zh.md)和"
            "[记忆工件](../../appendix/memory-retrieval-schema.zh.md)",
            "[委派授权记录（delegated authorization records）]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[验证器证据（verifier evidence）](../../appendix/eval-schema.zh.md)",
            "[验证器契约历史（verifier-contract history）]"
            "(../../appendix/eval-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)

    chinese_text = _read("docs/book/part-viii/chapter-23.zh.md")
    forbidden_chinese_links = (
        "[delegated authorization records]"
        "(../../appendix/lifecycle-artifact-schema.zh.md)",
        "[verifier evidence](../../appendix/eval-schema.zh.md)",
        "[verifier-contract history](../../appendix/eval-schema.zh.md)",
    )
    for forbidden_chinese_link in forbidden_chinese_links:
        assert forbidden_chinese_link not in chinese_text, forbidden_chinese_link


def test_chapter_23_staged_replacement_links_rollout_eval_lifecycle() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-23.md": (
            "[теневое сравнение](../../appendix/eval-schema.md)",
            "[ограниченная миграция клиентов]"
            "(../../appendix/change-rollout-schema.md)",
            "[параллельный запуск для критичных сценариев]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[сравнительные оценки](../../appendix/eval-schema.md)",
            "[поэтапное перенаправление трафика]"
            "(../../appendix/change-rollout-schema.md)",
            "[финальное переключение только после достаточной уверенности]"
            "(../../appendix/change-rollout-schema.md)",
        ),
        "docs/book/part-viii/chapter-23.en.md": (
            "[shadow comparison](../../appendix/eval-schema.en.md)",
            "[limited tenant migration](../../appendix/change-rollout-schema.en.md)",
            "[dual-run for critical scenarios]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[side-by-side evals](../../appendix/eval-schema.en.md)",
            "[staged traffic shift](../../appendix/change-rollout-schema.en.md)",
            "[final cutover only after confidence is high]"
            "(../../appendix/change-rollout-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-23.zh.md": (
            "[影子对比](../../appendix/eval-schema.zh.md)",
            "[小范围租户迁移](../../appendix/change-rollout-schema.zh.md)",
            "[在关键场景里双运行](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[并行评测](../../appendix/eval-schema.zh.md)",
            "[分阶段切流](../../appendix/change-rollout-schema.zh.md)",
            "[只有在信心足够时才做最终切换]"
            "(../../appendix/change-rollout-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_23_breakage_list_links_retirement_control_surfaces() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-23.md": (
            "[принципалы еще живы](../../appendix/lifecycle-artifact-schema.md)",
            "[фоновые задачи забыли выключить]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[путь записи в память остался активным]"
            "(../../appendix/memory-retrieval-schema.md)",
            "[приостановленные подтверждения остались возобновляемыми после "
            "вывода из эксплуатации]"
            "(../../appendix/approval-schema.md)",
            "[истекшие сессии возможностей все еще можно повторно инициализировать "
            "через устаревшие пути контроля]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[устаревшие схемы оркестрации или политики границ рабочих агентов "
            "остаются рабочими после вывода из эксплуатации]"
            "(../../appendix/change-rollout-schema.md)",
        ),
        "docs/book/part-viii/chapter-23.en.md": (
            "[principals are still active]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[background jobs were forgotten]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[memory write path remained live]"
            "(../../appendix/memory-retrieval-schema.en.md)",
            "[paused approvals were left resumable after retirement]"
            "(../../appendix/approval-schema.en.md)",
            "[expired capability sessions could still be re-initialized through "
            "stale control paths](../../appendix/lifecycle-artifact-schema.en.md)",
            "[deprecated orchestration patterns or worker-boundary policies "
            "remained usable after retirement]"
            "(../../appendix/change-rollout-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-23.zh.md": (
            "[主体还活着](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[后台任务没关](../../appendix/lifecycle-artifact-schema.zh.md)",
            "[记忆写入路径仍然在工作]"
            "(../../appendix/memory-retrieval-schema.zh.md)",
            "[暂停审批（paused approvals）在退役之后仍然可以恢复]"
            "(../../appendix/approval-schema.zh.md)",
            "[已过期能力会话（capability sessions）仍可通过陈旧控制路径重新初始化"
            "（re-initialize）]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[已废弃的编排模式（orchestration patterns）或工作者边界策略"
            "（worker-boundary policies）在退役后仍然可用]"
            "(../../appendix/change-rollout-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)

    chinese_text = _read("docs/book/part-viii/chapter-23.zh.md")
    forbidden_chinese_links = (
        "[paused approvals 在退役之后仍然可以恢复]"
        "(../../appendix/approval-schema.zh.md)",
        "[已过期 capability sessions 仍可通过陈旧控制路径 re-initialize]"
        "(../../appendix/lifecycle-artifact-schema.zh.md)",
        "[已废弃的 orchestration patterns 或 worker-boundary policies 在退役后仍然可用]"
        "(../../appendix/change-rollout-schema.zh.md)",
        "[已废弃的编排模式（orchestration patterns）或 worker-boundary 策略"
        "（worker-boundary policies）在退役后仍然可用]"
        "(../../appendix/change-rollout-schema.zh.md)",
    )
    for forbidden_chinese_link in forbidden_chinese_links:
        assert forbidden_chinese_link not in chinese_text, forbidden_chinese_link


def test_chapter_23_breakage_list_links_retirement_completion_controls() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-23.md": (
            "[фоновые маршруты забыли выключить]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[архивированное состояние никому не принадлежит]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[устаревшие схемы все еще принимаются шлюзами или средой исполнения]"
            "(../../appendix/lifecycle-artifact-schema.md)",
            "[устаревшие схемы остаются рабочими слишком долго]"
            "(../../appendix/change-rollout-schema.md)",
            "[параллельного запуска](../../appendix/lifecycle-artifact-schema.md) "
            "или [поэтапной миграции](../../appendix/change-rollout-schema.md)",
        ),
        "docs/book/part-viii/chapter-23.en.md": (
            "[background routes were forgotten]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[archived state belongs to nobody]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[deprecated schemas still remain accepted by gateways or runtimes]"
            "(../../appendix/lifecycle-artifact-schema.en.md)",
            "[deprecated patterns remain usable too long]"
            "(../../appendix/change-rollout-schema.en.md)",
            "[dual-run](../../appendix/lifecycle-artifact-schema.en.md) or "
            "[staged migration](../../appendix/change-rollout-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-23.zh.md": (
            "[后台路由（background routes）被遗忘没有关闭]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[归档状态没有负责人]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[已废弃的模式（schemas）仍然被网关（gateways）或运行时（runtimes）接受]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[已废弃模式存活太久]"
            "(../../appendix/change-rollout-schema.zh.md)",
            "[双运行](../../appendix/lifecycle-artifact-schema.zh.md)或"
            "[分阶段迁移](../../appendix/change-rollout-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)

    chinese_text = _read("docs/book/part-viii/chapter-23.zh.md")
    forbidden_chinese_links = (
        "[background routes 被遗忘没有关闭]"
        "(../../appendix/lifecycle-artifact-schema.zh.md)",
        "[已废弃的 schemas 仍然被 gateways 或 runtimes 接受]"
        "(../../appendix/lifecycle-artifact-schema.zh.md)",
    )
    for forbidden_chinese_link in forbidden_chinese_links:
        assert forbidden_chinese_link not in chinese_text, forbidden_chinese_link


def test_chapter_27_registry_threads_three_canonical_cases() -> None:
    common_markers = (
        "Registry case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "write-capability owners",
        "verifier evidence",
        "freshness review",
        "incident-role owners",
    )
    expected_markers_by_file = {
        "docs/book/part-viii/chapter-27.md": (
            "Заметка о сквозных сценариях реестра",
            "Разбор обращений поддержки",
            "Внутренний ассистент знаний",
            "Координация инцидентов",
            "владельцев пишущих возможностей",
            "доказательства проверяющего",
            "проверки свежести",
            "владельцев ролей инцидента",
            "режима подтверждения",
            "плана вывода из эксплуатации",
            "владельцев корпуса",
            "состояния жизненного цикла",
        ),
        "docs/book/part-viii/chapter-27.en.md": (
            *common_markers,
            "approval mode",
            "retirement plan",
            "corpus owners",
            "lifecycle state",
        ),
        "docs/book/part-viii/chapter-27.zh.md": (
            "注册表案例主线说明（Registry case-spine note）",
            "支持分诊（support-triage）不应该只是",
            "支持分诊（Support triage）",
            "内部知识助手（Internal knowledge assistant）",
            "事故协调（Incident coordination）",
            "追踪（trace）或工件包（artifact bundle）",
            "工件包（artifact bundle）",
            "金丝雀（canary）",
            "已废弃路由（route）",
            "规范案例（canonical case）",
            "变成[命名注册记录（named registry record）]",
            "命名注册记录（named registry record）",
            "写能力负责人（write-capability owners）",
            "审批模式（approval mode）",
            "已废弃工单路径（deprecated ticket paths）",
            "的[退役计划（retirement plan）]",
            "退役计划（retirement plan）",
            "需要[语料负责人（corpus owners）]",
            "语料负责人（corpus owners）",
            "新鲜度审查（freshness review）",
            "租户范围（tenant scope）",
            "和[检索策略链接（retrieval-policy linkage）]",
            "检索策略链接（retrieval-policy linkage）",
            "事故角色负责人（incident-role owners）",
            "升级权限（escalation authority）",
            "通知渠道（notification channels）",
            "仅限应急能力（emergency-only capabilities）",
            "的[生命周期状态（lifecycle state）]",
            "生命周期状态（lifecycle state）",
        ),
    }

    for path, expected_markers in expected_markers_by_file.items():
        text = _read(path)
        for expected_marker in expected_markers:
            assert expected_marker in text, (path, expected_marker)

    chinese_text = _read("docs/book/part-viii/chapter-27.zh.md")
    forbidden_chinese_markers = (
        "注册表里的 support-triage",
        "support-triage 不应该只是",
        "trace 或 artifact bundle",
        "**Registry case-spine note：**",
        "Support triage 需要写能力负责人",
        "Internal knowledge assistant 需要",
        "Incident coordination 需要事故角色负责人",
        "扩大 canary",
        "已废弃 route",
        "每个 canonical case",
        "变成 [命名注册记录",
        "需要 write-capability owners",
        "deprecated ticket paths 的",
        "的 [退役计划",
        "需要 [语料负责人",
        "corpus owners）、freshness review、tenant scope",
        "需要 incident-role owners、escalation authority、notification channels",
        "emergency-only capabilities 的",
        "和 [检索策略链接",
        "的 [生命周期状态",
    )
    for forbidden_chinese_marker in forbidden_chinese_markers:
        assert forbidden_chinese_marker not in chinese_text, forbidden_chinese_marker


def test_chapter_27_useful_refs_include_registry_evidence_contracts() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-27.md": (
            "[Схема наборов для оценки и правил проверки]"
            "(../../appendix/eval-schema.md)",
            "[Схема памяти и извлечения]"
            "(../../appendix/memory-retrieval-schema.md)",
        ),
        "docs/book/part-viii/chapter-27.en.md": (
            "[Eval Dataset Schema and Grading Contract]"
            "(../../appendix/eval-schema.en.md)",
            "[Memory and Retrieval Schema]"
            "(../../appendix/memory-retrieval-schema.en.md)",
        ),
        "docs/book/part-viii/chapter-27.zh.md": (
            "[生命周期工件模式]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[审批请求与决策记录模式](../../appendix/approval-schema.zh.md)",
            "[评测数据集模式与打分契约]"
            "(../../appendix/eval-schema.zh.md)",
            "[记忆记录与检索契约模式]"
            "(../../appendix/memory-retrieval-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_27_registry_case_spine_links_are_clickable() -> None:
    expected_links_by_file = {
        "docs/book/part-viii/chapter-27.md": (
            "../../appendix/eval-schema.md",
            "../../appendix/registry-operations-handbook.md",
            "../../appendix/approval-schema.md",
            "../../appendix/lifecycle-artifact-schema.md",
            "../../appendix/memory-retrieval-schema.md",
        ),
        "docs/book/part-viii/chapter-27.en.md": (
            "../../appendix/eval-schema.en.md",
            "../../appendix/registry-operations-handbook.en.md",
            "../../appendix/approval-schema.en.md",
            "../../appendix/lifecycle-artifact-schema.en.md",
            "../../appendix/memory-retrieval-schema.en.md",
        ),
        "docs/book/part-viii/chapter-27.zh.md": (
            "../../appendix/eval-schema.zh.md",
            "../../appendix/registry-operations-handbook.zh.md",
            "../../appendix/approval-schema.zh.md",
            "../../appendix/lifecycle-artifact-schema.zh.md",
            "../../appendix/memory-retrieval-schema.zh.md",
        ),
    }

    for path, expected_links in expected_links_by_file.items():
        text = _read(path)
        for expected_link in expected_links:
            assert f"]({expected_link})" in text, (path, expected_link)

    chinese_text = _read("docs/book/part-viii/chapter-27.zh.md")
    expected_chinese_links = (
        "[命名注册记录（named registry record）]"
        "(../../appendix/registry-operations-handbook.zh.md)",
        "[审批模式（approval mode）](../../appendix/approval-schema.zh.md)",
        "[退役计划（retirement plan）]"
        "(../../appendix/lifecycle-artifact-schema.zh.md)",
        "[语料负责人（corpus owners）]"
        "(../../appendix/memory-retrieval-schema.zh.md)",
        "[检索策略链接（retrieval-policy linkage）]"
        "(../../appendix/memory-retrieval-schema.zh.md)",
        "[生命周期状态（lifecycle state）]"
        "(../../appendix/lifecycle-artifact-schema.zh.md)",
    )
    for expected_chinese_link in expected_chinese_links:
        assert expected_chinese_link in chinese_text, expected_chinese_link
    forbidden_chinese_links = (
        "[named registry record](../../appendix/registry-operations-handbook.zh.md)",
        "[approval mode](../../appendix/approval-schema.zh.md)",
        "[retirement plan](../../appendix/lifecycle-artifact-schema.zh.md)",
        "[corpus owners](../../appendix/memory-retrieval-schema.zh.md)",
        "[retrieval-policy linkage](../../appendix/memory-retrieval-schema.zh.md)",
        "[lifecycle state](../../appendix/lifecycle-artifact-schema.zh.md)",
    )
    for forbidden_chinese_link in forbidden_chinese_links:
        assert forbidden_chinese_link not in chinese_text, forbidden_chinese_link


def test_chapter_20_useful_refs_include_change_rollout_schema() -> None:
    expected_snippets_by_file = {
        "docs/book/part-viii/chapter-20.md": (
            "[Схема проверки изменений и шлюза поэтапного выпуска]"
            "(../../appendix/change-rollout-schema.md)"
        ),
        "docs/book/part-viii/chapter-20.en.md": (
            "[Change Review and Rollout Gate Schema]"
            "(../../appendix/change-rollout-schema.en.md)"
        ),
        "docs/book/part-viii/chapter-20.zh.md": (
            "[评测数据集模式与打分契约](../../appendix/eval-schema.zh.md)",
            "[策略包模式与审批契约]"
            "(../../appendix/policy-bundle-schema.zh.md)",
            "[生命周期工件模式]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
            "[变更评审与发布门禁模式]"
            "(../../appendix/change-rollout-schema.zh.md)",
        ),
    }

    for path, expected_snippets in expected_snippets_by_file.items():
        text = _read(path)
        if isinstance(expected_snippets, str):
            expected_snippets = (expected_snippets,)
        for expected_snippet in expected_snippets:
            assert expected_snippet in text, (path, expected_snippet)


def test_chapter_20_chinese_evidence_spine_link_is_localized() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-20.zh.md")
    expected_markers = (
        "事故和发布（rollout）判断如何被维持在同一条链上",
        "打开[证据主干（Evidence Spine）](../part-v/evidence-spine.zh.md)",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "事故和 rollout 判断如何被维持在同一条链上",
        "打开 [Evidence Spine](../part-v/evidence-spine.zh.md)",
        "打开[Evidence Spine](../part-v/evidence-spine.zh.md)",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chapter_20_chinese_useful_ref_links_are_tightened() -> None:
    chinese_text = _read("docs/book/part-viii/chapter-20.zh.md")
    expected_markers = (
        "可以打开[变更评审与发布门禁模式]",
        "生命周期工件模式](../../appendix/lifecycle-artifact-schema.zh.md)和[评测数据集模式与打分契约]",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "可以打开 [变更评审与发布门禁模式]",
        "生命周期工件模式](../../appendix/lifecycle-artifact-schema.zh.md) 和 "
        "[评测数据集模式与打分契约]",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chapter_20_change_packets_thread_three_canonical_cases() -> None:
    common_markers = (
        "Change case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "write capabilities",
        "freshness windows",
    )
    expected_markers_by_file = {
        "docs/book/part-viii/chapter-20.md": (
            "Заметка о сквозных сценариях управления изменениями",
            "Разбор обращений поддержки",
            "Внутренний ассистент знаний",
            "Координация инцидентов",
            "пишущих возможностей",
            "окон свежести",
            "правил подтверждения",
            "корпуса извлечения",
            "семантики записи в память",
            "состояния инцидента",
        ),
        "docs/book/part-viii/chapter-20.en.md": (
            *common_markers,
            "approval rules",
            "retrieval corpus",
            "memory write semantics",
            "incident state",
        ),
        "docs/book/part-viii/chapter-20.zh.md": (
            "变更案例主线说明（Change case-spine note）",
            "支持分诊（Support triage）",
            "内部知识助手（Internal knowledge assistant）",
            "事故协调（Incident coordination）",
            "变更包（change packet）",
            "规范案例（canonical cases）",
            "重试（retries）",
            "写入能力（write capabilities）",
            "发布承载变更（release-bearing）",
            "新鲜度窗口（freshness windows）",
            "访问控制（access control）",
            "负责人转移（ownership transfer）",
            "审批规则（approval rules）",
            "检索语料（retrieval corpus）",
            "记忆写入语义（memory write semantics）",
            "事故状态（incident state）",
        ),
    }

    for path, expected_markers in expected_markers_by_file.items():
        text = _read(path)
        for expected_marker in expected_markers:
            assert expected_marker in text, (path, expected_marker)

    chinese_text = _read("docs/book/part-viii/chapter-20.zh.md")
    forbidden_chinese_markers = (
        "**Change case-spine note：**",
        "change packet 应该能对三个 canonical cases",
        "三个 canonical cases",
        "Support triage 会让",
        "Internal knowledge assistant 会让",
        "Incident coordination 会让",
        "retries 和 write capabilities 的变化变成 release-bearing",
        "freshness windows、",
        "access control 的变化变成 release-bearing",
        "ownership transfer 和",
    )
    for forbidden_chinese_marker in forbidden_chinese_markers:
        assert forbidden_chinese_marker not in chinese_text, forbidden_chinese_marker


def test_chapter_20_change_case_spine_links_are_clickable() -> None:
    expected_links_by_file = {
        "docs/book/part-viii/chapter-20.md": (
            "../../appendix/approval-schema.md",
            "../../appendix/memory-retrieval-schema.md",
            "../../appendix/incident-record-schema.md",
        ),
        "docs/book/part-viii/chapter-20.en.md": (
            "../../appendix/approval-schema.en.md",
            "../../appendix/memory-retrieval-schema.en.md",
            "../../appendix/incident-record-schema.en.md",
        ),
        "docs/book/part-viii/chapter-20.zh.md": (
            "../../appendix/approval-schema.zh.md",
            "../../appendix/memory-retrieval-schema.zh.md",
            "../../appendix/incident-record-schema.zh.md",
        ),
    }

    for path, expected_links in expected_links_by_file.items():
        text = _read(path)
        for expected_link in expected_links:
            assert f"]({expected_link})" in text, (path, expected_link)

    chinese_text = _read("docs/book/part-viii/chapter-20.zh.md")
    expected_chinese_links = (
        "[审批规则（approval rules）](../../appendix/approval-schema.zh.md)",
        "[检索语料（retrieval corpus）]"
        "(../../appendix/memory-retrieval-schema.zh.md)",
        "[记忆写入语义（memory write semantics）]"
        "(../../appendix/memory-retrieval-schema.zh.md)",
        "[事故状态（incident state）]"
        "(../../appendix/incident-record-schema.zh.md)",
    )
    for expected_chinese_link in expected_chinese_links:
        assert expected_chinese_link in chinese_text, expected_chinese_link
    forbidden_chinese_links = (
        "[approval rules](../../appendix/approval-schema.zh.md)",
        "[retrieval corpus](../../appendix/memory-retrieval-schema.zh.md)",
        "[memory write semantics](../../appendix/memory-retrieval-schema.zh.md)",
        "[incident state](../../appendix/incident-record-schema.zh.md)",
    )
    for forbidden_chinese_link in forbidden_chinese_links:
        assert forbidden_chinese_link not in chinese_text, forbidden_chinese_link


def test_chapter_7_retrieval_threads_three_canonical_cases() -> None:
    required_markers = (
        "Retrieval case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "current ticket state",
        "source attribution",
        "freshness windows",
        "tenant filters",
        "stale-index detection",
        "durable lessons",
    )
    checked_files = (
        "docs/book/part-iii/chapter-7.md",
        "docs/book/part-iii/chapter-7.en.md",
        "docs/book/part-iii/chapter-7.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)
    for path in checked_files:
        text = _read(path)
        assert "internal knowledge assistant" not in text, path
        assert "incident coordination" not in text, path


def test_chapter_6_memory_threads_three_canonical_cases() -> None:
    required_markers = (
        "Memory case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "temporary ticket state",
        "source provenance",
        "freshness",
        "tenant boundaries",
        "handoff summaries",
        "post-incident lessons",
    )
    checked_files = (
        "docs/book/part-iii/chapter-6.md",
        "docs/book/part-iii/chapter-6.en.md",
        "docs/book/part-iii/chapter-6.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_chapter_4_gateway_threads_three_canonical_cases() -> None:
    required_markers = (
        "Gateway case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "governed writes",
        "scoped reads",
        "retrieval limits",
        "escalation tools",
        "notification tools",
        "incident state",
    )
    checked_files = (
        "docs/book/part-ii/chapter-4.md",
        "docs/book/part-ii/chapter-4.en.md",
        "docs/book/part-ii/chapter-4.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)
    for path in checked_files:
        text = _read(path)
        assert "internal knowledge assistant" not in text, path
        assert "incident coordination" not in text, path


def test_chapter_13_eval_suite_threads_three_canonical_cases() -> None:
    required_markers = (
        "Eval case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "duplicate tickets",
        "retrieval freshness",
        "memory provenance",
        "escalation timing",
        "response ownership",
        "regression cases",
    )
    checked_files = (
        "docs/book/part-v/chapter-13.md",
        "docs/book/part-v/chapter-13.en.md",
        "docs/book/part-v/chapter-13.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_chapter_13_verifier_verdict_schema_links_are_clickable() -> None:
    expected_snippets_by_file = {
        "docs/book/part-v/chapter-13.md": (
            "](../../appendix/eval-schema.md)",
            "](../../appendix/trace-schema.md)",
        ),
        "docs/book/part-v/chapter-13.en.md": (
            "](../../appendix/eval-schema.en.md)",
            "](../../appendix/trace-schema.en.md)",
        ),
        "docs/book/part-v/chapter-13.zh.md": (
            "[验证器裁决记录（verifier verdict record）]"
            "(../../appendix/eval-schema.zh.md)",
            "[追踪模式（trace schema）](../../appendix/trace-schema.zh.md)",
            "[追踪模式与事件目录](../../appendix/trace-schema.zh.md)",
            "[评测数据集模式与打分契约]"
            "(../../appendix/eval-schema.zh.md)",
            "[生命周期工件模式]"
            "(../../appendix/lifecycle-artifact-schema.zh.md)",
        ),
    }

    for path, expected_links in expected_snippets_by_file.items():
        text = _read(path)
        for expected_link in expected_links:
            assert expected_link in text, (path, expected_link)


def test_evidence_spine_threads_three_canonical_cases() -> None:
    required_markers_by_file = {
        "docs/book/part-v/evidence-spine.md": (
            "Заметка о сквозной цепочке доказательств",
            "Разбор обращений поддержки",
            "Внутренний ассистент знаний",
            "Координация инцидентов",
            "подтверждения",
            "происхождение поиска",
            "владение ответом",
            "решение о поэтапном выпуске после инцидента",
        ),
        "docs/book/part-v/evidence-spine.en.md": (
            "Case-spine routing note",
            "Support triage",
            "Internal knowledge assistant",
            "Incident coordination",
            "approvals",
            "retrieval provenance",
            "response ownership",
            "post-incident rollout judgment",
        ),
        "docs/book/part-v/evidence-spine.zh.md": (
            "Case-spine routing note",
            "Support triage",
            "Internal knowledge assistant",
            "Incident coordination",
            "approvals",
            "retrieval provenance",
            "response ownership",
            "post-incident rollout judgment",
        ),
    }
    deprecated_markers = (
        "support-triage agent",
        "internal knowledge assistant stresses",
        "incident coordination stresses",
    )

    for path, required_markers in required_markers_by_file.items():
        _assert_files_contain_all((path,), required_markers)
    checked_files = tuple(required_markers_by_file)

    for path, required_markers in required_markers_by_file.items():
        _assert_files_contain_all((path,), required_markers)
    for path in checked_files:
        text = _read(path)
        for marker in deprecated_markers:
            assert marker not in text, (path, marker)


def test_chapter_1_decision_frame_is_print_friendly() -> None:
    chapter_sections = {
        "docs/book/part-i/chapter-1.md": (
            "## 6.",
            "## 7.",
            "Печатная рамка выбора",
            ("рабочий процесс", "одиночный агентный цикл", "многоагентная схема"),
        ),
        "docs/book/part-i/chapter-1.en.md": (
            "## 6.",
            "## 7.",
            "Print-ready decision frame",
            ("workflow", "single-agent loop", "multi-agent"),
        ),
        "docs/book/part-i/chapter-1.zh.md": (
            "## 6.",
            "## 7.",
            "适合印刷的判断框架",
            ("workflow", "single-agent loop", "multi-agent"),
        ),
    }

    for path, (start_marker, end_marker, title_marker, expected_terms) in chapter_sections.items():
        text = _read(path)
        section = text.split(start_marker, 1)[1].split(end_marker, 1)[0]
        assert title_marker in section
        assert "|" not in section
        assert "!!! info" not in section
        for expected_term in expected_terms:
            assert expected_term in section


def test_chapter_2_layer_map_is_print_friendly() -> None:
    chapter_sections = {
        "docs/book/part-i/chapter-2.md": ("## 4.", "## 5.", "Входной слой"),
        "docs/book/part-i/chapter-2.en.md": ("## 4.", "## 5.", "Interface layer"),
        "docs/book/part-i/chapter-2.zh.md": ("## 4.", "## 5.", "接口层"),
    }

    for path, (start_marker, end_marker, title_marker) in chapter_sections.items():
        text = _read(path)
        section = text.split(start_marker, 1)[1].split(end_marker, 1)[0]
        assert title_marker in section
        assert "|" not in section
        assert "control" in section or "управления" in section or "控制" in section
        assert "runtime" in section or "рантайм" in section or "运行时" in section
        assert "Telemetry" in section or "Телеметрия" in section or "遥测" in section


def test_reference_final_rule_stays_as_separate_bullet_list() -> None:
    expected = {
        "docs/reference.md": (
            "Самое простое правило такое:\n\n- книгу используй",
            "- справочный слой используй",
        ),
        "docs/reference.en.md": (
            "The simplest rule is:\n\n- use the book",
            "- use the reference layer",
        ),
        "docs/reference.zh.md": (
            "最简单的规则是：\n\n- 用本书",
            "- 用参考层",
        ),
    }

    for path, markers in expected.items():
        text = _read(path)
        for marker in markers:
            assert marker in text, (path, marker)


def test_russian_reference_fast_topic_routes_are_localized() -> None:
    text = _read("docs/reference.md")

    assert "Каталог инструментов, семантическая фильтрация инструментов" in text
    assert "классификация чтения и записи" in text
    assert "Роли MCP: хост, клиент и сервер" in text
    assert "передача возможностей" in text
    assert "границы песочницы" in text
    assert "Семантический разрыв, HyDE" in text
    assert "выбор между RAG и обучением модели" in text
    assert "Бюджет задержки" in text
    assert "быстрый/медленный путь и маршрутизированные конвейеры" in text
    assert "Оценка через языковую модель как судью, калибровка" in text
    assert "согласие судьи с человеком" in text

    forbidden_markers = (
        "- Tool catalog, semantic tool filtering, read/write taxonomy:",
        "(semantic tool filtering)",
        "(read/write taxonomy)",
        "(MCP host/client/server)",
        "(capability transport)",
        "(sandbox boundary)",
        "(semantic gap)",
        "(RAG vs training)",
        "(latency budget)",
        "(LLM-as-a-judge)",
        "(judge-human agreement)",
        "семантическая фильтрация инструментов (`semantic tool filtering`)",
        "классификация чтения/записи:",
        "- MCP host/client/server, capability transport, sandbox boundary:",
        "Роли MCP: `host`, `client` и `server`",
        "- Semantic gap, HyDE, RAG vs training:",
        "Семантический разрыв (`semantic gap`), `HyDE`",
        "выбор между RAG и обучением модели (`RAG vs training`)",
        "- Latency budget, fast path / slow path, routed pipeline:",
        "Бюджет задержки (`latency budget`)",
        "- LLM-as-a-judge, calibration и judge-human agreement:",
        "Оценка через `LLM-as-a-judge`",
        "согласие судьи с человеком (`judge-human agreement`)",
    )

    for marker in forbidden_markers:
        assert marker not in text, marker


def test_chinese_reference_fast_topic_routes_are_localized() -> None:
    text = _read("docs/reference.zh.md")

    assert "工具目录设计、语义化工具过滤（semantic tool filtering）" in text
    assert "读/写分类法（read/write taxonomy）" in text
    assert "MCP 主机/客户端/服务器角色（MCP host/client/server）" in text
    assert "能力传输（capability transport）" in text
    assert "沙箱边界（sandbox boundary）" in text
    assert "语义鸿沟（semantic gap）、HyDE、RAG 与训练的取舍（RAG vs training）" in text
    assert "延迟预算（latency budget）、快路径/慢路径、路由管线" in text
    assert "以 LLM 作为评审器（LLM-as-a-judge）、校准" in text
    assert "评审器/人类一致性（judge-human agreement）" in text

    forbidden_markers = (
        "工具目录设计、语义化工具过滤、读/写分类法",
        "MCP 主机/客户端/服务器角色、能力传输、沙箱边界",
        "延迟预算、快路径/慢路径、路由管线",
        "Latency budget, fast path / slow path, routed pipeline",
        "语义鸿沟、HyDE、RAG 与训练的取舍",
        "LLM-as-a-judge、校准与评审器/人类一致性",
    )

    for marker in forbidden_markers:
        assert marker not in text, marker


def test_english_book_plan_matches_home_publication_status() -> None:
    required_markers = (
        "Current publication status",
        "RU core manuscript",
        "published across eight book parts",
        "EN translation layer",
        "readable draft in editorial cleanup",
        "ZH translation layer",
        "readable draft localization preview in editorial cleanup",
        "Reference layer",
        "active companion material",
        "Runtime package",
        "runnable reference implementation and examples, not a production framework",
        "Print/readiness package",
        "in progress",
        "not a finished print-ready manuscript",
    )
    deprecated_markers = (
        "first chapter is published",
        "First chapter is published",
        "first part",
        "First part",
        "first set of practical case studies",
        "source base for the next chapters",
        "Publisher package",
        "publisher package",
        "publisher-ready",
    )

    plan = _read("docs/book/plan.en.md")
    home = _read("docs/index.en.md")

    for marker in required_markers:
        assert marker in plan
    assert "Published Russian core manuscript across eight book parts" in home
    assert "Draft `en` and `zh` translation layers" in home
    for marker in deprecated_markers:
        assert marker not in plan


def test_whats_new_publisher_readiness_claim_stays_scoped() -> None:
    date_markers_by_file = {
        "docs/whats-new.md": (
            "Актуально на 20 мая 2026 года",
            "Актуально на 4 июня 2026 года",
        ),
        "docs/whats-new.en.md": (
            "Current as of May 20, 2026",
            "Current as of June 4, 2026",
        ),
        "docs/whats-new.zh.md": (
            "更新于 2026 年 5 月 20 日",
            "更新于 2026 年 6 月 4 日",
        ),
    }
    expected_by_file = {
        "docs/whats-new.md": (
            "Проход качества для печатной версии идет, но еще не закрыт полностью.",
            "Более широкий проход качества для печатной версии и публикации остается в работе.",
            "черновые и плановые страницы исключены из опубликованного сайта",
            "исключены из опубликованного сайта и карты сайта",
            "метаданные для OpenGraph и Twitter и изображение для предпросмотра в соцсетях",
            "проверены поисковый индекс, карта сайта, файл robots, "
            "локальные ресурсы, якоря",
            "альтернативный текст и внешние ссылки",
            "резервные канонические редиректы покрывают основные точки входа",
            "запись о доступности публичных ссылок обновлена 20 мая 2026 года",
            "все девять ссылок из пакета публичных материалов вернули HTTP 200",
            "реестр блокеров, журнал решений/исключений, ограничение длины строк",
            "названия пакета материалов устойчивы для печати и экспорта",
            "карта ролей части VIII теперь устойчива для печати",
            "Глава 1 получила начальный читательский ориентир",
            "компактный печатный вывод",
            "без живой навигации сайта",
            "Глава 13 получила технический читательский ориентир",
            "оценочный набор -> контракт проверяющего -> шлюз раскатки",
            "файлы README на трех языках теперь содержат проверочный список "
            "быстрой синхронизации публикации",
            "До готовности к печатной версии еще остаются",
            "проверка английского и китайского слоев",
            "независимая проверка качества HTML/PDF и экспорта",
            "независимая вычитка образцовых глав",
            "независимая проверка качества экспорта образцовых глав",
            "упаковка печатной рукописи и онлайн-приложения под конкретный формат подачи",
            "не выглядеть как черновая сборка из файлов Markdown",
        ),
        "docs/whats-new.en.md": (
            "The print/publication quality pass is in progress, not fully closed.",
            "The broader print/publication quality pass remains in progress.",
            "draft and planning pages are excluded from the published site",
            "OpenGraph/Twitter metadata and a social preview image",
            "search index, sitemap, robots file",
            "canonical fallback redirects cover the main hand-copied entry points",
            "public-link availability record was refreshed on May 20, 2026",
            "all nine public-packet links returned HTTP 200",
            "line-length guard, and packet labels are print/export-friendly",
            "Part VIII role map is now print-friendly",
            "Chapter 1 now has a reader orientation block",
            "compact print-ready exit",
            "without relying on live site navigation",
            "Chapter 13 now has a technical reader orientation",
            "eval dataset -> verifier contract -> rollout gate",
            "Remaining before this can be called print-ready",
            "deep EN/ZH cleanup",
            "independent rendering/export QA",
            "independent sample copy-edit",
            "sample export QA",
        ),
        "docs/whats-new.zh.md": (
            "### 发布前站点表面更干净",
            "面向印刷与发布的质量检查正在进行中，但还没有完全关闭。",
            "更广泛的印刷与发布质量检查仍在进行中。",
            "已完成的站点工作：",
            "草稿与规划页面已从发布站点和站点地图（sitemap）中排除",
            "OpenGraph/Twitter 元数据和社交预览图（social preview image）",
            "检查了搜索索引（search index）、站点地图（sitemap）、robots 文件（robots file）",
            "本地资源（local assets）、锚点（anchors）",
            "图片替代文本（alt text）和外部链接（external links）",
            "基础导航和规范备用重定向（canonical fallback redirects）"
            "已覆盖人们最容易手动复制的主要入口",
            "公共链接可用性记录（public-link availability record）已在 2026 年 5 月 20 日刷新",
            "公开材料包中的九个链接全部返回 HTTP 200",
            "公开材料包的阻塞项登记表（blocker register）",
            "豁免与决策日志（waiver/decision log）",
            "行长限制（line-length guard）与材料包标签（packet labels）现在都适合打印和导出",
            "第 VIII 部分角色图（role map）现在适合打印和导出",
            "第 1 章现在有读者导向块",
            "稳定的判断框架",
            "不依赖网站实时导航",
            "第 13 章现在有技术读者导向",
            "评测数据集 -> 验证器契约 -> 发布门禁",
            "快速同步发布检查清单（quick sync publish checklist）",
            "在称为可印刷版本之前",
            "EN/ZH 清理（deep EN/ZH cleanup）",
            "独立 HTML/PDF 渲染/导出质量检查（independent rendering/export QA）",
            "独立样章审校（independent sample copy-edit）",
            "样章导出质量检查（sample export QA）",
            "面向具体提交格式的纸质稿件与在线配套材料包装",
        ),
    }
    forbidden = (
        "publisher-facing layer is fully closed",
        "publisher-facing слой полностью закрыт",
        "面向出版的质量层已经完全关闭",
        "Издательский проход качества",
        "издательского пакета",
        "конкретного издателя",
        "publisher-facing quality pass",
        "publisher-packet links",
        "publisher packet",
        "publisher-ready",
        "出版材料包",
        "面向具体出版社",
        "publisher-specific print/companion packaging",
        "### 发布前站点更干净了",
        "已经完成：",
        "Current as of May 19, 2026",
        "исключены из опубликованного сайта и sitemap",
        "Актуально на 19 мая 2026 года",
        "更新于 2026 年 5 月 19 日",
        "canonical fallback redirects покрывают основные entry points",
        "сырая сборка из Markdown-файлов",
        "сырая сборка из файлов Markdown",
        "резервные canonical redirects покрывают основные точки входа",
        "резервные canonical-редиректы покрывают основные точки входа",
        "basic navigation 和 canonical fallback redirects",
        "publisher-packet links вернули HTTP 200",
        "publisher packet вернули HTTP 200",
        "названия publisher packet устойчивы",
        "九个 publisher-packet links 全部返回 HTTP 200",
        "九个 publisher packet 链接全部返回 HTTP 200",
        "公共链接可用性记录已在 2026 年 5 月 20 日刷新",
        "печати/export",
        "打印/export",
        "打印/导出",
        "第 VIII 部分角色图现在适合打印导出",
        "第 VIII 部分角色图现在适合打印和导出",
        "role map части VIII",
        "Part VIII 角色图",
        "checklist быстрой синхронизации публикации",
        "чек-лист быстрой синхронизации публикации",
        "快速同步发布检查清单。",
        "README на трех языках теперь содержит чек-лист",
        "OpenGraph/Twitter metadata и социальная preview-картинка",
        "метаданные OpenGraph/Twitter и изображение для социальных превью",
        "социальная превью-картинка",
        "изображение для социальных превью",
        "проверены search index, sitemap, robots",
        "проверены поисковый индекс, sitemap, robots, локальные ресурсы",
        "проверены поисковый индекс, sitemap, файл robots",
        "локальные assets",
        "локальные ресурсы, anchors, alt text",
        "локальные ресурсы, якоря, alt-тексты",
        "альтернативные тексты (alt text)",
        "полировка Главы 13",
        "Chapter 13 sample polish",
        "第 13 章样章打磨（Chapter 13 sample polish）",
        "EN/ZH-проверка",
        "проверка EN/ZH-слоев",
        "EN/ZH-слоев",
        "深层 EN/ZH 清理、",
        "независимый HTML/PDF/export QA",
        "независимый QA HTML/PDF/экспорта",
        "независимая проверка качества (QA) HTML/PDF/экспорта",
        "независимая проверка качества (QA) HTML/PDF и экспорта",
        "blocker register, waiver/decision log, ограничение длины строк",
        "publisher packet blocker register、waiver/decision log",
        "реестр блокеров, waiver/decision log",
        "publisher packet 阻塞项登记表、waiver/decision log",
        "publisher packet 中的九个链接全部返回 HTTP 200",
        "publisher packet 阻塞项登记表、豁免/决策日志、行长限制",
        "出版材料包（publisher packet）的阻塞项登记表、豁免/决策日志、行长限制",
        "出版材料包（publisher packet）的阻塞项登记表、豁免与决策日志、行长限制",
        "阻塞项登记表（blocker register）、豁免与决策日志、行长限制",
        "豁免与决策日志（waiver/decision log）、行长限制与材料包标签",
        "packet 标签现在都适合打印和导出",
        "OpenGraph/Twitter metadata 和社交预览图",
        "OpenGraph/Twitter 元数据和社交预览图；",
        "robots 文件、本地资源、锚点",
        "robots 文件、本地资源（local assets）",
        "草稿与规划页面已从发布站点和 sitemap 中排除",
        "检查了搜索索引、sitemap、robots",
        "检查了搜索索引、站点地图（sitemap）",
        "图片 alt 文本和外部链接",
        "图片替代文本（alt text）和外部链接；",
        "独立 HTML/PDF/export QA",
        "独立 HTML/PDF/导出 QA",
        "独立 HTML/PDF/导出质量检查（QA）",
        "基础导航和 canonical fallback redirects 已覆盖",
        "基础导航和 canonical 备用重定向已覆盖",
        "面向具体出版社的纸质稿件/在线配套材料包装",
        "面向具体出版社的纸质稿件与在线配套材料包装。",
        "独立 HTML/PDF 渲染/导出质量检查（independent rendering/export QA）、样章打磨，",
    )

    for path, expected_markers in expected_by_file.items():
        text = _read(path)
        assert any(marker in text for marker in date_markers_by_file[path]), path
        for marker in expected_markers:
            assert marker in text, (path, marker)
        for marker in forbidden:
            assert marker not in text, (path, marker)


def test_russian_whats_new_intro_note_is_localized() -> None:
    text = _read("docs/whats-new.md")

    assert "крупных улучшений книги и эталонного пакета" in text
    assert "не заменяет историю Git" in text
    assert "как развивается проект и какие слои уже появились" in text
    assert "крупных улучшений книги и опорного пакета" not in text
    assert "насколько проект живой и какие слои уже появились" not in text
    assert "не заменяет git history" not in text


def test_chinese_whats_new_intro_note_is_localized() -> None:
    text = _read("docs/whats-new.zh.md")

    assert "Git 历史记录（Git history）的替代品" in text
    assert "不是 Git 历史的替代品" not in text


def test_russian_whats_new_section_headings_are_localized() -> None:
    text = _read("docs/whats-new.md")

    expected_headings = (
        "## Книга",
        "## Справочный слой",
        "## Эталонная среда исполнения",
        "## Практическое приложение",
        "## Навигация",
        "## Готовность к печати и публикации",
    )
    stale_headings = (
        "## Book",
        "## Reference",
        "## Runtime",
        "## Practical Appendix",
        "## Navigation",
        "## Publish readiness",
    )

    for heading in expected_headings:
        assert heading in text
    for heading in stale_headings:
        assert heading not in text


def test_russian_whats_new_runtime_heading_is_localized() -> None:
    text = _read("docs/whats-new.md")

    assert "### Возможности эталонной среды исполнения" in text
    assert "### Runnable reference runtime" not in text
    assert "### Исполняемый эталонный runtime" not in text
    assert "### Исполняемая эталонная среда исполнения (runtime)" not in text


def test_russian_whats_new_reader_value_note_is_localized() -> None:
    text = _read("docs/whats-new.md")

    assert "Можно читать книгу как практическое руководство." in text
    assert "Можно использовать справочные страницы как инженерные заготовки." in text
    assert "Можно запускать примерный исполняемый пакет, а не только читать файлы Markdown." in text
    assert "Можно читать книгу как handbook." not in text
    assert "Можно использовать reference pages как инженерные заготовки." not in text
    assert "Можно запускать примерный runtime, а не только читать Markdown." not in text
    assert "Можно запускать примерный исполняемый пакет, а не только читать Markdown." not in text
    assert (
        "Можно запускать примерный исполняемый пакет, а не только читать Markdown-файлы."
        not in text
    )


def test_russian_whats_new_canonical_case_note_is_localized() -> None:
    text = _read("docs/whats-new.md")

    assert '!!! note "Обновление канонических сценариев"' in text
    assert "сквозная карта трех канонических сценариев" in text
    assert "Триаж обращений поддержки" in text
    assert "внутренний ассистент знаний" in text
    assert "координация инцидентов" in text
    assert "главах книги" in text
    assert "публичных точках входа" in text
    assert "справочных страницах" in text
    assert "артефактах приложений" in text
    assert "проверки покрытия защищают главы и страницы приложений" in text
    assert '!!! note "Canonical case update"' not in text
    assert '!!! note "Обновление canonical cases"' not in text
    assert "сквозная карта трех canonical cases" not in text
    assert "**Support triage**, **Internal knowledge assistant**" not in text
    assert "book chapters" not in text
    assert "public entry points" not in text
    assert "reference pages" not in text
    assert "appendix artifacts" not in text
    assert "chapters и appendix pages" not in text
    assert "coverage guards" not in text


def test_russian_whats_new_safe_agent_note_is_localized() -> None:
    text = _read("docs/whats-new.md")

    assert '!!! note "Обновление схем безопасного агента"' in text
    assert (
        "связали прозу, приложения и защитные проверки для архитектуры "
        "безопасного агента"
        in text
    )
    assert "модель угроз для MCP и контракт `mcp_server`" in text
    assert "контракт доверия для передачи управления A2A" in text
    assert "артефакт делегирования доверия" in text
    assert "карта эшелонированной защиты" in text
    assert "запись вердикта проверяющего" in text
    assert "запись управленческого действия" in text
    assert "сопоставление телеметрии с NIST AI RMF" in text
    assert "поля проверки отравления памяти" in text
    assert "единая модель доказательств угроз агентам" in text
    assert "[схеме трасс](appendix/trace-schema.md)" in text
    assert "[схеме оценивания](appendix/eval-schema.md)" in text
    assert "[схеме памяти и поиска](appendix/memory-retrieval-schema.md)" in text
    assert '!!! note "Safe-agent schema update"' not in text
    assert '!!! note "Обновление safe-agent схем"' not in text
    assert '!!! note "Обновление схем safe-agent"' not in text
    assert "защитные проверки для safe-agent архитектуры" not in text
    assert "защитные проверки для архитектуры safe-agent" not in text
    assert "связали prose, appendices и guards" not in text
    assert "связали прозу, приложения и guards" not in text
    assert "MCP threat model и `mcp_server` contract" not in text
    assert "модель угроз MCP и контракт `mcp_server`" not in text
    assert "A2A handoff trust contract" not in text
    assert "контракт доверия для A2A handoff" not in text
    assert "контракт доверия для передачи A2A (handoff)" not in text
    assert "trust-delegation artifact" not in text
    assert "артефакт trust-delegation" not in text
    assert "defense-in-depth control map" not in text
    assert "карта defense-in-depth controls" not in text
    assert "карта defense-in-depth-контролей" not in text
    assert "verifier verdict record" not in text
    assert "запись verifier verdict" not in text
    assert "governance action record" not in text
    assert "запись governance action" not in text
    assert "NIST AI RMF telemetry mapping" not in text
    assert "сопоставление телеметрии NIST AI RMF" not in text
    assert "memory poisoning review fields" not in text
    assert "поля проверки memory poisoning" not in text
    assert "unified agent threat evidence" not in text
    assert "единая evidence-модель угроз агентам" not in text
    assert "[trace schema](appendix/trace-schema.md)" not in text
    assert "[eval schema](appendix/eval-schema.md)" not in text
    assert "[memory/retrieval schema](appendix/memory-retrieval-schema.md)" not in text


def test_russian_whats_new_book_note_is_localized() -> None:
    text = _read("docs/whats-new.md")

    assert "первый срез редакционной проверки качества" in text
    assert "рамка принятия решений в Главе 1" in text
    assert "для HTML/PDF и извлечения в простой текст" in text
    assert "часто обновляемые главы, «Источники» и «Что нового»" in text
    assert "особенностей отображения таблиц" in text
    assert "подвижные разделы по безопасности агентов" in text
    assert "пакет замечаний издательской проверки качества" not in text
    assert "издательского QA" not in text
    assert "decision frame в Главе 1" not in text
    assert "для HTML/PDF/plain-text extraction" not in text
    assert "извлечения в plain text" not in text
    assert "fast-moving главы" not in text
    assert "быстро меняющиеся главы" not in text
    assert "Sources и What’s New" not in text
    assert "agent-security разделы" not in text
    assert "особенностей рендера таблиц" not in text


def test_chinese_whats_new_book_note_is_localized() -> None:
    text = _read("docs/whats-new.zh.md")

    assert "### 2026 年 5 月 14 日编辑质量检查（QA）" in text
    assert "第一轮评审修复质量检查（QA）切片已经关闭" in text
    assert "更适合 HTML/PDF 与纯文本抽取的文字块" in text
    assert "快速变化的智能体安全（agent-security）章节" in text
    assert "第一组出版就绪质量检查（QA）问题已经关闭" not in text
    assert "### 2026 年 5 月 14 日编辑 QA" not in text
    assert "第一组出版就绪 QA 问题已经关闭" not in text
    assert "HTML/PDF/纯文本抽取" not in text
    assert "快速变化的 agent-security 章节" not in text


def test_chinese_whats_new_lifecycle_note_is_localized() -> None:
    text = _read("docs/whats-new.zh.md")

    assert "从软件开发生命周期到智能体开发生命周期（`SDLC→ADLC`）的迁移" in text
    assert "AI 原生（`AI-native`）可观测性" in text
    assert "现在全书已经包含 `SDLC→ADLC`、变更管理" not in text
    assert "AI 原生可观测性" not in text


def test_russian_whats_new_lifecycle_note_is_localized() -> None:
    text = _read("docs/whats-new.md")

    assert "Часть VIII про жизненный цикл агентной системы" in text
    assert "переход от `SDLC` к `ADLC`" in text
    assert "управление изменениями" in text
    assert "контур обеспечения доверия" in text
    assert "цепочку поставки" in text
    assert "вывод из эксплуатации" in text
    assert "расхождение целей" in text
    assert "поведенческие оценки" in text
    assert "наблюдаемость систем, изначально ориентированных на AI" in text
    assert "контроль инвентаризации" in text
    assert "change management" not in text
    assert "блок про `SDLC -> ADLC`" not in text
    assert "assurance loop" not in text
    assert "контур assurance" not in text
    assert "supply chain" not in text
    assert "retirement" not in text
    assert "вывод из эксплуатации, misalignment" not in text
    assert "behavioral evals" not in text
    assert "поведенческие evals" not in text
    assert "AI-native observability" not in text
    assert "AI-native-наблюдаемость (observability)" not in text
    assert "наблюдаемость AI-native-систем (observability)" not in text
    assert "inventory control" not in text
    assert "контроль inventory" not in text
    assert "контроль инвентаря (inventory)" not in text


def test_chinese_whats_new_production_note_is_localized() -> None:
    text = _read("docs/whats-new.zh.md")

    assert "提示注入（`prompt injection`）、越狱（`jailbreaking`）" in text
    assert "动作幻觉（`action hallucination`）分类法" in text
    assert "语义鸿沟（`semantic gap`）" in text
    assert "RAG 优先（`RAG first`）" in text
    assert "持续预训练（`continued pretraining`）与 `SFT` 的区别" in text
    assert "大型工具目录、语义工具过滤（`semantic tool filtering`）" in text
    assert "MCP 主机/客户端/服务器（`MCP host/client/server`）角色" in text
    assert "延迟预算（`latency budget`）" in text
    assert "以 LLM 作为评审器（`LLM-as-a-judge`）" in text
    assert "`prompt injection`、`jailbreaking` 与 `action hallucination` 分类法" not in text
    assert "检索轮廓：`semantic gap`、`HyDE`、`RAG first`" not in text
    assert "持续预训练与 `SFT` 的区别" not in text
    assert "持续预训练（continued pretraining）与 `SFT` 的区别" not in text
    assert "大工具目录、`semantic tool filtering` 和 `MCP host/client/server` 角色" not in text
    assert "补上了大工具目录、语义工具过滤" not in text
    assert "`latency budget` 的产品视角" not in text
    assert "实用的 `LLM-as-a-judge` 表述" not in text


def test_russian_whats_new_production_note_is_localized() -> None:
    text = _read("docs/whats-new.md")

    assert "Усилен эксплуатационный контур в частях I-V" in text
    assert "между архитектурой, поиском по знаниям, исполнением" in text
    assert "и дисциплиной оценивания" in text
    assert "архитектура исполнения, слой обучения и продуктовая поверхность" in text
    assert "более четкая таксономия для инъекций в запросы" in text
    assert "обхода ограничений" in text
    assert "галлюцинаций действий" in text
    assert "усилен контур поиска по знаниям" in text
    assert "семантический разрыв" in text
    assert "подход «сначала RAG»" in text
    assert "различие между продолженным предобучением и `SFT`" in text
    assert "добавлены практические правила для больших каталогов инструментов" in text
    assert "семантическая фильтрация инструментов" in text
    assert "явные роли MCP: `host`, `client` и `server`" in text
    assert "продуктовый разбор бюджета задержки" in text
    assert "практическая рамка для оценки через `LLM-as-a-judge`" in text
    assert "базовые платформенные слои" in text
    assert "между обсуждением дизайна, циклом оценивания и раскаткой" in text
    assert "повседневные вопросы эксплуатационной команды" in text
    assert "читательских точек входа" in text
    assert "семантическая фильтрация инструментов" in text
    assert "`HyDE` и выбор между RAG и обучением модели" in text
    assert "бюджет задержки и маршрутизированные конвейеры" in text
    assert "оценка через `LLM-as-a-judge` и калибровка судьи" in text
    assert "инъекцией промптов" in text
    assert "обходом ограничений" in text
    assert "галлюцинациями действий" in text
    assert "Усилен production contour" not in text
    assert "Усилен production-контур" not in text
    assert "между архитектурой, retrieval, execution и eval discipline" not in text
    assert "между архитектурой, retrieval, execution и eval-дисциплиной" not in text
    assert "исполнением и eval-дисциплиной" not in text
    assert "между архитектурой, retrieval, исполнением и eval-дисциплиной" not in text
    assert "между архитектурой, retrieval-поиском" not in text
    assert "training layer и product surface" not in text
    assert "training layer и продуктовая поверхность" not in text
    assert "runtime-архитектура, training-слой" not in text
    assert "training-слой" not in text
    assert "более четкая taxonomy для `prompt injection`" not in text
    assert "более четкая таксономия для `prompt injection`" not in text
    assert "`jailbreak` и `action hallucination`" not in text
    assert "`prompt injection`, `jailbreak`" not in text
    assert "усилен retrieval contour" not in text
    assert "retrieval-контур: `semantic gap`" not in text
    assert "усилен retrieval-контур" not in text
    assert "`HyDE`, `RAG first`, различие" not in text
    assert "подход RAG-first (`RAG first`)" not in text
    assert "различие между continued pretraining и `SFT`" not in text
    assert "различие между дообучением (continued pretraining)" not in text
    assert "добавлены practical rules для больших tool catalogs" not in text
    assert "практические правила для больших tool catalogs" not in text
    assert "каталогов инструментов, `semantic tool filtering`" not in text
    assert "явные роли `MCP host / client / server`" not in text
    assert "продуктовый взгляд на `latency budget`" not in text
    assert "продуктовый взгляд на бюджет задержки (`latency budget`)" not in text
    assert "practical framing для `LLM-as-a-judge`" not in text
    assert "практическая рамка для `LLM-as-a-judge`" not in text
    assert "базовые platform layers" not in text
    assert "между design review, eval loop и rollout" not in text
    assert "reader entry points" not in text
    assert "latency budget` и routed pipelines" not in text
    assert "`latency budget` и маршрутизированные конвейеры" not in text
    assert "- `semantic tool filtering`;" not in text
    assert "- `HyDE` и `RAG vs training`;" not in text
    assert "`HyDE` и выбор между RAG и обучением (`RAG vs training`)" not in text
    assert "`LLM-as-a-judge` и judge calibration" not in text
    assert "- `LLM-as-a-judge` и калибровку судьи" not in text
    assert "между дизайн-ревью, eval loop и rollout" not in text
    assert "между дизайн-ревью, циклом оценивания (eval) и раскаткой" not in text
    assert "между дизайн-ревью, eval-циклом" not in text
    assert "между дизайн-ревью, eval-циклом и rollout" not in text
    assert "повседневные вопросы production-команды" not in text


def test_chinese_whats_new_navigation_topics_are_localized() -> None:
    text = _read("docs/whats-new.zh.md")

    assert "### 读者入口页更清晰" in text
    assert "已更新的入口页：" in text
    assert "### 入口页更强了" not in text
    assert "已更新：" not in text
    assert "语义工具过滤（`semantic tool filtering`）" in text
    assert "`HyDE` 与 RAG 与训练之间的取舍（`RAG vs training`）" in text
    assert "延迟预算（`latency budget`）与路由管线" in text
    assert "以 LLM 作为评审器（`LLM-as-a-judge`）与评审器校准" in text
    assert "提示注入（`prompt injection`）、越狱（`jailbreaking`）" in text
    assert "动作幻觉（`action hallucination`）的区别" in text

    forbidden_markers = (
        "- `semantic tool filtering`；",
        "- `HyDE` 与 `RAG vs training`；",
        "`HyDE` 与 RAG 和训练取舍（`RAG vs training`）",
        "`HyDE` 与 RAG 和训练之间的取舍（`RAG vs training`）",
        "- `latency budget` 与路由管线；",
        "- `LLM-as-a-judge` 与评审器校准；",
        "- `prompt injection`、`jailbreaking` 与 `action hallucination` 的区别。",
    )

    for marker in forbidden_markers:
        assert marker not in text, marker


def test_chinese_whats_new_runtime_note_is_localized() -> None:
    text = _read("docs/whats-new.zh.md")

    assert "委派授权上下文（delegated authorization context）" in text
    assert "控制机制与生命周期内的运行时控制检查（runtime-control inspection）" in text
    assert "生命周期工件（lifecycle artifacts）" in text
    assert "会话导出与回放摘要（replay summaries）" in text
    assert "评测数据集导出（eval dataset export）" in text
    assert "带数据遮蔽（redaction）、遮蔽后摘要（redacted summaries）" in text
    assert "回放保留（replay preservation）" in text
    assert "模式版本控制（schema versioning）" in text
    assert "追踪导出（trace export）" in text

    forbidden_markers = (
        "审批与 delegated authorization context",
        "控制项与 lifecycle runtime-control inspection",
        "控制项与生命周期内的运行时控制检查",
        "- 生命周期工件；\n- 会话导出与回放摘要",
        "会话导出与 replay summaries",
        "- 评测数据集导出；",
        "带 redaction、redacted summaries、replay preservation 与 schema versioning",
        "schema versioning）的追踪导出。",
    )

    for marker in forbidden_markers:
        assert marker not in text, marker


def test_russian_whats_new_runtime_note_is_localized() -> None:
    text = _read("docs/whats-new.md")

    assert "согласования и контекст делегирования авторизации" in text
    assert "контрольные механизмы и проверку управления исполнением" in text
    assert "в жизненном цикле" in text
    assert "артефакты жизненного цикла" in text
    assert "экспорт сессий и сводки воспроизведения" in text
    assert "экспорт оценочных наборов данных" in text
    assert "экспорт наборов данных eval" not in text
    assert "экспорт трасс с маскированием данных, очищенными сводками" in text
    assert "сохранением воспроизведения" in text
    assert "версионированием схем" in text
    assert "описательные главы" in text
    assert "работающую эталонную реализацию" in text

    forbidden_markers = (
        "approvals и delegated authorization context",
        "approvals и контекст делегированной авторизации",
        "согласования (approvals) и контекст делегированной авторизации",
        "controls и lifecycle runtime-control inspection",
        "controls и проверку runtime-control в lifecycle",
        "контрольные механизмы и проверку runtime-control в lifecycle",
        "контрольные механизмы и проверку runtime-control в жизненном цикле (lifecycle)",
        "lifecycle artifacts",
        "lifecycle-артефакты",
        "session export и replay summaries",
        "экспорт сессий и replay-сводки",
        "eval dataset export",
        "экспорт eval-наборов данных",
        "trace export с redaction",
        "экспорт trace с redaction",
        "экспорт trace с редактированием (redaction)",
        "экспорт трасс (trace) с редактированием (redaction)",
        "редактированными сводками",
        "redacted summaries",
        "replay preservation",
        "сохранением replay",
        "schema versioning",
        "narrative chapters",
        "runnable reference implementation",
    )

    for marker in forbidden_markers:
        assert marker not in text, marker


def test_russian_whats_new_reference_note_is_localized() -> None:
    text = _read("docs/whats-new.md")

    assert "### Переиспользуемые схемы и артефакты" in text
    assert "### Справочный слой с переиспользуемыми схемами" not in text
    assert "отдельные справочные страницы" in text
    assert "- трассировки и каталог событий;" in text
    assert "- оценочные наборы данных и контракт оценивания;" in text
    assert "- наборы данных eval и контракт оценивания;" not in text
    assert "- пакеты политик и контуры согласований;" in text
    assert "- ревью изменений и контрольные этапы раскатки;" in text
    assert "- артефакты жизненного цикла;" in text
    assert "- контракты поиска и извлечения из памяти." in text
    assert "проверяемым схемам и артефактам" in text

    forbidden_markers = (
        "Справочный слой с reusable schemas",
        "reference pages для",
        "- traces и event catalog;",
        "- traces и каталог событий;",
        "- трассы (traces) и каталог событий;",
        "- eval datasets и grading contract;",
        "- eval-наборы данных и контракт оценивания;",
        "- policy bundles и approvals;",
        "- пакеты политик и approvals-контуры;",
        "- change review и rollout gates;",
        "- ревью изменений и rollout gates;",
        "- ревью изменений и rollout-гейты;",
        "- ревью изменений и гейты раскатки;",
        "- lifecycle-артефакты;",
        "- memory retrieval contracts.",
        "- контракты извлечения из памяти.",
        "reviewable схемам",
    )

    for marker in forbidden_markers:
        assert marker not in text, marker


def test_chinese_whats_new_reference_note_is_localized() -> None:
    text = _read("docs/whats-new.zh.md")

    assert "### 可复用的模式与契约" in text
    assert "### 可复用的参考层" not in text
    assert "追踪与事件目录（traces and event catalog）" in text
    assert "评测数据集与评分契约（eval datasets and grading contracts）" in text
    assert "策略包与审批（policy bundles and approvals）" in text
    assert "变更评审与发布门禁（change review and rollout gates）" in text
    assert "生命周期工件（lifecycle artifacts）" in text
    assert "记忆检索契约（memory retrieval contracts）" in text
    assert "- 追踪与事件目录；" not in text
    assert "- 评测数据集与评分契约；" not in text
    assert "- 策略包与审批；" not in text
    assert "- 变更评审与发布门禁；" not in text
    assert "- 生命周期工件；\n- 记忆检索契约" not in text
    assert "- 记忆检索契约。" not in text


def test_chinese_whats_new_practical_appendix_note_is_localized() -> None:
    text = _read("docs/whats-new.zh.md")

    assert "### 检查清单与实践工件" in text
    assert "术语表（glossary）" in text
    assert "速查清单（cheat sheets）" in text
    assert "案例研究（case studies）" in text
    assert "策略模板（policy templates）" in text
    assert "研究前沿页面（research frontier page）" in text
    assert "社区路线图（community roadmap）" in text
    assert "### 更强的实践附录" not in text
    assert "- 术语表；" not in text
    assert "- 速查清单；" not in text
    assert "- 案例研究；" not in text
    assert "- 策略模板；" not in text
    assert "- 研究前沿页面；" not in text
    assert "- 社区路线图。" not in text


def test_russian_whats_new_practical_appendix_note_is_localized() -> None:
    text = _read("docs/whats-new.md")

    assert "## Практическое приложение" in text
    assert "### Практические материалы приложения" in text
    assert "### Практическое приложение" not in text
    assert "- глоссарий;" in text
    assert "- шпаргалки;" in text
    assert "- кейсы;" in text
    assert "- шаблоны политик;" in text
    assert "- исследовательский фронтир;" in text
    assert "- дорожная карта сообщества." in text
    assert "глоссарий и практические материалы" in text

    forbidden_markers = (
        "Практический appendix",
        "- glossary;",
        "- cheat sheets;",
        "- case studies;",
        "- policy templates;",
        "- research frontier;",
        "- community roadmap.",
        "glossary и practical assets",
    )

    for marker in forbidden_markers:
        assert marker not in text, marker


def test_book_plan_defines_three_case_spines() -> None:
    expected_by_file = {
        "docs/book/plan.md": (
            "Карта сквозных сценариев",
            "Триаж поддержки",
            "Внутренний ассистент знаний",
            "Координация инцидентов",
            "побочных эффектов",
            "качества контекста",
            "реагирования и управления",
        ),
        "docs/book/plan.en.md": (
            "Case-spine map",
            "Support triage",
            "Internal knowledge assistant",
            "Incident coordination",
            "side effects",
            "context quality",
            "response and governance",
        ),
        "docs/book/plan.zh.md": (
            "Case-spine map",
            "Support triage",
            "Internal knowledge assistant",
            "Incident coordination",
            "side effects",
            "context quality",
            "response and governance",
        ),
    }
    deprecated_markers = (
        "support triage for side effects",
        "support triage для side effects",
        "Support triage для side effects",
        "support triage 对应 side effects",
        "internal knowledge for context quality",
        "internal knowledge для context quality",
        "Internal knowledge assistant для context quality",
        "internal knowledge 对应 context quality",
        "incident coordination for response and governance",
        "incident coordination для response and governance",
        "Incident coordination для response and governance",
        "incident coordination 对应 response and governance",
    )

    for path, required_markers in expected_by_file.items():
        _assert_files_contain_all((path,), required_markers)
    for path in expected_by_file:
        text = _read(path)
        for marker in deprecated_markers:
            assert marker not in text, (path, marker)


def test_practical_routines_threads_three_canonical_cases() -> None:
    required_markers = (
        "Routine case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "approved write routine",
        "retrieval routine",
        "source attribution",
        "tenant boundary",
        "incident escalation routine",
        "notification handoff",
        "owner record",
    )
    checked_files = (
        "docs/book/part-i/practical-routines.md",
        "docs/book/part-i/practical-routines.en.md",
        "docs/book/part-i/practical-routines.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_practical_routines_zh_schema_term_is_localized() -> None:
    text = _read("docs/book/part-i/practical-routines.zh.md")

    expected_snippets = (
        "输出模式",
        'schema: "support_triage_decision_v1"',
    )
    forbidden_snippets = (
        "输出 Schema",
    )

    for expected_snippet in expected_snippets:
        assert expected_snippet in text, expected_snippet
    for forbidden_snippet in forbidden_snippets:
        assert forbidden_snippet not in text, forbidden_snippet


def test_practical_manager_handoffs_threads_three_canonical_cases() -> None:
    required_markers = (
        "Manager/handoff case-spine note",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "approved write routine",
        "ticket state",
        "audit story",
        "read-heavy capabilities",
        "source attribution",
        "tenant boundary",
        "escalation",
        "owner record",
        "accountable roles",
    )
    checked_files = (
        "docs/book/part-i/practical-manager-handoffs.md",
        "docs/book/part-i/practical-manager-handoffs.en.md",
        "docs/book/part-i/practical-manager-handoffs.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_practical_mcp_a2a_threads_three_canonical_cases() -> None:
    required_markers_by_file = {
        "docs/book/part-iv/practical-mcp-a2a.md": (
            "Сквозные сценарии MCP и A2A",
            "Разбор обращений поддержки",
            "Внутренний ассистент знаний",
            "Координация инцидентов",
            "службу поддержки",
            "CRM",
            "инструменты записи тикетов",
            "границей MCP",
            "ответственная роль",
            "сервер знаний",
            "адаптер поиска",
            "привязку к источникам",
            "границу арендатора",
            "передачи управления A2A",
            "записью владельца",
            "инструменты уведомлений",
            "ресурсы состояния инцидента",
            "аудитом MCP и политики",
        ),
        "docs/book/part-iv/practical-mcp-a2a.en.md": (
            "MCP/A2A case-spine note",
            "Support triage",
            "Internal knowledge assistant",
            "Incident coordination",
            "helpdesk",
            "CRM",
            "ticket-write tools",
            "MCP boundary",
            "responsible role",
            "knowledge server",
            "retrieval adapter",
            "source attribution",
            "tenant boundary",
            "A2A handoff",
            "owner record",
            "notification tools",
            "incident state resources",
            "MCP/policy audit",
        ),
        "docs/book/part-iv/practical-mcp-a2a.zh.md": (
            "MCP/A2A case-spine note",
            "Support triage",
            "Internal knowledge assistant",
            "Incident coordination",
            "helpdesk",
            "CRM",
            "ticket-write tools",
            "MCP boundary",
            "responsible role",
            "knowledge server",
            "retrieval adapter",
            "source attribution",
            "tenant boundary",
            "A2A handoff",
            "owner record",
            "notification tools",
            "incident state resources",
            "MCP/policy audit",
        ),
    }

    for path, required_markers in required_markers_by_file.items():
        _assert_files_contain_all((path,), required_markers)


def test_part_iv_index_surfaces_three_execution_case_routes() -> None:
    russian_markers = (
        "Маршруты канонических сценариев",
        "Разбор обращений поддержки",
        "Внутренний ассистент знаний",
        "Координация инцидентов",
        "слое исполнения",
        "границам инструментов",
        "возможность записи тикета",
        "шлюз подтверждения",
        "ключ идемпотентности",
        "восстановление после дубля",
        "адаптер поиска",
        "привязку к источникам",
        "границу арендатора",
        "MCP-контракт только для чтения",
        "инструмент эскалации",
        "побочные эффекты уведомлений",
        "обновления состояния инцидента",
        "границу отката",
    )
    translated_markers = (
        "Part IV canonical case routes",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "execution layer",
        "tool boundaries",
        "ticket-write capability",
        "approval gate",
        "idempotency key",
        "duplicate-ticket recovery",
        "retrieval adapter",
        "source attribution",
        "tenant boundary",
        "read-only MCP contract",
        "escalation tool",
        "notification side effects",
        "incident state updates",
        "rollback boundary",
    )
    translated_files = (
        "docs/book/part-iv/index.en.md",
        "docs/book/part-iv/index.zh.md",
    )

    _assert_files_contain_all(("docs/book/part-iv/index.md",), russian_markers)
    _assert_files_contain_all(translated_files, translated_markers)


def test_part_iii_index_surfaces_three_memory_case_routes() -> None:
    russian_markers = (
        "Маршруты канонических сценариев",
        "Разбор обращений поддержки",
        "Внутренний ассистент знаний",
        "Координация инцидентов",
        "слое памяти и поиска",
        "временное состояние тикета",
        "контекст дубля",
        "поиск по утвержденным инструкциям",
        "привязку к источникам",
        "окно свежести",
        "границу арендатора",
        "происхождение записей памяти",
        "шкалу времени инцидента",
        "сводки передачи владельцу",
        "статус эскалации",
        "уроки после инцидента",
    )
    translated_markers = (
        "Part III canonical case routes",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "memory/retrieval layer",
        "temporary ticket state",
        "duplicate-ticket context",
        "approved playbook retrieval",
        "source attribution",
        "freshness window",
        "tenant boundary",
        "memory provenance",
        "incident timeline",
        "owner handoff summaries",
        "escalation status",
        "post-incident lessons",
    )
    translated_files = (
        "docs/book/part-iii/index.en.md",
        "docs/book/part-iii/index.zh.md",
    )

    _assert_files_contain_all(("docs/book/part-iii/index.md",), russian_markers)
    _assert_files_contain_all(translated_files, translated_markers)


def test_part_ii_index_surfaces_three_security_case_routes() -> None:
    russian_markers = (
        "Маршруты канонических сценариев",
        "Разбор обращений поддержки",
        "Внутренний ассистент знаний",
        "Координация инцидентов",
        "периметре безопасности",
        "контрольных точек",
        "инструментальный шлюз",
        "остановку на подтверждение",
        "журнал аудита",
        "доступ с минимальными правами",
        "записи тикетов",
        "границу поиска",
        "контроль доступа",
        "сборку подсказки",
        "выходную фильтрацию",
        "защищенных чтений",
        "инструменты эскалации",
        "подтверждения уведомлений",
        "границу данных инцидента",
        "побочных эффектов во время реагирования",
    )
    translated_markers = (
        "Part II canonical case routes",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "security perimeter",
        "control points",
        "tool gateway",
        "approval stop",
        "audit trail",
        "least-privilege access",
        "ticket writes",
        "retrieval boundary",
        "access control",
        "prompt assembly",
        "egress filtering",
        "protected reads",
        "escalation tools",
        "notification approvals",
        "incident-data boundary",
        "side effects during response",
    )
    translated_files = (
        "docs/book/part-ii/index.en.md",
        "docs/book/part-ii/index.zh.md",
    )

    _assert_files_contain_all(("docs/book/part-ii/index.md",), russian_markers)
    _assert_files_contain_all(translated_files, translated_markers)


def test_part_i_index_surfaces_three_foundation_case_routes() -> None:
    russian_markers = (
        "Маршруты канонических сценариев",
        "Разбор обращений поддержки",
        "Внутренний ассистент знаний",
        "Координация инцидентов",
        "слое оснований",
        "канонических сценария",
        "архитектурная форма",
        "границу между рабочим процессом и агентом",
        "право на действие",
        "ограниченную автономность",
        "первый рискованный путь записи",
        "рабочий процесс только для чтения",
        "потребность в поиске",
        "дисциплину памяти",
        "ответы с опорой на источники",
        "цикл координации",
        "триггер эскалации",
        "границу передачи управления",
        "одноагентной схеме",
    )
    translated_markers = (
        "Part I canonical case routes",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "foundations layer",
        "canonical cases",
        "architecture shape",
        "workflow vs agent boundary",
        "right to act",
        "guarded autonomy",
        "first risky write path",
        "read-only workflow",
        "retrieval need",
        "memory discipline",
        "source-grounded answers",
        "coordination loop",
        "escalation trigger",
        "handoff boundary",
        "single-agent first decision",
    )
    translated_files = (
        "docs/book/part-i/index.en.md",
        "docs/book/part-i/index.zh.md",
    )

    _assert_files_contain_all(("docs/book/part-i/index.md",), russian_markers)
    _assert_files_contain_all(translated_files, translated_markers)


def test_part_v_index_surfaces_three_reliability_case_routes() -> None:
    russian_markers = (
        "Маршруты канонических сценариев",
        "Разбор обращений поддержки",
        "Внутренний ассистент знаний",
        "Координация инцидентов",
        "слое надежности и наблюдаемости",
        "маршрутов доказательств",
        "покрытие трассировкой",
        "записи тикетов",
        "регрессию дублей",
        "доказательства пути подтверждения",
        "качество поиска",
        "суждение об опоре на источники",
        "бюджет свежести",
        "доказательства происхождения памяти",
        "задержку эскалации",
        "доставку уведомлений",
        "владение реагированием",
        "послеинцидентное суждение о поэтапном выпуске",
    )
    translated_markers = (
        "Part V canonical case routes",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "reliability/observability layer",
        "evidence routes",
        "trace coverage",
        "ticket writes",
        "duplicate-ticket regression",
        "approval-path evidence",
        "retrieval quality",
        "source-grounding judgment",
        "freshness budget",
        "memory-provenance evidence",
        "escalation latency",
        "notification delivery",
        "response ownership",
        "post-incident rollout judgment",
    )
    translated_files = (
        "docs/book/part-v/index.en.md",
        "docs/book/part-v/index.zh.md",
    )

    _assert_files_contain_all(("docs/book/part-v/index.md",), russian_markers)
    _assert_files_contain_all(translated_files, translated_markers)


def test_part_vi_index_surfaces_three_ownership_case_routes() -> None:
    russian_markers = (
        "Маршруты канонических сценариев",
        "Разбор обращений поддержки",
        "Внутренний ассистент знаний",
        "Координация инцидентов",
        "операционной модели",
        "границ ответственности",
        "настройками записи тикетов",
        "режимом подтверждения",
        "путем восстановления после дубля",
        "владеет корпусом знаний",
        "проверкой доступа",
        "качеством поиска",
        "происхождением знаний",
        "правом эскалации",
        "политикой уведомлений",
        "ответственностью за реагирование",
        "действиями после инцидента",
    )
    translated_markers = (
        "Part VI canonical case routes",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "operating model",
        "ownership boundaries",
        "ticket-write defaults",
        "approval mode",
        "duplicate-ticket recovery path",
        "corpus ownership",
        "access review",
        "retrieval quality",
        "knowledge provenance",
        "escalation authority",
        "notification policy",
        "response ownership",
        "post-incident action items",
    )
    translated_files = (
        "docs/book/part-vi/index.en.md",
        "docs/book/part-vi/index.zh.md",
    )

    _assert_files_contain_all(("docs/book/part-vi/index.md",), russian_markers)
    _assert_files_contain_all(translated_files, translated_markers)


def test_part_vii_index_surfaces_three_runtime_case_routes() -> None:
    russian_markers = (
        "Маршруты канонических сценариев",
        "Разбор обращений поддержки",
        "Внутренний ассистент знаний",
        "Координация инцидентов",
        "эталонной реализации",
        "пути среды исполнения",
        "цикл запуска",
        "каталог возможностей",
        "паузу и возобновление после подтверждения",
        "проверочный список поэтапного выпуска",
        "записи тикетов",
        "сервис памяти и поиска",
        "политику возможностей чтения",
        "привязку к источникам",
        "изоляцию арендаторов",
        "возможность эскалации",
        "побочные эффекты уведомлений",
        "передачу состояния инцидента",
        "доказательства готовности к поэтапному выпуску",
    )
    translated_markers = (
        "Part VII canonical case routes",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "reference implementation",
        "runtime paths",
        "run loop",
        "capability catalog",
        "approval pause/resume",
        "rollout checklist",
        "ticket writes",
        "memory/retrieval service",
        "read capability policy",
        "source attribution",
        "tenant isolation",
        "escalation capability",
        "notification side effects",
        "incident state handoff",
        "rollout readiness evidence",
    )
    translated_files = (
        "docs/book/part-vii/index.en.md",
        "docs/book/part-vii/index.zh.md",
    )

    _assert_files_contain_all(("docs/book/part-vii/index.md",), russian_markers)
    _assert_files_contain_all(translated_files, translated_markers)


def test_book_index_surfaces_three_canonical_cases() -> None:
    russian_markers = (
        "Карта канонических сценариев",
        "Разбор обращений поддержки",
        "Внутренний ассистент знаний",
        "Координация инцидентов",
        "записывающих возможностей",
        "восстановления после дубля тикета",
        "границы арендатора",
        "привязка к источникам",
        "побочные эффекты уведомлений",
        "обучение после инцидента",
        "поверхностей управления",
        "Открыть практические кейсы",
    )
    english_markers = (
        "Canonical case map",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "write capabilities",
        "duplicate-ticket recovery",
        "tenant boundaries",
        "source grounding",
        "notification side effects",
        "post-incident learning",
        "control surfaces",
        "Open Practical Case Studies",
    )
    chinese_markers = (
        "Canonical case map",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "write capabilities",
        "duplicate-ticket recovery",
        "tenant boundaries",
        "source grounding",
        "notification side effects",
        "post-incident learning",
        "control surfaces",
        "打开实战案例",
    )

    _assert_files_contain_all(("docs/book/index.md",), russian_markers)
    _assert_files_contain_all(("docs/book/index.en.md",), english_markers)
    _assert_files_contain_all(("docs/book/index.zh.md",), chinese_markers)


def test_multilingual_book_index_canonical_case_map_is_localized() -> None:
    russian_text = _read("docs/book/index.md")
    chinese_text = _read("docs/book/index.zh.md")

    assert "Карта канонических сценариев" in russian_text
    assert "три канонических сценария делают книгу" in russian_text
    assert "записывающих возможностей" in russian_text
    assert "поиск, память, границы арендатора" in russian_text
    assert "картой разных поверхностей управления" in russian_text

    assert "规范案例地图" in chinese_text
    assert "规范案例（canonical cases）" in chinese_text
    assert "写入能力（write capabilities）" in chinese_text
    assert "检索（retrieval）" in chinese_text
    assert "控制表面（control surfaces）" in chinese_text

    forbidden_markers = (
        "Support triage остается",
        "для write capabilities",
        "что retrieval, memory",
        "проверяет traces",
        "три canonical cases",
        "Каноническая карта сценариев (Canonical case map)",
        "записывающих возможностей (write capabilities)",
        "поверхностей управления (control surfaces)",
        "Support triage 仍然是",
        "是 write capabilities",
        "检查 retrieval、memory",
        "检查 traces、SLO",
        "三个 canonical cases",
    )

    for marker in forbidden_markers[:8]:
        assert marker not in russian_text
    for marker in forbidden_markers[8:]:
        assert marker not in chinese_text


def test_multilingual_book_index_support_case_example_is_localized() -> None:
    russian_text = _read("docs/book/index.md")
    chinese_text = _read("docs/book/index.zh.md")

    assert "Сквозной сценарий поддержки" in russian_text
    assert "следить за сценарием разбора обращений поддержки" in russian_text
    assert "от поиска и выполнения инструментов" in russian_text
    assert "до восстановления после дубля тикета" in russian_text
    assert "эталонной среды исполнения" in russian_text
    assert "контроля несоответствия" in russian_text

    assert "贯穿的支持案例（support case throughline）" in chinese_text
    assert "支持分诊（support-triage）" in chinese_text
    assert "检索（retrieval）" in chinese_text
    assert "工具执行（tool execution）" in chinese_text
    assert "重复工单恢复（duplicate-ticket recovery）" in chinese_text
    assert "失配控制（misalignment controls）" in chinese_text

    forbidden_markers = (
        'example "Сквозной кейс поддержки"',
        "Сквозной кейс поддержки (support case throughline)",
        "следить за кейсом support-triage",
        "от retrieval и tool execution",
        "выполнения инструментов (tool execution)",
        "duplicate-ticket recovery, traces",
        "эталонного runtime",
        "misalignment controls, telemetry",
        'example "贯穿的支持案例"',
        "跟随 support-triage 案例",
        "重复工单恢复、traces",
        "失配控制、telemetry",
    )

    for marker in forbidden_markers[:8]:
        assert marker not in russian_text
    for marker in forbidden_markers[8:]:
        assert marker not in chinese_text


def test_multilingual_book_index_promise_bullets_are_localized() -> None:
    russian_text = _read("docs/book/index.md")
    chinese_text = _read("docs/book/index.zh.md")

    assert "# Книга" in russian_text
    assert "главная входная страница самой книги" in russian_text
    assert "самый короткий путь в основной текст" in russian_text
    assert "структуру и статус публикации" in russian_text
    assert "План книги" in russian_text
    assert "Что обещает эта книга" in russian_text
    assert "После чтения ты должен уметь:" in russian_text
    assert "главный тезис: агенту нужна платформа" in russian_text
    assert "вместо эффектного разового трюка появляется система" in russian_text
    assert "ограничивать, наблюдать, выпускать и улучшать без гадания" in russian_text
    assert "минимальный набор платформенных слоев" in russian_text
    assert "рискованным действиям" in russian_text
    assert "обычного рабочего процесса" in russian_text
    assert "один управляемый запуск" in russian_text
    assert "политику, исполнение, доказательства" in russian_text
    assert "ответственность оператора" in russian_text

    assert "# 书籍（book）" in chinese_text
    assert "主入口页（main entry page）" in chinese_text
    assert "最短路径（shortest path）" in chinese_text
    assert "正文（main text）" in chinese_text
    assert "结构与发布状态（structure and publication status）" in chinese_text
    assert "全书计划（Book Plan）" in chinese_text
    assert "这本书的承诺（book promise）" in chinese_text
    assert "读完后，你应该能够做到（learning outcomes）" in chinese_text
    assert "核心判断（main thesis）" in chinese_text
    assert "平台（platform）" in chinese_text
    assert "一次性炫技（one-off trick）" in chinese_text
    assert "约束（constrain）、观察（observe）、发布（ship）" in chinese_text
    assert "无需猜测地持续改进（improve without guessing）" in chinese_text
    assert "高风险动作（risky actions）" in chinese_text
    assert "最小平台层集合（minimum platform layers）" in chinese_text
    assert "工作流（workflow）" in chinese_text
    assert "运行（run）" in chinese_text
    assert "策略（policy）" in chinese_text
    assert "证据（evidence）" in chinese_text
    assert "操作员问责（operator accountability）" in chinese_text

    forbidden_markers = (
        "# Книга (book)",
        "главная входная страница (main entry page)",
        "самый короткий путь (shortest path)",
        "основной текст (main text)",
        "План книги (Book Plan)",
        "Что обещает эта книга (book promise)",
        "После чтения ты должен уметь (learning outcomes)",
        "главный тезис (main thesis)",
        "платформа (platform)",
        "разового трюка (one-off trick)",
        "ограничивать (constrain)",
        "улучшать без гадания (improve without guessing)",
        "рабочего процесса (workflow)",
        "управляемый запуск (run)",
        "политику (policy)",
        "доказательства (evidence)",
        "operator accountability",
        "# 书籍\n",
        "这是整本书的主入口页。",
        "最短路径进入正文",
        "结构和发布状态",
        "[全书计划](plan.zh.md)",
        "## 这本书的承诺\n",
        "读完后，你应该能够：",
        "普通工作流就够了",
        "核心判断：智能体需要平台",
        "一次性的炫技",
        "约束、观察、发布并持续改进",
        "不必靠猜",
        "最少需要哪些平台层",
        "策略、执行、证据、审批、发布",
        "记忆、评测、来源谱系、退役",
    )

    for marker in forbidden_markers[:17]:
        assert marker not in russian_text
    for marker in forbidden_markers[17:]:
        assert marker not in chinese_text


def test_multilingual_book_index_direct_entry_links_are_localized() -> None:
    russian_text = _read("docs/book/index.md")
    chinese_text = _read("docs/book/index.zh.md")

    assert "Рекомендуемый маршрут чтения" in russian_text
    assert "короткий полезный маршрут" in russian_text
    assert "Быстрый ориентир по стабильности" in russian_text
    assert "практических слоя" in russian_text
    assert "`Стабильное ядро`" in russian_text
    assert "`Быстро меняющийся слой`" in russian_text
    assert "исследовательские страницы приложений" in russian_text
    assert "читаешь книгу впервые" in russian_text
    assert "Прямые точки входа" in russian_text
    assert "[Начать с Части I]" in russian_text
    assert "[Открыть план книги]" in russian_text
    assert "[Перейти к сквозной цепочке доказательств]" in russian_text
    assert "[Перейти к жизненному циклу агентной системы]" in russian_text
    assert "[Читать книгу]" in russian_text
    assert "[Открыть план]" in russian_text

    assert "推荐阅读路径（recommended reading path）" in chinese_text
    assert "最短有效路径（shortest useful path）" in chinese_text
    assert "稳定性指南（stability guide）" in chinese_text
    assert "实践层（practical layers）" in chinese_text
    assert "`稳定核心`（stable core）" in chinese_text
    assert "`快速变化层`（fast-moving layer）" in chinese_text
    assert "研究型附录页面（research appendix pages）" in chinese_text
    assert "第一次阅读者（first-time reader）" in chinese_text
    assert "直接入口（direct entry points）" in chinese_text
    assert "[从第一部分开始（Part I）]" in chinese_text
    assert "[打开全书计划（Book Plan）]" in chinese_text
    assert "[跳到证据主线（Evidence Spine）]" in chinese_text
    assert "[跳到智能体系统生命周期（agent system lifecycle）]" in chinese_text
    assert "[开始读书（Read the book）]" in chinese_text
    assert "[查看计划（Open plan）]" in chinese_text

    forbidden_markers = (
        "Рекомендуемый маршрут чтения (recommended reading path)",
        "короткий полезный маршрут (shortest useful path)",
        "Быстрый ориентир по стабильности (stability guide)",
        "`Стабильное ядро` (stable core)",
        "`Быстро меняющийся слой` (fast-moving layer)",
        "исследовательские страницы приложений (research appendix pages)",
        "читаешь книгу впервые (first-time reader)",
        "Прямые точки входа (direct entry points)",
        "[Начать с Части I (Part I)]",
        "[Открыть план книги (Book Plan)]",
        "[Перейти к Сквозной цепочке доказательств (Evidence Spine)]",
        "[Перейти к жизненному циклу агентной системы (agent system lifecycle)]",
        "[Читать книгу (Read the book)]",
        "[Открыть план (Open plan)]",
        "## 推荐阅读路径\n",
        "最短但有效的路线",
        "## 稳定性捷径\n",
        "可以粗分为两层",
        "`稳定核心`：",
        "`快速变化层`：",
        "偏研究型的附录页面",
        "如果你是第一次阅读，",
        "## 直接入口\n",
        "[从第一部分开始](part-i/index.zh.md)",
        "[打开全书计划](plan.zh.md)",
        "[跳到 Evidence Spine]",
        "[跳到智能体系统生命周期](part-viii/index.zh.md)",
        "[开始读书](part-i/index.zh.md)",
        "[查看计划](plan.zh.md)",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_chinese_case_studies_support_review_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/case-studies.zh.md")
    expected_markers = (
        "追踪（trace）没有阻止重试",
        "评测（eval）阻挡这类回归",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "为什么 trace 没有阻止重试",
        "哪个 eval 阻挡这类回归",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chinese_case_studies_knowledge_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/case-studies.zh.md")
    expected_markers = (
        "查询（query）、检索范围、来源 ID（source IDs）",
        "答案锚定结论（grounding verdict）",
        "回归集（regression set）确认锚定（grounding）",
        "过期运行手册（runbook）回答，没有引用（citations）",
        "检索范围（retrieval scope）为什么扩大",
        "来源（source）被当作可信（trusted）",
        "低置信度停止（low-confidence stop）",
        "评测（eval）覆盖陈旧知识（stale knowledge）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "query、检索范围、source IDs",
        "答案 grounding verdict",
        "regression set 确认 grounding",
        "过期 runbook 回答，没有 citations",
        "retrieval scope 为什么扩大",
        "哪个 source 被当作 trusted",
        "low-confidence stop 应该在哪里触发",
        "哪个 eval 覆盖 stale knowledge",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chinese_case_studies_incident_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/case-studies.zh.md")
    expected_markers = (
        "统一追踪（trace）",
        "正确负责人（owner）",
        "脑裂（split-brain）",
        "告警来源（alert source）",
        "事件线程 ID（incident thread ID）",
        "交接负责人（handoff owner）",
        "运行手册步骤（runbook step）",
        "噪声告警（noisy alert）",
        "运行手册上下文（runbook context）",
        "演练运行（dry run）",
        "追踪链（trace chain）",
        "高风险步骤（high-risk steps）",
        "交接（handoff）",
        "幂等键（idempotency keys）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "统一 trace、正确 owner",
        "出现 split-brain",
        "alert source、incident thread ID",
        "handoff owner、runbook step",
        "noisy alert、重复通知",
        "错误 owner 交接",
        "缺失 runbook context",
        "dry run 显示单一 trace chain",
        "high-risk steps 需要人工审批",
        "noisy alert 触发两条并行 handoff",
        "split-brain 是从哪里进入流程",
        "每一步 owner 是谁",
        "哪些 idempotency keys 缺失",
        "哪个 dry run 应该捕捉到重复",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chinese_case_studies_intro_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/case-studies.zh.md")
    expected_markers = (
        "支持分流（support triage）案例",
        "信任边界（trust boundaries）",
        "工具网关（tool gateway）",
        "记忆/检索（memory/retrieval）",
        "幂等性（idempotency）",
        "追踪（traces）",
        "服务级目标（SLO）",
        "评测门禁（eval gates）",
        "归属（ownership）",
        "运行时（runtime）",
        "策略（policy）",
        "发布（rollout）",
        "智能体开发生命周期（ADLC）",
        "保障（assurance）",
        "来源证明（provenance）",
        "退役（retirement）",
        "失配控制（misalignment controls）",
        "遥测（telemetry）",
        "注册表（registry）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "support triage 案例",
        "穿过 trust boundaries",
        "tool gateway、memory/retrieval",
        "idempotency、traces",
        "eval gates、ownership",
        "runtime、policy、rollout",
        "ADLC、assurance、provenance",
        "retirement、misalignment controls",
        "telemetry 和 registry",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_case_studies_align_with_three_canonical_cases() -> None:
    required_markers = (
        "Canonical case alignment",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "write capability",
        "duplicate-ticket recovery",
        "access control",
        "knowledge provenance",
        "notification side effects",
        "response ownership",
        "post-incident learning",
    )
    checked_files = (
        "docs/appendix/case-studies.md",
        "docs/appendix/case-studies.en.md",
        "docs/appendix/case-studies.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)
    deprecated_markers = (
        "Support Triage Agent",
        "Internal Knowledge Agent",
        "Incident Coordination Agent",
    )
    for path in checked_files:
        text = _read(path)
        for marker in deprecated_markers:
            assert marker not in text, (path, marker)


def test_case_studies_define_operational_contract_fields_for_each_canonical_case() -> None:
    required_by_file = {
        "docs/appendix/case-studies.md": (
            "Критерий успеха",
            "Критерий провала",
            "Минимальная телеметрия",
            "Минимальный оценочный набор",
            "Модель подтверждения",
            "Политика памяти",
            "Профиль риска инструментов",
            "Экспозиция MCP/A2A",
            "Шлюз поэтапного выпуска",
            "Пример инцидента",
            "Вопросы разбора после инцидента",
            "Условие вывода из эксплуатации",
        ),
        "docs/appendix/case-studies.en.md": (
            "Success criteria",
            "Failure criteria",
            "Minimum telemetry",
            "Minimum eval dataset",
            "Approval model",
            "Memory policy",
            "Tool risk profile",
            "MCP/A2A exposure",
            "Rollout gate",
            "Example incident",
            "Postmortem questions",
            "Retirement condition",
        ),
        "docs/appendix/case-studies.zh.md": (
            "成功标准",
            "失败标准",
            "最低遥测",
            "最低评测集",
            "审批模型",
            "记忆策略",
            "工具风险画像",
            "MCP/A2A 暴露面",
            "发布门禁",
            "事故示例",
            "复盘问题",
            "退役条件",
        ),
    }

    for path, fields in required_by_file.items():
        text = _read(path)
        for field in fields:
            assert text.count(field) >= 3, (path, field)


def test_case_studies_map_canonical_cases_across_book_chapters() -> None:
    expected_by_file = {
        "docs/appendix/case-studies.md": (
            "Сквозной маршрут по главам",
            "глава 1",
            "глава 2",
            "главы 3-4",
            "главы 5-7",
            "главы 8-10",
            "глава 13",
            "глава 18",
            "главы 21-27",
            "выбор между рабочим процессом, одиночным агентным циклом и многоагентной схемой",
            "оценки, проверяющий и регрессионные шлюзы",
            "жизненный цикл, контур заверения, происхождение, вывод из эксплуатации, "
            "телеметрия и реестр",
        ),
        "docs/appendix/case-studies.en.md": (
            "Cross-chapter route",
            "Chapter 1",
            "Chapter 2",
            "Chapters 3-4",
            "Chapters 5-7",
            "Chapters 8-10",
            "Chapter 13",
            "Chapter 18",
            "Chapters 21-27",
            "choice between workflow, single-agent loop, and multi-agent shape",
            "evals, verifier, and regression gates",
            "lifecycle, assurance, provenance, retirement, telemetry, and registry",
        ),
        "docs/appendix/case-studies.zh.md": (
            "跨章节路线",
            "第 1 章",
            "第 2 章",
            "第 3-4 章",
            "第 5-7 章",
            "第 8-10 章",
            "第 13 章",
            "第 18 章",
            "第 21-27 章",
            "工作流、单智能体循环和多智能体形态之间的选择",
            "评测、验证器和回归门禁",
            "生命周期、保障、来源证明、退役、遥测和注册表",
        ),
    }

    for path, expected_markers in expected_by_file.items():
        _assert_files_contain_all((path,), expected_markers)


def test_multilingual_case_studies_alignment_note_is_localized() -> None:
    russian_path = "docs/appendix/case-studies.md"
    russian_text = _read(russian_path)
    chinese_text = _read("docs/appendix/case-studies.zh.md")

    for marker in (
        "Canonical case alignment",
        "canonical cases",
        "write capability",
        "access control",
        "notification side effects",
    ):
        _assert_file_contains(russian_path, marker)

    assert "规范案例对齐" in chinese_text
    assert "规范案例（canonical cases）" in chinese_text
    assert "写入能力（write capability）" in chinese_text
    assert "访问控制（access control）" in chinese_text
    assert "服务级目标（SLO）" in chinese_text
    assert "通知副作用（notification side effects）" in chinese_text

    forbidden_markers = (
        "трем canonical cases",
        "про write capability",
        "про retrieval",
        "про traces",
        "三个 canonical cases",
        "承载 write capability",
        "承载 retrieval",
        "承载 traces",
        "追踪（traces）、SLO、升级",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_readmes_surface_three_canonical_cases() -> None:
    english_markers = (
        "canonical cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "write capabilities",
        "approvals",
        "knowledge provenance",
        "notification side effects",
        "response ownership",
        "post-incident learning",
    )
    russian_markers = (
        "Три канонических сценария для проверки покрытия",
        "Триаж поддержки",
        "внутренний ассистент знаний",
        "координация инцидентов",
        "записывающие возможности",
        "подтверждения",
        "происхождение знаний",
        "побочные эффекты уведомлений",
        "владельца реагирования",
        "обучение после инцидента",
    )
    chinese_markers = (
        "规范案例",
        "支持分诊",
        "内部知识助手",
        "事件协调",
        "写入能力",
        "审批",
        "知识来源",
        "通知副作用",
        "响应归属",
        "事后学习",
    )

    _assert_files_contain_all(("README.md",), english_markers)
    _assert_files_contain_all(("README.ru.md",), russian_markers)
    _assert_files_contain_all(("README.zh.md",), chinese_markers)


def test_multilingual_readme_canonical_case_intro_is_localized() -> None:
    russian_text = _read("README.ru.md")
    chinese_text = _read("README.zh.md")

    assert "Промышленная эксплуатация вместо театра агентов" in russian_text
    assert "Один сквозной сценарий по всему стеку" in russian_text
    assert "ветка дубля тикета связывают книгу" in russian_text
    assert "эталонные схемы и `agent_runtime_ref`" in russian_text
    assert "до телеметрии, оценок, поэтапного выпуска" in russian_text
    assert "Три канонических сценария для проверки покрытия" in russian_text
    assert "Триаж поддержки покрывает записывающие возможности" in russian_text
    assert "происхождение знаний" in russian_text
    assert "побочные эффекты уведомлений" in russian_text

    assert "生产现实（production reality）" in chinese_text
    assert "智能体表演（agent theater）" in chinese_text
    assert "贯穿全栈的案例线（full-stack case）" in chinese_text
    assert "重复工单线索（support-triage / duplicate-ticket thread）" in chinese_text
    assert "参考模式（reference schemas）" in chinese_text
    assert "遥测（telemetry）" in chinese_text
    assert "评测（evals）" in chinese_text
    assert "发布（rollout）" in chinese_text
    assert "生命周期（lifecycle）" in chinese_text
    assert "注册表控制（registry control）" in chinese_text
    assert "覆盖检查（coverage check）" in chinese_text
    assert "支持分诊（Support triage）" in chinese_text
    assert "写入能力（write capabilities）" in chinese_text
    assert "知识来源（knowledge provenance）" in chinese_text
    assert "通知副作用（notification side effects）" in chinese_text

    russian_forbidden = (
        "production reality",
        "agent theater",
        "full-stack case",
        "support-triage / duplicate-ticket thread",
        "reference schemas",
        "evals",
        "rollout",
        "registry control",
        "coverage check",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "write capabilities",
        "knowledge provenance",
        "notification side effects",
    )
    chinese_forbidden = (
        "一条贯穿全栈的案例线。",
        "support-triage / duplicate-ticket thread 把",
        "参考 Schema 和 `agent_runtime_ref`",
        "三个规范案例（canonical cases）用来检查覆盖面",
        "三个 canonical cases",
        "Support triage 覆盖 write capabilities",
        "Internal knowledge assistant 覆盖 retrieval",
        "Incident coordination 覆盖 traces",
    )

    for marker in russian_forbidden:
        assert marker not in russian_text
    for marker in chinese_forbidden:
        assert marker not in chinese_text


def test_multilingual_readme_purpose_prompting_term_is_localized() -> None:
    russian_text = _read("README.ru.md")
    chinese_text = _read("README.zh.md")

    assert "# Книга об архитектуре агентных систем" in russian_text
    assert "[Английская версия](README.md)" in russian_text
    assert "[Китайская версия](README.zh.md)" in russian_text
    assert "[Руководство для вкладов](CONTRIBUTING.md)" in russian_text
    assert "[Кодекс поведения](CODE_OF_CONDUCT.md)" in russian_text
    assert "## Зачем существует этот репозиторий" in russian_text
    assert "## Что есть в этом репозитории" in russian_text
    assert "## Почему это стоит читать" in russian_text
    assert "## С чего начать" in russian_text
    assert "готовой к промышленной эксплуатации архитектуре ИИ-агентов" in russian_text
    assert "контролируемые и безопасные агентные системы" in russian_text
    assert "реальными пользователями" in russian_text
    assert "реальными инструментами" in russian_text
    assert "реальной эксплуатацией" in russian_text
    assert "быстрой демонстрации" in russian_text
    assert "удачно сформулированный запрос" in russian_text
    assert "вызовы инструментов" in russian_text
    assert "явные границы доверия" in russian_text
    assert "слой политик и подтверждений" in russian_text
    assert "дисциплина памяти" in russian_text
    assert "наблюдаемость и оценки" in russian_text
    assert "контроль поэтапного выпуска" in russian_text
    assert "управление жизненным циклом" in russian_text
    assert "智能体架构之书（Agent Architecture Book）" in chinese_text
    assert "英文版（English version）" in chinese_text
    assert "俄文版（Russian version）" in chinese_text
    assert "贡献指南（Contributing guide）" in chinese_text
    assert "行为准则（Code of Conduct）" in chinese_text
    assert "为什么这个仓库存在（why this repository exists）" in chinese_text
    assert "这个仓库包含什么（what is in this repository）" in chinese_text
    assert "为什么值得读（why read this）" in chinese_text
    assert "从这里开始（Start Here）" in chinese_text
    assert "生产就绪架构（production-ready architecture）" in chinese_text
    assert "真实用户（real users）" in chinese_text
    assert "真实工具（real tools）" in chinese_text
    assert "真实运维（real operations）" in chinese_text
    assert "可控且安全的智能体系统（controlled and safe agent systems）" in chinese_text
    assert "快速演示（quick demo）" in chinese_text
    assert "提示词技巧（prompting）" in chinese_text
    assert "工具调用（tool calls）" in chinese_text
    assert "信任边界（trust boundaries）" in chinese_text
    assert "策略执行（policy enforcement）" in chinese_text
    assert "记忆治理与约束（memory governance）" in chinese_text
    assert "可观测性（observability）与评测体系（evals）" in chinese_text
    assert "发布控制（rollout control）" in chinese_text
    assert "生命周期治理（lifecycle governance）" in chinese_text

    russian_forbidden = (
        "Agent Architecture Book",
        "English version",
        "Chinese version",
        "Contributing guide",
        "Code of Conduct",
        "why this repository exists",
        "what is in this repository",
        "why read this",
        "Start Here",
        "production-ready architecture",
        "controlled and safe agent systems",
        "real users",
        "real tools",
        "real operations",
        "quick demo",
        "prompting",
        "tool calls",
        "trust boundaries",
        "policy layer",
        "memory discipline",
        "observability",
        "lifecycle governance",
        "# Agent Architecture Book\n",
        "готовой к production архитектуре AI-агентов",
        "[English version](README.md)",
        "[中文版](README.zh.md)",
        "[Contributing guide](CONTRIBUTING.md)",
        "[Code of Conduct](CODE_OF_CONDUCT.md)",
        "быстрому демо. Реальным системам",
        "удачный prompting",
        "контроль раскатки",
    )
    chinese_forbidden = (
        "可用于生产环境的 AI 智能体架构",
        "[Русская версия](README.ru.md)",
        "## 为什么这个仓库存在\n",
        "## 这个仓库包含什么\n",
        "## 为什么值得读\n",
        "## 从这里开始\n",
        "真实用户、真实工具和真实运维条件",
        "可控、安全、稳定运行的智能体系统",
        "快速做出演示",
        "提示词技巧和工具调用",
        "工具调用。它们还需要",
        "明确的信任边界\n",
        "策略执行与审批机制",
        "记忆治理与约束\n",
        "可观测性与评测体系\n",
        "发布控制与生命周期管理",
    )

    for marker in russian_forbidden:
        assert marker not in russian_text
    for marker in chinese_forbidden:
        assert marker not in chinese_text


def test_multilingual_readme_vendor_neutral_term_is_localized() -> None:
    russian_text = _read("README.ru.md")
    chinese_text = _read("README.zh.md")

    assert "Нейтральная к поставщикам архитектура" in russian_text
    assert "любой конкретный фреймворк" in russian_text
    assert "поставщика моделей" in russian_text
    assert "厂商中立架构（vendor-neutral architecture）" in chinese_text
    assert "框架（framework）" in chinese_text
    assert "模型厂商（model provider）" in chinese_text

    russian_forbidden = (
        "vendor-neutral architecture",
        "framework)",
        "model provider",
        "Vendor-neutral архитектура",
        "провайдера моделей",
    )
    chinese_forbidden = (
        "面向原则，而非单一厂商",
        "具体框架和模型厂商",
    )

    for marker in russian_forbidden:
        assert marker not in russian_text
    for marker in chinese_forbidden:
        assert marker not in chinese_text


def test_readmes_surface_safe_agent_schema_spine() -> None:
    english_markers = (
        "Safe-agent schema spine",
        "trace schema",
        "eval schema",
        "memory/retrieval schema",
        "MCP threat model",
        "A2A handoff trust contract",
        "verifier verdict record",
        "governance action record",
        "memory poisoning review fields",
        "unified agent threat evidence",
    )
    russian_markers = (
        "Сквозная цепочка схем безопасного агента",
        "схема трасс",
        "схема оценок",
        "схема памяти/поиска",
        "модель угроз MCP",
        "контракт доверия передачи A2A",
        "запись вердикта проверяющего",
        "запись управленческого действия",
        "поля проверки отравления памяти",
        "единые доказательства угроз агенту",
    )
    chinese_markers = (
        "Safe-agent schema spine",
        "trace schema",
        "eval schema",
        "memory/retrieval schema",
        "MCP threat model",
        "A2A handoff trust contract",
        "verifier verdict record",
        "governance action record",
        "memory poisoning review fields",
        "unified agent threat evidence",
    )

    _assert_files_contain_all(("README.md",), english_markers)
    _assert_files_contain_all(("README.ru.md",), russian_markers)
    _assert_files_contain_all(("README.zh.md",), chinese_markers)


def test_multilingual_readme_safe_agent_schema_spine_is_localized() -> None:
    russian_text = _read("README.ru.md")
    chinese_text = _read("README.zh.md")

    assert "Сквозная цепочка схем безопасного агента" in russian_text
    assert "схема трасс" in russian_text
    assert "схема оценок" in russian_text
    assert "модель угроз MCP" in russian_text
    assert "единые доказательства угроз агенту" in russian_text

    assert "安全智能体模式主线（Safe-agent schema spine）" in chinese_text
    assert "追踪模式（trace schema）" in chinese_text
    assert "评测模式（eval schema）" in chinese_text
    assert "MCP 威胁模型（MCP threat model）" in chinese_text
    assert "统一智能体威胁证据（unified agent threat evidence）" in chinese_text

    russian_forbidden = (
        "Safe-agent schema spine",
        "trace schema",
        "eval schema",
        "MCP threat model",
        "unified agent threat evidence",
        "- Safe-agent schema spine:",
        "trace schema](docs/appendix/trace-schema.md), [eval schema",
        "связывают MCP threat model",
        "verifier verdict record, governance action record",
    )
    chinese_forbidden = (
        "- Safe-agent schema spine：",
        "连接 MCP threat model",
        "verifier verdict record、governance action record",
    )

    for marker in russian_forbidden:
        assert marker not in russian_text
    for marker in chinese_forbidden:
        assert marker not in chinese_text


def test_multilingual_readme_runtime_artifact_bullets_are_localized() -> None:
    russian_text = _read("README.ru.md")
    chinese_text = _read("README.zh.md")

    assert "Локальная разработка" in russian_text
    assert "Проверки" in russian_text
    assert "Эталонный пакет" in russian_text
    assert "компактная кодовая опора" in russian_text
    assert "эталонная среда исполнения и слой политик" in russian_text
    assert "Эталонная среда исполнения:" in russian_text
    assert "команд CLI" in russian_text
    assert "обзор конфигурации" in russian_text
    assert "каталог возможностей и утвержденный инвентарь" in russian_text
    assert "путь памяти, телеметрия, подтверждения" in russian_text
    assert "проверки поэтапного выпуска" in russian_text
    assert "артефакты жизненного цикла для записей изменений" in russian_text
    assert "видимый контракт профиля песочницы" in russian_text
    assert "доказательства проверки песочницы" in russian_text
    assert "YAML-конфиги для операционного скелета" in russian_text
    assert "Быстрые примеры:" in russian_text
    assert "Каноническое описание пакета" in russian_text
    assert "Опциональные исследовательские зависимости" in russian_text
    assert "ноутбуки или инструменты анализа данных" in russian_text
    assert "исследовательскую группу" in russian_text

    assert "本地开发（local development）" in chinese_text
    assert "检查（checks）" in chinese_text
    assert "参考包（reference package）" in chinese_text
    assert "紧凑的代码支撑（compact code support）" in chinese_text
    assert "参考运行时（runtime）" in chinese_text
    assert "策略层（policy layer）" in chinese_text
    assert "参考运行时包（reference package）" in chinese_text
    assert "CLI 命令列表（CLI commands）" in chinese_text
    assert "配置概览（config overview）" in chinese_text
    assert "参考运行时包（runtime reference package）" in chinese_text
    assert "能力目录（capability catalog）" in chinese_text
    assert "已批准清单（approved inventory）" in chinese_text
    assert "记忆路径（memory path）" in chinese_text
    assert "遥测（telemetry）" in chinese_text
    assert "审批（approvals）" in chinese_text
    assert "发布检查（rollout checks）" in chinese_text
    assert "生命周期工件（lifecycle artifacts）" in chinese_text
    assert "变更记录（change records）" in chinese_text
    assert "工件包（artifact bundles）" in chinese_text
    assert "退役计划（retirement plans）" in chinese_text
    assert "沙箱配置契约（sandbox profile contract）" in chinese_text
    assert "沙箱审查证据（sandbox review evidence）" in chinese_text
    assert "生命周期检查（lifecycle inspection）" in chinese_text
    assert "运行骨架（operational skeleton）" in chinese_text
    assert "YAML 配置（YAML configs）" in chinese_text
    assert "概念性说明（conceptual prose）" in chinese_text
    assert "可执行的参考资产（reference assets）" in chinese_text
    assert "快速示例（quick examples）：" in chinese_text
    assert "规范包说明（canonical package description）" in chinese_text
    assert "可选研究依赖（optional research dependencies）" in chinese_text
    assert "笔记本（notebooks）" in chinese_text
    assert "数据分析工具（data analysis tools）" in chinese_text
    assert "研究组（research group）" in chinese_text

    russian_forbidden = (
        "local development",
        "reference package",
        "compact code support",
        "runtime)",
        "policy layer",
        "runtime reference package",
        "capability catalog",
        "approved inventory",
        "memory path",
        "telemetry)",
        "approvals)",
        "rollout checks",
        "lifecycle artifacts",
        "change records",
        "artifact bundles",
        "retirement plans",
        "sandbox profile contract",
        "sandbox review evidence",
        "lifecycle inspection",
        "YAML configs",
        "operational skeleton",
        "quick examples",
        "canonical package description",
        "optional research dependencies",
        "notebooks",
        "data analysis tools",
        "research group",
        "эталонный runtime",
        "Эталонный runtime",
        "эталонная среда исполнения (runtime) и слой политик\n",
        "approvals и rollout checks",
        "lifecycle-артефакты для change records",
        "sandbox profile contract и sandbox review evidence",
        "для operational skeleton",
    )
    chinese_forbidden = (
        "参考运行时（runtime）与策略层\n",
        "## 本地开发\n",
        "## 检查\n",
        "## 参考包\n",
        "- [Эталонный пакет]",
        "- 参考包：[docs/appendix/reference-package",
        "完整 CLI 列表",
        "紧凑的参考运行时，包含",
        "обзор конфигов",
        "配置概览可见",
        "каталог возможностей и approved inventory",
        "каталог возможностей и утвержденный инвентарь",
        "能力目录与已批准清单",
        "память, телеметрия, подтверждения",
        "记忆路径、遥测、审批",
        "approvals и rollout checks",
        "lifecycle-артефакты для change records",
        "артефакты жизненного цикла для записей изменений",
        "生命周期工件，用于变更记录",
        "sandbox profile contract и sandbox review evidence",
        "контракт профиля песочницы и доказательства ревью песочницы",
        "沙箱配置契约与沙箱审查证据",
        "для operational skeleton",
        "YAML-конфиги для операционного скелета",
        "Быстрые примеры:",
        "Каноническое описание пакета, полный список",
        "Опциональные исследовательские зависимости\n",
        "ноутбуки или инструменты для анализа данных",
        "В группу `research`",
        "рабочие эталонные артефакты (assets)",
        "lifecycle inspection 中可见",
        "用于 operational skeleton",
        "YAML 配置\n",
        "快速示例：",
        "规范说明、完整 CLI 命令列表",
        "可选研究依赖\n",
        "notebook 或数据分析工具",
        "`research` 组已包含",
        "参考资产（assets）",
        "不只是概念说明",
    )

    for marker in russian_forbidden:
        assert marker not in russian_text
    for marker in chinese_forbidden:
        assert marker not in chinese_text


def test_multilingual_readme_publishing_terms_are_localized() -> None:
    russian_text = _read("README.ru.md")
    chinese_text = _read("README.zh.md")

    assert "Публикация сайта" in russian_text
    assert "рабочий процесс GitHub Actions" in russian_text
    assert "сборка через `uv`" in russian_text
    assert "строгая проверка `mkdocs build --strict`" in russian_text
    assert "публикация в Pages из ветки `docs-prod`" in russian_text
    assert "локальные проверки" in russian_text
    assert "учетные данные на запись" in russian_text
    assert "командами прямого продвижения" in russian_text
    assert "ветка-триггер для GitHub Pages" in russian_text

    assert "发布（publishing）" in chinese_text
    assert "GitHub Actions 工作流（GitHub Actions workflow）" in chinese_text
    assert "构建（build）" in chinese_text
    assert "严格检查（strict check）" in chinese_text
    assert "部署（deploy）" in chinese_text
    assert "发布分支（publishing branch）" in chinese_text
    assert "本地检查（local checks）" in chinese_text
    assert "写入凭据（write credentials）" in chinese_text
    assert "fast-forward push 命令（fast-forward push commands）" in chinese_text
    assert "触发分支（trigger branch）" in chinese_text

    russian_forbidden = (
        "publishing)",
        "GitHub Actions workflow",
        "build)",
        "strict check",
        "deploy)",
        "publishing branch",
        "local checks",
        "write credentials",
        "fast-forward push commands",
        "trigger branch",
        "## Публикация\n",
        "деплой в Pages из ветки",
        "Когда write credentials настроены",
    )
    chinese_forbidden = (
        "## 发布\n",
        "GitHub Actions 工作流：",
        "使用 `uv` 构建",
        "严格执行 `mkdocs build --strict`",
        "分支部署到 Pages",
        "运行本地检查，并确认",
        "配置好写入凭据后",
        "触发分支。",
    )

    for marker in russian_forbidden:
        assert marker not in russian_text
    for marker in chinese_forbidden:
        assert marker not in chinese_text


def test_multilingual_readme_pages_setup_terms_are_localized() -> None:
    russian_text = _read("README.ru.md")
    chinese_text = _read("README.zh.md")

    assert "Первый запуск GitHub Pages" in russian_text
    assert "важное ограничение" in russian_text
    assert "создать сайт Pages" in russian_text
    assert "корректных варианта" in russian_text
    assert "вручную включить Pages" in russian_text
    assert "рабочий процесс сможет включить Pages" in russian_text
    assert "ограничения по веткам" in russian_text
    assert "разрешить публикацию из `docs-prod`" in russian_text
    assert "отдельный токен" in russian_text
    assert "персонального токена доступа" in russian_text
    assert "приложения GitHub" in russian_text
    assert "право записи Pages" in russian_text

    assert "GitHub Pages 首次设置（first GitHub Pages setup）" in chinese_text
    assert "重要限制（important limitation）" in chinese_text
    assert "Pages 站点（Pages site）" in chinese_text
    assert "正确选项（correct options）" in chinese_text
    assert "手动启用 Pages（manually enable Pages）" in chinese_text
    assert "工作流（workflow）" in chinese_text
    assert "分支限制（branch restrictions）" in chinese_text
    assert "部署（deployment）" in chinese_text
    assert "单独的 token（separate token）" in chinese_text
    assert "个人访问令牌（Personal Access Token）" in chinese_text
    assert "GitHub 应用（GitHub App）" in chinese_text
    assert "Pages 写权限（Pages write permission）" in chinese_text

    russian_forbidden = (
        "first GitHub Pages setup",
        "important limitation",
        "Pages site",
        "correct options",
        "manually enable Pages",
        "workflow)",
        "branch restrictions",
        "deployment)",
        "separate token",
        "Personal Access Token",
        "GitHub App)",
        "Pages write permission",
        "явно разрешить деплой из",
        "для Personal Access Token:",
        "для GitHub App:",
        "Pages write permission\n",
    )
    chinese_forbidden = (
        "## GitHub Pages 首次设置\n",
        "有一个重要限制：",
        "完成站点初始化",
        "有两种正确处理方式：",
        "手动启用一次",
        "让 workflow 自动",
        "部署分支限制",
        "来自 `docs-prod` 的部署。",
        "必须是真实 token",
        "Personal Access Token:",
        "GitHub App:",
        "Pages 写权限\n",
    )

    for marker in russian_forbidden:
        assert marker not in russian_text
    for marker in chinese_forbidden:
        assert marker not in chinese_text


def test_multilingual_readme_branch_stack_terms_are_localized() -> None:
    russian_text = _read("README.ru.md")
    chinese_text = _read("README.zh.md")

    assert "Модель веток" in russian_text
    assert "основная ветка разработки и источник правды" in russian_text
    assert "ветка публикации для GitHub Pages" in russian_text
    assert "Технический стек" in russian_text
    assert "для окружения и зависимостей" in russian_text
    assert "для статического анализа" in russian_text
    assert "для проверки типов" in russian_text
    assert "для визуальных материалов" in russian_text
    assert "Лицензия" in russian_text
    assert "опубликован под лицензией [CC BY-SA" in russian_text

    assert "分支模型（branch model）" in chinese_text
    assert "开发分支（development branch）" in chinese_text
    assert "事实来源（source of truth）" in chinese_text
    assert "发布分支（publishing branch）" in chinese_text
    assert "GitHub Pages 站点（GitHub Pages site）" in chinese_text
    assert "技术栈（stack）" in chinese_text
    assert "环境（environment）" in chinese_text
    assert "依赖管理（dependencies）" in chinese_text
    assert "代码检查（linting）" in chinese_text
    assert "类型检查（type checking）" in chinese_text
    assert "可视化内容（visualizations）" in chinese_text
    assert "许可证（license）" in chinese_text
    assert "授权发布（licensed under）" in chinese_text

    russian_forbidden = (
        "branch model",
        "development branch",
        "source of truth",
        "publishing branch",
        "GitHub Pages site",
        "Стек (stack)",
        "environment",
        "dependencies",
        "linting",
        "type checking",
        "visualizations",
        "license)",
        "licensed under",
        "для линтинга",
        "для визуализаций",
    )
    chinese_forbidden = (
        "## 分支模型\n",
        "事实来源开发分支",
        "使用的发布分支",
        "承载 GitHub Pages 的发布分支",
        "## 技术栈\n",
        "用于环境和依赖管理",
        "用于 lint",
        "用于类型检查\n",
        "用于可视化内容",
        "## 许可证\n",
        "基于 [CC BY-SA 4.0](LICENSE) 发布",
    )

    for marker in russian_forbidden:
        assert marker not in russian_text
    for marker in chinese_forbidden:
        assert marker not in chinese_text


def test_start_here_surfaces_three_canonical_case_routes() -> None:
    localized_markers = (
        "Канонические маршруты сценариев",
        "Триаж обращений поддержки",
        "Внутренний ассистент знаний",
        "Координация инцидентов",
        "записывающие возможности",
        "согласования",
        "восстановление после дубля тикета",
        "происхождение знаний",
        "побочные эффекты уведомлений",
        "владение ответом",
        "обучение после инцидента",
    )
    english_markers = (
        "Canonical case routes",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "write capabilities",
        "approvals",
        "duplicate-ticket recovery",
        "knowledge provenance",
        "notification side effects",
        "response ownership",
        "post-incident learning",
    )

    _assert_files_contain_all(("docs/start-here.md",), localized_markers)
    _assert_files_contain_all(
        ("docs/start-here.en.md", "docs/start-here.zh.md"), english_markers
    )


def test_multilingual_start_here_intro_terms_are_localized() -> None:
    russian_text = _read("docs/start-here.md")
    chinese_text = _read("docs/start-here.zh.md")

    assert "# С чего начать" in russian_text
    assert "впечатляющий демо-агент или система" in russian_text
    assert "производственную реальность" in russian_text
    assert "читать как один аргумент" in russian_text
    assert "прототипов, перегруженных промптами" in russian_text
    assert "управляемым системам с границами доверия" in russian_text
    assert "слоем политик, согласованиями, наблюдаемостью" in russian_text
    assert "дисциплиной жизненного цикла" in russian_text
    assert "производственную агентную систему нельзя строить" in russian_text
    assert "безопасно улучшать" in russian_text
    assert "маршрут чтения" in russian_text
    assert "Если читать только одно" in russian_text
    assert "самый короткий вход" in russian_text
    assert "Маршрут на 30 минут" in russian_text
    assert "Что это за книга" in russian_text
    assert "пройди этот путь" in russian_text
    assert "рабочая рамка" in russian_text
    assert "программному каркасу" in russian_text
    assert "каталог AI-возможностей" in russian_text
    assert "пути записи" in russian_text
    assert "человеческие согласования" in russian_text
    assert "границы доступа, телеметрия, оценки" in russian_text
    assert "эксплуатационная ответственность" in russian_text
    assert "реальные границы доверия" in russian_text
    assert "безопасное исполнение инструментов" in russian_text
    assert "“умной модели” мало" in russian_text
    assert "трасс, SLO и оценок" in russian_text
    assert "первой серьезной раскатки" in russian_text

    assert "# 从这里开始（Start Here）" in chinese_text
    assert "惊艳的演示智能体（impressive demo agent）" in chinese_text
    assert "生产现实（production reality）" in chinese_text
    assert "完整论证（single argument）" in chinese_text
    assert "提示堆出来的原型（prompt-heavy prototypes）" in chinese_text
    assert "受治理系统（governed systems）" in chinese_text
    assert "信任边界（trust boundaries）" in chinese_text
    assert "策略层（policy layer）" in chinese_text
    assert "生命周期纪律（lifecycle discipline）" in chinese_text
    assert "生产级智能体系统（production agent system）" in chinese_text
    assert "安全改进的系统（safely improve）" in chinese_text
    assert "阅读路线（reading route）" in chinese_text
    assert "如果你只读一章（read only one）" in chinese_text
    assert "最短入口（shortest entry point）" in chinese_text
    assert "30 分钟路线（30-minute route）" in chinese_text
    assert "这是什么样的书（what kind of book）" in chinese_text
    assert "这条路径（path）" in chinese_text
    assert "工作框架（working frame）" in chinese_text
    assert "框架（framework）的指南" in chinese_text
    assert "AI 功能目录（AI feature catalog）" in chinese_text
    assert "写入路径（write paths）" in chinese_text
    assert "人工审批（human approvals）" in chinese_text
    assert "访问边界（access boundaries）" in chinese_text
    assert "遥测（telemetry）、评测（evals）" in chinese_text
    assert "运维负责人机制（operational ownership）" in chinese_text
    assert "真实信任边界（trust boundaries）" in chinese_text
    assert "安全工具执行（safe tool execution）" in chinese_text
    assert "“聪明模型”（smart model）" in chinese_text
    assert "追踪（traces）、SLO 和评测（evals）" in chinese_text
    assert "认真发布（first serious rollout）之前" in chinese_text

    forbidden_markers = (
        "реальность production",
        "от prompt-heavy прототипов",
        "границами доверия, policy layer",
        "наблюдаемостью (observability), оценками (evals) и жизненным циклом.",
        "дисциплина вокруг trust boundaries",
        "production agent system нельзя",
        "фреймворку (framework)",
        "человеческие подтверждения, границы доступа",
        "набор tools",
        "есть write paths",
        "реальные trust boundaries",
        "без traces, SLO и evals",
        "серьезного rollout",
        "серьезной раскатки (rollout)",
        "生产现实的系统",
        "看起来厉害的演示智能体",
        "读成一个完整论证：",
        "提示堆出来的原型，",
        "生命周期纪律的受治理系统。",
        "安全改进的系统。",
        "阅读路线。",
        "## 如果你只读一章\n",
        "# 从这里开始\n",
        "最短时间进入",
        "## 这是什么样的书\n",
        "## 30 分钟路线\n",
        "先读这条路径：",
        "形成一个工作框架",
        "信任边界、策略层、审批",
        "生产级智能体系统不能",
        "某个框架的指南，也不是 AI 功能目录",
        "人工审批、访问边界",
        "访问边界、遥测、评测",
        "明确的运维负责人机制。",
        "几个工具”，",
        "有写入路径、人工审批",
        "真实信任边界在哪里",
        "安全工具执行应该",
        "单靠“聪明模型”不够",
        "没有追踪、SLO 和评测",
        "认真发布之前",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_multilingual_start_here_canonical_routes_note_is_localized() -> None:
    russian_text = _read("docs/start-here.md")
    chinese_text = _read("docs/start-here.zh.md")

    assert "Канонические маршруты сценариев" in russian_text
    assert "три канонических сценария" in russian_text
    assert "записывающие возможности" in russian_text
    assert "поиск, память, свежесть" in russian_text
    assert "трассы, эскалацию" in russian_text

    assert "规范案例路线" in chinese_text
    assert "规范案例（canonical cases）" in chinese_text
    assert "写入能力（write capabilities）" in chinese_text
    assert "检索（retrieval）" in chinese_text
    assert "追踪（traces）" in chinese_text

    forbidden_markers = (
        "три canonical cases",
        "ведет через write capabilities",
        "подсвечивает retrieval, memory",
        "проверяет traces, escalation",
        "三个 canonical cases",
        "承载 write capabilities",
        "突出 retrieval、memory",
        "检查 traces、escalation",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_multilingual_start_here_support_case_example_is_localized() -> None:
    russian_text = _read("docs/start-here.md")
    chinese_text = _read("docs/start-here.zh.md")

    assert "Если хочешь идти по сквозному кейсу" in russian_text
    assert "историей триажа поддержки" in russian_text
    assert "начинается с поиска" in russian_text
    assert "безопасного выполнения инструментов" in russian_text
    assert "восстановление после дубля тикета" in russian_text
    assert "шлюзы оценок" in russian_text
    assert "поэтапного выпуска" in russian_text
    assert "обеспечения доверия" in russian_text
    assert "происхождения данных" in russian_text
    assert "вывода из эксплуатации" in russian_text
    assert "контролей расхождения целей" in russian_text
    assert "телеметрии" in russian_text
    assert "реестра" in russian_text
    assert "платформенному контракту" in russian_text

    assert "如果你想跟随贯穿案例（throughline case）" in chinese_text
    assert "支持分诊（support-triage）" in chinese_text
    assert "检索（retrieval）" in chinese_text
    assert "安全工具执行（safe tool execution）" in chinese_text
    assert "重复工单恢复（duplicate-ticket recovery）" in chinese_text
    assert "评测门（eval gates）" in chinese_text
    assert "发布（rollout）" in chinese_text
    assert "保障（assurance）" in chinese_text
    assert "来源谱系（provenance）" in chinese_text
    assert "退役（retirement）" in chinese_text
    assert "失配控制（misalignment controls）" in chinese_text
    assert "遥测（telemetry）" in chinese_text
    assert "注册表（registry）" in chinese_text
    assert "从事故到平台契约的路径（incident-to-platform-contract path）" in chinese_text

    forbidden_markers = (
        "историей support-triage",
        "начинается с retrieval",
        "проходит через duplicate-ticket recovery",
        "misalignment controls, telemetry",
        "incident-to-platform-contract путь",
        'example "如果你想跟随贯穿案例"',
        "跟着 support-triage 故事",
        "重复工单恢复、traces",
        "进入 rollout、ADLC",
        "失配控制、telemetry",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_multilingual_start_here_code_artifact_route_is_localized() -> None:
    russian_text = _read("docs/start-here.md")
    chinese_text = _read("docs/start-here.zh.md")

    assert "Маршруты по ролям" in russian_text
    assert "инженер продукта" in russian_text
    assert "идеи агента" in russian_text
    assert "рабочей архитектуре" in russian_text
    assert "платформенный инженер" in russian_text
    assert "платформенный каркас" in russian_text
    assert "одной модели" in russian_text
    assert "инженер по безопасности" in russian_text
    assert "риск модели" in russian_text
    assert "риск реального исполнения" in russian_text
    assert "руководитель или архитектор" in russian_text
    assert "эксплуатационной дисциплине" in russian_text
    assert "код и артефакты" in russian_text
    assert "линейное чтение" in russian_text
    assert "исполняемые опоры" in russian_text
    assert "Справочные страницы" in russian_text
    assert "конкретную задачу" in russian_text
    assert "Безопасное выполнение инструментов" in russian_text
    assert "Память и извлечение" in russian_text
    assert "Наблюдаемость, оценки и раскатка" in russian_text
    assert "Главная линия схем безопасного агента" in russian_text
    assert "Справочный слой" in russian_text
    assert "рядом с книгой" in russian_text
    assert "реальной инженерии" in russian_text
    assert "страница про “автономность”" in russian_text

    assert "按角色阅读（role-based routes）" in chinese_text
    assert "产品工程师（product engineer）" in chinese_text
    assert "智能体想法（agent idea）" in chinese_text
    assert "可运行架构（working architecture）" in chinese_text
    assert "平台工程师（platform engineer）" in chinese_text
    assert "平台骨架（platform skeleton）" in chinese_text
    assert "模型包壳（model wrapper）" in chinese_text
    assert "安全工程师（security engineer）" in chinese_text
    assert "模型风险（model risk）" in chinese_text
    assert "真实执行风险（real execution risk）" in chinese_text
    assert "负责人或架构师（leader or architect）" in chinese_text
    assert "演示（demo）" in chinese_text
    assert "运营纪律（operating discipline）" in chinese_text
    assert "代码和工件（code and artifacts）" in chinese_text
    assert "可执行支撑（executable supports）" in chinese_text
    assert "线性阅读（linear reading）" in chinese_text
    assert "参考页面（reference pages）" in chinese_text
    assert "具体问题（specific task）" in chinese_text
    assert "安全工具执行（safe tool execution）" in chinese_text
    assert "记忆与检索（memory and retrieval）" in chinese_text
    assert "可观测性、评测与发布（observability, evals, and rollout）" in chinese_text
    assert "安全智能体模式主线（Safe-agent schema spine）" in chinese_text
    assert "追踪模式与事件目录" in chinese_text
    assert "评测数据集模式与打分契约" in chinese_text
    assert "记忆记录与检索契约模式" in chinese_text
    assert "参考层（reference layer）" in chinese_text
    assert "旁边还可以打开什么（companion references）" in chinese_text
    assert "AI 落地页（AI landing page）" in chinese_text
    assert "真实工程（real engineering）" in chinese_text

    assert "скелет среды исполнения" in russian_text
    assert "контракты политик" in russian_text
    assert "путь памяти" in russian_text
    assert "телеметрия" in russian_text
    assert "артефакты раскатки" in russian_text

    assert "运行时骨架（runtime skeleton）" in chinese_text
    assert "策略契约（policy contracts）" in chinese_text
    assert "记忆路径（memory path）" in chinese_text
    assert "遥测（telemetry）" in chinese_text
    assert "发布工件（rollout artifacts）" in chinese_text

    forbidden_markers = (
        "не только model risk",
        "### Наблюдаемость, оценки и раскатка (rollout)",
        "### Safe-agent schema spine\n",
        "AI-лендинг про",
        "скелет runtime (runtime skeleton)",
        "нужны runtime skeleton",
        "policy contracts, memory path",
        "telemetry и rollout-артефакты",
        "## 按角色阅读\n",
        "### 如果你是产品工程师\n",
        "从智能体想法快速走到可运行架构",
        "### 如果你是平台工程师\n",
        "搭平台骨架、而不只是给一个模型包壳",
        "### 如果你是安全工程师\n",
        "不仅要看模型风险，还要看真实执行风险",
        "### 如果你是负责人或架构师\n",
        "不想只交付演示，而是要",
        "真实运营纪律的人。",
        "## 如果你想先看代码和工件\n",
        "可执行支撑比线性阅读更重要",
        "## 如果你要快速解决一个具体问题\n",
        "[参考页面](reference.zh.md)",
        "### 安全工具执行\n",
        "### 记忆与检索\n",
        "### 可观测性、评测与发布（rollout）",
        "### Safe-agent schema spine\n",
        "安全智能体 Schema 主线",
        "追踪 Schema 与事件目录",
        "评测数据集 Schema 与打分契约",
        "记忆记录与检索契约 Schema",
        "## 读书时旁边还可以打开什么\n",
        "AI 落地页更接近真实工程",
        "需要运行时骨架、策略契约",
        "记忆路径、遥测和发布工件",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_multilingual_start_here_change_management_link_is_localized() -> None:
    russian_text = _read("docs/start-here.md")
    chinese_text = _read("docs/start-here.zh.md")

    assert "Управление изменениями в агентных системах" in russian_text
    assert "智能体系统的变更管理（Change management）" in chinese_text

    forbidden_markers = (
        "Change management для агентных систем",
        "智能体系统的变更管理](book/part-viii/chapter-20",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_multilingual_start_here_observability_heading_is_localized() -> None:
    russian_text = _read("docs/start-here.md")
    chinese_text = _read("docs/start-here.zh.md")

    assert "### Наблюдаемость, оценки и раскатка" in russian_text
    assert "### 可观测性、评测与发布（observability, evals, and rollout）" in chinese_text

    forbidden_markers = (
        "### Наблюдаемость, оценки и rollout",
        "### Наблюдаемость, оценки и раскатка (rollout)",
        "### 可观测性、评测与发布（rollout）",
        "### 可观测性、评测与发布\n",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_homepage_surfaces_three_canonical_cases() -> None:
    localized_markers = (
        "Каноническая карта сценариев",
        "Триаж обращений поддержки",
        "Внутренний ассистент знаний",
        "Координация инцидентов",
        "записывающие возможности",
        "согласования",
        "восстановление после дубля тикета",
        "происхождение знаний",
        "побочные эффекты уведомлений",
        "владение ответом",
        "обучение после инцидента",
    )
    english_markers = (
        "Canonical case map",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "write capabilities",
        "approvals",
        "duplicate-ticket recovery",
        "knowledge provenance",
        "notification side effects",
        "response ownership",
        "post-incident learning",
    )

    _assert_files_contain_all(("docs/index.md",), localized_markers)
    _assert_files_contain_all(("docs/index.en.md", "docs/index.zh.md"), english_markers)


def test_multilingual_homepage_canonical_case_map_is_localized() -> None:
    russian_text = _read("docs/index.md")
    chinese_text = _read("docs/index.zh.md")

    assert "Каноническая карта сценариев" in russian_text
    assert "три канонических сценария" in russian_text
    assert "записывающие возможности" in russian_text
    assert "поиск, память, свежесть" in russian_text
    assert "трассы, эскалацию" in russian_text

    assert "规范案例地图" in chinese_text
    assert "规范案例（canonical cases）" in chinese_text
    assert "写入能力（write capabilities）" in chinese_text
    assert "检索（retrieval）" in chinese_text
    assert "追踪（traces）" in chinese_text

    forbidden_markers = (
        "три canonical cases",
        "проверяет write capabilities",
        "проверяет retrieval, memory",
        "проверяет traces, escalation",
        "三个 canonical cases",
        "检查 write capabilities",
        "检查 retrieval、memory",
        "检查 traces、escalation",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_multilingual_homepage_platform_terms_are_localized() -> None:
    russian_text = _read("docs/index.md")
    chinese_text = _read("docs/index.zh.md")

    assert "Архитектура безопасных ИИ-агентов" in russian_text
    assert "производственную реальность" in russian_text
    assert "рискованные действия" in russian_text
    assert "память, согласования" in russian_text
    assert "долгий эксплуатационный след" in russian_text
    assert "инструментов уже недостаточно" in russian_text
    assert "слой политик" in russian_text
    assert "управляемое исполнение" in russian_text
    assert "наблюдаемость" in russian_text
    assert "оценка качества" in russian_text
    assert "дисциплина жизненного цикла" in russian_text
    assert "разового трюка" in russian_text
    assert "ограничивать, наблюдать, выпускать" in russian_text
    assert "улучшать без гадания" in russian_text
    assert "Для кого эта книга" in russian_text
    assert "Что она должна изменить в мышлении читателя" in russian_text
    assert "LLM плюс немного оркестрации" in russian_text
    assert "управляемую производственную систему" in russian_text
    assert "исполнением, ограниченным политиками" in russian_text
    assert "рискованных путей" in russian_text
    assert "агентные функции" in russian_text
    assert "общая среда исполнения" in russian_text
    assert "границы доверия" in russian_text
    assert "границами действий" in russian_text
    assert "рискованные пути исполнения" in russian_text
    assert "поверхности злоупотреблений" in russian_text
    assert "наблюдаемостью уровня запуска" in russian_text
    assert "доказательствами" in russian_text
    assert "дисциплиной поэтапного выпуска" in russian_text
    assert "владением" in russian_text
    assert "управлением жизненным циклом" in russian_text

    assert "安全 AI 智能体架构（Secure AI Agent Architecture）" in chinese_text
    assert "生产现实（production reality）" in chinese_text
    assert "高风险动作（risky actions）" in chinese_text
    assert "记忆（memory）、审批（approvals）" in chinese_text
    assert "长期运维尾部（long operational tail）" in chinese_text
    assert "工具（tools）" in chinese_text
    assert "策略层（policy layer）" in chinese_text
    assert "受控执行（controlled execution）" in chinese_text
    assert "可观测性（observability）" in chinese_text
    assert "质量评估（quality assessment）" in chinese_text
    assert "生命周期纪律（lifecycle discipline）" in chinese_text
    assert "一次性炫技（one-off trick）" in chinese_text
    assert "约束（constrain）、观察（observe）、发布（ship）" in chinese_text
    assert "无需猜测地持续改进（improve without guessing）" in chinese_text
    assert "这本书适合谁（who this book is for）" in chinese_text
    assert "它应该改变读者什么思维（reader mindset shift）" in chinese_text
    assert "LLM 加一点编排（orchestration）" in chinese_text
    assert "受治理的生产系统（governed production system）" in chinese_text
    assert "策略约束的执行（policy-constrained execution）" in chinese_text
    assert "高风险路径（risky paths）" in chinese_text
    assert "智能体功能（agent features）" in chinese_text
    assert "共享运行时（runtime）" in chinese_text
    assert "信任边界（trust boundaries）" in chinese_text
    assert "动作边界（action boundaries）" in chinese_text
    assert "高风险执行路径（risky execution paths）" in chinese_text
    assert "滥用表面（abuse surfaces）" in chinese_text
    assert "运行级可观测性（run-level observability）" in chinese_text
    assert "证据（evidence）" in chinese_text
    assert "发布纪律（rollout discipline）" in chinese_text
    assert "负责人机制（ownership）" in chinese_text
    assert "生命周期治理（lifecycle governance）" in chinese_text

    forbidden_markers = (
        "реальность production",
        "# Архитектура Безопасных AI-Агентов\n",
        "появляются risky actions",
        "память, подтверждения, раскатка",
        "нескольких tools",
        "Нужны явные границы доверия, policy layer",
        "управляемую production-систему",
        "с исполнением (execution) под контролем политик",
        "строить agent features",
        "общий runtime, policy layer, approvals",
        "важны trust boundaries, risky execution paths",
        "явными trust и action boundaries",
        "с execution под контролем",
        "с approvals для рискованных путей",
        "run-level observability и evidence",
        "rollout discipline, ownership и lifecycle governance",
        "承受生产现实的智能体系统",
        "# 安全 AI 智能体架构\n",
        "高风险动作、记忆",
        "记忆、审批、发布",
        "长期运维尾部，",
        "几个工具就不够",
        "受控执行、可观测性、质量判断",
        "一次性的炫技",
        "约束、观察、发布并持续改进",
        "不必靠猜",
        "## 这本书适合谁\n",
        "## 它应该改变读者什么思维\n",
        "LLM 加一点编排”，",
        "受治理的生产系统：",
        "执行（execution）受策略约束",
        "高风险路径有审批",
        "共享运行时、策略层、审批",
        "信任边界、高风险执行路径",
        "运行级可观测性与证据",
        "发布纪律、负责人机制",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_homepage_surfaces_safe_agent_schema_spine() -> None:
    localized_markers = (
        "Цепочка схем безопасного агента",
        "схемы трасс",
        "схемы оценивания",
        "схемы памяти и поиска",
        "модель угроз MCP",
        "контракт доверия передачи управления A2A",
        "запись вердикта проверяющего",
        "запись управленческого действия",
        "поля проверки отравления памяти",
        "единые доказательства угроз агенту",
    )
    english_markers = (
        "Safe-agent schema spine",
        "trace schema",
        "eval schema",
        "memory/retrieval schema",
        "MCP threat model",
        "A2A handoff trust contract",
        "verifier verdict record",
        "governance action record",
        "memory poisoning review fields",
        "unified agent threat evidence",
    )

    _assert_files_contain_all(("docs/index.md",), localized_markers)
    _assert_files_contain_all(("docs/index.en.md", "docs/index.zh.md"), english_markers)


def test_multilingual_homepage_safe_agent_schema_spine_is_localized() -> None:
    russian_text = _read("docs/index.md")
    chinese_text = _read("docs/index.zh.md")

    assert "Цепочка схем безопасного агента" in russian_text
    assert "архитектуре безопасного агента" in russian_text
    assert "схемы трасс" in russian_text
    assert "схемы оценивания" in russian_text
    assert "схемы памяти и поиска" in russian_text
    assert "модель угроз MCP" in russian_text
    assert "контракт доверия передачи управления A2A" in russian_text
    assert "запись вердикта проверяющего" in russian_text
    assert "единые доказательства угроз агенту" in russian_text

    assert "安全智能体模式主线（Safe-agent schema spine）" in chinese_text
    assert "安全智能体架构（safe-agent architecture）" in chinese_text
    assert "追踪模式（trace schema）" in chinese_text
    assert "评测模式（eval schema）" in chinese_text
    assert "记忆/检索模式（memory/retrieval schema）" in chinese_text
    assert "MCP 威胁模型（MCP threat model）" in chinese_text
    assert "A2A 移交信任契约（A2A handoff trust contract）" in chinese_text
    assert "验证器裁决记录（verifier verdict record）" in chinese_text
    assert "统一智能体威胁证据（unified agent threat evidence）" in chinese_text

    forbidden_markers = (
        '!!! note "Safe-agent schema spine"',
        "путь по safe-agent architecture",
        "начни с [trace schema]",
        "Этот spine связывает MCP threat model",
        "A2A handoff trust contract, verifier verdict record",
        "memory poisoning review fields и unified agent threat evidence",
        "safe-agent architecture 路线",
        "从 [trace schema]",
        "这个 spine 连接 MCP threat model",
        "A2A handoff trust contract、verifier verdict record",
        "memory poisoning review fields 和 unified agent threat evidence",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_multilingual_homepage_existing_scope_terms_are_localized() -> None:
    russian_text = _read("docs/index.md")
    chinese_text = _read("docs/index.zh.md")

    assert "Что здесь уже есть" in russian_text
    assert "основная рукопись" in russian_text
    assert "управления жизненным циклом" in russian_text
    assert "редакторскую очистку" in russian_text
    assert "схемами трасс" in russian_text
    assert "оценивания" in russian_text
    assert "пакетов политик" in russian_text
    assert "согласований" in russian_text
    assert "артефактов жизненного цикла" in russian_text
    assert "редакторский проход" in russian_text
    assert "программному каркасу" in russian_text
    assert "трюков с промптами" in russian_text
    assert "обзор AI-рынка" in russian_text
    assert "платформенной документацией" in russian_text
    assert "путь записи" in russian_text
    assert "Что не является целью книги" in russian_text
    assert "Куда идти дальше" in russian_text
    assert "С чего начать" in russian_text
    assert "Прочитать главу 1" in russian_text
    assert "Открыть план книги" in russian_text
    assert "Перейти к первой части" in russian_text
    assert "Открыть эталонный пакет" in russian_text
    assert "Как читать книгу" in russian_text
    assert "короткий вход" in russian_text
    assert "маршрут под задачу и роль" in russian_text
    assert "страницу старта" in russian_text
    assert "структура и статус разделов" in russian_text
    assert "план книги" in russian_text
    assert "Самый короткий путь" in russian_text
    assert "через книгу" in russian_text
    assert "переиспользуемые артефакты" in russian_text
    assert "схемы и контракты" in russian_text
    assert "справочный слой" in russian_text

    assert "这里已经有什么（what already exists）" in chinese_text
    assert "核心原稿（core manuscript）" in chinese_text
    assert "生命周期治理（lifecycle governance）" in chinese_text
    assert "编辑清理（editorial cleanup）" in chinese_text
    assert "追踪（traces）" in chinese_text
    assert "评测（evals）" in chinese_text
    assert "策略包（policy bundles）" in chinese_text
    assert "审批（approvals）" in chinese_text
    assert "生命周期工件（lifecycle artifacts）" in chinese_text
    assert "编辑打磨（editorial pass）" in chinese_text
    assert "框架（framework）的手册" in chinese_text
    assert "提示技巧合集（prompt tricks）" in chinese_text
    assert "AI 市场巡礼（AI market overview）" in chinese_text
    assert "平台文档（platform docs）" in chinese_text
    assert "写入路径（write path）" in chinese_text
    assert "这本书不打算成为什么（what the book is not）" in chinese_text
    assert "接下来去哪里（where to go next）" in chinese_text
    assert "从这里开始（Start Here）" in chinese_text
    assert "阅读第 1 章（chapter 1）" in chinese_text
    assert "打开全书计划（book plan）" in chinese_text
    assert "进入第一部分（Part I）" in chinese_text
    assert "打开参考包（reference package）" in chinese_text
    assert "这本书怎么读（how to read the book）" in chinese_text
    assert "短入口（short entry）" in chinese_text
    assert "任务和角色路线（task and role route）" in chinese_text
    assert "从这里开始（Start Here）" in chinese_text
    assert "结构与章节状态（structure and section status）" in chinese_text
    assert "全书计划（book plan）" in chinese_text
    assert "穿过全书（through the book）" in chinese_text
    assert "最短路径（shortest path）" in chinese_text
    assert "可复用工件（reusable artifacts）" in chinese_text
    assert "模式（schemas）" in chinese_text
    assert "契约（contracts）" in chinese_text
    assert "参考层（reference layer）" in chinese_text

    forbidden_markers = (
        "core-рукопись",
        "до lifecycle governance",
        "проходящие editorial cleanup",
        "схемами traces, evals",
        "policy bundles, approvals",
        "lifecycle-артефактов",
        "Активный editorial pass",
        "сборник prompt tricks",
        "SDK и platform docs",
        "ограничивать write path",
        "生命周期治理的八个部分",
        "## 这里已经有什么\n",
        "编辑清理的 `en`",
        "覆盖追踪、评测、策略包、审批",
        "生命周期工件的参考页面",
        "公开站点表面编辑打磨。",
        "某个框架的手册",
        "提示技巧合集，也不是",
        "AI 市场巡礼。本书",
        "平台文档之上",
        "写入路径应该怎样受限",
        "## 这本书不打算成为什么\n",
        "## 接下来去哪里\n",
        "[从这里开始](start-here.zh.md)",
        "[阅读第 1 章](book/part-i/chapter-1.zh.md)",
        "[打开全书计划](book/plan.zh.md)",
        "[进入第一部分](book/part-i/index.zh.md)",
        "[打开参考包](appendix/reference-package.zh.md)",
        "## 这本书怎么读\n",
        "如果你只想要最短入口",
        "按角色或任务选择路线",
        "更关心结构与状态",
        "穿过全书的最短实用途径",
        "可复用工件、Schema 和契约",
        "进入[参考层](reference.zh.md)",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_public_entry_safe_agent_schema_spine_links_are_clickable() -> None:
    expected_links_by_file = {
        "README.md": (
            "docs/appendix/trace-schema.en.md",
            "docs/appendix/eval-schema.en.md",
            "docs/appendix/memory-retrieval-schema.en.md",
        ),
        "README.ru.md": (
            "docs/appendix/trace-schema.md",
            "docs/appendix/eval-schema.md",
            "docs/appendix/memory-retrieval-schema.md",
        ),
        "README.zh.md": (
            "docs/appendix/trace-schema.zh.md",
            "docs/appendix/eval-schema.zh.md",
            "docs/appendix/memory-retrieval-schema.zh.md",
        ),
        "docs/index.md": (
            "appendix/trace-schema.md",
            "appendix/eval-schema.md",
            "appendix/memory-retrieval-schema.md",
        ),
        "docs/index.en.md": (
            "appendix/trace-schema.en.md",
            "appendix/eval-schema.en.md",
            "appendix/memory-retrieval-schema.en.md",
        ),
        "docs/index.zh.md": (
            "appendix/trace-schema.zh.md",
            "appendix/eval-schema.zh.md",
            "appendix/memory-retrieval-schema.zh.md",
        ),
        "docs/start-here.md": (
            "appendix/trace-schema.md",
            "appendix/eval-schema.md",
            "appendix/memory-retrieval-schema.md",
        ),
        "docs/start-here.en.md": (
            "appendix/trace-schema.en.md",
            "appendix/eval-schema.en.md",
            "appendix/memory-retrieval-schema.en.md",
        ),
        "docs/start-here.zh.md": (
            "appendix/trace-schema.zh.md",
            "appendix/eval-schema.zh.md",
            "appendix/memory-retrieval-schema.zh.md",
        ),
    }

    for path, expected_links in expected_links_by_file.items():
        text = _read(path)
        for link in expected_links:
            assert f"]({link})" in text, (path, link)


def test_reference_layer_surfaces_three_canonical_case_artifacts() -> None:
    required_markers_by_file = {
        "docs/reference.md": (
            "Канонические артефакты сценариев",
            "Триаж обращений поддержки",
            "Внутренний ассистент знаний",
            "Координация инцидентов",
            "запись подтверждения",
            "пакет политик",
            "доказательства восстановления после дубля тикета",
            "контракт памяти и поиска",
            "проверки свежести",
            "контроль доступа",
            "происхождение знаний",
            "побочные эффекты уведомлений",
            "ответственность за реагирование",
            "обучение после инцидента",
        ),
        "docs/reference.en.md": (
            "Canonical case artifacts",
            "Support triage",
            "Internal knowledge assistant",
            "Incident coordination",
            "approval record",
            "policy bundle",
            "duplicate-ticket recovery evidence",
            "memory/retrieval contract",
            "freshness checks",
            "access control",
            "knowledge provenance",
            "notification side effects",
            "response ownership",
            "post-incident learning",
        ),
        "docs/reference.zh.md": (
            "Canonical case artifacts",
            "Support triage",
            "Internal knowledge assistant",
            "Incident coordination",
            "approval record",
            "policy bundle",
            "duplicate-ticket recovery evidence",
            "memory/retrieval contract",
            "freshness checks",
            "access control",
            "knowledge provenance",
            "notification side effects",
            "response ownership",
            "post-incident learning",
        ),
    }

    for path, required_markers in required_markers_by_file.items():
        _assert_files_contain_all((path,), required_markers)


def test_multilingual_reference_case_artifacts_note_is_localized() -> None:
    russian_text = _read("docs/reference.md")
    chinese_text = _read("docs/reference.zh.md")

    assert "# Справочный слой" in russian_text
    assert "## С чего начать" in russian_text
    assert "Канонические артефакты сценариев" in russian_text
    assert "почему безопасная агентная система" in russian_text
    assert "какие артефакты, схемы и правила" in russian_text
    assert "нужную контрактную страницу" in russian_text
    assert "архитектурное ревью или ревью поэтапного выпуска" in russian_text
    assert "Три канонических сценария" in russian_text
    assert "запись подтверждения" in russian_text
    assert "контракт памяти и поиска" in russian_text
    assert "запись инцидента" in russian_text
    assert "поддерживающие схемы" in russian_text
    assert "проверочные списки" in russian_text
    assert "контрактные поверхности" in russian_text
    assert "переиспользуемых инженерных материалов" in russian_text
    assert "читательский путь" in russian_text
    assert "готовые артефакты" in russian_text
    assert "прикладной инженерной форме" in russian_text
    assert "причинно-следственный аргумент" in russian_text
    assert "компромиссы" in russian_text
    assert "границы между слоями" in russian_text

    assert "# 参考层（reference layer）" in chinese_text
    assert "从这里开始（Start Here）" in chinese_text
    assert "规范案例工件" in chinese_text
    assert "为什么（why）" in chinese_text
    assert "安全智能体系统（safe agent system）" in chinese_text
    assert "工件（artifacts）、模式页（schemas）与规则（rules）" in chinese_text
    assert "契约页（contract page）" in chinese_text
    assert "架构评审（architecture review）" in chinese_text
    assert "发布评审（rollout review）" in chinese_text
    assert "规范案例（canonical cases）" in chinese_text
    assert "审批记录（approval record）" in chinese_text
    assert "记忆/检索契约（memory/retrieval contract）" in chinese_text
    assert "事件记录（incident record）" in chinese_text
    assert "支撑性模式（supporting schemas）" in chinese_text
    assert "检查清单（checklists）" in chinese_text
    assert "契约表面（contract surfaces）" in chinese_text
    assert "参考层（reference layer）" in chinese_text
    assert "可复用工程材料（reusable engineering materials）" in chinese_text
    assert "阅读路径（reading path）" in chinese_text
    assert "即用工件（ready-to-use artifacts）" in chinese_text
    assert "工程形式（applied engineering form）" in chinese_text
    assert "因果论证（causal argument / chapter by chapter）" in chinese_text
    assert "取舍（tradeoffs）" in chinese_text
    assert "层间边界（layer boundaries）" in chinese_text
    assert "论证（argument）" in chinese_text
    assert "顺序（sequence）" in chinese_text
    assert "支撑工件（supporting artifacts）" in chinese_text
    assert "实现细节（implementation details）" in chinese_text

    forbidden_markers = (
        "Три canonical cases",
        "**почему** безопасная агентная система",
        "архитектурное ревью или ревью раскатки",
        "опирается на approval record",
        "требует memory/retrieval contract",
        "связывает incident record",
        "поддерживающие схемы, чеклисты и контрактные страницы",
        "не весь reference layer",
        "переиспользуемых инженерных материалов,",
        "(reference layer)",
        "(Start Here)",
        "(why)",
        "(safe agent system)",
        "(artifacts)",
        "(schemas)",
        "(rules)",
        "(contract page)",
        "(architecture review)",
        "(rollout review)",
        "(canonical cases)",
        "(approval record)",
        "(memory/retrieval contract)",
        "(incident record)",
        "(supporting schemas)",
        "(checklists)",
        "(contract surfaces)",
        "(reusable engineering materials)",
        "(reading path)",
        "(ready-to-use artifacts)",
        "(applied engineering form)",
        "(causal argument)",
        "(chapter by chapter)",
        "(tradeoffs)",
        "(layer boundaries)",
        "三个 canonical cases",
        "# 参考层\n",
        "## 从这里开始\n",
        "**为什么**安全智能体系统",
        "哪些工件、模式页与契约页",
        "合适的契约页；",
        "设计评审或发布评审",
        "依赖 approval record",
        "需要 memory/retrieval contract",
        "连接 incident record",
        "支撑性的 Schema、检查清单和契约表面",
        "不需要整个参考层，",
        "可复用的工程材料来支撑",
        "可复用的工程工件",
        "更落地的工程材料",
        "按章节去解释主要的因果论证",
        "取舍与层间边界",
        "理解论证与章节顺序",
        "支撑工件与面向实现的细节",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_multilingual_reference_support_triage_artifact_route_is_localized() -> None:
    russian_text = _read("docs/reference.md")
    chinese_text = _read("docs/reference.zh.md")

    assert "Артефактный маршрут триажа поддержки" in russian_text
    assert "трассы" in russian_text
    assert "набор данных оценок" in russian_text
    assert "пакет политик" in russian_text
    assert "запись подтверждения" in russian_text
    assert "запись инцидента" in russian_text
    assert "поэтапный выпуск изменений" in russian_text
    assert "артефакты жизненного цикла" in russian_text
    assert "операции реестра" in russian_text
    assert "инцидент с дублем тикета" in russian_text

    assert "支持分诊工件路线（support-triage）" in chinese_text
    assert "追踪（traces）" in chinese_text
    assert "评测数据集（eval dataset）" in chinese_text
    assert "策略包（policy bundle）" in chinese_text
    assert "审批记录（approval record）" in chinese_text
    assert "事故记录（incident record）" in chinese_text
    assert "变更发布（change rollout）" in chinese_text
    assert "生命周期工件（lifecycle artifacts）" in chinese_text
    assert "注册表运维（registry operations）" in chinese_text
    assert "重复工单事故（duplicate-ticket incident）" in chinese_text

    forbidden_markers = (
        'example "Артефактный маршрут support-triage"',
        "кейс support-triage",
        "страницы про traces, eval dataset",
        "policy bundle, approval record",
        "incident record, change rollout",
        "lifecycle artifacts и registry operations",
        "duplicate-ticket incident из рассказа",
        'example "support-triage 工件路线"',
        "按 support-triage 案例",
        "把 traces、评测数据集",
        "policy bundle、审批记录",
        "registry operations 这些页面",
        "(support-triage)",
        "(traces)",
        "(eval dataset)",
        "(policy bundle)",
        "(approval record)",
        "(incident record)",
        "(change rollout)",
        "(lifecycle artifacts)",
        "(registry operations)",
        "(duplicate-ticket incident)",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_multilingual_reference_practice_links_are_localized() -> None:
    russian_text = _read("docs/reference.md")
    chinese_text = _read("docs/reference.zh.md")

    assert "Схемы и контрактные страницы" in russian_text
    assert "Практические страницы" in russian_text
    assert "Быстрые маршруты по темам" in russian_text
    assert "короткий вход" in russian_text
    assert "конкретный вопрос" in russian_text
    assert "Для дальнейшего чтения" in russian_text
    assert "связи с разбором" in russian_text
    assert "реестру агентов" in russian_text
    assert "инвентаризации" in russian_text
    assert "Шаблон постмортема" in russian_text
    assert "многоагентных систем" in russian_text

    assert "模式页与契约页（schemas and contract pages）" in chinese_text
    assert "追踪模式与事件目录" in chinese_text
    assert "评测数据集模式与打分契约" in chinese_text
    assert "策略包模式与审批契约" in chinese_text
    assert "审批请求与决策记录模式" in chinese_text
    assert "事故记录与事后复盘链接模式" in chinese_text
    assert "变更评审与发布门禁模式" in chinese_text
    assert "生命周期工件模式" in chinese_text
    assert "记忆记录与检索契约模式" in chinese_text
    assert "实践页面（practice pages）" in chinese_text
    assert "按主题快速进入（quick topic routes）" in chinese_text
    assert "短入口（short entry）" in chinese_text
    assert "具体问题（specific question）" in chinese_text
    assert "继续阅读（further reading）" in chinese_text
    assert "智能体注册表（agent registry）" in chinese_text
    assert "清单运维（inventory operations）" in chinese_text
    assert "事后复盘（postmortem）模板" in chinese_text
    assert "多智能体（multi-agent）可靠性" in chinese_text

    forbidden_markers = (
        "связи с postmortem",
        "по registry агентов и inventory operations",
        "Шаблон postmortem",
        "multi-agent систем",
        "## 模式页与契约页\n",
        "## 实践页面\n",
        "追踪 Schema 与事件目录",
        "评测数据集 Schema 与打分契约",
        "策略包 Schema 与审批契约",
        "审批请求与决策记录 Schema",
        "事故记录与事后复盘链接 Schema",
        "变更评审与发布门禁 Schema",
        "生命周期工件 Schema",
        "记忆记录与检索契约 Schema",
        "## 按主题快速进入\n",
        "快速进入一个具体问题",
        "## 继续阅读\n",
        "智能体注册表与清单运维手册",
        "智能体系统事后复盘模板",
        "多智能体可靠性",
        "(schemas and contract pages)",
        "(practice pages)",
        "(quick topic routes)",
        "(short entry)",
        "(specific question)",
        "(further reading)",
        "(postmortem)",
        "(agent registry)",
        "(inventory operations)",
        "(multi-agent systems)",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_multilingual_reference_safe_agent_schema_spine_is_localized() -> None:
    russian_text = _read("docs/reference.md")
    chinese_text = _read("docs/reference.zh.md")

    assert "Цепочка схем безопасного агента" in russian_text
    assert "архитектуре безопасного агента" in russian_text
    assert "схему трасс" in russian_text
    assert "схему оценивания" in russian_text
    assert "схему памяти и поиска" in russian_text
    assert "модель угроз MCP" in russian_text
    assert "контракт доверия передачи управления A2A" in russian_text
    assert "запись вердикта проверяющего" in russian_text
    assert "единые доказательства угроз агенту" in russian_text

    assert "安全智能体模式主线（Safe-agent schema spine）" in chinese_text
    assert "安全智能体架构（safe-agent architecture）" in chinese_text
    assert "追踪模式（trace schema）" in chinese_text
    assert "评测模式（eval schema）" in chinese_text
    assert "记忆/检索模式（memory/retrieval schema）" in chinese_text
    assert "MCP 威胁模型（MCP threat model）" in chinese_text
    assert "A2A 移交信任契约（A2A handoff trust contract）" in chinese_text
    assert "验证器裁决记录（verifier verdict record）" in chinese_text
    assert "统一智能体威胁证据（unified agent threat evidence）" in chinese_text

    forbidden_markers = (
        '!!! note "Safe-agent schema spine"',
        "маршрут по safe-agent architecture",
        "рядом [trace schema]",
        "связаны MCP threat model",
        "A2A handoff trust contract, verifier verdict record",
        "memory poisoning review fields и unified agent threat evidence",
        "(Safe-agent schema spine)",
        "(safe-agent architecture)",
        "(trace schema)",
        "(eval schema)",
        "(memory/retrieval schema)",
        "(MCP threat model)",
        "(A2A handoff trust contract)",
        "(verifier verdict record)",
        "(unified agent threat evidence)",
        "safe-agent architecture 的短路线",
        "[trace schema]",
        "连接了 MCP threat model",
        "A2A handoff trust contract、verifier verdict record",
        "memory poisoning review fields 和 unified agent threat evidence",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_part_viii_index_surfaces_three_canonical_lifecycle_cases() -> None:
    russian_markers = (
        "Канонические сценарии жизненного цикла",
        "Разбор обращений поддержки",
        "Внутренний ассистент знаний",
        "Координация инцидентов",
        "пакеты изменений для записывающих возможностей",
        "подтверждения",
        "доказательства восстановления после дубля тикета",
        "владение корпусом",
        "проверку свежести",
        "контроль доступа",
        "происхождение знаний",
        "право эскалации",
        "побочные эффекты уведомлений",
        "ответственность за реагирование",
        "обучение после инцидента",
    )
    english_markers = (
        "Canonical lifecycle cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "write-capability change packets",
        "approvals",
        "duplicate-ticket recovery evidence",
        "corpus ownership",
        "freshness review",
        "access control",
        "knowledge provenance",
        "escalation authority",
        "notification side effects",
        "response ownership",
        "post-incident learning",
    )

    _assert_files_contain_all(("docs/book/part-viii/index.md",), russian_markers)
    _assert_files_contain_all(("docs/book/part-viii/index.en.md",), english_markers)

    chinese_text = _read("docs/book/part-viii/index.zh.md")
    expected_chinese_markers = (
        "规范生命周期案例（Canonical lifecycle cases）",
        "支持分诊（Support triage）",
        "内部知识助手（Internal knowledge assistant）",
        "事故协调（Incident coordination）",
        "写能力变更包（write-capability change packets）",
        "审批（approvals）",
        "重复工单恢复证据（duplicate-ticket recovery evidence）",
        "语料责任归属（corpus ownership）",
        "新鲜度审查（freshness review）",
        "访问控制（access control）",
        "知识来源证明（knowledge provenance）",
        "升级权限（escalation authority）",
        "通知副作用（notification side effects）",
        "响应责任归属（response ownership）",
        "事故后学习（post-incident learning）",
    )
    for expected_chinese_marker in expected_chinese_markers:
        assert expected_chinese_marker in chinese_text, expected_chinese_marker

    forbidden_chinese_markers = (
        'note "Canonical lifecycle cases"',
        "三个 canonical cases 会拆到不同 lifecycle questions",
        "**Support triage** 检查 write-capability change packets",
        "approvals 和 duplicate-ticket recovery evidence",
        "**Internal knowledge assistant** 检查 corpus ownership",
        "freshness review、access control 和 knowledge provenance",
        "**Incident coordination** 检查 escalation authority",
        "notification side effects、response ownership 和 post-incident learning",
    )
    for forbidden_chinese_marker in forbidden_chinese_markers:
        assert forbidden_chinese_marker not in chinese_text, forbidden_chinese_marker


def test_part_viii_chinese_role_map_labels_are_localized() -> None:
    chinese_text = _read("docs/book/part-viii/index.zh.md")
    expected_markers = (
        "地图（map）",
        "治理（governance）观点",
        "便于打印（print-friendly）",
        "工件（artifact）是 ADLC 状态模型",
        "发现项（findings）转成遏制（containment）",
        "修复（remediation）和责任归属（ownership）",
        "评测打分（eval scoring）",
        "证据基底（evidence substrate）",
        "治理决策（governance decision）",
        "负责人（owner）和生命周期状态",
        "智能体群体（estate）",
        "生命周期（lifecycle）定义状态",
        "变更管理（change management）控制移动",
        "评测（evals）判断是否可发布",
        "来源追踪（provenance）记录哪些工件可信",
        "可观测性（observability）保留证据（evidence）",
        "保障（assurance）在证据变成风险（risk）时响应",
        "退役（retirement）关闭旧路径",
        "注册表（registry）维持整个智能体群体（estate）的问责（accountability）",
        "评审（review）后必须留下的工件",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "用这张 map 来避免",
        "同一个 governance 观点",
        "Print-friendly 版本",
        "它的 artifact 是 ADLC 状态模型",
        "把 findings 转成 containment、remediation 和 ownership",
        "不是可观测性或 eval scoring",
        "让 evidence substrate 可见",
        "不是 governance decision 的负责人",
        "通过 owner 和生命周期状态让整个 estate 可问责",
        "lifecycle 定义状态，change management 控制移动",
        "evals 判断是否可发布",
        "provenance 记录哪些工件可信",
        "observability 保留 evidence",
        "assurance 在 evidence 变成 risk 时响应",
        "retirement 关闭旧路径",
        "registry 维持整个 estate 的 accountability",
        "像 “governance”",
        "review 后必须留下的工件",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_reference_package_scopes_three_canonical_cases_to_runtime() -> None:
    from agent_runtime_ref.config import load_agent_profile

    agent, _ = load_agent_profile(ROOT / "agent_runtime_ref/configs/agent.yaml")
    expected_markers_by_file = {
        "docs/appendix/reference-package.md": (
            "Каноническая область выполнения сценариев",
            "Триаж обращений поддержки",
            "Внутренний ассистент знаний",
            "Координация инцидентов",
            "исполняемую базовую линию",
            "записывающих возможностей",
            "подтверждений",
            "восстановления после дубля тикета",
            "контрольными линзами покрытия",
            "поиск, память, свежесть",
            "происхождение знаний",
            "побочные эффекты уведомлений",
            "владение ответом",
            "обучение после инцидента",
            "исполняемые конфигурации",
            f"`agent_id` `{agent.agent_id}`",
            f"`{agent.display_name}`",
            f"`owner_team` `{agent.owner_team}`",
            f"`runtime_principal` `{agent.runtime_principal}`",
            "контракты политик, телеметрии, жизненного цикла и реестра",
        ),
        "docs/appendix/reference-package.en.md": (
            "Canonical case runtime scope",
            "Support triage",
            "Internal knowledge assistant",
            "Incident coordination",
            "runnable baseline",
            "write capabilities",
            "approvals",
            "duplicate-ticket recovery",
            "coverage lenses",
            "retrieval",
            "memory",
            "freshness",
            "knowledge provenance",
            "notification side effects",
            "response ownership",
            "post-incident learning",
            "runnable configs",
            f"agent_id `{agent.agent_id}`",
            f"`{agent.display_name}`",
            f"owner_team `{agent.owner_team}`",
            f"runtime_principal `{agent.runtime_principal}`",
            "policy, telemetry, lifecycle",
            "registry contracts",
        ),
        "docs/appendix/reference-package.zh.md": (
            "规范案例运行时范围",
            "支持分诊",
            "内部知识助手",
            "事故协调",
            "可运行基线",
            "写入能力",
            "审批",
            "重复工单恢复",
            "覆盖视角",
            "检索",
            "记忆",
            "新鲜度",
            "知识来源",
            "通知副作用",
            "响应归属",
            "事件后学习",
            "可运行配置",
            f"agent_id `{agent.agent_id}`",
            f"`{agent.display_name}`",
            f"owner_team `{agent.owner_team}`",
            f"runtime_principal `{agent.runtime_principal}`",
            "策略、遥测、生命周期和注册表契约",
        ),
    }

    for path, expected_markers in expected_markers_by_file.items():
        text = _read(path)
        for expected_marker in expected_markers:
            assert expected_marker in text, (path, expected_marker)


def test_chinese_reference_package_generic_loader_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/reference-package.zh.md")
    assert "通用加载器（Generic loaders）" in chinese_text
    assert "畸形 YAML 形状（malformed YAML shapes）" in chinese_text
    assert "Generic loaders 也会明确暴露 malformed YAML shapes" not in chinese_text


def test_chinese_reference_package_eval_dataset_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/reference-package.zh.md")
    expected_markers = (
        "资料查询（profile lookup）",
        "标签（labels）",
        "预期结果（expected outcomes）",
        "多运行审批加记忆（multi-run approval-plus-memory）",
        "标签（label）",
        "预期结果（expected outcome）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "profile lookup 场景",
        "grounded_answer` labels",
        "session_evals` labels",
        "作为 expected outcomes 的 multi-run approval-plus-memory",
        "sandbox_profile_review` label",
        "sandbox_profile_reviewed` expected outcome",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chinese_reference_package_failed_run_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/reference-package.zh.md")
    expected_markers = (
        "失败或拒绝的运行（failed or denied runs）",
        "终止态（terminal）`run_complete.failure_reason`",
        "追踪检查（trace inspection）",
        "回放摘要（replay summaries）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "为 failed 或 denied runs 发出",
        "以及 terminal `run_complete.failure_reason`",
        "trace inspection、replay summaries 与 CLI 输出",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chinese_reference_package_rollout_cli_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/reference-package.zh.md")
    expected_markers = (
        "发布检查（Rollout check）",
        "必需证据（required evidence）",
        "信号覆盖（signal overrides）",
        "布尔型 `key=value` 键值对（boolean `key=value` pairs）",
        "未知布尔文本（boolean text）",
        "运行时 CLI 失败路径（Runtime CLI failure paths）",
        "面向操作员消息（operator-facing messages）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "Rollout check 会返回",
        "它的 required evidence 包括",
        "signal overrides 接受 boolean",
        "布尔型（boolean）`key=value` 对（pairs）",
        "拒绝未知 boolean text",
        "Runtime CLI failure paths 也会保持稳定的 operator-facing messages",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chinese_reference_package_change_readiness_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/reference-package.zh.md")
    expected_markers = (
        "必需信号（required signals）",
        "变更就绪度（change readiness）",
        "发布就绪度（rollout readiness）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "它的 required signals 包括",
        "进入 change readiness 和 rollout readiness",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chinese_reference_package_sandbox_profile_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/reference-package.zh.md")
    expected_markers = (
        "沙箱配置文件（sandbox profile）变更",
        "最小沙箱配置文件（sandbox profile）",
        "由沙箱（sandbox）支撑的执行",
        "工作区（workspace）",
        "配置文件（profile）",
        "运行时（runtime）",
        "清单（manifest）",
        "权限（permissions）",
        "工作区物化（workspace materialization）",
        "会话状态（session state）",
        "快照/恢复策略（snapshot/resume policy）",
        "复核（review）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "sandbox profile 变更",
        "### 最小 sandbox profile",
        "由 sandbox 支撑的执行",
        "把 workspace 和权限显式化的小 profile",
        "真实由 sandbox 支撑的 runtime",
        "manifest、permissions、workspace materialization",
        "session state，以及 snapshot/resume policy",
        "可以被 review",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chinese_reference_package_sandbox_construction_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/reference-package.zh.md")
    expected_markers = (
        "直接构造（direct construction）",
        "畸形沙箱根（malformed sandbox roots）",
        "畸形沙箱分区（malformed sandbox sections）",
        "畸形沙箱证据值（malformed sandbox evidence values）",
        "畸形工作区条目（malformed workspace entries）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "direct construction 会用",
        "拒绝 malformed sandbox roots",
        "拒绝 malformed sandbox sections",
        "拒绝 malformed sandbox evidence values",
        "拒绝 malformed workspace entries",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chinese_reference_package_lifecycle_loader_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/reference-package.zh.md")
    expected_markers = (
        "生命周期列表加载器（Lifecycle list loaders）",
        "拒绝畸形、空白和重复条目（malformed, blank, and duplicate entries）",
        "控制包（control-bundle）记录",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "Lifecycle list loaders reject malformed",
        "blank, and duplicate entries with",
        "审批/control-bundle 记录",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chinese_reference_package_controls_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/reference-package.zh.md")
    expected_markers = (
        "能力清单不匹配（capability inventory mismatches）",
        "输入（inputs）",
        "验证形状（validation shapes）",
        "控制策略（controls policy）",
        "规范化（normalize）",
        "评测（evaluation）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "与 capability inventory mismatches 就能",
        "中的 inputs 要求",
        "with validation shapes",
        "controls policy 会把这些 normalize",
        "在 evaluation 中成为",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chinese_reference_package_runtime_control_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/reference-package.zh.md")
    expected_markers = (
        "运行时控制摘要（runtime-control summary）",
        "能力会话（capability sessions）",
        "进度（progress）",
        "澄清请求（elicitation）",
        "过期假设（expiry assumptions）",
        "默认值（defaults）",
        "可恢复/重新初始化流程（resumable/reinit flows）",
        "沙箱配置文件加载器（Sandbox-profile loader）",
        "运行时控制形状（runtime-control shapes）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "同一份 runtime-control summary",
        "可恢复的 capability sessions 会明确暴露 progress",
        "elicitation 与 expiry assumptions",
        "`delegated_authorization` defaults",
        "resumable/reinit flows 使用",
        "Sandbox-profile loader 会用这些错误校验 runtime-control shapes",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chinese_reference_package_identity_loader_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/reference-package.zh.md")
    assert "身份/目录加载器（Identity/catalog loaders）" in chinese_text
    assert "错误验证形状（validation shapes）" in chinese_text
    assert "Identity/catalog loaders 会用这些错误校验 shape" not in chinese_text


def test_chinese_reference_package_inspect_agent_tail_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/reference-package.zh.md")
    expected_markers = (
        "重复工单线索（duplicate-ticket thread）",
        "支持团队拥有（support-owned）",
        "高风险（high-risk）",
        "经纪式（brokered）",
        "调和（reconciliation）",
        "幂等键（idempotency key）",
        "写入能力（write capability）",
        "负责人（owner）",
        "工具主体绑定（tool-principal binding）",
        "出口目标（egress target）",
        "操作员（operators）",
        "完整目录列表（catalog list）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "对于贯穿的 duplicate-ticket thread",
        "呈现为 support-owned、high-risk、brokered",
        "安全重试或 reconciliation 之前要求 idempotency key",
        "写入 capability 的 owner 与 tool-principal binding",
        "brokered `tickets.internal` egress target",
        "operators 不必先扫描完整 catalog list",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chinese_reference_package_inspect_agent_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/reference-package.zh.md")
    expected_markers = (
        "清单评审（inventory review）",
        "已配置身份（configured identity）",
        "能力目录（capability catalog）",
        "该身份（identity）使用 agent_id `support-triage-ref`",
        "显示名（display_name）是 `Support triage reference agent`",
        "归属团队 owner_team `agent_platform`",
        "运行时主体 runtime_principal `svc-support-triage-ref`",
        "只批准（approved）`search_docs` 与 `create_ticket`",
        "`catalog_capabilities` 条目（entry）",
        "评审者（reviewers）",
        "响应（response）",
        "能力身份（capability identity）",
        "出口姿态（egress posture）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "让 inventory review 可以把 configured identity 与 capability catalog 对照起来",
        "该 identity 使用 agent_id",
        "display_name 是 `Support triage reference agent`",
        "，owner_team `agent_platform`",
        "，runtime_principal `svc-support-triage-ref`",
        "只 approved `search_docs` 与 `create_ticket`",
        "随后 capability catalog 将",
        "`catalog_capabilities` entry",
        "让 reviewers 在同一个 response 中看到 capability identity",
        "egress posture。",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chinese_reference_package_contract_update_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/reference-package.zh.md")
    expected_markers = (
        "契约更新（contract updates）",
        "评审（review）",
        "委派授权上下文（delegated authorization context）",
        "CLI 演示（CLI demos）",
        "会话（sessions）",
        "评测导出（eval exports）",
        "回放（replay）",
        "追踪导出脱敏（trace export redaction）",
        "命令摘要（command summaries）",
        "JSONL 工件（JSONL artifacts）",
        "生命周期检查（lifecycle inspection）",
        "运行时控制假设（runtime-control assumptions）",
        "文档守卫（docs guard）",
        "稳定验证错误（stable validation errors）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "最近的 contract updates",
        "适合 review",
        "delegated authorization context 会贯穿 CLI demos",
        "sessions、eval exports 与 replay",
        "trace export redaction 现在覆盖 command summaries 和 JSONL artifacts",
        "lifecycle inspection 会暴露 runtime-control assumptions",
        "docs guard 也固定了",
        "定义这些边界的 stable validation errors",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_multilingual_reference_package_runtime_scope_note_is_localized() -> None:
    russian_text = _read("docs/appendix/reference-package.md")
    chinese_text = _read("docs/appendix/reference-package.zh.md")

    assert "Каноническая область выполнения сценариев" in russian_text
    assert "исполняемую базовую линию" in russian_text
    assert "записывающих возможностей" in russian_text
    assert "контрольными линзами покрытия" in russian_text
    assert "поиск, память, свежесть" in russian_text
    assert "трассы, эскалацию" in russian_text

    assert "支持分诊（support-triage）的运行时锚点" in chinese_text
    assert "追踪/会话 ID（trace/session IDs）" in chinese_text
    assert "正文叙事（prose）" in chinese_text
    assert "规范案例运行时范围" in chinese_text
    assert "支持分诊（Support triage）" in chinese_text
    assert "可运行基线（runnable baseline）" in chinese_text
    assert "写入能力（write capabilities）" in chinese_text
    assert "事故协调（Incident coordination）" in chinese_text
    assert "覆盖视角（coverage lenses）" in chinese_text
    assert "检索（retrieval）" in chinese_text
    assert "追踪（traces）" in chinese_text
    assert "附录模式" in chinese_text
    assert "追踪模式与事件目录" in chinese_text
    assert "评测数据集模式与打分契约" in chinese_text
    assert "策略包模式与审批契约" in chinese_text
    assert "生命周期工件模式" in chinese_text
    assert "生命周期模式看受治理工件链接" in chinese_text
    assert "运行时控制模式" in chinese_text

    forbidden_markers = (
        "Канонический runtime-scope сценариев",
        "исполняемую базовую линию (runnable baseline)",
        "записывающих возможностей (write capabilities)",
        "линзами покрытия (coverage lenses)",
        "поиск (retrieval)",
        "трассы (traces)",
        "как runnable baseline для write capabilities",
        "остаются coverage lenses",
        "проверяет retrieval, memory",
        "traces, escalation, notification side effects",
        "как runnable configs",
        "support-triage 的运行时锚点",
        "审批等待、trace/session IDs",
        "不只是 prose",
        "支持分流（Support triage）",
        "事件协调（Incident coordination）",
        "作为 runnable baseline，用来承载 write capabilities",
        "仍是同一架构的 coverage lenses",
        "检查 retrieval、memory",
        "检查 traces、escalation",
        "做成 runnable configs",
        "附录 Schema",
        "追踪 Schema 与事件目录",
        "评测数据集 Schema 与打分契约",
        "策略包 Schema 与审批契约",
        "生命周期工件 Schema",
        "生命周期 Schema 看受治理工件链接",
        "运行时控制 Schema",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_policy_bundle_schema_surfaces_three_canonical_policy_cases() -> None:
    required_markers = (
        "Canonical policy cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "write-capability approval policy",
        "idempotency evidence",
        "duplicate-ticket recovery controls",
        "retrieval policy",
        "memory write rules",
        "freshness checks",
        "access control",
        "knowledge provenance",
        "escalation rules",
        "notification side effects",
        "response ownership",
        "post-incident learning gates",
    )
    checked_files = (
        "docs/appendix/policy-bundle-schema.md",
        "docs/appendix/policy-bundle-schema.en.md",
        "docs/appendix/policy-bundle-schema.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_chinese_policy_bundle_support_triage_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/policy-bundle-schema.zh.md")
    expected_markers = (
        "支持分流（support-triage）",
        "网关（gateway）",
        "追踪（trace）",
        "策略包（policy bundle）",
        "调和（reconciliation）",
        "发布复核（rollout review）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "对 support-triage 来说",
        "人工审批、gateway 和 trace",
        "policy bundle 可以",
        "没有 reconciliation 的重试",
        "rollout review 检查的是",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chinese_policy_bundle_sandbox_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/policy-bundle-schema.zh.md")
    expected_markers = (
        "由沙箱（sandbox）支撑的路径",
        "沙箱配置文件契约（sandbox profile contract）",
        "复核（review）",
        "工作区（workspace）",
        "shell/文件系统权限（shell/filesystem permissions）",
        "快照/恢复行为（snapshot/resume behavior）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "由 sandbox 支撑的路径",
        "指向 sandbox profile contract",
        "经过 review；否则 workspace",
        "shell/filesystem permissions 与 snapshot/resume behavior",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chinese_policy_bundle_validation_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/policy-bundle-schema.zh.md")
    expected_markers = (
        "门禁（gate）",
        "控制包（control bundle）的输入形状",
        "控制配置验证（controls config validation）",
        "信号覆盖（signal overrides）",
        "畸形策略包（malformed policy bundle）",
        "控制评估（control assessment）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "同一个 gate 也会明确约束 control bundle 的输入形状",
        "controls config validation 会报告",
        "signal overrides 会报告",
        "区分 malformed policy bundle 与格式正确但评估失败的 control assessment",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chinese_policy_bundle_control_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/policy-bundle-schema.zh.md")
    expected_markers = (
        "运行时控制契约（runtime-control contracts）",
        "可执行门禁（Executable gate）",
        "控制包（control bundle）",
        "策略/控制失败（policy/control failures）",
        "能力清单漂移（capability inventory drift）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "与 runtime-control contracts 不再只是",
        "Executable gate `check-controls` 也让 control bundle 可审查",
        "会把 policy/control failures 和 capability inventory drift 分开",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_russian_policy_bundle_security_contract_labels_are_localized() -> None:
    russian_text = _read("docs/appendix/policy-bundle-schema.md")
    expected_markers = (
        "управляемому контракту отвечать на вопросы",
        "делегированные исполнители в схеме `orchestrator-workers`",
        "путь подтверждения с делегированием",
        "в поведении продукта",
        "в каких схемах оркестрации это можно использовать",
        "контракт авторизации описывает, от чьей идентичности и с какой "
        "делегированной областью действия вообще может быть выполнено действие",
        "контракт управления MCP описывает, из какого утвержденного реестра "
        "пришла возможность, кто владеет MCP-сервером, каким режимом "
        "авторизации она защищена и что делать, если обнаружен теневой путь MCP",
        "политика контрактов проверяющего описывает, каким контрактам "
        "проверяющего вообще можно доверять для оценивания высокого риска, "
        "доказательств раскатки и решений по заверению",
        "каким контрактам проверяющего можно доверять для оценивания высокого "
        "риска или доказательств раскатки",
    )
    forbidden_markers = (
        "governed contract отвечать на вопросы",
        "delegated workers в `orchestrator-workers` approval или delegated "
        "authorization context",
        "delegated approval path уже существует в product behavior",
        "в каких orchestration patterns это можно использовать",
        "authorization contract описывает",
        "MCP governance contract описывает",
        "approved registry",
        "кто owner у MCP server",
        "auth mode",
        "shadow MCP path",
        "verifier contract policy описывает",
        "каким verifier contracts можно доверять",
        "high-risk grading",
        "rollout evidence",
        "assurance decisions",
    )

    for expected_marker in expected_markers:
        assert expected_marker in russian_text, expected_marker
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in russian_text, forbidden_marker


def test_multilingual_policy_bundle_case_note_is_localized() -> None:
    russian_path = "docs/appendix/policy-bundle-schema.md"
    russian_text = _read(russian_path)
    chinese_text = _read("docs/appendix/policy-bundle-schema.zh.md")

    for marker in (
        "Canonical policy cases",
        "Пакет политик (policy bundle)",
        "write-capability approval policy",
        "idempotency evidence",
        "политики поиска (retrieval policy)",
        "правил эскалации (escalation rules)",
    ):
        _assert_file_contains(russian_path, marker)

    assert "规范策略案例" in chinese_text
    assert "策略包（policy bundle）" in chinese_text
    assert "写入能力审批策略（write-capability approval policy）" in chinese_text
    assert "幂等证据（idempotency evidence）" in chinese_text
    assert "检索策略（retrieval policy）" in chinese_text
    assert "升级规则（escalation rules）" in chinese_text
    assert "追踪模式与事件目录" in chinese_text
    assert "评测数据集模式与打分契约" in chinese_text
    assert "生命周期工件模式" in chinese_text
    assert "追踪模式和评测模式那两页" in chinese_text
    assert "生产级模式还应该补什么" in chinese_text

    forbidden_markers = (
        "Policy bundle не должен выглядеть",
        "во всех трех canonical cases",
        "требует write-capability approval policy",
        "требует retrieval policy",
        "требует escalation rules",
        "三个 canonical cases 的 policy bundle",
        "需要 write-capability approval policy",
        "需要 retrieval policy",
        "需要 escalation rules",
        "追踪 Schema 与事件目录",
        "评测数据集 Schema 与打分契约",
        "生命周期工件 Schema",
        "追踪 Schema 和评测 Schema 那两页",
        "生产级 Schema 还应该补什么",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_approval_schema_surfaces_three_canonical_approval_cases() -> None:
    expected_markers_by_file = {
        "docs/appendix/approval-schema.md": (
            "Канонические сценарии подтверждений",
            "Триаж обращений поддержки",
            "Внутренний ассистент знаний",
            "Координация инцидентов",
            "явного подтверждения человеком",
            "idempotency_key",
            "доказательств восстановления после дубля тикета",
            "записей в память",
            "исключений контроля доступа",
            "решений о видимости источников",
            "следа подтверждений",
            "полномочий эскалации",
            "побочных эффектов уведомлений",
            "передачи владения ответом",
            "обновлений обучения после инцидента",
        ),
        "docs/appendix/approval-schema.en.md": (
            "Canonical approval cases",
            "Support triage",
            "Internal knowledge assistant",
            "Incident coordination",
            "explicit human approval",
            "idempotency_key",
            "duplicate-ticket recovery evidence",
            "memory writes",
            "access-control exceptions",
            "source visibility decisions",
            "approval trail",
            "escalation authority",
            "notification side effects",
            "response ownership transfer",
            "post-incident learning updates",
        ),
        "docs/appendix/approval-schema.zh.md": (
            "规范审批案例",
            "支持分流",
            "内部知识助手",
            "事件协调",
            "明确的人工审批",
            "idempotency_key",
            "重复工单恢复证据",
            "记忆写入",
            "访问控制例外",
            "来源可见性决策",
            "审批轨迹",
            "升级权限",
            "通知副作用",
            "响应归属转移",
            "事件后学习更新",
        ),
    }

    for path, expected_markers in expected_markers_by_file.items():
        text = _read(path)
        for expected_marker in expected_markers:
            assert expected_marker in text, (path, expected_marker)


def test_chinese_approval_schema_sandbox_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/approval-schema.zh.md")
    expected_markers = (
        "由沙箱（sandbox）支撑的动作",
        "工作区物化（workspace materialization）",
        "权限（permissions）",
        "快照/恢复策略（snapshot/resume policy）",
        "由沙箱（sandbox）支撑的审批",
        "沙箱配置文件（sandbox profile）",
        "工作区条目（workspace entries）",
        "沙箱配置文件契约（sandbox profile contract）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "由 sandbox 支撑的动作",
        "workspace materialization、permissions",
        "snapshot/resume policy，而不只是业务载荷",
        "由 sandbox 支撑的审批隐藏了 sandbox profile",
        "workspace entries 或 permissions",
        "动作由 sandbox 支撑",
        "看到 sandbox profile contract、workspace entries",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chinese_approval_schema_support_triage_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/approval-schema.zh.md")
    expected_markers = (
        "支持分诊（support-triage）案例",
        "审批者（approver）",
        "批准（approve）",
        "载荷（payload）",
        "审计记录（audit record）",
        "键（key）",
        "复核（review）",
        "盲目重试（blind retry）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "在 support-triage 案例中",
        "approver 按下 approve",
        "在 payload 旁",
        "audit record 会把同一个 key",
        "让 review 能区分",
        "blind retry 之后",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chinese_approval_schema_lineage_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/approval-schema.zh.md")
    expected_markers = (
        "审批条目（approval entry）",
        "可运行演示（demo）",
        "审批脉络（approval lineage）",
        "能力会话状态（capability-session state）",
        "委派权限（delegated authority）",
        "重复写入意图（duplicate-write intent）",
        "最终审批状态（approval status）",
        "审批/会话脉络（Approval/session lineage）",
        "委派授权证据（delegated-authorization evidence）",
        "审批或能力会话状态（approval or capability-session states）",
        "未知模式或状态（mode/status）",
        "会话导出（session exports）",
        "子智能体继承（subagent inheritance）",
        "子智能体（child agent）",
        "审批路径（approval path）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "每条 approval entry",
        "可运行 demo",
        "保留可见的 approval lineage",
        "capability-session state、delegated authority",
        "duplicate-write intent 与最终 approval status",
        "Approval/session lineage 也会用",
        "拒绝不受支持的 delegated-authorization evidence",
        "approval 或 capability-session states",
        "未知 mode 或 status",
        "session exports 旁边",
        "subagent inheritance 设为",
        "delegated authority 不会流入 child agent",
        "approval path 明确点名",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chinese_approval_schema_policy_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/approval-schema.zh.md")
    expected_markers = (
        "审批运行策略（approval operating policy）",
        "顶层形状（top-level shape）",
        "委派动作（delegated actions）",
        "证据（evidence）必须保持可见",
        "委派（delegation）",
        "子智能体（subagents）",
        "策略加载器（Policy loader）",
        "评审者（reviewer）",
        "升级（escalation）",
        "委派授权证据（delegated-authorization evidence）",
        "类型安全（type-safety）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "明确 approval operating policy",
        "校验 top-level shape",
        "评审 delegated actions",
        "哪些 evidence 必须保持可见",
        "delegation 是否可以传递给 subagents",
        "Policy loader 也会用",
        "保持 reviewer、escalation 与 delegated-authorization evidence 的 type-safety",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_multilingual_approval_schema_case_note_is_localized() -> None:
    russian_text = _read("docs/appendix/approval-schema.md")
    chinese_text = _read("docs/appendix/approval-schema.zh.md")

    assert "Канонические сценарии подтверждений" in russian_text
    assert "Запись подтверждения нужна не только для пути записи" in russian_text
    assert "явного подтверждения человеком" in russian_text
    assert "исключений контроля доступа" in russian_text
    assert "следа подтверждений" in russian_text

    assert "规范审批案例" in chinese_text
    assert "审批记录（approval record）" in chinese_text
    assert "写入路径（write path）" in chinese_text
    assert "明确的人工审批（explicit human approval）" in chinese_text
    assert "访问控制例外（access-control exceptions）" in chinese_text
    assert "审批轨迹（approval trail）" in chinese_text
    assert "策略包模式与审批契约" in chinese_text
    assert "追踪模式与事件目录" in chinese_text
    assert "生命周期工件模式" in chinese_text
    assert "审批模式回答的就是" in chinese_text
    assert "为什么要单独有审批模式" in chinese_text
    assert "它和追踪模式的关系" in chinese_text

    forbidden_markers = (
        "Запись подтверждения (approval record)",
        "пути записи (write path)",
        "явного подтверждения человеком (explicit human approval)",
        "исключений контроля доступа (access-control exceptions)",
        "следа подтверждений (approval trail)",
        "Approval record нужен не только для write path",
        "требует explicit human approval",
        "требует approval trail для escalation authority",
        "Approval record 不只服务于 write path",
        "需要 explicit human approval",
        "需要一条 approval trail",
        "策略包 Schema 与审批契约",
        "追踪 Schema 与事件目录",
        "生命周期工件 Schema",
        "审批 Schema 回答的就是",
        "为什么要单独有审批 Schema",
        "最小可用的审批 Schema",
        "追踪 Schema 和生命周期工件",
        "它和追踪 Schema 的关系",
        "审批 Schema 回答的是另一层",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_trace_schema_surfaces_three_canonical_trace_cases() -> None:
    required_markers = (
        "Canonical trace cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "approval events",
        "idempotency_key",
        "tool side effects",
        "duplicate-ticket recovery evidence",
        "retrieval spans",
        "memory access",
        "source attribution",
        "freshness checks",
        "access control decisions",
        "escalation timeline",
        "notification side effects",
        "response ownership",
        "handoff events",
        "post-incident learning",
    )
    checked_files = (
        "docs/appendix/trace-schema.md",
        "docs/appendix/trace-schema.en.md",
        "docs/appendix/trace-schema.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_chinese_trace_schema_mcp_a2a_verdict_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/trace-schema.zh.md")
    expected_markers = (
        "生产追踪（production trace）",
        "MCP 威胁模型证据（MCP threat-model evidence）",
        "MCP 威胁模型（MCP threat model）词汇表",
        "允许/拒绝决策（allow/deny decision）",
        "载荷（payload）",
        "A2A 交接信任契约（A2A handoff trust contract）",
        "验证器裁决记录（verifier verdict record）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "production trace 应记录",
        "记录 MCP threat-model evidence",
        "MCP threat model 词汇表",
        "最终 allow/deny decision",
        "payload 应保留 A2A handoff trust contract",
        "承载 verifier verdict record",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chinese_trace_schema_threat_and_governance_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/trace-schema.zh.md")
    expected_markers = (
        "统一智能体威胁证据模型（unified agent threat evidence model）",
        "证据标记（evidence markers）",
        "威胁行（threat rows）",
        "追踪（traces）检查",
        "散文说明（prose）",
        "治理动作记录字段（governance action record fields）",
        "遥测（telemetry）",
        "仪表板信号（dashboard signal）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "保留 unified agent threat evidence model",
        "中的 evidence markers",
        "让 threat rows 能通过 traces 检查",
        "停留在 prose",
        "记录 governance action record fields",
        "让 telemetry 变成",
        "只是 dashboard signal",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chinese_trace_schema_support_and_memory_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/trace-schema.zh.md")
    expected_markers = (
        "支持分流（support-triage）案例",
        "最终结果（outcome）",
        "追踪（trace）应显示",
        "调和（reconciliation）",
        "记忆投毒复核（memory poisoning review）",
        "记忆模式（memory schema）",
        "记忆投毒复核字段（memory poisoning review fields）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "在 support-triage 案例里",
        "最终 outcome 应该",
        "trace 应显示",
        "没有 reconciliation 的情况下",
        "对于 memory poisoning review 中的",
        "trace 应保留与 memory schema",
        "相同的 memory poisoning review fields",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chinese_trace_schema_sandbox_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/trace-schema.zh.md")
    expected_markers = (
        "由沙箱（sandbox）支撑的路径",
        "工作区（workspace）",
        "权限（permissions）",
        "快照/恢复证据复核（snapshot/resume evidence review）",
        "发布（rollout）或评测（eval）",
        "复核证据（review evidence）",
        "状态字段（state fields）",
        "沙箱状态字段（sandbox state fields）",
        "shell/文件系统能力（shell/filesystem capabilities）",
        "快照（snapshot）",
        "运行（runs）",
        "事件（event）",
        "关联载荷（linked payload）",
        "发布/评测证据（rollout/eval evidence）",
        "工作区条目（workspace entries）",
        "追踪证据（trace evidence）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "由 sandbox 支撑的路径被评审时",
        "记录 workspace、permissions",
        "对于由 sandbox 支撑的运行",
        "如果 rollout 或 eval 要求",
        "指向 review evidence，而不只是 state fields",
        "sandbox state fields，用于",
        "物化 workspace、使用 shell/filesystem capabilities",
        "从 snapshot 继续的 runs",
        "event 或 linked payload",
        "snapshot/resume policy 的 rollout/eval evidence",
        "关于 workspace entries、permissions",
        "trace evidence？",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chinese_trace_schema_replay_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/trace-schema.zh.md")
    expected_markers = (
        "分诊（triage）",
        "原始 JSONL 转储（raw JSONL dump）",
        "载荷（payload）",
        "重放（replay）",
        "重复写入键（key）",
        "新运行（new run）",
        "追踪重放（Trace replay）",
        "证据（evidence）",
        "种子（seed）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "可用于 triage",
        "不只是 raw JSONL dump",
        "`tool_execution` payload",
        "说明 replay 是",
        "重复写入 key 的新 run",
        "Trace replay 会先校验这些 evidence",
        "作为新 run 的 seed",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chinese_trace_schema_tool_model_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/trace-schema.zh.md")
    expected_markers = (
        "参考载荷（reference payloads）",
        "操作元数据字段（operational metadata fields）",
        "工具请求/结果模型校验（Tool request/result model validation）",
        "追踪边界（trace boundary）",
        "畸形工具调用（malformed tool calls）",
        "畸形工具结果（malformed tool results）",
        "`span_name` 和 `duration_ms`",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "当前 reference payloads",
        "operational metadata fields：",
        "`span_name`, and `duration_ms`",
        "Tool request/result model validation 也属于",
        "trace boundary：malformed tool calls",
        "malformed tool results 会以",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_multilingual_trace_schema_case_note_is_localized() -> None:
    russian_path = "docs/appendix/trace-schema.md"
    russian_text = _read(russian_path)
    chinese_text = _read("docs/appendix/trace-schema.zh.md")

    for marker in (
        "Канонические сценарии трассировки",
        "акцентов трассировки (trace emphases)",
        "события подтверждений (approval events)",
        "спаны поиска (retrieval spans)",
        "таймлайн эскалации (escalation timeline)",
    ):
        _assert_file_contains(russian_path, marker)

    assert "规范追踪案例" in chinese_text
    assert "追踪重点（trace emphases）" in chinese_text
    assert "审批事件（approval events）" in chinese_text
    assert "检索跨度（retrieval spans）" in chinese_text
    assert "升级时间线（escalation timeline）" in chinese_text
    assert "评测数据集模式与打分契约" in chinese_text
    assert "策略包模式与审批契约" in chinese_text
    assert "生命周期工件模式" in chinese_text
    assert "为什么需要显式的追踪模式" in chinese_text
    assert "生产级模式还应该补什么" in chinese_text

    forbidden_markers = (
        "Три canonical cases требуют разных trace emphases",
        "связывает approval events",
        "сохранять retrieval spans",
        "показывать escalation timeline",
        "三个 canonical cases 需要不同的 trace emphases",
        "把 approval events",
        "保留 retrieval spans",
        "展示 escalation timeline",
        "真正的追踪 Schema",
        "为什么需要显式的追踪 Schema",
        "显式的追踪 Schema",
        "生产级 Schema 还应该补什么",
        "Schema 版本字段",
        "Schema 版本化",
        "评测数据集 Schema 与打分契约",
        "策略包 Schema 与审批契约",
        "生命周期工件 Schema",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_trace_schema_includes_agent_threat_evidence_markers() -> None:
    required_markers = (
        "agent_threat_evidence",
        "unified agent threat evidence",
        "prompt_boundary_event",
        "rejected_instruction_trace",
        "tool_output_sanitized",
        "untrusted_content_marker",
        "policy_decision_trace",
        "retrieval_source_id",
        "freshness_score",
        "quarantine_event",
        "memory_record_id",
        "validation_state",
        "rollback_replay_evidence",
        "tool_call_id",
        "approval_record",
        "argument_validation_result",
        "subject_id",
        "delegation_trace_id",
        "caller_callee_identity_check",
        "step_budget_event",
        "stop_reason",
        "escalation_decision",
        "tenant_id",
        "egress_decision",
        "redaction_dlp_result",
        "cost_budget_event",
        "rate_limit_decision",
        "circuit_breaker_state",
        "handoff_id",
        "containment_state",
        "verifier_verdict",
        "artifact_digest",
        "registry_decision",
        "sandbox_profile_id",
        "decision_trace_id",
        "immutable_log_pointer",
        "evidence_completeness_flag",
    )
    checked_files = (
        "docs/appendix/trace-schema.md",
        "docs/appendix/trace-schema.en.md",
        "docs/appendix/trace-schema.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_trace_schema_includes_mcp_tool_risk_review_fields() -> None:
    required_markers = (
        "mcp_tool_risk_review",
        "threat_class",
        "mcp_server_id",
        "tool_contract_version",
        "registry_owner",
        "scope_review",
        "quarantine_state",
        "evidence_refs",
        "tool poisoning",
        "rug pull attack",
        "tool shadowing",
        "confused deputy",
        "over-scoped tokens",
        "data exfiltration through legitimate channels",
        "supply-chain attack",
        "replay/tampering",
        "sandbox escape",
    )
    checked_files = (
        "docs/appendix/trace-schema.md",
        "docs/appendix/trace-schema.en.md",
        "docs/appendix/trace-schema.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_trace_schema_includes_a2a_handoff_trust_contract_fields() -> None:
    required_markers = (
        "a2a_handoff",
        "A2A handoff trust contract",
        "agent_identity",
        "delegation_chain",
        "allowed_collaboration_graph",
        "inter_agent_authorization",
        "policy_inheritance",
        "non_repudiation",
        "failure_attribution",
    )
    checked_files = (
        "docs/appendix/trace-schema.md",
        "docs/appendix/trace-schema.en.md",
        "docs/appendix/trace-schema.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_trace_schema_includes_memory_poisoning_decision_fields() -> None:
    required_markers = (
        "memory_write_decision",
        "memory poisoning",
        "write_trust_boundary",
        "activation_policy",
        "contamination_scope",
        "policy_influence",
        "provenance_check",
        "quarantine_state",
        "rollback_ref",
    )
    checked_files = (
        "docs/appendix/trace-schema.md",
        "docs/appendix/trace-schema.en.md",
        "docs/appendix/trace-schema.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_trace_schema_includes_governance_action_event_fields() -> None:
    required_markers = (
        "governance_action",
        "governance action record",
        "governance_action_id",
        "source_signal",
        "decision_owner",
        "action_state",
        "evidence_refs",
        "review_deadline",
        "policy_decision_feedback",
        "containment_decision",
        "rollout_gate_input",
        "incident_response_trigger",
        "registry_update_signal",
    )
    checked_files = (
        "docs/appendix/trace-schema.md",
        "docs/appendix/trace-schema.en.md",
        "docs/appendix/trace-schema.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_trace_schema_includes_verifier_verdict_record_fields() -> None:
    required_markers = (
        "verifier verdict record",
        "verdict_id",
        "verifier_id",
        "verifier_contract_version",
        "input_refs",
        "process_score",
        "outcome_score",
        "failure_attribution",
        "blocking_decision",
        "comparison_baseline",
        "reviewer_override",
        "evidence_refs",
    )
    checked_files = (
        "docs/appendix/trace-schema.md",
        "docs/appendix/trace-schema.en.md",
        "docs/appendix/trace-schema.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_eval_schema_surfaces_three_canonical_eval_cases() -> None:
    required_markers = (
        "Canonical eval cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "approval gates",
        "idempotency evidence",
        "retry behavior",
        "duplicate-ticket recovery",
        "retrieval freshness",
        "source attribution",
        "memory provenance",
        "access control",
        "grounded answer quality",
        "escalation timing",
        "notification side effects",
        "response ownership",
        "handoff quality",
        "post-incident learning regressions",
    )
    checked_files = (
        "docs/appendix/eval-schema.md",
        "docs/appendix/eval-schema.en.md",
        "docs/appendix/eval-schema.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_chinese_eval_schema_verdict_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/eval-schema.zh.md")
    assert "验证器裁决记录（verifier verdict record）字段" in chinese_text
    assert "这些 verifier verdict record 字段" not in chinese_text


def test_chinese_eval_schema_sandbox_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/eval-schema.zh.md")
    expected_markers = (
        "沙箱（sandbox）支撑的路径",
        "工作区物化（workspace materialization）",
        "shell/文件系统权限（shell/filesystem permissions）",
        "网络/密钥姿态（network/secrets posture）",
        "快照/恢复策略（snapshot/resume policy）",
        "运行时设置（runtime settings）",
        "发布（rollout）",
        "打分规则（grading rule）",
        "工作区（workspace）",
        "权限（permissions）",
        "快照/恢复证据（snapshot/resume evidence）",
        "沙箱配置文件契约（sandbox profile contract）",
        "工作区条目（workspace entries）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "对由 sandbox 支撑的路径很重要",
        "检查 workspace materialization",
        "shell/filesystem permissions、network/secrets posture",
        "snapshot/resume policy 是否",
        "隐含的 runtime settings",
        "在 rollout 中要求",
        "没有 grading rule 去检查 workspace",
        "检查 sandbox profile contract、workspace entries",
        "snapshot/resume evidence？",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chinese_eval_schema_gate_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/eval-schema.zh.md")
    expected_markers = (
        "评测门禁（eval gate）",
        "支持分诊（support-triage）案例",
        "专门评测（eval）",
        "提示词/模型/适配器（prompt/model/adapter）",
        "阻断发布（rollout）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "重复工单线索的 eval gate",
        "贯穿的 support-triage 案例",
        "专门 eval 复现",
        "新的 prompt/model/adapter 版本",
        "阻断 rollout",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chinese_eval_schema_scenario_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/eval-schema.zh.md")
    expected_markers = (
        "导出契约（Export contract）",
        "顶层摘要（top-level summary）",
        "审批支撑场景（approval-backed scenarios）",
        "内置场景（built-in scenarios）",
        "标签（label）",
        "标签（labels）",
        "预期结果（expected outcome）",
        "阻断型（blocking）",
        "打分规则（grading rule）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "Export contract 是有意保持具体的",
        "top-level summary 包含",
        "approval-backed scenarios 也会",
        "built-in scenarios 包括",
        "duplicate_ticket_eval_passed` label",
        "blocking `duplicate_ticket_guard` grading rule",
        "labels 的 `profile_memory`",
        "session_evals` labels",
        "作为 expected outcome",
        "sandbox_profile_review` label",
        "sandbox_profile_reviewed` expected outcome",
        "blocking `sandbox_profile_review` grading rule",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chinese_eval_schema_export_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/eval-schema.zh.md")
    expected_markers = (
        "打包导出契约（Bundled export contract）",
        "会话评测配置验证（Session eval config validation）",
        "畸形评测规格（malformed eval specs）",
        "失败的评测结果（failed eval results）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "Bundled export contract 是有意保持具体的",
        "Session eval config validation 也会用",
        "把 malformed eval specs 与 failed eval results 区分开",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_multilingual_eval_schema_case_note_is_localized() -> None:
    russian_path = "docs/appendix/eval-schema.md"
    russian_text = _read(russian_path)
    chinese_text = _read("docs/appendix/eval-schema.zh.md")

    for marker in (
        "Канонические сценарии оценок",
        "Набор оценок (eval dataset)",
        "регрессию дублей тикетов (duplicate-ticket regression)",
        "шлюзы подтверждения (approval gates)",
        "свежесть поиска (retrieval freshness)",
        "сроки эскалации (escalation timing)",
    ):
        _assert_file_contains(russian_path, marker)

    assert "规范评测案例" in chinese_text
    assert "评测数据集（eval dataset）" in chinese_text
    assert "重复工单回归（duplicate-ticket regression）" in chinese_text
    assert "审批门禁（approval gates）" in chinese_text
    assert "检索新鲜度（retrieval freshness）" in chinese_text
    assert "升级时序（escalation timing）" in chinese_text
    assert "追踪模式与事件目录" in chinese_text
    assert "策略包模式与审批契约" in chinese_text
    assert "生命周期工件模式" in chinese_text

    forbidden_markers = (
        "Eval dataset должен покрывать",
        "только duplicate-ticket regression",
        "проверяет approval gates",
        "проверяет retrieval freshness",
        "проверяет escalation timing",
        "Eval dataset 不应该只覆盖 duplicate-ticket regression",
        "检查 approval gates",
        "检查 retrieval freshness",
        "检查 escalation timing",
        "追踪 Schema 与事件目录",
        "策略包 Schema 与审批契约",
        "生命周期工件 Schema",
        "追踪 Schema 那一页",
        "追踪 Schema 描述实际运行行为",
        "评测数据集 Schema 描述期望行为",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_eval_schema_includes_verifier_verdict_record_fields() -> None:
    required_markers = (
        "verifier verdict record",
        "verifier_outputs",
        "verdict_id",
        "verifier_id",
        "verifier_contract_version",
        "input_refs",
        "blocking_decision",
        "comparison_baseline",
        "reviewer_override",
        "verifier_evidence_refs",
    )
    checked_files = (
        "docs/appendix/eval-schema.md",
        "docs/appendix/eval-schema.en.md",
        "docs/appendix/eval-schema.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_incident_record_schema_surfaces_three_canonical_incident_cases() -> None:
    english_markers = (
        "Canonical incident cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "corrective paths",
        "unknown write",
        "idempotency_key",
        "duplicate-ticket recovery",
        "eval/update gate",
        "stale retrieval",
        "source attribution gaps",
        "memory contamination",
        "access control breach",
        "knowledge provenance repair",
        "escalation delay",
        "notification side effects",
        "response ownership gap",
        "handoff failure",
        "post-incident learning update",
    )
    russian_markers = (
        "Канонические сценарии инцидентов",
        "Триаж обращений поддержки",
        "Внутренний ассистент знаний",
        "Координация инцидентов",
        "пути исправления",
        "неизвестным исходом",
        "idempotency_key",
        "восстановление после дубля тикета",
        "шлюз оценки/обновления",
        "устаревший поиск",
        "разрывы привязки к источникам",
        "загрязнение памяти",
        "нарушение контроля доступа",
        "восстановление происхождения знаний",
        "задержку эскалации",
        "побочные эффекты уведомлений",
        "разрыв владения ответом",
        "сбой передачи управления",
        "обновление обучения после инцидента",
    )

    _assert_files_contain_all(("docs/appendix/incident-record-schema.md",), russian_markers)
    _assert_files_contain_all(("docs/appendix/incident-record-schema.en.md",), english_markers)
    _assert_files_contain_all(("docs/appendix/incident-record-schema.zh.md",), english_markers)


def test_multilingual_incident_record_case_note_is_localized() -> None:
    russian_text = _read("docs/appendix/incident-record-schema.md")
    chinese_text = _read("docs/appendix/incident-record-schema.zh.md")

    assert "Канонические сценарии инцидентов" in russian_text
    assert "Запись инцидента должна оставлять разные пути исправления" in russian_text
    assert "запись с неизвестным исходом" in russian_text
    assert "устаревший поиск" in russian_text
    assert "задержку эскалации" in russian_text
    assert "Схема записи инцидента и связи с разбором" in russian_text

    assert "规范事故案例" in chinese_text
    assert "事故记录（incident record）" in chinese_text
    assert "纠正路径（corrective paths）" in chinese_text
    assert "结果未知的写入（unknown write）" in chinese_text
    assert "陈旧检索（stale retrieval）" in chinese_text
    assert "升级延迟（escalation delay）" in chinese_text
    assert "追踪模式与事件目录" in chinese_text
    assert "策略包模式与审批契约" in chinese_text
    assert "审批请求与决策记录模式" in chinese_text
    assert "变更评审与发布门禁模式" in chinese_text
    assert "生命周期工件模式" in chinese_text
    assert "这套最小模式通常围绕两个实体展开" in chinese_text

    forbidden_markers = (
        "Incident record должен оставлять",
        "разные corrective paths",
        "фиксирует unknown write",
        "фиксирует stale retrieval",
        "фиксирует escalation delay",
        "Incident record 应为三个 canonical cases",
        "不同 corrective paths",
        "记录 unknown write",
        "记录 stale retrieval",
        "记录 escalation delay",
        "追踪 Schema 与事件目录",
        "策略包 Schema 与审批契约",
        "审批请求与决策记录 Schema",
        "变更评审与发布门禁 Schema",
        "生命周期工件 Schema",
        "这套最小 Schema 通常围绕两个实体展开",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_chinese_incident_record_duplicate_ticket_example_is_localized() -> None:
    chinese_text = _read("docs/appendix/incident-record-schema.zh.md")

    assert "支持分流（support-triage）事故" in chinese_text
    assert "在 support-triage 事故里" not in chinese_text


def test_russian_incident_record_schema_prefers_reader_facing_terms() -> None:
    russian_text = _read("docs/appendix/incident-record-schema.md")

    expected_markers = (
        'title: "Несанкционированный путь записи ticket_write во время вводного прогона"',
        "с решением о поэтапном выпуске и его волной",
        "какой пакет политик был активен",
        "какая учетная запись или другой принципал реально выполнил действие",
        "несколько базовых механизмов, которые делают эту схему полезной на практике",
    )
    forbidden_markers = (
        'title: "Unauthorized ticket_write path during onboarding run"',
        "с дисциплиной выпуска",
        "какой набор политик был активен",
        "какой принципал реально выполнил действие",
        "несколько примитивов, которые делают эту схему полезной на практике",
    )

    for marker in expected_markers:
        assert marker in russian_text, marker
    for marker in forbidden_markers:
        assert marker not in russian_text, marker


def test_change_rollout_schema_surfaces_three_canonical_rollout_cases() -> None:
    required_markers = (
        "Canonical rollout cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "readiness signals",
        "duplicate-ticket eval pass",
        "rollback plan",
        "approval readiness",
        "idempotency evidence",
        "retrieval freshness window",
        "source attribution review",
        "memory provenance review",
        "access control signoff",
        "escalation drill",
        "notification side effects review",
        "response ownership readiness",
        "post-incident learning gate",
    )
    checked_files = (
        "docs/appendix/change-rollout-schema.md",
        "docs/appendix/change-rollout-schema.en.md",
        "docs/appendix/change-rollout-schema.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_chinese_change_rollout_sandbox_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/change-rollout-schema.zh.md")
    expected_markers = (
        "由沙箱（sandbox）支撑的执行",
        "沙箱配置文件契约（sandbox profile contract）",
        "工作区物化（workspace materialization）",
        "权限（permissions）",
        "快照/恢复策略（snapshot/resume policy）",
        "沙箱配置文件（sandbox profile）变更",
        "工作区条目（workspace entries）",
        "shell/文件系统权限（shell/filesystem permissions）",
        "快照/恢复行为（snapshot/resume behavior）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "由 sandbox 支撑的执行",
        "sandbox profile contract 是否也进入评审",
        "包括 workspace materialization、permissions",
        "snapshot/resume policy；",
        "sandbox profile 变更会在发布前被检查",
        "改变 workspace entries、shell/filesystem permissions",
        "snapshot/resume behavior 时",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chinese_change_rollout_canary_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/change-rollout-schema.zh.md")
    expected_markers = (
        "支持分诊金丝雀发布（support-triage canary）",
        "门禁（gate）",
        "结果（outcome）",
        "盲目重试（blind retry）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "对 support-triage canary 来说",
        "gate 不应只检查",
        "outcome 是一个工单副作用",
        "只有 blind retry 没有回来时",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chinese_change_rollout_review_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/change-rollout-schema.zh.md")
    expected_markers = (
        "已评审变更表面（reviewed change surface）",
        "发布证据（release evidence）",
        "必需评审者（required reviewers）",
        "发布评审（release review）",
        "降级路径（degraded-path）",
        "重复工单就绪度（duplicate-ticket readiness）",
        "变更加载器（Change loader）",
        "畸形评审记录（malformed review records）",
        "失败门禁（gates）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "定义 reviewed change surface",
        "等 release evidence",
        "标记为 required reviewers",
        "让 release review 能把",
        "与 degraded-path、duplicate-ticket readiness 区分开",
        "Change loader 也会把 malformed review records 与失败的 gates 区分开",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chinese_change_rollout_gate_input_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/change-rollout-schema.zh.md")
    expected_markers = (
        "门禁输入（gate inputs）",
        "必需证据（required evidence）",
        "运行时信号覆盖（Runtime signal overrides）",
        "直接评估输入（direct assessment inputs）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "把 gate inputs 具体化",
        "校验：required evidence 包括",
        "Runtime signal overrides 和 direct assessment inputs 也会被校验",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chinese_change_rollout_runtime_policy_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/change-rollout-schema.zh.md")
    expected_markers = (
        "发布策略（rollout policy）",
        "规范化（normalize）",
        "模式（schema）",
        "发布自动化（release automation）",
        "重复工单证据（duplicate-ticket evidence）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "internally rollout policy",
        "把 `block_if` normalize",
        "与 schema 中",
        "让 release automation 单独看到 duplicate-ticket evidence",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_multilingual_change_rollout_case_note_is_localized() -> None:
    russian_path = "docs/appendix/change-rollout-schema.md"
    russian_text = _read(russian_path)
    chinese_text = _read("docs/appendix/change-rollout-schema.zh.md")

    for marker in (
        "Канонические сценарии раскатки",
        "Шлюз раскатки",
        "сигналы готовности (readiness signals)",
        "плана отката (rollback plan)",
        "окна свежести поиска (retrieval freshness window)",
        "тренировки эскалации (escalation drill)",
    ):
        _assert_file_contains(russian_path, marker)

    assert "规范发布案例" in chinese_text
    assert "发布门禁（rollout gate）" in chinese_text
    assert "就绪信号（readiness signals）" in chinese_text
    assert "回滚计划（rollback plan）" in chinese_text
    assert "检索新鲜度窗口（retrieval freshness window）" in chinese_text
    assert "升级演练（escalation drill）" in chinese_text
    assert "评测数据集模式与打分契约" in chinese_text
    assert "生命周期工件模式" in chinese_text
    assert "策略包模式与审批契约" in chinese_text
    assert "变更与发布门禁模式回答的就是" in chinese_text
    assert "为什么需要单独的模式层" in chinese_text

    forbidden_markers = (
        "Rollout gate должен проверять",
        "разные readiness signals",
        "требует duplicate-ticket eval pass",
        "требует retrieval freshness window",
        "требует escalation drill",
        "Rollout gate 应为三个 canonical cases",
        "检查不同 readiness signals",
        "需要 duplicate-ticket eval pass",
        "需要 retrieval freshness window",
        "需要 escalation drill",
        "评测数据集 Schema 与打分契约",
        "生命周期工件 Schema",
        "策略包 Schema 与审批契约",
        "变更与发布门禁 Schema 回答的就是",
        "为什么需要单独的 Schema 层",
        "机器可读的 Schema 层",
        "最小可用的 Schema 层",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_russian_change_rollout_core_terms_are_localized() -> None:
    russian_text = _read("docs/appendix/change-rollout-schema.md")
    expected_markers = (
        "проверки изменений и шлюза поэтапного выпуска",
        "изменения в политике, промптах, маршрутизации моделей, поиске или доступе к инструментам",
        "У change review в агентной системе",
        "инженерное ревью в pull request",
        "результаты оценивания в CI",
        "решение о поэтапном выпуске в чате или устно на созвоне",
        "несколько ответственных",
        "высокорисковые действия",
        "поэтапный выпуск",
        "машинно-читаемый слой",
        "дисциплину эксплуатации",
        "кто это проверил",
        "рабочий факт",
    )
    for expected_marker in expected_markers:
        assert expected_marker in russian_text, expected_marker

    forbidden_markers = (
        "change review и rollout gate",
        "policy, prompt, model routing, retrieval или tool exposure",
        "agent system change review",
        "engineering review в pull request",
        "safety review где-то в отдельном документе",
        "eval results в CI",
        "rollout decision в чате или устно на созвоне",
        "несколько owners",
        "high-risk actions",
        "staged rollout",
        "machine-readable слой",
        "operational discipline",
        "кто это reviewed",
        "operational факт",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in russian_text, forbidden_marker


def test_lifecycle_artifact_schema_surfaces_three_canonical_lifecycle_cases() -> None:
    required_markers = (
        "Canonical lifecycle cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "artifact chains",
        "change record",
        "approved artifact bundle",
        "approval record",
        "eval dataset",
        "rollout gate",
        "retirement plan",
        "duplicate-ticket guard",
        "retrieval policy",
        "memory policy",
        "source provenance",
        "access-control review",
        "knowledge-base replacement plan",
        "escalation policy",
        "notification capability",
        "response ownership map",
        "handoff artifact",
        "post-incident learning retirement or replacement plan",
    )
    checked_files = (
        "docs/appendix/lifecycle-artifact-schema.md",
        "docs/appendix/lifecycle-artifact-schema.en.md",
        "docs/appendix/lifecycle-artifact-schema.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_chinese_lifecycle_artifact_sandbox_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/lifecycle-artifact-schema.zh.md")
    expected_markers = (
        "由沙箱（sandbox）支撑的执行",
        "沙箱配置文件契约（sandbox profile contract）",
        "发布身份（release identity）",
        "沙箱配置文件复核证据（sandbox profile review evidence）",
        "追踪事件（trace event）",
        "评测/发布证据（eval/rollout evidence）",
        "发布（rollout）要求",
        "包（bundle）、追踪（trace）或评测工件（eval artifact）",
        "工作区（workspace）",
        "权限（permissions）",
        "快照/恢复策略（snapshot/resume policy）",
        "复核证据链接（review-evidence link）",
        "复核证据（review evidence）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "由 sandbox 支撑的执行",
        "以及 sandbox profile contract",
        "当 release identity 包含",
        "sandbox profile review evidence，包括",
        "trace event、`workspace_manifest_ref`",
        "指向 eval/rollout evidence",
        "当 rollout 要求",
        "从 bundle、trace 或 eval artifact",
        "还原 sandbox profile review evidence",
        "bundle 写了 `sandbox_profile`",
        "workspace、permissions 与 snapshot/resume policy",
        "review-evidence link。",
        "review evidence？",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chinese_lifecycle_artifact_intro_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/lifecycle-artifact-schema.zh.md")
    expected_markers = (
        "生命周期工件（lifecycle artifact）",
        "支持分诊（support-triage）",
        "工件包（bundle）",
        "重复工单防护（duplicate-ticket guard）",
        "证据（evidence）",
        "审批记录（approval record）",
        "追踪（trace）",
        "发布门禁（rollout gate）",
        "事故复盘（incident review）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "重复工单线索的 lifecycle artifact",
        "对 support-triage 来说",
        "bundle 不只应该",
        "保留 duplicate-ticket guard 的 evidence",
        "approval record、带有",
        "和 rollout gate",
        "这样 incident review 可以",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chinese_lifecycle_artifact_loader_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/lifecycle-artifact-schema.zh.md")
    expected_markers = (
        "生命周期工件加载器（Lifecycle artifact loaders）",
        "畸形发布状态输入（malformed release-state inputs）",
        "YAML 键（YAML keys）",
        "身份/归属（identity/ownership）",
        "工件评审证据（artifact review evidence）",
        "畸形证据映射（malformed evidence maps）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "Lifecycle artifact loaders 会把 malformed release-state inputs",
        "非字符串 YAML keys",
        "缺失的 identity/ownership",
        "artifact review evidence 会用",
        "拒绝 malformed evidence maps",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chinese_lifecycle_artifact_retirement_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/lifecycle-artifact-schema.zh.md")
    expected_markers = (
        "退役表面（retiring surface）",
        "受控交接（controlled handover）",
        "退役（retirement）",
        "控制项（controls）",
        "归属（ownership）",
        "留存证据（retained evidence）",
        "归档列表（Archive list）",
        "记录（records）",
        "可执行摘要（Executable summary）",
        "退役步骤（retirement steps）",
        "降级路径（degraded-path）",
        "重复工单评审（duplicate-ticket review）",
        "证据包（evidence bundles）",
        "畸形退役步骤覆盖（malformed retirement step overrides）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "标识 retiring surface",
        "表示 controlled handover",
        "等 controls",
        "保留 ownership 和 retained evidence",
        "Archive list 会列出",
        "可审查的 records",
        "Executable summary `check-retirement`",
        "未完成的 retirement steps",
        "为 degraded-path 与 duplicate-ticket review",
        "准确 evidence bundles",
        "malformed retirement step overrides 会失败为",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chinese_lifecycle_artifact_bundle_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/lifecycle-artifact-schema.zh.md")
    expected_markers = (
        "参考运行时（runtime）",
        "契约（contract）",
        "包身份（bundle identity）",
        "问责（accountability）",
        "畸形身份与来源证明字段（malformed identity and provenance fields）",
        "证据链（evidence chain）",
        "证据引用（evidence refs）",
        "承载发布的文件（release-bearing files）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "参考 runtime 会把这个 contract 保存",
        "描述 bundle identity 与 accountability",
        "malformed identity 和 provenance fields",
        "evidence chain 这样的 evidence refs",
        "列出 release-bearing files",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_multilingual_lifecycle_artifact_case_note_is_localized() -> None:
    russian_path = "docs/appendix/lifecycle-artifact-schema.md"
    russian_text = _read(russian_path)
    chinese_text = _read("docs/appendix/lifecycle-artifact-schema.zh.md")

    for marker in (
        "Канонические сценарии жизненного цикла",
        "Артефакты жизненного цикла",
        "цепочки артефактов (artifact chains)",
        "запись изменения (change record)",
        "политику поиска (retrieval policy)",
        "политику эскалации (escalation policy)",
    ):
        _assert_file_contains(russian_path, marker)

    assert "规范生命周期案例" in chinese_text
    assert "生命周期工件（lifecycle artifacts）" in chinese_text
    assert "工件链（artifact chains）" in chinese_text
    assert "变更记录（change record）" in chinese_text
    assert "检索策略（retrieval policy）" in chinese_text
    assert "升级策略（escalation policy）" in chinese_text
    assert "追踪模式与事件目录" in chinese_text
    assert "评测数据集模式与打分契约" in chinese_text
    assert "策略包模式与审批契约" in chinese_text
    assert "运行时控制模式与契约版本" in chinese_text
    assert "这个模式直接支撑了几章核心内容" in chinese_text

    forbidden_markers = (
        "Lifecycle artifacts должны удерживать",
        "разные artifact chains",
        "связывает change record",
        "связывает retrieval policy",
        "связывает escalation policy",
        "Lifecycle artifacts 应为三个 canonical cases",
        "不同 artifact chains",
        "把 change record",
        "连接 retrieval policy",
        "连接 escalation policy",
        "追踪 Schema 回答的是",
        "评测 Schema 回答的是",
        "生命周期工件 Schema 回答的就是",
        "追踪 Schema 与事件目录",
        "评测数据集 Schema 与打分契约",
        "策略包 Schema 与审批契约",
        "运行时控制 Schema 与契约版本",
        "这个 Schema 直接支撑了几章核心内容",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_russian_lifecycle_artifact_core_terms_are_localized() -> None:
    russian_text = _read("docs/appendix/lifecycle-artifact-schema.md")
    expected_markers = (
        "записи изменений (change records)",
        "утвержденные пакеты артефактов (approved artifact bundles)",
        "планы вывода из эксплуатации (retirement plans)",
        "карты замены (replacement mappings)",
        "связи между схемами управления средой исполнения и версиями контрактов",
        "рабочие подтверждения и решения жизненного цикла",
        "правила прерывания, истечения и повторной инициализации сессий возможностей",
        "правила делегированного разрешения",
        "контракты проверяющего, рубрики оценивания и правила связи доказательств",
        "структурированные артефакты передачи управления",
        "управление изменениями",
        "разбор инцидента",
    )
    for expected_marker in expected_markers:
        assert expected_marker in russian_text, expected_marker

    forbidden_markers = (
        "- change records;",
        "- approved artifact bundles;",
        "- retirement plans;",
        "- replacement mappings;",
        "- runtime-control schemas и contract-version linkages;",
        "- operational approvals и lifecycle decisions;",
        (
            "- capability-session interruption, expiry и re-initialization rules, "
            "если они уже входят в runtime contract;"
        ),
        (
            "- delegated authorization rules, assumptions про principal binding и "
            "revoke behavior, если они уже входят в runtime contract;"
        ),
        (
            "- verifier contracts, grading rubrics и rules для evidence linkage, "
            "если release или assurance зависят от verifier output;"
        ),
        (
            "- структурированные handoff artifacts, если длинная работа пересекает "
            "границу context reset или role handoff."
        ),
        "change management быстро разваливается",
        "incident review превращается",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in russian_text, forbidden_marker


def test_russian_lifecycle_artifact_reader_facing_contract_terms_are_localized() -> None:
    russian_text = _read("docs/appendix/lifecycle-artifact-schema.md")

    expected_markers = (
        "с привязкой к подтверждению",
        "проверяемую поверхность",
        "идентичность пакета и подотчетность",
        "ошибки в полях идентичности и происхождения",
        "ссылки на доказательства",
        "файлы конфигурации релиза",
        "Загрузчики артефактов жизненного цикла",
        "слоя артефактов жизненного цикла",
        "высокорисковое изменение",
    )
    for expected_marker in expected_markers:
        assert expected_marker in russian_text, expected_marker

    forbidden_markers = (
        "approval-bound, stateful capability sessions",
        "reviewed surface",
        "bundle identity и accountability",
        "malformed identity и provenance fields",
        "evidence refs",
        "release-bearing files",
        "Lifecycle artifact loaders",
        "healthy lifecycle artifact layer",
        "high-risk change",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in russian_text, forbidden_marker


def test_memory_retrieval_schema_surfaces_three_canonical_memory_cases() -> None:
    expected_markers_by_file = {
        "docs/appendix/memory-retrieval-schema.md": (
            "Канонические сценарии памяти",
            "Триаж обращений поддержки",
            "Внутренний ассистент знаний",
            "Координация инцидентов",
            "границы памяти",
            "контекст запрашивающего",
            "состояние тикета",
            "idempotency_key",
            "короткоживущие рабочие заметки",
            "свежести поиска",
            "привязки к источникам",
            "фильтров арендатора",
            "происхождения памяти",
            "контроля доступа",
            "таймлайн инцидента",
            "владение ответом",
            "сводки передачи управления",
            "статус эскалации",
            "уроки после инцидента",
            "временный шум инцидента",
            "долговечную истину",
        ),
        "docs/appendix/memory-retrieval-schema.en.md": (
            "Canonical memory cases",
            "Support triage",
            "Internal knowledge assistant",
            "Incident coordination",
            "memory boundaries",
            "requester context",
            "ticket state",
            "idempotency_key",
            "short-lived working notes",
            "retrieval freshness",
            "source attribution",
            "tenant filters",
            "memory provenance",
            "access control",
            "incident timeline",
            "response ownership",
            "handoff summaries",
            "escalation status",
            "post-incident lessons",
            "transient incident noise",
            "durable truth",
        ),
        "docs/appendix/memory-retrieval-schema.zh.md": (
            "规范记忆案例",
            "支持分流",
            "内部知识助手",
            "事件协调",
            "记忆边界",
            "请求者上下文",
            "工单状态",
            "idempotency_key",
            "短期工作笔记",
            "检索新鲜度",
            "来源归因",
            "租户过滤器",
            "记忆来源",
            "访问控制",
            "事件时间线",
            "响应归属",
            "交接摘要",
            "升级状态",
            "临时事件噪声",
            "事件后经验",
            "持久真相",
        ),
    }

    for path, expected_markers in expected_markers_by_file.items():
        text = _read(path)
        for expected_marker in expected_markers:
            assert expected_marker in text, (path, expected_marker)


def test_chinese_memory_retrieval_poisoning_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/memory-retrieval-schema.zh.md")
    expected_markers = (
        "记忆投毒复核（memory poisoning review）",
        "记忆投毒复核字段（memory poisoning review fields）",
        "候选写入（candidate write）",
        "安全对象（security object）",
        "检索载荷（retrieval payload）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "对于 memory poisoning review",
        "通过 memory poisoning review fields",
        "candidate write 描述成",
        "security object，而不只是 retrieval payload",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chinese_memory_retrieval_candidate_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/memory-retrieval-schema.zh.md")
    expected_markers = (
        "候选修订模式（Memory candidate revision mode）",
        "候选置信度（Memory candidate confidence）",
        "候选字段（Memory candidate field）",
        "记忆查询字段（Memory lookup field）",
        "记忆查询限制（Memory lookup limit）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "以及 `Memory candidate revision mode must be a string`",
        "和 `Memory candidate confidence must be a number` 和",
        "和 `Memory candidate field must be a string: {field}` 和",
        "和 `Memory lookup field must be a string: {field}` 和",
        "和 `Memory lookup limit must be an integer` 和",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chinese_memory_retrieval_direct_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/memory-retrieval-schema.zh.md")
    expected_markers = (
        "直接记忆存储构造（direct memory store construction）",
        "畸形注入记录（malformed injected records）",
        "畸形直接候选（malformed direct candidates）",
        "直接构造记录（direct construction records）",
        "稳定错误（stable errors）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "direct memory store construction 会用",
        "拒绝 malformed injected records",
        "拒绝 malformed direct candidates",
        "direct construction records 使用稳定 errors",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chinese_memory_retrieval_machine_schema_label_is_localized() -> None:
    chinese_text = _read("docs/appendix/memory-retrieval-schema.zh.md")
    expected_markers = (
        "机器可检查的记忆模式（machine-checkable memory schema）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "连接到 machine-checkable memory schema",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_chinese_memory_retrieval_seed_labels_are_localized() -> None:
    chinese_text = _read("docs/appendix/memory-retrieval-schema.zh.md")
    expected_markers = (
        "种子记录（seed record）",
        "打包类别（bundled kinds）",
        "演示（demo）",
        "检索过滤（retrieval filtering）",
        "记录脉络（lineage）",
        "来源（sources）",
        "来源信息（provenance）",
        "检索示例（retrieval examples）",
        "信任与持久化级别（trust and persistence levels）",
        "非资料种子内容（Non-profile seed content）",
        "策略式事实（policy-like fact）",
        "工作笔记（working note）",
        "加载器（Loader）",
        "形状（shape）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "每条 seed record",
        "bundled kinds 是",
        "因此 demo 可以同时展示 retrieval filtering 与记录 lineage",
        "session_state` sources",
        "这样的 provenance",
        "让 retrieval examples 能呈现不同的 trust 与 persistence levels",
        "Non-profile seed content 还包括 policy-like fact",
        "以及 working note",
        "Loader 也会校验这个 shape",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_multilingual_memory_retrieval_case_note_is_localized() -> None:
    russian_text = _read("docs/appendix/memory-retrieval-schema.md")
    chinese_text = _read("docs/appendix/memory-retrieval-schema.zh.md")

    assert "Канонические сценарии памяти" in russian_text
    assert "Контракт памяти и поиска должен отделять разные границы памяти" in russian_text
    assert "контекст запрашивающего" in russian_text
    assert "свежести поиска" in russian_text
    assert "временный шум инцидента" in russian_text

    assert "规范记忆案例" in chinese_text
    assert "记忆与检索契约（memory and retrieval contract）" in chinese_text
    assert "记忆边界（memory boundaries）" in chinese_text
    assert "请求者上下文（requester context）" in chinese_text
    assert "检索新鲜度（retrieval freshness）" in chinese_text
    assert "临时事件噪声（transient incident noise）" in chinese_text
    assert "追踪模式与事件目录" in chinese_text
    assert "评测数据集模式与打分契约" in chinese_text
    assert "生命周期工件模式" in chinese_text

    forbidden_markers = (
        "Контракт памяти и поиска (memory and retrieval contract)",
        "границы памяти (memory boundaries)",
        "контекст запрашивающего (requester context)",
        "свежести поиска (retrieval freshness)",
        "временный шум инцидента (transient incident noise)",
        "Memory and retrieval contract должен",
        "разные memory boundaries",
        "хранит requester context",
        "требует retrieval freshness",
        "transient incident noise в durable truth",
        "Memory and retrieval contract 应为三个 canonical cases",
        "不同 memory boundaries",
        "保存 requester context",
        "需要 retrieval freshness",
        "transient incident noise 变成 durable truth",
        "追踪 Schema 与事件目录",
        "生命周期工件 Schema",
        "记忆与检索 Schema 回答的就是",
        "追踪 Schema 和参考运行时",
        "它和追踪 Schema 的关系",
        "评测数据集 Schema 与打分契约",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_postmortem_template_surfaces_three_canonical_postmortem_cases() -> None:
    expected_markers_by_file = {
        "docs/appendix/postmortem-template.md": (
            "Канонические сценарии разбора инцидентов",
            "Триаж обращений поддержки",
            "Внутренний ассистент знаний",
            "Координация инцидентов",
            "классы отказов",
            "контур управления",
            "корневую причину дубля тикета",
            "область подтверждения",
            "idempotency_key",
            "сдерживание побочного эффекта",
            "исправление оценки и поэтапного выпуска",
            "устаревший источник",
            "свежесть поиска",
            "происхождение памяти",
            "разрыв контроля доступа",
            "исправление базы знаний",
            "задержку эскалации",
            "побочные эффекты уведомлений",
            "разрыв владения ответом",
            "сбой передачи управления",
            "обновление обучения после инцидента",
        ),
        "docs/appendix/postmortem-template.en.md": (
            "Canonical postmortem cases",
            "Support triage",
            "Internal knowledge assistant",
            "Incident coordination",
            "failure classes",
            "control loop",
            "duplicate-ticket root cause",
            "approval scope",
            "idempotency_key",
            "side-effect containment",
            "eval/rollout correction",
            "stale source",
            "retrieval freshness",
            "memory provenance",
            "access-control gap",
            "knowledge-base correction",
            "escalation delay",
            "notification side effects",
            "response ownership gap",
            "handoff breakdown",
            "post-incident learning update",
        ),
        "docs/appendix/postmortem-template.zh.md": (
            "规范事后复盘案例",
            "支持分流",
            "内部知识助手",
            "事件协调",
            "失败类别",
            "控制循环",
            "重复工单根因",
            "审批范围",
            "idempotency_key",
            "副作用遏制",
            "评测/发布修正",
            "陈旧来源",
            "检索新鲜度",
            "记忆来源",
            "访问控制缺口",
            "知识库修正",
            "升级延迟",
            "通知副作用",
            "响应归属缺口",
            "交接崩溃",
            "事件后学习更新",
        ),
    }

    for path, expected_markers in expected_markers_by_file.items():
        text = _read(path)
        for expected_marker in expected_markers:
            assert expected_marker in text, (path, expected_marker)


def test_multilingual_postmortem_template_case_note_is_localized() -> None:
    russian_text = _read("docs/appendix/postmortem-template.md")
    chinese_text = _read("docs/appendix/postmortem-template.zh.md")

    assert "Канонические сценарии разбора инцидентов" in russian_text
    assert "Разбор инцидента должен возвращать" in russian_text
    assert "классы отказов" in russian_text
    assert "контур управления" in russian_text
    assert "корневую причину дубля тикета" in russian_text
    assert "задержку эскалации" in russian_text

    assert "规范事后复盘案例" in chinese_text
    assert "事后复盘（postmortem）" in chinese_text
    assert "失败类别（failure classes）" in chinese_text
    assert "控制循环（control loop）" in chinese_text
    assert "重复工单根因（duplicate-ticket root cause）" in chinese_text
    assert "升级延迟（escalation delay）" in chinese_text
    assert "事故记录与事后复盘链接模式" in chinese_text
    assert "变更评审与发布门禁模式" in chinese_text
    assert "生命周期工件模式" in chinese_text

    forbidden_markers = (
        "Разбор инцидента (postmortem)",
        "классы отказов (failure classes)",
        "контур управления (control loop)",
        "корневую причину дубля тикета (duplicate-ticket root cause)",
        "задержку эскалации (escalation delay)",
        "Postmortem должен возвращать",
        "разные failure classes",
        "в control loop",
        "проверяет duplicate-ticket root cause",
        "проверяет stale source",
        "проверяет escalation delay",
        "Postmortem 应把三个 canonical cases",
        "不同 failure classes",
        "回流到 control loop",
        "检查 duplicate-ticket root cause",
        "检查 stale source",
        "检查 escalation delay",
        "事故记录与事后复盘链接 Schema",
        "变更评审与发布门禁 Schema",
        "生命周期工件 Schema",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_chinese_postmortem_duplicate_ticket_example_is_localized() -> None:
    chinese_text = _read("docs/appendix/postmortem-template.zh.md")
    expected_markers = (
        "支持分流（support-triage）事故",
        "旧工单写入器（ticket writer）的退役计划",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "对于 support-triage 事故",
        "旧 ticket writer 的退役计划",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_incident_response_playbook_surfaces_three_canonical_response_cases() -> None:
    expected_markers_by_file = {
        "docs/appendix/incident-response-playbook.md": (
            "Канонические сценарии реагирования",
            "Триаж обращений поддержки",
            "Внутренний ассистент знаний",
            "Координация инцидентов",
            "пути сдерживания",
            "записывающую возможность",
            "доказательства подтверждения",
            "idempotency_key",
            "статус побочного эффекта",
            "волну поэтапного выпуска",
            "область поиска",
            "приостанавливает записи в память",
            "происхождение источников",
            "доказательства границы арендатора",
            "решение контроля доступа",
            "статус эскалации",
            "побочные эффекты уведомлений",
            "владение ответом",
            "состояние передачи управления",
            "владельцем экстренного отката",
        ),
        "docs/appendix/incident-response-playbook.en.md": (
            "Canonical response cases",
            "Support triage",
            "Internal knowledge assistant",
            "Incident coordination",
            "containment paths",
            "write capability",
            "approval evidence",
            "idempotency_key",
            "side-effect status",
            "rollout wave",
            "retrieval scope",
            "pauses memory writes",
            "source provenance",
            "tenant boundary evidence",
            "access-control decision",
            "escalation status",
            "notification side effects",
            "response ownership",
            "handoff state",
            "emergency rollback owner",
        ),
        "docs/appendix/incident-response-playbook.zh.md": (
            "规范响应案例",
            "支持分流",
            "内部知识助手",
            "事件协调",
            "遏制路径",
            "写入能力",
            "审批证据",
            "idempotency_key",
            "副作用状态",
            "发布波次",
            "检索范围",
            "暂停记忆写入",
            "来源证明",
            "租户边界证据",
            "访问控制决策",
            "升级状态",
            "通知副作用",
            "响应归属",
            "交接状态",
            "紧急回滚负责人",
        ),
    }

    for path, expected_markers in expected_markers_by_file.items():
        text = _read(path)
        for expected_marker in expected_markers:
            assert expected_marker in text, (path, expected_marker)


def test_multilingual_incident_response_playbook_case_note_is_localized() -> None:
    russian_text = _read("docs/appendix/incident-response-playbook.md")
    chinese_text = _read("docs/appendix/incident-response-playbook.zh.md")

    assert "Канонические сценарии реагирования" in russian_text
    assert "Реагирование на инцидент должно выбирать" in russian_text
    assert "пути сдерживания" in russian_text
    assert "записывающую возможность" in russian_text
    assert "область поиска" in russian_text
    assert "статус эскалации" in russian_text

    assert "规范响应案例" in chinese_text
    assert "事件响应（incident response）" in chinese_text
    assert "遏制路径（containment paths）" in chinese_text
    assert "写入能力（write capability）" in chinese_text
    assert "检索范围（retrieval scope）" in chinese_text
    assert "暂停记忆写入动作（pauses memory writes）" in chinese_text
    assert "升级状态（escalation status）" in chinese_text
    assert "追踪模式与事件目录" in chinese_text
    assert "策略包模式与审批契约" in chinese_text
    assert "审批请求与决策记录模式" in chinese_text
    assert "变更评审与发布门禁模式" in chinese_text
    assert "生命周期工件模式" in chinese_text

    forbidden_markers = (
        "Реагирование на инцидент (incident response)",
        "пути сдерживания (containment paths)",
        "записывающую возможность (write capability)",
        "область поиска (retrieval scope)",
        "статус эскалации (escalation status)",
        "Incident response должен выбирать",
        "разные containment paths",
        "трех canonical cases",
        "замораживает write capability",
        "ограничивает retrieval scope",
        "фиксирует escalation status",
        "Incident response 应为三个 canonical cases",
        "选择不同 containment paths",
        "冻结 write capability",
        "收窄 retrieval scope",
        "暂停记忆写入（pauses memory writes）",
        "记录 escalation status",
        "追踪 Schema 与事件目录",
        "策略包 Schema 与审批契约",
        "审批请求与决策记录 Schema",
        "变更评审与发布门禁 Schema",
        "生命周期工件 Schema",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_chinese_incident_response_duplicate_ticket_example_is_localized() -> None:
    chinese_text = _read("docs/appendix/incident-response-playbook.zh.md")
    expected_markers = (
        "支持分流（support-triage）事故",
        "评测/发布门禁（eval/rollout gate）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "贯穿的 support-triage 事故",
        "转成 eval/rollout gate",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_policy_templates_surface_three_canonical_policy_template_cases() -> None:
    english_markers = (
        "Canonical policy template cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "operational starters",
        "governed write capability",
        "approval boundary",
        "idempotency key",
        "traceable write intent",
        "duplicate-ticket guard",
        "role-scoped retrieval",
        "source references",
        "grounding checks",
        "tenant boundaries",
        "access-denied behavior",
        "controlled handoffs",
        "current owner",
        "notification approval",
        "risky remediation disabled by default",
        "incident trace coverage",
    )
    russian_markers = (
        "Канонические сценарии шаблонов политик",
        "Триаж обращений поддержки",
        "Внутренний ассистент знаний",
        "Координация инцидентов",
        "операционными заготовками",
        "управляемой пишущей возможности",
        "границы подтверждения",
        "ключа идемпотентности",
        "отслеживаемого намерения записи",
        "защиты от дубля тикета",
        "ролевых ограничений поиска",
        "ссылок на источники",
        "проверок привязки к источникам",
        "границ арендатора",
        "поведения при отказе доступа",
        "управляемых передач",
        "текущего владельца",
        "подтверждения уведомлений",
        "опасного исправления, выключенного по умолчанию",
        "покрытия трасс инцидента",
    )
    checked_files = (
        "docs/appendix/policy-templates.md",
        "docs/appendix/policy-templates.en.md",
        "docs/appendix/policy-templates.zh.md",
    )

    _assert_files_contain_all(("docs/appendix/policy-templates.md",), russian_markers)
    _assert_files_contain_all(("docs/appendix/policy-templates.en.md",), english_markers)
    _assert_files_contain_all(("docs/appendix/policy-templates.zh.md",), english_markers)
    deprecated_markers = (
        "Support Triage Agent",
        "Internal Knowledge Agent",
        "Incident Coordination Agent",
    )
    for path in checked_files:
        text = _read(path)
        for marker in deprecated_markers:
            assert marker not in text, (path, marker)


def test_chinese_policy_templates_duplicate_ticket_example_is_localized() -> None:
    chinese_text = _read("docs/appendix/policy-templates.zh.md")
    expected_markers = (
        "支持分流（support-triage）案例",
        "强制幂等键（idempotency key）",
        "发布/评测门禁（rollout/eval gate）",
    )
    for expected_marker in expected_markers:
        assert expected_marker in chinese_text, expected_marker

    forbidden_markers = (
        "贯穿的 support-triage 案例",
        "强制 idempotency key",
        "捕获重复建单的 rollout/eval gate",
    )
    for forbidden_marker in forbidden_markers:
        assert forbidden_marker not in chinese_text, forbidden_marker


def test_multilingual_policy_templates_case_note_is_localized() -> None:
    russian_text = _read("docs/appendix/policy-templates.md")
    chinese_text = _read("docs/appendix/policy-templates.zh.md")

    assert "Канонические сценарии шаблонов политик" in russian_text
    assert "операционными заготовками для трех канонических сценариев" in russian_text
    assert "управляемой пишущей возможности" in russian_text
    assert "ролевых ограничений поиска" in russian_text
    assert "управляемых передач" in russian_text

    assert "规范策略模板案例" in chinese_text
    assert "运营起点（operational starters）" in chinese_text
    assert "受治理的写入能力（governed write capability）" in chinese_text
    assert "按角色限定的检索（role-scoped retrieval）" in chinese_text
    assert "受控交接（controlled handoffs）" in chinese_text

    forbidden_markers = (
        "являются operational starters",
        "трех canonical cases",
        "governed write capability, approval boundary",
        "role-scoped retrieval, source references",
        "controlled handoffs, current owner",
        "三个 canonical cases 的 operational starters",
        "从 governed write capability",
        "从 role-scoped retrieval",
        "从 controlled handoffs",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_registry_operations_handbook_surfaces_three_canonical_registry_cases() -> None:
    required_markers_by_file = {
        "docs/appendix/registry-operations-handbook.md": (
            "Канонические сценарии реестра",
            "Триаж обращений поддержки",
            "Внутренний ассистент знаний",
            "Координация инцидентов",
            "якоря ответственности",
            "возможности записи",
            "режима подтверждения",
            "средств идемпотентности",
            "пакета политик",
            "связи с выводом из эксплуатации",
            "владельца корпуса",
            "политики извлечения",
            "границ арендатора",
            "проверки происхождения источников",
            "ритма проверки свежести",
            "владельца инцидентной роли",
            "полномочий эскалации",
            "владельца канала уведомлений",
            "владельца экстренного отката",
            "возможностей только на случай чрезвычайной ситуации",
        ),
        "docs/appendix/registry-operations-handbook.en.md": (
            "Canonical registry cases",
            "Support triage",
            "Internal knowledge assistant",
            "Incident coordination",
            "accountability anchors",
            "write capability",
            "approval mode",
            "idempotency controls",
            "policy bundle",
            "retirement linkage",
            "corpus owner",
            "retrieval policy",
            "tenant scope",
            "source provenance review",
            "freshness review cadence",
            "incident role owner",
            "escalation authority",
            "notification channel ownership",
            "emergency rollback owner",
            "emergency-only capabilities",
        ),
        "docs/appendix/registry-operations-handbook.zh.md": (
            "Canonical registry cases",
            "Support triage",
            "Internal knowledge assistant",
            "Incident coordination",
            "accountability anchors",
            "write capability",
            "approval mode",
            "idempotency controls",
            "policy bundle",
            "retirement linkage",
            "corpus owner",
            "retrieval policy",
            "tenant scope",
            "source provenance review",
            "freshness review cadence",
            "incident role owner",
            "escalation authority",
            "notification channel ownership",
            "emergency rollback owner",
            "emergency-only capabilities",
        ),
    }

    for path, required_markers in required_markers_by_file.items():
        _assert_files_contain_all((path,), required_markers)


def test_multilingual_registry_operations_case_note_is_localized() -> None:
    russian_text = _read("docs/appendix/registry-operations-handbook.md")
    chinese_text = _read("docs/appendix/registry-operations-handbook.zh.md")

    assert "Канонические сценарии реестра" in russian_text
    assert "Запись реестра должна фиксировать" in russian_text
    assert "якоря ответственности" in russian_text
    assert "возможности записи" in russian_text
    assert "владельца корпуса" in russian_text
    assert "владельца экстренного отката" in russian_text

    assert "规范注册表案例" in chinese_text
    assert "注册表记录（registry record）" in chinese_text
    assert "责任锚点（accountability anchors）" in chinese_text
    assert "支持分诊（Support triage）" in chinese_text
    assert "写入能力（write capability）" in chinese_text
    assert "语料负责人（corpus owner）" in chinese_text
    assert "事故协调（Incident coordination）" in chinese_text
    assert "事故角色负责人（incident role owner）" in chinese_text
    assert "紧急回滚负责人（emergency rollback owner）" in chinese_text
    assert "生命周期工件模式" in chinese_text
    assert "变更评审与发布门禁模式" in chinese_text

    forbidden_markers = (
        "Registry record должен фиксировать",
        "разные accountability anchors",
        "требует owner для write capability",
        "требует corpus owner",
        "требует incident role owner",
        "(registry record)",
        "(accountability anchors)",
        "(write capability)",
        "(corpus owner)",
        "(emergency rollback owner)",
        "Registry record 应为三个 canonical cases",
        "不同 accountability anchors",
        "支持分流（Support triage）",
        "事件协调（Incident coordination）",
        "事件角色负责人（incident role owner）",
        "需要 write capability",
        "需要 corpus owner",
        "需要 incident role owner",
        "生命周期工件 Schema",
        "变更评审与发布门禁 Schema",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_tool_failure_recovery_surfaces_three_canonical_recovery_cases() -> None:
    english_markers = (
        "Canonical recovery cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "failure surfaces",
        "side_effect_unknown",
        "idempotency lookup",
        "duplicate-ticket prevention",
        "manual reconciliation",
        "eval/rollout regression",
        "stale retrieval",
        "source lookup failure",
        "access-denied recovery",
        "memory write rollback",
        "grounded-answer recheck",
        "notification partial delivery",
        "escalation retry",
        "owner handoff repair",
        "emergency rollback decision",
        "post-incident learning capture",
    )
    russian_markers = (
        "Канонические сценарии восстановления",
        "Триаж обращений поддержки",
        "Внутренний ассистент знаний",
        "Координация инцидентов",
        "поверхности отказа",
        "side_effect_unknown",
        "ключу идемпотентности",
        "предотвращении дубля тикета",
        "ручной сверке",
        "регрессии оценки/поэтапного выпуска",
        "устаревшем поиске",
        "сбое поиска источника",
        "восстановлении после отказа доступа",
        "откате записи в память",
        "повторной проверке обоснованного ответа",
        "частичной доставке уведомлений",
        "повторе эскалации",
        "исправлении передачи владельца",
        "решении об экстренном откате",
        "фиксации обучения после инцидента",
    )
    chinese_markers = (
        "Canonical recovery cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "failure surfaces",
        "side_effect_unknown",
        "idempotency lookup",
        "duplicate-ticket prevention",
        "manual reconciliation",
        "eval/rollout regression",
        "stale retrieval",
        "source lookup failure",
        "access-denied recovery",
        "memory write rollback",
        "grounded-answer recheck",
        "notification partial delivery",
        "escalation retry",
        "owner handoff repair",
        "emergency rollback decision",
        "post-incident learning capture",
    )

    _assert_files_contain_all(("docs/appendix/tool-failure-recovery.en.md",), english_markers)
    _assert_files_contain_all(("docs/appendix/tool-failure-recovery.md",), russian_markers)
    _assert_files_contain_all(("docs/appendix/tool-failure-recovery.zh.md",), chinese_markers)


def test_multilingual_tool_failure_recovery_case_note_is_localized() -> None:
    russian_text = _read("docs/appendix/tool-failure-recovery.md")
    chinese_text = _read("docs/appendix/tool-failure-recovery.zh.md")

    assert "Канонические сценарии восстановления" in russian_text
    assert "Ветка восстановления должна различать поверхности отказа" in russian_text
    assert "поиске по ключу идемпотентности" in russian_text
    assert "устаревшем поиске" in russian_text
    assert "частичной доставке уведомлений" in russian_text

    assert "规范恢复案例" in chinese_text
    assert "恢复分支（recovery branch）" in chinese_text
    assert "失败表面（failure surfaces）" in chinese_text
    assert "幂等性查找（idempotency lookup）" in chinese_text
    assert "陈旧检索（stale retrieval）" in chinese_text
    assert "通知部分送达（notification partial delivery）" in chinese_text
    assert "追踪模式与事件目录" in chinese_text
    assert "事故记录与事后复盘链接模式" in chinese_text

    russian_forbidden = (
        "recovery branch",
        "failure surfaces",
        "idempotency lookup",
        "duplicate-ticket prevention",
        "stale retrieval",
        "source lookup failure",
        "notification partial delivery",
        "escalation retry",
        "owner handoff repair",
        "emergency rollback decision",
        "post-incident learning capture",
        "Recovery branch должен",
        "failure surfaces для трех canonical cases",
        "idempotency lookup, duplicate-ticket prevention",
        "stale retrieval, source lookup failure",
        "notification partial delivery, escalation retry",
    )
    chinese_forbidden = (
        "Recovery branch 应区分三个 canonical cases",
        "idempotency lookup、duplicate-ticket prevention",
        "stale retrieval、source lookup failure",
        "notification partial delivery、escalation retry",
        "追踪 Schema 与事件目录",
        "事故记录与事后复盘链接 Schema",
    )

    for marker in russian_forbidden:
        assert marker not in russian_text
    for marker in chinese_forbidden:
        assert marker not in chinese_text


def test_memory_eval_patterns_surface_three_canonical_memory_eval_cases() -> None:
    english_markers = (
        "Canonical memory eval cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "state quality",
        "requester context carryover",
        "ticket state retrieval",
        "idempotency_key",
        "no-write decision",
        "duplicate-ticket regression",
        "retrieval freshness",
        "source attribution",
        "tenant isolation",
        "memory provenance",
        "grounded-answer quality",
        "incident timeline recall",
        "response ownership handoff",
        "escalation status",
        "noisy alert filtering",
        "post-incident lesson retention",
    )
    russian_markers = (
        "Канонические сценарии оценки памяти",
        "Триаж обращений поддержки",
        "Внутренний ассистент знаний",
        "Координация инцидентов",
        "качество состояния",
        "перенос контекста заявителя",
        "извлечение состояния тикета",
        "idempotency_key",
        "решение не выполнять запись",
        "регрессию дубля тикета",
        "свежесть поиска",
        "привязку к источнику",
        "изоляцию арендатора",
        "происхождение памяти",
        "качество обоснованного ответа",
        "восстановление хронологии инцидента",
        "передачу владения ответом",
        "статус эскалации",
        "фильтрацию шумных оповещений",
        "сохранение уроков после инцидента",
    )

    _assert_files_contain_all(("docs/appendix/memory-eval-patterns.md",), russian_markers)
    _assert_files_contain_all(("docs/appendix/memory-eval-patterns.en.md",), english_markers)
    _assert_files_contain_all(("docs/appendix/memory-eval-patterns.zh.md",), english_markers)


def test_multilingual_memory_eval_patterns_case_note_is_localized() -> None:
    russian_text = _read("docs/appendix/memory-eval-patterns.md")
    chinese_text = _read("docs/appendix/memory-eval-patterns.zh.md")

    assert "Канонические сценарии оценки памяти" in russian_text
    assert "Набор оценок памяти должен по-разному проверять качество состояния" in russian_text
    assert "перенос контекста заявителя" in russian_text
    assert "свежесть поиска" in russian_text
    assert "восстановление хронологии инцидента" in russian_text

    assert "规范记忆评测案例" in chinese_text
    assert "记忆评测套件（memory eval suite）" in chinese_text
    assert "状态质量（state quality）" in chinese_text
    assert "请求者上下文延续（requester context carryover）" in chinese_text
    assert "检索新鲜度（retrieval freshness）" in chinese_text
    assert "事件时间线回忆（incident timeline recall）" in chinese_text
    assert "评测数据集模式与打分契约" in chinese_text
    assert "记忆记录与检索契约模式" in chinese_text

    forbidden_markers = (
        "Memory eval suite должен",
        "state quality для трех canonical cases",
        "проверяет requester context carryover",
        "проверяет retrieval freshness",
        "проверяет incident timeline recall",
        "Memory eval suite 应为三个 canonical cases",
        "分别检查 state quality",
        "检查 requester context carryover",
        "检查 retrieval freshness",
        "检查 incident timeline recall",
        "评测数据集 Schema 与打分契约",
        "记忆记录与检索契约 Schema",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_causal_debugging_surfaces_three_canonical_causal_cases() -> None:
    english_markers = (
        "Canonical causal cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "decisive edges",
        "retrieved context",
        "approval decision",
        "idempotency_key",
        "tool execution",
        "duplicate-ticket cascade",
        "stale source",
        "retrieval filtering",
        "source attribution",
        "memory write",
        "access-control decision",
        "escalation trigger",
        "notification side effects",
        "handoff edge",
        "response ownership",
        "post-incident learning update",
    )
    russian_markers = (
        "Канонические причинные сценарии",
        "Триаж обращений поддержки",
        "Внутренний ассистент знаний",
        "Координация инцидентов",
        "решающие связи",
        "найденный контекст",
        "решение о подтверждении",
        "idempotency_key",
        "выполнение инструмента",
        "каскад дубля тикета",
        "устаревший источник",
        "фильтрацию поиска",
        "привязку к источнику",
        "запись в память",
        "решение контроля доступа",
        "триггер эскалации",
        "побочные эффекты уведомлений",
        "связь передачи управления",
        "владение ответом",
        "обновление обучения после инцидента",
    )

    _assert_files_contain_all(("docs/appendix/causal-debugging.md",), russian_markers)
    _assert_files_contain_all(("docs/appendix/causal-debugging.en.md",), english_markers)
    _assert_files_contain_all(("docs/appendix/causal-debugging.zh.md",), english_markers)


def test_multilingual_causal_debugging_case_note_is_localized() -> None:
    russian_text = _read("docs/appendix/causal-debugging.md")
    chinese_text = _read("docs/appendix/causal-debugging.zh.md")

    assert "Канонические причинные сценарии" in russian_text
    assert "Причинная отладка должна искать разные решающие связи" in russian_text
    assert "найденный контекст" in russian_text
    assert "устаревший источник" in russian_text
    assert "триггер эскалации" in russian_text

    assert "规范因果案例" in chinese_text
    assert "因果调试（causal debugging）" in chinese_text
    assert "决定性边（decisive edges）" in chinese_text
    assert "检索到的上下文（retrieved context）" in chinese_text
    assert "陈旧来源（stale source）" in chinese_text
    assert "升级触发器（escalation trigger）" in chinese_text
    assert "追踪模式与事件目录" in chinese_text
    assert "事故记录与事后复盘链接模式" in chinese_text

    forbidden_markers = (
        "Causal debugging должен искать",
        "разные decisive edges",
        "отделяет retrieved context",
        "отделяет stale source",
        "отделяет escalation trigger",
        "Causal debugging 应在三个 canonical cases",
        "不同 decisive edges",
        "区分 retrieved context",
        "区分 stale source",
        "区分 escalation trigger",
        "追踪 Schema 与事件目录",
        "事故记录与事后复盘链接 Schema",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_cheat_sheets_surface_three_canonical_checklist_cases() -> None:
    required_markers_by_file = {
        "docs/appendix/cheat-sheets.md": (
            "Канонические сценарии для проверочных списков",
            "Триаж обращений поддержки",
            "Внутренний ассистент знаний",
            "Координация инцидентов",
            "быстрый маршрут",
            "безопасности",
            "шлюза инструментов",
            "подтверждения",
            "идемпотентности",
            "проверки поэтапного выпуска",
            "память",
            "извлечение",
            "привязки к источникам",
            "границ арендатора",
            "проверок наблюдаемости",
            "разбора инцидента",
            "ответственности за реагирование",
            "обучения после инцидента",
        ),
        "docs/appendix/cheat-sheets.en.md": (
            "Canonical checklist cases",
            "Support triage",
            "Internal knowledge assistant",
            "Incident coordination",
            "fast route",
            "safety",
            "tool gateway",
            "approval",
            "idempotency",
            "rollout checks",
            "memory",
            "retrieval",
            "source grounding",
            "tenant boundary",
            "observability checks",
            "incident review",
            "response ownership",
            "post-incident learning checks",
        ),
        "docs/appendix/cheat-sheets.zh.md": (
            "Canonical checklist cases",
            "Support triage",
            "Internal knowledge assistant",
            "Incident coordination",
            "fast route",
            "safety",
            "tool gateway",
            "approval",
            "idempotency",
            "rollout checks",
            "memory",
            "retrieval",
            "source grounding",
            "tenant boundary",
            "observability checks",
            "incident review",
            "response ownership",
            "post-incident learning checks",
        ),
    }

    for path, required_markers in required_markers_by_file.items():
        _assert_files_contain_all((path,), required_markers)


def test_multilingual_cheat_sheet_canonical_case_note_is_localized() -> None:
    russian_text = _read("docs/appendix/cheat-sheets.md")
    chinese_text = _read("docs/appendix/cheat-sheets.zh.md")

    assert "Канонические сценарии для проверочных списков" in russian_text
    assert "блоки проверок как быстрый маршрут" in russian_text
    assert "Триаж обращений поддержки" in russian_text
    assert "Внутренний ассистент знаний" in russian_text
    assert "Координация инцидентов" in russian_text
    assert "безопасности, шлюза инструментов" in russian_text
    assert "памяти, извлечения" in russian_text
    assert "разбора инцидента" in russian_text

    assert "规范检查清单案例" in chinese_text
    assert "快速路线（fast route）" in chinese_text
    assert "支持分流（Support triage）" in chinese_text
    assert "内部知识助手（Internal knowledge assistant）" in chinese_text
    assert "事件协调（Incident coordination）" in chinese_text
    assert "安全（safety）、工具网关（tool gateway）" in chinese_text
    assert "记忆（memory）、检索（retrieval）" in chinese_text
    assert "事故复盘（incident review）" in chinese_text

    forbidden_markers = (
        "Используй эти checklist blocks как fast route",
        "начинается с safety, tool gateway, approval",
        "начинается с memory, retrieval, source grounding",
        "начинается с rollout, observability, incident review",
        "(Canonical checklist cases)",
        "(fast route)",
        "(canonical cases)",
        "(Support triage)",
        "(Internal knowledge assistant)",
        "(Incident coordination)",
        "(safety)",
        "(tool gateway)",
        "(approval)",
        "(rollout checks)",
        "(memory)",
        "(retrieval)",
        "(source grounding)",
        "(tenant boundary)",
        "(observability checks)",
        "(incident review)",
        "(response ownership)",
        "(post-incident learning checks)",
        "Use these checklist blocks 作为三个 canonical cases 的 fast route",
        "从 safety、tool gateway、approval",
        "从 memory、retrieval、source grounding",
        "从 rollout、observability、incident review",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_community_roadmap_surfaces_three_canonical_roadmap_cases() -> None:
    required_markers = (
        "Canonical roadmap cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "next layer of value",
        "richer trace examples",
        "approval policy templates",
        "duplicate-ticket evals",
        "runnable high-risk scenario",
        "knowledge scenario",
        "retrieval policy template",
        "memory eval patterns",
        "source-grounding QA",
        "incident trace examples",
        "escalation/notification templates",
        "response ownership checks",
        "post-incident learning assets",
    )
    checked_files = (
        "docs/appendix/community-roadmap.md",
        "docs/appendix/community-roadmap.en.md",
        "docs/appendix/community-roadmap.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_multilingual_community_roadmap_case_note_is_localized() -> None:
    russian_path = "docs/appendix/community-roadmap.md"
    russian_text = _read(russian_path)
    chinese_text = _read("docs/appendix/community-roadmap.zh.md")

    for marker in (
        "Канонические сценарии дорожной карты",
        "Дорожная карта",
        "следующий слой пользы (next layer of value)",
    ):
        _assert_file_contains(russian_path, marker)
    _assert_file_contains(russian_path, "Триаж обращений поддержки (Support triage)")
    _assert_file_contains(russian_path, "incident trace examples")
    _assert_file_contains(russian_path, "post-incident learning assets")

    assert "规范路线图案例" in chinese_text
    assert "路线图（roadmap）" in chinese_text
    assert "下一层价值（next layer of value）" in chinese_text
    assert "参考模式" in chinese_text
    assert "追踪模式与事件目录" in chinese_text
    assert "渲染后的模式（schema）页面" in chinese_text
    assert "原始图表块（raw diagram blocks）" in chinese_text
    assert "渲染站点 QA 检查清单（rendered-site QA checklist）" in chinese_text
    assert "支持分流（Support triage）" in chinese_text
    assert "事件追踪示例（incident trace examples）" in chinese_text
    assert "事件后学习资产（post-incident learning assets）" in chinese_text

    forbidden_markers = (
        "Roadmap должен измерять next layer of value",
        "через три canonical cases",
        "задает приоритет для richer trace examples",
        "задает приоритет для knowledge scenario",
        "задает приоритет для incident trace examples",
        "Roadmap 应通过三个 canonical cases 衡量 next layer of value",
        "参考 Schema",
        "追踪 Schema 与事件目录",
        "schema 页面没有破损表格",
        "粘连列表或 raw diagram blocks",
        "轻量级 rendered-site QA checklist",
        "优先推动 richer trace examples",
        "优先推动 knowledge scenario",
        "优先推动 incident trace examples",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_google_integration_roadmap_surfaces_three_canonical_platform_cases() -> None:
    required_markers_by_file = {
        "docs/appendix/google-integration-roadmap.md": (
            "Канонические сценарии Google-интеграции",
            "Триаж обращений поддержки",
            "Внутренний ассистент знаний",
            "Координация инцидентов",
            "идеи платформенного уровня",
            "идентичность агента",
            "минимальные привилегии",
            "связь подтверждений и аудита",
            "профиль песочницы",
            "инструменты высокого риска",
            "контроль дублей тикетов",
            "слои контекста",
            "управление памятью",
            "политику поиска",
            "происхождение источников",
            "доступ с учетом арендатора",
            "управление реестром",
            "границы A2A",
            "непрерывные проверки",
            "шлюзы поэтапного выпуска",
            "трассы эскалации",
            "владение ответом",
        ),
        "docs/appendix/google-integration-roadmap.en.md": (
            "Canonical Google integration cases",
            "Support triage",
            "Internal knowledge assistant",
            "Incident coordination",
            "platform-grade ideas",
            "agent identity",
            "least privilege",
            "approval/audit linkage",
            "sandbox profile",
            "high-risk tools",
            "duplicate-ticket controls",
            "context layers",
            "memory governance",
            "retrieval policy",
            "source provenance",
            "tenant-aware access",
            "registry governance",
            "A2A boundaries",
            "continuous controls",
            "rollout gates",
            "escalation traces",
            "response ownership",
        ),
        "docs/appendix/google-integration-roadmap.zh.md": (
            "Canonical Google integration cases",
            "Support triage",
            "Internal knowledge assistant",
            "Incident coordination",
            "platform-grade ideas",
            "agent identity",
            "least privilege",
            "approval/audit linkage",
            "sandbox profile",
            "high-risk tools",
            "duplicate-ticket controls",
            "context layers",
            "memory governance",
            "retrieval policy",
            "source provenance",
            "tenant-aware access",
            "registry governance",
            "A2A boundaries",
            "continuous controls",
            "rollout gates",
            "escalation traces",
            "response ownership",
        ),
    }

    for path, required_markers in required_markers_by_file.items():
        _assert_files_contain_all((path,), required_markers)


def test_multilingual_google_integration_case_note_is_localized() -> None:
    russian_text = _read("docs/appendix/google-integration-roadmap.md")
    chinese_text = _read("docs/appendix/google-integration-roadmap.zh.md")

    assert "Канонические сценарии Google-интеграции" in russian_text
    assert "Дорожная карта Google-интеграции полезнее" in russian_text
    assert "идеи платформенного уровня" in russian_text
    assert "идентичность агента" in russian_text
    assert "слои контекста" in russian_text
    assert "управление реестром" in russian_text

    assert "规范 Google 集成案例" in chinese_text
    assert "Google 集成路线图（Google integration roadmap）" in chinese_text
    assert "平台级想法（platform-grade ideas）" in chinese_text
    assert "智能体身份（agent identity）" in chinese_text
    assert "上下文层（context layers）" in chinese_text
    assert "注册表治理（registry governance）" in chinese_text

    forbidden_markers = (
        "Google integration roadmap полезнее",
        "platform-grade ideas на трех canonical cases",
        "проверяет agent identity",
        "проверяет context layers",
        "проверяет registry governance",
        "Google integration roadmap 在用三个 canonical cases",
        "检查 platform-grade ideas",
        "检查 agent identity",
        "检查 context layers",
        "检查 registry governance",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_research_frontier_surfaces_three_canonical_frontier_cases() -> None:
    english_markers = (
        "Canonical frontier cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "research frontier",
        "promising pattern",
        "production default",
        "agent memory",
        "trace-linked evals",
        "approval gates",
        "duplicate-ticket recovery",
        "rollback cost",
        "hierarchical memory",
        "source provenance",
        "retrieval freshness",
        "tenant-aware access",
        "auditability",
        "causal tracing",
        "multi-agent reliability",
        "handoff contracts",
        "incident review",
        "diagnosable system boundaries",
    )
    russian_markers = (
        "Канонические сценарии исследовательского фронтира",
        "Триаж обращений поддержки",
        "Внутренний ассистент знаний",
        "Координация инцидентов",
        "исследовательский фронтир",
        "многообещающий шаблон",
        "промышленным правилом по умолчанию",
        "память агента",
        "оценки, связанные с трассами",
        "шлюзы подтверждений",
        "восстановление после дубля тикета",
        "стоимость отката",
        "иерархическую память",
        "происхождение источников",
        "свежесть поиска",
        "доступ с учетом арендатора",
        "аудитируемость",
        "причинную трассировку",
        "надежность многоагентных систем",
        "контракты передачи управления",
        "разбор инцидента",
        "диагностируемые границы системы",
    )

    _assert_files_contain_all(("docs/appendix/research-frontier.md",), russian_markers)
    _assert_files_contain_all(("docs/appendix/research-frontier.en.md",), english_markers)
    _assert_files_contain_all(("docs/appendix/research-frontier.zh.md",), english_markers)


def test_multilingual_research_frontier_case_note_is_localized() -> None:
    russian_text = _read("docs/appendix/research-frontier.md")
    chinese_text = _read("docs/appendix/research-frontier.zh.md")

    assert "Канонические сценарии исследовательского фронтира" in russian_text
    assert "Исследовательский фронтир стоит фильтровать" in russian_text
    assert "многообещающий шаблон" in russian_text
    assert "память агента" in russian_text
    assert "иерархическую память" in russian_text
    assert "причинную трассировку" in russian_text

    assert "规范前沿案例" in chinese_text
    assert "研究前沿（research frontier）" in chinese_text
    assert "有前景的模式（promising pattern）" in chinese_text
    assert "智能体记忆（agent memory）" in chinese_text
    assert "分层记忆（hierarchical memory）" in chinese_text
    assert "因果追踪（causal tracing）" in chinese_text
    assert "记忆记录与检索契约模式" in chinese_text
    assert "追踪模式；" in chinese_text
    assert "追踪模式与事件目录" in chinese_text
    assert "评测数据集模式与打分契约" in chinese_text

    forbidden_markers = (
        "Research frontier стоит фильтровать",
        "через три canonical cases",
        "promising pattern не стал production default",
        "проверяет agent memory",
        "проверяет hierarchical memory",
        "проверяет causal tracing",
        "通过三个 canonical cases 过滤 research frontier",
        "避免 promising pattern 过早变成 production default",
        "检查 agent memory",
        "检查 hierarchical memory",
        "检查 causal tracing",
        "记忆记录与检索契约 Schema",
        "追踪 Schema；",
        "追踪 Schema 与事件目录",
        "评测数据集 Schema 与打分契约",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_language_stack_surfaces_three_canonical_language_cases() -> None:
    required_markers = (
        "Canonical language cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "Language choice",
        "canonical cases",
        "Python/TypeScript",
        "behavior iteration",
        "tool gateway",
        "approval service",
        "idempotency control",
        "audit trail",
        "stricter platform services",
        "retrieval experiments",
        "eval loop",
        "contract layer",
        "memory/index service",
        "source provenance",
        "tenant-aware access",
        "runtime reliability",
        "trace ingestion pipeline",
        "notification safety",
        "response ownership",
        "platform control",
    )
    checked_files = (
        "docs/appendix/rust-vs-python-typescript.md",
        "docs/appendix/rust-vs-python-typescript.en.md",
        "docs/appendix/rust-vs-python-typescript.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_multilingual_language_stack_case_note_is_localized() -> None:
    russian_path = "docs/appendix/rust-vs-python-typescript.md"
    russian_text = _read(russian_path)
    chinese_text = _read("docs/appendix/rust-vs-python-typescript.zh.md")

    for marker in (
        "Канонические сценарии выбора языка",
        "Выбор языка",
        "итераций поведения (behavior iteration)",
    ):
        _assert_file_contains(russian_path, marker)
    _assert_file_contains(russian_path, "шлюз инструментов (tool gateway)")
    _assert_file_contains(russian_path, "retrieval experiments")
    _assert_file_contains(russian_path, "runtime reliability")

    assert "规范语言案例" in chinese_text
    assert "语言选择（Language choice）" in chinese_text
    assert "行为迭代（behavior iteration）" in chinese_text
    assert "工具网关（tool gateway）" in chinese_text
    assert "检索实验（retrieval experiments）" in chinese_text
    assert "运行时可靠性（runtime reliability）" in chinese_text

    forbidden_markers = (
        "Language choice должен",
        "через три canonical cases",
        "для behavior iteration",
        "выносит tool gateway",
        "держит retrieval experiments",
        "runtime reliability, trace ingestion pipeline",
        "Language choice 应该通过三个 canonical cases",
        "做 behavior iteration",
        "把 tool gateway",
        "把 retrieval experiments",
        "runtime reliability、trace ingestion pipeline",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_rust_agent_platforms_surface_three_canonical_platform_cases() -> None:
    english_markers = (
        "Canonical Rust platform cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "Rust infrastructure",
        "canonical cases",
        "tool gateway",
        "policy enforcement service",
        "approval queue service",
        "idempotency semantics",
        "audit pipeline",
        "memory/index layers",
        "retrieval service boundaries",
        "source provenance",
        "tenant isolation",
        "trace processors",
        "long-lived runtime",
        "MCP-compatible integration layer",
        "egress control services",
        "notification safety",
        "control-plane reliability",
    )
    russian_markers = (
        "Канонические сценарии Rust-платформы",
        "Триаж обращений поддержки",
        "Внутренний ассистент знаний",
        "Координация инцидентов",
        "Rust-инфраструктура",
        "канонических сценариях",
        "шлюз инструментов",
        "сервис применения политик",
        "сервис очереди подтверждений",
        "семантику идемпотентности",
        "конвейер аудита",
        "слои памяти и индекса",
        "границы сервиса поиска",
        "происхождение источников",
        "изоляцию арендатора",
        "обработчики трасс",
        "долгоживущую среду исполнения",
        "MCP-совместимый интеграционный слой",
        "сервисы контроля исходящих соединений",
        "безопасность уведомлений",
        "надежность управляющего слоя",
    )
    chinese_markers = (
        "Canonical Rust platform cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "Rust infrastructure",
        "canonical cases",
        "tool gateway",
        "policy enforcement service",
        "approval queue service",
        "idempotency semantics",
        "audit pipeline",
        "memory/index layers",
        "retrieval service boundaries",
        "source provenance",
        "tenant isolation",
        "trace processors",
        "long-lived runtime",
        "MCP-compatible integration layer",
        "egress control services",
        "notification safety",
        "control-plane reliability",
    )

    _assert_files_contain_all(("docs/appendix/rust-agent-platforms.en.md",), english_markers)
    _assert_files_contain_all(("docs/appendix/rust-agent-platforms.md",), russian_markers)
    _assert_files_contain_all(("docs/appendix/rust-agent-platforms.zh.md",), chinese_markers)


def test_multilingual_rust_agent_platforms_case_note_is_localized() -> None:
    russian_text = _read("docs/appendix/rust-agent-platforms.md")
    chinese_text = _read("docs/appendix/rust-agent-platforms.zh.md")

    assert "Канонические сценарии Rust-платформы" in russian_text
    assert "Rust-инфраструктура должна доказывать пользу" in russian_text
    assert "шлюз инструментов" in russian_text
    assert "слои памяти и индекса" in russian_text
    assert "долгоживущую среду исполнения" in russian_text

    assert "规范 Rust 平台案例" in chinese_text
    assert "Rust 基础设施（Rust infrastructure）" in chinese_text
    assert "工具网关（tool gateway）" in chinese_text
    assert "记忆/索引层（memory/index layers）" in chinese_text
    assert "长期运行时（long-lived runtime）" in chinese_text

    russian_forbidden = (
        "Rust infrastructure",
        "tool gateway",
        "memory/index layers",
        "long-lived runtime",
        "canonical cases",
        "agent infrastructure",
        "vendor-native agent building",
        "Rust infrastructure должен",
        "трех canonical cases",
        "проверяет tool gateway",
        "проверяет memory/index layers",
        "проверяет long-lived runtime",
    )
    chinese_forbidden = (
        "Rust infrastructure 应该通过三个 canonical cases",
        "检查 tool gateway",
        "检查 memory/index layers",
        "检查 long-lived runtime",
    )

    for marker in russian_forbidden:
        assert marker not in russian_text
    for marker in chinese_forbidden:
        assert marker not in chinese_text


def test_glossary_surfaces_three_canonical_routes() -> None:
    english_markers = (
        "Canonical glossary routes",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "fast route",
        "Tool gateway",
        "Approval gate",
        "Policy gate",
        "Capability catalog",
        "Trace",
        "Eval dataset",
        "Retrieval",
        "Long-term memory",
        "Profile memory",
        "Provenance",
        "Trust boundary",
        "Egress policy",
        "Agent runtime",
        "Control plane",
        "Rollout gate",
        "Span",
        "Approved inventory",
    )
    russian_markers = (
        "Канонические маршруты глоссария",
        "Триаж обращений поддержки",
        "Внутренний ассистент знаний",
        "Координация инцидентов",
        "быстрый маршрут",
        "Шлюз инструментов",
        "Шлюз подтверждения",
        "Шлюз политик",
        "Каталог возможностей",
        "Трасса",
        "Набор оценочных данных",
        "Извлечение контекста",
        "Долгосрочная память",
        "Профильная память",
        "Происхождение данных",
        "Граница доверия",
        "Правила исходящих соединений",
        "Исполняющая среда агента",
        "Управляющий слой",
        "Шлюз поэтапного выпуска",
        "Спан",
        "Утвержденный реестр",
    )
    chinese_markers = (
        "Canonical glossary routes",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "fast route",
        "Tool gateway",
        "Approval gate",
        "Policy gate",
        "Capability catalog",
        "Trace",
        "Eval dataset",
        "Retrieval",
        "Long-term memory",
        "Profile memory",
        "Provenance",
        "Trust boundary",
        "Egress policy",
        "Agent runtime",
        "Control plane",
        "Rollout gate",
        "Span",
        "Approved inventory",
    )

    _assert_files_contain_all(("docs/appendix/glossary.en.md",), english_markers)
    _assert_files_contain_all(("docs/appendix/glossary.md",), russian_markers)
    _assert_files_contain_all(("docs/appendix/glossary.zh.md",), chinese_markers)


def test_multilingual_glossary_routes_note_is_localized() -> None:
    russian_text = _read("docs/appendix/glossary.md")
    chinese_text = _read("docs/appendix/glossary.zh.md")

    assert "Канонические маршруты глоссария" in russian_text
    assert "глоссарий как быстрый маршрут" in russian_text
    assert "шлюза инструментов" in russian_text
    assert "долгосрочной памяти" in russian_text
    assert "управляющего слоя" in russian_text
    assert "утвержденного реестра" in russian_text

    assert "规范术语表路线" in chinese_text
    assert "术语表（glossary）" in chinese_text
    assert "快速路线（fast route）" in chinese_text
    assert "工具网关（Tool gateway）" in chinese_text
    assert "长期记忆（Long-term memory）" in chinese_text
    assert "控制平面（Control plane）" in chinese_text
    assert "已批准清单（Approved inventory）" in chinese_text

    russian_forbidden = (
        "glossary)",
        "fast route",
        "Tool gateway",
        "Long-term memory",
        "Control plane",
        "Approved inventory",
        "Agent runtime",
        "Policy gate",
        "Capability catalog",
        "Egress policy",
        "Rollout gate",
        "Используй glossary как fast route",
        "по трем canonical cases",
        "начинается с Tool gateway",
        "начинается с Retrieval",
        "начинается с Agent runtime",
    )
    chinese_forbidden = (
        "Use the glossary 作为三个 canonical cases 的 fast route",
        "从 Tool gateway、Approval gate",
        "从 Retrieval、Long-term memory",
        "从 Agent runtime、Control plane",
    )

    for marker in russian_forbidden:
        assert marker not in russian_text
    for marker in chinese_forbidden:
        assert marker not in chinese_text


def test_sources_surface_three_canonical_source_routes() -> None:
    english_markers = (
        "Canonical source routes",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "fast route",
        "OWASP",
        "OpenAI agent guides",
        "HITL sources",
        "policy/approval material",
        "trace grading",
        "incident cases",
        "LangGraph memory",
        "OpenAI Agent memory",
        "retrieval/eval sources",
        "provenance-oriented governance",
        "memory research frontier",
        "NIST/AI RMF",
        "Google/Microsoft governance",
        "observability sources",
        "multi-agent reliability research",
        "incident review",
        "rollout/control-plane material",
    )
    russian_markers = (
        "Канонические маршруты источников",
        "Триаж обращений поддержки",
        "Внутренний ассистент знаний",
        "Координация инцидентов",
        "быстрый маршрут",
        "OWASP",
        "руководств OpenAI по агентам",
        "человеке в контуре",
        "материалов по политикам и подтверждениям",
        "оценки трасс",
        "кейсов инцидентов",
        "материалов LangGraph о памяти",
        "материалов OpenAI о памяти агента",
        "источников по поиску и оценке",
        "управления с акцентом на происхождение данных",
        "исследовательского фронтира памяти",
        "NIST/AI RMF",
        "материалов Google и Microsoft по управлению",
        "источников наблюдаемости",
        "исследований надежности многоагентных систем",
        "разбора инцидентов",
        "материалов по выпуску и управляющему слою",
    )
    chinese_markers = (
        "Canonical source routes",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "fast route",
        "OWASP",
        "OpenAI agent guides",
        "HITL sources",
        "policy/approval material",
        "trace grading",
        "incident cases",
        "LangGraph memory",
        "OpenAI Agent memory",
        "retrieval/eval sources",
        "provenance-oriented governance",
        "memory research frontier",
        "NIST/AI RMF",
        "Google/Microsoft governance",
        "observability sources",
        "multi-agent reliability research",
        "incident review",
        "rollout/control-plane material",
    )

    _assert_files_contain_all(("docs/appendix/sources.en.md",), english_markers)
    _assert_files_contain_all(("docs/appendix/sources.md",), russian_markers)
    _assert_files_contain_all(("docs/appendix/sources.zh.md",), chinese_markers)


def test_multilingual_sources_canonical_routes_note_is_localized() -> None:
    russian_text = _read("docs/appendix/sources.md")
    chinese_text = _read("docs/appendix/sources.zh.md")

    assert "Канонические маршруты источников" in russian_text
    assert "источники как быстрый маршрут" in russian_text
    assert "руководств OpenAI по агентам" in russian_text
    assert "материалов LangGraph о памяти" in russian_text
    assert "источников наблюдаемости" in russian_text

    assert "规范来源路线" in chinese_text
    assert "来源（sources）" in chinese_text
    assert "快速路线（fast route）" in chinese_text
    assert "OpenAI 智能体指南（OpenAI agent guides）" in chinese_text
    assert "LangGraph 记忆（LangGraph memory）" in chinese_text
    assert "可观测性来源（observability sources）" in chinese_text

    russian_forbidden = (
        "sources)",
        "fast route",
        "OpenAI agent guides",
        "LangGraph memory",
        "OpenAI Agent memory",
        "retrieval/eval sources",
        "observability sources",
        "multi-agent reliability research",
        "rollout/control-plane material",
        "Используй sources как fast route",
        "трех canonical cases",
        "OpenAI agent guides, HITL sources",
        "LangGraph memory, OpenAI Agent memory",
        "observability sources, multi-agent reliability research",
    )
    chinese_forbidden = (
        "Use the sources 作为三个 canonical cases 的 fast route",
        "OpenAI agent guides、HITL sources",
        "LangGraph memory、OpenAI Agent memory",
        "observability sources、multi-agent reliability research",
    )

    for marker in russian_forbidden:
        assert marker not in russian_text
    for marker in chinese_forbidden:
        assert marker not in chinese_text


def test_sources_include_agent_specific_owasp_security_sources() -> None:
    english_markers = (
        "Agent-specific security",
        "AI Agent Security Cheat Sheet",
        "AI_Agent_Security_Cheat_Sheet.html",
        "MCP Security Cheat Sheet",
        "MCP_Security_Cheat_Sheet.html",
        "LLM Prompt Injection Prevention Cheat Sheet",
        "LLM_Prompt_Injection_Prevention_Cheat_Sheet.html",
        "RAG Security Cheat Sheet",
        "RAG_Security_Cheat_Sheet.html",
        "Governance and baseline controls",
    )
    russian_markers = (
        "Безопасность агентных систем",
        "AI Agent Security Cheat Sheet",
        "AI_Agent_Security_Cheat_Sheet.html",
        "MCP Security Cheat Sheet",
        "MCP_Security_Cheat_Sheet.html",
        "LLM Prompt Injection Prevention Cheat Sheet",
        "LLM_Prompt_Injection_Prevention_Cheat_Sheet.html",
        "RAG Security Cheat Sheet",
        "RAG_Security_Cheat_Sheet.html",
        "Управление и базовые меры контроля",
    )
    chinese_markers = (
        "Agent-specific security",
        "AI Agent Security Cheat Sheet",
        "AI_Agent_Security_Cheat_Sheet.html",
        "MCP Security Cheat Sheet",
        "MCP_Security_Cheat_Sheet.html",
        "LLM Prompt Injection Prevention Cheat Sheet",
        "LLM_Prompt_Injection_Prevention_Cheat_Sheet.html",
        "RAG Security Cheat Sheet",
        "RAG_Security_Cheat_Sheet.html",
        "Governance and baseline controls",
    )

    _assert_files_contain_all(("docs/appendix/sources.en.md",), english_markers)
    _assert_files_contain_all(("docs/appendix/sources.md",), russian_markers)
    _assert_files_contain_all(("docs/appendix/sources.zh.md",), chinese_markers)


def test_fast_moving_chapters_carry_may_17_review_dates() -> None:
    chapter_bases = (
        "docs/book/part-iv/chapter-9",
        "docs/book/part-v/chapter-13",
        "docs/book/part-viii/chapter-21",
        "docs/book/part-viii/chapter-24",
        "docs/book/part-viii/chapter-25",
        "docs/book/part-viii/chapter-26",
        "docs/book/part-viii/chapter-27",
    )
    expected_by_suffix = {
        ".md": (
            "Последняя редакционная проверка: **17 мая 2026 года**.",
            "Предыдущая проверка: **14 мая 2026 года**.",
            "Следующая плановая проверка: **17 июня 2026 года**.",
        ),
        ".en.md": (
            "Last reviewed: **May 17, 2026**.",
            "Previous review: **May 14, 2026**.",
            "Next scheduled review: **June 17, 2026**.",
        ),
        ".zh.md": (
            "最近一次编辑审查：**2026 年 5 月 17 日**。",
            "上一次审查：**2026 年 5 月 14 日**。",
            "下一次计划审查：**2026 年 6 月 17 日**。",
        ),
    }

    for base in chapter_bases:
        for suffix, expected_markers in expected_by_suffix.items():
            _assert_files_contain_all((f"{base}{suffix}",), expected_markers)


def test_fast_moving_chapter_review_notes_reflect_closed_editorial_work() -> None:
    chapter_bases = (
        "docs/book/part-iv/chapter-9",
        "docs/book/part-v/chapter-13",
        "docs/book/part-viii/chapter-20",
        "docs/book/part-viii/chapter-21",
        "docs/book/part-viii/chapter-22",
        "docs/book/part-viii/chapter-24",
        "docs/book/part-viii/chapter-25",
        "docs/book/part-viii/chapter-26",
        "docs/book/part-viii/chapter-27",
    )
    expected_by_suffix = {
        ".md": (
            "теперь покрыты конкретными контрактами и проверками документации",
            "ближайшие редакционные задачи",
        ),
        ".en.md": (
            "now have concrete contract coverage and docs-surface guards",
            "near-term editorial work",
        ),
        ".zh.md": (
            "现在都有具体契约覆盖和文档表面检查",
            "近期编辑任务",
        ),
    }

    for base in chapter_bases:
        for suffix, (required, forbidden) in expected_by_suffix.items():
            text = _read(f"{base}{suffix}")
            assert required in text, (base, suffix)
            assert forbidden not in text, (base, suffix)


def test_why_this_book_surfaces_three_canonical_book_cases() -> None:
    english_markers = (
        "Canonical book cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "write actions",
        "approvals",
        "policy gates",
        "duplicate-ticket recovery",
        "audit trail",
        "polished demo",
        "retrieval",
        "memory boundaries",
        "source grounding",
        "provenance",
        "tenant-aware access",
        "prompt tricks",
        "traces",
        "SLOs",
        "escalation",
        "response ownership",
        "rollout control",
        "post-incident learning",
        "production incident",
    )
    russian_markers = (
        "Канонические сценарии книги",
        "Триаж обращений поддержки",
        "Внутренний ассистент знаний",
        "Координация инцидентов",
        "записывающие действия",
        "подтверждения",
        "шлюзы политик",
        "восстановление после дубля тикета",
        "аудиторский след",
        "отполированной демонстрации",
        "поиск",
        "границы памяти",
        "привязка к источникам",
        "происхождение данных",
        "доступ с учетом арендатора",
        "приемами формулирования запросов",
        "трассы",
        "SLO",
        "эскалация",
        "владение реагированием",
        "контроль поэтапного выпуска",
        "обучение после инцидента",
        "производственного инцидента",
    )
    chinese_markers = (
        "Canonical book cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "write actions",
        "approvals",
        "policy gates",
        "duplicate-ticket recovery",
        "audit trail",
        "polished demo",
        "retrieval",
        "memory boundaries",
        "source grounding",
        "provenance",
        "tenant-aware access",
        "prompt tricks",
        "traces",
        "SLOs",
        "escalation",
        "response ownership",
        "rollout control",
        "post-incident learning",
        "production incident",
    )

    _assert_files_contain_all(("docs/appendix/why-this-book.en.md",), english_markers)
    _assert_files_contain_all(("docs/appendix/why-this-book.md",), russian_markers)
    _assert_files_contain_all(("docs/appendix/why-this-book.zh.md",), chinese_markers)


def test_multilingual_why_this_book_case_note_is_localized() -> None:
    russian_text = _read("docs/appendix/why-this-book.md")
    chinese_text = _read("docs/appendix/why-this-book.zh.md")

    assert "Канонические сценарии книги" in russian_text
    assert "канонических сценариях" in russian_text
    assert "записывающие действия" in russian_text
    assert "поиск" in russian_text
    assert "трассы" in russian_text
    assert "до производственного инцидента" in russian_text

    assert "规范书籍案例" in chinese_text
    assert "规范案例（canonical cases）" in chinese_text
    assert "写入动作（write actions）" in chinese_text
    assert "检索（retrieval）" in chinese_text
    assert "追踪（traces）" in chinese_text
    assert "服务级目标（SLOs）" in chinese_text
    assert "提示词技巧（prompt tricks）" in chinese_text
    assert "生产事故（production incident）之前" in chinese_text

    russian_forbidden = (
        "canonical cases",
        "write actions",
        "polished demo",
        "retrieval",
        "memory boundaries",
        "prompt tricks",
        "traces)",
        "production incident",
        "трех canonical cases",
        "почему write actions",
        "важнее polished demo",
        "почему retrieval, memory boundaries",
        "почему traces, SLOs",
    )
    chinese_forbidden = (
        "三个 canonical cases",
        "为什么 write actions",
        "比 polished demo",
        "为什么 retrieval、memory boundaries",
        "为什么 traces、SLOs",
        "而不是 prompt tricks",
        "production incident 之前",
    )

    for marker in russian_forbidden:
        assert marker not in russian_text
    for marker in chinese_forbidden:
        assert marker not in chinese_text


def test_publishing_stack_surfaces_three_canonical_publishing_cases() -> None:
    english_markers = (
        "Canonical publishing cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "Publishing stack",
        "canonical cases",
        "reader routes",
        "build pages",
        "fast build",
        "GitHub Pages deployment",
        "search/navigation",
        "policy/approval examples",
        "trace/eval artifacts",
        "Markdown-first authoring",
        "multilingual pages",
        "glossary/search surface",
        "source links",
        "memory/retrieval material",
        "strict build gate",
        "reproducible docs commands",
        "incident/rollout pages",
        "stable navigation",
        "visible changelog-style diffs",
        "migration-risk discipline",
    )
    russian_markers = (
        "Канонические сценарии публикации",
        "Триаж обращений поддержки",
        "Внутренний ассистент знаний",
        "Координация инцидентов",
        "Стек публикации",
        "канонических сценария",
        "маршруты чтения",
        "страницы сборки",
        "быстрой сборки",
        "публикации на GitHub Pages",
        "поиска и навигации",
        "примеров политик и подтверждений",
        "артефакты трасс и оценок",
        "авторства с приоритетом Markdown",
        "многоязычных страниц",
        "глоссария и поиска",
        "ссылок на источники",
        "материалов памяти/поиска",
        "строгого шлюза сборки",
        "воспроизводимых команд документации",
        "страницам инцидентов и выпусков",
        "стабильной навигации",
        "видимых различий в стиле журнала изменений",
        "дисциплины миграционного риска",
    )
    chinese_markers = (
        "Canonical publishing cases",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "Publishing stack",
        "canonical cases",
        "reader routes",
        "build pages",
        "fast build",
        "GitHub Pages deployment",
        "search/navigation",
        "policy/approval examples",
        "trace/eval artifacts",
        "Markdown-first authoring",
        "multilingual pages",
        "glossary/search surface",
        "source links",
        "memory/retrieval material",
        "strict build gate",
        "reproducible docs commands",
        "incident/rollout pages",
        "stable navigation",
        "visible changelog-style diffs",
        "migration-risk discipline",
    )

    _assert_files_contain_all(("docs/appendix/stack.en.md",), english_markers)
    _assert_files_contain_all(("docs/appendix/stack.md",), russian_markers)
    _assert_files_contain_all(("docs/appendix/stack.zh.md",), chinese_markers)


def test_multilingual_publishing_stack_case_note_is_localized() -> None:
    russian_text = _read("docs/appendix/stack.md")
    chinese_text = _read("docs/appendix/stack.zh.md")

    assert "Канонические сценарии публикации" in russian_text
    assert "Стек публикации должен поддерживать" in russian_text
    assert "маршруты чтения" in russian_text
    assert "быстрой сборки" in russian_text
    assert "многоязычных страниц" in russian_text
    assert "строгого шлюза сборки" in russian_text

    assert "规范发布案例" in chinese_text
    assert "发布栈（Publishing stack）" in chinese_text
    assert "阅读路线（reader routes）" in chinese_text
    assert "快速构建（fast build）" in chinese_text
    assert "多语言页面（multilingual pages）" in chinese_text
    assert "记忆/检索材料（memory/retrieval material）" in chinese_text
    assert "低摩擦更新（low-friction updates）" in chinese_text
    assert "严格构建门禁（strict build gate）" in chinese_text
    assert "事件/发布页面（incident/rollout pages）" in chinese_text
    assert "稳定导航（stable navigation）" in chinese_text

    russian_forbidden = (
        "Publishing stack",
        "canonical cases",
        "reader routes",
        "build pages",
        "fast build",
        "Markdown-first authoring",
        "multilingual pages",
        "strict build gate",
        "low-friction updates",
        "Publishing stack должен",
        "три canonical cases как reader routes",
        "только build pages",
        "требует fast build",
        "требует Markdown-first authoring",
        "требует strict build gate",
    )
    chinese_forbidden = (
        "Publishing stack 应该把三个 canonical cases",
        "支撑成 reader routes",
        "只是 build pages",
        "需要 fast build",
        "需要 Markdown-first authoring",
        "对记忆/检索材料的低摩擦更新（low-friction updates for memory/retrieval material）",
        "需要 strict build gate",
        "指向事件/发布页面的稳定导航（stable navigation to incident/rollout pages）",
    )

    for marker in russian_forbidden:
        assert marker not in russian_text
    for marker in chinese_forbidden:
        assert marker not in chinese_text


def test_start_here_surfaces_safe_agent_schema_spine() -> None:
    localized_markers = (
        "Главная линия схем безопасного агента",
        "trace-schema",
        "eval-schema",
        "memory-retrieval-schema",
        "модель угроз MCP",
        "контракт доверия передачи управления A2A",
        "запись вердикта проверяющего",
        "запись управленческого действия",
        "поля проверки отравления памяти",
        "единые доказательства угроз агенту",
    )
    english_markers = (
        "Safe-agent schema spine",
        "trace-schema",
        "eval-schema",
        "memory-retrieval-schema",
        "MCP threat model",
        "A2A handoff trust contract",
        "verifier verdict record",
        "governance action record",
        "memory poisoning review fields",
        "unified agent threat evidence",
    )

    _assert_files_contain_all(("docs/start-here.md",), localized_markers)
    _assert_files_contain_all(
        ("docs/start-here.en.md", "docs/start-here.zh.md"), english_markers
    )


def test_multilingual_start_here_safe_agent_schema_route_is_localized() -> None:
    russian_text = _read("docs/start-here.md")
    chinese_text = _read("docs/start-here.zh.md")

    assert "модель угроз MCP" in russian_text
    assert "контракт доверия передачи управления A2A" in russian_text
    assert "запись вердикта проверяющего" in russian_text
    assert "запись управленческого действия" in russian_text
    assert "поля проверки отравления памяти" in russian_text
    assert "единые доказательства угроз агенту" in russian_text

    assert "MCP 威胁模型（MCP threat model）" in chinese_text
    assert "A2A 移交信任契约（A2A handoff trust contract）" in chinese_text
    assert "验证器裁决记录（verifier verdict record）" in chinese_text
    assert "治理动作记录（governance action record）" in chinese_text
    assert "记忆投毒审查字段（memory poisoning review fields）" in chinese_text
    assert "统一智能体威胁证据（unified agent threat evidence）" in chinese_text

    forbidden_markers = (
        "проверить MCP threat model",
        "A2A handoff trust contract, verifier verdict record",
        "governance action record, memory poisoning review fields",
        "检查 MCP threat model",
        "A2A handoff trust contract、verifier verdict record",
        "governance action record、memory poisoning review fields",
    )

    for marker in forbidden_markers:
        assert marker not in russian_text
        assert marker not in chinese_text


def test_reference_surfaces_safe_agent_schema_spine() -> None:
    required_markers_by_file = {
        "docs/reference.md": (
            "Цепочка схем безопасного агента",
            "схему трасс",
            "схему оценивания",
            "схему памяти и поиска",
            "модель угроз MCP",
            "контракт доверия передачи управления A2A",
            "запись вердикта проверяющего",
            "запись управленческого действия",
            "поля проверки отравления памяти",
            "единые доказательства угроз агенту",
        ),
        "docs/reference.en.md": (
            "Safe-agent schema spine",
            "trace schema",
            "eval schema",
            "memory/retrieval schema",
            "MCP threat model",
            "A2A handoff trust contract",
            "verifier verdict record",
            "governance action record",
            "memory poisoning review fields",
            "unified agent threat evidence",
        ),
        "docs/reference.zh.md": (
            "Safe-agent schema spine",
            "trace schema",
            "eval schema",
            "memory/retrieval schema",
            "MCP threat model",
            "A2A handoff trust contract",
            "verifier verdict record",
            "governance action record",
            "memory poisoning review fields",
            "unified agent threat evidence",
        ),
    }

    for path, required_markers in required_markers_by_file.items():
        _assert_files_contain_all((path,), required_markers)


def test_reference_safe_agent_schema_spine_links_are_clickable() -> None:
    expected_links_by_file = {
        "docs/reference.md": (
            "appendix/trace-schema.md",
            "appendix/eval-schema.md",
            "appendix/memory-retrieval-schema.md",
        ),
        "docs/reference.en.md": (
            "appendix/trace-schema.en.md",
            "appendix/eval-schema.en.md",
            "appendix/memory-retrieval-schema.en.md",
        ),
        "docs/reference.zh.md": (
            "appendix/trace-schema.zh.md",
            "appendix/eval-schema.zh.md",
            "appendix/memory-retrieval-schema.zh.md",
        ),
    }

    for path, expected_links in expected_links_by_file.items():
        text = _read(path)
        for link in expected_links:
            assert f"]({link})" in text, (path, link)


def test_whats_new_surfaces_safe_agent_schema_update() -> None:
    required_markers = (
        "Safe-agent schema update",
        "May 19, 2026",
        "19 мая 2026 года",
        "2026 年 5 月 19 日",
        "MCP threat model",
        "mcp_server",
        "A2A handoff trust contract",
        "trust-delegation artifact",
        "defense-in-depth control map",
        "verifier verdict record",
        "governance action record",
        "NIST AI RMF telemetry mapping",
        "memory poisoning review fields",
        "unified agent threat evidence",
        "trace schema",
        "eval schema",
        "memory/retrieval schema",
    )
    checked_files = (
        "docs/whats-new.md",
        "docs/whats-new.en.md",
        "docs/whats-new.zh.md",
    )

    for marker in required_markers[:4]:
        assert any(marker in _read(path) for path in checked_files), marker
    _assert_files_contain_all(checked_files[1:], required_markers[4:])
    ru_text = _read("docs/whats-new.md")
    assert "модель угроз для MCP" in ru_text
    assert "контракт доверия для передачи управления A2A" in ru_text
    assert "контракт доверия для A2A handoff" not in ru_text
    assert "контракт доверия для передачи A2A (handoff)" not in ru_text
    assert "артефакт делегирования доверия" in ru_text
    assert "артефакт trust-delegation" not in ru_text
    assert "карта эшелонированной защиты" in ru_text
    assert "запись вердикта проверяющего" in ru_text
    assert "запись управленческого действия" in ru_text
    assert "сопоставление телеметрии с NIST AI RMF" in ru_text
    assert "поля проверки отравления памяти" in ru_text
    assert "единая модель доказательств угроз агентам" in ru_text
    assert "[схеме трасс](appendix/trace-schema.md)" in ru_text
    assert "[схеме оценивания](appendix/eval-schema.md)" in ru_text
    assert "[схеме памяти и поиска](appendix/memory-retrieval-schema.md)" in ru_text
    assert "карта defense-in-depth controls" not in ru_text
    assert "карта defense-in-depth-контролей" not in ru_text
    assert "verifier verdict record" not in ru_text
    assert "запись verifier verdict" not in ru_text
    assert "governance action record" not in ru_text
    assert "запись governance action" not in ru_text
    assert "модель угроз MCP" not in ru_text
    assert "NIST AI RMF telemetry mapping" not in ru_text
    assert "сопоставление телеметрии NIST AI RMF" not in ru_text
    assert "memory poisoning review fields" not in ru_text
    assert "поля проверки memory poisoning" not in ru_text
    assert "unified agent threat evidence" not in ru_text
    assert "единая evidence-модель угроз агентам" not in ru_text
    assert "[trace schema](appendix/trace-schema.md)" not in ru_text
    assert "[eval schema](appendix/eval-schema.md)" not in ru_text
    assert "[memory/retrieval schema](appendix/memory-retrieval-schema.md)" not in ru_text
    _assert_files_contain_all(("docs/whats-new.md",), required_markers[5:6])

    zh_text = _read("docs/whats-new.zh.md")
    assert '!!! note "安全智能体架构（safe-agent）模式更新"' in zh_text
    assert "安全智能体架构（safe-agent architecture）" in zh_text
    assert "正文（prose）、附录（appendices）和防护检查（guards）" in zh_text
    assert "MCP 威胁模型（MCP threat model）" in zh_text
    assert "`mcp_server` 合约（contract）" in zh_text
    assert "A2A 交接信任合约（A2A handoff trust contract）" in zh_text
    assert "信任委派工件（trust-delegation artifact）" in zh_text
    assert "纵深防御控制图（defense-in-depth control map）" in zh_text
    assert "验证者裁决记录（verifier verdict record）" in zh_text
    assert "治理动作记录（governance action record）" in zh_text
    assert "NIST AI RMF 遥测映射（NIST AI RMF telemetry mapping）" in zh_text
    assert "记忆投毒审查字段（memory poisoning review fields）" in zh_text
    assert "统一智能体威胁证据（unified agent threat evidence）" in zh_text
    assert "[跟踪模式（trace schema）](appendix/trace-schema.zh.md)" in zh_text
    assert "[评测模式（eval schema）](appendix/eval-schema.zh.md)" in zh_text
    assert (
        "[记忆/检索模式（memory/retrieval schema）]"
        "(appendix/memory-retrieval-schema.zh.md)"
        in zh_text
    )
    assert '!!! note "Safe-agent schema update"' not in zh_text
    assert "safe-agent architecture 的 prose、appendices 和 guards" not in zh_text
    assert "MCP threat model 与 `mcp_server` contract" not in zh_text
    assert "`mcp_server` 合同（contract）" not in zh_text
    assert "A2A handoff trust contract 与 trust-delegation artifact" not in zh_text
    assert "A2A 交接信任合同（A2A handoff trust contract）" not in zh_text
    assert "defense-in-depth control map、verifier verdict record" not in zh_text
    assert "memory poisoning review fields 和 unified agent threat evidence" not in zh_text
    assert "[trace schema](appendix/trace-schema.zh.md)" not in zh_text
    assert "[eval schema](appendix/eval-schema.zh.md)" not in zh_text
    assert "[memory/retrieval schema](appendix/memory-retrieval-schema.zh.md)" not in zh_text


def test_whats_new_safe_agent_schema_update_links_are_clickable() -> None:
    expected_links_by_file = {
        "docs/whats-new.md": (
            "appendix/trace-schema.md",
            "appendix/eval-schema.md",
            "appendix/memory-retrieval-schema.md",
        ),
        "docs/whats-new.en.md": (
            "appendix/trace-schema.en.md",
            "appendix/eval-schema.en.md",
            "appendix/memory-retrieval-schema.en.md",
        ),
        "docs/whats-new.zh.md": (
            "appendix/trace-schema.zh.md",
            "appendix/eval-schema.zh.md",
            "appendix/memory-retrieval-schema.zh.md",
        ),
    }

    for path, expected_links in expected_links_by_file.items():
        text = _read(path)
        for link in expected_links:
            assert f"]({link})" in text, (path, link)


def test_whats_new_surfaces_canonical_case_update() -> None:
    required_markers = (
        "Canonical case update",
        "May 15, 2026",
        "15 мая 2026 года",
        "2026 年 5 月 15 日",
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
        "book chapters",
        "public entry points",
        "reference pages",
        "appendix artifacts",
        "coverage guards",
        "chapters",
        "appendix pages",
    )
    checked_files = (
        "docs/whats-new.md",
        "docs/whats-new.en.md",
        "docs/whats-new.zh.md",
    )

    for marker in required_markers[:4]:
        assert any(marker in _read(path) for path in checked_files), marker
    _assert_files_contain_all(checked_files[1:], required_markers[4:7])
    _assert_files_contain_all(checked_files[1:], required_markers[7:])
    ru_text = _read("docs/whats-new.md")
    assert "Триаж обращений поддержки" in ru_text
    assert "внутренний ассистент знаний" in ru_text
    assert "координация инцидентов" in ru_text
    assert "главах книги" in ru_text
    assert "публичных точках входа" in ru_text
    assert "справочных страницах" in ru_text
    assert "артефактах приложений" in ru_text
    assert "проверки покрытия защищают главы и страницы приложений" in ru_text
    assert "**Support triage**, **Internal knowledge assistant**" not in ru_text
    assert "book chapters" not in ru_text
    assert "public entry points" not in ru_text
    assert "reference pages" not in ru_text
    assert "appendix artifacts" not in ru_text
    assert "chapters и appendix pages" not in ru_text
    assert "coverage guards" not in ru_text

    zh_text = _read("docs/whats-new.zh.md")
    assert '!!! note "规范案例更新"' in zh_text
    assert "三个规范案例（canonical cases）路线图" in zh_text
    assert "支持分流（Support triage）" in zh_text
    assert "内部知识助手（Internal knowledge assistant）" in zh_text
    assert "事件协调（Incident coordination）" in zh_text
    assert "章节（book chapters）" in zh_text
    assert "公共入口（public entry points）" in zh_text
    assert "参考页（reference pages）" in zh_text
    assert "附录工件（appendix artifacts）" in zh_text
    assert "覆盖率守卫（coverage guards）" in zh_text
    assert "章节与附录页面（appendix pages）丢失这些路线" in zh_text
    assert '!!! note "Canonical case update"' not in zh_text
    assert "三个 canonical cases 地图" not in zh_text
    assert "三个规范案例（canonical cases）地图" not in zh_text
    assert "**Support triage**、**Internal knowledge assistant**" not in zh_text
    assert "出现在 book chapters" not in zh_text
    assert "coverage guards 会防止 chapters" not in zh_text
    assert "章节（chapters）与附录页面" not in zh_text


def test_book_improvement_blueprint_reflects_safe_agent_schema_spine() -> None:
    required_markers = (
        "Implementation status, 20 May 2026",
        "MCP threat model",
        "mcp_server",
        "A2A handoff trust contract",
        "trust-delegation artifact",
        "unified agent threat evidence",
        "defense-in-depth control map",
        "verifier verdict record",
        "governance action record",
        "NIST AI RMF telemetry mapping",
        "memory poisoning review fields",
        "trace schema",
        "eval schema",
        "memory/retrieval schema",
    )

    _assert_files_contain_all(("docs/book-improvement-blueprint.md",), required_markers)


def test_book_improvement_blueprint_schema_spine_links_are_clickable() -> None:
    required_links = (
        "appendix/trace-schema.md",
        "appendix/eval-schema.md",
        "appendix/memory-retrieval-schema.md",
    )
    text = _read("docs/book-improvement-blueprint.md")

    for link in required_links:
        assert f"]({link})" in text, link


def test_editorial_artifacts_use_current_canonical_cases() -> None:
    checked_files = (
        "docs/book-improvement-blueprint.md",
        "docs/publisher-ready-toc.md",
        "docs/reader-journey-map.md",
    )
    required_markers = (
        "Support triage",
        "Internal knowledge assistant",
        "Incident coordination",
    )
    deprecated_markers = (
        "Support triage agent",
        "Internal enterprise knowledge assistant",
        "Approval-bound high-risk action agent",
        "high-risk action / approval-bound agent",
        "support triage, internal knowledge, incident coordination",
        "Support Triage",
        "Internal Knowledge",
        "Incident Coordination",
    )

    _assert_files_contain_all(checked_files, required_markers)
    for path in checked_files:
        text = _read(path)
        for marker in deprecated_markers:
            assert marker not in text, (path, marker)


def test_chapter_1_has_sample_chapter_ending_template() -> None:
    expected = {
        "docs/book/part-i/chapter-1.md": (
            "Шаблон завершения главы",
            "Что запомнить",
            "Типичные ошибки",
            "Что проверить в своей системе",
            "Сопутствующие материалы",
            "Что читать дальше",
        ),
        "docs/book/part-i/chapter-1.en.md": (
            "Chapter ending template",
            "What to remember",
            "Common mistakes",
            "What to check in your system",
            "Companion assets",
            "What to read next",
        ),
        "docs/book/part-i/chapter-1.zh.md": (
            "章节结尾模板",
            "要记住什么",
            "常见错误",
            "检查自己的系统",
            "Companion assets",
            "接下来读什么",
        ),
    }

    for path, markers in expected.items():
        _assert_files_contain_all((path,), markers)


def test_russian_book_chapters_have_unified_chapter_ending_template() -> None:
    chapter_paths = tuple(
        path
        for path in sorted(Path("docs/book").glob("part-*/chapter-*.md"))
        if not path.name.endswith((".en.md", ".zh.md"))
    )
    required_markers = (
        '!!! summary "Шаблон завершения главы"',
        "Что запомнить:",
        "Типичные ошибки:",
        "Что проверить в своей системе:",
        "Сопутствующие материалы:",
        "Что читать дальше:",
    )

    assert len(chapter_paths) == 27

    missing = []
    for path in chapter_paths:
        text = _read(str(path))
        absent = [marker for marker in required_markers if marker not in text]
        if absent:
            missing.append((str(path), absent))

    assert missing == []


def test_chinese_entry_surfaces_disclose_draft_localization_status() -> None:
    checked_files = (
        "docs/index.zh.md",
        "docs/start-here.zh.md",
        "docs/book/plan.zh.md",
    )
    required_markers = (
        "中文本地化预览",
        "最终中文版",
        "正式出版前",
    )
    forbidden_markers = (
        "Draft localization preview",
        "draft localization preview",
        "finished Chinese edition",
    )

    for path in checked_files:
        text = _read(path)
        for marker in required_markers:
            assert marker in text, (path, marker)
        for marker in forbidden_markers:
            assert marker not in text, (path, marker)


def test_governance_aware_telemetry_contract_is_documented() -> None:
    required_fields = (
        "Governance-aware telemetry",
        "policy_decision_feedback",
        "containment_decision",
        "rollout_gate_input",
        "incident_response_trigger",
        "registry_update_signal",
        "governance_action_id",
        "source_signal",
        "decision_owner",
        "action_state",
        "evidence_refs",
        "review_deadline",
    )
    checked_files = (
        "docs/book/part-viii/chapter-26.md",
        "docs/book/part-viii/chapter-26.en.md",
        "docs/book/part-viii/chapter-26.zh.md",
    )

    for path in checked_files:
        _assert_files_contain_all((path,), required_fields)

    chinese_text = _read("docs/book/part-viii/chapter-26.zh.md")
    expected_chinese_markers = (
        "治理感知遥测（Governance-aware telemetry）",
        "执行闭环（enforcement loop）",
        "策略决策（policy decisions）",
        "遏制（containment）",
        "发布门禁（rollout gates）",
        "事故响应（incident response）",
        "闭环契约（closed-loop contract）",
        "遥测信号（telemetry signals）",
        "策略决策（policy decision）",
        "风险层级（risk tier）",
        "发布波次（rollout wave）",
        "暂停/隔离状态（paused / quarantined state）",
        "漂移信号（drift signals）",
        "调查（investigation）",
        "复盘任务（postmortem task）",
        "影子能力（shadow capabilities）",
        "检测场景（detection scenario）",
        "验证器输出（verifier output）",
        "仪表板信号（dashboard signal）",
        "可审查治理队列（governance queue）",
        "治理闭环（governance loop）",
        "观察（observe）",
        "发布动作（rollout action）",
    )
    for expected_chinese_marker in expected_chinese_markers:
        assert expected_chinese_marker in chinese_text, expected_chinese_marker

    forbidden_chinese_markers = (
        "Governance-aware telemetry 会闭合 enforcement loop",
        "让 telemetry 可以直接服务治理动作",
        "作为 policy decisions、containment、rollout gates 和 incident response 的输入",
        "最小 closed-loop contract",
        "哪些 telemetry signals 会改变后续 policy decision 或 risk tier",
        "rollout wave 置为 paused / quarantined state",
        "哪些 coverage、verifier 和 drift signals",
        "哪些 patterns 会创建 investigation、escalation 或 postmortem task",
        "shadow capabilities 需要更新 inventory",
        "telemetry signal 或 detection scenario",
        "指向 trace、verifier output、policy decision 和 rollout gate",
        "telemetry 就不只是 dashboard signal",
        "可审查 governance queue",
        "telemetry 就不再只是事后的 evidence",
        "governance loop 的运行输入",
        "observe → policy decision → containment 或 rollout action",
    )
    for forbidden_chinese_marker in forbidden_chinese_markers:
        assert forbidden_chinese_marker not in chinese_text, forbidden_chinese_marker


def test_chapter_26_governance_telemetry_maps_to_nist_ai_rmf() -> None:
    common_required_fields = (
        "Govern",
        "Map",
        "Measure",
        "Manage",
        "decision_owner",
        "review_deadline",
        "source_signal",
        "evidence_refs",
        "policy_decision_feedback",
        "containment_decision",
        "rollout_gate_input",
        "incident_response_trigger",
        "[^nist-ai-rmf]",
    )
    english_required_fields = (
        "Mapping the Loop to NIST AI RMF",
        "inventory coverage",
        "bypass-path telemetry",
        "verifier outputs",
        "coverage ratios",
        "drift signals",
        "detection scenarios",
        "control action",
    )
    russian_required_fields = (
        "Наложение контура на NIST AI RMF",
        "покрытие инвентаря",
        "телеметрия путей обхода",
        "выходы проверяющего",
        "доли покрытия",
        "сигналы дрейфа",
        "сценарии обнаружения",
        "итоговое действие контроля",
    )

    _assert_files_contain_all(
        ("docs/book/part-viii/chapter-26.md",),
        (*common_required_fields, *russian_required_fields),
    )
    _assert_files_contain_all(
        ("docs/book/part-viii/chapter-26.en.md",),
        (*common_required_fields, *english_required_fields),
    )
    _assert_files_contain_all(
        ("docs/book/part-viii/chapter-26.zh.md",),
        common_required_fields,
    )

    chinese_text = _read("docs/book/part-viii/chapter-26.zh.md")
    expected_chinese_markers = (
        "将闭环映射到 NIST AI RMF（Mapping the Loop to NIST AI RMF）",
        "闭环（closed loop）",
        "可观测性（observability）",
        "合规清单（compliance checklist）",
        "治理（Govern）",
        "映射（Map）",
        "度量（Measure）",
        "管理（Manage）",
        "注册表覆盖（registry coverage）",
        "治理队列（governance queue）",
        "清单覆盖（inventory coverage）",
        "绕过路径遥测（bypass-path telemetry）",
        "发布表面（rollout surface）",
        "验证器输出（verifier outputs）",
        "覆盖率（coverage ratios）",
        "检测场景（detection scenarios）",
        "可观测证据（observable evidence）",
        "控制动作（control action）",
        "映射（mapping）",
        "可操作（operational）",
        "审查者（reviewer）",
        "风险表面（risk surface）",
        "度量证据（measurement evidence）",
    )
    for expected_chinese_marker in expected_chinese_markers:
        assert expected_chinese_marker in chinese_text, expected_chinese_marker

    forbidden_chinese_markers = (
        "它也应该和 provenance chapter 保持分离",
        "足够的 evidence、coverage 与 correlation",
        "approved artifacts、contract version 或 governed bundle",
        "### 7.2. Mapping the Loop to NIST AI RMF",
        "- **Govern**：",
        "- **Map**：",
        "- **Measure**：",
        "- **Manage**：",
        "这个 closed loop",
        "把 observability 映射到 NIST AI RMF",
        "变成 compliance checklist",
        "registry coverage 说明谁拥有这个 signal",
        "哪条 governance queue",
        "inventory coverage 和 bypass-path telemetry",
        "处于 risk 中的是哪个 agent、capability、tenant 或 rollout surface",
        "verifier outputs、coverage ratios、drift signals 和 detection scenarios",
        "变成 observable evidence",
        "说明 evidence 之后触发了哪项 control action",
        "这个 mapping 故意保持 operational",
        "dashboard 有没有写 Govern",
        "reviewer 是否能把一个 telemetry signal",
        "有没有写 Govern、Map、Measure、Manage",
        "owner、risk surface、measurement evidence 和最终 control action",
    )
    for forbidden_chinese_marker in forbidden_chinese_markers:
        assert forbidden_chinese_marker not in chinese_text, forbidden_chinese_marker


def test_verifier_contract_fields_are_documented() -> None:
    required_fields = (
        "rubric_version",
        "process_score",
        "outcome_score",
        "failure_attribution",
        "judge_human_agreement",
        "false_positive_budget",
        "false_negative_budget",
        "calibration_dataset_id",
        "replay_protocol",
        "verdict_id",
        "verifier_id",
        "verifier_contract_version",
        "input_refs",
        "evidence_refs",
        "blocking_decision",
        "comparison_baseline",
        "reviewer_override",
    )
    checked_files = (
        "docs/book/part-v/chapter-13.md",
        "docs/book/part-v/chapter-13.en.md",
        "docs/book/part-v/chapter-13.zh.md",
    )

    for path in checked_files:
        _assert_files_contain_all((path,), required_fields)


def test_chapter_13_has_technical_sample_orientation_and_compact_exit() -> None:
    expected_by_file = {
        "docs/book/part-v/chapter-13.md": (
            "Как читать эту главу",
            "Ориентир главы",
            "Печатный вывод главы",
            "контракт проверяющего",
            "шлюз раскатки",
            "без живой навигации сайта",
        ),
        "docs/book/part-v/chapter-13.en.md": (
            "How to read this chapter",
            "Chapter orientation",
            "Print-ready chapter exit",
            "verifier contract",
            "rollout gate",
            "without relying on live site navigation",
        ),
        "docs/book/part-v/chapter-13.zh.md": (
            "如何阅读本章",
            "章节导向",
            "适合印刷的章节结尾",
            "验证器契约",
            "发布门禁",
            "不依赖网站实时导航",
        ),
    }

    for path, expected_markers in expected_by_file.items():
        _assert_files_contain_all((path,), expected_markers)


def test_agent_threat_model_matrix_covers_required_classes() -> None:
    required_threats = (
        "Prompt injection",
        "Indirect injection",
        "RAG poisoning",
        "Memory poisoning",
        "Tool abuse",
        "Confused deputy",
        "Excessive agency",
        "Data exfiltration",
        "Denial of wallet",
        "Cascading multi-agent failure",
        "Supply-chain compromise",
        "Missing audit trail",
        "Evidence / telemetry",
        "unified agent threat evidence model",
        "prompt_boundary_event",
        "retrieval_source_id",
        "memory_record_id",
        "delegation_trace_id",
        "tenant_id",
        "cost_budget_event",
        "decision_trace_id",
    )
    checked_files = (
        "docs/book/part-ii/chapter-3.md",
        "docs/book/part-ii/chapter-3.en.md",
        "docs/book/part-ii/chapter-3.zh.md",
    )

    for path in checked_files:
        _assert_files_contain_all((path,), required_threats)


def test_chapter_3_defense_in_depth_map_covers_control_layers() -> None:
    required_markers = (
        "defense_in_depth_map:",
        "ingress_control:",
        "content_policy_and_tenant_scope",
        "context_boundary:",
        "trusted_untrusted_content_labels",
        "retrieval_memory_gate:",
        "source_provenance_ttl_and_write_review",
        "model_gateway_policy:",
        "instruction_hierarchy_and_safety_policy",
        "tool_gateway_approval:",
        "risk_tier_arguments_and_human_gate",
        "mcp_a2a_boundary:",
        "server_contract_and_delegation_contract",
        "egress_filter:",
        "redaction_dlp_and_output_validation",
        "trace_evidence:",
        "agent_threat_evidence_and_governance_action",
        "trace schema",
    )
    checked_files = (
        "docs/book/part-ii/chapter-3.md",
        "docs/book/part-ii/chapter-3.en.md",
        "docs/book/part-ii/chapter-3.zh.md",
    )

    _assert_files_contain_all(checked_files, required_markers)


def test_chapter_3_unified_threat_evidence_trace_links_are_clickable() -> None:
    expected_links_by_file = {
        "docs/book/part-ii/chapter-3.md": "../../appendix/trace-schema.md",
        "docs/book/part-ii/chapter-3.en.md": "../../appendix/trace-schema.en.md",
        "docs/book/part-ii/chapter-3.zh.md": "../../appendix/trace-schema.zh.md",
    }

    for path, expected_link in expected_links_by_file.items():
        assert f"]({expected_link})" in _read(path), (path, expected_link)

    chinese_text = _read("docs/book/part-ii/chapter-3.zh.md")
    assert "[追踪模式（trace schema）](../../appendix/trace-schema.zh.md)" in chinese_text
    assert "[trace schema](../../appendix/trace-schema.zh.md)" not in chinese_text


def test_mcp_threat_model_matrix_covers_required_attacks() -> None:
    expected = {
        "docs/book/part-iv/chapter-9.md": (
            "Матрица угроз для MCP",
            "модель угроз MCP",
            "tool poisoning",
            "rug pull attack",
            "tool shadowing",
            "confused deputy",
            "over-scoped tokens",
            "data exfiltration through legitimate channels",
            "supply-chain attack",
            "replay/tampering",
            "sandbox escape",
            "telemetry",
        ),
        "docs/book/part-iv/chapter-9.en.md": (
            "MCP Threat Model Matrix",
            "MCP threat model",
            "tool poisoning",
            "rug pull attack",
            "tool shadowing",
            "confused deputy",
            "over-scoped tokens",
            "data exfiltration through legitimate channels",
            "supply-chain attack",
            "replay/tampering",
            "sandbox escape",
            "telemetry",
        ),
        "docs/book/part-iv/chapter-9.zh.md": (
            "MCP 威胁模型矩阵",
            "MCP threat model",
            "tool poisoning",
            "rug pull attack",
            "tool shadowing",
            "confused deputy",
            "over-scoped tokens",
            "data exfiltration through legitimate channels",
            "supply-chain attack",
            "replay/tampering",
            "sandbox escape",
            "telemetry",
        ),
    }

    for path, markers in expected.items():
        _assert_files_contain_all((path,), markers)


def test_chapter_9_mcp_server_contract_covers_required_controls() -> None:
    expected_markers = {
        "docs/book/part-iv/chapter-9.md": (
            "Минимальный контракт MCP-сервера",
            "mcp_server:",
            "owner:",
            "approved_registry_id:",
            "schema_hash:",
            "tool_definition_hash:",
            "allowed_origins:",
            "auth_mode:",
            "token_scope:",
            "token_ttl:",
            "user_delegation_required:",
            "server_isolation_profile:",
            "return_value_filtering:",
            "replay_protection:",
            "schema_change_requires_review:",
            "внедрение схемы инструмента",
            "внедрение инструкций через результаты инструментов",
        ),
        "docs/book/part-iv/chapter-9.en.md": (
            "Minimal MCP Server Contract",
            "mcp_server:",
            "owner:",
            "approved_registry_id:",
            "schema_hash:",
            "tool_definition_hash:",
            "allowed_origins:",
            "auth_mode:",
            "token_scope:",
            "token_ttl:",
            "user_delegation_required:",
            "server_isolation_profile:",
            "return_value_filtering:",
            "replay_protection:",
            "schema_change_requires_review:",
            "tool schema injection",
            "prompt injection",
        ),
        "docs/book/part-iv/chapter-9.zh.md": (
            "最小 MCP server contract",
            "mcp_server:",
            "owner:",
            "approved_registry_id:",
            "schema_hash:",
            "tool_definition_hash:",
            "allowed_origins:",
            "auth_mode:",
            "token_scope:",
            "token_ttl:",
            "user_delegation_required:",
            "server_isolation_profile:",
            "return_value_filtering:",
            "replay_protection:",
            "schema_change_requires_review:",
            "tool schema injection",
            "prompt injection",
        ),
    }

    for path, markers in expected_markers.items():
        _assert_files_contain_all((path,), markers)


def test_russian_chapter_9_prefers_reader_facing_mcp_contract_terms() -> None:
    text = _read("docs/book/part-iv/chapter-9.md")
    expected_markers = (
        "MCP — это граница безопасности",
        "результаты инструментов",
        "инструменты и ресурсы",
        "операции записи требуют подтверждения",
        "области доступа, сетевые пути и ограничения песочницы",
        "среда исполнения валидирует описания инструментов и результаты инструментов",
        "телеметрия доказывает, какой запуск агента",
        "Матрица угроз для MCP",
        "модель угроз MCP",
        "Минимальный контракт MCP-сервера",
        "проверяемый серверный артефакт",
        "одобренную точку подключения",
        "неявным контуром доверия внутри поверхности платформы",
        "отделять результаты инструментов от инструкций и держать список разрешенных контрактов",
        "ранее одобренный MCP-сервер меняет инструменты, области доступа или поведение",
        "новый инструмент маскируется под похожий одобренный инструмент",
        "слишком широкими делегированными полномочиями",
        (
            "проверка субъекта, привязки к цели, состояния подтверждения и "
            "решения политики прямо перед побочным эффектом"
        ),
        "какой след останется в телеметрии после инцидента",
        "Полезно не путать узел, клиент и сервер MCP",
        "`host` - это узел",
        "`client` - это протокольный компонент, который узел создает",
        "`server` - это граница",
        "один узел может одновременно держать несколько клиентов",
        "MCP-клиент — это не пользовательский интерфейс",
    )
    forbidden_markers = (
        "MCP — это security boundary",
        "tool results",
        "tools/resources",
        "операции записи требуют approval",
        "scopes, network paths и sandbox limits",
        "runtime валидирует tool descriptions и tool return values",
        "telemetry доказывает, какой agent run, identity и policy decision",
        "MCP threat model matrix",
        "Минимальный контракт MCP server",
        "server artifact",
        "approved endpoint",
        "trust boundary внутри platform surface",
        (
            "валидировать tool descriptions, отделять tool output от инструкций "
            "и держать allowlist известных контрактов"
        ),
        "MCP server меняет инструменты, scopes или поведение",
        "новый tool маскируется под похожий approved tool",
        "уникальные capability names, registry ownership и semantic review",
        "слишком широкой delegated authority",
        (
            "проверка principal, purpose binding, approval state и policy "
            "decision прямо перед side effect"
        ),
        "MCP endpoint",
        "telemetry после инцидента",
        "MCP host, client и server",
        "`client` - это протокольный компонент, который host создает",
        "MCP client — это не пользовательский интерфейс",
    )

    for marker in expected_markers:
        assert marker in text, marker

    for marker in forbidden_markers:
        assert marker not in text, marker


def test_chapter_9_mcp_threat_model_trace_links_are_clickable() -> None:
    expected_links_by_file = {
        "docs/book/part-iv/chapter-9.md": "../../appendix/trace-schema.md",
        "docs/book/part-iv/chapter-9.en.md": "../../appendix/trace-schema.en.md",
        "docs/book/part-iv/chapter-9.zh.md": "../../appendix/trace-schema.zh.md",
    }

    for path, expected_link in expected_links_by_file.items():
        assert f"]({expected_link})" in _read(path), (path, expected_link)

    chinese_text = _read("docs/book/part-iv/chapter-9.zh.md")
    assert (
        "[MCP 威胁模型（MCP threat model）](../../appendix/trace-schema.zh.md)"
        in chinese_text
    )
    assert "[MCP threat model](../../appendix/trace-schema.zh.md)" not in chinese_text


def test_mcp_a2a_security_governance_sections_are_present() -> None:
    expected = {
        "docs/book/part-iv/chapter-9.md": (
            "MCP — это граница безопасности",
            "описания инструментов и результаты инструментов",
        ),
        "docs/book/part-iv/chapter-9.en.md": (
            "MCP Is a Security Boundary",
            "tool descriptions and tool return values",
        ),
        "docs/book/part-iv/chapter-9.zh.md": (
            "MCP 是安全边界",
            "tool descriptions 和 tool return values",
        ),
        "docs/book/part-iv/practical-mcp-a2a.md": (
            "A2A требует управления",
            "контракт доверия для передачи управления A2A",
            "делегированных полномочий",
            "agent identity",
            "цепочка делегирования",
            "граф разрешенного взаимодействия",
            "межагентная авторизация",
            "наследование политик",
            "неотказуемость",
            "атрибуция сбоев",
        ),
        "docs/book/part-iv/practical-mcp-a2a.en.md": (
            "A2A Needs Governance",
            "A2A handoff trust contract",
            "delegated authority",
            "agent identity",
            "delegation chain",
            "allowed collaboration graph",
            "inter-agent authorization",
            "policy inheritance",
            "non-repudiation",
            "failure attribution",
        ),
        "docs/book/part-iv/practical-mcp-a2a.zh.md": (
            "A2A 需要治理",
            "A2A handoff trust contract",
            "delegated authority",
            "agent identity",
            "delegation chain",
            "allowed collaboration graph",
            "inter-agent authorization",
            "policy inheritance",
            "non-repudiation",
            "failure attribution",
        ),
    }

    for path, markers in expected.items():
        _assert_files_contain_all((path,), markers)

    russian_practical_text = _read("docs/book/part-iv/practical-mcp-a2a.md")
    assert "A2A требует governance" not in russian_practical_text
    assert "A2A handoff trust contract" not in russian_practical_text
    assert "delegation chain" not in russian_practical_text
    assert "non-repudiation" not in russian_practical_text


def test_russian_practical_a2a_diagram_uses_localized_labels() -> None:
    text = _read("docs/book/part-iv/practical-mcp-a2a.md")

    expected_markers = (
        'A["Координирующий агент"]',
        'B["Передача управления A2A"]',
        'C["Специализированный агент"]',
        'D["MCP-клиент"]',
        'F["Сервер инструментов / ресурсов"]',
    )
    forbidden_markers = (
        'A["Coordinator agent"]',
        'B["A2A handoff"]',
        'C["Specialist agent"]',
        'D["MCP client"]',
        'F["Tool / resource server"]',
    )

    for marker in expected_markers:
        assert marker in text, marker
    for marker in forbidden_markers:
        assert marker not in text, marker


def test_practical_a2a_trust_delegation_contract_covers_required_controls() -> None:
    required_fields = (
        "A2A trust and delegation artifact",
        "a2a_trust_delegation:",
        "remote_agent_id:",
        "remote_agent_owner:",
        "trust_tier:",
        "allowed_tasks:",
        "forbidden_tasks:",
        "delegation_depth:",
        "context_sharing_policy:",
        "memory_sharing_policy:",
        "tool_access_via_remote_agent:",
        "approval_propagation:",
        "audit_correlation_id:",
        "failure_attribution:",
        "revocation_policy:",
        "delegation laundering",
        "context over-sharing",
        "remote-agent impersonation",
        "unbounded delegation chains",
        "conflicting actions",
        "lost accountability",
        "cross-agent prompt injection",
    )
    checked_files = (
        "docs/book/part-iv/practical-mcp-a2a.md",
        "docs/book/part-iv/practical-mcp-a2a.en.md",
        "docs/book/part-iv/practical-mcp-a2a.zh.md",
    )

    _assert_files_contain_all(checked_files, required_fields)


def test_practical_a2a_handoff_trust_trace_links_are_clickable() -> None:
    expected_links_by_file = {
        "docs/book/part-iv/practical-mcp-a2a.md": "../../appendix/trace-schema.md",
        "docs/book/part-iv/practical-mcp-a2a.en.md": "../../appendix/trace-schema.en.md",
        "docs/book/part-iv/practical-mcp-a2a.zh.md": "../../appendix/trace-schema.zh.md",
    }

    for path, expected_link in expected_links_by_file.items():
        assert f"]({expected_link})" in _read(path), (path, expected_link)

    chinese_text = _read("docs/book/part-iv/practical-mcp-a2a.zh.md")
    assert (
        "[A2A 交接信任合约（A2A handoff trust contract）]"
        "(../../appendix/trace-schema.zh.md)" in chinese_text
    )
    assert (
        "[A2A handoff trust contract](../../appendix/trace-schema.zh.md)"
        not in chinese_text
    )


def test_russian_practical_pages_prefer_reader_facing_terminology() -> None:
    practical_text = _read("docs/book/part-iv/practical-mcp-a2a.md")
    evidence_text = _read("docs/book/part-v/evidence-spine.md")

    _assert_files_contain_all(
        ("docs/book/part-iv/practical-mcp-a2a.md",),
        (
            "инструментами, ресурсами и адаптерами",
            "внешних возможностей",
            "контракты возможностей",
            "проверки политик",
            "протокола передачи управления",
            "операционными ролями",
            "A2A требует управления",
            "контракт доверия для передачи управления A2A",
            "цепочка делегирования",
            "наследование политик",
            "неотказуемость",
            "телеметрия различает ошибку инициатора",
            "управляемым графом взаимодействия",
            "Проверяемый артефакт доверия и делегирования для A2A",
            "обычном слое шлюза и адаптеров",
        ),
    )
    for marker in (
        "A2A требует governance",
        "A2A handoff trust contract",
        "delegation chain",
        "downstream agent",
        "non-repudiation",
        "trace/evidence",
        "policy denial",
        "tool failure",
        "collaboration graph",
        "A2A trust and delegation artifact",
        "gateway/adaptor layer",
    ):
        assert marker not in practical_text, marker
    _assert_files_contain_all(
        ("docs/book/part-v/evidence-spine.md",),
        (
            (
                "В производственной агентной системе трассировку, политики, "
                "подтверждения, оценки, разбор инцидентов"
            ),
            "один сквозной разбор",
            "от запроса пользователя до суждения о поэтапном выпуске",
            "Сильная цепочка доказательств",
        ),
    )

    forbidden_practical_markers = (
        "tools, resources и adapters",
        "external capability",
        "стандартизировать contract;",
        "adapters от core runtime",
        "governance, а не только handoff-протокола",
        "между operational roles",
    )
    forbidden_evidence_markers = (
        (
            "production agent system tracing, policy, approvals, evals, "
            "incident review и rollout judgment"
        ),
        "в один walkthrough",
        "от user request до rollout judgment",
        "Сильная evidence spine",
    )

    for marker in forbidden_practical_markers:
        assert marker not in practical_text
    for marker in forbidden_evidence_markers:
        assert marker not in evidence_text


def test_russian_practical_pages_localize_deeper_reader_facing_prose() -> None:
    practical_text = _read("docs/book/part-iv/practical-mcp-a2a.md")
    evidence_text = _read("docs/book/part-v/evidence-spine.md")

    _assert_files_contain_all(
        ("docs/book/part-iv/practical-mcp-a2a.md",),
        (
            "набор инструментов",
            "результат вызова инструмента",
            "еще один адаптер",
            "контракт управления для A2A",
            "контракт доверия для передачи управления A2A",
            "выявление возможностей",
            "журнал аудита для передачи управления",
            "проверки политик",
            "по какой политике и с какой областью действия",
            "не равно независимой проверке",
            "типизированный контракт для инструментов",
            "изолировать адаптер и путь политики",
            "другой среде исполнения агента",
            "Агент работает с инструментами через `MCP`",
            "политики и аудит должны покрывать оба направления",
            "собственного контура политик",
            "операционной идентичности",
            "контракт возможностей",
            "Это разные правила работы",
            "цепочка делегирования",
            "наследование политик",
            "управляемым графом взаимодействия",
            "Проверяемый артефакт доверия и делегирования для A2A",
            "обычном слое шлюза и адаптеров",
            "новый агент или просто новая возможность",
            "контур политик и жизненный цикл",
            "Это проблема делегирования или интеграции",
            "работу агента с инструментами",
            "взаимодействие между агентами",
            "внешний API или ресурс",
            "стабильный идентификатор агента `agent_id`",
        ),
    )
    _assert_files_contain_all(
        ("docs/book/part-v/evidence-spine.md",),
        (
            "подозрительный запуск",
            "цепочки доказательств",
            "оценки и суждение о поэтапном выпуске",
            "поведение среды исполнения",
            "артефакты жизненного цикла",
            "Как минимум один управляемый запуск",
            "в среде исполнения",
            "цепочка событий",
            "связанный утвержденный артефакт",
            "набор контрактов проверяющего",
            "границу сброса контекста или передачи роли",
            "Полезно мыслить цепочку доказательств",
            "запуск разбора обращений поддержки",
            "по производственному инциденту клиента",
            "поверхность выпуска",
            "возможность для данного арендатора и действующего лица",
            "поиск по внутренним знаниям",
            "делегированная авторизация",
            "для обработки высокого риска",
            "Слой политик",
            "События среды исполнения",
            "сырого набора доказательств",
            "какие входные данные были приняты или отклонены",
            "какие вызовы инструментов были сделаны",
            "ставилась ли сессия на паузу",
            "описании для оператора",
            "разбор оценки вне сети",
            "оценки в сети",
            "сравнение с регрессией",
            "отдельный лист оценок",
            "утверждение отклонено",
            "утверждение просрочено",
            "Если запуск выявил серьезную проблему",
            "оператор должен быстро ответить",
            "сбор сырых доказательств",
            "проверяемое суждение",
            "реагирование в контуре заверения",
            "линия происхождения артефактов",
        ),
    )

    forbidden_practical_markers = (
        "набор tools",
        "payload tool-а",
        "agent-а",
        "governance-контракт",
        "capability discovery",
        "audit trail",
        "по какой policy и с каким scope",
        "Согласие нескольких agents",
        "typed contract для tools",
        "изолировать adapter и policy path",
        "другому agent runtime",
        "агент работает с tools через `MCP`",
        "policy и audit должны покрывать оба направления",
        "policy surface",
        "operational identity",
        "capability contract",
        "operational semantics",
        "новый agent или просто новый capability",
        "policy surface и lifecycle",
        "delegation problem или integration problem",
        "agent-to-tool",
        "agent-to-agent",
        "внешний API или resource",
        "стабильный `agent id`",
        "собственной поверхности политик",
        "поверхность политик и жизненный цикл",
        "A2A handoff trust contract",
        "`delegation chain`",
        "downstream agent",
        "collaboration graph",
        "A2A trust and delegation artifact",
        "gateway/adaptor layer",
    )
    forbidden_evidence_markers = (
        "подозрительный run",
        "evidence spine",
        "policy, approvals, evals, incidents и rollout judgment",
        "runtime behavior",
        "lifecycle artifacts",
        "Как минимум один управляемый run",
        "в runtime",
        "event lineage",
        "approved artifact",
        "verifier contracts",
        "context reset или role handoff",
        "Полезно мыслить evidence spine",
        "run разбора обращений поддержки",
        "ticket по production-инциденту клиента",
        "release surface",
        "capability для данного tenant и actor",
        "internal knowledge retrieval",
        "delegated authorization",
        "high-risk handling",
        "Policy, это не просто",
        "Runtime извлекает контекст",
        "сырого evidence",
        "какие inputs были приняты или отклонены",
        "какие tool calls были сделаны",
        "была ли pause в session",
        "operator-facing summary",
        "offline review",
        "online grading",
        "regression comparison",
        "disconnected score sheet",
        "approval denied",
        "approval expired",
        "Если run выявил серьезную проблему",
        "operator должен быстро ответить",
        "raw evidence capture",
        "reviewable judgment",
        "assurance response",
        "artifact lineage",
    )

    for marker in forbidden_practical_markers:
        assert marker not in practical_text
    for marker in forbidden_evidence_markers:
        assert marker not in evidence_text


def test_chapter_1_decision_frame_is_extraction_safe() -> None:
    checked_files = (
        "docs/book/part-i/chapter-1.md",
        "docs/book/part-i/chapter-1.en.md",
        "docs/book/part-i/chapter-1.zh.md",
    )
    forbidden_table_headers = (
        "| Как выглядит задача |",
        "| If the task looks like this |",
        "| 任务看起来像什么 |",
    )
    required_text_markers = (
        "Текстовая формула выбора",
        "Text-only formula",
        "文本版公式",
    )
    required_step_markers = {
        "docs/book/part-i/chapter-1.md": (
            "### Рабочий процесс",
            "### Одиночный агентный цикл",
            "### Многоагентная схема",
        ),
        "docs/book/part-i/chapter-1.en.md": (
            "### Workflow",
            "### Single-agent loop",
            "### Multi-agent architecture",
        ),
        "docs/book/part-i/chapter-1.zh.md": (
            "### 工作流",
            "### 单智能体循环",
            "### 多智能体架构",
        ),
    }

    for path in checked_files:
        text = _read(path)
        assert not any(header in text for header in forbidden_table_headers), path
        for marker in required_step_markers[path]:
            assert marker in text, (path, marker)
    for path, marker in zip(checked_files, required_text_markers, strict=True):
        assert marker in _read(path), (path, marker)


def test_chapter_1_has_claim_evidence_and_diagram_fallback() -> None:
    expected = {
        "docs/book/part-i/chapter-1.md": (
            "Проверяемые утверждения главы",
            "Текстовый дубль схемы",
            "утверждение",
            "опора",
        ),
        "docs/book/part-i/chapter-1.en.md": (
            "Reviewable Claims in This Chapter",
            "Text fallback for the diagram",
            "claim",
            "source support",
        ),
        "docs/book/part-i/chapter-1.zh.md": (
            "本章可核查主张",
            "图示的文本补充",
            "主张",
            "来源支撑",
        ),
    }

    for path, markers in expected.items():
        _assert_files_contain_all((path,), markers)


def test_russian_chapter_1_uses_print_facing_vocabulary() -> None:
    chapter_body = _read("docs/book/part-i/chapter-1.md").split("\n[^", maxsplit=1)[0]
    visible_body = re.sub(r"\[\^[^\]]+\]", "", chapter_body)
    forbidden_terms = (
        "LLM",
        "API",
        "SDK",
        "демо",
        "Демо",
        "кейс",
        "Кейс",
        "тикет",
        "Тикет",
        "таймаут",
        "паттерн",
        "фреймворк",
        "рантайм",
        "workflow",
        "single-agent",
        "multi-agent",
        "runtime",
        "policy",
        "trace",
        "eval",
        "rollout",
        "metadata",
        "framework",
    )

    for term in forbidden_terms:
        pattern = rf"(?<![0-9A-Za-zА-Яа-яЁё_-]){re.escape(term)}(?![0-9A-Za-zА-Яа-яЁё_-])"
        assert re.search(pattern, visible_body) is None, term


def test_fast_moving_pages_have_may_2026_review_metadata() -> None:
    fast_moving_pages = (
        "docs/book/part-iv/chapter-9.md",
        "docs/book/part-iv/chapter-9.en.md",
        "docs/book/part-iv/chapter-9.zh.md",
        "docs/book/part-v/chapter-13.md",
        "docs/book/part-v/chapter-13.en.md",
        "docs/book/part-v/chapter-13.zh.md",
        "docs/book/part-viii/chapter-20.md",
        "docs/book/part-viii/chapter-20.en.md",
        "docs/book/part-viii/chapter-20.zh.md",
        "docs/book/part-viii/chapter-21.md",
        "docs/book/part-viii/chapter-21.en.md",
        "docs/book/part-viii/chapter-21.zh.md",
        "docs/book/part-viii/chapter-22.md",
        "docs/book/part-viii/chapter-22.en.md",
        "docs/book/part-viii/chapter-22.zh.md",
        "docs/book/part-viii/chapter-24.md",
        "docs/book/part-viii/chapter-24.en.md",
        "docs/book/part-viii/chapter-24.zh.md",
        "docs/book/part-viii/chapter-25.md",
        "docs/book/part-viii/chapter-25.en.md",
        "docs/book/part-viii/chapter-25.zh.md",
        "docs/book/part-viii/chapter-26.md",
        "docs/book/part-viii/chapter-26.en.md",
        "docs/book/part-viii/chapter-26.zh.md",
        "docs/book/part-viii/chapter-27.md",
        "docs/book/part-viii/chapter-27.en.md",
        "docs/book/part-viii/chapter-27.zh.md",
    )
    stale_markers = (
        "11 апреля 2026 года",
        "April 11, 2026",
        "2026 年 4 月 11 日",
    )

    for path in fast_moving_pages:
        text = _read(path)
        assert not any(marker in text for marker in stale_markers), path
        assert any(
            marker in text
            for marker in (
                "14 мая 2026 года",
                "May 14, 2026",
                "2026 年 5 月 14 日",
            )
        ), path

    _assert_files_contain_all(
        (
            "docs/appendix/sources.md",
            "docs/appendix/sources.en.md",
            "docs/appendix/sources.zh.md",
            "docs/whats-new.md",
            "docs/whats-new.en.md",
            "docs/whats-new.zh.md",
        ),
        ("2026",),
    )
    assert "22 апреля 2026 года" not in _read("docs/appendix/sources.md")
    assert "April 22, 2026" not in _read("docs/appendix/sources.en.md")
    assert "2026 年 4 月 22 日" not in _read("docs/appendix/sources.zh.md")
    assert "29 апреля 2026 года" not in _read("docs/whats-new.md")
    assert "April 29, 2026" not in _read("docs/whats-new.en.md")
    assert "2026 年 4 月 29 日" not in _read("docs/whats-new.zh.md")


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

    _assert_files_contain_all(checked_files, required_errors)


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

    _assert_files_contain_all(checked_files, required_errors)


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

    _assert_files_contain_all(checked_files, required_errors)


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

    _assert_files_contain_all(checked_files, required_errors)


def test_memory_schema_loader_root_error_is_documented() -> None:
    checked_files = (
        "docs/appendix/memory-retrieval-schema.md",
        "docs/appendix/memory-retrieval-schema.en.md",
        "docs/appendix/memory-retrieval-schema.zh.md",
    )

    for path in checked_files:
        assert "Memory store config must be a mapping" in _read(path), path


def test_russian_memory_retrieval_schema_prefers_reader_facing_terms() -> None:
    russian_text = _read("docs/appendix/memory-retrieval-schema.md")

    expected_markers = (
        "схема артефактов жизненного цикла",
        "среда исполнения решила вернуть в контекст",
        "команда `inspect-memory`",
        "встроенные типы записей",
        "эталонные исходные записи",
        "непрофильные исходные записи",
        "прямое построение хранилища памяти",
        "неправильные внедренные записи",
        "неправильные прямые кандидаты",
        "стабильные сообщения об ошибках",
        "Книга не только описывает этот контракт, но и показывает исполняемый эталонный каркас.",
    )
    forbidden_markers = (
        "схема lifecycle-артефактов",
        "рантайм решил вернуть в контекст",
        "- CLI:",
        "встроенные виды",
        "Непрофильное исходное содержимое",
        "некорректные внедренные записи",
        "некорректных прямых кандидатов",
        "стабильные ошибки",
        "Книга не только описывает этот контракт, но и показывает исполняемый каркас.",
    )

    for marker in expected_markers:
        assert marker in russian_text, marker
    for marker in forbidden_markers:
        assert marker not in russian_text, marker


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

    _assert_files_contain_all(checked_files, required_errors)


def test_reference_package_has_reader_route_contract() -> None:
    expected_markers_by_file = {
        "docs/appendix/reference-package.md": (
            "Маршрут чтения",
            "Быстрый запуск",
            "Архитектурная карта",
            "Примеры команд",
            "Контракты конфигураций",
            "Расширенный контроль жизненного цикла",
            "Внутреннее устройство среды выполнения",
        ),
        "docs/appendix/reference-package.en.md": (
            "Reader-route contract",
            "Quick start",
            "Architecture map",
            "CLI examples",
            "Config contracts",
            "Advanced lifecycle-controls",
            "Runtime internals",
        ),
        "docs/appendix/reference-package.zh.md": (
            "Reader-route contract",
            "Quick start",
            "Architecture map",
            "CLI examples",
            "Config contracts",
            "Advanced lifecycle-controls",
            "Runtime internals",
        ),
    }

    for path, expected_markers in expected_markers_by_file.items():
        text = _read(path)
        for expected_marker in expected_markers:
            assert expected_marker in text, (path, expected_marker)


def test_reference_package_rollout_errors_are_documented() -> None:
    required_errors = (
        "Rollout policy must be RolloutPolicy",
        "Rollout readiness must be RolloutReadiness",
        "Rollout readiness flag must be a boolean: {field}",
    )
    checked_files = (
        "docs/appendix/reference-package.md",
        "docs/appendix/reference-package.en.md",
        "docs/appendix/reference-package.zh.md",
    )

    _assert_files_contain_all(checked_files, required_errors)


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

    _assert_files_contain_all(checked_files, required_errors)


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

    _assert_files_contain_all(checked_files, required_errors)


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

    _assert_files_contain_all(checked_files, required_errors)


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
