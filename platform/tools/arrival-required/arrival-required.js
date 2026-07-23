import {
  PROP_GOLDENS,
  near,
  propagateArrival,
  propagateRequired,
} from "../../assets/sta-core.js";
import {
  createInteractiveStaLab,
  valuesNear,
} from "../../assets/interactive-sta-lab.js";
import { el } from "../../assets/sta-ui.js";

const G = PROP_GOLDENS;
const root = document.getElementById("lab-root");

createInteractiveStaLab(root, {
  mode: "values",
  valueLabel: "A",
  valueStep: 0.1,
  initialValues: {},
  revealValues: G.arrival,
  starterHtml: `
    <p><strong>Your workspace:</strong> set <em>arrival</em> on each pin (A +/−),
    or use <em>Propagate arrival</em> / <em>Propagate required</em> helpers.
    Challenges check <strong>your</strong> values. Reveal golden is study-only.</p>
  `,
  getTags: (api) => {
    const tags = {};
    const kind = api.getMeta().tagKind || "A";
    for (const [p, v] of Object.entries(api.getValues())) {
      tags[p] = `${kind}:${v}`;
    }
    return tags;
  },
  extraActions: (ctx, api) => [
    el("button", {
      className: "btn btn-secondary",
      type: "button",
      text: "Propagate arrival",
      onClick: () => {
        const arr = propagateArrival(api.getTiming());
        api.setValues(arr || {});
        api.setMeta({ tagKind: "A" });
        api.setRevealed(false);
        ctx.rerender();
      },
    }),
    el("button", {
      className: "btn btn-secondary",
      type: "button",
      text: "Propagate required",
      onClick: () => {
        const req = propagateRequired(api.getTiming());
        api.setValues(req || {});
        api.setMeta({ tagKind: "R" });
        api.setRevealed(false);
        ctx.rerender();
      },
    }),
    el("button", {
      className: "btn btn-ghost",
      type: "button",
      text: "Switch to edit R",
      onClick: () => {
        api.setMeta({ tagKind: "R" });
        ctx.rerender();
      },
    }),
  ],
  challenges: [
    {
      id: "arr-in-0",
      title: "Arrival in = 0",
      level: "Intro",
      prompt: "Set arrival at in to 0.",
      hint: "Select in; A +/− to 0, or Propagate arrival.",
      check: (_c, api) => near(api.getValues().in ?? NaN, 0),
    },
    {
      id: "arr-out-32",
      title: "Arrival out = 3.2",
      level: "Intro",
      prompt: "Set arrival at out to 3.2.",
      hint: "Forward max: 0+1.2+0.3+1.5+0.2.",
      check: (_c, api) => near(api.getValues().out ?? NaN, G.arrival.out),
    },
    {
      id: "arr-u1y",
      title: "Arrival u1/Y = 1.2",
      level: "Practice",
      prompt: "Arrival at u1/Y equals 1.2.",
      hint: "Cell delay on u1/A→u1/Y.",
      check: (_c, api) => near(api.getValues()["u1/Y"] ?? NaN, G.arrival["u1/Y"]),
    },
    {
      id: "arr-all",
      title: "All arrivals",
      level: "Practice",
      prompt: "Match golden arrivals on every pin.",
      hint: "Propagate arrival, or enter by hand.",
      check: (_c, api) => valuesNear(api.getValues(), G.arrival),
    },
    {
      id: "req-out-10",
      title: "Required out = 10",
      level: "Practice",
      prompt: "Set required at out to period 10 (Propagate required).",
      hint: "Sink required = clock period.",
      check: (_c, api) =>
        api.getMeta().tagKind === "R" &&
        near(api.getValues().out ?? NaN, G.requiredSetup.out),
    },
    {
      id: "req-in-68",
      title: "Required in = 6.8",
      level: "Practice",
      prompt: "After required propagate, in required equals 6.8.",
      hint: "Backward min through delays.",
      check: (_c, api) =>
        api.getMeta().tagKind === "R" &&
        near(api.getValues().in ?? NaN, G.requiredSetup.in),
    },
    {
      id: "req-all",
      title: "All required",
      level: "Challenge",
      prompt: "Match golden setup required on every pin.",
      hint: "Propagate required.",
      check: (_c, api) =>
        api.getMeta().tagKind === "R" && valuesNear(api.getValues(), G.requiredSetup),
    },
    {
      id: "arr-u2a",
      title: "Arrival u2/A = 1.5",
      level: "Challenge",
      prompt: "Arrival at u2/A is 1.5.",
      hint: "1.2 + 0.3 net.",
      check: (_c, api) => near(api.getValues()["u2/A"] ?? NaN, G.arrival["u2/A"]),
    },
    {
      id: "req-u2y",
      title: "Required u2/Y = 9.8",
      level: "Challenge",
      prompt: "Required at u2/Y is 9.8.",
      hint: "10 − 0.2.",
      check: (_c, api) =>
        api.getMeta().tagKind === "R" &&
        near(api.getValues()["u2/Y"] ?? NaN, G.requiredSetup["u2/Y"]),
    },
    {
      id: "arr-u2y",
      title: "Arrival u2/Y = 3.0",
      level: "Challenge",
      prompt: "Arrival at u2/Y is 3.0.",
      hint: "1.5 + 1.5 cell.",
      check: (_c, api) => near(api.getValues()["u2/Y"] ?? NaN, G.arrival["u2/Y"]),
    },
  ],
});
