import {
  GOLDENS,
  OVERLAP_PLACEMENT,
  createInteractiveLegalizationLab,
  el,
  positionsNear,
  tetrisLegalize,
} from "../../assets/interactive-legalization-lab.js";

const root = document.getElementById("lab-root");
const AFTER = tetrisLegalize(OVERLAP_PLACEMENT);

createInteractiveLegalizationLab(root, {
  initialPositions: OVERLAP_PLACEMENT,
  revealPositions: AFTER,
  originPositions: OVERLAP_PLACEMENT,
  starterHtml: `
    <p><strong>Your job:</strong> Tetris / shelf pack keeps nearest-row assignment then
    packs left-to-right. <strong>Apply Tetris</strong> → legal, disp
    <strong>${GOLDENS.tetrisDisp}</strong>, HPWL <strong>${GOLDENS.tetrisHpwl}</strong>
    (simpler than Abacus, higher displacement).</p>
  `,
  extraActions(ctx, api) {
    return [
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Apply Tetris",
        onClick: () => {
          api.setPositions(tetrisLegalize(OVERLAP_PLACEMENT));
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
      prompt: "Produce a legal packing.",
      hint: "Apply Tetris.",
      check: (_c, api) => api.isLegal(),
    },
    {
      id: "disp-6",
      title: "Displacement 6",
      level: "Intro",
      prompt: "Displacement vs origin is 6.",
      hint: "Reset → Apply Tetris.",
      check: (_c, api) => api.isLegal() && api.displacement() === GOLDENS.tetrisDisp,
    },
    {
      id: "hpwl-32",
      title: "HPWL 32",
      level: "Intro",
      prompt: "HPWL is 32 after Tetris.",
      hint: "Same as overlap-removal on this seed.",
      check: (_c, api) => api.isLegal() && api.hpwl() === GOLDENS.tetrisHpwl,
    },
    {
      id: "b-at-6-2",
      title: "B at (6,2)",
      level: "Practice",
      prompt: "B ends at (6,2) — stays on middle row.",
      hint: "Tetris does not move B to another row.",
      check: (_c, api) => {
        const b = api.getPositions().B;
        return b && b.x === 6 && b.y === 2;
      },
    },
    {
      id: "c-at-8-2",
      title: "C at (8,2)",
      level: "Practice",
      prompt: "C ends at (8,2).",
      hint: "Apply Tetris.",
      check: (_c, api) => {
        const c = api.getPositions().C;
        return c && c.x === 8 && c.y === 2;
      },
    },
    {
      id: "vs-abacus",
      title: "Abacus disp is smaller",
      level: "Practice",
      prompt: "GOLDENS.abacusDisp (4) < tetrisDisp (6).",
      hint: "Always true for this instance.",
      check: () => GOLDENS.abacusDisp < GOLDENS.tetrisDisp,
    },
    {
      id: "your-disp-6",
      title: "Your disp is Tetris",
      level: "Practice",
      prompt: "Your packing has disp 6 (Tetris teaching result).",
      hint: "Apply Tetris from starter.",
      check: (_c, api) => api.displacement() === GOLDENS.tetrisDisp,
    },
    {
      id: "match-tetris",
      title: "Match Tetris result",
      level: "Stretch",
      prompt: "Match Apply Tetris coordinates.",
      hint: "Reset → Apply Tetris.",
      check: (_c, api) => positionsNear(api.getPositions(), AFTER),
    },
    {
      id: "same-row-pack",
      title: "A/B/C on middle row",
      level: "Stretch",
      prompt: "A, B, and C all remain on y=2.",
      hint: "Tetris keeps nearest-row assignment.",
      check: (_c, api) => {
        const p = api.getPositions();
        return p.A.y === 2 && p.B.y === 2 && p.C.y === 2;
      },
    },
    {
      id: "legal-no-reveal",
      title: "Legal without reveal",
      level: "Stretch",
      prompt: "Legal with disp 6 and Reveal off.",
      hint: "Hide golden; Apply Tetris.",
      check: (_c, api) =>
        api.isLegal() && !api.isRevealed() && api.displacement() === GOLDENS.tetrisDisp,
    },
  ],
});
