# Handbook по agent registry и inventory operations

Когда в организации появляется несколько agent systems, одного chapter про inventory уже мало. Нужен короткий operating model: кто ведет registry, как искать drift, когда agent считается orphaned и что делать с deprecated entries.

Этот handbook собирает такой минимум в одной странице.

## 1. Что должно существовать всегда

Даже у небольшой agent-программы должны существовать два слоя:

- `inventory` для полного списка agent-like сущностей;
- `registry` для тех, кто признан, классифицирован и допущен в production contour.

Если есть только registry, команда почти всегда недооценивает shadow agents и local experiments.
Если есть только inventory, но нет registry, никто не может уверенно сказать, что именно считается approved.

## 2. Кто должен владеть этим слоем

Registry редко работает, если ownership размыт.

Минимально полезное распределение обычно такое:

- platform team отвечает за саму форму registry и verification rules;
- product owner отвечает за business purpose и lifecycle state;
- safety или governance owner отвечает за policy и approval linkage;
- operations отвечает за incident contact и retirement hygiene.

Одна и та же команда может совмещать эти роли. Но сами роли должны быть видны явно.

## 3. Как должна выглядеть запись агента

Минимальный record полезно проверять по одному шаблону:

- `agent_id`
- owner team;
- business purpose;
- lifecycle state;
- risk tier;
- runtime identity;
- allowed capabilities;
- policy bundle;
- approval mode;
- observability coverage;
- bundle linkage;
- retirement linkage.

Без этого registry быстро превращается в список имен без operational смысла.

!!! note "Канонические сценарии реестра (Canonical registry cases)"
    Запись реестра (registry record) должна фиксировать разные якоря ответственности (accountability anchors) для трех канонических сценариев (canonical cases). **Триаж обращений поддержки (Support triage)** требует владельца (owner) для возможности записи (write capability), режима подтверждения (approval mode), средств идемпотентности (idempotency controls), пакета политик (policy bundle) и связи с выводом из эксплуатации (retirement linkage). **Внутренний ассистент знаний (Internal knowledge assistant)** требует владельца корпуса (corpus owner), политики поиска (retrieval policy), границ арендатора (tenant scope), проверки происхождения источников (source provenance review) и ритма проверки свежести (freshness review cadence). **Координация инцидентов (Incident coordination)** требует владельца инцидентной роли (incident role owner), полномочий эскалации (escalation authority), владельца канала уведомлений (notification channel ownership), владельца экстренного отката (emergency rollback owner) и состояния жизненного цикла (lifecycle state) для возможностей только на случай ЧС (emergency-only capabilities).

## 4. Когда agent должен попадать в inventory

Хороший сильный default выглядит так:

- если сущность может вызывать tools;
- если она читает organization context;
- если она действует от имени сотрудника или сервиса;
- если она участвует в production workflow;

она должна попадать хотя бы в inventory.

Отдельные исключения лучше оформлять явно, а не держать как молчаливое допущение.

## 5. Когда agent должен попадать в registry

В registry обычно должны попадать сущности, которые:

- идут в production contour;
- имеют доступ к sensitive tools или external systems;
- могут создавать side effects;
- участвуют в staged rollout;
- требуют audit-ready ownership.

Именно registry нужен для governance, approvals и reliable incident response.

## 6. Как часто проверять registry

Registry становится неточным не из-за плохой идеи, а из-за плохого operational rhythm.

Минимальный cadence обычно такой:

- при каждом rollout update;
- при каждом change review для high-risk changes;
- на регулярном inventory review;
- при каждом retirement или replacement event;
- после incident review, если вскрылись hidden agents или stale records.

Если registry не обновляется в этих точках, drift почти неизбежен.

## 7. Какие признаки drift важнее всего

Не весь drift одинаково опасен. В первую очередь стоит ловить:

- active agent без owner;
- agent в `production`, которого нет в traces или registry-linked telemetry;
- deprecated agent с живым principal;
- capability в runtime, которой нет в allowed inventory;
- approval mode в registry, который не совпадает с policy bundle;
- retired bundle, который все еще встречается в live runs.

Это и есть минимальный список для continuous verification.

## 8. Когда запись надо переводить в restricted, deprecated или retired

Полезно не тянуть с lifecycle state change:

- `restricted`, если есть временное сужение capability set или approval mode;
- `deprecated`, если replacement уже выбран и новые rollout waves должны идти мимо;
- `retired`, если principal revoked, rollout stopped и historical state переведен в retention mode.

Самая частая ошибка здесь простая: agent уже фактически выключен, но в registry все еще выглядит как production-ready.

## 9. Что проверять в incident response

Во время incident review registry нужен не ради каталога, а ради нескольких прямых ответов:

- какой agent вообще участвовал в событии;
- кто его owner;
- какой lifecycle state у него был;
- какой policy bundle и approval mode считались активными;
- какой bundle linkage и retirement status были у записи.

Если registry не отвечает на эти вопросы быстро, он слабо помогает operations.

## 10. Минимальный weekly review

Короткий review можно строить вокруг нескольких вопросов:

- Есть ли новые agent-like сущности вне inventory?
- Есть ли orphaned records?
- Есть ли `production` agents без coverage в telemetry?
- Есть ли deprecated entries с живыми principals?
- Есть ли несоответствия между registry, policy bundle и rollout state?

Такой review лучше делать коротким, но регулярным.

## 11. Что сделать сразу

Сначала пройди по короткому списку и отдельно отметь все ответы «нет»:

- У каждого active agent есть owner?
- Inventory и registry разделены?
- Lifecycle state обновляется при rollout и retirement?
- Registry связан с policy bundle и approval mode?
- Registry проверяется против live telemetry?
- Deprecated agents теряют principals и tool access?
- Incidents обновляют registry hygiene?

## Что делать дальше

- [Плейбук реагирования на инциденты в агентных системах](incident-response-playbook.md)
- [Схема артефактов жизненного цикла](lifecycle-artifact-schema.md)
- [Схема проверки изменений и шлюза раскатки](change-rollout-schema.md)
- [Эталонный пакет](reference-package.md)
- [Глава 26. Наблюдаемость для ИИ-систем, покрытие реестра и телеметрия для обнаружения проблем](../book/part-viii/chapter-26.md)
- [Глава 27. Инвентаризация агентов, реестр и борьба с разрастанием](../book/part-viii/chapter-27.md)
