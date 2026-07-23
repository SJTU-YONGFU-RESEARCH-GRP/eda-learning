import {
  GOLDEN_PLACEMENT,
  GOLDENS,
  NETS,
  STARTER_PLACEMENT,
  cliqueHpwl,
  hpwl,
  starHpwl,
} from "../../assets/placement-core.js";
import { createInteractivePlacementLab } from "../../assets/interactive-placement-lab.js";

const root = document.getElementById("lab-root");
const NET4 = NETS[4];

createInteractivePlacementLab(root, {
  initialPositions: STARTER_PLACEMENT,
  revealPositions: GOLDEN_PLACEMENT,
  drawOpts: { highlightNets: ["4"], highlightCells: NET4 },
  showPerNetMetrics: false,
  starterHtml: `
    <p><strong>Your job:</strong> compare bbox / clique / star models on net ABCD while you move cells.
    On the compact teaching placement: bbox <strong>4</strong>, clique <strong>${GOLDENS.cliqueHpwlGolden4pin}</strong>,
    star-from-A <strong>${GOLDENS.starHpwlGolden4pinFromA}</strong>. Start from the spread starter (HPWL 52).</p>
  `,
  extraMetrics(api) {
    const pos = api.getPositions();
    return [
      `bbox HPWL(ABCD): ${hpwl(NET4, pos)}`,
      `clique HPWL: ${cliqueHpwl(NET4, pos)}`,
      `star-from-A: ${starHpwl(NET4, pos, "A")}`,
      `star-from-B: ${starHpwl(NET4, pos, "B")}`,
    ];
  },
  challenges: [
    {
      id: "starter-clique-64",
      title: "Starter clique 64",
      level: "Intro",
      prompt: "On starter (reset), clique HPWL on ABCD is 64.",
      hint: "Corners of an 8×8 square: six pairwise spans.",
      check: (_c, api) => cliqueHpwl(NET4, api.getPositions()) === 64,
    },
    {
      id: "bbox-4",
      title: "BBox HPWL 4",
      level: "Intro",
      prompt: "Move A–D so ABCD bbox HPWL is 4.",
      hint: "2×2 bounding box → half-perimeter 4.",
      check: (_c, api) => hpwl(NET4, api.getPositions()) === 4,
    },
    {
      id: "clique-16",
      title: "Clique 16",
      level: "Intro",
      prompt: "Reach clique HPWL 16 on ABCD (compact square).",
      hint: "Match golden A–D: (2,2)(4,2)(2,4)(4,4).",
      check: (_c, api) => cliqueHpwl(NET4, api.getPositions()) === GOLDENS.cliqueHpwlGolden4pin,
    },
    {
      id: "star-8",
      title: "Star-from-A 8",
      level: "Intro",
      prompt: "Star HPWL from A equals 8.",
      hint: "On compact: AB+AC+AD = 2+2+4.",
      check: (_c, api) => starHpwl(NET4, api.getPositions(), "A") === GOLDENS.starHpwlGolden4pinFromA,
    },
    {
      id: "clique-gt-star",
      title: "Clique > star",
      level: "Practice",
      prompt: "Any placement where clique HPWL > star-from-A (true on starter and golden).",
      hint: "Reset or compact — both satisfy.",
      check: (_c, api) => {
        const pos = api.getPositions();
        return cliqueHpwl(NET4, pos) > starHpwl(NET4, pos, "A");
      },
    },
    {
      id: "clique-gt-bbox",
      title: "Clique > bbox",
      level: "Practice",
      prompt: "Clique HPWL exceeds bbox HPWL on your placement.",
      hint: "True whenever ≥3 pins are not collinear in a degenerate way — try starter.",
      check: (_c, api) => {
        const pos = api.getPositions();
        return cliqueHpwl(NET4, pos) > hpwl(NET4, pos);
      },
    },
    {
      id: "star-gt-bbox",
      title: "Star > bbox",
      level: "Practice",
      prompt: "Star-from-A exceeds bbox HPWL.",
      hint: "Compact golden: 8 > 4.",
      check: (_c, api) => {
        const pos = api.getPositions();
        return starHpwl(NET4, pos, "A") > hpwl(NET4, pos);
      },
    },
    {
      id: "ratio-2",
      title: "Clique/star = 2",
      level: "Practice",
      prompt: "clique / star-from-A equals 2 (compact ABCD).",
      hint: "16/8 on the teaching square.",
      check: (_c, api) => {
        const pos = api.getPositions();
        const s = starHpwl(NET4, pos, "A");
        return s > 0 && cliqueHpwl(NET4, pos) / s === 2;
      },
    },
    {
      id: "models-compact",
      title: "All three goldens",
      level: "Stretch",
      prompt: "Simultaneously: bbox 4, clique 16, star-from-A 8.",
      hint: "Place A–D on the 2×2 teaching square.",
      check: (_c, api) => {
        const pos = api.getPositions();
        return (
          hpwl(NET4, pos) === 4 &&
          cliqueHpwl(NET4, pos) === 16 &&
          starHpwl(NET4, pos, "A") === 8
        );
      },
    },
    {
      id: "four-pins",
      title: "Four pins",
      level: "Stretch",
      prompt: "Net 4 still has exactly four pins A–D (instance check).",
      hint: "Always true for this lab netlist.",
      check: () => NET4.length === 4 && NET4.join("") === "ABCD",
    },
  ],
});
