# Часть VIII. Жизненный цикл агентной системы

До этого момента книга объясняла, как собрать архитектуру, защитить ее, наблюдать за ней и безопасно выкатывать изменения. Но production discipline не заканчивается на go-live.

Когда agent system живет дольше одной демки, у команды появляются вопросы другого класса:

- какие изменения вообще считать значимыми для релиза;
- как реагировать на drift и findings;
- как удерживать lineage доверенных артефактов;
- как выводить систему из эксплуатации;
- как не потерять контроль над целым estate, а не только над одним агентом.

Эта часть отвечает именно на них. Она читает agent system уже не как архитектурную схему, а как управляемый жизненный цикл.

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

## В этой части

- [Глава 19. От SDLC к ADLC](chapter-19.md)
- [Глава 20. Change management для агентных систем](chapter-20.md)
- [Глава 21. Assurance loop: red teaming, detection и response](chapter-21.md)
- [Глава 22. Supply chain, provenance и approved artifacts](chapter-22.md)
- [Глава 23. Retirement, replacement и end-of-life discipline](chapter-23.md)
- [Глава 24. Agentic misalignment и insider-risk](chapter-24.md)
- [Глава 25. Behavioral evals, control evals и automated red teaming](chapter-25.md)
- [Глава 26. Наблюдаемость для ИИ-систем, покрытие реестра и телеметрия для обнаружения проблем](chapter-26.md)
- [Глава 27. Инвентаризация агентов, реестр и борьба с разрастанием](chapter-27.md)

## Что ты должен вынести

- более взрослую рамку для release gates и change reviews;
- различие между judgment, response, lineage, observability и accountability;
- понятную модель того, как агентную систему менять, ограничивать, расследовать и закрывать во времени.
