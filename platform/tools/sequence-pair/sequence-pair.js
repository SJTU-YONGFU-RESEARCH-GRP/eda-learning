import {
  GOLDEN_SP,
  drawFloorplan,
  isLegalPacking,
  packSequencePair,
} from "../../assets/floorplanning-core.js";
import { createChallengeLab, el, metricsBlock } from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let pack = {};
let ran = false;
function arm() { pack = {}; ran = false; }
function run() {
  pack = packSequencePair(GOLDEN_SP.pos, GOLDEN_SP.neg);
  ran = true;
}

createChallengeLab(root, {
  starterHtml: `<p><strong>Starter SP:</strong> pos =
    <code>A B C E D</code>, neg = <code>D A B C E</code>.</p>`,
  loadStarter() { run(); },
  challenges: [
    { id: "run", title: "Pack SP", level: "Intro", prompt: "Run Pack sequence pair.",
      hint: "Click the button.", setup: arm, check: () => ran },
    { id: "legal", title: "Legal", level: "Intro",
      prompt: "Packing is legal.", hint: "Pack first.",
      setup: arm, check: () => ran && isLegalPacking(pack) },
    { id: "five", title: "Five modules", level: "Intro",
      prompt: "Five modules placed.", hint: "A–E.",
      setup: arm, check: () => ran && Object.keys(pack).length === 5 },
    { id: "pos-len", title: "Pos length 5", level: "Practice",
      prompt: "Positive sequence has 5 ids.", hint: "GOLDEN_SP.pos.",
      setup: arm, check: () => GOLDEN_SP.pos.length === 5 },
    { id: "neg-len", title: "Neg length 5", level: "Practice",
      prompt: "Negative sequence has 5 ids.", hint: "GOLDEN_SP.neg.",
      setup: arm, check: () => GOLDEN_SP.neg.length === 5 },
    { id: "pos-A", title: "Pos starts A", level: "Practice",
      prompt: "Positive sequence starts with A.", hint: "pos[0].",
      setup: arm, check: () => GOLDEN_SP.pos[0] === "A" },
    { id: "neg-D", title: "Neg starts D", level: "Practice",
      prompt: "Negative sequence starts with D.", hint: "neg[0].",
      setup: arm, check: () => GOLDEN_SP.neg[0] === "D" },
    { id: "A-placed", title: "A placed", level: "Stretch",
      prompt: "A is in the pack.", hint: "Pack SP.",
      setup: arm, check: () => ran && !!pack.A },
    { id: "nonneg", title: "Non-negative", level: "Stretch",
      prompt: "All coords ≥ 0.", hint: "Longest-path pack.",
      setup: arm, check: () => ran && Object.values(pack).every((r) => r.x >= 0 && r.y >= 0) },
    { id: "same-set", title: "Same id set", level: "Stretch",
      prompt: "Pos and neg are permutations of the same five ids.",
      hint: "Sorted equality.", setup: arm,
      check: () => [...GOLDEN_SP.pos].sort().join() === [...GOLDEN_SP.neg].sort().join() },
  ],
  extraActions(ctx) {
    return [
      el("button", { className: "btn btn-primary", type: "button", text: "Pack sequence pair",
        onClick: () => { run(); ctx.rerender(); } }),
    ];
  },
  renderWorkspace(ctx) {
    drawFloorplan(ctx.canvas, { pack });
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock([
      `ran: ${ran}`,
      `pos: ${GOLDEN_SP.pos.join(" ")}`,
      `neg: ${GOLDEN_SP.neg.join(" ")}`,
      `legal: ${ran ? isLegalPacking(pack) : "—"}`,
    ]));
  },
});

