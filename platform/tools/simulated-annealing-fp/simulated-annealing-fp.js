import {
  BAD_PACK,
  GOLDEN_PACK,
  cost,
  hpwl,
  isLegalPacking,
  saSwap,
} from "../../assets/floorplanning-core.js";
import {
  createInteractiveFloorplanLab,
  el,
  packHasAll,
} from "../../assets/floorplanning-lab.js";

const root = document.getElementById("lab-root");
let swapA = "A";
let swapB = "E";
let improved = false;

createInteractiveFloorplanLab(root, {
  initialPack: BAD_PACK,
  revealPack: GOLDEN_PACK,
  starterHtml: `
    <p><strong>Your job:</strong> start from an <em>illegal</em> bad seed (cost ≥ 1000).
    Swap module positions or rebuild a legal packing until cost drops below 1000.
    Select two ids and click <strong>Swap selected pair</strong>.</p>
  `,
  extraMetrics: (api) => [
    `cost: ${cost(api.getPack()).toFixed(2)}`,
    `hpwl: ${hpwl(api.getPack()).toFixed(2)}`,
    `swapPair: ${swapA}↔${swapB}`,
    `improvedFlag: ${improved}`,
  ],
  extraActions(ctx, api) {
    return [
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: "Reset bad seed",
        onClick: () => {
          api.setPack(BAD_PACK);
          api.setRevealed(false);
          improved = false;
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: `Set swap A=${api.getSelected()}`,
        onClick: () => {
          swapA = api.getSelected();
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: `Set swap B=${api.getSelected()}`,
        onClick: () => {
          swapB = api.getSelected();
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Swap selected pair",
        onClick: () => {
          const p = api.getPack();
          if (!p[swapA] || !p[swapB]) return;
          api.setPack(saSwap(p, swapA, swapB));
          api.setRevealed(false);
          if (isLegalPacking(api.getPack()) && cost(api.getPack()) < 1000) improved = true;
          ctx.rerender();
        },
      }),
    ];
  },
  onChallengeSetup(_ctx, api) {
    api.setPack(BAD_PACK);
    improved = false;
    swapA = "A";
    swapB = "E";
  },
  challenges: [
    {
      id: "see-bad",
      title: "Bad seed is illegal",
      level: "Intro",
      prompt: "Start packing is illegal with cost ≥ 1000.",
      hint: "Reset bad seed if you changed it.",
      check: (_c, api) => !isLegalPacking(api.getPack()) && cost(api.getPack()) >= 1000,
    },
    {
      id: "fix-e",
      title: "Fix E overflow",
      level: "Intro",
      prompt: "Move/place so E no longer overflows (legal packing of all five).",
      hint: "Select E and nudge left, or rebuild. E.x ≤ 8.",
      check: (_c, api) => packHasAll(api.getPack()) && isLegalPacking(api.getPack()),
    },
    {
      id: "cost-under",
      title: "Cost below 1000",
      level: "Intro",
      prompt: "Reach a legal packing with cost &lt; 1000.",
      hint: "Illegal penalty is +1000.",
      check: (_c, api) =>
        packHasAll(api.getPack()) &&
        isLegalPacking(api.getPack()) &&
        cost(api.getPack()) < 1000,
    },
    {
      id: "beats-bad",
      title: "Beat bad cost",
      level: "Practice",
      prompt: "Your cost must be strictly less than cost(bad seed).",
      hint: "Any legal packing works.",
      check: (_c, api) =>
        isLegalPacking(api.getPack()) && cost(api.getPack()) < cost(BAD_PACK),
    },
    {
      id: "swap-once",
      title: "Perform a swap",
      level: "Practice",
      prompt: "From bad seed, set swap pair and Swap once (state may still be illegal).",
      hint: "Set swap A/B then Swap selected pair.",
      check: (_c, api) => {
        // After at least one user edit from identical BAD positions for E
        const p = api.getPack();
        return p.E && (p.E.x !== BAD_PACK.E.x || p.E.y !== BAD_PACK.E.y || isLegalPacking(p));
      },
    },
    {
      id: "hpwl-finite",
      title: "HPWL finite when legal",
      level: "Practice",
      prompt: "Legal packing with finite HPWL.",
      hint: "Fix legality first.",
      check: (_c, api) =>
        isLegalPacking(api.getPack()) && Number.isFinite(hpwl(api.getPack())),
    },
    {
      id: "sizes-kept",
      title: "Sizes preserved",
      level: "Practice",
      prompt: "Legal packing where A is still 3×2.",
      hint: "Swaps move coordinates only.",
      check: (_c, api) => {
        const a = api.getPack().A;
        return a && a.w === 3 && a.h === 2 && isLegalPacking(api.getPack());
      },
    },
    {
      id: "near-golden-cost",
      title: "Near golden quality",
      level: "Stretch",
      prompt: "Legal packing with cost ≤ cost(golden) + 5.",
      hint: "Match the golden layout or get close.",
      check: (_c, api) =>
        isLegalPacking(api.getPack()) && cost(api.getPack()) <= cost(GOLDEN_PACK) + 5,
    },
    {
      id: "all-five-legal",
      title: "All five legal",
      level: "Stretch",
      prompt: "All five placed and legal.",
      hint: "Place or swap until legal.",
      check: (_c, api) => packHasAll(api.getPack()) && isLegalPacking(api.getPack()),
    },
    {
      id: "no-reveal",
      title: "Improve without reveal",
      level: "Stretch",
      prompt: "Legal cost &lt; 1000 with Reveal hidden.",
      hint: "Don’t use Reveal golden.",
      check: (_c, api) =>
        !api.isRevealed() &&
        packHasAll(api.getPack()) &&
        isLegalPacking(api.getPack()) &&
        cost(api.getPack()) < 1000,
    },
  ],
});
