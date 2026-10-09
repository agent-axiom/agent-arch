import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import {createRequire} from 'node:module';
import {fileURLToPath} from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const toolchain = process.env.DIAGRAM_TOOLCHAIN || path.dirname(here);
const require = createRequire(path.join(toolchain, 'package.json'));
const {build} = require('esbuild');
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const assets = path.resolve(here, '../../../docs/assets/diagrams');
const endpoint = (arrow, side) => {
  const point = side === 'start' ? arrow.points[0] : arrow.points.at(-1);
  return [arrow.x + point[0], arrow.y + point[1]];
};
const settle = page => page.evaluate(() => new Promise(resolve =>
  requestAnimationFrame(() => requestAnimationFrame(resolve))));

test('routed bindings keep the opposite endpoint stable during a 1px node edit',
  {timeout: 60000}, async t => {
    const bundle = await build({entryPoints: [path.join(here, 'editor-entry.mjs')],
      bundle: true, write: false, outdir: here, format: 'iife', conditions: ['production'],
      nodePaths: [path.join(toolchain, 'node_modules')],
      define: {'process.env.NODE_ENV': '"production"'}, loader: {'.woff2': 'dataurl'}});
    const browser = await chromium.launch({headless: true,
      ...(process.env.CHROMIUM_PATH ? {executablePath: process.env.CHROMIUM_PATH} : {})});
    t.after(() => browser.close());
    const page = await browser.newPage({viewport: {width: 1400, height: 1100}});
    await page.route('**/*', route => route.abort());
    await page.setContent('<!doctype html><html><head><meta charset="utf-8"></head>' +
      '<body style="margin:0"><div id="root" style="width:1400px;height:1100px"></div></body></html>');
    for (const output of bundle.outputFiles) {
      if (output.path.endsWith('.css')) await page.addStyleTag({content: output.text});
      else await page.addScriptTag({content: output.text});
    }
    for (const language of ['ru', 'en', 'zh']) {
      for (const name of ['part-i-chapter-2-01', 'part-ii-chapter-3-01']) {
        const scene = JSON.parse(await fs.readFile(path.join(assets, language, `${name}.excalidraw`), 'utf8'));
        const original = scene.elements.find(e => e.customData?.routing === 'clear-lane-below-peer-row');
        assert.ok(original, `${language}/${name}: routed fixture missing`);
        for (const side of ['start', 'end']) {
          for (const key of ['ArrowRight', 'ArrowDown']) {
            await t.test(`${language}/${name}: ${side} node ${key}`, async () => {
              // Normal runs must catch stale committed assets, without repairing them.
              await page.evaluate(({scene, generated}) => window.loadScene(scene, generated),
                {scene, generated: process.env.DIAGRAM_TEST_GENERATED_SCENES === '1'});
              await page.waitForFunction(n => window.editor?.getSceneElements().length === n &&
                !window.editor.getAppState().isLoading, scene.elements.length);
              await settle(page);
              const before = await page.evaluate(() => window.editor.getSceneElements());
              const arrow = before.find(e => e.id === original.id);
              assert.deepEqual(arrow.points, original.points);
              assert.deepEqual(endpoint(arrow, 'start'), endpoint(original, 'start'));
              assert.deepEqual(endpoint(arrow, 'end'), endpoint(original, 'end'));
              const nodeId = arrow[`${side}Binding`]?.elementId;
              assert.ok(nodeId, 'keep the editable binding, not an unbound workaround');
              const node = before.find(e => e.id === nodeId);
              const selected = before.filter(e => e.id === nodeId ||
                e.groupIds.some(g => node.groupIds.includes(g))).map(e => e.id);
              await page.evaluate(selected => window.editor.updateScene({appState: {
                selectedElementIds: Object.fromEntries(selected.map(id => [id, true])),
              }}), selected);
              await settle(page);
              await page.keyboard.press(key);
              const x = node.x + (key === 'ArrowRight' ? 1 : 0);
              const y = node.y + (key === 'ArrowDown' ? 1 : 0);
              await page.waitForFunction(({nodeId, x, y}) => {
                const node = window.editor.getSceneElements().find(e => e.id === nodeId);
                return node.x === x && node.y === y;
              }, {nodeId, x, y});
              const after = await page.evaluate(() => window.editor.getSceneElements());
              const edited = after.find(e => e.id === arrow.id);
              const opposite = side === 'start' ? 'end' : 'start';
              assert.equal(edited[`${side}Binding`]?.elementId, nodeId);
              assert.deepEqual(edited[`${opposite}Binding`], arrow[`${opposite}Binding`]);
              const a = endpoint(arrow, opposite), b = endpoint(edited, opposite);
              assert.ok(Math.hypot(a[0] - b[0], a[1] - b[1]) < 1e-6,
                `stationary ${opposite} endpoint jumped: ${a} -> ${b}`);
              const c = endpoint(arrow, side), d = endpoint(edited, side);
              assert.ok(Math.hypot(c[0] - d[0], c[1] - d[1]) > 0,
                'the endpoint on the edited node must still follow its binding');
            });
          }
        }
      }
    }
  });
