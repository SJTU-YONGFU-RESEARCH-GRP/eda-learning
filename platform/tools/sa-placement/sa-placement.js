import {
  GOLDENS,
  NETS,
  STARTER_PLACEMENT,
  near,
  round1,
  saPlace,
  totalHpwl,
} from "../../assets/placement-core.js";
import { createInteractivePlacementLab } from "../../assets/interactive-placement-lab.js";
import { el } from "../../assets/placement-ui.js";

const root = document.getElementById("lab-root");

/** Last SA run stats (positions live in the lab api). */
let lastSa = null;

createInteractivePlacementLab(root, {
  initialPositions: STARTER_PLACEMENT,
  starterHtml: `
    <p><strong>Your job:</strong> nudge cells yourself or <strong>Apply SA</strong> (seed 42, 60 moves).
    Best HPWL ≈ <strong>${GOLDENS.saHpwlAfter}</strong>
    (accepted ${GOLDENS.saAccepted} / rejected ${GOLDENS.saRejected}). Check uses your positions / last SA stats.</p>
  `,
  onLoadStarter() {
    lastSa = null;
  },
  onChallengeSetup() {
    lastSa = null;
  },
  extraActions(ctx, api) {
    return [
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Apply SA",
        onClick: () => {
          lastSa = saPlace(api.getPositions(), { seed: 42 });
          api.setPositions(lastSa.positions);
          api.setRevealed(false);
          ctx.rerender();
        },
      }),
    ];
  },
  extraMetrics(api) {
    const lines = [
      `HPWL now: ${round1(totalHpwl(NETS, api.getPositions()))}`,
      `target best ≈ ${GOLDENS.saHpwlAfter}`,
    ];
    if (lastSa) {
      lines.push(`best: ${round1(lastSa.hpwl)}  final: ${round1(lastSa.finalHpwl)}`);
      lines.push(`accepted: ${lastSa.accepted}  rejected: ${lastSa.rejected}`);
      lines.push(`history pts: ${lastSa.history.length}`);
    } else {
      lines.push("SA not run yet (optional).");
    }
    return lines;
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
      id: "improved",
      title: "HPWL < 52",
      level: "Intro",
      prompt: "Improve total HPWL below 52 (move or Apply SA).",
      hint: "Apply SA from starter, or pack cells.",
      check: (_c, api) => totalHpwl(NETS, api.getPositions()) < 52,
    },
    {
      id: "best-49-6",
      title: "SA best ≈ 49.6",
      level: "Intro",
      prompt: "Run Apply SA from starter so best HPWL round1 is 49.6.",
      hint: "Reset, then Apply SA (seed 42).",
      check: () => lastSa && near(round1(lastSa.hpwl), GOLDENS.saHpwlAfter, 0.05),
    },
    {
      id: "accepted-44",
      title: "Accepted 44",
      level: "Practice",
      prompt: "After Apply SA from starter, accepted = 44.",
      hint: "Reset then Apply SA.",
      check: () => lastSa && lastSa.accepted === GOLDENS.saAccepted,
    },
    {
      id: "rejected-16",
      title: "Rejected 16",
      level: "Practice",
      prompt: "After Apply SA from starter, rejected = 16.",
      hint: "60 = 44 + 16.",
      check: () => lastSa && lastSa.rejected === GOLDENS.saRejected,
    },
    {
      id: "moves-60",
      title: "60 trials",
      level: "Practice",
      prompt: "accepted + rejected equals 60 after SA.",
      hint: "Default move count.",
      check: () => lastSa && lastSa.accepted + lastSa.rejected === 60,
    },
    {
      id: "history",
      title: "Has history",
      level: "Practice",
      prompt: "SA history has at least 2 snapshots.",
      hint: "Logged every 10 moves.",
      check: () => lastSa && lastSa.history && lastSa.history.length >= 2,
    },
    {
      id: "pos-updated",
      title: "Positions match SA best",
      level: "Stretch",
      prompt: "Workspace positions match last SA best placement.",
      hint: "Apply SA; do not move cells afterward.",
      check: (_c, api) => {
        if (!lastSa) return false;
        const pos = api.getPositions();
        return (
          pos.A.x === lastSa.positions.A.x &&
          pos.B.x === lastSa.positions.B.x &&
          pos.C.y === lastSa.positions.C.y
        );
      },
    },
    {
      id: "above-force",
      title: "Above force 18.7",
      level: "Stretch",
      prompt: "Current HPWL > force-directed 18.7.",
      hint: "Short SA or starter-ish layouts stay above free force.",
      check: (_c, api) => totalHpwl(NETS, api.getPositions()) > GOLDENS.forceHpwlAfter,
    },
    {
      id: "sa-beats-starter",
      title: "SA best < 52",
      level: "Stretch",
      prompt: "Last SA best HPWL is below starter.",
      hint: "Apply SA from starter.",
      check: () => lastSa && lastSa.hpwl < 52,
    },
  ],
});
