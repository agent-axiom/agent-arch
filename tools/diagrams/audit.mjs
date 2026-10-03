const normalize = (text) => String(text).replace(/\s+/gu, ' ').trim();

export function auditScene(scene, expected = {}) {
  const errors = [];
  if (scene.type !== 'excalidraw' || scene.version !== 2) errors.push('Not an Excalidraw v2 scene');
  const elements = (scene.elements || []).filter((e) => !e.isDeleted);
  const ids = new Set();
  for (const e of elements) {
    if (ids.has(e.id)) errors.push(`Duplicate ID: ${e.id}`);
    ids.add(e.id);
    if (e.type === 'image') errors.push(`Noneditable image: ${e.id}`);
    for (const key of ['x', 'y', 'width', 'height']) {
      if (!Number.isFinite(e[key])) errors.push(`Invalid ${key}: ${e.id}`);
    }
    for (const point of e.points || []) {
      if (point.some((n) => !Number.isFinite(n))) errors.push(`Invalid point: ${e.id}`);
    }
    for (const binding of [e.startBinding, e.endBinding]) {
      if (binding && !elements.some((target) => target.id === binding.elementId)) {
        errors.push(`Broken binding: ${e.id}`);
      }
    }
  }
  const labels = elements.filter((e) => e.type === 'text').map((e) => normalize(e.text));
  for (const label of expected.labels || []) {
    if (!labels.includes(normalize(label))) errors.push(`Missing label: ${label}`);
  }
  const edges = elements.filter((e) => e.type === 'arrow').length;
  if (expected.edges !== undefined && expected.edges !== edges) errors.push(`Expected ${expected.edges} arrows, got ${edges}`);
  if (!labels.length) errors.push('No editable labels');
  return {ok: errors.length === 0, errors, elements: elements.length, labels: labels.length, edges};
}
