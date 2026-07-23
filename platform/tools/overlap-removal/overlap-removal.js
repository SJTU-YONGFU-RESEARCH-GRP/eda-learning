import {
  OVERLAP_PLACEMENT,
  GOLDENS,
  clonePositions,
  drawLegalization,
  isLegal,
  overlapRemoval,
  totalDisplacement,
  totalHpwl,
} from "../../assets/legalization-core.js";
import { createChallengeLab, el, metricsBlock } from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let origin = clonePositions(OVERLAP_PLACEMENT);
let pos = clonePositions(OVERLAP_PLACEMENT);
let ran = false;

function arm() {
  origin = clonePositions(OVERLAP_PLACEMENT);
  pos = clonePositions(OVERLAP_PLACEMENT);
  ran = false;
}

function run() {
  pos = overlapRemoval(origin);
  ran = true;
}

createChallengeLab(root, {
  starterHtml: `<p><strong>Starter:</strong> overlap seed on middle row.
    Overlap removal snaps then packs left within rows → legal, disp <strong>6</strong>, HPWL <strong>32</strong>.</p>`,
  loadStarter() { arm(); run(); },
  challenges: [
    { id: "run", title: "Run overlap removal", level: "Intro",
      prompt: "Run algorithm on overlap starter.", hint: "Run algorithm.",
      setup: arm, check: () => ran },
    { id: "legal", title: "Result legal", level: "Intro",
      prompt: "Resulting placement is legal.", hint: "Run first.",
      setup: arm, check: () => ran && isLegal(pos) },
    { id: "disp-6", title: "Displacement 6", level: "Intro",
      prompt: "Total displacement is 6.", hint: "Run first.",
      setup: arm, check: () => ran && totalDisplacement(origin, pos) === GOLDENS.overlapRemovalDisp },
    { id: "hpwl-32", title: "HPWL 32", level: "Practice",
      prompt: "HPWL is 32.", hint: "Run first.",
      setup: arm, check: () => ran && totalHpwl(pos) === GOLDENS.overlapRemovalHpwl },
    { id: "b-at-6", title: "B moves to x=6", level: "Practice",
      prompt: "B ends at x=6 on row y=2.", hint: "Run overlap removal.",
      setup: arm, check: () => ran && pos.B.x === 6 && pos.B.y === 2 },
    { id: "c-at-8", title: "C moves to x=8", level: "Practice",
      prompt: "C ends at x=8 on row y=2.", hint: "Run overlap removal.",
      setup: arm, check: () => ran && pos.C.x === 8 && pos.C.y === 2 },
    { id: "a-stays", title: "A stays at 4", level: "Practice",
      prompt: "A remains at x=4, y=2.", hint: "Run overlap removal.",
      setup: arm, check: () => ran && pos.A.x === 4 && pos.A.y === 2 },
    { id: "d-fixed", title: "D unchanged", level: "Stretch",
      prompt: "D stays at (8,4).", hint: "Run overlap removal.",
      setup: arm, check: () => ran && pos.D.x === 8 && pos.D.y === 4 },
    { id: "golden-disp", title: "Matches GOLDENS disp", level: "Stretch",
      prompt: "Displacement equals GOLDENS.overlapRemovalDisp (6).", hint: "Run first.",
      setup: arm, check: () => ran && totalDisplacement(origin, pos) === 6 },
    { id: "golden-hpwl", title: "Matches GOLDENS hpwl", level: "Stretch",
      prompt: "HPWL equals GOLDENS.overlapRemovalHpwl (32).", hint: "Run first.",
      setup: arm, check: () => ran && totalHpwl(pos) === 32 },
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
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock([
      `ran: ${ran}`,
      `legal: ${ran ? isLegal(pos) : "—"}`,
      `disp: ${ran ? totalDisplacement(origin, pos) : "—"}`,
      `hpwl: ${ran ? totalHpwl(pos) : "—"}`,
    ]));
  },
});

