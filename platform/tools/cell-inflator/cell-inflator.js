import {
  CONGESTED_SEED, PLACEMENT, WIDTHS, inflateWidths, congestionMap, rudyDemand, CAPACITY
} from "../../assets/congestion-core.js";
import { createInteractiveCongestionLab } from "../../assets/interactive-congestion-lab.js";
import { el } from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let lastWidths = { ...WIDTHS };

createInteractiveCongestionLab(root, {
  initialPositions: CONGESTED_SEED,
  revealPositions: PLACEMENT,
  starterHtml: `<p><strong>Your job:</strong> click <em>Run inflate</em> then verify some widths grew
    where congestion&gt;1. Moving cells changes which tiles are hot.</p>`,
  extraActions(_ctx, api) {
    return [el("button", { className:"btn btn-secondary", type:"button", text:"Run inflate",
      onClick: () => {
        const cong = congestionMap(rudyDemand(api.getPositions()), CAPACITY);
        lastWidths = inflateWidths(api.getPositions(), WIDTHS, cong, 0.5);
        _ctx.rerender();
      }})];
  },
  extraMetrics() {
    const grown = Object.keys(lastWidths).filter(k => lastWidths[k] > WIDTHS[k] + 1e-6);
    return [`inflated: ${grown.join(",")||"(none)"}`, `A width: ${lastWidths.A.toFixed(2)}`];
  },
  challenges: [
    { id: "run-inflate", title: "Inflate someone", level: "Intro",
      prompt: "After Run inflate on a hot seed, at least one width > base.",
      check: () => Object.keys(WIDTHS).some(k => lastWidths[k] > WIDTHS[k] + 1e-6) },
    { id: "a-or-b", title: "A or B grew", level: "Practice",
      prompt: "A or B width above base after inflate on clustered layout.",
      check: (_c, api) => {
        const cong=congestionMap(rudyDemand(api.getPositions()),CAPACITY);
        const w=inflateWidths(api.getPositions(), WIDTHS, cong, 0.5);
        return w.A>WIDTHS.A+1e-6 || w.B>WIDTHS.B+1e-6; } },
    { id: "cool-no", title: "Quiet cell unchanged", level: "Practice",
      prompt: "If you spread enough that E's tile cong≤1, E width stays base when computed.",
      check: (_c, api) => {
        const cong=congestionMap(rudyDemand(api.getPositions()),CAPACITY);
        const g=api.cellGcell(api.getPositions().E.x, api.getPositions().E.y);
        if (cong[g.i][g.j] > 1) return false;
        const w=inflateWidths(api.getPositions(), WIDTHS, cong, 0.5);
        return Math.abs(w.E - WIDTHS.E) < 1e-6; } },
    { id: "alpha", title: "Scale formula", level: "Intro",
      prompt: "Inflation uses (1+α(c−1)) with α=0.5 when c>1.",
      check: () => true },
    { id: "ov-still", title: "Still track overflow", level: "Practice",
      prompt: "Overflow total is finite after moves.",
      check: (_c, api) => Number.isFinite(api.getOverflow().total) },
    { id: "spread-then", title: "Total ≤ 8", level: "Challenge",
      prompt: "Total overflow ≤ 8 (placement still matters).",
      check: (_c, api) => api.getOverflow().total <= 8 },
    { id: "multi", title: "≥2 inflated when hot", level: "Challenge",
      prompt: "On a hot layout, ≥2 cells inflate.",
      check: (_c, api) => {
        const cong=congestionMap(rudyDemand(api.getPositions()),CAPACITY);
        const w=inflateWidths(api.getPositions(), WIDTHS, cong, 0.5);
        return Object.keys(WIDTHS).filter(k => w[k] > WIDTHS[k]+1e-6).length >= 2; } },
    { id: "base-reset", title: "Base widths known", level: "Intro",
      prompt: "Base A width is 2.",
      check: () => WIDTHS.A === 2 },
  ],
});
