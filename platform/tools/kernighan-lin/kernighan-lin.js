import {
  BAD_SEED,
  cutsize,
  kernighanLin,
  partsString,
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
  initialMeta: { history: null },
  starterHtml: `
    <p><strong>Your job:</strong> start from the bad seed (cut 12). Flip/swap nodes — or Run KL —
    until cutsize is 3 and parts are ABC|DE. Challenges check <em>your</em> assignment.</p>
  `,
  challenges: [
    {
      id: "seed-12",
      title: "Seed cutsize is 12",
      level: "Intro",
      prompt: "With the workspace seed (no edits), cutsize must be 12.",
      hint: "Reset workspace; do not flip yet.",
      check: (_c, api) => api.cutsize() === 12 && partsString(api.getAssignment()) === "AE|BCD",
    },
    {
      id: "seed-parts",
      title: "Seed parts AE|BCD",
      level: "Intro",
      prompt: "Confirm seed parts are AE|BCD.",
      hint: "A and E share side 0 opposite B,C,D.",
      check: (_c, api) => partsString(api.getAssignment()) === "AE|BCD",
    },
    {
      id: "swap-ad-cut3",
      title: "Swap A↔D → cut 3",
      level: "Intro",
      prompt: "From the seed, swap A with D so cutsize becomes 3.",
      hint: "Select A, Shift+click D, Swap. Or Run KL.",
      check: (_c, api) => api.cutsize() === 3,
    },
    {
      id: "parts-abc-de",
      title: "Reach ABC|DE",
      level: "Practice",
      prompt: "Assign sides so parts are ABC|DE.",
      hint: "After A↔D from the seed you get ABC|DE.",
      check: (_c, api) => partsString(api.getAssignment()) === "ABC|DE",
    },
    {
      id: "ab-same",
      title: "A and B same side",
      level: "Practice",
      prompt: "Heavy edge A–B uncut: A and B share a block, cut ≤ 3.",
      hint: "Keep A with B while repairing the seed.",
      check: (_c, api) => {
        const a = api.getAssignment();
        return a.A === a.B && api.cutsize() <= 3;
      },
    },
    {
      id: "de-same",
      title: "D and E same side",
      level: "Practice",
      prompt: "Heavy edge D–E uncut; cutsize 3.",
      hint: "D should join E after the A↔D swap.",
      check: (_c, api) => {
        const a = api.getAssignment();
        return a.D === a.E && api.cutsize() === 3;
      },
    },
    {
      id: "kl-history-ad",
      title: "KL records A↔D",
      level: "Practice",
      prompt: "Run KL from the seed; pass 0 first swap is A with D (g=9).",
      hint: "Reset, then Run KL — history appears in metrics.",
      check: (_c, api) => {
        const s = api.getMeta().history?.[0]?.swaps?.[0];
        return s && s.a === "A" && s.b === "D" && s.g === 9 && api.cutsize() === 3;
      },
    },
    {
      id: "kl-bestk-1",
      title: "KL best_k = 1",
      level: "Stretch",
      prompt: "After Run KL, pass 0 reports best_k=1 and bestCum=9; cut is 3.",
      hint: "Only the first swap is kept.",
      check: (_c, api) => {
        const h = api.getMeta().history?.[0];
        return h && h.bestK === 1 && h.bestCum === 9 && api.cutsize() === 3;
      },
    },
    {
      id: "manual-not-reveal",
      title: "Golden cut without reveal",
      level: "Stretch",
      prompt: "Reach cutsize 3 and ABC|DE while Reveal is off.",
      hint: "Hide golden if needed; Flip/Swap yourself or Run KL.",
      check: (_c, api) =>
        !api.isRevealed() &&
        api.cutsize() === 3 &&
        partsString(api.getAssignment()) === "ABC|DE",
    },
    {
      id: "bridge-only",
      title: "Only bridge edges cut",
      level: "Stretch",
      prompt: "ABC|DE with cut 3 (C–D + C–E).",
      hint: "Teaching golden bipartition.",
      check: (_c, api) =>
        partsString(api.getAssignment()) === "ABC|DE" && api.cutsize() === 3,
    },
  ],
  extraActions(ctx, api) {
    return [
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Run KL",
        onClick: () => {
          const g = api.getGraph();
          const seed = { ...BAD_SEED };
          const result = kernighanLin(g.nodes, g.edges, seed);
          api.setAssignment(result.assignment);
          api.setMeta({ history: result.history });
          api.setRevealed(false);
          ctx.rerender();
        },
      }),
    ];
  },
  extraMetrics(api) {
    const lines = [];
    const hist = api.getMeta().history;
    if (hist) {
      for (const h of hist) {
        lines.push(
          `pass ${h.pass}: best_k=${h.bestK} cum=${h.bestCum} cut ${h.cutBefore}→${h.cutAfter} improved=${h.improved}`
        );
        if (h.swaps?.length) {
          lines.push(`  swaps: ${h.swaps.map((s) => `${s.a}/${s.b}(${s.g})`).join(", ")}`);
        }
      }
    }
    return lines;
  },
  onClear(api) {
    api.setMeta({ history: null });
  },
});
