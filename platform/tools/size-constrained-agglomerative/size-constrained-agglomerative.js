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

function runConstrained(api, k, cap) {
  const g = api.getGraph();
  const result = greedyPairMerge(g.nodes, g.edges, g.sizes, k, cap);
  api.setAssignment(result.assignment);
  api.setMeta({ mergeLog: result.mergeLog, targetK: k, capacity: cap });
  api.setRevealed(false);
}

function clusterSizes(asn) {
  const sizes = {};
  for (const [, c] of Object.entries(asn)) sizes[c] = (sizes[c] || 0) + 1;
  return Object.values(sizes);
}

createInteractiveGraphLab(root, {
  initialAssignment: Object.fromEntries(["A", "B", "C", "D", "E"].map((n) => [n, n])),
  revealAssignment: GOLDEN,
  actionSet: "none",
  initialMeta: { mergeLog: [], targetK: 2, capacity: 2 },
  starterHtml: `
    <p><strong>Your job:</strong> run size-constrained agglomerative merges (capacity limits cluster size).
    Challenges check <em>your</em> assignment — capacity=2 yields AB|C|DE cut 8.</p>
  `,
  challenges: [
    {
      id: "cap2-cut8",
      title: "Capacity-2 cutsize 8",
      level: "Intro",
      prompt: "Run K=2 capacity=2; cutsize must be 8.",
      hint: "Use Run K=2 cap=2.",
      check: (_c, api) => cutsize(api.getAssignment(), api.getGraph().edges) === 8,
    },
    {
      id: "cap2-no-size3",
      title: "No size ≥ 3",
      level: "Intro",
      prompt: "With capacity=2 result loaded, no cluster size is ≥ 3.",
      hint: "Absorbing C into AB would create size 3 — illegal.",
      check: (_c, api) => !clusterSizes(api.getAssignment()).some((s) => s >= 3),
    },
    {
      id: "cap2-parts",
      title: "Parts AB|C|DE",
      level: "Intro",
      prompt: "Capacity-2 run ends with parts AB|C|DE.",
      hint: "A–B and D–E merge; C stays alone.",
      check: (_c, api) => partsString(api.getAssignment()) === "AB|C|DE",
    },
    {
      id: "first-merge-ab",
      title: "First merge A–B",
      level: "Practice",
      prompt: "Under capacity 2, first merge is still A–B at weight 5.",
      hint: "Check merge log after Run K=2 cap=2.",
      check: (_c, api) => {
        const m = api.getMeta().mergeLog?.[0];
        return m && ((m.u === "A" && m.v === "B") || (m.u === "B" && m.v === "A")) && m.w === 5;
      },
    },
    {
      id: "two-merges",
      title: "Exactly two merges",
      level: "Practice",
      prompt: "K=2 capacity=2 performs exactly 2 merges.",
      hint: "Stops before absorbing C.",
      check: (_c, api) => api.getMeta().mergeLog?.length === 2,
    },
    {
      id: "unconstrained-cut3",
      title: "Unconstrained cut 3",
      level: "Practice",
      prompt: "Run K=2 with no capacity; get ABC|DE cutsize 3.",
      hint: "Use Run K=2 no-cap.",
      check: (_c, api) =>
        partsString(api.getAssignment()) === "ABC|DE" &&
        cutsize(api.getAssignment(), api.getGraph().edges) === 3,
    },
    {
      id: "cap3-allows",
      title: "Capacity 3 allows ABC",
      level: "Practice",
      prompt: "K=2 capacity=3 recovers ABC|DE cutsize 3.",
      hint: "Size-3 cluster is legal again.",
      check: (_c, api) =>
        partsString(api.getAssignment()) === "ABC|DE" &&
        cutsize(api.getAssignment(), api.getGraph().edges) === 3,
    },
    {
      id: "k3-cap2",
      title: "K=3 capacity 2",
      level: "Stretch",
      prompt: "Run K=3 capacity=2; expect three clusters and cutsize 8 (AB|C|DE).",
      hint: "Same merges as K=2 cap=2 when already at 3 clusters.",
      check: (_c, api) =>
        new Set(Object.values(api.getAssignment())).size === 3 &&
        cutsize(api.getAssignment(), api.getGraph().edges) === 8 &&
        partsString(api.getAssignment()) === "AB|C|DE",
    },
    {
      id: "compare-delta",
      title: "Capacity costs +5 cut",
      level: "Stretch",
      prompt: "With a capacity-2 result showing cut 8, confirm it is five worse than unconstrained 3.",
      hint: "Run K=2 cap=2; cut must be 8.",
      check: (_c, api) =>
        cutsize(api.getAssignment(), api.getGraph().edges) === 8 &&
        partsString(api.getAssignment()) === "AB|C|DE",
    },
    {
      id: "c-alone",
      title: "C stays alone",
      level: "Stretch",
      prompt: "Under capacity 2, C’s cluster has only C.",
      hint: "C cannot join AB (size 3).",
      check: (_c, api) => {
        const asn = api.getAssignment();
        const cLab = asn.C;
        return Object.entries(asn).filter(([, lab]) => lab === cLab).length === 1;
      },
    },
  ],
  extraActions(ctx, api) {
    return [
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Run K=2 cap=2",
        onClick: () => {
          runConstrained(api, 2, 2);
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: "Run K=2 no-cap",
        onClick: () => {
          runConstrained(api, 2, null);
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: "Run K=2 cap=3",
        onClick: () => {
          runConstrained(api, 2, 3);
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: "Run K=3 cap=2",
        onClick: () => {
          runConstrained(api, 3, 2);
          ctx.rerender();
        },
      }),
    ];
  },
  extraMetrics(api) {
    const lines = [
      `K=${api.getMeta().targetK ?? "?"} cap=${api.getMeta().capacity ?? "none"}`,
      `clusters: ${partsString(api.getAssignment())}`,
      `cut: ${cutsize(api.getAssignment(), api.getGraph().edges)}`,
    ];
    for (const m of api.getMeta().mergeLog || []) {
      lines.push(`merge ${m.u}-${m.v} w=${m.w} → ${m.into}`);
    }
    return lines;
  },
});
