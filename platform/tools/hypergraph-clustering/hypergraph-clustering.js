import {
  TINY_HYPERGRAPH,
  hyperedgeCut,
  hyperedgesToPairEdges,
  hypergraphGreedyCluster,
  partsString,
} from "../../assets/clustering-core.js";
import {
  createInteractiveGraphLab,
  el,
} from "../../assets/interactive-graph-lab.js";

const root = document.getElementById("lab-root");
const GOLDEN = { A: "0", B: "0", C: "0", D: "1", E: "1" };

function hyperGraph() {
  return {
    nodes: [...TINY_HYPERGRAPH.nodes],
    edges: hyperedgesToPairEdges(TINY_HYPERGRAPH.hyperedges),
    sizes: { ...TINY_HYPERGRAPH.sizes },
    hyperedges: TINY_HYPERGRAPH.hyperedges.map((h) => ({ ...h, pins: [...h.pins] })),
  };
}

createInteractiveGraphLab(root, {
  graph: hyperGraph(),
  getGraph: hyperGraph,
  initialAssignment: Object.fromEntries(["A", "B", "C", "D", "E"].map((n) => [n, n])),
  revealAssignment: GOLDEN,
  actionSet: "none",
  cutFn: (asn, g) => hyperedgeCut(asn, g.hyperedges || TINY_HYPERGRAPH.hyperedges),
  initialMeta: { targetK: 2 },
  starterHtml: `
    <p><strong>Your job:</strong> run hypergraph greedy clustering (or edit via Reveal for study).
    Challenges check <em>your</em> hyperedge cut and parts — K=2 teaching cut is 1 (ABC|DE).</p>
  `,
  challenges: [
    {
      id: "hyper-cut-1",
      title: "Hyperedge cut 1",
      level: "Intro",
      prompt: "Reach hyperedge cut 1 (Run K=2 greedy).",
      hint: "Only n3 (C–D) should be cut.",
      check: (_c, api) => api.cutsize() === 1,
    },
    {
      id: "parts-abc-de",
      title: "Parts ABC|DE",
      level: "Intro",
      prompt: "Parts are ABC|DE.",
      hint: "Run K=2.",
      check: (_c, api) => partsString(api.getAssignment()) === "ABC|DE",
    },
    {
      id: "two-clusters",
      title: "Two clusters",
      level: "Intro",
      prompt: "Exactly two cluster ids.",
      hint: "Target K=2.",
      check: (_c, api) => new Set(Object.values(api.getAssignment())).size === 2,
    },
    {
      id: "n1-uncut",
      title: "n1 uncut",
      level: "Practice",
      prompt: "Pins of n1 (A,B,C) share one cluster.",
      hint: "Triangle net stays together.",
      check: (_c, api) => {
        const a = api.getAssignment();
        return a.A === a.B && a.B === a.C;
      },
    },
    {
      id: "n2-uncut",
      title: "n2 uncut",
      level: "Practice",
      prompt: "Pins of n2 (D,E) share one cluster.",
      hint: "D–E net stays together.",
      check: (_c, api) => api.getAssignment().D === api.getAssignment().E,
    },
    {
      id: "n3-cut",
      title: "n3 is cut",
      level: "Practice",
      prompt: "n3 pins C and D are on different sides; hyper cut 1.",
      hint: "Bridge net.",
      check: (_c, api) => {
        const a = api.getAssignment();
        return a.C !== a.D && api.cutsize() === 1;
      },
    },
    {
      id: "n4-uncut",
      title: "n4 uncut",
      level: "Practice",
      prompt: "n4 pins A and B stay together.",
      hint: "A–B net.",
      check: (_c, api) => api.getAssignment().A === api.getAssignment().B,
    },
    {
      id: "four-hedges",
      title: "Four hyperedges",
      level: "Stretch",
      prompt: "Instance exposes exactly 4 hyperedges (always true on this lab).",
      hint: "TINY_HYPERGRAPH has n1…n4.",
      check: (_c, api) => (api.getGraph().hyperedges || []).length === 4,
    },
    {
      id: "k5-noop",
      title: "K=5 no-op",
      level: "Stretch",
      prompt: "Run K=5; five singleton clusters.",
      hint: "Already at target K.",
      check: (_c, api) => new Set(Object.values(api.getAssignment())).size === 5,
    },
    {
      id: "vs-graph-cut",
      title: "Hyper cut is 1",
      level: "Stretch",
      prompt: "K=2 result has hyperedge cut === 1 with Reveal off.",
      hint: "Not the pairwise graph cut story — check hyper metric.",
      check: (_c, api) => !api.isRevealed() && api.cutsize() === 1 && partsString(api.getAssignment()) === "ABC|DE",
    },
  ],
  extraActions(ctx, api) {
    return [
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Run K=2 greedy",
        onClick: () => {
          const g = api.getGraph();
          const asn = hypergraphGreedyCluster(g.nodes, g.hyperedges, g.sizes, 2);
          api.setAssignment(asn);
          api.setMeta({ targetK: 2 });
          api.setRevealed(false);
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: "Run K=5",
        onClick: () => {
          const g = api.getGraph();
          const asn = hypergraphGreedyCluster(g.nodes, g.hyperedges, g.sizes, 5);
          api.setAssignment(asn);
          api.setMeta({ targetK: 5 });
          api.setRevealed(false);
          ctx.rerender();
        },
      }),
    ];
  },
  extraMetrics(api) {
    return [
      `hyperedge cut: ${api.cutsize()}`,
      `parts: ${partsString(api.getAssignment())}`,
      `hedges: ${(api.getGraph().hyperedges || []).map((h) => h.id).join(",")}`,
    ];
  },
});
