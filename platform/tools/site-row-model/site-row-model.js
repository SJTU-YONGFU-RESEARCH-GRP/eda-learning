import {
  CHIP_H,
  CHIP_W,
  GOLDEN_PLACEMENT,
  GOLDENS,
  OVERLAP_PLACEMENT,
  ROW_H,
  ROW_YS,
  SITE_W,
  WIDTHS,
  createInteractiveLegalizationLab,
  isLegal,
  positionsNear,
} from "../../assets/interactive-legalization-lab.js";

const root = document.getElementById("lab-root");

createInteractiveLegalizationLab(root, {
  initialPositions: OVERLAP_PLACEMENT,
  revealPositions: GOLDEN_PLACEMENT,
  originPositions: OVERLAP_PLACEMENT,
  starterHtml: `
    <p><strong>Your job:</strong> learn the chip model — <code>${CHIP_W}×${CHIP_H}</code>,
    <strong>${GOLDENS.nRows}</strong> rows at y=${ROW_YS.join("/")}, site pitch
    <strong>${SITE_W}</strong>, row height <strong>${ROW_H}</strong>. Move cells onto sites;
    challenges check <em>your</em> packing. Reveal golden is study-only.</p>
  `,
  challenges: [
    {
      id: "chip-w",
      title: "Chip width 12",
      level: "Intro",
      prompt: "Chip width is 12 sites.",
      hint: "Always true for this instance.",
      check: () => CHIP_W === 12 && GOLDENS.chipW === 12,
    },
    {
      id: "chip-h",
      title: "Chip height 6",
      level: "Intro",
      prompt: "Chip height is 6 (3 rows × rowH 2).",
      hint: "GOLDENS.chipH.",
      check: () => CHIP_H === 6 && GOLDENS.chipH === 6,
    },
    {
      id: "three-rows",
      title: "Three rows",
      level: "Intro",
      prompt: "There are 3 rows at y = 0, 2, 4.",
      hint: "ROW_YS.",
      check: () => ROW_YS.length === 3 && ROW_YS[0] === 0 && ROW_YS[2] === 4,
    },
    {
      id: "site-pitch",
      title: "Site pitch 1",
      level: "Intro",
      prompt: "Site width / pitch is 1.",
      hint: "SITE_W.",
      check: () => SITE_W === 1 && GOLDENS.siteW === 1,
    },
    {
      id: "widths-a-e",
      title: "Widths A=2, E=1",
      level: "Practice",
      prompt: "Cell A is width 2; E is width 1.",
      hint: "WIDTHS map.",
      check: () => WIDTHS.A === 2 && WIDTHS.E === 1,
    },
    {
      id: "total-width",
      title: "Total cell width 10",
      level: "Practice",
      prompt: "Sum of cell widths is 10 (fits in 12).",
      hint: "2+2+2+2+1+1.",
      check: () => GOLDENS.totalCellWidth === 10,
    },
    {
      id: "starter-illegal",
      title: "Starter illegal",
      level: "Practice",
      prompt: "Reset workspace: packing is illegal (A/B overlap).",
      hint: "Reset to starter overlap seed.",
      check: (_c, api) => !api.isLegal() && api.legalityReport().reason.includes("overlap"),
    },
    {
      id: "make-legal",
      title: "Make a legal packing",
      level: "Practice",
      prompt: "Move cells until the packing is legal (site-aligned, no overlap).",
      hint: "Separate A,B,C on the middle row, or Reveal then Hide and recreate.",
      check: (_c, api) => api.isLegal(),
    },
    {
      id: "match-golden",
      title: "Match teaching golden",
      level: "Stretch",
      prompt: "Recreate the golden packing positions.",
      hint: "Reveal for study, then Reset and place by hand.",
      check: (_c, api) => api.isLegal() && positionsNear(api.getPositions(), GOLDEN_PLACEMENT),
    },
    {
      id: "legal-no-reveal",
      title: "Legal without reveal",
      level: "Stretch",
      prompt: "Legal packing while Reveal is off.",
      hint: "Hide golden if showing; fix overlaps yourself.",
      check: (_c, api) => api.isLegal() && !api.isRevealed(),
    },
  ],
});
