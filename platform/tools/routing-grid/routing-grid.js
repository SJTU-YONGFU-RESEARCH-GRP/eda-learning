import {
  GOLDENS, PLACEMENT, GRID_NX, GRID_NY, isBlocked, neighbors4
} from "../../assets/detailed-routing-core.js";
import { createInteractiveDetailedRoutingLab } from "../../assets/interactive-detailed-routing-lab.js";

const root = document.getElementById("lab-root");
createInteractiveDetailedRoutingLab(root, {
  initialPositions: PLACEMENT,
  starterHtml: `<p><strong>Your job:</strong> explore the detailed routing grid (${GRID_NX}×${GRID_NY}).
    M1 routes horizontally; M2 vertically. Blockage covers cells (5–6, 2–3).</p>`,
  extraMetrics(api) {
    const t = api.getTerminals();
    const g = t.A;
    return [`A pin grid: (${g.x},${g.y})`, `neighbors(A): ${neighbors4(g).length}`];
  },
  challenges: [
    { id: "grid-shape", title: "Grid is 12×8", level: "Intro",
      prompt: "Confirm GOLDENS grid dimensions.",
      check: () => GOLDENS.gridNx === 12 && GOLDENS.gridNy === 8 },
    { id: "cap-two", title: "Capacity is 2", level: "Intro",
      prompt: "Each track capacity equals 2.",
      check: (_c, api) => api.getCapacity() === GOLDENS.trackCapacity },
    { id: "blockage", title: "Blockage at (5,2)", level: "Intro",
      prompt: "Cell (5,2) is blocked.",
      check: () => isBlocked(5, 2) },
    { id: "block-interior", title: "Interior blocked", level: "Practice",
      prompt: "Cell (6,3) inside 2×2 blockage is blocked.",
      check: () => isBlocked(6, 3) },
    { id: "free-corner", title: "Corner free", level: "Practice",
      prompt: "Corner (0,0) is not blocked.",
      check: () => !isBlocked(0, 0) },
    { id: "mid-neigh", title: "Mid cell neighbors", level: "Practice",
      prompt: "Grid point (1,1) has at least three neighbors.",
      check: () => neighbors4({ x: 1, y: 1 }).length >= 3 },
    { id: "h-tracks", title: "Horizontal track count", level: "Intro",
      prompt: "GOLDENS documents horizontal track slots.",
      check: () => GOLDENS.hTracks === 88 },
    { id: "v-tracks", title: "Vertical track count", level: "Intro",
      prompt: "GOLDENS documents vertical track slots.",
      check: () => GOLDENS.vTracks === 84 },
  ],
});
