# 智能体 registry 与 inventory 运维手册

当一个组织里已经有多个智能体系统时，只靠一章 inventory 已经不够了。团队还需要一套简明的 operating model：谁维护 registry，如何识别 drift，什么时候一个 agent 算 orphaned，deprecated entries 又该如何处理。

这份手册把这套最小工作面放在一页里。

## 1. 哪些层应该始终存在

即使是规模不大的智能体计划，也最好始终保留两层：

- `inventory`，用于记录全部 agent-like entities；
- `registry`，用于记录那些已经被识别、分类并允许进入 production contour 的实体。

如果只有 registry，团队通常会低估 shadow agents 与 local experiments。
如果只有 inventory，没有 registry，就没人能明确说明哪些东西真正算 approved。

## 2. 谁应该拥有这一层

当 ownership 模糊时，registry 往往很快失效。

最小可用的分工通常是：

- platform team 负责 registry 结构与 verification rules；
- product owner 负责 business purpose 与 lifecycle state；
- safety 或 governance owner 负责 policy 与 approval linkage；
- operations 负责 incident contact 与 retirement hygiene。

这些角色可以由同一支团队兼任，但角色本身必须明确。

## 3. 一条 agent record 应该包含什么

最小 record 最适合按一个固定模板检查：

- `agent_id`
- owner team；
- business purpose；
- lifecycle state；
- risk tier；
- runtime identity；
- allowed capabilities；
- policy bundle；
- approval mode；
- observability coverage；
- bundle linkage；
- retirement linkage。

没有这些内容，registry 很快就会退化成一个只有名字的列表，缺少 operational 意义。

## 4. 什么时候 agent 必须进入 inventory

一个比较强的默认规则通常是：

- 只要这个实体可以调用 tools；
- 只要它会读取组织上下文；
- 只要它会代表员工或服务行动；
- 只要它参与 production workflow；

它至少应该进入 inventory。

例外情况最好被明确记录，而不是作为默许存在。

## 5. 什么时候 agent 必须进入 registry

通常需要进入 registry 的实体包括：

- 运行在 production contour 中；
- 访问 sensitive tools 或 external systems；
- 能产生 side effects；
- 参与 staged rollout；
- 需要 audit-ready ownership。

这也是 registry 对 governance、approvals 与可靠 incident response 很重要的原因。

## 6. registry 应该多久检查一次

registry 之所以失真，通常不是因为设计不好，而是因为 operating rhythm 太弱。

最小 cadence 通常包括：

- 每次 rollout update；
- 每次 high-risk change review；
- 定期 inventory review；
- 每次 retirement 或 replacement event；
- 每次 incident review 之后，如果发现了 hidden agents 或 stale records。

如果这些时点都不更新 registry，drift 几乎不可避免。

## 7. 最值得优先捕捉的 drift 信号

并不是所有 drift 都同样危险。最好先盯住：

- active agent 没有 owner；
- `production` agent 在 traces 或 registry-linked telemetry 里根本看不到；
- deprecated agent 仍然保留 live principal；
- runtime 里出现了不在 allowed inventory 中的 capability；
- registry 中的 approval mode 与 policy bundle 不一致；
- 已 retired 的 bundle 仍然出现在 live runs 中。

这已经足够构成一个最小 continuous verification loop。

## 8. 什么时候该把记录改成 restricted、deprecated 或 retired

最好尽早调整 lifecycle state：

- `restricted`：当 capability set 或 approval mode 被临时收窄时；
- `deprecated`：当 replacement 已经确定，新 rollout waves 不应再走旧路径时；
- `retired`：当 principal 已被撤销、rollout 已停止、historical state 已进入 retention mode 时。

这里最常见的错误很简单：agent 实际上已经退出使用，但 registry 里仍然显示它是 production-ready。

## 9. incident response 时应该看什么

在 incident review 中，registry 的价值不在于“有目录”，而在于它应该能快速回答几件事：

- 哪个 agent 参与了这个事件；
- 它的 owner 是谁；
- 当时它处于什么 lifecycle state；
- 哪个 policy bundle 与 approval mode 本应生效；
- 这条记录关联了哪个 bundle linkage 与 retirement status。

如果 registry 不能快速回答这些问题，它对 operations 的帮助就很有限。

## 10. 最小 weekly review

一轮简短 review 可以围绕这些问题展开：

- inventory 外是否出现了新的 agent-like entities？
- 是否存在 orphaned records？
- 是否存在没有 telemetry coverage 的 `production` agents？
- 是否有保留 live principals 的 deprecated entries？
- registry、policy bundle 与 rollout state 之间是否一致？

这种 review 最好保持简短，但持续进行。

## 11. 实用检查清单

- 每个 active agent 都有 owner 吗？
- inventory 和 registry 分开了吗？
- rollout 与 retirement 时 lifecycle state 会更新吗？
- registry 是否与 policy bundle 和 approval mode 相连？
- registry 是否会对照 live telemetry 进行验证？
- deprecated agents 会失去 principals 与 tool access 吗？
- incidents 会推动 registry hygiene 改进吗？

## 延伸阅读

- [智能体系统事故响应手册](incident-response-playbook.zh.md)
- [Lifecycle Artifact Schema](lifecycle-artifact-schema.zh.md)
- [Change Review 与 Rollout Gate Schema](change-rollout-schema.zh.md)
- [参考运行时包](reference-package.zh.md)
- [第 26 章：AI-Native Observability、Inventory Coverage 与 Detection-Ready Telemetry](../book/part-viii/chapter-26.zh.md)
- [第 27 章：Agent Inventory、Registry 与 Sprawl 治理](../book/part-viii/chapter-27.zh.md)
