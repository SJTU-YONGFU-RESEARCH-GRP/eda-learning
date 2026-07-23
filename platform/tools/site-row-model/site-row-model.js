import {
  WIDTHS,
  SITE_W,
  ROW_H,
  N_ROWS,
  CHIP_W,
  CHIP_H,
  ROW_YS,
  GOLDEN_PLACEMENT,
  GOLDENS,
  clonePositions,
  drawLegalization,
  isLegal,
} from "../../assets/legalization-core.js";
import { createChallengeLab, el, metricsBlock } from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let pos = clonePositions(GOLDEN_PLACEMENT);
let mode = "golden";
let shown = true;

function arm() {
  pos = clonePositions(GOLDEN_PLACEMENT);
  mode = "golden";
  shown = false;
}

function run() {
  pos = clonePositions(GOLDEN_PLACEMENT);
  mode = "golden";
  shown = true;
}

const totalCellWidth = Object.values(WIDTHS).reduce((s, w) => s + w, 0);

createChallengeLab(root, {
  starterHtml: `<p><strong>Starter:</strong> legal golden packing on a
    <code>12×6</code> chip with <code>3</code> rows (row height <strong>2</strong>),
    site pitch <strong>1</strong>, total cell width <strong>10</strong>.</p>`,
  loadStarter() { run(); },
  challenges: [
    { id: "show-golden", title: "Show golden", level: "Intro",
      prompt: "Load starter to draw the golden placement.", hint: "Load starter.",
      setup: arm, check: () => shown && mode === "golden" },
    { id: "chip-w", title: "Chip width 12", level: "Intro",
      prompt: "CHIP_W equals 12.", hint: "Site columns.",
      setup: arm, check: () => CHIP_W === 12 && GOLDENS.chipW === 12 },
    { id: "chip-h", title: "Chip height 6", level: "Intro",
      prompt: "CHIP_H equals 6.", hint: "3 rows × rowH 2.",
      setup: arm, check: () => CHIP_H === 6 && GOLDENS.chipH === 6 },
    { id: "n-rows", title: "Three rows", level: "Practice",
      prompt: "N_ROWS is 3.", hint: "ROW_YS length.",
      setup: arm, check: () => N_ROWS === 3 && GOLDENS.nRows === 3 },
    { id: "site-w", title: "Site width 1", level: "Practice",
      prompt: "SITE_W is 1.", hint: "Site pitch.",
      setup: arm, check: () => SITE_W === 1 && GOLDENS.siteW === 1 },
    { id: "row-h", title: "Row height 2", level: "Practice",
      prompt: "ROW_H is 2.", hint: "Uniform row height.",
      setup: arm, check: () => ROW_H === 2 && GOLDENS.rowH === 2 },
    { id: "row-ys", title: "Row Y coords", level: "Practice",
      prompt: "ROW_YS is [0, 2, 4].", hint: "Bottom y of each row.",
      setup: arm, check: () => ROW_YS.join() === "0,2,4" },
    { id: "total-w", title: "Total cell width 10", level: "Stretch",
      prompt: "Sum of cell widths is 10.", hint: "A–F widths.",
      setup: arm, check: () => totalCellWidth === 10 && GOLDENS.totalCellWidth === 10 },
    { id: "width-a", title: "WIDTHS.A = 2", level: "Stretch",
      prompt: "Cell A width is 2 sites.", hint: "WIDTHS.A.",
      setup: arm, check: () => WIDTHS.A === 2 },
    { id: "width-e", title: "WIDTHS.E = 1", level: "Stretch",
      prompt: "Cell E width is 1 site.", hint: "WIDTHS.E.",
      setup: arm, check: () => WIDTHS.E === 1 },
    { id: "golden-legal", title: "Golden legal", level: "Stretch",
      prompt: "Shown golden placement is legal.", hint: "Load starter.",
      setup: arm, check: () => shown && isLegal(pos) && GOLDENS.goldenLegal },
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
    drawLegalization(ctx.canvas, { positions: shown ? pos : {} });
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock([
      `mode: ${mode}`,
      `shown: ${shown}`,
      `chip: ${CHIP_W}×${CHIP_H}`,
      `rows: ${N_ROWS} · site ${SITE_W} · rowH ${ROW_H}`,
      `totalCellWidth: ${totalCellWidth}`,
      `legal: ${shown ? isLegal(pos) : "—"}`,
    ]));
  },
});

