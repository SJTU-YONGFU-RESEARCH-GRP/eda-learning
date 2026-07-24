import { GOLDENS, PLACEMENT } from "../../assets/global-routing-core.js";
import { createInteractiveGlobalRoutingLab } from "../../assets/interactive-global-routing-lab.js";

const root = document.getElementById("lab-root");
createInteractiveGlobalRoutingLab(root, {
  initialPositions: PLACEMENT,
  starterHtml: `<p><strong>Your job:</strong> route L-HV first (overflow ≈ ${GOLDENS.spreadLhvTotalOv}),
    then try Route maze. Maze may reduce or redistribute overflow.</p>`,
  challenges: [
    { id: "l-first", title: "L-HV has overflow", level: "Intro",
      prompt: "Route L-HV on spread; total overflow > 0.",
      setup: (_c, api) => api.routeLHV(),
      check: (_c, api) => api.getOverflow().total > 0 },
    { id: "maze-route", title: "Route maze", level: "Intro",
      prompt: "Click Route maze.",
      setup: (_c, api) => api.routeMaze(),
      check: (_c, api) => api.getRoutes().length > 0 },
    { id: "maze-total", title: "Maze total finite", level: "Practice",
      prompt: "Maze total overflow is finite.",
      setup: (_c, api) => api.routeMaze(),
      check: (_c, api) => Number.isFinite(api.getOverflow().total) },
    { id: "maze-le-l", title: "Maze total ≤ L-HV", level: "Practice",
      prompt: "Maze total overflow ≤ L-HV on same placement.",
      check: (_c, api) => {
        api.routeLHV(); const l = api.getOverflow().total;
        api.routeMaze(); return api.getOverflow().total <= l + 0.01; } },
    { id: "clear-maze", title: "Maze total ≤ 1", level: "Challenge",
      prompt: "Move cells; maze route with total ≤ 1.",
      check: (_c, api) => api.getRoutes().length>0 && api.getOverflow().total <= 1 },
    { id: "max-maze", title: "Maze max ≤ 1", level: "Challenge",
      prompt: "Maze max overflow ≤ 1.",
      check: (_c, api) => api.getRoutes().length>0 && api.getOverflow().max <= 1 },
    { id: "zero-maze", title: "Maze clears overflow", level: "Challenge",
      prompt: "Achieve total overflow 0 with maze routing.",
      check: (_c, api) => api.getRoutes().length>0 && api.getOverflow().total === 0 },
    { id: "routes-six", title: "Six nets routed", level: "Intro",
      prompt: "All six nets have routes after maze.",
      setup: (_c, api) => api.routeMaze(),
      check: (_c, api) => api.getRoutes().length === 6 },
  ],
});
