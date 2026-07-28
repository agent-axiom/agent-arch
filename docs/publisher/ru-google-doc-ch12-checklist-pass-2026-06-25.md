# Google Doc chapter 12 checklist pass

Дата: 2026-06-25

Google Doc: https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI

Цель прохода: выполнить следующий 5-пунктовый editorial pass в рабочем Google Doc, усилить выход главы 12 к observability/trace, проверить listing route 12.1-12.10 и подготовить свежие DOCX-артефакты для издательского цикла.

## Пункт 1. Сжатие production checklist

В Google Doc заменен разросшийся хвост главы 12 в диапазоне перед реальным началом главы 13.

Новый блок начинается с:

- `Минимальный checklist перед production-вызовом write-capability`;
- `Проверь пять решений.`

Checklist теперь работает как production gate, а не как повтор практикума. Он фокусируется на пяти решениях:

1. идентичность записи;
2. класс исхода;
3. бюджет повтора;
4. граница отката;
5. сверка и доказательства.

## Пункт 2. Выход к observability и trace

Добавлен явный выход из главы:

`Выход из главы: idempotency и reconciliation не заканчиваются на runtime-логике.`

Смысловая связка стала такой:

- write intent и idempotency key задают контролируемое действие;
- `side_effect_unknown` блокирует слепой retry;
- reconciliation фиксирует evidence;
- trace в следующей главе должен показать intent, policy decision, approval, tool outcome, reconciliation attempt и verification result.

## Пункт 3. Терминологическая нормализация

Вставлено терминологическое правило главы:

- `retryable_failure` - сбой до необратимого эффекта, который можно повторить по политике;
- `side_effect_unknown` - неизвестность после потенциального эффекта, которая требует reconciliation;
- `rollback boundary` - граница, после которой автоматический откат невозможен или небезопасен;
- `reconciliation` - проектируемая ветка чтения внешнего состояния и фиксации доказательств.

Дополнительно исправлены две редакционные шероховатости:

- `later trace review` -> `последующее trace review`;
- `полный YAML belongs to companion` -> `полный YAML должен уходить в companion`.

## Пункт 4. Порядок листингов 12.1-12.10

Readback-проверка Google Doc подтвердила, что listing anchors идут в правильном порядке:

| Anchor | Index |
| --- | ---: |
| `Листинг 12.1 —` | 384591 |
| `Листинг 12.2` | 385368 |
| `Листинг 12.3` | 386180 |
| `Листинг 12.4` | 386976 |
| `Листинг 12.5` | 387769 |
| `Листинг 12.6` | 388604 |
| `Листинг 12.7` | 389342 |
| `Листинг 12.8` | 389914 |
| `Листинг 12.9` | 390490 |
| `Листинг 12.10` | 391190 |

После listing route идет новый checklist, затем companion route и глава 13.

## Пункт 5. Companion route

Добавлен явный route:

`Companion route для главы 12: полные YAML-контракты ... должны храниться в online companion.`

В печатной книге остается decision path и короткие excerpts. В companion должны уйти полные поля, CLI-проверки, payload examples и validation messages.

## Export and render QA

Созданы свежие DOCX-артефакты:

- raw Google Docs export: `docs/publisher/artifacts/agent-arch-ru-ch12-checklist-pass-2026-06-25.docx`;
- Template2000n derivative: `docs/publisher/artifacts/agent-arch-ru-template2000n-ch12-checklist-pass-2026-06-25.docx`.

Raw export:

- page count: 633;
- blank-like pages: 0;
- zero-byte PNG pages: 0;
- targeted visual QA pages: 306-309;
- marker pages: `Проверь пять решений` page 306, `Терминологическое правило главы` page 308, `Companion route для главы 12` page 309, body `Глава 13` page 309.

Template2000n derivative:

- page count: 378;
- blank-like pages: 0;
- zero-byte PNG pages: 0;
- targeted visual QA pages: 188-190;
- marker pages: `Проверь пять решений` page 188, `Терминологическое правило главы` page 189, `Companion route для главы 12` page 189, body `Глава 13` page 190.

Template2000n derivative был дополнительно поправлен на уровне OOXML: новые длинные абзацы главы 12 получили left alignment, чтобы избежать растянутых пробелов вокруг технических терминов.

## Что остается заполнить автору

Перед редакторской сдачей автор должен самостоятельно заполнить или подтвердить:

- `[Имя автора / публичное имя]`;
- `[текущая роль, специализация или независимое позиционирование]`;
- `[Имя автора]`;
- `[основная область: архитектура ИИ-агентов, платформенная инженерия, безопасность, продуктовая разработка, developer tooling]`;
- `Роль или должность`;
- `Ключевой опыт`;
- `Публичные проекты`;
- `Ссылки`;
- `Формулировка для издательства`;
- благодарности и dedication, если они нужны;
- публичный URL online companion;
- errata/contact channel;
- версию companion, соответствующую редакции книги.

## Следующий editorial focus

Следующие 100 итераций должны сместить фокус с локальной правки главы 12 на подготовку рукописи к сильной редакторской сдаче: глава 13, главы observability/eval/rollout, consistency pass, source/companion routing, author-owned front matter и final proof cycle.
