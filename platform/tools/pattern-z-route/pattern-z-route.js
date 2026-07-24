import {
  PLACEMENT, lRoute, zRoute, pathEdges, usageFromRoutes, edgeOverflow, EDGE_CAPACITY, terminalsFromPositions, NETS
} from "../../assets/global-routing-core.js";
import { createInteractiveGlobalRoutingLab } from "../../assets/interactive-global-routing-lab.js";
import { el } from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let lastZEdges = 0;
let lastLEdges = 0;

createInteractiveGlobalRoutingLab(root, {
  initialPositions: PLACEMENT,
  starterHtml: `<p><strong>Your job:</strong> compare Z vs L on net A–B. Click <em>Compare Z/L</em>, then route.</p>`,
  extraActions(_ctx, api) {
    return [el("button", { className:"btn btn-secondary", type:"button", text:"Compare Z/L on A–B",
      onClick: () => {
        const t = api.getTerminals();
        const z = zRoute(t.A, t.B);
        const l = lRoute(t.A, t.B, "HV");
        lastZEdges = pathEdges(z).length;
        lastLEdges = pathEdges(l).length;
        _ctx.rerender();
      }})];
  },
  extraMetrics() {
    return [`A–B Z edges: ${lastZEdges}`, `A–B L edges: ${lastLEdges}`];
  },
  challenges: [
    { id: "z-longer", title: "Z uses ≥ L edges", level: "Intro",
      prompt: "On spread A–B, Z path uses at least as many edges as L-HV.",
      check: () => {
        const t = terminalsFromPositions(PLACEMENT);
        return pathEdges(zRoute(t.A,t.B)).length >= pathEdges(lRoute(t.A,t.B,"HV")).length; } },
    { id: "compare-btn", title: "Run compare", level: "Intro",
      prompt: "Click Compare Z/L (metrics show edge counts).",
      check: () => lastZEdges > 0 },
    { id: "route-l", title: "Route L-HV", level: "Practice",
      prompt: "Route all nets with L-HV.",
      setup: (_c, api) => api.routeLHV(),
      check: (_c, api) => api.getRoutes().length === NETS.length },
    { id: "z-ov", title: "Z A–B overflow", level: "Practice",
      prompt: "Z-only A–B overflow is finite.",
      check: () => {
        const t = terminalsFromPositions(PLACEMENT);
        const u = usageFromRoutes([{ paths: [zRoute(t.A,t.B)] }]);
        return Number.isFinite(edgeOverflow(u, EDGE_CAPACITY).total); } },
    { id: "l-ov", title: "L overflow ≤ 2", level: "Practice",
      prompt: "L-HV on spread: total overflow ≤ 2.",
      setup: (_c, api) => api.routeLHV(),
      check: (_c, api) => api.getOverflow().total <= 2 },
    { id: "move-diff", title: "Move changes Z edges", level: "Challenge",
      prompt: "Move A or B so Z and L edge counts differ.",
      check: (_c, api) => {
        const t = api.getTerminals();
        return pathEdges(zRoute(t.A,t.B)).length !== pathEdges(lRoute(t.A,t.B,"HV")).length; } },
    { id: "max-le1", title: "Max ≤ 1 after route", level: "Challenge",
      prompt: "Route L-HV with max overflow ≤ 1.",
      check: (_c, api) => api.getRoutes().length>0 && api.getOverflow().max <= 1 },
    { id: "paths", title: "Z path length ≥ 3", level: "Intro",
      prompt: "Spread A–B Z path visits ≥3 GCells.",
      check: () => {
        const t = terminalsFromPositions(PLACEMENT);
        return zRoute(t.A, t.B).length >= 3; } },
  ],
});
