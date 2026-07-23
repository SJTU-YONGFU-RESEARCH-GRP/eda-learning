import {
  GOLDENS,
  OVERLAP_PLACEMENT,
  abacusLegalize,
  createInteractiveLegalizationLab,
  el,
  positionsNear,
} from "../../assets/interactive-legalization-lab.js";

const root = document.getElementById("lab-root");
const AFTER = abacusLegalize(OVERLAP_PLACEMENT);

createInteractiveLegalizationLab(root, {
  initialPositions: OVERLAP_PLACEMENT,
  revealPositions: AFTER,
  originPositions: OVERLAP_PLACEMENT,
  starterHtml: `
    <p><strong>Your job:</strong> cost = HPWL + λ·displacement. Legalize (hand or
    <strong>Apply Abacus</strong>) to HPWL <strong>38</strong> / disp <strong>4</strong>,
    then read cost at λ=<strong>1</strong> → <strong>${GOLDENS.abacusCostLambda1}</strong>
    and λ=<strong>5</strong> → <strong>${GOLDENS.abacusCostLambda5}</strong>.</p>
  `,
  extraActions(ctx, api) {
    return [
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Apply Abacus",
        onClick: () => {
          api.setPositions(abacusLegalize(OVERLAP_PLACEMENT));
          api.setOrigin(OVERLAP_PLACEMENT);
          api.setRevealed(false);
          ctx.rerender();
        },
      }),
    ];
  },
  extraMetrics(api) {
    return [
      `cost λ=1: ${api.cost(1)}`,
      `cost λ=5: ${api.cost(5)}`,
      `formula: HPWL + λ·disp`,
    ];
  },
  challenges: [
    {
      id: "abacus-metrics",
      title: "Abacus HPWL 38 / disp 4",
      level: "Intro",
      prompt: "Reach Abacus teaching metrics (HPWL 38, disp 4).",
      hint: "Reset → Apply Abacus.",
      check: (_c, api) =>
        api.isLegal() &&
        api.hpwl() === GOLDENS.abacusHpwl &&
        api.displacement() === GOLDENS.abacusDisp,
    },
    {
      id: "cost-l1",
      title: "Cost λ=1 is 42",
      level: "Intro",
      prompt: "With Abacus result, cost(1) = 42.",
      hint: "38 + 1×4.",
      check: (_c, api) =>
        api.hpwl() === 38 &&
        api.displacement() === 4 &&
        api.cost(1) === GOLDENS.abacusCostLambda1,
    },
    {
      id: "cost-l5",
      title: "Cost λ=5 is 58",
      level: "Intro",
      prompt: "With Abacus result, cost(5) = 58.",
      hint: "38 + 5×4.",
      check: (_c, api) =>
        api.hpwl() === 38 &&
        api.displacement() === 4 &&
        api.cost(5) === GOLDENS.abacusCostLambda5,
    },
    {
      id: "lambda-grows",
      title: "Higher λ raises cost",
      level: "Practice",
      prompt: "cost(5) > cost(1) on the Abacus packing.",
      hint: "Apply Abacus; compare metrics.",
      check: (_c, api) => api.cost(5) > api.cost(1),
    },
    {
      id: "formula-check",
      title: "Formula holds",
      level: "Practice",
      prompt: "cost(1) equals HPWL + disp.",
      hint: "Apply Abacus.",
      check: (_c, api) => api.cost(1) === api.hpwl() + api.displacement(),
    },
    {
      id: "formula-l5",
      title: "Formula at λ=5",
      level: "Practice",
      prompt: "cost(5) equals HPWL + 5·disp.",
      hint: "Apply Abacus.",
      check: (_c, api) => api.cost(5) === api.hpwl() + 5 * api.displacement(),
    },
    {
      id: "match-abacus",
      title: "Match Abacus packing",
      level: "Practice",
      prompt: "Match Apply Abacus coordinates.",
      hint: "Reset → Apply.",
      check: (_c, api) => positionsNear(api.getPositions(), AFTER),
    },
    {
      id: "goldens-42-58",
      title: "GOLDENS costs",
      level: "Stretch",
      prompt: "GOLDENS list λ1=42 and λ5=58.",
      hint: "Instance constants.",
      check: () =>
        GOLDENS.abacusCostLambda1 === 42 && GOLDENS.abacusCostLambda5 === 58,
    },
    {
      id: "illegal-cost",
      title: "Starter still illegal",
      level: "Stretch",
      prompt: "Reset: packing illegal before you legalize.",
      hint: "Reset workspace.",
      check: (_c, api) => !api.isLegal(),
    },
    {
      id: "legal-no-reveal",
      title: "Cost 42 without reveal",
      level: "Stretch",
      prompt: "cost(1)=42 with Reveal off.",
      hint: "Hide golden; Apply Abacus.",
      check: (_c, api) =>
        !api.isRevealed() && api.cost(1) === GOLDENS.abacusCostLambda1 && api.isLegal(),
    },
  ],
});
