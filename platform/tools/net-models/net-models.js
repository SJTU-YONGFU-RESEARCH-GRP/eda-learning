import {
  CELLS,
  GOLDEN_PLACEMENT,
  GOLDENS,
  NETS,
  STARTER_PLACEMENT,
  clonePositions,
  cliqueHpwl,
  hpwl,
  starHpwl,
} from "../../assets/placement-core.js";
import {
  createChallengeLab,
  drawPlacement,
  el,
  metricsBlock,
} from "../../assets/placement-ui.js";

const root = document.getElementById("lab-root");
const NET4 = NETS[4];
let pos = clonePositions(GOLDEN_PLACEMENT);
let mode = "golden";
let model = "both"; // bbox | clique | star | both

function arm() {
  pos = clonePositions(GOLDEN_PLACEMENT);
  mode = "none";
  model = "both";
}

createChallengeLab(root, {
  starterHtml: `
    <p><strong>Starter:</strong> on golden placement, 4-pin net ABCD has bbox HPWL
    <strong>4</strong>, clique (pairwise) <strong>${GOLDENS.cliqueHpwlGolden4pin}</strong>,
    star-from-A <strong>${GOLDENS.starHpwlGolden4pinFromA}</strong>. Clique overcounts vs star.</p>
  `,
  loadStarter() {
    pos = clonePositions(GOLDEN_PLACEMENT);
    mode = "golden";
    model = "both";
  },
  challenges: [
    {
      id: "bbox-4",
      title: "BBox HPWL 4",
      level: "Intro",
      prompt: "Golden ABCD bbox HPWL is 4.",
      hint: "Show golden; half-perimeter of 2×2 box.",
      setup: arm,
      check: () => mode === "golden" && hpwl(NET4, pos) === 4,
    },
    {
      id: "clique-16",
      title: "Clique 16",
      level: "Intro",
      prompt: "Clique HPWL on golden ABCD is 16.",
      hint: "Sum of 6 pairwise HPWLs.",
      setup: arm,
      check: () => mode === "golden" && cliqueHpwl(NET4, pos) === GOLDENS.cliqueHpwlGolden4pin,
    },
    {
      id: "star-8",
      title: "Star-from-A 8",
      level: "Intro",
      prompt: "Star HPWL from A is 8.",
      hint: "AB+AC+AD = 2+2+4.",
      setup: arm,
      check: () =>
        mode === "golden" && starHpwl(NET4, pos, "A") === GOLDENS.starHpwlGolden4pinFromA,
    },
    {
      id: "clique-gt-star",
      title: "Clique > star",
      level: "Practice",
      prompt: "Clique HPWL is strictly greater than star-from-A.",
      hint: "16 > 8.",
      setup: arm,
      check: () =>
        mode === "golden" && cliqueHpwl(NET4, pos) > starHpwl(NET4, pos, "A"),
    },
    {
      id: "clique-gt-bbox",
      title: "Clique > bbox",
      level: "Practice",
      prompt: "Clique HPWL exceeds bbox HPWL.",
      hint: "Pairwise sum vs half-perimeter.",
      setup: arm,
      check: () => mode === "golden" && cliqueHpwl(NET4, pos) > hpwl(NET4, pos),
    },
    {
      id: "star-gt-bbox",
      title: "Star > bbox",
      level: "Practice",
      prompt: "Star-from-A exceeds bbox HPWL.",
      hint: "8 > 4.",
      setup: arm,
      check: () => mode === "golden" && starHpwl(NET4, pos, "A") > hpwl(NET4, pos),
    },
    {
      id: "ratio-2",
      title: "Clique/star = 2",
      level: "Practice",
      prompt: "clique / star-from-A equals 2 on golden.",
      hint: "16/8.",
      setup: arm,
      check: () =>
        mode === "golden" &&
        cliqueHpwl(NET4, pos) / starHpwl(NET4, pos, "A") === 2,
    },
    {
      id: "starter-clique",
      title: "Starter clique 64",
      level: "Stretch",
      prompt: "Show starter; clique on ABCD is 64.",
      hint: "Corners of an 8×8 square: 8+8+16+16+8+8.",
      setup: arm,
      check: () => mode === "starter" && cliqueHpwl(NET4, pos) === 64,
    },
    {
      id: "model-contrast",
      title: "Model contrast",
      level: "Stretch",
      prompt: "With both models shown on golden, clique is 16 and star is 8.",
      hint: "Load starter / Show golden + both.",
      setup: arm,
      check: () =>
        mode === "golden" &&
        model === "both" &&
        cliqueHpwl(NET4, pos) === 16 &&
        starHpwl(NET4, pos, "A") === 8,
    },
    {
      id: "four-pins",
      title: "Four pins",
      level: "Stretch",
      prompt: "Net 4 has exactly four pins.",
      hint: "A,B,C,D.",
      setup: arm,
      check: () => NET4.length === 4 && NET4.join("") === "ABCD",
    },
  ],
  extraActions(ctx) {
    return [
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: "Show starter",
        onClick: () => {
          pos = clonePositions(STARTER_PLACEMENT);
          mode = "starter";
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Show golden",
        onClick: () => {
          pos = clonePositions(GOLDEN_PLACEMENT);
          mode = "golden";
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-ghost",
        type: "button",
        text: "Model: both",
        onClick: () => {
          model = "both";
          ctx.rerender();
        },
      }),
    ];
  },
  renderWorkspace(ctx) {
    drawPlacement(ctx.canvas, CELLS, pos, NETS, {
      highlightNets: ["4"],
      highlightCells: NET4,
    });
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(
      metricsBlock([
        `view: ${mode}  model: ${model}`,
        `bbox HPWL(ABCD): ${hpwl(NET4, pos)}`,
        `clique HPWL: ${cliqueHpwl(NET4, pos)}`,
        `star-from-A: ${starHpwl(NET4, pos, "A")}`,
        `star-from-B: ${starHpwl(NET4, pos, "B")}`,
      ])
    );
  },
});
