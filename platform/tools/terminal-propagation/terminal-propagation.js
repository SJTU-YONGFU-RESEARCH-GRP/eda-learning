import { cloneGraph, cutsize, partsString } from "../../assets/clustering-core.js";
import { terminalPropagation } from "../../assets/partitioning-core.js";
import {
  createChallengeLab,
  drawGraph,
  el,
  metricsBlock,
} from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let graph = cloneGraph();
let result = null;
let termKey = null; // AE | AD

function arm() {
  graph = cloneGraph();
  result = null;
  termKey = null;
}

function run(key, terminals) {
  termKey = key;
  result = terminalPropagation(graph.nodes, graph.edges, terminals);
}

createChallengeLab(root, {
  starterHtml: `
    <p><strong>Starter example (reference):</strong> fix terminals <code>A→0</code>,
    <code>E→1</code>. Propagation assigns free nodes by neighbor affinity and lands on
    <code>ABC|DE</code> with <strong>cutsize 3</strong>. Reload starter anytime.</p>
  `,
  loadStarter() {
    graph = cloneGraph();
    run("AE", { A: "0", E: "1" });
  },
  challenges: [
    {
      id: "ae-parts",
      title: "A/E terminals → ABC|DE",
      level: "Intro",
      prompt: "Propagate with A=0,E=1; parts are ABC|DE.",
      hint: "Click Terminals A/E.",
      setup: arm,
      check: () => termKey === "AE" && partsString(result.assignment) === "ABC|DE",
    },
    {
      id: "ae-cut-3",
      title: "A/E cutsize 3",
      level: "Intro",
      prompt: "A/E propagation cutsize is 3.",
      hint: "Same golden bipartition.",
      setup: arm,
      check: () => termKey === "AE" && cutsize(result.assignment, graph.edges) === 3,
    },
    {
      id: "ae-a-fixed",
      title: "A stays on side 0",
      level: "Intro",
      prompt: "Terminal A remains label 0.",
      hint: "Fixed nodes never flip.",
      setup: arm,
      check: () => termKey === "AE" && result.assignment.A === "0",
    },
    {
      id: "ae-e-fixed",
      title: "E stays on side 1",
      level: "Practice",
      prompt: "Terminal E remains label 1.",
      hint: "Opposite terminal.",
      setup: arm,
      check: () => termKey === "AE" && result.assignment.E === "1",
    },
    {
      id: "ae-b-with-a",
      title: "B joins A",
      level: "Practice",
      prompt: "Free node B takes A's side.",
      hint: "Heavy A–B affinity.",
      setup: arm,
      check: () => termKey === "AE" && result.assignment.B === result.assignment.A,
    },
    {
      id: "ae-d-with-e",
      title: "D joins E",
      level: "Practice",
      prompt: "Free node D takes E's side.",
      hint: "Heavy D–E affinity.",
      setup: arm,
      check: () => termKey === "AE" && result.assignment.D === result.assignment.E,
    },
    {
      id: "ad-same-golden",
      title: "A/D terminals same golden",
      level: "Practice",
      prompt: "Terminals A=0,D=1 also reach ABC|DE cut 3.",
      hint: "Click Terminals A/D.",
      setup: arm,
      check: () =>
        termKey === "AD" &&
        partsString(result.assignment) === "ABC|DE" &&
        cutsize(result.assignment, graph.edges) === 3,
    },
    {
      id: "ad-d-fixed",
      title: "D stays on side 1",
      level: "Stretch",
      prompt: "With A/D terminals, D remains label 1.",
      hint: "D is the fixed terminal now.",
      setup: arm,
      check: () => termKey === "AD" && result.assignment.D === "1",
    },
    {
      id: "two-sides",
      title: "Exactly two sides",
      level: "Stretch",
      prompt: "After either run, assignment uses exactly two labels.",
      hint: "Bipartition with fixed pins.",
      setup: arm,
      check: () => result && new Set(Object.values(result.assignment)).size === 2,
    },
    {
      id: "iters-positive",
      title: "Propagation iterated",
      level: "Stretch",
      prompt: "A/E run reports iters ≥ 1.",
      hint: "Free nodes update across iterations.",
      setup: arm,
      check: () => termKey === "AE" && result.iters >= 1,
    },
  ],
  extraActions(ctx) {
    return [
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Terminals A/E",
        onClick: () => {
          run("AE", { A: "0", E: "1" });
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: "Terminals A/D",
        onClick: () => {
          run("AD", { A: "0", D: "1" });
          ctx.rerender();
        },
      }),
    ];
  },
  renderWorkspace(ctx) {
    drawGraph(ctx.canvas, graph, { assignment: result?.assignment || null });
    const lines = [];
    if (!result) {
      lines.push("No result — pick a terminal pair.");
    } else {
      lines.push(`terminals: ${termKey}`);
      lines.push(`fixed: ${JSON.stringify(result.terminals)}`);
      lines.push(`parts: ${partsString(result.assignment)}`);
      lines.push(`cutsize: ${cutsize(result.assignment, graph.edges)}`);
      lines.push(`iters: ${result.iters}`);
    }
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock(lines));
  },
});
