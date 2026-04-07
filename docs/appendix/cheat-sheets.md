# Шпаргалки

Эта страница нужна для быстрых рабочих проверок. Если тебе не хочется перечитывать целую часть книги перед ревью дизайна, запуском агента или обсуждением с командой, начни отсюда.

## Safety checklist

- Есть ли у агента явные trust boundaries между вводом пользователя, памятью, инструментами и внешними системами?
- Есть ли policy gate перед каждым чувствительным действием, а не только перед вызовом модели?
- Разделены ли low-risk и high-risk инструменты?
- Есть ли approval gate для действий с необратимым side effect?
- Зафиксированы ли allowed egress destinations и network access profile?
- Пишется ли audit trail для policy decisions, approvals и tool execution?
- Есть ли понятный stop condition для run loop?

Читать дальше:

- [Глава 3. Контур безопасности и границы доверия](../book/part-ii/chapter-3.md)
- [Глава 4. Инструментальный шлюз, подтверждения и журнал аудита](../book/part-ii/chapter-4.md)

## Memory checklist

- Разделены ли short-term, long-term и profile memory?
- Есть ли разные правила для memory read и memory write?
- Хранится ли provenance у persistent records?
- Есть ли policy для того, что разрешено записывать в память?
- Есть ли compaction или background maintenance path?
- Ограничен ли retrieval по объему и релевантности?
- Есть ли clear deletion или revision strategy?

Читать дальше:

- [Глава 5. Зачем агенту память и почему она опасна](../book/part-iii/chapter-5.md)
- [Глава 7. Извлечение контекста, уплотнение и фоновые обновления](../book/part-iii/chapter-7.md)

## Rollout checklist

- Есть ли owner у агента, а не только команда “вообще”?
- Есть ли минимальный eval baseline до запуска?
- Есть ли rollout gate с safety, observability и approval requirements?
- Понятно ли, какие сценарии считаются blocking failures?
- Есть ли runbook на отказ, denial и approval backlog?
- Есть ли канал для incident review и postmortem?
- Можно ли быстро отключить high-risk capability без полной остановки системы?

Читать дальше:

- [Глава 12. SLO для агентных систем](../book/part-v/chapter-12.md)
- [Глава 18. Чеклист промышленного запуска](../book/part-vii/chapter-18.md)

## Observability checklist

- Есть ли trace_id у каждого запуска?
- Есть ли базовые spans для retrieval, model step, tool execution, approval и memory write?
- Есть ли structured events, а не только сырые логи?
- Видно ли, какой policy decision принял gateway?
- Видно ли, какой tool principal исполнил side effect?
- Можно ли отличить success, denied, approval_wait и failure?
- Есть ли way to aggregate runs into session-level or eval-level summaries?

Читать дальше:

- [Глава 11. Трассы, спаны и структурированные события](../book/part-v/chapter-11.md)
- [Глава 13. Офлайн-оценки, онлайн-оценки и регрессионные шлюзы](../book/part-v/chapter-13.md)

## Tool gateway checklist

- У каждой capability есть owner, risk tier и approved inventory status?
- Ясно ли, read это tool или write tool?
- Есть ли execution profile: sandbox, network access, allowed egress?
- Проверяет ли gateway actor identity и policy before execution?
- Есть ли idempotency semantics и retry policy?
- Понятно ли, когда нужен approval, а когда tool может исполниться автоматически?
- Есть ли audit trail на каждое внешнее действие?

Читать дальше:

- [Глава 8. Модель выполнения и каталог инструментов](../book/part-iv/chapter-8.md)
- [Глава 9. Песочница выполнения и MCP как интеграционный контракт](../book/part-iv/chapter-9.md)
- [Глава 10. Идемпотентность, повторы, лимиты запросов и границы отката](../book/part-iv/chapter-10.md)

## Как использовать эти шпаргалки

- Перед design review: быстро пройти safety, memory и tool gateway блоки.
- Перед запуском: пройти rollout и observability блоки.
- Во время incident review: использовать observability и safety блоки как каркас разбора.

- [С чего начать](../start-here.md)
- [Глоссарий терминов](glossary.md)
- [Шаблоны политик и проверочные списки по кейсам](policy-templates.md)
