import {convertToExcalidrawElements, exportToSvg, exportToCanvas, serializeAsJSON} from '@excalidraw/excalidraw';
import {auditScene} from './audit.mjs';

export function normalizeOrthogonalBindings(elements) {
  const byId = new Map(elements.map((element) => [element.id, element]));
  for (const arrow of elements) {
    if (arrow.type !== 'arrow' || arrow.elbowed || arrow.angle || arrow.points.length < 3) continue;
    for (const [side, edge, adjacent] of [
      ['startBinding', arrow.points[0], arrow.points[1]],
      ['endBinding', arrow.points.at(-1), arrow.points.at(-2)],
    ]) {
      const binding = arrow[side], node = byId.get(binding?.elementId);
      if (!node || node.type !== 'rectangle' || node.angle || !node.width || !node.height) continue;
      let focus;
      // Excalidraw 0.18.1 calculateFocusAndGap/determineFocusDistance, specialized
      // to an axis-aligned rectangle and orthogonal terminal segment.
      if (edge[0] === adjacent[0] && edge[1] !== adjacent[1]) {
        focus = -2 * (arrow.x + edge[0] - node.x - node.width / 2) / node.width *
          Math.sign(adjacent[1] - edge[1]);
      } else if (edge[1] === adjacent[1] && edge[0] !== adjacent[0]) {
        focus = 2 * (arrow.y + edge[1] - node.y - node.height / 2) / node.height *
          Math.sign(adjacent[0] - edge[0]);
      } else continue;
      // determineFocusPoint uses strict cross products at scaled corners. Bias
      // inward by a subpixel tolerance so roundoff cannot select the far corner.
      binding.focus = focus * (1 - 1e-12);
    }
  }
}

export function makeScene(skeleton, metadata = {}) {
  const nodes = skeleton.filter((e) => e.customData?.sourceNode && ['rectangle', 'ellipse', 'diamond'].includes(e.type));
  for (const arrow of skeleton.filter((e) => e.type === 'arrow')) {
    for (const [side, point] of [['start', arrow.points[0]], ['end', arrow.points.at(-1)]]) {
      const x = arrow.x + point[0], y = arrow.y + point[1];
      const nearby = nodes.map((node) => {
        const dx = Math.max(node.x-x, x-node.x-node.width, 0);
        const dy = Math.max(node.y-y, y-node.y-node.height, 0);
        return {node, distance: Math.hypot(dx,dy)};
      }).filter(({distance}) => distance < 14).sort((a,b) => a.distance-b.distance);
      if (nearby.length === 1 || (nearby[0] && nearby[1].distance - nearby[0].distance > 3)) {
        arrow[side] = {id: nearby[0].node.id};
      }
    }
  }
  const elements = convertToExcalidrawElements(skeleton, {regenerateIds: false});
  const originals = new Map(skeleton.map((e) => [e.id, e]));
  // Text constructor accepts an alignment anchor; migration inputs are top-left boxes.
  for (const e of elements) {
    const original = originals.get(e.id);
    if (e.type === 'text' && original) {
      Object.assign(e, {x: original.x, y: original.y, width: original.width, height: original.height});
    }
    if ((e.type === 'arrow' || e.type === 'line') && original) {
      Object.assign(e, {x: original.x, y: original.y, width: original.width, height: original.height,
        points: original.points.map((point) => [...point])});
    }
  }
  normalizeOrthogonalBindings(elements);
  // Stable exports keep diffs focused on deliberate diagram changes.
  elements.forEach((e, i) => { e.seed = i + 101; e.versionNonce = i + 1; e.updated = 1; });
  const scene = JSON.parse(serializeAsJSON(elements, {viewBackgroundColor: '#ffffff'}, {}, 'local'));
  scene.source = 'https://github.com/agent-axiom/agent-arch';
  scene.appState = {viewBackgroundColor: '#ffffff', gridSize: null};
  scene.metadata = metadata;
  return scene;
}

export async function renderScene(scene, {png = false, scale = 2} = {}) {
  const audit = auditScene(scene);
  if (!audit.ok) throw new Error(audit.errors.join('\n'));
  const options = {elements: scene.elements, files: {}, exportPadding: 16,
    appState: {viewBackgroundColor: '#ffffff', exportBackground: true, exportWithDarkMode: false}};
  const svg = await exportToSvg(options);
  const width = Number(svg.getAttribute('width'));
  const height = Number(svg.getAttribute('height'));
  svg.setAttribute('role', 'img');
  if (scene.metadata?.title) {
    const title = document.createElementNS('http://www.w3.org/2000/svg', 'title');
    title.textContent = scene.metadata.title;
    svg.prepend(title);
  }
  let pngData = null;
  if (png) {
    const canvas = await exportToCanvas({...options,
      getDimensions: (w, h) => ({width: Math.ceil(w * scale), height: Math.ceil(h * scale), scale})});
    pngData = canvas.toDataURL('image/png').split(',')[1];
  }
  return {svg: svg.outerHTML, png: pngData, width, height, audit};
}

window.bookExcalidraw = {makeScene, renderScene, normalizeOrthogonalBindings};
