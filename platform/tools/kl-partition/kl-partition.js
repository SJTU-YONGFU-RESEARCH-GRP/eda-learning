import { BAD_SEED, kernighanLin, partsString } from "../../assets/clustering-core.js";
import { GOLDEN_BIPART } from "../../assets/partitioning-core.js";
import { createInteractiveGraphLab, el } from "../../assets/interactive-graph-lab.js";

const root = document.getElementById("lab-root");

createInteractiveGraphLab(root, {
  initialAssignment: { ...BAD_SEED },
  revealAssignment: GOLDEN_BIPART,
  initialMeta: { history: null },
  starterHtml: `
    <p><strong>Your job:</strong> from bad seed cut 12, Swap A↔D (or Run KL) until cut 3 / ABC|DE.
    Challenges check <em>your</em> assignment — not a Show-golden click.</p>
  `,
  challenges: [
    {
      id: "seed-12",
      title: "Seed cutsize 12",
      level: "Intro",
      prompt: "Workspace seed cutsize must be 12.",
      hint: "Reset; leave the seed.",
      check: (_c, api) => api.cutsize() === 12,
    },
    {
      id: "seed-parts",
      title: "Seed AE|BCD",
      level: "Intro",
      prompt: "Seed parts are AE|BCD.",
      hint: "A,E vs B,C,D.",
      check: (_c, api) => partsString(api.getAssignment()) === "AE|BCD",
    },
    {
      id: "swap-ad",
      title: "Swap A↔D → cut 3",
      level: "Intro",
      prompt: "From the seed, swap A with D so cutsize becomes 3.",
      hint: "Select A, Shift+click D, Swap — or Run KL.",
      check: (_c, api) => api.cutsize() === 3,
    },
    {
      id: "parts-abc-de",
      title: "Parts ABC|DE",
      level: "Practice",
      prompt: "Reach parts ABC|DE.",
      hint: "Natural result of A↔D from the seed.",
      check: (_c, api) => partsString(api.getAssignment()) === "ABC|DE",
    },
    {
      id: "kl-swap-ad",
      title: "KL records A↔D",
      level: "Practice",
      prompt: "Run KL; pass 0 first swap is A with D (g=9); cut is 3.",
      hint: "Reset then Run KL.",
      check: (_c, api) => {
        const s = api.getMeta().history?.[0]?.swaps?.[0];
        return s && s.a === "A" && s.b === "D" && s.g === 9 && api.cutsize() === 3;
      },
    },
    {
      id: "kl-bestk-1",
      title: "best_k = 1",
      level: "Practice",
      prompt: "After Run KL, pass 0 best_k=1 and bestCum=9.",
      hint: "Only one swap kept.",
      check: (_c, api) => {
        const h = api.getMeta().history?.[0];
        return h && h.bestK === 1 && h.bestCum === 9;
      },
    },
    {
      id: "kl-pass1-stop",
      title: "Pass 1 stops",
      level: "Practice",
      prompt: "After Run KL, pass 1 has improved=false.",
      hint: "Local optimum.",
      check: (_c, api) => api.getMeta().history?.[1]?.improved === false,
    },
    {
      id: "ab-same",
      title: "A and B together",
      level: "Stretch",
      prompt: "A and B share a block; cutsize 3.",
      hint: "Heavy A–B uncut.",
      check: (_c, api) => {
        const a = api.getAssignment();
        return a.A === a.B && api.cutsize() === 3;
      },
    },
    {
      id: "de-same",
      title: "D and E together",
      level: "Stretch",
      prompt: "D and E share a block; cutsize 3.",
      hint: "After A↔D, D joins E.",
      check: (_c, api) => {
        const a = api.getAssignment();
        return a.D === a.E && api.cutsize() === 3;
      },
    },
    {
      id: "manual-not-reveal",
      title: "Cut 3 without reveal",
      level: "Stretch",
      prompt: "ABC|DE cut 3 with Reveal off.",
      hint: "Hide golden; Swap or Run KL.",
      check: (_c, api) =>
        !api.isRevealed() &&
        api.cutsize() === 3 &&
        partsString(api.getAssignment()) === "ABC|DE",
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
          const r = kernighanLin(g.nodes, g.edges, BAD_SEED);
          api.setAssignment(r.assignment);
          api.setMeta({ history: r.history });
          api.setRevealed(false);
          ctx.rerender();
        },
      }),
    ];
  },
  extraMetrics(api) {
    const lines = [];
    for (const h of api.getMeta().history || []) {
      lines.push(
        `pass ${h.pass}: best_k=${h.bestK} cum=${h.bestCum} ${h.cutBefore}→${h.cutAfter}`
      );
      if (h.swaps?.length) {
        lines.push(`  swaps: ${h.swaps.map((s) => `${s.a}/${s.b}(${s.g})`).join(", ")}`);
      }
    }
    return lines;
  },
  onClear(api) {
    api.setMeta({ history: null });
  },
});
