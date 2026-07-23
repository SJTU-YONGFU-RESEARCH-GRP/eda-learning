import {
  FIXED_PADS,
  GOLDENS,
  NETS,
  STARTER_PLACEMENT,
  analyticalPlace,
  densityBins,
  forceDirectedPlace,
  near,
  round1,
  totalHpwl,
} from "../../assets/placement-core.js";
import { createInteractivePlacementLab } from "../../assets/interactive-placement-lab.js";
import { el } from "../../assets/placement-ui.js";

const root = document.getElementById("lab-root");

createInteractivePlacementLab(root, {
  initialPositions: STARTER_PLACEMENT,
  lockedIds: FIXED_PADS,
  drawOpts: { grid: 2, highlightCells: FIXED_PADS },
  starterHtml: `
    <p><strong>Your job:</strong> pads <code>${FIXED_PADS.join(",")}</code> locked. Apply force stage,
    full analytical, or nudge free cells. Analytical lite → HPWL ≈
    <strong>${GOLDENS.analyticalHpwlAfter}</strong>.</p>
  `,
  extraActions(ctx, api) {
    return [
      el("button", {
        className: "btn btn-ghost",
        type: "button",
        text: "Apply force stage",
        onClick: () => {
          api.setPositions(
            forceDirectedPlace(api.getPositions(), {
              iters: 6,
              alpha: 0.14,
              centerPull: 0.025,
              fixed: FIXED_PADS,
            })
          );
          api.setRevealed(false);
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Apply analytical",
        onClick: () => {
          api.setPositions(analyticalPlace(api.getPositions(), { fixed: FIXED_PADS }));
          api.setRevealed(false);
          ctx.rerender();
        },
      }),
    ];
  },
  extraMetrics(api) {
    const dens = densityBins(api.getPositions(), { capacity: 1 });
    return [
      `overflow(cap1): ${dens.overflow}`,
      `bins: ${JSON.stringify(dens.counts)}`,
      `target ≈ ${GOLDENS.analyticalHpwlAfter}`,
    ];
  },
  challenges: [
    {
      id: "starter-52",
      title: "Starter 52",
      level: "Intro",
      prompt: "Reset so HPWL is 52.",
      hint: "Reset to starter.",
      check: (_c, api) => totalHpwl(NETS, api.getPositions()) === 52,
    },
    {
      id: "after-48-1",
      title: "After ≈ 48.1",
      level: "Intro",
      prompt: "Reach round1(HPWL) ≈ 48.1 (analytical from starter).",
      hint: "Reset, then Apply analytical.",
      check: (_c, api) =>
        near(round1(totalHpwl(NETS, api.getPositions())), GOLDENS.analyticalHpwlAfter, 0.15),
    },
    {
      id: "beats-starter",
      title: "Beats starter",
      level: "Intro",
      prompt: "HPWL < 52.",
      hint: "Apply analytical or force stage.",
      check: (_c, api) => totalHpwl(NETS, api.getPositions()) < 52,
    },
    {
      id: "pads-fixed",
      title: "Pads stay fixed",
      level: "Practice",
      prompt: "A at (0,0) and D at (8,8).",
      hint: "Pads are locked.",
      check: (_c, api) => {
        const pos = api.getPositions();
        return pos.A.x === 0 && pos.A.y === 0 && pos.D.x === 8 && pos.D.y === 8;
      },
    },
    {
      id: "vs-force-cluster",
      title: "Less clustered than free force",
      level: "Practice",
      prompt: "HPWL > free force ≈18.7 (pads + spread).",
      hint: "Analytical ≈48.1; force stage with pads also stays high.",
      check: (_c, api) => totalHpwl(NETS, api.getPositions()) > GOLDENS.forceHpwlAfter,
    },
    {
      id: "force-stage-hpwl",
      title: "Force stage improves",
      level: "Practice",
      prompt: "After a force stage (pads fixed), HPWL < 52 and pads unchanged.",
      hint: "Reset, Apply force stage.",
      check: (_c, api) => {
        const pos = api.getPositions();
        return (
          totalHpwl(NETS, pos) < 52 &&
          pos.A.x === 0 &&
          pos.A.y === 0 &&
          pos.D.x === 8 &&
          pos.D.y === 8
        );
      },
    },
    {
      id: "has-overflow",
      title: "Overflow reported",
      level: "Practice",
      prompt: "Density overflow (cap 1) is a finite number ≥ 0.",
      hint: "Any placement; read metrics.",
      check: (_c, api) => {
        const o = densityBins(api.getPositions(), { capacity: 1 }).overflow;
        return Number.isFinite(o) && o >= 0;
      },
    },
    {
      id: "near-quad",
      title: "Near quadratic 48",
      level: "Stretch",
      prompt: "HPWL within 1 of quadratic golden 48.",
      hint: "Apply analytical from starter.",
      check: (_c, api) => near(totalHpwl(NETS, api.getPositions()), GOLDENS.quadraticHpwlAfter, 1),
    },
    {
      id: "cells-six",
      title: "Six cells placed",
      level: "Stretch",
      prompt: "All six cells have positions.",
      hint: "Always true after reset / algo.",
      check: (_c, api) => {
        const pos = api.getPositions();
        return ["A", "B", "C", "D", "E", "F"].every((id) => pos[id]);
      },
    },
    {
      id: "improved-with-pads",
      title: "Improved with pads",
      level: "Stretch",
      prompt: "HPWL ≤ 50 with A,D still at starter corners.",
      hint: "Apply analytical.",
      check: (_c, api) => {
        const pos = api.getPositions();
        return (
          totalHpwl(NETS, pos) <= 50 &&
          pos.A.x === 0 &&
          pos.A.y === 0 &&
          pos.D.x === 8 &&
          pos.D.y === 8
        );
      },
    },
  ],
});
