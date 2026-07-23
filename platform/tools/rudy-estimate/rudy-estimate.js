import { CONGESTED_SEED, GOLDENS, PLACEMENT } from "../../assets/congestion-core.js";
import { createInteractiveCongestionLab } from "../../assets/interactive-congestion-lab.js";

const root = document.getElementById("lab-root");
createInteractiveCongestionLab(root, {
  initialPositions: CONGESTED_SEED,
  revealPositions: PLACEMENT,
  heatMode: "demand",
  starterHtml: `<p><strong>Your job:</strong> RUDY deposits HPWL density into GCells under each net bbox.
    Spread cells to cut overflow. Seed max overflow ≈ ${GOLDENS.congestedRudyMaxOv}.</p>`,
  challenges: [
    { id: "seed-max", title: "Seed max ≥ 4", level: "Intro",
      prompt: "Congested seed RUDY max overflow ≥ 4 at Cap=2.",
      check: (_c, api) => api.getOverflow().max >= 4 },
    { id: "demand-positive", title: "Demand > 0", level: "Intro",
      prompt: "Some GCell has positive demand.",
      check: (_c, api) => api.getDemand().some(col => col.some(v => v>0)) },
    { id: "cut-max", title: "Max overflow ≤ 4", level: "Practice",
      prompt: "Reduce max overflow to ≤ 4.",
      check: (_c, api) => api.getOverflow().max <= 4 },
    { id: "cut-total", title: "Total ≤ 10", level: "Practice",
      prompt: "Total overflow ≤ 10.",
      check: (_c, api) => api.getOverflow().total <= 10 },
    { id: "count-le-3", title: "Count ≤ 3", level: "Practice",
      prompt: "At most 3 overflowing GCells.",
      check: (_c, api) => api.getOverflow().count <= 3 },
    { id: "spread-shape", title: "Not all in one tile", level: "Challenge",
      prompt: "Cells occupy at least 3 distinct GCells.",
      check: (_c, api) => {
        const s=new Set(Object.values(api.getPositions()).map(p=>`${api.cellGcell(p.x,p.y).i},${api.cellGcell(p.x,p.y).j}`));
        return s.size>=3; } },
    { id: "total-lt-seed", title: "Total < 12", level: "Challenge",
      prompt: "Total overflow under 12.",
      check: (_c, api) => api.getOverflow().total < 12 },
    { id: "hpwl-lt-40", title: "HPWL < 40", level: "Challenge",
      prompt: "Keep HPWL under 40 while improving overflow.",
      check: (_c, api) => api.getHpwl() < 40 },
  ],
});
