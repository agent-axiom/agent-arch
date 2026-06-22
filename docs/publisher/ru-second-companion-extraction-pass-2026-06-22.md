# Второй проход выноса companion-материалов

Дата: 2026-06-22.

Целевой Google Doc: `Архитектура безопасных ИИ-агентов — полная рукопись`.

Документ: `https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI`

## Цель прохода

Продолжить превращение рукописи из технической source-to-print сборки в печатную книгу: оставить в Google Doc смысловые решения, переходы и критерии ревью, а полные YAML-формы, CLI-команды, eval datasets и trace/event catalogs вынести в companion.

Этот проход не сжимает книгу до краткого конспекта. Он убирает механические справочные блоки из глав, где они ломали книжный ритм, и добавляет рядом companion-страницы, где эти материалы можно версионировать и проверять.

## Что создано в companion

Добавлена папка `docs/companion/runtime-reference/`:

- `configs.md` — sandbox profile, MCP boundary, network/secrets/identity review, execution flow;
- `cli.md` — команды запуска, inspect/export workflows и критерии CLI-поверхности;
- `eval-datasets.md` — trace-to-eval, regression gate, verifier contract, rollout judgment;
- `traces-and-events.md` — event chain, обязательные поля trace, export workflow, validation-message классы.

## Что изменено в Google Doc

### Глава 11

Длинный практикум sandbox/MCP review был заменён печатным decision packet.

В печатной версии теперь остаются:

- зачем нужен review boundary до подключения capability;
- какие решения должны быть приняты до MCP-вызова;
- что должно быть видно в trace;
- какие минимальные признаки готовности отделяют prototype от production runtime.

В companion вынесены формы:

- `execution_boundary_review`;
- `sandbox_profile`;
- `sandbox_context`;
- `mcp_boundary`;
- `tool_content_controls`;
- `execution_flow`.

### Глава 15

Длинные YAML-формы практикума trace review -> regression gate были заменены короткой печатной цепочкой суждения.

В печатной версии теперь остаются:

- как один спорный trace становится источником eval-сценария;
- какие outcomes и blocking rules превращают его в regression gate;
- что должен проверять verifier;
- как rollout judgment фиксирует выпускное решение.

В companion вынесены формы:

- `trace_to_eval_source`;
- `regression_gate`;
- `verifier_contract`;
- `rollout_judgment`.

## Проверки Google Doc

Connector-readback:

- найден новый мост главы 11: `Шаг 1. Сжать sandbox/MCP review до одного decision packet`;
- найден новый мост главы 15: `Печатная версия этого практикума должна удержать не все YAML-формы`;
- старый YAML-маркер `execution_boundary_review:` больше не найден в Google Doc;
- старый YAML-маркер `trace_to_eval_source:` больше не найден в Google Doc.

DOCX export:

- файл экспортирован из Google Doc;
- `unzip -t` завершился без ошибок;
- в экспортированном DOCX найдено 7919 непустых параграфов;
- companion-ссылки `runtime-reference/configs` и `runtime-reference/eval-datasets` присутствуют.

PDF export:

- файл экспортирован из Google Doc;
- Google Docs PDF renderer: `Skia/PDF m151`;
- PDF не зашифрован;
- размер страницы: Letter, 612 x 792 pt;
- страниц после прохода: 657.

Визуальная QA:

- отрендерены страницы 259, 260 и 374;
- страницы вокруг заменённых блоков не показывают явных обрывов, наложений текста или пустых разрывов;
- визуальная проверка выполнена по PDF export, не по live browser canvas.

## Изменение объёма

После первого extraction-pass PDF содержал 679 страниц.

После второго extraction-pass PDF содержит 657 страниц.

Итого второй проход убрал примерно 22 страницы справочного YAML/CLI-подобного материала из печатного потока, сохранив смысловую линию через companion-мосты.

## Следующие редакционные шаги

1. Продолжить такой же вынос для оставшихся плотных приложений и хвостового reference package.
2. Исправить устаревшее слитное написание имени runtime-пакета в рукописи и заменить его на фактический пакет `agent_runtime_ref`, где это относится к репозиторию.
3. Отдельным проходом привести стиль новых companion-ссылок к финальному формату издательства, когда будет известен публичный URL companion-раздела.
4. После получения издательских стилей сделать DOCX/template pass, не смешивая его с содержательной редактурой.
