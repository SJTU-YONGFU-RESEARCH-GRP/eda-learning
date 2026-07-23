import {
  affinityEdgeWeight,
  affinitySharedNeighbors,
  cloneGraph,
} from "../../assets/clustering-core.js";
import {
  createChallengeLab,
  drawGraph,
  el,
  metricsBlock,
} from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let graph = cloneGraph();
let mode = "edge"; // edge | shared | none

function edgeRank() {
  return affinityEdgeWeight(graph.edges);
}
function sharedRank() {
  return affinitySharedNeighbors(graph.nodes, graph.edges);
}
function pairScore(rank, a, b) {
  const hit = rank.find((x) => x[0] === a && x[1] === b);
  return hit ? hit[2] : null;
}
function arm() {
  graph = cloneGraph();
  mode = "none";
}

createChallengeLab(root, {
  starterHtml: `
    <p><strong>Starter example (reference):</strong> five-node weighted graph.
    Edge-weight ranking puts <code>A–B</code> and <code>D–E</code> on top at score <strong>5</strong>.
    Shared-neighbor scoring raises <code>A–B</code> to <strong>6</strong>.
    Use <em>Load starter example</em> anytime to restore this worked reference.</p>
  `,
  loadStarter() {
    graph = cloneGraph();
    mode = "edge";
  },
  challenges: [
    {
      id: "top-edge",
      title: "Top edge-weight pair",
      level: "Intro",
      prompt: "Show edge-weight ranking; top pair must be A–B with score 5.",
      hint: "Tie-break prefers A–B before D–E when both score 5.",
      setup: arm,
      check: () => mode === "edge" && pairScore(edgeRank(), "A", "B") === 5 && edgeRank()[0][0] === "A",
    },
    {
      id: "second-de",
      title: "Second is D–E @ 5",
      level: "Intro",
      prompt: "In edge-weight mode, confirm the second-ranked pair is D–E at score 5.",
      hint: "Same weight as A–B; alphabetical order places D–E second.",
      setup: arm,
      check: () => {
        if (mode !== "edge") return false;
        const r = edgeRank();
        return r[1] && r[1][0] === "D" && r[1][1] === "E" && r[1][2] === 5;
      },
    },
    {
      id: "third-bc",
      title: "Third is B–C @ 4",
      level: "Intro",
      prompt: "In edge-weight mode, confirm B–C ranks third with score 4.",
      hint: "After the two weight-5 edges comes B–C.",
      setup: arm,
      check: () => {
        if (mode !== "edge") return false;
        const r = edgeRank();
        return r[2] && r[2][0] === "B" && r[2][1] === "C" && r[2][2] === 4;
      },
    },
    {
      id: "edge-six-pairs",
      title: "Six edge pairs ranked",
      level: "Intro",
      prompt: "Edge-weight mode ranks exactly the six existing edges.",
      hint: "No invented pairs under pure edge weight.",
      setup: arm,
      check: () => mode === "edge" && edgeRank().length === 6,
    },
    {
      id: "shared-ab",
      title: "Shared A–B = 6",
      level: "Practice",
      prompt: "Switch to shared-neighbor ranking; A–B must score 6.",
      hint: "5 + min(w(A,C), w(B,C)) = 5 + 1.",
      setup: arm,
      check: () => mode === "shared" && pairScore(sharedRank(), "A", "B") === 6,
    },
    {
      id: "shared-de",
      title: "Shared D–E = 6",
      level: "Practice",
      prompt: "In shared mode, D–E also scores 6 (symmetric to A–B).",
      hint: "Shared neighbor C contributes min(2,1)=1 on top of edge weight 5.",
      setup: arm,
      check: () => mode === "shared" && pairScore(sharedRank(), "D", "E") === 6,
    },
    {
      id: "ac-rises",
      title: "A–C rises to 5",
      level: "Practice",
      prompt: "In shared mode, A–C scores 5 (only 1 under edge weight).",
      hint: "Direct 1 + shared via B: min(5,4)=4.",
      setup: arm,
      check: () => mode === "shared" && pairScore(sharedRank(), "A", "C") === 5,
    },
    {
      id: "bc-shared-5",
      title: "B–C shared = 5",
      level: "Practice",
      prompt: "In shared mode, B–C scores 5.",
      hint: "Direct 4 + shared via A: min(5,1)=1.",
      setup: arm,
      check: () => mode === "shared" && pairScore(sharedRank(), "B", "C") === 5,
    },
    {
      id: "cd-rises",
      title: "C–D rises to 3",
      level: "Stretch",
      prompt: "In shared mode, C–D scores 3 (edge weight was only 2).",
      hint: "Shared via E: min(1,5)=1 added to direct 2.",
      setup: arm,
      check: () => mode === "shared" && pairScore(sharedRank(), "C", "D") === 3,
    },
    {
      id: "invented-bd",
      title: "Invented pair B–D",
      level: "Stretch",
      prompt: "Shared mode invents non-edge B–D with score 2. Confirm it.",
      hint: "B and D share C with min(w(B,C), w(D,C)) = min(4,2)=2.",
      setup: arm,
      check: () => mode === "shared" && pairScore(sharedRank(), "B", "D") === 2,
    },
  ],
  extraActions(ctx) {
    return [
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Show edge-weight ranking",
        onClick: () => {
          mode = "edge";
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Show shared-neighbor ranking",
        onClick: () => {
          mode = "shared";
          ctx.rerender();
        },
      }),
    ];
  },
  renderWorkspace(ctx) {
    if (mode === "none") {
      drawGraph(ctx.canvas, graph, {});
      ctx.metrics.innerHTML = "";
      ctx.metrics.append(
        metricsBlock([
          "Challenge armed — pick a ranking button, then Check.",
          "Tip: Load starter example to see the worked reference again.",
        ])
      );
      return;
    }
    const ranked = mode === "edge" ? edgeRank() : sharedRank();
    const top = ranked[0];
    drawGraph(ctx.canvas, graph, {
      highlightPairs: top ? [`${top[0]}|${top[1]}`] : [],
    });
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(
      el("p", {
        text:
          mode === "edge"
            ? "Reference: top A–B @ 5 (tie with D–E)."
            : "Reference: A–B @ 6; A–C rises to 5; non-edges like B–D appear.",
      })
    );
    ctx.metrics.append(
      el("p", {
        text: `Mode: ${mode === "edge" ? "edge-weight" : "shared-neighbor + edge"} (${ranked.length} pairs)`,
      })
    );
    const table = el("table", { className: "rank-table" });
    table.innerHTML =
      "<thead><tr><th>Pair</th><th>Score</th></tr></thead><tbody>" +
      ranked.map(([u, v, s]) => `<tr><td>${u}–${v}</td><td>${s}</td></tr>`).join("") +
      "</tbody>";
    ctx.metrics.append(table);
  },
});
