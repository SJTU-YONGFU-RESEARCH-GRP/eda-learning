import {
  GOLDEN_POLISH,
  OUTLINE,
  evalPolish,
  isLegalPacking,
} from "../../assets/floorplanning-core.js";
import {
  createInteractiveFloorplanLab,
  emptyPack,
  el,
  packHasAll,
} from "../../assets/floorplanning-lab.js";

const root = document.getElementById("lab-root");
let tokens = [];

function polishResult() {
  if (!tokens.length) return null;
  try {
    return evalPolish(tokens);
  } catch {
    return null;
  }
}

createInteractiveFloorplanLab(root, {
  initialPack: emptyPack(),
  revealPack: evalPolish(GOLDEN_POLISH).pack,
  starterHtml: `
    <p><strong>Your job:</strong> build a polish expression with module / H / V buttons, then
    <strong>Evaluate polish</strong>. Challenges check the packing <em>you</em> evaluated — not a preloaded golden.</p>
  `,
  extraMetrics: () => [
    `polish: ${tokens.join(" ") || "(empty)"}`,
    `tokens: ${tokens.length}`,
  ],
  extraActions(ctx, api) {
    const add = (t) => () => {
      tokens = [...tokens, t];
      api.setRevealed(false);
      ctx.rerender();
    };
    const btns = ["A", "B", "C", "D", "E", "H", "V"].map((t) =>
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: t,
        onClick: add(t),
      })
    );
    btns.push(
      el("button", {
        className: "btn btn-ghost",
        type: "button",
        text: "⌫ Undo",
        onClick: () => {
          tokens = tokens.slice(0, -1);
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-ghost",
        type: "button",
        text: "Clear polish",
        onClick: () => {
          tokens = [];
          api.setPack({});
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Evaluate polish",
        onClick: () => {
          const r = polishResult();
          if (!r) return;
          api.setPack(r.pack);
          api.setRevealed(false);
          ctx.rerender();
        },
      })
    );
    return btns;
  },
  onChallengeSetup(_ctx, api) {
    tokens = [];
    api.setPack({});
  },
  onLoadStarter(api) {
    tokens = [];
    api.setPack({});
  },
  challenges: [
    {
      id: "push-a",
      title: "Start with A",
      level: "Intro",
      prompt: "Add token A to the polish (expression starts with A).",
      hint: "Click A in the polish buttons.",
      check: () => tokens[0] === "A",
    },
    {
      id: "stack-ad",
      title: "Build A D H",
      level: "Intro",
      prompt: "Polish equals A D H, then Evaluate — BB height should be 3.",
      hint: "Tokens A, D, H then Evaluate polish.",
      check: (_c, api) => {
        if (tokens.join(" ") !== "A D H") return false;
        const r = polishResult();
        if (!r) return false;
        api.setPack(r.pack);
        return r.h === 3 && r.w === 3;
      },
    },
    {
      id: "golden-tokens",
      title: "Enter golden polish",
      level: "Practice",
      prompt: "Enter A D H B V C V E V (nine tokens).",
      hint: "Click tokens in order; don’t Evaluate yet.",
      check: () => tokens.join(" ") === GOLDEN_POLISH.join(" "),
    },
    {
      id: "eval-bb",
      title: "Evaluate → BB 9×3",
      level: "Practice",
      prompt: "With the golden polish, Evaluate; bounding box must be 9×3.",
      hint: "Evaluate polish after entering the nine tokens.",
      check: (_c, api) => {
        if (tokens.join(" ") !== GOLDEN_POLISH.join(" ")) return false;
        const r = polishResult();
        if (!r) return false;
        const p = api.getPack();
        return r.w === 9 && r.h === 3 && packHasAll(p) && p.A;
      },
    },
    {
      id: "eval-legal",
      title: "Evaluated pack is legal",
      level: "Practice",
      prompt: "Golden polish evaluated; packing legal in 10×8.",
      hint: "Evaluate after golden tokens.",
      check: (_c, api) => {
        const r = polishResult();
        const p = api.getPack();
        return (
          tokens.join(" ") === GOLDEN_POLISH.join(" ") &&
          r &&
          r.w === 9 &&
          packHasAll(p) &&
          isLegalPacking(p)
        );
      },
    },
    {
      id: "fits-outline",
      title: "BB fits outline",
      level: "Practice",
      prompt: "Evaluated golden: bb.w ≤ 10 and bb.h ≤ 8.",
      hint: "9≤10 and 3≤8.",
      check: () => {
        const r = polishResult();
        return (
          tokens.join(" ") === GOLDEN_POLISH.join(" ") &&
          r &&
          r.w <= OUTLINE.w &&
          r.h <= OUTLINE.h
        );
      },
    },
    {
      id: "a-origin",
      title: "A at origin after eval",
      level: "Stretch",
      prompt: "After evaluating golden polish, A is at (0,0).",
      hint: "First leaf stays at origin in this evaluator.",
      check: (_c, api) => {
        const p = api.getPack();
        return (
          tokens.join(" ") === GOLDEN_POLISH.join(" ") &&
          p.A &&
          p.A.x === 0 &&
          p.A.y === 0
        );
      },
    },
    {
      id: "five-mods",
      title: "Five modules placed",
      level: "Stretch",
      prompt: "Evaluated golden packing has five modules.",
      hint: "Evaluate the nine-token polish.",
      check: (_c, api) =>
        tokens.join(" ") === GOLDEN_POLISH.join(" ") && packHasAll(api.getPack()),
    },
    {
      id: "no-reveal",
      title: "Without reveal button",
      level: "Stretch",
      prompt: "Legal evaluated golden pack with Reveal hidden.",
      hint: "Build + Evaluate yourself.",
      check: (_c, api) =>
        !api.isRevealed() &&
        tokens.join(" ") === GOLDEN_POLISH.join(" ") &&
        packHasAll(api.getPack()) &&
        isLegalPacking(api.getPack()),
    },
    {
      id: "token-count",
      title: "Nine tokens",
      level: "Stretch",
      prompt: "Polish length is 9 (golden).",
      hint: "5 operands + 4 operators.",
      check: () => tokens.length === 9 && tokens.join(" ") === GOLDEN_POLISH.join(" "),
    },
  ],
});
