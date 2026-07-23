import {
  GOLDEN_PACK,
  deadspace,
  density,
  isLegalPacking,
  moduleAreaSum,
  outlineArea,
} from "../../assets/floorplanning-core.js";
import {
  createInteractiveFloorplanLab,
  emptyPack,
  packHasAll,
} from "../../assets/floorplanning-lab.js";

const root = document.getElementById("lab-root");

createInteractiveFloorplanLab(root, {
  initialPack: emptyPack(),
  revealPack: GOLDEN_PACK,
  starterHtml: `
    <p><strong>Your job:</strong> place a legal packing, then read metrics.
    Module area sum is always <strong>23</strong>, outline <strong>80</strong>, deadspace <strong>57</strong>,
    density <strong>0.2875</strong> — but only trust them after your packing is legal.</p>
  `,
  challenges: [
    {
      id: "place-legal",
      title: "Legal packing first",
      level: "Intro",
      prompt: "Place all five modules in a legal packing.",
      hint: "Use the same skills as fixed-outline.",
      check: (_c, api) => packHasAll(api.getPack()) && isLegalPacking(api.getPack()),
    },
    {
      id: "area-23",
      title: "See module area 23",
      level: "Intro",
      prompt: "With a legal packing, confirm module area sum is 23 (shown in metrics).",
      hint: "6+6+4+3+4. Legal packing required so you looked at the panel.",
      check: (_c, api) =>
        packHasAll(api.getPack()) &&
        isLegalPacking(api.getPack()) &&
        moduleAreaSum(api.getModules()) === 23,
    },
    {
      id: "outline-80",
      title: "Outline area 80",
      level: "Intro",
      prompt: "Legal packing + outline area 80.",
      hint: "10×8.",
      check: (_c, api) =>
        isLegalPacking(api.getPack()) && packHasAll(api.getPack()) && outlineArea() === 80,
    },
    {
      id: "ds-57",
      title: "Deadspace 57",
      level: "Practice",
      prompt: "Legal packing; deadspace metric equals 57.",
      hint: "80 − 23.",
      check: (_c, api) =>
        packHasAll(api.getPack()) &&
        isLegalPacking(api.getPack()) &&
        deadspace() === 57,
    },
    {
      id: "den",
      title: "Density 0.2875",
      level: "Practice",
      prompt: "Legal packing; density equals 0.2875.",
      hint: "23/80.",
      check: (_c, api) =>
        packHasAll(api.getPack()) &&
        isLegalPacking(api.getPack()) &&
        Math.abs(density() - 0.2875) < 1e-9,
    },
    {
      id: "whitespace",
      title: "Whitespace 0.7125",
      level: "Practice",
      prompt: "Legal packing; deadspace/outline = 0.7125.",
      hint: "57/80.",
      check: (_c, api) =>
        packHasAll(api.getPack()) &&
        isLegalPacking(api.getPack()) &&
        Math.abs(deadspace() / outlineArea() - 0.7125) < 1e-9,
    },
    {
      id: "density-lt1",
      title: "Density &lt; 1",
      level: "Practice",
      prompt: "Legal packing with density strictly below 1.",
      hint: "Always true here once legal.",
      check: (_c, api) =>
        packHasAll(api.getPack()) && isLegalPacking(api.getPack()) && density() < 1,
    },
    {
      id: "formula",
      title: "Deadspace formula",
      level: "Stretch",
      prompt: "Legal packing; deadspace === outlineArea − moduleAreaSum.",
      hint: "Identity check on the metrics.",
      check: (_c, api) =>
        packHasAll(api.getPack()) &&
        isLegalPacking(api.getPack()) &&
        deadspace() === outlineArea() - moduleAreaSum(api.getModules()),
    },
    {
      id: "legal-before-metrics",
      title: "Illegal does not count",
      level: "Stretch",
      prompt: "Only a legal all-five packing passes — empty/illegal fails.",
      hint: "Place carefully.",
      check: (_c, api) => packHasAll(api.getPack()) && isLegalPacking(api.getPack()),
    },
    {
      id: "no-reveal",
      title: "Legal without reveal",
      level: "Stretch",
      prompt: "Legal all-five packing with Reveal hidden.",
      hint: "Hide golden if you peeked.",
      check: (_c, api) =>
        !api.isRevealed() && packHasAll(api.getPack()) && isLegalPacking(api.getPack()),
    },
  ],
});
