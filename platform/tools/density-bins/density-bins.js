import {
  GOLDEN_PLACEMENT,
  GOLDENS,
  NETS,
  STARTER_PLACEMENT,
  densityBins,
  totalHpwl,
} from "../../assets/placement-core.js";
import { createInteractivePlacementLab } from "../../assets/interactive-placement-lab.js";
import { el } from "../../assets/placement-ui.js";

const root = document.getElementById("lab-root");
let cap = 1;

function dens(pos) {
  return densityBins(pos, { capacity: cap, nx: 2, ny: 2 });
}

createInteractivePlacementLab(root, {
  initialPositions: STARTER_PLACEMENT,
  revealPositions: GOLDEN_PLACEMENT,
  drawOpts: { grid: 2, showNets: false },
  showPerNetMetrics: false,
  starterHtml: `
    <p><strong>Your job:</strong> move cells across the 2×2 bins on [0,8]². Capacity 1 starter overflow
    <strong>${GOLDENS.density2x2Cap1StarterOverflow}</strong>; compact golden also overflows
    <strong>${GOLDENS.density2x2Cap1GoldenOverflow}</strong> at cap1, and
    <strong>${GOLDENS.density2x2Cap2GoldenOverflow}</strong> at cap2. Toggle Cap 1/2; Check uses your bins.</p>
  `,
  onLoadStarter() {
    cap = 1;
  },
  onChallengeSetup() {
    cap = 1;
  },
  extraActions(ctx) {
    return [
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
  extraMetrics(api) {
    const d = dens(api.getPositions());
    return [
      `capacity: ${cap}`,
      `counts: ${JSON.stringify(d.counts)}`,
      `overflow: ${d.overflow}`,
      `HPWL: ${totalHpwl(NETS, api.getPositions())}`,
    ];
  },
  challenges: [
    {
      id: "starter-ov-2",
      title: "Starter overflow 2",
      level: "Intro",
      prompt: "At cap=1 with starter layout, overflow is 2.",
      hint: "Reset to starter; Cap 1. Bins [[1,1],[2,2]].",
      check: (_c, api) =>
        cap === 1 && dens(api.getPositions()).overflow === GOLDENS.density2x2Cap1StarterOverflow,
    },
    {
      id: "bin-shape",
      title: "Starter 2×2 counts",
      level: "Intro",
      prompt: "Starter counts equal [[1,1],[2,2]].",
      hint: "Reset — do not move cells.",
      check: (_c, api) => JSON.stringify(dens(api.getPositions()).counts) === "[[1,1],[2,2]]",
    },
    {
      id: "golden-bins",
      title: "Golden bins [[3,1],[1,1]]",
      level: "Intro",
      prompt: "Move cells to match golden bin counts [[3,1],[1,1]].",
      hint: "Study Reveal golden, or place A,E,F in the lower-left bin.",
      check: (_c, api) => JSON.stringify(dens(api.getPositions()).counts) === "[[3,1],[1,1]]",
    },
    {
      id: "golden-ov-2",
      title: "Compact overflow 2 @ cap1",
      level: "Practice",
      prompt: "With cap=1, get overflow 2 on a compact-like clustering.",
      hint: "Match golden counts; Cap 1.",
      check: (_c, api) =>
        cap === 1 && dens(api.getPositions()).overflow === GOLDENS.density2x2Cap1GoldenOverflow,
    },
    {
      id: "golden-cap2",
      title: "Overflow 1 @ cap2",
      level: "Practice",
      prompt: "With capacity 2 and golden-like bins, overflow is 1.",
      hint: "Cap 2 + place three cells in one bin (as golden).",
      check: (_c, api) =>
        cap === 2 && dens(api.getPositions()).overflow === GOLDENS.density2x2Cap2GoldenOverflow,
    },
    {
      id: "sum-six",
      title: "Counts sum to 6",
      level: "Practice",
      prompt: "Sum of bin counts is 6.",
      hint: "Always true if all cells are placed.",
      check: (_c, api) => dens(api.getPositions()).counts.flat().reduce((a, b) => a + b, 0) === 6,
    },
    {
      id: "zero-overflow",
      title: "Zero overflow @ cap2",
      level: "Practice",
      prompt: "With Cap 2, spread cells so every bin has ≤2 cells (overflow 0).",
      hint: "Cap 2, then move cells out of crowded bins (e.g. keep at most two per quadrant).",
      check: (_c, api) => cap === 2 && dens(api.getPositions()).overflow === 0,
    },
    {
      id: "nx-ny",
      title: "Grid 2×2",
      level: "Stretch",
      prompt: "densityBins reports nx=2 and ny=2.",
      hint: "Default grid.",
      check: (_c, api) => {
        const d = dens(api.getPositions());
        return d.nx === 2 && d.ny === 2;
      },
    },
    {
      id: "set-cap2",
      title: "Capacity 2 armed",
      level: "Stretch",
      prompt: "Capacity selector is 2.",
      hint: "Cap 2 button.",
      check: () => cap === 2,
    },
    {
      id: "density-vs-wl",
      title: "Density ≠ wirelength",
      level: "Stretch",
      prompt: "Have overflow 2 at cap1 while HPWL ≤ 20 (compact can still overflow).",
      hint: "Build golden-like cluster; Cap 1; HPWL near 14.",
      check: (_c, api) => {
        const pos = api.getPositions();
        return cap === 1 && dens(pos).overflow === 2 && totalHpwl(NETS, pos) <= 20;
      },
    },
  ],
});
