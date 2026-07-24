import {
  PLACEMENT,
  GOLDENS,
  GRID_NX,
  GRID_NY,
  sequentialDetailed,
  usageFromDetailedRoutes,
  ripupDetailed,
  terminalsFromPositions,
  NETS,
  TRACK_CAPACITY,
} from "../../assets/detailed-routing-core.js";

const spread = PLACEMENT;

function step(id, title, caption, bullets, metrics, positions, extra = {}) {
  return { id, title, caption, bullets, metrics, positions, ...extra };
}

function spreadSeq(mode = "l_hv") {
  const t = terminalsFromPositions(spread);
  return sequentialDetailed(NETS, t, mode);
}

export const DETAILED_ROUTING_ALGOS = {
  "routing-grid": {
    title: "Routing grid",
    module: "module01-01-routing-grid",
    kind: "detailed-routing",
    steps: [
      step("grid", "12×8 grid", "Detailed routes walk grid points; M1 horizontal, M2 vertical.", ["Cap=2 per track", "Blockage 2×2"], [`${GRID_NX}×${GRID_NY}`], spread),
      step("layers", "Two layers", "Horizontal moves on M1; vertical on M2; via switches at grid point.", ["M1 / M2", "Layer rules"], ["Not GCell"], spread),
      step("block", "Blockage", "Cells (5–6, 2–3) are blocked—maze must detour.", ["2×2 macro", "Pin nudge"], ["Lee lab"], spread, { highlight: ["E", "F"] }),
      step("neigh", "Neighbors", "Free grid points have up to four neighbors.", ["Four-connected"], [`mid=${GOLDENS.neighborCountMid}`], spread),
      step("cap", "Capacity", "Track usage vs capacity drives overflow and rip-up.", ["Cap=2"], ["Document goldens"], spread),
    ],
  },
  "pin-access": {
    title: "Pin access",
    module: "module01-03-pin-access",
    kind: "detailed-routing",
    steps: [
      step("map", "Pin → grid", "Cell centers round to grid indices.", ["Same spread as global"], ["Clamp on-chip"], spread),
      step("a11", "A → (1,1)", "Spread A lands on grid (1,1).", ["Terminals move with cells"], [`A ${GOLDENS.aPin}`], spread, { highlight: ["A"] }),
      step("d85", "D → (8,5)", "D at (8,5) top row.", ["Top row y=5"], [`D ${GOLDENS.dPin}`], spread, { highlight: ["D"] }),
      step("nudge", "Blocked pins", "E/F on blockage nudge to nearest free neighbor.", ["Access point", "Toy only"], ["Pin access"], spread, { highlight: ["E", "F"] }),
      step("route", "Routes from pins", "Sequential routes start/end at terminal grid points.", ["Not bbox"], ["Track usage"], spread, (() => { const s = spreadSeq("l_hv"); return { routes: s.routes, usage: s.usage }; })()),
    ],
  },
  "lee-maze": {
    title: "Lee maze",
    module: "module02-01-lee-maze",
    kind: "detailed-routing",
    steps: [
      step("bfs", "Breadth-first", "Lee expands uniformly—first arrival is shortest hop count.", ["Grid graph", "Blockage aware"], ["BFS layers"], spread),
      step("detour", "Around macro", "Path (4,1)→(7,1) detours below blockage.", ["Avoid blocked cells"], [`len=${GOLDENS.leeDetourLen}`], spread),
      step("lee", "Route Lee", "Sequential Lee assigns layers per step.", ["Six nets"], ["Finite cost"], spread, (() => { const s = spreadSeq("lee"); return { routes: s.routes, usage: s.usage }; })()),
      step("compare", "vs layered", "Lee may differ from L overflow totals.", ["Compare totals"], [`Lee total≈${GOLDENS.spreadLeeTotalOv}`], spread, (() => { const s = spreadSeq("lee"); return { routes: s.routes, usage: s.usage }; })()),
      step("use", "When to maze", "Use maze when pattern routes hit blockages or hot tracks.", ["Detailed stage"], ["A* next"], spread),
    ],
  },
  "astar-route": {
    title: "A* route",
    module: "module02-03-astar-route",
    kind: "detailed-routing",
    steps: [
      step("cost", "Track cost", "A* adds penalty when usage ≥ capacity.", ["Manhattan h", "Detour allowed"], ["Penalize hot tracks"], spread),
      step("l-ov", "Layered overflow", "Layered L-HV on spread overflows shared tracks.", ["Shared M1/M2"], [`total=${GOLDENS.spreadLhvTotalOv}`], spread, (() => { const s = spreadSeq("l_hv"); return { routes: s.routes, usage: s.usage }; })()),
      step("astar", "Route A*", "Sequential A* considers current usage.", ["Six nets"], [`total≈${GOLDENS.spreadAstarTotalOv}`], spread, (() => { const s = spreadSeq("astar"); return { routes: s.routes, usage: s.usage }; })()),
      step("compare", "Compare totals", "A* may clear overflow on the toy spread.", ["Not magic"], ["Still Cap=2"], spread, (() => { const s = spreadSeq("astar"); return { routes: s.routes, usage: s.usage }; })()),
      step("move", "Move pins", "Moving cells changes pin grid and paths.", ["Learner state"], ["Check scores routes"], spread),
    ],
  },
  "track-usage": {
    title: "Track usage",
    module: "module03-01-track-usage",
    kind: "detailed-routing",
    steps: [
      step("def", "Usage heat", "Each M1/M2 track accumulates routed net count.", ["Heat on canvas", "Red = overflow"], ["Usage map"], spread, (() => { const s = spreadSeq("l_hv"); return { routes: s.routes, usage: s.usage }; })()),
      step("total", "Total overflow", "Sum over tracks—primary scalar.", ["Primary metric"], [`spread layered≈${GOLDENS.spreadLhvTotalOv}`], spread, (() => { const s = spreadSeq("l_hv"); return { routes: s.routes, usage: s.usage }; })()),
      step("max", "Max overflow", "Worst track catches hotspot corridors.", ["Hotspot"], [`max≈${GOLDENS.spreadLhvMaxOv}`], spread, (() => { const s = spreadSeq("l_hv"); return { routes: s.routes, usage: s.usage }; })()),
      step("count", "Overflow count", "How many tracks exceed Cap.", ["Triple report"], ["Same pattern as global"], spread, (() => { const s = spreadSeq("l_hv"); return { routes: s.routes, usage: s.usage }; })()),
      step("target", "Hit targets", "Move pins or switch Lee/A* to clear thresholds.", ["Challenge lab"], ["No golden mode"], spread),
    ],
  },
  "via-assignment": {
    title: "Via assignment",
    module: "module03-03-via-assignment",
    kind: "detailed-routing",
    steps: [
      step("bend", "L-bend via", "Layered L places a via at the corner to switch M1→M2.", ["HV / VH"], ["Orange dot"], spread),
      step("ab", "A–C example", "Spread A–C layered path uses M1 then M2 with via.", ["Same pins"], ["Via at bend"], spread, { highlight: ["A", "C"] }),
      step("draw", "Canvas vias", "Walkthrough marks via points on the grid.", ["Layer discipline"], ["Marked vias"], spread, (() => { const s = spreadSeq("l_hv"); return { routes: s.routes, usage: s.usage }; })()),
      step("multi", "Multi-pin", "Four-pin net concatenates L legs—multiple vias possible.", ["Star center"], ["Four legs"], spread, { ...(() => { const s = spreadSeq("l_hv"); return { routes: s.routes, usage: s.usage }; })(), selectedNet: 4 }),
      step("drc", "Spacing next", "Vias do not replace DRC spacing checks.", ["Lite checker"], ["DRC lab"], spread),
    ],
  },
  "drc-spacing": {
    title: "DRC spacing",
    module: "module04-01-drc-spacing",
    kind: "detailed-routing",
    steps: [
      step("lite", "Lite checker", "Same-layer parallel segments one grid apart fail.", ["Toy rule", "Not full deck"], ["minDist=1"], spread),
      step("pass", "Spread pass", "Spread layered routes pass on the toy.", ["pass=true"], ["Spread starter"], spread, (() => { const s = spreadSeq("l_hv"); return { routes: s.routes, usage: s.usage }; })()),
      step("fail", "Violation demo", "Adjacent M1 rows at y=2 and y=3 fail minDist=1.", ["Fail case"], ["Teaching"], spread),
      step("route", "After route", "Run checker on learner sequential routes.", ["Check button"], ["Learner routes"], spread, (() => { const s = spreadSeq("l_hv"); return { routes: s.routes, usage: s.usage }; })()),
      step("real", "Real DRC", "Production routers use full width/spacing/via rules.", ["learn_drc next"], ["Signoff"], spread),
    ],
  },
  "ripup-detailed": {
    title: "Rip-up detailed",
    module: "module04-03-ripup-detailed",
    kind: "detailed-routing",
    steps: [
      step("seq", "Sequential first", "Route layered; tracks exceed Cap.", ["Overflow appears"], [`total=${GOLDENS.spreadLhvTotalOv}`], spread, (() => { const s = spreadSeq("l_hv"); return { routes: s.routes, usage: s.usage }; })()),
      step("pick", "Pick hot net", "Find net with worst overflow contribution.", ["One net rip"], ["Toy order"], spread, (() => { const s = spreadSeq("l_hv"); return { routes: s.routes, usage: s.usage }; })()),
      step("rip", "Rip segments", "Subtract ripped net from track usage.", ["Ready to reroute"], ["Before reroute"], spread, (() => { const s = spreadSeq("l_hv"); return { routes: s.routes, usage: s.usage }; })()),
      step("astar-r", "A* reroute", "Reroute ripped net with A* on updated usage.", ["May improve"], ["GOLDENS.ripupImproves"], spread, (() => {
        const t = terminalsFromPositions(spread);
        const s = spreadSeq("l_hv");
        const ripped = ripupDetailed([...s.routes], { ...s.usage }, TRACK_CAPACITY, t);
        return { routes: ripped, usage: usageFromDetailedRoutes(ripped) };
      })()),
      step("loop", "Iterate", "Real detailed routers loop route→DRC→rip until clean.", ["Course wrap"], ["learn_drc"], spread),
    ],
  },
  "sequential-detailed": {
    title: "Sequential detailed",
    module: "module05-01-sequential-detailed",
    kind: "detailed-routing",
    steps: [
      step("order", "Net order", "Route nets 0..5 in order; later nets see earlier usage.", ["Six nets"], ["NETS array"], spread),
      step("layer-all", "Layered pass", "Layered L all nets documents baseline overflow.", ["Pattern route"], [`total≈${GOLDENS.spreadLhvTotalOv}`], spread, (() => { const s = spreadSeq("l_hv"); return { routes: s.routes, usage: s.usage }; })()),
      step("lee-all", "Lee pass", "Sequential Lee may redistribute usage.", ["Maze mode"], [`Lee≈${GOLDENS.spreadLeeTotalOv}`], spread, (() => { const s = spreadSeq("lee"); return { routes: s.routes, usage: s.usage }; })()),
      step("clear", "Clear overflow", "Goal: total overflow 0 after A* or moves.", ["Challenge lab"], ["HPWL optional"], spread, (() => { const s = spreadSeq("astar"); return { routes: s.routes, usage: s.usage }; })()),
      step("done", "Handoff", "Detailed routing feeds signoff DRC and extraction.", ["Tracks + vias"], ["learn_drc next"], spread),
    ],
  },
};
