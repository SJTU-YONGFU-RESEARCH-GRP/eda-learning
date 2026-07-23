import {
  PROP_GOLDENS,
  cloneTiming,
  fanoutCone,
  incrementalArrival,
  near,
  propagateArrival,
} from "../../assets/sta-core.js";
import { createInteractiveStaLab } from "../../assets/interactive-sta-lab.js";
import { el } from "../../assets/sta-ui.js";

const G = PROP_GOLDENS;
const INC = G.incremental;
const root = document.getElementById("lab-root");

createInteractiveStaLab(root, {
  mode: "cone",
  initialMarked: [],
  revealMarked: INC.invalidated,
  starterHtml: `
    <p><strong>Your workspace:</strong> bump cell delay <code>u1/A→u1/Y</code> from 1.2→2.0,
    then mark the <em>invalidated fanout cone</em> (click pins). Optional helpers apply the edit
    and mark the cone. Challenges check <strong>your</strong> marks and delay. Reveal golden is study-only.</p>
  `,
  extraActions: (ctx, api) => [
    el("button", {
      className: "btn btn-secondary",
      type: "button",
      text: "Bump u1 delay → 2.0",
      onClick: () => {
        const t = cloneTiming(api.getTiming());
        const arc = t.arcs.find((a) => a.from === INC.editFrom && a.to === INC.editTo);
        if (arc) arc.delay = INC.newDelay;
        api.setTiming(t);
        api.setMeta({ bumped: true });
        api.setRevealed(false);
        ctx.rerender();
      },
    }),
    el("button", {
      className: "btn btn-secondary",
      type: "button",
      text: "Mark fanout cone of u1/Y",
      onClick: () => {
        const cone = fanoutCone(api.getTiming(), INC.editTo);
        api.setMarked(cone);
        api.setRevealed(false);
        ctx.rerender();
      },
    }),
    el("button", {
      className: "btn btn-ghost",
      type: "button",
      text: "Apply incremental arrival",
      onClick: () => {
        const base = propagateArrival(api.getTiming());
        // ensure delay bumped
        let t = cloneTiming(api.getTiming());
        const arc = t.arcs.find((a) => a.from === INC.editFrom && a.to === INC.editTo);
        if (arc) arc.delay = INC.newDelay;
        api.setTiming(t);
        const baseOnOrig = propagateArrival(
          (() => {
            const o = cloneTiming(api.getTiming());
            const a = o.arcs.find((x) => x.from === INC.editFrom && x.to === INC.editTo);
            if (a) a.delay = 1.2;
            return o;
          })()
        );
        const res = incrementalArrival(t, { from: INC.editFrom, to: INC.editTo, delay: INC.newDelay }, baseOnOrig);
        api.setTiming(res.timing);
        api.setMarked(res.invalidated);
        api.setMeta({ arrival: res.arrival, bumped: true });
        api.setRevealed(false);
        ctx.rerender();
      },
    }),
  ],
  extraMetrics: (api) => {
    const t = api.getTiming();
    const arc = t.arcs.find((a) => a.from === INC.editFrom && a.to === INC.editTo);
    const lines = [`u1 cell delay: ${arc?.delay}`, `marked: ${[...api.getMarked()].sort().join(", ") || "(none)"}`];
    const arr = api.getMeta().arrival;
    if (arr?.out != null) lines.push(`arrival out (meta): ${arr.out}`);
    return lines;
  },
  challenges: [
    {
      id: "bump-delay",
      title: "Bump delay to 2.0",
      level: "Intro",
      prompt: "Set u1/A→u1/Y delay to 2.0.",
      hint: "Bump u1 delay → 2.0.",
      check: (_c, api) => {
        const arc = api.getTiming().arcs.find((a) => a.from === INC.editFrom && a.to === INC.editTo);
        return arc && near(arc.delay, INC.newDelay);
      },
    },
    {
      id: "mark-u1y",
      title: "Mark u1/Y",
      level: "Intro",
      prompt: "Mark pin u1/Y (edit target).",
      hint: "Click u1/Y.",
      check: (_c, api) => api.getMarked().has("u1/Y"),
    },
    {
      id: "mark-out",
      title: "Mark out",
      level: "Practice",
      prompt: "Mark out (downstream of the edit).",
      hint: "Fanout reaches out.",
      check: (_c, api) => api.getMarked().has("out"),
    },
    {
      id: "full-cone",
      title: "Full invalidated cone",
      level: "Practice",
      prompt: `Mark exactly {${INC.invalidated.join(", ")}}.`,
      hint: "Mark fanout cone of u1/Y.",
      check: (_c, api) => {
        const m = api.getMarked();
        return (
          INC.invalidated.every((p) => m.has(p)) &&
          m.size === INC.invalidated.length
        );
      },
    },
    {
      id: "not-in",
      title: "Do not mark in",
      level: "Practice",
      prompt: "Cone marked and in is not marked.",
      hint: "Upstream of edit stays valid.",
      check: (_c, api) => {
        const m = api.getMarked();
        return INC.invalidated.every((p) => m.has(p)) && !m.has("in");
      },
    },
    {
      id: "arrival-out-4",
      title: "Arrival out = 4.0",
      level: "Challenge",
      prompt: "After incremental update, arrival at out is 4.0.",
      hint: "Apply incremental arrival.",
      check: (_c, api) => near(api.getMeta().arrival?.out ?? NaN, INC.arrivalOut),
    },
    {
      id: "slack-6",
      title: "Setup slack out = 6.0",
      level: "Challenge",
      prompt: "After update, setup slack at out is 6.0 (10 − 4).",
      hint: "Apply incremental; slack = period − arrival.",
      check: (_c, api) => {
        const arr = api.getMeta().arrival?.out;
        return arr != null && near(10 - arr, INC.setupSlackOut);
      },
    },
    {
      id: "cone-has-u2",
      title: "Cone includes u2",
      level: "Challenge",
      prompt: "Marked set includes u2/A and u2/Y.",
      hint: "Both are downstream.",
      check: (_c, api) => api.getMarked().has("u2/A") && api.getMarked().has("u2/Y"),
    },
    {
      id: "bump-and-cone",
      title: "Bump + full cone",
      level: "Challenge",
      prompt: "Delay is 2.0 and cone matches golden invalidated set.",
      hint: "Bump then Mark fanout cone.",
      check: (_c, api) => {
        const arc = api.getTiming().arcs.find((a) => a.from === INC.editFrom && a.to === INC.editTo);
        const m = api.getMarked();
        return (
          arc &&
          near(arc.delay, INC.newDelay) &&
          INC.invalidated.every((p) => m.has(p)) &&
          m.size === INC.invalidated.length
        );
      },
    },
    {
      id: "u1a-not-invalid",
      title: "u1/A not invalidated",
      level: "Challenge",
      prompt: "Full cone marked; u1/A is not in the marked set.",
      hint: "Invalidation starts at arc.to = u1/Y.",
      check: (_c, api) => {
        const m = api.getMarked();
        return INC.invalidated.every((p) => m.has(p)) && !m.has("u1/A");
      },
    },
  ],
});
