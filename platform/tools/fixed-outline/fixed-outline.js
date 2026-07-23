import {
  BAD_PACK,
  GOLDEN_PACK,
  OVERLAP_PACK,
  OUTLINE,
  clonePack,
  deadspace,
  density,
  drawFloorplan,
  isLegalPacking,
  legalityReport,
} from "../../assets/floorplanning-core.js";
import {
  createChallengeLab,
  el,
  metricsBlock,
} from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let pack = clonePack(BAD_PACK);
let mode = "bad";

function arm() {
  pack = clonePack(BAD_PACK);
  mode = "none";
}

createChallengeLab(root, {
  starterHtml: `
    <p><strong>Starter (reference):</strong> bad pack overflows (E past right edge).
    Golden pack is legal inside <code>10×8</code>. Deadspace for module areas is
    <strong>57</strong> (density <strong>0.2875</strong>) whenever packing is legal.</p>
  `,
  loadStarter() {
    pack = clonePack(BAD_PACK);
    mode = "bad";
  },
  challenges: [
    { id: "bad-illegal", title: "Bad pack illegal", level: "Intro",
      prompt: "Show bad pack; legality must fail.", hint: "Click Show bad.",
      setup: arm, check: () => mode === "bad" && !isLegalPacking(pack) },
    { id: "bad-reason", title: "Bad reason: E outside", level: "Intro",
      prompt: "Bad pack report mentions E outside outline.",
      hint: "E at x=9 with w=2 overflows.",
      setup: arm, check: () => mode === "bad" && legalityReport(pack).reason.includes("E") },
    { id: "golden-legal", title: "Golden legal", level: "Intro",
      prompt: "Show golden; packing must be legal.", hint: "Click Show golden.",
      setup: arm, check: () => mode === "golden" && isLegalPacking(pack) },
    { id: "golden-ok", title: "Golden reason ok", level: "Practice",
      prompt: "Golden report reason is ok.", hint: "Show golden first.",
      setup: arm, check: () => mode === "golden" && legalityReport(pack).reason === "ok" },
    { id: "overlap-illegal", title: "Overlap illegal", level: "Practice",
      prompt: "Show overlap pack; must be illegal.", hint: "Click Show overlap.",
      setup: arm, check: () => mode === "overlap" && !isLegalPacking(pack) },
    { id: "outline-10x8", title: "Outline 10×8", level: "Practice",
      prompt: "Outline width is 10 and height is 8.", hint: "Always true for this lab.",
      setup: arm, check: () => OUTLINE.w === 10 && OUTLINE.h === 8 },
    { id: "deadspace-57", title: "Deadspace 57", level: "Practice",
      prompt: "Module deadspace vs outline is 57 (independent of placement).",
      hint: "80 − 23 = 57.", setup: arm, check: () => deadspace() === 57 },
    { id: "density-2875", title: "Density 0.2875", level: "Stretch",
      prompt: "Density equals 23/80 = 0.2875.", hint: "moduleAreaSum / outlineArea.",
      setup: arm, check: () => Math.abs(density() - 0.2875) < 1e-9 },
    { id: "golden-not-bad", title: "Golden differs from bad", level: "Stretch",
      prompt: "With golden shown, packing is legal while bad is not.",
      hint: "Show golden.", setup: arm,
      check: () => mode === "golden" && isLegalPacking(pack) && !isLegalPacking(BAD_PACK) },
    { id: "touching-ok", title: "Edge touching ok", level: "Stretch",
      prompt: "Golden stays legal (edge-touching allowed, interior overlap not).",
      hint: "Show golden; A touches D along an edge.", setup: arm,
      check: () => mode === "golden" && isLegalPacking(pack) },
  ],
  extraActions(ctx) {
    return [
      el("button", { className: "btn btn-secondary", type: "button", text: "Show bad",
        onClick: () => { pack = clonePack(BAD_PACK); mode = "bad"; ctx.rerender(); } }),
      el("button", { className: "btn btn-primary", type: "button", text: "Show golden",
        onClick: () => { pack = clonePack(GOLDEN_PACK); mode = "golden"; ctx.rerender(); } }),
      el("button", { className: "btn btn-secondary", type: "button", text: "Show overlap",
        onClick: () => { pack = clonePack(OVERLAP_PACK); mode = "overlap"; ctx.rerender(); } }),
    ];
  },
  renderWorkspace(ctx) {
    drawFloorplan(ctx.canvas, { pack: mode === "none" ? {} : pack });
    const rep = mode === "none" ? { legal: null, reason: "none" } : legalityReport(pack);
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock([
      `view: ${mode}`,
      `legal: ${rep.legal}`,
      `reason: ${rep.reason}`,
      `outline: ${OUTLINE.w}×${OUTLINE.h}`,
      `deadspace: ${deadspace()}`,
      `density: ${density().toFixed(4)}`,
    ]));
  },
});

