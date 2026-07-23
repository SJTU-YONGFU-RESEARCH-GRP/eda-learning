#!/usr/bin/env python3
"""Generate learn_congestion interactive tools + congestion-algos.js + wire walkthrough."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TOOLS = ROOT / "platform" / "tools"
ASSETS = ROOT / "platform" / "assets"
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
    "gcell-grid": {
        "title": "GCell grid model",
        "lead": "Map cell centers onto a 4×2 GCell grid over a 12×8 chip.",
        "js": r'''import {
  CONGESTED_SEED, GOLDENS, PLACEMENT, cellGcell
} from "../../assets/congestion-core.js";
import { createInteractiveCongestionLab } from "../../assets/interactive-congestion-lab.js";

const root = document.getElementById("lab-root");
createInteractiveCongestionLab(root, {
  initialPositions: PLACEMENT,
  revealPositions: CONGESTED_SEED,
  heatMode: "cong",
  starterHtml: `<p><strong>Your job:</strong> click to place cells. Challenges check GCell indices
    of <em>your</em> positions (A→(0,0) on spread starter).</p>`,
  challenges: [
    { id: "a00", title: "A in (0,0)", level: "Intro",
      prompt: "On spread starter, A is in GCell (0,0).",
      hint: "Reset starter; check selected A metrics.",
      check: (_c, api) => { const p=api.getPositions().A; const g=cellGcell(p.x,p.y); return g.i===0&&g.j===0; } },
    { id: "d21", title: "D in (2,1)", level: "Intro",
      prompt: "On spread starter, D is in GCell (2,1).",
      check: (_c, api) => { const p=api.getPositions().D; const g=cellGcell(p.x,p.y); return g.i===2&&g.j===1; } },
    { id: "move-e", title: "Move E to (3,0)", level: "Practice",
      prompt: "Place E so its center GCell is (3,0) (right column, bottom row).",
      hint: "x in [9,12), y in [0,4).",
      check: (_c, api) => { const p=api.getPositions().E; const g=cellGcell(p.x,p.y); return g.i===3&&g.j===0; } },
    { id: "grid-shape", title: "Grid is 4×2", level: "Intro",
      prompt: "Confirm GOLDENS grid shape.",
      check: () => GOLDENS.gcellNx===4 && GOLDENS.gcellNy===2 },
    { id: "b-top", title: "B bottom row", level: "Practice",
      prompt: "Keep B in row j=0 (bottom).",
      check: (_c, api) => cellGcell(api.getPositions().B.x, api.getPositions().B.y).j===0 },
    { id: "c-top", title: "C top row", level: "Practice",
      prompt: "On spread starter C is in j=1.",
      check: (_c, api) => cellGcell(api.getPositions().C.x, api.getPositions().C.y).j===1 },
    { id: "f-mid", title: "F in col 2", level: "Practice",
      prompt: "Place F with i=2.",
      check: (_c, api) => cellGcell(api.getPositions().F.x, api.getPositions().F.y).i===2 },
    { id: "all-valid", title: "All cells on-chip GCells", level: "Challenge",
      prompt: "Every cell reports a valid (i,j).",
      check: (_c, api) => Object.values(api.getPositions()).every(p => {
        const g=cellGcell(p.x,p.y); return g.i>=0&&g.i<4&&g.j>=0&&g.j<2; }) },
  ],
});
''',
    },
    "capacity-demand": {
        "title": "Capacity vs demand",
        "lead": "Compare per-GCell demand to routing capacity and spot oversubscribed tiles.",
        "js": r'''import { CONGESTED_SEED, PLACEMENT } from "../../assets/congestion-core.js";
import { createInteractiveCongestionLab } from "../../assets/interactive-congestion-lab.js";

const root = document.getElementById("lab-root");
createInteractiveCongestionLab(root, {
  initialPositions: CONGESTED_SEED,
  revealPositions: PLACEMENT,
  starterHtml: `<p><strong>Your job:</strong> Cap=2. Oversubscribed tiles have demand&gt;2.
    Spread out until overflow count drops.</p>`,
  challenges: [
    { id: "seed-count", title: "Seed has overflow", level: "Intro",
      prompt: "Congested seed has count≥1 at Cap=2.",
      check: (_c, api) => api.getOverflow().count >= 1 },
    { id: "cap-value", title: "Capacity is 2", level: "Intro",
      prompt: "Lab capacity equals 2.",
      check: (_c, api) => api.getCapacity() === 2 },
    { id: "reduce-count", title: "Overflow count ≤ 2", level: "Practice",
      prompt: "Move cells so overflow count ≤ 2.",
      check: (_c, api) => api.getOverflow().count <= 2 },
    { id: "reduce-total", title: "Total overflow ≤ 8", level: "Practice",
      prompt: "Bring total overflow ≤ 8.",
      check: (_c, api) => api.getOverflow().total <= 8 },
    { id: "some-ok", title: "At least one quiet tile", level: "Practice",
      prompt: "At least one GCell has demand ≤ Cap.",
      check: (_c, api) => {
        const d=api.getDemand(); let ok=false;
        for (const col of d) for (const v of col) if (v<=api.getCapacity()) ok=true;
        return ok; } },
    { id: "spread-better", title: "Total < 20", level: "Challenge",
      prompt: "Total overflow under 20.",
      check: (_c, api) => api.getOverflow().total < 20 },
    { id: "max-bound", title: "Max overflow ≤ 6", level: "Challenge",
      prompt: "Keep max overflow ≤ 6.",
      check: (_c, api) => api.getOverflow().max <= 6 },
    { id: "hpwl-finite", title: "HPWL finite", level: "Intro",
      prompt: "HPWL is a finite number.",
      check: (_c, api) => Number.isFinite(api.getHpwl()) },
  ],
});
''',
    },
    "rudy-estimate": {
        "title": "RUDY congestion estimate",
        "lead": "Estimate routing demand with RUDY on a tiny GCell grid.",
        "js": r'''import { CONGESTED_SEED, GOLDENS, PLACEMENT } from "../../assets/congestion-core.js";
import { createInteractiveCongestionLab } from "../../assets/interactive-congestion-lab.js";

const root = document.getElementById("lab-root");
createInteractiveCongestionLab(root, {
  initialPositions: CONGESTED_SEED,
  revealPositions: PLACEMENT,
  heatMode: "demand",
  starterHtml: `<p><strong>Your job:</strong> RUDY deposits HPWL density into GCells under each net bbox.
    Spread cells to cut overflow. Seed max overflow ≈ ${GOLDENS.congestedRudyMaxOv}.</p>`,
  challenges: [
    { id: "seed-max", title: "Seed max ≥ 4", level: "Intro",
      prompt: "Congested seed RUDY max overflow ≥ 4 at Cap=2.",
      check: (_c, api) => api.getOverflow().max >= 4 },
    { id: "demand-positive", title: "Demand > 0", level: "Intro",
      prompt: "Some GCell has positive demand.",
      check: (_c, api) => api.getDemand().some(col => col.some(v => v>0)) },
    { id: "cut-max", title: "Max overflow ≤ 4", level: "Practice",
      prompt: "Reduce max overflow to ≤ 4.",
      check: (_c, api) => api.getOverflow().max <= 4 },
    { id: "cut-total", title: "Total ≤ 10", level: "Practice",
      prompt: "Total overflow ≤ 10.",
      check: (_c, api) => api.getOverflow().total <= 10 },
    { id: "count-le-3", title: "Count ≤ 3", level: "Practice",
      prompt: "At most 3 overflowing GCells.",
      check: (_c, api) => api.getOverflow().count <= 3 },
    { id: "spread-shape", title: "Not all in one tile", level: "Challenge",
      prompt: "Cells occupy at least 3 distinct GCells.",
      check: (_c, api) => {
        const s=new Set(Object.values(api.getPositions()).map(p=>`${api.cellGcell(p.x,p.y).i},${api.cellGcell(p.x,p.y).j}`));
        return s.size>=3; } },
    { id: "total-lt-seed", title: "Total < 12", level: "Challenge",
      prompt: "Total overflow under 12.",
      check: (_c, api) => api.getOverflow().total < 12 },
    { id: "hpwl-lt-40", title: "HPWL < 40", level: "Challenge",
      prompt: "Keep HPWL under 40 while improving overflow.",
      check: (_c, api) => api.getHpwl() < 40 },
  ],
});
''',
    },
    "probabilistic-demand": {
        "title": "Probabilistic routing demand",
        "lead": "L-shape probabilistic demand versus RUDY on the same placement.",
        "js": r'''import {
  CONGESTED_SEED, PLACEMENT, probabilisticDemand, rudyDemand, overflowMetrics, CAPACITY
} from "../../assets/congestion-core.js";
import { createInteractiveCongestionLab } from "../../assets/interactive-congestion-lab.js";

const root = document.getElementById("lab-root");
createInteractiveCongestionLab(root, {
  initialPositions: CONGESTED_SEED,
  revealPositions: PLACEMENT,
  demandFn: probabilisticDemand,
  starterHtml: `<p><strong>Your job:</strong> this lab scores <em>probabilistic</em> L-shape demand.
    Compare mentally to RUDY (metrics show both).</p>`,
  extraMetrics(api) {
    const r = overflowMetrics(rudyDemand(api.getPositions()), CAPACITY);
    return [`RUDY overflow total: ${r.total.toFixed(2)} (compare)`];
  },
  challenges: [
    { id: "prob-pos", title: "Prob demand > 0", level: "Intro",
      prompt: "Probabilistic demand is positive somewhere.",
      check: (_c, api) => api.getDemand().some(col => col.some(v => v>0)) },
    { id: "seed-hot", title: "Seed overflow > 0", level: "Intro",
      prompt: "Congested seed has probabilistic overflow.",
      check: (_c, api) => api.getOverflow().total > 0 },
    { id: "cut-total", title: "Prob total ≤ 8", level: "Practice",
      prompt: "Probabilistic total overflow ≤ 8.",
      check: (_c, api) => api.getOverflow().total <= 8 },
    { id: "cut-max", title: "Prob max ≤ 6", level: "Practice",
      prompt: "Max overflow ≤ 6.",
      check: (_c, api) => api.getOverflow().max <= 6 },
    { id: "count-le-4", title: "Count ≤ 4", level: "Practice",
      prompt: "Overflow count ≤ 4.",
      check: (_c, api) => api.getOverflow().count <= 4 },
    { id: "disagree", title: "RUDY vs prob differ", level: "Challenge",
      prompt: "On your placement, RUDY total ≠ probabilistic total.",
      check: (_c, api) => {
        const r=overflowMetrics(rudyDemand(api.getPositions()),CAPACITY).total;
        return Math.abs(r - api.getOverflow().total) > 0.01; } },
    { id: "spread-3", title: "≥3 GCells used", level: "Challenge",
      prompt: "Cells in ≥3 GCells.",
      check: (_c, api) => {
        const s=new Set(Object.values(api.getPositions()).map(p=>{const g=api.cellGcell(p.x,p.y);return g.i+','+g.j;}));
        return s.size>=3; } },
    { id: "total-lt-5", title: "Total < 5", level: "Challenge",
      prompt: "Probabilistic total overflow < 5.",
      check: (_c, api) => api.getOverflow().total < 5 },
  ],
});
''',
    },
    "congestion-map": {
        "title": "Congestion heat map",
        "lead": "Paint demand/capacity per GCell and find the hottest tile.",
        "js": r'''import { CONGESTED_SEED, PLACEMENT, hottest } from "../../assets/congestion-core.js";
import { createInteractiveCongestionLab } from "../../assets/interactive-congestion-lab.js";

const root = document.getElementById("lab-root");
createInteractiveCongestionLab(root, {
  initialPositions: CONGESTED_SEED,
  revealPositions: PLACEMENT,
  starterHtml: `<p><strong>Your job:</strong> congestion = demand/capacity. Move cells until the hottest
    GCell is not a center tile — or cool the map below thresholds.</p>`,
  extraMetrics(api) {
    const h = hottest(api.getCongestion());
    return [`hottest: (${h.i},${h.j}) @ ${h.v.toFixed(2)}`];
  },
  challenges: [
    { id: "hot-exists", title: "Hottest defined", level: "Intro",
      prompt: "Hottest congestion ≥ 0.",
      check: (_c, api) => hottest(api.getCongestion()).v >= 0 },
    { id: "seed-hot", title: "Seed cong > 1", level: "Intro",
      prompt: "Some tile congestion > 1 on seed.",
      check: (_c, api) => api.getCongestion().some(col => col.some(v => v>1)) },
    { id: "cool-max", title: "Max cong ≤ 3", level: "Practice",
      prompt: "Hottest ratio ≤ 3.",
      check: (_c, api) => hottest(api.getCongestion()).v <= 3 },
    { id: "cool-2", title: "Max cong ≤ 2.5", level: "Practice",
      prompt: "Hottest ≤ 2.5.",
      check: (_c, api) => hottest(api.getCongestion()).v <= 2.5 },
    { id: "edge-hot", title: "Hottest on edge col", level: "Challenge",
      prompt: "Make hottest GCell have i=0 or i=3.",
      check: (_c, api) => { const h=hottest(api.getCongestion()); return h.i===0||h.i===3; } },
    { id: "ov-count", title: "Cong>1 count ≤ 3", level: "Practice",
      prompt: "At most 3 tiles with cong>1.",
      check: (_c, api) => api.getCongestion().flat().filter(v=>v>1).length <= 3 },
    { id: "total-ov", title: "Overflow total ≤ 6", level: "Challenge",
      prompt: "Overflow total ≤ 6.",
      check: (_c, api) => api.getOverflow().total <= 6 },
    { id: "hpwl", title: "HPWL < 50", level: "Intro",
      prompt: "HPWL under 50.",
      check: (_c, api) => api.getHpwl() < 50 },
  ],
});
''',
    },
    "overflow-metrics": {
        "title": "Overflow metrics",
        "lead": "Report total, max, and congested GCell count from a demand map.",
        "js": r'''import { CONGESTED_SEED, PLACEMENT } from "../../assets/congestion-core.js";
import { createInteractiveCongestionLab } from "../../assets/interactive-congestion-lab.js";

const root = document.getElementById("lab-root");
createInteractiveCongestionLab(root, {
  initialPositions: CONGESTED_SEED,
  revealPositions: PLACEMENT,
  starterHtml: `<p><strong>Your job:</strong> hit overflow targets by moving cells.
    Metrics: total · max · count.</p>`,
  challenges: [
    { id: "seed-pos", title: "Seed total > 0", level: "Intro",
      prompt: "Starter has positive total overflow.",
      check: (_c, api) => api.getOverflow().total > 0 },
    { id: "triple", title: "Metrics finite", level: "Intro",
      prompt: "total/max/count are finite.",
      check: (_c, api) => {
        const o=api.getOverflow();
        return Number.isFinite(o.total)&&Number.isFinite(o.max)&&Number.isFinite(o.count); } },
    { id: "t10", title: "Total ≤ 10", level: "Practice",
      prompt: "Total overflow ≤ 10.",
      check: (_c, api) => api.getOverflow().total <= 10 },
    { id: "t5", title: "Total ≤ 5", level: "Practice",
      prompt: "Total overflow ≤ 5.",
      check: (_c, api) => api.getOverflow().total <= 5 },
    { id: "m4", title: "Max ≤ 4", level: "Practice",
      prompt: "Max overflow ≤ 4.",
      check: (_c, api) => api.getOverflow().max <= 4 },
    { id: "c2", title: "Count ≤ 2", level: "Challenge",
      prompt: "Overflow count ≤ 2.",
      check: (_c, api) => api.getOverflow().count <= 2 },
    { id: "t2", title: "Total ≤ 2", level: "Challenge",
      prompt: "Total overflow ≤ 2.",
      check: (_c, api) => api.getOverflow().total <= 2 },
    { id: "zeroish", title: "Total < 1", level: "Challenge",
      prompt: "Nearly clear: total overflow < 1.",
      check: (_c, api) => api.getOverflow().total < 1 },
  ],
});
''',
    },
    "cell-inflator": {
        "title": "Cell inflation",
        "lead": "Inflate widths for cells sitting in oversubscribed GCells.",
        "js": r'''import {
  CONGESTED_SEED, PLACEMENT, WIDTHS, inflateWidths, congestionMap, rudyDemand, CAPACITY
} from "../../assets/congestion-core.js";
import { createInteractiveCongestionLab } from "../../assets/interactive-congestion-lab.js";
import { el } from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let lastWidths = { ...WIDTHS };

createInteractiveCongestionLab(root, {
  initialPositions: CONGESTED_SEED,
  revealPositions: PLACEMENT,
  starterHtml: `<p><strong>Your job:</strong> click <em>Run inflate</em> then verify some widths grew
    where congestion&gt;1. Moving cells changes which tiles are hot.</p>`,
  extraActions(_ctx, api) {
    return [el("button", { className:"btn btn-secondary", type:"button", text:"Run inflate",
      onClick: () => {
        const cong = congestionMap(rudyDemand(api.getPositions()), CAPACITY);
        lastWidths = inflateWidths(api.getPositions(), WIDTHS, cong, 0.5);
        _ctx.rerender();
      }})];
  },
  extraMetrics() {
    const grown = Object.keys(lastWidths).filter(k => lastWidths[k] > WIDTHS[k] + 1e-6);
    return [`inflated: ${grown.join(",")||"(none)"}`, `A width: ${lastWidths.A.toFixed(2)}`];
  },
  challenges: [
    { id: "run-inflate", title: "Inflate someone", level: "Intro",
      prompt: "After Run inflate on a hot seed, at least one width > base.",
      check: () => Object.keys(WIDTHS).some(k => lastWidths[k] > WIDTHS[k] + 1e-6) },
    { id: "a-or-b", title: "A or B grew", level: "Practice",
      prompt: "A or B width above base after inflate on clustered layout.",
      check: (_c, api) => {
        const cong=congestionMap(rudyDemand(api.getPositions()),CAPACITY);
        const w=inflateWidths(api.getPositions(), WIDTHS, cong, 0.5);
        return w.A>WIDTHS.A+1e-6 || w.B>WIDTHS.B+1e-6; } },
    { id: "cool-no", title: "Quiet cell unchanged", level: "Practice",
      prompt: "If you spread enough that E's tile cong≤1, E width stays base when computed.",
      check: (_c, api) => {
        const cong=congestionMap(rudyDemand(api.getPositions()),CAPACITY);
        const g=api.cellGcell(api.getPositions().E.x, api.getPositions().E.y);
        if (cong[g.i][g.j] > 1) return false;
        const w=inflateWidths(api.getPositions(), WIDTHS, cong, 0.5);
        return Math.abs(w.E - WIDTHS.E) < 1e-6; } },
    { id: "alpha", title: "Scale formula", level: "Intro",
      prompt: "Inflation uses (1+α(c−1)) with α=0.5 when c>1.",
      check: () => true },
    { id: "ov-still", title: "Still track overflow", level: "Practice",
      prompt: "Overflow total is finite after moves.",
      check: (_c, api) => Number.isFinite(api.getOverflow().total) },
    { id: "spread-then", title: "Total ≤ 8", level: "Challenge",
      prompt: "Total overflow ≤ 8 (placement still matters).",
      check: (_c, api) => api.getOverflow().total <= 8 },
    { id: "multi", title: "≥2 inflated when hot", level: "Challenge",
      prompt: "On a hot layout, ≥2 cells inflate.",
      check: (_c, api) => {
        const cong=congestionMap(rudyDemand(api.getPositions()),CAPACITY);
        const w=inflateWidths(api.getPositions(), WIDTHS, cong, 0.5);
        return Object.keys(WIDTHS).filter(k => w[k] > WIDTHS[k]+1e-6).length >= 2; } },
    { id: "base-reset", title: "Base widths known", level: "Intro",
      prompt: "Base A width is 2.",
      check: () => WIDTHS.A === 2 },
  ],
});
''',
    },
    "net-weighting": {
        "title": "Congestion-aware net weighting",
        "lead": "Raise weights for nets whose bbox covers congested GCells.",
        "js": r'''import {
  CONGESTED_SEED, PLACEMENT, netWeightsFromCongestion, congestionMap, rudyDemand, CAPACITY
} from "../../assets/congestion-core.js";
import { createInteractiveCongestionLab } from "../../assets/interactive-congestion-lab.js";

const root = document.getElementById("lab-root");
createInteractiveCongestionLab(root, {
  initialPositions: CONGESTED_SEED,
  revealPositions: PLACEMENT,
  starterHtml: `<p><strong>Your job:</strong> weights = 1 + mean congestion under each net bbox.
    Keep the 4-pin net heavier than E–F on a hot seed.</p>`,
  extraMetrics(api) {
    const w = netWeightsFromCongestion(api.getPositions(), api.getCongestion(), 1);
    return [`weights: ${w.map(x=>x.toFixed(2)).join(", ")}`];
  },
  challenges: [
    { id: "w-len", title: "Six weights", level: "Intro",
      prompt: "There are 6 net weights.",
      check: (_c, api) => netWeightsFromCongestion(api.getPositions(), api.getCongestion(),1).length===6 },
    { id: "w-ge1", title: "All weights ≥ 1", level: "Intro",
      prompt: "Every weight ≥ 1.",
      check: (_c, api) => netWeightsFromCongestion(api.getPositions(), api.getCongestion(),1).every(w=>w>=1) },
    { id: "hot-heavier", title: "Net4 ≥ Net5 on seed", level: "Practice",
      prompt: "On a hot layout, 4-pin net weight ≥ E–F weight.",
      check: (_c, api) => {
        const w=netWeightsFromCongestion(api.getPositions(), api.getCongestion(),1);
        return w[4] >= w[5] - 1e-6; } },
    { id: "seed-boost", title: "Some weight > 1.2", level: "Practice",
      prompt: "At least one weight > 1.2.",
      check: (_c, api) => netWeightsFromCongestion(api.getPositions(), api.getCongestion(),1).some(w=>w>1.2) },
    { id: "cool-lower", title: "Max weight ≤ 4", level: "Practice",
      prompt: "Max weight ≤ 4 after spreading.",
      check: (_c, api) => Math.max(...netWeightsFromCongestion(api.getPositions(), api.getCongestion(),1)) <= 4 },
    { id: "ov", title: "Overflow tracked", level: "Intro",
      prompt: "Overflow total finite.",
      check: (_c, api) => Number.isFinite(api.getOverflow().total) },
    { id: "spread-ov", title: "Total ≤ 10", level: "Challenge",
      prompt: "Total overflow ≤ 10.",
      check: (_c, api) => api.getOverflow().total <= 10 },
    { id: "ef-lighter", title: "E–F not heaviest", level: "Challenge",
      prompt: "E–F (net5) is not strictly heaviest.",
      check: (_c, api) => {
        const w=netWeightsFromCongestion(api.getPositions(), api.getCongestion(),1);
        return w[5] <= Math.max(...w.slice(0,5)) + 1e-6; } },
  ],
});
''',
    },
    "placement-feedback": {
        "title": "Placement feedback loop",
        "lead": "One estimate→push pass to reduce overflow on a tiny instance.",
        "js": r'''import { CONGESTED_SEED, PLACEMENT, placementFeedbackLite, rudyDemand, overflowMetrics, CAPACITY } from "../../assets/congestion-core.js";
import { createInteractiveCongestionLab } from "../../assets/interactive-congestion-lab.js";

const root = document.getElementById("lab-root");
const before = overflowMetrics(rudyDemand(CONGESTED_SEED), CAPACITY).total;

createInteractiveCongestionLab(root, {
  initialPositions: CONGESTED_SEED,
  revealPositions: PLACEMENT,
  starterHtml: `<p><strong>Your job:</strong> click <em>Run feedback</em> (or nudge) until overflow drops
    below the seed total (${before.toFixed(2)}).</p>`,
  challenges: [
    { id: "seed-base", title: "Seed total known", level: "Intro",
      prompt: "Reset starter: total overflow matches seed.",
      check: (_c, api) => Math.abs(api.getOverflow().total - before) < 0.2 },
    { id: "after-lower", title: "Below seed total", level: "Practice",
      prompt: "Total overflow strictly below seed.",
      check: (_c, api) => api.getOverflow().total < before - 0.01 },
    { id: "half", title: "≤ half seed", level: "Practice",
      prompt: "Total overflow ≤ half of seed.",
      check: (_c, api) => api.getOverflow().total <= before * 0.5 },
    { id: "low", title: "Total ≤ 2", level: "Challenge",
      prompt: "Total overflow ≤ 2.",
      check: (_c, api) => api.getOverflow().total <= 2 },
    { id: "count", title: "Count ≤ 2", level: "Practice",
      prompt: "Overflow count ≤ 2.",
      check: (_c, api) => api.getOverflow().count <= 2 },
    { id: "max", title: "Max ≤ 2", level: "Challenge",
      prompt: "Max overflow ≤ 2.",
      check: (_c, api) => api.getOverflow().max <= 2 },
    { id: "spread-cells", title: "≥3 GCells", level: "Challenge",
      prompt: "Cells span ≥3 GCells after feedback.",
      check: (_c, api) => {
        const s=new Set(Object.values(api.getPositions()).map(p=>{const g=api.cellGcell(p.x,p.y);return g.i+','+g.j;}));
        return s.size>=3; } },
    { id: "helper", title: "Feedback helper ok", level: "Intro",
      prompt: "placementFeedbackLite reduces seed overflow.",
      check: () => overflowMetrics(rudyDemand(placementFeedbackLite(CONGESTED_SEED)),CAPACITY).total < before },
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
    # Compact 5-step packs; positions from core constants referenced in captions
    write(
        WALK / "congestion-algos.js",
        r'''import {
  CONGESTED_SEED,
  PLACEMENT,
  rudyDemand,
  congestionMap,
  overflowMetrics,
  CAPACITY,
  placementFeedbackLite,
} from "../../assets/congestion-core.js";

const spread = PLACEMENT;
const seed = CONGESTED_SEED;

function step(id, title, caption, bullets, metrics, positions, extra = {}) {
  return { id, title, caption, bullets, metrics, positions, ...extra };
}

export const CONGESTION_ALGOS = {
  "gcell-grid": {
    title: "GCell grid",
    module: "module01-01-gcell-grid",
    kind: "congestion",
    steps: [
      step("chip", "Chip and GCells", "Twelve by eight chip with a four-by-two GCell overlay. Each tile is three by four.", ["Lower-left origin", "i = floor(x/3)", "j = floor(y/4)"], ["Grid: 4×2", "cellW=3 cellH=4"], spread),
      step("a00", "A lands in (0,0)", "Cell A at (1,1) indexes to GCell column 0, row 0.", ["Clamp to last tile on edges"], ["A → (0,0)"], spread, { highlight: ["A"] }),
      step("d21", "D lands in (2,1)", "D at (8,5) → i=2, j=1 (top row).", ["Top row is j=1"], ["D → (2,1)"], spread, { highlight: ["D"] }),
      step("paint", "Paint all centers", "Every cell maps to exactly one GCell; the grid is the router’s coarse map.", ["Used by every estimator"], ["8 tiles total"], spread),
      step("seed", "Clustered seed", "Congested seed piles cells into center tiles—later labs heat those GCells.", ["Same grid, hotter map"], ["Center columns"], seed),
    ],
  },
  "capacity-demand": {
    title: "Capacity vs demand",
    module: "module01-03-capacity-demand",
    kind: "congestion",
    steps: [
      step("cap", "Capacity budget", "Each GCell has capacity 2.0 on the toy instance.", ["Scalar Cap for goldens"], ["Cap=2"], seed),
      step("demand", "Demand arrives", "Estimators deposit demand into tiles; surplus = demand − Cap.", ["Positive surplus = overflow"], ["Compare per tile"], seed, { heatFrom: "rudy" }),
      step("flag", "Oversubscribed tiles", "Flag every tile with demand > Cap before trusting a heat map.", ["List hot tiles"], ["count ≥ 1 on seed"], seed),
      step("toggle", "Lower Cap", "At Cap=1 more tiles fail—capacity is part of the contract.", ["Document units"], ["Cap is a knob"], seed),
      step("spread", "Spread helps", "Moving cells outward reduces how many tiles exceed Cap.", ["Placement feeds congestion"], ["Toward quieter tiles"], spread),
    ],
  },
  "rudy-estimate": {
    title: "RUDY estimate",
    module: "module02-01-rudy-estimate",
    kind: "congestion",
    steps: [
      step("bbox", "Net bounding box", "RUDY starts from each net’s axis-aligned pin bbox and HPWL.", ["HPWL = width+height"], ["6 nets"], seed),
      step("share", "Uniform share", "Density = HPWL / #overlapping GCells; add to each overlapping tile.", ["At least one tile"], ["Deterministic"], seed),
      step("sum", "Sum over nets", "Demand is the sum across nets—center tiles collect many contributions on a cluster.", ["Matrix 4×2"], ["Seed max ov ≈ 5"], seed),
      step("overflow", "Overflow appears", "ov = max(0, demand−Cap). Seed shows a clear hotspot.", ["total/max/count"], ["Cap=2"], seed),
      step("spread", "Spread cools total pattern", "Long nets paint many tiles; cluster spikes max. Both are useful views.", ["Compare seeds"], ["Use max for hotspots"], spread),
    ],
  },
  "probabilistic-demand": {
    title: "Probabilistic demand",
    module: "module02-03-probabilistic-demand",
    kind: "congestion",
    steps: [
      step("lshape", "L-shape idea", "Two-pin nets route on L-shapes with half probability each bend.", ["H-then-V and V-then-H"], ["Corridors not filled boxes"], seed),
      step("deposit", "Deposit along legs", "Walk GCells on each leg and share demand along the path.", ["Corner may be shared"], ["Document scaling"], seed),
      step("multi", "Multi-pin star", "Star from bbox center to each pin; deposit like two-pin edges.", ["Toy multi-pin"], ["Same Cap"], seed),
      step("compare", "Versus RUDY", "Probabilistic concentrates on corridors; RUDY paints the bbox.", ["Totals may differ"], ["Both teach overflow"], seed),
      step("cool", "Spread again", "Spreading still reduces probabilistic overflow—feedback is placement.", ["Same push ideas"], ["Next: heat map"], spread),
    ],
  },
  "congestion-map": {
    title: "Congestion map",
    module: "module02-05-congestion-map",
    kind: "congestion",
    steps: [
      step("ratio", "Demand / Cap", "Congestion is a ratio per GCell—values above one are oversubscribed.", ["Heat = ratio"], ["Cap=2"], seed),
      step("hot", "Hottest tile", "Argmax over the matrix with fixed scan order for stable goldens.", ["Name (i,j)"], ["Center on seed"], seed),
      step("legend", "Read the colors", "Hotter colors mean higher congestion; use metrics for exact floats.", ["Don’t eyeball only"], ["Regression uses numbers"], seed),
      step("move", "Move the hotspot", "Dragging cells can move which tile is hottest.", ["Learner state"], ["Challenges score positions"], seed),
      step("spread", "Cooler map", "Spread placement lowers peak ratios.", ["Toward routing"], ["Overflow lab next"], spread),
    ],
  },
  "overflow-metrics": {
    title: "Overflow metrics",
    module: "module02-07-overflow-metrics",
    kind: "congestion",
    steps: [
      step("def", "Define overflow", "ov = max(0, demand−Cap) per tile.", ["Never negative"], ["Cap=2"], seed),
      step("total", "Total overflow", "Sum of per-tile overflow—primary regression number.", ["Seed total = 5"], ["Spread total higher but flatter"], seed),
      step("max", "Max overflow", "Worst tile—catches hotspots even when total is moderate.", ["Seed max = 5"], ["Hotspot detector"], seed),
      step("count", "Congested count", "How many tiles overflow—useful for “how widespread”.", ["count on seed = 1"], ["Triple report"], seed),
      step("target", "Hit a target", "Move cells until total/max/count clear challenge thresholds.", ["Check scores positions"], ["No reveal required"], spread),
    ],
  },
  "cell-inflator": {
    title: "Cell inflator",
    module: "module03-01-cell-inflator",
    kind: "congestion",
    steps: [
      step("idea", "Why inflate", "Make cells in hot GCells act larger so the next place pass spreads.", ["Width scale"], ["Coords unchanged here"], seed),
      step("rule", "Scale rule", "If cong>1: w' = w·(1+α(c−1)), α=0.5.", ["Else keep w"], ["Center cells grow"], seed),
      step("run", "Apply once", "Compute congestion from RUDY, then inflate widths once.", ["Don’t double-apply"], ["Reset to base widths"], seed),
      step("quiet", "Quiet tiles", "Cells in tiles with cong≤1 stay at base width.", ["Selective"], ["E may stay 1"], seed),
      step("link", "Link to place", "Widths feed the next placer—estimation alone is not enough.", ["Feedback course arc"], ["Net weights next"], spread),
    ],
  },
  "net-weighting": {
    title: "Net weighting",
    module: "module03-03-net-weighting",
    kind: "congestion",
    steps: [
      step("idea", "Weight hot nets", "Nets through congested GCells get larger weights for weighted place.", ["w=1+β·mean cong"], ["β=1 demo"], seed),
      step("bbox", "Mean under bbox", "Average congestion over GCells under the net bbox—not the whole chip.", ["Local mean"], ["6 nets"], seed),
      step("rank", "4-pin ranks high", "On a cluster, the 4-pin net outranks short E–F.", ["w4 ≥ w5"], ["Timing cousin"], seed),
      step("cool", "Spread lowers weights", "As congestion falls, weights ease back toward 1.", ["Coupled to map"], ["Still report overflow"], spread),
      step("use", "Use in placer", "Weighted HPWL pulls soft from hotspots—pair with inflators.", ["Two knobs"], ["Feedback lab next"], seed),
    ],
  },
  "placement-feedback": {
    title: "Placement feedback",
    module: "module04-01-placement-feedback",
    kind: "congestion",
    steps: [
      step("seed", "Hot starter", "Congested seed starts with total overflow 5 at Cap=2.", ["RUDY demand"], ["Need a loop"], seed),
      step("estimate", "Estimate", "Run RUDY → congestion → overflow per tile.", ["Same estimators"], ["Matrix in hand"], seed),
      step("push", "Push outward", "Cells in overflowing tiles step toward the quietest neighbor GCell.", ["Clamp to chip"], ["Toy one-pass"], seed),
      step("after", "Overflow drops", "After one feedback pass, total overflow falls (often to ~0 on this toy).", ["Remeasure demand"], ["Assert after < before"], placementFeedbackLite(seed)),
      step("next", "Toward routing", "Real flows iterate with global routing; next course deepens GCell edges.", ["learn_global_routing"], ["CTS also next"], spread),
    ],
  },
};
''',
    )
    print("Wrote congestion-algos.js")


def patch_walkthrough() -> None:
    path = WALK / "walkthrough.js"
    text = path.read_text(encoding="utf-8")
    if "CONGESTION_ALGOS" not in text:
        text = text.replace(
            'import { LEGALIZATION_ALGOS } from "./legalization-algos.js";\n',
            'import { LEGALIZATION_ALGOS } from "./legalization-algos.js";\n'
            'import { CONGESTION_ALGOS } from "./congestion-algos.js";\n'
            'import { drawCongestion } from "../../assets/congestion-core.js";\n',
        )
        text = text.replace(
            "  ...LEGALIZATION_ALGOS,\n};",
            "  ...LEGALIZATION_ALGOS,\n  ...CONGESTION_ALGOS,\n};",
        )
        needle = '  } else if (pack.kind === "legalization") {\n    drawLegalization(canvas, {\n      positions: s.positions || OVERLAP_PLACEMENT,\n      highlight: s.highlight || [],\n    });\n'
        insert = needle + '''  } else if (pack.kind === "congestion") {
    drawCongestion(canvas, {
      positions: s.positions || PLACEMENT,
      heat: s.heat || null,
      heatMode: s.heatMode || "cong",
      highlight: s.highlight || [],
    });
'''
        # Need PLACEMENT import - use CONGESTED from congestion via positions only; drawCongestion defaults
        insert = needle + '''  } else if (pack.kind === "congestion") {
    drawCongestion(canvas, {
      positions: s.positions,
      heat: s.heat || null,
      heatMode: s.heatMode || "cong",
      highlight: s.highlight || [],
    });
'''
        if 'pack.kind === "congestion"' not in text:
            text = text.replace(needle, insert)
        path.write_text(text, encoding="utf-8", newline="\n")
        print("Patched walkthrough.js")
    else:
        print("walkthrough.js already has congestion")


def patch_capture() -> None:
    text = CAPTURE.read_text(encoding="utf-8")
    block = """    "detailed-vs-global": ("detailed-vs-global", 5),
    "gcell-grid": ("gcell-grid", 5),
    "capacity-demand": ("capacity-demand", 5),
    "rudy-estimate": ("rudy-estimate", 5),
    "probabilistic-demand": ("probabilistic-demand", 5),
    "congestion-map": ("congestion-map", 5),
    "overflow-metrics": ("overflow-metrics", 5),
    "cell-inflator": ("cell-inflator", 5),
    "net-weighting": ("net-weighting", 5),
    "placement-feedback": ("placement-feedback", 5),
}"""
    if "gcell-grid" not in text:
        text = text.replace(
            '    "detailed-vs-global": ("detailed-vs-global", 5),\n}',
            block,
        )
        CAPTURE.write_text(text, encoding="utf-8", newline="\n")
        print("Patched LAB_TO_ALGO")
    else:
        print("LAB_TO_ALGO already has congestion")


def patch_tools_index() -> None:
    idx = TOOLS / "index.html"
    if not idx.is_file():
        print("No tools index.html")
        return
    text = idx.read_text(encoding="utf-8")
    if "gcell-grid" in text:
        print("tools index already lists congestion")
        return
    # Best-effort: append a section before </main> if present
    marker = "</main>"
    section = """
    <section class="tool-section">
      <h2>Congestion</h2>
      <ul class="tool-list">
        <li><a href="gcell-grid/">GCell grid</a></li>
        <li><a href="capacity-demand/">Capacity vs demand</a></li>
        <li><a href="rudy-estimate/">RUDY estimate</a></li>
        <li><a href="probabilistic-demand/">Probabilistic demand</a></li>
        <li><a href="congestion-map/">Congestion map</a></li>
        <li><a href="overflow-metrics/">Overflow metrics</a></li>
        <li><a href="cell-inflator/">Cell inflator</a></li>
        <li><a href="net-weighting/">Net weighting</a></li>
        <li><a href="placement-feedback/">Placement feedback</a></li>
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
