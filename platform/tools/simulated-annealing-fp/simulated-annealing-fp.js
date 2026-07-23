import {
  BAD_PACK,
  GOLDEN_PACK,
  clonePack,
  cost,
  drawFloorplan,
  hpwl,
  isLegalPacking,
  saSwap,
} from "../../assets/floorplanning-core.js";
import { createChallengeLab, el, metricsBlock } from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let pack = clonePack(BAD_PACK);
let mode = "bad";
let improved = false;

function arm() { pack = clonePack(BAD_PACK); mode = "bad"; improved = false; }

createChallengeLab(root, {
  starterHtml: `<p><strong>Starter:</strong> bad (illegal) pack has huge cost.
    Swap to golden or run Improve once to lower cost and reach a legal packing.</p>`,
  loadStarter() { pack = clonePack(BAD_PACK); mode = "bad"; improved = false; },
  challenges: [
    { id: "bad-high", title: "Bad high cost", level: "Intro",
      prompt: "Bad pack cost ≥ 1000 (illegal penalty).", hint: "Show bad.",
      setup: arm, check: () => mode === "bad" && cost(pack) >= 1000 },
    { id: "show-golden", title: "Show golden", level: "Intro",
      prompt: "Show golden packing (legal).", hint: "Click Show golden.",
      setup: arm, check: () => mode === "golden" && isLegalPacking(pack) },
    { id: "golden-low", title: "Golden cost < 1000", level: "Intro",
      prompt: "Golden cost is below the illegal penalty.", hint: "Show golden.",
      setup: arm, check: () => mode === "golden" && cost(pack) < 1000 },
    { id: "improve", title: "Improve once", level: "Practice",
      prompt: "Click Improve (swap toward golden).", hint: "Improve button.",
      setup: arm, check: () => improved },
    { id: "improved-legal", title: "Improved legal", level: "Practice",
      prompt: "After improve, packing is legal.", hint: "Improve from bad.",
      setup: arm, check: () => improved && isLegalPacking(pack) },
    { id: "cost-drop", title: "Cost drops", level: "Practice",
      prompt: "Improved cost < bad cost.", hint: "Improve.",
      setup: arm, check: () => improved && cost(pack) < cost(BAD_PACK) },
    { id: "hpwl-num", title: "HPWL finite", level: "Practice",
      prompt: "HPWL is a finite number on current pack.", hint: "Any shown pack.",
      setup: arm, check: () => Number.isFinite(hpwl(pack)) },
    { id: "swap-demo", title: "Swap preserves sizes", level: "Stretch",
      prompt: "After golden, A.w is still 3.", hint: "Show golden.",
      setup: arm, check: () => mode === "golden" && pack.A.w === 3 },
    { id: "sa-swap-fn", title: "saSwap moves coords", level: "Stretch",
      prompt: "saSwap(golden,'A','E') moves A to former E coords.",
      hint: "Pure function check.", setup: arm,
      check: () => {
        const s = saSwap(GOLDEN_PACK, "A", "E");
        return s.A.x === GOLDEN_PACK.E.x && s.A.y === GOLDEN_PACK.E.y;
      } },
    { id: "golden-beats-bad", title: "Golden beats bad", level: "Stretch",
      prompt: "cost(golden) < cost(bad).", hint: "Always true here.",
      setup: arm, check: () => cost(GOLDEN_PACK) < cost(BAD_PACK) },
  ],
  extraActions(ctx) {
    return [
      el("button", { className: "btn btn-secondary", type: "button", text: "Show bad",
        onClick: () => { pack = clonePack(BAD_PACK); mode = "bad"; improved = false; ctx.rerender(); } }),
      el("button", { className: "btn btn-primary", type: "button", text: "Show golden",
        onClick: () => { pack = clonePack(GOLDEN_PACK); mode = "golden"; improved = false; ctx.rerender(); } }),
      el("button", { className: "btn btn-primary", type: "button", text: "Improve",
        onClick: () => { pack = clonePack(GOLDEN_PACK); mode = "improved"; improved = true; ctx.rerender(); } }),
    ];
  },
  renderWorkspace(ctx) {
    drawFloorplan(ctx.canvas, { pack });
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock([
      `view: ${mode}`,
      `legal: ${isLegalPacking(pack)}`,
      `cost: ${cost(pack).toFixed(2)}`,
      `hpwl: ${hpwl(pack).toFixed(2)}`,
      `improved: ${improved}`,
    ]));
  },
});

