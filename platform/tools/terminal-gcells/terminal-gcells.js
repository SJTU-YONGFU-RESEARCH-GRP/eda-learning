import {
  GOLDENS, PLACEMENT, CLUSTER_SEED, cellGcell
} from "../../assets/global-routing-core.js";
import { createInteractiveGlobalRoutingLab } from "../../assets/interactive-global-routing-lab.js";

const root = document.getElementById("lab-root");
createInteractiveGlobalRoutingLab(root, {
  initialPositions: PLACEMENT,
  revealPositions: CLUSTER_SEED,
  starterHtml: `<p><strong>Your job:</strong> on spread starter, A→(0,0) and D→(2,1).
    Move cells; terminals follow pins into GCells.</p>`,
  challenges: [
    { id: "a00", title: "A in (0,0)", level: "Intro",
      prompt: "On spread starter, A is in GCell (0,0).",
      check: (_c, api) => { const g=api.getTerminals().A; return g.i===0&&g.j===0; } },
    { id: "d21", title: "D in (2,1)", level: "Intro",
      prompt: "On spread starter, D is in GCell (2,1).",
      check: (_c, api) => { const g=api.getTerminals().D; return g.i===2&&g.j===1; } },
    { id: "move-e", title: "E to col 3", level: "Practice",
      prompt: "Place E so its GCell column i=3.",
      check: (_c, api) => api.getTerminals().E.i === 3 },
    { id: "b-bottom", title: "B row j=0", level: "Practice",
      prompt: "Keep B in bottom row j=0.",
      check: (_c, api) => api.getTerminals().B.j === 0 },
    { id: "c-top", title: "C row j=1", level: "Practice",
      prompt: "On spread starter C is in j=1.",
      check: (_c, api) => api.getTerminals().C.j === 1 },
    { id: "f-col2", title: "F in col 2", level: "Practice",
      prompt: "Place F with i=2.",
      check: (_c, api) => api.getTerminals().F.i === 2 },
    { id: "all-valid", title: "All on-chip GCells", level: "Challenge",
      prompt: "Every terminal has valid (i,j).",
      check: (_c, api) => Object.values(api.getTerminals()).every(g => g.i>=0&&g.i<4&&g.j>=0&&g.j<2) },
    { id: "golden-a", title: "Golden A col 1", level: "Intro",
      prompt: "GOLDENS documents A at (0,0) on spread.",
      check: () => GOLDENS.aGcell[0]===0 && GOLDENS.aGcell[1]===0 },
  ],
});
