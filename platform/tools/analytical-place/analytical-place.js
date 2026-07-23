import {
  CELLS,
  FIXED_PADS,
  GOLDENS,
  NETS,
  STARTER_PLACEMENT,
  analyticalPlace,
  clonePositions,
  densityBins,
  forceDirectedPlace,
  near,
  round1,
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
let mode = "starter"; // starter | force | analytical

function arm() {
  pos = clonePositions(STARTER_PLACEMENT);
  mode = "none";
}

createChallengeLab(root, {
  starterHtml: `
    <p><strong>Starter:</strong> analytical lite = force/quadratic wirelength with pads
    <code>${FIXED_PADS.join(",")}</code>, then density spreading → HPWL ≈
    <strong>${GOLDENS.analyticalHpwlAfter}</strong> (still beats 52).</p>
  `,
  loadStarter() {
    pos = clonePositions(STARTER_PLACEMENT);
    mode = "starter";
  },
  challenges: [
    {
      id: "starter-52",
      title: "Starter 52",
      level: "Intro",
      prompt: "Starter view HPWL is 52.",
      hint: "Show starter / load.",
      setup: arm,
      check: () => mode === "starter" && totalHpwl(NETS, pos) === 52,
    },
    {
      id: "run-anal",
      title: "Run analytical",
      level: "Intro",
      prompt: "Click Run analytical.",
      hint: "Primary button.",
      setup: arm,
      check: () => mode === "analytical",
    },
    {
      id: "after-48-1",
      title: "After ≈ 48.1",
      level: "Intro",
      prompt: "Analytical round1(HPWL) is 48.1.",
      hint: "Default densIters.",
      setup: arm,
      check: () =>
        mode === "analytical" && near(round1(totalHpwl(NETS, pos)), GOLDENS.analyticalHpwlAfter, 0.05),
    },
    {
      id: "beats-starter",
      title: "Beats starter",
      level: "Practice",
      prompt: "Analytical HPWL < 52.",
      hint: "Wirelength stage still helps.",
      setup: arm,
      check: () => mode === "analytical" && totalHpwl(NETS, pos) < 52,
    },
    {
      id: "pads-fixed",
      title: "Pads stay fixed",
      level: "Practice",
      prompt: "After analytical, A and D match starter coords.",
      hint: "FIXED_PADS.",
      setup: arm,
      check: () =>
        mode === "analytical" &&
        pos.A.x === 0 &&
        pos.A.y === 0 &&
        pos.D.x === 8 &&
        pos.D.y === 8,
    },
    {
      id: "vs-force-cluster",
      title: "Less clustered than free force",
      level: "Practice",
      prompt: "Analytical HPWL > free force ≈18.7 (pads + spread).",
      hint: "Compare to force-directed tool.",
      setup: arm,
      check: () =>
        mode === "analytical" && totalHpwl(NETS, pos) > GOLDENS.forceHpwlAfter,
    },
    {
      id: "show-force-stage",
      title: "Force stage alone",
      level: "Practice",
      prompt: "Show force-stage (pads) then confirm mode=force.",
      hint: "Force stage button.",
      setup: arm,
      check: () => mode === "force",
    },
    {
      id: "has-overflow",
      title: "Overflow reported",
      level: "Stretch",
      prompt: "Analytical density overflow (cap 1) is a finite number ≥ 0.",
      hint: "Metrics panel.",
      setup: arm,
      check: () => {
        if (mode !== "analytical") return false;
        const o = densityBins(pos, { capacity: 1 }).overflow;
        return Number.isFinite(o) && o >= 0;
      },
    },
    {
      id: "near-quad",
      title: "Near quadratic 48",
      level: "Stretch",
      prompt: "Analytical HPWL is within 1 of quadratic golden 48.",
      hint: "Spreading keeps WL near the quad solve.",
      setup: arm,
      check: () =>
        mode === "analytical" && near(totalHpwl(NETS, pos), GOLDENS.quadraticHpwlAfter, 1),
    },
    {
      id: "cells-six",
      title: "Six cells placed",
      level: "Stretch",
      prompt: "All six cells have positions after analytical.",
      hint: "Run analytical.",
      setup: arm,
      check: () => mode === "analytical" && CELLS.every((id) => pos[id]),
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
        className: "btn btn-ghost",
        type: "button",
        text: "Force stage",
        onClick: () => {
          pos = forceDirectedPlace(STARTER_PLACEMENT, {
            iters: 6,
            alpha: 0.14,
            centerPull: 0.025,
            fixed: FIXED_PADS,
          });
          mode = "force";
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Run analytical",
        onClick: () => {
          pos = analyticalPlace(STARTER_PLACEMENT);
          mode = "analytical";
          ctx.rerender();
        },
      }),
    ];
  },
  renderWorkspace(ctx) {
    const dens = densityBins(pos, { capacity: 1 });
    drawPlacement(ctx.canvas, CELLS, pos, NETS, {
      grid: 2,
      highlightCells: FIXED_PADS,
    });
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(
      metricsBlock([
        `mode: ${mode}`,
        `HPWL: ${round1(totalHpwl(NETS, pos))}`,
        `overflow(cap1): ${dens.overflow}`,
        `bins: ${JSON.stringify(dens.counts)}`,
        `target ≈ ${GOLDENS.analyticalHpwlAfter}`,
      ])
    );
  },
});
