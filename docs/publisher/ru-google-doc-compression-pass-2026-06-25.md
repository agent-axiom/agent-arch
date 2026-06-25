# Google Doc compression pass, 2026-06-25

## Scope

This pass edits the live Google Doc manuscript:

- Google Doc: https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI
- Title: `Архитектура безопасных ИИ-агентов — полная рукопись`
- Tab: `t.0`
- Final revision after writes: `ALtnJHwfjLMG9gKPoabRSq2_KwaI_Lh_jy4cXwLoZUSMsT51PNH3uuUjGGl9hxo4mCOwCQsbwqNfk_EQczbb_sG69syt0RITKh6xXxaXWQU`

The goal was to move the manuscript further away from a reference dump and closer to an IT-book reading experience. The pass focuses on two dense practical sections:

- chapter 12 practical section: `side_effect_unknown`, idempotency key, retry, reconciliation, rollback boundary;
- trace investigation practical section with listings `15.1`-`15.10`.

## Implemented changes in Google Doc

### Chapter 12 practical section

Replaced the range from:

`12. Практикум: разбор side_effect_unknown, idempotency key и rollback boundary перед production-вызовом`

to before:

`Минимальный checklist перед production-вызовом write-capability`

The previous section contained full YAML-like blocks for ten listings. The replacement keeps all ten listing anchors but turns them into compact printed excerpts:

- `Листинг 12.1`: write intent excerpt;
- `Листинг 12.2`: idempotency contract excerpt;
- `Листинг 12.3`: outcome matrix excerpt;
- `Листинг 12.4`: retry contract excerpt;
- `Листинг 12.5`: rollback boundary excerpt;
- `Листинг 12.6`: reconciliation plan excerpt;
- `Листинг 12.7`: recovery approval excerpt;
- `Листинг 12.8`: durable step excerpt;
- `Листинг 12.9`: trace events excerpt;
- `Листинг 12.10`: eval scenario excerpt.

The new text keeps the logical chain:

write intent -> idempotency key -> outcome classification -> retry policy -> rollback boundary -> reconciliation -> recovery approval -> durable step -> trace evidence -> eval gate.

### Trace investigation practical section

Replaced the range from:

`15. Практикум: расследование агентного запуска по trace`

to before:

`15.11. Контрольный лист ревью trace`

The previous section contained full trace/eval-like field lists. The replacement keeps listing anchors `15.1`-`15.10` but makes each listing a printed excerpt with a short explanation:

- investigation question;
- trace review card;
- event timeline;
- identity invariants;
- policy decision evidence;
- approval review;
- span versus structured event boundary;
- `side_effect_unknown` result;
- `verification_result`;
- regression candidate.

The new text keeps the logical chain:

incident question -> trace identity -> event timeline -> access boundary -> policy decision -> approval link -> span/event split -> side-effect class -> verification -> regression gate.

## Connector readback

Readback checks after Google Docs writes:

- new chapter 12 marker found: `Печатный excerpt: intent_id, trace_id, capability, risk_tier, idempotency_key, requested_fields`;
- new trace marker found: `Печатный excerpt: incident_question, expected_answer_shape, evidence_required`;
- old dense marker absent: `write_intent:`;
- old dense marker absent: `capability_retry_contract:`;
- old dense marker absent: `trace_review:`;
- old dense marker absent: `regression_candidate:`.

## Exported artifacts

- Raw Google Doc export: `docs/publisher/artifacts/agent-arch-ru-compression-pass-2026-06-25.docx`
- Template2000n derivative: `docs/publisher/artifacts/agent-arch-ru-template2000n-compression-pass-2026-06-25.docx`
- Render QA: `docs/publisher/ru-google-doc-compression-pass-2026-06-25.render-qa.json`

## Render QA summary

Raw DOCX render:

- pages: 637;
- blank-like pages: 0;
- edge-risk pages: 0;
- marker pages: `Печатный excerpt: intent_id` page 300, `Печатный excerpt: incident_question` page 324, `Листинг 12.10` page 305, `Листинг 15.10` page 329.

Template2000n render:

- pages: 375;
- blank-like pages: 0;
- edge-risk pages: 0;
- marker pages: `Печатный excerpt: intent_id` page 182, `Листинг 12.10` page 186, `Листинг 15.10` page 202, `15.11. Контрольный лист ревью trace` page 203.

Template-specific repair:

- 20 paragraphs beginning with `Печатный excerpt:` were set to left alignment in the Template2000n derivative to avoid stretched justification around long `snake_case` terms.

## Editorial impact

This pass reduces the manuscript's reference-density in the edited practical sections while preserving all conceptual anchors. The printed text now explains why each artifact exists and sends full runnable/reference material to companion, which is the right split for an IT book:

- book: architectural decision, risk boundary, verification logic;
- companion: full YAML, field catalog, CLI, payload, dataset, command output.

## Remaining author-owned fields

These are still intentionally left for the author:

- `[Имя автора / публичное имя]`;
- `[текущая роль, специализация или независимое позиционирование]`;
- `[Имя автора]`;
- `[основная область: архитектура ИИ-агентов, платформенная инженерия, безопасность, продуктовая разработка, developer tooling — выбрать и уточнить]`;
- `Роль или должность`;
- `Ключевой опыт`;
- `Публичные проекты`;
- `Ссылки`;
- `Формулировка для издательства`;
- final acknowledgements;
- dedication, if any;
- errata channel;
- final companion URL and version tag for the publication snapshot.

## Remaining editorial debt

- Continue the same compression pass across other dense sections, especially runtime reference, eval/export, lifecycle artifacts, source appendix, and incident materials.
- Normalize heading/listing styles in the live Google Doc if the publisher expects the Google Doc itself, not only DOCX/Template derivative, to carry final typography.
- Confirm with the publisher whether listing captions should be italic captions, numbered Word captions, or normal styled paragraphs.
- Keep companion routes stable before final publication package.
