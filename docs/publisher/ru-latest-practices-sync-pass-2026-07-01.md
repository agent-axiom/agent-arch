# Latest practices sync pass

Date: 2026-07-01.

Status: synced to local full manuscript and Google Doc working manuscript.

Target Google Doc:
<https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI>

## Baseline

The repository source of truth in `docs/book/**` contained 13 late practical
sections that were not fully represented in the publisher manuscript layer.

Control result before this pass:

- `docs/book/**`: 13/13 control practice headings present;
- `docs/publisher/ru-manuscript-full.md`: 0/13 control practice headings
  present;
- Google Doc manuscript export: 5/13 control practice headings present;
- missing Google Doc practice headings: 8/13, concentrated in trace/SLO/eval,
  ownership/golden-path and final runtime/launch chapters.

## Local manuscript sync

`docs/publisher/ru-manuscript-full.md` was updated from `docs/book/**`.

Inserted source sections:

1. `docs/book/part-iii/chapter-5.md` -
   `Практикум: модель памяти, которую можно проверить`.
2. `docs/book/part-iii/chapter-7.md` -
   `Практикум: проверяемая сборка контекста`.
3. `docs/book/part-iv/chapter-8.md` -
   `Практикум: ревью capability contract перед выдачей инструмента модели`.
4. `docs/book/part-iv/chapter-9.md` -
   `Практикум: ревью sandbox profile и MCP boundary перед подключением capability`.
5. `docs/book/part-iv/chapter-10.md` -
   `Практикум: разбор side_effect_unknown, idempotency key и rollback boundary перед production-вызовом`.
6. `docs/book/part-v/chapter-11.md` -
   `Практикум: расследование агентного запуска по trace`.
7. `docs/book/part-v/chapter-12.md` -
   `Практикум: собрать SLO-карту для одного агентного пути`.
8. `docs/book/part-v/chapter-13.md` -
   `Практикум: превратить trace review в regression gate`.
9. `docs/book/part-vi/chapter-14.md` -
   `Практикум: назначить владельцев для trace -> SLO -> eval -> rollout`.
10. `docs/book/part-vi/chapter-15.md` -
    `Практикум: минимальный золотой путь для пишущего агента`.
11. `docs/book/part-vii/chapter-16.md` -
    `Практикум: собрать rollout-ready runtime skeleton из golden path`.
12. `docs/book/part-vii/chapter-17.md` -
    `Практикум: связать capability contract с SLO, eval gate и golden path`.
13. `docs/book/part-vii/chapter-18.md` -
    `Практикум: пройти цепочку trace -> eval gate -> rollout wave -> containment`.

Verification after local sync:

- all 13 control headings are present exactly once in
  `docs/publisher/ru-manuscript-full.md`;
- inserted source volume: 2360 lines;
- source heading levels were demoted one level to match the publisher
  manuscript hierarchy.

## Google Doc sync

The Google Doc already contained the first five practice sections. This pass
added eight missing late practice blocks in print-oriented form:

1. `Практикум: расследование агентного запуска по trace`;
2. `Практикум: собрать SLO-карту для одного агентного пути`;
3. `Практикум: превратить trace review в regression gate`;
4. `Практикум: назначить владельцев для trace -> SLO -> eval -> rollout`;
5. `Практикум: минимальный golden path для пишущего агента`;
6. `Практикум: собрать rollout-ready runtime skeleton из golden path`;
7. `Практикум: связать capability contract с SLO, eval gate и golden path`;
8. `Практикум: пройти цепочку trace -> eval gate -> rollout wave -> containment`.

Google Docs write path:

- pre-update revision:
  `ALtnJHwQSbMVcXf5UUw3QyuuxPZVGdtR-7yOKUdJM8DtE76ktgR6WhHDA0zngCtIQFMNxPaYHMglaPHowPxYQS8TpcL8wryth-RYjYpT_iQ`;
- first guarded `batchUpdate`: 6/8 replacements changed one occurrence each;
- second guarded `batchUpdate`: 2/2 fallback replacements changed one
  occurrence each;
- final revision:
  `ALtnJHw6WxhO001-I6mNISWhNzNDr7n5YMGTbGYCJgQC70hOmSth96E7ZqoA-Nu2VFfUElLa8JnWk-QcpYhyoU-Zzgu3EUIDi3iKWys1_D4`.

Readback:

- fresh plain-text export size: 1,266,284 bytes;
- approximate text volume: 766,889 characters and 101,584 words;
- each of the eight newly added Google Doc practice headings appears exactly
  once in the readback export.

## Editorial decision

The local Markdown manuscript now carries the full source practice content from
`docs/book/**`. The Google Doc carries publisher-readable practice blocks for
the eight late gaps, avoiding raw long YAML/payload expansion in the live
editorial document while preserving the practical meaning needed for editor
review.

This is a manuscript-content sync pass, not a final publisher export pass.

Still open before final publisher-ready DOCX:

- author-owned fields: byline, role, public bio, checked experience, public
  links, companion URL/version, acknowledgements, legal/compliance disclaimer
  and AI-use disclosure;
- final external proofread;
- publisher style application;
- fresh DOCX export and render QA after author fields and style application.

