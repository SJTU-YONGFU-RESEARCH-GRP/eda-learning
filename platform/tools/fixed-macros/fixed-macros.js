import {
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

