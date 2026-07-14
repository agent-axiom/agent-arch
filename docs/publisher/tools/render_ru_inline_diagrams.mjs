import fs from "node:fs/promises";
import { createRequire } from "node:module";
import path from "node:path";
import process from "node:process";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");
const sharp = require("sharp");


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


async function renderDiagram(page, diagram, outputDir) {
  const rendered = await page.evaluate(async ({ number, source }) => {
    const id = `ru-inline-diagram-${String(number).padStart(2, "0")}`;
    const result = await window.mermaid.render(id, source);
    return result.svg;
  }, { number: diagram.number, source: diagram.mermaid });

  const title = `<title>${escapeXml(diagram.caption)}</title>`;
  const svg = rendered.replace(/<svg([^>]*)>/, `<svg$1>${title}`);
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
  await sharp(screenshot)
    .resize({ width: 1600, height: 900, fit: "contain", background: "#ffffff" })
    .flatten({ background: "#ffffff" })
    .removeAlpha()
    .png({ compressionLevel: 9, adaptiveFiltering: true })
    .withMetadata({ density: 300 })
    .toFile(pngPath);

  const metadata = await sharp(pngPath).metadata();
  if (metadata.width !== 1600 || metadata.height !== 900 || metadata.hasAlpha) {
    throw new Error(`Invalid PNG output for ${diagram.filename}: ${JSON.stringify(metadata)}`);
  }
  return { number: diagram.number, svg: svgPath, png: pngPath };
}


async function main() {
  const args = parseArgs(process.argv);
  const manifest = JSON.parse(await fs.readFile(args["--manifest"], "utf8"));
  const outputDir = path.resolve(args["--output-dir"]);
  await fs.mkdir(outputDir, { recursive: true });

  if (!Array.isArray(manifest.diagrams) || manifest.diagrams.length !== 29) {
    throw new Error("The manuscript diagram manifest must contain exactly 29 diagrams");
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
        flowchart: { curve: "basis", htmlLabels: false, useMaxWidth: false },
        themeVariables: {
          background: "#ffffff",
          fontFamily: "Arial, sans-serif",
          fontSize: "18px",
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
