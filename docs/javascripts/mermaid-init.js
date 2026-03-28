let mermaidModulePromise;

async function getMermaid() {
  if (!mermaidModulePromise) {
    mermaidModulePromise = import(
      "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs"
    );
  }
  return mermaidModulePromise;
}

async function renderMermaidDiagrams() {
  const mermaidBlocks = [...document.querySelectorAll("pre.mermaid")];
  if (!mermaidBlocks.length) return;

  const { default: mermaid } = await getMermaid();
  const theme = document.body.dataset.mdColorScheme === "slate" ? "dark" : "default";

  mermaid.initialize({
    startOnLoad: false,
    securityLevel: "loose",
    theme,
  });

  for (const block of mermaidBlocks) {
    if (block.dataset.mermaidReady === "true") continue;

    const diagram = document.createElement("div");
    diagram.className = "mermaid";
    diagram.textContent = block.textContent.trim();
    block.replaceWith(diagram);
  }

  await mermaid.run({
    querySelector: ".mermaid",
  });

  for (const diagram of document.querySelectorAll(".mermaid")) {
    diagram.dataset.mermaidReady = "true";
  }
}

if (typeof document$ !== "undefined") {
  document$.subscribe(() => {
    renderMermaidDiagrams();
  });
} else {
  window.addEventListener("DOMContentLoaded", () => {
    renderMermaidDiagrams();
  });
}
