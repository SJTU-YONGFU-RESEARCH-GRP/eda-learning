import {
  BAD_SEED,
  affinityEdgeWeight,
  affinitySharedNeighbors,
} from "../../assets/clustering-core.js";
import {
  createInteractiveGraphLab,
  el,
} from "../../assets/interactive-graph-lab.js";

const root = document.getElementById("lab-root");
const GOLDEN = { A: "0", B: "0", C: "0", D: "1", E: "1" };

function rank(api) {
  const g = api.getGraph();
  const mode = api.getMeta().metric || "edge";
  return mode === "shared"
    ? affinitySharedNeighbors(g.nodes, g.edges)
    : affinityEdgeWeight(g.edges);
}

function pairScore(api, a, b) {
  const hit = rank(api).find((x) => x[0] === a && x[1] === b);
  return hit ? hit[2] : null;
}

createInteractiveGraphLab(root, {
  initialAssignment: { ...BAD_SEED },
  revealAssignment: GOLDEN,
  actionSet: "none",
  initialMeta: { metric: "edge", pinned: null },
  starterHtml: `
    <p><strong>Your job:</strong> switch scoring (Edge vs Shared) and pin pairs.
    Challenges check <em>your</em> selected metric and rankings — not a Show-golden click.</p>
  `,
  challenges: [
    {
      id: "top-edge",
      title: "Top edge-weight pair",
      level: "Intro",
      prompt: "Select Edge scoring; top pair must be A–B with score 5.",
      hint: "Click Edge weight. Tie-break prefers A–B before D–E.",
      check: (_c, api) =>
        api.getMeta().metric === "edge" &&
        pairScore(api, "A", "B") === 5 &&
        rank(api)[0][0] === "A" &&
        rank(api)[0][1] === "B",
    },
    {
      id: "second-de",
      title: "Second is D–E @ 5",
      level: "Intro",
      prompt: "With Edge scoring, confirm the second-ranked pair is D–E at 5.",
      hint: "Same weight as A–B; alphabetical order places D–E second.",
      check: (_c, api) => {
        if (api.getMeta().metric !== "edge") return false;
        const r = rank(api);
        return r[1] && r[1][0] === "D" && r[1][1] === "E" && r[1][2] === 5;
      },
    },
    {
      id: "third-bc",
      title: "Third is B–C @ 4",
      level: "Intro",
      prompt: "With Edge scoring, B–C ranks third with score 4.",
      hint: "After the two weight-5 edges comes B–C.",
      check: (_c, api) => {
        if (api.getMeta().metric !== "edge") return false;
        const r = rank(api);
        return r[2] && r[2][0] === "B" && r[2][1] === "C" && r[2][2] === 4;
      },
    },
    {
      id: "edge-six-pairs",
      title: "Six edge pairs ranked",
      level: "Intro",
      prompt: "Edge scoring ranks exactly the six existing edges.",
      hint: "Select Edge weight; no invented pairs.",
      check: (_c, api) => api.getMeta().metric === "edge" && rank(api).length === 6,
    },
    {
      id: "shared-ab",
      title: "Shared A–B = 6",
      level: "Practice",
      prompt: "Select Shared scoring; A–B must score 6.",
      hint: "5 + min(w(A,C), w(B,C)) = 5 + 1.",
      check: (_c, api) => api.getMeta().metric === "shared" && pairScore(api, "A", "B") === 6,
    },
    {
      id: "shared-de",
      title: "Shared D–E = 6",
      level: "Practice",
      prompt: "With Shared scoring, D–E also scores 6.",
      hint: "Shared neighbor C contributes min(2,1)=1 on top of edge weight 5.",
      check: (_c, api) => api.getMeta().metric === "shared" && pairScore(api, "D", "E") === 6,
    },
    {
      id: "ac-rises",
      title: "A–C rises to 5",
      level: "Practice",
      prompt: "With Shared scoring, A–C scores 5 (only 1 under edge weight).",
      hint: "Direct 1 + shared via B: min(5,4)=4.",
      check: (_c, api) => api.getMeta().metric === "shared" && pairScore(api, "A", "C") === 5,
    },
    {
      id: "pin-ab",
      title: "Pin top pair A–B",
      level: "Practice",
      prompt: "With Shared scoring, pin pair A–B (select A, Shift+click B, then Pin pair).",
      hint: "Pinned pair shows in metrics; must be A|B under shared mode.",
      check: (_c, api) => {
        const p = api.getMeta().pinned;
        return api.getMeta().metric === "shared" && p === "A|B";
      },
    },
    {
      id: "cd-rises",
      title: "C–D rises to 3",
      level: "Stretch",
      prompt: "With Shared scoring, C–D scores 3.",
      hint: "Shared via E: min(1,5)=1 added to direct 2.",
      check: (_c, api) => api.getMeta().metric === "shared" && pairScore(api, "C", "D") === 3,
    },
    {
      id: "invented-bd",
      title: "Invented pair B–D",
      level: "Stretch",
      prompt: "Shared mode invents non-edge B–D with score 2. Confirm it.",
      hint: "B and D share C with min(4,2)=2.",
      check: (_c, api) => api.getMeta().metric === "shared" && pairScore(api, "B", "D") === 2,
    },
  ],
  extraActions(ctx, api) {
    return [
      el("button", {
        className: "btn " + (api.getMeta().metric === "edge" ? "btn-primary" : "btn-secondary"),
        type: "button",
        text: "Edge weight",
        onClick: () => {
          api.setMeta({ metric: "edge" });
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn " + (api.getMeta().metric === "shared" ? "btn-primary" : "btn-secondary"),
        type: "button",
        text: "Shared neighbors",
        onClick: () => {
          api.setMeta({ metric: "shared" });
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: "Pin selected pair",
        onClick: () => {
          const a = api.getSelected();
          const b = api.getSwapPartner();
          if (!a || !b) {
            ctx.setStatus("idle", "Select a node, Shift+click partner, then Pin");
            return;
          }
          const key = a < b ? `${a}|${b}` : `${b}|${a}`;
          api.setMeta({ pinned: key });
          ctx.rerender();
        },
      }),
    ];
  },
  highlightPairs(api) {
    const pinned = api.getMeta().pinned;
    if (pinned) return [pinned];
    const top = rank(api)[0];
    return top ? [`${top[0]}|${top[1]}`] : [];
  },
  extraMetrics(api) {
    const ranked = rank(api);
    const mode = api.getMeta().metric || "edge";
    const lines = [
      `metric: ${mode === "edge" ? "edge-weight" : "shared-neighbor"} (${ranked.length} pairs)`,
      `pinned: ${api.getMeta().pinned || "—"}`,
      "ranking:",
    ];
    for (const [u, v, s] of ranked.slice(0, 8)) lines.push(`  ${u}–${v}: ${s}`);
    return lines;
  },
  onLoadStarter(api) {
    api.setMeta({ metric: "edge", pinned: null });
  },
});
