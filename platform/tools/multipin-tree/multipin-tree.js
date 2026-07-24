import { PLACEMENT, NETS, multipinStar, terminalsFromPositions } from "../../assets/global-routing-core.js";
import { createInteractiveGlobalRoutingLab } from "../../assets/interactive-global-routing-lab.js";

const root = document.getElementById("lab-root");
const NET4 = NETS[4];

createInteractiveGlobalRoutingLab(root, {
  initialPositions: PLACEMENT,
  starterHtml: `<p><strong>Your job:</strong> net4 is [A,B,C,D]. Route L-HV; the star uses four legs from center.</p>`,
  extraMetrics(api) {
    const r = api.getRoutes().find(x => x.netIndex === 4);
    const legs = r ? r.paths.length : 0;
    return [`net4 legs: ${legs}`];
  },
  challenges: [
    { id: "net4-exists", title: "Net4 listed", level: "Intro",
      prompt: "Fifth net (index 4) is the 4-pin net.",
      check: () => NET4.join(",") === "A,B,C,D" },
    { id: "star-legs", title: "Four legs", level: "Intro",
      prompt: "After L-HV route, net4 has four path legs.",
      setup: (_c, api) => api.routeLHV(),
      check: (_c, api) => api.getRoutes().find(r=>r.netIndex===4)?.paths.length === 4 },
    { id: "star-center", title: "Center GCell valid", level: "Practice",
      prompt: "Star center is an on-chip GCell.",
      check: () => {
        const t = terminalsFromPositions(PLACEMENT);
        const pins = NET4.map(id => t[id]);
        const c = multipinStar(pins).center;
        return c.i>=0&&c.i<4&&c.j>=0&&c.j<2; } },
    { id: "route-all", title: "Route all nets", level: "Practice",
      prompt: "Route L-HV for all six nets.",
      setup: (_c, api) => api.routeLHV(),
      check: (_c, api) => api.getRoutes().length === 6 },
    { id: "usage-pos", title: "Edge usage > 0", level: "Practice",
      prompt: "After routing, some edge has usage > 0.",
      setup: (_c, api) => api.routeLHV(),
      check: (_c, api) => Object.values(api.getUsage()).some(v => v > 0) },
    { id: "move-tree", title: "Move changes legs", level: "Challenge",
      prompt: "Move a 4-pin cell; re-route; net4 still has four legs.",
      check: (_c, api) => {
        api.routeLHV();
        return api.getRoutes().find(r=>r.netIndex===4)?.paths.length === 4; } },
    { id: "ov-finite", title: "Overflow finite", level: "Intro",
      prompt: "Overflow metrics finite after route.",
      setup: (_c, api) => api.routeLHV(),
      check: (_c, api) => Number.isFinite(api.getOverflow().total) },
    { id: "ef-short", title: "E–F two-pin", level: "Intro",
      prompt: "Net5 (E–F) is two-pin with one path.",
      setup: (_c, api) => api.routeLHV(),
      check: (_c, api) => api.getRoutes().find(r=>r.netIndex===5)?.paths.length === 1 },
  ],
});
