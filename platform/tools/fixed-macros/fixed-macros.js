import {
  FIXED_MACROS,
  GOLDENS,
  OVERLAP_PLACEMENT,
  abacusLegalize,
  createInteractiveLegalizationLab,
  el,
  positionsNear,
} from "../../assets/interactive-legalization-lab.js";

const root = document.getElementById("lab-root");
const AFTER = abacusLegalize(OVERLAP_PLACEMENT, { fixed: FIXED_MACROS });

createInteractiveLegalizationLab(root, {
  initialPositions: OVERLAP_PLACEMENT,
  revealPositions: AFTER,
  originPositions: OVERLAP_PLACEMENT,
  lockedIds: ["D"],
  fixedMacros: FIXED_MACROS,
  starterHtml: `
    <p><strong>Your job:</strong> macro <strong>D</strong> is locked at (8,4). Legalize the
    free cells around it (hand or <strong>Apply Abacus</strong>). D must never move.
    Target disp <strong>${GOLDENS.abacusDisp}</strong>.</p>
  `,
  extraActions(ctx, api) {
    return [
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Apply Abacus",
        onClick: () => {
          api.setPositions(abacusLegalize(OVERLAP_PLACEMENT, { fixed: FIXED_MACROS }));
          api.setOrigin(OVERLAP_PLACEMENT);
          api.setRevealed(false);
          ctx.rerender();
        },
      }),
    ];
  },
  challenges: [
    {
      id: "d-locked-start",
      title: "D at (8,4)",
      level: "Intro",
      prompt: "D starts (and stays) at (8,4).",
      hint: "Macro lock — Reset if needed.",
      check: (_c, api) => {
        const d = api.getPositions().D;
        return d && d.x === 8 && d.y === 4;
      },
    },
    {
      id: "make-legal",
      title: "Legal with macro",
      level: "Intro",
      prompt: "Produce a legal packing that respects fixed D.",
      hint: "Apply Abacus (fixed macros).",
      check: (_c, api) => api.isLegal(),
    },
    {
      id: "d-never-moves",
      title: "D never moves",
      level: "Intro",
      prompt: "After legalize, D is still exactly (8,4).",
      hint: "D is locked — Apply Abacus.",
      check: (_c, api) => {
        const d = api.getPositions().D;
        return api.isLegal() && d.x === 8 && d.y === 4;
      },
    },
    {
      id: "disp-4",
      title: "Displacement 4",
      level: "Practice",
      prompt: "Displacement vs origin is 4.",
      hint: "Reset → Apply Abacus.",
      check: (_c, api) => api.isLegal() && api.displacement() === GOLDENS.abacusDisp,
    },
    {
      id: "b-row0",
      title: "B on y=0",
      level: "Practice",
      prompt: "B ends on bottom row.",
      hint: "Same Abacus teaching move as without macros here.",
      check: (_c, api) => api.getPositions().B.y === 0,
    },
    {
      id: "c-row2",
      title: "C on y=4",
      level: "Practice",
      prompt: "C ends on y=4 (shares row with macro D, no overlap).",
      hint: "Apply Abacus; C at (4,4).",
      check: (_c, api) => {
        const c = api.getPositions().C;
        return c && c.y === 4 && c.x === 4;
      },
    },
    {
      id: "no-overlap-d",
      title: "No overlap with D",
      level: "Practice",
      prompt: "Legal packing (implies nothing overlaps D’s [8,10)×{4}).",
      hint: "Apply Abacus.",
      check: (_c, api) => api.isLegal() && api.getPositions().D.x === 8,
    },
    {
      id: "match-abacus",
      title: "Match Abacus+macro",
      level: "Stretch",
      prompt: "Match Apply Abacus with fixed D.",
      hint: "Reset → Apply Abacus.",
      check: (_c, api) => positionsNear(api.getPositions(), AFTER),
    },
    {
      id: "locked-set",
      title: "D is locked",
      level: "Stretch",
      prompt: "D appears in the locked set.",
      hint: "Always true in this lab.",
      check: (_c, api) => api.getLocked().has("D"),
    },
    {
      id: "legal-no-reveal",
      title: "Legal without reveal",
      level: "Stretch",
      prompt: "Legal, D fixed, Reveal off.",
      hint: "Hide golden; Apply Abacus.",
      check: (_c, api) =>
        api.isLegal() &&
        !api.isRevealed() &&
        api.getPositions().D.x === 8 &&
        api.getPositions().D.y === 4,
    },
  ],
});
