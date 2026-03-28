# Contributing Guide

Thank you for contributing to **Agent Architecture Book**.

Please also read the [Code of Conduct](CODE_OF_CONDUCT.md) before participating.

This repository is both a documentation site and an evolving book about modern secure AI agent architecture. Good contributions here are not only code changes. They also include:

- improving explanations
- adding diagrams
- fixing broken links
- refining translations
- adding examples
- improving build or publishing workflow

## Before you start

Please keep two things in mind:

1. This repository is **content-first**.
2. Clarity is more important than cleverness.

If you are changing content, the goal is not to sound academic. The goal is to help a reader understand, implement, and safely apply the ideas in practice.

## What kinds of contributions are welcome

- New chapters or chapter drafts
- Better architecture diagrams
- Security, reliability, or observability examples
- Translation fixes for Russian, English, and Chinese content
- Better navigation, UX, or presentation
- CI/CD and publishing improvements
- Source verification and citation cleanup

## Repository model

- `main` is the source-of-truth branch
- `docs-prod` is the publication branch used for GitHub Pages

In practice:

- make changes in a feature branch
- merge into `main`
- fast-forward or sync `docs-prod` when publishing

## License

By contributing to this repository, you agree that your contributions will be
distributed under the repository license: [CC BY-SA 4.0](LICENSE).

## Local setup

Install docs and development dependencies:

```bash
uv sync --group docs --group dev
```

Run the local docs server:

```bash
uv run mkdocs serve
```

Optional research dependencies:

```bash
uv sync --group research
```

## Validation

Before opening a PR, run:

```bash
uv run ruff check .
uv run ty check
uv run mkdocs build --strict
```

If `uv run ty check` is not relevant because the change is documentation-only, mention that clearly in your PR.

## Content conventions

### Tone

The book should feel technically serious, but still warm and readable.

- prefer direct language
- explain why something matters
- avoid unnecessary jargon
- prefer practical framing over abstract framing
- when writing in Russian, address the reader as `ты`

### Writing style

- use short sections
- use examples where they genuinely improve understanding
- do not add filler
- avoid marketing language
- avoid vague claims without explanation or source

### Architecture guidance

When adding architectural recommendations:

- prefer primary sources
- distinguish recommendations from hard requirements
- say when something is an engineering tradeoff
- favor patterns that are production-realistic

## Sources and citations

Use links to primary or official sources whenever possible.

Good source categories:

- official documentation
- engineering blog posts from model/platform vendors
- standards and risk frameworks
- security guidance from recognized organizations

Avoid building new content on top of:

- low-signal SEO articles
- unattributed summaries
- opinion pieces without technical grounding

If you add substantial claims, add or update citations in the relevant page and, if needed, in `docs/appendix/sources*.md`.

## Localization rules

This project currently supports:

- Russian
- English
- Chinese

Localization uses `mkdocs-static-i18n` with filename suffixes:

- default language: `page.md`
- English: `page.en.md`
- Chinese: `page.zh.md`

Examples:

- `docs/index.md`
- `docs/index.en.md`
- `docs/index.zh.md`

When changing a canonical page:

1. update the default file first
2. update translated versions if the change affects meaning, structure, navigation, or examples
3. if a translation lags behind, mention it explicitly in the PR

Do not silently let translated pages drift on core concepts.

## Diagrams and visuals

The preferred visual stack is:

- `Mermaid` for architecture and flow diagrams
- `Observable Plot` for lightweight interactive charts

Use Mermaid for:

- system architecture
- request flow
- approval paths
- threat boundaries
- lifecycle diagrams

Use Observable Plot for:

- prioritization maps
- maturity curves
- risk matrices
- simple comparative views

Guidelines:

- keep diagrams readable on laptop screens
- avoid giant all-in-one diagrams
- prefer one idea per diagram
- keep labels short
- make visuals explain something, not decorate the page

## Code examples

Code examples are welcome when they clarify implementation.

Prefer:

- short Python examples
- config snippets in YAML
- realistic gateway/policy/eval examples

Avoid:

- toy code that teaches nothing
- long blocks that hide the actual idea
- framework-specific code unless the framework is part of the point

## Navigation and structure

If you add a new top-level page, update:

- `mkdocs.yml`
- translated navigation labels if required by the change

If you add a new section of the book, try to keep:

- a clear reader path
- a reasonable chapter size
- internal links to adjacent chapters or appendices

## Pull request checklist

Before submitting a PR, verify:

- the docs build passes in strict mode
- links are valid
- navigation is still coherent
- translated pages are updated where needed
- diagrams render correctly
- sources are included for new substantial claims

## Suggested PR format

Please include:

- what changed
- why it changed
- whether translations were updated
- whether build checks passed
- screenshots if the UI or visuals changed

## Small contributions

You do not need a massive PR to help.

Very useful small contributions include:

- fixing one unclear paragraph
- correcting a broken source link
- improving one diagram
- tightening one translation
- replacing a vague claim with a sourced one

These changes matter.
