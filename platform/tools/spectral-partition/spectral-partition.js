import { partsString, spectralBisection } from "../../assets/clustering-core.js";
import { GOLDEN_BIPART } from "../../assets/partitioning-core.js";
import {
  createInteractiveGraphLab,
  el,
  emptyAssignment,
} from "../../assets/interactive-graph-lab.js";

const root = document.getElementById("lab-root");

createInteractiveGraphLab(root, {
  initialAssignment: emptyAssignment(),
  revealAssignment: GOLDEN_BIPART,
  initialMeta: { order: null },
  starterHtml: `
    <p><strong>Your job:</strong> Assign sides or Run spectral until cutsize 3 / ABC|DE.
    Challenges check <em>your</em> assignment (Fiedler order after Run spectral).</p>
  `,
  challenges: [
    {
      id: "cut-3",
      title: "Cutsize 3",
      level: "Intro",
      prompt: "Reach cutsize 3.",
      hint: "Run spectral or Assign ABC|DE.",
      check: (_c, api) => api.cutsize() === 3,
    },
    {
      id: "parts-abc-de",
      title: "Parts ABC|DE",
      level: "Intro",
      prompt: "Parts are ABC|DE.",
      hint: "Teaching spectral bipartition.",
      check: (_c, api) => partsString(api.getAssignment()) === "ABC|DE",
    },
    {
      id: "two-sides",
      title: "Two labels",
      level: "Intro",
      prompt: "All nodes labeled 0/1 with exactly two labels.",
      hint: "Assign every node.",
      check: (_c, api) => {
        const vals = Object.values(api.getAssignment());
        return vals.every((v) => v === "0" || v === "1") && new Set(vals).size === 2;
      },
    },
    {
      id: "order-e-lowest",
      title: "E lowest Fiedler",
      level: "Practice",
      prompt: "Run spectral; E has the lowest Fiedler value; cut 3.",
      hint: "Order in metrics.",
      check: (_c, api) => api.getMeta().order?.[0]?.[0] === "E" && api.cutsize() === 3,
    },
    {
      id: "order-a-highest",
      title: "A highest Fiedler",
      level: "Practice",
      prompt: "Run spectral; A has the highest Fiedler value.",
      hint: "Last in sorted order.",
      check: (_c, api) => {
        const o = api.getMeta().order;
        return o && o[o.length - 1][0] === "A";
      },
    },
    {
      id: "de-same",
      title: "D and E together",
      level: "Practice",
      prompt: "D and E share a block; cutsize 3.",
      hint: "Heavy D–E uncut.",
      check: (_c, api) => {
        const a = api.getAssignment();
        return a.D === a.E && api.cutsize() === 3;
      },
    },
    {
      id: "ab-same",
      title: "A and B together",
      level: "Practice",
      prompt: "A and B share a block; cutsize 3.",
      hint: "Heavy A–B uncut.",
      check: (_c, api) => {
        const a = api.getAssignment();
        return a.A === a.B && api.cutsize() === 3;
      },
    },
    {
      id: "c-with-ab",
      title: "C with A,B",
      level: "Stretch",
      prompt: "C same side as A and B; parts ABC|DE.",
      hint: "C joins the triangle.",
      check: (_c, api) => {
        const a = api.getAssignment();
        return a.C === a.A && a.A === a.B && partsString(a) === "ABC|DE";
      },
    },
    {
      id: "order-length-5",
      title: "Order length 5",
      level: "Stretch",
      prompt: "After Run spectral, order has 5 pairs.",
      hint: "One per node.",
      check: (_c, api) => api.getMeta().order?.length === 5,
    },
    {
      id: "bridge-cut",
      title: "Bridge cut without reveal",
      level: "Stretch",
      prompt: "ABC|DE cut 3 with Reveal off.",
      hint: "Hide golden.",
      check: (_c, api) =>
        !api.isRevealed() &&
        partsString(api.getAssignment()) === "ABC|DE" &&
        api.cutsize() === 3,
    },
  ],
  extraActions(ctx, api) {
    return [
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Run spectral",
        onClick: () => {
          const g = api.getGraph();
          const r = spectralBisection(g.nodes, g.edges, g.sizes);
          api.setAssignment(r.assignment);
          api.setMeta({ order: r.order });
          api.setRevealed(false);
          ctx.rerender();
        },
      }),
    ];
  },
  extraMetrics(api) {
    const lines = [];
    for (const [n, v] of api.getMeta().order || []) {
      lines.push(`Fiedler ${n}: ${v.toFixed(4)}`);
    }
    return lines;
  },
});
