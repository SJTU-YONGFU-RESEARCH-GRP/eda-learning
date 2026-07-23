import {
  BAD_SEED,
  cutsize,
  labelPropagation,
  partsString,
} from "../../assets/clustering-core.js";
import {
  createInteractiveGraphLab,
  el,
} from "../../assets/interactive-graph-lab.js";

const root = document.getElementById("lab-root");
const GOLDEN = { A: "0", B: "0", C: "0", D: "1", E: "1" };

createInteractiveGraphLab(root, {
  initialAssignment: Object.fromEntries(["A", "B", "C", "D", "E"].map((n) => [n, n])),
  revealAssignment: GOLDEN,
  actionSet: "bipart",
  initialMeta: { iters: null, labels: null },
  starterHtml: `
    <p><strong>Your job:</strong> run label propagation (or edit labels via Assign) until
    communities match the teaching result (cut 3, A/B/C share a label). Challenges check your assignment.</p>
  `,
  challenges: [
    {
      id: "init-five",
      title: "Five singleton labels",
      level: "Intro",
      prompt: "After Reset, each node is its own label — five communities.",
      hint: "Do not Run LP yet.",
      check: (_c, api) => new Set(Object.values(api.getAssignment())).size === 5,
    },
    {
      id: "iters-2",
      title: "Stabilizes in 2 iters",
      level: "Intro",
      prompt: "Run LP; iters_to_stable must be 2 and cutsize 3.",
      hint: "Click Run label propagation.",
      check: (_c, api) => api.getMeta().iters === 2 && cutsize(api.getAssignment(), api.getGraph().edges) === 3,
    },
    {
      id: "cut-3",
      title: "LP cutsize 3",
      level: "Intro",
      prompt: "After LP (or manual edit), cutsize of the label assignment is 3.",
      hint: "Run LP or assign communities yourself.",
      check: (_c, api) => cutsize(api.getAssignment(), api.getGraph().edges) === 3,
    },
    {
      id: "two-communities",
      title: "Two communities",
      level: "Practice",
      prompt: "Exactly two distinct labels remain.",
      hint: "Run LP.",
      check: (_c, api) => new Set(Object.values(api.getAssignment())).size === 2,
    },
    {
      id: "abc-same",
      title: "A,B,C same label",
      level: "Practice",
      prompt: "A, B, and C all share one label; cut ≤ 3.",
      hint: "Reference settles ABC on label B.",
      check: (_c, api) => {
        const a = api.getAssignment();
        return a.A === a.B && a.B === a.C && cutsize(a, api.getGraph().edges) <= 3;
      },
    },
    {
      id: "de-same",
      title: "D,E same label",
      level: "Practice",
      prompt: "D and E share a label; cutsize 3.",
      hint: "Reference settles DE on label E.",
      check: (_c, api) => {
        const a = api.getAssignment();
        return a.D === a.E && cutsize(a, api.getGraph().edges) === 3;
      },
    },
    {
      id: "label-b",
      title: "ABC settle on B",
      level: "Practice",
      prompt: "After Run LP, the {A,B,C} community uses label B.",
      hint: "Deterministic async LP reference.",
      check: (_c, api) => {
        const a = api.getAssignment();
        return a.A === "B" && a.B === "B" && a.C === "B";
      },
    },
    {
      id: "label-e",
      title: "DE settle on E",
      level: "Stretch",
      prompt: "After Run LP, D and E use label E.",
      hint: "Companion to label-B challenge.",
      check: (_c, api) => {
        const a = api.getAssignment();
        return a.D === "E" && a.E === "E";
      },
    },
    {
      id: "a-not-d",
      title: "A ≠ D labels",
      level: "Stretch",
      prompt: "A and D have different labels with cutsize 3.",
      hint: "Cut crosses C–D / C–E.",
      check: (_c, api) => {
        const a = api.getAssignment();
        return a.A !== a.D && cutsize(a, api.getGraph().edges) === 3;
      },
    },
    {
      id: "combo",
      title: "Full LP golden",
      level: "Stretch",
      prompt: "iters=2, cutsize=3, labels A/B/C→B and D/E→E (Reveal off).",
      hint: "Run LP from Reset; do not Reveal golden.",
      check: (_c, api) => {
        const a = api.getAssignment();
        return (
          !api.isRevealed() &&
          api.getMeta().iters === 2 &&
          cutsize(a, api.getGraph().edges) === 3 &&
          a.A === "B" &&
          a.B === "B" &&
          a.C === "B" &&
          a.D === "E" &&
          a.E === "E"
        );
      },
    },
  ],
  extraActions(ctx, api) {
    return [
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: "Show initial labels",
        onClick: () => {
          api.setAssignment(Object.fromEntries(["A", "B", "C", "D", "E"].map((n) => [n, n])));
          api.setMeta({ iters: null, labels: null });
          api.setRevealed(false);
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Run label propagation",
        onClick: () => {
          const g = api.getGraph();
          const result = labelPropagation(g.nodes, g.edges);
          api.setAssignment(result.labels);
          api.setMeta({ iters: result.iters, labels: result.labels });
          api.setRevealed(false);
          ctx.rerender();
        },
      }),
    ];
  },
  extraMetrics(api) {
    const lines = [];
    if (api.getMeta().iters != null) lines.push(`iters_to_stable: ${api.getMeta().iters}`);
    lines.push(`communities: ${partsString(api.getAssignment())}`);
    lines.push(`cutsize: ${cutsize(api.getAssignment(), api.getGraph().edges)}`);
    return lines;
  },
});
