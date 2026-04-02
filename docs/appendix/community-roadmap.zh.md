# 社区路线图

这本书已经有了很强的基础：架构、安全、记忆、执行、可观测性、组织模型，以及一个可运行的参考包。但如果目标是吸引全球读者，下一步最重要的不是“再写更多理论”，而是提供**更快可用的实际价值**。

下面是一份聚焦的 10 项改进 backlog。它不是抽象愿望清单，而是一组能让这本书对工程师、平台团队、安全团队和开源贡献者都更有用的具体升级。

## 选择标准

下面每一项都满足三个条件：

- 可以很快用于真实工作；
- 帮助的是整个社区，而不只是作者本人；
- 提升的是国际可读性，而不只是技术深度。

## Top 10 改进

### 1. 增加 `Start here` 页面

需要一张面向新读者的入口页：

- 这本书是什么；
- 适合谁看；
- 工程师应该从哪里开始；
- 安全团队应该从哪里开始；
- 现成模板和代码在哪里。

为什么重要：大多数读者不会从第一章开始，他们更想先找到自己的阅读路径。

### 2. 多语言 glossary

需要一个 `ru/en/zh` 术语表，覆盖关键术语：

- agent runtime；
- policy gate；
- trust boundary；
- profile memory；
- retrieval；
- compaction；
- rollout gate；
- capability catalog。

为什么重要：现在术语已经不错，但 glossary 会让阅读、翻译、链接引用和社区贡献都更顺畅。

### 3. 一页式 cheat sheets

需要几张简短实用的清单页：

- safety checklist；
- memory checklist；
- rollout checklist；
- observability checklist；
- tool gateway checklist。

为什么重要：这类页面最容易被收藏、转发，也最容易在真实项目里当天就用起来。

### 4. 一组 case studies

需要补充 3-5 个真实场景：

- support agent；
- internal knowledge agent；
- enterprise workflow agent；
- CRM/task agent；
- security-sensitive assistant。

为什么重要：案例能帮助读者迅速把书里的架构映射到自己的业务环境。

### 5. 可直接复用的 policy templates

书里已经有例子，但社区更需要明确的模板：

- tool approval policy；
- memory write policy；
- egress policy；
- rollout gate policy；
- retrieval policy。

为什么重要：可复制、可改造的模板，往往比长篇解释更有价值。

### 6. Trace schema 与 event catalog

需要一张单独的 telemetry reference 页面：

- 有哪些 event types；
- 哪些字段是必须的；
- `trace_id` 应该长什么样；
- 哪些 spans 算基线；
- 哪些内容绝不能写进 events。

为什么重要：当社区拥有统一事件模型时，可观测性才会真正形成共享实践，而不只是共享概念。

### 7. 扩展 `agent_runtime_ref` 的真实场景

参考包已经有用了，但下一步还应该补上：

- 一个 knowledge scenario；
- 一个带 approval 的 high-risk scenario；
- 一个 denied-by-policy scenario；
- 在文档里放几份 JSONL traces 示例。

为什么重要：可运行的参考包不该只展示 happy path，它应该教会读者生产环境里的真实行为。

### 8. 面向社区的 contribution kit

要让外部贡献更容易：

- 一页 `How to contribute patterns`；
- 一个 case study 模板；
- 一个 glossary entry 模板；
- 一个 policy template 模板。

为什么重要：好的开放手册会成长得更快，前提是贡献者知道该怎么帮忙。

### 9. 更强的首页

首页已经不错了，但还可以更适合第一次访问的人：

- 增加 “适合谁看” 模块；
- 增加 “30 分钟内你能带走什么” 模块；
- 增加 “这本书有什么不同” 模块。

为什么重要：全球传播首先取决于清晰度，而不是章节数量。

### 10. discoverability 层

需要更系统的 discoverability 改进：

- `Start here`；
- glossary；
- cheatsheets；
- 更强的章节内链；
- social preview assets；
- `ru/en/zh` 三语更结构化的落地页文案。

为什么重要：即使书本身很强，如果别人难以发现、难以快速理解、难以转发，它对社区的帮助也会打折扣。

## 最该先做什么

如果接下来只能做三件事，我会这样排：

1. `Start here`
2. Glossary
3. Cheat sheets

这是在不重写架构章节的前提下，最快提升实际价值的组合。

## 一个月后会带来什么变化

如果把这份 backlog 落下来，项目会获得：

- 对新读者更清晰的入口；
- 更多可被引用和分享的页面；
- 更多团队可以直接复用的材料；
- 更清晰的社区参与路径；
- 更强的国际化项目形象。

## 下一步最实用的动作

如果按这条路线走，下一页最值得做的是 `Start here`，紧接着就是多语言 glossary。

- [首页](../index.zh.md)
- [全书计划](../book/plan.zh.md)
- [参考包](reference-package.zh.md)
- [参考来源](sources.zh.md)
