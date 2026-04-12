# Практика. MCP для tools, A2A для agents

Очень многие команды слишком рано смешивают две разные задачи:

- как подключать инструменты и внешние системы;
- как организовывать взаимодействие между несколькими агентами.

Из-за этого `MCP` и `A2A` начинают восприниматься как взаимозаменяемые штуки. На деле это разные уровни архитектуры.

## 1. Короткое правило

Если совсем коротко:

- `MCP` нужен, когда агенту надо работать с tools, resources и adapters;
- `A2A` нужен, когда нескольким агентам надо обмениваться задачами, контекстом и результатами.

То есть один протокол отвечает в первую очередь за **agent-to-tool**, а другой за **agent-to-agent**.[^google-mcp-a2a][^google-multiagent]

## 2. Когда тебе почти точно нужен MCP

`MCP` полезен, если у тебя есть одна или несколько внешних capability, которые нужно подключать системно:

- поиск по документам;
- CRM;
- helpdesk;
- внутренние API;
- файловые ресурсы;
- базы знаний;
- песочница выполнения.

В такой ситуации главная задача не “построить общество агентов”, а:

- стандартизировать contract;
- отделить adapters от core runtime;
- упростить policy checks;
- централизовать logging, auth и isolation.

Именно здесь `MCP` ложится естественно.

## 3. Когда тебе действительно нужен A2A

`A2A` имеет смысл, когда у тебя уже есть не просто набор tools, а реально разные агенты с отдельной ответственностью:

- координатор;
- исследователь;
- аналитик;
- исполнитель;
- агент доменной области.

И они должны:

- передавать друг другу задачи;
- делегировать выполнение;
- обмениваться статусом;
- возвращать результат не как payload tool-а, а как результат работы другого agent-а.

То есть `A2A` появляется не там, где нужен “еще один adapter”, а там, где в системе уже есть отдельные agent boundaries.

## 4. Типовая ошибка: строить multi-agent слишком рано

На практике путаница обычно выглядит так:

1. У команды есть один runtime.
2. К нему надо подключить три системы.
3. Вместо capability contracts команда начинает проектировать multi-agent orchestration.

Это почти всегда лишняя сложность.

Если в системе пока нет реальных причин для разделения ответственности между агентами, то:

- tools лучше подключать через `MCP`;
- orchestration лучше держать внутри одного runtime;
- multi-agent coordination лучше не тащить раньше времени.

Хороший practical rule: **если сущность не принимает собственных решений и не несет собственной operational role, это, скорее всего, еще не агент, а capability**.

## 4.1. Research по multi-agent reliability пока скорее усиливает скепсис

Это место полезно дополнить одной важной мыслью. Свежие research papers по multi-agent reliability пока не дают сильного повода усложнять runtime заранее. Скорее наоборот: они показывают, как быстро растут coordination failures, verification gaps и ambiguity, когда система дробится без явной необходимости.

Поэтому practical reading здесь такая:

- research не говорит “строить больше агентов”;
- research говорит “если уже строишь multi-agent, то делай contracts, verification loops и diagnosable handoffs”;
- current best practice все еще остается `single-agent first`.

Именно поэтому `A2A` стоит вводить не потому, что это выглядит технологически красиво, а потому, что у тебя уже есть отдельные operational roles, которые нельзя честно описать как tools.

## 4.2. Согласие нескольких agents не равно независимой проверке

Даже если несколько agents пришли к похожему выводу, это еще не доказывает, что система получила независимый verification signal.

Проблемы здесь типовые:

- agents видят один и тот же contaminated context;
- reasoning paths слишком похожи;
- manager agent подталкивает downstream agents к ожидаемому ответу;
- consensus выглядит убедительно, но опирается на один и тот же bad assumption.

Поэтому multi-agent agreement полезно трактовать как signal, а не как доказательство correctness.

## 5. Decision table

| Вопрос | Скорее `MCP` | Скорее `A2A` |
| --- | --- | --- |
| Нужно подключить внешний API или resource? | Да | Нет |
| Нужен typed contract для tools? | Да | Нет |
| Есть отдельный агент со своей ролью и жизненным циклом? | Нет | Да |
| Нужно делегирование между агентами? | Нет | Да |
| Нужно изолировать adapter и policy path? | Да | Иногда |
| Нужно передать задачу другому agent runtime? | Нет | Да |

## 6. Как это выглядит в зрелой архитектуре

В зрелой платформе эти вещи обычно не конкурируют, а живут на разных слоях.

<div class="diagram-card">
<p>MCP и A2A дополняют друг друга, а не заменяют</p>

``` mermaid
flowchart LR
    A["Coordinator agent"] --> B["A2A handoff"]
    B --> C["Specialist agent"]
    A --> D["MCP client"]
    C --> E["MCP client"]
    D --> F["Tool / resource server"]
    E --> G["Tool / resource server"]
```

</div>

Нормальная логика такая:

- агент работает с tools через `MCP`;
- агент работает с другим агентом через `A2A`;
- policy и audit должны покрывать оба направления.

## 7. Когда `A2A` лучше не использовать

Есть несколько красных флагов:

- ты хочешь использовать второй агент просто как “обертку над API”;
- второй агент не имеет собственной policy surface;
- у него нет отдельной operational identity;
- его проще описать как capability contract;
- параллелизм и специализация не дают явной пользы.

Во всех этих случаях лучше остаться на `MCP` или даже на обычном gateway/adaptor layer.

## 8. Минимальный code sketch

Ниже очень короткий набросок, который показывает различие мышления:

```python
def call_tool_via_mcp(tool_name: str, payload: dict) -> dict:
    return {"kind": "tool_result", "tool": tool_name, "payload": payload}


def delegate_via_a2a(agent_name: str, task: dict) -> dict:
    return {"kind": "agent_result", "agent": agent_name, "task": task}
```

Смысл тут не в коде как таковом, а в типе взаимодействия:

- tool call возвращает результат capability;
- A2A handoff возвращает результат работы другого agent-а.

Это разные operational semantics, и их полезно не смешивать.

## 9. Что сделать сразу

Сначала пройди по короткому списку и отдельно отметь все ответы «нет»:

- Мне нужен новый agent или просто новый capability?
- У сущности есть собственная роль, policy surface и lifecycle?
- Это delegation problem или integration problem?
- Могу ли я объяснить, почему здесь недостаточно `MCP`?
- Не строю ли я multi-agent topology раньше, чем мне это реально нужно?

Если на эти вопросы трудно ответить, почти всегда безопаснее сначала выбрать `MCP`, а не `A2A`.

## 10. Что делать дальше

- [Часть IV. Инструменты и выполнение](index.md)
- [Глава 9. Песочница выполнения и MCP как интеграционный контракт](chapter-9.md)
- [Глава 10. Идемпотентность, повторы, лимиты запросов и границы отката](chapter-10.md)
- [Research frontier: память, наблюдаемость и надежность multi-agent систем](../../appendix/research-frontier.md)
- [Источники](../../appendix/sources.md)

[^google-mcp-a2a]: [Google Cloud, Building Connected Agents with MCP and A2A](https://cloud.google.com/blog/topics/developers-practitioners/building-connected-agents-with-mcp-and-a2a)
[^google-multiagent]: [Google Cloud Architecture Center, Multi-agent AI system in Google Cloud](https://docs.cloud.google.com/architecture/multiagent-ai-system)
