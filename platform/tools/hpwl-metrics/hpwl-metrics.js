import {
  GOLDEN_PLACEMENT,
  GOLDENS,
  NETS,
  STARTER_PLACEMENT,
  hpwl,
  near,
  totalHpwl,
} from "../../assets/placement-core.js";
import {
  createInteractivePlacementLab,
  positionsNear,
} from "../../assets/interactive-placement-lab.js";

const root = document.getElementById("lab-root");

createInteractivePlacementLab(root, {
  initialPositions: STARTER_PLACEMENT,
  revealPositions: GOLDEN_PLACEMENT,
  starterHtml: `
    <p><strong>Your job:</strong> move cells to change wirelength. Starter total HPWL is
    <strong>${GOLDENS.starterHpwl}</strong>; a compact placement reaches
    <strong>${GOLDENS.goldenHpwl}</strong>. Challenges check <em>your</em> positions — Reveal golden is study-only.</p>
  `,
  challenges: [
    {
      id: "starter-52",
      title: "Starter HPWL 52",
      level: "Intro",
      prompt: "With the workspace at starter (reset if needed), total HPWL must be 52.",
      hint: "Click Reset to starter — do not move cells yet.",
      check: (_c, api) => totalHpwl(NETS, api.getPositions()) === GOLDENS.starterHpwl,
    },
    {
      id: "net0-starter",
      title: "Net AB = 8",
      level: "Intro",
      prompt: "Keep starter layout so HPWL of net [A,B] is 8.",
      hint: "A(0,0) B(8,0) → span 8.",
      check: (_c, api) => hpwl(NETS[0], api.getPositions()) === 8,
    },
    {
      id: "net4-starter",
      title: "4-pin starter = 16",
      level: "Intro",
      prompt: "On starter (or any 8×8 ABCD bbox), 4-pin net ABCD has HPWL 16.",
      hint: "Reset workspace; bbox half-perimeter 8+8.",
      check: (_c, api) => hpwl(NETS[4], api.getPositions()) === 16,
    },
    {
      id: "below-40",
      title: "HPWL under 40",
      level: "Practice",
      prompt: "Move cells so total HPWL is strictly less than 40.",
      hint: "Pull B and D left, or C and D down toward the center.",
      check: (_c, api) => totalHpwl(NETS, api.getPositions()) < 40,
    },
    {
      id: "abcd-le-6",
      title: "ABCD ≤ 6",
      level: "Practice",
      prompt: "Shrink the ABCD net bbox so its HPWL is ≤ 6.",
      hint: "Place A,B,C,D inside a 3×3 box (half-perimeter ≤ 6).",
      check: (_c, api) => hpwl(NETS[4], api.getPositions()) <= 6,
    },
    {
      id: "golden-14",
      title: "Reach HPWL 14",
      level: "Practice",
      prompt: "Arrange cells so total HPWL equals 14 (teaching compact).",
      hint: "Study Reveal golden, then recreate: A(2,2) B(4,2) C(2,4) D(4,4) E(3,3) F(1,3).",
      check: (_c, api) => totalHpwl(NETS, api.getPositions()) === GOLDENS.goldenHpwl,
    },
    {
      id: "ef-2",
      title: "EF HPWL = 2",
      level: "Practice",
      prompt: "Place E and F so net [E,F] HPWL is 2.",
      hint: "Same y, |Δx|=2 (e.g. E(3,3) F(1,3)).",
      check: (_c, api) => hpwl(NETS[5], api.getPositions()) === 2,
    },
    {
      id: "drop-38",
      title: "Drop of 38 from starter",
      level: "Stretch",
      prompt: "Reach total HPWL 14 so the drop from starter 52 is 38.",
      hint: "52 − 14 = 38; match the compact placement.",
      check: (_c, api) => {
        const h = totalHpwl(NETS, api.getPositions());
        return h === GOLDENS.goldenHpwl && GOLDENS.starterHpwl - h === 38;
      },
    },
    {
      id: "match-golden",
      title: "Match golden coords",
      level: "Stretch",
      prompt: "Place every cell on the teaching golden coordinates.",
      hint: "Reveal golden to study, Reset, then rebuild cell by cell.",
      check: (_c, api) => positionsNear(api.getPositions(), GOLDEN_PLACEMENT, 0.05),
    },
    {
      id: "near-golden",
      title: "Near golden HPWL",
      level: "Stretch",
      prompt: "Get total HPWL within 2 of golden 14 (≤ 16).",
      hint: "Almost compact is enough.",
      check: (_c, api) => near(totalHpwl(NETS, api.getPositions()), GOLDENS.goldenHpwl, 2),
    },
  ],
});
