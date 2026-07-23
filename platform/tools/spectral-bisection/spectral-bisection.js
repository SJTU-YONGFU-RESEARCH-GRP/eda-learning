import {
  partsString,
  spectralBisection,
} from "../../assets/clustering-core.js";
import {
  createInteractiveGraphLab,
  el,
  emptyAssignment,
} from "../../assets/interactive-graph-lab.js";

const root = document.getElementById("lab-root");
const GOLDEN = { A: "0", B: "0", C: "0", D: "1", E: "1" };

createInteractiveGraphLab(root, {
  initialAssignment: emptyAssignment(),
  revealAssignment: GOLDEN,
  initialMeta: { order: null },
  starterHtml: `
    <p><strong>Your job:</strong> assign sides (or Run spectral) until cutsize is 3 / ABC|DE.
    You can also inspect the Fiedler order after running spectral. Challenges check your assignment.</p>
  `,
  challenges: [
    {
      id: "cut-3",
      title: "Cutsize 3",
      level: "Intro",
      prompt: "Assign a bipartition with cutsize 3 (Run spectral or edit).",
      hint: "Teaching cut is C–D(2)+C–E(1).",
      check: (_c, api) => api.cutsize() === 3,
    },
    {
      id: "parts-abc-de",
      title: "Parts ABC|DE",
      level: "Intro",
      prompt: "Reach parts ABC|DE.",
      hint: "Put A,B,C on 0 and D,E on 1 (or swapped).",
      check: (_c, api) => partsString(api.getAssignment()) === "ABC|DE",
    },
    {
      id: "two-sides",
      title: "Exactly two labels",
      level: "Intro",
      prompt: "Assignment uses exactly two labels 0/1 with all nodes labeled.",
      hint: "Assign every node, then Check.",
      check: (_c, api) => {
        const a = api.getAssignment();
        const vals = Object.values(a);
        return vals.every((v) => v === "0" || v === "1") && new Set(vals).size === 2;
      },
    },
    {
      id: "order-e-lowest",
      title: "E lowest Fiedler",
      level: "Practice",
      prompt: "Run spectral; E has the lowest Fiedler value; assignment cut is 3.",
      hint: "Order endpoints appear in metrics.",
      check: (_c, api) => {
        const order = api.getMeta().order;
        return order && order[0][0] === "E" && api.cutsize() === 3;
      },
    },
    {
      id: "order-a-highest",
      title: "A highest Fiedler",
      level: "Practice",
      prompt: "Run spectral; A has the highest Fiedler value.",
      hint: "Last entry in the sorted order.",
      check: (_c, api) => {
        const order = api.getMeta().order;
        return order && order[order.length - 1][0] === "A";
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
      title: "C with A and B",
      level: "Stretch",
      prompt: "C is on the same side as A and B; parts ABC|DE.",
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
      prompt: "After Run spectral, Fiedler order has exactly 5 pairs.",
      hint: "One value per node.",
      check: (_c, api) => api.getMeta().order?.length === 5,
    },
    {
      id: "bridge-cut",
      title: "Bridge-only cut",
      level: "Stretch",
      prompt: "ABC|DE cut 3 with Reveal off (you assigned or ran spectral).",
      hint: "Hide golden if needed.",
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
          const result = spectralBisection(g.nodes, g.edges, g.sizes);
          api.setAssignment(result.assignment);
          api.setMeta({ order: result.order });
          api.setRevealed(false);
          ctx.rerender();
        },
      }),
    ];
  },
  extraMetrics(api) {
    const lines = [];
    const order = api.getMeta().order;
    if (order) {
      lines.push("Fiedler order (low→high):");
      for (const [n, v] of order) lines.push(`  ${n}: ${v.toFixed(4)}`);
    }
    return lines;
  },
});
