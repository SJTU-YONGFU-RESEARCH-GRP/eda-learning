import {
  CONGESTED_SEED, PLACEMENT, netWeightsFromCongestion, congestionMap, rudyDemand, CAPACITY
} from "../../assets/congestion-core.js";
import { createInteractiveCongestionLab } from "../../assets/interactive-congestion-lab.js";

const root = document.getElementById("lab-root");
createInteractiveCongestionLab(root, {
  initialPositions: CONGESTED_SEED,
  revealPositions: PLACEMENT,
  starterHtml: `<p><strong>Your job:</strong> weights = 1 + mean congestion under each net bbox.
    Keep the 4-pin net heavier than E–F on a hot seed.</p>`,
  extraMetrics(api) {
    const w = netWeightsFromCongestion(api.getPositions(), api.getCongestion(), 1);
    return [`weights: ${w.map(x=>x.toFixed(2)).join(", ")}`];
  },
  challenges: [
    { id: "w-len", title: "Six weights", level: "Intro",
      prompt: "There are 6 net weights.",
      check: (_c, api) => netWeightsFromCongestion(api.getPositions(), api.getCongestion(),1).length===6 },
    { id: "w-ge1", title: "All weights ≥ 1", level: "Intro",
      prompt: "Every weight ≥ 1.",
      check: (_c, api) => netWeightsFromCongestion(api.getPositions(), api.getCongestion(),1).every(w=>w>=1) },
    { id: "hot-heavier", title: "Net4 ≥ Net5 on seed", level: "Practice",
      prompt: "On a hot layout, 4-pin net weight ≥ E–F weight.",
      check: (_c, api) => {
        const w=netWeightsFromCongestion(api.getPositions(), api.getCongestion(),1);
        return w[4] >= w[5] - 1e-6; } },
    { id: "seed-boost", title: "Some weight > 1.2", level: "Practice",
      prompt: "At least one weight > 1.2.",
      check: (_c, api) => netWeightsFromCongestion(api.getPositions(), api.getCongestion(),1).some(w=>w>1.2) },
    { id: "cool-lower", title: "Max weight ≤ 4", level: "Practice",
      prompt: "Max weight ≤ 4 after spreading.",
      check: (_c, api) => Math.max(...netWeightsFromCongestion(api.getPositions(), api.getCongestion(),1)) <= 4 },
    { id: "ov", title: "Overflow tracked", level: "Intro",
      prompt: "Overflow total finite.",
      check: (_c, api) => Number.isFinite(api.getOverflow().total) },
    { id: "spread-ov", title: "Total ≤ 10", level: "Challenge",
      prompt: "Total overflow ≤ 10.",
      check: (_c, api) => api.getOverflow().total <= 10 },
    { id: "ef-lighter", title: "E–F not heaviest", level: "Challenge",
      prompt: "E–F (net5) is not strictly heaviest.",
      check: (_c, api) => {
        const w=netWeightsFromCongestion(api.getPositions(), api.getCongestion(),1);
        return w[5] <= Math.max(...w.slice(0,5)) + 1e-6; } },
  ],
});
