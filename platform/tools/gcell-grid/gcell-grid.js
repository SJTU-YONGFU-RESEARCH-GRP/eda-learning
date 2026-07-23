import {
  CONGESTED_SEED, GOLDENS, PLACEMENT, cellGcell
} from "../../assets/congestion-core.js";
import { createInteractiveCongestionLab } from "../../assets/interactive-congestion-lab.js";

const root = document.getElementById("lab-root");
createInteractiveCongestionLab(root, {
  initialPositions: PLACEMENT,
  revealPositions: CONGESTED_SEED,
  heatMode: "cong",
  starterHtml: `<p><strong>Your job:</strong> click to place cells. Challenges check GCell indices
    of <em>your</em> positions (A→(0,0) on spread starter).</p>`,
  challenges: [
    { id: "a00", title: "A in (0,0)", level: "Intro",
      prompt: "On spread starter, A is in GCell (0,0).",
      hint: "Reset starter; check selected A metrics.",
      check: (_c, api) => { const p=api.getPositions().A; const g=cellGcell(p.x,p.y); return g.i===0&&g.j===0; } },
    { id: "d21", title: "D in (2,1)", level: "Intro",
      prompt: "On spread starter, D is in GCell (2,1).",
      check: (_c, api) => { const p=api.getPositions().D; const g=cellGcell(p.x,p.y); return g.i===2&&g.j===1; } },
    { id: "move-e", title: "Move E to (3,0)", level: "Practice",
      prompt: "Place E so its center GCell is (3,0) (right column, bottom row).",
      hint: "x in [9,12), y in [0,4).",
      check: (_c, api) => { const p=api.getPositions().E; const g=cellGcell(p.x,p.y); return g.i===3&&g.j===0; } },
    { id: "grid-shape", title: "Grid is 4×2", level: "Intro",
      prompt: "Confirm GOLDENS grid shape.",
      check: () => GOLDENS.gcellNx===4 && GOLDENS.gcellNy===2 },
    { id: "b-top", title: "B bottom row", level: "Practice",
      prompt: "Keep B in row j=0 (bottom).",
      check: (_c, api) => cellGcell(api.getPositions().B.x, api.getPositions().B.y).j===0 },
    { id: "c-top", title: "C top row", level: "Practice",
      prompt: "On spread starter C is in j=1.",
      check: (_c, api) => cellGcell(api.getPositions().C.x, api.getPositions().C.y).j===1 },
    { id: "f-mid", title: "F in col 2", level: "Practice",
      prompt: "Place F with i=2.",
      check: (_c, api) => cellGcell(api.getPositions().F.x, api.getPositions().F.y).i===2 },
    { id: "all-valid", title: "All cells on-chip GCells", level: "Challenge",
      prompt: "Every cell reports a valid (i,j).",
      check: (_c, api) => Object.values(api.getPositions()).every(p => {
        const g=cellGcell(p.x,p.y); return g.i>=0&&g.i<4&&g.j>=0&&g.j<2; }) },
  ],
});
