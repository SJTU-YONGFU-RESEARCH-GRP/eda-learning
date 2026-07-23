import {
  isLegalPacking,
  packHierarchical,
} from "../../assets/floorplanning-core.js";
import {
  createInteractiveFloorplanLab,
  emptyPack,
  el,
  packHasAll,
} from "../../assets/floorplanning-lab.js";

const root = document.getElementById("lab-root");
let ran = false;

createInteractiveFloorplanLab(root, {
  initialPack: emptyPack(),
  revealPack: packHierarchical(),
  starterHtml: `
    <p><strong>Your job:</strong> either click <strong>Pack hierarchy</strong>
    (AB left, CDE right @ x=5) or place clusters yourself so left modules have x&lt;5
    and right modules have x≥5.</p>
  `,
  extraActions(ctx, api) {
    return [
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Pack hierarchy",
        onClick: () => {
          api.setPack(packHierarchical());
          api.setRevealed(false);
          ran = true;
          ctx.rerender();
        },
      }),
    ];
  },
  onChallengeSetup(_ctx, api) {
    ran = false;
    api.setPack({});
  },
  onLoadStarter(api) {
    ran = false;
    api.setPack({});
  },
  challenges: [
    {
      id: "run",
      title: "Run hierarchy packer",
      level: "Intro",
      prompt: "Click Pack hierarchy (or place an equivalent).",
      hint: "Primary packer button.",
      check: (_c, api) => ran || (packHasAll(api.getPack()) && isLegalPacking(api.getPack())),
    },
    {
      id: "a-left",
      title: "A on left",
      level: "Intro",
      prompt: "A.x &lt; 5 in your packing.",
      hint: "Left cluster AB.",
      check: (_c, api) => api.getPack().A && api.getPack().A.x < 5,
    },
    {
      id: "c-right",
      title: "C on right",
      level: "Intro",
      prompt: "C.x ≥ 5.",
      hint: "Right cluster offset.",
      check: (_c, api) => api.getPack().C && api.getPack().C.x >= 5,
    },
    {
      id: "five",
      title: "Five modules",
      level: "Practice",
      prompt: "All five modules placed.",
      hint: "Pack hierarchy or place all.",
      check: (_c, api) => packHasAll(api.getPack()),
    },
    {
      id: "legal",
      title: "Legal hierarchy",
      level: "Practice",
      prompt: "Legal packing with AB left and CDE right.",
      hint: "A,B x&lt;5; C,D,E x≥5.",
      check: (_c, api) => {
        const p = api.getPack();
        return (
          packHasAll(p) &&
          isLegalPacking(p) &&
          p.A.x < 5 &&
          p.B.x < 5 &&
          p.C.x >= 5 &&
          p.D.x >= 5 &&
          p.E.x >= 5
        );
      },
    },
    {
      id: "gap",
      title: "Clusters separated",
      level: "Practice",
      prompt: "Left cluster max x+w ≤ right cluster min x.",
      hint: "No cluster overlap in x.",
      check: (_c, api) => {
        const p = api.getPack();
        if (!packHasAll(p)) return false;
        const leftMax = Math.max(p.A.x + p.A.w, p.B.x + p.B.w);
        const rightMin = Math.min(p.C.x, p.D.x, p.E.x);
        return leftMax <= rightMin && isLegalPacking(p);
      },
    },
    {
      id: "e-right",
      title: "E on right",
      level: "Practice",
      prompt: "E.x ≥ 5.",
      hint: "CDE cluster.",
      check: (_c, api) => api.getPack().E && api.getPack().E.x >= 5,
    },
    {
      id: "b-left",
      title: "B on left",
      level: "Stretch",
      prompt: "B.x &lt; 5.",
      hint: "AB cluster.",
      check: (_c, api) => api.getPack().B && api.getPack().B.x < 5,
    },
    {
      id: "match-hier",
      title: "Match teaching hierarchy",
      level: "Stretch",
      prompt: "Positions match packHierarchical().",
      hint: "Click Pack hierarchy.",
      check: (_c, api) => {
        const p = api.getPack();
        const g = packHierarchical();
        return (
          packHasAll(p) &&
          ["A", "B", "C", "D", "E"].every(
            (id) => p[id].x === g[id].x && p[id].y === g[id].y
          )
        );
      },
    },
    {
      id: "no-reveal",
      title: "Without reveal",
      level: "Stretch",
      prompt: "Legal separated clusters with Reveal hidden.",
      hint: "Pack hierarchy or place yourself.",
      check: (_c, api) => {
        const p = api.getPack();
        return (
          !api.isRevealed() &&
          packHasAll(p) &&
          isLegalPacking(p) &&
          p.A.x < 5 &&
          p.C.x >= 5
        );
      },
    },
  ],
});
