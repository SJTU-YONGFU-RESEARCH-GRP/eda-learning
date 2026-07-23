import { CONGESTED_SEED, PLACEMENT, hottest } from "../../assets/congestion-core.js";
import { createInteractiveCongestionLab } from "../../assets/interactive-congestion-lab.js";

const root = document.getElementById("lab-root");
createInteractiveCongestionLab(root, {
  initialPositions: CONGESTED_SEED,
  revealPositions: PLACEMENT,
  starterHtml: `<p><strong>Your job:</strong> congestion = demand/capacity. Move cells until the hottest
    GCell is not a center tile — or cool the map below thresholds.</p>`,
  extraMetrics(api) {
    const h = hottest(api.getCongestion());
    return [`hottest: (${h.i},${h.j}) @ ${h.v.toFixed(2)}`];
  },
  challenges: [
    { id: "hot-exists", title: "Hottest defined", level: "Intro",
      prompt: "Hottest congestion ≥ 0.",
      check: (_c, api) => hottest(api.getCongestion()).v >= 0 },
    { id: "seed-hot", title: "Seed cong > 1", level: "Intro",
      prompt: "Some tile congestion > 1 on seed.",
      check: (_c, api) => api.getCongestion().some(col => col.some(v => v>1)) },
    { id: "cool-max", title: "Max cong ≤ 3", level: "Practice",
      prompt: "Hottest ratio ≤ 3.",
      check: (_c, api) => hottest(api.getCongestion()).v <= 3 },
    { id: "cool-2", title: "Max cong ≤ 2.5", level: "Practice",
      prompt: "Hottest ≤ 2.5.",
      check: (_c, api) => hottest(api.getCongestion()).v <= 2.5 },
    { id: "edge-hot", title: "Hottest on edge col", level: "Challenge",
      prompt: "Make hottest GCell have i=0 or i=3.",
      check: (_c, api) => { const h=hottest(api.getCongestion()); return h.i===0||h.i===3; } },
    { id: "ov-count", title: "Cong>1 count ≤ 3", level: "Practice",
      prompt: "At most 3 tiles with cong>1.",
      check: (_c, api) => api.getCongestion().flat().filter(v=>v>1).length <= 3 },
    { id: "total-ov", title: "Overflow total ≤ 6", level: "Challenge",
      prompt: "Overflow total ≤ 6.",
      check: (_c, api) => api.getOverflow().total <= 6 },
    { id: "hpwl", title: "HPWL < 50", level: "Intro",
      prompt: "HPWL under 50.",
      check: (_c, api) => api.getHpwl() < 50 },
  ],
});
