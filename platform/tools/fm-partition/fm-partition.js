import { BAD_SEED, fiducciaMattheyses, partsString } from "../../assets/clustering-core.js";
import { GOLDEN_BIPART } from "../../assets/partitioning-core.js";
import { createInteractiveGraphLab, el } from "../../assets/interactive-graph-lab.js";

const root = document.getElementById("lab-root");

createInteractiveGraphLab(root, {
  initialAssignment: { ...BAD_SEED },
  revealAssignment: GOLDEN_BIPART,
  initialMeta: { history: null },
  starterHtml: `
    <p><strong>Your job:</strong> from bad seed cut 12, Flip D then A (or Run FM) until cut 3 / ABC|DE.
    Challenges check <em>your</em> assignment.</p>
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
      id: "flip-d-then-a",
      title: "Flip D then A",
      level: "Intro",
      prompt: "From the seed, flip D then A until cutsize is 3 and parts ABC|DE.",
      hint: "Same order FM accepts. Or Run FM.",
      check: (_c, api) => api.cutsize() === 3 && partsString(api.getAssignment()) === "ABC|DE",
    },
    {
      id: "fm-moves-da",
      title: "FM moves D then A",
      level: "Intro",
      prompt: "Run FM; accepted moves start with D then A; cut is 3.",
      hint: "Reset, Run FM.",
      check: (_c, api) => {
        const m = api.getMeta().history?.[0]?.moves;
        return m && m[0]?.v === "D" && m[1]?.v === "A" && api.cutsize() === 3;
      },
    },
    {
      id: "fm-d-gain-3",
      title: "D gain 3",
      level: "Practice",
      prompt: "After Run FM, moving D has gain g=3.",
      hint: "First accepted move.",
      check: (_c, api) => api.getMeta().history?.[0]?.moves?.[0]?.g === 3,
    },
    {
      id: "fm-a-gain-6",
      title: "A gain 6",
      level: "Practice",
      prompt: "After Run FM, moving A has gain g=6.",
      hint: "Second accepted move.",
      check: (_c, api) => api.getMeta().history?.[0]?.moves?.[1]?.g === 6,
    },
    {
      id: "fm-bestk-2",
      title: "best_k = 2",
      level: "Practice",
      prompt: "Pass 0 best_k is 2 and bestCum is 9.",
      hint: "Both moves kept.",
      check: (_c, api) => {
        const h = api.getMeta().history?.[0];
        return h && h.bestK === 2 && h.bestCum === 9;
      },
    },
    {
      id: "parts-abc-de",
      title: "Parts ABC|DE",
      level: "Practice",
      prompt: "Reach parts ABC|DE.",
      hint: "Flip D then A, or Run FM.",
      check: (_c, api) => partsString(api.getAssignment()) === "ABC|DE",
    },
    {
      id: "fm-pass1-stop",
      title: "Pass 1 stops",
      level: "Stretch",
      prompt: "After Run FM, pass 1 has improved=false.",
      hint: "Local optimum.",
      check: (_c, api) => api.getMeta().history?.[1]?.improved === false,
    },
    {
      id: "de-same",
      title: "D and E together",
      level: "Stretch",
      prompt: "D and E share a block; cutsize 3.",
      hint: "Heavy D–E uncut.",
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
      hint: "Hide golden; Flip or Run FM.",
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
        text: "Run FM",
        onClick: () => {
          const g = api.getGraph();
          const r = fiducciaMattheyses(g.nodes, g.edges, BAD_SEED);
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
      if (h.moves?.length) {
        lines.push(`  moves: ${h.moves.map((m) => `${m.v}(${m.g})`).join(", ")}`);
      }
    }
    return lines;
  },
  onClear(api) {
    api.setMeta({ history: null });
  },
});
