# Сквозная цепочка доказательств: от запроса к решению о rollout

В production agent system tracing, policy, approvals, evals, incident review и rollout judgment нельзя воспринимать как просто соседние темы. Для оператора это одна эксплуатационная запись.

Если ты не можешь проследить один подозрительный run через все эти слои, значит у тебя пока нет evidence spine. У тебя есть разрозненные controls.

## Что ты должен уметь после этой страницы

- объяснить, почему трассы, policy, approvals, evals, incidents и rollout judgment образуют одну управляемую запись;
- назвать минимальный набор идентификаторов, который делает один подозрительный run проверяемым;
- показать, как runtime behavior, человеческое решение, lifecycle artifacts и release judgment связываются без догадок.

## Зачем нужна эта страница

Несколько глав книги уже описывают части этой цепочки:

- [Глава 11. Трассы, спаны и структурированные события](chapter-11.md)
- [Глава 13. Офлайн-оценки, онлайн-оценки и регрессионные шлюзы](chapter-13.md)
- [Глава 17. Слой политик и каталог возможностей](../part-vii/chapter-17.md)
- [Глава 20. Change Management для агентных систем](../part-viii/chapter-20.md)
- [Глава 21. Assurance loop: red teaming, detection и response](../part-viii/chapter-21.md)
- [Глава 22. Цепочка поставки, происхождение и доверенные артефакты](../part-viii/chapter-22.md)

Эта страница собирает их в один walkthrough, чтобы показать, как один управляемый run остается читаемым от user request до rollout judgment.

## Главный тезис

Evidence spine, это минимальная управляемая непрерывность, которая позволяет оператору без догадок ответить на все вопросы ниже:

- какой запрос запустил run;
- какой policy bundle и какая release identity были активны;
- какие tools вызывались;
- требовалось ли approval и было ли оно granted, denied или expired;
- какие trace events и structured signals были зафиксированы;
- как run был потом graded или evaluated;
- привел ли он к incident review;
- повлияло ли собранное evidence на rollout judgment.

Это должно оставаться верным и для degraded paths. Failed-run drill полезен только тогда, когда та же цепочка по-прежнему объясняет, какая release identity управляла этим сбоем, какой trace его сохранил, какая конкретная причина сбоя, например в поле `failure_reason`, осталась видимой, как он был graded и повлиял ли он на rollout judgment.

Без этой непрерывности у команды могут быть и traces, и approval logs, и eval reports, но все равно не будет одной reviewable operational record.

## Минимальная карта общих сущностей

Сильная evidence spine не требует одного гигантского schema-файла. Но она требует устойчивого набора идентификаторов и ссылок между слоями.

Как минимум один управляемый run должен оставаться читаемым через такие сущности, как:

- `run_id`, идентификатор выполнения в runtime;
- `trace_id`, идентификатор трассы или event lineage для этого run;
- `approval_id`, запись о человеческом шлюзе, если approval вообще участвует;
- `policy_bundle_version`, версия управляемой policy surface, активной для run;
- `artifact_id`, approved artifact или artifact bundle, связанный с release surface;
- `evaluation_result_id`, запись о grading или judgment, добавленная позже.

В более зрелых системах в эту цепочку обычно входят и:

- `release_identity`;
- `change_id`;
- `session_id`;
- `incident_id`;
- `verifier_contract_id` или lineage набора verifier contracts;
- `handoff_artifact_id`, если длинная работа пересекает границу context reset или role handoff.[^anthropic-harness]

Смысл не в идеальной терминологии. Смысл в том, чтобы связь оставалась проверяемой.

<div class="diagram-card">
<p>Полезно мыслить evidence spine как цепочку связанных записей, а не как набор разрозненных артефактов</p>

``` mermaid
flowchart LR
    A["run_id"] --> B["trace_id"]
    A --> C["policy_bundle_version"]
    A --> D["approval_id"]
    A --> E["evaluation_result_id"]
    C --> F["release_identity"]
    C --> G["artifact_id"]
    E --> H["verifier_contract_id"]
    E --> I["incident_id"]
    I --> J["rollout judgment"]
```

</div>

## Один сквозной walkthrough run

Возьмем support-triage agent, который умеет классифицировать входящее обращение, искать внутренние знания и создавать ticket только после approval в high-risk случаях.

### Шаг 1. User request входит в систему

Пользователь отправляет сообщение с просьбой открыть ticket по production-инциденту клиента.

Уже в этот момент система должна создать хотя бы:

- `run_id` для конкретного выполнения;
- `trace_id` для event lineage;
- ссылку на активные `policy_bundle_version` и `release_identity`.

Если потом команда не может доказать, какая именно управляемая release surface обработала запрос, цепочка уже ослаблена еще до первого tool call.

### Шаг 2. Policy evaluation определяет границы допустимого

Слой политик определяет:

- разрешена ли эта capability для данного tenant и actor;
- можно ли выполнять internal knowledge retrieval;
- требует ли создание ticket approval;
- допустима ли delegated authorization;
- нужен ли verifier contract для high-risk handling.

Именно поэтому [глава 17](../part-vii/chapter-17.md) находится внутри этой цепочки. Policy, это не просто статический слой настроек. Это часть evidence, которая объясняет, почему run вообще было разрешено или запрещено продолжать.

### Шаг 3. Tool calls и runtime events создают сырую историю

Runtime извлекает контекст, возможно классифицирует проблему и готовит предлагаемый payload для ticket.

Здесь [глава 11](chapter-11.md) становится видимой как слой сырого evidence. Run должен порождать structured events, по которым оператор потом увидит:

- какие inputs были приняты или отклонены;
- какие tool calls были сделаны;
- были ли retries;
- была ли pause в session;
- редактировался ли output;
- какая конкретная причина сбоя, например в поле `failure_reason`, сохранилась для degraded paths, показывалась ли она в operator-facing summary вроде `latest_failure_reason` в момент review и продолжал ли этот run учитываться как `traceable_failed_runs` на уровне session review;
- где именно система остановилась до side effects.

Без этого слоя дальнейшее judgment превращается не в реконструкцию, а в пересказ.

### Шаг 4. Approval создает запись о человеческом решении

Слой политик требует approval перед созданием ticket.

На этом шаге должна появиться или быть привязана запись `approval_id`, связанная с:

- `run_id`;
- `trace_id`;
- `policy_bundle_version`;
- `release_identity`;
- запрошенной capability и risk tier.

Если approval denied, это не просто исход взаимодействия. Это часть управляемой истории run.

Если approval expired, это тоже evidence. Оно не должно исчезать внутри состояния UI.

### Шаг 5. Evals и grading превращают историю в judgment

После этого run может попасть в offline review, online grading или regression comparison.

Здесь в цепочку входит [глава 13](chapter-13.md). Слой evals не должен плавать отдельно как disconnected score sheet. Он должен привязывать judgment к конкретному run, trace и управляемой release surface, которая породила это поведение.

Именно это позволяет команде различать:

- разовый сбой;
- регрессию policy;
- деградацию, привязанную к конкретному release;
- проблему доверия к verifier;
- сбой approval path.

### Шаг 6. Incident review превращает evidence в operational response

Если run выявил серьезную проблему, в игру вступает [глава 21](../part-viii/chapter-21.md).

Теперь команде нужна одна связанная запись, которая показывает:

- что произошло;
- какие controls сработали;
- каких controls не хватило;
- правильно ли вмешался approval;
- относится ли проблема к runtime, policy bundle, release artifact, verifier contract или operator workflow.

Если этих связей нет, incident review превращается в археологию по нескольким системам сразу.

### Шаг 7. Rollout judgment использует ту же цепочку

Наконец, [глава 20](../part-viii/chapter-20.md) использует это evidence, чтобы ответить на release-вопрос:

- rollout можно продолжать;
- rollout нужно остановить;
- нужен rollback;
- policy bundle требует пересмотра;
- набор artifacts нужно заменить;
- approval contract нужно ужесточить.

Это последняя причина, по которой evidence spine так важен. Rollout judgment не должен опираться только на интуицию или dashboards. Он должен опираться на цепочку, которая уже связывает runtime behavior, controls, approval, evidence и release identity.

## Один пример на уровне артефактов

Компактная управляемая запись для такого run может выглядеть так:

```yaml
run_id: run-support-042
trace_id: trace-support-042
session_id: session-support-007
policy_bundle_version: 2026.04.19
release_identity: release-support-triage-2026-04-19-canary
approval_id: approval-118
artifact_id: artifact-bundle-2026-04-19-a
change_id: change-2026-04-19-17
verifier_contract_id: verifier-contract-v3
evaluation_result_id: eval-result-042
incident_id: incident-2026-04-19-3
latest_rollout_decision: pause-canary
```

Смысл этого примера не в точном наборе полей. Смысл в том, что один подозрительный run должен оставлять после себя достаточно связей, чтобы команда могла перейти от runtime behavior к approval record, eval judgment, incident review и rollout action без ручной реконструкции всей цепочки.

## Что оператор должен уметь восстановить

Для одного подозрительного run оператор должен быстро ответить на все вопросы ниже:

- какой запрос его запустил;
- какая release identity его обработала;
- какая версия policy bundle им управляла;
- запрашивался ли approval и чем он закончился;
- какие trace events описывают путь run;
- какая eval или grading record вынесла judgment;
- повлиял ли run на incident или rollout decision.

Если хотя бы на часть этих вопросов приходится отвечать догадками, evidence spine еще не собран.

## Чего эта страница не заменяет

Эта страница не заменяет соседние главы:

- глава 11 по-прежнему отвечает за raw evidence capture;
- глава 13 по-прежнему отвечает за reviewable judgment;
- глава 17 по-прежнему отвечает за policy в управляемом runtime;
- глава 20 по-прежнему отвечает за release judgment;
- глава 21 по-прежнему отвечает за assurance response;
- глава 22 по-прежнему отвечает за provenance, artifact lineage и evidence backbone.

Эта страница только делает явной соединительную ткань между ними.

## Читать дальше

- [Глава 11. Трассы, спаны и структурированные события](chapter-11.md)
- [Глава 13. Офлайн-оценки, онлайн-оценки и регрессионные шлюзы](chapter-13.md)
- [Глава 17. Слой политик и каталог возможностей](../part-vii/chapter-17.md)
- [Глава 20. Change Management для агентных систем](../part-viii/chapter-20.md)
- [Глава 21. Assurance loop: red teaming, detection и response](../part-viii/chapter-21.md)
- [Глава 22. Цепочка поставки, происхождение и доверенные артефакты](../part-viii/chapter-22.md)

[^anthropic-harness]: Anthropic, [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps).
