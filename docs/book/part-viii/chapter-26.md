# Глава 26. AI-native observability, inventory coverage и detection-ready telemetry

## 1. Почему observability для агентов нельзя сводить к latency и errors

В обычном сервисе observability часто начинается с простого набора:

- latency;
- error rate;
- throughput;
- resource utilization.

Для agent systems этого недостаточно.

Система может:

- не падать;
- отвечать быстро;
- отдавать HTTP 200;
- и при этом вести себя опасно, некачественно или неуправляемо.

Microsoft точно формулирует этот сдвиг: для agentic systems нужно эволюционировать от обычных logs, metrics и traces к `AI-native signals`, которые помогают восстанавливать не только факт запроса, но и форму поведения системы. [^ms-observability]

## 2. Observability здесь нужна не только для дебага

У agent platform observability играет как минимум пять ролей:

- runtime debugging;
- incident reconstruction;
- abuse detection;
- release evidence;
- governance coverage.

Если traces существуют только для разработчика, который локально ищет баг, этого уже недостаточно.

В production тебе нужно уметь отвечать и на другие вопросы:

- сколько agents вообще существует;
- какой процент из них вообще наблюдаем;
- какие capabilities они реально вызывают;
- где идут high-risk actions;
- какие approvals были запрошены, одобрены или обойдены;
- какие behavior shifts появились после rollout.

## 3. Что такое AI-native signals

Для agent systems полезный telemetry contract обычно включает:

- request identity;
- `run_id`, `trace_id`, `session_id`;
- actor и agent identity;
- retrieval provenance;
- tool invocations;
- tool permissions и principals;
- policy decisions;
- approvals;
- output summaries;
- redaction status;
- bundle, version и rollout wave.

То есть traces должны рассказывать не только “что упало”, но и:

- кто действовал;
- через какой control layer;
- с какими правами;
- по каким правилам;
- в рамках какого artifact bundle;
- и с каким side effect.

## 4. Inventory coverage — это тоже observability

Есть важная мысль, которую часто упускают: observability начинается не с красивого trace viewer, а с понимания, какие systems вообще существуют.

Microsoft отдельно подчеркивает complete production inventory как prerequisite для trusted telemetry. [^ms-inventory]

Для agent estate это означает, что ты должен знать:

- какие agents активны;
- какие уже deprecated;
- какие connectors и capabilities у них есть;
- какие principals они используют;
- какие из них вообще шлют telemetry;
- какие blind spots остаются.

Если у тебя нет inventory coverage, у тебя нет полноценной observability. У тебя есть только частично освещенная сцена.

## 5. Behavioral baselines важнее raw volume

В agent systems сигнал “у нас стало больше запросов” сам по себе мало что значит.

Гораздо важнее уметь видеть отклонение от нормального поведения:

- неожиданное увеличение risky tool calls;
- рост approval denials;
- изменение memory write pattern;
- смену обычного retrieval profile;
- всплеск unusual egress destinations;
- рост session length или tool hop count.

Именно здесь observability начинает пересекаться с security detection и operational governance.

## 6. Что значит detection-ready telemetry

`Detection-ready telemetry` — это не просто “мы что-то логируем”.

Это значит, что telemetry уже годится для:

- расследования;
- correlation;
- abuse detection;
- control verification.

Практически это означает:

- единые identifiers;
- стабильные schemas;
- redaction rules;
- retention policy;
- linkage между traces, approvals, policy decisions и lifecycle artifacts.

Если trace нельзя связать с `approval_id`, `tool_principal`, `policy_bundle` и `rollout_wave`, то он может быть полезен для отладки, но все еще слаб как evidence layer.

## 7. Почему governance без observability почти всегда хрупкая

Governance нередко оформляют как:

- policy bundles;
- review processes;
- release gates;
- approval contracts.

Но без наблюдаемости все это слишком легко превращается в бумажный контур.

Сильная governance требует:

- видеть фактическое поведение;
- замечать drift;
- измерять coverage;
- отличать governed path от bypass path.

Поэтому observability в agent systems лучше воспринимать как `evidence layer for governance`.

## 8. Куда frontier двигает observability дальше

Свежие research papers по observability для agents идут еще дальше: они пытаются превратить traces из удобного журнала событий в слой причинной диагностики.

Из этого для книги полезны две мысли.

Первая: одного trace viewer недостаточно. Красивый UI вокруг event stream еще не дает answerability, если:

- trace vocabulary слишком бедный;
- run нельзя связать с session, approval и artifact bundle;
- root cause все равно приходится восстанавливать вручную по длинному transcript.

Вторая: causal diagnosis выглядит перспективно, но ее пока рано считать solved problem. Research уже показывает интересный путь вперед, но production discipline по-прежнему должна стоять на более приземленных вещах:

- stable event catalog;
- schema versioning;
- redaction rules;
- session-aware traces;
- явные linkage между telemetry, approvals и lifecycle artifacts.

То есть frontier здесь полезен не как повод обещать “полную explainability”, а как напоминание, что observability должна постепенно эволюционировать от logging к diagnosability.

<div class="diagram-card">
<p>AI-native observability лучше думать как связку telemetry, inventory и governance evidence</p>

``` mermaid
flowchart LR
    A["Inventory coverage"] --> D["AI-native observability"]
    B["Runtime telemetry"] --> D
    C["Policy and approval evidence"] --> D
    D --> E["Incident reconstruction"]
    D --> F["Behavioral baselines"]
    D --> G["Abuse detection"]
    D --> H["Release evidence"]
```

</div>

## 9. Минимальный policy для observability coverage

```yaml
observability:
  require:
    request_identity: true
    trace_ids: true
    session_ids: true
    policy_decisions: true
    tool_principals: true
    approval_linkage: true
    artifact_bundle_linkage: true
  kpis:
    min_agent_inventory_coverage_pct: 95
    min_trace_coverage_pct: 95
    min_high_risk_action_trace_pct: 100
  block_if:
    - untracked_high_risk_agent_exists
    - approval_events_not_linked
    - bundle_version_missing
```

Такой policy помогает обсуждать observability как обязательный production layer, а не как nice-to-have для платформенной команды.

## 10. Пример простого coverage check

```python
from dataclasses import dataclass


@dataclass
class ObservabilityCoverage:
    inventory_coverage_pct: int
    trace_coverage_pct: int
    high_risk_trace_coverage_pct: int


def observability_ready(state: ObservabilityCoverage) -> bool:
    return (
        state.inventory_coverage_pct >= 95
        and state.trace_coverage_pct >= 95
        and state.high_risk_trace_coverage_pct == 100
    )
```

Здесь идея не в цифрах как таковых. Идея в том, что observability readiness тоже должна становиться явным gate.

## 11. Самые частые failure modes

- traces есть только у “основного” runtime, но не у реальных adapters;
- agents существуют вне inventory;
- approvals логируются отдельно и не связываются с traces;
- telemetry покрывает happy path, но не bypass path;
- drift замечают только по жалобам пользователей;
- retention и redaction rules не согласованы с forensic needs.

## 12. Практический checklist

- Знаешь ли ты, сколько agents реально живет в production estate?
- Какой процент из них вообще шлет structured telemetry?
- Можно ли связать high-risk action с `trace_id`, `approval_id`, `tool_principal` и `bundle_id`?
- Есть ли behavioral baselines, а не только raw dashboards?
- Видишь ли ты unobserved agents как отдельный risk class?
- Можешь ли ты использовать observability как release evidence, а не только как debug aid?

Если несколько ответов подряд “нет”, то observability у тебя уже есть, но она пока не стала governance layer.

## 13. Полезные справочные страницы

- [Схема трасс и каталог событий](../../appendix/trace-schema.md)
- [Схема eval datasets и grading contract](../../appendix/eval-schema.md)
- [Схема policy bundle и approval contract](../../appendix/policy-bundle-schema.md)
- [Схема change review и rollout gate](../../appendix/change-rollout-schema.md)
- [Research frontier: память, наблюдаемость и надежность multi-agent систем](../../appendix/research-frontier.md)

- [Глава 11. Трассы, спаны и структурированные события](../part-v/chapter-11.md)
- [Глава 13. Офлайн-оценки, онлайн-оценки и регрессионные шлюзы](../part-v/chapter-13.md)
- [Глава 21. Assurance loop: red teaming, detection и response](chapter-21.md)

[^ms-observability]: Microsoft Learn, [Observability for Generative AI and agentic AI systems](https://learn.microsoft.com/en-us/security/zero-trust/sfi/observability-ai-systems)
[^ms-inventory]: Microsoft Learn, [Complete production infrastructure inventory](https://learn.microsoft.com/en-us/security/zero-trust/sfi/complete-production-infrastructure-inventory)
