import {
  PROP_GOLDENS,
  TINY_TIMING,
  analyzeSetup,
  cloneTiming,
  levelize,
  near,
  propagateArrival,
  propagateRequired,
  setupSlack,
} from "../../assets/sta-core.js";
import {
  createChallengeLab,
  drawTimingGraph,
  el,
  metricsBlock,
} from "../../assets/sta-ui.js";

const G = PROP_GOLDENS;
const FP_ARC = "u1/Y|u2/A";
const root = document.getElementById("lab-root");
let timing = cloneTiming(TINY_TIMING);
let levels = levelize(timing);
let mode = "none"; // none | normal | multicycle | falsepath
let arrival = null;
let required = null;
let slackOut = null;
let disabled = [];

function arm() {
  timing = cloneTiming(TINY_TIMING);
  levels = levelize(timing);
  mode = "none";
  arrival = null;
  required = null;
  slackOut = null;
  disabled = [];
}

function normalSetup() {
  timing = cloneTiming(TINY_TIMING);
  levels = levelize(timing);
  mode = "normal";
  disabled = [];
  const r = analyzeSetup(timing);
  arrival = r.arrival;
  required = r.required;
  slackOut = r.slackAtSink;
}

function multicycleSetup() {
  timing = cloneTiming(TINY_TIMING);
  levels = levelize(timing);
  mode = "multicycle";
  disabled = [];
  arrival = propagateArrival(timing);
  required = propagateRequired(timing, { setupCycles: G.multicycle.setupCycles });
  slackOut = setupSlack(arrival, required, "out");
}

function falsePath() {
  timing = cloneTiming(TINY_TIMING);
  levels = levelize(timing);
  mode = "falsepath";
  disabled = [FP_ARC];
  arrival = propagateArrival(timing, { disableArcs: disabled });
  required = propagateRequired(timing, { disableArcs: disabled });
  slackOut = setupSlack(arrival, required, "out");
}

createChallengeLab(root, {
  starterHtml: `
    <p><strong>Starter example (reference):</strong> normal setup slack at out =
    <strong>${G.setupSlackOut}</strong>; multicycle setup×${G.multicycle.setupCycles}
    → required <strong>${G.multicycle.requiredOut}</strong>, slack
    <strong>${G.multicycle.setupSlackOut}</strong>; false-path disables
    <code>u1/Y→u2/A</code> so u2/A has no enabled predecessor (arrival 0).</p>
  `,
  loadStarter() {
    normalSetup();
  },
  challenges: [
    {
      id: "normal-slack",
      title: "Normal slack 6.8",
      level: "Intro",
      prompt: "Normal setup; slack at out is 6.8.",
      hint: "Single-cycle required = period.",
      setup: arm,
      check: () =>
        mode === "normal" && slackOut != null && near(slackOut, G.setupSlackOut),
    },
    {
      id: "multicycle-required",
      title: "Multicycle required 20",
      level: "Intro",
      prompt: "Multicycle×2; required at out is 20.",
      hint: "2 × period.",
      setup: arm,
      check: () =>
        mode === "multicycle" &&
        required &&
        near(required.out, G.multicycle.requiredOut),
    },
    {
      id: "multicycle-slack",
      title: "Multicycle slack 16.8",
      level: "Intro",
      prompt: "Multicycle×2; setup slack at out is 16.8.",
      hint: "20 − 3.2.",
      setup: arm,
      check: () =>
        mode === "multicycle" &&
        slackOut != null &&
        near(slackOut, G.multicycle.setupSlackOut),
    },
    {
      id: "normal-required",
      title: "Normal required 10",
      level: "Practice",
      prompt: "Normal setup; required at out is 10.",
      hint: "Default one clock cycle.",
      setup: arm,
      check: () =>
        mode === "normal" &&
        required &&
        near(required.out, G.requiredSetup.out),
    },
    {
      id: "normal-arrival",
      title: "Normal arrival 3.2",
      level: "Practice",
      prompt: "Normal setup; arrival at out is 3.2.",
      hint: "Unchanged by multicycle/false-path modes.",
      setup: arm,
      check: () =>
        mode === "normal" && arrival && near(arrival.out, G.arrival.out),
    },
    {
      id: "multicycle-cycles",
      title: "Setup cycles 2",
      level: "Practice",
      prompt: "Multicycle mode uses setupCycles=2.",
      hint: "Check required = 2×10.",
      setup: arm,
      check: () =>
        mode === "multicycle" &&
        required &&
        near(required.out, G.period * G.multicycle.setupCycles),
    },
    {
      id: "falsepath-u1y",
      title: "False-path u1/Y",
      level: "Practice",
      prompt: "False-path; u1/Y arrival still 1.2.",
      hint: "Upstream of cut is intact.",
      setup: arm,
      check: () =>
        mode === "falsepath" &&
        arrival &&
        near(arrival["u1/Y"], G.arrival["u1/Y"]),
    },
    {
      id: "falsepath-u2a",
      title: "False-path u2/A zero",
      level: "Stretch",
      prompt: "False-path; u2/A arrival is 0 (no enabled predecessor).",
      hint: "Disabled arc u1/Y→u2/A.",
      setup: arm,
      check: () =>
        mode === "falsepath" &&
        arrival &&
        near(arrival["u2/A"], 0),
    },
    {
      id: "falsepath-disable",
      title: "Arc disabled",
      level: "Stretch",
      prompt: "False-path mode disables u1/Y→u2/A.",
      hint: "Click False-path button.",
      setup: arm,
      check: () => mode === "falsepath" && disabled.includes(FP_ARC),
    },
    {
      id: "falsepath-propagate",
      title: "False-path propagate check",
      level: "Stretch",
      prompt: "False-path; propagateArrival with disable gives u1/Y≈1.2 and u2/A≈0.",
      hint: "Cross-check with sta-core propagateArrival.",
      setup: arm,
      check: () => {
        if (mode !== "falsepath" || !arrival) return false;
        const arr = propagateArrival(cloneTiming(TINY_TIMING), {
          disableArcs: [FP_ARC],
        });
        return (
          near(arr["u1/Y"], 1.2) &&
          near(arr["u2/A"], 0) &&
          near(arrival["u1/Y"], arr["u1/Y"]) &&
          near(arrival["u2/A"], arr["u2/A"])
        );
      },
    },
  ],
  extraActions(ctx) {
    return [
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: "Normal setup",
        onClick: () => {
          normalSetup();
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Multicycle×2",
        onClick: () => {
          multicycleSetup();
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: "False-path (disable u1/Y→u2/A)",
        onClick: () => {
          falsePath();
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
    if (required && mode !== "falsepath") {
      for (const [p, v] of Object.entries(required)) {
        if (p === "out" || mode === "multicycle") {
          tags[p] = tags[p] ? `${tags[p]} R:${v}` : `R:${v}`;
        }
      }
    }
    drawTimingGraph(ctx.canvas, timing, {
      levels,
      highlightPins:
        mode === "falsepath"
          ? ["u1/Y", "u2/A"]
          : mode === "normal" || mode === "multicycle"
            ? ["out"]
            : [],
      highlightArcs: mode === "falsepath" ? [FP_ARC] : [],
      tags,
    });
    const lines = [
      `view: ${mode}`,
      `slack at out: ${slackOut ?? "—"}`,
    ];
    if (mode === "multicycle") {
      lines.push(`setupCycles: ${G.multicycle.setupCycles}`);
      lines.push(`required out: ${required?.out ?? "—"}`);
    }
    if (mode === "normal") {
      lines.push(`required out: ${required?.out ?? "—"}`);
      lines.push(`arrival out: ${arrival?.out ?? "—"}`);
    }
    if (mode === "falsepath") {
      lines.push(`disabled: ${disabled.join(", ")}`);
      lines.push(`u1/Y arrival: ${arrival?.["u1/Y"] ?? "—"}`);
      lines.push(`u2/A arrival: ${arrival?.["u2/A"] ?? "—"} (no enabled pred)`);
      lines.push("note: downstream sink not fully timed when path is cut");
    }
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock(lines));
  },
});
