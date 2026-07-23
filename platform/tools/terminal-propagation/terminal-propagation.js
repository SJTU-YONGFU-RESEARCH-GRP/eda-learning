import { partsString } from "../../assets/clustering-core.js";
import { GOLDEN_BIPART, terminalPropagation } from "../../assets/partitioning-core.js";
import {
  createInteractiveGraphLab,
  el,
} from "../../assets/interactive-graph-lab.js";

const root = document.getElementById("lab-root");

createInteractiveGraphLab(root, {
  initialAssignment: { A: "0", E: "1", B: null, C: null, D: null },
  revealAssignment: GOLDEN_BIPART,
  lockedNodes: ["A", "E"],
  lockedSides: { A: "0", E: "1" },
  initialMeta: { iters: null, termKey: "AE" },
  starterHtml: `
    <p><strong>Your job:</strong> terminals A=0 and E=1 are locked. Assign free nodes (or Propagate)
    until ABC|DE cut 3. Challenges check <em>your</em> assignment — terminals stay fixed.</p>
  `,
  challenges: [
    {
      id: "ae-parts",
      title: "Propagate → ABC|DE",
      level: "Intro",
      prompt: "Propagate with A=0,E=1; parts are ABC|DE.",
      hint: "Click Propagate A/E (or Assign B,C to 0 and D to 1).",
      check: (_c, api) => partsString(api.getAssignment()) === "ABC|DE",
    },
    {
      id: "ae-cut-3",
      title: "Cutsize 3",
      level: "Intro",
      prompt: "Cutsize is 3 with terminals A/E fixed.",
      hint: "Propagate or Assign free nodes.",
      check: (_c, api) => api.cutsize() === 3,
    },
    {
      id: "ae-a-fixed",
      title: "Terminal A stays 0",
      level: "Intro",
      prompt: "Terminal A remains label 0.",
      hint: "A is locked — Flip will not move it.",
      check: (_c, api) => api.getAssignment().A === "0",
    },
    {
      id: "ae-e-fixed",
      title: "Terminal E stays 1",
      level: "Practice",
      prompt: "Terminal E remains label 1.",
      hint: "E is locked.",
      check: (_c, api) => api.getAssignment().E === "1",
    },
    {
      id: "ae-b-with-a",
      title: "B takes A’s side",
      level: "Practice",
      prompt: "Free node B is on A’s side (0); cut ≤ 3.",
      hint: "Propagate or Assign B to 0.",
      check: (_c, api) => {
        const a = api.getAssignment();
        return a.B === a.A && a.A === "0" && api.cutsize() <= 3;
      },
    },
    {
      id: "ae-d-with-e",
      title: "D takes E’s side",
      level: "Practice",
      prompt: "Free node D is on E’s side (1); cutsize 3.",
      hint: "Propagate or Assign D to 1.",
      check: (_c, api) => {
        const a = api.getAssignment();
        return a.D === a.E && a.E === "1" && api.cutsize() === 3;
      },
    },
    {
      id: "ad-same-golden",
      title: "Terminals A/D also golden",
      level: "Practice",
      prompt: "Propagate with terminals A=0,D=1; reach ABC|DE cut 3.",
      hint: "Click Propagate A/D.",
      check: (_c, api) =>
        api.getMeta().termKey === "AD" &&
        partsString(api.getAssignment()) === "ABC|DE" &&
        api.cutsize() === 3,
    },
    {
      id: "ad-d-fixed",
      title: "D fixed as terminal",
      level: "Stretch",
      prompt: "After Propagate A/D, D remains label 1.",
      hint: "D was the terminal on side 1.",
      check: (_c, api) => api.getMeta().termKey === "AD" && api.getAssignment().D === "1",
    },
    {
      id: "two-sides",
      title: "Two labels",
      level: "Stretch",
      prompt: "All nodes labeled; exactly two sides.",
      hint: "Propagate or Assign remaining nulls.",
      check: (_c, api) => {
        const vals = Object.values(api.getAssignment());
        return vals.every((v) => v === "0" || v === "1") && new Set(vals).size === 2;
      },
    },
    {
      id: "iters-positive",
      title: "Propagate iters ≥ 1",
      level: "Stretch",
      prompt: "After Propagate A/E, iters ≥ 1 and cut 3 (Reveal off).",
      hint: "Click Propagate A/E.",
      check: (_c, api) =>
        !api.isRevealed() &&
        api.getMeta().termKey === "AE" &&
        (api.getMeta().iters || 0) >= 1 &&
        api.cutsize() === 3,
    },
  ],
  extraActions(ctx, api) {
    return [
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Propagate A/E",
        onClick: () => {
          const g = api.getGraph();
          // Temporarily unlock D if previous AD run locked it via meta only
          const r = terminalPropagation(g.nodes, g.edges, { A: "0", E: "1" });
          api.setAssignment(r.assignment);
          api.setMeta({ iters: r.iters, termKey: "AE" });
          api.setRevealed(false);
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: "Propagate A/D",
        onClick: () => {
          const g = api.getGraph();
          const r = terminalPropagation(g.nodes, g.edges, { A: "0", D: "1" });
          api.setAssignment(r.assignment);
          api.setMeta({ iters: r.iters, termKey: "AD" });
          api.setRevealed(false);
          ctx.rerender();
        },
      }),
    ];
  },
  extraMetrics(api) {
    return [
      `terminals mode: ${api.getMeta().termKey || "AE"}`,
      `iters: ${api.getMeta().iters ?? "—"}`,
      "locked: A→0, E→1 (Flip ignored on locked)",
    ];
  },
});
