# Publishing Stack

This page explains why the book uses this publishing stack.

## Short answer

`MkDocs + Material for MkDocs` remains a strong choice for a Markdown-first book on a Python stack:

- low barrier to entry;
- fast builds;
- strong search and navigation out of the box;
- easy GitHub Pages deployment;
- natural integration with `uv`, `ruff`, and `ty`.[^mkdocs][^material][^uv][^ty]

At the same time, the ecosystem is in a transition period. This repository intentionally pins `mkdocs<2` to preserve compatibility with the current plugin and theme stack and to avoid unnecessary migration risk in the first public version.

## Why I did not switch to Astro Starlight immediately

`Starlight` is a strong option if you need:

- MDX and custom UI components;
- heavier front-end customization;
- tighter alignment with the Astro ecosystem.[^starlight]

For this book, however, different priorities matter more:

- writing fast;
- publishing reliably;
- keeping the authoring stack in Python;
- avoiding extra CI and local-build complexity without a real need.

That is why the first version is built on MkDocs instead of Astro.

## Chosen technology base

### Core stack

- `uv` for Python, virtual environments, and dependency groups;
- `MkDocs` and `Material for MkDocs` for site generation;
- `ruff` for linting;
- `ty` as a fast type checker when Python utilities appear in the repo.

### Optional research stack

- `marimo` for interactive research notebooks;
- `polars` for trace and eval dataset analysis.

In the current scaffold, `marimo` and `polars` are already included as the `research` dependency group, even though the book does not use them directly yet.

## Project commands

```bash
uv sync --group docs --group dev
uv run mkdocs serve
uv run mkdocs build --strict
uv run ruff check .
uvx ty check
```

## When migration to Starlight makes sense

Migration becomes reasonable if the book grows into:

- embedded React, Vue, or Svelte components inside chapters;
- a large amount of custom interactivity;
- a docs-as-app product rather than a docs-as-book project.

At the moment, those requirements do not exist.

[^mkdocs]: [MkDocs](https://www.mkdocs.org/)
[^material]: [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
[^uv]: [uv: Working on projects](https://docs.astral.sh/uv/guides/projects/)
[^ty]: [ty documentation](https://docs.astral.sh/ty/)
[^starlight]: [Starlight documentation](https://starlight.astro.build/)
