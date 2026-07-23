import {
  cloneGraph,
  cutsize,
  greedyPairMerge,
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
let capacity = null;

function parts(asn) {
  const g = {};
  for (const [n, c] of Object.entries(asn)) (g[c] ||= []).push(n);
  return Object.values(g)
    .map((a) => a.sort().join(""))
    .sort()
    .join("|");
}

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
    <p><strong>Starter example (reference):</strong> greedy merge to <code>K=2</code> on the five-node graph
    yields clusters <code>{A,B,C}</code> vs <code>{D,E}</code> with <strong>cutsize 3</strong>.
    Reload the starter anytime to see this reference result.</p>
  `,
  loadStarter() {
    graph = cloneGraph();
    targetK = 2;
    capacity = null;
    result = greedyPairMerge(graph.nodes, graph.edges, graph.sizes, 2);
  },
  challenges: [
    {
      id: "k2-cut3",
      title: "K=2 cutsize 3",
      level: "Intro",
      prompt: "Params are set to K=2 (no capacity). Run merge → cutsize 3 and ABC|DE.",
      hint: "Heaviest merges: A–B, D–E, then absorb C.",
      setup: () => arm(2),
      check: () => result && cutsize(result.assignment, graph.edges) === 3 && parts(result.assignment) === "ABC|DE",
    },
    {
      id: "first-merge-ab",
      title: "First merge is A–B",
      level: "Intro",
      prompt: "Run K=2 merge; first merge log entry must be A–B at weight 5.",
      hint: "Heaviest legal edge starts the greedy sequence.",
      setup: () => arm(2),
      check: () => {
        const m = result?.mergeLog?.[0];
        return m && ((m.u === "A" && m.v === "B") || (m.u === "B" && m.v === "A")) && m.w === 5;
      },
    },
    {
      id: "three-merges",
      title: "Three merges to K=2",
      level: "Intro",
      prompt: "K=2 unconstrained uses exactly 3 merges (5→2 clusters).",
      hint: "Each merge reduces cluster count by one.",
      setup: () => arm(2),
      check: () => result && result.mergeLog.length === 3,
    },
    {
      id: "k3-count",
      title: "Stop at K=3",
      level: "Practice",
      prompt: "Run with K=3 (no capacity). End with exactly 3 clusters.",
      hint: "Fewer merges than the K=2 run.",
      setup: () => arm(3),
      check: () => result && new Set(Object.values(result.assignment)).size === 3,
    },
    {
      id: "k3-parts",
      title: "K=3 is ABC|D|E",
      level: "Practice",
      prompt: "K=3 should leave D and E unmerged: parts ABC|D|E.",
      hint: "A–B and absorb C happen before D–E when stopping early.",
      setup: () => arm(3),
      check: () => result && parts(result.assignment) === "ABC|D|E",
    },
    {
      id: "k4-ab",
      title: "K=4 keeps only A–B",
      level: "Practice",
      prompt: "Run K=4; expect parts AB|C|D|E and cutsize 13.",
      hint: "Only the single heaviest merge A–B fires.",
      setup: () => arm(4),
      check: () =>
        result &&
        parts(result.assignment) === "AB|C|D|E" &&
        cutsize(result.assignment, graph.edges) === 13,
    },
    {
      id: "k5-noop",
      title: "K=5 is a no-op",
      level: "Practice",
      prompt: "Run K=5; zero merges, five singleton clusters.",
      hint: "Already at target K.",
      setup: () => arm(5),
      check: () =>
        result &&
        result.mergeLog.length === 0 &&
        new Set(Object.values(result.assignment)).size === 5,
    },
    {
      id: "capacity-2-block",
      title: "Capacity 2 blocks size-3",
      level: "Stretch",
      prompt: "K=2 with capacity=2: no cluster size ≥ 3.",
      hint: "Absorbing C into AB would create size 3 — illegal.",
      setup: () => arm(2, 2),
      check: () => result && !clusterSizes(result.assignment).some((s) => s >= 3),
    },
    {
      id: "capacity-2-parts",
      title: "Capacity 2 → AB|C|DE",
      level: "Stretch",
      prompt: "K=2 capacity=2 yields AB|C|DE (cutsize 8).",
      hint: "A–B and D–E merge; C stays alone.",
      setup: () => arm(2, 2),
      check: () =>
        result &&
        parts(result.assignment) === "AB|C|DE" &&
        cutsize(result.assignment, graph.edges) === 8,
    },
    {
      id: "capacity-3-allows",
      title: "Capacity 3 allows ABC",
      level: "Stretch",
      prompt: "K=2 with capacity=3 recovers the unconstrained ABC|DE cutsize 3.",
      hint: "Size-3 cluster is legal again.",
      setup: () => arm(2, 3),
      check: () =>
        result &&
        parts(result.assignment) === "ABC|DE" &&
        cutsize(result.assignment, graph.edges) === 3,
    },
  ],
  extraActions(ctx) {
    const presets = [
      ["K=2", 2, null],
      ["K=3", 3, null],
      ["K=4", 4, null],
      ["K=5", 5, null],
      ["K=2 cap=2", 2, 2],
      ["K=2 cap=3", 2, 3],
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
        text: "Run greedy merge",
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
      lines.push("No result yet — set params (or Start a challenge), then Run greedy merge.");
    } else {
      lines.push(`cutsize: ${cutsize(result.assignment, graph.edges)}`);
      lines.push(`clusters: ${parts(result.assignment)}`);
      lines.push("merges:");
      for (const m of result.mergeLog) lines.push(`  ${m.u}-${m.v} (w=${m.w}) → ${m.into}`);
    }
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock(lines));
  },
});
