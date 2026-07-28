# Google Doc editorial pass: глава 16 evidence chain

Дата прохода: 2026-06-27

Google Doc: https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI

Рукопись: `Архитектура безопасных ИИ-агентов — полная рукопись`

Глава: `Глава 16. Сквозная цепочка доказательств: от запроса к поэтапному выпуску`

Итоговая revision id после правки: `ALtnJHwPBkw08Z5wdMXfcli1CM9XJNM2cPmohRMbxMps8OEDUzyzP400KZlZNaQNTN4izCQgjgNvqnBVZcxTNRNbALMYSE_kcq-lAxLU3h4`

## Что реализовано

1. Подтвержден диапазон главы 16 в Google Doc: замена выполнена в body range `449330..475995`, после правки `Часть VI` начинается на `466800`, глава 17 начинается на `466851`.
2. Opening главы 16 переписан как прямое продолжение release verdict из главы 15: verdict становится доказательством только при наличии связанной evidence chain.
3. Нормализован словарь: `request`, `trace`, `policy decision`, `approval`, `eval verdict`, `SLO snapshot`, `rollout gate`, `incident evidence`.
4. Убраны устаревшие ссылки на неверные номера глав и старые reference-heavy фрагменты с validation-message dumps.
5. Добавлен минимальный набор идентификаторов: `run ID`, `request ID`, `capability ID/version`, `policy bundle ID/version`, `eval run ID`, `approval ID`, `override ID`, `rollout decision ID`, `incident ID`.
6. Добавлен сценарий подозрительного запуска duplicate-ticket agent после limited rollout.
7. Evidence chain связана с `override record`: reason, scope, owner, expiry, compensating controls, linked risk and rollback trigger.
8. Полные schema examples, JSON payloads, validation-message catalogs and CLI transcripts вынесены в companion route.
9. Добавлен `Readiness checklist для evidence chain`.
10. Подготовлены raw DOCX, Template2000n DOCX, render QA и следующий план из 100 редакционных итераций.

## Проверенные маркеры

- `Глава 15 закончилась не на красивом отчете`
- `Рабочее соглашение главы`
- `Минимальный набор идентификаторов`
- `Связь с override record`
- `Companion route для главы 16`
- `Readiness checklist для evidence chain`
- `Часть VI. Организационная модель`
- `Глава 17. Платформенная команда`

## Артефакты

- Raw Google Docs export: `docs/publisher/artifacts/agent-arch-ru-ch16-evidence-chain-pass-2026-06-27.docx`
- Template2000n derivative: `docs/publisher/artifacts/agent-arch-ru-template2000n-ch16-evidence-chain-pass-2026-06-27.docx`
- Render QA summary: `docs/publisher/ru-google-doc-ch16-evidence-chain-pass-2026-06-27.render-qa.json`
- Следующие 100 итераций: `docs/publisher/ru-editorial-100-ch16-evidence-chain-iterations-2026-06-27.md`

## Render QA

Raw export:

- DOCX size: 674378 bytes.
- SHA256: `cdd96c2733604f51d98fa80ef8425b3ffcf63eef6dfce9d0078d7cc1d39db498`.
- Rendered PDF size: 3508769 bytes.
- Page count: 607.
- Blankish pages: 0.
- Ключевые маркеры главы 16 и перехода к главе 17 найдены.

Template2000n derivative:

- DOCX size: 676020 bytes.
- SHA256: `6fd0c9c73f87504f0173ad1a37a7ec69595d8c6bba09caf0b64364e1ccd0f035`.
- Rendered PDF size: 3802862 bytes.
- Page count: 280.
- Blankish pages: 0.
- Визуально проверены страницы 185, 189, 190 и 191.
- Для Template2000n derivative применен строгий mapping: `Heading1` только для реальных заголовков вида `Глава N.`, `Часть N.` и front matter; body `numPr` сняты, чтобы Google Docs list state не раздувал маркеры списков в proof.

## Что остается заполнить автору

Эти поля остаются author-owned:

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
- Версия companion-пакета, соответствующая печатной рукописи.

## Редакционный вывод

Глава 16 теперь работает как мост между release decision и организационной моделью. Она показывает, как verdict из главы 15 превращается в доказуемую цепочку: от request and trace до policy decision, approval, eval verdict, SLO snapshot, rollout gate and incident evidence. Следующий содержательный проход должен взять главу 17 и сделать ownership продолжением evidence chain: у каждого артефакта должен быть владелец, escalation path and decision boundary.
