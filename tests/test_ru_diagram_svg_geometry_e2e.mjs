import assert from "node:assert/strict";
import test from "node:test";

import { classifyGeometry } from "../docs/publisher/tools/ru_diagram_renderer_contract.mjs";
import { collectSvgGeometry } from "../docs/publisher/tools/ru_diagram_svg_geometry.mjs";
import {
  assertBrowserTestEnvironment,
  browserTestSkip,
  resolveBrowserTestEnvironment,
} from "./ru_diagram_test_environment.mjs";

const environment = resolveBrowserTestEnvironment();

const COLLECTION_OPTIONS = {
  decision_node_label_padding_px: 8,
  edge_sample_step_px: 2,
  route_comparison_sample_count: 33,
  curved_edge_ids: [],
};


async function withSvg(svg, callback, collectionOptions = COLLECTION_OPTIONS) {
  assertBrowserTestEnvironment(environment);
  const browser = await environment.chromium.launch({
    headless: true,
    executablePath: environment.chrome,
  });
  try {
    const page = await browser.newPage({ viewport: { width: 800, height: 600 } });
    await page.setContent(`<main>${svg}</main>`);
    const geometry = await page.locator("main > svg").evaluate(
      collectSvgGeometry,
      collectionOptions,
    );
    await callback(geometry);
  } finally {
    await browser.close();
  }
}


test("diamond and ellipse labels are checked against padded shape interiors", {
  skip: browserTestSkip(environment),
}, async () => {
  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 240">
      <g class="node" id="diamond-good">
        <polygon points="0,100 100,0 200,100 100,200" />
        <g class="label">
          <rect x="80" y="80" width="40" height="40" fill="none" />
          <text x="88" y="105" font-size="12">good</text>
        </g>
      </g>
      <g class="node" id="diamond-bad" transform="translate(220 0)">
        <polygon points="0,100 100,0 200,100 100,200" />
        <g class="label">
          <rect x="25" y="25" width="20" height="20" fill="none" />
          <text x="27" y="40" font-size="12">bad</text>
        </g>
      </g>
      <g class="node" id="ellipse-good" transform="translate(0 210)">
        <ellipse cx="100" cy="100" rx="100" ry="70" />
        <g class="label">
          <rect x="80" y="80" width="40" height="40" fill="none" />
          <text x="88" y="105" font-size="12">good</text>
        </g>
      </g>
      <g class="node" id="ellipse-bad" transform="translate(220 210)">
        <ellipse cx="100" cy="100" rx="100" ry="70" />
        <g class="label">
          <rect x="30" y="55" width="20" height="20" fill="none" />
          <text x="32" y="70" font-size="12">bad</text>
        </g>
      </g>
    </svg>`;

  await withSvg(svg, (geometry) => {
    const nodes = new Map(geometry.nodes.map((node) => [node.id, node]));
    assert.equal(nodes.get("diamond-good").label_containment.contained, true);
    assert.equal(nodes.get("diamond-good").label_containment.shape_type, "polygon");
    assert.equal(nodes.get("diamond-good").label_containment.padding_px, 8);
    assert.equal(nodes.get("ellipse-good").label_containment.padding_px, 12);
    assert.equal(nodes.get("diamond-bad").label_containment.contained, false);
    assert.ok(nodes.get("diamond-bad").label_containment.outside_boundary_sample_count > 0);
    assert.equal(nodes.get("ellipse-good").label_containment.contained, true);
    assert.equal(nodes.get("ellipse-good").label_containment.shape_type, "ellipse");
    assert.equal(nodes.get("ellipse-bad").label_containment.contained, false);
    assert.ok(nodes.get("ellipse-bad").label_containment.outside_boundary_sample_count > 0);

    assert.deepEqual(
      classifyGeometry(geometry).node_label_overflows.map((finding) => finding.node_id),
      ["diamond-bad", "ellipse-bad"],
    );
  });
});


test("adaptive curved segments catch a text approach between coarse path samples", {
  skip: browserTestSkip(environment),
}, async () => {
  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 100">
      <path class="flowchart-link" data-id="curved" d="M 10 80 C 45 0 115 0 150 80"
        fill="none" stroke="#000" stroke-width="2" />
      <foreignObject id="curve-text" x="65" y="12" width="30" height="20">
        <div xmlns="http://www.w3.org/1999/xhtml" style="font-size: 12px">Text</div>
      </foreignObject>
    </svg>`;
  const options = {
    ...COLLECTION_OPTIONS,
    edge_sample_step_px: 1000,
    curved_edge_ids: ["curved"],
    curve_segment_deviation_bound_px: 0.01,
  };

  await withSvg(svg, (geometry) => {
    const edge = geometry.edge_paths[0];
    const textBounds = geometry.visible_text[0].bounds;
    assert.equal(edge.samples.length, 2);
    assert.equal(edge.route_kind, "curved");
    assert.ok(edge.segments.length > 2);
    assert.ok(edge.segments.every((segment) => segment.deviation_bound_px <= 0.01));
    for (const point of edge.samples) {
      const dx = Math.max(textBounds.x - point.x, point.x - textBounds.x - textBounds.width, 0);
      const dy = Math.max(textBounds.y - point.y, point.y - textBounds.y - textBounds.height, 0);
      assert.ok(Math.hypot(dx, dy) - edge.stroke_width_px / 2 >= 10);
    }
    assert.deepEqual(
      classifyGeometry(geometry).unrelated_edge_text_intersections.map(
        (finding) => finding.edge_id,
      ),
      ["curved"],
    );
  }, options);
});


test("an edge label is owned by its DOM edge ID when an unlabeled edge precedes it", {
  skip: browserTestSkip(environment),
}, async () => {
  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 100">
      <g class="edgePaths">
        <path class="flowchart-link" data-id="edge-unlabeled" d="M 10 10 L 150 10"
          fill="none" stroke="#000" stroke-width="2" />
        <path class="flowchart-link" data-id="edge-owned" d="M 10 50 L 150 50"
          fill="none" stroke="#000" stroke-width="2" />
        <path class="flowchart-link" data-id="edge-unrelated" d="M 70 30 L 70 70"
          fill="none" stroke="#000" stroke-width="2" />
      </g>
      <g class="edgeLabels">
        <g class="edgeLabel">
          <g class="label" data-id="edge-owned">
            <text id="owned-label-text" x="50" y="54" font-size="12">Owned</text>
          </g>
        </g>
      </g>
    </svg>`;

  await withSvg(svg, (geometry) => {
    assert.equal(geometry.edge_labels.length, 1);
    assert.equal(geometry.edge_labels[0].edge_id, "edge-owned");
    const labelText = geometry.visible_text.find((item) => item.id === "owned-label-text");
    assert.equal(labelText.owner_id, "edge-owned");

    const labelFindings = classifyGeometry(geometry).unrelated_edge_text_intersections
      .filter((finding) => finding.text_id === "owned-label-text");
    assert.deepEqual(labelFindings.map((finding) => finding.edge_id), ["edge-unrelated"]);
  });
});
