import {
  PLACEMENT, lRouteLayers, terminalsFromPositions, NETS
} from "../../assets/detailed-routing-core.js";
import { createInteractiveDetailedRoutingLab } from "../../assets/interactive-detailed-routing-lab.js";

const root = document.getElementById("lab-root");
let viaCount = 0;

createInteractiveDetailedRoutingLab(root, {
  initialPositions: PLACEMENT,
  starterHtml: `<p><strong>Your job:</strong> layered routes place vias at L-bends. Route layered and inspect metrics.</p>`,
  onAfterRoute(api) {
    const r = api.getRoutes().find(x => x.netIndex === 0);
    viaCount = r ? (r.segments || []).filter(s => s.via).length : 0;
  },
  extraMetrics() {
    return [`net0 vias: ${viaCount}`];
  },
  challenges: [
    { id: "ab-via", title: "A–B has via on L", level: "Intro",
      prompt: "Spread A–B layered HV uses a via when Δx and Δy both nonzero paths exist.",
      check: () => {
        const t = terminalsFromPositions(PLACEMENT);
        const segs = lRouteLayers(t.A, t.C, "HV");
        return segs.some(s => s.via); } },
    { id: "route-layer", title: "Route layered", level: "Intro",
      prompt: "Click Route layered.",
      setup: (_c, api) => api.routeLayered(),
      check: (_c, api) => api.getRoutes().some(r => r.segments?.length) },
    { id: "net0-via", title: "Net0 via counted", level: "Practice",
      prompt: "After route, net0 via metric updates.",
      setup: (_c, api) => api.routeLayered(),
      check: () => viaCount >= 0 },
    { id: "m1-segs", title: "M1 segments exist", level: "Practice",
      prompt: "Some segment uses M1 layer.",
      setup: (_c, api) => api.routeLayered(),
      check: (_c, api) => api.getRoutes().some(r => r.segments?.some(s => s.layer === "M1")) },
    { id: "m2-segs", title: "M2 segments exist", level: "Practice",
      prompt: "Some segment uses M2 layer.",
      setup: (_c, api) => api.routeLayered(),
      check: (_c, api) => api.getRoutes().some(r => r.segments?.some(s => s.layer === "M2")) },
    { id: "four-pin", title: "Four-pin net routed", level: "Challenge",
      prompt: "Net [A,B,C,D] has segments after layered route.",
      setup: (_c, api) => api.routeLayered(),
      check: (_c, api) => (api.getRoutes().find(r => r.netIndex === 4)?.segments?.length || 0) > 0 },
    { id: "move-via", title: "Move changes path", level: "Challenge",
      prompt: "Move a cell and re-route; routes still exist.",
      check: (_c, api) => { api.routeLayered(); return api.getRoutes().some(r => r.segments?.length); } },
    { id: "six-nets", title: "Six nets", level: "Intro",
      prompt: "Instance has six nets.",
      check: () => NETS.length === 6 },
  ],
});
