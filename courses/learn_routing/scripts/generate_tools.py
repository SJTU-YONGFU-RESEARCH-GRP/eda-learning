#!/usr/bin/env python3
"""Generate learn_routing interactive tools + detailed-routing-algos.js + wire walkthrough."""
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
    "routing-grid": {
        "title": "Detailed routing grid",
        "lead": "Twelve-by-eight grid with M1 horizontal and M2 vertical tracks; blockage at (5,2) size 2×2.",
        "js": r'''import {
  GOLDENS, PLACEMENT, GRID_NX, GRID_NY, isBlocked, neighbors4
} from "../../assets/detailed-routing-core.js";
import { createInteractiveDetailedRoutingLab } from "../../assets/interactive-detailed-routing-lab.js";

const root = document.getElementById("lab-root");
createInteractiveDetailedRoutingLab(root, {
  initialPositions: PLACEMENT,
  starterHtml: `<p><strong>Your job:</strong> explore the detailed routing grid (${GRID_NX}×${GRID_NY}).
    M1 routes horizontally; M2 vertically. Blockage covers cells (5–6, 2–3).</p>`,
  extraMetrics(api) {
    const t = api.getTerminals();
    const g = t.A;
    return [`A pin grid: (${g.x},${g.y})`, `neighbors(A): ${neighbors4(g).length}`];
  },
  challenges: [
    { id: "grid-shape", title: "Grid is 12×8", level: "Intro",
      prompt: "Confirm GOLDENS grid dimensions.",
      check: () => GOLDENS.gridNx === 12 && GOLDENS.gridNy === 8 },
    { id: "cap-two", title: "Capacity is 2", level: "Intro",
      prompt: "Each track capacity equals 2.",
      check: (_c, api) => api.getCapacity() === GOLDENS.trackCapacity },
    { id: "blockage", title: "Blockage at (5,2)", level: "Intro",
      prompt: "Cell (5,2) is blocked.",
      check: () => isBlocked(5, 2) },
    { id: "block-interior", title: "Interior blocked", level: "Practice",
      prompt: "Cell (6,3) inside 2×2 blockage is blocked.",
      check: () => isBlocked(6, 3) },
    { id: "free-corner", title: "Corner free", level: "Practice",
      prompt: "Corner (0,0) is not blocked.",
      check: () => !isBlocked(0, 0) },
    { id: "mid-neigh", title: "Mid cell neighbors", level: "Practice",
      prompt: "Grid point (1,1) has at least three neighbors.",
      check: () => neighbors4({ x: 1, y: 1 }).length >= 3 },
    { id: "h-tracks", title: "Horizontal track count", level: "Intro",
      prompt: "GOLDENS documents horizontal track slots.",
      check: () => GOLDENS.hTracks === 88 },
    { id: "v-tracks", title: "Vertical track count", level: "Intro",
      prompt: "GOLDENS documents vertical track slots.",
      check: () => GOLDENS.vTracks === 84 },
  ],
});
''',
    },
    "pin-access": {
        "title": "Pin access on grid",
        "lead": "Map each cell center to a grid pin; blocked pins nudge to nearest free neighbor.",
        "js": r'''import {
  GOLDENS, PLACEMENT, CLUSTER_SEED, pinGrid
} from "../../assets/detailed-routing-core.js";
import { createInteractiveDetailedRoutingLab } from "../../assets/interactive-detailed-routing-lab.js";

const root = document.getElementById("lab-root");
createInteractiveDetailedRoutingLab(root, {
  initialPositions: PLACEMENT,
  starterHtml: `<p><strong>Your job:</strong> on spread starter, A→(1,1) and D→(8,5).
    E/F sit on blockage and nudge to access points.</p>`,
  challenges: [
    { id: "a11", title: "A at (1,1)", level: "Intro",
      prompt: "Spread A pin grid is (1,1).",
      check: (_c, api) => { const g = api.getTerminals().A; return g.x === 1 && g.y === 1; } },
    { id: "d85", title: "D at (8,5)", level: "Intro",
      prompt: "Spread D pin grid is (8,5).",
      check: (_c, api) => { const g = api.getTerminals().D; return g.x === 8 && g.y === 5; } },
    { id: "e-access", title: "E access nudged", level: "Practice",
      prompt: "E terminal is not inside blockage.",
      check: (_c, api) => {
        const g = api.getTerminals().E;
        return !(g.x >= 5 && g.x <= 6 && g.y >= 2 && g.y <= 3); } },
    { id: "move-b", title: "B column ≥6", level: "Practice",
      prompt: "Place B with pin column x ≥ 6.",
      check: (_c, api) => api.getTerminals().B.x >= 6 },
    { id: "c-row", title: "C row j≥3", level: "Practice",
      prompt: "Place C with pin row y ≥ 3.",
      check: (_c, api) => api.getTerminals().C.y >= 3 },
    { id: "all-valid", title: "All on-grid", level: "Challenge",
      prompt: "Every terminal has valid grid coordinates.",
      check: (_c, api) => Object.values(api.getTerminals()).every(g => g.x >= 0 && g.x < 12 && g.y >= 0 && g.y < 8) },
    { id: "golden-a", title: "Golden A pin", level: "Intro",
      prompt: "GOLDENS documents A at (1,1).",
      check: () => GOLDENS.aPin[0] === 1 && GOLDENS.aPin[1] === 1 },
    { id: "pin-round", title: "Pin rounds", level: "Intro",
      prompt: "pinGrid(1.4,1.6) rounds to (1,2).",
      check: () => { const g = pinGrid(1.4, 1.6); return g.x === 1 && g.y === 2; } },
  ],
});
''',
    },
    "lee-maze": {
        "title": "Lee maze routing",
        "lead": "Breadth-first maze detours around the 2×2 blockage on the routing grid.",
        "js": r'''import {
  GOLDENS, PLACEMENT, leeMaze, isBlocked
} from "../../assets/detailed-routing-core.js";
import { createInteractiveDetailedRoutingLab } from "../../assets/interactive-detailed-routing-lab.js";

const root = document.getElementById("lab-root");
const blocked = new Set();
for (let x = 5; x < 7; x++) for (let y = 2; y < 4; y++) blocked.add(`${x},${y}`);

createInteractiveDetailedRoutingLab(root, {
  initialPositions: PLACEMENT,
  starterHtml: `<p><strong>Your job:</strong> Lee maze routes around blockage. Detour (4,1)→(7,1) length ≈ ${GOLDENS.leeDetourLen}.</p>`,
  extraMetrics() {
    const path = leeMaze({ x: 4, y: 1 }, { x: 7, y: 1 }, blocked);
    return [`detour len: ${path ? path.length : 0}`];
  },
  challenges: [
    { id: "detour-len", title: "Detour length", level: "Intro",
      prompt: "Lee (4,1)→(7,1) around blockage has documented length.",
      check: () => {
        const p = leeMaze({ x: 4, y: 1 }, { x: 7, y: 1 }, blocked);
        return p && p.length === GOLDENS.leeDetourLen; } },
    { id: "avoid-block", title: "Avoids blockage", level: "Intro",
      prompt: "Detour path avoids blocked cells.",
      check: () => {
        const p = leeMaze({ x: 4, y: 1 }, { x: 7, y: 1 }, blocked);
        return p && p.every(pt => !isBlocked(pt.x, pt.y)); } },
    { id: "route-lee", title: "Route Lee", level: "Practice",
      prompt: "Click Route Lee on spread starter.",
      setup: (_c, api) => api.routeLee(),
      check: (_c, api) => api.getRoutes().some(r => r.segments?.length) },
    { id: "lee-finite", title: "Lee overflow finite", level: "Practice",
      prompt: "After Lee route, overflow metrics are finite.",
      setup: (_c, api) => api.routeLee(),
      check: (_c, api) => Number.isFinite(api.getOverflow().total) },
    { id: "six-nets", title: "Six nets routed", level: "Practice",
      prompt: "Lee routes all six nets.",
      setup: (_c, api) => api.routeLee(),
      check: (_c, api) => api.getRoutes().filter(r => r.segments?.length).length === 6 },
    { id: "total-le2", title: "Total ≤ 2", level: "Challenge",
      prompt: "Move cells; Lee route with total overflow ≤ 2.",
      check: (_c, api) => api.getRoutes().some(r => r.segments?.length) && api.getOverflow().total <= 2 },
    { id: "zero-lee", title: "Clear overflow", level: "Challenge",
      prompt: "Achieve total overflow 0 with Lee routing.",
      check: (_c, api) => api.getRoutes().some(r => r.segments?.length) && api.getOverflow().total === 0 },
    { id: "same-pin", title: "Same pin trivial", level: "Intro",
      prompt: "Lee from A pin to itself returns one point.",
      check: () => {
        const p = leeMaze({ x: 1, y: 1 }, { x: 1, y: 1 }, blocked);
        return p && p.length === 1; } },
  ],
});
''',
    },
    "astar-route": {
        "title": "A* detailed routing",
        "lead": "A* penalizes saturated tracks; may beat layered L overflow on spread starter.",
        "js": r'''import { GOLDENS, PLACEMENT } from "../../assets/detailed-routing-core.js";
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
''',
    },
    "track-usage": {
        "title": "Track usage heat",
        "lead": "Report total, max, and overflowing-track count from routed usage.",
        "js": r'''import { GOLDENS, PLACEMENT } from "../../assets/detailed-routing-core.js";
import { createInteractiveDetailedRoutingLab } from "../../assets/interactive-detailed-routing-lab.js";

const root = document.getElementById("lab-root");
createInteractiveDetailedRoutingLab(root, {
  initialPositions: PLACEMENT,
  starterHtml: `<p><strong>Your job:</strong> route layered on spread (total ≈ ${GOLDENS.spreadLhvTotalOv}),
    then reduce overflow by moving cells or switching to A*.</p>`,
  challenges: [
    { id: "seed-ov", title: "Spread layered overflow", level: "Intro",
      prompt: "Route layered; total matches golden.",
      setup: (_c, api) => api.routeLayered(),
      check: (_c, api) => Math.abs(api.getOverflow().total - GOLDENS.spreadLhvTotalOv) < 0.01 },
    { id: "triple", title: "Metrics finite", level: "Intro",
      prompt: "total/max/count finite after route.",
      setup: (_c, api) => api.routeLayered(),
      check: (_c, api) => {
        const o = api.getOverflow();
        return Number.isFinite(o.total) && Number.isFinite(o.max) && Number.isFinite(o.count); } },
    { id: "usage-pos", title: "Usage > 0", level: "Practice",
      prompt: "Some track has usage > 0 after route.",
      setup: (_c, api) => api.routeLayered(),
      check: (_c, api) => Object.values(api.getUsage()).some(v => v > 0) },
    { id: "t2", title: "Total ≤ 2", level: "Practice",
      prompt: "Total overflow ≤ 2.",
      check: (_c, api) => api.getRoutes().some(r => r.segments?.length) && api.getOverflow().total <= 2 },
    { id: "m1", title: "Max ≤ 1", level: "Practice",
      prompt: "Max overflow ≤ 1.",
      check: (_c, api) => api.getRoutes().some(r => r.segments?.length) && api.getOverflow().max <= 1 },
    { id: "c1", title: "Count ≤ 1", level: "Practice",
      prompt: "At most one overflowing track.",
      check: (_c, api) => api.getRoutes().some(r => r.segments?.length) && api.getOverflow().count <= 1 },
    { id: "zero", title: "Total = 0", level: "Challenge",
      prompt: "Clear all track overflow.",
      check: (_c, api) => api.getRoutes().some(r => r.segments?.length) && api.getOverflow().total === 0 },
    { id: "cap", title: "Cap = 2", level: "Intro",
      prompt: "Track capacity is 2.",
      check: (_c, api) => api.getCapacity() === 2 },
  ],
});
''',
    },
    "via-assignment": {
        "title": "Via assignment",
        "lead": "Layered L routes use vias at bends to switch M1↔M2.",
        "js": r'''import {
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
''',
    },
    "drc-spacing": {
        "title": "DRC spacing lite",
        "lead": "Lite same-layer spacing check flags parallel tracks one grid apart.",
        "js": r'''import {
  PLACEMENT, drcSpacingLite, lRouteLayers, terminalsFromPositions
} from "../../assets/detailed-routing-core.js";
import { createInteractiveDetailedRoutingLab } from "../../assets/interactive-detailed-routing-lab.js";
import { el } from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let lastDrc = { pass: true };

createInteractiveDetailedRoutingLab(root, {
  initialPositions: PLACEMENT,
  starterHtml: `<p><strong>Your job:</strong> run DRC on your routes. Toy checker flags adjacent parallel M1/M2 segments.</p>`,
  extraActions(_ctx, api) {
    return [el("button", {
      className: "btn btn-secondary", type: "button", text: "Check DRC",
      onClick: () => {
        const segs = api.getRoutes().flatMap(r => r.segments || []);
        lastDrc = drcSpacingLite(segs);
        _ctx.rerender();
      },
    })];
  },
  extraMetrics() {
    return [`DRC: ${lastDrc.pass ? "pass" : "fail"}`];
  },
  challenges: [
    { id: "spread-pass", title: "Spread layered passes", level: "Intro",
      prompt: "Spread A–C layered segments pass lite DRC.",
      check: () => {
        const t = terminalsFromPositions(PLACEMENT);
        return drcSpacingLite(lRouteLayers(t.A, t.C, "HV")).pass; } },
    { id: "violation-demo", title: "Violation demo", level: "Intro",
      prompt: "Parallel M1 rows one apart fail DRC.",
      check: () => !drcSpacingLite([
        { x: 1, y: 2, layer: "M1" }, { x: 2, y: 2, layer: "M1" },
        { x: 1, y: 3, layer: "M1" }, { x: 2, y: 3, layer: "M1" },
      ]).pass },
    { id: "route-first", title: "Route layered", level: "Practice",
      prompt: "Route layered before DRC.",
      setup: (_c, api) => api.routeLayered(),
      check: (_c, api) => api.getRoutes().some(r => r.segments?.length) },
    { id: "drc-btn", title: "Run Check DRC", level: "Practice",
      prompt: "Click Check DRC after routing.",
      setup: (_c, api) => {
        api.routeLayered();
        lastDrc = drcSpacingLite(api.getRoutes().flatMap(r => r.segments || []));
      },
      check: () => lastDrc.pass !== undefined },
    { id: "pass-after", title: "Spread routes pass", level: "Practice",
      prompt: "Spread layered routes pass lite DRC.",
      setup: (_c, api) => {
        api.routeLayered();
        lastDrc = drcSpacingLite(api.getRoutes().flatMap(r => r.segments || []));
      },
      check: () => lastDrc.pass === true },
    { id: "overflow-finite", title: "Overflow finite", level: "Intro",
      prompt: "Overflow finite after route.",
      setup: (_c, api) => api.routeLayered(),
      check: (_c, api) => Number.isFinite(api.getOverflow().total) },
    { id: "move-drc", title: "Re-check after move", level: "Challenge",
      prompt: "Move a cell, route, DRC still runs.",
      check: (_c, api) => {
        api.routeLayered();
        lastDrc = drcSpacingLite(api.getRoutes().flatMap(r => r.segments || []));
        return lastDrc.pass !== undefined; } },
    { id: "m2-check", title: "M2 violation demo", level: "Intro",
      prompt: "Adjacent M2 columns fail spacing.",
      check: () => !drcSpacingLite([
        { x: 2, y: 1, layer: "M2" }, { x: 2, y: 2, layer: "M2" },
        { x: 3, y: 1, layer: "M2" }, { x: 3, y: 2, layer: "M2" },
      ]).pass },
  ],
});
''',
    },
    "ripup-detailed": {
        "title": "Rip-up detailed reroute",
        "lead": "Rip the worst overflowing net and reroute with A*.",
        "js": r'''import { GOLDENS, PLACEMENT } from "../../assets/detailed-routing-core.js";
import { createInteractiveDetailedRoutingLab } from "../../assets/interactive-detailed-routing-lab.js";

const root = document.getElementById("lab-root");
let beforeRip = null;

createInteractiveDetailedRoutingLab(root, {
  initialPositions: PLACEMENT,
  starterHtml: `<p><strong>Your job:</strong> Route layered, note overflow, click Rip-up detailed.
    Golden: rip-up can reduce total on hot tracks.</p>`,
  extraMetrics(api) {
    const lines = [];
    if (beforeRip != null) lines.push(`before rip: ${beforeRip.toFixed(2)}`);
    return lines;
  },
  challenges: [
    { id: "layer-first", title: "Route layered first", level: "Intro",
      prompt: "Route layered before rip-up.",
      setup: (_c, api) => { beforeRip = null; api.routeLayered(); beforeRip = api.getOverflow().total; },
      check: (_c, api) => api.getRoutes().some(r => r.segments?.length) },
    { id: "has-ov", title: "Overflow before rip", level: "Intro",
      prompt: "Spread layered has overflow > 0.",
      setup: (_c, api) => { api.routeLayered(); beforeRip = api.getOverflow().total; },
      check: (_c, api) => api.getOverflow().total > 0 },
    { id: "rip-btn", title: "Run rip-up", level: "Practice",
      prompt: "Click Rip-up detailed.",
      setup: (_c, api) => { api.routeLayered(); beforeRip = api.getOverflow().total; api.ripupDetailed(); },
      check: (_c, api) => api.getRoutes().some(r => r.segments?.length) },
    { id: "not-worse", title: "Rip ≤ before", level: "Practice",
      prompt: "After rip-up, total overflow ≤ before.",
      setup: (_c, api) => {
        api.routeLayered(); beforeRip = api.getOverflow().total; api.ripupDetailed(); },
      check: (_c, api) => api.getOverflow().total <= beforeRip + 0.01 },
    { id: "improve", title: "Rip improves", level: "Challenge",
      prompt: "Rip-up strictly lowers total or clears overflow.",
      setup: (_c, api) => {
        api.routeLayered(); beforeRip = api.getOverflow().total; api.ripupDetailed(); },
      check: (_c, api) => api.getOverflow().total < beforeRip || api.getOverflow().total === 0 },
    { id: "golden", title: "Rip helper ok", level: "Intro",
      prompt: "GOLDENS documents rip-up can improve overflow.",
      check: () => GOLDENS.ripupImproves === true },
    { id: "six-nets", title: "Six nets after rip", level: "Intro",
      prompt: "Still six net routes after rip-up.",
      setup: (_c, api) => { api.routeLayered(); api.ripupDetailed(); },
      check: (_c, api) => api.getRoutes().length === 6 },
    { id: "max-drop", title: "Max ≤ 1 after rip", level: "Challenge",
      prompt: "After rip-up, max overflow ≤ 1.",
      check: (_c, api) => {
        if (!api.getRoutes().some(r => r.segments?.length)) api.routeLayered();
        api.ripupDetailed();
        return api.getOverflow().max <= 1; } },
  ],
});
''',
    },
    "sequential-detailed": {
        "title": "Sequential detailed routing",
        "lead": "Route all six nets in order; clear overflow with layered, Lee, or A*.",
        "js": r'''import { GOLDENS, PLACEMENT, NETS } from "../../assets/detailed-routing-core.js";
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
    dest = WALK / "detailed-routing-algos.js"
    template = Path(__file__).resolve().parent / "_detailed_routing_algos.js"
    if template.is_file():
        write(dest, template.read_text(encoding="utf-8"))
        print("Wrote detailed-routing-algos.js")
        return
    write(dest, (ROOT / "platform" / "tools" / "algorithm-walkthrough" / "detailed-routing-algos.js").read_text(encoding="utf-8"))
    print("Wrote detailed-routing-algos.js (from platform copy)")


def patch_walkthrough() -> None:
    path = WALK / "walkthrough.js"
    text = path.read_text(encoding="utf-8")
    changed = False
    if "DETAILED_ROUTING_ALGOS" not in text:
        text = text.replace(
            'import { drawGlobalRoute, usageFromRoutes } from "../../assets/global-routing-core.js";\n',
            'import { drawGlobalRoute, usageFromRoutes } from "../../assets/global-routing-core.js";\n'
            'import { DETAILED_ROUTING_ALGOS } from "./detailed-routing-algos.js";\n'
            'import { drawDetailedRoute, usageFromDetailedRoutes } from "../../assets/detailed-routing-core.js";\n',
        )
        text = text.replace(
            "  ...GLOBAL_ROUTING_ALGOS,\n};",
            "  ...GLOBAL_ROUTING_ALGOS,\n  ...DETAILED_ROUTING_ALGOS,\n};",
        )
        changed = True
    needle = '  } else if (pack.kind === "global-routing") {\n    const grRoutes = s.routes || [];\n    const grUsage = s.usage || (grRoutes.length ? usageFromRoutes(grRoutes) : null);\n    drawGlobalRoute(canvas, {\n      positions: s.positions,\n      usage: grUsage,\n      routes: grRoutes,\n      highlightPath: s.highlightPath || null,\n      selectedNet: s.selectedNet ?? null,\n      highlight: s.highlight || [],\n    });\n'
    insert = needle + '''  } else if (pack.kind === "detailed-routing") {
    const drRoutes = s.routes || [];
    const drUsage = s.usage || (drRoutes.length ? usageFromDetailedRoutes(drRoutes) : null);
    drawDetailedRoute(canvas, {
      positions: s.positions,
      usage: drUsage,
      routes: drRoutes,
      cap: s.cap ?? undefined,
      highlightPath: s.highlightPath || null,
      selectedNet: s.selectedNet ?? null,
      highlight: s.highlight || [],
    });
'''
    if 'pack.kind === "detailed-routing"' not in text:
        text = text.replace(needle, insert)
        changed = True
    if changed:
        path.write_text(text, encoding="utf-8", newline="\n")
        print("Patched walkthrough.js")
    else:
        print("walkthrough.js already has detailed-routing")


def patch_capture() -> None:
    text = CAPTURE.read_text(encoding="utf-8")
    entries = [
        '"routing-grid": ("routing-grid", 5)',
        '"pin-access": ("pin-access", 5)',
        '"lee-maze": ("lee-maze", 5)',
        '"astar-route": ("astar-route", 5)',
        '"track-usage": ("track-usage", 5)',
        '"via-assignment": ("via-assignment", 5)',
        '"drc-spacing": ("drc-spacing", 5)',
        '"ripup-detailed": ("ripup-detailed", 5)',
        '"sequential-detailed": ("sequential-detailed", 5)',
    ]
    if "routing-grid" not in text or '"pin-access"' not in text:
        block = "    " + ",\n    ".join(entries) + ",\n"
        text = text.replace(
            '    "sequential-global": ("sequential-global", 5),\n}',
            '    "sequential-global": ("sequential-global", 5),\n' + block + "}",
        )
        CAPTURE.write_text(text, encoding="utf-8", newline="\n")
        print("Patched LAB_TO_ALGO")
    else:
        print("LAB_TO_ALGO already has detailed-routing")


def patch_tools_index() -> None:
    idx = TOOLS / "index.html"
    if not idx.is_file():
        print("No tools index.html")
        return
    text = idx.read_text(encoding="utf-8")
    if "detailed-routing" in text:
        print("tools index already lists detailed-routing")
        return
    marker = "</main>"
    section = """
    <section class="tool-section" id="detailed-routing">
      <h2>Detailed routing</h2>
      <ul class="tool-list">
        <li><a href="routing-grid/">Detailed routing grid</a></li>
        <li><a href="pin-access/">Pin access on grid</a></li>
        <li><a href="lee-maze/">Lee maze routing</a></li>
        <li><a href="astar-route/">A* detailed routing</a></li>
        <li><a href="track-usage/">Track usage heat</a></li>
        <li><a href="via-assignment/">Via assignment</a></li>
        <li><a href="drc-spacing/">DRC spacing lite</a></li>
        <li><a href="ripup-detailed/">Rip-up detailed reroute</a></li>
        <li><a href="sequential-detailed/">Sequential detailed routing</a></li>
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
