import {
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

