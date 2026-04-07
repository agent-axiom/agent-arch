# Схема policy bundle и approval contract

Эта страница связывает несколько уже написанных тем:

- [Глава 4. Инструментальный шлюз, подтверждения и журнал аудита](../book/part-ii/chapter-4.md)
- [Глава 17. Слой политик и каталог возможностей](../book/part-vii/chapter-17.md)
- [Глава 20. Change management для агентных систем](../book/part-viii/chapter-20.md)

И опирается на runnable package:

- [Опорный пакет](reference-package.md)

Если страницы про trace schema и eval schema отвечают на вопросы:

- как описывать фактическое поведение;
- как описывать ожидаемое поведение;

то эта страница отвечает на третий вопрос:

- как описывать управляющие правила, которые стоят между reasoning и side effect.

## Почему policy bundle полезно мыслить как artifact

Одна из самых частых ошибок в agent systems выглядит так:

- policy rules частично живут в prompt;
- частично в gateway code;
- частично в approval UI;
- частично в голове команды.

Пока система маленькая, это может работать. Но как только появляется change management, audit и staged rollout, такой policy layer становится слишком размытым.

Поэтому полезно собирать `policy bundle` как отдельный artifact.

## Что такое policy bundle

Под `policy bundle` здесь удобно понимать набор связанных правил, который выпускается как единое целое:

- runtime policy;
- tool policy;
- approval policy;
- memory write rules;
- escalation rules;
- egress rules.

Смысл не в том, что все должно лежать в одном YAML-файле. Смысл в том, что bundle должен быть:

- versioned;
- reviewable;
- traceable;
- releasable.

## Минимальная структура policy bundle

Минимально полезный bundle может выглядеть так:

```yaml
bundle:
  bundle_id: policy-support-triage-2026-04-07
  version: 2026.04.07
  owner_team: platform-safety
  applies_to:
    agent_ids: ["support-triage-ref"]
  artifacts:
    - policy.yaml
    - approvals.yaml
    - controls.yaml
```

Это еще не сами rules. Это envelope, который отвечает на вопрос:

“Что именно мы сейчас считаем policy artifact для этой agent system?”

## Почему approval contract нельзя прятать внутри policy prose

Очень часто approval logic описывается словами:

- “если риск высокий, нужно подтверждение”;
- “manager approves ticket creation”;
- “security signs off on dangerous actions”.

Этого недостаточно.

Approval contract полезно делать явным:

- кто может approve;
- какой action class требует approval;
- какие поля должны попасть в approval request;
- какие решения допустимы;
- что происходит после reject;
- что должно остаться в audit trail.

## Пример approval contract

Ниже рабочий skeleton:

```yaml
approval_contract:
  capability: create_ticket
  risk_tier: high
  required_reviewers:
    - manager
  request_fields:
    - trace_id
    - session_id
    - requested_by
    - reason
    - tool_arguments_redacted
  allowed_decisions:
    - approved
    - rejected
  on_reject: stop_run
```

Смысл тут простой: approval должен быть не “галочкой в UI”, а machine-readable operational contract.

## Как policy bundle связан с lifecycle

Из Part VIII здесь особенно важны две мысли:

- policy changes — это release-bearing changes;
- policy bundle должен участвовать в change management как полноценный artifact.

То есть для команды полезно отвечать не только на вопрос:

“какая политика у нас в принципе?”

Но и на вопрос:

“какая именно версия policy bundle была активна в момент этого rollout или incident?”

## Как policy bundle связан с traces

Связь очень практическая:

- trace показывает, какая policy decision реально сработала;
- policy bundle показывает, откуда эта decision взялась;
- approval contract показывает, как должен был выглядеть human gate.

Без этой тройки расследование быстро превращается в угадайку.

## Что уже умеет reference runtime

В `agent_runtime_ref` сейчас уже есть:

- [policy.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/policy.yaml)
- [approvals.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/approvals.yaml)
- [controls.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/controls.yaml)
- [change.yaml](/Users/if/PycharmProjects/agent-axiom/agent-arch/agent_runtime_ref/configs/change.yaml)

То есть package уже живет в модели, где policy и approvals не просто “побочные настройки”, а отдельные governed artifacts.

## Что production schema должна добавить

Как только система взрослеет, для policy bundle почти сразу полезно добавить:

- `bundle_version`
- `artifact_lineage`
- `change_id`
- `approval_contracts`
- `deprecated_rules`
- `redaction_policy`

Это превращает policy layer из набора файлов в нормальный release surface.

## Почему policy bundle и capability catalog нельзя разводить слишком далеко

Есть плохая крайность: policy bundle живет отдельно, capability catalog отдельно, approval rules отдельно, и между ними нет устойчивых ссылок.

Тогда быстро появляются проблемы:

- capability есть в каталоге, но про нее нет approval contract;
- policy знает capability name, которого уже нет;
- audit видит decision, но не может связать ее с bundle version.

Поэтому practical rule простой:

- capability catalog описывает, что система умеет;
- policy bundle описывает, как и при каких условиях это можно использовать;
- approval contract описывает, где reasoning обязан остановиться и уступить человеку.

## Практический чеклист

Если хочешь быстро понять, зрелый ли у тебя policy artifact layer, пройди по вопросам:

- Есть ли versioned policy bundle?
- Можно ли связать policy bundle с rollout и incident review?
- Approval contract machine-readable или только описан словами?
- Ясно ли, какие fields обязан содержать approval request?
- Есть ли связь между policy bundle и capability catalog?
- Можно ли понять, какая версия policy была активна в момент trace?

Если несколько ответов подряд “нет”, значит policy layer у тебя пока существует, но еще не оформлен как полноценный operational artifact.

## См. также

- [Схема трасс и каталог событий](trace-schema.md)
- [Схема eval datasets и grading contract](eval-schema.md)
- [Схема lifecycle-артефактов](lifecycle-artifact-schema.md)
- [Опорный пакет](reference-package.md)
- [Policy templates и checklists по кейсам](policy-templates.md)
