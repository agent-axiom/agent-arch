import fs from "node:fs/promises";
import { createRequire } from "node:module";
import path from "node:path";
import process from "node:process";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");
const sharp = require("sharp");

const MIN_EFFECTIVE_FONT_PT = 7.8;
const PRINT_MAX_WIDTH_INCHES = 6.5;
const PRINT_MAX_HEIGHT_INCHES = 7.6;
const PNG_DENSITY = 300;


function parseArgs(argv) {
  const values = {};
  for (let index = 2; index < argv.length; index += 2) {
    values[argv[index]] = argv[index + 1];
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


function wrapLabel(value, maxCharacters = 24) {
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


function calculateEffectiveFontPt(svg, metadata) {
  const viewBox = svg.match(/viewBox="[^"\s]+\s+[^"\s]+\s+([0-9.]+)\s+([0-9.]+)"/);
  const fontSizes = [...svg.matchAll(/font-size:\s*([0-9.]+)px/g)]
    .map((match) => Number(match[1]))
    .filter((size) => size >= 20);
  if (!viewBox || fontSizes.length === 0 || !metadata.width) {
    throw new Error("Cannot calculate effective print font size from rendered diagram");
  }

  const viewWidth = Number(viewBox[1]);
  const viewHeight = Number(viewBox[2]);
  const sourceFontSize = Math.max(...fontSizes);
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
    source: wrapMermaidLabels(diagram.mermaid),
  });

  const title = `<title>${escapeXml(diagram.caption)}</title>`;
  const xmlSafeRendered = rendered.replaceAll(/<br\s*>/g, "<br/>");
  const svg = xmlSafeRendered.replace(/<svg([^>]*)>/, `<svg$1>${title}`);
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
  const effectiveFontPt = calculateEffectiveFontPt(svg, metadata);
  if (effectiveFontPt < MIN_EFFECTIVE_FONT_PT) {
    throw new Error(
      `Unreadable print font for ${diagram.filename}: ${effectiveFontPt.toFixed(2)}pt`,
    );
  }
  return {
    number: diagram.number,
    svg: svgPath,
    png: pngPath,
    effective_font_pt: Number(effectiveFontPt.toFixed(2)),
  };
}


async function main() {
  const args = parseArgs(process.argv);
  const manifest = JSON.parse(await fs.readFile(args["--manifest"], "utf8"));
  const outputDir = path.resolve(args["--output-dir"]);
  await fs.mkdir(outputDir, { recursive: true });

  const expectedCount = manifest.expected_count ?? 29;
  if (!Array.isArray(manifest.diagrams) || manifest.diagrams.length !== expectedCount) {
    throw new Error(`The diagram manifest must contain exactly ${expectedCount} diagrams`);
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
          primaryColor: "#edf7f1",
          primaryTextColor: "#17201b",
          primaryBorderColor: "#2f6f4e",
          secondaryColor: "#f3f5f4",
          secondaryTextColor: "#17201b",
          secondaryBorderColor: "#66736c",
          tertiaryColor: "#ffffff",
          lineColor: "#3f4b45",
          textColor: "#17201b",
          edgeLabelBackground: "#ffffff",
        },
      });
    });

    const results = [];
    for (const diagram of manifest.diagrams) {
      results.push(await renderDiagram(page, diagram, outputDir));
    }
    process.stdout.write(`${JSON.stringify({ rendered: results.length, results }, null, 2)}\n`);
  } finally {
    await browser.close();
  }
}


await main();
