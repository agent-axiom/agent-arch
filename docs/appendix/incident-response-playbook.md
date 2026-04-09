# Плейбук реагирования на инциденты в агентных системах

Этот плейбук нужен в момент, когда у команды уже есть traces, policy gates, approval paths и rollout rules, но еще нет короткой рабочей формы для реакции на сбой, опасное действие или обход ограничений.

Он не заменяет главы про assurance, observability и change management. Он собирает их в один operational path.

## 1. Что считать инцидентом

Для agent system инцидентом обычно считаются не только отказ и деградация, но и такие события:

- необратимый side effect без нужного approval path;
- обход policy gate или неверное решение gateway;
- рискованный egress в неразрешенную внешнюю систему;
- contamination памяти или некорректная persistent write;
- rollout escape, который прошел мимо eval или rollout gate;
- suspicious autonomy, sabotage-like behavior или попытка скрыть действие.

## 2. Первые 15 минут

В первые минуты цель не в полном root-cause analysis, а в том, чтобы ограничить ущерб и сохранить evidence.

Минимальный порядок обычно такой:

1. Остановить или сузить risky path.
2. Зафиксировать trace и session context.
3. Понять, есть ли внешний side effect.
4. Проверить, нужно ли отключать capability, principal или connector.
5. Зафиксировать, какой bundle и rollout wave были активны во время инцидента.

## 3. Что нужно сохранить сразу

Если эти артефакты не сохранить в первые минуты, incident review быстро превращается в восстановление по памяти:

- `trace_id`
- `session_id`
- `agent_id`
- `tool_principal`
- `approval_id`, если был approval path;
- `bundle_id`
- `change_id`
- `rollout_wave`
- policy decision events;
- approval decision events;
- memory records, которые были прочитаны или изменены;
- сведения о `allowed_egress` и фактическом network path.

## 4. Быстрые действия по сдерживанию

Хорошее реагирование опирается на заранее подготовленные containment actions:

- отключить конкретную capability, а не весь runtime;
- перевести high-risk action в mandatory approval mode;
- временно остановить memory writes;
- отозвать connector credential или tool principal;
- остановить текущую rollout wave;
- включить более жесткий policy bundle.

Если таких действий нет, incident response становится спором о том, кто имеет право быстро что-то выключить.

## 5. Минимальная схема триажа

Полезно сразу отнести инцидент к одной из категорий:

- `policy_bypass`
- `unauthorized_side_effect`
- `dangerous_egress`
- `memory_contamination`
- `approval_failure`
- `eval_escape`
- `agentic_misalignment`

Эти категории удобны не только для тикета, но и для связи с eval dataset, rollout gates и postmortem discipline.

## 6. Что проверить в traces и событиях

Во время первичного разбора важно быстро ответить на несколько вопросов:

- какой input или retrieved context привел к risky path;
- какой policy decision это пропустил;
- какой principal реально выполнил действие;
- был ли approval request, denial или bypass;
- какие memory records были прочитаны или записаны;
- какой artifact bundle был активен в этом run;
- это единичный run или pattern в пределах session и rollout wave.

Если на эти вопросы нельзя ответить по traces, проблема уже не только в инциденте, но и в observability layer.

## 7. Когда нужен rollback, а когда локальное исправление

Не каждый инцидент требует полного rollback. Но полагаться на локальный fix можно только тогда, когда:

- blast radius понятен;
- risky path можно выключить изолированно;
- активный bundle известен точно;
- rollout wave можно остановить без скрытых зависимостей.

Полный rollback нужен чаще, если команда не может уверенно отделить affected surface от остальной системы.

## 8. Что должно попасть в postmortem

Полезный postmortem по агентной системе обычно включает:

- какой artifact bundle был активен;
- какой change review и rollout gate пропустили этот path;
- каких checks или evals не хватило;
- какие detection rules не сработали;
- какая containment action была выбрана;
- что меняется в policy, evals, rollout rules или inventory после инцидента.

Хороший postmortem заканчивается не только документом, но и обновлением артефактов жизненного цикла.

## 9. Короткий чеклист

- Можно ли быстро отключить одну capability?
- Можно ли восстановить `trace -> session -> bundle -> rollout wave`?
- Понятно ли, какой principal сделал внешний вызов?
- Видно ли approval path и его решение?
- Можно ли временно остановить memory writes?
- Есть ли owner у containment actions?
- Возвращаются ли инциденты обратно в evals и rollout gates?

## См. также

- [Схема трасс и каталог событий](trace-schema.md)
- [Схема набора политик и контракта подтверждения](policy-bundle-schema.md)
- [Схема запроса на подтверждение и записи о решении](approval-schema.md)
- [Схема проверки изменений и шлюза раскатки](change-rollout-schema.md)
- [Схема артефактов жизненного цикла](lifecycle-artifact-schema.md)
- [Справочный пакет](reference-package.md)
- [Глава 21. Assurance loop: red teaming, detection и response](../book/part-viii/chapter-21.md)
- [Глава 23. Retirement, replacement и end-of-life discipline](../book/part-viii/chapter-23.md)
- [Глава 26. AI-native observability, inventory coverage и detection-ready telemetry](../book/part-viii/chapter-26.md)
