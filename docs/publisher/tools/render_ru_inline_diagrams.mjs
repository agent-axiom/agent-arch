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


function wrapMermaidLabels(source) {
  return source.replaceAll(/"([^"\r\n]*)"/g, (_match, label) => `"${wrapLabel(label)}"`);
}


function normalizeMermaidSource(source) {
  const withoutLocalTheme = source.replace(/^\s*%%\{init:.*?\}%%\s*/s, "");
  return wrapMermaidLabels(withoutLocalTheme.trim());
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
  const svg = xmlSafeRendered.replace(
    /<svg([^>]*)>/,
    `<svg$1 data-visual-style="${VISUAL_STYLE_ID}">${title}${UNIFIED_SVG_STYLE}`,
  );
  const stem = path.parse(diagram.filename).name;
  const svgPath = path.join(outputDir, `${stem}.svg`);
  const pngPath = path.join(outputDir, diagram.filename);

  await fs.writeFile(svgPath, `${svg}\n`, "utf8");
  await page.evaluate((svgMarkup) => {
    document.body.innerHTML = `<main id="diagram">${svgMarkup}</main>`;
    document.documentElement.style.background = "#ffffff";
    document.body.style.margin = "0";
    document.body.style.background = "#ffffff";
    const element = document.querySelector("#diagram > svg");
    element.style.display = "block";
    element.style.maxWidth = "none";
  }, svg);
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
      top: 48,
      bottom: 48,
      left: 48,
      right: 48,
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
  if (effectiveFontPt < MIN_EFFECTIVE_FONT_PT) {
    violations.push(
      `effective font ${effectiveFontPt.toFixed(2)}pt is below ${MIN_EFFECTIVE_FONT_PT}pt`,
    );
  }
  const viewBox = svg.match(/viewBox="[^"\s]+\s+[^"\s]+\s+([0-9.]+)\s+([0-9.]+)"/);
  if (!viewBox) throw new Error(`Missing viewBox for ${diagram.filename}`);
  const aspectRatio = Number(viewBox[1]) / Number(viewBox[2]);
  if (aspectRatio < MIN_VIEWBOX_ASPECT_RATIO) {
    violations.push(
      `viewBox aspect ${aspectRatio.toFixed(3)} is below ${MIN_VIEWBOX_ASPECT_RATIO}`,
    );
  }
  return {
    number: diagram.number,
    filename: diagram.filename,
    svg: svgPath,
    png: pngPath,
    effective_font_pt: Number(effectiveFontPt.toFixed(2)),
    viewbox_aspect_ratio: Number(aspectRatio.toFixed(3)),
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
