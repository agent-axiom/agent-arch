import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import {
  MIN_CLUSTER_TITLE_CLEARANCE_PX,
  MIN_EFFECTIVE_FONT_PT,
  MIN_UNRELATED_EDGE_TEXT_CLEARANCE_PX,
  MIN_VIEWBOX_ASPECT_RATIO,
  VISUAL_STYLE_ID,
  assessPrintGeometry,
  classifyGeometry,
  measureClusterTitleClearances,
  normalizeDiagramOptions,
} from "../docs/publisher/tools/ru_diagram_renderer_contract.mjs";

const TESTS_DIR = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(TESTS_DIR, "..");
const FIXTURE_PATH = path.join(
  TESTS_DIR,
  "fixtures/ru_diagram_renderer/geometry-cases.json",
);
const CASES = JSON.parse(fs.readFileSync(FIXTURE_PATH, "utf8"));


function clone(value) {
  return JSON.parse(JSON.stringify(value));
}


test("v2 constants enforce the print geometry floor", () => {
  assert.equal(VISUAL_STYLE_ID, "agent-arch-book-v2");
  assert.equal(MIN_EFFECTIVE_FONT_PT, 9.5);
  assert.equal(MIN_VIEWBOX_ASPECT_RATIO, 0.72);
  assert.equal(MIN_CLUSTER_TITLE_CLEARANCE_PX, 12);
  assert.equal(MIN_UNRELATED_EDGE_TEXT_CLEARANCE_PX, 10);
});


test("good geometry has no categorized findings", () => {
  const findings = classifyGeometry(clone(CASES.good));

  assert.deepEqual(findings, {
    cluster_title_overlaps: [],
    unrelated_edge_text_intersections: [],
    node_label_overflows: [],
    duplicate_edge_routes: [],
  });
});


test("successful cluster title clearances are measured and reported", () => {
  assert.deepEqual(measureClusterTitleClearances(clone(CASES.good)), [{
    cluster_id: "cluster-main",
    title_id: "cluster-title-main",
    node_id: "node-a",
    clearance_px: 25,
    overlaps: false,
  }, {
    cluster_id: "cluster-main",
    title_id: "cluster-title-main",
    node_id: "node-b",
    clearance_px: 132.38,
    overlaps: false,
  }]);
});


test("cluster title within 12px of a node is rejected", () => {
  const geometry = clone(CASES.good);
  geometry.cluster_titles[0].bounds = CASES.cluster_title_overlap.cluster_title_bounds;
  geometry.nodes[0].bounds = CASES.cluster_title_overlap.node_bounds;
  geometry.nodes[0].shape_bounds = CASES.cluster_title_overlap.node_bounds;

  const findings = classifyGeometry(geometry);

  assert.equal(findings.cluster_title_overlaps.length, 1);
  assert.equal(findings.cluster_title_overlaps[0].cluster_id, "cluster-main");
  assert.ok(
    findings.cluster_title_overlaps[0].clearance_px
      < MIN_CLUSTER_TITLE_CLEARANCE_PX,
  );
});


test("an unrelated edge within 10px of visible text is rejected", () => {
  const geometry = clone(CASES.good);
  geometry.visible_text.push(CASES.unrelated_edge_text_intersection.text);

  const findings = classifyGeometry(geometry);

  assert.equal(findings.unrelated_edge_text_intersections.length, 1);
  assert.equal(findings.unrelated_edge_text_intersections[0].edge_id, "edge-a-b");
  assert.equal(
    findings.unrelated_edge_text_intersections[0].text_id,
    "text-unrelated-note",
  );
  assert.equal(findings.unrelated_edge_text_intersections[0].intersects, true);
});


test("clearance rejects a closest approach between 2px sample endpoints", () => {
  const sampleEndpointClearance = Math.hypot(0.95, 10.96) - 1;
  assert.ok(sampleEndpointClearance >= MIN_UNRELATED_EDGE_TEXT_CLEARANCE_PX);

  const findings = classifyGeometry({
    precision_px: 0.01,
    visible_text: [{
      id: "text-between-samples",
      role: "text",
      owner_id: null,
      text: "Контроль",
      bounds: { x: 0, y: 0, width: 0.1, height: 1 },
    }],
    nodes: [],
    cluster_frames: [],
    cluster_titles: [],
    edge_paths: [{
      id: "edge-between-samples",
      visible: true,
      source_node_id: "source",
      target_node_id: "target",
      stroke_width_px: 2,
      sample_step_px: 2,
      samples: [
        { x: -0.95, y: 11.96 },
        { x: 1.05, y: 11.96 },
      ],
      comparison_samples: [
        { x: -0.95, y: 11.96 },
        { x: 1.05, y: 11.96 },
      ],
    }],
  });

  assert.equal(findings.unrelated_edge_text_intersections.length, 1);
  assert.equal(
    findings.unrelated_edge_text_intersections[0].edge_id,
    "edge-between-samples",
  );
  assert.ok(
    findings.unrelated_edge_text_intersections[0].clearance_px
      < MIN_UNRELATED_EDGE_TEXT_CLEARANCE_PX,
  );
});


test("a node label outside its shape is rejected", () => {
  const geometry = clone(CASES.good);
  geometry.nodes[0].label_bounds = CASES.node_label_overflow.label_bounds;

  const findings = classifyGeometry(geometry);

  assert.equal(findings.node_label_overflows.length, 1);
  assert.equal(findings.node_label_overflows[0].node_id, "node-a");
  assert.ok(findings.node_label_overflows[0].overflow_px.left > 0);
  assert.ok(findings.node_label_overflows[0].overflow_px.right > 0);
});


test("coincident visible edge routes are rejected", () => {
  const geometry = clone(CASES.good);
  geometry.edge_paths.push({
    ...clone(geometry.edge_paths[0]),
    ...CASES.duplicate_edge_route,
  });

  const findings = classifyGeometry(geometry);

  assert.deepEqual(findings.duplicate_edge_routes, [{
    edge_ids: ["edge-a-b", "edge-a-b-duplicate"],
    maximum_separation_px: 0,
  }]);
});


test("print type below 9.5pt and an unreviewed narrow aspect are failures", () => {
  const findings = assessPrintGeometry({
    effective_font_pt: 9.49,
    viewbox_aspect_ratio: 0.719,
    aspect_ratio_override: null,
  });

  assert.equal(findings.print_font_failures.length, 1);
  assert.equal(findings.aspect_ratio_failures.length, 1);
  assert.equal(findings.aspect_ratio_overrides.length, 0);
});


test("an explicit reviewed aspect override is allowed and reported", () => {
  const override = {
    reviewed_by: "layout-editor",
    reviewed_on: "2026-08-30",
    reason: "A narrow state ladder is intentionally placed on a full-height page.",
  };
  const findings = assessPrintGeometry({
    effective_font_pt: 9.5,
    viewbox_aspect_ratio: 0.7,
    aspect_ratio_override: override,
  });

  assert.equal(findings.print_font_failures.length, 0);
  assert.equal(findings.aspect_ratio_failures.length, 0);
  assert.deepEqual(findings.aspect_ratio_overrides, [{
    threshold: MIN_VIEWBOX_ASPECT_RATIO,
    actual: 0.7,
    review: override,
  }]);
});


test("layout classes select Dagre for simple flows and ELK for layered architecture", () => {
  assert.deepEqual(normalizeDiagramOptions({ filename: "simple.png" }), {
    layout_class: "simple-flow",
    layout_engine: "dagre",
    connector_style: "linear",
    connector_curve: "linear",
    feedback_loop_review: null,
    aspect_ratio_override: null,
  });
  assert.deepEqual(normalizeDiagramOptions({
    filename: "layered.png",
    layout_class: "layered-architecture",
    connector_style: "orthogonal",
  }), {
    layout_class: "layered-architecture",
    layout_engine: "elk",
    connector_style: "orthogonal",
    connector_curve: "step",
    feedback_loop_review: null,
    aspect_ratio_override: null,
  });
});


test("basis is available only through an explicit feedback-loop review", () => {
  assert.throws(
    () => normalizeDiagramOptions({
      filename: "unreviewed.png",
      connector_style: "basis",
    }),
    /connector_style/,
  );

  const review = {
    curve: "basis",
    reviewed_by: "layout-editor",
    reviewed_on: "2026-08-30",
    reason: "The only curved route is the reviewed feedback edge.",
  };
  const options = normalizeDiagramOptions({
    filename: "feedback.png",
    reviewed_feedback_loop: review,
  });
  assert.equal(options.connector_curve, "basis");
  assert.deepEqual(options.feedback_loop_review, review);
});


test("all production manifests remain valid with v2 defaults", () => {
  for (const filename of [
    "ru-inline-diagrams-2026-07-13.json",
    "ru-numbered-diagrams-2026-07-15.json",
    "ru-editorial-diagrams-2026-07-16.json",
  ]) {
    const manifest = JSON.parse(fs.readFileSync(
      path.join(ROOT, "docs/publisher", filename),
      "utf8",
    ));
    for (const diagram of manifest.diagrams) {
      const options = normalizeDiagramOptions(diagram);
      assert.equal(options.layout_class, "simple-flow");
      assert.equal(options.layout_engine, "dagre");
      assert.equal(options.connector_curve, "linear");
    }
  }
});
