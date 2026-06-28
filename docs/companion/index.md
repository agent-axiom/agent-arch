# Online companion

Online companion хранит материалы, которые должны быть версионируемыми, проверяемыми и обновляемыми отдельно от печатной рукописи.

В книге остаются аргумент, критерии решений и минимальные формы контрактов. Здесь остаются полные CLI-проходы, runtime configs, trace/event catalogs, eval datasets, источники и справочные walkthrough.

## Основные маршруты

- [Runtime configs and MCP boundary](runtime-reference/configs.md)
- [Runtime CLI](runtime-reference/cli.md)
- [Eval datasets](runtime-reference/eval-datasets.md)
- [Traces and events](runtime-reference/traces-and-events.md)
- [Templates](templates/index.md)
- [Checklists](checklists/index.md)
- [Changelog](changelog.md)
- [Errata](errata.md)
- Example artifacts:
  `artifacts/trace-demo.jsonl`,
  `artifacts/trace-failed-tool-timeout.jsonl`,
  `artifacts/session-failed-tool-timeout.json`,
  `artifacts/eval-failed-run-timeout.json`
- [Полный reference package walkthrough](../appendix/reference-package.md)
- [Полный список источников](../appendix/sources.md)

## Что должно жить здесь

- Полные YAML-конфиги и review forms.
- CLI-команды и ожидаемые JSON-поверхности.
- Trace/event catalogs и validation-message catalogs.
- Eval datasets, verifier contracts и rollout judgment examples.
- Длинные source catalogs, changelog, errata и правила обновления.

## Что должно оставаться в книге

- Почему архитектурное решение нужно.
- Какой риск оно закрывает.
- Кто владеет действием и доказательствами.
- Как команда понимает, что runtime, policy, trace, eval gate и rollout готовы.
