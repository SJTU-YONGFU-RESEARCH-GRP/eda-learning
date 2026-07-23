import {
  BAD_SEED,
  EDGE_CONGESTION,
  congestionAwarePartition,
  partsString,
} from "../../assets/clustering-core.js";
import {
  createInteractiveGraphLab,
  el,
} from "../../assets/interactive-graph-lab.js";

const root = document.getElementById("lab-root");
const GOLDEN_LAM5 = { A: "0", B: "0", C: "1", D: "1", E: "1" };

createInteractiveGraphLab(root, {
  initialAssignment: { ...BAD_SEED },
  revealAssignment: GOLDEN_LAM5,
  initialMeta: { plain: null, pen: null, objective: null, lam: null },
  starterHtml: `
    <p><strong>Your job:</strong> from the bad seed, Run λ=0 or λ=5 (or Flip/Swap) to explore
    congestion-aware cuts. λ=5 teaching result: plain 5, pen 0, AB|CDE. Challenges check your state.</p>
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
      id: "lam0-plain3",
      title: "λ=0 plain cut 3",
      level: "Intro",
      prompt: "Run λ=0; plain cutsize is 3 (and parts ABC|DE).",
      hint: "Ignores congestion — classic FM-style cut.",
      check: (_c, api) =>
        api.getMeta().lam === 0 &&
        api.getMeta().plain === 3 &&
        partsString(api.getAssignment()) === "ABC|DE",
    },
    {
      id: "lam0-pen9",
      title: "λ=0 penalty 9",
      level: "Intro",
      prompt: "After λ=0, congestion penalty is 9 (5+4 on cut bridges).",
      hint: "C–D and C–E are cut under ABC|DE.",
      check: (_c, api) => api.getMeta().lam === 0 && api.getMeta().pen === 9,
    },
    {
      id: "lam5-plain5",
      title: "λ=5 plain cut 5",
      level: "Practice",
      prompt: "Run λ=5; plain cutsize is 5.",
      hint: "Avoids congested bridges.",
      check: (_c, api) => api.getMeta().lam === 5 && api.getMeta().plain === 5,
    },
    {
      id: "lam5-pen0",
      title: "λ=5 penalty 0",
      level: "Practice",
      prompt: "After λ=5, congestion penalty is 0.",
      hint: "No congested edge on the cut.",
      check: (_c, api) => api.getMeta().lam === 5 && api.getMeta().pen === 0,
    },
    {
      id: "lam5-parts",
      title: "λ=5 parts AB|CDE",
      level: "Practice",
      prompt: "λ=5 yields parts AB|CDE.",
      hint: "C joins D,E to spare congested bridges.",
      check: (_c, api) =>
        api.getMeta().lam === 5 && partsString(api.getAssignment()) === "AB|CDE",
    },
    {
      id: "cong-map-cd",
      title: "Congestion C|D = 5",
      level: "Practice",
      prompt: "EDGE_CONGESTION for C|D equals 5 (always true — confirm map).",
      hint: "Shown in metrics.",
      check: () => EDGE_CONGESTION["C|D"] === 5,
    },
    {
      id: "cong-map-ce",
      title: "Congestion C|E = 4",
      level: "Stretch",
      prompt: "EDGE_CONGESTION for C|E equals 4.",
      hint: "Companion to C|D.",
      check: () => EDGE_CONGESTION["C|E"] === 4,
    },
    {
      id: "obj-lam5",
      title: "Objective = 5",
      level: "Stretch",
      prompt: "After λ=5: objective = plain + λ·pen = 5.",
      hint: "5 + 5·0 = 5.",
      check: (_c, api) =>
        api.getMeta().lam === 5 &&
        api.getMeta().objective === 5 &&
        api.getMeta().plain === 5 &&
        api.getMeta().pen === 0,
    },
    {
      id: "manual-lam5-shape",
      title: "AB|CDE without reveal",
      level: "Stretch",
      prompt: "Reach AB|CDE (plain cut 5) with Reveal off — Run λ=5 or Flip.",
      hint: "Hide golden; assign C with D,E.",
      check: (_c, api) =>
        !api.isRevealed() &&
        partsString(api.getAssignment()) === "AB|CDE" &&
        api.cutsize() === 5,
    },
  ],
  extraActions(ctx, api) {
    return [
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: "Run λ=0",
        onClick: () => {
          const g = api.getGraph();
          const r = congestionAwarePartition(g.nodes, g.edges, BAD_SEED, EDGE_CONGESTION, 0);
          api.setAssignment(r.assignment);
          api.setMeta({ plain: r.plain, pen: r.pen, objective: r.objective, lam: 0 });
          api.setRevealed(false);
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Run λ=5",
        onClick: () => {
          const g = api.getGraph();
          const r = congestionAwarePartition(g.nodes, g.edges, BAD_SEED, EDGE_CONGESTION, 5);
          api.setAssignment(r.assignment);
          api.setMeta({ plain: r.plain, pen: r.pen, objective: r.objective, lam: 5 });
          api.setRevealed(false);
          ctx.rerender();
        },
      }),
    ];
  },
  extraMetrics(api) {
    const m = api.getMeta();
    return [
      `cong map: C|D=${EDGE_CONGESTION["C|D"]}, C|E=${EDGE_CONGESTION["C|E"]}`,
      m.lam != null
        ? `last run λ=${m.lam} plain=${m.plain} pen=${m.pen} obj=${m.objective}`
        : "last run: —",
    ];
  },
});
