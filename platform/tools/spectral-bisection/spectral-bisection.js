import {
  cloneGraph,
  cutsize,
  partsString,
  spectralBisection,
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

function arm() {
  graph = cloneGraph();
  result = null;
}

createChallengeLab(root, {
  starterHtml: `
    <p><strong>Starter example (reference):</strong> spectral bisection on the five-node graph
    yields <code>ABC|DE</code> with <strong>cutsize 3</strong>. Fiedler order places
    <strong>E</strong> lowest and <strong>A</strong> highest. Reload starter anytime.</p>
  `,
  loadStarter() {
    graph = cloneGraph();
    result = spectralBisection(graph.nodes, graph.edges, graph.sizes);
  },
  challenges: [
    {
      id: "cut-3",
      title: "Cutsize is 3",
      level: "Intro",
      prompt: "Run spectral; cutsize must be 3.",
      hint: "Best balanced split on the Fiedler order.",
      setup: arm,
      check: () => result && cutsize(result.assignment, graph.edges) === 3,
    },
    {
      id: "parts-abc-de",
      title: "Parts ABC|DE",
      level: "Intro",
      prompt: "Spectral assignment groups ABC vs DE.",
      hint: "Same communities as unconstrained greedy.",
      setup: arm,
      check: () => result && partsString(result.assignment) === "ABC|DE",
    },
    {
      id: "two-sides",
      title: "Exactly two sides",
      level: "Intro",
      prompt: "Assignment uses exactly two labels.",
      hint: "Bisection by definition.",
      setup: arm,
      check: () => result && new Set(Object.values(result.assignment)).size === 2,
    },
    {
      id: "order-e-lowest",
      title: "E is lowest Fiedler",
      level: "Practice",
      prompt: "Order endpoints: E has the lowest Fiedler value.",
      hint: "Check order list in metrics (first entry).",
      setup: arm,
      check: () => result?.order?.[0]?.[0] === "E",
    },
    {
      id: "order-a-highest",
      title: "A is highest Fiedler",
      level: "Practice",
      prompt: "Order endpoints: A has the highest Fiedler value.",
      hint: "Last entry in the sorted order.",
      setup: arm,
      check: () => result?.order?.[result.order.length - 1]?.[0] === "A",
    },
    {
      id: "de-same",
      title: "D and E same side",
      level: "Practice",
      prompt: "D and E share a block (heavy edge uncut).",
      hint: "Both sit on the low end of the Fiedler vector.",
      setup: arm,
      check: () => result && result.assignment.D === result.assignment.E,
    },
    {
      id: "ab-same",
      title: "A and B same side",
      level: "Practice",
      prompt: "A and B share a block.",
      hint: "High end of the spectrum.",
      setup: arm,
      check: () => result && result.assignment.A === result.assignment.B,
    },
    {
      id: "c-with-ab",
      title: "C joins ABC",
      level: "Stretch",
      prompt: "C is on the same side as A and B.",
      hint: "Balance + cut prefers ABC over AB|CDE.",
      setup: arm,
      check: () =>
        result &&
        result.assignment.C === result.assignment.A &&
        result.assignment.C === result.assignment.B,
    },
    {
      id: "order-length-5",
      title: "Order lists all five",
      level: "Stretch",
      prompt: "Fiedler order has exactly 5 (node, value) pairs.",
      hint: "One entry per node.",
      setup: arm,
      check: () => result && result.order.length === 5,
    },
    {
      id: "bridge-cut",
      title: "Only bridge edges cut",
      level: "Stretch",
      prompt: "Cutsize 3 equals C–D(2)+C–E(1) — heavy A–B and D–E stay internal.",
      hint: "Confirm A=B and D=E sides, cut=3.",
      setup: arm,
      check: () =>
        result &&
        cutsize(result.assignment, graph.edges) === 3 &&
        result.assignment.A === result.assignment.B &&
        result.assignment.D === result.assignment.E,
    },
  ],
  extraActions(ctx) {
    return [
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Run spectral",
        onClick: () => {
          result = spectralBisection(graph.nodes, graph.edges, graph.sizes);
          ctx.rerender();
        },
      }),
    ];
  },
  renderWorkspace(ctx) {
    drawGraph(ctx.canvas, graph, { assignment: result?.assignment || null });
    const lines = [];
    if (!result) {
      lines.push("No result yet — click Run spectral.");
    } else {
      lines.push(`cutsize: ${cutsize(result.assignment, graph.edges)}`);
      lines.push(`parts: ${partsString(result.assignment)}`);
      lines.push("Fiedler order (low → high):");
      for (const [n, v] of result.order) lines.push(`  ${n}: ${v.toFixed(4)}`);
    }
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock(lines));
  },
});
