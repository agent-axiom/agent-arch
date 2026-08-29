import assert from "node:assert/strict";
import test from "node:test";

import { runFixtureHarness } from "./ru_diagram_renderer_e2e_harness.mjs";

const MERMAID_JS = process.env.MERMAID_JS;
const CHROME = process.env.CHROME;


test("Mermaid fixtures render through SVG geometry and enforce every defect", {
  skip: !MERMAID_JS || !CHROME
    ? "set MERMAID_JS and CHROME to run the browser fixture harness"
    : false,
}, async () => {
  const summary = await runFixtureHarness({
    mermaidJs: MERMAID_JS,
    chrome: CHROME,
  });

  assert.deepEqual(summary, {
    good_diagrams: 2,
    good_layout_engines: ["dagre", "elk"],
    defective_fixtures: 5,
    defective_findings: [
      "cluster_title_overlaps",
      "unrelated_edge_text_intersections",
      "node_label_overflows",
      "duplicate_edge_routes",
      "print_font_failures",
    ],
  });
});
