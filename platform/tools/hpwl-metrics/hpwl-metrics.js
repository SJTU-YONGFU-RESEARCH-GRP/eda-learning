import {
  CELLS,
  GOLDEN_PLACEMENT,
  GOLDENS,
  NETS,
  STARTER_PLACEMENT,
  clonePositions,
  hpwl,
  near,
  round1,
  totalHpwl,
} from "../../assets/placement-core.js";
import {
  createChallengeLab,
  drawPlacement,
  el,
  metricsBlock,
} from "../../assets/placement-ui.js";

const root = document.getElementById("lab-root");
let pos = clonePositions(STARTER_PLACEMENT);
let mode = "starter";

function arm() {
  pos = clonePositions(STARTER_PLACEMENT);
  mode = "none";
}

function show(which) {
  mode = which;
  pos = clonePositions(which === "golden" ? GOLDEN_PLACEMENT : STARTER_PLACEMENT);
}

createChallengeLab(root, {
  starterHtml: `
    <p><strong>Starter example (reference):</strong> spread-out placement has
    <strong>total HPWL ${GOLDENS.starterHpwl}</strong>. Golden compact placement has
    <strong>HPWL ${GOLDENS.goldenHpwl}</strong>. Reload starter anytime.</p>
  `,
  loadStarter() {
    show("starter");
  },
  challenges: [
    {
      id: "starter-52",
      title: "Starter HPWL 52",
      level: "Intro",
      prompt: "Show starter; total HPWL must be 52.",
      hint: "Click Show starter.",
      setup: arm,
      check: () => mode === "starter" && totalHpwl(NETS, pos) === GOLDENS.starterHpwl,
    },
    {
      id: "golden-14",
      title: "Golden HPWL 14",
      level: "Intro",
      prompt: "Show golden; total HPWL must be 14.",
      hint: "Click Show golden.",
      setup: arm,
      check: () => mode === "golden" && totalHpwl(NETS, pos) === GOLDENS.goldenHpwl,
    },
    {
      id: "net0-starter",
      title: "Net AB starter = 8",
      level: "Intro",
      prompt: "On starter, HPWL of net [A,B] is 8.",
      hint: "Show starter; |8−0| + |0−0|.",
      setup: arm,
      check: () => mode === "starter" && hpwl(NETS[0], pos) === 8,
    },
    {
      id: "net4-starter",
      title: "4-pin starter = 16",
      level: "Practice",
      prompt: "On starter, 4-pin net ABCD has HPWL 16.",
      hint: "BBox is 8×8 → half-perimeter 16.",
      setup: arm,
      check: () => mode === "starter" && hpwl(NETS[4], pos) === 16,
    },
    {
      id: "net4-golden",
      title: "4-pin golden = 4",
      level: "Practice",
      prompt: "On golden, ABCD HPWL is 4.",
      hint: "BBox 2×2.",
      setup: arm,
      check: () => mode === "golden" && hpwl(NETS[4], pos) === 4,
    },
    {
      id: "drop-38",
      title: "Drop of 38",
      level: "Practice",
      prompt: "starter − golden HPWL equals 38.",
      hint: "52 − 14.",
      setup: arm,
      check: () =>
        GOLDENS.starterHpwl - GOLDENS.goldenHpwl === 38 &&
        (mode === "starter" || mode === "golden"),
    },
    {
      id: "ef-starter",
      title: "EF starter = 4",
      level: "Practice",
      prompt: "Starter net [E,F] HPWL is 4.",
      hint: "E(4,4) F(0,4).",
      setup: arm,
      check: () => mode === "starter" && hpwl(NETS[5], pos) === 4,
    },
    {
      id: "ef-golden",
      title: "EF golden = 2",
      level: "Stretch",
      prompt: "Golden net [E,F] HPWL is 2.",
      hint: "E(3,3) F(1,3).",
      setup: arm,
      check: () => mode === "golden" && hpwl(NETS[5], pos) === 2,
    },
    {
      id: "six-nets",
      title: "Six nets",
      level: "Stretch",
      prompt: "Instance has exactly 6 nets.",
      hint: "NETS.length.",
      setup: arm,
      check: () => NETS.length === 6 && (mode === "starter" || mode === "golden"),
    },
    {
      id: "six-cells",
      title: "Six cells",
      level: "Stretch",
      prompt: "Instance has exactly 6 cells A–F.",
      hint: "CELLS.",
      setup: arm,
      check: () => CELLS.length === 6 && CELLS.join("") === "ABCDEF",
    },
  ],
  extraActions(ctx) {
    return [
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: "Show starter",
        onClick: () => {
          show("starter");
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Show golden",
        onClick: () => {
          show("golden");
          ctx.rerender();
        },
      }),
    ];
  },
  renderWorkspace(ctx) {
    drawPlacement(ctx.canvas, CELLS, pos, NETS, { highlightNets: mode === "golden" ? ["4"] : [] });
    const lines = [
      `view: ${mode}`,
      `total HPWL: ${totalHpwl(NETS, pos)}`,
      ...NETS.map((n, i) => `  net${i} [${n.join(",")}]: ${hpwl(n, pos)}`),
      `round1: ${round1(totalHpwl(NETS, pos))} near(golden)? ${near(totalHpwl(NETS, pos), GOLDENS.goldenHpwl)}`,
    ];
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock(lines));
  },
});
