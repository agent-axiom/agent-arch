import test from 'node:test';
import assert from 'node:assert/strict';
import { auditScene } from '../audit.mjs';

const scene = () => ({type: 'excalidraw', version: 2, elements: [
  {id: 'a', type: 'rectangle', x: 0, y: 0, width: 100, height: 60},
  {id: 't', type: 'text', x: 5, y: 5, width: 90, height: 25, text: 'Allow only'},
  {id: 'e', type: 'arrow', x: 100, y: 30, width: 80, height: 0, points: [[0,0],[80,0]], endArrowhead: 'arrow'},
]});

test('accepts a native editable scene with its labels and relationship', () => {
  assert.equal(auditScene(scene(), {labels: ['Allow only'], edges: 1}).ok, true);
});
test('rejects flattening to an image', () => {
  const s = scene(); s.elements.push({id: 'flat', type: 'image', x:0,y:0,width:100,height:100});
  assert.equal(auditScene(s).ok, false);
});
test('detects lost labels and duplicated semantic arrows', () => {
  assert.equal(auditScene(scene(), {labels: ['Deny'], edges: 1}).ok, false);
  const s = scene(); s.elements.push({...s.elements[2], id: 'duplicate'});
  assert.equal(auditScene(s, {edges: 1}).ok, false);
});
test('rejects nonfinite geometry and duplicate IDs', () => {
  const s = scene(); s.elements[0].width = NaN;
  assert.equal(auditScene(s).ok, false);
  const t = scene(); t.elements[1].id = 'a';
  assert.equal(auditScene(t).ok, false);
});
