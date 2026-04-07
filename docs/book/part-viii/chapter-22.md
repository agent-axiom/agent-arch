# Глава 22. Supply chain, provenance и approved artifacts

## 1. Почему у agent systems supply chain шире, чем у обычного сервиса

Когда инженеры слышат слова “software supply chain”, они обычно думают о знакомых вещах:

- пакетные зависимости;
- контейнеры;
- CI/CD artifacts;
- подписи и provenance для build outputs.

Для agent systems этого мало.

Проблема в том, что production behavior здесь зависит не только от кода. На него влияют еще:

- model artifacts;
- prompt и routine bundles;
- policy configs;
- retrieval corpora;
- capability contracts;
- eval datasets;
- approval rules;
- rollout bundles.

То есть supply chain у агента шире, потому что сама система шире.

## 2. Что такое approved artifact в агентной системе

Полезно заранее дать очень прямое определение:

approved artifact — это любой артефакт, который разрешено использовать в production, потому что у него есть owner, provenance, review status и понятная operational роль.

Это означает, что approved artifacts — это не только образы или wheel-файлы.

В agent platform к ним часто относятся:

- approved model route;
- approved prompt bundle;
- approved policy bundle;
- approved capability contract;
- approved retrieval source;
- approved eval set;
- approved rollout template.

Если у команды нет такой категории, она очень быстро начинает жить в неявной системе доверия: “кажется, это нормальный артефакт, потому что кто-то его уже использовал”.

## 3. Provenance нужен для ответа на очень практичные вопросы

Google Research очень правильно показывает, что provenance для AI systems полезен не только как formal security idea, а как operational necessity.[^google-supply-chain]

Тебе нужно уметь отвечать:

- откуда взялась эта модель;
- какой prompt bundle сейчас активен;
- какой policy config был во время инцидента;
- какой retrieval corpus использовался;
- какой eval set подтвердил release;
- кто одобрил этот change.

Если на эти вопросы нельзя ответить быстро, change management и incident review начинают ломаться почти сразу.

## 4. У агента должно быть несколько цепочек доверия, а не одна

В обычной системе команда часто мыслит одной цепочкой доверия: “код собран в CI, контейнер подписан, значит все хорошо”.

В agent systems лучше мыслить несколькими связанными цепочками:

- code and build chain;
- model chain;
- prompt and routine chain;
- policy chain;
- capability chain;
- data and retrieval chain;
- eval chain.

<div class="diagram-card">
<p>Полезно думать не об одной supply chain, а о наборе связанных chains of trust</p>

``` mermaid
flowchart LR
    A["Code and build"] --> G["Approved release bundle"]
    B["Model artifacts"] --> G
    C["Prompt and routine bundles"] --> G
    D["Policy bundles"] --> G
    E["Capability contracts"] --> G
    F["Eval datasets and reports"] --> G
```

</div>

## 5. Approved inventory и approved artifacts не одно и то же

Это близкие, но разные понятия.

`approved inventory` отвечает на вопрос:

- какие runtimes, gateways, capabilities и patterns вообще разрешены на платформе.

`approved artifacts` отвечает на вопрос:

- какие конкретные версии и bundles разрешены к запуску прямо сейчас.

Например:

- capability `create_ticket` может быть частью approved inventory;
- но конкретный `policy_bundle_v12` или `prompt_bundle_support_v7` — это уже approved artifact.

Это различие полезно, потому что inventory дает platform-level рамку, а approved artifacts дают release-level дисциплину.

## 6. Prompt bundle без provenance — это такой же supply-chain пробел, как неподписанный build

Очень частая ошибка команд: относиться к prompt changes как к живому тексту, а не как к release artifact.

Но если ты не знаешь:

- кто менял prompt;
- какая версия сейчас в проде;
- какие evals ее покрыли;
- на какой волне rollout она активна;

то этот prompt bundle operationally ничем не лучше артефакта, происхождение которого неизвестно.

То же самое относится к:

- routines;
- policy YAML;
- retrieval configs;
- approval thresholds.

## 7. Eval datasets тоже должны быть trusted artifacts

Очень легко считать eval dataset чем-то второстепенным: “ну это просто набор тестовых примеров”.

На самом деле eval dataset — это критичный governance artifact.

Если он:

- собран непонятно откуда;
- не versioned;
- не имеет owner;
- quietly меняется между релизами;

то team начинает принимать release decisions на shaky foundation.

Поэтому хороший ADLC должен относиться к eval datasets как к части approved artifact model.

## 8. Capability contracts и egress rules тоже входят в supply chain

В agent systems контракт инструмента — это не просто документация, а часть доверенной операционной поверхности.

У capability должно быть понятно:

- кто owner;
- какой risk tier;
- какой tool principal;
- какой network access profile;
- какие allowed egress destinations;
- какая approval semantics.

Если контракт меняется тихо, без provenance и без review trail, то такой change может быть не менее опасен, чем непроверенный code deploy.

## 9. Пример approved artifact policy

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
    - eval_dataset
    - retrieval_source
```

Это помогает перевести разговор из “ну вроде нормальная конфигурация” в режим “это полноценный production artifact”.

## 10. Пример approved inventory policy

А вот более platform-level пример:

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
  deprecated_patterns:
    - direct_prod_tool_access
    - unversioned_prompt_override
```

Такой inventory полезен не потому, что он “красиво выглядит”, а потому что дает платформе явную карту доверенных и недоверенных operational patterns.

## 11. Пример проверки artifact readiness

Ниже очень простой каркас:

```python
from dataclasses import dataclass


@dataclass
class ArtifactRecord:
    has_owner: bool
    has_version: bool
    has_provenance: bool
    review_passed: bool


def artifact_ready(record: ArtifactRecord) -> bool:
    return (
        record.has_owner
        and record.has_version
        and record.has_provenance
        and record.review_passed
    )
```

Идея здесь простая: trusted artifact полезно определять не по интуиции, а по четким признакам.

## 12. Что чаще всего ломается в artifact discipline

Обычно проблемы выглядят так:

- prompt bundles не versioned;
- eval datasets quietly меняются;
- capability contracts редактируются без review trail;
- никто не знает, какой exact artifact был активен в момент инцидента;
- deprecated patterns живут в production слишком долго;
- approved inventory существует в wiki, но не в operational tooling.

Если это происходит, платформа теряет управляемость не из-за одной большой ошибки, а из-за сотни маленьких неучтенных артефактов.

## 13. Практический чеклист

Если хочешь быстро проверить свою artifact discipline, пройди по вопросам:

- У всех production artifacts есть owner?
- У model, prompt, policy и eval artifacts есть версии?
- Можно ли быстро восстановить provenance для incident review?
- Есть ли approved inventory платформы?
- Отличаете ли вы platform-approved pattern от release-approved artifact?
- Можно ли быстро заблокировать deprecated artifact?

Если на несколько вопросов подряд ответ “нет”, у тебя пока еще нет полноценной artifact governance layer.

## 14. Что читать дальше

После supply chain и artifact discipline логично переходить к последней operational теме этой части: retirement, replacement и end-of-life discipline. Потому что зрелая система должна уметь не только запускаться и исправляться, но и корректно уходить со сцены.

## 15. Полезные справочные страницы

- [Схема policy bundle и approval contract](../../appendix/policy-bundle-schema.md)
- [Схема lifecycle-артефактов](../../appendix/lifecycle-artifact-schema.md)
- [Опорный пакет](../../appendix/reference-package.md)

- [Глава 21. Assurance loop: red teaming, detection и response](chapter-21.md)
- [Глава 17. Слой политик и каталог возможностей](../part-vii/chapter-17.md)
- [Глава 18. Чеклист промышленного запуска](../part-vii/chapter-18.md)
- [Источники](../../appendix/sources.md)

[^google-supply-chain]: [Google Research, Securing the AI Software Supply Chain](https://research.google/pubs/securing-the-ai-software-supply-chain/)
