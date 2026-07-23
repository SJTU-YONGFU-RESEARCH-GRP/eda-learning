import {
  TINY_HYPERGRAPH,
  hyperedgeCut,
  hyperedgesToPairEdges,
  hypergraphGreedyCluster,
  partsString,
} from "../../assets/clustering-core.js";
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
let result = null;
let targetK = 2;

function graphForDraw() {
  return {
    nodes: hyper.nodes,
    edges: hyperedgesToPairEdges(hyper.hyperedges),
    sizes: hyper.sizes,
  };
}

function arm(k = 2) {
  hyper = {
    nodes: [...TINY_HYPERGRAPH.nodes],
    hyperedges: TINY_HYPERGRAPH.hyperedges.map((h) => ({ ...h, pins: [...h.pins] })),
    sizes: { ...TINY_HYPERGRAPH.sizes },
  };
  targetK = k;
  result = null;
}

createChallengeLab(root, {
  starterHtml: `
    <p><strong>Starter example (reference):</strong> hypergraph greedy to <code>K=2</code>
    clusters <code>ABC|DE</code> with <strong>hyperedge cut 1</strong> (only net n3 crosses).
    Graph view shows clique-expanded pairwise edges. Reload starter anytime.</p>
  `,
  loadStarter() {
    arm(2);
    result = hypergraphGreedyCluster(hyper.nodes, hyper.hyperedges, hyper.sizes, 2);
  },
  challenges: [
    {
      id: "hyper-cut-1",
      title: "Hyperedge cut is 1",
      level: "Intro",
      prompt: "Run K=2 hypergraph greedy; hyperedge cut must be 1.",
      hint: "Only the C–D net is cut.",
      setup: () => arm(2),
      check: () => result && hyperedgeCut(result, hyper.hyperedges) === 1,
    },
    {
      id: "parts-abc-de",
      title: "Parts ABC|DE",
      level: "Intro",
      prompt: "K=2 yields communities ABC|DE.",
      hint: "Multi-pin n1 pulls A,B,C together.",
      setup: () => arm(2),
      check: () => result && partsString(result) === "ABC|DE",
    },
    {
      id: "two-clusters",
      title: "Exactly two clusters",
      level: "Intro",
      prompt: "Target K=2 ends with two cluster ids.",
      hint: "H-labels after merges.",
      setup: () => arm(2),
      check: () => result && new Set(Object.values(result)).size === 2,
    },
    {
      id: "n1-uncut",
      title: "Net n1 uncut",
      level: "Practice",
      prompt: "Pins of n1 (A,B,C) share one cluster.",
      hint: "Heaviest multi-pin net stays internal.",
      setup: () => arm(2),
      check: () => result && result.A === result.B && result.B === result.C,
    },
    {
      id: "n2-uncut",
      title: "Net n2 uncut",
      level: "Practice",
      prompt: "Pins of n2 (D,E) share one cluster.",
      hint: "Pair net D–E stays together.",
      setup: () => arm(2),
      check: () => result && result.D === result.E,
    },
    {
      id: "n3-cut",
      title: "Net n3 is cut",
      level: "Practice",
      prompt: "n3 pins C and D are on different sides.",
      hint: "That single cut contributes weight 1.",
      setup: () => arm(2),
      check: () => result && result.C !== result.D,
    },
    {
      id: "n4-uncut",
      title: "Net n4 uncut",
      level: "Practice",
      prompt: "n4 pins A and B stay together.",
      hint: "A–B affinity reinforces ABC.",
      setup: () => arm(2),
      check: () => result && result.A === result.B,
    },
    {
      id: "four-hedges",
      title: "Instance has 4 hyperedges",
      level: "Stretch",
      prompt: "TINY_HYPERGRAPH exposes exactly 4 hyperedges (before running).",
      hint: "n1…n4 in the instance.",
      setup: () => arm(2),
      check: () => !result && hyper.hyperedges.length === 4,
    },
    {
      id: "k5-noop",
      title: "K=5 is a no-op",
      level: "Stretch",
      prompt: "Run with K=5; zero merges — five singleton clusters.",
      hint: "Already at target K.",
      setup: () => arm(5),
      check: () => result && new Set(Object.values(result)).size === 5,
    },
    {
      id: "vs-graph-cut",
      title: "Hyper cut ≠ graph expansion",
      level: "Stretch",
      prompt: "K=2 hyper cut is 1 (not the pairwise graph cut). Confirm hyperedge cut === 1.",
      hint: "Multi-pin modeling differs from clique expansion cut.",
      setup: () => arm(2),
      check: () => result && hyperedgeCut(result, hyper.hyperedges) === 1 && partsString(result) === "ABC|DE",
    },
  ],
  extraActions(ctx) {
    return [
      el("button", {
        className: "btn btn-ghost",
        type: "button",
        text: "K=2",
        onClick: () => {
          targetK = 2;
          result = null;
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-ghost",
        type: "button",
        text: "K=5",
        onClick: () => {
          targetK = 5;
          result = null;
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Run hypergraph greedy",
        onClick: () => {
          result = hypergraphGreedyCluster(hyper.nodes, hyper.hyperedges, hyper.sizes, targetK);
          ctx.rerender();
        },
      }),
    ];
  },
  renderWorkspace(ctx) {
    const g = graphForDraw();
    drawGraph(ctx.canvas, g, { assignment: result || null });
    const lines = [`target K=${targetK}`, `hyperedges: ${hyper.hyperedges.length}`];
    for (const h of hyper.hyperedges) {
      lines.push(`  ${h.id}: [${h.pins.join(",")}] w=${h.w}`);
    }
    if (!result) {
      lines.push("No result yet — click Run hypergraph greedy.");
    } else {
      lines.push(`hyperedge cut: ${hyperedgeCut(result, hyper.hyperedges)}`);
      lines.push(`parts: ${partsString(result)}`);
      lines.push(`labels: ${JSON.stringify(result)}`);
    }
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock(lines));
  },
});
