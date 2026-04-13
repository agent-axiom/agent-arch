# Agent Architecture Book

![Coverage](docs/assets/badges/coverage.svg)

[English version](README.md)
[Русская версия](README.ru.md)
[Contributing guide](CONTRIBUTING.md)
[Code of Conduct](CODE_OF_CONDUCT.md)

一本关于安全、可治理、可用于生产环境的 AI 智能体架构的实用书籍与文档站点。

这个项目面向那些不想只做演示型“智能体魔法”，而是想构建在真实用户、真实工具和真实运维条件下依然可控、安全、稳定运行的智能体系统的人。

![Agent Architecture Book Preview](docs/assets/images/readme.png)

## 为什么这个仓库存在

大多数智能体教程都在优化“快速做出演示”。但真实系统需要的不只是提示词技巧和工具调用。它们还需要：

- 明确的信任边界
- 策略执行与审批机制
- 记忆治理与约束
- 可观测性与评测体系
- 发布控制与生命周期管理

这个仓库的目标，是把这一整套运行模型完整地讲清楚。

## 这个仓库包含什么

- 一本关于安全 AI 智能体架构的多语言书籍
- 一个基于 `MkDocs` 和 `Material for MkDocs` 的 GitHub Pages 文档站点
- 位于 `agent_runtime_ref/` 的可运行参考运行时
- 一组实用的模式、检查清单与运维工件
- 一个基于 `uv` 的现代 Python-first 工具链

## 为什么值得读

- **面向原则，而非单一厂商。** 这本书关注的是能跨越具体框架和模型厂商长期成立的架构原则与运行模型。
- **关注生产现实，而不是智能体表演。** 它强调策略、审批、可观测性、评测与生命周期纪律。
- **不仅有文字，也有可运行参考层。** 仓库里包含可执行的参考资产，而不只是概念说明。

## 从这里开始

- 项目站点：<https://agent-axiom.github.io/agent-arch/>
- 书籍首页：[docs/index.zh.md](docs/index.zh.md)
- 导航入口页：[docs/start-here.zh.md](docs/start-here.zh.md)
- 参考运行时：[docs/appendix/reference-package.zh.md](docs/appendix/reference-package.zh.md)

## 本地开发

```bash
uv sync --group docs --group dev
uv run mkdocs serve
```

本地站点会运行在 `http://127.0.0.1:8000/`。

## 检查

```bash
uv run ruff check .
uv run ty check
uv run pytest --cov=agent_runtime_ref --cov-report=term-missing
uv run mkdocs build --strict
```

## 参考运行时

仓库中包含一个可运行的最小参考骨架包：

```bash
.venv/bin/python -m agent_runtime_ref
```

它为本书提供一个紧凑的参考运行时，包含：

- 运行时与策略层
- 能力目录与批准清单
- 记忆路径、遥测、审批与发布检查
- 面向生命周期的变更记录、工件包与退役计划
- 用于 operational skeleton 的 YAML 配置

快速示例：

```bash
.venv/bin/python -m agent_runtime_ref simulate-run
.venv/bin/python -m agent_runtime_ref inspect-agent
.venv/bin/python -m agent_runtime_ref inspect-lifecycle
.venv/bin/python -m agent_runtime_ref inspect-session
.venv/bin/python -m agent_runtime_ref export-session --output artifacts/session-demo-001.json
.venv/bin/python -m agent_runtime_ref export-eval-dataset --output artifacts/eval-dataset.json
```

规范说明、完整 CLI 列表和配置概览可见：

- [参考运行时](docs/appendix/reference-package.zh.md)

## 可选研究依赖

如果你需要 notebook 或数据分析工具：

```bash
uv sync --group research
```

`research` 组已包含 `marimo` 与 `polars`。

## 发布

仓库内包含用于 GitHub Pages 的 GitHub Actions 工作流：

- 使用 `uv` 构建
- 严格执行 `mkdocs build --strict`
- 从 `docs-prod` 分支部署到 Pages

## GitHub Pages 首次设置

`actions/configure-pages@v5` 有一个重要限制：如果仓库此前从未启用过 Pages，默认的 `GITHUB_TOKEN` 可能无法自动完成站点初始化。

有两种正确处理方式：

1. 在 `Settings -> Pages` 中手动启用一次，并选择 `GitHub Actions`。
2. 添加一个具有足够权限的 `PAGES_PAT` secret，让 workflow 自动启用 Pages。

如果 `github-pages` environment 配置了部署分支限制，请确保显式允许来自 `docs-prod` 的部署。

`PAGES_PAT` 必须是真实 token，而不是 `GITHUB_TOKEN`：

- Personal Access Token: `repo` 或 Pages 写权限
- GitHub App: `administration:write` 和 `pages:write`

## 分支模型

- `main` 是事实来源开发分支
- `docs-prod` 是 GitHub Pages 使用的发布分支

## 技术栈

- `uv` 用于环境和依赖管理
- `ruff` 用于 lint
- `ty` 用于类型检查
- `MkDocs + Material for MkDocs` 用于发布
- `Mermaid` 和 `Observable Plot` 用于可视化内容

## 许可证

本仓库基于 [CC BY-SA 4.0](LICENSE) 发布。
