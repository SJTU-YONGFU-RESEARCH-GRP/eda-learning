import { cloneGraph, cutsize, labelPropagation } from "../../assets/clustering-core.js";
import {
  createChallengeLab,
  drawGraph,
  el,
  metricsBlock,
} from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let graph = cloneGraph();
let result = null;
let showInit = false;

function arm() {
  graph = cloneGraph();
  result = null;
  showInit = false;
}

function labels() {
  return result?.labels || null;
}

createChallengeLab(root, {
  starterHtml: `
    <p><strong>Starter example (reference):</strong> asynchronous label propagation
    stabilizes in <strong>2</strong> iterations with <strong>cutsize 3</strong>
    (communities {A,B,C} and {D,E}). Reload starter to show this reference anytime.</p>
  `,
  loadStarter() {
    graph = cloneGraph();
    showInit = false;
    result = labelPropagation(graph.nodes, graph.edges);
  },
  challenges: [
    {
      id: "iters-2",
      title: "Stabilize in 2 iters",
      level: "Intro",
      prompt: "Run LP; iters_to_stable must be 2.",
      hint: "Default async order A…E converges quickly on this graph.",
      setup: arm,
      check: () => result && result.iters === 2,
    },
    {
      id: "cut-3",
      title: "Cutsize 3",
      level: "Intro",
      prompt: "After LP, cutsize of the label assignment is 3.",
      hint: "Only the bridge edges between {A,B,C} and {D,E} remain cut.",
      setup: arm,
      check: () => result && cutsize(result.labels, graph.edges) === 3,
    },
    {
      id: "two-communities",
      title: "Two communities",
      level: "Intro",
      prompt: "Exactly two distinct labels remain after LP.",
      hint: "Dense triangle collapses; D–E collapses.",
      setup: arm,
      check: () => result && new Set(Object.values(result.labels)).size === 2,
    },
    {
      id: "abc-same",
      title: "A, B, C share a label",
      level: "Practice",
      prompt: "After LP, A, B, and C all have the same label.",
      hint: "Strong A–B–C affinities pull them together.",
      setup: arm,
      check: () => {
        const L = labels();
        return L && L.A === L.B && L.B === L.C;
      },
    },
    {
      id: "de-same",
      title: "D and E share a label",
      level: "Practice",
      prompt: "After LP, D and E have the same label.",
      hint: "Edge D–E weight 5 dominates.",
      setup: arm,
      check: () => {
        const L = labels();
        return L && L.D === L.E;
      },
    },
    {
      id: "label-b",
      title: "Community label is B",
      level: "Practice",
      prompt: "The {A,B,C} community settles on label B (reference).",
      hint: "Async updates leave B as the surviving label id.",
      setup: arm,
      check: () => {
        const L = labels();
        return L && L.A === "B" && L.B === "B" && L.C === "B";
      },
    },
    {
      id: "label-e",
      title: "Other community is E",
      level: "Practice",
      prompt: "The {D,E} community settles on label E.",
      hint: "Symmetric to the B community on the other side.",
      setup: arm,
      check: () => {
        const L = labels();
        return L && L.D === "E" && L.E === "E";
      },
    },
    {
      id: "a-not-d",
      title: "A and D differ",
      level: "Practice",
      prompt: "After LP, A and D must have different labels (cut crosses C–D / C–E).",
      hint: "They end in opposite communities.",
      setup: arm,
      check: () => {
        const L = labels();
        return L && L.A !== L.D;
      },
    },
    {
      id: "init-five",
      title: "Initial: five labels",
      level: "Stretch",
      prompt: "Show initial labels (before LP). Each node starts as its own label — five communities.",
      hint: "Click Show initial labels.",
      setup: arm,
      check: () => showInit && !result,
    },
    {
      id: "combo",
      title: "Full reference combo",
      level: "Stretch",
      prompt: "Run LP and hit the full golden: iters=2, cutsize=3, labels A/B/C→B and D/E→E.",
      hint: "One Run should satisfy all of it.",
      setup: arm,
      check: () => {
        const L = labels();
        return (
          result &&
          result.iters === 2 &&
          cutsize(L, graph.edges) === 3 &&
          L.A === "B" &&
          L.C === "B" &&
          L.D === "E"
        );
      },
    },
  ],
  extraActions(ctx) {
    return [
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: "Show initial labels",
        onClick: () => {
          showInit = true;
          result = null;
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Run label propagation",
        onClick: () => {
          showInit = false;
          result = labelPropagation(graph.nodes, graph.edges);
          ctx.rerender();
        },
      }),
    ];
  },
  renderWorkspace(ctx) {
    if (showInit && !result) {
      const init = Object.fromEntries(graph.nodes.map((n) => [n, n]));
      drawGraph(ctx.canvas, graph, { assignment: init });
      ctx.metrics.innerHTML = "";
      ctx.metrics.append(
        metricsBlock([
          "Initial: each node is its own label.",
          `labels: ${JSON.stringify(init)}`,
          "num_clusters: 5",
        ])
      );
      return;
    }
    drawGraph(ctx.canvas, graph, { assignment: result?.labels || null });
    const lines = result
      ? [
          `iters_to_stable: ${result.iters}`,
          `cutsize: ${cutsize(result.labels, graph.edges)}`,
          `num_clusters: ${new Set(Object.values(result.labels)).size}`,
          `labels: ${JSON.stringify(result.labels)}`,
        ]
      : ["No result — run LP, or Load starter for the reference."];
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock(lines));
  },
});
