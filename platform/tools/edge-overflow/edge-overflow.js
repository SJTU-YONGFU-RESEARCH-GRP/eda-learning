import { GOLDENS, PLACEMENT } from "../../assets/global-routing-core.js";
import { createInteractiveGlobalRoutingLab } from "../../assets/interactive-global-routing-lab.js";

const root = document.getElementById("lab-root");
createInteractiveGlobalRoutingLab(root, {
  initialPositions: PLACEMENT,
  starterHtml: `<p><strong>Your job:</strong> route L-HV on spread (total ≈ ${GOLDENS.spreadLhvTotalOv}),
    then hit overflow targets by moving cells or switching L-VH / maze.</p>`,
  challenges: [
    { id: "seed-ov", title: "Spread L-HV overflow", level: "Intro",
      prompt: "Route L-HV; total matches golden.",
      setup: (_c, api) => api.routeLHV(),
      check: (_c, api) => Math.abs(api.getOverflow().total - GOLDENS.spreadLhvTotalOv) < 0.01 },
    { id: "triple", title: "Metrics finite", level: "Intro",
      prompt: "total/max/count are finite after route.",
      setup: (_c, api) => api.routeLHV(),
      check: (_c, api) => {
        const o = api.getOverflow();
        return Number.isFinite(o.total)&&Number.isFinite(o.max)&&Number.isFinite(o.count); } },
    { id: "t1", title: "Total ≤ 1", level: "Practice",
      prompt: "Total overflow ≤ 1.",
      check: (_c, api) => api.getRoutes().length>0 && api.getOverflow().total <= 1 },
    { id: "m1", title: "Max ≤ 1", level: "Practice",
      prompt: "Max overflow ≤ 1.",
      check: (_c, api) => api.getRoutes().length>0 && api.getOverflow().max <= 1 },
    { id: "c1", title: "Count ≤ 1", level: "Practice",
      prompt: "At most one overflowing edge.",
      check: (_c, api) => api.getRoutes().length>0 && api.getOverflow().count <= 1 },
    { id: "zero", title: "Total = 0", level: "Challenge",
      prompt: "Clear all edge overflow.",
      check: (_c, api) => api.getRoutes().length>0 && api.getOverflow().total === 0 },
    { id: "maze-help", title: "Maze total ≤ 2", level: "Challenge",
      prompt: "Maze route with total ≤ 2.",
      check: (_c, api) => api.getRoutes().length>0 && api.getOverflow().total <= 2 },
    { id: "cap", title: "Cap = 2", level: "Intro",
      prompt: "Edge capacity is 2.",
      check: (_c, api) => api.getCapacity() === 2 },
  ],
});
