import { cloneGraph, cutsize, partsString } from "../../assets/clustering-core.js";
import {
  recursiveBisection,
  roundRobinMultiway,
} from "../../assets/partitioning-core.js";
import {
  createChallengeLab,
  drawGraph,
  el,
  metricsBlock,
} from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let graph = cloneGraph();
let result = null;
let mode = null; // recursive | roundrobin
let k = 3;

function arm() {
  graph = cloneGraph();
  result = null;
  mode = null;
}

createChallengeLab(root, {
  starterHtml: `
    <p><strong>Starter example (reference):</strong> recursive multiway <code>k=3</code>
    yields <code>AB|C|DE</code> cut <strong>8</strong>. Naive round-robin
    <code>AD|BE|C</code> has cut <strong>18</strong> — literacy for why structure matters.
    Reload starter to restore the recursive reference.</p>
  `,
  loadStarter() {
    graph = cloneGraph();
    k = 3;
    mode = "recursive";
    result = recursiveBisection(graph.nodes, graph.edges, graph.sizes, 3).assignment;
  },
  challenges: [
    {
      id: "rec-parts",
      title: "Recursive AB|C|DE",
      level: "Intro",
      prompt: "Run recursive k=3; parts are AB|C|DE.",
      hint: "Click Recursive k=3.",
      setup: arm,
      check: () => mode === "recursive" && partsString(result) === "AB|C|DE",
    },
    {
      id: "rec-cut-8",
      title: "Recursive cut 8",
      level: "Intro",
      prompt: "Recursive k=3 cutsize is 8.",
      hint: "Same as recursive-bisection lab.",
      setup: arm,
      check: () => mode === "recursive" && cutsize(result, graph.edges) === 8,
    },
    {
      id: "rec-three",
      title: "Recursive has 3 parts",
      level: "Intro",
      prompt: "Recursive assignment uses exactly 3 labels.",
      hint: "k-way via repeated bisection.",
      setup: arm,
      check: () => mode === "recursive" && new Set(Object.values(result)).size === 3,
    },
    {
      id: "rr-parts",
      title: "Round-robin AD|BE|C",
      level: "Practice",
      prompt: "Round-robin k=3 parts are AD|BE|C.",
      hint: "Alphabetical A,B,C,D,E assigned i%3.",
      setup: arm,
      check: () => mode === "roundrobin" && partsString(result) === "AD|BE|C",
    },
    {
      id: "rr-cut-18",
      title: "Round-robin cut 18",
      level: "Practice",
      prompt: "Round-robin k=3 cutsize is 18.",
      hint: "Cuts almost every edge.",
      setup: arm,
      check: () => mode === "roundrobin" && cutsize(result, graph.edges) === 18,
    },
    {
      id: "rr-worse",
      title: "Round-robin worse",
      level: "Practice",
      prompt: "With round-robin showing cut 18, confirm recursive reference cut is 8.",
      hint: "Show round-robin; compare to known recursive cut.",
      setup: arm,
      check: () => {
        if (!(mode === "roundrobin" && cutsize(result, graph.edges) === 18)) return false;
        const rec = recursiveBisection(graph.nodes, graph.edges, graph.sizes, 3).assignment;
        return cutsize(rec, graph.edges) === 8;
      },
    },
    {
      id: "rec-ab-uncut",
      title: "Recursive keeps A–B",
      level: "Practice",
      prompt: "After recursive, A and B share a part (edge weight 5 uncut).",
      hint: "Structure-aware partitioning.",
      setup: arm,
      check: () => mode === "recursive" && result.A === result.B,
    },
    {
      id: "rr-ab-cut",
      title: "Round-robin cuts A–B",
      level: "Stretch",
      prompt: "After round-robin, A and B are in different parts.",
      hint: "A→0, B→1 in i%3.",
      setup: arm,
      check: () => mode === "roundrobin" && result.A !== result.B,
    },
    {
      id: "rec-de-uncut",
      title: "Recursive keeps D–E",
      level: "Stretch",
      prompt: "After recursive, D and E share a part.",
      hint: "DE block survives k=3.",
      setup: arm,
      check: () => mode === "recursive" && result.D === result.E,
    },
    {
      id: "gap-10",
      title: "Cut gap is 10",
      level: "Stretch",
      prompt: "Show recursive (cut 8); 18−8=10 gap vs round-robin.",
      hint: "Run recursive; challenge checks both numbers.",
      setup: arm,
      check: () =>
        mode === "recursive" &&
        cutsize(result, graph.edges) === 8 &&
        cutsize(roundRobinMultiway(graph.nodes, 3), graph.edges) === 18,
    },
  ],
  extraActions(ctx) {
    return [
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Recursive k=3",
        onClick: () => {
          k = 3;
          mode = "recursive";
          result = recursiveBisection(graph.nodes, graph.edges, graph.sizes, 3).assignment;
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: "Round-robin k=3",
        onClick: () => {
          k = 3;
          mode = "roundrobin";
          result = roundRobinMultiway(graph.nodes, 3);
          ctx.rerender();
        },
      }),
    ];
  },
  renderWorkspace(ctx) {
    drawGraph(ctx.canvas, graph, { assignment: result || null });
    const lines = [];
    if (!result) {
      lines.push("No assignment — pick recursive or round-robin.");
    } else {
      lines.push(`mode: ${mode} (k=${k})`);
      lines.push(`parts: ${partsString(result)}`);
      lines.push(`cutsize: ${cutsize(result, graph.edges)}`);
      lines.push(`#parts: ${new Set(Object.values(result)).size}`);
    }
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock(lines));
  },
});
