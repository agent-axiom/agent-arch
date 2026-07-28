# 100 editorial goals after chapter 22 policy/catalog pass - 2026-06-28

Назначение файла: зафиксировать следующие 100 редакционных целей для доведения рукописи до сильного варианта для редакции. Нумерация продолжает текущую серию проходов: `1601-1700`.

## Цели 1601-1700

| Iteration | Goal |
| --- | --- |
| 1601 | Проверить, нужно ли следующий блок оставить как `Практикум` или переименовать в явную главу 23. |
| 1602 | Переписать opening практикума trace -> eval gate -> rollout wave -> containment как продолжение главы 22. |
| 1603 | Убрать из практикума справочные YAML-фрагменты, которые должны жить в companion. |
| 1604 | Добавить в практикум один связный scenario walkthrough от policy decision до rollout gate. |
| 1605 | Явно связать trace evidence с eval gate and release decision. |
| 1606 | Развести hold, freeze and rollback как разные production decisions. |
| 1607 | Добавить checklist промышленного запуска для одного rollout wave. |
| 1608 | Добавить anti-patterns для release checklist без evidence. |
| 1609 | Проверить, что practical block не повторяет главы 19-22. |
| 1610 | Подготовить render QA после переработки practical block. |
| 1611 | Пересмотреть главу 23/следующий блок на наличие устаревших ссылок на schema catalogs. |
| 1612 | Добавить route в companion для rollout gate examples. |
| 1613 | Проверить terminology consistency: `rollout gate`, `eval gate`, `containment`, `incident freeze`. |
| 1614 | Сократить длинные validation-message lists в следующем блоке. |
| 1615 | Усилить пример `side_effect_unknown` в rollout context. |
| 1616 | Добавить short operator view: что видит release owner перед решением. |
| 1617 | Добавить security view: что проверяет security перед расширением rollout. |
| 1618 | Добавить product view: что означает denied/hold для пользователя. |
| 1619 | Проверить, нет ли повторов с readiness checklist главы 22. |
| 1620 | Зафиксировать итоговый report для practical block. |
| 1621 | Вернуться к главе 1 и проверить, соответствует ли promise книги текущей полной рукописи. |
| 1622 | Усилить вводный словарь: capability, policy, verifier, trace, rollout. |
| 1623 | Проверить, что первая часть не обещает framework instead of architecture. |
| 1624 | Добавить ранний пример управляемого действия, который потом раскрывается в главах 21-22. |
| 1625 | Убрать маркетинговые формулировки из начала книги. |
| 1626 | Проверить, что читатель понимает аудиторию книги до первой технической главы. |
| 1627 | Добавить короткую карту чтения для architect, tech lead, security and product owner. |
| 1628 | Сверить front matter with current companion route. |
| 1629 | Перепроверить author TODO block and placeholders. |
| 1630 | Сделать mini report по front matter consistency. |
| 1631 | Пересмотреть главу 2 на связь с policy/catalog vocabulary. |
| 1632 | Уточнить границу между агентом, workflow and automation. |
| 1633 | Добавить пример, где обычный скрипт безопаснее агента. |
| 1634 | Добавить пример, где агент оправдан из-за контекстного выбора. |
| 1635 | Убрать повторяющиеся определения autonomy. |
| 1636 | Проверить, что главы 1-3 не слишком абстрактны. |
| 1637 | Добавить practical checkpoint after chapter 3. |
| 1638 | Сверить термин `agentic system` во всей ранней части. |
| 1639 | Проверить headings hierarchy in early chapters. |
| 1640 | Подготовить report по части I. |
| 1641 | Пересмотреть главы про security boundary and prompt injection. |
| 1642 | Добавить связь prompt injection with tool gateway and policy gateway. |
| 1643 | Проверить, что data exfiltration examples do not look like instructions. |
| 1644 | Уточнить responsible red-team framing. |
| 1645 | Вынести чрезмерные attack payload details в companion. |
| 1646 | Добавить defensive checklist for retrieval and memory poisoning. |
| 1647 | Сверить claims with primary sources where needed. |
| 1648 | Уточнить legal/compliance disclaimers around security chapters. |
| 1649 | Проверить consistency with OWASP/NIST terminology in sources appendix. |
| 1650 | Подготовить report по security part. |
| 1651 | Пересмотреть главы про tools/MCP/A2A and external integrations. |
| 1652 | Добавить distinction: tool API vs capability contract. |
| 1653 | Убрать повтор примеров из главы 22, оставить cross-reference. |
| 1654 | Проверить, что MCP examples are stable and not vendor-transient. |
| 1655 | Перенести long endpoint lists в companion. |
| 1656 | Добавить tool gateway failure modes. |
| 1657 | Добавить egress policy example without full schema dump. |
| 1658 | Проверить style of code/listing captions. |
| 1659 | Сверить appendix references for tools chapters. |
| 1660 | Подготовить report по integration part. |
| 1661 | Пересмотреть memory and retrieval chapters. |
| 1662 | Связать memory persistence with policy checkpoint from chapter 22. |
| 1663 | Добавить example of memory quarantine. |
| 1664 | Проверить, что memory examples do not overpromise reliability. |
| 1665 | Уточнить relationship between retrieval metadata and data scope. |
| 1666 | Добавить checklist for retrieval source ownership. |
| 1667 | Перенести long trace payloads from memory chapters to companion. |
| 1668 | Проверить glossary terms around memory. |
| 1669 | Добавить note about retention and deletion responsibilities. |
| 1670 | Подготовить report по memory/retrieval part. |
| 1671 | Пересмотреть observability chapters for evidence spine consistency. |
| 1672 | Убедиться, что trace contains policy decision, verifier result and tool outcome. |
| 1673 | Добавить example of investigation using chapter 22 decision object. |
| 1674 | Сократить duplicate telemetry metrics. |
| 1675 | Добавить dashboard view for owners and operations. |
| 1676 | Проверить SLO chapter against new policy/catalog language. |
| 1677 | Уточнить incident candidate triggers. |
| 1678 | Перенести event catalog details to companion. |
| 1679 | Проверить render of tables/list-like blocks in observability chapters. |
| 1680 | Подготовить report по observability part. |
| 1681 | Пересмотреть главы 17-20 after chapter 22 rewrite. |
| 1682 | Уточнить owner map for capabilities and policy bundles. |
| 1683 | Добавить explicit handoff from organization layer to runtime/policy layer. |
| 1684 | Снять повторы про accountability, оставить one strong statement per chapter. |
| 1685 | Проверить incident response chapter for policy decision evidence. |
| 1686 | Добавить retirement link to lifecycle status in catalog. |
| 1687 | Проверить ADLC chapter against capability lifecycle states. |
| 1688 | Добавить organization dashboard route to companion. |
| 1689 | Render-check pages around chapters 17-22 in both DOCX variants. |
| 1690 | Подготовить report по organization/runtime bridge. |
| 1691 | Пересмотреть appendices for duplicate schemas and stale routes. |
| 1692 | Сформировать финальный companion manifest by chapter. |
| 1693 | Проверить sources appendix for current primary-source references. |
| 1694 | Уточнить glossary entries: policy decision, capability catalog, approval record, verifier. |
| 1695 | Проверить all internal cross-references in Google Doc export. |
| 1696 | Сформировать publisher-facing readiness memo. |
| 1697 | Обновить submission checklist with current artifacts and page counts. |
| 1698 | Сделать full raw DOCX render QA after next major pass. |
| 1699 | Сделать full Template2000n render QA after next major pass. |
| 1700 | Подготовить consolidated editorial report: что готово, что требует автора, что требует издательства. |

## Author-owned fields still open

- `Об авторе`: имя, роль, публичное позиционирование, опыт, проекты, ссылки.
- Авторская формулировка для издательства.
- Public companion URL and final repository structure.
- Real author cases/examples if the manuscript should carry personal practice.
- Publisher-required legal, compliance or AI-use disclosure wording.

