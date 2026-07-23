import {
  GOLDENS,
  OVERLAP_PLACEMENT,
  abacusLegalize,
  createInteractiveLegalizationLab,
  el,
  positionsNear,
} from "../../assets/interactive-legalization-lab.js";

const root = document.getElementById("lab-root");
const AFTER = abacusLegalize(OVERLAP_PLACEMENT);

createInteractiveLegalizationLab(root, {
  initialPositions: OVERLAP_PLACEMENT,
  revealPositions: AFTER,
  originPositions: OVERLAP_PLACEMENT,
  starterHtml: `
    <p><strong>Your job:</strong> from the overlap seed, legalize with Abacus (try each row
    per cell) — by hand or <strong>Apply Abacus</strong>. Target: legal, disp
    <strong>${GOLDENS.abacusDisp}</strong>, HPWL <strong>${GOLDENS.abacusHpwl}</strong>
    (lower disp than Tetris).</p>
  `,
  extraActions(ctx, api) {
    return [
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Apply Abacus",
        onClick: () => {
          api.setPositions(abacusLegalize(OVERLAP_PLACEMENT));
          api.setOrigin(OVERLAP_PLACEMENT);
          api.setRevealed(false);
          ctx.rerender();
        },
      }),
    ];
  },
  challenges: [
    {
      id: "make-legal",
      title: "Make legal",
      level: "Intro",
      prompt: "Produce a legal packing from the overlap seed.",
      hint: "Apply Abacus, or spread A/B/C across rows.",
      check: (_c, api) => api.isLegal(),
    },
    {
      id: "disp-4",
      title: "Displacement 4",
      level: "Intro",
      prompt: "Displacement vs origin is 4.",
      hint: "Reset → Apply Abacus.",
      check: (_c, api) => api.isLegal() && api.displacement() === GOLDENS.abacusDisp,
    },
    {
      id: "hpwl-38",
      title: "HPWL 38",
      level: "Intro",
      prompt: "HPWL is 38 after Abacus.",
      hint: "Apply Abacus from starter.",
      check: (_c, api) => api.isLegal() && api.hpwl() === GOLDENS.abacusHpwl,
    },
    {
      id: "b-row0",
      title: "B on bottom row",
      level: "Practice",
      prompt: "B ends on y=0.",
      hint: "Abacus moves B to row 0 at x=4.",
      check: (_c, api) => api.getPositions().B.y === 0,
    },
    {
      id: "c-row2",
      title: "C on top row",
      level: "Practice",
      prompt: "C ends on y=4.",
      hint: "Apply Abacus.",
      check: (_c, api) => api.getPositions().C.y === 4,
    },
    {
      id: "a-middle",
      title: "A stays (4,2)",
      level: "Practice",
      prompt: "A remains at (4,2).",
      hint: "Teaching Abacus keeps A.",
      check: (_c, api) => {
        const a = api.getPositions().A;
        return a && a.x === 4 && a.y === 2;
      },
    },
    {
      id: "b-at-4-0",
      title: "B at (4,0)",
      level: "Practice",
      prompt: "B ends at (4,0).",
      hint: "Apply Abacus.",
      check: (_c, api) => {
        const b = api.getPositions().B;
        return b && b.x === 4 && b.y === 0;
      },
    },
    {
      id: "less-tetris",
      title: "Disp < Tetris",
      level: "Stretch",
      prompt: "Abacus disp (4) is less than Tetris disp (6).",
      hint: "Compare GOLDENS; apply Abacus so your disp is 4.",
      check: (_c, api) =>
        api.displacement() === GOLDENS.abacusDisp &&
        GOLDENS.abacusDisp < GOLDENS.tetrisDisp,
    },
    {
      id: "match-abacus",
      title: "Match Abacus result",
      level: "Stretch",
      prompt: "Match Apply Abacus coordinates.",
      hint: "Reset → Apply Abacus.",
      check: (_c, api) => positionsNear(api.getPositions(), AFTER),
    },
    {
      id: "legal-no-reveal",
      title: "Legal without reveal",
      level: "Stretch",
      prompt: "Legal with disp 4 and Reveal off.",
      hint: "Hide golden; Apply Abacus.",
      check: (_c, api) =>
        api.isLegal() && !api.isRevealed() && api.displacement() === GOLDENS.abacusDisp,
    },
  ],
});
