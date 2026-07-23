import { cloneGraph, cutsize, partsString } from "../../assets/clustering-core.js";
import { recursiveBisection } from "../../assets/partitioning-core.js";
import {
  createChallengeLab,
  drawGraph,
  el,
  metricsBlock,
} from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let graph = cloneGraph();
let result = null;
let targetK = 3;

function arm(k = 3) {
  graph = cloneGraph();
  targetK = k;
  result = null;
}

createChallengeLab(root, {
  starterHtml: `
    <p><strong>Starter example (reference):</strong> recursive bisection to <code>k=3</code>
    first splits <code>ABC|DE</code> (cut 3), then bisects ABC → <code>AB|C|DE</code>
    with <strong>cutsize 8</strong>. Reload starter anytime.</p>
  `,
  loadStarter() {
    arm(3);
    result = recursiveBisection(graph.nodes, graph.edges, graph.sizes, 3);
  },
  challenges: [
    {
      id: "k3-parts",
      title: "k=3 parts AB|C|DE",
      level: "Intro",
      prompt: "Run k=3; parts string is AB|C|DE.",
      hint: "Second bisection splits ABC.",
      setup: () => arm(3),
      check: () => result && partsString(result.assignment) === "AB|C|DE",
    },
    {
      id: "k3-cut-8",
      title: "k=3 cutsize 8",
      level: "Intro",
      prompt: "Run k=3; multiway cutsize is 8.",
      hint: "Cutting C from AB plus bridges to DE.",
      setup: () => arm(3),
      check: () => result && cutsize(result.assignment, graph.edges) === 8,
    },
    {
      id: "k3-three-parts",
      title: "Exactly 3 parts",
      level: "Intro",
      prompt: "k=3 ends with exactly three labels.",
      hint: "Check the parts count.",
      setup: () => arm(3),
      check: () => result && new Set(Object.values(result.assignment)).size === 3,
    },
    {
      id: "hist-first-abc-de",
      title: "Step 1 is ABC|DE",
      level: "Practice",
      prompt: "History step 1 parts are ABC|DE with cut 3.",
      hint: "First spectral bisection of the whole graph.",
      setup: () => arm(3),
      check: () =>
        result?.history?.[1]?.parts === "ABC|DE" && result.history[1].cut === 3,
    },
    {
      id: "hist-second-split-abc",
      title: "Step 2 splits ABC",
      level: "Practice",
      prompt: "History step 2 reports split ABC.",
      hint: "Largest part after step 1.",
      setup: () => arm(3),
      check: () => result?.history?.[2]?.split === "ABC",
    },
    {
      id: "ab-together",
      title: "A and B same part",
      level: "Practice",
      prompt: "After k=3, A and B share a label.",
      hint: "Heaviest edge stays uncut inside AB.",
      setup: () => arm(3),
      check: () => result && result.assignment.A === result.assignment.B,
    },
    {
      id: "de-together",
      title: "D and E same part",
      level: "Practice",
      prompt: "After k=3, D and E share a label.",
      hint: "DE block never re-bisected at k=3.",
      setup: () => arm(3),
      check: () => result && result.assignment.D === result.assignment.E,
    },
    {
      id: "k4-parts",
      title: "k=4 parts AB|C|D|E",
      level: "Stretch",
      prompt: "Run k=4; parts are AB|C|D|E.",
      hint: "Third bisection splits DE.",
      setup: () => arm(4),
      check: () => result && partsString(result.assignment) === "AB|C|D|E",
    },
    {
      id: "k4-cut-13",
      title: "k=4 cutsize 13",
      level: "Stretch",
      prompt: "k=4 cutsize is 13 (splitting DE costs the weight-5 edge).",
      hint: "Click k=4 then Run.",
      setup: () => arm(4),
      check: () => result && cutsize(result.assignment, graph.edges) === 13,
    },
    {
      id: "k4-four-parts",
      title: "Exactly 4 parts",
      level: "Stretch",
      prompt: "k=4 ends with exactly four labels.",
      hint: "AB stays together; C,D,E singletons aside.",
      setup: () => arm(4),
      check: () => result && new Set(Object.values(result.assignment)).size === 4,
    },
  ],
  extraActions(ctx) {
    return [
      el("button", {
        className: "btn btn-ghost",
        type: "button",
        text: "k=3",
        onClick: () => {
          targetK = 3;
          result = null;
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-ghost",
        type: "button",
        text: "k=4",
        onClick: () => {
          targetK = 4;
          result = null;
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Run recursive bisection",
        onClick: () => {
          result = recursiveBisection(graph.nodes, graph.edges, graph.sizes, targetK);
          ctx.rerender();
        },
      }),
    ];
  },
  renderWorkspace(ctx) {
    drawGraph(ctx.canvas, graph, { assignment: result?.assignment || null });
    const lines = [`target k=${targetK}`];
    if (!result) {
      lines.push("No result yet — click Run recursive bisection.");
    } else {
      lines.push(`parts: ${partsString(result.assignment)}`);
      lines.push(`cutsize: ${cutsize(result.assignment, graph.edges)}`);
      lines.push(`#parts: ${new Set(Object.values(result.assignment)).size}`);
      for (const h of result.history) {
        if (h.step === 0) lines.push(`step 0: start ${h.parts}`);
        else lines.push(`step ${h.step}: ${h.event} split=${h.split} → ${h.parts} cut=${h.cut}`);
      }
    }
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock(lines));
  },
});
