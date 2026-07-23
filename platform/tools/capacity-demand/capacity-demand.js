import { CONGESTED_SEED, PLACEMENT } from "../../assets/congestion-core.js";
import { createInteractiveCongestionLab } from "../../assets/interactive-congestion-lab.js";

const root = document.getElementById("lab-root");
createInteractiveCongestionLab(root, {
  initialPositions: CONGESTED_SEED,
  revealPositions: PLACEMENT,
  starterHtml: `<p><strong>Your job:</strong> Cap=2. Oversubscribed tiles have demand&gt;2.
    Spread out until overflow count drops.</p>`,
  challenges: [
    { id: "seed-count", title: "Seed has overflow", level: "Intro",
      prompt: "Congested seed has count≥1 at Cap=2.",
      check: (_c, api) => api.getOverflow().count >= 1 },
    { id: "cap-value", title: "Capacity is 2", level: "Intro",
      prompt: "Lab capacity equals 2.",
      check: (_c, api) => api.getCapacity() === 2 },
    { id: "reduce-count", title: "Overflow count ≤ 2", level: "Practice",
      prompt: "Move cells so overflow count ≤ 2.",
      check: (_c, api) => api.getOverflow().count <= 2 },
    { id: "reduce-total", title: "Total overflow ≤ 8", level: "Practice",
      prompt: "Bring total overflow ≤ 8.",
      check: (_c, api) => api.getOverflow().total <= 8 },
    { id: "some-ok", title: "At least one quiet tile", level: "Practice",
      prompt: "At least one GCell has demand ≤ Cap.",
      check: (_c, api) => {
        const d=api.getDemand(); let ok=false;
        for (const col of d) for (const v of col) if (v<=api.getCapacity()) ok=true;
        return ok; } },
    { id: "spread-better", title: "Total < 20", level: "Challenge",
      prompt: "Total overflow under 20.",
      check: (_c, api) => api.getOverflow().total < 20 },
    { id: "max-bound", title: "Max overflow ≤ 6", level: "Challenge",
      prompt: "Keep max overflow ≤ 6.",
      check: (_c, api) => api.getOverflow().max <= 6 },
    { id: "hpwl-finite", title: "HPWL finite", level: "Intro",
      prompt: "HPWL is a finite number.",
      check: (_c, api) => Number.isFinite(api.getHpwl()) },
  ],
});
