import { GOLDENS, PLACEMENT } from "../../assets/detailed-routing-core.js";
import { createInteractiveDetailedRoutingLab } from "../../assets/interactive-detailed-routing-lab.js";

const root = document.getElementById("lab-root");
createInteractiveDetailedRoutingLab(root, {
  initialPositions: PLACEMENT,
  starterHtml: `<p><strong>Your job:</strong> route layered L first (overflow ≈ ${GOLDENS.spreadLhvTotalOv}),
    then A* (golden total ≈ ${GOLDENS.spreadAstarTotalOv}).</p>`,
  challenges: [
    { id: "layer-first", title: "Layered has overflow", level: "Intro",
      prompt: "Route layered; total overflow > 0 on spread.",
      setup: (_c, api) => api.routeLayered(),
      check: (_c, api) => api.getOverflow().total > 0 },
    { id: "astar-route", title: "Route A*", level: "Intro",
      prompt: "Click Route A*.",
      setup: (_c, api) => api.routeAstar(),
      check: (_c, api) => api.getRoutes().some(r => r.segments?.length) },
    { id: "astar-golden", title: "A* golden total", level: "Intro",
      prompt: "Spread A* total overflow matches golden.",
      setup: (_c, api) => api.routeAstar(),
      check: (_c, api) => Math.abs(api.getOverflow().total - GOLDENS.spreadAstarTotalOv) < 0.01 },
    { id: "astar-le-layer", title: "A* ≤ layered", level: "Practice",
      prompt: "A* total overflow ≤ layered on same placement.",
      check: (_c, api) => {
        api.routeLayered(); const l = api.getOverflow().total;
        api.routeAstar(); return api.getOverflow().total <= l + 0.01; } },
    { id: "max-le1", title: "Max ≤ 1", level: "Practice",
      prompt: "A* route with max overflow ≤ 1.",
      check: (_c, api) => api.getRoutes().some(r => r.segments?.length) && api.getOverflow().max <= 1 },
    { id: "zero-astar", title: "Clear overflow", level: "Challenge",
      prompt: "A* achieves total overflow 0.",
      setup: (_c, api) => api.routeAstar(),
      check: (_c, api) => api.getOverflow().total === 0 },
    { id: "mode-astar", title: "Mode is astar", level: "Intro",
      prompt: "After Route A*, mode is astar.",
      setup: (_c, api) => api.routeAstar(),
      check: (_c, api) => api.getMode() === "astar" },
    { id: "hpwl", title: "HPWL finite", level: "Intro",
      prompt: "HPWL is finite.",
      check: (_c, api) => Number.isFinite(api.getHpwl()) },
  ],
});
