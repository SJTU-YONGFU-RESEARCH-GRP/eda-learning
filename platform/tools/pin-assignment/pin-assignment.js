import {
  GOLDEN_PACK,
  GOLDEN_PINS,
  clonePack,
  drawFloorplan,
  pinsValid,
} from "../../assets/floorplanning-core.js";
import { createChallengeLab, el, metricsBlock } from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let pack = clonePack(GOLDEN_PACK);
let pins = [];
let mode = "none";

function arm() { pins = []; mode = "none"; }

createChallengeLab(root, {
  starterHtml: `<p><strong>Starter:</strong> golden packing with no pins.
    Assign golden pins so each side (left/right/top/bottom) has coverage.</p>`,
  loadStarter() { pack = clonePack(GOLDEN_PACK); pins = []; mode = "none"; },
  challenges: [
    { id: "assign", title: "Assign pins", level: "Intro",
      prompt: "Click Assign golden pins.", hint: "Button.",
      setup: arm, check: () => mode === "pins" && pins.length === 4 },
    { id: "valid", title: "Pins valid", level: "Intro",
      prompt: "pinsValid returns true.", hint: "Assign first.",
      setup: arm, check: () => mode === "pins" && pinsValid(pins) },
    { id: "four-sides", title: "Four sides", level: "Intro",
      prompt: "Exactly four distinct sides used.", hint: "One pin per side.",
      setup: arm, check: () => mode === "pins" && new Set(pins.map((p) => p.side)).size === 4 },
    { id: "count-4", title: "Four pins", level: "Practice",
      prompt: "Pin count is 4.", hint: "GOLDEN_PINS.",
      setup: arm, check: () => mode === "pins" && pins.length === 4 },
    { id: "has-left", title: "Has left", level: "Practice",
      prompt: "A pin is on the left side.", hint: "P0.",
      setup: arm, check: () => mode === "pins" && pins.some((p) => p.side === "left") },
    { id: "has-top", title: "Has top", level: "Practice",
      prompt: "A pin is on the top side.", hint: "P3.",
      setup: arm, check: () => mode === "pins" && pins.some((p) => p.side === "top") },
    { id: "P0-left", title: "P0 left", level: "Practice",
      prompt: "P0 is on left.", hint: "GOLDEN_PINS[0].",
      setup: arm, check: () => mode === "pins" && pins.find((p) => p.id === "P0")?.side === "left" },
    { id: "offsets", title: "Offsets in range", level: "Stretch",
      prompt: "All pin offsets are within outline edges.", hint: "pinsValid.",
      setup: arm, check: () => mode === "pins" && pinsValid(pins) },
    { id: "clear-invalid", title: "Empty invalid", level: "Stretch",
      prompt: "Empty pin list is not valid (needs 4 sides).", hint: "Clear pins.",
      setup: arm, check: () => mode === "none" && !pinsValid(pins) },
    { id: "ids", title: "Ids P0–P3", level: "Stretch",
      prompt: "Pin ids are P0,P1,P2,P3.", hint: "Assign golden.",
      setup: arm,
      check: () => mode === "pins" && pins.map((p) => p.id).sort().join() === "P0,P1,P2,P3" },
  ],
  extraActions(ctx) {
    return [
      el("button", { className: "btn btn-secondary", type: "button", text: "Clear pins",
        onClick: () => { pins = []; mode = "none"; ctx.rerender(); } }),
      el("button", { className: "btn btn-primary", type: "button", text: "Assign golden pins",
        onClick: () => { pins = GOLDEN_PINS.map((p) => ({ ...p })); mode = "pins"; ctx.rerender(); } }),
    ];
  },
  renderWorkspace(ctx) {
    drawFloorplan(ctx.canvas, { pack, pins });
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock([
      `mode: ${mode}`,
      `pins: ${pins.map((p) => `${p.id}@${p.side}`).join(", ") || "—"}`,
      `valid: ${pinsValid(pins)}`,
    ]));
  },
});

