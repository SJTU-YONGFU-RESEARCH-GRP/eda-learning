import {
  BAD_SEED,
  cloneGraph,
  cutsize,
  fiducciaMattheyses,
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

function parts(asn) {
  const g = {};
  for (const [n, c] of Object.entries(asn)) (g[c] ||= []).push(n);
  return Object.values(g)
    .map((a) => a.sort().join(""))
    .sort()
    .join("|");
}

createChallengeLab(root, {
  starterHtml: `
    <p><strong>Starter example (reference):</strong> same bad seed (<strong>cutsize 12</strong>).
    FM single-vertex moves reach <strong>cutsize 3</strong> (reference moves include D then A).
    Reload starter to restore the worked reference.</p>
  `,
  loadStarter() {
    graph = cloneGraph();
    seed = { ...BAD_SEED };
    result = fiducciaMattheyses(graph.nodes, graph.edges, seed);
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
      id: "fm-12-to-3",
      title: "FM improves 12 → 3",
      level: "Intro",
      prompt: "Run FM; cutBefore=12 and final cutsize=3.",
      hint: "Pass 0 repairs the bad seed.",
      setup: arm,
      check: () =>
        result &&
        result.history[0]?.cutBefore === 12 &&
        cutsize(result.assignment, graph.edges) === 3,
    },
    {
      id: "fm-moves-da",
      title: "Moves D then A",
      level: "Intro",
      prompt: "Accepted move prefix starts with D then A.",
      hint: "Single-vertex moves, not pairwise swaps.",
      setup: arm,
      check: () => {
        const m = result?.history?.[0]?.moves;
        return m && m.length >= 2 && m[0].v === "D" && m[1].v === "A";
      },
    },
    {
      id: "fm-d-gain-3",
      title: "First move gain 3",
      level: "Practice",
      prompt: "Moving D has gain g=3.",
      hint: "Check moves list: D(3).",
      setup: arm,
      check: () => result?.history?.[0]?.moves?.[0]?.g === 3,
    },
    {
      id: "fm-a-gain-6",
      title: "Second move gain 6",
      level: "Practice",
      prompt: "Moving A has gain g=6.",
      hint: "After D flips, A’s gain becomes 6.",
      setup: arm,
      check: () => result?.history?.[0]?.moves?.[1]?.g === 6,
    },
    {
      id: "fm-bestk-2",
      title: "best_k = 2",
      level: "Practice",
      prompt: "Pass 0 best_k is 2 (both moves kept).",
      hint: "Unlike KL’s single swap, FM’s best prefix length is 2.",
      setup: arm,
      check: () => result?.history?.[0]?.bestK === 2,
    },
    {
      id: "fm-bestcum-9",
      title: "bestCum = 9",
      level: "Practice",
      prompt: "Pass 0 best cumulative gain is 9 (3+6).",
      hint: "Same total improvement as KL’s one swap of gain 9.",
      setup: arm,
      check: () => result?.history?.[0]?.bestCum === 9,
    },
    {
      id: "fm-final-parts",
      title: "Final ABC|DE",
      level: "Stretch",
      prompt: "After FM, parts are ABC|DE.",
      hint: "Same bipartition KL reaches.",
      setup: arm,
      check: () => result && parts(result.assignment) === "ABC|DE",
    },
    {
      id: "fm-pass1-stop",
      title: "Pass 1 stops",
      level: "Stretch",
      prompt: "Pass 1 has improved=false.",
      hint: "Local optimum — no further improving move prefix.",
      setup: arm,
      check: () => result?.history?.[1]?.improved === false,
    },
    {
      id: "fm-de-same",
      title: "D and E same side",
      level: "Stretch",
      prompt: "After FM, D and E share a block (heavy edge uncut).",
      hint: "Final assignment keeps D–E internal.",
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
        text: "Run FM",
        onClick: () => {
          result = fiducciaMattheyses(graph.nodes, graph.edges, seed);
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
      `parts: ${parts(asn)}`,
    ];
    if (result) {
      for (const h of result.history) {
        lines.push(
          `pass ${h.pass}: best_k=${h.bestK} cum=${h.bestCum} cut ${h.cutBefore}→${h.cutAfter} improved=${h.improved}`
        );
        if (h.moves?.length) {
          lines.push(`  moves: ${h.moves.map((m) => `${m.v}(${m.g})`).join(", ")}`);
        }
      }
    } else {
      lines.push("Showing seed only.");
      lines.push(`seed: ${JSON.stringify(seed)}`);
    }
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock(lines));
  },
});
