import {
  BAD_SEED,
  EDGE_CRITICALITY,
  cloneGraph,
  cutsize,
  partsString,
  timingAwarePartition,
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

function arm() {
  graph = cloneGraph();
  seed = { ...BAD_SEED };
  result = null;
}

createChallengeLab(root, {
  starterHtml: `
    <p><strong>Starter example (reference):</strong> timing-aware FM from the bad seed
    yields <code>ABC|DE</code> with <strong>plain cut 3</strong> and
    <strong>weighted cut 7</strong>. Reload starter to restore this reference.</p>
  `,
  loadStarter() {
    graph = cloneGraph();
    seed = { ...BAD_SEED };
    result = timingAwarePartition(graph.nodes, graph.edges, seed, EDGE_CRITICALITY);
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
      id: "plain-3",
      title: "Plain cutsize 3",
      level: "Intro",
      prompt: "Run timing-aware; plain cutsize is 3.",
      hint: "Same communities as unconstrained FM on original weights.",
      setup: arm,
      check: () => result && result.plain === 3,
    },
    {
      id: "weighted-7",
      title: "Weighted cut 7",
      level: "Intro",
      prompt: "Weighted (criticality) cut is 7.",
      hint: "Cut edges scored with criticality multipliers.",
      setup: arm,
      check: () => result && result.weightedCut === 7,
    },
    {
      id: "parts-abc-de",
      title: "Parts ABC|DE",
      level: "Practice",
      prompt: "Final parts are ABC|DE.",
      hint: "Protects critical A–B–C path inside one side.",
      setup: arm,
      check: () => result && partsString(result.assignment) === "ABC|DE",
    },
    {
      id: "ab-same",
      title: "A and B same side",
      level: "Practice",
      prompt: "Critical edge A–B (crit=5) is uncut.",
      hint: "A and B share a block.",
      setup: arm,
      check: () => result && result.assignment.A === result.assignment.B,
    },
    {
      id: "bc-same",
      title: "B and C same side",
      level: "Practice",
      prompt: "Critical edge B–C (crit=4) is uncut.",
      hint: "B and C share a block.",
      setup: arm,
      check: () => result && result.assignment.B === result.assignment.C,
    },
    {
      id: "crit-ab-5",
      title: "Criticality A–B is 5",
      level: "Practice",
      prompt: "EDGE_CRITICALITY for A|B equals 5.",
      hint: "Shown in the metrics panel.",
      setup: arm,
      check: () => EDGE_CRITICALITY["A|B"] === 5,
    },
    {
      id: "crit-bc-4",
      title: "Criticality B–C is 4",
      level: "Stretch",
      prompt: "EDGE_CRITICALITY for B|C equals 4.",
      hint: "Second-most critical edge on the path.",
      setup: arm,
      check: () => EDGE_CRITICALITY["B|C"] === 4,
    },
    {
      id: "better-than-seed",
      title: "Improves seed 12→3",
      level: "Stretch",
      prompt: "After timing-aware, plain cut is 3 (was 12 on seed).",
      hint: "FM on criticality-weighted edges.",
      setup: arm,
      check: () => result && result.plain === 3 && cutsize(seed, graph.edges) === 12,
    },
    {
      id: "de-same",
      title: "D and E same side",
      level: "Stretch",
      prompt: "D and E share a block in the final assignment.",
      hint: "Non-critical heavy edge still ends internal.",
      setup: arm,
      check: () => result && result.assignment.D === result.assignment.E,
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
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Run timing-aware",
        onClick: () => {
          result = timingAwarePartition(graph.nodes, graph.edges, seed, EDGE_CRITICALITY);
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
      "criticality: A|B=5, B|C=4, A|C=1, C|D=3, D|E=1, C|E=1",
    ];
    if (!result) {
      lines.push("Showing seed only (BAD_SEED).");
      lines.push(`parts: ${partsString(seed)}`);
    } else {
      lines.push(`plain cut: ${result.plain}`);
      lines.push(`weighted cut: ${result.weightedCut}`);
      lines.push(`parts: ${partsString(result.assignment)}`);
    }
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock(lines));
  },
});
