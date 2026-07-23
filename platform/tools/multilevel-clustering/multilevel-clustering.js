import {
  BAD_SEED,
  cloneGraph,
  cutsize,
  multilevelCluster,
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

function arm() {
  graph = cloneGraph();
  result = null;
}

createChallengeLab(root, {
  starterHtml: `
    <p><strong>Starter example (reference):</strong> multilevel (greedy coarsen → FM refine)
    lands on <code>P0/P1</code> communities <strong>ABC|DE</strong> with <strong>cutsize 3</strong>.
    Reload starter to restore this reference.</p>
  `,
  loadStarter() {
    graph = cloneGraph();
    result = multilevelCluster(graph.nodes, graph.edges, graph.sizes, 2);
  },
  challenges: [
    {
      id: "cut-3",
      title: "Cutsize is 3",
      level: "Intro",
      prompt: "Run multilevel; cutsize must be 3.",
      hint: "Coarsen + FM refine on this graph.",
      setup: arm,
      check: () => result && cutsize(result, graph.edges) === 3,
    },
    {
      id: "parts-abc-de",
      title: "Parts ABC|DE",
      level: "Intro",
      prompt: "Multilevel assignment groups ABC vs DE.",
      hint: "Same golden as spectral/greedy unconstrained.",
      setup: arm,
      check: () => result && partsString(result) === "ABC|DE",
    },
    {
      id: "labels-p0-p1",
      title: "Labels are P0/P1",
      level: "Intro",
      prompt: "Community labels are exactly P0 and P1.",
      hint: "Multilevel renames FM sides to P{side}.",
      setup: arm,
      check: () => {
        if (!result) return false;
        const labs = new Set(Object.values(result));
        return labs.size === 2 && labs.has("P0") && labs.has("P1");
      },
    },
    {
      id: "abc-same",
      title: "A,B,C same community",
      level: "Practice",
      prompt: "A, B, and C share one P-label.",
      hint: "The coarse community that FM keeps.",
      setup: arm,
      check: () => result && result.A === result.B && result.B === result.C,
    },
    {
      id: "de-same",
      title: "D,E same community",
      level: "Practice",
      prompt: "D and E share the other P-label.",
      hint: "Heavy D–E stays internal.",
      setup: arm,
      check: () => result && result.D === result.E && result.D !== result.A,
    },
    {
      id: "better-than-seed",
      title: "Beats bad seed cut 12",
      level: "Practice",
      prompt: "Multilevel cutsize 3 is far better than BAD_SEED cutsize 12.",
      hint: "Compare mentally to AE|BCD.",
      setup: arm,
      check: () =>
        result && cutsize(result, graph.edges) === 3 && cutsize(BAD_SEED, graph.edges) === 12,
    },
    {
      id: "two-communities",
      title: "Exactly two communities",
      level: "Practice",
      prompt: "coarseK=2 ends with exactly two clusters.",
      hint: "P0 and P1 only.",
      setup: arm,
      check: () => result && new Set(Object.values(result)).size === 2,
    },
    {
      id: "ab-uncut",
      title: "A–B not cut",
      level: "Stretch",
      prompt: "A and B same side so heavy edge A–B is uncut.",
      hint: "Final assignment keeps A with B.",
      setup: arm,
      check: () => result && result.A === result.B,
    },
    {
      id: "de-uncut",
      title: "D–E not cut",
      level: "Stretch",
      prompt: "D and E same side so heavy edge D–E is uncut.",
      hint: "Final assignment keeps D with E.",
      setup: arm,
      check: () => result && result.D === result.E,
    },
    {
      id: "bridge-only",
      title: "Bridge cut only",
      level: "Stretch",
      prompt: "Cutsize 3 with ABC|DE means only C–D/C–E cross the cut.",
      hint: "Confirm parts and cut together.",
      setup: arm,
      check: () =>
        result && partsString(result) === "ABC|DE" && cutsize(result, graph.edges) === 3,
    },
  ],
  extraActions(ctx) {
    return [
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Run multilevel",
        onClick: () => {
          result = multilevelCluster(graph.nodes, graph.edges, graph.sizes, 2);
          ctx.rerender();
        },
      }),
    ];
  },
  renderWorkspace(ctx) {
    drawGraph(ctx.canvas, graph, { assignment: result || null });
    const lines = [];
    if (!result) {
      lines.push("No result yet — click Run multilevel.");
      lines.push(`For contrast, BAD_SEED cutsize=${cutsize(BAD_SEED, graph.edges)}`);
    } else {
      lines.push(`cutsize: ${cutsize(result, graph.edges)}`);
      lines.push(`parts: ${partsString(result)}`);
      lines.push(`labels: ${JSON.stringify(result)}`);
    }
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock(lines));
  },
});
