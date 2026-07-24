import { GOLDENS, PLACEMENT } from "../../assets/global-routing-core.js";
import { createInteractiveGlobalRoutingLab } from "../../assets/interactive-global-routing-lab.js";

const root = document.getElementById("lab-root");
createInteractiveGlobalRoutingLab(root, {
  initialPositions: PLACEMENT,
  starterHtml: `<p><strong>Your job:</strong> click Route L-HV or L-VH on spread starter.
    HV total overflow ≈ ${GOLDENS.spreadLhvTotalOv}; VH ≈ ${GOLDENS.spreadLvhTotalOv}.</p>`,
  onLoadStarter(api) { api.clearRoutes(); },
  challenges: [
    { id: "route-hv", title: "Route L-HV", level: "Intro",
      prompt: "Click Route L-HV so routes exist.",
      check: (_c, api) => api.getRoutes().length > 0 && api.getPrefer()==="HV" },
    { id: "hv-ov", title: "HV overflow known", level: "Intro",
      prompt: "On spread + L-HV, total overflow matches golden (${GOLDENS.spreadLhvTotalOv}).",
      setup: (_c, api) => api.routeLHV(),
      check: (_c, api) => Math.abs(api.getOverflow().total - GOLDENS.spreadLhvTotalOv) < 0.01 },
    { id: "vh-better", title: "VH ≤ HV overflow", level: "Practice",
      prompt: "Route L-VH; total overflow ≤ L-HV on same placement.",
      setup: (_c, api) => api.routeLVH(),
      check: (_c, api) => api.getOverflow().total <= GOLDENS.spreadLhvTotalOv + 0.01 },
    { id: "move-cut", title: "Total ≤ 1", level: "Practice",
      prompt: "Move cells and route L-HV until total overflow ≤ 1.",
      check: (_c, api) => api.getRoutes().length>0 && api.getOverflow().total <= 1 },
    { id: "max-one", title: "Max overflow ≤ 1", level: "Practice",
      prompt: "Keep max edge overflow ≤ 1 after routing.",
      check: (_c, api) => api.getRoutes().length>0 && api.getOverflow().max <= 1 },
    { id: "count-le2", title: "Count ≤ 2", level: "Challenge",
      prompt: "At most two overflowing edges.",
      check: (_c, api) => api.getRoutes().length>0 && api.getOverflow().count <= 2 },
    { id: "zero", title: "Clear overflow", level: "Challenge",
      prompt: "Route with total overflow 0.",
      check: (_c, api) => api.getRoutes().length>0 && api.getOverflow().total === 0 },
    { id: "hpwl", title: "HPWL finite", level: "Intro",
      prompt: "HPWL is finite.",
      check: (_c, api) => Number.isFinite(api.getHpwl()) },
  ],
});
