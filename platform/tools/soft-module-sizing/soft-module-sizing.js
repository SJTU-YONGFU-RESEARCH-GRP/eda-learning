import {
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

