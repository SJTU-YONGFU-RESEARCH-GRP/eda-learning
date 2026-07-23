import {
  PROP_GOLDENS,
  TINY_TIMING,
  cloneTiming,
  levelize,
  near,
  propagateArrival,
  propagateRequired,
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
let mode = "none"; // none | arrival | required | both
let arrival = null;
let required = null;

function arm() {
  timing = cloneTiming(TINY_TIMING);
  levels = levelize(timing);
  mode = "none";
  arrival = null;
  required = null;
}

function showArrival() {
  timing = cloneTiming(TINY_TIMING);
  levels = levelize(timing);
  mode = "arrival";
  arrival = propagateArrival(timing);
  required = null;
}

function showRequired() {
  timing = cloneTiming(TINY_TIMING);
  levels = levelize(timing);
  mode = "required";
  required = propagateRequired(timing);
  arrival = null;
}

function showBoth() {
  timing = cloneTiming(TINY_TIMING);
  levels = levelize(timing);
  mode = "both";
  arrival = propagateArrival(timing);
  required = propagateRequired(timing);
}

function pinTags() {
  const tags = {};
  if (arrival && (mode === "arrival" || mode === "both")) {
    for (const [p, v] of Object.entries(arrival)) tags[p] = `A:${v}`;
  }
  if (required && (mode === "required" || mode === "both")) {
    for (const [p, v] of Object.entries(required)) {
      tags[p] = tags[p] ? `${tags[p]} R:${v}` : `R:${v}`;
    }
  }
  return tags;
}

createChallengeLab(root, {
  starterHtml: `
    <p><strong>Starter example (reference):</strong> chain
    <code>in → u1 → u2 → out</code> with clock period <strong>${G.period}</strong>.
    Forward arrival at <strong>out = ${G.arrival.out}</strong>;
    backward setup required at <strong>out = ${G.requiredSetup.out}</strong>.
    Click <em>Show arrival</em>, <em>Show required</em>, or <em>Show both</em>.</p>
  `,
  loadStarter() {
    showBoth();
  },
  challenges: [
    {
      id: "arrival-out",
      title: "Arrival at out",
      level: "Intro",
      prompt: "Show arrival; out arrival equals 3.2.",
      hint: "Forward propagate from in=0.",
      setup: arm,
      check: () =>
        mode === "arrival" &&
        arrival &&
        near(arrival.out, G.arrival.out),
    },
    {
      id: "required-out",
      title: "Required at out",
      level: "Intro",
      prompt: "Show required; out required setup equals 10.",
      hint: "Sink required = clock period.",
      setup: arm,
      check: () =>
        mode === "required" &&
        required &&
        near(required.out, G.requiredSetup.out),
    },
    {
      id: "arrival-u1y",
      title: "Arrival u1/Y",
      level: "Intro",
      prompt: "Show arrival; u1/Y arrival equals 1.2.",
      hint: "Cell delay in→u1/A→u1/Y.",
      setup: arm,
      check: () =>
        mode === "arrival" &&
        arrival &&
        near(arrival["u1/Y"], G.arrival["u1/Y"]),
    },
    {
      id: "required-u1a",
      title: "Required u1/A",
      level: "Practice",
      prompt: "Show required; u1/A required equals 6.8.",
      hint: "Backward from out through u1/Y.",
      setup: arm,
      check: () =>
        mode === "required" &&
        required &&
        near(required["u1/A"], G.requiredSetup["u1/A"]),
    },
    {
      id: "arrival-in",
      title: "Arrival at in",
      level: "Practice",
      prompt: "Show arrival; source in arrival is 0.",
      hint: "Sources seed at 0.",
      setup: arm,
      check: () =>
        mode === "arrival" && arrival && near(arrival.in, G.arrival.in),
    },
    {
      id: "arrival-u2y",
      title: "Arrival u2/Y",
      level: "Practice",
      prompt: "Show arrival; u2/Y arrival equals 3.0.",
      hint: "Sum delays through u2 cell.",
      setup: arm,
      check: () =>
        mode === "arrival" &&
        arrival &&
        near(arrival["u2/Y"], G.arrival["u2/Y"]),
    },
    {
      id: "required-u2y",
      title: "Required u2/Y",
      level: "Practice",
      prompt: "Show required; u2/Y required equals 9.8.",
      hint: "out required minus net u2/Y→out.",
      setup: arm,
      check: () =>
        mode === "required" &&
        required &&
        near(required["u2/Y"], G.requiredSetup["u2/Y"]),
    },
    {
      id: "arrival-u2a",
      title: "Arrival u2/A",
      level: "Stretch",
      prompt: "Show arrival; u2/A arrival equals 1.5.",
      hint: "Net delay u1/Y→u2/A added to 1.2.",
      setup: arm,
      check: () =>
        mode === "arrival" &&
        arrival &&
        near(arrival["u2/A"], G.arrival["u2/A"]),
    },
    {
      id: "required-in",
      title: "Required at in",
      level: "Stretch",
      prompt: "Show required; in required equals 6.8.",
      hint: "Full backward chain to source.",
      setup: arm,
      check: () =>
        mode === "required" &&
        required &&
        near(required.in, G.requiredSetup.in),
    },
    {
      id: "both-goldens",
      title: "Both maps match",
      level: "Stretch",
      prompt: "Show both; every pin matches PROP_GOLDENS arrival and required.",
      hint: "Click Show both; compare all six pins.",
      setup: arm,
      check: () => {
        if (mode !== "both" || !arrival || !required) return false;
        for (const p of Object.keys(G.arrival)) {
          if (!near(arrival[p], G.arrival[p])) return false;
        }
        for (const p of Object.keys(G.requiredSetup)) {
          if (!near(required[p], G.requiredSetup[p])) return false;
        }
        return true;
      },
    },
  ],
  extraActions(ctx) {
    return [
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: "Show arrival",
        onClick: () => {
          showArrival();
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: "Show required",
        onClick: () => {
          showRequired();
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Show both",
        onClick: () => {
          showBoth();
          ctx.rerender();
        },
      }),
    ];
  },
  renderWorkspace(ctx) {
    drawTimingGraph(ctx.canvas, timing, {
      levels,
      highlightPins:
        mode === "both"
          ? ["in", "out"]
          : mode === "arrival"
            ? ["out"]
            : mode === "required"
              ? ["in", "out"]
              : [],
      tags: pinTags(),
    });
    const lines = [`view: ${mode}`, `period: ${G.period}`];
    if (arrival) {
      lines.push("arrival:");
      for (const p of Object.keys(G.arrival)) {
        lines.push(`  ${p}: ${arrival[p] ?? "—"}`);
      }
    }
    if (required) {
      lines.push("required (setup):");
      for (const p of Object.keys(G.requiredSetup)) {
        lines.push(`  ${p}: ${required[p] ?? "—"}`);
      }
    }
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock(lines));
  },
});
