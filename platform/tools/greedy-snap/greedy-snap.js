import {
  FLOAT_PLACEMENT,
  GOLDENS,
  ROW_YS,
  createInteractiveLegalizationLab,
  el,
  greedySnap,
  positionsNear,
} from "../../assets/interactive-legalization-lab.js";

const root = document.getElementById("lab-root");
const SNAPPED = greedySnap(FLOAT_PLACEMENT);

createInteractiveLegalizationLab(root, {
  initialPositions: FLOAT_PLACEMENT,
  revealPositions: SNAPPED,
  originPositions: FLOAT_PLACEMENT,
  allowFloat: true,
  starterHtml: `
    <p><strong>Your job:</strong> floats from a sloppy global place are off sites/rows.
    <strong>Snap all</strong> (or place by hand) — then notice A/B still overlap.
    Snap ≠ legal. Challenges check <em>your</em> positions.</p>
  `,
  extraActions(ctx, api) {
    return [
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Snap all",
        onClick: () => {
          api.setPositions(greedySnap(api.getPositions()));
          api.setRevealed(false);
          ctx.rerender();
        },
      }),
    ];
  },
  extraMetrics(api) {
    const p = api.getPositions();
    const onRow = Object.values(p).every((c) => ROW_YS.includes(c.y));
    return [`all on rows: ${onRow}`, `GOLDENS.floatSnapLegal: ${GOLDENS.floatSnapLegal}`];
  },
  challenges: [
    {
      id: "float-off-row",
      title: "Floats off rows",
      level: "Intro",
      prompt: "Before snap, at least one cell is not on a row bottom (0/2/4).",
      hint: "Reset to float starter.",
      check: (_c, api) => {
        const p = api.getPositions();
        return Object.values(p).some((c) => !ROW_YS.includes(c.y));
      },
    },
    {
      id: "snap-all",
      title: "Snap onto sites/rows",
      level: "Intro",
      prompt: "After Snap all, every cell sits on a row y in {0,2,4}.",
      hint: "Click Snap all.",
      check: (_c, api) => {
        const p = api.getPositions();
        return Object.values(p).every((c) => ROW_YS.includes(c.y));
      },
    },
    {
      id: "a-at-4-2",
      title: "A snaps to (4,2)",
      level: "Intro",
      prompt: "After snap, A is at (4,2).",
      hint: "Snap all from float starter.",
      check: (_c, api) => {
        const a = api.getPositions().A;
        return a && a.x === 4 && a.y === 2;
      },
    },
    {
      id: "still-illegal",
      title: "Still illegal after snap",
      level: "Practice",
      prompt: "After snap, packing is still illegal (A/B overlap).",
      hint: "Snap all; do not separate yet.",
      check: (_c, api) => {
        const p = api.getPositions();
        return (
          positionsNear(p, SNAPPED) &&
          !api.isLegal() &&
          api.legalityReport().reason.includes("overlap")
        );
      },
    },
    {
      id: "b-same-as-a",
      title: "B also at (4,2)",
      level: "Practice",
      prompt: "After snap, B shares A’s site (4,2).",
      hint: "That is why snap ≠ legal.",
      check: (_c, api) => {
        const p = api.getPositions();
        return p.A.x === 4 && p.A.y === 2 && p.B.x === 4 && p.B.y === 2;
      },
    },
    {
      id: "golden-flag",
      title: "floatSnapLegal is false",
      level: "Practice",
      prompt: "Teaching flag GOLDENS.floatSnapLegal is false.",
      hint: "Always true for this course instance.",
      check: () => GOLDENS.floatSnapLegal === false,
    },
    {
      id: "match-snap",
      title: "Match snap result",
      level: "Practice",
      prompt: "Match the greedy-snap teaching result.",
      hint: "Reset → Snap all.",
      check: (_c, api) => positionsNear(api.getPositions(), SNAPPED),
    },
    {
      id: "c-at-5-2",
      title: "C at (5,2)",
      level: "Stretch",
      prompt: "After snap, C is at (5,2).",
      hint: "Snap all.",
      check: (_c, api) => {
        const c = api.getPositions().C;
        return c && c.x === 5 && c.y === 2;
      },
    },
    {
      id: "f-at-10-0",
      title: "F at (10,0)",
      level: "Stretch",
      prompt: "After snap, F is at (10,0).",
      hint: "Snap all.",
      check: (_c, api) => {
        const f = api.getPositions().F;
        return f && f.x === 10 && f.y === 0;
      },
    },
    {
      id: "snap-not-legal-lesson",
      title: "Snap does not imply legal",
      level: "Stretch",
      prompt: "Positions match snap result AND packing is illegal.",
      hint: "Reset → Snap all; leave overlaps.",
      check: (_c, api) => positionsNear(api.getPositions(), SNAPPED) && !api.isLegal(),
    },
  ],
});
