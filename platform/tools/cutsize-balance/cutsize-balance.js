import { BAD_SEED, partsString } from "../../assets/clustering-core.js";
import { GOLDEN_BIPART, balanceMetrics } from "../../assets/partitioning-core.js";
import { createInteractiveGraphLab } from "../../assets/interactive-graph-lab.js";

const root = document.getElementById("lab-root");

createInteractiveGraphLab(root, {
  initialAssignment: { ...BAD_SEED },
  revealAssignment: GOLDEN_BIPART,
  starterHtml: `
    <p><strong>Your job:</strong> read cutsize and balance on the bad seed, then Flip/Swap
    (or Reveal for study) to reach cut 3 / ABC|DE. Challenges check <em>your</em> assignment.</p>
  `,
  challenges: [
    {
      id: "bad-cut-12",
      title: "Bad seed cutsize 12",
      level: "Intro",
      prompt: "With the workspace seed, cutsize must be 12.",
      hint: "Reset workspace; do not edit yet.",
      check: (_c, api) => api.cutsize() === 12,
    },
    {
      id: "bad-parts",
      title: "Bad parts AE|BCD",
      level: "Intro",
      prompt: "Seed parts string is AE|BCD.",
      hint: "A and E share side 0 opposite B,C,D.",
      check: (_c, api) => partsString(api.getAssignment()) === "AE|BCD",
    },
    {
      id: "bad-sizes-2-3",
      title: "Sizes 2 vs 3",
      level: "Intro",
      prompt: "Seed part sizes are 2 and 3.",
      hint: "balanceMetrics.sizes on the seed.",
      check: (_c, api) => {
        const m = balanceMetrics(api.getAssignment());
        return m.sizes && m.sizes[0] === 2 && m.sizes[1] === 3;
      },
    },
    {
      id: "bad-ratio",
      title: "Ratio 2/3",
      level: "Practice",
      prompt: "Seed balance ratio equals 2/3.",
      hint: "min/max of the two side sizes.",
      check: (_c, api) => Math.abs(balanceMetrics(api.getAssignment()).ratio - 2 / 3) < 1e-9,
    },
    {
      id: "bad-imbalance",
      title: "Imbalance 0.2",
      level: "Practice",
      prompt: "Seed imbalance |s0−s1|/n equals 0.2.",
      hint: "|2−3|/5 = 0.2.",
      check: (_c, api) => Math.abs(balanceMetrics(api.getAssignment()).imbalance - 0.2) < 1e-9,
    },
    {
      id: "golden-cut-3",
      title: "Reach cutsize 3",
      level: "Practice",
      prompt: "Assign sides so cutsize is 3.",
      hint: "Swap A↔D from the seed, or Flip until ABC|DE.",
      check: (_c, api) => api.cutsize() === 3,
    },
    {
      id: "golden-parts",
      title: "Parts ABC|DE",
      level: "Practice",
      prompt: "Reach parts ABC|DE.",
      hint: "Heavy edges A–B and D–E stay internal.",
      check: (_c, api) => partsString(api.getAssignment()) === "ABC|DE",
    },
    {
      id: "same-ratio",
      title: "Same ratio, better cut",
      level: "Stretch",
      prompt: "ABC|DE keeps ratio 2/3 but cut is 3.",
      hint: "Balance alone does not rank partitions.",
      check: (_c, api) =>
        api.cutsize() === 3 &&
        partsString(api.getAssignment()) === "ABC|DE" &&
        Math.abs(balanceMetrics(api.getAssignment()).ratio - 2 / 3) < 1e-9,
    },
    {
      id: "two-labels",
      title: "Exactly two labels",
      level: "Stretch",
      prompt: "Your assignment uses exactly two partition labels.",
      hint: "Keep bipartition sides 0/1.",
      check: (_c, api) => new Set(Object.values(api.getAssignment())).size === 2,
    },
    {
      id: "cut-beats-balance",
      title: "Cut without reveal",
      level: "Stretch",
      prompt: "Reach cut 3 / ABC|DE with Reveal off (seed cut was 12).",
      hint: "Hide golden; Flip/Swap yourself.",
      check: (_c, api) =>
        !api.isRevealed() &&
        api.cutsize() === 3 &&
        partsString(api.getAssignment()) === "ABC|DE",
    },
  ],
  extraMetrics(api) {
    const m = balanceMetrics(api.getAssignment());
    return [
      `sizes: ${m.sizes ? m.sizes.join(" vs ") : "?"}`,
      `ratio (min/max): ${m.ratio != null ? m.ratio.toFixed(4) : "?"}`,
      `imbalance: ${m.imbalance != null ? m.imbalance.toFixed(4) : "?"}`,
    ];
  },
});
