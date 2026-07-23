import {
  CELLS,
  GOLDENS,
  NETS,
  OVERLAP_PLACEMENT,
  clonePositions,
  minPairDistance,
  near,
  round1,
  spreadCells,
  totalHpwl,
} from "../../assets/placement-core.js";
import {
  createChallengeLab,
  drawPlacement,
  el,
  metricsBlock,
} from "../../assets/placement-ui.js";

const root = document.getElementById("lab-root");
let pos = clonePositions(OVERLAP_PLACEMENT);
let ran = false;

function arm() {
  pos = clonePositions(OVERLAP_PLACEMENT);
  ran = false;
}

createChallengeLab(root, {
  starterHtml: `
    <p><strong>Starter:</strong> A,B,C overlap at (4,4) so min pairwise distance is
    <strong>0</strong>. Spread/legalize lite pushes pairs to minDist
    <strong>${GOLDENS.spreadMinPairDist}</strong>.</p>
  `,
  loadStarter() {
    arm();
  },
  challenges: [
    {
      id: "overlap-0",
      title: "Overlap dist 0",
      level: "Intro",
      prompt: "Before spread, min pairwise distance is 0.",
      hint: "Reset / load overlap starter.",
      setup: arm,
      check: () => !ran && minPairDistance(pos) === 0,
    },
    {
      id: "run-spread",
      title: "Run spread",
      level: "Intro",
      prompt: "Click Spread cells.",
      hint: "Primary button.",
      setup: arm,
      check: () => ran,
    },
    {
      id: "min-0-5",
      title: "Min dist ≥ 0.5",
      level: "Intro",
      prompt: "After spread, min pairwise distance ≥ 0.5.",
      hint: "Default minDist.",
      setup: arm,
      check: () => ran && minPairDistance(pos) >= GOLDENS.spreadMinPairDist - 1e-6,
    },
    {
      id: "exact-0-5",
      title: "Min dist ≈ 0.5",
      level: "Practice",
      prompt: "After spread, round1(minDist) is 0.5.",
      hint: "Snap to minDist.",
      setup: arm,
      check: () => ran && near(round1(minPairDistance(pos)), 0.5, 0.05),
    },
    {
      id: "improved-dist",
      title: "Distance improved",
      level: "Practice",
      prompt: "After spread, minDist > before (0).",
      hint: "Any positive separation.",
      setup: arm,
      check: () => ran && minPairDistance(pos) > 0,
    },
    {
      id: "abc-separated",
      title: "A≠B coords",
      level: "Practice",
      prompt: "After spread, A and B are not at the same point.",
      hint: "They started coincident.",
      setup: arm,
      check: () =>
        ran && (pos.A.x !== pos.B.x || pos.A.y !== pos.B.y),
    },
    {
      id: "d-still-far",
      title: "D still away",
      level: "Practice",
      prompt: "D remains near (7,1) (not dragged to origin).",
      hint: "Only near-pairs are pushed.",
      setup: arm,
      check: () => ran && pos.D.x > 5 && pos.D.y < 3,
    },
    {
      id: "hpwl-finite",
      title: "HPWL finite",
      level: "Stretch",
      prompt: "Total HPWL is finite after spread.",
      hint: "Always true if coords finite.",
      setup: arm,
      check: () => ran && Number.isFinite(totalHpwl(NETS, pos)),
    },
    {
      id: "reset-overlap",
      title: "Reset restores overlap",
      level: "Stretch",
      prompt: "After Reset, minDist is 0 again.",
      hint: "Reset button.",
      setup: arm,
      check: () => !ran && minPairDistance(pos) === 0,
    },
    {
      id: "six-cells",
      title: "Six cells",
      level: "Stretch",
      prompt: "Placement still has keys A–F.",
      hint: "CELLS.",
      setup: arm,
      check: () => CELLS.every((id) => pos[id] != null),
    },
  ],
  extraActions(ctx) {
    return [
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: "Reset",
        onClick: () => {
          arm();
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Spread cells",
        onClick: () => {
          pos = spreadCells(OVERLAP_PLACEMENT);
          ran = true;
          ctx.rerender();
        },
      }),
    ];
  },
  renderWorkspace(ctx) {
    drawPlacement(ctx.canvas, CELLS, pos, NETS, {
      highlightCells: ["A", "B", "C"],
      showBBox: false,
    });
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(
      metricsBlock([
        `ran: ${ran}`,
        `minPairDist: ${round1(minPairDistance(pos))}`,
        `HPWL: ${round1(totalHpwl(NETS, pos))}`,
        `target minDist: ${GOLDENS.spreadMinPairDist}`,
      ])
    );
  },
});
