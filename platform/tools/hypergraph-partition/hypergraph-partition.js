import {
  BAD_SEED,
  TINY_HYPERGRAPH,
  hyperedgeCut,
  hyperedgesToPairEdges,
  partsString,
} from "../../assets/clustering-core.js";
import { GOLDEN_BIPART, hypergraphBipartition } from "../../assets/partitioning-core.js";
import { createInteractiveGraphLab, el } from "../../assets/interactive-graph-lab.js";

const root = document.getElementById("lab-root");

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
  initialAssignment: { ...BAD_SEED },
  revealAssignment: GOLDEN_BIPART,
  cutFn: (asn, g) => hyperedgeCut(asn, g.hyperedges || TINY_HYPERGRAPH.hyperedges),
  initialMeta: { pairCut: null, history: null },
  starterHtml: `
    <p><strong>Your job:</strong> seed hyper cut is 6 (AE|BCD). Flip/Swap or Run hypergraph FM
    until hyperedge cut is 1 / ABC|DE. Challenges check <em>your</em> assignment.</p>
  `,
  challenges: [
    {
      id: "seed-hyper-6",
      title: "Seed hyper cut 6",
      level: "Intro",
      prompt: "Workspace seed hyperedge cut must be 6.",
      hint: "Reset; leave the bad seed.",
      check: (_c, api) => api.cutsize() === 6,
    },
    {
      id: "seed-parts",
      title: "Seed AE|BCD",
      level: "Intro",
      prompt: "Seed parts string is AE|BCD.",
      hint: "Same shape as graph BAD_SEED.",
      check: (_c, api) => partsString(api.getAssignment()) === "AE|BCD",
    },
    {
      id: "run-hyper-1",
      title: "Hyper cut 1",
      level: "Intro",
      prompt: "Reach hyperedge cut 1 (Run FM or Flip to ABC|DE).",
      hint: "Only n3 should be cut.",
      check: (_c, api) => api.cutsize() === 1,
    },
    {
      id: "run-parts",
      title: "Parts ABC|DE",
      level: "Practice",
      prompt: "Parts are ABC|DE.",
      hint: "Swap A↔D from the seed.",
      check: (_c, api) => partsString(api.getAssignment()) === "ABC|DE",
    },
    {
      id: "n1-uncut",
      title: "n1 uncut",
      level: "Practice",
      prompt: "Pins of n1 (A,B,C) share one side.",
      hint: "Triangle net.",
      check: (_c, api) => {
        const a = api.getAssignment();
        return a.A === a.B && a.B === a.C;
      },
    },
    {
      id: "n2-uncut",
      title: "n2 uncut",
      level: "Practice",
      prompt: "Pins of n2 (D,E) share one side.",
      hint: "D–E net.",
      check: (_c, api) => api.getAssignment().D === api.getAssignment().E,
    },
    {
      id: "n3-cut",
      title: "n3 cut",
      level: "Practice",
      prompt: "n3 pins C and D differ; hyper cut 1.",
      hint: "Bridge net.",
      check: (_c, api) => {
        const a = api.getAssignment();
        return a.C !== a.D && api.cutsize() === 1;
      },
    },
    {
      id: "four-hedges",
      title: "Four hyperedges",
      level: "Stretch",
      prompt: "Instance has exactly 4 hyperedges.",
      hint: "Always true on this lab.",
      check: (_c, api) => (api.getGraph().hyperedges || []).length === 4,
    },
    {
      id: "pair-cut-1",
      title: "Pair cut also 1",
      level: "Stretch",
      prompt: "After Run hypergraph FM, pairCut on clique expansion is 1.",
      hint: "Reset, Run hypergraph FM.",
      check: (_c, api) => api.getMeta().pairCut === 1 && api.cutsize() === 1,
    },
    {
      id: "improves-seed",
      title: "Beat seed without reveal",
      level: "Stretch",
      prompt: "Hyper cut 1 with Reveal off (seed was 6).",
      hint: "Hide golden; Flip or Run FM.",
      check: (_c, api) => !api.isRevealed() && api.cutsize() === 1,
    },
  ],
  extraActions(ctx, api) {
    return [
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Run hypergraph FM",
        onClick: () => {
          const g = api.getGraph();
          const r = hypergraphBipartition(g.nodes, g.hyperedges, BAD_SEED);
          api.setAssignment(r.assignment);
          api.setMeta({ pairCut: r.pairCut, history: r.history });
          api.setRevealed(false);
          ctx.rerender();
        },
      }),
    ];
  },
  extraMetrics(api) {
    return [
      `hyperedge cut: ${api.cutsize()}`,
      `pairCut (last run): ${api.getMeta().pairCut ?? "—"}`,
      `hedges: ${(api.getGraph().hyperedges || []).map((h) => h.id).join(",")}`,
    ];
  },
});
