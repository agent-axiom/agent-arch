import fs from 'node:fs/promises';
import path from 'node:path';
import {createRequire} from 'node:module';
import {fileURLToPath} from 'node:url';
import {auditScene} from './audit.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const toolchain = process.env.DIAGRAM_TOOLCHAIN || here;
const require = createRequire(path.join(toolchain, 'package.json'));
const {build} = require('esbuild');
const {chromium} = process.env.PLAYWRIGHT_MODULE
  ? require(process.env.PLAYWRIGHT_MODULE) : require('playwright');
const files = process.argv.slice(2);
if (!files.length) throw new Error('Usage: node export.mjs scene.excalidraw [more scenes...]');
const bundle = await build({entryPoints: [path.join(here, 'browser.mjs')], bundle: true, write: false,
  format: 'iife', nodePaths: [path.join(toolchain, 'node_modules')],
  define: {'process.env.NODE_ENV': '"production"'}, loader: {'.woff2': 'dataurl', '.css': 'empty'}});
const browser = await chromium.launch({headless: true,
  ...(process.env.CHROMIUM_PATH ? {executablePath: process.env.CHROMIUM_PATH} : {})});
try {
  const page = await browser.newPage();
  await page.setContent('<!doctype html><html><head><meta charset="utf-8"></head><body></body></html>');
  await page.addScriptTag({content: bundle.outputFiles[0].text});
  for (const file of files) {
    if (!file.endsWith('.excalidraw')) throw new Error(`Expected .excalidraw input: ${file}`);
    const scene = JSON.parse(await fs.readFile(file, 'utf8'));
    const audit = auditScene(scene);
    if (!audit.ok) throw new Error(`${file}: ${audit.errors.join('; ')}`);
    const output = await page.evaluate((scene) => window.bookExcalidraw.renderScene(scene), scene);
    const target = file.replace(/\.excalidraw$/, '.svg');
    await fs.writeFile(target, output.svg);
    console.log(`${target}: ${audit.elements} editable elements, ${audit.edges} arrows`);
  }
} finally {
  await browser.close();
}
