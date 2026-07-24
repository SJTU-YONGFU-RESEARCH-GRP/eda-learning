import {
  PLACEMENT, drcSpacingLite, lRouteLayers, terminalsFromPositions
} from "../../assets/detailed-routing-core.js";
import { createInteractiveDetailedRoutingLab } from "../../assets/interactive-detailed-routing-lab.js";
import { el } from "../../assets/clustering-ui.js";

const root = document.getElementById("lab-root");
let lastDrc = { pass: true };

createInteractiveDetailedRoutingLab(root, {
  initialPositions: PLACEMENT,
  starterHtml: `<p><strong>Your job:</strong> run DRC on your routes. Toy checker flags adjacent parallel M1/M2 segments.</p>`,
  extraActions(_ctx, api) {
    return [el("button", {
      className: "btn btn-secondary", type: "button", text: "Check DRC",
      onClick: () => {
        const segs = api.getRoutes().flatMap(r => r.segments || []);
        lastDrc = drcSpacingLite(segs);
        _ctx.rerender();
      },
    })];
  },
  extraMetrics() {
    return [`DRC: ${lastDrc.pass ? "pass" : "fail"}`];
  },
  challenges: [
    { id: "spread-pass", title: "Spread layered passes", level: "Intro",
      prompt: "Spread A–C layered segments pass lite DRC.",
      check: () => {
        const t = terminalsFromPositions(PLACEMENT);
        return drcSpacingLite(lRouteLayers(t.A, t.C, "HV")).pass; } },
    { id: "violation-demo", title: "Violation demo", level: "Intro",
      prompt: "Parallel M1 rows one apart fail DRC.",
      check: () => !drcSpacingLite([
        { x: 1, y: 2, layer: "M1" }, { x: 2, y: 2, layer: "M1" },
        { x: 1, y: 3, layer: "M1" }, { x: 2, y: 3, layer: "M1" },
      ]).pass },
    { id: "route-first", title: "Route layered", level: "Practice",
      prompt: "Route layered before DRC.",
      setup: (_c, api) => api.routeLayered(),
      check: (_c, api) => api.getRoutes().some(r => r.segments?.length) },
    { id: "drc-btn", title: "Run Check DRC", level: "Practice",
      prompt: "Click Check DRC after routing.",
      setup: (_c, api) => {
        api.routeLayered();
        lastDrc = drcSpacingLite(api.getRoutes().flatMap(r => r.segments || []));
      },
      check: () => lastDrc.pass !== undefined },
    { id: "pass-after", title: "Spread routes pass", level: "Practice",
      prompt: "Spread layered routes pass lite DRC.",
      setup: (_c, api) => {
        api.routeLayered();
        lastDrc = drcSpacingLite(api.getRoutes().flatMap(r => r.segments || []));
      },
      check: () => lastDrc.pass === true },
    { id: "overflow-finite", title: "Overflow finite", level: "Intro",
      prompt: "Overflow finite after route.",
      setup: (_c, api) => api.routeLayered(),
      check: (_c, api) => Number.isFinite(api.getOverflow().total) },
    { id: "move-drc", title: "Re-check after move", level: "Challenge",
      prompt: "Move a cell, route, DRC still runs.",
      check: (_c, api) => {
        api.routeLayered();
        lastDrc = drcSpacingLite(api.getRoutes().flatMap(r => r.segments || []));
        return lastDrc.pass !== undefined; } },
    { id: "m2-check", title: "M2 violation demo", level: "Intro",
      prompt: "Adjacent M2 columns fail spacing.",
      check: () => !drcSpacingLite([
        { x: 2, y: 1, layer: "M2" }, { x: 2, y: 2, layer: "M2" },
        { x: 3, y: 1, layer: "M2" }, { x: 3, y: 2, layer: "M2" },
      ]).pass },
  ],
});
