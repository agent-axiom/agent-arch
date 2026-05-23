# 发布技术栈

这一页说明了这本书为什么选择这套发布技术栈。

## 简短回答

`MkDocs + Material for MkDocs` 仍然是基于 Python、以 Markdown 为中心的书籍型站点的一套强选择：

- 上手门槛低；
- 构建速度快；
- 搜索和导航开箱即用；
- 很容易部署到 GitHub Pages；
- 与 `uv`、`ruff`、`ty` 集成自然。[^mkdocs][^material][^uv][^ty]

同时，生态确实处于过渡期。这个仓库故意固定 `mkdocs<2`，以保持当前插件和主题栈的兼容性，并避免在第一版公开发布时引入不必要的迁移风险。

!!! note "规范发布案例（Canonical publishing cases）"
    发布栈（Publishing stack）应该把三个规范案例（canonical cases）支撑成阅读路线（reader routes），而不只是构建页面（build pages）。**支持分流（Support triage）** 需要快速构建（fast build）、GitHub Pages 部署（GitHub Pages deployment）、搜索/导航（search/navigation）、可读的策略/审批示例（policy/approval examples），以及指向追踪/评测工件（trace/eval artifacts）的稳定链接（stable links）。**内部知识助手（Internal knowledge assistant）** 需要 Markdown 优先创作（Markdown-first authoring）、多语言页面（multilingual pages）、术语表/搜索表面（glossary/search surface）、来源链接（source links），以及对记忆/检索材料的低摩擦更新（low-friction updates for memory/retrieval material）。**事件协调（Incident coordination）** 需要严格构建门禁（strict build gate）、可复现文档命令（reproducible docs commands）、指向事件/发布页面的稳定导航（stable navigation to incident/rollout pages）、可见的变更日志式差异（visible changelog-style diffs）和迁移风险纪律（migration-risk discipline）。

## 为什么没有立刻切到 Astro Starlight

如果你需要下面这些能力，`Starlight` 是很强的选择：

- MDX 与自定义界面组件；
- 更重的前端定制；
- 与 Astro 生态更紧密的结合。[^starlight]

但对这本书来说，目前更重要的是：

- 快速写作；
- 稳定发布；
- 保持整个写作栈在 Python 内；
- 没有明确需求前，不额外增加 CI 和本地构建复杂度。

因此，第一版采用 MkDocs，而不是 Astro。

## 选定的技术基础

### 核心栈

- `uv` 用于 Python、虚拟环境与依赖组；
- `MkDocs` 与 `Material for MkDocs` 用于站点生成；
- `ruff` 用于代码检查；
- `ty` 作为未来仓库出现 Python 工具代码时的快速类型检查器。

### 可选研究栈

- `marimo` 用于交互式研究型笔记本；
- `polars` 用于分析追踪和评测数据集。

在当前项目骨架里，`marimo` 和 `polars` 已经作为 `research` 研究依赖组存在，即使书籍还没有直接使用它们。

## 项目命令

```bash
uv sync --group docs --group dev
uv run mkdocs serve
uv run mkdocs build --strict
uv run ruff check .
uvx ty check
```

## 什么时候值得迁移到 Starlight

如果书籍演化为下面这种形态，就值得迁移：

- 章节中嵌入 React、Vue 或 Svelte 组件；
- 拥有大量自定义交互；
- 从“文档即书籍”转变为“文档即应用”。

目前还没有这些需求。

[^mkdocs]: [MkDocs](https://www.mkdocs.org/)
[^material]: [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
[^uv]: [uv: Working on projects](https://docs.astral.sh/uv/guides/projects/)
[^ty]: [ty documentation](https://docs.astral.sh/ty/)
[^starlight]: [Starlight documentation](https://starlight.astro.build/)
