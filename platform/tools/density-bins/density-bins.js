import {
  CELLS,
  GOLDEN_PLACEMENT,
  GOLDENS,
  NETS,
  STARTER_PLACEMENT,
  clonePositions,
  densityBins,
  totalHpwl,
} from "../../assets/placement-core.js";
import {
  createChallengeLab,
  drawPlacement,
  el,
  metricsBlock,
} from "../../assets/placement-ui.js";

const root = document.getElementById("lab-root");
let pos = clonePositions(STARTER_PLACEMENT);
let mode = "starter";
let cap = 1;

function arm() {
  pos = clonePositions(STARTER_PLACEMENT);
  mode = "none";
  cap = 1;
}

function dens() {
  return densityBins(pos, { capacity: cap, nx: 2, ny: 2 });
}

createChallengeLab(root, {
  starterHtml: `
    <p><strong>Starter:</strong> 2×2 bins on [0,8]². With capacity 1, starter overflow is
    <strong>${GOLDENS.density2x2Cap1StarterOverflow}</strong>; golden also
    <strong>${GOLDENS.density2x2Cap1GoldenOverflow}</strong> (clustered in one bin).
    Capacity 2 on golden → overflow <strong>${GOLDENS.density2x2Cap2GoldenOverflow}</strong>.</p>
  `,
  loadStarter() {
    pos = clonePositions(STARTER_PLACEMENT);
    mode = "starter";
    cap = 1;
  },
  challenges: [
    {
      id: "starter-ov-2",
      title: "Starter overflow 2",
      level: "Intro",
      prompt: "Starter with cap=1 has overflow 2.",
      hint: "Show starter; bins [[1,1],[2,2]].",
      setup: arm,
      check: () =>
        mode === "starter" &&
        cap === 1 &&
        dens().overflow === GOLDENS.density2x2Cap1StarterOverflow,
    },
    {
      id: "golden-ov-2",
      title: "Golden overflow 2",
      level: "Intro",
      prompt: "Golden with cap=1 has overflow 2.",
      hint: "Three cells share bin (0,0).",
      setup: arm,
      check: () =>
        mode === "golden" &&
        cap === 1 &&
        dens().overflow === GOLDENS.density2x2Cap1GoldenOverflow,
    },
    {
      id: "golden-cap2",
      title: "Golden cap2 → 1",
      level: "Intro",
      prompt: "Golden with capacity 2 has overflow 1.",
      hint: "Set cap 2 + show golden.",
      setup: arm,
      check: () =>
        mode === "golden" &&
        cap === 2 &&
        dens().overflow === GOLDENS.density2x2Cap2GoldenOverflow,
    },
    {
      id: "bin-shape",
      title: "2×2 counts",
      level: "Practice",
      prompt: "Starter counts equal [[1,1],[2,2]].",
      hint: "Show starter.",
      setup: arm,
      check: () =>
        mode === "starter" && JSON.stringify(dens().counts) === "[[1,1],[2,2]]",
    },
    {
      id: "golden-bins",
      title: "Golden bins",
      level: "Practice",
      prompt: "Golden counts equal [[3,1],[1,1]].",
      hint: "A,E,F in lower-left bin.",
      setup: arm,
      check: () =>
        mode === "golden" && JSON.stringify(dens().counts) === "[[3,1],[1,1]]",
    },
    {
      id: "sum-six",
      title: "Counts sum to 6",
      level: "Practice",
      prompt: "Sum of bin counts is always 6.",
      hint: "One cell per placement entry.",
      setup: arm,
      check: () => {
        if (mode !== "starter" && mode !== "golden") return false;
        const c = dens().counts.flat().reduce((a, b) => a + b, 0);
        return c === 6;
      },
    },
    {
      id: "cap1-same-ov",
      title: "Same overflow ≠ same WL",
      level: "Practice",
      prompt: "Both views overflow 2 at cap1, but starter HPWL is 52 and golden 14.",
      hint: "Density alone does not rank wirelength.",
      setup: arm,
      check: () => {
        const s = densityBins(STARTER_PLACEMENT, { capacity: 1 }).overflow;
        const g = densityBins(GOLDEN_PLACEMENT, { capacity: 1 }).overflow;
        return (
          (mode === "starter" || mode === "golden") &&
          s === 2 &&
          g === 2 &&
          totalHpwl(NETS, STARTER_PLACEMENT) === 52 &&
          totalHpwl(NETS, GOLDEN_PLACEMENT) === 14
        );
      },
    },
    {
      id: "nx-ny",
      title: "Grid 2×2",
      level: "Stretch",
      prompt: "densityBins reports nx=2 and ny=2.",
      hint: "Default grid.",
      setup: arm,
      check: () => {
        if (mode !== "starter" && mode !== "golden") return false;
        const d = dens();
        return d.nx === 2 && d.ny === 2;
      },
    },
    {
      id: "set-cap2",
      title: "Capacity 2 armed",
      level: "Stretch",
      prompt: "Capacity selector is 2 (and a view is shown).",
      hint: "Cap 2 button.",
      setup: arm,
      check: () => cap === 2 && (mode === "starter" || mode === "golden"),
    },
    {
      id: "overflow-formula",
      title: "Overflow formula",
      level: "Stretch",
      prompt: "overflow === sum max(0, count−cap) on golden cap2 → 1.",
      hint: "Only the bin with 3 cells overflows by 1.",
      setup: arm,
      check: () =>
        mode === "golden" &&
        cap === 2 &&
        dens().overflow === 1,
    },
  ],
  extraActions(ctx) {
    return [
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: "Show starter",
        onClick: () => {
          pos = clonePositions(STARTER_PLACEMENT);
          mode = "starter";
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Show golden",
        onClick: () => {
          pos = clonePositions(GOLDEN_PLACEMENT);
          mode = "golden";
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-ghost",
        type: "button",
        text: "Cap 1",
        onClick: () => {
          cap = 1;
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-ghost",
        type: "button",
        text: "Cap 2",
        onClick: () => {
          cap = 2;
          ctx.rerender();
        },
      }),
    ];
  },
  renderWorkspace(ctx) {
    const d = dens();
    drawPlacement(ctx.canvas, CELLS, pos, NETS, { grid: 2, showNets: false });
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(
      metricsBlock([
        `view: ${mode}  capacity: ${cap}`,
        `counts: ${JSON.stringify(d.counts)}`,
        `overflow: ${d.overflow}`,
        `HPWL: ${totalHpwl(NETS, pos)}`,
      ])
    );
  },
});
