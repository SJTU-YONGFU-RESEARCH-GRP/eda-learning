import {
  CELLS,
  FIXED_PADS,
  GOLDENS,
  NETS,
  STARTER_PLACEMENT,
  clonePositions,
  near,
  quadraticPlace,
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
let ran = false;

function arm() {
  pos = clonePositions(STARTER_PLACEMENT);
  ran = false;
}

createChallengeLab(root, {
  starterHtml: `
    <p><strong>Starter:</strong> HPWL <strong>52</strong>. Quadratic lite with pads
    <code>${FIXED_PADS.join(",")}</code> fixed → HPWL <strong>${GOLDENS.quadraticHpwlAfter}</strong>.</p>
  `,
  loadStarter() {
    arm();
  },
  challenges: [
    {
      id: "before-52",
      title: "Before = 52",
      level: "Intro",
      prompt: "Starter HPWL is 52 before solve.",
      hint: "Reset / load starter.",
      setup: arm,
      check: () => !ran && totalHpwl(NETS, pos) === 52,
    },
    {
      id: "run-quad",
      title: "Run quadratic",
      level: "Intro",
      prompt: "Click Run quadratic.",
      hint: "Primary button.",
      setup: arm,
      check: () => ran,
    },
    {
      id: "after-48",
      title: "After = 48",
      level: "Intro",
      prompt: "After solve, HPWL is 48.",
      hint: "Default blend/iters with pads A,D.",
      setup: arm,
      check: () => ran && near(totalHpwl(NETS, pos), GOLDENS.quadraticHpwlAfter, 0.05),
    },
    {
      id: "pads-fixed-a",
      title: "Pad A fixed",
      level: "Practice",
      prompt: "After solve, A stays at starter (0,0).",
      hint: "FIXED_PADS includes A.",
      setup: arm,
      check: () =>
        ran && pos.A.x === STARTER_PLACEMENT.A.x && pos.A.y === STARTER_PLACEMENT.A.y,
    },
    {
      id: "pads-fixed-d",
      title: "Pad D fixed",
      level: "Practice",
      prompt: "After solve, D stays at starter (8,8).",
      hint: "FIXED_PADS includes D.",
      setup: arm,
      check: () =>
        ran && pos.D.x === STARTER_PLACEMENT.D.x && pos.D.y === STARTER_PLACEMENT.D.y,
    },
    {
      id: "improved",
      title: "Improved",
      level: "Practice",
      prompt: "HPWL after < 52.",
      hint: "Free cells move toward neighbors.",
      setup: arm,
      check: () => ran && totalHpwl(NETS, pos) < 52,
    },
    {
      id: "worse-than-force",
      title: "Higher than force",
      level: "Practice",
      prompt: "Quadratic HPWL > force golden 18.7 (pads constrain).",
      hint: "Fixed corners keep span large.",
      setup: arm,
      check: () => ran && totalHpwl(NETS, pos) > GOLDENS.forceHpwlAfter,
    },
    {
      id: "b-moved",
      title: "B moved",
      level: "Stretch",
      prompt: "Cell B is no longer at (8,0).",
      hint: "B is free.",
      setup: arm,
      check: () =>
        ran && (pos.B.x !== STARTER_PLACEMENT.B.x || pos.B.y !== STARTER_PLACEMENT.B.y),
    },
    {
      id: "two-pads",
      title: "Two pads",
      level: "Stretch",
      prompt: "FIXED_PADS has exactly A and D.",
      hint: "Export list.",
      setup: arm,
      check: () => FIXED_PADS.join(",") === "A,D",
    },
    {
      id: "drop-4",
      title: "Drop of ~4",
      level: "Stretch",
      prompt: "HPWL drops by about 4 (52→48).",
      hint: "Run quadratic.",
      setup: arm,
      check: () => ran && near(GOLDENS.starterHpwl - totalHpwl(NETS, pos), 4, 0.05),
    },
  ],
  extraActions(ctx) {
    return [
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: "Reset",
        onClick: () => {
          arm();
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Run quadratic",
        onClick: () => {
          pos = quadraticPlace(STARTER_PLACEMENT);
          ran = true;
          ctx.rerender();
        },
      }),
    ];
  },
  renderWorkspace(ctx) {
    drawPlacement(ctx.canvas, CELLS, pos, NETS, { highlightCells: FIXED_PADS });
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(
      metricsBlock([
        `ran: ${ran}`,
        `fixed pads: ${FIXED_PADS.join(",")}`,
        `HPWL: ${round1(totalHpwl(NETS, pos))}`,
        `A: (${pos.A.x}, ${pos.A.y})  D: (${pos.D.x}, ${pos.D.y})`,
      ])
    );
  },
});
