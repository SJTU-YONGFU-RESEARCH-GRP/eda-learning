import { partsString } from "../../assets/clustering-core.js";
import { recursiveBisection } from "../../assets/partitioning-core.js";
import {
  createInteractiveGraphLab,
  el,
  emptyAssignment,
} from "../../assets/interactive-graph-lab.js";

const root = document.getElementById("lab-root");
const GOLDEN_K3 = { A: "0", B: "0", C: "1", D: "2", E: "2" };

createInteractiveGraphLab(root, {
  initialAssignment: emptyAssignment(),
  revealAssignment: GOLDEN_K3,
  actionSet: "bipart",
  initialMeta: { history: null, targetK: 3 },
  starterHtml: `
    <p><strong>Your job:</strong> Run recursive bisection to k=3 or k=4 (or Assign multiway labels).
    Teaching k=3 result: AB|C|DE cut 8. Challenges check <em>your</em> assignment.</p>
  `,
  challenges: [
    {
      id: "k3-parts",
      title: "k=3 parts AB|C|DE",
      level: "Intro",
      prompt: "Run k=3; parts string is AB|C|DE.",
      hint: "Click Run k=3.",
      check: (_c, api) => partsString(api.getAssignment()) === "AB|C|DE",
    },
    {
      id: "k3-cut-8",
      title: "k=3 cutsize 8",
      level: "Intro",
      prompt: "After k=3, multiway cutsize is 8.",
      hint: "Splits the ABC block after first spectral cut.",
      check: (_c, api) => api.cutsize() === 8 && partsString(api.getAssignment()) === "AB|C|DE",
    },
    {
      id: "k3-three-parts",
      title: "Exactly three labels",
      level: "Intro",
      prompt: "k=3 ends with exactly three labels.",
      hint: "Run k=3.",
      check: (_c, api) => new Set(Object.values(api.getAssignment())).size === 3,
    },
    {
      id: "hist-first-abc-de",
      title: "History step 1 ABC|DE",
      level: "Practice",
      prompt: "After Run k=3, history step 1 parts are ABC|DE with cut 3.",
      hint: "First bisection matches the golden bipartition.",
      check: (_c, api) => {
        const h = api.getMeta().history?.[1];
        return h && h.parts === "ABC|DE" && h.cut === 3;
      },
    },
    {
      id: "hist-second-split-abc",
      title: "Step 2 splits ABC",
      level: "Practice",
      prompt: "History step 2 reports split ABC.",
      hint: "Largest part after step 1.",
      check: (_c, api) => api.getMeta().history?.[2]?.split === "ABC",
    },
    {
      id: "ab-together",
      title: "A and B together",
      level: "Practice",
      prompt: "After k=3, A and B share a label.",
      hint: "AB stays as a pair.",
      check: (_c, api) => api.getAssignment().A === api.getAssignment().B,
    },
    {
      id: "de-together",
      title: "D and E together",
      level: "Practice",
      prompt: "After k=3, D and E share a label.",
      hint: "DE block preserved.",
      check: (_c, api) => api.getAssignment().D === api.getAssignment().E,
    },
    {
      id: "k4-parts",
      title: "k=4 parts AB|C|D|E",
      level: "Stretch",
      prompt: "Run k=4; parts are AB|C|D|E.",
      hint: "Click Run k=4.",
      check: (_c, api) => partsString(api.getAssignment()) === "AB|C|D|E",
    },
    {
      id: "k4-cut-13",
      title: "k=4 cutsize 13",
      level: "Stretch",
      prompt: "k=4 cutsize is 13 (splitting DE costs weight 5).",
      hint: "Run k=4.",
      check: (_c, api) => api.cutsize() === 13 && partsString(api.getAssignment()) === "AB|C|D|E",
    },
    {
      id: "k4-four-parts",
      title: "Four parts without reveal",
      level: "Stretch",
      prompt: "Exactly four labels and cut 13 with Reveal off.",
      hint: "Hide golden; Run k=4.",
      check: (_c, api) =>
        !api.isRevealed() &&
        new Set(Object.values(api.getAssignment())).size === 4 &&
        api.cutsize() === 13,
    },
  ],
  extraActions(ctx, api) {
    const run = (k) => {
      const g = api.getGraph();
      const r = recursiveBisection(g.nodes, g.edges, g.sizes, k);
      api.setAssignment(r.assignment);
      api.setMeta({ history: r.history, targetK: k });
      api.setRevealed(false);
      ctx.rerender();
    };
    return [
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Run k=3",
        onClick: () => run(3),
      }),
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: "Run k=4",
        onClick: () => run(4),
      }),
    ];
  },
  extraMetrics(api) {
    const lines = [`targetK: ${api.getMeta().targetK ?? "—"}`];
    for (const h of api.getMeta().history || []) {
      lines.push(
        `step ${h.step}: ${h.event || ""} parts=${h.parts} cut=${h.cut}` +
          (h.split ? ` split=${h.split}` : "")
      );
    }
    return lines;
  },
});
