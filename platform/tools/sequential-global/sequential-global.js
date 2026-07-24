import { GOLDENS, PLACEMENT, NETS } from "../../assets/global-routing-core.js";
import { createInteractiveGlobalRoutingLab } from "../../assets/interactive-global-routing-lab.js";

const root = document.getElementById("lab-root");
createInteractiveGlobalRoutingLab(root, {
  initialPositions: PLACEMENT,
  starterHtml: `<p><strong>Your job:</strong> route all ${NETS.length} nets. Try L-HV, L-VH, maze until overflow clears.</p>`,
  challenges: [
    { id: "six-nets", title: "Six nets", level: "Intro",
      prompt: "Instance has six nets.",
      check: () => NETS.length === 6 },
    { id: "route-all", title: "Route all", level: "Intro",
      prompt: "Route all nets (any mode).",
      check: (_c, api) => api.getRoutes().length === 6 },
    { id: "l-hv", title: "L-HV routed", level: "Practice",
      prompt: "Route L-HV for all nets.",
      setup: (_c, api) => api.routeLHV(),
      check: (_c, api) => api.getRoutes().length === 6 && api.getPrefer()==="HV" },
    { id: "total-le2", title: "Total ≤ 2", level: "Practice",
      prompt: "Total overflow ≤ 2 after routing.",
      check: (_c, api) => api.getRoutes().length>0 && api.getOverflow().total <= 2 },
    { id: "total-le1", title: "Total ≤ 1", level: "Practice",
      prompt: "Total overflow ≤ 1.",
      check: (_c, api) => api.getRoutes().length>0 && api.getOverflow().total <= 1 },
    { id: "zero", title: "Zero overflow", level: "Challenge",
      prompt: "Route with zero edge overflow.",
      check: (_c, api) => api.getRoutes().length>0 && api.getOverflow().total === 0 },
    { id: "maze-zero", title: "Maze clears", level: "Challenge",
      prompt: "Move cells if needed; maze route achieves total overflow 0.",
      check: (_c, api) => api.getRoutes().length>0 && api.getOverflow().total === 0 },
    { id: "hpwl", title: "HPWL tracked", level: "Intro",
      prompt: "HPWL is reported while routing.",
      check: (_c, api) => Number.isFinite(api.getHpwl()) },
  ],
});
