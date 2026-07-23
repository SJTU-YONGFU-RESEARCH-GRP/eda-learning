import {
  GOLDEN_BSTAR,
  drawFloorplan,
  isLegalPacking,
  packBstar,
} from "../../assets/floorplanning-core.js";
import { createChallengeLab, el, metricsBlock } from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let pack = {};
let ran = false;
function arm() { pack = {}; ran = false; }
function run() { pack = packBstar(GOLDEN_BSTAR); ran = true; }

createChallengeLab(root, {
  starterHtml: `<p><strong>Starter B*:</strong> A root; left chain B→C→E (right-of);
    right child D (above A). Pack with contour placement.</p>`,
  loadStarter() { run(); },
  challenges: [
    { id: "run", title: "Pack B*", level: "Intro", prompt: "Run Pack B*-tree.",
      hint: "Click the button.", setup: arm, check: () => ran },
    { id: "legal", title: "Legal packing", level: "Intro",
      prompt: "Result is legal.", hint: "Pack first.",
      setup: arm, check: () => ran && isLegalPacking(pack) },
    { id: "A-origin", title: "A at origin", level: "Intro",
      prompt: "A is at (0,0).", hint: "Root placed first.",
      setup: arm, check: () => ran && pack.A.x === 0 && pack.A.y === 0 },
    { id: "B-right", title: "B right of A", level: "Practice",
      prompt: "B.x equals A.x + A.w.", hint: "Left child = right-of.",
      setup: arm, check: () => ran && pack.B.x === pack.A.x + pack.A.w },
    { id: "D-above", title: "D above A", level: "Practice",
      prompt: "D.y >= A.h (above A contour).", hint: "Right child = above.",
      setup: arm, check: () => ran && pack.D.y >= pack.A.h },
    { id: "five", title: "Five modules", level: "Practice",
      prompt: "Five modules placed.", hint: "A–E.",
      setup: arm, check: () => ran && Object.keys(pack).length === 5 },
    { id: "C-exists", title: "C placed", level: "Practice",
      prompt: "C is in the pack.", hint: "In left chain.",
      setup: arm, check: () => ran && !!pack.C },
    { id: "E-exists", title: "E placed", level: "Stretch",
      prompt: "E is in the pack.", hint: "End of left chain.",
      setup: arm, check: () => ran && !!pack.E },
    { id: "no-neg", title: "Non-negative coords", level: "Stretch",
      prompt: "All x,y ≥ 0.", hint: "Contour pack.",
      setup: arm, check: () => ran && Object.values(pack).every((r) => r.x >= 0 && r.y >= 0) },
    { id: "root-A", title: "Root is A", level: "Stretch",
      prompt: "Golden tree root id is A.", hint: "GOLDEN_BSTAR.id.",
      setup: arm, check: () => GOLDEN_BSTAR.id === "A" },
  ],
  extraActions(ctx) {
    return [
      el("button", { className: "btn btn-primary", type: "button", text: "Pack B*-tree",
        onClick: () => { run(); ctx.rerender(); } }),
    ];
  },
  renderWorkspace(ctx) {
    drawFloorplan(ctx.canvas, { pack });
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock([
      `ran: ${ran}`,
      `legal: ${ran ? isLegalPacking(pack) : "—"}`,
      `A: ${ran ? `(${pack.A.x},${pack.A.y})` : "—"}`,
      `modules: ${Object.keys(pack).join(",") || "—"}`,
    ]));
  },
});

