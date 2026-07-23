import {
  GOLDENS,
  NETS,
  STARTER_PLACEMENT,
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
  starterHtml: `
    <p><strong>Your job:</strong> improve wirelength by moving cells and/or applying force steps.
    Starter HPWL <strong>${GOLDENS.starterHpwl}</strong>; default force-directed → about
    <strong>${GOLDENS.forceHpwlAfter}</strong>. Check scores your positions.</p>
  `,
  extraActions(ctx, api) {
    return [
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Apply force step",
        onClick: () => {
          api.setPositions(forceDirectedPlace(api.getPositions()));
          api.setRevealed(false);
          ctx.rerender();
        },
      }),
    ];
  },
  extraMetrics() {
    return [`target ≈ ${GOLDENS.forceHpwlAfter}`, `starter: ${GOLDENS.starterHpwl}`];
  },
  challenges: [
    {
      id: "before-52",
      title: "Before = 52",
      level: "Intro",
      prompt: "Reset so total HPWL is 52 (starter).",
      hint: "Reset to starter — do not apply force yet.",
      check: (_c, api) => totalHpwl(NETS, api.getPositions()) === GOLDENS.starterHpwl,
    },
    {
      id: "improved",
      title: "HPWL under 52",
      level: "Intro",
      prompt: "Move cells or Apply force step until HPWL < 52.",
      hint: "One force step from starter already helps.",
      check: (_c, api) => totalHpwl(NETS, api.getPositions()) < GOLDENS.starterHpwl,
    },
    {
      id: "after-18-7",
      title: "Near force ≈ 18.7",
      level: "Intro",
      prompt: "Reach round1(HPWL) ≈ 18.7 (default force from starter).",
      hint: "Reset, then Apply force step once (from starter positions).",
      check: (_c, api) =>
        near(round1(totalHpwl(NETS, api.getPositions())), GOLDENS.forceHpwlAfter, 0.15),
    },
    {
      id: "drop-gt-30",
      title: "Drop > 30",
      level: "Practice",
      prompt: "Cut more than 30 HPWL vs starter 52.",
      hint: "Apply force from starter, or pack cells tightly.",
      check: (_c, api) => GOLDENS.starterHpwl - totalHpwl(NETS, api.getPositions()) > 30,
    },
    {
      id: "beats-quad",
      title: "Beats quadratic 48",
      level: "Practice",
      prompt: "Your HPWL < 48.",
      hint: "Force or manual compact both beat fixed-pad quadratic.",
      check: (_c, api) => totalHpwl(NETS, api.getPositions()) < GOLDENS.quadraticHpwlAfter,
    },
    {
      id: "below-20",
      title: "Below 20",
      level: "Practice",
      prompt: "Total HPWL < 20.",
      hint: "Apply force step from starter.",
      check: (_c, api) => totalHpwl(NETS, api.getPositions()) < 20,
    },
    {
      id: "above-golden",
      title: "Still above golden 14",
      level: "Practice",
      prompt: "Have an improved placement with HPWL > 14 (lite force territory).",
      hint: "Apply force once — ≈18.7 is above 14.",
      check: (_c, api) => {
        const h = totalHpwl(NETS, api.getPositions());
        return h < GOLDENS.starterHpwl && h > GOLDENS.goldenHpwl;
      },
    },
    {
      id: "finite",
      title: "Finite coords",
      level: "Stretch",
      prompt: "All cell coords are finite.",
      hint: "Any valid move / force result.",
      check: (_c, api) => {
        const pos = api.getPositions();
        return ["A", "B", "C", "D", "E", "F"].every(
          (id) => pos[id] && Number.isFinite(pos[id].x) && Number.isFinite(pos[id].y)
        );
      },
    },
    {
      id: "manual-or-force",
      title: "HPWL ≤ 25",
      level: "Stretch",
      prompt: "Reach total HPWL ≤ 25 by hand or with force.",
      hint: "Force from starter lands near 18.7.",
      check: (_c, api) => totalHpwl(NETS, api.getPositions()) <= 25,
    },
    {
      id: "reset-52",
      title: "Reset restores 52",
      level: "Stretch",
      prompt: "After Reset to starter, HPWL is again 52.",
      hint: "Use Reset to starter.",
      check: (_c, api) => totalHpwl(NETS, api.getPositions()) === 52,
    },
  ],
});
