import {
  CELLS,
  GOLDENS,
  NETS,
  STARTER_PLACEMENT,
  clonePositions,
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
let ran = false;

function arm() {
  pos = clonePositions(STARTER_PLACEMENT);
  ran = false;
}

createChallengeLab(root, {
  starterHtml: `
    <p><strong>Starter:</strong> HPWL <strong>${GOLDENS.starterHpwl}</strong>.
    Run force-directed (default 5 iters) → about <strong>${GOLDENS.forceHpwlAfter}</strong>.</p>
  `,
  loadStarter() {
    pos = clonePositions(STARTER_PLACEMENT);
    ran = false;
  },
  challenges: [
    {
      id: "before-52",
      title: "Before = 52",
      level: "Intro",
      prompt: "With starter only (not run), HPWL is 52.",
      hint: "Load starter / Reset.",
      setup: arm,
      check: () => !ran && totalHpwl(NETS, pos) === GOLDENS.starterHpwl,
    },
    {
      id: "run-force",
      title: "Run force",
      level: "Intro",
      prompt: "Click Run force-directed.",
      hint: "Primary button.",
      setup: arm,
      check: () => ran,
    },
    {
      id: "after-18-7",
      title: "After ≈ 18.7",
      level: "Intro",
      prompt: "After run, round1(HPWL) is 18.7.",
      hint: "Default iters/alpha.",
      setup: arm,
      check: () => ran && near(round1(totalHpwl(NETS, pos)), GOLDENS.forceHpwlAfter, 0.05),
    },
    {
      id: "improved",
      title: "Improved vs starter",
      level: "Practice",
      prompt: "After run, HPWL < 52.",
      hint: "Springs pull connected cells together.",
      setup: arm,
      check: () => ran && totalHpwl(NETS, pos) < GOLDENS.starterHpwl,
    },
    {
      id: "drop-gt-30",
      title: "Drop > 30",
      level: "Practice",
      prompt: "HPWL drops by more than 30.",
      hint: "52 − 18.7 ≈ 33.3.",
      setup: arm,
      check: () => ran && GOLDENS.starterHpwl - totalHpwl(NETS, pos) > 30,
    },
    {
      id: "beats-quad",
      title: "Beats quadratic 48",
      level: "Practice",
      prompt: "Force result HPWL < quadratic golden 48.",
      hint: "Force has no fixed pads by default.",
      setup: arm,
      check: () => ran && totalHpwl(NETS, pos) < GOLDENS.quadraticHpwlAfter,
    },
    {
      id: "finite",
      title: "Finite coords",
      level: "Practice",
      prompt: "All cell coords are finite after run.",
      hint: "Run once.",
      setup: arm,
      check: () =>
        ran && CELLS.every((id) => Number.isFinite(pos[id].x) && Number.isFinite(pos[id].y)),
    },
    {
      id: "reset-52",
      title: "Reset restores 52",
      level: "Stretch",
      prompt: "After Reset, HPWL is 52 and ran=false.",
      hint: "Reset button.",
      setup: arm,
      check: () => !ran && totalHpwl(NETS, pos) === 52,
    },
    {
      id: "below-20",
      title: "Below 20",
      level: "Stretch",
      prompt: "After run, HPWL < 20.",
      hint: "≈18.7.",
      setup: arm,
      check: () => ran && totalHpwl(NETS, pos) < 20,
    },
    {
      id: "above-golden",
      title: "Still above golden 14",
      level: "Stretch",
      prompt: "Force result still has HPWL > golden 14.",
      hint: "Lite force does not reach golden.",
      setup: arm,
      check: () => ran && totalHpwl(NETS, pos) > GOLDENS.goldenHpwl,
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
        text: "Run force-directed",
        onClick: () => {
          pos = forceDirectedPlace(STARTER_PLACEMENT);
          ran = true;
          ctx.rerender();
        },
      }),
    ];
  },
  renderWorkspace(ctx) {
    drawPlacement(ctx.canvas, CELLS, pos, NETS);
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(
      metricsBlock([
        `ran: ${ran}`,
        `HPWL: ${round1(totalHpwl(NETS, pos))}`,
        `starter: ${GOLDENS.starterHpwl}`,
        `target ≈ ${GOLDENS.forceHpwlAfter}`,
      ])
    );
  },
});
