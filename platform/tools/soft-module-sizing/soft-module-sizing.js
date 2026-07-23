import {
  GOLDEN_PACK,
  SOFT_A_PACK,
  isLegalPacking,
} from "../../assets/floorplanning-core.js";
import {
  createInteractiveFloorplanLab,
  emptyPack,
  packHasAll,
} from "../../assets/floorplanning-lab.js";

const root = document.getElementById("lab-root");

createInteractiveFloorplanLab(root, {
  initialPack: emptyPack(),
  revealPack: SOFT_A_PACK,
  allowSoftToggle: true,
  starterHtml: `
    <p><strong>Your job:</strong> reshape soft module A (area stays 6) with
    <strong>A → 3×2</strong> / <strong>A → 2×3</strong>, then place a legal packing.
    Hard modules keep fixed sizes.</p>
  `,
  challenges: [
    {
      id: "a-soft",
      title: "A is soft",
      level: "Intro",
      prompt: "Confirm A is marked soft in the module list.",
      hint: "Always true on the starter modules.",
      check: (_c, api) => api.getModules().find((m) => m.id === "A")?.soft === true,
    },
    {
      id: "reshape-23",
      title: "Reshape A to 2×3",
      level: "Intro",
      prompt: "Click A → 2×3 so A’s size becomes 2×3 (area 6).",
      hint: "Soft toggle buttons.",
      check: (_c, api) => {
        const a = api.getModules().find((m) => m.id === "A");
        return a && a.w === 2 && a.h === 3 && a.w * a.h === 6;
      },
    },
    {
      id: "area-kept",
      title: "Area still 6",
      level: "Intro",
      prompt: "After reshape to 2×3, area is 6.",
      hint: "2×3=6.",
      check: (_c, api) => {
        const a = api.getModules().find((m) => m.id === "A");
        return a && a.w * a.h === 6;
      },
    },
    {
      id: "place-soft-legal",
      title: "Legal pack with soft A",
      level: "Practice",
      prompt: "A is 2×3; place all five legally.",
      hint: "Reshape first, then place (or mimic soft golden).",
      check: (_c, api) => {
        const a = api.getModules().find((m) => m.id === "A");
        const p = api.getPack();
        return a?.w === 2 && a?.h === 3 && packHasAll(p) && isLegalPacking(p) && p.A.w === 2;
      },
    },
    {
      id: "hard-32",
      title: "Back to hard 3×2 packing",
      level: "Practice",
      prompt: "Set A → 3×2 and produce a legal all-five packing.",
      hint: "A → 3×2 then place.",
      check: (_c, api) => {
        const a = api.getModules().find((m) => m.id === "A");
        const p = api.getPack();
        return a?.w === 3 && a?.h === 2 && packHasAll(p) && isLegalPacking(p);
      },
    },
    {
      id: "b-hard",
      title: "B stays hard",
      level: "Practice",
      prompt: "B is not soft.",
      hint: "Only A is soft.",
      check: (_c, api) => api.getModules().find((m) => m.id === "B")?.soft === false,
    },
    {
      id: "aspect-bounds",
      title: "Aspect bounds",
      level: "Practice",
      prompt: "A.aspect_min is 0.5 and aspect_max is 2.",
      hint: "Soft metadata.",
      check: (_c, api) => {
        const a = api.getModules().find((m) => m.id === "A");
        return a && a.aspect_min === 0.5 && a.aspect_max === 2.0;
      },
    },
    {
      id: "match-soft-golden",
      title: "Match soft teaching pack",
      level: "Stretch",
      prompt: "A is 2×3 and positions match the soft teaching golden.",
      hint: "Reveal is optional; better to place: A(0,0) B(2,0) C(4,0) D(4,2) E(7,0).",
      check: (_c, api) => {
        const p = api.getPack();
        const g = SOFT_A_PACK;
        return (
          api.getModules().find((m) => m.id === "A")?.w === 2 &&
          packHasAll(p) &&
          isLegalPacking(p) &&
          ["A", "B", "C", "D", "E"].every(
            (id) => p[id].x === g[id].x && p[id].y === g[id].y && p[id].w === g[id].w
          )
        );
      },
    },
    {
      id: "soft-not-overflow",
      title: "Soft A still inside",
      level: "Stretch",
      prompt: "Legal packing with A at 2×3 fully inside outline.",
      hint: "A.x+2≤10, A.y+3≤8.",
      check: (_c, api) => {
        const p = api.getPack();
        return (
          p.A &&
          p.A.w === 2 &&
          p.A.h === 3 &&
          packHasAll(p) &&
          isLegalPacking(p)
        );
      },
    },
    {
      id: "no-reveal",
      title: "Soft legal without reveal",
      level: "Stretch",
      prompt: "A is 2×3, legal packing, Reveal hidden.",
      hint: "Reshape + place yourself.",
      check: (_c, api) => {
        const a = api.getModules().find((m) => m.id === "A");
        return (
          !api.isRevealed() &&
          a?.w === 2 &&
          a?.h === 3 &&
          packHasAll(api.getPack()) &&
          isLegalPacking(api.getPack())
        );
      },
    },
  ],
});
