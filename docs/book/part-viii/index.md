# Часть VIII. Жизненный цикл агентной системы

До этого момента книга объясняла, как собрать архитектуру, защитить ее, наблюдать за ней и безопасно выкатывать изменения. Но производственная дисциплина не заканчивается на чеклисте выкладки.

В нашем сквозном support-кейсе к этому моменту уже есть рабочий runtime, policy layer, capability catalog и ограниченный rollout. Теперь вопрос меняется: как жить с этой системой месяцами, как менять ее без потери контроля и как вовремя останавливать, заменять или выводить из эксплуатации.

Если система живет дольше одной демки, у тебя почти сразу появляются вопросы другого класса:

- как принимать агентные инициативы в работу;
- как проводить design review;
- какие изменения считать risk-bearing;
- как выпускать model, prompt, policy и tool changes;
- как расследовать инциденты и когда выводить систему из эксплуатации.

Именно здесь обычная инженерная дисциплина встречается с агентной спецификой. Поэтому эта часть начинается с перехода от классического SDLC к ADLC, а не с попытки изобрести для агентов отдельный “магический процесс”.

!!! info "Короткий маршрут по этой части"
    Если тебе нужен быстрый проход, иди так:

    - [Глава 19](chapter-19.md): выровнять рамку через переход от SDLC к ADLC;
    - [Глава 20](chapter-20.md): понять, какие agent changes вообще считаются release-bearing;
    - [Глава 21](chapter-21.md): собрать assurance как operational response loop для drift, findings и containment;
    - [Глава 22](chapter-22.md): закрепить provenance, approved artifacts и contract lineage как evidence backbone, которая сохраняет, что именно было одобрено, какая версия была активна и на какой governed artifact потом опиралось решение;
    - [Глава 23](chapter-23.md): закрыть lifecycle через replacement, retirement и shutdown runtime-control surfaces;
    - [Главы 24-27](chapter-24.md): расширить тот же контур на adversarial pressure, eval judgment, observability evidence и accountability всего agent estate.

    Если читать эту часть как единый аргумент, она напрямую продолжает систему, собранную в Part VII: Глава 19 задает рамку жизненного цикла, Глава 20 превращает release-bearing change в operational judgment, Глава 21 делает assurance response function, Глава 22 закрепляет evidence backbone, Глава 23 закрывает жизненный цикл, а Главы 24-27 продолжают тот же контур через adversarial pressure, judgment, evidence substrate и accountability всего estate.

## Что решает эта часть

Эта часть дает читателю последовательность обещаний:

- после первых глав ты должен видеть agent system как governed lifecycle, а не как одноразовый launch;
- после средних глав ты должен различать response, evidence backbone, lifecycle closure, adversarial pressure, judgment, observability substrate и accountability как разные operational roles;
- к концу части ты должен уметь читать production agent estate как один управляемый contour, а не как рыхлую кучу controls.

Более конкретно эта часть:

- переводит reference implementation в управляемый lifecycle;
- связывает change management, assurance response, evidence lineage, eval judgment, observability evidence, runtime-control governance, discipline для interruption/expiry/re-init, delegated authorization lineage и accountability всего agent estate в один operational contour;
- отделяет устойчивую инженерную дисциплину от быстро меняющихся vendor- и research-layer деталей.

Если читать эту часть как единый блок, порядок такой:

- сначала ты выравниваешь понятийную рамку через переход от SDLC к ADLC;
- потом понимаешь, какие изменения в агентной системе вообще считаются release-bearing;
- затем рассматриваешь assurance как operational response loop для drift, findings и control failure;
- после этого закрепляешь artifact discipline, provenance и contract/schema governance как evidence backbone, которая хранит identity релиза и lineage решений, а не detection telemetry или ownership всего estate;
- затем закрываешь жизненный цикл через replacement, retirement и shutdown runtime-control surfaces;
- и в конце расширяешь тот же контур на adversarial pressure, eval judgment, observability evidence и accountability всего agent estate.

## В этой части

- [Глава 19. От SDLC к ADLC](chapter-19.md)
- [Глава 20. Change management для агентных систем](chapter-20.md)
- [Глава 21. Assurance loop: red teaming, detection и response](chapter-21.md)
- [Глава 22. Supply chain, provenance и approved artifacts](chapter-22.md)
- [Глава 23. Retirement, replacement и end-of-life discipline](chapter-23.md)
- [Глава 24. Agentic misalignment и insider-risk](chapter-24.md)
- [Глава 25. Behavioral evals, control evals и automated red teaming](chapter-25.md)
- [Глава 26. AI-native observability, inventory coverage и detection-ready telemetry](chapter-26.md)
- [Глава 27. Agent inventory, registry и борьба с sprawl](chapter-27.md)

## Что ты получишь в конце части

- цельную модель жизненного цикла для production-grade agent systems;
- более взрослую рамку для change reviews и release gates;
- более ясное различие между assurance response, provenance/evidence backbone, eval judgment, observability evidence и accountability всего estate;
- практический язык для разговоров о replacement, retirement, end-of-life discipline и shutdown runtime-control surfaces;
- более зрелую рамку для sabotage-like behavior, control failures, contract drift и adversarial assurance;
- представление о observability как о слое доказательств, а не просто о generic telemetry bucket;
- рабочую рамку для управления всем контуром агентов, а не только отдельными agent systems;
- более ясное ощущение, что Part VIII работает как единая operating model, а не как набор разрозненных security chapters.
