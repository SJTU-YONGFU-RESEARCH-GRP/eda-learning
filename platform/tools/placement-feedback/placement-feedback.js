import { CONGESTED_SEED, PLACEMENT, placementFeedbackLite, rudyDemand, overflowMetrics, CAPACITY } from "../../assets/congestion-core.js";
import { createInteractiveCongestionLab } from "../../assets/interactive-congestion-lab.js";

const root = document.getElementById("lab-root");
const before = overflowMetrics(rudyDemand(CONGESTED_SEED), CAPACITY).total;

createInteractiveCongestionLab(root, {
  initialPositions: CONGESTED_SEED,
  revealPositions: PLACEMENT,
  starterHtml: `<p><strong>Your job:</strong> click <em>Run feedback</em> (or nudge) until overflow drops
    below the seed total (${before.toFixed(2)}).</p>`,
  challenges: [
    { id: "seed-base", title: "Seed total known", level: "Intro",
      prompt: "Reset starter: total overflow matches seed.",
      check: (_c, api) => Math.abs(api.getOverflow().total - before) < 0.2 },
    { id: "after-lower", title: "Below seed total", level: "Practice",
      prompt: "Total overflow strictly below seed.",
      check: (_c, api) => api.getOverflow().total < before - 0.01 },
    { id: "half", title: "≤ half seed", level: "Practice",
      prompt: "Total overflow ≤ half of seed.",
      check: (_c, api) => api.getOverflow().total <= before * 0.5 },
    { id: "low", title: "Total ≤ 2", level: "Challenge",
      prompt: "Total overflow ≤ 2.",
      check: (_c, api) => api.getOverflow().total <= 2 },
    { id: "count", title: "Count ≤ 2", level: "Practice",
      prompt: "Overflow count ≤ 2.",
      check: (_c, api) => api.getOverflow().count <= 2 },
    { id: "max", title: "Max ≤ 2", level: "Challenge",
      prompt: "Max overflow ≤ 2.",
      check: (_c, api) => api.getOverflow().max <= 2 },
    { id: "spread-cells", title: "≥3 GCells", level: "Challenge",
      prompt: "Cells span ≥3 GCells after feedback.",
      check: (_c, api) => {
        const s=new Set(Object.values(api.getPositions()).map(p=>{const g=api.cellGcell(p.x,p.y);return g.i+','+g.j;}));
        return s.size>=3; } },
    { id: "helper", title: "Feedback helper ok", level: "Intro",
      prompt: "placementFeedbackLite reduces seed overflow.",
      check: () => overflowMetrics(rudyDemand(placementFeedbackLite(CONGESTED_SEED)),CAPACITY).total < before },
  ],
});
