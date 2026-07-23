import {
  CELLS,
  GOLDEN_PLACEMENT,
  GOLDENS,
  NETS,
  NET_WEIGHTS,
  STARTER_PLACEMENT,
  clonePositions,
  hpwl,
  timingWeightedHpwl,
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

createChallengeLab(root, {
  starterHtml: `
    <p><strong>Starter:</strong> plain HPWL <strong>52</strong>, timing-weighted
    (net4×5) <strong>${GOLDENS.starterTimingHpwl}</strong>. Golden plain
    <strong>14</strong>, weighted <strong>${GOLDENS.goldenTimingHpwl}</strong>.
    Critical net ABCD dominates the timing score.</p>
  `,
  loadStarter() {
    pos = clonePositions(STARTER_PLACEMENT);
    mode = "starter";
  },
  challenges: [
    {
      id: "plain-52",
      title: "Plain starter 52",
      level: "Intro",
      prompt: "Starter plain HPWL is 52.",
      hint: "Show starter.",
      setup: arm,
      check: () => mode === "starter" && totalHpwl(NETS, pos) === 52,
    },
    {
      id: "timing-116",
      title: "Timing starter 116",
      level: "Intro",
      prompt: "Starter timing-weighted HPWL is 116.",
      hint: "8+8+8+8+5×16+4.",
      setup: arm,
      check: () =>
        mode === "starter" &&
        timingWeightedHpwl(NETS, pos, NET_WEIGHTS) === GOLDENS.starterTimingHpwl,
    },
    {
      id: "golden-30",
      title: "Timing golden 30",
      level: "Intro",
      prompt: "Golden timing-weighted HPWL is 30.",
      hint: "2+2+2+2+5×4+2.",
      setup: arm,
      check: () =>
        mode === "golden" &&
        timingWeightedHpwl(NETS, pos, NET_WEIGHTS) === GOLDENS.goldenTimingHpwl,
    },
    {
      id: "weight-net4",
      title: "Net4 weight 5",
      level: "Practice",
      prompt: "NET_WEIGHTS[4] === 5.",
      hint: "Critical net.",
      setup: arm,
      check: () => NET_WEIGHTS[4] === 5,
    },
    {
      id: "critical-contrib",
      title: "Critical contrib 80",
      level: "Practice",
      prompt: "On starter, weight×HPWL for net4 equals 80.",
      hint: "5 × 16.",
      setup: arm,
      check: () =>
        mode === "starter" && NET_WEIGHTS[4] * hpwl(NETS[4], pos) === 80,
    },
    {
      id: "timing-gt-plain",
      title: "Timing > plain",
      level: "Practice",
      prompt: "On starter, timing HPWL > plain HPWL.",
      hint: "Critical weight amplifies net4.",
      setup: arm,
      check: () =>
        mode === "starter" &&
        timingWeightedHpwl(NETS, pos, NET_WEIGHTS) > totalHpwl(NETS, pos),
    },
    {
      id: "drop-weighted",
      title: "Weighted drop 86",
      level: "Practice",
      prompt: "starterTiming − goldenTiming equals 86.",
      hint: "116 − 30.",
      setup: arm,
      check: () =>
        (mode === "starter" || mode === "golden") &&
        GOLDENS.starterTimingHpwl - GOLDENS.goldenTimingHpwl === 86,
    },
    {
      id: "plain-drop-smaller",
      title: "Plain drop smaller",
      level: "Stretch",
      prompt: "Plain drop (38) is less than timing drop (86).",
      hint: "Critical net shrinks more in the score.",
      setup: arm,
      check: () =>
        GOLDENS.starterHpwl - GOLDENS.goldenHpwl <
          GOLDENS.starterTimingHpwl - GOLDENS.goldenTimingHpwl &&
        (mode === "starter" || mode === "golden"),
    },
    {
      id: "unit-weights",
      title: "Other weights 1",
      level: "Stretch",
      prompt: "Nets 0–3 and 5 all have weight 1.",
      hint: "Only net4 is critical.",
      setup: arm,
      check: () =>
        NET_WEIGHTS.filter((w, i) => i !== 4).every((w) => w === 1),
    },
    {
      id: "golden-plain-14",
      title: "Golden plain 14",
      level: "Stretch",
      prompt: "Show golden; plain HPWL is 14 and timing is 30.",
      hint: "Show golden.",
      setup: arm,
      check: () =>
        mode === "golden" &&
        totalHpwl(NETS, pos) === 14 &&
        timingWeightedHpwl(NETS, pos, NET_WEIGHTS) === 30,
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
    ];
  },
  renderWorkspace(ctx) {
    drawPlacement(ctx.canvas, CELLS, pos, NETS, { highlightNets: ["4"] });
    const tw = timingWeightedHpwl(NETS, pos, NET_WEIGHTS);
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(
      metricsBlock([
        `view: ${mode}`,
        `plain HPWL: ${totalHpwl(NETS, pos)}`,
        `timing HPWL: ${tw}`,
        `weights: [${NET_WEIGHTS.join(", ")}]`,
        ...NETS.map(
          (n, i) =>
            `  net${i} w=${NET_WEIGHTS[i]} hpwl=${hpwl(n, pos)} contrib=${NET_WEIGHTS[i] * hpwl(n, pos)}`
        ),
      ])
    );
  },
});
