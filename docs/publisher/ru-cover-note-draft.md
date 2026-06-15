# Cover note draft для БХВ

Status: working draft for the first Russian publisher packet. This is not final
email copy until the author fields are filled.

## Назначение

Сопроводительное письмо не должно пересказывать всю книгу. Его задача - открыть
редакторский разговор: кто автор, что за книга, что приложено, что читать
первым и какой технический sample можно запросить дополнительно.

## Default sending scope

- **Primary sample:** Chapter 1 only, `docs/book/part-i/chapter-1.md`.
- **Follow-up technical sample:** Chapter 13, `docs/book/part-v/chapter-13.md`,
  only if the editor asks for deeper material on evals, traces, verifier output,
  regression gates, and release decisions.
- **Working manuscript:** Google Doc `Архитектура безопасных ИИ-агентов`,
  <https://docs.google.com/document/d/1LyY2Psy2yaobn7VLmOwLTWm4QVrhp2I-ylE2B7V4pp4>.
- **Manuscript status:** собраны Введение, части I-VII и приложения; до
  финальной сдачи остаются авторские поля, стилевые файлы БХВ, DOCX/export QA и
  внешняя вычитка.
- **Online companion:** <https://agent-axiom.github.io/agent-arch/>; source
  repository: <https://github.com/agent-axiom/agent-arch>.
- **Packet source:** `docs/publisher/ru-publisher-packet-v0.1.md`.

## Темы письма

Variant A:

> Русская рукопись: "Архитектура безопасных ИИ-агентов"

Variant B:

> Рабочий пакет по книге об архитектуре безопасных ИИ-агентов

Variant C:

> Sample chapter и структура русской книги про production AI agents

## Черновик письма

Здравствуйте, [имя редактора].

Меня зовут [имя автора / публичное имя]. [Короткая авторская строка из блока
"Об авторе": роль, релевантный опыт, публичные проекты.]

Направляю рабочий пакет по русской версии книги "Архитектура безопасных
ИИ-агентов". Книга показывает, как перейти от demo-агентов к production-системам
с явными границами доверия, инструментами, памятью, подтверждениями, трассами,
оценками и поэтапным выпуском.

Репозиторий остается источником правды, а Google Doc используется как
редакционная рукопись для сборки, правки и согласования. Сейчас в нём собраны
Введение, части I-VII и приложения:
<https://docs.google.com/document/d/1LyY2Psy2yaobn7VLmOwLTWm4QVrhp2I-ylE2B7V4pp4>.

Для первого чтения предлагаю главу 1 как основной sample chapter. Она показывает
голос книги, problem-first opening и главную рамку: когда достаточно обычного
workflow, когда нужен одиночный agent loop, а когда оправдана многоагентная
схема.

Глава 13 подготовлена как follow-up technical sample и может быть отправлена
отдельно, если нужно показать техническую глубину по трассам, оценкам,
регрессионным шлюзам и решениям о выпуске.

Длинные схемы, runtime details, source catalog и расширенные чеклисты предлагаю
оставить в online companion, чтобы печатная рукопись сохраняла книжный ритм:
<https://agent-axiom.github.io/agent-arch/>.

С уважением,

[имя автора]

[контакты / публичные ссылки]

## Before sending

- заменить `[имя редактора]`;
- заменить авторскую строку фактическим текстом из блока "Об авторе";
- проверить, что Google Doc доступен редактору;
- не прикладывать Chapter 13 по умолчанию;
- приложить или явно указать publisher packet v0.1;
- убедиться, что письмо не содержит приватных фактов, NDA-деталей и
  неподтвержденных claims.

## После заполнения авторского блока

1. Обновить короткую авторскую строку в этом письме.
2. Синхронизировать такую же строку в Google Doc.
3. Зафиксировать финальный external packet version.
