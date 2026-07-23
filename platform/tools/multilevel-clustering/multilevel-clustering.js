import {
  BAD_SEED,
  multilevelCluster,
  partsString,
} from "../../assets/clustering-core.js";
import {
  createInteractiveGraphLab,
  el,
} from "../../assets/interactive-graph-lab.js";

const root = document.getElementById("lab-root");
const GOLDEN = { A: "P0", B: "P0", C: "P0", D: "P1", E: "P1" };

createInteractiveGraphLab(root, {
  initialAssignment: { ...BAD_SEED },
  revealAssignment: GOLDEN,
  initialMeta: {},
  starterHtml: `
    <p><strong>Your job:</strong> from the bad seed, Run multilevel (coarsen+FM) or edit sides
    until cutsize is 3 / ABC|DE (labels may be P0/P1). Challenges check your assignment.</p>
  `,
  challenges: [
    {
      id: "cut-3",
      title: "Cutsize 3",
      level: "Intro",
      prompt: "Reach cutsize 3 (Run multilevel or Flip/Swap).",
      hint: "Teaching multilevel lands on cut 3.",
      check: (_c, api) => api.cutsize() === 3,
    },
    {
      id: "parts-abc-de",
      title: "Parts ABC|DE",
      level: "Intro",
      prompt: "Parts string is ABC|DE (any label names).",
      hint: "Communities match the golden bipartition.",
      check: (_c, api) => partsString(api.getAssignment()) === "ABC|DE",
    },
    {
      id: "labels-p0-p1",
      title: "Labels P0 and P1",
      level: "Intro",
      prompt: "After Run multilevel, community labels are exactly P0 and P1.",
      hint: "Multilevel prefixes refined sides as P0/P1.",
      check: (_c, api) => {
        const labs = new Set(Object.values(api.getAssignment()));
        return labs.size === 2 && labs.has("P0") && labs.has("P1");
      },
    },
    {
      id: "abc-same",
      title: "A,B,C together",
      level: "Practice",
      prompt: "A, B, and C share one label; cutsize 3.",
      hint: "Triangle stays together.",
      check: (_c, api) => {
        const a = api.getAssignment();
        return a.A === a.B && a.B === a.C && api.cutsize() === 3;
      },
    },
    {
      id: "de-same",
      title: "D,E together",
      level: "Practice",
      prompt: "D and E share a label; cutsize 3.",
      hint: "Heavy D–E uncut.",
      check: (_c, api) => {
        const a = api.getAssignment();
        return a.D === a.E && api.cutsize() === 3;
      },
    },
    {
      id: "better-than-seed",
      title: "Beat seed cut 12",
      level: "Practice",
      prompt: "Your cutsize is 3 (seed was 12).",
      hint: "Run multilevel from Reset.",
      check: (_c, api) => api.cutsize() === 3,
    },
    {
      id: "two-communities",
      title: "Two communities",
      level: "Practice",
      prompt: "Exactly two cluster labels.",
      hint: "coarseK=2.",
      check: (_c, api) => new Set(Object.values(api.getAssignment())).size === 2,
    },
    {
      id: "ab-uncut",
      title: "A–B uncut",
      level: "Stretch",
      prompt: "A and B same side so heavy edge A–B is uncut; cut 3.",
      hint: "Keep A with B.",
      check: (_c, api) => {
        const a = api.getAssignment();
        return a.A === a.B && api.cutsize() === 3;
      },
    },
    {
      id: "de-uncut",
      title: "D–E uncut",
      level: "Stretch",
      prompt: "D and E same side; cutsize 3.",
      hint: "Companion to A–B.",
      check: (_c, api) => {
        const a = api.getAssignment();
        return a.D === a.E && api.cutsize() === 3;
      },
    },
    {
      id: "bridge-only",
      title: "Bridge-only without reveal",
      level: "Stretch",
      prompt: "ABC|DE cut 3 with Reveal off.",
      hint: "Hide golden; Run multilevel or edit.",
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
        text: "Run multilevel",
        onClick: () => {
          const g = api.getGraph();
          const asn = multilevelCluster(g.nodes, g.edges, g.sizes, 2);
          api.setAssignment(asn);
          api.setRevealed(false);
          ctx.rerender();
        },
      }),
    ];
  },
});
