#!/usr/bin/env python3
"""Generate learn_legalization browser labs under platform/tools/.

NOTE (2nd pass): Tool JS under platform/tools/<lab>/ is now **interactive**
(hand-maintained via interactive-legalization-lab.js). Re-running this script
would overwrite learner-driven labs with the older “Run algorithm” stubs —
prefer editing the tool JS files directly, or rewrite LABS here before regen.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TOOLS = ROOT / "platform" / "tools"

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
    "site-row-model": {
        "title": "Site & row model",
        "lead": "Inspect chip outline, row lines, and site grid on a tiny legalization instance.",
        "js": r'''import {
  WIDTHS,
  SITE_W,
  ROW_H,
  N_ROWS,
  CHIP_W,
  CHIP_H,
  ROW_YS,
  GOLDEN_PLACEMENT,
  GOLDENS,
  clonePositions,
  drawLegalization,
  isLegal,
} from "../../assets/legalization-core.js";
import { createChallengeLab, el, metricsBlock } from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let pos = clonePositions(GOLDEN_PLACEMENT);
let mode = "golden";
let shown = true;

function arm() {
  pos = clonePositions(GOLDEN_PLACEMENT);
  mode = "golden";
  shown = false;
}

function run() {
  pos = clonePositions(GOLDEN_PLACEMENT);
  mode = "golden";
  shown = true;
}

const totalCellWidth = Object.values(WIDTHS).reduce((s, w) => s + w, 0);

createChallengeLab(root, {
  starterHtml: `<p><strong>Starter:</strong> legal golden packing on a
    <code>12×6</code> chip with <code>3</code> rows (row height <strong>2</strong>),
    site pitch <strong>1</strong>, total cell width <strong>10</strong>.</p>`,
  loadStarter() { run(); },
  challenges: [
    { id: "show-golden", title: "Show golden", level: "Intro",
      prompt: "Load starter to draw the golden placement.", hint: "Load starter.",
      setup: arm, check: () => shown && mode === "golden" },
    { id: "chip-w", title: "Chip width 12", level: "Intro",
      prompt: "CHIP_W equals 12.", hint: "Site columns.",
      setup: arm, check: () => CHIP_W === 12 && GOLDENS.chipW === 12 },
    { id: "chip-h", title: "Chip height 6", level: "Intro",
      prompt: "CHIP_H equals 6.", hint: "3 rows × rowH 2.",
      setup: arm, check: () => CHIP_H === 6 && GOLDENS.chipH === 6 },
    { id: "n-rows", title: "Three rows", level: "Practice",
      prompt: "N_ROWS is 3.", hint: "ROW_YS length.",
      setup: arm, check: () => N_ROWS === 3 && GOLDENS.nRows === 3 },
    { id: "site-w", title: "Site width 1", level: "Practice",
      prompt: "SITE_W is 1.", hint: "Site pitch.",
      setup: arm, check: () => SITE_W === 1 && GOLDENS.siteW === 1 },
    { id: "row-h", title: "Row height 2", level: "Practice",
      prompt: "ROW_H is 2.", hint: "Uniform row height.",
      setup: arm, check: () => ROW_H === 2 && GOLDENS.rowH === 2 },
    { id: "row-ys", title: "Row Y coords", level: "Practice",
      prompt: "ROW_YS is [0, 2, 4].", hint: "Bottom y of each row.",
      setup: arm, check: () => ROW_YS.join() === "0,2,4" },
    { id: "total-w", title: "Total cell width 10", level: "Stretch",
      prompt: "Sum of cell widths is 10.", hint: "A–F widths.",
      setup: arm, check: () => totalCellWidth === 10 && GOLDENS.totalCellWidth === 10 },
    { id: "width-a", title: "WIDTHS.A = 2", level: "Stretch",
      prompt: "Cell A width is 2 sites.", hint: "WIDTHS.A.",
      setup: arm, check: () => WIDTHS.A === 2 },
    { id: "width-e", title: "WIDTHS.E = 1", level: "Stretch",
      prompt: "Cell E width is 1 site.", hint: "WIDTHS.E.",
      setup: arm, check: () => WIDTHS.E === 1 },
    { id: "golden-legal", title: "Golden legal", level: "Stretch",
      prompt: "Shown golden placement is legal.", hint: "Load starter.",
      setup: arm, check: () => shown && isLegal(pos) && GOLDENS.goldenLegal },
  ],
  extraActions(ctx) {
    return [
      el("button", { className: "btn btn-secondary", type: "button", text: "Load starter",
        onClick: () => { arm(); ctx.rerender(); } }),
      el("button", { className: "btn btn-primary", type: "button", text: "Run algorithm",
        onClick: () => { run(); ctx.rerender(); } }),
    ];
  },
  renderWorkspace(ctx) {
    drawLegalization(ctx.canvas, { positions: shown ? pos : {} });
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock([
      `mode: ${mode}`,
      `shown: ${shown}`,
      `chip: ${CHIP_W}×${CHIP_H}`,
      `rows: ${N_ROWS} · site ${SITE_W} · rowH ${ROW_H}`,
      `totalCellWidth: ${totalCellWidth}`,
      `legal: ${shown ? isLegal(pos) : "—"}`,
    ]));
  },
});
''',
    },
    "legality-metrics": {
        "title": "Legality metrics",
        "lead": "Toggle overlap vs golden placements and read legality reports.",
        "js": r'''import {
  OVERLAP_PLACEMENT,
  GOLDEN_PLACEMENT,
  GOLDENS,
  clonePositions,
  drawLegalization,
  isLegal,
  legalityReport,
} from "../../assets/legalization-core.js";
import { createChallengeLab, el, metricsBlock } from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let pos = clonePositions(OVERLAP_PLACEMENT);
let mode = "overlap";

function arm() {
  pos = clonePositions(OVERLAP_PLACEMENT);
  mode = "overlap";
}

function run() {
  pos = clonePositions(GOLDEN_PLACEMENT);
  mode = "golden";
}

createChallengeLab(root, {
  starterHtml: `<p><strong>Starter:</strong> illegal overlap seed (A/B/C stacked).
    Golden reference is legal. Toggle views and read <code>legalityReport</code>.</p>`,
  loadStarter() { arm(); },
  challenges: [
    { id: "show-overlap", title: "Show overlap", level: "Intro",
      prompt: "Load starter (overlap seed).", hint: "Load starter.",
      setup: arm, check: () => mode === "overlap" },
    { id: "overlap-illegal", title: "Overlap illegal", level: "Intro",
      prompt: "Overlap placement is not legal.", hint: "Load starter.",
      setup: arm, check: () => mode === "overlap" && !isLegal(pos) && GOLDENS.overlapIllegal },
    { id: "overlap-reason", title: "Overlap reason", level: "Intro",
      prompt: "Overlap report reason includes 'overlap'.", hint: "A/B overlap.",
      setup: arm, check: () => mode === "overlap" && legalityReport(pos).reason.includes("overlap") },
    { id: "show-golden", title: "Show golden", level: "Practice",
      prompt: "Run algorithm (show golden).", hint: "Run algorithm.",
      setup: arm, check: () => mode === "golden" },
    { id: "golden-legal", title: "Golden legal", level: "Practice",
      prompt: "Golden placement is legal.", hint: "Run algorithm.",
      setup: arm, check: () => mode === "golden" && isLegal(pos) && GOLDENS.goldenLegal },
    { id: "golden-ok", title: "Golden reason ok", level: "Practice",
      prompt: "Golden report reason is 'ok'.", hint: "Run algorithm.",
      setup: arm, check: () => mode === "golden" && legalityReport(pos).reason === "ok" },
    { id: "site-aligned", title: "Golden site-aligned", level: "Practice",
      prompt: "Golden has no site-alignment violations.", hint: "Run algorithm.",
      setup: arm, check: () => {
        if (mode !== "golden") return false;
        return !legalityReport(pos).reasons.some((r) => r.includes("site-aligned"));
      } },
    { id: "on-row", title: "Golden on rows", level: "Stretch",
      prompt: "Golden has no off-row violations.", hint: "Run algorithm.",
      setup: arm, check: () => {
        if (mode !== "golden") return false;
        return !legalityReport(pos).reasons.some((r) => r.includes("not on a row"));
      } },
    { id: "overlap-ab", title: "Overlap A/B cited", level: "Stretch",
      prompt: "Overlap reasons include A/B.", hint: "Load starter.",
      setup: arm, check: () => mode === "overlap" && legalityReport(pos).reasons.some((r) => r.includes("A/B")) },
    { id: "differs", title: "Golden differs", level: "Stretch",
      prompt: "Golden A.x differs from overlap A.x.", hint: "Compare views.",
      setup: arm, check: () => mode === "golden" && pos.A.x !== OVERLAP_PLACEMENT.A.x },
  ],
  extraActions(ctx) {
    return [
      el("button", { className: "btn btn-secondary", type: "button", text: "Load starter",
        onClick: () => { arm(); ctx.rerender(); } }),
      el("button", { className: "btn btn-primary", type: "button", text: "Run algorithm",
        onClick: () => { run(); ctx.rerender(); } }),
    ];
  },
  renderWorkspace(ctx) {
    drawLegalization(ctx.canvas, { positions: pos });
    const rep = legalityReport(pos);
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock([
      `mode: ${mode}`,
      `legal: ${rep.legal}`,
      `reason: ${rep.reason}`,
      `violations: ${rep.reasons.length}`,
    ]));
  },
});
''',
    },
    "greedy-snap": {
        "title": "Greedy snap",
        "lead": "Snap float coordinates to nearest site and row — overlap may remain.",
        "js": r'''import {
  CELLS,
  FLOAT_PLACEMENT,
  GOLDENS,
  clonePositions,
  drawLegalization,
  greedySnap,
  isLegal,
  legalityReport,
  near,
} from "../../assets/legalization-core.js";
import { createChallengeLab, el, metricsBlock } from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let origin = clonePositions(FLOAT_PLACEMENT);
let pos = clonePositions(FLOAT_PLACEMENT);
let ran = false;

function arm() {
  origin = clonePositions(FLOAT_PLACEMENT);
  pos = clonePositions(FLOAT_PLACEMENT);
  ran = false;
}

function run() {
  pos = greedySnap(origin);
  ran = true;
}

createChallengeLab(root, {
  starterHtml: `<p><strong>Starter:</strong> sloppy float placement from global place.
    Greedy snap rounds x to sites and y to rows — A/B can still overlap at (4,2).</p>`,
  loadStarter() { arm(); },
  challenges: [
    { id: "run", title: "Run greedy snap", level: "Intro",
      prompt: "Click Run algorithm.", hint: "Run algorithm button.",
      setup: arm, check: () => ran },
    { id: "still-illegal", title: "Still illegal", level: "Intro",
      prompt: "Snapped result is not legal.", hint: "Run first.",
      setup: arm, check: () => ran && !isLegal(pos) && !GOLDENS.floatSnapLegal },
    { id: "a-snap", title: "A snaps to (4,2)", level: "Intro",
      prompt: "A is at x=4, y=2 after snap.", hint: "Run greedy snap.",
      setup: arm, check: () => ran && pos.A.x === 4 && pos.A.y === 2 },
    { id: "b-snap", title: "B snaps to (4,2)", level: "Practice",
      prompt: "B shares A's snapped site (overlap).", hint: "Run greedy snap.",
      setup: arm, check: () => ran && pos.B.x === 4 && pos.B.y === 2 },
    { id: "overlap-ab", title: "Overlap A/B", level: "Practice",
      prompt: "Report cites overlap A/B.", hint: "Run greedy snap.",
      setup: arm, check: () => ran && legalityReport(pos).reason.includes("A/B") },
    { id: "f-snap", title: "F at (10,0)", level: "Practice",
      prompt: "F snaps to x=10, y=0.", hint: "Run greedy snap.",
      setup: arm, check: () => ran && pos.F.x === 10 && pos.F.y === 0 },
    { id: "e-snap", title: "E at (0,4)", level: "Practice",
      prompt: "E snaps to x=0, y=4.", hint: "Run greedy snap.",
      setup: arm, check: () => ran && pos.E.x === 0 && pos.E.y === 4 },
    { id: "float-flag", title: "floatSnapLegal false", level: "Stretch",
      prompt: "GOLDENS.floatSnapLegal is false.", hint: "Reference constant.",
      setup: arm, check: () => GOLDENS.floatSnapLegal === false },
    { id: "disp-finite", title: "Displacement finite", level: "Stretch",
      prompt: "After snap, all cells have integer coords.", hint: "Run greedy snap.",
      setup: arm, check: () => ran && CELLS.every((id) => Number.isInteger(pos[id].x) && Number.isInteger(pos[id].y)) },
    { id: "c-snap", title: "C at (5,2)", level: "Stretch",
      prompt: "C snaps to x=5, y=2.", hint: "Run greedy snap.",
      setup: arm, check: () => ran && pos.C.x === 5 && pos.C.y === 2 },
  ],
  extraActions(ctx) {
    return [
      el("button", { className: "btn btn-secondary", type: "button", text: "Load starter",
        onClick: () => { arm(); ctx.rerender(); } }),
      el("button", { className: "btn btn-primary", type: "button", text: "Run algorithm",
        onClick: () => { run(); ctx.rerender(); } }),
    ];
  },
  renderWorkspace(ctx) {
    drawLegalization(ctx.canvas, { positions: pos });
    const rep = ran ? legalityReport(pos) : { legal: null, reason: "—" };
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock([
      `ran: ${ran}`,
      `legal: ${rep.legal}`,
      `reason: ${rep.reason}`,
      `A: ${ran ? `(${pos.A.x},${pos.A.y})` : "—"}`,
    ]));
  },
});
''',
    },
    "overlap-removal": {
        "title": "Overlap removal",
        "lead": "Snap then left-pack within each row to remove overlaps.",
        "js": r'''import {
  OVERLAP_PLACEMENT,
  GOLDENS,
  clonePositions,
  drawLegalization,
  isLegal,
  overlapRemoval,
  totalDisplacement,
  totalHpwl,
} from "../../assets/legalization-core.js";
import { createChallengeLab, el, metricsBlock } from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let origin = clonePositions(OVERLAP_PLACEMENT);
let pos = clonePositions(OVERLAP_PLACEMENT);
let ran = false;

function arm() {
  origin = clonePositions(OVERLAP_PLACEMENT);
  pos = clonePositions(OVERLAP_PLACEMENT);
  ran = false;
}

function run() {
  pos = overlapRemoval(origin);
  ran = true;
}

createChallengeLab(root, {
  starterHtml: `<p><strong>Starter:</strong> overlap seed on middle row.
    Overlap removal snaps then packs left within rows → legal, disp <strong>6</strong>, HPWL <strong>32</strong>.</p>`,
  loadStarter() { arm(); run(); },
  challenges: [
    { id: "run", title: "Run overlap removal", level: "Intro",
      prompt: "Run algorithm on overlap starter.", hint: "Run algorithm.",
      setup: arm, check: () => ran },
    { id: "legal", title: "Result legal", level: "Intro",
      prompt: "Resulting placement is legal.", hint: "Run first.",
      setup: arm, check: () => ran && isLegal(pos) },
    { id: "disp-6", title: "Displacement 6", level: "Intro",
      prompt: "Total displacement is 6.", hint: "Run first.",
      setup: arm, check: () => ran && totalDisplacement(origin, pos) === GOLDENS.overlapRemovalDisp },
    { id: "hpwl-32", title: "HPWL 32", level: "Practice",
      prompt: "HPWL is 32.", hint: "Run first.",
      setup: arm, check: () => ran && totalHpwl(pos) === GOLDENS.overlapRemovalHpwl },
    { id: "b-at-6", title: "B moves to x=6", level: "Practice",
      prompt: "B ends at x=6 on row y=2.", hint: "Run overlap removal.",
      setup: arm, check: () => ran && pos.B.x === 6 && pos.B.y === 2 },
    { id: "c-at-8", title: "C moves to x=8", level: "Practice",
      prompt: "C ends at x=8 on row y=2.", hint: "Run overlap removal.",
      setup: arm, check: () => ran && pos.C.x === 8 && pos.C.y === 2 },
    { id: "a-stays", title: "A stays at 4", level: "Practice",
      prompt: "A remains at x=4, y=2.", hint: "Run overlap removal.",
      setup: arm, check: () => ran && pos.A.x === 4 && pos.A.y === 2 },
    { id: "d-fixed", title: "D unchanged", level: "Stretch",
      prompt: "D stays at (8,4).", hint: "Run overlap removal.",
      setup: arm, check: () => ran && pos.D.x === 8 && pos.D.y === 4 },
    { id: "golden-disp", title: "Matches GOLDENS disp", level: "Stretch",
      prompt: "Displacement equals GOLDENS.overlapRemovalDisp (6).", hint: "Run first.",
      setup: arm, check: () => ran && totalDisplacement(origin, pos) === 6 },
    { id: "golden-hpwl", title: "Matches GOLDENS hpwl", level: "Stretch",
      prompt: "HPWL equals GOLDENS.overlapRemovalHpwl (32).", hint: "Run first.",
      setup: arm, check: () => ran && totalHpwl(pos) === 32 },
  ],
  extraActions(ctx) {
    return [
      el("button", { className: "btn btn-secondary", type: "button", text: "Load starter",
        onClick: () => { arm(); ctx.rerender(); } }),
      el("button", { className: "btn btn-primary", type: "button", text: "Run algorithm",
        onClick: () => { run(); ctx.rerender(); } }),
    ];
  },
  renderWorkspace(ctx) {
    drawLegalization(ctx.canvas, { positions: pos });
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock([
      `ran: ${ran}`,
      `legal: ${ran ? isLegal(pos) : "—"}`,
      `disp: ${ran ? totalDisplacement(origin, pos) : "—"}`,
      `hpwl: ${ran ? totalHpwl(pos) : "—"}`,
    ]));
  },
});
''',
    },
    "abacus-row-pack": {
        "title": "Abacus row pack",
        "lead": "Abacus-lite legalizer: try rows and pick minimum displacement.",
        "js": r'''import {
  OVERLAP_PLACEMENT,
  GOLDENS,
  clonePositions,
  drawLegalization,
  abacusLegalize,
  isLegal,
  totalDisplacement,
  totalHpwl,
} from "../../assets/legalization-core.js";
import { createChallengeLab, el, metricsBlock } from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let origin = clonePositions(OVERLAP_PLACEMENT);
let pos = clonePositions(OVERLAP_PLACEMENT);
let ran = false;

function arm() {
  origin = clonePositions(OVERLAP_PLACEMENT);
  pos = clonePositions(OVERLAP_PLACEMENT);
  ran = false;
}

function run() {
  pos = abacusLegalize(origin);
  ran = true;
}

createChallengeLab(root, {
  starterHtml: `<p><strong>Starter:</strong> overlap seed. Abacus tries rows per cell →
    legal, disp <strong>4</strong>, HPWL <strong>38</strong> (lower disp than tetris).</p>`,
  loadStarter() { arm(); run(); },
  challenges: [
    { id: "run", title: "Run Abacus", level: "Intro",
      prompt: "Run algorithm on overlap starter.", hint: "Run algorithm.",
      setup: arm, check: () => ran },
    { id: "legal", title: "Result legal", level: "Intro",
      prompt: "Abacus result is legal.", hint: "Run first.",
      setup: arm, check: () => ran && isLegal(pos) && GOLDENS.abacusLegal },
    { id: "disp-4", title: "Displacement 4", level: "Intro",
      prompt: "Total displacement is 4.", hint: "Run first.",
      setup: arm, check: () => ran && totalDisplacement(origin, pos) === GOLDENS.abacusDisp },
    { id: "hpwl-38", title: "HPWL 38", level: "Practice",
      prompt: "HPWL is 38.", hint: "Run first.",
      setup: arm, check: () => ran && totalHpwl(pos) === GOLDENS.abacusHpwl },
    { id: "b-row0", title: "B moves to y=0", level: "Practice",
      prompt: "B ends on bottom row (y=0).", hint: "Run Abacus.",
      setup: arm, check: () => ran && pos.B.y === 0 },
    { id: "c-row2", title: "C moves to y=4", level: "Practice",
      prompt: "C ends on top row (y=4).", hint: "Run Abacus.",
      setup: arm, check: () => ran && pos.C.y === 4 },
    { id: "a-stays", title: "A stays middle", level: "Practice",
      prompt: "A remains at (4,2).", hint: "Run Abacus.",
      setup: arm, check: () => ran && pos.A.x === 4 && pos.A.y === 2 },
    { id: "golden-disp", title: "GOLDENS.abacusDisp", level: "Stretch",
      prompt: "Displacement equals GOLDENS.abacusDisp (4).", hint: "Run first.",
      setup: arm, check: () => ran && totalDisplacement(origin, pos) === GOLDENS.abacusDisp },
    { id: "less-tetris", title: "Disp < tetris", level: "Stretch",
      prompt: "Abacus disp (4) < tetris disp (6).", hint: "Compare GOLDENS.",
      setup: arm, check: () => ran && GOLDENS.abacusDisp < GOLDENS.tetrisDisp },
    { id: "b-at-4", title: "B at x=4", level: "Stretch",
      prompt: "B ends at x=4 on row 0.", hint: "Run Abacus.",
      setup: arm, check: () => ran && pos.B.x === 4 && pos.B.y === 0 },
  ],
  extraActions(ctx) {
    return [
      el("button", { className: "btn btn-secondary", type: "button", text: "Load starter",
        onClick: () => { arm(); ctx.rerender(); } }),
      el("button", { className: "btn btn-primary", type: "button", text: "Run algorithm",
        onClick: () => { run(); ctx.rerender(); } }),
    ];
  },
  renderWorkspace(ctx) {
    drawLegalization(ctx.canvas, { positions: pos });
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock([
      `ran: ${ran}`,
      `legal: ${ran ? isLegal(pos) : "—"}`,
      `disp: ${ran ? totalDisplacement(origin, pos) : "—"}`,
      `hpwl: ${ran ? totalHpwl(pos) : "—"}`,
    ]));
  },
});
''',
    },
    "tetris-row-pack": {
        "title": "Tetris row pack",
        "lead": "Per-row shelf pack after snap — same as overlap removal on this instance.",
        "js": r'''import {
  OVERLAP_PLACEMENT,
  GOLDENS,
  clonePositions,
  drawLegalization,
  tetrisLegalize,
  abacusLegalize,
  isLegal,
  totalDisplacement,
  totalHpwl,
} from "../../assets/legalization-core.js";
import { createChallengeLab, el, metricsBlock } from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let origin = clonePositions(OVERLAP_PLACEMENT);
let pos = clonePositions(OVERLAP_PLACEMENT);
let ran = false;

function arm() {
  origin = clonePositions(OVERLAP_PLACEMENT);
  pos = clonePositions(OVERLAP_PLACEMENT);
  ran = false;
}

function run() {
  pos = tetrisLegalize(origin);
  ran = true;
}

createChallengeLab(root, {
  starterHtml: `<p><strong>Starter:</strong> overlap seed. Tetris snap+pack within rows →
    legal, disp <strong>6</strong>, HPWL <strong>32</strong> (same as overlap removal).</p>`,
  loadStarter() { arm(); run(); },
  challenges: [
    { id: "run", title: "Run Tetris", level: "Intro",
      prompt: "Run algorithm on overlap starter.", hint: "Run algorithm.",
      setup: arm, check: () => ran },
    { id: "legal", title: "Result legal", level: "Intro",
      prompt: "Tetris result is legal.", hint: "Run first.",
      setup: arm, check: () => ran && isLegal(pos) && GOLDENS.tetrisLegal },
    { id: "disp-6", title: "Displacement 6", level: "Intro",
      prompt: "Total displacement is 6.", hint: "Run first.",
      setup: arm, check: () => ran && totalDisplacement(origin, pos) === GOLDENS.tetrisDisp },
    { id: "hpwl-32", title: "HPWL 32", level: "Practice",
      prompt: "HPWL is 32.", hint: "Run first.",
      setup: arm, check: () => ran && totalHpwl(pos) === GOLDENS.tetrisHpwl },
    { id: "b-at-6", title: "B at x=6", level: "Practice",
      prompt: "B ends at x=6, y=2.", hint: "Run Tetris.",
      setup: arm, check: () => ran && pos.B.x === 6 && pos.B.y === 2 },
    { id: "c-at-8", title: "C at x=8", level: "Practice",
      prompt: "C ends at x=8, y=2.", hint: "Run Tetris.",
      setup: arm, check: () => ran && pos.C.x === 8 && pos.C.y === 2 },
    { id: "abacus-less", title: "Abacus disp smaller", level: "Practice",
      prompt: "Abacus displacement (4) < Tetris (6).", hint: "Compare GOLDENS.",
      setup: arm, check: () => GOLDENS.abacusDisp < GOLDENS.tetrisDisp },
    { id: "same-overlap", title: "Matches overlap removal", level: "Stretch",
      prompt: "Tetris disp equals overlapRemovalDisp.", hint: "GOLDENS.",
      setup: arm, check: () => ran && totalDisplacement(origin, pos) === GOLDENS.overlapRemovalDisp },
    { id: "abacus-fn", title: "Abacus disp 4", level: "Stretch",
      prompt: "abacusLegalize on origin has disp 4.", hint: "Function check.",
      setup: arm, check: () => totalDisplacement(origin, abacusLegalize(origin)) === 4 },
    { id: "golden-tetris", title: "GOLDENS.tetrisDisp", level: "Stretch",
      prompt: "Displacement equals GOLDENS.tetrisDisp (6).", hint: "Run first.",
      setup: arm, check: () => ran && totalDisplacement(origin, pos) === GOLDENS.tetrisDisp },
  ],
  extraActions(ctx) {
    return [
      el("button", { className: "btn btn-secondary", type: "button", text: "Load starter",
        onClick: () => { arm(); ctx.rerender(); } }),
      el("button", { className: "btn btn-primary", type: "button", text: "Run algorithm",
        onClick: () => { run(); ctx.rerender(); } }),
    ];
  },
  renderWorkspace(ctx) {
    drawLegalization(ctx.canvas, { positions: pos });
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock([
      `ran: ${ran}`,
      `legal: ${ran ? isLegal(pos) : "—"}`,
      `disp: ${ran ? totalDisplacement(origin, pos) : "—"}`,
      `hpwl: ${ran ? totalHpwl(pos) : "—"}`,
    ]));
  },
});
''',
    },
    "fixed-macros": {
        "title": "Fixed macros",
        "lead": "Legalize with macro D locked at (8,4).",
        "js": r'''import {
  OVERLAP_PLACEMENT,
  FIXED_MACROS,
  GOLDENS,
  clonePositions,
  drawLegalization,
  abacusLegalize,
  isLegal,
  legalityReport,
  totalDisplacement,
  totalHpwl,
} from "../../assets/legalization-core.js";
import { createChallengeLab, el, metricsBlock } from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let origin = clonePositions(OVERLAP_PLACEMENT);
let pos = clonePositions(OVERLAP_PLACEMENT);
let ran = false;

function arm() {
  origin = clonePositions(OVERLAP_PLACEMENT);
  pos = clonePositions(OVERLAP_PLACEMENT);
  ran = false;
}

function run() {
  pos = abacusLegalize(origin, { fixed: FIXED_MACROS });
  ran = true;
}

createChallengeLab(root, {
  starterHtml: `<p><strong>Starter:</strong> overlap seed with macro D fixed at (8,4).
    Abacus respects fixed macros → legal, disp <strong>4</strong>.</p>`,
  loadStarter() { arm(); run(); },
  challenges: [
    { id: "run", title: "Run Abacus+fixed", level: "Intro",
      prompt: "Run algorithm with FIXED_MACROS.", hint: "Run algorithm.",
      setup: arm, check: () => ran },
    { id: "legal", title: "Result legal", level: "Intro",
      prompt: "Result is legal with fixed D.", hint: "Run first.",
      setup: arm, check: () => ran && isLegal(pos, { fixed: FIXED_MACROS }) },
    { id: "d-fixed", title: "D stays at (8,4)", level: "Intro",
      prompt: "D remains at x=8, y=4.", hint: "Run Abacus+fixed.",
      setup: arm, check: () => ran && pos.D.x === 8 && pos.D.y === 4 },
    { id: "disp-4", title: "Displacement 4", level: "Practice",
      prompt: "Total displacement is 4.", hint: "Run first.",
      setup: arm, check: () => ran && totalDisplacement(origin, pos) === GOLDENS.abacusDisp },
    { id: "no-macro-move", title: "No macro violation", level: "Practice",
      prompt: "Report has no 'moved off fixed macro'.", hint: "Run first.",
      setup: arm, check: () => ran && !legalityReport(pos, { fixed: FIXED_MACROS }).reasons.some((r) => r.includes("fixed macro")) },
    { id: "b-row0", title: "B to y=0", level: "Practice",
      prompt: "B moves to bottom row.", hint: "Run Abacus+fixed.",
      setup: arm, check: () => ran && pos.B.y === 0 },
    { id: "c-row2", title: "C to y=4", level: "Practice",
      prompt: "C moves to top row (not into D).", hint: "Run Abacus+fixed.",
      setup: arm, check: () => ran && pos.C.y === 4 && pos.C.x === 4 },
    { id: "fixed-const", title: "FIXED_MACROS.D", level: "Stretch",
      prompt: "FIXED_MACROS.D is (8,4).", hint: "Constant.",
      setup: arm, check: () => FIXED_MACROS.D.x === 8 && FIXED_MACROS.D.y === 4 },
    { id: "hpwl-38", title: "HPWL 38", level: "Stretch",
      prompt: "HPWL is 38.", hint: "Run first.",
      setup: arm, check: () => ran && totalHpwl(pos) === GOLDENS.abacusHpwl },
    { id: "golden-disp", title: "GOLDENS.abacusDisp", level: "Stretch",
      prompt: "Displacement equals GOLDENS.abacusDisp (4).", hint: "Run first.",
      setup: arm, check: () => ran && totalDisplacement(origin, pos) === GOLDENS.abacusDisp },
  ],
  extraActions(ctx) {
    return [
      el("button", { className: "btn btn-secondary", type: "button", text: "Load starter",
        onClick: () => { arm(); ctx.rerender(); } }),
      el("button", { className: "btn btn-primary", type: "button", text: "Run algorithm",
        onClick: () => { run(); ctx.rerender(); } }),
    ];
  },
  renderWorkspace(ctx) {
    drawLegalization(ctx.canvas, { positions: pos, highlight: ran ? ["D"] : [] });
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock([
      `ran: ${ran}`,
      `legal: ${ran ? isLegal(pos, { fixed: FIXED_MACROS }) : "—"}`,
      `disp: ${ran ? totalDisplacement(origin, pos) : "—"}`,
      `hpwl: ${ran ? totalHpwl(pos) : "—"}`,
      `D fixed: (8,4)`,
    ]));
  },
});
''',
    },
    "displacement-hpwl": {
        "title": "Displacement vs HPWL",
        "lead": "Trade displacement against wirelength with cost = HPWL + λ·disp.",
        "js": r'''import {
  OVERLAP_PLACEMENT,
  GOLDENS,
  clonePositions,
  drawLegalization,
  abacusLegalize,
  isLegal,
  legalizeCost,
  totalDisplacement,
  totalHpwl,
} from "../../assets/legalization-core.js";
import { createChallengeLab, el, metricsBlock } from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let origin = clonePositions(OVERLAP_PLACEMENT);
let pos = clonePositions(OVERLAP_PLACEMENT);
let ran = false;
let lambda = 1;

function arm() {
  origin = clonePositions(OVERLAP_PLACEMENT);
  pos = clonePositions(OVERLAP_PLACEMENT);
  ran = false;
  lambda = 1;
}

function run() {
  pos = abacusLegalize(origin);
  ran = true;
}

createChallengeLab(root, {
  starterHtml: `<p><strong>Starter:</strong> overlap seed → Abacus result vs origin.
    Cost λ=1 → <strong>42</strong>; λ=5 → <strong>58</strong>.</p>`,
  loadStarter() { arm(); run(); },
  challenges: [
    { id: "run", title: "Run Abacus", level: "Intro",
      prompt: "Run algorithm to get Abacus result.", hint: "Run algorithm.",
      setup: arm, check: () => ran },
    { id: "disp-4", title: "Displacement 4", level: "Intro",
      prompt: "Displacement vs origin is 4.", hint: "Run first.",
      setup: arm, check: () => ran && totalDisplacement(origin, pos) === GOLDENS.abacusDisp },
    { id: "hpwl-38", title: "HPWL 38", level: "Intro",
      prompt: "HPWL is 38.", hint: "Run first.",
      setup: arm, check: () => ran && totalHpwl(pos) === GOLDENS.abacusHpwl },
    { id: "cost-l1", title: "Cost λ=1 → 42", level: "Practice",
      prompt: "legalizeCost at λ=1 is 42.", hint: "38 + 1×4.",
      setup: arm, check: () => ran && legalizeCost(pos, origin, 1) === GOLDENS.abacusCostLambda1 },
    { id: "cost-l5", title: "Cost λ=5 → 58", level: "Practice",
      prompt: "legalizeCost at λ=5 is 58.", hint: "38 + 5×4.",
      setup: arm, check: () => ran && legalizeCost(pos, origin, 5) === GOLDENS.abacusCostLambda5 },
    { id: "set-l5", title: "Set λ=5", level: "Practice",
      prompt: "Click λ=5 and verify cost 58.", hint: "λ=5 button.",
      setup: arm, check: () => ran && lambda === 5 && legalizeCost(pos, origin, 5) === 58 },
    { id: "legal", title: "Result legal", level: "Practice",
      prompt: "Abacus result is legal.", hint: "Run first.",
      setup: arm, check: () => ran && isLegal(pos) },
    { id: "golden-l1", title: "GOLDENS λ=1", level: "Stretch",
      prompt: "GOLDENS.abacusCostLambda1 is 42.", hint: "Reference.",
      setup: arm, check: () => GOLDENS.abacusCostLambda1 === 42 },
    { id: "golden-l5", title: "GOLDENS λ=5", level: "Stretch",
      prompt: "GOLDENS.abacusCostLambda5 is 58.", hint: "Reference.",
      setup: arm, check: () => GOLDENS.abacusCostLambda5 === 58 },
    { id: "cost-formula", title: "Cost formula", level: "Stretch",
      prompt: "Cost = HPWL + λ·disp.", hint: "λ=1 check.",
      setup: arm, check: () => ran && legalizeCost(pos, origin, 1) === totalHpwl(pos) + totalDisplacement(origin, pos) },
  ],
  extraActions(ctx) {
    return [
      el("button", { className: "btn btn-secondary", type: "button", text: "Load starter",
        onClick: () => { arm(); ctx.rerender(); } }),
      el("button", { className: "btn btn-primary", type: "button", text: "Run algorithm",
        onClick: () => { run(); ctx.rerender(); } }),
      el("button", { className: "btn btn-secondary", type: "button", text: "λ=1",
        onClick: () => { lambda = 1; ctx.rerender(); } }),
      el("button", { className: "btn btn-secondary", type: "button", text: "λ=5",
        onClick: () => { lambda = 5; ctx.rerender(); } }),
    ];
  },
  renderWorkspace(ctx) {
    drawLegalization(ctx.canvas, { positions: pos });
    const cost = ran ? legalizeCost(pos, origin, lambda) : null;
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock([
      `ran: ${ran}`,
      `legal: ${ran ? isLegal(pos) : "—"}`,
      `disp: ${ran ? totalDisplacement(origin, pos) : "—"}`,
      `hpwl: ${ran ? totalHpwl(pos) : "—"}`,
      `λ: ${lambda}`,
      `cost: ${cost ?? "—"}`,
    ]));
  },
});
''',
    },
    "detailed-vs-global": {
        "title": "Detailed vs global",
        "lead": "Compare global (Tetris) vs detailed (Abacus) legalization displacement.",
        "js": r'''import {
  OVERLAP_PLACEMENT,
  GOLDENS,
  clonePositions,
  drawLegalization,
  globalLegalize,
  detailedLegalize,
  isLegal,
  totalDisplacement,
  totalHpwl,
} from "../../assets/legalization-core.js";
import { createChallengeLab, el, metricsBlock } from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let origin = clonePositions(OVERLAP_PLACEMENT);
let globalPos = clonePositions(OVERLAP_PLACEMENT);
let detailedPos = clonePositions(OVERLAP_PLACEMENT);
let mode = "none";
let ranGlobal = false;
let ranDetailed = false;

function arm() {
  origin = clonePositions(OVERLAP_PLACEMENT);
  globalPos = clonePositions(OVERLAP_PLACEMENT);
  detailedPos = clonePositions(OVERLAP_PLACEMENT);
  mode = "none";
  ranGlobal = false;
  ranDetailed = false;
}

function runGlobal() {
  globalPos = globalLegalize(origin);
  mode = "global";
  ranGlobal = true;
}

function runDetailed() {
  detailedPos = detailedLegalize(origin);
  mode = "detailed";
  ranDetailed = true;
}

function pos() {
  if (mode === "global") return globalPos;
  if (mode === "detailed") return detailedPos;
  return origin;
}

createChallengeLab(root, {
  starterHtml: `<p><strong>Starter:</strong> overlap seed. Global (Tetris) disp <strong>6</strong>;
    detailed (Abacus) disp <strong>4</strong> — both legal.</p>`,
  loadStarter() { arm(); },
  challenges: [
    { id: "run-global", title: "Run global", level: "Intro",
      prompt: "Run global legalize (Tetris).", hint: "Run global button.",
      setup: arm, check: () => ranGlobal },
    { id: "global-disp", title: "Global disp 6", level: "Intro",
      prompt: "Global displacement is 6.", hint: "Run global.",
      setup: arm, check: () => ranGlobal && totalDisplacement(origin, globalPos) === GOLDENS.globalDisp },
    { id: "global-legal", title: "Global legal", level: "Intro",
      prompt: "Global result is legal.", hint: "Run global.",
      setup: arm, check: () => ranGlobal && isLegal(globalPos) },
    { id: "run-detailed", title: "Run detailed", level: "Practice",
      prompt: "Run detailed legalize (Abacus).", hint: "Run detailed button.",
      setup: arm, check: () => ranDetailed },
    { id: "detailed-disp", title: "Detailed disp 4", level: "Practice",
      prompt: "Detailed displacement is 4.", hint: "Run detailed.",
      setup: arm, check: () => ranDetailed && totalDisplacement(origin, detailedPos) === GOLDENS.detailedDisp },
    { id: "detailed-legal", title: "Detailed legal", level: "Practice",
      prompt: "Detailed result is legal.", hint: "Run detailed.",
      setup: arm, check: () => ranDetailed && isLegal(detailedPos) },
    { id: "detailed-less", title: "Detailed < global", level: "Practice",
      prompt: "Detailed disp < global disp.", hint: "Run both.",
      setup: arm, check: () => ranGlobal && ranDetailed && GOLDENS.detailedDisp < GOLDENS.globalDisp },
    { id: "global-hpwl", title: "Global HPWL 32", level: "Stretch",
      prompt: "Global HPWL is 32.", hint: "Run global.",
      setup: arm, check: () => ranGlobal && totalHpwl(globalPos) === GOLDENS.tetrisHpwl },
    { id: "detailed-hpwl", title: "Detailed HPWL 38", level: "Stretch",
      prompt: "Detailed HPWL is 38.", hint: "Run detailed.",
      setup: arm, check: () => ranDetailed && totalHpwl(detailedPos) === GOLDENS.abacusHpwl },
    { id: "golden-disp", title: "GOLDENS detailedDisp", level: "Stretch",
      prompt: "GOLDENS.detailedDisp equals GOLDENS.abacusDisp (4).", hint: "Reference.",
      setup: arm, check: () => GOLDENS.detailedDisp === GOLDENS.abacusDisp },
  ],
  extraActions(ctx) {
    return [
      el("button", { className: "btn btn-secondary", type: "button", text: "Load starter",
        onClick: () => { arm(); ctx.rerender(); } }),
      el("button", { className: "btn btn-primary", type: "button", text: "Run global",
        onClick: () => { runGlobal(); ctx.rerender(); } }),
      el("button", { className: "btn btn-primary", type: "button", text: "Run detailed",
        onClick: () => { runDetailed(); ctx.rerender(); } }),
    ];
  },
  renderWorkspace(ctx) {
    const p = pos();
    const ran = mode !== "none";
    drawLegalization(ctx.canvas, { positions: p });
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock([
      `mode: ${mode}`,
      `legal: ${ran ? isLegal(p) : "—"}`,
      `disp: ${ran ? totalDisplacement(origin, p) : "—"}`,
      `hpwl: ${ran ? totalHpwl(p) : "—"}`,
      `globalDisp: ${ranGlobal ? totalDisplacement(origin, globalPos) : "—"}`,
      `detailedDisp: ${ranDetailed ? totalDisplacement(origin, detailedPos) : "—"}`,
    ]));
  },
});
''',
    },
}


def main() -> None:
    for lab, meta in LABS.items():
        d = TOOLS / lab
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(
            HTML.format(title=meta["title"], lead=meta["lead"], lab=lab),
            encoding="utf-8",
        )
        (d / f"{lab}.js").write_text(meta["js"].lstrip() + "\n", encoding="utf-8")
        print("wrote", lab)
    print("done", len(LABS), "labs")


if __name__ == "__main__":
    main()
