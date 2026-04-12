# Tool failure recovery patterns для agent systems

Ошибки tools редко заканчиваются простым `error`. Чаще команда сталкивается с более неприятными состояниями:

- side effect unknown;
- partial success;
- stale reconciliation;
- повторный вызов, который уже опаснее исходной ошибки.

Поэтому для agent systems полезно держать отдельный набор recovery patterns, а не сводить все к retry policy.

## 1. Почему tool failure recovery это отдельный слой

Когда execution path ломается, команда обычно хочет “просто повторить”. Но у tools разные последствия:

- read tool можно повторить безопаснее;
- write tool может создать дубль;
- connector может успеть выполнить действие, но не вернуть подтверждение;
- downstream system может оказаться в промежуточном состоянии.

Именно поэтому recovery logic должна быть частью contract layer.

## 2. Какие классы исходов полезно различать

Минимально полезная taxonomy выглядит так:

- `success`
- `retryable_failure`
- `validation_failure`
- `permission_failure`
- `side_effect_unknown`
- `partial_side_effect`
- `manual_reconciliation_required`

Если execution layer не различает эти классы, agent почти неизбежно начинает принимать слишком грубые recovery decisions.

## 3. Что делать с `side_effect_unknown`

Это самый неприятный класс отказов.

Вместо naïve retry обычно полезнее:

- проверить текущее состояние во внешней системе;
- найти объект по idempotency key;
- перевести capability во временный restricted mode;
- запросить human review;
- зафиксировать неопределенность в trace и incident record.

Главная цель: не умножать side effects, пока состояние не восстановлено.

## 4. Что делать с `partial_side_effect`

Здесь система уже изменила внешний мир, но не дошла до clean completion.

Полезные стратегии:

- compensating action, если она допустима;
- explicit reconciliation step;
- stop and surface partial completion;
- follow-up task instead of silent retry.

Важная мысль здесь простая: partial success не означает success, но и не означает, что все можно безопасно начать заново.

## 5. Когда recovery должен требовать человека

Human gate особенно полезен, если:

- side effect необратим;
- reconciliation сама по себе risky;
- external system не дает надежной проверки состояния;
- у команды нет уверенности, какая версия payload была применена;
- retry может усилить blast radius.

То есть human review нужен не только для initial action, но и для некоторых recovery paths.

## 6. Какие поля полезно хранить в tool contract

Recovery quality сильно зависит от того, что знает execution layer о tool contract.

Минимально полезны такие поля:

- `idempotent`
- `retry_on`
- `reconcile_on_unknown`
- `requires_manual_recovery`
- `compensating_action`
- `external_lookup_key`

Без этого recovery decisions часто становятся ad hoc.

## 7. Что проверять в traces

Во время recovery review полезно быстро увидеть:

- какой статус вернул tool;
- был ли retry;
- какой idempotency key использовался;
- делалась ли reconciliation lookup;
- какой payload реально пошел в write path;
- кто принял final recovery decision.

Если эти вещи не видны в traces, recovery incidents будут расследоваться слишком долго.

## 8. Как это связано с evals

Tool failure recovery полезно явно проверять в eval dataset:

- timeout after write;
- connector disconnect after commit;
- duplicate retry attempt;
- partial success requiring follow-up;
- manual approval for recovery path.

Это особенно важно потому, что многие тяжелые production incidents происходят не на happy path, а именно в recovery branch.

## 9. Что сделать сразу

Сначала пройди по короткому списку и отдельно отметь все ответы «нет»:

- Различает ли execution layer `retryable_failure` и `side_effect_unknown`?
- Есть ли explicit recovery path для partial success?
- Видно ли в traces, какой recovery decision был принят?
- Есть ли tools, где retry запрещен по умолчанию?
- Есть ли cases на recovery branch в eval dataset?
- Может ли dangerous recovery path требовать human review?

## Что делать дальше

- [Глава 10. Идемпотентность, повторы, лимиты запросов и границы отката](../book/part-iv/chapter-10.md)
- [Схема трасс и каталог событий](trace-schema.md)
- [Схема incident record и postmortem linkage](incident-record-schema.md)
- [Плейбук реагирования на инциденты в агентных системах](incident-response-playbook.md)
- [Шаблон postmortem для агентных систем](postmortem-template.md)
