import {
  PROP_GOLDENS,
  TINY_TIMING,
  analyzeSetup,
  cloneTiming,
  holdSlack,
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
const root = document.getElementById("lab-root");
let timing = cloneTiming(TINY_TIMING);
let levels = levelize(timing);
let mode = "none"; // none | setup | hold
let arrival = null;
let required = null;
let slackOut = null;

function arm() {
  timing = cloneTiming(TINY_TIMING);
  levels = levelize(timing);
  mode = "none";
  arrival = null;
  required = null;
  slackOut = null;
}

function computeSetup() {
  timing = cloneTiming(TINY_TIMING);
  levels = levelize(timing);
  mode = "setup";
  const r = analyzeSetup(timing);
  arrival = r.arrival;
  required = r.required;
  slackOut = r.slackAtSink;
}

function computeHold() {
  timing = cloneTiming(TINY_TIMING);
  levels = levelize(timing);
  mode = "hold";
  arrival = propagateArrival(timing);
  required = propagateRequired(timing, { mode: "hold" });
  slackOut = holdSlack(arrival, required, "out");
}

createChallengeLab(root, {
  starterHtml: `
    <p><strong>Starter example (reference):</strong> at <code>out</code>,
    setup slack = required − arrival = <strong>${G.setupSlackOut}</strong>
    (10 − 3.2); hold slack = arrival − required = <strong>${G.holdSlackOut}</strong>
    (3.2 − 0). Use <em>Compute setup</em> and <em>Compute hold</em>.</p>
  `,
  loadStarter() {
    computeSetup();
  },
  challenges: [
    {
      id: "setup-slack",
      title: "Setup slack 6.8",
      level: "Intro",
      prompt: "Compute setup; slack at out equals 6.8.",
      hint: "analyzeSetup → slackAtSink.",
      setup: arm,
      check: () =>
        mode === "setup" && slackOut != null && near(slackOut, G.setupSlackOut),
    },
    {
      id: "hold-slack",
      title: "Hold slack 3.2",
      level: "Intro",
      prompt: "Compute hold; slack at out equals 3.2.",
      hint: "Hold required at sink = 0.",
      setup: arm,
      check: () =>
        mode === "hold" && slackOut != null && near(slackOut, G.holdSlackOut),
    },
    {
      id: "setup-mode",
      title: "Setup computed",
      level: "Intro",
      prompt: "Compute setup; view mode is setup with arrival and required maps.",
      hint: "Click Compute setup.",
      setup: arm,
      check: () => mode === "setup" && arrival && required,
    },
    {
      id: "hold-mode",
      title: "Hold computed",
      level: "Intro",
      prompt: "Compute hold; view mode is hold with both maps.",
      hint: "Click Compute hold.",
      setup: arm,
      check: () => mode === "hold" && arrival && required,
    },
    {
      id: "setup-arrival-out",
      title: "Setup arrival out",
      level: "Practice",
      prompt: "Compute setup; arrival at out is 3.2.",
      hint: "Forward propagate first.",
      setup: arm,
      check: () =>
        mode === "setup" && arrival && near(arrival.out, G.arrival.out),
    },
    {
      id: "setup-required-out",
      title: "Setup required out",
      level: "Practice",
      prompt: "Compute setup; required at out is 10.",
      hint: "Period × 1 cycle.",
      setup: arm,
      check: () =>
        mode === "setup" &&
        required &&
        near(required.out, G.requiredSetup.out),
    },
    {
      id: "hold-required-out",
      title: "Hold required out",
      level: "Practice",
      prompt: "Compute hold; hold required at out is 0.",
      hint: "mode: hold seeds sinks at 0.",
      setup: arm,
      check: () => mode === "hold" && required && near(required.out, 0),
    },
    {
      id: "hold-arrival-out",
      title: "Hold arrival out",
      level: "Practice",
      prompt: "Compute hold; arrival at out still 3.2.",
      hint: "Arrival unchanged for hold check.",
      setup: arm,
      check: () =>
        mode === "hold" && arrival && near(arrival.out, G.arrival.out),
    },
    {
      id: "setup-slack-fn",
      title: "setupSlack matches",
      level: "Stretch",
      prompt: "Compute setup; setupSlack(arr, req, out) === 6.8.",
      hint: "Cross-check with setupSlack helper.",
      setup: arm,
      check: () =>
        mode === "setup" &&
        near(setupSlack(arrival, required, "out"), G.setupSlackOut),
    },
    {
      id: "hold-slack-fn",
      title: "holdSlack matches",
      level: "Stretch",
      prompt: "Compute hold; holdSlack(arr, req, out) === 3.2.",
      hint: "Cross-check with holdSlack helper.",
      setup: arm,
      check: () =>
        mode === "hold" &&
        near(holdSlack(arrival, required, "out"), G.holdSlackOut),
    },
  ],
  extraActions(ctx) {
    return [
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Compute setup",
        onClick: () => {
          computeSetup();
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: "Compute hold",
        onClick: () => {
          computeHold();
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
    if (required && mode === "hold") {
      for (const [p, v] of Object.entries(required)) {
        tags[p] = tags[p] ? `${tags[p]} H:${v}` : `H:${v}`;
      }
    } else if (required && mode === "setup") {
      for (const [p, v] of Object.entries(required)) {
        tags[p] = tags[p] ? `${tags[p]} R:${v}` : `R:${v}`;
      }
    }
    drawTimingGraph(ctx.canvas, timing, {
      levels,
      highlightPins: slackOut != null ? ["out"] : [],
      tags,
    });
    const lines = [
      `view: ${mode}`,
      `slack at out: ${slackOut ?? "—"}`,
    ];
    if (mode === "setup" && arrival && required) {
      lines.push(
        `setup: req[out] − arr[out] = ${required.out} − ${arrival.out} = ${slackOut}`
      );
    }
    if (mode === "hold" && arrival && required) {
      lines.push(
        `hold: arr[out] − req[out] = ${arrival.out} − ${required.out} = ${slackOut}`
      );
    }
    if (arrival) {
      lines.push(`arrival out: ${arrival.out}`);
    }
    if (required) {
      lines.push(`required out: ${required.out}`);
    }
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock(lines));
  },
});
