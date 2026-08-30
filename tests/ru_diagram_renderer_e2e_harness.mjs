import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

import {
  MERMAID_SHA256,
  MERMAID_VERSION,
  VISUAL_STYLE_ID,
} from "../docs/publisher/tools/ru_diagram_renderer_contract.mjs";

const TESTS_DIR = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(TESTS_DIR, "..");
const RENDERER = path.join(
  ROOT,
  "docs/publisher/tools/render_ru_inline_diagrams.mjs",
);
const FIXTURE_DIR = path.join(TESTS_DIR, "fixtures/ru_diagram_renderer");
const GOOD_MANIFEST = path.join(FIXTURE_DIR, "good-manifest.json");
const DEFECTIVE_MANIFEST = path.join(FIXTURE_DIR, "defective-manifest.json");
const INVALID_FEEDBACK_MANIFEST = path.join(
  FIXTURE_DIR,
  "invalid-feedback-manifest.json",
);


function invokeRenderer({ manifest, mermaidJs, chrome, outputDir, reportPath }) {
  const childArgs = [
    RENDERER,
    "--manifest", manifest,
    "--mermaid-js", mermaidJs,
    "--output-dir", outputDir,
    "--chrome", chrome,
    "--report-json", reportPath,
  ];
  return new Promise((resolve, reject) => {
    const child = spawn(process.execPath, childArgs, {
      cwd: ROOT,
      env: process.env,
      stdio: ["ignore", "pipe", "pipe"],
    });
    let stdout = "";
    let stderr = "";
    child.stdout.setEncoding("utf8");
    child.stderr.setEncoding("utf8");
    child.stdout.on("data", (chunk) => { stdout += chunk; });
    child.stderr.on("data", (chunk) => { stderr += chunk; });
    child.on("error", reject);
    child.on("close", (status, signal) => resolve({ status, signal, stdout, stderr }));
  });
}


async function readJson(filename) {
  return JSON.parse(await fs.readFile(filename, "utf8"));
}


async function pathExists(filename) {
  try {
    await fs.access(filename);
    return true;
  } catch {
    return false;
  }
}


function assertReportContract(report, expectedCount) {
  assert.equal(report.schema_version, 2);
  assert.equal(report.visual_style, VISUAL_STYLE_ID);
  assert.deepEqual(report.mermaid, {
    version: MERMAID_VERSION,
    sha256: MERMAID_SHA256,
  });
  assert.equal(report.rendered, expectedCount);
  assert.equal(report.results.length, expectedCount);
}


async function assertSvgGeometryStage(outputDir, result) {
  const svgPath = path.join(outputDir, result.svg);
  const pngPath = path.join(outputDir, result.png);
  assert.ok(await pathExists(svgPath), `${result.filename}: renderer did not write SVG`);
  assert.ok(await pathExists(pngPath), `${result.filename}: renderer did not write PNG`);
  const svg = await fs.readFile(svgPath, "utf8");
  assert.match(svg, /^<svg\b/);
  assert.match(svg, new RegExp(`data-visual-style="${VISUAL_STYLE_ID}"`));
  assert.equal(result.geometry.coordinate_space, "svg-viewbox-px");
  assert.equal(result.geometry.precision_px, 0.01);
  assert.ok(result.geometry.visible_text.length > 0);
  assert.ok(result.geometry.nodes.length > 0);
  assert.ok(Array.isArray(result.geometry.edge_paths));
  assert.equal(typeof result.geometry.findings, "object");
  assert.equal(typeof result.findings, "object");
}


async function runGoodFixture({ mermaidJs, chrome, tempRoot }) {
  const outputDir = path.join(tempRoot, "good");
  const reportPath = path.join(tempRoot, "good-report.json");
  const run = await invokeRenderer({
    manifest: GOOD_MANIFEST,
    mermaidJs,
    chrome,
    outputDir,
    reportPath,
  });
  assert.equal(
    run.status,
    0,
    `good manifest renderer failed before success:\n${run.stderr}`,
  );
  assert.equal(run.signal, null);
  const report = await readJson(reportPath);
  assert.deepEqual(JSON.parse(run.stdout), report);
  assertReportContract(report, 3);
  assert.deepEqual(report.violations, []);
  assert.deepEqual(
    report.results.map((result) => result.layout_engine),
    ["dagre", "elk", "dagre"],
  );
  for (const result of report.results) {
    await assertSvgGeometryStage(outputDir, result);
    assert.deepEqual(result.violations, []);
  }
  const feedbackResult = report.results.find(
    (result) => result.filename === "fixture-good-reviewed-feedback.png",
  );
  assert.ok(feedbackResult, "good fixture report lacks the reviewed feedback diagram");
  assert.equal(feedbackResult.connector_curve, "linear");
  assert.equal(feedbackResult.feedback_loop_review.edge_id, "feedback");
  assert.equal(
    feedbackResult.geometry.edge_paths.find((edge) => edge.id === "feedback")?.route_kind,
    "curved",
  );
  assert.ok(
    feedbackResult.geometry.edge_paths
      .filter((edge) => edge.id !== "feedback")
      .every((edge) => edge.route_kind === "polyline"),
    "a non-reviewed feedback edge was rendered as curved",
  );
  return {
    layoutEngines: report.results.map((result) => result.layout_engine),
    reviewedFeedbackEdgeIds: [feedbackResult.feedback_loop_review.edge_id],
  };
}


async function runDefectiveFixtures({ mermaidJs, chrome, tempRoot }) {
  const manifest = await readJson(DEFECTIVE_MANIFEST);
  assert.equal(manifest.diagrams.length, manifest.expected_count);
  const findings = [];
  for (const diagram of manifest.diagrams) {
    const expectedFinding = diagram.fixture_expected_finding;
    assert.equal(typeof expectedFinding, "string");
    const stem = path.parse(diagram.filename).name;
    const caseRoot = path.join(tempRoot, "defective", stem);
    const outputDir = path.join(caseRoot, "output");
    const manifestPath = path.join(caseRoot, "manifest.json");
    const reportPath = path.join(caseRoot, "report.json");
    await fs.mkdir(caseRoot, { recursive: true });
    await fs.writeFile(manifestPath, `${JSON.stringify({
      expected_count: 1,
      diagrams: [diagram],
    }, null, 2)}\n`, "utf8");

    const run = await invokeRenderer({
      manifest: manifestPath,
      mermaidJs,
      chrome,
      outputDir,
      reportPath,
    });
    assert.notEqual(run.status, 0, `${diagram.filename}: defective fixture exited zero`);
    assert.equal(run.signal, null, `${diagram.filename}: renderer ended from ${run.signal}`);
    assert.ok(
      await pathExists(reportPath),
      `${diagram.filename}: renderer failed before writing its report:\n${run.stderr}`,
    );
    const report = await readJson(reportPath);
    assert.deepEqual(JSON.parse(run.stdout), report);
    assertReportContract(report, 1);
    await assertSvgGeometryStage(outputDir, report.results[0]);
    assert.ok(report.violations.length > 0);
    assert.ok(Array.isArray(report.findings[expectedFinding]));
    assert.ok(
      report.findings[expectedFinding].some((finding) => (
        finding.filename === diagram.filename
      )),
      `${diagram.filename}: report lacks ${expectedFinding}`,
    );
    assert.ok(report.results[0].findings[expectedFinding].length > 0);
    if (diagram.filename === "fixture-bad-edge-text.png") {
      const result = report.results[0];
      const ownedLabel = result.geometry.edge_labels.find(
        (label) => label.edge_id === "labeled",
      );
      assert.ok(ownedLabel, "labeled edge lacks stable DOM ownership");
      const labelFindings = result.findings.unrelated_edge_text_intersections.filter(
        (finding) => finding.text_id === ownedLabel.text_id,
      );
      assert.ok(labelFindings.some((finding) => finding.edge_id === "unrelated"));
      assert.ok(labelFindings.every((finding) => finding.edge_id !== "labeled"));
    }
    assert.match(run.stderr, /print-readability violations/);
    findings.push(expectedFinding);
  }
  return findings;
}


async function runInvalidFeedbackFixtures({ mermaidJs, chrome, tempRoot }) {
  const manifest = await readJson(INVALID_FEEDBACK_MANIFEST);
  assert.equal(manifest.diagrams.length, manifest.expected_count);
  const rejectedFilenames = [];
  for (const diagram of manifest.diagrams) {
    const caseRoot = path.join(tempRoot, "invalid-feedback", path.parse(diagram.filename).name);
    const outputDir = path.join(caseRoot, "output");
    const manifestPath = path.join(caseRoot, "manifest.json");
    const reportPath = path.join(caseRoot, "report.json");
    await fs.mkdir(caseRoot, { recursive: true });
    await fs.writeFile(manifestPath, `${JSON.stringify({
      expected_count: 1,
      diagrams: [diagram],
    }, null, 2)}\n`, "utf8");

    const run = await invokeRenderer({
      manifest: manifestPath,
      mermaidJs,
      chrome,
      outputDir,
      reportPath,
    });
    assert.notEqual(run.status, 0, `${diagram.filename}: invalid review exited zero`);
    assert.equal(run.signal, null, `${diagram.filename}: renderer ended from ${run.signal}`);
    assert.equal(
      await pathExists(reportPath),
      false,
      `${diagram.filename}: invalid review reached geometry reporting`,
    );
    assert.match(run.stderr, new RegExp(diagram.fixture_expected_error));
    rejectedFilenames.push(diagram.filename);
  }
  return rejectedFilenames;
}


export async function runFixtureHarness({ mermaidJs, chrome }) {
  assert.ok(mermaidJs, "MERMAID_JS or --mermaid-js is required");
  assert.ok(chrome, "CHROME or --chrome is required");
  const resolvedMermaidJs = path.resolve(mermaidJs);
  const resolvedChrome = path.resolve(chrome);
  assert.ok(await pathExists(resolvedMermaidJs), `Mermaid bundle not found: ${resolvedMermaidJs}`);
  assert.ok(await pathExists(resolvedChrome), `Chrome executable not found: ${resolvedChrome}`);

  const tempRoot = await fs.mkdtemp(path.join(os.tmpdir(), "ru-diagram-renderer-e2e-"));
  try {
    const good = await runGoodFixture({
      mermaidJs: resolvedMermaidJs,
      chrome: resolvedChrome,
      tempRoot,
    });
    const defectiveFindings = await runDefectiveFixtures({
      mermaidJs: resolvedMermaidJs,
      chrome: resolvedChrome,
      tempRoot,
    });
    const invalidFeedbackFixtures = await runInvalidFeedbackFixtures({
      mermaidJs: resolvedMermaidJs,
      chrome: resolvedChrome,
      tempRoot,
    });
    return {
      good_diagrams: good.layoutEngines.length,
      good_layout_engines: good.layoutEngines,
      reviewed_feedback_edge_ids: good.reviewedFeedbackEdgeIds,
      defective_fixtures: defectiveFindings.length,
      defective_findings: defectiveFindings,
      invalid_feedback_fixtures: invalidFeedbackFixtures,
    };
  } finally {
    await fs.rm(tempRoot, { recursive: true, force: true });
  }
}


function parseCliArgs(argv) {
  const values = {
    mermaidJs: process.env.MERMAID_JS,
    chrome: process.env.CHROME,
  };
  for (let index = 2; index < argv.length; index += 2) {
    const key = argv[index];
    const value = argv[index + 1];
    if (!value || !["--mermaid-js", "--chrome"].includes(key)) {
      throw new Error(`Invalid argument near ${key}`);
    }
    values[key === "--mermaid-js" ? "mermaidJs" : "chrome"] = value;
  }
  return values;
}


const invokedPath = process.argv[1] ? path.resolve(process.argv[1]) : null;
if (invokedPath === fileURLToPath(import.meta.url)) {
  try {
    const summary = await runFixtureHarness(parseCliArgs(process.argv));
    process.stdout.write(`${JSON.stringify(summary, null, 2)}\n`);
  } catch (error) {
    process.stderr.write(`${error.stack ?? error}\n`);
    process.exitCode = 1;
  }
}
