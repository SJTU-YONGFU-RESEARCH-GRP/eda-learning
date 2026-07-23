import {
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

