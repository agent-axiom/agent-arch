import assert from "node:assert/strict";
import test from "node:test";

import { runFixtureHarness } from "./ru_diagram_renderer_e2e_harness.mjs";
import {
  assertBrowserTestEnvironment,
  browserTestSkip,
  resolveBrowserTestEnvironment,
} from "./ru_diagram_test_environment.mjs";

const environment = resolveBrowserTestEnvironment();


test("Mermaid fixtures render through SVG geometry and enforce every defect", {
  skip: browserTestSkip(environment),
}, async () => {
  assertBrowserTestEnvironment(environment);
  const summary = await runFixtureHarness({
    mermaidJs: environment.mermaidJs,
    chrome: environment.chrome,
  });

  assert.deepEqual(summary, {
    good_diagrams: 3,
    good_layout_engines: ["dagre", "elk", "dagre"],
    reviewed_feedback_edge_ids: ["feedback"],
    defective_fixtures: 5,
    defective_findings: [
      "cluster_title_overlaps",
      "unrelated_edge_text_intersections",
      "node_label_overflows",
      "duplicate_edge_routes",
      "print_font_failures",
    ],
    invalid_feedback_fixtures: [
      "fixture-bad-feedback-missing-id.png",
      "fixture-bad-feedback-multiple.png",
      "fixture-bad-feedback-unidentified.png",
      "fixture-bad-feedback-unreviewed-curve.png",
    ],
  });
});
