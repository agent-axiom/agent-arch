const AGENT_PRIORITY_DATA = [
  {
    area: "Контроль",
    impact: 9.8,
    effort: 4.2,
    category: "foundation",
    summary: "Сначала дай агенту границы, а уже потом свободу.",
  },
  {
    area: "Безопасность",
    impact: 9.6,
    effort: 5.4,
    category: "foundation",
    summary: "IAM, policy, sandboxing и approval окупаются раньше, чем кажется.",
  },
  {
    area: "Наблюдаемость",
    impact: 9.1,
    effort: 4.8,
    category: "foundation",
    summary: "Без traces и evals ты не знаешь, что именно делает агент.",
  },
  {
    area: "Инструменты",
    impact: 8.6,
    effort: 5.9,
    category: "execution",
    summary: "Tool gateway и контрактные адаптеры делают систему устойчивой.",
  },
  {
    area: "Память",
    impact: 7.3,
    effort: 6.2,
    category: "execution",
    summary: "Память полезна, если не смешивать ее с retrieval.",
  },
  {
    area: "Автономность",
    impact: 6.4,
    effort: 7.8,
    category: "advanced",
    summary: "Максимальная автономность редко должна быть первым приоритетом.",
  },
];

const I18N = {
  ru: {
    title: "Во что вкладываться в агентной платформе сначала",
    x: "Сложность внедрения",
    y: "Практическая отдача",
    footer:
      "Подсказка: чем выше точка и левее она стоит, тем полезнее начинать именно с этого слоя.",
  },
  en: {
    title: "What to invest in first in an agent platform",
    x: "Implementation effort",
    y: "Practical payoff",
    footer:
      "Hint: the higher and more left a point is, the earlier it usually deserves attention.",
  },
  zh: {
    title: "在智能体平台里，最值得优先投入的部分",
    x: "实施复杂度",
    y: "实际收益",
    footer: "提示：点越靠左且越高，通常越值得优先建设。",
  },
};

const CATEGORY_COLORS = {
  foundation: "#d97706",
  execution: "#0f766e",
  advanced: "#1d4ed8",
};

async function renderPriorityPlots() {
  const containers = [...document.querySelectorAll('[data-plot="agent-priority"]')];
  if (!containers.length) return;

  const Plot = await import("https://cdn.jsdelivr.net/npm/@observablehq/plot@0.6/+esm");

  for (const container of containers) {
    const locale = document.documentElement.lang?.startsWith("zh")
      ? "zh"
      : document.documentElement.lang?.startsWith("en")
        ? "en"
        : "ru";
    const labels = I18N[locale];

    container.innerHTML = "";

    const chart = Plot.plot({
      marginTop: 50,
      marginRight: 24,
      marginBottom: 56,
      marginLeft: 58,
      width: Math.min(container.clientWidth || 760, 760),
      height: 430,
      grid: true,
      style: {
        background: "transparent",
        color: "currentColor",
        fontFamily: '"IBM Plex Sans", sans-serif',
      },
      x: {
        label: labels.x,
        domain: [0, 10],
      },
      y: {
        label: labels.y,
        domain: [0, 10],
      },
      color: {
        domain: ["foundation", "execution", "advanced"],
        range: [
          CATEGORY_COLORS.foundation,
          CATEGORY_COLORS.execution,
          CATEGORY_COLORS.advanced,
        ],
      },
      marks: [
        Plot.ruleX([0]),
        Plot.ruleY([0]),
        Plot.dot(AGENT_PRIORITY_DATA, {
          x: "effort",
          y: "impact",
          fill: "category",
          r: 9,
          stroke: "white",
          strokeWidth: 2,
          title: (d) => `${d.area}\n${d.summary}`,
        }),
        Plot.text(AGENT_PRIORITY_DATA, {
          x: "effort",
          y: "impact",
          text: "area",
          dy: -16,
          lineAnchor: "bottom",
          fontWeight: 700,
        }),
      ],
    });

    const title = document.createElement("h3");
    title.className = "plot-card__title";
    title.textContent = labels.title;

    const footer = document.createElement("p");
    footer.className = "plot-card__caption";
    footer.textContent = labels.footer;

    container.append(title, chart, footer);
  }
}

if (typeof document$ !== "undefined") {
  document$.subscribe(() => {
    renderPriorityPlots();
  });
} else {
  window.addEventListener("DOMContentLoaded", () => {
    renderPriorityPlots();
  });
}
