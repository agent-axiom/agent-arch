# Архитектура Безопасных AI-Агентов

Это книга для тех, кто хочет строить не “магических агентов из презентации”, а спокойные, управляемые и безопасные production-системы.

Ее центральный тезис очень простой: **агенту нужна платформа, а не магия**. Если команда относится к агенту как к промпту с прикрученными tools, система может впечатлять на демо и при этом начать ломаться сразу, как только появляются risky actions, memory, approvals, rollout и давление реальной эксплуатации.

Это практическая книга о безопасной, управляемой и production-ready архитектуре AI-агентов. Она нужна командам, которым мало промптов и tool calling, и которые хотят спроектировать всю операционную систему вокруг агента: trust boundaries, policy enforcement, approvals, evidence capture, health budgets, eval judgment и lifecycle management.

> За отправную точку я беру статью Дмитрия Викулина о надежных AI-агентах, а дальше расширяю ее до платформенного уровня: с политиками, человеческим подтверждением, наблюдаемостью, оценками, эксплуатационной дисциплиной и жизненным циклом.

<div class="hero-actions" markdown="1">

[С чего начать](start-here.md){ .md-button .md-button--primary }
[Открыть план книги](book/plan.md){ .md-button }
[Посмотреть справочный пакет](appendix/reference-package.md){ .md-button }

</div>

<div class="book-cover" markdown="1">

![Визуальная обложка книги](assets/images/hero-home.png)

</div>

## Зачем нужна эта книга

Большинство материалов про агентов оптимизируют путь к быстрому демо. Реальные системы ломаются в другом месте: на границе между reasoning и action, в memory layer, в approval paths, при rollout, в drift и в долгой операционной ответственности. Эта книга нужна, чтобы описать именно эту полную операционную модель.

Ее цель не в том, чтобы помочь собрать “самого автономного агента в комнате”. Ее цель в том, чтобы помочь собрать систему, которая выдерживает production reality.

## Для кого эта книга

- Для инженеров, которые добавляют agent features в продукт и не хотят превращать систему в набор промптов и исключений.
- Для платформенных команд, которым нужен общий рантайм, слой политик, реестр, подтверждения и наблюдаемость.
- Для security engineers, которым нужно видеть trust boundaries, risky execution paths и surfaces для abuse.
- Для техлидов и архитекторов, которым нужен не “вау-демо”, а рабочая инженерная дисциплина.

## Что можно забрать в работу уже сегодня

- Маршрут от workflow к agent system без преждевременного усложнения.
- Практические главы про policy layer, approvals, memory, evals и lifecycle.
- Исполняемый справочный рантайм с экспортом сессий, экспортом eval-наборов, подтверждениями, контролями и артефактами жизненного цикла.
- Справочные схемы для traces, eval datasets, policy bundles, approvals, rollout gates, memory retrieval и lifecycle artifacts.
- Кейсы, чеклисты и шаблоны политик, которые можно брать как стартовые артефакты.

## Что это за книга

В первую очередь это практическая архитектурная книга и operating model для production agent systems.

Это не manual по одному фреймворку, не пособие по prompt engineering и не хайповый обзор AI-экосистемы. Справочный слой и runnable runtime здесь нужны для поддержки аргумента книги, а не для замены самой книги.

И это еще и намеренно собранная книга, а не просто набор хороших тем. Operational chapters разведены по ролям так, чтобы читатель чувствовал, как собирается production discipline:

- traces захватывают raw run history;
- SLO задают health и risk budgets;
- evals производят reviewable judgments;
- assurance отвечает за response;
- provenance и artifacts сохраняют evidence backbone;
- observability дает evidence substrate;
- registry задает accountability всего estate.

И эта форма должна чувствоваться как reader outcomes, а не только как chapter taxonomy:
- Part V учит читателя захватывать run history, задавать допустимые budgets и производить reviewable judgments;
- Part VIII учит читателя управлять lifecycle response, governed lineage, evidence visibility и accountability всего estate как одним production contour.

## Состояние проекта

- `Published core`: восемь частей книги уже опубликованы.
- `Expanding now`: входные страницы, справочный слой и навигация еще доводятся.
- `Справочные материалы доступны`: уже есть схемы, чеклисты, кейсы и исполняемый справочный рантайм.

## Три удобных маршрута чтения

### Если ты строишь продуктового агента

1. [Глава 1. Почему агенту нужна платформа, а не магия](book/part-i/chapter-1.md)
2. [Глава 3. Контур безопасности и границы доверия](book/part-ii/chapter-3.md)
3. [Глава 8. Модель выполнения и каталог инструментов](book/part-iv/chapter-8.md)
4. [Глава 13. Офлайн-оценки, онлайн-оценки и регрессионные шлюзы](book/part-v/chapter-13.md)

### Если ты строишь платформу или runtime

1. [Глава 2. Референсная архитектура безопасного агента](book/part-i/chapter-2.md)
2. [Глава 4. Инструментальный шлюз, подтверждения и журнал аудита](book/part-ii/chapter-4.md)
3. [Глава 17. Слой политик и каталог возможностей](book/part-vii/chapter-17.md)
4. [Глава 20. Change management для агентных систем](book/part-viii/chapter-20.md)

### Если тебе важны безопасность, контроль и эксплуатация

1. [Глава 21. Assurance loop: red teaming, detection и response](book/part-viii/chapter-21.md)
2. [Глава 22. Supply chain, provenance и approved artifacts](book/part-viii/chapter-22.md)
3. [Глава 26. AI-native observability, inventory coverage и detection-ready telemetry](book/part-viii/chapter-26.md)
4. [Глава 27. Agent inventory, registry и борьба с sprawl](book/part-viii/chapter-27.md)

## Что уже есть в проекте

- Полноценная книга на `ru / en / zh`.
- Исполняемый пакет `agent_runtime_ref` с `pytest`-покрытием.
- Справочный слой со схемами и контрактными страницами.
- Практическое приложение с кейсами, чеклистами, глоссарием и дорожной картой.

## Главная инженерная идея

Самая частая ошибка в агентных системах простая: сначала все пытаются добиться автономности, и только потом вспоминают про управляемость. На практике лучше работает другой путь:

1. Сначала ты строишь **предсказуемый workflow**.
2. Потом добавляешь автономность **локально и измеримо**.
3. Все опасные действия пропускаешь через **политики, подтверждения и трассировку**.
4. Качество держишь не обещаниями модели, а **health budgets, eval judgment, telemetry и жизненным циклом**.

## Где лежит справочный слой

Если тебе нужны не только главы, но и готовые артефакты, начни с этих support pages. Они нужны, чтобы закреплять аргумент книги, а не заменять ее reader journey:

- [Схема трасс и каталог событий](appendix/trace-schema.md)
- [Схема наборов для оценки и правил проверки](appendix/eval-schema.md)
- [Схема набора политик и контракта подтверждения](appendix/policy-bundle-schema.md)
- [Схема артефактов жизненного цикла](appendix/lifecycle-artifact-schema.md)
- [Схема записей памяти и контракта извлечения](appendix/memory-retrieval-schema.md)

## Дальше по сайту

[С чего начать](start-here.md){ .md-button .md-button--primary }
[Открыть справочные страницы](appendix/trace-schema.md){ .md-button }
[Посмотреть источники](appendix/sources.md){ .md-button }
