import {
  cutsize,
  greedyPairMerge,
  partsString,
} from "../../assets/clustering-core.js";
import {
  createInteractiveGraphLab,
  el,
} from "../../assets/interactive-graph-lab.js";

const root = document.getElementById("lab-root");
const GOLDEN = { A: "0", B: "0", C: "0", D: "1", E: "1" };

function runToK(api, k, cap = null) {
  const g = api.getGraph();
  const result = greedyPairMerge(g.nodes, g.edges, g.sizes, k, cap);
  api.setAssignment(result.assignment);
  api.setMeta({ mergeLog: result.mergeLog, targetK: k, capacity: cap, ran: true });
  api.setRevealed(false);
}

createInteractiveGraphLab(root, {
  initialAssignment: Object.fromEntries(["A", "B", "C", "D", "E"].map((n) => [n, n])),
  revealAssignment: GOLDEN,
  actionSet: "none",
  initialMeta: { mergeLog: [], targetK: 2, capacity: null, ran: false },
  starterHtml: `
    <p><strong>Your job:</strong> set target K (and optional capacity), then merge step-by-step or run to K.
    Challenges check <em>your</em> cluster assignment and merge log — not a golden click.</p>
  `,
  challenges: [
    {
      id: "k2-cut3",
      title: "K=2 cutsize 3",
      level: "Intro",
      prompt: "Merge to K=2 (no capacity). Cutsize must be 3 and parts ABC|DE.",
      hint: "Use Run to K=2, or Merge one step three times.",
      check: (_c, api) =>
        cutsize(api.getAssignment(), api.getGraph().edges) === 3 &&
        partsString(api.getAssignment()) === "ABC|DE",
    },
    {
      id: "first-merge-ab",
      title: "First merge is A–B",
      level: "Intro",
      prompt: "After merging toward K=2, the first merge log entry is A–B at weight 5.",
      hint: "Run to K=2 (or one step) so mergeLog[0] is A–B.",
      check: (_c, api) => {
        const m = api.getMeta().mergeLog?.[0];
        return m && ((m.u === "A" && m.v === "B") || (m.u === "B" && m.v === "A")) && m.w === 5;
      },
    },
    {
      id: "three-merges",
      title: "Three merges to K=2",
      level: "Intro",
      prompt: "Reach K=2 with exactly 3 merges in the log (5→2 clusters).",
      hint: "Each merge reduces cluster count by one.",
      check: (_c, api) =>
        api.getMeta().mergeLog?.length === 3 &&
        new Set(Object.values(api.getAssignment())).size === 2,
    },
    {
      id: "k3-count",
      title: "Stop at K=3",
      level: "Practice",
      prompt: "Merge to K=3. End with exactly 3 clusters.",
      hint: "Run to K=3.",
      check: (_c, api) => new Set(Object.values(api.getAssignment())).size === 3,
    },
    {
      id: "k3-parts",
      title: "K=3 is ABC|D|E",
      level: "Practice",
      prompt: "At K=3, parts should be ABC|D|E.",
      hint: "A–B and absorb C happen before D–E when stopping early.",
      check: (_c, api) => partsString(api.getAssignment()) === "ABC|D|E",
    },
    {
      id: "k4-ab",
      title: "K=4 keeps only A–B",
      level: "Practice",
      prompt: "Merge to K=4; expect AB|C|D|E and cutsize 13.",
      hint: "Only the single heaviest merge A–B fires.",
      check: (_c, api) =>
        partsString(api.getAssignment()) === "AB|C|D|E" &&
        cutsize(api.getAssignment(), api.getGraph().edges) === 13,
    },
    {
      id: "k5-noop",
      title: "K=5 is a no-op",
      level: "Practice",
      prompt: "Set K=5 and run; zero merges, five singleton clusters.",
      hint: "Already at target K.",
      check: (_c, api) =>
        (api.getMeta().mergeLog?.length || 0) === 0 &&
        new Set(Object.values(api.getAssignment())).size === 5,
    },
    {
      id: "capacity-2-block",
      title: "Capacity 2 blocks size-3",
      level: "Stretch",
      prompt: "Run K=2 with capacity=2: no cluster size ≥ 3.",
      hint: "Use Run K=2 cap=2.",
      check: (_c, api) => {
        const asn = api.getAssignment();
        const sizes = {};
        for (const [n, c] of Object.entries(asn)) sizes[c] = (sizes[c] || 0) + 1;
        return !Object.values(sizes).some((s) => s >= 3);
      },
    },
    {
      id: "capacity-2-parts",
      title: "Capacity 2 → AB|C|DE",
      level: "Stretch",
      prompt: "K=2 capacity=2 yields AB|C|DE (cutsize 8).",
      hint: "A–B and D–E merge; C stays alone.",
      check: (_c, api) =>
        partsString(api.getAssignment()) === "AB|C|DE" &&
        cutsize(api.getAssignment(), api.getGraph().edges) === 8,
    },
    {
      id: "capacity-3-allows",
      title: "Capacity 3 allows ABC",
      level: "Stretch",
      prompt: "K=2 with capacity=3 recovers ABC|DE cutsize 3.",
      hint: "Size-3 cluster is legal again.",
      check: (_c, api) =>
        partsString(api.getAssignment()) === "ABC|DE" &&
        cutsize(api.getAssignment(), api.getGraph().edges) === 3,
    },
  ],
  extraActions(ctx, api) {
    const presets = [
      ["Run K=2", 2, null],
      ["Run K=3", 3, null],
      ["Run K=4", 4, null],
      ["Run K=5", 5, null],
      ["Run K=2 cap=2", 2, 2],
      ["Run K=2 cap=3", 2, 3],
    ];
    const btns = presets.map(([label, k, cap]) =>
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: label,
        onClick: () => {
          runToK(api, k, cap);
          ctx.rerender();
        },
      })
    );
    btns.push(
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Merge one step",
        onClick: () => {
          const k = api.getMeta().targetK || 2;
          const cap = api.getMeta().capacity;
          const g = api.getGraph();
          const curK = new Set(Object.values(api.getAssignment())).size;
          if (curK <= k) {
            ctx.setStatus("idle", `Already at ${curK} clusters`);
            return;
          }
          const nextK = curK - 1;
          const one = greedyPairMerge(g.nodes, g.edges, g.sizes, nextK, cap);
          api.setAssignment(one.assignment);
          api.setMeta({
            mergeLog: one.mergeLog,
            targetK: k,
            capacity: cap,
            ran: true,
          });
          api.setRevealed(false);
          ctx.rerender();
        },
      })
    );
    return btns;
  },
  extraMetrics(api) {
    const lines = [
      `target K=${api.getMeta().targetK ?? 2}` +
        (api.getMeta().capacity != null ? `, capacity=${api.getMeta().capacity}` : ", capacity=none"),
      `clusters: ${partsString(api.getAssignment())}`,
      `pairwise cut: ${cutsize(api.getAssignment(), api.getGraph().edges)}`,
    ];
    const log = api.getMeta().mergeLog || [];
    if (log.length) {
      lines.push("merges:");
      for (const m of log) lines.push(`  ${m.u}-${m.v} (w=${m.w}) → ${m.into}`);
    }
    return lines;
  },
});
