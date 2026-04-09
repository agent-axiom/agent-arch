# Memory eval patterns для agent systems

Память в agent systems ломается не так, как обычный retrieval. Ошибки здесь часто проявляются не в одном запросе, а через серию runs, обновлений профиля и фоновых записей.

Поэтому memory layer полезно оценивать отдельно, а не надеяться, что он “как-нибудь попадет” в общий eval dataset.

## 1. Почему memory evals нужны отдельно

Даже если overall task success выглядит хорошо, memory design может деградировать по-тихому:

- профиль заполняется лишними или рискованными фактами;
- stale preference продолжает влиять на ответы;
- system remembers the wrong thing;
- нужный факт не извлекается в длинной сессии;
- background compaction искажает смысл записи.

Именно поэтому memory layer требует своего evaluation logic.

## 2. Какие типы ошибок стоит ловить

Минимальный memory eval set обычно должен покрывать:

- incorrect write;
- missing write;
- unsafe write;
- stale retrieval;
- false retrieval;
- profile contradiction;
- over-retention;
- deletion failure.

Этот набор уже полезен даже без сложного benchmark.

## 3. Что оценивать в краткосрочной памяти

Short-term memory чаще всего проверяют на:

- удержание критичного контекста в пределах диалога;
- отсутствие лишнего переноса в следующий turn;
- устойчивость к noisy user turns;
- корректность переспрашивания при неоднозначности.

Здесь проблема обычно не в storage itself, а в том, как runtime решает, что именно worth carrying forward.

## 4. Что оценивать в профильной и долгосрочной памяти

Profile memory и long-term memory требуют более строгих checks:

- был ли факт вообще достоин записи;
- был ли факт записан в правильный memory class;
- можно ли объяснить provenance;
- можно ли безопасно удалить или обновить запись;
- не влияет ли stale record на текущий answer path.

Здесь особенно важны evals на contradiction и retention hygiene.

## 5. Long-horizon memory нужно проверять на сериях runs

Один из самых частых промахов такой: memory quality проверяют на одном isolated prompt.

Но реальные проблемы обычно проявляются на сериях:

- preference записали в run 1;
- неверно извлекли в run 4;
- обновили конфликтующим фактом в run 6;
- stale profile продолжил влиять в run 9.

Поэтому полезно строить memory evals как multi-run scenarios, а не только как single-turn checks.

## 6. Какие поля полезно фиксировать в memory eval case

Минимально полезный eval record часто включает:

- `memory_class`
- `write_expected`
- `retrieval_expected`
- `allowed_to_persist`
- `expected_provenance`
- `revision_behavior`
- `deletion_behavior`

Это помогает отделять “ответ плохой” от “memory semantics нарушены”.

## 7. Что особенно важно для safety

Memory evals полезны не только для personalization. Они важны и для safety:

- не пишет ли система sensitive data без права;
- не удерживает ли слишком долго risky state;
- не путает ли user-specific data;
- можно ли быстро прекратить harmful memory path;
- можно ли доказать provenance у persistent records.

Если этого слоя нет, memory incidents будут выглядеть как “странное поведение модели”, хотя проблема уже в lifecycle записи.

## 8. Как memory evals связаны с обычным eval loop

Memory evals не живут отдельно от [главы про evals](../book/part-v/chapter-13.md). Они просто добавляют отдельную плоскость:

- обычные offline evals проверяют task success;
- memory evals проверяют state quality across runs;
- online signals помогают ловить drift;
- incidents и postmortems обновляют memory-specific cases.

То есть memory layer должен входить в regression discipline так же явно, как tools или policy.

## 9. Практический чеклист

- Есть ли отдельные cases на write / no-write decisions?
- Проверяется ли retrieval на длинных сериях runs?
- Есть ли cases на stale profile и contradiction?
- Оценивается ли provenance у persistent records?
- Есть ли deletion и revision cases?
- Возвращаются ли memory incidents в eval dataset?

## См. также

- [Схема наборов для оценки и правил проверки](eval-schema.md)
- [Схема записей памяти и контракта извлечения](memory-retrieval-schema.md)
- [Глава 5. Зачем агенту память и почему она опасна](../book/part-iii/chapter-5.md)
- [Глава 7. Извлечение контекста, уплотнение и фоновые обновления](../book/part-iii/chapter-7.md)
- [Глава 13. Офлайн-оценки, онлайн-оценки и регрессионные шлюзы](../book/part-v/chapter-13.md)
