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
    - [Глава 21](chapter-21.md) и [Глава 22](chapter-22.md): собрать assurance, provenance и artifact discipline;
    - [Глава 23](chapter-23.md): закрыть lifecycle через replacement и retirement.

    Главы 24-27 расширяют этот же контур через misalignment, behavioral evals, AI-native observability и управление agent estate.

## Что решает эта часть

- переводит reference implementation в управляемый lifecycle;
- связывает change management, assurance, provenance, incidents, retirement, observability и agent-estate governance в один operational contour;
- отделяет устойчивую инженерную дисциплину от быстро меняющихся vendor- и research-layer деталей.

Если читать эту часть как единый блок, порядок такой:

- сначала ты выравниваешь понятийную рамку через переход от SDLC к ADLC;
- потом понимаешь, какие изменения в агентной системе вообще считаются release-bearing;
- затем строишь assurance loop вокруг red teaming, detection и response;
- после этого закрепляешь artifact discipline и provenance;
- затем закрываешь жизненный цикл через replacement и retirement;
- и в конце расширяешь тот же контур на misalignment, behavioral assurance, AI-native observability и управление всем agent estate.

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
- понятную связь между evals, incidents, provenance и рабочей ответственностью;
- практический язык для разговоров о replacement, retirement и end-of-life discipline;
- более зрелую рамку для sabotage-like behavior, control failures и automated assurance;
- представление о observability как о слое доказательств для inventory, detection и governance;
- рабочую рамку для управления всем контуром агентов, а не только отдельными agent systems;
- более ясное ощущение, что Part VIII работает как единая operating model, а не как набор разрозненных security chapters.
