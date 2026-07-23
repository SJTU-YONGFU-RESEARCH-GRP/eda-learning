import {
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

