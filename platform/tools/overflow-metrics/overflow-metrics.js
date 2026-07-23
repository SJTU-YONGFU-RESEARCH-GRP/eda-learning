import { CONGESTED_SEED, PLACEMENT } from "../../assets/congestion-core.js";
import { createInteractiveCongestionLab } from "../../assets/interactive-congestion-lab.js";

const root = document.getElementById("lab-root");
createInteractiveCongestionLab(root, {
  initialPositions: CONGESTED_SEED,
  revealPositions: PLACEMENT,
  starterHtml: `<p><strong>Your job:</strong> hit overflow targets by moving cells.
    Metrics: total · max · count.</p>`,
  challenges: [
    { id: "seed-pos", title: "Seed total > 0", level: "Intro",
      prompt: "Starter has positive total overflow.",
      check: (_c, api) => api.getOverflow().total > 0 },
    { id: "triple", title: "Metrics finite", level: "Intro",
      prompt: "total/max/count are finite.",
      check: (_c, api) => {
        const o=api.getOverflow();
        return Number.isFinite(o.total)&&Number.isFinite(o.max)&&Number.isFinite(o.count); } },
    { id: "t10", title: "Total ≤ 10", level: "Practice",
      prompt: "Total overflow ≤ 10.",
      check: (_c, api) => api.getOverflow().total <= 10 },
    { id: "t5", title: "Total ≤ 5", level: "Practice",
      prompt: "Total overflow ≤ 5.",
      check: (_c, api) => api.getOverflow().total <= 5 },
    { id: "m4", title: "Max ≤ 4", level: "Practice",
      prompt: "Max overflow ≤ 4.",
      check: (_c, api) => api.getOverflow().max <= 4 },
    { id: "c2", title: "Count ≤ 2", level: "Challenge",
      prompt: "Overflow count ≤ 2.",
      check: (_c, api) => api.getOverflow().count <= 2 },
    { id: "t2", title: "Total ≤ 2", level: "Challenge",
      prompt: "Total overflow ≤ 2.",
      check: (_c, api) => api.getOverflow().total <= 2 },
    { id: "zeroish", title: "Total < 1", level: "Challenge",
      prompt: "Nearly clear: total overflow < 1.",
      check: (_c, api) => api.getOverflow().total < 1 },
  ],
});
