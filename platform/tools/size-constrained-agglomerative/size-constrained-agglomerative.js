import {
  cloneGraph,
  cutsize,
  greedyPairMerge,
  partsString,
} from "../../assets/clustering-core.js";
import {
  createChallengeLab,
  drawGraph,
  el,
  metricsBlock,
} from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let graph = cloneGraph();
let result = null;
let targetK = 2;
let capacity = 2;

function clusterSizes(asn) {
  const sizes = {};
  for (const [n, c] of Object.entries(asn)) {
    sizes[c] = (sizes[c] || 0) + (graph.sizes[n] || 1);
  }
  return Object.values(sizes);
}

function arm(k, cap = null) {
  graph = cloneGraph();
  targetK = k;
  capacity = cap;
  result = null;
}

function runMerge() {
  result = greedyPairMerge(graph.nodes, graph.edges, graph.sizes, targetK, capacity);
}

createChallengeLab(root, {
  starterHtml: `
    <p><strong>Starter example (reference):</strong> greedy merge with <code>K=2</code> and
    <code>capacity=2</code> yields <code>AB|C|DE</code> with <strong>cutsize 8</strong>
    (cannot form size-3 {A,B,C}). Reload starter to restore this reference.</p>
  `,
  loadStarter() {
    graph = cloneGraph();
    targetK = 2;
    capacity = 2;
    result = greedyPairMerge(graph.nodes, graph.edges, graph.sizes, 2, 2);
  },
  challenges: [
    {
      id: "cap2-cut8",
      title: "Capacity 2 → cutsize 8",
      level: "Intro",
      prompt: "Run K=2 capacity=2; cutsize must be 8.",
      hint: "C cannot join AB under capacity 2.",
      setup: () => arm(2, 2),
      check: () => result && cutsize(result.assignment, graph.edges) === 8,
    },
    {
      id: "cap2-no-size3",
      title: "No cluster size ≥ 3",
      level: "Intro",
      prompt: "With capacity=2, no cluster size is ≥ 3.",
      hint: "Check cluster sizes in metrics.",
      setup: () => arm(2, 2),
      check: () => result && !clusterSizes(result.assignment).some((s) => s >= 3),
    },
    {
      id: "cap2-parts",
      title: "Parts AB|C|DE",
      level: "Intro",
      prompt: "Capacity-2 run ends with parts AB|C|DE.",
      hint: "A–B and D–E merge; C stays alone.",
      setup: () => arm(2, 2),
      check: () => result && partsString(result.assignment) === "AB|C|DE",
    },
    {
      id: "first-merge-ab",
      title: "First merge is A–B",
      level: "Practice",
      prompt: "Under capacity 2, first merge is still A–B at weight 5.",
      hint: "Heaviest legal edge starts the sequence.",
      setup: () => arm(2, 2),
      check: () => {
        const m = result?.mergeLog?.[0];
        return m && ((m.u === "A" && m.v === "B") || (m.u === "B" && m.v === "A")) && m.w === 5;
      },
    },
    {
      id: "two-merges",
      title: "Exactly two merges",
      level: "Practice",
      prompt: "K=2 capacity=2 performs exactly 2 merges (stops before absorbing C).",
      hint: "A–B then D–E; no third merge is legal.",
      setup: () => arm(2, 2),
      check: () => result && result.mergeLog.length === 2,
    },
    {
      id: "unconstrained-cut3",
      title: "Unconstrained cutsize 3",
      level: "Practice",
      prompt: "Run K=2 with capacity=null (or cap=3); get ABC|DE cutsize 3.",
      hint: "Use the K=2 no-cap or K=2 cap=3 preset.",
      setup: () => arm(2, null),
      check: () =>
        result &&
        partsString(result.assignment) === "ABC|DE" &&
        cutsize(result.assignment, graph.edges) === 3,
    },
    {
      id: "cap3-allows",
      title: "Capacity 3 allows ABC",
      level: "Practice",
      prompt: "K=2 capacity=3 recovers unconstrained ABC|DE cutsize 3.",
      hint: "Size-3 cluster is legal again.",
      setup: () => arm(2, 3),
      check: () =>
        result &&
        partsString(result.assignment) === "ABC|DE" &&
        cutsize(result.assignment, graph.edges) === 3,
    },
    {
      id: "k3-cap2",
      title: "K=3 capacity 2",
      level: "Stretch",
      prompt: "Run K=3 capacity=2; expect three clusters and cutsize 8 (AB|C|DE).",
      hint: "Same merges as K=2 cap=2 when target is already 3.",
      setup: () => arm(3, 2),
      check: () =>
        result &&
        new Set(Object.values(result.assignment)).size === 3 &&
        partsString(result.assignment) === "AB|C|DE" &&
        cutsize(result.assignment, graph.edges) === 8,
    },
    {
      id: "compare-delta",
      title: "Capacity costs +5 cut",
      level: "Stretch",
      prompt: "After a capacity-2 run, cutsize is 8 — five worse than unconstrained 3.",
      hint: "Bridge C–D/C–E plus keeping C separate costs more.",
      setup: () => arm(2, 2),
      check: () => result && cutsize(result.assignment, graph.edges) === 8,
    },
    {
      id: "c-alone",
      title: "C stays singleton",
      level: "Stretch",
      prompt: "Under capacity 2, C’s cluster has only C.",
      hint: "Absorbing C into AB would create size 3.",
      setup: () => arm(2, 2),
      check: () => {
        if (!result) return false;
        const lab = result.assignment.C;
        return Object.values(result.assignment).filter((c) => c === lab).length === 1;
      },
    },
  ],
  extraActions(ctx) {
    const presets = [
      ["K=2 cap=2", 2, 2],
      ["K=2 no-cap", 2, null],
      ["K=2 cap=3", 2, 3],
      ["K=3 cap=2", 3, 2],
    ];
    const btns = presets.map(([label, k, cap]) =>
      el("button", {
        className: "btn btn-ghost",
        type: "button",
        text: label,
        onClick: () => {
          targetK = k;
          capacity = cap;
          result = null;
          ctx.rerender();
        },
      })
    );
    btns.push(
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Run constrained merge",
        onClick: () => {
          runMerge();
          ctx.rerender();
        },
      })
    );
    return btns;
  },
  renderWorkspace(ctx) {
    drawGraph(ctx.canvas, graph, { assignment: result?.assignment || null });
    const lines = [];
    lines.push(`target K=${targetK}` + (capacity != null ? `, capacity=${capacity}` : ", capacity=none"));
    if (!result) {
      lines.push("No result yet — set params, then Run constrained merge.");
    } else {
      lines.push(`cutsize: ${cutsize(result.assignment, graph.edges)}`);
      lines.push(`clusters: ${partsString(result.assignment)}`);
      lines.push(`cluster sizes: ${clusterSizes(result.assignment).sort((a, b) => a - b).join(", ")}`);
      lines.push("merges:");
      for (const m of result.mergeLog) lines.push(`  ${m.u}-${m.v} (w=${m.w}) → ${m.into}`);
    }
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock(lines));
  },
});
