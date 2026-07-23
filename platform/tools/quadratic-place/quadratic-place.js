import {
  FIXED_PADS,
  GOLDENS,
  NETS,
  STARTER_PLACEMENT,
  near,
  quadraticPlace,
  round1,
  totalHpwl,
} from "../../assets/placement-core.js";
import { createInteractivePlacementLab } from "../../assets/interactive-placement-lab.js";
import { el } from "../../assets/placement-ui.js";

const root = document.getElementById("lab-root");

createInteractivePlacementLab(root, {
  initialPositions: STARTER_PLACEMENT,
  lockedIds: FIXED_PADS,
  drawOpts: { highlightCells: FIXED_PADS },
  starterHtml: `
    <p><strong>Your job:</strong> pads <code>${FIXED_PADS.join(",")}</code> are locked.
    Move free cells or <strong>Apply quadratic</strong> (Gauss–Seidel average). Starter 52 →
    quadratic lite <strong>${GOLDENS.quadraticHpwlAfter}</strong>.</p>
  `,
  extraActions(ctx, api) {
    return [
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Apply quadratic",
        onClick: () => {
          api.setPositions(quadraticPlace(api.getPositions(), { fixed: FIXED_PADS }));
          api.setRevealed(false);
          ctx.rerender();
        },
      }),
    ];
  },
  extraMetrics(api) {
    const pos = api.getPositions();
    return [
      `fixed pads: ${FIXED_PADS.join(",")}`,
      `A: (${pos.A.x}, ${pos.A.y})  D: (${pos.D.x}, ${pos.D.y})`,
      `target: ${GOLDENS.quadraticHpwlAfter}`,
    ];
  },
  challenges: [
    {
      id: "before-52",
      title: "Before = 52",
      level: "Intro",
      prompt: "Starter HPWL is 52.",
      hint: "Reset to starter.",
      check: (_c, api) => totalHpwl(NETS, api.getPositions()) === 52,
    },
    {
      id: "after-48",
      title: "HPWL = 48",
      level: "Intro",
      prompt: "Reach HPWL 48 (default quadratic from starter).",
      hint: "Reset, then Apply quadratic.",
      check: (_c, api) => near(totalHpwl(NETS, api.getPositions()), GOLDENS.quadraticHpwlAfter, 0.05),
    },
    {
      id: "pads-fixed-a",
      title: "Pad A fixed",
      level: "Intro",
      prompt: "A stays at starter (0,0).",
      hint: "A is locked — Apply quadratic or nudge free cells only.",
      check: (_c, api) => {
        const pos = api.getPositions();
        return pos.A.x === STARTER_PLACEMENT.A.x && pos.A.y === STARTER_PLACEMENT.A.y;
      },
    },
    {
      id: "pads-fixed-d",
      title: "Pad D fixed",
      level: "Practice",
      prompt: "D stays at starter (8,8).",
      hint: "D is locked.",
      check: (_c, api) => {
        const pos = api.getPositions();
        return pos.D.x === STARTER_PLACEMENT.D.x && pos.D.y === STARTER_PLACEMENT.D.y;
      },
    },
    {
      id: "improved",
      title: "Improved",
      level: "Practice",
      prompt: "HPWL < 52 with pads still fixed.",
      hint: "Apply quadratic or move B/C/E/F inward.",
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
      id: "worse-than-force",
      title: "Higher than force",
      level: "Practice",
      prompt: "HPWL > force golden 18.7 (pads keep span large).",
      hint: "Quadratic result ≈48; or any lightly improved layout.",
      check: (_c, api) => totalHpwl(NETS, api.getPositions()) > GOLDENS.forceHpwlAfter,
    },
    {
      id: "b-moved",
      title: "B moved",
      level: "Practice",
      prompt: "Cell B is no longer at (8,0).",
      hint: "Apply quadratic or select B and move it.",
      check: (_c, api) => {
        const pos = api.getPositions();
        return pos.B.x !== STARTER_PLACEMENT.B.x || pos.B.y !== STARTER_PLACEMENT.B.y;
      },
    },
    {
      id: "drop-4",
      title: "Drop of ~4",
      level: "Stretch",
      prompt: "HPWL drops by about 4 from 52 (→48).",
      hint: "Apply quadratic from starter.",
      check: (_c, api) => near(GOLDENS.starterHpwl - totalHpwl(NETS, api.getPositions()), 4, 0.15),
    },
    {
      id: "two-pads",
      title: "Two pads",
      level: "Stretch",
      prompt: "FIXED_PADS is exactly A,D.",
      hint: "Instance constant.",
      check: () => FIXED_PADS.join(",") === "A,D",
    },
    {
      id: "round-48",
      title: "round1 shows 48",
      level: "Stretch",
      prompt: "round1(HPWL) is 48.",
      hint: "Apply quadratic from starter.",
      check: (_c, api) => round1(totalHpwl(NETS, api.getPositions())) === 48,
    },
  ],
});
