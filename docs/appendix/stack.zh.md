# 发布技术栈

## 简短回答

在 2026 年，`MkDocs + Material for MkDocs` 仍然不能算过时。对于基于 Python、以 Markdown 为中心的书籍型站点，它依旧是最务实的选择之一：

- 上手门槛低；
- 构建速度快；
- 搜索和导航开箱即用；
- 很容易部署到 GitHub Pages；
- 与 `uv`、`ruff`、`ty` 集成自然。[^mkdocs][^material][^uv][^ty]

同时，生态确实处于过渡期。这个仓库故意固定 `mkdocs<2`，以保持当前插件和主题栈的兼容性，并避免在第一版公开发布时引入不必要的迁移风险。

## 为什么没有立刻切到 Astro Starlight

如果你需要下面这些能力，`Starlight` 是很强的选择：

- MDX 与自定义 UI 组件；
- 更重的前端定制；
- 与 Astro 生态更紧密的结合。[^starlight]

但对这本书来说，目前更重要的是：

- 快速写作；
- 稳定发布；
- 保持整个 authoring stack 在 Python 内；
- 没有明确需求前，不额外增加 CI 和本地构建复杂度。

因此，第一版采用 MkDocs，而不是 Astro。

## 选定的技术基础

### 核心栈

- `uv` 用于 Python、虚拟环境与 dependency groups；
- `MkDocs` 与 `Material for MkDocs` 用于站点生成；
- `ruff` 用于 linting；
- `ty` 作为未来仓库出现 Python 工具代码时的快速 type checker。

### 可选 research 栈

- `marimo` 用于交互式研究型 notebooks；
- `polars` 用于分析 traces 和 eval datasets。

在当前项目骨架里，`marimo` 和 `polars` 已经作为 `research` 依赖组存在，即使书籍还没有直接使用它们。

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
- 从 docs-as-book 转变为 docs-as-app。

目前还没有这些需求。

[^mkdocs]: [MkDocs](https://www.mkdocs.org/)
[^material]: [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
[^uv]: [uv: Working on projects](https://docs.astral.sh/uv/guides/projects/)
[^ty]: [ty documentation](https://docs.astral.sh/ty/)
[^starlight]: [Starlight documentation](https://starlight.astro.build/)

