import {
  BAD_SEED,
  EDGE_CRITICALITY,
  partsString,
  timingAwarePartition,
} from "../../assets/clustering-core.js";
import {
  createInteractiveGraphLab,
  el,
} from "../../assets/interactive-graph-lab.js";

const root = document.getElementById("lab-root");
const GOLDEN = { A: "0", B: "0", C: "0", D: "1", E: "1" };

createInteractiveGraphLab(root, {
  initialAssignment: { ...BAD_SEED },
  revealAssignment: GOLDEN,
  initialMeta: { plain: null, weightedCut: null },
  starterHtml: `
    <p><strong>Your job:</strong> from the bad seed, Run timing-aware FM (or Flip/Swap)
    until plain cut 3 / weighted 7 / ABC|DE. Challenges check your assignment metrics.</p>
  `,
  challenges: [
    {
      id: "seed-12",
      title: "Seed cutsize 12",
      level: "Intro",
      prompt: "Workspace seed plain cutsize is 12.",
      hint: "Reset; leave the bad seed.",
      check: (_c, api) => api.cutsize() === 12,
    },
    {
      id: "plain-3",
      title: "Plain cut 3",
      level: "Intro",
      prompt: "Reach plain cutsize 3 (Run timing-aware or edit).",
      hint: "Teaching result matches classic golden bipartition.",
      check: (_c, api) => api.cutsize() === 3,
    },
    {
      id: "weighted-7",
      title: "Weighted cut 7",
      level: "Intro",
      prompt: "After Run timing-aware, weighted (criticality) cut is 7.",
      hint: "Critical edges stay internal; bridges contribute weighted cost.",
      check: (_c, api) => api.getMeta().weightedCut === 7 && api.cutsize() === 3,
    },
    {
      id: "parts-abc-de",
      title: "Parts ABC|DE",
      level: "Practice",
      prompt: "Parts are ABC|DE.",
      hint: "Same communities as cut-3 golden.",
      check: (_c, api) => partsString(api.getAssignment()) === "ABC|DE",
    },
    {
      id: "ab-same",
      title: "Critical A–B uncut",
      level: "Practice",
      prompt: "A and B share a block (crit=5); cutsize 3.",
      hint: "Keep heavy critical edge internal.",
      check: (_c, api) => {
        const a = api.getAssignment();
        return a.A === a.B && api.cutsize() === 3;
      },
    },
    {
      id: "bc-same",
      title: "Critical B–C uncut",
      level: "Practice",
      prompt: "B and C share a block (crit=4); cutsize 3.",
      hint: "Triangle stays together.",
      check: (_c, api) => {
        const a = api.getAssignment();
        return a.B === a.C && api.cutsize() === 3;
      },
    },
    {
      id: "crit-ab-5",
      title: "Criticality A|B = 5",
      level: "Practice",
      prompt: "EDGE_CRITICALITY for A|B equals 5.",
      hint: "Shown in metrics.",
      check: () => EDGE_CRITICALITY["A|B"] === 5,
    },
    {
      id: "crit-bc-4",
      title: "Criticality B|C = 4",
      level: "Stretch",
      prompt: "EDGE_CRITICALITY for B|C equals 4.",
      hint: "Companion to A|B.",
      check: () => EDGE_CRITICALITY["B|C"] === 4,
    },
    {
      id: "better-than-seed",
      title: "Beat seed 12→3",
      level: "Stretch",
      prompt: "Plain cut is 3 (was 12 on seed) with Reveal off.",
      hint: "Hide golden; Run timing-aware or Flip.",
      check: (_c, api) => !api.isRevealed() && api.cutsize() === 3,
    },
    {
      id: "de-same",
      title: "D and E together",
      level: "Stretch",
      prompt: "D and E share a block; cutsize 3.",
      hint: "Teaching golden.",
      check: (_c, api) => {
        const a = api.getAssignment();
        return a.D === a.E && api.cutsize() === 3;
      },
    },
  ],
  extraActions(ctx, api) {
    return [
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Run timing-aware",
        onClick: () => {
          const g = api.getGraph();
          const r = timingAwarePartition(g.nodes, g.edges, BAD_SEED, EDGE_CRITICALITY);
          api.setAssignment(r.assignment);
          api.setMeta({ plain: r.plain, weightedCut: r.weightedCut });
          api.setRevealed(false);
          ctx.rerender();
        },
      }),
    ];
  },
  extraMetrics(api) {
    const m = api.getMeta();
    return [
      `criticality: A|B=${EDGE_CRITICALITY["A|B"]}, B|C=${EDGE_CRITICALITY["B|C"]}`,
      m.weightedCut != null
        ? `last run plain=${m.plain} weighted=${m.weightedCut}`
        : "last run: —",
    ];
  },
});
