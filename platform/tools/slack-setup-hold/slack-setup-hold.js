import {
  PROP_GOLDENS,
  near,
  propagateArrival,
  propagateRequired,
  setupSlack,
  holdSlack,
} from "../../assets/sta-core.js";
import { createInteractiveStaLab } from "../../assets/interactive-sta-lab.js";
import { el } from "../../assets/sta-ui.js";

const G = PROP_GOLDENS;
const root = document.getElementById("lab-root");

createInteractiveStaLab(root, {
  mode: "values",
  valueLabel: "S",
  valueStep: 0.1,
  initialValues: {},
  revealValues: { out: G.setupSlackOut },
  starterHtml: `
    <p><strong>Your workspace:</strong> compute and enter <em>slack</em> at pins
    (setup: R−A, hold: A−Rhold). Use helpers to fill arrivals/required first, then set slack at <code>out</code>.
    Challenges check <strong>your</strong> slack values. Reveal golden is study-only.</p>
  `,
  getTags: (api) => {
    const tags = {};
    for (const [p, v] of Object.entries(api.getValues())) tags[p] = `S:${v}`;
    const m = api.getMeta();
    if (m.arr && m.req) {
      for (const p of Object.keys(m.arr)) {
        if (tags[p]) continue;
        tags[p] = `A:${m.arr[p]}`;
      }
    }
    return tags;
  },
  extraActions: (ctx, api) => [
    el("button", {
      className: "btn btn-secondary",
      type: "button",
      text: "Fill A+R (setup)",
      onClick: () => {
        const t = api.getTiming();
        const arr = propagateArrival(t);
        const req = propagateRequired(t);
        api.setMeta({ arr, req, mode: "setup" });
        api.setValues({});
        api.setRevealed(false);
        ctx.rerender();
      },
    }),
    el("button", {
      className: "btn btn-secondary",
      type: "button",
      text: "Compute setup slack→values",
      onClick: () => {
        const t = api.getTiming();
        const arr = propagateArrival(t);
        const req = propagateRequired(t);
        const slack = {};
        for (const p of t.pins) {
          const s = setupSlack(arr, req, p.id);
          if (s != null) slack[p.id] = s;
        }
        api.setMeta({ arr, req, mode: "setup" });
        api.setValues(slack);
        api.setRevealed(false);
        ctx.rerender();
      },
    }),
    el("button", {
      className: "btn btn-ghost",
      type: "button",
      text: "Compute hold slack→values",
      onClick: () => {
        const t = api.getTiming();
        const arr = propagateArrival(t);
        const reqH = propagateRequired(t, { mode: "hold" });
        const slack = {};
        for (const p of t.pins) {
          const s = holdSlack(arr, reqH, p.id);
          if (s != null) slack[p.id] = s;
        }
        api.setMeta({ arr, req: reqH, mode: "hold" });
        api.setValues(slack);
        api.setRevealed(false);
        ctx.rerender();
      },
    }),
  ],
  extraMetrics: (api) => {
    const m = api.getMeta();
    const lines = [];
    if (m.arr?.out != null) lines.push(`arrival out: ${m.arr.out}`);
    if (m.req?.out != null) lines.push(`required out: ${m.req.out}`);
    if (api.getValues().out != null) lines.push(`your slack out: ${api.getValues().out}`);
    return lines;
  },
  challenges: [
    {
      id: "setup-out-68",
      title: "Setup slack out = 6.8",
      level: "Intro",
      prompt: "Enter setup slack at out = 6.8 (10 − 3.2).",
      hint: "Fill A+R, then set S at out, or Compute setup slack.",
      check: (_c, api) => near(api.getValues().out ?? NaN, G.setupSlackOut),
    },
    {
      id: "hold-out-32",
      title: "Hold slack out = 3.2",
      level: "Intro",
      prompt: "Enter hold slack at out = 3.2 (arrival − 0).",
      hint: "Compute hold slack→values.",
      check: (_c, api) =>
        api.getMeta().mode === "hold" && near(api.getValues().out ?? NaN, G.holdSlackOut),
    },
    {
      id: "setup-positive",
      title: "Setup meets",
      level: "Practice",
      prompt: "Setup slack at out is positive (meets).",
      hint: "6.8 > 0.",
      check: (_c, api) => (api.getValues().out ?? -1) > 0,
    },
    {
      id: "setup-in",
      title: "Setup slack at in",
      level: "Practice",
      prompt: "Setup slack at in equals 6.8 (same as path slack on this chain).",
      hint: "Compute setup slack→values.",
      check: (_c, api) => near(api.getValues().in ?? NaN, G.setupSlackOut),
    },
    {
      id: "formula-setup",
      title: "R − A at out",
      level: "Practice",
      prompt: "With A+R filled, your slack out equals required−arrival.",
      hint: "Fill A+R, set S=out R−A by hand.",
      check: (_c, api) => {
        const m = api.getMeta();
        if (!m.arr || !m.req) return false;
        const expect = setupSlack(m.arr, m.req, "out");
        return near(api.getValues().out ?? NaN, expect);
      },
    },
    {
      id: "all-setup-slacks",
      title: "All setup slacks",
      level: "Challenge",
      prompt: "Every pin has setup slack 6.8 on this pure chain.",
      hint: "Compute setup slack→values.",
      check: (_c, api) => {
        const v = api.getValues();
        const t = api.getTiming();
        return t.pins.every((p) => near(v[p.id] ?? NaN, G.setupSlackOut));
      },
    },
    {
      id: "hold-positive",
      title: "Hold meets at out",
      level: "Challenge",
      prompt: "Hold slack at out is positive.",
      hint: "Compute hold slack.",
      check: (_c, api) =>
        api.getMeta().mode === "hold" && (api.getValues().out ?? -1) > 0,
    },
    {
      id: "setup-not-hold",
      title: "Setup ≠ hold number",
      level: "Challenge",
      prompt: "Your out slack equals setup 6.8 (not hold 3.2).",
      hint: "Use setup path.",
      check: (_c, api) =>
        near(api.getValues().out ?? NaN, G.setupSlackOut) &&
        !near(api.getValues().out, G.holdSlackOut),
    },
    {
      id: "u1y-setup",
      title: "Slack at u1/Y",
      level: "Challenge",
      prompt: "Setup slack at u1/Y is 6.8.",
      hint: "Compute setup slack→values.",
      check: (_c, api) => near(api.getValues()["u1/Y"] ?? NaN, G.setupSlackOut),
    },
    {
      id: "period-used",
      title: "Period 10 in play",
      level: "Challenge",
      prompt: "After Fill A+R, required out is 10 and your setup slack out is 6.8.",
      hint: "Fill A+R then set slack.",
      check: (_c, api) => {
        const m = api.getMeta();
        return (
          m.req &&
          near(m.req.out, G.period) &&
          near(api.getValues().out ?? NaN, G.setupSlackOut)
        );
      },
    },
  ],
});
