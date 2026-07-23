import {
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

