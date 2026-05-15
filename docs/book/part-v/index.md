# Часть V. Надежность и наблюдаемость

К этому моменту у нас уже есть архитектура, security perimeter, память и execution layer. Теперь вопрос меняется: как управлять системой после запуска, когда она уже может ошибаться в живой эксплуатации, дорожать, дрейфовать и ломаться не только в happy path.

Эта часть отвечает на три очень практических вопроса:

- как восстановить реальный путь одного run;
- как определить, что считать здоровьем и допустимым риском системы;
- как превратить поведение системы в judgments, которыми можно пользоваться в rollout.

!!! info "Короткий маршрут по этой части"
    Если нужен быстрый проход, иди так:

    - [Глава 11](chapter-11.md): восстановить сырую историю одного реального сбоя;
    - [Глава 12](chapter-12.md): задать health и risk budgets;
    - [Глава 13](chapter-13.md): превратить поведение системы в reviewable judgments;
    - [Evidence Spine](evidence-spine.md): увидеть, как эти слои собираются в одну эксплуатационную запись.

!!! note "Part V canonical case routes"
    В reliability/observability layer три canonical cases требуют разных evidence routes. **Support triage** проверяет trace coverage для ticket writes, duplicate-ticket regression и approval-path evidence. **Internal knowledge assistant** проверяет retrieval quality, source-grounding judgment, freshness budget и memory-provenance evidence. **Incident coordination** проверяет escalation latency, notification delivery, response ownership и post-incident rollout judgment.

<div class="book-cover" markdown="1">

![Обложка части про надежность и наблюдаемость](../../assets/images/part-v.png)

</div>

## Что решает эта часть

- после главы 11 ты должен уметь восстанавливать путь run, а не гадать по симптомам;
- после главы 12 ты должен уметь формулировать health и risk budgets через latency, cost, safety и escalation;
- после главы 13 ты должен уметь выносить reviewable judgments по quality и regression risk;
- после Evidence Spine ты должен видеть, как traces, policy, approvals, evals и rollout связываются в одну проверяемую цепочку.

## В этой части

- [Глава 11. Трассы, спаны и структурированные события](chapter-11.md)
- [Глава 12. SLO для агентных систем](chapter-12.md)
- [Глава 13. Офлайн-оценки, онлайн-оценки и регрессионные шлюзы](chapter-13.md)
- [Сквозная цепочка доказательств: от запроса к решению о rollout](evidence-spine.md)

## Куда она ведет дальше

Как только система уже умеет захватывать поведение, задавать budgets и выносить judgments, следующим вопросом становится ownership. Поэтому после этой части естественно идти в [Часть VI](../part-vi/index.md): кто владеет этими обещаниями внутри реальной организации.
