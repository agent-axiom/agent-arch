# 100 applied editorial iterations for редакционная подготовка

Дата прохода: 2026-06-23.

Назначение: продолжить backlog 1-100 и 101-200 после первого applied pass в Google Doc. Эти итерации 201-300 ориентированы на практическое доведение рукописи до сильного редакционного варианта: главы 6-20, приложения, companion, proof QA, авторские поля и издательский handoff.

Исходная точка:

- Google Doc source: `https://docs.google.com/document/d/1LJHcIIpggUwaFYRXvSZ91KyNzb2kyxCsESVRAHMWlxI`;
- fresh Google Docs export after applied edits: 654 страниц, включая одну trailing blank-like page;
- Template2000n-applied derivative: 419 страниц, blank-like pages: 0;
- предыдущие backlog:
  - `docs/publisher/ru-editorial-100-iteration-plan-2026-06-23.md`;
  - `docs/publisher/ru-editorial-100-next-iterations-2026-06-23.md`;
- этот backlog: дополнительные итерации 201-300.

## Итерации 201-300

| # | Цель итерации | Критерий готовности | Следующий action |
| ---: | --- | --- | --- |
| 201 | Проверить chapter focus pattern после вставок 1-5 | Все пять блоков читаются как lead, а не как редакционные комментарии | Повторить паттерн для 6-10 |
| 202 | Пройти главу 6 на центральный тезис | Первый экран главы объясняет, зачем нужен tool gateway | Добавить или усилить lead |
| 203 | Пройти главу 7 на связь MCP/A2A с boundary model | Интеграционные протоколы не выглядят как мода | Уточнить практический контекст |
| 204 | Пройти главу 8 на human review responsibility | Human review описан как решение и ответственность | Добавить owner-oriented framing |
| 205 | Пройти главу 9 на policy/runtime distinction | Prompt policy и runtime policy не смешиваются | Уточнить терминологию |
| 206 | Пройти главу 10 на verifier narrative | Verifier показывает evidence и stop condition | Сократить лишние payload |
| 207 | Добавить focus blocks 6-10 | У каждой главы есть короткий практический фокус | Сделать readback |
| 208 | Проверить переход 5 -> 6 | Identity/policy логично ведут к tool gateway | Добавить мост, если нужен |
| 209 | Проверить переход 10 -> 11 | Verifier/evals логично ведут к sandbox/MCP | Добавить мост, если нужен |
| 210 | Проверить part-level introduction перед эксплуатационным блоком | Читатель понимает смену масштаба с design на operation | Добавить intro |
| 211 | Пройти главу 11 на sandbox boundary | Sandbox не выглядит только инфраструктурной деталью | Связать с risk containment |
| 212 | Пройти главу 12 на idempotency/rollback | Повторы и откаты связаны с side effects | Добавить practical gate |
| 213 | Пройти главу 13 на trace/event clarity | Trace, span, event разведены | Добавить словарный блок |
| 214 | Пройти главу 14 на SLO realism | SLO не обещают невозможной стабильности | Уточнить caveats |
| 215 | Пройти главу 15 на eval gates | Offline/online evals связаны с release decisions | Добавить release gate language |
| 216 | Пройти главу 16 на evidence chain | Запрос -> trace -> eval -> rollout читается как цепочка | Добавить diagram candidate |
| 217 | Добавить focus blocks 11-16 | У каждой главы есть practical focus | Сделать readback |
| 218 | Проверить переход 11 -> 16 | Эксплуатационные главы идут от runtime к evidence | Сжать повторы |
| 219 | Проверить повтор термина `evidence` | Термин используется единообразно | Терминологический sweep |
| 220 | Проверить trace examples | Длинные event catalogs не перегружают печать | Вынести полные catalogs |
| 221 | Пройти главу 17 на platform team model | Роли platform/product/security разведены | Добавить responsibility map |
| 222 | Пройти главу 18 на golden paths | Golden paths не превращаются в rigid bureaucracy | Уточнить anti-zoo framing |
| 223 | Пройти главу 19 на ADLC | ADLC объяснен до активного использования | Добавить early definition if needed |
| 224 | Пройти главу 20 на assurance loop | Assurance, incidents, registry, retirement объединены | Сжать дубли |
| 225 | Добавить focus blocks 17-20 | У финальных глав есть практический фокус | Сделать readback |
| 226 | Проверить финальную дугу книги | Книга идет от platform boundary к lifecycle responsibility | Составить one-page arc |
| 227 | Проверить conclusion | Заключение не пересказывает оглавление | Усилить центральную мысль |
| 228 | Проверить recurring scenarios | Сквозные сценарии возвращаются в нужных главах | Составить scenario map |
| 229 | Проверить workshop usability | Главы дают материал для командного ревью | Добавить review prompts |
| 230 | Проверить role-based usability | Архитектор, security, platform, product видят свои действия | Добавить role notes |
| 231 | Пройти Appendix 1 capability contract | Поля контракта применимы без объяснений автора | Уточнить labels |
| 232 | Пройти Appendix 2 readiness review | Checklist проверяет release readiness, а не общее желание | Нормализовать вопросы |
| 233 | Пройти Appendix 3 incident/postmortem | Incident template связан с trace/evidence/owner | Уточнить caveats |
| 234 | Пройти Appendix 4 companion | Appendix остается навигацией, не source dump | Сократить лишние paths |
| 235 | Проверить route labels в companion appendix | Routes человекочитаемы и стабильны | Обновить labels |
| 236 | Проверить public links | В приложении активны только стабильные публичные ссылки | Повторить hyperlink audit |
| 237 | Проверить internal repo paths | В теле книги не осталось длинных blob URLs | `find_text_range` по raw URLs |
| 238 | Проверить source attribution | Фактические утверждения имеют source route | Source appendix pass |
| 239 | Проверить fast-changing facts | Современные API/product statements не устарели | Browse official docs before submission |
| 240 | Проверить legal caveats | Книга не обещает compliance/legal guarantee | Add caveat where needed |
| 241 | Listing sweep для глав 1-5 | Каждый listing имеет purpose before/after | Перенести лишнее в companion |
| 242 | Listing sweep для глав 6-10 | Длинные YAML/CLI сокращены | Перенести в companion |
| 243 | Listing sweep для глав 11-16 | Trace/event examples показывают evidence | Сократить payload |
| 244 | Listing sweep для глав 17-20 | Lifecycle artifacts не перегружают финал | Сжать или вынести |
| 245 | Listing sweep для приложений | Приложения содержат шаблоны, а не сырой dump | Оставить usable artifacts |
| 246 | Проверить code block style in Template2000n | Code-like blocks читаются в proof | Render spot pages |
| 247 | Проверить inline code terms | Inline code не ломает русскую пунктуацию | Typography pass |
| 248 | Проверить YAML terminology | Поля YAML не конфликтуют с текстовыми терминами | Терминологический pass |
| 249 | Проверить CLI reproducibility | Команды не обещают запуск без context | Add companion route |
| 250 | Проверить datasets/evals references | Dataset details не в печатном потоке | Move to companion |
| 251 | Проверить glossary need | Терминологического соглашения достаточно или нужен глоссарий | Decide after editor |
| 252 | Создать терминологический sweep list | capability, verifier, trace, rollout, incident, retirement | Пройти по всему тексту |
| 253 | Развести verifier/validator/evaluator | Термины не используются как взаимозаменяемые | Исправить в главах |
| 254 | Развести policy gateway/tool gateway | Gateway terms имеют разные границы | Исправить в главах |
| 255 | Развести memory/retrieval/provenance | Memory governance не смешивается с retrieval | Исправить в главах |
| 256 | Развести rollout/release/deployment | Release gates и rollout waves не смешиваются | Исправить в главах |
| 257 | Развести incident/postmortem/learning loop | Incident response и learning не одно и то же | Исправить в главах |
| 258 | Проверить ADLC definition | ADLC определен до системного использования | Добавить early definition |
| 259 | Проверить русском-английский баланс | Английские термины являются architecture names | Убрать случайные англицизмы |
| 260 | Проверить consistency of `online companion` | Везде один термин и URL policy | Normalize wording |
| 261 | Proof QA fresh Google Docs export | Raw export page count and blank page tracked | Устранить trailing blank |
| 262 | Proof QA Template2000n derivative | Page count, blank pages, edge risks tracked | Повторить после следующего batch |
| 263 | Проверить title style box | Publisher confirms or rejects boxed title style | Ask publisher |
| 264 | Проверить first-page density | Аннотация помещается без служебного шума | Visual check |
| 265 | Проверить author page | Placeholder block не уйдет случайно в финал | Author fill gate |
| 266 | Проверить chapter focus formatting | Focus paragraphs не выглядят как comments | Style check |
| 267 | Проверить low-ink pages | Low-ink pages are intentional tails, not broken pages | Spot check |
| 268 | Проверить page breaks before appendices | Appendices start cleanly | Render spot check |
| 269 | Проверить final page | Финальная страница не пустая в Template2000n proof | Render spot check |
| 270 | Проверить exported DOCX metadata | Title, language, author placeholder policy | Metadata pass |
| 271 | Author fill: public name | Имя заполнено в short/extended bio | Автор |
| 272 | Author fill: role | Роль/позиционирование заполнены | Автор |
| 273 | Author fill: key experience | 1-2 проверяемые фразы | Автор |
| 274 | Author fill: public projects | Только публично безопасные проекты | Автор |
| 275 | Author fill: links | GitHub/site/blog/profile/companion | Автор |
| 276 | Author fill: publisher bio | Короткая формулировка для издательства | Автор + редактор |
| 277 | Author decision: acknowledgments | Текст или явный отказ | Автор |
| 278 | Author decision: dedication | Текст или явный отказ | Автор |
| 279 | Author decision: errata route | Email/site/repo issues selected | Автор |
| 280 | Author decision: companion version | Versioning policy confirmed | Автор |
| 281 | Editor handoff: cover note | Статус и ограничения вынесены из тела книги | Update packet |
| 282 | Editor handoff: artifact list | Google Doc, DOCX proofs, reports listed | Update packet |
| 283 | Editor handoff: known risks | Blank page, title style, author fields listed | Update packet |
| 284 | Editor handoff: requested review | Что именно просим у редактора | Update packet |
| 285 | Editor handoff: style note | Русско-английский терминологический принцип описан | Update packet |
| 286 | Editor handoff: link policy | Active links and companion routes described | Update packet |
| 287 | Editor handoff: proof scope | Render QA versus human proofread separated | Update packet |
| 288 | Editor handoff: legal caveat | Книга не compliance/legal advice | Update packet |
| 289 | Editor handoff: companion ownership | Owner/changelog/errata policy described | Update packet |
| 290 | Editor handoff: next proof cycle | Fresh export + Template2000n + render QA planned | Update packet |
| 291 | Regression check: service lines | Служебные строки не вернулись в body | find text |
| 292 | Regression check: long URLs | Long GitHub blob/tree URLs absent from body | find text |
| 293 | Regression check: focus blocks | Expected focus blocks are present | find text |
| 294 | Regression check: listing rule | Listing rule present in front matter | find text |
| 295 | Regression check: raw export pages | Page count recorded after next export | Render QA |
| 296 | Regression check: Template2000n pages | Page count recorded after next derivative | Render QA |
| 297 | Repository sync | Reports, metrics, artifacts committed | git status |
| 298 | CI/docs checks | `pytest` and `mkdocs build --strict` pass | Verification |
| 299 | Push branch | Remote branch contains applied pass | git push |
| 300 | Final author report | Автор видит result, page counts, must-fill fields | Send report |

## Итог по итерациям 201-300

Эти 100 итераций переводят работу из состояния "собраны отчеты" в состояние "есть applied changes в Google Doc и повторяемый proof cycle". Главная линия следующего этапа: расширить applied content pass на главы 6-20, провести listing/companion sweep и закрыть author-owned поля до внешней редакторской сдачи.
