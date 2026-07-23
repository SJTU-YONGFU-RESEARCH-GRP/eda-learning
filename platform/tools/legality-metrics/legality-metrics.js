import {
  OVERLAP_PLACEMENT,
  GOLDEN_PLACEMENT,
  GOLDENS,
  clonePositions,
  drawLegalization,
  isLegal,
  legalityReport,
} from "../../assets/legalization-core.js";
import { createChallengeLab, el, metricsBlock } from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let pos = clonePositions(OVERLAP_PLACEMENT);
let mode = "overlap";

function arm() {
  pos = clonePositions(OVERLAP_PLACEMENT);
  mode = "overlap";
}

function run() {
  pos = clonePositions(GOLDEN_PLACEMENT);
  mode = "golden";
}

createChallengeLab(root, {
  starterHtml: `<p><strong>Starter:</strong> illegal overlap seed (A/B/C stacked).
    Golden reference is legal. Toggle views and read <code>legalityReport</code>.</p>`,
  loadStarter() { arm(); },
  challenges: [
    { id: "show-overlap", title: "Show overlap", level: "Intro",
      prompt: "Load starter (overlap seed).", hint: "Load starter.",
      setup: arm, check: () => mode === "overlap" },
    { id: "overlap-illegal", title: "Overlap illegal", level: "Intro",
      prompt: "Overlap placement is not legal.", hint: "Load starter.",
      setup: arm, check: () => mode === "overlap" && !isLegal(pos) && GOLDENS.overlapIllegal },
    { id: "overlap-reason", title: "Overlap reason", level: "Intro",
      prompt: "Overlap report reason includes 'overlap'.", hint: "A/B overlap.",
      setup: arm, check: () => mode === "overlap" && legalityReport(pos).reason.includes("overlap") },
    { id: "show-golden", title: "Show golden", level: "Practice",
      prompt: "Run algorithm (show golden).", hint: "Run algorithm.",
      setup: arm, check: () => mode === "golden" },
    { id: "golden-legal", title: "Golden legal", level: "Practice",
      prompt: "Golden placement is legal.", hint: "Run algorithm.",
      setup: arm, check: () => mode === "golden" && isLegal(pos) && GOLDENS.goldenLegal },
    { id: "golden-ok", title: "Golden reason ok", level: "Practice",
      prompt: "Golden report reason is 'ok'.", hint: "Run algorithm.",
      setup: arm, check: () => mode === "golden" && legalityReport(pos).reason === "ok" },
    { id: "site-aligned", title: "Golden site-aligned", level: "Practice",
      prompt: "Golden has no site-alignment violations.", hint: "Run algorithm.",
      setup: arm, check: () => {
        if (mode !== "golden") return false;
        return !legalityReport(pos).reasons.some((r) => r.includes("site-aligned"));
      } },
    { id: "on-row", title: "Golden on rows", level: "Stretch",
      prompt: "Golden has no off-row violations.", hint: "Run algorithm.",
      setup: arm, check: () => {
        if (mode !== "golden") return false;
        return !legalityReport(pos).reasons.some((r) => r.includes("not on a row"));
      } },
    { id: "overlap-ab", title: "Overlap A/B cited", level: "Stretch",
      prompt: "Overlap reasons include A/B.", hint: "Load starter.",
      setup: arm, check: () => mode === "overlap" && legalityReport(pos).reasons.some((r) => r.includes("A/B")) },
    { id: "differs", title: "Golden differs", level: "Stretch",
      prompt: "Golden A.x differs from overlap A.x.", hint: "Compare views.",
      setup: arm, check: () => mode === "golden" && pos.A.x !== OVERLAP_PLACEMENT.A.x },
  ],
  extraActions(ctx) {
    return [
      el("button", { className: "btn btn-secondary", type: "button", text: "Load starter",
        onClick: () => { arm(); ctx.rerender(); } }),
      el("button", { className: "btn btn-primary", type: "button", text: "Run algorithm",
        onClick: () => { run(); ctx.rerender(); } }),
    ];
  },
  renderWorkspace(ctx) {
    drawLegalization(ctx.canvas, { positions: pos });
    const rep = legalityReport(pos);
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock([
      `mode: ${mode}`,
      `legal: ${rep.legal}`,
      `reason: ${rep.reason}`,
      `violations: ${rep.reasons.length}`,
    ]));
  },
});

