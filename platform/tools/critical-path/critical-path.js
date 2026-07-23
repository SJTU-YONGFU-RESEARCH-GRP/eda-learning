import {
  GOLDENS,
  PROP_GOLDENS,
  TINY_TIMING,
  cloneTiming,
  criticalPathTo,
  levelize,
  near,
  propagateArrival,
} from "../../assets/sta-core.js";
import {
  createChallengeLab,
  drawTimingGraph,
  el,
  metricsBlock,
} from "../../assets/sta-ui.js";

const G = PROP_GOLDENS;
const root = document.getElementById("lab-root");
let timing = cloneTiming(TINY_TIMING);
let levels = levelize(timing);
let mode = "none"; // none | path
let arrival = null;
let path = null;

function arm() {
  timing = cloneTiming(TINY_TIMING);
  levels = levelize(timing);
  mode = "none";
  arrival = null;
  path = null;
}

function tracePath() {
  timing = cloneTiming(TINY_TIMING);
  levels = levelize(timing);
  mode = "path";
  arrival = propagateArrival(timing);
  path = criticalPathTo(timing, arrival, "out");
}

function pathArcs(p) {
  if (!p || p.length < 2) return [];
  const arcs = [];
  for (let i = 0; i < p.length - 1; i++) arcs.push(`${p[i]}|${p[i + 1]}`);
  return arcs;
}

createChallengeLab(root, {
  starterHtml: `
    <p><strong>Starter example (reference):</strong> critical path
    <code>${G.criticalPath.join(" → ")}</code> — length <strong>${G.criticalPath.length}</strong>,
    arrival at out <strong>${G.arrival.out}</strong> (= path delay Σ <strong>${GOLDENS.pathDelay}</strong>).
    Click <em>Trace critical path</em> to highlight pins and arcs.</p>
  `,
  loadStarter() {
    tracePath();
  },
  challenges: [
    {
      id: "path-length",
      title: "Path length 6",
      level: "Intro",
      prompt: "Trace critical path; path has 6 pins.",
      hint: "Every pin on the chain is critical.",
      setup: arm,
      check: () => mode === "path" && path && path.length === 6,
    },
    {
      id: "starts-in",
      title: "Starts at in",
      level: "Intro",
      prompt: "Critical path starts at in.",
      hint: "Backward trace ends at source.",
      setup: arm,
      check: () => mode === "path" && path && path[0] === "in",
    },
    {
      id: "ends-out",
      title: "Ends at out",
      level: "Intro",
      prompt: "Critical path ends at out.",
      hint: "Trace into the sink pin.",
      setup: arm,
      check: () => mode === "path" && path && path[path.length - 1] === "out",
    },
    {
      id: "includes-u1y",
      title: "Includes u1/Y",
      level: "Practice",
      prompt: "Critical path includes u1/Y.",
      hint: "Cell output of u1.",
      setup: arm,
      check: () => mode === "path" && path && path.includes("u1/Y"),
    },
    {
      id: "includes-u2a",
      title: "Includes u2/A",
      level: "Practice",
      prompt: "Critical path includes u2/A.",
      hint: "Net from u1/Y lands here.",
      setup: arm,
      check: () => mode === "path" && path && path.includes("u2/A"),
    },
    {
      id: "golden-path",
      title: "Matches golden path",
      level: "Practice",
      prompt: "Path equals PROP_GOLDENS.criticalPath.",
      hint: "in → u1/A → u1/Y → u2/A → u2/Y → out.",
      setup: arm,
      check: () =>
        mode === "path" && path && path.join(",") === G.criticalPath.join(","),
    },
    {
      id: "arrival-out",
      title: "Arrival out 3.2",
      level: "Practice",
      prompt: "After trace, arrival at out is 3.2.",
      hint: "Matches path delay sum.",
      setup: arm,
      check: () =>
        mode === "path" && arrival && near(arrival.out, G.arrival.out),
    },
    {
      id: "includes-u1a",
      title: "Includes u1/A",
      level: "Stretch",
      prompt: "Critical path includes u1/A.",
      hint: "First cell input.",
      setup: arm,
      check: () => mode === "path" && path && path.includes("u1/A"),
    },
    {
      id: "includes-u2y",
      title: "Includes u2/Y",
      level: "Stretch",
      prompt: "Critical path includes u2/Y.",
      hint: "Second cell output.",
      setup: arm,
      check: () => mode === "path" && path && path.includes("u2/Y"),
    },
    {
      id: "delay-matches",
      title: "Delay sum 3.2",
      level: "Stretch",
      prompt: "Arrival at out matches GOLDENS.pathDelay (3.2).",
      hint: "Only one path — sum of arc delays.",
      setup: arm,
      check: () =>
        mode === "path" &&
        arrival &&
        near(arrival.out, GOLDENS.pathDelay),
    },
  ],
  extraActions(ctx) {
    return [
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Trace critical path",
        onClick: () => {
          tracePath();
          ctx.rerender();
        },
      }),
    ];
  },
  renderWorkspace(ctx) {
    const tags = {};
    if (arrival) {
      for (const [p, v] of Object.entries(arrival)) tags[p] = `A:${v}`;
    }
    drawTimingGraph(ctx.canvas, timing, {
      levels,
      highlightPins: path || [],
      highlightArcs: pathArcs(path),
      tags,
    });
    const lines = [
      `view: ${mode}`,
      `path: ${path ? path.join(" → ") : "—"}`,
      `path length: ${path ? path.length : "—"}`,
      `arrival out: ${arrival?.out ?? "—"}`,
      `path delay Σ: ${GOLDENS.pathDelay}`,
    ];
    if (path) {
      lines.push("path pins:");
      for (const p of path) lines.push(`  ${p}: arr=${arrival?.[p] ?? "—"}`);
    }
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock(lines));
  },
});
