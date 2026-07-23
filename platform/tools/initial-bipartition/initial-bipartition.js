import { partsString } from "../../assets/clustering-core.js";
import {
  GOLDEN_BIPART,
  greedyInitialBipartition,
  growBipartition,
  randomBipartition,
} from "../../assets/partitioning-core.js";
import {
  createInteractiveGraphLab,
  el,
  emptyAssignment,
} from "../../assets/interactive-graph-lab.js";

const root = document.getElementById("lab-root");

createInteractiveGraphLab(root, {
  initialAssignment: emptyAssignment(),
  revealAssignment: GOLDEN_BIPART,
  initialMeta: { method: null },
  starterHtml: `
    <p><strong>Your job:</strong> grow / greedy / random initial bipartitions, or Assign sides yourself.
    Challenges check <em>your</em> assignment (grow-from-D → ABC|DE cut 3).</p>
  `,
  challenges: [
    {
      id: "grow-d-cut-3",
      title: "Grow D → cut 3",
      level: "Intro",
      prompt: "Grow from D; cutsize must be 3.",
      hint: "Click Grow from D.",
      check: (_c, api) => api.getMeta().method === "grow-D" && api.cutsize() === 3,
    },
    {
      id: "grow-d-parts",
      title: "Grow D → ABC|DE",
      level: "Intro",
      prompt: "Grow from D yields parts ABC|DE.",
      hint: "Same teaching golden.",
      check: (_c, api) =>
        api.getMeta().method === "grow-D" && partsString(api.getAssignment()) === "ABC|DE",
    },
    {
      id: "grow-e-same",
      title: "Grow E same golden",
      level: "Intro",
      prompt: "Grow from E also yields ABC|DE cut 3.",
      hint: "Click Grow from E.",
      check: (_c, api) =>
        api.getMeta().method === "grow-E" &&
        partsString(api.getAssignment()) === "ABC|DE" &&
        api.cutsize() === 3,
    },
    {
      id: "grow-a-cut-5",
      title: "Grow A → cut 5",
      level: "Practice",
      prompt: "Grow from A yields AB|CDE with cutsize 5.",
      hint: "Seed choice matters.",
      check: (_c, api) =>
        api.getMeta().method === "grow-A" &&
        partsString(api.getAssignment()) === "AB|CDE" &&
        api.cutsize() === 5,
    },
    {
      id: "greedy-parts",
      title: "Greedy AB|CDE",
      level: "Practice",
      prompt: "Run greedy initial; parts are AB|CDE.",
      hint: "Click Greedy initial.",
      check: (_c, api) =>
        api.getMeta().method === "greedy" && partsString(api.getAssignment()) === "AB|CDE",
    },
    {
      id: "greedy-cut-5",
      title: "Greedy cut 5",
      level: "Practice",
      prompt: "Greedy initial cutsize is 5.",
      hint: "Worse than grow-from-D.",
      check: (_c, api) => api.getMeta().method === "greedy" && api.cutsize() === 5,
    },
    {
      id: "random-1-golden",
      title: "Random seed=1 golden",
      level: "Practice",
      prompt: "Random (seed=1) yields ABC|DE cut 3.",
      hint: "Click Random seed=1.",
      check: (_c, api) =>
        api.getMeta().method === "rand-1" &&
        partsString(api.getAssignment()) === "ABC|DE" &&
        api.cutsize() === 3,
    },
    {
      id: "random-4-bad",
      title: "Random seed=4 bad",
      level: "Stretch",
      prompt: "Random (seed=4) yields AD|BCE with cutsize 13.",
      hint: "Click Random seed=4.",
      check: (_c, api) =>
        api.getMeta().method === "rand-4" &&
        partsString(api.getAssignment()) === "AD|BCE" &&
        api.cutsize() === 13,
    },
    {
      id: "two-sides",
      title: "Two labels",
      level: "Stretch",
      prompt: "Assignment uses exactly two labels (all nodes labeled).",
      hint: "Run any method or Assign 0/1 yourself.",
      check: (_c, api) => {
        const vals = Object.values(api.getAssignment());
        return vals.every((v) => v === "0" || v === "1") && new Set(vals).size === 2;
      },
    },
    {
      id: "manual-beats-greedy",
      title: "Beat greedy without reveal",
      level: "Stretch",
      prompt: "Reach cut 3 (better than greedy’s 5) with Reveal off.",
      hint: "Grow from D, or Assign ABC|DE yourself.",
      check: (_c, api) => !api.isRevealed() && api.cutsize() === 3,
    },
  ],
  extraActions(ctx, api) {
    const apply = (asn, method) => {
      api.setAssignment(asn);
      api.setMeta({ method });
      api.setRevealed(false);
      ctx.rerender();
    };
    const g = () => api.getGraph();
    return [
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Grow from D",
        onClick: () => apply(growBipartition(g().nodes, g().edges, "D"), "grow-D"),
      }),
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: "Grow from E",
        onClick: () => apply(growBipartition(g().nodes, g().edges, "E"), "grow-E"),
      }),
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: "Grow from A",
        onClick: () => apply(growBipartition(g().nodes, g().edges, "A"), "grow-A"),
      }),
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: "Greedy initial",
        onClick: () => apply(greedyInitialBipartition(g().nodes, g().edges), "greedy"),
      }),
      el("button", {
        className: "btn btn-ghost",
        type: "button",
        text: "Random seed=1",
        onClick: () => apply(randomBipartition(g().nodes, 1), "rand-1"),
      }),
      el("button", {
        className: "btn btn-ghost",
        type: "button",
        text: "Random seed=4",
        onClick: () => apply(randomBipartition(g().nodes, 4), "rand-4"),
      }),
    ];
  },
  extraMetrics(api) {
    return [`method: ${api.getMeta().method || "— (edit manually)"}`];
  },
});
