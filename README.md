# Agent Architecture Book

![Coverage](docs/assets/badges/coverage.svg)

[Русская версия](README.ru.md)
[中文版](README.zh.md)
[Contributing guide](CONTRIBUTING.md)
[Code of Conduct](CODE_OF_CONDUCT.md)

A practical book and documentation site about secure, governable, production-grade AI agent architecture.

This project is for people who want to build not demo magic, but calm, controllable, and safe agent systems that can survive contact with real users, real tools, and real operations.

![Agent Architecture Book Preview](docs/assets/images/readme.png)

## Why this repository exists

Most agent tutorials optimize for fast demos. Real systems need more than clever prompting or tool calling. They need:

- explicit trust boundaries
- policy enforcement and approvals
- memory discipline
- observability and evals
- rollout control and lifecycle management

This repository exists to document that full operating model.

## What this repository contains

- a multilingual book on secure AI agent architecture
- a GitHub Pages documentation site built with `MkDocs` and `Material for MkDocs`
- a runnable reference runtime in `agent_runtime_ref/`
- practical schemas, checklists, and operational artifacts
- a modern Python-first tooling setup based on `uv`

## Why read it

- **Vendor-neutral architecture.** The book focuses on principles and operating models that outlive any single framework or model provider.
- **Production reality over agent theater.** It emphasizes policy, approvals, observability, evals, and lifecycle discipline.
- **A runnable reference layer.** The repository includes executable reference assets, not just prose.
- **One running case across the stack.** The support-triage / duplicate-ticket thread connects the book, reference schemas, and `agent_runtime_ref` so readers can follow one incident from retrieval and tool execution to telemetry, evals, rollout, lifecycle, and registry control.
- **Three canonical cases for coverage.** Support triage covers write capabilities and approvals, Internal knowledge assistant covers retrieval, memory, freshness, and knowledge provenance, and Incident coordination covers traces, escalation, notification side effects, response ownership, and post-incident learning.

## Start here

- Read the site: <https://agent-axiom.github.io/agent-arch/>
- Start with the book homepage: [docs/index.en.md](docs/index.en.md)
- Open the guided entry page: [docs/start-here.en.md](docs/start-here.en.md)
- Safe-agent schema spine: follow the [trace schema](docs/appendix/trace-schema.en.md), [eval schema](docs/appendix/eval-schema.en.md), and [memory/retrieval schema](docs/appendix/memory-retrieval-schema.en.md) for the MCP threat model, A2A handoff trust contract, verifier verdict record, governance action record, memory poisoning review fields, and unified agent threat evidence.
- Explore the reference runtime: [docs/appendix/reference-package.en.md](docs/appendix/reference-package.en.md)

## Local development

```bash
uv sync --group docs --group dev
uv run mkdocs serve
```

The local site will be available at `http://127.0.0.1:8000/`.

## Checks

```bash
uv run ruff check .
uv run ty check
uv run pytest --cov=agent_runtime_ref --cov-report=term-missing
uv run mkdocs build --strict
```

## Reference package

The repository includes a minimal runnable skeleton package:

```bash
.venv/bin/python -m agent_runtime_ref
```

It gives you a compact reference runtime for the book:

- runtime and policy layer
- capability catalog and approved inventory
- memory path, telemetry, approvals, and rollout checks
- lifecycle-oriented artifacts for change records, artifact bundles, and retirement plans
- a visible sandbox profile contract and sandbox review evidence in lifecycle inspection
- YAML-driven configs for the operational skeleton

Quick examples:

```bash
.venv/bin/python -m agent_runtime_ref simulate-run
.venv/bin/python -m agent_runtime_ref inspect-agent
.venv/bin/python -m agent_runtime_ref inspect-lifecycle
.venv/bin/python -m agent_runtime_ref inspect-session
.venv/bin/python -m agent_runtime_ref export-session --output artifacts/session-demo-001.json
.venv/bin/python -m agent_runtime_ref export-eval-dataset --output artifacts/eval-dataset.json
```

The canonical walkthrough, full CLI list, and config overview live on the docs page:

- [Reference package](docs/appendix/reference-package.en.md)

## Optional research dependencies

If you want notebooks or data analysis tooling:

```bash
uv sync --group research
```

The `research` group already includes `marimo` and `polars`.

## Publishing

The repository includes a GitHub Actions workflow for GitHub Pages:

- build with `uv`
- strict `mkdocs build --strict`
- Pages deployment from the `docs-prod` branch

Before publishing, run the local gates and make sure `main` can fast-forward both remote
branches:

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

Once write credentials are configured, publish with fast-forward pushes only:

```bash
git push origin main
git push origin HEAD:docs-prod
```

Do not force-push `docs-prod`; it is intentionally just the GitHub Pages trigger branch.

## First GitHub Pages setup

`actions/configure-pages@v5` has an important limitation: if Pages have never been enabled in the repository before, the default `GITHUB_TOKEN` may not be able to bootstrap the Pages site automatically.

There are two correct ways to handle the first setup:

1. Enable Pages once in `Settings -> Pages` and choose `GitHub Actions`.
2. Add a `PAGES_PAT` secret with sufficient permissions, and the workflow can enable Pages automatically.

If the `github-pages` environment has deployment branch restrictions, make sure it explicitly allows deployments from `docs-prod`.

`PAGES_PAT` should be a real token, not `GITHUB_TOKEN`:

- for a Personal Access Token: `repo` or Pages write permission
- for a GitHub App: `administration:write` and `pages:write`

## Branch model

- `main` is the source-of-truth development branch
- `docs-prod` is the publication branch used for GitHub Pages deployment

## Stack

- `uv` for environment and dependency management
- `ruff` for linting
- `ty` for type checking
- `MkDocs + Material for MkDocs` for publishing
- `Mermaid` and `Observable Plot` for visual content

## License

This repository is published under [CC BY-SA 4.0](LICENSE).
