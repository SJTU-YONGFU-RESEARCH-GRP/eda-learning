import {
  BAD_SEED,
  cloneGraph,
  cutsize,
  kernighanLin,
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

function arm() {
  graph = cloneGraph();
  seed = { ...BAD_SEED };
  result = null;
}

createChallengeLab(root, {
  starterHtml: `
    <p><strong>Starter example (reference):</strong> bad seed cuts both heavy edges
    (<strong>cutsize 12</strong>). KL accepts swap <code>(A, D)</code> and lands on
    <strong>cutsize 3</strong> / <code>ABC|DE</code>. Reload starter anytime.</p>
  `,
  loadStarter() {
    graph = cloneGraph();
    seed = { ...BAD_SEED };
    result = kernighanLin(graph.nodes, graph.edges, seed);
  },
  challenges: [
    {
      id: "seed-12",
      title: "Seed cutsize is 12",
      level: "Intro",
      prompt: "Show seed only; cutsize must be 12.",
      hint: "Click Show seed only.",
      setup: arm,
      check: () => !result && cutsize(seed, graph.edges) === 12,
    },
    {
      id: "seed-parts",
      title: "Seed parts AE|BCD",
      level: "Intro",
      prompt: "With seed only, parts are AE|BCD.",
      hint: "BAD_SEED places A and E together.",
      setup: arm,
      check: () => !result && partsString(seed) === "AE|BCD",
    },
    {
      id: "kl-12-to-3",
      title: "KL improves 12 → 3",
      level: "Intro",
      prompt: "Run KL; final cutsize is 3.",
      hint: "One accepted swap repairs both heavy cuts.",
      setup: arm,
      check: () => result && cutsize(result.assignment, graph.edges) === 3,
    },
    {
      id: "kl-swap-ad",
      title: "First swap A↔D",
      level: "Practice",
      prompt: "Pass 0 first accepted swap is A with D.",
      hint: "Look at swaps in the metrics panel.",
      setup: arm,
      check: () => {
        const s = result?.history?.[0]?.swaps?.[0];
        return s && s.a === "A" && s.b === "D";
      },
    },
    {
      id: "kl-gain-9",
      title: "Swap gain is 9",
      level: "Practice",
      prompt: "That A↔D swap has gain g=9.",
      hint: "Gain equals cut reduction on this instance.",
      setup: arm,
      check: () => result?.history?.[0]?.swaps?.[0]?.g === 9,
    },
    {
      id: "kl-bestk-1",
      title: "best_k = 1",
      level: "Practice",
      prompt: "Pass 0 reports best_k=1.",
      hint: "Only the first swap is kept in the optimal prefix.",
      setup: arm,
      check: () => result?.history?.[0]?.bestK === 1,
    },
    {
      id: "kl-bestcum-9",
      title: "bestCum = 9",
      level: "Practice",
      prompt: "Pass 0 best cumulative gain is 9.",
      hint: "Matches the single accepted swap gain.",
      setup: arm,
      check: () => result?.history?.[0]?.bestCum === 9,
    },
    {
      id: "kl-final-parts",
      title: "Final ABC|DE",
      level: "Stretch",
      prompt: "After KL, parts are ABC|DE.",
      hint: "A joins B,C; D joins E.",
      setup: arm,
      check: () => result && partsString(result.assignment) === "ABC|DE",
    },
    {
      id: "kl-pass1-stop",
      title: "Pass 1 stops",
      level: "Stretch",
      prompt: "Pass 1 has improved=false.",
      hint: "Local optimum — no further improving prefix.",
      setup: arm,
      check: () => result?.history?.[1]?.improved === false,
    },
    {
      id: "kl-ab-same",
      title: "A and B same side",
      level: "Stretch",
      prompt: "After KL, A and B share a block.",
      hint: "Heavy A–B is uncut.",
      setup: arm,
      check: () => result && result.assignment.A === result.assignment.B,
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
        text: "Run KL",
        onClick: () => {
          result = kernighanLin(graph.nodes, graph.edges, seed);
          ctx.rerender();
        },
      }),
    ];
  },
  renderWorkspace(ctx) {
    const asn = result ? result.assignment : seed;
    drawGraph(ctx.canvas, graph, { assignment: asn });
    const lines = [
      `cutsize now: ${cutsize(asn, graph.edges)}`,
      `parts: ${partsString(asn)}`,
    ];
    if (result) {
      for (const h of result.history) {
        lines.push(
          `pass ${h.pass}: best_k=${h.bestK} cum=${h.bestCum} cut ${h.cutBefore}→${h.cutAfter} improved=${h.improved}`
        );
        if (h.swaps?.length) {
          lines.push(`  swaps: ${h.swaps.map((s) => `${s.a}/${s.b}(${s.g})`).join(", ")}`);
        }
      }
    } else {
      lines.push("Showing seed only (bad partition).");
      lines.push(`seed: ${JSON.stringify(seed)}`);
    }
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock(lines));
  },
});
