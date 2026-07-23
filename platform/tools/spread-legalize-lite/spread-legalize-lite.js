import {
  GOLDENS,
  NETS,
  OVERLAP_PLACEMENT,
  minPairDistance,
  near,
  round1,
  spreadCells,
  totalHpwl,
} from "../../assets/placement-core.js";
import { createInteractivePlacementLab } from "../../assets/interactive-placement-lab.js";
import { el } from "../../assets/placement-ui.js";

const root = document.getElementById("lab-root");

createInteractivePlacementLab(root, {
  initialPositions: OVERLAP_PLACEMENT,
  revealPositions: OVERLAP_PLACEMENT,
  drawOpts: { highlightCells: ["A", "B", "C"], showBBox: false },
  starterHtml: `
    <p><strong>Your job:</strong> A,B,C start overlapped at (4,4) (min pairwise distance
    <strong>0</strong>). Separate them by hand or <strong>Apply spread</strong> until minDist ≥
    <strong>${GOLDENS.spreadMinPairDist}</strong>.</p>
  `,
  extraActions(ctx, api) {
    return [
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Apply spread",
        onClick: () => {
          api.setPositions(spreadCells(api.getPositions()));
          api.setRevealed(false);
          ctx.rerender();
        },
      }),
    ];
  },
  extraMetrics(api) {
    const pos = api.getPositions();
    return [
      `minPairDist: ${round1(minPairDistance(pos))}`,
      `HPWL: ${round1(totalHpwl(NETS, pos))}`,
      `target minDist: ${GOLDENS.spreadMinPairDist}`,
    ];
  },
  challenges: [
    {
      id: "overlap-0",
      title: "Overlap dist 0",
      level: "Intro",
      prompt: "Before separating, min pairwise distance is 0.",
      hint: "Reset to starter — A,B,C share (4,4).",
      check: (_c, api) => minPairDistance(api.getPositions()) === 0,
    },
    {
      id: "min-0-5",
      title: "Min dist ≥ 0.5",
      level: "Intro",
      prompt: "Separate cells so min pairwise distance ≥ 0.5.",
      hint: "Apply spread, or nudge A/B/C apart.",
      check: (_c, api) => minPairDistance(api.getPositions()) >= GOLDENS.spreadMinPairDist - 1e-6,
    },
    {
      id: "exact-0-5",
      title: "Min dist ≈ 0.5",
      level: "Intro",
      prompt: "After spread (or careful nudges), round1(minDist) is 0.5.",
      hint: "Reset, Apply spread.",
      check: (_c, api) => near(round1(minPairDistance(api.getPositions())), 0.5, 0.05),
    },
    {
      id: "improved-dist",
      title: "Distance improved",
      level: "Practice",
      prompt: "minDist > 0.",
      hint: "Any positive separation of the overlapped triple.",
      check: (_c, api) => minPairDistance(api.getPositions()) > 0,
    },
    {
      id: "abc-separated",
      title: "A≠B coords",
      level: "Practice",
      prompt: "A and B are not at the same point.",
      hint: "They start coincident — move one or Apply spread.",
      check: (_c, api) => {
        const pos = api.getPositions();
        return pos.A.x !== pos.B.x || pos.A.y !== pos.B.y;
      },
    },
    {
      id: "d-still-far",
      title: "D still away",
      level: "Practice",
      prompt: "D remains near (7,1) (x>5, y<3).",
      hint: "Only near-pairs are pushed; leave D alone.",
      check: (_c, api) => {
        const pos = api.getPositions();
        return pos.D.x > 5 && pos.D.y < 3;
      },
    },
    {
      id: "hpwl-finite",
      title: "HPWL finite",
      level: "Practice",
      prompt: "Total HPWL is finite.",
      hint: "True whenever coords are finite.",
      check: (_c, api) => Number.isFinite(totalHpwl(NETS, api.getPositions())),
    },
    {
      id: "reset-overlap",
      title: "Reset restores overlap",
      level: "Stretch",
      prompt: "After Reset to starter, minDist is 0 again.",
      hint: "Reset to starter.",
      check: (_c, api) => minPairDistance(api.getPositions()) === 0,
    },
    {
      id: "six-cells",
      title: "Six cells",
      level: "Stretch",
      prompt: "Placement still has keys A–F.",
      hint: "Always after reset / spread.",
      check: (_c, api) => {
        const pos = api.getPositions();
        return ["A", "B", "C", "D", "E", "F"].every((id) => pos[id] != null);
      },
    },
    {
      id: "spread-keeps-d",
      title: "Spread keeps D far",
      level: "Stretch",
      prompt: "minDist ≥ 0.5 and D still x>5, y<3.",
      hint: "Apply spread from overlap starter.",
      check: (_c, api) => {
        const pos = api.getPositions();
        return (
          minPairDistance(pos) >= GOLDENS.spreadMinPairDist - 1e-6 &&
          pos.D.x > 5 &&
          pos.D.y < 3
        );
      },
    },
  ],
});
