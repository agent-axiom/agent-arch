import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import * as rendererContract from "../docs/publisher/tools/ru_diagram_renderer_contract.mjs";
import {
  assertBrowserTestEnvironment,
  browserTestSkip,
} from "./ru_diagram_test_environment.mjs";

const {
  BLOCK_PADDING_PX,
  DEFAULT_LABEL_WRAP_WIDTH_PX,
  DUPLICATE_ROUTE_MIN_OVERLAP_FRACTION,
  DUPLICATE_ROUTE_MIN_OVERLAP_LENGTH_PX,
  MIN_CLUSTER_TITLE_CLEARANCE_PX,
  MIN_EFFECTIVE_FONT_PT,
  MIN_UNRELATED_EDGE_TEXT_CLEARANCE_PX,
  MIN_VIEWBOX_ASPECT_RATIO,
  NODE_LABEL_PADDING_PX,
  VISUAL_STYLE_ID,
  assessPrintGeometry,
  classifyGeometry,
  measureClusterTitleClearances,
  normalizeDiagramOptions,
  normalizeMermaidSource,
  prepareMermaidSource,
} = rendererContract;

const TESTS_DIR = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(TESTS_DIR, "..");
const TASK_3B1_LAYOUT_CLASSES = new Map([
  ["ru-figure-13-autonomy-ladder.png", "simple-flow"],
  ["ru-figure-02-trust-boundaries.png", "simple-flow"],
  ["ru-figure-19-localhost-control-plane.png", "decision-state"],
  ["ru-figure-16-capability-endpoint-contract.png", "simple-flow"],
  ["ru-figure-06-approval-gateway.png", "decision-state"],
  ["ru-figure-25-memory-write-lifecycle.png", "decision-state"],
  ["ru-figure-05-memory-retrieval.png", "decision-state"],
  ["ru-figure-07-sandbox-mcp.png", "decision-state"],
  ["ru-figure-21-mcp-gateway.png", "decision-state"],
  ["ru-figure-08-idempotency-recovery.png", "decision-state"],
  ["ru-figure-20-eval-integrity.png", "evidence-overlay"],
]);
const FIXTURE_PATH = path.join(
  TESTS_DIR,
  "fixtures/ru_diagram_renderer/geometry-cases.json",
);
const CASES = JSON.parse(fs.readFileSync(FIXTURE_PATH, "utf8"));


function clone(value) {
  return JSON.parse(JSON.stringify(value));
}


function clearanceGeometry(clearancePx) {
  const textBounds = { x: 0, y: 0, width: 10, height: 10 };
  const strokeWidthPx = 2;
  const centerlineY = textBounds.height + clearancePx + strokeWidthPx / 2;
  const start = { x: -10, y: centerlineY };
  const end = { x: 20, y: centerlineY };
  return {
    precision_px: 0.01,
    visible_text: [{
      id: `text-${clearancePx}`,
      role: "text",
      owner_id: null,
      text: "Контроль",
      bounds: textBounds,
    }],
    nodes: [],
    cluster_frames: [],
    cluster_titles: [],
    edge_paths: [{
      id: `edge-${clearancePx}`,
      visible: true,
      source_node_id: "source",
      target_node_id: "target",
      stroke_width_px: strokeWidthPx,
      route_kind: "polyline",
      sampling_error_bound_px: 1,
      samples: [start, end],
      segments: [{ start, end, deviation_bound_px: 0 }],
      comparison_samples: [start, end],
    }],
  };
}


test("v2 constants enforce the print geometry floor", () => {
  assert.equal(VISUAL_STYLE_ID, "agent-arch-book-v2");
  assert.equal(MIN_EFFECTIVE_FONT_PT, 9.5);
  assert.equal(MIN_VIEWBOX_ASPECT_RATIO, 0.72);
  assert.equal(MIN_CLUSTER_TITLE_CLEARANCE_PX, 12);
  assert.equal(MIN_UNRELATED_EDGE_TEXT_CLEARANCE_PX, 10);
  assert.equal(NODE_LABEL_PADDING_PX, 12);
  assert.equal(BLOCK_PADDING_PX, 20);
  assert.ok(BLOCK_PADDING_PX > NODE_LABEL_PADDING_PX);
  assert.equal(DEFAULT_LABEL_WRAP_WIDTH_PX, 220);
  assert.equal(DUPLICATE_ROUTE_MIN_OVERLAP_LENGTH_PX, 24);
  assert.equal(DUPLICATE_ROUTE_MIN_OVERLAP_FRACTION, 0.25);
});


test("required CI browser dependencies fail instead of producing a skip", () => {
  const environment = {
    required: true,
    missing: ["Playwright module", "Mermaid bundle", "Chromium executable"],
  };

  assert.equal(browserTestSkip(environment), false);
  assert.throws(
    () => assertBrowserTestEnvironment(environment),
    /browser dependencies unavailable/,
  );
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


test("straight-route clearance rejects 9.9px and accepts exact 10.0px and 10.1px", () => {
  const below = classifyGeometry(clearanceGeometry(9.9));
  const exact = classifyGeometry(clearanceGeometry(10));
  const above = classifyGeometry(clearanceGeometry(10.1));

  assert.equal(below.unrelated_edge_text_intersections.length, 1);
  assert.equal(below.unrelated_edge_text_intersections[0].clearance_px, 9.9);
  assert.deepEqual(exact.unrelated_edge_text_intersections, []);
  assert.deepEqual(above.unrelated_edge_text_intersections, []);
});


test("a curved route approaching text between coarse samples is rejected", () => {
  const geometry = clearanceGeometry(10.1);
  const edge = geometry.edge_paths[0];
  const midpoint = { x: 5, y: 20.8 };
  edge.route_kind = "curved";
  edge.segments = [
    { start: edge.samples[0], end: midpoint, deviation_bound_px: 0.01 },
    { start: midpoint, end: edge.samples[1], deviation_bound_px: 0.01 },
  ];

  const findings = classifyGeometry(geometry);

  assert.equal(findings.unrelated_edge_text_intersections.length, 1);
  assert.equal(findings.unrelated_edge_text_intersections[0].edge_id, "edge-10.1");
  assert.equal(findings.unrelated_edge_text_intersections[0].clearance_px, 9.79);
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
    overlap_length_px: 140,
    overlap_fraction: 1,
    minimum_overlap_length_px: DUPLICATE_ROUTE_MIN_OVERLAP_LENGTH_PX,
    minimum_overlap_fraction: DUPLICATE_ROUTE_MIN_OVERLAP_FRACTION,
  }]);
});


test("routes that diverge after a long shared segment are rejected", () => {
  const geometry = clone(CASES.good);
  geometry.visible_text = [];
  geometry.nodes = [];
  geometry.cluster_frames = [];
  geometry.cluster_titles = [];
  geometry.edge_paths = [{
    id: "edge-left",
    visible: true,
    stroke_width_px: 2,
    samples: [
      { x: 0, y: 0 },
      { x: 60, y: 0 },
      { x: 100, y: 0 },
    ],
    comparison_samples: [],
  }, {
    id: "edge-right",
    visible: true,
    stroke_width_px: 2,
    samples: [
      { x: 0, y: 0 },
      { x: 60, y: 0 },
      { x: 100, y: 40 },
    ],
    comparison_samples: [],
  }];

  const findings = classifyGeometry(geometry);

  assert.deepEqual(findings.duplicate_edge_routes, [{
    edge_ids: ["edge-left", "edge-right"],
    overlap_length_px: 60,
    overlap_fraction: 0.6,
    minimum_overlap_length_px: DUPLICATE_ROUTE_MIN_OVERLAP_LENGTH_PX,
    minimum_overlap_fraction: DUPLICATE_ROUTE_MIN_OVERLAP_FRACTION,
  }]);
});


test("print type below 9.5pt and an unreviewed narrow aspect are failures", () => {
  const findings = assessPrintGeometry({
    effective_font_pt: 9.49,
    viewbox_width: 719,
    viewbox_height: 1000,
    aspect_ratio_override: null,
  });

  assert.equal(findings.print_font_failures.length, 1);
  assert.equal(findings.aspect_ratio_failures.length, 1);
  assert.equal(findings.aspect_ratio_overrides.length, 0);
});


test("raw viewBox aspect fails below 0.72 before its report value is rounded", () => {
  const belowBoundary = assessPrintGeometry({
    effective_font_pt: 9.5,
    viewbox_width: 719.568345323741,
    viewbox_height: 1000,
    aspect_ratio_override: null,
  });
  const atBoundary = assessPrintGeometry({
    effective_font_pt: 9.5,
    viewbox_width: 720,
    viewbox_height: 1000,
    aspect_ratio_override: null,
  });

  assert.equal(belowBoundary.viewbox_aspect_ratio, 0.72);
  assert.deepEqual(belowBoundary.aspect_ratio_failures, [{
    threshold: MIN_VIEWBOX_ASPECT_RATIO,
    actual: 0.72,
  }]);
  assert.equal(atBoundary.viewbox_aspect_ratio, 0.72);
  assert.deepEqual(atBoundary.aspect_ratio_failures, []);
});


test("an explicit reviewed aspect override is allowed and reported", () => {
  const override = {
    reviewed_by: "layout-editor",
    reviewed_on: "2026-08-30",
    reason: "A narrow state ladder is intentionally placed on a full-height page.",
  };
  const findings = assessPrintGeometry({
    effective_font_pt: 9.5,
    viewbox_width: 700,
    viewbox_height: 1000,
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


test("layout classes reserve ELK for layered architecture", () => {
  assert.deepEqual(normalizeDiagramOptions({ filename: "simple.png" }), {
    layout_class: "simple-flow",
    layout_engine: "dagre",
    connector_style: "linear",
    connector_curve: "linear",
    label_wrap_width_px: 220,
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
    label_wrap_width_px: 220,
    feedback_loop_review: null,
    aspect_ratio_override: null,
  });
  for (const layoutClass of ["decision-state", "evidence-overlay"]) {
    assert.deepEqual(normalizeDiagramOptions({
      filename: `${layoutClass}.png`,
      layout_class: layoutClass,
    }), {
      layout_class: layoutClass,
      layout_engine: "dagre",
      connector_style: "linear",
      connector_curve: "linear",
      label_wrap_width_px: 220,
      feedback_loop_review: null,
      aspect_ratio_override: null,
    });
  }
});


test("a bounded per-diagram label wrap width preserves whole technical terms", () => {
  assert.equal(normalizeDiagramOptions({
    filename: "wide-label.png",
    label_wrap_width_px: 240,
  }).label_wrap_width_px, 240);
  for (const value of [159, 321, 220.5, "240"]) {
    assert.throws(
      () => normalizeDiagramOptions({
        filename: "invalid-label-width.png",
        label_wrap_width_px: value,
      }),
      /label_wrap_width_px/,
    );
  }
});


test("a reviewed feedback loop keeps the global curve linear and targets one edge ID", () => {
  assert.throws(
    () => normalizeDiagramOptions({
      filename: "unreviewed.png",
      connector_style: "basis",
    }),
    /connector_style/,
  );

  const review = {
    edge_id: "feedback",
    curve: "basis",
    reviewed_by: "layout-editor",
    reviewed_on: "2026-08-30",
    reason: "The only curved route is the reviewed feedback edge.",
  };
  const diagram = {
    filename: "feedback.png",
    mermaid: "flowchart LR\nA main@--> B\nB feedback@--> A",
    reviewed_feedback_loop: review,
  };
  const options = normalizeDiagramOptions(diagram);
  assert.equal(options.connector_curve, "linear");
  assert.deepEqual(options.feedback_loop_review, review);
  assert.match(prepareMermaidSource(diagram, options), /feedback@\{ curve: basis \}$/);
});


test("feedback-loop reviews reject missing, multiple, and unidentified edge declarations", () => {
  const review = {
    edge_id: "feedback",
    curve: "basis",
    reviewed_by: "layout-editor",
    reviewed_on: "2026-08-30",
    reason: "The feedback edge needs a distinct return route.",
  };
  const mermaid = "flowchart LR\nA main@--> B\nB feedback@--> A";

  assert.throws(
    () => normalizeDiagramOptions({
      filename: "missing-id.png",
      mermaid,
      reviewed_feedback_loop: { ...review, edge_id: undefined },
    }),
    /reviewed_feedback_loop\.edge_id/,
  );
  assert.throws(
    () => normalizeDiagramOptions({
      filename: "multiple-reviews.png",
      mermaid,
      reviewed_feedback_loop: [review, { ...review, edge_id: "main" }],
    }),
    /must be an object/,
  );
  assert.throws(
    () => normalizeDiagramOptions({
      filename: "unidentified.png",
      mermaid,
      reviewed_feedback_loop: { ...review, edge_id: "not-declared" },
    }),
    /does not identify an edge declared in Mermaid source/,
  );
  assert.throws(
    () => normalizeDiagramOptions({
      filename: "duplicate-id.png",
      mermaid: `${mermaid}\nC feedback@--> D`,
      reviewed_feedback_loop: review,
    }),
    /must identify exactly one Mermaid edge declaration/,
  );
});


test("leading and embedded Mermaid init/config directives are rejected before normalization", () => {
  for (const source of [
    "%%{init: { 'flowchart': { 'curve': 'basis' } }}%%\nflowchart LR\nA --> B",
    "%%{ config: { 'theme': 'dark' } }%%\nflowchart LR\nA --> B",
    "flowchart LR\nA --> B\n%%{init: { 'theme': 'dark' }}%%",
    "flowchart LR\n%%{ config: { 'flowchart': { 'curve': 'basis' } } }%%\nA --> B",
  ]) {
    assert.throws(
      () => normalizeMermaidSource(source, "directive.png"),
      /local Mermaid configuration is not allowed/,
    );
  }
});


test("all production manifests preserve the exact Task 3B1 layout classifications", () => {
  const seenTask3B1 = new Map();
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
      if (diagram.filename === "ru-figure-03-reference-architecture.png") {
        assert.equal(options.layout_class, "layered-architecture");
        assert.equal(options.layout_engine, "elk");
        assert.equal(options.connector_curve, "step");
      } else if (TASK_3B1_LAYOUT_CLASSES.has(diagram.filename)) {
        const expectedClass = TASK_3B1_LAYOUT_CLASSES.get(diagram.filename);
        assert.equal(options.layout_class, expectedClass);
        assert.equal(options.layout_engine, "dagre");
        assert.equal(options.connector_curve, "linear");
        seenTask3B1.set(diagram.filename, expectedClass);
      } else {
        assert.equal(options.layout_class, "simple-flow");
        assert.equal(options.layout_engine, "dagre");
        assert.equal(options.connector_curve, "linear");
      }
    }
  }
  assert.deepEqual(seenTask3B1, TASK_3B1_LAYOUT_CLASSES);
});
