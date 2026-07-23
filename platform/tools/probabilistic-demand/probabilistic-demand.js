import {
  CONGESTED_SEED, PLACEMENT, probabilisticDemand, rudyDemand, overflowMetrics, CAPACITY
} from "../../assets/congestion-core.js";
import { createInteractiveCongestionLab } from "../../assets/interactive-congestion-lab.js";

const root = document.getElementById("lab-root");
createInteractiveCongestionLab(root, {
  initialPositions: CONGESTED_SEED,
  revealPositions: PLACEMENT,
  demandFn: probabilisticDemand,
  starterHtml: `<p><strong>Your job:</strong> this lab scores <em>probabilistic</em> L-shape demand.
    Compare mentally to RUDY (metrics show both).</p>`,
  extraMetrics(api) {
    const r = overflowMetrics(rudyDemand(api.getPositions()), CAPACITY);
    return [`RUDY overflow total: ${r.total.toFixed(2)} (compare)`];
  },
  challenges: [
    { id: "prob-pos", title: "Prob demand > 0", level: "Intro",
      prompt: "Probabilistic demand is positive somewhere.",
      check: (_c, api) => api.getDemand().some(col => col.some(v => v>0)) },
    { id: "seed-hot", title: "Seed overflow > 0", level: "Intro",
      prompt: "Congested seed has probabilistic overflow.",
      check: (_c, api) => api.getOverflow().total > 0 },
    { id: "cut-total", title: "Prob total ≤ 8", level: "Practice",
      prompt: "Probabilistic total overflow ≤ 8.",
      check: (_c, api) => api.getOverflow().total <= 8 },
    { id: "cut-max", title: "Prob max ≤ 6", level: "Practice",
      prompt: "Max overflow ≤ 6.",
      check: (_c, api) => api.getOverflow().max <= 6 },
    { id: "count-le-4", title: "Count ≤ 4", level: "Practice",
      prompt: "Overflow count ≤ 4.",
      check: (_c, api) => api.getOverflow().count <= 4 },
    { id: "disagree", title: "RUDY vs prob differ", level: "Challenge",
      prompt: "On your placement, RUDY total ≠ probabilistic total.",
      check: (_c, api) => {
        const r=overflowMetrics(rudyDemand(api.getPositions()),CAPACITY).total;
        return Math.abs(r - api.getOverflow().total) > 0.01; } },
    { id: "spread-3", title: "≥3 GCells used", level: "Challenge",
      prompt: "Cells in ≥3 GCells.",
      check: (_c, api) => {
        const s=new Set(Object.values(api.getPositions()).map(p=>{const g=api.cellGcell(p.x,p.y);return g.i+','+g.j;}));
        return s.size>=3; } },
    { id: "total-lt-5", title: "Total < 5", level: "Challenge",
      prompt: "Probabilistic total overflow < 5.",
      check: (_c, api) => api.getOverflow().total < 5 },
  ],
});
