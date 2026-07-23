import { cloneGraph, cutsize, partsString } from "../../assets/clustering-core.js";
import {
  BAD_SEED,
  GOLDEN_BIPART,
  balanceMetrics,
} from "../../assets/partitioning-core.js";
import {
  createChallengeLab,
  drawGraph,
  el,
  metricsBlock,
} from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let graph = cloneGraph();
let assignment = { ...BAD_SEED };
let mode = "bad"; // bad | golden | none

function arm() {
  graph = cloneGraph();
  assignment = { ...BAD_SEED };
  mode = "none";
}

function show(which) {
  mode = which;
  assignment = which === "golden" ? { ...GOLDEN_BIPART } : { ...BAD_SEED };
}

createChallengeLab(root, {
  starterHtml: `
    <p><strong>Starter example (reference):</strong> bad seed <code>AE|BCD</code> has
    <strong>cutsize 12</strong> and balance ratio <strong>2/3</strong>.
    Golden <code>ABC|DE</code> has <strong>cutsize 3</strong> with the same ratio.
    Reload starter to restore the bad-seed reference.</p>
  `,
  loadStarter() {
    graph = cloneGraph();
    show("bad");
  },
  challenges: [
    {
      id: "bad-cut-12",
      title: "Bad seed cutsize 12",
      level: "Intro",
      prompt: "Show bad seed; cutsize must be 12.",
      hint: "Click Show bad seed.",
      setup: arm,
      check: () => mode === "bad" && cutsize(assignment, graph.edges) === 12,
    },
    {
      id: "bad-parts",
      title: "Bad parts AE|BCD",
      level: "Intro",
      prompt: "Bad seed parts string is AE|BCD.",
      hint: "A and E share side 0 opposite B,C,D.",
      setup: arm,
      check: () => mode === "bad" && partsString(assignment) === "AE|BCD",
    },
    {
      id: "bad-sizes-2-3",
      title: "Bad sizes 2 vs 3",
      level: "Intro",
      prompt: "Bad seed part sizes are 2 and 3.",
      hint: "balanceMetrics.sizes after Show bad seed.",
      setup: arm,
      check: () => {
        if (mode !== "bad") return false;
        const m = balanceMetrics(assignment);
        return m.sizes && m.sizes[0] === 2 && m.sizes[1] === 3;
      },
    },
    {
      id: "bad-ratio",
      title: "Bad ratio 2/3",
      level: "Practice",
      prompt: "Bad seed balance ratio equals 2/3.",
      hint: "min/max of the two side sizes.",
      setup: arm,
      check: () => mode === "bad" && Math.abs(balanceMetrics(assignment).ratio - 2 / 3) < 1e-9,
    },
    {
      id: "bad-imbalance",
      title: "Bad imbalance 0.2",
      level: "Practice",
      prompt: "Bad seed imbalance |s0−s1|/n equals 0.2.",
      hint: "|2−3|/5 = 0.2.",
      setup: arm,
      check: () => mode === "bad" && Math.abs(balanceMetrics(assignment).imbalance - 0.2) < 1e-9,
    },
    {
      id: "golden-cut-3",
      title: "Golden cutsize 3",
      level: "Practice",
      prompt: "Show golden ABC|DE; cutsize must be 3.",
      hint: "Click Show golden.",
      setup: arm,
      check: () => mode === "golden" && cutsize(assignment, graph.edges) === 3,
    },
    {
      id: "golden-parts",
      title: "Golden parts ABC|DE",
      level: "Practice",
      prompt: "Golden parts string is ABC|DE.",
      hint: "Heavy edges A–B and D–E stay internal.",
      setup: arm,
      check: () => mode === "golden" && partsString(assignment) === "ABC|DE",
    },
    {
      id: "same-ratio",
      title: "Same ratio, better cut",
      level: "Stretch",
      prompt: "Golden keeps ratio 2/3 but cut drops 12→3.",
      hint: "Show golden; compare mentally to bad seed.",
      setup: arm,
      check: () =>
        mode === "golden" &&
        cutsize(assignment, graph.edges) === 3 &&
        Math.abs(balanceMetrics(assignment).ratio - 2 / 3) < 1e-9,
    },
    {
      id: "two-labels",
      title: "Exactly two labels",
      level: "Stretch",
      prompt: "Either view uses exactly two partition labels.",
      hint: "Show bad or golden first.",
      setup: arm,
      check: () =>
        (mode === "bad" || mode === "golden") &&
        new Set(Object.values(assignment)).size === 2,
    },
    {
      id: "cut-beats-balance",
      title: "Cut distinguishes quality",
      level: "Stretch",
      prompt: "With golden shown, cut is 3 (not 12) — balance alone does not rank partitions.",
      hint: "Both seeds share ratio 2/3; cutsize decides.",
      setup: arm,
      check: () =>
        mode === "golden" &&
        cutsize(assignment, graph.edges) === 3 &&
        cutsize(BAD_SEED, graph.edges) === 12,
    },
  ],
  extraActions(ctx) {
    return [
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: "Show bad seed",
        onClick: () => {
          show("bad");
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Show golden",
        onClick: () => {
          show("golden");
          ctx.rerender();
        },
      }),
    ];
  },
  renderWorkspace(ctx) {
    drawGraph(ctx.canvas, graph, { assignment: mode === "none" ? null : assignment });
    const lines = [];
    if (mode === "none") {
      lines.push("No partition shown — pick bad seed or golden.");
    } else {
      const m = balanceMetrics(assignment);
      lines.push(`view: ${mode}`);
      lines.push(`parts: ${partsString(assignment)}`);
      lines.push(`cutsize: ${cutsize(assignment, graph.edges)}`);
      lines.push(`sizes: ${m.sizes ? m.sizes.join(" vs ") : "?"}`);
      lines.push(`ratio (min/max): ${m.ratio != null ? m.ratio.toFixed(4) : "?"}`);
      lines.push(`imbalance: ${m.imbalance != null ? m.imbalance.toFixed(4) : "?"}`);
    }
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock(lines));
  },
});
