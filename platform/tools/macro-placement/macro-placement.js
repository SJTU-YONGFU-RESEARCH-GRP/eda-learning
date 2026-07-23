import {
  GOLDEN_PACK,
  MACRO_PACK,
  isLegalPacking,
} from "../../assets/floorplanning-core.js";
import {
  createInteractiveFloorplanLab,
  packHasAll,
} from "../../assets/floorplanning-lab.js";

const root = document.getElementById("lab-root");

const seed = {
  D: { x: 0, y: 0, w: 3, h: 1, macro: true },
};

createInteractiveFloorplanLab(root, {
  initialPack: seed,
  lockedIds: ["D"],
  revealPack: MACRO_PACK,
  starterHtml: `
    <p><strong>Your job:</strong> macro <strong>D is locked</strong> at (0,0).
    Place A, B, C, E around it without overlaps. You cannot move D.</p>
  `,
  challenges: [
    {
      id: "d-locked",
      title: "D stays at origin",
      level: "Intro",
      prompt: "D remains at (0,0) as the fixed macro.",
      hint: "Don’t try to move D — it’s locked.",
      check: (_c, api) => {
        const d = api.getPack().D;
        return d && d.x === 0 && d.y === 0 && d.macro === true;
      },
    },
    {
      id: "place-a-above",
      title: "Place A above D",
      level: "Intro",
      prompt: "Place A with A.y ≥ 1 (above the macro strip).",
      hint: "Select A, click at (0,1).",
      check: (_c, api) => {
        const p = api.getPack();
        return p.D && p.A && p.A.y >= p.D.h;
      },
    },
    {
      id: "place-rest",
      title: "Place B C E",
      level: "Intro",
      prompt: "Place B, C, and E as well (five modules present).",
      hint: "Keep D fixed; fill the right side.",
      check: (_c, api) => packHasAll(api.getPack()) && api.getPack().D.macro,
    },
    {
      id: "legal-macro",
      title: "Legal around macro",
      level: "Practice",
      prompt: "All five placed, D fixed at (0,0), packing legal.",
      hint: "A above D; B/C/E to the right.",
      check: (_c, api) => {
        const p = api.getPack();
        return (
          packHasAll(p) &&
          p.D.x === 0 &&
          p.D.y === 0 &&
          p.D.macro &&
          isLegalPacking(p)
        );
      },
    },
    {
      id: "d-size",
      title: "D size 3×1",
      level: "Practice",
      prompt: "Macro D remains 3×1 in a legal packing.",
      hint: "Hard macro size.",
      check: (_c, api) => {
        const d = api.getPack().D;
        return d && d.w === 3 && d.h === 1 && isLegalPacking(api.getPack());
      },
    },
    {
      id: "differs-free",
      title: "Differs from free golden D",
      level: "Practice",
      prompt: "Legal macro packing where D is not at free-golden (0,2).",
      hint: "D is at (0,0) here.",
      check: (_c, api) => {
        const p = api.getPack();
        return (
          packHasAll(p) &&
          isLegalPacking(p) &&
          (p.D.x !== GOLDEN_PACK.D.x || p.D.y !== GOLDEN_PACK.D.y)
        );
      },
    },
    {
      id: "a-above-strict",
      title: "A stacked on D",
      level: "Practice",
      prompt: "Legal packing with A at (0,1) above D.",
      hint: "Teaching macro pack uses A@(0,1).",
      check: (_c, api) => {
        const p = api.getPack();
        return p.A && p.A.x === 0 && p.A.y === 1 && packHasAll(p) && isLegalPacking(p);
      },
    },
    {
      id: "match-macro",
      title: "Match macro teaching pack",
      level: "Stretch",
      prompt: "Match MACRO_PACK positions for A–E.",
      hint: "D(0,0) A(0,1) B(3,0) C(5,0) E(7,0).",
      check: (_c, api) => {
        const p = api.getPack();
        const g = MACRO_PACK;
        return (
          packHasAll(p) &&
          isLegalPacking(p) &&
          ["A", "B", "C", "D", "E"].every(
            (id) => p[id].x === g[id].x && p[id].y === g[id].y
          )
        );
      },
    },
    {
      id: "cannot-clear-d",
      title: "Clear keeps D",
      level: "Stretch",
      prompt: "Place A then Clear — D remains, A is gone.",
      hint: "Place A, click Clear; only locked D should remain.",
      check: (_c, api) => {
        const p = api.getPack();
        return p.D && p.D.x === 0 && p.D.y === 0 && !p.A && Object.keys(p).length === 1;
      },
    },
    {
      id: "no-reveal",
      title: "Legal without reveal",
      level: "Stretch",
      prompt: "Legal macro packing with Reveal hidden.",
      hint: "Place around locked D yourself.",
      check: (_c, api) =>
        !api.isRevealed() &&
        packHasAll(api.getPack()) &&
        api.getPack().D?.macro &&
        isLegalPacking(api.getPack()),
    },
  ],
});
