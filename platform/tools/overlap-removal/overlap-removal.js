import {
  GOLDENS,
  OVERLAP_PLACEMENT,
  createInteractiveLegalizationLab,
  el,
  overlapRemoval,
  positionsNear,
} from "../../assets/interactive-legalization-lab.js";

const root = document.getElementById("lab-root");
const AFTER = overlapRemoval(OVERLAP_PLACEMENT);

createInteractiveLegalizationLab(root, {
  initialPositions: OVERLAP_PLACEMENT,
  revealPositions: AFTER,
  originPositions: OVERLAP_PLACEMENT,
  starterHtml: `
    <p><strong>Your job:</strong> A,B,C start stacked at (4,2). Separate them on the row
    (or <strong>Apply overlap removal</strong>) until legal with disp
    <strong>${GOLDENS.overlapRemovalDisp}</strong> and HPWL
    <strong>${GOLDENS.overlapRemovalHpwl}</strong>.</p>
  `,
  extraActions(ctx, api) {
    return [
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Apply overlap removal",
        onClick: () => {
          api.setPositions(overlapRemoval(OVERLAP_PLACEMENT));
          api.setOrigin(OVERLAP_PLACEMENT);
          api.setRevealed(false);
          ctx.rerender();
        },
      }),
    ];
  },
  challenges: [
    {
      id: "stacked",
      title: "Starter stacked",
      level: "Intro",
      prompt: "Before repair, A and B share (4,2).",
      hint: "Reset workspace.",
      check: (_c, api) => {
        const p = api.getPositions();
        return p.A.x === 4 && p.A.y === 2 && p.B.x === 4 && p.B.y === 2 && !api.isLegal();
      },
    },
    {
      id: "make-legal",
      title: "Make legal",
      level: "Intro",
      prompt: "Produce a legal packing.",
      hint: "Apply overlap removal, or nudge B then C right on y=2.",
      check: (_c, api) => api.isLegal(),
    },
    {
      id: "disp-6",
      title: "Displacement 6",
      level: "Intro",
      prompt: "Displacement vs origin is 6.",
      hint: "Reset → Apply overlap removal.",
      check: (_c, api) => api.isLegal() && api.displacement() === GOLDENS.overlapRemovalDisp,
    },
    {
      id: "hpwl-32",
      title: "HPWL 32",
      level: "Practice",
      prompt: "HPWL is 32 after teaching repair.",
      hint: "Apply overlap removal from starter.",
      check: (_c, api) => api.isLegal() && api.hpwl() === GOLDENS.overlapRemovalHpwl,
    },
    {
      id: "b-at-6",
      title: "B at (6,2)",
      level: "Practice",
      prompt: "B ends at x=6 on the middle row.",
      hint: "Teaching pack: A@4, B@6, C@8 on y=2.",
      check: (_c, api) => {
        const b = api.getPositions().B;
        return b && b.x === 6 && b.y === 2;
      },
    },
    {
      id: "c-at-8",
      title: "C at (8,2)",
      level: "Practice",
      prompt: "C ends at x=8 on the middle row.",
      hint: "Apply overlap removal.",
      check: (_c, api) => {
        const c = api.getPositions().C;
        return c && c.x === 8 && c.y === 2;
      },
    },
    {
      id: "a-stays",
      title: "A stays (4,2)",
      level: "Practice",
      prompt: "A remains at (4,2) in the teaching result.",
      hint: "Leftmost of the stacked triple keeps prefer x.",
      check: (_c, api) => {
        const a = api.getPositions().A;
        return a && a.x === 4 && a.y === 2;
      },
    },
    {
      id: "match-after",
      title: "Match teaching result",
      level: "Stretch",
      prompt: "Match Apply overlap-removal coordinates.",
      hint: "Reset → Apply.",
      check: (_c, api) => positionsNear(api.getPositions(), AFTER),
    },
    {
      id: "d-unchanged",
      title: "D still (8,4)",
      level: "Stretch",
      prompt: "D remains at (8,4).",
      hint: "Other rows stay put in this lite repair.",
      check: (_c, api) => {
        const d = api.getPositions().D;
        return d && d.x === 8 && d.y === 4;
      },
    },
    {
      id: "legal-no-reveal",
      title: "Legal without reveal",
      level: "Stretch",
      prompt: "Legal packing with Reveal off and disp 6.",
      hint: "Hide golden; Apply overlap removal.",
      check: (_c, api) =>
        api.isLegal() && !api.isRevealed() && api.displacement() === GOLDENS.overlapRemovalDisp,
    },
  ],
});
