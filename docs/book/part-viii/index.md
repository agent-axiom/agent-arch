# Часть VIII. Жизненный цикл агентной системы

До этого момента книга объясняла, как собрать архитектуру, защитить ее, наблюдать за ней и безопасно выкатывать изменения. Но production discipline не заканчивается на rollout checklist.

Если система живет дольше одной демки, у тебя почти сразу появляются вопросы другого класса:

- как принимать агентные инициативы в работу;
- как проводить design review;
- какие изменения считать risk-bearing;
- как выпускать model, prompt, policy и tool changes;
- как расследовать инциденты и когда выводить систему из эксплуатации.

Именно здесь обычная инженерная дисциплина встречается с агентной спецификой. Поэтому эту часть логично начинать не с “магического нового процесса”, а с перехода от классического SDLC к ADLC.

## В этой части

- [Глава 19. От SDLC к ADLC](chapter-19.md)
- [Глава 20. Change management для агентных систем](chapter-20.md)
- [Глава 21. Assurance loop: red teaming, detection и response](chapter-21.md)
- [Глава 22. Supply chain, provenance и approved artifacts](chapter-22.md)
- [Глава 23. Retirement, replacement и end-of-life discipline](chapter-23.md)

Следующие главы этой части логично строить вокруг change management, assurance loop, supply chain и retirement discipline.
