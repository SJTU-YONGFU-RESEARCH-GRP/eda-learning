import {
  GOLDENS,
  TINY_TIMING,
  arcKindCounts,
  cellDelaySum,
  cloneTiming,
  levelize,
  near,
  pathDelaySum,
  sinks,
  sources,
  summarize,
  topoOrder,
  withCycle,
} from "../../assets/sta-core.js";
import {
  createChallengeLab,
  drawTimingGraph,
  el,
  metricsBlock,
} from "../../assets/sta-ui.js";

const root = document.getElementById("lab-root");
let timing = cloneTiming(TINY_TIMING);
let levels = levelize(timing);
let mode = "starter"; // starter | cyclic | none

function arm() {
  timing = cloneTiming(TINY_TIMING);
  levels = null;
  mode = "none";
}

function show(which) {
  mode = which;
  if (which === "cyclic") {
    timing = withCycle(TINY_TIMING);
    levels = levelize(timing);
  } else {
    timing = cloneTiming(TINY_TIMING);
    levels = levelize(timing);
  }
}

createChallengeLab(root, {
  starterHtml: `
    <p><strong>Starter example (reference):</strong> chain
    <code>in → u1 → u2 → out</code> has <strong>${GOLDENS.pinCount} pins</strong>,
    <strong>${GOLDENS.arcCount} arcs</strong> (${GOLDENS.cellArcs} cell /
    ${GOLDENS.netArcs} net), levelized <strong>0…${GOLDENS.maxLevel}</strong>,
    path delay sum <strong>${GOLDENS.pathDelay}</strong>.
    A cyclic back-edge <code>out→in</code> fails levelize. Reload starter anytime.</p>
  `,
  loadStarter() {
    show("starter");
  },
  challenges: [
    {
      id: "pins-6",
      title: "Six pins",
      level: "Intro",
      prompt: "Starter has exactly 6 pins.",
      hint: "Show starter; count pin nodes.",
      setup: arm,
      check: () => mode === "starter" && timing.pins.length === GOLDENS.pinCount,
    },
    {
      id: "arcs-5",
      title: "Five arcs",
      level: "Intro",
      prompt: "Starter has exactly 5 arcs.",
      hint: "Show starter.",
      setup: arm,
      check: () => mode === "starter" && timing.arcs.length === GOLDENS.arcCount,
    },
    {
      id: "cell-net-split",
      title: "2 cell / 3 net",
      level: "Intro",
      prompt: "Starter has 2 cell arcs and 3 net arcs.",
      hint: "arcKindCounts after Show starter.",
      setup: arm,
      check: () => {
        if (mode !== "starter") return false;
        const k = arcKindCounts(timing);
        return k.cell === GOLDENS.cellArcs && k.net === GOLDENS.netArcs;
      },
    },
    {
      id: "source-in",
      title: "Source is in",
      level: "Practice",
      prompt: "The only source pin is in.",
      hint: "Pins with no incoming arc.",
      setup: arm,
      check: () =>
        mode === "starter" && sources(timing).join(",") === GOLDENS.sources.join(","),
    },
    {
      id: "sink-out",
      title: "Sink is out",
      level: "Practice",
      prompt: "The only sink pin is out.",
      hint: "Pins with no outgoing arc.",
      setup: arm,
      check: () =>
        mode === "starter" && sinks(timing).join(",") === GOLDENS.sinks.join(","),
    },
    {
      id: "max-level-5",
      title: "Max level 5",
      level: "Practice",
      prompt: "After levelize, max level is 5 (out).",
      hint: "Show starter; levels[out] === 5.",
      setup: arm,
      check: () => {
        if (mode !== "starter" || !levels) return false;
        return Math.max(...Object.values(levels)) === GOLDENS.maxLevel;
      },
    },
    {
      id: "topo-chain",
      title: "Topo order chain",
      level: "Practice",
      prompt: "Topo order is in, u1/A, u1/Y, u2/A, u2/Y, out.",
      hint: "Levelize then sort by level.",
      setup: arm,
      check: () => {
        if (mode !== "starter") return false;
        const t = topoOrder(timing);
        return t && t.join(",") === GOLDENS.topo.join(",");
      },
    },
    {
      id: "path-delay-3-2",
      title: "Path delay 3.2",
      level: "Stretch",
      prompt: "Sum of all arc delays equals 3.2.",
      hint: "0 + 1.2 + 0.3 + 1.5 + 0.2.",
      setup: arm,
      check: () =>
        mode === "starter" && near(pathDelaySum(timing), GOLDENS.pathDelay),
    },
    {
      id: "cell-delay-2-7",
      title: "Cell delay sum 2.7",
      level: "Stretch",
      prompt: "Sum of cell-arc delays equals 2.7.",
      hint: "1.2 + 1.5.",
      setup: arm,
      check: () =>
        mode === "starter" && near(cellDelaySum(timing), GOLDENS.cellDelaySum),
    },
    {
      id: "cycle-fails",
      title: "Cycle fails levelize",
      level: "Stretch",
      prompt: "Show cyclic; levelize returns null (acyclic false).",
      hint: "Click Show cyclic (adds out→in).",
      setup: arm,
      check: () => mode === "cyclic" && levels == null && !summarize(timing).acyclic,
    },
  ],
  extraActions(ctx) {
    return [
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: "Show starter",
        onClick: () => {
          show("starter");
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Show cyclic",
        onClick: () => {
          show("cyclic");
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: "Levelize",
        onClick: () => {
          levels = levelize(timing);
          ctx.rerender();
        },
      }),
    ];
  },
  renderWorkspace(ctx) {
    drawTimingGraph(ctx.canvas, timing, {
      levels,
      highlightPins: mode === "starter" ? ["in", "out"] : mode === "cyclic" ? ["out", "in"] : [],
      highlightArcs: mode === "cyclic" ? ["out|in"] : [],
    });
    const s = summarize(timing);
    const lines = [
      `view: ${mode}`,
      `pins: ${s.pins}  arcs: ${s.arcs}  (cell ${s.cellArcs} / net ${s.netArcs})`,
      `sources: ${s.sources.join(", ") || "—"}`,
      `sinks: ${s.sinks.join(", ") || "—"}`,
      `acyclic: ${s.acyclic}`,
      `max level: ${s.maxLevel ?? "—"}`,
      `topo: ${s.topo ? s.topo.join(" → ") : "(cycle)"}`,
      `path delay Σ: ${s.pathDelay}`,
      `cell delay Σ: ${s.cellDelaySum}`,
    ];
    if (levels) {
      lines.push("levels:");
      for (const [p, lv] of Object.entries(levels).sort((a, b) => a[1] - b[1] || a[0].localeCompare(b[0]))) {
        lines.push(`  ${p}: ${lv}`);
      }
    }
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock(lines));
  },
});
