import {
  PROP_GOLDENS,
  analyzeSetup,
  near,
  propagateArrival,
  propagateRequired,
  setupSlack,
} from "../../assets/sta-core.js";
import { createInteractiveStaLab } from "../../assets/interactive-sta-lab.js";
import { el } from "../../assets/sta-ui.js";

const G = PROP_GOLDENS;
const root = document.getElementById("lab-root");

createInteractiveStaLab(root, {
  mode: "exceptions",
  initialDisabled: [],
  initialSetupCycles: 1,
  revealDisabled: G.falsePath.arcs.map(([a, b]) => `${a}|${b}`),
  revealSetupCycles: G.multicycle.setupCycles,
  starterHtml: `
    <p><strong>Your workspace:</strong> disable arcs for a <em>false path</em>, or raise
    <em>setup multicycle</em> cycles so required = cycles×period.
    Challenges check <strong>your</strong> disables / cycles (and resulting slack). Reveal golden is study-only.</p>
  `,
  extraActions: (ctx, api) => [
    el("button", {
      className: "btn btn-secondary",
      type: "button",
      text: "Analyze setup slack",
      onClick: () => {
        const t = api.getTiming();
        const disabled = [...api.getDisabledArcs()];
        const cycles = api.getSetupCycles();
        const arr = propagateArrival(t, { disableArcs: disabled });
        const req = propagateRequired(t, { disableArcs: disabled, setupCycles: cycles });
        const slack = arr && req ? setupSlack(arr, req, "out") : null;
        api.setMeta({ arr, req, slack });
        ctx.rerender();
      },
    }),
  ],
  extraMetrics: (api) => {
    const m = api.getMeta();
    return [
      m.slack == null && m.arr == null
        ? "slack: (run Analyze)"
        : `setup slack out: ${m.slack == null ? "untimed/null" : m.slack}`,
      m.req?.out != null ? `required out: ${m.req.out}` : null,
      m.arr?.out != null ? `arrival out: ${m.arr.out}` : null,
    ].filter(Boolean);
  },
  challenges: [
    {
      id: "default-slack",
      title: "Default slack 6.8",
      level: "Intro",
      prompt: "No disables, cycles=1: Analyze → setup slack out = 6.8.",
      hint: "Reset workspace, Analyze setup slack.",
      check: (_c, api) => {
        const t = api.getTiming();
        const r = analyzeSetup(t, { setupCycles: api.getSetupCycles() });
        return (
          api.getDisabledArcs().size === 0 &&
          api.getSetupCycles() === 1 &&
          r &&
          near(r.slackAtSink, G.setupSlackOut)
        );
      },
    },
    {
      id: "disable-net",
      title: "Disable u1/Y→u2/A",
      level: "Intro",
      prompt: "Disable the false-path arc u1/Y→u2/A.",
      hint: "Select that arc, Disable arc.",
      check: (_c, api) => api.getDisabledArcs().has("u1/Y|u2/A"),
    },
    {
      id: "false-untimed",
      title: "False path breaks chain slack",
      level: "Practice",
      prompt: "Disable u1/Y→u2/A; Analyze — setup slack out is no longer 6.8.",
      hint: "Disable false arc, Analyze setup slack.",
      check: (_c, api) => {
        if (!api.getDisabledArcs().has("u1/Y|u2/A")) return false;
        const r = analyzeSetup(api.getTiming(), {
          disableArcs: [...api.getDisabledArcs()],
          setupCycles: 1,
        });
        return !r || r.slackAtSink == null || !near(r.slackAtSink, G.setupSlackOut);
      },
    },
    {
      id: "mc-cycles-2",
      title: "Multicycle = 2",
      level: "Practice",
      prompt: "Set setup cycles to 2 (no false-path disable).",
      hint: "Cycles + until 2; clear disables.",
      check: (_c, api) =>
        api.getSetupCycles() === G.multicycle.setupCycles &&
        api.getDisabledArcs().size === 0,
    },
    {
      id: "mc-required-20",
      title: "Required out = 20",
      level: "Practice",
      prompt: "Cycles=2: Analyze → required out = 20.",
      hint: "Cycles + to 2, Analyze.",
      check: (_c, api) => {
        if (api.getSetupCycles() !== 2) return false;
        const req = propagateRequired(api.getTiming(), { setupCycles: 2 });
        return req && near(req.out, G.multicycle.requiredOut);
      },
    },
    {
      id: "mc-slack-168",
      title: "Multicycle slack 16.8",
      level: "Challenge",
      prompt: "Cycles=2, no disables: setup slack out = 16.8.",
      hint: "Analyze after setting cycles=2.",
      check: (_c, api) => {
        const r = analyzeSetup(api.getTiming(), { setupCycles: api.getSetupCycles() });
        return (
          api.getSetupCycles() === 2 &&
          api.getDisabledArcs().size === 0 &&
          r &&
          near(r.slackAtSink, G.multicycle.setupSlackOut)
        );
      },
    },
    {
      id: "cycles-at-least-2",
      title: "Cycles ≥ 2",
      level: "Challenge",
      prompt: "Setup cycles is at least 2.",
      hint: "Cycles +.",
      check: (_c, api) => api.getSetupCycles() >= 2,
    },
    {
      id: "reenable",
      title: "Re-enable all arcs",
      level: "Challenge",
      prompt: "No arcs disabled and cycles back to 1 with default slack 6.8.",
      hint: "Enable any disabled arc; Cycles − to 1.",
      check: (_c, api) => {
        const r = analyzeSetup(api.getTiming(), { setupCycles: 1 });
        return (
          api.getDisabledArcs().size === 0 &&
          api.getSetupCycles() === 1 &&
          r &&
          near(r.slackAtSink, G.setupSlackOut)
        );
      },
    },
    {
      id: "false-arc-only",
      title: "Only false arc disabled",
      level: "Challenge",
      prompt: "Exactly one disable: u1/Y|u2/A.",
      hint: "Disable that arc only.",
      check: (_c, api) => {
        const d = api.getDisabledArcs();
        return d.size === 1 && d.has("u1/Y|u2/A");
      },
    },
    {
      id: "mc-not-false",
      title: "Multicycle without false",
      level: "Challenge",
      prompt: "Cycles=2 and zero disabled arcs.",
      hint: "Clear disables; Cycles +.",
      check: (_c, api) =>
        api.getSetupCycles() === 2 && api.getDisabledArcs().size === 0,
    },
  ],
});
