import { GOLDENS, PLACEMENT } from "../../assets/detailed-routing-core.js";
import { createInteractiveDetailedRoutingLab } from "../../assets/interactive-detailed-routing-lab.js";

const root = document.getElementById("lab-root");
createInteractiveDetailedRoutingLab(root, {
  initialPositions: PLACEMENT,
  starterHtml: `<p><strong>Your job:</strong> route layered on spread (total ≈ ${GOLDENS.spreadLhvTotalOv}),
    then reduce overflow by moving cells or switching to A*.</p>`,
  challenges: [
    { id: "seed-ov", title: "Spread layered overflow", level: "Intro",
      prompt: "Route layered; total matches golden.",
      setup: (_c, api) => api.routeLayered(),
      check: (_c, api) => Math.abs(api.getOverflow().total - GOLDENS.spreadLhvTotalOv) < 0.01 },
    { id: "triple", title: "Metrics finite", level: "Intro",
      prompt: "total/max/count finite after route.",
      setup: (_c, api) => api.routeLayered(),
      check: (_c, api) => {
        const o = api.getOverflow();
        return Number.isFinite(o.total) && Number.isFinite(o.max) && Number.isFinite(o.count); } },
    { id: "usage-pos", title: "Usage > 0", level: "Practice",
      prompt: "Some track has usage > 0 after route.",
      setup: (_c, api) => api.routeLayered(),
      check: (_c, api) => Object.values(api.getUsage()).some(v => v > 0) },
    { id: "t2", title: "Total ≤ 2", level: "Practice",
      prompt: "Total overflow ≤ 2.",
      check: (_c, api) => api.getRoutes().some(r => r.segments?.length) && api.getOverflow().total <= 2 },
    { id: "m1", title: "Max ≤ 1", level: "Practice",
      prompt: "Max overflow ≤ 1.",
      check: (_c, api) => api.getRoutes().some(r => r.segments?.length) && api.getOverflow().max <= 1 },
    { id: "c1", title: "Count ≤ 1", level: "Practice",
      prompt: "At most one overflowing track.",
      check: (_c, api) => api.getRoutes().some(r => r.segments?.length) && api.getOverflow().count <= 1 },
    { id: "zero", title: "Total = 0", level: "Challenge",
      prompt: "Clear all track overflow.",
      check: (_c, api) => api.getRoutes().some(r => r.segments?.length) && api.getOverflow().total === 0 },
    { id: "cap", title: "Cap = 2", level: "Intro",
      prompt: "Track capacity is 2.",
      check: (_c, api) => api.getCapacity() === 2 },
  ],
});
