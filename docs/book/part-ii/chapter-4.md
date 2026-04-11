# Глава 4. Инструментальный шлюз, подтверждения и журнал аудита

!!! info "Как читать эту главу"
    Здесь полезно держать в голове не общий security checklist, а один конкретный момент:

    - агент уже что-то понял;
    - агент уже хочет вызвать tool;
    - системе нужно решить, можно ли вообще превращать это решение во внешний side effect.

    Если этот переход не оформлен жестко, все предыдущие архитектурные слои начинают быстро терять смысл.

## 1. Где на самом деле происходят дорогие инциденты

Самые дорогие сбои в агентных системах обычно случаются не тогда, когда модель “не так подумала”, а тогда, когда система перешла к действию:

- что-то записала;
- что-то отправила;
- что-то изменила;
- куда-то выгрузила данные.

Именно поэтому execution boundary важнее, чем многим кажется.

В нашем сквозном support-кейсе это выглядит очень приземленно: агент уже проверил статус заявки и теперь собирается создать срочный тикет. До этого момента система еще могла ошибаться “внутри себя”. С этого момента она начинает менять внешний мир.

## 2. Инструментальный шлюз должен быть скучным и жестким

У хорошего tool gateway очень простая задача: не дать агенту превратить красивое рассуждение в неконтролируемый side effect.

Минимальные требования:

- принимать только разрешенные инструменты;
- валидировать аргументы;
- знать риск-класс операции;
- уметь останавливать вызов до side effect;
- отправлять опасные операции на human approval;
- журналировать и решение, и факт исполнения.

Ниже очень практичный шаблон policy для tool execution:

```yaml
tools:
  read_kb:
    risk: low
    approval: none
    allowed_roles: ["agent_runtime"]
  create_ticket:
    risk: medium
    approval: manager
    allowed_roles: ["agent_runtime"]
  prod_db_write:
    risk: critical
    approval: security_and_owner
    allowed_roles: []
    environments: ["staging"]
```

В этом YAML нет ничего “умного”, и именно это хорошо. Security perimeter любит обозримые правила.

### 2.1. Gateway должен знать не только tool, но и actor

Если gateway валидирует только имя инструмента и аргументы, этого мало. Ему еще нужно понимать, **кто именно пытается вызвать capability**.

Минимально полезная модель запроса к gateway обычно включает:

- `actor_id`;
- `actor_type`;
- `tenant_id`;
- `requested_capability`;
- `risk_class`;
- `approval_state`.

Тогда gateway может принимать решения не только по правилу “этот tool разрешен”, но и по правилу “этот tool разрешен именно этому actor-у и именно в этом контексте”.

Это и есть момент, где identity превращается в исполняемую границу доступа, а не остается просто записью в IAM-таблице.[^google-secure-agents][^google-ai-controls]

## 3. Human approval должен быть нормальным процессом

Есть действия, которые агент не должен завершать самостоятельно вообще:

- изменение production-данных;
- отправка сообщений во внешние каналы;
- операции с финансами;
- доступ к чувствительным документам;
- любые действия с высоким blast radius.

Для них нужен не просто toggle “approval required”, а нормальный сценарий подтверждения.

<div class="diagram-card">
<p>Как выглядит approval flow для опасного действия</p>

``` mermaid
sequenceDiagram
    autonumber
    participant R as Agent runtime
    participant P as Policy engine
    participant H as Human approver
    participant T as Tool gateway
    participant A as Audit trail

    R->>P: Request risky action
    P-->>R: Approval required
    R->>H: Ask for approval with context
    H-->>R: Approve / reject
    R->>T: Execute only if approved
    T->>A: Persist action + approval record
```

</div>

Хороший approval flow всегда хранит:

- кто запросил действие;
- какой был risk class;
- что именно собирались сделать;
- кто подтвердил;
- в какое время;
- был ли overridden policy gate.

## 4. На выходе тоже нужна защита

Многие команды старательно фильтруют входящие данные, но почти не думают о выходе. Это ошибка.

Утечка чаще всего происходит на egress:

- агент вставил лишний фрагмент документа в ответ;
- отправил чувствительный текст во внешний tool;
- положил приватные данные в лог;
- вернул пользователю результат из чужого tenant.

Минимальный egress checklist:

- redact PII where required;
- mask secrets and tokens;
- validate tenant ownership of retrieved content;
- restrict outbound destinations;
- log all sensitive outbound actions.

## 5. Журнал аудита должен быть пригоден для расследования

Просто “включить tracing” недостаточно. Для security тебе нужен trail, по которому можно восстановить историю события.

На один рискованный run полезно хранить:

- входной request id;
- principal и tenant;
- policy decision;
- prompt assembly metadata;
- tool call arguments в безопасно редактированном виде;
- approval records;
- итоговый egress event.

Если после инцидента команда видит только “модель вызвала tool X”, расследование уже наполовину проиграно.

### 5.1. Что именно должно связываться в audit trail

У хорошего audit trail есть не только события, но и связки между ними:

- какой principal начал run;
- какой policy decision открыл или закрыл действие;
- какой approver подтвердил исключение;
- какой tool principal реально пошел во внешний system;
- какой response или side effect получился на выходе.

Именно эта связность превращает логи в материал для расследования, а не в склад плохо связанных сообщений.

По сути, audit trail должен отвечать на четыре вопроса:

1. Кто инициировал действие?
2. Кто разрешил его исполнение?
3. Под какой identity оно реально ушло наружу?
4. Какой side effect или ответ это произвело?

Если на любой из этих вопросов нет ответа, у тебя, скорее всего, уже не audit trail, а просто наблюдаемость без достаточной accountability.[^google-ai-controls]

## 6. Security perimeter как набор привычек

Очень хочется найти одну волшебную библиотеку, которая “сделает безопасность”. Но на практике perimeter состоит из набора привычек:

- недоверенные данные явно маркируются;
- agent runtime не получает лишних прав;
- tools идут только через gateway;
- опасные действия требуют approval;
- все ключевые шаги попадают в audit trail;
- система умеет не только выполнять, но и отказывать.

Это и есть взрослая безопасность для агентной платформы.

## 7. Практический чеклист

Если хочешь быстро оценить свой текущий контур, пройди по этому списку:

- Есть ли у агента отдельная identity model?
- Разделены ли trusted instructions и untrusted content?
- Все ли tools проходят через gateway?
- Есть ли allowlist и arg validation?
- Есть ли approval flow для high-risk действий?
- Есть ли egress filtering?
- Достаточен ли audit trail для расследования?
- Видно ли в traces, какой policy gate сработал?
- Видно ли, какой principal реально исполнил внешний вызов?

Если на несколько пунктов подряд ответ “нет”, значит эту главу ты открыл очень вовремя.

## 8. Что читать дальше

- [Глава 3. Контур безопасности и границы доверия](chapter-3.md)
- [Глава 5. Зачем агенту память и почему она опасна](../part-iii/chapter-5.md)
- [Часть II. Контур безопасности](index.md)
- [Источники](../../appendix/sources.md)

[^google-secure-agents]: [Google Cloud, How Google secures AI Agents](https://cloud.google.com/blog/products/identity-security/cloud-ciso-perspectives-how-google-secures-ai-agents)
[^google-ai-controls]: [Google Cloud, Recommended AI Controls framework](https://cloud.google.com/blog/products/identity-security/audit-smarter-introducing-our-recommended-ai-controls-framework)
