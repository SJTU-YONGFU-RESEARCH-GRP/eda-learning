import {
  BAD_SEED,
  TINY_HYPERGRAPH,
  hyperedgeCut,
  hyperedgesToPairEdges,
  partsString,
} from "../../assets/clustering-core.js";
import { hypergraphBipartition } from "../../assets/partitioning-core.js";
import {
  createChallengeLab,
  drawGraph,
  el,
  metricsBlock,
} from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let hyper = {
  nodes: [...TINY_HYPERGRAPH.nodes],
  hyperedges: TINY_HYPERGRAPH.hyperedges.map((h) => ({ ...h, pins: [...h.pins] })),
  sizes: { ...TINY_HYPERGRAPH.sizes },
};
let seed = { ...BAD_SEED };
let result = null;
let view = "seed"; // seed | result

function graphForDraw() {
  return {
    nodes: hyper.nodes,
    edges: hyperedgesToPairEdges(hyper.hyperedges),
    sizes: hyper.sizes,
  };
}

function arm() {
  hyper = {
    nodes: [...TINY_HYPERGRAPH.nodes],
    hyperedges: TINY_HYPERGRAPH.hyperedges.map((h) => ({ ...h, pins: [...h.pins] })),
    sizes: { ...TINY_HYPERGRAPH.sizes },
  };
  seed = { ...BAD_SEED };
  result = null;
  view = "none";
}

createChallengeLab(root, {
  starterHtml: `
    <p><strong>Starter example (reference):</strong> bad seed hyperedge cut is
    <strong>6</strong> (nets n1, n2, n4 span sides). FM on the clique expansion reaches
    <code>ABC|DE</code> with <strong>hyperedge cut 1</strong> (only n3). Reload starter anytime.</p>
  `,
  loadStarter() {
    arm();
    result = hypergraphBipartition(hyper.nodes, hyper.hyperedges, seed);
    view = "result";
  },
  challenges: [
    {
      id: "seed-hyper-6",
      title: "Seed hyper cut 6",
      level: "Intro",
      prompt: "Show seed only; hyperedge cut must be 6.",
      hint: "Click Show seed only — n1+n2+n4 = 3+2+1.",
      setup: arm,
      check: () => view === "seed" && hyperedgeCut(seed, hyper.hyperedges) === 6,
    },
    {
      id: "seed-parts",
      title: "Seed parts AE|BCD",
      level: "Intro",
      prompt: "Seed parts string is AE|BCD.",
      hint: "Same BAD_SEED as graph labs.",
      setup: arm,
      check: () => view === "seed" && partsString(seed) === "AE|BCD",
    },
    {
      id: "run-hyper-1",
      title: "Refined hyper cut 1",
      level: "Intro",
      prompt: "Run hypergraph FM; hyperedge cut is 1.",
      hint: "Only net n3 crosses.",
      setup: arm,
      check: () => view === "result" && result && result.hyperCut === 1,
    },
    {
      id: "run-parts",
      title: "Refined ABC|DE",
      level: "Practice",
      prompt: "After FM, parts are ABC|DE.",
      hint: "Same golden communities.",
      setup: arm,
      check: () => view === "result" && result && partsString(result.assignment) === "ABC|DE",
    },
    {
      id: "n1-uncut",
      title: "Net n1 uncut",
      level: "Practice",
      prompt: "Pins of n1 (A,B,C) share one side.",
      hint: "Heaviest multi-pin net stays internal.",
      setup: arm,
      check: () =>
        view === "result" &&
        result &&
        result.assignment.A === result.assignment.B &&
        result.assignment.B === result.assignment.C,
    },
    {
      id: "n2-uncut",
      title: "Net n2 uncut",
      level: "Practice",
      prompt: "Pins of n2 (D,E) share one side.",
      hint: "Pair net D–E stays together.",
      setup: arm,
      check: () => view === "result" && result && result.assignment.D === result.assignment.E,
    },
    {
      id: "n3-cut",
      title: "Net n3 is cut",
      level: "Practice",
      prompt: "n3 pins C and D are on different sides.",
      hint: "That single cut contributes weight 1.",
      setup: arm,
      check: () => view === "result" && result && result.assignment.C !== result.assignment.D,
    },
    {
      id: "four-hedges",
      title: "Instance has 4 nets",
      level: "Stretch",
      prompt: "Before running, instance exposes exactly 4 hyperedges.",
      hint: "n1…n4 — show seed or leave armed.",
      setup: arm,
      check: () => !result && hyper.hyperedges.length === 4,
    },
    {
      id: "pair-cut-1",
      title: "Pair expansion cut 1",
      level: "Stretch",
      prompt: "After refine, pairCut on clique expansion is also 1.",
      hint: "On this tiny instance hyper and pair agree at optimum.",
      setup: arm,
      check: () => view === "result" && result && result.pairCut === 1,
    },
    {
      id: "improves-seed",
      title: "Improves seed 6→1",
      level: "Stretch",
      prompt: "Refined hyperCut 1 beats seed hyper cut 6.",
      hint: "Run FM after arming from seed.",
      setup: arm,
      check: () =>
        view === "result" &&
        result &&
        result.hyperCut === 1 &&
        hyperedgeCut(BAD_SEED, hyper.hyperedges) === 6,
    },
  ],
  extraActions(ctx) {
    return [
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: "Show seed only",
        onClick: () => {
          result = null;
          view = "seed";
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Run hypergraph FM",
        onClick: () => {
          result = hypergraphBipartition(hyper.nodes, hyper.hyperedges, seed);
          view = "result";
          ctx.rerender();
        },
      }),
    ];
  },
  renderWorkspace(ctx) {
    const g = graphForDraw();
    const asn = view === "result" && result ? result.assignment : view === "seed" ? seed : null;
    drawGraph(ctx.canvas, g, { assignment: asn });
    const lines = [`hyperedges: ${hyper.hyperedges.length}`];
    for (const h of hyper.hyperedges) {
      lines.push(`  ${h.id}: [${h.pins.join(",")}] w=${h.w}`);
    }
    if (view === "none" || (!result && view !== "seed")) {
      lines.push("No view yet — show seed or run FM.");
    } else if (view === "seed") {
      lines.push(`seed parts: ${partsString(seed)}`);
      lines.push(`hyperedge cut: ${hyperedgeCut(seed, hyper.hyperedges)}`);
    } else if (result) {
      lines.push(`parts: ${partsString(result.assignment)}`);
      lines.push(`hyperedge cut: ${result.hyperCut}`);
      lines.push(`pair expansion cut: ${result.pairCut}`);
    }
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock(lines));
  },
});
