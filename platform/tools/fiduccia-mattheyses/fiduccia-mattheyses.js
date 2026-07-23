import {
  BAD_SEED,
  fiducciaMattheyses,
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
    <p><strong>Your job:</strong> from the bad seed (cut 12), Flip D then A (or Run FM)
    until cutsize is 3 / ABC|DE. Challenges check <em>your</em> assignment.</p>
  `,
  challenges: [
    {
      id: "seed-12",
      title: "Seed cutsize 12",
      level: "Intro",
      prompt: "Workspace seed cutsize must be 12.",
      hint: "Reset workspace; leave the bad seed.",
      check: (_c, api) => api.cutsize() === 12,
    },
    {
      id: "flip-d",
      title: "Flip D first",
      level: "Intro",
      prompt: "From the seed, flip D only — cutsize becomes 9 (D joins E’s side).",
      hint: "Select D, Flip. Parts should be A|BCDE or similar with D moved.",
      check: (_c, api) => {
        const a = api.getAssignment();
        return a.D !== BAD_SEED.D && a.A === BAD_SEED.A && api.cutsize() === 9;
      },
    },
    {
      id: "flip-d-then-a",
      title: "Flip D then A → cut 3",
      level: "Intro",
      prompt: "From the seed, flip D then flip A until cutsize is 3.",
      hint: "Same move order FM accepts. Or Run FM.",
      check: (_c, api) => api.cutsize() === 3 && partsString(api.getAssignment()) === "ABC|DE",
    },
    {
      id: "parts-abc-de",
      title: "Parts ABC|DE",
      level: "Practice",
      prompt: "Reach parts ABC|DE.",
      hint: "Flip D then A from the seed.",
      check: (_c, api) => partsString(api.getAssignment()) === "ABC|DE",
    },
    {
      id: "de-same",
      title: "D and E together",
      level: "Practice",
      prompt: "D and E share a block with cutsize 3.",
      hint: "Heavy D–E stays internal.",
      check: (_c, api) => {
        const a = api.getAssignment();
        return a.D === a.E && api.cutsize() === 3;
      },
    },
    {
      id: "fm-moves-da",
      title: "FM moves D then A",
      level: "Practice",
      prompt: "Run FM; accepted move prefix starts with D then A; cut is 3.",
      hint: "Reset, Run FM — check history in metrics.",
      check: (_c, api) => {
        const m = api.getMeta().history?.[0]?.moves;
        return m && m[0]?.v === "D" && m[1]?.v === "A" && api.cutsize() === 3;
      },
    },
    {
      id: "fm-gains",
      title: "Gains 3 then 6",
      level: "Practice",
      prompt: "After Run FM, move gains are g(D)=3 and g(A)=6; bestCum=9.",
      hint: "Pass 0 best_k=2.",
      check: (_c, api) => {
        const h = api.getMeta().history?.[0];
        return (
          h &&
          h.moves?.[0]?.g === 3 &&
          h.moves?.[1]?.g === 6 &&
          h.bestCum === 9 &&
          h.bestK === 2
        );
      },
    },
    {
      id: "fm-pass1-stop",
      title: "Pass 1 stops",
      level: "Stretch",
      prompt: "After Run FM, pass 1 has improved=false and cut stays 3.",
      hint: "Local optimum after the D,A prefix.",
      check: (_c, api) =>
        api.getMeta().history?.[1]?.improved === false && api.cutsize() === 3,
    },
    {
      id: "manual-not-reveal",
      title: "Cut 3 without reveal",
      level: "Stretch",
      prompt: "Reach ABC|DE cut 3 while Reveal is off.",
      hint: "Hide golden; flip yourself or Run FM.",
      check: (_c, api) =>
        !api.isRevealed() &&
        api.cutsize() === 3 &&
        partsString(api.getAssignment()) === "ABC|DE",
    },
    {
      id: "ab-uncut",
      title: "A–B uncut",
      level: "Stretch",
      prompt: "A and B same side, cutsize 3.",
      hint: "Teaching golden keeps A–B internal.",
      check: (_c, api) => {
        const a = api.getAssignment();
        return a.A === a.B && api.cutsize() === 3;
      },
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
          const result = fiducciaMattheyses(g.nodes, g.edges, BAD_SEED);
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
        if (h.moves?.length) {
          lines.push(`  moves: ${h.moves.map((m) => `${m.v}(${m.g})`).join(", ")}`);
        }
      }
    }
    return lines;
  },
  onClear(api) {
    api.setMeta({ history: null });
  },
});
