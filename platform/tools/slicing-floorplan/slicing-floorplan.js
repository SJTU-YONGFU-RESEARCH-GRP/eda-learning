import {
  GOLDEN_POLISH,
  OUTLINE,
  drawFloorplan,
  evalPolish,
  isLegalPacking,
} from "../../assets/floorplanning-core.js";
import { createChallengeLab, el, metricsBlock } from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let pack = {};
let bb = { w: 0, h: 0 };
let ran = false;

function arm() { pack = {}; bb = { w: 0, h: 0 }; ran = false; }
function run() {
  const r = evalPolish(GOLDEN_POLISH);
  pack = r.pack; bb = { w: r.w, h: r.h }; ran = true;
}

createChallengeLab(root, {
  starterHtml: `<p><strong>Starter polish:</strong>
    <code>A D H B V C V E V</code> → bounding box width 9, height 3 (fits in 10×8).</p>`,
  loadStarter() { run(); },
  challenges: [
    { id: "run", title: "Evaluate polish", level: "Intro",
      prompt: "Run Evaluate polish.", hint: "Click the button.",
      setup: arm, check: () => ran },
    { id: "bb-w", title: "BB width 9", level: "Intro",
      prompt: "Bounding width is 9.", hint: "Evaluate first.",
      setup: arm, check: () => ran && bb.w === 9 },
    { id: "bb-h", title: "BB height 3", level: "Intro",
      prompt: "Bounding height is 3.", hint: "A+D stacked is height 3.",
      setup: arm, check: () => ran && bb.h === 3 },
    { id: "legal", title: "Fits outline", level: "Practice",
      prompt: "Resulting packing is legal in 10×8.", hint: "Evaluate.",
      setup: arm, check: () => ran && isLegalPacking(pack) },
    { id: "has-A", title: "Places A", level: "Practice",
      prompt: "Pack includes A at origin-ish.", hint: "A is first leaf.",
      setup: arm, check: () => ran && pack.A && pack.A.x === 0 && pack.A.y === 0 },
    { id: "has-E", title: "Places E", level: "Practice",
      prompt: "Pack includes E.", hint: "Last V attaches E.",
      setup: arm, check: () => ran && !!pack.E },
    { id: "five", title: "Five modules", level: "Practice",
      prompt: "Exactly five modules placed.", hint: "A–E.",
      setup: arm, check: () => ran && Object.keys(pack).length === 5 },
    { id: "polish-len", title: "Polish length 9", level: "Stretch",
      prompt: "Golden polish token count is 9.", hint: "5 ops + 4 operators? count tokens.",
      setup: arm, check: () => GOLDEN_POLISH.length === 9 },
    { id: "fits-w", title: "BB ≤ outline W", level: "Stretch",
      prompt: "Bounding width ≤ outline width.", hint: "9 ≤ 10.",
      setup: arm, check: () => ran && bb.w <= OUTLINE.w },
    { id: "fits-h", title: "BB ≤ outline H", level: "Stretch",
      prompt: "Bounding height ≤ outline height.", hint: "3 ≤ 8.",
      setup: arm, check: () => ran && bb.h <= OUTLINE.h },
  ],
  extraActions(ctx) {
    return [
      el("button", { className: "btn btn-primary", type: "button", text: "Evaluate polish",
        onClick: () => { run(); ctx.rerender(); } }),
    ];
  },
  renderWorkspace(ctx) {
    drawFloorplan(ctx.canvas, { pack });
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock([
      `ran: ${ran}`,
      `polish: ${GOLDEN_POLISH.join(" ")}`,
      `bb: ${bb.w}×${bb.h}`,
      `legal: ${ran ? isLegalPacking(pack) : "—"}`,
    ]));
  },
});

