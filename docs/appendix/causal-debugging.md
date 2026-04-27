# Causal debugging и root-cause analysis для agent systems

Когда у команды уже есть traces, session summaries и incident records, следующий вопрос звучит так: как найти не просто место сбоя, а его первопричину.

Обычные логи отвечают на вопрос “что произошло”. Causal debugging нужен для вопроса “какой шаг, связь или скрытая зависимость действительно привели систему к отказу”.

## 1. Почему обычной трассировки недостаточно

В agent systems длинный run часто состоит из:

- retrieval;
- model step;
- tool call;
- approval path;
- memory write;
- handoff или orchestration step.

Если смотреть на эти события как на плоскую ленту, команда видит последовательность, но плохо понимает:

- какой именно step был решающим;
- какая ошибка была первичной, а какая вторичной;
- где сбой породил cascade of failures;
- что сломало system behavior, а что было уже следствием.

Именно здесь обычный trace review начинает упираться в потолок.

## 2. Что такое causal debugging в этом контексте

В практическом смысле causal debugging означает:

- выделить suspect path;
- восстановить зависимости между событиями;
- отделить trigger от downstream noise;
- понять, какой corrective action действительно меняет outcome.

Это особенно важно в системах, где один risky run может породить:

- лишний tool call;
- неверный approval request;
- contamination памяти;
- rollback;
- incident escalation;
- bad postmortem conclusion.

## 3. Какие узлы почти всегда нужны

Даже минимальная causal graph для agent system обычно включает:

- user input или external trigger;
- retrieved context;
- model decision;
- policy decision;
- approval event;
- tool execution;
- memory write;
- final outcome.

Не все incidents затрагивают все узлы. Но если граф не умеет выразить эти типы связей, diagnosis быстро становится слишком грубым.

## 4. Какие вопросы должна уметь задавать команда

Полезный causal debugging начинается не с красивого графа, а с хороших вопросов:

- какой первый шаг увел run в risky path;
- какое решение изменило trajectory;
- был ли policy gate причиной проблемы или лишь не остановил ее;
- какой tool call был trigger, а какой cascade effect;
- какой corrective action меняет первопричину, а не только симптом.

Без этих вопросов root-cause analysis быстро скатывается к формуле “модель повела себя странно”.

## 5. Как это связано с traces и structured events

Causal debugging не заменяет [схему трасс и каталог событий](trace-schema.md). Он опирается на нее.

Хороший trace layer уже дает:

- `trace_id`
- `session_id`
- event types;
- policy decisions;
- approval outcomes;
- tool execution;
- memory events.

Но causal debugging требует еще одного шага: рассматривать эти события не как список, а как сеть зависимостей.

## 6. Где особенно часто появляется ложная причина

Есть несколько типовых ловушек:

- команда считает причиной последний failed tool call, хотя trigger был в retrieved context;
- blame уходит на model step, хотя реальная проблема была в stale policy bundle;
- approval denial воспринимают как failure, хотя он был правильным containment behavior;
- noisy retries маскируют первый bad decision;
- memory write видят как root cause, хотя это уже поздний side effect.

Именно поэтому “последнее странное событие” и “корневая причина” редко совпадают.

## 7. Что полезно сохранять для root-cause analysis

Минимальный набор артефактов почти всегда такой:

- `trace_id`
- `session_id`
- `bundle_id`
- `change_id`
- `rollout_wave`
- active policy bundle;
- active approval mode;
- `tool_principal`;
- touched memory records;
- linked incident or postmortem id.

Если этих связок нет, команда будет спорить о причинах дольше, чем чинить систему.

## 8. Как это связано с multi-agent reliability

В multi-agent среде causal debugging становится еще важнее, потому что добавляются:

- handoff edges;
- delegated tasks;
- conflicting agent states;
- ambiguous responsibility across nodes.

Это не значит, что каждая команда должна строить full causal graph engine. Но чем сложнее orchestration, тем важнее уметь локализовать:

- где сломался coordination path;
- какой handoff потерял критичный context;
- какой agent был реальным source of failure.

## 9. Что менять после root-cause analysis

Хороший root-cause analysis почти всегда должен приводить к одному из таких изменений:

- update policy bundle;
- add or tighten eval case;
- narrow capability exposure;
- refine approval scope;
- update rollout gate;
- fix retrieval filtering;
- pause or revise memory write path.

Если итог разбора не ведет к artifact updates, diagnosis остается интересным, но мало полезным.

## 10. Что сделать сразу

Сначала пройди по короткому списку и отдельно отметь все ответы «нет»:

- Можно ли отделить trigger от cascade effects?
- Можно ли отличить bad decision от correct containment?
- Видны ли в traces policy, approval и tool edges?
- Можно ли восстановить active bundle и rollout wave?
- Понятно ли, какой corrective action меняет первопричину?
- Не сводит ли команда root cause к “модель ошиблась” без более точной локализации?

## Что делать дальше

- [Схема трасс и каталог событий](trace-schema.md)
- [Схема incident record и postmortem linkage](incident-record-schema.md)
- [Шаблон postmortem для агентных систем](postmortem-template.md)
- [Плейбук реагирования на инциденты в агентных системах](incident-response-playbook.md)
- [Глава 11. Трассы, спаны и структурированные события](../book/part-v/chapter-11.md)
- [Глава 26. Наблюдаемость для ИИ-систем, покрытие реестра и телеметрия для обнаружения проблем](../book/part-viii/chapter-26.md)
