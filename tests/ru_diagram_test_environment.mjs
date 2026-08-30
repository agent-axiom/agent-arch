import fs from "node:fs";
import { createRequire } from "node:module";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

const TESTS_DIR = path.dirname(fileURLToPath(import.meta.url));
const PUBLISHER_DIR = path.resolve(TESTS_DIR, "../docs/publisher");
const publisherRequire = createRequire(path.join(PUBLISHER_DIR, "package.json"));


function loadPlaywright() {
  try {
    return publisherRequire("playwright");
  } catch {
    return null;
  }
}


function hasSharp() {
  try {
    publisherRequire("sharp");
    return true;
  } catch {
    return false;
  }
}


export function resolveBrowserTestEnvironment() {
  const playwright = loadPlaywright();
  const mermaidJs = path.resolve(
    process.env.MERMAID_JS
      ?? path.join(PUBLISHER_DIR, "node_modules/mermaid/dist/mermaid.min.js"),
  );
  const chrome = process.env.CHROME
    ? path.resolve(process.env.CHROME)
    : playwright?.chromium.executablePath() ?? null;
  const missing = [];
  if (!playwright) missing.push("Playwright module");
  if (!hasSharp()) missing.push("Sharp module");
  if (!fs.existsSync(mermaidJs)) missing.push(`Mermaid bundle ${mermaidJs}`);
  if (!chrome || !fs.existsSync(chrome)) missing.push(`Chromium executable ${chrome ?? "<none>"}`);
  return {
    chromium: playwright?.chromium ?? null,
    mermaidJs,
    chrome,
    missing,
    required: process.env.CI === "true" || process.env.RU_DIAGRAM_E2E_REQUIRED === "1",
  };
}


export function browserTestSkip(environment) {
  if (environment.required || environment.missing.length === 0) return false;
  return `browser dependencies unavailable: ${environment.missing.join(", ")}`;
}


export function assertBrowserTestEnvironment(environment) {
  if (environment.missing.length > 0) {
    throw new Error(`browser dependencies unavailable: ${environment.missing.join(", ")}`);
  }
}
