# 社区路线图

这本书已经有了很强的基础：架构、安全、记忆、执行、可观测性、组织模型，以及一个可运行的参考包。因此，下面不是通用愿望清单，而是**下一层价值**的 backlog。

## 已经完成的部分

- [从这里开始](../start-here.zh.md) 页面；
- [多语言术语表](glossary.zh.md)；
- [一组 cheat sheets](cheat-sheets.zh.md)；
- 第一组[实战案例](case-studies.zh.md)；
- 第一组[Policy Templates](policy-templates.zh.md)；
- 可运行的参考包及其[包文档](reference-package.zh.md)；
- 单独的[发布技术栈](stack.zh.md)页面。

## 如何选择下一步

下面每一项都满足三个条件：

- 可以很快用于真实工作；
- 帮助的是整个社区，而不只是作者本人；
- 提升的是国际可读性，而不只是技术深度。

## 接下来的 10 个改进

### 1. 扩展 case studies 集合

现有案例已经有用了，但还应该再补 2-3 个：

- enterprise workflow agent；
- CRM/task agent；
- security-sensitive assistant。

为什么重要：可识别场景越多，读者越容易把书里的架构映射到自己的系统上。

### 2. 扩展 policy templates 集合

书里已经有第一批例子，但社区还需要更明确的模板：

- tool approval policy；
- memory write policy；
- egress policy；
- rollout gate policy；
- retrieval policy。

为什么重要：可复制、可改造的模板，往往比长篇解释更有价值。

### 3. Trace schema 与 event catalog

需要一张单独的 telemetry reference 页面：

- 有哪些 event types；
- 哪些字段是必须的；
- `trace_id` 应该长什么样；
- 哪些 spans 算基线；
- 哪些内容绝不能写进 events。

为什么重要：当社区拥有统一事件模型时，可观测性才会真正形成共享实践，而不只是共享概念。

### 4. 扩展 `agent_runtime_ref` 的真实场景

参考包已经有用了，但下一步还应该补上：

- 一个 knowledge scenario；
- 一个带 approval 的 high-risk scenario；
- 一个 denied-by-policy scenario；
- 在文档里放几份 JSONL traces 示例。

为什么重要：可运行的参考包不该只展示 happy path，它应该教会读者生产环境里的真实行为。

### 5. 面向社区的 contribution kit

要让外部贡献更容易：

- 一页 `How to contribute patterns`；
- 一个 case study 模板；
- 一个 glossary entry 模板；
- 一个 policy template 模板。

为什么重要：好的开放手册会成长得更快，前提是贡献者知道该怎么帮忙。

### 6. 更强的内链与 chapter journeys

需要让章节之间的移动更顺：

- 更明确的 “下一步读什么”；
- 架构、案例和模板之间更强的互链；
- 每个部分内部更短的 decision paths。

为什么重要：这本书越不容易让人迷路，它的实际价值就越高。

### 7. discoverability 层

需要更系统的 discoverability 改进：

- glossary；
- cheatsheets；
- 更强的章节内链；
- social preview assets；
- `ru/en/zh` 三语更结构化的落地页文案。

为什么重要：即使书本身很强，如果别人难以发现、难以快速理解、难以转发，它对社区的帮助也会打折扣。

### 8. Social and sharing assets

需要一些轻量的传播素材：

- social preview assets；
- 几张适合转发的 cheat sheets；
- `ru/en/zh` 的简短 landing summaries。

为什么重要：国际传播不只取决于内容本身，也取决于它是否方便分享。

## 最该先做什么

如果接下来只能做三件事，我会这样排：

1. Trace schema 与 event catalog
2. Contribution kit
3. 扩展 case studies 集合

这是在不重写架构章节的前提下，最快提升实际价值的组合。

## 一个月后会带来什么变化

如果把这份 backlog 落下来，项目会获得：

- 对新读者更清晰的入口；
- 更多可被引用和分享的页面；
- 更多团队可以直接复用的材料；
- 更清晰的社区参与路径；
- 更强的国际化项目形象。

## 下一步最实用的动作

如果按这条路线走，下一步最值得做的是 trace schema 与 event catalog，接着是 contribution kit。

- [首页](../index.zh.md)
- [全书计划](../book/plan.zh.md)
- [参考包](reference-package.zh.md)
- [参考来源](sources.zh.md)
