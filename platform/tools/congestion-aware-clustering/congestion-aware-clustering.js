import {
  BAD_SEED,
  EDGE_CONGESTION,
  cloneGraph,
  congestionAwarePartition,
  cutsize,
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
let seed = { ...BAD_SEED };
let result = null;
let lastLam = null;

function arm() {
  graph = cloneGraph();
  seed = { ...BAD_SEED };
  result = null;
  lastLam = null;
}

function run(lam) {
  lastLam = lam;
  result = congestionAwarePartition(graph.nodes, graph.edges, seed, EDGE_CONGESTION, lam);
}

createChallengeLab(root, {
  starterHtml: `
    <p><strong>Starter example (reference):</strong> from the bad seed, run with
    <strong>λ=5</strong> → plain cut <strong>5</strong>, congestion penalty <strong>0</strong>
    (avoids cutting congested C–D/C–E). Reload starter to restore this reference.</p>
  `,
  loadStarter() {
    graph = cloneGraph();
    seed = { ...BAD_SEED };
    lastLam = 5;
    result = congestionAwarePartition(graph.nodes, graph.edges, seed, EDGE_CONGESTION, 5);
  },
  challenges: [
    {
      id: "seed-12",
      title: "Seed cutsize is 12",
      level: "Intro",
      prompt: "Show seed only; plain cutsize must be 12.",
      hint: "Click Show seed only.",
      setup: arm,
      check: () => !result && cutsize(seed, graph.edges) === 12,
    },
    {
      id: "lam0-plain3",
      title: "λ=0 plain cut 3",
      level: "Intro",
      prompt: "Run λ=0; plain cutsize is 3.",
      hint: "No congestion boost — same as ordinary FM.",
      setup: arm,
      check: () => result && lastLam === 0 && result.plain === 3,
    },
    {
      id: "lam0-pen9",
      title: "λ=0 penalty 9",
      level: "Intro",
      prompt: "λ=0 result has congestion penalty 9 (5+4 on cut bridges).",
      hint: "Cuts both congested edges C–D and C–E.",
      setup: arm,
      check: () => result && lastLam === 0 && result.pen === 9,
    },
    {
      id: "lam0-parts",
      title: "λ=0 parts ABC|DE",
      level: "Practice",
      prompt: "λ=0 lands on ABC|DE.",
      hint: "Classic communities, expensive under congestion.",
      setup: arm,
      check: () => result && lastLam === 0 && partsString(result.assignment) === "ABC|DE",
    },
    {
      id: "lam5-plain5",
      title: "λ=5 plain cut 5",
      level: "Practice",
      prompt: "Run λ=5; plain cutsize is 5.",
      hint: "Trades a worse wire cut to dodge congestion.",
      setup: arm,
      check: () => result && lastLam === 5 && result.plain === 5,
    },
    {
      id: "lam5-pen0",
      title: "λ=5 penalty 0",
      level: "Practice",
      prompt: "λ=5 result has congestion penalty 0.",
      hint: "Does not cut C–D or C–E.",
      setup: arm,
      check: () => result && lastLam === 5 && result.pen === 0,
    },
    {
      id: "lam5-parts",
      title: "λ=5 parts AB|CDE",
      level: "Practice",
      prompt: "λ=5 yields parts AB|CDE.",
      hint: "Keeps congested bridges internal on the CDE side.",
      setup: arm,
      check: () => result && lastLam === 5 && partsString(result.assignment) === "AB|CDE",
    },
    {
      id: "cong-map-cd",
      title: "Congestion C–D is 5",
      level: "Stretch",
      prompt: "EDGE_CONGESTION for C|D equals 5 (check before or after any run).",
      hint: "Look at congestion map in metrics.",
      setup: arm,
      check: () => EDGE_CONGESTION["C|D"] === 5,
    },
    {
      id: "cong-map-ce",
      title: "Congestion C–E is 4",
      level: "Stretch",
      prompt: "EDGE_CONGESTION for C|E equals 4.",
      hint: "Together with C–D these sum to penalty 9 when both cut.",
      setup: arm,
      check: () => EDGE_CONGESTION["C|E"] === 4,
    },
    {
      id: "obj-lam5",
      title: "λ=5 objective is 5",
      level: "Stretch",
      prompt: "λ=5: objective = plain + λ·pen = 5 + 5·0 = 5.",
      hint: "Matches plain when pen is zero.",
      setup: arm,
      check: () => result && lastLam === 5 && result.objective === 5,
    },
  ],
  extraActions(ctx) {
    return [
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: "Show seed only",
        onClick: () => {
          result = null;
          lastLam = null;
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-ghost",
        type: "button",
        text: "Run λ=0",
        onClick: () => {
          run(0);
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Run λ=5",
        onClick: () => {
          run(5);
          ctx.rerender();
        },
      }),
    ];
  },
  renderWorkspace(ctx) {
    const asn = result ? result.assignment : seed;
    drawGraph(ctx.canvas, graph, { assignment: asn });
    const lines = [
      `seed cutsize: ${cutsize(seed, graph.edges)}`,
      `congestion: C|D=${EDGE_CONGESTION["C|D"]}, C|E=${EDGE_CONGESTION["C|E"]} (else 0)`,
    ];
    if (!result) {
      lines.push("Showing seed only (BAD_SEED).");
      lines.push(`parts: ${partsString(seed)}`);
    } else {
      lines.push(`λ=${lastLam}`);
      lines.push(`plain cut: ${result.plain}`);
      lines.push(`congestion pen: ${result.pen}`);
      lines.push(`objective: ${result.objective}`);
      lines.push(`parts: ${partsString(result.assignment)}`);
    }
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock(lines));
  },
});
