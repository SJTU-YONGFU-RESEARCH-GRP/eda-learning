#!/usr/bin/env python3
"""Generate learn_global_routing interactive tools + global-routing-algos.js + wire walkthrough."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TOOLS = ROOT / "platform" / "tools"
WALK = TOOLS / "algorithm-walkthrough"
CAPTURE = ROOT / ".cursor" / "skills" / "module-slides" / "scripts" / "capture_algorithm_walkthrough.py"

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — EDA Algorithms Platform</title>
  <link rel="stylesheet" href="../../assets/site.css">
  <link rel="stylesheet" href="../../assets/tools-shared.css">
  <link rel="stylesheet" href="../../assets/clustering-lab.css">
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="site-header-inner">
      <p class="brand"><a href="../../index.html">EDA Algorithms Platform</a></p>
      <nav class="site-nav" aria-label="Site">
        <a href="../../index.html">Home</a>
        <a href="../index.html" class="is-active" aria-current="page">Tools</a>
      </nav>
    </div>
    <div class="site-header-crumb">
      <nav aria-label="Breadcrumb">
        <a href="../../index.html">Home</a>
        <a href="../index.html">Tools</a>
        <span class="here">{title}</span>
      </nav>
    </div>
  </header>
  <main id="main">
    <div class="eyebrow">Interactive tool</div>
    <section class="hero">
      <h1>{title}</h1>
      <p class="lead">{lead}</p>
    </section>
    <div id="lab-root"></div>
  </main>
  <footer class="site-footer">EDA Algorithms Platform — client-side concept labs.</footer>
  <script type="module" src="{lab}.js"></script>
  <script src="../../assets/site.js"></script>
</body>
</html>
"""

LABS = {
    "routing-graph": {
        "title": "GCell routing graph",
        "lead": "Four-by-two GCell grid with horizontal and vertical edges; capacity two per edge.",
        "js": r'''import {
  GOLDENS, PLACEMENT, allEdges, neighbors, gcellKey
} from "../../assets/global-routing-core.js";
import { createInteractiveGlobalRoutingLab } from "../../assets/interactive-global-routing-lab.js";

const root = document.getElementById("lab-root");
createInteractiveGlobalRoutingLab(root, {
  initialPositions: PLACEMENT,
  starterHtml: `<p><strong>Your job:</strong> explore the routing graph. Edge count is ${GOLDENS.edgeCount}.
    Interior GCells have up to four neighbors; corners have two.</p>`,
  extraMetrics(api) {
    const t = api.getTerminals();
    const g = t.A;
    return [`A GCell: (${g.i},${g.j})`, `neighbors(A): ${neighbors(g).length}`];
  },
  challenges: [
    { id: "edge-count", title: "Ten edges", level: "Intro",
      prompt: "This 4×2 grid has exactly ten routing edges.",
      check: () => allEdges().length === GOLDENS.edgeCount },
    { id: "cap-two", title: "Capacity is 2", level: "Intro",
      prompt: "Each edge capacity equals 2.",
      check: (_c, api) => api.getCapacity() === GOLDENS.edgeCapacity },
    { id: "mid-neigh", title: "Mid cell ≥3 neighbors", level: "Intro",
      prompt: "GCell (1,0) has at least three neighbors.",
      check: () => neighbors({ i: 1, j: 0 }).length >= GOLDENS.neighborCountMid },
    { id: "corner-neigh", title: "Corner has 2 neighbors", level: "Practice",
      prompt: "Corner (0,0) has exactly two neighbors.",
      check: () => neighbors({ i: 0, j: 0 }).length === 2 },
    { id: "grid-shape", title: "Grid is 4×2", level: "Intro",
      prompt: "Confirm GOLDENS grid shape.",
      check: () => GOLDENS.gcellNx === 4 && GOLDENS.gcellNy === 2 },
    { id: "unique-keys", title: "Unique edge keys", level: "Practice",
      prompt: "All edge keys are unique strings.",
      check: () => new Set(allEdges()).size === allEdges().length },
    { id: "h-edges", title: "Six horizontal edges", level: "Practice",
      prompt: "Count horizontal edges (same j, adjacent i).",
      check: () => allEdges().filter(e => e.split("|")[0].split(",")[1] === e.split("|")[1].split(",")[1]).length === 6 },
    { id: "v-edges", title: "Four vertical edges", level: "Practice",
      prompt: "Count vertical edges (same i, adjacent j).",
      check: () => allEdges().filter(e => e.split("|")[0].split(",")[0] === e.split("|")[1].split(",")[0]).length === 4 },
  ],
});
''',
    },
    "terminal-gcells": {
        "title": "Terminal GCell mapping",
        "lead": "Map each cell center to the GCell tile that owns its pin.",
        "js": r'''import {
  GOLDENS, PLACEMENT, CLUSTER_SEED, cellGcell
} from "../../assets/global-routing-core.js";
import { createInteractiveGlobalRoutingLab } from "../../assets/interactive-global-routing-lab.js";

const root = document.getElementById("lab-root");
createInteractiveGlobalRoutingLab(root, {
  initialPositions: PLACEMENT,
  revealPositions: CLUSTER_SEED,
  starterHtml: `<p><strong>Your job:</strong> on spread starter, A→(0,0) and D→(2,1).
    Move cells; terminals follow pins into GCells.</p>`,
  challenges: [
    { id: "a00", title: "A in (0,0)", level: "Intro",
      prompt: "On spread starter, A is in GCell (0,0).",
      check: (_c, api) => { const g=api.getTerminals().A; return g.i===0&&g.j===0; } },
    { id: "d21", title: "D in (2,1)", level: "Intro",
      prompt: "On spread starter, D is in GCell (2,1).",
      check: (_c, api) => { const g=api.getTerminals().D; return g.i===2&&g.j===1; } },
    { id: "move-e", title: "E to col 3", level: "Practice",
      prompt: "Place E so its GCell column i=3.",
      check: (_c, api) => api.getTerminals().E.i === 3 },
    { id: "b-bottom", title: "B row j=0", level: "Practice",
      prompt: "Keep B in bottom row j=0.",
      check: (_c, api) => api.getTerminals().B.j === 0 },
    { id: "c-top", title: "C row j=1", level: "Practice",
      prompt: "On spread starter C is in j=1.",
      check: (_c, api) => api.getTerminals().C.j === 1 },
    { id: "f-col2", title: "F in col 2", level: "Practice",
      prompt: "Place F with i=2.",
      check: (_c, api) => api.getTerminals().F.i === 2 },
    { id: "all-valid", title: "All on-chip GCells", level: "Challenge",
      prompt: "Every terminal has valid (i,j).",
      check: (_c, api) => Object.values(api.getTerminals()).every(g => g.i>=0&&g.i<4&&g.j>=0&&g.j<2) },
    { id: "golden-a", title: "Golden A col 1", level: "Intro",
      prompt: "GOLDENS documents A at (0,0) on spread.",
      check: () => GOLDENS.aGcell[0]===0 && GOLDENS.aGcell[1]===0 },
  ],
});
''',
    },
    "pattern-l-route": {
        "title": "L-pattern routing",
        "lead": "Route nets with horizontal-then-vertical or vertical-then-horizontal L-shapes.",
        "js": r'''import { GOLDENS, PLACEMENT } from "../../assets/global-routing-core.js";
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
''',
    },
    "pattern-z-route": {
        "title": "Z vs L routing",
        "lead": "Compare Z-shaped two-bend routes with single-bend L routes on the same pins.",
        "js": r'''import {
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
''',
    },
    "maze-gcell-route": {
        "title": "Maze GCell routing",
        "lead": "Maze search detours around saturated edges when L-routes overflow.",
        "js": r'''import { GOLDENS, PLACEMENT } from "../../assets/global-routing-core.js";
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
''',
    },
    "multipin-tree": {
        "title": "Multi-pin Steiner tree",
        "lead": "Four-pin net A–B–C–D routes as a star from the bbox center GCell.",
        "js": r'''import { PLACEMENT, NETS, multipinStar, terminalsFromPositions } from "../../assets/global-routing-core.js";
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
''',
    },
    "edge-overflow": {
        "title": "Edge overflow metrics",
        "lead": "Report total, max, and overflowing-edge count from routed usage.",
        "js": r'''import { GOLDENS, PLACEMENT } from "../../assets/global-routing-core.js";
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
''',
    },
    "ripup-reroute": {
        "title": "Rip-up and reroute",
        "lead": "After sequential L routing overflows, rip-up and maze-reroute hot nets.",
        "js": r'''import { GOLDENS, PLACEMENT } from "../../assets/global-routing-core.js";
import { createInteractiveGlobalRoutingLab } from "../../assets/interactive-global-routing-lab.js";

const root = document.getElementById("lab-root");
let beforeRip = null;

createInteractiveGlobalRoutingLab(root, {
  initialPositions: PLACEMENT,
  starterHtml: `<p><strong>Your job:</strong> Route L-HV, note overflow, click Rip-up reroute.
    Golden: rip-up can reduce total on hot corridors.</p>`,
  onAfterRoute(api) {
    if (beforeRip == null && api.getRoutes().length) beforeRip = api.getOverflow().total;
  },
  extraMetrics(api) {
    const lines = [];
    if (beforeRip != null) lines.push(`before rip: ${beforeRip.toFixed(2)}`);
    return lines;
  },
  challenges: [
    { id: "l-route", title: "Route L-HV first", level: "Intro",
      prompt: "Route L-HV before rip-up.",
      setup: (_c, api) => { beforeRip=null; api.routeLHV(); beforeRip=api.getOverflow().total; },
      check: (_c, api) => api.getRoutes().length > 0 },
    { id: "has-ov", title: "Overflow before rip", level: "Intro",
      prompt: "Spread L-HV has overflow > 0.",
      setup: (_c, api) => { api.routeLHV(); beforeRip=api.getOverflow().total; },
      check: (_c, api) => api.getOverflow().total > 0 },
    { id: "rip-btn", title: "Run rip-up", level: "Practice",
      prompt: "Click Rip-up reroute.",
      setup: (_c, api) => { api.routeLHV(); beforeRip=api.getOverflow().total; api.ripupReroute(); },
      check: (_c, api) => api.getRoutes().length > 0 },
    { id: "not-worse", title: "Rip ≤ before", level: "Practice",
      prompt: "After rip-up, total overflow ≤ before.",
      setup: (_c, api) => {
        api.routeLHV(); beforeRip=api.getOverflow().total; api.ripupReroute(); },
      check: (_c, api) => api.getOverflow().total <= beforeRip + 0.01 },
    { id: "improve", title: "Rip improves or clears", level: "Challenge",
      prompt: "Rip-up strictly lowers total or clears overflow.",
      setup: (_c, api) => {
        api.routeLHV(); beforeRip=api.getOverflow().total; api.ripupReroute(); },
      check: (_c, api) => api.getOverflow().total < beforeRip || api.getOverflow().total === 0 },
    { id: "max-drop", title: "Max ≤ 1 after rip", level: "Challenge",
      prompt: "After rip-up, max overflow ≤ 1.",
      check: (_c, api) => {
        if (!api.getRoutes().length) api.routeLHV();
        api.ripupReroute();
        return api.getOverflow().max <= 1; } },
    { id: "golden", title: "Rip helper ok", level: "Intro",
      prompt: "GOLDENS documents rip-up can improve overflow.",
      check: () => GOLDENS.ripupImproves === true },
    { id: "six-nets", title: "Six nets after rip", level: "Intro",
      prompt: "Still six net routes after rip-up.",
      setup: (_c, api) => { api.routeLHV(); api.ripupReroute(); },
      check: (_c, api) => api.getRoutes().length === 6 },
  ],
});
''',
    },
    "sequential-global": {
        "title": "Sequential global routing",
        "lead": "Route all six nets in order; clear overflow thresholds on the tiny instance.",
        "js": r'''import { GOLDENS, PLACEMENT, NETS } from "../../assets/global-routing-core.js";
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
''',
    },
}


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def write_tools() -> None:
    for lab, meta in LABS.items():
        write(TOOLS / lab / "index.html", HTML.format(title=meta["title"], lead=meta["lead"], lab=lab))
        write(TOOLS / lab / f"{lab}.js", meta["js"])
    print(f"Wrote {len(LABS)} tools")


def write_algos() -> None:
    write(
        WALK / "global-routing-algos.js",
        r'''import {
  PLACEMENT,
  CLUSTER_SEED,
  GOLDENS,
  allEdges,
  neighbors,
  lRoute,
  zRoute,
  mazeRoute,
  multipinStar,
  routeAllL,
  routeAllMaze,
  usageFromRoutes,
  edgeOverflow,
  ripupReroute,
  terminalsFromPositions,
  NETS,
  EDGE_CAPACITY,
} from "../../assets/global-routing-core.js";

const spread = PLACEMENT;
const seed = CLUSTER_SEED;

function step(id, title, caption, bullets, metrics, positions, extra = {}) {
  return { id, title, caption, bullets, metrics, positions, ...extra };
}

function spreadRoutes(prefer = "HV") {
  const t = terminalsFromPositions(spread);
  return routeAllL(NETS, t, prefer);
}

export const GLOBAL_ROUTING_ALGOS = {
  "routing-graph": {
    title: "Routing graph",
    module: "module01-01-routing-graph",
    kind: "global-routing",
    steps: [
      step("grid", "GCell graph", "Four-by-two GCells form a grid graph: nodes are tiles, edges are adjacency.", ["10 edges total", "Cap=2 per edge"], [`edges: ${GOLDENS.edgeCount}`], spread),
      step("h", "Horizontal edges", "Three horizontal edges per row connect columns i and i+1.", ["6 horizontal"], ["Same j"], spread),
      step("v", "Vertical edges", "Four vertical edges connect rows j and j+1.", ["4 vertical"], ["Same i"], spread),
      step("neigh", "Neighbors", "Interior GCell (1,0) has three neighbors; corners have two.", [`mid=${GOLDENS.neighborCountMid}`], spread, { highlight: ["B"] }),
      step("cap", "Capacity", "Each edge tracks usage vs capacity—overflow drives rip-up.", ["Cap=2"], ["Document goldens"], spread),
    ],
  },
  "terminal-gcells": {
    title: "Terminal GCells",
    module: "module01-03-terminal-gcells",
    kind: "global-routing",
    steps: [
      step("map", "Pin → GCell", "Cell centers map to GCells with floor(x/cellW), floor(y/cellH).", ["Same as congestion grid"], ["i,j clamped"], spread),
      step("a00", "A → (0,0)", "Spread A at (1,1) lands in GCell (0,0).", ["Terminals move with cells"], [`A ${GOLDENS.aGcell}`], spread, { highlight: ["A"] }),
      step("d21", "D → (2,1)", "D at (8,5) → (2,1) top row.", ["Top row j=1"], [`D ${GOLDENS.dGcell}`], spread, { highlight: ["D"] }),
      step("route", "Routes on graph", "Global routes walk GCell edges between terminal tiles.", ["Not bbox paint"], ["Edge usage"], spread, { routes: spreadRoutes("HV") }),
      step("cluster", "Cluster seed", "Tight cluster maps many pins to one GCell—zero-length routes.", ["Hot for study"], ["Spread for overflow"], seed),
    ],
  },
  "pattern-l-route": {
    title: "L-pattern route",
    module: "module02-01-pattern-l-route",
    kind: "global-routing",
    steps: [
      step("idea", "L-shape", "Two-pin nets use one bend: HV (horizontal first) or VH.", ["Manhattan"], ["One corner"], spread),
      step("hv", "Route L-HV", "Spread placement L-HV yields documented overflow.", [`total≈${GOLDENS.spreadLhvTotalOv}`], spread, { routes: spreadRoutes("HV") }),
      step("vh", "Route L-VH", "Swapping bend order changes which edges saturate.", [`VH total≈${GOLDENS.spreadLvhTotalOv}`], spread, { routes: spreadRoutes("VH") }),
      step("edges", "Edge usage", "Thicker edges show usage; red dash marks overflow.", ["usage vs cap"], ["max/count"], spread, { routes: spreadRoutes("HV") }),
      step("move", "Move pins", "Moving cells changes terminal GCells and L paths.", ["Learner state"], ["Check scores routes"], spread),
    ],
  },
  "pattern-z-route": {
    title: "Z-pattern route",
    module: "module02-03-pattern-z-route",
    kind: "global-routing",
    steps: [
      step("z", "Two bends", "Z-route uses a midpoint column (or row) with two corners.", ["vs one-bend L"], ["More edges possible"], spread),
      step("ab", "A–B compare", "On spread, Z and L may differ in edge count and overflow.", ["Compare metrics"], ["Same pins"], spread, { highlightPath: (() => { const t=terminalsFromPositions(spread); return zRoute(t.A,t.D); })() }),
      step("l", "L reference", "L-HV is the fast pattern route baseline.", ["Prefer HV/VH"], ["Pattern router"], spread, { routes: spreadRoutes("HV") }),
      step("ov", "Overflow tradeoff", "Extra bends can spread or concentrate edge usage.", ["Not always better"], ["Measure"], spread, { routes: spreadRoutes("HV") }),
      step("next", "Maze escape", "When L/Z overflow, maze search detours.", ["Penalize saturated edges"], ["Next lab"], spread),
    ],
  },
  "maze-gcell-route": {
    title: "Maze routing",
    module: "module02-05-maze-gcell-route",
    kind: "global-routing",
    steps: [
      step("cost", "Edge cost", "Maze adds penalty when usage ≥ capacity.", ["Dijkstra on GCells"], ["Detour allowed"], spread),
      step("l-ov", "L overflow", "L-HV on spread overflows on shared corridors.", [`total=${GOLDENS.spreadLhvTotalOv}`], spread, { routes: spreadRoutes("HV") }),
      step("maze", "Route maze", "Sequential maze routing considers current usage.", ["Six nets"], ["Finite cost"], spread, { routes: routeAllMaze(NETS, terminalsFromPositions(spread)) }),
      step("compare", "Compare totals", "Maze may match or beat L overflow on the toy.", ["Not magic"], ["Still Cap=2"], spread, { routes: routeAllMaze(NETS, terminalsFromPositions(spread)) }),
      step("use", "When to maze", "Use maze when pattern routes saturate edges.", ["Global stage"], ["Rip-up next"], spread),
    ],
  },
  "multipin-tree": {
    title: "Multi-pin tree",
    module: "module03-01-multipin-tree",
    kind: "global-routing",
    steps: [
      step("net4", "Four-pin net", "Net [A,B,C,D] needs a tree, not a single two-pin path.", ["Star demo"], ["4 legs"], spread),
      step("center", "Bbox center", "Star hub at mean GCell of pins (clamped).", ["Steiner lite"], ["Toy only"], spread, { highlight: ["A","B","C","D"] }),
      step("legs", "Four L legs", "Each pin gets an L-route from the hub.", ["4 paths"], ["Edge sharing"], spread, { routes: spreadRoutes("HV"), selectedNet: 4 }),
      step("usage", "Shared edges", "Multi-pin trees reuse edges—overflow adds up.", ["Sum usage"], ["Cap=2"], spread, { routes: spreadRoutes("HV") }),
      step("two", "Two-pin nets", "Short nets E–F stay single L paths.", ["Mix topologies"], ["Six nets total"], spread, { routes: spreadRoutes("HV") }),
    ],
  },
  "edge-overflow": {
    title: "Edge overflow",
    module: "module03-03-edge-overflow",
    kind: "global-routing",
    steps: [
      step("def", "Overflow", "ov(e)=max(0, usage(e)−Cap) per edge.", ["Not tile RUDY"], ["Router metric"], spread, { routes: spreadRoutes("HV") }),
      step("total", "Total overflow", "Sum over edges—primary regression scalar.", [`spread L-HV≈${GOLDENS.spreadLhvTotalOv}`], spread, { routes: spreadRoutes("HV") }),
      step("max", "Max overflow", "Worst edge—catches hotspot corridors.", [`max≈${GOLDENS.spreadLhvMaxOv}`], spread, { routes: spreadRoutes("HV") }),
      step("count", "Overflow count", "How many edges exceed Cap.", ["Triple report"], ["Same as congestion labs"], spread, { routes: spreadRoutes("HV") }),
      step("target", "Hit targets", "Move pins or switch HV/VH/maze to clear thresholds.", ["Check scores learner"], ["No golden mode"], spread),
    ],
  },
  "ripup-reroute": {
    title: "Rip-up reroute",
    module: "module04-01-ripup-reroute",
    kind: "global-routing",
    steps: [
      step("seq", "Sequential L first", "Route L-HV; some edges exceed Cap.", ["Overflow appears"], ["Before rip"], spread, { routes: spreadRoutes("HV") }),
      step("pick", "Pick hot edge", "Find worst overflowing edge; mark nets using it.", ["Shared corridor"], ["Toy rip order"], spread, { routes: spreadRoutes("HV") }),
      step("rip", "Rip nets", "Remove those nets from usage.", ["Subtract paths"], ["Ready to reroute"], spread, { routes: spreadRoutes("HV") }),
      step("maze-r", "Maze reroute", "Rerip'd nets maze-route with updated usage.", ["May improve"], ["GOLDENS.ripupImproves"], spread, { routes: (() => {
        const t=terminalsFromPositions(spread); const r=spreadRoutes("HV"); const u=usageFromRoutes(r);
        return ripupReroute(r,u,EDGE_CAPACITY,t); })() }),
      step("loop", "Iterate", "Real routers loop estimate→route→rip until clean or budget.", ["Detailed route next"], ["learn_routing"], spread),
    ],
  },
  "sequential-global": {
    title: "Sequential global",
    module: "module04-03-sequential-global",
    kind: "global-routing",
    steps: [
      step("order", "Net order", "Route nets 0..5 in order; later nets see earlier usage.", ["Six nets"], ["NETS array"], spread),
      step("l-all", "Pattern pass", "L-HV all nets documents baseline overflow.", [`total≈${GOLDENS.spreadLhvTotalOv}`], spread, { routes: spreadRoutes("HV") }),
      step("maze-all", "Maze pass", "Sequential maze may redistribute usage.", ["Penalties"], ["Compare totals"], spread, { routes: routeAllMaze(NETS, terminalsFromPositions(spread)) }),
      step("clear", "Clear overflow", "Goal: total overflow 0 on the toy after moves or maze.", ["Challenge lab"], ["HPWL optional"], spread, { routes: routeAllMaze(NETS, terminalsFromPositions(spread)) }),
      step("done", "Handoff", "Global routing feeds detailed routing and DRC-clean paths.", ["Edges + caps"], ["Course wrap"], spread),
    ],
  },
};
''',
    )
    print("Wrote global-routing-algos.js")


def patch_walkthrough() -> None:
    path = WALK / "walkthrough.js"
    text = path.read_text(encoding="utf-8")
    changed = False
    if "GLOBAL_ROUTING_ALGOS" not in text:
        text = text.replace(
            'import { drawCongestion } from "../../assets/congestion-core.js";\n',
            'import { drawCongestion } from "../../assets/congestion-core.js";\n'
            'import { GLOBAL_ROUTING_ALGOS } from "./global-routing-algos.js";\n'
            'import { drawGlobalRoute, usageFromRoutes } from "../../assets/global-routing-core.js";\n',
        )
        text = text.replace(
            "  ...CONGESTION_ALGOS,\n};",
            "  ...CONGESTION_ALGOS,\n  ...GLOBAL_ROUTING_ALGOS,\n};",
        )
        changed = True
    needle = '  } else if (pack.kind === "congestion") {\n    drawCongestion(canvas, {\n      positions: s.positions,\n      heat: s.heat || null,\n      heatMode: s.heatMode || "cong",\n      highlight: s.highlight || [],\n    });\n'
    insert = needle + '''  } else if (pack.kind === "global-routing") {
    const grRoutes = s.routes || [];
    const grUsage = s.usage || (grRoutes.length ? usageFromRoutes(grRoutes) : null);
    drawGlobalRoute(canvas, {
      positions: s.positions,
      usage: grUsage,
      routes: grRoutes,
      highlightPath: s.highlightPath || null,
      selectedNet: s.selectedNet ?? null,
      highlight: s.highlight || [],
    });
'''
    if 'pack.kind === "global-routing"' not in text:
        text = text.replace(needle, insert)
        changed = True
    if changed:
        path.write_text(text, encoding="utf-8", newline="\n")
        print("Patched walkthrough.js")
    else:
        print("walkthrough.js already has global-routing")


def patch_capture() -> None:
    text = CAPTURE.read_text(encoding="utf-8")
    entries = [
        '"routing-graph": ("routing-graph", 5)',
        '"terminal-gcells": ("terminal-gcells", 5)',
        '"pattern-l-route": ("pattern-l-route", 5)',
        '"pattern-z-route": ("pattern-z-route", 5)',
        '"maze-gcell-route": ("maze-gcell-route", 5)',
        '"multipin-tree": ("multipin-tree", 5)',
        '"edge-overflow": ("edge-overflow", 5)',
        '"ripup-reroute": ("ripup-reroute", 5)',
        '"sequential-global": ("sequential-global", 5)',
    ]
    if "routing-graph" not in text:
        block = "    " + ",\n    ".join(entries) + ",\n"
        text = text.replace(
            '    "placement-feedback": ("placement-feedback", 5),\n}',
            '    "placement-feedback": ("placement-feedback", 5),\n' + block + "}",
        )
        CAPTURE.write_text(text, encoding="utf-8", newline="\n")
        print("Patched LAB_TO_ALGO")
    else:
        print("LAB_TO_ALGO already has global-routing")


def patch_tools_index() -> None:
    idx = TOOLS / "index.html"
    if not idx.is_file():
        print("No tools index.html")
        return
    text = idx.read_text(encoding="utf-8")
    if "routing-graph" in text:
        print("tools index already lists global-routing")
        return
    marker = "</main>"
    section = """
    <section class="tool-section" id="global-routing">
      <h2>Global routing</h2>
      <ul class="tool-list">
        <li><a href="routing-graph/">GCell routing graph</a></li>
        <li><a href="terminal-gcells/">Terminal GCell mapping</a></li>
        <li><a href="pattern-l-route/">L-pattern routing</a></li>
        <li><a href="pattern-z-route/">Z vs L routing</a></li>
        <li><a href="maze-gcell-route/">Maze GCell routing</a></li>
        <li><a href="multipin-tree/">Multi-pin Steiner tree</a></li>
        <li><a href="edge-overflow/">Edge overflow metrics</a></li>
        <li><a href="ripup-reroute/">Rip-up and reroute</a></li>
        <li><a href="sequential-global/">Sequential global routing</a></li>
      </ul>
    </section>
"""
    if marker in text:
        text = text.replace(marker, section + "\n" + marker)
        idx.write_text(text, encoding="utf-8", newline="\n")
        print("Patched tools index.html")
    else:
        print("Could not patch tools index (no </main>)")


def main() -> None:
    write_tools()
    write_algos()
    patch_walkthrough()
    patch_capture()
    patch_tools_index()
    print("OK")


if __name__ == "__main__":
    main()
