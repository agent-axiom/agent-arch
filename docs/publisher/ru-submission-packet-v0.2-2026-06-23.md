# Submission packet v0.2

Дата: 2026-06-23.

Назначение: собрать текущие артефакты рукописи, ограничения и следующий порядок действий в один пакет для редакционной подготовки. Это не финальная сдача в издательство; это управляемая точка handoff перед авторским заполнением, link restoration и внешней вычиткой.

## Текущий статус рукописи

Рукопись перешла из compressed editorial assembly в полнообъемный рабочий вариант:

- Google Doc source: `https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI`;
- Google Docs PDF volume: 647 страниц;
- publisher DOCX derivative: `docs/publisher/artifacts/agent-arch-ru-template2000n-full-2026-06-23.docx`;
- publisher derivative PDF volume после Template2000n pass: 388 страниц;
- текстовых абзацев: 7801;
- ориентировочно слов: 97759;
- символов: 756102;
- TODO/FIXME/TBD markers: 0;
- авторские placeholders: есть, см. author pass;
- link restoration: требуется отдельный проход после подтверждения companion URL.

## Основные артефакты

| Артефакт | Назначение | Статус |
| --- | --- | --- |
| Google Doc source | Рабочая рукопись и source manuscript для издательства | Актуален, но требует author fill и финального cleanup. |
| `docs/publisher/artifacts/agent-arch-ru-template2000n-full-2026-06-23.docx` | Publisher-style DOCX proof | Создан и отрендерен. |
| `docs/publisher/ru-template2000n-full-pass-2026-06-23.md` | Отчет о полном Template2000n pass | Готов. |
| `docs/publisher/ru-template2000n-full-pass-2026-06-23.metrics.json` | Структурные метрики DOCX pass | Готов. |
| `docs/publisher/ru-template2000n-full-pass-2026-06-23.render-qa.json` | Render QA proof metrics | Готов. |
| `docs/publisher/ru-editorial-100-iteration-plan-2026-06-23.md` | Первый 100-iteration editorial backlog | Готов. |
| `docs/publisher/ru-author-pass-2026-06-23.md` | Author-owned поля | Готов. |
| `docs/publisher/ru-link-restoration-pass-2026-06-23.md` | Политика ссылок | Готов. |
| `docs/publisher/ru-front-matter-cleanup-pass-2026-06-23.md` | Решение по служебным строкам front matter | Готов. |
| `docs/publisher/ru-editorial-100-next-iterations-2026-06-23.md` | Дополнительные 100 итераций, 101-200 | Готов. |

## Что можно отдавать редактору сейчас

Редактору уже можно отдавать:

- полнообъемный Google Doc как живую рукопись;
- publisher DOCX derivative как style/render proof;
- отчет о Template2000n pass;
- author pass;
- link restoration pass;
- front matter cleanup pass;
- оба 100-iteration backlog как карту дальнейшей доводки.

При передаче нужно явно указать, что это editorial preparation packet, а не финальный "approved for print" файл.

## Что нельзя считать закрытым

До финальной сдачи нельзя считать закрытыми:

- блок "Об авторе";
- благодарности/посвящение, если они нужны;
- финальный companion URL;
- errata/contact route;
- политику активных hyperlinks;
- удаление служебных строк из тела книги;
- полный человеческий proofread всех страниц;
- fact-check современных спецификаций, продуктов, товарных знаков и ссылок;
- финальную стилистическую вычитку после редактора.

## Рекомендуемый порядок сдачи в редактуру

1. Автор заполняет author-owned поля.
2. Служебные строки front matter переносятся из тела рукописи в cover note.
3. Подтверждается companion URL и repository URL.
4. Выполняется link restoration pass.
5. Редактор получает Google Doc + DOCX proof + этот packet.
6. После редакторских правок выполняется fresh DOCX export.
7. Повторяется Template2000n pass и render QA.
8. Только после этого собирается финальный submission package.

## Cover note draft

```text
Передаю полнообъемную русскую рукопись книги "Архитектура безопасных ИИ-агентов" для редакционной подготовки.

Источник рукописи: Google Doc.
Производный DOCX proof: собран с применением Template2000n и прошел автоматический render QA.
Текущий объем: 647 страниц в Google Docs PDF, 388 страниц в publisher derivative PDF.

Важно: авторский блок, финальные публичные ссылки, companion URL, errata route и внешняя вычитка еще не закрыты. Служебные строки о source-to-print сборке должны оставаться в сопроводительном пакете, а не в читательском тексте.
```

## Следующий пункт

Submission packet v0.2 готов. Следующий шаг - дополнительные 100 итераций 101-200: editorial development backlog для доведения рукописи до сильного редакционного варианта.
