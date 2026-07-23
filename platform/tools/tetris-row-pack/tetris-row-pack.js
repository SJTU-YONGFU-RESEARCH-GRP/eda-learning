import {
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

