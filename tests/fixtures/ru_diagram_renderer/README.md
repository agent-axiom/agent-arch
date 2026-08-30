# Russian diagram renderer E2E fixtures

The harness renders `good-manifest.json` as one Dagre-and-ELK batch, then renders
each entry from `defective-manifest.json` in an isolated process. It requires a
local Mermaid 11.17.2 browser bundle and a local Chrome executable; it never
downloads dependencies.

The repository-pinned Node 20+ setup is in `docs/publisher/package.json` and
`docs/publisher/package-lock.json`. CI installs it with `npm ci`, installs the
pinned Playwright Chromium build, and runs both contract and browser suites:

```sh
npm test --prefix docs/publisher
```

When `CI=true`, missing Mermaid, Playwright, Sharp, or Chromium dependencies are
test failures. They are never reported as skips.

Run it as a Node test with environment variables:

```sh
NODE_PATH=/absolute/path/to/node_modules \
MERMAID_JS=/absolute/path/to/mermaid-11.17.2.min.js \
CHROME=/absolute/path/to/chrome \
node --test tests/test_ru_diagram_renderer_e2e.mjs
```

The same harness accepts Mermaid and Chrome paths through CLI flags:

```sh
NODE_PATH=/absolute/path/to/node_modules \
node tests/ru_diagram_renderer_e2e_harness.mjs \
  --mermaid-js /absolute/path/to/mermaid-11.17.2.min.js \
  --chrome /absolute/path/to/chrome
```

For every case, the harness checks the generated SVG and PNG, the SVG geometry
record in the deterministic JSON report, and the renderer exit status. Every
defective case must exit nonzero only after its report contains the category in
`fixture_expected_finding`.

`invalid-feedback-manifest.json` covers configuration failures that must stop
before rendering or report creation. The accepted feedback fixture proves that
Mermaid 11.17.2 keeps the global curve linear and applies a reviewed curve only
to the named edge ID.
