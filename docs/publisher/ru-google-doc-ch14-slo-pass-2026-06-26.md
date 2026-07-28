# Google Doc editorial pass: глава 14 SLO

Дата прохода: 2026-06-26

Google Doc: https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI

Рукопись: `Архитектура безопасных ИИ-агентов — полная рукопись`

Глава: `Глава 14. SLO для агентных систем`

Итоговая revision id после правки: `ALtnJHwy04sYLnrGqMbGQcmQIBs2QBDBFG9EYNkcaZ6EnbBoIq_m9cABGoXR_-nYcYGwjpow6GWzXgn8eMoI1u4Mm4z8W3gbQVdWGCodpvE`

## Что реализовано

1. Подтвержден рабочий диапазон главы 14 в Google Doc: исходная замена выполнена в body range `411668..431934`, после правки старт главы 15 найден на `428401`.
2. Opening главы 14 переписан как прямое продолжение главы 13: переход идет от одного trace к ежедневной эксплуатационной надежности.
3. Повторы про observability/trace сжаты: trace остался как источник доказательств, но не подменяет SLO.
4. Нормализованы рабочие определения `SLI`, `SLO`, `error budget`, `product metric` и `safety metric`.
5. SLO привязаны к agent failure modes: latency failure, unsafe action failure, silent refusal, tool outcome ambiguity, side-effect uncertainty, evidence failure, regression failure и ownership failure.
6. Разведены product metrics и safety metrics: product-успех не считается достаточным доказательством безопасности.
7. Alerting приведен к правилу `owner_role + expected_action + escalation path + linked runbook`.
8. Dashboard-примеры вынесены в companion route, в книге оставлены только decision excerpts и объяснение управленческого смысла.
9. Добавлен `SLO readiness checklist перед эксплуатацией` из восьми проверок перед production-запуском capability.
10. Подготовлены raw DOCX, Template2000n DOCX, render QA и следующий план из 100 редакционных итераций.

## Проверенные маркеры

- `Глава 13 закончилась на trace`
- `SLO, SLI и error budget: рабочее соглашение главы`
- `Терминологическое правило главы: product metric говорит`
- `Failure modes, которые должны попасть в SLO`
- `Product metrics и safety metrics не должны конкурировать`
- `Минимальный набор SLO для агента поддержки`
- `Evidence completeness SLO`
- `Error budget как ограничитель rollout`
- `Alerting: у каждого сигнала должен быть owner и action`
- `Dashboards: что остается в книге, а что уходит в companion`
- `SLO readiness checklist перед эксплуатацией`
- `Companion route для главы 14`
- `Глава 15. Офлайн- и онлайн-оценки и регрессионные шлюзы`

## Артефакты

- Raw Google Docs export: `docs/publisher/artifacts/agent-arch-ru-ch14-slo-pass-2026-06-26.docx`
- Template2000n derivative: `docs/publisher/artifacts/agent-arch-ru-template2000n-ch14-slo-pass-2026-06-26.docx`
- Render QA summary: `docs/publisher/ru-google-doc-ch14-slo-pass-2026-06-26.render-qa.json`
- Следующие 100 итераций: `docs/publisher/ru-editorial-100-ch14-slo-iterations-2026-06-26.md`

## Render QA

Raw export:

- DOCX size: 711864 bytes.
- Rendered PDF size: 3890949 bytes.
- Page count: 621.
- Blankish pages: 0.
- Ключевые маркеры главы 14 и перехода к главе 15 найдены.

Template2000n derivative:

- DOCX size: 718680 bytes.
- Rendered PDF size: 5473509 bytes.
- Page count: 308.
- Blankish pages: 0.
- Визуально проверены страницы 176, 183, 184 и 185.
- Чеклист SLO после повторной нормализации отображается обычным текстом, без ложного повышения пунктов до крупных заголовков.

## Что остается заполнить автору

Эти поля намеренно остаются author-owned и не должны заполняться автоматически:

- `[Имя автора / публичное имя]`
- `[текущая роль, компания или независимый статус]`
- `[Имя автора]`
- `[основная область: агентные системы, безопасность ИИ, платформенная инженерия и т.д.]`
- `Роль или должность`
- `Ключевой опыт`
- `Публичные проекты`
- `Ссылки`
- `Формулировка для издательства`
- Посвящение и благодарности.
- Публичный URL companion-материалов.
- Канал errata/contact для читателей.
- Версия companion-пакета, которая будет соответствовать печатной рукописи.

## Редакционный вывод

Глава 14 теперь работает как самостоятельная эксплуатационная глава: она не повторяет observability из главы 13, а объясняет, какие SLO нужны агентной системе, как они связаны с failure modes, error budget, rollout decision, alerting и будущими eval gates. Следующий содержательный участок для такого же прохода - глава 15: offline/online evals и regression gates должны стать продолжением SLO, а не отдельным набором тестов.
