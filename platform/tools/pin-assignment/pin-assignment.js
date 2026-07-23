import {
  GOLDEN_PACK,
  GOLDEN_PINS,
  OUTLINE,
  pinsValid,
} from "../../assets/floorplanning-core.js";
import {
  createInteractiveFloorplanLab,
  el,
} from "../../assets/floorplanning-lab.js";

const root = document.getElementById("lab-root");

createInteractiveFloorplanLab(root, {
  initialPack: GOLDEN_PACK,
  initialPins: [],
  revealPack: GOLDEN_PACK,
  starterHtml: `
    <p><strong>Your job:</strong> assign I/O pins on outline edges.
    Use <strong>Add pin on side</strong> buttons (cycles offsets) or
    <strong>Assign golden pins</strong> then edit. Empty pins are invalid —
    cover left, right, top, and bottom.</p>
  `,
  extraMetrics: (api) => {
    const pins = api.getPins();
    return [
      `pins: ${pins.map((p) => `${p.id}@${p.side}:${p.offset}`).join(", ") || "—"}`,
      `valid: ${pinsValid(pins)}`,
      `sides: ${[...new Set(pins.map((p) => p.side))].join(",") || "—"}`,
    ];
  },
  extraActions(ctx, api) {
    const addSide = (side) => () => {
      const pins = api.getPins();
      const lim = side === "left" || side === "right" ? OUTLINE.h : OUTLINE.w;
      const id = `P${pins.length}`;
      const offset = Math.min(2 + pins.length, lim);
      api.setPins([...pins, { id, side, offset }]);
      api.setRevealed(false);
      ctx.rerender();
    };
    return [
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: "+ left",
        onClick: addSide("left"),
      }),
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: "+ right",
        onClick: addSide("right"),
      }),
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: "+ top",
        onClick: addSide("top"),
      }),
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: "+ bottom",
        onClick: addSide("bottom"),
      }),
      el("button", {
        className: "btn btn-ghost",
        type: "button",
        text: "Clear pins",
        onClick: () => {
          api.setPins([]);
          api.setRevealed(false);
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Assign golden pins",
        onClick: () => {
          api.setPins(GOLDEN_PINS.map((p) => ({ ...p })));
          api.setRevealed(false);
          ctx.rerender();
        },
      }),
    ];
  },
  onChallengeSetup(_ctx, api) {
    api.setPins([]);
  },
  challenges: [
    {
      id: "empty-invalid",
      title: "Empty is invalid",
      level: "Intro",
      prompt: "With no pins, pinsValid is false.",
      hint: "Clear pins if needed.",
      check: (_c, api) => api.getPins().length === 0 && !pinsValid(api.getPins()),
    },
    {
      id: "add-four-sides",
      title: "Cover four sides",
      level: "Intro",
      prompt: "Add at least one pin on each of left, right, top, bottom.",
      hint: "Click + left/right/top/bottom once each.",
      check: (_c, api) => {
        const sides = new Set(api.getPins().map((p) => p.side));
        return sides.has("left") && sides.has("right") && sides.has("top") && sides.has("bottom");
      },
    },
    {
      id: "valid",
      title: "Make pinsValid true",
      level: "Intro",
      prompt: "Produce a pin set where pinsValid returns true.",
      hint: "Four sides with in-range offsets — golden works.",
      check: (_c, api) => pinsValid(api.getPins()),
    },
    {
      id: "count-4",
      title: "Exactly four pins",
      level: "Practice",
      prompt: "Valid set with exactly four pins.",
      hint: "One per side.",
      check: (_c, api) => api.getPins().length === 4 && pinsValid(api.getPins()),
    },
    {
      id: "has-left",
      title: "Has left pin",
      level: "Practice",
      prompt: "Valid pins including a left-side pin.",
      hint: "+ left or golden.",
      check: (_c, api) =>
        pinsValid(api.getPins()) && api.getPins().some((p) => p.side === "left"),
    },
    {
      id: "has-top",
      title: "Has top pin",
      level: "Practice",
      prompt: "Valid pins including a top-side pin.",
      hint: "+ top.",
      check: (_c, api) =>
        pinsValid(api.getPins()) && api.getPins().some((p) => p.side === "top"),
    },
    {
      id: "golden-set",
      title: "Match golden pin ids",
      level: "Practice",
      prompt: "Assign golden pins (P0–P3 on the four sides).",
      hint: "Assign golden pins button.",
      check: (_c, api) => {
        const pins = api.getPins();
        const ids = pins.map((p) => p.id).sort().join();
        return ids === "P0,P1,P2,P3" && pinsValid(pins);
      },
    },
    {
      id: "p0-left",
      title: "P0 on left",
      level: "Stretch",
      prompt: "Golden-style: P0 is on the left side.",
      hint: "Assign golden pins.",
      check: (_c, api) => api.getPins().find((p) => p.id === "P0")?.side === "left",
    },
    {
      id: "clear-again",
      title: "Clear breaks validity",
      level: "Stretch",
      prompt: "After Clear pins, valid is false.",
      hint: "Clear pins button.",
      check: (_c, api) => api.getPins().length === 0 && !pinsValid([]),
    },
    {
      id: "rebuild-valid",
      title: "Rebuild without peeking pack",
      level: "Stretch",
      prompt: "Valid four-side pin set (Reveal irrelevant).",
      hint: "Add one pin per side.",
      check: (_c, api) => {
        const pins = api.getPins();
        const sides = new Set(pins.map((p) => p.side));
        return pinsValid(pins) && sides.size === 4;
      },
    },
  ],
});
