# 智能体架构之书（Agent Architecture Book）

![Coverage](docs/assets/badges/coverage.svg)

[英文版（English version）](README.md)
[俄文版（Russian version）](README.ru.md)
[贡献指南（Contributing guide）](CONTRIBUTING.md)
[行为准则（Code of Conduct）](CODE_OF_CONDUCT.md)

一本关于安全、可治理、生产就绪架构（production-ready architecture）的 AI 智能体实用书籍与文档站点。

这个项目面向那些不想只做演示型“智能体魔法”，而是想构建在真实用户（real users）、真实工具（real tools）和真实运维（real operations）条件下依然可控且安全的智能体系统（controlled and safe agent systems）的人。

![Agent Architecture Book Preview](docs/assets/images/readme.png)

## 为什么这个仓库存在（why this repository exists）

大多数智能体教程都在优化“快速演示（quick demo）”。但真实系统需要的不只是提示词技巧（prompting）和工具调用（tool calls）。它们还需要：

- 明确的信任边界（trust boundaries）
- 策略执行（policy enforcement）与审批机制（approvals）
- 记忆治理与约束（memory governance）
- 可观测性（observability）与评测体系（evals）
- 发布控制（rollout control）与生命周期治理（lifecycle governance）

这个仓库的目标，是把这一整套运行模型完整地讲清楚。

## 这个仓库包含什么（what is in this repository）

- 一本关于安全 AI 智能体架构的多语言书籍
- 一个基于 `MkDocs` 和 `Material for MkDocs` 的 GitHub Pages 文档站点
- 位于 `agent_runtime_ref/` 的可运行参考运行时（runtime）
- 一组实用的模式、检查清单与运维工件
- 一个基于 `uv` 的现代 Python-first 工具链

## 为什么值得读（why read this）

- **面向原则的厂商中立架构（vendor-neutral architecture）。** 这本书关注的是能跨越具体框架（framework）和模型厂商（model provider）长期成立的架构原则与运行模型。
- **关注生产现实（production reality），而不是智能体表演（agent theater）。** 它强调策略、审批、可观测性、评测（evals）与生命周期纪律。
- **不仅有文字，也有可运行参考层。** 仓库里不仅有概念性说明（conceptual prose），还包含可执行的参考资产（reference assets）。
- **一条贯穿全栈的案例线（full-stack case）。** 支持分诊 / 重复工单线索（support-triage / duplicate-ticket thread）把书籍、参考模式（reference schemas）和 `agent_runtime_ref` 连在一起，让读者可以沿着一个事故，从检索（retrieval）与工具执行（tool execution）一路看到遥测（telemetry）、评测（evals）、发布（rollout）、生命周期（lifecycle）和注册表控制（registry control）。
- **三个规范案例（canonical cases）用于覆盖检查（coverage check）。** 支持分诊（Support triage）覆盖写入能力（write capabilities）和审批（approvals），内部知识助手（Internal knowledge assistant）覆盖检索（retrieval）、记忆（memory）、新鲜度（freshness）和知识来源（knowledge provenance），事件协调（Incident coordination）覆盖追踪（traces）、升级（escalation）、通知副作用（notification side effects）、响应归属（response ownership）和事后学习（post-incident learning）。

## 从这里开始（Start Here）

- 项目站点：<https://agent-axiom.github.io/agent-arch/>
- 书籍首页：[docs/index.zh.md](docs/index.zh.md)
- 导航入口页：[docs/start-here.zh.md](docs/start-here.zh.md)
- 安全智能体模式主线（Safe-agent schema spine）：[追踪模式（trace schema）](docs/appendix/trace-schema.zh.md)、[评测模式（eval schema）](docs/appendix/eval-schema.zh.md) 与 [记忆/检索模式（memory/retrieval schema）](docs/appendix/memory-retrieval-schema.zh.md) 连接 MCP 威胁模型（MCP threat model）、A2A 移交信任契约（A2A handoff trust contract）、验证器裁决记录（verifier verdict record）、治理动作记录（governance action record）、记忆投毒审查字段（memory poisoning review fields）和统一智能体威胁证据（unified agent threat evidence）。
- 参考运行时包（reference package）：[docs/appendix/reference-package.zh.md](docs/appendix/reference-package.zh.md)

## 本地开发（local development）

```bash
uv sync --group docs --group dev
uv run mkdocs serve
```

本地站点会运行在 `http://127.0.0.1:8000/`。

## 检查（checks）

```bash
uv run ruff check .
uv run ty check
uv run pytest --cov=agent_runtime_ref --cov-report=term-missing
uv run mkdocs build --strict
```

## 参考包（reference package）

仓库中包含一个可运行的最小参考骨架包：

```bash
.venv/bin/python -m agent_runtime_ref
```

它为本书提供紧凑的代码支撑（compact code support），包含：

- 参考运行时（runtime）与策略层（policy layer）
- 能力目录（capability catalog）与已批准清单（approved inventory）
- 记忆路径（memory path）、遥测（telemetry）、审批（approvals）与发布检查（rollout checks）
- 生命周期工件（lifecycle artifacts），用于变更记录（change records）、工件包（artifact bundles）与退役计划（retirement plans）
- 生命周期检查（lifecycle inspection）中可见的沙箱配置契约（sandbox profile contract）与沙箱审查证据（sandbox review evidence）
- 用于运行骨架（operational skeleton）的 YAML 配置（YAML configs）

快速示例（quick examples）：

```bash
.venv/bin/python -m agent_runtime_ref simulate-run
.venv/bin/python -m agent_runtime_ref inspect-agent
.venv/bin/python -m agent_runtime_ref inspect-lifecycle
.venv/bin/python -m agent_runtime_ref inspect-session
.venv/bin/python -m agent_runtime_ref export-session --output artifacts/session-demo-001.json
.venv/bin/python -m agent_runtime_ref export-eval-dataset --output artifacts/eval-dataset.json
```

规范包说明（canonical package description）、完整 CLI 命令列表（CLI commands）和配置概览（config overview）可见：

- [参考运行时包（runtime reference package）](docs/appendix/reference-package.zh.md)

## 可选研究依赖（optional research dependencies）

如果你需要笔记本（notebooks）或数据分析工具（data analysis tools）：

```bash
uv sync --group research
```

研究组（research group）已包含 `marimo` 与 `polars`。

## 发布（publishing）

仓库内包含用于 GitHub Pages 的 GitHub Actions 工作流（GitHub Actions workflow）：

- 通过 `uv` 执行构建（build）
- 严格检查（strict check）`mkdocs build --strict`
- 从发布分支（publishing branch）`docs-prod` 部署（deploy）到 Pages

发布前，先运行本地检查（local checks），并确认 `main` 可以以 fast-forward 方式更新两个远端分支：

```bash
.venv/bin/ruff check .
.venv/bin/ty check
.venv/bin/pytest --cov=agent_runtime_ref --cov-report=term-missing
.venv/bin/mkdocs build --strict
git diff --check
git status --short --branch
git rev-list --left-right --count origin/main...HEAD
git rev-list --left-right --count origin/docs-prod...HEAD
```

配置好写入凭据（write credentials）后，只用 fast-forward push 命令（fast-forward push commands）发布：

```bash
git push origin main
git push origin HEAD:docs-prod
```

不要 force-push 到 `docs-prod`；它刻意只是 GitHub Pages 的触发分支（trigger branch）。

## GitHub Pages 首次设置（first GitHub Pages setup）

`actions/configure-pages@v5` 有一个重要限制（important limitation）：如果仓库此前从未启用过 Pages，默认的 `GITHUB_TOKEN` 可能无法自动创建 Pages 站点（Pages site）。

有两种正确选项（correct options）：

1. 在 `Settings -> Pages` 中手动启用 Pages（manually enable Pages）一次，并选择 `GitHub Actions`。
2. 添加一个具有足够权限的 `PAGES_PAT` secret，让工作流（workflow）自动启用 Pages。

如果 `github-pages` environment 配置了分支限制（branch restrictions），请确保显式允许来自 `docs-prod` 的部署（deployment）。

`PAGES_PAT` 必须是单独的 token（separate token），而不是 `GITHUB_TOKEN`：

- 个人访问令牌（Personal Access Token）：`repo` 或 Pages 写权限（Pages write permission）
- GitHub 应用（GitHub App）：`administration:write` 和 `pages:write`

## 分支模型（branch model）

- `main` 是开发分支（development branch）和事实来源（source of truth）
- `docs-prod` 承载 GitHub Pages 站点（GitHub Pages site）的发布分支（publishing branch）

## 技术栈（stack）

- `uv` 用于环境（environment）和依赖管理（dependencies）
- `ruff` 用于代码检查（linting）
- `ty` 执行类型检查（type checking）
- `MkDocs + Material for MkDocs` 用于发布（publishing）
- `Mermaid` 和 `Observable Plot` 生成可视化内容（visualizations）

## 许可证（license）

本仓库基于 [CC BY-SA 4.0](LICENSE) 授权发布（licensed under）。
