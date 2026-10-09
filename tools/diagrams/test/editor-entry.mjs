import React from 'react';
import {createRoot} from 'react-dom/client';
import {Excalidraw} from '@excalidraw/excalidraw';
import '@excalidraw/excalidraw/index.css';
import {makeScene} from '../browser.mjs';

const root = createRoot(document.getElementById('root'));
let serial = 0;
window.loadScene = (scene, generated) => {
  const data = generated ? makeScene(scene.elements, scene.metadata) : scene;
  window.editor = null;
  root.render(React.createElement(Excalidraw, {
    key: ++serial,
    initialData: {...data, scrollToContent: true},
    excalidrawAPI: api => { window.editor = api; },
    autoFocus: true,
  }));
};
