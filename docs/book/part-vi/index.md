# Часть VI. Организационная модель

К этому моменту у нас уже есть почти весь технический каркас:

- архитектура;
- безопасность;
- память;
- execution layer;
- observability и eval loop.

Но дальше почти всегда начинается не технический, а организационный bottleneck.

Даже хорошая agent platform быстро упрется в вопросы:

- кто владеет базовыми слоями;
- кто отвечает за policy и guardrails;
- как продуктовые команды используют платформу, не ломая ее;
- как не получить пять несовместимых agent runtimes внутри одной компании.

В этой части мы разберем operating model: кто за что отвечает, как строить golden paths и как не превратить платформу в хаотичный набор локальных решений.

## В этой части

- [Глава 14. Platform team vs product teams](chapter-14.md)
- [Глава 15. Golden paths, shared gateways и anti-zoo patterns](chapter-15.md)

Дальше логично добить platform roadmap и перейти к reference implementation.
