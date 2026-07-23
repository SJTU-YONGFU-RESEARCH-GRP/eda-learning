import { cloneGraph, cutsize, partsString } from "../../assets/clustering-core.js";
import {
  greedyInitialBipartition,
  growBipartition,
  randomBipartition,
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
let method = null; // random | greedy | grow
let growSeed = "D";
let randSeed = 1;

function arm() {
  graph = cloneGraph();
  result = null;
  method = null;
}

createChallengeLab(root, {
  starterHtml: `
    <p><strong>Starter example (reference):</strong> grow from <code>D</code> reaches
    <code>ABC|DE</code> with <strong>cutsize 3</strong>. Greedy heaviest-edge seed lands on
    <code>AB|CDE</code> cut <strong>5</strong>. Random seed=1 is lucky (<code>ABC|DE</code>).
    Reload starter to restore the grow-from-D reference.</p>
  `,
  loadStarter() {
    graph = cloneGraph();
    method = "grow";
    growSeed = "D";
    result = growBipartition(graph.nodes, graph.edges, growSeed);
  },
  challenges: [
    {
      id: "grow-d-cut-3",
      title: "Grow D → cut 3",
      level: "Intro",
      prompt: "Grow from D; cutsize must be 3.",
      hint: "Click Grow from D.",
      setup: arm,
      check: () => method === "grow" && growSeed === "D" && cutsize(result, graph.edges) === 3,
    },
    {
      id: "grow-d-parts",
      title: "Grow D → ABC|DE",
      level: "Intro",
      prompt: "Grow from D yields parts ABC|DE.",
      hint: "Heavy D–E pulls E into the seed side first.",
      setup: arm,
      check: () => method === "grow" && growSeed === "D" && partsString(result) === "ABC|DE",
    },
    {
      id: "grow-e-same",
      title: "Grow E matches D",
      level: "Intro",
      prompt: "Grow from E also yields ABC|DE cut 3.",
      hint: "Click Grow from E.",
      setup: arm,
      check: () =>
        method === "grow" &&
        growSeed === "E" &&
        partsString(result) === "ABC|DE" &&
        cutsize(result, graph.edges) === 3,
    },
    {
      id: "grow-a-cut-5",
      title: "Grow A → cut 5",
      level: "Practice",
      prompt: "Grow from A yields AB|CDE with cutsize 5.",
      hint: "Seed on the ABC triangle fills A,B first.",
      setup: arm,
      check: () =>
        method === "grow" &&
        growSeed === "A" &&
        partsString(result) === "AB|CDE" &&
        cutsize(result, graph.edges) === 5,
    },
    {
      id: "greedy-parts",
      title: "Greedy AB|CDE",
      level: "Practice",
      prompt: "Run greedy initial; parts are AB|CDE.",
      hint: "Starts with heaviest edge A–B on side 0.",
      setup: arm,
      check: () => method === "greedy" && partsString(result) === "AB|CDE",
    },
    {
      id: "greedy-cut-5",
      title: "Greedy cutsize 5",
      level: "Practice",
      prompt: "Greedy initial cutsize is 5.",
      hint: "Worse than grow-from-D on this instance.",
      setup: arm,
      check: () => method === "greedy" && cutsize(result, graph.edges) === 5,
    },
    {
      id: "random-1-golden",
      title: "Random seed 1 lucky",
      level: "Practice",
      prompt: "Random (seed=1) yields ABC|DE cut 3.",
      hint: "Click Random seed=1.",
      setup: arm,
      check: () =>
        method === "random" &&
        randSeed === 1 &&
        partsString(result) === "ABC|DE" &&
        cutsize(result, graph.edges) === 3,
    },
    {
      id: "random-4-bad",
      title: "Random seed 4 bad",
      level: "Stretch",
      prompt: "Random (seed=4) yields AD|BCE with cutsize 13.",
      hint: "Click Random seed=4 — unlucky cut.",
      setup: arm,
      check: () =>
        method === "random" &&
        randSeed === 4 &&
        partsString(result) === "AD|BCE" &&
        cutsize(result, graph.edges) === 13,
    },
    {
      id: "two-sides",
      title: "Always two sides",
      level: "Stretch",
      prompt: "After any method, assignment uses exactly two labels.",
      hint: "Run grow, greedy, or random first.",
      setup: arm,
      check: () => result && new Set(Object.values(result)).size === 2,
    },
    {
      id: "grow-beats-greedy",
      title: "Grow D beats greedy",
      level: "Stretch",
      prompt: "With grow-from-D showing cut 3, confirm greedy reference cut is 5.",
      hint: "Show grow D; challenges compare to known greedy cut.",
      setup: arm,
      check: () => {
        if (!(method === "grow" && growSeed === "D" && cutsize(result, graph.edges) === 3)) return false;
        const g = greedyInitialBipartition(graph.nodes, graph.edges);
        return cutsize(g, graph.edges) === 5;
      },
    },
  ],
  extraActions(ctx) {
    const run = (m, fn) => {
      method = m;
      result = fn();
      ctx.rerender();
    };
    return [
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Grow from D",
        onClick: () => {
          growSeed = "D";
          run("grow", () => growBipartition(graph.nodes, graph.edges, "D"));
        },
      }),
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: "Grow from E",
        onClick: () => {
          growSeed = "E";
          run("grow", () => growBipartition(graph.nodes, graph.edges, "E"));
        },
      }),
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: "Grow from A",
        onClick: () => {
          growSeed = "A";
          run("grow", () => growBipartition(graph.nodes, graph.edges, "A"));
        },
      }),
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: "Greedy initial",
        onClick: () => run("greedy", () => greedyInitialBipartition(graph.nodes, graph.edges)),
      }),
      el("button", {
        className: "btn btn-ghost",
        type: "button",
        text: "Random seed=1",
        onClick: () => {
          randSeed = 1;
          run("random", () => randomBipartition(graph.nodes, 1));
        },
      }),
      el("button", {
        className: "btn btn-ghost",
        type: "button",
        text: "Random seed=4",
        onClick: () => {
          randSeed = 4;
          run("random", () => randomBipartition(graph.nodes, 4));
        },
      }),
    ];
  },
  renderWorkspace(ctx) {
    drawGraph(ctx.canvas, graph, { assignment: result || null });
    const lines = [];
    if (!result) {
      lines.push("No seed yet — pick grow / greedy / random.");
    } else {
      lines.push(`method: ${method}${method === "grow" ? ` (seed ${growSeed})` : ""}`);
      if (method === "random") lines.push(`rng seed: ${randSeed}`);
      lines.push(`parts: ${partsString(result)}`);
      lines.push(`cutsize: ${cutsize(result, graph.edges)}`);
    }
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock(lines));
  },
});
