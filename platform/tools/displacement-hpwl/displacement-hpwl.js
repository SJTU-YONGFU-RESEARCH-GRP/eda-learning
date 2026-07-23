import {
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

