# Google Doc editorial pass: глава 15 eval gates

Дата прохода: 2026-06-27

Google Doc: https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI

Рукопись: `Архитектура безопасных ИИ-агентов — полная рукопись`

Глава: `Глава 15. Офлайн- и онлайн-оценки и регрессионные шлюзы`

Итоговая revision id после правки: `ALtnJHy_nhZtPAaknr8gSZ20lp3_iAMQsDSEa_Nit44PXXaYwPnVVc82ZUnlGwKpmmXBDHn6aGFKV_PPu25mUp3hmwir1smZbtPwCkxBG54`

## Что реализовано

1. Подтвержден диапазон главы 15 в Google Doc: исходная замена выполнена в body range `428401..476889`, после правки старт главы 16 найден на `449330`.
2. Opening главы 15 переписан как прямое продолжение главы 14: SLO показывает operational health, а eval gate отвечает, можно ли выпускать изменение.
3. Разведены `offline evals`, `online evals`, `regression gates`, `judge`, `verdict` и `threshold`.
4. Eval cases привязаны к failure modes из главы 14: latency, unsafe action, silent refusal, tool outcome ambiguity, side-effect uncertainty, evidence, regression and ownership.
5. Добавлен сценарий duplicate ticket regression: проверяется не только ответ, но intent, policy decision, tool outcome, idempotency, reconciliation and final verification.
6. Добавлен release decision table в печатном виде: signal, threshold, owner, release action.
7. Добавлены разделы про `false pass` и `false block`.
8. Добавлены override rules: owner, scope, expiry, compensating controls, rollback condition and evidence bundle.
9. Длинные datasets, scoring scripts, judge prompts, CLI output, dashboard JSON and full payloads вынесены в companion route.
10. Подготовлены raw DOCX, Template2000n DOCX, render QA и следующий план из 100 редакционных итераций.

## Проверенные маркеры

- `Глава 14 закончилась на SLO`
- `Рабочее соглашение главы`
- `Regression gate contract`
- `Coverage по failure modes из главы 14`
- `Decision table для release gate`
- `False pass`
- `False block`
- `Override не должен быть обходом контроля`
- `Eval readiness checklist перед rollout`
- `Companion route для главы 15`
- `Глава 16. Сквозная цепочка доказательств`

## Артефакты

- Raw Google Docs export: `docs/publisher/artifacts/agent-arch-ru-ch15-eval-gates-pass-2026-06-27.docx`
- Template2000n derivative: `docs/publisher/artifacts/agent-arch-ru-template2000n-ch15-eval-gates-pass-2026-06-27.docx`
- Render QA summary: `docs/publisher/ru-google-doc-ch15-eval-gates-pass-2026-06-27.render-qa.json`
- Следующие 100 итераций: `docs/publisher/ru-editorial-100-ch15-eval-gates-iterations-2026-06-27.md`

## Render QA

Raw export:

- DOCX size: 685185 bytes.
- Rendered PDF size: 3632591 bytes.
- Page count: 614.
- Blankish pages: 0.
- Ключевые маркеры главы 15 и перехода к главе 16 найдены.

Template2000n derivative:

- DOCX size: 688053 bytes.
- Rendered PDF size: 3480811 bytes.
- Page count: 330.
- Blankish pages: 0.
- Визуально проверены страницы 193, 201, 205, 206 и 207.
- Для Template2000n derivative сохранены typography assets шаблона, но body `numPr` сняты, чтобы старые Google Docs list properties не раздували маркеры списков в proof.

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

Глава 15 теперь работает как release-decision глава: она объясняет, какие offline checks должны остановить опасное изменение до rollout, какие online signals останавливают уже выпущенную волну, как gate отличает hard blockers от warnings, почему false pass и false block оба опасны, и какие evidence нужны для override. Следующий содержательный проход должен взять главу 16 и сделать сквозную цепочку доказательств продолжением eval gate, а не отдельным набором ссылок на trace, SLO and rollout.
