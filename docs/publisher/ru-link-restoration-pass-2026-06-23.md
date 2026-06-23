# Link restoration pass

Дата прохода: 2026-06-23.

Назначение: зафиксировать политику восстановления ссылок перед редакционной сдачей и отделить печатные ссылки от companion/source navigation.

Исходная точка:

- publisher DOCX derivative: `docs/publisher/artifacts/agent-arch-ru-template2000n-full-2026-06-23.docx`;
- Google Docs PDF volume: 647 страниц;
- publisher derivative PDF volume: 388 страниц;
- текстовых абзацев: 7801;
- broad URL-like occurrences по текущему DOCX inspection: 22;
- true public HTTP(S) references в теле рукописи: 16;
- hyperlinks в Google Docs DOCX export сейчас требуют отдельного восстановления/нормализации.

## Статус

В текущем publisher derivative ссылки в основном представлены как plain text. Это приемлемо для чтения и редакционного proof, но недостаточно для финального DOCX/PDF/EPUB.

Финальный link restoration нужно делать после двух авторских решений:

1. какой companion URL является стабильным публичным адресом;
2. какие GitHub/source references разрешено оставлять прямо в книге.

## Обнаруженные классы ссылок

| Класс | Примеры | Решение для печатной книги |
| --- | --- | --- |
| Public companion | `https://agent-axiom.github.io/agent-arch/` | Оставить в front/back matter и сделать активной ссылкой. |
| Source repository | `https://github.com/agent-axiom/agent-arch` | Оставить один раз как исходный репозиторий/companion source. |
| Runtime reference root | `https://github.com/agent-axiom/agent-arch/tree/main/agent_runtime_ref` | Лучше заменить на короткую ссылку companion route или дать один раз в приложении. |
| Runtime file references | `approvals.py`, `memory.py`, `rollout.py`, `lifecycle.py`, `configs/*.yaml` | В книге оставить file labels, полные URLs перенести в companion. |
| Internal docs paths | `docs/appendix/sources.md`, `docs/appendix/reference-package.md`, `docs/companion/runtime-reference/` | В печатной книге использовать как companion navigation labels, не как основной URL-слой. |
| Front matter source note | `docs/book/`, `docs/appendix/` | Убрать из тела книги, оставить в cover note/submission packet. |

## Конкретные URL-like occurrences

| Абзац | Ссылка / путь | Редакционное действие |
| ---: | --- | --- |
| 4 | `docs/book/`, `docs/appendix/` | Перенести в cover note, из тела книги убрать. |
| 1511 | `agent_runtime_ref` root | Сократить до "см. runtime reference в companion". |
| 1512 | `approvals.py` | Оставить имя файла, полный URL в companion. |
| 1513 | `configs/approvals.yaml` | Оставить имя файла, полный URL в companion. |
| 2170 | `agent_runtime_ref` root | Сократить до companion reference. |
| 2171 | `memory.py` | Оставить имя файла, полный URL в companion. |
| 2172 | `background.py` | Оставить имя файла, полный URL в companion. |
| 2173 | `configs/memory.yaml` | Оставить имя файла, полный URL в companion. |
| 6199 | `agent_runtime_ref` root | Сократить до companion reference. |
| 6200 | `rollout.py` | Оставить имя файла, полный URL в companion. |
| 6201 | `lifecycle.py` | Оставить имя файла, полный URL в companion. |
| 6202 | `configs/rollout.yaml` | Оставить имя файла, полный URL в companion. |
| 6203 | `configs/change.yaml` | Оставить имя файла, полный URL в companion. |
| 6204 | `configs/runtime-controls.yaml` | Оставить имя файла, полный URL в companion. |
| 7673 | `agent_runtime_ref` root | Сократить до companion reference. |
| 7728 | `/README.md` | Не печатать как standalone URL; описать как companion root. |
| 7773 | `https://agent-axiom.github.io/agent-arch/` | Оставить, сделать активной ссылкой. |
| 7774 | `https://github.com/agent-axiom/agent-arch` | Оставить, сделать активной ссылкой. |
| 7777 | `docs/appendix/sources.md` | Оставить как label, полный путь в companion. |
| 7778 | `docs/appendix/reference-package.md` | Оставить как label, полный путь в companion. |
| 7779 | `docs/companion/runtime-reference/` | Оставить как companion route label. |

## Политика ссылок для книги

Для печатной и электронной версии нужна простая политика:

1. В основном тексте не держать длинные GitHub blob URLs.
2. В главе оставлять короткие имена артефактов: `approvals.py`, `memory.py`, `rollout.py`, `configs/approvals.yaml`.
3. Все длинные пути и актуальные URL держать в companion.
4. В приложении дать один стабильный companion URL и один repository URL.
5. Для EPUB/PDF сделать active hyperlinks только для стабильных публичных адресов.
6. Для печатной версии рядом с URL использовать человекочитаемую формулировку, а не raw path wall.

## Link restoration workflow

Практический порядок:

1. Автор подтверждает финальный companion URL и repository URL.
2. В Google Doc руками или batch pass заменяются длинные GitHub URLs на короткие labels там, где они мешают чтению.
3. В приложении "Online companion" остаются активные публичные ссылки.
4. После следующего DOCX export выполняется технический hyperlink restoration.
5. Рендеряется повторный proof и проверяются PDF/EPUB переходы.

## Что не делать

- Не восстанавливать все 22 URL-like occurrences как active links автоматически.
- Не оставлять `docs/book/` и `docs/appendix/` в front matter как часть читательского текста.
- Не превращать каждое имя файла в ссылку: это ухудшит печатное чтение.
- Не менять публичные URL до авторского подтверждения.

## Следующий пункт

Link restoration analysis закрыт. Следующий шаг внутри пункта 3 - front matter cleanup: служебные строки нужно вынести из рукописи в cover note/submission packet.
