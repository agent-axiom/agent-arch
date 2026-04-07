# Agent Architecture Book

[Русская версия](README.ru.md)
[Contributing guide](CONTRIBUTING.md)
[Code of Conduct](CODE_OF_CONDUCT.md)

Publishable documentation site and book about modern secure AI agent architecture.

![Agent Architecture Book Preview](docs/assets/images/readme.png)

## What this repository contains

- a GitHub Pages site built with `MkDocs` and `Material for MkDocs`
- a multilingual documentation structure
- the first published part of the book on safe agent architecture
- a small runnable reference package in `agent_runtime_ref/`
- a modern Python-first tooling setup based on `uv`

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
uv run mkdocs build --strict
.venv/bin/python -m unittest discover -s tests
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
- YAML-driven configs for the operational skeleton

Quick examples:

```bash
.venv/bin/python -m agent_runtime_ref simulate-run
.venv/bin/python -m agent_runtime_ref inspect-agent
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
