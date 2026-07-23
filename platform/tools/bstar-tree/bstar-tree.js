import {
  GOLDEN_BSTAR,
  isLegalPacking,
  packBstar,
} from "../../assets/floorplanning-core.js";
import {
  createInteractiveFloorplanLab,
  emptyPack,
  el,
  packHasAll,
} from "../../assets/floorplanning-lab.js";

const root = document.getElementById("lab-root");
let ran = false;

createInteractiveFloorplanLab(root, {
  initialPack: emptyPack(),
  revealPack: packBstar(GOLDEN_BSTAR),
  starterHtml: `
    <p><strong>Your job:</strong> run <strong>Pack B*-tree</strong> on the teaching tree
    (A root; left B→C→E; right D above A), then inspect / nudge if you want.
    You can also place manually — challenges prefer the B* packer result.</p>
  `,
  extraActions(ctx, api) {
    return [
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Pack B*-tree",
        onClick: () => {
          api.setPack(packBstar(GOLDEN_BSTAR));
          api.setRevealed(false);
          ran = true;
          ctx.rerender();
        },
      }),
    ];
  },
  onChallengeSetup(_ctx, api) {
    ran = false;
    api.setPack({});
  },
  onLoadStarter(api) {
    ran = false;
    api.setPack({});
  },
  extraMetrics: () => [`packerRan: ${ran}`],
  challenges: [
    {
      id: "run-pack",
      title: "Run B* packer",
      level: "Intro",
      prompt: "Click Pack B*-tree so the packer runs.",
      hint: "Primary button Pack B*-tree.",
      check: () => ran,
    },
    {
      id: "a-origin",
      title: "A at (0,0)",
      level: "Intro",
      prompt: "After packing, A is at the origin.",
      hint: "Pack B*-tree.",
      check: (_c, api) => {
        const p = api.getPack();
        return ran && p.A && p.A.x === 0 && p.A.y === 0;
      },
    },
    {
      id: "b-right",
      title: "B right of A",
      level: "Intro",
      prompt: "B.x equals A.x + A.w (right-of).",
      hint: "Left child geometry.",
      check: (_c, api) => {
        const p = api.getPack();
        return ran && p.A && p.B && p.B.x === p.A.x + p.A.w;
      },
    },
    {
      id: "d-above",
      title: "D above A",
      level: "Practice",
      prompt: "D.y ≥ A.h after packing.",
      hint: "Right child sits on contour above A.",
      check: (_c, api) => {
        const p = api.getPack();
        return ran && p.A && p.D && p.D.y >= p.A.h;
      },
    },
    {
      id: "five",
      title: "Five modules",
      level: "Practice",
      prompt: "Packer placed A–E.",
      hint: "Pack B*-tree.",
      check: (_c, api) => ran && packHasAll(api.getPack()),
    },
    {
      id: "legal",
      title: "Legal packing",
      level: "Practice",
      prompt: "B* result is legal inside 10×8.",
      hint: "Pack then Check.",
      check: (_c, api) => ran && packHasAll(api.getPack()) && isLegalPacking(api.getPack()),
    },
    {
      id: "c-placed",
      title: "C placed",
      level: "Practice",
      prompt: "C exists in the pack.",
      hint: "Left chain B→C→E.",
      check: (_c, api) => ran && !!api.getPack().C,
    },
    {
      id: "e-placed",
      title: "E placed",
      level: "Stretch",
      prompt: "E exists in the pack.",
      hint: "End of left chain.",
      check: (_c, api) => ran && !!api.getPack().E,
    },
    {
      id: "nonneg",
      title: "Non-negative coords",
      level: "Stretch",
      prompt: "All x,y ≥ 0 after pack.",
      hint: "Contour packer.",
      check: (_c, api) =>
        ran &&
        Object.values(api.getPack()).every((r) => r.x >= 0 && r.y >= 0),
    },
    {
      id: "no-reveal",
      title: "Pack without reveal",
      level: "Stretch",
      prompt: "Legal B* pack with Reveal hidden.",
      hint: "Use Pack B*-tree, not Reveal golden.",
      check: (_c, api) =>
        ran &&
        !api.isRevealed() &&
        packHasAll(api.getPack()) &&
        isLegalPacking(api.getPack()),
    },
  ],
});
