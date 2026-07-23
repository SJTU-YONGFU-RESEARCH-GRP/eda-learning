import {
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

