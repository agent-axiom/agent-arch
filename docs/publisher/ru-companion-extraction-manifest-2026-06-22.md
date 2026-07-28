# Companion Extraction Manifest

Дата: 2026-06-22

Google Doc: <https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>

Цель: зафиксировать первый физический вынос справочных материалов из печатной рукописи в online companion.

## Первый диапазон выноса

Раздел: хвостовая reference-package область эталонной среды выполнения.

Начальный якорь в Google Doc:

- `Примерные конфиги`

Финальный якорь:

- `Буквальные маркеры среды выполнения также включают evalgate`

Тип материала:

- config list;
- CLI check commands;
- runtime reference package notes;
- sandbox profile surface;
- durable runner pattern;
- process spine pattern;
- inspection command catalogue;
- next-schema backlog;
- literal runtime markers.

Почему выносится:

- материал полезен как companion-справочник;
- в печатной книге он разрывает аргумент и превращает финальные страницы в changelog/reference dump;
- детали команд, YAML, config filenames и future-pattern backlog должны быть версионируемыми рядом с репозиторием.

Что остаётся в печатной книге:

- краткое объяснение роли эталонного пакета;
- принцип разделения книги и companion;
- список типов companion-артефактов;
- критерии чтения: книга отвечает на "зачем и где границы", companion отвечает на "как запустить и проверить".

## Кандидаты следующих проходов

1. Глава 23: длинные launch/readiness fragments, если они повторяют companion contract.
2. Приложения: YAML/schema catalogs и длинные event lists.
3. Главы 11-15: CLI-output, validation catalogs, exporter commands и dataset details.
4. Front matter: заменить plain numbered paragraphs на native numbered list перед DOCX style pass.
5. Appendix backlog: разбить companion backlog на versioned files в репозитории.

## Предлагаемые companion артефакты

- `companion/runtime-reference/configs.md`
- `companion/runtime-reference/cli.md`
- `companion/runtime-reference/eval-datasets.md`
- `companion/runtime-reference/traces-and-events.md`
- `companion/runtime-reference/sandbox-profile.md`
- `companion/runtime-reference/durable-runner.md`
- `companion/runtime-reference/process-spine.md`
