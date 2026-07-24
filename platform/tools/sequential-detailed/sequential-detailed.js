import { GOLDENS, PLACEMENT, NETS } from "../../assets/detailed-routing-core.js";
import { createInteractiveDetailedRoutingLab } from "../../assets/interactive-detailed-routing-lab.js";

const root = document.getElementById("lab-root");
createInteractiveDetailedRoutingLab(root, {
  initialPositions: PLACEMENT,
  starterHtml: `<p><strong>Your job:</strong> route all ${NETS.length} nets sequentially.
    Try layered, Lee, or A* until overflow clears.</p>`,
  challenges: [
    { id: "six-nets", title: "Six nets", level: "Intro",
      prompt: "Instance has six nets.",
      check: () => NETS.length === 6 },
    { id: "route-all", title: "Route all", level: "Intro",
      prompt: "Route all nets (any mode).",
      check: (_c, api) => api.getRoutes().filter(r => r.segments?.length).length === 6 },
    { id: "layer-all", title: "Layered routed", level: "Practice",
      prompt: "Route layered for all nets.",
      setup: (_c, api) => api.routeLayered(),
      check: (_c, api) => api.getMode() === "l_hv" && api.getRoutes().filter(r => r.segments?.length).length === 6 },
    { id: "total-le3", title: "Total ≤ 3", level: "Practice",
      prompt: "Total overflow ≤ 3 after routing.",
      check: (_c, api) => api.getRoutes().some(r => r.segments?.length) && api.getOverflow().total <= 3 },
    { id: "total-le1", title: "Total ≤ 1", level: "Practice",
      prompt: "Total overflow ≤ 1.",
      check: (_c, api) => api.getRoutes().some(r => r.segments?.length) && api.getOverflow().total <= 1 },
    { id: "zero", title: "Zero overflow", level: "Challenge",
      prompt: "Route with zero track overflow.",
      check: (_c, api) => api.getRoutes().some(r => r.segments?.length) && api.getOverflow().total === 0 },
    { id: "astar-zero", title: "A* clears", level: "Challenge",
      prompt: "A* route achieves total overflow 0 on spread.",
      setup: (_c, api) => api.routeAstar(),
      check: (_c, api) => api.getOverflow().total === 0 },
    { id: "hpwl", title: "HPWL tracked", level: "Intro",
      prompt: "HPWL is reported while routing.",
      check: (_c, api) => Number.isFinite(api.getHpwl()) },
  ],
});
