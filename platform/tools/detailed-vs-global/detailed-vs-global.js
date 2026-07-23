import {
  GOLDENS,
  OVERLAP_PLACEMENT,
  createInteractiveLegalizationLab,
  detailedLegalize,
  el,
  globalLegalize,
  positionsNear,
} from "../../assets/interactive-legalization-lab.js";

const root = document.getElementById("lab-root");
const GLOBAL = globalLegalize(OVERLAP_PLACEMENT);
const DETAILED = detailedLegalize(OVERLAP_PLACEMENT);

createInteractiveLegalizationLab(root, {
  initialPositions: OVERLAP_PLACEMENT,
  revealPositions: DETAILED,
  originPositions: OVERLAP_PLACEMENT,
  starterHtml: `
    <p><strong>Your job:</strong> compare <strong>global</strong> (Tetris, disp
    <strong>${GOLDENS.globalDisp}</strong>) vs <strong>detailed</strong> (Abacus, disp
    <strong>${GOLDENS.detailedDisp}</strong>). Apply each helper; challenges check
    <em>your</em> packing.</p>
  `,
  extraActions(ctx, api) {
    return [
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: "Apply global (Tetris)",
        onClick: () => {
          api.setPositions(globalLegalize(OVERLAP_PLACEMENT));
          api.setOrigin(OVERLAP_PLACEMENT);
          api.setRevealed(false);
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Apply detailed (Abacus)",
        onClick: () => {
          api.setPositions(detailedLegalize(OVERLAP_PLACEMENT));
          api.setOrigin(OVERLAP_PLACEMENT);
          api.setRevealed(false);
          ctx.rerender();
        },
      }),
    ];
  },
  extraMetrics(api) {
    return [
      `global target disp: ${GOLDENS.globalDisp}`,
      `detailed target disp: ${GOLDENS.detailedDisp}`,
    ];
  },
  challenges: [
    {
      id: "global-disp",
      title: "Global disp 6",
      level: "Intro",
      prompt: "Apply global (Tetris): displacement is 6.",
      hint: "Click Apply global (Tetris).",
      check: (_c, api) =>
        api.isLegal() &&
        api.displacement() === GOLDENS.globalDisp &&
        positionsNear(api.getPositions(), GLOBAL),
    },
    {
      id: "detailed-disp",
      title: "Detailed disp 4",
      level: "Intro",
      prompt: "Apply detailed (Abacus): displacement is 4.",
      hint: "Click Apply detailed (Abacus).",
      check: (_c, api) =>
        api.isLegal() &&
        api.displacement() === GOLDENS.detailedDisp &&
        positionsNear(api.getPositions(), DETAILED),
    },
    {
      id: "both-legal-global",
      title: "Global is legal",
      level: "Intro",
      prompt: "Global result is legal.",
      hint: "Apply global.",
      check: (_c, api) => positionsNear(api.getPositions(), GLOBAL) && api.isLegal(),
    },
    {
      id: "both-legal-detailed",
      title: "Detailed is legal",
      level: "Practice",
      prompt: "Detailed result is legal.",
      hint: "Apply detailed.",
      check: (_c, api) => positionsNear(api.getPositions(), DETAILED) && api.isLegal(),
    },
    {
      id: "detailed-less",
      title: "Detailed disp smaller",
      level: "Practice",
      prompt: "detailedDisp (4) < globalDisp (6).",
      hint: "GOLDENS constants.",
      check: () => GOLDENS.detailedDisp < GOLDENS.globalDisp,
    },
    {
      id: "your-detailed",
      title: "Show detailed packing",
      level: "Practice",
      prompt: "Workspace matches detailed (Abacus) result.",
      hint: "Apply detailed.",
      check: (_c, api) => positionsNear(api.getPositions(), DETAILED),
    },
    {
      id: "your-global",
      title: "Show global packing",
      level: "Practice",
      prompt: "Workspace matches global (Tetris) result.",
      hint: "Apply global.",
      check: (_c, api) => positionsNear(api.getPositions(), GLOBAL),
    },
    {
      id: "hpwl-contrast",
      title: "HPWL differs",
      level: "Stretch",
      prompt: "Detailed HPWL 38 ≠ global HPWL 32 (different packs).",
      hint: "Apply detailed; HPWL should be 38.",
      check: (_c, api) =>
        positionsNear(api.getPositions(), DETAILED) && api.hpwl() === GOLDENS.abacusHpwl,
    },
    {
      id: "pick-detailed",
      title: "Prefer detailed when tight",
      level: "Stretch",
      prompt: "With detailed packing, disp equals GOLDENS.detailedDisp.",
      hint: "Apply detailed when displacement budget is tight.",
      check: (_c, api) =>
        positionsNear(api.getPositions(), DETAILED) &&
        api.displacement() === GOLDENS.detailedDisp,
    },
    {
      id: "legal-no-reveal",
      title: "Detailed without reveal",
      level: "Stretch",
      prompt: "Detailed packing, Reveal off.",
      hint: "Hide golden; Apply detailed.",
      check: (_c, api) =>
        !api.isRevealed() &&
        positionsNear(api.getPositions(), DETAILED) &&
        api.isLegal(),
    },
  ],
});
