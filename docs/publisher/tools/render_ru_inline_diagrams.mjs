import fs from "node:fs/promises";
import { createRequire } from "node:module";
import path from "node:path";
import process from "node:process";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");
const sharp = require("sharp");

const VISUAL_STYLE_ID = "agent-arch-book-v1";
const MIN_EFFECTIVE_FONT_PT = 8.5;
const MIN_VIEWBOX_ASPECT_RATIO = 0.72;
const MIN_CLUSTER_TITLE_GAP_PX = 12;
const PRINT_MAX_WIDTH_INCHES = 6.5;
const PRINT_MAX_HEIGHT_INCHES = 6.3;
const PNG_DENSITY = 300;

const UNIFIED_SVG_STYLE = `
  <style data-visual-style="${VISUAL_STYLE_ID}">
    svg { background: #ffffff; }
    .node rect, .node circle, .node ellipse, .node polygon, .node path {
      stroke-width: 2.2px !important;
    }
    .node rect { rx: 10px; ry: 10px; }
    .node polygon {
      fill: #fff4cc !important;
      stroke: #9b7a14 !important;
    }
    .nodeLabel, .label text {
      fill: #1f2a3d !important;
      font-weight: 600 !important;
    }
    .edgeLabel, .edgeLabel text {
      color: #36465d !important;
      fill: #36465d !important;
      font-size: 26px !important;
    }
    .edgeLabel rect, .labelBkg { fill: #ffffff !important; opacity: 0.96 !important; }
    .flowchart-link, .edgePath path {
      stroke: #5e6b7d !important;
      stroke-width: 2.2px !important;
    }
    marker path { fill: #5e6b7d !important; stroke: #5e6b7d !important; }
    .cluster rect {
      fill: #f7f9fc !important;
      stroke: #b7c4d6 !important;
      stroke-width: 1.6px !important;
      rx: 12px;
      ry: 12px;
    }
    .cluster-label text, .cluster-label span {
      color: #26364d !important;
      fill: #26364d !important;
      font-size: 26px !important;
      font-weight: 700 !important;
    }
  </style>`;


function parseArgs(argv) {
  const values = {};
  for (let index = 2; index < argv.length; index += 2) {
    const key = argv[index];
    const value = argv[index + 1];
    if (key === "--manifest") {
      values[key] ??= [];
      values[key].push(value);
    } else {
      values[key] = value;
    }
  }
  const required = ["--manifest", "--mermaid-js", "--output-dir"];
  for (const key of required) {
    if (!values[key]) throw new Error(`Missing required argument: ${key}`);
  }
  return values;
}


function escapeXml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&apos;");
}


function wrapLabel(value, maxCharacters = 22) {
  const wrappedLines = [];
  for (const originalLine of value.split("\\n")) {
    const words = originalLine.trim().split(/\s+/).filter(Boolean);
    if (words.length === 0) {
      wrappedLines.push("");
      continue;
    }
    let line = words.shift();
    for (const word of words) {
      if (`${line} ${word}`.length <= maxCharacters) {
        line = `${line} ${word}`;
      } else {
        wrappedLines.push(line);
        line = word;
      }
    }
    wrappedLines.push(line);
  }
  return wrappedLines.join("\\n");
}


function wrapMermaidLabels(source, maxCharacters) {
  return source
    .split("\n")
    .map((line) => {
      if (/^\s*subgraph\b/.test(line)) return line;
      return line.replaceAll(
        /"([^"\r\n]*)"/g,
        (_match, label) => `"${wrapLabel(label, maxCharacters)}"`,
      );
    })
    .join("\n");
}


function normalizeMermaidSource(source) {
  const withoutLocalTheme = source.replace(/^\s*%%\{init:.*?\}%%\s*/s, "");
  return wrapMermaidLabels(withoutLocalTheme.trim(), 22);
}


function calculateEffectiveFontPt(svg, metadata, sourceFontSize) {
  const viewBox = svg.match(/viewBox="[^"\s]+\s+[^"\s]+\s+([0-9.]+)\s+([0-9.]+)"/);
  if (!viewBox || !Number.isFinite(sourceFontSize) || !metadata.width) {
    throw new Error("Cannot calculate effective print font size from rendered diagram");
  }

  const viewWidth = Number(viewBox[1]);
  const viewHeight = Number(viewBox[2]);
  const placedWidthInches = Math.min(
    PRINT_MAX_WIDTH_INCHES,
    metadata.width / PNG_DENSITY,
    PRINT_MAX_HEIGHT_INCHES * viewWidth / viewHeight,
  );
  return sourceFontSize * placedWidthInches * 72 / viewWidth;
}


async function renderDiagram(page, diagram, outputDir) {
  const rendered = await page.evaluate(async ({ id, source }) => {
    const result = await window.mermaid.render(id, source);
    return result.svg;
  }, {
    id: path.parse(diagram.filename).name.replaceAll(/[^A-Za-z0-9_-]/g, "-"),
    source: normalizeMermaidSource(diagram.mermaid),
  });

  const title = `<title>${escapeXml(diagram.caption)}</title>`;
  const xmlSafeRendered = rendered.replaceAll(/<br\s*>/g, "<br/>");
  const initialSvg = xmlSafeRendered.replace(
    /<svg([^>]*)>/,
    `<svg$1 data-visual-style="${VISUAL_STYLE_ID}">${title}${UNIFIED_SVG_STYLE}`,
  );
  const stem = path.parse(diagram.filename).name;
  const svgPath = path.join(outputDir, `${stem}.svg`);
  const pngPath = path.join(outputDir, diagram.filename);

  await page.evaluate((svgMarkup) => {
    document.body.innerHTML = `<main id="diagram">${svgMarkup}</main>`;
    document.documentElement.style.background = "#ffffff";
    document.body.style.margin = "0";
    document.body.style.background = "#ffffff";
    const element = document.querySelector("#diagram > svg");
    element.style.display = "block";
    element.style.maxWidth = "none";
  }, initialSvg);
  await page.locator("#diagram > svg").evaluate((element) => {
    const root = element.querySelector(".root");
    if (!root) return;
    const edgePaths = [...element.querySelectorAll(".flowchart-link")];
    const countEdgeIntersections = (labelBounds) => edgePaths.reduce((count, pathElement) => {
      const length = pathElement.getTotalLength();
      const matrix = pathElement.getScreenCTM();
      if (!matrix || length === 0) return count;
      for (let offset = 0; offset <= length; offset += 2) {
        const localPoint = pathElement.getPointAtLength(offset);
        const point = new DOMPoint(localPoint.x, localPoint.y).matrixTransform(matrix);
        if (
          point.x >= labelBounds.left - 3
          && point.x <= labelBounds.right + 3
          && point.y >= labelBounds.top - 3
          && point.y <= labelBounds.bottom + 3
        ) return count + 1;
      }
      return count;
    }, 0);
    for (const cluster of element.querySelectorAll(".cluster")) {
      const label = cluster.querySelector(":scope > .cluster-label");
      if (!label) continue;
      const text = label.querySelector("text, foreignObject");
      if (!text || !(label.textContent ?? "").trim()) continue;
      const bounds = text.getBBox();
      const frame = cluster.querySelector(":scope > rect");
      if (!frame) continue;
      let background = label.querySelector(":scope > rect.background");
      if (!background) {
        background = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        background.setAttribute("class", "background");
        label.prepend(background);
      }
      background.setAttribute("x", String(bounds.x - 7));
      background.setAttribute("y", String(bounds.y - 4));
      background.setAttribute("width", String(bounds.width + 14));
      background.setAttribute("height", String(bounds.height + 6));
      background.setAttribute("rx", "4");
      background.setAttribute("fill", "#f7f9fc");
      background.setAttribute("stroke", "none");
      label.dataset.clusterId = cluster.id;
      label.dataset.opaqueBackground = "true";
      root.append(label);

      const frameBounds = frame.getBBox();
      const top = frameBounds.y + 8 - bounds.y;
      const candidates = [
        frameBounds.x + 14 - bounds.x,
        frameBounds.x + frameBounds.width - bounds.width - 14 - bounds.x,
        frameBounds.x + (frameBounds.width - bounds.width) / 2 - bounds.x,
      ];
      const placements = candidates.map((left, preference) => {
        label.setAttribute("transform", `translate(${left} ${top})`);
        const labelBounds = label.getBoundingClientRect();
        return {
          left,
          preference,
          intersections: countEdgeIntersections(labelBounds),
        };
      });
      placements.sort((left, right) => (
        left.intersections - right.intersections
        || left.preference - right.preference
      ));
      label.setAttribute("transform", `translate(${placements[0].left} ${top})`);
    }
  });
  const svg = await page.locator("#diagram > svg").evaluate((element) => element.outerHTML);
  const standaloneSvg = svg.replaceAll(/<br\s*>/g, "<br/>");
  await fs.writeFile(svgPath, `${standaloneSvg}\n`, "utf8");
  const geometryAudit = await page.locator("#diagram > svg").evaluate((element) => {
    const nodes = [...element.querySelectorAll(".node")].map((node) => ({
      element: node,
      bounds: node.getBoundingClientRect(),
    }));
    const clusterLabels = [...element.querySelectorAll(".cluster-label[data-cluster-id]")].flatMap((label) => {
      if (!(label.textContent ?? "").trim()) return [];
      const cluster = element.querySelector(`#${CSS.escape(label.dataset.clusterId)}`);
      if (!cluster) return [];
      const frame = cluster.querySelector(":scope > rect");
      if (!frame || !label) return [];
      const frameBounds = frame.getBoundingClientRect();
      const labelBounds = label.getBoundingClientRect();
      const containedNodes = nodes.filter(({ bounds }) => {
        const centerX = bounds.left + bounds.width / 2;
        const centerY = bounds.top + bounds.height / 2;
        return (
          centerX >= frameBounds.left
          && centerX <= frameBounds.right
          && centerY >= frameBounds.top
          && centerY <= frameBounds.bottom
        );
      });
      if (containedNodes.length === 0) return [];
      const gap = Math.min(...containedNodes.map(({ bounds }) => bounds.top)) - labelBounds.bottom;
      return [{
        cluster: cluster.id || label.textContent.trim(),
        bounds: labelBounds,
        gap_px: Number(gap.toFixed(2)),
        opaque_background: label.dataset.opaqueBackground === "true",
      }];
    });
    const edgeTitleIntersections = [];
    for (const pathElement of element.querySelectorAll(".flowchart-link")) {
      const length = pathElement.getTotalLength();
      const matrix = pathElement.getScreenCTM();
      if (!matrix || length === 0) continue;
      for (let offset = 0; offset <= length; offset += 2) {
        const localPoint = pathElement.getPointAtLength(offset);
        const point = new DOMPoint(localPoint.x, localPoint.y).matrixTransform(matrix);
        const crossedLabel = clusterLabels.find(({ bounds }) => (
          point.x >= bounds.left - 3
          && point.x <= bounds.right + 3
          && point.y >= bounds.top - 3
          && point.y <= bounds.bottom + 3
        ));
        if (!crossedLabel) continue;
        edgeTitleIntersections.push({
          cluster: crossedLabel.cluster,
          edge: pathElement.id || "unnamed-edge",
        });
        break;
      }
    }
    const nodeLabelOverflows = nodes.flatMap(({ element: node }) => {
      const shape = node.querySelector(
        ":scope > rect, :scope > circle, :scope > ellipse, :scope > polygon, :scope > path",
      );
      const label = node.querySelector(":scope > .label");
      if (!shape || !label) return [];
      const shapeBounds = shape.getBoundingClientRect();
      const labelBounds = label.getBoundingClientRect();
      const intrinsicLabelOverflow = [...label.querySelectorAll("foreignObject div")].some(
        (content) => (
          content.scrollWidth > content.clientWidth + 1
          || content.scrollHeight > content.clientHeight + 1
        ),
      );
      const tolerance = 2;
      if (
        !intrinsicLabelOverflow
        &&
        labelBounds.left >= shapeBounds.left - tolerance
        && labelBounds.right <= shapeBounds.right + tolerance
        && labelBounds.top >= shapeBounds.top - tolerance
        && labelBounds.bottom <= shapeBounds.bottom + tolerance
      ) return [];
      return [{
        node: node.id || label.textContent.trim(),
        intrinsic_clip: intrinsicLabelOverflow,
        overflow_px: {
          left: Number(Math.max(0, shapeBounds.left - labelBounds.left).toFixed(2)),
          right: Number(Math.max(0, labelBounds.right - shapeBounds.right).toFixed(2)),
          top: Number(Math.max(0, shapeBounds.top - labelBounds.top).toFixed(2)),
          bottom: Number(Math.max(0, labelBounds.bottom - shapeBounds.bottom).toFixed(2)),
        },
      }];
    });
    return {
      cluster_title_gaps: clusterLabels.map(({ bounds: _bounds, ...cluster }) => cluster),
      edge_title_intersections: edgeTitleIntersections,
      node_label_overflows: nodeLabelOverflows,
    };
  });
  const sourceFontSize = await page.locator("#diagram > svg").evaluate((element) => {
    const sizes = [...element.querySelectorAll("text, foreignObject span")]
      .filter((node) => (node.textContent ?? "").trim())
      .map((node) => Number.parseFloat(getComputedStyle(node).fontSize))
      .filter((size) => Number.isFinite(size) && size > 0);
    return Math.min(...sizes);
  });
  const screenshot = await page.locator("#diagram > svg").screenshot({
    animations: "disabled",
    omitBackground: false,
  });

  const trimmed = await sharp(screenshot)
    .flatten({ background: "#ffffff" })
    .removeAlpha()
    .trim({ background: "#ffffff", threshold: 8 })
    .toBuffer();
  const resized = await sharp(trimmed)
    .resize({
      width: 2400,
      height: 1800,
      fit: "inside",
      withoutEnlargement: false,
    })
    .toBuffer();
  await sharp(resized)
    .extend({
      top: 32,
      bottom: 32,
      left: 32,
      right: 32,
      background: "#ffffff",
    })
    .flatten({ background: "#ffffff" })
    .removeAlpha()
    .png({ compressionLevel: 9, adaptiveFiltering: true })
    .withMetadata({ density: PNG_DENSITY })
    .toFile(pngPath);

  const metadata = await sharp(pngPath).metadata();
  if (
    !metadata.width
    || !metadata.height
    || metadata.width > 2496
    || metadata.height > 1896
    || metadata.hasAlpha
  ) {
    throw new Error(`Invalid PNG output for ${diagram.filename}: ${JSON.stringify(metadata)}`);
  }
  const effectiveFontPt = calculateEffectiveFontPt(svg, metadata, sourceFontSize);
  const violations = [];
  const warnings = [];
  if (effectiveFontPt < MIN_EFFECTIVE_FONT_PT) {
    violations.push(
      `effective font ${effectiveFontPt.toFixed(2)}pt is below ${MIN_EFFECTIVE_FONT_PT}pt`,
    );
  }
  const viewBox = svg.match(/viewBox="[^"\s]+\s+[^"\s]+\s+([0-9.]+)\s+([0-9.]+)"/);
  if (!viewBox) throw new Error(`Missing viewBox for ${diagram.filename}`);
  const aspectRatio = Number(viewBox[1]) / Number(viewBox[2]);
  if (aspectRatio < MIN_VIEWBOX_ASPECT_RATIO) {
    warnings.push(
      `manual review: viewBox aspect ${aspectRatio.toFixed(3)} is below `
      + `${MIN_VIEWBOX_ASPECT_RATIO}`,
    );
  }
  for (const cluster of geometryAudit.cluster_title_gaps) {
    if (cluster.gap_px < MIN_CLUSTER_TITLE_GAP_PX) {
      violations.push(
        `cluster ${cluster.cluster} title gap ${cluster.gap_px.toFixed(2)}px `
        + `is below ${MIN_CLUSTER_TITLE_GAP_PX}px`,
      );
    }
  }
  for (const intersection of geometryAudit.edge_title_intersections) {
    violations.push(
      `edge ${intersection.edge} crosses cluster title ${intersection.cluster}`,
    );
  }
  for (const overflow of geometryAudit.node_label_overflows) {
    violations.push(
      `node ${overflow.node} label exceeds its shape: ${JSON.stringify(overflow.overflow_px)}`,
    );
  }
  return {
    number: diagram.number,
    filename: diagram.filename,
    svg: svgPath,
    png: pngPath,
    effective_font_pt: Number(effectiveFontPt.toFixed(2)),
    viewbox_aspect_ratio: Number(aspectRatio.toFixed(3)),
    cluster_title_gaps: geometryAudit.cluster_title_gaps,
    cluster_title_edge_intersections: geometryAudit.edge_title_intersections,
    node_label_overflows: geometryAudit.node_label_overflows,
    warnings,
    violations,
  };
}


async function main() {
  const args = parseArgs(process.argv);
  const outputDir = path.resolve(args["--output-dir"]);
  await fs.mkdir(outputDir, { recursive: true });

  const diagrams = [];
  for (const manifestPath of args["--manifest"]) {
    const manifest = JSON.parse(await fs.readFile(manifestPath, "utf8"));
    const expectedCount = manifest.expected_count ?? manifest.diagrams?.length;
    if (!Array.isArray(manifest.diagrams) || manifest.diagrams.length !== expectedCount) {
      throw new Error(
        `${manifestPath} must contain exactly ${expectedCount} diagrams`,
      );
    }
    diagrams.push(...manifest.diagrams);
  }
  const expectedTotal = Number(args["--expected-count"] ?? diagrams.length);
  if (diagrams.length !== expectedTotal) {
    throw new Error(`Expected ${expectedTotal} diagrams, found ${diagrams.length}`);
  }
  const filenames = diagrams.map((diagram) => diagram.filename);
  if (new Set(filenames).size !== filenames.length) {
    throw new Error("Diagram filenames must be unique across manifests");
  }

  const browser = await chromium.launch({
    headless: true,
    executablePath: args["--chrome"] || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  });
  try {
    const page = await browser.newPage({ viewport: { width: 1800, height: 1000 } });
    await page.setContent("<!doctype html><html><body></body></html>");
    await page.addScriptTag({ path: path.resolve(args["--mermaid-js"]) });
    await page.evaluate(() => {
      window.mermaid.initialize({
        startOnLoad: false,
        securityLevel: "strict",
        theme: "base",
        flowchart: {
          curve: "basis",
          htmlLabels: false,
          useMaxWidth: false,
          nodeSpacing: 36,
          rankSpacing: 44,
          padding: 14,
          subGraphTitleMargin: {
            top: 8,
            bottom: 24,
          },
        },
        themeVariables: {
          background: "#ffffff",
          fontFamily: "Arial, sans-serif",
          fontSize: "26px",
          primaryColor: "#eef4fa",
          primaryTextColor: "#1f2a3d",
          primaryBorderColor: "#355a7a",
          secondaryColor: "#edf8f3",
          secondaryTextColor: "#1f2a3d",
          secondaryBorderColor: "#3d7257",
          tertiaryColor: "#ffffff",
          tertiaryBorderColor: "#9b7a14",
          lineColor: "#5e6b7d",
          textColor: "#1f2a3d",
          clusterBkg: "#f7f9fc",
          clusterBorder: "#b7c4d6",
          edgeLabelBackground: "#ffffff",
        },
      });
    });

    const results = [];
    for (const diagram of diagrams) {
      results.push(await renderDiagram(page, diagram, outputDir));
    }
    const report = {
      visual_style: VISUAL_STYLE_ID,
      rendered: results.length,
      minimum_effective_font_pt: Math.min(...results.map((item) => item.effective_font_pt)),
      minimum_viewbox_aspect_ratio: Math.min(
        ...results.map((item) => item.viewbox_aspect_ratio),
      ),
      minimum_cluster_title_gap_px: Math.min(
        ...results.flatMap((item) => item.cluster_title_gaps.map((cluster) => cluster.gap_px)),
      ),
      cluster_title_violations: results.flatMap((item) =>
        item.cluster_title_gaps
          .filter((cluster) => cluster.gap_px < MIN_CLUSTER_TITLE_GAP_PX)
          .map((cluster) => `${item.filename}: ${cluster.cluster} (${cluster.gap_px}px)`),
      ),
      cluster_title_edge_violations: results.flatMap((item) =>
        item.cluster_title_edge_intersections.map((intersection) => (
          `${item.filename}: ${intersection.edge} -> ${intersection.cluster}`
        )),
      ),
      node_label_violations: results.flatMap((item) =>
        item.node_label_overflows.map((overflow) => `${item.filename}: ${overflow.node}`),
      ),
      aspect_ratio_warnings: results.flatMap((item) =>
        item.warnings.map((warning) => `${item.filename}: ${warning}`),
      ),
      violations: results.flatMap((item) =>
        item.violations.map((violation) => `${item.filename}: ${violation}`),
      ),
      results,
    };
    const payload = `${JSON.stringify(report, null, 2)}\n`;
    if (args["--report-json"]) {
      await fs.writeFile(args["--report-json"], payload, "utf8");
    }
    process.stdout.write(payload);
    if (report.violations.length > 0) {
      throw new Error(
        `${report.violations.length} print-readability violations; see ${args["--report-json"] ?? "stdout"}`,
      );
    }
  } finally {
    await browser.close();
  }
}


await main();
