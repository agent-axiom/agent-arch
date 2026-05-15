# Книга

Это главная входная страница самой книги. Если нужен самый короткий путь в основной текст, начинай с [Части I. Основания](part-i/index.md). Если сначала хочется увидеть структуру и статус публикации, открой [План книги](plan.md).

## Что обещает эта книга

У книги один главный тезис: агенту нужна платформа, а не магия.

Агентов строить скучно, но результат ошеломляющий: вместо эффектного разового трюка появляется система, которую можно ограничивать, наблюдать, выпускать и улучшать без гадания.

После чтения ты должен уметь:

- понимать, когда агент действительно нужен, а когда достаточно обычного workflow;
- видеть минимальный набор платформенных слоев, без которых нельзя пускать систему к рискованным действиям;
- прослеживать один управляемый run через policy, execution, evidence, approval, rollout и lifecycle control;
- рассматривать memory, evals, provenance, retirement и operator accountability как единую рабочую модель.

!!! example "Сквозной кейс поддержки"
    Один из способов читать книгу — следить за кейсом support-triage: от retrieval и tool execution до duplicate-ticket recovery, traces, SLO, eval gates, ownership, reference runtime, policy, rollout, ADLC, assurance, provenance, retirement, misalignment controls, telemetry и registry. Это превращает главы из набора тем в одну проверяемую историю о том, как инцидент становится платформенным контрактом.

!!! note "Canonical case map"
    Support triage остается основной нитью для write capabilities, approvals и duplicate-ticket recovery. Internal knowledge assistant проверяет, что retrieval, memory, tenant boundaries, freshness и source grounding не потерялись в архитектуре. Incident coordination проверяет traces, SLO, escalation, notification side effects, response ownership и post-incident learning. Вместе эти три canonical cases делают книгу не одной историей про поддержку, а картой разных control surfaces.

## Рекомендуемый маршрут чтения

Если нужен самый короткий полезный маршрут, иди так:

1. [Часть I. Основания](part-i/index.md)
2. [Часть II. Контур безопасности](part-ii/index.md)
3. [Часть III. Память и знания](part-iii/index.md)
4. [Часть IV. Инструменты и выполнение](part-iv/index.md)
5. [Часть V. Надежность и наблюдаемость](part-v/index.md)
6. [Часть VI. Организационная модель](part-vi/index.md)
7. [Часть VII. Эталонная реализация](part-vii/index.md)
8. [Часть VIII. Жизненный цикл агентной системы](part-viii/index.md)

## Быстрый ориентир по стабильности

У книги есть два практических слоя:

- `Стабильное ядро`: части I-VII, особенно главы 1-12 и 18;
- `Быстро меняющийся слой`: глава 13, часть VIII и исследовательские страницы приложений.

Если читаешь книгу впервые, сначала лучше пройти стабильное ядро, а потом вернуться к более подвижному слою.

## Прямые точки входа

- [Начать с Части I](part-i/index.md)
- [Открыть план книги](plan.md)
- [Перейти к Сквозной цепочке доказательств](part-v/evidence-spine.md)
- [Перейти к жизненному циклу агентной системы](part-viii/index.md)

[Читать книгу](part-i/index.md){ .md-button .md-button--primary }
[Открыть план](plan.md){ .md-button }
