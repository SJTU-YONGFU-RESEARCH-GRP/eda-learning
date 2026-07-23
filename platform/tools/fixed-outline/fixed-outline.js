import {
  GOLDEN_PACK,
  OUTLINE,
  isLegalPacking,
  legalityReport,
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
    <p><strong>Your job:</strong> place modules A–E inside the <code>10×8</code> outline so the packing is legal
    (no overflow, no interior overlap). Select a module, click the grid to set its lower-left.
    Challenges check <em>your</em> packing — Reveal golden is study-only.</p>
  `,
  challenges: [
    {
      id: "place-a",
      title: "Place module A",
      level: "Intro",
      prompt: "Place A somewhere fully inside the outline.",
      hint: "Select A, click a cell so A.x≥0, A.y≥0, A.x+3≤10, A.y+2≤8.",
      check: (_c, api) => {
        const a = api.getPack().A;
        return a && a.x >= 0 && a.y >= 0 && a.x + a.w <= OUTLINE.w && a.y + a.h <= OUTLINE.h;
      },
    },
    {
      id: "place-all",
      title: "Place all five",
      level: "Intro",
      prompt: "Place A, B, C, D, and E (positions can be rough).",
      hint: "Select each id and click the grid.",
      check: (_c, api) => packHasAll(api.getPack()),
    },
    {
      id: "legal-pack",
      title: "Make a legal packing",
      level: "Intro",
      prompt: "Produce any legal packing of all five modules.",
      hint: "No overlaps; stay inside 10×8. Try the bottom row then stack D on A.",
      check: (_c, api) => {
        const p = api.getPack();
        return packHasAll(p) && isLegalPacking(p);
      },
    },
    {
      id: "a-at-origin",
      title: "A at origin",
      level: "Practice",
      prompt: "In a legal packing, place A at (0,0).",
      hint: "Select A, click the lower-left corner cell.",
      check: (_c, api) => {
        const p = api.getPack();
        return p.A && p.A.x === 0 && p.A.y === 0 && isLegalPacking(p);
      },
    },
    {
      id: "e-not-overflow",
      title: "E must not overflow",
      level: "Practice",
      prompt: "Legal packing where E’s right edge is ≤ 10 (E.x + E.w ≤ 10).",
      hint: "E is 2 wide — max E.x is 8.",
      check: (_c, api) => {
        const p = api.getPack();
        return packHasAll(p) && isLegalPacking(p) && p.E.x + p.E.w <= 10;
      },
    },
    {
      id: "no-ce-overlap",
      title: "C and E do not overlap",
      level: "Practice",
      prompt: "Legal packing of all five (implies C and E don’t share interior).",
      hint: "If Check fails on overlap, move E further right.",
      check: (_c, api) => {
        const p = api.getPack();
        return packHasAll(p) && isLegalPacking(p) && legalityReport(p).reason === "ok";
      },
    },
    {
      id: "d-above-a",
      title: "D above A",
      level: "Practice",
      prompt: "Legal packing with A at (0,0) and D stacked on A (D.y ≥ 2, same x band).",
      hint: "A is height 2; put D at (0,2).",
      check: (_c, api) => {
        const p = api.getPack();
        return (
          p.A &&
          p.A.x === 0 &&
          p.A.y === 0 &&
          p.D &&
          p.D.y >= p.A.h &&
          p.D.x === 0 &&
          packHasAll(p) &&
          isLegalPacking(p)
        );
      },
    },
    {
      id: "match-golden-row",
      title: "Bottom row B–C–E",
      level: "Stretch",
      prompt: "Legal packing with B at (3,0), C at (5,0), E at (7,0).",
      hint: "Same bottom strip as the teaching golden.",
      check: (_c, api) => {
        const p = api.getPack();
        return (
          p.B &&
          p.B.x === 3 &&
          p.B.y === 0 &&
          p.C &&
          p.C.x === 5 &&
          p.C.y === 0 &&
          p.E &&
          p.E.x === 7 &&
          p.E.y === 0 &&
          isLegalPacking(p)
        );
      },
    },
    {
      id: "full-golden",
      title: "Recreate teaching golden",
      level: "Stretch",
      prompt: "Match the teaching golden positions for A–E (legal).",
      hint: "A(0,0) D(0,2) B(3,0) C(5,0) E(7,0).",
      check: (_c, api) => {
        const p = api.getPack();
        const g = GOLDEN_PACK;
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
      id: "legal-not-reveal",
      title: "Legal without relying on reveal",
      level: "Stretch",
      prompt: "Any legal all-five packing while Reveal is off (Hide golden if needed).",
      hint: "Clear, then place yourself. Reveal must be hidden.",
      check: (_c, api) =>
        !api.isRevealed() && packHasAll(api.getPack()) && isLegalPacking(api.getPack()),
    },
  ],
});
