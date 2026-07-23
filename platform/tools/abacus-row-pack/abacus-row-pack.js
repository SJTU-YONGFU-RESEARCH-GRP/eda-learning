import {
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

