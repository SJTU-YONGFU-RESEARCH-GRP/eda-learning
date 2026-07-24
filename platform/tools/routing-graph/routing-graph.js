import {
  GOLDENS, PLACEMENT, allEdges, neighbors, gcellKey
} from "../../assets/global-routing-core.js";
import { createInteractiveGlobalRoutingLab } from "../../assets/interactive-global-routing-lab.js";

const root = document.getElementById("lab-root");
createInteractiveGlobalRoutingLab(root, {
  initialPositions: PLACEMENT,
  starterHtml: `<p><strong>Your job:</strong> explore the routing graph. Edge count is ${GOLDENS.edgeCount}.
    Interior GCells have up to four neighbors; corners have two.</p>`,
  extraMetrics(api) {
    const t = api.getTerminals();
    const g = t.A;
    return [`A GCell: (${g.i},${g.j})`, `neighbors(A): ${neighbors(g).length}`];
  },
  challenges: [
    { id: "edge-count", title: "Ten edges", level: "Intro",
      prompt: "This 4×2 grid has exactly ten routing edges.",
      check: () => allEdges().length === GOLDENS.edgeCount },
    { id: "cap-two", title: "Capacity is 2", level: "Intro",
      prompt: "Each edge capacity equals 2.",
      check: (_c, api) => api.getCapacity() === GOLDENS.edgeCapacity },
    { id: "mid-neigh", title: "Mid cell ≥3 neighbors", level: "Intro",
      prompt: "GCell (1,0) has at least three neighbors.",
      check: () => neighbors({ i: 1, j: 0 }).length >= GOLDENS.neighborCountMid },
    { id: "corner-neigh", title: "Corner has 2 neighbors", level: "Practice",
      prompt: "Corner (0,0) has exactly two neighbors.",
      check: () => neighbors({ i: 0, j: 0 }).length === 2 },
    { id: "grid-shape", title: "Grid is 4×2", level: "Intro",
      prompt: "Confirm GOLDENS grid shape.",
      check: () => GOLDENS.gcellNx === 4 && GOLDENS.gcellNy === 2 },
    { id: "unique-keys", title: "Unique edge keys", level: "Practice",
      prompt: "All edge keys are unique strings.",
      check: () => new Set(allEdges()).size === allEdges().length },
    { id: "h-edges", title: "Six horizontal edges", level: "Practice",
      prompt: "Count horizontal edges (same j, adjacent i).",
      check: () => allEdges().filter(e => e.split("|")[0].split(",")[1] === e.split("|")[1].split(",")[1]).length === 6 },
    { id: "v-edges", title: "Four vertical edges", level: "Practice",
      prompt: "Count vertical edges (same i, adjacent j).",
      check: () => allEdges().filter(e => e.split("|")[0].split(",")[0] === e.split("|")[1].split(",")[0]).length === 4 },
  ],
});
