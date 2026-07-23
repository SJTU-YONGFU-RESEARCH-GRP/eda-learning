import { cloneGraph, cutsize, partsString } from "../../assets/clustering-core.js";
import { BAD_SEED, multilevelVCycle } from "../../assets/partitioning-core.js";
import {
  createChallengeLab,
  drawGraph,
  el,
  metricsBlock,
} from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let graph = cloneGraph();
let result = null;
let stage = "final"; // coarsen | project | refine | final

function arm() {
  graph = cloneGraph();
  result = null;
  stage = "final";
}

function asnForStage() {
  if (!result) return null;
  if (stage === "coarsen") return result.stages.coarsen.assignment;
  if (stage === "project") return result.stages.project.assignment;
  if (stage === "refine") return result.stages.refine.assignment;
  return result.stages.final.assignment;
}

createChallengeLab(root, {
  starterHtml: `
    <p><strong>Starter example (reference):</strong> multilevel V-cycle
    (coarsen → project → FM refine) lands on <code>P0/P1</code> communities
    <strong>ABC|DE</strong> with <strong>cutsize 3</strong>. Reload starter anytime.</p>
  `,
  loadStarter() {
    graph = cloneGraph();
    result = multilevelVCycle(graph.nodes, graph.edges, graph.sizes, 2);
    stage = "final";
  },
  challenges: [
    {
      id: "final-cut-3",
      title: "Final cutsize 3",
      level: "Intro",
      prompt: "Run V-cycle; final cutsize is 3.",
      hint: "Click Run V-cycle, view Final.",
      setup: arm,
      check: () => result && stage === "final" && result.stages.final.cut === 3,
    },
    {
      id: "final-parts",
      title: "Final ABC|DE",
      level: "Intro",
      prompt: "Final parts are ABC|DE.",
      hint: "P0/P1 labels still sort to ABC|DE.",
      setup: arm,
      check: () => result && stage === "final" && result.stages.final.parts === "ABC|DE",
    },
    {
      id: "labels-p0-p1",
      title: "Labels P0/P1",
      level: "Intro",
      prompt: "Final labels are exactly P0 and P1.",
      hint: "View Final stage.",
      setup: arm,
      check: () => {
        if (!(result && stage === "final")) return false;
        const labs = new Set(Object.values(result.stages.final.assignment));
        return labs.size === 2 && labs.has("P0") && labs.has("P1");
      },
    },
    {
      id: "project-abc-de",
      title: "Project is ABC|DE",
      level: "Practice",
      prompt: "Project stage parts are ABC|DE with cut 3.",
      hint: "Click View project.",
      setup: arm,
      check: () =>
        result &&
        stage === "project" &&
        result.stages.project.parts === "ABC|DE" &&
        result.stages.project.cut === 3,
    },
    {
      id: "refine-matches",
      title: "Refine matches project",
      level: "Practice",
      prompt: "Refine stage also ABC|DE cut 3 (already good projection).",
      hint: "Click View refine.",
      setup: arm,
      check: () =>
        result &&
        stage === "refine" &&
        result.stages.refine.parts === "ABC|DE" &&
        result.stages.refine.cut === 3,
    },
    {
      id: "coarsen-two",
      title: "Coarsen has 2 clusters",
      level: "Practice",
      prompt: "Coarsen stage uses exactly two cluster ids.",
      hint: "Click View coarsen.",
      setup: arm,
      check: () =>
        result &&
        stage === "coarsen" &&
        new Set(Object.values(result.stages.coarsen.assignment)).size === 2,
    },
    {
      id: "coarsen-merges",
      title: "Coarsen logged merges",
      level: "Practice",
      prompt: "Coarsen mergeLog has length ≥ 1.",
      hint: "Greedy contractions down to 2 clusters.",
      setup: arm,
      check: () => result && result.stages.coarsen.mergeLog.length >= 1,
    },
    {
      id: "beats-seed",
      title: "Beats bad seed cut 12",
      level: "Stretch",
      prompt: "Final cut 3 beats BAD_SEED cut 12.",
      hint: "View Final after Run.",
      setup: arm,
      check: () =>
        result &&
        stage === "final" &&
        result.stages.final.cut === 3 &&
        cutsize(BAD_SEED, graph.edges) === 12,
    },
    {
      id: "abc-same",
      title: "A,B,C same final",
      level: "Stretch",
      prompt: "Final assignment keeps A,B,C together.",
      hint: "View Final.",
      setup: arm,
      check: () => {
        if (!(result && stage === "final")) return false;
        const a = result.stages.final.assignment;
        return a.A === a.B && a.B === a.C;
      },
    },
    {
      id: "de-same",
      title: "D,E same final",
      level: "Stretch",
      prompt: "Final assignment keeps D,E together.",
      hint: "View Final.",
      setup: arm,
      check: () => {
        if (!(result && stage === "final")) return false;
        const a = result.stages.final.assignment;
        return a.D === a.E && a.D !== a.A;
      },
    },
  ],
  extraActions(ctx) {
    const viewBtn = (label, s) =>
      el("button", {
        className: "btn btn-ghost",
        type: "button",
        text: label,
        onClick: () => {
          if (!result) return;
          stage = s;
          ctx.rerender();
        },
      });
    return [
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Run V-cycle",
        onClick: () => {
          result = multilevelVCycle(graph.nodes, graph.edges, graph.sizes, 2);
          stage = "final";
          ctx.rerender();
        },
      }),
      viewBtn("View coarsen", "coarsen"),
      viewBtn("View project", "project"),
      viewBtn("View refine", "refine"),
      viewBtn("View final", "final"),
    ];
  },
  renderWorkspace(ctx) {
    const asn = asnForStage();
    drawGraph(ctx.canvas, graph, { assignment: asn });
    const lines = [];
    if (!result) {
      lines.push("No result — click Run V-cycle.");
      lines.push(`For contrast, BAD_SEED cutsize=${cutsize(BAD_SEED, graph.edges)}`);
    } else {
      lines.push(`viewing stage: ${stage}`);
      const st = result.stages[stage] || result.stages.final;
      if (stage === "coarsen") {
        lines.push(`coarse labels: ${result.stages.coarsen.labels.join(", ")}`);
        lines.push(`merges: ${result.stages.coarsen.mergeLog.length}`);
        for (const m of result.stages.coarsen.mergeLog) {
          lines.push(`  ${m.u}+${m.v}→${m.into} (w=${m.w})`);
        }
        lines.push(`parts: ${partsString(result.stages.coarsen.assignment)}`);
      } else {
        lines.push(`parts: ${st.parts || partsString(st.assignment)}`);
        lines.push(`cutsize: ${st.cut != null ? st.cut : cutsize(st.assignment, graph.edges)}`);
      }
    }
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock(lines));
  },
});
