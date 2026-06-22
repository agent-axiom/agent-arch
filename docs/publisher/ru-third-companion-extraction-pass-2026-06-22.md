# Третий проход выноса companion-материалов

Дата: 2026-06-22.

Целевой Google Doc: `Архитектура безопасных ИИ-агентов — полная рукопись`.

Документ: `https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI`

## Цель прохода

Закрыть хвостовую перегрузку приложения `Источники и online companion`: убрать из печатного Google Doc длинный source catalog и reference-package walkthrough, оставить компактную навигацию, а полные материалы закрепить в versioned companion и публичной документации.

## Что изменено в Google Doc

Длинный хвост приложения заменён компактным навигационным блоком.

После визуальной проверки хвоста также убрана устаревшая фраза о том, что адрес
online companion будет добавлен позднее: адрес уже зафиксирован для текущей
редакции. Повтор public/repo ссылок внутри компактного блока снят, а рабочие
пути вынесены под отдельную строку `Справочные маршруты:`.

В печатной рукописи теперь остаётся:

- публичный URL companion;
- URL исходного репозитория;
- ссылки на полный список источников и reference package walkthrough;
- указание на `docs/companion/runtime-reference/`;
- корректное имя исполняемого пакета `agent_runtime_ref/`;
- краткие маршруты по источникам;
- краткое объяснение роли reference package;
- правило переноса материалов в companion.

Из печатного потока удалены:

- полный source catalog;
- длинные списки ссылок;
- runtime command walkthrough;
- повторный reference-package разбор;
- устаревшее слитное имя runtime-пакета.

## Что изменено в repo

Добавлен `docs/companion/index.md` как входная страница online companion.

В `mkdocs.yml` добавлен top-level раздел `Online Companion`:

- `companion/index.md`;
- `companion/runtime-reference/configs.md`;
- `companion/runtime-reference/cli.md`;
- `companion/runtime-reference/eval-datasets.md`;
- `companion/runtime-reference/traces-and-events.md`.

Для RU/EN/ZH добавлены nav translations новых пунктов.

## Проверки readback

Connector-readback подтвердил:

- новый компактный блок содержит `Исполняемый пакет: agent_runtime_ref/.`;
- старое слитное имя runtime-пакета в Google Doc больше не находится;
- новая ссылка `Полный список источников: docs/appendix/sources.md.` присутствует.

## QA после экспорта

Финальный export QA выполнен по текущей Google Doc ревизии:

- DOCX export скачан во временный файл
  `/private/tmp/agent_arch_third_pass_20260622.docx`;
- `unzip -t /private/tmp/agent_arch_third_pass_20260622.docx` завершился без
  ошибок;
- PDF export скачан во временный файл
  `/private/tmp/agent_arch_third_pass_20260622.pdf`;
- `pdfinfo` показывает `Pages: 652`, формат `612 x 792 pts (letter)`,
  `Encrypted: no`, `PDF version: 1.4`;
- текстовый поиск по PDF нашёл `agent_runtime_ref`,
  `docs/appendix/sources.md` и `docs/companion/runtime-reference` в хвостовой
  части документа;
- текстовый поиск по PDF не нашёл устаревшее слитное имя runtime-пакета;
- контрольная страница хвоста отрендерена через `pdftoppm`: страница 650 из
  652 содержит public companion URL, repo URL, `Справочные маршруты`, sources,
  reference-package, runtime companion и `agent_runtime_ref`.

## Локальные проверки repo

После правок выполнены проверки:

- терминологический `rg` по устаревшему слитному имени runtime-пакета в `docs`,
  `README.ru.md`, `README.md` и `mkdocs.yml` не нашёл совпадений;
- `git diff --check` завершился без замечаний;
- `uv run --group dev pytest` завершился успешно: `948 passed`;
- `uv run --group docs mkdocs build --strict` завершился с кодом 0; в выводе
  остались только существующие informational сообщения о publisher-страницах вне
  `nav` и предупреждение Material for MkDocs.
