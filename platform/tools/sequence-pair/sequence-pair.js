import {
  GOLDEN_SP,
  isLegalPacking,
  packSequencePair,
} from "../../assets/floorplanning-core.js";
import {
  createInteractiveFloorplanLab,
  emptyPack,
  el,
  packHasAll,
} from "../../assets/floorplanning-lab.js";

const root = document.getElementById("lab-root");
let pos = [];
let neg = [];
let ran = false;

function sameSet(a, b) {
  return [...a].sort().join() === [...b].sort().join();
}

createInteractiveFloorplanLab(root, {
  initialPack: emptyPack(),
  revealPack: packSequencePair(GOLDEN_SP.pos, GOLDEN_SP.neg),
  starterHtml: `
    <p><strong>Your job:</strong> build <code>pos</code> and <code>neg</code> permutations, then
    <strong>Pack sequence pair</strong>. Teaching golden is pos <code>A B C E D</code>,
    neg <code>D A B C E</code>.</p>
  `,
  extraMetrics: () => [
    `pos: ${pos.join(" ") || "(empty)"}`,
    `neg: ${neg.join(" ") || "(empty)"}`,
    `packerRan: ${ran}`,
  ],
  extraActions(ctx, api) {
    const pushPos = (id) => () => {
      if (!pos.includes(id)) pos = [...pos, id];
      ran = false;
      ctx.rerender();
    };
    const pushNeg = (id) => () => {
      if (!neg.includes(id)) neg = [...neg, id];
      ran = false;
      ctx.rerender();
    };
    const btns = [];
    for (const id of ["A", "B", "C", "D", "E"]) {
      btns.push(
        el("button", {
          className: "btn btn-secondary",
          type: "button",
          text: `pos+${id}`,
          onClick: pushPos(id),
        })
      );
    }
    for (const id of ["A", "B", "C", "D", "E"]) {
      btns.push(
        el("button", {
          className: "btn btn-secondary",
          type: "button",
          text: `neg+${id}`,
          onClick: pushNeg(id),
        })
      );
    }
    btns.push(
      el("button", {
        className: "btn btn-ghost",
        type: "button",
        text: "Clear seqs",
        onClick: () => {
          pos = [];
          neg = [];
          ran = false;
          api.setPack({});
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Pack sequence pair",
        onClick: () => {
          if (pos.length !== 5 || neg.length !== 5 || !sameSet(pos, neg)) return;
          api.setPack(packSequencePair(pos, neg));
          api.setRevealed(false);
          ran = true;
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-ghost",
        type: "button",
        text: "Load golden seqs",
        onClick: () => {
          pos = [...GOLDEN_SP.pos];
          neg = [...GOLDEN_SP.neg];
          ran = false;
          ctx.rerender();
        },
      })
    );
    return btns;
  },
  onChallengeSetup(_ctx, api) {
    pos = [];
    neg = [];
    ran = false;
    api.setPack({});
  },
  onLoadStarter(api) {
    pos = [];
    neg = [];
    ran = false;
    api.setPack({});
  },
  challenges: [
    {
      id: "pos-a",
      title: "Pos starts building",
      level: "Intro",
      prompt: "Add A to pos (first entry).",
      hint: "Click pos+A.",
      check: () => pos[0] === "A",
    },
    {
      id: "golden-seqs",
      title: "Enter golden sequences",
      level: "Intro",
      prompt: "pos = A B C E D and neg = D A B C E.",
      hint: "Use pos+/neg+ buttons or Load golden seqs.",
      check: () =>
        pos.join(" ") === GOLDEN_SP.pos.join(" ") &&
        neg.join(" ") === GOLDEN_SP.neg.join(" "),
    },
    {
      id: "pack-run",
      title: "Pack the pair",
      level: "Intro",
      prompt: "With golden seqs, click Pack sequence pair.",
      hint: "Sequences must be complete first.",
      check: () =>
        ran &&
        pos.join(" ") === GOLDEN_SP.pos.join(" ") &&
        neg.join(" ") === GOLDEN_SP.neg.join(" "),
    },
    {
      id: "legal",
      title: "Legal SP packing",
      level: "Practice",
      prompt: "Packed golden SP is legal with five modules.",
      hint: "Pack sequence pair.",
      check: (_c, api) =>
        ran && packHasAll(api.getPack()) && isLegalPacking(api.getPack()),
    },
    {
      id: "same-set",
      title: "Same id set",
      level: "Practice",
      prompt: "Pos and neg are permutations of the same five ids.",
      hint: "Both must include A–E once.",
      check: () => pos.length === 5 && neg.length === 5 && sameSet(pos, neg),
    },
    {
      id: "pos-len",
      title: "Pos length 5",
      level: "Practice",
      prompt: "Positive sequence has 5 modules.",
      hint: "Add each id once to pos.",
      check: () => pos.length === 5,
    },
    {
      id: "neg-d",
      title: "Neg starts with D",
      level: "Practice",
      prompt: "On the golden neg, first id is D.",
      hint: "neg = D A B C E.",
      check: () => neg[0] === "D" && neg.join(" ") === GOLDEN_SP.neg.join(" "),
    },
    {
      id: "nonneg",
      title: "Non-negative coords",
      level: "Stretch",
      prompt: "After packing golden SP, all coords ≥ 0.",
      hint: "Pack sequence pair.",
      check: (_c, api) =>
        ran && Object.values(api.getPack()).every((r) => r.x >= 0 && r.y >= 0),
    },
    {
      id: "a-placed",
      title: "A placed",
      level: "Stretch",
      prompt: "A is in the packed result.",
      hint: "Pack after golden seqs.",
      check: (_c, api) => ran && !!api.getPack().A,
    },
    {
      id: "no-reveal",
      title: "Pack without reveal",
      level: "Stretch",
      prompt: "Legal SP pack with Reveal hidden.",
      hint: "Pack sequence pair yourself.",
      check: (_c, api) =>
        ran &&
        !api.isRevealed() &&
        packHasAll(api.getPack()) &&
        isLegalPacking(api.getPack()),
    },
  ],
});
