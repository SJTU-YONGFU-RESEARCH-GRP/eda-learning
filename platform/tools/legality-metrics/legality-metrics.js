import {
  GOLDEN_PLACEMENT,
  OVERLAP_PLACEMENT,
  createInteractiveLegalizationLab,
  el,
  overlapRemoval,
  positionsNear,
} from "../../assets/interactive-legalization-lab.js";

const root = document.getElementById("lab-root");
const AFTER = overlapRemoval(OVERLAP_PLACEMENT);

createInteractiveLegalizationLab(root, {
  initialPositions: OVERLAP_PLACEMENT,
  revealPositions: GOLDEN_PLACEMENT,
  originPositions: OVERLAP_PLACEMENT,
  starterHtml: `
    <p><strong>Your job:</strong> read legality on the overlap seed (A/B/C stacked), then
    fix it by hand or <strong>Apply overlap removal</strong>. Challenges check <em>your</em>
    packing — Reveal golden is study-only.</p>
  `,
  extraActions(ctx, api) {
    return [
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Apply overlap removal",
        onClick: () => {
          api.setPositions(overlapRemoval(api.getPositions()));
          api.setRevealed(false);
          ctx.rerender();
        },
      }),
    ];
  },
  challenges: [
    {
      id: "illegal-start",
      title: "Starter illegal",
      level: "Intro",
      prompt: "On the overlap starter, packing is illegal.",
      hint: "Reset workspace.",
      check: (_c, api) => !api.isLegal(),
    },
    {
      id: "reason-overlap",
      title: "Reason: overlap",
      level: "Intro",
      prompt: "Legality report mentions overlap (A/B).",
      hint: "Reset; read metrics reason.",
      check: (_c, api) => {
        const r = api.legalityReport();
        return !r.legal && r.reason.includes("overlap");
      },
    },
    {
      id: "make-legal",
      title: "Make legal",
      level: "Intro",
      prompt: "Produce a legal packing.",
      hint: "Apply overlap removal, or nudge A/B/C apart on the row.",
      check: (_c, api) => api.isLegal(),
    },
    {
      id: "reason-ok",
      title: "Reason ok",
      level: "Practice",
      prompt: "When legal, report reason is ok.",
      hint: "Fix overlaps first.",
      check: (_c, api) => api.isLegal() && api.legalityReport().reason === "ok",
    },
    {
      id: "disp-after",
      title: "Displacement after repair",
      level: "Practice",
      prompt: "After overlap removal (or matching pack), disp vs origin is 6.",
      hint: "Reset, Apply overlap removal.",
      check: (_c, api) => api.isLegal() && api.displacement() === 6,
    },
    {
      id: "hpwl-32",
      title: "HPWL 32 after repair",
      level: "Practice",
      prompt: "Legal packing with HPWL 32 (teaching overlap-removal result).",
      hint: "Apply overlap removal from starter.",
      check: (_c, api) => api.isLegal() && api.hpwl() === 32,
    },
    {
      id: "match-removal",
      title: "Match overlap-removal coords",
      level: "Practice",
      prompt: "Match the Apply overlap-removal result.",
      hint: "Reset → Apply.",
      check: (_c, api) => positionsNear(api.getPositions(), AFTER),
    },
    {
      id: "golden-legal",
      title: "Golden is legal",
      level: "Stretch",
      prompt: "Reveal golden: packing is legal with reason ok.",
      hint: "Reveal golden (study).",
      check: (_c, api) =>
        api.isRevealed() && api.isLegal() && api.legalityReport().reason === "ok",
    },
    {
      id: "site-aligned",
      title: "Site-aligned when legal",
      level: "Stretch",
      prompt: "Any legal packing implies site-aligned x and on-row y.",
      hint: "Make legal; metrics should say ok.",
      check: (_c, api) => api.isLegal() && api.legalityReport().reason === "ok",
    },
    {
      id: "legal-no-reveal",
      title: "Legal without reveal",
      level: "Stretch",
      prompt: "Legal packing with Reveal off.",
      hint: "Hide golden; Apply overlap removal.",
      check: (_c, api) => api.isLegal() && !api.isRevealed(),
    },
  ],
});
