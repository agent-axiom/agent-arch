# Google Doc editorial pass: глава 17 ownership

Дата прохода: 2026-06-27

Google Doc: https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI

Рукопись: `Архитектура безопасных ИИ-агентов — полная рукопись`

Глава: `Глава 17. Платформенная команда и продуктовые команды`

Итоговая revision id после правки: `ALtnJHyFmRqkbvGG-qsEouswRq4sFXlDcXCEKbMzYNA430Zubk5zUDtm_oAhni8bYiifRnpdcq4Gm3u2Nl_lxPaDpXqJ_OAAOaoMRCTRl-4`

## Что реализовано

1. Глава 17 переписана как продолжение главы 16: evidence chain теперь получает owner map и организационную границу ответственности.
2. Разведены `platform-owned artifacts` и `product-owned artifacts`.
3. Добавлен owner map для `request`, `trace`, `policy decision`, `approval`, `eval verdict`, `rollout gate` и `incident evidence`.
4. Уточнена граница между `common gateway` и `domain decision`.
5. Добавлены анти-паттерны `platform as bottleneck` и `local agent zoo`.
6. Ownership связан с `override record`, включая owner возврата, expiry и compensating controls.
7. RACI-like matrices перенесены в companion route, а в печатном тексте оставлена логика по evidence artifacts.
8. Добавлен `Readiness checklist: ownership review`.
9. При проверке диапазона обнаружено, что прежнее тело главы 18 находилось между главами 17 и 19; глава 18 восстановлена отдельным body chapter перед главой 19 и состыкована с новой логикой ownership -> standard paths.
10. Подготовлены raw DOCX, Template2000n DOCX, render QA и следующий план из 100 редакционных итераций.

## Проверенные маркеры

- `Глава 17. Платформенная команда`
- `Platform-owned artifacts`
- `Product-owned artifacts`
- `Owner map для evidence chain`
- `Граница common gateway и domain decision`
- `Override record как проверка ownership`
- `RACI-подобные матрицы и companion route`
- `Readiness checklist: ownership review`
- `Глава 18. Поддерживаемые стандартные пути`
- `Глава 19. От SDLC к ADLC`

## Артефакты

- Raw Google Docs export: `docs/publisher/artifacts/agent-arch-ru-ch17-ownership-pass-2026-06-27.docx`
- Template2000n derivative: `docs/publisher/artifacts/agent-arch-ru-template2000n-ch17-ownership-pass-2026-06-27.docx`
- Render QA summary: `docs/publisher/ru-google-doc-ch17-ownership-pass-2026-06-27.render-qa.json`
- Следующие 100 итераций: `docs/publisher/ru-editorial-100-ch17-ownership-iterations-2026-06-27.md`

## Render QA

Raw export:

- DOCX size: 683265 bytes.
- SHA256: `7e4d73fc0fa88d8e8f99044eb8dd92e514cbc7b73a7c6819699d52a93158ff5d`.
- Rendered PDF size: 3543936 bytes.
- Page count: 620.
- Blank-like pages: 0.
- Визуально проверены страницы 378, 383, 388, 403, 406, 407 и 423.

Template2000n derivative:

- DOCX size: 685630 bytes.
- SHA256: `dcd2314a53ae9261c5e49567b1472cc9d5ede555972aaffa120b0ef7a908ef42`.
- Rendered PDF size: 3564306 bytes.
- Page count: 331.
- Blank-like pages: 0.
- Визуально проверены страницы 215, 217, 220, 226, 227, 228 и 236.
- Для Template2000n derivative применен conservative mapping: `Heading1` для глав/частей/front matter, `Heading3` для новых подзаголовков главы 17/18, основной текст в `BodyText`, body `numPr` сняты.

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

Глава 17 теперь связывает evidence chain с ownership: у каждого доказательного артефакта есть владелец, граница решения, override behavior и readiness review. Глава 18 восстановлена как отдельный следующий шаг: ownership превращается в поддерживаемые standard paths, common gateways и борьбу с local agent zoo. Следующий содержательный проход должен взять главу 19 и усилить ADLC как lifecycle для всех surface, которые меняют поведение агента.
