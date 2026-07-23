import {
  PROP_GOLDENS,
  TINY_TIMING,
  cloneTiming,
  incrementalArrival,
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
const INC = G.incremental;
const root = document.getElementById("lab-root");
let timing = cloneTiming(TINY_TIMING);
let levels = levelize(timing);
let mode = "none"; // none | base | edited
let baseArr = null;
let edited = null; // { timing, arrival, invalidated }

function arm() {
  timing = cloneTiming(TINY_TIMING);
  levels = levelize(timing);
  mode = "none";
  baseArr = null;
  edited = null;
}

function showBase() {
  timing = cloneTiming(TINY_TIMING);
  levels = levelize(timing);
  mode = "base";
  baseArr = propagateArrival(timing);
  edited = null;
}

function applyEdit() {
  const base = cloneTiming(TINY_TIMING);
  if (!baseArr) baseArr = propagateArrival(base);
  edited = incrementalArrival(
    base,
    { from: INC.editFrom, to: INC.editTo, delay: INC.newDelay },
    baseArr
  );
  timing = edited.timing;
  levels = levelize(timing);
  mode = "edited";
}

function currentArr() {
  if (mode === "edited" && edited) return edited.arrival;
  if (mode === "base" && baseArr) return baseArr;
  return null;
}

function editedSlack() {
  if (mode !== "edited" || !edited) return null;
  const req = propagateRequired(timing);
  return setupSlack(edited.arrival, req, "out");
}

createChallengeLab(root, {
  starterHtml: `
    <p><strong>Starter example (reference):</strong> base arrival at out =
    <strong>${G.arrival.out}</strong>. After editing arc
    <code>${INC.editFrom}→${INC.editTo}</code> delay to <strong>${INC.newDelay}</strong>,
    out arrival = <strong>${INC.arrivalOut}</strong>, setup slack =
    <strong>${INC.setupSlackOut}</strong>, invalidated =
    <code>${INC.invalidated.join(", ")}</code>.</p>
  `,
  loadStarter() {
    showBase();
    applyEdit();
  },
  challenges: [
    {
      id: "base-out",
      title: "Base out 3.2",
      level: "Intro",
      prompt: "Show base; arrival at out is 3.2.",
      hint: "Full propagate before edit.",
      setup: arm,
      check: () =>
        mode === "base" && baseArr && near(baseArr.out, G.arrival.out),
    },
    {
      id: "edited-out",
      title: "Edited out 4.0",
      level: "Intro",
      prompt: "Apply delay edit; arrival at out is 4.0.",
      hint: "u1 cell +0.8 ns propagates downstream.",
      setup: arm,
      check: () =>
        mode === "edited" &&
        edited &&
        near(edited.arrival.out, INC.arrivalOut),
    },
    {
      id: "edited-slack",
      title: "Edited slack 6.0",
      level: "Intro",
      prompt: "After edit, setup slack at out is 6.0.",
      hint: "10 − 4.0.",
      setup: arm,
      check: () => {
        if (mode !== "edited" || !edited) return false;
        return near(editedSlack(), INC.setupSlackOut);
      },
    },
    {
      id: "invalidated-out",
      title: "out invalidated",
      level: "Practice",
      prompt: "Apply edit; out is in the invalidated cone.",
      hint: "Fanout from u1/Y includes out.",
      setup: arm,
      check: () =>
        mode === "edited" &&
        edited &&
        edited.invalidated.includes("out"),
    },
    {
      id: "invalidated-u1y",
      title: "u1/Y invalidated",
      level: "Practice",
      prompt: "Apply edit; u1/Y is invalidated.",
      hint: "Edit target's fanout starts at u1/Y.",
      setup: arm,
      check: () =>
        mode === "edited" &&
        edited &&
        edited.invalidated.includes("u1/Y"),
    },
    {
      id: "not-in",
      title: "in not invalidated",
      level: "Practice",
      prompt: "Apply edit; in is NOT in the invalidated set.",
      hint: "Upstream of edit is unchanged.",
      setup: arm,
      check: () =>
        mode === "edited" &&
        edited &&
        !edited.invalidated.includes("in"),
    },
    {
      id: "invalidated-u2a",
      title: "u2/A invalidated",
      level: "Practice",
      prompt: "Apply edit; u2/A is invalidated.",
      hint: "Downstream of u1/Y.",
      setup: arm,
      check: () =>
        mode === "edited" &&
        edited &&
        edited.invalidated.includes("u2/A"),
    },
    {
      id: "base-u1y",
      title: "Base u1/Y 1.2",
      level: "Stretch",
      prompt: "Show base; u1/Y arrival is 1.2.",
      hint: "Before the delay bump.",
      setup: arm,
      check: () =>
        mode === "base" &&
        baseArr &&
        near(baseArr["u1/Y"], G.arrival["u1/Y"]),
    },
    {
      id: "edited-u1y",
      title: "Edited u1/Y 2.0",
      level: "Stretch",
      prompt: "After edit; u1/Y arrival is 2.0.",
      hint: "Cell delay now 2.0 from u1/A.",
      setup: arm,
      check: () =>
        mode === "edited" &&
        edited &&
        near(edited.arrival["u1/Y"], INC.newDelay),
    },
    {
      id: "invalidated-set",
      title: "Invalidated set match",
      level: "Stretch",
      prompt: "Invalidated pins match PROP_GOLDENS.incremental.invalidated.",
      hint: "u1/Y, u2/A, u2/Y, out — not in or u1/A.",
      setup: arm,
      check: () => {
        if (mode !== "edited" || !edited) return false;
        const got = [...edited.invalidated].sort().join(",");
        const exp = [...INC.invalidated].sort().join(",");
        return got === exp;
      },
    },
  ],
  extraActions(ctx) {
    return [
      el("button", {
        className: "btn btn-secondary",
        type: "button",
        text: "Show base",
        onClick: () => {
          showBase();
          ctx.rerender();
        },
      }),
      el("button", {
        className: "btn btn-primary",
        type: "button",
        text: "Apply delay edit (u1 1.2→2.0)",
        onClick: () => {
          applyEdit();
          ctx.rerender();
        },
      }),
    ];
  },
  renderWorkspace(ctx) {
    const arr = currentArr();
    const tags = {};
    if (arr) {
      for (const [p, v] of Object.entries(arr)) tags[p] = `A:${v}`;
    }
    const highlightPins =
      mode === "edited" && edited ? edited.invalidated : mode === "base" ? ["out"] : [];
    const highlightArcs =
      mode === "edited"
        ? [`${INC.editFrom}|${INC.editTo}`]
        : [];
    drawTimingGraph(ctx.canvas, timing, {
      levels,
      highlightPins,
      highlightArcs,
      tags,
    });
    const lines = [
      `view: ${mode}`,
      `edit: ${INC.editFrom}→${INC.editTo} delay ${INC.newDelay}`,
    ];
    if (mode === "base" && baseArr) {
      lines.push(`arrival out: ${baseArr.out}`);
      lines.push(`u1/Y: ${baseArr["u1/Y"]}`);
    }
    if (mode === "edited" && edited) {
      lines.push(`arrival out: ${edited.arrival.out}`);
      lines.push(`setup slack out: ${editedSlack()}`);
      lines.push(`invalidated: ${edited.invalidated.join(", ")}`);
      lines.push("arrival (invalidated cone):");
      for (const p of edited.invalidated) {
        lines.push(`  ${p}: ${edited.arrival[p] ?? "—"}`);
      }
    }
    ctx.metrics.innerHTML = "";
    ctx.metrics.append(metricsBlock(lines));
  },
});
