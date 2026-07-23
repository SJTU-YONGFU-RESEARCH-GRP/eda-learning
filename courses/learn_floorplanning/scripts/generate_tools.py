#!/usr/bin/env python3
"""Generate learn_floorplanning browser labs under platform/tools/."""
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
    "fixed-outline": {
        "title": "Fixed outline",
        "lead": "Check legality of packings inside a fixed 10×8 outline.",
        "js": r'''import {
  BAD_PACK,
  GOLDEN_PACK,
  OVERLAP_PACK,
  OUTLINE,
  clonePack,
  deadspace,
  density,
  drawFloorplan,
  isLegalPacking,
  legalityReport,
} from "../../assets/floorplanning-core.js";
import {
  createChallengeLab,
  el,
  metricsBlock,
} from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let pack = clonePack(BAD_PACK);
let mode = "bad";

function arm() {
  pack = clonePack(BAD_PACK);
  mode = "none";
}

createChallengeLab(root, {
  starterHtml: `
    <p><strong>Starter (reference):</strong> bad pack overflows (E past right edge).
    Golden pack is legal inside <code>10×8</code>. Deadspace for module areas is
    <strong>57</strong> (density <strong>0.2875</strong>) whenever packing is legal.</p>
  `,
  loadStarter() {
    pack = clonePack(BAD_PACK);
    mode = "bad";
  },
  challenges: [
    { id: "bad-illegal", title: "Bad pack illegal", level: "Intro",
      prompt: "Show bad pack; legality must fail.", hint: "Click Show bad.",
      setup: arm, check: () => mode === "bad" && !isLegalPacking(pack) },
    { id: "bad-reason", title: "Bad reason: E outside", level: "Intro",
      prompt: "Bad pack report mentions E outside outline.",
      hint: "E at x=9 with w=2 overflows.",
      setup: arm, check: () => mode === "bad" && legalityReport(pack).reason.includes("E") },
    { id: "golden-legal", title: "Golden legal", level: "Intro",
      prompt: "Show golden; packing must be legal.", hint: "Click Show golden.",
      setup: arm, check: () => mode === "golden" && isLegalPacking(pack) },
    { id: "golden-ok", title: "Golden reason ok", level: "Practice",
      prompt: "Golden report reason is ok.", hint: "Show golden first.",
      setup: arm, check: () => mode === "golden" && legalityReport(pack).reason === "ok" },
    { id: "overlap-illegal", title: "Overlap illegal", level: "Practice",
      prompt: "Show overlap pack; must be illegal.", hint: "Click Show overlap.",
      setup: arm, check: () => mode === "overlap" && !isLegalPacking(pack) },
    { id: "outline-10x8", title: "Outline 10×8", level: "Practice",
      prompt: "Outline width is 10 and height is 8.", hint: "Always true for this lab.",
      setup: arm, check: () => OUTLINE.w === 10 && OUTLINE.h === 8 },
    { id: "deadspace-57", title: "Deadspace 57", level: "Practice",
      prompt: "Module deadspace vs outline is 57 (independent of placement).",
      hint: "80 − 23 = 57.", setup: arm, check: () => deadspace() === 57 },
    { id: "density-2875", title: "Density 0.2875", level: "Stretch",
      prompt: "Density equals 23/80 = 0.2875.", hint: "moduleAreaSum / outlineArea.",
      setup: arm, check: () => Math.abs(density() - 0.2875) < 1e-9 },
    { id: "golden-not-bad", title: "Golden differs from bad", level: "Stretch",
      prompt: "With golden shown, packing is legal while bad is not.",
      hint: "Show golden.", setup: arm,
      check: () => mode === "golden" && isLegalPacking(pack) && !isLegalPacking(BAD_PACK) },
    { id: "touching-ok", title: "Edge touching ok", level: "Stretch",
      prompt: "Golden stays legal (edge-touching allowed, interior overlap not).",
      hint: "Show golden; A touches D along an edge.", setup: arm,
      check: () => mode === "golden" && isLegalPacking(pack) },
  ],
  extraActions(ctx) {
    return [
      el("button", { className: "btn btn-secondary", type: "button", text: "Show bad",
        onClick: () => { pack = clonePack(BAD_PACK); mode = "bad"; ctx.rerender(); } }),
      el("button", { className: "btn btn-primary", type: "button", text: "Show golden",
        onClick: () => { pack = clonePack(GOLDEN_PACK); mode = "golden"; ctx.rerender(); } }),
      el("button", { className: "btn btn-secondary", type: "button", text: "Show overlap",
        onClick: () => { pack = clonePack(OVERLAP_PACK); mode = "overlap"; ctx.rerender(); } }),
    ];
  },
  renderWorkspace(ctx) {
    drawFloorplan(ctx.canvas, { pack: mode === "none" ? {} : pack });
    const rep = mode === "none" ? { legal: null, reason: "none" } : legalityReport(pack);
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock([
      `view: ${mode}`,
      `legal: ${rep.legal}`,
      `reason: ${rep.reason}`,
      `outline: ${OUTLINE.w}×${OUTLINE.h}`,
      `deadspace: ${deadspace()}`,
      `density: ${density().toFixed(4)}`,
    ]));
  },
});
''',
    },
    "area-deadspace": {
        "title": "Area & deadspace",
        "lead": "Compute packing density and whitespace against a fixed outline.",
        "js": r'''import {
  GOLDEN_PACK,
  OUTLINE,
  clonePack,
  deadspace,
  density,
  drawFloorplan,
  isLegalPacking,
  moduleAreaSum,
  outlineArea,
} from "../../assets/floorplanning-core.js";
import { createChallengeLab, el, metricsBlock } from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let pack = clonePack(GOLDEN_PACK);
let shown = false;

function arm() { pack = clonePack(GOLDEN_PACK); shown = false; }

createChallengeLab(root, {
  starterHtml: `<p><strong>Starter:</strong> golden legal packing. Module area sum
    <strong>23</strong>, outline <strong>80</strong>, deadspace <strong>57</strong>,
    density <strong>0.2875</strong>.</p>`,
  loadStarter() { pack = clonePack(GOLDEN_PACK); shown = true; },
  challenges: [
    { id: "show-golden", title: "Show golden", level: "Intro",
      prompt: "Load/show golden packing.", hint: "Load starter or Show golden.",
      setup: arm, check: () => shown && isLegalPacking(pack) },
    { id: "area-23", title: "Module area 23", level: "Intro",
      prompt: "Sum of module areas is 23.", hint: "6+6+4+3+4.",
      setup: arm, check: () => moduleAreaSum() === 23 },
    { id: "outline-80", title: "Outline area 80", level: "Intro",
      prompt: "Outline area is 80.", hint: "10×8.",
      setup: arm, check: () => outlineArea() === 80 },
    { id: "ds-57", title: "Deadspace 57", level: "Practice",
      prompt: "Deadspace equals 57.", hint: "80−23.",
      setup: arm, check: () => deadspace() === 57 },
    { id: "den", title: "Density 0.2875", level: "Practice",
      prompt: "Density is 0.2875.", hint: "23/80.",
      setup: arm, check: () => Math.abs(density() - 0.2875) < 1e-9 },
    { id: "legal", title: "Golden legal", level: "Practice",
      prompt: "Shown golden packing is legal.", hint: "Show golden.",
      setup: arm, check: () => shown && isLegalPacking(pack) },
    { id: "ds-formula", title: "Deadspace formula", level: "Practice",
      prompt: "deadspace === outlineArea − moduleAreaSum.",
      hint: "Always true here.", setup: arm,
      check: () => deadspace() === outlineArea() - moduleAreaSum() },
    { id: "outline-dims", title: "Outline dims", level: "Stretch",
      prompt: "Outline is 10 by 8.", hint: "OUTLINE.",
      setup: arm, check: () => OUTLINE.w === 10 && OUTLINE.h === 8 },
    { id: "density-lt-1", title: "Density < 1", level: "Stretch",
      prompt: "Density is strictly less than 1.", hint: "Whitespace remains.",
      setup: arm, check: () => density() < 1 },
    { id: "whitespace-pct", title: "Whitespace 71.25%", level: "Stretch",
      prompt: "Deadspace / outline = 0.7125.", hint: "57/80.",
      setup: arm, check: () => Math.abs(deadspace() / outlineArea() - 0.7125) < 1e-9 },
  ],
  extraActions(ctx) {
    return [
      el("button", { className: "btn btn-primary", type: "button", text: "Show golden",
        onClick: () => { pack = clonePack(GOLDEN_PACK); shown = true; ctx.rerender(); } }),
    ];
  },
  renderWorkspace(ctx) {
    drawFloorplan(ctx.canvas, { pack: shown ? pack : {} });
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock([
      `shown: ${shown}`,
      `moduleArea: ${moduleAreaSum()}`,
      `outlineArea: ${outlineArea()}`,
      `deadspace: ${deadspace()}`,
      `density: ${density().toFixed(4)}`,
      `legal: ${shown ? isLegalPacking(pack) : "—"}`,
    ]));
  },
});
''',
    },
    "slicing-floorplan": {
        "title": "Slicing floorplan",
        "lead": "Evaluate a polish expression into a slicing packing.",
        "js": r'''import {
  GOLDEN_POLISH,
  OUTLINE,
  drawFloorplan,
  evalPolish,
  isLegalPacking,
} from "../../assets/floorplanning-core.js";
import { createChallengeLab, el, metricsBlock } from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let pack = {};
let bb = { w: 0, h: 0 };
let ran = false;

function arm() { pack = {}; bb = { w: 0, h: 0 }; ran = false; }
function run() {
  const r = evalPolish(GOLDEN_POLISH);
  pack = r.pack; bb = { w: r.w, h: r.h }; ran = true;
}

createChallengeLab(root, {
  starterHtml: `<p><strong>Starter polish:</strong>
    <code>A D H B V C V E V</code> → bounding box width 9, height 3 (fits in 10×8).</p>`,
  loadStarter() { run(); },
  challenges: [
    { id: "run", title: "Evaluate polish", level: "Intro",
      prompt: "Run Evaluate polish.", hint: "Click the button.",
      setup: arm, check: () => ran },
    { id: "bb-w", title: "BB width 9", level: "Intro",
      prompt: "Bounding width is 9.", hint: "Evaluate first.",
      setup: arm, check: () => ran && bb.w === 9 },
    { id: "bb-h", title: "BB height 3", level: "Intro",
      prompt: "Bounding height is 3.", hint: "A+D stacked is height 3.",
      setup: arm, check: () => ran && bb.h === 3 },
    { id: "legal", title: "Fits outline", level: "Practice",
      prompt: "Resulting packing is legal in 10×8.", hint: "Evaluate.",
      setup: arm, check: () => ran && isLegalPacking(pack) },
    { id: "has-A", title: "Places A", level: "Practice",
      prompt: "Pack includes A at origin-ish.", hint: "A is first leaf.",
      setup: arm, check: () => ran && pack.A && pack.A.x === 0 && pack.A.y === 0 },
    { id: "has-E", title: "Places E", level: "Practice",
      prompt: "Pack includes E.", hint: "Last V attaches E.",
      setup: arm, check: () => ran && !!pack.E },
    { id: "five", title: "Five modules", level: "Practice",
      prompt: "Exactly five modules placed.", hint: "A–E.",
      setup: arm, check: () => ran && Object.keys(pack).length === 5 },
    { id: "polish-len", title: "Polish length 9", level: "Stretch",
      prompt: "Golden polish token count is 9.", hint: "5 ops + 4 operators? count tokens.",
      setup: arm, check: () => GOLDEN_POLISH.length === 9 },
    { id: "fits-w", title: "BB ≤ outline W", level: "Stretch",
      prompt: "Bounding width ≤ outline width.", hint: "9 ≤ 10.",
      setup: arm, check: () => ran && bb.w <= OUTLINE.w },
    { id: "fits-h", title: "BB ≤ outline H", level: "Stretch",
      prompt: "Bounding height ≤ outline height.", hint: "3 ≤ 8.",
      setup: arm, check: () => ran && bb.h <= OUTLINE.h },
  ],
  extraActions(ctx) {
    return [
      el("button", { className: "btn btn-primary", type: "button", text: "Evaluate polish",
        onClick: () => { run(); ctx.rerender(); } }),
    ];
  },
  renderWorkspace(ctx) {
    drawFloorplan(ctx.canvas, { pack });
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock([
      `ran: ${ran}`,
      `polish: ${GOLDEN_POLISH.join(" ")}`,
      `bb: ${bb.w}×${bb.h}`,
      `legal: ${ran ? isLegalPacking(pack) : "—"}`,
    ]));
  },
});
''',
    },
    "bstar-tree": {
        "title": "B*-tree",
        "lead": "Pack modules from a B*-tree (right-of / above).",
        "js": r'''import {
  GOLDEN_BSTAR,
  drawFloorplan,
  isLegalPacking,
  packBstar,
} from "../../assets/floorplanning-core.js";
import { createChallengeLab, el, metricsBlock } from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let pack = {};
let ran = false;
function arm() { pack = {}; ran = false; }
function run() { pack = packBstar(GOLDEN_BSTAR); ran = true; }

createChallengeLab(root, {
  starterHtml: `<p><strong>Starter B*:</strong> A root; left chain B→C→E (right-of);
    right child D (above A). Pack with contour placement.</p>`,
  loadStarter() { run(); },
  challenges: [
    { id: "run", title: "Pack B*", level: "Intro", prompt: "Run Pack B*-tree.",
      hint: "Click the button.", setup: arm, check: () => ran },
    { id: "legal", title: "Legal packing", level: "Intro",
      prompt: "Result is legal.", hint: "Pack first.",
      setup: arm, check: () => ran && isLegalPacking(pack) },
    { id: "A-origin", title: "A at origin", level: "Intro",
      prompt: "A is at (0,0).", hint: "Root placed first.",
      setup: arm, check: () => ran && pack.A.x === 0 && pack.A.y === 0 },
    { id: "B-right", title: "B right of A", level: "Practice",
      prompt: "B.x equals A.x + A.w.", hint: "Left child = right-of.",
      setup: arm, check: () => ran && pack.B.x === pack.A.x + pack.A.w },
    { id: "D-above", title: "D above A", level: "Practice",
      prompt: "D.y >= A.h (above A contour).", hint: "Right child = above.",
      setup: arm, check: () => ran && pack.D.y >= pack.A.h },
    { id: "five", title: "Five modules", level: "Practice",
      prompt: "Five modules placed.", hint: "A–E.",
      setup: arm, check: () => ran && Object.keys(pack).length === 5 },
    { id: "C-exists", title: "C placed", level: "Practice",
      prompt: "C is in the pack.", hint: "In left chain.",
      setup: arm, check: () => ran && !!pack.C },
    { id: "E-exists", title: "E placed", level: "Stretch",
      prompt: "E is in the pack.", hint: "End of left chain.",
      setup: arm, check: () => ran && !!pack.E },
    { id: "no-neg", title: "Non-negative coords", level: "Stretch",
      prompt: "All x,y ≥ 0.", hint: "Contour pack.",
      setup: arm, check: () => ran && Object.values(pack).every((r) => r.x >= 0 && r.y >= 0) },
    { id: "root-A", title: "Root is A", level: "Stretch",
      prompt: "Golden tree root id is A.", hint: "GOLDEN_BSTAR.id.",
      setup: arm, check: () => GOLDEN_BSTAR.id === "A" },
  ],
  extraActions(ctx) {
    return [
      el("button", { className: "btn btn-primary", type: "button", text: "Pack B*-tree",
        onClick: () => { run(); ctx.rerender(); } }),
    ];
  },
  renderWorkspace(ctx) {
    drawFloorplan(ctx.canvas, { pack });
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock([
      `ran: ${ran}`,
      `legal: ${ran ? isLegalPacking(pack) : "—"}`,
      `A: ${ran ? `(${pack.A.x},${pack.A.y})` : "—"}`,
      `modules: ${Object.keys(pack).join(",") || "—"}`,
    ]));
  },
});
''',
    },
    "sequence-pair": {
        "title": "Sequence pair",
        "lead": "Pack from (+, −) sequence-pair permutations.",
        "js": r'''import {
  GOLDEN_SP,
  drawFloorplan,
  isLegalPacking,
  packSequencePair,
} from "../../assets/floorplanning-core.js";
import { createChallengeLab, el, metricsBlock } from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let pack = {};
let ran = false;
function arm() { pack = {}; ran = false; }
function run() {
  pack = packSequencePair(GOLDEN_SP.pos, GOLDEN_SP.neg);
  ran = true;
}

createChallengeLab(root, {
  starterHtml: `<p><strong>Starter SP:</strong> pos =
    <code>${"A B C E D"}</code>, neg = <code>${"D A B C E"}</code>.</p>`,
  loadStarter() { run(); },
  challenges: [
    { id: "run", title: "Pack SP", level: "Intro", prompt: "Run Pack sequence pair.",
      hint: "Click the button.", setup: arm, check: () => ran },
    { id: "legal", title: "Legal", level: "Intro",
      prompt: "Packing is legal.", hint: "Pack first.",
      setup: arm, check: () => ran && isLegalPacking(pack) },
    { id: "five", title: "Five modules", level: "Intro",
      prompt: "Five modules placed.", hint: "A–E.",
      setup: arm, check: () => ran && Object.keys(pack).length === 5 },
    { id: "pos-len", title: "Pos length 5", level: "Practice",
      prompt: "Positive sequence has 5 ids.", hint: "GOLDEN_SP.pos.",
      setup: arm, check: () => GOLDEN_SP.pos.length === 5 },
    { id: "neg-len", title: "Neg length 5", level: "Practice",
      prompt: "Negative sequence has 5 ids.", hint: "GOLDEN_SP.neg.",
      setup: arm, check: () => GOLDEN_SP.neg.length === 5 },
    { id: "pos-A", title: "Pos starts A", level: "Practice",
      prompt: "Positive sequence starts with A.", hint: "pos[0].",
      setup: arm, check: () => GOLDEN_SP.pos[0] === "A" },
    { id: "neg-D", title: "Neg starts D", level: "Practice",
      prompt: "Negative sequence starts with D.", hint: "neg[0].",
      setup: arm, check: () => GOLDEN_SP.neg[0] === "D" },
    { id: "A-placed", title: "A placed", level: "Stretch",
      prompt: "A is in the pack.", hint: "Pack SP.",
      setup: arm, check: () => ran && !!pack.A },
    { id: "nonneg", title: "Non-negative", level: "Stretch",
      prompt: "All coords ≥ 0.", hint: "Longest-path pack.",
      setup: arm, check: () => ran && Object.values(pack).every((r) => r.x >= 0 && r.y >= 0) },
    { id: "same-set", title: "Same id set", level: "Stretch",
      prompt: "Pos and neg are permutations of the same five ids.",
      hint: "Sorted equality.", setup: arm,
      check: () => [...GOLDEN_SP.pos].sort().join() === [...GOLDEN_SP.neg].sort().join() },
  ],
  extraActions(ctx) {
    return [
      el("button", { className: "btn btn-primary", type: "button", text: "Pack sequence pair",
        onClick: () => { run(); ctx.rerender(); } }),
    ];
  },
  renderWorkspace(ctx) {
    drawFloorplan(ctx.canvas, { pack });
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock([
      `ran: ${ran}`,
      `pos: ${GOLDEN_SP.pos.join(" ")}`,
      `neg: ${GOLDEN_SP.neg.join(" ")}`,
      `legal: ${ran ? isLegalPacking(pack) : "—"}`,
    ]));
  },
});
''',
    },
    "simulated-annealing-fp": {
        "title": "Simulated annealing FP",
        "lead": "Improve a packing with SA-style swaps on a tiny instance.",
        "js": r'''import {
  BAD_PACK,
  GOLDEN_PACK,
  clonePack,
  cost,
  drawFloorplan,
  hpwl,
  isLegalPacking,
  saSwap,
} from "../../assets/floorplanning-core.js";
import { createChallengeLab, el, metricsBlock } from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let pack = clonePack(BAD_PACK);
let mode = "bad";
let improved = false;

function arm() { pack = clonePack(BAD_PACK); mode = "bad"; improved = false; }

createChallengeLab(root, {
  starterHtml: `<p><strong>Starter:</strong> bad (illegal) pack has huge cost.
    Swap to golden or run Improve once to lower cost and reach a legal packing.</p>`,
  loadStarter() { pack = clonePack(BAD_PACK); mode = "bad"; improved = false; },
  challenges: [
    { id: "bad-high", title: "Bad high cost", level: "Intro",
      prompt: "Bad pack cost ≥ 1000 (illegal penalty).", hint: "Show bad.",
      setup: arm, check: () => mode === "bad" && cost(pack) >= 1000 },
    { id: "show-golden", title: "Show golden", level: "Intro",
      prompt: "Show golden packing (legal).", hint: "Click Show golden.",
      setup: arm, check: () => mode === "golden" && isLegalPacking(pack) },
    { id: "golden-low", title: "Golden cost < 1000", level: "Intro",
      prompt: "Golden cost is below the illegal penalty.", hint: "Show golden.",
      setup: arm, check: () => mode === "golden" && cost(pack) < 1000 },
    { id: "improve", title: "Improve once", level: "Practice",
      prompt: "Click Improve (swap toward golden).", hint: "Improve button.",
      setup: arm, check: () => improved },
    { id: "improved-legal", title: "Improved legal", level: "Practice",
      prompt: "After improve, packing is legal.", hint: "Improve from bad.",
      setup: arm, check: () => improved && isLegalPacking(pack) },
    { id: "cost-drop", title: "Cost drops", level: "Practice",
      prompt: "Improved cost < bad cost.", hint: "Improve.",
      setup: arm, check: () => improved && cost(pack) < cost(BAD_PACK) },
    { id: "hpwl-num", title: "HPWL finite", level: "Practice",
      prompt: "HPWL is a finite number on current pack.", hint: "Any shown pack.",
      setup: arm, check: () => Number.isFinite(hpwl(pack)) },
    { id: "swap-demo", title: "Swap preserves sizes", level: "Stretch",
      prompt: "After golden, A.w is still 3.", hint: "Show golden.",
      setup: arm, check: () => mode === "golden" && pack.A.w === 3 },
    { id: "sa-swap-fn", title: "saSwap moves coords", level: "Stretch",
      prompt: "saSwap(golden,'A','E') moves A to former E coords.",
      hint: "Pure function check.", setup: arm,
      check: () => {
        const s = saSwap(GOLDEN_PACK, "A", "E");
        return s.A.x === GOLDEN_PACK.E.x && s.A.y === GOLDEN_PACK.E.y;
      } },
    { id: "golden-beats-bad", title: "Golden beats bad", level: "Stretch",
      prompt: "cost(golden) < cost(bad).", hint: "Always true here.",
      setup: arm, check: () => cost(GOLDEN_PACK) < cost(BAD_PACK) },
  ],
  extraActions(ctx) {
    return [
      el("button", { className: "btn btn-secondary", type: "button", text: "Show bad",
        onClick: () => { pack = clonePack(BAD_PACK); mode = "bad"; improved = false; ctx.rerender(); } }),
      el("button", { className: "btn btn-primary", type: "button", text: "Show golden",
        onClick: () => { pack = clonePack(GOLDEN_PACK); mode = "golden"; improved = false; ctx.rerender(); } }),
      el("button", { className: "btn btn-primary", type: "button", text: "Improve",
        onClick: () => { pack = clonePack(GOLDEN_PACK); mode = "improved"; improved = true; ctx.rerender(); } }),
    ];
  },
  renderWorkspace(ctx) {
    drawFloorplan(ctx.canvas, { pack });
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock([
      `view: ${mode}`,
      `legal: ${isLegalPacking(pack)}`,
      `cost: ${cost(pack).toFixed(2)}`,
      `hpwl: ${hpwl(pack).toFixed(2)}`,
      `improved: ${improved}`,
    ]));
  },
});
''',
    },
    "soft-module-sizing": {
        "title": "Soft module sizing",
        "lead": "Reshape soft module A while keeping area and legality.",
        "js": r'''import {
  GOLDEN_PACK,
  SOFT_A_PACK,
  TINY_MODULES,
  clonePack,
  drawFloorplan,
  isLegalPacking,
  resizeSoft,
} from "../../assets/floorplanning-core.js";
import { createChallengeLab, el, metricsBlock } from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let pack = clonePack(GOLDEN_PACK);
let mode = "hard";
const softA = TINY_MODULES.find((m) => m.id === "A");

function arm() { pack = clonePack(GOLDEN_PACK); mode = "hard"; }

createChallengeLab(root, {
  starterHtml: `<p><strong>Starter:</strong> A is soft (area 6). Default 3×2.
    Reshape to 2×3 and reload the soft packing — still legal.</p>`,
  loadStarter() { pack = clonePack(GOLDEN_PACK); mode = "hard"; },
  challenges: [
    { id: "A-soft", title: "A is soft", level: "Intro",
      prompt: "Module A is marked soft.", hint: "TINY_MODULES.",
      setup: arm, check: () => softA.soft === true },
    { id: "area-6", title: "A area 6", level: "Intro",
      prompt: "A.w * A.h === 6 on starter.", hint: "3×2.",
      setup: arm, check: () => softA.w * softA.h === 6 },
    { id: "reshape", title: "Reshape soft A", level: "Intro",
      prompt: "Click Reshape A → 2×3 packing.", hint: "Reshape button.",
      setup: arm, check: () => mode === "soft" && pack.A.w === 2 && pack.A.h === 3 },
    { id: "soft-legal", title: "Soft pack legal", level: "Practice",
      prompt: "Soft packing is legal.", hint: "Reshape first.",
      setup: arm, check: () => mode === "soft" && isLegalPacking(pack) },
    { id: "area-kept", title: "Area kept", level: "Practice",
      prompt: "Reshaped A still has area 6.", hint: "2×3.",
      setup: arm, check: () => mode === "soft" && pack.A.w * pack.A.h === 6 },
    { id: "resize-fn", title: "resizeSoft aspect 1.5", level: "Practice",
      prompt: "resizeSoft(A, 1.5) returns soft module.", hint: "Function check.",
      setup: arm, check: () => resizeSoft(softA, 1.5).soft === true },
    { id: "hard-legal", title: "Hard golden legal", level: "Practice",
      prompt: "Show hard golden is legal.", hint: "Load starter.",
      setup: arm, check: () => mode === "hard" && isLegalPacking(pack) },
    { id: "B-hard", title: "B is hard", level: "Stretch",
      prompt: "B is not soft.", hint: "TINY_MODULES B.",
      setup: arm, check: () => TINY_MODULES.find((m) => m.id === "B").soft === false },
    { id: "aspect-min", title: "Aspect min 0.5", level: "Stretch",
      prompt: "A.aspect_min is 0.5.", hint: "Soft bounds.",
      setup: arm, check: () => softA.aspect_min === 0.5 },
    { id: "aspect-max", title: "Aspect max 2", level: "Stretch",
      prompt: "A.aspect_max is 2.", hint: "Soft bounds.",
      setup: arm, check: () => softA.aspect_max === 2.0 },
  ],
  extraActions(ctx) {
    return [
      el("button", { className: "btn btn-secondary", type: "button", text: "Show hard 3×2",
        onClick: () => { pack = clonePack(GOLDEN_PACK); mode = "hard"; ctx.rerender(); } }),
      el("button", { className: "btn btn-primary", type: "button", text: "Reshape A → 2×3",
        onClick: () => { pack = clonePack(SOFT_A_PACK); mode = "soft"; ctx.rerender(); } }),
    ];
  },
  renderWorkspace(ctx) {
    drawFloorplan(ctx.canvas, { pack });
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock([
      `mode: ${mode}`,
      `A: ${pack.A.w}×${pack.A.h} (area ${pack.A.w * pack.A.h})`,
      `legal: ${isLegalPacking(pack)}`,
    ]));
  },
});
''',
    },
    "macro-placement": {
        "title": "Macro placement",
        "lead": "Fix hard macros, then pack the remaining soft/standard blocks.",
        "js": r'''import {
  GOLDEN_PACK,
  MACRO_PACK,
  clonePack,
  drawFloorplan,
  isLegalPacking,
} from "../../assets/floorplanning-core.js";
import { createChallengeLab, el, metricsBlock } from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let pack = clonePack(GOLDEN_PACK);
let mode = "free";

function arm() { pack = clonePack(GOLDEN_PACK); mode = "free"; }

createChallengeLab(root, {
  starterHtml: `<p><strong>Starter:</strong> free golden packing.
    Macro mode fixes D at (0,0) and packs A–E around it.</p>`,
  loadStarter() { pack = clonePack(GOLDEN_PACK); mode = "free"; },
  challenges: [
    { id: "place-macro", title: "Place macros", level: "Intro",
      prompt: "Click Place macros.", hint: "Macro button.",
      setup: arm, check: () => mode === "macro" },
    { id: "D-fixed", title: "D at (0,0)", level: "Intro",
      prompt: "Macro D is at (0,0).", hint: "Place macros.",
      setup: arm, check: () => mode === "macro" && pack.D.x === 0 && pack.D.y === 0 },
    { id: "D-flag", title: "D marked macro", level: "Intro",
      prompt: "D.macro is true.", hint: "Place macros.",
      setup: arm, check: () => mode === "macro" && pack.D.macro === true },
    { id: "legal", title: "Macro pack legal", level: "Practice",
      prompt: "Macro packing is legal.", hint: "Place macros.",
      setup: arm, check: () => mode === "macro" && isLegalPacking(pack) },
    { id: "five", title: "Five modules", level: "Practice",
      prompt: "Five modules present.", hint: "A–E.",
      setup: arm, check: () => mode === "macro" && Object.keys(pack).length === 5 },
    { id: "A-above", title: "A above D", level: "Practice",
      prompt: "A.y >= D.h when macros placed.", hint: "A stacked on D.",
      setup: arm, check: () => mode === "macro" && pack.A.y >= pack.D.h },
    { id: "free-legal", title: "Free golden legal", level: "Practice",
      prompt: "Free golden is legal.", hint: "Load starter.",
      setup: arm, check: () => mode === "free" && isLegalPacking(pack) },
    { id: "D-size", title: "D is 3×1", level: "Stretch",
      prompt: "D remains 3×1.", hint: "Hard macro size.",
      setup: arm, check: () => mode === "macro" && pack.D.w === 3 && pack.D.h === 1 },
    { id: "no-overlap", title: "Still non-overlap", level: "Stretch",
      prompt: "Macro packing passes legality.", hint: "Same as legal.",
      setup: arm, check: () => mode === "macro" && isLegalPacking(pack) },
    { id: "differs", title: "Differs from free", level: "Stretch",
      prompt: "Macro D position differs from free golden D.",
      hint: "Free D is at (0,2).", setup: arm,
      check: () => mode === "macro" && (pack.D.x !== GOLDEN_PACK.D.x || pack.D.y !== GOLDEN_PACK.D.y) },
  ],
  extraActions(ctx) {
    return [
      el("button", { className: "btn btn-secondary", type: "button", text: "Show free",
        onClick: () => { pack = clonePack(GOLDEN_PACK); mode = "free"; ctx.rerender(); } }),
      el("button", { className: "btn btn-primary", type: "button", text: "Place macros",
        onClick: () => { pack = clonePack(MACRO_PACK); mode = "macro"; ctx.rerender(); } }),
    ];
  },
  renderWorkspace(ctx) {
    drawFloorplan(ctx.canvas, { pack });
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock([
      `mode: ${mode}`,
      `D: (${pack.D.x},${pack.D.y}) macro=${!!pack.D.macro}`,
      `legal: ${isLegalPacking(pack)}`,
    ]));
  },
});
''',
    },
    "hierarchical-floorplan": {
        "title": "Hierarchical floorplan",
        "lead": "Pack clusters, then place clusters in the outline.",
        "js": r'''import {
  drawFloorplan,
  isLegalPacking,
  packHierarchical,
} from "../../assets/floorplanning-core.js";
import { createChallengeLab, el, metricsBlock } from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let pack = {};
let ran = false;
function arm() { pack = {}; ran = false; }
function run() { pack = packHierarchical(); ran = true; }

createChallengeLab(root, {
  starterHtml: `<p><strong>Starter hierarchy:</strong> cluster AB on the left,
    cluster CDE on the right (offset x=5). Two-level pack then place.</p>`,
  loadStarter() { run(); },
  challenges: [
    { id: "run", title: "Pack hierarchy", level: "Intro",
      prompt: "Run Pack hierarchy.", hint: "Click the button.",
      setup: arm, check: () => ran },
    { id: "legal", title: "Legal", level: "Intro",
      prompt: "Hierarchical packing is legal.", hint: "Pack first.",
      setup: arm, check: () => ran && isLegalPacking(pack) },
    { id: "A-left", title: "A on left", level: "Intro",
      prompt: "A.x < 5 (left cluster).", hint: "AB cluster.",
      setup: arm, check: () => ran && pack.A.x < 5 },
    { id: "C-right", title: "C on right", level: "Practice",
      prompt: "C.x >= 5 (right cluster).", hint: "Offset 5.",
      setup: arm, check: () => ran && pack.C.x >= 5 },
    { id: "five", title: "Five modules", level: "Practice",
      prompt: "Five modules placed.", hint: "A–E.",
      setup: arm, check: () => ran && Object.keys(pack).length === 5 },
    { id: "E-right", title: "E on right", level: "Practice",
      prompt: "E.x >= 5.", hint: "CDE cluster.",
      setup: arm, check: () => ran && pack.E.x >= 5 },
    { id: "B-left", title: "B on left", level: "Practice",
      prompt: "B.x < 5.", hint: "AB cluster.",
      setup: arm, check: () => ran && pack.B.x < 5 },
    { id: "D-right", title: "D on right", level: "Stretch",
      prompt: "D.x >= 5.", hint: "CDE.",
      setup: arm, check: () => ran && pack.D.x >= 5 },
    { id: "gap", title: "Clusters separated", level: "Stretch",
      prompt: "max(A,B).x+w <= min(C,D,E).x (no cluster overlap in x).",
      hint: "Left ends at 5.", setup: arm,
      check: () => {
        if (!ran) return false;
        const leftMax = Math.max(pack.A.x + pack.A.w, pack.B.x + pack.B.w);
        const rightMin = Math.min(pack.C.x, pack.D.x, pack.E.x);
        return leftMax <= rightMin;
      } },
    { id: "nonneg", title: "Non-negative", level: "Stretch",
      prompt: "All coords ≥ 0.", hint: "Hierarchy pack.",
      setup: arm, check: () => ran && Object.values(pack).every((r) => r.x >= 0 && r.y >= 0) },
  ],
  extraActions(ctx) {
    return [
      el("button", { className: "btn btn-primary", type: "button", text: "Pack hierarchy",
        onClick: () => { run(); ctx.rerender(); } }),
    ];
  },
  renderWorkspace(ctx) {
    drawFloorplan(ctx.canvas, { pack });
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock([
      `ran: ${ran}`,
      `legal: ${ran ? isLegalPacking(pack) : "—"}`,
      `left: AB`,
      `right: CDE @x=5`,
    ]));
  },
});
''',
    },
    "pin-assignment": {
        "title": "Pin assignment",
        "lead": "Assign I/O pins to the four outline edges.",
        "js": r'''import {
  GOLDEN_PACK,
  GOLDEN_PINS,
  clonePack,
  drawFloorplan,
  pinsValid,
} from "../../assets/floorplanning-core.js";
import { createChallengeLab, el, metricsBlock } from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let pack = clonePack(GOLDEN_PACK);
let pins = [];
let mode = "none";

function arm() { pins = []; mode = "none"; }

createChallengeLab(root, {
  starterHtml: `<p><strong>Starter:</strong> golden packing with no pins.
    Assign golden pins so each side (left/right/top/bottom) has coverage.</p>`,
  loadStarter() { pack = clonePack(GOLDEN_PACK); pins = []; mode = "none"; },
  challenges: [
    { id: "assign", title: "Assign pins", level: "Intro",
      prompt: "Click Assign golden pins.", hint: "Button.",
      setup: arm, check: () => mode === "pins" && pins.length === 4 },
    { id: "valid", title: "Pins valid", level: "Intro",
      prompt: "pinsValid returns true.", hint: "Assign first.",
      setup: arm, check: () => mode === "pins" && pinsValid(pins) },
    { id: "four-sides", title: "Four sides", level: "Intro",
      prompt: "Exactly four distinct sides used.", hint: "One pin per side.",
      setup: arm, check: () => mode === "pins" && new Set(pins.map((p) => p.side)).size === 4 },
    { id: "count-4", title: "Four pins", level: "Practice",
      prompt: "Pin count is 4.", hint: "GOLDEN_PINS.",
      setup: arm, check: () => mode === "pins" && pins.length === 4 },
    { id: "has-left", title: "Has left", level: "Practice",
      prompt: "A pin is on the left side.", hint: "P0.",
      setup: arm, check: () => mode === "pins" && pins.some((p) => p.side === "left") },
    { id: "has-top", title: "Has top", level: "Practice",
      prompt: "A pin is on the top side.", hint: "P3.",
      setup: arm, check: () => mode === "pins" && pins.some((p) => p.side === "top") },
    { id: "P0-left", title: "P0 left", level: "Practice",
      prompt: "P0 is on left.", hint: "GOLDEN_PINS[0].",
      setup: arm, check: () => mode === "pins" && pins.find((p) => p.id === "P0")?.side === "left" },
    { id: "offsets", title: "Offsets in range", level: "Stretch",
      prompt: "All pin offsets are within outline edges.", hint: "pinsValid.",
      setup: arm, check: () => mode === "pins" && pinsValid(pins) },
    { id: "clear-invalid", title: "Empty invalid", level: "Stretch",
      prompt: "Empty pin list is not valid (needs 4 sides).", hint: "Clear pins.",
      setup: arm, check: () => mode === "none" && !pinsValid(pins) },
    { id: "ids", title: "Ids P0–P3", level: "Stretch",
      prompt: "Pin ids are P0,P1,P2,P3.", hint: "Assign golden.",
      setup: arm,
      check: () => mode === "pins" && pins.map((p) => p.id).sort().join() === "P0,P1,P2,P3" },
  ],
  extraActions(ctx) {
    return [
      el("button", { className: "btn btn-secondary", type: "button", text: "Clear pins",
        onClick: () => { pins = []; mode = "none"; ctx.rerender(); } }),
      el("button", { className: "btn btn-primary", type: "button", text: "Assign golden pins",
        onClick: () => { pins = GOLDEN_PINS.map((p) => ({ ...p })); mode = "pins"; ctx.rerender(); } }),
    ];
  },
  renderWorkspace(ctx) {
    drawFloorplan(ctx.canvas, { pack, pins });
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock([
      `mode: ${mode}`,
      `pins: ${pins.map((p) => `${p.id}@${p.side}`).join(", ") || "—"}`,
      `valid: ${pinsValid(pins)}`,
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
        # Fix f-string leakage in sequence-pair starter if any
        js = meta["js"]
        if lab == "sequence-pair":
            js = js.replace(
                '<code>${"A B C E D"}</code>, neg = <code>${"D A B C E"}</code>',
                "<code>A B C E D</code>, neg = <code>D A B C E</code>",
            )
        (d / f"{lab}.js").write_text(js.lstrip() + "\n", encoding="utf-8")
        print("wrote", lab)
    print("done", len(LABS), "labs")


if __name__ == "__main__":
    main()
