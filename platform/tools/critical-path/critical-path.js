import { PROP_GOLDENS, near } from "../../assets/sta-core.js";
import { createInteractiveStaLab } from "../../assets/interactive-sta-lab.js";
import { el } from "../../assets/sta-ui.js";
import {
  criticalPathTo,
  propagateArrival,
} from "../../assets/sta-core.js";

const G = PROP_GOLDENS;
const root = document.getElementById("lab-root");

function pathEqual(a, b) {
  if (!a || !b || a.length !== b.length) return false;
  return a.every((p, i) => p === b[i]);
}

createInteractiveStaLab(root, {
  mode: "path",
  initialPath: [],
  revealPath: G.criticalPath,
  starterHtml: `
    <p><strong>Your workspace:</strong> click pins in order to build the critical path
    from <code>in</code> to <code>out</code>. Optional: <em>Trace critical path</em> helper.
    Challenges check <strong>your</strong> path. Reveal golden is study-only.</p>
  `,
  extraActions: (ctx, api) => [
    el("button", {
      className: "btn btn-secondary",
      type: "button",
      text: "Trace critical path",
      onClick: () => {
        const t = api.getTiming();
        const arr = propagateArrival(t);
        const path = criticalPathTo(t, arr, "out");
        api.setPath(path || []);
        api.setMeta({ arrival: arr });
        api.setRevealed(false);
        ctx.rerender();
      },
    }),
  ],
  extraMetrics: (api) => {
    const p = api.getPath();
    return [
      `golden length: ${G.criticalPath.length}`,
      `your length: ${p.length}`,
      `arrival out (ref): ${G.arrival.out}`,
    ];
  },
  challenges: [
    {
      id: "len-6",
      title: "Path length 6",
      level: "Intro",
      prompt: "Build a path with 6 pins.",
      hint: "Click each pin on the chain once.",
      check: (_c, api) => api.getPath().length === 6,
    },
    {
      id: "starts-in",
      title: "Starts at in",
      level: "Intro",
      prompt: "Path starts at in.",
      hint: "First click: in.",
      check: (_c, api) => api.getPath()[0] === "in",
    },
    {
      id: "ends-out",
      title: "Ends at out",
      level: "Intro",
      prompt: "Path ends at out.",
      hint: "Last pin: out.",
      check: (_c, api) => {
        const p = api.getPath();
        return p.length && p[p.length - 1] === "out";
      },
    },
    {
      id: "full-path",
      title: "Exact critical path",
      level: "Practice",
      prompt: `Path equals ${G.criticalPath.join(" → ")}.`,
      hint: "Click in order, or Trace critical path.",
      check: (_c, api) => pathEqual(api.getPath(), G.criticalPath),
    },
    {
      id: "includes-u1y",
      title: "Includes u1/Y",
      level: "Practice",
      prompt: "Path includes u1/Y.",
      hint: "Middle of the chain.",
      check: (_c, api) => api.getPath().includes("u1/Y"),
    },
    {
      id: "includes-u2a",
      title: "Includes u2/A",
      level: "Practice",
      prompt: "Path includes u2/A.",
      hint: "After the net from u1/Y.",
      check: (_c, api) => api.getPath().includes("u2/A"),
    },
    {
      id: "no-dupes",
      title: "No duplicate pins",
      level: "Challenge",
      prompt: "Critical path has 6 unique pins (no repeats).",
      hint: "Clear and rebuild if you double-clicked.",
      check: (_c, api) => {
        const p = api.getPath();
        return p.length === 6 && new Set(p).size === 6;
      },
    },
    {
      id: "order-u1",
      title: "u1/A before u1/Y",
      level: "Challenge",
      prompt: "u1/A appears before u1/Y on your path.",
      hint: "Cell input before output.",
      check: (_c, api) => {
        const p = api.getPath();
        return p.indexOf("u1/A") >= 0 && p.indexOf("u1/A") < p.indexOf("u1/Y");
      },
    },
    {
      id: "matches-arrival",
      title: "Path matches arrival trace",
      level: "Challenge",
      prompt: "Your path equals criticalPathTo(arrival, out).",
      hint: "Trace critical path helper.",
      check: (_c, api) => {
        const t = api.getTiming();
        const arr = propagateArrival(t);
        return pathEqual(api.getPath(), criticalPathTo(t, arr, "out"));
      },
    },
    {
      id: "delay-sum",
      title: "Path delay sense-check",
      level: "Challenge",
      prompt: "Full critical path built (length 6 ending at out) — delay sum is 3.2 by construction.",
      hint: "Build the full path.",
      check: (_c, api) =>
        pathEqual(api.getPath(), G.criticalPath) && near(G.arrival.out, 3.2),
    },
  ],
});
