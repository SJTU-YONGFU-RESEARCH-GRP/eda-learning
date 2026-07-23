import { partsString } from "../../assets/clustering-core.js";
import { recursiveBisection, roundRobinMultiway } from "../../assets/partitioning-core.js";
import {
  createInteractiveGraphLab,
  el,
  emptyAssignment,
} from "../../assets/interactive-graph-lab.js";

const root = document.getElementById("lab-root");
const GOLDEN = { A: "0", B: "0", C: "1", D: "2", E: "2" };

createInteractiveGraphLab(root, {
  initialAssignment: emptyAssignment(),
  revealAssignment: GOLDEN,
  actionSet: "bipart",
  initialMeta: { mode: null },
  starterHtml: `
    <p><strong>Your job:</strong> compare recursive k=3 (AB|C|DE cut 8) vs round-robin k=3 (cut 18).
    Challenges check <em>your</em> assignment — Run a method or Assign labels yourself.</p>
  `,
  challenges: [
    {
      id: "rec-parts",
      title: "Recursive AB|C|DE",
      level: "Intro",
      prompt: "Run recursive k=3; parts are AB|C|DE.",
      hint: "Click Recursive k=3.",
      check: (_c, api) =>
        api.getMeta().mode === "recursive" && partsString(api.getAssignment()) === "AB|C|DE",
    },
    {
      id: "rec-cut-8",
      title: "Recursive cut 8",
      level: "Intro",
      prompt: "Recursive k=3 cutsize is 8.",
      hint: "Same as recursive-bisection teaching number.",
      check: (_c, api) => api.getMeta().mode === "recursive" && api.cutsize() === 8,
    },
    {
      id: "rec-three",
      title: "Three recursive labels",
      level: "Intro",
      prompt: "Recursive assignment uses exactly 3 labels.",
      hint: "Run recursive k=3.",
      check: (_c, api) =>
        api.getMeta().mode === "recursive" &&
        new Set(Object.values(api.getAssignment())).size === 3,
    },
    {
      id: "rr-parts",
      title: "Round-robin AD|BE|C",
      level: "Practice",
      prompt: "Round-robin k=3 parts are AD|BE|C.",
      hint: "Click Round-robin k=3.",
      check: (_c, api) =>
        api.getMeta().mode === "roundrobin" && partsString(api.getAssignment()) === "AD|BE|C",
    },
    {
      id: "rr-cut-18",
      title: "Round-robin cut 18",
      level: "Practice",
      prompt: "Round-robin k=3 cutsize is 18.",
      hint: "Much worse than recursive.",
      check: (_c, api) => api.getMeta().mode === "roundrobin" && api.cutsize() === 18,
    },
    {
      id: "rr-worse",
      title: "Gap vs recursive",
      level: "Practice",
      prompt: "With round-robin showing cut 18, confirm you understand recursive reference is 8 (check cut===18).",
      hint: "Show round-robin; gap is 10.",
      check: (_c, api) => api.getMeta().mode === "roundrobin" && api.cutsize() === 18,
    },
    {
      id: "rec-ab-uncut",
      title: "Recursive A–B uncut",
      level: "Practice",
      prompt: "After recursive, A and B share a part.",
      hint: "Edge weight 5 stays internal.",
      check: (_c, api) =>
        api.getMeta().mode === "recursive" &&
        api.getAssignment().A === api.getAssignment().B,
    },
    {
      id: "rr-ab-cut",
      title: "Round-robin cuts A–B",
      level: "Stretch",
      prompt: "After round-robin, A and B are in different parts.",
      hint: "Alphabet round-robin separates them.",
      check: (_c, api) =>
        api.getMeta().mode === "roundrobin" &&
        api.getAssignment().A !== api.getAssignment().B,
    },
    {
      id: "rec-de-uncut",
      title: "Recursive D–E uncut",
      level: "Stretch",
      prompt: "After recursive, D and E share a part.",
      hint: "DE block preserved.",
      check: (_c, api) =>
        api.getMeta().mode === "recursive" &&
        api.getAssignment().D === api.getAssignment().E,
    },
    {
      id: "rec-without-reveal",
      title: "Recursive without reveal",
      level: "Stretch",
      prompt: "AB|C|DE cut 8 with Reveal off.",
      hint: "Hide golden; Run recursive k=3.",
      check: (_c, api) =>
        !api.isRevealed() &&
        partsString(api.getAssignment()) === "AB|C|DE" &&
        api.cutsize() === 8,
    },
  ],
  extraActions(ctx, api) {
    return [
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Recursive k=3",
        onClick: () => {
          const g = api.getGraph();
          const r = recursiveBisection(g.nodes, g.edges, g.sizes, 3);
          api.setAssignment(r.assignment);
          api.setMeta({ mode: "recursive" });
          api.setRevealed(false);
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: "Round-robin k=3",
        onClick: () => {
          const g = api.getGraph();
          api.setAssignment(roundRobinMultiway(g.nodes, 3));
          api.setMeta({ mode: "roundrobin" });
          api.setRevealed(false);
          ctx.rerender();
        },
      }),
    ];
  },
  extraMetrics(api) {
    return [`mode: ${api.getMeta().mode || "—"}`, `gap vs recursive: round-robin 18 − recursive 8 = 10`];
  },
});
