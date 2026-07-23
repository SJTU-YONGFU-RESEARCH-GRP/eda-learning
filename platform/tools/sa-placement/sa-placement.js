import {
  CELLS,
  GOLDENS,
  NETS,
  STARTER_PLACEMENT,
  clonePositions,
  near,
  round1,
  saPlace,
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
let result = null;

function arm() {
  pos = clonePositions(STARTER_PLACEMENT);
  result = null;
}

createChallengeLab(root, {
  starterHtml: `
    <p><strong>Starter:</strong> HPWL <strong>52</strong>. SA with seed 42 (60 moves)
    keeps best HPWL ≈ <strong>${GOLDENS.saHpwlAfter}</strong>
    (accepted ${GOLDENS.saAccepted} / rejected ${GOLDENS.saRejected}).</p>
  `,
  loadStarter() {
    arm();
  },
  challenges: [
    {
      id: "before-52",
      title: "Before = 52",
      level: "Intro",
      prompt: "Starter HPWL is 52 before SA.",
      hint: "Reset.",
      setup: arm,
      check: () => !result && totalHpwl(NETS, pos) === 52,
    },
    {
      id: "run-sa",
      title: "Run SA",
      level: "Intro",
      prompt: "Click Run SA.",
      hint: "Primary button.",
      setup: arm,
      check: () => !!result,
    },
    {
      id: "best-49-6",
      title: "Best ≈ 49.6",
      level: "Intro",
      prompt: "Best HPWL round1 is 49.6.",
      hint: "seed=42 defaults.",
      setup: arm,
      check: () => result && near(round1(result.hpwl), GOLDENS.saHpwlAfter, 0.05),
    },
    {
      id: "improved",
      title: "Best < 52",
      level: "Practice",
      prompt: "SA best HPWL is below starter.",
      hint: "Accept improving moves.",
      setup: arm,
      check: () => result && result.hpwl < 52,
    },
    {
      id: "accepted-44",
      title: "Accepted 44",
      level: "Practice",
      prompt: "SA reports accepted = 44.",
      hint: "Metrics after Run SA.",
      setup: arm,
      check: () => result && result.accepted === GOLDENS.saAccepted,
    },
    {
      id: "rejected-16",
      title: "Rejected 16",
      level: "Practice",
      prompt: "SA reports rejected = 16.",
      hint: "60 = 44 + 16.",
      setup: arm,
      check: () => result && result.rejected === GOLDENS.saRejected,
    },
    {
      id: "moves-60",
      title: "60 trials",
      level: "Practice",
      prompt: "accepted + rejected equals 60.",
      hint: "Default move count.",
      setup: arm,
      check: () => result && result.accepted + result.rejected === 60,
    },
    {
      id: "history",
      title: "Has history",
      level: "Stretch",
      prompt: "Result history has at least 2 snapshots.",
      hint: "Logged every 10 moves.",
      setup: arm,
      check: () => result && result.history && result.history.length >= 2,
    },
    {
      id: "pos-updated",
      title: "Positions updated",
      level: "Stretch",
      prompt: "Displayed placement matches result.positions.",
      hint: "After Run SA.",
      setup: arm,
      check: () =>
        !!result &&
        pos.A.x === result.positions.A.x &&
        pos.B.x === result.positions.B.x &&
        pos.C.y === result.positions.C.y,
    },
    {
      id: "above-force",
      title: "Above force 18.7",
      level: "Stretch",
      prompt: "Few SA moves stay above force-directed 18.7.",
      hint: "Short anneal is a lite demo.",
      setup: arm,
      check: () => result && result.hpwl > GOLDENS.forceHpwlAfter,
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
        text: "Run SA",
        onClick: () => {
          result = saPlace(STARTER_PLACEMENT);
          pos = result.positions;
          ctx.rerender();
        },
      }),
    ];
  },
  renderWorkspace(ctx) {
    drawPlacement(ctx.canvas, CELLS, pos, NETS);
    const lines = [
      `HPWL now: ${round1(totalHpwl(NETS, pos))}`,
      `starter: 52  target best ≈ ${GOLDENS.saHpwlAfter}`,
    ];
    if (result) {
      lines.push(`best: ${round1(result.hpwl)}  final: ${round1(result.finalHpwl)}`);
      lines.push(`accepted: ${result.accepted}  rejected: ${result.rejected}`);
      lines.push(`history pts: ${result.history.length}`);
    } else {
      lines.push("SA not run yet.");
    }
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock(lines));
  },
});
