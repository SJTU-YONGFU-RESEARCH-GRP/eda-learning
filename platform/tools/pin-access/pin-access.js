import {
  GOLDENS, PLACEMENT, CLUSTER_SEED, pinGrid
} from "../../assets/detailed-routing-core.js";
import { createInteractiveDetailedRoutingLab } from "../../assets/interactive-detailed-routing-lab.js";

const root = document.getElementById("lab-root");
createInteractiveDetailedRoutingLab(root, {
  initialPositions: PLACEMENT,
  starterHtml: `<p><strong>Your job:</strong> on spread starter, A→(1,1) and D→(8,5).
    E/F sit on blockage and nudge to access points.</p>`,
  challenges: [
    { id: "a11", title: "A at (1,1)", level: "Intro",
      prompt: "Spread A pin grid is (1,1).",
      check: (_c, api) => { const g = api.getTerminals().A; return g.x === 1 && g.y === 1; } },
    { id: "d85", title: "D at (8,5)", level: "Intro",
      prompt: "Spread D pin grid is (8,5).",
      check: (_c, api) => { const g = api.getTerminals().D; return g.x === 8 && g.y === 5; } },
    { id: "e-access", title: "E access nudged", level: "Practice",
      prompt: "E terminal is not inside blockage.",
      check: (_c, api) => {
        const g = api.getTerminals().E;
        return !(g.x >= 5 && g.x <= 6 && g.y >= 2 && g.y <= 3); } },
    { id: "move-b", title: "B column ≥6", level: "Practice",
      prompt: "Place B with pin column x ≥ 6.",
      check: (_c, api) => api.getTerminals().B.x >= 6 },
    { id: "c-row", title: "C row j≥3", level: "Practice",
      prompt: "Place C with pin row y ≥ 3.",
      check: (_c, api) => api.getTerminals().C.y >= 3 },
    { id: "all-valid", title: "All on-grid", level: "Challenge",
      prompt: "Every terminal has valid grid coordinates.",
      check: (_c, api) => Object.values(api.getTerminals()).every(g => g.x >= 0 && g.x < 12 && g.y >= 0 && g.y < 8) },
    { id: "golden-a", title: "Golden A pin", level: "Intro",
      prompt: "GOLDENS documents A at (1,1).",
      check: () => GOLDENS.aPin[0] === 1 && GOLDENS.aPin[1] === 1 },
    { id: "pin-round", title: "Pin rounds", level: "Intro",
      prompt: "pinGrid(1.4,1.6) rounds to (1,2).",
      check: () => { const g = pinGrid(1.4, 1.6); return g.x === 1 && g.y === 2; } },
  ],
});
