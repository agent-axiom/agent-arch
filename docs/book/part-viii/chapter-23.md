# Глава 23. Retirement, replacement и end-of-life discipline

## 1. Почему зрелая агентная система должна уметь не только запускаться, но и уходить

Очень многие команды мыслят жизненный цикл примерно так:

- придумать систему;
- построить ее;
- защитить ее;
- наблюдать за ней;
- безопасно выкатывать изменения.

Но у любой production system есть еще один обязательный этап: она когда-то должна быть заменена, выключена или выведена из эксплуатации.

Для agent systems это особенно важно, потому что они обычно оставляют за собой длинный рабочий хвост:

- memory state;
- tool access;
- approvals and audit trails;
- состояние paused runs и background runs;
- состояние capability sessions и interruption lineage;
- lineage для orchestration patterns и worker-boundary decisions;
- delegated authorization lineage и revoke state;
- external integrations;
- user expectations;
- dependent workflows.

То есть retirement здесь — это не “удалили сервис и забыли”. Это управляемый рабочий процесс.

## 2. Когда вообще пора думать о retirement

Полезно перестать воспринимать retirement как нечто далекое и неприятное.

На практике trigger'ами часто становятся:

- runtime or model устарел;
- capability contract больше не считается безопасным;
- maintenance cost стал слишком высоким;
- quality ceiling reached, дальше нужен replacement;
- новый platform path вытесняет старый;
- regulatory or governance requirements изменились;
- продуктовая задача больше не существует.

Если у команды нет явных retirement triggers, старые agent systems почти всегда живут дольше, чем безопасно и полезно.

## 3. Retirement и replacement — это не одно и то же

Полезно разделять два сценария:

- `retirement`: система или capability просто выводится из эксплуатации;
- `replacement`: старая система снимается, но перед этим или параллельно ее заменяет новая.

Это важное различие.

В retirement главный вопрос: как безопасно убрать систему.

В replacement главный вопрос: как провести controlled transition, не потеряв качество, контроль и историю.

## 4. Главная опасность — тихо оставить за системой право действовать

Одна из самых неприятных рабочих ошибок устроена так:

- команда считает систему “почти выключенной”;
- но у нее все еще есть:
  - active tool principal;
  - живой connector;
  - доступ к memory;
  - старый путь rollout;
  - background job;
  - resumable paused approval path;
  - expired capability session, которую все еще можно re-initialize через старый path;
  - старая runtime-control schema, которую gateways все еще принимают.

То есть формально система уже “мертвая”, а по факту она все еще может делать действия.

Для agent systems это особенно опасно, потому что автономные и полуавтономные пути исполнения очень легко забыть.

## 5. Retirement должен идти по слоям

Хороший end-of-life process редко сводится к одному действию. Обычно его стоит раскладывать по слоям:

- остановить новые rollout waves;
- запретить risky capabilities;
- перевести write actions в approval-only или disable;
- остановить memory writes;
- истечь или отменить paused runs;
- отключить background jobs и background routes;
- закрыть или архивировать capability-session state и запретить uncontrolled re-init;
- выключить deprecated orchestration patterns и отозвать worker-safe catalog exposure;
- отозвать delegated authorization paths и архивировать их final lineage;
- отозвать egress access;
- закрыть principals, secrets и connectors;
- зафиксировать final audit state.

<div class="diagram-card">
<p>Retirement лучше делать как последовательное сужение рабочей поверхности системы</p>

``` mermaid
flowchart LR
    A["Freeze rollout"] --> B["Disable risky capabilities"]
    B --> C["Disable writes and background jobs"]
    C --> D["Revoke egress and principals"]
    D --> E["Archive audit and memory state"]
    E --> F["Mark system retired"]
```

</div>

## 6. Memory и audit data требуют отдельной дисциплины

Когда система уходит, сразу появляется неудобный вопрос: что делать с накопленным state?

Обычно здесь нужно отдельно решить:

- что архивировать;
- что удалить;
- что anonymize;
- как долго хранить traces и approvals;
- кто остается owner у archived state;
- можно ли использовать старые datasets и memory artifacts в replacement;
- нужно ли сохранять delegated authorization records, чтобы объяснять, под чьей identity исполнялись старые действия.

То есть retirement затрагивает не только running system, но и накопленный рабочий след системы.

## 7. Replacement должен быть staged, а не бинарным переключением

Когда старую систему заменяет новая, соблазн велик: “сделаем cutover и поедем дальше”.

Для agent systems это рискованный путь.

Полезнее staged replacement:

- shadow comparison;
- limited tenant migration;
- dual-run for critical scenarios;
- side-by-side evals;
- staged traffic shift;
- final cutover only after confidence is high.

Именно здесь replacement сближается с rollout discipline, но добавляет еще один вопрос: как не потерять continuity между старой и новой системой.

## 8. Старые capabilities и patterns нужно уметь официально депрекейтить

Полезно иметь не только `approved inventory`, но и `deprecated inventory`.

Например:

- deprecated runtime;
- deprecated prompt bundle family;
- deprecated gateway pattern;
- deprecated memory strategy;
- deprecated capability contract;
- deprecated approval schema;
- deprecated runtime-control schema;
- deprecated orchestration pattern или worker-boundary policy;
- deprecated capability-session contract.

Это важно, потому что retirement почти всегда начинается не с выключения, а с ясного сигнала:

“это больше не считается нормальным путем”.

## 9. User-facing transition тоже часть жизненного цикла

Если agent system влияет на пользовательский или внутренний workflow, end-of-life нельзя делать только внутри platform layer.

Полезно отдельно продумать:

- кого нужно предупредить;
- какие flows изменятся;
- какие expectations надо переустановить;
- какие fallback paths появятся;
- как временно поддерживать старые интеграции.

Это особенно важно для internal agent systems, которые быстро встраиваются в реальные привычки команд.

## 10. Пример retirement policy

Ниже очень рабочий skeleton:

```yaml
retirement:
  triggers:
    - deprecated_runtime
    - unsafe_capability_pattern
    - maintenance_cost_exceeded
    - replacement_ready
  required_steps:
    - freeze_rollout
    - disable_risky_capabilities
    - stop_memory_write
    - expire_paused_runs
    - stop_background_routes
    - freeze_reinitialization
    - disable_deprecated_patterns
    - revoke_worker_capability_exposure
    - revoke_egress
    - archive_audit_state
    - set_retired_status
```

Это полезно не потому, что YAML “решает проблему”, а потому что retirement превращается в явный operational contract.

## 11. Пример replacement readiness check

Ниже каркас, который показывает правильный тип проверки:

```python
from dataclasses import dataclass


@dataclass
class ReplacementState:
    shadow_eval_passed: bool
    migration_plan_ready: bool
    risky_capabilities_disabled: bool
    archive_plan_ready: bool
    paused_runs_drained: bool
    capability_sessions_resolved: bool


def ready_for_replacement(state: ReplacementState) -> bool:
    return (
        state.shadow_eval_passed
        and state.migration_plan_ready
        and state.risky_capabilities_disabled
        and state.archive_plan_ready
        and state.paused_runs_drained
        and state.capability_sessions_resolved
    )
```

Смысл здесь в том, что replacement тоже должен иметь gate, а не быть “переключением по настроению”.

## 12. Что чаще всего ломается в end-of-life discipline

Проблемы здесь довольно повторяемые:

- система считается retired, но principals еще живы;
- background jobs забыли выключить;
- memory write path остался активным;
- paused approvals остались resumable после retirement;
- expired capability sessions все еще можно re-initialize через stale control paths;
- deprecated orchestration patterns или worker-boundary policies остаются рабочими после retirement;
- background routes забыли выключить;
- archived state никому не принадлежит;
- deprecated schemas все еще принимаются gateways или runtime;
- deprecated patterns остаются рабочими слишком долго;
- replacement делается без dual-run или staged migration.

Именно такие мелочи превращают “почти завершенный” жизненный цикл в источник новых инцидентов.

## 13. Быстрый тест зрелости для end-of-life discipline

Команде не стоит думать, что она умеет делать retirement, только потому, что умеет отвести трафик в сторону и пометить систему как deprecated.

Более сильная планка такая:

- система теряет право действовать до того, как ее объявляют retired;
- principals, connectors, memory writes, paused runs, capability sessions, orchestration patterns и background jobs сужаются осознанно, а не по остаточному принципу;
- replacement идет staged, а не как бинарный cutover;
- deprecated approval и runtime-control schemas выключаются, а не висят как скрытые compatibility paths;
- у archived state есть owner и решение по retention;
- deprecated patterns превращаются в заблокированные paths, а не только в warnings.

Если большинство этих условий не выполняется, у команды уже может быть shutdown mechanics, но реального end-of-life discipline у нее пока нет.

## 14. Практический чеклист

Если хочешь быстро проверить свою end-of-life discipline, пройди по вопросам:

- У системы есть явные retirement triggers?
- Можно ли выключать capabilities поэтапно, а не только все сразу?
- Ясно ли, что делать с memory, traces, approvals, состоянием paused runs и capability-session state после shutdown?
- Есть ли staged plan для replacement?
- Можно ли быстро отозвать principals, connectors, egress access, paused approvals, capability-session re-init и background routes?
- Понятно ли, кто owner у archived artifacts и historical state?

Если на несколько вопросов подряд ответ “нет”, значит жизненный цикл у тебя пока все еще заканчивается на релизе, а не на реальной эксплуатации.

## 15. Что читать дальше

Эта глава замыкает Part VIII в цельный operational цикл:

- SDLC -> ADLC;
- change management;
- assurance loop;
- artifact governance;
- retirement and replacement.

Эта часть работает не только как архитектурное объяснение, но и как handbook по жизненному циклу production-grade agent systems.

## 16. Полезные справочные страницы

- [Схема артефактов жизненного цикла](../../appendix/lifecycle-artifact-schema.md)
- [Схема набора политик и контракта подтверждения](../../appendix/policy-bundle-schema.md)
- [Справочный пакет](../../appendix/reference-package.md)

- [Глава 19. От SDLC к ADLC](chapter-19.md)
- [Глава 22. Supply chain, provenance и approved artifacts](chapter-22.md)
- [Глава 24. Agentic misalignment и insider-risk](chapter-24.md)
- [Глава 27. Agent inventory, registry и борьба с sprawl](chapter-27.md)
- [Часть VIII. Жизненный цикл агентной системы](index.md)
- [Источники](../../appendix/sources.md)
