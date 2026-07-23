import { BAD_SEED, partsString } from "../../assets/clustering-core.js";
import { multilevelVCycle } from "../../assets/partitioning-core.js";
import { createInteractiveGraphLab, el } from "../../assets/interactive-graph-lab.js";

const root = document.getElementById("lab-root");
const GOLDEN = { A: "P0", B: "P0", C: "P0", D: "P1", E: "P1" };

createInteractiveGraphLab(root, {
  initialAssignment: { ...BAD_SEED },
  revealAssignment: GOLDEN,
  initialMeta: { stages: null, stage: "final" },
  starterHtml: `
    <p><strong>Your job:</strong> Run V-cycle (or Flip/Swap) until final cut 3 / ABC|DE (P0/P1).
    Use stage buttons to inspect coarsen → project → refine → final. Challenges check your assignment.</p>
  `,
  challenges: [
    {
      id: "final-cut-3",
      title: "Final cutsize 3",
      level: "Intro",
      prompt: "Reach cutsize 3 (Run V-cycle or edit).",
      hint: "Teaching V-cycle lands on cut 3.",
      check: (_c, api) => api.cutsize() === 3,
    },
    {
      id: "final-parts",
      title: "Parts ABC|DE",
      level: "Intro",
      prompt: "Parts are ABC|DE.",
      hint: "Communities match the golden bipartition.",
      check: (_c, api) => partsString(api.getAssignment()) === "ABC|DE",
    },
    {
      id: "labels-p0-p1",
      title: "Labels P0/P1",
      level: "Intro",
      prompt: "After Run V-cycle (final stage), labels are exactly P0 and P1.",
      hint: "View final after the run.",
      check: (_c, api) => {
        const labs = new Set(Object.values(api.getAssignment()));
        return labs.size === 2 && labs.has("P0") && labs.has("P1");
      },
    },
    {
      id: "project-abc-de",
      title: "Project stage golden",
      level: "Practice",
      prompt: "After Run V-cycle, project stage parts are ABC|DE with cut 3.",
      hint: "Click View project.",
      check: (_c, api) => {
        const p = api.getMeta().stages?.project;
        return p && p.parts === "ABC|DE" && p.cut === 3;
      },
    },
    {
      id: "refine-matches",
      title: "Refine matches project",
      level: "Practice",
      prompt: "Refine stage also ABC|DE cut 3.",
      hint: "Already good projection.",
      check: (_c, api) => {
        const r = api.getMeta().stages?.refine;
        return r && r.parts === "ABC|DE" && r.cut === 3;
      },
    },
    {
      id: "coarsen-two",
      title: "Coarsen two clusters",
      level: "Practice",
      prompt: "Coarsen stage uses exactly two cluster ids.",
      hint: "View coarsen after Run V-cycle.",
      check: (_c, api) => {
        const c = api.getMeta().stages?.coarsen;
        return c && new Set(Object.values(c.assignment)).size === 2;
      },
    },
    {
      id: "coarsen-merges",
      title: "Coarsen has merges",
      level: "Practice",
      prompt: "Coarsen mergeLog length ≥ 1.",
      hint: "Greedy coarsening fired.",
      check: (_c, api) => (api.getMeta().stages?.coarsen?.mergeLog?.length || 0) >= 1,
    },
    {
      id: "beats-seed",
      title: "Beat seed 12",
      level: "Stretch",
      prompt: "Final cut 3 (seed was 12).",
      hint: "Run V-cycle.",
      check: (_c, api) => api.cutsize() === 3,
    },
    {
      id: "abc-same",
      title: "A,B,C together",
      level: "Stretch",
      prompt: "A, B, C share a label; cutsize 3.",
      hint: "Triangle stays together.",
      check: (_c, api) => {
        const a = api.getAssignment();
        return a.A === a.B && a.B === a.C && api.cutsize() === 3;
      },
    },
    {
      id: "de-same",
      title: "D,E without reveal",
      level: "Stretch",
      prompt: "D and E together, cut 3, Reveal off.",
      hint: "Hide golden; Run V-cycle.",
      check: (_c, api) => {
        const a = api.getAssignment();
        return !api.isRevealed() && a.D === a.E && api.cutsize() === 3;
      },
    },
  ],
  extraActions(ctx, api) {
    const showStage = (stage) => {
      const stages = api.getMeta().stages;
      if (!stages) {
        ctx.setStatus("idle", "Run V-cycle first");
        return;
      }
      const asn = stages[stage]?.assignment;
      if (!asn) return;
      api.setAssignment(asn);
      api.setMeta({ stage });
      api.setRevealed(false);
      ctx.rerender();
    };
    return [
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Run V-cycle",
        onClick: () => {
          const g = api.getGraph();
          const r = multilevelVCycle(g.nodes, g.edges, g.sizes, 2);
          api.setMeta({ stages: r.stages, stage: "final" });
          api.setAssignment(r.assignment);
          api.setRevealed(false);
          ctx.rerender();
        },
      }),
      ...["coarsen", "project", "refine", "final"].map((s) =>
        el("button", {
          className: "btn btn-ghost",
          type: "button",
          text: `View ${s}`,
          onClick: () => showStage(s),
        })
      ),
    ];
  },
  extraMetrics(api) {
    const lines = [`stage view: ${api.getMeta().stage || "—"}`];
    const st = api.getMeta().stages;
    if (st) {
      for (const name of ["coarsen", "project", "refine", "final"]) {
        const s = st[name];
        if (!s) continue;
        lines.push(
          `${name}: parts=${partsString(s.assignment)}` +
            (s.cut != null ? ` cut=${s.cut}` : "")
        );
      }
    }
    return lines;
  },
});
