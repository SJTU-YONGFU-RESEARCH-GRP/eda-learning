import {
  GOLDEN_PLACEMENT,
  GOLDENS,
  NETS,
  NET_WEIGHTS,
  STARTER_PLACEMENT,
  hpwl,
  timingWeightedHpwl,
  totalHpwl,
} from "../../assets/placement-core.js";
import { createInteractivePlacementLab } from "../../assets/interactive-placement-lab.js";

const root = document.getElementById("lab-root");

createInteractivePlacementLab(root, {
  initialPositions: STARTER_PLACEMENT,
  revealPositions: GOLDEN_PLACEMENT,
  drawOpts: { highlightNets: ["4"] },
  starterHtml: `
    <p><strong>Your job:</strong> move cells to cut plain and timing-weighted HPWL.
    Starter plain <strong>52</strong> / timing <strong>${GOLDENS.starterTimingHpwl}</strong>
    (net4×5). Compact golden plain <strong>14</strong> / timing <strong>${GOLDENS.goldenTimingHpwl}</strong>.</p>
  `,
  extraMetrics(api) {
    const pos = api.getPositions();
    const tw = timingWeightedHpwl(NETS, pos, NET_WEIGHTS);
    return [
      `plain HPWL: ${totalHpwl(NETS, pos)}`,
      `timing HPWL: ${tw}`,
      `weights: [${NET_WEIGHTS.join(", ")}]`,
      ...NETS.map(
        (n, i) =>
          `  net${i} w=${NET_WEIGHTS[i]} hpwl=${hpwl(n, pos)} contrib=${NET_WEIGHTS[i] * hpwl(n, pos)}`
      ),
    ];
  },
  showPerNetMetrics: false,
  challenges: [
    {
      id: "plain-52",
      title: "Plain starter 52",
      level: "Intro",
      prompt: "Reset so plain HPWL is 52.",
      hint: "Reset to starter.",
      check: (_c, api) => totalHpwl(NETS, api.getPositions()) === 52,
    },
    {
      id: "timing-116",
      title: "Timing starter 116",
      level: "Intro",
      prompt: "On starter layout, timing-weighted HPWL is 116.",
      hint: "8+8+8+8+5×16+4.",
      check: (_c, api) =>
        timingWeightedHpwl(NETS, api.getPositions(), NET_WEIGHTS) === GOLDENS.starterTimingHpwl,
    },
    {
      id: "weight-net4",
      title: "Net4 weight 5",
      level: "Intro",
      prompt: "NET_WEIGHTS[4] === 5.",
      hint: "Critical net constant.",
      check: () => NET_WEIGHTS[4] === 5,
    },
    {
      id: "critical-contrib",
      title: "Critical contrib 80",
      level: "Practice",
      prompt: "On starter, weight×HPWL for net4 equals 80.",
      hint: "5 × 16 — keep ABCD at corners.",
      check: (_c, api) => NET_WEIGHTS[4] * hpwl(NETS[4], api.getPositions()) === 80,
    },
    {
      id: "timing-gt-plain",
      title: "Timing > plain",
      level: "Practice",
      prompt: "Timing HPWL > plain HPWL on your placement.",
      hint: "True on starter (and most layouts with net4 weight 5).",
      check: (_c, api) => {
        const pos = api.getPositions();
        return timingWeightedHpwl(NETS, pos, NET_WEIGHTS) > totalHpwl(NETS, pos);
      },
    },
    {
      id: "timing-golden-30",
      title: "Timing HPWL 30",
      level: "Practice",
      prompt: "Arrange cells so timing-weighted HPWL equals 30.",
      hint: "Match compact golden (Reveal to study).",
      check: (_c, api) =>
        timingWeightedHpwl(NETS, api.getPositions(), NET_WEIGHTS) === GOLDENS.goldenTimingHpwl,
    },
    {
      id: "plain-14",
      title: "Plain HPWL 14",
      level: "Practice",
      prompt: "Reach plain HPWL 14.",
      hint: "Same compact placement.",
      check: (_c, api) => totalHpwl(NETS, api.getPositions()) === GOLDENS.goldenHpwl,
    },
    {
      id: "drop-weighted",
      title: "Weighted drop 86",
      level: "Stretch",
      prompt: "Reach timing 30 so the drop from starter 116 is 86.",
      hint: "116 − 30 = 86.",
      check: (_c, api) => {
        const tw = timingWeightedHpwl(NETS, api.getPositions(), NET_WEIGHTS);
        return tw === GOLDENS.goldenTimingHpwl && GOLDENS.starterTimingHpwl - tw === 86;
      },
    },
    {
      id: "unit-weights",
      title: "Other weights 1",
      level: "Stretch",
      prompt: "Nets 0–3 and 5 all have weight 1.",
      hint: "Only net4 is critical.",
      check: () => NET_WEIGHTS.filter((w, i) => i !== 4).every((w) => w === 1),
    },
    {
      id: "both-goldens",
      title: "Plain 14 & timing 30",
      level: "Stretch",
      prompt: "Simultaneously plain HPWL 14 and timing 30.",
      hint: "Compact teaching placement.",
      check: (_c, api) => {
        const pos = api.getPositions();
        return (
          totalHpwl(NETS, pos) === 14 &&
          timingWeightedHpwl(NETS, pos, NET_WEIGHTS) === 30
        );
      },
    },
  ],
});
