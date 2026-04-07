# Часть VIII. Жизненный цикл агентной системы

До этого момента книга объясняла, как собрать архитектуру, защитить ее, наблюдать за ней и безопасно выкатывать изменения. Но производственная дисциплина не заканчивается на чеклисте выкладки.

Если система живет дольше одной демки, у тебя почти сразу появляются вопросы другого класса:

- как принимать агентные инициативы в работу;
- как проводить design review;
- какие изменения считать risk-bearing;
- как выпускать model, prompt, policy и tool changes;
- как расследовать инциденты и когда выводить систему из эксплуатации.

Именно здесь обычная инженерная дисциплина встречается с агентной спецификой. Поэтому эту часть логично начинать не с “магического нового процесса”, а с перехода от классического SDLC к ADLC.

Если читать эту часть как единый блок, логика очень простая:

- сначала ты выравниваешь понятийную рамку через переход от SDLC к ADLC;
- потом понимаешь, какие изменения в агентной системе вообще считаются release-bearing;
- затем строишь assurance loop вокруг red teaming, detection и response;
- после этого закрепляешь artifact discipline и provenance;
- и только в конце закрываешь жизненный цикл через replacement и retirement.

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
- рабочую рамку для управления всем контуром агентов, а не только отдельными agent systems.
