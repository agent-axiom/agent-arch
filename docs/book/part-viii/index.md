# Часть VIII. Жизненный цикл агентной системы

До этого момента книга объясняла, как собрать архитектуру, защитить ее, наблюдать за ней и безопасно выкатывать изменения. Но production discipline не заканчивается на go-live.

Когда agent system живет дольше одной демки, у команды появляются вопросы другого класса:

- какие изменения вообще считать значимыми для релиза;
- как реагировать на drift и findings;
- как удерживать lineage доверенных артефактов;
- как выводить систему из эксплуатации;
- как не потерять контроль над целым estate, а не только над одним агентом.

Эта часть отвечает именно на них. Она читает agent system уже не как архитектурную схему, а как управляемый жизненный цикл.

!!! example "Сквозной кейс в этой части"
    Support-triage кейс здесь проходит весь lifecycle arc: duplicate-ticket fix становится ADLC change set, high-risk change packet, managed assurance finding, approved artifact bundle, retirement control для старого ticket writer, misalignment/control-eval сценарий, detection-ready telemetry и registry record с owner. Так читатель видит, что один инцидент должен менять не только код, но и evidence, rollout, operations и accountability.

!!! info "Короткий маршрут по этой части"
    Если нужен быстрый проход, иди так:

    - [Глава 19](chapter-19.md): перейти от SDLC к ADLC как к рабочей рамке;
    - [Глава 20](chapter-20.md): понять, какие изменения считать значимыми для релиза;
    - [Глава 21](chapter-21.md): увидеть, как findings превращаются в response;
    - [Глава 22](chapter-22.md): зафиксировать lineage доверенных артефактов;
    - [Глава 23](chapter-23.md): закрыть lifecycle через replacement и retirement;
    - [Главы 24-27](chapter-24.md): расширить тот же контур на adversarial pressure, judgment, observability и accountability всего estate.

## Что решает эта часть

- показывает agent system как управляемый жизненный цикл, а не как одноразовый launch;
- отделяет release judgment от response, lineage, closure и estate accountability;
- дает язык для разговоров о change reviews, incidents, retirement и sprawl;
- помогает читать production agent estate как систему с ownership, а не как набор отдельных controls.

## Карта ролей этой части

Эта карта нужна, чтобы поздние главы не читались как один и тот же governance-тезис под разными названиями:

| Функция жизненного цикла | Главная работа | Главный артефакт | Чем она не является |
| --- | --- | --- | --- |
| Lifecycle frame | Удерживает переходы состояний от design до retirement | ADLC state model | Просто новым названием для SDLC |
| Change management | Решает, какие изменения требуют review и rollout gates | Change packet | Обычным project management |
| Assurance | Превращает findings в containment, remediation и ownership | Finding and response record | Observability или eval scoring |
| Provenance | Сохраняет lineage доверенных артефактов и release identity | Approved artifact bundle | Общей папкой с evidence |
| Retirement | Закрывает или заменяет системы без потери accountability | Retirement plan | Удалением старого агента |
| Misalignment и insider risk | Называет adversarial или incentive-driven misuse paths | Risk scenario and control plan | Повтором prompt-injection guidance |
| Behavioral/control evals | Дают release judgment о поведении и controls | Eval gate and verifier contract | Incident response |
| Observability | Делает evidence substrate видимым и проверяемым | Trace and telemetry coverage record | Владельцем governance decisions |
| Inventory и registry | Делают estate accountable через owners и lifecycle state | Registry record | Свободной таблицей агентов |

Читай главы как цепочку: lifecycle задает состояния, change management контролирует движение, evals выносят judgment о готовности, provenance фиксирует доверенные артефакты, observability сохраняет evidence, assurance реагирует, когда evidence превращается в risk, retirement закрывает старые пути, а registry удерживает accountability всего estate.

## В этой части

- [Глава 19. От SDLC к ADLC](chapter-19.md)
- [Глава 20. Change management для агентных систем](chapter-20.md)
- [Глава 21. Assurance loop: red teaming, detection и response](chapter-21.md)
- [Глава 22. Цепочка поставки, происхождение и доверенные артефакты](chapter-22.md)
- [Глава 23. Retirement, replacement и end-of-life discipline](chapter-23.md)
- [Глава 24. Agentic misalignment и insider-risk](chapter-24.md)
- [Глава 25. Behavioral evals, control evals и automated red teaming](chapter-25.md)
- [Глава 26. Наблюдаемость для ИИ-систем, покрытие реестра и телеметрия для обнаружения проблем](chapter-26.md)
- [Глава 27. Инвентаризация агентов, реестр и борьба с разрастанием](chapter-27.md)

## Что ты должен вынести

- более взрослую рамку для release gates и change reviews;
- различие между judgment, response, lineage, observability и accountability;
- понятную модель того, как агентную систему менять, ограничивать, расследовать и закрывать во времени.
