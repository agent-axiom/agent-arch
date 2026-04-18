# Глава 22. Цепочка поставки, происхождение и доверенные артефакты

!!! info "Актуальность главы"
    Эта глава актуальна на 11 апреля 2026 года.

    Быстрее всего здесь меняются:

    - инструменты аттестации, подписи и provenance для моделей и конфигураций;
    - вендорские функции для artifact governance и managed supply-chain controls;
    - практики описания prompt-, policy- и eval-артефактов как reviewable units.

    Медленнее меняются:

    - требование иметь owner, provenance и review status у каждого доверенного артефакта;
    - идея нескольких цепочек доверия вместо одной общей;
    - связь supply chain с incident review, change management и rollout discipline.

## 1. Почему у агентных систем цепочка поставки шире, чем у обычного сервиса

Когда инженеры слышат слова «цепочка поставки ПО», они обычно думают о знакомых вещах:

- пакетные зависимости;
- контейнеры;
- артефакты CI/CD;
- подписи и происхождение для результатов сборки.

Для агентных систем этого мало.

Проблема в том, что рабочее поведение здесь зависит не только от кода. На него влияют еще:

- маршруты к моделям;
- наборы prompt- и routine-правил;
- конфигурации политик;
- корпуса для извлечения;
- контракты возможностей;
- наборы для оценки;
- verifier contracts, rubric definitions и rules для evidence linkage;
- правила и схемы подтверждения;
- схемы runtime-control;
- правила governance для orchestration pattern и определения worker-safe catalog;
- правила interruption и re-initialization для capability sessions;
- наборы для раскатки.

То есть цепочка поставки у агента шире, потому что сама система шире.

## 2. Что такое доверенный артефакт в агентной системе

Полезно заранее дать очень прямое определение:

Доверенный артефакт — это любой артефакт, который разрешено использовать в промышленной среде, потому что у него есть владелец, происхождение, статус проверки и понятная рабочая роль.

Это означает, что доверенные артефакты — это не только образы или wheel-файлы.

В агентной платформе к ним часто относятся:

- утвержденный маршрут к модели;
- утвержденный набор prompt-правил;
- утвержденный набор политик;
- утвержденный контракт возможности;
- утвержденная approval schema;
- утвержденная runtime-control schema;
- утвержденный источник для извлечения;
- утвержденный набор для оценки;
- утвержденный шаблон раскатки.

Если у команды нет такой категории, она очень быстро начинает жить в неявной системе доверия: «Кажется, это нормальный артефакт, потому что кто-то его уже использовал».

## 3. Происхождение нужно для ответа на очень практичные вопросы

Google Research очень правильно показывает, что происхождение для ИИ-систем полезно не только как формальная идея безопасности, а как рабочая необходимость.[^google-supply-chain]

Тебе нужно уметь отвечать:

- откуда взялась эта модель;
- какой набор prompt-правил сейчас активен;
- какая конфигурация политик была во время инцидента;
- какой корпус для извлечения использовался;
- какой набор для оценки подтвердил выпуск;
- какой verifier contract, grading rubric и rules для evidence linkage были активны;
- какая contract version и approval schema были активны;
- какая interruption или expiry policy управляла этим run;
- какой orchestration pattern и какая worker-boundary policy управляли этим run;
- какой delegated authorization mode, principal binding и revoke policy управляли этим run;
- кто одобрил это изменение.

Если на эти вопросы нельзя ответить быстро, управление изменениями и разбор инцидентов начинают ломаться почти сразу.

Именно поэтому provenance в этой главе стоит читать узко и предметно. Это не весь evidence layer целиком. Это governed lineage layer для trusted artifacts, release identity и decision-bearing versions.

В этом и состоит главный смысл этой главы. Она должна показать, где evidence перестает быть просто общей телеметрией и превращается в управляемый опорный слой: место, которое сохраняет, на какой именно reviewed artifact set, trusted contract version и approved release identity потом опирается разбор инцидента или управленческое решение.

!!! info "Нужны артефакты цепочки поставки?"
    Для формального описания смотри [схему lifecycle-артефактов](../../appendix/lifecycle-artifact-schema.md), [схему набора политик и контракта подтверждения](../../appendix/policy-bundle-schema.md) и [схему change review и rollout gate](../../appendix/change-rollout-schema.md).

## 4. У агента должно быть несколько цепочек доверия, а не одна

В обычной системе команда часто мыслит одной цепочкой доверия: «Код собран в CI, контейнер подписан, значит все хорошо».

В агентных системах лучше мыслить несколькими связанными цепочками:

- цепочкой кода и сборки;
- цепочкой моделей;
- цепочкой prompt- и routine-правил;
- цепочкой политик;
- цепочкой возможностей;
- цепочкой approval и runtime-control;
- цепочкой governance для capability sessions;
- цепочкой delegated authorization;
- цепочкой данных и извлечения;
- цепочкой оценки.

<div class="diagram-card">
<p>Полезно думать не об одной цепочке поставки, а о наборе связанных цепочек доверия</p>

``` mermaid
flowchart LR
    A["Code and build"] --> G["Approved release bundle"]
    B["Model artifacts"] --> G
    C["Prompt and routine bundles"] --> G
    D["Policy bundles"] --> G
    E["Capability contracts"] --> G
    F["Approval and runtime-control schemas"] --> G
    H["Eval datasets and reports"] --> G
```

</div>

## 5. Утвержденный реестр и доверенные артефакты не одно и то же

Это близкие, но разные понятия.

`approved inventory` отвечает на вопрос:

- какие рантаймы, шлюзы, возможности и шаблоны вообще разрешены на платформе.

`approved artifacts` отвечает на вопрос:

- какие конкретные версии и наборы разрешены к запуску прямо сейчас.

Например:

- возможность `create_ticket` может быть частью утвержденного реестра;
- но конкретный `policy_bundle_v12` или `prompt_bundle_support_v7` — это уже доверенный артефакт.

Это различие полезно, потому что реестр дает рамку уровня платформы, а доверенные артефакты дают дисциплину уровня конкретного выпуска.

Именно эта дисциплина уровня релиза и составляет здесь сердцевину provenance. Вопрос не только в том, есть ли телеметрия, а в том, под какой governed version, approved bundle или reviewed schema система реально работала.

## 6. Набор prompt-правил без происхождения — это такой же пробел, как неподписанная сборка

Очень частая ошибка команд: относиться к изменениям prompt как к живому тексту, а не как к артефакту выпуска.

Но если ты не знаешь:

- кто менял prompt;
- какая версия сейчас в проде;
- какие оценки ее покрыли;
- на какой волне раскатки она активна;

то такой набор правил по сути ничем не лучше артефакта, происхождение которого неизвестно.

То же самое относится к:

- routines;
- policy YAML;
- конфигурациям извлечения;
- порогам подтверждения;
- runtime-control schemas, которые определяют paused/background behavior.

## 7. Наборы для оценки тоже должны быть доверенными артефактами

Очень легко считать набор для оценки чем-то второстепенным: «Ну это просто набор тестовых примеров».

На самом деле это критичный артефакт управления.

Если он:

- собран непонятно откуда;
- не версионируется;
- не имеет владельца;
- тихо меняется между релизами;

то команда начинает принимать решения о выпуске на шатком основании.

Поэтому хороший ADLC должен относиться к наборам для оценки как к части модели доверенных артефактов.

То же все больше верно и для verifier contracts. Если release или assurance зависят от process scores, outcome scores, failure attribution или linked evidence, verifier layer уже нельзя считать неформальной вспомогательной логикой. Это полноценный governed production artifact.

## 8. Контракты возможностей и правила сетевого выхода тоже входят в цепочку поставки

В агентных системах контракт инструмента — это не просто документация, а часть доверенной рабочей поверхности.

У возможности должно быть понятно:

- кто владелец;
- какой уровень риска;
- какой инструментальный принципал;
- какой профиль сетевого доступа;
- какие направления выхода разрешены;
- как устроена семантика подтверждения.

Если контракт меняется тихо, без происхождения и без следа проверки, то такое изменение может быть не менее опасно, чем непроверенный деплой кода.

То же самое верно и для approval и runtime-control schemas. Если команда меняет timeout, pause/resume behavior, expiry semantics, правила re-initialization или ожидаемую форму payloads без governed artifact discipline, она меняет production behavior, даже если ни модель, ни исходный код не сдвинулись.

Это означает, что provenance все чаще должна хранить не только сам факт существования runtime-control schema, но и то, какая версия interruption-governance реально была активна:

- paused runs истекали или могли ждать бесконечно;
- capability-session re-init была allowed, denied или approval-bound;
- telemetry обязана была связывать исходную и reinitialized capability sessions или нет;
- какой orchestration pattern был утвержден для этого path и действовали ли worker-safe catalog boundaries;
- approval и session-control logic еще управлялись одним contract version или уже начали расходиться;
- delegated access была platform-owned или user-delegated;
- какое principal-binding rule и revoke behavior управляли in-flight или paused actions.

Это вопросы provenance именно потому, что они определяют governed identity поведения, а не просто факт того, что поведение было видно в telemetry.

## 9. Пример политики доверенных артефактов

Ниже очень рабочий skeleton:

```yaml
artifacts:
  require_owner: true
  require_version: true
  require_provenance: true
  require_review_status: true
  types:
    - model_route
    - prompt_bundle
    - policy_bundle
    - capability_contract
    - approval_schema
    - runtime_control_schema
    - capability_session_contract
    - verifier_contract
    - eval_dataset
    - retrieval_source
```

Такой список убирает разговор в стиле «Ну вроде нормальная конфигурация» и заставляет относиться к артефактам как к полноценным рабочим объектам.

## 10. Пример политики утвержденного реестра

А вот более платформенный пример:

```yaml
inventory:
  approved_runtimes:
    - agent_runtime_v3
  approved_gateways:
    - shared_tool_gateway
    - approval_gateway
  approved_patterns:
    - staged_rollout
    - approval_required_for_high_risk
    - governed_background_mode
    - reviewed_routing
    - bounded_parallelization
    - worker_safe_orchestrator_workers
  deprecated_patterns:
    - direct_prod_tool_access
    - unversioned_prompt_override
```

Такой реестр полезен не внешним видом, а тем, что дает платформе явную карту доверенных и недоверенных рабочих шаблонов.

## 11. Пример проверки готовности артефакта

Ниже очень простой каркас:

```python
from dataclasses import dataclass


@dataclass
class ArtifactRecord:
    has_owner: bool
    has_version: bool
    has_provenance: bool
    review_passed: bool
    schema_linked: bool


def artifact_ready(record: ArtifactRecord) -> bool:
    return (
        record.has_owner
        and record.has_version
        and record.has_provenance
        and record.review_passed
        and record.schema_linked
    )
```

Идея здесь простая: доверенный артефакт полезно определять не по интуиции, а по четким признакам.

## 12. Что чаще всего ломается в дисциплине артефактов

Обычно проблемы выглядят так:

- наборы prompt-правил не версионируются;
- наборы для оценки тихо меняются;
- контракты возможностей редактируются без следа проверки;
- approval или runtime-control schemas меняются без version discipline;
- changes в governance orchestration pattern не имеют artifact lineage;
- никто не знает, какой именно артефакт был активен в момент инцидента;
- в evidence layer отсутствует contract-version linkage;
- устаревшие шаблоны живут в промышленной среде слишком долго;
- утвержденный реестр существует в wiki, но не в рабочих инструментах.

Если это происходит, платформа теряет управляемость не из-за одной большой ошибки, а из-за сотни маленьких неучтенных артефактов.

## 13. Быстрый тест зрелости для artifact governance

Команде не стоит думать, что у нее уже есть supply-chain discipline, только потому, что сборки подписаны, а несколько конфигураций лежат в version control.

Более сильная планка такая:

- prompt, policy, eval, capability, approval и runtime-control artifacts считаются полноценными production artifacts;
- provenance можно быстро восстановить и для incident review, и для rollout decisions;
- approved inventory и approved artifacts живут как разные control layers;
- deprecated patterns можно заблокировать до того, как они тихо закрепятся в production;
- доверие привязано к явным свойствам артефакта, а не передается социально.

Если большинство этих условий не выполняется, у команды уже может быть какая-то artifact hygiene, но реального artifact governance у нее пока нет.

## 14. Практический чеклист

Если хочешь быстро проверить свою дисциплину артефактов, пройди по вопросам:

- У всех рабочих артефактов есть владелец?
- У model, prompt, policy, approval-schema, runtime-control и eval-артефактов есть версии?
- Можно ли быстро восстановить происхождение и активные contract/schema versions для разбора инцидента?
- Есть ли утвержденный реестр платформы?
- Отличаете ли вы шаблон, разрешенный на уровне платформы, от артефакта, разрешенного к выпуску?
- Можно ли быстро заблокировать устаревший артефакт?

Если на несколько вопросов подряд ответ «нет», у тебя пока еще нет полноценного слоя управления артефактами.

## 15. Что читать дальше

После темы цепочки поставки и дисциплины артефактов остается последняя рабочая тема этой части: вывод из эксплуатации, замена и завершение жизненного цикла. Зрелая система должна уметь не только запускаться и исправляться, но и корректно уходить со сцены.

## 16. Полезные справочные страницы

- [Схема набора политик и контракта подтверждения](../../appendix/policy-bundle-schema.md)
- [Схема артефактов жизненного цикла](../../appendix/lifecycle-artifact-schema.md)
- [Справочный пакет](../../appendix/reference-package.md)

- [Глава 21. Assurance loop: red teaming, detection и response](chapter-21.md)
- [Глава 17. Слой политик и каталог возможностей](../part-vii/chapter-17.md)
- [Глава 18. Чеклист промышленного запуска](../part-vii/chapter-18.md)
- [Источники](../../appendix/sources.md)

[^google-supply-chain]: [Google Research, Securing the AI Software Supply Chain](https://research.google/pubs/securing-the-ai-software-supply-chain/)
